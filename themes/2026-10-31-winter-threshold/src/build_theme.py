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
for i in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8')):
    if i.get('status', 'ok').startswith('rejected'): continue  # 许可不合（如 CC BY-NC-ND）的图留档不用：引用它会在下面报错
    IM[i['id']] = i
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
# v4：三类——祭亡灵（dead）/ 只点灯（light）/ 不祭亡灵也不点灯（none）；按 TILES 两格的有无归类
def cat_of(nid):
    t = E.TILES.get(nid)
    if not t: return 'none'
    if not t['dead'][2]: return 'dead'
    if not t['light'][2]: return 'light'
    return 'none'
CAT = {i: cat_of(i) for i in E.TILES}
CAT_NAME = dict(E.CAT_GROUPS)

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
                img=im['file'] if im else None, contrast=nid in E.CONTRAST, cat=CAT.get(nid, 'none'))
FEST = {nid: fest_record(nid) for nid in NODES}
ORDER = [r['id'] for r in E.COMPARE]

# ---------- 小工具
OPEN, CLOSE = '（(「『【[《', '）)」』】]》'
def brief(t, n=72):
    """取开头几句，到 n 个字左右为止：只在括号、引号之外的「。；」处断开；剩下的放进折叠。"""
    t = str(t or '').strip()
    if len(t) <= n: return t
    parts, cur, depth = [], '', 0
    for ch in t:
        cur += ch
        if ch in OPEN: depth += 1
        elif ch in CLOSE: depth = max(0, depth - 1)
        elif ch in '。；' and depth == 0: parts.append(cur); cur = ''
    if cur: parts.append(cur)
    out = ''
    for p in parts:
        if out and len(out + p) > n: break
        out += p
    return out.rstrip('；') + ('……' if len(out) < len(t) else '')
def fact(nid, key, field, n):
    """灯谱行里的短事实：编辑手写的（editorial.FACTS）优先，否则取底稿原文的开头几句。"""
    v = (E.FACTS.get(nid) or {}).get(key)
    return v if v else brief(NODES[nid].get(field, ''), n)
def latlabel(lat): return ('北纬 ' if lat >= 0 else '南纬 ') + f'{abs(lat):.1f}°'
WDN = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
def wdz(iso): y, m, d = (int(x) for x in iso.split('-')); return WDN[dt.date(y, m, d).weekday()]
def capspan(im, n=80):
    """图注分两段：说明可以截短，署名（作者 + 许可）永远完整显示。"""
    s = im['subject']; s = s[:n] + '…' if len(s) > n else s
    return f'<span class="cs">{esc(s)}</span><span class="cr">图：{esc(im["author_short"])}，{esc(im["license_short"])}。</span>'

# ---------- 卷首（v4，风格 A「引路」）：紫夜底，左字右图；一条万寿菊花瓣路（app.js 按实际位置画）从左下角引到照片
def hero():
    H = E.HERO4; im = IM[H['img']]
    arrow = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5"/></svg>'
    return f'''<header class="h4 band" id="top">
  <svg class="h4path" id="h4path" aria-hidden="true"><path class="pp" d=""/><g class="pl"></g></svg>
  <div class="h4in wide">
    <div class="h4txt">
      <p class="h3k rise">{esc(H['kicker'])}</p>
      <h1 class="h4t rise">{esc(H['title'])}</h1>
      <p class="h4s rise">{esc(H['sub'])}</p>
      <p class="h4th rise">{esc(H['thesis'])}</p>
      <div class="h3a rise"><a class="btn" href="{esc(H['cta_href'])}">{esc(H['cta'])}{arrow}</a><span class="h3p">{esc(H['proof'])}</span></div>
    </div>
    <figure class="h4fig rise" id="h4fig"><img src="assets/{esc(im['file'])}" alt="{esc(H['alt'])}" width="{im['width']}" height="{im['height']}" fetchpriority="high" decoding="async"><figcaption><span class="cs">{esc(H['cap'])}</span><span class="cr">图：{esc(im['author_short'])}，{esc(im['license_short'])}。</span></figcaption></figure>
  </div>
</header>'''

