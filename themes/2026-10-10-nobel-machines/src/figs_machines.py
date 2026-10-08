# -*- coding: utf-8 -*-
"""十二座装置的同比例示意图（程序绘制）。

每张图里同一视图内的东西按同一比例画；比例写在图内的比例尺或尺寸线上。
尺寸出处见各装置卡的资料；没有核到的尺寸在图上标「示意」或「推算」。
"""
import math
from figs_base import Svg, f

W, H = 600, 430


def balloon(s, x, y, n):
    s.circle(x, y, 8.5, 'o1 fs')
    s.text(x, y + 4.5, str(n), 'tn', 'middle')


# ------------------------------------------------------------------ 1 迈克尔逊
def fig_michelson():
    s = Svg(W, H, title='迈克尔逊–莫雷装置（1887 年）的平面与立面，按比例绘制')
    # 平面：1 米 = 132 像素
    k = 132.0
    x0, y0, a = 26, 54, 1.5 * k
    cx, cy = x0 + a / 2, y0 + a / 2
    s.text(x0, 38, '平面：从上往下看', 'tb')
    s.rect(x0, y0, a, a, 'o fs')
    r2 = math.sqrt(2)
    # 两条对角线上的折返光路（各画三条示意）
    for sx, sy in ((-1, -1), (1, -1)):
        ux, uy = sx / r2, sy / r2
        vx, vy = -uy, ux
        L = a / 2 * r2 - 24
        for t in (-8, 0, 8):
            s.line(cx + ux * L + vx * t, cy + uy * L + vy * t, cx - ux * L + vx * t, cy - uy * L + vy * t, 'a o2')
    # 四角的镜组：每角 4 面
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        ux, uy = sx / r2, sy / r2
        vx, vy = -uy, ux
        L = a / 2 * r2 - 22
        px, py = cx + ux * L, cy + uy * L
        for j in range(4):
            t = (j - 1.5) * 8
            mx, my = px + vx * t, py + vy * t
            s.line(mx - vx * 2.4, my - vy * 2.4, mx + vx * 2.4, my + vy * 2.4, 'o25')
    # 中心：分束玻璃与补偿玻璃
    s.line(cx, cy - 9, cx, cy + 9, 'o')
    s.line(cx + 7, cy - 16, cx + 7, cy - 4, 'o1')
    # 光源与望远镜（都装在石板上，随石板一起转）
    s.circle(x0 + 16, cy + 40, 5, 'o1 fs')
    s.line(x0 + 21, cy + 38, cx - 3, cy + 2, 'a o2')
    s.rect(cx + 30, y0 + a - 24, 26, 9, 'o1 fs')
    s.line(cx + 2, cy + 4, cx + 40, y0 + a - 24, 'a o2')
    s.text(x0 + 6, cy + 60, '光源', 'ts')
    s.text(cx + 43, y0 + a - 30, '望远镜', 'ts', 'middle')
    s.dim_h(x0, x0 + a, y0 + a + 14, '石板 1.5 米见方', above=False)
    yy = y0 + a + 50
    s.line(x0, yy - 4, x0 + 22, yy - 4, 'a o2')
    s.lines(x0 + 30, yy, ['光在两条对角线上来回折返，', '等效臂长约 11 米', '（1881 年那台约 1 米）'], 'tm')
    s.line(x0 + 4, yy + 56, x0 + 18, yy + 56, 'o25')
    s.lines(x0 + 30, yy + 61, ['四角各 4 面镜，共 16 面', '整块石板 6 分钟转一圈，', '边转边读数'], 'tm')

    # 立面：1 米 = 108 像素
    ke = 108.0
    ex, base = 352, 392
    s.text(262, 38, '立面：剖开看', 'tb')
    s.lines(262, 60, ['① 砂岩板，厚 0.3 米', '② 环形木浮子，厚 0.25 米', '③ 铸铁槽里的水银', '④ 砖墩（原文没给尺寸，示意）'], 'tm')
    s.ground(250, 592, base)
    pw, ph = 1.12 * ke, 0.52 * ke
    s.add(f'<rect x="{f(ex - pw / 2)}" y="{f(base - ph)}" width="{f(pw)}" height="{f(ph)}" fill="url(#pat-brick)" class="pf"/>')
    s.rect(ex - pw / 2, base - ph, pw, ph, 'o1')
    ty = base - ph                      # 墩顶
    half = 0.75 * ke
    cw, cd = 0.44 * ke, 0.21 * ke       # 槽宽、槽深
    for sgn in (-1, 1):
        xo = ex + sgn * half
        xi = xo - sgn * cw
        xl, xr = min(xo, xi), max(xo, xi)
        s.rect(xl + 1, ty - 13, cw - 2, 13, 'fa2')                      # 水银
        s.poly([(xl, ty - cd), (xl, ty), (xr, ty), (xr, ty - cd)], 'o', close=False)  # 槽
        fw, fh = 0.40 * ke, 0.25 * ke
        fx = xl + (cw - fw) / 2
        s.rect(fx, ty - 7 - fh, fw, fh, 'o1 fs')                        # 木浮子
    top = ty - 7 - 0.25 * ke
    th = 0.30 * ke
    s.rect(ex - half, top - th, 1.5 * ke, th, 'o fs')                     # 石板
    for sgn in (-1, 1):
        s.rect(ex + sgn * (half - 9) - 5, top - th - 11, 10, 11, 'o1 fs')  # 镜架
    s.line(ex - half + 14, top - th - 6, ex + half - 14, top - th - 6, 'a o2')
    balloon(s, ex - half - 20, top - th / 2, 1)
    s.line(ex - half - 11.5, top - th / 2, ex - half, top - th / 2, 'dim')
    balloon(s, ex - half - 20, top + 16, 2)
    s.line(ex - half - 11.5, top + 16, ex - half + 4, top + 16, 'dim')
    balloon(s, ex + half + 20, ty - 6, 3)
    s.line(ex + half + 11.5, ty - 6, ex + half - 6, ty - 6, 'dim')
    balloon(s, ex + pw / 2 + 22, base - 22, 4)
    s.line(ex + pw / 2 + 13.5, base - 22, ex + pw / 2, base - 22, 'dim')
    s.dim_h(ex - half, ex + half, base + 14, '1.5 米', above=False)
    hm = 1.75 * ke
    s.man(516, base, hm)
    s.text(516, base - hm - 8, '人 1.75 米', 'tm', 'middle')
    return s.svg()


