# -*- coding: utf-8 -*-
"""程序绘制：对数速度尺、两条总线图、赛道小图标。颜色一律走 CSS 类（模板里的令牌），不写死十六进制。"""
import math, html

def esc(s): return html.escape(str(s), quote=True)

SUP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
def sup(n): return ''.join(SUP[c] for c in str(n))

def fmt(v):
    if v >= 1e8: return f'{v/1e8:.4g} 亿'
    if v >= 10000: return f'{v:,.0f}'
    if v >= 100: return f'{v:,.0f}'
    if v >= 10: return f'{v:.1f}'.rstrip('0').rstrip('.')
    return f'{v:.2f}'.rstrip('0').rstrip('.')

# ---------- 对数速度尺（卷首）
SHORT = {'bolt': '博尔特', 'horse': '赛马', 'cheetah': '猎豹', 'bike_drafted': '领骑自行车', 'hsr': '高铁', 'falcon': '游隼俯冲', 'airliner': '客机巡航',
         'sound': '音速', 'stratos': '鲍姆加特纳', 'concorde': '协和', 'sr71': 'SR-71', 'x15': 'X-15', 'orbital': '第一宇宙速度', 'apollo10': 'Apollo 10', 'parker': '帕克探测器', 'light': '光速', 'walk': '步行'}
def ruler_svg(scale):
    W, H = 1400, 300
    x0, x1 = 70, 1340
    lo, hi = 0.0, 9.3  # log10 km/h
    def X(v): return x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)
    base = 152
    out = [f'<svg class="dwg ruler" viewBox="0 0 {W} {H}" role="img" aria-label="从步行到光速的对数速度尺">']
    for d in range(0, 10):
        x = X(10 ** d)
        out.append(f'<line class="dec" x1="{x:.1f}" y1="{base-22}" x2="{x:.1f}" y2="{base+22}"/>')
        out.append(f'<text class="tm" x="{x:.1f}" y="{base+40}" text-anchor="middle">10{sup(d)}</text>')
        for k in range(2, 10):
            if 10 ** d * k > 10 ** hi: break
            xx = X(10 ** d * k)
            out.append(f'<line class="dec2" x1="{xx:.1f}" y1="{base-9}" x2="{xx:.1f}" y2="{base+9}"/>')
    out.append(f'<line class="o" x1="{x0-20}" y1="{base}" x2="{x1+20}" y2="{base}"/>')
    out.append(f'<text class="tm tsm" x="{x0-20}" y="20" text-anchor="start">km/h · 对数刻度，每大格 ×10</text>')
    items = sorted(scale, key=lambda s: s['kmh'])
    # 贪心排标签：上下两侧各三层，同侧同层相邻标签至少隔 92px
    last = {(side, lvl): -999 for side in (0, 1) for lvl in (0, 1, 2)}
    for i, s in enumerate(items):
        x = X(s['kmh'])
        pref = i % 2
        placed = None
        for lvl in (0, 1, 2):
            for side in (pref, 1 - pref):
                if x - last[(side, lvl)] >= 92: placed = (side, lvl); break
            if placed: break
        if not placed: placed = (pref, 2)
        side, lvl = placed; last[placed] = x
        dy = -1 if side == 0 else 1
        ty = base + dy * (46 + lvl * 30)
        lab = SHORT.get(s['id'], s['label'])
        out.append(f'<g class="tick" data-id="{esc(s["id"])}" tabindex="0" role="button" aria-label="{esc(s["label"])} {fmt(s["kmh"])} km/h">')
        out.append(f'<line class="o2" x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{ty + (6 if dy<0 else -13)}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{base}" r="5"/>')
        out.append(f'<text x="{x:.1f}" y="{ty}" text-anchor="middle">{esc(lab)}</text>')
        vy = ty + 14 if dy > 0 else ty - 14
        out.append(f'<text class="ts tsm" x="{x:.1f}" y="{vy}" text-anchor="middle">{fmt(s["kmh"])}</text>')
        out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out)

