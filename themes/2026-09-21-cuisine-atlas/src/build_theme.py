#!/usr/bin/env python3
"""把 src/ 下的模板、内容数据、地图数据和配色拼装成单文件网页。

  python3 src/build_theme.py              # 生成本主题的 index.html（完整 HTML 文档）
  python3 src/build_theme.py --artifact   # 生成 src/dist/artifact.html（Claude Artifact 版，不含骨架）

改内容只需编辑 src/content/*.js，然后重新运行本脚本。
"""
import json, os, sys

SRC = os.path.dirname(os.path.abspath(__file__))      # themes/<theme>/src
ROOT = os.path.dirname(SRC)                              # themes/<theme>
SITE_URL = 'https://tianjie.me/t/cuisine-atlas/'
TITLE = '中国菜系演化图谱'
DESC = '以食材、器具、技法、口味四条线索，把先秦到当代十个时期的中国饮食变迁映射到今天的 34 个省级行政区：交互地图、时间轴与各地菜系沿革。'

tpl = open(os.path.join(SRC, 'template.html'), encoding='utf-8').read()
content = ''.join(open(os.path.join(SRC, 'content', f), encoding='utf-8').read() + '\n'
                  for f in ['c_meta.js', 'c_p1.js', 'c_p2.js', 'c_p3.js', 'c_modern.js'])
pal = json.load(open(os.path.join(SRC, 'palette.json')))
spec = json.load(open(os.path.join(SRC, 'palette_spec.json')))
mp = json.load(open(os.path.join(SRC, 'map_data.json')))

# 南海诸岛的小岛点抽稀，避免插图里堆成一团
ded = []
for x, y in mp['islands']:
    if all(abs(x - a) > 5 or abs(y - b) > 5 for a, b in ded):
        ded.append((x, y))
mp['islands'] = [[x, y] for x, y in ded]

def css_vars(mode):
    return ''.join(f'--{k}:{v};' for k, v in pal[mode].items())

# 填色较深（OKLCH L < 0.58）时省名用浅色字
meta = {'light': {}, 'dark': {}}
for mode in ('light', 'dark'):
    for group in ('fam', 'taste', 'staple'):
        for k, (h, c, l) in spec[group][mode].items():
            if l < 0.58:
                meta[mode][f'{group}-{k}'] = True

page = (tpl.replace('/*PALETTE_LIGHT*/', css_vars('light'))
           .replace('/*PALETTE_DARK*/', css_vars('dark'))
           .replace('/*DATA*/', content)
           .replace('/*MAP*/', 'const MAP = ' + json.dumps(mp, ensure_ascii=False, separators=(',', ':')) + ';')
           .replace('/*PALMETA*/', 'const PALMETA = ' + json.dumps(meta, separators=(',', ':')) + ';'))

artifact_mode = '--artifact' in sys.argv

if artifact_mode:
    out = page.replace('<!--THEME_TOGGLE-->', '').replace('/*THEME_TOGGLE_JS*/', '')
    dst = os.path.join(SRC, 'dist', 'artifact.html')
else:
    # 拆出模板头部（title / 字体 link / style）与正文，组装成完整 HTML 文档
    head_end = page.index('</style>') + len('</style>')
    head_part, body_part = page[:head_end], page[head_end:]
    title_line = f'<title>{TITLE}</title>'
    font_link = [l for l in head_part.splitlines() if l.startswith('<link rel="stylesheet"')][0]
    style_block = head_part.replace(title_line, '').replace(font_link, '').strip()
    font_href = font_link.split('href="')[1].split('"')[0]

    toggle_html = '<button class="theme-btn" id="themebtn" type="button" aria-label="切换深浅色">◐ 深浅色</button>'
    toggle_js = """
  (function(){ const root=document.documentElement, btn=$('#themebtn'); if(!btn) return;
    const label=()=>{ const t=root.getAttribute('data-theme'); btn.textContent = t==='dark' ? '☀ 浅色' : t==='light' ? '☾ 深色' : '◐ 深浅色'; };
    btn.addEventListener('click',()=>{ const dark = root.getAttribute('data-theme')==='dark' || (!root.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
      root.setAttribute('data-theme', dark ? 'light' : 'dark'); try{ localStorage.setItem('cuisine-theme', root.getAttribute('data-theme')); }catch(e){} label(); });
    label(); })();"""
    body_part = body_part.replace('<!--THEME_TOGGLE-->', toggle_html).replace('/*THEME_TOGGLE_JS*/', toggle_js)

    favicon = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%23b5432c'/%3E"
               "%3Ctext x='32' y='44' font-size='34' text-anchor='middle' font-family='Noto Serif SC,Songti SC,serif' font-weight='900' fill='%23fff'%3E味%3C/text%3E%3C/svg%3E")
    head = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title_line}
<meta name="description" content="{DESC}">
<meta name="author" content="Tianjie Sun">
<meta name="theme-color" content="#f3f4ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16181b" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{SITE_URL}">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:locale" content="zh_CN">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{favicon}">
<script>try{{var t=localStorage.getItem('cuisine-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{font_href}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{font_href}"></noscript>
<style>
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
{style_block}
</head>
<body>
"""
    out = head + body_part.lstrip('\n') + "\n</body>\n</html>\n"
    dst = os.path.join(ROOT, 'index.html')

os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, 'w', encoding='utf-8').write(out)
print('wrote', os.path.relpath(dst, ROOT), f'{len(out.encode("utf-8"))/1024:.0f} KB')