# ------------------------------------------------------------------ 2 莱顿
def fig_leiden():
    s = Svg(W, H, title='莱顿低温实验室的级联液化：温度阶梯（对数坐标）与 1908 年 7 月 10 日的用料')
    s.text(26, 38, '温度阶梯（纵轴是对数）', 'tb')
    s.text(206, 38, '前三级是减压后的温度', 'tm')
    ya, yb = 62, 392
    la, lb = math.log10(320), math.log10(1.2)

    def Y(T):
        return ya + (la - math.log10(T)) / (la - lb) * (yb - ya)
    ax = 74
    s.line(ax, ya, ax, yb, 'o1')
    for T in (300, 100, 30, 10, 3):
        s.line(ax - 5, Y(T), ax, Y(T), 'o1')
        s.text(ax - 9, Y(T) + 4.5, f'{T} K', 'tn', 'end')
    # 前三级是减压后的温度（1912 年的报道：−90、−160、−210 °C）；液氢取常压沸点，液氦是昂内斯自己报的 4.25 K
    steps = [(293, '室温', ''), (183, '氯甲烷', '约 −90 °C'), (113, '乙烯', '约 −160 °C'), (63, '液氧', '约 −210 °C'),
             (20.4, '液氢', '约 20 K'), (4.25, '液氦', '4.25 K'), (1.7, '抽气减压', '约 1.7 K')]
    x = ax + 16
    wstep = 44
    pts = []
    for i, (T, name, sub) in enumerate(steps):
        y = Y(T)
        pts += [(x, y), (x + wstep, y)]
        acc = i >= 5
        s.text(x + wstep + 6, y - 3, name, 'tb' if acc else 't')
        if sub:
            s.text(x + wstep + 6 + 15 * len(name) + 6, y - 3, sub, 'tm')
        if i < 5:
            x += wstep * 0.62
    d = 'M' + 'L'.join(f'{f(px)} {f(py)}' for px, py in pts)
    s.path(d, 'o')
    # 最后两级用强调色重描
    s.line(pts[10][0], pts[10][1], pts[11][0], pts[11][1], 'a o3')
    s.line(pts[12][0], pts[12][1], pts[13][0], pts[13][1], 'a o3')
    s.text(ax + 16, yb + 22, '每一级的冷量，用来把下一级的气体冷到能液化', 'tm')

    # 右侧：当天的用料，方块面积按体积比例
    rx = 392
    s.text(rx, 38, '1908-07-10 的用料', 'tb')
    s.text(rx, 56, '方块面积按体积比例', 'tm')
    kk = 9.4
    a1, a2, a3 = math.sqrt(75) * kk, math.sqrt(20) * kk, math.sqrt(0.06) * kk
    by = 160
    s.rect(rx, by - a1 + 0, a1, a1, 'o1')
    s.text(rx + 8, by - a1 + 20, '液空 75 升', 't')
    s.text(rx + 8, by - a1 + 37, '前一天备好', 'tm')
    s.rect(rx + a1 + 14, by - a2, a2, a2, 'o1')
    s.lines(rx + a1 + 14, by + 17, ['液氢 20 升'], 't')
    s.rect(rx + a1 + 14 + a2 + 20, by - a3, a3, a3, 'af')
    s.leader(rx + a1 + 34 + a2 + 12, by - 34, rx + a1 + 34 + a2 + a3 / 2, by - a3 - 1, None)
    s.lines(rx + a1 + 34 + a2 - 16, by - 58, ['液氦', '约 60 毫升'], 'tb')
    # 当天的时间
    ty = 262
    s.text(rx, ty - 36, '当天的工时', 'tb')
    x1, x2 = rx, rx + 168
    s.line(x1, ty, x2, ty, 'o1')

    def X(hh):
        return x1 + (hh - 5.5) / 16.0 * (x2 - x1)
    for hh, lab in ((5.5, '05:30'), (19.5, '19:30'), (21.5, '21:30')):
        s.line(X(hh), ty - 5, X(hh), ty + 5, 'o1')
    s.line(X(19.5), ty, X(21.5), ty, 'a o3')
    s.text(X(5.5), ty + 20, '05:30 开工', 'tm')
    s.text(X(21.5), ty + 20, '21:30 收工', 'tm', 'end')
    s.text(X(21.5), ty - 10, '19:30 看到液面', 'tm', 'end')
    s.lines(rx, 326, ['全部家当是 360 升氦气：', '200 升闭路循环，160 升备用。', '此前 26 年都在准备上游：', '1892 年液氧，1906 年液氢。'], 'tm')
    return s.svg()


# ------------------------------------------------------------------ 3 回旋加速器
def fig_cyclotron():
    s = Svg(W, H, title='伯克利五代回旋加速器与 184 英寸的磁极直径，同比例套画')
    k = 56.0
    cx, base = 372, 384
    s.text(26, 38, '磁极直径，同比例套画', 'tb')
    rows = [(0.114, '4.5 英寸', '1931', '80 keV'), (0.279, '11 英寸', '1932', '1.22 MeV'),
            (0.686, '27 英寸', '1932', '4.8 MeV，磁铁约 80 吨'), (0.94, '37 英寸', '1937', '氘核 8 MeV'),
            (1.524, '60 英寸', '1939', '氘核 16 MeV，磁铁约 220 吨'), (4.67, '184 英寸', '1946', '氘核约 200 MeV，磁铁 4,000 多吨')]
    s.ground(170, 592, base)
    ly0 = 78
    for i, (d, name, yr, note) in enumerate(reversed(rows)):
        r = d * k / 2
        big = (i == 0)
        s.circle(cx, base - r, r, 'o' if d in (4.67, 1.524) else 'o1')
        ly = ly0 + i * 47
        s.text(26, ly, name, 'tb')
        s.text(26 + 15 * 5.2, ly, yr, 'tn')
        s.text(26, ly + 16, note, 'tm')
        # 引线：从文字右端到圆的左上
        ang = math.radians(140 if big else 100)
        tx, ty = cx + r * math.cos(ang), base - r - r * math.sin(ang)
        s.leader(150 if not big else 216, ly - 4 if not big else ly + 11, tx, ty, None)
    hm = 1.75 * k
    s.man(548, base, hm)
    s.text(548, base - hm - 8, '人 1.75 米', 'tm', 'middle')
    s.dim_h(cx - 4.67 * k / 2, cx + 4.67 * k / 2, base + 14, '4.67 米', above=False)
    s.text(cx, base - 4.67 * k - 10, '1939 年获奖时最大的是 60 英寸', 'tm', 'middle')
    return s.svg()


