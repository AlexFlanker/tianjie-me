(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
  var fmt = function (v) { v = Number(v); if (v >= 1e8) return num(v / 1e8, 4) + ' 亿'; if (v >= 100) return num(v, 0); if (v >= 10) return num(v, 1); return num(v, 2); };
  var srcs = function (ss) { if (!ss || !ss.length) return ''; return '<p class="src">来源：' + ss.map(function (s) { return s.u ? '<a href="' + esc(s.u) + '" target="_blank" rel="noopener">' + esc(s.t) + '</a>' : esc(s.t); }).join('；') + '</p>'; };
  var conf = function (c) { var k = { '高': 'h', '中': 'm', '低': 'l' }[c] || 'm'; return '<span class="conf ' + k + '">' + esc(c || '中') + '</span>'; };

  /* ---------- 深浅色 */
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
  });

  /* ---------- 入场 */
  var fades = $$('.fade');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else { fades.forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- 章节导航与进度 */
  var nav = $('#cnav'), prog = $('#prog');
  var links = $$('[data-nav]');
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-nav')); });
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
      links.forEach(function (a, i) {
        var on = i === cur;
        if (on !== a.classList.contains('on')) {
          a.classList.toggle('on', on);
          if (on && nav) { var r = a.getBoundingClientRect(), rr = nav.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) a.parentNode.scrollLeft += r.left - rr.left - 20; }
        }
      });
    });
  }
  setNavH(); onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { setNavH(); onScroll(); });


  /* ---------- 卷首指标带：进入视口时从 0 数到目标值（只播一次） */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fmtN = function (v, dec) { v = Number(v); if (dec) return v.toFixed(dec); if (v >= 1e8) return num(v / 1e8, 4) + ' 亿'; if (v >= 100) return num(v, 0); if (v >= 10) return num(v, 1); return num(v, 2); };
  function countTo(el, to, dec, ms) {
    var from = parseFloat(el.getAttribute('data-cur') || '0') || 0;
    if (reduced || !ms) { el.textContent = fmtN(to, dec); el.setAttribute('data-cur', to); return; }
    var t0 = performance.now();
    var useLog = from > 0 && to > 0 && Math.max(from, to) / Math.min(from, to) > 20;
    function tick(t) {
      var p = Math.min(1, (t - t0) / ms); var e = 1 - Math.pow(1 - p, 3);
      var v = useLog ? Math.exp(Math.log(from) + (Math.log(to) - Math.log(from)) * e) : from + (to - from) * e;
      el.textContent = fmtN(p < 1 ? v : to, dec);
      if (p < 1) requestAnimationFrame(tick); else el.setAttribute('data-cur', to);
    }
    requestAnimationFrame(tick);
  }
  var cnts = $$('.cnt[data-to]');
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { countTo(e.target, parseFloat(e.target.getAttribute('data-to')), parseInt(e.target.getAttribute('data-dec') || '0', 10), 1100); cio.unobserve(e.target); } }); }, { threshold: .4 });
    cnts.forEach(function (el) { cio.observe(el); });
  } else { cnts.forEach(function (el) { countTo(el, parseFloat(el.getAttribute('data-to')), parseInt(el.getAttribute('data-dec') || '0', 10), 0); }); }

  /* ---------- 序章 · 速度之旅 */
  var J = D.journey || [], jstage = $('#jstage');
  if (jstage && J.length) {
    var needle = $('#g-needle'), gfill = $('#g-fill'), jnum = $('#jnum'), jalt = $('#jalt'), jk = $('#jk'), jt = $('#jt'), jidx = $('#jidx'), scene = $('.jscene', jstage);
    var vehs = $$('.veh', jstage), lads = $$('.lad', jstage), jsteps = $$('.jstep');
    if (gfill) gfill.setAttribute('pathLength', '1');
    var cur = -1, moveT = null;
    function setLevel(i, instant) {
      if (i === cur || !J[i]) return;
      var prev = cur; cur = i; var L = J[i];
      if (needle) needle.style.transform = 'rotate(' + (-135 + 270 * L.f) + 'deg)';
      if (gfill) gfill.style.strokeDasharray = L.f + ' 1';
      countTo(jnum, L.kmh, 0, instant ? 0 : 900);
      if (jalt) jalt.textContent = num(L.kmh / 1.609344, L.kmh < 100 ? 1 : 0) + ' mph · Mach ' + (L.kmh / 1225 < 0.01 ? (L.kmh / 1225).toFixed(4) : L.kmh / 1225 > 1000 ? num(L.kmh / 1225, 0) : (L.kmh / 1225).toFixed(2)) + ' · 北京到上海 ' + (function (h) { return h >= 1 ? num(h, 1) + ' 小时' : h * 60 >= 1 ? num(h * 60, 1) + ' 分钟' : num(h * 3600, 2) + ' 秒'; })(D.tool1.bjsh / L.kmh);
      if (jk) jk.textContent = L.kicker; if (jt) jt.textContent = L.name; if (jidx) jidx.textContent = (i < 9 ? '0' : '') + (i + 1);
      vehs.forEach(function (v, k) {
        if (k === i) { v.classList.remove('out'); v.classList.add('on'); }
        else if (k === prev) { v.classList.remove('on'); v.classList.add('out'); setTimeout(function () { v.classList.remove('out'); }, 600); }
        else v.classList.remove('on', 'out');
      });
      lads.forEach(function (b, k) { b.classList.toggle('on', k === i); b.classList.toggle('done', k < i); });
      jsteps.forEach(function (s, k) { s.classList.toggle('on', k === i); });
      if (scene && !instant && !reduced) {
        scene.style.setProperty('--op', String(Math.min(.7, .15 + L.f * .6)));
        scene.classList.add('moving'); clearTimeout(moveT); moveT = setTimeout(function () { scene.classList.remove('moving'); }, 1400);
      }
    }
    function pickLevel() {
      var mid = window.innerHeight * 0.5, best = 0, bestD = Infinity;
      for (var k = 0; k < jsteps.length; k++) {
        var r = jsteps[k].getBoundingClientRect();
        if (r.top <= mid && r.bottom >= mid) { best = k; bestD = 0; break; }
        var d = Math.min(Math.abs(r.top - mid), Math.abs(r.bottom - mid));
        if (d < bestD) { bestD = d; best = k; }
      }
      var sr = jstage.getBoundingClientRect();
      if (sr.top > window.innerHeight || jsteps[jsteps.length - 1].getBoundingClientRect().bottom < 0) return;
      setLevel(best, cur < 0);
    }
    var jt2 = false;
    window.addEventListener('scroll', function () { if (jt2) return; jt2 = true; requestAnimationFrame(function () { jt2 = false; pickLevel(); }); }, { passive: true });
    window.addEventListener('resize', pickLevel);
    lads.forEach(function (b) { b.addEventListener('click', function () { var k = parseInt(b.getAttribute('data-lvl'), 10); jsteps[k].scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); }); });
    setLevel(0, true); pickLevel();
  }

  /* ---------- 卷首速度尺 */
  var rcard = $('#rcard');
  var REF = { walk: 5, bolt: 44.72, cheetah: 98, hsr: 350, airliner: 900, sound: 1225, orbital: 28440, light: 1079252848.8 };
  function showTick(id) {
    var s = D.scale[id]; if (!s || !rcard) return;
    $$('.ruler .tick').forEach(function (t) { t.classList.toggle('on', t.getAttribute('data-id') === id); });
    var v = Number(s.kmh);
    var cmp = [['步行', v / REF.walk, '倍'], ['博尔特', v / REF.bolt, '倍'], ['高铁', v / REF.hsr, '倍'], ['音速', v / REF.sound, '倍'], ['光速', v / REF.light * 100, '%']];
    rcard.innerHTML = '<div class="v">' + fmt(v) + '<small>km/h</small></div><div class="t">' + esc(s.label) + (s.year ? ' <span class="small">' + esc(s.year) + '</span>' : '') + ' ' + conf(s.conf) + '</div>'
      + '<p>' + esc(s.note || '') + '</p><div class="cmp">' + cmp.map(function (c) { var x = c[1]; var t = c[2] === '%' ? (x < 0.01 ? x.toExponential(2) : num(x, 3)) + ' %' : (x < 0.1 ? num(x, 3) : x < 10 ? num(x, 2) : num(x, 0)) + ' ' + c[2]; return '<span>' + c[0] + ' <b>' + t + '</b></span>'; }).join('') + '</div>' + srcs(s.sources);
  }
  $$('.ruler .tick').forEach(function (t) {
    t.addEventListener('click', function () { showTick(t.getAttribute('data-id')); });
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showTick(t.getAttribute('data-id')); } });
  });
  if (rcard) showTick(rcard.getAttribute('data-first'));

  /* ---------- 矩阵详情 */
  var mxd = $('#mxd');
  function showCell(key) {
    var c = D.cells[key]; if (!c || !mxd) return;
    $$('.cell').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-cell') === key); });
    var also = c.also ? '<dt>同格另一条</dt><dd><b>' + esc(c.also.subject) + '</b> · ' + esc(c.also.speed) + ' · ' + esc(c.also.who) + '。' + esc(c.also.why || '') + (c.also.note ? ' ' + esc(c.also.note) : '') + ' ' + conf(c.also.conf) + srcs(c.also.sources) + '</dd>' : '';
    var ph = c.img ? '<figure class="ph"><img src="' + esc(c.img.file) + '" alt="' + esc(c.img.alt) + '" loading="lazy"><figcaption>' + esc(c.img.cap) + ' 图：' + esc(c.img.credit) + '。</figcaption></figure>' : '<div class="ph none">本格没有合规照片，只用文字。</div>';
    mxd.innerHTML = '<div class="txt"><div class="kicker">' + esc(c.track) + ' · ' + esc(c.era) + '</div><h3>' + esc(c.subject) + '</h3><p class="big">' + fmt(c.kmh) + '<small>km/h</small></p><p class="spd">' + esc(c.speed) + ' ' + conf(c.conf) + '</p>'
      + '<dl><dt>年份</dt><dd>' + esc(c.year) + '</dd><dt>谁</dt><dd>' + esc(c.who) + (c.where ? '，' + esc(c.where) : '') + '</dd><dt>为什么是它</dt><dd>' + esc(c.why) + '</dd>' + (c.note ? '<dt>口径</dt><dd>' + esc(c.note) + '</dd>' : '') + also + '</dl>' + srcs(c.sources) + '</div>' + ph;
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.cell[data-cell]'); if (!b) return;
    showCell(b.getAttribute('data-cell'));
    mxd.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  });
  if (mxd) showCell(mxd.getAttribute('data-first'));
  var mxwrap = $('#mxwrap'), mxhead = $('#mxhead');
  if (mxwrap && mxhead) mxwrap.addEventListener('scroll', function () { mxhead.scrollLeft = mxwrap.scrollLeft; }, { passive: true });

  /* ---------- 卡片筛选 */
  var chips = $('#chips'), cards = $$('#cardgrid .card'), ccnt = $('#ccnt');
  function applyFilter(tag) {
    var n = 0;
    cards.forEach(function (c) { var on = tag === '全部' || c.getAttribute('data-tag') === tag; c.classList.toggle('hide', !on); if (on) { n++; c.classList.add('in'); } });
    if (ccnt) ccnt.textContent = n + ' 张';
  }
  if (chips) {
    chips.addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-tag]'); if (!b) return;
      $$('button', chips).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      applyFilter(b.getAttribute('data-tag'));
    });
    applyFilter('全部');
  }

  /* ---------- 小工具一：速度换算 */
  var sv = $('#spd-v'), su = $('#spd-u'), sout = $('#spd-out');
  function calcSpeed() {
    if (!sv || !sout) return;
    var v = parseFloat(sv.value); if (!(v >= 0)) { sout.innerHTML = ''; return; }
    var kmh = v * parseFloat(su.value);
    var rows = [
      ['换算', fmt(kmh) + ' km/h', num(kmh / 3.6, 2) + ' m/s · ' + num(kmh / 1.609344, 1) + ' mph · ' + num(kmh / 1.852, 1) + ' 节 · Mach ' + num(kmh / 1225, 3) + '（海平面）'],
      ['相当于步行', num(kmh / REF.walk, 1) + ' 倍', '成人常速 5 km/h'],
      ['相当于博尔特峰值', num(kmh / REF.bolt, 2) + ' 倍', '44.72 km/h（2009 柏林，60–80 m 分段）'],
      ['相当于猎豹', num(kmh / REF.cheetah, 2) + ' 倍', '98 km/h（辛辛那提动物园 Sarah，2012）'],
      ['相当于高铁', num(kmh / REF.hsr, 2) + ' 倍', '350 km/h 商业运营'],
      ['相当于客机巡航', num(kmh / REF.airliner, 2) + ' 倍', '约 900 km/h，Mach 0.85'],
      ['占第一宇宙速度', num(kmh / REF.orbital * 100, 2) + ' %', '7.9 km/s = 28,440 km/h'],
      ['占光速', (kmh / REF.light * 100 < 0.001 ? (kmh / REF.light * 100).toExponential(2) : num(kmh / REF.light * 100, 4)) + ' %', 'c = 299,792,458 m/s'],
    ];
    if (kmh > 0) {
      var hC = D.tool1.china / kmh, hB = D.tool1.bjsh / kmh;
      var t = function (h) { return h >= 48 ? num(h / 24, 1) + ' 天' : h >= 1 ? num(h, 1) + ' 小时' : h * 60 >= 1 ? num(h * 60, 1) + ' 分钟' : num(h * 3600, 1) + ' 秒'; };
      rows.push(['横穿中国东西', t(hC), '约 ' + num(D.tool1.china) + ' km，不停不转弯']);
      rows.push(['北京到上海', t(hB), '京沪高铁里程 ' + num(D.tool1.bjsh) + ' km']);
    }
    sout.innerHTML = rows.map(function (r) { return '<li><span>' + r[0] + '<small>' + r[2] + '</small></span><b>' + r[1] + '</b></li>'; }).join('');
  }
  if (sv) { sv.addEventListener('input', calcSpeed); su.addEventListener('change', calcSpeed); calcSpeed(); }
  $$('#tools .presets button[data-v]').forEach(function (b) { b.addEventListener('click', function () { su.value = '1'; sv.value = b.getAttribute('data-v'); calcSpeed(); }); });

  /* ---------- 小工具二：0–100 ↔ g ↔ μ */
  var at = $('#acc-t'), a60 = $('#acc-60'), ga = $('#g-a'), gg = $('#g-g'), gmu = $('#g-mu'), gv = $('#g-v');
  function calcAcc() {
    if (!at) return;
    var t = parseFloat(at.value); if (!(t > 0)) return;
    var dv = (a60.checked ? 96.56 : 100) / 3.6;
    var a = dv / t, g = a / 9.81;
    ga.textContent = num(a, 2); gg.textContent = num(g, 2); gmu.textContent = num(g, 2);
    var v;
    if (g <= 0.45) v = '很从容：家用车的范围。GB 7258—2026 媒体转述的「默认 5 秒」对应约 0.57 g，这台车在它之下。';
    else if (g <= 0.75) v = '性能车的范围：需要 μ ≈ ' + num(g, 2) + '，普通轮胎在干沥青上能给到（μ 约 1.0–1.2），还有余量。';
    else if (g <= 1.2) v = '接近轮胎的极限：需要 μ ≈ ' + num(g, 2) + '，必须四驱、起步控制、好胎和干净路面；这是电动超跑 2 秒上下的世界。';
    else if (g <= 1.45) v = '超过普通轮胎能给的 μ：只有赛道胶处理、半热熔胎和「1 英尺 rollout」口径才量得到（Rimac Nevera 1.74 s ≈ 1.6 g 就是这样来的）。';
    else v = '轮胎做不到：需要 μ ≈ ' + num(g, 2) + '，超过任何橡胶在沥青上的摩擦系数。要么是起步时就有大下压力（风扇 / 吸附），要么推力不经过轮胎（火箭、冷气推进器）——这正是 Roadster「0.81 秒」争论的物理核心：向上喷气只会让轮胎抓地更少，推车必须向后喷。';
    gv.innerHTML = esc(v) + ' <span class="small">（匀加速假设；' + (a60.checked ? '0–60 mph' : '0–100 km/h') + '，' + num(t, 2) + ' 秒）</span>';
  }
  if (at) { at.addEventListener('input', calcAcc); a60.addEventListener('change', calcAcc); calcAcc(); }
  $$('#tools .presets button[data-t]').forEach(function (b) { b.addEventListener('click', function () { at.value = b.getAttribute('data-t'); a60.checked = /mph/.test(b.textContent); calcAcc(); }); });
})();
