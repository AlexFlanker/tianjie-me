/*DATA*/
/*MAP*/
/*PALMETA*/
(function(){
  const $ = (s, el=document) => el.querySelector(s);
  const PER = DATA.periods, PROV = DATA.provinces;
  const state = { p: 0, mode: 'fam', prov: null, playing: false, timer: null };
  const DIMS = [['food','食材','ingredients'],['tool','器具','utensils'],['tech','技法','techniques'],['taste','口味','flavors']];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  // ---------- lookups ----------
  const regionOf = (pi, code) => PER[pi].regions.find(r => r.provs.includes(code));
  function keyOf(pi, code){
    const r = regionOf(pi, code); if (!r) return null;
    const ov = (PER[pi].overrides||{})[code] || {};
    if (state.mode === 'fam') return { key: r.fam, css: 'fam-' + r.fam, name: r.name, note: r.note, region: r };
    if (state.mode === 'taste'){ const k = ov.taste || r.taste; return { key: k, css: 'taste-' + k, name: DATA.tastes[k].name, note: r.note, region: r }; }
    const k = ov.staple || r.staple; return { key: k, css: 'staple-' + k, name: DATA.staples[k].name, note: r.note, region: r };
  }
  function isDark(){ const t = document.documentElement.getAttribute('data-theme'); if (t) return t === 'dark'; return matchMedia('(prefers-color-scheme: dark)').matches; }
  const fillOf = css => css === 'staple-daomai' ? 'url(#hatch)' : `var(--${css})`;
  const needsLight = css => !!(PALMETA[isDark() ? 'dark' : 'light'][css]);

  // ---------- timeline ----------
  const tl = $('#tl');
  PER.forEach((p, i) => {
    const b = document.createElement('button');
    b.className = 'tl-item'; b.id = 'tl-' + p.id; b.setAttribute('aria-pressed', 'false');
    b.innerHTML = `<span class="n">${esc(p.name)}</span><span class="y">${esc(p.years)}</span>`;
    b.addEventListener('click', () => setPeriod(i));
    tl.appendChild(b);
  });
  function paintTimeline(){
    [...tl.querySelectorAll('.tl-item')].forEach((b, i) => { b.setAttribute('aria-pressed', String(i === state.p)); b.classList.toggle('past', i < state.p); });
    const items = tl.querySelectorAll('.tl-item'); const it = items[state.p];
    $('#tlfill').style.width = (it.offsetLeft + 14) + 'px';
    // v2：只横向滚时间轴自己，不带动整页（时间轴已不在首屏，scrollIntoView 会在载入时把页面拽下去）
    const sc = tl.closest('.tl-scroll');
    if (sc && sc.scrollWidth > sc.clientWidth) { const l = it.offsetLeft - 16, r = it.offsetLeft + it.offsetWidth + 16;
      if (l < sc.scrollLeft) sc.scrollTo({ left: l, behavior: 'smooth' }); else if (r > sc.scrollLeft + sc.clientWidth) sc.scrollTo({ left: r - sc.clientWidth, behavior: 'smooth' }); }
  }

  // ---------- map ----------
  const wrap = $('#mapwrap');
  const W = MAP.w, H = MAP.h + 46, ins = MAP.inset;
  const iw = ins.x1 - ins.x0, ih = ins.y1 - ins.y0, isc = 172 / iw, bw = 172, bh = ih * isc, bx = W - bw - 8, by = H - bh - 8;
  let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="中国省级行政区地图，按所选时期着色">
  <defs>
    <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="var(--staple-dao)"/><rect width="4" height="8" fill="var(--staple-mai)"/></pattern>
    <clipPath id="ic"><rect x="${ins.x0}" y="${ins.y0}" width="${iw}" height="${ih}"/></clipPath>
  </defs>
  <g id="layers">`;
  for (const [c, v] of Object.entries(MAP.prov)) svg += `<path class="prov" id="p-${c}" data-code="${c}" d="${v.d}" tabindex="0" role="button" aria-label="${esc(PROV[c].name)}"/>`;
  svg += `<path class="jd" d="${MAP.jd}"/>`;
  svg += MAP.islands.map(([x, y]) => `<circle class="isl" cx="${x}" cy="${y}" r="1.6"/>`).join('');
  svg += `</g><g id="labels">`;
  for (const [c, v] of Object.entries(MAP.prov)){ const p = PROV[c]; svg += `<text class="lbl" id="l-${c}" x="${v.c[0] + p.dx}" y="${v.c[1] + p.dy}" text-anchor="middle" dominant-baseline="middle">${esc(p.label)}</text>`; }
  svg += `</g>
  <g transform="translate(${bx} ${by}) scale(${isc}) translate(${-ins.x0} ${-ins.y0})" clip-path="url(#ic)" pointer-events="none"><rect class="inset-box" x="${ins.x0}" y="${ins.y0}" width="${iw}" height="${ih}" style="stroke-width:${(1.2 / isc).toFixed(2)}"/><use href="#layers"/></g>
  <text class="inset-title" x="${bx + 6}" y="${by + 14}">南海诸岛</text>
  <text class="map-note" x="12" y="${H - 12}">按现行省级行政区划 · 各时期分区为饮食文化区示意</text>
  </svg>`;
  wrap.innerHTML = svg;
  const paths = {}; const labels = {};
  for (const c of Object.keys(MAP.prov)) { paths[c] = $('#p-' + c); labels[c] = $('#l-' + c); }
  // inset clones can't be interactive; the main paths are.
  const hoverable = matchMedia('(hover: hover)').matches;
  for (const [c, el] of Object.entries(paths)){
    el.addEventListener('pointerenter', () => { if (hoverable) showInfo(c); highlightSame(c); });
    el.addEventListener('pointerleave', () => { clearHighlight(); });
    el.addEventListener('click', () => { if (hoverable) openDrawer(c); else { showInfo(c); } });
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openDrawer(c); } });
    el.addEventListener('focus', () => showInfo(c));
  }
  function highlightSame(code){
    const k = keyOf(state.p, code); if (!k) return;
    for (const c of Object.keys(paths)){ const kk = keyOf(state.p, c); const same = kk && (state.mode === 'fam' ? kk.region.id === k.region.id : kk.key === k.key); paths[c].classList.toggle('hi', same && c !== code); }
  }
  function clearHighlight(){ for (const c of Object.keys(paths)) paths[c].classList.remove('hi','dim'); }
  function paintMap(){
    for (const c of Object.keys(paths)){
      const k = keyOf(state.p, c);
      paths[c].style.fill = k ? fillOf(k.css) : 'var(--map-dim)';
      labels[c].classList.toggle('on-dark', k ? needsLight(k.css) : false);
    }
    wrap.querySelector('svg').dataset.mode = state.mode;
  }
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', paintMap);
  new MutationObserver(paintMap).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  // ---------- info bar ----------
  function showInfo(code){
    state.prov = code;
    const k = keyOf(state.p, code); const p = PROV[code];
    $('#ib-name').textContent = p.name;
    $('#ib-region').textContent = k ? (state.mode === 'fam' ? k.name : `${k.region.name} · ${k.name}`) : '';
    const pn = (DATA.provNotes[code]||{})[PER[state.p].id];
    $('#ib-note').textContent = (k ? k.note : '') + (pn ? ' ' + pn : '');
    $('#ib-sw').style.background = k ? fillOf(k.css) : 'var(--map-dim)';
    const go = $('#ib-go'); go.hidden = false; go.onclick = () => openDrawer(code);
  }

  // ---------- legend ----------
  function paintLegend(){
    const lg = $('#legend'); lg.innerHTML = '';
    const P = PER[state.p];
    if (state.mode === 'fam'){
      P.regions.forEach(r => {
        const d = document.createElement('div'); d.className = 'it';
        d.innerHTML = `<span class="sw" style="background:var(--fam-${r.fam})"></span>${esc(r.name)} <span class="cnt">${r.provs.map(c => PROV[c].short).join('')}</span>`;
        d.addEventListener('pointerenter', () => { for (const c of Object.keys(paths)) paths[c].classList.toggle('dim', !r.provs.includes(c)); });
        d.addEventListener('pointerleave', clearHighlight);
        lg.appendChild(d);
      });
      $('#legendnote').textContent = '同一色相 = 同一菜系家族（如巴蜀→川饭→川菜始终为朱红）；分区随时期分合，反映“南北分立→多元分化”的过程。';
    } else {
      const dict = state.mode === 'taste' ? DATA.tastes : DATA.staples;
      const used = new Map();
      for (const c of Object.keys(paths)){ const k = keyOf(state.p, c); if (k) used.set(k.key, (used.get(k.key)||0) + 1); }
      Object.keys(dict).forEach(k => { if (!used.has(k)) return;
        const d = document.createElement('div'); d.className = 'it'; d.title = dict[k].desc;
        const sw = (state.mode === 'staple' && k === 'daomai') ? `<span class="sw" style="background:repeating-linear-gradient(45deg,var(--staple-dao) 0 3px,var(--staple-mai) 3px 6px)"></span>` : `<span class="sw" style="background:var(--${state.mode}-${k})"></span>`;
        d.innerHTML = `${sw}${esc(dict[k].name)} <span class="cnt">${used.get(k)}</span>`;
        d.addEventListener('pointerenter', () => { for (const c of Object.keys(paths)){ const kk = keyOf(state.p, c); paths[c].classList.toggle('dim', !(kk && kk.key === k)); } });
        d.addEventListener('pointerleave', clearHighlight);
        lg.appendChild(d);
      });
      $('#legendnote').textContent = state.mode === 'taste' ? '口味主调为该分区在此时期最有代表性的味觉基调（辣椒直到清代才真正上桌，此前的“辣”是花椒、姜、茱萸的辛）。' : '主食按各区域当时的主要谷物/食物类型标注；稻麦兼作以斜纹表示，明清以后玉米薯类进入山区。';
    }
  }

  // ---------- period panel ----------
  function paintPanel(hit){
    const P = PER[state.p];
    let h = `<div class="kicker">第 ${state.p + 1} / ${PER.length} 期</div><h2>${esc(P.name)}</h2><div class="years">${esc(P.years)}<span>${esc(P.sub)}</span></div><p class="summary">${esc(P.summary)}</p><div class="dims">`;
    for (const [k, nm, en] of DIMS){
      h += `<section class="dim ${k}"><h3><i></i>${nm}<small>${en}</small></h3><ul>`;
      P.dims[k].forEach((it, i) => { h += `<li id="d-${k}-${i}"${hit === k + '-' + i ? ' class="hit"' : ''}><b>${esc(it.h)}</b>${esc(it.t)}${it.src && it.src !== '—' ? `<span class="src" title="${esc(it.src)}">${esc(it.src)}</span>` : ''}</li>`; });
      h += `</ul></section>`;
    }
    $('#panel').innerHTML = h + '</div>';
  }

  // ---------- matrix ----------
  function buildMatrix(){
    const t = $('#matrix');
    let h = '<thead><tr><th></th>' + PER.map((p, i) => `<th data-i="${i}">${esc(p.name)}<small>${esc(p.years)}</small></th>`).join('') + '</tr></thead><tbody>';
    for (const [k, nm] of DIMS){
      h += `<tr class="${k}"><th><i></i>${nm}</th>` + PER.map((p, i) => `<td data-i="${i}">` + p.dims[k].map((it, j) => `<button class="chip" data-i="${i}" data-k="${k}" data-j="${j}" title="${esc(it.t)}">${esc(it.h)}</button>`).join('') + '</td>').join('') + '</tr>';
    }
    t.innerHTML = h + '</tbody>';
    t.addEventListener('click', e => {
      const chip = e.target.closest('.chip'); const th = e.target.closest('thead th');
      if (chip){ setPeriod(+chip.dataset.i, chip.dataset.k + '-' + chip.dataset.j); scrollToAtlas(chip.dataset.k, chip.dataset.j); }
      else if (th && th.dataset.i){ setPeriod(+th.dataset.i); scrollToAtlas(); }
    });
  }
  function paintMatrix(){ $('#matrix').querySelectorAll('[data-i]').forEach(el => el.classList.toggle('act', +el.dataset.i === state.p)); }
  function scrollToAtlas(k, j){
    const target = (k != null) ? $('#d-' + k + '-' + j) : $('#panel');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // ---------- cards ----------
  function buildCards(){
    const box = $('#cards'); let h = '';
    for (const c of Object.keys(PROV)){
      const m = DATA.modern[c]; const cur = keyOf(PER.length - 1, c); const tk = ((PER[PER.length - 1].overrides||{})[c]||{}).taste || cur.region.taste;
      h += `<div class="card" data-code="${c}" role="button" tabindex="0"><div class="top"><span class="nm">${esc(PROV[c].name)}<small>${esc(PROV[c].short)}</small></span><span class="cu">${esc(m.cuisine)}</span></div>
      <div class="strip">${PER.map((p, i) => { const r = regionOf(i, c); return `<i style="background:var(--fam-${r.fam})" title="${esc(p.name)}：${esc(r.name)}"></i>`; }).join('')}</div>
      <div class="ts"><span class="sw" style="background:var(--taste-${tk})"></span>${esc(m.taste)}</div>
      <div class="dishes">${esc(m.dishes.slice(0, 4).join(' · '))}</div></div>`;
    }
    box.innerHTML = h;
    box.addEventListener('click', e => { const card = e.target.closest('.card'); if (card) openDrawer(card.dataset.code); });
    box.addEventListener('keydown', e => { const card = e.target.closest('.card'); if (card && (e.key === 'Enter' || e.key === ' ')){ e.preventDefault(); openDrawer(card.dataset.code); } });
  }

  // ---------- drawer ----------
  const drawer = $('#drawer'); let lastFocus = null;
  function openDrawer(code){
    const p = PROV[code], m = DATA.modern[code]; const tk = ((PER[PER.length - 1].overrides||{})[code]||{}).taste || regionOf(PER.length - 1, code).taste;
    let h = `<div class="hd"><h2 id="dr-title">${esc(p.name)}<small>${esc(p.short)}</small></h2><button class="close" id="dr-close" aria-label="关闭">×</button></div>
    <div class="cu">${esc(m.cuisine)}<span class="pill"><span class="sw" style="background:var(--taste-${tk})"></span>${esc(DATA.tastes[tk].name)}</span></div>
    <p class="story">${esc(m.story)}</p>
    <dl class="kv"><dt>代表菜</dt><dd class="dishes">${esc(m.dishes.join('、'))}</dd><dt>口味</dt><dd>${esc(m.taste)}</dd><dt>食材</dt><dd>${esc(m.food.join('、'))}</dd><dt>器具</dt><dd>${esc(m.tool.join('、'))}</dd><dt>技法</dt><dd>${esc(m.tech.join('、'))}</dd></dl>
    <h3>沿革 · 十个时期</h3><ul class="hist">`;
    PER.forEach((per, i) => {
      const r = regionOf(i, code); const ov = (per.overrides||{})[code]||{}; const tk2 = ov.taste || r.taste, sk = ov.staple || r.staple;
      const pn = (DATA.provNotes[code]||{})[per.id];
      h += `<li${i === state.p ? ' class="cur"' : ''}><i style="background:var(--fam-${r.fam})"></i><span class="p">${esc(per.name)}<small>${esc(per.years)}</small></span><span class="r"><b>${esc(r.name)}</b>${esc(r.note)}<span class="tt">口味：${esc(DATA.tastes[tk2].name)} · 主食：${esc(DATA.staples[sk].name)}</span>${pn ? `<span class="pn2">${esc(pn)}</span>` : ''}</span></li>`;
    });
    $('#drawer-pn').innerHTML = h + '</ul>';
    lastFocus = document.activeElement; drawer.hidden = false; document.body.style.overflow = 'hidden';
    $('#dr-close').addEventListener('click', closeDrawer); $('#dr-close').focus();
  }
  function closeDrawer(){ drawer.hidden = true; document.body.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus(); }
  $('#drawer-bd').addEventListener('click', closeDrawer);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !drawer.hidden) closeDrawer(); if (drawer.hidden && !e.target.closest('input,textarea')){ if (e.key === 'ArrowRight') setPeriod(Math.min(PER.length - 1, state.p + 1)); if (e.key === 'ArrowLeft') setPeriod(Math.max(0, state.p - 1)); } });

  // ---------- modes / play ----------
  $('#modes').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; state.mode = b.dataset.mode; $('#modes').querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b))); paintMap(); paintLegend(); if (state.prov) showInfo(state.prov); try{ localStorage.setItem('cuisine-mode', state.mode); }catch(e){} });
  const playBtn = $('#play');
  playBtn.addEventListener('click', () => { if (state.playing) stopPlay(); else startPlay(); });
  function startPlay(){ state.playing = true; playBtn.setAttribute('aria-pressed', 'true'); $('#playtxt').textContent = '停止'; if (state.p === PER.length - 1) setPeriod(0); state.timer = setInterval(() => { if (state.p >= PER.length - 1) stopPlay(); else setPeriod(state.p + 1); }, 2600); }
  function stopPlay(){ state.playing = false; playBtn.setAttribute('aria-pressed', 'false'); $('#playtxt').textContent = '播放演化'; clearInterval(state.timer); }

  function setPeriod(i, hit){
    state.p = i; paintTimeline(); paintMap(); paintLegend(); paintPanel(hit); paintMatrix(); if (state.prov) showInfo(state.prov);
    try{ localStorage.setItem('cuisine-period', String(i)); }catch(e){}
  }

  // ---------- refs ----------
  $('#refs-list').innerHTML = DATA.refs.map(r => `<li>${esc(r)}</li>`).join('');
  $('#mapnote').textContent = '地图底图：省级行政区边界数据来自阿里云 DataV GeoAtlas（含南海诸岛与十段线），经拓扑简化后按 Albers 等积圆锥投影绘制。各时期的“风味分区”是饮食文化区的示意划分，以今天的省级行政区为最小单位近似表示，不代表历史政区边界；同一省份内部（如陕北/陕南、桂北/桂南）的差异未在图上区分。年代与出处以正文标注为准，若有争议之处（如辣椒首载版本、《南方草木状》真伪）已在文字中说明。';

  // ---------- init ----------
  
  if (!hoverable){ $('#ib-name').textContent = '点按一个省份'; $('#ib-note').textContent = '查看它在当前时期所属的风味分区、口味与主食，再点“查看沿革”读完整故事。'; }
  buildMatrix(); buildCards();
  let p0 = 0, m0 = 'fam';
  try{ const sp = localStorage.getItem('cuisine-period'); if (sp !== null && PER[+sp]) p0 = +sp; const sm = localStorage.getItem('cuisine-mode'); if (sm && ['fam','taste','staple'].includes(sm)) m0 = sm; }catch(e){}
  state.mode = m0; $('#modes').querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.mode === m0)));
  setPeriod(p0);
  window.addEventListener('resize', paintTimeline);
})();