# ------------------------------------------------------------------ 4 气泡室
def fig_bubble():
    s = Svg(W, H, title='从格拉泽的 1 英寸玻璃泡到 72 英寸液氢气泡室，同比例')
    k = 150.0
    s.text(26, 38, '逐级放大，长度同比例', 'tb')
    s.text(196, 38, '前六只的形状是示意', 'tm')
    seq = [(0.025, '约 1 英寸', '1952', '格拉泽，乙醚'), (0.038, '1.5 英寸', '1953', '第一只液氢室'), (0.064, '2.5 英寸', '', ''),
           (0.102, '4 英寸', '1954', '上加速器取数'), (0.254, '10 英寸', '', ''), (0.381, '15 英寸', '', '72 英寸的样机')]
    x = 34
    by = 118
    for L, name, yr, note in seq:
        w, h = L * k, L * k * 0.42
        s.rect(x, by - h, w, h, 'o1 fs')
        s.text(x + w / 2, by + 17, name, 'ts', 'middle')
        if yr:
            s.text(x + w / 2, by + 32, yr, 'tn', 'middle')
        if note and L < 0.03:
            s.text(x + w / 2, by + 47, '格拉泽', 'ts', 'middle')
        x += max(w, 34) + 34
    s.line(34, by + 0.5, x - 30, by + 0.5, 'dim')
    # 72 英寸
    bw, bh = 1.83 * k, 0.51 * k
    bx, bb = 34, 352
    s.rect(bx, bb - bh, bw, bh, 'o fs', rx=6)
    s.rect(bx + 5, bb - bh + 5, bw - 10, bh - 10, 'fa', rx=3)
    # 几条径迹
    s.path(f'M{f(bx + 8)} {f(bb - 30)}C{f(bx + 90)} {f(bb - 34)} {f(bx + 170)} {f(bb - 44)} {f(bx + bw - 10)} {f(bb - 62)}', 'a o1')
    s.path(f'M{f(bx + 8)} {f(bb - 48)}C{f(bx + 70)} {f(bb - 50)} {f(bx + 110)} {f(bb - 46)} {f(bx + 128)} {f(bb - 40)}', 'a o1')
    s.path(f'M{f(bx + 128)} {f(bb - 40)}C{f(bx + 170)} {f(bb - 30)} {f(bx + 215)} {f(bb - 26)} {f(bx + bw - 12)} {f(bb - 16)}', 'a o1')
    s.path(f'M{f(bx + 128)} {f(bb - 40)}c18 -12 34 -6 30 8c-4 12 -22 12 -22 2c0 -7 10 -8 12 -2', 'a o1')
    s.dim_h(bx, bx + bw, bb + 14, '72 英寸（1.83 米）', above=False)
    s.dim_v(bx + bw + 14, bb - bh, bb, '0.51 米', left=False)
    s.text(bx, bb - bh - 10, '72 英寸液氢气泡室，1959', 'tb')
    s.lines(bx, bb + 52, ['内腔深 0.38 米，装液氢约 354 升；磁场 1.8 特斯拉；整机 240 吨。', '蓝线示意带电粒子在磁场里留下的气泡径迹。'], 'tm')
    hm = 1.75 * k
    s.man(520, bb, hm)
    s.text(520, bb - hm - 8, '人 1.75 米', 'tm', 'middle')
    return s.svg()


# ------------------------------------------------------------------ 5 剑桥
def fig_cambridge():
    s = Svg(W, H, title='剑桥一英里望远镜与行星际闪烁阵的平面，同比例')
    k = 0.30
    x0, y = 52, 92
    s.text(26, 38, '平面，同比例', 'tb')
    xa, xb, xc = x0, x0 + 800 * k, x0 + 1600 * k
    # 铁轨
    s.line(xb, y - 3, xc, y - 3, 'o2')
    s.line(xb, y + 3, xc, y + 3, 'o2')
    for i in range(0, 17):
        xx = xb + i * (xc - xb) / 16
        s.line(xx, y - 5, xx, y + 5, 'o2')
    s.line(xa, y, xb, y, 'dim')
    for xx in (xa, xb):
        s.circle(xx, y, 5, 'o fs')
    for xx in (xb + 90, xb + 170):
        s.circle(xx, y, 4, 'o2 fs')
    s.circle(xc - 34, y, 5, 'o fa')
    s.text(xa, y - 14, '固定', 'ts', 'middle')
    s.text(xb, y - 14, '固定', 'ts', 'middle')
    s.text(xc - 34, y - 14, '可移动', 'ts', 'middle')
    s.dim_h(xa, xc, y + 30, '最长基线约 1.6 公里（1 英里）', above=False)
    s.dim_h(xb, xc, y + 62, '铁轨 800 米', above=False)
    s.dim_h(xa, xb, y + 62, '约 800 米（推算）', above=False)
    # 闪烁阵
    ay = 228
    aw, ah = 470 * k, 45 * k
    s.rect(x0, ay, aw, ah, 'o1 fa')
    for i in (1, 2, 3):
        s.line(x0, ay + i * ah / 4, x0 + aw, ay + i * ah / 4, 'o2')
    s.text(x0, ay - 10, '行星际闪烁阵，1967', 'tb')
    s.lines(x0, ay + ah + 20, ['约 470 米 × 45 米，16 排共 2,048 个偶极子', '（1968 年论文的数字，原文没能打开核对）；', '1,000 多根木桩；贝尔的说法是 4.5 英亩。'], 'tm')
    fx = x0 + aw + 46
    s.rect(fx, ay - 3, 105 * k, 68 * k, 'o1 d')
    s.text(fx + 105 * k + 8, ay + 12, '足球场', 'ts')
    s.scalebar(x0, 318, 500 * k, '500 米')
    # 右下：一面天线的立面，1 米 = 5 像素
    kd = 5.0
    dx, db = 470, 396
    s.ground(396, 592, db)
    s.poly([(dx - 12, db), (dx + 12, db), (dx + 5, db - 46), (dx - 5, db - 46)], 'o1 fs')
    R = 9 * kd
    s.path(f'M{f(dx - R)} {f(db - 84)}Q{f(dx)} {f(db - 34)} {f(dx + R)} {f(db - 84)}', 'o')
    s.line(dx - R, db - 84, dx + R, db - 84, 'o2')
    s.line(dx, db - 59, dx, db - 100, 'o1')
    s.circle(dx, db - 100, 2.5, 'af')
    s.dim_h(dx - R, dx + R, db - 110, '口径 18 米，重 120 吨')
    s.man(dx + 70, db, 1.75 * kd)
    s.text(dx + 78, db - 4, '人', 'ts')
    # 左下：地球自转合成口径
    ux, uy = 100, 376
    for r in (10, 19, 28, 37, 46):
        s.ellipse(ux, uy, r, r * 0.52, 'a o2' if r == 46 else 'o2')
    s.lines(ux + 62, uy - 6, ['地球自转半圈，一条基线在天上', '扫出一圈；挪一次天线，再多两圈。'], 'ts')
    return s.svg()


