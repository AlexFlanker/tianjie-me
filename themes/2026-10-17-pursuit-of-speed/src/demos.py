# -*- coding: utf-8 -*-
"""交互演示的 HTML 骨架。逻辑在 demos.js（按 data-demo 绑定）。所有图形都是抽象的几何（线、点、箭头、仪表），不画载具外形。"""
import html
def esc(s): return html.escape(str(s), quote=True)

def slider(id_, label, mn, mx, step, val, unit=''):
    return f'<label class="dsl"><span>{esc(label)}</span><input type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}"><output for="{id_}" id="{id_}-o">{val}{esc(unit)}</output></label>'

def chips(items, attr='data-v'):
    return '<div class="dchips">' + ''.join(f'<button type="button" {attr}="{v}">{esc(n)}</button>' for n, v in items) + '</div>'

def readouts(items):
    return '<div class="dread">' + ''.join(f'<div><b id="{i}">—</b><span>{esc(l)}</span></div>' for i, l in items) + '</div>'

# ---------- 物理墙
def wall_tyre():
    return f'''<div class="demo" data-demo="tyre">
<div class="dstage"><div class="strip"><i class="lane"></i><b class="dot" id="ty-dot"></b><span class="mk" style="left:0">0</span><span class="mk" style="right:0">100 km/h</span><em class="slip" id="ty-slip">打滑</em></div>
<div class="mu"><i style="--a:0;--b:1.2" class="z1">量产胎 μ≈1.0–1.2</i><i style="--a:1.2;--b:1.5" class="z2">赛道胶 / 半热熔</i><i style="--a:1.5;--b:3" class="z3">轮胎做不到</i><b class="needle" id="ty-mu"></b></div></div>
{slider('ty-t', '0–100 km/h 用时', 0.5, 6, 0.01, 3, ' s')}
{chips([('GB 7258 默认 5 s', 5), ('SU7 Max 宣称 2.78', 2.78), ('Plaid 1.99（0–60）', 1.99), ('Nevera 1.74（0–60）', 1.74), ('Roadster 宣称 0.81（0–60）', 0.81)])}
{readouts([('ty-a', '平均加速度 m/s²'), ('ty-g', '平均 g'), ('ty-need', '需要的 μ')])}
<button type="button" class="dgo" id="ty-go">起步</button></div>'''

def wall_rail():
    return f'''<div class="demo" data-demo="rail">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160" id="rl-svg"><path class="wire" id="rl-wire" d="M0 60 L600 60"/><rect class="pan" x="285" y="100" width="30" height="8"/><line class="panarm" x1="300" y1="108" x2="300" y2="140"/><g id="rl-spark" class="spark"><circle cx="300" cy="60" r="6"/><circle cx="300" cy="60" r="14"/></g><text class="dt" x="8" y="150">示意：接触线振幅随 v / 波速 增大，接近 0.7 倍波速时离线跳火</text></svg></div>
{slider('rl-v', '列车速度', 0, 650, 5, 300, ' km/h')}
<div class="dchips"><button type="button" data-t="25" aria-pressed="true">标准接触网 25 kN</button><button type="button" data-t="40">V150 加张到 40 kN</button></div>
{readouts([('rl-ratio', 'v / 波速'), ('rl-amp', '接触线振幅（示意）'), ('rl-state', '受电弓状态')])}</div>'''

def wall_water():
    return f'''<div class="demo" data-demo="water">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160" id="wt-svg"><rect class="sea" x="0" y="70" width="600" height="90"/><g id="wt-bub"></g><path class="foil" id="wt-foil" d="M240 100 Q300 80 360 100 Q300 112 240 100Z"/><line class="lift" id="wt-lift" x1="300" y1="100" x2="300" y2="40"/><text class="dt" x="8" y="150">示意：水翼上表面压力低于蒸汽压就起泡（空化），升力塌陷</text></svg></div>
{slider('wt-v', '艇速', 0, 300, 1, 40, ' 节')}
{chips([('Sailrocket 2 · 65.45 节', 65.45), ('K7 · 1967 翻艇', 160), ('Spirit of Australia · 276 节', 275.97)])}
{readouts([('wt-kmh', 'km/h'), ('wt-sigma', '空化数 σ（示意）'), ('wt-state', '状态')])}</div>'''

