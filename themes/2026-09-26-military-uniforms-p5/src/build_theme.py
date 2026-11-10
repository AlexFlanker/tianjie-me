# -*- coding: utf-8 -*-
"""第 2 题 v2（2026-11-10）构建：content.js（UDATA，事实底稿，不改）+ editorial2.py（新写文字）+ images.json（make_images.py 生成）
→ ../index.html 与 ../meta.json。版面系统沿用第 5、8 题：卷首大图、逐词点亮的论点、全屏舞台序章、每章图版开篇、可拖主图、透镜列表、卷末折叠。
python3 build_theme.py"""
import json, os, re, html, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial2 as E

esc = lambda s: html.escape(str(s), quote=True)
ROOT = os.path.join(HERE, '..')

# ---------- 数据
node = "const vm=require('vm'),fs=require('fs');const w={};w.window=w;vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),w);process.stdout.write(JSON.stringify(w.UDATA))"
U = json.loads(subprocess.check_output(['node', '-e', node, os.path.join(HERE, 'content.js')]).decode('utf-8'))
IJ = json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))
IM = IJ['images']
ERAS = U['ERAS']; ERA = {e['k']: e for e in ERAS}
CCS = U['COUNTRIES']; CC = {c['k']: c for c in CCS}
CC_X = dict(CC, de={'k': 'de', 'name': '德国', 'short': '德'}, ca={'k': 'ca', 'name': '加拿大', 'short': '加'})
CATS = U['CATS']; TAGS = U['TAGS']
USED = []

# ---------- 参考编号：〔英3〕 ↔ uk3
GL = {'cn': '中', 'us': '美', 'ru': '俄', 'uk': '英', 'fr': '法', 'de': '德'}
REF = {}
for g, lst in U['REFS'].items():
    for r in lst:
        k = r[0]; lab = ('加' + k[1:]) if k.startswith('x') else GL[g] + re.sub(r'^[a-z]+', '', k)
        REF[k] = dict(k=k, g=g, label=lab, text=r[1], url=r[2])
LAB2KEY = {v['label']: k for k, v in REF.items()}
MISSING_REF = set()
def ref_link(k):
    r = REF.get(k)
    if not r: MISSING_REF.add(k); return ''
    return f'<a class="rf" href="#ref-{k}" title="{esc(r["text"])}">〔{r["label"]}〕</a>'
def linkify(s):
    def rep(m):
        k = LAB2KEY.get(m.group(1)); return ref_link(k) if k else m.group(0)
    return re.sub(r'〔([中美俄英法德加]\d+b?)〕', rep, esc(s))
def conf(c):
    c = c or '中'; k = 'h' if c.startswith('高') else 'l' if c.startswith('低') else 'm'
    return f'<span class="conf {k}">置信度 {esc(c)}</span>'

# ---------- 图片
def author_short(s):
    s = re.sub(r'（.*?）', '', s or '').strip()
    return s if len(s) <= 36 else s[:36] + '…'
def credit(im): return f'图：{author_short(im["author"])}，{im["lic"]}。'
def use(k):
    assert k in IM, '图片未登记：' + k
    if k not in USED: USED.append(k)
    return IM[k]
def figure(k, cls='ph', eager=False):
    im = use(k)
    return (f'<figure class="{cls}"><button type="button" class="zoom" data-full="assets/{esc(im["file"])}" aria-label="放大：{esc(im["cap"])}">'
            f'<img src="assets/{esc(im["file"])}" alt="{esc(im["cap"])}" width="{im["w"]}" height="{im["h"]}" loading="{"eager" if eager else "lazy"}" decoding="async"></button>'
            f'<figcaption><span class="cs">{esc(im["cap"])}</span> <span class="cr">{esc(credit(im))}</span></figcaption></figure>')

def swatches(colors, n=4):
    return ''.join(f'<i style="background:{esc(c[0])}" title="{esc(c[1])}"></i>' for c in colors[:n])

