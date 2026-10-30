#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 1 题「中国菜系演化图谱」v2：shell.html + app.js + content/*.js（v1 数据，构建时按 editorial2.DATA_FIX 改正）
+ map_data.json + palette*.json + chili.json + images.json → ../index.html，并更新 ../meta.json。

  python3 themes/2026-09-21-cuisine-atlas/src/build_theme.py

改 v1 的内容数据只改 src/content/*.js（改正写进 editorial2.DATA_FIX，每条必须恰好命中一次）；新写的文案在 src/editorial2.py；
辣椒一章的记录在 src/chili.json；图片记录在 src/images.json。v1 的单文件模板与 2026-10-30 首屏阶段的 atlas.* 已删（git 历史里有）。
需要 node（用来求值 content/*.js）。
"""
import json, os, re, sys, html, subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import editorial2 as E2

SITE_URL = 'https://tianjie.me/t/cuisine-atlas/'
TITLE = '中国菜系演化图谱'
esc = lambda s: html.escape(str(s), quote=True)
rd = lambda f: open(os.path.join(SRC, f), encoding='utf-8').read()
q = lambda s: str(s).replace('“', '「').replace('”', '」')        # 新写的章节统一用「」
CN = '零一二三四五六七八九十'

IM = {i['id']: i for i in json.load(open(os.path.join(SRC, 'images.json'), encoding='utf-8')) if i.get('status') == 'ok'}

# ---------- v1 数据：拼接、改正、求值
def load_data():
    js = ''.join(rd(os.path.join('content', f)) + '\n' for f in ['c_meta.js', 'c_p1.js', 'c_p2.js', 'c_p3.js', 'c_modern.js'])
    for old, new, why in E2.DATA_FIX:
        n = js.count(old)
        if n != 1: sys.exit(f'DATA_FIX 命中 {n} 次（应为 1 次）：{old[:60]}…')
        js = js.replace(old, new)
    r = subprocess.run(['node'], input=js + '\nprocess.stdout.write(JSON.stringify(DATA));', capture_output=True, text=True)
    if r.returncode: sys.exit('node 求值失败：' + r.stderr[-800:])
    return json.loads(r.stdout)
DATA = load_data()
PER, PROV = DATA['periods'], DATA['provinces']
NP = len(PER)
CODES = list(PROV.keys())

def region_of(pi, c): return next((r for r in PER[pi]['regions'] if c in r['provs']), None)
def taste_of(pi, c): return ((PER[pi].get('overrides') or {}).get(c) or {}).get('taste') or region_of(pi, c)['taste']
def staple_of(pi, c): return ((PER[pi].get('overrides') or {}).get(c) or {}).get('staple') or region_of(pi, c)['staple']
for pi in range(NP):
    for c in CODES: assert region_of(pi, c), (PER[pi]['id'], c)

# ---------- 地图与配色
MP = json.load(open(os.path.join(SRC, 'map_data.json')))
ded = []                                   # 南海诸岛的小岛点抽稀
for x, y in MP['islands']:
    if all(abs(x - a) > 5 or abs(y - b) > 5 for a, b in ded): ded.append((x, y))
MP['islands'] = [[x, y] for x, y in ded]
pal = json.load(open(os.path.join(SRC, 'palette.json')))
spec = json.load(open(os.path.join(SRC, 'palette_spec.json')))
def css_vars(mode): return ''.join(f'--{k}:{v};' for k, v in pal[mode].items())
palmeta = {'light': {}, 'dark': {}}       # 填色较深（OKLCH L < 0.58）时省名用浅色字
for mode in ('light', 'dark'):
    for group in ('fam', 'taste', 'staple'):
        for k, (h, c, l) in spec[group][mode].items():
            if l < 0.58: palmeta[mode][f'{group}-{k}'] = True

def path_bbox(d):
    toks = re.findall(r'[MmLlHhVvZz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    x = y = sx = sy = 0.0; cmd = 'M'; xs, ys = [], []; i = 0
    while i < len(toks):
        t = toks[i]
        if t[0] in 'MmLlHhVvZz':
            cmd = t; i += 1
            if t in 'Zz': x, y = sx, sy
            continue
        if cmd in 'Mm':
            a, b = float(toks[i]), float(toks[i + 1]); i += 2
            x, y = (a, b) if cmd == 'M' else (x + a, y + b); sx, sy = x, y; cmd = 'L' if cmd == 'M' else 'l'
        elif cmd in 'Ll':
            a, b = float(toks[i]), float(toks[i + 1]); i += 2
            x, y = (a, b) if cmd == 'L' else (x + a, y + b)
        elif cmd in 'Hh': a = float(toks[i]); i += 1; x = a if cmd == 'H' else x + a
        elif cmd in 'Vv': a = float(toks[i]); i += 1; y = a if cmd == 'V' else y + a
        else: i += 1; continue
        xs.append(x); ys.append(y)
    return [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
PBOX = {c: path_bbox(v['d']) for c, v in MP['prov'].items()}
ANCHOR = {c: [round(MP['prov'][c]['c'][0] + PROV[c]['dx'], 1), round(MP['prov'][c]['c'][1] + PROV[c]['dy'], 1)] for c in CODES}
VW, VH = MP['w'], MP['h'] + 46
INS = MP['inset']; IW, IH = INS['x1'] - INS['x0'], INS['y1'] - INS['y0']; ISC = 172 / IW; BW, BH = 172, IH * ISC; BX, BY = VW - BW - 8, VH - BH - 8

def defs_svg():
    paths = ''.join(f'<path id="pd-{c}" d="{v["d"]}" vector-effect="non-scaling-stroke"/>' for c, v in MP['prov'].items())
    isl = ''.join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x, y in MP['islands'])
    return (f'<svg class="mdefs" aria-hidden="true" focusable="false" width="0" height="0"><defs>{paths}'
            f'<path id="pd-jd" d="{MP["jd"]}"/><g id="pd-isl">{isl}</g>'
            '<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="8" height="8" style="fill:var(--staple-dao)"/><rect width="4" height="8" style="fill:var(--staple-mai)"/></pattern></defs></svg>')

def map_svg(px, aria, fills=None, extra=''):
    fills = fills or {}
    uses = ''.join(f'<use href="#pd-{c}" class="pv" data-code="{c}"' + (f' style="fill:{fills[c]}"' if c in fills else '') + '/>' for c in MP['prov'])
    lbls = ''.join(f'<text class="lbl" data-code="{c}" x="{ANCHOR[c][0]}" y="{ANCHOR[c][1]}">{esc(PROV[c]["label"])}</text>' for c in CODES)
    return (f'<svg class="cmap" viewBox="0 0 {VW:g} {VH:g}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(aria)}">'
            f'<defs><clipPath id="{px}-ic"><rect x="{INS["x0"]}" y="{INS["y0"]}" width="{IW:.1f}" height="{IH:.1f}"/></clipPath></defs>'
            f'<g id="{px}-layers">{uses}<use href="#pd-jd" class="jd"/><use href="#pd-isl" class="isl"/></g>'
            f'<g class="chg" id="{px}-chg"></g><use class="hov" id="{px}-hov"/>{extra}<g class="lbls">{lbls}</g>'
            f'<g class="inset" transform="translate({BX:.1f} {BY:.1f}) scale({ISC:.4f}) translate({-INS["x0"]} {-INS["y0"]})" clip-path="url(#{px}-ic)">'
            f'<rect class="inset-box" x="{INS["x0"]}" y="{INS["y0"]}" width="{IW:.1f}" height="{IH:.1f}" style="stroke-width:{1.2 / ISC:.2f}"/><use href="#{px}-layers"/></g>'
            f'<text class="inset-title" x="{BX + 6:.1f}" y="{BY + 6:.1f}">南海诸岛</text></svg>')

def fill_css(css): return 'url(#hatch)' if css == 'staple-daomai' else f'var(--{css})'

# ---------- 卷首、导航、论点
def hero():
    H = E2.HERO2; im = IM[H['img']]; b = 'assets/' + H['img']
    title = ''.join(f'<span>{esc(t)}</span>' for t in H['title'])
    sub = ''.join(f'<span>{esc(x)}</span>' for x in H['sub'])
    arrow = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5"/></svg>'
    return f'''<header class="h3" id="top">
  <figure class="h3img"><picture>
    <source media="(max-aspect-ratio: 3/2)" srcset="{b}-s1000.jpg 1000w, {b}-s1600.jpg 1600w" sizes="(min-aspect-ratio: 1/1) 50vw, (min-width: 701px) 72vw, 100vw">
    <img src="assets/{esc(im['file'])}" srcset="{b}-1600.jpg 1600w, {b}-2400.jpg 2400w, {b}-3200.jpg 3200w" sizes="(max-aspect-ratio: 2/1) calc(200vh - 72px), 100vw" alt="{esc(H['alt'])}" width="{im['w']}" height="{im['h']}" fetchpriority="high" decoding="async">
  </picture></figure>
  <div class="h3in wide">
    <p class="h3k rise">{esc(H['kicker'])}</p>
    <h1 class="h3t rise" aria-label="{esc(''.join(H['title']))}">{title}</h1>
    <p class="h3s rise">{sub}</p>
    <div class="h3a rise"><a class="btn" href="{esc(H['cta_href'])}">{esc(H['cta'])}{arrow}</a><span class="h3p">{esc(H['proof'])}</span></div>
  </div>
  <p class="h3cap">{esc(H['cap'])}</p>
</header>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n:02d}</small>{esc(nav)}</a>' for cid, n, nav, _, _ in E2.CHAPTERS)
    links += f'<a href="#end" data-nav="end"><small>末</small>{esc(E2.END_NAV)}</a>'
    links += '<button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="换成深色">夜里读</button>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def tagline_sec():
    lines, k = [], 0
    for ln in E2.TAGLINE.split('/'):
        ws = []
        for w in ln.split('|'):
            key = w.startswith('*'); w = w.lstrip('*')
            ws.append(f'<span class="w{" k" if key else ""}" style="--i:{k}">{esc(w)}</span>'); k += 1
        lines.append('<span class="ln">' + ''.join(ws) + '</span>')
    plain = E2.TAGLINE.replace('|', '').replace('/', '').replace('*', '')
    nums = ''.join(f'<div class="tn"><b>{esc(v)}<small>{esc(u)}</small></b><p>{esc(t)}</p></div>' for v, u, t in E2.NUMS)
    return f'''<section class="tagsec" id="tagsec" aria-label="这一页的论点"><div class="tagstick"><div class="wide">
<p class="tagl" aria-label="{esc(plain)}"><span aria-hidden="true">{''.join(lines)}</span></p>
<div class="tagrest"><p>{esc(E2.TAGREST)}</p><div class="tnums">{nums}</div></div>
</div></div></section>'''

def chead(cid):
    _, n, _, title, lede = next(c for c in E2.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第{CN[n]}章'
    h2 = ''.join(f'<span>{esc(x)}</span>' for x in title.split('/'))
    txt = f'<div class="ptext"><p class="cno">{n:02d} · {label}</p><h2 aria-label="{esc(title.replace("/", ""))}">{h2}</h2><p class="lede">{esc(lede)}</p></div>'
    O = E2.OPENERS.get(cid)
    if not O: return f'<header class="chead fade">{txt}</header>'
    im = IM[O['img']]
    fig = (f'<figure class="pimg"><img src="assets/{esc(im["file"])}" width="{im["w"]}" height="{im["h"]}" style="object-position:{O["pos"]}" '
           f'alt="{esc(im["alt"])}" loading="lazy" decoding="async"><figcaption>{esc(im["cap"])}<span class="cr">{esc(credit_short(im))}</span></figcaption></figure>')
    return f'<header class="chead plate fade">{txt}{fig}</header>'

def lic_short(im):
    s = im['license']
    if 'CC0' in s: return 'CC0'
    if 'PD Mark' in s: return '公有领域（PD Mark）'
    if '无已知版权限制' in s: return '无已知版权限制'
    return '公有领域'
def credit_short(im): return f'{im["author"]}，{lic_short(im)}'

# ---------- 序章舞台
FAM_ORDER = 'ABCDEFGHIJKLMN'
def stage_img(pid):
    im = IM['st-' + pid]
    return dict(src='assets/' + im['file'], w=im['w'], h=im['h'], alt=im['alt'], cap=im['cap'], cr=credit_short(im))

def ch_journey():
    P0, S0, I0 = PER[0], E2.STAGE[PER[0]['id']], stage_img(PER[0]['id'])
    fills = {c: fill_css('fam-' + region_of(0, c)['fam']) for c in CODES}
    modes = ''.join(f'<button type="button" role="radio" data-mode="{k}" aria-checked="{"true" if k == "fam" else "false"}">{esc(t)}</button>' for k, t, _ in E2.MODES)
    marks = ''.join(f'<button type="button" class="rmark" data-step="{i}" tabindex="-1" style="left:{i / (NP - 1) * 100:.3f}%" aria-label="{esc(p["name"])}"><i></i><span><b class="lf">{esc(p["name"])}</b><b class="ls">{esc(p["name"][:2])}</b></span></button>' for i, p in enumerate(PER))
    leg0 = ''.join(f'<li><i style="background:var(--fam-{r["fam"]})"></i><span>{esc(r["name"])}</span><small>{esc("".join(PROV[c]["short"] for c in r["provs"]))}</small></li>' for r in P0['regions'])
    _, n, _, title, lede = E2.CHAPTERS[0]
    return f'''<section class="chap tl" id="journey" aria-label="序章：十个时期">
<header class="tlintro wide fade"><p class="cno">00 · 序章</p><h2>{esc(title)}</h2><p class="lede">{esc(lede)}</p></header>
<div class="tlpin" id="tlpin"><div class="tlstage" id="tlstage">
  <div class="smap" id="smap">{map_svg('sm', '中国省级行政区地图，按所选时期的饮食文化区着色', fills)}</div>
  <div class="tlhud" id="tlhud"><p class="jk"><span id="jkn">第 1 / {NP} 期</span><span class="jks" id="jks"> · {esc(P0["sub"])}</span></p><p class="jname" id="jname">{esc(P0["name"])}</p><p class="jyears" id="jyears">{esc(P0["years"])}</p></div>
  <div class="smodes"><div class="seg" id="smodes" role="radiogroup" aria-label="着色方式">{modes}</div></div>
  <aside class="slegend glass" id="slegend" aria-label="图例"><p class="slegh" id="slegh">{esc(E2.MODES[0][2])}</p><ul id="sleglist">{leg0}</ul></aside>
  <article class="tlcard glass" id="tlcard">
    <p class="tlhd"><span class="tlno" id="tlno">01</span><span id="tlkick">{esc(P0["name"])} · {esc(P0["years"])}</span></p>
    <figure class="tlph"><img id="tlimg" src="{esc(I0["src"])}" width="{I0["w"]}" height="{I0["h"]}" alt="{esc(I0["alt"])}" decoding="async"><figcaption id="tlcap">{esc(I0["cap"])}<span class="cr">{esc(I0["cr"])}</span></figcaption></figure>
    <h3 class="tlhead" id="tlhead">{esc(S0["head"])}</h3>
    <p class="tltext" id="tltext">{esc(S0["text"])}</p>
    <p class="tlchg" id="tlchg" hidden></p>
  </article>
  <div class="stip glass" id="stip" role="status" hidden></div>
  <div class="tlruler glass" id="tlruler" role="slider" tabindex="0" aria-label="时期" aria-valuemin="0" aria-valuemax="{NP - 1}" aria-valuenow="0" aria-valuetext="{esc(P0["name"])}">
    <div class="rtrack" id="rtrack"><i class="rline"></i>{marks}<span class="rhead" id="rhead"><i></i></span></div>
  </div>
</div></div>
<p class="tlnote wide">{esc(E2.STAGE_NOTE)}</p>
</section>'''

# ---------- 列表（两章共用）：透镜分组 + 行内展开
def lens_wrap(key, lenses, cols, groups_html, total, unit):
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if i == 0 else "false"}">{esc(t)}</button>' for i, (k, t) in enumerate(lenses))
    return f'''<div class="lwrap" data-lw="{key}">
<div class="lensbar"><span class="lensk">按</span><div class="lens" role="tablist" aria-label="分组方式">{tabs}</div><span class="lensnote">{total} {unit} · 点一行展开</span></div>
<div class="lcols lcols-{key}" aria-hidden="true">{''.join(f'<span>{esc(c)}</span>' for c in cols)}</div>
<div class="lgrid">{groups_html}</div></div>'''
def lgh(g):
    return (f'<div class="lgh" data-g="{esc(g["k"])}"><div class="lghh"><b>{esc(g["label"])}</b><small>{esc(g.get("sub", ""))}</small></div>'
            + (f'<p>{esc(g["desc"])}</p>' if g.get('desc') else '') + '</div>')

# 第一章：150 条要点
DIM_NAME = {k: t for k, t, _ in E2.DIMS}
LINES = []          # (rid, pi, dim, j, item)
for pi, p in enumerate(PER):
    for dim, _, _ in E2.DIMS:
        for j, it in enumerate(p['dims'][dim]): LINES.append((f'd-{p["id"]}-{dim}-{j}', pi, dim, j, it))
def line_row(rid, pi, dim, j, it):
    p = PER[pi]; src = it.get('src') if it.get('src') not in (None, '', '—') else ''
    facts = (f'<dt>出处</dt><dd>{esc(src)}</dd>' if src else '') + f'<dt>时期</dt><dd>{esc(p["name"])} · {esc(p["years"])} · {esc(p["sub"])}</dd>'
    return f'''<div class="lrow" data-id="{rid}" id="{rid}"><button class="lhead" type="button" aria-expanded="false">
<span class="ldate"><b>{esc(p["name"])}</b><small>{esc(p["years"])}</small></span><span class="lname"><b>{esc(it["h"])}</b><small>{esc(it["t"])}</small></span>
<span class="lkind k-{dim}"><i></i>{esc(DIM_NAME[dim])}</span><span class="lsrc">{esc(src or "—")}</span><span class="lchev" aria-hidden="true"></span></button>
<div class="lmore"><div class="lmore-in"><p class="lwhy">{esc(it["t"])}</p><dl class="lfacts">{facts}</dl><button type="button" class="lgo" data-goto="{pi}">在地图上看{esc(p["name"])} →</button></div></div></div>'''
def lines_groups():
    by_dim = [dict(k=d, label=t, sub=f'{sum(1 for x in LINES if x[2] == d)} 条', desc=desc, ids=[x[0] for x in LINES if x[2] == d]) for d, t, desc in E2.DIMS]
    by_era = [dict(k=p['id'], label=p['name'], sub=f'{p["years"]} · {p["sub"]}', desc=q(p['summary']),
                   ids=[x[0] for d, _, _ in E2.DIMS for x in LINES if x[1] == pi and x[2] == d]) for pi, p in enumerate(PER)]
    return {'dim': by_dim, 'era': by_era}
LG = lines_groups()
def ch_lines():
    rows = {x[0]: line_row(*x) for x in LINES}
    body = ''.join(lgh(g) + ''.join(rows[i] for i in g['ids']) for g in LG['dim'])
    return f'''<section class="chap wide" id="lines" aria-label="第一章：四条线">{chead('lines')}
{lens_wrap('lines', E2.LINES_LENSES, ['时期', '要点', '线索', '出处'], body, len(LINES), '条')}</section>'''

# 第三章：34 个省级行政区
def prov_row(c):
    m, p = DATA['modern'][c], PROV[c]
    tk = taste_of(NP - 1, c)
    strip = ''.join(f'<i style="background:var(--fam-{region_of(i, c)["fam"]})" title="{esc(PER[i]["name"])}：{esc(region_of(i, c)["name"])}"></i>' for i in range(NP))
    hist = ''
    for i, per in enumerate(PER):
        r = region_of(i, c); pn = (DATA['provNotes'].get(c) or {}).get(per['id'])
        hist += (f'<li><i style="background:var(--fam-{r["fam"]})"></i><span class="hp"><b>{esc(per["name"])}</b><small>{esc(per["years"])}</small></span>'
                 f'<span class="hr"><b>{esc(r["name"])}</b>{esc(r["note"])}<span class="ht">口味：{esc(DATA["tastes"][taste_of(i, c)]["name"])} · 主食：{esc(DATA["staples"][staple_of(i, c)]["name"])}</span>'
                 + (f'<span class="hn">{esc(pn)}</span>' if pn else '') +
                 f'</span><button type="button" class="hgo" data-goto="{i}" data-prov="{c}" aria-label="在地图上看{esc(p["name"])}的{esc(per["name"])}">地图</button></li>')
    facts = ''.join(f'<dt>{k}</dt><dd>{esc(v)}</dd>' for k, v in (('代表菜', '、'.join(m['dishes'])), ('口味', m['taste']), ('食材', '、'.join(m['food'])), ('器具', '、'.join(m['tool'])), ('技法', '、'.join(m['tech']))))
    return f'''<div class="lrow prow" data-id="p-{c}" id="p-{c}"><button class="lhead" type="button" aria-expanded="false">
<span class="pnm"><b>{esc(p["name"])}</b><small>{esc(p["short"])} · {esc(m["cuisine"])}</small></span><span class="pstrip" role="img" aria-label="十个时期的菜系家族">{strip}</span>
<span class="ptaste"><i style="background:var(--taste-{tk})"></i>{esc(DATA["tastes"][tk]["name"])}</span><span class="pdish">{esc(" · ".join(m["dishes"][:4]))}</span><span class="lchev" aria-hidden="true"></span></button>
<div class="lmore"><div class="lmore-in"><p class="lwhy">{esc(m["story"])}</p><dl class="lfacts">{facts}</dl><h4 class="hh">十个时期</h4><ol class="phist">{hist}</ol></div></div></div>'''
def provs_groups():
    reg = [dict(k=k, label=t, sub=f'{len(cs)} 个', ids=['p-' + c for c in cs]) for k, t, cs in E2.REGIONS]
    assert sorted(c for _, _, cs in E2.REGIONS for c in cs) == sorted(CODES)
    fam = []
    for f in FAM_ORDER:
        cs = [c for c in CODES if region_of(NP - 1, c)['fam'] == f]
        if cs: fam.append(dict(k=f, label=DATA['families'][f]['name'], sub=f'{len(cs)} 个', ids=['p-' + c for c in cs]))
    tas = []
    for t in DATA['tastes']:
        cs = [c for c in CODES if taste_of(NP - 1, c) == t]
        if cs: tas.append(dict(k=t, label=DATA['tastes'][t]['name'], sub=f'{len(cs)} 个', desc=DATA['tastes'][t]['desc'], ids=['p-' + c for c in cs]))
    return {'region': reg, 'fam': fam, 'taste': tas}
PG = provs_groups()
def ch_provs():
    rows = {'p-' + c: prov_row(c) for c in CODES}
    body = ''.join(lgh(g) + ''.join(rows[i] for i in g['ids']) for g in PG['region'])
    return f'''<section class="chap wide" id="provs" aria-label="第三章：各地沿革">{chead('provs')}
{lens_wrap('provs', E2.PROV_LENSES, ['省级行政区', '十个时期的家族', '今天的口味', '代表菜'], body, len(CODES), '个')}</section>'''

# ---------- 第二章：辣椒
CH = json.load(open(os.path.join(SRC, 'chili.json'), encoding='utf-8'))
RECS = sorted(CH['records'], key=lambda r: (r['year'], r['prov']))
for r in RECS:
    r['cat'] = E2.CHILI_USE[r['use']]
    r['qj'] = r['name_used'].strip() == '秦椒' and '花椒' not in r['quote']
assert sum(r['qj'] for r in RECS) == 10, sum(r['qj'] for r in RECS)
MS = CH['milestones']
Y0, Y1 = E2.CHILI_RANGE
CONF_CLS = {'高': 'h', '中': 'm', '低': 'l'}
def conf(c): return f'<span class="conf c-{CONF_CLS.get(c, "m")}" title="可信度：高 = 原文或两个独立来源一致；中 = 只有一个可靠来源或小有出入；低 = 只见于一篇二手转述">{esc(c)}</span>'
def srcs(ss):
    return '；'.join(f'<a href="{esc(s["u"])}" target="_blank" rel="noopener">{esc(s["t"])}</a>' if s.get('u') else esc(s['t']) for s in ss)
USE_LABEL = {k: t for k, t, _ in E2.CHILI_USE_NAME}
def ch_chili():
    last_year = max(r['year'] for r in RECS)
    pct = lambda y: f'{(y - Y0) / (Y1 - Y0) * 100:.3f}%'
    ticks = ''.join(f'<i class="chtk u-{r["cat"]}{" low" if r["conf"] == "低" else ""}{" qj" if r["qj"] else ""}" style="left:{pct(r["year"])}" data-i="{i}"></i>' for i, r in enumerate(RECS))
    msk = ''.join(f'<i class="chms" style="left:{pct(m["year"])}"></i>' for m in MS if Y0 <= m['year'] <= Y1)
    yl = ''.join(f'<span class="chyl{" minor" if (y // 50) % 2 else ""}" style="left:{pct(y)}">{y}</span>' for y in range(1600, Y1 + 1, 50))
    has = {r['prov'] for r in RECS}
    fills = {c: 'var(--chili-has)' if c in has else 'var(--chili-none)' for c in CODES}
    dots = ''.join(f'<circle class="cdot u-{r["cat"]}{" low" if r["conf"] == "低" else ""}{" qj" if r["qj"] else ""} on" data-i="{i}" cx="{ANCHOR[r["prov"]][0]}" cy="{ANCHOR[r["prov"]][1]}" r="5"/>' for i, r in enumerate(RECS))
    dlab = ''.join(f'<text class="clab" data-i="{i}" x="{ANCHOR[r["prov"]][0]}" y="{ANCHOR[r["prov"]][1]}">{esc(E2.CHILI_LABELS[(r["year"], r["prov"])])}</text>' for i, r in enumerate(RECS) if (r['year'], r['prov']) in E2.CHILI_LABELS)
    extra = f'<g class="cdots">{dots}</g><g class="clabs">{dlab}</g>'
    leg = ''.join(f'<li><i class="sw u-{k}"></i><b>{esc(t)}</b><small>{esc(d)}</small></li>' for k, t, d in E2.CHILI_USE_NAME)
    leg += '<li><i class="sw ring"></i><b>空心圈</b><small>只有一个弱来源</small></li><li><i class="sw has"></i><b>有记录的省</b><small>到当前年份为止</small></li>'
    notes = ''.join(f'<article class="note fade"><h4>{esc(t)}</h4><p>{esc(x)}</p></article>' for t, x in E2.CHILI_NOTES)
    ms = ''.join(f'<li class="fade"><span class="my">{m["year"]}</span><p>{esc(q(m["text"]))}</p>{conf(m["conf"])}</li>' for m in MS)
    rows = ''.join(f'<tr><td>{r["year"]}</td><td>{esc(PROV[r["prov"]]["name"])}</td><td>{esc(q(r["book"]))}<small>{esc(r["era"])}</small></td><td>{esc(r["name_used"] or "—")}</td>'
                   f'<td><i class="sw u-{r["cat"]}"></i>{esc(r["use"])}</td><td>{esc(r["quote"] or "—")}<small>{esc(q(r["note"]))}</small></td><td>{conf(r["conf"])}</td><td class="tsrc">{srcs(r["sources"])}</td></tr>' for r in RECS)
    last = RECS[-1]
    return f'''<section class="chap wide" id="chili" aria-label="第二章：辣椒">{chead('chili')}
<figure class="chfig fade" id="chfig">
  <div class="chmap" id="chmap">{map_svg('cm', '辣椒早期记录的分布图，随年份变化', fills, extra)}<div class="stip glass" id="ctip" role="status" hidden></div></div>
  <div class="chpanel">
    <p class="chy"><b id="chy">{last_year}</b><small>年</small></p>
    <p class="chcount" id="chcount">{len(has)} 个省级行政区有记录 · {len(RECS)} 条</p>
    <div class="chrec" id="chrec" aria-live="polite"><p class="chrh"><b>{last["year"]}</b> · {esc(PROV[last["prov"]]["name"])} · {esc(q(last["book"]))}</p><p class="chrq">{esc(last["quote"] or "（原文未引）")}</p><p class="chrn">{esc(q(last["note"]))}</p></div>
    <p class="chms-now" id="chmsn"></p>
    <label class="chq"><input type="checkbox" id="chq" checked><span class="tg" aria-hidden="true"></span><span>{esc(E2.CHILI_QJ_LABEL)}</span></label>
    <ul class="chleg">{leg}</ul>
  </div>
  <div class="chaxis">
    <button type="button" class="chplay" id="chplay" aria-label="从头播放"><svg viewBox="0 0 16 16" aria-hidden="true"><path class="pl" d="M5 3.5v9l7.5-4.5z"/><path class="pa" d="M5 3.5v9M11 3.5v9"/></svg></button>
    <div class="chtrackw" id="chslider" role="slider" tabindex="0" aria-label="年份" aria-valuemin="{Y0}" aria-valuemax="{Y1}" aria-valuenow="{Y1}" aria-valuetext="{Y1} 年">
      <div class="chtrack" id="chtrack"><i class="chline"></i>{msk}{ticks}{yl}<span class="chhead" id="chhead" style="left:100%"><i></i></span></div>
    </div>
  </div>
  <figcaption class="chcap">每个点是一条早期记录，颜色是原文写的用途；横轴上的细竖线是右下列出的节点。拖动或点播放；← → 跳到上一条、下一条记录。</figcaption>
</figure>
<div class="notes">{notes}</div>
<div class="msec"><header class="msech fade"><h3>{esc(E2.CHILI_MS_HEAD[0])}</h3><p>{esc(E2.CHILI_MS_HEAD[1])}</p></header><ol class="mlist">{ms}</ol></div>
<details class="fold big fade"><summary><h3>28 条记录（表）</h3></summary><div class="tblwrap rtable"><table><thead><tr><th>年份</th><th>省</th><th>书</th><th>名称</th><th>用途</th><th>原文 · 说明</th><th>可信度</th><th>来源</th></tr></thead><tbody>{rows}</tbody></table></div></details>
</section>'''

# ---------- 卷末
USED = [E2.HERO2['img']] + ['st-' + p['id'] for p in PER] + [E2.OPENERS[k]['img'] for k in ('lines', 'chili', 'provs')]
def refs_block():
    out = [f'<h3>古籍与综述（v1）</h3><ul>{"".join(f"<li>{esc(r)}</li>" for r in DATA["refs"])}</ul>']
    for g, items in E2.REFS_MORE:
        out.append(f'<h3>{esc(g)}（{len(items)}）</h3><ul>' + ''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in items) + '</ul>')
    return ''.join(out)
def credits():
    rows = ''.join(f'<tr><td>{esc(k)}</td><td>{esc(IM[k]["subject"])}</td><td>{esc(IM[k]["credit_line"])}</td><td>{esc(lic_short(IM[k]))}</td><td><a href="{esc(IM[k]["source"])}" target="_blank" rel="noopener">原始页面 ↗</a></td></tr>' for k in USED)
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>署名</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'
def endm():
    return f'''<footer class="endm" id="end"><div class="wide">
<h2 class="fade">卷末 · 参考、方法与署名</h2>
<details class="fold big fade"><summary><h3>参考</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{"".join(f"<li>{esc(p)}</li>" for p in E2.METHOD)}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{"".join(f"<li>{esc(t)}</li>" for t in E2.TODO)}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(USED)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">{esc(E2.STAMP[0])}<br>{esc(E2.STAMP[1])}</div>
</div></footer>'''

# ---------- 给 app.js 的数据
def data():
    per = [dict(id=p['id'], name=p['name'], years=p['years'], sub=p['sub'],
                regions=[dict(id=r['id'], fam=r['fam'], name=r['name'], provs=r['provs'], taste=r['taste'], staple=r['staple'], note=r['note']) for r in p['regions']],
                ov=p.get('overrides') or {}) for p in PER]
    stage = [dict(head=E2.STAGE[p['id']]['head'], text=E2.STAGE[p['id']]['text'], img=stage_img(p['id'])) for p in PER]
    recs = [dict(y=r['year'], p=r['prov'], book=q(r['book']), name=r['name_used'], quote=r['quote'], use=r['use'], cat=r['cat'], conf=r['conf'], qj=r['qj'], note=q(r['note']), place=r['place']) for r in RECS]
    return {
        'periods': per, 'prov': {c: dict(name=PROV[c]['name'], short=PROV[c]['short'], label=PROV[c]['label']) for c in CODES},
        'fam': {k: v['name'] for k, v in DATA['families'].items()}, 'tastes': {k: v['name'] for k, v in DATA['tastes'].items()},
        'staples': {k: v['name'] for k, v in DATA['staples'].items()}, 'notes': DATA['provNotes'],
        'stage': stage, 'modes': [[k, t, n] for k, t, n in E2.MODES], 'palmeta': palmeta, 'pbox': PBOX, 'anchor': ANCHOR,
        'chili': {'y0': Y0, 'y1': Y1, 'recs': recs, 'ms': [dict(y=m['year'], t=q(m['text'])) for m in MS], 'useName': USE_LABEL},
        'lens': {'lines': {k: [dict(k=g['k'], label=g['label'], sub=g.get('sub', ''), desc=g.get('desc', ''), ids=g['ids']) for g in v] for k, v in LG.items()},
                 'provs': {k: [dict(k=g['k'], label=g['label'], sub=g.get('sub', ''), desc=g.get('desc', ''), ids=g['ids']) for g in v] for k, v in PG.items()}},
    }

def main():
    shell = rd('shell.html')
    favicon = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%23b5432c'/%3E"
               "%3Ctext x='32' y='44' font-size='34' text-anchor='middle' font-family='Noto Serif SC,Songti SC,serif' font-weight='700' fill='%23fff'%3E味%3C/text%3E%3C/svg%3E")
    body = (hero() + '\n' + cnav() + '\n' + defs_svg() + '\n<main>\n' + tagline_sec() + '\n' + ch_journey() + '\n' + ch_lines() + '\n' + ch_chili() + '\n' + ch_provs() + '\n</main>\n' + endm()
            + '\n<script type="application/json" id="data">' + json.dumps(data(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>')
    page = shell
    for k, v in (('{{TITLE}}', esc(TITLE)), ('{{DESCRIPTION}}', esc(E2.META_DESC)), ('{{CANONICAL}}', SITE_URL), ('{{FAVICON}}', favicon),
                 ('{{PAL_LIGHT}}', css_vars('light')), ('{{PAL_DARK}}', css_vars('dark')), ('{{BODY}}', body), ('{{APP_JS}}', rd('app.js'))):
        assert page.count(k) >= 1, k
        page = page.replace(k, v)
    assert '{{' not in page
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    mpath = os.path.join(ROOT, 'meta.json'); meta = json.load(open(mpath, encoding='utf-8'))
    meta.update({'summary': E2.META_DESC, 'cover_focus': '#top', 'cover_scheme': 'light', 'reading_time': '20 分钟', 'sources': E2.META_SOURCES})
    json.dump(meta, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(mpath, 'a').write('\n')
    print('wrote index.html', f'{len(page.encode("utf-8")) / 1024:.0f} KB', '·', len(E2.DATA_FIX), 'data fixes ·', len(LINES), 'lines ·', len(RECS), 'chili records')

if __name__ == '__main__':
    main()
