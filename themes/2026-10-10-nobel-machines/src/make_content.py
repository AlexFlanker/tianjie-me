#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 4 题：research/{A,B,C,D}.json + editorial*.py → content.json

  python3 themes/2026-10-10-nobel-machines/src/make_content.py

研究底稿里夹着写给编辑的话（「种子事实」「任务书写……」「本次没有核到」之类），
这里按分句清洗：含内部用语的分句删掉，其余原样保留；清洗前后的对照写到 dist/scrub_report.txt（不进仓库）。
上线前核查后的改正在 fixes.py，最后一步执行。
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editorial as E
import editorial2 as E2

R = {k: json.load(open(os.path.join(HERE, 'research', k + '.json'), encoding='utf-8')) for k in 'ABCD'}

# ------------------------------------------------------------------ 清洗
DROP = re.compile(r'种子(事实|写|里|标|用|的|与|和|口径)|任务书(写|里|说|提到|的|与)|规格(写|里|说|的数字|种子|口径)|选题规格|代理|SCHEMA|编辑|页面(上|如|里|若)|上页面|统稿|画图|同比例示意图缺|size_m|scale_m|drawing|metrics|t_build|t_result|t_idea|见 notes|facts 第|awards')
REPORT = []

def _split(s):
    # 按句号、分号切开，保留分隔符
    parts = re.split(r'(?<=[。；])', s)
    return [p for p in parts if p]

# 个别句子删掉内部用语后会缺主语或缺一方说法，这里先人工改写（左边是底稿原文片段）
FIX = [
    ('停工的起止：种子写 1896–98、约两年。通信录文显示 1895 年已被叫停，1897-02 获准；van Delft 说 1898-06-04 才恢复低温工作、前后 3 年。两年指的是打官司的时间，三年是停工的时间。',
     '停工的起止：通信录文显示 1895 年已被叫停，1897-02 获准；van Delft 说 1898-06-04 才恢复低温工作，前后 3 年。常见的「两年」指的是打官司的时间。'),
    ('种子写约 250 万美元（常见于转引阿尔瓦雷茨诺奖演讲的文献，本轮打不开原文，无法判断是不是含了计算机、厂房或后续改造）。',
     '常见的说法是约 250 万美元（多转引自阿尔瓦雷茨的诺奖演讲，这次打不开原文，无法判断是不是含了计算机、厂房或后续改造）。'),
    ('对 1972（种子与通行说法）。', '对 1972（通行说法）。'),
    ('种子写「一天攒约 3×10^10 个」，这个数在 Di Lella 文中是每天的需求量，在维基百科里也写作每天的产率；',
     '「每天约 3×10^10 个」在 Di Lella 文中是每天的需求量，维基百科写作每天的产率；'),
    ('反质子积累速度：种子与维基百科写每天约 3×10^10 个；Di Lella 把这个数写作每天的需求量；',
     '反质子积累速度：维基百科写每天约 3×10^10 个，Di Lella 把这个数写作每天的需求量；'),
    ('任务书里的「全部约 10,170 处接头」：Rossi 2010 写每处互连 6 个 13 kA 接头、共约 10,000 个，都要加铜分流片；',
     '接头总数：Rossi 2010 写每处互连 6 个 13 kA 接头、共约 10,000 个，都要加铜分流片；常见的'),
    ('隧道年代：种子与维基百科写 1983–88 年；', '隧道年代：维基百科写 1983–88 年（从 LEP 土建开工算起）；'),
    ('规格里的 11,146 是 1996–2001 年的数字；', '11,146 是 1996–2001 年的数字；'),
    ('重水估值：规格写 3.3 亿加元；', '重水估值：常见的说法是 3.3 亿加元；'),
    ('超级神冈的造价没有核到一手数字：规格写约 1 亿美元，任务书写约 104 亿日元；',
     '超级神冈的造价没有核到一手数字：常见的说法是约 1 亿美元或约 104 亿日元；'),
    ('规格写的「臂内约 100 千瓦」是 2015 年首次观测运行时的实际值（出自发现论文正文，本次未直接打开核对）；',
     '常见的「臂内约 100 千瓦」是 2015 年首次观测运行时的实际值（出自发现论文正文，这次没有直接打开核对）；'),
    ('1994 年的预算：规格写「批准时 3.95 亿美元」（维基百科口径）；', '1994 年的预算：维基百科写「批准时 3.95 亿美元」；'),
    ('2015 年首次探测时约 100 千瓦（规格的数字，出自发现论文正文，本次未直接核）。', '2015 年首次探测时约 100 千瓦（出自发现论文正文，这次未直接核）。'),
    ('JUNO 的 20 英寸管数量：新闻稿写「2 万只」，种子事实写 17,612 只（中心探测器口径）。', 'JUNO 的 20 英寸管数量：新闻稿写「2 万只」（含水池），另有 17,612 只的说法（中心探测器口径）。'),
    ('Hyper-K 十年的灵敏度：种子事实写约 6 × 10^34 年，', 'Hyper-K 十年的灵敏度：常见的说法约 6 × 10^34 年，'),
    ('种子事实的「1609 伽利略约 4 厘米」：博物馆藏品的物镜是 51 毫米，年代标为约 1610 年；', '伽利略望远镜的物镜是 51 毫米（博物馆藏品，约 1610 年）；'),
    ('。；只有一个来源，按约定标「中」', '。'),
    ('；只有一个来源，按约定标「中」', ''),
    ('任务书写约 4,100–4,400 米水当量。', ''),
    ('测到的是理论的几分之几：规格写「约三分之一」；', '测到的是理论的几分之几：常说「约三分之一」；'),
    ('事故损失：规格写「约 6,600 只」；', '事故损失：常见的说法是「约 6,600 只」；'),
    ('重新设计前后的质量：任务书与一些二手材料写约 4,990 公斤', '重新设计前后的质量：一些二手材料写约 4,990 公斤'),
    ('设计寿命：种子写 6 个月；', '设计寿命：常见的说法是 6 个月；'),
    ('费米实验室的态度：种子写「费米实验室拒绝」。', '费米实验室的态度：常见的说法是「费米实验室拒绝了提案」。'),
    ('种子写「运行到 1991 年」。', ''),
    ('种子用的是后一种。', ''),
    ('种子用 96 吨。', ''),
    ('种子用的是 96 吨', ''),
    ('规格写 1,200 公里；', '常见的说法是 1,200 公里；'),
    ('规格写约 9,600 只；', '常见的说法是约 9,600 只；'),
    ('规格写约 9,600；', '常见的说法是约 9,600；'),
    ('任务书写 2,092 米；', '另有 2,092 米的说法；'),
    ('种子写「上千根偶极子」不对，上千根的是木桩。', ''),
    ('种子写 1967–69；', '另有 1967–69 年的说法；'),
]

