# -*- coding: utf-8 -*-
"""序章「对历与对表」：固定舞台（世界地图 + 十二座城市的日期牌与表盘）+ 十四级滚动卡片。
每一级有一个参考瞬间（格林尼治平太阳正午所在的公历日期）；每座城的日期牌按它当时的民用历换算，表盘按它当时的时间制度（地方平时 / 区时 / 夏令时）显示此刻的钟。
公历 / 儒略历 / 伊斯兰算表历 / 希伯来历由本文件内的算法算（与 calendars.js 同公式）；中国与日本只写到年号与月份（editorial.CN_PLATE / JP_PLATE）。"""
import math, html, re
import editorial as E
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
        if Y < 1917: return (isl, '伊斯兰历 · 财政用鲁米历（儒略历为基）' if Y >= 1840 else '伊斯兰历')
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
        'moscow': [(1919, 180, '莫斯科时间 +3'), (2011, 240, '+4（取消换时）'), (2014, 180, '莫斯科时间 +3')], 'delhi': [(1906, 330, '印度标准时间 +5:30')],
        'beijing': [(1902, 480, '海关海岸时 +8'), (1918, 480, '中原标准时 +8'), (1949, 480, '北京时间 +8')], 'urumqi': [(1918, 360, '新藏时区 +6'), (1949, 480, '北京时间 +8（官方）· 并行乌鲁木齐时间 +6')],
        'tokyo': [(1888, 540, '日本标准时 +9')], 'new-york': [(1883, -300, '东部标准时 −5')], 'mexico-city': [(1922, -420, '−7'), (1927, -360, '中部时间 −6')],
    }
    best = None
    for yr, off, label in rules.get(cid, []):
        if Y >= yr: best = (off, label)
    if best is None: return L()
    off, label = best
    # 2027-05-20 的夏令时：欧盟 / 英国 / 美国
    if Y == 2027 and cid in ('rome', 'london', 'paris', 'new-york'): return (off + 60, label + ' · 夏令时 +1', True)
    return (off, label, False)

def dial_svg(minutes, size=64):
    """表盘：此刻当地钟表指向（12 小时制）。minutes 为相对格林尼治正午的分钟偏移 → 当地时间 = 12:00 + offset。"""
    t = (720 + minutes) % 1440; h = t / 60; mn = t % 60
    ha = (h % 12) * 30; ma = mn * 6
    def hand(a, r, cls):
        x = 50 + r * math.sin(math.radians(a)); y = 50 - r * math.cos(math.radians(a))
        return f'<line class="{cls}" x1="50" y1="50" x2="{x:.1f}" y2="{y:.1f}"/>'
    ticks = ''.join(f'<line class="tk" x1="{50+44*math.sin(math.radians(k*30)):.1f}" y1="{50-44*math.cos(math.radians(k*30)):.1f}" x2="{50+48*math.sin(math.radians(k*30)):.1f}" y2="{50-48*math.cos(math.radians(k*30)):.1f}"/>' for k in range(12))
    night = ' night' if (t < 360 or t >= 1080) else ''
    return f'<svg class="dial{night}" viewBox="0 0 100 100" width="{size}" height="{size}" aria-hidden="true"><circle class="face" cx="50" cy="50" r="48"/>{ticks}{hand(ha, 26, "hh")}{hand(ma, 38, "mh")}<circle class="pin" cx="50" cy="50" r="2.5"/></svg>'

