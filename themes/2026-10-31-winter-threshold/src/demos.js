(function () {
  'use strict';
  var D = window.YZ.D, S = window.YZ.sun;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var WD = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  function wd(iso) { var p = iso.split('-').map(Number); return WD[new Date(Date.UTC(p[0], p[1] - 1, p[2])).getUTCDay()]; }
  function md(iso) { var p = iso.split('-'); return parseInt(p[1], 10) + ' 月 ' + parseInt(p[2], 10) + ' 日'; }
  var FEST = D.fest;

  /* ================= 墙 ① 纬度与门槛 */
  var wl = $('#wl-lat');
  if (wl) {
    var latI = $('#wl-lat'), doyI = $('#wl-doy'), svg = $('#wl-svg'), latO = $('#wl-lat-o'), doyO = $('#wl-doy-o');
    var W = 640, H = 230, L = 40, R = 14, T = 12, B = 26;
    function x(d) { return L + (d - 1) / 364 * (W - L - R); }
    function y(h) { return T + (1 - h / 24) * (H - T - B); }
    function latTxt(v) { return v > 0 ? '北纬 ' + v + '°' : v < 0 ? '南纬 ' + (-v) + '°' : '赤道'; }
    function render() {
      var lat = parseFloat(latI.value), doy = parseInt(doyI.value, 10), m = S.doyToMd(doy);
      latO.textContent = latTxt(lat); doyO.textContent = m.m + ' 月 ' + m.d + ' 日';
      var pts = [], night = [];
      for (var d = 1; d <= 365; d += 2) { var dl = S.dayLen(lat, d); pts.push(x(d).toFixed(1) + ',' + y(dl).toFixed(1)); }
      var dl0 = S.dayLen(lat, doy), ss = S.sunset(lat, doy);
      var s = '<rect class="nite" x="' + L + '" y="' + T + '" width="' + (W - L - R) + '" height="' + (H - T - B) + '"/>';
      s += '<polygon class="nite" points="' + x(1).toFixed(1) + ',' + y(0).toFixed(1) + ' ' + pts.join(' ') + ' ' + x(365).toFixed(1) + ',' + y(0).toFixed(1) + '" style="fill:var(--bg);opacity:1"/>';
      [0, 6, 12, 18, 24].forEach(function (h) { s += '<line class="ln2" x1="' + L + '" y1="' + y(h).toFixed(1) + '" x2="' + (W - R) + '" y2="' + y(h).toFixed(1) + '"/><text class="dt" x="' + (L - 6) + '" y="' + (y(h) + 4).toFixed(1) + '" text-anchor="end">' + h + 'h</text>'; });
      [[1, '1 月'], [91, '4 月'], [182, '7 月'], [274, '10 月'], [365, '12 月']].forEach(function (t) { s += '<text class="dt" x="' + x(t[0]).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="middle">' + t[1] + '</text>'; });
      s += '<polyline class="cur" points="' + pts.join(' ') + '"/>';
      s += '<line class="amark" x1="' + x(doy).toFixed(1) + '" y1="' + T + '" x2="' + x(doy).toFixed(1) + '" y2="' + (H - B) + '"/><circle class="pt" cx="' + x(doy).toFixed(1) + '" cy="' + y(dl0).toFixed(1) + '" r="5"/>';
      s += '<text class="dt2" x="' + (x(doy) + (doy > 300 ? -8 : 8)).toFixed(1) + '" y="' + (y(dl0) - 10).toFixed(1) + '" text-anchor="' + (doy > 300 ? 'end' : 'start') + '">' + S.hm(dl0) + '</text>';
      // 这个纬度带上的节日（±8°）
      var band = D.order.map(function (id) { return FEST[id]; }).filter(function (f) { return Math.abs(f.lat - lat) <= 8; });
      band.forEach(function (f) { var d = S.isoDoy(f.date); s += '<circle class="pt" cx="' + x(d).toFixed(1) + '" cy="' + y(S.dayLen(f.lat, d)).toFixed(1) + '" r="3" opacity=".8"/>'; });
      svg.innerHTML = s;
      $('#wl-dl').textContent = S.hm(dl0); $('#wl-set').textContent = ss === null ? (dl0 >= 24 ? '极昼' : '极夜') : S.mm(ss); $('#wl-night').textContent = Math.round((1 - dl0 / 24) * 100) + '%';
      var wrap = $('#wl-list'), seen = {};
      wrap.innerHTML = band.length ? band.map(function (f) { var cl = f.climate || {}; return '<div><b>' + esc(f.short) + '</b><span>' + esc(f.city) + ' · ' + latTxt(Math.round(f.lat)) + ' · ' + esc(f.koppen) + ' · ' + esc(f.season) + '</span><small>' + md(f.date) + ' · 昼长 ' + S.hm(S.dayLen(f.lat, S.isoDoy(f.date))) + '</small></div>'; }).join('') : '<div class="none">这个纬度带（±8°）上没有本页收录的节日。北纬 60° 以北只有圣露西亚，南纬 20° 以南只有悉尼的万圣节。</div>';
      var over = dl0 < 9; $('#wl-lat').closest('.demo').classList.toggle('over', over);
    }
    latI.addEventListener('input', render); doyI.addEventListener('input', render);
    render();
  }

  /* ================= 墙 ② 年轮 */
  var ww = $('#ww-chips');
  if (ww) {
    var g = $('#wheel-g2'), svgw = g && g.closest('svg');
    ww.addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-doy]'); if (!b) return;
      $$('button', ww).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      var doy = parseInt(b.getAttribute('data-doy'), 10), deg = -(doy - 1) / 365 * 360, cx = parseFloat(svgw.getAttribute('data-cx')), cy = parseFloat(svgw.getAttribute('data-cy'));
      g.style.transition = reduced ? 'none' : 'transform .9s cubic-bezier(.16,1,.3,1)'; g.style.transformOrigin = cx + 'px ' + cy + 'px'; g.style.transform = 'rotate(' + deg + 'deg)';
      $$('.mt', g).forEach(function (t) { var x = parseFloat(t.getAttribute('x')), y = parseFloat(t.getAttribute('y')); t.style.transformOrigin = x + 'px ' + y + 'px'; t.style.transition = g.style.transition; t.style.transform = 'rotate(' + (-deg) + 'deg)'; });
      // 标签与引线不随环转：淡出、按新角度重排、淡入
      svgw.setAttribute('data-rot', deg); svgw.classList.add('relabel');
      clearTimeout(svgw._rl); svgw._rl = setTimeout(function () { if (window.YZ && YZ.wheelLabels) YZ.wheelLabels(svgw, deg); svgw.classList.remove('relabel'); }, reduced ? 0 : 450);
      var cen = $('.cen2', svgw); if (cen) cen.textContent = '顶上 = ' + b.textContent;
    });
  }

  /* ================= 工具 ① 算日子 */
  var td = $('#td-year');
  if (td) {
    var T = D.tables, CAL = window.CAL; if (CAL && CAL.setLunar) CAL.setLunar(D.lunar);
    function iso(y, m, d) { return y + '-' + (m < 10 ? '0' : '') + m + '-' + (d < 10 ? '0' : '') + d; }
    function nthWeekday(y, m, wdn, n) { var first = new Date(Date.UTC(y, m - 1, 1)).getUTCDay(), d = 1 + ((wdn - first + 7) % 7) + (n - 1) * 7; return iso(y, m, d); }
    function lunar(y, mon, day) { if (!CAL || !D.lunar[String(y)]) return null; var j = CAL.lunarToJdn(y, mon, false, day); if (!j) return null; var g = CAL.jdnToGreg(j); return iso(g.y, g.m, g.d); }
    function compute(y) {
      var rows = [], note = '';
      var t = T.terms[String(y)];
      rows.push(['万圣节 · Samhain', iso(y, 10, 31), '固定 10/31']);
      rows.push(['诸圣节 · 亡灵节（儿童）· Todos Santos', iso(y, 11, 1), '固定 11/1']);
      rows.push(['诸灵节 · 亡灵节（成人）', iso(y, 11, 2), '固定 11/2']);
      rows.push(['篝火夜', iso(y, 11, 5), '固定 11/5']);
      if (t) rows.push(['立冬', t.lidong.slice(0, 10), '太阳黄经 225° · ' + t.lidong.slice(11) + ' 北京时间']);
      var dw = T.diwali[String(y)]; if (dw) rows.push(['排灯节（吉祥天女祭）· Tihar 同夜', dw.date, (T.diwali_official[y] ? '印度中央政府假日表' : 'amanta 历朔日 · 德里日落 tithi') + '；朔 ' + dw.newmoon]);
      var hy = lunar(y, 10, 1); rows.push(['寒衣节（农历十月初一）', hy || '超出 1900–2100 月表', '含朔时刻之日为初一（GB/T 33661）']);
      rows.push(['圣马丁节', iso(y, 11, 11), '固定 11/11']);
      rows.push(['七五三', iso(y, 11, 15), '固定 11/15']);
      if (t) rows.push(['小雪', t.xiaoxue.slice(0, 10), '太阳黄经 240°']);
      rows.push(['新尝祭 · 勤劳感谢日', iso(y, 11, 23), '固定 11/23']);
      var xy = lunar(y, 10, 15); rows.push(['下元节（农历十月十五）', xy || '超出月表', '农历十月十五']);
      var lk = T.loy_krathong_official[y]; var fm = null;
      if (!lk && T.fullmoons[String(y)]) { T.fullmoons[String(y)].forEach(function (s) { var p = s.split(' '), dd = p[0], mmn = parseInt(dd.slice(5, 7), 10), day = parseInt(dd.slice(8, 10), 10); var th = new Date(Date.parse(s.replace(' ', 'T') + ':00Z') + 7 * 3600e3), thd = th.toISOString().slice(0, 10); if ((mmn === 10 && day >= 26) || (mmn === 11 && day <= 28)) fm = thd; }); }
      rows.push(['水灯节 · Yi Peng', lk || (fm ? fm + '（天文望日，±1 天）' : '—'), lk ? '泰国官方公告（2015–2027）' : '泰历十二月望为算术历，这里只给天文望日']);
      rows.push(['感恩节（美国）', nthWeekday(y, 11, 4, 4), '11 月第四个周四']);
      rows.push(['圣露西亚', iso(y, 12, 13), '固定 12/13']);
      if (t) rows.push(['冬至', t.dongzhi.slice(0, 10), '太阳黄经 270°']);
      var zy = lunar(y, 7, 15); rows.push(['（对照）中元节 · 盂兰盆', (zy || '—') + '；日本 ' + iso(y, 8, 13) + '–16', '农历七月十五；日本月迟盆固定 8/13–16']);
      var moon = '';
      if (dw && hy) { var nmB = new Date(Date.parse(dw.newmoon.replace(' UTC', 'Z').replace(' ', 'T')) + 8 * 3600e3).toISOString().slice(0, 10); moon = y + ' 年这轮朔（北京时间 ' + nmB + ' ' + new Date(Date.parse(dw.newmoon.replace(' UTC', 'Z').replace(' ', 'T')) + 8 * 3600e3).toISOString().slice(11, 16) + '）：排灯节 ' + md(dw.date) + '（按德里日落时的 tithi），寒衣节 ' + md(hy) + '（按含朔时刻的那一天为初一）——' + (dw.date === hy ? '同一天。' : dw.date < hy ? '印度早一天。' : '中国早一天。') + (nmB !== hy ? ' 注意：这轮朔不是十月的朔（农历十月初一另有一轮朔）。' : ''); }
      return { rows: rows, moon: moon, note: note };
    }
    function go() {
      var y = parseInt(td.value, 10); if (isNaN(y) || y < 1900 || y > 2100) { $('#td-note').textContent = '请输入 1900–2100 的年份。'; return; }
      var r = compute(y), tb = $('#td-tab tbody'), today = '2026-10-31';
      tb.innerHTML = r.rows.map(function (row) { var d = row[1].slice(0, 10), ok = /^\d{4}-\d{2}-\d{2}$/.test(d); return '<tr' + (y === 2026 && d >= '2026-10-31' && d <= '2026-11-09' ? ' class="hl"' : '') + '><td>' + esc(row[0]) + '</td><td class="dd">' + (ok ? md(d) + (row[1].length > 10 ? '<small>' + esc(row[1].slice(10)) + '</small>' : '') : esc(row[1])) + '</td><td class="wk">' + (ok ? wd(d) : '') + '</td><td><small style="display:inline">' + esc(row[2]) + '</small></td></tr>'; }).join('');
      $('#td-moon').textContent = r.moon; $('#td-note').textContent = y === 2026 ? '高亮的是这十天。' : '';
    }
    $('#td-go').addEventListener('click', go); td.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
    $('#td-next').addEventListener('click', function () { td.value = parseInt(td.value, 10) + 1; go(); });
    go();
  }

  /* ================= 工具 ② 同与异对照 */
  var pa = $('#tp-a');
  if (pa) {
    var pb = $('#tp-b');
    function card(id) {
      var f = FEST[id], cl = f.climate || {}, dl = S.dayLen(f.lat, S.isoDoy(f.date));
      // 长段落只取前两句，细节在第二、三章的卡片里
      function brief(t, n) { if (!t) return '—'; var parts = String(t).split(/(?<=[。；])/), out = '', i = 0; while (i < parts.length && (out + parts[i]).length <= (n || 110)) { out += parts[i]; i++; } if (!out) out = String(t).slice(0, n || 110); return (i < parts.length ? out.replace(/[。；]$/, '') + '……' : out); }
      var rows = [['城市 · 纬度', f.city + ' · ' + (f.lat >= 0 ? '北纬 ' : '南纬 ') + Math.abs(f.lat).toFixed(1) + '°', true], ['2026 年', md(f.date) + '（' + wd(f.date) + '）', true], ['当天昼长', S.hm(dl), true], ['气候带', f.koppen + (f.koppen_note ? ' · ' + String(f.koppen_note).split(/[，；（(]/)[0] : ''), false], ['门槛', f.season + '（' + f.kindName + '）', false], ['历法', f.basisName + (f.basisSub ? ' · ' + f.basisSub : ''), false], ['传播', f.spreadName, false], ['收成', brief(cl.harvest), false], ['雨季 / 季风', brief(cl.rain), false], ['霜', brief(cl.frost), false], ['请亡灵', brief(f.three.dead), false], ['点灯', brief(f.three.light), false], ['吃一顿', brief(f.three.food), false]];
      return '<h4>' + esc(f.name) + '</h4><dl>' + rows.map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd' + (r[2] ? ' class="k"' : '') + '>' + esc(r[1]) + '</dd>'; }).join('') + '</dl>' + (f.img ? '<figure><img src="assets/' + esc(f.img) + '" alt="" loading="lazy"></figure>' : '');
    }
    function upd() { $('#tp-ca').innerHTML = card(pa.value); $('#tp-cb').innerHTML = card(pb.value); }
    pa.addEventListener('change', upd); pb.addEventListener('change', upd);
    pa.value = 'diwali'; pb.value = 'hanyi'; upd();
  }

  /* ================= 工具 ③ 看点清单 */
  var ls = $('#tls-sel');
  if (ls) {
    function text(id) { var f = FEST[id], w = D.watch[id]; return f.name + '\n日期：' + w.when + '\n必看：' + w.see + '\n必吃：' + w.eat + '\n礼仪：' + w.mind + '\n— tianjie.me 一周一题 · 第 7 题'; }
    function upd2() { var f = FEST[ls.value], w = D.watch[ls.value]; $('#tls-out').innerHTML = '<h4>' + esc(f.name) + '</h4><p class="ld">' + esc(w.when) + '</p><dl><dt>必看</dt><dd>' + esc(w.see) + '</dd><dt>必吃</dt><dd>' + esc(w.eat) + '</dd><dt>礼仪</dt><dd>' + esc(w.mind) + '</dd><dt>在哪</dt><dd>' + esc(f.city) + ' · ' + esc(f.koppen) + ' · ' + esc(f.season) + '</dd></dl>'; $('#tls-msg').textContent = ''; }
    ls.addEventListener('change', upd2); upd2();
    $('#tls-copy').addEventListener('click', function () { var t = text(ls.value); if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function () { $('#tls-msg').textContent = '已复制'; }, function () { $('#tls-msg').textContent = '浏览器不让复制，请手动选取。'; }); else $('#tls-msg').textContent = '浏览器不让复制，请手动选取。'; });
  }
})();
