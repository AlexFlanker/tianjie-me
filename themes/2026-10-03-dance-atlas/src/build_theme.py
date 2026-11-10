#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 3 题《舞从劳作来》v2 构建：content.json（事实）+ editorial2.py（新写的字与图片清单）+ images.json（授权）→ ../index.html
  python3 src/build_theme.py
事实一律来自 content.json；本脚本只排版，不改字。构建时做：图片存在性、授权字段、占位符、禁用词、命中断言。"""
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__)); THEME = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import editorial2 as E

def rd(n): return open(os.path.join(HERE, n), encoding='utf-8').read()
_c = rd('content.json')
for _a, _b in E.FIXES:
    _a, _b = json.dumps(_a, ensure_ascii=False)[1:-1], json.dumps(_b, ensure_ascii=False)[1:-1]
    assert _c.count(_a) == 1, ('FIXES 命中次数', _a, _c.count(_a)); _c = _c.replace(_a, _b)
C = json.loads(_c); MAP = json.loads(rd('map_data.json')); META = json.load(open(os.path.join(THEME, 'meta.json'), encoding='utf-8'))
IMGS = {x['id']: x for x in json.loads(rd('images.json'))}
esc = lambda s: html.escape(str(s), quote=True)

# ---------- 小工具 ----------
URL_RE = re.compile(r'https?://[^\s，；。）」、]+')
def dom(u):
    m = re.match(r'https?://([^/]+)', u); return m.group(1).replace('www.', '') if m else u
def linkify(s):
    """来源串里的裸 URL → 以域名为字的链接。"""
    out, last = [], 0
    for m in URL_RE.finditer(s):
        out.append(esc(s[last:m.start()])); u = m.group(0)
        out.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(u), esc(dom(u)))); last = m.end()
    out.append(esc(s[last:])); return ''.join(out)
def conf(c, cls=''):
    k, t = E.CONF[c]; return '<span class="conf %s %s" title="置信度：%s">置信 %s</span>' % (k, cls, t, t)
used_imgs = []
def credit(im): return '%s · %s · <a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(im['author']), esc(im['inst']), esc(im['licUrl']), esc(im['lic']))
def fig(iid, cls='', eager=False, sizes=None):
    im = IMGS[iid]; used_imgs.append(iid)
    return ('<figure class="%s"><img src="%s" width="%d" height="%d" alt="%s"%s decoding="async"><figcaption><b>%s</b>%s<span class="cr">%s</span></figcaption></figure>'
            % (cls, esc(im['file']), im['w'], im['h'], esc(im['title']), '' if eager else ' loading="lazy"', esc(im['title']), esc(im['cap']), credit(im)))
def kv(pairs):
    return '<dl class="kv">' + ''.join('<dt>%s</dt><dd>%s</dd>' % (esc(k), v) for k, v in pairs if v) + '</dl>'
def row(rid, cls, head, body):
    return ('<div class="lrow" data-id="%s" id="n-%s"><button class="lhead" type="button" aria-expanded="false">%s<span class="lchev" aria-hidden="true"></span></button>'
            '<div class="lmore"><div class="lmore-in">%s</div></div></div>' % (rid, rid, head, body))
def lensbar(key, lenses, first):
    b = ''.join('<button type="button" role="tab" data-lens="%s" aria-selected="%s">%s</button>' % (k, 'true' if k == first else 'false', esc(v)) for k, v in lenses)
    return '<div class="lensbar"><span class="lensk">分组</span><div class="lens" id="lens-%s" role="tablist">%s</div><span class="lensnote" id="lensnote-%s"></span></div>' % (key, b, key)
def groups_html(key, groups, rows_by_id):
    s = ''
    for g in groups:
        s += '<div class="lgh" data-g="%s"><b>%s</b><small>%d 条</small></div>' % (esc(g['k']), esc(g['label']), len(g['ids']))
        s += ''.join(rows_by_id[i] for i in g['ids'])
    return s
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3v10M4 9l4 4 4-4"/></svg>'

# ---------- 数据整理 ----------
nodes = C['nodes']; decks = C['decks']
def why_of(n):
    v = [it['v'] for it in n['items'] if it['k'] == '为什么是它']
    assert len(v) == 1, n['id']; return v[0]
def lead_of(n):
    s = n['summary']; i = s.find('为什么是它：'); return s[:i].strip()
moves = []
for d in decks:
    for m in d['moves']:
        mid = 'm%02d' % (len(moves) + 1); moves.append(dict(m, id=mid, deck=d['name'], dkey=d['key']))
assert len(moves) == 14 and len(nodes) == 12 and len(C['works']) == 18 and len(C['quick']) == 10
works = [dict(w, id='w%02d' % (i + 1)) for i, w in enumerate(C['works'])]
quick = [dict(q, id='q%02d' % (i + 1)) for i, q in enumerate(C['quick'])]
def qcat(q):
    e = q['ethnic']
    return 'aca' if '当代' in e else 'han' if e.startswith('汉族') else 'eth'

LENS = {
    'moves': {
        'deck': [dict(k=d['key'], label=d['name'], ids=[m['id'] for m in moves if m['dkey'] == d['key']]) for d in decks],
        'conf': [dict(k=c, label='置信度 ' + c, ids=[m['id'] for m in moves if m['confidence'] == c]) for c in '高中低'],
    },
    'nodes': {
        'era': [dict(k='e%d' % i, label=lab, ids=ids) for i, (lab, ids) in enumerate(E.NODES['era_groups'])],
        'spread': [dict(k='s%d' % i, label=lab, ids=[n['id'] for n in nodes if lo <= len(n['map']['highlight']) <= hi]) for i, (lab, lo, hi) in enumerate(E.NODES['spread_groups'])],
    },
    'works': {
        'genre': [dict(k='g%d' % i, label=g, ids=[w['id'] for w in works if w['genre'] == g]) for i, g in enumerate(dict.fromkeys(w['genre'] for w in works))],
        'conf': [dict(k=c, label='置信度 ' + c, ids=[w['id'] for w in works if w['confidence'] == c]) for c in '高中低'],
    },
}
for key in LENS:
    for ln in LENS[key]:
        LENS[key][ln] = [g for g in LENS[key][ln] if g['ids']]
        n_all = {'moves': 14, 'nodes': 12, 'works': 18}[key]
        assert sum(len(g['ids']) for g in LENS[key][ln]) == n_all, (key, ln)
LENSNAME = {'moves': {'deck': '舞种', 'conf': '置信度'}, 'nodes': E.NODES['lens'], 'works': E.WATCH['lens']}

# ---------- 卷首 ----------
H = E.HERO
proof = H['proof'].format(N_NODES=len(nodes), N_MOVES=len(moves), N_WORKS=len(works), N_IMG=len(IMGS))
B = []
B.append('<header class="hero" id="top"><div class="wide"><div><div class="mast rise"><span>%s</span><span>%s</span></div><h1 class="rise">%s</h1><p class="hsub rise">%s</p><p class="hth rise">%s</p>'
         '<div class="hact rise"><a class="btn" href="#stage">%s%s</a><span class="hproof">%s</span></div></div>%s</div></header>'
         % (esc(H['mast'][0]), esc(H['mast'][1]), esc(H['h1']), esc(H['sub']), esc(H['th']), esc(H['btn']), ARROW, esc(proof), fig(H['img'], 'hfig rise', eager=True)))
tl = ''
for ln in E.TAGLINE:
    tl += '<span class="ln">' + ''.join('<span class="w%s">%s</span>' % (' k' if w.startswith('*') else '', esc(w.lstrip('*'))) for w in ln) + '</span>'
assert ''.join(w.lstrip('*') for ln in E.TAGLINE for w in ln) == C['thesis'], '论点须与 content.json 的 thesis 一字不差'
B.append('<section class="tagsec" id="tagsec" aria-label="论点"><div class="tagstick"><div class="wide"><p class="tagl">%s</p><p class="tagrest">%s</p></div></div></section>' % (tl, esc(E.TAGREST)))
B.append('<nav class="cnav" id="cnav" aria-label="章节"><div class="row">%s<button class="ntheme" id="theme-btn" type="button"></button><span class="prog" id="prog"></span></div></nav>'
         % ''.join('<a href="#%s" data-nav="%s"><small>%s</small>%s</a>' % (i, i, esc(no), esc(t)) for i, no, t in E.NAV))

# ---------- 序章 ----------
S = E.STAGE
stage_nodes = []
for n in nodes:
    iid = E.NODE_IMGS[n['id']][0]; im = IMGS[iid]; used_imgs.append(iid)
    stage_nodes.append(dict(id=n['id'], era=n['era'], years=n['years'], title=n['title'], layer=n['map']['layer'], why=why_of(n), tick=S['ticks'][n['id']],
                            img=im['file'], cap='%s · %s' % (im['title'], im['author']), hi=n['map']['highlight'], route=n['map'].get('route', []), labels=n['map'].get('labels', [])))
    for c in n['map']['highlight']: assert c in MAP['prov'] and c != 'TW', (n['id'], c)
ticks = ''.join('<span class="rtick%s" data-i="%d" style="left:calc(var(--gut) + 20px + (100%% - 2 * var(--gut) - 40px) * %.4f)"><i></i><b>%s</b></span>'
                % (' last' if i == len(nodes) - 1 else '', i, i / (len(nodes) - 1), esc(sn['tick'])) for i, sn in enumerate(stage_nodes))
B.append('<section class="stage" id="stage" aria-label="序章"><div class="stpin" id="stpin"><div class="ststage" id="ststage"><div class="stin">'
         '<div class="stmap"><div class="stk">%s<span>%s</span></div><div id="stmap" class="map" style="height:100%%;display:flex;align-items:center;justify-content:center;width:100%%"></div></div>'
         '<div class="stside" id="stside"><div class="stcard" aria-live="polite"><div class="stera"><b id="stera"></b><span id="styears"></span></div><h3 class="sttitle" id="sttitle"></h3><p class="stlayer" id="stlayer"></p><p class="stwhy" id="stwhy"></p><p class="stcap" id="stcap"></p>'
         '<button class="sbtn" id="stopen" type="button">%s</button></div></div>'
         '<div class="struler" id="struler" role="slider" tabindex="0" aria-label="时代" aria-valuemin="0" aria-valuemax="%d" aria-valuenow="0"><span class="rtrack"></span>%s<span class="rknob" id="stknob"></span></div>'
         '</div></div></div></section>' % (esc(S['k']), esc(S['hint']), esc(S['open']), len(nodes) - 1, ticks))

def chead(key):
    c = E.CH[key]; im = IMGS[c['img']]; used_imgs.append(c['img'])
    return ('<div class="chead"><div class="plate"><div class="ptext"><p class="cno">%s</p><h2>%s</h2><p class="lede">%s</p></div>%s</div></div>'
            % (c['no'], esc(c['h2']), esc(c['lede']), fig(c['img'], 'pimg')))

# ---------- 01 这一回的梗 ----------
M = E.MEME; L = M['labels']
evs = ''.join('<article class="ev"><div class="d">%s</div><p>%s</p><p class="src"><a href="%s" target="_blank" rel="noopener">%s</a></p></article>' % (esc(e['d']), esc(e['t']), esc(e['u']), esc(e['s'])) for e in C['meme']['events'])
pair = ''.join('<article class="pcard"><div class="k">%s</div><h3>%s</h3><div class="what">%s</div><p>%s</p><p>%s</p><blockquote>%s</blockquote></article>'
               % (esc(p['heritage']), esc(p['who']), esc(p['what']), esc(p['role']), esc(p['material']), esc(p['quote'])) for p in C['meme']['pair'])
figmoves = [m for m in moves if m.get('fig')]
assert [m['fig'] for m in figmoves] == ['shan', 'langzi', 'dou']
tabs = ''.join('<button class="sbtn" type="button" data-move="%s" aria-pressed="%s">%s</button>' % (m['id'], 'true' if i == 0 else 'false', esc(m['name'])) for i, m in enumerate(figmoves))
marks = ''.join('<button class="sbtn" type="button" data-mark="%s">%s</button>' % (k, esc(v)) for k, v in M['lab_marks'].items())
lab = ('<div class="lab"><div><div class="labtabs" id="labtabs" role="group" aria-label="选动作">%s</div>'
       '<div class="labstage paper" id="labstage"><svg id="labsvg" viewBox="0 0 260 300" role="img" aria-label="墨线小人示范动作"></svg><span class="labt" id="labt"></span></div>'
       '<div class="labscrub"><input type="range" id="labscrub" min="0" max="1000" value="0" aria-label="逐帧"></div>'
       '<div class="labctl"><button class="sbtn" type="button" id="labplay" aria-pressed="true">%s</button><span class="k">%s</span><span class="grp" id="labspeed">'
       '<button class="sbtn" type="button" data-sp="1" aria-pressed="true">1×</button><button class="sbtn" type="button" data-sp="0.5" aria-pressed="false">½</button><button class="sbtn" type="button" data-sp="0.25" aria-pressed="false">¼</button></span>'
       '<span class="k" id="labmarksk">%s</span><span class="grp" id="labmarks">%s</span></div></div>'
       '<div class="labcard" id="labcard" aria-live="polite"></div></div>' % (tabs, esc(M['lab_pause']), esc(M['lab_speed']), esc(M['lab_marks_k']), marks))
labor = '<div class="labor">' + ''.join(fig(i) for i in E.LABOR_IMGS) + '</div>'
# 动作行
mrows = {}
for m in moves:
    th = ('<span class="thumb paper"><svg viewBox="0 0 260 300" data-thumb="%s" aria-hidden="true"></svg></span>' % m['fig']) if m.get('fig') else '<span class="thumb" aria-hidden="true">—</span>'
    cue = m['cue'] if m['cue'] not in ('——', '—', '') else ''
    head = '%s<span class="lname"><b>%s</b><small>%s</small></span><span class="lcol">%s</span><span class="lconf">%s</span>' % (th, esc(m['name']), esc(cue or m['deck']), esc(m['life'] if len(m['life']) <= 44 else m['scene']), conf(m['confidence']))
    see = ('<ul>' + ''.join('<li>%s</li>' % esc(x) for x in m['see']) + '</ul>') if m['see'] else ''
    body = kv([(L['cue'], esc(cue)), (L['how'], esc(m['how'])), (L['life'], esc(m['life'])), (L['role'], esc(m['role'])), (L['scene'], esc(m['scene'])), (L['risk'], esc(m['risk'])), (L['see'], see)])
    body += '<p class="src">%s　%s</p>' % (conf(m['confidence']), linkify(m['source']))
    if m.get('fig'): body += '<div class="lacts"><button class="sbtn" type="button" data-tolab="%s">%s</button></div>' % (m['id'], esc(M['tolab']))
    mrows[m['id']] = row(m['id'], 'mv', head, body)
def deckmeta(d):
    s = '<p><b>名录</b>　%s</p><p><b>流布</b>　%s</p>' % (esc(d['heritage']), esc(d['region']))
    t = d['teacher']; s += '<p><b>教材</b>　%s：%s</p><p class="src">%s</p>' % (esc(t['name']), esc(t['material']), linkify(t['source']))
    for key, lab in (('roles', '角色'), ('scenes', '场景')):
        s += '<h4>%s</h4>' % lab + ''.join('<p><b>%s</b>　%s %s</p>' % (esc(x['name']), esc(x['desc']), conf(x['confidence'])) for x in d[key])
    s += '<h4>流派与地域</h4>' + ''.join('<p><b>%s</b>　%s%s %s</p>' % (esc(x['name']), (esc(x['founder']) + '。') if x.get('founder') and x['founder'] != '——' else '', esc(x['trait']), conf(x['confidence'])) for x in d['schools'])
    s += '<h4>传承人</h4>' + ''.join('<p><b>%s</b>　%s %s</p>' % (esc(x['name']), esc(x['note']), conf(x['confidence'])) for x in d['inheritors'])
    s += '<h4>来源</h4><ul class="refs">' + ''.join('<li>%s</li>' % linkify(x) for x in d['sources']) + '</ul>'
    chips = '<div class="chips">' + ''.join('<span class="chip">%s</span>' % esc(x) for x in d['names_only']) + '</div>'
    return ('<details class="fold"><summary><h3>%s</h3><span class="small">%s</span></summary><div class="deckmeta">%s</div></details>'
            '<p class="small" style="margin:16px 0 0">%s · %s（%d 个）</p>%s' % (esc(d['name']), esc(M['deck_more']), s, esc(d['name']), esc(M['names_k']), len(d['names_only']), chips))
all_names = [m['name'] for m in moves] + [x for d in decks for x in d['names_only']]
B.append('<main><section class="chap" id="meme"><div class="wide">' + chead('meme')
         + '<div class="sec"><div class="sech"><h3>%s</h3><span class="small">%s</span></div><div class="evs" id="evs">%s</div></div>' % (esc(M['ev_h']), esc(M['ev_note']), evs)
         + '<div class="sec"><div class="sech"><h3>%s</h3></div><div class="pair">%s</div></div>' % (esc(M['pair_h']), pair)
         + '<div class="sec" id="lab"><div class="sech"><h3>%s</h3><span class="small">%s</span></div>%s</div>' % (esc(M['lab_h']), esc(M['lab_note']), lab)
         + '<div class="sec"><div class="sech"><h3>%s</h3><span class="small">%s</span></div>%s</div>' % (esc(M['labor_h']), esc(M['labor_note']), labor)
         + '<div class="sec" id="moves"><div class="sech"><h3>%s</h3><span class="small">%s</span></div>' % (esc(M['moves_h']), esc(M['moves_note']))
         + '<div class="finder"><input id="finder-in" list="finder-list" type="search" placeholder="%s" aria-label="%s"><datalist id="finder-list">%s</datalist><button class="sbtn" type="button" id="finder-go">%s</button><button class="sbtn" type="button" id="finder-rand">%s</button></div><p class="finderout" id="finder-out" aria-live="polite"></p>'
           % (esc(M['finder_ph']), esc(M['finder_h']), ''.join('<option value="%s">' % esc(x) for x in all_names), esc(M['finder_go']), esc(M['finder_rand']))
         + lensbar('moves', [('deck', '舞种'), ('conf', '置信度')], 'deck') + '<div class="lgrid mv" id="lgrid-moves">%s</div>' % groups_html('moves', LENS['moves']['deck'], mrows)
         + ''.join(deckmeta(d) for d in decks) + '</div></div></section>')

# ---------- 02 十二个节点 ----------
N = E.NODES
nrows = {}
for n in nodes:
    head = '<span class="lyear">%s</span><span class="lname"><b>%s</b><small>%s</small></span><span class="lcol">%s</span><span class="lconf">%s</span>' % (esc(n['years']), esc(n['title']), esc(n['era']), esc(n['map']['layer']), conf(n['confidence']))
    items = kv([(it['k'], esc(it['v'])) for it in n['items'] if not (it['k'] == '为什么是它' and '为什么是它：' in n['summary'])])
    q = n.get('quote'); qh = '<blockquote class="lquote">%s<small>%s</small></blockquote>' % (esc(q['text']), esc(q['who'])) if q else ''
    def fli(f): return '<li>%s<div class="src">%s<a href="%s" target="_blank" rel="noopener">%s</a></div></li>' % (esc(f['text']), conf(f['confidence']), esc(f['url']), esc(f['source']))
    fs = n['facts']; top, rest = fs[:3], fs[3:]
    facts = '<h4>%s</h4><ul class="facts">%s</ul>' % (esc(N['facts_k']), ''.join(fli(f) for f in top))
    if rest: facts += '<details class="fold"><summary>%s</summary><ul class="facts">%s</ul></details>' % (esc(N['more_facts'].format(n=len(rest))), ''.join(fli(f) for f in rest))
    left = '<div><p class="ltext">%s</p>%s%s%s<div class="lacts"><button class="sbtn" type="button" data-tomap="%s">%s</button></div></div>' % (esc(n['summary']), qh, items, facts, n['id'], esc(N['tomap']))
    right = '<div class="figs">%s</div>' % ''.join(fig(i) for i in E.NODE_IMGS[n['id']])
    nrows[n['id']] = row(n['id'], 'nd', head, '<div class="lbody">%s%s</div>' % (left, right))
B.append('<section class="chap" id="nodes"><div class="wide">' + chead('nodes') + lensbar('nodes', list(N['lens'].items()), 'era')
         + '<div class="lgrid nd" id="lgrid-nodes">%s</div></div></section>' % groups_html('nodes', LENS['nodes']['era'], nrows))

# ---------- 03 去哪儿看 ----------
W = E.WATCH; WL = W['labels']
qrows = {}
for q in quick:
    ims = E.QUICK_IMGS[q['genre']]
    th = '<span class="qth">%s</span>' % (('<img src="%s" alt="" loading="lazy" decoding="async">' % esc(IMGS[ims[0]]['file'])) if ims else '—')
    head = '%s<span class="lname"><b>%s</b><small>%s</small></span><span class="lcol">%s</span>' % (th, esc(q['genre']), esc(q['region']), esc(q['motif'] if len(q['motif']) <= 60 else q['motif'][:q['motif'].find('：')] if 0 < q['motif'].find('：') <= 60 else q['props']))
    wl = '<ul>' + ''.join('<li>%s　%s%s %s%s</li>' % (esc(w['title']), esc(w['who']), ('，' + esc(w['year'])) if w.get('year') else '', conf(w['confidence']),
                                                    (' <a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(w['link']), esc(dom(w['link'])))) if w.get('link') else '') for w in q['works']) + '</ul>'
    left = '<div>' + kv([(WL['ethnic'], esc(q['ethnic'])), (WL['region'], esc(q['region'])), (WL['motif'], esc(q['motif'])), (WL['props'], esc(q['props'])), (WL['watch'], esc(q['watch'])), (WL['works'], wl)]) + '<p class="src">%s</p></div>' % linkify(q['source'])
    right = ('<div class="figs">%s</div>' % ''.join(fig(i) for i in ims)) if ims else '<p class="small">%s</p>' % esc(W['noimg'])
    qrows[q['id']] = row(q['id'], 'qk', head, '<div class="lbody">%s%s</div>' % (left, right))
qgroups = [dict(k=k, label=lab, ids=[q['id'] for q in quick if qcat(q) == k]) for lab, k in W['quick_groups']]
assert sum(len(g['ids']) for g in qgroups) == 10 and all(g['ids'] for g in qgroups)
wrows = {}
for w in works:
    yshort = re.split(r'[（(]', w['year'])[0].strip()
    head = '<span class="lg lcol">%s</span><span class="lname"><b>%s</b><small>%s</small></span><span class="lcol y">%s</span><span class="lconf">%s</span>' % (esc(w['genre']), esc(w['work']), esc(w['combo']), esc(yshort), conf(w['confidence']))
    link = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(w['link']), esc(dom(w['link']))) if w['link'] else ''
    body = kv([(WL['combo'], esc(w['combo'])), (WL['troupe'], esc(w['troupe'])), (WL['year'], esc(w['year'])), (WL['where'], esc(w['where'])), (WL['look'], esc(w['look'])), (WL['link'], link)]) + '<p class="src">%s　%s</p>' % (conf(w['confidence']), linkify(w['source']))
    wrows[w['id']] = row(w['id'], 'wk', head, body)
B.append('<section class="chap" id="watch"><div class="wide">' + chead('watch')
         + '<div class="sec"><div class="sech"><h3>%s</h3><span class="small">%s</span></div><div class="lgrid qk" id="lgrid-quick">%s</div></div>' % (esc(W['quick_h']), esc(W['quick_note']), groups_html('quick', qgroups, qrows))
         + '<div class="sec"><div class="sech"><h3>%s</h3></div>%s<div class="lgrid wk" id="lgrid-works">%s</div></div>' % (esc(W['works_h']), lensbar('works', list(W['lens'].items()), 'genre'), groups_html('works', LENS['works']['genre'], wrows))
         + '</div></section></main>')

# ---------- 卷末 ----------
X = E.END
def fold(h, inner, note=''): return '<details class="fold"><summary><h3>%s</h3>%s</summary><div>%s</div></details>' % (esc(h), ('<span class="small">%s</span>' % esc(note)) if note else '', inner)
refs = ''
for chap, items in C['refs'].items():
    seen = set(); lis = ''
    for r in items:
        key = (r['t'], r.get('u'))
        if key in seen: continue
        seen.add(key); lis += '<li>%s</li>' % (('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(r['u']), esc(r['t']))) if r.get('u') else esc(r['t']))
    refs += '<h4>%s</h4><ol class="refs">%s</ol>' % (esc(chap), lis)
order = list(dict.fromkeys(used_imgs))
assert set(order) == set(IMGS), ('图片清单与页面用图不一致', set(IMGS) ^ set(order))
cred = '<p class="small">%s</p><div class="tblwrap"><table class="credits"><thead><tr><th>图</th><th>作者</th><th>机构 / 来源</th><th>年份</th><th>许可</th><th>来源页</th></tr></thead><tbody>' % esc(X['credits_note'].format(n=len(order)))
for iid in order:
    im = IMGS[iid]
    cred += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s<br><a href="%s" target="_blank" rel="noopener">%s</a></td><td><a href="%s" target="_blank" rel="noopener">%s</a></td></tr>' % (
        esc(im['title']), esc(im['author']), esc(im['inst']), esc(im['year']), esc(im['lic']), esc(im['licUrl']), esc(im['licUrl']), esc(im['page']), esc(dom(im['page'])))
cred += '</tbody></table></div>'
B.append('<footer class="endm" id="end"><div class="wide"><h2>%s</h2><p class="small">%s</p>' % (esc(X['h2']), esc(X['v2_note']))
         + fold(X['why_h'], ''.join('<p>%s</p>' % esc(p) for p in C['why']['paras']))
         + fold(X['method_h'], '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in C['method']['items']))
         + fold(X['todo_h'], '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in C['method']['todo']))
         + fold(X['refs_h'], refs) + fold(X['credits_h'], cred)
         + '<div class="stamp">%s</div></div></footer>' % esc(X['stamp']))

# ---------- 数据（给 app.js） ----------
DATA = dict(
    map=dict(w=MAP['w'], h=MAP['h'], jd=MAP['jd'], islands=MAP['islands'], inset=MAP['inset'], note=S['note'],
             prov={c: dict(d=p['d'], c=p['c']) for c, p in MAP['prov'].items()}),  # 不带省名：页面只画形状，文字标注全部来自各节点的 labels
    stage=stage_nodes, lens=LENS, lensName=LENSNAME,
    moves=[dict(id=m['id'], name=m['name'], deck=m['deck'], fig=m.get('fig'), cue=m['cue'] if m['cue'] not in ('——', '—') else '', how=m['how'], life=m['life'], risk=m['risk']) for m in moves],
    nameOnly=[dict(name=x, deck=d['name']) for d in decks for x in d['names_only']],
    t=dict(play=M['lab_play'], pause=M['lab_pause'], open=M['lab_open'], nameonly=M['finder_nameonly'], none=M['finder_none'], labels={k: L[k] for k in ('how', 'life', 'risk')}),
)
body = '\n'.join(B)
fig_js = rd('dance-fig.js')
assert 'drawAt' in fig_js, 'dance-fig.js 需带 v2 加的 drawAt / T'
out = rd('template.html')
for k, v in (('{{TITLE}}', esc(META['title'])), ('{{DESCRIPTION}}', esc(META['summary'])), ('{{BODY}}', body),
             ('{{DATA_JSON}}', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')), ('{{FIG_JS}}', fig_js), ('{{APP_JS}}', rd('app.js'))):
    assert k in out, k; out = out.replace(k, v)

# ---------- 检查 ----------
def audit(doc):
    errs = []
    for bad in ('台湾', '臺灣', 'Taiwan', '台北', '{{', '{N_', 'TODO', 'FIXME', 'lorem', '占位', '车、表、球', '吃喝玩乐', '>None<', '>undefined<'):
        if bad in doc: errs.append('禁用 / 泄漏：' + bad)
    for m in re.finditer(r'(?:src|href)="(assets/[^"]+)"', doc):
        if not os.path.exists(os.path.join(THEME, m.group(1))): errs.append('缺图：' + m.group(1))
    for im in IMGS.values():
        for f in ('author', 'inst', 'year', 'lic', 'licUrl', 'page', 'title', 'cap'):
            if not im.get(f): errs.append('授权字段空：%s.%s' % (im['id'], f))
        if not im['licUrl'].startswith('https://creativecommons.org/'): errs.append('许可 URL 非 CC / PDM：' + im['id'])
    for f in os.listdir(os.path.join(THEME, 'assets')):
        if ('assets/' + f) not in doc: errs.append('assets 里有没用到的文件：' + f)
    if 'fonts.googleapis.com/css2?family=Noto+Serif+SC' not in doc: errs.append('字体')
    for must in ('id="lgrid-moves"', 'id="lgrid-nodes"', 'id="lgrid-works"', 'id="lgrid-quick"', 'id="stpin"', 'id="labsvg"', 'class="credits"'):
        if doc.count(must) != 1: errs.append('命中次数不为 1：' + must)
    if doc.count('class="lrow"') != 14 + 12 + 18 + 10: errs.append('行数不对：%d' % doc.count('class="lrow"'))
    return errs
errs = audit(out)
if errs:
    print('\n'.join(errs)); sys.exit(1)
open(os.path.join(THEME, 'index.html'), 'w', encoding='utf-8').write(out)
text = re.sub(r'<(script|style)[\s\S]*?</\1>', '', out); text = re.sub(r'<[^>]+>', '', text)
print('index.html %d KB · 可见文字约 %d 字 · 图 %d 张 · assets %d KB' % (len(out.encode()) // 1024, len(re.sub(r'\s+', '', text)), len(order),
      sum(os.path.getsize(os.path.join(THEME, 'assets', f)) for f in os.listdir(os.path.join(THEME, 'assets'))) // 1024))
