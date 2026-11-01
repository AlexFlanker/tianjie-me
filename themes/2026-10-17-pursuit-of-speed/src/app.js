(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  var SVGNS = 'http://www.w3.org/2000/svg';
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
  var fmt = function (v) { v = Number(v); if (v >= 1e8) return num(v / 1e8, 2) + ' 亿'; if (v >= 100) return num(v, 0); if (v >= 10) return num(v, 1); return num(v, 2); };
  var srcs = function (ss) { if (!ss || !ss.length) return ''; return '<p class="src">来源：' + ss.slice(0, 4).map(function (s) { return s.u ? '<a href="' + esc(s.u) + '" target="_blank" rel="noopener">' + esc(s.t) + '</a>' : esc(s.t); }).join('；') + '</p>'; };
  var conf = function (c) { var k = { '高': 'h', '中': 'm', '低': 'l' }[c] || 'm'; return '<span class="conf ' + k + '">置信度 ' + esc(c || '中') + '</span>'; };
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

  /* ================= 深浅色：这一题默认是夜；用户切过就记住 ================= */
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  function curTheme() { return root.getAttribute('data-theme') || (window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'); }
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

  /* ================= 卷首：标题依次升起；论点逐词掠过 ================= */
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

  /* ================= 数字从 0 数到目标（进入视口时播一次） ================= */
  function countTo(n, to, dec, ms) {
    if (!n) return;
    if (RM.on || !ms) { n.textContent = num(to, dec); return; }
    var t0 = performance.now();
    (function step(t) { var p = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - p, 3); n.textContent = num(to * e, dec); if (p < 1) requestAnimationFrame(step); })(t0);
  }
  (function initCounts() {
    var cs = $$('.cnt[data-to]');
    var go = function (n) { countTo(n, parseFloat(n.getAttribute('data-to')), parseInt(n.getAttribute('data-dec') || '0', 10), 1100); };
    if ('IntersectionObserver' in window) { var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { go(e.target); cio.unobserve(e.target); } }); }, { threshold: .4 }); cs.forEach(function (n) { cio.observe(n); }); }
    else cs.forEach(function (n) { countTo(n, parseFloat(n.getAttribute('data-to')), parseInt(n.getAttribute('data-dec') || '0', 10), 0); });
  })();

  /* ================= 序章 · 十九级阶梯：全屏舞台（滚动与尺子是同一个量 t = 第几级） ================= */
  (function initStage() {
    var pin = $('#tlpin'), stg = $('#tlstage'), LV = D.stage; if (!pin || !stg || !LV) return;
    var N = LV.length, LO = 0, HI = 9.3;
    var card = $('#tlcard'), ruler = $('#tlruler'), track = $('#rtrack'), head = $('#rhead'), rlog = $('#rlog'), rlp = $('#rlp'), fan = $('#rfan'), pics = $('#tlpics'), cap = $('#tlcap');
    var E = { no: $('#tlno'), kick: $('#tlkick'), name: $('#tlname'), big: $('#tlbig'), alt: $('#tlalt'), text: $('#tltext'), specs: $('#tlspecs'), who: $('#tlwho'), src: $('#tlsrc'), cs: $('#tlcs'), cr: $('#tlcr'), c: $('#tlc'), needle: $('#tlneedle'), dfill: $('#tldfill') };
    var P = [$('#tlp0'), $('#tlp1')], BG = [$$('.tlbg img', stg)[0], $$('.tlbg img', stg)[1]], cur = 0;
    var marks = $$('.rmark', ruler), dots = $$('.rdot', ruler);
    // ---- 长度：每一级约 0.55 屏（手机 0.45）
    var stageH = 0, perStep = 0, pinTop = 0;
    function layout() {
      stageH = stg.offsetHeight; perStep = Math.round(window.innerHeight * (window.innerWidth < 700 ? 0.45 : 0.55));
      pin.style.height = (stageH + (N - 1) * perStep) + 'px';
      pinTop = pin.getBoundingClientRect().top + window.scrollY;
      drawFan();
      ruler.classList.toggle('all', track.clientWidth >= 1080);
      placeCap();
    }
    function tFromScroll() { return clamp((window.scrollY - (pinTop - navH())) / perStep, 0, N - 1); }
    function scrollForT(t) { return pinTop - navH() + t * perStep; }
    // ---- 尺子两排之间的连线：对数位置（上）→ 等距位置（下）
    var fanLines = [];
    function drawFan() {
      var W = track.clientWidth; if (!W) return;
      fan.setAttribute('viewBox', '0 0 ' + W + ' 22'); fan.innerHTML = ''; fanLines = [];
      LV.forEach(function (L, k) { fanLines.push(el('line', { x1: (L.f * W).toFixed(1), y1: 0, x2: (k / (N - 1) * W).toFixed(1), y2: 22 }, fan)); });
      if (curK >= 0 && fanLines[curK]) fanLines[curK].classList.add('on');
    }
    // ---- 速度读数与小表盘：一个弹簧走 log10(km/h)
    var logSp = new Spring({ from: Math.log10(LV[0].kmh), damping: 1, response: 0.42, eps: 0.0015, onUpdate: function (x) {
      var v = Math.pow(10, x), f = clamp((x - LO) / (HI - LO), 0, 1);
      E.big.textContent = bigFmt(v, x);
      E.needle.setAttribute('transform', 'rotate(' + (-135 + 270 * f).toFixed(2) + ' 50 50)');
      E.dfill.style.strokeDasharray = f.toFixed(4) + ' 1';
    } });
    var target = LV[0].kmh;
    function bigFmt(v, x) { if (Math.abs(x - Math.log10(target)) < 0.0002) return LV[curK >= 0 ? curK : 0].big; return fmt(v); }
    function altLine(L) {
      var v = L.kmh, h = D.tool1.bjsh / v;
      var t = h >= 48 ? num(h / 24, 1) + ' 天' : h >= 1 ? num(h, 1) + ' 小时' : h * 60 >= 1 ? num(h * 60, 1) + ' 分钟' : h * 3600 >= 0.1 ? num(h * 3600, 1) + ' 秒' : num(h * 3600, 4) + ' 秒';
      return num(v / 1.609344, v < 100 ? 1 : 0) + ' mph · 北京到上海 ' + t + (L.id !== 'walk' ? ' · 步行的 ' + num(v / 5, v / 5 < 100 ? 1 : 0) + ' 倍' : '');
    }
    // ---- 卡片换内容：淡出、换、淡入
    $$('.tlhd, .tlname, .tlalt, .tltext, .tlspecs, .tlwho, .tlsrc', card).forEach(function (n) { n.classList.add('swap'); });
    function fillCard(k) {
      var L = LV[k];
      E.no.textContent = ('0' + (k + 1)).slice(-2) + ' / ' + ('0' + N).slice(-2); E.kick.textContent = L.kick; E.name.textContent = L.name;
      E.alt.textContent = altLine(L); E.text.textContent = L.tag;
      E.specs.innerHTML = L.specs.map(function (s) { return '<div><dt>' + esc(s[0]) + '</dt><dd>' + esc(s[1]) + '</dd></div>'; }).join('');
      E.who.innerHTML = esc(L.who) + ' ' + L.conf; E.src.innerHTML = L.src;
    }
    var swapT = 0, shown = -1;
    function showCard(k) {
      if (k === shown) return; var first = shown < 0; shown = k;
      if (first || RM.on) { fillCard(k); return; }
      clearTimeout(swapT); card.classList.add('swapping');
      swapT = setTimeout(function () { fillCard(k); card.classList.remove('swapping'); }, 160);
    }
    // ---- 照片：两层交替；往上走新图从右边掠进来，往下走从左边（进出同一条路）
    var picK = 0, picTimer = 0, pending = -1;
    function placeCap() {
      var img = P[cur]; if (!img || !cap) return;
      if (!LV[picK].img) { cap.style.marginLeft = ''; cap.style.maxWidth = ''; return; }
      var w = img.offsetWidth, l = img.offsetLeft;
      if (w > 0) { cap.style.marginLeft = l + 'px'; cap.style.maxWidth = Math.max(240, w) + 'px'; }
    }
    function setCap(L) { E.cs.textContent = L.cap; E.cr.textContent = L.cred; }
    function showPic(k) {
      if (k === picK) return;
      var dir = k > picK ? 1 : -1, L = LV[k]; picK = k;
      var out = P[cur], inn = P[1 - cur], bo = BG[cur], bi = BG[1 - cur];
      if (!L.img) { // 光速：没有照片，只有字
        out.classList.remove('on'); bo.classList.remove('on'); E.c.classList.add('on'); setCap(L); placeCap(); return;
      }
      E.c.classList.remove('on');
      var go = function () {
        if (picK !== k) return;
        inn.className = RM.on ? '' : (dir > 0 ? 'from-r' : 'from-l'); void inn.offsetWidth;
        inn.className = 'on'; out.className = RM.on ? '' : (dir > 0 ? 'to-l' : 'to-r');
        bi.className = 'on'; bo.className = '';
        cur = 1 - cur; setCap(L);
        requestAnimationFrame(placeCap);
        setTimeout(function () { if (out !== P[cur]) out.className = ''; }, 520);
      };
      inn.alt = L.alt; inn.width = L.w; inn.height = L.h; bi.src = L.img;
      if (inn.getAttribute('src') === L.img && inn.complete) { go(); return; }
      inn.src = L.img;
      if (inn.decode) inn.decode().then(go, go); else inn.onload = go;
    }
    function prefetch(k) { [k - 1, k + 1].forEach(function (j) { if (LV[j] && LV[j].img) { var im = new Image(); im.decoding = 'async'; im.src = LV[j].img; } }); }
    // ---- 渲染一个 t
    var curK = -1, curT = null;
    function render(t) {
      curT = t;
      var k = clamp(Math.round(t), 0, N - 1), L = LV[k];
      if (k !== curK) {
        var first = curK < 0; curK = k;
        showCard(k);
        clearTimeout(picTimer); if (first) picK = 0; else picTimer = setTimeout(function () { showPic(k); }, RM.on ? 0 : 120);
        target = L.kmh; if (first) logSp.set(Math.log10(L.kmh)); else logSp.to(Math.log10(L.kmh));
        marks.forEach(function (m, i) { m.classList.toggle('on', i === k); });
        dots.forEach(function (d, i) { d.classList.toggle('on', i === k); });
        fanLines.forEach(function (l, i) { l.classList.toggle('on', i === k); });
        ruler.setAttribute('aria-valuenow', k); ruler.setAttribute('aria-valuetext', '第 ' + (k + 1) + ' 级：' + L.name + '，' + L.big + ' km/h');
        prefetch(k);
      }
      var W = track.clientWidth;
      head.style.transform = 'translateX(' + (t / (N - 1) * W).toFixed(1) + 'px)';
      var k0 = Math.floor(t), k1 = Math.min(N - 1, k0 + 1), f = LV[k0].f + (LV[k1].f - LV[k0].f) * smooth(t - k0);
      rlp.style.transform = 'translateX(' + (f * rlog.clientWidth).toFixed(1) + 'px)';
    }
    // ---- t 是一个弹簧：滚动给目标（轻微平滑），拖动直接设，松手按速度投影后吸附到最近的一级
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
      drag.off = Math.abs(t - hx) < 0.35 ? hx - t : 0; // 抓在播放头上：保留抓取偏移；抓在别处：按下即跳过去
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
    P.forEach(function (im) { im.addEventListener('load', function () { if (im === P[cur]) placeCap(); }); });
    var rz = 0;
    function relayout() { layout(); var t = mode === 'scroll' ? tFromScroll() : ts.x; ts.set(t); render(t); }
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(relayout, 120); });
    window.addEventListener('load', relayout);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
    layout(); ts.set(tFromScroll());
  })();

  /* ================= 第二章主图：六条赛道 × 八个时代（按实际宽度现画；窄屏改成时代在左、速度向右） ================= */
  (function initTracks() {
    var box = $('#tkbox'), svg = $('#tksv'), mxd = $('#mxd'), chips = $('#tkchips'); if (!box || !svg || !D.cells) return;
    var TR = D.tracks, ER = D.eras, sel = '', curKey = mxd ? mxd.getAttribute('data-first') : '';
    var YMIN = 0.6, YMAX = 6; // log10 km/h：4 km/h – 100 万 km/h
    var DEC = { 1: '10', 2: '100', 3: '1,000', 4: '1 万', 5: '10 万', 6: '100 万' };
    function showCell(key) {
      var c = D.cells[key]; if (!c || !mxd) return; curKey = key;
      $$('.pt', svg).forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-key') === key); });
      $$('.pv', svg).forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-key') === key); });
      if (c.empty) { mxd.innerHTML = '<p class="kicker">' + esc(c.track) + ' · ' + esc(c.era) + '</p><h4>这一格空着</h4><p class="empty">' + esc(c.why) + '</p>'; return; }
      var also = c.also ? '<dt>同格另一条</dt><dd><b>' + esc(c.also.subject) + '</b> · ' + esc(c.also.speed) + ' · ' + esc(c.also.who) + '。' + esc(c.also.why || '') + (c.also.note ? ' ' + esc(c.also.note) : '') + ' ' + conf(c.also.conf) + srcs(c.also.sources) + '</dd>' : '';
      var ph = c.img ? '<figure><img src="' + esc(c.img.file) + '" alt="' + esc(c.img.alt) + '" loading="lazy"><figcaption>' + esc(c.img.cap) + ' ' + esc(c.img.credit) + '</figcaption></figure>' : '';
      mxd.innerHTML = '<p class="kicker">' + esc(c.track) + ' · ' + esc(c.era) + '</p><h4>' + esc(c.subject) + '</h4><p class="big"><b>' + fmt(c.kmh) + '</b><small>km/h</small></p><p class="spd">' + esc(c.speed) + ' ' + conf(c.conf) + '</p>'
        + '<dl><dt>年份</dt><dd>' + esc(c.year) + '</dd><dt>谁</dt><dd>' + esc(c.who) + (c.where ? '，' + esc(c.where) : '') + '</dd><dt>为什么是它</dt><dd>' + esc(c.why) + '</dd>' + (c.note ? '<dt>口径</dt><dd>' + esc(c.note) + '</dd>' : '') + also + '</dl>' + srcs(c.sources) + ph;
    }
    function setSel(tid) {
      sel = tid;
      $$('button', chips).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-tk') === tid)); });
      svg.classList.toggle('hl', !!tid);
      $$('.tl, .tn2', svg).forEach(function (n) { n.classList.toggle('on', n.getAttribute('data-tk') === tid); });
      $$('.pt, .pv', svg).forEach(function (n) { n.classList.toggle('lit', n.getAttribute('data-tk') === tid); });
    }
    function draw() {
      var W = Math.round(box.clientWidth - 16); if (W < 200) return;
      var vert = W < 640;
      svg.innerHTML = '';
      var Hh, X, Y, pos;
      if (!vert) {
        var L = 64, R = 104, T = 16, B = 40, PH = 360; Hh = T + PH + B;
        X = function (e) { return L + e * (W - L - R) / (ER.length - 1); };
        Y = function (v) { return T + (YMAX - Math.log10(v)) / (YMAX - YMIN) * PH; };
        for (var d = 1; d <= 6; d++) { var y = Y(Math.pow(10, d)); el('line', { 'class': 'gl' + (d === 3 ? ' s' : ''), x1: L, y1: y, x2: W - R + 16, y2: y }, svg); var tx = el('text', { 'class': 'gt', x: L - 8, y: y + 4, 'text-anchor': 'end' }, svg); tx.textContent = DEC[d]; }
        var ux = el('text', { 'class': 'gt', x: L - 8, y: T - 4 + 0, 'text-anchor': 'end' }, svg); ux.textContent = '';
        ER.forEach(function (e, i) { var t1 = el('text', { 'class': 'gt s', x: X(i), y: T + PH + 20, 'text-anchor': 'middle' }, svg); t1.textContent = e[2]; var t2 = el('text', { 'class': 'gt', x: X(i), y: T + PH + 36, 'text-anchor': 'middle' }, svg); t2.textContent = e[1]; });
        pos = function (tid, e, v) { return [X(e), v ? Y(v) : T + PH]; };
      } else {
        var L2 = 72, R2 = 12, T2 = 28, RH = 40; Hh = T2 + ER.length * RH + 8;
        X = function (v) { return L2 + (Math.log10(v) - YMIN) / (YMAX - YMIN) * (W - L2 - R2); };
        Y = function (e) { return T2 + e * RH + RH / 2; };
        for (var d2 = 1; d2 <= 6; d2++) { var x = X(Math.pow(10, d2)); el('line', { 'class': 'gl' + (d2 === 3 ? ' s' : ''), x1: x, y1: T2 - 4, x2: x, y2: Hh - 8 }, svg); if (d2 % 2 === 1 || W > 420) { var tx2 = el('text', { 'class': 'gt', x: x, y: T2 - 10, 'text-anchor': 'middle' }, svg); tx2.textContent = DEC[d2]; } }
        ER.forEach(function (e, i) { var t3 = el('text', { 'class': 'gt s', x: 0, y: Y(i) + 4 }, svg); t3.textContent = e[2]; });
        pos = function (tid, e, v) { return [v ? X(v) : L2 + 8, Y(e)]; };
      }
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh); svg.setAttribute('width', W); svg.setAttribute('height', Hh);
      var gLines = el('g', {}, svg), gPts = el('g', {}, svg), gLab = el('g', {}, svg), ends = [];
      TR.forEach(function (tr, ti) {
        var tid = tr[0], pts = [];
        ER.forEach(function (e, i) {
          var key = tid + '-' + i, c = D.cells[key]; if (!c) return;
          var p = pos(tid, i, c.empty ? 0 : c.kmh);
          if (c.empty) { p = vert ? [p[0] + ti * 6, p[1]] : [p[0] + (ti - 2.5) * 6, p[1]]; }
          else pts.push(p);
          var g = el('g', { 'class': 'pt' + (c.empty ? ' e' : ''), 'data-key': key, 'data-tk': tid, tabindex: '0', role: 'button', 'aria-label': tr[1] + ' · ' + e[0] + '：' + (c.empty ? '空格' : c.subject + ' ' + fmt(c.kmh) + ' km/h') }, gPts);
          el('circle', { 'class': 'hit', cx: p[0].toFixed(1), cy: p[1].toFixed(1), r: 12 }, g);
          el('circle', { 'class': 'dot', cx: p[0].toFixed(1), cy: p[1].toFixed(1), r: c.empty ? 3.5 : 4.5 }, g);
          if (!c.empty) { var pv = el('text', { 'class': 'pv', 'data-key': key, 'data-tk': tid, x: p[0].toFixed(1), y: (p[1] - 10).toFixed(1), 'text-anchor': 'middle' }, gLab); pv.textContent = fmt(c.kmh); }
        });
        if (pts.length > 1) el('polyline', { 'class': 'tl', 'data-tk': tid, points: pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ') }, gLines);
        if (pts.length) ends.push({ tid: tid, name: tr[1], x: pts[pts.length - 1][0], y: pts[pts.length - 1][1] });
      });
      // 线尾标签：横屏放右侧并按 y 错开 16 px
      if (!vert) {
        ends.sort(function (a, b) { return a.y - b.y; });
        for (var i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 16) ends[i].y = ends[i - 1].y + 16;
        ends.forEach(function (e) { var t = el('text', { 'class': 'tn2', 'data-tk': e.tid, x: e.x + 10, y: e.y + 4 }, gLab); t.textContent = e.name; });
      }
      setSel(sel); showCell(curKey);
    }
    svg.addEventListener('click', function (e) { var p = e.target.closest('.pt'); if (p) showCell(p.getAttribute('data-key')); });
    svg.addEventListener('keydown', function (e) { if (e.key !== 'Enter' && e.key !== ' ') return; var p = e.target.closest('.pt'); if (p) { e.preventDefault(); showCell(p.getAttribute('data-key')); } });
    chips.addEventListener('click', function (e) { var b = e.target.closest('button[data-tk]'); if (b) setSel(b.getAttribute('data-tk')); });
    var lastW = 0;
    function maybe() { var w = box.clientWidth; if (w !== lastW) { lastW = w; draw(); } }
    if ('ResizeObserver' in window) new ResizeObserver(maybe).observe(box); else window.addEventListener('resize', maybe);
    maybe();
  })();

  /* ================= 第三章主图：两条线（按实际宽度现画；拖动竖线、方向键、播放） ================= */
  (function initLines() {
    var box = $('#lnbox'), svg = $('#lnsv'), play = $('#ln-play'), yEl = $('#ln-y'), flash = $('#ln-flash'); if (!box || !svg || !D.lines) return;
    var LN = D.lines, REC = LN.rec, DAY = LN.day, Y0 = 1790, Y1 = 2030, V0 = 0.6, V1 = 5;
    var rv = $('#ln-rv'), rvs = $('#ln-rv-s'), dv = $('#ln-dv'), dvs = $('#ln-dv-s'), xv = $('#ln-x');
    var year = 2026, G = null;
    function valAt(arr, y) { var p = arr[0]; for (var i = 0; i < arr.length; i++) if (arr[i].y <= y) p = arr[i]; return p; }
    function draw() {
      var W = Math.round(box.clientWidth - 16); if (W < 200) return;
      var narrow = W < 640, L = narrow ? 44 : 64, R = narrow ? 12 : 24, T = 24, B = 32, PH = narrow ? 260 : 380, Hh = T + PH + B;
      var X = function (y) { return L + (clamp(y, Y0, Y1) - Y0) / (Y1 - Y0) * (W - L - R); };
      var Y = function (v) { return T + (V1 - Math.log10(v)) / (V1 - V0) * PH; };
      svg.innerHTML = ''; svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh); svg.setAttribute('width', W); svg.setAttribute('height', Hh);
      el('rect', { 'class': 'band2', x: X(1976), y: T, width: X(2003) - X(1976), height: PH }, svg);
      var bt = el('text', { 'class': 'bandt', x: (X(1976) + X(2003)) / 2, y: T + PH - 8, 'text-anchor': 'middle' }, svg); bt.textContent = narrow ? '协和' : '协和 1976–2003';
      var DEC = { 1: '10', 2: '100', 3: '1,000', 4: '1 万', 5: '10 万' };
      for (var d = 1; d <= 5; d++) { var y = Y(Math.pow(10, d)); el('line', { 'class': 'gl' + (d === 3 ? ' s' : ''), x1: L, y1: y, x2: W - R, y2: y }, svg); var t = el('text', { 'class': 'gt', x: L - 8, y: y + 4, 'text-anchor': 'end' }, svg); t.textContent = DEC[d]; }
      var step = narrow ? 50 : 25;
      for (var yr = 1800; yr <= 2025; yr += step) { var x = X(yr); el('line', { 'class': 'gl', x1: x, y1: T, x2: x, y2: T + PH }, svg); var t2 = el('text', { 'class': 'gt', x: x, y: T + PH + 20, 'text-anchor': 'middle' }, svg); t2.textContent = yr; }
      var ku = el('text', { 'class': 'gt', x: L - 8, y: T - 8, 'text-anchor': 'end' }, svg); ku.textContent = 'km/h';
      function stepPath(arr, endY) { var p = [], prev = null; arr.forEach(function (q) { var x = X(q.y), y = Y(q.v); if (prev !== null) p.push(x.toFixed(1) + ',' + prev.toFixed(1)); p.push(x.toFixed(1) + ',' + y.toFixed(1)); prev = y; }); p.push(X(endY).toFixed(1) + ',' + prev.toFixed(1)); return p.join(' '); }
      // 底层：整条线淡显；上层：到当前年份为止的部分
      var recPts = stepPath(REC, 2026), dayPts = stepPath(DAY, 2026);
      el('polyline', { 'class': 'rec ghost', points: recPts }, svg); el('polyline', { 'class': 'day ghost', points: dayPts }, svg);
      var clip = el('clipPath', { id: 'lnclip' }, el('defs', {}, svg)), cr = el('rect', { x: 0, y: 0, width: X(year), height: Hh }, clip);
      var g = el('g', { 'clip-path': 'url(#lnclip)' }, svg);
      el('polyline', { 'class': 'day', points: dayPts }, g); el('polyline', { 'class': 'rec', points: recPts }, g);
      REC.forEach(function (q) { el('circle', { 'class': 'pr', cx: X(q.y), cy: Y(q.v), r: 4 }, g); });
      DAY.forEach(function (q) { el('circle', { 'class': 'pd', cx: X(q.y), cy: Y(q.v), r: 3.5 }, g); });
      el('circle', { 'class': 'art', cx: X(LN.art.y), cy: Y(LN.art.v), r: 6 }, g);
      (LN.hsr || []).forEach(function (q) { el('circle', { 'class': 'ph', cx: X(q.y), cy: Y(q.v), r: 4.5 }, g); });
      // 标签：只标转折点
      var LAB = narrow ? [['r', 1969, 'Apollo 10 · 39,897', -8, -10, 'end'], ['d', 1976, '协和 · 2,180', -8, -8, 'end'], ['h', 2017, '高铁 350', -8, 20, 'end']]
                       : [['r', 1947, 'X-1 · 1,127', -8, -8, 'end'], ['r', 1961, '加加林 · 27,400', -8, -8, 'end'], ['r', 1969, 'Apollo 10 · 39,897', 8, -10, 'start'], ['d', 1958, '喷气客机 · 900', 8, 18, 'start'], ['d', 1976, '协和 · 2,180', 8, -8, 'start'], ['d', 2003, '退回 900', 8, 18, 'start'], ['h', 1964, '新干线 · 210', 9, 4, 'start'], ['h', 2017, '地面高铁 · 350', -8, 20, 'end'], ['d', 1830, '铁路 · 27', 8, 18, 'start']];
      LAB.forEach(function (a) { var arr = a[0] === 'r' ? REC : a[0] === 'h' ? (LN.hsr || []) : DAY, q = null; arr.forEach(function (p) { if (p.y === a[1]) q = p; }); if (!q) return; var t3 = el('text', { 'class': 'pl' + (a[0] === 'r' ? ' r' : ''), x: X(q.y) + a[3], y: Y(q.v) + a[4], 'text-anchor': a[5] }, g); t3.textContent = a[2]; });
      // 游标
      var cur = el('g', {}, svg);
      G = { X: X, Y: Y, T: T, PH: PH, clip: cr, cur: cur, line: el('line', { 'class': 'cur', x1: 0, y1: T, x2: 0, y2: T + PH }, cur), glow: null, dr: el('circle', { 'class': 'dotr', r: 5.5 }, cur), dd: el('circle', { 'class': 'dotd', r: 5 }, cur), knob: el('circle', { 'class': 'curk', r: 7, cy: T + PH }, cur) };
      G.glow = el('line', { 'class': 'curg', x1: 0, y1: T, x2: 0, y2: T + PH }, cur); cur.insertBefore(G.glow, G.line);
      setYear(year, false);
    }
    var lastMs = 1799;
    function setYear(y, fromPlay) {
      year = clamp(Math.round(y), 1800, 2026); if (!G) return;
      var x = G.X(year), r = valAt(REC, year), d = valAt(DAY, year);
      G.clip.setAttribute('width', (x + 1).toFixed(1));
      [G.line, G.glow].forEach(function (l) { l.setAttribute('x1', x.toFixed(1)); l.setAttribute('x2', x.toFixed(1)); });
      G.knob.setAttribute('cx', x.toFixed(1)); G.dr.setAttribute('cx', x.toFixed(1)); G.dr.setAttribute('cy', G.Y(r.v).toFixed(1)); G.dd.setAttribute('cx', x.toFixed(1)); G.dd.setAttribute('cy', G.Y(d.v).toFixed(1));
      yEl.textContent = year; rv.textContent = fmt(r.v) + ' km/h'; rvs.textContent = '人类坐过的最快 · ' + r.n; dv.textContent = fmt(d.v) + ' km/h'; dvs.textContent = '普通乘客能坐到的最快 · ' + d.n;
      xv.textContent = num(r.v / d.v, r.v / d.v < 10 ? 1 : 0) + ' 倍';
      box.setAttribute('aria-valuenow', year); box.setAttribute('aria-valuetext', year + ' 年：纪录 ' + fmt(r.v) + '，日常 ' + fmt(d.v) + ' km/h');
      if (fromPlay) LN.ms.forEach(function (m) { if (lastMs < m[0] && year >= m[0]) msg(m[2], m[1]); });
      lastMs = year;
    }
    function msg(t, cls) { flash.textContent = t; flash.className = 'lflash on ' + cls; clearTimeout(flash._t); flash._t = setTimeout(function () { flash.classList.remove('on'); }, 2600); }
    // 拖动：按下即跳到指针处，之后 1:1 跟手
    var drag = null, raf = 0;
    function yAt(e) { var r = svg.getBoundingClientRect(), s = r.width / svg.viewBox.baseVal.width, x = (e.clientX - r.left) / s; return Y0 + (x - G.X(Y0)) / (G.X(Y1) - G.X(Y0)) * (Y1 - Y0); }
    box.addEventListener('pointerdown', function (e) { if (e.button > 0 || !G) return; drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: e.pointerType === 'mouse' }; if (drag.on) { cancelAnimationFrame(raf); try { box.setPointerCapture(e.pointerId); } catch (er) {} setYear(yAt(e), false); } });
    box.addEventListener('pointermove', function (e) { if (!drag || e.pointerId !== drag.id) return; if (!drag.on) { var it = dragIntent(e, drag.sx, drag.sy); if (it === 1) { drag.on = true; cancelAnimationFrame(raf); try { box.setPointerCapture(e.pointerId); } catch (er) {} } else if (it === -1) { drag = null; return; } else return; } setYear(yAt(e), false); });
    ['pointerup', 'pointercancel'].forEach(function (ev) { box.addEventListener(ev, function (e) { if (drag && e.pointerId === drag.id) drag = null; }); });
    box.addEventListener('keydown', function (e) { var s = e.shiftKey ? 10 : 1, y = null; if (e.key === 'ArrowRight' || e.key === 'ArrowUp') y = year + s; else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') y = year - s; else if (e.key === 'Home') y = 1800; else if (e.key === 'End') y = 2026; else return; e.preventDefault(); cancelAnimationFrame(raf); setYear(y, false); });
    play.addEventListener('click', function () {
      cancelAnimationFrame(raf); lastMs = 1799;
      if (RM.on) { setYear(2026, true); return; }
      var t0 = performance.now(), dur = 9000;
      (function stepF(t) { var p = clamp((t - t0) / dur, 0, 1); setYear(1800 + 226 * p, true); if (p < 1) raf = requestAnimationFrame(stepF); })(t0);
    });
    var lastW = 0;
    function maybe() { var w = box.clientWidth; if (w !== lastW) { lastW = w; draw(); } }
    if ('ResizeObserver' in window) new ResizeObserver(maybe).observe(box); else window.addEventListener('resize', maybe);
    maybe();
  })();

  /* ================= 列表：透镜分组（FLIP 补间）+ 行内展开 ================= */
  (function initLists() {
    var allRows = {};
    $$('.lrow').forEach(function (r) { allRows[r.id] = r; });
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
        grid.offsetHeight; // 强制回流
        Object.keys(rows).forEach(function (id) { var r = rows[id]; if (!r.style.transform) return; r.style.transition = 'transform .5s cubic-bezier(.22,1,.36,1)'; r.style.transform = ''; });
        $$('.lgh', grid).forEach(function (h) { if (h.animate) h.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'cubic-bezier(.22,1,.36,1)' }); });
      }
      lensEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-lens]'); if (b) setLens(b.getAttribute('data-lens')); });
      lensEl.addEventListener('keydown', function (e) { if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return; var i = tabs.findIndex(function (t) { return t.getAttribute('data-lens') === cur; }), n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); setLens(n.getAttribute('data-lens')); e.preventDefault(); });
      movePill(true);
      window.addEventListener('resize', function () { movePill(true); });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); });
    });
    var m = /^#((?:h|why)-[\w-]+)$/.exec(location.hash || '');
    if (m && allRows[m[1]]) setTimeout(function () { var r = allRows[m[1]]; toggle(r, true); scrollToRow(r); }, 60);
  })();
})();
