(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  window.YZ = { D: D };

  /* ================= 共用 ================= */
  var RM = { on: false };
  try { var rmq = window.matchMedia('(prefers-reduced-motion: reduce)'); RM.on = rmq.matches; var rmc = function (e) { RM.on = e.matches; }; if (rmq.addEventListener) rmq.addEventListener('change', rmc); else if (rmq.addListener) rmq.addListener(rmc); } catch (e) {}
  function Spring(o) { this.x = o.from || 0; this.v = 0; this.target = this.x; this.z = o.damping == null ? 1 : o.damping; this.T = o.response || 0.4; this.eps = o.eps || 0.001; this.onUpdate = o.onUpdate || function () {}; this.raf = 0; this.running = false; this.last = 0; }
  Spring.prototype.to = function (target) {
    this.target = target;
    if (RM.on) { this.set(target); return this; }
    if (!this.running) { var self = this; this.running = true; this.last = performance.now(); this.raf = requestAnimationFrame(function step(now) { self.tick(now); if (self.running) self.raf = requestAnimationFrame(step); }); }
    return this;
  };
  Spring.prototype.tick = function (now) {
    var dt = Math.min(0.05, Math.max(0, (now - this.last) / 1000)); this.last = now;
    var w = 2 * Math.PI / this.T, k = w * w, c = 2 * this.z * w, n = Math.max(1, Math.ceil(dt * 240)), h = dt / n;
    for (var i = 0; i < n; i++) { var a = -k * (this.x - this.target) - c * this.v; this.v += a * h; this.x += this.v * h; }
    if (Math.abs(this.x - this.target) < this.eps && Math.abs(this.v) < this.eps * 8) { this.x = this.target; this.v = 0; this.running = false; }
    this.onUpdate(this.x, this.v);
  };
  Spring.prototype.set = function (x) { if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0; this.running = false; this.x = x; this.target = x; this.v = 0; this.onUpdate(x, 0); };
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ================= 深浅色（默认墨黑） ================= */
  try { var saved = localStorage.getItem('yzyt-theme-3'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  function curTheme() { return root.getAttribute('data-theme') || 'dark'; }
  function themeLabel() { if (!tb) return; var d = curTheme() === 'dark'; tb.textContent = d ? '白天读' : '夜里读'; tb.setAttribute('aria-label', d ? '换成浅色' : '换成深色'); }
  if (tb) { themeLabel(); tb.addEventListener('click', function () { var next = curTheme() === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next); themeLabel(); try { localStorage.setItem('yzyt-theme-3', next); } catch (e) {} }); }

  /* ================= 入场与论点 ================= */
  (function () {
    var h = $('#top'); if (!h) return; var rs = $$('.rise', h);
    if (RM.on) { rs.forEach(function (el) { el.classList.add('in'); }); return; }
    requestAnimationFrame(function () { rs.forEach(function (el, i) { el.style.transitionDelay = (0.1 + Math.min(i * 0.08, 0.4)).toFixed(2) + 's'; el.classList.add('in'); }); });
  })();
  (function () {
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
      var y = window.scrollY + navH() + 40, cur = -1;
      for (var i = 0; i < secs.length; i++) if (secs[i] && secs[i].getBoundingClientRect().top + window.scrollY <= y) cur = i;
      links.forEach(function (a, i) { var on = i === cur; if (on !== a.classList.contains('on')) { a.classList.toggle('on', on); if (on && nav) { var r = a.getBoundingClientRect(), rr = nav.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) a.parentNode.scrollLeft += r.left - rr.left - 20; } } });
    });
  }
  setNavH(); onScrollNav();
  window.addEventListener('scroll', onScrollNav, { passive: true });
  window.addEventListener('resize', function () { setNavH(); onScrollNav(); });

  /* ================= 行：展开 / 收起（四个列表共用）；透镜：分组重排（FLIP） ================= */
  function toggleRow(r, open) { var o = open == null ? !r.classList.contains('open') : open; r.classList.toggle('open', o); var b = $('.lhead', r); if (b) b.setAttribute('aria-expanded', String(o)); }
  document.addEventListener('click', function (e) { var b = e.target.closest('.lhead'); if (b) toggleRow(b.closest('.lrow')); });
  function scrollToRow(r) {
    var lb = $('.lensbar', r.parentNode.parentNode), off = navH() + (lb ? lb.offsetHeight : 0) + 8;
    window.scrollTo({ top: Math.max(0, r.getBoundingClientRect().top + window.scrollY - off), behavior: RM.on ? 'auto' : 'smooth' });
  }
  function openRow(id) {
    var r = document.getElementById('n-' + id); if (!r) return false;
    toggleRow(r, true); scrollToRow(r); r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1400);
    try { history.replaceState(null, '', '#n-' + id); } catch (er) {}
    return true;
  }
  function initList(key) {
    var grid = $('#lgrid-' + key), lensEl = $('#lens-' + key); if (!grid || !lensEl) return;
    var rows = {}; $$('.lrow', grid).forEach(function (r) { rows[r.getAttribute('data-id')] = r; });
    var tabs = $$('button[data-lens]', lensEl), cur = (tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0]).getAttribute('data-lens'), note = $('#lensnote-' + key);
    var pill = document.createElement('span'); pill.className = 'pill'; lensEl.insertBefore(pill, lensEl.firstChild);
    var px = new Spring({ response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
    var pw = new Spring({ response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
    function movePill(instant) { var b = tabs.filter(function (t) { return t.getAttribute('data-lens') === cur; })[0]; if (!b) return; var x = b.offsetLeft, w = b.offsetWidth; if (instant) { px.set(x); pw.set(w); } else { px.to(x); pw.to(w); } }
    function header(g) { var h = document.createElement('div'); h.className = 'lgh'; h.setAttribute('data-g', g.k); h.innerHTML = '<b>' + esc(g.label) + '</b><small>' + g.ids.length + ' 条</small>'; return h; }
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
      $$('.lgh', grid).forEach(function (h) { if (h.animate) h.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'cubic-bezier(.22,1,.36,1)' }); });
    }
    lensEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-lens]'); if (b) setLens(b.getAttribute('data-lens')); });
    lensEl.addEventListener('keydown', function (e) { if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return; var i = tabs.findIndex(function (t) { return t.getAttribute('data-lens') === cur; }), n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); setLens(n.getAttribute('data-lens')); e.preventDefault(); });
    movePill(true); setNote();
    window.addEventListener('resize', function () { movePill(true); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); });
  }
  ['moves', 'nodes', 'works'].forEach(initList);
  var m0 = /^#n-([\w-]+)$/.exec(location.hash || '');
  if (m0) setTimeout(function () { openRow(m0[1]); }, 80);

  /* ================= 序章：地图舞台 ================= */
  var stageGo = function () {};
  (function initStage() {
    var pin = $('#stpin'), st = $('#ststage'), wrap = $('#stmap'), side = $('#stside'), ruler = $('#struler'), knob = $('#stknob'); if (!pin || !wrap) return;
    var MAP = D.map, steps = D.stage, N = steps.length, cur = -1, t = 0;
    // 底图：省界形状、九段线与南海诸岛附图照首发版画法；文字标注只来自各节点的 labels
    var W = MAP.w, H = MAP.h + 46, ins = MAP.inset, iw = ins.x1 - ins.x0, ih = ins.y1 - ins.y0, isc = 172 / iw, bw = 172, bh = ih * isc, bx = W - bw - 8, by = H - bh - 8;
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="中国省级行政区地图，按所选时代高亮舞蹈发生地与传播路线">';
    s += '<defs><clipPath id="ic"><rect x="' + ins.x0 + '" y="' + ins.y0 + '" width="' + iw + '" height="' + ih + '"/></clipPath></defs><g id="layers">';
    Object.keys(MAP.prov).forEach(function (c) { s += '<path class="prov" id="p-' + c + '" d="' + MAP.prov[c].d + '"/>'; });
    s += '<path class="jd" d="' + MAP.jd + '"/>' + MAP.islands.map(function (p) { return '<circle class="isl" cx="' + p[0] + '" cy="' + p[1] + '" r="1.6"/>'; }).join('');
    s += '</g><g id="routes"></g><g id="labels"></g>';
    s += '<g transform="translate(' + bx + ' ' + by + ') scale(' + isc + ') translate(' + (-ins.x0) + ' ' + (-ins.y0) + ')" clip-path="url(#ic)" pointer-events="none"><rect class="inset-box" x="' + ins.x0 + '" y="' + ins.y0 + '" width="' + iw + '" height="' + ih + '" style="stroke-width:' + (1.2 / isc).toFixed(2) + '"/><use href="#layers"/></g>';
    s += '<text class="inset-title" x="' + (bx + 6) + '" y="' + (by + 14) + '">南海诸岛</text><text class="map-note" x="12" y="' + (H - 12) + '">' + esc(MAP.note) + '</text></svg>';
    wrap.innerHTML = s;
    var prov = {}; Object.keys(MAP.prov).forEach(function (c) { prov[c] = $('#p-' + c, wrap); });
    var routeLayer = $('#routes', wrap), labelLayer = $('#labels', wrap);
    function cen(c) { var p = MAP.prov[c]; return p ? p.c : null; }
    function pathThrough(codes) {
      var pts = codes.map(cen).filter(Boolean); if (pts.length < 2) return '';
      var d = 'M' + pts[0][0] + ' ' + pts[0][1];
      for (var i = 1; i < pts.length; i++) { var a = pts[i - 1], b = pts[i], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 - Math.min(60, Math.hypot(b[0] - a[0], b[1] - a[1]) * 0.25); d += ' Q' + mx + ' ' + my + ' ' + b[0] + ' ' + b[1]; }
      return d;
    }
    // 图版：每个节点一张，就近三张才加载
    var imgs = steps.map(function (sn) { var im = document.createElement('img'); im.alt = ''; im.decoding = 'async'; im.setAttribute('data-src', sn.img); side.insertBefore(im, side.firstChild); return im; });
    function load(i) { var im = imgs[i]; if (im && !im.getAttribute('src')) im.setAttribute('src', im.getAttribute('data-src')); }
    var ticks = $$('.rtick', ruler);
    function show(i) {
      if (i === cur) return; cur = i; var n = steps[i];
      Object.keys(prov).forEach(function (c) { prov[c].classList.toggle('hi', n.hi.indexOf(c) >= 0); });
      var r = '';
      n.route.forEach(function (codes) { var d = pathThrough(codes); if (!d) return; r += '<path class="route" d="' + d + '"/>'; codes.forEach(function (c) { var p = cen(c); if (p) r += '<circle class="rdot" cx="' + p[0] + '" cy="' + p[1] + '" r="4.5"/>'; }); });
      routeLayer.innerHTML = r;
      // 标注：估出每条的宽度，先夹在画框里，再自上而下错开，不让两条压在一起
      var boxes = [], l = '', fs = window.innerWidth <= 900 ? 22 : 15;
      n.labels.map(function (lb) { return { t: window.innerWidth <= 900 ? lb.text.split(/[：（(]/)[0] : lb.text, p: cen(lb.code) }; }).filter(function (o) { return o.p; }).sort(function (a, b) { return a.p[1] - b.p[1]; }).forEach(function (o) {
        var tw = 0; for (var i = 0; i < o.t.length; i++) tw += o.t.charCodeAt(i) > 255 ? fs * 1.05 : fs * 0.6;
        var x = clamp(o.p[0], tw / 2 + 8, W - tw / 2 - 8), y = o.p[1] - 10, guard = 0;
        while (guard++ < 12 && boxes.some(function (b) { return Math.abs(b.x - x) < (b.w + tw) / 2 + 6 && Math.abs(b.y - y) < fs + 4; })) y += fs + 5;
        boxes.push({ x: x, y: y, w: tw });
        l += '<text class="lbl" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="middle">' + esc(o.t) + '</text>';
      });
      labelLayer.innerHTML = l;
      [i - 1, i, i + 1].forEach(load);
      imgs.forEach(function (im, k) { im.classList.toggle('on', k === i); });
      $('#stera').textContent = n.era; $('#styears').textContent = n.era === n.years ? '' : n.years; $('#sttitle').textContent = n.title; $('#stlayer').textContent = n.layer; $('#stwhy').textContent = n.why; $('#stcap').textContent = '图：' + n.cap;
      ticks.forEach(function (tk, k) { tk.classList.toggle('on', k === i); });
      ruler.setAttribute('aria-valuenow', String(i)); ruler.setAttribute('aria-valuetext', n.era + ' ' + n.years);
    }
    function setT(v) { t = clamp(v, 0, N - 1); knob.style.left = 'calc(var(--gut) + 20px + (100% - 2 * var(--gut) - 40px) * ' + (t / (N - 1)).toFixed(4) + ')'; show(Math.round(t)); }
    function span() { return pin.offsetHeight - st.offsetHeight; }
    var tick = false;
    function onScroll() { if (tick) return; tick = true; requestAnimationFrame(function () { tick = false; var r = pin.getBoundingClientRect(), p = clamp((-r.top + navH()) / Math.max(1, span()), 0, 1); setT(p * (N - 1)); }); }
    window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); onScroll();
    // 刻度尺：拖动 = 把页面滚到对应位置（滚动与刻度是同一个量）
    function scrollToT(v, smooth) { var top = pin.getBoundingClientRect().top + window.scrollY - navH() + clamp(v, 0, N - 1) / (N - 1) * span(); window.scrollTo({ top: top + 2, behavior: smooth && !RM.on ? 'smooth' : 'auto' }); }
    var drag = null, track = $('.rtrack', ruler);
    function tFromX(x) { var r = track.getBoundingClientRect(); return clamp((x - r.left) / Math.max(1, r.width), 0, 1) * (N - 1); }
    ruler.addEventListener('pointerdown', function (e) { if (e.button) return; drag = { id: e.pointerId }; ruler.setPointerCapture(e.pointerId); scrollToT(tFromX(e.clientX), false); e.preventDefault(); });
    ruler.addEventListener('pointermove', function (e) { if (!drag || e.pointerId !== drag.id) return; scrollToT(tFromX(e.clientX), false); });
    function up(e) { if (!drag || e.pointerId !== drag.id) return; drag = null; scrollToT(Math.round(t), true); }
    ruler.addEventListener('pointerup', up); ruler.addEventListener('pointercancel', up);
    ruler.addEventListener('keydown', function (e) { var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : e.key === 'Home' ? -N : e.key === 'End' ? N : 0; if (!d) return; scrollToT(clamp(Math.round(t) + d, 0, N - 1), true); e.preventDefault(); });
    $('#stopen').addEventListener('click', function () { openRow(steps[Math.max(0, cur)].id); });
    stageGo = function (id) { for (var i = 0; i < N; i++) if (steps[i].id === id) { scrollToT(i, true); return; } };
    show(0);
    window.YZ.stage = { cur: function () { return cur; }, go: stageGo };
  })();
  document.addEventListener('click', function (e) { var b = e.target.closest('[data-tomap]'); if (b) stageGo(b.getAttribute('data-tomap')); });

  /* ================= 01：事件条（鼠标可拖） ================= */
  (function () {
    var el = $('#evs'); if (!el) return; var d = null;
    el.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse' || e.button || e.target.closest('a')) return; d = { x: e.clientX, s: el.scrollLeft, id: e.pointerId, moved: false }; });
    window.addEventListener('pointermove', function (e) { if (!d || e.pointerId !== d.id) return; var dx = e.clientX - d.x; if (Math.abs(dx) > 3) { d.moved = true; el.classList.add('drag'); } el.scrollLeft = d.s - dx; });
    window.addEventListener('pointerup', function (e) { if (!d || e.pointerId !== d.id) return; d = null; el.classList.remove('drag'); });
  })();

  /* ================= 01：动作台（墨线小人：慢放 / 逐帧 / 定格） ================= */
  var labSelect = function () {};
  (function initLab() {
    var svg = $('#labsvg'), stageEl = $('#labstage'); if (!svg || typeof mountDanceFig !== 'function') return;
    // 墨线滤镜放在一张常驻的隐形 svg 里，免得被某个小人的 svg 清空时带走
    if (!document.getElementById('dance-ink')) {
      var holder = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); holder.setAttribute('width', '0'); holder.setAttribute('height', '0'); holder.setAttribute('aria-hidden', 'true'); holder.style.position = 'absolute';
      holder.innerHTML = '<defs><filter id="dance-ink" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.5" xChannelSelector="R" yChannelSelector="G"/></filter></defs>';
      document.body.appendChild(holder);
    }
    var MV = {}; D.moves.forEach(function (m) { MV[m.id] = m; });
    var figMoves = D.moves.filter(function (m) { return m.fig; });
    var marksOf = { shan: window.SHAN_MARKS || (typeof SHAN_MARKS !== 'undefined' ? SHAN_MARKS : null) };
    var st = { m: null, h: null, t: 0, T: 1, playing: !RM.on, speed: 1, vis: false, raf: 0, last: 0, acc: 0 };
    var scrub = $('#labscrub'), playB = $('#labplay'), tl = $('#labt'), card = $('#labcard'), marksEl = $('#labmarks'), marksK = $('#labmarksk');
    function sexOf(f) { return f === 'dou' ? 'm' : 'f'; }
    function readout() { var tt = ((st.t % st.T) + st.T) % st.T; scrub.value = String(Math.round(tt / st.T * 1000)); tl.textContent = tt.toFixed(2) + ' / ' + st.T.toFixed(2) + ' 秒' + (st.speed !== 1 ? ' · ' + (st.speed === 0.5 ? '½' : '¼') + ' 速' : ''); }
    function setPlaying(p) { st.playing = p; playB.textContent = p ? D.t.pause : D.t.play; playB.setAttribute('aria-pressed', String(p)); if (p) kick(); }
    function frame(now) {
      st.raf = 0; if (!st.playing || !st.vis || !st.h) return;
      var dt = Math.min(0.1, (now - st.last) / 1000); st.last = now; st.acc += dt;
      if (st.acc >= 0.03) { st.t += st.acc * st.speed; st.acc = 0; st.h.drawAt(st.t); readout(); }
      st.raf = requestAnimationFrame(frame);
    }
    function kick() { if (st.raf || !st.playing || !st.vis) return; st.last = performance.now(); st.raf = requestAnimationFrame(frame); }
    function still(t) { st.t = t; if (st.h) st.h.setTime(t); readout(); }
    function select(id, keepPlay) {
      var m = MV[id]; if (!m || !m.fig) return;
      if (st.h) st.h.stop(); while (svg.firstChild) svg.removeChild(svg.firstChild);
      st.m = m; st.h = mountDanceFig(svg, { move: m.fig, sex: sexOf(m.fig), style: 'ink', props: true }); st.T = st.h.T; st.t = 0; st.h.drawAt(0);
      $$('#labtabs [data-move]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-move') === id)); });
      var mk = marksOf[m.fig]; marksEl.style.display = marksK.style.display = mk ? '' : 'none';
      card.innerHTML = '<h3>' + esc(m.name) + '</h3>' + (m.cue ? '<p class="cue">' + esc(m.cue) + '</p>' : '') + '<dl class="kv"><dt>' + esc(D.t.labels.how) + '</dt><dd>' + esc(m.how) + '</dd><dt>' + esc(D.t.labels.life) + '</dt><dd>' + esc(m.life) + '</dd><dt>' + esc(D.t.labels.risk) + '</dt><dd>' + esc(m.risk) + '</dd></dl><button class="sbtn" type="button" data-openrow="' + m.id + '">' + esc(D.t.open) + '</button><p class="small" style="margin:12px 0 0">' + esc(m.deck) + '</p>';
      if (RM.on) { setPlaying(false); still(mk ? mk.flash : 1.0); } else if (keepPlay === false) { setPlaying(false); still(0); } else { setPlaying(true); readout(); }
    }
    $('#labtabs').addEventListener('click', function (e) { var b = e.target.closest('[data-move]'); if (b) select(b.getAttribute('data-move')); });
    playB.addEventListener('click', function () { setPlaying(!st.playing); });
    $('#labspeed').addEventListener('click', function (e) { var b = e.target.closest('[data-sp]'); if (!b) return; st.speed = +b.getAttribute('data-sp'); $$('#labspeed [data-sp]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); readout(); });
    marksEl.addEventListener('click', function (e) { var b = e.target.closest('[data-mark]'); if (!b || !st.m) return; var mk = marksOf[st.m.fig]; if (!mk) return; setPlaying(false); still(mk[b.getAttribute('data-mark')]); });
    scrub.addEventListener('input', function () { setPlaying(false); st.t = +scrub.value / 1000 * st.T; st.h.drawAt(st.t); readout(); });
    // 左右拖小人 = 逐帧
    var drag = null;
    stageEl.addEventListener('pointerdown', function (e) { if (e.button) return; drag = { id: e.pointerId, x: e.clientX, t: ((st.t % st.T) + st.T) % st.T, was: st.playing, moved: false }; try { stageEl.setPointerCapture(e.pointerId); } catch (er) {} });
    stageEl.addEventListener('pointermove', function (e) { if (!drag || e.pointerId !== drag.id) return; var dx = e.clientX - drag.x; if (!drag.moved && Math.abs(dx) < 4) return; if (!drag.moved) { drag.moved = true; setPlaying(false); } st.t = (((drag.t + dx / Math.max(1, stageEl.clientWidth) * st.T) % st.T) + st.T) % st.T; st.h.drawAt(st.t); readout(); });
    function dup(e) { if (!drag || e.pointerId !== drag.id) return; var d = drag; drag = null; if (!d.moved) setPlaying(!st.playing); }
    stageEl.addEventListener('pointerup', dup); stageEl.addEventListener('pointercancel', function () { drag = null; });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { es.forEach(function (en) { st.vis = en.isIntersecting; if (st.vis) kick(); }); }, { rootMargin: '80px 0px' }).observe(stageEl); else { st.vis = true; }
    select(figMoves[0].id);
    labSelect = function (id) { select(id); var sec = $('#lab'); window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - navH() - 8, behavior: RM.on ? 'auto' : 'smooth' }); };
    window.YZ.lab = st;
    // 行头的小静帧
    $$('svg[data-thumb]').forEach(function (s) { var f = s.getAttribute('data-thumb'), h = mountDanceFig(s, { move: f, sex: sexOf(f), style: 'ink', props: true, ribbon: false }); h.setTime(marksOf[f] ? marksOf[f].flash : 1.0); });
  })();
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-tolab]'); if (a) { labSelect(a.getAttribute('data-tolab')); return; }
    var b = e.target.closest('[data-openrow]'); if (b) openRow(b.getAttribute('data-openrow'));
  });

  /* ================= 01：动作查找器 ================= */
  (function () {
    var inp = $('#finder-in'), out = $('#finder-out'); if (!inp) return;
    function find(q) {
      q = (q || '').trim(); if (!q) return;
      var m = D.moves.filter(function (x) { return x.name === q; })[0] || D.moves.filter(function (x) { return x.name.indexOf(q) >= 0 || q.indexOf(x.name) >= 0; })[0];
      if (m) { out.textContent = ''; openRow(m.id); return; }
      var n = D.nameOnly.filter(function (x) { return x.name === q; })[0] || D.nameOnly.filter(function (x) { return x.name.indexOf(q) >= 0; })[0];
      out.textContent = n ? D.t.nameonly.replace('{name}', n.name).replace('{deck}', n.deck) : D.t.none.replace('{name}', q).replace('{n}', String(D.moves.length + D.nameOnly.length));
    }
    $('#finder-go').addEventListener('click', function () { find(inp.value); });
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { find(inp.value); e.preventDefault(); } });
    inp.addEventListener('change', function () { find(inp.value); });
    $('#finder-rand').addEventListener('click', function () { var m = D.moves[Math.floor(Math.random() * D.moves.length)]; inp.value = m.name; find(m.name); });
  })();
})();
