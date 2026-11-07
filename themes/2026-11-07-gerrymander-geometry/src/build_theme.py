# -*- coding: utf-8 -*-
"""第 8 题「蝾螈的几何」构建脚本：research/*.json + editorial.py + stage.json → ../index.html + ../meta.json。
python3 build_theme.py"""
import json, os, re, html, datetime as dt, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import editorial as E, geo

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
def esc(s): return html.escape(str(s), quote=True)
def J(name): return json.load(open(os.path.join(HERE, 'research', name), encoding='utf-8'))
import fixes
def J2(path, key):
    t = open(path, encoding='utf-8').read()
    for item in fixes.POST:
        k, old, new = item[:3]; n = item[3] if len(item) > 3 else 1
        if k != key: continue
        c = t.count(old)
        if c != n: raise SystemExit(f'fixes.POST 命中 {c} 次（期望 {n}）：{old[:40]}')
        t = t.replace(old, new)
    return json.loads(t)
A = J2(os.path.join(HERE, 'research', 'timeline_A.json'), 'A'); B = J2(os.path.join(HERE, 'research', 'polities_B.json'), 'B'); C = J2(os.path.join(HERE, 'research', 'metrics_C.json'), 'C'); D = J('week_D.json')
IM = {i['id']: i for i in J2(os.path.join(HERE, 'images.json'), 'I')}
def _patch(obj, path, val):
    cur = obj
    for p in path[:-1]: cur = cur[p]
    cur[path[-1]] = val
for k, path, val in fixes.PATCH:
    root = {'A': {n['id']: n for n in A['nodes']}, 'B': {p['id']: p for p in B['polities']}}[k]
    _patch(root, path, val)
print('fixes:', len(fixes.POST), 'POST +', len(fixes.PATCH), 'PATCH 全部命中')
STAGE = json.load(open(os.path.join(HERE, 'stage.json'), encoding='utf-8'))
WORLD = json.load(open(os.path.join(os.path.dirname(OUT), '2026-10-10-nobel-machines', 'src', 'world.json'), encoding='utf-8'))
NODES = {n['id']: n for n in A['nodes']}
POLS = {p['id']: p for p in B['polities']}
METRICS = {m['id']: m for m in C['metrics']}
DS = {d['id']: d for d in C['datasets']}
CONF_CLS = {'高': 'h', '中': 'm', '低': 'l'}
USED_IMG = []

def conf(c): return f'<span class="conf {CONF_CLS.get(c, "m")}" title="资料置信度：高 = 一手官方或学术来源；中 = 可靠二手；低 = 通行说法">置信度 {esc(c or "中")}</span>'
def srcs(ss, n=8):
    if not ss: return ''
    items = []
    for s in ss[:n]:
        t = s.get('title') or s.get('url'); u = s.get('url', '')
        items.append(f'<a href="{esc(u)}" rel="noopener">{esc(t)}</a>' if u else esc(t))
    return '<p class="src">来源：' + '；'.join(items) + '</p>'
def img_tag(iid, alt='', cls='', lazy=True, w=None):
    im = IM[iid]; USED_IMG.append(iid) if iid not in USED_IMG else None
    return f'<img src="assets/{esc(im["file"])}" alt="{esc(alt or im["subject"])}" width="{im["width"]}" height="{im["height"]}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async">'
def credit(iid): im = IM[iid]; return f'<span class="cr">图：{esc(im["author_short"])}，{esc(im["license_short"])}。</span>'
def fmtnum(v):
    return f'{v:,}' if isinstance(v, int) and abs(v) >= 10000 else str(v)
def brief(s, n):
    """截到 n 字以内的最后一个「；」「，」「。」处，没有就硬截加「…」。"""
    s = str(s or '')
    if len(s) <= n: return s
    cut = s[:n]
    for sep in '；。，':
        i = cut.rfind(sep)
        if i >= n // 2: return cut[:i]
    return cut.rstrip('（(') + '…'
def clean(s):
    """清掉底稿里写给编辑看的话。"""
    s = str(s or '')
    s = re.sub(r'（text_long[^）]*）', '', s)
    s = re.sub(r'——待核[^，。；）]*', '', s)
    return s.strip()

# ---------- 卷首、论点、导航、章头
def hero():
    H = E.HERO; im = IM[H['img']]; USED_IMG.append(H['img'])
    arrow = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5"/></svg>'
    return f'''<header class="hero" id="top">
  <div class="wide">
    <div class="htxt">
      <p class="mast rise"><span>{esc(H['kicker'])}</span><span>tianjie.me</span></p>
      <h1 class="rise">{esc(H['title'])}</h1>
      <p class="hsub rise">{esc(H['sub'])}</p>
      <p class="hth rise">{esc(H['thesis'])}</p>
      <div class="hact rise"><a class="btn" href="{esc(H['cta_href'])}">{esc(H['cta'])}{arrow}</a><span class="hproof">{esc(H['proof'])}</span></div>
    </div>
    <figure class="hfig rise"><img src="assets/{esc(im['file'])}" alt="{esc(H['alt'])}" width="{im['width']}" height="{im['height']}" fetchpriority="high" decoding="async"><figcaption>{esc(H['cap'])}{credit(H['img'])}</figcaption></figure>
  </div>
</header>'''

