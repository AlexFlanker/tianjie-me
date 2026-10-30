# -*- coding: utf-8 -*-
"""程序绘制：九条文明泳道图、节点地图、精度阶梯、ΔT 曲线。颜色全走 CSS 令牌。"""
import math, html
import editorial as E
esc = lambda s: html.escape(str(s), quote=True)

# 分段比例尺：前 3200 年压缩，1500–2030 放大
SEGS = [(-3200, 0, 0.17), (0, 1500, 0.30), (1500, 2030, 0.53)]
def tx(year, w):
    x = 0.0
    for a, b, f in SEGS:
        if year <= a: return x * w
        if year <= b: return (x + (year - a) / (b - a) * f) * w
        x += f
    return w

SHAPE = {'year': 'circle', 'month': 'half', 'week': 'diamond', 'day': 'square', 'hour': 'tri', 'second': 'tri2'}
def marker(shape, x, y, r=5.5, cls=''):
    if shape == 'circle': return f'<circle class="mk {cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
    if shape == 'half': return f'<path class="mk {cls}" d="M{x-r:.1f} {y:.1f}A{r} {r} 0 0 1 {x+r:.1f} {y:.1f}Z"/><circle class="mk hollow" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
    if shape == 'diamond': return f'<path class="mk {cls}" d="M{x:.1f} {y-r-1:.1f}L{x+r+1:.1f} {y:.1f}L{x:.1f} {y+r+1:.1f}L{x-r-1:.1f} {y:.1f}Z"/>'
    if shape == 'square': return f'<rect class="mk {cls}" x="{x-r+.5:.1f}" y="{y-r+.5:.1f}" width="{2*r-1:.1f}" height="{2*r-1:.1f}"/>'
    if shape == 'tri': return f'<path class="mk {cls}" d="M{x:.1f} {y-r-1:.1f}L{x+r+1:.1f} {y+r:.1f}L{x-r-1:.1f} {y+r:.1f}Z"/>'
    return f'<path class="mk {cls}" d="M{x:.1f} {y+r+1:.1f}L{x+r+1:.1f} {y-r:.1f}L{x-r-1:.1f} {y-r:.1f}Z"/>'

LEAP_EVENTS = {'greg-1582', 'adoption', 'rome-julian', 'shoushi-1281', 'taichu-104bc', 'zhang-cycle', 'babylon-lunisolar', 'utc-1972', 'cgpm-2022-2026', 'republican', 'east-asia', 'roc-1912', 'us-1883', 'meridian-1884'}

def lanes_svg(nodes, W=1000):
    """nodes: 列表 [{'id','year','lane','scales','title','chapter'}]"""
    L = 150; R = 16; top = 34; rowh = 40; H = top + rowh * len(E.LANES) + 30
    pw = W - L - R
    out = [f'<svg class="dwg lanes" viewBox="0 0 {W} {H}" role="img" aria-label="九条文明泳道 × 时间">']
    # 年份刻度
    ticks = [-3000, -2000, -1000, 0, 500, 1000, 1500, 1700, 1800, 1900, 2000]
    for yv in ticks:
        x = L + tx(yv, pw)
        out.append(f'<line class="ln2" x1="{x:.1f}" y1="{top-6}" x2="{x:.1f}" y2="{H-26}"/><text class="tm tsm" x="{x:.1f}" y="{top-12}" text-anchor="middle">{"前 " + str(-yv) if yv < 0 else yv}</text>')
    # 分段提示
    for a, b, f in SEGS:
        xa, xb = L + tx(a, pw), L + tx(b, pw)
        out.append(f'<line class="o2" x1="{xa:.1f}" y1="{H-22}" x2="{xb:.1f}" y2="{H-22}"/>')
    out.append(f'<text class="tm tsm" x="{L}" y="{H-8}">比例尺分三段：前 3200–0 年压缩，0–1500 年居中，1500–2030 年放大</text>')
    # 泳道
    for i, (lid, ln) in enumerate(E.LANES):
        y = top + rowh * i + rowh / 2
        out.append(f'<line class="ln" x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}"/><text class="ts" x="{L-10}" y="{y+4:.1f}" text-anchor="end">{esc(ln)}</text>')
    # 节点（同一泳道同一年附近错开）
    placed = {}
    for n in sorted(nodes, key=lambda n: n['year']):
        li = [k for k, (lid, _) in enumerate(E.LANES) if lid == n['lane']]
        if not li: continue
        y = top + rowh * li[0] + rowh / 2
        x = L + tx(n['year'], pw)
        key = (li[0], round(x / 14))
        k = placed.get(key, 0); placed[key] = k + 1
        y2 = y + (k * 11 if k % 2 == 0 else -k * 11)
        sc = (n.get('scales') or ['year'])[0]
        cls = 'ev' if n['id'] in LEAP_EVENTS else ''
        label = n['title'].split('：')[0][:14]
        out.append(f'<g class="nd" data-node="{esc(n["id"])}" tabindex="0" role="button" aria-label="{esc(n["title"])}"><title>{esc(n["year_label"])} · {esc(n["title"])}</title>{marker(SHAPE.get(sc, "circle"), x, y2, 5.5, cls)}<text class="nl" x="{x:.1f}" y="{y2-9:.1f}" text-anchor="middle">{esc(label)}</text></g>')
    out.append('</svg>')
    return ''.join(out)

