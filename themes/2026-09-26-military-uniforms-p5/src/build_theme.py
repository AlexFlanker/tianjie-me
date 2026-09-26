#!/usr/bin/env python3
"""重建第 2 题页面：把 src/ 里的模板、示意图生成器、内容数据、图片元数据与交互脚本内联成 ../index.html

  python3 themes/2026-09-26-military-uniforms-p5/src/build_theme.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'index.html')
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
imgs = json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))
parts = {
    'uniform-fig.js': open(os.path.join(HERE, 'uniform-fig.js'), encoding='utf-8').read(),
    'content.js': open(os.path.join(HERE, 'content.js'), encoding='utf-8').read(),
    'images.js': 'window.UIMAGES = ' + json.dumps(imgs, ensure_ascii=False, separators=(',', ':')) + ';',
    'app.js': open(os.path.join(HERE, 'app.js'), encoding='utf-8').read(),
}
for name, js in parts.items():
    assert '</script' not in js.lower(), name
    key = '/*INLINE:%s*/' % name
    assert key in tpl, key
    tpl = tpl.replace(key, js)
open(OUT, 'w', encoding='utf-8').write(tpl)
print('wrote', os.path.relpath(OUT), f'{len(tpl.encode("utf-8"))/1024:.0f} KB')
