// POST /api/contact  { email, message, question?, answer_id?, invite? }
// The conversion point: a visitor leaves an email, Tianjie replies himself.
// Stored under inbox:<iso>:<id> for 180 days; optional NOTIFY_WEBHOOK gets a short ping.

import { makeStore, verifyInvite, visitorKey, readCount, today } from '../../ask/lib/auth.js';

const EMAIL_RE = /^[^\s@<>()]+@[^\s@<>()]+\.[^\s@<>()]{2,}$/;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
}

export async function onRequestPost(context) {
  const { env, request } = context;
  let b;
  try { b = await request.json(); } catch { return json({ error: 'bad_json' }, 400); }
  const email = String(b.email || '').trim().slice(0, 200);
  const message = String(b.message || '').trim().slice(0, 2000);
  if (!EMAIL_RE.test(email)) return json({ error: 'email' }, 400);

  const token = String(b.invite || '');
  const invite = token ? await verifyInvite(token, env.INVITE_SECRET) : null;
  const store = makeStore(env);
  const vkey = await visitorKey(request, env, invite, token);
  const rateKey = `contact:${today()}:${vkey}`;
  const sent = await readCount(store, rateKey);
  if (sent >= 5) return json({ error: 'rate' }, 429);

  const id = crypto.randomUUID().slice(0, 8);
  const at = new Date().toISOString();
  const record = {
    id, at, email, message,
    question: String(b.question || '').slice(0, 500),
    answer_id: String(b.answer_id || '').slice(0, 16),
    invite_label: invite && invite.ok ? invite.label : null,
  };
  await store.put(`inbox:${at}:${id}`, JSON.stringify(record), 180 * 86400);
  await store.put(rateKey, String(sent + 1), 2 * 86400);

  if (env.NOTIFY_WEBHOOK) {
    const text = `tianjie.me/ask 新留言${record.invite_label ? `（邀请：${record.invite_label}）` : ''}：${email}\n${message || '(无留言)'}${record.question ? `\n问题：${record.question}` : ''}`;
    context.waitUntil(fetch(env.NOTIFY_WEBHOOK, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text, content: text }),
    }).catch(() => {}));
  }
  return json({ ok: true, id });
}
