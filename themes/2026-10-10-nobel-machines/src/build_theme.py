#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 4 题《把预言造出来》：由 src/{template.html, content.json, world.json, app.js, figs_*.py} 生成 ../index.html

  python3 themes/2026-10-10-nobel-machines/src/make_content.py   # 研究底稿 + 编辑稿 → content.json
  python3 themes/2026-10-10-nobel-machines/src/build_theme.py    # 生成 index.html
"""
import html
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs_base as FB
import figs_machines as FM
import figs_charts as FC

OUT = os.path.join(os.path.dirname(HERE), 'index.html')
C = json.load(open(os.path.join(HERE, 'content.json'), encoding='utf-8'))
WORLD = json.load(open(os.path.join(HERE, 'world.json'), encoding='utf-8'))
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
app_js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
M = C['machines']
IMG = json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))['groups']
MID = {m['id']: m for m in M}
CIRC = '①②③④'


SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def esc(s):
    """转义，并把 10^-15 这样的写法换成上标。"""
    t = html.escape(str(s if s is not None else ''), quote=True)
    return re.sub(r'10\^(-?\d+)', lambda m: '10' + m.group(1).translate(SUP), t)


def link(t, u):
    t = esc(t)
    return f'<a href="{esc(u)}" target="_blank" rel="noopener">{t}</a>' if u else t


def conf(c):
    cls = {'高': 'h', '中': 'm', '低': 'l'}.get((c or '中')[:1], 'm')
    return f'<span class="conf {cls}">置信 {esc((c or "中")[:1])}</span>'


def srcs(ss):
    return '；'.join(link(s['t'], s['u']) for s in ss if s.get('t'))


def chead(no, title, lede):
    return (f'<div class="chead fade"><div class="cno">{esc(no)}</div><h2>{esc(title)}</h2>'
            f'<p class="lede">{esc(lede)}</p></div>')


def pct(v):
    return f'{max(0.0, min(100.0, v)):.2f}%'


# ------------------------------------------------------------------ 卷首
def hero():
    m = C['meta']
    steps = ''.join(f'<li>{esc(s)}</li>' for s in m['steps'])
    return f'''
<header class="hero" id="top"><div class="wide">
<div class="strip"><span><b>题号</b>一周一题 第四题</span><span><b>格式</b>图谱</span><span><b>日期</b>{esc(m['date'])}</span></div>
<h1>{esc(m['title'])}</h1>
<p class="sub">{esc(m['subtitle'])}</p>
<div class="dimline" aria-hidden="true"><span>1887</span><i></i><b>139 年，十二份任务书</b><i></i><span>2026</span></div>
<div class="hero-grid" data-cover-hide><p class="thesis">{esc(m['thesis'])}</p><ol class="steps">{steps}</ol></div>
<figure class="rulerfig" id="keyvis">{FC.hero_ruler_h()}{FC.hero_ruler_v()}<figcaption data-cover-hide>{esc(m['ruler_note'])}</figcaption></figure>
</div></header>'''


def nav():
    row = ''
    for cid, name, no in C['chapters']:
        sm = f'<small>{esc(no)}</small>' if no else ''
        row += f'<a href="#{cid}" data-nav="{cid}"{" class=on" if cid == "top" else ""}>{sm}{esc(name)}</a>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{row}</div><div class="prog" id="prog"></div></nav>'


# ------------------------------------------------------------------ 第 1 章
def ch1():
    c = C['ch1']
    hooks = ''.join(f'<li><b>{esc(h["h"])}</b><p>{esc(h["p"])}</p></li>' for h in c['hooks'])
    cites = ''
    for x in c['citations']:
        en = esc(x['en']).replace('decisive contributions', '<mark>decisive contributions</mark>')
        cites += (f'<div class="cite"><div class="y">{x["year"]}</div><div class="w">{esc(x["who"])}</div>'
                  f'<p class="en" lang="en">{en}</p><p class="zh">{esc(x["zh"])}</p><span class="n">{esc(x["names"])}</span></div>')
    lo, hi = -1.0, 9.4
    rows = ('<div class="rw axis"><div class="lb"></div><div class="trk">'
            + ''.join(f'<i class="g" style="left:{pct((d - lo) / (hi - lo) * 100)}"></i><span style="left:{pct((d - lo) / (hi - lo) * 100)}">{t}</span>'
                      for d, t in ((0, '1 吨'), (3, '1,000 吨'), (6, '100 万吨'), (9, '10 亿吨')))
            + '</div></div>')
    for n in c['nu']:
        p = (math.log10(n['mass_t']) - lo) / (hi - lo) * 100
        left = p > 62
        rows += (f'<div class="rw"><div class="lb"><b>{n["built"]}</b>{esc(n["what"])}<small>{esc(n["result"])}；{esc(n["prize"])}</small></div>'
                 f'<div class="trk"><i class="stem" style="left:0;width:{pct(p)}"></i><i class="dot" style="left:{pct(p)}"></i>'
                 f'<span class="n{" l" if left else ""}" style="left:{pct(p)}">{esc(n["mass"])}</span></div></div>')
    q = c['quote']
    return f'''
<section class="chap" id="c1"><div class="wide">
{chead('图 01', '今年的奖', c['lede'])}
<div class="c1-grid fade">
  <div><p>{esc(c['who'])}</p>
    <div class="quote"><p>「{esc(q['zh'])}」</p><p class="en" lang="en">{esc(q['en'])}</p><cite>{link(q['by'], q['url'])}</cite></div>
    <div class="note-card" style="margin-top:28px"><b>{esc(c['program']['h'])}</b><p>{esc(c['program']['p'])}</p><p class="small" style="margin-top:6px">出处：{esc(c['program']['src'])}。</p></div></div>
  <ul class="hooks">{hooks}</ul>
</div>
<h3 class="sub-h fade">四句颁奖词，同一个词</h3>
<div class="cites fade">{cites}</div>
<p class="small" style="margin-top:10px">{esc(c['cite_note'])}</p>
<h3 class="sub-h fade">五次中微子奖用的装置，按建成年份排</h3>
<div class="rows fade" aria-label="中微子探测器的靶质量，对数坐标">{rows}</div>
<p class="small" style="margin-top:10px">横轴是对数。{esc(c['nu_note'])}</p>
<div class="note-card col fade" style="margin-top:clamp(26px,4vw,44px)"><b>{esc(c['china']['h'])}</b><p>{esc(c['china']['p'])}</p></div>
<p class="bridge fade">{esc(c['bridge'])}</p>
</div></section>'''


# ------------------------------------------------------------------ 第 2 章
def facts_html(card):
    fs = ''
    for x in card['facts']:
        nt = f'<span class="nt">口径：{esc(x["note"])}</span>' if x.get('note') else ''
        fs += f'<li>{esc(x["text"])}{conf(x.get("confidence"))}{nt}<span class="src">{srcs(x["sources"])}</span></li>'
    out = f'<ul class="facts">{fs}</ul>'
    if card.get('disputes'):
        out += '<div class="dh">来源对不上的地方</div><ul class="plain">' + ''.join(f'<li>{esc(d)}</li>' for d in card['disputes']) + '</ul>'
    if card.get('todo'):
        out += '<div class="dh">没有核到的</div><ul class="plain">' + ''.join(f'<li>{esc(d)}</li>' for d in card['todo']) + '</ul>'
    return out


def fmt_len(v):
    if v >= 1000:
        x = v / 1000
        return (f'{x:,.0f}' if x >= 10 else f'{x:g}'), '公里'
    return f'{v:g}', '米'


def fmt_mass(v):
    if v >= 1e8:
        return f'{v / 1e8:g}', '亿吨'
    if v >= 1e4:
        return f'{v / 1e4:g}', '万吨'
    return (f'{v:,.0f}' if v >= 10 else f'{v:g}'), '吨'


def readout(m):
    """卡片顶上的读数条：尺度、质量、人数、从成果到获奖的年数。没有核到的不显示。"""
    t = m['tool']
    cells = []
    if t.get('size_m'):
        v, u = fmt_len(t['size_m'])
        cells.append(('尺度', v, u, t.get('size_what', '')))
    if t.get('mass_t'):
        v, u = fmt_mass(t['mass_t'])
        cells.append(('质量', v, u, t.get('mass_what', '')))
    if t.get('people'):
        cells.append(('人', f'{t["people"]:,}', '人', t.get('people_what', '')))
    cells.append(('从成果到获奖', str(t['wait']), '年', f'{t["t_result"]} 年出成果，{t["t_prize"]} 年获奖'))
    return ''.join(f'<div><dt>{esc(k)}</dt><dd><b>{esc(v)}</b><i>{esc(u)}</i></dd><small>{esc(w)}</small></div>' for k, v, u, w in cells)


def gallery_html(m):
    """每座装置一条图片带：第一张是大图，其余是小图；点开看图注、署名与出处。"""
    imgs = IMG.get(m['id'], [])
    if not imgs:
        return ''
    tiles = ''
    for i, g in enumerate(imgs):
        cls = 'g-t' + (' g-lead' if i == 0 else '') + (' plate' if g['kind'] == 'plate' else '') + (' bk' if g.get('bg') == 'black' else '')
        tiles += (f'<button type="button" class="{cls}" data-g="{m["id"]}" data-i="{i}" aria-label="放大：{esc(g["title"])}">'
                  f'<img src="{esc(g["file"])}" width="{g["w"]}" height="{g["h"]}" loading="lazy" decoding="async" alt="{esc(g["title"])}">'
                  f'<span class="g-n">{m["no"]:02d}-{chr(65 + i)}</span>'
                  f'<span class="g-c"><i>{esc(g["role_zh"])}</i>{esc(g["title"])}</span></button>')
    others = len(imgs) - 1
    if others % 2 == 1:
        tiles += (f'<div class="g-info"><b>{len(imgs)}</b><span>张图<br>点开看图注、署名与出处</span></div>')
        others += 1
    cols = max(1, others // 2)
    roles = '、'.join(dict.fromkeys(g['role_zh'] for g in imgs))
    return (f'<div class="m-gal fade" data-cols="{cols}"><div class="g-bar"><span>图片陈列 {m["no"]:02d}</span><span>{len(imgs)} 张：{esc(roles)}</span></div>'
            f'<div class="g-grid" style="grid-template-columns:minmax(0,{cols}fr) repeat({cols},minmax(0,1fr))">{tiles}</div></div>')


def credits_html():
    rows = ''
    for m in M:
        for i, g in enumerate(IMG.get(m['id'], [])):
            rows += (f'<tr><td>{m["no"]:02d}-{chr(65 + i)}</td><td>{esc(m["short"])}：{esc(g["title"])}</td><td>{esc(g["credit"])}</td>'
                     f'<td>{esc(g["license"])}</td><td>{link("来源", g["source_url"])}</td></tr>')
    n = sum(len(v) for v in IMG.values())
    return (f'<div class="credits"><h3>图片署名</h3>'
            f'<p class="small">共 {n} 张，按装置排列。公有领域与知识共享许可的图可照许可转用；标「机构条款」的只许用于教育、信息或非商业用途，版权仍归原机构，转载请回到来源页看条款。个别图为排版做了裁边、缩小，气泡室两张做了水平翻转（原翻拍片左右颠倒）。</p>'
            f'<div class="tbl"><table><thead><tr><th>图号</th><th>内容</th><th>署名</th><th>许可</th><th></th></tr></thead><tbody>{rows}</tbody></table></div></div>')


def card_html(m):
    no = m['no']
    pz = m['prize']
    who = ''
    for l in pz['laureates']:
        share = f'，{esc(l["share"])}' if l.get('share') and l['share'] != '全奖' else ''
        who += (f'<div class="who"><b>{esc(l["zh"])}</b> <span>{esc(l["en"])}，{esc(l["life"])}{share}</span><br>'
                f'<span>{esc(l["role"])}</span></div>')
    crit = ''.join(CIRC[i - 1] for i in m['criteria'])
    tb = [('图号', f'02-{no:02d}'), ('项目', m['short']), ('获奖', f'{pz["year"]} 年'),
          ('年代', m['era']), ('地点', m['place']), ('入围标准', crit)]
    tblock = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in tb)
    brief = ''.join(f'<li>{esc(b)}</li>' for b in m['brief'])
    scale = ''
    for s in m['scale']:
        note = s.get('note') or ''
        if ('造价' in s['k'] or '经费' in s['k']) and m['cost'].get('approx'):
            note = (note + '；' if note else '') + '折算：' + m['cost']['approx'] + '（按当年汇率和美国物价指数粗算）'
        sm = f'<small>{esc(note)}</small>' if note else ''
        scale += f'<div><dt>{esc(s["k"])}</dt><dd>{esc(s["v"])}{sm}</dd></div>'
    approach = ''.join(f'<li><span>{esc(a)}</span></li>' for a in m['approach'])
    people = ''.join(f'<li><b>{esc(p["name"])}</b>　{esc(p["r"])}</li>' for p in m['people'])
    anec = ''.join(f'<li>{esc(a["t"])}<small>{esc(a["kind"])}</small></li>' for a in m['anecdotes'])
    hist = ''.join(f'<li><b>{esc(h["d"])}</b><span>{esc(h["t"])}</span></li>' for h in m['history'])
    awards = ''.join(f'<li>{esc(a)}</li>' for a in m['awards'])
    cnote = f'<p class="small">入围标准：{esc(m["criteria_note"])}</p>' if m.get('criteria_note') else ''
    ssc = '<p class="small">同一类机器的反例 SSC，见 <a href="#ssc">工程思维一章的末尾</a>。</p>' if m['id'] == 'lhc' else ''
    ls = m['lesson']
    return f'''
<article class="m" id="m-{m['id']}">
  <header class="m-head">
    <div class="m-plate"><span>图 02-{no:02d}</span><span>{no:02d} / 12</span><span>{esc(m['era'])}</span><span>{esc(m['place'])}</span><span>{pz['year']} 年获奖</span></div>
    <h3>{esc(m['short'])}<small>{esc(m['name'])}　{esc(m['name_en'])}</small></h3>
    <p class="tag">{esc(m['tag'])}</p>
    <dl class="readout">{readout(m)}</dl>
  </header>
  {gallery_html(m)}
  <div class="m-fig">
    <div class="frame"><button type="button" class="zb" aria-pressed="false">放大</button>{FM.FIGS[m['id']]()}</div>
    <div class="tblock"><div class="kp">{FC.keyplan(m)}</div><dl>{tblock}</dl></div>
    <div class="tl">{FC.tl_strip(m, M)}</div>
  </div>
  <div class="m-txt">
    <div class="prize"><div class="who"><b>{pz['year']} 年诺贝尔物理学奖</b></div>{who}
      <blockquote lang="en">{esc(pz['citation_en'])}</blockquote><p class="zh">{esc(pz['citation_zh'])}　<span class="small">（{link(pz['citation_src']['t'], pz['citation_src']['u'])}）</span></p></div>
    <h4>预言</h4><p class="claim">{esc(m['claim'])}</p>
    <h4>任务书</h4><ul class="brief">{brief}</ul>
    <h4>规模</h4><dl class="scale">{scale}</dl>
    <h4>思路</h4><ol class="approach">{approach}</ol>
    <h4>人</h4><ul class="people">{people}</ul>
    <h4>逸闻</h4><ul class="anec">{anec}</ul>
    <div class="lesson-link"><small>工程思维</small><b>{esc(ls['principle'])}</b><a href="#l-{m['id']}">看这一条怎么换到自己的工作里</a></div>
    {f'<p class="lineage">传承：{esc(m["lineage"])}</p>' if m.get('lineage') else ''}
    {cnote}{ssc}
    <div class="m-more">
      <details><summary><span>历程<small>{len(m['history'])} 个节点</small></span></summary><ol class="hist">{hist}</ol></details>
      {f'<details><summary><span>奖项<small>诺奖之外</small></span></summary><ul class="plain">{awards}</ul></details>' if awards else ''}
      <details><summary><span>资料与置信度<small>{len(m['facts'])} 条事实</small></span></summary>{facts_html(m)}</details>
    </div>
  </div>
</article>'''


def cmp_tool():
    opts = '<optgroup label="十二座装置">' + ''.join(f'<option value="{m["id"]}">{m["prize"]["year"]} {esc(m["short"])}</option>' for m in M) + '</optgroup>'
    groups = {}
    for x in C['extra_shapes']:
        groups.setdefault(x['group'], []).append(x)
    for g, xs in groups.items():
        opts += f'<optgroup label="{esc(g)}">' + ''.join(f'<option value="{x["id"]}">{esc(x["name"])}</option>' for x in xs) + '</optgroup>'
    return f'''
<div class="tool fade" id="cmp">
  <div class="tool-h"><h3>规模对比器</h3><p>任选两样，按同一比例并排画出来，再比质量、造价、人数和年数。</p></div>
  <div class="tool-b">
    <div>
      <div class="pick"><label for="cmp-a">左</label><select id="cmp-a">{opts}</select><label for="cmp-b">右</label><select id="cmp-b">{opts}</select></div>
      <svg id="cmp-svg" class="dwg" viewBox="0 0 600 300" role="img" aria-label="两样东西的同比例对比"></svg>
      <p class="cmp-say" id="cmp-say"></p>
    </div>
    <div class="tbl"><table id="cmp-tbl" style="min-width:0"><thead><tr><th></th><th id="cmp-ha"></th><th id="cmp-hb"></th></tr></thead><tbody></tbody></table>
      <p class="small" style="margin-top:10px">造价是「约合 2025 年美元」的粗算，算法见卷末「方法」；口径各不相同，只宜看量级。</p></div>
  </div>
</div>'''


def ch2():
    c = C['ch2']
    crit = ''.join(f'<li><b>{CIRC[i]}</b><span>{esc(t)}</span></li>' for i, t in enumerate(C['criteria']))
    cards = ''.join(card_html(m) for m in M)
    key = '　'.join(f'<b>{m["no"]}</b>{esc(m["short"])}' for m in M)
    return f'''
<section class="chap" id="c2"><div class="wide">
{chead('图 02', '十二座装置', c['lede'])}
<h4 style="margin-top:0">入围标准</h4>
<ul class="crit fade">{crit}</ul>
<figure class="fig map fade"><div class="frame">{FC.map_overview(M)}</div><figcaption>{esc(c['map_cap'])}<br>{key}</figcaption></figure>
{cards}
{cmp_tool()}
</div></section>'''


# ------------------------------------------------------------------ 第 3 章
def ch3():
    c = C['ch3']
    P = C['principles']
    head = '<div class="mx-h"><span>原则</span><span class="dots">' + ''.join(f'<span>{m["no"]}</span>' for m in M) + '</span></div>'
    rows = ''
    panels = ''
    for i, p in enumerate(P):
        ms = [e[0] for e in p['ev']]
        dots = ''.join(f'<i class="{"y" if m["id"] in ms else ""}" title="{esc(m["short"])}"></i>' for m in M)
        rows += (f'<a class="mx-r" href="#pp-{p["id"]}">'
                 f'<b><small>{i + 1:02d}</small>{esc(p["title"])}</b><span class="dots">{dots}</span></a>')
        ev = ''.join(f'<li><a href="#m-{mid}">{MID[mid]["prize"]["year"]} {esc(MID[mid]["short"])}</a><span>{esc(t)}</span></li>' for mid, t in p['ev'])
        panels += (f'<div class="pr-panel" id="pp-{p["id"]}"><h3><small>{i + 1:02d}</small>{esc(p["title"])}</h3>'
                   f'<p>{esc(p["text"])}</p><ul>{ev}</ul></div>')
    key = '　'.join(f'<b>{m["no"]}</b>{esc(m["short"])}' for m in M)
    lab = c['card_labels']
    ls = ''
    for m in M:
        l = m['lesson']
        ls += (f'<article class="ls" id="l-{m["id"]}" data-m="{m["id"]}"><div class="k">{m["no"]:02d}　{m["prize"]["year"]} {esc(m["short"])}</div>'
               f'<h3>{esc(l["principle"])}</h3><dl><dt>{lab[0]}</dt><dd>{esc(l["how"])}</dd><dt>{lab[2]}</dt><dd>{esc(l["engineer"])}</dd>'
               f'<dt>{lab[3]}</dt><dd>{esc(l["public"])}</dd></dl></article>')
    s = C['ssc']
    ct = MID['lhc']['counter']
    nums = ''.join(f'<div><dt>{esc(x["k"])}</dt><dd>{esc(x["v"])}</dd></div>' for x in ct['numbers'])
    contrast = ''.join(f'<li>{esc(x)}</li>' for x in ct['contrast'])
    return f'''
<section class="band" id="c3"><div class="wide">
{chead('图 03', '工程思维', c['lede'])}
<h3 class="sub-h fade" style="margin-top:0">十二座装置，各一条</h3>
<div class="lessons" id="lessons">{ls}</div>
<h3 class="sub-h fade">归并成十条</h3>
<div class="mx fade" id="mx">{head}{rows}</div>
<p class="mx-key">{key}</p>
<p class="small" style="margin-top:4px">{esc(c['matrix_cap'])}</p>
<div id="pp">{panels}</div>
<div class="ssc fade" id="ssc"><h3>{esc(s['h'])}</h3><p style="margin:8px 0 0;color:var(--band-ink-2);max-width:46em">{esc(s['lede'])}</p>
<dl class="nums">{nums}</dl><ul>{contrast}</ul><p style="margin:14px 0 0;max-width:46em;color:var(--band-ink-2)">{esc(s['close'])}</p></div>
</div></section>'''


# ------------------------------------------------------------------ 第 4 章
def srcs_html(sources):
    """来源的紧凑写法：「出处 1 2 3」，每个编号是一个链接，完整标题放在 title 里。"""
    out = ''
    for i, s in enumerate(sources or [], 1):
        t = esc(s.get('t', ''))
        if s.get('u'):
            out += f'<a href="{esc(s["u"])}" title="{t}" aria-label="出处 {i}：{t}" target="_blank" rel="noopener">{i}</a>'
        else:
            out += f'<span title="{t}">{i}</span>'
    return f'<span class="srcs">出处{out}</span>' if out else ''


def bench_card(b):
    return (f'<article class="bc" id="b-{b["id"]}"><div class="y">{b["year"]}</div><div class="w">{esc(b["who"])}</div>'
            f'<h3>{esc(b["what"])}</h3><p>{esc(b["line"])}</p><div class="num">{esc(b["number"])}</div>'
            f'<div class="ls1">{esc(b["lesson"])}{conf(b.get("confidence"))}</div>{srcs_html(b.get("sources"))}</article>')


def team_rows():
    hi = math.log10(20000)
    ax = ''.join(f'<i class="g" style="left:{pct(math.log10(v) / hi * 100)}"></i><span class="{cls}" style="left:{pct(math.log10(v) / hi * 100)}">{t}</span>'
                 for v, t, cls in ((1, '1 人', 's'), (10, '10', ''), (100, '100', ''), (1000, '1,000', ''), (10000, '1 万', '')))
    rows = f'<div class="rw axis"><div class="lb"></div><div class="trk">{ax}</div></div>'
    for m in M:
        t = m['tool']
        nl = 1 if m['id'] == 'homestake' else len(m['prize']['laureates'])
        sq = '<span class="sqs">' + '<i></i>' * nl + '</span>'
        if t.get('people'):
            p = math.log10(t['people']) / hi * 100
            mark = (f'<i class="stem" style="left:0;width:{pct(p)}"></i><i class="dot" style="left:{pct(p)}"></i>'
                    f'<span class="n{" l" if p > 70 else ""}" style="left:{pct(p)}">{t["people"]:,} 人</span>')
        else:
            p = math.log10(300) / hi * 100
            mark = f'<i class="dot h" style="left:{pct(p)}"></i><span class="n" style="left:{pct(p)}">数百人，没有确数</span>'
        rows += (f'<div class="rw"><div class="lb">{sq}<b>{m["prize"]["year"]}</b>{esc(m["laur"])}<small>{esc(t["people_what"])}</small></div>'
                 f'<div class="trk">{mark}</div></div>')
    return rows


def wait_rows():
    a, b = 1880, 2030

    def P(y):
        return (y - a) / (b - a) * 100
    ax = ''.join(f'<i class="g" style="left:{pct(P(y))}"></i><span style="left:{pct(P(y))}">{y}</span>' for y in (1900, 1925, 1950, 1975, 2000, 2025))
    rows = f'<div class="rw axis"><div class="lb"></div><div class="trk">{ax}</div></div>'
    for m in M:
        t = m['tool']
        late = t['t_prize'] > 1990
        npos = P(t['t_idea']) if late else P(t['t_prize'])
        rows += (f'<div class="rw"><div class="lb"><b>{t["t_prize"]}</b>{esc(m["short"])}</div><div class="trk">'
                 f'<i class="thin" style="left:{pct(P(t["t_idea"]))};width:{pct(P(t["t_result"]) - P(t["t_idea"]))}"></i>'
                 f'<i class="thick" style="left:{pct(P(t["t_result"]))};width:{pct(P(t["t_prize"]) - P(t["t_result"]))}"></i>'
                 f'<i class="dot" style="left:{pct(P(t["t_prize"]))}"></i>'
                 f'<span class="n{" l" if late else ""}" style="left:{pct(npos)}" data-wait="等了 {t["wait"]} 年" data-span="共 {t["span"]} 年">等了 {t["wait"]} 年</span>'
                 f'</div></div>')
    return rows


def ch4():
    c = C['ch4']
    r = C['rontgen']
    bench = ''.join(bench_card(b) for b in C['bench'])
    eng = ''
    for gname, names in c['eng_groups']:
        lis = ''
        for e in C['engineers']:
            if any(n in e['zh'] for n in names):
                lis += f'<li><b>{e["year"]}</b><span>{esc(e["zh"])}：{esc(e["for"])}<small>{esc(e["why"])}{conf(e.get("confidence"))}{srcs_html(e.get("sources"))}</small></span></li>'
        eng += f'<div><h4>{esc(gname)}</h4><ul>{lis}</ul></div>'
    bt = ''.join(f'<tr><td>{b["year"]}</td><td>{esc(b["what"])}</td><td>{(str(format(b["people"], ",")) + " 人") if b.get("people") else ""}</td><td>{esc(b["money"])}</td></tr>'
                 for b in C['breakthrough'])
    return f'''
<section class="chap" id="c4"><div class="wide">
{chead('图 04', '候补席与三张旁表', c['lede'])}
<div class="rt fade"><div><div class="n">1901</div><h3 style="font-size:22px;margin-top:6px">{esc(c['rontgen_h'])}</h3><p>{esc(c['rontgen_p'])}</p></div>
<div><p style="margin-top:0"><b>{esc(r['who'])}</b>：{esc(r['what'])}。{esc(r['line'])}</p><p>{esc(r['number'])}。</p>
<p class="small" lang="en" style="margin-top:8px">{esc(r['citation_en'])}</p><p class="small">{esc(r['citation_zh'])}{conf(r.get('confidence'))}{srcs_html(r.get('sources'))}</p></div></div>
<div class="bench fade">{bench}</div>

<div class="side fade" id="side-eng"><h3>{esc(c['eng_h'])}</h3><p>{esc(c['eng_p'])}</p><div class="eng">{eng}</div></div>

<div class="side fade" id="side-team"><h3>{esc(c['team_h'])}</h3><p>{esc(c['team_p'])}</p>
<div class="rows" aria-label="得主人数与团队规模">{team_rows()}</div>
<div class="legend"><span><i class="k-sq"></i>一个方块是一位得主</span><span><i class="k-dot"></i>团队规模（对数坐标）</span></div>
<p class="small" style="margin-top:8px">{esc(c['team_rule'])}</p>
<h4>{esc(c['team_bt_h'])}</h4><p class="sub-p" style="margin:0">{esc(c['team_bt_p'])}</p>
<div class="tbl"><table><thead><tr><th>年份</th><th>发给谁</th><th>人数</th><th>奖金怎么分</th></tr></thead><tbody>{bt}</tbody></table></div></div>

<div class="side fade" id="side-wait"><h3>{esc(c['wait_h'])}</h3><p>{esc(c['wait_p'])}</p>
<div class="seg" id="wait-seg" role="group" aria-label="数字的口径"><button type="button" data-k="wait" aria-pressed="true">从成果到获奖</button><button type="button" data-k="span" aria-pressed="false">从设想到获奖</button></div>
<div class="rows" id="wait-rows" aria-label="每座装置从设想、成果到获奖的时间">{wait_rows()}</div>
<div class="legend"><span><i class="k-thin"></i>设想到成果</span><span><i class="k-thick"></i>成果到获奖</span><span><i class="k-dot"></i>获奖</span></div>
<p class="small" style="margin-top:8px">{esc(c['wait_note'])}</p></div>
</div></section>'''


# ------------------------------------------------------------------ 第 5 章
KIND = {'官方计划': 1, '按规律外推': 2, '纯属猜测': 3}
FZ = ['', '已在建或已批准', '待立项', '差一两项关键技术', '文明级，或靠宇宙']
# 尺度阶梯每一级的短说明（与 content.json 里 ladder 的顺序一一对应）：(尺度的写法, 一行例子, 是否已造出来或已在用)
LADDER = [
    ('1.5 米', '1887 年的石板；量子引力的桌面实验还是设想', True),
    ('约 40 米', '超级神冈；Hyper-K 是 68 × 71 米', True),
    ('1 公里', 'IceCube；Gen2 要 8 立方公里', True),
    ('4 公里', 'LIGO；印度的第三台 2026 年开工', True),
    ('直径 8.5 公里', 'LHC，周长 26.7 公里', True),
    ('约 30 公里', 'FCC 隧道（待批）；Cosmic Explorer 40 公里', False),
    ('1,300 公里', 'DUNE，从伊利诺伊到南达科他（在建）', False),
    ('1.27 万公里', '事件视界望远镜', True),
    ('38 万公里', 'LuSEE-Night；鸿蒙计划', False),
    ('250 万公里', 'LISA，计划 2035 年前后发射', False),
    ('1.5 亿公里', '视差法的基线；DECIGO 的设想', True),
    ('约 550 天文单位', '太阳引力透镜的焦线起点', False),
    ('几千光年', '脉冲星计时阵', True),
]


def when_text(w):
    e, l, t = w.get('earliest'), w.get('likely'), w.get('latest')
    if not e:
        return '<b>没有任务书</b>'
    if e >= 2200:
        return '<b>2200 年以后</b>'
    if l and l >= 2200:
        return f'最早 {e} 年，<b>上不封顶</b>'
    if t and t >= 2200:
        return f'最可能 <b>{l}</b> 年前后；最早 {e}，上不封顶'
    return f'最可能 <b>{l}</b> 年前后；{e}–{t}'


def road_rows():
    a, b = 2026, 2150

    def P(y):
        return (y - a) / (b - a) * 100
    ax = ''.join(f'<i class="g" style="left:{pct(P(y))}"></i><span class="{cls}" style="left:{pct(P(y))}">{y}</span>'
                 for y, cls in ((2026, 's'), (2050, ''), (2075, ''), (2100, ''), (2125, ''), (2150, 'e')))
    out = f'<div class="rw axis"><div class="lb"></div><div class="trk">{ax}</div></div>'
    tiers = C['ch5']['tiers']
    for ti in (1, 2, 3):
        out += f'<div class="tier-h" data-tier="{ti}">{"一二三"[ti - 1]}　{esc(tiers[ti - 1][0])}</div>'
        for t in [x for x in C['topics'] if x['tier'] == ti]:
            w = t['when']
            k = KIND.get(w.get('kind'), 3)
            cn = 1 if any(p.get('china') for p in t['projects']) else 0
            e, l, la = w.get('earliest'), w.get('likely'), w.get('latest')
            sub = ''
            if not e:
                mark = f'<span class="none">{esc(C["ch5"]["none_task"])}</span>'
            elif e > b:
                mark = '<span class="n l" style="left:100%">2150 年以后 ▸</span>'
            else:
                right = min(la or b, b)
                opn = ' open' if (la or 0) > b else ''
                mark = f'<i class="bar k{k}{opn}" style="left:{pct(P(e))};width:{pct(P(right) - P(e))}"></i>'
                if l and l <= b:
                    mark += f'<i class="dot" style="left:{pct(P(l))}"></i>'
                lab = f'约 {l}' if (l and l <= b) else '上不封顶'
                if P(right) > 78:
                    sub = lab + ('，上不封顶' if ((la or 0) > b and lab != '上不封顶') else '')
                else:
                    mark += f'<span class="n" style="left:{pct(P(right))}">{lab}</span>'
            title = esc(re.sub('<[^>]+>', '', when_text(w)) + '。' + w.get('basis', ''))
            subh = f'<small>{sub}</small>' if sub else ''
            out += (f'<div class="rw" data-tier="{ti}" data-kind="{k}" data-cn="{cn}" title="{title}"><div class="lb"><a href="#t-{t["id"]}">{esc(t["topic"])}</a>'
                    f'{"<span class=cn>中</span>" if cn else ""}{subh}</div><div class="trk">{mark}</div></div>')
    return out


def topic_html(t):
    w = t['when']
    k = KIND.get(w.get('kind'), 3)
    cn = 1 if any(p.get('china') for p in t['projects']) else 0
    fz = t.get('feasibility') or 4
    proj = ''
    for p in t['projects']:
        cnchip = '<span class="cn">中</span>' if p.get('china') else ''
        dates = '<span>' + esc(p['dates']) + '</span>' if p.get('dates') else ''
        pcost = '<span>造价：' + esc(p['cost']) + '</span>' if p.get('cost') else ''
        proj += (f'<li><b>{esc(p["name"])}</b><span class="st">{esc(p["status"])}</span>{cnchip}'
                 f'<span><em>{esc(p["where"])}</em></span><span>{esc(p["key"])}</span>{dates}{pcost}</li>')
    extra = ''
    if t.get('universe'):
        extra += f'<div class="full"><h4>靠宇宙的那条路</h4><p>{esc(t["universe"])}</p></div>'
    more = facts_html(t)
    fn = f'<p class="small" style="margin-top:6px">{esc(t["feasibility_note"])}</p>' if t.get('feasibility_note') else ''
    return f'''
<details class="topic" id="t-{t['id']}" data-tier="{t['tier']}" data-kind="{k}" data-cn="{cn}">
<summary><span class="t"><b>{esc(t['topic'])}</b>{"<span class=cn>中</span>" if cn else ""}<span class="q">{esc(t['question'])}</span></span>
<span class="w">{when_text(w)}<br><span class="fz f{fz}">{FZ[fz]}</span> <span class="fz">{esc(w.get('kind', ''))}</span></span></summary>
<div class="body">
  <div><h4>理论说了什么</h4><p>{esc(t['theory'])}</p></div>
  <div><h4>要测到什么量级</h4><p>{esc(t['target'])}</p></div>
  <div class="full"><h4>需要怎样的工程</h4><p>{esc(t['engineering'])}</p></div>
  <div class="full"><h4>现状与项目</h4><ul class="proj">{proj}</ul>{fn}</div>
  <div class="full"><h4>时间估计的依据</h4><p>{esc(w.get('basis', ''))}</p></div>
  {extra}
  <div class="full"><details><summary><span>资料与置信度<small>{len(t['facts'])} 条事实</small></span></summary>{more}</details></div>
</div></details>'''


def delays_rows():
    a, b = 2010, 2042

    def P(y):
        return (y - a) / (b - a) * 100
    # (项目, 原定, 实际或现口径, 图上的字, 说明)；年份可以带小数
    data = [('JWST', 2014, 2021, '晚 7 年', '2009 年定的基线是 2014 年发射；造价从 49.6 亿涨到 97 亿美元'),
            ('LiteBIRD', 2028, 2036, '晚 8 年', '最初目标 2020 年代末，现为 2036 年度发射'),
            ('欧洲极大望远镜', 2024, 2029, '晚 5 年', '2014 年批准时说十年后首光；现为 2029 年首光，科学观测在 2030 年底'),
            ('DUNE', 2026, 2031, '晚 5 年', '2015 年设想 2026 年运行；现为不晚于 2031 年出束'),
            ('ITER 氘氚运行', 2035, 2039, '晚 4 年', '2016 年的进度是 2035 年，2024 年新基线 2039 年；原定 2025 年的首次等离子体节点已取消'),
            ('Hyper-K', 2027, 2028, '晚 1 年', '2020 年批准后的口径是 2027 年'),
            ('Rubin 天文台', 2024, 2025, '晚 1 年', '比的是后期的预期（2024 年首光）；2014 年开工时的基线没有核到'),
            ('Roman 空间望远镜', 2027.4, 2026.66, '早约 8 个月', '承诺不晚于 2027-05，实际 2026-08-30 发射')]
    ax = ''.join(f'<i class="g" style="left:{pct(P(y))}"></i><span style="left:{pct(P(y))}">{y}</span>' for y in (2015, 2020, 2025, 2030, 2035, 2040))
    rows = f'<div class="rw axis"><div class="lb"></div><div class="trk">{ax}</div></div>'
    for name, p0, p1, tag, note in data:
        lo_, hi_ = min(p0, p1), max(p0, p1)
        rows += (f'<div class="rw" title="{esc(note)}"><div class="lb"><b>{esc(name)}</b><small>{esc(note)}</small></div><div class="trk">'
                 f'<i class="seg2" style="left:{pct(P(lo_))};width:{pct(P(hi_) - P(lo_))}"></i><i class="p0" style="left:{pct(P(p0))}"></i><i class="p1" style="left:{pct(P(p1))}"></i>'
                 f'<span class="n{" l" if P(hi_) > 76 else ""}" style="left:{pct(P(lo_) if P(hi_) > 76 else P(hi_))}">{esc(tag)}</span></div></div>')
    return rows


def pow10(d):
    return '1' if d == 0 else ('10' if d == 1 else '10' + ''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(ch)] if ch.isdigit() else '⁻' for ch in str(d)))


def laws_html():
    L = {l['id']: l for l in C['laws']}
    spec = [('livingston', (1925, 2085), lambda d: pow10(d), '纵轴：粒子能量（电子伏）'),
            ('nu-mass', (1950, 2045), lambda d: pow10(d), '纵轴：靶质量（吨）'),
            ('gw-arm', (1965, 2045), lambda d: pow10(d), '纵轴：臂长（米）'),
            ('aperture', (1580, 2060), lambda d: {-2: '1 厘米', -1: '10 厘米', 0: '1 米', 1: '10 米', 2: '100 米'}.get(d, pow10(d)), '纵轴：口径')]
    out = ''
    for lid, xr, yf, ylab in spec:
        l = L[lid]
        out += f'<figure>{FC.law_chart(l, xr, yf, ylab)}<figcaption><b>{esc(l["name"])}</b>{esc(l["summary"])}</figcaption></figure>'
    return out


def ch5():
    c = C['ch5']
    tiers = ''.join(f'<div><small>第{"一二三"[i]}层</small><b>{esc(a)}</b><p>{esc(b)}</p></div>' for i, (a, b) in enumerate(c['tiers']))
    rungs = []
    for x, (size, short, built) in zip(C['ladder'], LADDER):
        rungs.append({'scale_m': x['scale_m'], 'label': x['label'], 'size': size, 'short': short, 'built': built})
    uni = ''.join(f'<li><b>{esc(u["what"])}</b>{esc(u["line"])}{conf(u.get("confidence"))}</li>' for u in C['universe'])
    kinds = ''.join(f'<span><i class="k{i + 1}"></i>{esc(k)}：{esc(d)}</span>' for i, (k, d) in enumerate(c['kinds']))
    topics = ''
    for ti in (1, 2, 3):
        topics += f'<h4 data-tier-h="{ti}">第{"一二三"[ti - 1]}层　{esc(c["tiers"][ti - 1][0])}</h4>'
        topics += ''.join(topic_html(t) for t in C['topics'] if t['tier'] == ti)
    cost = [l for l in C['laws'] if l['id'] == 'cost-ceiling'][0]
    china = ''.join(f'<tr><td><b>{esc(x["name"])}</b></td><td>{esc(x["what"])}</td><td>{esc(x["status"])}{conf(x.get("confidence"))}</td><td>{esc(x["key"])}</td></tr>'
                    for x in C['china'])
    return f'''
<section class="chap" id="c5"><div class="wide">
{chead('图 05', '下一批任务书', c['lede'])}
<div class="tiers fade">{tiers}</div>

<h3 class="sub-h fade">{esc(c['ladder_h'])}</h3>
<div class="lad fade">
  <figure class="fig" style="margin:0"><div class="frame">{FC.ladder_fig(rungs)}</div><figcaption>{esc(c['ladder_p'])}纵轴是对数，每一小格十倍。</figcaption></figure>
  <div><h4 style="margin-top:0">{esc(c['universe_h'])}</h4><p class="sub-p">{esc(c['universe_p'])}</p><ul class="uni">{uni}</ul></div>
</div>

<h3 class="sub-h fade" id="road-h">{esc(c['road_h'])}</h3>
<p class="sub-p">{esc(c['road_p'])}</p>
<div class="chips" id="road-chips">
  <span class="lab">层级</span><span class="grp" data-f="tier"><button type="button" data-v="all" aria-pressed="true">全部</button><button type="button" data-v="1" aria-pressed="false">已在路上</button><button type="button" data-v="2" aria-pressed="false">还差一步</button><button type="button" data-v="3" aria-pressed="false">文明级</button></span>
  <span class="lab">依据</span><span class="grp" data-f="kind"><button type="button" data-v="all" aria-pressed="true">全部</button><button type="button" data-v="1" aria-pressed="false">官方计划</button><button type="button" data-v="2" aria-pressed="false">按规律外推</button><button type="button" data-v="3" aria-pressed="false">纯属猜测</button></span>
  <span class="grp" data-f="cn"><button type="button" data-v="all" aria-pressed="true">全部</button><button type="button" data-v="1" aria-pressed="false">有中国项目</button></span>
</div>
<div class="road fade" id="road" aria-label="各课题的时间估计，2026 到 2150 年">{road_rows()}</div>
<div class="legend">{kinds}<span><i class="k-dot"></i>最可能的年份</span></div>

<div class="topics" id="topics">{topics}</div>

<h3 class="sub-h fade">{esc(c['how_h'])}</h3>
<div class="how">
  <div><p class="sub-p">{esc(c['how_rule'])}</p><p class="sub-p">{esc(c['delays_p'])}</p>
    <div class="rows dly" aria-label="几个大项目的原定年份与实际年份">{delays_rows()}</div>
    <div class="legend"><span><i class="p0" style="position:static;display:inline-block;width:8px;height:8px;border-radius:50%;box-shadow:0 0 0 1.5px var(--ink-2) inset"></i>原定</span><span><i class="k-dot"></i>实际或现口径</span></div></div>
  <div><h4 style="margin-top:0">{esc(c['cost_h'])}</h4><p class="sub-p">{esc(cost['summary'])}</p><p class="small">{esc(cost.get('note', ''))}</p></div>
</div>
<h3 class="sub-h fade">{esc(c['laws_h'])}</h3>
<p class="sub-p">{esc(c['laws_p'])}</p>
<div class="lawg fade">{laws_html()}</div>

<h3 class="sub-h fade">{esc(c['china_h'])}</h3>
<p class="sub-p">{esc(c['china_p'])}</p>
<div class="tbl"><table><thead><tr><th>项目</th><th>做什么</th><th>状态</th><th>关键数字</th></tr></thead><tbody>{china}</tbody></table></div>
</div></section>'''


# ------------------------------------------------------------------ 卷末
def end():
    nref = sum(len(g['items']) for g in C['refs'])
    main = ''.join(f'<li>{esc(x)}</li>' for x in C['main_sources'])
    refs = (f'<p style="font-size:14px;line-height:1.85;color:var(--ink-2)">逐条出处写在各张装置卡和各个课题底下的「资料与置信度」里，共引用约 {nref} 个不同的页面与文献。主要来源：</p>'
            f'<ul>{main}</ul>')
    method = ''.join(f'<li>{esc(x)}</li>' for x in C['method'])
    todo = ''.join(f'<li>{esc(x)}</li>' for x in C['todo'])
    return f'''
<footer class="end" id="end"><div class="wide">
<div class="end-g">
  <div><h3>方法</h3><ol>{method}</ol><h3 style="margin-top:34px">仍待核</h3><ul>{todo}</ul></div>
  <div class="refs"><h3>参考</h3>{refs}</div>
</div>
{credits_html()}
<div class="stamp"><div><b>题号</b>一周一题 第四题</div><div><b>日期</b>2026-10-10</div><div><b>格式</b>图谱</div><div><b>作者</b>天杰</div><div>{esc(C['stamp'])}</div></div>
</div></footer>
<button type="button" class="theme-btn" id="theme-btn" aria-label="切换深浅色" data-cover-hide>深 / 浅</button>
<dialog class="lbx" id="lb" aria-label="图片放大"><div class="lb-in">
  <div class="lb-bar"><span id="lb-n"></span><span id="lb-role"></span><button type="button" id="lb-x" aria-label="关闭">关闭</button></div>
  <div class="lb-stage"><button type="button" class="lb-nav" id="lb-p" aria-label="上一张">‹</button><img id="lb-img" alt=""><button type="button" class="lb-nav" id="lb-q" aria-label="下一张">›</button></div>
  <div class="lb-cap"><h4 id="lb-t"></h4><p id="lb-c"></p><p class="lb-cr"><span id="lb-cr"></span><span id="lb-li"></span><a id="lb-src" target="_blank" rel="noopener">来源页</a></p></div>
</div></dialog>'''


DARK = ('--bg:#0C2444;--surface:#102D55;--surface-2:#163765;--ink:#EAF1FA;--ink-2:#C5D3E6;--muted:#93A9C6;'
        '--line:#3A5680;--line-2:#24406A;--accent:#72CCFF;--accent-ink:#8AD5FF;--wash:rgba(114,204,255,.14);--wash-2:rgba(114,204,255,.24);'
        '--band-bg:#071830;--band-surface:#0B2141;--band-ink:#EAF1FA;--band-ink-2:#BCCBE0;--band-muted:#8FA5C2;--band-line:#2C4770;'
        '--band-accent:#8AD9FF;--band-wash:rgba(138,217,255,.14)')
dark_blocks = ('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){' + DARK + '}}\n'
               ':root[data-theme="dark"]{' + DARK + '}')

data = {'machines': [{'id': m['id'], 'no': m['no'], 'name': m['short'], 'year': m['prize']['year'], 'tool': m['tool'],
                      'cost': {'usd': m['cost'].get('usd2025'), 'usdText': m['cost'].get('usd_text', ''), 'text': m['cost'].get('text', '')}, 'shape': m.get('shape')} for m in M],
        'extra': C['extra_shapes'],
        'gallery': {k: [{x: g.get(x, '') for x in ('file', 'title', 'caption', 'year', 'credit', 'license', 'source_url', 'role_zh', 'w', 'h')} for g in v] for k, v in IMG.items()}}

body = (FB.DEFS + FC.world_symbol(WORLD) + hero() + nav() + ch1() + ch2() + ch3() + ch4() + ch5() + end())
page = (tpl.replace('{{DESCRIPTION}}', esc(C['meta']['desc'])).replace('{{DARK_BLOCKS}}', dark_blocks)
        .replace('{{BODY}}', body)
        .replace('{{DATA_JSON}}', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
        .replace('{{APP_JS}}', app_js))
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', OUT, len(page.encode('utf-8')) // 1024, 'KB')
