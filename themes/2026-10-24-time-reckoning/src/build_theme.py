#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 6 题「时间的刻度」：把 research/*.json + editorial.py + images.json + lunar_table.json 合成 ../index.html 与 ../meta.json。
用法（仓库根目录）：python3 themes/2026-10-24-time-reckoning/src/build_theme.py
"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial as E
import figs, stage, demos, fixes

def esc(s): return html.escape(str(s), quote=True)
def J(name): return json.load(open(os.path.join(HERE, 'research', name), encoding='utf-8'))
A, B, C, D = J('cal_A.json'), J('cal_B.json'), J('clock_C.json'), J('sec_D.json')
WORLD = json.load(open(os.path.join(HERE, 'world.json'), encoding='utf-8'))
LUNAR = json.load(open(os.path.join(HERE, 'lunar_table.json'), encoding='utf-8'))
for _l in fixes.patch_data(A, B, C, D): print('data', _l)
NODES = {}
for route, src in (('A', A), ('B', B), ('C', C), ('D', D)):
    for n in src['nodes']: n['route'] = route; NODES[n['id']] = n
ALL_NODES = list(NODES.values())
LIC_SHORT = lambda s: 'CC0' if 'CC0' in s else 'CC BY-SA 2.0' if 'BY-SA' in s else 'CC BY 4.0' if 'CC BY 4.0' in s else 'Public Domain Mark' if 'Public Domain Mark' in s else '公有领域'
IM = {}
for i in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8')):
    if i.get('status') != 'ok': continue
    i['license_short'] = LIC_SHORT(i['license']); i['author_short'] = re.sub(r'（.*?）', '', i['author'])[:60]
    IM[i['id'].replace('img-d-', '')[3:]] = i
CONF_CLS = {'高': 'h', '中': 'm', '低': 'l'}
def conf(c): return f'<span class="conf {CONF_CLS.get(c, "m")}" title="置信度">{esc(c or "中")}</span>'
def srcs(ss, cls='src'):
    if not ss: return ''
    seen, uniq = set(), []
    for s in ss:
        k = s.get('url') or s.get('title')
        if not k or k in seen: continue
        seen.add(k); uniq.append(s)
    return f'<p class="{cls}">来源：' + '；'.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>' if s.get('url') else esc(s['title']) for s in uniq) + '</p>'
def caption_of(img_id, im): return im.get('subject', '')
def src_lookup(key):
    r, nid = key.split(':'); n = NODES.get(nid)
    if not n: return '', conf('中')
    return srcs(n.get('sources')[:4]), conf(n.get('confidence'))
LANE_NAME = dict(E.LANES); SCALE_NAME = dict(E.SCALES)

# ---------- 卷首（v2：全幅实拍 + 标题 + 一个动作）
def hero():
    H = E.HERO2; im = IM[H['img']]
    sub = ''.join(f'<span>{esc(x)}</span>' for x in H['sub'])
    arrow = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5"/></svg>'
    return f'''<header class="h3 band" id="top">
  <figure class="h3img"><img src="assets/{esc(im['file'])}" srcset="assets/{esc(H['img_1280'])} 1280w, assets/{esc(im['file'])} 2400w" sizes="100vw" alt="{esc(H['alt'])}" fetchpriority="high" decoding="async"></figure>
  <div class="h3in wide">
    <p class="h3k rise">{esc(H['kicker'])}</p>
    <h1 class="h3t rise">{esc(H['title'])}</h1>
    <p class="h3s rise">{sub}</p>
    <div class="h3a rise"><a class="btn" href="{esc(H['cta_href'])}">{esc(H['cta'])}{arrow}</a><span class="h3p">{esc(H['proof'])}</span></div>
  </div>
  <p class="h3cap">{esc(H['cap'])}</p>
</header>'''

def tagline_sec():
    lines, k = [], 0
    for ln in E.TAGLINE.split('/'):
        ws = []
        for w in ln.split('|'):
            ws.append(f'<span class="w" style="--i:{k}">{esc(w)}</span>'); k += 1
        lines.append('<span class="ln">' + ''.join(ws) + '</span>')
    nums = ''.join(f'<div class="tn"><b>{esc(v)}<small>{esc(u)}</small></b><p>{esc(t)}</p></div>' for v, u, t in E.NUMS)
    return f'''<section class="tagsec band" id="tagsec" aria-label="这一页的论点"><div class="tagstick"><div class="wide">
<p class="tagl" aria-label="{esc(E.TAGLINE.replace('|', '').replace('/', ''))}"><span aria-hidden="true">{''.join(lines)}</span></p>
<div class="tagrest"><p>{esc(E.TAGREST)}</p><div class="tnums">{nums}</div></div>
</div></div></section>'''

