/* 交互演示：物理墙、驾驭、两条总线播放、跑一跑。全部纯 DOM / SVG，无依赖。 */
(function () {
  'use strict';
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var D = JSON.parse($('#data').textContent);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var num = function (v, d) { return Number(v).toLocaleString('zh-CN', { maximumFractionDigits: d == null ? 0 : d }); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  /* ---------- 声音（程序合成，默认关） */
  var AC = null, sndOn = false, sndBtn = $('#snd-btn');
  function ctx() { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { AC = null; } } if (AC && AC.state === 'suspended') AC.resume(); return AC; }
  if (sndBtn) sndBtn.addEventListener('click', function () { sndOn = !sndOn; sndBtn.setAttribute('aria-pressed', String(sndOn)); sndBtn.textContent = '声音：' + (sndOn ? '开' : '关'); if (sndOn) ctx(); });
  function noise(dur, gain, lp) {
    var ac = sndOn && ctx(); if (!ac) return;
    var n = ac.sampleRate * dur, buf = ac.createBuffer(1, n, ac.sampleRate), d = buf.getChannelData(0);
    for (var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2);
    var src = ac.createBufferSource(); src.buffer = buf; var f = ac.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp || 800;
    var g = ac.createGain(); g.gain.value = gain || .5; src.connect(f); f.connect(g); g.connect(ac.destination); src.start();
  }
  function tone(freq, dur, gain, type) {
    var ac = sndOn && ctx(); if (!ac) return;
    var o = ac.createOscillator(), g = ac.createGain(); o.type = type || 'square'; o.frequency.value = freq; g.gain.value = gain || .08;
    o.connect(g); g.connect(ac.destination); o.start(); g.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + dur); o.stop(ac.currentTime + dur);
  }
  var boom = function () { noise(.5, .9, 300); };
  var spark = function () { noise(.08, .35, 4000); };
  var click = function () { tone(1800, .02, .05); };

  function hit(el) { if (!el) return; el.classList.remove('hit'); void el.offsetWidth; el.classList.add('hit'); }
  function bindSlider(id, fn) {
    var s = $('#' + id), o = $('#' + id + '-o'); if (!s) return null;
    var h = function () { if (o) o.textContent = s.value + (o.getAttribute('data-unit') || ''); fn(parseFloat(s.value)); };
    s.addEventListener('input', h); return { s: s, run: h, set: function (v) { s.value = v; h(); } };
  }
  function bindChips(root, sl) { $$('.dchips button[data-v]', root).forEach(function (b) { b.addEventListener('click', function () { sl.set(parseFloat(b.getAttribute('data-v'))); }); }); }
  function toggles(root, fn) {
    var st = {};
    $$('.dchips.tog button', root).forEach(function (b) { st[b.getAttribute('data-k')] = b.getAttribute('aria-pressed') === 'true'; b.addEventListener('click', function () { st[b.getAttribute('data-k')] = !st[b.getAttribute('data-k')]; b.setAttribute('aria-pressed', String(st[b.getAttribute('data-k')])); fn(st); }); });
    return st;
  }
  var set = function (id, t) { var e = $('#' + id); if (e) e.textContent = t; };
  var DEMO = {};

  /* ---------- 路面：镜头跟随，地面以物体速度后退；速度越高条纹越糊、流线越亮 */
  var PPM = 10; // 1 m = 10 px
  function road(el) {
    var r = { el: el, x: 0, v: 0 };
    r.step = function (dt, v) {
      r.v = v; r.x = (r.x - v * PPM * dt) % 600; var pxs = v * PPM;
      el.style.setProperty('--x', r.x.toFixed(1) + 'px');
      el.style.setProperty('--blur', clamp((pxs - 1000) / 2600, 0, .9).toFixed(2));
      el.style.setProperty('--rl', clamp(pxs / 1500, 0, 1).toFixed(2));
    };
    r.reset = function () { r.x = 0; r.step(0, 0); };
    return r;
  }
  var fmtD = function (d) { return Math.abs(d) >= 1000 ? num(d / 1000, Math.abs(d) >= 10000 ? 0 : 1) + ' km' : num(d, 0) + ' m'; };

  /* ---------- 墙 1 轮胎 */
  DEMO.tyre = function (root) {
    var wall = root.closest('.wall'), slip = $('#ty-slip'), mu = $('#ty-mu'), rd = road($('#ty-road')), t = 3, raf = null;
    var sl = bindSlider('ty-t', function (v) {
      t = v; var a = 27.78 / v, g = a / 9.81;
      set('ty-a', num(a, 1)); set('ty-g', num(g, 2)); set('ty-need', num(g, 2));
      mu.style.left = clamp(g / 3 * 100, 0, 100) + '%'; mu.classList.toggle('over', g > 1.5); mu.classList.toggle('warn', g > 1.2 && g <= 1.5);
    });
    $$('.dchips button[data-v]', root).forEach(function (b) { b.addEventListener('click', function () { sl.set(parseFloat(b.getAttribute('data-v'))); go(); }); });
    function go() {
      cancelAnimationFrame(raf); var a = 27.78 / t, over = a / 9.81 > 1.5, t0 = performance.now(), last = t0, v = 0, slipping = false;
      slip.classList.remove('on'); root.classList.remove('slipping', 'over'); rd.reset(); set('ty-v', '0');
      if (reduced) { set('ty-v', over ? '—' : '100'); if (over) { slip.classList.add('on'); root.classList.add('over'); } return; }
      noise(.25, .35, over ? 2500 : 900);
      (function step(now) {
        var dt = Math.min(.05, (now - last) / 1000), s = (now - t0) / 1000; last = now;
        if (over && s > .12 && !slipping) { slipping = true; slip.classList.add('on'); root.classList.add('slipping', 'over'); hit(wall); noise(.6, .5, 3000); }
        v = Math.min(27.78, v + (slipping ? 0.55 * 9.81 : a) * dt); // 打滑后只剩动摩擦，约 0.55 g 往前拱
        rd.step(dt, v); set('ty-v', num(v * 3.6, 0));
        if (v < 27.78 && s < 8) raf = requestAnimationFrame(step);
        else { set('ty-v', '100'); if (!over) tone(220 + 600 / t, .15, .06, 'sawtooth'); }
      })(t0);
    }
    $('#ty-go').addEventListener('click', go); sl.run();
  };

  /* ---------- 墙 2 接触网 */
  DEMO.rail = function (root) {
    var wall = root.closest('.wall'), wire = $('#rl-wire'), sp = $('#rl-spark'), T = 25, v = 300, raf = null, ph = 0;
    var vLimit = function () { return 575 * Math.sqrt(T / 40); }; // 0.7×波速：按 V150 40 kN 时 ≈575 km/h 标定，张力 25 kN 时按 √T 缩
    function draw() {
      var r = v / vLimit(), amp = Math.min(48, 3 + 4 / Math.max(.05, 1 - Math.min(r, .98) * Math.min(r, .98)));
      ph += 0.08 + r * 0.25; var d = 'M0 60';
      for (var x = 0; x <= 600; x += 10) d += ' L' + x + ' ' + (60 + Math.sin(x / 40 + ph) * amp * Math.sin(x / 600 * Math.PI));
      wire.setAttribute('d', d);
      var off = r >= 0.95; sp.classList.toggle('on', off && Math.random() > .4);
      set('rl-ratio', num(r * 0.7, 2) + ' × 波速'); set('rl-amp', num(amp, 0) + '（相对）'); set('rl-state', off ? '离线跳火、接触线被扯断的边缘' : r > .8 ? '振幅急升' : '贴线');
      root.classList.toggle('over', off);
      if (off && Math.random() > .85) { spark(); hit(wall); }
      raf = requestAnimationFrame(draw);
    }
    var sl = bindSlider('rl-v', function (x) { v = x; });
    $$('.dchips button[data-t]', root).forEach(function (b) { b.addEventListener('click', function () { T = parseFloat(b.getAttribute('data-t')); $$('.dchips button[data-t]', root).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); }); });
    sl.run(); if (!reduced) draw(); else { ph = 1; draw(); cancelAnimationFrame(raf); }
  };

  /* ---------- 墙 3 空化 */
  DEMO.water = function (root) {
    var wall = root.closest('.wall'), bub = $('#wt-bub'), foil = $('#wt-foil'), lift = $('#wt-lift'), v = 40, raf = null, bubbles = [];
    var sl = bindSlider('wt-v', function (x) {
      v = x; var kmh = v * 1.852, vs = v * 0.5144, sigma = (101325 + 1025 * 9.81 * 0.5 - 2340) / (0.5 * 1025 * vs * vs);
      set('wt-kmh', num(kmh, 0)); set('wt-sigma', vs > 0 ? num(sigma, 2) : '—');
      var cav = v > 50, st = v > 150 ? '气动升力抬艇头，三点失稳' : cav ? '空化：升力塌陷、剧烈振动' : '水翼正常';
      set('wt-state', st); root.classList.toggle('over', cav); lift.setAttribute('y2', String(cav ? 85 : 100 - Math.min(60, v))); foil.setAttribute('transform', v > 150 ? 'rotate(-12 300 100)' : '');
      if (cav) hit(wall);
    });
    function tick() {
      if (v > 50) { for (var i = 0; i < Math.min(6, (v - 50) / 10 + 1); i++) bubbles.push({ x: 240 + Math.random() * 120, y: 96, r: 1 + Math.random() * 3, vy: 0.3 + Math.random() * 1.2 }); }
      bubbles = bubbles.filter(function (b) { b.y -= b.vy; b.x += 1.5; return b.y > 72 && b.x < 600; }).slice(-160);
      bub.innerHTML = bubbles.map(function (b) { return '<circle cx="' + b.x.toFixed(1) + '" cy="' + b.y.toFixed(1) + '" r="' + b.r.toFixed(1) + '"/>'; }).join('');
      raf = requestAnimationFrame(tick);
    }
    bindChips(root, sl); sl.run(); if (!reduced) tick();
  };

  /* ---------- 墙 4 音障 / 热障 */
  DEMO.air = function (root) {
    var wall = root.closest('.wall'), cone = $('#ar-cone'), boomEl = $('#ar-boom'), nose = $('#ar-nose'), was = 0.85;
    var sl = bindSlider('ar-m', function (m) {
      var kmh = m * 1225, T = 216.65 * (1 + 0.2 * m * m) - 273.15;
      set('ar-kmh', num(kmh, 0)); set('ar-temp', num(T, 0));
      set('ar-mat', T < 120 ? '铝合金' : T < 300 ? '钛合金（SR-71 约 300 °C）' : T < 650 ? 'Inconel X 镍合金 + 热沉（X-15）' : '烧蚀涂层 / 没有金属能长期扛住');
      if (m >= 1) { var th = Math.asin(1 / m), dx = 200 * Math.cos(th), dy = 200 * Math.sin(th); cone.style.display = ''; $$('line', cone)[0].setAttribute('x2', 300 - dx); $$('line', cone)[0].setAttribute('y2', 80 - dy); $$('line', cone)[1].setAttribute('x2', 300 - dx); $$('line', cone)[1].setAttribute('y2', 80 + dy); } else cone.style.display = 'none';
      var heat = clamp((T - 50) / 900, 0, 1); nose.style.fill = 'rgb(' + Math.round(241 - 20 * heat) + ',' + Math.round(239 - 170 * heat) + ',' + Math.round(232 - 200 * heat) + ')'; root.style.setProperty('--heat', heat);
      if (was < 1 && m >= 1) { boomEl.classList.remove('on'); void boomEl.offsetWidth; boomEl.classList.add('on'); boom(); hit(wall); }
      root.classList.toggle('over', T > 650); was = m;
    });
    bindChips(root, sl); sl.run();
  };

  /* ---------- 墙 5 黑视 */
  DEMO.g = function (root) {
    var stage = $('#g-stage'), n = $('#g-n');
    var sl = bindSlider('g-s', function (g) {
      set('g-v', num(g, 1)); n.style.left = clamp(Math.log10(1 + g) / Math.log10(51) * 100, 0, 100) + '%';
      var note = g < 1.5 ? '站着不动，或者家用车正常加速。' : g < 3 ? '过弯、起步：身体被按进座椅。' : g < 4.5 ? '视野边缘开始发灰（灰视）：血被甩向下半身。' : g < 6.5 ? '不穿抗荷服几秒内黑视；Apollo 10 再入峰值 6.78 g。' : g < 10 ? '战机极限 9 g：抗荷服 + 加压呼吸 + 肌肉对抗，也只能撑十几秒。' : g < 25 ? '只有瞬间能活：撞车、弹射座椅的量级。' : 'Stapp 1954-12-10 的峰值：1.4 秒从 1,017 km/h 刹停，暂时失明、肋骨骨折。';
      set('g-note', note); var dark = clamp((g - 3) / 6, 0, .92); stage.style.setProperty('--vig', dark); root.classList.toggle('over', g > 9);
    });
    bindChips(root, sl); sl.run();
  };

  /* ---------- 墙 6 光速 */
  DEMO.light = function (root) {
    var h1 = $('#lt-h1'), h2 = $('#lt-h2'), eb = $('#lt-e'), beta = 0.0006, raf = null, a1 = 0, a2 = 0, last = 0;
    var sl = bindSlider('lt-v', function (b) {
      beta = b; var gam = 1 / Math.sqrt(1 - b * b);
      set('lt-kmh', num(b * 1079252849, 0)); set('lt-gamma', gam < 1.001 ? gam.toFixed(6) : num(gam, 3)); set('lt-year', gam < 1.001 ? '1 年零 ' + num((gam - 1) * 365.25 * 86400, 1) + ' 秒' : num(gam, 2) + ' 年');
      eb.style.width = clamp((gam - 1) / 22 * 100, 0.5, 100) + '%'; root.classList.toggle('over', b > 0.99);
    });
    function tick(t) { var dt = last ? (t - last) / 1000 : 0; last = t; var gam = 1 / Math.sqrt(1 - beta * beta); a1 += dt * 60; a2 += dt * 60 / gam; h1.setAttribute('transform', 'rotate(' + a1 + ' 50 50)'); h2.setAttribute('transform', 'rotate(' + a2 + ' 50 50)'); raf = requestAnimationFrame(tick); }
    bindChips(root, sl); sl.run(); if (!reduced) requestAnimationFrame(tick);
  };

  /* ---------- 驾驭 · Roadster */
  DEMO.roadster = function (root) {
    var W = 1700, S = 4700, Tn = 80000 / 9.81; // kg 等效
    var st = toggles(root, upd); var world = $('#rd-world');
    function upd() {
      var suction = st.suction, thrust = st.thrust, flip = st.flip;
      $('#rd-s').style.display = suction ? '' : 'none'; $('#rd-t').style.display = thrust ? '' : 'none';
      var N = (flip ? -W : W) + (suction ? S : 0); // 对轮胎的正压力（kg 等效）
      world.setAttribute('transform', flip ? 'rotate(180 300 120)' : '');
      var grip = Math.max(0, N) * 1.1; var acc = (grip + (thrust ? Tn : 0)) / W; // g
      set('rd-n', (N / W).toFixed(2) + ' ×'); set('rd-acc', num(acc, 2) + ' g');
      var falls = flip && N <= 0; set('rd-state', falls ? '掉下来：吸附力不够抵消重力' : flip ? '倒置贴面（宣称值下吸附 > 重力）' : thrust && !suction ? '推力直接加速；Electrek：若喷口向上，会减少轮胎正压力' : '贴地');
      root.classList.toggle('over', falls); $('#rd-gt').textContent = '轮胎抓地 ∝ 正压力 ' + (N / W).toFixed(1) + '×'; if (falls) hit(root.closest('.hcard'));
    }
    upd();
  };
  /* ---------- X-15 */
  DEMO.x15 = function (root) {
    var sl = bindSlider('x15-h', function (h) {
      var rho = Math.exp(-h / 7.2); var aero = clamp(rho * 100, 0, 100);
      $('#x15-aero').style.width = aero + '%'; $('#x15-rcs').style.width = '100%';
      set('x15-rho', rho < 0.001 ? rho.toExponential(1) : num(rho, 3)); set('x15-who', h >= 30 ? '反作用小火箭（舵面推不动空气）' : h >= 20 ? '两者并用' : '气动舵面');
      root.classList.toggle('over', h >= 30);
    });
    bindChips(root, sl); sl.run();
  };
  /* ---------- Apollo */
  DEMO.apollo = function (root) {
    var sl = bindSlider('ap-r', function (r) {
      $('#ap-l').style.transform = 'rotate(' + r + 'deg)'; var c = Math.cos(r * Math.PI / 180);
      set('ap-dir', r < 30 ? '向上（抬升）' : r < 150 ? '侧向（转向）' : '向下（压入大气）'); set('ap-g', c > .5 ? '降低，再入更长更缓' : c < -.5 ? '升高，再入更短更猛' : '居中'); set('ap-range', c > .5 ? '延长 / 可跳出再进' : c < -.5 ? '缩短' : '—');
    });
    sl.run();
  };
  /* ---------- 三点式 */
  DEMO.hydro = function (root) {
    var boat = $('#hy-boat');
    var sl = bindSlider('hy-a', function (a) {
      var lift = Math.pow(a / 5.5, 2); boat.style.transform = 'rotate(' + (-a * 2) + 'deg)';
      set('hy-lift', num(lift, 2)); var over = a > 5.5; set('hy-state', over ? '艇头抬起，翻' : a > 4.5 ? '接近临界' : '三点贴水');
      root.classList.toggle('over', over); if (over) hit(root.closest('.hcard'));
    });
    bindChips(root, sl); sl.run();
  };
  /* ---------- 地面效应 */
  DEMO.ground = function (root) {
    var body = $('#gr-body'), h = 50, st = toggles(root, upd), raf = null, t0 = performance.now();
    var sl = bindSlider('gr-h', function (v) { h = v; upd(); });
    function upd() {
      var hh = h; if (st.bump && !st.active) hh = h + Math.sin((performance.now() - t0) / 120) * 18;
      hh = clamp(hh, 0, 90); var df = hh <= 2 ? 0 : clamp(1.2 * 40 / hh, 0, 4);
      body.setAttribute('y', String(124 - hh * 0.9 - 22)); $('#gr-dft').textContent = '下压力 ' + num(df, 2) + '× 车重'; $$('#gr-df line')[0].setAttribute('y2', String(108 + df * 12));
      set('gr-val', num(df, 2) + ' ×'); var stall = hh <= 2; set('gr-state', stall ? '车底触地，下压力瞬间归零（1982 年前的「海豚跳」）' : st.active ? '主动悬架锁定间隙，下压力稳定' : st.bump ? '随路面起伏，下压力忽大忽小' : '稳定');
      root.classList.toggle('over', stall || (st.bump && !st.active && h < 30));
      if (st.bump && !st.active) raf = requestAnimationFrame(upd);
    }
    sl.run();
  };
  /* ---------- ABS */
  DEMO.abs = function (root) {
    var car = $('#ab-car'), wh = $('#ab-wheel'), btn = $('#ab-brake'), st = toggles(root, function () {}), v = 100, w = 100, x = 0, raf = null, down = false, last = 0, tick = 0;
    function reset() { v = 100; w = 100; x = 0; draw(); }
    function draw() { car.style.width = v + '%'; wh.style.width = w + '%'; set('ab-dist', num(x, 0)); }
    function loop(t) {
      var dt = last ? Math.min(.05, (t - last) / 1000) : 0; last = t;
      if (down && v > 0) {
        if (st.abs) { tick += dt; var phase = Math.floor(tick * 40) % 2; w = phase ? v : v * 0.6; v -= 9.5 * dt * 3.6 * 0.9; if (phase === 0 && Math.floor(tick * 40) !== Math.floor((tick - dt) * 40)) click(); set('ab-state', 'ABS 每秒 40 次松开再抓住，轮子一直在转'); }
        else { w = Math.max(0, w - 400 * dt); v -= 9.5 * dt * 3.6 * (w > 5 ? 0.9 : 0.6); set('ab-state', '轮子抱死：滑动摩擦更小，还不能转向'); root.classList.add('over'); }
        x += (v / 3.6) * dt; v = Math.max(0, v); draw();
        if (v <= 0) { set('ab-note', '刹停。' + (st.abs ? '' : '没有 ABS，距离更长、方向锁死。')); }
      }
      raf = requestAnimationFrame(loop);
    }
    var press = function (e) { e.preventDefault(); if (v <= 0) reset(); down = true; root.classList.remove('over'); set('ab-note', '刹车中…'); };
    var rel = function () { down = false; };
    btn.addEventListener('pointerdown', press); btn.addEventListener('pointerup', rel); btn.addEventListener('pointerleave', rel); btn.addEventListener('pointercancel', rel);
    reset(); set('ab-state', '—'); requestAnimationFrame(loop);
  };
  /* ---------- 放宽静稳定 */
  DEMO.relaxed = function (root) {
    var n = $('#rx-n'), st = toggles(root, function () {}), dev = 0, last = 0, acc = 0;
    function loop(t) {
      var dt = last ? Math.min(.05, (t - last) / 1000) : 0; last = t; acc += dt;
      if (st.fbw) { if (acc >= 1 / 40) { acc = 0; dev *= 0.55; } dev += (Math.random() - .5) * 0.4; }
      else dev *= Math.pow(2, dt / 0.12);
      dev = clamp(dev, -60, 60); n.style.transform = 'rotate(' + dev + 'deg)';
      var lost = Math.abs(dev) >= 60; set('rx-dev', num(dev, 1) + '°'); set('rx-state', lost ? '失控——「没有任何人类操作者能把它稳住」' : st.fbw ? '计算机每秒 40 次拉回' : '发散中：每 0.12 s 翻倍');
      root.classList.toggle('over', lost); requestAnimationFrame(loop);
    }
    $('#rx-kick').addEventListener('click', function () { dev += (Math.random() > .5 ? 1 : -1) * 6; });
    requestAnimationFrame(loop);
  };
  /* ---------- SR-71 unstart */
  DEMO.unstart = function (root) {
    var spike = $('#us-spike'), nac = $('#us-nac'), m = 2, busy = false;
    var sl = bindSlider('us-m', function (v) { m = v; var pos = clamp((m - 1.6) / 1.7 * 26, 0, 26); spike.setAttribute('transform', 'translate(' + (pos * 3) + ' 0)'); set('us-pos', num(pos, 1) + ' in'); if (!busy) set('us-state', m > 2.5 ? '激波收在唇口：巡航' : '亚临界'); });
    $('#us-go').addEventListener('click', function () {
      if (busy) return; busy = true; root.classList.add('over'); set('us-state', 'unstart：激波弹出，推力骤降，机头甩偏——飞行员的头盔撞到座舱盖'); noise(.6, .7, 500); hit(root.closest('.hcard'));
      var t0 = performance.now(); (function shake(t) { var p = (t - t0) / 900; if (p < 1) { nac.setAttribute('transform', 'translate(' + Math.sin(t / 18) * 18 * (1 - p) + ' ' + Math.sin(t / 23) * 6 * (1 - p) + ')'); requestAnimationFrame(shake); } else { nac.setAttribute('transform', ''); busy = false; root.classList.remove('over'); set('us-state', '自动重启：进气锥前推、旁通门打开，再重新收激波'); } })(t0);
    });
    sl.run();
  };
  /* ---------- 磁浮间隙 */
  DEMO.gap = function (root) {
    var body = $('#gp-body'), line = $('#gp-line'), st = toggles(root, function () {}), gap = 10, vel = 0, last = 0, lost = false;
    function loop(t) {
      var dt = last ? Math.min(.04, (t - last) / 1000) : 0; last = t;
      if (!lost) {
        var force = -40 / (gap * gap) * 100 + 40; // 吸力随间隙变小而增大（不稳定）
        if (st.ctl) force += (10 - gap) * 180 - vel * 20; // 控制器
        vel += force * dt; gap += vel * dt;
        if (gap <= 1 || gap >= 30) { lost = true; root.classList.add('over'); set('gp-state', gap <= 1 ? '吸死在轨道上' : '掉下来'); hit(root.closest('.hcard')); }
      }
      gap = clamp(gap, 1, 30); body.setAttribute('y', String(110 - gap * 2 - 30)); line.setAttribute('y1', String(110 - gap * 2)); $('#gp-t').textContent = '间隙 ' + num(gap, 1) + ' mm';
      set('gp-v', num(gap, 2)); if (!lost) set('gp-state', st.ctl ? '控制器把间隙钉在 10 mm' : '没有控制：偏一点就一路偏下去');
      requestAnimationFrame(loop);
    }
    $('#gp-kick').addEventListener('click', function () { if (lost) { lost = false; gap = 10; vel = 0; root.classList.remove('over'); } vel += (Math.random() > .5 ? 1 : -1) * 25; });
    requestAnimationFrame(loop);
  };
  /* ---------- 协和配平 */
  DEMO.cg = function (root) {
    var cp = $('#cg-cp'), cg = $('#cg-cg'), st = toggles(root, upd), m = 0.9;
    var sl = bindSlider('cg-m', function (v) { m = v; upd(); });
    function upd() {
      var shift = clamp((m - 0.9) / 1.14, 0, 1) * 120; var cgx = st.pump ? shift * 0.95 : 0;
      cp.setAttribute('transform', 'translate(' + shift + ' 0)'); cg.setAttribute('transform', 'translate(' + cgx + ' 0)');
      var gap = shift - cgx; set('cg-gap', num(gap / 120 * 100, 0) + '%'); var bad = gap > 30; set('cg-state', bad ? '机头下栽，只能用升降舵硬顶，阻力大增' : m > 1 ? '泵油把质心追上压心' : '亚音速，无需配平');
      root.classList.toggle('over', bad);
    }
    sl.run();
  };

  $$('.demo[data-demo]').forEach(function (el) { var k = el.getAttribute('data-demo'); if (DEMO[k]) { try { DEMO[k](el); } catch (e) { console.error(k, e); } } });

  /* 第三章「两条线」的播放与拖动在 app.js（v2 改为按实际宽度现画的主图） */

  /* ---------- 反例小图 */
  $$('.ctile').forEach(function (t) {
    var k = t.getAttribute('data-kind'), v = parseFloat(t.getAttribute('data-v')), mx = parseFloat(t.getAttribute('data-max'));
    var run = function () {
      if (k === 'bar') $('.cvis b', t).style.width = (v / mx * 100) + '%';
      if (k === 'gauge') $('.cvis .cn', t).style.transform = 'rotate(' + (-90 + v / mx * 180) + 'deg)';
      if (k === 'launch') { var d = $('.cvis .dot', t); d.style.transition = 'left ' + v + 's cubic-bezier(.3,0,.7,1)'; d.style.left = '100%'; }
      if (k === 'mach') { $('.cvis b', t).style.left = (v / mx * 100) + '%'; $('.cvis span', t).style.left = (1 / mx * 100) + '%'; }
    };
    if ('IntersectionObserver' in window) { var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { run(); io.unobserve(t); } }); }, { threshold: .5 }); io.observe(t); } else run();
  });

  /* ---------- 跑一跑 · 比速度：镜头钉在你身上 */
  (function () {
    var root = $('.demo.race'); if (!root) return;
    var REF = { walk: 5, bolt: 44.72, hsr: 350, air: 900, snd: 1225 }, NAME = { walk: '步行', bolt: '博尔特', hsr: '高铁', air: '客机', snd: '音速' };
    var TOP = { walk: 13, bolt: 31, you: 50, hsr: 67, air: 82, snd: 94 }, el = $('#rc-road'), rd = road(el), lanes = {}, raf = null, tab = $('#rc-tab');
    $$('.rl', root).forEach(function (l) { var k = l.getAttribute('data-k'); lanes[k] = l; l.style.setProperty('--t', TOP[k]); });
    function place(k, dk) { // dk：与你的距离差（m）
      var W = el.clientWidth, x = W * .3 + dk * PPM, l = lanes[k], dot = $('.rdot', l), c = clamp(x, 12, W - 12);
      dot.style.left = c + 'px'; l.classList.toggle('lead', x > W - 12); l.classList.toggle('lag', x < 12);
      if (x > W - 12 || x < 12) dot.setAttribute('data-gap', NAME[k] + ' ' + (dk > 0 ? '领先 ' : '落后 ') + fmtD(Math.abs(dk)));
    }
    function go() {
      cancelAnimationFrame(raf); var v = parseFloat($('#rc-v').value) * parseFloat($('#rc-u').value); if (!(v >= 0)) return;
      var vy = v / 3.6, t0 = performance.now(), last = t0; rd.reset(); tab.innerHTML = '';
      Object.keys(REF).forEach(function (k) { place(k, 0); });
      raf = raf || 1;
      function finish(s) {
        var dy = vy * s, h = D.tool1.bjsh / Math.max(v, 1e-6);
        var html = '<div class="you"><b>' + fmtD(dy) + '</b><i>你 ' + num(s, 0) + ' 秒跑的距离</i><i>北京→上海 ' + (h >= 1 ? num(h, 1) + ' 小时' : num(h * 60, 1) + ' 分钟') + '</i></div>';
        Object.keys(REF).forEach(function (k) { var r = v / REF[k]; html += '<div><b>' + fmtD(REF[k] / 3.6 * s) + '</b><i>' + NAME[k] + ' ' + num(REF[k], 0) + ' km/h</i><i>' + (r >= 1 ? '你是它的 ' + num(r, r >= 10 ? 0 : 1) + ' 倍' : '它是你的 ' + num(1 / r, 1 / r >= 10 ? 0 : 1) + ' 倍') + '</i></div>'; });
        tab.innerHTML = html;
      }
      if (reduced) { rd.step(0, vy); Object.keys(REF).forEach(function (k) { place(k, (REF[k] / 3.6 - vy) * 10); }); set('rc-t', '10.0'); set('rc-d', fmtD(vy * 10)); finish(10); return; }
      noise(.5, clamp(v / 1200, .15, .6), 600 + v * 2);
      (function step(now) {
        var dt = Math.min(.05, (now - last) / 1000), s = clamp((now - t0) / 1000, 0, 10); last = now;
        rd.step(dt, vy); set('rc-t', num(s, 1)); set('rc-d', fmtD(vy * s));
        Object.keys(REF).forEach(function (k) { place(k, (REF[k] / 3.6 - vy) * s); });
        if (s < 10) raf = requestAnimationFrame(step); else { raf = null; finish(10); }
      })(t0);
    }
    $('#rc-go').addEventListener('click', go); $('#rc-v').addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
    function grid() { var W = el.clientWidth; Object.keys(REF).forEach(function (k, i) { var l = lanes[k]; l.classList.remove('lead', 'lag'); $('.rdot', l).style.left = Math.max(14, W * .3 - (i + 1) * 16) + 'px'; }); }
    grid(); window.addEventListener('resize', function () { if (!raf) grid(); });
  })();

  /* ---------- 跑一跑 · 比起步：表盘扫到目标速度为止 */
  (function () {
    var root = $('.demo.drag'); if (!root) return;
    var raf = null, R = { a: road($('#dg-ar')), b: road($('#dg-br')) }, sum = $('#dg-sum'), base = sum.textContent;
    function parse(sel) { var p = sel.value.split('|'); var vt = { '0–100': 100, '0–60 mph': 96.56, '0–48': 48, '0–350': 350 }[p[1]] || 100; return { t: parseFloat(p[0]), vt: vt, n: sel.options[sel.selectedIndex].text + ' · ' + p[1] + (p[1].indexOf('mph') < 0 ? ' km/h' : '') }; }
    function go() {
      cancelAnimationFrame(raf); var C = { a: parse($('#dg-a')), b: parse($('#dg-b')) }, scale = Math.max(1, Math.max(C.a.t, C.b.t) / 10), t0 = performance.now(), last = t0, done = {};
      sum.textContent = (scale > 1 ? '时间 ×' + num(scale, 0) + ' 快进。' : '') + base;
      ['a', 'b'].forEach(function (i) { set('dg-' + i + 'n', C[i].n); R[i].reset(); $('#dg-' + i + 't').parentNode.classList.remove('done'); });
      function draw(i, s) {
        var c = C[i], a = c.vt / 3.6 / c.t, v = Math.min(c.vt / 3.6, a * s), fin = s >= c.t, lane = $('#dg-' + i + 'r').parentNode;
        $('#dg-' + i + 'nd').style.transform = 'rotate(' + (-90 + v / (c.vt / 3.6) * 180) + 'deg)'; set('dg-' + i + 'v', num(v * 3.6, 0));
        set('dg-' + i + 't', num(fin ? c.t : s, c.t > 30 ? 1 : 2)); set('dg-' + i + 'g', fin ? '到 ' + num(c.vt, 0) + ' km/h' : '推背 ' + num(a / 9.81, 2) + ' g');
        lane.classList.toggle('push', !fin); $('#dg-' + i + 't').parentNode.classList.toggle('done', fin);
        if (fin && !done[i]) { done[i] = true; tone(160 + 500 / c.t, .2, .06, 'sawtooth'); }
        return v;
      }
      if (reduced) { ['a', 'b'].forEach(function (i) { draw(i, C[i].t); R[i].step(0, C[i].vt / 3.6); }); return; }
      noise(.35, .4, 1500);
      (function step(now) {
        var dt = Math.min(.05, (now - last) / 1000) * scale, s = (now - t0) / 1000 * scale; last = now;
        ['a', 'b'].forEach(function (i) { R[i].step(dt, draw(i, s)); });
        if (!(done.a && done.b)) raf = requestAnimationFrame(step);
      })(t0);
    }
    $('#dg-go').addEventListener('click', go); $('#dg-b').selectedIndex = 4;
    ['a', 'b'].forEach(function (i) { set('dg-' + i + 'n', parse($('#dg-' + i)).n); });
  })();
})();
