#!/usr/bin/env python3
"""给主题生成 1200×630 封面（也用作 OG 分享图）。在作者环境运行（需要 playwright + chromium），不在 Pages 构建里跑。

  python3 tools/cover.py themes/2026-09-21-cuisine-atlas            # 输出 themes/.../cover.png
  python3 tools/cover.py themes/<dir> --focus ".map-wrap" --scheme light

meta.json 里可以写 "cover_focus": "<css selector>"（截图前把该元素滚到视口中央）和 "cover_scheme": "light|dark"。
页面里给元素加 data-cover-hide 属性（比如深浅色切换按钮），截图时会隐藏。
"""
import sys, os, json, argparse
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(); ap.add_argument('theme_dir'); ap.add_argument('--focus'); ap.add_argument('--scheme'); ap.add_argument('--out')
a = ap.parse_args()
d = os.path.abspath(a.theme_dir)
meta = json.load(open(os.path.join(d, 'meta.json'), encoding='utf-8')) if os.path.exists(os.path.join(d, 'meta.json')) else {}
focus = a.focus or meta.get('cover_focus'); scheme = a.scheme or meta.get('cover_scheme', 'light'); out = a.out or os.path.join(d, 'cover.png')
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1200, 'height': 630}, device_scale_factor=1, color_scheme=scheme)
    pg = ctx.new_page(); pg.goto('file://' + os.path.join(d, 'index.html')); pg.wait_for_timeout(1800)
    pg.add_style_tag(content='[data-cover-hide]{display:none !important}')  # 主题页里标了 data-cover-hide 的元素（如深浅色按钮）不进封面
    if focus:
        pg.evaluate("sel => { const el = document.querySelector(sel); if (el) el.scrollIntoView({block:'center'}); }", focus); pg.wait_for_timeout(500)
    pg.screenshot(path=out); b.close()
print('wrote', os.path.relpath(out))
