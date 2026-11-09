/* 号外 · 奶酪 — app.js（每个模块一层 IIFE，局部变量不串） */
(function () {
  'use strict';
  var root = document.documentElement, D = window.PB || {};
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var RM = false; try { RM = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  function lang() { return root.lang === 'en' ? 'en' : 'zh'; }
  function L(o) { if (o == null) return ''; if (typeof o === 'string') return o; return o[lang()] || o.zh || o.en || ''; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function famColor(f) { return 'var(--f-' + (f || 'hard') + ')'; }
  function Spring(o) { this.x = o.x || 0; this.v = 0; this.target = this.x; this.resp = o.response || 0.4; this.cb = o.onUpdate; this.raf = 0; this.last = 0; }
  Spring.prototype.to = function (t) { var s = this; s.target = t; if (RM) { s.x = t; s.v = 0; s.cb(s.x); return; } if (s.raf) return; s.last = performance.now(); s.raf = requestAnimationFrame(function step(now) { var dt = Math.min(0.032, (now - s.last) / 1000); s.last = now; var w = 2 * Math.PI / s.resp, a = -w * w * (s.x - s.target) - 2 * w * s.v; s.v += a * dt; s.x += s.v * dt; if (Math.abs(s.x - s.target) < 0.0005 && Math.abs(s.v) < 0.002) { s.x = s.target; s.v = 0; s.cb(s.x); s.raf = 0; return; } s.cb(s.x); s.raf = requestAnimationFrame(step); }); };
  Spring.prototype.set = function (x) { if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0; this.x = this.target = x; this.v = 0; this.cb(x); };

  /* ---------- 语言与深浅色 ---------- */
  (function () {
    var lb = $('#langbtn'), tb = $('#themebtn');
    function setTitle() { if (D.meta) document.title = lang() === 'en' ? D.meta.title_en + ' | Tianjie · Extra' : D.meta.title_zh + '｜一周一题 · 号外'; }
    function lbl() { if (lb) { lb.textContent = lang() === 'en' ? '中文' : 'EN'; lb.setAttribute('aria-label', lang() === 'en' ? '切换到中文' : 'Switch to English'); } }
    lbl(); setTitle();
    if (lb) lb.addEventListener('click', function () { root.lang = lang() === 'en' ? 'zh-CN' : 'en'; try { localStorage.setItem('xcheese-lang', root.lang); } catch (e) {} lbl(); setTitle(); window.dispatchEvent(new Event('langchange')); });
    function cur() { return root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'); }
    function tl() { if (tb) { tb.textContent = cur() === 'dark' ? '☀' : '☾'; tb.setAttribute('aria-label', cur() === 'dark' ? 'Light' : 'Dark'); } }
    tl(); if (tb) tb.addEventListener('click', function () { root.setAttribute('data-theme', cur() === 'dark' ? 'light' : 'dark'); try { localStorage.setItem('yzyt-theme', root.getAttribute('data-theme')); } catch (e) {} tl(); window.dispatchEvent(new Event('themechange')); });
  })();

  /* ---------- 入场 ---------- */
  (function () {
    var els = $$('.fade');
    if ('IntersectionObserver' in window && !RM) { var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' }); els.forEach(function (el) { io.observe(el); }); }
    else els.forEach(function (el) { el.classList.add('in'); });
    var rs = $$('.hero .rise'); requestAnimationFrame(function () { rs.forEach(function (el, i) { el.style.transitionDelay = (0.15 + i * 0.12) + 's'; el.classList.add('in'); }); });
  })();

  /* ---------- 论点逐词「熟成」 ---------- */
  (function () {
    if (!$('.thesis')) return; var t = false;
    function upd() { t = false; $$('.thesis .lines').forEach(function (ln) { if (ln.offsetParent === null) return; var ws = $$('.w', ln), r = ln.getBoundingClientRect(), vh = innerHeight; var p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1); if (RM) p = 1; var n = Math.round(p * ws.length * 1.15); ws.forEach(function (w, i) { w.classList.toggle('on', i < n); }); }); }
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

  /* ---------- 00 沿革：全屏舞台 + 刻度尺 ---------- */
  (function () {
    var st = $('#stage'); if (!st || !D.stage) return;
    var steps = D.stage, idx = -1, card = $('.card', st), ruler = $('.ruler', st), ph = $('.ph', st), cap = $('.cap2', st), imgs = {};
    st.style.setProperty('--steps', steps.length);
    steps.forEach(function (s) { if (s.img && !imgs[s.img]) { var im = new Image(); im.alt = ''; im.decoding = 'async'; im.loading = 'lazy'; im.src = s.img; if (s.fit === 'contain') { im.className = 'contain'; if (s.pw) im.style.setProperty('--pw', s.pw + 'px'); } ph.appendChild(im); imgs[s.img] = im; } });
    function pos(i) { var pad = innerWidth < 700 ? 8 : 5; return steps.length < 2 ? 50 : pad + (100 - 2 * pad) * i / (steps.length - 1); }
    function ticks() { ruler.innerHTML = '<div class="hd"></div>'; steps.forEach(function (s, i) { var b = document.createElement('div'); b.className = 'tk'; b.style.left = pos(i) + '%'; b.textContent = L(s.label); b.addEventListener('click', function () { go(i); }); ruler.appendChild(b); }); }
    var head; var sp = new Spring({ x: 0, response: 0.4, onUpdate: function (x) { head = head || $('.hd', ruler); var n = steps.length - 1, i = Math.floor(x), f = x - i, a = pos(clamp(i, 0, n)), b = pos(clamp(i + 1, 0, n)); if (head) head.style.left = (a + (b - a) * f) + '%'; } });
    function show(i, force) {
      i = clamp(i, 0, steps.length - 1); if (i === idx && !force) return; idx = i; var s = steps[i];
      $$('.tk', ruler).forEach(function (t, k) { t.classList.toggle('on', k === i); });
      for (var k in imgs) imgs[k].classList.toggle('on', k === s.img);
      card.classList.add('out');
      setTimeout(function () {
        var yt = L(s.yr); card.innerHTML = '<div class="mv"><div class="yr' + (yt.length > 9 ? ' long' : '') + '">' + esc(yt) + '</div><div class="era">' + esc(L(s.era)) + '</div><h3>' + esc(L(s.title)) + '</h3><p>' + L(s.text) + '</p>' + (s.tags && s.tags.length ? '<div class="tags">' + s.tags.map(function (d) { return '<span>' + esc(L(d)) + '</span>'; }).join('') + '</div>' : '') + '</div>';
        card.classList.remove('out'); cap.innerHTML = s.cap ? L(s.cap) : '';
      }, RM || force ? 0 : 180);
      sp.to(i);
    }
    function nav() { var n = $('#cnav'); return n ? n.offsetHeight : 0; }
    function frac() { var r = st.getBoundingClientRect(), tot = st.offsetHeight - (innerHeight - nav()); return clamp(-r.top / Math.max(1, tot), 0, 1); }
    function go(i) { var tot = st.offsetHeight - (innerHeight - nav()); scrollTo({ top: st.offsetTop - nav() + tot * (i + 0.5) / steps.length, behavior: RM ? 'auto' : 'smooth' }); }
    var dragging = false, sx = 0, moved = false;
    function onScroll() { if (!dragging) show(Math.min(steps.length - 1, Math.floor(frac() * steps.length))); }
    var tk = false; addEventListener('scroll', function () { if (!tk) { tk = true; requestAnimationFrame(function () { tk = false; onScroll(); }); } }, { passive: true });
    function xToI(cx) { var r = ruler.getBoundingClientRect(), p = (cx - r.left) / r.width * 100, best = 0, bd = 1e9; steps.forEach(function (s, i) { var d = Math.abs(pos(i) - p); if (d < bd) { bd = d; best = i; } }); return best; }
    ruler.addEventListener('pointerdown', function (e) { if (e.target.classList.contains('tk')) return; dragging = true; moved = false; sx = e.clientX; ruler.setPointerCapture(e.pointerId); });
    ruler.addEventListener('pointermove', function (e) { if (!dragging) return; if (Math.abs(e.clientX - sx) > 6) moved = true; if (moved) show(xToI(e.clientX)); });
    ruler.addEventListener('pointerup', function (e) { if (!dragging) return; dragging = false; go(xToI(e.clientX)); }); ruler.addEventListener('pointercancel', function () { dragging = false; });
    ruler.tabIndex = 0; ruler.setAttribute('role', 'slider'); ruler.setAttribute('aria-label', 'Timeline');
    ruler.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); } });
    addEventListener('langchange', function () { ticks(); head = null; sp.set(idx); show(idx, true); });
    addEventListener('resize', function () { ticks(); head = null; var k = idx; idx = -1; show(k, true); sp.set(k); });
    ticks(); show(0, true); onScroll();
  })();

  /* ---------- 01 做一块：工作台 ---------- */
  (function () {
    var b = $('#bench'); if (!b || !D.bench) return;
    var B = D.bench, styles = B.styles, cur = styles[0], si = 0, timer = 0;
    var list = $('.styles', b), shot = $('.shot', b), lab = $('.lab', shot), capEl = $('.cap', shot), rail = $('.rail .steps', b), say = $('.say', b), playBtn = $('[data-act=play]', b);
    var imgs = {};
    function img(src) { if (!src) return null; if (!imgs[src]) { var im = new Image(); im.alt = ''; im.loading = 'lazy'; im.src = src; shot.insertBefore(im, shot.firstChild); imgs[src] = im; } return imgs[src]; }
    var famBox = $('.fam', b);
    function renderList() { if (famBox) famBox.innerHTML = cur.famdef ? '<b>' + esc(L(cur.famName)) + '</b> ' + esc(L(cur.famdef)) : ''; list.innerHTML = styles.map(function (s, i) { return '<button type="button" class="' + (s === cur ? 'on' : '') + '" data-i="' + i + '"><i style="background:' + famColor(s.fam) + '"></i><b>' + esc(L(s.name)) + '</b><em>' + esc(L(s.origin)) + '</em></button>'; }).join(''); $$('button', list).forEach(function (bt) { bt.addEventListener('click', function () { stop(); cur = styles[+bt.getAttribute('data-i')]; si = 0; renderList(); renderRail(); show(); }); }); }
    function renderRail() { rail.innerHTML = cur.steps.map(function (s, i) { return '<button type="button" data-i="' + i + '" class="' + (i < si ? 'done' : '') + (i === si ? ' on' : '') + '">' + (i + 1) + '<b>' + esc(L(s.title)) + '</b></button>'; }).join(''); $$('button', rail).forEach(function (bt) { bt.addEventListener('click', function () { stop(); si = +bt.getAttribute('data-i'); show(); }); }); }
    function gauge(sel, val, frac, txt) { var g = $(sel, b); $('b', g).textContent = txt; $('.bar i', g).style.width = (clamp(frac, 0, 1) * 100) + '%'; }
    function show() {
      var s = cur.steps[si], im = img(s.img || cur.img);
      for (var k in imgs) imgs[k].classList.toggle('on', imgs[k] === im);
      lab.innerHTML = '<div class="stepno">' + esc(L(cur.name)) + ' · ' + (si + 1) + ' / ' + cur.steps.length + '</div><h4>' + esc(L(s.title)) + '</h4>';
      capEl.innerHTML = s.cap ? L(s.cap) : (cur.cap ? L(cur.cap) : '');
      gauge('.g.t', s.temp, s.temp == null ? 0 : clamp(s.temp, 0, 95) / 95, s.td ? L(s.td) : '—');
      gauge('.g.ph', s.ph, s.ph == null ? 0 : (6.8 - s.ph) / (6.8 - 4.4), s.phd ? 'pH ' + s.phd : '—');
      gauge('.g.time', null, s.tf == null ? 0 : s.tf, L(s.time) || '—');
      gauge('.g.step', null, (si + 1) / cur.steps.length, (si + 1) + ' / ' + cur.steps.length);
      say.innerHTML = '<p>' + L(s.text) + '</p>' + (s.sci ? '<p class="sci">' + L(s.sci) + '</p>' : '');
      $$('button', rail).forEach(function (bt, i) { bt.classList.toggle('on', i === si); bt.classList.toggle('done', i < si); if (i === si) { var r = bt.getBoundingClientRect(), rr = rail.getBoundingClientRect(); if (r.left < rr.left || r.right > rr.right) rail.scrollLeft += r.left - rr.left - 40; } });
      window.dispatchEvent(new CustomEvent('cheesestyle', { detail: cur.id }));
    }
    function stop() { if (timer) clearInterval(timer); timer = 0; if (playBtn) playBtn.textContent = L({ zh: '▶ 播放', en: '▶ Play' }); }
    if (playBtn) playBtn.addEventListener('click', function () { if (timer) { stop(); return; } if (si >= cur.steps.length - 1) si = 0; else si++; show(); playBtn.textContent = L({ zh: '❚❚ 暂停', en: '❚❚ Pause' }); timer = setInterval(function () { if (si >= cur.steps.length - 1) { stop(); return; } si++; show(); }, RM ? 900 : 3200); });
    $('[data-act=prev]', b).addEventListener('click', function () { stop(); si = Math.max(0, si - 1); show(); });
    $('[data-act=next]', b).addEventListener('click', function () { stop(); si = Math.min(cur.steps.length - 1, si + 1); show(); });
    addEventListener('langchange', function () { renderList(); renderRail(); show(); stop(); });
    renderList(); renderRail(); show(); stop();
  })();

  /* ---------- 01 熟成时间尺（对数） ---------- */
  (function () {
    var box = $('#agebar'); if (!box || !D.age) return; var A = D.age, sel = null, W0 = 0;
    function draw() {
      var W = box.clientWidth, narrow = W < 560, m = { l: narrow ? 92 : 150, r: 16, t: 28, b: 24 }, rowH = 22, H = m.t + m.b + A.length * rowH; W0 = W;
      var lo = Math.log10(0.5), hi = Math.log10(3650 * 1.2);
      var X = function (d) { return m.l + (W - m.l - m.r) * (Math.log10(Math.max(d, 0.5)) - lo) / (hi - lo); };
      var ticks = [[1, { zh: '1 天', en: '1 day' }], [7, { zh: '1 周', en: '1 wk' }], [30, { zh: '1 月', en: '1 mo' }], [180, { zh: '半年', en: '6 mo' }], [365, { zh: '1 年', en: '1 yr' }], [1095, { zh: '3 年', en: '3 yr' }], [3650, { zh: '10 年', en: '10 yr' }]];
      var g = ticks.map(function (t) { return '<line x1="' + X(t[0]) + '" x2="' + X(t[0]) + '" y1="' + (m.t - 6) + '" y2="' + (H - m.b) + '" stroke="var(--line)"/><text x="' + X(t[0]) + '" y="' + (m.t - 12) + '" text-anchor="middle">' + esc(L(t[1])) + '</text>'; }).join('');
      A.forEach(function (a, i) {
        var y = m.t + i * rowH + 4, x1 = X(a.min), x2 = X(Math.max(a.max, a.min * 1.15)), on = sel === a.id;
        g += '<text x="' + (m.l - 8) + '" y="' + (y + 11) + '" text-anchor="end" style="fill:' + (on ? 'var(--ink)' : 'var(--ink-2)') + ';font-weight:' + (on ? 700 : 400) + '">' + esc(L(a.name)) + '</text>';
        g += '<rect x="' + x1 + '" y="' + y + '" width="' + Math.max(4, x2 - x1) + '" height="14" rx="7" fill="' + famColor(a.fam) + '" opacity="' + (sel && !on ? 0.35 : 1) + '"' + (on ? ' stroke="var(--ink)" stroke-width="1.5"' : '') + '/>';
      });
      box.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '" role="img">' + g + '</svg>';
    }
    addEventListener('cheesestyle', function (e) { sel = e.detail; draw(); });
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (box.clientWidth !== W0) draw(); }, 120); });
    addEventListener('langchange', draw); draw();
  })();

  /* ---------- 02 品鉴光谱 + 一组品鉴 ---------- */
  (function () {
    var box = $('#spec'); if (!box || !D.spec) return;
    var S = D.spec, plot = $('.plot .cv', box), side = $('.side', box), fbox = $('.filters', box), sel = S[0], flight = [], filt = 'all', W0 = 0;
    var FILT = [{ id: 'all', zh: '全部', en: 'All' }, { id: 'cow', zh: '牛奶', en: 'Cow' }, { id: 'goat', zh: '山羊奶', en: 'Goat' }, { id: 'sheep', zh: '绵羊奶', en: 'Sheep' }, { id: 'buffalo', zh: '水牛奶', en: 'Buffalo' }];
    function shown(c) { return filt === 'all' || (c.milk || '').indexOf(filt) >= 0; }
    function draw() {
      var W = plot.clientWidth, H = Math.round(Math.min(560, Math.max(340, W * 0.7))), m = { l: 36, r: 16, t: 16, b: 40 }; W0 = W;
      var X = function (v) { return m.l + (W - m.l - m.r) * (v - 0.5) / 10; }, Y = function (v) { return m.t + (H - m.t - m.b) * (1 - (v - 0.5) / 10); };
      var g = '';
      for (var v = 1; v <= 10; v++) { g += '<line class="ax" x1="' + X(v) + '" x2="' + X(v) + '" y1="' + m.t + '" y2="' + (H - m.b) + '" opacity=".5"/><line class="ax" x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" opacity=".5"/>'; }
      g += '<text x="' + ((W + m.l) / 2) + '" y="' + (H - 8) + '" text-anchor="middle">' + esc(L({ zh: '风味强度：温和 → 浓烈', en: 'Intensity: mild → bold' })) + '</text>';
      g += '<text transform="translate(12,' + ((H - m.b + m.t) / 2) + ') rotate(-90)" text-anchor="middle">' + esc(L({ zh: '质地：软 → 硬', en: 'Texture: soft → hard' })) + '</text>';
      
      var narrow = W < 520, boxes = [], pos = {}, seen = {};
      // 同一格的点围成小圈，避免完全重叠
      S.forEach(function (c, i) { var k = c.x + ',' + c.y; seen[k] = (seen[k] || 0) + 1; c._k = seen[k] - 1; });
      S.forEach(function (c, i) { var n = seen[c.x + ',' + c.y], a = c._k / n * 2 * Math.PI - Math.PI / 2, r = n > 1 ? 9 : 0; pos[i] = [X(c.x) + r * Math.cos(a), Y(c.y) + r * Math.sin(a)]; });
      function fits(b) { if (b[0] < m.l || b[2] > W - 4) return false; for (var j = 0; j < boxes.length; j++) { var o = boxes[j]; if (b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]) return false; } return true; }
      var order = S.map(function (c, i) { return i; }).sort(function (a, b) { var A = S[a], Bc = S[b]; var pa = (A === sel ? 0 : flight.indexOf(A) >= 0 ? 1 : A.label ? 2 : 3), pb = (Bc === sel ? 0 : flight.indexOf(Bc) >= 0 ? 1 : Bc.label ? 2 : 3); return pa - pb; });
      S.forEach(function (c, i) { var p = pos[i]; boxes.push([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7]); });
      var labels = '';
      order.forEach(function (i) {
        var c = S[i], on = c === sel, inF = flight.indexOf(c) >= 0, vis = shown(c);
        if (!(on || inF || (!narrow && vis && c.label))) return;
        var t = L(c.name), w = t.length * (lang() === 'en' ? 6.6 : 12) + 4, p = pos[i];
        var cands = [[p[0] + 10, p[1] + 4, 'start'], [p[0] - 10, p[1] + 4, 'end'], [p[0] - w / 2, p[1] - 12, 'start'], [p[0] - w / 2, p[1] + 20, 'start']];
        for (var q = 0; q < cands.length; q++) {
          var cx = cands[q][0], cy = cands[q][1], an = cands[q][2], x0 = an === 'end' ? cx - w : cx, b = [x0, cy - 11, x0 + w, cy + 3];
          if (fits(b) || (on && q === cands.length - 1)) { boxes.push(b); labels += '<text class="lbl" x="' + cx + '" y="' + cy + '" text-anchor="' + an + '"' + (on ? ' style="fill:var(--ink);font-weight:700"' : '') + '>' + esc(t) + '</text>'; break; }
        }
      });
      var dots = '';
      S.forEach(function (c, i) {
        var on = c === sel, inF = flight.indexOf(c) >= 0, vis = shown(c), p = pos[i];
        dots += '<circle class="dot' + (vis ? '' : ' dim') + '" data-i="' + i + '" cx="' + p[0] + '" cy="' + p[1] + '" r="' + (on ? 9 : inF ? 8 : 6) + '" fill="' + famColor(c.fam) + '" stroke="' + (on || inF ? 'var(--ink)' : 'var(--bg)') + '" stroke-width="' + (on || inF ? 2 : 1) + '"/>';
      });
      if (flight.length > 1) { var fl = flight.slice().sort(function (a, b) { return a.x - b.x || a.y - b.y; }); g += '<polyline class="flight" points="' + fl.map(function (c) { var p = pos[S.indexOf(c)]; return p[0] + ',' + p[1]; }).join(' ') + '"/>'; }
      g += dots + labels;
      plot.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '" role="img" aria-label="' + esc(L({ zh: '奶酪品鉴光谱', en: 'Cheese tasting spectrum' })) + '">' + g + '</svg>';
      $$('.dot', plot).forEach(function (d) { d.addEventListener('click', function () { var c = S[+d.getAttribute('data-i')]; sel = c; draw(); renderSide(); }); });
    }
    function renderFilters() { fbox.innerHTML = FILT.map(function (f) { return '<button class="chip" type="button" aria-pressed="' + (f.id === filt) + '" data-f="' + f.id + '">' + esc(L(f)) + '</button>'; }).join('') + (D.fams ? D.fams.map(function (f) { return '<span class="chip" style="cursor:default"><i style="background:' + famColor(f.id) + '"></i>' + esc(L(f)) + '</span>'; }).join('') : ''); $$('[data-f]', fbox).forEach(function (bt) { bt.addEventListener('click', function () { filt = bt.getAttribute('data-f'); renderFilters(); draw(); }); }); }
    function renderSide() {
      var c = sel, inF = flight.indexOf(c) >= 0;
      var fl = flight.slice().sort(function (a, b) { return a.x - b.x || a.y - b.y; });
      side.innerHTML = '<span class="kick">' + esc(L(c.famName || '')) + '</span><h4>' + esc(L(c.name)) + '</h4><div class="meta">' + esc(L(c.origin || '')) + (c.milkName ? ' · ' + esc(L(c.milkName)) : '') + '</div>' +
        '<dl><dt>' + esc(L({ zh: '风味', en: 'Flavor' })) + '</dt><dd>' + esc(L(c.note)) + '</dd>' + (c.pair ? '<dt>' + esc(L({ zh: '配', en: 'Pair' })) + '</dt><dd>' + esc(L(c.pair)) + '</dd>' : '') + '<dt>' + esc(L({ zh: '位置', en: 'Placed' })) + '</dt><dd>' + esc(L({ zh: '强度 ' + c.x + ' · 硬度 ' + c.y, en: 'intensity ' + c.x + ' · firmness ' + c.y })) + '</dd></dl>' +
        '<div style="margin-top:14px"><button class="btn' + (inF ? ' ghost' : '') + '" type="button" data-act="flight">' + esc(L(inF ? { zh: '从这一组拿掉', en: 'Remove from flight' } : { zh: '加进一组品鉴', en: 'Add to tasting flight' })) + '</button></div>' +
        '<div class="flightbox"><span class="kick">' + esc(L({ zh: '这一组的品尝顺序（从淡到浓）', en: 'Tasting order (mild to bold)' })) + '</span>' + (fl.length ? '<ol>' + fl.map(function (x) { return '<li><b>' + esc(L(x.name)) + '</b> <span class="small">' + esc(L(x.famName || '')) + '</span></li>'; }).join('') + '</ol>' + (fl.length >= 3 ? '<p class="small" style="margin-top:8px">' + esc(L(D.flightTip || '')) + '</p>' : '') : '<p class="small" style="margin:8px 0 0">' + esc(L({ zh: '在图上点 3–5 种，排出一组从淡到浓的品鉴顺序。', en: 'Tap 3–5 cheeses on the chart to line up a mild-to-bold flight.' })) + '</p>') + '</div>';
      $('[data-act=flight]', side).addEventListener('click', function () { var k = flight.indexOf(c); if (k >= 0) flight.splice(k, 1); else { if (flight.length >= 6) flight.shift(); flight.push(c); } draw(); renderSide(); });
    }
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (plot.clientWidth !== W0) draw(); }, 120); });
    addEventListener('langchange', function () { renderFilters(); draw(); renderSide(); });
    addEventListener('themechange', draw);
    renderFilters(); draw(); renderSide();
  })();

  /* ---------- 02 风味轮 ---------- */
  (function () {
    var box = $('#wheel'); if (!box || !D.wheel) return;
    var A = D.wheel.axes, svgBox = $('.wheel', box), info = $('.wheelinfo', box), selA = null, selI = null;
    function arc(cx, cy, r0, r1, a0, a1) { var p = function (r, a) { return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; }, la = a1 - a0 > Math.PI ? 1 : 0, s0 = p(r1, a0), e0 = p(r1, a1), s1 = p(r0, a1), e1 = p(r0, a0); return 'M' + s0 + 'A' + r1 + ',' + r1 + ' 0 ' + la + ' 1 ' + e0 + 'L' + s1 + 'A' + r0 + ',' + r0 + ' 0 ' + la + ' 0 ' + e1 + 'Z'; }
    function draw() {
      var S = 520, c = S / 2, r0 = 70, r1 = 150, r2 = 250, tot = 0, g = '';
      A.forEach(function (a) { tot += a.items.length; });
      var ang = -Math.PI / 2;
      A.forEach(function (a, ai) {
        var span = 2 * Math.PI * a.items.length / tot, a0 = ang, a1 = ang + span, dimA = selA !== null && selA !== ai;
        g += '<path d="' + arc(c, c, r0, r1, a0, a1) + '" fill="' + a.color + '" class="' + (dimA ? 'dim' : '') + '" data-a="' + ai + '"/>';
        var mid = (a0 + a1) / 2, tx = c + (r0 + r1) / 2 * Math.cos(mid), ty = c + (r0 + r1) / 2 * Math.sin(mid);
        g += '<text class="ring1" x="' + tx + '" y="' + ty + '" text-anchor="middle" dominant-baseline="middle">' + esc(L(a)) + '</text>';
        a.items.forEach(function (it, ii) {
          var b0 = a0 + span * ii / a.items.length, b1 = a0 + span * (ii + 1) / a.items.length, on = selA === ai && selI === ii;
          g += '<path d="' + arc(c, c, r1 + 2, r2, b0, b1) + '" fill="' + a.color + '" fill-opacity="' + (on ? 1 : 0.62) + '" class="' + (dimA ? 'dim' : '') + '" data-a="' + ai + '" data-i="' + ii + '"/>';
          var m2 = (b0 + b1) / 2, deg = m2 * 180 / Math.PI, flip = Math.cos(m2) < 0, rr = (r1 + r2) / 2 + 4;
          g += '<text x="' + (c + rr * Math.cos(m2)) + '" y="' + (c + rr * Math.sin(m2)) + '" text-anchor="middle" dominant-baseline="middle" transform="rotate(' + (flip ? deg + 180 : deg) + ' ' + (c + rr * Math.cos(m2)) + ' ' + (c + rr * Math.sin(m2)) + ')">' + esc(L(it)) + '</text>';
        });
        ang = a1;
      });
      g += '<circle cx="' + c + '" cy="' + c + '" r="' + (r0 - 6) + '" fill="var(--paper)" stroke="var(--line)"/><text x="' + c + '" y="' + c + '" text-anchor="middle" dominant-baseline="middle" style="fill:var(--ink);font-size:14px;font-weight:700">' + esc(L({ zh: '闻 · 尝', en: 'Smell · Taste' })) + '</text>';
      svgBox.innerHTML = '<svg viewBox="0 0 ' + S + ' ' + S + '" role="img" aria-label="' + esc(L({ zh: '奶酪风味轮', en: 'Cheese flavor wheel' })) + '">' + g + '</svg>';
      $$('path', svgBox).forEach(function (p) { p.addEventListener('click', function () { selA = +p.getAttribute('data-a'); selI = p.hasAttribute('data-i') ? +p.getAttribute('data-i') : null; draw(); renderInfo(); }); });
    }
    function renderInfo() {
      if (selA === null) { info.innerHTML = '<h4>' + esc(L(D.wheel.title)) + '</h4><p>' + L(D.wheel.intro) + '</p>' + (D.wheel.src ? '<p class="src">' + L(D.wheel.src) + '</p>' : ''); return; }
      var a = A[selA];
      if (selI === null) { info.innerHTML = '<span class="kick">' + esc(L({ zh: '气味族', en: 'Aroma family' })) + '</span><h4>' + esc(L(a)) + '</h4><p>' + esc(L(a.desc || '')) + '</p><p class="small">' + a.items.map(function (it) { return esc(L(it)); }).join(' · ') + '</p>'; return; }
      var it = a.items[selI];
      info.innerHTML = '<span class="kick">' + esc(L(a)) + '</span><h4>' + esc(L(it)) + '</h4>' + (it.cheese ? '<p><b>' + esc(L({ zh: '典型：', en: 'Typical in: ' })) + '</b>' + esc(L(it.cheese)) + '</p>' : '') + (it.compound ? '<p><b>' + esc(L({ zh: '来自：', en: 'From: ' })) + '</b>' + esc(L(it.compound)) + '</p>' : '');
    }
    addEventListener('langchange', function () { draw(); renderInfo(); });
    draw(); renderInfo();
  })();

  /* ---------- 02 搭配：按类别筛 ---------- */
  (function () {
    var box = $('#pairs'); if (!box || !D.pairs) return;
    var P = D.pairs.items, K = D.pairs.kinds, kind = K[0].id, chips = $('.lens', box), grid = $('.pairs', box);
    function render() {
      chips.innerHTML = K.map(function (k) { return '<button class="chip" type="button" aria-pressed="' + (k.id === kind) + '" data-k="' + k.id + '">' + esc(L(k)) + '</button>'; }).join('');
      grid.innerHTML = P.filter(function (p) { return p.kind === kind; }).map(function (p) { return '<div class="pair"><span class="k">' + esc(L(p.cheese)) + '</span><h5>+ ' + esc(L(p.with)) + '</h5><p>' + esc(L(p.why)) + '</p></div>'; }).join('');
      $$('[data-k]', chips).forEach(function (b) { b.addEventListener('click', function () { kind = b.getAttribute('data-k'); render(); }); });
    }
    addEventListener('langchange', render); render();
  })();

  /* ---------- 透镜列表（通用） ---------- */
  (function () {
    $$('[data-list]').forEach(function (host) {
      var key = host.getAttribute('data-list'), items = D[key]; if (!items) return;
      var lensBox = $('.lens', host), list = $('.list', host), lenses = (D.lenses && D.lenses[key]) || null, lens = lenses ? lenses[0].id : null, open = {};
      function row(it) { return '<div class="item' + (open[it.id] ? ' open' : '') + (it.img ? '' : ' noimg') + '" data-id="' + it.id + '"><button aria-expanded="' + (open[it.id] ? 'true' : 'false') + '">' + (it.img ? '<span class="thumb"><img src="' + it.img + '" alt="" loading="lazy"></span>' : '') + '<span class="tt"><b>' + esc(L(it.title)) + (it.sub ? '<small>' + esc(L(it.sub)) + '</small>' : '') + '</b><span>' + esc(L(it.one)) + '</span></span><span class="pl">+</span></button><div class="body"><ul>' + (it.facts || []).map(function (f) { return '<li>' + (f.k ? '<em>' + esc(L(f.k)) + '</em>' : '') + L(f) + (f.src ? ' <a class="src" href="' + esc(f.src) + '" target="_blank" rel="noopener">↗</a>' : '') + '</li>'; }).join('') + '</ul>' + (it.img ? '<figure><img src="' + it.img + '" alt="" loading="lazy"><figcaption>' + L(it.cap || '') + '</figcaption></figure>' : '<div></div>') + '</div></div>'; }
      function render() {
        if (lensBox && lenses) lensBox.innerHTML = lenses.map(function (l) { return '<button class="chip" type="button" aria-pressed="' + (l.id === lens ? 'true' : 'false') + '" data-l="' + l.id + '">' + esc(L(l)) + '</button>'; }).join('');
        var html = '';
        if (lenses) { var lz = lenses.filter(function (l) { return l.id === lens; })[0]; lz.groups.forEach(function (gr) { var its = items.filter(function (it) { return (it.g || {})[lens] === gr.id; }); if (!its.length) return; html += '<div class="grp">' + esc(L(gr)) + '</div>' + its.map(row).join(''); }); }
        else html = items.map(row).join('');
        list.innerHTML = html;
        $$('.item>button', list).forEach(function (b) { b.addEventListener('click', function () { var id = b.parentNode.getAttribute('data-id'); open[id] = !open[id]; b.parentNode.classList.toggle('open', open[id]); b.setAttribute('aria-expanded', open[id] ? 'true' : 'false'); }); });
        if (lensBox) $$('.chip', lensBox).forEach(function (b) { b.addEventListener('click', function () { lens = b.getAttribute('data-l'); render(); }); });
      }
      render(); addEventListener('langchange', render);
    });
  })();

  /* ---------- 04 柜台：分区 → 价格区间图 → 卡片 ---------- */
  (function () {
    var box = $('#case'); if (!box || !D.counter) return;
    var C = D.counter, zb = $('.zones', box), pc = $('.pricechart', box), card = $('.cheesecard', box), zi = C.zones[0].id, sel = null, W0 = 0;
    function zone() { return C.zones.filter(function (z) { return z.id === zi; })[0]; }
    function zones() {
      zb.innerHTML = C.zones.map(function (z) { return '<button type="button" class="zone' + (z.id === zi ? ' on' : '') + '" data-z="' + z.id + '"><b>' + esc(L(z)) + '</b><span>' + z.cheeses.length + '</span></button>'; }).join('');
      $$('.zone', zb).forEach(function (b) { b.addEventListener('click', function () { zi = b.getAttribute('data-z'); sel = zone().cheeses[0]; zones(); chart(); detail(); }); });
    }
    function chart() {
      var z = zone(), W = pc.clientWidth, narrow = W < 520, lw = narrow ? 118 : 200, m = { l: lw, r: narrow ? 8 : 70, t: 28, b: 8 }, rh = 32, H = m.t + m.b + z.cheeses.length * rh, max = 60; W0 = W;
      var X = function (v) { return m.l + (W - m.l - m.r) * v / max; }, g = '';
      for (var v = 0; v <= max; v += 10) g += '<line x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (m.t - 6) + '" y2="' + (H - m.b) + '" stroke="var(--line)"/><text x="' + X(v) + '" y="' + (m.t - 12) + '" text-anchor="middle" class="ax">$' + v + '</text>';
      z.cheeses.forEach(function (id, i) {
        var c = C.cheeses[id], y = m.t + i * rh, on = id === sel, nm = c.name.length > (narrow ? 15 : 26) ? c.name.slice(0, narrow ? 14 : 25) + '…' : c.name;
        g += '<g class="row' + (on ? ' on' : '') + '" data-id="' + id + '"><rect x="0" y="' + y + '" width="' + W + '" height="' + rh + '" fill="transparent"/>';
        g += '<text x="' + (m.l - 10) + '" y="' + (y + rh / 2 + 4) + '" text-anchor="end" class="nm">' + esc(nm) + '</text>';
        if (c.lo != null) g += '<rect x="' + X(c.lo) + '" y="' + (y + 9) + '" width="' + Math.max(8, X(c.hi) - X(c.lo)) + '" height="' + (rh - 18) + '" rx="' + ((rh - 18) / 2) + '" fill="' + famColor(c.fam) + '"' + (on ? ' stroke="var(--ink)" stroke-width="1.5"' : '') + '/>';
        if (!narrow && c.lo != null) g += '<text x="' + (X(c.hi) + 8) + '" y="' + (y + rh / 2 + 4) + '" class="pv">$' + c.lo + '–' + c.hi + '</text>';
        g += '</g>';
      });
      pc.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '" role="img" aria-label="' + esc(L({ zh: '每磅价格区间', en: 'Price range per pound' })) + '">' + g + '</svg>';
      $$('.row', pc).forEach(function (r) { r.addEventListener('click', function () { sel = r.getAttribute('data-id'); chart(); detail(); }); });
    }
    function detail() {
      var c = C.cheeses[sel], z = zone(); if (!c) return;
      card.innerHTML = '<span class="kick">' + esc(L(z)) + '</span><h4>' + esc(c.name) + '</h4>' + (lang() === 'zh' ? '<div class="zhn">' + esc(c.zhname) + '</div>' : '') +
        '<div class="meta">' + esc(L(c.origin)) + '</div>' + (c.labels.length ? '<div class="lbs">' + c.labels.map(function (l) { return '<span class="lb">' + esc(l) + '</span>'; }).join('') + '</div>' : '') +
        (c.lo != null ? '<div class="pr">$' + c.lo + '–' + c.hi + ' <small>/ lb</small></div>' : '') + '<p>' + esc(L(c.taste)) + '</p>' + (c.pair ? '<p><b>' + esc(L({ zh: '配', en: 'With' })) + '</b> ' + esc(L(c.pair)) + '</p>' : '') +
        '<p class="zw">' + L(z.what) + '</p>';
    }
    sel = zone().cheeses[0]; zones(); chart(); detail();
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (pc.clientWidth !== W0) chart(); }, 120); });
    addEventListener('langchange', function () { zones(); chart(); detail(); }); addEventListener('themechange', chart);
  })();

  /* ---------- 04 读价签 ---------- */
  (function () {
    var box = $('#tagbox'); if (!box || !D.tags) return;
    var TG = D.tags, pick = $('.tagpick', box), tagEl = $('.pricetag', box), gl = $('.gloss', box), ti = 0, gk = null;
    function firstG(t) { for (var i = 0; i < t.tokens.length; i++) if (t.tokens[i].g) return t.tokens[i].g; return 'lb'; }
    function render() {
      var t = TG.list[ti]; if (!gk) gk = firstG(t);
      pick.innerHTML = TG.list.map(function (x, i) { return '<button class="chip" type="button" aria-pressed="' + (i === ti) + '" data-i="' + i + '">' + esc(L(x.name)) + '</button>'; }).join('');
      $$('[data-i]', pick).forEach(function (b) { b.addEventListener('click', function () { ti = +b.getAttribute('data-i'); gk = firstG(TG.list[ti]); render(); }); });
      var tok = function (k) { var x = t.tokens[k]; return x.g ? '<button type="button" class="tk' + (x.g === gk ? ' on' : '') + '" data-g="' + x.g + '">' + esc(x.w) + '</button>' : '<span class="tw">' + esc(x.w) + '</span>'; };
      var rest = []; for (var k = 1; k < t.tokens.length; k++) rest.push(tok(k));
      tagEl.innerHTML = '<div class="hole"></div><div class="t1">' + tok(0) + '</div><div class="t2">' + rest.join('<i>·</i>') + '</div><div class="t3"><button type="button" class="tk' + (gk === 'lb' ? ' on' : '') + '" data-g="lb">' + esc(t.price) + '</button></div><div class="tnote">' + esc(L({ zh: '示例价签', en: 'Sample tag' })) + '</div>';
      $$('[data-g]', tagEl).forEach(function (b) { b.addEventListener('click', function () { gk = b.getAttribute('data-g'); render(); }); });
      var G = TG.gloss[gk]; gl.innerHTML = G ? '<span class="kick">' + esc(L({ zh: '这个词', en: 'This word' })) + '</span><h4>' + esc(L(G.t)) + '</h4><p>' + L(G) + '</p>' : '';
    }
    addEventListener('langchange', render); render();
  })();

  /* ---------- 04 柜台英文：翻面卡 ---------- */
  (function () {
    var box = $('#flips'); if (!box || !D.phrases) return;
    function render() {
      box.innerHTML = D.phrases.map(function (p, i) { return '<button type="button" class="flip" aria-pressed="false"><span class="f"><q>' + esc(p.en) + '</q><em>' + esc(L({ zh: '点一下看意思', en: 'Tap to flip' })) + '</em></span><span class="b"><b>' + esc(p.zh) + '</b><em>' + esc(p.en) + '</em></span></button>'; }).join('');
      $$('.flip', box).forEach(function (b) { b.addEventListener('click', function () { var on = b.classList.toggle('on'); b.setAttribute('aria-pressed', on ? 'true' : 'false'); }); });
    }
    addEventListener('langchange', render); render();
  })();

  /* ---------- 04 配一盘 ---------- */
  (function () {
    var box = $('#builder'); if (!box || !D.boards) return;
    var BD = D.boards.list, CS = D.counter.cheeses, bi_ = 1, ppl = 4;
    var bud = $('.bbudget', box), bar = $('.bbar', box), chk = $('.bchecks', box), list = $('.blist', box), pn = $('.pn', box);
    function r2(x) { return Math.max(1, Math.round(x * 2) / 2); }
    function render() {
      var b = BD[bi_], k = ppl / b.people;
      bud.innerHTML = BD.map(function (x, i) { return '<button class="chip" type="button" aria-pressed="' + (i === bi_) + '" data-i="' + i + '">$' + x.budget + '</button>'; }).join('');
      $$('[data-i]', bud).forEach(function (x) { x.addEventListener('click', function () { bi_ = +x.getAttribute('data-i'); render(); }); });
      pn.textContent = ppl;
      var items = b.items.map(function (it) { return { c: CS[it.id], oz: r2(it.oz * k), why: it.why }; });
      var tot = items.reduce(function (s, x) { return s + x.oz; }, 0), lo = 0, hi = 0, milks = {}, fams = {}, ca = false;
      items.forEach(function (x) { lo += x.oz / 16 * x.c.lo; hi += x.oz / 16 * x.c.hi; x.c.milks.forEach(function (m) { milks[m] = 1; }); fams[x.c.fam] = 1; if (x.c.ca) ca = true; });
      bar.innerHTML = '<div class="bh"><b>' + esc(L(b.title)) + '</b><span>' + esc(L({ zh: '奶酪约 $' + Math.round(lo) + '–' + Math.round(hi) + ' · 共 ' + tot + ' oz（约 ' + Math.round(tot * 28.35) + ' 克）· 每人 ' + (Math.round(tot / ppl * 10) / 10) + ' oz', en: 'Cheese about $' + Math.round(lo) + '–' + Math.round(hi) + ' · ' + tot + ' oz in all (~' + Math.round(tot * 28.35) + ' g) · ' + (Math.round(tot / ppl * 10) / 10) + ' oz each' })) + '</span></div>' +
        '<div class="segs">' + items.map(function (x) { return '<div class="seg" style="flex:' + x.oz + ';background:' + famColor(x.c.fam) + '"><span>' + esc(x.c.name) + ' · ' + x.oz + ' oz</span></div>'; }).join('') + '</div>';
      var nm = Object.keys(milks).length, nf = Object.keys(fams).length;
      chk.innerHTML = [[nm >= 2, L({ zh: '奶源 ' + nm + ' 种', en: nm + ' milk' + (nm > 1 ? 's' : '') })], [nf >= 3, L({ zh: '类型 ' + nf + ' 种', en: nf + ' styles' })], [ca, L({ zh: '有加州奶酪', en: 'A Californian' })]]
        .map(function (c) { return '<span class="ck' + (c[0] ? ' ok' : '') + '">' + (c[0] ? '✓ ' : '· ') + esc(c[1]) + '</span>'; }).join('');
      list.innerHTML = items.map(function (x) { return '<div class="bi"><i style="background:' + famColor(x.c.fam) + '"></i><b>' + esc(x.c.name) + '</b><span class="oz">' + x.oz + ' oz</span><p>' + esc(L(x.why)) + '</p></div>'; }).join('') +
        (L(b.extras) ? '<p class="small bx"><b>' + esc(L({ zh: '再配上', en: 'Add' })) + '</b> ' + esc(L(b.extras)) + '</p>' : '');
    }
    $$('[data-p]', box).forEach(function (x) { x.addEventListener('click', function () { ppl = clamp(ppl + 2 * (+x.getAttribute('data-p')), 2, 12); render(); }); });
    addEventListener('langchange', render); render();
  })();

  /* ---------- 04 从柜台到餐桌 ---------- */
  (function () {
    var box = $('#path'); if (!box || !D.path) return;
    var P = D.path.list, rail = $('.prail', box), body = $('.pbody', box), pi = 0;
    function shelf() {
      var S = D.path.shelf, W = 520, m = { l: 0, r: 40, t: 22, b: 6 }, rh = 46, H = m.t + m.b + S.length * rh, max = 30, X = function (v) { return m.l + (W - m.l - m.r) * v / max; }, g = '';
      [0, 7, 14, 21, 28].forEach(function (v) { g += '<line x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (m.t - 4) + '" y2="' + (H - m.b) + '" stroke="var(--line)"/><text x="' + X(v) + '" y="' + (m.t - 8) + '" text-anchor="middle" class="ax">' + v + '</text>'; });
      S.forEach(function (s, i) { var y = m.t + i * rh; g += '<text x="0" y="' + (y + 14) + '" class="nm2">' + esc(L(s.t)) + '</text><rect x="' + X(0) + '" y="' + (y + 20) + '" width="' + (X(s.b) - X(0)) + '" height="14" rx="7" fill="var(--amber)" opacity=".35"/><rect x="' + X(0) + '" y="' + (y + 20) + '" width="' + (X(s.a) - X(0)) + '" height="14" rx="7" fill="var(--amber)"/><text x="' + (X(s.b) + 6) + '" y="' + (y + 31) + '" class="pv">' + (s.a === s.b ? s.a : s.a + '–' + s.b) + L({ zh: ' 天', en: ' d' }) + '</text>'; });
      return '<div class="shelf"><span class="kick">' + esc(L(D.path.shelfHead)) + '</span><svg viewBox="0 0 ' + W + ' ' + H + '" role="img">' + g + '</svg></div>';
    }
    function render() {
      rail.innerHTML = P.map(function (p, i) { return '<button type="button" class="pn' + (i === pi ? ' on' : '') + (i < pi ? ' done' : '') + '" data-i="' + i + '"><i>' + (i + 1) + '</i><b>' + esc(L(p.t)) + '</b></button>'; }).join('');
      $$('[data-i]', rail).forEach(function (b) { b.addEventListener('click', function () { pi = +b.getAttribute('data-i'); render(); }); });
      var p = P[pi];
      body.innerHTML = (p.id === 'later' ? shelf() : '') + '<div class="tips">' + p.tips.map(function (t) { return '<div class="tip"><b>' + esc(L(t.t)) + '</b><p>' + L(t) + '</p></div>'; }).join('') + '</div>';
    }
    addEventListener('langchange', render); render();
  })();

  /* ---------- 04 从 Daisy 家出发：距离罗盘 ---------- */
  (function () {
    var box = $('#where'); if (!box || !D.where) return;
    var WL = D.where.list, K = {}, comp = $('.compass', box), card = $('.wcard', box), leg = $('#wlegend'), sel = WL[0].id, W0 = 0;
    var KC = { wholefoods: '#7FA36B', shop: '#E3A72F', market: '#C0533F', class: '#8DA9C4', trip: '#B48EAD' };
    D.where.kinds.forEach(function (k) { K[k.id] = k; });
    function R(mins, Rmax) { return mins <= 30 ? Rmax * 0.86 * mins / 30 : Rmax * 0.97; }
    function draw() {
      var S = Math.min(comp.clientWidth, 560), c = S / 2, Rm = S / 2 - 22, g = ''; W0 = comp.clientWidth;
      [10, 20, 30].forEach(function (m) { g += '<circle cx="' + c + '" cy="' + c + '" r="' + R(m, Rm) + '" class="ring"/><text x="' + c + '" y="' + (c - R(m, Rm) + 13) + '" text-anchor="middle" class="rl">' + esc(L({ zh: m + ' 分钟', en: m + ' min' })) + '</text>'; });
      g += '<circle cx="' + c + '" cy="' + c + '" r="' + R(60, Rm) + '" class="ring far"/><text x="' + c + '" y="' + (c + R(60, Rm) - 5) + '" text-anchor="middle" class="rl">' + esc(L({ zh: '约 1 小时（压缩）', en: '~1 h (compressed)' })) + '</text>';
      [['N', '北', 0], ['E', '东', 90], ['S', '南', 180], ['W', '西', 270]].forEach(function (d) { var a = d[2] * Math.PI / 180, r = Rm + 12; g += '<text x="' + (c + r * Math.sin(a)) + '" y="' + (c - r * Math.cos(a) + 4) + '" text-anchor="middle" class="cd">' + (lang() === 'en' ? d[0] : d[1]) + '</text>'; });
      var placed = [];
      WL.forEach(function (p) {
        var a = p.brg * Math.PI / 180, r = R(p.mins, Rm), x = c + r * Math.sin(a), y = c - r * Math.cos(a);
        for (var t = 0; t < 8; t++) { var hit = placed.some(function (q) { return Math.hypot(q[0] - x, q[1] - y) < 22; }); if (!hit) break; a += 0.16; x = c + r * Math.sin(a); y = c - r * Math.cos(a); }
        placed.push([x, y]); p._x = x; p._y = y;
      });
      g += '<circle cx="' + c + '" cy="' + c + '" r="7" fill="var(--ink)"/><text x="' + c + '" y="' + (c + 24) + '" text-anchor="middle" class="home">' + esc(L({ zh: 'Daisy 家', en: 'Daisy’s' })) + '</text>';
      WL.forEach(function (p) { var on = p.id === sel; g += '<g class="pt' + (on ? ' on' : '') + '" data-id="' + p.id + '"><circle cx="' + p._x + '" cy="' + p._y + '" r="' + (on ? 13 : 10) + '" fill="' + KC[p.kind] + '"' + (on ? ' stroke="var(--ink)" stroke-width="2"' : '') + '/><text x="' + p._x + '" y="' + (p._y + 4) + '" text-anchor="middle" class="num">' + p.n + '</text></g>'; });
      var sp = WL.filter(function (p) { return p.id === sel; })[0];
      if (sp && S >= 480) { var near = Math.hypot(sp._x - c, sp._y - c) < 60, right = sp._x < c + 40;
        g += near ? '<text x="' + sp._x + '" y="' + (sp._y - 20) + '" text-anchor="middle" class="sl">' + esc(L(sp.name)) + '</text>'
                  : '<text x="' + (sp._x + (right ? 18 : -18)) + '" y="' + (sp._y + 4) + '" text-anchor="' + (right ? 'start' : 'end') + '" class="sl">' + esc(L(sp.name)) + '</text>'; }
      comp.innerHTML = '<svg viewBox="0 0 ' + S + ' ' + S + '" width="' + S + '" height="' + S + '" role="img" aria-label="' + esc(L({ zh: '从 Daisy 家出发的距离图', en: 'Distance chart from Daisy’s place' })) + '">' + g + '</svg>';
      $$('.pt', comp).forEach(function (n) { n.addEventListener('click', function () { sel = n.getAttribute('data-id'); all(); }); });
    }
    function cardR() {
      var p = WL.filter(function (x) { return x.id === sel; })[0];
      card.innerHTML = '<span class="kind" style="--k:' + KC[p.kind] + '">' + p.n + ' · ' + esc(L(K[p.kind])) + '</span><h4>' + esc(L(p.name)) + '</h4><div class="meta">' + esc(L(p.dist)) + '</div>' +
        '<dl><dt>' + esc(L({ zh: '地址', en: 'Address' })) + '</dt><dd>' + esc(L(p.addr)) + '</dd><dt>' + esc(L({ zh: '是什么', en: 'What' })) + '</dt><dd>' + L(p.what) + '</dd><dt>' + esc(L({ zh: '适合', en: 'Best for' })) + '</dt><dd>' + L(p.best) + '</dd></dl>' +
        (p.more.length ? '<ul>' + p.more.map(function (m) { return '<li>' + esc(L(m)) + '</li>'; }).join('') + '</ul>' : '');
    }
    function legend() {
      leg.innerHTML = WL.map(function (p) { return '<button type="button" class="wl' + (p.id === sel ? ' on' : '') + '" data-id="' + p.id + '"><i style="background:' + KC[p.kind] + '">' + p.n + '</i>' + esc(L(p.name)) + '</button>'; }).join('');
      $$('.wl', leg).forEach(function (b) { b.addEventListener('click', function () { sel = b.getAttribute('data-id'); all(); }); });
    }
    function all() { draw(); cardR(); legend(); }
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (comp.clientWidth !== W0) draw(); }, 120); });
    addEventListener('langchange', all); addEventListener('themechange', draw); all();
  })();
})();