# ---------- 两条总线
def lines_svg(record, daily):
    W, H = 1200, 460
    x0, x1, y0, y1 = 70, 1150, 30, 400
    ylo, yhi = 0.6, 5.0  # log10
    ya, yb = 1790, 2032
    def X(y): return x0 + (max(y, ya) - ya) / (yb - ya) * (x1 - x0)
    def Y(v): return y1 - (math.log10(v) - ylo) / (yhi - ylo) * (y1 - y0)
    out = [f'<svg class="dwg" viewBox="0 0 {W} {H}" role="img" aria-label="两条总线：人类乘坐过的最快速度与普通人日常能坐到的最快速度，1800 年至今">']
    for d in range(1, 6):
        y = Y(10 ** d)
        out.append(f'<line class="ln" x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}"/>')
        out.append(f'<text class="tm" x="{x0-8}" y="{y+4:.1f}" text-anchor="end">10{sup(d)}</text>')
        for k in (2, 5):
            yy = Y(10 ** d * k)
            if yy > y0: out.append(f'<line class="ln2" x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}"/>')
    for yr in range(1800, 2040, 20):
        x = X(yr)
        out.append(f'<line class="ln2" x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}"/>')
        out.append(f'<text class="tm" x="{x:.1f}" y="{y1+20}" text-anchor="middle">{yr}</text>')
    out.append(f'<text class="tm tsm" x="{x0-8}" y="{y0-10}" text-anchor="end">km/h</text>')
    # 协和退役的回落用阴影标出
    out.append(f'<rect class="fw" x="{X(1976):.1f}" y="{y0}" width="{X(2003)-X(1976):.1f}" height="{y1-y0}"/>')
    out.append(f'<text class="tm tsm" x="{(X(1976)+X(2003))/2:.1f}" y="{y0+16}" text-anchor="middle">协和 1976–2003</text>')
    def poly(pts, cls, step=False):
        p = []
        prev = None
        for pt in pts:
            x, y = X(pt['year']), Y(pt['kmh'])
            if step and prev is not None: p.append(f'{x:.1f},{prev:.1f}')
            p.append(f'{x:.1f},{y:.1f}')
            prev = y
        return f'<polyline class="{cls}" points="{" ".join(p)}"/>'
    rec = sorted(record, key=lambda p: p['year'])
    day = sorted(daily, key=lambda p: p['year'])
    out.append(poly(day, 'day', step=True))
    out.append(poly([p for p in rec if not p.get('flat')] + [dict(year=2030, kmh=max(p['kmh'] for p in rec))], 'rec', step=True))
    # 标签（手工错位）
    OFF = {'rec': {-3000: (8, -8), 1829: (8, -8), 1903: (-8, -10), 1939: (-8, -10), 1947: (8, -8), 1956: (10, -6), 1961: (10, 4), 1967: (10, 16), 1969: (-10, -10), 2026: (-8, 20)},
           'day': {1800: (8, 18), 1830: (8, 18), 1900: (-8, 18), 1935: (-8, 18), 1958: (8, 18), 1976: (8, 16), 2003: (-10, 18), 2008: (8, 18), 2017: (0, 0), 2026: (-6, -10)}}
    for pt in rec:
        x, y = X(pt['year']), Y(pt['kmh'])
        out.append(f'<circle class="pt" cx="{x:.1f}" cy="{y:.1f}" r="4.5"/>' if not pt.get('flat') else f'<circle class="pt d" cx="{x:.1f}" cy="{y:.1f}" r="5.5"/>')
        dx, dy = OFF['rec'].get(pt['year'], (6, -8))
        anchor = 'end' if dx < 0 else 'start'
        lab = pt.get('short') or pt['label']
        out.append(f'<text class="ts tsm" x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}">{esc(lab)} · {fmt(pt["kmh"])}</text>')
    for pt in day:
        x, y = X(pt['year']), Y(pt['kmh'])
        out.append(f'<circle class="pt2" cx="{x:.1f}" cy="{y:.1f}" r="4"/>')
        dx, dy = OFF['day'].get(pt['year'], (6, 16))
        if dx == 0 and dy == 0: continue
        anchor = 'end' if dx < 0 else 'start'
        lab = pt.get('short') or pt['label']
        out.append(f'<text class="ts tsm" x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}">{esc(lab)} · {fmt(pt["kmh"])}</text>')
    out.append('</svg>')
    return '\n'.join(out)

# ---------- 赛道小图标（剪影，不画商标）
GLYPHS = {
    'road': '<path class="glyph" d="M3 14l2-5h10l3 5h2v4h-2a2 2 0 0 1-4 0H8a2 2 0 0 1-4 0H2v-4zM6 13h9l-1.6-3H7.2z"/>',
    'rail': '<path class="glyph" d="M4 5h12a3 3 0 0 1 3 3v6a2 2 0 0 1-2 2l1.5 2h-2l-1-2H8.5l-1 2h-2L7 16a2 2 0 0 1-2-2V8a3 3 0 0 1 3-3h-4zm2 3v4h11V8a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z"/>',
    'water': '<path class="glyph" d="M3 15h18l-2 4H5zM6 13l1-6h5l5 6zM13 8l3 5h-3z"/>',
    'air': '<path class="glyph" d="M2 13l8-1 4-8h2l-1 8 6 1v2l-6 1 1 4h-2l-3-4-9 1z"/>',
    'space': '<path class="glyph" d="M12 2c3 2 4 7 4 11l3 4h-5l-2 3-2-3H5l3-4c0-4 1-9 4-11zm0 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>',
    'body': '<path class="glyph" d="M14 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM9 8l4 1 3 3-2 3 4 4-2 1-4-4-2 2-1 4H7l1-5 3-3-2-2-4 2-1-2z"/>',
}
def glyph(track):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{GLYPHS[track]}</svg>'
