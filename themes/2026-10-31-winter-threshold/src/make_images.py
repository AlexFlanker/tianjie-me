#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并找图底稿（research/images_{1,2,3}.json 三路 + images_4.json v3 补图）→ images.json；核对文件存在、读尺寸；舍弃 status != ok 与 DROP 里的条目。
用法：python3 themes/2026-10-31-winter-threshold/src/make_images.py"""
import json, os, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ASSETS = os.path.join(HERE, '..', 'assets')
DROP = {'img-dia-de-muertos-14'}  # 正脸多的照片不用
def lic_short(s):
    s = s or ''
    if 'CC0' in s: return 'CC0'
    if 'BY-SA' in s: return 'CC BY-SA'
    if re.search(r'CC[ -]BY', s): return 'CC BY'
    if 'No known' in s or 'no known' in s: return '无已知版权限制'
    if 'Public Domain Mark' in s or 'PDM' in s: return '公有领域标记'
    if 'NASA' in s or 'Public Domain' in s or '公有领域' in s or 'PD' in s: return '公有领域'
    return s[:20]
out = []
for k in (1, 2, 3, 4):
    p = os.path.join(HERE, 'research', f'images_{k}.json')
    if not os.path.exists(p): continue
    d = json.load(open(p, encoding='utf-8')); items = d['images'] if isinstance(d, dict) else d
    for i in items:
        if i.get('status') != 'ok' or i['id'] in DROP: continue
        f = os.path.join(ASSETS, i['file'])
        if not os.path.exists(f): print('missing file', i['id'], i['file']); continue
        with Image.open(f) as im: i['width'], i['height'] = im.size
        i['license_short'] = lic_short(i.get('license')); i['route'] = str(k)
        i['author_short'] = re.sub(r'（.*?）', '', i.get('author') or '')[:60]
        out.append(i)
# 舞台底图：NASA 黑色弹珠 3600×1800 → 1920×960
src = os.path.join(ASSETS, 'earth-night-1-full.jpg'); dst = os.path.join(ASSETS, 'earth-night-1920.jpg')
if os.path.exists(src) and not os.path.exists(dst):
    with Image.open(src) as im: im.convert('RGB').resize((1920, 960), Image.LANCZOS).save(dst, 'JPEG', quality=78, optimize=True)
    print('wrote', dst)
json.dump(out, open(os.path.join(HERE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('images.json', len(out), '张；按节点：', sorted(set(i['node'] for i in out)))