# ---------- 卷首（v1，留作对照，不再输出）
def hero_v1():
    M = E.META; H = E.HERO
    steps = ''.join(f'<li><span>{s}</span></li>' for s in H['steps'])
    week = ''.join(f'<span><i>{esc(d)}</i> <b>{esc(t)}</b> {esc(x)}</span>' for d, t, x in H['week'])
    stats = ''.join(f'<div class="stat"><div class="k">{esc(k)}</div><div class="v"><b class="cnt" data-to="{v}" data-dec="{dec}">{(('%.' + str(dec) + 'f') % v) if dec else v}</b><small>{esc(u)}</small></div><div class="d">{esc(d)}</div><div class="n">{esc(n)}</div></div>' for k, v, dec, u, d, n in H['stats'])
    t1, t2 = M['title'].split('：')
    return f'''
<header class="hero paper band"><div class="wide">
  <div class="strip fade"><span><b>一周一题</b>第 {M['no']} 题</span><span><b>上线</b>{M['date']}</span><span><b>格式</b>{M['format']}</span><span><b>阅读</b>{M['reading_time']}</span></div>
  <h1 class="fade">{esc(t1)}<br><span style="font-size:.5em;letter-spacing:.04em">{esc(t2)}</span></h1>
  <p class="sub fade">{esc(M['subtitle'])}</p>
  <div class="hero-grid"><div class="fade"><p class="thesis">{H['thesis']}</p><div class="week">{week}</div></div><ol class="steps fade">{steps}</ol></div>
  <div class="stats fade">{stats}</div>
</div></header>'''

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n}</small>{esc(t)}</a>' for cid, n, t, _ in E.CHAPTERS)
    links += '<a href="#end" data-nav="end"><small>末</small>参考 · 方法</a>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i><button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="切换深浅色">白天读</button></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第 {"一二三四五六七八"[n-1]} 章'
    return f'<div class="chead fade"><div class="cno">{n:02d}<small>{label}</small></div><h2>{esc(t)}</h2><p class="lede">{lede}</p></div>'

# ---------- 序章
def ch_journey():
    return (f'<section class="chap journey band" id="journey"><div class="wide">{chead("journey")}</div>' + stage.stage(C['cities'], WORLD, IM, caption_of) + stage.steps(IM, caption_of, src_lookup)
            + '<p class="jnote">日期牌按各城当时的民用历换算（公历 / 儒略历 / 伊斯兰算表历 / 科普特历 / 拜占庭纪年由算法算，中国与日本只写年号与月份）；表盘为格林尼治平太阳正午这一刻各城钟表的指向（1884 年前按经度算地方平时，之后按各城采用标准时的年份；2027 年含夏令时）。城市资料与来源见第三章与卷末。</p></section>')