def _label(clause):
    m = re.match(r'^([^：；。，]{2,24}：)', clause)
    return m.group(1) if m else ''

def scrub(s, where=''):
    if not isinstance(s, str) or not s:
        return s
    orig = s
    for a_, b_ in FIX:
        if a_ in s:
            s = s.replace(a_, b_)
    # 先删带内部用语的括号
    s = re.sub(r'（[^（）]*(?:SCHEMA|种子(?:事实|写|里|与)|本环境|按约定)[^（）]*）', '', s)
    s = re.sub(r'[；，]?\s*只有一个来源（[^（）]*），按约定标「中」', '', s)
    if DROP.search(s):
        parts = _split(s); kept = []; lab = ''
        for i, p in enumerate(parts):
            if DROP.search(p):
                if i == 0:
                    lab = _label(p)
                continue
            kept.append(p)
        s = ''.join(kept).strip()
        if lab and s and not _label(s):
            s = lab + s
        s = re.sub(r'[；，、]$', '。', s) if s else s
    s = (s.replace('本轮', '这次').replace('本次', '这次').replace('见 disputes', '见「来源对不上的地方」')
           .replace('disputes', '「来源对不上的地方」').replace('见 todo', '见「没有核到的」').replace('todo', '「没有核到的」'))
    s = re.sub(r'\s+', ' ', s).strip()
    if s != orig:
        REPORT.append((where, orig, s))
    return s

def scrub_list(xs, where=''):
    out = []
    for i, x in enumerate(xs or []):
        y = scrub(x, f'{where}[{i}]')
        if y and len(y) > 3:
            out.append(y)
    return out

