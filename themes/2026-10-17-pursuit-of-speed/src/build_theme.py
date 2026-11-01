#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 5 题「速度的阶梯」v2（2026-10-30 起，按第 7 题 v3 的版面系统连结构一起重排）：
research/*.json + editorial.py（v1 文案与数据）+ editorial2.py（v2 的章节、短句与图注）+ images.json → ../index.html 与 ../meta.json。
用法（仓库根目录）：python3 themes/2026-10-17-pursuit-of-speed/src/build_theme.py
"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial as E
import editorial2 as E2
import figs, fixes, journey, demos, stage

def esc(s): return html.escape(str(s), quote=True)
def J(name): return json.load(open(os.path.join(HERE, 'research', name), encoding='utf-8'))
A, B, C = J('matrix_A.json'), J('matrix_B.json'), J('cards_C.json')
H = J('harness_D.json')
for _l in fixes.patch_data(A, B, C): print('data', _l)
IM = {i['id']: i for i in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8')) if i.get('status') == 'ok'}

CELLS = {}
for c in A['cells'] + B['cells']: CELLS[(c['track'], c['era'])] = c
WALLS = {w['id']: w for w in A['wall'] + B['wall']}
NOW = {n['id']: n for n in C['now']}
CONF_CLS = {'高': 'h', '中': 'm', '低': 'l'}
CN_NUM = '零一二三四五六七八九十'
def cn_count(n): return (CN_NUM[n // 10] if n >= 20 else '') + ('十' if n >= 10 else '') + (CN_NUM[n % 10] if n % 10 else '') if n >= 10 else CN_NUM[n]

def conf(c): return f'<span class="conf {CONF_CLS.get(c, "m")}" title="资料置信度：高 = 认证机构或官方一手；中 = 只有媒体、博物馆或维基；低 = 推算或通行说法">置信度 {esc(c or "中")}</span>'
def srcs(ss, cls='src', n=8):
    if not ss: return ''
    seen, uniq = set(), []
    for s in ss:
        k = s.get('u') or s['t']
        if k in seen: continue
        seen.add(k); uniq.append(s)
    return f'<p class="{cls}">来源：' + '；'.join(f'<a href="{esc(s["u"])}" target="_blank" rel="noopener">{esc(s["t"])}</a>' if s.get('u') else esc(s['t']) for s in uniq[:n]) + '</p>'
def fmt(v): return figs.fmt(v)
def caption_of(img_id, im): return E2.CAPTION_FIX.get(img_id) or E.CAPTIONS.get(img_id, im.get('caption', ''))
def capspan(img_id, n=96):
    im = IM[img_id]; s = caption_of(img_id, im); s = s[:n] + '…' if len(s) > n else s
    return f'<span class="cs">{esc(s)}</span><span class="cr">{esc(stage.credit(im))}</span>'

def src_lookup_raw(key):
    parts = key.split(':'); obj = None
    if parts[0] == 'scale': obj = next((s for s in B['scale'] if s['id'] == parts[1]), None)
    elif parts[0] == 'cell':
        t, e = parts[1].split('-'); obj = CELLS.get((t, int(e)))
        if obj and len(parts) > 2 and parts[2] == 'also': obj = obj.get('also')
    return obj
def src_lookup(key):
    obj = src_lookup_raw(key)
    if not obj: return '', ''
    return srcs(obj.get('sources'), n=3), conf(obj.get('conf'))

# ---------- 卷首（v2：全幅实拍 + 标题 + 一个动作）
def hero():
    Hh = E.HERO2; im = IM[Hh['img']]; b = 'assets/' + Hh['img']
    sub = ''.join(f'<span>{esc(x)}</span>' for x in Hh['sub'])
    arrow = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5"/></svg>'
    return f'''<header class="h3 band" id="top">
  <figure class="h3img"><picture>
    <source media="(max-aspect-ratio: 4/5)" srcset="{b}-p960.jpg 960w, {b}-p1440.jpg 1440w" sizes="(max-aspect-ratio: 9/16) 57vh, 100vw">
    <img src="assets/{esc(im['file'])}" srcset="{b}-1600.jpg 1600w, {b}-2400.jpg 2400w, {b}-3200.jpg 3200w" sizes="(max-aspect-ratio: 2/1) calc(200vh - 72px), 100vw" alt="{esc(Hh['alt'])}" width="{im['w']}" height="{im['h']}" fetchpriority="high" decoding="async">
  </picture></figure>
  <div class="h3in wide">
    <p class="h3k rise">{esc(Hh['kicker'])}</p>
    <h1 class="h3t rise">{esc(Hh['title'])}</h1>
    <p class="h3s rise">{sub}</p>
    <div class="h3a rise"><a class="btn" href="{esc(Hh['cta_href'])}">{esc(Hh['cta'])}{arrow}</a><span class="h3p">{esc(Hh['proof'])}</span></div>
  </div>
  <p class="h3cap">{esc(Hh['cap'])}</p>
</header>'''

def tagline_sec():
    lines, k = [], 0
    for ln in E.TAGLINE.split('/'):
        ws = []
        for w in ln.split('|'):
            ws.append(f'<span class="w" style="--i:{k}">{esc(w.rstrip())}</span>' + (' ' if w.endswith(' ') else '')); k += 1
        lines.append('<span class="ln">' + ''.join(ws) + '</span>')
    nums = ''.join(f'<div class="tn"><b>{esc(v)}<small>{esc(u)}</small></b><p>{esc(t)}</p></div>' for v, u, t in E.NUMS)
    return f'''<section class="tagsec band" id="tagsec" aria-label="这一页的论点"><div class="tagstick"><div class="wide">
<p class="tagl" aria-label="{esc(E.TAGLINE.replace('|', '').replace('/', ''))}"><span aria-hidden="true">{''.join(lines)}</span></p>
<div class="tagrest"><p>{esc(E.TAGREST)}</p><div class="tnums">{nums}</div></div>
</div></div></section>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n:02d}</small>{esc(t)}</a>' for cid, n, t, _ in E2.CHAPTERS)
    links += f'<a href="#end" data-nav="end"><small>末</small>{esc(E2.END_NAV)}</a>'
    links += '<button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="切换深浅色">白天读</button>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E2.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第{"一二三四五六七八"[n-1]}章'
    txt = f'<div class="ptext"><p class="cno">{n:02d} · {label}</p><h2>{esc(t)}</h2><p class="lede">{esc(lede)}</p></div>'
    O = E2.OPENERS.get(cid)
    if not O: return f'<header class="chead fade">{txt}</header>'
    im = IM[O['img']]
    fig = (f'<figure class="pimg"><img src="assets/{esc(im["file"])}" width="{im["w"]}" height="{im["h"]}" alt="{esc(O["alt"])}" loading="lazy" decoding="async">'
           f'<figcaption>{esc(O["cap"])}</figcaption></figure>')
    return f'<header class="chead plate fade">{txt}{fig}</header>'

def sech(k, title, lede=''):
    return f'<header class="sech fade"><span class="k">{esc(k)}</span><h3>{esc(title)}</h3>' + (f'<p>{esc(lede)}</p>' if lede else '') + '</header>'

# ---------- 序章：十九级阶梯（全屏舞台）
def ch_journey():
    _, n, t, lede = E2.CHAPTERS[0]
    intro = f'<header class="tlintro wide fade"><p class="cno">00 · 序章</p><h2>{esc(t)}</h2><p class="lede">{esc(lede)}</p></header>'
    return (f'<section class="chap tl band" id="journey" aria-label="序章 · 十九级阶梯">{intro}{stage.stage(IM, caption_of, src_lookup)}'
            f'<p class="tlnote">{esc(E2.STAGE_NOTE)}</p></section>')

# ---------- 第一章 这一周
KIND_CLS = {'宣称': 'claim', '实测': 'meas', '官方': 'off', '设计值': 'des', '媒体转述': 'med', '厂商宣称': 'claim'}
def kind_cls(k):
    for key, cls in KIND_CLS.items():
        if (k or '').startswith(key): return cls
    return 'note'
def now_item(nid):
    if nid == 'anniv':
        li = ''.join(f'<li><span class="ny">{esc(d)}</span><span>{esc(t)}</span></li>' for d, t in E2.ANNIVS)
        return (f'<article class="nitem fade"><div class="nd"><b>10/14 · 10/15</b><small>本周的两个纪念日</small></div><div class="nb"><h3>两个「音障日」，外加一次自由落体</h3>'
                f'<ul class="nann">{li}</ul><div class="nfoot">{srcs(E2.ANNIV_SRC)}</div></div></article>')
    n = NOW[nid]
    claims = ''.join(f'<li><b>{esc(c["k"])}</b><span>{esc(c["v"])}</span><i class="tag {kind_cls(c.get("kind"))}">{esc(c.get("kind", "宣称"))}</i></li>' for c in n.get('claims', []))
    disp = f'<p class="dispute"><b>质疑 / 分歧</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    return (f'<article class="nitem fade" id="now-{esc(nid)}"><div class="nd"><b>{esc(E2.NOW_DATE.get(nid, ""))}</b><small><span>{esc(n["date"])}</span></small></div>'
            f'<div class="nb"><h3>{esc(n["title"])}</h3><p class="nt">{esc(n["text"])}</p><ul class="claims">{claims}</ul>{disp}'
            f'<div class="nfoot">{srcs(n.get("sources"))}{conf(n.get("conf"))}</div></div></article>')
def ch_now():
    return f'<section class="chap" id="now"><div class="wide">{chead("now")}<div class="nlist">{"".join(now_item(i) for i in E2.NOW_ORDER)}</div></div></section>'

# ---------- 第二章 五条赛道（主图：JS 按实际宽度画）
def ch_tracks():
    F = E2.TRACKS_FIG
    chips = '<button type="button" data-tk="" aria-pressed="true">全部</button>' + ''.join(f'<button type="button" data-tk="{tid}" aria-pressed="false">{esc(E2.TRACK_SHORT[tid])}</button>' for tid, _, _ in E.TRACKS)
    return f'''<section class="chap" id="tracks"><div class="wide">{chead("tracks")}
<div class="sec" id="tracks-sec">{sech("主图 · 点赛道名或任何一个点", F["title"], F["lede"])}
<div class="tkw fade"><div class="tkmain"><div class="rchips tkchips" id="tkchips" role="group" aria-label="只看一条赛道">{chips}</div>
<div class="tkbox" id="tkbox"><svg class="tksv" id="tksv" role="img" aria-label="六条赛道在八个时代的最快代表，纵轴对数"></svg></div></div>
<aside class="mxd" id="mxd" data-first="road-6" aria-live="polite"></aside></div>
<p class="fnote">{esc(F["note"])}</p></div>
</div></section>'''

# ---------- 第三章 两条线
def year0(s):
    if isinstance(s, int): return s
    import re as _re
    m = _re.match(r'\d{4}', str(s)); return int(m.group(0)) if m else 0
def line_series():
    """红线 = 人类坐过的最快：研究底稿的纪录线、普通乘客的日常线、第二章里的载人格子（含「同格另一条」）与 E2.REC_ADD 合在一起，逐年累计最大；
    黑线 = 普通乘客当时能坐到的最快（日常线去掉地面高铁的 2008、2017 两点，2026 年仍是 900）；高铁单列成空心点。"""
    cand = []
    for p in B['record_line']: cand.append(dict(year=p['year'], kmh=p['kmh'], label=p['label'], conf=p.get('conf'), note=p.get('note', ''), sources=p.get('sources', [])))
    for p in C['daily_line']: cand.append(dict(year=p['year'], kmh=p['kmh'], label=p['label'], conf=p.get('conf'), note=p.get('note', ''), sources=p.get('sources', [])))
    for (t, e), c in CELLS.items():
        if c.get('subject') == '—' or (t, e) in (('space', 4), ('space', 7)): continue  # Sputnik、帕克探测器无人
        cand.append(dict(year=year0(c.get('year')), kmh=c['kmh'], label=c['subject'], conf=c.get('conf'), note=c.get('speed', ''), sources=c.get('sources', [])))
        al = c.get('also')
        if al and al.get('kmh') and '无人' not in (al.get('subject', '') + al.get('speed', '')):
            cand.append(dict(year=year0(al.get('year')), kmh=al['kmh'], label=al['subject'], conf=al.get('conf'), note=al.get('speed', ''), sources=al.get('sources', [])))
    cand += [dict(a) for a in E2.REC_ADD]
    cand = sorted([x for x in cand if x['year'] and x['kmh']], key=lambda x: (x['year'], -x['kmh']))
    rec, mx = [], 0
    for x in cand:
        if x['kmh'] > mx: rec.append(x); mx = x['kmh']
    art = next(dict(p) for p in B['record_line'] if p['year'] == 2026)
    hsr_years = {y for y, _, _, k in E2.HSR_POINTS if k.startswith('daily:')}
    day = []
    for p in sorted(C['daily_line'], key=lambda p: p['year']):
        if p['year'] in hsr_years: continue
        p = dict(p)
        if p['year'] == 2026: p.update(E2.DAY_2026)
        day.append(p)
    hsr = []
    for y, v, n, k in E2.HSR_POINTS:
        if k.startswith('daily:'): p = dict(next(q for q in C['daily_line'] if q['year'] == int(k[6:]))); p['label'] = n + ' ' + str(v)
        else:
            t, e = k[5:].split('-'); c = CELLS[(t, int(e))]; p = dict(year=y, kmh=v, label=c['subject'], conf=c.get('conf'), note=c.get('speed', ''), sources=c.get('sources', []))
        p['year'], p['kmh'], p['n'] = y, v, n; hsr.append(p)
    return rec, art, day, hsr
def ch_lines():
    F = E2.LINES_FIG
    rec, art, day, hsr = line_series()
    rec = rec + [art]
    def li(p):
        yr = '前 1800' if p['year'] < 1800 else str(p['year'])
        return f'<li><span class="y">{yr}</span><span>{esc(p["label"])} {conf(p.get("conf"))}</span><span class="v">{fmt(p["kmh"])} km/h</span><p>{esc(re.sub(r"^口径[：:]\s*", "", p.get("note","")))}</p></li>'
    tiles = []
    for it in E.COUNTER['items']:
        vis = {'bar': '<div class="cvis bar"><i><b></b></i></div>', 'gauge': '<div class="cvis gauge2"><svg viewBox="0 0 120 70"><path class="g-track" d="M10 65 A50 50 0 0 1 110 65"/><path class="g-red" d="M60 15 A50 50 0 0 1 110 65"/><line class="cn" x1="60" y1="65" x2="60" y2="20" style="transform-origin:60px 65px"/></svg></div>',
               'launch': '<div class="cvis strip"><i class="lane"></i><b class="dot"></b></div>', 'mach': '<div class="cvis machbar"><i></i><b></b><span>Mach 1</span></div>'}[it['kind']]
        tiles.append(f'<div class="ctile fade" data-kind="{it["kind"]}" data-v="{it["v"]}" data-max="{it["max"]}" data-mark="{it.get("mark","")}"><div class="k">{esc(E2.COUNTER_K.get(it["k"], it["k"]))}</div><div class="v"><b class="cnt" data-to="{it["v"]}" data-dec="{it["dec"]}">0</b><small>{esc(it["unit"])}</small></div>{vis}<p class="cd">{esc(it["d"])}</p></div>')
    read = ''.join(f'<div><b id="{i}">—</b><span id="{i}-s">{esc(l)}</span></div>' for i, l in (('ln-rv', '人类坐过的最快'), ('ln-dv', '普通乘客能坐到的最快'), ('ln-x', '两条线差几倍')))
    return f'''<section class="chap" id="lines"><div class="wide">{chead("lines")}
<div class="sec" id="lines-sec">{sech("主图 · 拖动竖线或按播放", F["title"], F["lede"])}
<div class="lnw fade"><div class="lnctl"><button type="button" class="dgo" id="ln-play"><span aria-hidden="true">▶</span> 播放 1800 → 2026</button><p class="lnyr"><b id="ln-y">2026</b></p></div>
<div class="lnbox" id="lnbox" tabindex="0" role="slider" aria-label="两条线：拖动竖线换年份，方向键一年，Shift 加方向键十年" aria-valuemin="1800" aria-valuemax="2026" aria-valuenow="2026" aria-valuetext="2026 年"><svg class="lnsv" id="lnsv" aria-hidden="true"></svg><p class="lflash" id="ln-flash" aria-live="polite"></p></div>
<div class="dread lnread">{read}</div>
<div class="lkey"><span><i class="k1"></i>人类坐过的最快（载人纪录）</span><span><i class="k2"></i>普通乘客当时能坐到的最快（商业运营）</span><span><i class="k4"></i>地面高铁（商业运营，单列）</span><span><i class="k3"></i>协和 1976–2003</span></div></div>
<p class="fnote">{esc(F["note"])}</p>
<details class="fold big fade"><summary><h3>数据表 · 两条线逐点口径与来源</h3></summary><div class="cols2"><div><h4>红线 · 人类坐过的最快</h4><ul class="pts">{''.join(li(p) for p in rec)}</ul>{srcs([s for p in rec for s in p.get('sources', [])][:6])}</div><div><h4>黑线 · 普通乘客当时能坐到的最快</h4><ul class="pts day">{''.join(li(p) for p in day)}</ul>{srcs([s for p in day for s in p.get('sources', [])][:6])}<h4>空心点 · 地面高铁</h4><ul class="pts day">{''.join(li(p) for p in hsr)}</ul>{srcs([s for p in hsr for s in p.get('sources', [])][:6])}</div></div></details>
</div>
<div class="sec" id="counter-sec">{sech("反例，并列", "停住的，和没停住的", E2.COUNTER_LEDE)}<div class="ctiles">{''.join(tiles)}</div></div>
</div></section>'''

# ---------- 第四章 撞墙
def ch_walls():
    order = ['tyre', 'rail', 'water', 'air', 'g', 'light']
    out = []
    for wid in order:
        w = WALLS[wid]
        br = ''.join(f'<li>{esc(x)}</li>' for x in w.get('breakthroughs', []))
        out.append(f'''<article class="wall fade" id="wall-{wid}"><header class="whd"><h3>{esc(w['title'])}</h3><p class="wf">{esc(w['formula'])}</p></header>
{demos.WALL_DEMOS[wid]()}
<details class="fold"><summary>这面墙是怎么回事、谁撞过、怎么绕过去 {conf(w.get('conf'))}</summary><p>{esc(w['text'])}</p><h4>突破手段</h4><ul>{br}</ul><p class="ex"><b>今天的例子</b>{esc(w.get('example',''))}</p>{srcs(w.get('sources'))}</details></article>''')
    snd = '<div class="snd fade"><button type="button" id="snd-btn" aria-pressed="false">声音：关</button><span>打开后撞墙有音爆、跳火、ABS 的点击（程序合成，没有采样）。</span></div>'
    return f'<section class="chap" id="walls"><div class="wide">{chead("walls")}{snd}<div class="walls">{"".join(out)}</div></div></section>'

# ---------- 透镜列表（驾驭 / 为什么要快）
def lens_bar(lenses, label, total, first):
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == first else "false"}">{esc(t)}</button>' for k, t in lenses)
    return f'<div class="lensbar fade"><span class="lensk">按</span><div class="lens" role="tablist" aria-label="{esc(label)}">{tabs}</div><span class="lensnote">{cn_count(total)}行 · 点一行展开</span></div>'
def lens_body(groups, rows):
    return ''.join(f'<div class="lgh" data-g="{g["k"]}"><b>{esc(g["label"])}</b><small>{len(g["ids"])} 行</small></div>' + ''.join(rows[i] for i in g['ids']) for g in groups)

HARNESS_IMG = {'x15-rcs': 'x15', 'apollo-reentry': 'apollo_cm', 'falcon9-landing': 'falcon9', 'thrust-ssc': 'thrustssc', 'three-point-hydroplane': 'spiritoz',
               'f1-aero': 'f1_ground', 'relaxed-stability': 'x29', 'sr71-unstart': 'sr71', 'rail-pantograph-tilt-maglev': 'maglev_l0', 'human-g-limit': 'stapp2',
               'animal-control': 'cheetah', 'concorde-cg': 'concorde'}
NUM_CLS = {'宣称': 'claim', '实测': 'meas', '官方': 'off', '设计值': 'des'}
def harness_row(c):
    measure, demo = E.MEASURE.get(c['id'], (c['title'], ''))
    img = HARNESS_IMG.get(c['id']); im = IM.get(img) if img else None
    dm = demos.H_DEMOS[demo]() if demo else ''
    nums = ''.join(f'<div><span>{esc(n["k"])}</span><b>{esc(n["v"])}</b><i class="tag {NUM_CLS.get(n.get("kind"), "off")}">{esc(n.get("kind", ""))}</i></div>' for n in c.get('numbers', [])[:(8 if c['id'] == 'roadster-2026' else 4)])
    thumb = f'<span class="lthumb"><img src="assets/{esc(im["file"])}" alt="" loading="lazy"></span>' if im else '<span class="lthumb none"></span>'
    ph = f'<figure class="lph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{capspan(img, 72)}</figcaption></figure>' if (im and not demo) else ''
    link = f'<p class="hlink">{esc(c["link"])}</p>' if c.get('link') else ''
    yr = E2.HARNESS_SHORT_YEAR.get(c['id'], c['year'])
    return f'''<article class="lrow" id="h-{esc(c['id'])}" data-id="{esc(c['id'])}">
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(c['id'])}">
<span class="ldate"><b>{esc(yr)}</b></span>
<span class="lname"><b>{esc(measure)}</b><small>{esc(c['title'])}</small></span>
<span class="lkind">{esc(c['domain'])}</span><span class="lerr">{'<i class="dmk">有演示</i>' if demo else ''}</span>
{thumb}<span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(c['id'])}" role="region" aria-label="{esc(measure)}"><div class="lmore-in">
<div class="lbody{'' if ph else ' nophoto'}"><div class="lmain">{dm}<div class="nnums">{nums}</div></div>{ph}</div>
<details class="fold"><summary>失控的原因、解法、代价与来源 {conf(c.get('conf'))}</summary><p class="hprob"><b>失控的原因</b>{esc(c['problem'])}</p><p class="hsol"><b>解法</b>{esc(c['solution'])}</p><p class="hcost"><b>代价 / 争议</b>{esc(c['cost'])}</p>{link}{srcs(c.get('sources'))}</details>
</div></div></article>'''
def harness_groups():
    ids = [c['id'] for c in H['cards']]; byid = {c['id']: c for c in H['cards']}
    order = lambda xs: sorted(xs, key=lambda i: (year0(byid[i]['year']), i))
    dom = [dict(k=k, label=l, ids=order([i for i in ids if byid[i]['domain'] in ds])) for k, l, ds in E2.HARNESS_DOMAIN]
    era = [dict(k=k, label=l, ids=order([i for i in ids if lo <= year0(byid[i]['year']) < hi])) for k, l, lo, hi in E2.HARNESS_ERA]
    return {'domain': [g for g in dom if g['ids']], 'era': [g for g in era if g['ids']]}
def ch_harness():
    G = harness_groups(); rows = {c['id']: harness_row(c) for c in H['cards']}
    facts = ''.join(f'<li>{esc(f["fact"])} {srcs(f.get("sources"), n=2)}</li>' for f in H.get('intro_facts', []))
    return f'''<section class="chap" id="harness"><div class="wide">{chead("harness")}
<div class="lwrap" data-lw="harness">{lens_bar(E2.HARNESS_LENSES, "驾驭：分组方式", len(H["cards"]), "domain")}
<div class="lcols" aria-hidden="true"><span>年代</span><span>办法 · 出处</span><span>领域</span><span>演示</span></div>
<div class="lgrid">{lens_body(G["domain"], rows)}</div></div>
<details class="fold big fade"><summary><h3>五条背景：计算机、小火箭与每秒几十次</h3></summary><ul class="facts">{facts}</ul></details>
</div></section>'''

def why_row(c):
    one = E.WHY.get(c['id'], '')
    img = E.IMAGES.get('card:' + c['id']); im = IM.get(img) if img else None
    ph = f'<figure class="lph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{capspan(img, 72)}</figcaption></figure>' if im else ''
    return f'''<article class="lrow" id="why-{esc(c['id'])}" data-id="{esc(c['id'])}">
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(c['id'])}">
<span class="ldate"><b>{esc(c['year'])}</b></span>
<span class="lname"><b>{esc(c['title'])}</b><small>{esc(one)}</small></span>
<span class="lkind">{esc(c['tag'])}</span><span class="lerr">{esc(c.get('number', ''))}</span><span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(c['id'])}" role="region" aria-label="{esc(c['title'])}"><div class="lmore-in">
<div class="lbody{'' if ph else ' nophoto'}"><div class="lmain"><p class="lwhy">{esc(one)}</p><p class="ltext">{esc(c['text'])}</p>{srcs(c.get('sources')) or '<p class="small">通行说法，未找到可引的一手来源。</p>'}<p class="lconf">{conf(c.get('conf'))}</p></div>{ph}</div>
</div></div></article>'''
def why_groups():
    cs = C['cards']; order = lambda xs: [c['id'] for c in sorted(xs, key=lambda c: (year0(c['year']), c['id']))]
    tag = [dict(k=t, label=f'{t} · {w}', ids=order([c for c in cs if c['tag'] == t])) for t, w in E2.WHY_TAGS]
    era = [dict(k=k, label=l, ids=order([c for c in cs if lo <= year0(c['year']) < hi])) for k, l, lo, hi in E2.WHY_ERA]
    return {'tag': [g for g in tag if g['ids']], 'era': [g for g in era if g['ids']]}
def ch_why():
    G = why_groups(); rows = {c['id']: why_row(c) for c in C['cards']}
    return f'''<section class="chap" id="why"><div class="wide">{chead("why")}
<div class="lwrap nothumb" data-lw="why">{lens_bar(E2.WHY_LENSES, "为什么要快：分组方式", len(C["cards"]), "tag")}
<div class="lcols" aria-hidden="true"><span>年代</span><span>事件 · 为什么</span><span>动机</span><span>数字</span></div>
<div class="lgrid">{lens_body(G["tag"], rows)}</div></div>
</div></section>'''

# ---------- 第七章 跑一跑
def tool(tid, body):
    title, lede = E2.TOOLS[tid]
    return f'<div class="tool fade" id="tool-{tid}"><div class="hd"><span class="k">动手</span><b>{esc(title)}</b><p>{esc(lede)}</p></div>{body}</div>'
def ch_tools():
    return (f'<section class="chap" id="tools"><div class="wide">{chead("tools")}{tool("race", demos.race())}{tool("drag", demos.drag())}'
            '<p class="fnote">参照：步行 5、博尔特 44.72、高铁 350、客机 900、音速 1,225 km/h（海平面 15 °C）；京沪高铁 1,318 km。</p></div></section>')

# ---------- 卷末
def refs_block():
    groups = [('序章 · 十九级阶梯（速度尺各级）', [s for L in journey.LEVELS for s in ((src_lookup_raw(L['src']) or {}).get('sources') or [])] + [s for x in B['scale'] for s in x.get('sources', [])]),
              ('第一章 · 这一周', [s for n in C['now'] for s in n.get('sources', [])] + E2.ANNIV_SRC),
              ('第二章 · 五条赛道（陆上轮式 / 铁路 / 水上）', [s for c in A['cells'] for s in c.get('sources', []) + c.get('also', {}).get('sources', [])]),
              ('第二章 · 五条赛道（空中 / 太空 / 人体与动物）', [s for c in B['cells'] for s in c.get('sources', []) + c.get('also', {}).get('sources', [])]),
              ('第三章 · 两条线', [s for p in B['record_line'] + C['daily_line'] for s in p.get('sources', [])]),
              ('第四章 · 撞墙', [s for w in WALLS.values() for s in w.get('sources', [])]),
              ('第五章 · 驾驭', [s for c in H['cards'] for s in c.get('sources', [])] + [s for f in H['intro_facts'] for s in f.get('sources', [])]),
              ('第六章 · 为什么要快', [s for c in C['cards'] for s in c.get('sources', [])])]
    out = []
    for g, ss in groups:
        seen, items = set(), []
        for s in ss:
            k = s.get('u') or s['t']
            if k in seen: continue
            seen.add(k)
            items.append(f'<li><a href="{esc(s["u"])}" target="_blank" rel="noopener">{esc(s["t"])}</a></li>' if s.get('u') else f'<li>{esc(s["t"])}</li>')
        out.append(f'<h3>{esc(g)}（{len(items)}）</h3><ul>{"".join(items)}</ul>')
    return ''.join(out)
USED = []  # 页面上实际出现的图（main() 在拼卷末之前算出）；署名表只列这些
def method_process():
    out = []
    for p in E.METHOD['process']:
        if p.startswith('序章与第五章「驾驭」是 10/18'): p = p.replace('序章舞台用真实照片', '序章（v2 改为全屏的十九级舞台）用真实照片')
        p = p.replace('矩阵里每格右上角有标记。', '每条数字旁都有标记。').replace('速度尺、矩阵、总线图全部程序绘制。', '十九级的尺子与表盘、五条赛道与两条线两张主图全部程序绘制。')
        out.append(p)
    out.append(esc(E2.METHOD_V2))
    return out
def credits():
    rows = ''.join(f'<tr><td>{esc(k)}</td><td>{esc(im["subject"])}</td><td>{esc(im["author"])}，{esc(im.get("year",""))}</td><td>{esc(im["license"])}</td><td><a href="{esc(im["source_page"])}" target="_blank" rel="noopener">来源页</a></td></tr>' for k, im in ((k, IM[k]) for k in USED))
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>作者 / 年代</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'
def endm():
    M = E.METHOD
    return f'''<footer class="endm" id="end"><div class="wide">
<h2 class="fade">卷末 · 参考、方法与署名</h2>
<details class="fold big fade"><summary><h3>参考（按章分组）</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{''.join(f'<li>{p}</li>' for p in method_process())}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{''.join(f'<li>{t}</li>' for t in M['todo'])}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(USED)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">一周一题 · 第 {E.META['no']} 题 · {E.META['date']}<br>研究、绘图与核查：Claude（站长复核）</div>
</div></footer>'''

# ---------- 数据（给 app.js / demos.js）
def data():
    cells = {}
    for (t, e), c in CELLS.items():
        img = E.IMAGES.get(f'{t}-{e}'); im = IM.get(img) if img else None
        if c.get('subject') == '—':
            cells[f'{t}-{e}'] = {'empty': True, 'why': c.get('why', ''), 'track': E2.TRACK_SHORT[t], 'era': f'{E.ERAS[e][0]} {E.ERAS[e][1]}'}
            continue
        d = {k: c.get(k) for k in ('subject', 'kmh', 'speed', 'year', 'who', 'where', 'conf', 'why', 'note', 'sources', 'also')}
        if d.get('note'): d['note'] = re.sub(r'^口径[：:]\s*', '', d['note'])
        if d.get('also') and d['also'].get('note'): d['also']['note'] = re.sub(r'^口径[：:]\s*', '', d['also']['note'])
        d['track'] = E2.TRACK_SHORT[t]; d['era'] = f'{E.ERAS[e][0]} {E.ERAS[e][1]}'
        if im: d['img'] = {'file': 'assets/' + im['file'], 'cap': caption_of(img, im), 'credit': stage.credit(im), 'alt': im['subject']}
        cells[f'{t}-{e}'] = d
    rec, art, day, hsr = line_series()
    rl = [{'y': max(p['year'], 1790), 'v': p['kmh'], 'n': p['label'].split('（')[0]} for p in rec]
    dl = [{'y': p['year'], 'v': p['kmh'], 'n': p['label']} for p in day]
    hl = [{'y': p['year'], 'v': p['kmh'], 'n': p['n']} for p in hsr]
    return {'cells': cells, 'tracks': [[tid, E2.TRACK_SHORT[tid]] for tid, _, _ in E.TRACKS], 'eras': [[e[0], e[1], s] for e, s in zip(E.ERAS, E2.ERA_SHORT)],
            'stage': stage.data(IM, caption_of, src_lookup),
            'lines': {'rec': rl, 'day': dl, 'hsr': hl, 'art': {'y': 2026, 'v': art['kmh']}, 'ms': [list(m) for m in E2.MILESTONES]},
            'lens': {'harness': harness_groups(), 'why': why_groups()}, 'lensName': {'harness': dict(E2.HARNESS_LENSES), 'why': dict(E2.WHY_LENSES)},
            'tool1': {'china': E.TOOL1['china_ew_km'], 'bjsh': E.TOOL1['bj_sh_km']}}

LIGHT = ('--bg:#F5F3EC;--surface:#FBFAF6;--surface-2:#ECE9DF;--ink:#17181C;--ink-2:#3B3D44;--muted:#6C6F78;--line:rgba(23,24,28,.16);--line-2:rgba(23,24,28,.09);--grid:rgba(23,24,28,.05);'
         '--accent:#C8202E;--accent-2:#E0414E;--accent-ink:#A9131F;--wash:rgba(200,32,46,.08);--wash-2:rgba(200,32,46,.16);--fill:#C8202E;--on-fill:#FFFFFF;--nav-glass:rgba(245,243,236,.8);--glass-line:rgba(23,24,28,.12);'
         '--road:#26272B;color-scheme:light;')

def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'demos.js'), encoding='utf-8').read()
    light = ('@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){' + LIGHT + '}}\n:root[data-theme="light"]{' + LIGHT + '}')
    pre = hero() + cnav() + '<main>' + tagline_sec() + ch_journey() + ch_now() + ch_tracks() + ch_lines() + ch_walls() + ch_harness() + ch_why() + ch_tools() + '</main>'
    dj = json.dumps(data(), ensure_ascii=False).replace('</', '<\\/')
    seen = pre + dj
    USED[:] = [k for k, im in IM.items() if ('assets/' + im['file']) in seen]
    print('images used', len(USED), '/', len(IM), '· unused:', [k for k in IM if k not in USED])
    body = pre + endm()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E2.META_DESC)).replace('{{LIGHT_BLOCKS}}', light)
            .replace('{{BODY}}', body).replace('{{DATA_JSON}}', dj).replace('{{APP_JS}}', app))
    page, report = fixes.apply(page)
    for line in report: print(line)
    open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(page)
    meta = {'no': E.META['no'], 'slug': E.META['slug'], 'title': E.META['title'], 'subtitle': E2.META_SUBTITLE, 'date': E.META['date'], 'summary': E2.META_DESC,
            'tags': E.META['tags'], 'format': E2.META_FORMAT, 'cover': 'cover.png', 'cover_focus': E.META['cover_focus'], 'cover_scheme': E.META['cover_scheme'], 'reading_time': E2.META_READING,
            'sources': ['FIA / FIM / FAI / UIM / 世界田径 / 吉尼斯的纪录页；NASA 与美国空军官方史（X-1、X-2、X-15、X-29、SR-71、Apollo 10、Artemis II、帕克探测器、Falcon 9 回收、Stapp）',
                        '英国国家铁路博物馆与科学博物馆集团、JR 东海、SNCF / Alstom、国铁集团与中车、澳大利亚国家海事博物馆、辛辛那提动物园',
                        'TechCrunch、Electrek、CBS 对 2026-10-15 Roadster 演示的报道；央视、新华网、界面对 GB 7258—2026 的报道；motorionline 对腾势 Z 的转述',
                        f'图片 {len(USED)} 张：NASA、美国陆军 / 海军、美国国会图书馆 Bain 收藏、Gallica、大都会博物馆 Open Access、geograph.org.uk、Flickr（CC BY / CC BY-SA）；逐张署名见页面卷末与 src/images.json']}
    json.dump(meta, open(os.path.join(HERE, '..', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote index.html', len(page), 'chars')

if __name__ == '__main__':
    main()
