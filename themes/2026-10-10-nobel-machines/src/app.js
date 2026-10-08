(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  /* ---------- 深浅色 */
  try {
    var saved = localStorage.getItem('yzyt-theme');
    if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  } catch (e) {}
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
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else {
    fades.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- 章节导航与进度 */
  var nav = $('#cnav'), prog = $('#prog');
  var links = $$('[data-nav]');
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-nav')); });
  function setNavH() { if (nav) root.style.setProperty('--nav-h', nav.offsetHeight + 'px'); }
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
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
          if (on && a.scrollIntoView && nav) {
            var r = a.getBoundingClientRect(), rr = nav.getBoundingClientRect();
            if (r.left < rr.left || r.right > rr.right) a.parentNode.scrollLeft += r.left - rr.left - 20;
          }
        }
      });
    });
  }
  setNavH(); onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { setNavH(); onScroll(); });

  /* 链接指到折叠块时把它打开 */
  function openTarget() {
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === 'DETAILS') { el.classList.remove('hide'); el.open = true; }
  }
  window.addEventListener('hashchange', openTarget);
  openTarget();

  /* ---------- 窄屏上放大示意图 */
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.zb');
    if (!b) return;
    var fr = b.parentNode, on = !fr.classList.contains('zoom');
    fr.classList.toggle('zoom', on);
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.textContent = on ? '缩小' : '放大';
  });

  /* ---------- 等了多少年：切换口径 */
  var ws = $('#wait-seg');
  if (ws) ws.addEventListener('click', function (ev) {
    var b = ev.target.closest('button');
    if (!b) return;
    var k = b.getAttribute('data-k');
    $$('button', ws).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    $$('#wait-rows .n').forEach(function (n) { n.textContent = n.getAttribute('data-' + k); });
  });

  /* ---------- 路线图筛选 */
  var chips = $('#road-chips');
  if (chips) {
    var st = { tier: 'all', kind: 'all', cn: 'all' };
    var apply = function () {
      var items = $$('#road .rw[data-tier], #topics .topic');
      items.forEach(function (el) {
        var ok = (st.tier === 'all' || el.getAttribute('data-tier') === st.tier) &&
                 (st.kind === 'all' || el.getAttribute('data-kind') === st.kind) &&
                 (st.cn === 'all' || el.getAttribute('data-cn') === '1');
        el.classList.toggle('hide', !ok);
      });
      $$('#road .tier-h').forEach(function (h) {
        var t = h.getAttribute('data-tier');
        h.style.display = $$('#road .rw[data-tier="' + t + '"]:not(.hide)').length ? '' : 'none';
      });
      $$('#topics [data-tier-h]').forEach(function (h) {
        var t = h.getAttribute('data-tier-h');
        h.style.display = $$('#topics .topic[data-tier="' + t + '"]:not(.hide)').length ? '' : 'none';
      });
    };
    chips.addEventListener('click', function (ev) {
      var b = ev.target.closest('button');
      if (!b) return;
      var g = b.parentNode, f = g.getAttribute('data-f');
      st[f] = b.getAttribute('data-v');
      $$('button', g).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      apply();
    });
  }

  /* ---------- 规模对比器 */
  var dataEl = $('#data'), D = null;
  try { D = JSON.parse(dataEl.textContent); } catch (e) {}
  var selA = $('#cmp-a'), selB = $('#cmp-b'), svg = $('#cmp-svg');
  if (D && selA && selB && svg) {
    var NS = 'http://www.w3.org/2000/svg';
    var items = {};
    D.machines.forEach(function (m) {
      items[m.id] = { name: m.name, year: m.year, size: m.tool.size_m, sizeWhat: m.tool.size_what, mass: m.tool.mass_t, massWhat: m.tool.mass_what,
        usd: m.cost.usd, usdText: m.cost.usdText, costText: m.cost.text, people: m.tool.people, peopleWhat: m.tool.people_what, span: m.tool.span, wait: m.tool.wait, shape: m.shape };
    });
    D.extra.forEach(function (x) {
      items[x.id] = { name: x.name, size: x.size_m, sizeWhat: x.note, shape: { kind: x.kind, w: x.w, h: x.h } };
    });
    var num = function (v, d) { return v.toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
    var fLen = function (m) {
      if (m == null) return '—';
      if (m < 1000) return num(m, 2) + ' 米';
      if (m < 1e7) return num(m / 1000, m < 1e5 ? 1 : 0) + ' 公里';
      return num(m / 1e7, 0) + ' 万公里';
    };
    var fMass = function (t) {
      if (t == null) return '—';
      if (t >= 1e8) return num(t / 1e8, 1) + ' 亿吨';
      if (t >= 1e4) return num(t / 1e4, 1) + ' 万吨';
      return num(t, 2) + ' 吨';
    };
    var fUsd = function (u) {
      if (u == null) return '—';
      if (u >= 1e8) return '约 ' + num(u / 1e8, u >= 2e9 ? 0 : 1) + ' 亿美元';
      return '约 ' + num(Math.round(u / 1e5) * 10, 0) + ' 万美元';
    };
    var el = function (tag, attrs, text) {
      var e = document.createElementNS(NS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      if (text != null) e.textContent = text;
      return e;
    };
    var drawShape = function (it, cx, base, k) {
      var s = it.shape, g = el('g', {});
      if (!s) {
        g.appendChild(el('text', { x: cx, y: base - 90, 'text-anchor': 'middle', 'class': 'tm' }, '标尺是温度，'));
        g.appendChild(el('text', { x: cx, y: base - 72, 'text-anchor': 'middle', 'class': 'tm' }, '没有可比的尺寸'));
        return g;
      }
      var w = s.w * k, h = s.h * k, big = Math.max(w, h);
      if (big < 2.5) {
        g.appendChild(el('circle', { cx: cx, cy: base - 2, r: 2, 'class': 'af' }));
        g.appendChild(el('line', { x1: cx, y1: base - 6, x2: cx, y2: base - 56, 'class': 'dim' }));
        var px = big < 0.01 ? '不到 0.01' : '约 ' + num(big, 2);
        g.appendChild(el('text', { x: cx, y: base - 78, 'text-anchor': 'middle', 'class': 'tm' }, '按同一比例'));
        g.appendChild(el('text', { x: cx, y: base - 62, 'text-anchor': 'middle', 'class': 'tm' }, '只有' + px + ' 像素'));
        return g;
      }
      if (s.kind === 'circ' || s.kind === 'ring') {
        g.appendChild(el('circle', { cx: cx, cy: base - h / 2, r: w / 2, 'class': s.kind === 'ring' ? 'o' : 'o fa' }));
        if (s.kind === 'ring' && w > 24) g.appendChild(el('circle', { cx: cx, cy: base - h / 2, r: w / 2 - 4, 'class': 'a o2' }));
      } else if (s.kind === 'line') {
        g.appendChild(el('line', { x1: cx - w / 2, y1: base - 8, x2: cx + w / 2, y2: base - 8, 'class': 'a o25' }));
        g.appendChild(el('circle', { cx: cx - w / 2, cy: base - 8, r: 3.5, 'class': 'af' }));
        g.appendChild(el('circle', { cx: cx + w / 2, cy: base - 8, r: 3.5, 'class': 'af' }));
      } else if (s.kind === 'L') {
        g.appendChild(el('path', { d: 'M' + (cx - w / 2) + ' ' + (base - h) + 'V' + base + 'H' + (cx + w / 2), 'class': 'o' }));
        g.appendChild(el('path', { d: 'M' + (cx - w / 2 + 3) + ' ' + (base - h) + 'V' + (base - 3) + 'H' + (cx + w / 2), 'class': 'a o2' }));
      } else if (s.kind === 'tri') {
        g.appendChild(el('path', { d: 'M' + (cx - w / 2) + ' ' + base + 'H' + (cx + w / 2) + 'L' + cx + ' ' + (base - h) + 'Z', 'class': 'o fa' }));
      } else {
        g.appendChild(el('rect', { x: cx - w / 2, y: base - h, width: w, height: h, 'class': 'o fa' }));
      }
      return g;
    };
    var render = function () {
      var A = items[selA.value], B = items[selB.value];
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var narrow = window.innerWidth < 720, W = narrow ? 360 : 600;
      svg.setAttribute('viewBox', '0 0 ' + W + ' 300');
      var base = 236, cw = W * 0.4, ch = 180;
      var mw = Math.max(A.shape ? A.shape.w : 0, B.shape ? B.shape.w : 0), mh = Math.max(A.shape ? A.shape.h : 0, B.shape ? B.shape.h : 0);
      var k = (mw && mh) ? Math.min(cw / mw, ch / mh) : 1;
      svg.appendChild(el('line', { x1: 10, y1: base, x2: W - 10, y2: base, 'class': 'o1' }));
      svg.appendChild(el('line', { x1: W / 2, y1: 30, x2: W / 2, y2: base + 46, 'class': 'dim d' }));
      [[A, W * 0.26], [B, W * 0.74]].forEach(function (p) {
        svg.appendChild(drawShape(p[0], p[1], base, k));
        svg.appendChild(el('text', { x: p[1], y: base + 22, 'text-anchor': 'middle', 'class': 'tb' }, p[0].name));
        svg.appendChild(el('text', { x: p[1], y: base + 41, 'text-anchor': 'middle', 'class': 'tm' }, fLen(p[0].size)));
      });
      var say = $('#cmp-say');
      if (A.size && B.size) {
        var r = B.size / A.size;
        if (Math.abs(r - 1) < 0.005) say.textContent = '两边一样大。';
        else if (r >= 1) say.textContent = '右边的跨度是左边的 ' + num(r, r < 10 ? 1 : 0) + ' 倍。';
        else say.textContent = '左边的跨度是右边的 ' + num(1 / r, 1 / r < 10 ? 1 : 0) + ' 倍。';
      } else {
        say.textContent = '其中一样没有可比的尺寸：莱顿低温实验室推到极限的是温度。';
      }
      $('#cmp-ha').textContent = A.name; $('#cmp-hb').textContent = B.name;
      var tbody = $('#cmp-tbl tbody');
      while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
      var cell = function (main, sub) {
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(main));
        if (sub) { var sm = document.createElement('small'); sm.textContent = sub; td.appendChild(sm); }
        return td;
      };
      var yrs = function (v) { return v == null ? '—' : v + ' 年'; };
      [['跨度', function (x) { return cell(fLen(x.size), x.sizeWhat); }],
       ['质量', function (x) { return cell(fMass(x.mass), x.massWhat); }],
       ['造价', function (x) { return cell(x.usdText || fUsd(x.usd), x.costText); }],
       ['人数', function (x) { return cell(x.people ? num(x.people) + ' 人' : '—', x.peopleWhat); }],
       ['设想到获奖', function (x) { return cell(yrs(x.span)); }],
       ['成果到获奖', function (x) { return cell(yrs(x.wait)); }]].forEach(function (row) {
        var tr = document.createElement('tr'), th = document.createElement('td');
        th.textContent = row[0]; tr.appendChild(th); tr.appendChild(row[1](A)); tr.appendChild(row[1](B));
        tbody.appendChild(tr);
      });
    };
    selA.value = 'michelson'; selB.value = 'ligo';
    selA.addEventListener('change', render); selB.addEventListener('change', render);
    var rt = null;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(render, 150); });
    render();
  }
})();