def tagline_sec():
    lines = []
    k = 0
    for ln in E.TAGLINE.split('/'):
        ws = []
        for w in ln.split('|'):
            hl = w.startswith('*'); w = w.lstrip('*')
            ws.append(f'<span class="w{" k" if hl else ""}" style="--i:{k}">{esc(w)}</span>'); k += 1
        lines.append('<span class="ln">' + ''.join(ws) + '</span>')
    return f'''<section class="tagsec band" id="tagsec" aria-label="这一页的论点"><div class="tagstick"><div class="wide">
<p class="tagl" aria-label="{esc(E.TAGLINE.replace('|', '').replace('/', '').replace('*', ''))}"><span aria-hidden="true">{''.join(lines)}</span></p>
<p class="tagrest">{esc(E.TAGREST)}</p>
</div></div></section>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n}</small>{esc(t)}</a>' for cid, n, t, _ in E.CHAPTERS)
    links += '<a href="#end" data-nav="end"><small>末</small>规则与参考</a>'
    links += '<button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="切换深浅色">白天读</button>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第{"一二三四五六七八"[n-1]}章'
    txt = f'<div class="ptext"><p class="cno">{n:02d} · {label}</p><h2>{esc(t)}</h2><p class="lede">{lede}</p></div>'
    O = E.OPENERS.get(cid)
    if not O:
        return f'<header class="chead fade">{txt}</header>'
    im = IM[O['img']]
    srcset = (f' srcset="assets/{esc(O["small"])} 1280w, assets/{esc(im["file"])} {O["w"]}w" sizes="(min-width: 981px) 58vw, 100vw"' if O['small'] != im['file'] else '')
    fig = (f'<figure class="pimg{" pano" if O.get("wide") else ""}{" film" if O.get("film") else ""}"><img src="assets/{esc(im["file"])}"{srcset} width="{im["width"]}" height="{im["height"]}" '
           f'alt="{esc(O["alt"])}" loading="lazy" decoding="async"><figcaption>{esc(O["cap"])}</figcaption></figure>')
    return f'<header class="chead plate fade">{txt}{fig}</header>'

# ---------- 序章：全屏时间轴
def ch_days():
    return f'<section class="chap tl band" id="days" aria-label="序章 · 这十天">{stage.stage(STAGE_CITIES, "assets/earth-night-1920.jpg", IM, FEST)}</section>'

# ---------- 灯谱：透镜分组
KIND_ORDER = ['harvest', 'monsoon', 'night', 'solar', 'calendar', 'event', 'sowing', 'religion', 'none']
SPREAD_ORDER = ['native', 'church-calendar', 'migration', 'commercial', 'transplant']
def lens_groups():
    rows = [FEST[i] for i in ORDER]
    bydoy = lambda ids: sorted(ids, key=lambda i: (FEST[i]['doy'], -FEST[i]['lat']))
    out = {}
    out['who'] = [dict(k='c-' + k, label=l + f'（{sum(1 for f in rows if f["cat"] == k)}）', ids=bydoy([f['id'] for f in rows if f['cat'] == k])) for k, l in E.CAT_GROUPS]
    g = [('before', '这十天之前', [f['id'] for f in rows if f['doy'] < 304]), ('ten', '这十天 · 10/31–11/9 · 七个节日', [f['id'] for f in rows if 304 <= f['doy'] <= 313]), ('after', '这十天之后', [f['id'] for f in rows if f['doy'] > 313])]
    out['date'] = [dict(k=k, label=l, ids=bydoy(ids)) for k, l, ids in g if ids]
    def latk(lat): return 'n50' if lat >= 50 else 'n30' if lat >= 30 else 'n0' if lat >= 0 else 's'
    LATL = [('n50', '北纬 50° 以北'), ('n30', '北纬 30°–50°'), ('n0', '北纬 0°–30°'), ('s', '南半球')]
    out['lat'] = [dict(k=k, label=l, ids=sorted([f['id'] for f in rows if latk(f['lat']) == k], key=lambda i: -FEST[i]['lat'])) for k, l in LATL]
    out['kind'] = [dict(k=k, label=E.KIND_NAME[k] + ('（另一道门槛）' if k == 'religion' else ''), ids=bydoy([f['id'] for f in rows if f['kind'] == k])) for k in KIND_ORDER]
    bk = {}
    for f in rows: bk.setdefault(f['basisName'], []).append(f['id'])
    out['basis'] = [dict(k=k, label=k + ' · ' + '、'.join(dict.fromkeys(FEST[i]['basisSub'] for i in ids if FEST[i]['basisSub'])), ids=bydoy(ids)) for k, ids in sorted(bk.items(), key=lambda kv: ['固定日', '跟月亮', '跟太阳', '按规则'].index(kv[0]) if kv[0] in ['固定日', '跟月亮', '跟太阳', '按规则'] else 9)]
    out['spread'] = [dict(k=k, label=E.SPREAD_NAME.get(k, k), ids=bydoy([f['id'] for f in rows if f['spread'] == k])) for k in SPREAD_ORDER]
    for k in out: out[k] = [x for x in out[k] if x['ids']]
    return out
LENS = lens_groups()
GROUP_OF = {lens: {i: g['k'] for g in groups for i in g['ids']} for lens, groups in LENS.items()}

def light_tile(nid):
    """引路一章的行内展开只放「这盏灯」一格；「吃一顿」「祭亡灵」两格分别排进款待、记得两章。"""
    txt, img, none = E.TILES[nid]['light']; im = IM.get(img) if img else None
    if img and not im: raise SystemExit(f'TILES {nid}.light: 图片 {img} 不在 images.json')
    fig = f'<figure><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{capspan(im, 56)}</figcaption></figure>' if im else ''
    c = FEST[nid]['cat']
    links = (f'<a class="l1go" href="#f-{esc(nid)}">款待 →</a>' + (f'<a class="l1go" href="#r-{esc(nid)}">记得 →</a>' if c == 'dead' else ''))
    return (f'<div class="l1"><div class="l1t{" none" if none else ""}{" ph" if im else ""}"><b>这盏灯</b>{fig}<p>{esc(txt)}</p></div>'
            f'<p class="l1who"><span class="l1c"><i class="cd {c}"></i>{esc(CAT_NAME[c])}</span><span class="l1links">{links}</span></p></div>')

def spread_line(nid):
    """「传播」一栏：标签 · 正文；正文若以标签开头的短句起头（如「本土节日。」「宗教日历：」），去掉这段重复。"""
    lab = FEST[nid]['spreadName']; t = fact(nid, 'spread', 'spread_text', 70)
    for sep in '。：':
        head, _, rest = t.partition(sep)
        if rest and head.startswith(lab) and len(head) <= 16: t = rest; break
    return f'{lab} · {t}'

def lamp_row(nid):
    n = NODES[nid]; f = FEST[nid]; im = IM.get(E.NODE_IMG.get(nid) or '')
    lat = f['lat']; pct = (lat + 40) / 100 * 100; dl = f['dl']
    thumb = f'<span class="lthumb"><img src="assets/{esc(im["file"])}" alt="" loading="lazy"></span>' if im else f'<span class="lthumb none"><i class="lamp {f["cat"]}"></i></span>'
    watch = E.WATCH.get(nid)
    wblk = (f'<div class="lwatch"><h4>去看的话</h4><dl><dt>日期</dt><dd>{esc(watch["when"])}</dd><dt>必看</dt><dd>{esc(watch["see"])}</dd><dt>必吃</dt><dd>{esc(watch["eat"])}</dd><dt>礼仪</dt><dd>{esc(watch["mind"])}</dd></dl></div>') if watch else ''
    o = n.get('origin') or {}; c = n.get('city') or {}; cl = c.get('climate') or {}
    tl = ''.join(f'<li><i>{esc(t.get("year_label") or t.get("year"))}</i><div>{esc(t.get("label", ""))}{("：" + esc(t["text"])) if t.get("text") else ""}</div></li>' for t in (n.get('timeline') or [])[:10])
    nums = ''.join(f'<div><span>{esc(x["label"])}</span><b>{esc(x["value"])}{(" " + esc(x["unit"])) if x.get("unit") else ""}</b></div>' for x in (n.get('numbers') or [])[:6])
    clim = ''.join(f'<dt>{k}</dt><dd>{esc(v)}</dd>' for k, v in (('这一天', cl.get('season')), ('收成', cl.get('harvest')), ('雨季 / 季风', cl.get('rain')), ('霜', cl.get('frost'))) if v)
    disp = f'<p class="dispute"><b>两说</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    wasny = n.get('was_new_year') or ''
    ny = ('<dt>岁首</dt><dd>' + esc(fact(nid, 'ny', 'was_new_year', 80)) + '</dd>') if wasny and not wasny.startswith('否') else ''
    attrs = ' '.join(f'data-g-{lens}="{GROUP_OF[lens].get(nid, "")}"' for lens in LENS)
    ten = 304 <= f['doy'] <= 313
    return f'''<article class="lrow{" ct" if f["contrast"] else ""}{" ten" if ten else ""}" id="n-{esc(nid)}" data-id="{esc(nid)}" {attrs}>
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(nid)}">
<span class="ldate"><b>{esc(f["date"][5:].replace("-", "/"))}</b><small>{wdz(f["date"])}</small></span>
<span class="lname"><b><i class="lamp {f["cat"]}{"" if ten else " dim"}"></i>{esc(f["short"])}</b><small>{esc(f["city"])} · {latlabel(lat)} · {esc(f["koppen"])}</small></span>
<span class="llat" title="纬度：南纬 40° → 北纬 60°"><u></u><i style="left:{pct:.1f}%"></i></span>
<span class="ldl" title="当天昼长"><span class="bar"><i style="width:{dl / 24 * 100:.1f}%"></i><u></u></span><small>{sun.hm(dl)}</small></span>
<span class="ltags"><span>{esc(f["basisName"])}</span><span class="lk">{esc(f["kindName"])}</span>{'<span class="lct">对照</span>' if f["contrast"] else ''}</span>
{thumb}<span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(nid)}" role="region" aria-label="{esc(f['short'])} 详情"><div class="lmore-in">
<p class="lwhy">{esc(n.get('why', ''))}</p>
<dl class="lfacts"><dt>怎么定日</dt><dd>{esc(fact(nid, 'rule', 'date_rule', 80))}</dd><dt>压在哪道门槛上</dt><dd>{esc(fact(nid, 'threshold', 'threshold', 90))}</dd>{ny}<dt>传播</dt><dd>{esc(spread_line(nid))}</dd></dl>
{light_tile(nid)}{wblk}
<details class="fold"><summary>全文：来历、定日规则、气候口径、时间轴、数字、两说与来源 {conf(n.get('confidence'))}</summary>
<p><b>{esc(o.get('year_label', ''))}</b> {esc(o.get('text', ''))}</p><p>{esc(n.get('text', ''))}</p>
<dl class="lfacts"><dt>怎么定日</dt><dd>{esc(n.get('date_rule', ''))}</dd><dt>压在哪道门槛上</dt><dd>{esc(n.get('threshold', ''))}</dd>{('<dt>岁首</dt><dd>' + esc(wasny) + '</dd>') if wasny else ''}<dt>传播</dt><dd>{esc(n.get('spread_text', ''))}</dd>{clim}</dl>
{('<ol class="tl">' + tl + '</ol>') if tl else ''}{('<div class="nnums">' + nums + '</div>') if nums else ''}{disp}{srcs(n.get('sources'), n=8)}</details>
</div></div></article>'''

def ch_lamps():
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == "who" else "false"}">{esc(t)}</button>' for k, t in E.LENSES)
    body = ''
    for g in LENS['who']:
        body += f'<div class="lgh" data-g="{g["k"]}"><b>{esc(g["label"])}</b><small>{len(g["ids"])} 行</small></div>' + ''.join(lamp_row(i) for i in g['ids'])
    return f'''<section class="chap" id="lamps"><div class="wide">{chead("lamps")}
