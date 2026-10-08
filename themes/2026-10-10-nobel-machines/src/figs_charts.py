# -*- coding: utf-8 -*-
"""卷首的对数尺、世界地图、尺度阶梯和几张小图（都是内联 SVG，颜色走 CSS 类）。"""
import math
from figs_base import Svg, esc, f


def tw(s, size=13.0):
    """粗估一行字的宽度（像素）：中日韩字符按字号算，西文数字约 0.56 倍。"""
    w = 0.0
    for ch in str(s):
        o = ord(ch)
        if o >= 0x2E80:
            w += size
        elif ch == ' ':
            w += size * 0.3
        else:
            w += size * 0.56
    return w


def zh_len(m):
    """把米数写成中文读者习惯的长度。"""
    if m < 1:
        return f'{m*100:g} 厘米'
    if m < 1000:
        return f'{m:g} 米'
    km = m / 1000.0
    if km < 10000:
        return f'{km:,.0f} 公里' if km >= 100 else f'{km:g} 公里'
    if km < 1e8:
        return f'{km/1e4:g} 万公里'
    return f'{km/1e8:g} 亿公里'


# ------------------------------------------------------------------ 卷首：对数尺
RULER_BUILT = [
    (1.5, '1887 浮在水银上的石板，1.5 米', 'michelson'),
    (1.52, '1939 60 英寸回旋加速器', 'cyclotron'),
    (1.83, '1959 液氢气泡室，1.83 米', 'bubble'),
    (2.7, '1895 伦琴的荧光屏，在约 2.7 米外发光', None),
    (5.49, '1989 COBE 卫星，5.5 米', 'cobe'),
    (14.6, '1967 Homestake 的罐子，14.6 米', 'homestake'),
    (41.4, '1996 超级神冈的水罐，41 米', 'superk-sno'),
    (1000, '2010 IceCube，边长 1 公里', 'icecube'),
    (1600, '1964 一英里望远镜的基线', 'cambridge'),
    (2200, '1981 SPS 环，直径 2.2 公里', 'spps'),
    (4000, '2015 LIGO 的臂，4 公里', 'ligo'),
    (8486, '2008 LHC 环，直径 8.5 公里', 'lhc'),
]
RULER_FUTURE = [
    (28900, 'FCC 隧道，直径约 29 公里（待批）'),
    (1.3e6, 'DUNE 的束流，1,300 公里（在建）'),
    (1.2742e7, '事件视界望远镜：整个地球'),
    (2.5e9, 'LISA 的臂，250 万公里（2035 年前后）'),
]
RULER_SHORT = {
    1.5: '1887 石板，1.5 米', 1.52: '1939 回旋加速器，1.5 米', 1.83: '1959 气泡室，1.83 米', 2.7: '1895 伦琴的荧光屏，2.7 米',
    5.49: '1989 COBE，5.5 米', 14.6: '1967 Homestake，14.6 米', 41.4: '1996 超级神冈，41 米', 1000: '2010 IceCube，1 公里',
    1600: '1964 一英里望远镜', 2200: '1981 SPS 环，2.2 公里', 4000: '2015 LIGO，4 公里', 8486: '2008 LHC 环，8.5 公里',
    28900: 'FCC 隧道，29 公里（待批）', 1.3e6: 'DUNE 束流，1,300 公里', 1.2742e7: '事件视界望远镜：地球', 2.5e9: 'LISA，250 万公里',
}
DECADES_V = ['10 厘米', '1 米', '10 米', '100 米', '1 公里', '10 公里', '100 公里', '千公里', '1 万公里', '10 万公里', '百万公里', '千万公里']
DECADES = [(-1, '10 厘米'), (0, '1 米'), (1, '10 米'), (2, '100 米'), (3, '1 公里'), (4, '10 公里'), (5, '100 公里'),
           (6, '1,000 公里'), (7, '1 万公里'), (8, '10 万公里'), (9, '100 万公里'), (10, '1,000 万公里')]