def lanes_legend():
    sc = ''.join(f'<span><svg viewBox="0 0 16 16" width="14" height="14">{marker(SHAPE[k], 8, 8, 5)}</svg>{v}</span>' for k, v in E.SCALES)
    return f'<div class="lkey2">{sc}<span><svg viewBox="0 0 16 16" width="14" height="14"><circle class="mk ev" cx="8" cy="8" r="5"/></svg>置闰 / 跳日 / 改制</span><span>点节点跳到卡片</span></div>'

def XY(lat, lon): return (lon + 180) * 2.0, (90 - lat) * 2.0
def nodes_map(nodes, world):
    dots = ''.join(f'<circle class="pd" data-node="{esc(n["id"])}" cx="{XY(n["place"]["lat"], n["place"]["lon"])[0]:.1f}" cy="{XY(n["place"]["lat"], n["place"]["lon"])[1]:.1f}" r="4"><title>{esc(n["place"]["name"])} · {esc(n["title"])}</title></circle>' for n in nodes if n.get('place') and n['place'].get('lat') is not None)
    return f'<svg class="wmap small" viewBox="0 20 720 290" preserveAspectRatio="xMidYMid slice"><path class="land" d="{world["d"]}"/><line class="gmt" x1="360" y1="0" x2="360" y2="360"/>{dots}</svg>'

def ladder_svg(ladder, W=1000):
    """精度阶梯：每天误差（秒）的对数尺。ladder 每级含 name/year/err_s_per_day（秒 / 天，可为 None）。"""
    H = 230; L = 30; R = 30; pw = W - L - R
    lo, hi = -14, 3  # log10 秒/天：10^-14 … 10^3
    def X(v): return L + (math.log10(v) - lo) / (hi - lo) * pw
    out = [f'<svg class="dwg ladder" viewBox="0 0 {W} {H}">']
    for e in range(lo, hi + 1):
        x = X(10 ** e); lab = {3: '1000 s', 2: '100 s', 1: '10 s', 0: '1 s', -1: '0.1 s', -2: '10 ms', -3: '1 ms', -4: '0.1 ms', -5: '10 μs', -6: '1 μs', -7: '0.1 μs', -8: '10 ns', -9: '1 ns', -10: '0.1 ns', -11: '10 ps', -12: '1 ps', -13: '0.1 ps', -14: '10 fs'}.get(e, '')
        out.append(f'<line class="{"dec" if e % 3 == 0 else "dec2"}" x1="{x:.1f}" y1="120" x2="{x:.1f}" y2="{134 if e % 3 == 0 else 128}"/>')
        if e % 3 == 0: out.append(f'<text class="tm tsm" x="{x:.1f}" y="150" text-anchor="middle">{lab}</text>')
    out.append(f'<line class="o" x1="{L}" y1="120" x2="{W-R}" y2="120"/><text class="tm tsm" x="{L}" y="172">每天差多少秒（对数尺，向左每格精一千倍）</text>')
    lvl = 0
    for it in sorted([l for l in ladder if l.get('err_s_per_day')], key=lambda l: -l['err_s_per_day']):
        x = X(it['err_s_per_day']); y = 100 - (lvl % 3) * 28; lvl += 1
        out.append(f'<g class="tick" tabindex="0"><title>{esc(it["name"])} · {esc(it.get("year",""))} · {esc(it.get("note",""))}</title><line class="o2" x1="{x:.1f}" y1="{y+4}" x2="{x:.1f}" y2="120"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5"/><text class="ts tsm" x="{x:.1f}" y="{y-8}" text-anchor="middle">{esc(it["short"])}</text></g>')
    out.append('</svg>')
    return ''.join(out)

