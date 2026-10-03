#!/usr/bin/env python3
"""第 3 题《舞从劳作来》：由 src/{template.html, content.json, map_data.json, dance-fig.js, app.js} 生成 ../index.html

  python3 themes/2026-10-03-dance-atlas/src/make_content.py   # 研究底稿 → content.json（需要 research/ 目录）
  python3 themes/2026-10-03-dance-atlas/src/build_theme.py    # 生成 index.html
"""
import json, os, html, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'index.html')
C = json.load(open(os.path.join(HERE, 'content.json'), encoding='utf-8'))
MAP = json.load(open(os.path.join(HERE, 'map_data.json'), encoding='utf-8'))
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
fig_js = open(os.path.join(HERE, 'dance-fig.js'), encoding='utf-8').read()
app_js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

def esc(s): return html.escape(str(s if s is not None else ''), quote=True)
def conf(c):
    cls = {'高': 'h', '中': 'm', '低': 'l'}.get((c or '').strip()[:1], 'm')
    return f'<span class="conf {cls}">置信 {esc(c or "中")}</span>'
def link(t, u, cls=''):
    t = esc(t)
    return f'<a href="{esc(u)}" target="_blank" rel="noopener"{(" class=%s" % cls) if cls else ""}>{t}</a>' if u else t

def side(num, name):
    return f'<div class="chap-side"><span class="vt">卷之{num}</span><span class="dot"></span><span class="vt small">{esc(name)}</span></div>'

# ---------- 卷首 ----------
def hero():
    steps = ''.join(f'<span><b>{"一二三"[i]}</b>{esc(s)}</span>' for i, s in enumerate(C['steps']))
    return f'''
<header class="hero wide" id="top">
  <svg class="ribbons" viewBox="0 0 1000 220" aria-hidden="true" preserveAspectRatio="none">
    <path class="ribbon" pathLength="1000" d="M-20 150 C 170 30, 300 240, 500 120 S 760 -10, 1030 140"></path>
    <path class="ribbon thin" pathLength="1000" d="M-20 170 C 180 60, 300 250, 520 150 S 780 30, 1030 160"></path>
  </svg>
  <div class="eyebrow">一周一题 · 第三题 · 图谱</div>
  <h1>{esc(C['title'])}</h1>
  <p class="sub serif">{esc(C['subtitle'])}</p>
  <p class="thesis serif"><span class="dot"></span>{esc(C['thesis'])}<span class="dot"></span></p>
  <div class="steps">{steps}</div>
  <div class="keyvis" id="keyvis">
    <figure><svg viewBox="0 0 260 300" data-fig="shan" data-static="prep" role="img" aria-label="闪身步 · 蓄"></svg><figcaption>蓄</figcaption></figure>
    <figure><svg viewBox="0 0 260 300" data-fig="shan" data-static="flash" role="img" aria-label="闪身步 · 闪"></svg><figcaption class="red">闪</figcaption></figure>
    <figure><svg viewBox="0 0 260 300" data-fig="shan" data-static="stop" role="img" aria-label="闪身步 · 刹"></svg><figcaption>刹</figcaption></figure>
    <figure><svg viewBox="0 0 260 300" data-fig="shan" role="img" aria-label="闪身步 · 动态演示，节奏来自教学原片"></svg><figcaption>原片节奏 · 3.3 秒一循环</figcaption></figure>
    <figure><svg viewBox="0 0 260 300" data-fig="dou" role="img" aria-label="狗熊哆嗦毛 · 动态演示"></svg><figcaption>狗熊哆嗦毛</figcaption></figure>
  </div>
  <div class="note">卷首小人：二维骨架 × 原教学片段的骨架数据 · 扇与手巾、鼓与槌为道具 · 鼠标悬停图版可看原色</div>
</header>'''

# ---------- 导航 ----------
def nav():
    items = [('top', '卷首'), ('c1', '卷之一 · 爆梗现场'), ('c2', '卷之二 · 从劳作到艺术'), ('c3', '卷之三 · 动作教材'), ('c4', '卷之四 · 鉴赏对照'), ('c5', '卷之五 · 为什么是现在'), ('end', '卷末')]
    row = ''.join(f'<a href="#{i}" data-nav="{i}"{" class=on" if i == "top" else ""}>{esc(t)}</a>' for i, t in items)
    beats = [0, .54, 1.08, 1.44, 1.8, 2.16]
    ticks = ''.join(('<span class="tick beat" style="animation-delay:%ss"></span>' % d) if i % 2 == 0 else '<span class="tick"></span><span class="tick"></span>' for i, d in enumerate(beats * 2))
    return f'<nav class="nav" id="nav" aria-label="章节"><div class="row">{row}</div><div class="ticks" aria-hidden="true">{ticks}</div><div class="prog" id="prog"></div></nav>'

