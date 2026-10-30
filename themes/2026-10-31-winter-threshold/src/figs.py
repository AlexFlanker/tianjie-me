# -*- coding: utf-8 -*-
"""程序绘制：年轮（第二章 / 年轮墙）、序章舞台地图（NASA 夜光图 + 纬度夜带 + 城市灯）。只画抽象图形，颜色全走 CSS 令牌。"""
import math, html, datetime as dt
esc = lambda s: html.escape(str(s), quote=True)

def doy(date_iso):
    y, m, d = (int(x) for x in date_iso[:10].split('-'))
    return dt.date(y, m, d).timetuple().tm_yday

MONTHS = ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月', '7 月', '8 月', '9 月', '10 月', '11 月', '12 月']
MSTART = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

def ang(d): return (d - 1) / 365.0 * 2 * math.pi - math.pi / 2  # 1 月 1 日在顶，顺时针

def wheel_svg(items, size=520, labels=True, idattr='data-node', center=('2026', '年轮'), doors=True, cls='wheel', gid='wheel-g', anchors=None):
    """items: [{id, name, date (ISO), basis, lane}]。返回 SVG：环、月份刻度、两道门槛、节点（圆点）。
    节日标签不在这里画——二十一个节日有十七个挤在十月末到十一月的 40° 弧里，径向标签必然叠字；
    由 app.js 的 wheelLabels() 在两侧排成「扇出」的标签列，用引线连到环上的点，并按容器宽度选字号与行距。"""
    W = int(size * 1.2); cx = round(W * 0.54, 1); cy = size / 2; R0 = size * 0.325; out = []  # 环心略偏右：十七个节日的标签都在左边
    out.append(f'<svg class="{cls}" viewBox="0 0 {W} {size}" data-cx="{cx:.1f}" data-cy="{cy:.1f}" data-r0="{R0:.1f}" data-w="{W}" data-h="{size}" role="img" aria-label="年轮：各节日 2026 年落在一年里的位置">')
    out.append(f'<g id="{gid}">')
    if doors:
        # 两道门槛：夏末（7/25–9/20）与冬初（10/25–11/27）；随环一起转
        for a0, a1 in ((206, 263), (298, 331)):
            s_, e_ = ang(a0), ang(a1)
            out.append(f'<path class="door" d="M{cx + R0*.70*math.cos(s_):.1f} {cy + R0*.70*math.sin(s_):.1f} A{R0*.70:.1f} {R0*.70:.1f} 0 0 1 {cx + R0*.70*math.cos(e_):.1f} {cy + R0*.70*math.sin(e_):.1f} L{cx + R0*1.16*math.cos(e_):.1f} {cy + R0*1.16*math.sin(e_):.1f} A{R0*1.16:.1f} {R0*1.16:.1f} 0 0 0 {cx + R0*1.16*math.cos(s_):.1f} {cy + R0*1.16*math.sin(s_):.1f} Z"/>')
    out.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{R0:.1f}"/>')
    for i, ms in enumerate(MSTART):
        a = ang(ms); x1, y1 = cx + R0 * .94 * math.cos(a), cy + R0 * .94 * math.sin(a); x2, y2 = cx + R0 * 1.03 * math.cos(a), cy + R0 * 1.03 * math.sin(a)
        out.append(f'<line class="ml" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        am = ang(ms + 15); tx, ty = cx + R0 * .82 * math.cos(am), cy + R0 * .82 * math.sin(am)
        out.append(f'<text class="mt" x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" dominant-baseline="middle">{MONTHS[i]}</text>')
    for k, (short, _desc, ad) in enumerate(anchors or []):
        a = ang(ad); x1, y1 = cx + R0 * 0.94 * math.cos(a), cy + R0 * 0.94 * math.sin(a); x2, y2 = cx + R0 * 1.06 * math.cos(a), cy + R0 * 1.06 * math.sin(a)
        out.append(f'<line class="anc" data-k="{k}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    pts = sorted(items, key=lambda it: doy(it['date']))
    for it in pts:
        dy_ = doy(it['date']); a = ang(dy_); x, y = cx + R0 * math.cos(a), cy + R0 * math.sin(a)
        k = {'lunisolar-chinese': 'moon', 'lunisolar-hindu': 'moon', 'thai-lunar': 'moon', 'solar-term': 'sun'}.get(it.get('basis'), 'fixed')
        out.append(f'<g class="fx {k}" {idattr}="{esc(it["id"])}" data-lane="{esc(it.get("lane", ""))}" data-doy="{dy_}" data-name="{esc(it["name"])}" tabindex="0" role="button" aria-label="{esc(it["name"])}"><circle cx="{x:.1f}" cy="{y:.1f}" r="4.2"/></g>')
    out.append('</g>')
    out.append(f'<path class="topmark" d="M{cx:.1f} {cy - R0 * 1.12:.1f} l-6 -9 h12 Z"/>')
    out.append('<g class="leaders" aria-hidden="true"></g><g class="labels"></g>')
    out.append(f'<text class="cen" x="{cx}" y="{cy - 6}" text-anchor="middle">{esc(center[0])}</text><text class="cen2" x="{cx}" y="{cy + 14}" text-anchor="middle">{esc(center[1])}</text>')
    out.append('</svg>')
    return ''.join(out)

def XY(lat, lon): return (lon + 180) * 2.0, (90 - lat) * 2.0

def stage_map(cities, img_src):
    """序章舞台：NASA 夜光图 + 纬度夜带 + 城市灯。视窗（viewBox）由 app.js 的「镜头」按每一步点亮的城市推进；
    标签位置也由 app.js 按像素避让后再摆，这里只给首选方位（data-off）。"""
    OFF = {'dublin': 'l', 'lewes': 'b', 'utrecht': 'r', 'stockholm': 't', 'rome': 'b', 'beijing': 't', 'tokyo': 'r', 'delhi': 'l', 'kathmandu': 'r', 'sukhothai': 'l', 'mexico-city': 'b', 'la-paz': 'b', 'sydney': 'b', 'new-york': 't', 'phnom-penh': 'r'}
    bands = ''.join(f'<rect class="nb" data-lat="{90 - i*10}" x="0" y="{i*20}" width="720" height="20" opacity="0"/>' for i in range(18))
    dots = ''.join(f'<g class="cdot" data-city="{esc(c["id"])}" data-x="{XY(c["lat"], c["lon"])[0]:.1f}" data-y="{XY(c["lat"], c["lon"])[1]:.1f}" data-off="{OFF.get(c["id"], "t")}" transform="translate({XY(c["lat"], c["lon"])[0]:.1f} {XY(c["lat"], c["lon"])[1]:.1f})"><circle class="g" r="16" fill="url(#lampglow)"/><circle class="c" r="3.2"/><text x="0" y="-8">{esc(c["name_zh"])}</text></g>' for c in cities)
    return (f'<svg class="wmap" id="wmap" viewBox="0 0 720 360" preserveAspectRatio="xMidYMid meet" role="img" aria-label="世界地图：NASA 夜间灯光图，城市的灯按日期点亮">'
            f'<defs><linearGradient id="mapfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05050F" stop-opacity="0"/><stop offset="1" stop-color="#05050F"/></linearGradient><linearGradient id="mapfadeT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05050F"/><stop offset="1" stop-color="#05050F" stop-opacity="0"/></linearGradient><linearGradient id="mapfadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#05050F"/><stop offset="1" stop-color="#05050F" stop-opacity="0"/></linearGradient><linearGradient id="mapfadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#05050F" stop-opacity="0"/><stop offset="1" stop-color="#05050F"/></linearGradient><radialGradient id="lampglow"><stop offset="0" stop-color="#F2A33A" stop-opacity=".9"/><stop offset=".45" stop-color="#F2A33A" stop-opacity=".35"/><stop offset="1" stop-color="#F2A33A" stop-opacity="0"/></radialGradient></defs>'
            f'<rect x="-2160" y="-1080" width="5040" height="2520" fill="#05050F"/>'  # 地图以外铺成与海面同色、四边羽化，镜头露出图外时看不到切边
            f'<image href="{esc(img_src)}" x="0" y="0" width="720" height="360" preserveAspectRatio="none"/>'
            f'<rect x="-2" y="-2" width="724" height="26" fill="url(#mapfadeT)"/><rect x="-2" y="-2" width="26" height="364" fill="url(#mapfadeL)"/><rect x="696" y="-2" width="26" height="364" fill="url(#mapfadeR)"/>'
            f'<rect x="-720" y="318" width="2160" height="44" fill="url(#mapfade)"/><rect x="-720" y="360" width="2160" height="400" fill="#05050F"/>{bands}<line class="eq" x1="0" y1="180" x2="720" y2="180"/>{dots}</svg>')