def wall_air():
    return f'''<div class="demo" data-demo="air">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160" id="ar-svg"><g id="ar-cone"><line class="shock" x1="300" y1="80" x2="100" y2="20"/><line class="shock" x1="300" y1="80" x2="100" y2="140"/></g><circle class="nose" id="ar-nose" cx="300" cy="80" r="7"/><circle class="boom" id="ar-boom" cx="300" cy="80" r="0"/><text class="dt" x="8" y="150">示意：马赫锥 sin θ = 1/M；驻点温度 T₀ = T·(1 + 0.2·M²)</text></svg></div>
{slider('ar-m', '马赫数', 0.3, 7, 0.01, 0.85, '')}
{chips([('客机 0.85', 0.85), ('X-1 1.06', 1.06), ('协和 2.04', 2.04), ('SR-71 3.2', 3.2), ('X-15 6.7', 6.7)])}
{readouts([('ar-kmh', 'km/h（海平面音速）'), ('ar-temp', '驻点温度 °C（11 km 高空，−56 °C）'), ('ar-mat', '扛得住的材料')])}</div>'''

def wall_g():
    return f'''<div class="demo" data-demo="g">
<div class="dstage gstage" id="g-stage"><div class="gbar"><i class="z" style="--a:0;--b:2">过弯 2 g</i><i class="z" style="--a:2;--b:4.5">4–5 g 灰视</i><i class="z" style="--a:4.5;--b:9">黑视 · 抗荷服 9 g</i><i class="z" style="--a:9;--b:50">火箭滑车 46.2 g</i><b class="needle" id="g-n"></b></div><div class="gnum"><b id="g-v">1.0</b><span>g</span></div><div class="gnote" id="g-note">站着不动。</div></div>
{slider('g-s', '过载', 0, 46.2, 0.1, 1, ' g')}
{chips([('F1 急弯 5 g', 5), ('战机 9 g', 9), ('Apollo 10 再入 6.78 g', 6.78), ('Stapp 1954 峰值 46.2 g', 46.2)])}</div>'''

def wall_light():
    return f'''<div class="demo" data-demo="light">
<div class="dstage"><div class="clocks"><div class="clk"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46"/><line id="lt-h1" x1="50" y1="50" x2="50" y2="12"/></svg><span>地球上的钟</span></div><div class="clk"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46"/><line id="lt-h2" x1="50" y1="50" x2="50" y2="12"/></svg><span>飞船上的钟</span></div><div class="ebar"><span>推到这个速度要的能量（相对静止质量，示意）</span><i><b id="lt-e"></b></i></div></div></div>
{slider('lt-v', '速度 / 光速', 0, 0.999, 0.001, 0.0006, '')}
{chips([('帕克探测器 0.00064 c', 0.00064), ('0.5 c', 0.5), ('0.9 c', 0.9), ('0.99 c', 0.99), ('0.999 c', 0.999)])}
{readouts([('lt-kmh', 'km/h'), ('lt-gamma', 'γ（时间慢多少倍）'), ('lt-year', '飞船过一年，地球过')])}</div>'''

# ---------- 驾驭
def h_roadster():
    return f'''<div class="demo" data-demo="roadster">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 200" id="rd-svg"><g id="rd-world"><rect class="ground" x="40" y="140" width="520" height="6"/><rect class="body" id="rd-body" x="230" y="100" width="140" height="36" rx="6"/><g class="arrow" id="rd-w"><line x1="300" y1="118" x2="300" y2="172"/><text x="306" y="172">重力 ≈ 1,700 kg</text></g><g class="arrow a" id="rd-s"><line x1="260" y1="100" x2="260" y2="60"/><line x1="340" y1="100" x2="340" y2="60"/><text x="346" y="64">吸附（宣称 4,700 kg）</text></g><g class="arrow a" id="rd-t"><line x1="230" y1="118" x2="150" y2="118"/><text x="60" y="110">冷气推进 80 kN →</text></g><g class="arrow" id="rd-g"><line x1="300" y1="146" x2="300" y2="190"/><text x="306" y="190" id="rd-gt">轮胎抓地</text></g></g><text class="dt" x="8" y="18">示意图，力的大小按宣称值等比</text></svg></div>
<div class="dchips tog"><button type="button" data-k="suction">风扇吸附</button><button type="button" data-k="thrust">冷气推进器</button><button type="button" data-k="flip">倒置</button></div>
{readouts([('rd-n', '轮胎正压力（×车重）'), ('rd-acc', '可用加速度（g，示意）'), ('rd-state', '状态')])}</div>'''

def h_x15():
    return f'''<div class="demo" data-demo="x15">
<div class="dstage"><div class="bars2"><div><span>气动舵面的权威（∝ 空气密度）</span><i><b id="x15-aero"></b></i></div><div><span>反作用小火箭（不依赖空气）</span><i><b id="x15-rcs"></b></i></div></div></div>
{slider('x15-h', '高度', 0, 110, 1, 20, ' km')}
{chips([('客机 11 km', 11), ('SR-71 26 km', 26), ('X-15 舵面失效 ≈30 km', 30), ('X-15 最高 108 km', 108)])}
{readouts([('x15-rho', '空气密度（海平面 = 1）'), ('x15-who', '谁在控姿态')])}</div>'''

