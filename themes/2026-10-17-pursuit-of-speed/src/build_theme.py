#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 5 题「速度的阶梯」：把 research/*.json + editorial.py + images.json 合成 ../index.html 与 ../meta.json。
用法（仓库根目录）：python3 themes/2026-10-17-pursuit-of-speed/src/build_theme.py
"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial as E
import figs
import fixes
import journey
import demos
H = None

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

def conf(c): return f'<span class="conf {CONF_CLS.get(c, "m")}" title="置信度">{esc(c or "中")}</span>'
def srcs(ss, cls='src'):
    if not ss: return ''
    seen, uniq = set(), []
    for s in ss:
        k = s.get('u') or s['t']
        if k in seen: continue
        seen.add(k); uniq.append(s)
    return f'<p class="{cls}">来源：' + '；'.join(f'<a href="{esc(s["u"])}" target="_blank" rel="noopener">{esc(s["t"])}</a>' if s.get('u') else esc(s['t']) for s in uniq) + '</p>'
def fmt(v): return figs.fmt(v)

def fig(img_id, cls='ph', h=None):
    im = IM.get(img_id)
    if not im: return f'<div class="{cls} none">本格没有合规照片，只用文字。</div>'
    cap = E.CAPTIONS.get(img_id, im.get('caption', ''))
    return (f'<figure class="{cls}"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy" width="{im.get("w","")}" height="{im.get("h","")}">'
            f'<figcaption>{esc(cap)} 图：{esc(im["author"])}，{esc(im["license"])}。</figcaption></figure>')

