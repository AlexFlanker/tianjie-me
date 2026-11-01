# -*- coding: utf-8 -*-
"""把 raw_img/ 里选中的原图压成页面用的 assets/img/*.jpg，并写 images.json（署名、许可、来源）。
CHOICE：页面槽位 key → (images_D.json 里的 id, 中文说明, 英文说明[, 最长边])。raw_img/ 不进仓库。"""
import json, os, glob
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'assets', 'img')
D = {x['id']: x for x in json.load(open(os.path.join(HERE, 'research', 'images_D.json'), encoding='utf-8'))}
from choice import CHOICE, MOBILE, CONTAIN

def rawfile(i):
    x = D[i]; f = x.get('file') or ''
    p = os.path.join(HERE, f) if f and os.path.exists(os.path.join(HERE, f)) else None
    if not p:
        c = glob.glob(os.path.join(HERE, 'raw_img', i + '*'))
        p = c[0] if c else None
    return p

def save(i, name, edge):
    p = rawfile(i)
    if not p: print('  ! 缺原图', i); return None
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    im.thumbnail((edge, edge), Image.LANCZOS)
    dst = os.path.join(OUT, name + '.jpg'); im.save(dst, 'JPEG', quality=76, optimize=True, progressive=True)
    return 'assets/img/' + name + '.jpg', im.size

os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*.jpg')): os.remove(f)
out, done = [], {}
for key, v in CHOICE.items():
    i, zh, en = v[0], v[1], v[2]; edge = v[3] if len(v) > 3 else 1800
    if i not in D: print('  ! 不在 images_D', key, i); continue
    if i in done and done[i][1] >= edge: rel, size = done[i][0], done[i][2]
    else:
        r = save(i, i, edge)
        if not r: continue
        rel, size = r; done[i] = (rel, edge, size)
    x = D[i]
    rec = dict(key=key, id=i, file=rel, w=size[0], h=size[1], zh=zh, en=en, author=x.get('author') or '—', license=x.get('license'), license_url=x.get('license_url'), page=x.get('source_page') or x.get('download_url'), title=x.get('title'))
    if key in CONTAIN: rec['fit'] = 'contain'
    out.append(rec)
    if key in MOBILE:
        mi = MOBILE[key]; r = save(mi, mi + '-m', 1200)
        if r:
            rec['mobile'] = r[0]; m = D[mi]
            out.append(dict(key=key + '-mobile', id=mi, file=r[0], w=r[1][0], h=r[1][1], zh=m.get('desc_zh') or m.get('title'), en=m.get('desc_en') or m.get('title'), author=m.get('author') or '—', license=m.get('license'), license_url=m.get('license_url'), page=m.get('source_page') or m.get('download_url'), title=m.get('title')))
json.dump(out, open(os.path.join(HERE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(f) for f in glob.glob(os.path.join(OUT, '*.jpg')))
print(f'{len(out)} 个槽位，{len(glob.glob(os.path.join(OUT, "*.jpg")))} 个文件，{tot/1e6:.1f} MB')
