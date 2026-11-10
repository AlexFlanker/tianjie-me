# -*- coding: utf-8 -*-
"""把 editorial2.IMG 里选定的图从暂存区拷进 assets/，并生成 src/images.json（完整授权信息）。
用法：python3 src/make_images.py <暂存区 stage 目录>   暂存区不在时不必重跑：assets/ 与 images.json 已入库。"""
import sys, os, json, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__)); THEME = os.path.dirname(HERE); A = os.path.join(THEME, 'assets')
sys.path.insert(0, HERE)
from editorial2 import IMG
from PIL import Image
stage = sys.argv[1]
st = {}
for r in ('D1', 'D2'):
    for x in json.load(open(os.path.join(stage, r, 'images.json'), encoding='utf-8')): st[(r, x['id'])] = x
old_meta = json.load(open(os.path.join(HERE, 'images_v1.json'), encoding='utf-8'))
PDM = 'https://creativecommons.org/publicdomain/mark/1.0/'
LIC = {  # 许可简称 → 规范名
    'CC0': 'CC0 1.0', 'PD': 'Public Domain', 'Public domain': 'Public Domain'}
OLD = {  # 首发版沿用图：作者 / 年份按首发版图注口径
    'n01': ('Augusthaiho', '2018（摄）'), 'n02': ('Windmemories', '2023（摄）'), 'n03': ('BabelStone', '2011（摄）'), 'n04': ('佚名（西魏）', '535–557'),
    'n05': ('佚名（中唐）', '781–848'), 'n06': ('佚名（宋）', '宋'), 'n07': ('佚名（元）', '1324'), 'n08': ('佚名（明）', '明'), 'n09': ('不详', '1945'),
    'n10': ('Roger & Renate Rössing / Deutsche Fotothek', '1953'), 'n11': ('慕尼黑啤酒', '2015（摄）'), 'deck-hgd': ('MNXANL', '2018（摄）')}
out = []
for iid, e in IMG.items():
    src = e['src']
    if src[0] == 'old':
        fn = src[1]; key = fn[:-4]; m = old_meta[key]
        lic = m['license']; url = m['license_link'] or PDM
        if lic.startswith('Public domain'): lic = 'Public Domain'
        if not url.endswith('/') and 'creativecommons.org' in url and not url.endswith('deed.en'): url += '/'
        author = m['author']; inst = 'Wikimedia Commons'; year = re.sub(r',.*', '', m['date']); page = m['page']
        author, year = OLD[key]
        w, h = Image.open(os.path.join(A, fn)).size
    else:
        r, sid, size = src; m = st[(r, sid)]
        fn = '%s-%d.jpg' % (sid, size); sp = os.path.join(stage, r, 'out', fn)
        if not os.path.exists(os.path.join(A, fn)): shutil.copy(sp, os.path.join(A, fn))
        w, h = Image.open(os.path.join(A, fn)).size
        lic = m['license_short']; lic = LIC.get(lic, lic); url = m['license_url']
        if 'loc.gov' in url or 'commons.wikimedia.org/wiki/File' in url: url = PDM; lic = 'Public Domain'
        author = m.get('author_short') or m['author']; inst = m['inst']; year = str(m['year']); page = m['source_url']
        if '雪候鹰座' in author or author == '陈文': author = '陈文（雪候鹰座）'
        inst = re.sub(r'（NARA.*', '（NARA）', inst); inst = inst.replace(' Prints & Photographs Division', '')
    assert url.startswith('https://') and page.startswith('http'), iid
    out.append(dict(id=iid, file='assets/' + fn, w=w, h=h, title=e['title'], cap=e['cap'], author=author, inst=inst, year=year, lic=lic, licUrl=url, page=page))
json.dump(out, open(os.path.join(HERE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
used = {os.path.basename(x['file']) for x in out}
for f in os.listdir(A):
    if f not in used: os.remove(os.path.join(A, f)); print('removed', f)
print(len(out), 'images', sum(os.path.getsize(os.path.join(A, f)) for f in used) // 1024, 'KB')
