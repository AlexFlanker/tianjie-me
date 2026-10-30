/* 第 1 题 v2 外壳：深浅色、入场、吸顶导航与进度、卷首升起、论点逐词点亮。地图与长卷的逻辑在 atlas.js（v1）。 */
(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  var RM = { on: false };
  try { var rmq = window.matchMedia('(prefers-reduced-motion: reduce)'); RM.on = rmq.matches; var rmc = function (e) { RM.on = e.matches; }; if (rmq.addEventListener) rmq.addEventListener('change', rmc); else if (rmq.addListener) rmq.addListener(rmc); } catch (e) {}

  /* ---------- 深浅色：这一题默认是纸；切过就记住（全站同一个键） */
  var tb = $('#theme-btn');
  function curTheme() { return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }
  function themeLabel() { if (!tb) return; var d = curTheme() === 'dark'; tb.textContent = d ? '白天读' : '夜里读'; tb.setAttribute('aria-label', d ? '换成浅色' : '换成深色'); }
  if (tb) {
    themeLabel();
    tb.addEventListener('click', function () {
      var next = curTheme() === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next); themeLabel();
      try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
    });
  }

  /* ---------- 入场 */
  var fades = $$('.fade');
  if ('IntersectionObserver' in window && !RM.on) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (n) { io.observe(n); });
  } else { fades.forEach(function (n) { n.classList.add('in'); }); }

  /* ---------- 章节导航与进度 */
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
      var y = window.scrollY + navH() + 80, cur = -1;
      for (var i = 0; i < secs.length; i++) if (secs[i] && secs[i].getBoundingClientRect().top + window.scrollY <= y) cur = i;
      links.forEach(function (a, i) {
        var on = i === cur;
        if (on !== a.classList.contains('on')) {
          a.classList.toggle('on', on);
          if (on && nav) { var r = a.getBoundingClientRect(), rr = nav.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) a.parentNode.scrollLeft += r.left - rr.left - 20; }
        }
      });
    });
  }
  setNavH(); onScrollNav();
  window.addEventListener('scroll', onScrollNav, { passive: true });
  window.addEventListener('resize', function () { setNavH(); onScrollNav(); });

  /* ---------- 卷首：依次升起 */
  (function initHero() {
    var h = $('#top'); if (!h) return;
    var rs = $$('.rise', h);
    if (RM.on) { rs.forEach(function (n) { n.classList.add('in'); }); return; }
    requestAnimationFrame(function () { rs.forEach(function (n, i) { n.style.transitionDelay = (0.15 + Math.min(i * 0.08, 0.4)).toFixed(2) + 's'; n.classList.add('in'); }); });
  })();

  /* ---------- 论点：钉住时按滚动进度逐词点亮；放不下就随文流动、按位置点亮 */
  (function initTagline() {
    var sec = $('#tagsec'); if (!sec) return;
    var ws = $$('.tagl .w', sec), rest = $('.tagrest', sec), tagl = $('.tagl', sec), inner = $('.tagstick > .wide', sec), tick = false;
    function upd() {
      tick = false;
      if (RM.on) { ws.forEach(function (w) { w.classList.add('on'); }); if (rest) rest.classList.add('on'); return; }
      var nh = navH(), avail = window.innerHeight - nh;
      var fits = inner.offsetHeight + 48 <= avail;
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
})();
