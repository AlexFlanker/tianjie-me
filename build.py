#!/usr/bin/env python3
"""一周一题 · tianjie.me 站点构建脚本（纯标准库，Cloudflare Pages 构建环境可直接运行）

  python3 build.py            # 生成 public/

输入：
  themes/<YYYY-MM-DD>-<slug>/index.html   每期主题的自包含单页
  themes/<YYYY-MM-DD>-<slug>/meta.json    标题、日期、摘要、标签、封面等
  themes/<YYYY-MM-DD>-<slug>/cover.png    1200×630 封面（tools/cover.py 生成）
  hub/home.html                           首页模板
  hub/site.json                           站点信息与长期专题
输出：
  public/index.html            首页：本周主题 + 归档
  public/t/<slug>/index.html   每期主题（注入统一顶栏）
  public/t/<slug>/cover.png    封面 / OG 图
  public/feed.xml  sitemap.xml  robots.txt  404.html  _headers  _redirects
"""
import json, os, re, shutil, html, datetime as dt

ROOT = os.path.dirname(os.path.abspath(__file__))
THEMES = os.path.join(ROOT, 'themes')
HUB = os.path.join(ROOT, 'hub')
OUT = os.path.join(ROOT, 'public')
site = json.load(open(os.path.join(HUB, 'site.json'), encoding='utf-8'))
BASE = site['url'].rstrip('/')

def esc(s): return html.escape(str(s), quote=True)

# ---------- 读取主题 ----------
themes = []
for d in sorted(os.listdir(THEMES)):
    p = os.path.join(THEMES, d)
    if not os.path.isdir(p) or not re.match(r'^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$', d): continue
    if not os.path.exists(os.path.join(p, 'index.html')) or not os.path.exists(os.path.join(p, 'meta.json')): continue
    m = json.load(open(os.path.join(p, 'meta.json'), encoding='utf-8'))
    m.setdefault('slug', d[11:]); m.setdefault('date', d[:10]); m.setdefault('tags', []); m.setdefault('format', '')
    m['dir'] = p; m['url'] = f"/t/{m['slug']}/"
    if m.get('draft'): continue
    themes.append(m)
themes.sort(key=lambda m: (m['date'], m.get('no', 0)))
for i, m in enumerate(themes): m.setdefault('no', i + 1)
latest = themes[-1] if themes else None

# ---------- 输出目录 ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 't'))

# ---------- 顶栏（注入每期页面） ----------
BAR_CSS = """<style id="yzyt-bar-css">
.yzyt-bar{--yb:#f5f5f2;--yi:#1a1c1a;--y2:#5b5f5a;--yl:#d9dbd5;--ya:#b5432c;font:13px/1.4 "Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:var(--yb);color:var(--y2);border-bottom:1px solid var(--yl);padding:8px clamp(16px,3vw,36px);display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:space-between}
.yzyt-bar a{color:var(--yi);text-decoration:none}.yzyt-bar a:hover{color:var(--ya)}
.yzyt-bar .brand{font-family:"Noto Serif SC","Songti SC",serif;font-weight:900;letter-spacing:.12em;color:var(--yi)}
.yzyt-bar .brand b{display:inline-block;background:var(--ya);color:#fff;font-size:11px;letter-spacing:.1em;padding:1px 6px;border-radius:2px;margin-left:8px;vertical-align:1px;font-family:"Noto Sans SC",sans-serif;font-weight:500}
.yzyt-bar .lhs{display:flex;gap:14px;align-items:center}.yzyt-bar .dt{color:var(--y2)}
.yzyt-bar .nav{display:flex;gap:16px;align-items:center}.yzyt-bar .nav span{color:var(--yl)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .yzyt-bar{--yb:#141618;--yi:#ecebe4;--y2:#a9aca6;--yl:#2b2f33;--ya:#e2694f}}
:root[data-theme="dark"] .yzyt-bar{--yb:#141618;--yi:#ecebe4;--y2:#a9aca6;--yl:#2b2f33;--ya:#e2694f}
</style>"""

def bar_html(m, prev_m, next_m):
    left = f'<div class="lhs"><a class="brand" href="/">{esc(site["name"])}<b>第 {m["no"]} 题</b></a><span class="dt">{esc(m["date"])}</span></div>'
    nav = []
    nav.append(f'<a href="{prev_m["url"]}" title="{esc(prev_m["title"])}">← 上一题</a>' if prev_m else '<span>← 上一题</span>')
    nav.append('<a href="/#archive">归档</a>')
    nav.append(f'<a href="{next_m["url"]}" title="{esc(next_m["title"])}">下一题 →</a>' if next_m else '<span>下一题 →</span>')
    return f'{BAR_CSS}\n<div class="yzyt-bar" role="navigation" aria-label="一周一题">{left}<div class="nav">{"".join(nav)}</div></div>\n'

def inject(page, m, prev_m, next_m):
    bar = bar_html(m, prev_m, next_m)
    # 注入到 <body> 之后；顺带加 feed 链接与 OG 图
    page = re.sub(r'(<body[^>]*>)', lambda mm: mm.group(1) + '\n' + bar, page, count=1)
    head_extra = (f'<link rel="alternate" type="application/atom+xml" title="{esc(site["name"])}" href="/feed.xml">\n'
                  f'<meta property="og:image" content="{BASE}{m["url"]}cover.png">\n<meta name="twitter:card" content="summary_large_image">\n')
    if 'og:image' not in page:
        page = page.replace('</head>', head_extra + '</head>', 1)
    page = page.replace('<meta name="twitter:card" content="summary">', '')
    return page