# ---------- 第一章
def ch_now():
    tw = NODES['this-week']; cg = NODES['cgpm-2022-2026']; gr = NODES['greg-1582']
    cards = [
        ('10/25 · 周日', '欧洲拨回一小时', '01:00', 'UTC · 欧盟与英国同一瞬间', '欧盟指令 2000/84/EC 第 3 条：夏令时在 10 月最后一个周日 01:00 GMT 结束。2018 年委员会提议废除换时，理事会至今没有立场。上线次日凌晨，伦敦 02:00 BST 拨回 01:00 GMT。', [s for s in tw['sources'] if 'GOV.UK' in s['title'] or '2000/84' in s['title']]),
        ('11/1 · 周日', '北美拨回一小时，国会还在吵', '308 : 117', '众院 7/14 通过 H.R. 139', '按 15 U.S.C. §260a，美国在 11 月第一个周日凌晨 2 点拨回。众议院 7 月 14 日以 308 票对 117 票通过《阳光保护法》，要把夏令时变成永久；参议院没有排表决。所以 11 月 1 日照拨。', [s for s in tw['sources'] if 'NIST' in s['title'] or '260a' in s['title'] or 'Roll Call' in s['title']]),
        ('10/15 · 上周四', '凡尔赛：闰秒的终结', '2027-05-20', '第 28 届 CGPM 第 5 号决议', '连续 UTC 自 2027 年 5 月 20 日起生效，|UT1−UTC| 上限放宽到 3,600 秒。同次大会还决定 2030 年用光学频标重新定义秒（第 4 号），并为月球建立参考时间尺度（第 6 号）。', cg['sources'][:4]),
        ('10/24 · 今天', '农历九月十五 · 格里历生效 444 周年', '444', '年 · 1582-10-15 → 2026-10-24', '今天是丙午年九月十五，昨天霜降。1582 年的今天前后，罗马的日历刚跳过十天——从 10 月 4 日直接到 10 月 15 日。二十四节气是阳历的东西、农历是阴阳历，这一对矛盾正好用来开讲。', gr['sources'][:3] + [s for s in B['facts'] if s['id'] == 'today-lunar'][0]['sources'][:1]),
    ]
    out = ''.join(f'<article class="nowcard fade"><div class="d">{esc(d)}</div><h3>{esc(t)}</h3><p class="big">{esc(b)}<small>{esc(u)}</small></p><p>{esc(x)}</p>{srcs(ss)}</article>' for d, t, b, u, x, ss in cards)
    return f'<section class="chap" id="now"><div class="wide">{chead("now")}<div class="nowcards">{out}</div><p class="small" style="margin-top:14px">{esc(tw["text"])} {conf(tw.get("confidence"))}</p></div></section>'

# ---------- 节点卡
def node_card(nid, photo=True):
    n = NODES[nid]; img = E.NODE_IMG.get(nid); im = IM.get(img) if (photo and img) else None
    ph = f'<figure class="nph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{esc(im["subject"])} 图：{esc(im["author_short"])}，{esc(im["license_short"])}。</figcaption></figure>' if im else ''
    sc = ''.join(f'<i>{esc(SCALE_NAME.get(s, s))}</i>' for s in (n.get('scales') or [])[:3])
    mot = ' · '.join(E.MOTIVES.get(m, m) for m in (n.get('motive') or [])[:3])
    err = f'<span>误差</span><b{" class=ev" if nid in figs.LEAP_EVENTS else ""}>{esc(n["error"])}</b>' if n.get('error') else ''
    rows = ''.join(f'<span>{k}</span><b>{esc(v)}</b>' for k, v in (('办法', n.get('method')), ('代价', n.get('cost')), ('还在用吗', n.get('still_used'))) if v)
    nums = ''.join(f'<div><span>{esc(x["label"])}</span><b>{esc(x["value"])}{(" " + esc(x["unit"])) if x.get("unit") else ""}</b></div>' for x in (n.get('numbers') or [])[:4])
    disp = f'<p class="dispute"><b>两说</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    extra = adoption_table() if nid == 'adoption' else ''
    place = n['place']['name'] if n.get('place') and n['place'].get('name') else ''
    return f'''<article class="ncard fade" id="n-{esc(nid)}" data-node="{esc(nid)}" data-scales="{esc(' '.join(n.get('scales') or []))}">
<div class="nhd"><span class="ny">{esc(n['year_label'])}</span><span class="nlane">{esc(LANE_NAME.get(n['lane'], n['lane']))}{(' · ' + esc(place)) if place else ''}</span><span class="nsc">{sc}</span>{conf(n.get('confidence'))}</div>
<h3>{esc(n['title'])}</h3><p class="nobj">{esc(n.get('object', ''))}{(' · 动因：' + esc(mot)) if mot else ''}</p>
<div class="nerr"><span>要解决的</span><b>{esc(n.get('problem', ''))}</b>{err}</div>
<p class="why">{esc(n.get('why', ''))}</p>{ph}
<details class="fold"><summary>办法、代价、数字与来源</summary><div class="nerr" style="margin-top:0">{rows}</div><p>{esc(n['text'])}</p><div class="nnums">{nums}</div>{disp}{extra}{srcs(n.get('sources'))}</details></article>'''