def dt_svg(points, leaps, W=1000):
    """ΔT 曲线 1900–2030 + 闰秒刻度。points: [(year, dt_s)]；leaps: [year.frac]"""
    H = 260; L = 50; R = 20; T = 20; B = 50
    x = lambda yv: L + (yv - 1900) / 130 * (W - L - R)
    y = lambda v: T + (75 - v) / 85 * (H - T - B)
    out = [f'<svg class="dwg dtfig" viewBox="0 0 {W} {H}">']
    for v in (-10, 0, 20, 40, 60, 70): out.append(f'<line class="ln2" x1="{L}" y1="{y(v):.1f}" x2="{W-R}" y2="{y(v):.1f}"/><text class="tm tsm" x="{L-6}" y="{y(v)+4:.1f}" text-anchor="end">{v}</text>')
    for yv in range(1900, 2031, 10): out.append(f'<text class="tm tsm" x="{x(yv):.1f}" y="{H-B+16}" text-anchor="middle">{yv}</text>')
    d = 'M' + ' L'.join(f'{x(a):.1f} {y(b):.1f}' for a, b in points)
    out.append(f'<path class="day" d="{d}"/>')
    for ly in leaps: out.append(f'<line class="a" x1="{x(ly):.1f}" y1="{H-B}" x2="{x(ly):.1f}" y2="{H-B-14}" stroke-width="2"/>')
    out.append(f'<text class="ts tsm" x="{x(1972):.1f}" y="{H-B+30}">▲ 27 次闰秒（1972–2016）</text><text class="tm tsm" x="{L}" y="{T-6}">ΔT = TT − UT1（秒）</text>')
    out.append(f'<line class="o2 d" x1="{x(2027.4):.1f}" y1="{T}" x2="{x(2027.4):.1f}" y2="{H-B}"/><text class="ts tsm" x="{x(2027.4)+4:.1f}" y="{T+14}">2027-05-20 连续 UTC</text>')
    out.append('</svg>')
    return ''.join(out)

# ---------- v2 序章舞台：晨昏线世界地图（2026-10-30）
def day_poly(decl, sslon, step=3):
    """白天半球的多边形（等经纬投影 720×360）：晨昏线 tan φ = −cos(λ − λs) / tan δ；北半球夏天往上封口，冬天往下封口。与 app.js 同式。"""
    d = decl if abs(decl) > 0.2 else (0.2 if decl >= 0 else -0.2)
    td = math.tan(math.radians(d)); pts = []
    for lam in range(-186, 187, step):
        phi = math.degrees(math.atan(-math.cos(math.radians(lam - sslon)) / td))
        pts.append(((lam + 180) * 2, (90 - phi) * 2))
    edge = -40 if d > 0 else 400
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + f' L{pts[-1][0]:.1f} {edge} L{pts[0][0]:.1f} {edge}Z'

