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
import sys, json, os, re, shutil, html, datetime as dt

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

# ---------- 号外（extras/）：与周更分开的专题，不占题号，地址 /x/<slug>/ ----------
EXTRAS = os.path.join(ROOT, 'extras')
extras = []
if os.path.isdir(EXTRAS):
    for d in sorted(os.listdir(EXTRAS)):
        p = os.path.join(EXTRAS, d)
        if not os.path.isdir(p) or not re.match(r'^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$', d): continue
        if not os.path.exists(os.path.join(p, 'index.html')) or not os.path.exists(os.path.join(p, 'meta.json')): continue
        m = json.load(open(os.path.join(p, 'meta.json'), encoding='utf-8'))
        m.setdefault('slug', d[11:]); m.setdefault('date', d[:10]); m.setdefault('tags', []); m.setdefault('format', '')
        m['dir'] = p; m['url'] = f"/x/{m['slug']}/"
        if m.get('draft'): continue
        extras.append(m)
extras.sort(key=lambda m: m['date'])

# ---------- 输出目录 ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 't'))

# ---------- 顶栏（注入每期页面） ----------
BAR_CSS = """<style id="yzyt-bar-css">
.yzyt-bar{--yb:#f5f5f2;--yi:#1a1c1a;--y2:#5b5f5a;--yl:#d9dbd5;--ya:#b5432c;font:13px/1.4 "Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:var(--yb);color:var(--y2);border-bottom:1px solid var(--yl);padding:8px clamp(16px,3vw,36px);display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:space-between}
.yzyt-bar a{color:var(--yi);text-decoration:none}.yzyt-bar a:hover{color:var(--ya)}
.yzyt-bar .brand{font-family:"Noto Serif SC","Songti SC",serif;font-weight:900;letter-spacing:.12em;color:var(--yi)}
.yzyt-bar .brand b{display:inline-block;background:var(--ya);color:#fff;font-size:11px;letter-spacing:.1em;padding:1px 6px;border-radius:2px;margin-left:8px;vertical-align:1px;font-family:"Noto Sans SC",sans-serif;font-weight:500}
.yzyt-bar .lhs{display:flex;gap:14px;align-items:center}.yzyt-bar .dt{color:var(--y2)}.yzyt-bar .home{color:var(--y2);letter-spacing:.08em}.yzyt-bar .home:after{content:"/";margin-left:14px;color:var(--yl)}
.yzyt-bar .nav{display:flex;gap:16px;align-items:center}.yzyt-bar .nav span{color:var(--yl)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .yzyt-bar{--yb:#141618;--yi:#ecebe4;--y2:#a9aca6;--yl:#2b2f33;--ya:#e2694f}}
:root[data-theme="dark"] .yzyt-bar{--yb:#141618;--yi:#ecebe4;--y2:#a9aca6;--yl:#2b2f33;--ya:#e2694f}
</style>"""

def bar_html(m, prev_m, next_m):
    left = f'<div class="lhs"><a class="home" href="/">{esc(site.get("person", {}).get("name", "首页"))}</a><a class="brand" href="/t/">{esc(site["name"])}<b>第 {m["no"]} 题</b></a><span class="dt">{esc(m["date"])}</span></div>'
    nav = []
    nav.append(f'<a href="{prev_m["url"]}" title="{esc(prev_m["title"])}">← 上一题</a>' if prev_m else '<span>← 上一题</span>')
    nav.append('<a href="/t/#archive">归档</a>')
    nav.append(f'<a href="{next_m["url"]}" title="{esc(next_m["title"])}">下一题 →</a>' if next_m else '<span>下一题 →</span>')
    return f'{BAR_CSS}\n<div class="yzyt-bar" role="navigation" aria-label="一周一题">{left}<div class="nav">{"".join(nav)}</div></div>\n'

