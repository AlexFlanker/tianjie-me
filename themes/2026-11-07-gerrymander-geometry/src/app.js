(function () {
  'use strict';
  var root = document.documentElement, G = window.GEO;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  window.YZ = { D: D };

  /* ================= 共用：减少动效、弹簧、速度、投影 ================= */
  var RM = { on: false };
  try { var rmq = window.matchMedia('(prefers-reduced-motion: reduce)'); RM.on = rmq.matches; var rmc = function (e) { RM.on = e.matches; }; if (rmq.addEventListener) rmq.addEventListener('change', rmc); else if (rmq.addListener) rmq.addListener(rmc); } catch (e) {}
  function Spring(o) { this.x = o.from || 0; this.v = 0; this.target = this.x; this.z = o.damping == null ? 1 : o.damping; this.T = o.response || 0.4; this.eps = o.eps || 0.001; this.onUpdate = o.onUpdate || function () {}; this.onRest = o.onRest || null; this.raf = 0; this.running = false; this.last = 0; }
  Spring.prototype.to = function (target, o) {
    o = o || {}; if (o.velocity != null) this.v = o.velocity; if (o.damping != null) this.z = o.damping; if (o.response != null) this.T = o.response; this.target = target;
    if (RM.on) { this.stop(); this.x = target; this.v = 0; this.onUpdate(this.x, 0); if (this.onRest) this.onRest(); return this; }
    if (!this.running) { var self = this; this.running = true; this.last = performance.now(); this.raf = requestAnimationFrame(function step(now) { self.tick(now); if (self.running) self.raf = requestAnimationFrame(step); }); }
    return this;
  };
  Spring.prototype.tick = function (now) {
    var dt = Math.min(0.05, Math.max(0, (now - this.last) / 1000)); this.last = now;
    var w = 2 * Math.PI / this.T, k = w * w, c = 2 * this.z * w, n = Math.max(1, Math.ceil(dt * 240)), h = dt / n;
    for (var i = 0; i < n; i++) { var a = -k * (this.x - this.target) - c * this.v; this.v += a * h; this.x += this.v * h; }
    if (Math.abs(this.x - this.target) < this.eps && Math.abs(this.v) < this.eps * 8) { this.x = this.target; this.v = 0; this.running = false; this.onUpdate(this.x, 0); if (this.onRest) this.onRest(); return; }
    this.onUpdate(this.x, this.v);
  };
  Spring.prototype.set = function (x) { this.stop(); this.x = x; this.target = x; this.v = 0; this.onUpdate(x, 0); };
  Spring.prototype.stop = function () { if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0; this.running = false; };
  function VTrack() { this.s = []; }
  VTrack.prototype.add = function (x) { var t = performance.now(); this.s.push([t, x]); while (this.s.length > 2 && t - this.s[0][0] > 100) this.s.shift(); };
  VTrack.prototype.v = function () { var s = this.s; if (s.length < 2) return 0; var a = s[0], b = s[s.length - 1], dt = (b[0] - a[0]) / 1000; if (dt <= 0 || performance.now() - b[0] > 80) return 0; return (b[1] - a[1]) / dt; };
  VTrack.prototype.reset = function () { this.s = []; };
  function project(v, d) { d = d || 0.998; return (v / 1000) * d / (1 - d); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fmtSigned(x, digits) { var s = x.toFixed(digits == null ? 2 : digits); return (x > 0 ? '+' : '') + s; }
  var SVGNS = 'http://www.w3.org/2000/svg';
  function svgEl(tag, attrs, parent) { var el = document.createElementNS(SVGNS, tag); if (attrs) for (var k in attrs) el.setAttribute(k, attrs[k]); if (parent) parent.appendChild(el); return el; }
  var SEATS_K = D.stage.K, GN = D.stage.n, CELLS = D.stage.cells;

  /* ================= 深浅色 ================= */
  try { var saved = localStorage.getItem('yzyt-theme-8'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  function curTheme() { return root.getAttribute('data-theme') || 'light'; }
  function themeLabel() { if (!tb) return; var d = curTheme() === 'dark'; tb.textContent = d ? '白天读' : '夜里读'; tb.setAttribute('aria-label', d ? '换成浅色' : '换成深色'); }
  if (tb) { themeLabel(); tb.addEventListener('click', function () { var next = curTheme() === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next); themeLabel(); try { localStorage.setItem('yzyt-theme-8', next); } catch (e) {} }); }

  /* ================= 入场 ================= */
  var fades = $$('.fade').concat($$('.rise').filter(function (el) { return !el.closest('#top'); }));
  if ('IntersectionObserver' in window && !RM.on) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else { fades.forEach(function (el) { el.classList.add('in'); }); }
  (function initHero() {
    var h = $('#top'); if (!h) return; var rs = $$('.rise', h);
    if (RM.on) { rs.forEach(function (el) { el.classList.add('in'); }); return; }
    requestAnimationFrame(function () { rs.forEach(function (el, i) { el.style.transitionDelay = (0.1 + Math.min(i * 0.08, 0.4)).toFixed(2) + 's'; el.classList.add('in'); }); });
  })();
  (function initTagline() {
    var sec = $('#tagsec'); if (!sec) return;
    var ws = $$('.tagl .w', sec), rest = $('.tagrest', sec), tick = false;
    function upd() {
      tick = false;
      if (RM.on) { ws.forEach(function (w) { w.classList.add('on'); }); if (rest) rest.classList.add('on'); return; }
      var r = sec.getBoundingClientRect(), span = sec.offsetHeight - window.innerHeight;
      var p = clamp(-r.top / (span > 0 ? span : 1), 0, 1), n = Math.floor(p * (ws.length + 3));
      ws.forEach(function (w, i) { var on = i < n; if (on !== w.classList.contains('on')) w.classList.toggle('on', on); });
      if (rest) rest.classList.toggle('on', n >= ws.length + 1);
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener('resize', upd); upd();
  })();

  /* ================= 章节导航与进度 ================= */
  var nav = $('#cnav'), prog = $('#prog'), links = $$('[data-nav]'), secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-nav')); });
  function navH() { return nav ? nav.offsetHeight : 0; }
  function setNavH() { root.style.setProperty('--nav-h', navH() + 'px'); }
  var navTick = false;
  function onScrollNav() {
    if (navTick) return; navTick = true;
    requestAnimationFrame(function () {
      navTick = false;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (prog) prog.style.transform = 'scaleX(' + (h > 0 ? clamp(window.scrollY / h, 0, 1) : 0).toFixed(4) + ')';
      var y = window.scrollY + navH() + 40, cur = 0;
      for (var i = 0; i < secs.length; i++) if (secs[i] && secs[i].getBoundingClientRect().top + window.scrollY <= y) cur = i;
      links.forEach(function (a, i) { var on = i === cur; if (on !== a.classList.contains('on')) { a.classList.toggle('on', on); if (on && nav) { var r = a.getBoundingClientRect(), rr = nav.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) a.parentNode.scrollLeft += r.left - rr.left - 20; } } });
    });
  }
  setNavH(); onScrollNav();
  window.addEventListener('scroll', onScrollNav, { passive: true });
  window.addEventListener('resize', function () { setNavH(); onScrollNav(); });

  /* ================= 透镜列表（三处共用）：分组重排（FLIP）+ 行内展开 ================= */
  var LISTS = {};
  function initList(key) {
    var grid = $('#lgrid-' + key), lensEl = $('#lens-' + key); if (!grid || !lensEl) return null;
    var rows = {}; $$('.lrow', grid).forEach(function (r) { rows[r.getAttribute('data-id')] = r; });
    var tabs = $$('button[data-lens]', lensEl), cur = (tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0]).getAttribute('data-lens'), note = $('#lensnote-' + key);
    var pill = document.createElement('span'); pill.className = 'pill'; lensEl.insertBefore(pill, lensEl.firstChild);
    var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
    var pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
    function movePill(instant) { var b = tabs.filter(function (t) { return t.getAttribute('data-lens') === cur; })[0]; if (!b) return; var x = b.offsetLeft, w = b.offsetWidth; if (instant) { px.set(x); pw.set(w); } else { px.to(x); pw.to(w); } }
    function header(g) { var h = document.createElement('div'); h.className = 'lgh'; h.setAttribute('data-g', g.k); h.innerHTML = '<b>' + g.label + '</b><small>' + g.ids.length + ' 条</small>'; return h; }
    function setNote() { if (note) note.textContent = '按' + D.lensName[key][cur] + '分成 ' + D.lens[key][cur].length + ' 组 · 点一行展开'; }
    function setLens(lens, instant) {
      if (!D.lens[key][lens]) return; cur = lens;
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-lens') === lens)); });
      movePill(instant);
      var first = {}; Object.keys(rows).forEach(function (id) { first[id] = rows[id].getBoundingClientRect().top; });
      var frag = document.createDocumentFragment();
      D.lens[key][lens].forEach(function (g) { frag.appendChild(header(g)); g.ids.forEach(function (id) { if (rows[id]) frag.appendChild(rows[id]); }); });
      $$('.lgh', grid).forEach(function (h) { h.remove(); });
      grid.appendChild(frag); setNote();
      if (instant || RM.on) return;
      Object.keys(rows).forEach(function (id) { var r = rows[id], dy = first[id] - r.getBoundingClientRect().top; if (Math.abs(dy) < 1) return; r.style.transition = 'none'; r.style.transform = 'translateY(' + dy.toFixed(1) + 'px)'; });
      grid.offsetHeight;
      Object.keys(rows).forEach(function (id) { var r = rows[id]; if (!r.style.transform) return; r.style.transition = 'transform .5s cubic-bezier(.22,1,.36,1)'; r.style.transform = ''; });
      $$('.lgh', grid).forEach(function (h) { h.animate && h.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'cubic-bezier(.22,1,.36,1)' }); });
    }
    lensEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-lens]'); if (b) setLens(b.getAttribute('data-lens')); });
    lensEl.addEventListener('keydown', function (e) { if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return; var i = tabs.findIndex(function (t) { return t.getAttribute('data-lens') === cur; }), n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); setLens(n.getAttribute('data-lens')); e.preventDefault(); });
    function toggle(r, open) { var o = open == null ? !r.classList.contains('open') : open; r.classList.toggle('open', o); var b = $('.lhead', r); if (b) b.setAttribute('aria-expanded', String(o)); if (api.onToggle) api.onToggle(r.getAttribute('data-id'), o); }
    grid.addEventListener('click', function (e) { var b = e.target.closest('.lhead'); if (!b) return; toggle(b.closest('.lrow')); });
    function scrollToRow(r) { var lb = $('.lensbar', grid.parentNode), off = navH() + (lb ? lb.offsetHeight : 0) + 8, top = r.getBoundingClientRect().top + window.scrollY - off; window.scrollTo({ top: Math.max(0, top), behavior: RM.on ? 'auto' : 'smooth' }); }
    var api = {
      open: function (id, lens) { var r = rows[id]; if (!r) return; if (lens && lens !== cur) setLens(lens, true); toggle(r, true); scrollToRow(r); r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1400); try { history.replaceState(null, '', '#n-' + id); } catch (er) {} },
      rows: rows, onToggle: null
    };
    movePill(true); setNote();
    window.addEventListener('resize', function () { movePill(true); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); });
    return api;
  }
  ['history', 'rulers', 'world'].forEach(function (k) { LISTS[k] = initList(k); });
  var m0 = /^#n-([\w-]+)$/.exec(location.hash || '');
  if (m0) Object.keys(LISTS).forEach(function (k) { if (LISTS[k] && LISTS[k].rows[m0[1]]) setTimeout(function () { LISTS[k].open(m0[1]); }, 60); });

  /* ================= 格子渲染器（序章与画线器共用） ================= */
  function Grid(svg, n, cells, opts) {
    opts = opts || {}; var self = this; this.svg = svg; this.n = n; this.cells = cells; this.S = 400 / n; this.plan = null;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var gc = svgEl('g', { 'class': 'cells' }, svg), i;
    this.cellEls = [];
    for (i = 0; i < n * n; i++) { var r = (i / n) | 0, c = i % n; this.cellEls.push(svgEl('rect', { 'class': 'cell ' + (cells[i] ? 'a' : 'b'), x: c * this.S, y: r * this.S, width: this.S, height: this.S, 'data-i': i }, gc)); }
    // 内部边：竖边 (r, c|c+1) 与横边 (r|r+1, c)
    var gb = svgEl('g', { 'class': 'bords' }, svg); this.vEdges = []; this.hEdges = [];
    for (i = 0; i < n * n; i++) { var rr = (i / n) | 0, cc = i % n;
      if (cc < n - 1) this.vEdges.push(svgEl('line', { 'class': 'bord', x1: (cc + 1) * this.S, y1: rr * this.S, x2: (cc + 1) * this.S, y2: (rr + 1) * this.S }, gb)); else this.vEdges.push(null);
      if (rr < n - 1) this.hEdges.push(svgEl('line', { 'class': 'bord', x1: cc * this.S, y1: (rr + 1) * this.S, x2: (cc + 1) * this.S, y2: (rr + 1) * this.S }, gb)); else this.hEdges.push(null);
    }
    svgEl('rect', { 'class': 'frame', x: 0, y: 0, width: 400, height: 400 }, svg);
    this.gl = svgEl('g', { 'class': 'labels' }, svg); this.labels = [];
    if (opts.cellLabels) { this.gcl = svgEl('g', { 'class': 'celllabels' }, svg); this.cellLabels = []; for (i = 0; i < n * n; i++) { var r2 = (i / n) | 0, c2 = i % n; var t = svgEl('text', { x: c2 * this.S + this.S / 2, y: r2 * this.S + this.S / 2 + 4, 'text-anchor': 'middle', style: 'font:600 11px var(--sans);fill:var(--ink);paint-order:stroke;stroke:var(--pat-bg);stroke-width:3px;pointer-events:none' }, this.gcl); this.cellLabels.push(t); } }
  }
  Grid.prototype.setPlan = function (plan, K, winners) {
    var n = this.n, i; this.plan = plan;
    for (i = 0; i < n * n; i++) {
      var r = (i / n) | 0, c = i % n;
      if (this.vEdges[i]) this.vEdges[i].classList.toggle('on', plan[i] !== plan[i + 1] && (plan[i] >= 0 || plan[i + 1] >= 0));
      if (this.hEdges[i]) this.hEdges[i].classList.toggle('on', plan[i] !== plan[i + n] && (plan[i] >= 0 || plan[i + n] >= 0));
      if (this.cellLabels) this.cellLabels[i].textContent = plan[i] >= 0 ? String(plan[i] + 1) : '';
    }
    // 区号放在各区质心
    var cx = [], cy = [], cnt = [], k;
    for (k = 0; k < K; k++) { cx.push(0); cy.push(0); cnt.push(0); }
    for (i = 0; i < n * n; i++) { if (plan[i] < 0) continue; cx[plan[i]] += (i % n) + 0.5; cy[plan[i]] += ((i / n) | 0) + 0.5; cnt[plan[i]]++; }
    while (this.labels.length < K) { var g = svgEl('g', { style: 'transition:transform .5s var(--ease)' }, this.gl); var t = svgEl('text', { 'class': 'dlab', y: 5 }, g); this.labels.push({ g: g, t: t }); }
    for (k = 0; k < K; k++) {
      var L = this.labels[k];
      if (!cnt[k]) { L.g.style.opacity = 0; continue; }
      // 质心可能落在区外（L 形）：挑离质心最近的本区格子
      var gx = cx[k] / cnt[k], gy = cy[k] / cnt[k], best = null, bd = 1e9;
      for (i = 0; i < n * n; i++) { if (plan[i] !== k) continue; var dx = (i % n) + 0.5 - gx, dy = ((i / n) | 0) + 0.5 - gy, d = dx * dx + dy * dy; if (d < bd) { bd = d; best = i; } }
      var px = ((best % n) + 0.5) * this.S, py = (((best / n) | 0) + 0.5) * this.S;
      L.g.style.opacity = 1; L.g.setAttribute('transform', 'translate(' + px.toFixed(1) + ',' + py.toFixed(1) + ')');
      if (this.cellLabels) { this.cellLabels[best].textContent = ''; L.t.textContent = winners ? (winners[k] === 'a' ? '甲' : winners[k] === 'b' ? '乙' : '平') : String(k + 1); }
      else L.t.textContent = (k + 1) + (winners ? (winners[k] === 'a' ? ' 甲' : winners[k] === 'b' ? ' 乙' : ' 平') : '');
      L.t.setAttribute('class', 'dlab' + (winners && winners[k] === 'b' ? ' red' : ''));
    }
  };
  function winnersOf(m) { var w = []; for (var k = 0; k < m.aVotes.length; k++) { var a = m.aVotes[k], b = m.tot[k] - a; w.push(a > b ? 'a' : b > a ? 'b' : 't'); } return w; }
  function seatRow(el, m, lbl) {
    var w = winnersOf(m).slice().sort(function (x, y) { return x === y ? 0 : x === 'a' ? -1 : y === 'a' ? 1 : x === 't' ? -1 : 1; });
    $$('i', el).forEach(function (i, k) { i.className = w[k] || ''; });
    if (lbl) lbl.textContent = '甲 ' + m.seatsA + ' 席 · 乙 ' + m.seatsB + ' 席' + (m.ties ? ' · 平 ' + m.ties : '');
  }

  /* ================= 序章：舞台 ================= */
  (function initStage() {
    var pin = $('#stpin'), st = $('#ststage'), svg = $('#stsvg'), ruler = $('#struler'), knob = $('#stknob'); if (!pin || !svg) return;
    var steps = D.stage.steps, N = steps.length, grid = new Grid(svg, GN, CELLS), cur = -1, t = 0;
    var M = {}; steps.forEach(function (s) { M[s.plan] = G.metrics(CELLS, D.stage.plans[s.plan], GN, SEATS_K); });
    var ticks = $$('.rtick', ruler);
    function show(i) {
      if (i === cur) return; cur = i; var s = steps[i], m = M[s.plan];
      grid.setPlan(D.stage.plans[s.plan], SEATS_K, winnersOf(m));
      $('#stk').textContent = '第 ' + (i + 1) + ' 张 · 共 ' + N + ' 张'; $('#stname').textContent = s.name; $('#stshort').textContent = s.short;
      $('#sthow').textContent = s.how; $('#stread').textContent = s.read;
      seatRow($('#stseats'), m, $('#stseatsl'));
      $('#stwa').style.width = (m.wastedA / 60 * 100).toFixed(0) + '%'; $('#stwan').textContent = m.wastedA + ' / 60'; $('#stwb').style.width = (m.wastedB / 40 * 100).toFixed(0) + '%'; $('#stwbn').textContent = m.wastedB + ' / 40';
      var eg = $('#steg'); eg.textContent = fmtSigned(m.eg, 2); eg.className = Math.abs(m.eg) >= 0.08 ? 'red' : '';
      $('#stmm').textContent = fmtSigned(m.meanMedian, 2); $('#stcut').textContent = m.cutEdges;
      ticks.forEach(function (tk, k) { tk.classList.toggle('on', k === i); });
      ruler.setAttribute('aria-valuenow', String(i)); ruler.setAttribute('aria-valuetext', s.name + ' ' + s.short);
    }
    function setT(v) { t = clamp(v, 0, N - 1); knob.style.left = 'calc(var(--gut) + (100% - 2 * var(--gut)) * ' + (t / (N - 1)).toFixed(4) + ')'; show(Math.round(t)); }
    function span() { return pin.offsetHeight - st.offsetHeight; }
    var tick = false;
    function onScroll() { if (tick) return; tick = true; requestAnimationFrame(function () { tick = false; var r = pin.getBoundingClientRect(), p = clamp((-r.top + navH()) / Math.max(1, span()), 0, 1); setT(p * (N - 1)); }); }
    window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); onScroll();
    // 刻度尺：拖动 = 滚动页面到对应位置（滚动与刻度是同一个量）
    function scrollToT(v, smooth) { var top = pin.getBoundingClientRect().top + window.scrollY - navH() + clamp(v, 0, N - 1) / (N - 1) * span(); window.scrollTo({ top: top + 2, behavior: smooth && !RM.on ? 'smooth' : 'auto' }); }
    var drag = null, track = $('.rtrack', ruler);
    function tFromX(x) { var r = track.getBoundingClientRect(); return clamp((x - r.left) / Math.max(1, r.width), 0, 1) * (N - 1); }
    ruler.addEventListener('pointerdown', function (e) { if (e.button) return; drag = { id: e.pointerId }; ruler.setPointerCapture(e.pointerId); scrollToT(tFromX(e.clientX), false); e.preventDefault(); });
    ruler.addEventListener('pointermove', function (e) { if (!drag || e.pointerId !== drag.id) return; scrollToT(tFromX(e.clientX), false); });
    function up(e) { if (!drag || e.pointerId !== drag.id) return; drag = null; scrollToT(Math.round(t), true); }
    ruler.addEventListener('pointerup', up); ruler.addEventListener('pointercancel', up);
    ruler.addEventListener('keydown', function (e) { var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : e.key === 'Home' ? -N : e.key === 'End' ? N : 0; if (!d) return; scrollToT(clamp(Math.round(t) + d, 0, N - 1), true); e.preventDefault(); });
    ticks.forEach(function (tk) { tk.style.pointerEvents = 'auto'; tk.style.cursor = 'pointer'; tk.addEventListener('click', function () { scrollToT(+tk.getAttribute('data-i'), true); }); });
    show(0);
    window.YZ.stageMetrics = M;
  })();

  /* ================= 第一章：时间轴主图 ================= */
  (function initTimeline() {
    var box = $('#tlbox'), svg = $('#tlsvg'); if (!box || !svg) return;
    var nodes = D.nodes, W = 1200, H = 300, L = 40, R = 24, Y = { draw: 78, count: 160, measure: 242 };
    var Y0 = -520, Y1 = 1790, Y2 = 2032, X0 = L, XB = L + 120, X1 = W - R;
    function xOf(y) { return y <= Y1 ? X0 + (y - Y0) / (Y1 - Y0) * (XB - X0) : XB + 16 + (y - Y1) / (Y2 - Y1) * (X1 - XB - 16); }
    function yOf(x) { return x <= XB ? Y0 + (x - X0) / (XB - X0) * (Y1 - Y0) : Y1 + (x - XB - 16) / (X1 - XB - 16) * (Y2 - Y1); }
    // 泳道
    Object.keys(Y).forEach(function (l) { svgEl('line', { 'class': 'lanel', x1: X0, y1: Y[l], x2: X1, y2: Y[l] }, svg); svgEl('text', { 'class': 'lane', x: X0, y: Y[l] - 46 }, svg).textContent = D.laneName[l]; });
    // 轴与刻度
    svgEl('line', { 'class': 'axis', x1: X0, y1: 282, x2: X1, y2: 282 }, svg);
    [-500, 0, 1000, 1500].forEach(function (y) { var x = xOf(y); svgEl('line', { 'class': 'tick', x1: x, y1: 278, x2: x, y2: 286 }, svg); svgEl('text', { 'class': 'tlab', x: x, y: 298, 'text-anchor': 'middle' }, svg).textContent = y < 0 ? '前 ' + (-y) : String(y); });
    svgEl('path', { 'class': 'brk', d: 'M' + (XB + 4) + ' 276 l4 6 l-4 6 M' + (XB + 12) + ' 276 l4 6 l-4 6', fill: 'none' }, svg);
    for (var yy = 1800; yy <= 2020; yy += 20) { var x = xOf(yy); svgEl('line', { 'class': 'tick', x1: x, y1: 278, x2: x, y2: 286 }, svg); if (yy % 40 === 0) svgEl('text', { 'class': 'tlab', x: x, y: 298, 'text-anchor': 'middle' }, svg).textContent = String(yy); }
    // 节点：同泳道相近的交错上下
    var els = {}, lastLab = { draw: [], count: [], measure: [] };
    nodes.forEach(function (n) {
      var x = xOf(n.year), y = Y[n.lane], g = svgEl('g', { 'class': 'node', 'data-id': n.id, transform: 'translate(' + x.toFixed(1) + ',' + y + ')' }, svg);
      svgEl('circle', { r: 7 }, g); svgEl('circle', { r: 16, fill: 'transparent' }, g);
      // 标签：同泳道相邻太近（< 90px）时依次换档位（上 / 下 / 更上 / 更下），并左右错开
      var slots = [-14, 24, -32, 42], used = lastLab[n.lane], pick = 0;
      if (used.length && x - used[used.length - 1].x < 90) pick = (used[used.length - 1].pick + 1) % slots.length;
      var dy = slots[pick]; used.push({ x: x, pick: pick }); if (used.length > 4) used.shift();
      var anchor = x < X0 + 60 ? 'start' : x > X1 - 60 ? 'end' : 'middle', tx = anchor === 'start' ? -8 : anchor === 'end' ? 8 : 0;
      if (anchor === 'middle' && pick >= 2) { anchor = pick === 2 ? 'end' : 'start'; tx = pick === 2 ? 6 : -6; }
      var t = svgEl('text', { x: tx, y: dy, 'text-anchor': anchor }, g); t.textContent = n.short;
      els[n.id] = g; n.x = x;
    });
    var curL = svgEl('line', { 'class': 'cur', x1: 0, y1: 40, x2: 0, y2: 286 }, svg), curT = svgEl('text', { 'class': 'curlab', x: 0, y: 30, 'text-anchor': 'middle' }, svg);
    var ry = $('#tly'), rt = $('#tlt'), rw = $('#tlw'), rr = $('#tlr'), go = $('#tlgo'), curId = null;
    function nearest(x) { var best = null, bd = 1e9; nodes.forEach(function (n) { var d = Math.abs(n.x - x); if (d < bd) { bd = d; best = n; } }); return best; }
    function setX(x) {
      x = clamp(x, X0, X1); curL.setAttribute('x1', x); curL.setAttribute('x2', x); curT.setAttribute('x', x);
      var y = Math.round(yOf(x)); curT.textContent = y < 0 ? '前 ' + (-y) : String(y);
      var n = nearest(x); if (n && n.id !== curId) { curId = n.id; nodes.forEach(function (m) { els[m.id].classList.toggle('on', m.id === n.id); }); ry.innerHTML = n.label + '<small>' + D.laneName[n.lane] + '</small>'; rt.textContent = n.title; rw.textContent = n.what; rr.textContent = n.ruler; }
      box.setAttribute('aria-valuenow', String(y));
    }
    var sp = new Spring({ damping: 1, response: 0.35, eps: 0.3, onUpdate: setX });
    function jumpTo(n, smooth) { if (smooth) sp.to(n.x); else sp.set(n.x); }
    var drag = null, vt = new VTrack();
    function xFromClient(cx) { var r = svg.getBoundingClientRect(); return (cx - r.left) / r.width * W; }
    box.addEventListener('pointerdown', function (e) { if (e.button) return; var narrow = window.innerWidth <= 700; var g = e.target.closest('.node'); if (g) { var n = nodes.filter(function (m) { return m.id === g.getAttribute('data-id'); })[0]; jumpTo(n, true); if (narrow) { if (LISTS.history) LISTS.history.open(n.id); return; } drag = { id: e.pointerId, click: n }; box.setPointerCapture(e.pointerId); return; } if (narrow) return; drag = { id: e.pointerId }; box.setPointerCapture(e.pointerId); sp.set(xFromClient(e.clientX)); vt.reset(); vt.add(sp.x); e.preventDefault(); });
    box.addEventListener('pointermove', function (e) { if (!drag || e.pointerId !== drag.id) return; if (drag.click) { if (Math.abs(e.movementX) > 2) drag.click = null; else return; } sp.set(xFromClient(e.clientX)); vt.add(sp.x); });
    function up(e) { if (!drag || e.pointerId !== drag.id) return; var c = drag.click; drag = null; if (c) { if (LISTS.history) LISTS.history.open(c.id); return; } var v = vt.v(), target = sp.x + project(v, 0.995); var n = nearest(target); sp.to(n.x, { velocity: v }); }
    box.addEventListener('pointerup', up); box.addEventListener('pointercancel', up);
    box.addEventListener('keydown', function (e) { var i = nodes.findIndex(function (n) { return n.id === curId; }), d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : e.key === 'Home' ? -99 : e.key === 'End' ? 99 : 0; if (!d) return; jumpTo(nodes[clamp(i + d, 0, nodes.length - 1)], true); e.preventDefault(); });
    if (go) go.addEventListener('click', function () { if (curId && LISTS.history) LISTS.history.open(curId); });
    var start = nodes.filter(function (n) { return n.id === 'gerry-mander-1812'; })[0] || nodes[0]; jumpTo(start, false);
    if (LISTS.history) LISTS.history.onToggle = function (id, open) { if (open) { var n = nodes.filter(function (m) { return m.id === id; })[0]; if (n) jumpTo(n, true); } };
  })();

  /* ================= 第二章：席位—选票曲线 ================= */
  var MINE = { plan: null, metrics: null };
  (function initSV() {
    var svg = $('#svsvg'), btns = $('#svplans'); if (!svg || !btns) return;
    var W = 1200, H = 520, L = 70, R = 40, T = 30, Bm = 60, PW = W - L - R, PH = H - T - Bm;
    function xOf(v) { return L + (v - 0.3) / 0.4 * PW; } function yOf(s) { return T + (1 - s) * PH; }
    var i;
    for (i = 0; i <= 8; i++) { var v = 0.3 + i * 0.05; svgEl('line', { 'class': 'gr', x1: xOf(v), y1: T, x2: xOf(v), y2: T + PH }, svg); svgEl('text', { 'class': 'lab', x: xOf(v), y: H - 36, 'text-anchor': 'middle' }, svg).textContent = Math.round(v * 100) + '%'; }
    for (i = 0; i <= 5; i++) { var s = i / 5; svgEl('line', { 'class': 'gr', x1: L, y1: yOf(s), x2: L + PW, y2: yOf(s) }, svg); svgEl('text', { 'class': 'lab', x: L - 10, y: yOf(s) + 4, 'text-anchor': 'end' }, svg).textContent = Math.round(s * 100) + '%'; }
    svgEl('text', { 'class': 'lab', x: L + PW / 2, y: H - 14, 'text-anchor': 'middle' }, svg).textContent = '甲的全局得票率 V';
    svgEl('text', { 'class': 'lab', x: 16, y: T + PH / 2, 'text-anchor': 'middle', transform: 'rotate(-90 16 ' + (T + PH / 2) + ')' }, svg).textContent = '甲的席位份额 S';
    svgEl('line', { 'class': 'ax', x1: L, y1: T + PH, x2: L + PW, y2: T + PH }, svg); svgEl('line', { 'class': 'ax', x1: L, y1: T, x2: L, y2: T + PH }, svg);
    svgEl('line', { 'class': 'diag', x1: xOf(0.3), y1: yOf(0.3), x2: xOf(0.7), y2: yOf(0.7) }, svg);
    var cd = ''; for (i = 0; i <= 80; i++) { var vv = 0.3 + 0.4 * i / 80; cd += (i ? 'L' : 'M') + xOf(vv).toFixed(1) + ' ' + yOf(G.cube(vv, 3)).toFixed(1) + ' '; } svgEl('path', { 'class': 'cube', d: cd }, svg);
    var leg = svgEl('g', {}, svg); svgEl('line', { 'class': 'cube', x1: L + 16, y1: T + 16, x2: L + 56, y2: T + 16 }, leg); svgEl('text', { 'class': 'leg', x: L + 64, y: T + 20 }, leg).textContent = '立方律 S/(1−S) = (V/(1−V))³';
    svgEl('line', { 'class': 'diag', x1: L + 16, y1: T + 40, x2: L + 56, y2: T + 40 }, leg); svgEl('text', { 'class': 'leg', x: L + 64, y: T + 44 }, leg).textContent = '纯比例';
    svgEl('line', { 'class': 'plan', x1: L + 16, y1: T + 64, x2: L + 56, y2: T + 64 }, leg); var legT = svgEl('text', { 'class': 'leg', x: L + 64, y: T + 68 }, leg);
    var path = svgEl('path', { 'class': 'plan', d: '' }, svg), mark = svgEl('circle', { 'class': 'mark', r: 6 }, svg), mark2 = svgEl('circle', { 'class': 'mark', r: 4, style: 'fill:var(--ink)' }, svg);
    var cur = 'fair';
    function S(curve, V) { var best = curve[0]; for (var k = 0; k < curve.length; k++) if (Math.abs(curve[k][0] - V) < Math.abs(best[0] - V)) best = curve[k]; return best[1]; }
    function draw() {
      var m = cur === 'mine' ? MINE.metrics : window.YZ.stageMetrics[cur]; if (!m) return;
      var curve = G.svCurve(m.shares, SEATS_K, 161), d = '';
      curve.forEach(function (p, k) { d += (k ? 'L' : 'M') + xOf(p[0]).toFixed(1) + ' ' + yOf(p[1]).toFixed(1) + ' '; });
      path.setAttribute('d', d);
      var s50 = S(curve, 0.5), s60 = S(curve, 0.6); mark.setAttribute('cx', xOf(0.5)); mark.setAttribute('cy', yOf(s50)); mark2.setAttribute('cx', xOf(0.6)); mark2.setAttribute('cy', yOf(s60));
      var bias = s50 - 0.5, sB60 = 1 - S(curve, 0.4);
      var b = $('#svbias'); b.textContent = fmtSigned(bias, 2) + (bias > 0 ? '（对甲有利）' : bias < 0 ? '（对乙有利）' : '（对称）'); b.className = Math.abs(bias) >= 0.1 ? 'red' : '';
      $('#svnow').textContent = Math.round(s60 * SEATS_K) + ' 席（' + Math.round(s60 * 100) + '%）';
      var r2 = $('#svresp'); r2.textContent = Math.round(sB60 * SEATS_K) + ' 席（' + Math.round(sB60 * 100) + '%）'; r2.className = Math.round(sB60 * SEATS_K) !== Math.round(s60 * SEATS_K) ? 'red' : '';
      var name = cur === 'mine' ? '你画的那张' : D.stage.steps.filter(function (s) { return s.plan === cur; })[0].name; legT.textContent = '这张划法：' + name;
    }
    btns.addEventListener('click', function (e) { var b = e.target.closest('button[data-plan]'); if (!b || b.disabled) return; cur = b.getAttribute('data-plan'); $$('button', btns).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(); });
    window.YZ.svDraw = function () { if (cur === 'mine') draw(); };
    draw();
  })();

  /* ================= 第三章：世界地图 ↔ 行 ================= */
  (function initWorld() {
    var svg = $('#wmsvg'); if (!svg || !LISTS.world) return;
    var pols = $$('.pol', svg);
    svg.addEventListener('click', function (e) { var g = e.target.closest('.pol'); if (!g) return; LISTS.world.open(g.getAttribute('data-id')); });
    LISTS.world.onToggle = function (id, open) { pols.forEach(function (g) { if (g.getAttribute('data-id') === id) g.classList.toggle('on', open); }); };
  })();

  /* ================= 第四章：分配计算器 ================= */
  (function initAp() {
    var tbl = $('#aptbl'), sel = $('#apds'), range = $('#aprange'), hl = $('#aph'), read = $('#apread'), mbox = $('#apmethods'); if (!tbl || !sel) return;
    var RANGES = { '1880': [275, 350, 325], '1900': [350, 400, 386], '2020': [400, 470, 435] }, ds = '1880', H = 325, hlState = null, timer = 0;
    var methods = Object.keys(D.methodName);
    function chosen() { return $$('input[data-m]', mbox).filter(function (c) { return c.checked; }).map(function (c) { return c.getAttribute('data-m'); }); }
    function render() {
      var rows = D.ap[ds].rows, pops = rows.map(function (r) { return r.pop; }), ms = chosen(), tot = pops.reduce(function (a, b) { return a + b; }, 0), official = D.ap[ds].H;
      var res = {}, prev = {}; ms.forEach(function (m) { res[m] = G.apportion(pops, H, m); prev[m] = G.apportion(pops, H - 1, m); });
      var order = rows.map(function (r, i) { return i; }).sort(function (a, b) { return pops[b] - pops[a]; });
      var h = '<table><thead><tr><th>州</th><th>人口</th><th>配额</th>' + ms.map(function (m) { return '<th>' + D.methodName[m] + '</th>'; }).join('') + (H === official ? '<th>法案</th>' : '') + '</tr></thead><tbody>';
      var downs = [], diffs = 0;
      order.forEach(function (i) {
        var r = rows[i], q = pops[i] / tot * H, vals = ms.map(function (m) { return res[m][i]; }), allSame = vals.every(function (v) { return v === vals[0]; });
        if (!allSame) diffs++;
        h += '<tr' + (hlState === r.state ? ' class="hl"' : '') + '><td class="st">' + r.state + '</td><td>' + r.pop.toLocaleString('en-US') + '</td><td class="q">' + q.toFixed(2) + '</td>';
        ms.forEach(function (m, j) { var down = res[m][i] < prev[m][i]; if (down) downs.push(D.methodName[m] + '：' + r.state + '（' + (H - 1) + ' 席时 ' + prev[m][i] + '，' + H + ' 席时 ' + res[m][i] + '）'); h += '<td class="' + (down ? 'down' : allSame ? '' : 'diff') + '">' + res[m][i] + '</td>'; });
        if (H === official) h += '<td class="off">' + (r.seats != null ? r.seats : '') + '</td>';
        h += '</tr>';
      });
      h += '</tbody></table>'; tbl.innerHTML = h; hl.textContent = H;
      var note = '<span>总席位 ' + H + '（' + (H === official ? '法定数' : '假设') + '）· ' + rows.length + ' 州 · 算法间席位不同的州 <b>' + diffs + '</b> 个</span>';
      if (downs.length) note += '<span>总席位从 ' + (H - 1) + ' 加到 ' + H + '，反而少一席：<b>' + downs.join('；') + '</b></span>'; else note += '<span>从 ' + (H - 1) + ' 到 ' + H + '：没有州反而少席。</span>';
      if (ds === '1900') note += '<span class="small">1900 年用的是总人口而非分配人口，与 1901 年法案在四个州各差一席（见方法）。</span>';
      read.innerHTML = note;
      if (hlState) { var tr = $('tr.hl', tbl); if (tr) tr.scrollIntoView({ block: 'nearest' }); }
    }
    function setDs(v) { ds = v; sel.value = v; var r = RANGES[v]; range.min = r[0]; range.max = r[1]; H = r[2]; range.value = H; }
    sel.addEventListener('change', function () { setDs(sel.value); hlState = null; render(); });
    range.addEventListener('input', function () { H = +range.value; render(); });
    mbox.addEventListener('change', render);
    $$('[data-demo]').forEach(function (b) { b.addEventListener('click', function () {
      clearInterval(timer); var kind = b.getAttribute('data-demo'); var sec = $('#aptbl'); sec.scrollIntoView({ behavior: RM.on ? 'auto' : 'smooth', block: 'center' });
      var hm = $('input[data-m="hamilton"]', mbox); hm.checked = true;
      if (kind === 'alabama') { setDs('1880'); hlState = 'Alabama'; H = 299; range.value = 299; render(); timer = setTimeout(function () { H = 300; range.value = 300; render(); }, 1400); }
      if (kind === 'maine') { setDs('1900'); hlState = 'Maine'; H = 350; range.value = 350; render(); timer = setInterval(function () { if (H >= 400) { clearInterval(timer); return; } H++; range.value = H; render(); }, RM.on ? 0 : 160); }
    }); });
    setDs('1880'); render();
  })();

  /* ================= 动手：画线器 + 随机地图集合 ================= */
  var ENS = { mine: function () {} };
  (function initHands() {
    var svg = $('#drawsvg'), pal = $('#dpal'), stat = $('#dstat'); if (!svg) return;
    var N2 = GN * GN, plan = [], i; for (i = 0; i < N2; i++) plan.push(-1);
    var grid = new Grid(svg, GN, CELLS, { cellLabels: true }), brush = 0, painting = null;
    function counts() { var c = []; for (var k = 0; k < SEATS_K; k++) c.push(0); plan.forEach(function (p) { if (p >= 0) c[p]++; }); return c; }
    function update() {
      var c = counts(), full = c.every(function (x) { return x === 20; }), m = null, winners = null;
      if (full) { m = G.metrics(CELLS, plan, GN, SEATS_K); winners = winnersOf(m); }
      grid.setPlan(plan, SEATS_K, winners);
      $$('button[data-d]', pal).forEach(function (b) { var k = +b.getAttribute('data-d'); if (k < 0) return; var cnt = $('[data-cnt="' + k + '"]', b); if (cnt) cnt.textContent = c[k]; b.classList.toggle('full', c[k] >= 20); });
      var bad = [];
      for (var k = 0; k < SEATS_K; k++) { if (c[k] > 20) bad.push('区 ' + (k + 1) + ' 多了 ' + (c[k] - 20) + ' 格'); else if (c[k] && !G.contiguous(plan, k, GN)) bad.push('区 ' + (k + 1) + ' 不连通'); }
      var left = N2 - c.reduce(function (a, b) { return a + b; }, 0);
      if (bad.length) { stat.textContent = bad.join('；'); stat.className = 'dstat bad'; }
      else if (left) { stat.textContent = '还有 ' + left + ' 格没分区。'; stat.className = 'dstat'; }
      else { stat.textContent = '五个区都齐了：各二十格、连通。读数算数。'; stat.className = 'dstat'; }
      var ok = full && !bad.length;
      if (ok) { seatRow($('#dseats'), m, $('#dseatsl')); $('#dwa').style.width = (m.wastedA / 60 * 100).toFixed(0) + '%'; $('#dwan').textContent = m.wastedA + ' / 60'; $('#dwb').style.width = (m.wastedB / 40 * 100).toFixed(0) + '%'; $('#dwbn').textContent = m.wastedB + ' / 40';
        $('#deg').textContent = fmtSigned(m.eg, 2); $('#dmm').textContent = fmtSigned(m.meanMedian, 2); $('#dcut').textContent = m.cutEdges; $('#dpp').textContent = m.ppMean.toFixed(2);
        MINE.plan = plan.slice(); MINE.metrics = m; var sb = $('#svmine'); if (sb) sb.disabled = false; window.YZ.svDraw && window.YZ.svDraw(); ENS.mine(m); }
      else { $$('#dseats i').forEach(function (x) { x.className = ''; }); $('#dseatsl').textContent = ''; $('#dwa').style.width = '0'; $('#dwb').style.width = '0'; $('#dwan').textContent = '—'; $('#dwbn').textContent = '—'; ['#deg', '#dmm', '#dcut', '#dpp'].forEach(function (s) { $(s).textContent = '—'; }); MINE.plan = null; MINE.metrics = null; ENS.mine(null); }
    }
    function cellAt(e) { var r = svg.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * GN, y = (e.clientY - r.top) / r.height * GN; if (x < 0 || y < 0 || x >= GN || y >= GN) return -1; return (y | 0) * GN + (x | 0); }
    function paint(e) { var i = cellAt(e); if (i < 0 || plan[i] === brush) return; if (brush >= 0 && counts()[brush] >= 20 && plan[i] !== brush) { stat.textContent = '区 ' + (brush + 1) + ' 已经二十格了——换一个区号，或者用橡皮。'; stat.className = 'dstat bad'; return; } plan[i] = brush; update(); }
    svg.addEventListener('pointerdown', function (e) { if (e.button) return; painting = e.pointerId; svg.setPointerCapture(e.pointerId); paint(e); e.preventDefault(); });
    svg.addEventListener('pointermove', function (e) { if (painting !== e.pointerId) return; paint(e); });
    function up(e) { if (painting === e.pointerId) painting = null; }
    svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
    pal.addEventListener('click', function (e) { var b = e.target.closest('button[data-d]'); if (!b) return; brush = +b.getAttribute('data-d'); $$('button[data-d]', pal).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); });
    document.addEventListener('click', function (e) { var b = e.target.closest('button[data-preset]'); if (!b) return; var k = b.getAttribute('data-preset'); plan = k === 'clear' ? plan.map(function () { return -1; }) : D.stage.plans[k].slice(); update(); });
    update();
    window.YZ.drawPlan = function () { return plan; };
  })();
  (function initEnsemble() {
    var run = $('#ensrun'), bars = $('#hbars'), st = $('#ensstat'), rd = $('#ensread'), pg = $('#ensprog'); if (!run || !bars) return;
    var hist = [], egs = [], total = 0, mineM = null, running = false, worker = null, STEPS = 3000, BURN = 300;
    for (var k = 0; k <= SEATS_K; k++) hist.push(0);
    function draw() {
      var max = Math.max(1, Math.max.apply(null, hist));
      $$('.hbar', bars).forEach(function (hb) { var s = +hb.getAttribute('data-s'), u = $('u', hb), b = $('b', hb); u.style.height = (hist[s] / max * 100).toFixed(1) + '%'; var isYou = mineM && mineM.seatsA === s; u.classList.toggle('you', !!isYou); hb.classList.toggle('you', !!isYou); b.innerHTML = s + ':' + (SEATS_K - s) + '<small>' + (total ? (hist[s] / total * 100).toFixed(1) + '%' : '甲 ' + s + ' 席') + (isYou ? ' · 你' : '') + '</small>'; });
      if (!total) { rd.textContent = ''; return; }
      var t = '抽了 ' + total.toLocaleString('en-US') + ' 张：甲得 ' + hist.map(function (c, s) { return s + ' 席 ' + (c / total * 100).toFixed(1) + '%'; }).filter(function (x, s) { return hist[s]; }).join('、') + '。';
      if (mineM) { var le = egs.filter(function (e) { return e <= mineM.eg; }).length, pct = le / total * 100; t += ' 你画的那张：甲 ' + mineM.seatsA + ' 席，效率差 ' + fmtSigned(mineM.eg, 2) + '——' + (pct < 2.5 || pct > 97.5 ? '落在分布最极端的 ' + Math.min(pct, 100 - pct).toFixed(1) + '% 里，是一张离群的图。' : '按效率差排在第 ' + pct.toFixed(0) + ' 百分位，随机画也常画出这样的。'); }
      rd.innerHTML = t.replace(/(你画的那张[^。]*。?)/, '<b>$1</b>');
    }
    ENS.mine = function (m) { mineM = m; draw(); };
    function start() {
      if (running) return; running = true; run.disabled = true; hist = hist.map(function () { return 0; }); egs = []; total = 0; st.textContent = '在跑……';
      var src = document.getElementById('geojs').textContent, blob = new Blob([src], { type: 'text/javascript' });
      try { worker = new Worker(URL.createObjectURL(blob)); } catch (e) { st.textContent = '这个浏览器不让开后台线程，改在主线程慢慢跑。'; worker = null; }
      var seed = (Date.now() % 100000) | 1;
      if (worker) {
        worker.onmessage = function (ev) { var m = ev.data; m.batch.forEach(function (b, idx) { if (m.done - m.batch.length + idx >= BURN) { hist[b[0]]++; egs.push(b[1]); total++; } }); pg.style.width = (m.done / m.total * 100).toFixed(1) + '%'; draw(); if (m.done >= m.total) { running = false; run.disabled = false; st.textContent = '跑完了，' + (m.ms / 1000).toFixed(1) + ' 秒。再点一次换一组随机数。'; worker.terminate(); } };
        worker.postMessage({ cells: CELLS, plan: null, n: GN, K: SEATS_K, steps: STEPS, seed: seed, every: 100 });
      } else {
        var cur = G.strips(GN, SEATS_K), rnd = G.RNG(seed), s = 0;
        (function step() { var t0 = performance.now(); while (performance.now() - t0 < 16 && s < STEPS) { var nx = G.recomStep(cur, GN, SEATS_K, 20, rnd); if (nx) cur = nx; var m = G.metrics(CELLS, cur, GN, SEATS_K); if (s >= BURN) { hist[m.seatsA]++; egs.push(m.eg); total++; } s++; } pg.style.width = (s / STEPS * 100).toFixed(1) + '%'; draw(); if (s < STEPS) requestAnimationFrame(step); else { running = false; run.disabled = false; st.textContent = '跑完了。'; } })();
      }
    }
    run.addEventListener('click', start);
    draw();
  })();
})();
