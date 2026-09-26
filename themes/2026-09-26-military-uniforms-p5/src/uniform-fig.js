/* uniform-fig.js — 零依赖军服示意图生成器（扁平插画风，正面站姿）
 * 用法：UniformFig.svg(params, { id:'uk1815', title:'英国 1815', plate:true, width, height }) -> SVG 字符串
 *       UniformFig.PRESETS[key] -> 预设参数
 * 坐标：viewBox 0 0 100 220；头顶 y≈19，脚底 y≈214，高帽可到 y=0。
 * 迷彩只画"类型示意"：带 seed 的 LCG 伪随机生成的通用图案，不复刻任何具体受保护图案。
 * 约定：camo.colors[0] 为底色，其余依次为叠加色（最后一色通常为最深色）。
 * 本文件不使用模块语法、不引用外部资源，可直接内联进页面。 */
(function (root) {
  'use strict';
  var INK = '#2a2a26', SKIN = '#e3c3a3', HAIR = '#2b2420', BRASS = '#c9a646', LEATHER = '#1d1b19';

  /* ---------- 工具 ---------- */
  function r1(n) { return Math.round(n * 10) / 10; }
  // 以 x=50 为轴镜像路径（路径只用绝对坐标 "x,y" 对）
  function mx(d) {
    return d.replace(/(-?\d*\.?\d+),(-?\d*\.?\d+)/g, function (m, x, y) { return r1(100 - x) + ',' + y; });
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function P(d, fill, x) { return '<path d="' + d + '" fill="' + (fill || 'none') + '"' + (x || '') + '/>'; }
  function PP(d, fill, x) { return P(d, fill, x) + P(mx(d), fill, x); }           // 左右成对
  function line(d, col, w, x) { return '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="' + w + '"' + (x || '') + '/>'; }
  function circ(cx, cy, r, fill, x) { return '<circle cx="' + r1(cx) + '" cy="' + r1(cy) + '" r="' + r + '" fill="' + fill + '"' + (x || '') + '/>'; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function hex2rgb(h) {
    h = String(h).replace('#', '');
    if (h.length === 3) h = h.replace(/./g, '$&$&');
    var n = parseInt(h.slice(0, 6), 16);
    return [n >> 16 & 255, n >> 8 & 255, n & 255];
  }
  // k<0 变暗，k>0 变亮（-1..1）
  function shade(h, k) {
    if (!h || h.charAt(0) !== '#') return h;
    var c = hex2rgb(h), t = k < 0 ? 0 : 255, a = Math.abs(k);
    return '#' + c.map(function (v) { var x = Math.round(v + (t - v) * a); return (x < 16 ? '0' : '') + x.toString(16); }).join('');
  }
  function lum(h) { var c = hex2rgb(h); return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255; }
  function rng(seed) {
    var s = (seed >>> 0) || 1;
    return function () { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  }
  function star(cx, cy, r) {
    var d = '';
    for (var i = 0; i < 10; i++) {
      var a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.42 : r;
      d += (i ? 'L' : 'M') + r1(cx + rr * Math.cos(a)) + ',' + r1(cy + rr * Math.sin(a));
    }
    return d + 'Z';
  }
  // 平滑有机斑块（二次贝塞尔中点法）
  function blob(R, cx, cy, rx, ry, n) {
    var pts = [], i;
    for (i = 0; i < n; i++) {
      var a = i / n * 2 * Math.PI + R() * 0.5, k = 0.62 + R() * 0.55;
      pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
    }
    function mid(p, q) { return r1((p[0] + q[0]) / 2) + ',' + r1((p[1] + q[1]) / 2); }
    var d = 'M' + mid(pts[n - 1], pts[0]);
    for (i = 0; i < n; i++) d += 'Q' + r1(pts[i][0]) + ',' + r1(pts[i][1]) + ' ' + mid(pts[i], pts[(i + 1) % n]);
    return d + 'Z';
  }
  // 让越过图块边界的形状在对侧重复一次 → 无缝拼接
  function wrap(s, x0, y0, x1, y1, W) {
    var out = s, dxs = [0], dys = [0];
    if (x1 > W) dxs.push(-W); if (x0 < 0) dxs.push(W);
    if (y1 > W) dys.push(-W); if (y0 < 0) dys.push(W);
    dxs.forEach(function (dx) {
      dys.forEach(function (dy) { if (dx || dy) out += '<g transform="translate(' + dx + ',' + dy + ')">' + s + '</g>'; });
    });
    return out;
  }

  /* ---------- 迷彩（通用类型示意） ---------- */
  var CAMO_TILE = { brush: 26, lizard: 24, tiger: 26, woodland: 30, flora: 24, digital: 24, multi: 26, splinter: 26 };
  var CAMO = {
    // 刷痕：不规则长条笔触
    brush: function (R, c, W) {
      var s = '';
      for (var ci = 1; ci < c.length; ci++) {
        var last = ci === c.length - 1 && c.length > 3, n = last ? 4 : 6;
        for (var i = 0; i < n; i++) {
          var x = R() * W, y = R() * W, a = -1.7 + R() * 1.9, L = 7 + R() * 8, w = last ? 1.1 + R() * 0.8 : 1.9 + R() * 1.9;
          var ex = x + Math.cos(a) * L, ey = y + Math.sin(a) * L;
          var qx = (x + ex) / 2 + (R() - 0.5) * 4, qy = (y + ey) / 2 + (R() - 0.5) * 4;
          var d = 'M' + r1(x) + ',' + r1(y) + 'Q' + r1(qx) + ',' + r1(qy) + ' ' + r1(ex) + ',' + r1(ey);
          s += wrap(line(d, c[ci], r1(w), ' stroke-linecap="round"'),
            Math.min(x, ex) - 3, Math.min(y, ey) - 3, Math.max(x, ex) + 3, Math.max(y, ey) + 3, W);
        }
      }
      return s;
    },
    // 蜥蜴：水平断续短条
    lizard: function (R, c, W) {
      var s = '', rows = 11;
      for (var r = 0; r < rows; r++) {
        var y = r * W / rows + R() * 0.5, x = R() * 3;
        while (x < W) {
          var len = 2 + R() * 4.5, ci = 1 + Math.floor(R() * (c.length - 1)), h = 0.8 + R() * 0.5;
          if (R() < 0.6) s += wrap('<rect x="' + r1(x) + '" y="' + r1(y) + '" width="' + r1(len) + '" height="' + r1(h) + '" fill="' + c[ci] + '"/>', x, y, x + len, y + h, W);
          x += len + 0.8 + R() * 2.6;
        }
      }
      return s;
    },
    // 虎斑：水平粗锯齿条
    tiger: function (R, c, W) {
      var s = '';
      for (var ci = 1; ci < c.length; ci++) {
        var last = ci === c.length - 1;
        for (var b = 0; b < 3; b++) {
          var y = (b + 0.2 + R() * 0.6) * W / 3, x0 = R() * W, L = W * (0.55 + R() * 0.4), th = last ? 2.6 + R() * 1.2 : 1.8 + R() * 1.2;
          var n = 7, top = [], bot = [];
          for (var i = 0; i <= n; i++) {
            var x = x0 + L * i / n, t = (i === 0 || i === n) ? 0 : 1;
            top.push(r1(x) + ',' + r1(y - (th / 2 + (R() - 0.3) * 1.5) * t));
            bot.push(r1(x + (R() - 0.5) * 1.5) + ',' + r1(y + (th / 2 + (R() - 0.3) * 1.5) * t));
          }
          s += wrap(P('M' + top.join('L') + 'L' + bot.reverse().join('L') + 'Z', c[ci]), x0 - 1, y - th * 1.5, x0 + L + 1, y + th * 1.5, W);
        }
      }
      return s;
    },
    // 林地大斑块：圆润有机形
    woodland: function (R, c, W) {
      var s = '';
      for (var ci = 1; ci < c.length; ci++) {
        var k = Math.min(ci, 3), n = [0, 5, 5, 5][k], rad = [0, 6.2, 4.4, 2.1][k];
        for (var i = 0; i < n; i++) {
          var x = R() * W, y = R() * W, rx = rad * (1.1 + R() * 0.6) * (k === 3 ? 1.6 : 1), ry = rad * (0.65 + R() * 0.35);
          s += wrap(P(blob(R, x, y, rx, ry, 7), c[ci]), x - rx, y - ry, x + rx, y + ry, W);
        }
      }
      return s;
    },
    // Flora 类：竖向波浪条
    flora: function (R, c, W) {
      var s = '';
      for (var ci = 1; ci < c.length; ci++) {
        for (var b = 0; b < 3; b++) {
          var x0 = R() * W, w = 2.2 + R() * 2.6, A = 0.8 + R() * 1.2, ph = R() * 6.28, k = 2 * Math.PI * (1 + Math.floor(R() * 2)) / W;
          var L = [], Rr = [];
          for (var i = 0; i <= 12; i++) {
            var y = W * i / 12, x = x0 + A * Math.sin(k * y + ph), ww = w * (0.75 + 0.25 * Math.sin(2 * k * y + ph));
            L.push(r1(x - ww / 2) + ',' + r1(y)); Rr.push(r1(x + ww / 2) + ',' + r1(y));
          }
          s += wrap(P('M' + L.join('L') + 'L' + Rr.reverse().join('L') + 'Z', c[ci]), x0 - A - w, 0, x0 + A + w, W, W);
        }
      }
      return s;
    },
    // 数码像素：随机游走聚簇（模运算，天然无缝）
    digital: function (R, c, W) {
      var cs = 2, N = Math.round(W / cs), g = [], i, j, s = '';
      for (i = 0; i < N * N; i++) g[i] = 0;
      function set(x, y, v) { g[((y % N + N) % N) * N + ((x % N + N) % N)] = v; }
      for (var ci = 1; ci < c.length; ci++) {
        var clusters = ci === c.length - 1 && c.length > 3 ? 4 : 5;
        for (var k = 0; k < clusters; k++) {
          var x = Math.floor(R() * N), y = Math.floor(R() * N), steps = 9 + Math.floor(R() * 10);
          for (var t = 0; t < steps; t++) {
            set(x, y, ci);
            if (R() < 0.5) set(x + 1, y, ci);
            var dir = Math.floor(R() * 4);
            x += dir === 0 ? 1 : dir === 1 ? -1 : 0; y += dir === 2 ? 1 : dir === 3 ? -1 : 0;
          }
        }
      }
      for (j = 0; j < N; j++) for (i = 0; i < N;) {
        var v = g[j * N + i], e = i;
        while (e < N && g[j * N + e] === v) e++;
        if (v) s += '<rect x="' + i * cs + '" y="' + j * cs + '" width="' + (e - i) * cs + '" height="' + cs + '" fill="' + c[v] + '"/>';
        i = e;
      }
      return '<g shape-rendering="crispEdges">' + s + '</g>';
    },
    // 多地形：柔边小斑块层叠（半透明外圈模拟模糊边缘）
    multi: function (R, c, W) {
      var s = '';
      for (var ci = 1; ci < c.length; ci++) {
        var k = Math.min(ci, 3), n = [0, 6, 6, 6][k], rad = [0, 4, 2.9, 1.5][k];
        for (var i = 0; i < n; i++) {
          var x = R() * W, y = R() * W, rx = rad * (0.7 + R() * 0.5), ry = rad * (0.9 + R() * 0.6);
          var inner = P(blob(R, x, y, rx * 1.4, ry * 1.4, 6), c[ci], ' opacity=".35"') + P(blob(R, x, y, rx, ry, 6), c[ci], ' opacity=".85"');
          s += wrap(inner, x - rx * 1.7, y - ry * 1.7, x + rx * 1.7, y + ry * 1.7, W);
        }
      }
      return s;
    },
    // 碎片几何
    splinter: function (R, c, W) {
      var s = '';
      for (var ci = 1; ci < c.length; ci++) for (var i = 0; i < 5; i++) {
        var x = R() * W, y = R() * W, pts = [], n = 3 + Math.floor(R() * 2), rad = 3 + R() * 4;
        for (var k = 0; k < n; k++) {
          var a = k / n * 6.283 + R() * 0.8;
          pts.push(r1(x + Math.cos(a) * rad * (0.7 + R() * 0.8)) + ',' + r1(y + Math.sin(a) * rad * 0.7));
        }
        s += wrap(P('M' + pts.join('L') + 'Z', c[ci]), x - rad * 1.6, y - rad, x + rad * 1.6, y + rad, W);
      }
      return s;
    }
  };

  function drawCamoDefs(id, camo) {
    var c = camo.colors && camo.colors.length > 1 ? camo.colors : ['#8b8a66', '#5b6b3a', '#4d3b2a', '#1e1e1a'];
    var type = CAMO[camo.type] ? camo.type : 'woodland', W = CAMO_TILE[type], sc = camo.scale || 1;
    var R = rng((camo.seed || 1) * 7919 + type.length * 131);
    return '<pattern id="' + id + '-camo" patternUnits="userSpaceOnUse" width="' + W + '" height="' + W + '"' +
      (sc !== 1 ? ' patternTransform="scale(' + sc + ')"' : '') + '>' +
      '<rect width="' + W + '" height="' + W + '" fill="' + c[0] + '"/>' + CAMO[type](R, c, W) + '</pattern>';
  }

  function ell(cx, cy, rx, ry, fill, x) {
    return '<ellipse cx="' + r1(cx) + '" cy="' + r1(cy) + '" rx="' + rx + '" ry="' + ry + '" fill="' + fill + '"' + (x || '') + '/>';
  }
  // 成对圆点（左 + 镜像）
  function dots2(pts, r, fill, x) {
    var s = '';
    pts.forEach(function (q) { s += circ(q[0], q[1], r, fill, x) + circ(100 - q[0], q[1], r, fill, x); });
    return s;
  }

  /* ---------- 腿 / 裤 / 鞋 ---------- */
  var SHOE = 'M39.4,203.5L48.2,203.5L48.9,211Q49,214 46.4,214L38.6,214Q35.4,214 36.2,211Q37.2,208.6 39.4,206.5Z';
  var LEG_STRAIGHT = 'M50.3,93L37.2,93L36.5,112L37.9,160L38.9,207.2L48.6,207.2L49,160L50.3,119Z';

  function shoes(col, sole) {
    return PP(SHOE, col) + (sole ? PP('M36,211.8L49,211.8L48.9,213.2Q48.6,214 46.4,214L38.6,214Q35.6,214 36,211.8Z', sole) :
      PP('M36.4,212.3L48.9,212.3', 'none', ' stroke-width=".45"'));
  }
  function stripe(C, yEnd) {
    var pts = [[38.4, 97], [37.7, 112], [39.1, 160], [40.1, 206]], d = '';
    for (var i = 0; i < pts.length; i++) {
      var q = pts[i];
      if (q[1] > yEnd) { var a = pts[i - 1], t = (yEnd - a[1]) / (q[1] - a[1]); d += 'L' + r1(lerp(a[0], q[0], t)) + ',' + yEnd; break; }
      d += (i ? 'L' : 'M') + q[0] + ',' + q[1];
    }
    var w = C.tr.stripeWidth || 1.3;
    return line(d, C.tr.stripe, w) + line(mx(d), C.tr.stripe, w);
  }
  function lacing(y0, y1, col) { // 现代靴鞋带
    var d = '';
    for (var y = y0; y < y1; y += 3) d += 'M42.6,' + r1(y) + 'L46,' + r1(y);
    return PP(d, 'none', ' stroke="' + col + '" stroke-width=".5"');
  }

  function drawTrousers(C) {
    var p = C.p, st = C.tr.style, f = C.trFill, foot = p.footwear || LEATHER, o = '', stripeEnd = 206, gT, y, b;
    if (C.cut === 'qing') { // 长袍遮腿，只露布靴
      return PP('M39.4,178L48.6,178L48.4,205L48.9,211L36.3,211L39.6,205Z', foot) + shoes(foot, '#efeee8');
    }
    if (st === 'breeches-gaiters') {
      gT = p.gaiterTop || 156; stripeEnd = gT;
      var gcol = p.gaiters || '#f2efe6';
      o += PP('M50.3,93L37.2,93L36.4,112L37.8,150L38.6,166L48.4,166L48.8,150L50.3,119Z', f);
      o += PP('M38.6,163Q37.4,178 40.2,204L47.6,204Q48.8,180 48.4,163Z', p.stockings || '#f2efe6');
      o += shoes(foot, p.sole);
      o += PP('M37.6,' + gT + 'L48.9,' + gT + 'L48.6,170Q48.9,186 47.9,203L49.2,209.6Q44,211.4 38.1,209.6L40,203Q36.9,182 37.8,168Z', gcol);
      b = [];
      for (y = gT + 6; y < 203; y += 5.5) b.push([lerp(38.9, 40.7, (y - gT) / (203 - gT)), y]);
      o += dots2(b, 0.55, shade(gcol, lum(gcol) > 0.5 ? -0.4 : 0.35), ' stroke="none"');
      o += PP('M37.7,' + (gT + 2.6) + 'L48.8,' + (gT + 2.6), 'none', ' stroke-width=".7"');
    } else if (st === 'puttees') {
      stripeEnd = 150;
      var pc = p.puttees || shade(C.tr.color, -0.08);
      o += PP('M50.3,93L37.2,93L36.4,112L36.9,150Q36.6,160 38.5,165L48.5,165Q49.5,158 49,150L50.3,119Z', f);
      o += shoes(foot, p.sole);
      o += PP('M38.3,161L48.5,161L47.7,204L40.1,204Q37.9,182 38.3,161Z', pc);
      var d = '';
      for (y = 165; y < 203; y += 3.6) d += 'M' + r1(lerp(38.3, 40, (y - 161) / 43)) + ',' + r1(y) + 'L' + r1(lerp(48.5, 47.7, (y - 163) / 43)) + ',' + r1(y - 2.2);
      o += PP(d, 'none', ' stroke-width=".45" stroke-opacity=".7"');
    } else if (st === 'boots') {
      stripeEnd = 154;
      o += C.tr.flare ? PP('M50.3,93L37.2,93L35.6,108Q31.4,128 36.2,146L38,158L48.6,158L49,146L50.3,119Z', f)
        : PP('M50.3,93L37.2,93L36.5,112L38,158L48.6,158L49,146L50.3,119Z', f);
      o += PP('M37.5,154L49.3,154L48.5,180L48.3,205L40.2,205L39.1,180Z', foot) + shoes(foot, p.sole);
      o += PP('M41.2,159L41.7,201', 'none', ' stroke="#fff" stroke-opacity=".18" stroke-width="1.2"');
    } else if (st === 'bloused') {
      stripeEnd = 182;
      o += PP('M39.2,182L48.6,182L48.2,205L40.2,205Z', foot) + shoes(foot, p.sole) + lacing(186, 203, shade(foot, 0.3));
      o += PP('M50.3,93L37.2,93L36.5,112L37.9,160L38.3,178Q36.6,184 38.7,187.6L48.6,187.6Q50.2,184 48.9,178L49,160L50.3,119Z', f);
    } else if (st === 'anklets' || st === 'leggings') {
      gT = p.gaiterTop || (st === 'leggings' ? 170 : 190); stripeEnd = gT;
      var ac = p.gaiters || (st === 'leggings' ? LEATHER : '#8a7f5a');
      o += shoes(foot, p.sole) + PP(LEG_STRAIGHT, f);
      o += PP('M38.5,' + gT + 'L49,' + gT + 'L48.9,208.2Q44,209.6 38.9,208.2Z', ac);
      o += PP('M38.6,' + (gT + 4) + 'L49,' + (gT + 4) + 'M38.8,' + (gT + 10) + 'L49,' + (gT + 10), 'none', ' stroke="' + shade(ac, -0.35) + '" stroke-width=".8"');
    } else { // 'trousers'
      o += shoes(foot, p.sole) + PP(LEG_STRAIGHT, f);
    }
    // 膝部褶线
    if (st !== 'breeches-gaiters') o += PP('M40.5,150Q43.5,152 46.5,150', 'none', ' stroke-width=".4" stroke-opacity=".45"');
    if (C.tr.stripe) o += stripe(C, stripeEnd);
    return o;
  }

  /* ---------- 手臂 / 手 ---------- */
  function armPath(o, sw) {
    return 'M34.6,47.4Q' + r1(29.6 - sw) + ',48.2 ' + r1(28.3 - sw) + ',55L' + r1(25.9 - o / 2 - sw) + ',92L' + r1(26.4 - o - sw) +
      ',124L' + r1(32.9 - o) + ',124L' + r1(33.7 - o / 2) + ',92L35.9,60Z';
  }
  // 袖口 / 袖上色带：top..bot 之间（y>=92）
  function cuffPath(o, sw, top, bot, g) {
    g = g || 0;
    var t0 = (top - 92) / 32, t1 = (bot - 92) / 32;
    function ox(t) { return r1(lerp(25.9 - o / 2 - sw, 26.4 - o - sw, t) - g); }
    function ix(t) { return r1(lerp(33.7 - o / 2, 32.9 - o, t) + g); }
    return 'M' + ox(t0) + ',' + top + 'L' + ox(t1) + ',' + bot + 'L' + ix(t1) + ',' + bot + 'L' + ix(t0) + ',' + top + 'Z';
  }
  function drawArms(C) {
    var p = C.p, sw = C.sleeveW, oL = C.armOut, s = '', fill = C.coatFill;
    s += P(armPath(oL, sw), fill) + P(mx(armPath(0, sw)), fill);
    // 肘部褶线
    s += line('M' + r1(28.6 - oL / 2 - sw / 2) + ',94Q' + r1(30.4 - oL / 2) + ',95.6 ' + r1(32.6 - oL / 2) + ',94.2', INK, 0.4, ' stroke-opacity=".4"');
    s += line(mx('M' + r1(28.6 - sw / 2) + ',94Q30.4,95.6 32.6,94.2'), INK, 0.4, ' stroke-opacity=".4"');
    var cf = p.cuffs, cut = C.cut;
    if (cut === 'justaucorps') {
      cf = cf || C.coatColor;
      s += P(cuffPath(oL, sw, 104, 124, 0.9), cf) + P(mx(cuffPath(0, sw, 104, 124, 0.9)), cf);
      var bc = C.btn.color;
      [107.5, 112, 116.5].forEach(function (y) { s += circ(30.4 - oL * 0.85, y, 0.8, bc) + circ(69.6, y, 0.8, bc); });
    } else if (cut === 'qing') {
      // 马蹄袖放在手之后画（见 drawHands）
    } else if (cf) {
      s += P(cuffPath(oL, sw, 115.5, 124), cf) + P(mx(cuffPath(0, sw, 115.5, 124)), cf);
    } else if (cut === 'combat-shirt' || cut === 'field') {
      s += P(cuffPath(oL, sw, 119.5, 124), 'none', ' stroke-width=".45"') + P(mx(cuffPath(0, sw, 119.5, 124)), 'none', ' stroke-width=".45"');
    }
    return s;
  }
  function drawHands(C) {
    var g = C.p.gloves || SKIN, oL = C.armOut, s = ell(29.65 - oL, 129.3, 3.3, 5.3, g) + ell(70.35, 129.3, 3.3, 5.3, g);
    if (C.cut === 'qing') { // 马蹄袖：盖住手背的弧形袖头
      var hc = C.p.cuffs || shade(C.coatColor, 0.18), sw = C.sleeveW;
      s += P('M' + r1(26.4 - oL - sw) + ',121Q' + r1(29.2 - oL) + ',135.5 ' + r1(33.2 - oL) + ',121Z', hc);
      s += P(mx('M' + r1(26.4 - sw) + ',121Q29.2,135.5 33.2,121Z'), hc);
    }
    return s;
  }

  /* ---------- 武器（竖在身体右侧 = 观者左侧，枪托着地） ---------- */
  function drawWeapon(C) {
    var w = C.p.weapon, s = '';
    if (!w) return s;
    var wood = '#7a4a26', steel = '#62676b';
    if (w === 'musket' || w === 'rifle') {
      var top = w === 'musket' ? 62 : 84, bt = w === 'musket' ? 186 : 190;
      s += P('M22.6,213.4L27.8,213.4L26.5,' + bt + 'L24,' + bt + 'Z', wood);
      s += P('M24,' + bt + 'L26.5,' + bt + 'L26.1,' + top + 'L24.6,' + top + 'Z', wood);
      s += P('M24.8,' + top + 'L25.9,' + top + 'L25.8,' + (top - 16) + 'L24.9,' + (top - 16) + 'Z', steel);
      if (w === 'musket') {
        s += P('M25,' + (top - 15.5) + 'L25.9,' + (top - 15.5) + 'L25.5,20Z', '#b3b9bd');
        s += line('M26.9,176L26.4,76', '#e9e4d6', 0.9);                       // 白色枪背带
        s += line('M24.2,100L26.3,100M24.1,128L26.3,128', BRASS, 0.8);
      } else {
        s += circ(27.2, 174, 0.9, steel) + line('M24.1,120L26.3,120', steel, 0.8);
      }
    } else { // assault：枪托着地的现代步枪侧影
      var bk = '#2b2d2c';
      s += P('M22.8,213.2L27.4,213.2L27,196L23.6,196Z', bk);
      s += P('M24.4,196L26.4,196L26.4,180L24.4,180Z', bk);
      s += P('M23.2,180L27.6,180L27.6,152L23.2,152Z', bk);
      s += P('M23.2,174L23.2,166L19.4,164.2L18.6,171.8Z', bk);             // 弹匣
      s += P('M23.2,182L20.6,184.4L21.3,186.6L23.2,185Z', bk);             // 握把
      s += P('M27.6,160L29.4,160L29.4,170L27.6,170Z', bk);                 // 瞄具
      s += P('M23.6,152L27.2,152L27,126L23.8,126Z', '#3a3d3b');            // 护木
      s += P('M24.9,126L26,126L25.9,110L25,110Z', bk);
    }
    return s;
  }

  /* ---------- 上衣 ---------- */
  var HEM = { waist: 101, hip: 119, thigh: 134, knee: 165, calf: 192 };
  var HW = { waist: 12.9, hip: 13.9, thigh: 15.2, knee: 16.8, calf: 18.2 };
  var CUT = { // 默认：长度 / 领型 / [排数, 扣数]
    justaucorps: ['knee', 'none', 1, 10], coatee: ['waist', 'standing', 1, 8], tunic: ['hip', 'standing', 1, 8],
    frock: ['knee', 'standing', 1, 7], sack: ['thigh', 'turndown', 1, 4], blouse: ['thigh', 'standing', 1, 3],
    'service-closed': ['hip', 'turndown', 1, 5], service: ['hip', 'open-tie', 1, 4], battledress: ['waist', 'turndown', 1, 0],
    field: ['hip', 'turndown', 1, 5], 'combat-shirt': ['hip', 'mandarin', 1, 0], qing: ['calf', 'none', 1, 0]
  };
  function torso(H, hw, wx) {
    wx = wx || 37.2;
    return 'M44.5,44.5L33.5,48Q34.8,54 35.6,60L' + wx + ',94L' + r1(50 - hw) + ',' + H + 'L' + r1(50 + hw) + ',' + H +
      'L' + r1(100 - wx) + ',94L64.4,60Q65.2,54 66.5,48L55.5,44.5Z';
  }
  function btnCol(x, y0, y1, n, col, r) {
    var s = '';
    for (var i = 0; i < n; i++) s += circ(x, n > 1 ? lerp(y0, y1, i / (n - 1)) : y0, r || 0.95, col, ' stroke-width=".4"');
    return s;
  }
  // 成对贴袋：袋身（翻盖下）+ 尖角袋盖 + 扣 + 可选箱褶
  function pockets(x0, y0, x1, y1, fh, bc, pleat, fill) {
    var cx = r1((x0 + x1) / 2), yb = y0 + fh;
    var d = 'M' + x0 + ',' + yb + 'L' + x0 + ',' + y1 + 'L' + x1 + ',' + y1 + 'L' + x1 + ',' + yb;
    if (pleat) d += 'M' + cx + ',' + r1(yb + 1.4) + 'L' + cx + ',' + y1;
    var flap = 'M' + r1(x0 - 0.3) + ',' + y0 + 'L' + r1(x1 + 0.3) + ',' + y0 + 'L' + r1(x1 + 0.3) + ',' + yb + 'L' + cx + ',' + r1(yb + 1.4) + 'L' + r1(x0 - 0.3) + ',' + yb + 'Z';
    return PP(d, 'none', ' stroke-width=".5"') + PP(flap, fill, ' stroke-width=".55"') + (bc ? dots2([[+cx, yb - 0.3]], 0.65, bc, ' stroke-width=".3"') : '');
  }

  // 燕尾（画在裤子之前）
  function drawCoatBack(C) {
    if (C.cut !== 'coatee') return '';
    var tb = C.p.turnbacks || C.coatFill;
    return PP('M37.4,94L41.8,97L39.4,139L33.2,138.4Q33.8,118 36.6,98Z', tb) +
      PP('M36.6,98Q33.8,118 33.2,138.4L35.3,138.6Q36,118 37.8,99.2Z', C.coatFill);
  }

  function drawCoat(C) {
    var p = C.p, cut = C.cut, f = C.coatFill, col = C.coatColor, H = C.hem, s = '', bt = C.btn, hw, x;
    var edge = function (d) { return line(d, INK, 0.6); };
    switch (cut) {
      case 'justaucorps':
        hw = H >= 150 ? 18.2 : 15.6;
        s += P('M45.2,45L54.8,45L56.6,96L57.2,131Q50,133.5 42.8,131L43.4,96Z', p.waistcoat || shade(col, 0.12));
        s += btnCol(50, 51, 127, 10, bt.color, 0.65) + PP('M43.8,112L48.4,112', 'none', ' stroke-width=".6"');
        if (p.belt) s += P('M43,93.4L57,93.4L57.1,98L42.9,98Z', p.belt);
        s += PP('M44.5,44.5L33.5,48Q34.8,54 35.6,60L37.2,94L' + r1(50 - hw) + ',' + H + 'L43.4,' + H + 'L45.6,96L47.4,46Z', f);
        s += PP('M45.5,99L43.4,' + H + 'L' + r1(50 - hw + 4.2) + ',' + H + 'Z', p.turnbacks || p.facing || shade(col, 0.3));
        s += PP('M35.4,109.6L42.6,109.6L42.5,113.8Q40.9,112.4 39.1,114.2Q37.3,112.4 35.5,114Z', f, ' stroke-width=".6"');
        if (p.facing) {
          s += PP('M47.4,46.2L42.2,48.8L41.8,86L45.8,91.5Z', p.facing);
          x = []; for (var i = 0; i < 5; i++) x.push([43.4, 52 + i * 7.6]);
          s += dots2(x, 0.8, bt.color, ' stroke-width=".35"');
        } else {
          s += dots2([[46.4, 52], [46.2, 62], [46, 72], [45.8, 82]], 0.8, bt.color, ' stroke-width=".35"');
        }
        break;
      case 'coatee':
        if (p.waistcoat) s += P('M38.6,96L61.4,96L60.8,101.6L39.2,101.6Z', p.waistcoat);
        s += P('M44.5,44.5L33.5,48Q34.8,54 35.6,60L37.2,94L38.2,97.6L61.8,97.6L62.8,94L64.4,60Q65.2,54 66.5,48L55.5,44.5Z', f);
        if (p.facing) {
          s += P('M44.2,46.4L55.8,46.4L56.1,91.6L43.9,91.6Z', p.facing) + edge('M50,46.6L50,91.6');
          s += btnCol(45.3, 50, 88, bt.n || 7, bt.color, 0.8) + btnCol(54.7, 50, 88, bt.n || 7, bt.color, 0.8);
        } else if (p.lace) {
          for (var k = 0; k < 8; k++) { var y = 51 + k * 5.3; s += PP('M43.8,' + r1(y - 0.7) + 'L49.4,' + r1(y - 0.7) + 'L49.4,' + r1(y + 0.7) + 'L43.8,' + r1(y + 0.7) + 'L42.8,' + y + 'Z', p.lace, ' stroke-width=".3"'); }
          s += edge('M50,47L50,97.4') + btnCol(50, 51, 88.1, 8, bt.color, 0.75);
        } else if (bt.rows === 2) {
          s += edge('M55.4,47L55.2,97.4') + btnCol(45.6, 51, 90, bt.n || 7, bt.color, 0.8) + btnCol(54.4, 51, 90, bt.n || 7, bt.color, 0.8);
        } else s += edge('M50,47L50,97.4') + btnCol(50, 51, 92, bt.n || 8, bt.color);
        break;
      case 'sack':
        s += P('M44.5,44.5L33.5,48Q34.8,54 35.6,60L36.4,94L35.4,' + H + 'L64.6,' + H + 'L63.6,94L64.4,60Q65.2,54 66.5,48L55.5,44.5Z', f);
        s += edge('M50.8,48L50.8,' + (H - 2) + 'Q50.8,' + H + ' 52.6,' + H) + btnCol(50.8, 52, 93, bt.n || 4, bt.color, 1);
        s += PP('M38.6,70L44.6,69.4', 'none', ' stroke-width=".5"');
        break;
      case 'blouse':
        s += P('M44.5,44.5L33.5,48Q34.8,54 35.6,60L37.4,93L36.6,100L35.8,128L64.2,128L63.4,100L62.6,93L64.4,60Q65.2,54 66.5,48L55.5,44.5Z', f);
        s += P('M48.6,47L51.4,47L51.4,69.4L48.6,69.4Z', 'none', ' stroke-width=".55"') + btnCol(50, 51.6, 65.4, bt.n || 3, bt.color, 0.7);
        s += PP('M41.4,101Q40.8,108 40.4,114M46,101.5L45.8,109', 'none', ' stroke-width=".4" stroke-opacity=".35"');
        if (C.pk) s += pockets(38.4, 56, 46.8, 70, 4.4, bt.color, true, f);
        break;
      case 'battledress':
        s += P('M44.5,44.5L33.5,48Q34.8,54 35.6,60Q35.6,80 36,88Q35.4,93 37,95L63,95Q64.6,93 64,88Q64.4,80 64.4,60Q65.2,54 66.5,48L55.5,44.5Z', f);
        s += edge('M50.8,48L50.8,94') + pockets(38.4, 57.4, 47, 72, 4.6, bt.color, true, f);
        s += P('M36.8,94L63.2,94L63,101.4L37,101.4Z', f) + P('M55.6,95.4L59.4,95.4L59.4,100L55.6,100Z', p.beltBuckle || '#9a9784', ' stroke-width=".4"');
        s += P('M53,122L60.4,122L61,142L53.4,142Z', 'none', ' stroke-width=".5"') + P('M52.7,121.4L60.6,121.4L60.7,126.4L52.8,126.4Z', f, ' stroke-width=".55"');
        break;
      case 'qing':
        var hao = (p.hao && p.hao.color) || p.waistcoat || shade(col, -0.18), trim = (p.hao && p.hao.trim) || p.facing || '#b33a2e';
        C.trim = trim;
        s += P('M44.5,44.5L33.5,48Q34.8,54 35.6,60L37,94L31.8,192L68.2,192L63,94L64.4,60Q65.2,54 66.5,48L55.5,44.5Z', f) + edge('M50,150L50,192');
        s += P('M44,44.2L32.6,48Q34.2,56 35,62L35.6,96L34.2,136L65.8,136L64.4,96L65,62Q65.8,56 67.4,48L56,44.2Z', hao);
        s += P('M34.3,131.8L65.7,131.8L65.8,136L34.2,136Z', trim, ' stroke-width=".5"') + P('M49,46.6L51,46.6L51,131.8L49,131.8Z', trim, ' stroke-width=".4"');
        s += line('M44.2,44.3Q50,49.6 55.8,44.3', trim, 1.8) + P('M44.2,44.3Q50,49.6 55.8,44.3', 'none', ' stroke-width=".5"');
        break;
      default: // tunic / frock / service-closed / service / field / combat-shirt
        var wx = cut === 'field' ? 36.6 : 37.2;
        hw = C.hemHW;
        s += P(torso(H, hw, wx), f);
        if (cut === 'frock') s += line('M37.3,95.2Q50,96.8 62.7,95.2', INK, 0.5, ' stroke-opacity=".6"');
        if (cut === 'field') s += line('M36.8,96.4Q50,97.8 63.2,96.4', INK, 0.4, ' stroke-opacity=".5"');
        if (bt.rows === 2) {
          s += edge('M55.6,47.6L55.4,96L54.6,' + H);
          var n2 = bt.n || 6;
          for (var j = 0; j < n2; j++) {
            var t = n2 > 1 ? j / (n2 - 1) : 0, yy = lerp(52, 92, t), dx = lerp(4.8, 3.6, t);
            s += circ(50 - dx, yy, 0.95, bt.color, ' stroke-width=".4"') + circ(50 + dx, yy, 0.95, bt.color, ' stroke-width=".4"');
          }
        } else if (cut === 'combat-shirt') {
          s += line('M50,47.4L50,' + H, shade(C.coatColor, -0.45), 0.8);
        } else {
          var top = cut === 'service' ? 75 : 51.5, bot = cut === 'frock' ? 93 : cut === 'service' ? 111 : H - 8;
          s += edge('M50.8,' + (cut === 'service' ? 71 : 48) + 'L50.8,' + H) + (bt.n ? btnCol(50.8, top, bot, bt.n, bt.color) : '');
          if (p.facing && cut === 'tunic') s += line('M51.4,48L51.4,' + H, p.facing, 0.6);
        }
        if (cut === 'service-closed' || cut === 'field' || cut === 'service') {
          s += pockets(37.8, cut === 'service' ? 60 : 57, 46.8, cut === 'service' ? 72 : 72, 4.4, bt.n ? bt.color : null, cut !== 'service', f);
          s += pockets(37.4, 99, 47.2, cut === 'field' ? 121 : 115.5, 4.6, bt.n ? bt.color : null, cut === 'field', f);
        }
        if (cut === 'combat-shirt') {
          s += PP('M38.8,58.6L46.4,56.2L47.6,67.6L40,70Z', 'none', ' stroke-width=".5"') + PP('M38.9,60.4L46.6,58', 'none', ' stroke-width=".45"');
        }
    }
    return s;
  }

  /* ---------- 领 ---------- */
  function drawCollar(C) {
    var p = C.p, t = C.collar, cc = p.collarColor || C.coatFill, s = '';
    if (t === 'standing') {
      s += P('M44.6,47.8L44.8,40.6Q50,42.2 55.2,40.6L55.4,47.8Q50,48.8 44.6,47.8Z', cc) + line('M50,42.1L50,48.4', INK, 0.5);
      if (p.collarTabs) s += PP('M45.6,43.4L48.6,43.8L48.6,47.3L45.6,46.9Z', p.collarTabs, ' stroke-width=".4"');
    } else if (t === 'turndown') {
      s += P('M44.9,45.6L45.2,41Q50,42.4 54.8,41L55.1,45.6Z', cc);
      s += PP('M50,48.4L45.3,41.5L42.4,44.4L43.6,52.6Z', cc);
      if (p.collarTabs) s += PP('M42.9,45.8L46.9,48.4L45.6,51.2L43.5,51.2Z', p.collarTabs, ' stroke-width=".4"');
    } else if (t === 'open-tie') {
      var sh = p.shirt || '#d8cfb8', tie = p.tie || shade(C.coatColor, -0.3);
      s += P('M45.6,43.4L54.4,43.4L50,71Z', sh) + PP('M50,48.2L45.9,42.4L44.9,45L47.8,50.2Z', sh);
      s += P('M48.9,47.6L51.1,47.6L50.7,50.2L49.3,50.2Z', tie) + P('M49.3,50.2L50.7,50.2L51.5,66.5L50,69L48.5,66.5Z', tie);
      s += PP('M46.4,44L42.3,50.4L44.3,52.4L42.5,56.6L49.9,71.2Z', cc);
      if (p.collarTabs) s += dots2([[44.1, 49.6], [45.2, 58.8]], 1.05, p.collarTabs, ' stroke-width=".4"');
    } else if (t === 'mandarin') {
      s += P('M45,47L45.2,42.2Q50,43.4 54.8,42.2L55,47Q50,48 45,47Z', cc);
    } else if (C.cut === 'justaucorps' || C.cut === 'coatee') {
      s += P('M45.9,43L54.1,43L54.3,46.8L45.7,46.8Z', p.stock || LEATHER);   // 18 世纪黑领巾
    }
    return s;
  }

  /* ---------- 肩章 / 皮带 / 护甲 / 胸章 ---------- */
  function drawBelts(C) {
    var p = C.p, s = '';
    if (p.crossbelts) {
      s += P('M36.6,48.6L40.2,47.6L63.4,100.8L60,101.8Z', p.crossbelts, ' stroke-width=".6"');
      s += P(mx('M36.6,48.6L40.2,47.6L63.4,100.8L60,101.8Z'), p.crossbelts, ' stroke-width=".6"');
      s += ell(50, 74.8, 1.7, 2.2, p.beltBuckle || BRASS, ' stroke-width=".4"');
    }
    var wx = C.waistX;
    if (p.belt && C.cut !== 'justaucorps' && C.cut !== 'qing') {
      s += P('M' + r1(wx - 0.2) + ',93.6L' + r1(100.2 - wx) + ',93.6L' + r1(100.2 - wx) + ',98.6L' + r1(wx - 0.2) + ',98.6Z', p.belt, ' stroke-width=".6"');
      s += P('M47.3,93L52.7,93L52.7,99.2L47.3,99.2Z', p.beltBuckle || BRASS, ' stroke-width=".5"');
    }
    if (p.pouches) s += PP('M40,89.6L46.4,89.6L46.4,99.6L40,99.6Z', p.pouches, ' stroke-width=".55"') + PP('M40,92.2L46.4,92.2', 'none', ' stroke-width=".4"');
    if (p.sash) {
      s += P('M' + r1(wx - 0.2) + ',91.6L' + r1(100.2 - wx) + ',91.6L' + r1(100.2 - wx) + ',98.4L' + r1(wx - 0.2) + ',98.4Z', p.sash, ' stroke-width=".5"');
      s += P('M56.4,97L59.6,97L61,116L55.4,116Z', p.sash, ' stroke-width=".5"') + line('M56.4,112L60.4,112', INK, 0.4);
    }
    return s;
  }
  function drawArmor(C) {
    var p = C.p, s = '';
    if (!p.armor) return s;
    var af = p.armorColor || (C.camo ? C.coatFill : '#5f5f4c'), dk = ' fill="#000" fill-opacity=".13" stroke="none"';
    var body = p.armor === 'plate' ? 'M39,56.4Q50,59.4 61,56.4L61.4,106L50,107.4L38.6,106Z'
      : 'M36.8,55.4Q44,58.6 50,58.4Q56,58.6 63.2,55.4L64.2,70L63.4,113L50,114.6L36.6,113L35.8,70Z';
    var strap = 'M44.8,44.6L38.8,46.4L37.8,57.6L45.2,58.2Z';
    s += PP(strap, af) + P(body, af) + '<path d="' + body + '"' + dk + '/><path d="' + strap + '"' + dk + '/><path d="' + mx(strap) + '"' + dk + '/>';
    var y0 = p.armor === 'plate' ? 88 : 93;
    [39.8, 47.1, 54.4].forEach(function (x) {
      var d = 'M' + x + ',' + y0 + 'L' + r1(x + 5.8) + ',' + y0 + 'L' + r1(x + 5.8) + ',' + (y0 + 14) + 'L' + x + ',' + (y0 + 14) + 'Z';
      s += P(d, af, ' stroke-width=".55"') + '<path d="' + d + '"' + dk + '/>' + line('M' + x + ',' + (y0 + 3.4) + 'L' + r1(x + 5.8) + ',' + (y0 + 3.4), INK, 0.45);
    });
    s += line('M37,70L63,70', INK, 0.4, ' stroke-opacity=".5"');
    return s;
  }
  function drawOver(C) { // 画在手臂之后：肩章、臂袋、号衣短袖、肩饰绶
    var p = C.p, s = '', sw = C.sleeveW, t = p.shoulder, sc = p.shoulderColor || C.coatColor;
    if (C.cut === 'combat-shirt') {
      s += PP('M28.9,61L34.8,61L34.6,72.6L28.6,72.6Z', 'none', ' stroke-width=".5"');
      s += PP('M29.9,62.4L33.8,62.4L33.8,66.6L29.9,66.6Z', '#000', ' fill-opacity=".2" stroke="none"');
    }
    if (C.cut === 'qing') {
      var cap = 'M34.6,47.2Q' + r1(29 - sw) + ',48 ' + r1(27.6 - sw) + ',55L' + r1(26 - sw) + ',84.4L34.7,84.4L35.9,60Z';
      s += PP(cap, C.hao) + PP('M' + r1(26.1 - sw) + ',81L34.8,81L34.7,84.4L' + r1(26 - sw) + ',84.4Z', C.trim, ' stroke-width=".4"');
    }
    if (t === 'boards' || t === 'straps') {
      var w = t === 'boards' ? 1.05 : 0.7, ex = p.shoulderEdge ? ' stroke="' + p.shoulderEdge + '" stroke-width=".7"' : ' stroke-width=".5"';
      s += PP('M44.2,' + r1(44.4 - w) + 'L34.2,' + r1(47.3 - w) + 'L34.5,' + r1(47.4 + w) + 'L44.5,' + r1(44.5 + w) + 'Z', sc, ex);
      s += dots2([[42.9, 45]], 0.5, C.btn.color, ' stroke-width=".3"');
    } else if (t === 'epaulettes') {
      var fr = '';
      for (var x = 29.8; x < 38.5; x += 1.2) fr += 'M' + r1(x) + ',50.6L' + r1(x - 0.1) + ',55.4';
      s += PP('M29.2,49L38.9,48.6L38.6,55.6L29.4,56Z', sc, ' stroke-width=".5"') + PP(fr, 'none', ' stroke-width=".35" stroke-opacity=".6"');
      s += PP('M29.4,49.8Q28.4,46.4 33.4,45.6Q38.8,45.2 39.6,48.4Q35,50.8 29.4,49.8Z', sc, ' stroke-width=".6"');
    }
    if (p.aiguillette) {
      s += line('M36.4,49.4C37,60 42,66.8 47.2,64.6M36.9,49.6C38.6,56.8 43,61.8 47.2,60.8', p.aiguillette, 1);
      s += line('M47,64.8L46.6,72M47.4,61L48,70', p.aiguillette, 0.8) + circ(46.6, 72.4, 0.7, p.aiguillette) + circ(48, 70.4, 0.7, p.aiguillette);
    }
    return s;
  }
  function drawChestBadge(C) {
    var b = C.p.badge;
    if (!b || !b.chest) return '';
    var ch = String(b.chest).replace(/^char:/, ''), cy = C.cut === 'qing' ? 78 : 72;
    return circ(50, cy, 8.4, b.bg || '#f3efe2', ' stroke="' + (b.ring || C.trim || INK) + '" stroke-width="1.1"') +
      '<text x="50" y="' + (cy + 3.9) + '" font-size="11" text-anchor="middle" font-weight="700" stroke="none" fill="' + (b.color || '#1d1b19') +
      '" font-family="\'Noto Serif CJK SC\',\'Source Han Serif SC\',\'Songti SC\',SimSun,serif">' + esc(ch) + '</text>';
  }

  /* ---------- 头 ---------- */
  function drawHead(C) {
    var s = ell(41.8, 31.4, 1.7, 2.7, SKIN) + ell(58.2, 31.4, 1.7, 2.7, SKIN) + ell(50, 30, 8.2, 11.2, SKIN);
    s += P('M41.6,31C40.8,21.4 44,18.2 50,18.2C56,18.2 59.2,21.4 58.4,31L57.6,31C57.4,27 56.4,25 54.8,24.3Q50,23 45.2,24.3C43.6,25 42.6,27 42.4,31Z', HAIR, ' stroke-width=".6"');
    s += circ(46.7, 31, 0.75, INK, ' stroke="none"') + circ(53.3, 31, 0.75, INK, ' stroke="none"');
    s += line('M45.3,28.7L47.9,28.4M52.1,28.4L54.7,28.7', HAIR, 0.6) + line('M50,31.8L49.3,34.4L50.4,34.6', '#b48a6c', 0.5);
    s += line('M48.5,37Q50,37.7 51.5,37', '#9a6650', 0.6);
    if (C.p.moustache) s += P('M46.6,35.8Q50,33.8 53.4,35.8Q50,35.4 46.6,35.8Z', HAIR, ' stroke-width=".3"');
    return s;
  }

  /* ---------- 帽 / 盔 ---------- */
  function hatBadge(hg, cx, cy, r) {
    if (!hg.badge) return '';
    if (hg.badge === 'star') return P(star(cx, cy, r), hg.badgeColor || '#c8102e', ' stroke-width=".35"');
    return ell(cx, cy, r1(r * 0.75), r, hg.badge, ' stroke-width=".4"');
  }
  var STRAP = 'M42.2,26Q42.6,37 50,41.6Q57.4,37 57.8,26';
  function drawHeadgearBack(C) {
    var hg = C.hg;
    if (hg.type === 'cap' && hg.neckflap) return P('M40.8,22L59.2,22L60.8,39.4Q50,41 39.2,39.4Z', C.hatFill);
    return '';
  }
  function drawHeadgear(C) {
    var hg = C.hg, t = hg.type, f = C.hatFill, b = hg.band, s = '', dk = shade(hg.color || '#555', -0.3);
    switch (t) {
      case 'tricorne':
        s += ell(50, 11, 8.5, 4.2, f);
        s += P('M31,14Q40,17.6 50,26.6Q60,17.6 69,14Q64,11.6 57,11.4Q50,9.6 43,11.4Q36,11.6 31,14Z', f);
        if (b) s += line('M31,14Q40,17.6 50,26.6Q60,17.6 69,14M31,14Q36,11.6 43,11.4M69,14Q64,11.6 57,11.4', b, 1.1);
        s += circ(39.4, 15.4, 1.8, hg.cockade || LEATHER, ' stroke-width=".4"') + circ(39.4, 15.4, 0.6, BRASS, ' stroke="none"');
        break;
      case 'bicorne':
        s += P('M27,23Q31,19.2 38,18Q43,3.6 50,3.2Q57,3.6 62,18Q69,19.2 73,23Q50,19.8 27,23Z', f);
        if (b) s += line('M27,23Q31,19.2 38,18Q43,3.6 50,3.2Q57,3.6 62,18Q69,19.2 73,23', b, 0.9);
        s += circ(50, 12.4, 2.7, hg.cockade || '#1f3a8a', ' stroke-width=".4"') + circ(50, 12.4, 1.7, '#f2efe6', ' stroke="none"') + circ(50, 12.4, 0.8, '#c8102e', ' stroke="none"');
        if (hg.plume) s += P('M48.6,5.6Q48.2,3.2 50,2.4Q51.8,3.2 51.4,5.6Z', hg.plume);
        break;
      case 'mitre':
        s += P('M41,25L41.4,14Q43.4,5.6 50,2.6Q56.6,5.6 58.6,14L59,25Z', f);
        s += P('M41,20.8L59,20.8L59,25L41,25Z', b || shade(f, -0.3)) + ell(50, 12.4, 3.4, 4.6, hg.badge || BRASS, ' stroke-width=".5"');
        s += circ(50, 3.6, 1.3, hg.plume || '#f2efe6', ' stroke-width=".4"');
        break;
      case 'shako':
        if (hg.flare) {
          s += P('M42,25.2C42.6,18 37.8,11.2 36.8,6.8L63.2,6.8C62.2,11.2 57.4,18 58,25.2Z', f) + ell(50, 6.8, 13.2, 1.8, shade(f, 0.12));
        } else if (hg.belgic) {
          s += P('M41.6,25.2L41,6.4Q50,1.2 59,6.4L58.4,25.2Z', f);
        } else {
          s += P('M41.6,25.2L40.2,6.8L59.8,6.8L58.4,25.2Z', f) + ell(50, 6.8, 9.8, 1.6, shade(f, 0.12));
        }
        if (b) s += P('M41.6,22.4L58.4,22.4L58.4,25.2L41.6,25.2Z', b);
        s += P(hg.belgic ? 'M50,11L54.8,16.6L50,22.4L45.2,16.6Z' : 'M50,10.6L54.2,15.8L50,21L45.8,15.8Z', hg.badge || BRASS, ' stroke-width=".5"');
        if (hg.cords || hg.flare || hg.belgic) s += line('M41.8,21.4Q46,25.2 50,21.8Q54,25.2 58.2,21.4', hg.cords || '#f2efe6', 0.8);
        s += P('M41,24.6Q50,29.4 59,24.6Q50,26.4 41,24.6Z', LEATHER);
        if (hg.plume) s += hg.belgic ? P('M56.2,14.4Q55.2,9.4 57.3,6.2Q59.4,9.4 58.4,14.4Z', hg.plume)
          : hg.flare ? ell(50, 4.6, 2.4, 2.2, hg.plume) : P('M48.5,7.4Q47.6,4 50,2.4Q52.4,4 51.5,7.4Z', hg.plume);
        break;
      case 'bearskin':
        s += P('M40.2,26C37.4,19 37,8 41.6,3.6Q50,1.2 58.4,3.6C63,8 62.6,19 59.8,26Z', f);
        s += line('M44,8.6L43.6,12M48.2,5.8L48,9.4M52.6,6L52.8,9.6M56.4,9L56.8,12.4M42.4,15L42,18.6M46.6,13L46.4,16.6M51,12.6L51.2,16.4M55.4,15.4L55.8,19M58.2,19.6L58.6,22.6M44.6,20L44.4,23.2', '#fff', 0.45, ' stroke-opacity=".22"');
        if (hg.plume) s += P('M59.6,19Q58.8,10 60.4,5.6Q62.4,10 61.4,19Z', hg.plume);
        break;
      case 'papakha':
        s += P('M40.6,26.2L41,13.6Q50,11.2 59,13.6L59.4,26.2Z', f);
        s += line('M43.2,15.2L43,18.2M46.8,14.2L46.6,17.4M50.4,13.9L50.4,17.1M54,14.2L54.2,17.4M57.2,15.2L57.4,18.2M42.8,20.8L42.6,23.8M47,19.8L46.8,23M51.6,19.8L51.8,23M56,20.6L56.2,23.6', '#fff', 0.45, ' stroke-opacity=".22"');
        if (hg.badge) s += '<circle cx="50" cy="19" r="1.9" fill="' + (hg.badge === true ? BRASS : hg.badge) + '" stroke-width=".4"/>';
        break;
      case 'pickelhaube':
        var hc = hg.cover ? (hg.coverColor || '#8d8f7e') : (hg.color || LEATHER);
        s += P('M41,24.6C40.6,14.8 44,11.2 50,11.2C56,11.2 59.4,14.8 59,24.6Z', hc);
        s += P('M47.8,11.8L52.2,11.8L51.4,9.6L48.6,9.6Z', hg.cover ? hc : BRASS) + P('M48.9,9.8L51.1,9.8L50,2.6Z', hg.cover ? hc : BRASS);
        if (hg.cover) s += '<text x="50" y="21" font-size="5" text-anchor="middle" font-weight="700" stroke="none" fill="#b8322a" font-family="sans-serif">' + esc(hg.number || '9') + '</text>';
        else s += P('M50,14.4L54,16.6L53.4,20.8L50,23L46.6,20.8L46,16.6Z', hg.badge || BRASS, ' stroke-width=".5"');
        s += P('M41,24.2Q50,29.4 59,24.2Q50,26.2 41,24.2Z', LEATHER);
        break;
      case 'hsh':
        s += P('M40.6,25.2C39.8,13 43.4,6.4 50,6.2C56.6,6.4 60.2,13 59.4,25.2Z', f);
        s += P('M48.3,6.9L51.7,6.9L50,2.6Z', BRASS) + ell(50, 6.8, 2, 0.8, BRASS);
        s += P(star(50, 16.4, 4.6), hg.badge || BRASS, ' stroke-width=".4"') + circ(50, 16.4, 1.4, shade(f, 0.2), ' stroke-width=".3"');
        s += line('M40.8,23.4Q50,25.4 59.2,23.4', BRASS, 0.9) + P('M40.6,24.6Q50,29.6 59.4,24.6Q50,26.6 40.6,24.6Z', f);
        break;
      case 'kepi':
        var top = b || f;
        if (hg.slouch) s += P('M42.4,21C41.6,16 42,10.6 47.6,9.6Q57,8.6 58,13.4C58.4,16.6 57.8,19 57.6,21Z', top);
        else s += P('M42.4,21L43.4,14L56.6,14L57.6,21Z', top) + ell(50, 14, 6.6, 1.3, shade(top, 0.12));
        s += P('M41.6,20.4L58.4,20.4L58.8,25.2L41.2,25.2Z', f) + line('M42,23.2L58,23.2', LEATHER, 0.7) + circ(42.6, 23.2, 0.6, BRASS) + circ(57.4, 23.2, 0.6, BRASS);
        s += hatBadge(hg, 50, 17.4, 1.8) + P('M41.2,24.8Q50,29.8 58.8,24.8Q50,26.8 41.2,24.8Z', LEATHER);
        break;
      case 'peaked':
        s += P('M40.8,19.2C35.6,18.6 35.4,12.4 42,11.4Q50,10.2 58,11.4C64.6,12.4 64.4,18.6 59.2,19.2Z', f);
        s += P('M41.8,18.4L58.2,18.4L58.4,24.6L41.6,24.6Z', b || shade(f, -0.2)) + line('M42.4,23.4L57.6,23.4', hg.cord || BRASS, 0.7);
        s += hatBadge(hg, 50, 20.6, 2.5) + P('M41.4,24.2Q50,30 58.6,24.2Q50,26.8 41.4,24.2Z', hg.visor || LEATHER);
        break;
      case 'sidecap':
        s += P('M41.4,24.2L42.4,17.6Q46.6,15.2 50,16.8Q53.8,13.8 58,14.4L58.6,22.4Q50,22.2 41.4,24.2Z', f) + line('M41.8,21.2Q50,19.2 58.4,18.8', INK, 0.5);
        s += hatBadge(hg, 50, 20.6, 1.8);
        break;
      case 'budenovka':
        s += P('M41.2,21.4C40.8,13 44.6,7.4 50,2.2C55.4,7.4 59.2,13 58.8,21.4Z', f) + circ(50, 2.4, 0.9, f);
        s += P('M41,20.6L59,20.6L59.4,25.4L40.6,25.4Z', f) + circ(42.6, 23, 0.6, dk) + circ(57.4, 23, 0.6, dk);
        s += P(star(50, 13.4, 6.2), b || '#b22234', ' stroke-width=".4"') + P(star(50, 13.8, 2.2), hg.badgeColor || '#c8102e', ' stroke-width=".3"');
        s += P('M41.4,25Q50,29.6 58.6,25Q50,27 41.4,25Z', f);
        break;
      case 'beret':
        s += P('M57.8,21.4Q60.4,17.4 56.4,14.4Q49,10.6 40.6,14Q34.2,17.2 34.8,21.8Q35.6,24.6 40.2,23.2L42.4,22.6Z', f);
        s += P('M42,22.2L58.2,21.2L58.4,24.2Q50,24.4 41.8,25.4Z', shade(hg.color || '#333', -0.35), ' stroke-width=".5"');
        s += hg.badge === 'star' ? hatBadge(hg, 55, 19, 1.9) : ell(55, 19, 1.5, 2, hg.badge || BRASS, ' stroke-width=".4"');
        break;
      case 'brodie':
        s += P('M38.6,23.4C38.6,14.8 43.4,11.8 50,11.8C56.6,11.8 61.4,14.8 61.4,23.4Z', f) + P('M29.4,25.4Q50,18.4 70.6,25.4Q50,28.4 29.4,25.4Z', f);
        s += line(STRAP, '#4a3f30', 0.7, ' stroke-opacity=".8"');
        break;
      case 'adrian':
        s += P('M41,23.2C40.6,15.4 44.4,11.6 50,11.6C55.6,11.6 59.4,15.4 59,23.2Z', f);
        s += P('M48.2,12.4C48.4,8.2 49.2,6.8 50,6.8C50.8,6.8 51.6,8.2 51.8,12.4Z', f);
        s += circ(50, 18.4, 1.5, hg.badge || shade(hg.color || '#777', -0.25), ' stroke-width=".35"') + P('M48.9,17.2Q50,13.8 51.1,17.2Z', hg.badge || shade(hg.color || '#777', -0.25), ' stroke-width=".35"');
        s += P('M36.4,23.4Q50,20.6 63.6,23.4Q60,26.2 50,26.4Q40,26.2 36.4,23.4Z', f) + line(STRAP, '#4a3f30', 0.7, ' stroke-opacity=".8"');
        break;
      case 'm1':
        s += P('M38.8,25.4C38.4,13.6 42.4,9.2 50,9.2C57.6,9.2 61.6,13.6 61.2,25.4Z', f);
        s += P('M37.4,25.2Q50,23.2 62.6,25.2L62.2,27.2Q50,25.4 37.8,27.2Z', f) + line('M39.6,27L40.6,34.6M60.4,27L59.4,34.6', '#6b5a40', 0.7);
        s += hatBadge(hg, 50, 17, 2.2);
        break;
      case 'ssh40':
        s += P('M39,28.2C38,15 42.4,8.8 50,8.8C57.6,8.8 62,15 61,28.2Q59.6,26 57.6,25.4Q50,23.8 42.4,25.4Q40.4,26 39,28.2Z', f);
        s += line('M39.2,27.6Q40.6,25.8 42.4,25.2Q50,23.6 57.6,25.2Q59.4,25.8 60.8,27.6', dk, 0.8) + hatBadge(hg, 50, 16, 2.5) + line(STRAP, '#4a3f30', 0.7, ' stroke-opacity=".8"');
        break;
      case 'm35':
        s += P('M39.6,20C40,11.4 44,8 50,8C56,8 60,11.4 60.4,20L61,26.6Q63.2,29.6 64.6,32.2L59.6,31.6Q58.6,27.6 57,25.8Q50,24 43,25.8Q41.4,27.6 40.4,31.6L35.4,32.2Q36.8,29.6 39,26.6Z', f);
        s += circ(40.9, 17.6, 0.55, dk) + circ(59.1, 17.6, 0.55, dk) + hatBadge(hg, 50, 16.4, 2.2) + line(STRAP, '#4a3f30', 0.7, ' stroke-opacity=".8"');
        break;
      case 'pasgt':
        s += P('M38.6,30.4C37.4,14.2 41.4,8.4 50,8.4C58.6,8.4 62.6,14.2 61.4,30.4L58.6,31.4Q57.8,27.2 56,26Q50,24.6 44,26Q42.2,27.2 41.4,31.4Z', f);
        s += P('M38.7,19.6Q50,17.2 61.3,19.6L61.4,22.4Q50,20.2 38.6,22.4Z', b || '#4b4a36', ' stroke-width=".4"') + line(STRAP, '#3a3b36', 0.7);
        break;
      case 'modern':
        s += P('M39.4,26.6C38.4,13.4 42,8.6 50,8.6C58,8.6 61.6,13.4 60.6,26.6L58.2,27Q57.6,24.6 55.6,24.2Q50,23.4 44.4,24.2Q42.4,24.6 41.8,27Z', f);
        s += PP('M39.5,19.2L41.8,19L42,25L39.8,25.2Z', '#3a3b36', ' stroke-width=".4"') + line(STRAP, '#3a3b36', 0.8);
        if (hg.nvg !== false) s += P('M46.4,17L53.6,17L53.2,21.8L46.8,21.8Z', '#3a3b36', ' stroke-width=".4"');
        break;
      case 'campaign':
        s += P('M42,22L44.2,11.4Q46.8,8.4 50,5.6Q53.2,8.4 55.8,11.4L58,22Z', f) + line('M47.2,9.4L48.2,15.6M52.8,9.4L51.8,15.6', dk, 0.5);
        s += P('M42,19.2L58,19.2L58.2,22L41.8,22Z', b || dk) + P('M28,23.2Q50,19.6 72,23.2Q50,25.6 28,23.2Z', f);
        break;
      case 'boonie':
        s += P('M42.2,23L42.6,14.2Q50,11.2 57.4,14.2L57.8,23Z', f) + P('M42.4,18.2L57.6,18.2L57.7,21.4L42.3,21.4Z', f, ' stroke-width=".4"');
        s += line('M45,18.2L45,21.4M50,18.2L50,21.4M55,18.2L55,21.4', INK, 0.4) + hatBadge(hg, 50, 15.4, 1.8);
        s += P('M32,27.8Q34,22.6 42,22L58,22Q66,22.6 68,27.8Q63.6,25.6 58,25.4Q50,25 42,25.4Q36.4,25.6 32,27.8Z', f);
        break;
      case 'cap':
        s += P('M41.6,24.2C41,16.6 43.6,12.4 50,12.2C56.4,12.4 59,16.6 58.4,24.2Z', f) + line('M42.6,16.6Q50,14.6 57.4,16.6', INK, 0.4, ' stroke-opacity=".6"');
        s += hatBadge(hg, 50, 19.6, 2.3) + P('M42,23.4Q50,21.8 58,23.4L57.4,26.4Q50,28.6 42.6,26.4Z', hg.visor || f);
        break;
      case 'cap8':
        s += P('M42,20.4L38.4,15.6L40.6,11.6L46,10.2L54,10.2L59.4,11.6L61.6,15.6L58,20.4Z', f) + line('M46,10.2L45.4,19.6M54,10.2L54.6,19.6', INK, 0.4, ' stroke-opacity=".6"');
        s += P('M41.8,19.6L58.2,19.6L58.4,24.8L41.6,24.8Z', f) + hatBadge(hg, 50, 21.8, 2.4);
        s += P('M41.6,24.4Q50,29.2 58.4,24.4Q50,26.6 41.6,24.4Z', hg.visor || shade(hg.color || '#666', -0.15));
        break;
      case 'ushanka':
        s += P('M40.6,20C40.4,11.4 44.6,9.6 50,9.6C55.4,9.6 59.6,11.4 59.4,20Z', b || shade(f, -0.1));
        s += hg.flaps === 'down' ? PP('M37.6,21L43.4,21L43.2,36.6Q40.4,38.4 37.8,36.6Z', f) : PP('M37.8,14.6L42,13.8L42.4,23.6L38,24.2Z', f);
        s += P('M38.8,16.6Q50,13.6 61.2,16.6L61.6,24.8Q50,23.4 38.4,24.8Z', f);
        s += line('M41.6,18L41.8,22.4M45.4,17.2L45.4,21.6M54.6,17.2L54.6,21.6M58.4,18L58.2,22.4', '#000', 0.45, ' stroke-opacity=".25"') + hatBadge(hg, 50, 19.8, 2.4);
        break;
      case 'qing':
        var red = hg.plume || '#b3261e';
        if (hg.warm) {
          s += P('M40.6,23.6Q40.8,13.6 50,13Q59.2,13.6 59.4,23.6Z', hg.color || '#2a2622');
          s += P('M50,12.6L57.6,20.2Q50,21.6 42.4,20.2Z', red) + line('M50,12.8L45,20.4M50,12.8L50,21M50,12.8L55,20.4', shade(red, -0.35), 0.35);
          s += P('M38.6,25.6Q38.8,20.6 41.2,20L58.8,20Q61.2,20.6 61.4,25.6Q50,27.6 38.6,25.6Z', hg.band || '#3b3029');
          s += circ(50, 12.4, 1.5, hg.badge || '#b8962e', ' stroke-width=".4"');
          break;
        }
        s += P('M30.6,24.6L50,10.6L69.4,24.6Q50,28.6 30.6,24.6Z', f);
        s += P('M50,10.4L60.8,22.6Q50,24.6 39.2,22.6Z', red) + line('M50,10.8L42.6,22.6M50,10.8L46.4,23.4M50,10.8L50,23.8M50,10.8L53.6,23.4M50,10.8L57.4,22.6', shade(red, -0.35), 0.35);
        s += circ(50, 9.8, 1.6, hg.badge || '#b8962e', ' stroke-width=".4"');
        break;
    }
    return s;
  }

  /* ---------- 组装 ---------- */
  var HAT_DEF = {
    tricorne: '#1f1d1b', bicorne: '#1f1d1b', mitre: '#b0282e', shako: '#1f1d1b', bearskin: '#1f1d1b', pickelhaube: LEATHER,
    hsh: '#1d2a57', brodie: '#6a6a45', adrian: '#7c93ab', m1: '#5b5a3c', ssh40: '#56603f', m35: '#5b5e52', pasgt: '#5b5a3c',
    modern: '#6b6a55', ushanka: '#6e6a58', qing: '#e6d9b0', beret: '#23304f'
  };
  function svg(p, opts) {
    p = p || {}; opts = opts || {};
    var id = String(opts.id || 'uf').replace(/[^\w-]/g, '_');
    var coat = p.coat || {}, cut = CUT[coat.cut] ? coat.cut : 'tunic', def = CUT[cut], col = coat.color || '#6b6a4a';
    var camo = p.camo && p.camo.type ? p.camo : null, len = coat.length || def[0], bt = p.buttons || {}, tr = p.trousers || {};
    var C = {
      p: p, id: id, cut: cut, coatColor: col, camo: camo, coatFill: camo ? 'url(#' + id + '-camo)' : col,
      hem: HEM[len] || 119, hemHW: HW[len] || 13.9, collar: p.collar || def[1], pk: coat.pockets,
      btn: { rows: bt.rows || def[2], n: bt.n != null ? bt.n : def[3], color: bt.color || BRASS },
      armOut: p.weapon ? 4.5 : 0, sleeveW: cut === 'qing' ? 1.4 : (cut === 'sack' || cut === 'field') ? 0.6 : 0,
      waistX: { sack: 36.4, field: 36.6, blouse: 37.4 }[cut] || 37.2
    };
    if (C.btn.rows === 2 && bt.n == null) C.btn.n = 6;
    C.tr = { color: tr.color || col, stripe: tr.stripe || null, style: tr.style || 'trousers', flare: tr.flare, stripeWidth: tr.stripeWidth };
    C.trFill = camo && tr.camo !== false ? C.coatFill : C.tr.color;
    C.hg = p.headgear || { type: 'none' };
    C.hatFill = C.hg.cover === 'camo' && camo ? C.coatFill : (C.hg.color || HAT_DEF[C.hg.type] || col);
    C.hao = (p.hao && p.hao.color) || p.waistcoat || shade(col, -0.18);
    C.trim = (p.hao && p.hao.trim) || p.facing || '#b33a2e';

    var HS = '<g transform="translate(50 30) scale(1.07) translate(-50 -30)">', hb = drawHeadgearBack(C);
    var body = (hb ? HS + hb + '</g>' : '') + drawCoatBack(C) + drawTrousers(C) +
      P('M46,35L54,35L54.2,47.5L45.8,47.5Z', SKIN) +                    // 颈
      drawCoat(C) + drawChestBadge(C) + drawBelts(C) + drawArmor(C) +
      drawArms(C) + drawOver(C) + drawWeapon(C) + drawHands(C) +
      drawCollar(C) + HS + drawHead(C) + drawHeadgear(C) + '</g>';

    var s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 220"' +
      (opts.width ? ' width="' + opts.width + '"' : '') + (opts.height ? ' height="' + opts.height + '"' : '') +
      ' role="img" aria-labelledby="' + id + '-t"><title id="' + id + '-t">' + esc(opts.title || p.title || '军服示意图') + '</title>';
    if (camo) s += '<defs>' + drawCamoDefs(id, camo) + '</defs>';
    if (opts.plate !== false) s += '<rect x="1" y="1" width="98" height="218" rx="6" fill="#ecebe4" stroke="#d6d4ca" stroke-width="1"/>';
    s += ell(50, 214, 17, 2.2, '#000', ' fill-opacity=".08"');
    return s + '<g stroke="' + INK + '" stroke-width=".9" stroke-linejoin="round" stroke-linecap="round">' + body + '</g></svg>';
  }

  /* ---------- 预设（颜色为近似值，页面可覆盖） ---------- */
  var W = '#f2efe6', BK = '#1d1b19', PEWTER = '#d9d6cc';
  var PRESETS = {
    uk1750: { title: '英国 1750 步兵', headgear: { type: 'tricorne', band: W }, coat: { cut: 'justaucorps', color: '#b0282e' },
      facing: '#e8d67a', cuffs: '#e8d67a', turnbacks: '#e8d67a', waistcoat: '#b0282e', buttons: { color: PEWTER },
      belt: W, trousers: { color: '#b0282e', style: 'breeches-gaiters' }, gaiters: W, weapon: 'musket' },
    uk1815: { title: '英国 1815 近卫步兵', headgear: { type: 'shako', belgic: true, plume: W, cords: W }, coat: { cut: 'coatee', color: '#b0282e' },
      collarColor: '#1d2a57', cuffs: '#1d2a57', turnbacks: W, lace: W, buttons: { color: PEWTER }, shoulder: 'straps', shoulderColor: '#1d2a57',
      crossbelts: W, trousers: { color: '#8a8c8e' }, weapon: 'musket' },
    fr1812: { title: '法国 1812 线列步兵', headgear: { type: 'shako', badge: BRASS, plume: '#c8322a' }, coat: { cut: 'coatee', color: '#1f2e5c' },
      facing: W, cuffs: '#c0302a', collarColor: '#c0302a', turnbacks: W, waistcoat: W, shoulder: 'straps', shoulderColor: '#1f2e5c', shoulderEdge: '#c0302a',
      crossbelts: W, trousers: { color: W, style: 'breeches-gaiters' }, gaiters: BK },
    ru1812: { title: '俄国 1812 步兵', headgear: { type: 'shako', flare: true, plume: '#e8e2d0' }, coat: { cut: 'coatee', color: '#1f3b2a' },
      buttons: { rows: 2, n: 6 }, collarColor: '#c0302a', cuffs: '#c0302a', turnbacks: '#c0302a', shoulder: 'straps', shoulderColor: '#c0302a',
      crossbelts: W, trousers: { color: W }, footwear: BK },
    us1779: { title: '美国 1779 大陆军', headgear: { type: 'tricorne', band: W }, coat: { cut: 'justaucorps', color: '#1f2c52', length: 'thigh' },
      facing: '#b0282e', cuffs: '#b0282e', turnbacks: W, waistcoat: W, buttons: { color: PEWTER }, crossbelts: W,
      trousers: { color: W, style: 'breeches-gaiters' }, gaiters: BK },
    us1863: { title: '美国 1863 联邦步兵', headgear: { type: 'kepi', color: '#253357', slouch: true }, coat: { cut: 'sack', color: '#253357' },
      buttons: { n: 4 }, trousers: { color: '#7d95b8' }, belt: BK, beltBuckle: BRASS },
    fr1914: { title: '法国 1914 步兵', headgear: { type: 'kepi', color: '#2d3a63', band: '#b8322a' }, coat: { cut: 'frock', color: '#2d3a63', length: 'knee' },
      buttons: { rows: 2, n: 6 }, collar: 'turndown', collarTabs: '#b8322a', trousers: { color: '#b8322a', style: 'leggings' }, gaiters: BK, gaiterTop: 184, belt: BK, pouches: BK },
    de1914: { title: '德国 1914 步兵', headgear: { type: 'pickelhaube', cover: true }, coat: { cut: 'tunic', color: '#6f7462' },
      buttons: { n: 8 }, facing: '#b8322a', cuffs: '#6f7462', shoulder: 'straps', shoulderColor: '#6f7462', shoulderEdge: '#b8322a',
      belt: '#2a2723', beltBuckle: '#a4a494', pouches: '#2a2723', trousers: { color: '#6f7462', style: 'boots' }, moustache: true },
    fr1916: { title: '法国 1916 步兵', headgear: { type: 'adrian', color: '#7c93ab' }, coat: { cut: 'frock', color: '#7c93ab' },
      buttons: { rows: 2, n: 6, color: '#a9ada6' }, collar: 'turndown', collarTabs: '#e0c060', trousers: { color: '#7c93ab', style: 'puttees' }, puttees: '#7c93ab',
      belt: '#5a3a24', pouches: '#5a3a24', footwear: '#3a2a1e' },
    uk1916: { title: '英国 1916 步兵', headgear: { type: 'brodie', color: '#6a6a45' }, coat: { cut: 'service-closed', color: '#7a6a45' },
      buttons: { color: '#b89a52' }, shoulder: 'straps', trousers: { color: '#7a6a45', style: 'puttees' }, puttees: '#7a6a45',
      belt: '#9a8c62', beltBuckle: '#b89a52', pouches: '#9a8c62', footwear: '#3a2a1e' },
    ru1943: { title: '苏联 1943 步兵', headgear: { type: 'sidecap', color: '#7b7454', badge: 'star' }, coat: { cut: 'blouse', color: '#7b7454' },
      collar: 'standing', shoulder: 'boards', shoulderColor: '#7b7454', shoulderEdge: '#b8322a', belt: '#5a3d24', beltBuckle: '#b09a52',
      trousers: { color: '#6f6a4c', style: 'boots', flare: true } },
    us1944: { title: '美国 1944 步兵', headgear: { type: 'm1', color: '#5b5a3c' }, coat: { cut: 'field', color: '#6a654a' },
      buttons: { color: '#4a4636' }, belt: '#8a7f5a', beltBuckle: '#8a8778', trousers: { color: '#5e5a44', style: 'bloused' }, footwear: '#5a3a24' },
    uk1944: { title: '英国 1944 步兵', headgear: { type: 'brodie', color: '#5d5a40' }, coat: { cut: 'battledress', color: '#6b5f45' },
      buttons: { color: '#5a4f38' }, belt: '#8a7f5a', beltBuckle: '#b89a52', trousers: { color: '#6b5f45', style: 'anklets' }, gaiters: '#8a7f5a' },
    cn1965: { title: '中国 1965 式', headgear: { type: 'cap', color: '#5d6a3c', badge: 'star' }, coat: { cut: 'service-closed', color: '#5d6a3c' },
      collar: 'turndown', collarTabs: '#c8102e', buttons: { color: '#4a5530' }, trousers: { color: '#5d6a3c' }, footwear: BK, sole: '#e8e6de' },
    fr1956: { title: '法国 1956 伞兵', headgear: { type: 'cap', cover: 'camo', neckflap: true }, coat: { cut: 'field' },
      camo: { type: 'lizard', colors: ['#6b7a4a', '#5a4a33', '#2f3b25'], seed: 3 }, buttons: { color: '#3a3a2a' },
      trousers: { style: 'bloused' }, footwear: BK },
    us1985: { title: '美国 1985 步兵', headgear: { type: 'pasgt', cover: 'camo' }, coat: { cut: 'field' },
      camo: { type: 'woodland', colors: ['#5b6b3a', '#5a4632', '#b19b73', '#1e1e1a'], seed: 4 }, buttons: { color: '#2a2a22' },
      trousers: { style: 'bloused' }, footwear: BK },
    ru1985: { title: '苏联 1985 阿富汗', headgear: { type: 'boonie', color: '#b5a57a', badge: 'star' }, coat: { cut: 'field', color: '#b5a57a' },
      buttons: { color: '#8a7d58' }, shoulder: 'straps', shoulderColor: '#b5a57a', belt: '#5a3d24', beltBuckle: '#b09a52',
      trousers: { color: '#b5a57a', style: 'bloused' }, footwear: BK },
    uk1990: { title: '英国 1990 步兵', headgear: { type: 'beret', color: '#23304f', badge: BRASS }, coat: { cut: 'field' },
      camo: { type: 'brush', colors: ['#b4a07a', '#5d6b3d', '#6b4a30', '#1e1e1a'], seed: 5 }, buttons: { n: 0 },
      trousers: { style: 'bloused' }, footwear: BK },
    cn2007: { title: '中国 07 式', headgear: { type: 'cap', cover: 'camo' }, coat: { cut: 'combat-shirt' },
      camo: { type: 'digital', colors: ['#6f7d4f', '#3f4f2e', '#5c4a33', '#1f211b'], seed: 7 }, belt: '#2f3326', beltBuckle: '#6b6f66',
      trousers: { style: 'bloused' }, footwear: BK },
    us2008: { title: '美国 2008 ACU', headgear: { type: 'modern', cover: 'camo' }, coat: { cut: 'combat-shirt' },
      camo: { type: 'digital', colors: ['#b8b8a8', '#8a8f7a', '#b9ae8f'], seed: 11 }, armor: 'vest',
      trousers: { style: 'bloused' }, footwear: '#a08c6a' },
    uk2012: { title: '英国 2012 MTP', headgear: { type: 'modern', cover: 'camo' }, coat: { cut: 'combat-shirt' },
      camo: { type: 'multi', colors: ['#b9a57e', '#7a7a52', '#6e5a3e', '#3e3325'], seed: 13 }, armor: 'vest', gloves: '#4a4538',
      trousers: { style: 'bloused' }, footwear: '#7a5f40' },
    us2020: { title: '美国 2020 AGSU', headgear: { type: 'peaked', color: '#3b4a33', band: '#2c3826', badge: BRASS }, coat: { cut: 'service', color: '#3b4a33' },
      collar: 'open-tie', shirt: '#c8b48f', tie: '#2c3826', collarTabs: BRASS, buttons: { n: 4 }, shoulder: 'straps',
      belt: '#3b4a33', beltBuckle: BRASS, trousers: { color: '#a89a88' }, footwear: '#4a2f1f' },
    cn1955: { title: '中国 1955 式', headgear: { type: 'peaked', color: '#7d7a4b', band: '#b22222', badge: 'star' }, coat: { cut: 'service-closed', color: '#7d7a4b' },
      collar: 'standing', collarTabs: '#b22222', shoulder: 'boards', shoulderColor: '#c9a646', buttons: { n: 5 },
      trousers: { color: '#7d7a4b' }, footwear: BK },
    qing1860: { title: '清 1860 绿营', headgear: { type: 'qing' }, coat: { cut: 'qing', color: '#2b3b5c' }, hao: { trim: '#b33a2e' },
      badge: { chest: '兵', color: BK, bg: '#f3efe2' }, footwear: BK }
  };

  root.UniformFig = {
    svg: svg, PRESETS: PRESETS,
    CUTS: Object.keys(CUT), CAMO_TYPES: Object.keys(CAMO),
    HEADGEAR: ['tricorne', 'bicorne', 'mitre', 'shako', 'bearskin', 'pickelhaube', 'hsh', 'kepi', 'peaked', 'sidecap', 'budenovka', 'beret',
      'brodie', 'adrian', 'm1', 'ssh40', 'm35', 'pasgt', 'modern', 'campaign', 'boonie', 'cap', 'cap8', 'ushanka', 'qing', 'papakha', 'none']
  };
})(typeof window !== 'undefined' ? window : this);
