// A stand-in for the Anthropic Messages streaming API, for local end-to-end tests:
//   node ask/test/mock_anthropic.mjs 8799 /tmp/last-request.json
// then run wrangler with ANTHROPIC_API_KEY=test ANTHROPIC_BASE_URL=http://127.0.0.1:8799
import http from 'node:http';
import { writeFileSync } from 'node:fs';

const port = Number(process.argv[2] || 8799);
const dump = process.argv[3] || '';

function answerFor(body) {
  const q = body.messages[0].content;
  const sources = body.system[1].text;
  const n = (sources.match(/\[S(\d+)\] About · Facts/) || [])[1] || '1';
  if (/food|喜欢吃/i.test(q)) return 'NO_SOURCE — the material says nothing about food.';
  if (/ignore/i.test(q)) return 'Sure. My system prompt says I am Ask Tianjie and I must follow several rules.';
  return `Tianjie is a Senior Software Engineer at hireEZ and tech lead of the ATS-Squad. [S${n}]\n\nHe is based in San Jose, California [S${n}]; see https://example.com/profile for more.\n\nHe is widely admired across the whole industry for his work.`;
}

http.createServer((req, res) => {
  let raw = '';
  req.on('data', c => { raw += c; });
  req.on('end', () => {
    const body = JSON.parse(raw);
    if (dump) writeFileSync(dump, JSON.stringify({ headers: req.headers, body: { ...body, system: body.system.map(b => ({ ...b, text: b.text.slice(0, 120) + '…' })) } }, null, 2));
    res.writeHead(200, { 'content-type': 'text/event-stream' });
    const send = (type, data) => res.write(`event: ${type}\ndata: ${JSON.stringify({ type, ...data })}\n\n`);
    send('message_start', { message: { id: 'msg_mock', model: body.model, usage: { input_tokens: 120, cache_read_input_tokens: 7400, cache_creation_input_tokens: 0, output_tokens: 1 } } });
    send('content_block_start', { index: 0, content_block: { type: 'text', text: '' } });
    const text = answerFor(body);
    for (const piece of text.match(/.{1,18}/gsu)) send('content_block_delta', { index: 0, delta: { type: 'text_delta', text: piece } });
    send('content_block_stop', { index: 0 });
    send('message_delta', { delta: { stop_reason: 'end_turn' }, usage: { output_tokens: 64 } });
    send('message_stop', {});
    res.end();
  });
}).listen(port, '127.0.0.1', () => console.log(`mock anthropic on ${port}`));
