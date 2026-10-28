#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7 题「冬天的门槛」：用 PyEphem 预算 1900–2100 的三张日期表，写到 ../tables.json。
  1) terms：立冬（太阳黄经 225°）、小雪（240°）、冬至（270°）的北京时间日期与时刻；
  2) diwali：排灯节（amanta 历阿湿缚庾阇月末的朔日 amavasya，以德里日落时 tithi 为准；Lahiri 岁差）；
  3) fullmoons：10–12 月的望（UTC），给水灯节「天文望日」参考；水灯节正日用泰国官方表（research/fest_C.json dates_table）校准。
用法：pip install ephem；python3 tools/tables.py   （在 src/ 目录下运行）
对拍：排灯节 2015–2027 对印度中央政府假日备忘录（fest_C.json dates_table），全部要对上，差一天的在页面上列出。"""
import json, math, os, sys, datetime as dt
import ephem

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'tables.json')
BJ = dt.timedelta(hours=8); IST = dt.timedelta(hours=5, minutes=30)

def to_dt(e): return ephem.Date(e).datetime()

# ---------- 节气：太阳视黄经到达 λ 的时刻（UTC）
def sun_lon(d):
    e = ephem.Date(d); s = ephem.Sun(); s.compute(e)
    return math.degrees(ephem.Ecliptic(ephem.Equatorial(s.g_ra, s.g_dec, epoch=e)).lon) % 360  # 视黄经（含章动、光行差）
def solar_term(year, lam, guess_md):
    t = ephem.Date(dt.datetime(year, guess_md[0], guess_md[1]))
    for _ in range(60):
        l = sun_lon(t); diff = (lam - l + 540) % 360 - 180
        if abs(diff) < 1e-6: break
        t = ephem.Date(t + diff / 360.0 * 365.2422)
    return to_dt(t)

# ---------- 排灯节
def ayanamsa(d):  # Lahiri 近似：2000-01-01 23.857°，每年 +50.29"
    y = d.year + (d.timetuple().tm_yday - 1) / 365.25
    return 23.857 + (y - 2000) * 50.29 / 3600
def sun_sid(d): return (sun_lon(ephem.Date(d)) - ayanamsa(d)) % 360
def elong(d):
    s = ephem.Sun(); m = ephem.Moon(); e = ephem.Date(d); s.compute(e); m.compute(e)
    ls = math.degrees(ephem.Ecliptic(ephem.Equatorial(s.g_ra, s.g_dec, epoch=e)).lon); lm = math.degrees(ephem.Ecliptic(ephem.Equatorial(m.g_ra, m.g_dec, epoch=e)).lon)
    return (lm - ls) % 360
def sunset_delhi(day):  # day: date (IST 民用日) → 日落 UTC datetime
    o = ephem.Observer(); o.lat, o.lon = '28.6139', '77.2090'; o.elevation = 216; o.pressure = 0
    o.horizon = '-0:34'
    o.date = ephem.Date(dt.datetime(day.year, day.month, day.day, 6, 0))  # 06:00 UTC = 11:30 IST，当天中午前
    return to_dt(o.next_setting(ephem.Sun()))
def diwali(year):
    """返回 (日期 ISO, 朔时刻 UTC, 说明)。"""
    # 找 8–12 月的朔
    nms = []
    t = ephem.Date(dt.datetime(year, 8, 1))
    for _ in range(6):
        nm = ephem.next_new_moon(t); nms.append(nm); t = ephem.Date(nm + 1)
    # amanta 月：从朔 k 到朔 k+1；以月初朔时太阳恒星黄经所在星座命名；Kanya(150–180) = 阿湿缚庾阇月(Ashvina)
    months = []
    for k in range(len(nms) - 1):
        lon0 = sun_sid(to_dt(nms[k])); lon1 = sun_sid(to_dt(nms[k + 1]))
        # 该月内是否有「入 Tula」(180°) 的 sankranti：lon0 < 180 <= lon1（处理环绕）
        has_tula = (lon0 < 180 <= lon1) if lon1 >= lon0 else (lon0 < 180 or 180 <= lon1)
        months.append((nms[k], nms[k + 1], lon0, has_tula))
    # 阿湿缚庾阇月 = 含「入 Tula」sankranti 的那个 amanta 月（朔→朔）；若两个月都含（不可能）/ 都不含（闰月情形：前一月为 adhika），取最后一个含的
    cands = [m for m in months if m[3]]
    if not cands: return None
    m = cands[-1]
    nm_end = to_dt(m[1])  # 阿湿缚庾阇月末的朔（UTC）= amavasya 结束
    # amavasya 开始：黄经差到达 348° 的时刻（二分）
    lo = ephem.Date(m[1] - 1.6); hi = ephem.Date(m[1])
    for _ in range(40):
        mid = ephem.Date((lo + hi) / 2); e = elong(mid)
        if e >= 348 or e < 10: hi = mid
        else: lo = mid
    am_start = to_dt(hi)
    day = (nm_end + IST).date(); prev = day - dt.timedelta(days=1)
    PR = dt.timedelta(hours=2, minutes=24)  # pradosh 约三个 muhurta
    def prevails(d):
        ss = sunset_delhi(d); return am_start < ss + PR and nm_end > ss
    pD, pP = prevails(day), prevails(prev)
    if pD and pP:
        # 两天的 pradosh 都在 amavasya 里：取 amavasya 也覆盖子夜（nishita）的那天，通常是前一天
        midnight = dt.datetime(day.year, day.month, day.day) - IST  # prev 的子夜（IST 00:00 of day）
        d = prev if am_start < midnight < nm_end else day; note = '两天 pradosh 均在 amavasya 内，取覆盖子夜的一天'
    elif pD: d = day; note = '朔在日落之后，当天 pradosh 在 amavasya 内'
    elif pP: d = prev; note = '朔在日落之前，取前一天'
    else: d = prev if (sunset_delhi(prev) < nm_end) else day; note = '按就近规则'
    return d.isoformat(), nm_end.strftime('%Y-%m-%d %H:%M UTC'), note + '；amavasya ' + (am_start + IST).strftime('%m-%d %H:%M') + ' → ' + (nm_end + IST).strftime('%m-%d %H:%M') + ' IST'

def fullmoons(year):
    out = []; t = ephem.Date(dt.datetime(year, 9, 25))
    for _ in range(4):
        fm = ephem.next_full_moon(t); d = to_dt(fm); out.append(d.strftime('%Y-%m-%d %H:%M')); t = ephem.Date(fm + 1)
    return out

def main():
    terms = {}; dw = {}; fms = {}
    for y in range(1900, 2101):
        ld = solar_term(y, 225, (11, 7)) + BJ; xx = solar_term(y, 240, (11, 22)) + BJ; dz = solar_term(y, 270, (12, 21)) + BJ
        rm = lambda t: (t + dt.timedelta(seconds=30)).strftime('%Y-%m-%d %H:%M')  # 取整到分，不截断
        terms[y] = {'lidong': rm(ld), 'xiaoxue': rm(xx), 'dongzhi': rm(dz)}
        r = diwali(y); dw[y] = {'date': r[0], 'newmoon': r[1], 'note': r[2]} if r else None
        fms[y] = fullmoons(y)
    # 对拍
    cal = json.load(open(os.path.join(HERE, '..', 'research', 'fest_C.json'), encoding='utf-8'))
    official = {r['year']: r['date'] for r in cal['dates_table'] if r['festival'] == 'diwali'}
    mism = []
    for y, d in official.items():
        if dw[y]['date'] != d: mism.append((y, d, dw[y]['date'], dw[y]['note']))
    print('排灯节对拍（官方 vs 算法）：', '全部一致' if not mism else mism)
    lk = {r['year']: r['date'] for r in cal['dates_table'] if r['festival'] == 'loy-krathong'}
    json.dump({'terms': terms, 'diwali': dw, 'fullmoons': fms, 'diwali_official': official, 'loy_krathong_official': lk,
               'method': {'terms': '太阳视黄经 225°/240°/270°（PyEphem，当日历元黄道），换算北京时间',
                          'diwali': 'amanta 历：以「入天秤（恒星黄经 180°，Lahiri 岁差近似）」的 sankranti 所在的朔望月为阿湿缚庾阇月，其末朔为 amavasya；按德里日落时 tithi 是否仍为 amavasya 定日（Dharmasindhu 的 pradosh 规则）',
                          'loy_krathong': '泰历十二月望为算术历，页面用泰国官方公告表 2015–2027；其它年份只给天文望日并标 ±1 天'}},
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('wrote', OUT, '| 2026 立冬', terms[2026]['lidong'], '| 2026 排灯节', dw[2026], '| 2026 望', fms[2026])

if __name__ == '__main__':
    main()
