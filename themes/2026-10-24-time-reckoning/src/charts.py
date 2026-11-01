# -*- coding: utf-8 -*-
"""第 6 题 v2 的三张主图（2026-10-30）：HTML 骨架与静态 SVG；拖动、读数与动画在 demos.js。
① 新年落在哪个季节（第一章）② 谁的正午（第二章）③ 每天差多少 + 地球这只钟（第三章）。"""
import math, html
import editorial2 as E2
esc = lambda s: html.escape(str(s), quote=True)

# ---------- ① 新年落在哪个季节
DRIFT_RULES = E2.DRIFT['rules'] + [('met', '19 年 7 闰', 365.24682)]
RULE_CAL = {'none': 'egy', 'jul': 'jul', 'jal': 'per', 'greg': 'greg', 'met': 'heb', 'c128': ''}
RULE_NOTE = {
    'none': '不置闰，历年比回归年短约 6 小时：每 4 年早约一天。图里的埃及民用历就是这样一路往下滑。',
    'jul': '儒略历四年一闰，每年又多出约 11 分钟：128 年多出一天；从 325 年尼西亚会议到 1582 年攒下十天，格里历一次跳掉。图里那条缓缓上升的线。',
    'jal': '贾拉里历按「七个四年加一个五年」置闰，后人概括为 33 年 8 闰；今天的伊朗太阳历按天文春分定年首，33 年 8 闰是它的近似（1925–2088 年逐年吻合）。图里按 33 年规则画，诺鲁孜几乎一动不动。',
    'c128': '有人提过 128 年 31 闰：误差比格里历小得多，但不好记。',
    'greg': '格里历 400 年 97 闰，平均年比回归年长约 27 秒，约 3,200 年差一天；不是最准的，但好记。',
    'met': '阴阳历的 19 年 7 闰：235 个朔望月对 19 个回归年。希伯来历用固定算法，约 216 年差一天；中国农历以冬至定十一月，不累积。',
}

def drift():
    D = E2.DRIFT
    zoom = (''.join(f'<button type="button" role="tab" data-z="{k}" aria-selected="{"true" if k == "all" else "false"}">{esc(t)}</button>'
                    for k, t in (('all', '全程'), ('ce', '公元以来'), ('m', '1500 年以来'))))
    li = ''.join(f'<li data-cal="{k}"><button type="button" aria-pressed="false"><span class="dln"><i class="dsw"></i>{esc(n)}<small>{esc(ny)}</small></span>'
                 f'<span class="dlv" id="dv-{k}">—</span><span class="dls" id="ds-{k}"></span></button></li>' for k, n, ny, a, b in D['cals'])
    chips = ''.join(f'<button type="button" data-rule="{k}" aria-pressed="{"true" if k == "greg" else "false"}">{esc(n)}</button>' for k, n, L in DRIFT_RULES)
    rread = ''.join(f'<div><b id="{i}">—</b><span>{esc(l)}</span></div>' for i, l in (('rr-mean', '平均历年（日）'), ('rr-err', '比回归年'), ('rr-day', '多少年差一天'), ('rr-10k', '一万年下来')))
    return f'''<div class="drift">
<div class="dmain">
<div class="dctl"><span class="lensk">看</span><div class="lens" id="dzoom" role="tablist" aria-label="时间范围">{zoom}</div></div>
<div class="dbox" id="dbox" tabindex="0" role="slider" aria-label="新年落在哪个季节：拖动竖线换年份，方向键一年，Shift 加方向键十年" aria-valuemin="-2500" aria-valuemax="2100" aria-valuenow="2026" aria-valuetext="2026 年"><svg class="dsv" id="dsv" viewBox="0 0 960 440" aria-hidden="true"></svg></div>
<div class="ruleb"><h4>换一种闰法，看多少年差一天</h4><div class="rchips" id="rchips">{chips}</div><div class="rread">{rread}</div><p class="rnote" id="rr-note"></p></div>
</div>
<aside class="dside" aria-live="polite"><p class="dyr" id="dyr">2026<small>年 · 七种历法的新年</small></p><ul class="dlist" id="dlist">{li}</ul><p class="small" style="margin-top:12px">点一行，图里只亮这一条；再点一次恢复。</p></aside>
</div>'''

