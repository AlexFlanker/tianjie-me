#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 6 题「时间的刻度」v2（2026-10-30 起，按第 7 题 v3 的版面系统连结构一起重排）：
research/*.json + editorial.py（v1 文案与数据）+ editorial2.py（v2 的章节、短文与图注）+ images.json + lunar_table.json → ../index.html 与 ../meta.json。
用法（仓库根目录）：python3 themes/2026-10-24-time-reckoning/src/build_theme.py
"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial as E
import editorial2 as E2
import figs, stage, demos, charts, fixes

def esc(s): return html.escape(str(s), quote=True)
def J(name): return json.load(open(os.path.join(HERE, 'research', name), encoding='utf-8'))
A, B, C, D = J('cal_A.json'), J('cal_B.json'), J('clock_C.json'), J('sec_D.json')
LUNAR = json.load(open(os.path.join(HERE, 'lunar_table.json'), encoding='utf-8'))
for _l in fixes.patch_data(A, B, C, D): print('data', _l)
NODES = {}
for route, src in (('A', A), ('B', B), ('C', C), ('D', D)):
    for n in src['nodes']: n['route'] = route; NODES[n['id']] = n
def LIC_SHORT(s):
    if 'CC0' in s: return 'CC0'
    if 'BY-SA' in s: return 'CC BY-SA 2.0'
    if 'CC BY 4.0' in s: return 'CC BY 4.0'
    if 'Public Domain Mark' in s: return 'Public Domain Mark'
    if '无已知版权限制' in s: return '无已知版权限制'
    return '公有领域'
IM = {}
for i in json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8')):
    if i.get('status') != 'ok': continue
    i['license_short'] = LIC_SHORT(i['license']); i['author_short'] = re.sub(r'（.*?）', '', i['author'])[:60]
    IM[i['id'].replace('img-d-', '')[3:]] = i
NODE_IMG = dict(E.NODE_IMG, **E2.NODE_IMG_ADD)
CONF_CLS = {'高': 'h', '中': 'm', '低': 'l'}
def conf(c): return f'<span class="conf {CONF_CLS.get(c, "m")}" title="资料置信度：高 = 一手或两个独立权威来源一致；中 = 只有一个权威来源或小有出入；低 = 只有二手或通行说法">置信度 {esc(c or "中")}</span>'
def srcs(ss, cls='src', n=8):
    if not ss: return ''
    seen, uniq = set(), []
    for s in ss:
        if not isinstance(s, dict): continue
        k = s.get('url') or s.get('title')
        if not k or k in seen: continue
        seen.add(k); uniq.append(s)
    return f'<p class="{cls}">来源：' + '；'.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>' if s.get('url') else esc(s['title']) for s in uniq[:n]) + '</p>'
def capspan(im, n=80):
    """图注分两段：说明可以截短，署名（作者 + 许可）永远完整显示。"""
    s = im['subject']; s = s[:n] + '…' if len(s) > n else s
    return f'<span class="cs">{esc(s)}</span><span class="cr">图：{esc(im["author_short"])}，{esc(im["license_short"])}。</span>'
LANE_NAME = dict(E.LANES)
CN_NUM = '零一二三四五六七八九十'
def cn_count(n): return (CN_NUM[n // 10] if n >= 20 else '') + ('十' if n >= 10 else '') + (CN_NUM[n % 10] if n % 10 else '') if n >= 10 else CN_NUM[n]

# ---------- 卷首：全幅实拍 + 标题 + 一个动作
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

def cnav():
    links = ''.join(f'<a href="#{cid}" data-nav="{cid}"><small>{n:02d}</small>{esc(t)}</a>' for cid, n, t, _ in E2.CHAPTERS)
    links += '<a href="#end" data-nav="end"><small>末</small>规矩与参考</a>'
    links += '<button type="button" class="ntheme" id="theme-btn" data-cover-hide aria-label="切换深浅色">白天读</button>'
    return f'<nav class="cnav" id="cnav" aria-label="章节"><div class="row">{links}<i class="prog" id="prog"></i></div></nav>'

def chead(cid):
    _, n, t, lede = next(c for c in E2.CHAPTERS if c[0] == cid)
    label = '序章' if n == 0 else f'第{"一二三四五六七八"[n-1]}章'
    txt = f'<div class="ptext"><p class="cno">{n:02d} · {label}</p><h2>{esc(t)}</h2><p class="lede">{esc(lede)}</p></div>'
    O = E2.OPENERS.get(cid)
    if not O: return f'<header class="chead fade">{txt}</header>'
    im = IM[O['img']]
    fig = (f'<figure class="pimg"><img src="assets/{esc(im["file"])}" srcset="assets/{esc(O["small"])} 1280w, assets/{esc(im["file"])} {O["w"]}w" '
           f'sizes="(min-width: 981px) 58vw, 100vw" alt="{esc(O["alt"])}" loading="lazy" decoding="async"><figcaption>{esc(O["cap"])}</figcaption></figure>')
    return f'<header class="chead plate fade">{txt}{fig}</header>'

def sech(k, title, lede=''):
    return f'<header class="sech fade"><span class="k">{esc(k)}</span><h3>{esc(title)}</h3>' + (f'<p>{esc(lede)}</p>' if lede else '') + '</header>'

# ---------- 序章：全屏舞台
def ch_journey():
    _, n, t, lede = E2.CHAPTERS[0]
    intro = f'<header class="tlintro wide fade"><p class="cno">00 · 序章</p><h2>{esc(t)}</h2><p class="lede">{esc(lede)}</p></header>'
    note = ('<p class="tlnote">日期牌按各城当时的民用历换算：公历、儒略历、伊斯兰算表历、科普特历、拜占庭纪年由算法算，中国与日本在改用公历以前只写年号与月份。'
            '表盘是格林尼治平太阳正午这一刻各城钟表的指向：各城采用标准时以前按经度算地方平时（伦敦 1847 年、纽约 1883 年最早改），之后按标准时，1949、1972、2027 年含当年的夏令时。'
            '每一步的出处在它链接的节点里，城市资料见卷末参考。</p>')
    return f'<section class="chap tl band" id="journey" aria-label="序章 · 对历与对表">{intro}{stage.stage(C["cities"], IM, "assets/earth-day-1920.jpg")}{note}</section>'

# ---------- 节点行（三章共用）
def node_kind(nid): return E2.KIND.get(nid, '')
def node_era(n):
    for k, _, lo, hi in E2.ERAS:
        if lo <= n['year'] < hi: return k
    return 'n'
def node_row(nid):
    n = NODES[nid]; img = NODE_IMG.get(nid); im = IM.get(img) if img else None
    yl = n.get('year_label') or str(n['year']); short = E2.YEAR_SHORT.get(nid, yl)
    place = (n.get('place') or {}).get('name') or ''
    sub = ' · '.join(x for x in (place, LANE_NAME.get(n['lane'], '')) if x)
    kind = node_kind(nid)
    thumb = f'<span class="lthumb"><img src="assets/{esc(im["file"])}" alt="" loading="lazy"></span>' if im else '<span class="lthumb none"></span>'
    facts = ''.join(f'<dt>{k}</dt><dd{" class=ev" if (k == "误差" and nid in figs.LEAP_EVENTS) else ""}>{esc(v)}</dd>' for k, v in (('要解决的', n.get('problem')), ('办法', n.get('method')), ('误差', n.get('error')), ('代价', n.get('cost')), ('还在用吗', n.get('still_used'))) if v)
    ph = f'<figure class="lph"><img src="assets/{esc(im["file"])}" alt="{esc(im["subject"])}" loading="lazy"><figcaption>{capspan(im, 64)}</figcaption></figure>' if im else ''
    nums = ''.join(f'<div><span>{esc(x["label"])}</span><b>{esc(x["value"])}{(" " + esc(x["unit"])) if x.get("unit") else ""}</b></div>' for x in (n.get('numbers') or [])[:6])
    disp = f'<p class="dispute"><b>两说</b>{esc(n["dispute"])}</p>' if n.get('dispute') else ''
    extra = adoption_table() if nid == 'adoption' else ''
    attrs = f'data-g-era="{node_era(n)}" data-g-lane="{esc(n["lane"])}" data-g-kind="{esc(kind)}"'
    return f'''<article class="lrow" id="n-{esc(nid)}" data-id="{esc(nid)}" {attrs}>
<button type="button" class="lhead" aria-expanded="false" aria-controls="lm-{esc(nid)}">
<span class="ldate"><b>{esc(short)}</b>{f'<small>{esc(yl)}</small>' if short != yl else ''}</span>
<span class="lname"><b>{esc(n['title'])}</b><small>{esc(sub)}</small></span>
<span class="lkind">{esc(E2.KINDS.get(kind, ''))}</span><span class="lerr">{esc(E2.ERR_SHORT.get(nid, ''))}</span>
{thumb}<span class="lchev" aria-hidden="true"></span></button>
<div class="lmore" id="lm-{esc(nid)}" role="region" aria-label="{esc(n['title'])}"><div class="lmore-in">
<div class="lbody{'' if im else ' nophoto'}"><div><p class="lwhy">{esc(n.get('why', ''))}</p><dl class="lfacts">{facts}</dl></div>{ph}</div>
<details class="fold"><summary>全文、数字、两说与来源 {conf(n.get('confidence'))}</summary><p>{esc(n['text'])}</p>{('<div class="nnums">' + nums + '</div>') if nums else ''}{disp}{extra}{srcs(n.get('sources'))}</details>
</div></div></article>'''

def adoption_table():
    rows = ''.join(f'<tr><td>{esc(r["country"])}</td><td>{esc(r["year"])}</td><td>{esc(r.get("date_from") or "")} → {esc(r.get("date_to") or "")}</td><td class="sk">{esc(r.get("skipped_days") if r.get("skipped_days") is not None else "—")}</td><td>{esc(r.get("legal_or_common") or "")}{(" · " + esc(r["dispute"])) if r.get("dispute") else ""} {conf(r.get("confidence"))}</td></tr>' for r in A['adoption'])
    return f'<div class="adopt tblwrap"><h4>各国采用格里历（{len(A["adoption"])} 行）</h4><table><thead><tr><th>国家 / 地区</th><th>年</th><th>跳日</th><th>天数</th><th>口径</th></tr></thead><tbody>{rows}</tbody></table></div>'

def lens_groups(ids, lenses, kind_order):
    by_year = lambda xs: sorted(xs, key=lambda i: (NODES[i]['year'], i))
    out = {}
    for lens, _ in lenses:
        if lens == 'era': gs = [(k, l, [i for i in ids if node_era(NODES[i]) == k]) for k, l, lo, hi in E2.ERAS]
        elif lens == 'lane': gs = [(k, l, [i for i in ids if NODES[i]['lane'] == k]) for k, l in E.LANES]
        else: gs = [(k, E2.KINDS[k], [i for i in ids if node_kind(i) == k]) for k in kind_order]
        out[lens] = [dict(k=k, label=l, ids=by_year(xs)) for k, l, xs in gs if xs]
    return out
LENS = {'year': lens_groups(E.CH2, E2.YEAR_LENSES, E2.YEAR_KIND_ORDER), 'day': lens_groups(E.CH3, E2.DAY_LENSES, E2.DAY_KIND_ORDER)}
LENS_NAME = {'year': dict(E2.YEAR_LENSES), 'day': dict(E2.DAY_LENSES)}

def lens_list(key, ids, lenses, label):
    tabs = ''.join(f'<button type="button" role="tab" data-lens="{k}" aria-selected="{"true" if k == "era" else "false"}">{esc(t)}</button>' for k, t in lenses)
    body = ''.join(f'<div class="lgh" data-g="{g["k"]}"><b>{esc(g["label"])}</b><small>{len(g["ids"])} 行</small></div>' + ''.join(node_row(i) for i in g['ids']) for g in LENS[key]['era'])
    return f'''<div class="lwrap" data-lw="{key}">
<div class="lensbar fade"><span class="lensk">按</span><div class="lens" role="tablist" aria-label="{esc(label)}">{tabs}</div><span class="lensnote">{cn_count(len(ids))}行 · 点一行展开</span></div>
<div class="lcols" aria-hidden="true"><span>年代</span><span>节点 · 地点</span><span>办法</span><span>误差 / 结果</span></div>
<div class="lgrid">{body}</div></div>'''

def plain_list(ids):
    return '<div class="lwrap"><div class="lgrid">' + ''.join(node_row(i) for i in sorted(ids, key=lambda i: NODES[i]['year'])) + '</div></div>'

def tool(tid, body):
    title, lede = E2.TOOLS[tid]
    return f'<div class="tool fade" id="tool-{tid}"><div class="hd"><span class="k">动手</span><b>{esc(title)}</b><p>{esc(lede)}</p></div>{body}</div>'

# ---------- 第一章 年与月
def ch_year():
    Dr = E2.DRIFT
    return f'''<section class="chap" id="year"><div class="wide">{chead("year")}
<div class="sec" id="drift-sec">{sech("主图 · 拖动竖线换年份", Dr["title"], Dr["lede"])}<div class="fade">{charts.drift()}</div><p class="fnote">{esc(Dr["note"])}</p></div>
<div class="sec" id="year-nodes">{sech("节点", cn_count(len(E.CH2)) + "个节点", "按年代、文明或办法排。每行一句误差；点开看要解决的问题、办法、代价，全文与来源在最底下的折叠里。")}{lens_list("year", E.CH2, E2.YEAR_LENSES, "年与月的节点：分组方式")}</div>
{tool("conv", demos.tool_conv())}
</div></section>'''

# ---------- 第二章 日与时
DST_CITIES = [('london', '伦敦', 0, 'eu'), ('paris', '巴黎', 1, 'eu'), ('berlin', '柏林', 1, 'eu'), ('istanbul', '伊斯坦布尔', 3, 'none'), ('moscow', '莫斯科', 3, 'none'), ('cairo', '开罗', 2, 'eg'), ('delhi', '德里', 5.5, 'none'), ('kathmandu', '加德满都', 5.75, 'none'), ('beijing', '北京', 8, 'none'), ('urumqi', '乌鲁木齐（北京时间）', 8, 'none'), ('tokyo', '东京', 9, 'none'), ('sydney', '悉尼', 10, 'au'), ('auckland', '奥克兰', 12, 'nz'), ('new-york', '纽约', -5, 'us'), ('chicago', '芝加哥', -6, 'us'), ('los-angeles', '洛杉矶', -8, 'us'), ('toronto', '多伦多', -5, 'us'), ('mexico-city', '墨西哥城', -6, 'none'), ('santiago', '圣地亚哥', -4, 'cl')]
def ch_day():
    N = E2.NOON
    opts = ''.join(f'<option value="{cid}">{esc(n)}</option>' for cid, n, o, r in DST_CITIES)
    return f'''<section class="chap" id="day"><div class="wide">{chead("day")}
<div class="sec" id="noon-sec">{sech("主图 · 切年代、拖日期、填经度", N["title"], N["lede"])}<div class="fade">{charts.noon()}</div><p class="fnote">{esc(N["note"])}</p></div>
<div class="sec" id="day-nodes">{sech("节点", cn_count(len(E.CH3)) + "个节点", "从时辰与刻到时区地图：怎么分一天、怎么造钟、怎么把一个国家的钟对齐、怎么一年拨两次。")}{lens_list("day", E.CH3, E2.DAY_LENSES, "日与时的节点：分组方式")}</div>
{tool("dst", demos.tool_dst(opts))}
</div></section>'''

# ---------- 第三章 秒
LADDER_ERR = {1: (90, '日晷'), 2: (300, '水钟'), 3: (900, '机轴钟'), 4: (10, '摆钟'), 5: (0.33, 'H4'), 6: (0.02, 'Shortt'), 7: (1e-3, '石英钟'), 8: (1e-5, '铯束钟'), 9: (1.5e-10, 'NIST-F1'), 10: (1e-11, 'NIST-F2'), 11: (5e-14, '光钟')}
LADDER_YR = {1: '前 1500', 2: '前 1500', 3: '14 世纪', 4: '1656', 5: '1761', 6: '1921', 7: '1927', 8: '1955', 9: '1999', 10: '2014', 11: '2025'}
def ladder_rungs():
    out = []
    for it in D['ladder']:
        if it['rank'] == 'ref': continue
        v, short = LADDER_ERR[it['rank']]; im = IM.get(E2.LADDER_IMG.get(it['rank'], ''))
        out.append(dict(k=it['rank'], v=v, short=short, yr=LADDER_YR[it['rank']], name=it['name'], year=it.get('year_label') or str(it.get('year')), principle=it.get('principle', ''),
                        per_day=it.get('per_day', ''), one=it.get('one_second_in', '') if it.get('one_second_in') not in (None, '—', '-') else '', note=it.get('note', ''), conf=it.get('confidence', ''), vtxt=charts.si(v),
                        img=('assets/' + im['file']) if im else '', alt=im['subject'] if im else '', cap=(('示意：' if it['rank'] in (1, 2, 5) else '') + im['subject'][:64] + ('…' if len(im['subject']) > 64 else '')) if im else '', cred=f'图：{im["author_short"]}，{im["license_short"]}。' if im else ''))
    return out
DELTA_T = [(1900, -2.72), (1910, 10.5), (1920, 21.2), (1930, 24.0), (1940, 24.3), (1950, 29.1), (1960, 33.2), (1970, 40.2), (1980, 50.5), (1990, 56.9), (2000, 63.83), (2010, 66.1), (2016, 68.1), (2020, 69.36), (2025, 69.14)]  # 年初值；2025 年以后无数据，不外推
LEAPS = [s['date'] for s in D['leap_seconds']]
LEAP_YEARS = [(s, int(s[:4]) + (0.5 if s[5:] == '06-30' else 1.0)) for s in LEAPS]
def ch_second():
    L, Lo = E2.LADDER, E2.LOD
    ref = [it for it in D['ladder'] if it['rank'] == 'ref'][0]
    gps = dict(v=3.8e-5, label='GPS 卫星钟若不做相对论修正：每天快约 38 微秒')
    srcl = srcs([it['source'] for it in D['ladder'] if it.get('source')], n=10)
    return f'''<section class="chap" id="second"><div class="wide">{chead("second")}
<div class="sec" id="ladder-sec">{sech("主图 · 点一级或用方向键", L["title"], L["lede"])}<div class="fade">{charts.ladder(ladder_rungs(), gps)}</div><p class="fnote">{esc(L["note"])}</p>{srcl.replace('class="src"', 'class="fnote src"')}</div>
<div class="sec" id="lod-sec">{sech("主图 · 拖动竖线换年份", Lo["title"], Lo["lede"])}<div class="fade">{charts.lod(DELTA_T, LEAP_YEARS)}</div><p class="fnote">{esc(Lo["note"])}</p></div>
<div class="sec" id="second-nodes">{sech("节点", cn_count(len(E.CH4)) + "个节点", "从地球这只钟、第一台铯钟到 2026 年的凡尔赛决议。")}{plain_list(E.CH4)}</div>
{tool("leaps", demos.tool_leaps())}
</div></section>'''

# ---------- 卷末：规矩 + 折叠
def find_src(nid, pat):
    for s in NODES.get(nid, {}).get('sources', []):
        if re.search(pat, s.get('title', '') + ' ' + s.get('url', ''), re.I): return s
    return None
RULES = [
    ('1582', '教皇诏书 Inter gravissimas', '格里历：闰法 400 年 97 闰，1582-10-04 的次日为 10-15。', ('greg-1582', r'gravissimas|诏书')),
    ('1750', '英国《历法（新式）法》Calendar (New Style) Act 1750', '1752-09-02 的次日为 09-14；岁首改为 1 月 1 日。', ('adoption', r'1750|legislation')),
    ('1880', '英国《法定时间定义法》Statutes (Definition of Time) Act 1880', '格林尼治平时成为大不列颠法定时间。', ('railway-time', r'1880|Definition')),
    ('1884', '国际子午线会议 Final Act', '七项决议：格林尼治为本初子午线，「世界日」从格林尼治子夜起。', ('meridian-1884', r'gutenberg|Protocols|Final')),
    ('1918', '美国《标准时间法》Standard Time Act', '联邦法律确立时区并实行夏令时。', ('dst-history', r'1918|Standard Time Act|260')),
    ('1966', '美国《统一时间法》Uniform Time Act · 15 U.S.C. §260a', '全国统一夏令时起止日；2005 年能源政策法改为 3 月第二个周日至 11 月第一个周日。', ('this-week', r'260a')),
    ('1967', '第 13 届 CGPM 第 1 号决议', '秒 = 铯-133 基态超精细跃迁 9,192,631,770 个周期。', ('essen-1955', r'1967')),
    ('1986', '国务院关于实行夏时制的通知 / 1992 年暂停', '中国 1986-05-04 起实行、1992 年起暂停。', ('dst-history', r'国务院|gov\.cn|1986')),
    ('2000', '欧盟指令 2000/84/EC', '3 月最后一个周日 01:00 GMT 起、10 月最后一个周日 01:00 GMT 止。', ('this-week', r'2000/84')),
    ('2017', 'GB/T 33661-2017《农历的编算和颁行》', '朔日为初一、冬至所在月为十一月、无中气置闰，以北京时间为准。', ('prc-1949', r'33661|openstd')),
    ('2022', '第 27 届 CGPM 第 4 号决议', '「UT1−UTC 之差的最大值将在 2035 年或之前提高」。', ('cgpm-2022-2026', r'2022')),
    ('2026', '第 28 届 CGPM 第 5 号决议', '连续 UTC 自 2027-05-20 起生效，|UT1−UTC| 上限 3,600 秒。', ('cgpm-2022-2026', r'Resolution 5')),
    ('持续', 'IANA tz 数据库', '各国时区与夏令时规则的代码化，附历史注释；由志愿者维护，通过邮件列表投稿。', ('computer-era', r'iana|tz')),
]
RULE_FALLBACK = {'railway-time': {'url': 'https://www.legislation.gov.uk/ukpga/Vict/43-44/9', 'title': 'legislation.gov.uk'}}
def rules_block():
    li = ''
    for y, t, d, (nid, pat) in RULES:
        s_ = find_src(nid, pat) or RULE_FALLBACK.get(nid)
        li += (f'<article class="ritem fade"><span class="ry">{esc(y)}</span><div><b>{esc(t)}</b><p>{esc(d)}</p>'
               + (f'<a class="rgo" href="{esc(s_["url"])}" target="_blank" rel="noopener">原文 / 入口 ↗</a>' if s_ and s_.get('url') else '') + '</div></article>')
    return f'<div class="rlist">{li}</div>'
def refs_block():
    groups = [('序章 · 对历与对表（十二座城的资料）', [s for c in C['cities'] for s in c.get('sources', [])]),
              ('第一章 · 年与月（两河 / 埃及 / 欧洲 / 希伯来 / 伊斯兰 / 波斯 / 印度 / 全球）', [s for n in A['nodes'] for s in n.get('sources', [])] + [s for r in A['adoption'] for s in r.get('sources', [])]),
              ('第一章 · 年与月（中国与东亚 / 中美洲）', [s for n in B['nodes'] for s in n.get('sources', [])] + [s for f in B['facts'] for s in f.get('sources', [])]),
              ('第二章 · 日与时', [s for n in C['nodes'] for s in n.get('sources', [])] + [s for f in C['facts'] for s in f.get('sources', [])]),
              ('第三章 · 秒', [s for n in D['nodes'] for s in n.get('sources', [])] + [it['source'] for it in D['ladder'] if it.get('source')])]
    out = []
    for g, ss in groups:
        seen, items = set(), []
        for s in ss:
            if isinstance(s, str) and s.startswith('http'): s = {'url': s, 'title': re.sub(r'^https?://(www\.)?', '', s).rstrip('/')}
            if not isinstance(s, dict): continue
            k = s.get('url') or s.get('title')
            if not k or k in seen: continue
            seen.add(k)
            items.append(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>' if s.get('url') else f'<li>{esc(s["title"])}</li>')
        out.append(f'<h3>{esc(g)}（{len(items)}）</h3><ul>{"".join(items)}</ul>')
    return ''.join(out)
USED = []  # 页面上实际出现的图（main() 在拼卷末之前算出）；署名表只列这些
def method_process():
    """v1 的方法条目，按 v2 改两条：图片与程序绘制、上线前核查。"""
    out = []
    for p in E.METHOD['process']:
        if p.startswith('图片 '): p = f'图片 {len(USED)} 张：大都会博物馆 Open Access（CC0）9 张、美国国会图书馆 5 张、Wellcome Collection（Public Domain Mark）3 张、NIST（美国联邦政府作品）2 张、geograph.org.uk（CC BY-SA 2.0）2 张、ESO（CC BY 4.0）、NASA、NOAA/NASA 各 1 张；序章底图用 NASA「蓝色弹珠」，晨昏线、表盘与四张主图由程序绘制，颜色走 CSS 令牌。'
        elif p.startswith('上线前两路子代理'): p = p + '2026 年 10 月 30 日按第 7 题的版面系统重排（v2）后，又由一个子代理按研究底稿与 v1 文案逐条核对新写的短文、标签与主图的算法，改正直接写进 src/editorial2.py 与 src/stage.py。'
        out.append(p)
    return out
def credits():
    rows = ''.join(f'<tr><td>{esc(k)}</td><td>{esc(im["subject"])}</td><td>{esc(im["author_short"])}，{esc(im.get("year", ""))}</td><td>{esc(im["license_short"])}</td><td><a href="{esc(im["url_page"])}" target="_blank" rel="noopener">{esc(im["source_name"])}</a></td></tr>' for k, im in ((k, IM[k]) for k in USED))
    return f'<div class="tblwrap credits"><table><thead><tr><th>编号</th><th>主题</th><th>作者 / 年代</th><th>许可</th><th>出处</th></tr></thead><tbody>{rows}</tbody></table></div>'
def endm():
    M = E.METHOD
    return f'''<footer class="endm" id="end"><div class="wide">
<h2 class="fade">卷末 · 规矩、参考与署名</h2>
<h3 class="endh fade">规矩写在哪<small>{esc(E2.RULES_LEDE)}这一页用到的十三份文件：</small></h3>
{rules_block()}
<details class="fold big fade"><summary><h3>参考（按章分组）</h3></summary><div class="refs">{refs_block()}</div></details>
<details class="fold big fade"><summary><h3>方法</h3></summary><div class="method"><ul>{''.join(f'<li>{p}</li>' for p in method_process())}</ul></div></details>
<details class="fold big fade"><summary><h3>仍待核</h3></summary><div class="method"><ul>{''.join(f'<li>{t}</li>' for t in M['todo'])}</ul></div></details>
<details class="fold big fade"><summary><h3>图片署名（{len(USED)} 张）</h3></summary>{credits()}</details>
<div class="stamp fade">一周一题 · 第 {E.META['no']} 题 · {E.META['date']}<br>研究、绘图与核查：Claude（站长复核）</div>
</div></footer>'''

# ---------- 数据
def data():
    return {'stage': stage.data(C['cities'], IM), 'drift': charts.drift_data(),
            'noon': [dict(id=cid, n=n, lon=lon, tz=tz, r=r) for cid, n, lon, tz, r in E2.NOON_CITIES],
            'ladder': ladder_rungs(), 'deltaT': DELTA_T, 'leaps': LEAPS,
            'lens': {k: {lens: [dict(k=g['k'], label=g['label'], ids=g['ids']) for g in gs] for lens, gs in v.items()} for k, v in LENS.items()}, 'lensName': LENS_NAME,
            'lunar': LUNAR, 'lunarLeap': {y: v[1] for y, v in LUNAR.items()},
            'dstCities': {cid: {'n': n, 'o': o, 'r': r} for cid, n, o, r in DST_CITIES}}

LIGHT = ('--bg:#F4EFE3;--surface:#FBF8F0;--surface-2:#EBE4D3;--ink:#1B1A17;--ink-2:#4A4639;--muted:#6E685A;--line:rgba(27,26,23,.16);--line-2:rgba(27,26,23,.09);--grid:rgba(27,26,23,.05);'
         '--accent:#B8862B;--accent-2:#D9A441;--accent-ink:#8A6318;--wash:rgba(184,134,43,.10);--wash-2:rgba(184,134,43,.2);--nav-glass:rgba(244,239,227,.78);--glass-line:rgba(27,26,23,.12);--dial-face:#FBF8F0;--dial-night:#DDD5C2;color-scheme:light;')

def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    app = open(os.path.join(HERE, 'calendars.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'demos.js'), encoding='utf-8').read()
    light = ('@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){' + LIGHT + '}}\n:root[data-theme="light"]{' + LIGHT + '}')
    pre = hero() + cnav() + '<main>' + tagline_sec() + ch_journey() + ch_year() + ch_day() + ch_second() + '</main>'
    dj = json.dumps(data(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    seen = pre + dj
    USED[:] = [k for k, im in IM.items() if ('assets/' + im['file']) in seen]
    print('images used', len(USED), '/', len(IM), '· unused:', [k for k in IM if k not in USED])
    body = pre + endm()
    page = (tpl.replace('{{TITLE}}', esc(E.META['title'])).replace('{{DESCRIPTION}}', esc(E2.META_DESC)).replace('{{LIGHT_BLOCKS}}', light)
            .replace('{{BODY}}', body).replace('{{DATA_JSON}}', dj).replace('{{APP_JS}}', app))
    page, report = fixes.apply(page)
    for line in report: print(line)
    open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(page)
    meta = {'no': E.META['no'], 'slug': E.META['slug'], 'title': E.META['title'], 'subtitle': E.META['subtitle'], 'date': E.META['date'], 'summary': E2.META_DESC,
            'tags': E.META['tags'], 'format': E2.META_FORMAT, 'cover': 'cover.png', 'cover_focus': E.META['cover_focus'], 'cover_scheme': E.META['cover_scheme'], 'reading_time': E2.META_READING,
            'sources': ['BIPM（第 27、28 届 CGPM 决议、CCTF 主席声明、SI 手册）、IERS 公报 C 72（经 IANA tz 列表转发）、USNO tai-utc.dat 与 deltat.data、NIST、USNO GPS Time Transfer、GPS World',
                        '1884 年国际子午线会议记录（Gutenberg）、英国 1750 与 1880 年法案（legislation.gov.uk）、美国法典 15 U.S.C. §§260–267、EUR-Lex 2000/84/EC、gov.uk、IANA tz 数据库源文件与 theory.html、国务院公报页码、国家授时中心',
                        'Inter gravissimas 英译（Wikisource）、Reingold & Dershowitz《Calendrical Calculations》、Meeus《天文算法》、IANA tz calendars 文件（Grotefend 表）、Toke Nørby 各国改历日期表、香港天文台公历与农历对照表、国家标准全文公开系统（GB/T 33661-2017）、新华社、紫金山天文台、UNESCO、史密森尼 NMAI、Britannica',
                        f'图片 {len(USED)} 张：ESO（CC BY 4.0）、NASA 与 NOAA、美国国会图书馆、大都会博物馆 Open Access（CC0）、NIST、Wellcome Collection、geograph.org.uk（CC BY-SA 2.0）；逐张署名见页面卷末与 src/images.json']}
    json.dump(meta, open(os.path.join(HERE, '..', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote index.html', len(page), 'bytes')

if __name__ == '__main__':
    main()