def src_list(srcs, where=''):
    out = []
    for s in srcs or []:
        if not isinstance(s, dict):
            continue
        t = scrub(s.get('t', ''), where + '/src') or '来源'
        u = (s.get('u') or '').strip()
        out.append({'t': t, 'u': u if u.startswith('http') else ''})
    return out

def facts_list(fs, where):
    out = []
    for f in fs or []:
        out.append({'n': f.get('n'), 'text': scrub(f.get('text', ''), f'{where}/facts[{f.get("n")}].text'),
                    'confidence': (f.get('confidence') or '中')[:1],
                    'note': scrub(f.get('note', ''), f'{where}/facts[{f.get("n")}].note'),
                    'sources': src_list(f.get('sources'), where)})
    return out

# ------------------------------------------------------------------ 折今价
CPI = R['D']['cpi']
MULT = {int(k): v for k, v in CPI['to_2025_multiplier'].items()}
# 当年年均汇率（每 1 美元合多少该币种）；1978 年瑞士法郎取自 FRED AEXSZUS，其余见底稿 fx
FX = {('USD', None): 1.0, ('CHF', 1978): 1.7907, ('CHF', 2008): 1.0816, ('CAD', 1999): 1.4858}

def usd2025(amount, cur, year):
    rate = 1.0 if cur == 'USD' else FX[(cur, year)]
    return amount / rate * MULT[year]

def zh_money(x, unit='美元'):
    if x >= 1e8:
        v = x / 1e8
        s = f'{v:.0f}' if v >= 20 else f'{v:.1f}'.rstrip('0').rstrip('.')
        return f'{s} 亿{unit}'
    v = x / 1e4
    if v >= 1000:
        return f'{round(v, -2):,.0f} 万{unit}'
    if v >= 100:
        return f'{round(v, -1):,.0f} 万{unit}'
    return f'{v:,.0f} 万{unit}'

CUR = {'USD': '美元', 'CHF': '瑞士法郎', 'CAD': '加元'}

def zh_exact(x, unit):
    if x >= 1e8:
        return f'{x/1e8:.3f}'.rstrip('0').rstrip('.') + f' 亿{unit}'
    return f'{x/1e4:,.0f} 万{unit}'

def cost_block(c, what_none):
    if c is None:
        return {'usd2025': None, 'text': what_none, 'calc': ''}
    items = c if isinstance(c, list) else [c]
    total = 0; parts = []; calc = []
    for amt, cur, year, what in items:
        v = usd2025(amt, cur, year); total += v
        parts.append(f'{zh_exact(amt, CUR[cur])}（{what}）')
        fx = '' if cur == 'USD' else f' ÷ {FX[(cur, year)]}（{year} 年均汇率）'
        calc.append(f'{amt:,.0f} {cur}{fx} × {MULT[year]}（{year}→2025 年 CPI 比值）≈ {v/1e4:,.0f} 万美元')
    if len(items) == 1:
        amt, cur, year, what = items[0]
        approx = f'{zh_exact(amt, CUR[cur])}约合 2025 年的 {zh_money(total)}'
    else:
        approx = '这几笔合计约合 2025 年的 ' + zh_money(total)
    return {'usd2025': round(total), 'text': '；'.join(parts), 'approx': approx, 'usd_text': '约 ' + zh_money(total),
            'calc': '；'.join(calc)}

# ------------------------------------------------------------------ 十二座装置
def find_machine(mid):
    for m in R[E.SRC[mid]]['machines']:
        if m['id'] == mid:
            return m
    raise KeyError(mid)

def person(p):
    zh, en = (p.get('zh') or '').strip(), (p.get('en') or '').strip()
    name = f'{zh}（{en}）' if zh and en else (zh or en)
    return {'name': name, 'r': scrub(p.get('r', ''), 'people')}