# ---------- 卷首
def hero():
    M = E.META; H = E.HERO
    steps = ''.join(f'<li><span>{s}</span></li>' for s in H['steps'])
    week = ''.join(f'<span><i>{esc(d)}</i> <b>{esc(t)}</b> {esc(x)}</span>' for d, t, x in H['week'])
    scale = sorted(B['scale'], key=lambda s: s['kmh'])
    first = next(s for s in scale if s['id'] == 'sound')
    return f'''
<header class="hero paper band"><div class="wide">
  <div class="strip fade"><span><b>一周一题</b>第 {M['no']} 题</span><span><b>上线</b>{M['date']}</span><span><b>格式</b>{M['format']}</span><span><b>阅读</b>{M['reading_time']}</span></div>
  <h1 class="fade">{esc(M['title'].split('：')[0])}<br><span style="font-size:.56em;letter-spacing:.04em">{esc(M['title'].split('：')[1])}</span></h1>
  <p class="sub fade">{esc(M['subtitle'])}</p>
  <div class="hero-grid">
    <div class="fade"><p class="thesis">{H['thesis']}</p><div class="week">{week}</div></div>
    <ol class="steps fade">{steps}</ol>
  </div>
  <div class="stats fade">
    <div class="stat"><div class="k">FASTEST HUMANS · 1969</div><div class="v"><b class="cnt" data-to="39897">0</b><small>km/h</small></div><div class="d">人类乘坐过的最快速度：Apollo 10 返回地球</div><div class="n">NASA 口径 24,791 mph；吉尼斯作 39,937.7 km/h。五十七年未破，今年的 Artemis II 也没有。</div></div>
    <div class="stat"><div class="k">EVERYDAY MAXIMUM · 2017–</div><div class="v"><b class="cnt" data-to="350">0</b><small>km/h</small></div><div class="d">普通人今天能买票坐到的陆上最快：轮轨高铁</div><div class="n">空中约 900 km/h（Mach 0.85）；1976–2003 年协和曾到 2,180。</div></div>
    <div class="stat"><div class="k">THIS WEEK · CLAIMED</div><div class="v"><b class="cnt" data-to="0.81" data-dec="2">0</b><small>s · 0–60 mph</small></div><div class="d">特斯拉 Roadster 演示：现场计时器故障后的宣称值</div><div class="n">录像 1.0 秒；推文称顶配 0.59 秒以内。没有第三方实测，见第一章。</div></div>
  </div>
  <figure class="rulerfig fade">
    <div class="ruler-wrap">{figs.ruler_svg(scale)}</div>
    <div class="rcard" id="rcard" data-first="{esc(first['id'])}"></div>
    <figcaption><b>对数速度尺。</b>每一大格快十倍：从步行到光速跨九个大格、八个多数量级，人类自己乘坐过的只到第五格（Apollo 10，39,897 km/h）。点刻度看口径与出处；音速取海平面 15 °C 的 1,225 km/h，随温度变化。</figcaption>
  </figure>
</div></header>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n}</small>{esc(t)}</a>' for cid, n, t, _ in E.CHAPTERS)
    links += '<a href="#end" data-nav="end"><small>末</small>参考 · 方法</a>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E.CHAPTERS if c[0] == cid)
    label = '序章' if int(n) == 0 else f'第 {"一二三四五六七八"[int(n)-1]} 章'
    return f'<div class="chead fade"><div class="cno">{int(n):02d}<small>{label}</small></div><h2>{esc(t)}</h2><p class="lede">{lede}</p></div>'

# ---------- 序章 · 速度之旅
def src_lookup(key):
    parts = key.split(':')
    obj = None
    if parts[0] == 'scale': obj = next((s for s in B['scale'] if s['id'] == parts[1]), None)
    elif parts[0] == 'cell':
        t, e = parts[1].split('-'); obj = CELLS.get((t, int(e)))
        if obj and len(parts) > 2 and parts[2] == 'also': obj = obj.get('also')
    if not obj: return '', ''
    return srcs(obj.get('sources')), conf(obj.get('conf'))

def src_lookup_raw(key):
    parts = key.split(':'); obj = None
    if parts[0] == 'scale': obj = next((s for s in B['scale'] if s['id'] == parts[1]), None)
    elif parts[0] == 'cell':
        t, e = parts[1].split('-'); obj = CELLS.get((t, int(e)))
        if obj and len(parts) > 2 and parts[2] == 'also': obj = obj.get('also')
    return obj.get('sources') if obj else None

def caption_of(img_id, im): return E.CAPTIONS.get(img_id, im.get('caption', ''))

def ch_journey():
    return (f'<section class="chap journey band" id="journey"><div class="wide">{chead("journey")}</div>'
            + journey.stage(IM, caption_of) + journey.steps(IM, caption_of, src_lookup)
            + '<p class="jnote">照片全部公有领域或 CC，署名见各级卡片与卷末；数字与口径同第二章与卷首速度尺。</p></section>')

# ---------- 第一章
def now_card(n, side=False):
    claims = ''.join(f'<li><b>{esc(c["k"])}</b><span>{esc(c["v"])}</span><span class="tag claim">{esc(c.get("kind","宣称"))}</span></li>' for c in n.get('claims', []))
    disp = f'<p class="dispute"><b>质疑 / 分歧</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    return f'''<article class="nowcard fade"><div class="hd"><b>{esc(n['title'])}</b><span>{esc(n['date'])}</span>{conf(n.get('conf'))}</div>
<div class="bd"><p>{esc(n['text'])}</p><ul class="claims">{claims}</ul>{disp}{srcs(n.get('sources'))}</div></article>'''

def ch_now():
    annivs = [('1947-10-14', '耶格尔驾 Bell X-1 首次载人超音速，Mach 1.06。美国空军 1948 年 6 月才正式确认。'),
              ('1997-10-15', 'Andy Green 驾 Thrust SSC 在黑岩沙漠跑出 1,227.985 km/h（Mach 1.016，吉尼斯作 1.020），至今唯一的超音速陆地纪录——与 X-1 相隔五十年零一天。'),
              ('2012-10-14', '鲍姆加特纳从 39 km 高空跳下，自由落体 1,357.6 km/h（FAI），第一个不靠载具超音速的人。')]
    an = ''.join(f'<div class="anniv"><div class="y">{esc(d)}</div><p>{esc(t)}</p></div>' for d, t in annivs)
    side = f'''<div class="side">{now_card(NOW['denza_z'])}<article class="nowcard fade"><div class="hd"><b>两个「音障日」，外加一次自由落体</b><span>都在本周</span></div>{an}
