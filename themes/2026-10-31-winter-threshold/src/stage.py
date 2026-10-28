# -*- coding: utf-8 -*-
"""序章「这十天」：固定舞台（NASA 夜光图 + 纬度夜带 + 城市灯 + HUD）+ 八张滚动卡片。每一步：日期、点亮的城市、主城的昼长。"""
import html, datetime as dt
import editorial as E, figs, sun
esc = lambda s: html.escape(str(s), quote=True)
WD = {'一': '周一', '二': '周二', '三': '周三', '四': '周四', '五': '周五', '六': '周六', '日': '周日'}

def stage(cities, img_src):
    """左侧固定舞台：上半是会推镜头的夜光地图，下半是「昼带」——15 座城按纬度从北到南排，每行一条 0–24 时的轨道，亮的那段是白昼。"""
    rows = []
    for c in sorted(cities, key=lambda c: -c['lat']):
        lat = f"{abs(c['lat']):.0f}°{'N' if c['lat'] >= 0 else 'S'}"
        rows.append(f'<div class="dbrow" data-city="{esc(c["id"])}"><span class="dbn"><i class="lamp off"></i><span class="dbnm">{esc(c["name_zh"])}</span><small>{lat}</small></span>'
                    f'<span class="dbt"><b class="dbb"></b></span><span class="dbv"></span></div>')
    band = (f'<div class="dayband" id="dayband" aria-label="十五座城当天的日出日落与昼长">'
            f'<div class="dbh"><span>北 → 南</span><span class="dbscale"><i>0</i><i>6</i><i>12</i><i>18</i><i>24 时</i></span><span class="dbnote">每行一条 0–24 时的轨道，亮段是白昼</span><span>昼长</span></div>{"".join(rows)}</div>')
    lads = ''.join(f'<button type="button" class="lad" data-lvl="{i}" aria-label="第 {i+1} 天 {esc(s["date"])}"><i></i></button>' for i, s in enumerate(E.STEPS))
    return (f'<div class="jwrap"><div class="jstage" id="jstage"><div class="jscene" id="jscene">{figs.stage_map(cities, img_src)}'
            f'<div class="jhud" id="jhud"><span class="jk" id="jk"></span><div class="jdate" id="jdate"></div><div class="jt" id="jt"></div></div>'
            f'<div class="jdl" id="jdlbox"><b id="jdl"></b><span id="jdls"></span></div><div class="jladder">{lads}</div></div>'
            f'{band}</div>')

def steps(IM, FEST):
    out = []
    for i, s in enumerate(E.STEPS):
        ph = ''
        im = IM.get(s.get('photo'))
        if im: ph = f'<figure class="jph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{esc(im["subject"][:90])}{"…" if len(im["subject"]) > 90 else ""} 图：{esc(im["author_short"])}，{esc(im["license_short"])}。</figcaption></figure>'
        chips = ''.join(f'<a class="chip a" href="#n-{esc(f)}">{esc(FEST[f]["short"])}</a>' for f in s['fest'] if f in FEST)
        y, m, d = s['date'].split('-')
        out.append(f'''<article class="jstep" id="lvl-{esc(s['id'])}" data-lvl="{i}"><div class="jcard">
<div class="jcard-hd"><span class="jno">{i+1:02d} / {len(E.STEPS):02d}</span><span>{int(m)} 月 {int(d)} 日 · {WD[s['wd']]}</span><span>{esc(s['kicker'])}</span></div>
<h3>{esc(s['title'])}</h3>
<p class="jbig"><b id="jb-{i}"></b><small id="jbu-{i}"></small></p>
<p class="jbasis" id="jbs-{i}"></p>
<p class="jtag">{esc(s['text'])}</p>
<div class="jfest">{chips}</div>
{ph}</div></article>''')
    return f'<div class="jsteps">{"".join(out)}</div></div>'

def data(cities):
    """给 app.js：每步每城的昼长、日出日落、是否点亮。"""
    C = {c['id']: c for c in cities}
    levels = []
    for s in E.STEPS:
        y, m, d = (int(x) for x in s['date'].split('-')); date = dt.date(y, m, d)
        row = {'id': s['id'], 'date': s['date'], 'wd': WD[s['wd']], 'kicker': s['kicker'], 'title': s['title'], 'main': s['main'], 'lit': s['cities'], 'doy': date.timetuple().tm_yday, 'cities': {}}
        for c in cities:
            dl = sun.day_length(c['lat'], date); rise, sset = sun.sun_times(c['lat'], c['lon'], date, c.get('tz', 0))
            row['cities'][c['id']] = {'dl': round(dl, 2), 'rise': rise, 'set': sset, 'on': c['id'] in s['cities']}
        levels.append(row)
    return levels