KIND = {'著作': '书刊与报道'}   # 这一类里有书、期刊文章，也有媒体报道
SHARE = {'二分之一': '1/2', '四分之一': '1/4', '三分之一': '1/3'}   # 份额写法各卡统一
machines = []
for no, mid in enumerate(E.IDS, 1):
    m = find_machine(mid); o = E.OVR[mid]; w = f'/{mid}'
    pz = m['prize']
    cs = pz.get('citation_source') or {}
    cs_t = cs.get('t', '')
    if 'NobelPrize' in cs_t or 'nobelprize' in (cs.get('u') or ''):
        cs = {'t': '通行文本，未与诺贝尔奖官网逐字核对', 'u': cs.get('u', '')}
    else:
        cs = {'t': scrub(cs_t, w + '/citation_source'), 'u': cs.get('u', '')}
    drop_a = set(o.get('drop_anecdotes', [])); drop_w = set(o.get('drop_awards', []))
    card = {
        'id': mid, 'no': no,
        'prize': {'year': pz['year'],
                  'laureates': [{'zh': l['zh'], 'en': l['en'], 'life': l.get('life', ''), 'share': SHARE.get(l.get('share', ''), l.get('share', '')),
                                 'role': scrub(l.get('role', ''), w + '/role')} for l in pz['laureates']],
                  'citation_en': pz['citation_en'], 'citation_zh': pz['citation_zh'], 'citation_src': cs},
        'name': m['apparatus']['zh'], 'name_en': m['apparatus']['en'],
        'short': o['short'], 'laur': o['laur'], 'era': o['era'], 'place': o['place'],
        'place_full': scrub(m['apparatus'].get('place_zh', ''), w + '/place'),
        'sites': [{'name': n, 'lat': la, 'lon': lo} for n, la, lo in o['sites']],
        'tag': o['tag'],
        'claim': scrub(m['claim'], w + '/claim'),
        'brief': scrub_list(m['brief'], w + '/brief'),
        'scale': [{'k': s['k'], 'v': scrub(s['v'], w + '/scale.v'), 'note': scrub(s.get('note', ''), w + '/scale.note')} for s in m['scale']],
        'approach': scrub_list(m['approach'], w + '/approach'),
        'history': [{'d': h['d'], 't': scrub(h['t'], w + '/history').rstrip('。')} for h in m['history']],
        'people': [person(p) for p in m.get('people', [])],
        'awards': [a for i, a in enumerate(scrub_list(m.get('awards', []), w + '/awards')) if i not in drop_w],
        'anecdotes': [{'t': scrub(a['t'], w + '/anecdote'), 'kind': KIND.get(a.get('kind', ''), a.get('kind', ''))}
                      for i, a in enumerate(m.get('anecdotes', [])) if i not in drop_a],
        'lesson': {k: scrub(v, w + '/lesson') for k, v in m['lesson'].items()},
        'criteria': m.get('criteria', []),
        'criteria_note': scrub(m.get('criteria_note', ''), w + '/criteria_note'),
        'lineage': scrub(m.get('lineage', ''), w + '/lineage'),
        'tool': o['tool'], 'shape': o.get('shape'),
        'cost': cost_block(o.get('cost'), o.get('cost_what', '')),
        'facts': facts_list(m.get('facts'), w),
        'disputes': scrub_list(m.get('disputes', []), w + '/disputes'),
        'todo': scrub_list(m.get('todo', []), w + '/todo'),
    }
    if o.get('cost_note') and card['cost'].get('approx'):
        card['cost']['approx'] += o['cost_note']
    if o.get('cost_what') and card['cost']['usd2025'] is None:
        card['cost']['text'] = o['cost_what']
    if mid == 'lhc':
        c = m['counter']
        card['counter'] = {'name': c['name'], 'summary': scrub(c['summary'], w + '/counter'),
                           'numbers': [{'k': x['k'], 'v': scrub(x['v'], w + '/counter.n')} for x in c['numbers']],
                           'why': [re.sub(r'［[^］]*］$', '', scrub(x, w + '/counter.why')).strip() for x in c['why']],
                           'contrast': [re.sub(r'［[^］]*］$', '', scrub(x, w + '/counter.contrast')).strip() for x in c['contrast']]}
    if mid == 'superk-sno':
        card['tool_alt'] = {'size_m': 12, 'size_what': 'SNO 亚克力球直径', 'mass_t': 1000, 'mass_what': 'SNO 的重水', 'depth_m': 2070}
    t = card['tool']
    t['wait'] = t['t_prize'] - t['t_result']; t['span'] = t['t_prize'] - t['t_idea']
    machines.append(card)

# ------------------------------------------------------------------ 候补席
bench_all = {}
for k in 'ABC':
    for b in R[k]['bench']:
        bench_all[b['id']] = b