# ---------- 卷之一 ----------
def chap1():
    m = C['meme']
    tl = ''.join(f'<li><span class="d">{esc(e["d"])}</span>{esc(e["t"])}<span class="s">{link(e["s"], e["u"])}</span></li>' for e in m['events'])
    pair = ''
    for p in m['pair']:
        pair += f'''<article class="card"><h3>{esc(p['who'])}</h3><div class="what">{esc(p['what'])}</div>
<dl><dt>身份</dt><dd>{esc(p['role'])}</dd><dt>教材</dt><dd>{esc(p['material'])}</dd><dt>非遗</dt><dd>{esc(p['heritage'])}</dd></dl>
<blockquote>{esc(p['quote'])}</blockquote></article>'''
    return f'''
<section class="chap wide" id="c1"><div class="chap-head">{side('一', '爆梗现场')}<div class="chap-body fade">
<h2>爆梗现场</h2><p class="lede">{esc(m['intro'])}</p>
<ol class="tl">{tl}</ol>
<div class="pair">{pair}</div>
<p class="lede" style="margin-top:26px">要看懂这两个动作，得先回到舞蹈怎么来的——往下，是五千年。</p>
</div></div></section>'''

# ---------- 卷之二 ----------
def node_html(n, i):
    kv = ''.join(f'<dt>{esc(it["k"])}</dt><dd>{esc(it["v"])}</dd>' for it in n.get('items', []))
    facts = ''.join(f'<li>{esc(f["text"])}{conf(f.get("confidence"))}<span class="src">{link(f.get("source", ""), f.get("url", ""))}</span></li>' for f in n.get('facts', []))
    q = n.get('quote') or {}
    quote = f'<blockquote>{esc(q.get("text"))}<cite>{esc(q.get("who"))}</cite></blockquote>' if q and q.get('text') else ''
    im = n['image']
    lic = link(im['license'], im.get('license_link')) if im.get('license_link') else esc(im['license'])
    fig = f'''<figure class="plate" style="--ar:{im['w']}/{im['h']}"><div class="fr"><img src="{esc(im['src'])}" alt="{esc(im['title'])}" loading="lazy" width="{im['w']}" height="{im['h']}"></div>
<figcaption><b>图 {i+1:02d} · {esc(im['title'])}</b> · {esc(im['caption'])}<br>{esc(im['author'])} · {lic} · <a href="{esc(im['page'])}" target="_blank" rel="noopener">Wikimedia Commons</a></figcaption></figure>'''
    return f'''<article class="node" id="{n['id']}" data-node="{i}">
<div class="kicker">节点 {i+1:02d} / 12 · {esc(n['years'])}</div>
<h3>{esc(n['era'])} · {esc(n['title'])}</h3>
<p class="sum">{esc(n['summary'])}</p>
<dl class="kv">{kv}</dl>
{quote}
{fig}
<details class="facts"><summary>资料与置信度（{len(n.get('facts', []))} 条）</summary><ul>{facts}</ul></details>
</article>'''

def chap2():
    nodes = ''.join(node_html(n, i) for i, n in enumerate(C['nodes']))
    strip = ''.join(f'<button type="button" data-era="{i}"{" class=on" if i == 0 else ""}>{esc(n["era"])}</button>' for i, n in enumerate(C['nodes']))
    return f'''
<section class="chap wide" id="c2"><div class="chap-head">{side('二', '从劳作到艺术')}<div class="chap-body">
<div class="fade"><h2>从劳作到艺术</h2>
<p class="lede">十二个时代节点。左边的地图随你滚动换图层——高亮的是那个时代舞蹈的发生地，虚线是传播与迁徙的路线；右边的文字按时间往下走，左侧墨线逢节点打一个朱砂点。每个节点都列出代表物、它来自什么劳作或仪式、发生了什么交融，以及「为什么是它」。</p></div>
<div class="atlas">
  <div class="map-col fade">
    <div class="map-wrap" id="mapwrap" aria-live="polite"></div>
    <div class="map-layer"><b id="layer-name">{esc(C['nodes'][0]['map'].get('layer', ''))}</b><span id="layer-years">{esc(C['nodes'][0]['years'])}</span></div>
    <div class="era-strip" id="era-strip">{strip}</div>
  </div>
  <div class="nodes" id="nodes"><div class="rail" aria-hidden="true"><i id="rail-fill"></i></div>{nodes}</div>
</div>
</div></div></section>'''