<div class="bd" style="padding-top:0">{srcs([{"t":"NASA · Bell X-1 / SP-4219","u":"https://history.nasa.gov/SP-4219/Chapter3.html"},{"t":"FIA · 陆地速度纪录","u":"https://www.fia.com/land-speed-records"},{"t":"FAI · Baumgartner 纪录","u":"https://www.fai.org/record/16671"}])}</div></article>{now_card(NOW['gb7258'])}</div>'''
    return f'<section class="chap" id="now"><div class="wide">{chead("now")}<div class="now-grid"><div>{now_card(NOW["roadster"])}</div>{side}</div></div></section>'

# ---------- 第二章 矩阵
def cell_html(track, era):
    c = CELLS.get((track, era))
    if not c or c.get('subject') == '—':
        why = esc(c['why']) if c else ''
        return f'<div><div class="cell empty">—<br>{why}</div></div>'
    also = f'<span class="also">另：{esc(c["also"]["subject"])} · {fmt(c["also"]["kmh"])} km/h · {esc(c["also"]["year"])}</span>' if c.get('also') else ''
    return (f'<div><button class="cell" type="button" data-cell="{track}-{era}"><span class="s">{esc(c["subject"])}</span>'
            f'<span class="v">{fmt(c["kmh"])}<small>km/h</small></span><span class="y">{esc(c["year"])} · {esc(c["who"])}</span>{conf(c.get("conf"))}{also}</button></div>')

def ch_matrix():
    import math
    rows = []
    for tid, tn, tsub in E.TRACKS:
        bars = []
        for e in range(8):
            c = CELLS.get((tid, e))
            if not c or c.get('subject') == '—':
                bars.append(f'<div class="tb none" title="{esc(c["why"]) if c else ""}"><i></i></div>'); continue
            h = max(2, (math.log10(c['kmh']) + 0.3) / 6.3 * 100)
            bars.append(f'<button type="button" class="tb" data-cell="{tid}-{e}" style="--h:{h:.1f}%" title="{esc(c["subject"])} · {fmt(c["kmh"])} km/h · {esc(c["year"])}"><i></i><b>{fmt(c["kmh"])}</b><span>{esc(E.ERAS[e][1])}</span></button>')
        rows.append(f'<div class="trk{" body" if tid=="body" else ""}"><div class="th"><b>{figs.glyph(tid)}{esc(tn)}</b><span>{esc(tsub)}</span></div><div class="tbars">{"".join(bars)}</div></div>')
    return f'''<section class="chap" id="tracks"><div class="wide">{chead("tracks")}
<div class="tracks fade">{''.join(rows)}</div>
<div class="mxd fade" id="mxd" data-first="road-6"></div>
<p class="small" style="margin-top:10px">柱高按对数刻度；灰柱 = 该时代没有合适的代表物（鼠标悬停看原因）。置信度与口径在详情里。</p>
</div></section>'''

# ---------- 第三章
def ch_lines():
    rec = sorted(B['record_line'], key=lambda p: p['year'])
    rec_line, mx = [], 0
    for p in rec:
        if p['kmh'] > mx: rec_line.append(p); mx = p['kmh']
        elif p['year'] >= 2020: rec_line.append(dict(p, flat=True))
    day = sorted(C['daily_line'], key=lambda p: p['year'])
    for p in rec: p['short'] = p['label'].split('（')[0].replace('史蒂芬森「火箭号」Rainhill 试车', '火箭号').replace('Zossen 三相电力试验车 210 km/h', 'Zossen 电动车').replace('Deperdussin 飞机 203.85 km/h', 'Deperdussin').replace('Me 209 V1 活塞飞机 755 km/h', 'Me 209').replace('Bell X-1 突破音障 Mach 1.06', 'X-1').replace('Bell X-2 Mach 3.2', 'X-2').replace('加加林轨道飞行', '加加林').replace('X-15 7,274 km/h', 'X-15').replace('Apollo 10 返回', 'Apollo 10').replace('Artemis II 返回', 'Artemis II')
    for p in day: p['short'] = p['label'].replace('京津城际 350', '京津城际').replace('复兴号 350', '复兴号').replace('仍是 350 / 900', '高铁至今')
    def li(p):
        yr = '前 1800' if p['year'] < 1800 else str(p['year'])
        return f'<li><span class="y">{yr}</span><span>{esc(p["label"])} {conf(p.get("conf"))}</span><span class="v">{fmt(p["kmh"])} km/h</span><p>{esc(re.sub(r"^口径[：:]\s*", "", p.get("note","")))}</p></li>'
    tiles = []
    for it in E.COUNTER['items']:
        vis = {'bar': '<div class="cvis bar"><i><b></b></i></div>', 'gauge': '<div class="cvis gauge2"><svg viewBox="0 0 120 70"><path class="g-track" d="M10 65 A50 50 0 0 1 110 65"/><path class="g-red" d="M60 15 A50 50 0 0 1 110 65"/><line class="cn" x1="60" y1="65" x2="60" y2="20" style="transform-origin:60px 65px"/></svg></div>',
               'launch': '<div class="cvis strip"><i class="lane"></i><b class="dot"></b></div>', 'mach': '<div class="cvis machbar"><i></i><b></b><span>Mach 1</span></div>'}[it['kind']]
        tiles.append(f'<div class="ctile fade" data-kind="{it["kind"]}" data-v="{it["v"]}" data-max="{it["max"]}" data-mark="{it.get("mark","")}"><div class="k">{esc(it["k"])}</div><div class="v"><b class="cnt" data-to="{it["v"]}" data-dec="{it["dec"]}">0</b><small>{esc(it["unit"])}</small></div>{vis}<details class="fold"><summary>为什么算反例</summary><p>{esc(it["d"])}</p></details></div>')
    return f'''<section class="chap" id="lines"><div class="wide">{chead("lines")}
