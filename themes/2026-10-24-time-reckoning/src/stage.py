# -*- coding: utf-8 -*-
"""序章「对历与对表」v2（2026-10-30）：全屏固定舞台——晨昏线世界地图 + 右侧十二城的日期牌与表盘 + 左下卡片 + 底部十四个年份的刻度尺（滚动与拖动是同一个量 t）。
每一级有一个参考瞬间（格林尼治平太阳正午所在的公历日期）；每座城的日期牌按它当时的民用历换算，表盘按它当时的时间制度（地方平时 / 区时 / 夏令时）显示此刻的钟。
公历 / 儒略历 / 伊斯兰算表历 / 希伯来历由本文件内的算法算（与 calendars.js 同公式）；中国与日本只写到年号与月份（editorial.CN_PLATE / JP_PLATE）。"""
import math, html, re, datetime as dt
import editorial as E, editorial2 as E2, figs
esc = lambda s: html.escape(str(s), quote=True)

def g2j(y, m, d):
    a = (14 - m) // 12; yy = y + 4800 - a; mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045
def j2jul(j):
    c = j + 32082; d = (4 * c + 3) // 1461; e = c - 1461 * d // 4; m = (5 * e + 2) // 153
    return d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1
def j2isl(j):
    EP = 1948440
    y = (30 * (j - EP) + 10646) // 10631
    def i2j(y, m, d): return d + math.ceil(29.5 * (m - 1)) + (y - 1) * 354 + (3 + 11 * y) // 30 + EP - 1
    m = min(12, math.ceil((j - (29 + i2j(y, 1, 1))) / 29.5) + 1); d = j - i2j(y, m, 1) + 1
    return y, m, d