# ---------- 卷首与论点
def hero():
    im = use(IJ['plates']['hero'])
    s = ''.join(f'<span>{esc(x)}</span>' for x in E.HERO_S)
    return (f'<header class="h3 band" id="top"><figure class="h3img"><img src="assets/{esc(im["file"])}" alt="{esc(im["cap"])}" width="{im["w"]}" height="{im["h"]}" fetchpriority="high" decoding="async"></figure>'
            f'<div class="h3scrim" aria-hidden="true"></div>'
            f'<div class="wide h3in"><p class="h3k rise">{esc(E.HERO_K)}</p><h1 class="h3t rise">{esc(E.HERO_T)}</h1><p class="h3s rise">{s}</p>'
            f'<div class="h3a rise"><a class="btn" href="#s0">{esc(E.HERO_BTN)}<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3v10M3.5 8.5 8 13l4.5-4.5"/></svg></a><span class="h3p">{esc(E.HERO_P)}</span></div></div>'
            f'<p class="h3cap">{esc(E.HERO_CAP)} {esc(credit(im))}</p></header>')
def tagline():
    lines = [[]]
    for w in E.THESIS:
        if w == '/': lines.append([])
        else: lines[-1].append(w)
    tl = ''.join('<span class="ln">' + ''.join(f'<span class="w">{esc(w)}</span>' for w in ln) + '</span>' for ln in lines)
    nums = ''.join(f'<div class="tn"><b>{esc(a)}<small>{esc(b)}</small></b><p>{esc(c)}</p></div>' for a, b, c in E.THESIS_NUMS)
    return (f'<section class="tagsec band" id="tagsec" aria-label="论点"><div class="tagstick"><div class="wide"><p class="tagl">{tl}</p>'
            f'<div class="tagrest"><p>{esc(E.THESIS_REST)}</p><div class="tnums">{nums}</div></div></div></div></section>')
def cnav():
    items = [('s0', '00', '八个时代')] + [(k, v['no'], v['nav']) for k, v in E.CH.items()] + [('end', '', '出处')]
    a = ''.join(f'<a href="#{i}" data-nav="{i}">{f"<small>{n}</small>" if n else ""}{esc(t)}</a>' for i, n, t in items)
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{a}<button type="button" class="ntheme" id="theme-btn">白天读</button><span class="prog" id="prog"></span></div></nav>'

# ---------- 序章：全屏舞台
def stage_data():
    out = []
    for e in ERAS:
        k = e['k']; im = use(IJ['stage'][k])
        rows = [dict(cc=c['k'], cn=c['name'], name=U['CELLS'][c['k']][k]['name'], colors=[x[0] for x in U['CELLS'][c['k']][k]['colors'][:4]], row=f'u-{c["k"]}-{k}') for c in CCS]
        out.append(dict(k=k, name=e['name'], range=e['range'], text=E.STAGE_TEXT[k], img='assets/' + im['file'], w=im['w'], h=im['h'], alt=im['cap'], cap=im['cap'], cred=credit(im), rows=rows))
    return out
