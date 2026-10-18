# -*- coding: utf-8 -*-
"""序章「速度之旅」：固定舞台（真实照片 + 速度线 + 对数仪表 + 读数）+ 十九级滚动卡片。数字与出处取自研究底稿，口径与全页一致。照片全部公有领域或 CC，见 images.json。"""
import math, html

def esc(s): return html.escape(str(s), quote=True)

# 每一级：id、名字、kicker（英文小标）、kmh、年份、谁、类别、剪影、照片 id、一句宣传腔但有口径的 tagline、三行规格、口径说明、数据来源（key: scale:<id> / cell:<track-era> / cell:<track-era>:also / const）
LEVELS = [
    dict(id='walk', name='步行', kicker='HUMAN · WALKING', kmh=5, year='—', who='所有人', cls='人体', photo='walk',
         tag='一切速度的基准。本页所有「几倍」都从这里算起。', specs=[('速度', '约 5 km/h'), ('口径', '成人常速'), ('横穿中国东西', '约 43 天不停')], src='scale:walk'),
    dict(id='bolt', name='博尔特', kicker='HUMAN · SPRINT', kmh=44.72, year='2009', who='Usain Bolt · 柏林', cls='人体', photo='bolt',
         tag='9.58 秒。人类自己能跑出的最高速度；比它快的，都得靠动物或机器。', specs=[('峰值速度', '44.72 km/h'), ('100 m', '9.58 s'), ('口径', '60–80 m 分段，柏林大会生物力学报告')], src='scale:bolt'),
    dict(id='rocket', name='火箭号', kicker='RAIL · 1829', kmh=48, year='1829', who='斯蒂芬森父子 · 雨山', cls='铁路', photo='rocket',
         tag='第一次有机器跑得比驿站马车快一倍以上，而且不喘气。铁路公司从此按「跑得快而且不坏」采购。', specs=[('冲刺', '约 30 mph · 48 km/h'), ('试车平均', '12 mph'), ('奖金', '500 英镑')], src='cell:rail-1'),
    dict(id='horse', name='赛马', kicker='ANIMAL · 2008', kmh=70.76, year='2008', who='Winning Brew · 宾州', cls='动物', photo='horse',
         tag='前工业时代的速度上限。驿传、骑兵、邮车，全世界的「快」都由它定义了几千年。', specs=[('极速', '70.76 km/h'), ('口径', '吉尼斯，1/4 英里'), ('纪录保持', '2008 年至今')], src='scale:horse'),
    dict(id='jamais', name='La Jamais Contente', kicker='ROAD · 1899 · ELECTRIC', kmh=105.88, year='1899', who='Camille Jenatzy · Achères', cls='陆上轮式', photo='jamais',
         tag='第一辆破百的车是电动车。两台电机、一副鱼雷车身，比内燃机早了十年。', specs=[('速度', '105.88 km/h'), ('口径', '单向一公里'), ('动力', '两台电机共 50 kW')], src='cell:road-2:also'),
    dict(id='blitzen', name='Blitzen Benz', kicker='ROAD · 1909 · 200 KM/H', kmh=202.65, year='1909', who='Victor Hémery · 布鲁克兰兹', cls='陆上轮式', photo='lsr',
         tag='第一辆跑过 200 km/h 的内燃机汽车，比当时任何飞机都快——电动列车在 1903 年已先到过这里。', specs=[('速度', '202.65 km/h'), ('口径', '飞行一公里，单向'), ('同级', '1903 Zossen 电动试验车 210.2')], src='cell:road-2'),
    dict(id='cr', name='复兴号', kicker='RAIL · EVERYDAY · 350', kmh=350, year='2017', who='京沪高铁 · 国铁集团', cls='铁路', photo='shinkansen0',
         tag='普通人今天能买票坐到的陆上最快。纪录还在往上，日常停在这里快十年了。', specs=[('商业运营', '350 km/h'), ('口径', '轮轨最高商业速度'), ('网络', '截至 2025 年底约 5.04 万公里')], src='scale:hsr'),
    dict(id='spirit', name='Spirit of Australia', kicker='WATER · 1978 · UNBROKEN', kmh=511.11, year='1978', who='Ken Warby · Blowering Dam', cls='水上', photo='spiritoz',
         tag='水上速度纪录，四十八年无人能破。1930 年以来十三位挑战者七人身亡——这是一面真正的物理墙。', specs=[('速度', '511.11 km/h · 317.6 mph'), ('口径', 'UIM 认证，双向平均'), ('动力', '喷气，自家后院造')], src='cell:water-5'),
    dict(id='tgv', name='TGV V150', kicker='RAIL · 2007 · WHEEL ON RAIL', kmh=574.8, year='2007', who='SNCF / Alstom · 东线', cls='铁路', photo='tgv',
         tag='轮子贴着钢轨能跑多快？574.8 km/h。接触网电压推到 31 kV、张力 40 kN，车轮加大到 1,092 mm。', specs=[('速度', '574.8 km/h'), ('口径', '轮轨试验纪录，2007-04-03'), ('功率', '19.6 MW')], src='cell:rail-6'),
    dict(id='l0', name='L0 系磁浮', kicker='RAIL · 2015 · MAGLEV', kmh=603, year='2015', who='JR 东海 · 山梨试验线', cls='铁路', photo='maglev_l0',
         tag='不碰钢轨，就没有黏着极限。603 km/h，有人乘坐的地面交通纪录。', specs=[('速度', '603 km/h'), ('口径', '吉尼斯，载人'), ('商业目标', '中央新干线 500 km/h')], src='cell:rail-7'),
    dict(id='airliner', name='喷气客机', kicker='AIR · EVERYDAY · MACH 0.85', kmh=900, year='1958–', who='所有航空公司', cls='空中', photo='airliner',
         tag='1958 年以来，普通人能坐到的最快速度就停在这里——中间只有协和的二十七年例外。', specs=[('巡航', '约 900 km/h'), ('口径', 'Mach 0.78–0.85'), ('北京到上海', '约 1.5 小时')], src='scale:airliner'),
    dict(id='x1', name='Bell X-1', kicker='AIR · 1947 · MACH 1.06', kmh=1127, year='1947', who='Chuck Yeager · 穆罗克干湖', cls='空中', photo='x1',
         tag='10 月 14 日，人类第一次飞过音速。火箭推力硬推过激波，可调安定面保住操纵。', specs=[('速度', 'Mach 1.06 · 约 1,127 km/h'), ('高度', '约 43,000 ft'), ('口径', 'NASA SP-4219')], src='cell:air-4'),
    dict(id='ssc', name='Thrust SSC', kicker='ROAD · 1997 · SUPERSONIC', kmh=1227.985, year='1997', who='Andy Green · 黑岩沙漠', cls='陆上轮式', photo='thrustssc',
         tag='10 月 15 日，陆地上唯一的超音速纪录。两台喷气发动机，两程都突破音障，与 X-1 相隔五十年零一天。', specs=[('速度', '1,227.985 km/h · 763.035 mph'), ('口径', 'FIA 双向平均飞行一英里'), ('马赫', '1.016（吉尼斯作 1.020）')], src='cell:road-6'),
    dict(id='concorde', name='协和', kicker='AIR · 1976–2003 · MACH 2', kmh=2180, year='1976', who='英航 / 法航', cls='空中', photo='concorde',
         tag='乘客能买票坐到的最快速度，二十七年。2003 年 10 月 24 日之后，日常速度退回了 Mach 0.85。', specs=[('巡航', 'Mach 2.04 · 约 2,180 km/h'), ('口径', 'BA 口径 1,350 mph'), ('商业首航', '1976-01-21，今年整 50 年')], src='scale:concorde'),
    dict(id='sr71', name='SR-71', kicker='AIR · 1976 · AIR-BREATHING', kmh=3529.56, year='1976', who='美国空军 · Joersz / Morgan', cls='空中', photo='sr71',
         tag='吸气式飞机的绝对纪录，五十年未破。机身几乎全钛，巡航时蒙皮超过 300 °C。', specs=[('速度', '3,529.56 km/h'), ('口径', 'FAI 直线航线纪录，1976-07-28'), ('材料', '钛合金，热浸 >600 °F')], src='scale:sr71'),
    dict(id='x15', name='X-15', kicker='AIR · 1967 · MACH 6.7', kmh=7274, year='1967', who='Pete Knight · NASA / USAF', cls='空中', photo='x15',
         tag='有翼载人飞行器的顶点。Inconel X 镍铬合金作热沉，机头驻点 1,900 °F。', specs=[('速度', '7,274 km/h · Mach 6.7'), ('口径', 'NASA，1967-10-03'), ('纪录保持', '59 年')], src='scale:x15'),
    dict(id='apollo', name='Apollo 10', kicker='SPACE · 1969 · FASTEST HUMANS', kmh=39897, year='1969', who='Stafford / Young / Cernan', cls='太空', photo='apollo_cm',
         tag='人类乘坐过的最快速度。1969 年 5 月 26 日从月球返回、溅落南太平洋，此后五十七年无人更快——今年的 Artemis II 也没有。', specs=[('速度', '39,897 km/h · 24,791 mph'), ('口径', 'NASA；吉尼斯作 39,937.7'), ('Artemis II', '约 39,693 km/h，未改写')], src='scale:apollo10'),
    dict(id='parker', name='帕克太阳探测器', kicker='SPACE · 2024 · FASTEST OBJECT', kmh=692000, year='2024', who='NASA · 无人', cls='太空', photo='psp',
         tag='最快的人造物，无人。掠过近日点时相对太阳 692,000 km/h，是 Apollo 10 的十七倍。', specs=[('速度', '约 692,000 km/h · 430,000 mph'), ('口径', '相对太阳，2024-12-24 近日点'), ('光速的', '0.064%')], src='scale:parker'),
    dict(id='light', name='光速', kicker='PHYSICS · c', kmh=1079252848.8, year='—', who='宇宙', cls='物理', photo=None,
         tag='终点。再往上没有了——帕克探测器只走到这把尺子的 0.064%，人类自己只走到 0.0037%。', specs=[('速度', '299,792,458 m/s'), ('口径', 'SI 定义值'), ('北京到上海', '0.0044 秒')], src='scale:light'),
]

