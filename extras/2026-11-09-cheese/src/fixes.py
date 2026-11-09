# -*- coding: utf-8 -*-
"""核查（research/check_F.json、check_G.json）之后对研究底稿的改正。
底稿 JSON 不动；构建时在原文里逐条替换再解析，并断言每条恰好命中一次（命中不了就报错，免得改正悄悄失效）。
editorial.py 的条目已直接改在源文件里，这里跳过。SKIP 里列不采纳的条目（按 old 的前 24 个字）。EXTRA 是额外的手工改正。"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {}
EXTRA = []  # (file, old, new)
COUNT = {'n': 0}

def _todo():
    out = []
    for n in ('check_F.json', 'check_G.json'):
        p = os.path.join(HERE, 'research', n)
        if not os.path.exists(p): continue
        for e in json.load(open(p, encoding='utf-8')):
            if 'old' not in e or e.get('file') == 'editorial.py': continue
            if e['old'][:24] in SKIP: continue
            out.append((e['file'], e['old'], e['new']))
    return out + EXTRA

def load(name):
    t = open(os.path.join(HERE, 'research', name), encoding='utf-8').read()
    for f, old, new in _todo():
        if f != name: continue
        n = t.count(old)
        assert n == 1, (name, old[:50], n)
        t = t.replace(old, new); COUNT['n'] += 1
    return json.loads(t)