def stage(SD):
    N = len(SD); s0 = SD[0]
    def rows(s): return ''.join(f'<li><button type="button" data-row="{r["row"]}"><b>{esc(r["cn"])}</b><span class="sw">' + ''.join(f'<i style="background:{esc(c)}"></i>' for c in r['colors']) + f'</span><em>{esc(r["name"])}</em></button></li>' for r in s['rows'])
    marks = ''.join(f'<button type="button" class="rmark{" edge" if i in (0, N - 1) else ""}" data-step="{i}" style="left:{i / (N - 1) * 100:.3f}%" aria-label="{esc(s["name"])}，{esc(s["range"])}"><i></i><span><b>{esc(s["name"])}</b><small>{esc(s["range"])}</small></span></button>' for i, s in enumerate(SD))
    return (f'<section class="tl band" id="s0"><div class="wide tlintro"><p class="cno">{esc(E.STAGE_K)}</p><h2>{esc(E.STAGE_H)}</h2><p class="lede">{esc(E.STAGE_LEDE)}</p></div>'
            f'<div class="tlpin" id="tlpin"><div class="tlstage" id="tlstage">'
            f'<div class="tlbg" aria-hidden="true"><img class="on" id="tlbg0" src="{esc(s0["img"])}" alt=""><img id="tlbg1" alt=""></div>'
            f'<p class="tlhint">{esc(E.STAGE_HINT)}</p>'
            f'<figure class="tlplate"><div class="tlpics" id="tlpics"><img class="on" id="tlp0" src="{esc(s0["img"])}" alt="{esc(s0["alt"])}" width="{s0["w"]}" height="{s0["h"]}" decoding="async"><img id="tlp1" alt="" decoding="async"></div>'
            f'<figcaption class="tlcap" id="tlcap"><span class="cs" id="tlcs">{esc(s0["cap"])}</span> <span class="cr" id="tlcr">{esc(s0["cred"])}</span></figcaption></figure>'
            f'<aside class="tlcard glass" id="tlcard" aria-live="polite"><div class="tlhd"><span class="tlno" id="tlno">01 / {N:02d}</span><span id="tlrange">{esc(s0["range"])}</span></div>'
            f'<h3 class="tlname" id="tlname">{esc(s0["name"])}</h3><p class="tltext" id="tltext">{esc(s0["text"])}</p><ul class="tlrows" id="tlrows">{rows(s0)}</ul></aside>'
            f'<div class="tlruler glass" id="tlruler" role="slider" tabindex="0" aria-label="八个时代：拖动或用方向键" aria-valuemin="0" aria-valuemax="{N - 1}" aria-valuenow="0" aria-valuetext="{esc(s0["name"])}">'
            f'<div class="rin"><div class="rtrack" id="rtrack"><span class="rline"></span>{marks}<span class="rhead" id="rhead"><i></i></span></div></div></div>'
            f'</div></div></section>')

# ---------- 章头
def chead(key, extra=''):
    c = E.CH[key]; im = use(IJ['plates'][key])
    return (f'<div class="chead plate fade"><div class="ptext"><p class="cno">{c["no"]}</p><h2>{esc(c["h"])}</h2><p class="lede">{esc(c["lede"])}</p>{extra}</div>'
            f'<figure class="pimg"><button type="button" class="zoom" data-full="assets/{esc(im["file"])}" aria-label="放大：{esc(im["cap"])}"><img src="assets/{esc(im["file"])}" alt="{esc(im["cap"])}" width="{im["w"]}" height="{im["h"]}" loading="lazy" decoding="async"></button>'
            f'<figcaption>{esc(im["cap"])} {esc(credit(im))}</figcaption></figure></div>')

# ---------- 01 颜色总线
def year_of(s):
    m = re.search(r'(1[5-9]\d\d|20\d\d)', s); return int(m.group(1)) if m else None
def bus_data():
    lanes = []
    for c in CCS:
        segs = [dict(a=s['a'], b=s['b'], t=s['t'], c=s['c'], label=(E.BUS_UNKNOWN if s['t'] == 'unknown' else s['label']), minor=bool(s.get('minor'))) for s in U['BUS']['lanes'][c['k']]]
        lanes.append(dict(cc=c['k'], name=c['name'], short=c['short'], segs=segs))
    marks = []
    for cd in U['CARDS']:
        if cd['cc'] in CC:
            y = year_of(cd['year']); assert y, cd['id']
            marks.append(dict(id='why-' + cd['id'], cc=cd['cc'], y=y, t=cd['title']))
    return dict(lanes=lanes, stages=U['BUS']['stages'], marks=marks, presets=E.BUS_PRESETS, empty=E.BUS_EMPTY, y0=1700, y1=2026, brk=1900, brkf=0.34)
