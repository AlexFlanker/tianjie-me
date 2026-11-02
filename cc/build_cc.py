#!/usr/bin/env python3
"""Render static/cc/index.html from cc/cc.json. Run before build.py (or let build.py call it).
Skin: Columbia College's CC page palette — deep blue #002855 as the only accent, warm paper #F2F0ED,
white content cards, ink #333, sky #77C2EF only for progress / current week. Fonts per site rule: Noto Serif SC + Noto Sans SC."""
import json, os, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'cc', 'cc.json'), encoding='utf-8'))
e = html.escape
today = datetime.date.today()

def week_state(w):
    if w.get('status') == 'now': return 'now'
    d = datetime.date.fromisoformat(w['date'])
    return 'done' if d < today and w.get('status') != 'now' and w.get('done') else ('past' if d < today else 'todo')

weeks = D['weeks']; cur = next((w for w in weeks if w.get('status') == 'now'), weeks[0])
done_n = sum(1 for w in weeks if w.get('done'))
pct = round(100 * done_n / len(weeks))

spine = ''.join(f'''<li><span class="no">{s["no"]:02d}</span><div><b>{e(s["name"])}</b><i>{e(s["era"])}</i><p>{e(s["who"])}</p><p class="ln">{e(s["line"])}</p></div></li>''' for s in D['spine'])
threads = ''.join(f'<li><b>{e(t["name"])}</b><span>{e(t["path"])}</span></li>' for t in D['threads'])
method = ''.join(f'<li>{e(m)}</li>' for m in D['method'])

def wk(w):
    st = week_state(w)
    ep = f'<a class="ep" href="{e(w["ep"])}">听节目 ↗</a>' if w.get('ep') else '<span class="ep off">节目待出</span>'
    lib = w.get('lib', '')
    libc = 'ok' if lib.startswith('有') or lib.startswith('自有') else ('part' if lib.startswith('部分') else 'no')
    return (f'<li class="wk {st}" id="w{w["no"]}"><div class="d"><span class="n">第 {w["no"]} 周</span><time datetime="{w["date"]}">{w["date"][5:].replace("-", " / ")}</time></div>'
            f'<div class="b"><h3>{e(w["author"])}<small>{e(w["work"])}</small></h3><p class="rd">{e(w["read"])}</p>'
            f'<p class="fr"><span class="k">对着</span>{e(w["for"])}</p><p class="pp"><span class="k">一页纸</span>{e(w["paper"])}</p>'
            f'<div class="ft"><span class="lib {libc}">书库：{e(lib)}</span>{ep}</div></div></li>')
wks = ''.join(wk(w) for w in weeks)

lib = D['library']
have = ''.join(f'<li>{e(x)}</li>' for x in lib['have']); free = ''.join(f'<li>{e(x)}</li>' for x in lib['free']); buy = ''.join(f'<li>{e(x)}</li>' for x in lib['buy'])

page = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(D["title"])} · 跟着哥大 Contemporary Civilization 书单读十二周 — 天杰</title>
<meta name="description" content="{e(D["subtitle"])} 知识脉络、十二周路径、本地书库对照、每周节目与一页纸。">
<meta property="og:title" content="{e(D["title"])} · 天杰">
<meta property="og:description" content="{e(D["subtitle"])}">
<meta property="og:image" content="https://tianjie.me/listen/cc-leviathan/cover.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%23002855'/%3E%3Ctext x='32' y='44' font-size='30' text-anchor='middle' font-family='Noto Serif SC,serif' font-weight='900' fill='%23F2F0ED'%3ECC%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700;900&family=Noto+Sans+SC:wght@400;500;700&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700;900&family=Noto+Sans+SC:wght@400;500;700&display=swap"></noscript>
<script>try{{var t=localStorage.getItem('yzyt-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
<style>
:root{{--blue:#002855;--blue-ink:#F2F0ED;--paper:#F2F0ED;--card:#FFFFFF;--ink:#333333;--ink-2:#5A5A5A;--muted:#7A7772;--line:#D9D4CC;--sky:#77C2EF;--link:#0753A0;--ok:#1E7B4C;--warn:#8A6D1E;--bad:#A3362B}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--blue:#9DC3EA;--blue-ink:#0B1626;--paper:#0B1626;--card:#132339;--ink:#E8E4DC;--ink-2:#C2BDB3;--muted:#8E93A0;--line:#27405E;--link:#9DC3EA;--ok:#6FCB95;--warn:#D9B45A;--bad:#E88A7E}}}}
:root[data-theme="dark"]{{--blue:#9DC3EA;--blue-ink:#0B1626;--paper:#0B1626;--card:#132339;--ink:#E8E4DC;--ink-2:#C2BDB3;--muted:#8E93A0;--line:#27405E;--link:#9DC3EA;--ok:#6FCB95;--warn:#D9B45A;--bad:#E88A7E}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans SC","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;font-size:16px;line-height:1.75;-webkit-font-smoothing:antialiased}}
a{{color:var(--link)}}
h1,h2,h3{{font-family:"Noto Serif SC","Songti SC",serif;margin:0;text-wrap:balance}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 20px}}
.top{{background:var(--blue);color:var(--blue-ink)}}
.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 20px;font-size:13.5px}}
.top a{{color:inherit;text-decoration:none;opacity:.9}}.top a:hover{{opacity:1;text-decoration:underline}}
.top .brand{{font-family:"Noto Serif SC",serif;font-weight:900;letter-spacing:.12em;font-size:15px}}
.top nav{{display:flex;gap:16px;flex-wrap:wrap}}
.theme-btn{{font:inherit;font-size:12px;color:inherit;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:2px 10px;background:none;cursor:pointer}}
.hero{{padding:48px 0 36px;border-bottom:1px solid var(--line)}}
.hero .kicker{{font:600 12px/1.6 "Noto Sans SC",sans-serif;letter-spacing:.14em;color:var(--blue);text-transform:uppercase}}
.hero h1{{font-size:clamp(34px,5.4vw,56px);font-weight:900;color:var(--blue);line-height:1.15;margin:6px 0 10px}}
.hero .sub{{font-size:17px;color:var(--ink-2);max-width:60ch}}
.hero .q{{margin:22px 0 0;padding:16px 20px;background:var(--card);border-left:4px solid var(--blue);font-family:"Noto Serif SC",serif;font-size:19px;font-weight:700;color:var(--blue)}}
.hero .src{{margin:14px 0 0;font-size:13px;color:var(--muted)}}
.now{{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.9fr);gap:24px;align-items:stretch;padding:28px 0;border-bottom:1px solid var(--line)}}
.now .card{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--blue);padding:20px 22px}}
.now .card .k{{font:600 12px/1.6 "Noto Sans SC",sans-serif;letter-spacing:.12em;color:var(--blue)}}
.now .card h2{{font-size:26px;font-weight:900;margin:4px 0 6px}}
.now .card h2 small{{display:block;font-size:15px;font-weight:500;color:var(--ink-2);margin-top:2px}}
.now .card p{{margin:6px 0;font-size:15px}}
.now .card .btn{{display:inline-block;margin-top:12px;padding:9px 18px;border-radius:999px;background:var(--blue);color:var(--blue-ink);text-decoration:none;font-weight:600;font-size:14px}}
.prog{{background:var(--card);border:1px solid var(--line);padding:20px 22px;display:flex;flex-direction:column;justify-content:center;gap:10px}}
.prog .big{{font-family:"Noto Serif SC",serif;font-size:44px;font-weight:900;color:var(--blue);line-height:1;font-variant-numeric:tabular-nums}}
.prog .big small{{font-size:16px;font-weight:500;color:var(--ink-2);margin-left:6px}}
.prog .bar{{height:8px;background:var(--paper);border:1px solid var(--line);border-radius:999px;overflow:hidden}}
.prog .bar i{{display:block;height:100%;width:{pct}%;min-width:0;background:var(--sky)}}
.prog .dots{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:4px;align-items:stretch}}
.prog .dots span{{display:block;height:10px;min-width:0;border-radius:2px;background:var(--line)}}.prog .dots span.done{{background:var(--blue)}}.prog .dots span.now{{background:var(--sky)}}
.prog p{{margin:0;font-size:13px;color:var(--muted)}}
section.sec{{padding:36px 0;border-bottom:1px solid var(--line)}}
.sec-h{{display:flex;align-items:baseline;gap:14px;margin-bottom:18px}}.sec-h h2{{font-size:24px;font-weight:900;color:var(--blue)}}.sec-h span{{font-size:13px;color:var(--muted)}}
.spine{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}}
.spine li{{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);padding:14px 14px 12px}}
.spine .no{{font-family:"Noto Serif SC",serif;font-weight:900;font-size:22px;color:var(--blue);line-height:1;font-variant-numeric:tabular-nums}}
.spine b{{display:block;font-family:"Noto Serif SC",serif;font-size:16px}}.spine i{{display:block;font-style:normal;font-size:12px;color:var(--muted);letter-spacing:.06em}}
.spine p{{margin:6px 0 0;font-size:13.5px;color:var(--ink-2)}}.spine p.ln{{color:var(--ink);margin-top:4px}}
.half{{display:flex;justify-content:space-between;gap:16px;margin:6px 0 14px;font-size:13px;color:var(--muted)}}.half b{{color:var(--blue);font-weight:600}}
.threads{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.threads li{{display:grid;grid-template-columns:150px minmax(0,1fr);gap:12px;padding:10px 14px;background:var(--card);border:1px solid var(--line);font-size:14.5px}}
.threads b{{color:var(--blue);font-family:"Noto Serif SC",serif}}
.method{{margin:0;padding-left:22px;font-size:15px}}.method li{{margin:6px 0}}
.weeks{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}
.wk{{display:grid;grid-template-columns:96px minmax(0,1fr);gap:0;background:var(--card);border:1px solid var(--line)}}
.wk .d{{padding:14px 12px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:2px;background:var(--paper)}}
.wk .d .n{{font:700 13px/1.4 "Noto Sans SC",sans-serif;color:var(--blue)}}.wk .d time{{font-size:12.5px;color:var(--muted);font-variant-numeric:tabular-nums}}
.wk .b{{padding:14px 16px 12px}}
.wk h3{{font-size:18px;font-weight:700}}.wk h3 small{{font-weight:500;font-size:14px;color:var(--ink-2);margin-left:8px}}
.wk p{{margin:4px 0;font-size:14px}}.wk .rd{{color:var(--ink)}}.wk .k{{display:inline-block;min-width:3.5em;color:var(--muted);font-size:12.5px;letter-spacing:.06em}}
.wk .ft{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:8px;font-size:12.5px}}
.wk .lib{{padding:1px 8px;border-radius:999px;border:1px solid var(--line)}}.wk .lib.ok{{color:var(--ok);border-color:var(--ok)}}.wk .lib.part{{color:var(--warn);border-color:var(--warn)}}.wk .lib.no{{color:var(--bad);border-color:var(--bad)}}
.wk .ep{{font-weight:600;text-decoration:none}}.wk .ep.off{{color:var(--muted);font-weight:400}}
.wk.now{{border-color:var(--blue);box-shadow:0 0 0 2px var(--sky) inset}}.wk.now .d{{background:var(--blue);color:var(--blue-ink)}}.wk.now .d .n,.wk.now .d time{{color:inherit}}
.wk.done .d{{background:color-mix(in srgb,var(--blue) 12%,var(--paper))}}
.lib3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
.lib3 div{{background:var(--card);border:1px solid var(--line);padding:14px 16px}}.lib3 h3{{font-size:15px;margin-bottom:6px}}.lib3 ul{{margin:0;padding-left:18px;font-size:14px}}.lib3 li{{margin:2px 0}}
.lib3 .h h3{{color:var(--ok)}}.lib3 .f h3{{color:var(--warn)}}.lib3 .b h3{{color:var(--bad)}}
.note{{font-size:14px;color:var(--ink-2);margin:0 0 14px}}
footer{{padding:28px 0 40px;font-size:13px;color:var(--muted);display:flex;gap:16px;flex-wrap:wrap}}footer a{{color:inherit}}
@media (max-width:720px){{.now{{grid-template-columns:minmax(0,1fr)}}.threads li{{grid-template-columns:minmax(0,1fr)}}.wk{{grid-template-columns:minmax(0,1fr)}}.wk .d{{flex-direction:row;gap:10px;border-right:0;border-bottom:1px solid var(--line)}}.top nav{{gap:10px}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
</style>
</head>
<body>
<div class="top"><div class="wrap"><a class="brand" href="/">一周一题</a><nav><a href="#path">十二周</a><a href="#spine">脉络</a><a href="#lib">书库</a><a href="/listen/">合读</a><button class="theme-btn" id="themebtn" type="button" aria-label="切换深浅色">◐ 深浅色</button></nav></div></div>
<main class="wrap">
<section class="hero">
  <div class="kicker">长期专题 · Contemporary Civilization</div>
  <h1>{e(D["title"])}</h1>
  <p class="sub">{e(D["subtitle"])} 每周：听一期节目拿到地图，读原书的指定章节，做测验，周日前交一页纸。</p>
  <div class="q">{e(D["question"])}</div>
  <p class="src">书单来源：<a href="{e(D["source"]["course"])}" rel="noopener">课程页</a> · <a href="{e(D["source"]["bulletin"])}" rel="noopener">Bulletin</a> · <a href="{e(D["source"]["list"])}" rel="noopener">2021–22 必读书单（PDF）</a>。书单每三年修订一次。</p>
</section>

<section class="now">
  <div class="card">
    <div class="k">本周 · 第 {cur["no"]} 周 · {cur["date"]}</div>
    <h2>{e(cur["author"])}<small>{e(cur["work"])} · {e(cur["read"])}</small></h2>
    <p><b>对着：</b>{e(cur["for"])}</p>
    <p><b>一页纸：</b>{e(cur["paper"])}</p>
    {'<a class="btn" href="'+e(cur["ep"])+'">听这一期 → 约 44 分钟 · 五组测验</a>' if cur.get("ep") else ''}
  </div>
  <div class="prog">
    <div class="big">{done_n}<small>/ 12 周交了一页纸</small></div>
    <div class="bar"><i></i></div>
    <div class="dots">{''.join('<span class="'+('done' if w.get('done') else ('now' if w.get('status')=='now' else ''))+'" title="第 '+str(w['no'])+' 周"></span>' for w in weeks)}</div>
    <p>进度在交一页纸后更新；当前周为浅蓝。</p>
  </div>
</section>

<section class="sec" id="path">
  <div class="sec-h"><h2>十二周路径</h2><span>按弱点排序，不按书单顺序 · 每周 2–3 小时</span></div>
  <ol class="method">{method}</ol>
  <ul class="weeks">{wks}</ul>
  <p class="note" style="margin-top:14px">{e(D["second"])}</p>
</section>

<section class="sec" id="spine">
  <div class="sec-h"><h2>知识脉络</h2><span>八段主干 · 五条纵线</span></div>
  <div class="half"><span><b>上学期</b> 从「秩序是被发现的」到「秩序是被约定的」（01–05）</span><span><b>下学期</b> 契约许下的承诺，以及它排除了谁（06–08）</span></div>
  <ol class="spine">{spine}</ol>
  <h3 style="font-size:17px;margin:22px 0 10px;color:var(--blue)">五条纵线（横着串起全书）</h3>
  <ul class="threads">{threads}</ul>
</section>

<section class="sec" id="lib">
  <div class="sec-h"><h2>书库对照</h2><span>HarborLibrary 本地书库 × CC 必读书单</span></div>
  <p class="note">{e(lib["note"])}</p>
  <div class="lib3">
    <div class="h"><h3>库里有（指定篇目）</h3><ul>{have}</ul></div>
    <div class="f"><h3>缺，但公有领域可免费取得</h3><ul>{free}</ul></div>
    <div class="b"><h3>缺，在版权内（买中译或借）</h3><ul>{buy}</ul></div>
  </div>
</section>
</main>
<footer class="wrap"><span>© {today.year} Tianjie Sun</span><a href="/">一周一题</a><a href="/listen/">合读</a><a href="/listen/feed.xml">播客 RSS</a></footer>
<script>
(function(){{var r=document.documentElement,b=document.getElementById('themebtn');if(!b)return;function L(){{var t=r.getAttribute('data-theme');b.textContent=t==='dark'?'☀ 浅色':t==='light'?'☾ 深色':'◐ 深浅色'}}
b.addEventListener('click',function(){{var d=r.getAttribute('data-theme')==='dark'||(!r.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);r.setAttribute('data-theme',d?'light':'dark');try{{localStorage.setItem('yzyt-theme',r.getAttribute('data-theme'))}}catch(e){{}}L()}});L()}})();
</script>
</body>
</html>'''
out = os.path.join(ROOT, 'static', 'cc'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
print('static/cc/index.html written; current week', cur['no'], 'done', done_n)
