/* 五面墙 + 四个小工具的逻辑。依赖 calendars.js 的 CAL 与 #data 里的 D。 */
(function () {
  'use strict';
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  CAL.setLunar(D.lunar);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  function hit(el) { if (!el) return; el.classList.remove('hit'); void el.offsetWidth; el.classList.add('hit'); }
  function bindSlider(id, fn) {
    var s = $('#' + id), o = $('#' + id + '-o'); if (!s) return null;
    var h = function () { if (o) o.textContent = s.value + (o.getAttribute('data-unit') || ''); fn(parseFloat(s.value)); };
    s.addEventListener('input', h); return { s: s, run: h, set: function (v) { s.value = v; h(); } };
  }
  var set = function (id, t) { var e = $('#' + id); if (e) e.textContent = t; };
  var gdate = function (y, m, d) { return y + '-' + pad(m) + '-' + pad(d); };
  var fromJdn = function (j) { var g = CAL.jdnToGreg(j); return gdate(g.y, g.m, g.d); };
  var hhmm = function (min) { min = ((min % 1440) + 1440) % 1440; var h = Math.floor(min / 60), m = Math.round(min - h * 60); if (m === 60) { h = (h + 1) % 24; m = 0; } return pad(h) + ':' + pad(m); };
  function dialSvg(min, size) {
    var t = ((min % 1440) + 1440) % 1440, ha = (t / 60 % 12) * 30, ma = (t % 60) * 6, R = function (a, r) { return [50 + r * Math.sin(a * Math.PI / 180), 50 - r * Math.cos(a * Math.PI / 180)]; };
    var tk = '', k; for (k = 0; k < 12; k++) { var p1 = R(k * 30, 44), p2 = R(k * 30, 48); tk += '<line class="tk" x1="' + p1[0].toFixed(1) + '" y1="' + p1[1].toFixed(1) + '" x2="' + p2[0].toFixed(1) + '" y2="' + p2[1].toFixed(1) + '"/>'; }
    var h = R(ha, 26), m = R(ma, 38);
    return '<svg class="dial' + (t < 360 || t >= 1080 ? ' night' : '') + '" viewBox="0 0 100 100" width="' + (size || 64) + '" height="' + (size || 64) + '"><circle class="face" cx="50" cy="50" r="48"/>' + tk + '<line class="hh" x1="50" y1="50" x2="' + h[0].toFixed(1) + '" y2="' + h[1].toFixed(1) + '"/><line class="mh" x1="50" y1="50" x2="' + m[0].toFixed(1) + '" y2="' + m[1].toFixed(1) + '"/><circle class="pin" cx="50" cy="50" r="2.5"/></svg>';
  }
  var DEMO = {};

  /* ---------- 墙 1 一年不是整数天 */
  DEMO.leap = function (root) {
    var wall = root.closest('.wall'), RULES = { none: [365, '不置闰'], jul: [365.25, '4 年 1 闰'], greg: [365.2425, '400 年 97 闰'], jal: [365 + 8 / 33, '33 年 8 闰'], c128: [365 + 31 / 128, '128 年 31 闰'], met: [365.2468, '19 年 7 闰（阴阳历，235 朔望月）'] };
    var TROP = 365.24219, rule = 'jul', years = 400, months = $('#lp-months'), mark = $('#lp-mark');
    var MN = ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月', '7 月', '8 月', '9 月', '10 月', '11 月', '12 月'], ML = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    months.innerHTML = MN.map(function (m, i) { return '<i style="flex:' + ML[i] + '"' + (i === 2 ? ' class="mar"' : '') + '>' + m + '</i>'; }).join('');
    function draw() {
      var mean = RULES[rule][0], err = (mean - TROP) * 86400, drift = (mean - TROP) * years; // 正：历年偏长 → 春分在历上越来越早
      var doy = 80 - drift; // 3 月 21 日 ≈ 第 80 天
      var wrapped = false; while (doy < 1) { doy += 365; wrapped = true; } while (doy > 365) { doy -= 365; wrapped = true; }
      var m = 0, d = Math.round(doy); while (d > ML[m]) { d -= ML[m]; m++; if (m > 11) { m = 11; break; } }
      mark.style.left = (doy / 365 * 100) + '%';
      set('lp-date', MN[m] + ' ' + d + ' 日'); set('lp-drift', (Math.abs(drift) < 0.5 ? '基本没漂' : '漂了 ' + num(Math.abs(drift), 1) + ' 天' + (drift > 0 ? '（提前）' : '（推后）')) + (wrapped ? '，已绕过一整年' : ''));
      set('lp-mean', mean.toFixed(5)); set('lp-err', (Math.abs(err) < 1 ? num(err, 2) + ' 秒' : Math.abs(err) >= 60 ? num(err / 60, 1) + ' 分钟' : num(err, 0) + ' 秒')); set('lp-day', Math.abs(err) < 1e-6 ? '—' : num(86400 / Math.abs(err), 0) + ' 年');
      var out = m !== 2;
      if (out !== root.classList.contains('over')) { root.classList.toggle('over', out); if (out) hit(wall); }
    }
    var sl = bindSlider('lp-y', function (v) { years = v; draw(); });
    $$('.dchips button[data-rule]', root).forEach(function (b) { b.addEventListener('click', function () { rule = b.getAttribute('data-rule'); $$('.dchips button[data-rule]', root).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(); }); });
    sl.run();
  };

  /* ---------- 墙 2 阴历漂移 */
  DEMO.lunar = function (root) {
    var isl = $('#ln-isl'), cn = $('#ln-cn'), heb = $('#ln-heb'), seasons = $('#ln-seasons');
    var SEAS = [['春分', 80], ['夏至', 172], ['秋分', 266], ['冬至', 356]];
    seasons.innerHTML = SEAS.map(function (s) { var a = s[1] / 365 * 2 * Math.PI - Math.PI / 2; return '<line class="st" x1="' + (100 + 72 * Math.cos(a)).toFixed(1) + '" y1="' + (100 + 72 * Math.sin(a)).toFixed(1) + '" x2="' + (100 + 84 * Math.cos(a)).toFixed(1) + '" y2="' + (100 + 84 * Math.sin(a)).toFixed(1) + '"/><text class="rc2" x="' + (100 + 94 * Math.cos(a)).toFixed(1) + '" y="' + (100 + 94 * Math.sin(a) + 4).toFixed(1) + '" text-anchor="middle">' + s[0] + '</text>'; }).join('')
      + '<text class="rc2" x="100" y="22" text-anchor="middle">1 月</text>';
    function place(g, doy) { var a = doy / 365 * 2 * Math.PI - Math.PI / 2; g.setAttribute('transform', 'translate(' + (100 + 78 * Math.cos(a)).toFixed(1) + ' ' + (100 + 78 * Math.sin(a)).toFixed(1) + ')'); }
    function draw(Y) {
      var j0 = CAL.gregToJdn(Y, 1, 1), j1 = CAL.gregToJdn(Y + 1, 1, 1);
      // 斋月：找落在本公历年的 1 赖买丹
      var iy = Math.floor((Y - 622) * 1.0307) + 1, rams = [], k;
      for (k = iy - 1; k <= iy + 2; k++) { var jr = CAL.islToJdn(k, 9, 1); if (jr >= j0 && jr < j1) rams.push(jr); }
      var cny = CAL.lunarToJdn(Y, 1, false, 1), rh = CAL.hebToJdn(Y + 3761, 7, 1);
      if (rams.length) { place(isl, rams[0] - j0); isl.style.display = ''; } else isl.style.display = 'none';
      if (cny) { place(cn, cny - j0); cn.style.display = ''; } else cn.style.display = 'none';
      place(heb, rh - j0);
      set('ln-yr', Y);
      set('ln-r1', rams.length ? rams.map(fromJdn).join(' 与 ') : '本年没有'); set('ln-r2', cny ? fromJdn(cny) : '—'); set('ln-r3', fromJdn(rh));
      var cy = CAL.jdnToLunar(cny || j0), hl = CAL.hebLeap(Y + 3761);
      var leapM = D.lunarLeap[String(Y)];
      $('#ln-note').textContent = '斋月每年提前约 11 天，约 33 年绕一圈' + (rams.length === 2 ? '——这一年有两个斋月开始日' : '') + '；农历 ' + Y + ' 年' + (leapM ? '闰' + CAL.CN_M[leapM - 1] + '月' : '无闰月') + '，犹太历 ' + (Y + 3761) + ' 年' + (hl ? '是闰年（13 个月）' : '是平年') + '——两种阴阳历用闰月把新年拉回同一个季节。';
    }
    var sl = bindSlider('ln-y', draw); sl.run();
  };

  /* ---------- 墙 3 均时差 */
  DEMO.eot = function (root) {
    var curve = $('#eo-curve'), dot = $('#eo-dot'), an = $('#eo-an'), X = function (d) { return 40 + (d - 1) / 364 * 520; }, Y = function (e) { return 95 - e * 4.6; };
    var d, pts = []; for (d = 1; d <= 365; d++) pts.push(X(d).toFixed(1) + ' ' + Y(CAL.eot(d)).toFixed(1));
    curve.setAttribute('d', 'M' + pts.join(' L'));
    // 小日行迹（8 字）：x = 均时差，y = 赤纬
    var an8 = []; for (d = 1; d <= 365; d += 3) an8.push((540 + CAL.eot(d) * 1.4).toFixed(1) + ' ' + (60 - CAL.decl(d) * 180 / Math.PI * 1.1).toFixed(1));
    an.innerHTML = '<path class="o2" d="M' + an8.join(' L') + 'Z"/><circle id="eo-an-dot" class="pt3" r="3.5" cx="540" cy="60"/><text class="dt" x="540" y="112" text-anchor="middle">日行迹</text>';
    var and = $('#eo-an-dot'), MN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    function draw(doy) {
      var e = CAL.eot(doy); dot.setAttribute('cx', X(doy)); dot.setAttribute('cy', Y(e)); and.setAttribute('cx', 540 + e * 1.4); and.setAttribute('cy', 60 - CAL.decl(doy) * 180 / Math.PI * 1.1);
      var m = 0, dd = doy; while (dd > MN[m]) { dd -= MN[m]; m++; }
      set('eo-date', (m + 1) + ' 月 ' + dd + ' 日'); set('eo-eot', (e >= 0 ? '+' : '−') + num(Math.abs(e), 1) + ' 分钟'); set('eo-sun', hhmm(720 - e));
      root.classList.toggle('over', Math.abs(e) > 14);
    }
    var sl = bindSlider('eo-d', draw); sl.run();
  };

  /* ---------- 墙 4 / 工具 2 你的正午 */
  DEMO.noon = function (root) {
    var pid = root.id.replace('noon-', ''), lon = $('#' + pid + '-lon'), tz = $('#' + pid + '-tz'), date = $('#' + pid + '-date'), clock = $('#' + pid + '-clock');
    function draw() {
      var L = parseFloat(lon.value), T = parseFloat(tz.value); if (!isFinite(L) || !isFinite(T)) return;
      var p = (date.value || '2026-10-24').split('-').map(Number), doy = CAL.dayOfYear(p[0], p[1], p[2]), e = CAL.eot(doy);
      var noon = CAL.solarNoonMin(L, T, doy), central = T * 15, dl = (central - L) * 4;
      clock.innerHTML = dialSvg(noon, 96);
      set(pid + '-noon', hhmm(noon)); set(pid + '-r1', (central >= 0 ? '东经 ' : '西经 ') + num(Math.abs(central), 1) + '°'); set(pid + '-r2', (dl >= 0 ? '晚 ' : '早 ') + num(Math.abs(dl), 0) + ' 分钟'); set(pid + '-r3', (e >= 0 ? '+' : '−') + num(Math.abs(e), 1) + ' 分钟');
      root.classList.toggle('over', Math.abs(noon - 720) > 60);
    }
    [lon, tz, date].forEach(function (i) { i.addEventListener('input', draw); });
    $$('.dchips button[data-city]', root).forEach(function (b) { b.addEventListener('click', function () { var p = b.getAttribute('data-city').split('|'); lon.value = p[0]; tz.value = p[1]; $$('.dchips button[data-city]', root).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(); }); });
    draw();
  };

  /* ---------- 墙 5 自转不稳 */
  DEMO.lod = function (root) {
    var P = D.deltaT, cur = $('#lod-cur'), fig = $('.dtfig', root);
    function dt(y) { var i; for (i = 0; i < P.length - 1; i++) if (y >= P[i][0] && y <= P[i + 1][0]) return P[i][1] + (P[i + 1][1] - P[i][1]) * (y - P[i][0]) / (P[i + 1][0] - P[i][0]); return y < P[0][0] ? P[0][1] : P[P.length - 1][1]; }
    function draw(y) {
      var v = dt(y), slope = (dt(y + 0.5) - dt(y - 0.5)); // 秒 / 年
      var n = D.leaps.filter(function (s) { return parseInt(s.slice(0, 4), 10) < y || (parseInt(s.slice(0, 4), 10) === y && s.slice(5) === '06-30'); }).length;
      set('lod-dt', (v >= 0 ? '+' : '−') + num(Math.abs(v), 1)); set('lod-ls', y < 1972 ? '还没有闰秒制度' : n + ' 次'); set('lod-lod', (slope >= 0 ? '+' : '−') + num(Math.abs(slope) / 365.25 * 1000, 2) + ' ms（由 ΔT 年差分换算）');
      cur.style.left = ((y - 1900) / 130 * 93 + 5) + '%'; cur.textContent = y;
      root.classList.toggle('over', y >= 2016 && slope < 0.3);
    }
    var sl = bindSlider('lod-y', draw); sl.run();
  };

  $$('[data-demo]').forEach(function (r) { var k = r.getAttribute('data-demo'); if (DEMO[k]) try { DEMO[k](r); } catch (e) { if (window.console) console.error(k, e); } });

  /* ---------- 工具 1 历法换算器 */
  (function () {
    var root = $('.tconv'); if (!root) return;
    var grid = $('#cv-grid'), date = $('#cv-date'), WD = ['日', '一', '二', '三', '四', '五', '六'];
    var systems = [
      { id: 'jul', name: '儒略历', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { return CAL.jdnToJul(j); }, to: function (f) { return CAL.julToJdn(f.y, f.m, f.d); }, note: '1582 年以前欧洲通用；俄国用到 1918，东正教会历至今' },
      { id: 'jdn', name: '儒略日数', fields: [['j', 'JDN']], from: function (j) { return { j: j }; }, to: function (f) { return f.j; }, note: 'Scaliger 1583；从公元前 4713-01-01 正午起算的天数，天文学家的通用计数' },
      { id: 'cn', name: '农历', fields: [['y', '年'], ['m', '月'], ['l', '闰 1/0'], ['d', '日']], from: function (j) { var l = CAL.jdnToLunar(j); return l ? { y: l.y, m: l.m, l: l.leap ? 1 : 0, d: l.d, text: CAL.lunarStr(l) } : null; }, to: function (f) { return CAL.lunarToJdn(f.y, f.m, !!f.l, f.d); }, note: 'GB/T 33661-2017 规则，1900–2100' },
      { id: 'isl', name: '伊斯兰历（算表）', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { var r = CAL.jdnToIsl(j); r.text = '希吉拉 ' + r.y + ' 年 ' + CAL.ISL_M[r.m - 1] + '月 ' + r.d + ' 日'; return r; }, to: function (f) { return CAL.islToJdn(f.y, f.m, f.d); }, note: '民用算表口径；观月历可差一天' },
      { id: 'heb', name: '希伯来历', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { var r = CAL.jdnToHeb(j); r.text = r.y + ' 年 ' + CAL.HEB_M[r.m - 1] + '月 ' + r.d + ' 日（月序 1 = 尼散）'; return r; }, to: function (f) { return CAL.hebToJdn(f.y, f.m, f.d); }, note: '固定算法（通行说法 359 年定）；一日从日落起' },
      { id: 'per', name: '伊朗太阳历', fields: [['y', '年'], ['m', '月'], ['d', '日']], from: function (j) { var r = CAL.jdnToPer(j); r.text = r.y + ' 年 ' + CAL.PER_M[r.m - 1] + '月 ' + r.d + ' 日'; return r; }, to: function (f) { return CAL.perToJdn(f.y, f.m, f.d); }, note: '春分起年；33 年周期规则' },
      { id: 'maya', name: '玛雅长纪历', fields: [['b', 'baktun'], ['k', 'katun'], ['t', 'tun'], ['w', 'winal'], ['n', 'kin']], from: function (j) { var m = CAL.jdnToMaya(j), tz = CAL.jdnToTzolkin(j), h = CAL.jdnToHaab(j); return { b: m[0], k: m[1], t: m[2], w: m[3], n: m[4], text: m.join('.') + ' · ' + tz.n + ' ' + tz.name + ' ' + h.d + ' ' + CAL.HAAB_M[h.m] }; }, to: function (f) { return CAL.mayaToJdn(f.b, f.k, f.t, f.w, f.n); }, note: 'GMT 相关常数 584283；13.0.0.0.0 = 2012-12-21' },
    ];
    function render(j) {
      var g = CAL.jdnToGreg(j), wd = CAL.weekday(j), lunar = CAL.jdnToLunar(j);
      date.value = gdate(g.y, g.m, g.d);
      var html = '<div class="cvcard main"><div class="cvh">公历 · 星期' + WD[wd] + '</div><div class="cvbig">' + gdate(g.y, g.m, g.d) + '</div><div class="cvs">干支纪日 ' + CAL.ganzhiDay(j) + (lunar ? ' · ' + CAL.ganzhiYear(lunar.y) + '年' : '') + '</div></div>';
      systems.forEach(function (s) {
        var f = s.from(j);
        html += '<div class="cvcard" data-sys="' + s.id + '"><div class="cvh">' + esc(s.name) + '</div><div class="cvbig">' + (f ? esc(f.text || (f.j != null ? num(f.j) : f.y + '-' + pad(f.m) + '-' + pad(f.d))) : '超出月表范围') + '</div><div class="cvf">'
          + s.fields.map(function (fd) { return '<label>' + esc(fd[1]) + '<input type="number" data-f="' + fd[0] + '" value="' + (f ? f[fd[0]] : '') + '"></label>'; }).join('') + '<button type="button" class="cvgo">按此反推</button></div><div class="cvs">' + esc(s.note) + '</div></div>';
      });
      grid.innerHTML = html;
    }
    grid.addEventListener('click', function (ev) {
      var b = ev.target.closest('.cvgo'); if (!b) return; var card = b.closest('.cvcard'), s = systems.filter(function (x) { return x.id === card.getAttribute('data-sys'); })[0], f = {};
      $$('input[data-f]', card).forEach(function (i) { f[i.getAttribute('data-f')] = parseInt(i.value, 10); });
      try { var j = s.to(f); if (j && isFinite(j)) render(Math.round(j)); } catch (e) {}
    });
    date.addEventListener('change', function () { var p = date.value.split('-').map(Number); if (p.length === 3 && p[0]) render(CAL.gregToJdn(p[0], p[1], p[2])); });
    $('#cv-today').addEventListener('click', function () { var t = new Date(); render(CAL.gregToJdn(t.getFullYear(), t.getMonth() + 1, t.getDate())); });
    render(CAL.gregToJdn(2026, 10, 24));
  })();

  /* ---------- 工具 3 拨表换算 */
  (function () {
    var root = $('.tdst'); if (!root) return;
    var A = $('#ds-a'), B = $('#ds-b'), date = $('#ds-date'), row = $('#ds-row');
    var nth = function (y, m, wd, n) { var j = CAL.gregToJdn(y, m, 1), w = CAL.weekday(j), d = 1 + ((wd - w + 7) % 7) + (n - 1) * 7; return CAL.gregToJdn(y, m, d); };
    var last = function (y, m, wd) { var ml = [31, CAL.isGregLeap(y) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1], j = CAL.gregToJdn(y, m, ml), w = CAL.weekday(j); return j - ((w - wd + 7) % 7); };
    var RULES = { // 返回 [start JDN, end JDN]（含 start，不含 end；南半球跨年用 (start>end) 表示）
      eu: function (y) { return [last(y, 3, 0), last(y, 10, 0)]; }, us: function (y) { return [nth(y, 3, 0, 2), nth(y, 11, 0, 1)]; },
      au: function (y) { return [nth(y, 10, 0, 1), nth(y, 4, 0, 1)]; }, nz: function (y) { return [last(y, 9, 0), nth(y, 4, 0, 1)]; },
      cl: function (y) { var s = nth(y, 9, 0, 1); if (CAL.jdnToGreg(s).d < 2) s += 7; var e = nth(y, 4, 0, 1); if (CAL.jdnToGreg(e).d < 2) e += 7; return [s, e]; },
      eg: function (y) { return [last(y, 4, 5), last(y, 10, 4)]; }, none: null };
    function inDst(c, j) { var r = RULES[c.r]; if (!r) return false; var y = CAL.jdnToGreg(j).y, se = r(y); if (se[0] < se[1]) return j >= se[0] && j < se[1]; return j >= se[0] || j < se[1]; }
    function status(c, j) { var r = RULES[c.r]; if (!r) return c.note || '全年 UTC' + (c.o >= 0 ? '+' : '') + c.o + '，不换时'; var y = CAL.jdnToGreg(j).y, se = r(y), on = inDst(c, j); return (on ? '夏令时中 UTC' : '标准时 UTC') + (function (v) { return (v >= 0 ? '+' : '−') + num(Math.abs(v), 2); })(c.o + (on ? 1 : 0)) + '；' + (se[0] < se[1] ? '夏令时 ' + fromJdn(se[0]) + ' → ' + fromJdn(se[1]) : '夏令时 ' + fromJdn(se[0]) + ' 起、到 ' + fromJdn(se[1]) + ' 止（跨年）'); }
    function draw() {
      var a = D.dstCities[A.value], b = D.dstCities[B.value], p = (date.value || '2026-10-24').split('-').map(Number), j = CAL.gregToJdn(p[0], p[1], p[2]);
      var oa = a.o + (inDst(a, j) ? 1 : 0), ob = b.o + (inDst(b, j) ? 1 : 0), diff = ob - oa;
      row.innerHTML = [[a, oa], [b, ob]].map(function (x) { return '<div class="dsc"><b>' + esc(x[0].n) + '</b>' + dialSvg(720 + x[1] * 60, 72) + '<span>' + hhmm(720 + x[1] * 60) + '</span><small>UTC 12:00 时</small></div>'; }).join('<div class="dsarrow">' + (diff === 0 ? '同时' : (diff > 0 ? '快 ' : '慢 ') + num(Math.abs(diff), 2) + ' 小时') + '</div>');
      set('ds-diff', (diff === 0 ? '0' : (diff > 0 ? '+' : '−') + num(Math.abs(diff), 2)) + ' 小时'); set('ds-a-st', status(a, j)); set('ds-b-st', status(b, j));
      $('#ds-note').textContent = '规则：欧盟 / 英国 3 月与 10 月最后一个周日 01:00 UTC；美国 / 加拿大 3 月第二个周日至 11 月第一个周日当地 02:00；澳大利亚东南各州 10 月第一个周日至 4 月第一个周日；新西兰 9 月最后一个周日至 4 月第一个周日；智利 9 月与 4 月第一个在 2 日或之后的周日；埃及 4 月最后一个周五至 10 月最后一个周四（2023 起）。墨西哥 2022 年、中国 1992 年、日本 1952 年起不实行。只按日期判断，不计换时当天的具体时刻。';
    }
    [A, B, date].forEach(function (i) { i.addEventListener('input', draw); i.addEventListener('change', draw); });
    B.selectedIndex = 1; draw();
  })();

  /* ---------- 工具 4 闰秒年表 */
  (function () {
    var root = $('.tleap'); if (!root) return;
    var yin = $('#ls-y'), bar = $('#ls-bar'), list = $('#ls-list'), proj = $('#ls-proj');
    function draw() {
      var by = parseInt(yin.value, 10) || 1985, mine = D.leaps.filter(function (s) { return parseInt(s.slice(0, 4), 10) >= by; });
      $('#ls-sum').textContent = by < 1972 ? '你出生时还没有闰秒；1972 年以来的 27 次你全经历了。' : by > 2016 ? '你出生后一次闰秒也没有插过——而且以后也不会有了。' : '你经历过 ' + mine.length + ' 次闰秒，第一次是 ' + mine[0] + '，最后一次 2016-12-31。';
      bar.innerHTML = '<div class="axis">' + [1972, 1980, 1990, 2000, 2010, 2020, 2027].map(function (y) { return '<span style="left:' + ((y - 1972) / 58 * 100) + '%">' + y + '</span>'; }).join('') + '</div>'
        + D.leaps.map(function (s) { var y = parseInt(s.slice(0, 4), 10) + (s.slice(5) === '06-30' ? .5 : 1); return '<i style="left:' + ((y - 1972) / 58 * 100) + '%" class="' + (y >= by ? 'me' : '') + '" title="' + s + '"></i>'; }).join('')
        + '<em style="left:' + ((2027.38 - 1972) / 58 * 100) + '%">2027-05-20 起不再插</em>' + (by >= 1972 && by <= 2027 ? '<u style="left:' + ((by - 1972) / 58 * 100) + '%">' + by + ' 出生</u>' : '');
      list.innerHTML = D.leaps.map(function (s, i) { return '<li' + (parseInt(s.slice(0, 4), 10) >= by ? ' class="me"' : '') + '><span>' + (i + 1) + '</span>' + s + '</li>'; }).join('');
      // 2027 后 UT1−UTC 的示意漂移：按 1972–2016 平均速率（约 0.6 s/年）与 2016–2025 的近零速率两条线；纵轴 1 格 = 10 秒
      var X = function (y) { return 40 + (y - 2016) / 84 * 540; }, Y = function (v) { return 14 - v * 1.0; };
      var d1 = 'M' + X(2016) + ' ' + Y(0) + ' L' + X(2027.4) + ' ' + Y(0) + ' L' + X(2100) + ' ' + Y(-(2100 - 2027.4) * 0.6), d2 = 'M' + X(2027.4) + ' ' + Y(0) + ' L' + X(2100) + ' ' + Y(-(2100 - 2027.4) * 0.1);
      proj.innerHTML = [0, -20, -40].map(function (v) { return '<line class="' + (v ? 'ln2' : 'ln') + '" x1="40" y1="' + Y(v) + '" x2="580" y2="' + Y(v) + '"/><text class="dt" x="36" y="' + (Y(v) + 4) + '" text-anchor="end">' + v + ' s</text>'; }).join('') + '<path class="o2 d" d="' + d1 + '"/><path class="o2" d="' + d2 + '"/>'
        + '<text class="dt" x="' + X(2027.4) + '" y="10">2027-05-20</text><line class="a" x1="' + X(2027.4) + '" y1="12" x2="' + X(2027.4) + '" y2="' + Y(-44) + '"/><text class="dt" x="40" y="112">UT1 − UTC 示意：虚线 0.6 s / 年（1972–2016 均速），实线 0.1 s / 年（2016–2025）</text><text class="dt" x="580" y="' + (Y(0) - 4) + '" text-anchor="end">2100</text>';
    }
    yin.addEventListener('input', draw); draw();
  })();
})();
