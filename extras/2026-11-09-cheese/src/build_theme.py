# -*- coding: utf-8 -*-
"""号外 · 奶酪：python3 extras/2026-11-09-cheese/src/build_theme.py → ../index.html + ../meta.json"""
import json, os, html, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.dirname(HERE)
import sys; sys.path.insert(0, HERE)
import editorial as E

def esc(s): return html.escape(str(s), quote=False)
def J(n): return json.load(open(os.path.join(HERE, 'research', n), encoding='utf-8'))
def bi(o, tag='span'):
    return f'<{tag} class="zh">{o["zh"]}</{tag}><{tag} class="en">{o["en"]}</{tag}>'
def T(z, e): return {'zh': z, 'en': e}

A, B, C, D = J('hist_A.json'), J('craft_B.json'), J('world_C.json'), J('counter_D.json')
try:
    import fixes
    print('  核查改正', fixes.apply(A, B, C, D), '条全部命中')
except ImportError:
    pass
IMGS = {im['key']: im for im in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))} if os.path.exists(os.path.join(HERE, 'images.json')) else {}
def img(k): return IMGS.get(k)
def src(k): im = img(k); return im['file'] if im else None
def cred(k, photo=True):
    im = img(k)
    if not im: return None
    a = f'<a href="{html.escape(im["page"] or "")}" target="_blank" rel="noopener">{esc(im["author"])}</a> · {esc(im["license"])}'
    return T(f'{im["zh"]} · 图：{a}', f'{im["en"]} · {"Photo" if photo else "Image"}: {a}')

# ---------- 卷首 / 论点 / 导航 ----------
def hero():
    h = E.HERO; im = img('hero')
    pic = ''
    if im:
        ms = f'<source media="(max-aspect-ratio: 4/5)" srcset="{im["mobile"]}">' if im.get('mobile') else ''
        pic = f'<picture>{ms}<img src="{im["file"]}" alt="" fetchpriority="high"></picture>'
    c = cred('hero')
    return (f'<header class="hero" id="top">{pic}<div class="hero-tx"><span class="kick rise">{bi(h["kick"])}</span>'
            f'<h1 class="rise">{bi(h["h1"])}</h1><p class="sub rise">{bi(E.HERO_SUB)}</p>'
            f'<div class="row rise"><a class="btn" href="#hist">{bi(h["cta"])}</a><span class="small" style="color:#8F806B">{bi(T("约 20 分钟 · 中 / EN 在导航里切换", "About 20 min · switch 中 / EN in the bar"))}</span></div></div>'
            + (f'<div class="cred">{bi(c)}</div>' if c else '') + '</header>')

def thesis():
    t = E.THESIS
    zl = ''.join(f'<span class="w{" hot" if hot else ""}">{esc(w)}</span>' for w, hot in t['zh'])
    el = ' '.join(f'<span class="w{" hot" if hot else ""}">{esc(w)}</span>' for w, hot in t['en'])
    nums = ''.join(f'<div class="n fade"><b>{esc(n["zh"])}</b><span>{bi(n["k"])}</span></div>' for n in t['nums'])
    return f'<section class="thesis"><div class="wide"><div class="lines zh">{zl}</div><div class="lines en">{el}</div><div class="nums">{nums}</div></div></section>'

def nav():
    chs = ''.join(f'<a href="#{i}" data-nav="{i}"><b>{k}</b>{bi(n)}</a>' for i, k, n in E.NAV)
    return f'<nav id="cnav" aria-label="章节"><div class="in"><div class="chs">{chs}</div><div class="tools"><button id="langbtn" type="button">EN</button><button id="themebtn" type="button" data-cover-hide>☾</button></div></div><div id="prog"></div></nav>'

def plate(cid, key):
    c = E.CH[cid]; im = img(key); cr = cred(key)
    pic = f'<img src="{im["file"]}" alt="" loading="lazy">' if im else ''
    return (f'<div class="plate">{pic}<div class="tx"><div class="no">{c["no"]}</div><h2>{bi(c["h"])}</h2></div>'
            + (f'<div class="cred">{bi(cr)}</div>' if cr else '') + '</div>')

def sec_h(kick, h, p=None):
    return f'<div class="sec-h fade"><span class="kick">{kick}</span><h3>{bi(h)}</h3>' + (f'<p>{bi(p)}</p>' if p else '') + '</div>'

def yk(y):
    if not y: return None
    y = str(y); return T(y, '' if re.search(r'[\u4e00-\u9fff]', y) else y)

def lede(cid):
    return f'<div class="wide"><p class="lede fade">{bi(E.CH[cid]["lede"])}</p></div>'

