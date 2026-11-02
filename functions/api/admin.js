// GET /api/admin?kind=log|inbox|stats&limit=50   Authorization: Bearer <ADMIN_TOKEN>
// Disabled (404) unless ADMIN_TOKEN is set. Read it with tools/ask_admin.py.

import { makeStore, safeEqual } from '../../ask/lib/auth.js';

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
}

export async function onRequestGet(context) {
  const { env, request } = context;
  if (!env.ADMIN_TOKEN) return json({ error: 'not_found' }, 404);
  const auth = request.headers.get('authorization') || '';
  if (!safeEqual(auth, `Bearer ${env.ADMIN_TOKEN}`)) return json({ error: 'unauthorized' }, 401);

  const url = new URL(request.url);
  const kind = url.searchParams.get('kind') || 'log';
  const limit = Math.min(Number(url.searchParams.get('limit') || 50), 500);
  const store = makeStore(env);
  const prefix = kind === 'inbox' ? 'inbox:' : 'log:';
  const keys = await store.list(prefix, kind === 'stats' ? 500 : limit);
  const items = [];
  for (const k of keys) {
    const v = await store.get(k);
    if (v) { try { items.push(JSON.parse(v)); } catch {} }
  }
  if (kind !== 'stats') return json({ storage: store.kind, count: items.length, items });

  const stats = { storage: store.kind, answers: items.length, by_verdict: {}, by_mode: {}, cost_usd: 0, avg_ttfb_ms: null, avg_total_ms: null };
  let ttfbSum = 0, ttfbN = 0, totSum = 0, totN = 0;
  for (const it of items) {
    const r = it.receipt || {};
    stats.by_verdict[r.verdict] = (stats.by_verdict[r.verdict] || 0) + 1;
    stats.by_mode[it.mode] = (stats.by_mode[it.mode] || 0) + 1;
    if (typeof r.cost_usd === 'number') stats.cost_usd += r.cost_usd;
    if (typeof r.ttfb_ms === 'number') { ttfbSum += r.ttfb_ms; ttfbN++; }
    if (typeof r.total_ms === 'number') { totSum += r.total_ms; totN++; }
  }
  stats.cost_usd = Math.round(stats.cost_usd * 10000) / 10000;
  stats.avg_ttfb_ms = ttfbN ? Math.round(ttfbSum / ttfbN) : null;
  stats.avg_total_ms = totN ? Math.round(totSum / totN) : null;
  return json(stats);
}
