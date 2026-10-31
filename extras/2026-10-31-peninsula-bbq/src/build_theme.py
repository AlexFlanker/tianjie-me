# -*- coding: utf-8 -*-
"""号外 · 半岛的烤肉：python3 extras/2026-10-31-peninsula-bbq/src/build_theme.py → ../index.html + ../meta.json"""
import json, os, html, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.dirname(HERE)
import sys; sys.path.insert(0, HERE)
import editorial as E, geo

def esc(s): return html.escape(str(s), quote=False)
def J(n): return json.load(open(os.path.join(HERE, 'research', n), encoding='utf-8'))
def bi(o, tag='span', raw=True):
    z, e = (o['zh'], o['en']) if raw else (esc(o['zh']), esc(o['en']))
    return f'<{tag} class="zh">{z}</{tag}><{tag} class="en">{e}</{tag}>'
def T(z, e): return {'zh': z, 'en': e}

A, B, C = J('hist_A.json'), J('hanwoo_B.json'), J('market_C.json')
IMGS = {im['key']: im for im in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))} if os.path.exists(os.path.join(HERE, 'images.json')) else {}
def img(k): return IMGS.get(k)
def src(k): im = img(k); return im['file'] if im else None
def cred(k):
    im = img(k)
    if not im: return None
    a = f'<a href="{html.escape(im["page"])}" target="_blank" rel="noopener">{esc(im["author"])}</a> · {esc(im["license"])}'
    return T(f'{im["zh"]} · 图：{a}', f'{im["en"]} · Photo: {a}')

# ---------- 卷首 ----------
def hero():
    h = E.HERO; im = img('hero')
    pic = ''
    if im:
        pic = f'<picture>{"<source media=" + chr(34) + "(max-aspect-ratio: 4/5)" + chr(34) + " srcset=" + chr(34) + im["mobile"] + chr(34) + ">" if im.get("mobile") else ""}<img src="{im["file"]}" alt="" fetchpriority="high"></picture>'
    c = cred('hero')
    return (f'<header class="hero" id="top">{pic}<div class="hero-tx"><span class="sticker red rise">{bi(h["kick"])}</span>'
            f'<h1 class="rise">{h["h1"]["en"]}</h1><p class="sub rise">{bi(h["sub"])}</p>'
            f'<div class="row rise"><a class="btn" href="#fire">{bi(h["cta"])}</a><span class="small" style="color:var(--band-ink-2)">{bi(T("约 15 分钟 · 中 / EN 在导航里切换", "About 15 min · switch 中 / EN in the bar"))}</span></div></div>'
            + (f'<div class="cred">{bi(c)}</div>' if c else '') + '</header>')

def thesis():
    t = E.THESIS
    zl = ' '.join(f'<span class="w{" hot" if hot else ""}">{esc(w)}</span>' for w, hot in t['zh'])
    el = ' '.join(f'<span class="w{" hot" if hot else ""}">{esc(w)}</span>' for w, hot in t['en'])
    nums = ''.join(f'<div class="n fade"><b>{esc(n["zh"])}</b><span>{bi(n["k"])}</span></div>' for n in t['nums'])
    return f'<section class="thesis"><div class="wide"><div class="lines zh">{zl}</div><div class="lines en">{el}</div><div class="nums">{nums}</div></div></section>'

def nav():
    chs = ''.join(f'<a href="#{i}" data-nav="{i}"><b>{k}</b>{bi(n)}</a>' for i, k, n in E.NAV)
    return f'<nav id="cnav" aria-label="章节"><div class="in"><div class="chs">{chs}</div><div class="tools"><button id="langbtn" type="button">EN</button><button id="themebtn" type="button" data-cover-hide>☾</button></div></div><div id="prog"></div></nav>'

