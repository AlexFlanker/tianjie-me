/* 第 3 题 · 舞从劳作来 · 页面行为（原生 JS，无依赖） */
(function(){
  'use strict';
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var C = window.CONTENT, MAP = window.MAP;
  var reduced = false; try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  /* ---------- 深浅色 ---------- */
  var root = document.documentElement;
  try { var saved = localStorage.getItem('yzyt-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  var tb = $('#theme-btn');
  if (tb) tb.addEventListener('click', function(){
    var dark = root.getAttribute('data-theme') === 'dark' || (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark'; root.setAttribute('data-theme', next);
    try { localStorage.setItem('yzyt-theme', next); } catch (e) {}
  });

  /* ---------- 入场 ---------- */
  var fades = $$('.fade');
  if ('IntersectionObserver' in window && !reduced){
    var fo = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); fo.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    fades.forEach(function(el){ fo.observe(el); });
  } else { fades.forEach(function(el){ el.classList.add('in'); }); }

  /* ---------- 导航：高度、当前章、进度 ---------- */
  var nav = $('#nav'), prog = $('#prog');
  function setNavH(){ if (nav) root.style.setProperty('--nav-h', nav.offsetHeight + 'px'); }
  setNavH(); window.addEventListener('resize', setNavH);
  var chapIds = ['top', 'c1', 'c2', 'c3', 'c4', 'c5', 'end'];
  var navLinks = {}; $$('[data-nav]').forEach(function(a){ navLinks[a.getAttribute('data-nav')] = a; });
  function onScroll(){
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (prog) prog.style.width = (h > 0 ? Math.min(100, y / h * 100) : 0) + '%';
    var cur = 'top', line = y + (nav ? nav.offsetHeight : 0) + window.innerHeight * 0.33;
    chapIds.forEach(function(id){ var el = document.getElementById(id); if (el && el.offsetTop <= line) cur = id; });
    if (y + window.innerHeight >= document.documentElement.scrollHeight - 4) cur = 'end';
    Object.keys(navLinks).forEach(function(k){ navLinks[k].classList.toggle('on', k === cur); });
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- 地图 ---------- */
  var wrap = $('#mapwrap'), prov = {}, routeLayer, labelLayer;
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function buildMap(){
    if (!wrap || !MAP) return;
    var W = MAP.w, H = MAP.h + 46, ins = MAP.inset;
    var iw = ins.x1 - ins.x0, ih = ins.y1 - ins.y0, isc = 172 / iw, bw = 172, bh = ih * isc, bx = W - bw - 8, by = H - bh - 8;
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="中国省级行政区地图，按所选时代高亮舞蹈发生地与传播路线">';
    s += '<defs><clipPath id="ic"><rect x="' + ins.x0 + '" y="' + ins.y0 + '" width="' + iw + '" height="' + ih + '"/></clipPath></defs><g id="layers">';
    Object.keys(MAP.prov).forEach(function(c){ s += '<path class="prov" id="p-' + c + '" d="' + MAP.prov[c].d + '"><title>' + esc(MAP.prov[c].name) + '</title></path>'; });
    s += '<path class="jd" d="' + MAP.jd + '"/>';
    s += MAP.islands.map(function(p){ return '<circle class="isl" cx="' + p[0] + '" cy="' + p[1] + '" r="1.6"/>'; }).join('');
    s += '</g><g id="routes"></g><g id="labels"></g>';
    s += '<g transform="translate(' + bx + ' ' + by + ') scale(' + isc + ') translate(' + (-ins.x0) + ' ' + (-ins.y0) + ')" clip-path="url(#ic)" pointer-events="none"><rect class="inset-box" x="' + ins.x0 + '" y="' + ins.y0 + '" width="' + iw + '" height="' + ih + '" style="stroke-width:' + (1.2 / isc).toFixed(2) + '"/><use href="#layers"/></g>';
    s += '<text class="inset-title" x="' + (bx + 6) + '" y="' + (by + 14) + '">南海诸岛</text>';
    s += '<text class="map-note" x="12" y="' + (H - 12) + '">按现行省级行政区划 · 高亮与路线为文化传播示意，非政区图</text></svg>';
    wrap.innerHTML = s;
    Object.keys(MAP.prov).forEach(function(c){ prov[c] = $('#p-' + c, wrap); });
    routeLayer = $('#routes', wrap); labelLayer = $('#labels', wrap);
  }
  function centroid(c){ var p = MAP.prov[c]; return p ? p.c : null; }
  function pathThrough(codes){
    var pts = codes.map(centroid).filter(Boolean); if (pts.length < 2) return '';
    var d = 'M' + pts[0][0] + ' ' + pts[0][1];
    for (var i = 1; i < pts.length; i++){
      var a = pts[i-1], b = pts[i]; var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 - Math.min(60, Math.hypot(b[0]-a[0], b[1]-a[1]) * 0.25);
      d += ' Q' + mx + ' ' + my + ' ' + b[0] + ' ' + b[1];
    }
    return d;
  }
  var curNode = -1;
  function showNode(i){
    if (!wrap || i === curNode) return; curNode = i;
    var n = C.nodes[i], m = n.map || {};
    Object.keys(prov).forEach(function(c){ prov[c].classList.toggle('hi', (m.highlight || []).indexOf(c) >= 0); });
    var r = '';
    (m.route || []).forEach(function(codes){ var d = pathThrough(codes); if (!d) return; r += '<path class="route" d="' + d + '"/>'; codes.forEach(function(c){ var p = centroid(c); if (p) r += '<circle class="rdot" cx="' + p[0] + '" cy="' + p[1] + '" r="4.5"/>'; }); });
    routeLayer.innerHTML = r;
    var used = {}; var l = '';
    (m.labels || []).forEach(function(lb){ var p = centroid(lb.code); if (!p) return; var k = Math.round(p[1] / 18); var dy = used[k] ? 16 : 0; used[k] = true; l += '<text class="lbl" x="' + p[0] + '" y="' + (p[1] - 10 + dy) + '" text-anchor="middle">' + esc(lb.text) + '</text>'; });
    labelLayer.innerHTML = l;
    var ln = $('#layer-name'), ly = $('#layer-years'); if (ln) ln.textContent = m.layer || n.title; if (ly) ly.textContent = n.years;
    $$('#era-strip button').forEach(function(b, j){ b.classList.toggle('on', j === i); });
    $$('.node').forEach(function(el, j){ el.classList.toggle('on', j === i); });
  }
  buildMap();
  var nodeEls = $$('.node');
  if (nodeEls.length){
    if ('IntersectionObserver' in window){
      var no = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) showNode(+e.target.getAttribute('data-node')); }); }, { rootMargin: '-35% 0px -50% 0px', threshold: 0 });
      nodeEls.forEach(function(el){ no.observe(el); });
    }
    showNode(0);
    $$('#era-strip button').forEach(function(b){ b.addEventListener('click', function(){ var i = +b.getAttribute('data-era'); nodeEls[i].scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' }); }); });
    var rail = $('#rail-fill'), nodesBox = $('#nodes');
    function railUpdate(){ if (!rail || !nodesBox) return; var r = nodesBox.getBoundingClientRect(); var line = window.innerHeight * 0.45; var h = Math.max(0, Math.min(r.height, line - r.top)); rail.style.height = h + 'px'; }
    window.addEventListener('scroll', railUpdate, { passive: true }); railUpdate();
  }

  /* ---------- 墨线小人 ---------- */
  var figs = $$('svg[data-fig]');
  var mounted = new Map();
  function mountOne(svg){
    if (mounted.has(svg) || typeof mountDanceFig !== 'function') return;
    var move = svg.getAttribute('data-fig'), st = svg.getAttribute('data-static');
    var sex = move === 'dou' ? 'm' : 'f';
    var h = mountDanceFig(svg, { move: move, sex: sex, style: 'ink', props: true, ribbon: !st });
    if (st && window.SHAN_MARKS) h.setTime(SHAN_MARKS[st] || 0.82);
    mounted.set(svg, h);
  }
  function unmountOne(svg){ var h = mounted.get(svg); if (!h) return; h.stop(); mounted.delete(svg); while (svg.firstChild) svg.removeChild(svg.firstChild); }
  if ('IntersectionObserver' in window){
    var vo = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) mountOne(e.target); else if (!e.target.getAttribute('data-static')) unmountOne(e.target); }); }, { rootMargin: '120px 0px' });
    figs.forEach(function(svg){ vo.observe(svg); });
  } else { figs.forEach(mountOne); }

  /* ---------- 对照表筛选 ---------- */
  var fGenre = 'all', fConf = 'all';
  function applyFilter(){ $$('#works tbody tr').forEach(function(tr){ var ok = (fGenre === 'all' || tr.getAttribute('data-genre') === fGenre) && (fConf === 'all' || tr.getAttribute('data-conf') === fConf); tr.classList.toggle('hide', !ok); }); }
  $$('#filters button').forEach(function(b){ b.addEventListener('click', function(){
    if (b.hasAttribute('data-f')){ fGenre = b.getAttribute('data-f'); $$('#filters [data-f]').forEach(function(x){ x.classList.toggle('on', x === b); }); }
    else { fConf = b.getAttribute('data-c'); $$('#filters [data-c]').forEach(function(x){ x.classList.toggle('on', x === b); }); }
    applyFilter(); }); });

  /* ---------- 动作查找器 ---------- */
  var allMoves = [];
  C.decks.forEach(function(d){ d.moves.forEach(function(m){ allMoves.push({ deck: d, m: m }); }); (d.names_only || []).forEach(function(n){ allMoves.push({ deck: d, m: { name: n, nameOnly: true } }); }); });
  var dl = $('#finder-list'); if (dl) dl.innerHTML = allMoves.map(function(x){ return '<option value="' + esc(x.m.name) + '">'; }).join('');
  function findMove(q){ q = (q || '').trim().replace(/\s+/g, ''); if (!q) return null; var exact = allMoves.filter(function(x){ return x.m.name.replace(/\s+/g, '') === q; })[0]; if (exact) return exact; return allMoves.filter(function(x){ return x.m.name.indexOf(q) >= 0 || q.indexOf(x.m.name.split('（')[0]) >= 0; })[0] || null; }
  function renderFinder(x){
    var out = $('#finder-out'); if (!out) return;
    if (!x){ out.innerHTML = '没找到这个动作。教材里的动作名见上方「卷之三」，或试试「闪身步」「狗熊哆嗦毛」「浪子踢球」。'; return; }
    var m = x.m, d = x.deck;
    var s = '';
    if (m.fig) s += '<div class="figbox"><svg viewBox="0 0 260 300" role="img" aria-label="' + esc(m.name) + ' 动态演示"></svg></div>';
    s += '<h4>' + esc(m.name) + ' <small style="font-family:Noto Sans SC,sans-serif;font-weight:400;font-size:12px;color:var(--muted)">' + esc(d.name) + '</small></h4>';
    if (m.nameOnly){ s += '<p>本次只在教材 / 文献里查到这个动作的名字，没有查到可靠的要领与演出记录，所以页面不写。</p>'; }
    else {
      if (m.cue && m.cue !== '——') s += '<p><b style="color:var(--ink)">口令</b>　' + esc(m.cue) + '</p>';
      if (m.how && !/^要领未|^仅见/.test(m.how)) s += '<p><b style="color:var(--ink)">要领</b>　' + esc(m.how) + '</p>';
      if (m.scene) s += '<p><b style="color:var(--ink)">场景</b>　' + esc(m.scene) + '</p>';
      var rows = C.works.filter(function(r){ return (r.combo + ' ' + (r.look || '')).indexOf(m.name.split('（')[0]) >= 0 || (m.see || []).some(function(w){ return r.work.indexOf(w.replace(/[《》]/g, '')) >= 0 || w.indexOf(r.work.replace(/[《》]/g, '').slice(0, 4)) >= 0; }); });
      var see = (m.see || []).slice();
      rows.forEach(function(r){ if (see.indexOf(r.work) < 0) see.push(r.work + (r.where ? '（' + r.where + '）' : '')); });
      if (see.length) s += '<p><b style="color:var(--ink)">能看到它的作品</b></p><ul>' + see.map(function(w){ return '<li>' + esc(w) + '</li>'; }).join('') + '</ul>';
      var id = 'mv-' + d.key + '-' + m.name; var el = document.getElementById(id);
      if (el){ s += '<p style="margin-top:8px"><a href="#' + esc(id) + '">↑ 到这张动作卡</a></p>'; }
    }
    out.innerHTML = s;
    var svg = $('svg', out); if (svg) mountDanceFig(svg, { move: m.fig, sex: m.fig === 'dou' ? 'm' : 'f', style: 'ink', props: true });
  }
  var fi = $('#finder-input');
  if (fi){
    $('#finder-go').addEventListener('click', function(){ renderFinder(findMove(fi.value)); });
    fi.addEventListener('keydown', function(e){ if (e.key === 'Enter') renderFinder(findMove(fi.value)); });
    $('#finder-rand').addEventListener('click', function(){ var pool = allMoves.filter(function(x){ return !x.m.nameOnly; }); var x = pool[Math.floor(Math.random() * pool.length)]; fi.value = x.m.name; renderFinder(x); });
  }

  /* ---------- 看点清单生成器 ---------- */
  var clOut = $('#cl-out'), clText = '';
  function genChecklist(){
    var g = $('#cl-genre').value, w = ($('#cl-work').value || '').trim();
    var q = C.quick.filter(function(x){ return x.genre === g; })[0];
    var d = C.decks.filter(function(x){ return x.name === g; })[0];
    var lines = [];
    var title = (w ? w + ' · ' : '') + g + ' · 看点清单';
    if (d){
      lines.push('角色：' + d.roles.map(function(r){ return r.name; }).join('、'));
      lines.push('场景：' + d.scenes.map(function(s){ return s.name; }).join(' / '));
      d.moves.slice(0, 4).forEach(function(m){ lines.push('动作「' + m.name + '」：' + (m.cue && m.cue !== '——' ? m.cue + '；' : '') + (m.how && !/^要领未|^仅见/.test(m.how) ? m.how.split('；')[0].split('。')[0] : '看它在场上什么时候出现')); });
      var rows = C.works.filter(function(r){ return r.genre === g; }).slice(0, 4);
      rows.forEach(function(r){ lines.push('作品《' + r.work.replace(/[《》]/g, '') + '》：' + (r.look || '')); });
    }
    if (q){
      lines.push('动律：' + q.motif);
      if (q.props) lines.push('道具：' + q.props);
      lines.push('看什么：' + q.watch);
      (q.works || []).forEach(function(wk){ lines.push('名作：' + wk.title + (wk.who ? ' · ' + wk.who : '') + (wk.year ? ' · ' + wk.year : '')); });
    }
    if (!lines.length){ lines.push('这个舞种本题没有收录看点，先看「卷之四」的速查卡。'); }
    clText = title + '\n' + lines.map(function(l){ return '□ ' + l; }).join('\n') + '\n—— 一周一题 · 第 3 题《舞从劳作来》 tianjie.me/t/dance-atlas/';
    clOut.innerHTML = '<h4>' + esc(title) + '</h4><ul>' + lines.map(function(l){ return '<li>' + esc(l) + '</li>'; }).join('') + '</ul>';
  }
  if (clOut){
    $('#cl-go').addEventListener('click', genChecklist);
    function copyFallback(){
      /* 剪贴板不可用时：把清单文字放进可选中的文本框，提示手动复制 */
      var btn = $('#cl-copy');
      clOut.innerHTML = '<p class="hint">这个浏览器不允许直接写入剪贴板，请在下面全选后复制：</p><textarea class="cl-raw" readonly rows="10"></textarea>';
      var ta = clOut.querySelector('textarea'); ta.value = clText; ta.focus(); ta.select();
      btn.textContent = '请手动复制'; setTimeout(function(){ btn.textContent = '复制文字'; }, 2000);
    }
    $('#cl-copy').addEventListener('click', function(){
      if (!clText) genChecklist();
      var btn = $('#cl-copy');
      function done(){ btn.textContent = '已复制'; setTimeout(function(){ btn.textContent = '复制文字'; }, 1500); }
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(clText).then(done, copyFallback);
        else copyFallback();
      } catch (e) { copyFallback(); }
    });
  }
})();