def _place_rows(items, X, size, wmax, gap=14):
    """从右往左给标签排行：返回 [(x, row, anchor)]，保证同一行不重叠、引线不穿过上面的字。"""
    order = sorted(range(len(items)), key=lambda i: -X(items[i][0]))
    rows = []          # 每行已占用的最左端
    out = [None] * len(items)
    for i in order:
        x = X(items[i][0])
        w = tw(items[i][1], size) + 10
        if x + w > wmax:                      # 靠右边放不下：改成右对齐，占用 [x-w, x]
            r = 0
            while r < len(rows) and rows[r] < x + gap:
                r += 1
            if r == len(rows):
                rows.append(1e9)
            rows[r] = min(rows[r], x - w)
            out[i] = (x, r, 'end')
            continue
        r = 0
        while r < len(rows) and rows[r] < x + w + gap:
            r += 1
        if r == len(rows):
            rows.append(1e9)
        rows[r] = x
        out[i] = (x, r, 'start')
    return out, len(rows)


def hero_ruler_h():
    W = 1200
    x0, x1 = 44, 1150
    lo, hi = -1.0, 10.0

    def X(m):
        return x0 + (math.log10(m) - lo) / (hi - lo) * (x1 - x0)
    size = 13.5
    pb, nb = _place_rows(RULER_BUILT, X, size, W - 8)
    pf_, nf = _place_rows(RULER_FUTURE, X, size, W - 8)
    rowh = 21
    top = 18 + nf * rowh + 16
    ay = top + 22
    H = ay + 30 + nb * rowh + 16
    s = Svg(W, H, cls='dwg ruler ruler-h', title='对数尺：从 10 厘米到 1,000 万公里，十二座装置和几座未来装置的尺度')
    # 尺身
    s.rect(x0 - 12, ay - 22, x1 - x0 + 24, 44, 'o1 fs')
    for d, lab in DECADES:
        xx = x0 + (d - lo) / (hi - lo) * (x1 - x0)
        s.line(xx, ay - 22, xx, ay - 4, 'o1')
        if d < hi:
            s.text(xx + 4, ay - 8, lab, 'tn')
        if d < hi:
            for k in range(2, 10):
                xk = x0 + (d + math.log10(k) - lo) / (hi - lo) * (x1 - x0)
                s.line(xk, ay + 22, xk, ay + (10 if k == 5 else 14), 'o2')
    # 已建成：尺子下方
    for (m, lab, mid), (x, r, anc) in zip(RULER_BUILT, pb):
        y = ay + 22 + 20 + r * rowh
        s.line(x, ay + 22, x, y - 4, 'dim')
        s.circle(x, ay + 22, 3.2, 'af' if mid else 'o1 fs')
        s.text(x + (5 if anc == 'start' else -5), y, lab, 'tr', anc)
    # 在建与设想：尺子上方，虚线
    for (m, lab), (x, r, anc) in zip(RULER_FUTURE, pf_):
        y = ay - 22 - 14 - r * rowh
        s.line(x, ay - 22, x, y + 4, 'dim d')
        s.circle(x, ay - 22, 3.2, 'o1 fs a')
        s.text(x + (5 if anc == 'start' else -5), y, lab, 'tr tmu', anc)
    return s.svg()


