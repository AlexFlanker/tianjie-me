(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  window.YZ = { D: D };

  /* ================= 共用：减少动效（实时）、弹簧、速度、动量投影 ================= */
  var RM = { on: false };
  try { var rmq = window.matchMedia('(prefers-reduced-motion: reduce)'); RM.on = rmq.matches; var rmc = function (e) { RM.on = e.matches; }; if (rmq.addEventListener) rmq.addEventListener('change', rmc); else if (rmq.addListener) rmq.addListener(rmc); } catch (e) {}
  window.YZ.RM = RM;
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
  window.YZ.Spring = Spring; window.YZ.VTrack = VTrack; window.YZ.project = project; window.YZ.clamp = clamp; window.YZ.smooth = smooth; window.YZ.dragIntent = dragIntent;

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
  var fades = $$('.fade').concat($$('.rise').filter(function (el) { return !el.closest('#top'); }));
  if ('IntersectionObserver' in window && !RM.on) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else { fades.forEach(function (el) { el.classList.add('in'); }); }

  /* ================= 卷首：标题依次升起；论点逐词点亮 ================= */
  (function initHero() {
    var h = $('#top'); if (!h) return;
    var rs = $$('.rise', h);
    if (RM.on) { rs.forEach(function (el) { el.classList.add('in'); }); return; }
    requestAnimationFrame(function () { rs.forEach(function (el, i) { el.style.transitionDelay = (0.15 + Math.min(i * 0.08, 0.4)).toFixed(2) + 's'; el.classList.add('in'); }); });
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
  window.YZ.navH = navH;
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

  /* ================= 节点行的公开接口（序章卡片、主图都会调） ================= */
  var LAMPS = { open: function () {} };
  window.YZ.lamps = LAMPS;
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('[data-open]'); if (!a) return;
    var id = a.getAttribute('data-open'); if (!id || !document.getElementById('n-' + id)) return;
    ev.preventDefault(); LAMPS.open(id);
  });

  /* ================= 序章 · 对历与对表：全屏舞台（滚动与刻度尺是同一个量 t = 第几步） ================= */
  var RAD = Math.PI / 180;
  function dayPoly(decl, sslon) {
    var d = Math.abs(decl) > 0.2 ? decl : (decl >= 0 ? 0.2 : -0.2), td = Math.tan(d * RAD), pts = [];
    for (var lam = -186; lam <= 186; lam += 3) { var phi = Math.atan(-Math.cos((lam - sslon) * RAD) / td) / RAD; pts.push(((lam + 180) * 2).toFixed(1) + ' ' + ((90 - phi) * 2).toFixed(1)); }
    var edge = d > 0 ? -40 : 400;
    return 'M' + pts.join(' L') + ' L' + ((186 + 180) * 2) + ' ' + edge + ' L' + ((-186 + 180) * 2) + ' ' + edge + 'Z';
  }
  (function initStage() {
    var pin = $('#tlpin'), stg = $('#tlstage'); if (!pin || !stg || !D.stage) return;
    var S = D.stage, STEPS = S.steps, N = STEPS.length, CITIES = S.cities, ORDER = S.order;
    var wmap = $('#wmap'), scene = $('#jscene'), hud = $('#jhud'), card = $('#tlcard'), panel = $('#tlplates'), pbtn = $('#tlbtn'), ruler = $('#tlruler'), track = $('#rtrack'), head = $('#rhead');
    var el = { jk: $('#jk'), jyear: $('#jyear'), jt: $('#jt'), no: $('#tlno'), kick: $('#tlkick'), big: $('#tlbig'), bigu: $('#tlbigu'), basis: $('#tlbasis'), text: $('#tltext'), chips: $('#tlchips'), img: $('#tlimg'), cap: $('#tlcap'), fig: $('.tlph', card) };
    var daypoly = $('#daypoly'), ssm = $('#ssmark'), gmt = $('#gmtline'), gmtl = $('#gmtlab');
    var dots = {}, rows = {}, marks = $$('.rmark', ruler);
    $$('.cdot', stg).forEach(function (d) { dots[d.getAttribute('data-city')] = d; });
    $$('.tpr', stg).forEach(function (r) { rows[r.getAttribute('data-city')] = { el: r, hh: $('.hh', r), mh: $('.mh', r), dial: $('.dial', r), time: $('.tpn span', r), plate: $('.tpp b', r), sub: $('.tpp span', r) }; });
    var ALL = Object.keys(CITIES);
    function focusIds(s) { return s.hl && s.hl.length ? s.hl : ALL; }
    // ---- 长度：每一步约 0.55 屏
    var stageH = 0, perStep = 0, pinTop = 0;
    function layout() {
      stageH = stg.offsetHeight; perStep = Math.round(window.innerHeight * (window.innerWidth < 700 ? 0.45 : 0.55));
      pin.style.height = (stageH + (N - 1) * perStep) + 'px';
      pinTop = pin.getBoundingClientRect().top + window.scrollY;
      frames = STEPS.map(function (s) { return frameFor(focusIds(s)); });
    }
    function freeRect() {
      var sr = scene.getBoundingClientRect(), W = sr.width, H = sr.height, r = { x0: 14, x1: W - 14, y0: 14, y1: H - 14 }, hb = hud.getBoundingClientRect();
      r.y0 = Math.max(r.y0, hb.bottom - sr.top + 10);
      if (window.innerWidth >= 981) {
        var cb = card.getBoundingClientRect(), rb = ruler.getBoundingClientRect();
        r.x0 = cb.right - sr.left + 26; r.y1 = rb.top - sr.top - 18;
        if (panel && !panel.hidden) { var pb = panel.getBoundingClientRect(); r.x1 = pb.left - sr.left - 22; }
      }
      if (r.x1 - r.x0 < 160) r.x0 = Math.max(14, r.x1 - 160);
      if (r.y1 - r.y0 < 120) r.y0 = Math.max(14, r.y1 - 120);
      return { W: W, H: H, r: r };
    }
    function tFromScroll() { return clamp((window.scrollY - (pinTop - navH())) / perStep, 0, N - 1); }
    function scrollForT(t) { return pinTop - navH() + t * perStep; }
    // ---- 镜头：把这一步有变化的城框进来（没有就框全部十二城）；相邻两步之间按 t 插值
    var frames = [];
    function frameFor(ids) {
      var F = freeRect(), W = F.W || 720, H = F.H || 360, r = F.r, xs = [], ys = [];
      ids.forEach(function (id) { var c = CITIES[id]; if (c) { xs.push((c.lon + 180) * 2); ys.push((90 - c.lat) * 2); } });
      if (!xs.length) return [0, 0, 720, 720 * H / W];
      var padX = 40, padY = 30, minx = Math.min.apply(null, xs) - padX, maxx = Math.max.apply(null, xs) + padX, miny = Math.min.apply(null, ys) - padY, maxy = Math.max.apply(null, ys) + padY;
      var fw = r.x1 - r.x0, fh = r.y1 - r.y0, minW = W < 700 ? 220 : 320;
      var ppu = Math.min(fw / (maxx - minx), fh / (maxy - miny), W / minW);
      ppu = Math.max(ppu, fw / 800); // 最远缩到空处装下整个世界（720 + 边距），不再更小
      var w = W / ppu, h = H / ppu, cxu = (minx + maxx) / 2, cyu = (miny + maxy) / 2;
      var x = cxu - ((r.x0 + r.x1) / 2) / ppu, y = cyu - ((r.y0 + r.y1) / 2) / ppu;
      var xlo = maxx - r.x1 / ppu, xhi = minx - r.x0 / ppu, ylo = maxy - r.y1 / ppu, yhi = miny - r.y0 / ppu;
      var xm = w <= 720 ? clamp(x, 0, 720 - w) : (720 - w) / 2, ym = h <= 360 ? clamp(y, 0, 360 - h) : (360 - h) / 2;
      x = xlo <= xhi ? clamp(xm, xlo, xhi) : x; y = ylo <= yhi ? clamp(ym, ylo, yhi) : y;
      return [x, y, w, h];
    }
    var blendFrom = null, blendU = 1;
    var blendSp = new Spring({ from: 1, damping: 1, response: 0.45, eps: 0.002, onUpdate: function (u) { blendU = u; if (curT !== null) render(curT, true); }, onRest: function () { blendFrom = null; } });
    function reframe(animated) { var old = frames; frames = STEPS.map(function (s) { return frameFor(focusIds(s)); }); if (animated && old.length && !RM.on) { blendFrom = old; blendSp.set(0); blendSp.to(1); } else if (curT !== null) render(curT, true); }
    if (pbtn && panel) pbtn.addEventListener('click', function () { var open = panel.hidden; panel.hidden = !open; pbtn.setAttribute('aria-expanded', String(open)); reframe(true); });
    function lerpArr(a, b, u) { return [0, 1, 2, 3].map(function (i) { return a[i] + (b[i] - a[i]) * u; }); }
    function vbAt(t, fr) { fr = fr || frames; var k0 = Math.floor(clamp(t, 0, N - 1)), k1 = Math.min(N - 1, k0 + 1); return lerpArr(fr[k0], fr[k1], smooth(t - k0)); }
    var lastVB = null;
    function setVB(v) {
      wmap.setAttribute('viewBox', v.map(function (n) { return n.toFixed(2); }).join(' '));
      var ppu = (scene.clientWidth || 720) / v[2], k = 1.1 / ppu;
      Object.keys(dots).forEach(function (id) { var d = dots[id]; d.setAttribute('transform', 'translate(' + d.getAttribute('data-x') + ' ' + d.getAttribute('data-y') + ') scale(' + k.toFixed(3) + ')'); });
      var p = ssm.getAttribute('data-p'); if (p) ssm.setAttribute('transform', 'translate(' + p + ') scale(' + k.toFixed(3) + ')');
      if (gmtl) { var hb = hud.getBoundingClientRect(), sr = scene.getBoundingClientRect(), top = Math.max(20, hb.bottom - sr.top + 24); gmtl.setAttribute('transform', 'translate(364 ' + (v[1] + top / ppu).toFixed(1) + ') scale(' + k.toFixed(3) + ')'); gmtl.setAttribute('x', '0'); gmtl.setAttribute('y', '0'); gmtl.style.display = ((360 - v[0]) * ppu < 8 || (v[0] + v[2] - 360) * ppu < 96) ? 'none' : ''; }
      lastVB = v;
    }
    // ---- 晨昏线：按 t 在相邻两步的太阳赤纬与直射点经度之间插值
    var lastSun = '';
    function setSun(t) {
      var k0 = Math.floor(clamp(t, 0, N - 1)), k1 = Math.min(N - 1, k0 + 1), u = smooth(t - k0);
      var dec = STEPS[k0].decl + (STEPS[k1].decl - STEPS[k0].decl) * u, sl = STEPS[k0].sslon + (STEPS[k1].sslon - STEPS[k0].sslon) * u;
      var key = dec.toFixed(2) + '|' + sl.toFixed(2); if (key === lastSun) return; lastSun = key;
      daypoly.setAttribute('d', dayPoly(dec, sl));
      ssm.setAttribute('data-p', ((sl + 180) * 2).toFixed(1) + ' ' + ((90 - dec) * 2).toFixed(1));
    }
    // ---- 标签避让（像素）：先给有变化的城找位置，再给其余；躲开 HUD、卡片、十二城面板与刻度尺
    function placeLabels(v, lit) {
      var W = scene.clientWidth || 720, H = scene.clientHeight || 360, ppu = W / v[2], sr = scene.getBoundingClientRect();
      function box(e) { if (!e || (!e.offsetParent && e !== hud)) return null; var r = e.getBoundingClientRect(); if (!r.width) return null; return { x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height }; }
      var taken = [box(hud), box(card), box(panel && !panel.hidden ? panel : null), box(pbtn), box(ruler)].filter(Boolean), pos = {};
      var nUI = taken.length;
      Object.keys(dots).forEach(function (id) { var d = dots[id]; var P = pos[id] = { x: (parseFloat(d.getAttribute('data-x')) - v[0]) * ppu, y: (parseFloat(d.getAttribute('data-y')) - v[1]) * ppu }; taken.push({ x: P.x - 5, y: P.y - 5, w: 10, h: 10 }); var under = taken.slice(0, nUI).some(function (q) { return P.x > q.x - 4 && P.x < q.x + q.w + 4 && P.y > q.y - 4 && P.y < q.y + q.h + 4; }); d.classList.toggle('under', under && lit.indexOf(id) < 0); });
      var order = lit.slice(); Object.keys(dots).forEach(function (id) { if (order.indexOf(id) < 0) order.push(id); });
      var DIRS = { t: [0, -9, 'middle'], b: [0, 15, 'middle'], r: [8, 4, 'start'], l: [-8, 4, 'end'] };
      order.forEach(function (id) {
        var d = dots[id], tx = d.querySelector('text'), n = tx.textContent.length, tw = n * 12.5 + 2, th = 13, p = pos[id], isLit = lit.indexOf(id) >= 0;
        if (p.x < -20 || p.x > W + 20 || p.y < -20 || p.y > H + 20) { d.classList.remove('lab'); return; }
        var pref = d.getAttribute('data-off') || 't', tries = [pref].concat(['t', 'b', 'r', 'l'].filter(function (k) { return k !== pref; })), best = null;
        for (var i = 0; i < tries.length; i++) {
          var dd = DIRS[tries[i]], lx = p.x + dd[0] * 1.1, ly = p.y + dd[1] * 1.1, bx = dd[2] === 'middle' ? lx - tw / 2 : dd[2] === 'start' ? lx : lx - tw, b = { x: bx - 2, y: ly - th + 2, w: tw + 4, h: th + 2 };
          if (b.x < 2 || b.y < 2 || b.x + b.w > W - 2 || b.y + b.h > H - 2) continue;
          var hit = taken.some(function (q) { return b.x < q.x + q.w && b.x + b.w > q.x && b.y < q.y + q.h && b.y + b.h > q.y; });
          if (!hit) { best = { d: dd, b: b }; break; }
          if (!best && isLit && i === 0) best = { d: dd, b: b };
        }
        if (!best) { d.classList.remove('lab'); return; }
        tx.setAttribute('x', best.d[0]); tx.setAttribute('y', best.d[1]); tx.setAttribute('text-anchor', best.d[2]); d.classList.add('lab'); taken.push(best.b);
      });
    }
    // ---- 卡片换内容：淡出、换、淡入
    var shownStep = -1, swapT = 0;
    function fillCard(k) {
      var s = STEPS[k];
      el.no.textContent = ('0' + (k + 1)).slice(-2) + ' / ' + ('0' + N).slice(-2); el.kick.textContent = s.year + ' · ' + s.refTxt;
      el.big.textContent = s.big; el.bigu.textContent = s.unit; el.basis.textContent = s.basis; el.text.textContent = s.text;
      el.chips.innerHTML = s.chip ? '<a class="chip" href="#n-' + s.chip[0] + '" data-open="' + s.chip[0] + '">' + s.chip[1] + '</a>' : '';
      if (el.fig) {
        el.fig.classList.toggle('none', !s.img);
        if (s.img && el.img) { el.img.src = s.img; el.img.alt = s.alt; var cs = el.cap.querySelector('.cs'), cr = el.cap.querySelector('.cr'); if (cs) cs.textContent = s.cap; if (cr) cr.textContent = s.cred; }
      }
      fitCard();
    }
    // ---- 卡片放不下时：上沿最高到 HUD 下沿以下 24 px；照片先按 CSS 收矮（最矮 96 px），还不够就依次收起底图一行、照片、口径行；正文从不截断
    function cardOver() {
      var lim = card.clientHeight - 16, kids = card.children;
      for (var i = 0; i < kids.length; i++) { var c = kids[i]; if (!c.offsetHeight) continue; if (c.offsetTop + c.offsetHeight > lim + 1 || (c.classList.contains('tlph') && c.scrollHeight > c.offsetHeight + 1)) return true; }
      return false;
    }
    function fitCard() {
      card.classList.remove('fit1', 'fit2', 'fit3');
      if (getComputedStyle(card).position === 'absolute') { var mh = Math.floor(card.getBoundingClientRect().bottom - hud.getBoundingClientRect().bottom - 24); card.style.maxHeight = mh >= 160 ? mh + 'px' : ''; }
      else card.style.maxHeight = '';
      if (!card.clientHeight) return;
      if (cardOver()) card.classList.add('fit1'); if (cardOver()) card.classList.add('fit2'); if (cardOver()) card.classList.add('fit3');
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitCard);
    function showStep(k) {
      if (k === shownStep) return; var first = shownStep < 0; shownStep = k;
      if (first || RM.on) { fillCard(k); return; }
      clearTimeout(swapT); card.classList.add('swapping');
      swapT = setTimeout(function () { fillCard(k); card.classList.remove('swapping'); }, 160);
    }
    $$('.tlhd, .tlbig, .tlbasis, .tltext, .tlchips, .tlph', card).forEach(function (n) { n.classList.add('swap'); });
    // ---- 表盘：一个弹簧把十二只表的指针从当前角度转到新的时刻
    var dialFrom = {}, dialTo = {}, dialNow = {};
    function setHands(cid, m) {
      var r = rows[cid]; if (!r) return; dialNow[cid] = m;
      var hm = ((m % 720) + 720) % 720, mm = ((m % 60) + 60) % 60;
      r.hh.setAttribute('transform', 'rotate(' + (hm / 2).toFixed(2) + ' 50 50)'); r.mh.setAttribute('transform', 'rotate(' + (mm * 6).toFixed(2) + ' 50 50)');
    }
    var dialSp = new Spring({ from: 1, damping: 1, response: 0.5, eps: 0.002, onUpdate: function (u) { Object.keys(dialTo).forEach(function (cid) { setHands(cid, dialFrom[cid] + (dialTo[cid] - dialFrom[cid]) * u); }); } });
    function dialsTo(k, instant) {
      var s = STEPS[k];
      ORDER.forEach(function (cid) { var c = s.cities[cid]; dialFrom[cid] = dialNow[cid] == null ? 720 + c.off : dialNow[cid]; dialTo[cid] = 720 + c.off; });
      if (instant) dialSp.set(1); else { dialSp.set(0); dialSp.to(1); }
    }
    function updateRows(k, instant) {
      var s = STEPS[k], firstChg = null;
      ORDER.forEach(function (cid) {
        var c = s.cities[cid], r = rows[cid]; if (!r) return;
        var m = ((720 + c.off) % 1440 + 1440) % 1440;
        r.time.textContent = c.time; r.plate.textContent = c.plate; r.sub.textContent = c.sub; r.el.title = c.label;
        r.dial.classList.toggle('night', m < 360 || m >= 1080);
        r.el.classList.toggle('chg', !!c.changed);
        if (c.changed && !firstChg) firstChg = r.el;
        if (c.changed && !instant && !RM.on) { r.el.classList.remove('flip'); void r.el.offsetWidth; r.el.classList.add('flip'); }
        if (dots[cid]) dots[cid].classList.toggle('on', !!c.changed);
      });
      dialsTo(k, instant);
      // 窄屏：十二城是横向一条，把这一步第一座有变化的城滑进来
      if (panel && firstChg && panel.scrollWidth > panel.clientWidth + 4) {
        var left = firstChg.offsetLeft - 16; if (Math.abs(panel.scrollLeft - left) > 4) panel.scrollTo({ left: Math.max(0, left), behavior: RM.on || instant ? 'auto' : 'smooth' });
      }
    }
    // ---- 渲染一个 t
    var curK = -1, lastLab = 0, labTimer = 0, curT = null;
    function litOf(k) { return Object.keys(STEPS[k].cities).filter(function (cid) { return STEPS[k].cities[cid].changed; }); }
    function render(t, force) {
      curT = t;
      var k = clamp(Math.round(t), 0, N - 1), s = STEPS[k];
      if (k !== curK) {
        var instant = curK < 0; curK = k;
        el.jk.textContent = s.kicker; el.jyear.innerHTML = s.year + '<small>' + s.refTxt + ' · 格林尼治正午</small>'; el.jt.textContent = s.title;
        showStep(k); updateRows(k, instant);
        if (gmt) { gmt.classList.toggle('on', !!s.gmt); gmtl.classList.toggle('on', !!s.gmt); }
        marks.forEach(function (m) { m.classList.toggle('on', parseInt(m.getAttribute('data-step'), 10) === k); });
        ruler.setAttribute('aria-valuenow', k); ruler.setAttribute('aria-valuetext', s.year + ' 年：' + s.title);
      }
      setSun(t);
      var v = RM.on ? frames[k] : vbAt(t);
      if (blendFrom && blendU < 1) { var o = RM.on ? blendFrom[k] : vbAt(t, blendFrom); v = v.map(function (n, i) { return o[i] + (n - o[i]) * blendU; }); }
      setVB(v);
      head.style.transform = 'translateX(' + (t / (N - 1) * track.clientWidth).toFixed(1) + 'px)';
      var now = performance.now(), lit = litOf(k);
      if (now - lastLab > 120) { lastLab = now; placeLabels(v, lit); }
      clearTimeout(labTimer); labTimer = setTimeout(function () { placeLabels(lastVB, litOf(curK)); }, 140);
    }
    // ---- t 是一个弹簧：滚动给目标（轻微平滑），拖动直接设，松手按速度投影后吸附到最近的一步
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
    if ('ResizeObserver' in window) { var ro0 = null; new ResizeObserver(function () { var sz = scene.clientWidth + 'x' + scene.clientHeight; if (ro0 && sz !== ro0) reframe(true); ro0 = sz; }).observe(scene); }
    var rz = 0;
    function relayout() { layout(); var t = mode === 'scroll' ? tFromScroll() : ts.x; ts.set(t); render(t, true); fitCard(); }
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(relayout, 120); });
    window.addEventListener('load', relayout);
    layout(); ts.set(tFromScroll());
  })();

  /* ================= 节点列表：透镜分组（FLIP 补间）+ 行内展开 ================= */
  (function initLists() {
    var allRows = {};
    $$('.lrow').forEach(function (r) { allRows[r.getAttribute('data-id')] = r; });
    function toggle(r, open) { var o = open == null ? !r.classList.contains('open') : open; r.classList.toggle('open', o); var b = $('.lhead', r); if (b) b.setAttribute('aria-expanded', String(o)); }
    document.addEventListener('click', function (e) { var b = e.target.closest('.lhead'); if (!b) return; toggle(b.closest('.lrow')); });
    function scrollToRow(r) {
      var w = r.closest('.lwrap'), lb = w ? $('.lensbar', w) : null, off = navH() + (lb ? lb.offsetHeight : 0) + 8, top = r.getBoundingClientRect().top + window.scrollY - off;
      window.scrollTo({ top: Math.max(0, top), behavior: RM.on ? 'auto' : 'smooth' });
    }
    LAMPS.open = function (id) {
      var r = allRows[id]; if (!r) return;
      toggle(r, true); scrollToRow(r);
      r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1400);
      try { history.replaceState(null, '', '#n-' + id); } catch (er) {}
    };
    $$('.lwrap[data-lw]').forEach(function (w) {
      var key = w.getAttribute('data-lw'), groups = (D.lens || {})[key], lensEl = $('.lens', w), grid = $('.lgrid', w), note = $('.lensnote', w);
      if (!groups || !lensEl || !grid) return;
      var rows = {}; $$('.lrow', grid).forEach(function (r) { rows[r.getAttribute('data-id')] = r; });
      var tabs = $$('button[data-lens]', lensEl), cur = 'era', total = Object.keys(rows).length;
      var pill = document.createElement('span'); pill.className = 'pill'; lensEl.insertBefore(pill, lensEl.firstChild);
      var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
      var pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
      function movePill(instant) { var b = tabs.filter(function (t) { return t.getAttribute('data-lens') === cur; })[0]; if (!b) return; var x = b.offsetLeft, wd = b.offsetWidth; if (instant) { px.set(x); pw.set(wd); } else { px.to(x); pw.to(wd); } }
      function header(g) { var h = document.createElement('div'); h.className = 'lgh'; h.setAttribute('data-g', g.k); h.innerHTML = '<b>' + g.label + '</b><small>' + g.ids.length + ' 行</small>'; return h; }
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
    var m = /^#n-([\w-]+)$/.exec(location.hash || ''); if (m && allRows[m[1]]) setTimeout(function () { LAMPS.open(m[1]); }, 60);
  })();
})();
