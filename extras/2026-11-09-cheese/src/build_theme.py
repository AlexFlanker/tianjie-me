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

def lede(cid):
    return f'<div class="wide"><p class="lede fade">{bi(E.CH[cid]["lede"])}</p></div>'