def stage_map(cities, img_src, s0):
    """序章舞台：NASA「蓝色弹珠」日间图 + 夜半球的暗罩（晨昏线处羽化）+ 太阳直射点 + 1884 年后的格林尼治子午线 + 十二城。
    视窗（viewBox）由 app.js 的「镜头」按每一步变化的城市推进；标签也由 app.js 按像素避让后再摆，这里只给首选方位（data-off）。"""
    OFF = {'rome': 'b', 'london': 'l', 'paris': 'r', 'istanbul': 'r', 'cairo': 'b', 'moscow': 't', 'delhi': 'b', 'beijing': 'r', 'urumqi': 't', 'tokyo': 'r', 'new-york': 't', 'mexico-city': 'b'}
    dots = ''.join(f'<g class="cdot" data-city="{esc(c["id"])}" data-x="{XY(c["lat"], c["lon"])[0]:.1f}" data-y="{XY(c["lat"], c["lon"])[1]:.1f}" data-off="{OFF.get(c["id"], "t")}" transform="translate({XY(c["lat"], c["lon"])[0]:.1f} {XY(c["lat"], c["lon"])[1]:.1f})"><circle class="g" r="16" fill="url(#lampglow)"/><circle class="c" r="3.2"/><text x="0" y="-8">{esc(c["name"])}</text></g>' for c in cities)
    sx, sy = XY(s0['decl'], s0['sslon'])
    bg = '#05080F'
    return (f'<svg class="wmap" id="wmap" viewBox="0 0 720 360" preserveAspectRatio="xMidYMid meet" role="img" aria-label="世界地图：格林尼治平太阳正午这一刻的白天与黑夜，十二座城的位置">'
            f'<defs><filter id="tblur" filterUnits="userSpaceOnUse" x="-120" y="-120" width="960" height="600"><feGaussianBlur stdDeviation="5"/></filter>'
            f'<mask id="nightm" maskUnits="userSpaceOnUse" x="-2200" y="-1100" width="5120" height="2560"><rect x="-2200" y="-1100" width="5120" height="2560" fill="#fff"/><path id="daypoly" fill="#000" filter="url(#tblur)" d="{day_poly(s0["decl"], s0["sslon"])}"/></mask>'
            f'<linearGradient id="mapfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{bg}" stop-opacity="0"/><stop offset="1" stop-color="{bg}"/></linearGradient>'
            f'<linearGradient id="mapfadeT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{bg}"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="mapfadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{bg}"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="mapfadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{bg}" stop-opacity="0"/><stop offset="1" stop-color="{bg}"/></linearGradient>'
            f'<radialGradient id="lampglow"><stop offset="0" stop-color="#E6BC6A" stop-opacity=".9"/><stop offset=".45" stop-color="#E6BC6A" stop-opacity=".35"/><stop offset="1" stop-color="#E6BC6A" stop-opacity="0"/></radialGradient></defs>'
            f'<rect x="-2160" y="-1080" width="5040" height="2520" fill="{bg}"/>'
            f'<image class="dayimg" href="{esc(img_src)}" x="0" y="0" width="720" height="360" preserveAspectRatio="none"/>'
            f'<rect class="shade" x="-2160" y="-1080" width="5040" height="2520" mask="url(#nightm)"/>'
            f'<rect x="-2" y="-2" width="724" height="26" fill="url(#mapfadeT)"/><rect x="-2" y="-2" width="26" height="364" fill="url(#mapfadeL)"/><rect x="696" y="-2" width="26" height="364" fill="url(#mapfadeR)"/>'
            f'<rect x="-720" y="318" width="2160" height="44" fill="url(#mapfade)"/><rect x="-720" y="360" width="2160" height="400" fill="{bg}"/>'
            f'<line class="gmt{" on" if s0["gmt"] else ""}" id="gmtline" x1="360" y1="8" x2="360" y2="352"/><text class="gmtl{" on" if s0["gmt"] else ""}" id="gmtlab" x="364" y="20">格林尼治 0°</text>'
            f'<g class="ss" id="ssmark" transform="translate({sx:.1f} {sy:.1f})"><circle r="6"/><circle r="2" style="fill:#FFE2A6;stroke:none"/><text x="0" y="-11">直射点</text></g>'
            f'{dots}</svg>')