def bench_card(b):
    return {'id': b['id'], 'year': b['year'], 'who': b['who_zh'], 'who_en': b.get('who_en', ''),
            'what': scrub(b['what'], 'bench'), 'line': scrub(b['line'], 'bench/line'), 'number': scrub(b['number'], 'bench/number'),
            'lesson': scrub(b['lesson'], 'bench/lesson'), 'confidence': (b.get('confidence') or '中')[:1],
            'sources': src_list(b.get('sources'), 'bench')}

bench = [bench_card(bench_all[i]) for i in E2.BENCH_ORDER]
rontgen = bench_card(bench_all['rontgen-1901'])
rontgen['citation_en'] = bench_all['rontgen-1901']['citation_en']
rontgen['citation_zh'] = bench_all['rontgen-1901']['citation_zh']

# ------------------------------------------------------------------ 旁表
engineers = []
for e in R['A']['sidebars']['engineers']:
    engineers.append({'year': e['year'], 'zh': e['zh'], 'en': e['en'], 'for': scrub(e['for'], 'eng'), 'why': scrub(e['why'], 'eng/why'),
                      'confidence': (e.get('confidence') or '中')[:1], 'sources': src_list(e.get('sources'), 'eng')})
for e in engineers:
    if '达伦' in e['zh']:
        e['confidence'] = '中'   # 与候补席短卡的置信度一致
bt = []
for b in R['B']['sidebars']['team']['breakthrough']:
    if b['year'] in (2018, 2026):
        continue
    bt.append({'year': b['year'], 'what': scrub(b['what'], 'bt'), 'people': b.get('people'), 'money': scrub(b.get('money', ''), 'bt/money'),
               'sources': src_list(b.get('sources'), 'bt')})

# ------------------------------------------------------------------ 展望
D = R['D']
topics = []
for t in D['topics']:
    if t['id'] in E2.TOPIC_DROP:
        continue
    w = '/D/' + t['id']
    wh = t.get('when') or {}
    topics.append({
        'id': t['id'], 'tier': t['tier'], 'feasibility': t.get('feasibility'),
        'topic': t['topic'], 'question': scrub(t.get('question', ''), w), 'theory': scrub(t.get('theory', ''), w + '/theory'),
        'target': scrub(t.get('target', ''), w + '/target'), 'engineering': scrub(t.get('engineering', ''), w + '/eng'),
        'projects': [{'name': p['name'], 'where': p.get('where', ''), 'china': bool(p.get('china')), 'status': p.get('status', ''),
                      'key': scrub(p.get('key', ''), w + '/proj.key'), 'dates': scrub(p.get('dates', ''), w + '/proj.dates'),
                      'cost': scrub(p.get('cost', ''), w + '/proj.cost'), 'sources': src_list(p.get('sources'), w)}
                     for p in t.get('projects', [])],
        'when': {'earliest': wh.get('earliest'), 'likely': wh.get('likely'), 'latest': wh.get('latest'),
                 'kind': wh.get('kind', ''), 'basis': scrub(wh.get('basis', ''), w + '/basis')},
        'scale_m': t.get('scale_m'), 'scale_what': scrub(t.get('scale_what', ''), w + '/scale_what'),
        'universe': scrub(t.get('universe', ''), w + '/universe'),
        'feasibility_note': scrub(t.get('feasibility_note', ''), w + '/feas_note'),
        'facts': facts_list(t.get('facts'), w),
        'disputes': scrub_list(t.get('disputes', []), w + '/disputes'),
        'todo': scrub_list(t.get('todo', []), w + '/todo'),
    })

laws = []
for l in D['laws']:
    pts = [{'year': p['year'], 'value': p['value'], 'unit': p.get('unit', ''),
            'label': re.sub(r'（[^（）]*(?:种子|未核|本次)[^（）]*）', '', p.get('label', '')).strip()} for p in l['points']]
    laws.append({'id': l['id'], 'name': l['name'], 'summary': scrub(l['summary'], 'law'), 'points': pts,
                 'note': scrub(l.get('note', ''), 'law/note'), 'confidence': (l.get('confidence') or '中')[:1],
                 'sources': src_list(l.get('sources'), 'law')})

delays = [{'project': x['project'], 'planned': scrub(x.get('planned', ''), 'delay'), 'actual': scrub(x.get('actual', ''), 'delay'),
           'slip_years': x.get('slip_years'), 'cost_planned': scrub(x.get('cost_planned', ''), 'delay'),
           'cost_actual': scrub(x.get('cost_actual', ''), 'delay'), 'note': scrub(x.get('note', ''), 'delay/note'),
           'confidence': (x.get('confidence') or '中')[:1], 'sources': src_list(x.get('sources'), 'delay')} for x in D['delays']]