def tagline_sec():
    lines = []; k = 0
    for ln in E.TAGLINE.split('/'):
        ws = []
        for w in ln.split('|'):
            hl = w.startswith('*'); w = w.lstrip('*')
            ws.append(f'<span class="w{" k" if hl else ""}" style="--i:{k}">{esc(w)}</span>'); k += 1
        lines.append('<span class="ln">' + ''.join(ws) + '</span>')
    plain = E.TAGLINE.replace('|', '').replace('/', '').replace('*', '')
    return f'''<section class="tagsec" id="tagsec" aria-label="这一页的论点"><div class="tagstick"><div class="wide">
<p class="tagl" aria-label="{esc(plain)}"><span aria-hidden="true">{''.join(lines)}</span></p>
<p class="tagrest">{esc(E.TAGREST)}</p>
</div></div></section>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n:02d}</small>{esc(t)}</a>' for cid, n, t, _ in E.CHAPTERS)
    links = links.replace('data-nav="history"', 'data-nav="history"', 1)
    links = links[:links.index('<a href="#history"')] + '<a href="#week" data-nav="week"><small>·</small>这一周</a>' + links[links.index('<a href="#history"'):]
    links += '<a href="#end" data-nav="end"><small>末</small>方法与参考</a>'
    links += '<button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="切换深浅色">夜里读</button>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第{"一二三四五六七八"[n-1]}章'
    txt = f'<div class="ptext"><p class="cno">{n:02d} · {label}</p><h2>{esc(t)}</h2><p class="lede">{esc(lede)}</p></div>'
    O = E.OPENERS.get(cid)
    if not O: return f'<header class="chead fade">{txt}</header>'
    fig = f'<figure class="pimg{" pano" if O.get("wide") else ""}{" film" if O.get("film") else ""}">{img_tag(O["img"], O["alt"])}<figcaption>{esc(O["cap"])}{credit(O["img"])}</figcaption></figure>'
    return f'<header class="chead plate fade">{txt}{fig}</header>'

# ---------- 序章：舞台
def ch_stage():
    ticks = ''.join(f'<span class="rtick" data-i="{i}" style="left:calc(var(--gut) + (100% - 2 * var(--gut)) * {i / (len(STEPS) - 1):.4f})"><i></i><b>{esc(s["name"])}</b></span>' for i, s in enumerate(STEPS))
    seats = ''.join('<i></i>' for _ in range(STAGE['K']))
    return f'''<section class="chap stage" id="stage" aria-label="序章 · 一张格子的五种画法">
<div class="stpin" id="stpin" style="--st-len:{len(E.STAGE_STEPS) * 100 + 60}vh">
<div class="ststage" id="ststage">
  <p class="stfoot">序章 · 一张格子的五种画法 · <span class="sw a"></span>甲 60 人 · <span class="sw b"></span>乙 40 人 · 五个区各 20 格</p>
  <div class="stin">
    <div class="stgrid"><svg class="grid" id="stsvg" viewBox="0 0 400 400" role="img" aria-label="十乘十的选民格子与五个区的边界"></svg></div>
    <div class="stpanel" id="stpanel" aria-live="polite">
      <p class="stk" id="stk">第 1 张 · 共 5 张</p>
      <h2 class="stname"><span id="stname">按比例</span><small id="stshort">3 : 2</small></h2>
      <p class="sthow" id="sthow"></p>
      <div class="seats" id="stseats">{seats}<small id="stseatsl"></small></div>
      <div class="wbar"><span>甲浪费</span><u><i class="a" id="stwa"></i></u><b id="stwan">0</b></div>
      <div class="wbar"><span>乙浪费</span><u><i class="b" id="stwb"></i></u><b id="stwbn">0</b></div>
      <div class="stnums">
        <div><span>效率差</span><b id="steg">0</b></div>
        <div><span>均值—中位数</span><b id="stmm">0</b></div>
        <div><span>切边数</span><b id="stcut">0</b></div>
      </div>
      <p class="stread" id="stread"></p>
    </div>
    <div class="struler" id="struler" role="slider" tabindex="0" aria-label="五种画法" aria-valuemin="0" aria-valuemax="{len(E.STAGE_STEPS) - 1}" aria-valuenow="0"><div class="rtrack"></div>{ticks}<span class="rknob" id="stknob"></span></div>
  </div>
</div>
</div>
<div class="wide"><p class="small fignote" style="margin-top:16px">{esc(E.STAGE_NOTE)}</p></div>
</section>'''

# ---------- 这一周
def week_sec():
    W = E.WEEK; cards = ''
    for c in W['cards']:
        extra = srcs([{'title': t, 'url': u} for t, u in c['src']]) if c.get('src') else ''
        cards += f'<div class="wcard fade"><p class="k">{esc(c["k"])}</p><h3>{esc(c["title"])}</h3><p>{esc(c["text"])}</p>{extra}</div>'
    rows = ''.join(f'<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td><td>{esc(r[3])}</td><td>{esc(r[4])}</td></tr>' for r in W['table'])
    table = f'''<details class="fold big"><summary><h3>十年中途重划：谁通过、什么时候、改了多少、法院怎么说（截至 2026-11-05）</h3></summary>
<div class="wtable"><table><thead><tr><th>州</th><th>谁定的图</th><th>日期</th><th>改动</th><th>法院状态 · 2026 年用哪张图</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small" style="margin-top:12px">{esc(W['table_note'])}</p></details>'''
    return f'''<section class="week" id="week" aria-label="这一周"><div class="wide"><div class="weekin">
<div class="weekk"><h2>这一周</h2><p class="small">{esc(W['lede'])}</p></div>
<div class="wcards">{cards}</div>{table}
</div></div></section>'''

# ---------- 第一章 · 时间轴
LANE_ORDER = ['draw', 'count', 'measure']
def node_year(n):
    y = n['year']
    return int(y) if isinstance(y, (int, float)) else int(re.search(r'-?\d+', str(y)).group())
def hist_groups():
    ids = sorted(NODES, key=lambda i: (node_year(NODES[i]), i))
    out = {'lane': [dict(k=l, label=E.LANE_NAME[l] + '：' + {'draw': '谁来画线、能不能画', 'count': '席位怎么按人口分', 'measure': '拿什么判断偏不偏'}[l], ids=[i for i in ids if NODES[i]['lane'] == l]) for l in LANE_ORDER]}
    out['era'] = [dict(k=k, label=l, ids=[i for i in ids if f(node_year(NODES[i]))]) for k, l, f in E.ERA]
    out['region'] = [dict(k=k, label=l, ids=[i for i in ids if E.REGION[i] == k]) for k, l in E.REGION_NAME.items()]
    return {k: [g for g in v if g['ids']] for k, v in out.items()}