<div class="lensbar fade"><span class="lensk">按</span><div class="lens" id="lens" role="tablist" aria-label="灯谱的透镜">{tabs}</div><span class="lensnote" id="lensnote">按为谁点灯分成 3 组 · 点一行展开</span></div>
<div class="lcols" aria-hidden="true"><span>日期</span><span>节日 · 核心城市</span><span>纬度 南 40° → 北 60°</span><span>当天昼长</span><span>历法 · 门槛</span></div>
<div class="lgrid" id="lgrid">{body}</div>
<p class="small lfoot">灯的样子：实心的万寿菊色祭亡灵，淡金圈只点灯，灰圈两样都没有；落在这十天里的灯带一圈光。昼长按核心城市纬度与 2026 年日期算；柯本类型按 Beck 等 2018 的 1 km 数据逐城读取；「门槛」是编辑按各路气象与农业口径归的类。标着「对照」的三行是对照：悉尼的万圣节在仲春，中元与 Pchum Ben 在另一道门槛上。</p>
</div></section>'''

# ---------- 款待：一桌饭（各行「吃一顿」一格）
BYDOY = sorted(ORDER, key=lambda i: (FEST[i]['doy'], -FEST[i]['lat']))
def _when(f):
    return f'<span class="ccd">{esc(f["date"][5:].replace("-", "/"))}</span><span class="ccc">{esc(f["city"])}</span>'
def _dish(nid):
    """款待：一桌饭像一张菜单——灯 + 节日名，一行花瓣点引到日期与城市，下面一句桌上摆什么。"""
    f = FEST[nid]; txt, _img, none = E.TILES[nid]['food']
    return (f'<article class="dish {f["cat"]}{" empty" if none else ""}" id="f-{esc(nid)}"><div class="drow">'
            f'<h3 class="dnm"><i class="cd {f["cat"]}"></i>{esc(f["short"])}</h3><span class="dlead" aria-hidden="true"></span><p class="dwhen">{_when(f)}</p></div>'
            f'<p class="dtx">{esc(txt)}</p><button type="button" class="cgo" data-open="{esc(nid)}">看这一行的来历 →</button></article>')

def ch_feast():
    dead = [i for i in BYDOY if CAT[i] == 'dead']; rest = [i for i in BYDOY if CAT[i] != 'dead']
    return f'''<section class="chap" id="feast"><div class="wide">{chead("feast")}
