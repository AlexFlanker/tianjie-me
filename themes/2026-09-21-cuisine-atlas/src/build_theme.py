#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 1 题「中国菜系演化图谱」v2：把 shell.html（新外壳：卷首、导航、论点）+ atlas.*（v1 的地图、时期面板、四维长卷、各地沿革）
+ content/*.js + map_data.json + palette*.json 拼成 ../index.html，并更新 ../meta.json。

  python3 themes/2026-09-21-cuisine-atlas/src/build_theme.py

改 v1 的内容数据仍只改 src/content/*.js；新写的文案在 src/editorial2.py；图片记录在 src/images.json。
v1 的单文件模板 template.html 已于 2026-10-30 拆成 atlas.css / atlas.html / atlas.js（git 历史里有原文件）。
"""
import json, os, sys, html

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import editorial2 as E2

SITE_URL = 'https://tianjie.me/t/cuisine-atlas/'
TITLE = '中国菜系演化图谱'
esc = lambda s: html.escape(str(s), quote=True)
rd = lambda f: open(os.path.join(SRC, f), encoding='utf-8').read()

IM = {i['id']: i for i in json.load(open(os.path.join(SRC, 'images.json'), encoding='utf-8')) if i.get('status') == 'ok'}

# ---------- v1 数据：内容、地图、配色
content = ''.join(rd(os.path.join('content', f)) + '\n' for f in ['c_meta.js', 'c_p1.js', 'c_p2.js', 'c_p3.js', 'c_modern.js'])
pal = json.load(open(os.path.join(SRC, 'palette.json')))
spec = json.load(open(os.path.join(SRC, 'palette_spec.json')))
mp = json.load(open(os.path.join(SRC, 'map_data.json')))
ded = []                                   # 南海诸岛的小岛点抽稀，避免插图里堆成一团
for x, y in mp['islands']:
    if all(abs(x - a) > 5 or abs(y - b) > 5 for a, b in ded): ded.append((x, y))
mp['islands'] = [[x, y] for x, y in ded]
def css_vars(mode): return ''.join(f'--{k}:{v};' for k, v in pal[mode].items())
palmeta = {'light': {}, 'dark': {}}       # 填色较深（OKLCH L < 0.58）时省名用浅色字
for mode in ('light', 'dark'):
    for group in ('fam', 'taste', 'staple'):
        for k, (h, c, l) in spec[group][mode].items():
            if l < 0.58: palmeta[mode][f'{group}-{k}'] = True

# ---------- 新外壳
def hero():
    H = E2.HERO2; im = IM[H['img']]; b = 'assets/' + H['img']
    title = ''.join(f'<span>{esc(t)}</span>' for t in H['title'])
    sub = ''.join(f'<span>{esc(x)}</span>' for x in H['sub'])
    arrow = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5"/></svg>'
    return f'''<header class="h3" id="top">
  <figure class="h3img"><picture>
    <source media="(max-aspect-ratio: 4/5) and (min-width: 701px)" srcset="{b}-t1024.jpg 1024w, {b}-t1536.jpg 1536w" sizes="100vw">
    <source media="(max-aspect-ratio: 4/5)" srcset="{b}-p960.jpg 960w, {b}-p1440.jpg 1440w" sizes="(max-aspect-ratio: 9/16) 57vh, 100vw">
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
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n}</small>{esc(t)}</a>' for cid, n, t in E2.NAV)
    links += '<button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="换成深色">夜里读</button>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def tagline_sec():
    lines, k = [], 0
    for ln in E2.TAGLINE.split('/'):
        ws = []
        for w in ln.split('|'):
            key = w.startswith('*'); w = w.lstrip('*')
            ws.append(f'<span class="w{" k" if key else ""}" style="--i:{k}">{esc(w.rstrip())}</span>' + (' ' if w.endswith(' ') else '')); k += 1
        lines.append('<span class="ln">' + ''.join(ws) + '</span>')
    plain = E2.TAGLINE.replace('|', '').replace('/', '').replace('*', '')
    nums = ''.join(f'<div class="tn"><b>{esc(v)}<small>{esc(u)}</small></b><p>{esc(t)}</p></div>' for v, u, t in E2.NUMS)
    return f'''<section class="tagsec" id="tagsec" aria-label="这一页的论点"><div class="tagstick"><div class="wide">
<p class="tagl" aria-label="{esc(plain)}"><span aria-hidden="true">{''.join(lines)}</span></p>
<div class="tagrest"><p>{esc(E2.TAGREST)}</p><div class="tnums">{nums}</div></div>
</div></div></section>'''

def atlas_body():
    A = E2.ATLAS_HEAD
    head = (f'<header class="sech fade" id="atlas"><p class="cno">{esc(A["kicker"])}</p><h2>{esc(A["title"])}</h2>'
            f'<p class="slede">{esc(A["lede"])}</p></header>')
    body = rd('atlas.html')
    assert body.count('<div class="wrap">') == 1
    return body.replace('<div class="wrap">', '<div class="wrap">\n  ' + head, 1)

def main():
    shell = rd('shell.html')
    favicon = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%23b5432c'/%3E"
               "%3Ctext x='32' y='44' font-size='34' text-anchor='middle' font-family='Noto Serif SC,Songti SC,serif' font-weight='700' fill='%23fff'%3E味%3C/text%3E%3C/svg%3E")
    v1js = (rd('atlas.js').replace('/*DATA*/', content)
            .replace('/*MAP*/', 'const MAP = ' + json.dumps(mp, ensure_ascii=False, separators=(',', ':')) + ';')
            .replace('/*PALMETA*/', 'const PALMETA = ' + json.dumps(palmeta, separators=(',', ':')) + ';'))
    body = hero() + '\n' + cnav() + '\n<main>\n' + tagline_sec() + '\n' + atlas_body() + '</main>\n'
    page = shell
    for k, v in (('{{TITLE}}', esc(TITLE)), ('{{DESCRIPTION}}', esc(E2.META_DESC)), ('{{CANONICAL}}', SITE_URL), ('{{FAVICON}}', favicon),
                 ('{{PAL_LIGHT}}', css_vars('light')), ('{{PAL_DARK}}', css_vars('dark')), ('{{V1_CSS}}', rd('atlas.css')),
                 ('{{BODY}}', body), ('{{V1_SCRIPT}}', v1js), ('{{APP_JS}}', rd('app.js'))):
        assert page.count(k) >= 1, k
        page = page.replace(k, v)
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    mpath = os.path.join(ROOT, 'meta.json'); meta = json.load(open(mpath, encoding='utf-8'))
    meta.update({'summary': E2.META_DESC, 'cover_focus': '#top', 'cover_scheme': 'light'})
    json.dump(meta, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(mpath, 'a').write('\n')
    print('wrote index.html', f'{len(page.encode("utf-8")) / 1024:.0f} KB')

if __name__ == '__main__':
    main()
