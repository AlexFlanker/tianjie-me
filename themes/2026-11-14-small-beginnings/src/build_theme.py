#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 9 题「起于微末」构建脚本：research/*.json + editorial.py + template.html + app.js → ../index.html、../meta.json、images.json
用法：python3 themes/2026-11-14-small-beginnings/src/build_theme.py"""
import os, sys, json, glob, html, re, copy
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import editorial as E
import fixes as F

WARN = []
def warn(s): WARN.append(s); print('  ! ' + s)
def esc(s): return html.escape(str(s if s is not None else ''), quote=True)
def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: warn(f'读不了 {os.path.basename(p)}：{e}'); return None

# ---------- 数据 ----------
def load_cases():
    files = sorted(glob.glob(os.path.join(HERE, 'research', 'cases_*.json')))
    sample = False
    if os.environ.get('SB_SAMPLE'): files = []   # SB_SAMPLE=1：强制用示例数据（调版面用）
    if not files: files = [os.path.join(HERE, 'research', '_sample.json')]; sample = True
    out, seen = [], set()
    for f in files:
        d = load(f)
        if isinstance(d, dict): d = d.get('cases') or d.get('items') or []
        for c in d or []:
            if not isinstance(c, dict) or not c.get('id'): continue
            if c['id'] in seen: warn(f'重复 id {c["id"]}（{os.path.basename(f)}），只取第一个'); continue
            if c['id'] in F.DROP: continue
            seen.add(c['id']); out.append(c)
    print(f'案例 {len(out)} 个，来自 {", ".join(os.path.basename(f) for f in files)}' + ('（示例数据）' if sample else ''))
    return out, sample

def load_images():
    ims = []
    for f in sorted(glob.glob(os.path.join(HERE, 'research', 'images_*.json'))):
        d = load(f)
        if isinstance(d, dict): d = d.get('images') or []
        ims += [x for x in (d or []) if isinstance(x, dict)]
    ok = []
    for im in ims:
        if im.get('status') in ('rejected-license', 'rejected'): continue
        fn = im.get('file')
        if not fn or not os.path.exists(os.path.join(ROOT, 'assets', fn)): warn(f'图片文件不在 assets/：{im.get("id")} {fn}'); continue
        if not im.get('license_short') or not im.get('source_url'): warn(f'图片缺许可或来源：{im.get("id")} {fn}'); continue
        if not im.get('width') or not im.get('height'):
            try:
                from PIL import Image
                with Image.open(os.path.join(ROOT, 'assets', fn)) as I: im['width'], im['height'] = I.size
            except Exception: im['width'], im['height'] = 1600, 1067
        ok.append(im)
    json.dump(ok, open(os.path.join(HERE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    by = {}
    for im in ok: by.setdefault(im['id'], []).append(im)
    return by

def patch(cases):
    by = {c['id']: c for c in cases}
    for cid, path, val in F.PATCH:
        c = by.get(cid)
        if c is None: warn(f'PATCH 未命中：没有案例 {cid}'); continue
        o = c; ks = path.split('.')
        try:
            for k in ks[:-1]: o = o[int(k)] if isinstance(o, list) else o[k]
            k = ks[-1]
            if isinstance(o, list): o[int(k)] = val
            else: o[k] = val
            print(f'  PATCH {cid}.{path} ✓')
        except Exception as e: warn(f'PATCH 未命中：{cid}.{path}（{e}）')

BAD = ['示例', '待核', '待填', '本路', '页面可', '页面不要', '不下结论', '研究员', 'TODO', 'verify']
def scan_text(cases, sample):
    def walk(o, where):
        if isinstance(o, str):
            for b in BAD:
                if b in o: warn(f'编辑用语「{b}」在 {where}：{o[:40]}'); break
        elif isinstance(o, list):
            for i, x in enumerate(o): walk(x, f'{where}.{i}')
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ('note', 'verify', 'sources', 'id'): continue
                walk(v, f'{where}.{k}')
    if sample: print('  （示例数据：跳过编辑用语扫描）'); return
    for c in cases: walk(c, c['id'])

def norm(c):
    """把案例整理成页面要的样子，缺的字段补空，数值转型。"""
    o = c.setdefault('origin', {}); c.setdefault('chain', []); c.setdefault('reach', {}); c.setdefault('lag', {})
    c.setdefault('facts', []); c.setdefault('sources', []); c.setdefault('dispute', ''); c.setdefault('confidence', '中')
    if c.get('kind') not in ('block', 'boost'): warn(f'{c["id"]} kind 不是 block / boost：{c.get("kind")}'); c['kind'] = 'block'
    for p in [o] + c['chain']:
        for k in ('lat', 'lon'):
            try: p[k] = float(p.get(k))
            except Exception: p[k] = None
        try: p['year'] = int(p.get('year'))
        except Exception: p['year'] = None
    try: c['reach']['year'] = int(c['reach'].get('year'))
    except Exception: c['reach']['year'] = (c['chain'][-1]['year'] if c['chain'] else o.get('year'))
    try: c['lag']['days'] = float(c['lag'].get('days'))
    except Exception: c['lag']['days'] = None
    c['st'] = E.SMALL_TYPE.get(c['id'])
    if not c['st']: warn(f'{c["id"]} 不在 editorial.SMALL_TYPE 里，归到 thing'); c['st'] = 'thing'
    y = o.get('year') or 0
    c['era'] = next((i for i, (a, b, _) in enumerate(E.ERAS) if a <= y < b), 0)
    return c

def audit(cases, sample):
    ids = {c['id'] for c in cases}
    for c in cases:
        i = c['id']; o = c['origin']
        if len(c['chain']) < 2: warn(f'{i} 因果链不足 2 步')
        if len(c['chain']) > 5: warn(f'{i} 因果链超过 5 步（{len(c["chain"])}）')
        for n, p in enumerate([o] + c['chain']):
            if p.get('lat') is None or p.get('lon') is None or not (-90 <= p['lat'] <= 90) or not (-180 <= p['lon'] <= 180): warn(f'{i} 第 {n} 个地点经纬度不对：{p.get("lat")}, {p.get("lon")}')
            if p.get('year') is None: warn(f'{i} 第 {n} 个地点缺年份')
        if len(c['sources']) < 2: warn(f'{i} 来源不足 2 个')
        for s in c['sources']:
            if not str(s.get('url', '')).startswith('http'): warn(f'{i} 来源缺网址：{s.get("title")}')
        if c['lag']['days'] is None or c['lag']['days'] <= 0: warn(f'{i} lag.days 缺失或不为正')
        for k, lim in (('title_zh', 10), ('small_zh', 26), ('big_zh', 36)):
            if not c.get(k): warn(f'{i} 缺 {k}')
            elif len(c[k]) > lim: warn(f'{i} {k} 偏长（{len(c[k])} 字）：{c[k]}')
        if c.get('verify') and not sample: warn(f'{i} 仍标 verify：{c.get("note", "")[:50]}')
    for p in E.PAIRS:
        for i in p['ids']:
            if i not in ids: warn(f'序章对子「{p["name"]}」缺案例 {i}，这一对会被跳过')
    for i in E.SMALL_TYPE:
        if i not in ids and not sample: warn(f'editorial.SMALL_TYPE 里的 {i} 没有案例数据')
    def todo(o, where):
        if isinstance(o, str):
            if '待填' in o: warn(f'editorial.{where} 待填')
        elif isinstance(o, (list, tuple)):
            for n, x in enumerate(o): todo(x, f'{where}[{n}]')
        elif isinstance(o, dict):
            for k, v in o.items(): todo(v, f'{where}.{k}')
    for name in ('META', 'HERO', 'THESIS_NOTE', 'NUMS', 'CHAPTERS', 'LAG_NOTE', 'METHOD', 'VERIFY'): todo(getattr(E, name), name)

# ---------- 小部件 ----------
CONF = {'高': 'h', '中': 'm', '低': 'l'}
def conf(c): return f'<span class="conf {CONF.get(c, "m")}" title="资料置信度：高 = 一手官方或学术来源；中 = 可靠二手；低 = 通行说法或传说">置信度 {esc(c or "中")}</span>'
def yr(y):
    if y is None: return ''
    return f'前 {-y} 年' if y < 0 else f'{y}'
def yspan(c):
    a, b = c['origin'].get('year'), c['reach'].get('year')
    return yr(a) if (b is None or a == b) else f'{yr(a)} → {yr(b)}'
def kmark(kind, cls=''): return f'<i class="km {kind} {cls}" aria-hidden="true"></i>'
def pic(im, cls='', lazy=True, sizes=None):
    return f'<img class="{cls}" src="assets/{esc(im["file"])}" alt="{esc(im.get("subject", ""))}" width="{im["width"]}" height="{im["height"]}"' + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + '>'
def credit(im): return f'<span class="cr">图：{esc(im.get("author_short") or im.get("author", ""))}，{esc(im["license_short"])}。</span>'
def figure(im, cls='fig'):
    return f'<figure class="{cls}">{pic(im)}<figcaption><span class="cap">{esc(im.get("subject", ""))}</span>{credit(im)}</figcaption></figure>'
def srcs(ss):
    li = ''.join(f'<li><a href="{esc(s.get("url"))}" target="_blank" rel="noopener">{esc(s.get("title") or s.get("url"))}</a>' + (f'<span class="pub">{esc(s.get("publisher", ""))}{("，" + esc(s.get("year"))) if s.get("year") else ""}</span>' if s.get('publisher') or s.get('year') else '') + '</li>' for s in ss if s.get('url'))
    return f'<details class="fold src"><summary>来源（{len(ss)}）</summary><ol>{li}</ol></details>' if li else ''

USED = []
def use(im):
    if im and im not in USED: USED.append(im)
    return im

# ---------- 各节 ----------
def hero(IM):
    H = E.HERO; hs = IM.get('hero') or [None]; im = use(next((x for x in hs if x and x.get('file') == H.get('file')), hs[0]))
    bg = f'<div class="hbg">{pic(im, lazy=False)}</div><div class="hveil"></div>' if im else '<div class="hbg plain"></div>'
    cap = f'<p class="hcap" data-cover-hide><span class="cap">{esc(H["caption"] if "待填" not in H["caption"] else im.get("subject", ""))}</span>{credit(im)}</p>' if im else ''
    return f'''<header class="hero{' has-img' if im else ''}" id="top">{bg}
<div class="wide hin"><p class="kick">{esc(H["kicker"])}</p>
<h1><span class="h1a">{esc(H["title"])}</span><span class="h1b">{esc(H["sub"])}</span></h1>
<p class="hlede">{esc(H["lede"])}</p>
<p class="hact" data-cover-hide><a class="btn" href="#stage">{esc(H["cta"])}<span aria-hidden="true">↓</span></a></p>
<p class="hbasis" data-cover-hide>{esc(H["basis"])}</p></div>{cap}</header>'''

def thesis():
    ws = ''.join(f'<span class="w">{esc(w)}</span>' for w in E.THESIS_WORDS)
    nums = ''.join(f'<div class="num"><div class="nv">{esc(n["value"])}<small>{esc(n["unit"])}</small></div><p>{esc(n["note"])}</p></div>' for n in E.NUMS)
    return f'''<section class="thesis" id="thesis" aria-label="论点"><div class="wide"><p class="tw" aria-label="{esc(E.THESIS)}">{ws}</p>
<p class="tnote rise">{esc(E.THESIS_NOTE)}</p>
<div class="twokinds rise"><span>{kmark("block")}<b>卡住</b>了世界</span><span>{kmark("boost")}<b>推</b>了世界<b>一把</b></span></div>
<div class="nums rise">{nums}</div></div></section>'''

def cnav():
    a = ''.join(f'<a href="#{c["id"]}" data-ch="{c["id"]}">{("<span>" + c["no"] + "</span>") if c["no"] else ""}{esc(c["nav"])}</a>' for c in E.CHAPTERS if c['id'] in SHOWN)
    return f'''<nav class="cnav" aria-label="章节"><div class="wide cin"><a class="chome" href="#top">起于微末</a><div class="clinks">{a}</div>
<button class="theme" type="button" data-cover-hide aria-pressed="false" aria-label="切换深浅色"><span class="t-l">夜里读</span><span class="t-d">白天读</span></button></div><div class="cprog"><i></i></div></nav>'''

def chead(cid, IM=None, plate=None):
    c = next(x for x in E.CHAPTERS if x['id'] == cid)
    im = use((IM.get(plate) or [None])[0]) if (IM and plate) else None
    pl = f'<figure class="plate rise">{pic(im)}<figcaption><span class="cap">{esc(im.get("subject", ""))}</span>{credit(im)}</figcaption></figure>' if im else ''
    no = f'<span class="cno">{c["no"]}</span>' if c['no'] else ''
    return f'{pl}<div class="chd rise">{no}<h2>{esc(c["title"])}</h2><p class="lede">{esc(c["lede"])}</p></div>'

def steps(cases):
    by = {c['id']: c for c in cases}; out = []
    for pi, p in enumerate(E.PAIRS):
        ok = lambda c: c['origin'].get('lat') is not None and c['origin'].get('lon') is not None and any(q.get('lat') is not None and q.get('lon') is not None for q in c['chain'])
        if all(i in by and ok(by[i]) for i in p['ids']):
            for i in p['ids']: out.append({'pair': p['key'], 'pname': p['name'], 'line': p['line'], 'id': i})
    return out

def ch_stage(ST):
    if not ST: return ''
    c = next(x for x in E.CHAPTERS if x['id'] == 'stage')
    ticks = ''; last = None
    for i, s in enumerate(ST):
        if s['pair'] != last: ticks += ('</div>' if last else '') + f'<div class="rg"><span class="rgn">{esc(s["pname"])}</span>'; last = s['pair']
        k = BY[s['id']]['kind']
        ticks += f'<button type="button" class="rt {k}" data-i="{i}" aria-label="{esc(s["pname"])}：{esc(BY[s["id"]]["title_zh"])}">{kmark(k)}<span>{esc(BY[s["id"]]["title_zh"])}</span></button>'
    ticks += '</div>'
    return f'''<section class="stage" id="stage" style="--n:{len(ST)}" aria-label="序章：{esc(c["title"])}">
<div class="sin"><div class="smap mv" data-mv="stage"></div>
<div class="shud"><p class="sno"><span class="cno">00</span>{esc(c["title"])}</p><p class="spair"></p><p class="sline"></p></div>
<article class="scard" aria-live="polite"></article>
<div class="sruler" role="slider" tabindex="0" aria-label="序章进度" aria-valuemin="1" aria-valuemax="{len(ST)}" aria-valuenow="1">{ticks}<i class="rcur"></i></div>
</div></section>'''

def ch_week(WK):
    if not WK: return ''
    items = WK.get('items') if isinstance(WK, dict) else WK
    if not items: return ''
    rows = ''
    for it in items:
        if not isinstance(it, dict): continue
        t = it.get('text_zh') or it.get('what_zh') or it.get('title_zh') or ''
        if not t.strip(): continue
        by = it.get('by_zh') or it.get('said_by_zh') or it.get('who_zh') or ''
        ss = it.get('sources') or ([it['source']] if isinstance(it.get('source'), dict) else [])
        sl = '、'.join(f'<a href="{esc(s.get("url"))}" target="_blank" rel="noopener">{esc(s.get("publisher") or s.get("title") or "来源")}</a>' for s in ss if isinstance(s, dict) and s.get('url'))
        rows += f'<li class="rise"><time>{esc(it.get("date_zh") or it.get("date") or "")}</time><div><p class="wt">{esc(it.get("title_zh") if it.get("title_zh") and it.get("title_zh") != t else "")}</p><p>{esc(t)}</p><p class="small">{("据 " + esc(by) + "。") if by else ""}{("来源：" + sl) if sl else ""}</p></div></li>'
    note = WK.get('note_zh', '') if isinstance(WK, dict) else ''
    if not rows: return ''
    return f'<section class="ch" id="week"><div class="wide">{chead("week")}<ol class="week">{rows}</ol>{("<p class=small>" + esc(note) + "</p>") if note else ""}</div></section>'

def chips(cases):
    return ''.join(f'<button type="button" class="chip {c["kind"]}" data-id="{c["id"]}" aria-pressed="false">{kmark(c["kind"])}{esc(c["title_zh"])}</button>' for c in sorted(cases, key=lambda c: (c['origin'].get('year') or 0)))

def ch_ripple(cases, IM):
    nb = sum(1 for c in cases if c['kind'] == 'block'); nt = len(cases) - nb
    return f'''<section class="ch" id="ripple"><div class="wide">{chead("ripple", IM, "plate-place")}
<div class="lens rise" role="group" aria-label="只看哪一类"><button type="button" class="sbtn on" data-f="all" aria-pressed="true">全部 {len(cases)}</button><button type="button" class="sbtn" data-f="block" aria-pressed="false">{kmark("block")}卡住 {nb}</button><button type="button" class="sbtn" data-f="boost" aria-pressed="false">{kmark("boost")}推一把 {nt}</button></div>
<div class="rgrid rise"><div class="rscroll"><div class="rmap mv" data-mv="ripple"></div></div>
<aside class="rpanel" aria-live="polite"><p class="rhint">{esc(E.RIPPLE_HINT)}</p></aside></div>
<div class="chips rise" role="group" aria-label="选一个案例">{chips(cases)}</div></div></section>'''

def ch_lag(cases, IM):
    return f'''<section class="ch" id="lag"><div class="wide">{chead("lag", IM, "plate-code")}
<div class="lens rise" role="group" aria-label="两种看法"><button type="button" class="sbtn on" data-v="lag" aria-pressed="true">隔了多久</button><button type="button" class="sbtn" data-v="year" aria-pressed="false">哪年到哪年</button></div>
<p class="lread rise" aria-live="polite"></p>
<div class="lchart rise" tabindex="0" role="img" aria-label="每个案例从起点到牵动全球隔了多久"></div>
<p class="small rise">{esc(E.LAG_NOTE)}</p></div></section>'''

def row(c, IM):
    ims = IM.get(c['id']) or []; im = use(ims[0]) if ims else None
    th = f'<span class="rth">{pic(im)}</span>' if im else '<span class="rth none"></span>'
    chain = ''.join(f'<li><time>{yr(p.get("year"))}</time><span class="pl">{esc(p.get("place_zh", ""))}</span><p>{esc(p.get("text_zh", ""))}</p></li>' for p in c['chain'])
    facts = ''.join(f'<li>{esc(f)}</li>' for f in c['facts'])
    o = c['origin']; r = c['reach']
    disp = f'<p class="dispute"><b>有不同说法</b>{esc(c["dispute"])}</p>' if c.get('dispute') else ''
    figs = ''.join(figure(use(x)) for x in ims[:2])
    lag = f'<p class="lagl"><b>隔了多久</b>{esc(c["lag"].get("text_zh", ""))}</p>' if c['lag'].get('text_zh') else ''
    return f'''<article class="row {c["kind"]}" id="c-{c["id"]}" data-id="{c["id"]}" data-kind="{c["kind"]}" data-st="{c["st"]}" data-era="{c["era"]}" data-year="{o.get("year") or 0}">
<button type="button" class="rh" aria-expanded="false" aria-controls="b-{c["id"]}"><span class="ry">{yr(o.get("year"))}</span><span class="rn">{kmark(c["kind"])}{esc(c["title_zh"])}</span><span class="rs">{esc(c.get("small_zh", ""))}</span><span class="rb2">{esc(c.get("big_zh", ""))}</span>{th}<span class="rx" aria-hidden="true"></span></button>
<div class="rb" id="b-{c["id"]}" hidden><div class="rbi"><div class="rbt">
<p class="otext"><b>起点</b><span class="pl">{esc(o.get("place_zh", ""))}，{yr(o.get("year"))}</span>{esc(o.get("text_zh", ""))}</p>
<ol class="chain">{chain}</ol>
<p class="reach"><b>牵动到</b>{esc(r.get("text_zh", ""))}</p>{lag}
{("<ul class=facts>" + facts + "</ul>") if facts else ""}{disp}
<p class="rmeta">{conf(c.get("confidence"))}<a class="tomap" href="#ripple" data-id="{c["id"]}">在涟漪图上看</a></p>{srcs(c["sources"])}</div>
{("<div class=rbf>" + figs + "</div>") if figs else ""}</div></div></article>'''

def ch_cases(cases, IM):
    rows = ''.join(row(c, IM) for c in sorted(cases, key=lambda c: (c['origin'].get('year') or 0)))
    return f'''<section class="ch" id="cases"><div class="wide">{chead("cases", IM, "plate-life")}
<div class="lens sticky rise" role="group" aria-label="换一种看法"><button type="button" class="sbtn on" data-l="kind" aria-pressed="true">走向</button><button type="button" class="sbtn" data-l="st" aria-pressed="false">小在哪里</button><button type="button" class="sbtn" data-l="era" aria-pressed="false">年代</button></div>
<div class="rows">{rows}</div></div></section>'''

def endm(cases):
    meth = ''.join(f'<li>{esc(x)}</li>' for x in E.METHOD); ver = ''.join(f'<li>{esc(x)}</li>' for x in E.VERIFY)
    refs = ''.join(f'<li><b>{esc(c["title_zh"])}</b>' + '；'.join(f'<a href="{esc(s.get("url"))}" target="_blank" rel="noopener">{esc(s.get("title") or s.get("url"))}</a>' for s in c['sources'] if s.get('url')) + '</li>' for c in cases)
    crs = ''.join(f'<tr><td>{esc(im.get("subject", ""))}</td><td>{esc(im.get("author", ""))}{("，" + esc(im.get("year"))) if im.get("year") else ""}</td><td><a href="{esc(im.get("license_url") or im.get("source_url"))}" target="_blank" rel="noopener">{esc(im["license_short"])}</a></td><td><a href="{esc(im["source_url"])}" target="_blank" rel="noopener">来源页</a></td></tr>' for im in USED)
    base = '<tr><td>序章与涟漪图底图：NASA「蓝色弹珠：下一代」2004 年 10 月全球合成图</td><td>NASA Earth Observatory，2004</td><td><a href="https://www.nasa.gov/nasa-brand-center/images-and-media/" target="_blank" rel="noopener">公有领域</a></td><td><a href="https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/topography-bathymetry/" target="_blank" rel="noopener">来源页</a></td></tr>'
    return f'''<section class="ch end" id="end"><div class="wide"><div class="chd rise"><h2>卷末</h2></div>
<details class="fold"><summary>方法</summary><ul>{meth}</ul></details>
<details class="fold"><summary>仍待核</summary><ul>{ver}</ul></details>
<details class="fold"><summary>按案例参考（{len(cases)}）</summary><ul class="refs">{refs}</ul></details>
<details class="fold"><summary>图片署名（{len(USED) + 1}）</summary><div class="tscroll"><table class="crt"><thead><tr><th>图</th><th>作者与年份</th><th>许可</th><th>来源</th></tr></thead><tbody>{base}{crs}</tbody></table></div></details>
<p class="stamp">{esc(E.STAMP)}</p></div></section>'''

# ---------- 组装 ----------
def main():
    global BY, SHOWN
    cases, sample = load_cases(); patch(cases)
    cases = [norm(c) for c in cases]
    bad = [c['id'] for c in cases if c['origin'].get('lat') is None or c['origin'].get('lon') is None or not c.get('title_zh')]
    if bad: warn('以下案例缺起点经纬度或名字，这次不上页面：' + '、'.join(bad))
    cases = [c for c in cases if c['id'] not in bad]; BY = {c['id']: c for c in cases}
    IM = load_images(); scan_text(cases, sample); audit(cases, sample)
    WK = load(os.path.join(HERE, 'research', 'week.json')) if os.path.exists(os.path.join(HERE, 'research', 'week.json')) else None
    ST = steps(cases)
    wk = ch_week(WK)
    SHOWN = {'stage', 'ripple', 'lag', 'cases', 'end'} - (set() if ST else {'stage'}) | ({'week'} if wk else set())
    # 先渲染各节（登记用到的图），卷末最后
    parts = [hero(IM), thesis(), cnav(), ch_stage(ST), wk, ch_ripple(cases, IM), ch_lag(cases, IM), ch_cases(cases, IM)]
    for s in ST:
        for im in (IM.get(s['id']) or [])[:1]: use(im)
    parts.append(endm(cases))
    def slim(c):
        im = (IM.get(c['id']) or [None])[0]
        return {'id': c['id'], 't': c['title_zh'], 'k': c['kind'], 'st': c['st'], 'era': c['era'], 's': c.get('small_zh', ''), 'b': c.get('big_zh', ''),
                'o': {'y': c['origin'].get('year'), 'p': c['origin'].get('place_zh', ''), 'la': c['origin']['lat'], 'lo': c['origin']['lon'], 'x': c['origin'].get('text_zh', '')},
                'c': [{'y': p.get('year'), 'p': p.get('place_zh', ''), 'la': p['lat'], 'lo': p['lon'], 'x': p.get('text_zh', '')} for p in c['chain'] if p.get('lat') is not None and p.get('lon') is not None],
                'r': {'y': c['reach'].get('year'), 'x': c['reach'].get('text_zh', '')}, 'lag': c['lag'].get('days'), 'lagx': c['lag'].get('text_zh', ''),
                'im': ({'f': im['file'], 'w': im['width'], 'h': im['height'], 'a': im.get('subject', ''), 'cr': f'图：{im.get("author_short") or im.get("author", "")}，{im["license_short"]}。'} if im else None)}
    data = {'cases': [slim(c) for c in cases], 'steps': ST,
            'kinds': {k: v['name'] for k, v in E.KIND.items()}, 'st': [list(x) for x in E.SMALL_TYPES], 'eras': [x[2] for x in E.ERAS],
            'ticks': [list(x) for x in E.LAG_TICKS], 'base': 'assets/earth-day-1920.jpg'}
    T = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    page = (T.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E.META['subtitle']))
             .replace('{{BODY}}', '\n'.join(p for p in parts if p))
             .replace('{{DATA}}', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
             .replace('{{APP}}', open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()))
    for old, new in F.POST:
        n = page.count(old)
        if n: page = page.replace(old, new); print(f'  POST ✓×{n} {old[:30]}')
        else: warn(f'POST 未命中：{old[:40]}')
    if not sample:
        body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', page)
        for b in ('示例', '待填', '本路', '页面可'):
            if b in body: warn(f'成品页正文里还有「{b}」')
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    meta = copy.deepcopy(E.META)
    json.dump(meta, open(os.path.join(ROOT, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'写出 index.html（{len(page.encode("utf-8")) // 1024} KB）、meta.json、images.json；舞台 {len(ST)} 步；用图 {len(USED)} 张；警告 {len(WARN)} 条')

if __name__ == '__main__': main()