def h_apollo():
    return f'''<div class="demo" data-demo="apollo">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 200"><circle class="cap" cx="300" cy="110" r="34"/><g id="ap-l" class="arrow a" style="transform-origin:300px 110px"><line x1="300" y1="110" x2="300" y2="30"/><text x="306" y="34">升力</text></g><line class="vel" x1="120" y1="110" x2="260" y2="110"/><text class="dt" x="120" y="100">来流 39,897 km/h →</text><text class="dt" x="8" y="190">升力大小改不了（质心偏置是固定的），只能滚转舱体改方向</text></svg></div>
{slider('ap-r', '滚转角', 0, 180, 1, 0, '°')}
{readouts([('ap-dir', '升力方向'), ('ap-g', '过载趋势'), ('ap-range', '航程趋势')])}</div>'''

def h_hydro():
    return f'''<div class="demo" data-demo="hydro">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160"><rect class="sea" x="0" y="110" width="600" height="50"/><g id="hy-boat" style="transform-origin:300px 104px"><line class="hull" x1="180" y1="104" x2="420" y2="104"/><circle class="pt3" cx="200" cy="106" r="5"/><circle class="pt3" cx="400" cy="106" r="5"/><circle class="pt3" cx="300" cy="106" r="5"/></g><text class="dt" x="8" y="150">示意：三点触水；攻角超过安全值，气动升力把艇头抬起来</text></svg></div>
{slider('hy-a', '艇体攻角', 0, 9, 0.1, 3, '°')}
{chips([('设计攻角 ~3°', 3), ('K7 1967 临界 ~5.5°', 5.5), ('翻', 7)])}
{readouts([('hy-lift', '气动升力 / 重力（示意）'), ('hy-state', '状态')])}</div>'''

def h_ground():
    return f'''<div class="demo" data-demo="ground">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160"><rect class="ground" x="40" y="130" width="520" height="6"/><rect class="body" id="gr-body" x="200" y="86" width="200" height="22" rx="4"/><g id="gr-df" class="arrow a"><line x1="300" y1="108" x2="300" y2="128"/><text x="306" y="124" id="gr-dft">下压力</text></g><text class="dt" x="8" y="150">示意：离地间隙越小，车底「翼」的下压力越大——直到车底碰地，一下全没了</text></svg></div>
{slider('gr-h', '离地间隙', 10, 80, 1, 50, ' mm')}
<div class="dchips tog"><button type="button" data-k="active">1992 主动悬架（锁定间隙）</button><button type="button" data-k="bump">颠簸路面</button></div>
{readouts([('gr-val', '下压力（示意，×车重）'), ('gr-state', '状态')])}</div>'''

def h_abs():
    return f'''<div class="demo" data-demo="abs">
<div class="dstage"><div class="bars2"><div><span>车速</span><i><b id="ab-car"></b></i></div><div><span>轮速</span><i><b id="ab-wheel"></b></i></div></div><div class="gnote" id="ab-note">按住「刹车」。</div></div>
<div class="dchips tog"><button type="button" data-k="abs" aria-pressed="true">ABS（每秒最多 40 次）</button></div>
<button type="button" class="dgo hold" id="ab-brake">按住刹车</button>
{readouts([('ab-dist', '刹停距离（示意，m）'), ('ab-state', '轮胎状态')])}</div>'''

def h_relaxed():
    return f'''<div class="demo" data-demo="relaxed">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160"><line class="ln" x1="300" y1="20" x2="300" y2="140"/><g id="rx-n" style="transform-origin:300px 130px"><line class="needle2" x1="300" y1="130" x2="300" y2="30"/></g><text class="dt" x="8" y="150">示意：静不稳定——偏离越大，翻得越快（振幅每 0.12 s 翻倍）；计算机每秒修正 40 次</text></svg></div>
<div class="dchips tog"><button type="button" data-k="fbw" aria-pressed="true">飞控计算机</button></div>
<button type="button" class="dgo" id="rx-kick">扰动一下</button>
{readouts([('rx-dev', '偏离'), ('rx-state', '状态')])}</div>'''

def h_unstart():
    return f'''<div class="demo" data-demo="unstart">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160" id="us-svg"><g id="us-nac"><path class="inlet" d="M160 50 L440 50 L440 110 L160 110"/><polygon class="spike" id="us-spike" points="120,80 200,56 200,104"/><line class="shock2" id="us-shock" x1="200" y1="56" x2="160" y2="50"/><line class="shock2" id="us-shock2" x1="200" y1="104" x2="160" y2="110"/></g><text class="dt" x="8" y="150">示意：进气锥随马赫数后退，把激波收在唇口；激波跑出去 = unstart，推力骤降、机头甩向一侧</text></svg></div>
{slider('us-m', '马赫数', 1.6, 3.3, 0.01, 2.0, '')}
<button type="button" class="dgo" id="us-go">触发 unstart</button>
{readouts([('us-pos', '进气锥位置（后退 in）'), ('us-state', '状态')])}</div>'''