def bus():
    chips = ''.join(f'<button type="button" data-y="{y}">{y}</button>' for y in E.BUS_PRESETS)
    return (f'<div class="tool bus fade" id="bus"><div class="bushd"><div class="busyr"><b id="busy">1914</b><span id="busst"></span></div>'
            f'<div class="buschips" id="buschips" role="group" aria-label="跳到某一年">{chips}<button type="button" class="play" id="busplay" aria-pressed="false">从头放一遍</button></div></div>'
            f'<div class="buswrap" id="buswrap" role="slider" tabindex="0" aria-label="年份：拖动或用方向键" aria-valuemin="1700" aria-valuemax="2026" aria-valuenow="1914"><svg id="bussvg" aria-hidden="true"></svg></div>'
            f'<ul class="busread" id="busread" aria-live="polite"></ul><p class="fnote">{esc(E.BUS_NOTE)}</p></div>')

# ---------- 列表行
def lens_bar(key, lenses, cur, cols):
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == cur else "false"}">{esc(n)}</button>' for k, n in lenses)
    return (f'<div class="lensbar"><span class="lensk">排法</span><div class="lens" role="tablist">{tabs}</div><span class="lensnote"></span></div>'
            f'<div class="lcols" aria-hidden="true">{"".join(f"<span>{esc(c)}</span>" for c in cols)}</div>')
def cell_row(cc, ek):
    c = U['CELLS'][cc][ek]; e = ERA[ek]; rid = f'u-{cc}-{ek}'; pics = IJ['cells'].get(f'{cc}-{ek}', [])
    thumb = ''
    if pics:
        im = use(pics[0]); thumb = f'<span class="lthumb"><img src="assets/{esc(im["file"])}" alt="" loading="lazy" decoding="async" width="{im["w"]}" height="{im["h"]}"></span>'
    else: thumb = '<span class="lthumb none"></span>'
    head = (f'<button type="button" class="lhead" aria-expanded="false" aria-controls="{rid}-m"><span class="ldate"><b>{esc(CC[cc]["name"])}</b><small>{esc(e["name"])} · {esc(e["range"])}</small></span>'
            f'<span class="lname"><b>{esc(c["name"])}</b><small>{esc(c["year"])}</small></span><span class="lsw">{swatches(c["colors"])}</span>{thumb}<span class="lchev" aria-hidden="true"></span></button>')
    cats = ''.join(f'<div><dt>{esc(k["name"])}</dt><dd>{linkify(c[k["k"]])}</dd></div>' for k in CATS if c.get(k['k']))
    cols = ''.join(f'<li><i style="background:{esc(x[0])}"></i>{esc(x[1])}</li>' for x in c['colors'])
    disp = f'<p class="dispute"><b>分歧</b>{linkify(c["dispute"])}</p>' if c.get('dispute') else ''
    note = f'<p class="small">{linkify(c["confNote"])}</p>' if c.get('confNote') else ''
    refs = ''.join(ref_link(r) for r in c.get('refs', []))
    main = (f'<div class="lmain"><p class="ltext">{linkify(c["why"])}</p><dl class="cats">{cats}</dl><ul class="cols">{cols}</ul>{disp}'
            f'<p class="lconf">{conf(c["conf"])} <span class="rfs">出处 {refs}</span></p>{note}</div>')
    ph = ''
    if pics: ph = '<div class="lpics">' + figure(pics[0], 'ph big') + ('<div class="lpics2">' + ''.join(figure(p) for p in pics[1:]) + '</div>' if len(pics) > 1 else '') + '</div>'
    return (f'<div class="lrow" id="{rid}" data-id="{rid}">{head}<div class="lmore" id="{rid}-m"><div class="lmore-in"><div class="lbody{"" if pics else " nophoto"}">{main}{ph}</div></div></div></div>')
