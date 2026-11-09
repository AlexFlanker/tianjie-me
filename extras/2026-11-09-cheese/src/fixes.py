# -*- coding: utf-8 -*-
"""核查（research/check_F.json、check_G.json）之后对研究底稿的改正。
底稿 JSON 不动；构建时逐条在字符串里替换，并断言每条恰好命中一次（命中不了就报错，免得改正悄悄失效）。
editorial.py 的条目直接改在源文件里，这里跳过。SKIP 里列不采纳的条目（按 old 的前 24 个字）及理由。"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {}
EXTRA = []  # 额外手工改正：(file, old, new)

def _walk(o, old, new, hits):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and old in v:
                hits.append(1); o[k] = v.replace(old, new)
            elif isinstance(v, (dict, list)): _walk(v, old, new, hits)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str) and old in v:
                hits.append(1); o[i] = v.replace(old, new)
            elif isinstance(v, (dict, list)): _walk(v, old, new, hits)

def apply(A, B, C, D):
    M = {'hist_A.json': A, 'craft_B.json': B, 'world_C.json': C, 'counter_D.json': D}
    todo = []
    for n in ('check_F.json', 'check_G.json'):
        p = os.path.join(HERE, 'research', n)
        if not os.path.exists(p): continue
        for e in json.load(open(p, encoding='utf-8')):
            if 'old' not in e or e.get('file') not in M: continue
            if e['old'][:24] in SKIP: continue
            todo.append((e['file'], e['old'], e['new']))
    todo += EXTRA
    for f, old, new in todo:
        hits = []; _walk(M[f], old, new, hits)
        assert len(hits) == 1, (f, old[:40], len(hits))
    return len(todo)