HIST = hist_groups()
def hist_row(nid):
    n = NODES[nid]; y = node_year(n); lane = n['lane']
    attrs = ' '.join(f'data-g-{lens}="{next((g["k"] for g in groups if nid in g["ids"]), "")}"' for lens, groups in HIST.items())
    nums = ''.join(f'<div><span>{esc(x["label"])}</span><b>{esc(fmtnum(x["value"]))}{(" " + esc(x["unit"])) if x.get("unit") else ""}</b></div>' for x in (n.get('numbers') or [])[:4])
    q = f'<blockquote class="lquote">{esc(n["quote"])}<small>{esc(clean(n.get("quote_src", "")))}</small></blockquote>' if n.get('quote') else ''
    disp = f'<p class="dispute"><b>两说</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    fig = ''
    if nid in E.NODE_IMG:
        iid = E.NODE_IMG[nid]; fig = f'<figure class="lfig">{img_tag(iid)}<figcaption>{esc(IM[iid]["subject"])}{credit(iid)}</figcaption></figure>'
    return f'''<article class="lrow" id="n-{esc(nid)}" data-id="{esc(nid)}" {attrs}>
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(nid)}">
<span class="lyear">{esc(n['year_label'])}<small>{esc(n['place'].split('（')[0].split('·')[0][:10])}</small></span>
<span class="lname"><b>{esc(E.NODE_SHORT.get(nid, n['title_zh']))}</b><small>{esc(n['title_zh'])}</small></span>
<span class="lwhat">{esc(n['what'])}</span>
<span class="llane {lane}">{esc(E.LANE_NAME[lane])}</span>
<span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(nid)}" role="region" aria-label="{esc(n['title_zh'])} 详情"><div class="lmore-in">
<p class="ltext">{esc(clean(n['text']))}</p>
<dl class="lfacts"><dt>改了哪把尺子</dt><dd>{esc(n['ruler'])}</dd></dl>
{q}{('<div class="nnums">' + nums + '</div>') if nums else ''}{fig}{disp}
<details class="fold"><summary>来源 {conf(n.get('confidence'))}</summary>{srcs(n.get('sources'))}</details>
</div></div></article>'''

def ch_history():
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == "lane" else "false"}">{esc(t)}</button>' for k, t in E.HISTORY_LENSES)
    body = ''
    for g in HIST['lane']:
        body += f'<div class="lgh" data-g="{g["k"]}"><b>{esc(g["label"])}</b><small>{len(g["ids"])} 条</small></div>' + ''.join(hist_row(i) for i in g['ids'])
    return f'''<section class="chap hist" id="history"><div class="wide">{chead("history")}
<div class="fig fade"><div class="fighead"><h3>二十二个节点，三条泳道</h3><p class="small">拖动竖线，或者点一个点。</p></div>
<div class="tlbox" id="tlbox" role="slider" tabindex="0" aria-label="时间轴" aria-valuemin="-508" aria-valuemax="2026" aria-valuenow="1812"><svg class="tl" id="tlsvg" viewBox="0 0 1200 300" aria-hidden="true"></svg></div>
<div class="tlread" id="tlread"><div class="y" id="tly">1812<small>画线</small></div><div><b id="tlt"></b><p id="tlw"></p><p class="ru" id="tlr"></p></div><div class="go"><button type="button" class="sbtn" id="tlgo">看这一条 ↓</button></div></div>
<p class="fignote">{esc(E.HISTORY_NOTE)}</p></div>
<div class="lensbar fade"><span class="lensk">按</span><div class="lens" id="lens-history" role="tablist" aria-label="时间轴的透镜">{tabs}</div><span class="lensnote" id="lensnote-history"></span></div>
<div class="lgrid" id="lgrid-history">{body}</div>
</div></section>'''

# ---------- 第二章 · 量尺
def rfig(kind):
    """每把尺子一张小示意图（72×48，抽象几何）。"""
    if kind == 'circle': return '<svg viewBox="0 0 72 48"><circle class="ink2" cx="22" cy="24" r="18"/><path class="ink" d="M8 30 C12 10 30 8 34 20 C38 32 56 14 62 26 C66 36 54 42 42 40 C30 38 20 44 8 30Z"/></svg>'
    if kind == 'mbc': return '<svg viewBox="0 0 72 48"><circle class="ink2" cx="36" cy="24" r="22"/><path class="ink" d="M16 22 L50 14 L58 30 L30 38 Z"/></svg>'
    if kind == 'hull': return '<svg viewBox="0 0 72 48"><path class="ink2" d="M10 40 L20 6 L60 10 L64 40 Z"/><path class="ink" d="M10 40 L20 6 L36 22 L60 10 L64 40 L40 30 Z"/></svg>'
    if kind == 'cut': return '<svg viewBox="0 0 72 48"><g class="ink2">' + ''.join(f'<line x1="{8 + i * 14}" y1="6" x2="{8 + i * 14}" y2="42"/>' for i in range(5)) + ''.join(f'<line x1="8" y1="{6 + j * 12}" x2="64" y2="{6 + j * 12}"/>' for j in range(4)) + '</g><path class="red" d="M22 6 L22 18 L36 18 L36 30 L50 30 L50 42"/></svg>'
    if kind == 'packcrack': return '<svg viewBox="0 0 72 48"><rect class="fb" x="4" y="6" width="20" height="36"/><rect class="ink" x="4" y="6" width="20" height="36"/><rect class="fa" x="30" y="6" width="38" height="36"/><rect class="ink" x="30" y="6" width="38" height="36"/><line class="ink" x1="43" y1="6" x2="43" y2="42"/><line class="ink" x1="56" y1="6" x2="56" y2="42"/></svg>'
    if kind == 'wasted': return '<svg viewBox="0 0 72 48"><rect class="grey" x="6" y="12" width="60" height="10"/><rect class="fa" x="6" y="12" width="36" height="10"/><rect class="redf" x="30" y="12" width="6" height="10"/><rect class="grey" x="6" y="28" width="60" height="10"/><rect class="fb" x="6" y="28" width="24" height="10"/><rect class="redf" x="6" y="28" width="24" height="10" style="fill-opacity:.35"/><line class="ink2" x1="36" y1="8" x2="36" y2="42"/></svg>'
    if kind == 'dist': return '<svg viewBox="0 0 72 48">' + ''.join(f'<circle class="inkf" cx="{10 + i * 11}" cy="{30 - [0, 2, 3, 12, 14, 16][i]}" r="3"/>' for i in range(6)) + '<line class="red" x1="4" y1="38" x2="68" y2="38"/><line class="ink2" x1="38" y1="6" x2="38" y2="42"/></svg>'
    if kind == 'decl': return '<svg viewBox="0 0 72 48"><line class="ink2" x1="4" y1="24" x2="68" y2="24"/><line class="ink" x1="4" y1="40" x2="30" y2="30"/><line class="red" x1="30" y1="30" x2="68" y2="6"/><circle class="redf" cx="30" cy="30" r="2.5"/></svg>'
    if kind == 'sv': return '<svg viewBox="0 0 72 48"><line class="ink2" x1="6" y1="42" x2="66" y2="6"/><path class="ink" d="M6 44 C30 44 30 4 66 4"/><path class="red" d="M6 44 C40 44 36 4 66 4"/></svg>'
    if kind == 'cube': return '<svg viewBox="0 0 72 48"><line class="ink2" x1="6" y1="42" x2="66" y2="6"/><path class="ink" d="M6 44 C30 44 30 4 66 4"/><circle class="redf" cx="36" cy="24" r="2.5"/></svg>'
    if kind == 'hist': return '<svg viewBox="0 0 72 48">' + ''.join(f'<rect class="inkf" x="{8 + i * 9}" y="{42 - h}" width="7" height="{h}" style="fill-opacity:.35"/>' for i, h in enumerate([2, 6, 16, 30, 24, 10, 3])) + '<rect class="redf" x="62" y="38" width="7" height="4"/><line class="red" x1="65" y1="8" x2="65" y2="36"/></svg>'
    return ''