ladder = [{'scale_m': x['scale_m'], 'label': x['label'], 'example': scrub(x['example'], 'ladder'),
           'topic_ids': x.get('topic_ids', [])} for x in D['ladder']]
china = [{'name': x['name'], 'what': scrub(x['what'], 'china'), 'status': scrub(x['status'], 'china'), 'key': scrub(x.get('key', ''), 'china/key'),
          'confidence': (x.get('confidence') or '中')[:1], 'topic_ids': x.get('topic_ids', []), 'sources': src_list(x.get('sources'), 'china')} for x in D['china']]
universe = [{'id': x['id'], 'what': x['what'], 'line': scrub(x['line'], 'universe'), 'number': scrub(x.get('number', ''), 'universe'),
             'confidence': (x.get('confidence') or '中')[:1], 'sources': src_list(x.get('sources'), 'universe')} for x in D['universe_lab']]

# ------------------------------------------------------------------ 参考（按组去重）
def uniq(srcs):
    seen = set(); out = []
    for s in srcs:
        key = s['u'] or s['t']
        if key in seen or not s['t']:
            continue
        seen.add(key); out.append(s)
    return out

refs = []
for c in machines:
    ss = [c['prize']['citation_src']] + [s for f in c['facts'] for s in f['sources']]
    refs.append({'group': f"{c['prize']['year']} {c['short']}", 'items': uniq(ss)})
refs.append({'group': '候补席与旁表', 'items': uniq([s for b in [rontgen] + bench for s in b['sources']] +
                                                [s for e in engineers for s in e['sources']] + [s for b in bt for s in b['sources']])})
refs.append({'group': '下一批任务书', 'items': uniq([s for t in topics for f in t['facts'] for s in f['sources']] +
                                                [s for t in topics for p in t['projects'] for s in p['sources']] +
                                                [s for x in laws + delays + china + universe for s in x['sources']])})

content = {
    'meta': E.META, 'chapters': E.CHAPTERS, 'criteria': E.CRITERIA,
    'ch1': E.CH1, 'ch2': E.CH2, 'machines': machines, 'extra_shapes': E.EXTRA_SHAPES,
    'ch3': E2.CH3, 'principles': E2.PRINCIPLES, 'ssc': E2.SSC,
    'ch4': E2.CH4, 'rontgen': rontgen, 'bench': bench, 'engineers': engineers, 'breakthrough': bt,
    'ch5': E2.CH5, 'topics': topics, 'laws': laws, 'delays': delays, 'delays_summary': D.get('delays_summary', {}),
    'ladder': ladder, 'china': china, 'universe': universe,
    'cpi': {'what': scrub(CPI['what'], 'cpi'), 'mult': CPI['to_2025_multiplier']},
    'refs': refs, 'main_sources': E2.MAIN_SOURCES, 'method': E2.METHOD, 'todo': E2.TODO, 'stamp': E2.STAMP,
}

# ------------------------------------------------------------------ 事实核查后的改正（fixes.py）
import fixes
for coll in (machines, topics):
    for c in coll:
        extra = fixes.ADD_FACTS.get(c['id'], [])
        n0 = max([f['n'] for f in c['facts'] if isinstance(f.get('n'), int)] or [0])
        have = {}
        for f0 in c['facts'] + c.get('projects', []):
            for s0 in f0['sources']:
                have.setdefault(s0['t'], s0)
        for i, f in enumerate(extra, 1):
            srcs = list(f.get('sources', []))
            for kw in f.get('src', []):
                hit = [v for t, v in have.items() if kw in t]
                if hit:
                    srcs.append(hit[0])
                else:
                    print('  ADD_FACTS: no source matches', c['id'], kw)
            c['facts'].append({'n': n0 + i, 'text': f['text'], 'confidence': f.get('confidence', '中')[:1],
                               'note': f.get('note', ''), 'sources': srcs})
        c['todo'] = c['todo'] + fixes.ADD_TODO.get(c['id'], [])