# ------------------------------------------------------------------ 6 质子–反质子对撞机
def fig_spps():
    s = Svg(W, H, title='CERN 的 SPS、PS 与反质子积累环，同比例；右下是 UA1 探测器')
    k = 0.148
    cx, cy = 196, 232
    R = 6900 / (2 * math.pi) * k
    s.text(26, 38, '平面，同比例', 'tb')
    s.circle(cx, cy, R, 'o')
    s.circle(cx, cy, R - 5, 'a o2')
    # 反向运行的两束
    for ang, sgn in ((60, 1), (240, 1), (150, -1), (330, -1)):
        a1 = math.radians(ang)
        rr = R + 10 if sgn > 0 else R - 15
        x1, y1 = cx + rr * math.cos(a1), cy - rr * math.sin(a1)
        a2 = a1 + sgn * 0.16
        x2, y2 = cx + rr * math.cos(a2), cy - rr * math.sin(a2)
        s.arrow(x1, y1, x2, y2, 'o1' if sgn > 0 else 'a o1', 6)
    s.text(cx, cy - 16, 'SPS', 'tb', 'middle')
    s.text(cx, cy + 4, '周长约 6.9 公里', 't', 'middle')
    s.lines(cx, cy + 26, ['质子与反质子共用一根', '真空管，反向运行'], 'tm', 'middle')
    # UA1 与 UA2
    for ang, name in ((205, 'UA1'), (255, 'UA2')):
        a1 = math.radians(ang)
        x1, y1 = cx + R * math.cos(a1), cy - R * math.sin(a1)
        s.rect(x1 - 5, y1 - 5, 10, 10, 'af')
        s.text(x1 + (-12 if ang < 230 else 12), y1 + (4 if ang < 230 else 20), name, 'tb', 'end' if ang < 230 else 'start')
    # PS 与 AA（同比例，很小）
    rp = 628 / (2 * math.pi) * k
    ra = 157 / (2 * math.pi) * k
    px, py = cx + R * math.cos(math.radians(20)) + 26, cy - R * math.sin(math.radians(20)) - 6
    s.circle(px, py, rp, 'o1 fs')
    s.circle(px + rp + 9, py + 6, ra, 'a o1')
    s.line(px - rp, py + 2, cx + R * math.cos(math.radians(14)), cy - R * math.sin(math.radians(14)), 'o2')
    s.scalebar(26, 58, 1000 * k, '1 公里')
    # 右上：放大看反质子从哪来
    bx, by, bw, bh = 384, 26, 202, 204
    s.rect(bx, by, bw, bh, 'o2 d')
    s.line(px + rp + 4, py - 8, bx, by + 60, 'dim')
    s.text(bx + 8, by + 18, '放大：反质子从哪来', 'tb')
    c1x, c1y, r1 = bx + 62, by + 100, 44
    s.circle(c1x, c1y, r1, 'o1')
    s.text(c1x, c1y - 2, 'PS', 'tb', 'middle')
    s.text(c1x, c1y + 15, '628 米', 'ts', 'middle')
    c2x, c2y, r2 = bx + 150, by + 84, 11
    s.circle(c2x, c2y, r2, 'a o')
    s.arrow(c1x + r1 * 0.9, c1y - r1 * 0.44, c2x - r2 - 14, c2y, 'o1', 5)
    s.rect(c2x - r2 - 14, c2y - 4, 5, 8, 'af')
    s.text(bx + bw - 8, c2y - 20, '积累环 157 米', 'ts', 'end')
    s.lines(bx + 8, by + 162, ['每百万个质子打靶，得约 1 个', '可用的反质子；攒上一天左右', '才够往 SPS 注入一次'], 'ts', lh=15)
    # 右下：UA1 立面，1 米 = 9 像素
    kd = 9.0
    ux, ub = 420, 396
    s.ground(396, 592, ub)
    s.rect(ux, ub - 6 * kd, 10 * kd, 6 * kd, 'o fs')
    s.rect(ux + 14, ub - 6 * kd + 10, 10 * kd - 28, 6 * kd - 20, 'o1')
    s.rect(ux + 26, ub - 6 * kd + 19, 10 * kd - 52, 6 * kd - 38, 'fa')
    s.line(ux - 8, ub - 3 * kd, ux + 10 * kd + 8, ub - 3 * kd, 'a o2')
    s.man(ux + 10 * kd + 26, ub, 1.75 * kd)
    s.text(ux, ub - 6 * kd - 26, 'UA1 探测器', 'tb')
    s.text(ux, ub - 6 * kd - 9, '约 10 × 6 × 6 米，2,000 吨', 'tm')
    return s.svg()


