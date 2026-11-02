// Tokenizer + BM25 over the prebuilt corpus (public/ask/index.json).
// The tokenizer MUST stay identical to tokenize() in build.py: the index's term
// frequencies are computed in Python at build time, queries are tokenized here.

const TOKEN_RE = /[a-z0-9]+(?:[.\-_][a-z0-9]+)*|[㐀-鿿豈-﫿]+/gu;
const CJK_RE = /^[㐀-鿿豈-﫿]+$/u;
const DIGITS_RE = /^\d+$/;

export const STOPWORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can', 'do', 'does', 'did', 'for', 'from',
  'has', 'have', 'he', 'his', 'him', 'how', 'i', 'in', 'is', 'it', 'its', 'me', 'my', 'of',
  'on', 'or', 'she', 'so', 'that', 'the', 'their', 'there', 'this', 'to', 'was', 'what',
  'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your', 'about', 'tell',
]);

export function tokenize(text) {
  const out = [];
  const lower = String(text || '').toLowerCase();
  for (const m of lower.matchAll(TOKEN_RE)) {
    const s = m[0];
    if (CJK_RE.test(s)) {
      const chars = Array.from(s);
      if (chars.length === 1) out.push(s);
      else for (let i = 0; i < chars.length - 1; i++) out.push(chars[i] + chars[i + 1]);
    } else if ((s.length > 1 && !STOPWORDS.has(s)) || DIGITS_RE.test(s)) {
      out.push(s);
    }
  }
  return out;
}

// BM25 (k1 = 1.2, b = 0.75). index = { chunks: [{ id, tf: {term: n}, len }], df, n, avgdl }
export function bm25(index, query, k = 5) {
  const terms = [...new Set(tokenize(query))];
  if (!terms.length) return [];
  const { df, n, avgdl } = index;
  const k1 = 1.2, b = 0.75;
  const scored = [];
  for (const c of index.chunks) {
    let score = 0;
    for (const t of terms) {
      const f = c.tf[t];
      if (!f) continue;
      const d = df[t] || 0;
      const idf = Math.log((n - d + 0.5) / (d + 0.5) + 1);
      score += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * (c.len / avgdl)));
    }
    if (score > 0) scored.push({ id: c.id, score });
  }
  scored.sort((a, b2) => b2.score - a.score);
  return scored.slice(0, k);
}

// Rough token estimate, used only to decide between full-context and top-k retrieval.
export function estimateTokens(text) {
  const s = String(text || '');
  const cjk = (s.match(/[㐀-鿿豈-﫿]/gu) || []).length;
  const words = (s.replace(/[㐀-鿿豈-﫿]/gu, ' ').match(/\S+/g) || []).length;
  return Math.ceil(cjk * 1.1 + words * 1.4);
}
