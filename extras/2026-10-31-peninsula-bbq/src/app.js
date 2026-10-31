/* 号外 · 半岛的烤肉 — app.js（每个模块一层 IIFE，局部变量不串；见第 7 题经验 ㊱） */
(function () {
  'use strict';
  var root = document.documentElement, D = window.PB || {};
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var RM = false; try { RM = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  function lang() { return root.lang === 'en' ? 'en' : 'zh'; }
  function L(o) { if (o == null) return ''; if (typeof o === 'string') return o; return o[lang()] || o.zh || o.en || ''; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fmt(n, d) { return Number(n).toLocaleString(lang() === 'en' ? 'en-US' : 'zh-CN', { maximumFractionDigits: d == null ? 0 : d, minimumFractionDigits: d == null ? 0 : d }); }
  window.PBX = { L: L, lang: lang, esc: esc, clamp: clamp, fmt: fmt, RM: RM };

  /* 弹簧（阻尼比 1，response 秒） */
  function Spring(o) { this.x = o.x || 0; this.v = 0; this.target = this.x; this.resp = o.response || 0.38; this.cb = o.onUpdate; this.raf = 0; this.last = 0; }
  Spring.prototype.to = function (t) { var s = this; s.target = t; if (RM) { s.x = t; s.v = 0; s.cb(s.x); return; } if (s.raf) return; s.last = performance.now(); s.raf = requestAnimationFrame(function step(now) { var dt = Math.min(0.032, (now - s.last) / 1000); s.last = now; var w = 2 * Math.PI / s.resp, a = -w * w * (s.x - s.target) - 2 * w * s.v; s.v += a * dt; s.x += s.v * dt; if (Math.abs(s.x - s.target) < 0.0005 && Math.abs(s.v) < 0.002) { s.x = s.target; s.v = 0; s.cb(s.x); s.raf = 0; return; } s.cb(s.x); s.raf = requestAnimationFrame(step); }); };
  Spring.prototype.set = function (x) { if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0; this.x = this.target = x; this.v = 0; this.cb(x); };
  window.PBX.Spring = Spring;

  /* ---------- 语言与深浅色 ---------- */
  (function () {
    var lb = $('#langbtn'), tb = $('#themebtn');
    function lbl() { if (lb) { lb.textContent = lang() === 'en' ? '中文' : 'EN'; lb.setAttribute('aria-label', lang() === 'en' ? '切换到中文' : 'Switch to English'); } }
    lbl();
    if (lb) lb.addEventListener('click', function () { root.lang = lang() === 'en' ? 'zh-CN' : 'en'; try { localStorage.setItem('pbbq-lang', root.lang); } catch (e) {} lbl(); document.title = lang() === 'en' ? (D.meta && D.meta.title_en) + ' | Tianjie · Extra' : (D.meta && D.meta.title_zh) + '｜一周一题 · 号外'; window.dispatchEvent(new Event('langchange')); });
    if (lang() === 'en' && D.meta) document.title = D.meta.title_en + ' | Tianjie · Extra';
    function cur() { return root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); }
    function tl() { if (tb) tb.textContent = cur() === 'dark' ? '☀' : '☾'; if (tb) tb.setAttribute('aria-label', cur() === 'dark' ? 'Light' : 'Dark'); }
    tl(); if (tb) tb.addEventListener('click', function () { root.setAttribute('data-theme', cur() === 'dark' ? 'light' : 'dark'); try { localStorage.setItem('yzyt-theme', root.getAttribute('data-theme')); } catch (e) {} tl(); window.dispatchEvent(new Event('themechange')); });
  })();

  /* ---------- 入场 ---------- */
  (function () {
    var els = $$('.fade');
    if ('IntersectionObserver' in window && !RM) { var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' }); els.forEach(function (el) { io.observe(el); }); }
    else els.forEach(function (el) { el.classList.add('in'); });
    var rs = $$('.hero .rise'); requestAnimationFrame(function () { rs.forEach(function (el, i) { el.style.transitionDelay = (0.15 + i * 0.1) + 's'; el.classList.add('in'); }); });
  })();

  /* ---------- 论点逐词上火 ---------- */
  (function () {
    var box = $('.thesis'); if (!box) return; var t = false;
    function upd() { t = false; $$('.thesis .lines').forEach(function (ln) { if (ln.offsetParent === null) return; var ws = $$('.w', ln); var r = ln.getBoundingClientRect(), vh = innerHeight; var p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1); if (RM) p = 1; var n = Math.round(p * ws.length * 1.15); ws.forEach(function (w, i) { w.classList.toggle('on', i < n); }); }); }
    addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(upd); } }, { passive: true }); addEventListener('langchange', upd); upd();
  })();

  /* ---------- 章节导航 ---------- */
  (function () {
    var nav = $('#cnav'), prog = $('#prog'), links = $$('#cnav [data-nav]'); if (!nav) return;
    var secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-nav')); });
    function setH() { root.style.setProperty('--nav-h', nav.offsetHeight + 'px'); }
    var t = false;
    function upd() { t = false; var y = scrollY + nav.offsetHeight + 40, cur = -1; secs.forEach(function (s, i) { if (s && s.offsetTop <= y) cur = i; }); links.forEach(function (a, i) { var on = i === cur; if (on !== a.classList.contains('on')) { a.classList.toggle('on', on); if (on) { var c = a.parentNode, r = a.getBoundingClientRect(), rr = c.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) c.scrollLeft += r.left - rr.left - 16; } } }); var h = document.documentElement.scrollHeight - innerHeight; if (prog) prog.style.width = (h > 0 ? scrollY / h * 100 : 0) + '%'; }
    setH(); upd(); addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(upd); } }, { passive: true }); addEventListener('resize', function () { setH(); upd(); });
  })();

  /* ---------- 00 FIRE 舞台 ---------- */
  (function () {
    var st = $('#stage'); if (!st || !D.stage) return;
    var all = D.stage, laneSel = 'south', steps = [], idx = -1;
    var card = $('.card', st), ruler = $('.ruler', st), head = $('.hd', ruler), ph = $('.ph', st), cap = $('.cap', st);
    var imgs = {};
    all.forEach(function (s) { if (s.img && !imgs[s.img]) { var im = new Image(); im.alt = ''; im.decoding = 'async'; im.loading = 'lazy'; im.src = s.img; ph.appendChild(im); imgs[s.img] = im; } });
    function pick() { steps = all.filter(function (s) { return s.lane === 'both' || s.lane === laneSel; }); st.style.setProperty('--steps', steps.length); }
    function ticks() { ruler.innerHTML = '<div class="hd"></div>'; head = $('.hd', ruler); steps.forEach(function (s, i) { var b = document.createElement('div'); b.className = 'tk'; b.style.left = pos(i) + '%'; b.textContent = s.label; b.addEventListener('click', function () { go(i); }); ruler.appendChild(b); }); }
    function pos(i) { var pad = innerWidth < 700 ? 8 : 5; return steps.length < 2 ? 50 : pad + (100 - 2 * pad) * i / (steps.length - 1); }
    var sp = new Spring({ x: 0, response: 0.38, onUpdate: function (x) { var n = steps.length - 1, i = Math.floor(x), f = x - i, a = pos(clamp(i, 0, n)), b = pos(clamp(i + 1, 0, n)); head.style.left = (a + (b - a) * f) + '%'; } });
    function show(i, force) {
      i = clamp(i, 0, steps.length - 1); if (i === idx && !force) return; idx = i; var s = steps[i];
      $$('.tk', ruler).forEach(function (t, k) { t.classList.toggle('on', k === i); });
      for (var k in imgs) imgs[k].classList.toggle('on', k === s.img);
      card.classList.add('out');
      setTimeout(function () {
        card.innerHTML = '<div class="mv"><div class="yr">' + esc(L(s.yr || s.label)) + '</div><div class="era">' + esc(L(s.era)) + '</div><h3>' + esc(L(s.title)) + '</h3><p>' + L(s.text) + '</p>' +
          (s.dishes && s.dishes.length ? '<div class="dish">' + s.dishes.map(function (d) { return '<span>' + esc(L(d)) + (d.ko ? '<i>' + esc(d.ko) + '</i>' : '') + '</span>'; }).join('') + '</div>' : '') + '</div>';
        card.classList.remove('out');
        cap.innerHTML = s.cap ? L(s.cap) : '';
      }, RM || force ? 0 : 160);
      sp.to(i);
    }
    function frac() { var r = st.getBoundingClientRect(), tot = st.offsetHeight - (innerHeight - nav()); return clamp(-r.top / Math.max(1, tot), 0, 1); }
    function nav() { var n = $('#cnav'); return n ? n.offsetHeight : 0; }
    function go(i) { var tot = st.offsetHeight - (innerHeight - nav()); var y = st.offsetTop - nav() + tot * (i + 0.5) / steps.length; scrollTo({ top: y, behavior: RM ? 'auto' : 'smooth' }); }
    var dragging = false;
    function onScroll() { if (dragging) return; var f = frac(); show(Math.min(steps.length - 1, Math.floor(f * steps.length))); }
    var tk = false; addEventListener('scroll', function () { if (!tk) { tk = true; requestAnimationFrame(function () { tk = false; onScroll(); }); } }, { passive: true });
    /* 拖刻度尺 */
    var sx = 0, moved = false;
    function xToI(cx) { var r = ruler.getBoundingClientRect(), p = (cx - r.left) / r.width * 100, best = 0, bd = 1e9; steps.forEach(function (s, i) { var d = Math.abs(pos(i) - p); if (d < bd) { bd = d; best = i; } }); return best; }
    ruler.addEventListener('pointerdown', function (e) { if (e.target.classList.contains('tk')) return; dragging = true; moved = false; sx = e.clientX; ruler.setPointerCapture(e.pointerId); });
    ruler.addEventListener('pointermove', function (e) { if (!dragging) return; if (Math.abs(e.clientX - sx) > 6) moved = true; if (moved) show(xToI(e.clientX)); });
    function up(e) { if (!dragging) return; dragging = false; var i = xToI(e.clientX); go(i); }
    ruler.addEventListener('pointerup', up); ruler.addEventListener('pointercancel', function () { dragging = false; });
    ruler.tabIndex = 0; ruler.setAttribute('role', 'slider'); ruler.setAttribute('aria-label', 'Timeline');
    ruler.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); } });
    /* 南 / 北 */
    $$('.lane .pill', st).forEach(function (b) { b.addEventListener('click', function () { if (b.getAttribute('data-lane') === laneSel) return; var curS = steps[idx]; laneSel = b.getAttribute('data-lane'); $$('.lane .pill', st).forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); }); pick(); ticks(); var ni = 0; steps.forEach(function (s, i) { if (s.y <= (curS ? curS.y : 0)) ni = i; }); idx = -1; sp.set(ni); show(ni, true); go(ni); }); });
    addEventListener('langchange', function () { show(idx, true); });
    addEventListener('resize', function () { ticks(); var k = idx; idx = -1; show(k, true); sp.set(k); });
    pick(); ticks(); show(0, true); onScroll();
  })();

  /* ---------- 01 CUT：部位图 ---------- */
  (function () {
    var map = $('#cutmap'), panel = $('#cutpanel'); if (!map || !D.cuts) return;
    var cur = null, sub = -1;
    function render() {
      map.innerHTML = '<span class="axis" style="left:8px;top:-20px">← ' + esc(L({ zh: '头', en: 'Head' })) + '</span><span class="axis" style="right:8px;top:-20px">' + esc(L({ zh: '尾', en: 'Tail' })) + ' →</span>' +
        D.cuts.map(function (c, i) { return '<button class="pr' + (cur === c.id ? ' on' : '') + '" data-id="' + c.id + '" style="grid-area:' + c.area + '"><i>' + (i + 1 < 10 ? '0' : '') + (i + 1) + '</i><b>' + esc(L(c)) + '</b><span>' + esc(c.ko) + (lang() === 'zh' ? ' · ' + esc(c.en) : '') + '</span></button>'; }).join('');
      $$('.pr', map).forEach(function (b) { b.addEventListener('click', function () { cur = b.getAttribute('data-id'); sub = -1; render(); }); });
      var c = D.cuts.filter(function (x) { return x.id === cur; })[0] || D.cuts[0]; if (!cur) { cur = c.id; $$('.pr', map)[0].classList.add('on'); }
      var s = sub >= 0 ? c.subs[sub] : null;
      panel.innerHTML = (c.img ? '<div class="im"><img src="' + c.img + '" alt="" loading="lazy"></div>' + (c.cap ? '<div class="cap2">' + L(c.cap) + '</div>' : '') : '') +
        '<div class="bd"><span class="sticker red pop">' + esc(L({ zh: '大分割', en: 'Primal' })) + ' ' + (D.cuts.indexOf(c) + 1) + ' / ' + D.cuts.length + '</span><h4 style="margin-top:12px">' + esc(L(c)) + '</h4><div class="ko">' + esc(c.ko) + ' · ' + esc(c.en) + '</div>' +
        (c.subs && c.subs.length ? '<div class="small">' + esc(L({ zh: '小分割（点一个看说明）', en: 'Sub-primals (tap one)' })) + '</div><div class="subs">' + c.subs.map(function (x, i) { return '<button data-i="' + i + '" class="' + (i === sub ? 'on' : '') + '">' + esc(L(x)) + '</button>'; }).join('') + '</div>' : '') +
        (s ? '<p style="margin:0 0 8px"><b>' + esc(L(s)) + '</b> <span class="small">' + esc(s.ko) + ' · ' + esc(s.en) + '</span><br>' + esc(L(s.note || '')) + '</p>' : '') +
        '<dl><dt>' + esc(L({ zh: '口感', en: 'Texture' })) + '</dt><dd>' + esc(L(c.texture)) + '</dd><dt>' + esc(L({ zh: '吃法', en: 'Best as' })) + '</dt><dd>' + esc(L(c.how)) + '</dd>' + (c.price ? '<dt>' + esc(L({ zh: '价位', en: 'Price' })) + '</dt><dd>' + esc(L(c.price)) + '</dd>' : '') + '</dl></div>';
      $$('.subs button', panel).forEach(function (b) { b.addEventListener('click', function () { sub = +b.getAttribute('data-i'); render(); }); });
    }
    render(); addEventListener('langchange', render);
  })();

  /* ---------- 01 CUT：烤一块（计时器） ---------- */
  (function () {
    var g = $('#grill'); if (!g || !D.grill) return;
    var cuts = D.grill, cur = cuts[0], t0 = 0, raf = 0, side = 1, running = false;
    var bx = $('.gcuts', g), clock = $('.clock b', g), unit = $('.clock span', g), bar = $('.bar i', g), say = $('.say', g), img = $('.gp img', g), note = $('.note', g), bStart = $('[data-act=go]', g), bReset = $('[data-act=reset]', g), gcap = $('.gpcap', g);
    function chips() { bx.innerHTML = cuts.map(function (c) { return '<button class="pill' + (c === cur ? ' on' : '') + '" data-id="' + c.id + '">' + esc(L(c)) + '</button>'; }).join(''); $$('.pill', bx).forEach(function (b) { b.addEventListener('click', function () { cur = cuts.filter(function (c) { return c.id === b.getAttribute('data-id'); })[0]; reset(); chips(); }); }); }
    function total() { return cur.sides.reduce(function (a, b) { return a + b; }, 0) + (cur.rest || 0); }
    function idle() { clock.textContent = total(); unit.textContent = L({ zh: '秒 · ' + cur.sides.length + ' 面' + (cur.rest ? ' + 静置' : ''), en: 'sec · ' + cur.sides.length + ' side' + (cur.sides.length > 1 ? 's' : '') + (cur.rest ? ' + rest' : '') }); say.innerHTML = L(cur.tip); note.innerHTML = L(cur.note); if (cur.img) { img.src = cur.img; } if (gcap) gcap.innerHTML = cur.cap ? L(cur.cap) : ''; img.style.filter = ''; bar.style.width = '0'; bStart.textContent = L({ zh: '上烤盘', en: 'On the grill' }); }
    function reset() { cancelAnimationFrame(raf); running = false; g.classList.remove('run'); idle(); }
    function stepper(now) {
      var el = (now - t0) / 1000, tot = total(), acc = 0, k = 0, msg = '';
      while (k < cur.sides.length && el > acc + cur.sides[k]) { acc += cur.sides[k]; k++; }
      if (k !== side - 1 && k < cur.sides.length) { side = k + 1; g.classList.remove('flip'); void g.offsetWidth; g.classList.add('flip'); }
      if (k < cur.sides.length) { var left = Math.ceil(acc + cur.sides[k] - el); clock.textContent = left; unit.textContent = L({ zh: '秒 · 第 ' + (k + 1) + ' 面', en: 'sec · side ' + (k + 1) }); msg = k === 0 ? L(cur.s1 || { zh: '滋——别动它。', en: 'Sizzle. Don’t touch it.' }) : L(cur.s2 || { zh: '<b>翻面！</b>', en: '<b>Flip!</b>' }); }
      else if (el < tot) { clock.textContent = Math.ceil(tot - el); unit.textContent = L({ zh: '秒 · 静置', en: 'sec · rest' }); msg = L({ zh: '离火，静置一会儿，让肉汁回流。', en: 'Off the heat. Let the juices settle.' }); }
      else { clock.textContent = '✓'; unit.textContent = L({ zh: '可以吃了', en: 'Eat' }); msg = L(cur.done); running = false; g.classList.remove('run'); bStart.textContent = L({ zh: '再来一块', en: 'Another' }); }
      say.innerHTML = msg; var p = clamp(el / tot, 0, 1); bar.style.width = (p * 100) + '%'; img.style.filter = 'saturate(' + (1 + p * 0.35) + ') brightness(' + (1 - p * 0.12) + ') contrast(' + (1 + p * 0.12) + ')';
      if (running) raf = requestAnimationFrame(stepper);
    }
    bStart.addEventListener('click', function () { if (running) return; side = 1; running = true; g.classList.add('run'); t0 = performance.now(); bStart.textContent = L({ zh: '烤着呢…', en: 'Grilling…' }); raf = requestAnimationFrame(stepper); });
    bReset.addEventListener('click', reset);
    addEventListener('langchange', function () { chips(); if (!running) idle(); });
    chips(); idle();
  })();

  /* ---------- 主图：进口量与自给率 ---------- */
  (function () {
    var box = $('#chart1'); if (!box || !D.series) return;
    var S = D.series, svgW = 0, yr = S.focus || S.years[S.years.length - 1];
    var rd = $('.rd', box), ev = $('.ev', box), wrap = $('.cv', box);
    function draw() {
      var W = wrap.clientWidth, H = W < 560 ? 300 : 360, m = { l: 44, r: 44, t: 16, b: 28 }; svgW = W;
      var ys = S.years, x0 = ys[0], x1 = ys[ys.length - 1];
      var X = function (y) { return m.l + (W - m.l - m.r) * (y - x0) / (x1 - x0); };
      var maxI = S.imax || Math.max.apply(null, S.imports.filter(function (v) { return v != null; })) * 1.1;
      var Yi = function (v) { return m.t + (H - m.t - m.b) * (1 - v / maxI); }, Ys = function (p) { return m.t + (H - m.t - m.b) * (1 - p / 100); };
      var p1 = '', p2 = '', a1 = '';
      ys.forEach(function (y, i) { var v = S.imports[i]; if (v != null) { p1 += (p1 ? 'L' : 'M') + X(y).toFixed(1) + ',' + Yi(v).toFixed(1); } var s = S.selfsuff[i]; if (s != null) p2 += (p2 ? 'L' : 'M') + X(y).toFixed(1) + ',' + Ys(s).toFixed(1); });
      a1 = p1 + 'L' + X(x1) + ',' + Yi(0) + 'L' + X(x0) + ',' + Yi(0) + 'Z';
      var g = '';
      for (var t = 0; t <= 100; t += 25) g += '<line class="ax" x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Ys(t) + '" y2="' + Ys(t) + '"/><text x="' + (W - m.r + 6) + '" y="' + (Ys(t) + 4) + '">' + t + '%</text>';
      var step = maxI > 400 ? 200 : 100;
      for (var v = 0; v <= maxI; v += step) g += '<text x="' + (m.l - 6) + '" y="' + (Yi(v) + 4) + '" text-anchor="end">' + v + '</text>';
      var dec = W < 560 ? 10 : 5;
      for (var y = Math.ceil(x0 / dec) * dec; y <= x1; y += dec) g += '<text x="' + X(y) + '" y="' + (H - 8) + '" text-anchor="middle">' + y + '</text>';
      var mk = (S.events || []).map(function (e, i) { return '<g class="mk" data-i="' + i + '"><circle cx="' + X(e.year) + '" cy="' + (m.t + 4) + '" r="7"/><text x="' + X(e.year) + '" y="' + (m.t + 8) + '" text-anchor="middle" style="font-size:9px;pointer-events:none">' + (i + 1) + '</text></g>'; }).join('');
      wrap.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '" role="img" aria-label="' + esc(L(S.title)) + '">' + g + '<path class="a1" d="' + a1 + '"/><path class="l1" d="' + p1 + '"/><path class="l2" d="' + p2 + '"/>' + mk + '<line class="cur" y1="' + m.t + '" y2="' + (H - m.b) + '"/></svg>';
      var svg = $('svg', wrap), cur = $('.cur', svg);
      function setY(y) { yr = clamp(Math.round(y), x0, x1); cur.setAttribute('x1', X(yr)); cur.setAttribute('x2', X(yr)); var i = ys.indexOf(yr); var im = S.imports[i], ss = S.selfsuff[i];
        rd.innerHTML = '<div><b>' + yr + '</b></div><div><b style="color:var(--red)">' + (im != null ? fmt(im) : '—') + '</b><div class="k">' + esc(L(S.l1)) + '</div></div><div><b>' + (ss != null ? fmt(ss, 1) + '%' : '—') + '</b><div class="k">' + esc(L(S.l2)) + '</div></div>';
        var e = (S.events || []).filter(function (e) { return e.year === yr; })[0] || (S.events || []).filter(function (e) { return e.year <= yr; }).slice(-1)[0];
        ev.innerHTML = e ? '<b>' + e.year + '</b> · ' + L(e) : ''; }
      function xy(cx) { var r = svg.getBoundingClientRect(); return x0 + (x1 - x0) * clamp((cx - r.left - m.l * r.width / W) / ((W - m.l - m.r) * r.width / W), 0, 1); }
      var dn = false;
      svg.addEventListener('pointerdown', function (e) { dn = true; svg.setPointerCapture(e.pointerId); setY(xy(e.clientX)); });
      svg.addEventListener('pointermove', function (e) { if (dn) setY(xy(e.clientX)); });
      svg.addEventListener('pointerup', function () { dn = false; }); svg.addEventListener('pointercancel', function () { dn = false; });
      $$('.mk', svg).forEach(function (g) { g.addEventListener('click', function (e) { e.stopPropagation(); setY(S.events[+g.getAttribute('data-i')].year); }); });
      svg.tabIndex = 0; svg.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); setY(yr + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); setY(yr - 1); } });
      setY(yr);
    }
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (wrap.clientWidth !== svgW) draw(); }, 120); });
    addEventListener('langchange', draw); draw();
  })();

  /* ---------- 透镜列表（通用） ---------- */
  (function () {
    $$('[data-list]').forEach(function (host) {
      var key = host.getAttribute('data-list'), items = D[key]; if (!items) return;
      var lensBox = $('.lens', host), list = $('.list', host), lenses = (D.lenses && D.lenses[key]) || null, lens = lenses ? lenses[0].id : null, open = {};
      function row(it, i) { return '<div class="item' + (open[it.id] ? ' open' : '') + '" data-id="' + it.id + '"><button aria-expanded="' + (open[it.id] ? 'true' : 'false') + '"><span class="no">' + esc(it.no || ((i + 1 < 10 ? '0' : '') + (i + 1))) + '</span><span class="tt"><b>' + esc(L(it.title)) + '</b><span>' + esc(L(it.one)) + '</span></span><span class="pl">+</span></button><div class="body"><ul>' + (it.facts || []).map(function (f) { return '<li>' + (f.k ? '<em>' + esc(L(f.k)) + '</em>' : '') + L(f) + (f.src ? ' <a class="src" href="' + esc(f.src) + '" target="_blank" rel="noopener">↗</a>' : '') + '</li>'; }).join('') + '</ul>' + (it.img ? '<figure><img src="' + it.img + '" alt="" loading="lazy"><figcaption>' + L(it.cap || '') + '</figcaption></figure>' : '<div></div>') + '</div></div>'; }
      function render() {
        if (lensBox && lenses) lensBox.innerHTML = lenses.map(function (l) { return '<button class="pill" aria-pressed="' + (l.id === lens ? 'true' : 'false') + '" data-l="' + l.id + '">' + esc(L(l)) + '</button>'; }).join('');
        var html = '';
        if (lenses) { var lz = lenses.filter(function (l) { return l.id === lens; })[0]; var groups = lz.groups; groups.forEach(function (gr) { var its = items.filter(function (it) { return (it.g || {})[lens] === gr.id; }); if (!its.length) return; html += '<div class="grp">' + esc(L(gr)) + '</div>' + its.map(function (it) { return row(it, items.indexOf(it)); }).join(''); }); }
        else html = items.map(row).join('');
        list.innerHTML = html;
        $$('.item>button', list).forEach(function (b) { b.addEventListener('click', function () { var id = b.parentNode.getAttribute('data-id'); open[id] = !open[id]; b.parentNode.classList.toggle('open', open[id]); b.setAttribute('aria-expanded', open[id] ? 'true' : 'false'); }); });
        if (lensBox) $$('.pill', lensBox).forEach(function (b) { b.addEventListener('click', function () { lens = b.getAttribute('data-l'); render(); }); });
      }
      render(); addEventListener('langchange', render);
    });
  })();

  /* ---------- 02 TABLE：一桌 ---------- */
  (function () {
    var t = $('#table'); if (!t || !D.table) return;
    var ls = $('.tl', t), im = $('.tp img', t), cp = $('.tcap', t), cur = 0;
    function render() { ls.innerHTML = D.table.map(function (x, i) { return '<button class="' + (i === cur ? 'on' : '') + '" data-i="' + i + '"><i>' + (i + 1) + '</i><span><b>' + esc(L(x.title)) + '</b><span>' + L(x.text) + '</span></span></button>'; }).join(''); $$('button', ls).forEach(function (b) { b.addEventListener('click', function () { cur = +b.getAttribute('data-i'); render(); }); }); var x = D.table[cur]; if (x.img && im.getAttribute('src') !== x.img) { im.style.opacity = 0; setTimeout(function () { im.src = x.img; im.style.opacity = 1; }, RM ? 0 : 180); } cp.innerHTML = L(x.cap || ''); }
    render(); addEventListener('langchange', render);
  })();

  /* ---------- 03 WORLD：扩张地图 ---------- */
  (function () {
    var m = $('#map'); if (!m || !D.map) return;
    var M = D.map, svg = $('svg', m), hud = $('.hud', m), rng = $('input', m.parentNode), note = $('.mapnote', m.parentNode), yr = +rng.value, play = $('[data-act=play]', m.parentNode), pt = 0;
    var vb = M.vb; svg.setAttribute('viewBox', vb.join(' '));
    svg.innerHTML = '<path class="land" d="' + M.land + '"/>' + M.nodes.map(function (n, i) { return '<g class="node" data-i="' + i + '" transform="translate(' + n.x + ',' + n.y + ')"><circle r="' + (n.r || 3) + '"/><text x="' + (n.dx || 5) + '" y="' + (n.dy || 3) + '" text-anchor="' + (n.ta || 'start') + '"></text></g>'; }).join('');
    var gs = $$('.node', svg);
    function upd() { yr = +rng.value; var last = null; gs.forEach(function (g, i) { var n = M.nodes[i], on = n.year <= yr; g.classList.toggle('off', !on); g.classList.toggle('on', on && n.year > yr - 6); $('text', g).textContent = L(n.city); g.classList.toggle('hide-l', !!n.minor && !(on && n.year > yr - 6)); if (on && (!last || n.year >= last.year)) last = n; });
      var cnt = M.nodes.filter(function (n) { return n.year <= yr; }).length;
      hud.innerHTML = yr + '<span>' + esc(L({ zh: '已标出 ' + cnt + ' 个节点', en: cnt + ' milestones on the map' })) + '</span>';
      note.innerHTML = last ? '<b>' + last.year + ' · ' + esc(L(last.city)) + '</b> — ' + L(last.text) : ''; }
    gs.forEach(function (g) { g.style.cursor = 'pointer'; g.addEventListener('click', function () { var n = M.nodes[+g.getAttribute('data-i')]; note.innerHTML = '<b>' + n.year + ' · ' + esc(L(n.city)) + '</b> — ' + L(n.text); }); });
    rng.addEventListener('input', upd);
    if (play) play.addEventListener('click', function () { if (pt) { clearInterval(pt); pt = 0; play.textContent = '▶'; return; } if (+rng.value >= +rng.max) rng.value = rng.min; play.textContent = '❚❚'; pt = setInterval(function () { rng.value = +rng.value + 1; upd(); if (+rng.value >= +rng.max) { clearInterval(pt); pt = 0; play.textContent = '▶'; } }, RM ? 30 : 160); });
    addEventListener('langchange', upd); upd();
  })();
})();