# ---------- 卷之三 ----------
def move_html(m, deck_key):
    has_fig = bool(m.get('fig'))
    cls = 'move hero-move' if has_fig else 'move'
    figwrap = f'<div class="figwrap"><svg viewBox="0 0 260 300" data-fig="{m["fig"]}" role="img" aria-label="{esc(m["name"])} 动态演示"></svg><span class="cap">{esc(m.get("cue") or "")}</span></div>' if has_fig else ''
    rows = []
    for k, key in [('要领', 'how'), ('生活来源', 'life'), ('角色', 'role'), ('场景', 'scene'), ('提示', 'risk')]:
        v = (m.get(key) or '').strip()
        if v and not v.startswith('要领未') and not v.startswith('仅见'):
            rows.append(f'<dt>{k}</dt><dd>{esc(v)}</dd>')
    see = ''.join(f'<span>{esc(s)}</span>' for s in (m.get('see') or []) if s)
    see_html = f'<div class="see">看哪里：{see}</div>' if see else ''
    cue = f'<div class="cue"><span class="dot"></span>{esc(m["cue"])}</div>' if m.get('cue') and m['cue'] != '——' and not has_fig else ''
    src = (m.get('source') or '')
    srcs = ' · '.join(link(('来源 %d' % (j+1)) if len(re.findall(r'https?://\S+', src)) > 1 else '来源', u) for j, u in enumerate(re.findall(r'https?://[^\s;；，,）)]+', src)))
    body = f'<div><h4>{esc(m["name"])}{conf(m.get("confidence"))}</h4>{cue}<dl>{"".join(rows)}</dl>{see_html}{("<div class=src>" + srcs + "</div>") if srcs else ""}</div>'
    return f'<article class="{cls}" id="mv-{deck_key}-{esc(m["name"])}">{figwrap}{body}</article>'

def deck_html(d):
    roles = ''.join(f'<span class="chip"><b>{esc(r["name"])}</b> {esc(r.get("desc") or "")}</span>' for r in d.get('roles') or [])
    scenes = ''.join(f'<span class="chip"><b>{esc(s["name"])}</b> {esc(s.get("desc") or "")}</span>' for s in d.get('scenes') or [])
    schools = '、'.join(esc(s.get('name') or '') for s in d.get('schools') or [])
    t = d.get('teacher') or {}
    moves = ''.join(move_html(m, d['key']) for m in d['moves'])
    names = ('<p class="names"><b>教材与文献里还有这些动作名</b>（本次只查到名字、未见要领，不编）：' + '、'.join(esc(x) for x in d['names_only']) + '。</p>') if d.get('names_only') else ''
    inh = ''.join(f'<div class="card"><b>{esc(i["name"])}</b><p>{esc(i.get("note") or "")}</p></div>' for i in (d.get('inheritors') or []) if i.get('name') and not i['name'].startswith('（'))
    img = ''
    if d.get('image'):
        im = d['image']; lic = link(im['license'], im.get('license_link')) if im.get('license_link') else esc(im['license'])
        img = f'<figure class="plate" style="--ar:{im["w"]}/{im["h"]}"><div class="fr"><img src="{esc(im["src"])}" alt="{esc(im["title"])}" loading="lazy" width="{im["w"]}" height="{im["h"]}"></div><figcaption><b>{esc(im["title"])}</b> · {esc(im["caption"])}<br>{esc(im["author"])} · {lic} · <a href="{esc(im["page"])}" target="_blank" rel="noopener">Wikimedia Commons</a></figcaption></figure>'
    return f'''<div class="deck fade" id="deck-{d['key']}">
<div class="deck-head">
  <div><h3>{esc(d['name'])}</h3><div class="meta">{esc(d.get('heritage') or '')}</div><p>{esc(d.get('region') or '')}</p>
  <dl><dt>角色</dt><dd><span class="chips">{roles}</span></dd><dt>场景</dt><dd><span class="chips">{scenes}</span></dd><dt>流派</dt><dd>{schools}</dd>
  <dt>老师</dt><dd><b>{esc(t.get('name') or '')}</b> · {esc(t.get('title') or '')}</dd><dt>教材</dt><dd>{esc(t.get('material') or '')}</dd></dl></div>
  <div>{img}</div>
</div>
<div class="moves">{moves}</div>
{names}
<div class="inheritors">{inh}</div>
</div>'''