def adoption_table():
    rows = ''.join(f'<tr><td>{esc(r["country"])}</td><td>{esc(r["year"])}</td><td>{esc(r.get("date_from") or "")} → {esc(r.get("date_to") or "")}</td><td class="sk">{esc(r.get("skipped_days") if r.get("skipped_days") is not None else "—")}</td><td>{esc(r.get("legal_or_common") or "")}{(" · " + esc(r["dispute"])) if r.get("dispute") else ""} {conf(r.get("confidence"))}</td></tr>' for r in A['adoption'])
    return f'<div class="adopt tblwrap"><h4>各国采用格里历（{len(A["adoption"])} 行）</h4><table><thead><tr><th>国家 / 地区</th><th>年</th><th>跳日</th><th>天数</th><th>口径</th></tr></thead><tbody>{rows}</tbody></table></div>'

# ---------- 第二章
def ch_year():
    lane_nodes = [dict(id=n['id'], year=n['year'], lane=n['lane'], scales=n.get('scales'), title=n['title'], year_label=n['year_label']) for n in ALL_NODES if n['lane'] in LANE_NAME and n['id'] not in ('sundial-noon',)]
    chips = '<div class="schips" id="scale-chips"><button type="button" data-scale="all" aria-pressed="true">全部</button>' + ''.join(f'<button type="button" data-scale="{k}" aria-pressed="false">{v}</button>' for k, v in E.SCALES) + '</div>'
    map_nodes = [n for n in ALL_NODES if n.get('place') and n['place'].get('lat') is not None]
    left = f'<div class="lanestage fade"><div class="lanebox">{figs.lanes_svg(lane_nodes)}</div>{figs.lanes_legend()}<div class="nmap">{figs.nodes_map(map_nodes, WORLD)}</div>{chips}<p class="small" style="margin-top:8px">泳道图收全页 {len(lane_nodes)} 个节点（第二到四章）；黄铜点 = 置闰、跳日、改制。卡片滚过视口中线时，泳道与地图上的落点一起亮。</p></div>'
    cards = ''.join(node_card(nid) for nid in E.CH2)
    return f'<section class="chap" id="year"><div class="wide">{chead("year")}<div class="lanewrap">{left}<div class="ncards">{cards}</div></div></div></section>'

def ch_day():
    cards = ''.join(node_card(nid) for nid in E.CH3)
    return f'<section class="chap" id="day"><div class="wide">{chead("day")}<div class="ncards two">{cards}</div></div></section>'

LADDER_ERR = {1: (90, '日晷'), 2: (300, '水钟'), 3: (900, '机轴钟 1300'), 4: (10, '摆钟 1656'), 5: (0.33, 'H4 1761'), 6: (0.02, 'Shortt 1921'), 7: (1e-3, '石英 1927'), 8: (1e-5, '铯束 1955'), 9: (1.5e-10, 'NIST-F1 1999'), 10: (1e-11, 'NIST-F2 2014'), 11: (5e-14, '光钟 2025'), 'ref': (3.8e-5, 'GPS 相对论修正')}
def ch_second():
    cards = ''.join(node_card(nid) for nid in E.CH4)
    lad = []
    for it in D['ladder']:
        e = LADDER_ERR.get(it['rank'])
        if e: lad.append(dict(name=it['name'], year=it.get('year_label', it.get('year')), err_s_per_day=e[0], short=e[1], note=it['per_day']))
    srcl = srcs([it['source'] for it in D['ladder'] if it.get('source')][:8])
    return f'''<section class="chap" id="second"><div class="wide">{chead("second")}<div class="ncards two">{cards}</div>
<figure class="ladderfig fade">{figs.ladder_svg(lad)}<figcaption><b>精度阶梯。</b>每台钟每天差多少秒，对数尺，向左每格精一千倍：从日晷的一两分钟到光钟的五十飞秒，跨十五个数量级。GPS 卫星钟若不做相对论修正，每天会快 38 微秒——比 1955 年的第一台铯钟还差。悬停看口径；数字多为量级，出处见下。{srcl}</figcaption></figure></div></section>'''

