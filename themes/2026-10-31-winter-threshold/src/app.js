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
  // Apple 的两参数弹簧：阻尼比 z（1 = 临界阻尼，不回弹）+ response T（秒）。k = (2π/T)²，c = 2zω。永远从当前值出发，可随时改目标，松手时可带初速度。
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
  window.YZ.Spring = Spring; window.YZ.VTrack = VTrack; window.YZ.project = project;
  // 触屏拖动的方向判定：先看前 6 px 往哪走，横向才接管（竖向交给页面滚动）
  function dragIntent(e, sx, sy) { var dx = e.clientX - sx, dy = e.clientY - sy; if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return 0; return Math.abs(dx) > Math.abs(dy) ? 1 : -1; }

  /* ================= 深浅色：这一题默认是夜；用户切过就记住 ================= */
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') || 'dark', next = cur === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next);
    try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
  });

  /* ================= 太阳：昼长（小时）、日落（分钟，经度 0° 平太阳时）。与 sun.py 同公式 ================= */
  var RAD = Math.PI / 180;
  function declEqt(doy) { var g = 2 * Math.PI / 365 * (doy - 1); return { decl: 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g), eqt: 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g)) }; }
  function dayLen(lat, doy) { var d = declEqt(doy).decl, c = Math.cos(90.833 * RAD) / (Math.cos(lat * RAD) * Math.cos(d)) - Math.tan(lat * RAD) * Math.tan(d); if (c >= 1) return 0; if (c <= -1) return 24; return 2 * Math.acos(c) / RAD / 15; }
  function sunset(lat, doy) { var e = declEqt(doy), c = Math.cos(90.833 * RAD) / (Math.cos(lat * RAD) * Math.cos(e.decl)) - Math.tan(lat * RAD) * Math.tan(e.decl); if (c >= 1 || c <= -1) return null; var ha = Math.acos(c) / RAD; return 720 + 4 * ha - e.eqt; }
  function hm(h) { var H = Math.floor(h), M = Math.round((h - H) * 60); if (M === 60) { H++; M = 0; } return H + ' 小时 ' + (M < 10 ? '0' : '') + M + ' 分'; }
  function mm(m) { m = ((m % 1440) + 1440) % 1440; var H = Math.floor(m / 60), M = Math.round(m % 60); if (M === 60) { H++; M = 0; } return (H < 10 ? '0' : '') + H + ':' + (M < 10 ? '0' : '') + M; }
  var MD = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  function doyToMd(doy, y) { var md = MD.slice(); if (y && ((y % 4 === 0 && y % 100 !== 0) || y % 400 === 0)) md[1] = 29; var m = 0; while (m < 11 && doy > md[m]) { doy -= md[m]; m++; } return { m: m + 1, d: doy }; }
  function isoDoy(iso) { var p = iso.split('-').map(Number), t = 0; for (var i = 0; i < p[1] - 1; i++) t += MD[i]; return t + p[2]; }
  var WDN = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  function wdOfDoy(doy) { var m = doyToMd(doy, 2026); return WDN[new Date(Date.UTC(2026, m.m - 1, m.d)).getUTCDay()]; }
  function latTxt(v) { v = Math.round(v); return v > 0 ? '北纬 ' + v + '°' : v < 0 ? '南纬 ' + (-v) + '°' : '赤道'; }
  window.YZ.sun = { dayLen: dayLen, sunset: sunset, hm: hm, mm: mm, doyToMd: doyToMd, isoDoy: isoDoy, latTxt: latTxt };

  /* ================= 入场 ================= */
  var fades = $$('.fade');
  if ('IntersectionObserver' in window && !RM.on) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else { fades.forEach(function (el) { el.classList.add('in'); }); }

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

  /* ================= 灯谱的公开接口（田野、序章、年轮、证据都会调） ================= */
  var LAMPS = { open: function () {}, lens: function () {} };
  window.YZ.lamps = LAMPS;
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('[data-open]'); if (!a || a.closest('[data-sup]')) return;
    var id = a.getAttribute('data-open'); if (!id || !document.getElementById('n-' + id)) return;
    ev.preventDefault(); LAMPS.open(id, a.getAttribute('data-lens'));
  });

  /* ================= 卷首 · 夜的田野：一条可拖的竖线 ================= */
  (function initField() {
    var fbox = $('#fieldbox'), cv = $('#fcv'), fov = $('#fov'), ftip = $('#ftip'), fread = $('#fread');
    if (!fbox || !fov) return;
    var FW = 1200, FH = 520, FL = 58, FR = 16, FT = 16, FB = 30, LAT0 = 62, LAT1 = -36, DOY0 = 274, DOY1 = 365, FSM = false;
    var FKEY = ['samhain', 'halloween', 'dia-de-muertos', 'bonfire-night', 'lidong', 'diwali', 'hanyi', 'lucia', 'loy-krathong', 'thanksgiving', 'martinmas', 'todos-santos-andes'];
    var placed = [], lampEls = [], lampElDoy = [], scrub = null, readLat = 40;
    var lampDoys = D.field.map(function (f) { return isoDoy(f.date); });
    function fieldSize() { var bw = fbox.clientWidth || 1200, sm = bw < 700; FSM = sm; FW = sm ? 720 : 1200; FH = sm ? 600 : 520; FL = sm ? 64 : 58; FB = sm ? 34 : 30; if (cv) { cv.width = FW; cv.height = FH; } fov.setAttribute('viewBox', '0 0 ' + FW + ' ' + FH); fbox.classList.toggle('sm', sm); }
    function fx(doy) { return FL + (doy - DOY0) / (DOY1 - DOY0) * (FW - FL - FR); }
    function fy(lat) { return FT + (LAT0 - lat) / (LAT0 - LAT1) * (FH - FT - FB); }
    function xdoy(x) { return DOY0 + (x - FL) / (FW - FL - FR) * (DOY1 - DOY0); }
    function ylat(y) { return LAT0 + (y - FT) / (FH - FT - FB) * (LAT1 - LAT0); }
    function hex(h) { h = h.trim().replace('#', ''); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
    function drawField() {
      if (!cv) return;
      var cs = getComputedStyle(fbox), a = hex(cs.getPropertyValue('--night-0')), b = hex(cs.getPropertyValue('--night-1')), c = hex(cs.getPropertyValue('--day')), s = hex(cs.getPropertyValue('--surface'));
      var ctx = cv.getContext('2d'), img = ctx.createImageData(FW, FH), dat = img.data, cols = [];
      for (var x = 0; x < FW; x++) cols.push(DOY0 + (DOY1 - DOY0) * ((x - FL) / (FW - FL - FR)));
      for (var y = 0; y < FH; y++) {
        var lat = LAT0 + (LAT1 - LAT0) * ((y - FT) / (FH - FT - FB)), inY = y >= FT && y <= FH - FB;
        for (var x2 = 0; x2 < FW; x2++) {
          var col; if (!inY || x2 < FL || x2 > FW - FR) col = s;
          else { var n = 1 - dayLen(lat, cols[x2]) / 24, t = clamp((n - 0.38) / (0.70 - 0.38), 0, 1); col = t < .5 ? [c[0] + (b[0] - c[0]) * t * 2, c[1] + (b[1] - c[1]) * t * 2, c[2] + (b[2] - c[2]) * t * 2] : [b[0] + (a[0] - b[0]) * (t - .5) * 2, b[1] + (a[1] - b[1]) * (t - .5) * 2, b[2] + (a[2] - b[2]) * (t - .5) * 2]; }
          var i = (y * FW + x2) * 4; dat[i] = col[0]; dat[i + 1] = col[1]; dat[i + 2] = col[2]; dat[i + 3] = 255;
        }
      }
      ctx.putImageData(img, 0, 0);
    }
    function build() {
      fieldSize(); drawField();
      var s = '', LF = FSM ? 17 : 12, LS = LF + 3; placed = [];
      [8, 10, 12, 14].forEach(function (hrs) {
        var pts = [];
        for (var x = FL; x <= FW - FR; x += 6) { var doy = xdoy(x), best = null, bd = 9; for (var lat = LAT0; lat >= LAT1; lat -= 0.5) { var d = Math.abs(dayLen(lat, doy) - hrs); if (d < bd) { bd = d; best = lat; } } if (best !== null && bd < 0.12) pts.push([x, fy(best)]); }
        if (pts.length > 2) s += '<polyline class="iso" points="' + pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ') + '"/><text class="isol" x="' + (pts[pts.length - 1][0] - 4) + '" y="' + (pts[pts.length - 1][1] - 5) + '" text-anchor="end">白昼 ' + hrs + ' 小时</text>';
      });
      [60, 40, 20, 0, -20].forEach(function (lat) { s += '<text class="ax" x="' + (FL - 8) + '" y="' + (fy(lat) + 4).toFixed(1) + '" text-anchor="end">' + latTxt(lat) + '</text>'; });
      [[274, '10 月 1 日'], [305, '11 月 1 日'], [335, '12 月 1 日']].forEach(function (m) { s += '<text class="ax" x="' + fx(m[0]).toFixed(1) + '" y="' + (FH - 10) + '" text-anchor="middle">' + m[1] + '</text>'; });
      s += '<rect class="win" x="' + fx(304).toFixed(1) + '" y="' + FT + '" width="' + (fx(313) - fx(304)).toFixed(1) + '" height="' + (FH - FT - FB) + '"/>';
      s += '<text class="lab s" x="' + (fx(304) + 4).toFixed(1) + '" y="' + (FT + 14) + '">这十天</text>';
      s += '<text class="ftitle" x="' + (FL + 16) + '" y="' + (FT + (FSM ? 40 : 46)) + '">冬天的门槛</text><text class="fsub" x="' + (FL + 17) + '" y="' + (FT + (FSM ? 64 : 70)) + '">这些节日的夜与灯 · 2026 年 10–12 月</text>';
      placed.push({ x: FL + 10, y: FT + 20, w: FSM ? 330 : 300, h: FSM ? 56 : 60 });
      var items = D.field.slice().sort(function (p, q) { return isoDoy(p.date) - isoDoy(q.date) || q.lat - p.lat; });
      items.forEach(function (f, i) {
        var show = !FSM || FKEY.indexOf(f.id) >= 0, x = fx(isoDoy(f.date)), y = fy(f.lat), w = show ? f.name.length * LF + 6 : 0, flip = x + 9 + w > FW - 8, lx = flip ? x - 9 - w : x + 9, ly = y + 4;
        if (show) { for (var k = 0; k < 12; k++) { var clash = placed.some(function (p) { return ly - LF < p.y + (p.h || LS) - 2 && ly > p.y - 2 && lx < p.x + p.w && lx + w > p.x; }); if (!clash) break; ly += LS; } placed.push({ x: lx, y: ly - LF, w: w, h: LS }); }
        s += '<g class="lg" data-fid="' + f.id + '"' + (f.node ? ' data-open="' + f.node + '" role="link"' : '') + ' style="opacity:0;animation:lit .45s ' + (0.3 + i * 0.06).toFixed(2) + 's forwards"><circle class="halo" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="9"/><circle class="lampd" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="3.6"/>' + (ly !== y + 4 ? '<line x1="' + (x + 4).toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + (flip ? lx + w : lx).toFixed(1) + '" y2="' + (ly - 4) + '" stroke="#F3EDDE" stroke-opacity=".45" stroke-width="1"/>' : '') + (show ? '<text class="lab" x="' + lx.toFixed(1) + '" y="' + ly + '">' + f.name + '</text>' : '') + '</g>';
      });
      s += '<g class="fscrub" id="fscrub"><line class="fs-glow" y1="' + FT + '" y2="' + (FH - FB) + '"/><line class="fs-line" y1="' + FT + '" y2="' + (FH - FB) + '"/><circle class="fs-dot" r="5"/><rect class="fs-knob" width="14" height="22" rx="7"/><text class="fs-date"></text></g>';
      fov.innerHTML = s;
      lampEls = $$('.lg', fov); lampElDoy = lampEls.map(function (g) { var f = D.field.filter(function (x) { return x.id === g.getAttribute('data-fid'); })[0]; return f ? isoDoy(f.date) : -99; }); scrub = { g: $('#fscrub', fov), lines: $$('#fscrub line', fov), dot: $('.fs-dot', fov), knob: $('.fs-knob', fov), date: $('.fs-date', fov) };
      render(sp.x);
    }
    var st = document.createElement('style'); st.textContent = '@keyframes lit{to{opacity:1}}'; document.head.appendChild(st);
    // 竖线的位置是一个弹簧（单位：年内序日）
    var sp = new Spring({ from: 304, damping: 1, response: 0.38, eps: 0.004, onUpdate: function (x) { render(x); } });
    function render(doy) {
      if (!scrub) return;
      var x = fx(doy), d = Math.round(doy), md = doyToMd(d, 2026), dl = dayLen(readLat, d);
      scrub.lines.forEach(function (l) { l.setAttribute('x1', x.toFixed(1)); l.setAttribute('x2', x.toFixed(1)); });
      scrub.dot.setAttribute('cx', x.toFixed(1)); scrub.dot.setAttribute('cy', fy(readLat).toFixed(1));
      scrub.knob.setAttribute('x', (x - 7).toFixed(1)); scrub.knob.setAttribute('y', (FH - FB - 11).toFixed(1));
      // 竖线底部的日期：默认放右边；撞上灯的标签（比如 10/31 悉尼的万圣节）就换到左边
      var dtxt = md.m + '/' + md.d, dw = dtxt.length * (FSM ? 11.5 : 8.6) + 2, dh = FSM ? 20 : 15, dy = FH - FB - (FSM ? 8 : 6), dtop = dy - dh + 3;
      var hit = function (x0) { return placed.some(function (p) { return dtop < p.y + (p.h || 15) && dtop + dh > p.y && x0 < p.x + p.w && x0 + dw > p.x; }); };
      var canR = x + 11 + dw < FW - FR, canL = x - 11 - dw > FL, right = canR && (!hit(x + 11) || !canL || hit(x - 11 - dw));
      scrub.date.setAttribute('x', (right ? x + 11 : x - 11).toFixed(1)); scrub.date.setAttribute('text-anchor', right ? 'start' : 'end'); scrub.date.setAttribute('y', dy.toFixed(1)); scrub.date.textContent = dtxt;
      lampEls.forEach(function (g, i) { g.classList.toggle('near', Math.abs(lampElDoy[i] - doy) <= 1.5); });
      // 读数：那天、那条纬线的昼长；当天或最近的灯
      var today = D.field.filter(function (f) { return isoDoy(f.date) === d; }), next = null, gap = 99;
      if (!today.length) D.field.forEach(function (f) { var g = isoDoy(f.date) - d; if (g > 0 && g < gap) { gap = g; next = f; } });
      fread.innerHTML = '<b>' + md.m + ' 月 ' + md.d + ' 日 · ' + wdOfDoy(d) + '</b><span class="fr-dl">' + latTxt(readLat) + '：昼长 ' + hm(dl) + '</span>' +
        '<span class="fr-l">' + (today.length ? '这一天：' + today.map(function (f) { return f.name; }).join(' · ') : next ? '下一盏：' + next.name + '（还有 ' + gap + ' 天）' : '之后没有本页收录的节日') + '</span>';
      placeRead(x);
      fbox.setAttribute('aria-valuenow', d); fbox.setAttribute('aria-valuetext', md.m + ' 月 ' + md.d + ' 日，' + latTxt(readLat) + ' 昼长 ' + hm(dl));
    }
    // 读数框：贴着竖线，躲开灯的标签（像素）
    function placeRead(x) {
      var bw = fbox.clientWidth, sc = bw / FW, w = fread.offsetWidth || 224, h = fread.offsetHeight || 74;
      var px = x * sc + 14; if (px + w > bw - 8) px = x * sc - 14 - w; px = clamp(px, 6, bw - w - 6);
      var cands = FSM ? [0.70, 0.86, 0.5] : [0.62, 0.78, 0.44, 0.2], best = cands[0], bestHit = 1e9;
      cands.forEach(function (fr) {
        var py = fr * fbox.clientHeight - h / 2, hit = 0;
        placed.forEach(function (p) { var ox = Math.max(0, Math.min(px + w, (p.x + p.w) * sc) - Math.max(px, p.x * sc)), oy = Math.max(0, Math.min(py + h, (p.y + (p.h || 15)) * sc) - Math.max(py, p.y * sc)); hit += ox * oy; });
        if (hit < bestHit - 1) { bestHit = hit; best = fr; }
      });
      fread.style.left = Math.round(px) + 'px'; fread.style.top = Math.round(clamp(best * fbox.clientHeight - h / 2, 6, fbox.clientHeight - h - 6)) + 'px'; fread.classList.add('on');
    }
    // 拖动：鼠标按下即跳到指针处；触屏先判方向，横向才接管
    var vt = new VTrack(), drag = null;
    function ptr(e) { var r = fbox.getBoundingClientRect(), sc = FW / r.width; return { doy: clamp(xdoy((e.clientX - r.left) * sc), DOY0, DOY1), lat: clamp(ylat((e.clientY - r.top) * sc), LAT1, LAT0) }; }
    fbox.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return;
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: e.pointerType === 'mouse', moved: false, lamp: e.target.closest('.lg') };
      if (drag.on) start(e);
    });
    function start(e) {
      drag.on = true; try { fbox.setPointerCapture(drag.id); } catch (er) {}
      var p = ptr(e); readLat = Math.round(p.lat); vt.reset(); vt.add(p.doy); sp.set(p.doy); ftip.style.display = 'none';
    }
    fbox.addEventListener('pointermove', function (e) {
      if (!drag) { if (e.pointerType === 'mouse') hover(e); return; }
      if (e.pointerId !== drag.id) return;
      if (!drag.on) { var it = dragIntent(e, drag.sx, drag.sy); if (it === 1) start(e); else if (it === -1) { drag = null; } return; }
      if (Math.abs(e.clientX - drag.sx) > 4) drag.moved = true;
      var p = ptr(e); readLat = Math.round(p.lat); vt.add(p.doy); sp.set(p.doy);
    });
    function end(e, cancel) {
      if (!drag || e.pointerId !== drag.id) return;
      var d0 = drag; drag = null; if (!d0.on) return;
      if (d0.moved) { fbox.setAttribute('data-sup', '1'); setTimeout(function () { fbox.removeAttribute('data-sup'); }, 0); }
      if (!d0.moved && d0.lamp && !cancel) { sp.to(Math.round(sp.x)); return; }
      var v = vt.v(), proj = clamp(sp.x + project(v, 0.995), DOY0, DOY1), target = Math.round(proj);
      // 吸附：投影点 3 天内有灯就停在灯上
      var near = null, nd = 3.01; lampDoys.forEach(function (ld) { var dd = Math.abs(ld - proj); if (dd < nd) { nd = dd; near = ld; } });
      if (near !== null && (Math.abs(v) > 3 || nd <= 0.8)) target = near;
      sp.to(target, { velocity: v, damping: 1, response: 0.4 });
    }
    fbox.addEventListener('pointerup', function (e) { end(e, false); });
    fbox.addEventListener('pointercancel', function (e) { end(e, true); });
    function hover(e) {
      var g = e.target.closest('.lg'); if (!g) { ftip.style.display = 'none'; return; }
      var f = D.field.filter(function (x) { return x.id === g.getAttribute('data-fid'); })[0]; if (!f) return;
      var r = fbox.getBoundingClientRect(); ftip.innerHTML = '<b>' + f.name + '</b>' + f.city + ' · ' + latTxt(f.lat) + ' · ' + f.date.slice(5).replace('-', '/') + '<br>当天昼长 ' + hm(dayLen(f.lat, isoDoy(f.date))) + ' · ' + f.rule + (f.node ? '<br>点一下打开它在灯谱里的那一行' : '');
      ftip.style.display = 'block'; var tx = e.clientX - r.left + 14, ty = e.clientY - r.top + 14; if (tx > r.width - 270) tx = e.clientX - r.left - 274; ftip.style.left = tx + 'px'; ftip.style.top = ty + 'px';
    }
    fbox.addEventListener('mouseleave', function () { ftip.style.display = 'none'; });
    fbox.addEventListener('keydown', function (e) {
      var k = e.key, d = Math.round(sp.target);
      if (k === 'ArrowRight') d += 1; else if (k === 'ArrowLeft') d -= 1; else if (k === 'PageUp') d += 7; else if (k === 'PageDown') d -= 7; else if (k === 'Home') d = DOY0; else if (k === 'End') d = DOY1;
      else if (k === 'ArrowUp' || k === 'ArrowDown') { readLat = clamp(readLat + (k === 'ArrowUp' ? 5 : -5), LAT1, LAT0); render(sp.x); e.preventDefault(); return; }
      else if (k === 'Enter') { var hit = D.field.filter(function (f) { return isoDoy(f.date) === d && f.node; })[0]; if (hit) LAMPS.open(hit.node); return; }
      else return;
      e.preventDefault(); sp.to(clamp(d, DOY0, DOY1));
    });
    build();
    var fsz = 0; window.addEventListener('resize', function () { clearTimeout(fsz); fsz = setTimeout(function () { var sm = (fbox.clientWidth || 1200) < 700; if (sm !== FSM) build(); else render(sp.x); }, 150); });
  })();

  /* ================= 序章 · 这十天：全屏时间轴（滚动与刻度尺是同一个量 t） ================= */
  (function initTimeline() {
    var pin = $('#tlpin'), stg = $('#tlstage'); if (!pin || !stg || !D.stage) return;
    var S = D.stage, N = S.n, DAYS = S.days, STEPS = S.steps;
    var wmap = $('#wmap'), scene = $('#jscene'), hud = $('#jhud'), card = $('#tlcard'), band = $('#dayband'), bandBtn = $('#tlbtn'), ruler = $('#tlruler'), track = $('#rtrack'), head = $('#rhead');
    var el = { jk: $('#jk'), jdate: $('#jdate'), jt: $('#jt'), no: $('#tlno'), kick: $('#tlkick'), title: $('#tltitle'), big: $('#tlbig'), bigu: $('#tlbigu'), basis: $('#tlbasis'), text: $('#tltext'), chips: $('#tlchips'), img: $('#tlimg'), cap: $('#tlcap') };
    var dots = {}, rows = {}, marks = $$('.rmark', ruler), bands = $$('.wmap .nb', stg);
    $$('.cdot', stg).forEach(function (d) { dots[d.getAttribute('data-city')] = d; });
    $$('.dbrow', stg).forEach(function (r) { rows[r.getAttribute('data-city')] = r; });
    var stepDays = STEPS.map(function (s) { return s.day; });
    var litBefore = []; (function () { var acc = {}; for (var i = 0; i < N; i++) { litBefore.push(Object.assign({}, acc)); DAYS[i].lit.forEach(function (c) { acc[c] = 1; }); } })();
    function toH(t) { var p = t.split(':'); return parseInt(p[0], 10) + parseInt(p[1], 10) / 60; }
    function shortHm(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + 'h' + ('0' + (m % 60)).slice(-2) + 'm'; }
    function stepAtOrBefore(di) { var k = 0; for (var i = 0; i < STEPS.length; i++) if (STEPS[i].day <= di) k = i; return k; }
    // ---- 长度：每天约 0.42 屏
    var stageH = 0, perDay = 0, pinTop = 0;
    function layout() {
      stageH = stg.offsetHeight; perDay = Math.round(window.innerHeight * (window.innerWidth < 700 ? 0.36 : 0.42));
      pin.style.height = (stageH + (N - 1) * perDay) + 'px';
      pinTop = pin.getBoundingClientRect().top + window.scrollY;
      frames = STEPS.map(function (s) { return frameFor(s.cities); });
    }
    function freeRect() {
      var sr = scene.getBoundingClientRect(), W = sr.width, H = sr.height, r = { x0: 14, x1: W - 14, y0: 14, y1: H - 14 }, hb = hud.getBoundingClientRect();
      r.y0 = Math.max(r.y0, hb.bottom - sr.top + 10);
      if (window.innerWidth >= 981) {
        var cb = card.getBoundingClientRect(), rb = ruler.getBoundingClientRect();
        r.x0 = cb.right - sr.left + 26; r.y1 = rb.top - sr.top - 18;
        if (band && !band.hidden) { var bb = band.getBoundingClientRect(); r.x1 = bb.left - sr.left - 22; }
      }
      if (r.x1 - r.x0 < 160) r.x0 = Math.max(14, r.x1 - 160);
      if (r.y1 - r.y0 < 140) r.y0 = Math.max(14, r.y1 - 140);
      return { W: W, H: H, r: r };
    }
    function tFromScroll() { return clamp((window.scrollY - (pinTop - navH())) / perDay, 0, N - 1); }
    function scrollForT(t) { return pinTop - navH() + t * perDay; }
    // ---- 镜头：把这一步点亮的城框进来；相邻两步之间按 t 插值
    var frames = [];
    function frameFor(ids) {
      var F = freeRect(), W = F.W || 720, H = F.H || 360, r = F.r, xs = [], ys = [];
      ids.forEach(function (id) { var c = D.cities[id]; if (c) { xs.push((c.lon + 180) * 2); ys.push((90 - c.lat) * 2); } });
      if (!xs.length) return [0, 0, 720, 720 * H / W];
      var padX = 36, padY = 26, minx = Math.min.apply(null, xs) - padX, maxx = Math.max.apply(null, xs) + padX, miny = Math.min.apply(null, ys) - padY, maxy = Math.max.apply(null, ys) + padY;
      var fw = r.x1 - r.x0, fh = r.y1 - r.y0, minW = W < 700 ? 150 : 230;
      var ppu = Math.min(fw / (maxx - minx), fh / (maxy - miny), W / minW);
      ppu = Math.max(ppu, W / 1100); // 最远也不缩到一屏看三个世界那么小
      var w = W / ppu, h = H / ppu, cxu = (minx + maxx) / 2, cyu = (miny + maxy) / 2;
      var x = cxu - ((r.x0 + r.x1) / 2) / ppu, y = cyu - ((r.y0 + r.y1) / 2) / ppu;
      // 能不露出地图外的暗处就不露：先按「地图铺满」收，再收回到「灯都在空处」的可行区间里
      var xlo = maxx - r.x1 / ppu, xhi = minx - r.x0 / ppu, ylo = maxy - r.y1 / ppu, yhi = miny - r.y0 / ppu;
      var xm = w <= 720 ? clamp(x, 0, 720 - w) : (720 - w) / 2, ym = h <= 360 ? clamp(y, 0, 360 - h) : (360 - h) / 2;
      x = xlo <= xhi ? clamp(xm, xlo, xhi) : x; y = ylo <= yhi ? clamp(ym, ylo, yhi) : y;
      return [x, y, w, h];
    }
    var blendFrom = null, blendU = 1;
    var blendSp = new Spring({ from: 1, damping: 1, response: 0.45, eps: 0.002, onUpdate: function (u) { blendU = u; if (curT !== null) render(curT, true); }, onRest: function () { blendFrom = null; } });
    function reframe(animated) { var old = frames; frames = STEPS.map(function (s) { return frameFor(s.cities); }); if (animated && old.length && !RM.on) { blendFrom = old; blendSp.set(0); blendSp.to(1); } else if (curT !== null) render(curT, true); }
    if (bandBtn && band) bandBtn.addEventListener('click', function () { var open = band.hidden; band.hidden = !open; bandBtn.setAttribute('aria-expanded', String(open)); reframe(true); });
    function vbAt(t, fr) {
      fr = fr || frames;
      var k0 = 0, k1 = STEPS.length - 1;
      for (var i = 0; i < STEPS.length; i++) { if (STEPS[i].day <= t) k0 = i; }
      for (var j = STEPS.length - 1; j >= 0; j--) { if (STEPS[j].day >= t) k1 = j; }
      if (k1 < k0) k1 = k0;
      var d0 = STEPS[k0].day, d1 = STEPS[k1].day, u = d1 > d0 ? smooth((t - d0) / (d1 - d0)) : 0, a = fr[k0], b = fr[k1];
      return [0, 1, 2, 3].map(function (i) { return a[i] + (b[i] - a[i]) * u; });
    }
    var lastVB = null;
    function setVB(v) {
      wmap.setAttribute('viewBox', v.map(function (n) { return n.toFixed(2); }).join(' '));
      var ppu = (scene.clientWidth || 720) / v[2], k = 1.1 / ppu;
      Object.keys(dots).forEach(function (id) { var d = dots[id]; d.setAttribute('transform', 'translate(' + d.getAttribute('data-x') + ' ' + d.getAttribute('data-y') + ') scale(' + k.toFixed(3) + ')'); });
      lastVB = v;
    }
    // ---- 标签避让（像素）：先给点亮的城找位置，再给其余；躲开 HUD、卡片、昼带与刻度尺
    function placeLabels(v, lit) {
      var W = scene.clientWidth || 720, H = scene.clientHeight || 360, ppu = W / v[2], sr = scene.getBoundingClientRect();
      function box(e) { if (!e || !e.offsetParent && e !== hud) return null; var r = e.getBoundingClientRect(); if (!r.width) return null; return { x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height }; }
      var taken = [box(hud), box(card), box(band), box(ruler)].filter(Boolean), pos = {};
      var nUI = taken.length;
      Object.keys(dots).forEach(function (id) { var d = dots[id]; var P = pos[id] = { x: (parseFloat(d.getAttribute('data-x')) - v[0]) * ppu, y: (parseFloat(d.getAttribute('data-y')) - v[1]) * ppu }; taken.push({ x: P.x - 5, y: P.y - 5, w: 10, h: 10 }); var under = taken.slice(0, nUI).some(function (q) { return P.x > q.x - 4 && P.x < q.x + q.w + 4 && P.y > q.y - 4 && P.y < q.y + q.h + 4; }); d.classList.toggle('under', under && lit.indexOf(id) < 0); });
      var order = lit.slice(); Object.keys(dots).forEach(function (id) { if (order.indexOf(id) < 0) order.push(id); });
      var DIRS = { t: [0, -9, 'middle'], b: [0, 15, 'middle'], r: [8, 4, 'start'], l: [-8, 4, 'end'] };
      order.forEach(function (id) {
        var d = dots[id], tx = d.querySelector('text'), n = tx.textContent.length, tw = n * 11.5 + 2, th = 13, p = pos[id], isLit = lit.indexOf(id) >= 0;
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
      el.no.textContent = ('0' + (k + 1)).slice(-2) + ' / ' + ('0' + STEPS.length).slice(-2); el.kick.textContent = s.kicker; el.title.textContent = s.title; el.text.textContent = s.text;
      el.chips.innerHTML = s.fest.map(function (f) { return '<a class="chip a" href="#n-' + f[0] + '" data-open="' + f[0] + '">' + f[1] + '</a>'; }).join('');
      if (el.img && s.img) { el.img.src = s.img; el.img.alt = s.alt; el.cap.textContent = s.cap; }
    }
    function showStep(k) {
      if (k === shownStep) return; var first = shownStep < 0; shownStep = k;
      if (first || RM.on) { fillCard(k); return; }
      clearTimeout(swapT); card.classList.add('swapping');
      swapT = setTimeout(function () { fillCard(k); card.classList.remove('swapping'); }, 160);
    }
    $$('.tlhd, .tltitle, .tlbig, .tlbasis, .tltext, .tlchips, .tlph', card).forEach(function (n) { n.classList.add('swap'); });
    // ---- 渲染一个 t
    var curDay = -1, lastLab = 0, labTimer = 0, curT = null;
    function render(t, force) {
      curT = t;
      var di = clamp(Math.round(t), 0, N - 1), day = DAYS[di], k = stepAtOrBefore(di), s = STEPS[k], onStep = day.step >= 0;
      if (di !== curDay) {
        curDay = di;
        var md = day.date.split('-');
        el.jdate.innerHTML = parseInt(md[1], 10) + ' 月 ' + parseInt(md[2], 10) + ' 日<small>' + day.wd + '</small>';
        el.jk.textContent = onStep ? STEPS[day.step].kicker : '这一天没有本页收录的节日';
        el.jt.textContent = onStep ? STEPS[day.step].title : '';
        showStep(onStep ? day.step : k); card.classList.toggle('empty', !onStep);
        var main = (onStep ? STEPS[day.step] : s).main, mc = day.cities[main], mcity = D.cities[main];
        el.big.textContent = hm(mc.dl); el.bigu.textContent = mcity.name_zh + ' · 昼长';
        el.basis.textContent = '日出 ' + mc.rise + '，日落 ' + mc.set + '（当地标准时，不含夏令时）· ' + latTxt(mcity.lat) + ' · ' + mcity.koppen;
        Object.keys(day.cities).forEach(function (cid) {
          var c = day.cities[cid], r = rows[cid], on = day.lit.indexOf(cid) >= 0;
          if (r) { var rs = toH(c.rise), ss = toH(c.set), bar = $('.dbb', r); bar.style.left = (rs / 24 * 100).toFixed(2) + '%'; bar.style.width = ((ss - rs) / 24 * 100).toFixed(2) + '%'; $('.dbv', r).textContent = shortHm(c.dl); r.title = D.cities[cid].name_zh + '：日出 ' + c.rise + '，日落 ' + c.set + '（当地标准时）'; r.classList.toggle('lit', on); r.classList.toggle('main', cid === main); $('.lamp', r).classList.toggle('off', !on); }
          if (dots[cid]) { dots[cid].classList.toggle('on', on); dots[cid].classList.toggle('was', !on && !!litBefore[di][cid]); }
        });
        marks.forEach(function (m) { m.classList.toggle('on', parseInt(m.getAttribute('data-step'), 10) === day.step); });
        ruler.setAttribute('aria-valuenow', di); ruler.setAttribute('aria-valuetext', parseInt(md[1], 10) + ' 月 ' + parseInt(md[2], 10) + ' 日' + (onStep ? ' ' + STEPS[day.step].label : ''));
      }
      var doy = 304 + t;
      bands.forEach(function (b) { var lat = parseFloat(b.getAttribute('data-lat')) - 5, n = 1 - dayLen(lat, doy) / 24; b.setAttribute('opacity', clamp((n - .42) * 1.9, 0, .75).toFixed(2)); });
      var v = RM.on ? frames[stepAtOrBefore(di)] : vbAt(t);
      if (blendFrom && blendU < 1) { var o = RM.on ? blendFrom[stepAtOrBefore(di)] : vbAt(t, blendFrom); v = v.map(function (n, i) { return o[i] + (n - o[i]) * blendU; }); }
      setVB(v);
      head.style.transform = 'translateX(' + (t / (N - 1) * track.clientWidth).toFixed(1) + 'px)';
      // 标签：移动中每 120 ms 排一次，停下再排一次
      var now = performance.now(), lit = DAYS[di].lit;
      if (now - lastLab > 120) { lastLab = now; placeLabels(v, lit); }
      clearTimeout(labTimer); labTimer = setTimeout(function () { placeLabels(lastVB, DAYS[curDay].lit); }, 140);
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
    // 刻度尺贴在视口底边时，把右下角的「夜 / 昼」按钮让到刻度尺上方，免得盖住最后一个刻度
    function tlOn() { var rr = ruler.getBoundingClientRect(); document.documentElement.classList.toggle('tl-on', rr.bottom > innerHeight - 64 && rr.top < innerHeight); }
    window.addEventListener('scroll', tlOn, { passive: true }); window.addEventListener('resize', tlOn); tlOn();
    ['wheel', 'touchstart'].forEach(function (ev) { window.addEventListener(ev, function () { if (mode === 'fly') mode = 'scroll'; }, { passive: true }); });
    function nearestStepDay(t) { var best = stepDays[0], bd = 1e9; stepDays.forEach(function (d) { var dd = Math.abs(d - t); if (dd < bd) { bd = dd; best = d; } }); return best; }
    function flyTo(t, v) { mode = 'fly'; progY = null; ts.to(clamp(t, 0, N - 1), { velocity: v || 0, damping: 1, response: 0.42 }); }
    // 刻度尺拖动
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
      if (!d0.on) { if (d0.mark && !cancel) flyTo(STEPS[parseInt(d0.mark.getAttribute('data-step'), 10)].day, 0); return; }
      if (!d0.moved && d0.mark) { flyTo(STEPS[parseInt(d0.mark.getAttribute('data-step'), 10)].day, 0); return; }
      var v = vt.v(); flyTo(nearestStepDay(clamp(ts.x + project(v, 0.995), 0, N - 1)), v);
    }
    ruler.addEventListener('pointerup', function (e) { endDrag(e, false); });
    marks.forEach(function (m) { m.addEventListener('click', function (e) { if (e.detail === 0) flyTo(STEPS[parseInt(m.getAttribute('data-step'), 10)].day, 0); }); });
    ruler.addEventListener('pointercancel', function (e) { endDrag(e, true); if (mode === 'drag') mode = 'scroll'; });
    ruler.addEventListener('keydown', function (e) {
      var di = Math.round(ts.target), t = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { for (var i = 0; i < stepDays.length; i++) if (stepDays[i] > di) { t = stepDays[i]; break; } }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { for (var j = stepDays.length - 1; j >= 0; j--) if (stepDays[j] < di) { t = stepDays[j]; break; } }
      else if (e.key === 'Home') t = 0; else if (e.key === 'End') t = N - 1; else return;
      e.preventDefault(); if (t !== null) flyTo(t, 0);
    });
    if ('ResizeObserver' in window) { var ro0 = null; new ResizeObserver(function () { var sz = scene.clientWidth + 'x' + scene.clientHeight; if (ro0 && sz !== ro0) reframe(true); ro0 = sz; }).observe(scene); }
    var rz = 0;
    function relayout() { layout(); var t = mode === 'scroll' ? tFromScroll() : ts.x; ts.set(t); curDay = -1; render(t); }
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(relayout, 120); });
    window.addEventListener('load', relayout);
    layout(); ts.set(tFromScroll());
  })();

  /* ================= 灯谱：透镜分组（FLIP 补间）+ 行内展开 ================= */
  (function initLamps() {
    var grid = $('#lgrid'), lensEl = $('#lens'); if (!grid || !lensEl) return;
    var rows = {}; $$('.lrow', grid).forEach(function (r) { rows[r.getAttribute('data-id')] = r; });
    var tabs = $$('button[data-lens]', lensEl), cur = 'date', note = $('#lensnote');
    // 胶囊指示条：两个弹簧（位置、宽度）
    var pill = document.createElement('span'); pill.className = 'pill'; lensEl.insertBefore(pill, lensEl.firstChild);
    var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
    var pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
    function movePill(instant) { var b = tabs.filter(function (t) { return t.getAttribute('data-lens') === cur; })[0]; if (!b) return; var x = b.offsetLeft, w = b.offsetWidth; if (instant) { px.set(x); pw.set(w); } else { px.to(x); pw.to(w); } }
    function header(g) { var h = document.createElement('div'); h.className = 'lgh'; h.setAttribute('data-g', g.k); h.innerHTML = '<b>' + g.label + '</b><small>' + g.ids.length + ' 行</small>'; return h; }
    function setLens(lens, instant) {
      if (!D.lens[lens]) return; cur = lens;
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-lens') === lens)); });
      movePill(instant);
      var first = {}; Object.keys(rows).forEach(function (id) { first[id] = rows[id].getBoundingClientRect().top; });
      var frag = document.createDocumentFragment();
      D.lens[lens].forEach(function (g) { frag.appendChild(header(g)); g.ids.forEach(function (id) { if (rows[id]) frag.appendChild(rows[id]); }); });
      $$('.lgh', grid).forEach(function (h) { h.remove(); });
      grid.appendChild(frag);
      if (note) note.textContent = '按' + D.lensName[lens] + '分成 ' + D.lens[lens].length + ' 组 · 点一行展开';
      if (instant || RM.on) return;
      Object.keys(rows).forEach(function (id) {
        var r = rows[id], dy = first[id] - r.getBoundingClientRect().top; if (Math.abs(dy) < 1) return;
        r.style.transition = 'none'; r.style.transform = 'translateY(' + dy.toFixed(1) + 'px)';
      });
      grid.offsetHeight; // 强制回流
      Object.keys(rows).forEach(function (id) { var r = rows[id]; if (!r.style.transform) return; r.style.transition = 'transform .5s cubic-bezier(.2,.8,.2,1)'; r.style.transform = ''; });
      $$('.lgh', grid).forEach(function (h) { h.animate && h.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 260, easing: 'ease-out' }); });
    }
    lensEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-lens]'); if (b) setLens(b.getAttribute('data-lens')); });
    lensEl.addEventListener('keydown', function (e) { if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return; var i = tabs.findIndex(function (t) { return t.getAttribute('data-lens') === cur; }), n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); setLens(n.getAttribute('data-lens')); e.preventDefault(); });
    function toggle(r, open) { var o = open == null ? !r.classList.contains('open') : open; r.classList.toggle('open', o); var b = $('.lhead', r); if (b) b.setAttribute('aria-expanded', String(o)); }
    grid.addEventListener('click', function (e) { var b = e.target.closest('.lhead'); if (!b) return; toggle(b.closest('.lrow')); });
    function scrollToRow(r) {
      var lb = $('.lensbar'), off = navH() + (lb ? lb.offsetHeight : 0) + 8, top = r.getBoundingClientRect().top + window.scrollY - off;
      window.scrollTo({ top: Math.max(0, top), behavior: RM.on ? 'auto' : 'smooth' });
    }
    LAMPS.open = function (id, lens) {
      var r = rows[id]; if (!r) return;
      if (lens && lens !== cur) setLens(lens, true);
      toggle(r, true); scrollToRow(r);
      r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1400);
      try { history.replaceState(null, '', '#n-' + id); } catch (er) {}
    };
    LAMPS.lens = function (lens) { setLens(lens, true); var sec = $('#lamps'); if (sec) window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - navH(), behavior: RM.on ? 'auto' : 'smooth' }); };
    document.addEventListener('click', function (e) { var b = e.target.closest('.evb.all'); if (!b) return; LAMPS.lens(b.getAttribute('data-lens')); });
    // 初始：服务器渲染的就是「日期」分组；装上指示条
    movePill(true);
    window.addEventListener('resize', function () { movePill(true); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); });
    var m = /^#n-([\w-]+)$/.exec(location.hash || ''); if (m && rows[m[1]]) setTimeout(function () { LAMPS.open(m[1]); }, 60);
  })();

  /* ================= 门槛 · 年轮：扇出标签 + 直接拖转（松手按角速度投影，吸附到最近的岁首） ================= */
  function wheelLabels(svg, rot) {
    if (!svg) return; rot = rot || 0;
    var cx = parseFloat(svg.getAttribute('data-cx')), cy = parseFloat(svg.getAttribute('data-cy')), R0 = parseFloat(svg.getAttribute('data-r0')), W = parseFloat(svg.getAttribute('data-w')), H = parseFloat(svg.getAttribute('data-h'));
    var pxw = svg.getBoundingClientRect().width || W, scale = pxw / W, fs = Math.min(15, Math.max(10.5 / scale, 10.5)), gap = fs * 1.28, pad = fs;
    var ld = $('.leaders', svg), lb = $('.labels', svg); if (!ld || !lb) return;
    var sides = { L: [], R: [] };
    $$('.fx', svg).forEach(function (g) {
      var d = parseInt(g.getAttribute('data-doy'), 10), a = (d - 1) / 365 * 2 * Math.PI - Math.PI / 2 + rot * Math.PI / 180, c = Math.cos(a), sn = Math.sin(a);
      sides[c < 0 ? 'L' : 'R'].push({ id: g.getAttribute('data-node'), name: g.getAttribute('data-name') || '', x: cx + R0 * c, y: cy + R0 * sn, ideal: cy + (R0 + 46) * sn, on: g.classList.contains('on') });
    });
    var lines = '', texts = '';
    Object.keys(sides).forEach(function (side) {
      var arr = sides[side].sort(function (p, q) { return p.ideal - q.ideal; }), n = arr.length; if (!n) return;
      var ys = arr.map(function (p) { return clamp(p.ideal, pad, H - pad); });
      for (var i = 1; i < n; i++) ys[i] = Math.max(ys[i], ys[i - 1] + gap);
      if (ys[n - 1] > H - pad) { ys[n - 1] = H - pad; for (var j = n - 2; j >= 0; j--) ys[j] = Math.min(ys[j], ys[j + 1] - gap); }
      if (ys[0] < pad) { ys[0] = pad; for (var k = 1; k < n; k++) ys[k] = Math.max(ys[k], ys[k - 1] + gap); }
      var lx = side === 'L' ? cx - R0 - 30 : cx + R0 + 30, anchor = side === 'L' ? 'end' : 'start', ex = side === 'L' ? lx + 5 : lx - 5, room = (side === 'L' ? lx : W - lx) - 6;
      arr.forEach(function (p, i) {
        var est = 0, f = fs; for (var q = 0; q < p.name.length; q++) est += p.name.charCodeAt(q) > 255 ? 1 : 0.56;
        if (est * fs > room) f = Math.max(9, room / est);
        lines += '<path class="ld' + (p.on ? ' on' : '') + '" data-node="' + p.id + '" d="M' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + ' L' + ex.toFixed(1) + ' ' + ys[i].toFixed(1) + '"/>';
        texts += '<text class="wl' + (p.on ? ' on' : '') + '" data-node="' + p.id + '" x="' + lx.toFixed(1) + '" y="' + ys[i].toFixed(1) + '" text-anchor="' + anchor + '" dominant-baseline="middle" font-size="' + f.toFixed(1) + '">' + p.name.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</text>';
      });
    });
    ld.innerHTML = lines; lb.innerHTML = texts;
  }
  (function initWheel() {
    var box = $('#wheelbox'), svg = box && $('svg.wheel', box); if (!svg) return;
    var g = $('#wheel-g', svg), cx = parseFloat(svg.getAttribute('data-cx')), cy = parseFloat(svg.getAttribute('data-cy')), R0 = parseFloat(svg.getAttribute('data-r0')), W = parseFloat(svg.getAttribute('data-w'));
    var mts = $$('.mt', g), ancEls = $$('.anc', g), chips = $$('#anchors button'), cen = $('.cen2', svg), A = D.anchors;
    var rotOf = A.map(function (a) { return -(a.doy - 1) / 365 * 360; });
    var curK = 0;
    function apply(r) {
      g.setAttribute('transform', 'rotate(' + r.toFixed(2) + ' ' + cx + ' ' + cy + ')');
      mts.forEach(function (t) { t.setAttribute('transform', 'rotate(' + (-r).toFixed(2) + ' ' + t.getAttribute('x') + ' ' + t.getAttribute('y') + ')'); });
    }
    function settle() {
      var r = rs.x, best = 0, bd = 1e9; rotOf.forEach(function (ro, k) { var dd = Math.abs(((r - ro) % 360 + 540) % 360 - 180); if (dd < bd) { bd = dd; best = k; } });
      curK = best; chips.forEach(function (c, k) { c.setAttribute('aria-pressed', String(k === best)); }); ancEls.forEach(function (a, k) { a.classList.toggle('on', k === best); });
      if (cen) cen.textContent = '顶上 = ' + A[best].short; box.setAttribute('aria-valuetext', '顶上 = ' + A[best].desc);
      wheelLabels(svg, r); svg.classList.remove('spin');
    }
    var rs = new Spring({ from: 0, damping: 1, response: 0.4, eps: 0.02, onUpdate: function (x) { apply(x); }, onRest: settle });
    function nearestRot(k, from) { var r = rotOf[k]; while (r - from > 180) r -= 360; while (from - r > 180) r += 360; return r; }
    function goAnchor(k, v, z) { svg.classList.add('spin'); rs.to(nearestRot(k, rs.x), { velocity: v || 0, damping: z || 1, response: 0.4 }); }
    chips.forEach(function (c, k) { c.addEventListener('click', function () { goAnchor(k); }); });
    // 拖转：在环带里按下；角度 1:1 跟手（保留抓取角），松手按角速度投影
    var vt = new VTrack(), drag = null;
    function geo(e) { var r = svg.getBoundingClientRect(), s = r.width / W, x = e.clientX - (r.left + cx * s), y = e.clientY - (r.top + cy * s); return { a: Math.atan2(y, x) * 180 / Math.PI, r: Math.sqrt(x * x + y * y) / s }; }
    function inRing(e) { var q = geo(e); return q.r > R0 * 0.42 && q.r < R0 * 1.45; }
    box.addEventListener('touchstart', function (e) { if (e.touches.length === 1 && inRing(e.touches[0])) e.preventDefault(); }, { passive: false });
    box.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return;
      var q = geo(e), ring = inRing(e); drag = { id: e.pointerId, a: q.a, sx: e.clientX, sy: e.clientY, moved: false, ring: ring, node: e.target.closest('[data-node]') };
      if (ring) { try { box.setPointerCapture(e.pointerId); } catch (er) {} rs.stop(); vt.reset(); vt.add(rs.x); }
    });
    box.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.moved && Math.abs(e.clientX - drag.sx) + Math.abs(e.clientY - drag.sy) < 6) return;
      if (!drag.ring) { drag.moved = true; return; }
      if (!drag.moved) { drag.moved = true; box.classList.add('drag'); svg.classList.add('spin'); }
      var q = geo(e), da = q.a - drag.a; if (da > 180) da -= 360; if (da < -180) da += 360; drag.a = q.a;
      rs.set(rs.x + da); vt.add(rs.x);
    });
    function end(e, cancel) {
      if (!drag || e.pointerId !== drag.id) return;
      var d0 = drag; drag = null; box.classList.remove('drag');
      if (!d0.moved) { if (!cancel && d0.node) { LAMPS.open(d0.node.getAttribute('data-node')); } if (d0.ring && !rs.running) settle(); return; }
      if (!d0.ring) return;
      var v = vt.v(), proj = rs.x + project(v, 0.996), best = 0, bd = 1e9;
      rotOf.forEach(function (ro, k) { var r = nearestRot(k, proj), dd = Math.abs(r - proj); if (dd < bd) { bd = dd; best = k; } });
      rs.to(nearestRot(best, proj), { velocity: v, damping: Math.abs(v) > 60 ? 0.8 : 1, response: 0.4 });
    }
    box.addEventListener('pointerup', function (e) { end(e, false); });
    box.addEventListener('pointercancel', function (e) { end(e, true); });
    box.addEventListener('keydown', function (e) {
      if (['ArrowRight', 'ArrowDown', 'ArrowLeft', 'ArrowUp'].indexOf(e.key) < 0) { if (e.key === 'Enter' && e.target.closest('[data-node]')) LAMPS.open(e.target.closest('[data-node]').getAttribute('data-node')); return; }
      e.preventDefault(); var dir = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : -1; goAnchor((curK + dir + A.length) % A.length);
    });
    apply(0); wheelLabels(svg, 0); settle();
    var wt = 0; window.addEventListener('resize', function () { clearTimeout(wt); wt = setTimeout(function () { wheelLabels(svg, rs.x); }, 150); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { wheelLabels(svg, rs.x); });
  })();
})();