ISL_M = ['穆哈兰姆', '色法尔', '赖比尔一', '赖比尔二', '主马达一', '主马达二', '赖哲卜', '舍尔邦', '赖买丹', '闪瓦鲁', '都尔喀尔德', '都尔黑哲']
COPTIC_EPOCH = 1825030  # 284-08-29 儒略
def j2coptic(j):
    y = (4 * (j - COPTIC_EPOCH) + 1463) // 1461
    m = (j - (COPTIC_EPOCH + 365 * (y - 1) + (y // 4))) // 30 + 1
    d = j - (COPTIC_EPOCH + 365 * (y - 1) + (y // 4) + 30 * (m - 1)) + 1
    return y, m, d

def fmt_g(y, m, d): return f'{y} 年 {m} 月 {d} 日'

def plate(city, step):
    """返回 (主行, 副行, 变化标记)。"""
    y, m, d = step['ref']; j = g2j(y, m, d); Y = step['year']
    cid = city['id']
    jy, jm, jd = j2jul(j); iy, im, idd = j2isl(j)
    isl = f'希吉拉 {iy} 年 {ISL_M[im-1]}月 {idd} 日'
    if cid in ('rome', 'mexico-city'):
        return (fmt_g(y, m, d), '格里历（1582 起）' if Y >= 1582 else '儒略历')
    if cid == 'paris':
        if Y == 1793: return ('共和二年 霜月 4 日', f'共和历（1793–1805）· 民间仍记格里历 {fmt_g(y, m, d)}')
        if Y == 1800: return ('共和八年 雪月 11 日', f'共和历 · 格里历 {fmt_g(y, m, d)}')
        if j < g2j(1582, 12, 20): return (fmt_g(jy, jm, jd), '儒略历 · 12 月 20 日起改用格里历')
        return (fmt_g(y, m, d), '格里历（1582-12-20 起）')
    if cid in ('london', 'new-york'):
        if Y < 1752: return (fmt_g(jy, jm, jd), f'儒略历 · 比罗马慢 {gap(j)} 天')
        return (fmt_g(y, m, d), '格里历（1752-09-14 起）')
    if cid == 'delhi':
        if Y < 1803: return (isl, '伊斯兰历（莫卧儿宫廷）· 维克拉姆纪元 ' + str(y + 57 if m >= 4 else y + 56) + ' 年')
        return (fmt_g(y, m, d), '格里历（东印度公司 / 英属印度，1752 起）· 伊斯兰历与印度教诸历并行')
    if cid == 'istanbul':
        if Y < 1917: return (isl, '伊斯兰历 · 财政用鲁米历（儒略历为基）' if Y >= 1789 else '伊斯兰历')
        if Y < 1926: return (f'鲁米历 {y - 584} 年 {m} 月 {d} 日', f'1917 年起鲁米历改用格里日期 · 伊斯兰历 {iy} 年')
        return (fmt_g(y, m, d), '格里历 · 基督纪元（1926-01-01 起，第 698 号法律）')
    if cid == 'cairo':
        cy, cm, cd = j2coptic(j)
        if Y < 1875: return (isl, f'伊斯兰历 · 科普特历殉道纪元 {cy} 年')
        return (fmt_g(y, m, d), f'格里历（行政，1875 起）· 伊斯兰历 {iy} 年')
    if cid == 'moscow':
        if Y < 1700:
            am = jy + 5509 if jm >= 9 else jy + 5508
            return (f'创世纪元 {am} 年 {jm} 月 {jd} 日', f'儒略历 · 拜占庭纪年（1700 年起改用基督纪元）')
        if Y < 1918: return (fmt_g(jy, jm, jd), f'儒略历 · 比格里历慢 {gap(j)} 天')
        return (fmt_g(y, m, d), '格里历（1918-02-14 起）· 教会历仍用儒略历')
    if cid in ('beijing', 'urumqi'):
        main, sub = E.CN_PLATE[Y], E.CN_PLATE_SUB[Y]
        if cid == 'urumqi' and Y < 1912: sub = sub + f' · 当地穆斯林社群用伊斯兰历 {iy} 年'
        return (main, sub)
    if cid == 'tokyo':
        return (E.JP_PLATE[Y], E.JP_PLATE_SUB[Y])
    return (fmt_g(y, m, d), '')

def gap(j):
    """该 JDN 时儒略历落后格里历的天数。"""
    jy, jm, jd = j2jul(j); return j - (g2j(jy, jm, jd))

# 各城时间制度：返回 (相对格林尼治的分钟偏移, 口径文字, 是否夏令时)
def clock(city, step):
    cid = city['id']; Y = step['year']; lon = city['lon']; lmt = lon * 4
    def L(): return (lmt, f'地方平时 · 东经 {lon}°' if lon >= 0 else f'地方平时 · 西经 {-lon}°', False)
    rules = {
        'rome': [(1893, 60, '中欧时间 +1')], 'london': [(1847, 0, '格林尼治平时（铁路，1880 法定）')], 'paris': [(1891, 9.35, '巴黎平时 +0:09:21'), (1911, 0, '格林尼治时间（法律称「巴黎平时减 9 分 21 秒」）'), (1940, 60, '中欧时间 +1')],
        'istanbul': [(1910, 120, '东欧时间 +2'), (1978, 180, '+3'), (2007, 120, '+2'), (2016, 180, '土耳其时间 +3')], 'cairo': [(1900, 120, '东欧时间 +2')],
        'moscow': [(1919, 180, '莫斯科时间 +3'), (1922, 120, '东欧时间 +2（1922-10 起）'), (1930, 180, '莫斯科时间 +3（1930 年「法令时」）'), (2011, 240, '+4（取消换时）'), (2014, 180, '莫斯科时间 +3')], 'delhi': [(1906, 330, '印度标准时间 +5:30')],
        'beijing': [(1902, 480, '海关海岸时 +8'), (1918, 480, '中原标准时 +8（1918 方案，1939 法定）'), (1949, 480, '北京时间 +8')], 'urumqi': [(1928, 360, '+6（tz 数据库：1928 起）'), (1949, 480, '北京时间 +8（官方）· 并行乌鲁木齐时间 +6')],
        'tokyo': [(1888, 540, '日本标准时 +9')], 'new-york': [(1883, -300, '东部标准时 −5')], 'mexico-city': [(1922, -420, '−7'), (1927, -360, '中部时间 −6')],
    }
    # 纽约 1883-11-18 是当地正午才改用东部标准时；这一步的参考瞬间是格林尼治正午（纽约早上 7 点），钟还走地方平时
    if cid == 'new-york' and Y == 1883: return (lmt, f'地方平时 · 西经 {-lon}°（当天当地正午起改东部标准时 −5）', False)
    best = None
    for yr, off, label in rules.get(cid, []):
        if Y >= yr: best = (off, label)
    if best is None: return L()
    off, label = best
    # 夏令时：2027-05-20 按现行规则（欧盟 / 英国 / 美国 / 埃及）；1972-06-30 与 1949-10-01 按 IANA tz 当年规则
    DST = {2027: ('rome', 'london', 'paris', 'new-york', 'cairo'), 1972: ('london', 'rome', 'new-york', 'cairo'), 1949: ('london', 'istanbul')}
    if cid in DST.get(Y, ()): return (off + 60, label + ' · 夏令时 +1', True)
    return (off, label, False)

def dial_svg(minutes, size=40):
    """表盘：此刻当地钟表指向（12 小时制）。minutes 为相对格林尼治正午的分钟偏移 → 当地时间 = 12:00 + offset。
    指针画成朝上的线，用 rotate 转到位（app.js 用弹簧转同一个角度）。"""
    t = (720 + minutes) % 1440; ha = (t / 60 % 12) * 30; ma = (t % 60) * 6
    ticks = ''.join(f'<line class="tk" x1="{50+42*math.sin(math.radians(k*30)):.1f}" y1="{50-42*math.cos(math.radians(k*30)):.1f}" x2="{50+47*math.sin(math.radians(k*30)):.1f}" y2="{50-47*math.cos(math.radians(k*30)):.1f}"/>' for k in range(12))
    night = ' night' if (t < 360 or t >= 1080) else ''
    return (f'<svg class="dial{night}" viewBox="0 0 100 100" width="{size}" height="{size}" aria-hidden="true"><circle class="face" cx="50" cy="50" r="47"/>{ticks}'
            f'<line class="hh" x1="50" y1="50" x2="50" y2="25" transform="rotate({ha:.2f} 50 50)"/><line class="mh" x1="50" y1="50" x2="50" y2="13" transform="rotate({ma:.2f} 50 50)"/><circle class="pin" cx="50" cy="50" r="3.5"/></svg>')

def hhmm(minutes):
    t = (720 + minutes) % 1440; h = int(t // 60); m = int(round(t % 60))
    if m == 60: h, m = (h + 1) % 24, 0
    return f'{h:02d}:{m:02d}'

def sun_at(y, m, d):
    """格林尼治 12:00 UT 时的太阳赤纬（度）与直射点经度（度，东正）：NOAA 简化式，与 app.js 同。"""
    doy = dt.date(y, m, d).timetuple().tm_yday
    g = 2 * math.pi / 365 * (doy - 1)
    decl = 0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    return math.degrees(decl), -eqt / 4

def _cap(im):
    """（说明, 署名）：说明可以截短，署名（作者 + 许可）永远完整显示。"""
    s = im['subject']
    return (s[:80] + '…' if len(s) > 80 else s), f'图：{im["author_short"]}，{im["license_short"]}。'

def order(cities):
    return sorted(cities, key=lambda c: c['lon'])

def stage(cities, IM, img_src):
    S = data(cities, IM)
    s0 = S['steps'][0]
    rows = []
    for c in order(cities):
        c0 = s0['cities'][c['id']]
        rows.append(f'<div class="tpr{" chg" if c0["changed"] else ""}" data-city="{esc(c["id"])}" title="{esc(c0["label"])}">{dial_svg(c0["off"])}'
                    f'<span class="tpn"><b>{esc(c["name"])}</b><span>{esc(c0["time"])}</span></span><span class="tpp"><b>{esc(c0["plate"])}</b><span>{esc(c0["sub"])}</span></span></div>')
    plates = (f'<div class="tlbandw" id="tlbandw"><button type="button" class="tlbtn glass" id="tlbtn" aria-expanded="true" aria-controls="tlplates">十二城 · 日期牌与表盘<span class="tlbtn-c" aria-hidden="true"></span></button>'
              f'<aside class="tlplates glass" id="tlplates" aria-label="十二座城在这一刻的日期牌与钟表">'
              f'<div class="tph" aria-hidden="true"><span>表盘</span><span>城 · 钟</span><span>日期牌（西 → 东）</span></div>{"".join(rows)}'
              f'<p class="tpf">表盘 = 格林尼治平太阳正午这一刻当地的钟；黄铜 = 这一步有变化的城。</p></aside></div>')
    n = len(S['steps'])
    marks = ''.join(f'<button type="button" class="rmark{" edge" if k in (0, n - 1) else ""}" data-step="{k}" style="left:{k / (n - 1) * 100:.3f}%" aria-label="跳到 {s["year"]} 年：{esc(s["title"])}"><i></i><span>{s["year"]}</span></button>' for k, s in enumerate(S['steps']))
    chip0 = f'<a class="chip" href="#n-{esc(s0["chip"][0])}" data-open="{esc(s0["chip"][0])}">{esc(s0["chip"][1])}</a>' if s0.get('chip') else ''
    ph0 = (f'<figure class="tlph{"" if s0["img"] else " none"}"><img id="tlimg" src="{esc(s0["img"])}" alt="{esc(s0["alt"])}"><figcaption id="tlcap"><span class="cs">{esc(s0["cap"])}</span><span class="cr">{esc(s0["cred"])}</span></figcaption></figure>')
    card = (f'<aside class="tlcard glass" id="tlcard" aria-live="polite">'
            f'<div class="tlhd"><span class="tlno" id="tlno">01 / {n:02d}</span><span id="tlkick">{esc(s0["year"])} · {esc(s0["refTxt"])}</span></div>'
            f'<p class="tlbig"><b id="tlbig">{esc(s0["big"])}</b><small id="tlbigu">{esc(s0["unit"])}</small></p><p class="tlbasis" id="tlbasis">{esc(s0["basis"])}</p>'
            f'<p class="tltext" id="tltext">{esc(s0["text"])}</p><div class="tlchips" id="tlchips">{chip0}</div>{ph0}'
            f'<p class="tlcredit">底图：NASA「蓝色弹珠」2004 年合成图，公有领域 · 晨昏线按这一刻的太阳位置现算</p></aside>')
    hud = (f'<div class="tlhud glass" id="jhud"><span class="tlch">00 · 序章 · 对历与对表 · 拖动底部刻度尺，或往下滚</span><span class="jk" id="jk">{esc(s0["kicker"])}</span>'
           f'<div class="jyear" id="jyear">{s0["year"]}<small>{esc(s0["refTxt"])} · 格林尼治正午</small></div><div class="jt" id="jt">{esc(s0["title"])}</div></div>')
    ruler = (f'<div class="tlruler glass" id="tlruler" role="slider" tabindex="0" aria-label="十四个年份：拖动、甩动或用方向键" aria-valuemin="0" aria-valuemax="{n - 1}" aria-valuenow="0" aria-valuetext="{s0["year"]} 年">'
             f'<div class="rtrack" id="rtrack"><span class="rline"></span>{marks}<span class="rhead" id="rhead"><i></i></span></div></div>')
    steps_sr = ''.join(f'<li><b>{s["year"]} · {esc(s["title"])}</b> {esc(s["text"])}</li>' for s in S['steps'])
    return (f'<div class="tlpin" id="tlpin"><div class="tlstage" id="tlstage"><div class="tlmap" id="jscene">{figs.stage_map(cities, img_src, s0)}</div>'
            f'{hud}{card}{plates}{ruler}</div></div><ol class="sr-only" id="tlsr">{steps_sr}</ol>')

def data(cities, IM):
    """给 app.js：每一步的文字、照片、太阳位置，以及每座城的日期牌、表盘偏移、是否变化。"""
    steps, prev = [], {}
    for s in E.STEPS:
        y, m, d = s['ref']; decl, sslon = sun_at(y, m, d)
        im = IM.get(s.get('photo')) if s.get('photo') else None
        ch = E2.STEP_CHIP.get(str(s['year']))
        row = {'id': s['id'], 'year': s['year'], 'refTxt': f'{m} 月 {d} 日', 'kicker': s['kicker'], 'title': s['title'], 'big': s['big'], 'unit': s['unit'], 'basis': s['basis'],
               'text': E2.STEP_TEXT[str(s['year'])], 'gmt': s['year'] >= 1884, 'decl': round(decl, 3), 'sslon': round(sslon, 3), 'hl': s.get('hl', []),
               'img': ('assets/' + im['file']) if im else '', 'alt': im['subject'] if im else '', 'cap': _cap(im)[0] if im else '', 'cred': _cap(im)[1] if im else '',
               'chip': list(ch) if ch else None, 'cities': {}}
        for c in cities:
            main, sub = plate(c, s); off, label, dst = clock(c, s)
            changed = (prev.get(c['id']) is not None and prev[c['id']] != label) or c['id'] in s.get('hl', [])
            prev[c['id']] = label
            row['cities'][c['id']] = {'plate': main, 'sub': sub, 'off': round(off, 2), 'time': hhmm(off), 'label': label, 'changed': changed}
        steps.append(row)
    return {'steps': steps, 'order': [c['id'] for c in order(cities)], 'cities': {c['id']: {'name': c['name'], 'lat': c['lat'], 'lon': c['lon']} for c in cities}}