def drift_data():
    D = E2.DRIFT
    return {'cals': [dict(k=k, n=n, ny=ny, a=a, b=b) for k, n, ny, a, b in D['cals']], 'marks': D['marks'],
            'rules': [dict(k=k, n=n, L=L, cal=RULE_CAL.get(k, ''), note=RULE_NOTE[k]) for k, n, L in DRIFT_RULES]}

# ---------- ② 谁的正午
def noon():
    rows = ''.join(f'<div class="nbr" data-city="{esc(cid)}"><span class="nbn">{esc(n)}<small></small></span><span class="nbt"><i class="gap"></i><i class="c12"></i><i class="sun"></i></span><span class="nbv"><b>—</b><small></small></span></div>'
                   for cid, n, lon, tz, r in sorted(E2.NOON_CITIES, key=lambda c: c[2]))
    mode = '<button type="button" role="tab" data-m="lmt" aria-selected="false">1800 · 各城地方平时</button><button type="button" role="tab" data-m="now" aria-selected="true">今天 · 时区与夏令时</button>'
    opts = ''.join(f'<option value="{k}"{" selected" if k == "eu" else ""}>{esc(t)}</option>' for k, t in (('none', '不换时'), ('eu', '欧盟规则'), ('us', '美国规则'), ('eg', '埃及规则')))
    return f'''<div class="noon" id="noon">
<div class="nctl"><div class="lens" id="nmode" role="tablist" aria-label="哪个年代的钟">{mode}</div>
<label class="nslide"><span>日期</span><input type="range" id="ndate" min="1" max="365" step="1" value="297"><output id="ndate-o" for="ndate">10 月 24 日</output></label></div>
<div class="nbh" aria-hidden="true"><span>城市</span><span class="nbax" id="nbax"></span><span>太阳正午<em> · 比 12:00</em></span></div>
<div id="nbrows">{rows}</div>
<div class="nbr you" id="nbyou" data-city="you"><span class="nbn">你的城<small></small></span><span class="nbt"><i class="gap"></i><i class="c12"></i><i class="sun"></i></span><span class="nbv"><b>—</b><small></small></span></div>
<div class="nyou frow"><span class="lensk">你的城</span><label>经度 <input type="number" id="nlon" step="0.01" min="-180" max="180" value="-3.70" style="width:7em"> °</label><label>时区 UTC <input type="number" id="ntz" step="0.25" min="-12" max="14" value="1" style="width:5em"></label><label>夏令时 <select id="ndst">{opts}</select></label><span class="small">默认是马德里：西经 3.7°，却用中欧时间。</span></div>
<div class="nfoot"><span><i class="k1"></i>钟表的 12:00</span><span><i class="k2"></i>太阳过中天的时刻（真太阳正午）</span><span><i class="k3"></i>两者之差</span></div>
</div>'''

# ---------- ③ 每天差多少（精度阶梯）
LAD_W, LAD_H, LAD_L, LAD_R, LAD_T, LAD_B = 760, 440, 64, 16, 16, 64
LAD_TOP, LAD_BOT = 3, -14  # 10³ 秒 … 10⁻¹⁴ 秒 / 天
def lad_y(v): return LAD_T + (LAD_TOP - math.log10(v)) / (LAD_TOP - LAD_BOT) * (LAD_H - LAD_T - LAD_B)
def si(v):
    """秒数 → 中文读法（取三位有效数字）。"""
    for f, u in ((1, '秒'), (1e-3, '毫秒'), (1e-6, '微秒'), (1e-9, '纳秒'), (1e-12, '皮秒'), (1e-15, '飞秒')):
        if v >= f * 0.999:
            x = v / f
            s = f'{x:.0f}' if x >= 10 else f'{x:.2g}'
            return f'{s} {u}'
    return f'{v:g} 秒'

