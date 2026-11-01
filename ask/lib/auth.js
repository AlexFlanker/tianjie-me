// Access tiers without an account system:
//   anonymous  -> daily quota keyed by a salted, daily-rotating IP hash (IP itself never stored)
//   invite     -> signed link (?i=token) made by tools/ask_invite.py; higher quota, recruiter mode
//   admin      -> bearer ADMIN_TOKEN for /api/admin
// Storage is the ASK_KV namespace when bound, otherwise an in-memory map (demo/preview only).

const enc = new TextEncoder();

export function b64urlEncode(bytes) {
  let s = '';
  const arr = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  for (const b of arr) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function b64urlDecodeToString(s) {
  const pad = s.length % 4 ? '='.repeat(4 - (s.length % 4)) : '';
  const bin = atob(s.replace(/-/g, '+').replace(/_/g, '/') + pad);
  const bytes = Uint8Array.from(bin, c => c.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

async function hmac(secret, message) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return new Uint8Array(await crypto.subtle.sign('HMAC', key, enc.encode(message)));
}

export function safeEqual(a, b) {
  a = String(a || ''); b = String(b || '');
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

// token = base64url(JSON payload) + "." + base64url(HMAC-SHA256(secret, base64url payload))
// payload = { v: 1, l: label, e: expiry unix seconds, q: daily quota }
export async function verifyInvite(token, secret, nowSec = Math.floor(Date.now() / 1000)) {
  if (!token || !secret) return { ok: false, reason: token ? 'invites disabled' : 'no token' };
  const parts = String(token).split('.');
  if (parts.length !== 2) return { ok: false, reason: 'malformed' };
  const expected = b64urlEncode(await hmac(secret, parts[0]));
  if (!safeEqual(expected, parts[1])) return { ok: false, reason: 'bad signature' };
  let p;
  try { p = JSON.parse(b64urlDecodeToString(parts[0])); } catch { return { ok: false, reason: 'malformed' }; }
  if (!p || p.v !== 1) return { ok: false, reason: 'version' };
  if (p.e && nowSec > p.e) return { ok: false, reason: 'expired' };
  return { ok: true, label: String(p.l || '').slice(0, 80), quota: Number(p.q) || 0, exp: p.e || null };
}

export async function sha256hex(text) {
  const d = await crypto.subtle.digest('SHA-256', enc.encode(text));
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('');
}

export function today() { return new Date().toISOString().slice(0, 10); }

export async function visitorKey(request, env, invite, token) {
  if (invite && invite.ok) return `inv:${(await sha256hex(token)).slice(0, 16)}`;
  const ip = request.headers.get('CF-Connecting-IP') || request.headers.get('x-forwarded-for') || 'local';
  return `ip:${(await sha256hex(`${ip}|${env.IP_SALT || 'tianjie.me'}|${today()}`)).slice(0, 16)}`;
}

// ---------- storage ----------
const MEMORY = new Map();
export function makeStore(env) {
  const kv = env.ASK_KV;
  if (kv) {
    return {
      kind: 'kv',
      get: k => kv.get(k),
      put: (k, v, ttl) => kv.put(k, v, ttl ? { expirationTtl: ttl } : undefined),
      list: async (prefix, limit = 100) => {
        const out = []; let cursor;
        do {
          const r = await kv.list({ prefix, cursor, limit: 1000 });
          out.push(...r.keys.map(k => k.name)); cursor = r.list_complete ? null : r.cursor;
        } while (cursor && out.length < 5000);
        return out.sort().reverse().slice(0, limit);
      },
    };
  }
  return {
    kind: 'memory',
    get: async k => (MEMORY.has(k) ? MEMORY.get(k) : null),
    put: async (k, v) => { MEMORY.set(k, v); },
    list: async (prefix, limit = 100) => [...MEMORY.keys()].filter(k => k.startsWith(prefix)).sort().reverse().slice(0, limit),
  };
}

export async function readCount(store, key) {
  const v = await store.get(key);
  return v ? Number(v) || 0 : 0;
}

// ---------- optional Cloudflare Turnstile (only when TURNSTILE_SECRET is set) ----------
export async function verifyTurnstile(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return true;
  if (!token) return false;
  const form = new FormData();
  form.append('secret', env.TURNSTILE_SECRET);
  form.append('response', token);
  if (ip) form.append('remoteip', ip);
  try {
    const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const j = await r.json();
    return !!j.success;
  } catch { return false; }
}
