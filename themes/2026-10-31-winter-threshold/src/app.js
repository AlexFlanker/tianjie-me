(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  window.YZ = { D: D };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };

  /* ---------- 深浅色：这一题默认是夜；用户切过就记住 */
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') || 'dark', next = cur === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next);
    try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
    drawField();
  });

  /* ---------- 太阳：昼长（小时）、日落（分钟，经度 0° 平太阳时）。与 sun.py 同公式 */
  var RAD = Math.PI / 180;
  function declEqt(doy) { var g = 2 * Math.PI / 365 * (doy - 1); return { decl: 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g), eqt: 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g)) }; }
  function dayLen(lat, doy) { var d = declEqt(doy).decl, c = Math.cos(90.833 * RAD) / (Math.cos(lat * RAD) * Math.cos(d)) - Math.tan(lat * RAD) * Math.tan(d); if (c >= 1) return 0; if (c <= -1) return 24; return 2 * Math.acos(c) / RAD / 15; }
  function sunset(lat, doy) { var e = declEqt(doy), c = Math.cos(90.833 * RAD) / (Math.cos(lat * RAD) * Math.cos(e.decl)) - Math.tan(lat * RAD) * Math.tan(e.decl); if (c >= 1 || c <= -1) return null; var ha = Math.acos(c) / RAD; return 720 + 4 * ha - e.eqt; }
  function hm(h) { var H = Math.floor(h), M = Math.round((h - H) * 60); if (M === 60) { H++; M = 0; } return H + ' 小时 ' + (M < 10 ? '0' : '') + M + ' 分'; }
  function mm(m) { m = ((m % 1440) + 1440) % 1440; var H = Math.floor(m / 60), M = Math.round(m % 60); if (M === 60) { H++; M = 0; } return (H < 10 ? '0' : '') + H + ':' + (M < 10 ? '0' : '') + M; }
  var MD = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  function doyToMd(doy, y) { var md = MD.slice(); if (y && ((y % 4 === 0 && y % 100 !== 0) || y % 400 === 0)) md[1] = 29; var m = 0; while (m < 11 && doy > md[m]) { doy -= md[m]; m++; } return { m: m + 1, d: doy }; }
  function isoDoy(iso) { var p = iso.split('-').map(Number), t = 0; for (var i = 0; i < p[1] - 1; i++) t += MD[i]; return t + p[2]; }
  window.YZ.sun = { dayLen: dayLen, sunset: sunset, hm: hm, mm: mm, doyToMd: doyToMd, isoDoy: isoDoy };

  /* ---------- 入场 */
  var fades = $$('.fade');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else { fades.forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- 章节导航与进度 */
  var nav = $('#cnav'), prog = $('#prog'), links = $$('[data-nav]'), secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-nav')); });
  function setNavH() { if (nav) root.style.setProperty('--nav-h', nav.offsetHeight + 'px'); }
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (prog) prog.style.width = (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%';
      var y = window.scrollY + (nav ? nav.offsetHeight : 0) + 40, cur = 0;
      for (var i = 0; i < secs.length; i++) if (secs[i] && secs[i].offsetTop <= y) cur = i;
      links.forEach(function (a, i) { var on = i === cur; if (on !== a.classList.contains('on')) { a.classList.toggle('on', on); if (on && nav) { var r = a.getBoundingClientRect(), rr = nav.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) a.parentNode.scrollLeft += r.left - rr.left - 20; } } });
    });
  }
  setNavH(); onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { setNavH(); onScroll(); });

  /* ---------- 数字入视口计数 */
  function countTo(el, to, dec, ms) {
    if (reduced || !ms) { el.textContent = dec ? to.toFixed(dec) : num(to, 0); return; }
    var t0 = performance.now();
    (function tick(t) { var p = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - p, 3), v = to * e; el.textContent = dec ? v.toFixed(dec) : num(v, 0); if (p < 1) requestAnimationFrame(tick); else el.textContent = dec ? to.toFixed(dec) : num(to, 0); })(t0);
  }
  var cnts = $$('.cnt[data-to]');
  if ('IntersectionObserver' in window) { var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { countTo(e.target, parseFloat(e.target.getAttribute('data-to')), parseInt(e.target.getAttribute('data-dec') || '0', 10), 1100); cio.unobserve(e.target); } }); }, { threshold: .4 }); cnts.forEach(function (el) { cio.observe(el); }); }

  /* ---------- 卷首 · 夜的田野 */
  var fbox = $('#fieldbox'), cv = $('#fcv'), fov = $('#fov'), ftip = $('#ftip');
  var FW = 1200, FH = 520, FL = 58, FR = 16, FT = 16, FB = 30, LAT0 = 62, LAT1 = -36, DOY0 = 274, DOY1 = 365, FSM = false; // 10/1 → 12/31
  // 窄屏（手机）：画布改成 720×600 的更竖的比例，字放大，只给主要的节日写名字
  var FKEY = ['samhain', 'halloween', 'dia-de-muertos', 'bonfire-night', 'lidong', 'diwali', 'hanyi', 'lucia', 'loy-krathong', 'thanksgiving', 'martinmas', 'todos-santos-andes'];
  function fieldSize() { var bw = (fbox && fbox.clientWidth) || 1200, sm = bw < 700; FSM = sm; FW = sm ? 720 : 1200; FH = sm ? 600 : 520; FL = sm ? 64 : 58; FB = sm ? 34 : 30; if (cv) { cv.width = FW; cv.height = FH; } if (fov) fov.setAttribute('viewBox', '0 0 ' + FW + ' ' + FH); if (fbox) fbox.classList.toggle('sm', sm); }
  function fx(doy) { return FL + (doy - DOY0) / (DOY1 - DOY0) * (FW - FL - FR); }
  function fy(lat) { return FT + (LAT0 - lat) / (LAT0 - LAT1) * (FH - FT - FB); }
  function hex(h) { h = h.trim().replace('#', ''); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
  function drawField() {
    if (!cv) return;
    var cs = getComputedStyle(fbox), a = hex(cs.getPropertyValue('--night-0')), b = hex(cs.getPropertyValue('--night-1')), c = hex(cs.getPropertyValue('--day')), s = hex(cs.getPropertyValue('--surface'));
    var ctx = cv.getContext('2d'), img = ctx.createImageData(FW, FH), dat = img.data;
    var cols = []; for (var x = 0; x < FW; x++) cols.push(DOY0 + (DOY1 - DOY0) * ((x - FL) / (FW - FL - FR)));
    for (var y = 0; y < FH; y++) {
      var lat = LAT0 + (LAT1 - LAT0) * ((y - FT) / (FH - FT - FB)), inY = y >= FT && y <= FH - FB;
      for (var x = 0; x < FW; x++) {
        var col; if (!inY || x < FL || x > FW - FR) col = s;
        else { var n = 1 - dayLen(lat, cols[x]) / 24, t = Math.max(0, Math.min(1, (n - 0.38) / (0.70 - 0.38))); col = t < .5 ? [c[0] + (b[0] - c[0]) * t * 2, c[1] + (b[1] - c[1]) * t * 2, c[2] + (b[2] - c[2]) * t * 2] : [b[0] + (a[0] - b[0]) * (t - .5) * 2, b[1] + (a[1] - b[1]) * (t - .5) * 2, b[2] + (a[2] - b[2]) * (t - .5) * 2]; }
        var i = (y * FW + x) * 4; dat[i] = col[0]; dat[i + 1] = col[1]; dat[i + 2] = col[2]; dat[i + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
  }
  function buildField() {
    if (!fov) return; fieldSize(); drawField();
    var s = '', LF = FSM ? 17 : 12, LS = LF + 3;
    [8, 10, 12, 14].forEach(function (hrs) {
      var pts = [];
      for (var x = FL; x <= FW - FR; x += 6) { var doy = DOY0 + (DOY1 - DOY0) * ((x - FL) / (FW - FL - FR)), best = null, bd = 9; for (var lat = LAT0; lat >= LAT1; lat -= 0.5) { var d = Math.abs(dayLen(lat, doy) - hrs); if (d < bd) { bd = d; best = lat; } } if (best !== null && bd < 0.12) pts.push([x, fy(best)]); }
      if (pts.length > 2) s += '<polyline class="iso" points="' + pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ') + '"/><text class="isol" x="' + (pts[pts.length - 1][0] - 4) + '" y="' + (pts[pts.length - 1][1] - 5) + '" text-anchor="end">白昼 ' + hrs + ' 小时</text>';
    });
    [60, 40, 20, 0, -20].forEach(function (lat) { s += '<text class="ax" x="' + (FL - 8) + '" y="' + (fy(lat) + 4).toFixed(1) + '" text-anchor="end">' + (lat > 0 ? '北纬 ' + lat + '°' : lat < 0 ? '南纬 ' + (-lat) + '°' : '赤道') + '</text>'; });
    [[274, '10 月 1 日'], [305, '11 月 1 日'], [335, '12 月 1 日']].forEach(function (m) { s += '<text class="ax" x="' + fx(m[0]).toFixed(1) + '" y="' + (FH - 10) + '" text-anchor="middle">' + m[1] + '</text>'; });
    s += '<rect class="win" x="' + fx(isoDoy('2026-10-31')).toFixed(1) + '" y="' + FT + '" width="' + (fx(isoDoy('2026-11-09')) - fx(isoDoy('2026-10-31'))).toFixed(1) + '" height="' + (FH - FT - FB) + '"/>';
    s += '<text class="lab s" x="' + (fx(isoDoy('2026-10-31')) + 4).toFixed(1) + '" y="' + (FT + 14) + '">这十天</text>';
    // 图题：放在十月北半球的空白处（也是封面截图里的标题）
    s += '<text class="ftitle" x="' + (FL + 16) + '" y="' + (FT + (FSM ? 40 : 46)) + '">冬天的门槛</text><text class="fsub" x="' + (FL + 17) + '" y="' + (FT + (FSM ? 64 : 70)) + '">二十一个节日的夜与灯 · 2026 年 10–12 月</text>';
    // 灯：按日期排，标签避让
    var items = D.field.slice().sort(function (p, q) { return isoDoy(p.date) - isoDoy(q.date) || q.lat - p.lat; }), placed = [];
    items.forEach(function (f, i) {
      var show = !FSM || FKEY.indexOf(f.id) >= 0, x = fx(isoDoy(f.date)), y = fy(f.lat), w = show ? f.name.length * LF + 6 : 0, flip = x + 9 + w > FW - 8, lx = flip ? x - 9 - w : x + 9, ly = y + 4;
      if (show) { for (var k = 0; k < 12; k++) { var clash = placed.some(function (p) { return Math.abs(p.y - ly) < LS && lx < p.x + p.w && lx + w > p.x; }); if (!clash) break; ly += LS; } placed.push({ x: lx, y: ly, w: w }); }
      s += '<g class="lg" data-fid="' + f.id + '" style="opacity:0;animation:lit .45s ' + (0.3 + i * 0.07).toFixed(2) + 's forwards"><circle class="halo" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="9"/><circle class="lampd" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="3.6"/>' + (ly !== y + 4 ? '<line x1="' + (x + 4).toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + lx + '" y2="' + (ly - 4) + '" stroke="#F3EDDE" stroke-opacity=".5" stroke-width="1"/>' : '') + (show ? '<text class="lab" x="' + lx + '" y="' + ly + '">' + f.name + '</text>' : '') + '</g>';
    });
    fov.innerHTML = s;
    if (fov._wired) return; fov._wired = true;
    var st = document.createElement('style'); st.textContent = '@keyframes lit{to{opacity:1}}'; document.head.appendChild(st);
    fov.addEventListener('mousemove', function (ev) { var g = ev.target.closest('.lg'); if (!g) { ftip.style.display = 'none'; return; } var f = D.field.filter(function (x) { return x.id === g.getAttribute('data-fid'); })[0]; if (!f) return; var r = fbox.getBoundingClientRect(); ftip.innerHTML = '<b>' + f.name + '</b>' + f.city + ' · ' + (f.lat >= 0 ? '北纬 ' : '南纬 ') + Math.abs(f.lat).toFixed(1) + '° · ' + f.date.slice(5).replace('-', '/') + '<br>当天昼长 ' + hm(dayLen(f.lat, isoDoy(f.date))) + ' · ' + f.rule; ftip.style.display = 'block'; var tx = ev.clientX - r.left + 14, ty = ev.clientY - r.top + 14; if (tx > r.width - 270) tx = ev.clientX - r.left - 274; ftip.style.left = tx + 'px'; ftip.style.top = ty + 'px'; });
    fov.addEventListener('mouseleave', function () { ftip.style.display = 'none'; });
    fov.addEventListener('click', function (ev) { var g = ev.target.closest('.lg'); if (!g) return; var f = D.field.filter(function (x) { return x.id === g.getAttribute('data-fid'); })[0]; var card = f && document.getElementById('n-' + f.node); if (card) card.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); });
  }
  buildField();
  var fsz = 0; window.addEventListener('resize', function () { clearTimeout(fsz); fsz = setTimeout(function () { var sm = ((fbox && fbox.clientWidth) || 1200) < 700; if (sm !== FSM) buildField(); }, 150); });

  /* ---------- 序章 · 这十天：镜头推进的夜光地图 + 昼带 */
  var J = D.stage || [], jstage = $('#jstage');
  if (jstage && J.length) {
    var jk = $('#jk'), jdate = $('#jdate'), jt = $('#jt'), jdl = $('#jdl'), jdls = $('#jdls'), lads = $$('.lad', jstage), jsteps = $$('.jstep'), dbrows = {}, dots = {}, bands = $$('.wmap .nb', jstage);
    var scene = $('#jscene'), wmap = $('#wmap'), hud = $('#jhud'), dlbox = $('#jdlbox');
    $$('.dbrow', jstage).forEach(function (t) { dbrows[t.getAttribute('data-city')] = t; });
    $$('.cdot', jstage).forEach(function (d) { dots[d.getAttribute('data-city')] = d; });
    var cur = -1, vb = [0, 0, 720, 360], raf = 0, litBefore = [];
    J.forEach(function (L, i) { var m = {}; if (i) { Object.keys(litBefore[i - 1]).forEach(function (k) { m[k] = 1; }); J[i - 1].lit.forEach(function (k) { m[k] = 1; }); } litBefore.push(m); });
    function toH(t) { var p = t.split(':'); return parseInt(p[0], 10) + parseInt(p[1], 10) / 60; }
    function shortHm(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + 'h' + ('0' + (m % 60)).slice(-2) + 'm'; }
    // 镜头：把这一步点亮的城市框进来，按舞台的宽高比取景，最少看 110° 经度
    function frameFor(L) {
      var W = scene.clientWidth || 720, H = scene.clientHeight || 360, A = W / H, xs = [], ys = [];
      L.lit.forEach(function (id) { var c = D.cities[id]; if (c) { xs.push((c.lon + 180) * 2); ys.push((90 - c.lat) * 2); } });
      if (!xs.length) return [0, 0, 720, 720 / A];
      var minx = Math.min.apply(null, xs) - 56, maxx = Math.max.apply(null, xs) + 56, miny = Math.min.apply(null, ys) - 44, maxy = Math.max.apply(null, ys) + 44;
      var w = Math.max(maxx - minx, 220), h = Math.max(maxy - miny, 110);
      if (w / h < A) w = h * A; else h = w / A;
      if (w > 720) { w = 720; h = w / A; }
      var x = (minx + maxx) / 2 - w / 2, y = (miny + maxy) / 2 - h / 2;
      x = Math.max(0, Math.min(720 - w, x));
      y = h <= 360 ? Math.max(0, Math.min(360 - h, y)) : (360 - h) / 2;
      return [x, y, w, h];
    }
    function setVB(v) { wmap.setAttribute('viewBox', v.map(function (n) { return n.toFixed(2); }).join(' ')); scaleDots(v); }
    function scaleDots(v) { var ppu = (scene.clientWidth || 720) / v[2], k = 1.1 / ppu; Object.keys(dots).forEach(function (id) { var d = dots[id]; d.setAttribute('transform', 'translate(' + d.getAttribute('data-x') + ' ' + d.getAttribute('data-y') + ') scale(' + k.toFixed(3) + ')'); }); }
    function flyTo(v, done) {
      cancelAnimationFrame(raf);
      if (reduced) { vb = v; setVB(v); if (done) done(); return; }
      var from = vb.slice(), t0 = performance.now(), dur = 1100;
      (function step(now) {
        var k = Math.min(1, (now - t0) / dur), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        vb = from.map(function (a, i) { return a + (v[i] - a) * e; }); setVB(vb);
        if (k < 1) raf = requestAnimationFrame(step); else if (done) done();
      })(t0);
    }
    // 标签避让：先给点亮的城市找位置，再给其余城市；躲开 HUD、昼长框、其他城市的点和已放的标签
    function placeLabels(v, L) {
      var W = scene.clientWidth || 720, H = scene.clientHeight || 360, ppu = W / v[2], sr = scene.getBoundingClientRect();
      function box(el) { var r = el.getBoundingClientRect(); return { x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height }; }
      var taken = [box(hud), box(dlbox)], pos = {};
      Object.keys(dots).forEach(function (id) { var d = dots[id]; pos[id] = { x: (parseFloat(d.getAttribute('data-x')) - v[0]) * ppu, y: (parseFloat(d.getAttribute('data-y')) - v[1]) * ppu }; taken.push({ x: pos[id].x - 5, y: pos[id].y - 5, w: 10, h: 10 }); var P = pos[id], under = taken.slice(0, 2).some(function (q) { return P.x > q.x - 6 && P.x < q.x + q.w + 6 && P.y > q.y - 6 && P.y < q.y + q.h + 6; }); d.classList.toggle('under', under && L.lit.indexOf(id) < 0); });
      var order = L.lit.slice(); Object.keys(dots).forEach(function (id) { if (order.indexOf(id) < 0) order.push(id); });
      var DIRS = { t: [0, -9, 'middle'], b: [0, 15, 'middle'], r: [8, 4, 'start'], l: [-8, 4, 'end'] };
      order.forEach(function (id) {
        var d = dots[id], t = d.querySelector('text'), n = t.textContent.length, tw = n * 11.5 + 2, th = 13, p = pos[id], lit = L.lit.indexOf(id) >= 0;
        if (p.x < -20 || p.x > W + 20 || p.y < -20 || p.y > H + 20) { d.classList.remove('lab'); return; }
        var pref = d.getAttribute('data-off') || 't', tries = [pref].concat(['t', 'b', 'r', 'l'].filter(function (k) { return k !== pref; })), best = null;
        for (var i = 0; i < tries.length; i++) {
          var dd = DIRS[tries[i]], lx = p.x + dd[0] * 1.1, ly = p.y + dd[1] * 1.1, bx = dd[2] === 'middle' ? lx - tw / 2 : dd[2] === 'start' ? lx : lx - tw, b = { x: bx - 2, y: ly - th + 2, w: tw + 4, h: th + 2 };
          if (b.x < 2 || b.y < 2 || b.x + b.w > W - 2 || b.y + b.h > H - 2) continue;
          var hit = taken.some(function (q) { return b.x < q.x + q.w && b.x + b.w > q.x && b.y < q.y + q.h && b.y + b.h > q.y; });
          if (!hit) { best = { d: dd, b: b }; break; }
          if (!best && lit && i === 0) best = { d: dd, b: b, forced: true };
        }
        if (!best) { d.classList.remove('lab'); return; }
        t.setAttribute('x', best.d[0]); t.setAttribute('y', best.d[1]); t.setAttribute('text-anchor', best.d[2]); d.classList.add('lab'); taken.push(best.b);
      });
    }
    function setLevel(i) {
      if (i === cur || !J[i]) return; cur = i; var L = J[i], p = L.date.split('-');
      jk.textContent = L.kicker; jdate.innerHTML = parseInt(p[1], 10) + ' 月 ' + parseInt(p[2], 10) + ' 日<small>' + L.wd + '</small>'; jt.textContent = L.title;
      var mc = L.cities[L.main], mcity = D.cities[L.main];
      jdl.textContent = hm(mc.dl); jdls.textContent = mcity.name_zh + ' 昼长 · 日落 ' + mc.set;
      Object.keys(L.cities).forEach(function (cid) {
        var c = L.cities[cid], r = dbrows[cid];
        if (r) {
          var rs = toH(c.rise), ss = toH(c.set), bar = $('.dbb', r);
          bar.style.left = (rs / 24 * 100).toFixed(2) + '%'; bar.style.width = ((ss - rs) / 24 * 100).toFixed(2) + '%';
          $('.dbv', r).textContent = shortHm(c.dl); r.title = D.cities[cid].name_zh + '：日出 ' + c.rise + '，日落 ' + c.set + '（当地标准时）';
          r.classList.toggle('lit', !!c.on); r.classList.toggle('main', cid === L.main); $('.lamp', r).classList.toggle('off', !c.on);
        }
        if (dots[cid]) { dots[cid].classList.toggle('on', !!c.on); dots[cid].classList.toggle('was', !c.on && !!litBefore[i][cid]); }
      });
      bands.forEach(function (b) { var lat = parseFloat(b.getAttribute('data-lat')) - 5, n = 1 - dayLen(lat, L.doy) / 24; b.setAttribute('opacity', Math.max(0, Math.min(.75, (n - .42) * 1.9)).toFixed(2)); });
      var bi = $('#jb-' + i), bu = $('#jbu-' + i), bs = $('#jbs-' + i);
      if (bi) { bi.textContent = hm(mc.dl); bu.textContent = mcity.name_zh + ' · 昼长'; bs.textContent = '日出 ' + mc.rise + '，日落 ' + mc.set + '（当地标准时，不含夏令时）· ' + (mcity.lat >= 0 ? '北纬 ' : '南纬 ') + Math.abs(mcity.lat) + '° · ' + mcity.koppen; }
      lads.forEach(function (b, k) { b.classList.toggle('on', k === i); b.classList.toggle('done', k < i); });
      jsteps.forEach(function (s, k) { s.classList.toggle('on', k === i); });
      var v = frameFor(L); Object.keys(dots).forEach(function (id) { dots[id].classList.remove('lab'); });
      flyTo(v, function () { placeLabels(v, L); });
    }
    // 每张卡的大数字先填好（静态可见）
    J.forEach(function (L, i) { var mc = L.cities[L.main], mcity = D.cities[L.main], bi = $('#jb-' + i); if (bi) { bi.textContent = hm(mc.dl); $('#jbu-' + i).textContent = mcity.name_zh + ' · 昼长'; $('#jbs-' + i).textContent = '日出 ' + mc.rise + '，日落 ' + mc.set + '（当地标准时，不含夏令时）· ' + (mcity.lat >= 0 ? '北纬 ' : '南纬 ') + Math.abs(mcity.lat) + '° · ' + mcity.koppen; } });
    function pickLevel() {
      var mid = window.innerHeight * 0.5, best = 0, bestD = Infinity;
      for (var k = 0; k < jsteps.length; k++) { var r = jsteps[k].getBoundingClientRect(); if (r.top <= mid && r.bottom >= mid) { best = k; break; } var d = Math.min(Math.abs(r.top - mid), Math.abs(r.bottom - mid)); if (d < bestD) { bestD = d; best = k; } }
      if (jstage.getBoundingClientRect().top > window.innerHeight || jsteps[jsteps.length - 1].getBoundingClientRect().bottom < 0) return;
      setLevel(best);
    }
    var jt2 = false, rsz = 0;
    window.addEventListener('scroll', function () { if (jt2) return; jt2 = true; requestAnimationFrame(function () { jt2 = false; pickLevel(); }); }, { passive: true });
    window.addEventListener('resize', function () { clearTimeout(rsz); rsz = setTimeout(function () { if (cur >= 0) { var v = frameFor(J[cur]); vb = v; setVB(v); placeLabels(v, J[cur]); } pickLevel(); }, 120); });
    lads.forEach(function (b) { b.addEventListener('click', function () { jsteps[parseInt(b.getAttribute('data-lvl'), 10)].scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); }); });
    setLevel(0); pickLevel();
  }

  /* ---------- 年轮标签：扇出排列。节点按角度落在环上，标签按环的左右两侧排成两列，引线相连；字号随容器宽度定 */
  function wheelLabels(svg, rot) {
    if (!svg) return; rot = rot || 0;
    var cx = parseFloat(svg.getAttribute('data-cx')), cy = parseFloat(svg.getAttribute('data-cy')), R0 = parseFloat(svg.getAttribute('data-r0')), W = parseFloat(svg.getAttribute('data-w')), H = parseFloat(svg.getAttribute('data-h'));
    var px = svg.getBoundingClientRect().width || W, scale = px / W, fs = Math.min(15, Math.max(10.5 / scale, 10.5)), gap = fs * 1.28, pad = fs;
    var ld = $('.leaders', svg), lb = $('.labels', svg); if (!ld || !lb) return;
    var sides = { L: [], R: [] };
    $$('.fx', svg).forEach(function (g) {
      var d = parseInt(g.getAttribute('data-doy'), 10), a = (d - 1) / 365 * 2 * Math.PI - Math.PI / 2 + rot * Math.PI / 180, c = Math.cos(a), sn = Math.sin(a);
      var it = { id: g.getAttribute('data-node'), lane: g.getAttribute('data-lane') || '', name: g.getAttribute('data-name') || '', x: cx + R0 * c, y: cy + R0 * sn, ideal: cy + (R0 + 46) * sn, dim: g.classList.contains('dim'), on: g.classList.contains('on') };
      sides[c < 0 ? 'L' : 'R'].push(it);
    });
    var lines = '', texts = '';
    Object.keys(sides).forEach(function (side) {
      var arr = sides[side].sort(function (p, q) { return p.ideal - q.ideal; }), n = arr.length; if (!n) return;
      var ys = arr.map(function (p) { return Math.max(pad, Math.min(H - pad, p.ideal)); });
      for (var i = 1; i < n; i++) ys[i] = Math.max(ys[i], ys[i - 1] + gap);
      if (ys[n - 1] > H - pad) { ys[n - 1] = H - pad; for (var j = n - 2; j >= 0; j--) ys[j] = Math.min(ys[j], ys[j + 1] - gap); }
      if (ys[0] < pad) { ys[0] = pad; for (var k = 1; k < n; k++) ys[k] = Math.max(ys[k], ys[k - 1] + gap); }
      var lx = side === 'L' ? cx - R0 - 30 : cx + R0 + 30, anchor = side === 'L' ? 'end' : 'start', ex = side === 'L' ? lx + 5 : lx - 5, room = (side === 'L' ? lx : W - lx) - 6;
      arr.forEach(function (p, i) {
        var cls = (p.on ? ' on' : '') + (p.dim ? ' dim' : ''), est = 0, f = fs;
        for (var q = 0; q < p.name.length; q++) est += p.name.charCodeAt(q) > 255 ? 1 : 0.56;
        if (est * fs > room) f = Math.max(9, room / est);
        lines += '<path class="ld' + cls + '" data-node="' + p.id + '" data-lane="' + p.lane + '" d="M' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + ' L' + ex.toFixed(1) + ' ' + ys[i].toFixed(1) + '"/>';
        texts += '<text class="wl' + cls + '" data-node="' + p.id + '" data-lane="' + p.lane + '" x="' + lx.toFixed(1) + '" y="' + ys[i].toFixed(1) + '" text-anchor="' + anchor + '" dominant-baseline="middle" font-size="' + f.toFixed(1) + '" tabindex="0" role="button">' + p.name.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</text>';
      });
    });
    ld.innerHTML = lines; lb.innerHTML = texts;
  }
  window.YZ.wheelLabels = wheelLabels;
  $$('svg.wheel').forEach(function (sv) { wheelLabels(sv, 0); });
  var wlt = 0; window.addEventListener('resize', function () { clearTimeout(wlt); wlt = setTimeout(function () { $$('svg.wheel').forEach(function (sv) { wheelLabels(sv, parseFloat(sv.getAttribute('data-rot') || '0')); }); }, 150); });

  /* ---------- 年轮 ↔ 节点卡 */
  var fxEls = $$('#threshold .wheel .fx[data-node]'), cards = $$('.ncard[data-node]');
  function lightNode(id) { fxEls.forEach(function (g) { g.classList.toggle('on', g.getAttribute('data-node') === id); }); $$('#threshold .wheel .wl, #threshold .wheel .ld').forEach(function (t) { t.classList.toggle('on', t.getAttribute('data-node') === id); }); }
  document.addEventListener('click', function (ev) {
    var g = ev.target.closest('.fx[data-node], .wl[data-node]'); if (!g) return;
    var id = g.getAttribute('data-node'), card = document.getElementById('n-' + id); if (!card) return;
    card.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); lightNode(id); card.classList.add('pulse'); setTimeout(function () { card.classList.remove('pulse'); }, 1200);
  });
  document.addEventListener('keydown', function (ev) { if ((ev.key === 'Enter' || ev.key === ' ') && ev.target.classList && (ev.target.classList.contains('fx') || ev.target.classList.contains('wl'))) { ev.preventDefault(); ev.target.click(); } });
  if (cards.length && 'IntersectionObserver' in window) {
    var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) lightNode(e.target.getAttribute('data-node')); }); }, { rootMargin: '-45% 0px -45% 0px' });
    cards.forEach(function (c) { nio.observe(c); });
  }
  var lchips = $('#lane-chips');
  if (lchips) lchips.addEventListener('click', function (ev) {
    var b = ev.target.closest('button[data-lane]'); if (!b) return; var ln = b.getAttribute('data-lane');
    $$('button', lchips).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    fxEls.forEach(function (g) { g.classList.toggle('dim', ln !== 'all' && g.getAttribute('data-lane') !== ln); });
    $$('#threshold .wheel .wl, #threshold .wheel .ld').forEach(function (t) { t.classList.toggle('dim', ln !== 'all' && t.getAttribute('data-lane') !== ln); });
    cards.forEach(function (c) { c.classList.toggle('dim', ln !== 'all' && c.getAttribute('data-lane') !== ln); });
  });

  /* ---------- 第三章 同与异：排序与展开 */
  var cmp = $('#cmpbody');
  if (cmp) {
    var rows = $$('.cmprow', cmp), hd = $('#cmphd');
    hd.addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-sort]'); if (!b) return; var key = b.getAttribute('data-sort'), asc = b.getAttribute('data-dir') !== 'desc';
      $$('button', hd).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); if (x !== b) x.removeAttribute('data-dir'); });
      b.setAttribute('data-dir', asc ? 'desc' : 'asc');
      rows.sort(function (p, q) { var a = p.getAttribute('data-' + key), c = q.getAttribute('data-' + key), na = parseFloat(a), nc = parseFloat(c); var r = (!isNaN(na) && !isNaN(nc)) ? na - nc : String(a).localeCompare(String(c), 'zh'); return asc ? r : -r; });
      rows.forEach(function (r) { cmp.appendChild(r); });
    });
    cmp.addEventListener('click', function (ev) { var b = ev.target.closest('.cmpbtn'); if (!b) return; b.closest('.cmprow').classList.toggle('open'); b.textContent = b.closest('.cmprow').classList.contains('open') ? '收起' : '详情'; });
  }
})();