def plate(cid, key):
    c = E.CH[cid]; im = img(key); cr = cred(key)
    pic = f'<img src="{im["file"]}" alt="" loading="lazy">' if im else ''
    return (f'<div class="plate">{pic}<div class="tx"><div class="big">{c["big"]}</div><div class="nm"><h2>{bi(c["h"])}</h2></div></div>'
            + (f'<div class="cred">{bi(cr)}</div>' if cr else '') + '</div>')

def sec_h(kick, h, p=None):
    return f'<div class="sec-h"><span class="kick">{kick}</span><h3>{bi(h)}</h3>' + (f'<p>{bi(p)}</p>' if p else '') + '</div>'

# ---------- 章 ----------
def ch_fire():
    return (f'<section class="ch" id="fire">{plate("fire", "plate-fire")}<div class="wide"><p class="lede fade">{bi(E.CH["fire"]["lede"])}</p></div>'
            f'<div class="sec"><div class="stage" id="stage"><div class="pin"><div class="ph"></div>'
            f'<div class="lane" role="group" aria-label="南 / 北"><button class="pill" data-lane="south" aria-pressed="true">{bi(T("1945 后 · 南", "After 1945 · South"))}</button><button class="pill" data-lane="north" aria-pressed="false">{bi(T("1945 后 · 北", "After 1945 · North"))}</button></div>'
            f'<div class="card"></div><div class="cap"></div><div class="ruler"><div class="hd"></div></div></div></div></div></section>')