def ladder(rungs, gps):
    n = len(rungs); pw = LAD_W - LAD_L - LAD_R; xs = [LAD_L + (k + .5) / n * pw for k in range(n)]
    grid = ''
    for e in range(LAD_TOP, LAD_BOT - 1, -1):
        y = lad_y(10 ** e); major = e % 3 == 0
        grid += f'<line class="gl{" s" if major else ""}" x1="{LAD_L}" y1="{y:.1f}" x2="{LAD_W - LAD_R}" y2="{y:.1f}"/>'
        if major: grid += f'<text class="gt" x="{LAD_L - 8}" y="{y + 4:.1f}" text-anchor="end">{si(10 ** e)}</text>'
    step = ''
    for k, r in enumerate(rungs):
        y = lad_y(r['v']); x0 = LAD_L + k / n * pw; x1 = LAD_L + (k + 1) / n * pw
        step += (f'M{x0:.1f} {y:.1f} H{x1:.1f}' if k == 0 else f' V{y:.1f} H{x1:.1f}')
    gy = lad_y(gps['v'])
    rg = ''.join(f'<g class="rung{" on" if k == n - 1 else ""}" data-k="{k}"><rect x="{xs[k] - pw / n / 2:.1f}" y="{LAD_T}" width="{pw / n:.1f}" height="{LAD_H - LAD_T:.1f}" fill="transparent"/>'
                 f'<rect class="bar" x="{xs[k] - 2:.1f}" y="{lad_y(r["v"]):.1f}" width="4" height="{LAD_H - LAD_B - lad_y(r["v"]):.1f}" rx="2"/>'
                 f'<circle class="bar" cx="{xs[k]:.1f}" cy="{lad_y(r["v"]):.1f}" r="6"/>'
                 f'<text class="bv" x="{xs[k]:.1f}" y="{lad_y(r["v"]) - 14:.1f}" text-anchor="middle">{esc(si(r["v"]))}</text>'
                 f'<text class="bn" x="{xs[k]:.1f}" y="{LAD_H - LAD_B + 20}" text-anchor="middle">{esc(r["short"])}</text><text class="by" x="{xs[k]:.1f}" y="{LAD_H - LAD_B + 38}" text-anchor="middle">{esc(r["yr"])}</text></g>' for k, r in enumerate(rungs))
    svg = (f'<svg class="lsv" id="lsv" viewBox="0 0 {LAD_W} {LAD_H}" aria-hidden="true">{grid}'
           f'<path d="{step}" fill="none" style="stroke:var(--line);stroke-width:1.5"/>'
           f'<line class="gps" x1="{LAD_L}" y1="{gy:.1f}" x2="{LAD_W - LAD_R}" y2="{gy:.1f}"/><text class="gpst" x="{LAD_W - LAD_R}" y="{gy - 8:.1f}" text-anchor="end">{esc(gps["label"])}</text>{rg}</svg>')
    return (f'<div class="ladw"><div class="lbox" id="lbox" tabindex="0" role="slider" aria-label="精度阶梯：左右方向键或拖动选一台钟" aria-valuemin="1" aria-valuemax="{n}" aria-valuenow="{n}">{svg}</div>'
            f'<aside class="ladcard" id="ladcard" aria-live="polite"><figure id="lc-fig" class="none"><img id="lc-img" alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" loading="lazy"><figcaption id="lc-cap"><span class="cs"></span><span class="cr"></span></figcaption></figure>'
            f'<p class="lck" id="lc-k"></p><p class="lcn" id="lc-n"></p><p class="lcy" id="lc-y"></p><p class="lcv"><b id="lc-v"></b><small>每天差</small></p>'
            f'<dl class="lcd"><dt>凭什么准</dt><dd id="lc-p"></dd><dt>每天</dt><dd id="lc-d"></dd><dt id="lc-1t">差一秒要</dt><dd id="lc-1"></dd><dt>口径</dt><dd id="lc-o"></dd></dl></aside></div>')