def card_row(cd):
    rid = 'why-' + cd['id']; cc = cd['cc']; e = ERA[cd['era']]
    tags = ''.join(f'<i class="tg t-{t}">{esc(TAGS[t]["name"])}</i>' for t in cd['tags'])
    head = (f'<button type="button" class="lhead" aria-expanded="false" aria-controls="{rid}-m"><span class="ldate"><b>{esc(cd["year"])}</b><small>{esc(CC_X[cc]["name"])}</small></span>'
            f'<span class="lname"><b>{esc(cd["title"])}</b></span><span class="ltags">{tags}</span><span class="lchev" aria-hidden="true"></span></button>')
    disp = f'<p class="dispute"><b>分歧</b>{linkify(cd["dispute"])}</p>' if cd.get('dispute') else ''
    refs = ''.join(ref_link(r) for r in cd.get('refs', []))
    jump = f'<p class="jump"><a href="#u-{cc}-{cd["era"]}" data-open="u-{cc}-{cd["era"]}">看这一格：{esc(CC[cc]["name"])} · {esc(e["name"])} →</a></p>' if cc in CC else ''
    main = (f'<div class="lmain"><p class="lk">发生了什么</p><p class="ltext">{linkify(cd["what"])}</p><p class="lk">为什么</p><p class="lwhy">{linkify(cd["why"])}</p>{disp}'
            f'<p class="lconf">{conf(cd["conf"])} <span class="rfs">出处 {refs}</span></p>{jump}</div>')
    pk = IJ['cards'].get(cd['id']); ph = '<div class="lpics">' + figure(pk, 'ph big') + '</div>' if pk else ''
    return f'<div class="lrow" id="{rid}" data-id="{rid}">{head}<div class="lmore" id="{rid}-m"><div class="lmore-in"><div class="lbody{"" if pk else " nophoto"}">{main}{ph}</div></div></div></div>'

def lens_data():
    cells = {'era': [dict(k=e['k'], label=f'{e["name"]} · {e["range"]}', ids=[f'u-{c["k"]}-{e["k"]}' for c in CCS]) for e in ERAS],
             'cc': [dict(k=c['k'], label=c['long'], ids=[f'u-{c["k"]}-{e["k"]}' for e in ERAS]) for c in CCS]}
    cards = U['CARDS']
    tag = [dict(k=t, label=f'{TAGS[t]["name"]} · {TAGS[t]["desc"]}', ids=['why-' + c['id'] for c in cards if c['tags'][0] == t]) for t in ('combat', 'tech', 'politics', 'culture')]
    cc = [dict(k=c['k'], label=c['name'], ids=['why-' + x['id'] for x in cards if x['cc'] == c['k']]) for c in CCS]
    cc.append(dict(k='x', label='五常之外（德国、加拿大）', ids=['why-' + x['id'] for x in cards if x['cc'] not in CC]))
    era = [dict(k=e['k'], label=f'{e["name"]} · {e["range"]}', ids=['why-' + x['id'] for x in cards if x['era'] == e['k']]) for e in ERAS]
    for grp in (tag, cc, era): assert sum(len(g['ids']) for g in grp) == len(cards)
    return {'cells': cells, 'cards': {'era': era, 'tag': [g for g in tag if g['ids']], 'cc': [g for g in cc if g['ids']]}}

def flows():
    rows = ''.join(f'<li><span class="fy">{esc(f["year"])}</span><span class="fd"><b>{esc(f["from"])}</b><i aria-hidden="true">→</i><b>{esc(f["to"])}</b></span><span class="fw">{linkify(f["what"])} {conf(f["conf"])} <span class="rfs">{"".join(ref_link(r) for r in f.get("refs", []))}</span></span></li>' for f in U['FLOWS'])
    return f'<div class="sec fade" id="flows"><div class="sech"><h3>{esc(E.C3_FLOW_H)}</h3><p>{esc(E.C3_FLOW_LEDE)}</p></div><ul class="flows">{rows}</ul></div>'