for i, m in enumerate(themes):
    prev_m = themes[i - 1] if i > 0 else None
    next_m = themes[i + 1] if i + 1 < len(themes) else None
    dst = os.path.join(OUT, 't', m['slug']); os.makedirs(dst)
    page = open(os.path.join(m['dir'], 'index.html'), encoding='utf-8').read()
    open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8').write(inject(page, m, prev_m, next_m))
    for extra in ('cover.png', 'assets'):
        src = os.path.join(m['dir'], extra)
        if os.path.isdir(src): shutil.copytree(src, os.path.join(dst, extra))
        elif os.path.exists(src): shutil.copy(src, dst)
    m['has_cover'] = os.path.exists(os.path.join(m['dir'], 'cover.png'))

# ---------- 首页 ----------
tpl = open(os.path.join(HUB, 'home.html'), encoding='utf-8').read()
WEEKDAY = '一二三四五六日'
def nice_date(s):
    d = dt.date.fromisoformat(s); return f"{d.year} 年 {d.month} 月 {d.day} 日 · 周{WEEKDAY[d.weekday()]}"

def card(m):
    cover = f'<img src="{m["url"]}cover.png" alt="" loading="lazy">' if m['has_cover'] else '<div class="nocover"></div>'
    tags = ''.join(f'<span>{esc(t)}</span>' for t in m['tags'])
    return (f'<a class="card" href="{m["url"]}"><div class="cv">{cover}</div><div class="cb"><div class="no">第 {m["no"]} 题 <time datetime="{m["date"]}">{esc(m["date"])}</time></div>'
            f'<h3>{esc(m["title"])}</h3><p>{esc(m.get("subtitle") or m.get("summary",""))}</p><div class="tags">{tags}{"<i>"+esc(m["format"])+"</i>" if m["format"] else ""}</div></div></a>')

hero = ''
if latest:
    cover = f'<img src="{latest["url"]}cover.png" alt="{esc(latest["title"])}">' if latest['has_cover'] else ''
    hero = (f'<section class="hero"><div class="hero-cv">{cover}</div><div class="hero-tx"><div class="kicker">本周 · 第 {latest["no"]} 题 · {nice_date(latest["date"])}</div>'
            f'<h2><a href="{latest["url"]}">{esc(latest["title"])}</a></h2>'
            f'{"<div class=sub>"+esc(latest["subtitle"])+"</div>" if latest.get("subtitle") else ""}<p>{esc(latest.get("summary",""))}</p>'
            f'<div class="cta"><a class="btn" href="{latest["url"]}">打开这一题 →</a>{"<span class=meta>"+esc(latest["reading_time"])+"</span>" if latest.get("reading_time") else ""}</div></div></section>')
archive = ''.join(card(m) for m in reversed(themes))
projects = ''.join(f'<a class="proj" href="{esc(p["url"])}"><b>{esc(p["title"])}</b><span>{esc(p["desc"])}</span></a>' for p in site.get('projects', []))
home = (tpl.replace('{{SITE_NAME}}', esc(site['name'])).replace('{{TAGLINE}}', esc(site['tagline'])).replace('{{ABOUT}}', site['about'])
           .replace('{{HERO}}', hero).replace('{{ARCHIVE}}', archive).replace('{{PROJECTS}}', projects)
           .replace('{{COUNT}}', str(len(themes))).replace('{{BASE}}', BASE)
           .replace('{{OG_IMAGE}}', f"{BASE}{latest['url']}cover.png" if latest and latest['has_cover'] else '')
           .replace('{{YEAR}}', str(dt.date.today().year)))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(home)

# ---------- feed / sitemap / robots / 404 / headers / redirects ----------
def rfc3339(s): return s + 'T08:00:00-07:00'
entries = ''.join(f"""  <entry>
    <title>{esc(m['title'])}</title>
    <link href="{BASE}{m['url']}"/>
    <id>{BASE}{m['url']}</id>
    <updated>{rfc3339(m['date'])}</updated>
    <summary>{esc(m.get('summary',''))}</summary>
  </entry>
""" for m in reversed(themes))
feed = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{esc(site['name'])}</title>
  <subtitle>{esc(site['tagline'])}</subtitle>
  <link href="{BASE}/"/>
  <link rel="self" href="{BASE}/feed.xml"/>
  <id>{BASE}/</id>
  <updated>{rfc3339(latest['date']) if latest else rfc3339(str(dt.date.today()))}</updated>
  <author><name>{esc(site['author'])}</name></author>
{entries}</feed>
"""
open(os.path.join(OUT, 'feed.xml'), 'w', encoding='utf-8').write(feed)
urls = [f"  <url><loc>{BASE}/</loc><lastmod>{latest['date'] if latest else dt.date.today()}</lastmod><changefreq>weekly</changefreq></url>"] + \
       [f"  <url><loc>{BASE}{m['url']}</loc><lastmod>{m['date']}</lastmod></url>" for m in themes]
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
for f in ('_headers', '_redirects', '404.html'):
    src = os.path.join(HUB, f)
    if os.path.exists(src): shutil.copy(src, OUT)
print(f"built {len(themes)} theme(s) → public/  (latest: 第 {latest['no']} 题 {latest['title']})" if latest else 'built: no themes')