<div class="cgroup fade"><h3 class="cgh"><i class="cd dead"></i>祭亡灵的 {len(dead)} 个：供给亡者的，和活人吃的</h3><div class="menu">{''.join(_dish(i) for i in dead)}</div></div>
<div class="cgroup fade"><h3 class="cgh"><i class="cd light"></i>其余 {len(rest)} 个：活人吃的</h3><div class="menu">{''.join(_dish(i) for i in rest)}</div></div>
</div></section>'''

# ---------- 记得：名牌墙（八个祭亡灵的节日，各行「祭亡灵」一格）
def _name(nid):
    """记得：一块名牌——上沿一行花瓣点，节日名最大，日期与城市，下面一句怎么记。"""
    f = FEST[nid]; txt = E.TILES[nid]['dead'][0]
    return (f'<article class="ntile" id="r-{esc(nid)}"><p class="nwhen">{_when(f)}</p><h3 class="nnm">{esc(f["short"])}</h3>'
            f'<p class="ntx">{esc(txt)}</p><button type="button" class="cgo" data-open="{esc(nid)}">看这一行的来历 →</button></article>')

def ch_remember():
    dead = [i for i in BYDOY if CAT[i] == 'dead']
    winter = [i for i in dead if 298 <= FEST[i]['doy'] <= 331]; other = [i for i in dead if i not in winter]
    return f'''<section class="chap" id="remember"><div class="wide">{chead("remember")}
