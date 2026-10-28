# -*- coding: utf-8 -*-
"""序章「这十天」v2：全屏固定舞台。NASA 夜光图上的镜头随日期 t（10/31 → 11/11，按天连续）移动；
底部是可拖、可甩的日期刻度尺（与页面滚动是同一个量）；左下是半透明卡片，右侧是十五城的昼带。
HTML 先把第一步渲染好（不开脚本也有内容），其余由 app.js 按 data() 给的逐日数据接管。"""
import html, datetime as dt
import editorial as E, figs, sun
esc = lambda s: html.escape(str(s), quote=True)
WD = {'一': '周一', '二': '周二', '三': '周三', '四': '周四', '五': '周五', '六': '周六', '日': '周日'}
WDN = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
DAY0 = dt.date(2026, 10, 31)
NDAYS = 12  # 10/31 … 11/11


def _day_index(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return (dt.date(y, m, d) - DAY0).days


def stage(cities, img_src, IM, FEST):
    rows = []
    for c in sorted(cities, key=lambda c: -c['lat']):
        lat = f"{abs(c['lat']):.0f}°{'N' if c['lat'] >= 0 else 'S'}"
        rows.append(f'<div class="dbrow" data-city="{esc(c["id"])}"><span class="dbn"><i class="lamp off"></i><span class="dbnm">{esc(c["name_zh"])}</span><small>{lat}</small></span>'
                    f'<span class="dbt"><b class="dbb"></b></span><span class="dbv"></span></div>')
    band = (f'<div class="tlbandw" id="tlbandw"><button type="button" class="tlbtn glass" id="tlbtn" aria-expanded="false" aria-controls="dayband"><i class="lamp"></i>昼带 · 十五城<span class="tlbtn-c" aria-hidden="true"></span></button>'
            f'<aside class="tlband glass" id="dayband" aria-label="十五座城当天的日出日落与昼长" hidden>'
            f'<div class="dbh"><span>北 → 南</span><span class="dbscale"><i>0</i><i>6</i><i>12</i><i>18</i><i>24 时</i></span><span>昼长</span></div>{"".join(rows)}</aside></div>')
    # 刻度尺：12 天的刻度 + 有节的日子做成可点的灯
    ticks = ''.join(f'<span class="rtick{" wk" if (DAY0 + dt.timedelta(days=i)).weekday() >= 5 else ""}" style="left:{i / (NDAYS - 1) * 100:.3f}%"><span>{(DAY0 + dt.timedelta(days=i)).month}/{(DAY0 + dt.timedelta(days=i)).day}</span></span>' for i in range(NDAYS))
    marks = ''.join(f'<button type="button" class="rmark" data-step="{k}" style="left:{_day_index(s["date"]) / (NDAYS - 1) * 100:.3f}%" aria-label="跳到 {esc(s["date"][5:].replace("-", "/"))} {esc(s["label"])}"><i></i><span>{esc(s["label"])}</span></button>' for k, s in enumerate(E.STEPS))
    s0 = E.STEPS[0]; im = IM.get(s0.get('photo'))
    chips0 = ''.join(f'<a class="chip a" href="#n-{esc(f)}" data-open="{esc(f)}">{esc(FEST[f]["short"])}</a>' for f in s0['fest'] if f in FEST)
    y, m, d = s0['date'].split('-')
    card = (f'<aside class="tlcard glass" id="tlcard" aria-live="polite">'
            f'<div class="tlhd"><span class="tlno" id="tlno">01 / {len(E.STEPS):02d}</span><span id="tlkick">{esc(s0["kicker"])}</span></div>'
            f'<h3 class="tltitle" id="tltitle">{esc(s0["title"])}</h3>'
            f'<p class="tlbig"><b id="tlbig"></b><small id="tlbigu"></small></p><p class="tlbasis" id="tlbasis"></p>'
            f'<p class="tltext" id="tltext">{esc(s0["text"])}</p><div class="tlchips" id="tlchips">{chips0}</div>'
            + (f'<figure class="tlph"><img id="tlimg" src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}"><figcaption id="tlcap">{esc(_cap(im))}</figcaption></figure>' if im else '')
            + '<p class="tlcredit">底图：NASA「黑色弹珠」2016 夜光图，公有领域 · 昼长按各城纬度现算</p></aside>')
    hud = (f'<div class="tlhud" id="jhud"><span class="tlch">00 · 序章 · 这十天 · 拖动底部刻度尺，或往下滚</span><span class="jk" id="jk">{esc(s0["kicker"])}</span>'
           f'<div class="jdate" id="jdate">{int(m)} 月 {int(d)} 日<small>{WD[s0["wd"]]}</small></div><div class="jt" id="jt">{esc(s0["title"])}</div></div>')
    ruler = (f'<div class="tlruler glass" id="tlruler" role="slider" tabindex="0" aria-label="这十天的日期：拖动、甩动或用方向键" aria-valuemin="0" aria-valuemax="{NDAYS - 1}" aria-valuenow="0" aria-valuetext="10 月 31 日 万圣节">'
             f'<div class="rtrack" id="rtrack"><span class="rline"></span>{ticks}{marks}<span class="rhead" id="rhead"><i></i></span></div></div>')
    steps_sr = ''.join(f'<li><b>{esc(s["date"][5:].replace("-", "/"))} {esc(s["kicker"])}：{esc(s["title"])}</b> {esc(s["text"])}</li>' for s in E.STEPS)
    return (f'<div class="tlpin" id="tlpin"><div class="tlstage" id="tlstage"><div class="tlmap" id="jscene">{figs.stage_map(cities, img_src)}</div>'
            f'{hud}{card}{band}{ruler}</div></div><ol class="sr-only" id="tlsr">{steps_sr}</ol>')


def _cap(im):
    s = im['subject']
    return (s[:80] + '…' if len(s) > 80 else s) + f' 图：{im["author_short"]}，{im["license_short"]}。'


def data(cities, IM, FEST):
    """给 app.js：逐日（10/31 → 11/11）每城的昼长与日出日落、那天点亮的城市；以及八步的文字。"""
    lit_by_day = {}
    for k, s in enumerate(E.STEPS):
        lit_by_day.setdefault(_day_index(s['date']), []).extend(s['cities'])
    days = []
    for i in range(NDAYS):
        date = DAY0 + dt.timedelta(days=i)
        row = {'date': date.isoformat(), 'wd': WDN[date.weekday()], 'doy': date.timetuple().tm_yday, 'lit': sorted(set(lit_by_day.get(i, []))),
               'step': next((k for k, s in enumerate(E.STEPS) if _day_index(s['date']) == i), -1), 'cities': {}}
        for c in cities:
            dl = sun.day_length(c['lat'], date); rise, sset = sun.sun_times(c['lat'], c['lon'], date, c.get('tz', 0))
            row['cities'][c['id']] = {'dl': round(dl, 3), 'rise': rise, 'set': sset}
        days.append(row)
    steps = []
    for k, s in enumerate(E.STEPS):
        im = IM.get(s.get('photo'))
        steps.append({'id': s['id'], 'day': _day_index(s['date']), 'date': s['date'], 'wd': WD[s['wd']], 'label': s['label'], 'kicker': s['kicker'], 'title': s['title'],
                      'text': s['text'], 'main': s['main'], 'cities': s['cities'],
                      'img': ('assets/' + im['file']) if im else '', 'alt': im['subject'] if im else '', 'cap': _cap(im) if im else '',
                      'fest': [[f, FEST[f]['short']] for f in s['fest'] if f in FEST]})
    return {'days': days, 'steps': steps, 'n': NDAYS}