# ------------------------------------------------------------------ 7 Homestake
def fig_homestake():
    s = Svg(W, H, title='Homestake 金矿里的氯探测器：左为深度剖面，右为洞室与罐体，各按比例')
    k = 0.21
    gx, gy = 108, 60
    s.text(26, 38, '深度剖面', 'tb')
    s.ground(26, 228, gy)
    depth = 1478
    yb = gy + depth * k
    s.add(f'<rect x="26" y="{f(gy + 1)}" width="202" height="{f(yb - gy + 22)}" fill="url(#pat-rock)" class="pf faint"/>')
    s.rect(gx - 4, gy, 8, yb - gy, 'o1 fs')                       # 竖井
    s.poly([(gx - 9, gy), (gx + 9, gy), (gx + 4, gy - 20), (gx - 4, gy - 20)], 'o1 fs')   # 井架
    for dm in (0, 500, 1000, 1478):
        yy = gy + dm * k
        s.line(gx - 30, yy, gx - 6, yy, 'dim')
        s.text(gx - 34, yy + (4.5 if dm else 16), f'{dm:,} 米' if dm else '地面', 'tn', 'end')
    # 参照：上海中心大厦 632 米，倒着叠两座多
    tx = 176
    th = 632 * k
    for i in range(2):
        s.tower(tx, gy + i * th, th, 26, 'o1 d fs', up=False)
    s.poly([(tx - 13, gy + 2 * th), (tx + 13, gy + 2 * th), (tx + 9.5, yb), (tx - 9.5, yb)], 'o1 d fs', close=False)
    s.lines(tx + 20, gy + th + 2, ['倒着叠 2.3 座', '上海中心大厦', '（每座 632 米）'], 'ts')
    s.rect(gx + 4, yb - 5, 22, 7, 'af')
    s.text(gx - 34, yb + 22, '洞室', 'tb', 'end')
    # 右：洞室放大，1 米 = 15 像素
    kd = 14.4
    cx0, cb = 304, 318
    cw, ch = 18.3 * kd, 9.8 * kd
    s.text(cx0, 38, '洞室与罐体（放大）', 'tb')
    s.add(f'<rect x="{f(cx0 - 14)}" y="{f(cb - ch - 14)}" width="{f(cw + 28)}" height="{f(ch + 28)}" fill="url(#pat-rock)" class="pf"/>')
    s.rect(cx0, cb - ch, cw, ch, 'o fs')
    tl, td = 14.6 * kd, 6.1 * kd
    tx0 = cx0 + (cw - tl) / 2
    tyb = cb - 12
    s.rect(tx0, tyb - td, tl, td, 'o fa', rx=td / 2 * 0.5)
    s.line(tx0 + 30, tyb - td, tx0 + 30, tyb - td - 18, 'o1')
    s.line(tx0 + 30, tyb - td - 18, tx0 + 78, tyb - td - 18, 'o1')
    for (ax_, ay_) in ((0.3, 0.4), (0.55, 0.62), (0.74, 0.3)):
        s.circle(tx0 + tl * ax_, tyb - td * ay_, 2.6, 'af')
    s.text(tx0 + tl / 2, tyb - td / 2 + 5, '615 吨四氯乙烯', 't', 'middle')
    s.man(cx0 + cw - 16, cb, 1.75 * kd)
    s.dim_h(tx0, tx0 + tl, cb + 30, '罐长约 14.6 米，直径约 6.1 米（通行口径）', above=False)
    s.dim_h(cx0, cx0 + cw, cb - ch - 24, '洞室 18.3 × 9.1 × 9.8 米')
    s.lines(cx0, cb + 66, ['罐里约 2×10³⁰ 个氯-37 原子。每两个月用氦气', '吹一遍，平均捞出 17 个氩-37 原子（蓝点示意）。'], 'tm')
    return s.svg()