def h_gap():
    return f'''<div class="demo" data-demo="gap">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160"><rect class="ground" x="60" y="110" width="480" height="8"/><rect class="body" id="gp-body" x="150" y="60" width="300" height="30" rx="4"/><line class="gapline" id="gp-line" x1="300" y1="90" x2="300" y2="110"/><text class="dt" id="gp-t" x="310" y="104">间隙 10 mm</text><text class="dt" x="8" y="150">示意：电磁吸力随间隙变小而变大（天然不稳定），控制器不停地改电流把间隙钉在 10 mm</text></svg></div>
<div class="dchips tog"><button type="button" data-k="ctl" aria-pressed="true">悬浮控制器</button></div>
<button type="button" class="dgo" id="gp-kick">来一个扰动</button>
{readouts([('gp-v', '当前间隙 mm'), ('gp-state', '状态')])}</div>'''

def h_cg():
    return f'''<div class="demo" data-demo="cg">
<div class="dstage"><svg class="dsvg" viewBox="0 0 600 160"><line class="hull" x1="100" y1="90" x2="500" y2="90"/><g id="cg-cp" class="arrow a"><line x1="300" y1="90" x2="300" y2="40"/><text x="306" y="44">压心（升力）</text></g><g id="cg-cg" class="arrow"><line x1="300" y1="90" x2="300" y2="140"/><text x="306" y="140">质心（重力）</text></g><text class="dt" x="8" y="156">示意：超音速时压心后移；不把质心也挪过去，机头就会一直往下栽</text></svg></div>
{slider('cg-m', '马赫数', 0.5, 2.04, 0.01, 0.9, '')}
<div class="dchips tog"><button type="button" data-k="pump" aria-pressed="true">往后泵油（最多约 20 吨）</button></div>
{readouts([('cg-gap', '压心 − 质心（示意）'), ('cg-state', '配平状态')])}</div>'''

WALL_DEMOS = {'tyre': wall_tyre, 'rail': wall_rail, 'water': wall_water, 'air': wall_air, 'g': wall_g, 'light': wall_light}
H_DEMOS = {'roadster': h_roadster, 'x15': h_x15, 'apollo': h_apollo, 'hydro': h_hydro, 'ground': h_ground, 'abs': h_abs, 'relaxed': h_relaxed, 'unstart': h_unstart, 'gap': h_gap, 'cg': h_cg}

# ---------- 跑一跑
def race():
    lanes = [('你输入的', 'you'), ('步行 5', 'walk'), ('博尔特 44.72', 'bolt'), ('高铁 350', 'hsr'), ('客机 900', 'air'), ('音速 1,225', 'snd')]
    ln = ''.join(f'<div class="rlane" data-k="{k}"><span>{esc(n)}</span><i><b></b></i><em></em></div>' for n, k in lanes)
    return f'''<div class="demo race" data-demo="race">
<div class="frow"><input id="rc-v" type="number" inputmode="decimal" min="0" step="any" value="120"><select id="rc-u"><option value="1">km/h</option><option value="3.6">m/s</option><option value="1.609344">mph</option><option value="1.852">节</option><option value="1225">马赫</option></select><button type="button" class="dgo" id="rc-go">开跑 10 秒</button><span class="small" id="rc-scale"></span></div>
<div class="rlanes" id="rc-lanes">{ln}</div>
<p class="small" id="rc-sum"></p></div>'''

def drag():
    presets = [('GB 7258 默认 5 s', 5, '0–100'), ('SU7 Max 宣称 2.78', 2.78, '0–100'), ('Plaid 厂商 1.99', 1.99, '0–60 mph'), ('Nevera 1.74', 1.74, '0–60 mph'), ('Roadster 宣称 0.81', 0.81, '0–60 mph'), ('Roadster 推文 0.59', 0.59, '0–60 mph')]
    opts = ''.join(f'<option value="{v}|{m}">{esc(n)}</option>' for n, v, m in presets)
    return f'''<div class="demo drag" data-demo="drag">
<div class="frow"><select id="dg-a">{opts}</select><span class="small">vs</span><select id="dg-b">{opts}</select><button type="button" class="dgo" id="dg-go">起步</button></div>
<div class="dlanes"><div class="dlane"><span id="dg-an"></span><i><b></b></i><em></em></div><div class="dlane"><span id="dg-bn"></span><i><b></b></i><em></em></div></div>
<p class="small" id="dg-sum">匀加速假设；0–60 mph 按 96.56 km/h 换算，厂商口径多含 1 英尺 rollout。到 100 km/h 之后继续滑行到 200 m 结束。</p></div>'''
