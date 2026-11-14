(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('D').textContent);
  var BY = {}; D.cases.forEach(function (c) { BY[c.id] = c; });
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var NS = 'http://www.w3.org/2000/svg';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]; }); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function yr(y) { return y == null ? '' : (y < 0 ? '前 ' + (-y) + ' 年' : String(y)); }
  function navH() { return parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 48; }
  function ease(t) { return 1 - Math.pow(1 - t, 3); }
  function km(k) { return '<i class="km ' + k + '" aria-hidden="true"></i>'; }

  /* ---------- 通用：主题、导航、入场、论点 ---------- */
  (function () {
    var root = document.documentElement, btn = $('.theme');
    function set(t) { root.setAttribute('data-theme', t); if (btn) btn.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false'); }
    try { var s = localStorage.getItem('sb-theme'); if (s === 'dark' || s === 'light') set(s); } catch (e) {}
    if (btn) btn.addEventListener('click', function () {
      var t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; set(t);
      try { localStorage.setItem('sb-theme', t); } catch (e) {}
    });
  })();
  (function () {
    var links = $$('.clinks a'), bar = $('.cprog i');
    var secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-ch')); });
    function on() {
      var h = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.width = (h > 0 ? clamp(scrollY / h, 0, 1) * 100 : 0) + '%';
      var cur = -1, y = navH() + innerHeight * 0.3;
      secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top <= y) cur = i; });
      links.forEach(function (a, i) {
        var was = a.classList.contains('on'); a.classList.toggle('on', i === cur);
        if (i === cur && !was) { var p = a.parentNode; p.scrollLeft = a.offsetLeft - p.offsetLeft - 16; }
      });
    }
    addEventListener('scroll', on, { passive: true }); addEventListener('resize', on); on();
  })();
  (function () {
    var els = $$('.rise');
    if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (e) { io.observe(e); });
  })();
  (function () {
    var tw = $('.tw'); if (!tw) return; var ws = $$('.w', tw);
    function on() {
      var r = tw.getBoundingClientRect(), p = clamp((innerHeight * 0.85 - r.top) / (innerHeight * 0.5), 0, 1), n = Math.round(p * ws.length);
      ws.forEach(function (w, i) { w.classList.toggle('on', RM.matches || i < n); });
    }
    addEventListener('scroll', on, { passive: true }); on();
  })();

  /* ---------- 地图视图：一张等经纬底图 + 像素坐标的覆盖层 ---------- */
  function MapView(el) {
    var self = this; this.el = el; this.vb = { x: 0, y: 0, w: 360, h: 180 }; this.W = 1; this.H = 1; this.tw = null; this.visible = false; this.onframe = null;
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('preserveAspectRatio', 'none'); svg.setAttribute('aria-hidden', 'true');
    svg.innerHTML = '<image class="mv-img" href="' + D.base + '" preserveAspectRatio="none"/><image class="mv-img" href="' + D.base + '" preserveAspectRatio="none"/><rect class="mv-veil"/><g class="st"></g><g class="an"></g>';
    el.appendChild(svg); this.svg = svg; this.img = svg.childNodes[0]; this.img2 = svg.childNodes[1]; this.veil = svg.childNodes[2]; this.gst = svg.childNodes[3]; this.gan = svg.childNodes[4];
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { self.visible = es[0].isIntersecting; if (self.visible) self.kick(); }).observe(el); else this.visible = true;
    this.resize();
  }
  MapView.prototype.resize = function () {
    var r = this.el.getBoundingClientRect(); this.W = Math.max(1, r.width); this.H = Math.max(1, r.height);
    this.svg.setAttribute('viewBox', '0 0 ' + this.W + ' ' + this.H);
    this.veil.setAttribute('width', this.W); this.veil.setAttribute('height', this.H);
    this.vb = this.norm(this.vb); this.apply();
  };
  MapView.prototype.maxW = function () { return Math.min(360, 180 * this.W / this.H); };
  /* 经度方向可以绕圈（底图画两份）；纬度方向夹住 */
  MapView.prototype.norm = function (v) {
    var w = clamp(v.w, 8, this.maxW()), h = w * this.H / this.W, cx = v.x + v.w / 2, cy = v.y + v.h / 2;
    return { x: cx - w / 2, y: clamp(cy - h / 2, 0, Math.max(0, 180 - h)), w: w, h: h };
  };
  MapView.prototype.apply = function () {
    var s = this.W / this.vb.w, xm = ((this.vb.x % 360) + 360) % 360; this.sc = s;
    [this.img, this.img2].forEach(function (im, k) { im.setAttribute('x', (k * 360 - xm) * s - (k ? 0.5 : 0)); im.setAttribute('y', -this.vb.y * s); im.setAttribute('width', 360 * s + 1); im.setAttribute('height', 180 * s); }, this);
  };
  MapView.prototype.px = function (lon, lat) {
    var dx = (((lon + 180 - this.vb.x) % 360) + 360) % 360; if (dx > (360 + this.vb.w) / 2) dx -= 360;
    return [dx * this.sc, (90 - lat - this.vb.y) * this.sc];
  };
  /* 把一组点框进去（pts[0] 是起点，必须落在空处）；free = 四边要让开的像素 */
  MapView.prototype.fit = function (pts, free, minW) {
    free = free || { l: 0, t: 0, r: 0, b: 0 };
    var x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    pts.forEach(function (p) { var x = p.lo + 180, y = 90 - p.la; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); });
    var fw = Math.max(80, this.W - free.l - free.r), fh = Math.max(80, this.H - free.t - free.b);
    var bw = Math.max(x1 - x0, 1) * 1.25 + 6, bh = Math.max(y1 - y0, 1) * 1.3 + 6;
    var s = Math.max(bw / fw, bh / fh), w = Math.max(s * this.W, minW || 50); w = Math.min(w, this.maxW());
    var k = w / this.W, h = w * this.H / this.W, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    var x = cx - (free.l + fw / 2) * k, y = clamp(cy - (free.t + fh / 2) * k, 0, Math.max(0, 180 - h));
    var ox = (pts[0].lo + 180 - x) / k;   /* 起点的屏幕 x */
    if (ox < free.l + 24) x = pts[0].lo + 180 - (free.l + 24) * k; else if (ox > this.W - free.r - 24) x = pts[0].lo + 180 - (this.W - free.r - 24) * k;
    return { x: x, y: y, w: w, h: h };
  };
  MapView.prototype.fly = function (to, instant) {
    to = this.norm(to);
    if (instant || RM.matches) { this.vb = to; this.tw = null; this.apply(); this.kick(); return; }
    this.tw = { a: this.vb, b: to, t0: performance.now(), d: 1100 }; this.kick();
  };
  MapView.prototype.kick = function () {
    var self = this; if (this.raf) return;
    this.raf = requestAnimationFrame(function tick(now) {
      self.raf = 0; var more = false;
      if (self.tw) {
        var t = clamp((now - self.tw.t0) / self.tw.d, 0, 1), e = ease(t), a = self.tw.a, b = self.tw.b;
        self.vb = { x: a.x + (b.x - a.x) * e, y: a.y + (b.y - a.y) * e, w: a.w + (b.w - a.w) * e, h: a.h + (b.h - a.h) * e };
        self.apply(); if (t < 1) more = true; else self.tw = null;
      }
      if (self.onframe && self.onframe(now)) more = true;
      if (more && self.visible) self.raf = requestAnimationFrame(tick);
    });
  };

  /* 大圆弧取样（经纬度） */
  function gc(a, b, n) {
    var R = Math.PI / 180, la1 = a.la * R, lo1 = a.lo * R, la2 = b.la * R, lo2 = b.lo * R;
    var d = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin((la2 - la1) / 2), 2) + Math.cos(la1) * Math.cos(la2) * Math.pow(Math.sin((lo2 - lo1) / 2), 2)));
    var out = [];
    for (var i = 0; i <= n; i++) {
      var f = i / n;
      if (d < 1e-6) { out.push([a.lo, a.la]); continue; }
      var A = Math.sin((1 - f) * d) / Math.sin(d), B = Math.sin(f * d) / Math.sin(d);
      var x = A * Math.cos(la1) * Math.cos(lo1) + B * Math.cos(la2) * Math.cos(lo2), y = A * Math.cos(la1) * Math.sin(lo1) + B * Math.cos(la2) * Math.sin(lo2), z = A * Math.sin(la1) + B * Math.sin(la2);
      out.push([Math.atan2(y, x) / R, Math.atan2(z, Math.sqrt(x * x + y * y)) / R]);
    }
    return out;
  }
  function arcPath(mv, a, b, f) {
    var pts = gc(a, b, 36), n = Math.max(1, Math.round(36 * f)), d = '', prev = null;
    for (var i = 0; i <= n; i++) {
      var p = mv.px(pts[i][0], pts[i][1]);
      d += (prev === null || Math.abs(pts[i][0] - prev) > 180 ? 'M' : 'L') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); prev = pts[i][0];
    }
    return d;
  }
  function orgMark(k, x, y, s) {
    return k === 'block'
      ? '<rect class="org block" x="' + (x - s).toFixed(1) + '" y="' + (y - s).toFixed(1) + '" width="' + 2 * s + '" height="' + 2 * s + '" transform="rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')"/>'
      : '<circle class="org boost" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (s * 1.2).toFixed(1) + '"/>';
  }
  function label(mv, x, y, cls, txt) {
    var anc = x > mv.W - 110 ? 'end' : (x < 110 ? 'start' : 'middle');
    return '<text class="' + cls + '" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + anc + '">' + esc(txt) + '</text>';
  }
  /* 画一条因果链：shown = 已点亮到第几站（可带小数） */
  function drawChain(mv, c, shown, now) {
    var o = mv.px(c.o.lo, c.o.la), h = '<g class="' + c.k + '">', i;
    if (RM.matches) h += '<circle class="ring" cx="' + o[0] + '" cy="' + o[1] + '" r="14" opacity=".7"/><circle class="ring" cx="' + o[0] + '" cy="' + o[1] + '" r="24" opacity=".4"/>';
    else for (i = 0; i < 3; i++) { var f = ((now / 2600) + i / 3) % 1; h += '<circle class="ring" cx="' + o[0].toFixed(1) + '" cy="' + o[1].toFixed(1) + '" r="' + (7 + f * 30).toFixed(1) + '" opacity="' + ((1 - f) * 0.85).toFixed(2) + '"/>'; }
    var prev = c.o, last = -1;
    for (i = 0; i < c.c.length; i++) {
      var g = clamp(shown - i, 0, 1); if (g <= 0) break;
      h += '<path class="arc" d="' + arcPath(mv, prev, c.c[i], g) + '"/>'; if (g >= 1) last = i; prev = c.c[i];
    }
    /* 标签：起点与最新一站必写，其余的撞上就不写 */
    var boxes = [], lab = '';
    function tw(t) { var w = 0; for (var q = 0; q < t.length; q++) w += t.charCodeAt(q) > 255 ? 12 : 6.6; return w; }
    function put(x, y, txt, force) {
      var w = tw(txt), anc = x > mv.W - 110 ? 'end' : (x < 110 ? 'start' : 'middle'), l = anc === 'middle' ? x - w / 2 : (anc === 'end' ? x - w : x), b = [l - 3, y - 13, l + w + 3, y + 4];
      if (!force && boxes.some(function (r) { return b[0] < r[2] && b[2] > r[0] && b[1] < r[3] && b[3] > r[1]; })) return;
      boxes.push(b); lab += label(mv, x, y, 'yr', txt);
    }
    put(o[0], o[1] + 22, yr(c.o.y) + ' · ' + c.o.p, true);
    for (i = 0; i <= last; i++) {
      var p = mv.px(c.c[i].lo, c.c[i].la);
      h += '<circle class="stn" cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="4.5"/>';
    }
    if (last >= 0) { var pl = mv.px(c.c[last].lo, c.c[last].la); put(pl[0], pl[1] - 10, yr(c.c[last].y) + ' · ' + c.c[last].p, false); if (lab.split('<text').length < 3) put(pl[0], pl[1] - 28, yr(c.c[last].y) + ' · ' + c.c[last].p, true); }
    for (i = 0; i < last; i++) { var pq = mv.px(c.c[i].lo, c.c[i].la); put(pq[0], pq[1] - 10, yr(c.c[i].y), false); }
    h += orgMark(c.k, o[0], o[1], 6) + '</g>' + lab;
    return h;
  }
  function chainList(c) {
    return '<ol class="sch">' + [c.o].concat(c.c).map(function (p, i) { return '<li' + (i === 0 ? ' class="on cur"' : '') + '><time>' + yr(p.y) + '</time><div><span class="pl">' + esc(p.p) + '</span><span class="tx">' + esc(p.x) + '</span></div></li>'; }).join('') + '</ol>';
  }
  /* k = 已点亮的站数（0 = 只有起点）；列表第 0 行是起点 */
  function markList(root, k) { $$('.sch li', root).forEach(function (li, i) { li.classList.toggle('on', i <= k); li.classList.toggle('cur', i === k); }); }

  var openCase, selectRipple, PACE = 1500;   /* 每站点亮的间隔（毫秒） */

  /* ---------- 00 序章舞台 ---------- */
  (function () {
    var sec = $('.stage'); if (!sec || !D.steps.length) return;
    var sin = $('.sin', sec), card = $('.scard', sec), hud = $('.shud', sec), ruler = $('.sruler', sec), ticks = $$('.rt', ruler);
    var mv = new MapView($('.smap', sec)), N = D.steps.length, cur = -1, t0 = 0, lit = -1;
    var STK = window.matchMedia('(max-width:760px), (max-height:520px)');
    function mobile() { return STK.matches; }
    function stepH() { return innerHeight * 0.9; }
    function free() {
      if (mobile()) return { l: 16, t: 36, r: 16, b: 16 };
      var m = mv.el.getBoundingClientRect(), c = card.getBoundingClientRect(), h = hud.getBoundingClientRect(), r = ruler.getBoundingClientRect();
      return { l: clamp(Math.max(c.right, h.right) - m.left + 40, 0, m.width * 0.55), t: 40, r: 48, b: clamp(m.bottom - r.top + 40, 0, m.height * 0.4) };
    }
    function over() {
      var lis = $$('.sch li', card), k, bad = false;
      for (k = 0; k < lis.length && !bad; k++) { lis.forEach(function (li, i) { li.classList.toggle('cur', i === k); }); if (card.scrollHeight > card.clientHeight + 1) bad = true; }
      lis.forEach(function (li, i) { li.classList.toggle('cur', i === 0); });
      return bad;
    }
    function tighten() {
      card.classList.remove('tight', 'tighter', 'tightest', 'min');
      if (mobile()) card.style.maxHeight = '';
      else { var s = sin.getBoundingClientRect(), h = hud.getBoundingClientRect(), r = ruler.getBoundingClientRect(); card.style.maxHeight = Math.max(120, r.top - h.bottom - 32) + 'px'; }
      ['tight', 'tighter', 'tightest', 'min'].some(function (k) { if (!over()) return true; card.classList.add(k); return false; });
    }
    function show(i, instant) {
      var s = D.steps[i], c = BY[s.id]; cur = i; lit = -1;
      $('.spair', hud).textContent = s.pname; $('.sline', hud).textContent = s.line;
      card.className = 'scard ' + c.k;
      card.innerHTML = '<p class="sk">' + km(c.k) + esc(s.pname) + ' · ' + esc(D.kinds[c.k]) + '</p><h3>' + esc(c.t) + '</h3><p class="ssm"><b>小</b>' + esc(c.s) + '</p><p class="sbg"><b>大</b>' + esc(c.b) + '</p>' + chainList(c) +
        (c.im ? '<figure class="sph"><img src="assets/' + esc(c.im.f) + '" alt="' + esc(c.im.a) + '" width="' + c.im.w + '" height="' + c.im.h + '" decoding="async"><figcaption><span class="cr">' + esc(c.im.cr) + '</span></figcaption></figure>' : '');
      tighten();
      ticks.forEach(function (t, k) { t.classList.toggle('on', k === i); t.classList.toggle('done', k < i); });
      ruler.setAttribute('aria-valuenow', i + 1); ruler.setAttribute('aria-valuetext', s.pname + '：' + c.t);
      mv.fly(mv.fit([c.o].concat(c.c), free(), mobile() ? 60 : 100), instant);
      t0 = performance.now() + (RM.matches ? -1e6 : 1400); mv.kick();
    }
    mv.onframe = function (now) {
      if (cur < 0) return false; var c = BY[D.steps[cur].id], n = c.c.length;
      var shown = RM.matches ? n : clamp((now - t0) / PACE, 0, n), k = Math.floor(shown + 1e-6);
      mv.gan.innerHTML = drawChain(mv, c, shown, now);
      if (k !== lit) { lit = k; markList(card, k); }
      return !RM.matches;
    };
    function fromScroll() {
      var off = navH() - sec.getBoundingClientRect().top, i = clamp(Math.floor(off / stepH()), 0, N - 1);
      if (i !== cur) show(i, cur < 0);
    }
    function go(i, smooth) {
      i = clamp(i, 0, N - 1);
      var top = sec.getBoundingClientRect().top + scrollY - navH() + i * stepH() + 8;
      window.scrollTo({ top: top, behavior: smooth && !RM.matches ? 'smooth' : 'auto' });
    }
    addEventListener('scroll', fromScroll, { passive: true });
    var rz; addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { mv.resize(); var c = cur; cur = -1; if (c >= 0) show(c, true); fromScroll(); }, 150); });
    /* 刻度尺：点、拖、甩（松手时按速度多走一格）、方向键 */
    var drag = null;
    function idxAt(x) { var best = 0, bd = 1e9; ticks.forEach(function (t, k) { var r = t.getBoundingClientRect(), d = Math.abs(x - (r.left + r.width / 2)); if (d < bd) { bd = d; best = k; } }); return best; }
    ruler.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, t: performance.now(), v: 0, moved: false }; try { ruler.setPointerCapture(e.pointerId); } catch (_) {} go(idxAt(e.clientX), false); });
    ruler.addEventListener('pointermove', function (e) {
      if (!drag) return; var now = performance.now(), dx = e.clientX - drag.x;
      if (Math.abs(dx) > 6) drag.moved = true;
      if (now > drag.t) drag.v = 0.7 * drag.v + 0.3 * (dx / (now - drag.t)); drag.x = e.clientX; drag.t = now;
      if (drag.moved) go(idxAt(e.clientX), false);
    });
    function up(e) { if (!drag) return; var i = idxAt(e.clientX); if (drag.moved && Math.abs(drag.v) > 0.9) i += drag.v > 0 ? 1 : -1; go(i, drag.moved); drag = null; }
    ruler.addEventListener('pointerup', up); ruler.addEventListener('pointercancel', function () { drag = null; });
    ruler.addEventListener('keydown', function (e) {
      var k = e.key; if (k === 'ArrowRight' || k === 'ArrowDown') { go(cur + 1, true); e.preventDefault(); }
      else if (k === 'ArrowLeft' || k === 'ArrowUp') { go(cur - 1, true); e.preventDefault(); }
      else if (k === 'Home') { go(0, true); e.preventDefault(); } else if (k === 'End') { go(N - 1, true); e.preventDefault(); }
    });
    ticks.forEach(function (t) { t.tabIndex = -1; });
    fromScroll();
    window.__stage = { go: go, cur: function () { return cur; }, n: N };
  })();

  /* ---------- 01 涟漪图 ---------- */
  (function () {
    var box = $('.rmap'); if (!box) return;
    var sec = $('#ripple'), panel = $('.rpanel', sec), scroller = $('.rscroll', sec), chips = $$('.chip', sec), fbtns = $$('.lens .sbtn', sec);
    var mv = new MapView(box), sel = null, filter = 'all', t0 = 0, manual = null, lit = -1, hint = panel.innerHTML;
    function world() { mv.fly({ x: 0, y: 0, w: 360, h: 180 }, true); }
    function vis(c) { return filter === 'all' || c.k === filter; }
    function statics() {
      var h = '';
      D.cases.slice().sort(function (a, b) { return (a.id === sel) - (b.id === sel); }).forEach(function (c) {
        var p = mv.px(c.o.lo, c.o.la), dim = !vis(c) || (sel && sel !== c.id);
        h += '<g class="pt ' + (dim ? 'dim ' : '') + (sel === c.id ? 'sel' : '') + '" data-id="' + c.id + '" tabindex="-1"><title>' + esc(yr(c.o.y) + ' ' + c.t) + '</title><circle class="hit" cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="13"/>' + orgMark(c.k, p[0], p[1], 4.5) + '</g>';
      });
      mv.gst.innerHTML = h;
    }
    function render() {
      chips.forEach(function (b) { var c = BY[b.getAttribute('data-id')]; b.classList.toggle('on', sel === c.id); b.classList.toggle('off', !vis(c)); b.setAttribute('aria-pressed', sel === c.id ? 'true' : 'false'); });
      statics();
      if (!sel) { panel.innerHTML = hint; mv.gan.innerHTML = ''; return; }
      var c = BY[sel];
      panel.innerHTML = '<p class="sk">' + km(c.k) + esc(D.kinds[c.k]) + ' · ' + yr(c.o.y) + (c.r.y != null && c.r.y !== c.o.y ? ' → ' + yr(c.r.y) : '') + '</p><h3>' + esc(c.t) + '</h3><p class="ssm"><b>小</b>' + esc(c.s) + '</p><p class="sbg"><b>大</b>' + esc(c.b) + '</p>' + chainList(c) +
        '<div class="rctl"><button type="button" class="sbtn" data-a="prev">上一步</button><button type="button" class="sbtn" data-a="next">下一步</button><button type="button" class="sbtn" data-a="replay">重播</button><a href="#c-' + c.id + '" data-a="open">看全文</a></div>';
      lit = -1;
    }
    function select(id, quiet) {
      sel = sel === id && !quiet ? null : id; manual = null; t0 = performance.now() + 900; render(); mv.kick();
      if (sel && scroller.scrollWidth > scroller.clientWidth) { var p = mv.px(BY[sel].o.lo, BY[sel].o.la); scroller.scrollTo({ left: clamp(p[0] - scroller.clientWidth / 2, 0, scroller.scrollWidth), behavior: RM.matches ? 'auto' : 'smooth' }); }
    }
    mv.onframe = function (now) {
      if (!sel) return false; var c = BY[sel], n = c.c.length;
      var shown = manual != null ? manual : (RM.matches ? n : clamp((now - t0) / PACE, 0, n)), k = Math.floor(shown + 1e-6);
      mv.gan.innerHTML = drawChain(mv, c, shown, now);
      if (k !== lit) { lit = k; markList(panel, k); }
      return !RM.matches;
    };
    mv.gst.addEventListener('click', function (e) { var g = e.target.closest ? e.target.closest('.pt') : null; if (g) select(g.getAttribute('data-id')); });
    chips.forEach(function (b) { b.addEventListener('click', function () { select(b.getAttribute('data-id')); }); });
    fbtns.forEach(function (b) { b.addEventListener('click', function () {
      filter = b.getAttribute('data-f'); fbtns.forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      if (sel && !vis(BY[sel])) sel = null; render();
    }); });
    panel.addEventListener('click', function (e) {
      var a = e.target.getAttribute && e.target.getAttribute('data-a'); if (!a || !sel) return; var n = BY[sel].c.length, curr = manual != null ? manual : lit;
      if (a === 'prev') manual = clamp(curr - 1, 0, n); else if (a === 'next') manual = clamp(curr + 1, 0, n);
      else if (a === 'replay') { manual = null; t0 = performance.now() + 500; lit = -1; }
      else if (a === 'open') { e.preventDefault(); if (openCase) openCase(sel); return; }
      mv.kick(); if (RM.matches || manual != null) mv.onframe(performance.now());
    });
    var rz; addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { mv.resize(); world(); statics(); mv.kick(); }, 150); });
    world(); render();
    selectRipple = function (id) { if (filter !== 'all' && BY[id].k !== filter) fbtns[0].click(); select(id, true); sec.scrollIntoView({ behavior: RM.matches ? 'auto' : 'smooth', block: 'start' }); };
  })();

  /* ---------- 02 要等多久 ---------- */
  (function () {
    var box = $('.lchart'); if (!box) return;
    var sec = $('#lag'), read = $('.lread', sec), vb = $$('.lens .sbtn', sec), mode = 'lag', cursor = { lag: 365, year: 1950 }, G = null;
    var cases = D.cases.filter(function (c) { return c.lag > 0 && c.o.y != null; });
    function fmtDays(d) {
      if (d < 1 / 24) return Math.max(1, Math.round(d * 1440)) + ' 分钟'; if (d < 1) return Math.round(d * 24) + ' 小时'; if (d < 60) return Math.round(d) + ' 天';
      if (d < 730) return Math.round(d / 30.4) + ' 个月'; return Math.round(d / 365.25) + ' 年';
    }
    function mark(k, x, y) { return k === 'block' ? '<rect class="mk" x="' + (x - 4.5) + '" y="' + (y - 4.5) + '" width="9" height="9" transform="rotate(45 ' + x + ' ' + y + ')"/>' : '<circle class="mk" cx="' + x + '" cy="' + y + '" r="5.5"/>'; }
    function build() {
      var W = Math.max(280, box.clientWidth), LW = W < 600 ? 108 : 176, PR = 20, RH = 26, TOP = 32, x0 = LW, x1 = W - PR, rows, X, inv, tk = [];
      if (mode === 'lag') {
        var a = Math.log10(D.ticks[0][0]) - 0.35, b = Math.log10(D.ticks[D.ticks.length - 1][0]) + 0.25;
        cases.forEach(function (c) { b = Math.max(b, Math.log10(c.lag) + 0.2); a = Math.min(a, Math.log10(c.lag) - 0.2); });
        X = function (d) { return x0 + (Math.log10(d) - a) / (b - a) * (x1 - x0); }; inv = function (x) { return Math.pow(10, a + (x - x0) / (x1 - x0) * (b - a)); };
        rows = cases.slice().sort(function (p, q) { return p.lag - q.lag; }); tk = D.ticks.map(function (t) { return [X(t[0]), t[1]]; });
      } else {
        var lo = 1e9, hi = 2030; cases.forEach(function (c) { lo = Math.min(lo, c.o.y); }); lo = Math.floor(lo / 100) * 100;
        var brk = lo < 1800 ? 0.25 : 0, mid = Math.max(lo, 1800);
        X = function (y) { return y < mid ? x0 + (y - lo) / (mid - lo) * brk * (x1 - x0) : x0 + (brk + (y - mid) / (hi - mid) * (1 - brk)) * (x1 - x0); };
        inv = function (x) { var f = (x - x0) / (x1 - x0); return f < brk ? lo + f / brk * (mid - lo) : mid + (f - brk) / (1 - brk) * (hi - mid); };
        rows = cases.slice().sort(function (p, q) { return p.o.y - q.o.y; });
        var ys = lo < 1800 ? [lo, 1800, 1850, 1900, 1950, 2000] : [1800, 1850, 1900, 1950, 2000].filter(function (y) { return y >= lo; });
        if (lo < 1800 && 1800 - lo > 600) ys.splice(1, 0, Math.round((lo + 1800) / 200) * 100);
        tk = ys.map(function (y) { return [X(y), yr(y)]; });
      }
      var H = TOP + rows.length * RH + 8, h = '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '">', lastx = -99;
      tk.forEach(function (t) { h += '<line class="gl" x1="' + t[0] + '" x2="' + t[0] + '" y1="' + (TOP - 6) + '" y2="' + (H - 4) + '"/>'; if (t[0] - lastx > 54) { h += '<text x="' + t[0] + '" y="16" text-anchor="middle">' + esc(t[1]) + '</text>'; lastx = t[0]; } });
      rows.forEach(function (c, i) {
        var y = TOP + i * RH + RH / 2, xa = mode === 'lag' ? x0 : X(c.o.y), xb = mode === 'lag' ? X(c.lag) : Math.max(X(c.r.y != null ? c.r.y : c.o.y), X(c.o.y) + 1);
        h += '<g class="lr ' + c.k + '" data-id="' + c.id + '" data-v="' + (mode === 'lag' ? c.lag : c.o.y) + '" data-e="' + (c.r.y != null ? c.r.y : c.o.y) + '"><rect class="rowbg" x="0" y="' + (y - RH / 2) + '" width="' + W + '" height="' + RH + '"/>' +
          '<text class="nm" x="' + (LW - 12) + '" y="' + (y + 4) + '" text-anchor="end" tabindex="0" role="link">' + esc(c.t) + '</text><line class="bar" x1="' + xa.toFixed(1) + '" x2="' + xb.toFixed(1) + '" y1="' + y + '" y2="' + y + '"/>' +
          (mode === 'year' ? '<circle class="o" cx="' + xa.toFixed(1) + '" cy="' + y + '" r="3.5"/>' : '') + mark(c.k, +xb.toFixed(1), y) + '</g>';
      });
      h += '<g class="cg"><line class="cur" y1="' + (TOP - 10) + '" y2="' + (H - 4) + '"/><rect class="curh" y="' + (TOP - 16) + '" width="9" height="9"/></g></svg>';
      box.innerHTML = h; G = { X: X, inv: inv, x0: x0, x1: x1, W: W }; setCur(X(cursor[mode]));
    }
    function setCur(x) {
      x = clamp(x, G.x0, G.x1); var v = G.inv(x); cursor[mode] = v;
      var l = $('.cur', box), hd = $('.curh', box); l.setAttribute('x1', x); l.setAttribute('x2', x); hd.setAttribute('x', x - 4.5);
      var nb = 0, nt = 0, names = [];
      $$('g.lr', box).forEach(function (g) {
        var c = BY[g.getAttribute('data-id')], on = mode === 'lag' ? c.lag <= v : (c.o.y <= v && +g.getAttribute('data-e') >= v);
        g.classList.toggle('past', on); if (on) { if (c.k === 'block') nb++; else nt++; names.push(c.t); }
      });
      if (mode === 'lag') read.innerHTML = '不到 <b>' + esc(fmtDays(v)) + '</b> 就牵动全球的：<b>' + (nb + nt) + '</b> 个（卡住 ' + nb + '，推一把 ' + nt + '）';
      else read.innerHTML = '<b>' + esc(yr(Math.round(v))) + '</b> 年：已经开始、还没走完的有 <b>' + (nb + nt) + '</b> 个' + (names.length ? '：' + esc(names.slice(0, 6).join('、')) + (names.length > 6 ? '…' : '') : '');
    }
    var down = false;
    function lx(e) { var r = box.getBoundingClientRect(); return (e.clientX - r.left) * (G.W / r.width); }
    box.addEventListener('pointerdown', function (e) { if (e.target.classList && e.target.classList.contains('nm')) return; if (lx(e) < G.x0 - 8) return; down = true; try { box.setPointerCapture(e.pointerId); } catch (_) {} setCur(lx(e)); });
    box.addEventListener('pointermove', function (e) { if (down) setCur(lx(e)); });
    box.addEventListener('pointerup', function () { down = false; }); box.addEventListener('pointercancel', function () { down = false; });
    box.addEventListener('keydown', function (e) {
      if (e.target.classList && e.target.classList.contains('nm')) { if (e.key === 'Enter') { openCase && openCase(e.target.parentNode.getAttribute('data-id')); } return; }
      var x = G.X(cursor[mode]); if (e.key === 'ArrowRight') { setCur(x + 12); e.preventDefault(); } else if (e.key === 'ArrowLeft') { setCur(x - 12); e.preventDefault(); }
    });
    box.addEventListener('click', function (e) { if (e.target.classList && e.target.classList.contains('nm') && openCase) openCase(e.target.parentNode.getAttribute('data-id')); });
    vb.forEach(function (b) { b.addEventListener('click', function () { mode = b.getAttribute('data-v'); vb.forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); build(); }); });
    var rz, lw = 0; addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (box.clientWidth !== lw) { lw = box.clientWidth; build(); } }, 150); });
    lw = box.clientWidth; build();
  })();

  /* ---------- 03 案例透镜列表 ---------- */
  (function () {
    var wrap = $('.rows'); if (!wrap) return;
    var sec = $('#cases'), rows = $$('.row', wrap), btns = $$('.lens .sbtn', sec);
    function groups(l) {
      if (l === 'kind') return [['block', '卡住了世界'], ['boost', '推了世界一把']];
      if (l === 'st') return D.st; return D.eras.map(function (n, i) { return [String(i), n]; });
    }
    function lens(l, animate) {
      var first = {}; if (animate) rows.forEach(function (r) { first[r.id] = r.getBoundingClientRect().top; });
      $$('.gh', wrap).forEach(function (g) { g.remove(); });
      var frag = document.createDocumentFragment();
      groups(l).forEach(function (g) {
        var rs = rows.filter(function (r) { return r.getAttribute('data-' + l) === g[0]; }).sort(function (a, b) { return a.getAttribute('data-year') - b.getAttribute('data-year'); });
        if (!rs.length) return; var hd = document.createElement('h3'); hd.className = 'gh';
        hd.innerHTML = (l === 'kind' ? km(g[0]) : '') + esc(g[1]) + '<small>' + rs.length + ' 个</small>'; frag.appendChild(hd); rs.forEach(function (r) { frag.appendChild(r); });
      });
      wrap.appendChild(frag);
      if (animate && !RM.matches && wrap.animate) rows.forEach(function (r) {
        var d = first[r.id] - r.getBoundingClientRect().top; if (Math.abs(d) > 1 && Math.abs(d) < 3000) r.animate([{ transform: 'translateY(' + d + 'px)' }, { transform: 'none' }], { duration: 500, easing: 'cubic-bezier(.22,1,.36,1)' });
      });
    }
    function toggle(r, open) {
      var b = $('.rh', r), body = $('.rb', r), want = open == null ? body.hidden : open;
      body.hidden = !want; b.setAttribute('aria-expanded', want ? 'true' : 'false');
    }
    rows.forEach(function (r) { $('.rh', r).addEventListener('click', function () { toggle(r); }); });
    btns.forEach(function (b) { b.addEventListener('click', function () { btns.forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); lens(b.getAttribute('data-l'), true); }); });
    $$('.tomap', wrap).forEach(function (a) { a.addEventListener('click', function (e) { if (selectRipple) { e.preventDefault(); selectRipple(a.getAttribute('data-id')); } }); });
    lens('kind', false);
    openCase = function (id) {
      var r = document.getElementById('c-' + id); if (!r) return; toggle(r, true);
      var y = r.getBoundingClientRect().top + scrollY - navH() - 120; window.scrollTo({ top: y, behavior: RM.matches ? 'auto' : 'smooth' });
    };
    if (location.hash.indexOf('#c-') === 0) setTimeout(function () { openCase(location.hash.slice(3)); }, 60);
  })();
})();