# ---------- ③ 地球这只钟（ΔT 与闰秒）
LOD_W, LOD_H, LOD_L, LOD_R, LOD_T, LOD_B = 960, 300, 48, 16, 24, 48
LOD_X0, LOD_X1, LOD_Y0, LOD_Y1 = 1900, 2030, -10, 80
def lod_x(y): return LOD_L + (y - LOD_X0) / (LOD_X1 - LOD_X0) * (LOD_W - LOD_L - LOD_R)
def lod_y(v): return LOD_T + (LOD_Y1 - v) / (LOD_Y1 - LOD_Y0) * (LOD_H - LOD_T - LOD_B)
def lod(points, leaps):
    grid = ''.join(f'<line class="gl" x1="{LOD_L}" y1="{lod_y(v):.1f}" x2="{LOD_W - LOD_R}" y2="{lod_y(v):.1f}"/><text class="gt" x="{LOD_L - 8}" y="{lod_y(v) + 4:.1f}" text-anchor="end">{v} s</text>' for v in (0, 20, 40, 60, 80))
    grid += ''.join(f'<text class="gt" x="{lod_x(y):.1f}" y="{LOD_H - LOD_B + 40}" text-anchor="middle">{y}</text>' for y in range(1900, 2031, 20))
    d = 'M' + ' L'.join(f'{lod_x(y):.1f} {lod_y(v):.1f}' for y, v in points)
    area = d + f' L{lod_x(points[-1][0]):.1f} {lod_y(0):.1f} L{lod_x(points[0][0]):.1f} {lod_y(0):.1f}Z'
    by = LOD_H - LOD_B
    ls = ''.join(f'<line class="ls" data-y="{ly}" x1="{lod_x(ly):.1f}" y1="{by - 4}" x2="{lod_x(ly):.1f}" y2="{by + 12}"><title>{esc(s)}</title></line>' for s, ly in leaps)
    xe = lod_x(2027.38)
    return (f'<div class="lodbox" id="lodbox" tabindex="0" role="slider" aria-label="ΔT：拖动竖线换年份" aria-valuemin="1900" aria-valuemax="2024" aria-valuenow="2024">'
            f'<svg class="lodsv" id="lodsv" viewBox="0 0 {LOD_W} {LOD_H}" aria-hidden="true">{grid}<path class="dta" d="{area}"/><path class="dtl" d="{d}"/>'
            f'<line class="gl" x1="{LOD_L}" y1="{by}" x2="{LOD_W - LOD_R}" y2="{by}" style="stroke:var(--line)"/>{ls}'
            f'<text class="lsl" x="{lod_x(1972):.1f}" y="{by + 26}">闰秒（27 次）</text>'
            f'<line class="end" x1="{xe:.1f}" y1="{LOD_T}" x2="{xe:.1f}" y2="{by + 12}"/><text class="lsl" x="{xe - 6:.1f}" y="{by + 26}" text-anchor="end">2027-05-20 起不再插</text>'
            f'<g id="lodcur"><line class="curg" x1="0" y1="{LOD_T}" x2="0" y2="{by}"/><line class="cur" x1="0" y1="{LOD_T}" x2="0" y2="{by}"/><circle class="pt" r="6" cx="0" cy="0"/><text class="cury" x="8" y="{LOD_T + 16}"></text></g></svg></div>'
            f'<div class="dread"><div><b id="lod-dt">—</b><span>这一年年中的 ΔT（秒）：地球比原子时累计慢了多少</span></div><div><b id="lod-ls">—</b><span>到这一年年底为止插过的闰秒</span></div><div><b id="lod-lod">—</b><span>这一年的日长 − 86,400 秒（由 ΔT 年差分换算）</span></div></div>')