def chap3():
    decks = ''.join(deck_html(d) for d in C['decks'])
    return f'''
<section class="chap wide" id="c3"><div class="chap-head">{side('三', '动作教材')}<div class="chap-body">
<div class="fade"><h2>动作教材</h2>
<p class="lede">两套卡组，来自两位老师的教学原片和北京舞蹈学院的公开教材。每张卡统一写口令、要领、生活来源、角色与原生场景；带小人的三张，动作数据直接取自原片的骨架。查不到要领的动作只列名字——这也是本题的态度：不编。</p></div>
{decks}
</div></div></section>'''

# ---------- 卷之四 ----------
def chap4():
    rows = ''
    for r in C['works']:
        genre_key = 'hgd' if '花鼓灯' in (r.get('genre') or '') else ('gz' if '秧歌' in (r.get('genre') or '') else 'other')
        work = f'<b>{esc(r["work"])}</b>' + (f'<span class="sub">{esc(r.get("troupe") or "")}{(" · " + esc(r["year"])) if r.get("year") else ""}</span>')
        rows += f'<tr data-genre="{genre_key}" data-conf="{esc((r.get("confidence") or "中")[:1])}"><td>{esc(r["combo"])}</td><td>{esc(r.get("genre") or "")}</td><td>{work}</td><td>{esc(r.get("where") or "")}</td><td>{esc(r.get("look") or "")}</td><td>{conf(r.get("confidence"))}{(" " + link("官方", r["link"])) if r.get("link") else ""}</td></tr>'
    quick = ''
    for q in C['quick']:
        wk = ''.join(f'<span>{link(w["title"], w.get("link"))} · {esc(w.get("who") or "")}{(" · " + esc(w["year"])) if w.get("year") else ""}{conf(w.get("confidence")) if (w.get("confidence") or "") != "高" else ""}</span>' for w in q.get('works') or [])
        quick += f'<article class="card"><h4>{esc(q["genre"])}<small>{esc(q.get("ethnic") or "")} · {esc(q.get("region") or "")}</small></h4><div class="motif"><b>动律</b>{esc(q["motif"])}</div><div class="watch"><b style="color:var(--muted);font-weight:500">道具</b> {esc(q.get("props") or "")}<br><b style="color:var(--muted);font-weight:500">看什么</b> {esc(q["watch"])}</div><div class="wk">{wk}</div></article>'
    genres = sorted({q['genre'] for q in C['quick']} | {'安徽花鼓灯', '山东鼓子秧歌'})
    genre_opts = ''.join(f'<option>{esc(g)}</option>' for g in genres)
    return f'''
<section class="chap wide" id="c4"><div class="chap-head">{side('四', '鉴赏对照')}<div class="chap-body">
<div class="fade"><h2>鉴赏对照</h2>
<p class="lede">按「组合 / 场景」排的一张表：这个动作在哪部作品里能看到、看哪一段、看什么。只给官方渠道，不嵌第三方视频。表下是十个舞种的看点速查，带着去剧场或打开春晚回放就用得上。</p></div>
<div class="tool fade" id="finder">
  <div><h3>动作查找器</h3><p class="hint">输入或选一个梗名，跳到动作卡并列出能看到它的作品。</p>
    <label for="finder-input">动作名</label><input id="finder-input" list="finder-list" placeholder="闪身步 / 狗熊哆嗦毛 / 浪子踢球 / 伞头领场 …"><datalist id="finder-list"></datalist>
    <button type="button" class="btn" id="finder-go">查找</button> <button type="button" class="btn ghost" id="finder-rand">随便来一个</button></div>
  <div class="out" id="finder-out">还没有查。试试「狗熊哆嗦毛」。</div>
</div>
<div class="filters" id="filters"><span class="lab">筛选</span><button type="button" data-f="all" class="on">全部</button><button type="button" data-f="hgd">安徽花鼓灯</button><button type="button" data-f="gz">山东鼓子秧歌</button><span class="lab" style="margin-left:10px">置信</span><button type="button" data-c="all" class="on">全部</button><button type="button" data-c="高">只看高</button></div>
<div class="tbl"><table id="works"><thead><tr><th>组合 / 场景</th><th>舞种</th><th>作品</th><th>看哪一段</th><th>看什么</th><th>置信 · 渠道</th></tr></thead><tbody>{rows}</tbody></table></div>
<h3 style="font-size:22px;letter-spacing:.1em;margin-top:38px" class="fade">其它舞种看点速查</h3>
<div class="quick fade">{quick}</div>
<div class="tool fade" id="checklist">
  <div><h3>看点清单生成器</h3><p class="hint">选一个舞种，填上你要去看的作品，生成一页看点提示——截图带去剧场。</p>
    <label for="cl-genre">舞种</label><select id="cl-genre">{genre_opts}</select>
    <label for="cl-work">作品（可不填）</label><input id="cl-work" placeholder="例：《大染坊》谢幕 / 春晚某年的秧歌">
    <button type="button" class="btn" id="cl-go">生成清单</button> <button type="button" class="btn ghost" id="cl-copy">复制文字</button></div>
  <div class="out" id="cl-out">选好舞种点「生成清单」。</div>
</div>
</div></div></section>'''