def hhmm(minutes):
    t = (720 + minutes) % 1440; h = int(t // 60); m = int(round(t % 60))
    if m == 60: h, m = (h + 1) % 24, 0
    return f'{h:02d}:{m:02d}'

def XY(lat, lon): return (lon + 180) * 2.0, (90 - lat) * 2.0

def stage(cities, world, IM, caption_of):
    # 地图
    OFF = {'rome': (-2, 14), 'london': (-14, -7), 'paris': (-12, 15), 'istanbul': (26, -4), 'cairo': (18, 14), 'moscow': (0, -8), 'delhi': (14, 13), 'beijing': (0, -8), 'urumqi': (-4, -8), 'tokyo': (12, 12), 'new-york': (0, -8), 'mexico-city': (0, 15)}
    dots = ''.join(f'<g class="cdot" data-city="{esc(c["id"])}" transform="translate({XY(c["lat"], c["lon"])[0]:.1f} {XY(c["lat"], c["lon"])[1]:.1f})"><circle r="4"/><text x="{OFF.get(c["id"], (0, -8))[0]}" y="{OFF.get(c["id"], (0, -8))[1]}">{esc(c["name"])}</text></g>' for c in cities)
    svg = (f'<svg class="wmap" viewBox="0 28 720 270" preserveAspectRatio="xMidYMid slice"><path class="land" d="{world["d"]}"/>'
           f'<line class="gmt" id="gmt-line" x1="360" y1="0" x2="360" y2="360"/>{dots}</svg>')
    tiles = ''.join(f'<div class="ctile" data-city="{esc(c["id"])}"><div class="cn">{esc(c["name"])}<small></small></div><div class="dl"></div><div class="pl"><b></b><span></span></div></div>' for c in cities)
    return (f'<div class="jwrap"><div class="jstage" id="jstage"><div class="jscene">{svg}<div class="jhud"><span class="jk" id="jk"></span><b class="jt" id="jt"></b><span class="jc" id="jidx"></span></div>'
            f'<div class="jladder">' + ''.join(f'<button type="button" class="lad" data-lvl="{i}" aria-label="第 {i+1} 级 {esc(s["year"])}"><i></i></button>' for i, s in enumerate(E.STEPS)) + '</div></div>'
            f'<div class="ctiles" id="ctiles">{tiles}</div><p class="jlegend">表盘 = 格林尼治平太阳正午这一刻各城钟表的指向；日期牌 = 同一天在各城民用历里的写法。黄铜 = 本级有变化的城市。</p></div>')

def steps(IM, caption_of, src_lookup):
    out = []
    for i, s in enumerate(E.STEPS):
        ph = ''
        if s.get('photo') and s['photo'] in IM:
            im = IM[s['photo']]
            ph = f'<figure class="jph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{esc(caption_of(s["photo"], im))} 图：{esc(im["author"])}，{esc(im["license_short"])}。</figcaption></figure>'
        srcs, conf = src_lookup(s['src'])
        out.append(f'''<article class="jstep" id="lvl-{esc(s['id'])}" data-lvl="{i}"><div class="jcard">
<div class="jcard-hd"><span class="jno">{i+1:02d} / {len(E.STEPS):02d}</span><span>{esc(s['kicker'])}</span><span>{esc(s['year'])}</span></div>
<h3>{esc(s['title'])}</h3>
<p class="jbig"><b>{esc(s['big'])}</b><small>{esc(s['unit'])}</small></p>
<p class="jbasis">{esc(s['basis'])}</p>
<p class="jtag">{esc(s['text'])}</p>
{ph}{srcs}<p class="jwho">置信度 {conf}</p></div></article>''')
    return f'<div class="jsteps">{"".join(out)}</div></div>'

def data(cities):
    """给 app.js：每级每城的日期牌、表盘偏移、是否变化。"""
    levels = []
    prev = {}
    for s in E.STEPS:
        row = {'id': s['id'], 'year': s['year'], 'kicker': s['kicker'], 'title': s['title'], 'gmt': s['year'] >= 1884, 'cities': {}}
        for c in cities:
            main, sub = plate(c, s); off, label, dst = clock(c, s)
            key = (re.sub(r'（[^）]*）|\s', '', sub.split('·')[0]), label)
            changed = (prev.get(c['id']) is not None and prev[c['id']] != key) or c['id'] in s.get('hl', [])
            prev[c['id']] = key
            row['cities'][c['id']] = {'plate': main, 'sub': sub, 'off': round(off, 1), 'time': hhmm(off), 'label': label, 'changed': changed, 'dial': dial_svg(off)}
        levels.append(row)
    return levels