<figure class="lines-fig fade" id="lines-fig">{figs.lines_svg(rec_line, day)}
<div class="lctl"><button type="button" class="dgo" id="ln-play">▶ 播放 1800 → 2026</button><input type="range" id="ln-yr" min="1800" max="2026" step="1" value="2026"><div class="lyr"><b id="ln-y">2026</b><span id="ln-rec">最快 <i>39,897</i></span><span id="ln-day">日常 <i>350</i></span></div><div class="lflash" id="ln-flash"></div></div>
<div class="lkey"><span><i></i>人类乘坐过的最快速度（载人纪录）</span><span><i class="k2"></i>普通人日常能坐到的最快速度（商业运营）</span><span>纵轴对数</span></div></figure>
<h3 class="sub-h">{esc(E.COUNTER['title'])}</h3>
<div class="ctiles">{''.join(tiles)}</div>
<details class="fold big fade" style="margin-top:22px"><summary><h3>数据表 · 两条线逐点口径与来源</h3></summary><div class="cols2"><div><h4>红线</h4><ul class="pts">{''.join(li(p) for p in rec)}</ul>{srcs([s for p in rec for s in p.get('sources', [])][:6])}</div><div><h4>黑线</h4><ul class="pts day">{''.join(li(p) for p in day)}</ul>{srcs([s for p in day for s in p.get('sources', [])][:6])}</div></div></details>
</div></section>'''

# ---------- 第四章
def ch_walls():
    order = [('tyre', '轮胎打滑'), ('rail', '接触网跳火'), ('water', '水翼空化'), ('air', '音障与热障'), ('g', '黑视'), ('light', '光速')]
    out = []
    for wid, short in order:
        w = WALLS[wid]
        br = ''.join(f'<li>{esc(x)}</li>' for x in w.get('breakthroughs', []))
        out.append(f'''<article class="wall fade" id="wall-{wid}"><div class="hd"><b>{esc(w['title'])}</b><span class="f">{esc(w['formula'])}</span></div>
{demos.WALL_DEMOS[wid]()}
<details class="fold"><summary>这面墙是怎么回事、谁撞过、怎么绕过去</summary><p>{esc(w['text'])}</p><h4>突破手段</h4><ul>{br}</ul><p class="ex"><b>今天的例子</b>{esc(w.get('example',''))}</p>{srcs(w.get('sources'))}<p class="small">置信度 {conf(w.get('conf'))}</p></details></article>''')
    return f'<section class="chap" id="walls"><div class="wide">{chead("walls")}<div class="snd fade"><button type="button" id="snd-btn" aria-pressed="false">声音：关</button><span>打开后撞墙有音爆、跳火、ABS 的点击（程序合成，没有采样）。</span></div><div class="walls">{"".join(out)}</div></div></section>'

# ---------- 第五章 · 驾驭
HARNESS_IMG = {'x15-rcs': 'x15', 'apollo-reentry': 'apollo_cm', 'falcon9-landing': 'falcon9', 'thrust-ssc': 'thrustssc', 'three-point-hydroplane': 'spiritoz',
               'f1-aero': 'f1_ground', 'relaxed-stability': 'x29', 'sr71-unstart': 'sr71', 'rail-pantograph-tilt-maglev': 'maglev_l0', 'human-g-limit': 'stapp2',
               'animal-control': 'cheetah', 'concorde-cg': 'concorde'}
KIND_CLS = {'宣称': 'claim', '实测': 'meas', '官方': 'off', '设计值': 'des'}
def ch_harness():
    cards = []
    for c in H['cards']:
        measure, demo = E.MEASURE.get(c['id'], (c['title'], ''))
        img = HARNESS_IMG.get(c['id']); im = IM.get(img) if img else None
        ph = (f'<figure class="hph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{esc(E.CAPTIONS.get(img, im.get("caption", "")))} 图：{esc(im["author"])}，{esc(im["license"])}。</figcaption></figure>') if (im and not demo) else ''
        dm = demos.H_DEMOS[demo]() if demo else ''
        nums = ''.join(f'<div><span>{esc(n["k"])}</span><b>{esc(n["v"])}</b><i class="tag kind {KIND_CLS.get(n.get("kind"), "off")}">{esc(n.get("kind", ""))}</i></div>' for n in c.get('numbers', [])[:(8 if c['id'] == 'roadster-2026' else 4)])
        link = f'<p class="hlink">{esc(c["link"])}</p>' if c.get('link') else ''
        cards.append(f'''<article class="hcard fade{' demo-card' if demo else ''}" id="h-{esc(c['id'])}">{ph}