def ch_cut():
    vs = B['wagyu_vs']
    vrows = ''.join(f'<div class="rw"><div>{bi({"zh": esc(v["dim_zh"]), "en": esc(v["dim_en"])})}</div><div>{bi({"zh": esc(v["hanwoo_zh"]), "en": esc(v["hanwoo_en"])})}</div><div>{bi({"zh": esc(v["wagyu_zh"]), "en": esc(v["wagyu_en"])})}</div></div>' for v in vs)
    gr = [g for g in B['grades'] if g['grade'] in ('1++', '1+', '1', '2', '3')]
    mx = {'1++': (7, 9), '1+': (6, 6), '1': (4, 5), '2': (2, 3), '3': (1, 1)}
    gh = ''.join(f'<div class="g"><b>{g["grade"]}</b><div class="mb">' + ''.join(f'<i class="{"f" if k <= mx[g["grade"]][1] else ""}" style="{"opacity:.45" if mx[g["grade"]][0] > k else ""}"></i>' for k in range(1, 10)) +
                 f'</div><p>{bi(T("大理石纹 " + g["marbling_no"].split("（")[0] + " 号", "Marbling No. " + g["marbling_no"].split("（")[0]))}</p></div>' for g in gr)
    rh = E.RHAPSODY
    return (f'<section class="ch" id="cut">{plate("cut", "plate-cut")}<div class="wide"><p class="lede fade">{bi(E.CH["cut"]["lede"])}</p>'
            f'<div class="sec">{sec_h("10 × 39", T("一头牛的分割图", "Butchery chart of one animal"), E.CUT_INTRO)}'
            f'<div class="cutwrap"><div><div class="cutmap" id="cutmap" style="margin-top:24px"></div><p class="small" style="margin-top:8px">{bi(T("示意图只表示各大分割的相对位置（左头右尾、上背下腹），面积不按重量。", "Positions are schematic (head left, back on top); areas are not to scale."))}</p></div><div class="cutpanel" id="cutpanel"></div></div>'
            f'<div class="grill" id="grill"><div class="gp"><img src="{src("grill-beef") or ""}" alt=""><div class="heat"></div><div class="tcap gpcap" style="position:absolute;left:0;right:0;bottom:0;padding:8px 12px;font-size:11px;line-height:16px;color:#fff;background:linear-gradient(0deg,rgba(0,0,0,.7),rgba(0,0,0,0))"></div></div>'
            f'<div class="gc"><span class="kick" style="color:var(--yellow)">GRILL TIMER</span><h4>{bi(T("烤一块：选个部位，按下上烤盘", "Grill one: pick a cut, put it on"))}</h4><div class="gcuts"></div>'
            f'<div class="clock"><b>0</b><span></span></div><div class="bar"><i></i></div><div class="say"></div>'
            f'<div class="gbtns"><button class="btn" data-act="go" type="button"></button><button class="btn ghost" data-act="speed" type="button">5×</button><button class="btn ghost" data-act="reset" type="button">{bi(T("重来", "Reset"))}</button></div><div class="note"></div></div></div>'
            f'<div class="fade" style="margin-top:48px;border:2px solid var(--line);padding:24px;background:var(--paper)"><span class="sticker">NETFLIX · KBS1</span><h4 style="font-size:22px;line-height:1.3;margin:16px 0 8px;font-weight:900">{bi(rh["h"])}</h4><ul style="margin:0;padding-left:18px;font-size:15px;line-height:24px">' + ''.join(f'<li style="margin-bottom:8px">{bi(x)}</li>' for x in rh['li']) + '</ul></div></div>'
            f'<div class="sec">{sec_h("1++ / 1+ / 1 / 2 / 3", T("等级：卖的是大理石纹", "Grades: selling the marbling"), E.GRADES_NOTE)}<div class="grades fade">{gh}</div></div>'
            f'<div class="sec">{sec_h("IMPORTS", E.SERIES["title"], T("拖动图表或点黄色编号，看每个年份发生了什么。红线是进口量（左轴），黑线是自给率（右轴）。", "Drag across the chart or tap the yellow markers. Red: imports (left axis). Black: self-sufficiency (right axis)."))}'
            f'<div class="chart" id="chart1"><div class="rd"></div><div class="legend"><span><i style="background:var(--red)"></i>{bi(E.SERIES["l1"])}</span><span><i style="background:var(--ink)"></i>{bi(E.SERIES["l2"])}</span></div><div class="cv"></div><div class="ev"></div></div><p class="small" style="margin-top:8px">{bi(E.SERIES["note"])}</p></div>'
            f'<div class="sec">{sec_h("HANWOO × WAGYU", T("韩牛与和牛：一个守家，一个出海", "Hanwoo vs Wagyu: one guards home, one went global"))}<div class="vs fade"><div class="hd"><div></div><div>{bi(T("韩牛", "Hanwoo"))}</div><div>{bi(T("和牛", "Wagyu"))}</div></div>{vrows}</div></div>'
            f'<div class="sec" data-list="ops">{sec_h("PLAYBOOK", T("把国产牛卖贵的七招", "Seven ways to sell domestic beef dear"), T("点开每一行看事实与出处。", "Open a row for the facts and sources."))}<div class="list"></div></div>'
            '</div></section>')

def ch_table():
    ns = E.NS
    def side(k):
        s = ns[k]; im = img(s['img']); cr = cred(s['img'])
        f = f'<figure><img src="{im["file"]}" alt="" loading="lazy"><figcaption>{bi(cr)}</figcaption></figure>' if im else ''
        return f'<div>{f}<h4>{bi(s["h"])}</h4><span class="kick">{bi(s["k"])}</span><ul>' + ''.join(f'<li>{bi(x)}</li>' for x in s['li']) + '</ul></div>'
    return (f'<section class="ch" id="table">{plate("table", "plate-table")}<div class="wide"><p class="lede fade">{bi(E.CH["table"]["lede"])}</p>'
            f'<div class="sec">{sec_h("8 RULES", T("一张韩烤桌的规矩", "The rules of the table"), T("点左边的每一条。", "Tap each rule."))}<div class="tbl" id="table"><div class="tp"><img src="" alt=""><div class="tcap"></div></div><div class="tl"></div></div></div>'
            f'<div class="sec">{sec_h("SOUTH / NORTH", T("同一张桌子，两种肉", "One table, two kinds of meat"))}<div class="ns fade">{side("s")}{side("n")}</div></div>'
            '</div></section>').replace('<div class="tbl" id="table">', '<div class="tbl" id="tablebox">')