# ------------------------------------------------------------------ 8 COBE
def fig_cobe():
    s = Svg(W, H, title='COBE 卫星立面，按比例；虚线是航天飞机方案的外廓')
    k = 50.0
    cx, base = 236, 372
    s.text(26, 38, '立面，同比例', 'tb')
    hh = 5.49 * k
    wb = 2.44 * k
    # 航天飞机方案外廓（虚线）
    s.rect(cx - 4.6 * k / 2, base - 5.5 * k, 4.6 * k, 5.5 * k, 'o2 d')
    s.lines(cx - 4.6 * k / 2 - 8, base - 5.5 * k + 14, ['航天飞机方案', '直径 4.6 米', '约 4.5 吨'], 'ts', 'end')
    # 太阳翼
    span = 8.53 * k
    wy = base - 96
    for sgn in (-1, 1):
        x1 = cx + sgn * wb / 2
        x2 = cx + sgn * span / 2
        xl, xr = min(x1, x2), max(x1, x2)
        s.rect(xl, wy, xr - xl, 16, 'o1 fs')
        for j in (1, 2):
            xx = xl + (xr - xl) * j / 3
            s.line(xx, wy, xx, wy + 16, 'o2')
    # 星体下段
    bh = 2.3 * k
    s.rect(cx - wb / 2, base - bh, wb, bh, 'o fs')
    s.line(cx - wb / 2, base - bh * 0.5, cx + wb / 2, base - bh * 0.5, 'o2')
    # 杜瓦与遮阳罩
    dw, dh = 1.7 * k, hh - bh - 0.25 * k
    dy = base - bh - dh
    s.poly([(cx - wb / 2, base - bh), (cx - 2.0 * k, dy - 8), (cx + 2.0 * k, dy - 8), (cx + wb / 2, base - bh)], 'o1', close=False)
    s.rect(cx - dw / 2, dy, dw, dh, 'o fa', rx=10)
    s.text(cx, dy + dh / 2 - 4, '杜瓦', 'tb', 'middle')
    s.text(cx, dy + dh / 2 + 14, '650 升超流氦', 'ts', 'middle')
    # 仪器
    s.poly([(cx - 9, dy), (cx - 20, dy - 20), (cx + 2, dy - 20), (cx - 5, dy)], 'o1 fs')       # FIRAS 喇叭
    s.rect(cx + 14, dy - 14, 16, 14, 'o1 fs')                                                 # DIRBE
    for sgn in (-1, 1):
        s.rect(cx + sgn * (dw / 2 + 9) - 6, dy + 22, 12, 20, 'o1 fs')                         # DMR
    s.line(cx, base, cx, base + 0, 'o1')
    s.leader(404, dy - 44, cx - 9, dy - 21, 'FIRAS：量谱，自带黑体标尺', 'start')
    s.leader(404, dy - 22, cx + 30, dy - 7, 'DIRBE：红外背景', 'start')
    s.leader(404, dy + 4, cx + dw / 2 + 15, dy + 26, 'DMR：量两块天区之差', 'start')
    s.dim_v(cx + 2.0 * k + 30, base - hh, base, '5.49 米', left=False)
    s.text(cx, base - bh / 2 + 22, '发射质量 2,270 公斤', 'ts', 'middle')
    s.dim_h(cx - wb / 2, cx + wb / 2, base + 14, '收拢直径 2.44 米', above=False)
    s.dim_h(cx - span / 2, cx + span / 2, base + 36, '太阳翼展开 8.53 米', above=False)
    hm = 1.75 * k
    s.man(556, base, hm)
    s.text(556, base - hm - 8, '人', 'tm', 'middle')
    # 轨道小图
    ox, oy, re_ = 520, 150, 24
    s.circle(ox, oy, re_, 'o1 fs')
    s.circle(ox, oy, re_ * (6371 + 900) / 6371.0, 'a o1')
    s.text(ox, oy + 4, '地球', 'ts', 'middle')
    s.text(ox, oy + re_ + 24, '轨道高 900 公里', 'ts', 'middle')
    return s.svg()


# ------------------------------------------------------------------ 9 LHC（与 SSC）
def fig_lhc():
    s = Svg(W, H, title='LHC、SPS 与被取消的 SSC，同比例；右侧是 ATLAS 与 CMS 的立面')
    k = 0.0100
    cx, cy = 186, 214
    s.text(26, 38, '平面，同比例', 'tb')
    a, b = 15300 * k, 12300 * k
    s.ellipse(cx, cy, a, b, 'o1 d')
    # 已挖的约 23 公里：占周长约 26%
    t1, t2 = math.radians(-58), math.radians(43)   # 这一段弧长约 23.0 公里
    n = 40
    pts = [(cx + a * math.cos(t1 + (t2 - t1) * i / n), cy - b * math.sin(t1 + (t2 - t1) * i / n)) for i in range(n + 1)]
    s.poly(pts, 'o3', close=False)
    s.lines(cx - a + 14, cy - b - 12, ['SSC：周长 87.1 公里（外形示意）'], 'tb')
    s.text(cx, cy + b + 26, '粗线：1993 年终止时已挖的约 23 公里', 'ts', 'middle')
    rl = 26659 / (2 * math.pi) * k
    s.circle(cx - 20, cy + 6, rl, 'o')
    s.circle(cx - 20, cy + 6, rl - 4, 'a o2')
    s.text(cx - 20, cy + 2, 'LHC', 'tb', 'middle')
    s.text(cx - 20, cy + 19, '26.7 公里', 'ts', 'middle')
    rs = 6900 / (2 * math.pi) * k
    s.circle(cx - 20 + rl - rs + 2, cy + 6 + 20, rs, 'o1 fs')
    s.leader(cx + 70, cy + 76, cx - 20 + rl - rs + 2 + rs * 0.7, cy + 6 + 20 + rs * 0.7, 'SPS，6.9 公里', 'start', 'ts')
    for ang, nm in ((90, 'ATLAS'), (270, 'CMS')):
        a1 = math.radians(ang)
        s.rect(cx - 20 + rl * math.cos(a1) - 4, cy + 6 - rl * math.sin(a1) - 4, 8, 8, 'af')
    s.scalebar(26, 404, 10000 * k, '10 公里')
    # 右：两台探测器的立面，1 米 = 3.5 像素
    kd = 3.5
    ex, eb = 402, 250
    s.text(ex, 38, '立面，同比例', 'tb')
    s.ground(ex - 10, 592, eb)
    aw, ah = 46 * kd, 25 * kd
    s.rect(ex, eb - ah, aw, ah, 'o fs')
    for j in range(1, 4):
        s.rect(ex + j * 9, eb - ah + j * 9, aw - j * 18, ah - j * 18, 'o2')
    s.line(ex - 6, eb - ah / 2, ex + aw + 6, eb - ah / 2, 'a o2')
    s.text(ex, eb - ah - 22, 'ATLAS', 'tb')
    s.text(ex, eb - ah - 6, '46 × 25 米，7,000 吨', 'ts')
    s.man(ex + aw + 14, eb, 1.75 * kd)
    eb2 = 372
    s.ground(ex - 10, 592, eb2)
    cw, chh = 21 * kd, 15 * kd
    s.rect(ex, eb2 - chh, cw, chh, 'o fs')
    s.rect(ex + 12, eb2 - chh + 12, cw - 24, chh - 24, 'fa')
    s.line(ex - 6, eb2 - chh / 2, ex + cw + 6, eb2 - chh / 2, 'a o2')
    s.text(ex + cw + 14, eb2 - chh + 12, 'CMS', 'tb')
    s.text(ex + cw + 14, eb2 - chh + 29, '21 × 15 米', 'ts')
    s.text(ex + cw + 14, eb2 - chh + 45, '14,000 吨', 'ts')
    s.lines(ex, eb2 + 22, ['环在地下 50–175 米。', 'ATLAS 高 25 米，约 14 个人叠起来。'], 'ts', lh=16)
    return s.svg()