# ---------- 第五章
def ch_walls():
    out = []
    for w in E.WALLS:
        dm = {'leap': demos.wall_leap, 'lunar': demos.wall_lunar, 'eot': demos.wall_eot, 'noon': lambda: demos.wall_noon('nn'), 'lod': lambda: demos.wall_lod(figs.dt_svg(DELTA_T, LEAP_YEARS))}[w['id']]()
        ss = [s for key in w['src'] for s in NODES[key.split(':')[1]].get('sources', [])[:2]]
        out.append(f'<article class="wall fade" id="wall-{w["id"]}"><div class="hd"><b>{esc(w["title"])}</b><span class="f">{esc(w["formula"])}</span></div>{dm}<details class="fold"><summary>这面墙是怎么回事</summary><p>{esc(w["text"])}</p>{srcs(ss)}</details></article>')
    return f'<section class="chap" id="walls"><div class="wide">{chead("walls")}<div class="walls">{"".join(out)}</div></div></section>'

# ---------- 第六章
DST_CITIES = [('london', '伦敦', 0, 'eu'), ('paris', '巴黎', 1, 'eu'), ('berlin', '柏林', 1, 'eu'), ('istanbul', '伊斯坦布尔', 3, 'none'), ('moscow', '莫斯科', 3, 'none'), ('cairo', '开罗', 2, 'eg'), ('delhi', '德里', 5.5, 'none'), ('kathmandu', '加德满都', 5.75, 'none'), ('beijing', '北京', 8, 'none'), ('urumqi', '乌鲁木齐（北京时间）', 8, 'none'), ('tokyo', '东京', 9, 'none'), ('sydney', '悉尼', 10, 'au'), ('auckland', '奥克兰', 12, 'nz'), ('new-york', '纽约', -5, 'us'), ('chicago', '芝加哥', -6, 'us'), ('los-angeles', '洛杉矶', -8, 'us'), ('toronto', '多伦多', -5, 'us'), ('mexico-city', '墨西哥城', -6, 'none'), ('santiago', '圣地亚哥', -4, 'cl')]
def ch_tools():
    opts = ''.join(f'<option value="{cid}">{esc(n)}</option>' for cid, n, o, r in DST_CITIES)
    T = {t['id']: t for t in E.TOOLS}
    def tool(tid, body, full=False): return f'<div class="tool fade{" full" if full else ""}"><div class="hd"><b>{esc(T[tid]["title"])}</b><p>{esc(T[tid]["lede"])}</p></div>{body}</div>'
    return f'''<section class="chap" id="tools"><div class="wide">{chead("tools")}<div class="tools">
{tool('conv', demos.tool_conv(), True)}
{tool('noon', demos.wall_noon('tl'))}
{tool('dst', demos.tool_dst(opts))}
{tool('leap', demos.tool_leaps(), True)}
</div></div></section>'''

# ---------- 第七章 规则
def find_src(nid, pat):
    for s in NODES.get(nid, {}).get('sources', []):
        if re.search(pat, s.get('title', '') + ' ' + s.get('url', ''), re.I): return s
    return None
