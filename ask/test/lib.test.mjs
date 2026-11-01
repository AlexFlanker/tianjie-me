// node --test ask/test/   (run `python3 build.py` first: some tests read public/ask/index.json)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { tokenize, bm25 } from '../lib/text.js';
import { validateAnswer, detectHandoff, buildSourcesBlock } from '../lib/policy.js';
import { verifyInvite } from '../lib/auth.js';
import { estimateCost } from '../lib/providers.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

test('tokenizer matches the Python one used at build time', () => {
  const samples = [
    'What does Tianjie do at hireEZ?', '天杰在 hireEZ 负责什么？', '第 6 题讲的是什么', 'H-1B and the AC21 §204(j) path',
    'claude-haiku-5-5 v0.3.1 a2a-bridge', '时', 'Mixed 中英 text, ATS/CRM/HCM 58 家', '',
  ];
  const py = execFileSync('python3', ['-c',
    "import sys,json; sys.path.insert(0,'ask'); import ask_corpus; print(json.dumps([ask_corpus.tokenize(s) for s in json.load(sys.stdin)], ensure_ascii=False))"],
  { cwd: ROOT, input: JSON.stringify(samples) }).toString();
  assert.deepEqual(samples.map(tokenize), JSON.parse(py));
});

test('bm25 finds the right page', () => {
  const index = JSON.parse(readFileSync(path.join(ROOT, 'public/ask/index.json'), 'utf8'));
  assert.equal(bm25(index, '第 6 题讲的是什么？', 1)[0].id, 't/time-reckoning');
  assert.ok(bm25(index, '一周一题的研究员要遵守哪些规则', 3).some(h => h.id === 'how#rules'));
  assert.ok(bm25(index, 'hireEZ ATS-Squad tech lead', 3).some(h => h.id.startsWith('about#') || h.id === 'card/scope-at-hireez'));
  assert.deepEqual(bm25(index, '???', 3), []);
});

test('answer check: every paragraph cited', () => {
  const v = validateAnswer('He leads the ATS-Squad. [S2]\n\nThe platform covers about 58 vendors. [S2][S5]', 10);
  assert.equal(v.verdict, 'ALL_CITED');
  assert.deepEqual(v.cited, [2, 5]);
});

test('answer check: uncited paragraph is flagged, invalid markers and links removed', () => {
  const v = validateAnswer('He leads the ATS-Squad [S2].\n\nHe probably also mentors many juniors everywhere.\n\nSee https://evil.example/x for the full story of the platform [S99].', 10);
  assert.equal(v.verdict, 'PARTIAL');
  assert.equal(v.checks.uncited, 2);
  assert.equal(v.checks.invalid_markers, 1);
  assert.equal(v.checks.stripped_urls, 1);
  assert.ok(!v.text.includes('http'));
  assert.deepEqual(v.checks.uncited_paragraphs, [1, 2]);
});

test('answer check: no citation at all is blocked', () => {
  assert.equal(validateAnswer('Tianjie is a great engineer who loves sushi.', 10).verdict, 'UNCITED');
});

test('answer check: NO_SOURCE line and combined markers', () => {
  const ns = validateAnswer('NO_SOURCE — the site does not mention food.', 10);
  assert.equal(ns.verdict, 'NO_SOURCE');
  assert.equal(ns.text, 'the site does not mention food.');
  const v = validateAnswer('两处都写了 [S1, S3]。另一句也有出处 [S4，S2]', 5);
  assert.equal(v.verdict, 'ALL_CITED');
  assert.deepEqual(v.cited, [1, 2, 3, 4]);
});

test('handoff routing', () => {
  assert.equal(detectHandoff('What is his expected salary?'), 'compensation');
  assert.equal(detectHandoff('他什么时候能入职？'), 'availability');
  assert.equal(detectHandoff('Does he need visa sponsorship?'), 'authorization');
  assert.equal(detectHandoff('他结婚了吗'), 'personal');
  assert.equal(detectHandoff('What does Tianjie do at hireEZ?'), null);
  assert.equal(detectHandoff('一周一题是怎么核查的'), null);
  assert.equal(detectHandoff('Which page explains the database design?'), null);
});

test('invite tokens made by tools/ask_invite.py verify in the worker', async () => {
  const make = (secret, days) => execFileSync('python3', ['-c',
    `import sys; sys.path.insert(0,'tools'); import ask_invite; print(ask_invite.make('${secret}', 'Acme · 招聘', ${days}, 25))`], { cwd: ROOT }).toString().trim();
  const tok = make('s3cret', 30);
  const ok = await verifyInvite(tok, 's3cret');
  assert.equal(ok.ok, true);
  assert.equal(ok.label, 'Acme · 招聘');
  assert.equal(ok.quota, 25);
  assert.equal((await verifyInvite(tok, 'other')).reason, 'bad signature');
  assert.equal((await verifyInvite(tok.slice(0, -2) + 'xx', 's3cret')).ok, false);
  assert.equal((await verifyInvite(make('s3cret', -1), 's3cret')).reason, 'expired');
  assert.equal((await verifyInvite(tok, '')).ok, false);
});

test('cost estimate and sources block', () => {
  assert.equal(estimateCost('claude-haiku-5-5', { input: 300, output: 500, cache_read: 7000, cache_write: 0 }), 0.00035);
  assert.equal(estimateCost('unknown-model', { input: 1 }), null);
  const block = buildSourcesBlock([{ title: 'A', date: '2026-10-31', text: 'x' }, { title: 'B', text: 'y' }]);
  assert.match(block, /\[S1\] A \(2026-10-31\)\nx/);
  assert.match(block, /\[S2\] B\ny/);
});