# ------------------------------------------------------------------ 10 超级神冈与 SNO
def fig_superk():
    s = Svg(W, H, title='超级神冈水罐与 SNO 洞室、亚克力球的立面，同比例')
    k = 5.3
    base = 384
    s.text(26, 38, '立面，同比例', 'tb')
    # 超级神冈
    x0 = 40
    tw, th = 39.3 * k, 41.4 * k
    top = base - th
    s.add(f'<rect x="{f(x0 - 14)}" y="{f(top - 30)}" width="{f(tw + 28)}" height="{f(th + 44)}" fill="url(#pat-rock)" class="pf"/>')
    s.rect(x0, top, tw, th, 'o fs')
    s.rect(x0 + 2.5 * k, top + 2.5 * k, tw - 5 * k, th - 5 * k, 'fa')
    s.rect(x0 + 2.5 * k, top + 2.5 * k, tw - 5 * k, th - 5 * k, 'o2')
    n = 14
    for i in range(n + 1):
        yy = top + 2.5 * k + (th - 5 * k) * i / n
        s.circle(x0 + 2.5 * k, yy, 2, 'af')
        s.circle(x0 + tw - 2.5 * k, yy, 2, 'af')
    for i in range(1, 13):
        xx = x0 + 2.5 * k + (tw - 5 * k) * i / 13
        s.circle(xx, top + 2.5 * k, 2, 'af')
        s.circle(xx, base - 2.5 * k, 2, 'af')
    # 一个切伦科夫光锥
    px, py = x0 + tw * 0.38, top + th * 0.62
    wx = x0 + tw - 2.5 * k
    s.line(px - 46, py + 20, px, py, 'o1')
    s.poly([(px, py), (wx, py - 62), (wx, py + 10)], 'a o2')
    s.ellipse(wx, py - 26, 4, 36, 'a o1')
    s.text(x0 + tw / 2, top + 30, '5 万吨超纯水', 't', 'middle')
    s.text(x0 + tw / 2, top - 38, '超级神冈：上方 1,000 米岩石', 'tb', 'middle')
    s.dim_h(x0, x0 + tw, base + 14, '直径 39.3 米', above=False)
    s.dim_v(x0 + tw + 16, top, base, '41.4 米', left=False)
    # 人
    s.man(x0 + tw + 60, base, 1.75 * k)
    s.text(x0 + tw + 60, base - 1.75 * k - 8, '人', 'ts', 'middle')
    # SNO
    sx = 372
    cw, ch = 22 * k, 34 * k
    ctop = base - ch
    s.add(f'<rect x="{f(sx - 14)}" y="{f(ctop - 30)}" width="{f(cw + 28)}" height="{f(ch + 44)}" fill="url(#pat-rock)" class="pf"/>')
    s.path(f'M{f(sx)} {f(base)}V{f(ctop + 20)}Q{f(sx + cw / 2)} {f(ctop - 12)} {f(sx + cw)} {f(ctop + 20)}V{f(base)}Z', 'o fs')
    ccx, ccy = sx + cw / 2, base - 13.5 * k
    s.circle(ccx, ccy, 17.8 * k / 2, 'o2 d')
    s.circle(ccx, ccy, 6 * k, 'o fa')
    s.rect(ccx - 0.75 * k, ccy - 6 * k - 6.8 * k, 1.5 * k, 6.8 * k, 'o1 fs')
    s.text(ccx, ccy - 2, '重水', 'tb', 'middle')
    s.text(ccx, ccy + 14, '1,000 吨', 'ts', 'middle')
    s.text(ccx, ctop - 38, 'SNO：上方约 2,070 米岩石', 'tb', 'middle')
    s.dim_h(sx, sx + cw, base + 14, '洞室宽 22 米', above=False)
    s.dim_v(sx + cw + 16, ctop, base, '34 米', left=False)
    s.leader(sx + cw + 22, ccy + 54, ccx + 6 * k * 0.7, ccy + 6 * k * 0.7, None)
    s.lines(sx + cw + 26, ccy + 50, ['亚克力球', '直径 12 米'], 'ts')
    s.lines(26, 60, ['蓝点：20 英寸光电倍增管（示意，实际内层 11,146 只）'], 'ts')
    return s.svg()


# ------------------------------------------------------------------ 11 LIGO
def fig_ligo():
    s = Svg(W, H, title='LIGO 一个站的平面，按比例；右侧是束流管的断面')
    k = 0.0575
    ox, oy = 78, 344
    L = 4000 * k
    s.text(26, 38, '一个站的平面，同比例', 'tb')
    s.line(ox, oy, ox + L, oy, 'o')
    s.line(ox, oy, ox, oy - L, 'o')
    s.line(ox + 3, oy - 3, ox + L, oy - 3, 'a o2')
    s.line(ox + 3, oy - 3, ox + 3, oy - L, 'a o2')
    s.rect(ox - 9, oy - 9, 18, 18, 'o fs')
    for (xx, yy) in ((ox + L, oy), (ox, oy - L)):
        s.rect(xx - 6, yy - 6, 12, 12, 'o fs')
    s.dim_h(ox, ox + L, oy + 24, '臂长 4 公里', above=False)
    s.dim_v(ox - 22, oy - L, oy, '4 公里', left=True)
    s.lines(ox + 26, oy - L + 14, ['光在每条臂里来回约 280 趟，', '等效臂长约 1,120 公里'], 'tm')
    s.lines(ox + 26, oy - 150, ['要量的臂长变化：10⁻¹⁸ 米量级', '4 公里上地面要垫平约 1 米的', '地球曲率下垂'], 'tm')
    s.leader(ox + 60, oy - 40, ox + 14, oy - 14, None)
    s.text(ox + 64, oy - 36, '激光与分束镜', 'ts')
    s.circle(ox + 150, oy - 62, 1.2, 'af')
    s.leader(ox + 172, oy - 78, ox + 151, oy - 63, None, dot=False)
    s.lines(ox + 176, oy - 82, ['1887 年的等效臂长 11 米，', '按这个比例只是一个点'], 'ts')
    s.scalebar(ox + 110, oy + 58, 1000 * k, '1 公里')
    # 右上：束流管断面，1 米 = 62 像素
    kd = 62.0
    tx, tb_ = 440, 170
    s.text(388, 38, '束流管断面，同比例', 'tb')
    s.ground(380, 592, tb_)
    s.path(f'M{f(tx - 1.55 * kd)} {f(tb_)}V{f(tb_ - 1.2 * kd)}Q{f(tx)} {f(tb_ - 2.3 * kd)} {f(tx + 1.55 * kd)} {f(tb_ - 1.2 * kd)}V{f(tb_)}', 'o2 d')
    s.circle(tx, tb_ - 0.25 * kd - 0.6 * kd, 0.6 * kd, 'o fa')
    s.circle(tx, tb_ - 0.25 * kd - 0.6 * kd, 2.2, 'af')
    s.man(tx + 1.55 * kd + 26, tb_, 1.75 * kd)
    s.lines(388, tb_ + 24, ['钢管直径 1.2 米、壁厚 3 毫米，', '外面是混凝土罩；每站抽空', '约 1 万立方米。'], 'tm')
    # 右下：两个站
    y2 = 340
    xa, xb = 392, 568
    s.line(xa, y2, xb, y2, 'dim')
    s.circle(xa, y2, 5, 'af')
    s.circle(xb, y2, 5, 'af')
    s.text(xa, y2 - 14, '汉福德', 't', 'start')
    s.text(xb, y2 - 14, '利文斯顿', 't', 'end')
    s.text((xa + xb) / 2, y2 + 22, '相距 3,002 公里', 'tm', 'middle')
    s.text((xa + xb) / 2, y2 + 39, '光行约 10 毫秒', 'tm', 'middle')
    s.text(388, y2 - 44, '两个站要先后看到', 'tb')
    return s.svg()