def ch_rules():
    items = [
        ('1582', '教皇诏书 Inter gravissimas', '格里历：闰法 400 年 97 闰，1582-10-04 的次日为 10-15。', find_src('greg-1582', r'gravissimas|诏书')),
        ('1750', '英国《历法（新式）法》Calendar (New Style) Act 1750', '1752-09-02 的次日为 09-14；岁首改为 1 月 1 日。', find_src('adoption', r'1750|legislation')),
        ('1880', '英国《法定时间定义法》Statutes (Definition of Time) Act 1880', '格林尼治平时成为大不列颠法定时间。', find_src('railway-time', r'1880|Definition') or {'url': 'https://www.legislation.gov.uk/ukpga/Vict/43-44/9', 'title': 'legislation.gov.uk'}),
        ('1884', '国际子午线会议 Final Act', '七项决议：格林尼治为本初子午线，「世界日」从格林尼治子夜起。', find_src('meridian-1884', r'gutenberg|Protocols|Final')),
        ('1918', '美国《标准时间法》Standard Time Act', '联邦法律确立时区并实行夏令时。', find_src('dst-history', r'1918|Standard Time Act|260')),
        ('1966', '美国《统一时间法》Uniform Time Act · 15 U.S.C. §260a', '全国统一夏令时起止日；2005 年能源政策法改为 3 月第二个周日至 11 月第一个周日。', find_src('this-week', r'260a')),
        ('1967', '第 13 届 CGPM 第 1 号决议', '秒 = 铯-133 基态超精细跃迁 9,192,631,770 个周期。', find_src('essen-1955', r'1967')),
        ('1986', '国务院关于实行夏时制的通知 / 1992 年暂停', '中国 1986-05-04 起实行、1992 年起暂停。', find_src('dst-history', r'国务院|gov\.cn|1986')),
        ('2000', '欧盟指令 2000/84/EC', '3 月最后一个周日 01:00 GMT 起、10 月最后一个周日 01:00 GMT 止。', find_src('this-week', r'2000/84')),
        ('2017', 'GB/T 33661-2017《农历的编算和颁行》', '朔日为初一、冬至所在月为十一月、无中气置闰，以北京时间为准。', find_src('prc-1949', r'33661|openstd')),
        ('2022', '第 27 届 CGPM 第 4 号决议', '「UT1−UTC 之差的最大值将在 2035 年或之前提高」。', find_src('cgpm-2022-2026', r'2022')),
        ('2026', '第 28 届 CGPM 第 5 号决议', '连续 UTC 自 2027-05-20 起生效，|UT1−UTC| 上限 3,600 秒。', find_src('cgpm-2022-2026', r'Resolution 5')),
        ('持续', 'IANA tz 数据库', '各国时区与夏令时规则的代码化，附历史注释；由志愿者维护，通过邮件列表投稿。', find_src('computer-era', r'iana|tz')),
    ]
    li = ''.join(f'<li><span class="ry">{esc(y)}</span><div><b>{esc(t)}</b><p>{esc(d)}' + (f' <a href="{esc(s["url"])}" target="_blank" rel="noopener">原文 / 入口</a>' if s and s.get('url') else '') + '</p></div></li>' for y, t, d, s in items)
    return f'<section class="chap" id="rules"><div class="wide">{chead("rules")}<details class="fold big fade"><summary><h3>十三份文件</h3></summary><ol class="rules">{li}</ol></details></div></section>'