def phases(k):
    out = ''
    for p in C[k]['phases']:
        fs = [f for f in p['facts'] if f.get('conf') != '低']
        li = lambda f: f'<li>{bi({"zh": esc(f["zh"]), "en": esc(f["en"])})}</li>'
        more = (f'<details class="more"><summary>{bi(T(f"再看 {len(fs) - 2} 条", f"{len(fs) - 2} more"))}</summary><ul>' + ''.join(li(f) for f in fs[2:]) + '</ul></details>') if len(fs) > 2 else ''
        out += f'<div class="phase fade"><div class="yy">{p["from"]}–{p["to"] if p["to"] < 2026 else ""}</div><div><h4>{bi({"zh": esc(p["title_zh"]), "en": esc(p["title_en"])})}</h4><ul>{"".join(li(f) for f in fs[:2])}</ul>{more}</div></div>'
    return out

def photo_row(keys):
    figs = ''
    for k in keys:
        im = img(k)
        if not im: continue
        figs += f'<figure><img src="{im["file"]}" alt="" loading="lazy"><figcaption>{bi(cred(k))}</figcaption></figure>'
    return f'<div class="prow fade">{figs}</div>' if figs else ''

def ch_world():
    return (f'<section class="ch" id="world">{plate("world", "plate-world")}<div class="wide"><p class="lede fade">{bi(E.CH["world"]["lede"])}</p>'
            f'<div class="sec">{sec_h("MAP · 1900–2026", T("扩张地图", "Expansion map"), T("拖动年份或按 ▶ 播放；点任一节点看说明。", "Drag the year or press ▶; tap any point."))}'
            f'<div><div class="map" id="map"><div class="hud"></div><svg></svg></div><div class="maphint small">{bi(T("← 左右滑动地图，美国在右边 →", "← Swipe the map; the US is on the right →"))}</div><div class="mapctl"><button class="pill" data-act="play" type="button">▶</button><input type="range" min="1900" max="2026" value="2026" step="1" aria-label="Year"></div><div class="mapnote"></div></div></div>'
            + photo_row(['w-la', 'w-cote', 'w-yanji', 'w-baekjeong']) +
            f'<div class="sec">{sec_h("US / CN", T("两条曲线", "Two curves"), E.WORLD_NOTE)}'
            f'<div class="twin"><div class="side"><h4><span class="sticker red">USA</span>{bi(T("美国：从社区食堂到纳斯达克", "US: from canteen to Nasdaq"))}</h4>{phases("us")}</div>'
            f'<div class="side"><h4><span class="sticker">CHINA</span>{bi(T("中国：从延边炭火到本土赛道", "China: from Yanbian charcoal to a local category"))}</h4>{phases("cn")}</div></div></div>'
            '</div></section>')

