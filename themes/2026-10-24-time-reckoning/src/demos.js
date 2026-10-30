/* 三张主图（新年落在哪个季节 / 谁的正午 / 每天差多少 + 地球这只钟）与三个小工具的逻辑。依赖 calendars.js 的 CAL、app.js 的 window.YZ（弹簧等）与 #data 里的 D。 */
(function () {
  'use strict';
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var YZ = window.YZ || {}, D = YZ.D || JSON.parse($('#data').textContent);
  CAL.setLunar(D.lunar);
  var RM = YZ.RM || { on: false }, Spring = YZ.Spring, VTrack = YZ.VTrack, clamp = YZ.clamp, dragIntent = YZ.dragIntent;
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var set = function (id, t) { var e = $('#' + id); if (e) e.textContent = t; };
  var gdate = function (y, m, d) { return y + '-' + pad(m) + '-' + pad(d); };
  var fromJdn = function (j) { var g = CAL.jdnToGreg(j); return gdate(g.y, g.m, g.d); };
  var hhmm = function (min) { min = ((min % 1440) + 1440) % 1440; var h = Math.floor(min / 60), m = Math.round(min - h * 60); if (m === 60) { h = (h + 1) % 24; m = 0; } return pad(h) + ':' + pad(m); };
  var SVGNS = 'http://www.w3.org/2000/svg';
  function mk(tag, attrs, parent) { var e = document.createElementNS(SVGNS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  function dialSvg(min, size) {
    var t = ((min % 1440) + 1440) % 1440, ha = (t / 60 % 12) * 30, ma = (t % 60) * 6, R = function (a, r) { return [50 + r * Math.sin(a * Math.PI / 180), 50 - r * Math.cos(a * Math.PI / 180)]; };
    var tk = '', k; for (k = 0; k < 12; k++) { var p1 = R(k * 30, 42), p2 = R(k * 30, 47); tk += '<line class="tk" x1="' + p1[0].toFixed(1) + '" y1="' + p1[1].toFixed(1) + '" x2="' + p2[0].toFixed(1) + '" y2="' + p2[1].toFixed(1) + '"/>'; }
    var h = R(ha, 25), m = R(ma, 37);
    return '<svg class="dial' + (t < 360 || t >= 1080 ? ' night' : '') + '" viewBox="0 0 100 100" width="' + (size || 64) + '" height="' + (size || 64) + '"><circle class="face" cx="50" cy="50" r="47"/>' + tk + '<line class="hh" x1="50" y1="50" x2="' + h[0].toFixed(1) + '" y2="' + h[1].toFixed(1) + '"/><line class="mh" x1="50" y1="50" x2="' + m[0].toFixed(1) + '" y2="' + m[1].toFixed(1) + '"/><circle class="pin" cx="50" cy="50" r="3.5"/></svg>';
  }
  // 横向拖动的通用骨架：鼠标按下即拖，触屏先判方向（横向才接管）；onX(clientX) 每次移动调用
  function dragX(box, onX, onEnd) {
    var dg = null;
    box.addEventListener('pointerdown', function (e) { if (e.button > 0) return; dg = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: false }; if (e.pointerType === 'mouse') { dg.on = true; try { box.setPointerCapture(e.pointerId); } catch (er) {} onX(e.clientX); } });
    box.addEventListener('pointermove', function (e) {
      if (!dg || e.pointerId !== dg.id) return;
      if (!dg.on) { var it = dragIntent(e, dg.sx, dg.sy); if (it === 1) { dg.on = true; try { box.setPointerCapture(e.pointerId); } catch (er) {} } else if (it === -1) { dg = null; return; } else return; }
      onX(e.clientX);
    });
    function end(e) { if (!dg || e.pointerId !== dg.id) return; var was = dg.on; if (!was && e.type === 'pointerup') onX(e.clientX); dg = null; if (onEnd) onEnd(); }
    box.addEventListener('pointerup', end); box.addEventListener('pointercancel', function (e) { dg = null; });
  }

  /* ================= 第一章主图 · 新年落在哪个季节 ================= */
  (function initDrift() {
    var box = $('#dbox'), svg = $('#dsv'); if (!box || !svg || !D.drift) return;
    var DR = D.drift, W = 960, H = 440, PL = 56, PR = 88, PT = 40, PB = 36, PW = 0, PH = 0, YR = 365.2422;
    // ---- 天文：Meeus《天文算法》表 27.a / 27.b 的平均春分与冬至（JDE）、平朔
    function decSol(y) {
      if (y < 1000) { var Y = y / 1000; return 1721414.39987 + 365242.88257 * Y - 0.00769 * Y * Y - 0.00933 * Y * Y * Y - 0.00006 * Y * Y * Y * Y; }
      var Z = (y - 2000) / 1000; return 2451900.05952 + 365242.74049 * Z - 0.06223 * Z * Z - 0.00823 * Z * Z * Z + 0.00032 * Z * Z * Z * Z;
    }
    var SYN = 29.530588861, NM0 = 2451550.09766;
    function bjDay(jde) { return Math.floor(jde + 0.5 + 8 / 24); } // 北京时间（UTC+8）的民用日 JDN
    function cnNewYear(y) { // 天文年 y 的春节：冬至所在月为十一月，往后第二个朔日（1900–2100 用 GB/T 33661 月表）
      if (y >= 1901 && y <= 2100) { var j = CAL.lunarToJdn(y, 1, false, 1); if (j) return j; }
      var sol = decSol(y - 1), sd = bjDay(sol), k = Math.floor((sol - NM0) / SYN);
      if (bjDay(NM0 + k * SYN) > sd) k--; if (bjDay(NM0 + (k + 1) * SYN) <= sd) k++;
      return bjDay(NM0 + (k + 2) * SYN);
    }
    function xOf(j) { return 2000 + (j - 2451545) / 365.25; }
    function astro(h) { return h < 0 ? h + 1 : h; } // 历史纪年（前 = 负）→ 天文纪年
    function hy(a) { a = Math.round(a); return a <= 0 ? '前 ' + (1 - a) : String(a); }
    function season(j) { // 民用日 j 落在最近一个冬至之后第几天
      var y = Math.floor(xOf(j)), s = decSol(y); if (s > j) s = decSol(y - 1); var d = j - s; if (d >= YR) d -= YR; if (d < 0) d += YR; return d;
    }
    // ---- 七种历法的新年序列
    var SER = {};
    DR.cals.forEach(function (c) {
      var a = astro(c.a), b = astro(c.b), ev = [], j, y;
      if (c.k === 'greg') for (y = Math.max(a, 1583); y <= b; y++) ev.push(CAL.gregToJdn(y, 1, 1));
      else if (c.k === 'jul') for (y = a; y <= b; y++) ev.push(CAL.julToJdn(y, 1, 1));
      else if (c.k === 'egy') { var k0 = Math.floor((2451545 + (a - 2000) * 365.25 - 1448638) / 365), k1 = Math.ceil((2451545 + (b + 1 - 2000) * 365.25 - 1448638) / 365); for (var k = k0; k <= k1; k++) { j = 1448638 + 365 * k; var xx = xOf(j); if (xx >= a && xx < b + 1) ev.push(j); } }
      else if (c.k === 'isl') for (y = 1; y <= 1560; y++) { j = CAL.islToJdn(y, 1, 1); var xi = xOf(j); if (xi >= a && xi < b + 1) ev.push(j); }
      else if (c.k === 'heb') for (y = a + 3760; y <= b + 3762; y++) { j = CAL.hebToJdn(y, 7, 1); var xh = xOf(j); if (xh >= a && xh < b + 1) ev.push(j); }
      else if (c.k === 'cn') for (y = a; y <= b; y++) ev.push(cnNewYear(y));
      else if (c.k === 'per') for (y = a - 621; y <= b - 620; y++) { j = CAL.perToJdn(y, 1, 1); var xp = xOf(j); if (xp >= a && xp < b + 1) ev.push(j); }
      SER[c.k] = ev.map(function (j) { return { j: j, x: xOf(j), d: season(j) }; });
    });
    // ---- SVG 骨架：按容器的实际像素宽度画（字永远是 12 px）；横轴按年份，用 matrix 缩放；纵轴固定像素
    function yPx(d) { return PT + PH - d / YR * PH; }
    var SEAS = [[0, '冬至'], [89.0, '春分'], [181.8, '夏至'], [275.4, '秋分'], [YR, '冬至']]; // 今天的季节长度；早年会偏几天，读数因此只从算出的冬至起数
    var gx, gm, lineG, labG, curGl, curL, curY, paths = {}, labels = {}, pts = {}, PATHD = {};
    DR.cals.forEach(function (c) { // 路径只算一次：x 用年份，y 用 0–1 的季节比例，画的时候再乘高度
      var ev = SER[c.k], d = [], prev = null;
      ev.forEach(function (e) {
        if (!prev) d.push(['M', e.x, e.d]);
        else if (Math.abs(e.d - prev.d) > YR / 2) { // 绕过一整圈：先画到边上，再从另一边接着画
          var up = e.d < prev.d, dd = up ? (e.d + YR - prev.d) : (e.d - YR - prev.d), f = ((up ? YR : 0) - prev.d) / dd, xc = prev.x + (e.x - prev.x) * f;
          d.push(['L', xc, up ? YR : 0], ['M', xc, up ? 0 : YR], ['L', e.x, e.d]);
        } else d.push(['L', e.x, e.d]);
        prev = e;
      });
      PATHD[c.k] = d;
    });
    function build() {
      W = Math.max(300, Math.round(box.clientWidth - 16)); H = Math.round(clamp(W * 0.46, 340, 440)); PL = W < 600 ? 44 : 56; PR = W < 600 ? 68 : 88; PW = W - PL - PR; PH = H - PT - PB;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.innerHTML = '';
      var defs = mk('defs', {}, svg), cp = mk('clipPath', { id: 'dclip' }, defs); mk('rect', { x: PL, y: PT - 2, width: PW, height: PH + 4 }, cp);
      var gy = mk('g', {}, svg);
      SEAS.forEach(function (s) { mk('line', { class: 'gl s', x1: PL, y1: yPx(s[0]), x2: PL + PW, y2: yPx(s[0]) }, gy); var t = mk('text', { class: 'gt s', x: PL - 8, y: yPx(s[0]) + 4, 'text-anchor': 'end' }, gy); t.textContent = s[1]; });
      gx = mk('g', {}, svg); gm = mk('g', {}, svg); var clipG = mk('g', { 'clip-path': 'url(#dclip)' }, svg); lineG = mk('g', {}, clipG); labG = mk('g', {}, svg); var curG = mk('g', {}, svg);
      DR.cals.forEach(function (c) {
        var d = PATHD[c.k].map(function (q) { return q[0] + q[1].toFixed(2) + ' ' + yPx(q[2]).toFixed(1); }).join(' ');
        paths[c.k] = mk('path', { class: 'cal' + (c.k === 'isl' || c.k === 'egy' ? ' thin' : ''), d: d }, lineG);
        var lt = mk('text', { class: 'cl' }, labG); lt.textContent = c.n; labels[c.k] = lt;
      });
      curGl = mk('line', { class: 'curg', y1: PT, y2: PT + PH }, curG); curL = mk('line', { class: 'cur', y1: PT, y2: PT + PH }, curG); curY = mk('text', { class: 'cury', y: PT + 20 }, curG);
      DR.cals.forEach(function (c) { pts[c.k] = mk('circle', { class: 'pt', r: 4.5, cx: 0, cy: 0, style: 'display:none' }, curG); });
    }
    // ---- 视窗（三档）用弹簧过渡
    var ZOOM = { all: [-2500, 2100], ce: [1, 2100], m: [1500, 2100] }, view = ZOOM.all.slice(), curYr = 2026, hl = '';
    function sx(x) { return PL + (x - view[0]) / (view[1] - view[0]) * PW; }
    function fmtTick(x) { return x <= 0 ? '前 ' + (1 - x) : String(x); }
    function drawAxis() {
      var span = view[1] - view[0], ppy = PW / span, st = [50, 100, 250, 500, 1000].filter(function (q) { return q * ppy >= 60; })[0] || 1000;
      gx.innerHTML = '';
      for (var h = Math.ceil(-2500 / st) * st; h <= 2100; h += st) {
        var a = h <= 0 ? h + 1 : h; if (h === 0) a = 1; if (a < view[0] - 1 || a > view[1] + 1) continue;
        var X = sx(a); mk('line', { class: 'gl', x1: X, y1: PT, x2: X, y2: PT + PH }, gx); var t = mk('text', { class: 'gt', x: X, y: PT + PH + 20, 'text-anchor': 'middle' }, gx); t.textContent = h === 0 ? '1' : fmtTick(a);
      }
      gm.innerHTML = ''; var lastR = [-1e9, -1e9], lastW = [0, 0];
      DR.marks.forEach(function (m) {
        var a = astro(m[0]); if (a < view[0] || a > view[1]) return; var X = sx(a), wd = m[1].length * 12 + 8;
        mk('line', { class: 'mk', x1: X, y1: PT, x2: X, y2: PT + PH }, gm);
        var row = X - lastR[0] >= lastW[0] ? 0 : X - lastR[1] >= lastW[1] ? 1 : -1; if (row < 0 || X + wd > W) return; lastR[row] = X; lastW[row] = wd;
        var t = mk('text', { class: 'mkt', x: X + 4, y: PT - 22 + row * 14 }, gm); t.textContent = m[1];
      });
      lineG.setAttribute('transform', 'matrix(' + (PW / (view[1] - view[0])).toFixed(6) + ' 0 0 1 ' + (PL - view[0] * PW / (view[1] - view[0])).toFixed(3) + ' 0)');
      // 直接标注：每条线在视窗里的最后一点
      var L = [];
      DR.cals.forEach(function (c) {
        var ev = SER[c.k], last = null; for (var i = ev.length - 1; i >= 0; i--) if (ev[i].x <= view[1] + 0.5) { last = ev[i]; break; }
        var lt = labels[c.k]; if (!last || last.x < view[0]) { lt.style.display = 'none'; return; } lt.style.display = '';
        L.push({ k: c.k, x: sx(last.x), y: yPx(last.d) + 4, el: lt });
      });
      L.sort(function (a, b) { return a.y - b.y; });
      for (var i = 1; i < L.length; i++) if (L[i].y - L[i - 1].y < 14 && Math.abs(L[i].x - L[i - 1].x) < 90) L[i].y = L[i - 1].y + 14;
      L.forEach(function (l) { l.el.setAttribute('x', (l.x + 8).toFixed(1)); l.el.setAttribute('y', l.y.toFixed(1)); });
      drawCursor();
    }
    // ---- 竖线与读数
    var CALN = {}; DR.cals.forEach(function (c) { CALN[c.k] = c; });
    function civil(j) { return j < 2299161 ? CAL.jdnToJul(j) : CAL.jdnToGreg(j); }
    function seasonTxt(d) { var n = Math.floor(d); return n === 0 ? '冬至当天' : '冬至后 ' + n + ' 天'; }
    function drawCursor() {
      var X = sx(curYr + 0.5); curL.setAttribute('x1', X); curL.setAttribute('x2', X); curGl.setAttribute('x1', X); curGl.setAttribute('x2', X); var rt = X > PL + PW - 90; curY.setAttribute('x', rt ? X - 8 : X + 8); curY.setAttribute('text-anchor', rt ? 'end' : 'start'); curY.textContent = hy(curYr);
      set('dyr', ''); var dyr = $('#dyr'); if (dyr) dyr.innerHTML = (curYr <= 0 ? '前 ' + (1 - curYr) : curYr) + '<small>年 · 七种历法的新年</small>';
      DR.cals.forEach(function (c) {
        var ev = SER[c.k], hit = null; for (var i = 0; i < ev.length; i++) { if (ev[i].x >= curYr && ev[i].x < curYr + 1) { hit = ev[i]; break; } }
        var li = $('#dlist li[data-cal="' + c.k + '"]'), p = pts[c.k];
        if (!hit) { li.classList.add('na'); set('dv-' + c.k, '—'); set('ds-' + c.k, curYr < astro(c.a) ? hy(astro(c.a)) + ' 年起' : '画到 ' + hy(astro(c.b)) + ' 年'); p.style.display = 'none'; return; }
        li.classList.remove('na'); var g = civil(hit.j);
        set('dv-' + c.k, g.m + ' 月 ' + g.d + ' 日'); set('ds-' + c.k, seasonTxt(hit.d));
        p.setAttribute('cx', sx(hit.x).toFixed(1)); p.setAttribute('cy', yPx(hit.d).toFixed(1)); p.style.display = (!hl || hl === c.k) ? '' : 'none';
      });
      box.setAttribute('aria-valuenow', curYr); box.setAttribute('aria-valuetext', hy(curYr) + ' 年');
    }
    function setHl(k) {
      hl = k || ''; svg.classList.toggle('hl', !!hl);
      DR.cals.forEach(function (c) { paths[c.k].classList.toggle('on', c.k === hl); labels[c.k].classList.toggle('on', c.k === hl); var b = $('#dlist li[data-cal="' + c.k + '"] button'); if (b) b.setAttribute('aria-pressed', String(c.k === hl)); });
      if (hl) lineG.appendChild(paths[hl]);
      drawCursor();
    }
    $$('#dlist li').forEach(function (li) { $('button', li).addEventListener('click', function () { var k = li.getAttribute('data-cal'); setHl(hl === k ? '' : k); }); });
    var vs0 = new Spring({ from: view[0], damping: 1, response: 0.5, eps: 0.05, onUpdate: function (x) { view[0] = x; drawAxis(); } });
    var vs1 = new Spring({ from: view[1], damping: 1, response: 0.5, eps: 0.05, onUpdate: function (x) { view[1] = x; drawAxis(); } });
    var ztabs = $$('#dzoom button'), zEl = $('#dzoom');
    var pill = document.createElement('span'); pill.className = 'pill'; zEl.insertBefore(pill, zEl.firstChild);
    var pxs = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } }), pws = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
    var zcur = 'all';
    function zpill(instant) { var b = ztabs.filter(function (t) { return t.getAttribute('data-z') === zcur; })[0]; if (!b) return; if (instant) { pxs.set(b.offsetLeft); pws.set(b.offsetWidth); } else { pxs.to(b.offsetLeft); pws.to(b.offsetWidth); } }
    function setZoom(z) {
      zcur = z; var Z = ZOOM[z]; ztabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-z') === z)); }); zpill(false);
      curYr = clamp(curYr, Math.ceil(Z[0]), Math.floor(Z[1]) - 1); box.setAttribute('aria-valuemin', Z[0]); box.setAttribute('aria-valuemax', Z[1]);
      vs0.to(Z[0]); vs1.to(Z[1]);
    }
    zEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-z]'); if (b) setZoom(b.getAttribute('data-z')); });
    window.addEventListener('resize', function () { zpill(true); }); if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { zpill(true); });
    // 拖动竖线（1:1 跟手）与键盘
    function yrAt(cx) { var r = svg.getBoundingClientRect(), X = (cx - r.left) / r.width * W; return Math.round(clamp(view[0] + (X - PL) / PW * (view[1] - view[0]) - 0.5, Math.ceil(view[0]), Math.floor(view[1]) - 1)); }
    dragX(box, function (cx) { var y = yrAt(cx); if (y !== curYr) { curYr = y; drawCursor(); } });
    box.addEventListener('keydown', function (e) {
      var st = e.shiftKey ? 10 : 1, y = curYr;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') y += st; else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') y -= st; else if (e.key === 'Home') y = Math.ceil(view[0]); else if (e.key === 'End') y = Math.floor(view[1]) - 1; else return;
      e.preventDefault(); curYr = clamp(y, Math.ceil(view[0]), Math.floor(view[1]) - 1); drawCursor();
    });
    // ---- 换一种闰法
    var TROP = 365.24219;
    function setRule(k) {
      var r = DR.rules.filter(function (x) { return x.k === k; })[0]; if (!r) return;
      $$('#rchips button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-rule') === k)); });
      var diff = r.L - TROP, sec = diff * 86400;
      set('rr-mean', r.L.toFixed(5)); set('rr-err', Math.abs(sec) < 1 ? '几乎不差' : (sec > 0 ? '长 ' : '短 ') + (Math.abs(sec) >= 3600 ? num(Math.abs(sec) / 3600, 1) + ' 小时' : Math.abs(sec) >= 60 ? num(Math.abs(sec) / 60, 1) + ' 分钟' : num(Math.abs(sec), 0) + ' 秒'));
      set('rr-day', Math.abs(diff) < 1e-7 ? '—' : num(1 / Math.abs(diff), 0) + ' 年'); set('rr-10k', (Math.abs(diff * 10000) < 0.5 ? '不到半天' : (diff > 0 ? '晚 ' : '早 ') + num(Math.abs(diff * 10000), Math.abs(diff * 10000) < 10 ? 1 : 0) + ' 天'));
      set('rr-note', r.note);
      return r;
    }
    $$('#rchips button').forEach(function (b) { b.addEventListener('click', function () { var r = setRule(b.getAttribute('data-rule')); if (r) setHl(r.cal); }); });
    build(); setRule('greg'); drawAxis(); zpill(true);
    var rzD = 0, lastBW = Math.round(box.clientWidth);
    window.addEventListener('resize', function () { clearTimeout(rzD); rzD = setTimeout(function () { var w = Math.round(box.clientWidth); if (w === lastBW) return; lastBW = w; build(); setHl(hl); drawAxis(); }, 150); });
  })();

  /* ================= 第二章主图 · 谁的正午 ================= */
  (function initNoon() {
    var wrap = $('#noon'); if (!wrap || !D.noon) return;
    var T0 = 660, T1 = 900, Y = 2026, J0 = CAL.gregToJdn(Y, 1, 1), MDN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    var ax = $('#nbax'); for (var t = T0; t <= T1; t += 30) { var i = document.createElement('i'); i.style.left = ((t - T0) / (T1 - T0) * 100) + '%'; i.textContent = t % 60 ? '' : hhmm(t); ax.appendChild(i); }
    $$('.nbt', wrap).forEach(function (tr) { for (var t = T0; t <= T1; t += 30) { var k = document.createElement('i'); k.className = 'tk'; k.style.left = ((t - T0) / (T1 - T0) * 100) + '%'; tr.insertBefore(k, tr.firstChild); } var c = $('.c12', tr); c.style.left = ((720 - T0) / (T1 - T0) * 100) + '%'; });
    var nth = function (m, wd, n) { var j = CAL.gregToJdn(Y, m, 1), w = CAL.weekday(j); return CAL.gregToJdn(Y, m, 1 + ((wd - w + 7) % 7) + (n - 1) * 7); };
    var last = function (m, wd) { var j = CAL.gregToJdn(Y, m, MDN[m - 1]), w = CAL.weekday(j); return j - ((w - wd + 7) % 7); };
    var RULES = { eu: [last(3, 0), last(10, 0)], us: [nth(3, 0, 2), nth(11, 0, 1)], eg: [last(4, 5), last(10, 4) + 1] }; // 埃及到 10 月最后一个周四 24:00 为止
    function inDst(r, doy) { var se = RULES[r]; if (!se) return false; var j = J0 + doy - 1; return j >= se[0] && j < se[1]; }
    var CITIES = D.noon.slice().sort(function (a, b) { return a.lon - b.lon; });
    var rows = {}; $$('.nbr', wrap).forEach(function (r) { rows[r.getAttribute('data-city')] = { el: r, sun: $('.sun', r), gap: $('.gap', r), b: $('.nbv b', r), s: $('.nbv small', r), n: $('.nbn small', r) }; });
    var mode = 'now', doy = parseInt($('#ndate').value, 10), lonI = $('#nlon'), tzI = $('#ntz'), dstI = $('#ndst');
    function noonOf(c) { var e = CAL.eot(doy); if (mode === 'lmt') return { m: 720 - e, dst: false }; var dst = inDst(c.r, doy); return { m: 720 + 4 * (c.tz * 15 - c.lon) - e + (dst ? 60 : 0), dst: dst }; }
    function you() { var L = parseFloat(lonI.value), T = parseFloat(tzI.value); if (!isFinite(L) || !isFinite(T)) return null; return { id: 'you', lon: clamp(L, -180, 180), tz: clamp(T, -12, 14), r: dstI.value }; }
    var shown = {}, from = {}, to = {};
    function pct(m) { return clamp((m - T0) / (T1 - T0), 0, 1) * 100; }
    function paint(id, m) { var r = rows[id]; if (!r) return; shown[id] = m; var p = pct(m), z = pct(720); r.sun.style.left = p.toFixed(2) + '%'; r.gap.style.left = Math.min(p, z).toFixed(2) + '%'; r.gap.style.width = Math.abs(p - z).toFixed(2) + '%'; }
    var sp = new Spring({ from: 1, damping: 1, response: 0.55, eps: 0.002, onUpdate: function (u) { Object.keys(to).forEach(function (id) { paint(id, from[id] + (to[id] - from[id]) * u); }); } });
    function diffTxt(m) { var d = Math.round(m - 720); if (Math.abs(d) < 1) return '差不到 1 分钟'; var a = Math.abs(d), h = Math.floor(a / 60), mm = a % 60; return (d > 0 ? '晚 ' : '早 ') + (h ? h + ' 小时 ' : '') + (mm ? mm + ' 分' : '').trim(); }
    function tzTxt(c, dst) { if (mode === 'lmt') return '地方平时'; var o = c.tz + (dst ? 1 : 0), s = (o >= 0 ? '+' : '−') + (Math.abs(o) % 1 ? Math.floor(Math.abs(o)) + ':' + pad(Math.round(Math.abs(o) % 1 * 60)) : Math.abs(o)); return 'UTC' + s + (dst ? ' · 夏令时' : ''); }
    function update(animate) {
      var list = CITIES.slice(), y = you(); if (y) list.push(y);
      list.forEach(function (c) {
        var r = rows[c.id]; if (!r) return; var n = noonOf(c);
        r.b.textContent = hhmm(n.m); r.s.textContent = diffTxt(n.m); r.n.textContent = tzTxt(c, n.dst); r.el.classList.toggle('dst', n.dst);
        r.el.title = (c.n || '你的城') + '：太阳正午在钟表的 ' + hhmm(n.m) + (n.m < T0 || n.m > T1 ? '（在图外）' : '');
        from[c.id] = shown[c.id] == null ? n.m : shown[c.id]; to[c.id] = n.m;
      });
      if (animate && !RM.on) { sp.set(0); sp.to(1); } else sp.set(1);
      var e = CAL.eot(doy), md = (function () { var m = 0, d = doy; while (d > MDN[m]) { d -= MDN[m]; m++; } return (m + 1) + ' 月 ' + d + ' 日'; })();
      set('ndate-o', md); set('neot', '均时差 ' + (e >= 0 ? '+' : '−') + num(Math.abs(e), 1) + ' 分钟（' + (e >= 0 ? '日晷比钟表快' : '日晷比钟表慢') + '）');
    }
    var eo = document.createElement('span'); eo.id = 'neot'; eo.className = 'small'; $('.nctl', wrap).appendChild(eo);
    // 模式切换：胶囊 + 弹簧
    var mEl = $('#nmode'), mt = $$('button', mEl), pill = document.createElement('span'); pill.className = 'pill'; mEl.insertBefore(pill, mEl.firstChild);
    var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } }), pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
    function mpill(instant) { var b = mt.filter(function (t) { return t.getAttribute('data-m') === mode; })[0]; if (!b) return; if (instant) { px.set(b.offsetLeft); pw.set(b.offsetWidth); } else { px.to(b.offsetLeft); pw.to(b.offsetWidth); } }
    mEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-m]'); if (!b) return; mode = b.getAttribute('data-m'); mt.forEach(function (t) { t.setAttribute('aria-selected', String(t === b)); }); mpill(false); update(true); });
    window.addEventListener('resize', function () { mpill(true); }); if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { mpill(true); });
    $('#ndate').addEventListener('input', function (e) { doy = parseInt(e.target.value, 10); update(false); });
    [lonI, tzI].forEach(function (i) { i.addEventListener('input', function () { i.setAttribute('aria-invalid', String(!isFinite(parseFloat(i.value)))); update(false); }); });
    dstI.addEventListener('change', function () { update(true); });
    mpill(true); update(false);
  })();

  /* ================= 第三章主图 · 每天差多少（精度阶梯）：宽屏横排、窄屏竖排，都按容器实际像素画 ================= */
  (function initLadder() {
    var box = $('#lbox'); if (!box || !D.ladder) return;
    var R = D.ladder, n = R.length, cur = n - 1, svg = $('#lsv', box), TOP = 3, BOT = -14, GPS = 3.8e-5, narrow = false, geo = null;
    var fig = $('#lc-fig'), img = $('#lc-img'), cap = $('#lc-cap');
    function si(v) { var U = [[1, '秒'], [1e-3, '毫秒'], [1e-6, '微秒'], [1e-9, '纳秒'], [1e-12, '皮秒'], [1e-15, '飞秒']]; for (var i = 0; i < U.length; i++) if (v >= U[i][0] * 0.999) { var x = v / U[i][0]; return (x >= 10 ? Math.round(x) : Number(x.toPrecision(2))) + ' ' + U[i][1]; } return v + ' 秒'; }
    function draw() {
      var w = Math.max(300, Math.round(box.clientWidth - 16)); narrow = w < 560; svg.innerHTML = '';
      if (!narrow) {
        var W = w, H = Math.round(clamp(w * 0.58, 380, 440)), L = 64, Rr = 16, T = 16, B = 64, pw = W - L - Rr, ly = function (v) { return T + (TOP - Math.log10(v)) / (TOP - BOT) * (H - T - B); };
        geo = { L: L, pw: pw, W: W };
        svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
        for (var e = TOP; e >= BOT; e--) { var y = ly(Math.pow(10, e)); mk('line', { class: 'gl' + (e % 3 === 0 ? ' s' : ''), x1: L, y1: y, x2: W - Rr, y2: y }, svg); if (e % 3 === 0) { var t = mk('text', { class: 'gt', x: L - 8, y: y + 4, 'text-anchor': 'end' }, svg); t.textContent = si(Math.pow(10, e)); } }
        var st = ''; R.forEach(function (r, k) { var y = ly(r.v), x0 = L + k / n * pw, x1 = L + (k + 1) / n * pw; st += k ? ' V' + y.toFixed(1) + ' H' + x1.toFixed(1) : 'M' + x0.toFixed(1) + ' ' + y.toFixed(1) + ' H' + x1.toFixed(1); });
        mk('path', { d: st, fill: 'none', style: 'stroke:var(--line);stroke-width:1.5' }, svg);
        var gy = ly(GPS); mk('line', { class: 'gps', x1: L, y1: gy, x2: W - Rr, y2: gy }, svg); var gt = mk('text', { class: 'gpst', x: W - Rr, y: gy - 8, 'text-anchor': 'end' }, svg); gt.textContent = 'GPS 卫星钟若不做相对论修正：每天快约 38 微秒';
        R.forEach(function (r, k) {
          var x = L + (k + .5) / n * pw, y = ly(r.v), g = mk('g', { class: 'rung', 'data-k': k }, svg);
          mk('rect', { x: x - pw / n / 2, y: T, width: pw / n, height: H - T, fill: 'transparent' }, g);
          mk('rect', { class: 'bar', x: x - 2, y: y, width: 4, height: H - B - y, rx: 2 }, g); mk('circle', { class: 'bar', cx: x, cy: y, r: 6 }, g);
          var tv = mk('text', { class: 'bv', x: x, y: y - 14, 'text-anchor': 'middle' }, g); tv.textContent = r.vtxt;
          var tn = mk('text', { class: 'bn', x: x, y: H - B + 20, 'text-anchor': 'middle' }, g); tn.textContent = r.short; var ty = mk('text', { class: 'by', x: x, y: H - B + 38, 'text-anchor': 'middle' }, g); ty.textContent = r.yr;
        });
      } else {
        var W2 = w, rowH = 44, T2 = 44, L2 = 84, R2 = 16, H2 = T2 + n * rowH + 28, pw2 = W2 - L2 - R2, lx = function (v) { return L2 + (Math.log10(v) - BOT) / (TOP - BOT) * pw2; }, ry = function (k) { return T2 + k * rowH + rowH / 2; };
        geo = null; svg.setAttribute('viewBox', '0 0 ' + W2 + ' ' + H2);
        var lastL = -1e9;
        for (var e2 = BOT; e2 <= TOP; e2++) { var x = lx(Math.pow(10, e2)); mk('line', { class: 'gl' + (e2 % 3 === 0 ? ' s' : ''), x1: x, y1: T2 - 8, x2: x, y2: H2 - 24 }, svg); if (e2 % 3 === 0) { var lab = si(Math.pow(10, e2)), row = (x - lastL < lab.length * 9 + 8) ? 1 : 0; if (!row) lastL = x; var t2 = mk('text', { class: 'gt', x: x, y: row ? 30 : 14, 'text-anchor': 'middle' }, svg); t2.textContent = lab; } }
        var st2 = ''; R.forEach(function (r, k) { var x = lx(r.v), y = ry(k); st2 += k ? ' H' + x.toFixed(1) + ' V' + y.toFixed(1) : 'M' + x.toFixed(1) + ' ' + (y - rowH / 2).toFixed(1) + ' V' + y.toFixed(1); });
        mk('path', { d: st2, fill: 'none', style: 'stroke:var(--line);stroke-width:1.5' }, svg);
        var gx2 = lx(GPS); mk('line', { class: 'gps', x1: gx2, y1: T2 - 8, x2: gx2, y2: H2 - 24 }, svg); var gt2 = mk('text', { class: 'gpst', x: gx2, y: H2 - 8, 'text-anchor': 'middle' }, svg); gt2.textContent = 'GPS 修正 · 38 微秒';
        R.forEach(function (r, k) {
          var x = lx(r.v), y = ry(k), g = mk('g', { class: 'rung', 'data-k': k }, svg);
          mk('rect', { x: 0, y: y - rowH / 2, width: W2, height: rowH, fill: 'transparent' }, g);
          mk('rect', { class: 'bar', x: L2, y: y - 2, width: Math.max(0, x - L2), height: 4, rx: 2 }, g); mk('circle', { class: 'bar', cx: x, cy: y, r: 6 }, g);
          var tn = mk('text', { class: 'bn', x: 0, y: y - 2, 'text-anchor': 'start' }, g); tn.textContent = r.short; var ty = mk('text', { class: 'by', x: 0, y: y + 14, 'text-anchor': 'start' }, g); ty.textContent = r.yr;
          var right = x > W2 - 70, tv = mk('text', { class: 'bv', x: right ? x - 12 : x + 12, y: y + 4, 'text-anchor': right ? 'end' : 'start' }, g); tv.textContent = r.vtxt;
        });
      }
      paint();
    }
    function paint() { $$('.rung', svg).forEach(function (g) { g.classList.toggle('on', parseInt(g.getAttribute('data-k'), 10) === cur); }); }
    function sel(k) {
      k = clamp(k, 0, n - 1); var r = R[k]; cur = k; paint();
      set('lc-k', '第 ' + (k + 1) + ' 级 · 共 ' + n + ' 级'); set('lc-n', r.name); set('lc-y', r.year); set('lc-v', r.vtxt); set('lc-p', r.principle); set('lc-d', r.per_day); set('lc-1', r.one || ''); $('#lc-1').style.display = $('#lc-1t').style.display = r.one ? '' : 'none'; set('lc-o', (r.note ? r.note + '；' : '') + '置信度 ' + (r.conf || '中'));
      if (r.img) { fig.classList.remove('none'); img.src = r.img; img.alt = r.alt; $('.cs', cap).textContent = r.cap; $('.cr', cap).textContent = r.cred; } else fig.classList.add('none');
      box.setAttribute('aria-valuenow', k + 1); box.setAttribute('aria-valuetext', r.name + '，每天差约 ' + r.vtxt);
    }
    function kAt(cx) { if (!geo) return cur; var rc = svg.getBoundingClientRect(), X = (cx - rc.left) / rc.width * geo.W; return Math.floor((X - geo.L) / (geo.pw / n)); }
    dragX(box, function (cx) { if (geo) { var k = kAt(cx); if (k !== cur) sel(k); } });
    box.addEventListener('click', function (e) { var g = e.target.closest('.rung'); if (g) sel(parseInt(g.getAttribute('data-k'), 10)); });
    box.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight' || e.key === 'ArrowDown') sel(cur + 1); else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') sel(cur - 1); else if (e.key === 'Home') sel(0); else if (e.key === 'End') sel(n - 1); else return; e.preventDefault(); });
    var lw = 0, rz = 0; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { var w = Math.round(box.clientWidth); if (w !== lw) { lw = w; draw(); } }, 150); });
    lw = Math.round(box.clientWidth); draw(); sel(n - 1);
  })();

  /* ================= 第三章主图 · 地球这只钟（ΔT 与闰秒）：按容器实际像素画 ================= */
  (function initLod() {
    var box = $('#lodbox'), svg = $('#lodsv'); if (!box || !svg) return;
    var X0 = 1900, X1 = 2030, Y0 = -10, Y1 = 80, P = D.deltaT, YMAX = 2024, yr = 2024; // 数据到 2025 年初为止：年中读数最多到 2024 年
    var W, H, L, Rr = 16, T = 24, B = 52, lines, pt, lab, ls;
    function xs(y) { return L + (y - X0) / (X1 - X0) * (W - L - Rr); }
    function ys(v) { return T + (Y1 - v) / (Y1 - Y0) * (H - T - B); }
    function dt(y) { for (var i = 0; i < P.length - 1; i++) if (y >= P[i][0] && y <= P[i + 1][0]) return P[i][1] + (P[i + 1][1] - P[i][1]) * (y - P[i][0]) / (P[i + 1][0] - P[i][0]); return y < P[0][0] ? P[0][1] : P[P.length - 1][1]; }
    function build() {
      W = Math.max(300, Math.round(box.clientWidth - 16)); var narrow = W < 560; H = narrow ? 260 : 300; L = narrow ? 40 : 48;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.innerHTML = '';
      var by = H - B;
      [0, 20, 40, 60, 80].forEach(function (v) { mk('line', { class: 'gl', x1: L, y1: ys(v), x2: W - Rr, y2: ys(v) }, svg); var t = mk('text', { class: 'gt', x: L - 8, y: ys(v) + 4, 'text-anchor': 'end' }, svg); t.textContent = v + ' s'; });
      for (var y = 1900; y <= 2020; y += narrow ? 40 : 20) { var t2 = mk('text', { class: 'gt', x: xs(y), y: by + 44, 'text-anchor': 'middle' }, svg); t2.textContent = y; }
      var d = 'M' + P.map(function (p) { return xs(p[0]).toFixed(1) + ' ' + ys(p[1]).toFixed(1); }).join(' L');
      mk('path', { class: 'dta', d: d + ' L' + xs(P[P.length - 1][0]).toFixed(1) + ' ' + ys(0).toFixed(1) + ' L' + xs(P[0][0]).toFixed(1) + ' ' + ys(0).toFixed(1) + 'Z' }, svg);
      mk('path', { class: 'dtl', d: d }, svg);
      mk('line', { class: 'gl', x1: L, y1: by, x2: W - Rr, y2: by, style: 'stroke:var(--line)' }, svg);
      ls = D.leaps.map(function (s) { var ly = parseInt(s.slice(0, 4), 10) + (s.slice(5) === '06-30' ? 0.5 : 1); var l = mk('line', { class: 'ls', 'data-y': ly, x1: xs(ly), y1: by - 4, x2: xs(ly), y2: by + 12 }, svg); var tt = mk('title', {}, l); tt.textContent = s; return l; });
      var xe = xs(2027.38); mk('line', { class: 'end', x1: xe, y1: T, x2: xe, y2: by + 12 }, svg);
      var tl = mk('text', { class: 'lsl', x: xs(1972), y: by + 26 }, svg); tl.textContent = narrow ? '闰秒 27 次' : '闰秒（27 次）';
      var te = mk('text', { class: 'lsl', x: xe - 6, y: narrow ? T + 12 : by + 26, 'text-anchor': 'end' }, svg); te.textContent = narrow ? '2027 起不插' : '2027-05-20 起不再插';
      var g = mk('g', {}, svg); lines = [mk('line', { class: 'curg', y1: T, y2: by }, g), mk('line', { class: 'cur', y1: T, y2: by }, g)]; pt = mk('circle', { class: 'pt', r: 6 }, g); lab = mk('text', { class: 'cury' }, g);
      draw();
    }
    function draw() {
      var X = xs(yr + 0.5), v = dt(yr + 0.5), slope = dt(yr + 1) - dt(yr);
      lines.forEach(function (l) { l.setAttribute('x1', X); l.setAttribute('x2', X); }); pt.setAttribute('cx', X); pt.setAttribute('cy', ys(v)); var rt = X > W - 120; lab.setAttribute('x', rt ? X - 12 : X + 12); lab.setAttribute('y', ys(v) + (v > 50 ? 28 : -14)); lab.setAttribute('text-anchor', rt ? 'end' : 'start'); lab.textContent = yr;
      var n = D.leaps.filter(function (s) { return parseInt(s.slice(0, 4), 10) <= yr; }).length;
      ls.forEach(function (l) { l.classList.toggle('me', parseFloat(l.getAttribute('data-y')) <= yr + 1); });
      set('lod-dt', (v >= 0 ? '+' : '−') + num(Math.abs(v), 1)); set('lod-ls', yr < 1972 ? '还没有闰秒制度' : n + ' 次'); set('lod-lod', (slope >= 0 ? '+' : '−') + num(Math.abs(slope) / 365.25 * 1000, 2) + ' 毫秒');
      box.setAttribute('aria-valuenow', yr); box.setAttribute('aria-valuetext', yr + ' 年：ΔT 约 ' + num(v, 1) + ' 秒，闰秒 ' + n + ' 次');
    }
    function yAt(cx) { var r = svg.getBoundingClientRect(), X = (cx - r.left) / r.width * W; return Math.round(clamp(X0 + (X - L) / (W - L - Rr) * (X1 - X0) - 0.5, X0, YMAX)); }
    dragX(box, function (cx) { var y = yAt(cx); if (y !== yr) { yr = y; draw(); } });
    box.addEventListener('keydown', function (e) { var st = e.shiftKey ? 10 : 1; if (e.key === 'ArrowRight' || e.key === 'ArrowUp') yr += st; else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') yr -= st; else if (e.key === 'Home') yr = X0; else if (e.key === 'End') yr = YMAX; else return; e.preventDefault(); yr = clamp(yr, X0, YMAX); draw(); });
    var lw = 0, rz = 0; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { var w = Math.round(box.clientWidth); if (w !== lw) { lw = w; build(); } }, 150); });
    lw = Math.round(box.clientWidth); build();
  })();

  /* ================= 工具 · 历法换算器 ================= */
  (function () {
    var root = $('.tconv'); if (!root) return;
    var grid = $('#cv-grid'), date = $('#cv-date'), WD = ['日', '一', '二', '三', '四', '五', '六'];
    var systems = [
      { id: 'jul', name: '儒略历', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { return CAL.jdnToJul(j); }, to: function (f) { return CAL.julToJdn(f.y, f.m, f.d); }, note: '1582 年以前欧洲通用；俄国用到 1918，东正教会历至今' },
      { id: 'jdn', name: '儒略日数', fields: [['j', 'JDN']], from: function (j) { return { j: j }; }, to: function (f) { return f.j; }, note: 'Scaliger 1583；从公元前 4713-01-01 正午起算的天数，天文学家的通用计数' },
      { id: 'cn', name: '农历', fields: [['y', '年'], ['m', '月'], ['l', '闰 1/0'], ['d', '日']], from: function (j) { var l = CAL.jdnToLunar(j); return l ? { y: l.y, m: l.m, l: l.leap ? 1 : 0, d: l.d, text: CAL.lunarStr(l) } : null; }, to: function (f) { return CAL.lunarToJdn(f.y, f.m, !!f.l, f.d); }, note: 'GB/T 33661-2017 规则，1900–2100' },
      { id: 'isl', name: '伊斯兰历（算表）', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { var r = CAL.jdnToIsl(j); r.text = '希吉拉 ' + r.y + ' 年 ' + CAL.ISL_M[r.m - 1] + '月 ' + r.d + ' 日'; return r; }, to: function (f) { return CAL.islToJdn(f.y, f.m, f.d); }, note: '民用算表口径；观月历可差一天' },
      { id: 'heb', name: '希伯来历', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { var r = CAL.jdnToHeb(j); r.text = r.y + ' 年 ' + CAL.HEB_M[r.m - 1] + '月 ' + r.d + ' 日（月序 1 = 尼散）'; return r; }, to: function (f) { return CAL.hebToJdn(f.y, f.m, f.d); }, note: '固定算法（通行说法 359 年定）；一日从日落起' },
      { id: 'per', name: '伊朗太阳历', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { var r = CAL.jdnToPer(j); r.text = r.y + ' 年 ' + CAL.PER_M[r.m - 1] + '月 ' + r.d + ' 日'; return r; }, to: function (f) { return CAL.perToJdn(f.y, f.m, f.d); }, note: '春分起年；33 年周期规则' },
      { id: 'maya', name: '玛雅长纪历', fields: [['b', 'baktun'], ['k', 'katun'], ['t', 'tun'], ['w', 'winal'], ['n', 'kin']], from: function (j) { var m = CAL.jdnToMaya(j), tz = CAL.jdnToTzolkin(j), h = CAL.jdnToHaab(j); return { b: m[0], k: m[1], t: m[2], w: m[3], n: m[4], text: m.join('.') + ' · ' + tz.n + ' ' + tz.name + ' ' + h.d + ' ' + CAL.HAAB_M[h.m] }; }, to: function (f) { return CAL.mayaToJdn(f.b, f.k, f.t, f.w, f.n); }, note: 'GMT 相关常数 584283；13.0.0.0.0 = 2012-12-21' },
    ];
    function render(j) {
      var g = CAL.jdnToGreg(j), wd = CAL.weekday(j), lunar = CAL.jdnToLunar(j);
      date.value = gdate(g.y, g.m, g.d);
      var html = '<div class="cvcard main"><div class="cvh">公历 · 星期' + WD[wd] + '</div><div class="cvbig">' + gdate(g.y, g.m, g.d) + '</div><div class="cvs">干支纪日 ' + CAL.ganzhiDay(j) + (lunar ? ' · ' + CAL.ganzhiYear(lunar.y) + '年' : '') + '</div></div>';
      systems.forEach(function (s) {
        var f = s.from(j);
        html += '<div class="cvcard" data-sys="' + s.id + '"><div class="cvh">' + esc(s.name) + '</div><div class="cvbig">' + (f ? esc(f.text || (f.j != null ? num(f.j) : f.y + '-' + pad(f.m) + '-' + pad(f.d))) : '超出月表范围') + '</div><div class="cvf">'
          + s.fields.map(function (fd) { return '<label>' + esc(fd[1]) + '<input type="number" data-f="' + fd[0] + '" value="' + (f ? f[fd[0]] : '') + '"></label>'; }).join('') + '<button type="button" class="cvgo">按此反推</button></div><div class="cvs">' + esc(s.note) + '</div></div>';
      });
      grid.innerHTML = html;
    }
    grid.addEventListener('click', function (ev) {
      var b = ev.target.closest('.cvgo'); if (!b) return; var card = b.closest('.cvcard'), s = systems.filter(function (x) { return x.id === card.getAttribute('data-sys'); })[0], f = {};
      $$('input[data-f]', card).forEach(function (i) { f[i.getAttribute('data-f')] = parseInt(i.value, 10); });
      try { var j = s.to(f); if (j && isFinite(j)) render(Math.round(j)); } catch (e) {}
    });
    date.addEventListener('change', function () { var p = date.value.split('-').map(Number); if (p.length === 3 && p[0]) render(CAL.gregToJdn(p[0], p[1], p[2])); });
    $('#cv-today').addEventListener('click', function () { var t = new Date(); render(CAL.gregToJdn(t.getFullYear(), t.getMonth() + 1, t.getDate())); });
    render(CAL.gregToJdn(2026, 10, 24));
  })();

  /* ================= 工具 · 拨表换算 ================= */
  (function () {
    var root = $('.tdst'); if (!root) return;
    var A = $('#ds-a'), B = $('#ds-b'), date = $('#ds-date'), row = $('#ds-row');
    var nth = function (y, m, wd, n) { var j = CAL.gregToJdn(y, m, 1), w = CAL.weekday(j), d = 1 + ((wd - w + 7) % 7) + (n - 1) * 7; return CAL.gregToJdn(y, m, d); };
    var last = function (y, m, wd) { var ml = [31, CAL.isGregLeap(y) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1], j = CAL.gregToJdn(y, m, ml), w = CAL.weekday(j); return j - ((w - wd + 7) % 7); };
    var RULES = { // 返回 [start JDN, end JDN]（含 start，不含 end；南半球跨年用 (start>end) 表示）
      eu: function (y) { return [last(y, 3, 0), last(y, 10, 0)]; }, us: function (y) { return [nth(y, 3, 0, 2), nth(y, 11, 0, 1)]; },
      au: function (y) { return [nth(y, 10, 0, 1), nth(y, 4, 0, 1)]; }, nz: function (y) { return [last(y, 9, 0), nth(y, 4, 0, 1)]; },
      cl: function (y) { var s = nth(y, 9, 0, 1); if (CAL.jdnToGreg(s).d < 2) s += 7; var e = nth(y, 4, 0, 1); if (CAL.jdnToGreg(e).d < 2) e += 7; return [s, e]; },
      eg: function (y) { return [last(y, 4, 5), last(y, 10, 4) + 1]; }, none: null };
    function inDst(c, j) { var r = RULES[c.r]; if (!r) return false; var y = CAL.jdnToGreg(j).y, se = r(y); if (se[0] < se[1]) return j >= se[0] && j < se[1]; return j >= se[0] || j < se[1]; }
    function status(c, j) { var r = RULES[c.r]; if (!r) return c.note || '全年 UTC' + (c.o >= 0 ? '+' : '') + c.o + '，不换时'; var y = CAL.jdnToGreg(j).y, se = r(y), on = inDst(c, j); return (on ? '夏令时中 UTC' : '标准时 UTC') + (function (v) { return (v >= 0 ? '+' : '−') + num(Math.abs(v), 2); })(c.o + (on ? 1 : 0)) + '；' + (se[0] < se[1] ? '夏令时 ' + fromJdn(se[0]) + ' → ' + fromJdn(se[1]) : '夏令时 ' + fromJdn(se[0]) + ' 起、到 ' + fromJdn(se[1]) + ' 止（跨年）'); }
    function draw() {
      var a = D.dstCities[A.value], b = D.dstCities[B.value], p = (date.value || '2026-10-24').split('-').map(Number), j = CAL.gregToJdn(p[0], p[1], p[2]);
      var oa = a.o + (inDst(a, j) ? 1 : 0), ob = b.o + (inDst(b, j) ? 1 : 0), diff = ob - oa;
      row.innerHTML = [[a, oa], [b, ob]].map(function (x) { return '<div class="dsc"><b>' + esc(x[0].n) + '</b>' + dialSvg(720 + x[1] * 60, 72) + '<span>' + hhmm(720 + x[1] * 60) + '</span><small>UTC 12:00 时</small></div>'; }).join('<div class="dsarrow">' + (diff === 0 ? '同时' : (diff > 0 ? '快 ' : '慢 ') + num(Math.abs(diff), 2) + ' 小时') + '</div>');
      set('ds-diff', (diff === 0 ? '0' : (diff > 0 ? '+' : '−') + num(Math.abs(diff), 2)) + ' 小时'); set('ds-a-st', status(a, j)); set('ds-b-st', status(b, j));
      $('#ds-note').textContent = '规则：欧盟 / 英国 3 月与 10 月最后一个周日 01:00 UTC；美国 / 加拿大 3 月第二个周日至 11 月第一个周日当地 02:00；澳大利亚东南各州 10 月第一个周日至 4 月第一个周日；新西兰 9 月最后一个周日至 4 月第一个周日；智利 9 月与 4 月第一个在 2 日或之后的周日；埃及 4 月最后一个周五至 10 月最后一个周四（2023 起）。墨西哥 2022 年、中国 1992 年、日本 1952 年起不实行。只按日期判断，不计换时当天的具体时刻。';
    }
    [A, B, date].forEach(function (i) { i.addEventListener('input', draw); i.addEventListener('change', draw); });
    B.selectedIndex = 1; draw();
  })();

  /* ================= 工具 · 你经历过几次闰秒 ================= */
  (function () {
    var root = $('.tleap'); if (!root) return;
    var yin = $('#ls-y'), bar = $('#ls-bar'), list = $('#ls-list'), proj = $('#ls-proj');
    function draw() {
      var by = parseInt(yin.value, 10) || 1985, mine = D.leaps.filter(function (s) { return parseInt(s.slice(0, 4), 10) >= by; });
      $('#ls-sum').textContent = by < 1972 ? '你出生时还没有闰秒；1972 年以来的 27 次你全经历了。' : by > 2016 ? '你出生后一次闰秒也没有插过——而且以后也不会有了。' : '你经历过 ' + mine.length + ' 次闰秒，第一次是 ' + mine[0] + '，最后一次 2016-12-31。';
      bar.innerHTML = '<div class="axis">' + [1972, 1980, 1990, 2000, 2010, 2020, 2027].map(function (y) { return '<span style="left:' + ((y - 1972) / 58 * 100) + '%">' + y + '</span>'; }).join('') + '</div>'
        + D.leaps.map(function (s) { var y = parseInt(s.slice(0, 4), 10) + (s.slice(5) === '06-30' ? .5 : 1); return '<i style="left:' + ((y - 1972) / 58 * 100) + '%" class="' + (y >= by ? 'me' : '') + '" title="' + s + '"></i>'; }).join('')
        + '<em style="left:' + ((2027.38 - 1972) / 58 * 100) + '%">2027-05-20 起不再插</em>' + (by >= 1972 && by <= 2027 ? '<u style="left:' + ((by - 1972) / 58 * 100) + '%">' + by + ' 出生</u>' : '');
      list.innerHTML = D.leaps.map(function (s, i) { return '<li' + (parseInt(s.slice(0, 4), 10) >= by ? ' class="me"' : '') + '><span>' + (i + 1) + '</span>' + s + '</li>'; }).join('');
      // 2027 后 UT1−UTC 的示意漂移：按 1972–2016 平均速率（约 0.6 s/年）与 2016–2025 的近零速率两条线；纵轴 1 格 = 10 秒
      var X = function (y) { return 40 + (y - 2016) / 84 * 540; }, Y = function (v) { return 14 - v * 1.0; };
      var d1 = 'M' + X(2016) + ' ' + Y(0) + ' L' + X(2027.4) + ' ' + Y(0) + ' L' + X(2100) + ' ' + Y(-(2100 - 2027.4) * 0.6), d2 = 'M' + X(2027.4) + ' ' + Y(0) + ' L' + X(2100) + ' ' + Y(-(2100 - 2027.4) * 0.1);
      proj.innerHTML = [0, -20, -40].map(function (v) { return '<line class="' + (v ? 'ln2' : 'ln') + '" x1="40" y1="' + Y(v) + '" x2="580" y2="' + Y(v) + '"/><text class="dt" x="36" y="' + (Y(v) + 4) + '" text-anchor="end">' + v + ' s</text>'; }).join('') + '<path class="o2 d" d="' + d1 + '"/><path class="o2" d="' + d2 + '"/>'
        + '<text class="dt" x="' + X(2027.4) + '" y="10">2027-05-20</text><line class="a" x1="' + X(2027.4) + '" y1="12" x2="' + X(2027.4) + '" y2="' + Y(-44) + '"/><text class="dt" x="40" y="112">UT1−UTC 示意：虚线 0.6 s / 年（1972–2016 均速），实线 0.1 s / 年（2016–2025）</text><text class="dt" x="580" y="' + (Y(0) - 4) + '" text-anchor="end">2100</text>';
    }
    yin.addEventListener('input', draw); draw();
  })();
})();