# ------------------------------------------------------------------ 12 IceCube
def fig_icecube():
    s = Svg(W, H, title='IceCube 的冰下剖面，按比例；右侧是光学模块与钻孔')
    k = 0.126
    gx0, gx1, gy = 96, 392, 56
    s.text(26, 38, '冰下剖面，同比例', 'tb')
    ice = 2810
    yb = gy + ice * k
    s.add(f'<rect x="{f(gx0)}" y="{f(gy)}" width="{f(gx1 - gx0)}" height="{f(1400 * k)}" fill="url(#pat-ice)" class="pf"/>')
    s.add(f'<rect x="{f(gx0)}" y="{f(yb)}" width="{f(gx1 - gx0)}" height="16" fill="url(#pat-rock)" class="pf"/>')
    s.line(gx0, gy, gx1, gy, 'o')
    s.line(gx0, yb, gx1, yb, 'o1')
    for dm in (0, 1000, 1450, 2000, 2450, 2810):
        yy = gy + dm * k
        s.line(gx0 - 6, yy, gx0, yy, 'o1')
        s.text(gx0 - 10, yy + 4.5, ('冰面' if dm == 0 else f'{dm:,} 米'), 'tn', 'end')
    # 含尘层
    s.rect(gx0, gy + 2000 * k, gx1 - gx0, 100 * k, 'fdust')
    # 缆
    cx = 216
    xs = [cx + (i - 4) * 125 * k for i in range(9)]
    y1, y2 = gy + 1450 * k, gy + 2450 * k
    for x in xs:
        s.line(x, gy, x, y1, 'o2')
        s.line(x, y1, x, y2, 'a o1')
        for j in range(0, 11):
            s.circle(x, y1 + (y2 - y1) * j / 10, 1.5, 'af')
        s.rect(x - 2.5, gy - 5, 5, 5, 'o2 fs')
    for x in (cx - 4, cx + 4):
        s.line(x, gy + 2100 * k, x, y2, 'a o1')
    s.rect(cx - 9, gy - 16, 18, 11, 'o1 fs')
    s.dim_h(xs[0], xs[-1], y2 + 16, '1 公里', above=False)
    s.dim_v(xs[-1] + 14, y1, y2, '1 公里', left=False)
    # 参照：上海中心 632 米
    tx = xs[-1] + 84
    s.tower(tx, y2, 632 * k, 12, 'o1 d fs', up=True)
    s.lines(tx - 22, y2 + 18, ['上海中心', '632 米'], 'ts')
    s.lines(gx1 + 10, gy + 500 * k, ['1,400 米以上：', '冰里有气泡，', '光走不到 1 米'], 'ts')
    s.leader(gx1 + 10, gy + 2050 * k, gx1 - 2, gy + 2050 * k, '含尘层', 'start', 'ts', dot=False)
    s.text(gx0 + 4, yb + 30, '基岩；冰厚约 2,810 米', 'ts')
    s.text(cx + 18, gy - 9, '冰面实验室与 IceTop', 'ts')
    # 右：光学模块与钻孔，1 米 = 60 像素
    kd = 60.0
    mx, mb = 532, 204
    s.text(474, 38, '模块与钻孔', 'tb')
    s.ground(468, 592, mb)
    s.man(mx - 30, mb, 1.75 * kd)
    s.circle(mx + 30, mb - 0.3 * kd, 0.3 * kd, 'o2 d')
    s.circle(mx + 30, mb - 0.3 * kd, 0.165 * kd, 'o fa')
    s.lines(474, mb + 22, ['光学模块：33 厘米的', '玻璃球，冻进 60 厘米', '的孔里，取不出来'], 'ts')
    s.lines(474, mb + 86, ['86 根缆 × 60 个', '= 5,160 个模块', '热水钻约 5 兆瓦，', '约两天一孔'], 'tm')
    return s.svg()


FIGS = {
    'michelson': fig_michelson, 'leiden': fig_leiden, 'cyclotron': fig_cyclotron, 'bubble': fig_bubble,
    'cambridge': fig_cambridge, 'spps': fig_spps, 'homestake': fig_homestake, 'cobe': fig_cobe,
    'lhc': fig_lhc, 'superk-sno': fig_superk, 'ligo': fig_ligo, 'icecube': fig_icecube,
}