def ch_end():
    refs = {}
    def add(fs, grp):
        for f in fs:
            for s in f.get('sources', []) or []:
                if s.get('url'): refs.setdefault(grp, {})[s['url']] = s.get('title') or s['url']
    for e in A['eras']: add(e['facts'], 'A')
    for k in ('north', 'dogmeat', 'table', 'grills'): add(A[k], 'A')
    add(B['timeline'], 'B'); add(B['rhapsody'], 'B'); add(B['wagyu_vs'], 'B'); add(B['price'], 'B')
    for o in B['ops']: add(o['facts'], 'B')
    for k in ('us', 'cn'):
        for p in C[k]['phases']: add(p['facts'], 'C')
    add(C['global'], 'C'); add(C['kfood'], 'C')
    names = {'A': T('火 · 一张桌子（历史、北半岛）', 'Fire · Table (history, North Korea)'), 'B': T('刀（韩牛、分割、等级）', 'Cut (Hanwoo, butchery, grades)'), 'C': T('出海（美国、中国）', 'Abroad (US, China)')}
    rf = ''.join(f'<h5 style="margin:16px 0 8px;font-size:14px">{bi(names[g])}</h5><ul>' + ''.join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for u, t in refs[g].items()) + '</ul>' for g in ('A', 'B', 'C') if g in refs)
    seen, creds = set(), ''
    for im in IMGS.values():
        if im['id'] in seen: continue
        seen.add(im['id'])
        lic = f'<a href="{html.escape(im["license_url"])}" target="_blank" rel="noopener">{esc(im["license"])}</a>' if im.get('license_url') else esc(im['license'])
        creds += f'<li>{bi(T(esc(im["zh"]), esc(im["en"])))} — <a href="{html.escape(im["page"])}" target="_blank" rel="noopener">{esc(im["author"])}</a> · {lic}</li>'
    method = E.METHOD if hasattr(E, 'METHOD') else T('', '')
    pending = E.PENDING if hasattr(E, 'PENDING') else []
    return (f'<section class="ch" id="end"><div class="wide"><div class="sec endm">{sec_h("END", T("卷末", "Notes"))}'
            f'<details class="fold"><summary>{bi(T("方法", "Method"))}</summary><div class="fb">{bi(method, "p")}</div></details>'
            f'<details class="fold"><summary>{bi(T("仍待核实", "Still to verify"))}</summary><div class="fb"><ul>' + ''.join(f'<li>{bi(x)}</li>' for x in pending) + '</ul></div></details>'
            f'<details class="fold"><summary>{bi(T("参考来源", "Sources"))}</summary><div class="fb">{rf}</div></details>'
            f'<details class="fold"><summary>{bi(T("图片署名", "Photo credits"))}</summary><div class="fb"><ul>{creds}</ul></div></details>'
            f'<div class="stamp"><span class="sticker red">TIANJIE.ME · EXTRA</span><span class="small">{bi(T("号外 · 2026 年 10 月 31 日 · 天杰与 Claude 一起研究、写作、核查。错漏欢迎指正。", "Extra · 31 Oct 2026 · researched, written and checked by Tianjie with Claude. Corrections welcome."))}</span></div>'
            '</div></div></section>')