<div class="hbd"><div class="hhd"><span class="tag">{esc(c['domain'])}</span><span class="hyr">{esc(c['year'])}</span>{conf(c.get('conf'))}</div>
<h3>{esc(measure)}</h3><p class="hsub">{esc(c['title'])}</p>
{dm}
<div class="hnums">{nums}</div>
<details class="fold"><summary>失控的原因、解法、代价与来源</summary><p class="hprob"><b>失控的原因</b>{esc(c['problem'])}</p><p class="hsol"><b>解法</b>{esc(c['solution'])}</p><p class="hcost"><b>代价 / 争议</b>{esc(c['cost'])}</p>{link}{srcs(c.get('sources'))}</details></div></article>''')
    return f'''<section class="chap" id="harness"><div class="wide">{chead("harness")}
<div class="hgrid">{''.join(cards)}</div></div></section>'''

# ---------- 第六章
def ch_cards():
    groups = [('商业', '钱'), ('政治', '国旗'), ('技术', '能不能'), ('规则', '许不许'), ('文化', '敢不敢')]
    cols = []
    for tag, word in groups:
        cs = [c for c in C['cards'] if c['tag'] == tag]
        cs.sort(key=lambda c: int(re.match(r'\d{4}', c['year']).group(0)) if re.match(r'\d{4}', c['year']) else 0)
        items = ''.join(f'''<article class="why fade" id="why-{esc(c['id'])}"><div class="wy">{esc(c['year'])}</div><h3>{esc(c['title'])}</h3><p class="wq">{esc(E.WHY.get(c['id'], ''))}</p><div class="wn">{esc(c.get('number',''))} {conf(c.get('conf'))}</div><details class="fold"><summary>展开</summary><p>{esc(c['text'])}</p>{srcs(c.get('sources')) or '<p class="small">通行说法，未找到可引的一手来源。</p>'}</details></article>''' for c in cs)
        cols.append(f'<div class="wcol" data-tag="{tag}"><div class="wh"><b>{esc(tag)}</b><span>{esc(word)}</span><em>{len(cs)}</em></div>{items}</div>')
    return f'''<section class="chap" id="why"><div class="wide">{chead("why")}