<div class="cgroup fade"><h3 class="cgh"><i class="cd dead"></i>冬初这几周（{len(winter)} 个）</h3><div class="names">{''.join(_name(i) for i in winter)}</div></div>
<div class="cgroup fade"><h3 class="cgh"><i class="cd dead"></i>另一道门槛：夏末与雨季（{len(other)} 个）</h3><div class="names">{''.join(_name(i) for i in other)}</div></div>
</div></section>'''

# ---------- 为什么是这时候：田野 + 年轮 + 同与异
def ch_threshold():
    items = [dict(id=i, name=FEST[i]['short'], date=FEST[i]['date'], basis=FEST[i]['basis'], lane=FEST[i]['lane'], cat=FEST[i]['cat']) for i in ORDER]
    wheel = figs.wheel_svg(items, size=520, center=('年轮', '顶上 = 公历 1/1'), anchors=E.ANCHORS)
    anc = ''.join(f'<button type="button" data-k="{k}" title="{esc(desc)}" aria-pressed="{"true" if k == 0 else "false"}">{esc(short)}</button>' for k, (short, desc, _d) in enumerate(E.ANCHORS))
    SAME_ORDER = ['亡灵', '灯火', '吃一顿', '门槛', '长夜']; ACT = {'亡灵': 'rem', '灯火': 'lit', '吃一顿': 'fst'}
    same_rows = sorted(E.SAME, key=lambda r: SAME_ORDER.index(r[0]) if r[0] in SAME_ORDER else 9)
    same = ''.join(f'<li><b>{esc(k)}</b><span class="waf {ACT.get(k, "")}" aria-label="十九行里 {n} 行">' + ''.join('<i' + (' class="f"' if j < n else '') + '></i>' for j in range(19)) + f'<em>{n} / 19</em></span><span class="sdt">{esc(v)}</span></li>' for k, n, v in same_rows)
    F = E.FIELD3
    field = f'''<div class="fieldwrap band"><div class="fhead fade"><h3>{esc(F['title'])}</h3><p>{esc(F['lede'])}</p></div>
  <figure class="field fade" id="field"><div class="fieldbox" id="fieldbox" tabindex="0" role="slider" aria-label="夜的田野：拖动竖线选日期" aria-valuemin="274" aria-valuemax="365" aria-valuenow="304" aria-valuetext="10 月 31 日">
    <canvas id="fcv" width="1200" height="520" aria-hidden="true"></canvas><svg class="fov" id="fov" viewBox="0 0 1200 520" preserveAspectRatio="none" aria-hidden="true"></svg>
    <div class="fread glass" id="fread" aria-live="polite" data-cover-hide></div><div class="ftip" id="ftip"></div></div>
    <figcaption class="fcap"><span>横轴 10 月 1 日 → 12 月 31 日，纵轴北纬 62° → 南纬 36°，白线是等昼长线。每盏灯是灯谱里的一行，放在它 2026 年的日子与核心城市的纬度上：实心的万寿菊色祭亡灵，淡金圈只点灯，灰圈两样都没有；点一下打开那一行。虚线圈的感恩节只作参照，8 月的中元在横轴以外。</span></figcaption></figure></div>'''
    diff = ''.join(f'<li><b>{esc(k)}</b><span class="sdt">{esc(v)}</span><span class="ev">' + ''.join(f'<button type="button" class="evb" data-open="{esc(i)}" data-lens="{esc(lens)}">{esc(FEST[i]["short"])}</button>' for i in ids) + f'<button type="button" class="evb all" data-lens="{esc(lens)}">按{esc(dict(E.LENSES)[lens])}看灯谱 →</button></span></li>' for k, v, ids, lens in E.DIFF)
    return f'''<section class="chap" id="threshold"><div class="wide">{chead("threshold")}
{field}
<div class="thwrap"><div class="wheelcol fade">
<div class="wheelbox" id="wheelbox" role="slider" tabindex="0" aria-label="年轮：拖动旋转，方向键切换岁首" aria-valuetext="顶上 = 公历 1/1">{wheel}</div>
<div class="anchors" id="anchors" role="group" aria-label="把谁的岁首转到顶上"><span>岁首</span>{anc}</div>
<p class="small">拖住年轮转一转，松手会停在最近的岁首；点一个节日打开它在灯谱里的那一行。底色是两道门槛：夏末（7 月下旬–9 月中）与冬初（10 月下旬–11 月下旬）；虚线圈 = 跟月亮走，实线圈 = 公历固定日与节气（立冬）；圈上的短刻线是各家的岁首，顶上的小三角指着当前的岁首。</p>
</div><div class="sdcol">
<div class="sdcard fade"><h3>同：五条</h3><ol>{same}</ol></div>
<div class="sdcard diff fade"><h3>异：四根轴</h3><ol>{diff}</ol></div>
</div></div></div></section>'''

# ---------- 动手
def ch_hands():
    W = E.WALLS[0]; T = E.TOOLS[0]
    return f'''<section class="chap" id="hands"><div class="wide">{chead("hands")}<div class="hands">