# ---------- 数据 ----------
def data():
    stage = []
    for s in E.STAGE:
        d = {k: s[k] for k in ('id', 'y', 'lane', 'label', 'yr', 'era', 'title', 'text', 'dishes')}
        k = s['img'] if src(s['img']) else 'plate-fire'
        d['img'] = src(k); d['cap'] = cred(k); d['fit'] = (img(k) or {}).get('fit')
        stage.append(d)
    cuts = []
    for c in B['cuts']:
        if c.get('kind') != 'primal': continue
        im = 'cut-' + c['id']
        cuts.append(dict(id=c['id'], ko=c['primal_ko'], zh=c['primal_zh'].split('（')[0], full=c['primal_zh'], en=c['primal_en'], area=E.CUT_AREA[c['id']], area2=E.CUT_AREA2.get(c['id']),
                         subs=[dict(ko=x['ko'], zh=x['zh'], en=x['en']) for x in c['subs']],
                         texture=T(c['texture_zh'], c['texture_en']), how=T(c['how_zh'], c['how_en']),
                         price=T(c['price_rank'], E.PRICE_EN.get(c['price_rank'], c['price_rank'])) if c.get('price_rank') else None,
                         img=src(im) or src('cuts'), cap=cred(im) if src(im) else cred('cuts')))
    bb = {c['id']: c for c in B['cuts'] if c.get('kind') == 'bbq'}
    grill = []
    for gid, sides, tip in E.GRILL:
        c = bb[gid]
        grill.append(dict(id=gid, zh=c['primal_zh'].split('（')[0] + ' ' + c['primal_ko'], en=c['primal_en'].split(' (')[0], sides=sides, tip=tip,
                          note=E.GRILL_NOTE, done=T('可以吃了：' + c['how_zh'], 'Ready. ' + c['how_en']),
                          img=src('grill-' + gid) or src('grill-beef'), cap=cred('grill-' + gid) if src('grill-' + gid) else cred('grill-beef')))
    yrs = list(range(2004, 2027))
    imp = {x['year']: x['value'] for x in B['series']['imports']}; ss = {x['year']: x['pct'] for x in B['series']['selfsuff']}
    series = dict(title=E.SERIES['title'], l1=E.SERIES['l1'], l2=E.SERIES['l2'], years=yrs, imports=[imp.get(y) for y in yrs], selfsuff=[ss.get(y) for y in yrs], imax=500, focus=2008, events=E.SERIES['events'])
    ops = []
    for i, o in enumerate(B['ops']):
        facts = [dict(zh=f['zh'], en=f['en'], src=(f.get('sources') or [{}])[0].get('url')) for f in o['facts'] if f.get('conf') != '低']
        ops.append(dict(id=o['id'], title=T(o['title_zh'].split('：')[0], o['title_en'].split(':')[0]), one=T((o['title_zh'].split('：') + [''])[1], (o['title_en'].split(':') + [''])[1].strip()), facts=facts, img=src('ops-' + o['id']), cap=cred('ops-' + o['id'])))
    table = [dict(title=t['title'], text=t['text'], img=src(t['img']), cap=cred(t['img'])) for t in E.TABLE]
    # 地图节点
    nodes = []
    for k in ('us', 'cn'):
        for m in C[k]['map']:
            if m.get('note') or m['city'] in E.MAP_DROP: continue
            x, y = geo.proj(m['lat'], m['lon']); nm, minor = E.MAP_NAME[m['city']]
            nd = dict(x=x, y=y, year=m['year'], city=nm, minor=minor, text=T(m['zh'], m['en']), c=k); nd.update(E.MAP_POS.get(m['city'], {})); nodes.append(nd)
    nodes += E.MAP_EXTRA
    for n in nodes:
        if 'x' not in n: n['x'], n['y'] = geo.proj(n['lat'], n['lon'])
    nodes.sort(key=lambda n: n['year'])
    return dict(meta=dict(title_zh=E.META['title_zh'], title_en=E.META['title_en']), stage=stage, cuts=cuts, grill=grill, series=series, ops=ops, table=table,
                map=dict(vb=geo.vb(), land=geo.land(), nodes=nodes))

def main():
    body = hero() + thesis() + nav() + '<main>' + ch_fire() + ch_cut() + ch_table() + ch_world() + ch_end() + '</main>'
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title_zh'])).replace('{{DESCRIPTION}}', esc(E.META['desc']))
            .replace('{{BODY}}', body).replace('{{DATA}}', json.dumps(data(), ensure_ascii=False).replace('</', '<\\/')).replace('{{APP}}', app))
    open(os.path.join(OUTD, 'index.html'), 'w', encoding='utf-8').write(page)
    meta = dict(slug=E.META['slug'], date=E.META['date'], title=E.META['title_zh'], subtitle=E.META['sub_zh'], summary=E.META['desc'],
                tags=['号外', '吃喝玩乐', '韩国', '朝鲜', '烤肉', '中英双语'], format='号外 · 时间轴舞台 · 分割图 · 烤肉计时器 · 扩张地图', reading_time='15 分钟',
                cover='cover.png', cover_focus='#top', cover_scheme='dark')
    json.dump(meta, open(os.path.join(OUTD, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    # 自检：泄漏词
    txt = re.sub(r'<script>window.PB.*?</script>', '', page, flags=re.S)
    for w in ('待核', '本路', '本轮', 'TODO', '建议页面'):
        n = page.count(w)
        if n: print('  ! 泄漏词', w, n)
    print('wrote', os.path.relpath(os.path.join(OUTD, 'index.html')), f'{len(page)//1024} KB')

if __name__ == '__main__': main()
