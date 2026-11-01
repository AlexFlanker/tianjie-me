// POST /api/ask  { q, lang?, invite?, turnstile? }  ->  text/event-stream
//   meta        { mode, label, quota_left, provider, model, demo }
//   candidates  [{ n, id, title, url, date }]   (BM25 preview, within ~100 ms)
//   delta       { t }                            (raw model text while it streams)
//   done        { answer, sources, receipt, quota_left }
// GET /api/ask[?i=token] -> status (provider, corpus, quota) without secrets.

import { bm25 } from '../../ask/lib/text.js';
import {
  SYSTEM_RULES, buildSourcesBlock, detectHandoff, handoffMessage, noSourceMessage,
  blockedMessage, validateAnswer, isChinese,
} from '../../ask/lib/policy.js';
import { pickProvider, estimateCost } from '../../ask/lib/providers.js';
import { makeStore, verifyInvite, visitorKey, readCount, verifyTurnstile, today } from '../../ask/lib/auth.js';

const DAY = 86400;
let CORPUS = null;
let CORPUS_AT = 0;

async function loadCorpus(context) {
  if (CORPUS && Date.now() - CORPUS_AT < 5 * 60 * 1000) return CORPUS;
  const res = await context.env.ASSETS.fetch(new URL('/ask/index.json', context.request.url));
  if (!res.ok) throw new Error(`corpus not found (${res.status})`);
  CORPUS = await res.json();
  CORPUS_AT = Date.now();
  return CORPUS;
}

function limits(env, invite) {
  if (invite && invite.ok) return invite.quota || Number(env.INVITE_DAILY || 30);
  return Number(env.ANON_DAILY || 5);
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
}

export async function onRequestGet(context) {
  const { env, request } = context;
  const url = new URL(request.url);
  const token = url.searchParams.get('i') || '';
  const invite = token ? await verifyInvite(token, env.INVITE_SECRET) : null;
  const store = makeStore(env);
  const vkey = await visitorKey(request, env, invite, token);
  const used = await readCount(store, `quota:${today()}:${vkey}`);
  const limit = limits(env, invite);
  const provider = pickProvider(env);
  let corpus = null;
  try { const c = await loadCorpus(context); corpus = { version: c.version, built: c.built, chunks: c.chunks.length }; } catch (e) { corpus = { error: String(e.message || e) }; }
  return json({
    ok: true, provider: provider.name, model: provider.model, demo: provider.demo, storage: store.kind,
    mode: invite && invite.ok ? 'invite' : 'anonymous', label: invite && invite.ok ? invite.label : null,
    invite_error: invite && !invite.ok ? invite.reason : null,
    quota: { limit, used, left: Math.max(0, limit - used) }, corpus,
    turnstile: !!env.TURNSTILE_SECRET,
  });
}