<article class="wall fade" id="wall-lat"><div class="hd"><b>{esc(W["title"])}</b><span class="f">{esc(W["formula"])}</span></div>{demos.wall_lat()}<details class="fold"><summary>这面墙是怎么算的</summary><p>{esc(W["text"])}</p></details></article>
<div class="tool fade" id="tool-dates"><div class="hd"><b>{esc(T["title"])}</b><p>{esc(T["lede"])}</p></div>{demos.tool_dates()}</div>
</div></div></section>'''

# ---------- 卷末：规则文件 + 折叠
def find_src(nid, pat):
    pool = Dd['cities'][0].get('koppen_source') and [Dd['cities'][0]['koppen_source']] if nid == 'cities' else NODES.get(nid, {}).get('sources', [])
    for s in pool or []:
        if isinstance(s, dict) and re.search(pat, (s.get('title') or '') + ' ' + (s.get('url') or ''), re.I): return s
    return None
def rules_block():
    li = ''
    for k, (y, t, d, (nid, pat)) in enumerate(E.RULES):
        s_ = find_src(nid, pat)
        li += (f'<article class="ritem fade"><span class="ry">{esc(y)}</span><div><b>{esc(t)}</b><p>{esc(d)}</p>'
               + (f'<a class="rgo" href="{esc(s_["url"])}" target="_blank" rel="noopener">原文 / 入口 ↗</a>' if s_ and s_.get('url') else '') + '</div></article>')
    return f'<div class="rlist">{li}</div>'
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
USED = []  # 页面上实际出现的图（main() 在拼卷末之前算出）；署名表只列这些
def credits():
    rows = ''.join(f'<tr><td>{esc(k)}</td><td>{esc(im["subject"])}</td><td>{esc(im["author_short"])}，{esc(im.get("year", ""))}</td><td>{(f'<a href="{esc(im["license_url"])}" target="_blank" rel="noopener">{esc(im["license_short"])}</a>' if im.get('license_url') else esc(im['license_short']))}</td><td><a href="{esc(im["url_page"])}" target="_blank" rel="noopener">{esc(im["source_name"])}</a></td></tr>' for k, im in ((k, IM[k]) for k in USED))
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>作者 / 年代</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'
def endm():
    M = E.METHOD
    return f'''<footer class="endm" id="end"><div class="wide">