# ---------- 卷末
def endm():
    th = ''.join(f'<th>{esc(c["name"])}</th>' for c in CCS)
    trs = ''.join(f'<tr><td><b>{esc(k["name"])}</b><small>{esc(k["def"])}</small></td>' + ''.join(f'<td>{esc(k["names"][c["k"]])}</td>' for c in CCS) + '</tr>' for k in CATS)
    cats = f'<details class="fold big"><summary><h3>四类着装在各国条例里叫什么</h3></summary><div class="tscroll"><table class="catt"><thead><tr><th>本页归类</th>{th}</tr></thead><tbody>{trs}</tbody></table></div></details>'
    meth = '<details class="fold big"><summary><h3>方法与口径</h3></summary><div class="method">' + ''.join(f'<p><b>{esc(a)}</b>{esc(b)}</p>' for a, b in E.METHOD) + '</div></details>'
    refs = ''
    for g, lst in U['REFS'].items():
        refs += f'<h3>{esc(CC_X[g]["name"] if g in CC_X else g)}</h3><ul>' + ''.join(
            f'<li id="ref-{r[0]}"><b>〔{REF[r[0]]["label"]}〕</b> ' + (f'<a href="{esc(r[2])}" target="_blank" rel="noopener">{esc(r[1])}</a>' if r[2] else esc(r[1])) + '</li>' for r in lst) + '</ul>'
    n_ref = sum(len(v) for v in U['REFS'].values())
    refs = f'<details class="fold big" id="refs"><summary><h3>参考（按国家分组，{n_ref} 条）</h3></summary><div class="refs">{refs}</div></details>'
    rows = ''
    for k in USED:
        im = IM[k]
        rows += (f'<tr><td>{esc(im["cap"])}</td><td>{esc(im["author"])}<br>{esc(im["inst"])}，{esc(im["year"])}</td>'
                 f'<td><a href="{esc(im["lic_url"])}" target="_blank" rel="noopener">{esc(im["lic"])}</a></td><td><a href="{esc(im["src"])}" target="_blank" rel="noopener">来源页</a></td></tr>')
    cred = (f'<details class="fold big" id="credits"><summary><h3>图片署名（{len(USED)} 张）</h3></summary><p class="small">{esc(E.CREDITS_LEDE)}</p>'
            f'<div class="tscroll credits"><table><thead><tr><th>图</th><th>作者 / 馆藏</th><th>许可</th><th>来源</th></tr></thead><tbody>{rows}</tbody></table></div></details>')
    return f'<footer class="endm" id="end"><div class="wide"><h2>{esc(E.END_H)}</h2>{cats}{meth}{refs}{cred}<p class="foot">{esc(E.FOOT)}</p></div></footer>'