def ruler_year(mid):
    return {'pack_crack': 2018, 'efficiency_gap': 2015, 'mean_median': 2015, 'partisan_symmetry': 2007, 'declination': 2018, 'cube_law': 1950, 'polsby_popper': 1991, 'reock': 1961, 'schwartzberg': 1966, 'convex_hull': 1991, 'cut_edges': 2021, 'ensemble_outlier': 2017}[mid]
def ruler_groups():
    ids = E.RULER_ORDER
    out = {'what': [dict(k=k, label=l, ids=[i for i in ids if E.RULER_GROUP[i] == k]) for k, l in E.RULER_GROUP_NAME]}
    out['year'] = [dict(k='old', label='1991 年以前的代表作', ids=[i for i in ids if ruler_year(i) < 1991]), dict(k='mid', label='1991–2014 年的代表作', ids=[i for i in ids if 1991 <= ruler_year(i) < 2015]), dict(k='new', label='2015 年以后的代表作', ids=[i for i in ids if ruler_year(i) >= 2015])]
    return {k: [g for g in v if g['ids']] for k, v in out.items()}
RUL = ruler_groups()
def ruler_row(mid):
    m = METRICS[mid]
    attrs = ' '.join(f'data-g-{lens}="{next((g["k"] for g in groups if mid in g["ids"]), "")}"' for lens, groups in RUL.items())
    rng = m.get('range', ''); rng_short = rng.split('；')[0].split('。')[0]
    return f'''<article class="lrow" id="n-{esc(mid)}" data-id="{esc(mid)}" {attrs}>
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(mid)}">
<span class="rfig" aria-hidden="true">{rfig(E.RULER_FIG[mid])}</span>
<span class="lname"><b>{esc(m['name_zh'])}</b><small>{esc(m['name_en'])}</small></span>
<span class="lone">{esc(E.RULER_ONE[mid])}<br><span class="lrange">{esc(rng_short)}</span></span>
<span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(mid)}" role="region" aria-label="{esc(m['name_zh'])} 详情"><div class="lmore-in">
<p class="ltext">{esc(m['what'])}</p>
<div class="formula">{esc(m['formula'])}</div>
<dl class="lfacts"><dt>取值</dt><dd>{esc(m.get('range', ''))}</dd><dt>什么时候失灵</dt><dd>{esc(m.get('fails', ''))}</dd><dt>出处</dt><dd>{esc(m.get('origin', ''))}</dd></dl>
<details class="fold"><summary>来源 {conf(m.get('confidence'))}</summary>{srcs(m.get('sources'))}</details>
</div></div></article>'''

def ch_rulers():
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == "what" else "false"}">{esc(t)}</button>' for k, t in [('what', '量什么'), ('year', '用于选区研究的年代')])
    body = ''
    for g in RUL['what']:
        body += f'<div class="lgh" data-g="{g["k"]}"><b>{esc(g["label"])}</b><small>{len(g["ids"])} 把</small></div>' + ''.join(ruler_row(i) for i in g['ids'])
    plans = ''.join(f'<button type="button" class="sbtn" data-plan="{esc(s["plan"])}" aria-pressed="{"true" if i == 0 else "false"}">{esc(s["name"])} {esc(s["short"])}</button>' for i, s in enumerate(E.STAGE_STEPS))
    plans += '<button type="button" class="sbtn" data-plan="mine" aria-pressed="false" id="svmine" disabled>你画的</button>'
    return f'''<section class="chap rulers" id="rulers"><div class="wide">{chead("rulers")}
<div class="fig fade"><div class="fighead"><h3>席位—选票曲线</h3><p class="small">同一张划法，如果全体选民的票整体向一边摆，席位会怎么跟着变？</p></div>
<div class="ctl"><span>划法</span><div class="grp" id="svplans">{plans}</div></div>
<div class="svbox"><svg class="sv" id="svsvg" viewBox="0 0 1200 520" role="img" aria-label="席位—选票曲线"></svg></div>
<div class="svread"><div><span>50% 票时的席位偏差 S(0.5) − 0.5</span><b id="svbias">0</b></div><div><span>甲拿 60% 票 → 席位</span><b id="svnow">—</b></div><div><span>换成乙拿 60% 票 → 乙的席位（对称性检验）</span><b id="svresp">—</b></div></div>
<p class="fignote">{esc(E.SV_NOTE)}</p></div>
<div class="lensbar fade"><span class="lensk">按</span><div class="lens" id="lens-rulers" role="tablist" aria-label="量尺的透镜">{tabs}</div><span class="lensnote" id="lensnote-rulers"></span></div>
<div class="lgrid" id="lgrid-rulers">{body}</div>
</div></section>'''