export async function onRequestPost(context) {
  const { env, request } = context;
  let body;
  try { body = await request.json(); } catch { return json({ error: 'bad_json' }, 400); }
  const q = String(body.q || '').trim();
  if (!q) return json({ error: 'empty' }, 400);
  if (q.length > 500) return json({ error: 'too_long', max: 500 }, 400);
  const lang = isChinese(q) ? 'zh' : (body.lang === 'zh' ? 'zh' : 'en');

  const token = String(body.invite || '');
  const invite = token ? await verifyInvite(token, env.INVITE_SECRET) : null;
  const mode = invite && invite.ok ? 'invite' : 'anonymous';
  const ip = request.headers.get('CF-Connecting-IP') || '';
  if (mode === 'anonymous' && !(await verifyTurnstile(env, body.turnstile, ip))) return json({ error: 'turnstile' }, 403);

  const store = makeStore(env);
  const vkey = await visitorKey(request, env, invite, token);
  const quotaKey = `quota:${today()}:${vkey}`;
  const limit = limits(env, invite);
  const used = await readCount(store, quotaKey);
  if (used >= limit) return json({ error: 'quota', limit, left: 0 }, 429);

  const provider = pickProvider(env);
  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();
  const te = new TextEncoder();
  const send = (event, data) => writer.write(te.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`));

  const answerId = crypto.randomUUID().slice(0, 8);
  const t0 = Date.now();

  const run = async () => {
    let receipt = { id: answerId, at: new Date().toISOString(), mode, provider: provider.name, model: provider.model, demo: provider.demo, storage: store.kind };
    let answer = '';
    let sourcesOut = [];
    let charged = false;
    try {
      await writer.write(te.encode(': stream open\n\n'));
      await send('meta', { mode, label: mode === 'invite' ? invite.label : null, quota_left: limit - used, provider: provider.name, model: provider.model, demo: provider.demo });

      // 1. questions the agent never answers
      const topic = detectHandoff(q);
      if (topic) {
        receipt = { ...receipt, verdict: 'HANDOFF', topic, total_ms: Date.now() - t0 };
        answer = handoffMessage(lang);
        return;
      }

      // 2. context: whole corpus while it is small (stable -> cacheable), top-k when it grows
      const corpus = await loadCorpus(context);
      const fullMax = Number(env.FULL_CONTEXT_MAX_TOKENS || 60000);
      let sources;
      let cacheable;
      if ((corpus.est_tokens || 0) <= fullMax) {
        sources = corpus.chunks;
        cacheable = true;
      } else {
        const hits = bm25(corpus, q, 12).map(h => h.id);
        const ids = [...new Set([...(corpus.core || []), ...hits])];
        sources = ids.map(id => corpus.chunks.find(c => c.id === id)).filter(Boolean);
        cacheable = false;
      }
      const pos = new Map(sources.map((s, i) => [s.id, i + 1]));
      const candidates = bm25(corpus, q, 5)
        .filter(h => pos.has(h.id))
        .map(h => { const s = sources[pos.get(h.id) - 1]; return { n: pos.get(h.id), id: s.id, title: s.title, url: s.url, date: s.date }; });
      await send('candidates', candidates);

      // 3. the model
      const user = (mode === 'invite' ? `Visitor context: invited link "${invite.label}" (recruiter or referrer).\n\n` : '') + `Question: ${q}`;
      let raw = '';
      let usage = null;
      let ttfb = null;
      for await (const ev of provider.stream({ systemRules: SYSTEM_RULES, sourcesBlock: buildSourcesBlock(sources), cacheable, user, maxTokens: 800, candidates, sources, lang })) {
        if (ev.type === 'delta') {
          if (ttfb === null) ttfb = Date.now() - t0;
          raw += ev.text;
          await send('delta', { t: ev.text });
        } else if (ev.type === 'usage') {
          usage = ev.usage;
        }
      }
      charged = true;

      // 4. the check
      const v = validateAnswer(raw, sources.length);
      let verdict = v.verdict;
      if (verdict === 'NO_SOURCE') answer = noSourceMessage(lang, v.text);
      else if (verdict === 'UNCITED') answer = blockedMessage(lang);
      else answer = v.text;
      sourcesOut = verdict === 'ALL_CITED' || verdict === 'PARTIAL'
        ? v.cited.map(n => { const s = sources[n - 1]; return { n, id: s.id, title: s.title, url: s.url, date: s.date }; })
        : [];
      receipt = {
        ...receipt, verdict, corpus_version: corpus.version, context: cacheable ? 'full' : 'top-k',
        sources_in_context: sources.length, cited: sourcesOut.map(s => s.id), checks: v.checks,
        ttfb_ms: ttfb, total_ms: Date.now() - t0,
        tokens: usage, cost_usd: estimateCost(provider.model, usage),
      };
      if (verdict === 'UNCITED') receipt.blocked_text_chars = raw.length;
    } catch (e) {
      receipt = { ...receipt, verdict: 'ERROR', error: String(e && e.message || e).slice(0, 300), total_ms: Date.now() - t0 };
      answer = lang === 'zh' ? '出错了，这次不扣次数。稍后再试，或在下面留言。' : 'Something went wrong; this one does not count against your quota. Try again later, or leave a note below.';
      charged = false;
    } finally {
      let left = limit - used;
      try {
        if (charged && receipt.verdict !== 'ERROR') {
          await store.put(quotaKey, String(used + 1), 2 * DAY);
          left = limit - used - 1;
        }
        await store.put(`log:${receipt.at}:${answerId}`, JSON.stringify({ q, lang, mode, label: mode === 'invite' ? invite.label : null, receipt }), 30 * DAY);
      } catch (e) {
        console.log(JSON.stringify({ ask_log_error: String(e) }));
      }
      console.log(JSON.stringify({ ask: { id: answerId, verdict: receipt.verdict, mode, model: receipt.model, total_ms: receipt.total_ms, cost: receipt.cost_usd } }));
      try { await send('done', { answer, sources: sourcesOut, receipt, quota_left: Math.max(0, left) }); } catch {}
      try { await writer.close(); } catch {}
    }
  };

  context.waitUntil(run());
  return new Response(readable, {
    headers: {
      'content-type': 'text/event-stream; charset=utf-8',
      'cache-control': 'no-store, no-transform',
      'x-accel-buffering': 'no',
    },
  });
}
