// node tools/crosscheck.js：用 geo.js 复算 stage.json 的五张划法与 metrics_C 的分配数据，和 Python 结果比
const fs = require('fs'), path = require('path');
const vm = require('vm');
const ctx = { self: {} }; ctx.self = ctx; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'geo.js'), 'utf8'), ctx);
const GEO = ctx.GEO;
const S = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'stage.json'), 'utf8'));
let bad = 0;
for (const k of Object.keys(S.plans)) {
  const m = GEO.metrics(S.cells, S.plans[k], S.n, S.K), p = S.metrics[k];
  const same = m.seatsA === p.seatsA && Math.abs(m.eg - p.eg) < 1e-9 && Math.abs(m.meanMedian - p.meanMedian) < 1e-9 && m.cutEdges === p.cutEdges && Math.abs(m.ppMean - p.ppMean) < 1e-9 && m.wastedA === p.wastedA;
  if (!same) bad++;
  console.log(k, 'JS', m.seatsA, m.eg.toFixed(3), m.meanMedian.toFixed(3), m.cutEdges, m.ppMean.toFixed(3), '| PY', p.seatsA, p.eg.toFixed(3), p.meanMedian.toFixed(3), p.cutEdges, p.ppMean.toFixed(3), same ? 'OK' : 'DIFF', 'valid', GEO.valid(S.plans[k], S.n, S.K, 20));
}
const C = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'research', 'metrics_C.json'), 'utf8'));
const ds = Object.fromEntries(C.datasets.map(d => [d.id, d]));
const d20 = ds.us_2020_states.rows, pops = d20.map(r => r.pop), off = d20.map(r => r.seats);
const hh = GEO.apportion(pops, 435, 'huntington_hill');
let diff = d20.filter((r, i) => hh[i] !== r.seats).map((r, i) => r.state);
console.log('2020 HH vs official diff:', diff.length ? diff : 'none');
const d80 = ds.us_1880_states.rows, p80 = d80.map(r => r.pop);
const h299 = GEO.apportion(p80, 299, 'hamilton'), h300 = GEO.apportion(p80, 300, 'hamilton');
const ia = d80.findIndex(r => r.state === 'Alabama');
console.log('1880 Alabama Hamilton 299 ->', h299[ia], '300 ->', h300[ia]);
const h325 = GEO.apportion(p80, 325, 'hamilton'), w325 = GEO.apportion(p80, 325, 'webster');
console.log('1880 325 Hamilton vs act diff:', d80.filter((r, i) => h325[i] !== r.seats).map(r => r.state), 'Webster diff:', d80.filter((r, i) => w325[i] !== r.seats).map(r => r.state));
const d00 = ds.us_1900_states.rows, p00 = d00.map(r => r.pop), im = d00.findIndex(r => r.state === 'Maine');
let seq = []; for (let H = 350; H <= 400; H++) seq.push(GEO.apportion(p00, H, 'hamilton')[im]);
console.log('1900 Maine Hamilton 350..400:', seq.join(''));
// 随机链小跑：席位分布
const rnd = GEO.RNG(11); let cur = GEO.strips(10, 5), hist = {};
for (let s = 0; s < 1500; s++) { const nx = GEO.recomStep(cur, 10, 5, 20, rnd); if (nx) cur = nx; if (s >= 300) { const m = GEO.metrics(S.cells, cur, 10, 5); hist[m.seatsA] = (hist[m.seatsA] || 0) + 1; } }
console.log('JS ensemble 1200 samples seatsA hist', hist, '| PY', S.ensemble.hist);
process.exit(bad ? 1 : 0);
