/* 历法算法（浏览器端）。公历 / 儒略历 / 儒略日数 / 伊斯兰算表历 / 希伯来历 / 伊朗太阳历 / 玛雅长纪历 按 Reingold & Dershowitz《Calendrical Calculations》的算术公式实现；
   农历不现场算天文，用 PyEphem 预算的 1900–2100 月表（src/tools/lunar_table.py，GB/T 33661-2017 规则：UTC+8 日界、冬至所在月为十一月、无中气置闰）。 */
var CAL = (function () {
  'use strict';
  var floor = Math.floor, mod = function (a, b) { return a - b * floor(a / b); };
  // ---- 公历 / 儒略历 <-> JDN（当天正午的整数 JDN）
  function gregToJdn(y, m, d) { var a = floor((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3; return d + floor((153 * mm + 2) / 5) + 365 * yy + floor(yy / 4) - floor(yy / 100) + floor(yy / 400) - 32045; }
  function jdnToGreg(j) { var a = j + 32044, b = floor((4 * a + 3) / 146097), c = a - floor(146097 * b / 4), d = floor((4 * c + 3) / 1461), e = c - floor(1461 * d / 4), m = floor((5 * e + 2) / 153); return { y: 100 * b + d - 4800 + floor(m / 10), m: m + 3 - 12 * floor(m / 10), d: e - floor((153 * m + 2) / 5) + 1 }; }
  function julToJdn(y, m, d) { var a = floor((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3; return d + floor((153 * mm + 2) / 5) + 365 * yy + floor(yy / 4) - 32083; }
  function jdnToJul(j) { var c = j + 32082, d = floor((4 * c + 3) / 1461), e = c - floor(1461 * d / 4), m = floor((5 * e + 2) / 153); return { y: d - 4800 + floor(m / 10), m: m + 3 - 12 * floor(m / 10), d: e - floor((153 * m + 2) / 5) + 1 }; }
  function weekday(j) { return mod(j + 1, 7); } // 0 = 周日
  function isGregLeap(y) { return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0; }
  // ---- 伊斯兰算表历（民用口径：闰年 2,5,7,10,13,16,18,21,24,26,29；纪元 JDN 1948440 = 622-07-16 儒略）
  var ISL_EPOCH = 1948440;
  function islToJdn(y, m, d) { return d + Math.ceil(29.5 * (m - 1)) + (y - 1) * 354 + floor((3 + 11 * y) / 30) + ISL_EPOCH - 1; }
  function jdnToIsl(j) { var y = floor((30 * (j - ISL_EPOCH) + 10646) / 10631); var m = Math.min(12, Math.ceil((j - (29 + islToJdn(y, 1, 1))) / 29.5) + 1); var d = j - islToJdn(y, m, 1) + 1; return { y: y, m: m, d: d }; }
  var ISL_M = ['穆哈兰姆', '色法尔', '赖比尔·敖外鲁', '赖比尔·阿色尼', '主马达·敖外鲁', '主马达·阿色尼', '赖哲卜', '舍尔邦', '赖买丹（斋月）', '闪瓦鲁', '都尔喀尔德', '都尔黑哲'];
  // ---- 希伯来历（Dershowitz–Reingold；纪元 JDN 347998 = 公元前 3761-10-07 儒略）
  var HEB_EPOCH = 347998;
  function hebLeap(y) { return mod(7 * y + 1, 19) < 7; }
  function hebElapsedDays(y) {
    var months = floor((235 * y - 234) / 19), parts = 12084 + 13753 * months, day = months * 29 + floor(parts / 25920);
    if (mod(3 * (day + 1), 7) < 3) day += 1;
    return day;
  }
  function hebNewYearDelay(y) { var ny0 = hebElapsedDays(y - 1), ny1 = hebElapsedDays(y), ny2 = hebElapsedDays(y + 1); if (ny2 - ny1 === 356) return 2; return (ny1 - ny0 === 382) ? 1 : 0; }
  function hebNewYear(y) { return HEB_EPOCH + hebElapsedDays(y) + hebNewYearDelay(y); }
  function hebYearDays(y) { return hebNewYear(y + 1) - hebNewYear(y); }
  function hebMonthsInYear(y) { return hebLeap(y) ? 13 : 12; }
  function hebMonthDays(y, m) { // m: 1=尼散 … 7=提斯利 … 12=亚达，13=亚达二
    if (m === 2 || m === 4 || m === 6 || m === 10 || m === 13) return 29;
    if (m === 12 && !hebLeap(y)) return 29;
    if (m === 8 && !(mod(hebYearDays(y), 10) === 5)) return 29;
    if (m === 9 && mod(hebYearDays(y), 10) === 3) return 29;
    return 30;
  }
  function hebToJdn(y, m, d) {
    var j = hebNewYear(y) + d - 1, k;
    if (m < 7) { for (k = 7; k <= hebMonthsInYear(y); k++) j += hebMonthDays(y, k); for (k = 1; k < m; k++) j += hebMonthDays(y, k); }
    else { for (k = 7; k < m; k++) j += hebMonthDays(y, k); }
    return j;
  }
  function jdnToHeb(j) {
    var approx = floor((j - HEB_EPOCH) * 98496 / 35975351) + 1, y = approx - 1;
    while (hebNewYear(y + 1) <= j) y++;
    var start = j < hebToJdn(y, 1, 1) ? 7 : 1, m = start;
    while (j > hebToJdn(y, m, hebMonthDays(y, m))) m++;
    return { y: y, m: m, d: j - hebToJdn(y, m, 1) + 1 };
  }
  var HEB_M = ['尼散', '以珥', '西弯', '搭模斯', '埃波', '以禄', '提斯利', '玛西班', '基斯流', '提别', '细罢特', '亚达', '亚达二'];
  // ---- 伊朗太阳历（33 年周期算术规则：年号 mod 33 ∈ {1,5,9,13,17,22,26,30} 为闰年；与官方按天文春分定的历在 1300–1500 年区间一致，更远的年份可能差一天）
  var PER_EPOCH = 1948320, PER_LEAPS = { 1: 1, 5: 1, 9: 1, 13: 1, 17: 1, 22: 1, 26: 1, 30: 1 };
  function perLeap(y) { return !!PER_LEAPS[mod(y, 33)]; }
  function perLeapsBefore(y) { var n = y - 1, c = floor(n / 33) * 8, r = mod(n, 33), k; for (k = 1; k <= r; k++) if (PER_LEAPS[k]) c++; return c; } // 1..y-1 里的闰年数
  function perToJdn(y, m, d) { return PER_EPOCH + 365 * (y - 1) + perLeapsBefore(y) + (m <= 7 ? (m - 1) * 31 : (m - 1) * 30 + 6) + d - 1; }
  function jdnToPer(j) { var y = floor((j - PER_EPOCH) / 365.2424) + 1; while (perToJdn(y + 1, 1, 1) <= j) y++; while (perToJdn(y, 1, 1) > j) y--; var yd = j - perToJdn(y, 1, 1) + 1, m = yd <= 186 ? Math.ceil(yd / 31) : Math.ceil((yd - 6) / 30), d = j - perToJdn(y, m, 1) + 1; return { y: y, m: m, d: d }; }
  var PER_M = ['法尔瓦丁', '奥尔迪贝赫什特', '霍尔达德', '提尔', '莫尔达德', '沙赫里瓦尔', '梅赫尔', '阿班', '阿扎尔', '代伊', '巴赫曼', '埃斯凡德'];
  // ---- 玛雅长纪历（GMT 相关常数 584283，通行说法；另说 584285）
  var MAYA_EPOCH = 584283;
  function jdnToMaya(j) { var d = j - MAYA_EPOCH, b = floor(d / 144000); d -= b * 144000; var k = floor(d / 7200); d -= k * 7200; var t = floor(d / 360); d -= t * 360; var w = floor(d / 20); return [b, k, t, w, d - w * 20]; }
  function mayaToJdn(b, k, t, w, kin) { return MAYA_EPOCH + b * 144000 + k * 7200 + t * 360 + w * 20 + kin; }
  // 哈布历与卓尔金历（按 0.0.0.0.0 = 4 Ahau 8 Cumku）
  var HAAB_M = ['Pop', 'Wo', 'Sip', 'Sotz', 'Sek', 'Xul', 'Yaxkin', 'Mol', 'Chen', 'Yax', 'Sak', 'Keh', 'Mak', 'Kankin', 'Muwan', 'Pax', 'Kayab', 'Kumku', 'Wayeb'];
  var TZ_N = ['Imix', 'Ik', 'Akbal', 'Kan', 'Chikchan', 'Kimi', 'Manik', 'Lamat', 'Muluk', 'Ok', 'Chuwen', 'Eb', 'Ben', 'Ix', 'Men', 'Kib', 'Kaban', 'Etznab', 'Kawak', 'Ajaw'];
  function jdnToHaab(j) { var c = mod(j - MAYA_EPOCH + 348, 365); return { d: mod(c, 20), m: floor(c / 20) }; } // 8 Kumku = 17*20+8 = 348
  function jdnToTzolkin(j) { var d = j - MAYA_EPOCH; return { n: mod(d + 4 - 1, 13) + 1, name: TZ_N[mod(d + 19, 20)] }; } // 4 Ahau
  // ---- 农历（预算表）
  var LUNAR = null; // 由页面注入 {"1900":[jdn,leap,bits],...}
  var CN_M = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'];
  var CN_D = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
  var GAN = '甲乙丙丁戊己庚辛壬癸', ZHI = '子丑寅卯辰巳午未申酉戌亥', SX = '鼠牛虎兔龙蛇马羊猴鸡狗猪';
  function lunarYearMonths(y) { // -> [{start, num, leap, len}]
    var r = LUNAR[String(y)]; if (!r) return null;
    var j = r[0], leap = r[1], bits = r[2], out = [], n = 1, k;
    for (k = 0; k < bits.length; k++) {
      var isLeap = leap && (k === leap); // 闰月排在第 leap 个月之后：序号 k == leap（0 基）时为闰月
      var len = bits.charAt(k) === '1' ? 30 : 29;
      out.push({ start: j, num: isLeap ? leap : n, leap: isLeap, len: len });
      if (!isLeap) n++;
      j += len;
    }
    return out;
  }
  function jdnToLunar(j) {
    if (!LUNAR) return null;
    var g = jdnToGreg(j), y = g.y, ms = lunarYearMonths(y);
    if (!ms || j < ms[0].start) { y--; ms = lunarYearMonths(y); if (!ms) return null; }
    for (var k = 0; k < ms.length; k++) { var m = ms[k]; if (j >= m.start && j < m.start + m.len) { return { y: y, m: m.num, leap: m.leap, d: j - m.start + 1, mlen: m.len }; } }
    return null;
  }
  function lunarToJdn(y, m, leap, d) { var ms = lunarYearMonths(y); if (!ms) return null; for (var k = 0; k < ms.length; k++) if (ms[k].num === m && !!ms[k].leap === !!leap) return ms[k].start + d - 1; return null; }
  function ganzhiYear(y) { var i = mod(y - 4, 60); return GAN.charAt(i % 10) + ZHI.charAt(i % 12); }
  function shengxiao(y) { return SX.charAt(mod(y - 4, 12)); }
  function ganzhiDay(j) { var i = mod(j + 49, 60); return GAN.charAt(i % 10) + ZHI.charAt(i % 12); } // JDN 2451545 (2000-01-01) = 戊午 → (2451545+49)%60=... 校准见下
  function lunarStr(l) { if (!l) return '超出 1900–2100 月表'; return ganzhiYear(l.y) + '年（' + shengxiao(l.y) + '）' + (l.leap ? '闰' : '') + CN_M[l.m - 1] + '月' + CN_D[l.d - 1]; }
  // ---- 均时差与太阳正午（NOAA 简化式，误差 < 1 分钟）
  function eot(dayOfYear, hourUTC) { var g = 2 * Math.PI / 365 * (dayOfYear - 1 + ((hourUTC || 12) - 12) / 24); return 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g)); }
  function decl(dayOfYear) { var g = 2 * Math.PI / 365 * (dayOfYear - 1); return 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g); }
  function solarNoonMin(lon, tzHours, dayOfYear) { return 720 - 4 * lon - eot(dayOfYear) + tzHours * 60; } // 当地钟表时间的分钟数
  function dayOfYear(y, m, d) { return gregToJdn(y, m, d) - gregToJdn(y, 1, 1) + 1; }
  return { gregToJdn: gregToJdn, jdnToGreg: jdnToGreg, julToJdn: julToJdn, jdnToJul: jdnToJul, weekday: weekday, isGregLeap: isGregLeap,
    islToJdn: islToJdn, jdnToIsl: jdnToIsl, ISL_M: ISL_M, hebToJdn: hebToJdn, jdnToHeb: jdnToHeb, HEB_M: HEB_M, hebLeap: hebLeap,
    perToJdn: perToJdn, jdnToPer: jdnToPer, perLeap: perLeap, PER_M: PER_M, jdnToMaya: jdnToMaya, mayaToJdn: mayaToJdn, jdnToHaab: jdnToHaab, jdnToTzolkin: jdnToTzolkin, HAAB_M: HAAB_M,
    setLunar: function (t) { LUNAR = t; }, jdnToLunar: jdnToLunar, lunarToJdn: lunarToJdn, lunarStr: lunarStr, lunarYearMonths: lunarYearMonths, ganzhiYear: ganzhiYear, shengxiao: shengxiao, ganzhiDay: ganzhiDay, CN_M: CN_M, CN_D: CN_D,
    eot: eot, decl: decl, solarNoonMin: solarNoonMin, dayOfYear: dayOfYear };
})();