def extra_bar_html(m):
    left = f'<div class="lhs"><a class="home" href="/">{esc(site.get("person", {}).get("name", "首页"))}</a><a class="brand" href="/t/">{esc(site["name"])}<b>号外</b></a><span class="dt">{esc(m["date"])}</span></div>'
    nav = '<div class="nav"><a href="/t/#extras">号外</a><a href="/t/#archive">归档</a></div>'
    return f'{BAR_CSS}\n<div class="yzyt-bar" role="navigation" aria-label="一周一题 · 号外">{left}{nav}</div>\n'

def inject(page, m, prev_m, next_m, bar=None):
    bar = bar or bar_html(m, prev_m, next_m)
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

for m in extras:
    dst = os.path.join(OUT, 'x', m['slug']); os.makedirs(dst)
    page = open(os.path.join(m['dir'], 'index.html'), encoding='utf-8').read()
    open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8').write(inject(page, m, None, None, bar=extra_bar_html(m)))
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
def xcard(m):
    cover = f'<img src="{m["url"]}cover.png" alt="" loading="lazy">' if m['has_cover'] else '<div class="nocover"></div>'
    tags = ''.join(f'<span>{esc(t)}</span>' for t in m['tags'])
    return (f'<a class="card" href="{m["url"]}"><div class="cv">{cover}</div><div class="cb"><div class="no">号外 <time datetime="{m["date"]}">{esc(m["date"])}</time></div>'
            f'<h3>{esc(m["title"])}</h3><p>{esc(m.get("subtitle") or m.get("summary",""))}</p><div class="tags">{tags}{"<i>"+esc(m["format"])+"</i>" if m["format"] else ""}</div></div></a>')
extras_html = ''
if extras:
    extras_html = (f'<section class="sec" id="extras"><div class="sec-h"><h2>号外</h2><span>周更之外的定制专题 · 共 {len(extras)} 篇</span></div>'
                   f'<div class="grid">{"".join(xcard(m) for m in reversed(extras))}</div></section>')
projects = ''.join(f'<a class="proj" href="{esc(p["url"])}"><b>{esc(p["title"])}</b><span>{esc(p["desc"])}</span></a>' for p in site.get('projects', []))
home = (tpl.replace('{{SITE_NAME}}', esc(site['name'])).replace('{{TAGLINE}}', esc(site['tagline'])).replace('{{ABOUT}}', site['about'])
           .replace('{{HERO}}', hero).replace('{{EXTRAS}}', extras_html).replace('{{ARCHIVE}}', archive).replace('{{PROJECTS}}', projects)
           .replace('{{COUNT}}', str(len(themes))).replace('{{BASE}}', BASE)
           .replace('{{OG_IMAGE}}', f"{BASE}{latest['url']}cover.png" if latest and latest['has_cover'] else '')
           .replace('{{YEAR}}', str(dt.date.today().year)))
os.makedirs(os.path.join(OUT, 't'), exist_ok=True)
open(os.path.join(OUT, 't', 'index.html'), 'w', encoding='utf-8').write(home)   # 一周一题首页搬到 /t/，站点根 / 是门户（见文末）

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
urls = [f"  <url><loc>{BASE}/</loc><lastmod>{latest['date'] if latest else dt.date.today()}</lastmod><changefreq>weekly</changefreq></url>",
        f"  <url><loc>{BASE}/t/</loc><lastmod>{latest['date'] if latest else dt.date.today()}</lastmod><changefreq>weekly</changefreq></url>"] + \
       [f"  <url><loc>{BASE}{m['url']}</loc><lastmod>{m['date']}</lastmod></url>" for m in themes + extras] + \
       [f"  <url><loc>{BASE}{p['url']}</loc></url>" for p in site.get('projects', []) if p['url'].startswith('/')]
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
for f in ('_headers', '_redirects', '404.html'):
    src = os.path.join(HUB, f)
    if os.path.exists(src): shutil.copy(src, OUT)
# ---------- static/：原样复制到站点根（独立小页面，如 /listen/） ----------
if os.path.exists(os.path.join(ROOT, 'cc', 'build_cc.py')):
    import subprocess; subprocess.run([sys.executable, os.path.join(ROOT, 'cc', 'build_cc.py')], check=True)