def hero_ruler_v():
    """手机上用的竖版：小的在上，大的在下。"""
    W = 360
    y0, y1 = 26, 846
    lo, hi = -1.0, 10.0
    ax = 112

    def Y(m):
        return y0 + (math.log10(m) - lo) / (hi - lo) * (y1 - y0)
    items = [(m, lab, True, mid) for m, lab, mid in RULER_BUILT] + [(m, lab, False, None) for m, lab in RULER_FUTURE]
    items.sort(key=lambda t: t[0])
    ys = [Y(t[0]) for t in items]
    lab_y = ys[:]
    step = 19.0
    for _ in range(60):                       # 把挤在一起的标签推开
        moved = False
        for i in range(1, len(lab_y)):
            if lab_y[i] - lab_y[i - 1] < step:
                mid_ = (lab_y[i] + lab_y[i - 1]) / 2
                lab_y[i - 1], lab_y[i] = mid_ - step / 2, mid_ + step / 2
                moved = True
        if not moved:
            break
    s = Svg(W, y1 + 24, cls='dwg ruler ruler-v', title='对数尺（竖版）：从 10 厘米到 1,000 万公里')
    s.rect(ax - 46, y0 - 10, 46, y1 - y0 + 20, 'o1 fs')
    for (d, _), lab in zip(DECADES, DECADES_V):
        yy = y0 + (d - lo) / (hi - lo) * (y1 - y0)
        s.line(ax - 46, yy, ax - 30, yy, 'o1')
        s.text(ax - 50, yy + 4, lab, 'tn', 'end')
        if d < hi:
            for k in range(2, 10):
                yk = y0 + (d + math.log10(k) - lo) / (hi - lo) * (y1 - y0)
                s.line(ax, yk, ax - (10 if k == 5 else 6), yk, 'o2')
    for (m, lab, built, mid), yt, yl in zip(items, ys, lab_y):
        s.path(f'M{f(ax)} {f(yt)}L{f(ax + 14)} {f(yl)}H{f(ax + 22)}', 'dim' if built else 'dim d')
        s.circle(ax, yt, 3.2, ('af' if mid else 'o1 fs') if built else 'o1 fs a')
        s.text(ax + 26, yl + 4.5, RULER_SHORT.get(m, lab), 'tr' if built else 'tr tmu')
    return s.svg()


# ------------------------------------------------------------------ 世界地图
def world_symbol(world):
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
            f'<symbol id="world" viewBox="0 0 {world["w"]} {world["h"]}"><path d="{world["d"]}" class="land"/></symbol></defs></svg>')


def XY(lat, lon):
    return (lon + 180) * 2.0, (90 - lat) * 2.0


# 徽标相对落点的偏移（手工排开，免得挤在一起）；键是 (装置 id, 第几个落点)
BADGE = {
    ('michelson', 0): (27, -17), ('leiden', 0): (4, -30), ('cyclotron', 0): (-30, 8), ('cambridge', 0): (-22, -22),
    ('spps', 0): (30, 8), ('homestake', 0): (-2, -30), ('cobe', 0): (26, 8), ('superk-sno', 0): (22, -20),
    ('superk-sno', 1): (-8, -30), ('ligo', 0): (-10, -28), ('ligo', 1): (8, 24), ('icecube', 0): (0, -22),
}


def map_overview(machines):
    s = Svg(720, 366, cls='dwg map', title='十二座装置在世界地图上的位置')
    s.add('<use href="#world" x="0" y="0" width="720" height="360"/>')
    s.line(0, 180, 720, 180, 'grat')
    s.line(360, 0, 360, 360, 'grat')
    groups = {}
    for m in machines:
        for j, st in enumerate(m['sites']):
            if m['id'] == 'michelson' and j == 1:
                continue
            x, y = XY(st['lat'], st['lon'])
            y = min(y, 357)
            key = (round(x), round(y))
            groups.setdefault(key, []).append((m, j, x, y))
    # 同一地点的两座装置合成一个徽标（伯克利 3·4，CERN 6·9）
    merged = {}
    for key, lst in groups.items():
        near = [k for k in merged if abs(k[0] - key[0]) <= 2 and abs(k[1] - key[1]) <= 2]
        if near:
            merged[near[0]] += lst
        else:
            merged[key] = list(lst)
    for key, lst in merged.items():
        m0, j0, x, y = lst[0]
        dx, dy = BADGE.get((m0['id'], j0), (20, -20))
        nums = '·'.join(str(m['no']) for m, _, _, _ in lst)
        bx, by = x + dx, y + dy
        s.line(x, y, bx, by, 'dim')
        s.circle(x, y, 3, 'af')
        wbadge = max(17, tw(nums, 10.5) + 9)
        s.rect(bx - wbadge / 2, by - 8.5, wbadge, 17, 'o1 fs', rx=8.5)
        s.text(bx, by + 3.8, nums, 'tb tbadge', 'middle')
    return s.svg()


