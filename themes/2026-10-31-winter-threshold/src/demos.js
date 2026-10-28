(function () {
  'use strict';
  var D = window.YZ.D, S = window.YZ.sun, Spring = window.YZ.Spring;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var WD = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  function wd(iso) { var p = iso.split('-').map(Number); return WD[new Date(Date.UTC(p[0], p[1] - 1, p[2])).getUTCDay()]; }
  function md(iso) { var p = iso.split('-'); return parseInt(p[1], 10) + ' 月 ' + parseInt(p[2], 10) + ' 日'; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  var FEST = D.fest;

  /* ================= 纬度墙：图上左右拖换日期（按下即跳，1:1 跟手），滑块换纬度 ================= */
  (function initLatWall() {
    var stage = $('#wl-stage'), latI = $('#wl-lat'), svg = $('#wl-svg'); if (!stage || !latI) return;
    var latO = $('#wl-lat-o'), doyO = $('#wl-doy-o');
    var W = 640, H = 230, L = 40, R = 14, T = 12, B = 26, doy = 311;
    function x(d) { return L + (d - 1) / 364 * (W - L - R); }
    function y(h) { return T + (1 - h / 24) * (H - T - B); }
    var sp = new Spring({ from: 311, damping: 1, response: 0.3, eps: 0.02, onUpdate: function (v) { doy = clamp(Math.round(v), 1, 365); render(); } });
    function render() {
      var lat = parseFloat(latI.value), m = S.doyToMd(doy);
      latO.textContent = S.latTxt(lat); doyO.textContent = m.m + ' 月 ' + m.d + ' 日';
      var pts = [];
      for (var d = 1; d <= 365; d += 2) pts.push(x(d).toFixed(1) + ',' + y(S.dayLen(lat, d)).toFixed(1));
      var dl0 = S.dayLen(lat, doy), ss = S.sunset(lat, doy), X = x(doy).toFixed(1);
      var s = '<rect class="nite" x="' + L + '" y="' + T + '" width="' + (W - L - R) + '" height="' + (H - T - B) + '"/>';
      s += '<polygon points="' + x(1).toFixed(1) + ',' + y(0).toFixed(1) + ' ' + pts.join(' ') + ' ' + x(365).toFixed(1) + ',' + y(0).toFixed(1) + '" style="fill:var(--bg)"/>';
      [0, 6, 12, 18, 24].forEach(function (h) { s += '<line class="ln2" x1="' + L + '" y1="' + y(h).toFixed(1) + '" x2="' + (W - R) + '" y2="' + y(h).toFixed(1) + '"/><text class="dt" x="' + (L - 6) + '" y="' + (y(h) + 4).toFixed(1) + '" text-anchor="end">' + h + 'h</text>'; });
      [[1, '1 月'], [91, '4 月'], [182, '7 月'], [274, '10 月'], [365, '12 月']].forEach(function (t) { s += '<text class="dt" x="' + x(t[0]).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="middle">' + t[1] + '</text>'; });
      s += '<polyline class="cur" points="' + pts.join(' ') + '"/>';
      var band = D.order.map(function (id) { return FEST[id]; }).filter(function (f) { return Math.abs(f.lat - lat) <= 8; });
      band.forEach(function (f) { var d = S.isoDoy(f.date); s += '<circle class="pt" cx="' + x(d).toFixed(1) + '" cy="' + y(S.dayLen(f.lat, d)).toFixed(1) + '" r="3" opacity=".75"/>'; });
      s += '<line class="aglow" x1="' + X + '" y1="' + T + '" x2="' + X + '" y2="' + (H - B) + '"/><line class="amark" x1="' + X + '" y1="' + T + '" x2="' + X + '" y2="' + (H - B) + '"/>';
      s += '<circle class="knob" cx="' + X + '" cy="' + y(dl0).toFixed(1) + '" r="6"/>';
      s += '<text class="dt2" x="' + (x(doy) + (doy > 290 ? -10 : 10)).toFixed(1) + '" y="' + (y(dl0) - 12).toFixed(1) + '" text-anchor="' + (doy > 290 ? 'end' : 'start') + '">' + S.hm(dl0) + '</text>';
      svg.innerHTML = s;
      $('#wl-dl').textContent = S.hm(dl0); $('#wl-set').textContent = ss === null ? (dl0 >= 24 ? '极昼' : '极夜') : S.mm(ss); $('#wl-night').textContent = Math.round((1 - dl0 / 24) * 100) + '%';
      $('#wl-list').innerHTML = band.length ? band.map(function (f) { return '<div><button type="button" data-open="' + esc(f.id) + '">' + esc(f.short) + '</button><span>' + esc(f.city) + ' · ' + S.latTxt(f.lat) + ' · ' + esc(f.koppen) + ' · ' + esc(f.season) + '</span><small>' + md(f.date) + ' · 昼长 ' + S.hm(S.dayLen(f.lat, S.isoDoy(f.date))) + '</small></div>'; }).join('') : '<span class="none">这个纬度带（±8°）上没有本页收录的节日。本页最北的一行在斯德哥尔摩（北纬 59.3°），南半球只收了拉巴斯（南纬 16.5°）与悉尼（南纬 33.9°）。</span>';
      stage.closest('.demo').classList.toggle('over', dl0 < 9);
      stage.setAttribute('aria-valuenow', doy); stage.setAttribute('aria-valuetext', m.m + ' 月 ' + m.d + ' 日，昼长 ' + S.hm(dl0));
    }
    var drag = null;
    function doyAt(e) { var r = svg.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * W; return clamp(1 + (px - L) / (W - L - R) * 364, 1, 365); }
    stage.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return; drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, on: false };
      if (e.pointerType === 'mouse') { drag.on = true; try { stage.setPointerCapture(e.pointerId); } catch (er) {} sp.set(doyAt(e)); }
    });
    stage.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.on) { var dx = e.clientX - drag.sx, dy = e.clientY - drag.sy; if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return; if (Math.abs(dx) > Math.abs(dy)) { drag.on = true; try { stage.setPointerCapture(e.pointerId); } catch (er) {} } else { drag = null; return; } }
      sp.set(doyAt(e));
    });
    function end(e) { if (drag && e.pointerId === drag.id) drag = null; }
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    stage.addEventListener('keydown', function (e) {
      var d = doy; if (e.key === 'ArrowRight') d += 1; else if (e.key === 'ArrowLeft') d -= 1; else if (e.key === 'PageUp') d += 10; else if (e.key === 'PageDown') d -= 10; else if (e.key === 'Home') d = 1; else if (e.key === 'End') d = 365; else return;
      e.preventDefault(); sp.to(clamp(d, 1, 365));
    });
    latI.addEventListener('input', render);
    render();
  })();

  /* ================= 算日子 ================= */
  (function initDates() {
    var td = $('#td-year'); if (!td) return;
    var T = D.tables, CAL = window.CAL; if (CAL && CAL.setLunar) CAL.setLunar(D.lunar);
    function iso(y, m, d) { return y + '-' + (m < 10 ? '0' : '') + m + '-' + (d < 10 ? '0' : '') + d; }
    function nthWeekday(y, m, wdn, n) { var first = new Date(Date.UTC(y, m - 1, 1)).getUTCDay(), d = 1 + ((wdn - first + 7) % 7) + (n - 1) * 7; return iso(y, m, d); }
    function lunar(y, mon, day) { if (!CAL || !D.lunar[String(y)]) return null; var j = CAL.lunarToJdn(y, mon, false, day); if (!j) return null; var g = CAL.jdnToGreg(j); return iso(g.y, g.m, g.d); }
    function compute(y) {
      var rows = [], t = T.terms[String(y)];
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
      var lk = T.loy_krathong_official[y], fm = null;
      if (!lk && T.fullmoons[String(y)]) T.fullmoons[String(y)].forEach(function (s) { var dd = s.split(' ')[0], mmn = parseInt(dd.slice(5, 7), 10), day = parseInt(dd.slice(8, 10), 10), th = new Date(Date.parse(s.replace(' ', 'T') + ':00Z') + 7 * 3600e3).toISOString().slice(0, 10); if ((mmn === 10 && day >= 26) || (mmn === 11 && day <= 28)) fm = th; });
      rows.push(['水灯节 · Yi Peng', lk || (fm ? fm + '（天文望日，±1 天）' : '—'), lk ? '泰国官方公告（2015–2027）' : '泰历十二月望为算术历，这里只给天文望日']);
      rows.push(['感恩节（美国）', nthWeekday(y, 11, 4, 4), '11 月第四个周四']);
      rows.push(['圣露西亚', iso(y, 12, 13), '固定 12/13']);
      if (t) rows.push(['冬至', t.dongzhi.slice(0, 10), '太阳黄经 270°']);
      var zy = lunar(y, 7, 15); rows.push(['（对照）中元节 · 盂兰盆', (zy || '—') + '；日本 ' + iso(y, 8, 13) + '–16', '农历七月十五；日本月迟盆固定 8/13–16']);
      var moon = '';
      if (dw && hy) { var nm = new Date(Date.parse(dw.newmoon.replace(' UTC', 'Z').replace(' ', 'T')) + 8 * 3600e3).toISOString(), nmB = nm.slice(0, 10); moon = y + ' 年这轮朔（北京时间 ' + nmB + ' ' + nm.slice(11, 16) + '）：排灯节 ' + md(dw.date) + '（按德里日落时的 tithi），寒衣节 ' + md(hy) + '（按含朔时刻的那一天为初一）——' + (dw.date === hy ? '同一天。' : dw.date < hy ? '印度早一天。' : '中国早一天。') + (nmB !== hy ? ' 注意：这轮朔不是十月的朔（农历十月初一另有一轮朔）。' : ''); }
      return { rows: rows, moon: moon };
    }
    function go() {
      var y = parseInt(td.value, 10); if (isNaN(y) || y < 1900 || y > 2100) { $('#td-note').textContent = '请输入 1900–2100 的年份。'; return; }
      var r = compute(y), tb = $('#td-tab tbody');
      tb.innerHTML = r.rows.map(function (row) { var d = row[1].slice(0, 10), ok = /^\d{4}-\d{2}-\d{2}$/.test(d); return '<tr' + (y === 2026 && d >= '2026-10-31' && d <= '2026-11-09' ? ' class="hl"' : '') + '><td>' + esc(row[0]) + '</td><td class="dd">' + (ok ? md(d) + (row[1].length > 10 ? '<small>' + esc(row[1].slice(10)) + '</small>' : '') : esc(row[1])) + '</td><td class="wk">' + (ok ? wd(d) : '') + '</td><td><small style="display:inline">' + esc(row[2]) + '</small></td></tr>'; }).join('');
      $('#td-moon').textContent = r.moon; $('#td-note').textContent = y === 2026 ? '高亮的是这十天。' : '';
    }
    $('#td-go').addEventListener('click', go); td.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
    $('#td-next').addEventListener('click', function () { td.value = Math.min(2100, parseInt(td.value, 10) + 1); go(); });
    $('#td-prev').addEventListener('click', function () { td.value = Math.max(1900, parseInt(td.value, 10) - 1); go(); });
    go();
  })();
})();
