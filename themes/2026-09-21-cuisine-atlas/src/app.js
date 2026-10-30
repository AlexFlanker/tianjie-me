/* 第 1 题 v2：深浅色、入场、导航、卷首、论点；序章地图舞台；两张透镜列表；辣椒年份图；章节之间的互相跳转。 */
(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  function mk(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

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
  // 触屏拖动的方向判定：先看前 6 px 往哪走，横向才接管（竖向交给页面滚动）
  function dragIntent(e, sx, sy) { var dx = e.clientX - sx, dy = e.clientY - sy; if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return 0; return Math.abs(dx) > Math.abs(dy) ? 1 : -1; }

  /* ================= 深浅色：这一题默认是纸；切过就记住（全站同一个键） ================= */
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

  /* ================= 入场 ================= */
  var fades = $$('.fade');
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

  /* ================= 卷首：依次升起；论点：钉住时逐词点亮，放不下就随文流动 ================= */
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

  /* ================= 地图：省名按渲染尺寸换算字号（--k），省份放得下才显示名字 ================= */
  // 先看省份的外框放不放得下名字，再按面积从大到小摆，和已摆好的名字相撞就不显示（consider 可以限定参与的省）
  function Mapper(svg, onScale, consider) {
    var lbls = $$('.lbl', svg), self = this; this.k = 0;
    function fit() {
      var r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal; if (!r.width || !r.height) return;
      var k = Math.min(r.width / vb.width, r.height / vb.height); if (Math.abs(k - self.k) < 0.0005) return; self.k = k;
      svg.style.setProperty('--k', k.toFixed(4));
      var cand = [];
      lbls.forEach(function (t) {
        var c = t.getAttribute('data-code'), b = D.pbox[c], a = D.anchor[c], lw = t.textContent.length * 12 + 6;
        var ok = (b[2] - b[0]) * k >= lw && (b[3] - b[1]) * k >= 16 && (!consider || consider(c));
        if (ok) cand.push({ t: t, x: a[0] * k, y: a[1] * k, w: lw, area: (b[2] - b[0]) * (b[3] - b[1]) }); else t.classList.remove('fit');
      });
      cand.sort(function (p, q) { return q.area - p.area; });
      var placed = [];
      cand.forEach(function (o) {
        var hit = placed.some(function (p) { return Math.abs(p.x - o.x) < (p.w + o.w) / 2 + 2 && Math.abs(p.y - o.y) < 18; });
        if (!hit) placed.push(o); o.t.classList.toggle('fit', !hit);
      });
      if (onScale) onScale(k);
    }
    this.fit = fit;
    if ('ResizeObserver' in window) new ResizeObserver(fit).observe(svg); else window.addEventListener('resize', fit);
    fit();
  }
  function placeTip(tip, box, x, y) {
    var sr = box.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight, lx = x - sr.left + 16, ly = y - sr.top + 16;
    if (lx + w > sr.width - 8) lx = x - sr.left - w - 16;
    if (ly + h > sr.height - 8) ly = y - sr.top - h - 16;
    tip.style.transform = 'translate(' + Math.round(clamp(lx, 8, Math.max(8, sr.width - w - 8))) + 'px,' + Math.round(clamp(ly, 8, Math.max(8, sr.height - h - 8))) + 'px)';
  }
  var STAGE = { go: function () {} }, LISTS = { open: function () {} };

  /* ================= 序章：全屏舞台（滚动与刻度尺是同一个量 t = 第几期） ================= */
  (function initStage() {
    var pin = $('#tlpin'), stg = $('#tlstage'); if (!pin || !stg) return;
    var P = D.periods, N = P.length, S = D.stage, MODES = D.modes;
    var svg = $('#smap svg'), uses = {}, lbls = {};
    $$('use.pv', svg).forEach(function (u) { uses[u.getAttribute('data-code')] = u; });
    $$('.lbl', svg).forEach(function (t) { lbls[t.getAttribute('data-code')] = t; });
    var CODES = Object.keys(uses), chgG = $('#sm-chg'), hov = $('#sm-hov');
    var hud = $('#tlhud'), card = $('#tlcard'), legList = $('#sleglist'), legH = $('#slegh'), seg = $('#smodes'), ruler = $('#tlruler'), track = $('#rtrack'), head = $('#rhead'), tip = $('#stip');
    var el = { jkn: $('#jkn'), jks: $('#jks'), jname: $('#jname'), jyears: $('#jyears'), no: $('#tlno'), kick: $('#tlkick'), head: $('#tlhead'), text: $('#tltext'), chg: $('#tlchg'), img: $('#tlimg'), cap: $('#tlcap') };
    var marks = $$('.rmark', ruler), mbtns = $$('button[data-mode]', seg);
    var mode = 'fam';
    try { var sm = localStorage.getItem('cuisine-mode'); if (sm === 'taste' || sm === 'staple') mode = sm; } catch (e) {}
    function modeRow(m) { for (var i = 0; i < MODES.length; i++) if (MODES[i][0] === m) return MODES[i]; return MODES[0]; }

    // ---- 着色
    function regionOf(k, c) { var rs = P[k].regions; for (var i = 0; i < rs.length; i++) if (rs[i].provs.indexOf(c) >= 0) return rs[i]; return null; }
    function keyOf(k, c, m) {
      m = m || mode; var r = regionOf(k, c); if (!r) return null; var ov = P[k].ov[c] || {};
      if (m === 'fam') return { key: r.fam, css: 'fam-' + r.fam, r: r };
      if (m === 'taste') { var t = ov.taste || r.taste; return { key: t, css: 'taste-' + t, r: r }; }
      var s = ov.staple || r.staple; return { key: s, css: 'staple-' + s, r: r };
    }
    function nameOf(kk) { return mode === 'fam' ? kk.r.name : (mode === 'taste' ? D.tastes[kk.key] : D.staples[kk.key]); }
    function fillOf(css) { return css === 'staple-daomai' ? 'url(#hatch)' : 'var(--' + css + ')'; }
    function swatchOf(css) { return css === 'staple-daomai' ? 'repeating-linear-gradient(45deg,var(--staple-dao) 0 3px,var(--staple-mai) 3px 6px)' : 'var(--' + css + ')'; }
    var chgCache = {};
    function changedAt(k) {
      var key = mode + k; if (chgCache[key]) return chgCache[key];
      var out = k <= 0 ? [] : CODES.filter(function (c) { var a = keyOf(k - 1, c), b = keyOf(k, c); return a && b && a.key !== b.key; });
      return (chgCache[key] = out);
    }
    function paint(k) {
      var pm = D.palmeta[curTheme()] || {};
      CODES.forEach(function (c) { var kk = keyOf(k, c); uses[c].style.fill = kk ? fillOf(kk.css) : 'var(--map-dim)'; lbls[c].classList.toggle('on-dark', !!(kk && pm[kk.css])); });
      chgG.innerHTML = changedAt(k).map(function (c) { return '<use href="#pd-' + c + '" class="co"></use>'; }).join('');
    }
    function legend(k) {
      var ch = changedAt(k), items = [];
      legH.textContent = modeRow(mode)[2];
      if (mode === 'fam') {
        P[k].regions.forEach(function (r) { items.push({ sw: 'var(--fam-' + r.fam + ')', name: r.name, sub: r.provs.map(function (c) { return D.prov[c].short; }).join(''), codes: r.provs }); });
      } else {
        var dict = mode === 'taste' ? D.tastes : D.staples, by = {};
        CODES.forEach(function (c) { var kk = keyOf(k, c); if (kk) (by[kk.key] = by[kk.key] || []).push(c); });
        Object.keys(dict).forEach(function (key) { var cs = by[key]; if (cs) items.push({ sw: swatchOf(mode + '-' + key), name: dict[key], sub: cs.length + ' 个', codes: cs }); });
      }
      legList.textContent = '';
      items.forEach(function (it) {
        var li = mk('li', it.codes.some(function (c) { return ch.indexOf(c) >= 0; }) ? 'chg' : ''), sw = mk('i');
        sw.style.background = it.sw; li.appendChild(sw); li.appendChild(mk('span', '', it.name)); li.appendChild(mk('small', '', it.sub));
        li._codes = it.codes; li.title = it.name + '：' + it.codes.map(function (c) { return D.prov[c].name; }).join('、'); legList.appendChild(li);
      });
    }
    function dim(cs) { CODES.forEach(function (c) { uses[c].classList.toggle('dim', !!cs && cs.indexOf(c) < 0); }); }
    var legHi = null;
    legList.addEventListener('pointerover', function (e) { if (e.pointerType !== 'mouse') return; var li = e.target.closest('li'); if (li && li._codes) dim(li._codes); });
    legList.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && !legHi) dim(null); });
    legList.addEventListener('click', function (e) {
      var li = e.target.closest('li'); if (!li || !li._codes) return;
      if (legHi === li) { legHi = null; li.style.background = ''; dim(null); return; }
      if (legHi) legHi.style.background = ''; legHi = li; li.style.background = 'var(--wash-2)'; dim(li._codes);
    });

    // ---- 卡片与标题
    function hudFill(k) { var p = P[k]; el.jkn.textContent = '第 ' + (k + 1) + ' / ' + N + ' 期'; el.jks.textContent = ' · ' + p.sub; el.jname.textContent = p.name; el.jyears.textContent = p.years; }
    function chgLine(k) {
      if (k === 0) { el.chg.hidden = true; return; }
      var ch = changedAt(k), mn = modeRow(mode)[1], a = P[k - 1].regions.length, b = P[k].regions.length;
      var rg = mode === 'fam' && a !== b ? '分区从 ' + a + ' 片' + (b > a ? '分成 ' : '并成 ') + b + ' 片' : '';
      if (!ch.length) el.chg.textContent = '按「' + mn + '」看，这一期没有省份换色' + (rg ? '；' + rg : '') + '。';
      else { var nm = ch.map(function (c) { return D.prov[c].name; }); el.chg.textContent = '换了颜色（描红边）：' + (nm.length > 8 ? nm.slice(0, 8).join('、') + ' 等 ' + nm.length + ' 个' : nm.join('、')) + (rg ? '。' + rg : ''); }
      el.chg.hidden = false;
    }
    function setCardText(k) { var p = P[k], s = S[k]; el.no.textContent = (k < 9 ? '0' : '') + (k + 1); el.kick.textContent = p.name + ' · ' + p.years; el.head.textContent = s.head; el.text.textContent = s.text; chgLine(k); }
    function setCardImg(k) { var im = S[k].img; el.img.width = im.w; el.img.height = im.h; el.img.src = im.src; el.img.alt = im.alt; el.cap.textContent = im.cap; el.cap.appendChild(mk('span', 'cr', im.cr)); }
    function fitCard() {
      card.classList.remove('fit1', 'fit2', 'fit3', 'fit4');
      if (getComputedStyle(card).position !== 'absolute') { card.style.maxHeight = ''; return; }
      var cb = card.getBoundingClientRect(), hb = hud.getBoundingClientRect();
      card.style.maxHeight = Math.max(160, Math.floor(cb.bottom - hb.bottom - 24)) + 'px';
      for (var i = 1; i <= 4; i++) { if (card.scrollHeight <= card.clientHeight + 1) break; card.classList.add('fit' + i); }
    }
    // 手机上卡片在地图下方：先量出十期里最高的一张，固定最小高度，免得地图随文字长短跳动
    function cardMin() {
      card.style.minHeight = '';
      if (getComputedStyle(card).position === 'absolute') return;
      var mx = 0, cur = shownK < 0 ? 0 : shownK;
      for (var k = 0; k < N; k++) { setCardText(k); mx = Math.max(mx, card.offsetHeight); }
      setCardText(cur); card.style.minHeight = mx + 'px';
    }
    var shownK = -1, swapT = 0;
    function showStep(k) {
      if (k === shownK) return; var first = shownK < 0; shownK = k;
      [k - 1, k + 1].forEach(function (j) { if (j >= 0 && j < N) { var im = new Image(); im.src = S[j].img.src; } });
      if (first || RM.on) { setCardText(k); setCardImg(k); fitCard(); return; }
      clearTimeout(swapT); card.classList.add('swapping');
      swapT = setTimeout(function () { setCardText(shownK); setCardImg(shownK); fitCard(); card.classList.remove('swapping'); }, 200);
    }

    // ---- 省份提示：鼠标悬停跟随，点按钉住（钉住时可以去读沿革）
    var tipC = null, tipPinned = false, tipXY = [0, 0];
    function tipFill(c) {
      var kk = keyOf(curK, c); if (!kk) return false;
      var r = kk.r, pn = (D.notes[c] || {})[P[curK].id];
      tip.textContent = '';
      var h = mk('p', 'stn'), sw = mk('i'); sw.style.background = swatchOf(kk.css); h.appendChild(sw); h.appendChild(document.createTextNode(D.prov[c].name)); tip.appendChild(h);
      tip.appendChild(mk('p', 'str', mode === 'fam' ? r.name : nameOf(kk) + ' · ' + r.name));
      tip.appendChild(mk('p', 'stt', r.note));
      if (pn) tip.appendChild(mk('p', 'stp', pn));
      if (tipPinned) { var b = mk('button', 'stgo', '读' + D.prov[c].name + '的沿革 →'); b.type = 'button'; b.setAttribute('data-open-prov', c); tip.appendChild(b); }
      return true;
    }
    function tipShow(c, x, y, pinned) {
      tipC = c; tipPinned = !!pinned; tipXY = [x, y];
      if (!tipFill(c)) return;
      tip.hidden = false; tip.classList.toggle('pinned', tipPinned); placeTip(tip, stg, x, y);
      hov.setAttribute('href', '#pd-' + c);
    }
    function tipHide() { tipC = null; tipPinned = false; tip.hidden = true; tip.classList.remove('pinned'); hov.removeAttribute('href'); }
    function tipRefresh() { if (!tipC) return; tipFill(tipC); placeTip(tip, stg, tipXY[0], tipXY[1]); }
    function anchorXY(c) { var a = D.anchor[c], m = svg.getScreenCTM(); if (!m) return [0, 0]; var pt = svg.createSVGPoint(); pt.x = a[0]; pt.y = a[1]; pt = pt.matrixTransform(m); return [pt.x, pt.y]; }
    function provAt(e) { var u = e.target && e.target.closest ? e.target.closest('use.pv') : null; return u ? u.getAttribute('data-code') : null; }
    svg.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse' || tipPinned) return;
      var c = provAt(e); if (!c) { if (tipC) tipHide(); return; }
      tipShow(c, e.clientX, e.clientY, false);
    });
    svg.addEventListener('pointerleave', function () { if (!tipPinned) tipHide(); });
    svg.addEventListener('click', function (e) {
      var c = provAt(e); if (!c) { tipHide(); return; }
      if (tipPinned && tipC === c) { tipHide(); return; }
      tipShow(c, e.clientX, e.clientY, true);
    });
    document.addEventListener('pointerdown', function (e) { if (tipPinned && !tip.contains(e.target) && !svg.contains(e.target)) tipHide(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && tipC) tipHide(); });

    // ---- 着色方式：分段按钮 + 滑块
    var pill = mk('span', 'pill'); pill.setAttribute('aria-hidden', 'true'); seg.insertBefore(pill, seg.firstChild);
    var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
    var pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
    function movePill(instant) { var b = mbtns.filter(function (x) { return x.getAttribute('data-mode') === mode; })[0]; if (!b) return; if (instant) { px.set(b.offsetLeft); pw.set(b.offsetWidth); } else { px.to(b.offsetLeft); pw.to(b.offsetWidth); } }
    function setMode(m, instant) {
      mode = m; try { localStorage.setItem('cuisine-mode', m); } catch (e) {}
      mbtns.forEach(function (b) { var on = b.getAttribute('data-mode') === m; b.setAttribute('aria-checked', String(on)); b.tabIndex = on ? 0 : -1; });
      movePill(instant);
      if (curK >= 0) { paint(curK); legend(curK); cardMin(); chgLine(curK); fitCard(); if (tipC) tipRefresh(); }
    }
    seg.addEventListener('click', function (e) { var b = e.target.closest('button[data-mode]'); if (b) setMode(b.getAttribute('data-mode')); });
    seg.addEventListener('keydown', function (e) {
      if (['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp'].indexOf(e.key) < 0) return;
      var i = mbtns.findIndex(function (b) { return b.getAttribute('data-mode') === mode; }), d = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : mbtns.length - 1, n = mbtns[(i + d) % mbtns.length];
      e.preventDefault(); n.focus(); setMode(n.getAttribute('data-mode'));
    });

    // ---- 渲染
    var curK = -1;
    function render(t) {
      var k = clamp(Math.round(t), 0, N - 1);
      if (k !== curK) {
        curK = k; paint(k); legend(k); hudFill(k); showStep(k);
        marks.forEach(function (m, i) { m.classList.toggle('on', i === k); m.classList.toggle('past', i <= k); });
        ruler.setAttribute('aria-valuenow', k); ruler.setAttribute('aria-valuetext', P[k].name + '，' + P[k].years);
        if (tipC) tipRefresh();
      }
      head.style.transform = 'translateX(' + (t / (N - 1) * track.clientWidth).toFixed(1) + 'px)';
    }

    // ---- 长度：每一期约 0.55 屏
    var stageH = 0, perStep = 0, pinTop = 0;
    function layout() {
      stageH = stg.offsetHeight; perStep = Math.round(window.innerHeight * (window.innerWidth < 700 ? 0.45 : 0.55));
      pin.style.height = (stageH + (N - 1) * perStep) + 'px';
      pinTop = pin.getBoundingClientRect().top + window.scrollY;
    }
    function tFromScroll() { return clamp((window.scrollY - (pinTop - navH())) / perStep, 0, N - 1); }
    function scrollForT(t) { return pinTop - navH() + t * perStep; }

    // ---- t 是一个弹簧：滚动给目标（轻微平滑），拖动直接设，松手按速度投影后吸附到最近的一期
    var drive = 'scroll', progY = null;
    var ts = new Spring({ from: 0, damping: 1, response: 0.22, eps: 0.0015, onUpdate: function (x) { render(x); if (drive === 'fly') { progY = scrollForT(x); window.scrollTo(0, progY); } }, onRest: function () { if (drive === 'fly') drive = 'scroll'; } });
    function onScroll() {
      if (drive === 'drag') return;
      if (drive === 'fly') { if (progY !== null && Math.abs(window.scrollY - progY) > 3) drive = 'scroll'; else return; }
      var t = tFromScroll();
      if (RM.on) { ts.set(t); return; }
      ts.to(t, { damping: 1, response: 0.22 });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    ['wheel', 'touchstart'].forEach(function (ev) { window.addEventListener(ev, function () { if (drive === 'fly') drive = 'scroll'; }, { passive: true }); });
    function flyTo(t, v) { drive = 'fly'; progY = null; ts.to(clamp(t, 0, N - 1), { velocity: v || 0, damping: 1, response: 0.42 }); }
    var vt = new VTrack(), drag = null;
    function tAt(e) { var r = track.getBoundingClientRect(); return clamp((e.clientX - r.left) / r.width * (N - 1), 0, N - 1); }
    ruler.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return;
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: false, moved: false, mark: e.target.closest('.rmark'), off: 0 };
      if (e.pointerType === 'mouse') startDrag(e);
    });
    function startDrag(e) {
      drag.on = true; drive = 'drag'; ruler.classList.add('drag'); try { ruler.setPointerCapture(drag.id); } catch (er) {}
      var t = tAt(e), hx = ts.x;
      drag.off = Math.abs(t - hx) < 0.35 ? hx - t : 0;   // 抓在播放头上：保留抓取偏移；抓在别处：按下即跳过去
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
    ruler.addEventListener('pointercancel', function (e) { endDrag(e, true); if (drive === 'drag') drive = 'scroll'; });
    marks.forEach(function (m) { m.addEventListener('click', function (e) { if (e.detail === 0) flyTo(parseInt(m.getAttribute('data-step'), 10), 0); }); });
    ruler.addEventListener('keydown', function (e) {
      var k = Math.round(ts.target), t = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') t = Math.min(N - 1, k + 1);
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') t = Math.max(0, k - 1);
      else if (e.key === 'Home') t = 0; else if (e.key === 'End') t = N - 1; else return;
      e.preventDefault(); flyTo(t, 0);
    });

    // ---- 从别处跳过来：滚到那一期，并把那个省钉出提示
    STAGE.go = function (k, c) {
      k = clamp(k, 0, N - 1); pinTop = pin.getBoundingClientRect().top + window.scrollY;
      var y = scrollForT(k);
      if (!RM.on && Math.abs(window.scrollY - y) < window.innerHeight * 1.5) flyTo(k, 0);
      else { drive = 'scroll'; window.scrollTo(0, y); ts.set(k); }
      if (c) setTimeout(function () { var xy = anchorXY(c); tipShow(c, xy[0], xy[1], true); }, RM.on ? 30 : 480);
    };

    new MutationObserver(function () { if (curK >= 0) { paint(curK); if (tipC) tipRefresh(); } }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    new Mapper(svg);
    var rz = 0;
    function relayout() { layout(); var t = drive === 'scroll' ? tFromScroll() : ts.x; ts.set(t); movePill(true); cardMin(); fitCard(); }
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(relayout, 120); });
    window.addEventListener('load', relayout);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); cardMin(); fitCard(); });
    setMode(mode, true); layout(); ts.set(tFromScroll()); cardMin(); fitCard();
  })();

  /* ================= 列表：透镜分组（FLIP 补间）+ 行内展开 ================= */
  (function initLists() {
    var allRows = {};
    $$('.lrow').forEach(function (r) { allRows[r.getAttribute('data-id')] = r; });
    function toggle(r, open) { var o = open == null ? !r.classList.contains('open') : open; r.classList.toggle('open', o); var b = $('.lhead', r); if (b) b.setAttribute('aria-expanded', String(o)); }
    document.addEventListener('click', function (e) { var b = e.target.closest('.lhead'); if (!b) return; toggle(b.closest('.lrow')); });
    function scrollToRow(r) {
      var w = r.closest('.lwrap'), lb = w ? $('.lensbar', w) : null, off = navH() + (lb ? lb.offsetHeight : 0) + 8, top = r.getBoundingClientRect().top + window.scrollY - off;
      window.scrollTo({ top: Math.max(0, top), behavior: RM.on ? 'auto' : 'smooth' });
    }
    LISTS.open = function (id) {
      var r = allRows[id]; if (!r) return;
      toggle(r, true); scrollToRow(r);
      r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1400);
      try { history.replaceState(null, '', '#' + id); } catch (er) {}
    };
    function header(g) {
      var h = mk('div', 'lgh'), hh = mk('div', 'lghh'); h.setAttribute('data-g', g.k);
      hh.appendChild(mk('b', '', g.label)); if (g.sub) hh.appendChild(mk('small', '', g.sub)); h.appendChild(hh);
      if (g.desc) h.appendChild(mk('p', '', g.desc));
      return h;
    }
    $$('.lwrap[data-lw]').forEach(function (w) {
      var key = w.getAttribute('data-lw'), groups = (D.lens || {})[key], lensEl = $('.lens', w), grid = $('.lgrid', w), note = $('.lensnote', w);
      if (!groups || !lensEl || !grid) return;
      var rows = {}; $$('.lrow', grid).forEach(function (r) { rows[r.getAttribute('data-id')] = r; });
      var tabs = $$('button[data-lens]', lensEl), cur = tabs[0].getAttribute('data-lens'), total = Object.keys(rows).length, unit = key === 'lines' ? '条' : '个';
      var pill = mk('span', 'pill'); pill.setAttribute('aria-hidden', 'true'); lensEl.insertBefore(pill, lensEl.firstChild);
      var px = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.transform = 'translateX(' + x.toFixed(1) + 'px)'; } });
      var pw = new Spring({ damping: 1, response: 0.32, eps: 0.2, onUpdate: function (x) { pill.style.width = x.toFixed(1) + 'px'; } });
      function movePill(instant) { var b = tabs.filter(function (t) { return t.getAttribute('data-lens') === cur; })[0]; if (!b) return; if (instant) { px.set(b.offsetLeft); pw.set(b.offsetWidth); } else { px.to(b.offsetLeft); pw.to(b.offsetWidth); } }
      function setLens(lens) {
        if (!groups[lens] || lens === cur) return; cur = lens;
        tabs.forEach(function (t) { var on = t.getAttribute('data-lens') === lens; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
        movePill(false);
        var wt = w.getBoundingClientRect().top, inside = wt < navH() - 8, vh = window.innerHeight;
        var first = {}; if (!inside && !RM.on) Object.keys(rows).forEach(function (id) { first[id] = rows[id].getBoundingClientRect().top; });
        var frag = document.createDocumentFragment();
        groups[lens].forEach(function (g) { frag.appendChild(header(g)); g.ids.forEach(function (id) { if (rows[id]) frag.appendChild(rows[id]); }); });
        $$('.lgh', grid).forEach(function (h) { h.remove(); });
        grid.appendChild(frag);
        var tab = tabs.filter(function (t) { return t.getAttribute('data-lens') === lens; })[0];
        if (note) note.textContent = '按' + (tab ? tab.textContent : '') + '分成 ' + groups[lens].length + ' 组 · ' + total + ' ' + unit + ' · 点一行展开';
        if (inside) { window.scrollTo(0, w.getBoundingClientRect().top + window.scrollY - navH() + 1); return; }   // 已经读到列表里面：回到列表开头，不做补间
        if (RM.on) return;
        Object.keys(first).forEach(function (id) {
          var r = rows[id], now = r.getBoundingClientRect().top, dy = first[id] - now;
          if (Math.abs(dy) < 1 || (now > vh * 1.5 && first[id] > vh * 1.5) || Math.abs(dy) > vh * 2) return;
          r.style.transition = 'none'; r.style.transform = 'translateY(' + dy.toFixed(1) + 'px)';
        });
        grid.offsetHeight; // 强制回流
        Object.keys(first).forEach(function (id) { var r = rows[id]; if (!r.style.transform) return; r.style.transition = 'transform .5s cubic-bezier(.22,1,.36,1)'; r.style.transform = ''; });
        $$('.lgh', grid).forEach(function (h) { if (h.animate) h.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'cubic-bezier(.22,1,.36,1)' }); });
      }
      lensEl.addEventListener('click', function (e) { var b = e.target.closest('button[data-lens]'); if (b) setLens(b.getAttribute('data-lens')); });
      lensEl.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        var i = tabs.findIndex(function (t) { return t.getAttribute('data-lens') === cur; }), n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
        n.focus(); setLens(n.getAttribute('data-lens')); e.preventDefault();
      });
      tabs.forEach(function (t, i) { t.tabIndex = i === 0 ? 0 : -1; });
      movePill(true);
      window.addEventListener('resize', function () { movePill(true); });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { movePill(true); });
    });
    var m = /^#((?:p|d)-[\w-]+)$/.exec(location.hash || ''); if (m && allRows[m[1]]) setTimeout(function () { LISTS.open(m[1]); }, 60);
  })();

  /* ================= 第二章：辣椒——年份轴（拖动、甩、键盘、播放）驱动地图上的记录 ================= */
  (function initChili() {
    var fig = $('#chfig'); if (!fig) return;
    var C = D.chili, R = C.recs, Y0 = C.y0, Y1 = C.y1, NR = R.length;
    var box = $('#chmap'), svg = $('svg', box), uses = {}, lbls = {};
    $$('use.pv', svg).forEach(function (u) { uses[u.getAttribute('data-code')] = u; });
    $$('.lbl', svg).forEach(function (t) { lbls[t.getAttribute('data-code')] = t; });
    var dots = $$('.cdot', svg), labs = $$('.clab', svg), hov = $('#cm-hov');
    var yEl = $('#chy'), cnt = $('#chcount'), recEl = $('#chrec'), msn = $('#chmsn'), qj = $('#chq'), play = $('#chplay'), slider = $('#chslider'), track = $('#chtrack'), headEl = $('#chhead'), ticks = $$('.chtk', track), tip = $('#ctip');
    var useQJ = qj ? qj.checked : true, y = Y1, lastKey = '';
    var byProv = {}; R.forEach(function (rc, i) { (byProv[rc.p] = byProv[rc.p] || []).push(i); });
    function shown(i, yi) { return R[i].y <= yi && (useQJ || !R[i].qj); }

    // 点：放在省名下方 14 px，同一省的几条横排；半径 5 px，换算成地图单位
    function layoutDots(k) {
      var r = 5 / k, gap = 2.6 * r, dy = 14 / k;
      Object.keys(byProv).forEach(function (c) {
        var ids = byProv[c], a = D.anchor[c], n = ids.length;
        ids.forEach(function (i, j) { var d = dots[i]; d.setAttribute('r', r.toFixed(2)); d.setAttribute('cx', (a[0] + (j - (n - 1) / 2) * gap).toFixed(1)); d.setAttribute('cy', (a[1] + dy).toFixed(1)); });
      });
      labs.forEach(function (t) { var i = +t.getAttribute('data-i'), c = R[i].p, a = D.anchor[c], n = byProv[c].length; t.setAttribute('x', (a[0] + ((n - 1) / 2) * gap + r + 4 / k).toFixed(1)); t.setAttribute('y', (a[1] + dy).toFixed(1)); });
    }
    new Mapper(svg, layoutDots, function (c) { return !!byProv[c]; });

    function recCard(i, yi) {
      recEl.textContent = '';
      if (i < 0) { recEl.appendChild(mk('p', 'chrn', '到 ' + yi + ' 年，目前所见的中国书里还没有写到辣椒。')); return; }
      var r = R[i], h = mk('p', 'chrh');
      h.appendChild(mk('b', '', String(r.y))); h.appendChild(mk('span', '', D.prov[r.p].name + ' · ' + r.book));
      var tg = mk('span', 'utag u-' + r.cat); tg.appendChild(mk('i')); tg.appendChild(document.createTextNode(r.use + (r.conf === '低' ? ' · 待核' : ''))); h.appendChild(tg);
      recEl.appendChild(h);
      recEl.appendChild(mk('p', 'chrq', r.quote ? '「' + r.quote + '」' : '（原文未引）'));
      recEl.appendChild(mk('p', 'chrn', r.note));
    }
    function render(force) {
      var yi = Math.round(y);
      yEl.textContent = yi;
      headEl.style.left = ((y - Y0) / (Y1 - Y0) * 100).toFixed(3) + '%';
      slider.setAttribute('aria-valuenow', yi); slider.setAttribute('aria-valuetext', yi + ' 年');
      var key = yi + (useQJ ? 'q' : 'n'); if (key === lastKey && !force) return; lastKey = key;
      var has = {}, nrec = 0, latest = -1;
      for (var i = 0; i < NR; i++) { var v = shown(i, yi); dots[i].classList.toggle('on', v); if (v) { has[R[i].p] = 1; nrec++; latest = i; } }
      ticks.forEach(function (t, j) { t.classList.toggle('off', !useQJ && R[j].qj); });
      Object.keys(uses).forEach(function (c) { uses[c].style.fill = has[c] ? 'var(--chili-has)' : 'var(--chili-none)'; lbls[c].classList.toggle('show', !!has[c]); });
      labs.forEach(function (t) { t.classList.toggle('on', shown(+t.getAttribute('data-i'), yi)); });
      var np = Object.keys(has).length;
      cnt.textContent = np ? np + ' 个省级行政区有记录 · ' + nrec + ' 条' : '还没有记录';
      recCard(latest, yi);
      var ms = null; C.ms.forEach(function (m) { if (m.y <= yi) ms = m; });
      msn.textContent = ms ? '同一时期：' + ms.y + ' 年，' + ms.t : '';
      if (tipC) tipFill(tipC);
    }

    // 年份是一个弹簧：拖动直接设，松手按速度投影、吸附到最近的一条记录（12 年以内）
    var ys = new Spring({ from: Y1, damping: 1, response: 0.3, eps: 0.05, onUpdate: function (x) { y = x; render(); } });
    function yAt(e) { var r = track.getBoundingClientRect(); return Y0 + clamp((e.clientX - r.left) / r.width, 0, 1) * (Y1 - Y0); }
    function visYears() { var out = []; R.forEach(function (rc) { if (useQJ || !rc.qj) out.push(rc.y); }); return out; }
    function snap(t) { var best = null, bd = 1e9; visYears().forEach(function (v) { var d = Math.abs(v - t); if (d < bd) { bd = d; best = v; } }); return bd <= 12 ? best : Math.round(t); }
    var vt = new VTrack(), drag = null;
    slider.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return; stopPlay();
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: false, off: 0 };
      if (e.pointerType === 'mouse') start(e);
    });
    function start(e) {
      drag.on = true; slider.classList.add('drag'); try { slider.setPointerCapture(drag.id); } catch (er) {}
      var t = yAt(e); drag.off = Math.abs(t - ys.x) < 4 ? ys.x - t : 0;
      vt.reset(); vt.add(t + drag.off); ys.set(clamp(t + drag.off, Y0, Y1));
    }
    slider.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.on) { var it = dragIntent(e, drag.sx, drag.sy); if (it === 1) start(e); else if (it === -1) drag = null; return; }
      var t = clamp(yAt(e) + drag.off, Y0, Y1); vt.add(t); ys.set(t);
    });
    function end(e, cancel) {
      if (!drag || e.pointerId !== drag.id) return;
      var d0 = drag; drag = null; slider.classList.remove('drag');
      if (!d0.on) { if (!cancel) ys.to(snap(yAt(e))); return; }
      var v = vt.v(); ys.to(clamp(snap(ys.x + project(v, 0.995)), Y0, Y1), { velocity: v });
    }
    slider.addEventListener('pointerup', function (e) { end(e, false); });
    slider.addEventListener('pointercancel', function (e) { end(e, true); });
    slider.addEventListener('keydown', function (e) {
      var vy = visYears(), cur = Math.round(ys.target), t = null, i;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { t = Y1; for (i = 0; i < vy.length; i++) if (vy[i] > cur) { t = vy[i]; break; } }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { t = Y0; for (i = vy.length - 1; i >= 0; i--) if (vy[i] < cur) { t = vy[i]; break; } }
      else if (e.key === 'Home') t = Y0; else if (e.key === 'End') t = Y1;
      else if (e.key === 'PageUp') t = cur + 10; else if (e.key === 'PageDown') t = cur - 10; else return;
      e.preventDefault(); stopPlay(); ys.to(clamp(t, Y0, Y1));
    });

    // 播放：记录密集的 1655–1770 年放慢
    var playing = false, raf = 0, lastT = 0;
    function speed(v) { return v >= 1655 && v <= 1770 ? 14 : 40; }
    function step(now) {
      if (!playing) return;
      var dt = Math.min(0.05, (now - lastT) / 1000); lastT = now;
      var ny = Math.min(Y1, ys.x + dt * speed(ys.x)); ys.set(ny);
      if (ny >= Y1) { stopPlay(); return; }
      raf = requestAnimationFrame(step);
    }
    function startPlay() {
      if (RM.on) { ys.set(Y1); return; }
      if (ys.x >= Y1 - 0.5) ys.set(Y0);
      playing = true; play.classList.add('on'); play.setAttribute('aria-label', '暂停'); lastT = performance.now(); raf = requestAnimationFrame(step);
    }
    function stopPlay() { if (!playing) return; playing = false; cancelAnimationFrame(raf); play.classList.remove('on'); play.setAttribute('aria-label', '播放'); }
    play.addEventListener('click', function () { if (playing) stopPlay(); else startPlay(); });
    if (qj) qj.addEventListener('change', function () { useQJ = qj.checked; render(true); });
    // 第一次有一半进入视野时，从 1585 年自动放一遍（减少动效时不放，直接停在全部记录）
    if ('IntersectionObserver' in window && !RM.on) {
      var auto = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { auto.disconnect(); if (!playing && !drag) { ys.set(Y0); startPlay(); } } }); }, { threshold: 0.5 });
      auto.observe(svg);
    }

    // 提示：指一个省（或它的点）列出到当前年份为止的记录；点按钉住
    var tipC = null, tipPinned = false, tipXY = [0, 0];
    function tipFill(c) {
      var yi = Math.round(y), all = byProv[c] || [], list = all.filter(function (i) { return shown(i, yi); });
      tip.textContent = ''; tip.appendChild(mk('p', 'stn', D.prov[c].name));
      if (!list.length) { tip.appendChild(mk('p', 'stt', all.length ? '到 ' + yi + ' 年还没有记录。' : '这次没有查到这里的首载记录。')); }
      else { var ul = mk('ul', 'stl'); list.forEach(function (i) { var r = R[i], li = mk('li'); li.appendChild(mk('b', '', String(r.y))); li.appendChild(mk('span', '', r.book + ' · ' + r.use + (r.conf === '低' ? ' · 待核' : ''))); ul.appendChild(li); }); tip.appendChild(ul); }
      placeTip(tip, box, tipXY[0], tipXY[1]);
    }
    function codeAt(e) {
      var t = e.target; if (!t || !t.closest) return null;
      var d = t.closest('.cdot'); if (d) return R[+d.getAttribute('data-i')].p;
      var u = t.closest('use.pv'); return u ? u.getAttribute('data-code') : null;
    }
    function tipShow(c, x, yy, pinned) { tipC = c; tipPinned = !!pinned; tipXY = [x, yy]; tip.hidden = false; tipFill(c); hov.setAttribute('href', '#pd-' + c); }
    function tipHide() { tipC = null; tipPinned = false; tip.hidden = true; hov.removeAttribute('href'); }
    svg.addEventListener('pointermove', function (e) { if (e.pointerType !== 'mouse' || tipPinned) return; var c = codeAt(e); if (!c) { if (tipC) tipHide(); return; } tipShow(c, e.clientX, e.clientY, false); });
    svg.addEventListener('pointerleave', function () { if (!tipPinned) tipHide(); });
    svg.addEventListener('click', function (e) { var c = codeAt(e); if (!c || (tipPinned && tipC === c)) { tipHide(); return; } tipShow(c, e.clientX, e.clientY, true); });
    document.addEventListener('pointerdown', function (e) { if (tipPinned && !box.contains(e.target)) tipHide(); });
    render(true);
  })();

  /* ================= 章节之间：「在地图上看」→ 序章那一期；「读沿革」→ 第三章那一行 ================= */
  document.addEventListener('click', function (e) {
    var g = e.target.closest('[data-goto]');
    if (g) { e.preventDefault(); STAGE.go(parseInt(g.getAttribute('data-goto'), 10), g.getAttribute('data-prov')); return; }
    var o = e.target.closest('[data-open-prov]');
    if (o) { e.preventDefault(); LISTS.open('p-' + o.getAttribute('data-open-prov')); }
  });
})();