def keyplan(m):
    """标题栏里的位置小图：一张小地图，装置所在处打一个十字。"""
    s = Svg(720, 360, cls='dwg keyplan', title=f'{m["short"]}的位置')
    s.add('<use href="#world" x="0" y="0" width="720" height="360"/>')
    for st in m['sites']:
        if m['id'] == 'michelson' and st['name'].startswith('波茨坦'):
            continue
        x, y = XY(st['lat'], st['lon'])
        y = min(y, 352)
        s.line(x, 0, x, 360, 'cross')
        s.line(0, y, 720, y, 'cross')
        s.circle(x, y, 13, 'af')
    return s.svg()


# ------------------------------------------------------------------ 每张卡片里的时间条
def tl_strip(m, machines):
    W, H = 600, 62
    x0, x1 = 16, 584
    a, b = 1880, 2030

    def X(yr):
        return x0 + (yr - a) / (b - a) * (x1 - x0)
    s = Svg(W, H, cls='dwg tls', title=f'{m["short"]}：{m["tool"]["t_idea"]} 年设想，{m["tool"]["t_result"]} 年出成果，{m["prize"]["year"]} 年获奖')
    y = 40
    s.line(x0, y, x1, y, 'dim')
    for yr in (1900, 1950, 2000):
        s.line(X(yr), y - 4, X(yr), y + 4, 'dim')
        s.text(X(yr), y + 18, str(yr), 'tn', 'middle')
    for o in machines:
        if o['id'] != m['id']:
            s.circle(X(o['prize']['year']), y, 2.2, 'dimdot')
    t = m['tool']
    xi, xr, xp = X(t['t_idea']), X(t['t_result']), X(t['t_prize'])
    s.line(xi, y, xr, y, 'o25')
    s.line(xr, y, xp, y, 'a o3')
    s.circle(xi, y, 3.2, 'o1 fs')
    s.circle(xp, y, 4.4, 'af')
    left = f'{t["t_idea"]} 设想'
    right = f'{t["t_result"]} 成果，{t["t_prize"]} 获奖'
    if xi - tw(left, 12.5) - 8 > x0:
        s.text(xi - 7, y - 9, left, 'ts', 'end')
    else:
        s.text(xi, y - 12, left, 'ts', 'start')
        right = ' ' * 0 + right
    if xp + tw(right, 12.5) + 10 < x1:
        s.text(xp + 8, y - 9, right, 'ts', 'start')
    else:
        s.text(xp + 4, y - 12, right, 'ts', 'end')
    return s.svg()