# ---------- 卷末
def refs_block():
    groups = [('序章 · 对历与对表（城市资料）', [s for c in C['cities'] for s in c.get('sources', [])]),
              ('第一章 · 这一周', NODES['this-week']['sources'] + NODES['cgpm-2022-2026']['sources']),
              ('第二章 · 年与月（A 路：两河 / 埃及 / 欧洲 / 希伯来 / 伊斯兰 / 波斯 / 印度 / 全球）', [s for n in A['nodes'] for s in n.get('sources', [])] + [s for r in A['adoption'] for s in r.get('sources', [])]),
              ('第二章 · 年与月（B 路：中国与东亚 / 中美洲）', [s for n in B['nodes'] for s in n.get('sources', [])] + [s for f in B['facts'] for s in f.get('sources', [])]),
              ('第三章 · 日与时', [s for n in C['nodes'] for s in n.get('sources', [])] + [s for f in C['facts'] for s in f.get('sources', [])]),
              ('第四章 · 秒', [s for n in D['nodes'] for s in n.get('sources', [])] + [it['source'] for it in D['ladder'] if it.get('source')])]
    out = []
    for g, ss in groups:
        seen, items = set(), []
        for s in ss:
            if not isinstance(s, dict): continue
            k = s.get('url') or s.get('title')
            if not k or k in seen: continue
            seen.add(k)
            items.append(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>' if s.get('url') else f'<li>{esc(s["title"])}</li>')
        out.append(f'<h3>{esc(g)}</h3><ul>{"".join(items)}</ul>')
    return ''.join(out)

def credits():
    rows = ''.join(f'<tr><td>{esc(k)}</td><td>{esc(im["subject"])}</td><td>{esc(im["author_short"])}，{esc(im.get("year",""))}</td><td>{esc(im["license_short"])}</td><td><a href="{esc(im["url_page"])}" target="_blank" rel="noopener">{esc(im["source_name"])}</a></td></tr>' for k, im in IM.items())
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>作者 / 年代</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'

def endm():
    M = E.METHOD
    unv = sorted(set(A.get('unverified', []) + B.get('unverified', []) + C.get('unverified', []) + D.get('unverified', [])))
    return f'''<footer class="endm paper" id="end"><div class="wide">
<h2 class="fade">卷末 · 参考、方法与署名</h2>
<p class="small fade">都折叠着，点开看。</p>
<details class="fold big fade"><summary><h3>参考（按章分组）</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{''.join(f'<li>{p}</li>' for p in M['process'])}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{''.join(f'<li>{t}</li>' for t in M['todo'])}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(IM)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">一周一题 · 第 {E.META['no']} 题 · {E.META['date']}<br>研究、绘图与核查：Claude（站长复核）</div>
</div></footer>'''

# ---------- 数据
DELTA_T = [(1900, -2.7), (1910, 10.5), (1920, 21.2), (1930, 24.0), (1940, 24.3), (1950, 29.1), (1960, 33.2), (1970, 40.2), (1980, 50.5), (1990, 56.9), (2000, 63.8), (2010, 66.1), (2016, 68.1), (2020, 69.4), (2025, 69.1), (2030, 69.6)]
LEAPS = [s['date'] for s in D['leap_seconds']]
LEAP_YEARS = [int(s[:4]) + (0.5 if s[5:] == '06-30' else 1.0) for s in LEAPS]
def data():
    return {'stage': stage.data(C['cities']), 'lunar': LUNAR, 'lunarLeap': {y: v[1] for y, v in LUNAR.items()}, 'deltaT': DELTA_T, 'leaps': LEAPS,
            'dstCities': {cid: {'n': n, 'o': o, 'r': r} for cid, n, o, r in DST_CITIES}}

def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'calendars.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'demos.js'), encoding='utf-8').read()
    dark = ('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){' + DARK + '}}\n:root[data-theme="dark"]{' + DARK + '}')
    body = hero() + cnav() + '<main>' + tagline_sec() + ch_journey() + ch_now() + ch_year() + ch_day() + ch_second() + ch_walls() + ch_tools() + ch_rules() + '</main>' + endm()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E.META['desc'])).replace('{{DARK_BLOCKS}}', dark)
            .replace('{{BODY}}', body).replace('{{DATA_JSON}}', json.dumps(data(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('{{APP_JS}}', app))
    page, report = fixes.apply(page)
    for line in report: print(line)
    open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(page)
    meta = {'no': E.META['no'], 'slug': E.META['slug'], 'title': E.META['title'], 'subtitle': E.META['subtitle'], 'date': E.META['date'], 'summary': E.META['desc'],
            'tags': E.META['tags'], 'format': E.META['format'], 'cover': 'cover.png', 'cover_focus': E.META['cover_focus'], 'cover_scheme': E.META['cover_scheme'], 'reading_time': E.META['reading_time'],
            'sources': ['BIPM（第 27、28 届 CGPM 决议、CCTF 主席声明、SI 手册）、IERS 公报 C 72（经 IANA tz 列表转发）、USNO tai-utc.dat 与 deltat.data、NIST、GPS.gov',
                        '1884 年国际子午线会议记录（Gutenberg）、英国 1750 与 1880 年法案（legislation.gov.uk）、美国法典 15 U.S.C. §§260–267、EUR-Lex 2000/84/EC、gov.uk、IANA tz 数据库源文件与 theory.html、国务院公报页码、国家授时中心',
                        'Inter gravissimas 英译（Wikisource）、Reingold & Dershowitz《Calendrical Calculations》、IANA tz calendars 文件（Grotefend / Nørby 采用表）、香港天文台公历农历对照与朔望表、国家标准全文公开系统（GB/T 33661-2017）、新华社、紫金山天文台、UNESCO、史密森尼 NMAI、Britannica',
                        '图片 18 张：大都会博物馆 Open Access（CC0）、美国国会图书馆、NIST、Wellcome Collection、geograph.org.uk（CC BY-SA 2.0）；逐张署名见页面卷末与 src/images.json']}
    json.dump(meta, open(os.path.join(HERE, '..', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote index.html', len(page), 'bytes')

DARK = ('--bg:#0E1726;--surface:#14203A;--surface-2:#1B2A48;--ink:#EDE6D3;--ink-2:#C8C1AE;--muted:#8E8C82;--line:#2A3650;--line-2:#22304A;--grid:rgba(237,230,211,.05);'
        '--accent:#D9A441;--accent-ink:#E2B45B;--wash:rgba(217,164,65,.13);--wash-2:rgba(217,164,65,.22);')

if __name__ == '__main__':
    main()