# ---------- 00 沿革（舞台） ----------
def ch_hist():
    return (f'<section class="ch" id="hist">{plate("hist", "plate-hist")}{lede("hist")}'
            f'<div class="sec"><div class="stage" id="stage"><div class="pin"><div class="ph"></div><div class="card"></div><div class="cap2"></div><div class="ruler"><div class="hd"></div></div></div></div></div>'
            f'<div class="wide"><div class="sec">{sec_h("ASIA", E.ASIA_HEAD, E.ASIA_NOTE)}<div data-list="asia"><div class="list"></div></div></div></div></section>')

def asia_data():
    AS = {a['id']: a for a in A['asia']}
    out = []
    for aid, title, sub, one in E.ASIA_ITEMS:
        a = AS[aid]; k = 'a-' + aid
        facts = [dict(k=yk(a.get('year')), zh=esc(a['zh']), en=esc(a['en']), src=(a.get('sources') or [{}])[0].get('url'))]
        out.append(dict(id=aid, title=title, sub=sub, one=one, facts=facts, img=src(k), cap=cred(k)))
    return out

def stage_data():
    st = []
    for s in E.STAGE:
        k = s['img'] if src(s['img']) else 'plate-hist'
        im = img(k) or {}
        st.append(dict(id=s['id'], label=s['label'], yr=s['yr'], era=s['era'], title=s['title'], text=s['text'], tags=s['tags'],
                       img=src(k), cap=cred(k, photo=im.get('kind') != 'art'), fit=im.get('fit'), pw=round(im.get('w', 0) * 1.4) if im.get('fit') else None))
    return st

# ---------- 01 做一块 ----------
def ch_make():
    g = lambda cls, k: f'<div class="g {cls}"><span class="k">{bi(k)}</span><b>—</b><div class="bar"><i></i></div></div>'
    gauges = g('t', T('温度', 'Temp')) + g('ph', T('酸度', 'Acidity')) + g('time', T('时长', 'Time')) + g('step', T('步骤', 'Step'))
    ctl = (f'<div class="ctl"><button class="chip" type="button" data-act="prev" aria-label="Prev">‹</button>'
           f'<button class="chip" type="button" data-act="play">▶</button><button class="chip" type="button" data-act="next" aria-label="Next">›</button></div>')
    return (f'<section class="ch" id="make">{plate("make", "plate-make")}{lede("make")}<div class="wide"><div class="sec">'
            f'<div class="bench fade" id="bench"><div class="pick"><h4>{bi(E.BENCH_HEAD)}</h4><div class="styles"></div><p class="fam small" style="margin:16px 0 0;color:#8F806B"></p></div>'
            f'<div class="main"><div class="shot"><div class="lab"></div><div class="cap"></div></div><div class="gauges">{gauges}</div><div class="say"></div><div class="rail">{ctl}<div class="steps"></div></div></div></div>'
            f'<p class="small" style="margin-top:12px">{bi(E.BENCH_NOTE)}</p></div>'
            f'<div class="sec">{sec_h("AGEING", E.AGE_HEAD)}<div class="agebar fade" id="agebar"></div></div>'
            '</div></section>')

# ---------- 02 品鉴 ----------
def ch_taste():
    tips = ''.join(f'<div><b>{bi(T(t["zh"].split("：")[0], t["en"].split(":")[0]))}</b><p>{bi(T(esc(t["zh"].split("：", 1)[-1]), esc(t["en"].split(":", 1)[-1].strip())))}</p></div>' for t in B['tasting'])
    return (f'<section class="ch" id="taste">{plate("taste", "plate-taste")}{lede("taste")}<div class="wide">'
            f'<div class="sec">{sec_h("HOW TO", E.TASTE_HEAD)}<div class="decode fade">{tips}</div></div>'
            f'<div class="sec">{sec_h("SPECTRUM", E.SPEC_HEAD, E.SPEC_NOTE)}<div class="spec" id="spec"><div><div class="filters lens"></div><div class="plot"><div class="cv"></div></div></div><div class="side"></div></div></div>'
            f'<div class="sec">{sec_h("WHEEL", E.WHEEL["title"])}<div class="wheelwrap" id="wheel"><div class="wheel"></div><div class="wheelinfo"></div></div></div>'
            f'<div class="sec" id="pairs">{sec_h("PAIRING", E.PAIR_HEAD)}<ul class="principles fade">' + ''.join(f'<li>{bi(T(esc(x["zh"]), esc(x["en"])))}</li>' for x in B['pairing']['principles']) + '</ul><div class="lens"></div><div class="pairs"></div></div>'
            '</div></section>')