# ------------------------------------------------------------------ 探测器的尺度阶梯（竖版对数尺）
def ladder_fig(rungs):
    """rungs: [{scale_m, label, short, built}]，从小到大。"""
    W = 420
    lo, hi = 0.0, 20.0
    y0, y1 = 30, 770
    ax = 96

    def Y(m):
        return y0 + (math.log10(m) - lo) / (hi - lo) * (y1 - y0)
    rs = sorted(rungs, key=lambda r: r['scale_m'])
    ys = [Y(r['scale_m']) for r in rs]
    ly = ys[:]
    step = 41.0
    for _ in range(200):
        moved = False
        for i in range(1, len(ly)):
            if ly[i] - ly[i - 1] < step - 0.01:
                mid_ = (ly[i] + ly[i - 1]) / 2
                ly[i - 1], ly[i] = mid_ - step / 2, mid_ + step / 2
                moved = True
        if ly[0] < y0 + 4:
            sh = y0 + 4 - ly[0]
            ly = [v + sh for v in ly]
            moved = True
        if not moved:
            break
    Hh = max(y1, ly[-1]) + 44
    s = Svg(W, Hh, cls='dwg ladder', title='探测器的尺度阶梯：从 1 米的桌面到几千光年的脉冲星计时阵（对数坐标）')
    s.line(ax, y0 - 8, ax, y1 + 8, 'o1')
    for d in range(0, 21):
        yy = y0 + (d - lo) / (hi - lo) * (y1 - y0)
        s.line(ax - (7 if d % 3 == 0 else 4), yy, ax, yy, 'o2')
    for d, lab in ((0, '1 米'), (3, '1 公里'), (6, '1,000 公里'), (9, '100 万公里'), (12, '10 亿公里'), (16, '约 1 光年'), (19, '约 1,000 光年')):
        yy = y0 + (d - lo) / (hi - lo) * (y1 - y0)
        s.text(ax - 11, yy + 4, lab, 'tn', 'end')
    for r, yt, yl in zip(rs, ys, ly):
        s.path(f'M{f(ax)} {f(yt)}L{f(ax + 18)} {f(yl)}H{f(ax + 26)}', 'dim' if r['built'] else 'dim d')
        s.circle(ax, yt, 4, 'af' if r['built'] else 'o1 fs a')
        s.text(ax + 30, yl + 1, r['label'], 'tb')
        s.text(ax + 30 + tw(r['label'], 14) + 8, yl + 1, r['size'], 'tn')
        s.text(ax + 30, yl + 18, r['short'], 'tm')
    return s.svg()


# ------------------------------------------------------------------ 外推规律的小图
def law_chart(law, xr, yfmt, ylab):
    W, H = 320, 210
    x0, x1, y0, y1 = 46, 306, 18, 170
    pts = sorted(law['points'], key=lambda p: p['year'])
    vals = [math.log10(p['value']) for p in pts]
    lo, hi = math.floor(min(vals)), math.ceil(max(vals))
    if hi == lo:
        hi += 1
    a, b = xr

    def X(yr):
        return x0 + (yr - a) / (b - a) * (x1 - x0)

    def Y(v):
        return y1 - (v - lo) / (hi - lo) * (y1 - y0)
    s = Svg(W, H, cls='dwg lawc', title=law['name'])
    s.line(x0, y1, x1, y1, 'dim')
    s.line(x0, y0, x0, y1, 'dim')
    nt = hi - lo
    stepd = 1 if nt <= 6 else (2 if nt <= 12 else 5)
    for d in range(lo, hi + 1, stepd):
        s.line(x0 - 4, Y(d), x1, Y(d), 'grid')
        s.text(x0 - 7, Y(d) + 4, yfmt(d), 'tn tsm', 'end')
    stx = 20 if (b - a) <= 130 else (50 if (b - a) <= 260 else 100)
    yr = (a // stx + 1) * stx
    while yr < b:
        s.line(X(yr), y1, X(yr), y1 + 4, 'dim')
        s.text(X(yr), y1 + 17, str(yr), 'tn tsm', 'middle')
        yr += stx
    # 只把「纪录线」连起来：每个点都比前面所有的点大才连
    # 点可以带分组键 s：同一组里才连线，s 为 None 的点不连线
    groups = []
    for p in pts:
        g = p.get('s', 'all')
        if g is not None and g not in groups:
            groups.append(g)
    for g in groups:
        run = -1e9
        chain = []
        for p, v in zip(pts, vals):
            if p.get('s', 'all') == g and v > run:
                chain.append((X(p['year']), Y(v), p['year'] > 2026))
                run = v
        for i in range(1, len(chain)):
            (xa, ya, fa), (xb, yb, fb) = chain[i - 1], chain[i]
            s.line(xa, ya, xb, yb, 'o1 d' if fb else 'o1')
    for p, v in zip(pts, vals):
        fut = p['year'] > 2026
        s.add(f'<circle cx="{f(X(p["year"]))}" cy="{f(Y(v))}" r="4.2" class="{"o1 fs a" if fut else "af"} ring"><title>{esc(str(p["year"]) + "：" + p["label"])}</title></circle>')
    s.text(x0, y1 + 34, ylab, 'tm tsm')
    return s.svg()
