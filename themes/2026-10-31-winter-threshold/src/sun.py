# -*- coding: utf-8 -*-
"""昼长与日出日落（NOAA 近似：太阳赤纬 + 均时差，天顶距 90.833° 含折射）。与 app.js 里的 JS 版同公式。"""
import math, datetime as dt
R = math.radians; D = math.degrees

def frac_year(date, hour=12.0):
    doy = date.timetuple().tm_yday
    return 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)

def decl_eqt(g):
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = 0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g)
    return decl, eqt  # 弧度, 分钟

def day_length(lat, date):
    """昼长（小时），天顶距 90.833°。极昼 24、极夜 0。"""
    decl, _ = decl_eqt(frac_year(date))
    c = (math.cos(R(90.833)) / (math.cos(R(lat)) * math.cos(decl))) - math.tan(R(lat)) * math.tan(decl)
    if c >= 1: return 0.0
    if c <= -1: return 24.0
    return 2 * D(math.acos(c)) / 15.0

def sun_times(lat, lon, date, tz_hours):
    """返回 (日出, 日落) 当地时间字符串 HH:MM（按给定固定时差，不考虑夏令时）。"""
    decl, eqt = decl_eqt(frac_year(date))
    c = (math.cos(R(90.833)) / (math.cos(R(lat)) * math.cos(decl))) - math.tan(R(lat)) * math.tan(decl)
    if c >= 1 or c <= -1: return None, None
    ha = D(math.acos(c))
    rise = 720 - 4 * (lon + ha) - eqt + tz_hours * 60
    sset = 720 - 4 * (lon - ha) - eqt + tz_hours * 60
    f = lambda m: '%02d:%02d' % (int(m // 60) % 24, int(round(m % 60)) % 60)
    return f(rise), f(sset)

def hm(hours):
    h = int(hours); m = int(round((hours - h) * 60))
    if m == 60: h += 1; m = 0
    return f'{h} 小时 {m:02d} 分'
