// Model providers behind one streaming interface:
//   for await (const ev of provider.stream({ system, user, maxTokens })) { ev.type === 'delta' | 'usage' }
// Switch with env ASK_PROVIDER = anthropic | openai | mock, and ASK_MODEL.
// Public traffic must use an API key (Anthropic's Agent SDK note: products may not
// use claude.ai login or subscription limits), never a personal subscription.

// USD per million tokens: [input, output, cache read, cache write (5 min)]
// From platform.claude.com/docs/en/about-claude/pricing (checked 2026-10-31).
const PRICES = {
  'claude-haiku-5-5': [0.10, 0.50, 0.01, 0.125],
  'claude-sonnet-5-5': [2, 10, 0.10, 2.5],
  'claude-opus-5-5': [4, 20, 0.20, 5],
};

export function estimateCost(model, usage) {
  const p = PRICES[model];
  if (!p || !usage) return null;
  const c = ((usage.input || 0) * p[0] + (usage.output || 0) * p[1] + (usage.cache_read || 0) * p[2] + (usage.cache_write || 0) * p[3]) / 1e6;
  return Math.round(c * 1e6) / 1e6;
}

export function pickProvider(env) {
  const want = (env.ASK_PROVIDER || '').toLowerCase();
  if ((want === 'anthropic' || !want) && env.ANTHROPIC_API_KEY) {
    return anthropicProvider(env.ANTHROPIC_API_KEY, env.ASK_MODEL || 'claude-haiku-5-5', env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com');
  }
  if ((want === 'openai' || !want) && env.OPENAI_COMPAT_API_KEY) {
    return openaiProvider(env.OPENAI_COMPAT_API_KEY, env.OPENAI_COMPAT_BASE_URL || 'https://openrouter.ai/api/v1', env.ASK_MODEL || 'deepseek/deepseek-chat');
  }
  return mockProvider();
}

// ---------- SSE parsing shared by the two HTTP providers ----------
async function* sseEvents(response) {
  const reader = response.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    let i;
    while ((i = buf.indexOf('\n\n')) >= 0) {
      const block = buf.slice(0, i); buf = buf.slice(i + 2);
      let event = 'message'; const data = [];
      for (const line of block.split('\n')) {
        if (line.startsWith('event:')) event = line.slice(6).trim();
        else if (line.startsWith('data:')) data.push(line.slice(5).trimStart());
      }
      if (data.length) yield { event, data: data.join('\n') };
    }
  }
}

async function failIfBad(res, who) {
  if (res.ok) return;
  const body = (await res.text()).slice(0, 300);
  throw new Error(`${who} ${res.status}: ${body}`);
}

// ---------- Anthropic Messages API ----------
function anthropicProvider(apiKey, model, baseUrl) {
  return {
    name: 'anthropic', model, demo: false,
    async *stream({ systemRules, sourcesBlock, cacheable, user, maxTokens = 800 }) {
      const system = [
        { type: 'text', text: systemRules },
        { type: 'text', text: sourcesBlock, ...(cacheable ? { cache_control: { type: 'ephemeral' } } : {}) },
      ];
      const res = await fetch(`${baseUrl.replace(/\/$/, '')}/v1/messages`, {
        method: 'POST',
        headers: { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
        body: JSON.stringify({ model, max_tokens: maxTokens, temperature: 0.2, stream: true, system, messages: [{ role: 'user', content: user }] }),
      });
      await failIfBad(res, 'anthropic');
      const usage = { input: 0, output: 0, cache_read: 0, cache_write: 0 };
      for await (const ev of sseEvents(res)) {
        let d; try { d = JSON.parse(ev.data); } catch { continue; }
        if (d.type === 'message_start' && d.message && d.message.usage) {
          const u = d.message.usage;
          usage.input = u.input_tokens || 0;
          usage.cache_read = u.cache_read_input_tokens || 0;
          usage.cache_write = u.cache_creation_input_tokens || 0;
        } else if (d.type === 'content_block_delta' && d.delta && d.delta.type === 'text_delta') {
          yield { type: 'delta', text: d.delta.text };
        } else if (d.type === 'message_delta' && d.usage) {
          usage.output = d.usage.output_tokens || usage.output;
        } else if (d.type === 'error') {
          throw new Error(`anthropic stream error: ${JSON.stringify(d.error).slice(0, 200)}`);
        }
      }
      yield { type: 'usage', usage };
    },
  };
}

// ---------- any OpenAI-compatible endpoint (OpenRouter, DeepSeek, StepFun ...) ----------
function openaiProvider(apiKey, baseUrl, model) {
  return {
    name: 'openai', model, demo: false,
    async *stream({ systemRules, sourcesBlock, user, maxTokens = 800 }) {
      const res = await fetch(`${baseUrl.replace(/\/$/, '')}/chat/completions`, {
        method: 'POST',
        headers: { authorization: `Bearer ${apiKey}`, 'content-type': 'application/json' },
        body: JSON.stringify({
          model, max_tokens: maxTokens, temperature: 0.2, stream: true, stream_options: { include_usage: true },
          messages: [{ role: 'system', content: `${systemRules}\n\n${sourcesBlock}` }, { role: 'user', content: user }],
        }),
      });
      await failIfBad(res, 'openai-compatible');
      const usage = { input: 0, output: 0, cache_read: 0, cache_write: 0 };
      for await (const ev of sseEvents(res)) {
        if (ev.data === '[DONE]') break;
        let d; try { d = JSON.parse(ev.data); } catch { continue; }
        const delta = d.choices && d.choices[0] && d.choices[0].delta && d.choices[0].delta.content;
        if (delta) yield { type: 'delta', text: delta };
        if (d.usage) { usage.input = d.usage.prompt_tokens || 0; usage.output = d.usage.completion_tokens || 0; }
      }
      yield { type: 'usage', usage };
    },
  };
}

// ---------- demo mode: no key configured. Stitches an answer from the top sources ----------
function mockProvider() {
  return {
    name: 'mock', model: 'demo (no model key)', demo: true,
    async *stream({ candidates, sources, lang }) {
      const top = (candidates || []).slice(0, 2);
      let text;
      if (!top.length) {
        text = 'NO_SOURCE (demo mode: no matching material)';
      } else {
        const lines = top.map(c => {
          const s = sources[c.n - 1];
          const snippet = String(s.text).replace(/\s+/g, ' ').slice(0, 140);
          return `${lang === 'zh' ? '（演示模式，未接模型）相关材料：' : '(Demo mode, no model connected) Relevant material: '}${snippet}… [S${c.n}]`;
        });
        text = lines.join('\n\n');
      }
      for (const piece of text.match(/.{1,24}/gsu) || []) {
        yield { type: 'delta', text: piece };
        await new Promise(r => setTimeout(r, 15));
      }
      yield { type: 'usage', usage: { input: 0, output: 0, cache_read: 0, cache_write: 0 } };
    },
  };
}
