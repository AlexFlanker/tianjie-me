/* 第 8 题的算法层（浏览器版，与 src/geo.py 同公式）。纯函数，挂在 self.GEO；同一份代码也被塞进 Web Worker 跑随机地图集合。 */
(function (root) {
  'use strict';
  function nbrs(i, n) { var r = (i / n) | 0, c = i % n, o = []; if (r > 0) o.push(i - n); if (r < n - 1) o.push(i + n); if (c > 0) o.push(i - 1); if (c < n - 1) o.push(i + 1); return o; }
  function contiguous(plan, k, n) {
    var cells = [], i; for (i = 0; i < n * n; i++) if (plan[i] === k) cells.push(i);
    if (!cells.length) return false;
    var seen = new Uint8Array(n * n), q = [cells[0]], cnt = 1; seen[cells[0]] = 1;
    while (q.length) { var u = q.pop(), nb = nbrs(u, n); for (var j = 0; j < nb.length; j++) { var v = nb[j]; if (plan[v] === k && !seen[v]) { seen[v] = 1; cnt++; q.push(v); } } }
    return cnt === cells.length;
  }
  function sizes(plan, K) { var s = []; for (var k = 0; k < K; k++) s.push(0); for (var i = 0; i < plan.length; i++) if (plan[i] >= 0) s[plan[i]]++; return s; }
  function valid(plan, n, K, size) { var s = sizes(plan, K); for (var k = 0; k < K; k++) { if (s[k] !== size) return false; if (!contiguous(plan, k, n)) return false; } return true; }
  function metrics(cells, plan, n, K) {
    var size = n * n, a = [], tot = [], k, i;
    for (k = 0; k < K; k++) { a.push(0); tot.push(0); }
    for (i = 0; i < size; i++) { if (plan[i] < 0) continue; tot[plan[i]]++; if (cells[i]) a[plan[i]]++; }
    var seatsA = 0, seatsB = 0, wA = 0, wB = 0, shares = [];
    for (k = 0; k < K; k++) {
      var b = tot[k] - a[k], half = tot[k] / 2;
      if (a[k] > b) { seatsA++; wA += a[k] - half; wB += b; }
      else if (b > a[k]) { seatsB++; wB += b - half; wA += a[k]; }
      else { wA += a[k] - half; wB += b - half; }
      shares.push(tot[k] ? a[k] / tot[k] : 0);
    }
    var V = 0; for (i = 0; i < size; i++) V += cells[i]; V /= size;
    var eg = (wB - wA) / size, egSimple = (seatsA / K - 0.5) - 2 * (V - 0.5);
    var sh = shares.slice().sort(function (x, y) { return x - y; });
    var med = K % 2 ? sh[(K - 1) / 2] : (sh[K / 2 - 1] + sh[K / 2]) / 2, mean = 0; for (k = 0; k < K; k++) mean += sh[k]; mean /= K;
    var cut = 0, per = [], area = [];
    for (k = 0; k < K; k++) { per.push(0); area.push(0); }
    for (i = 0; i < size; i++) {
      var r = (i / n) | 0, c = i % n, p = plan[i]; if (p >= 0) area[p]++;
      if (c < n - 1 && plan[i] !== plan[i + 1]) cut++;
      if (r < n - 1 && plan[i] !== plan[i + n]) cut++;
      if (p < 0) continue;
      if (r === 0 || plan[i - n] !== p) per[p]++; if (r === n - 1 || plan[i + n] !== p) per[p]++;
      if (c === 0 || plan[i - 1] !== p) per[p]++; if (c === n - 1 || plan[i + 1] !== p) per[p]++;
    }
    var pp = [], ppm = 0; for (k = 0; k < K; k++) { var v = per[k] ? 4 * Math.PI * area[k] / (per[k] * per[k]) : 0; pp.push(v); ppm += v; }
    return { seatsA: seatsA, seatsB: seatsB, ties: K - seatsA - seatsB, aVotes: a, tot: tot, wastedA: wA, wastedB: wB, eg: eg, egSimple: egSimple, meanMedian: med - mean, shares: shares, sharesSorted: sh, cutEdges: cut, pp: pp, ppMean: ppm / K, V: V };
  }
  // 均匀摆动：把每区甲得票率同加 delta，数过半的区 → 席位份额
  function svCurve(shares, K, steps) {
    var out = [], mean = 0, i; for (i = 0; i < K; i++) mean += shares[i]; mean /= K;
    steps = steps || 81;
    for (i = 0; i < steps; i++) { var V = 0.3 + 0.4 * i / (steps - 1), d = V - mean, s = 0; for (var k = 0; k < K; k++) if (shares[k] + d > 0.5) s++; out.push([V, s / K]); }
    return out;
  }
  function cube(V, k) { k = k == null ? 3 : k; V = Math.min(0.999, Math.max(0.001, V)); var r = Math.pow(V / (1 - V), k); return r / (1 + r); }
  // ---- 随机数（可复现）
  function RNG(seed) { var s = seed >>> 0 || 1; return function () { s = (s + 0x6D2B79F5) >>> 0; var t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  // ---- ReCom 一步：合并两个相邻区，重新一分为二（各恰 size 格，连通）
  function recomStep(plan, n, K, size, rnd, tries) {
    tries = tries || 30; var N = n * n;
    for (var t = 0; t < tries; t++) {
      var i = (rnd() * N) | 0, nb = nbrs(i, n).filter(function (j) { return plan[j] !== plan[i]; });
      if (!nb.length) continue;
      var j = nb[(rnd() * nb.length) | 0], k1 = plan[i], k2 = plan[j];
      var inset = new Uint8Array(N), nodes = [], x; for (x = 0; x < N; x++) if (plan[x] === k1 || plan[x] === k2) { inset[x] = 1; nodes.push(x); }
      // 随机边顺序的生成树
      var parent = new Int32Array(N).fill(-2), start = nodes[(rnd() * nodes.length) | 0]; parent[start] = -1;
      var edges = nbrs(start, n).filter(function (v) { return inset[v]; }).map(function (v) { return [start, v]; }), got = 1;
      while (edges.length) {
        var idx = (rnd() * edges.length) | 0, e = edges[idx]; edges[idx] = edges[edges.length - 1]; edges.pop();
        if (parent[e[1]] !== -2) continue; parent[e[1]] = e[0]; got++;
        var nn = nbrs(e[1], n); for (var q = 0; q < nn.length; q++) if (inset[nn[q]] && parent[nn[q]] === -2) edges.push([e[1], nn[q]]);
      }
      if (got !== nodes.length) continue;
      // 子树大小（按 BFS 顺序反向累加）
      var order = [start], children = {}, u; for (x = 0; x < nodes.length; x++) children[nodes[x]] = [];
      for (x = 0; x < nodes.length; x++) { u = nodes[x]; if (parent[u] >= 0) children[parent[u]].push(u); }
      for (x = 0; x < order.length; x++) { var ch = children[order[x]]; for (var y = 0; y < ch.length; y++) order.push(ch[y]); }
      var sub = {}; for (x = order.length - 1; x >= 0; x--) { u = order[x]; var s = 1, ch2 = children[u]; for (var z = 0; z < ch2.length; z++) s += sub[ch2[z]]; sub[u] = s; }
      var cands = nodes.filter(function (v) { return parent[v] >= 0 && sub[v] === size; });
      if (!cands.length) continue;
      var v0 = cands[(rnd() * cands.length) | 0], part = new Uint8Array(N), st = [v0];
      while (st.length) { u = st.pop(); part[u] = 1; var ch3 = children[u]; for (var w = 0; w < ch3.length; w++) st.push(ch3[w]); }
      var out = plan.slice(), A = rnd() < 0.5 ? k1 : k2, B = A === k1 ? k2 : k1;
      for (x = 0; x < nodes.length; x++) { var nd = nodes[x]; out[nd] = part[nd] ? A : B; }
      return out;
    }
    return null;
  }
  function strips(n, K) { var size = (n * n / K) | 0, p = []; for (var i = 0; i < n * n; i++) p.push(Math.min(K - 1, (i / size) | 0)); return p; }
  // ---- 分配
  function hamilton(pops, H, minimum) {
    minimum = minimum == null ? 1 : minimum; var tot = 0, i; for (i = 0; i < pops.length; i++) tot += pops[i];
    // 汉密尔顿（含宪法最少 1 席）：先给 max(1, floor(配额))，余席按「配额 − 已得」从大到小发（配额不足 1 的州不再竞争余席）
    var q = pops.map(function (p) { return p / tot * H; }), seats = q.map(function (x) { return Math.max(minimum, Math.floor(x)); }), used = 0;
    for (i = 0; i < seats.length; i++) used += seats[i];
    var rem = H - used, order = q.map(function (x, k) { return [x - seats[k], k]; }).sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; });
    for (i = 0; i < Math.max(0, rem); i++) seats[order[i][1]]++;
    return seats;
  }
  function dfun(method, s) {
    if (method === 'jefferson') return s + 1; if (method === 'adams') return s; if (method === 'webster') return s + 0.5;
    if (method === 'dean') return s * (s + 1) / (s + 0.5); if (method === 'huntington_hill') return Math.sqrt(s * (s + 1)); throw new Error(method);
  }
  function divisor(pops, H, method, minimum) {
    minimum = minimum == null ? 1 : minimum; var n = pops.length, seats = [], i; for (i = 0; i < n; i++) seats.push(minimum);
    for (var t = 0; t < H - minimum * n; t++) {
      var best = -1, bi = -1;
      for (i = 0; i < n; i++) { var d = dfun(method, seats[i]), pv = d === 0 ? Infinity : pops[i] / d; if (pv > best) { best = pv; bi = i; } }
      seats[bi]++;
    }
    return seats;
  }
  function apportion(pops, H, method, minimum) { return method === 'hamilton' ? hamilton(pops, H, minimum) : divisor(pops, H, method, minimum); }
  var GEO = { nbrs: nbrs, contiguous: contiguous, sizes: sizes, valid: valid, metrics: metrics, svCurve: svCurve, cube: cube, RNG: RNG, recomStep: recomStep, strips: strips, apportion: apportion, hamilton: hamilton, divisor: divisor };
  root.GEO = GEO;
  // Worker 入口：收到 {cells, plan, n, K, steps, seed, every} 就跑链，按批回报
  if (typeof importScripts === 'function' || (typeof WorkerGlobalScope !== 'undefined' && root instanceof WorkerGlobalScope)) {
    root.onmessage = function (ev) {
      var m = ev.data, cur = m.plan || strips(m.n, m.K), rnd = RNG(m.seed || 7), size = (m.n * m.n / m.K) | 0, batch = [], t0 = Date.now();
      for (var s = 0; s < m.steps; s++) {
        var nxt = recomStep(cur, m.n, m.K, size, rnd); if (nxt) cur = nxt;
        var mt = metrics(m.cells, cur, m.n, m.K);
        batch.push([mt.seatsA, Math.round(mt.eg * 1000) / 1000, mt.cutEdges]);
        if (batch.length >= (m.every || 100) || s === m.steps - 1) { root.postMessage({ batch: batch, done: s + 1, total: m.steps, plan: s === m.steps - 1 ? cur : null, ms: Date.now() - t0 }); batch = []; }
      }
    };
  }
})(typeof self !== 'undefined' ? self : this);