# ---------- 组装
def build():
    SD = stage_data()
    cells_rows = ''.join(cell_row(c['k'], e['k']) for e in ERAS for c in CCS)
    cards_rows = ''.join(card_row(cd) for cd in U['CARDS'])
    L = lens_data()
    body = (hero() + tagline() + cnav() + '<main>' + stage(SD)
            + f'<section class="chap" id="c1"><div class="wide">{chead("c1")}{bus()}</div></section>'
            + f'<section class="chap" id="c2"><div class="wide">{chead("c2")}<div class="lwrap" data-lw="cells">'
              + lens_bar('cells', [('era', '按时代'), ('cc', '按国家')], 'era', ['国家 · 时代', '代表性军服', '主色', '', '']) + f'<div class="lgrid">{cells_rows}</div></div><p class="fnote">{esc(E.C2_NOTE)}</p></div></section>'
            + f'<section class="chap" id="c3"><div class="wide">{chead("c3")}<div class="lwrap nothumb" data-lw="cards">'
              + lens_bar('cards', [('era', '按时代'), ('tag', '按动机'), ('cc', '按国家')], 'era', ['年份 · 国家', '转折点', '动机', '']) + f'<div class="lgrid">{cards_rows}</div></div>{flows()}</div></section>'
            + '</main>' + endm()
            + '<dialog class="lb" id="lb" aria-label="大图"><button type="button" class="lbx" id="lbx" aria-label="关闭">×</button><img id="lbimg" alt=""><p id="lbcap"></p></dialog>')
    data = dict(stage=SD, bus=bus_data(), lens=L, lensName={'cells': {'era': '时代', 'cc': '国家'}, 'cards': {'era': '时代', 'tag': '第一动机', 'cc': '国家'}})
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
    dj = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    page = tpl
    for k, v in (('{{TITLE}}', esc(E.TITLE)), ('{{DESCRIPTION}}', esc(E.META_DESC)), ('{{BODY}}', body), ('{{DATA_JSON}}', dj), ('{{APP_JS}}', app)):
        assert page.count(k) >= 1, '模板缺占位：' + k
        page = page.replace(k, v)
    audit(page, L)
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    old = json.load(open(os.path.join(ROOT, 'meta.json'), encoding='utf-8'))
    n_new = sum(1 for k in USED if IM[k]['batch'] == 'v2')
    meta = dict(no=old['no'], slug=old['slug'], title=E.TITLE, subtitle=E.META_SUBTITLE, date=old['date'], summary=E.META_DESC, tags=old['tags'], format='图谱', cover='cover.png',
                cover_focus='#top', cover_scheme='dark', reading_time=E.META_READING,
                sources=old['sources'][:7] + [f'图片 {len(USED)} 张：大都会博物馆、克利夫兰美术馆、巴黎博物馆联盟等开放获取馆藏，美国国会图书馆，美国国家档案馆与国防部影像库，布朗大学 Anne S.K. Brown 军事收藏，Wikimedia Commons；逐张署名见页面卷末与 src/images.json'])
    json.dump(meta, open(os.path.join(ROOT, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'wrote index.html {len(page)} chars; images used {len(USED)} ({n_new} new); cells without image:', [k for k in (f'{c["k"]}-{e["k"]}' for e in ERAS for c in CCS) if not IJ['cells'].get(k)])

def audit(page, L):
    # 图片：登记了就要用上，用上的文件要在
    for k in IM:
        assert k in USED, '登记未用：' + k
    for k in USED:
        im = IM[k]; assert os.path.exists(os.path.join(ROOT, 'assets', im['file'])), '缺文件：' + im['file']
        assert im['lic_url'].startswith('http') and im['src'].startswith('http') and im['author'] and im['lic'], '授权信息不全：' + k
    for fn in os.listdir(os.path.join(ROOT, 'assets')):
        assert any(IM[k]['file'] == fn for k in USED), 'assets 里有没用到的文件：' + fn
    assert not MISSING_REF, '参考编号缺失：' + str(MISSING_REF)
    # 行数
    assert page.count('class="lrow"') == 40 + len(U['CARDS']), page.count('class="lrow"')
    ids = re.findall(r' id="([^"]+)"', page); dup = {i for i in ids if ids.count(i) > 1}; assert not dup, '重复 id：' + str(dup)
    for m in re.findall(r'href="#([^"]+)"', page): assert m in ids, '锚点悬空：' + m
    for g in L.values():
        for grp in g.values():
            for x in grp:
                for i in x['ids']: assert i in ids, i
    # 文字
    text = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>', ' ', page)
    for bad in ('台湾', '臺灣', '台灣', 'Taiwan', '车、表、球', '吃喝玩乐', '示意图', 'TODO', '待核实', '（待补', 'undefined', 'None', '{{'):
        assert bad not in text, '不该出现：' + bad + ' … ' + text[max(0, text.find(bad) - 30):text.find(bad) + 30]
    for bad in ('值得一提', '不难发现', '让我们', '总而言之', '综上所述', '众所周知', '本文将', '笔者'):
        assert bad not in text, '编辑腔：' + bad
    assert 'uniform-fig' not in page and 'UFIG' not in page

if __name__ == '__main__':
    build()