STATIC = os.path.join(ROOT, 'static')
if os.path.isdir(STATIC):
    shutil.copytree(STATIC, OUT, dirs_exist_ok=True)
print(f"built {len(themes)} theme(s) → public/  (latest: 第 {latest['no']} 题 {latest['title']})" if latest else 'built: no themes')

# ======================================================================
# 播客 /listen/：podcast/episodes/<YYYY-MM-DD>-<slug>/{meta.json, notes.html, cover.png, audio/, script.md}
# 输出 public/listen/index.html、public/listen/<slug>/、public/listen/feed.xml（带 enclosure 的播客 RSS）
# ======================================================================
POD = site.get('podcast')
PODDIR = os.path.join(ROOT, 'podcast', 'episodes')
if POD and os.path.isdir(PODDIR):
    PBASE = POD.get('path', '/listen/')
    eps = []
    for d in sorted(os.listdir(PODDIR)):
        p = os.path.join(PODDIR, d)
        if not os.path.isdir(p) or not re.match(r'^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$', d): continue
        if not os.path.exists(os.path.join(p, 'meta.json')): continue
        e = json.load(open(os.path.join(p, 'meta.json'), encoding='utf-8'))
        if e.get('draft'): continue
        e.setdefault('slug', d[11:]); e.setdefault('date', d[:10]); e.setdefault('tags', [])
        e['dir'] = p; e['url'] = f"{PBASE}{e['slug']}/"
        e['dur'] = e['tracks'][0]['dur']; e['min'] = round(e['dur'] / 60)
        e['has_cover'] = os.path.exists(os.path.join(p, 'cover.png'))
        e['sq'] = 'cover-sq.png' if os.path.exists(os.path.join(p, 'cover-sq.png')) else 'cover.png'
        eps.append(e)
    eps.sort(key=lambda e: e['date'])
    for i, e in enumerate(eps): e.setdefault('no', i + 1)
    pod_out = os.path.join(OUT, PBASE.strip('/')); os.makedirs(pod_out, exist_ok=True)

    def mmss(s): return f"{int(s)//60}:{int(s)%60:02d}"
    def hhmmss(s): s = int(s); return f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"
    ep_tpl = open(os.path.join(HUB, 'podcast_episode.html'), encoding='utf-8').read()
    skin_css = open(os.path.join(HUB, 'skin_cc.css'), encoding='utf-8').read()
    def thesis_html(th):
        if not th: return ''
        keys = set(th.get('keys', []))
        lines = ''.join('<span class="ln">' + ''.join(f'<span class="w{" k" if w in keys else ""}">{esc(w)}</span>' for w in ln) + '</span>' for ln in th['lines'])
        rest = f'<p class="tagrest">{esc(th["rest"])}</p>' if th.get('rest') else ''
        return f'<section class="band tagsec" aria-label="论点"><div class="tagstick"><div class="wide"><p class="tagl">{lines}</p>{rest}</div></div></section>'
    for i, e in enumerate(eps):
        dst = os.path.join(pod_out, e['slug']); os.makedirs(dst, exist_ok=True)
        for extra in ('cover.png', 'cover-sq.png', 'hero.jpg', 'hero-portrait.jpg', 'plate.jpg', 'audio', 'script.md'):
            src = os.path.join(e['dir'], extra)
            if os.path.isdir(src): shutil.copytree(src, os.path.join(dst, extra), dirs_exist_ok=True)
            elif os.path.exists(src): shutil.copy(src, dst)
        rd = lambda name: open(os.path.join(e['dir'], name), encoding='utf-8').read() if os.path.exists(os.path.join(e['dir'], name)) else ''
        notes, sections = rd('notes.html'), rd('sections.html')
        nav_extra = ''.join(f'<a href="#{m.group(1)}"><small>{esc(m.group(2))}</small>{esc(m.group(3))}</a>' for m in re.finditer(r'<section[^>]*\sid="([^"]+)"[^>]*data-nav="([^"|]*)\|([^"]*)"', sections))
        has = lambda name: os.path.exists(os.path.join(e['dir'], name))
        hero_img = ('<picture>' + (f'<source media="(max-aspect-ratio: 4/5)" srcset="hero-portrait.jpg">' if has('hero-portrait.jpg') else '') + f'<img src="hero.jpg" alt="{esc(e["title"])}"></picture>') if has('hero.jpg') else (f'<img src="cover.png" alt="{esc(e["title"])}">' if e['has_cover'] else '')
        plate_img = '<img src="plate.jpg" alt="" loading="lazy">' if has('plate.jpg') else ''
        prev_e = eps[i - 1] if i > 0 else None; next_e = eps[i + 1] if i + 1 < len(eps) else None
        epjson = json.dumps({'slug': e['slug'], 'title': e['title'], 'chapters': e['chapters'], 'tracks': [{'id': t['id'], 'title': t['title'], 'sub': t.get('sub', ''), 'src': t['file'], 'dur': t['dur'], 'ch': t['ch']} for t in e['tracks']]}, ensure_ascii=False)
        page = (ep_tpl.replace('{{SKIN}}', skin_css).replace('{{SKIN_OVERRIDE}}', e.get('skin_css', '')).replace('{{EP_JSON}}', epjson).replace('{{EP_TITLE}}', esc(e['title'])).replace('{{H1_CLASS}}', 'long' if len(e['title']) > 6 else '').replace('{{EP_TITLE_HTML}}', e.get('title_html') or esc(e['title'])).replace('{{EP_SUB}}', esc(e.get('subtitle', '')))
                .replace('{{EP_DESC}}', esc(e.get('summary', '')[:150])).replace('{{EP_SUMMARY}}', esc(e.get('summary', ''))).replace('{{EP_KICKER}}', esc(e.get('kicker', e['date']))).replace('{{EP_DATE}}', e['date']).replace('{{EP_NO}}', str(e['no'])).replace('{{EP_MIN}}', str(e['min']))
                .replace('{{EP_URL}}', e['url']).replace('{{POD_NAME}}', esc(POD['name'])).replace('{{BASE}}', BASE).replace('{{YEAR}}', str(dt.date.today().year))
                .replace('{{BOOKS}}', ''.join(f'<span>{esc(b)}</span>' for b in e.get('books', []))).replace('{{NOTES}}', notes).replace('{{SECTIONS}}', sections).replace('{{NAV_EXTRA}}', nav_extra)
                .replace('{{HERO_IMG}}', hero_img).replace('{{HERO_CAP}}', esc(e.get('hero_caption', ''))).replace('{{THESIS}}', thesis_html(e.get('thesis')))
                .replace('{{PLATE0_IMG}}', plate_img).replace('{{PLATE0_CAP}}', esc(e.get('plate_caption', '')))
                .replace('{{PREV}}', f'<a href="{prev_e["url"]}" title="{esc(prev_e["title"])}">← 上一期</a>' if prev_e else '<span>← 上一期</span>')
                .replace('{{NEXT}}', f'<a href="{next_e["url"]}" title="{esc(next_e["title"])}">下一期 →</a>' if next_e else '<span>下一期 →</span>'))
        open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8').write(page)

    # 播客首页（骨架与节目页同一皮肤）
    latest_e = eps[-1] if eps else None
    def ep_card(e):
        cover = f'<img src="{e["url"]}{e["sq"]}" alt="" loading="lazy">' if e['has_cover'] else ''
        tags = ''.join(f'<span>{esc(t)}</span>' for t in e['tags'])
        return (f'<li><a href="{e["url"]}"><div class="d">{e["date"]}<b>第 {e["no"]} 期</b></div><div class="cv">{cover}</div>'
                f'<div><h3>{esc(e["title"])}</h3><p>{esc(e.get("subtitle") or e.get("summary", ""))}</p><div class="meta"><span>{e["min"]} 分钟</span><span>{len(e["tracks"])} 个声音版本</span>{tags}</div></div></a></li>')
    hero = hero_fig = ''
    if latest_e:
        hero = (f'<p class="latest">最新 · 第 {latest_e["no"]} 期 · {nice_date(latest_e["date"])}</p><p class="hp"><b>{esc(latest_e["title"])}</b>　{esc(latest_e.get("summary", ""))}</p>'
                f'<div class="ha"><a class="btn" href="{latest_e["url"]}">开始收听<svg viewBox="0 0 24 24"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a><span class="hm">{latest_e["min"]} 分钟 · {len(latest_e["tracks"])} 个声音版本</span></div>')
        img = f'{latest_e["url"]}hero.jpg' if os.path.exists(os.path.join(latest_e['dir'], 'hero.jpg')) else (f'{latest_e["url"]}cover.png' if latest_e['has_cover'] else '')
        hero_fig = f'<figure class="hfig rise"><a href="{latest_e["url"]}"><img src="{img}" alt="{esc(latest_e["title"])}"></a><figcaption>{esc(latest_e.get("hero_caption", latest_e["title"]))}</figcaption></figure>' if img else ''
    ptpl = open(os.path.join(HUB, 'podcast_home.html'), encoding='utf-8').read()
    home_p = (ptpl.replace('{{SKIN}}', skin_css).replace('{{POD_NAME}}', esc(POD['name'])).replace('{{POD_TAGLINE}}', esc(POD['tagline'].split('。')[0] + '。')).replace('{{POD_ABOUT}}', POD['about'])
              .replace('{{HERO}}', hero).replace('{{HERO_FIG}}', hero_fig).replace('{{EPISODES}}', ''.join(ep_card(e) for e in reversed(eps))).replace('{{COUNT}}', str(len(eps)))
              .replace('{{BASE}}', BASE).replace('{{YEAR}}', str(dt.date.today().year))
              .replace('{{OG_IMAGE}}', f"{BASE}{latest_e['url']}cover.png" if latest_e and latest_e['has_cover'] else ''))
    open(os.path.join(pod_out, 'index.html'), 'w', encoding='utf-8').write(home_p)

    # 播客 RSS（iTunes 命名空间；enclosure 用第一条音轨）
    items = ''
    for e in reversed(eps):
        t = e['tracks'][0]; af = os.path.join(e['dir'], t['file']); size = os.path.getsize(af) if os.path.exists(af) else 0
        pub = dt.datetime.fromisoformat(e['date'] + 'T08:00:00-07:00').strftime('%a, %d %b %Y %H:%M:%S %z')
        items += f"""    <item>
      <title>{esc(e['title'])}</title>
      <link>{BASE}{e['url']}</link>
      <guid isPermaLink="true">{BASE}{e['url']}</guid>
      <pubDate>{pub}</pubDate>
      <description>{esc(e.get('summary', ''))}</description>
      <enclosure url="{BASE}{e['url']}{t['file']}" length="{size}" type="audio/mpeg"/>
      <itunes:duration>{hhmmss(t['dur'])}</itunes:duration>
      <itunes:episode>{e['no']}</itunes:episode>
      {'<itunes:image href="'+BASE+e['url']+'cover.png"/>' if e['has_cover'] else ''}
    </item>
"""
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{esc(POD['name'])}</title>
    <link>{BASE}{PBASE}</link>
    <atom:link href="{BASE}{PBASE}feed.xml" rel="self" type="application/rss+xml"/>
    <language>zh-cn</language>
    <description>{esc(POD['tagline'])}</description>
    <itunes:author>{esc(POD.get('author', site['author']))}</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    {'<itunes:image href="'+BASE+latest_e['url']+'cover.png"/>' if latest_e and latest_e['has_cover'] else ''}
{items}  </channel>
</rss>
"""
    open(os.path.join(pod_out, 'feed.xml'), 'w', encoding='utf-8').write(rss)
    # sitemap 补充
    sm = open(os.path.join(OUT, 'sitemap.xml'), encoding='utf-8').read()
    add = ''.join(f"  <url><loc>{BASE}{e['url']}</loc><lastmod>{e['date']}</lastmod></url>\n" for e in eps)
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm.replace('</urlset>', add + '</urlset>'))
    print(f"podcast: {len(eps)} episode(s) → {PBASE}")

# ======================================================================
# 门户 /：孙天杰的首页。看（一周一题 + 号外）/ 听（合读 + CC 读书会）/ 玩（Game Studio）/ 走（摄影导览）
# 数据：themes、extras、eps（上面播客段算出来的）、cc/cc.json、site.json 的 person / lines / games / tour
# ======================================================================
PERSON = site.get('person', {'name': '首页', 'en': site['author'], 'lead': site['tagline']})
LINES = site.get('lines', {})
GAMES = site.get('games', [])
TOUR = site.get('tour', {})
try: eps
except NameError: eps = []
CC = None
cc_path = os.path.join(ROOT, 'cc', 'cc.json')
if os.path.exists(cc_path): CC = json.load(open(cc_path, encoding='utf-8'))

def cn_md(s):
    d = dt.date.fromisoformat(s); return f"{d.month} 月 {d.day} 日", f"周{WEEKDAY[d.weekday()]}"
def num_only(s):
    mm = re.search(r'\d+', s or ''); return mm.group(0) if mm else ''

# --- 日志：四条线最近更新的 ---
log = []
for m in themes: log.append({'date': m['date'], 'ch': '看', 'title': m['title'], 'sub': f"一周一题 第 {m['no']} 题" + (f"，{m['reading_time']}" if m.get('reading_time') else ''), 'url': m['url']})
for m in extras: log.append({'date': m['date'], 'ch': '看', 'title': m['title'], 'sub': '号外' + ('，' + '，'.join(t for t in m['tags'] if '双语' in t) if any('双语' in t for t in m['tags']) else ''), 'url': m['url']})
for e in eps: log.append({'date': e['date'], 'ch': '听', 'title': e['title'], 'sub': f"合读 第 {e['no']} 期" + (f"，{e['kicker'].replace(' · ', ' ')}" if e.get('kicker') else ''), 'url': e['url']})
for g in GAMES:
    if g.get('date'): log.append({'date': g['date'], 'ch': '玩', 'title': g.get('log', g['title']), 'sub': g.get('log_sub', ''), 'url': g['url']})
if TOUR.get('date'): log.append({'date': TOUR['date'], 'ch': '走', 'title': f"{TOUR['title']}：{TOUR['place']}", 'sub': TOUR.get('kicker', ''), 'url': TOUR['url']})
log.sort(key=lambda x: x['date'], reverse=True)
log = log[:6]
log_html = ''.join(f'<a{" class=new" if i == 0 else ""} href="{x["url"]}"><span class="d"><b>{cn_md(x["date"])[0]}</b>{cn_md(x["date"])[1]}</span>'
                   f'<span class="t"><span class="ch">{x["ch"]}</span><span>{esc(x["title"])}</span>{"<small>"+esc(x["sub"])+"</small>" if x["sub"] else ""}</span></a>' for i, x in enumerate(log))

# --- 目录 ---
latest_e = eps[-1] if eps else None
toc = [('看', '#kan', site['name'], LINES.get('kan', {}).get('desc', ''), f"第 {latest['no']} 题" if latest else ''),
       ('听', '#ting', POD['name'] if POD else '合读', LINES.get('ting', {}).get('desc', ''), f"第 {latest_e['no']} 期" if latest_e else ''),
       ('玩', '#wan', 'Game Studio', LINES.get('wan', {}).get('desc', ''), f"作品 {GAMES[-1]['no']:02d}" if GAMES else ''),
       ('走', '#zou', TOUR.get('title', '摄影导览'), LINES.get('zou', {}).get('desc', ''), TOUR.get('place', '').split(' ')[-1] if TOUR else '')]
toc_html = ''.join(f'<li><a href="{h}"><span class="ch">{ch}</span><span class="nm">{esc(nm)}<span class="sub">{esc(sub)}</span></span><span class="dots"></span><span class="pg">{esc(pg)}</span></a></li>' for ch, h, nm, sub, pg in toc)

# --- 看 ---
def plate(img, cap, url, sq=False):
    return f'<figure{" class=sq" if sq else ""}><a href="{url}"><img src="{img}" alt="" loading="lazy"></a>{"<figcaption>"+esc(cap)+"</figcaption>" if cap else ""}</figure>'
kan = ''
if latest:
    md, wd = cn_md(latest['date'])
    cap = '第 %d 题封面' % latest['no']
    kan_feat = (f'<div class="entry">{plate(latest["url"]+"cover.png", cap, latest["url"]) if latest["has_cover"] else "<div></div>"}'
                f'<div><div class="no">本周 第 {latest["no"]} 题，{md}</div><h3>{esc(latest["title"])}</h3><p>{esc(latest.get("subtitle") or latest.get("summary", ""))}</p><a class="go" href="{latest["url"]}">打开这一题</a></div></div>')
    rows = ''.join(f'<li><span>第 {m["no"]} 题</span><a href="{m["url"]}">{esc(m["title"])}</a><em>{cn_md(m["date"])[0]}</em></li>' for m in list(reversed(themes))[1:4])
    rows += ''.join(f'<li><span>号外</span><a href="{m["url"]}">{esc(m["title"])}</a><em>{cn_md(m["date"])[0]}</em></li>' for m in list(reversed(extras))[:2])
    kan = (f'<section class="ch-sec" id="kan"><div class="big">看</div><h2>{esc(site["name"])}<span>共 {len(themes)} 题，每周六</span></h2><p class="lead">{esc(LINES.get("kan", {}).get("lead", site["tagline"]))}</p>'
           f'{kan_feat}<ul class="rows">{rows}</ul><a class="go" href="/t/">全部 {len(themes)} 题{"与号外" if extras else ""}</a></section>')

# --- 听 ---
ting = ''
if latest_e or CC:
    ent = ''
    if latest_e:
        md, wd = cn_md(latest_e['date'])
        cap = '第 %d 期' % latest_e['no']
        ent += (f'<div class="entry">{plate(latest_e["url"]+latest_e["sq"], cap, latest_e["url"], sq=True) if latest_e["has_cover"] else "<div></div>"}'
                f'<div><div class="no">最新 第 {latest_e["no"]} 期，{md}，{latest_e["min"]} 分钟</div><h3 class="disp">{esc(latest_e["title"])}</h3><p>{esc(latest_e.get("subtitle", ""))}</p><a class="go" href="{latest_e["url"]}">开始收听</a></div></div>')
    if CC:
        weeks = CC.get('weeks', [])
        today = str(dt.date.today())
        cur = next((w for w in weeks if w.get('status') == 'now'), None) or next((w for w in reversed(weeks) if w['date'] <= today), weeks[0] if weeks else None)
        nxt = next((w for w in weeks if cur and w['no'] == cur['no'] + 1), None)
        wk = ''
        if cur: wk += f'<dt>本周 第 {cur["no"]} 周</dt><dd>{esc(cur["author"])}{esc(cur["work"])} {esc(cur["read"])}</dd>'
        if nxt: wk += f'<dt>下周 {cn_md(nxt["date"])[0]}</dt><dd>{esc(nxt["author"])}{esc(nxt["work"])} {esc(nxt["read"])}</dd>'
        cc_img = '/cc/img/hero-athens.jpg' if os.path.exists(os.path.join(ROOT, 'static', 'cc', 'img', 'hero-athens.jpg')) else ''
        ent += (f'<div class="entry">{plate(cc_img, "CC 读书会，雅典", "/cc/") if cc_img else "<div></div>"}'
                f'<div><div class="no">{esc(CC["title"])}，跟着哥大书单读十二周</div><h3>一周一本，每周一期节目、一份测验、一页纸</h3><dl class="week">{wk}</dl><a class="go" href="/cc/">十二周路径与书库</a></div></div>')
    ting = (f'<section class="ch-sec" id="ting"><div class="big">听</div><h2>{esc(POD["name"] if POD else "合读")}<span>共 {len(eps)} 期</span></h2><p class="lead">{esc(LINES.get("ting", {}).get("lead", POD["tagline"] if POD else ""))}</p>{ent}</section>')

# --- 玩 ---
wan = ''
if GAMES:
    ent = ''.join(f'<div class="entry">{plate(g["cover"], g.get("caption", ""), g["url"]) if g.get("cover") else "<div></div>"}'
                  f'<div><div class="no">{esc(g.get("kicker", ""))}</div><h3 class="disp">{esc(g["title"])}</h3><p>{esc(g.get("desc", ""))}</p><a class="btn" href="{g.get("play", g["url"])}">在浏览器里玩</a> <a class="go" href="{g["url"]}" style="margin-left:14px">作品页</a></div></div>' for g in GAMES)
    wan = f'<section class="ch-sec" id="wan"><div class="big">玩</div><h2>Game Studio<span>一个人的游戏工作室</span></h2><p class="lead">{esc(LINES.get("wan", {}).get("lead", ""))}</p>{ent}</section>'

# --- 走 ---
zou = ''
if TOUR:
    stops = TOUR.get('stops', [])
    n = max(len(stops), 2)
    pts = [(90 + i * (1020 / (n - 1)), 520 - i * (430 / (n - 1)) + (60 if i % 2 else -20)) for i in range(n)]
    path = f'M{pts[0][0]:.0f} {pts[0][1]:.0f} ' + ' '.join(f'Q{(pts[i-1][0]+pts[i][0])/2:.0f} {pts[i-1][1]:.0f} {pts[i][0]:.0f} {pts[i][1]:.0f}' for i in range(1, n))
    dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12"/>' for x, y in pts)
    labels = ''.join(f'<text x="{x+18:.0f}" y="{y+ (38 if i % 2 else -16):.0f}">{esc(s)}</text>' for i, ((x, y), s) in enumerate(zip(pts, stops)))
    svg = (f'<svg class="route" viewBox="0 0 1200 630" aria-hidden="true"><path d="{path}" fill="none" stroke="var(--ink)" stroke-width="4" stroke-dasharray="12 10"/>'
           f'<g fill="var(--ink)">{dots}</g><g font-family="Noto Sans SC,sans-serif" font-size="26" fill="var(--ink2)">{labels}</g></svg>')
    zou = (f'<section class="ch-sec" id="zou"><div class="big">走</div><h2>{esc(TOUR["title"])}<span>{esc(TOUR["place"])}</span></h2><p class="lead">{esc(LINES.get("zou", {}).get("lead", ""))}</p>'
           f'<div class="entry"><figure><a href="{TOUR["url"]}">{svg}</a><figcaption>路线示意，{len(stops)} 个落脚点</figcaption></figure>'
           f'<div><div class="no">{esc(TOUR.get("kicker", ""))}</div><h3>{esc(TOUR["place"])} 的一条拍摄路线</h3><p>{esc(TOUR.get("desc", ""))}</p><a class="go" href="{TOUR["url"]}">打开 3D 路线地图</a></div></div></section>')

ptl = open(os.path.join(HUB, 'portal.html'), encoding='utf-8').read()
portal = (ptl.replace('{{NAME}}', esc(PERSON['name'])).replace('{{EN}}', esc(PERSON.get('en', site['author']))).replace('{{LEAD}}', esc(PERSON.get('lead', '')))
             .replace('{{TOC}}', toc_html).replace('{{LOG}}', log_html).replace('{{KAN}}', kan).replace('{{TING}}', ting).replace('{{WAN}}', wan).replace('{{ZOU}}', zou)
             .replace('{{BASE}}', BASE).replace('{{YEAR}}', str(dt.date.today().year))
             .replace('{{OG_IMAGE}}', f"{BASE}{latest['url']}cover.png" if latest and latest['has_cover'] else ''))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(portal)
print(f"portal: / ({len(log)} log entries; 看 {len(themes)} 听 {len(eps)} 玩 {len(GAMES)} 走 {1 if TOUR else 0})")