# ---------- 第三章 · 各国
def pol_index(pid):
    p = POLS[pid]
    if p['id'] in ('zaf', 'nld', 'isr'): return 0.0
    if pid == 'nir': return None
    return B['index']['values'].get(p['iso3'])
def pol_groups():
    ids = [p['id'] for p in B['polities']]
    def iv(pid): return pol_index(pid)
    byidx = lambda L: sorted(L, key=lambda i: (-(iv(i) if iv(i) is not None else -1), POLS[i]['name_zh']))
    out = {}
    out['who'] = [dict(k=k, label=l, ids=byidx([i for i in ids if POLS[i]['who_draws'] == k])) for k, l in E.WHO_NAME.items()]
    out['sys'] = [dict(k=k, label=l, ids=byidx([i for i in ids if POLS[i]['system'] == k])) for k, l in E.SYS_NAME.items()]
    out['path'] = [dict(k=k, label=l, ids=byidx([i for i in ids if POLS[i]['pathology'] == k])) for k, l in E.PATH_NAME.items()]
    out['region'] = [dict(k=k, label=l, ids=byidx([i for i in ids if E.POL_REGION[i] == k])) for k, l in E.POL_REGION_NAME]
    return {k: [g for g in v if g['ids']] for k, v in out.items()}
POL = pol_groups()
def pol_row(pid):
    p = POLS[pid]; v = pol_index(pid)
    attrs = ' '.join(f'data-g-{lens}="{next((g["k"] for g in groups if pid in g["ids"]), "")}"' for lens, groups in POL.items())
    idx = (f'<span class="lidx"><b>{v:.3f}</b>指数<u><i style="width:{min(100, v / 0.21 * 100):.0f}%"></i></u></span>' if v is not None else '<span class="lidx"><b>—</b>指数缺</span>')
    nums = ''.join(f'<div><span>{esc(x["label"])}{(" · " + esc(x["year"])) if x.get("year") else ""}</span><b>{esc(fmtnum(x["value"]))}{(" " + esc(x["unit"])) if x.get("unit") else ""}</b></div>' for x in (p.get('numbers') or [])[:4])
    disp = f'<p class="dispute"><b>两说</b>{esc(p["dispute"])}</p>' if p.get('dispute') else ''
    ev = p.get('event') or {}
    return f'''<article class="lrow" id="n-{esc(pid)}" data-id="{esc(pid)}" {attrs}>
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(pid)}">
<span class="lname"><b>{esc(p['name_zh'])}</b><small>{esc(p['name_en'])}</small></span>
<span class="lwho"><span class="tag">{esc(E.WHO_NAME[p['who_draws']])}</span>{esc(brief(p['who_text'], 38))}</span>
<span class="lsys"><span class="tag">{esc(E.SYS_NAME[p['system']])}</span>{esc(brief(p['system_text'], 30))}</span>
<span class="lpath {esc(p['pathology'])}">{esc(E.PATH_NAME[p['pathology']])}：{esc(brief(p['pathology_text'], 44))}</span>
{idx}<span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(pid)}" role="region" aria-label="{esc(p['name_zh'])} 详情"><div class="lmore-in">
<p class="ltext">{esc(clean(p['text']))}</p>
<dl class="lfacts"><dt>谁画线</dt><dd>{esc(p['who_text'])}</dd><dt>选举制</dt><dd>{esc(p['system_text'])}</dd><dt>病症</dt><dd>{esc(p['pathology_text'])}</dd><dt>周期</dt><dd>{esc(p['cadence'])}</dd><dt>一件事 · {esc(ev.get('year', ''))}</dt><dd>{esc(ev.get('text', ''))}</dd></dl>
{('<div class="nnums">' + nums + '</div>') if nums else ''}{disp}
<details class="fold"><summary>来源 {conf(p.get('confidence'))}</summary>{srcs(p.get('sources'))}</details>
</div></div></article>'''

def world_svg():
    W, H = WORLD['w'], WORLD['h']
    grat = ''.join(f'<line class="grat" x1="0" y1="{(90 - la) / 180 * H:.1f}" x2="{W}" y2="{(90 - la) / 180 * H:.1f}"/>' for la in (-60, -30, 0, 30, 60))
    grat += ''.join(f'<line class="grat" x1="{(lo + 180) / 360 * W:.1f}" y1="0" x2="{(lo + 180) / 360 * W:.1f}" y2="{H}"/>' for lo in range(-150, 180, 30))
    dots = ''
    for p in B['polities']:
        v = pol_index(p['id']); x = (p['lon'] + 180) / 360 * W; y = (90 - p['lat']) / 180 * H
        r = 3 + (0 if v is None else (v ** 0.5) * 26)
        cls = 'pol' + (' none' if v is None else '') + (' zero' if v == 0 else '')
        LAB = {'nir': (-6, -10, 'end'), 'irl': (-6, 14, 'end'), 'gbr': (r + 3, -8, 'start'), 'nld': (r + 2, -12, 'start'), 'deu': (r + 3, 2, 'start'), 'fra': (-(r + 3), 12, 'end'), 'esp': (0, r + 11, 'middle'), 'hun': (r + 3, 10, 'start'), 'swe': (r + 3, -4, 'start'), 'isr': (r + 3, 10, 'start'), 'sgp': (r + 3, 10, 'start'), 'mys': (r + 3, -4, 'start'), 'twn': (r + 3, 4, 'start'), 'kor': (-(r + 3), -4, 'end'), 'jpn': (r + 3, 4, 'start'), 'nzl': (-(r + 3), 12, 'end'), 'aus': (-(r + 3), 12, 'end'), 'chl': (-(r + 3), 4, 'end'), 'arg': (r + 3, 12, 'start'), 'zaf': (r + 3, 4, 'start'), 'ind': (r + 3, 4, 'start'), 'bra': (r + 3, 4, 'start'), 'can': (r + 3, -4, 'start'), 'usa': (r + 3, 10, 'start')}
        dx, dy, anc = LAB.get(p['id'], (r + 4, 4, 'start'))
        dots += f'<g class="{cls}" data-id="{esc(p["id"])}" transform="translate({x:.1f},{y:.1f})"><circle class="r" r="{r:.1f}"/><circle r="{max(r, 9):.0f}" fill="transparent"/><text x="{dx}" y="{dy}" text-anchor="{anc}">{esc(p["name_zh"])}</text></g>'
    return f'<svg class="wm" id="wmsvg" viewBox="0 0 {W} {H}" role="img" aria-label="24 个政体在世界地图上"><g>{grat}</g><path class="land" d="{WORLD["d"]}"/><g id="wmdots">{dots}</g></svg>'

