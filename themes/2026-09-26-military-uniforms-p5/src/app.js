(function () {
  'use strict';
  var D = window.UDATA, IMG = window.UIMAGES || {}, U = window.UniformFig;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  var CC = {}; D.COUNTRIES.forEach(function (c) { CC[c.k] = c; });
  CC.de = { k: 'de', name: '德国', short: '德' }; CC.ca = { k: 'ca', name: '加拿大', short: '加' };
  var ERA = {}; D.ERAS.forEach(function (e, i) { e.i = i; ERA[e.k] = e; });

  /* ---------- references ---------- */
  var GL = { cn: '中', us: '美', ru: '俄', uk: '英', fr: '法', de: '德' };
  var REF = {};
  Object.keys(D.REFS).forEach(function (g) {
    D.REFS[g].forEach(function (r) {
      var k = r[0], lab = /^x/.test(k) ? '加' + k.slice(1) : GL[g] + k.replace(/^[a-z]+/, '');
      REF[k] = { k: k, g: g, label: lab, text: r[1], url: r[2] };
    });
  });
  var LAB2KEY = {}; Object.keys(REF).forEach(function (k) { LAB2KEY[REF[k].label] = k; });
  function refLink(k) { var r = REF[k]; if (!r) return ''; return '<a class="rf" href="#ref-' + k + '" title="' + esc(r.text) + '">〔' + r.label + '〕</a>'; }
  function refLinks(arr) { return (arr || []).map(refLink).join(''); }
  function linkify(s) { return esc(s).replace(/〔([中美俄英法德加]\d+b?)〕/g, function (m, lab) { var k = LAB2KEY[lab]; return k ? refLink(k) : m; }); }

  function confClass(c) { c = String(c || ''); if (/^高/.test(c)) return 'hi'; if (/^低/.test(c)) return 'lo'; return ''; }
  function confBadge(c) { return '<span class="conf ' + confClass(c) + '" title="置信度"><i></i>置信度：' + esc(c) + '</span>'; }
  function tagChip(t) { var T = D.TAGS[t]; return '<span class="tag ' + t + '">' + esc(T.name) + '</span>'; }

  /* ---------- figures ---------- */
  function figParams(f) {
    if (!f) return null;
    var base = f.preset && U.PRESETS[f.preset] ? JSON.parse(JSON.stringify(U.PRESETS[f.preset])) : {};
    Object.keys(f).forEach(function (k) { if (k !== 'preset') base[k] = f[k]; });
    return base;
  }
  var figSeq = 0;
  function figSVG(f, title, w, h) {
    var p = figParams(f); if (!p) return '';
    figSeq++;
    return U.svg(p, { id: 'f' + figSeq, title: title || p.title || '军服示意图', width: w, height: h });
  }

  /* ---------- camo tiles for the colour bus ---------- */
  function rng(seed) { var s = seed >>> 0 || 1; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function svgURI(w, h, body) { return "url('data:image/svg+xml;utf8," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '">' + body + '</svg>').replace(/'/g, '%27') + "')"; }
  function tile(t, c, seed, fine) {
    var r = rng(seed || 7), b = '<rect width="100%" height="100%" fill="' + c[0] + '"/>', i, x, y, k, W = 48, H = 24;
    if (t === 'woodland') { for (i = 0; i < 14; i++) { k = c[1 + (i % (c.length - 1))]; x = r() * W; y = r() * H; b += '<ellipse cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" rx="' + (4 + r() * 7).toFixed(1) + '" ry="' + (2 + r() * 4).toFixed(1) + '" transform="rotate(' + (r() * 60 - 30).toFixed(0) + ' ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')" fill="' + k + '"/>'; } }
    else if (t === 'brush') { for (i = 0; i < 12; i++) { k = c[1 + (i % (c.length - 1))]; x = r() * W; y = r() * H; b += '<path d="M' + x.toFixed(1) + ' ' + y.toFixed(1) + 'q' + (5 + r() * 6).toFixed(1) + ' ' + (-3 - r() * 4).toFixed(1) + ' ' + (10 + r() * 8).toFixed(1) + ' ' + (-2 + r() * 4).toFixed(1) + '" stroke="' + k + '" stroke-width="' + (2.2 + r() * 2.4).toFixed(1) + '" stroke-linecap="round" fill="none"/>'; } }
    else if (t === 'lizard') { for (i = 0; i < 16; i++) { k = c[1 + (i % (c.length - 1))]; x = r() * W; y = r() * H; b += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + (5 + r() * 9).toFixed(1) + '" height="1.6" rx=".8" fill="' + k + '"/>'; } }
    else if (t === 'flora') { for (i = 0; i < 7; i++) { k = c[1 + (i % (c.length - 1))]; x = i * 7 + r() * 3; b += '<path d="M' + x.toFixed(1) + ' 0q3 6 0 12t0 12" stroke="' + k + '" stroke-width="' + (2 + r() * 2).toFixed(1) + '" fill="none"/>'; } }
    else if (t === 'digital') { var q = fine ? 2 : 3; for (i = 0; i < (fine ? 90 : 60); i++) { k = c[1 + (i % (c.length - 1))]; x = Math.floor(r() * W / q) * q; y = Math.floor(r() * H / q) * q; b += '<rect x="' + x + '" y="' + y + '" width="' + (q * (1 + Math.floor(r() * 3))) + '" height="' + q + '" fill="' + k + '"/>'; } }
    else if (t === 'multi') { for (i = 0; i < 16; i++) { k = c[1 + (i % (c.length - 1))]; x = r() * W; y = r() * H; b += '<ellipse cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" rx="' + (2 + r() * 5).toFixed(1) + '" ry="' + (1.5 + r() * 3).toFixed(1) + '" fill="' + k + '" fill-opacity=".72"/>'; } }
    return svgURI(W, H, b);
  }
  function segBG(s) {
    var c = s.c;
    if (s.t === 'solid') return 'background:' + c[0];
    if (s.t === 'split') return 'background:linear-gradient(180deg,' + c[0] + ' 0 50%,' + c[1] + ' 50% 100%)';
    if (s.t === 'hatch') return 'background:repeating-linear-gradient(135deg,' + c[0] + ' 0 6px,' + c[1] + ' 6px 10px,' + c[2] + ' 10px 14px)';
    if (s.t === 'unknown') return 'background:repeating-linear-gradient(135deg,rgba(150,150,140,.35) 0 4px,transparent 4px 8px)';
    return 'background-color:' + c[0] + ';background-image:' + tile(s.t, c, (s.a * 7 + s.b) % 997, s.fine) + ';background-size:48px 24px';
  }
  function lum(hex) { var n = parseInt(hex.slice(1), 16), r = n >> 16 & 255, g = n >> 8 & 255, b = n & 255; return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255; }
  function xPct(y) {
    var E = D.ERAS;
    if (y <= E[0].a) return 0;
    for (var i = 0; i < E.length; i++) { if (y < E[i].b || i === E.length - 1) { var f = Math.min(1, (y - E[i].a) / (E[i].b - E[i].a)); return (i + Math.max(0, f)) / E.length * 100; } }
    return 100;
  }

  /* ---------- guide ---------- */
  function renderGuide() {
    var h = '<thead><tr><th>类别</th>' + D.COUNTRIES.map(function (c) { return '<th>' + esc(c.name) + '</th>'; }).join('') + '</tr></thead><tbody>';
    D.CATS.forEach(function (cat) {
      h += '<tr><th>' + esc(cat.name) + '<small>' + esc(cat.def) + '</small></th>' + D.COUNTRIES.map(function (c) { return '<td>' + esc(cat.names[c.k]) + '</td>'; }).join('') + '</tr>';
    });
    $('#cats').innerHTML = h + '</tbody>';
    var L = '<li><div><h4>“为什么”的四种标签</h4>' + Object.keys(D.TAGS).map(function (t) { return tagChip(t) + ' <span class="note">' + esc(D.TAGS[t].desc) + '</span>'; }).join('<br>') + '</div></li>';
    L += '<li><div><h4>置信度</h4><span class="conf hi"><i></i>高</span> <span class="note">两个以上独立来源一致，或有条例 / 法令原文</span><br><span class="conf"><i></i>中</span> <span class="note">细节有出入，或只有一个权威来源</span><br><span class="conf lo"><i></i>低</span> <span class="note">只有百科、爱好者资料，或来源矛盾</span></div></li>';
    L += '<li><div><h4>图谱里的记号</h4><span class="note">格子右上角的小圆点＝该格置信度；“图”＝附有真实图片。示意图只画类型与关键细节，依据写在每张图下方。</span></div></li>';
    $('#legend').innerHTML = L;
  }

  /* ---------- matrix ---------- */
  function shortYear(y) { var s = String(y).split('；')[0]; return s.length > 18 ? s.slice(0, 17) + '…' : s; }
  function renderMatrix() {
    var h = '<div class="corner">时代 →<br>国家 ↓</div>';
    D.ERAS.forEach(function (e) { h += '<div class="eh" role="columnheader"><b>' + esc(e.name) + '</b><span>' + esc(e.range) + '</span></div>'; });
    h += '<div class="lane-lab" style="border-top:0">总线</div><div class="stage-row">';
    var SB = { '鲜艳': 'linear-gradient(90deg,#b0282e,#1f2a4d 45%,#1f3a2b 70%,#e6e1d3)', '卡其 / 灰': 'linear-gradient(90deg,#c3b091,#7c6a46 40%,#6f7462 65%,#7b96b2)', '迷彩': null, '数码': null, '多地形': null };
    D.BUS.stages.forEach(function (s, i) {
      var l = xPct(s.a), r = xPct(s.b), bg = SB[s.name];
      if (!bg) bg = s.name === '迷彩' ? 'url(' + tile('woodland', ['#8a8456', '#4e5b35', '#5a4632', '#1e1e1a'], 3).slice(4, -1) + ')' : s.name === '数码' ? 'url(' + tile('digital', ['#8a8d8f', '#c2b8a3', '#6e7b63', '#4f6b3a'], 5).slice(4, -1) + ')' : 'url(' + tile('multi', ['#b7a98b', '#6b7353', '#7a5c3e', '#4a3a2a'], 9).slice(4, -1) + ')';
      h += '<div class="stage" style="left:calc(' + l + '% + 3px);width:calc(' + (r - l) + '% - 6px);background-image:' + bg + ';background-size:' + (/gradient/.test(bg) ? 'cover' : '48px 24px') + '" title="' + esc(s.name + '：' + s.note) + '"><b>' + esc(s.name) + '</b><span>' + esc(s.note) + '</span></div>';
    });
    h += '</div>';
    D.COUNTRIES.forEach(function (c) {
      h += '<div class="lane-lab">色带</div><div class="lane" aria-label="' + esc(c.name) + '野战服颜色变化">';
      D.BUS.lanes[c.k].forEach(function (s) {
        var l = xPct(s.a), r = xPct(s.b), dark = lum(s.c[0]) < 0.45;
        h += '<div class="seg ' + (s.minor ? 'minor ' : '') + (dark ? 'dk' : 'lt') + '" style="left:' + l + '%;width:' + Math.max(0.6, r - l) + '%;' + segBG(s) + '" title="' + esc(c.name + ' ' + s.a + '–' + (s.b >= 2026 ? '今' : s.b) + '：' + s.label) + '">' + (s.minor ? '' : '<em>' + esc(s.label) + '</em>') + '</div>';
      });
      h += '</div>';
      h += '<div class="rowlab" role="rowheader"><b>' + esc(c.name) + '</b></div>';
      D.ERAS.forEach(function (e) {
        var cell = D.CELLS[c.k][e.k];
        if (!cell) { h += '<div class="cell empty">—</div>'; return; }
        var fig = cell.fig ? figSVG(cell.fig, c.name + ' ' + e.range + '：' + cell.name, 72, 158) : (cell.photos && cell.photos[0] ? '<img src="assets/' + esc(cell.photos[0]) + '" alt="' + esc(cell.name) + '" loading="lazy">' : '');
        var cls = confClass(cell.conf);
        h += '<button class="cell" type="button" data-c="' + c.k + '" data-e="' + e.k + '" aria-label="' + esc(c.name + '，' + e.name + '（' + e.range + '）：' + cell.name) + '">' +
          '<span class="badges"><span class="cdot ' + cls + '" title="置信度：' + esc(cell.conf) + '"></span>' + (cell.photos && cell.photos.length ? '<span class="ph" title="附真实图片">图</span>' : '') + '</span>' +
          '<span class="fig">' + fig + '</span><span class="nm">' + esc(cell.name) + '</span><span class="yr">' + esc(shortYear(cell.year)) + '</span></button>';
      });
    });
    $('#mx').innerHTML = h;
    var hint = '<span>← 手机上可左右滑动 →</span><span><i class="sw" style="background:var(--c-hi)"></i>置信度高</span><span><i class="sw" style="background:var(--c-mid)"></i>中</span><span><i class="sw" style="background:var(--c-lo)"></i>低</span><span><i class="sw" style="height:5px;background:#c3b091"></i>细条＝同期的少数部队（如英军殖民地卡其、伞兵迷彩）</span><span><i class="sw" style="background:repeating-linear-gradient(135deg,rgba(150,150,140,.45) 0 3px,transparent 3px 6px)"></i>本轮未核</span>';
    $('#mxhint').innerHTML = hint;
    $('#mx').addEventListener('click', function (ev) { var b = ev.target.closest('.cell[data-c]'); if (b) openCell(b.dataset.c, b.dataset.e, b); });
  }

  /* ---------- photos ---------- */
  function photoFig(f) {
    var m = IMG[f]; if (!m) return '';
    var lic = m.licUrl ? '<a href="' + esc(m.licUrl) + '" rel="license noopener" target="_blank">' + esc(m.lic) + '</a>' : esc(m.lic);
    var who = [m.author, m.inst].filter(Boolean).join('；');
    return '<figure class="photo"><a class="im" href="assets/' + esc(f) + '" target="_blank" rel="noopener"><img src="assets/' + esc(f) + '" alt="' + esc(m.cap.slice(0, 80)) + '" loading="lazy"></a>' +
      '<figcaption>' + esc(m.cap) + '<span class="meta">' + esc(who) + ' · ' + esc(m.date) + ' · ' + lic + ' · <a href="' + esc(m.page) + '" target="_blank" rel="noopener">来源：Wikimedia Commons</a></span></figcaption></figure>';
  }

  /* ---------- drawer ---------- */
  var drawer = $('#drawer'), pn = $('#drawer-pn'), lastFocus = null, cur = null;
  function openCell(ck, ek, from) {
    var c = CC[ck], e = ERA[ek], cell = D.CELLS[ck] && D.CELLS[ck][ek];
    if (!cell) return;
    cur = { c: ck, e: ek };
    if (from) lastFocus = from;
    var i = e.i, prev = D.ERAS[i - 1], next = D.ERAS[i + 1];
    var figs = '';
    if (cell.fig) figs += '<figure>' + figSVG(cell.fig, c.name + ' ' + e.range + '：' + cell.name, 150, 330) + '<figcaption>' + esc(cell.fig.title || '野战 / 作战形态') + '</figcaption></figure>';
    if (cell.fig2) figs += '<figure>' + figSVG(cell.fig2, cell.fig2.title, 150, 330) + '<figcaption>' + esc(cell.fig2.title || '') + '</figcaption></figure>';
    var sw = (cell.colors || []).map(function (x) { return '<span><i style="background:' + x[0] + '"></i>' + esc(x[1]) + ' <code style="font-size:11px;color:var(--muted)">' + x[0] + '</code></span>'; }).join('');
    var rows = D.CATS.map(function (cat) { return '<tr><th>' + esc(cat.name) + '</th><td>' + linkify(cell[cat.k] || '—') + '</td></tr>'; }).join('');
    var cards = D.CARDS.filter(function (x) { return x.cc === ck && x.era === ek; });
    var h = '<div class="pn-top"><span class="crumb">' + esc(c.name) + ' · ' + esc(e.name) + '（' + esc(e.range) + '）</span><span class="sp"></span>' +
      '<button type="button" data-go="' + (prev ? prev.k : '') + '"' + (prev ? '' : ' disabled') + '>← ' + (prev ? esc(prev.range) : '') + '</button>' +
      '<button type="button" data-go="' + (next ? next.k : '') + '"' + (next ? '' : ' disabled') + '>' + (next ? esc(next.range) : '') + ' →</button>' +
      '<button type="button" id="dr-close" aria-label="关闭">✕ 关闭</button></div>' +
      '<h2 id="dr-title">' + esc(cell.name) + '</h2><div class="yr2">' + esc(cell.year) + ' · ' + confBadge(cell.conf) + '</div>' +
      '<div class="pn-grid"><div>' + (figs ? '<div class="figs">' + figs + '</div>' : '') + (cell.figNote ? '<div class="fignote">' + linkify(cell.figNote) + '</div>' : '') + '</div>' +
      '<div><table class="four">' + rows + '</table>' + (sw ? '<div class="swatches">' + sw + '</div>' : '') +
      '<div class="why"><h4>为什么这样设计</h4>' + linkify(cell.why) + '</div>' +
      (cell.dispute ? '<div class="dispute"><h4>不同说法 / 未能核实</h4>' + linkify(cell.dispute) + '</div>' : '') +
      '<div class="srcline">' + (cell.confNote ? '<span>' + esc(cell.confNote) + '</span>' : '') + '<span>出处：' + refLinks(cell.refs) + '</span></div>' +
      (cards.length ? '<div class="srcline">相关卡片：' + cards.map(function (x) { return '<a href="#card-' + x.id + '" data-card="' + x.id + '">' + esc(x.year + ' ' + x.title) + '</a>'; }).join('；') + '</div>' : '') +
      '</div></div>' +
      ((cell.photos && cell.photos.length) ? '<div class="photos">' + cell.photos.map(photoFig).join('') + '</div>' : '<p class="note" style="margin-top:18px">这一格没有找到可合法使用且内容准确的真实图片，只用示意图。</p>');
    pn.innerHTML = h;
    drawer.hidden = false; document.body.style.overflow = 'hidden';
    pn.scrollTop = 0; pn.focus();
    try { history.replaceState(null, '', '#cell-' + ck + '-' + ek); } catch (err) {}
  }
  function closeDrawer() {
    drawer.hidden = true; document.body.style.overflow = ''; cur = null;
    try { history.replaceState(null, '', location.pathname + location.search); } catch (err) {}
    if (lastFocus) try { lastFocus.focus(); } catch (err) {}
  }
  $('#drawer-bd').addEventListener('click', closeDrawer);
  pn.addEventListener('click', function (ev) {
    var t = ev.target;
    if (t.closest('#dr-close')) { closeDrawer(); return; }
    var g = t.closest('[data-go]'); if (g && g.dataset.go) { openCell(cur.c, g.dataset.go); return; }
    var cd = t.closest('[data-card]'); if (cd) { ev.preventDefault(); closeDrawer(); var el = document.getElementById('card-' + cd.dataset.card); if (el) { el.scrollIntoView({ block: 'center' }); el.style.outline = '2px solid var(--accent)'; setTimeout(function () { el.style.outline = ''; }, 1600); } return; }
    var rf = t.closest('a.rf'); if (rf) { ev.preventDefault(); closeDrawer(); var id = rf.getAttribute('href').slice(1); var el2 = document.getElementById(id); if (el2) { el2.scrollIntoView({ block: 'center' }); try { history.replaceState(null, '', '#' + id); } catch (err) {} } }
  });
  document.addEventListener('keydown', function (ev) {
    if (drawer.hidden) return;
    if (ev.key === 'Escape') closeDrawer();
    if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
      var i = ERA[cur.e].i + (ev.key === 'ArrowLeft' ? -1 : 1);
      if (D.ERAS[i]) openCell(cur.c, D.ERAS[i].k);
    }
    if (ev.key === 'Tab') { // keep focus in dialog
      var f = pn.querySelectorAll('a[href],button:not([disabled])'); if (!f.length) return;
      var a = f[0], z = f[f.length - 1];
      if (ev.shiftKey && document.activeElement === a) { ev.preventDefault(); z.focus(); }
      else if (!ev.shiftKey && document.activeElement === z) { ev.preventDefault(); a.focus(); }
    }
  });

  /* ---------- cards ---------- */
  var ftag = 'all', fcc = 'all';
  function renderFilters() {
    var t = '<button class="chip" type="button" data-t="all" aria-pressed="true">全部</button>' + Object.keys(D.TAGS).map(function (k) { return '<button class="chip" type="button" data-t="' + k + '" aria-pressed="false">' + esc(D.TAGS[k].name) + '</button>'; }).join('');
    $('#f-tag').innerHTML = t;
    var cc = '<button class="chip" type="button" data-cc="all" aria-pressed="true">全部</button>' + D.COUNTRIES.map(function (c) { return '<button class="chip" type="button" data-cc="' + c.k + '" aria-pressed="false">' + esc(c.name) + '</button>'; }).join('') + '<button class="chip" type="button" data-cc="other" aria-pressed="false">其他（德、加）</button>';
    $('#f-cc').innerHTML = cc;
    $('#f-tag').addEventListener('click', function (ev) { var b = ev.target.closest('[data-t]'); if (!b) return; ftag = b.dataset.t; [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); renderCards(); });
    $('#f-cc').addEventListener('click', function (ev) { var b = ev.target.closest('[data-cc]'); if (!b) return; fcc = b.dataset.cc; [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); renderCards(); });
  }
  function renderCards() {
    var list = D.CARDS.filter(function (x) {
      if (ftag !== 'all' && x.tags.indexOf(ftag) < 0) return false;
      if (fcc === 'other') return !D.CELLS[x.cc];
      if (fcc !== 'all' && x.cc !== fcc) return false;
      return true;
    });
    var h = list.map(function (x) {
      var c = CC[x.cc], cell = D.CELLS[x.cc] && D.CELLS[x.cc][x.era];
      var mini = cell && cell.fig ? '<span class="mini" aria-hidden="true">' + figSVG(cell.fig, '', 46, 101) + '</span>' : '';
      return '<article class="tp" id="card-' + x.id + '">' +
        '<div class="hd">' + mini + '<div><div class="yr">' + esc(x.year) + '</div><div class="cc">' + esc(c.name) + ' · ' + esc(ERA[x.era].name) + '</div><h3>' + esc(x.title) + '</h3></div></div>' +
        '<div class="tags">' + x.tags.map(tagChip).join('') + '</div>' +
        '<p><b>发生了什么　</b>' + linkify(x.what) + '</p>' +
        '<p><b>为什么这样设计　</b>' + linkify(x.why) + '</p>' +
        (x.dispute ? '<div class="dis"><b>不同说法：</b>' + linkify(x.dispute) + '</div>' : '') +
        '<div class="ft">' + confBadge(x.conf) + '<span>' + refLinks(x.refs) + '</span>' + (cell ? '<button type="button" data-open="' + x.cc + ' ' + x.era + '">在图谱中查看 →</button>' : '') + '</div></article>';
    }).join('');
    $('#cardlist').innerHTML = h || '<p class="nores">没有符合条件的卡片。</p>';
  }
  $('#cardlist').addEventListener('click', function (ev) { var b = ev.target.closest('[data-open]'); if (b) { var p = b.dataset.open.split(' '); openCell(p[0], p[1], b); } });

  /* ---------- flows ---------- */
  function renderFlows() {
    $('#flowlist').innerHTML = D.FLOWS.map(function (f) {
      return '<li><span class="y">' + esc(f.year) + '</span><span class="ft"><span class="node">' + esc(f.from) + '</span><span class="arr">→</span><span class="node">' + esc(f.to) + '</span></span>' +
        '<span class="w">' + esc(f.what) + '</span><span class="m">' + confBadge(f.conf) + ' ' + refLinks(f.refs) + '</span></li>';
    }).join('');
  }

  /* ---------- gallery ---------- */
  function renderGallery() {
    var used = {}, groups = { cn: [], us: [], ru: [], uk: [], fr: [], other: [] };
    D.COUNTRIES.forEach(function (c) { D.ERAS.forEach(function (e) { var cell = D.CELLS[c.k][e.k]; (cell && cell.photos || []).forEach(function (f) { if (!used[f] && IMG[f]) { used[f] = 1; groups[c.k].push(f); } }); }); });
    Object.keys(IMG).forEach(function (f) { if (!used[f]) groups.other.push(f); });
    var names = { cn: '中国', us: '美国', ru: '俄罗斯 / 苏联', uk: '英国', fr: '法国', other: '其他国家（影响）' };
    var h = '';
    Object.keys(groups).forEach(function (g) { if (!groups[g].length) return; h += '<div class="gal-group"><h3>' + names[g] + '（' + groups[g].length + '）</h3><div class="gal">' + groups[g].map(photoFig).join('') + '</div></div>'; });
    $('#gallist').innerHTML = h;
  }

  /* ---------- references ---------- */
  function renderRefs() {
    var names = { cn: '中国', us: '美国（含加拿大 CADPAT）', ru: '俄罗斯 / 苏联', uk: '英国', fr: '法国', de: '德国 / 普鲁士（影响）' };
    $('#reflist').innerHTML = Object.keys(D.REFS).map(function (g) {
      return '<div><h3>' + names[g] + '</h3><ol>' + D.REFS[g].map(function (r) {
        var R = REF[r[0]];
        return '<li id="ref-' + r[0] + '"><b>' + R.label + '</b><span>' + esc(r[1]) + (r[2] ? ' <a href="' + esc(r[2]) + '" target="_blank" rel="noopener">' + esc(r[2].replace(/^https?:\/\//, '').slice(0, 64)) + (r[2].replace(/^https?:\/\//, '').length > 64 ? '…' : '') + '</a>' : '') + '</span></li>';
      }).join('') + '</ol></div>';
    }).join('');
  }

  /* ---------- theme ---------- */
  $('#themebtn').addEventListener('click', function () {
    var root = document.documentElement, curT = root.getAttribute('data-theme');
    var isDark = curT ? curT === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    var nt = isDark ? 'light' : 'dark'; root.setAttribute('data-theme', nt);
    try { localStorage.setItem('uniforms-theme', nt); } catch (e) {}
  });

  /* ---------- masthead strip ---------- */
  function renderStrip() {
    var picks = [['uk', 'E1', '1742', '英 · 红衣'], ['fr', 'E2', '1829', '法 · 红裤'], ['uk', 'E3', '1902', '英 · 卡其'], ['fr', 'E3', '1915', '法 · 地平线蓝'], ['ru', 'E4', '1943', '苏 · 保护色'],
      ['fr', 'E5', '1947', '法 · 蜥蜴纹'], ['us', 'E6', '1981', '美 · 林地'], ['cn', 'E7', '2007', '中 · 数码'], ['uk', 'E8', '2010', '英 · 多地形'], ['cn', 'E8', '2021', '中 · 细像素']];
    $('#strip').innerHTML = picks.map(function (p, i) {
      var cell = D.CELLS[p[0]][p[1]];
      return (i ? '<span class="ar" aria-hidden="true">›</span>' : '') + '<a class="st" href="#cell-' + p[0] + '-' + p[1] + '" data-c="' + p[0] + '" data-e="' + p[1] + '" title="' + esc(cell.name) + '">' + figSVG(cell.fig, p[3] + ' ' + p[2], 60, 132) + '<b>' + p[2] + '</b><small>' + esc(p[3]) + '</small></a>';
    }).join('');
    $('#strip').addEventListener('click', function (ev) { var a = ev.target.closest('a.st'); if (a) { ev.preventDefault(); openCell(a.dataset.c, a.dataset.e, a); } });
  }

  renderStrip();
  renderGuide(); renderMatrix(); renderFilters(); renderCards(); renderFlows(); renderGallery(); renderRefs();

  // deep link
  var m = /^#cell-([a-z]{2})-(E\d)$/.exec(location.hash);
  if (m) openCell(m[1], m[2]);
})();
