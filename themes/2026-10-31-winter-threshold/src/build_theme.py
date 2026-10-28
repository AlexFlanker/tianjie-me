#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7 题「冬天的门槛」：把 research/fest_*.json + editorial.py + images.json + tables.json + lunar_table.json 合成 ../index.html 与 ../meta.json。
用法（仓库根目录）：python3 themes/2026-10-31-winter-threshold/src/build_theme.py"""
import json, os, re, sys, html, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial as E
import figs, stage, demos, sun, fixes

def esc(s): return html.escape(str(s), quote=True)
def J(name): return json.load(open(os.path.join(HERE, 'research', name), encoding='utf-8'))
A, B, C, Dd = J('fest_A.json'), J('fest_B.json'), J('fest_C.json'), J('fest_D.json')
TABLES = json.load(open(os.path.join(HERE, 'tables.json'), encoding='utf-8'))
LUNAR = json.load(open(os.path.join(HERE, 'lunar_table.json'), encoding='utf-8'))
for _l in fixes.patch_data(A, B, C, Dd): print('data', _l)
NODES = {}
for route, src in (('A', A), ('B', B), ('C', C), ('D', Dd)):
    for n in src['nodes']: n['route'] = route; NODES[n['id']] = n
IM = {}
for i in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8')): IM[i['id']] = i
CONF_CLS = {'高': 'h', '中': 'm', '低': 'l'}
def conf(c): return f'<span class="conf {CONF_CLS.get(c, "m")}" title="资料置信度：高 = 一手官方或学术来源；中 = 可靠二手；低 = 通行说法">置信度 {esc(c or "中")}</span>'
def srcs(ss, cls='src', n=6):
    if not ss: return ''
    seen, uniq = set(), []
    for s in ss:
        if not isinstance(s, dict): continue
        k = s.get('url') or s.get('title')
        if not k or k in seen: continue
        seen.add(k); uniq.append(s)
    return f'<p class="{cls}">来源：' + '；'.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>' if s.get('url') else esc(s.get('title', '')) for s in uniq[:n]) + '</p>'

# ---------- 城市表（D 路 + 纽约、金边）
TZ = {'dublin': 0, 'london': 0, 'lewes': 0, 'utrecht': 1, 'stockholm': 1, 'rome': 1, 'beijing': 8, 'tokyo': 9, 'delhi': 5.5, 'kathmandu': 5.75, 'sukhothai': 7, 'bangkok': 7, 'mexico-city': -6, 'la-paz': -4, 'sydney': 10, 'new-york': -5, 'phnom-penh': 7}
CITIES = {c['id']: c for c in Dd['cities']}
CITIES['new-york'] = dict(id='new-york', name_zh='纽约', name='New York', lat=40.7, lon=-74.0, elev_m=10, koppen='Cfa', koppen_source=NODES['halloween']['city'].get('koppen_source') or {}, climate=NODES['halloween']['city'].get('climate') or {}, sources=[])
CITIES['phnom-penh'] = dict(id='phnom-penh', name_zh='金边', name='Phnom Penh', lat=11.56, lon=104.92, elev_m=12, koppen='Aw', climate=NODES['pchum-ben']['city'].get('climate') or {}, sources=[])
for cid, c in CITIES.items():
    c['tz'] = TZ.get(cid, 0); c.setdefault('name_zh', c.get('name_zh') or c.get('name'))
STAGE_CITIES = [CITIES[k] for k in ('dublin', 'lewes', 'utrecht', 'stockholm', 'rome', 'new-york', 'mexico-city', 'la-paz', 'beijing', 'tokyo', 'delhi', 'kathmandu', 'sukhothai', 'sydney', 'phnom-penh')]
SHORT = {'samhain': 'Samhain', 'halloween': '万圣节', 'all-saints-souls': '诸圣 · 诸灵', 'rome-contrast': '罗马 Parentalia', 'bonfire-night': '篝火夜', 'martinmas': '圣马丁节', 'lucia': '圣露西亚', 'todos-santos-andes': 'Todos Santos', 'halloween-south': '万圣节（悉尼）',
         'hanyi': '寒衣节', 'lidong': '立冬', 'xiayuan': '下元节', 'zhongyuan-contrast': '中元 · 盂兰盆', 'shichigosan': '七五三', 'niinamesai': '新尝祭', 'qin-new-year': '秦十月朔', 'diwali': '排灯节', 'tihar': 'Tihar', 'loy-krathong': '水灯节', 'pchum-ben': 'Pchum Ben', 'dia-de-muertos': '亡灵节'}
LANE_OF = {}
for lid, lname, ids in E.LANES:
    for i in ids: LANE_OF[i] = (lid, lname)
CMP = {r['id']: r for r in E.COMPARE}

def date_main(n):
    return (n.get('date_2026') or '')[:10]

def fest_record(nid):
    n = NODES[nid]; r = CMP.get(nid, {}); cid = r.get('city') or ''
    c = CITIES.get(cid) or {}
    lat = c.get('lat', (n.get('city') or {}).get('lat')); lon = c.get('lon', (n.get('city') or {}).get('lon'))
    d = date_main(n); doy = dt.date(*[int(x) for x in d.split('-')]).timetuple().tm_yday
    basis = n.get('calendar_basis') or 'gregorian-fixed'; bn = E.BASIS_NAME.get(basis, ('固定日', ''))
    img = E.NODE_IMG.get(nid); im = IM.get(img) if img else None
    cl = (n.get('city') or {}).get('climate') or {}
    return dict(id=nid, node=nid, name=n['name'], short=SHORT.get(nid, n['name']), lane=LANE_OF.get(nid, ('', ''))[0], laneName=LANE_OF.get(nid, ('', ''))[1],
                city=c.get('name_zh') or (n.get('city') or {}).get('name', ''), cityId=cid, lat=lat, lon=lon, date=d, doy=doy, dl=round(sun.day_length(lat, dt.date(*[int(x) for x in d.split('-')])), 2) if lat is not None else None,
                basis=basis, basisName=bn[0], basisSub=bn[1], spread=n.get('spread') or 'native', spreadName=E.SPREAD_NAME.get(n.get('spread') or 'native', '本土'),
                kind=r.get('kind', ''), kindName=E.KIND_NAME.get(r.get('kind', ''), ''), season=r.get('season', ''), note=r.get('note', ''),
                koppen=c.get('koppen') or (n.get('city') or {}).get('koppen', ''), koppen_note=(n.get('city') or {}).get('koppen_note', ''),
                rule=n.get('date_rule', ''), range=n.get('date_range', ''), three=n.get('three') or {}, climate={k: cl.get(k, '') for k in ('season', 'harvest', 'rain', 'frost')},
                img=im['file'] if im else None, contrast=nid in E.CONTRAST)
FEST = {nid: fest_record(nid) for nid in NODES}
ORDER = [r['id'] for r in E.COMPARE]

# ---------- 卷首
def hero():
    M = E.META; H = E.HERO
    steps = ''.join(f'<li><span>{esc(s)}</span></li>' for s in H['steps'])
    week = ''.join(f'<span><i>{esc(d)}</i> <b>{esc(t)}</b> {esc(x)}</span>' for d, t, x in H['week'])
    stats = ''.join(f'<div class="stat"><div class="k">{esc(k)}</div><div class="v"><b class="cnt" data-to="{v}" data-dec="{dec}">{(("%." + str(dec) + "f") % v) if dec else v}</b><small>{esc(u)}</small></div><div class="d">{esc(d)}</div><div class="n">{esc(n)}</div></div>' for k, v, dec, u, d, n in H['stats'])
    t1, t2 = M['title'].split('：', 1)
    return f'''<header class="hero band"><div class="wide">
  <div class="strip fade"><span><b>一周一题</b>第 {M['no']} 题</span><span><b>上线</b>{M['date']}</span><span><b>格式</b>{esc(M['format'])}</span><span><b>阅读</b>{esc(M['reading_time'])}</span></div>
  <h1 class="fade">{esc(t1)}<small>{esc(t2)}</small></h1>
  <p class="sub fade">{esc(M['subtitle'])}</p>
  <div class="lead"><p class="thesis fade">{H['thesis']}</p><ol class="steps fade">{steps}</ol></div>
  <figure class="field" id="field"><div class="fieldbox" id="fieldbox"><canvas id="fcv" width="1200" height="520" aria-label="夜的田野：横轴日期、纵轴纬度、底色是黑夜长短"></canvas><svg class="fov" id="fov" viewBox="0 0 1200 520" preserveAspectRatio="none" aria-hidden="true"></svg><div class="ftip" id="ftip"></div></div>
  <figcaption class="fcap"><span><b>夜的田野。</b>横轴 10 月 1 日 → 12 月 31 日，纵轴北纬 62° → 南纬 36°；底色越深，那一天那条纬线上的黑夜越长（白线是等昼长线）。每盏灯是一种节日 2026 年落下的日子与它核心城市的纬度，悬停看昼长，点灯跳到它的卡片。虚线框是这十天。</span><span class="fkey">昼长按太阳赤纬算，天顶距 90.833° · 不计海拔</span></figcaption></figure>
  <div class="week fade">{week}</div>
  <div class="stats fade">{stats}</div>
</div></header>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n}</small>{esc(t)}</a>' for cid, n, t, _ in E.CHAPTERS)
    links += '<a href="#end" data-nav="end"><small>末</small>参考 · 方法</a>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第 {"一二三四五六七八"[n-1]} 章'
    return f'<div class="chead fade"><div class="cno">{n:02d}<small>{label}</small></div><h2>{esc(t)}</h2><p class="lede">{lede}</p></div>'

# ---------- 序章
def ch_days():
    return (f'<section class="chap journey band" id="days"><div class="wide">{chead("days")}</div>' + stage.stage(STAGE_CITIES, 'assets/earth-night-1920.jpg') + stage.steps(IM, FEST)
            + '<p class="jnote">底图：NASA「黑色弹珠」2016 年全球夜间灯光合成图（Suomi NPP / VIIRS，公有领域）。地图上的横带按当天各纬度的黑夜长短加深；城市的灯在有节的那天点亮。昼长与日出日落按太阳赤纬与均时差的标准近似算，取各城标准时、不含夏令时，误差在几分钟内。</p></section>')

# ---------- 第一章
def ch_now():
    dm = NODES['dia-de-muertos']; hw = NODES['halloween']; dw = NODES['diwali']; hy = NODES['hanyi']; ld = NODES['lidong']
    def nums(n, key):
        for x in n.get('numbers', []):
            if key in x.get('label', ''): return x
        return {}
    nrf = nums(hw, '2026 预期'); nrf25 = nums(hw, '2025')
    cards = [
        ('10/31 · 周六 14:00', '墨西哥城亡灵节大游行', '2016', '年起 · 第十届', '从改革大道的狩猎女神雕像走到宪法广场。这条「传统」只有十年：2015 年 007《幽灵党》开场拍了一场虚构的亡灵节游行，次年市政府把它办成了真的；今年 6 月为世界杯还办过一场夏季版。亡灵节本身 2008 年列入人类非遗。', [s for s in dm.get('sources', []) if re.search(r'gob|Desfile|desfile|游行|unesco|UNESCO', (s.get('title') or '') + (s.get('url') or ''))][:4]),
        ('10/31 · 周六', '万圣节的生意', esc(nrf.get('value', '135')), '亿美元 · 美国 2026 年预期（NRF）', f'美国零售联合会的年度调查：2025 年创纪录的 {nrf25.get("value", "131")} 亿美元，2026 年预期 {nrf.get("value", "135")} 亿，49% 的人 9 月或更早就开始买。日子是爱尔兰的夏末，内容是北美的货架——「门槛」从霜期变成了货架期。', [s for s in hw.get('sources', []) if 'nrf' in (s.get('url') or '').lower()][:3]),
        ('11/8 → 11/9', '同一轮新月，两个节', '12:32', '印度时间 11/9 朔 · 北京时间 15:02', '印度按日落时的 tithi：11 月 8 日傍晚 amavasya 当值，当晚点灯；中国按《农历的编算和颁行》以含朔时刻的那一天为初一：11 月 9 日是十月初一，送寒衣。同一个天象，两种数法，差出一天。', [s for s in dw.get('sources', [])[:2]] + [s for s in hy.get('sources', []) if re.search(r'天文台|hko|33661', (s.get('title') or '') + (s.get('url') or ''))][:2]),
        ('11/7 · 周六 17:52', '立冬 = 天文学上的 Samhain', '225°', '太阳黄经 · 秋分与冬至正中', '立冬是太阳黄经 225° 的时刻，正好在秋分（180°）与冬至（270°）之间——天文学上的「跨季日」，也是 Samhain 被赋予的天文定义。中国把它钉在黄河流域的物候上：「水始冰，地始冻」，北京常年 11 月 8 日第一次跌破冰点。', [s for s in ld.get('sources', [])[:3]]),
    ]
    out = ''.join(f'<article class="nowcard fade"><div class="d">{esc(d)}</div><h3>{esc(t)}</h3><p class="big">{b}<small>{esc(u)}</small></p><p>{esc(x)}</p>{srcs(ss)}</article>' for d, t, b, u, x, ss in cards)
    return f'<section class="chap" id="now"><div class="wide">{chead("now")}<div class="nowcards">{out}</div></div></section>'

# ---------- 节点卡
def node_card(nid):
    n = NODES[nid]; f = FEST[nid]; im = IM.get(E.NODE_IMG.get(nid) or '')
    ph = f'<figure class="nph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{esc(im["subject"][:110])}{"…" if len(im["subject"]) > 110 else ""} 图：{esc(im["author_short"])}，{esc(im["license_short"])}。</figcaption></figure>' if im else ''
    c = n.get('city') or {}; lat = c.get('lat')
    where = f'{esc(c.get("name", ""))} · {("北纬 " if lat >= 0 else "南纬 ") + str(abs(lat)) + "°" if lat is not None else ""} · {esc(c.get("koppen", ""))}'
    three = n.get('three') or {}
    tl = ''.join(f'<li><i>{esc(t.get("year_label") or t.get("year"))}</i><div>{esc(t.get("label", ""))}{("：" + esc(t["text"])) if t.get("text") else ""}</div></li>' for t in (n.get('timeline') or [])[:10])
    nums = ''.join(f'<div><span>{esc(x["label"])}</span><b>{esc(x["value"])}{(" " + esc(x["unit"])) if x.get("unit") else ""}</b></div>' for x in (n.get('numbers') or [])[:4])
    disp = f'<p class="dispute"><b>两说</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    cl = c.get('climate') or {}
    clim = ''.join(f'<span>{k}</span><b>{esc(v)}</b>' for k, v in (('这一天', cl.get('season')), ('收成', cl.get('harvest')), ('雨季', cl.get('rain')), ('霜', cl.get('frost'))) if v)
    wasny = n.get('was_new_year') or ''
    o = n.get('origin') or {}
    kind = f'<span class="chip a">{esc(f["kindName"])}</span>' if f.get('kindName') else ''
    return f'''<article class="ncard fade{" contrast" if nid in E.CONTRAST else ""}" id="n-{esc(nid)}" data-node="{esc(nid)}" data-lane="{esc(f["lane"])}">
<div class="nhd"><span class="ny">{esc(f["date"][5:].replace("-", "/"))}</span><span class="chip">{esc(f["basisName"])}{(" · " + esc(f["basisSub"])) if f["basisSub"] else ""}</span>{kind}<span class="chip">{esc(f["spreadName"])}</span><span>{where}</span>{conf(n.get('confidence'))}</div>
<h3>{esc(n['name'])}</h3><p class="nobj">{esc(n.get('name_local', ''))}{(' · ' + esc(n.get('region', ''))) if n.get('region') else ''}</p>
<p class="why">{esc(n.get('why', ''))}</p>
<div class="nrow"><span>怎么定日</span><b class="k">{esc(n.get('date_rule', ''))}</b><span>压在哪道门槛上</span><b>{esc(n.get('threshold', ''))}</b>{('<span>岁首</span><b>' + esc(wasny) + '</b>') if wasny and not wasny.startswith('否') else ''}</div>
{ph}
<details class="fold"><summary>来历、三件事、怎么传开的、数字与来源</summary><p><b>{esc(o.get('year_label', ''))}</b> {esc(o.get('text', ''))}</p><p>{esc(n.get('text', ''))}</p>
<div class="nrow"><span>请亡灵</span><b>{esc(three.get('dead', '—'))}</b><span>点灯</span><b>{esc(three.get('light', '—'))}</b><span>吃一顿</span><b>{esc(three.get('food', '—'))}</b></div>
<div class="nrow"><span>传播</span><b>{esc(n.get('spread_text', ''))}</b>{clim}</div>
{('<ol class="tl">' + tl + '</ol>') if tl else ''}<div class="nnums">{nums}</div>{disp}{srcs(n.get('sources'), n=8)}</details></article>'''

# ---------- 第二章
def ch_threshold():
    items = [dict(id=i, name=FEST[i]['short'], date=FEST[i]['date'], basis=FEST[i]['basis'], lane=FEST[i]['lane']) for i in NODES]
    wheel = figs.wheel_svg(items, size=520)
    chips = '<div class="lchips" id="lane-chips"><button type="button" data-lane="all" aria-pressed="true">全部</button>' + ''.join(f'<button type="button" data-lane="{lid}" aria-pressed="false">{esc(ln)}</button>' for lid, ln, _ in E.LANES) + '</div>'
    key = '<div class="lkey"><span><svg width="14" height="14"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>公历固定日</span><span><svg width="14" height="14"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="2 1.5"/></svg>跟月亮走</span><span>底色 = 两道门槛：夏末（7 月下旬–9 月中）、冬初（10 月下旬–11 月下旬）</span></div>'
    left = f'<div class="lanestage fade"><div class="wheelbox">{wheel}</div>{key}{chips}<p class="small" style="margin-top:8px">点年轮上的点跳到卡片；卡片滚过视口中线时年轮上的点一起亮。虚线边框的卡片是反例与对照。</p></div>'
    cards = ''
    for lid, ln, ids in E.LANES:
        sub = {'europe': '从都柏林到罗马：本土的夏末、教会定的 11 月、议会定的 11 月 5 日', 'eastasia': '黄河流域的十月：岁首、授衣、迎冬；日本把收成门槛钉成固定日', 'southasia': '季风退去后的第一个新月，与雨季末最满的河', 'americas': '教会日历搬到两个半球：雨季末的墨西哥高原、春天的安第斯、仲春的悉尼', 'contrast': '同样请亡灵回家，却不在冬天的门槛上'}.get(lid, '')
        cards += f'<div class="lanehd"><b>{esc(ln)}</b><span>{esc(sub)}</span></div>' + ''.join(node_card(i) for i in ids)
    return f'<section class="chap" id="threshold"><div class="wide">{chead("threshold")}<div class="lanewrap">{left}<div class="ncards">{cards}</div></div></div></section>'

# ---------- 第三章
def ch_compare():
    hd = ('<div class="cmphd" id="cmphd"><button type="button" data-sort="date" aria-pressed="true">节日 · 日期 ↕</button><button type="button" data-sort="lat">纬度 ↕</button><button type="button" data-sort="dl">当天昼长 ↕</button>'
          '<button type="button" data-sort="koppen">气候带 ↕</button><button type="button" data-sort="kind">门槛 ↕</button><button type="button" data-sort="basis">历法 ↕</button><button type="button" data-sort="spread">传播 ↕</button></div>')
    rows = []
    for r in E.COMPARE:
        f = FEST[r['id']]; lat = f['lat']; pct = (lat - (-40)) / 100.0 * 100; dl = f['dl']; cl = f['climate']
        rows.append(f'''<div class="cmprow{" ct" if f["contrast"] else ""}" data-date="{f['doy']}" data-lat="{lat}" data-dl="{dl}" data-koppen="{esc(f['koppen'])}" data-kind="{esc(f['kindName'])}" data-basis="{esc(f['basisName'])}" data-spread="{esc(f['spreadName'])}">
<div class="nm"><b><a href="#n-{esc(r['id'])}" style="color:inherit;text-decoration:none">{esc(f['short'])}</a></b><span>{esc(f['city'])} · {esc(f['date'][5:].replace('-', '/'))}{(' · ' + esc(r['note'])) if r.get('note') else ''}</span></div>
<div class="lat"><span>{'北纬' if lat >= 0 else '南纬'} {abs(lat):.1f}°</span><div class="sc"><u style="left:40%"></u><i style="left:{pct:.1f}%"></i></div></div>
<div class="dl"><span>{sun.hm(dl)}</span><div class="bar"><u></u><i style="width:{dl/24*100:.1f}%"></i></div></div>
<div class="kop">{esc(f['koppen'])}<small>{esc(f['koppen_note'] or '')}</small></div>
<div class="sea">{esc(r['season'])}<br><span class="chip a" style="margin-top:3px">{esc(f['kindName'])}</span></div>
<div><span class="chip">{esc(f['basisName'])}</span><br><small style="color:var(--muted)">{esc(f['basisSub'])}</small></div>
<div><span class="chip">{esc(f['spreadName'])}</span><br><button type="button" class="cmpbtn" style="margin-top:4px">详情</button></div>
<div class="cmpmore"><div><b>收成 / 农事</b>{esc(cl.get('harvest') or '—')}</div><div><b>雨季 / 季风 / 霜</b>{esc((cl.get('rain') or '—') + ('；霜：' + cl['frost'] if cl.get('frost') else ''))}</div><div><b>三件事</b>亡灵：{esc(f['three'].get('dead') or '—')}<br>灯：{esc(f['three'].get('light') or '—')}<br>吃：{esc(f['three'].get('food') or '—')}</div></div>
</div>''')
    same = ''.join(f'<li><b>{esc(k)}</b><span class="waf" aria-label="十九行里 {n} 行">' + ''.join('<i' + (' class="f"' if j < n else '') + '></i>' for j in range(19)) + f'<em>{n} / 19</em></span>{esc(v)}</li>' for k, n, v in E.SAME)
    diff = ''.join(f'<li><b>{esc(k)}</b>{esc(v)}<span class="ev">证据：' + ' '.join(f'<a href="#n-{esc(i)}">{esc(FEST[i]["short"])}</a>' for i in ids) + '</span></li>' for k, v, ids in E.DIFF)
    return f'''<section class="chap" id="compare"><div class="wide">{chead("compare")}
<div class="cmpwrap fade"><div class="cmpbox">{hd}<div id="cmpbody">{''.join(rows)}</div></div></div>
<p class="small" style="margin-top:8px">昼长按核心城市纬度与 2026 年日期算；纬度刻度从南纬 40° 到北纬 60°，竖线是赤道；柯本类型按 Beck 等 2018 的 1 km 数据逐城读取；「门槛」是编辑按各路气象与农业口径归的类。最后三行是对照组。</p>
<div class="sdgrid"><div class="sdcard fade"><h3>同：五件事</h3><ol>{same}</ol></div><div class="sdcard diff fade"><h3>异：四根轴</h3><ol>{diff}</ol></div></div>
</div></section>'''

# ---------- 第四章
def ch_three():
    cells = ['<div class="th"></div>'] + [f'<div class="th">{k}<b>{esc(t)}</b></div>' for k, t in zip(('一', '二', '三'), [t for _, t in E.THREE_COLS])]
    for rid in E.THREE_ROWS:
        r = E.THREE[rid]
        cells.append(f'<div class="rh"><b>{esc(r["name"])}</b><span>{esc(r["city"])}</span></div>')
        for key, _ in E.THREE_COLS:
            txt, img = r[key]; im = IM.get(img) if img else None
            fig = f'<figure><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"></figure><small>{esc(im["subject"][:60])}{"…" if len(im["subject"]) > 60 else ""} · {esc(im["license_short"])}</small>' if im else ''
            cells.append(f'<div class="tcell">{fig}<p{" class=none" if txt.startswith(("不祭", "篝火夜不", "排灯节不")) else ""}>{esc(txt)}</p></div>')
    return f'<section class="chap" id="three"><div class="wide">{chead("three")}<div class="three fade">{"".join(cells)}</div><p class="small" style="margin-top:10px">每格的来历与出处在第二章对应的卡片里；照片的作者与许可见卷末署名表。没有合规照片的格子不放图。</p></div></section>'

# ---------- 第五章
def ch_walls():
    items = [dict(id=i, name=FEST[i]['short'], date=FEST[i]['date'], basis=FEST[i]['basis'], lane=FEST[i]['lane']) for i in NODES]
    wheel2 = figs.wheel_svg(items, size=520, center=('年轮', '顶上 = 公历 1/1'), gid='wheel-g2', cls='wheel')
    body = {'lat': demos.wall_lat(), 'wheel': demos.wall_wheel(wheel2)}
    out = ''.join(f'<article class="wall fade" id="wall-{w["id"]}"><div class="hd"><b>{esc(w["title"])}</b><span class="f">{esc(w["formula"])}</span></div>{body[w["id"]]}<details class="fold"><summary>这面墙是怎么回事</summary><p>{esc(w["text"])}</p></details></article>' for w in E.WALLS)
    return f'<section class="chap band" id="walls"><div class="wide">{chead("walls")}<div class="walls">{out}</div></div></section>'

# ---------- 第六章
def ch_tools():
    opts = ''.join(f'<option value="{i}">{esc(FEST[i]["short"])} · {esc(FEST[i]["city"])}</option>' for i in ORDER)
    opts3 = ''.join(f'<option value="{i}">{esc(FEST[i]["short"])} · {esc(FEST[i]["city"])}</option>' for i in E.WATCH)
    T = {t['id']: t for t in E.TOOLS}
    def tool(tid, body, full=False): return f'<div class="tool fade{" full" if full else ""}"><div class="hd"><b>{esc(T[tid]["title"])}</b><p>{esc(T[tid]["lede"])}</p></div>{body}</div>'
    return f'<section class="chap" id="tools"><div class="wide">{chead("tools")}<div class="tools">{tool("dates", demos.tool_dates(), True)}{tool("pair", demos.tool_pair(opts))}{tool("list", demos.tool_list(opts3))}</div></div></section>'

# ---------- 第七章
def find_src(nid, pat):
    pool = Dd['cities'][0].get('koppen_source') and [Dd['cities'][0]['koppen_source']] if nid == 'cities' else NODES.get(nid, {}).get('sources', [])
    for s in pool or []:
        if isinstance(s, dict) and re.search(pat, (s.get('title') or '') + ' ' + (s.get('url') or ''), re.I): return s
    return None
def ch_rules():
    li = ''
    for k, (y, t, d, (nid, pat)) in enumerate(E.RULES):
        s = find_src(nid, pat)
        li += (f'<article class="rcard fade" style="--i:{k}"><span class="ry">{esc(y)}</span><b>{esc(t)}</b><p>{esc(d)}</p>'
               + (f'<a class="rgo" href="{esc(s["url"])}" target="_blank" rel="noopener">原文 / 入口 ↗</a>' if s and s.get('url') else '') + '</article>')
    return f'<section class="chap" id="rules"><div class="wide">{chead("rules")}<div class="rgrid">{li}</div></div></section>'

# ---------- 卷末
def refs_block():
    groups = [('欧洲与南半球（A 路）', [s for n in A['nodes'] for s in n.get('sources', [])] + [s for f in A.get('facts', []) for s in f.get('sources', [])]),
              ('中国与日本（B 路）', [s for n in B['nodes'] for s in n.get('sources', [])] + [s for f in B.get('facts', []) for s in f.get('sources', [])]),
              ('南亚与东南亚（C 路，含排灯节与水灯节官方日期表）', [s for n in C['nodes'] for s in n.get('sources', [])] + [s for r in C.get('dates_table', []) for s in (r.get('sources') or [])]),
              ('中美洲与十五座城市的气候（D 路）', [s for n in Dd['nodes'] for s in n.get('sources', [])] + [s for c in Dd['cities'] for s in (c.get('sources') or [])] + [c.get('koppen_source') for c in Dd['cities'] if c.get('koppen_source')])]
    out = []
    for g, ss in groups:
        seen, items = set(), []
        for s in ss:
            if not isinstance(s, dict): continue
            k = s.get('url') or s.get('title')
            if not k or k in seen: continue
            seen.add(k)
            items.append(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s.get("title") or s["url"])}</a></li>' if s.get('url') else f'<li>{esc(s.get("title", ""))}</li>')
        out.append(f'<h3>{esc(g)}（{len(items)}）</h3><ul>{"".join(items)}</ul>')
    return ''.join(out)
def credits():
    rows = ''.join(f'<tr><td>{esc(k)}</td><td>{esc(im["subject"])}</td><td>{esc(im["author_short"])}，{esc(im.get("year", ""))}</td><td>{esc(im["license_short"])}</td><td><a href="{esc(im["url_page"])}" target="_blank" rel="noopener">{esc(im["source_name"])}</a></td></tr>' for k, im in IM.items())
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>作者 / 年代</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'
def endm():
    M = E.METHOD
    return f'''<footer class="endm" id="end"><div class="wide">
<h2 class="fade">卷末 · 参考、方法与署名</h2>
<p class="small fade">都折叠着，点开看。</p>
<details class="fold big fade"><summary><h3>参考（按研究路分组）</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{''.join(f'<li>{esc(p)}</li>' for p in M['process'])}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{''.join(f'<li>{esc(t)}</li>' for t in M['todo'])}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(IM)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">一周一题 · 第 {E.META['no']} 题 · {E.META['date']}<br>研究、绘图与核查：Claude（站长复核）</div>
</div></footer>
<button class="theme-btn" id="theme-btn" type="button" data-cover-hide aria-label="切换深浅色">夜 / 昼</button>'''

# ---------- 数据
def data():
    field = []
    for r in E.COMPARE:
        f = FEST[r['id']]
        if f['doy'] < 274: continue
        field.append(dict(id=r['id'], node=r['id'], name=f['short'] + ('（' + f['city'] + '）' if r['id'] == 'halloween' else ''), city=f['city'], lat=f['lat'], date=f['date'], rule=f['rule'][:40]))
    field.append(dict(id='thanksgiving', node='martinmas', name='感恩节', city='华盛顿', lat=38.9, date='2026-11-26', rule='11 月第四个周四'))
    cities = {cid: dict(name_zh=c['name_zh'], lat=c['lat'], lon=c['lon'], koppen=c.get('koppen', ''), tz=c['tz']) for cid, c in CITIES.items()}
    return {'field': field, 'stage': stage.data(STAGE_CITIES), 'cities': cities, 'fest': FEST, 'order': ORDER, 'tables': TABLES, 'lunar': LUNAR, 'watch': E.WATCH}

LIGHT = ('--bg:#ECEDF0;--surface:#F7F7F9;--surface-2:#E2E4EA;--ink:#1C2030;--ink-2:#48506A;--muted:#7A8094;--line:#C9CDD8;--line-2:#DCDFE7;--grid:rgba(28,32,48,.06);'
         '--accent:#D9661F;--accent-2:#F2A33A;--accent-ink:#B4511A;--wash:rgba(217,102,31,.10);--wash-2:rgba(217,102,31,.2);color-scheme:light;')

def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'calendars.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'demos.js'), encoding='utf-8').read()
    light = ('@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){' + LIGHT + '}}\n:root[data-theme="light"]{' + LIGHT + '}')
    body = hero() + cnav() + '<main>' + ch_days() + ch_now() + ch_threshold() + ch_compare() + ch_three() + ch_walls() + ch_tools() + ch_rules() + '</main>' + endm()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E.META['desc'])).replace('{{LIGHT_BLOCKS}}', light)
            .replace('{{BODY}}', body).replace('{{DATA_JSON}}', json.dumps(data(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('{{APP_JS}}', app))
    page, report = fixes.apply(page)
    for line in report: print(line)
    open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(page)
    meta = {'no': E.META['no'], 'slug': E.META['slug'], 'title': E.META['title'], 'subtitle': E.META['subtitle'], 'date': E.META['date'], 'summary': E.META['desc'],
            'tags': E.META['tags'], 'format': E.META['format'], 'cover': 'cover.png', 'cover_focus': E.META['cover_focus'], 'cover_scheme': E.META['cover_scheme'], 'reading_time': E.META['reading_time'],
            'sources': ['原典与专著：《诗经·七月》《礼记·月令》《史记·秦始皇本纪》《汉书·律历志》《东京梦华录》《帝京景物略》、Tochmarc Emire（CELT）、Hutton《Stations of the Sun》、Brandes、Fernández Juárez 2006、萨阿贡 / 托瓦尔手抄本（LoC）',
                        '官方与数据：印度中央政府假日备忘录 2015–2027、印度气象局季风常年日期、泰国政府门户与旅游局、墨西哥城政府、UNESCO 非遗名录（2008、2016）、国立天文台暦要項、香港天文台历表、北京市气象台、国家气候中心、FAO GIEWS、Beck 等 2018 柯本数据集、NRF、ARA / Roy Morgan',
                        '算法：立冬 / 小雪 / 冬至按太阳视黄经（PyEphem）；排灯节按 amanta 历朔日与德里日落 tithi（与官方表 2015–2027 全部一致）；农历按 GB/T 33661-2017 月表；昼长按太阳赤纬标准近似',
                        f'图片 {len(IM)} 张：纽约公共图书馆、美国国会图书馆、大都会与克利夫兰艺术博物馆 Open Access、Rijksmuseum、Wellcome、Europeana 合作馆（斯德哥尔摩民族学博物馆、哥德堡世界文化博物馆等）、geograph、NASA、pxhere / WordPress CC0 图库；逐张署名见页面卷末与 src/images.json']}
    json.dump(meta, open(os.path.join(HERE, '..', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote index.html', len(page), 'bytes')

if __name__ == '__main__':
    main()