<div class="wcols">{''.join(cols)}</div></div></section>'''

# ---------- 第六章
def ch_tools():
    return f'''<section class="chap" id="tools"><div class="wide">{chead("tools")}<div class="tools">
<div class="tool fade"><div class="hd"><b>比速度</b><p>输入一个速度，和步行、博尔特、高铁、客机、音速同场跑 10 秒。</p></div><div class="bd">{demos.race()}</div></div>
<div class="tool fade"><div class="hd"><b>比起步</b><p>两辆车各自宣称的起步秒数，看表盘谁先扫到目标速度——0.81 秒和 5 秒是两个世界。</p></div><div class="bd">{demos.drag()}</div></div>
</div><p class="small" style="margin-top:12px">参照：步行 5、博尔特 44.72、高铁 350、客机 900、音速 1,225 km/h（海平面 15 °C）；京沪高铁 1,318 km。</p></div></section>'''

# ---------- 卷末
def refs_block():
    groups = [('第一章 · 这一周', [s for n in C['now'] for s in n.get('sources', [])]),
              ('第二章 · 五条赛道（陆上轮式 / 铁路 / 水上）', [s for c in A['cells'] for s in c.get('sources', []) + c.get('also', {}).get('sources', [])]),
              ('序章 · 速度之旅', [s for l in journey.LEVELS for s in (src_lookup_raw(l['src']) or [])]),
              ('第二章 · 五条赛道（空中 / 太空 / 人体与动物）与速度尺', [s for c in B['cells'] for s in c.get('sources', []) + c.get('also', {}).get('sources', [])] + [s for c in B['scale'] for s in c.get('sources', [])]),
              ('第三章 · 两条总线', [s for p in B['record_line'] + C['daily_line'] for s in p.get('sources', [])]),
              ('第四章 · 物理墙', [s for w in WALLS.values() for s in w.get('sources', [])]),
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
        out.append(f'<h3>{esc(g)}</h3><ul>{"".join(items)}</ul>')
    return ''.join(out)

def credits():
    rows = ''.join(f'<tr><td>{esc(im["id"])}</td><td>{esc(im["subject"])}</td><td>{esc(im["author"])}，{esc(im.get("year",""))}</td><td>{esc(im["license"])}</td><td><a href="{esc(im["source_page"])}" target="_blank" rel="noopener">来源页</a></td></tr>' for im in IM.values())
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>作者 / 年代</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'

def endm():
    M = E.METHOD
    proc = ''.join(f'<li>{p}</li>' for p in M['process'])
    todo = ''.join(f'<li>{t}</li>' for t in M['todo'])
    return f'''<footer class="endm paper" id="end"><div class="wide">