# ---------- 03 全球 ----------
def ch_world():
    ms = ''.join(f'<div class="method fade"><b>{bi(T(m.get("short_zh") or m["zh"], m.get("short_en") or m["en"]))}</b><p>{bi(T(esc(m["principle_zh"]), esc(m["principle_en"])))}</p>'
                 + (f'<p class="small" style="color:var(--amber-ink)">{bi(T(esc(m["aw_note_zh"]), esc(m["aw_note_en"])))}</p>' if m.get('aw_note_zh') else '') + '</div>' for m in C['methods'])
    return (f'<section class="ch" id="world">{plate("world", "plate-world")}{lede("world")}<div class="wide">'
            f'<div class="sec">{sec_h("PRINCIPLES", E.WORLD_HEAD)}<div class="methods">{ms}</div></div>'
            f'<div class="sec">{sec_h("ATLAS", E.WORLD_LIST_HEAD)}<div data-list="world"><div class="lens"></div><div class="list"></div></div></div>'
            '</div></section>')

def world_data():
    M = {m['id']: m for m in C['methods']}
    items = []
    for it in C['items']:
        if it.get('drop'): continue
        facts = []
        if it.get('how_zh'): facts.append(dict(k=T('做法', 'How'), zh=esc(it['how_zh']), en=esc(it['how_en'])))
        if it.get('flavor_zh'): facts.append(dict(k=T('味道', 'Taste'), zh=esc(it['flavor_zh']), en=esc(it['flavor_en'])))
        if it.get('shelf_zh'): facts.append(dict(k=T('能放多久', 'Keeps'), zh=esc(it['shelf_zh']), en=esc(it.get('shelf_en') or '')))
        for h in it.get('history', []):
            if h.get('conf') == '低': continue
            facts.append(dict(k=yk(h.get('year')), zh=esc(h['zh']), en=esc(h['en']), src=(h.get('sources') or [{}])[0].get('url')))
        mid = it['method_id']; also = [M[x] for x in it.get('method_also_ids', []) if x in M]
        sub = T(' · '.join([M[mid]['short_zh']] + [m['short_zh'] for m in also]), ' · '.join([M[mid]['short_en']] + [m['short_en'] for m in also]))
        k = 'w-' + it['id']
        items.append(dict(id=it['id'], title=T(it['name_short_zh'], it['name_short_en']), sub=T(it['region'].split('（')[0] + ' · ' + sub['zh'], it['region_en'].split(' (')[0] + ' · ' + sub['en']),
                          one=T(it['one_zh'], it['one_en']), facts=facts, img=src(k), cap=cred(k), g=dict(method=mid, area=it['area'])))
    lenses = [dict(id='method', zh='按原理', en='By principle', groups=[dict(id=m['id'], zh=m['short_zh'], en=m['short_en']) for m in C['methods']]),
              dict(id='area', zh='按地区', en='By region', groups=[dict(id=a, **n) for a, n in E.AREAS])]
    return items, lenses

# ---------- 卷末 ----------
def all_sources():
    seen, out = set(), []
    def walk(o):
        if isinstance(o, dict):
            for s in o.get('sources', []) or []:
                u = s.get('url')
                if u and u not in seen: seen.add(u); out.append(s)
            for v in o.values():
                if isinstance(v, (dict, list)): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for x in (A, B, C, D): walk(x)
    return out

def ch_end():
    srcs = all_sources()
    rf = '<ul>' + ''.join(f'<li><a href="{html.escape(s["url"])}" target="_blank" rel="noopener">{esc(s.get("title") or s["url"])}</a></li>' for s in srcs) + '</ul>'
    creds = ''
    for im in IMGS.values():
        if im['key'].endswith('-mobile'): continue
        lic = f'<a href="{html.escape(im["license_url"])}" target="_blank" rel="noopener">{esc(im["license"])}</a>' if im.get('license_url') else esc(im.get('license') or '')
        creds += f'<li>{bi(T(esc(im["zh"]), esc(im["en"])))} — <a href="{html.escape(im["page"] or "")}" target="_blank" rel="noopener">{esc(im["author"])}</a> · {lic}</li>'
    pending = getattr(E, 'PENDING', [])
    return (f'<section class="ch" id="end"><div class="wide"><div class="sec endm">{sec_h("NOTES", T("卷末", "Notes"))}'
            f'<details class="fold"><summary>{bi(T("方法", "Method"))}</summary><div class="fb">{bi(E.METHOD, "p")}</div></details>'
            + (f'<details class="fold"><summary>{bi(T("仍待核实", "Still to verify"))}</summary><div class="fb"><ul>' + ''.join(f'<li>{bi(x)}</li>' for x in pending) + '</ul></div></details>' if pending else '')
            + f'<details class="fold"><summary>{bi(T("参考来源", "Sources"))} <span class="small">({len(srcs)})</span></summary><div class="fb">{rf}</div></details>'
            f'<details class="fold"><summary>{bi(T("图片署名", "Image credits"))}</summary><div class="fb"><ul>{creds}</ul></div></details>'
            f'<div class="stamp"><b>TIANJIE.ME · EXTRA</b><span class="small">{bi(T("号外 · 2026 年 11 月 9 日 · 天杰与 Claude 一起研究、写作、核查。错漏欢迎指正。", "Extra · 9 Nov 2026 · researched, written and checked by Tianjie with Claude. Corrections welcome."))}</span></div>'
            '</div></div></section>')