for mid, frag, new_d in fixes.HIST:
    c = next(x for x in machines if x['id'] == mid)
    hits = [h for h in c['history'] if frag in h['t']]
    if len(hits) != 1:
        print('  HIST: expected 1 match, got', len(hits), mid, frag)
    for h in hits:
        h['d'] = new_d
for lid, year, frag, new_v, new_label in fixes.LAWPT:
    l = next(x for x in laws if x['id'] == lid)
    hits = [p for p in l['points'] if p['year'] == year and frag in p['label']]
    if len(hits) != 1:
        print('  LAWPT: expected 1 match, got', len(hits), lid, year, frag)
    for p in hits:
        if new_v is not None:
            p['value'] = new_v
        if new_label is not None:
            p['label'] = new_label
for tid, upd in fixes.WHEN.items():
    t = next(x for x in topics if x['id'] == tid)
    t['when'].update(upd)
for tid, frag, field, val in fixes.PROJ:
    t = next(x for x in topics if x['id'] == tid)
    hits = [p for p in t['projects'] if frag in p['name']]
    if len(hits) != 1:
        print('  PROJ: expected 1 match, got', len(hits), tid, frag)
    for p in hits:
        p[field] = val
for l in laws:
    for p in l['points']:
        # 分组连线：Livingston 图里束流能量与质心能量分开；引力波图里太空与脉冲星计时阵不和地面干涉仪连线
        if l['id'] == 'livingston':
            p['s'] = 'cm' if '质心' in p.get('unit', '') else 'beam'
        elif l['id'] == 'gw-arm':
            p['s'] = None if p['value'] >= 1e8 else 'ground'
        else:
            p['s'] = 'all'
    if l['id'] in fixes.LAW_ADD:
        l['summary'] = l['summary'].rstrip() + fixes.LAW_ADD[l['id']]
for mid, frag, new_kind in fixes.ANEC_KIND:
    c = next(x for x in machines if x['id'] == mid)
    hits = [a for a in c['anecdotes'] if frag in a['t']]
    if len(hits) != 1:
        print('  ANEC_KIND: expected 1 match, got', len(hits), mid, frag)
    for a in hits:
        a['kind'] = new_kind
HIT = [0] * len(fixes.POST)
PROC = re.compile(r'这次(?=没|未|打不开|只核到|都打不开|均未)')   # 工作过程用语：「这次未核」→「未核」
def post(x):
    if isinstance(x, str):
        x = PROC.sub('', x)
        for i, (a_, b_) in enumerate(fixes.POST):
            if a_ in x:
                x = x.replace(a_, b_); HIT[i] += 1
        return x.strip() if x != x.strip() else x
    if isinstance(x, list):
        out = [post(v) for v in x]
        return [v for v in out if not (v == '' or (isinstance(v, dict) and (v.get('t') == '' or v.get('text') == '')))]
    if isinstance(x, dict):
        return {k: post(v) for k, v in x.items()}
    return x
content = post(content)
MISS = [fixes.POST[i][0] for i, n in enumerate(HIT) if n == 0]

# ------------------------------------------------------------------ 自检：页面上不该出现的内部用语
LEFT = re.compile(r'种子(事实|写|里|标|用|的|与|和|口径)|SCHEMA|代理|统稿|上页面|本环境|请编辑|编辑复核|本轮|本次|按约定')
bad = []
def walk(x, path):
    if isinstance(x, str):
        if LEFT.search(x):
            bad.append((path, x[:120]))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, f'{path}[{i}]')
    elif isinstance(x, dict):
        for k, v in x.items():
            walk(v, f'{path}/{k}')
walk(content, '')

out = os.path.join(HERE, 'content.json')
json.dump(content, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
with open(os.path.join(HERE, 'dist', 'scrub_report.txt'), 'w', encoding='utf-8') as f:
    for w, a, b in REPORT:
        f.write(f'## {w}\n- {a}\n+ {b}\n\n')
print('wrote', out, os.path.getsize(out) // 1024, 'KB;', len(machines), 'machines,', len(bench), 'bench,', len(topics), 'topics;',
      'scrubbed', len(REPORT), 'strings; leftover jargon:', len(bad))
for p, x in bad[:40]:
    print('  LEFT', p, '|', x)
print('fixes:', len(fixes.POST), 'entries,', len(MISS), 'missed')
for a_ in MISS:
    print('  MISS', a_[:70])