<h2 class="fade">卷末 · 规则、参考与署名</h2>
<h3 class="endh fade">规则是怎么写的<small>页面上的日子和数字从哪来：十一份文件</small></h3>
{rules_block()}
<details class="fold big fade"><summary><h3>参考（按研究路分组）</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{''.join(f'<li>{esc(p)}</li>' for p in M['process'])}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{''.join(f'<li>{esc(t)}</li>' for t in M['todo'])}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(USED)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">一周一题 · 第 {E.META['no']} 题 · {E.META['date']}<br>研究、绘图与核查：Claude（站长复核）</div>
</div></footer>
'''

# ---------- 数据
def data():
    field = []
    for r in E.COMPARE:
        f = FEST[r['id']]
        if f['doy'] < 274: continue
        field.append(dict(id=r['id'], node=r['id'], name=f['short'] + ('（' + f['city'] + '）' if r['id'] == 'halloween' else ''), city=f['city'], lat=f['lat'], date=f['date'], rule=E.RULE_SHORT.get(r['id']) or brief(f['rule'], 40), cat=f['cat']))
    field.append(dict(id='thanksgiving', node='', name='感恩节', city='华盛顿', lat=38.9, date='2026-11-26', rule='11 月第四个周四', cat='ref'))
    cities = {cid: dict(name_zh=c['name_zh'], lat=c['lat'], lon=c['lon'], koppen=c.get('koppen', ''), tz=c['tz']) for cid, c in CITIES.items()}
    fest = {i: {k: FEST[i][k] for k in ('id', 'short', 'name', 'city', 'lat', 'date', 'doy', 'dl', 'koppen', 'season', 'kindName', 'basisName', 'cat')} for i in ORDER}
    lens = {k: [dict(k=g['k'], label=g['label'], ids=g['ids']) for g in v] for k, v in LENS.items()}
    anchors = [dict(short=a, desc=b, doy=d) for a, b, d in E.ANCHORS]
    return {'field': field, 'stage': stage.data(STAGE_CITIES, IM, FEST), 'cities': cities, 'fest': fest, 'order': ORDER, 'lens': lens, 'lensName': dict(E.LENSES), 'anchors': anchors, 'tables': TABLES, 'lunar': LUNAR}

LIGHT = ('--bg:#FBF4EA;--surface:#FFFAF2;--surface-2:#F2E6D4;--ink:#23182F;--ink-2:#4A3D5A;--muted:#6B5D7B;--line:rgba(35,24,47,.16);--line-2:rgba(35,24,47,.09);--grid:rgba(35,24,47,.05);'
         '--accent:#A34C05;--accent-2:#C2650F;--accent-ink:#A34C05;--wash:rgba(163,76,5,.08);--wash-2:rgba(163,76,5,.16);--nav-glass:rgba(251,244,234,.8);--glass-line:rgba(35,24,47,.12);'
         '--c-dead:#B4560A;--c-light:#8C6400;--c-none:#9A8FA8;--act-lit:#CF630D;--act-fst:#2D8AB8;--act-rem:#942E79;--magenta:#B42A63;--glow-d:rgba(180,86,10,.28);--glow-l:rgba(140,100,0,0);color-scheme:light;')

def audit():
    """文案里的计数与数据对账：同的五个数、门槛透镜、年轮冬初段、这十天的行数、长夜。对不上就报出来（不拦构建）。"""
    same = {k: n for k, n, _ in E.SAME}; ids = ORDER; out = []
    for col, key in (('dead', '亡灵'), ('light', '灯火'), ('food', '吃一顿')):
        n = sum(1 for i in ids if not E.TILES[i][col][2]); out.append((key, n, same[key]))
    out.append(('门槛', sum(1 for i in ids if FEST[i]['kind'] not in ('none', 'religion', 'sowing')), same['门槛']))
    north = [i for i in ids if FEST[i]['lat'] >= 50]
    out.append(('长夜', sum(1 for i in north if FEST[i]['dl'] < 10), same['长夜']))
    out.append(('长夜·南边跌破 10 小时的只有下元', [i for i in ids if FEST[i]['lat'] < 50 and FEST[i]['dl'] < 10], ['xiayuan']))
    out.append(('年轮冬初段 16 行', sum(1 for i in ids if 298 <= FEST[i]['doy'] <= 331), 16))
    out.append(('这十天 11 行', sum(1 for i in ids if 304 <= FEST[i]['doy'] <= 313), 11))
    out.append(('十九行', len(ids), 19))
    out.append(('三类：祭亡灵 / 只点灯 / 都没有', [sum(1 for i in ids if CAT[i] == k) for k in ('dead', 'light', 'none')], [8, 8, 3]))
    out.append(('祭亡灵里落在冬初的', sum(1 for i in ids if CAT[i] == 'dead' and 298 <= FEST[i]['doy'] <= 331), 6))
    bad = [x for x in out if x[1] != x[2]]
    for k, got, want in out: print(f'{"ok  " if got == want else "DIFF"} audit {k}: {got} / 文案 {want}')
    return bad

def main():
    audit()
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'calendars.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'demos.js'), encoding='utf-8').read()
    light = ('@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){' + LIGHT + '}}\n:root[data-theme="light"]{' + LIGHT + '}')
    pre = hero() + cnav() + '<main>' + tagline_sec() + ch_days() + ch_lamps() + ch_feast() + ch_remember() + ch_threshold() + ch_hands() + '</main>'
    dj = json.dumps(data(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    seen = pre + dj  # 舞台底图用的是 earth-night-1 的 1920 宽副本
    USED[:] = [k for k, im in IM.items() if ('assets/' + im['file']) in seen or (k == 'img-earth-night-1' and 'assets/earth-night-1920.jpg' in seen)]
    print('images used', len(USED), '/', len(IM))
    body = pre + endm()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E.META['desc'])).replace('{{LIGHT_BLOCKS}}', light)
            .replace('{{BODY}}', body).replace('{{DATA_JSON}}', dj).replace('{{APP_JS}}', app))
    page, report = fixes.apply(page)
    for line in report: print(line)
    open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(page)
    meta = {'no': E.META['no'], 'slug': E.META['slug'], 'title': E.META['title'], 'subtitle': E.META['subtitle'], 'date': E.META['date'], 'summary': E.META['desc'],
            'tags': E.META['tags'], 'format': E.META['format'], 'cover': 'cover.png', 'cover_focus': E.META['cover_focus'], 'cover_scheme': E.META['cover_scheme'], 'reading_time': E.META['reading_time'],
            'sources': ['原典与专著：《诗经·七月》《礼记·月令》《史记·秦始皇本纪》《汉书·律历志》《东京梦华录》《帝京景物略》、Tochmarc Emire（CELT）、Hutton《Stations of the Sun》、Brandes、Fernández Juárez 2006、萨阿贡 / 托瓦尔手抄本（LoC）',
                        '官方与数据：印度中央政府假日备忘录 2015–2027、印度气象局季风常年日期、泰国政府门户与旅游局、墨西哥城政府、UNESCO 非遗名录（2008、2016）、国立天文台暦要項、香港天文台历表、北京市气象台、国家气候中心、FAO GIEWS、Beck 等 2018 柯本数据集、NRF、ARA / Roy Morgan',
                        '算法：立冬 / 小雪 / 冬至按太阳视黄经（PyEphem）；排灯节按 amanta 历朔日与德里日落 tithi（与官方表 2015–2027 全部一致）；农历按 GB/T 33661-2017 月表；昼长按太阳赤纬标准近似',
                        f'图片 {len(USED)} 张：纽约公共图书馆、美国国会图书馆、大都会与克利夫兰艺术博物馆 Open Access、Rijksmuseum、Wellcome、Europeana 合作馆（斯德哥尔摩民族学博物馆、哥德堡世界文化博物馆等）、geograph、NASA、pxhere / WordPress CC0 图库；逐张署名见页面卷末与 src/images.json']}
    json.dump(meta, open(os.path.join(HERE, '..', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote index.html', len(page), 'bytes')

if __name__ == '__main__':
    main()