def ch_world():
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == "who" else "false"}">{esc(t)}</button>' for k, t in E.WORLD_LENSES)
    body = ''
    for g in POL['who']:
        body += f'<div class="lgh" data-g="{g["k"]}"><b>{esc(g["label"])}</b><small>{len(g["ids"])} 个</small></div>' + ''.join(pol_row(i) for i in g['ids'])
    return f'''<section class="chap world" id="world"><div class="wide">{chead("world")}
<div class="fig fade"><div class="fighead"><h3>席位与人口有多不成比例</h3><p class="small">圆越大，各选区「每席人口」差得越多。点一个圆看那一行。</p></div>
<div class="wmapbox">{world_svg()}</div>
<div class="wmkey"><span><i style="width:7px;height:7px"></i>指数 0（全国一区）</span><span><i style="width:14px;height:14px"></i>0.03</span><span><i style="width:22px;height:22px"></i>0.10</span><span><i style="width:30px;height:30px"></i>0.20</span><span><i class="none" style="width:12px;height:12px"></i>没有数值</span></div>
<p class="fignote">{esc(E.WORLD_NOTE)}</p></div>
<div class="lensbar fade"><span class="lensk">按</span><div class="lens" id="lens-world" role="tablist" aria-label="各国的透镜">{tabs}</div><span class="lensnote" id="lensnote-world"></span></div>
<div class="lgrid" id="lgrid-world">{body}</div>
</div></section>'''

# ---------- 第四章 · 分配
def ch_count():
    cards = ''
    for c in E.PARADOX_CARDS:
        btn = ' '.join(f'<button type="button" class="sbtn red" data-demo="{esc(k)}">{esc(t)}</button>' for k, t in c.get('btns', []))
        cards += f'<div class="pcard fade"><p class="k">{esc(c["year"])}</p><h3>{esc(c["title"])}</h3><p>{esc(c["text"])}</p>{btn}</div>'
    methods = ''.join(f'<label><input type="checkbox" data-m="{k}" {"checked" if k in ("hamilton", "webster", "huntington_hill") else ""}> {esc(E.METHOD_SHORT[k])}</label>' for k in E.METHOD_SHORT)
    opts = ''.join(f'<option value="{y}">{lab}</option>' for y, lab in (('1880', '1880 年普查 · 38 州（1882 年法案 325 席）'), ('1900', '1900 年普查 · 45 州（1901 年法案 386 席）'), ('2020', '2020 年普查 · 50 州（435 席）')))
    contrast = ''.join(f'<div class="pcard fade"><h3>{esc(c["title"])}</h3><p>{esc(c["text"])}</p></div>' for c in E.COUNT_CONTRAST)
    return f'''<section class="chap count" id="count"><div class="wide">{chead("count")}
<div class="pcards">{cards}</div>
<div class="fig fade"><div class="fighead"><h3>六种分配法，同一组人口</h3><p class="small">勾选算法，拖动总席位；标朱砂的格子是「总席位加了一席、这个州反而少一席」。</p></div>
<div class="ctl"><label>人口 <select id="apds">{opts}</select></label><label style="flex:1 1 260px">总席位 <b id="aph">325</b><input type="range" id="aprange" min="275" max="350" value="325" step="1" aria-label="总席位"></label><span class="grp" style="gap:12px;flex-wrap:wrap" id="apmethods">{methods}</span></div>
<div class="aptbl" id="aptbl"></div>
<div class="apread" id="apread"></div>
<p class="fignote">{esc(E.COUNT_NOTE)}</p></div>
<div class="ccards">{contrast}</div>
</div></section>'''