LO, HI = 0.0, 9.3  # log10 km/h，与卷首速度尺一致

def fmt(v):
    if v >= 1e8: return f'{v/1e8:.4g} 亿'
    if v >= 100: return f'{v:,.0f}'
    if v >= 10: return f'{v:.1f}'.rstrip('0').rstrip('.')
    return f'{v:.2f}'.rstrip('0').rstrip('.')

SUP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}

def gauge_svg():
    """对数仪表：270° 弧，10⁰–10⁹，红线区 = Apollo 10 以上（没有人乘坐过）。"""
    cx, cy, r = 200, 200, 160
    a0, a1 = 135, 405  # 起止角（度，顺时针，0 = 右）
    def pt(frac, rr):
        a = math.radians(a0 + frac * (a1 - a0))
        return cx + rr * math.cos(a), cy + rr * math.sin(a)
    def arc(f0, f1, rr):
        x0, y0 = pt(f0, rr); x1, y1 = pt(f1, rr)
        large = 1 if (f1 - f0) * (a1 - a0) > 180 else 0
        return f'M{x0:.1f},{y0:.1f} A{rr},{rr} 0 {large} 1 {x1:.1f},{y1:.1f}'
    out = ['<svg class="gdial" viewBox="-40 -14 480 430" aria-hidden="true">']
    out.append(f'<path class="g-track" d="{arc(0, 1, r)}"/>')
    fa = (math.log10(39897) - LO) / (HI - LO)
    out.append(f'<path class="g-red" d="{arc(fa, 1, r)}"/>')
    out.append(f'<path class="g-fill" id="g-fill" d="{arc(0, 1, r)}"/>')
    for d in range(0, 10):
        f = (d - LO) / (HI - LO)
        x0, y0 = pt(f, r - 14); x1, y1 = pt(f, r + 10)
        out.append(f'<line class="g-tick" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
        tx, ty = pt(f, r - 34)
        out.append(f'<text class="g-lab" x="{tx:.1f}" y="{ty + 5:.1f}" text-anchor="middle">10{SUP[str(d)]}</text>')
        for k in range(2, 10):
            v = 10 ** d * k
            if math.log10(v) > HI: break
            ff = (math.log10(v) - LO) / (HI - LO)
            x0, y0 = pt(ff, r - 6); x1, y1 = pt(ff, r + 6)
            out.append(f'<line class="g-tick2" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    # 关键刻度小标
    for v, lab in ((350, '高铁'), (1225, '音速'), (39897, 'Apollo 10')):
        ff = (math.log10(v) - LO) / (HI - LO)
        x0, y0 = pt(ff, r + 12); x1, y1 = pt(ff, r + 26)
        out.append(f'<line class="g-mark" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
        tx, ty = pt(ff, r + 44)
        anchor = 'middle' if abs(tx - cx) < 40 else ('end' if tx < cx else 'start')
        out.append(f'<text class="g-mk" x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}">{lab}</text>')
    out.append(f'<text class="g-unit" x="{cx}" y="{cy + 118}" text-anchor="middle">km/h · 对数刻度</text>')
    out.append(f'<text class="g-redlab" x="{cx}" y="{cy + 136}" text-anchor="middle">红区：没有人乘坐过</text>')
    out.append(f'<g id="g-needle" class="g-needle" style="transform-origin:{cx}px {cy}px"><path d="M{cx},{cy - r + 18} L{cx - 7},{cy + 10} L{cx + 7},{cy + 10} Z"/><circle cx="{cx}" cy="{cy}" r="14"/></g>')
    out.append('</svg>')
    return '\n'.join(out)

def speed_lines():
    ls = []
    for i, (y, w, o) in enumerate(((40, 220, .5), (70, 320, .35), (100, 180, .6), (130, 360, .3), (160, 260, .45), (190, 140, .35), (215, 300, .25))):
        ls.append(f'<line class="spd" x1="{600 - w}" y1="{y}" x2="600" y2="{y}" style="--i:{i}"/>')
    return f'<svg class="spdlines" viewBox="0 0 600 240" preserveAspectRatio="none" aria-hidden="true">{"".join(ls)}</svg>'

def stage(IM, caption_of):
    def veh(i, l):
        im = IM.get(l['photo']) if l.get('photo') else None
        if not im: return f'<div class="veh veh-c" data-lvl="{i}"><div class="cglyph"><b>c</b><span>299,792,458 m/s</span></div></div>'
        return f'<div class="veh" data-lvl="{i}"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy" decoding="async"></div>'
    sils = ''.join(veh(i, l) for i, l in enumerate(LEVELS))
    ladder = ''.join(f'<button type="button" class="lad" data-lvl="{i}" title="{esc(l["name"])} · {fmt(l["kmh"])} km/h"><i></i></button>' for i, l in enumerate(LEVELS))
    return f'''
<div class="jwrap"><div class="jstage" id="jstage">
  <div class="jscene">
    <div class="jveh-wrap">{speed_lines()}{sils}</div>
    <div class="jhud"><div class="jk" id="jk">HUMAN · WALKING</div><div class="jt" id="jt">步行</div><div class="jc"><span id="jidx">01</span> / {len(LEVELS):02d}</div></div>
    <div class="jladder" id="jladder">{ladder}</div>
  </div>
  <div class="jdial">
    {gauge_svg()}
    <div class="jread"><div class="jnum"><b id="jnum">5</b><span>km/h</span></div><div class="jalt" id="jalt">3.1 mph · Mach 0.004</div></div>
  </div>
</div>'''

def steps(IM, caption_of, src_lookup):
    out = []
    for i, l in enumerate(LEVELS):
        im = IM.get(l['photo']) if l.get('photo') else None
        ph = (f'<p class="jcap">图：{esc(caption_of(l["photo"], im))} {esc(im["author"])}，{esc(im["license"])}。</p>') if im else ''
        specs = ''.join(f'<div><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in l['specs'])
        srcs, conf = src_lookup(l['src'])
        out.append(f'''<article class="jstep" data-lvl="{i}" id="lvl-{esc(l['id'])}">
<div class="jcard">
  <div class="jcard-hd"><span class="jno">{i+1:02d}</span><span class="jcls">{esc(l['cls'])}</span><span class="jyr">{esc(l['year'])}</span></div>
  <h3>{esc(l['name'])}</h3>
  <p class="jbig"><b>{fmt(l['kmh'])}</b><small>km/h</small></p>
  <p class="jtag">{esc(l['tag'])}</p>
  <div class="jspecs">{specs}</div>
  <p class="jwho">{esc(l['who'])} {conf}</p>
  {srcs}{ph}
</div></article>''')
    return '<div class="jsteps" id="jsteps">' + ''.join(out) + '</div></div>'

def data():
    return [{'id': l['id'], 'name': l['name'], 'kicker': l['kicker'], 'kmh': l['kmh'], 'f': (math.log10(l['kmh']) - LO) / (HI - LO)} for l in LEVELS]
