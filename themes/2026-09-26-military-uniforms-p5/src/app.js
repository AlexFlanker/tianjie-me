(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  var SVGNS = 'http://www.w3.org/2000/svg';
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  window.YZ = { D: D };

  /* ================= 共用：减少动效（实时）、弹簧、速度、动量投影 ================= */
  var RM = { on: false };
  try { var rmq = window.matchMedia('(prefers-reduced-motion: reduce)'); RM.on = rmq.matches; var rmc = function (e) { RM.on = e.matches; }; if (rmq.addEventListener) rmq.addEventListener('change', rmc); else if (rmq.addListener) rmq.addListener(rmc); } catch (e) {}
  // Apple 的两参数弹簧：阻尼比 z（1 = 临界阻尼，不回弹）+ response T（秒）。永远从当前值出发，可随时改目标，松手时可带初速度。
  function Spring(o) {
    this.x = o.from || 0; this.v = 0; this.target = this.x; this.z = o.damping == null ? 1 : o.damping; this.T = o.response || 0.4;
    this.eps = o.eps || 0.001; this.onUpdate = o.onUpdate || function () {}; this.onRest = o.onRest || null; this.raf = 0; this.running = false; this.last = 0;
  }
  Spring.prototype.to = function (target, o) {
    o = o || {};
    if (o.velocity != null) this.v = o.velocity;
    if (o.damping != null) this.z = o.damping;
    if (o.response != null) this.T = o.response;
    this.target = target;
    if (RM.on) { this.stop(); this.x = target; this.v = 0; this.onUpdate(this.x, 0); if (this.onRest) this.onRest(); return this; }
    if (!this.running) {
      var self = this; this.running = true; this.last = performance.now();
      this.raf = requestAnimationFrame(function step(now) { self.tick(now); if (self.running) self.raf = requestAnimationFrame(step); });
    }
    return this;
  };
  Spring.prototype.tick = function (now) {
    var dt = Math.min(0.05, Math.max(0, (now - this.last) / 1000)); this.last = now;
    var w = 2 * Math.PI / this.T, k = w * w, c = 2 * this.z * w, n = Math.max(1, Math.ceil(dt * 240)), h = dt / n;
    for (var i = 0; i < n; i++) { var a = -k * (this.x - this.target) - c * this.v; this.v += a * h; this.x += this.v * h; }
    if (Math.abs(this.x - this.target) < this.eps && Math.abs(this.v) < this.eps * 8) {
      this.x = this.target; this.v = 0; this.running = false; this.onUpdate(this.x, 0); if (this.onRest) this.onRest(); return;
    }
    this.onUpdate(this.x, this.v);
  };
  Spring.prototype.set = function (x) { this.stop(); this.x = x; this.target = x; this.v = 0; this.onUpdate(x, 0); };
  Spring.prototype.stop = function () { if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0; this.running = false; };
  // 最近 100 ms 的位置历史 → 松手速度（单位 / 秒）；停住超过 80 ms 再松手算 0
  function VTrack() { this.s = []; }
  VTrack.prototype.add = function (x) { var t = performance.now(); this.s.push([t, x]); while (this.s.length > 2 && t - this.s[0][0] > 100) this.s.shift(); };
  VTrack.prototype.v = function () { var s = this.s; if (s.length < 2) return 0; var a = s[0], b = s[s.length - 1], dt = (b[0] - a[0]) / 1000; if (dt <= 0 || performance.now() - b[0] > 80) return 0; return (b[1] - a[1]) / dt; };
  VTrack.prototype.reset = function () { this.s = []; };
  // Apple《Designing Fluid Interfaces》示例代码里的投影：指数衰减，d ≈ 0.998
  function project(v, d) { d = d || 0.998; return (v / 1000) * d / (1 - d); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function smooth(u) { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); }
  // 触屏拖动的方向判定：先看前 6 px 往哪走，横向才接管（竖向交给页面滚动）
  function dragIntent(e, sx, sy) { var dx = e.clientX - sx, dy = e.clientY - sy; if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return 0; return Math.abs(dx) > Math.abs(dy) ? 1 : -1; }
  function el(tag, attrs, parent) { var n = document.createElementNS(SVGNS, tag); for (var k in attrs) n.setAttribute(k, attrs[k]); if (parent) parent.appendChild(n); return n; }
  window.YZ.Spring = Spring;

  /* ================= 深浅色：这一题默认是深色；用户切过就记住 ================= */
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  function curTheme() { return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark'; }
  function themeLabel() { if (!tb) return; var d = curTheme() === 'dark'; tb.textContent = d ? '白天读' : '夜里读'; tb.setAttribute('aria-label', d ? '换成浅色' : '换成深色'); }
  if (tb) { themeLabel(); tb.addEventListener('click', function () {
    var next = curTheme() === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next); themeLabel();
    try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
  }); }

  /* ================= 入场 ================= */
  var fades = $$('.fade').concat($$('.rise').filter(function (n) { return !n.closest('#top'); }));
  if ('IntersectionObserver' in window && !RM.on) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (n) { io.observe(n); });
  } else { fades.forEach(function (n) { n.classList.add('in'); }); }

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

  /* ================= 卷首：标题依次升起；论点逐词点亮 ================= */
  (function initHero() {
    var h = $('#top'); if (!h) return;
    var rs = $$('.rise', h);
    if (RM.on) { rs.forEach(function (n) { n.classList.add('in'); }); return; }
    requestAnimationFrame(function () { rs.forEach(function (n, i) { n.style.transitionDelay = (0.15 + Math.min(i * 0.08, 0.4)).toFixed(2) + 's'; n.classList.add('in'); }); });
  })();
  (function initTagline() {
    var sec = $('#tagsec'); if (!sec) return;
    var ws = $$('.tagl .w', sec), rest = $('.tagrest', sec), tagl = $('.tagl', sec), inner = $('.tagstick > .wide', sec), tick = false;
    function upd() {
      tick = false;
      if (RM.on) { ws.forEach(function (w) { w.classList.add('on'); }); if (rest) rest.classList.add('on'); return; }
      var nh = navH(), avail = window.innerHeight - nh;
      var fits = inner.offsetHeight + 48 <= avail;   // 放得下才钉住
      if (fits === sec.classList.contains('flow')) sec.classList.toggle('flow', !fits);
      var p;
      if (fits) { var r = sec.getBoundingClientRect(), span = sec.offsetHeight - avail; p = clamp((nh - r.top) / (span > 0 ? span : 1), 0, 1); }
      else { var t = tagl.getBoundingClientRect(); p = clamp((window.innerHeight * 0.8 - t.top) / (window.innerHeight * 0.45), 0, 1); }
      var n = Math.floor(p * (ws.length + 3));
      ws.forEach(function (w, i) { var on = i < n; if (on !== w.classList.contains('on')) w.classList.toggle('on', on); });
      if (rest) rest.classList.toggle('on', n >= ws.length + 1);
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener('resize', upd); upd();
  })();

  /* ================= 序章 · 八个时代：全屏舞台（滚动与尺子是同一个量 t = 第几个时代） ================= */
  var LISTS = {};   // 透镜列表的开行接口，舞台卡片、总线圆点、行内链接都用它
  function openRow(id) { for (var k in LISTS) if (LISTS[k].has(id)) { LISTS[k].open(id); return true; } return false; }
  (function initStage() {
    var pin = $('#tlpin'), stg = $('#tlstage'), LV = D.stage; if (!pin || !stg || !LV) return;
    var N = LV.length;
    var card = $('#tlcard'), ruler = $('#tlruler'), track = $('#rtrack'), head = $('#rhead');
    var E = { no: $('#tlno'), range: $('#tlrange'), name: $('#tlname'), text: $('#tltext'), rows: $('#tlrows'), cs: $('#tlcs'), cr: $('#tlcr') };
    var P = [$('#tlp0'), $('#tlp1')], BG = [$('#tlbg0'), $('#tlbg1')], cur = 0;
    var marks = $$('.rmark', ruler);
    var stageH = 0, perStep = 0, pinTop = 0;
    function layout() {
      stageH = stg.offsetHeight; perStep = Math.round(window.innerHeight * (window.innerWidth < 700 ? 0.55 : 0.7));
      pin.style.height = (stageH + (N - 1) * perStep) + 'px';
      pinTop = pin.getBoundingClientRect().top + window.scrollY;
      ruler.classList.toggle('all', track.clientWidth >= 860);
    }
    function tFromScroll() { return clamp((window.scrollY - (pinTop - navH())) / perStep, 0, N - 1); }
    function scrollForT(t) { return pinTop - navH() + t * perStep; }
    $$('.tlhd, .tlname, .tltext, .tlrows', card).forEach(function (n) { n.classList.add('swap'); });
    function fillCard(k) {
      var L = LV[k];
      E.no.textContent = ('0' + (k + 1)).slice(-2) + ' / ' + ('0' + N).slice(-2); E.range.textContent = L.range; E.name.textContent = L.name; E.text.textContent = L.text;
      E.rows.innerHTML = L.rows.map(function (r) {
        return '<li><button type="button" data-row="' + esc(r.row) + '"><b>' + esc(r.cn) + '</b><span class="sw">' + r.colors.map(function (c) { return '<i style="background:' + esc(c) + '"></i>'; }).join('') + '</span><em>' + esc(r.name) + '</em></button></li>';
      }).join('');
    }
    var swapT = 0, shown = -1;
    function showCard(k) {
      if (k === shown) return; var first = shown < 0; shown = k;
      if (first) return;
      if (RM.on) { fillCard(k); return; }
      clearTimeout(swapT); card.classList.add('swapping');
      swapT = setTimeout(function () { fillCard(k); card.classList.remove('swapping'); }, 160);
    }
    E.rows.addEventListener('click', function (e) { var b = e.target.closest('button[data-row]'); if (b) openRow(b.getAttribute('data-row')); });
    // 照片：两层交替；往后走新图从右边进来，往前走从左边
    var picK = 0, picTimer = 0;
    function setCap(L) { E.cs.textContent = L.cap; E.cr.textContent = L.cred; }
    function showPic(k) {
      if (k === picK) return;
      var dir = k > picK ? 1 : -1, L = LV[k]; picK = k;
      var out = P[cur], inn = P[1 - cur], bo = BG[cur], bi = BG[1 - cur];
      var go = function () {
        if (picK !== k) return;
        inn.className = RM.on ? '' : (dir > 0 ? 'from-r' : 'from-l'); void inn.offsetWidth;
        inn.className = 'on'; out.className = RM.on ? '' : (dir > 0 ? 'to-l' : 'to-r');
        bi.className = 'on'; bo.className = '';
        cur = 1 - cur; setCap(L);
        setTimeout(function () { if (out !== P[cur]) out.className = ''; }, 520);
      };
      inn.alt = L.alt; inn.width = L.w; inn.height = L.h; bi.src = L.img;
      if (inn.getAttribute('src') === L.img && inn.complete) { go(); return; }
      inn.src = L.img;
      if (inn.decode) inn.decode().then(go, go); else inn.onload = go;
    }
    function prefetch(k) { [k - 1, k + 1].forEach(function (j) { if (LV[j]) { var im = new Image(); im.decoding = 'async'; im.src = LV[j].img; } }); }
    var curK = -1, near = false;
    function render(t) {
      var k = clamp(Math.round(t), 0, N - 1), L = LV[k];
      if (k !== curK) {
        var first = curK < 0; curK = k;
        showCard(k);
        clearTimeout(picTimer); if (first) picK = 0; else picTimer = setTimeout(function () { showPic(k); }, RM.on ? 0 : 120);
        marks.forEach(function (m, i) { m.classList.toggle('on', i === k); });
        ruler.setAttribute('aria-valuenow', k); ruler.setAttribute('aria-valuetext', L.name + '，' + L.range);
        if (near) prefetch(k);
      }
      head.style.transform = 'translateX(' + (t / (N - 1) * track.clientWidth).toFixed(1) + 'px)';
    }
    if ('IntersectionObserver' in window) { var pio = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { near = true; prefetch(curK < 0 ? 0 : curK); pio.disconnect(); } }, { rootMargin: '600px 0px' }); pio.observe(pin); } else near = true;
    var mode = 'scroll', progY = null;
    var ts = new Spring({ from: 0, damping: 1, response: 0.22, eps: 0.0015, onUpdate: function (x) { render(x); if (mode === 'fly') { progY = scrollForT(x); window.scrollTo(0, progY); } }, onRest: function () { if (mode === 'fly') mode = 'scroll'; } });
    function onScroll() {
      if (mode === 'drag') return;
      if (mode === 'fly') { if (progY !== null && Math.abs(window.scrollY - progY) > 3) { mode = 'scroll'; } else return; }
      var t = tFromScroll();
      if (RM.on) { ts.set(t); return; }
      ts.to(t, { damping: 1, response: 0.22 });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    ['wheel', 'touchstart'].forEach(function (ev) { window.addEventListener(ev, function () { if (mode === 'fly') mode = 'scroll'; }, { passive: true }); });
    function flyTo(t, v) { mode = 'fly'; progY = null; ts.to(clamp(t, 0, N - 1), { velocity: v || 0, damping: 1, response: 0.42 }); }
    var vt = new VTrack(), drag = null;
    function tAt(e) { var r = track.getBoundingClientRect(); return clamp((e.clientX - r.left) / r.width * (N - 1), 0, N - 1); }
    ruler.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return;
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: false, moved: false, mark: e.target.closest('.rmark'), off: 0 };
      if (e.pointerType === 'mouse') startDrag(e);
    });
    function startDrag(e) {
      drag.on = true; mode = 'drag'; ruler.classList.add('drag'); try { ruler.setPointerCapture(drag.id); } catch (er) {}
      var t = tAt(e), hx = ts.x;
      drag.off = Math.abs(t - hx) < 0.35 ? hx - t : 0;
      vt.reset(); vt.add(t + drag.off); ts.set(t + drag.off); window.scrollTo(0, scrollForT(ts.x));
    }
    ruler.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.on) { var it = dragIntent(e, drag.sx, drag.sy); if (it === 1) startDrag(e); else if (it === -1) drag = null; return; }
      if (Math.abs(e.clientX - drag.sx) > 4) drag.moved = true;
      var t = clamp(tAt(e) + drag.off, 0, N - 1); vt.add(t); ts.set(t); window.scrollTo(0, scrollForT(t));
    });
    function endDrag(e, cancel) {
      if (!drag || e.pointerId !== drag.id) return;
      var d0 = drag; drag = null; ruler.classList.remove('drag');
      if (!d0.on) { if (d0.mark && !cancel) flyTo(parseInt(d0.mark.getAttribute('data-step'), 10), 0); return; }
      if (!d0.moved && d0.mark) { flyTo(parseInt(d0.mark.getAttribute('data-step'), 10), 0); return; }
      var v = vt.v(); flyTo(Math.round(clamp(ts.x + project(v, 0.995), 0, N - 1)), v);
    }
    ruler.addEventListener('pointerup', function (e) { endDrag(e, false); });
    ruler.addEventListener('pointercancel', function (e) { endDrag(e, true); if (mode === 'drag') mode = 'scroll'; });
    marks.forEach(function (m) { m.addEventListener('click', function (e) { if (e.detail === 0) flyTo(parseInt(m.getAttribute('data-step'), 10), 0); }); });
    ruler.addEventListener('keydown', function (e) {
      var k = Math.round(ts.target), t = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') t = Math.min(N - 1, k + 1);
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') t = Math.max(0, k - 1);
      else if (e.key === 'Home') t = 0; else if (e.key === 'End') t = N - 1; else return;
      e.preventDefault(); flyTo(t, 0);
    });
    var rz = 0;
    function relayout() { layout(); var t = mode === 'scroll' ? tFromScroll() : ts.x; ts.set(t); render(t); }
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(relayout, 120); });
    window.addEventListener('load', relayout);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
    layout(); ts.set(tFromScroll());
  })();

  /* ================= 01 颜色总线：五条泳道 × 1700–2026（按实际宽度现画；拖竖线、方向键、播放） ================= */
  (function initBus() {
    var B = D.bus, wrap = $('#buswrap'), svg = $('#bussvg'), read = $('#busread'); if (!B || !wrap || !svg) return;
    var Y0 = B.y0, Y1 = B.y1, BR = B.brk, BF = B.brkf;
    var W = 0, H = 0, PL = 0, PR = 8, laneH = 36, minorH = 10, gap = 14, top = 44, uid = 0;
    function fx(y) { return y <= BR ? (y - Y0) / (BR - Y0) * BF : BF + (y - BR) / (Y1 - BR) * (1 - BF); }
    function X(y) { return PL + fx(y) * (W - PL - PR); }
    function yAt(px) { var f = clamp((px - PL) / (W - PL - PR), 0, 1); return f <= BF ? Y0 + f / BF * (BR - Y0) : BR + (f - BF) / (1 - BF) * (Y1 - BR); }
    function rng(seed) { var s = seed >>> 0 || 1; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
    function lum(hex) { var n = parseInt(hex.slice(1), 16); return (0.299 * (n >> 16 & 255) + 0.587 * (n >> 8 & 255) + 0.114 * (n & 255)) / 255; }
    // 迷彩只画类型：林地斑块、笔刷、横纹、竖纹、数码像素、多地形
    function pattern(defs, s, seed) {
      var id = 'bp' + (++uid), c = s.c, t = s.t, PW = 48, PH = 24, r = rng(seed), p, i, k, x, y;
      if (t === 'hatch') { p = el('pattern', { id: id, patternUnits: 'userSpaceOnUse', width: 15, height: 15, patternTransform: 'rotate(45)' }, defs); el('rect', { width: 15, height: 15, fill: c[0] }, p); el('rect', { x: 7, width: 4, height: 15, fill: c[1] }, p); el('rect', { x: 11, width: 4, height: 15, fill: c[2] || c[1] }, p); return id; }
      if (t === 'unknown') { p = el('pattern', { id: id, patternUnits: 'userSpaceOnUse', width: 8, height: 8, patternTransform: 'rotate(45)' }, defs); el('line', { x1: 0, y1: 0, x2: 0, y2: 8, 'class': 'unk', 'stroke-width': 3, 'stroke-opacity': .5 }, p); return id; }
      p = el('pattern', { id: id, patternUnits: 'userSpaceOnUse', width: PW, height: PH }, defs); el('rect', { width: PW, height: PH, fill: c[0] }, p);
      var n = c.length - 1; if (n < 1) return id;
      if (t === 'woodland') for (i = 0; i < 14; i++) { k = c[1 + i % n]; x = r() * PW; y = r() * PH; el('ellipse', { cx: x.toFixed(1), cy: y.toFixed(1), rx: (4 + r() * 7).toFixed(1), ry: (2 + r() * 4).toFixed(1), transform: 'rotate(' + (r() * 60 - 30).toFixed(0) + ' ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')', fill: k }, p); }
      else if (t === 'brush') for (i = 0; i < 12; i++) { k = c[1 + i % n]; x = r() * PW; y = r() * PH; el('path', { d: 'M' + x.toFixed(1) + ' ' + y.toFixed(1) + 'q' + (5 + r() * 6).toFixed(1) + ' ' + (-3 - r() * 4).toFixed(1) + ' ' + (10 + r() * 8).toFixed(1) + ' ' + (-2 + r() * 4).toFixed(1), stroke: k, 'stroke-width': (2.2 + r() * 2.4).toFixed(1), 'stroke-linecap': 'round', fill: 'none' }, p); }
      else if (t === 'lizard') for (i = 0; i < 16; i++) { k = c[1 + i % n]; el('rect', { x: (r() * PW).toFixed(1), y: (r() * PH).toFixed(1), width: (5 + r() * 9).toFixed(1), height: 1.8, rx: .9, fill: k }, p); }
      else if (t === 'flora') for (i = 0; i < 7; i++) { k = c[1 + i % n]; x = i * 7 + r() * 3; el('path', { d: 'M' + x.toFixed(1) + ' 0q3 6 0 12t0 12', stroke: k, 'stroke-width': (2 + r() * 2).toFixed(1), fill: 'none' }, p); }
      else if (t === 'digital') for (i = 0; i < 64; i++) { k = c[1 + i % n]; el('rect', { x: Math.floor(r() * PW / 3) * 3, y: Math.floor(r() * PH / 3) * 3, width: 3 * (1 + Math.floor(r() * 3)), height: 3, fill: k }, p); }
      else if (t === 'multi') for (i = 0; i < 16; i++) { k = c[1 + i % n]; el('ellipse', { cx: (r() * PW).toFixed(1), cy: (r() * PH).toFixed(1), rx: (2 + r() * 5).toFixed(1), ry: (1.5 + r() * 3).toFixed(1), fill: k, 'fill-opacity': .75 }, p); }
      return id;
    }
    function fillFor(defs, s, seed) { return s.t === 'solid' ? s.c[0] : 'url(#' + pattern(defs, s, seed) + ')'; }
    function drawSeg(g, defs, s, x0, y, w, h, seed) {
      if (s.t === 'split') { el('rect', { x: x0, y: y, width: w, height: h / 2, fill: s.c[0] }, g); el('rect', { x: x0, y: y + h / 2, width: w, height: h / 2, fill: s.c[1] }, g); return el('rect', { x: x0, y: y, width: w, height: h, fill: 'none', 'class': 'seg' }, g); }
      return el('rect', { x: x0, y: y, width: w, height: h, fill: fillFor(defs, s, seed), 'class': 'seg' }, g);
    }
    var tickEls = []; var curG = null, curLine = null, curLab = null, curLabBg = null, curDots = [], stageEls = [], laneY = [];
    function draw() {
      W = wrap.clientWidth; if (!W) return;
      var narrow = W < 640; PL = narrow ? 28 : 64; laneH = narrow ? 30 : 36; gap = narrow ? 12 : 16;
      svg.innerHTML = ''; uid = 0; tickEls = []; stageEls = []; laneY = []; curDots = [];
      var defs = el('defs', {}, svg), y = top, i;
      // 阶段标带
      var gs = el('g', {}, svg);
      B.stages.forEach(function (st) {
        var x0 = X(st.a), x1 = X(st.b), g = el('g', { 'class': 'stg' }, gs);
        el('rect', { x: x0 + 1, y: 8, width: Math.max(0, x1 - x0 - 2), height: 24, rx: 4 }, g);
        var t = el('text', { x: (x0 + x1) / 2, y: 25, 'text-anchor': 'middle' }, g); t.textContent = st.name;
        if (t.getComputedTextLength && t.getComputedTextLength() > x1 - x0 - 6) t.textContent = st.name.split(' ')[0].slice(0, x1 - x0 > 28 ? 2 : 1);
        stageEls.push(g);
      });
      // 泳道
      B.lanes.forEach(function (ln, li) {
        var g = el('g', {}, svg), hasMinor = ln.segs.some(function (s) { return s.minor; });
        laneY.push(y);
        var nm = el('text', { x: 0, y: y + laneH / 2 + 5, 'class': 'lname' }, g); nm.textContent = narrow ? ln.short : ln.name;
        var first = Math.min.apply(null, ln.segs.filter(function (s) { return !s.minor; }).map(function (s) { return s.a; }));
        if (first > Y0) { el('rect', { x: X(Y0), y: y + .5, width: X(first) - X(Y0), height: laneH - 1, 'class': 'none' }, g); if (!narrow) { var et = el('text', { x: X(Y0) + 8, y: y + laneH / 2 + 4 }, g); et.textContent = B.empty; } }
        ln.segs.forEach(function (s, si) {
          var x0 = X(s.a), w = X(s.b) - x0, yy = s.minor ? y + laneH + 2 : y, hh = s.minor ? minorH : laneH;
          drawSeg(g, defs, s, x0, yy, w, hh, (s.a * 7 + s.b + li * 131) % 997);
          if (!s.minor && !narrow) {
            var t = el('text', { x: x0 + 8, y: yy + hh / 2 + 4, 'class': 'slab ' + (lum(s.c[0]) < .5 || s.t === 'unknown' ? 'dk' : 'lt') }, g); t.textContent = s.label;
            if (t.getComputedTextLength() > w - 14) g.removeChild(t);
          }
        });
        B.marks.forEach(function (m) {
          if (m.cc !== ln.cc) return;
          var c = el('circle', { cx: X(Math.max(m.y, Y0 + 3)).toFixed(1), cy: y + 1, r: narrow ? 4 : 5, 'class': 'mk', tabindex: 0, role: 'link', 'data-id': m.id }, g);
          var tt = el('title', {}, c); tt.textContent = m.y + ' · ' + m.t;
        });
        curDots.push(null);
        y += laneH + (hasMinor ? minorH + 2 : 0) + gap;
      });
      // 时间轴
      var ay = y + 2; el('line', { x1: X(Y0), y1: ay, x2: X(Y1), y2: ay, 'class': 'axl' }, svg);
      var ticks = narrow ? [1700, 1800, 1900, 1950, 2000] : [1700, 1750, 1800, 1850, 1900, 1920, 1940, 1960, 1980, 2000, 2020];
      ticks.forEach(function (ty) { var x = X(ty); el('line', { x1: x, y1: top - 6, x2: x, y2: ay, 'class': 'axg' }, svg); el('line', { x1: x, y1: ay, x2: x, y2: ay + 5, 'class': 'axl' }, svg); var t = el('text', { x: x, y: ay + 20, 'text-anchor': ty === 1700 ? 'start' : 'middle' }, svg); t.textContent = ty; tickEls.push([x, t]); });
      el('line', { x1: X(BR), y1: top - 8, x2: X(BR), y2: ay + 5, 'class': 'brk' }, svg);
      H = ay + 28; svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('height', H);
      // 游标
      curG = el('g', { 'class': 'cur' }, svg);
      curLine = el('line', { x1: 0, y1: 2, x2: 0, y2: ay }, curG);
      B.lanes.forEach(function (ln, li) { curDots[li] = el('circle', { cx: 0, cy: laneY[li] + laneH / 2, r: 0 }, curG); });
      curLabBg = el('rect', { x: -22, y: ay + 6, width: 44, height: 20, rx: 10 }, curG);
      curLab = el('text', { x: 0, y: ay + 20, 'text-anchor': 'middle' }, curG);
      place(sp.x);
    }
    // 读数
    var yrEl = $('#busy'), stEl = $('#busst'), lastKey = [], shownY = null, chips = $$('#buschips button[data-y]');
    function segAt(ln, y, minor) { var yy = Math.min(y, Y1 - 0.01); for (var i = 0; i < ln.segs.length; i++) { var s = ln.segs[i]; if (!!s.minor === minor && yy >= s.a && yy < s.b) return s; } return null; }
    var sdefs = null;
    function readout(y) {
      if (y === shownY) return; shownY = y;
      yrEl.textContent = y; wrap.setAttribute('aria-valuenow', y);
      var yy = Math.min(y, Y1 - 0.01), st = B.stages.filter(function (s) { return yy >= s.a && yy < s.b; })[0];
      stEl.innerHTML = st ? '<em>' + esc(st.name) + '</em>' + esc(st.note) : '';
      stageEls.forEach(function (g, i) { g.classList.toggle('on', B.stages[i] === st); });
      chips.forEach(function (c) { c.classList.toggle('on', +c.getAttribute('data-y') === y); });
      B.lanes.forEach(function (ln, li) {
        var s = segAt(ln, y, false), m = segAt(ln, y, true), key = (s ? s.a : 'x') + '|' + (m ? m.a : '');
        if (key === lastKey[li]) return;
        var li_ = read.children[li], first = lastKey[li] === undefined; lastKey[li] = key;
        var sw = li_.querySelector('svg'); sw.innerHTML = '';
        if (s) { var d = el('defs', {}, sw); uid += 1000; drawSeg(sw, d, s, 0, 0, 400, 32, (s.a * 7 + s.b + li * 131) % 997); uid -= 1000; uid++; }
        else el('rect', { x: 1, y: 1, width: 398, height: 30, fill: 'none', stroke: 'currentColor', 'stroke-opacity': .3, 'stroke-dasharray': '3 4' }, sw);
        li_.querySelector('.bn small').textContent = s ? s.a + '–' + (s.b >= Y1 ? '今' : s.b) : '';
        li_.querySelector('.bl').innerHTML = (s ? esc(s.label) : esc(B.empty)) + (m ? '<span class="bm">另有：' + esc(m.label) + '</span>' : '');
        if (!first) { li_.classList.remove('chg'); void li_.offsetWidth; li_.classList.add('chg'); }
      });
    }
    read.innerHTML = B.lanes.map(function (ln) { return '<li><span class="bn">' + esc(ln.name) + '<small></small></span><svg viewBox="0 0 400 32" preserveAspectRatio="none" aria-hidden="true"></svg><span class="bl"></span></li>'; }).join('');
    function place(y) {
      if (!curG) return;
      var x = X(y); curG.setAttribute('transform', 'translate(' + x.toFixed(1) + ' 0)');
      var yr = Math.round(y); curLab.textContent = yr;
      tickEls.forEach(function (te) { te[1].style.opacity = Math.abs(te[0] - x) < 40 ? 0 : 1; });
      B.lanes.forEach(function (ln, li) { curDots[li].setAttribute('r', segAt(ln, yr, false) ? 3.5 : 0); });
      readout(yr);
    }
    var sp = new Spring({ from: 1914, damping: 1, response: 0.3, eps: 0.05, onUpdate: function (x) { place(x); } });
    // 播放：1700 → 2026，约 14 秒，按屏幕上的位置匀速走
    var playBtn = $('#busplay'), playing = false, praf = 0;
    function stopPlay() { playing = false; cancelAnimationFrame(praf); playBtn.setAttribute('aria-pressed', 'false'); playBtn.textContent = '从头放一遍'; }
    function play() {
      if (RM.on) { sp.set(Y1); return; }
      playing = true; playBtn.setAttribute('aria-pressed', 'true'); playBtn.textContent = '停';
      var t0 = performance.now(), dur = 14000;
      (function step(now) { if (!playing) return; var f = clamp((now - t0) / dur, 0, 1); sp.set(yAt(PL + f * (W - PL - PR))); if (f < 1) praf = requestAnimationFrame(step); else stopPlay(); })(t0);
    }
    playBtn.addEventListener('click', function () { if (playing) stopPlay(); else play(); });
    $('#buschips').addEventListener('click', function (e) { var b = e.target.closest('button[data-y]'); if (!b) return; stopPlay(); sp.to(+b.getAttribute('data-y')); });
    // 拖动
    var drag = null;
    function yFromEvent(e) { var r = svg.getBoundingClientRect(); return yAt(e.clientX - r.left); }
    wrap.addEventListener('pointerdown', function (e) {
      if (e.button > 0 || e.target.closest('.mk')) return;
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: false };
      if (e.pointerType === 'mouse') { drag.on = true; stopPlay(); try { wrap.setPointerCapture(e.pointerId); } catch (er) {} sp.to(yFromEvent(e), { response: 0.18 }); }
    });
    wrap.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.on) { var it = dragIntent(e, drag.sx, drag.sy); if (it === 1) { drag.on = true; stopPlay(); try { wrap.setPointerCapture(e.pointerId); } catch (er) {} } else if (it === -1) { drag = null; return; } else return; }
      sp.set(yFromEvent(e));
    });
    function end(e) { if (!drag || e.pointerId !== drag.id) return; var d0 = drag; drag = null; if (!d0.on && e.type === 'pointerup') { stopPlay(); sp.to(yFromEvent(e)); return; } if (d0.on) sp.to(Math.round(sp.x), { response: 0.2 }); }
    wrap.addEventListener('pointerup', end); wrap.addEventListener('pointercancel', end);
    wrap.addEventListener('keydown', function (e) {
      if (e.target.closest && e.target.closest('.mk')) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openRow(e.target.getAttribute('data-id')); } return; }
      var y = Math.round(sp.target), d = e.shiftKey ? 10 : 1;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') y += d; else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') y -= d; else if (e.key === 'Home') y = Y0; else if (e.key === 'End') y = Y1; else return;
      e.preventDefault(); stopPlay(); sp.to(clamp(y, Y0, Y1), { response: 0.2 });
    });
    svg.addEventListener('click', function (e) { var m = e.target.closest('.mk'); if (m) openRow(m.getAttribute('data-id')); });
    var rz = 0; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(draw, 120); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
    draw(); sp.set(1914);
  })();

  /* ================= 列表：透镜分组（FLIP 补间）+ 行内展开 ================= */
  (function initLists() {
    function toggle(r, open) { var o = open == null ? !r.classList.contains('open') : open; r.classList.toggle('open', o); var b = $('.lhead', r); if (b) b.setAttribute('aria-expanded', String(o)); }
    document.addEventListener('click', function (e) { var b = e.target.closest('.lhead'); if (!b) return; toggle(b.closest('.lrow')); });
    function scrollToRow(r) {
      var w = r.closest('.lwrap'), lb = w ? $('.lensbar', w) : null, off = navH() + (lb ? lb.offsetHeight : 0) + 8, top = r.getBoundingClientRect().top + window.scrollY - off;
      window.scrollTo({ top: Math.max(0, top), behavior: RM.on ? 'auto' : 'smooth' });
    }
    $$('.lwrap[data-lw]').forEach(function (w) {
      var key = w.getAttribute('data-lw'), groups = (D.lens || {})[key], lensEl = $('.lens', w), grid = $('.lgrid', w), note = $('.lensnote', w);
      if (!groups || !lensEl || !grid) return;
      var rows = {}; $$('.lrow', grid).forEach(function (r) { rows[r.getAttribute('data-id')] = r; });
      var tabs = $$('button[data-lens]', lensEl), total = Object.keys(rows).length;
      var cur = (tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0]).getAttribute('data-lens');
      var pill = document.createElement('span'); pill.className = 'pill'; lensEl.insertBefore(pill, lensEl.firstChild);
      var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
      var pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
      function movePill(instant) { var b = tabs.filter(function (t) { return t.getAttribute('data-lens') === cur; })[0]; if (!b) return; var x = b.offsetLeft, wd = b.offsetWidth; if (instant) { px.set(x); pw.set(wd); } else { px.to(x); pw.to(wd); } }
      function header(g) { var h = document.createElement('div'); h.className = 'lgh'; h.setAttribute('data-g', g.k); h.innerHTML = '<b>' + esc(g.label) + '</b><small>' + g.ids.length + ' 行</small>'; return h; }
      function setLens(lens, instant) {
        if (!groups[lens]) return; cur = lens;
        tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-lens') === lens)); });
        movePill(instant);
        var first = {}; Object.keys(rows).forEach(function (id) { first[id] = rows[id].getBoundingClientRect().top; });
        var frag = document.createDocumentFragment();
        groups[lens].forEach(function (g) { frag.appendChild(header(g)); g.ids.forEach(function (id) { if (rows[id]) frag.appendChild(rows[id]); }); });
        $$('.lgh', grid).forEach(function (h) { h.remove(); });
        grid.appendChild(frag);
        if (note) note.textContent = '按' + D.lensName[key][lens] + '分成 ' + groups[lens].length + ' 组 · ' + total + ' 行 · 点一行展开';
        if (instant || RM.on) return;
        Object.keys(rows).forEach(function (id) {
          var r = rows[id], dy = first[id] - r.getBoundingClientRect().top; if (Math.abs(dy) < 1) return;
          r.style.transition = 'none'; r.style.transform = 'translateY(' + dy.toFixed(1) + 'px)';
        });
        grid.offsetHeight;
        Object.keys(rows).forEach(function (id) { var r = rows[id]; if (!r.style.transform) return; r.style.transition = 'transform .5s cubic-bezier(.22,1,.36,1)'; r.style.transform = ''; });
        $$('.lgh', grid).forEach(function (h) { if (h.animate) h.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'cubic-bezier(.22,1,.36,1)' }); });
      }
      lensEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-lens]'); if (b) setLens(b.getAttribute('data-lens')); });
      lensEl.addEventListener('keydown', function (e) { if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return; var i = tabs.findIndex(function (t) { return t.getAttribute('data-lens') === cur; }), n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); setLens(n.getAttribute('data-lens')); e.preventDefault(); });
      setLens(cur, true);
      window.addEventListener('resize', function () { movePill(true); });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); });
      LISTS[key] = {
        has: function (id) { return !!rows[id]; }, setLens: setLens,
        open: function (id) { var r = rows[id]; if (!r) return; toggle(r, true); setTimeout(function () { scrollToRow(r); r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1600); }, 30); }
      };
    });
    document.addEventListener('click', function (e) { var a = e.target.closest('a[data-open]'); if (!a) return; if (openRow(a.getAttribute('data-open'))) e.preventDefault(); });
    var m = /^#((?:u|why)-[\w-]+)$/.exec(location.hash || '');
    if (m) setTimeout(function () { openRow(m[1]); }, 80);
  })();

  /* ================= 大图 ================= */
  (function initLightbox() {
    var lb = $('#lb'), img = $('#lbimg'), cap = $('#lbcap'); if (!lb || !lb.showModal) return;
    document.addEventListener('click', function (e) {
      var z = e.target.closest('.zoom'); if (!z) return;
      var fc = z.parentNode.querySelector('figcaption'); img.src = z.getAttribute('data-full'); img.alt = (z.querySelector('img') || {}).alt || ''; cap.textContent = fc ? fc.textContent : '';
      lb.showModal();
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.closest('#lbx') || e.target === img) lb.close(); });
  })();
})();