# ---------- 动手
def ch_hands():
    Hd = E.HANDS
    pal = ''.join(f'<button type="button" class="sbtn" data-d="{k}" aria-pressed="{"true" if k == 0 else "false"}"><i></i>区 {k + 1} <small>·<span data-cnt="{k}">0</span>/20</small></button>' for k in range(STAGE['K']))
    presets = ''.join(f'<button type="button" class="sbtn" data-preset="{esc(s["plan"])}">{esc(s["name"])}</button>' for s in E.STAGE_STEPS)
    return f'''<section class="chap hands" id="hands"><div class="wide">{chead("hands")}
<div class="hands2 fade">
<div>
  <div class="fighead"><h3>{esc(Hd['draw_title'])}</h3></div><p class="small">{esc(Hd['draw_lede'])}</p>
  <div class="dpal" id="dpal">{pal}<button type="button" class="sbtn" data-d="-1" aria-pressed="false">橡皮</button></div>
  <div class="drawbox"><svg class="grid" id="drawsvg" viewBox="0 0 400 400" role="img" aria-label="画线器：十乘十的格子"></svg></div>
  <p class="dstat" id="dstat">{esc(Hd['draw_hint'])}</p>
  <div class="dpal"><span class="small" style="margin-right:4px">预设</span>{presets}<button type="button" class="sbtn" data-preset="clear">清空</button></div>
</div>
<div>
  <div class="fighead"><h3>读数</h3></div>
  <div class="seats" id="dseats">{''.join('<i></i>' for _ in range(STAGE['K']))}<small id="dseatsl"></small></div>
  <div class="wbar" style="margin-top:12px"><span>甲浪费</span><u><i class="a" id="dwa"></i></u><b id="dwan">0</b></div>
  <div class="wbar"><span>乙浪费</span><u><i class="b" id="dwb"></i></u><b id="dwbn">0</b></div>
  <div class="dnums">
    <div><span>效率差（正值对甲有利）</span><b id="deg">—</b></div>
    <div><span>均值—中位数差（甲）</span><b id="dmm">—</b></div>
    <div><span>切边数</span><b id="dcut">—</b></div>
    <div><span>Polsby–Popper 均值</span><b id="dpp">—</b></div>
  </div>
  <p class="small" style="margin-top:16px">画满五个区（各二十格、连通）读数才算数。想看这张的席位—选票曲线，回到第二章点「你画的」。</p>
</div>
</div>
<div class="ens fade" id="ens">
  <div class="enshead"><h3>{esc(Hd['ens_title'])}</h3><button type="button" class="btn" id="ensrun" style="padding:8px 16px;font-size:14px">随机画 3,000 张</button><span class="small" id="ensstat">还没跑。</span></div>
  <p class="small">{esc(Hd['ens_lede'])}</p>
  <div class="ensbox"><div class="hbars" id="hbars">{''.join(f'<div class="hbar" data-s="{s}"><u></u><b>{s}:{STAGE["K"] - s}<small>甲 {s} 席</small></b></div>' for s in range(STAGE['K'] + 1))}</div>
  <div class="prog2"><i id="ensprog"></i></div>
  <p class="ensread" id="ensread"></p></div>
  <p class="fignote">{esc(Hd['ens_hint'])}</p>
</div>
</div></section>'''

# ---------- 卷末
def refs_block():
    groups = [('这一周', [{'title': t, 'url': u} for c in E.WEEK['cards'] if c.get('src') for t, u in c['src']] + [{'title': 'NCSL, Changing the Maps: Tracking Mid-Decade Redistricting', 'url': 'https://www.ncsl.org/redistricting-and-census/changing-the-maps-tracking-mid-decade-redistricting'}]),
              ('第一章 · 时间轴', [s for n in A['nodes'] for s in n.get('sources', [])]),
              ('第二章 · 量尺', [s for m in C['metrics'] for s in m.get('sources', [])]),
              ('第三章 · 各国', [s for p in B['polities'] for s in p.get('sources', [])] + [{'title': B['index']['source'], 'url': 'https://doi.org/10.1017/S0007123401000254'}]),
              ('第四章 · 分配', [s for a in C['apportionment'] for s in a.get('sources', [])] + [s for p in C['paradoxes'] for s in p.get('sources', [])] + [s for d in C['datasets'] for s in (d.get('sources') or [])])]
    out = ''
    for title, ss in groups:
        seen = set(); items = []
        for s in ss:
            u = s.get('url') or ''; t = s.get('title') or u
            key = u or t
            if key in seen: continue
            seen.add(key); items.append(f'<li><a href="{esc(u)}" rel="noopener">{esc(t)}</a></li>' if u else f'<li>{esc(t)}</li>')
        out += f'<details class="fold refs"><summary>{esc(title)} · {len(items)} 条</summary><ol>{"".join(items)}</ol></details>'
    return out
def credits():
    rows = ''.join(f'<tr><td>{esc(IM[i]["subject"])}</td><td>{esc(IM[i]["author"])}</td><td>{esc(IM[i]["year"])}</td><td><a href="{esc(IM[i]["license_url"])}" rel="noopener">{esc(IM[i]["license_short"])}</a></td><td><a href="{esc(IM[i]["source_url"])}" rel="noopener">来源</a></td></tr>' for i in USED_IMG)
    return f'<table class="credits"><thead><tr><th>图</th><th>作者</th><th>年代</th><th>许可</th><th></th></tr></thead><tbody>{rows}</tbody></table>'
def endm():
    return f'''<footer class="endm" id="end"><div class="wide">
<h2>方法与参考</h2>
<details class="fold big" open><summary><h3>方法</h3></summary><ul>{''.join(f'<li>{esc(x)}</li>' for x in E.METHOD)}</ul></details>
<details class="fold big"><summary><h3>仍待核</h3></summary><ul>{''.join(f'<li>{esc(x)}</li>' for x in E.VERIFY)}</ul></details>
<details class="fold big"><summary><h3>参考（按章）</h3></summary>{refs_block()}</details>
<details class="fold big"><summary><h3>图片署名（{len(USED_IMG)} 张）</h3></summary>{credits()}</details>
<p class="stamp">一周一题 · 第 8 题 · 2026-11-07</p>
</div></footer>'''

# ---------- 数据 → JSON（app.js 用）
def data():
    nodes = [dict(id=n['id'], year=node_year(n), label=n['year_label'], lane=n['lane'], short=E.NODE_SHORT.get(n['id'], n['title_zh']), title=n['title_zh'], what=n['what'], ruler=n['ruler']) for n in A['nodes']]
    nodes.sort(key=lambda n: (n['year'], n['id']))
    ap = {y: dict(rows=DS[f'us_{y}_states']['rows'], H=DS[f'us_{y}_states'].get('H') or {'1880': 325, '1900': 386, '2020': 435}[y]) for y in ('1880', '1900', '2020')}
    return dict(
        stage=dict(n=STAGE['n'], K=STAGE['K'], cells=STAGE['cells'], plans=STAGE['plans'], steps=[dict(id=s['id'], plan=s['plan'], name=s['name'], short=s['short'], how=s['how'], read=s['read']) for s in STEPS]),
        nodes=nodes, laneName=E.LANE_NAME,
        lens={'history': HIST, 'rulers': RUL, 'world': POL},
        lensName={'history': dict(E.HISTORY_LENSES), 'rulers': {'what': '量什么', 'year': '用于选区研究的年代'}, 'world': dict(E.WORLD_LENSES)},
        ap=ap, methodName=E.METHOD_SHORT,
        pols=[dict(id=p['id'], name=p['name_zh']) for p in B['polities']],
    )