# ---------- 拼页 ----------
def data():
    world, wl = world_data()
    d = dict(meta=dict(title_zh=E.META['title_zh'], title_en=E.META['title_en']), stage=stage_data(), asia=asia_data(), world=world, lenses=dict(world=wl))
    d.update(make_data()); d.update(taste_data()); d.update(counter_data())
    return d

def main():
    body = hero() + thesis() + nav() + '<main>' + ch_hist() + ch_make() + ch_taste() + ch_world() + ch_counter() + ch_end() + '</main>'
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title_zh'])).replace('{{DESCRIPTION}}', esc(E.META['desc']))
            .replace('{{BODY}}', body).replace('{{DATA}}', json.dumps(data(), ensure_ascii=False).replace('</', '<\\/')).replace('{{APP}}', app))
    open(os.path.join(OUTD, 'index.html'), 'w', encoding='utf-8').write(page)
    meta = dict(slug=E.META['slug'], date=E.META['date'], title=E.META['title_zh'], subtitle=E.META['sub_zh'], summary=E.META['desc'],
                tags=['号外', '吃喝玩乐', '奶酪', '发酵', '湾区', '中英双语'], format='号外 · 时间轴舞台 · 工艺演示 · 品鉴光谱 · 风味轮 · 柜台导购', reading_time='20 分钟',
                cover='cover.png', cover_focus='#top', cover_scheme='dark')
    json.dump(meta, open(os.path.join(OUTD, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for w in ('待核', '本路', '本轮', 'TODO', '凭记忆', '未核', '建议页面', '骨架'):
        n = page.count(w)
        if n: print('  ! 泄漏词', w, n)
    print('wrote', os.path.relpath(os.path.join(OUTD, 'index.html')), f'{len(page)//1024} KB')


# ---------- 01 / 02 数据 ----------
FAM = {'fresh': 'fresh', 'soft-bloomy': 'bloomy', 'washed-rind': 'washed', 'semi-hard': 'semi', 'hard-pressed': 'hard', 'extra-hard': 'xhard', 'blue': 'blue', 'pasta-filata': 'pasta', 'brined': 'brine'}
FAMS = {f['id']: f for f in B['families']}
ORDER = ['mozzarella', 'feta', 'camembert', 'epoisses', 'roquefort', 'gouda', 'cheddar', 'emmental', 'comte', 'parmigiano']
COUNTRY = {'mozzarella': T('意大利', 'Italy'), 'feta': T('希腊', 'Greece'), 'camembert': T('法国', 'France'), 'epoisses': T('法国', 'France'), 'roquefort': T('法国', 'France'),
           'gouda': T('荷兰', 'Netherlands'), 'cheddar': T('英格兰', 'England'), 'emmental': T('瑞士', 'Switzerland'), 'comte': T('法国', 'France'), 'parmigiano': T('意大利', 'Italy')}
MILK = {'cow': T('牛奶', 'Cow'), 'goat': T('山羊奶', 'Goat'), 'sheep': T('绵羊奶', 'Sheep'), 'buffalo': T('水牛奶', 'Buffalo')}
import math

def make_data():
    STEPS = {s['id']: s for s in B['steps']}; SB = {s['id']: s for s in B['styles']}
    styles, age = [], []
    for sid in ORDER:
        s = SB[sid]; f = FAMS[s['family']]
        sk = 's-' + sid; simg = src(sk) or src('plate-make')
        steps = []
        for p in s['process']:
            g = STEPS[p['step']]
            ik = 'step-' + p['step']
            # 最后一步（熟成 / 鲜食）用这种奶酪自己的成品图；其余用工序图
            use = sk if p['step'] == 'ripen' and src(sk) else (ik if src(ik) else sk)
            sec = p.get('time_sec')
            steps.append(dict(title=T(g['zh'], g['en']), text=T(esc(p['note_zh']), esc(p['note_en'])), sci=T(esc(g['science_zh']), esc(g['science_en'])),
                              temp=p.get('temp_num'), td=T(p['temp_disp_zh'], p['temp_disp_en']) if p.get('temp_disp_zh') else None,
                              ph=p.get('ph_num'), phd=p.get('ph_disp'), time=T(p['time_zh'], p['time_en']) if p.get('time_zh') else None,
                              tf=round(min(1, math.log10(sec) / math.log10(9.5e7)), 3) if sec and sec >= 1 else None,
                              img=src(use) or simg, cap=cred(use) if src(use) else cred(sk)))
        styles.append(dict(id=sid, fam=FAM[s['family']], famName=T(f['short_zh'], f['short_en']), famdef=T(f['def_zh'], f['def_en']),
                           name=T(s['name_short_zh'], s['name_short_en']), origin=COUNTRY[sid], img=simg, cap=cred(sk), steps=steps))
        age.append(dict(id=sid, name=T(s['name_short_zh'], s['name_short_en']), fam=FAM[s['family']], min=s['age_days_min'], max=s['age_days_max']))
    return dict(bench=dict(styles=styles), age=age)

LABELED = {'ricotta', 'mozzarella-bufala', 'brie', 'camembert', 'feta', 'halloumi', 'young-gouda', 'epoisses', 'roquefort', 'stilton', 'mild-cheddar', 'aged-cheddar', 'comte-12', 'parmigiano-24', 'taleggio', 'gorgonzola-dolce'}
WHEEL_COL = {'lactic': '#EADBBE', 'fruity': '#E7B46A', 'floral': '#D9A3AE', 'brown': '#C88A52', 'vegetal': '#A8BC84', 'animal': '#C4A07C', 'mould': '#9CB2A6', 'spicy': '#D88E6B', 'taste': '#BCB0D4'}
PKIND = {'honey': 'sweet', 'fruit': 'sweet', 'nut': 'sweet', 'sake': 'spirit'}

def taste_data():
    spec = []
    for c in B['spectrum']:
        f = FAMS[c['family']]
        spec.append(dict(id=c['id'], name=T(c['name_zh'], c['name_en']), origin=T(c['origin_zh'], c['origin_en']), milk=' '.join(c['milk_tags']),
                         milkName=T('、'.join(MILK[m]['zh'] for m in c['milk_tags']), ', '.join(MILK[m]['en'] for m in c['milk_tags'])),
                         fam=FAM[c['family']], famName=T(f['short_zh'], f['short_en']), x=c['x_intensity_1_10'], y=c['y_texture_1_10'],
                         note=T(c['note_zh'], c['note_en']), pair=T(c['pair_zh'], c['pair_en']) if c.get('pair_zh') else None, label=c['id'] in LABELED))
    fams = [dict(id=FAM[f['id']], zh=f['short_zh'], en=f['short_en']) for f in B['families']]
    axes = []
    for a in B['wheel']['axes']:
        axes.append(dict(id=a['id'], zh=a['zh'], en=a['en'], color=WHEEL_COL.get(a['id'], '#CDBFA8'), desc=T(a.get('axis_desc_zh', ''), a.get('axis_desc_en', '')),
                         items=[dict(zh=x['zh'], en=x['en'], cheese=T(x.get('example_cheese') or '', x.get('example_en') or ''), compound=T(x.get('compound') or '', x.get('compound_en') or '')) for x in a['descriptors']]))
    kinds = [dict(id=k, **n) for k, n in E.PAIR_KINDS]
    items = [dict(kind=PKIND.get(p['kind'], p['kind']), cheese=T(p['cheese_zh'], p['cheese_en']), **{'with': T(p['with_zh'], p['with_en'])}, why=T(p['why_zh'], p['why_en'])) for p in B['pairing']['pairs']]
    return dict(spec=spec, fams=fams, flightTip=E.FLIGHT_TIP, wheel=dict(title=E.WHEEL['title'], intro=E.WHEEL['intro'], axes=axes), pairs=dict(kinds=kinds, items=items))

# ---------- 04 柜台（占位，待 D 完成后替换） ----------
def ch_counter():
    return '<section class="ch" id="counter"><div class="wide"><div class="sec"></div></div></section>'
def counter_data():
    return {}

if __name__ == '__main__': main()