<h2 class="fade">卷末 · 参考、方法与署名</h2>
<p class="small fade">都折叠着，点开看。</p>
<details class="fold big fade"><summary><h3>参考（按章分组）</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{proc}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{todo}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(IM)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">一周一题 · 第 {E.META['no']} 题 · {E.META['date']}<br>研究、绘图与核查：Claude（站长复核）</div>
</div></footer>
<button class="theme-btn" id="theme-btn" type="button" data-cover-hide aria-label="切换深浅色">深 / 浅</button>'''

# ---------- 数据（给 app.js）
def data():
    cells = {}
    for (t, e), c in CELLS.items():
        if c.get('subject') == '—': continue
        img = E.IMAGES.get(f'{t}-{e}')
        im = IM.get(img) if img else None
        cells[f'{t}-{e}'] = {k: c.get(k) for k in ('subject', 'kmh', 'speed', 'year', 'who', 'where', 'conf', 'why', 'note', 'sources', 'also')}
        if cells[f'{t}-{e}'].get('note'): cells[f'{t}-{e}']['note'] = re.sub(r'^口径[：:]\s*', '', cells[f'{t}-{e}']['note'])
        if cells[f'{t}-{e}'].get('also') and cells[f'{t}-{e}']['also'].get('note'): cells[f'{t}-{e}']['also']['note'] = re.sub(r'^口径[：:]\s*', '', cells[f'{t}-{e}']['also']['note'])
        cells[f'{t}-{e}']['track'] = dict((x[0], x[1]) for x in E.TRACKS)[t]
        cells[f'{t}-{e}']['era'] = f'{E.ERAS[e][0]} {E.ERAS[e][1]}'
        if im: cells[f'{t}-{e}']['img'] = {'file': 'assets/' + im['file'], 'cap': E.CAPTIONS.get(img, im.get('caption', '')), 'credit': f'{im["author"]}，{im["license"]}', 'alt': im['subject']}
    scale = {s['id']: s for s in B['scale']}
    rec = sorted(B['record_line'], key=lambda p: p['year']); rl, mx = [], 0
    for p in rec:
        if p['kmh'] > mx: rl.append({'y': max(p['year'], 1790), 'v': p['kmh'], 'n': p['short']}); mx = p['kmh']
    dl = [{'y': p['year'], 'v': p['kmh'], 'n': p['short']} for p in sorted(C['daily_line'], key=lambda p: p['year'])]
    return {'cells': cells, 'scale': scale, 'journey': journey.data(), 'lines': {'rec': rl, 'day': dl}, 'tool1': {'china': E.TOOL1['china_ew_km'], 'bjsh': E.TOOL1['bj_sh_km']}}

def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'demos.js'), encoding='utf-8').read()
    dark = ('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){' + DARK + '}}\n:root[data-theme="dark"]{' + DARK + '}')
    body = hero() + cnav() + '<main>' + ch_journey() + ch_now() + ch_matrix() + ch_lines() + ch_walls() + ch_harness() + ch_cards() + ch_tools() + '</main>' + endm()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E.META['desc'])).replace('{{DARK_BLOCKS}}', dark)
            .replace('{{BODY}}', body).replace('{{DATA_JSON}}', json.dumps(data(), ensure_ascii=False).replace('</', '<\\/')).replace('{{APP_JS}}', app))
    page, report = fixes.apply(page)
    for line in report: print(line)
    out = os.path.join(HERE, '..', 'index.html')
    open(out, 'w', encoding='utf-8').write(page)
    meta = {'no': E.META['no'], 'slug': E.META['slug'], 'title': E.META['title'], 'subtitle': E.META['subtitle'], 'date': E.META['date'], 'summary': E.META['desc'],
            'tags': E.META['tags'], 'format': E.META['format'], 'cover': 'cover.png', 'cover_focus': E.META['cover_focus'], 'cover_scheme': E.META['cover_scheme'], 'reading_time': E.META['reading_time'],
            'sources': ['FIA / FIM / FAI / UIM / 世界田径 / 吉尼斯的纪录页；NASA 与美国空军官方史（X-1、X-2、X-15、X-29、SR-71、Apollo 10、Artemis II、帕克探测器、Falcon 9 回收、Stapp）',
                        '英国国家铁路博物馆与科学博物馆集团、JR 东海、SNCF / Alstom、国铁集团与中车、澳大利亚国家海事博物馆、辛辛那提动物园',
                        'TechCrunch、Electrek、CBS 对 2026-10-15 Roadster 演示的报道；央视、新华网、界面对 GB 7258—2026 的报道；motorionline 对腾势 Z 的转述',
                        '图片 29 张：NASA、美国陆军 / 海军、美国国会图书馆 Bain 收藏、Gallica、大都会博物馆 Open Access、geograph.org.uk、Flickr（CC BY / CC BY-SA）；逐张署名见页面卷末与 src/images.json']}
    json.dump(meta, open(os.path.join(HERE, '..', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote index.html', len(page), 'bytes')

DARK = ('--bg:#121214;--surface:#1B1B1F;--surface-2:#242429;--ink:#F1EFE8;--ink-2:#CFCDC4;--muted:#9A9CA3;--line:#3E3F46;--line-2:#2B2C32;--grid:rgba(241,239,232,.06);'
        '--accent:#FF4F4F;--accent-ink:#FF6B6B;--wash:rgba(255,79,79,.13);--wash-2:rgba(255,79,79,.22);')

if __name__ == '__main__':
    main()