def fill_step(s):
    """把 stage.json 的读数填进文案。"""
    m = STAGE['metrics'][s['plan']]; hist = STAGE['ensemble']['hist']; tot = sum(hist.values())
    def sg(x): return ('+' if x > 0 else '') + f'{x:.2f}'
    vals = dict(cut=m['cutEdges'], eg=sg(m['eg']), wa=int(m['wastedA']), wb=int(m['wastedB']), **{f'p{k}': f'{hist.get(str(k), 0) / tot * 100:.0f}%' if hist.get(str(k), 0) / tot >= 0.015 else f'{hist.get(str(k), 0) / tot * 100:.1f}%' for k in range(6)})
    out = dict(s); out['read'] = s['read'].format(**vals); out['how'] = s['how'].format(**vals); return out
STEPS = [fill_step(s) for s in E.STAGE_STEPS]

def audit():
    """文案里写死的数字必须和 stage.json 对得上。"""
    M = STAGE['metrics']; hist = STAGE['ensemble']['hist']; tot = sum(hist.values())
    checks = [
        ('fair cut 28 (写在 crack 的文案里)', M['fair']['cutEdges'] == 28), ('fair seats 3', M['fair']['seatsA'] == 3 and M['fair']['seatsB'] == 2), ('crack 5:0', M['crack']['seatsA'] == 5), ('pack 4:1', M['pack']['seatsA'] == 4 and M['pack']['seatsB'] == 1), ('flip 2:3', M['flip']['seatsA'] == 2 and M['flip']['seatsB'] == 3),
        ('crack B wasted 40', M['crack']['wastedB'] == 40 and M['crack']['wastedA'] == 10), ('pack B wasted 10 extra', M['pack']['wastedB'] >= 10),
        ('pack: one district all B, others ≤9 B', sorted(20 - a for a in M['pack']['aVotes'])[-1] == 20 and sorted(20 - a for a in M['pack']['aVotes'])[-2] <= 9 and M['pack']['ties'] == 0),
        ('flip: three districts with ≥11 B, no ties', sum(1 for a in M['flip']['aVotes'] if 20 - a >= 11) == 3 and M['flip']['ties'] == 0),
        ('crack/fair/random no ties', all(M[k]['ties'] == 0 for k in M)),
        ('hist 5 rare', hist['5'] / tot < 0.02), ('hist 3+4 dominate', (hist['3'] + hist['4']) / tot > 0.9),
    ]
    bad = [k for k, ok in checks if not ok]
    if bad: raise SystemExit('audit 失败：' + ', '.join(bad) + f'\n{json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ("seatsA", "eg", "cutEdges", "wastedA", "wastedB", "aVotes")} for k, v in M.items()}, ensure_ascii=False)}\n{hist}')
    print('audit ok:', len(checks), '项')

def main():
    audit()
    body = hero() + tagline_sec() + cnav() + ch_stage() + week_sec() + ch_history() + ch_rulers() + ch_world() + ch_count() + ch_hands() + endm()
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    dark = ''':root[data-theme=dark]{--bg:#15130F;--surface:#1D1A15;--surface-2:#252119;--surface-3:#332D23;--ink:#EFE6D3;--ink-2:#CFC5B0;--muted:#9B9385;--line:rgba(239,230,211,.22);--line-2:rgba(239,230,211,.1);--grid:rgba(239,230,211,.08);--accent:#D9553B;--accent-ink:#E2694F;--accent-2:#F07A5E;--wash:rgba(217,85,59,.12);--wash-2:rgba(217,85,59,.24);--pat-ink:#EFE6D3;--pat-bg:#1D1A15;color-scheme:dark}'''
    html_out = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E.META['description'])).replace('{{DARK_BLOCKS}}', dark)
                .replace('{{BODY}}', body).replace('{{DATA_JSON}}', json.dumps(data(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
                .replace('{{GEO_JS}}', open(os.path.join(HERE, 'geo.js'), encoding='utf-8').read())
                .replace('{{APP_JS}}', open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()))
    # 自检：编辑用语不该漏到页面上
    for bad in ('text_long', '本路', '不下结论', '页面不要写成', '待核原文', 'verify', '{cut}', '{eg}', '{p3}'):
        if bad in re.sub(r'<script[\s\S]*?</script>', '', html_out): raise SystemExit(f'页面里出现了编辑用语「{bad}」')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html_out)
    meta = dict(no=E.META['no'], slug=E.META['slug'], title=E.META['title'], subtitle=E.META['subtitle'], date=E.META['date'], summary=E.META['summary'], tags=E.META['tags'], format=E.META['format'],
                cover='cover.png', cover_focus='#top', cover_scheme='light', reading_time=E.META['reading_time'],
                sources=['法院判决与法律条文：Baker、Wesberry、Reynolds、Gingles、Shaw、Gill、Rucho、Milligan（supremecourt.gov / LII / govinfo）；1842、1911、1929、1941 年分配法；英国 1832、1944、2020 年法；日本最高裁 2011–2023 判决；Cameron 报告（1969）',
                         '机构与数据：美国普查局（分配方法与历次分配表）、各国选举委员会与边界委员会、总务省、OSCE/ODIHR、Samuels & Snyder 2001',
                         '论文：Stephanopoulos & McGhee 2015、McDonald & Best 2015、Grofman & King 2007、Warrington 2018、Polsby & Popper 1991、Chen & Rodden 2013、Chikina–Frieze–Pegden 2017、DeFord–Duchin–Solomon 2021、Kendall & Stuart 1950、Balinski & Young 1982',
                         f'图片 {len(USED_IMG)} 张：美国国会图书馆、大都会艺术博物馆 Open Access、美国最高法院判决附录、美国普查局、维基共享资源（CC BY-SA）；逐张署名见页面卷末与 src/images.json'])
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('index.html', len(html_out), 'bytes; images used', len(USED_IMG))

if __name__ == '__main__':
    main()