# ---------- 卷之五 ----------
def chap5():
    paras = ''.join(f'<p>{esc(p)}</p>' for p in C['why']['paras'])
    return f'''
<section class="chap wide" id="c5"><div class="chap-head">{side('五', '为什么是现在')}<div class="chap-body fade">
<h2>为什么是现在</h2>
<div class="essay">{paras}</div>
</div></div></section>'''

# ---------- 卷末 ----------
def end():
    refs = ''
    for k, items in C['refs'].items():
        lis = ''.join(f'<li>{link(x["t"], x["u"])}</li>' for x in items)
        refs += f'<details><summary>{esc(k)}（{len(items)}）</summary><ul>{lis}</ul></details>'
    method = ''.join(f'<li>{esc(x)}</li>' for x in C['method']['items'])
    todo = '、'.join(esc(x) for x in C['method']['todo'])
    credits = ''.join(f'<li>{esc(v["title"])} — {esc(v["author"])}，{esc(v["license"])}，<a href="{esc(v["page"])}" target="_blank" rel="noopener">Commons</a></li>' for k, v in C['credits'].items())
    return f'''
<footer class="end wide" id="end">
<div class="grid">
  <div><h3>参考</h3>{refs}<details><summary>图片来源与许可证（{len(C['credits'])}）</summary><ul>{credits}</ul></details></div>
  <div><h3>方法</h3><ol>{method}</ol><p class="todo"><b>仍待核：</b>{todo}。</p></div>
</div>
<div class="stamp"><div class="meta">一周一题 · 第 3 题 · 2026-10-03 · 图谱<br>文字与小人引擎：Claude（Fable 5.1）与天杰 · 骨架数据取自教学原片 · 地图按现行省级行政区划</div><div class="vt">一周一题 · 第三题 · 天杰</div></div>
</footer>
<button type="button" class="theme-btn" id="theme-btn" aria-label="切换深浅色" data-cover-hide>深 / 浅</button>'''

body = hero() + nav() + chap1() + chap2() + chap3() + chap4() + chap5() + end()
desc = '从青海大通舞蹈纹彩陶盆到北舞教学视频里的「闪身步」：十二个时代节点 × 中国版图图层，讲舞蹈怎样从劳作、仪式与交融里沉淀成艺术；附安徽花鼓灯与山东鼓子秧歌两套动作教材、原片骨架驱动的墨线小人，以及一张「在哪部作品里看什么」的鉴赏对照表。'
page = (tpl.replace('{{DESCRIPTION}}', esc(desc)).replace('{{BODY}}', body)
        .replace('{{CONTENT_JSON}}', json.dumps({k: C[k] for k in ('nodes', 'decks', 'works', 'quick')}, ensure_ascii=False).replace('</', '<\\/'))
        .replace('{{MAP_JSON}}', json.dumps(MAP, ensure_ascii=False).replace('</', '<\\/'))
        .replace('{{DANCE_FIG_JS}}', fig_js).replace('{{APP_JS}}', app_js))
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', OUT, len(page) // 1024, 'KB')
