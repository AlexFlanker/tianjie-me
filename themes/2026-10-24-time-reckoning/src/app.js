(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  /* ---------- 深浅色：按钮在导航里，写「白天读 / 夜里读」；用户切过就记住 */
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  function curTheme() { return root.getAttribute('data-theme') || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); }
  function themeLabel() { if (!tb) return; var d = curTheme() === 'dark'; tb.textContent = d ? '白天读' : '夜里读'; tb.setAttribute('aria-label', d ? '换成浅色' : '换成深色'); }
  if (tb) { themeLabel(); tb.addEventListener('click', function () {
    var next = curTheme() === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next); themeLabel();
    try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
  }); }

  /* ---------- v2 卷首：标题依次升起；论点逐词点亮 */
  (function initHero() {
    var h = $('#top'); if (!h) return;
    var rs = $$('.rise', h);
    if (reduced) { rs.forEach(function (el) { el.classList.add('in'); }); return; }
    requestAnimationFrame(function () { rs.forEach(function (el, i) { el.style.transitionDelay = (0.15 + Math.min(i * 0.08, 0.4)).toFixed(2) + 's'; el.classList.add('in'); }); });
  })();
  (function initTagline() {
    var sec = $('#tagsec'); if (!sec) return;
    var ws = $$('.tagl .w', sec), rest = $('.tagrest', sec), tick = false;
    function upd() {
      tick = false;
      if (reduced) { ws.forEach(function (w) { w.classList.add('on'); }); if (rest) rest.classList.add('on'); return; }
      var r = sec.getBoundingClientRect(), span = sec.offsetHeight - window.innerHeight;
      var p = clamp(-r.top / (span > 0 ? span : 1), 0, 1), n = Math.floor(p * (ws.length + 3));
      ws.forEach(function (w, i) { var on = i < n; if (on !== w.classList.contains('on')) w.classList.toggle('on', on); });
      if (rest) rest.classList.toggle('on', n >= ws.length + 1);
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener('resize', upd); upd();
  })();

  /* ---------- 入场 */
  var fades = $$('.fade').concat($$('.rise').filter(function (el) { return !el.closest('#top'); }));
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
  var fmtN = function (v, dec) { v = Number(v); return dec ? v.toFixed(dec) : num(v, 0); };
  function countTo(el, to, dec, ms) {
    if (reduced || !ms) { el.textContent = fmtN(to, dec); return; }
    var t0 = performance.now();
    (function tick(t) { var p = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - p, 3); el.textContent = fmtN(to * e, dec); if (p < 1) requestAnimationFrame(tick); else el.textContent = fmtN(to, dec); })(t0);
  }
  var cnts = $$('.cnt[data-to]');
  if ('IntersectionObserver' in window) { var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { countTo(e.target, parseFloat(e.target.getAttribute('data-to')), parseInt(e.target.getAttribute('data-dec') || '0', 10), 1100); cio.unobserve(e.target); } }); }, { threshold: .4 }); cnts.forEach(function (el) { cio.observe(el); }); }
  else cnts.forEach(function (el) { countTo(el, parseFloat(el.getAttribute('data-to')), parseInt(el.getAttribute('data-dec') || '0', 10), 0); });

  /* ---------- 序章 · 对历与对表 */
  var J = D.stage || [], jstage = $('#jstage');
  if (jstage && J.length) {
    var jk = $('#jk'), jt = $('#jt'), jidx = $('#jidx'), lads = $$('.lad', jstage), jsteps = $$('.jstep'), tiles = {}, dots = {}, gmt = $('#gmt-line');
    $$('.ctile', jstage.parentNode).forEach(function (t) { tiles[t.getAttribute('data-city')] = t; });
    $$('.cdot', jstage).forEach(function (d) { dots[d.getAttribute('data-city')] = d; });
    var cur = -1;
    function setLevel(i) {
      if (i === cur || !J[i]) return; cur = i; var L = J[i];
      jk.textContent = L.kicker; jt.textContent = L.title; jidx.textContent = L.year;
      Object.keys(L.cities).forEach(function (cid) {
        var c = L.cities[cid], t = tiles[cid]; if (!t) return;
        $('.cn small', t).textContent = c.time; $('.dl', t).innerHTML = c.dial; $('.pl b', t).textContent = c.plate; $('.pl span', t).textContent = c.sub; t.title = c.label;
        t.classList.toggle('chg', !!c.changed); if (dots[cid]) dots[cid].classList.toggle('on', !!c.changed);
        if (c.changed && !reduced) { t.classList.remove('flip'); void t.offsetWidth; t.classList.add('flip'); }
      });
      if (gmt) gmt.classList.toggle('on', !!L.gmt);
      lads.forEach(function (b, k) { b.classList.toggle('on', k === i); b.classList.toggle('done', k < i); });
      jsteps.forEach(function (s, k) { s.classList.toggle('on', k === i); });
    }
    function pickLevel() {
      var mid = window.innerHeight * 0.5, best = 0, bestD = Infinity;
      for (var k = 0; k < jsteps.length; k++) { var r = jsteps[k].getBoundingClientRect(); if (r.top <= mid && r.bottom >= mid) { best = k; break; } var d = Math.min(Math.abs(r.top - mid), Math.abs(r.bottom - mid)); if (d < bestD) { bestD = d; best = k; } }
      if (jstage.getBoundingClientRect().top > window.innerHeight || jsteps[jsteps.length - 1].getBoundingClientRect().bottom < 0) return;
      setLevel(best);
    }
    var jt2 = false;
    window.addEventListener('scroll', function () { if (jt2) return; jt2 = true; requestAnimationFrame(function () { jt2 = false; pickLevel(); }); }, { passive: true });
    window.addEventListener('resize', pickLevel);
    lads.forEach(function (b) { b.addEventListener('click', function () { jsteps[parseInt(b.getAttribute('data-lvl'), 10)].scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); }); });
    setLevel(0); pickLevel();
  }

  /* ---------- 泳道图 ↔ 节点卡：点节点跳卡片；卡片过视口中线时点亮节点与地图落点 */
  var ndEls = $$('.lanes .nd'), pdEls = $$('.pd'), cards = $$('.ncard[data-node]');
  function lightNode(id) {
    ndEls.forEach(function (g) { g.classList.toggle('on', g.getAttribute('data-node') === id); });
    pdEls.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-node') === id); });
  }
  document.addEventListener('click', function (ev) {
    var g = ev.target.closest('.nd[data-node],.pd[data-node]'); if (!g) return;
    var id = g.getAttribute('data-node'), card = document.getElementById('n-' + id); if (!card) return;
    card.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); lightNode(id); card.classList.add('pulse'); setTimeout(function () { card.classList.remove('pulse'); }, 1200);
  });
  document.addEventListener('keydown', function (ev) { if ((ev.key === 'Enter' || ev.key === ' ') && ev.target.classList && ev.target.classList.contains('nd')) { ev.preventDefault(); ev.target.click(); } });
  if (cards.length && 'IntersectionObserver' in window) {
    var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) lightNode(e.target.getAttribute('data-node')); }); }, { rootMargin: '-45% 0px -45% 0px' });
    cards.forEach(function (c) { nio.observe(c); });
  }
  /* 刻度筛选 */
  var fchips = $('#scale-chips');
  if (fchips) fchips.addEventListener('click', function (ev) {
    var b = ev.target.closest('button[data-scale]'); if (!b) return; var sc = b.getAttribute('data-scale');
    $$('button', fchips).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    ndEls.forEach(function (g) { g.classList.toggle('dim', sc !== 'all' && (g.getAttribute('data-scales') || '').indexOf(sc) < 0); });
    cards.forEach(function (c) { c.classList.toggle('dim', sc !== 'all' && (c.getAttribute('data-scales') || '').indexOf(sc) < 0); });
  });
})();
