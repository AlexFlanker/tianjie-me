#!/usr/bin/env python3
"""Render static/cc/index.html from cc/cc.json + cc/images.json, in the site's chapter system (skin: hub/skin_cc.css).
Structure: 站点顶栏 → 卷首（左字右图）→ 论点逐词点亮 → 章节导航 → 00 本周 → 01 十二周 → 02 脉络 → 03 书库 → 卷末。"""
import json, os, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'cc', 'cc.json'), encoding='utf-8'))
IMG = json.load(open(os.path.join(ROOT, 'cc', 'images.json'), encoding='utf-8'))
SKIN = open(os.path.join(ROOT, 'hub', 'skin_cc.css'), encoding='utf-8').read()
e = html.escape
today = datetime.date.today()

weeks = D['weeks']; cur = next((w for w in weeks if w.get('status') == 'now'), weeks[0])
done_n = sum(1 for w in weeks if w.get('done'))

def fig(key, cls='pimg', lazy=True):
    i = IMG[key]
    return f'<figure class="{cls}"><img src="img/{key}.jpg" alt="{e(i["alt"])}"{" loading=lazy" if lazy else ""}><figcaption>{e(i["cap"])}</figcaption></figure>'

# ---- 卷首 / 论点
th = D['thesis']
tag = ''.join('<span class="ln">' + ''.join(f'<span class="w{" k" if w in th["keys"] else ""}">{e(w)}</span>' for w in ln) + '</span>' for ln in th['lines'])

# ---- 00 本周：十二格刻度 + 本周卡
ruler = ''.join(f'<a class="tick{" done" if w.get("done") else ""}{" now" if w.get("status")=="now" else ""}" href="#w{w["no"]}" title="第 {w["no"]} 周 · {e(w["author"])}"><i></i><span>{w["no"]}</span></a>' for w in weeks)
lib_cls = lambda s: 'ok' if s.startswith('有') or s.startswith('自有') else ('part' if s.startswith('部分') else 'no')

# ---- 01 十二周：行列表（透镜：按周 / 按书库）
def wk(w):
    st = 'now' if w.get('status') == 'now' else ('done' if w.get('done') else '')
    ep = f'<a class="ep" href="{e(w["ep"])}">听这一期 →</a>' if w.get('ep') else '<span class="ep off">节目待出</span>'
    return (f'<li class="{st}" id="w{w["no"]}" data-lib="{lib_cls(w["lib"])}" data-no="{w["no"]}"><div class="rh">'
            f'<div class="d">{w["date"][5:].replace("-", " / ")}<b>第 {w["no"]} 周</b></div>'
            f'<div><h3>{e(w["author"])}<small>{e(w["work"])}</small></h3><p class="sub">{e(w["read"])}</p>'
            f'<p class="sub"><span class="k">对着</span>{e(w["for"])}<br><span class="k">一页纸</span>{e(w["paper"])}</p></div>'
            f'<div class="meta"><span class="lib {lib_cls(w["lib"])}"><i></i>书库 · {e(w["lib"])}</span>{ep}</div></div></li>')
wks = ''.join(wk(w) for w in weeks)

# ---- 02 脉络：八段（带小图）+ 五条线
spine = ''.join(f'<li class="seg"><div class="sno">{s["no"]:02d}<small>{e(s["era"])}</small></div><div class="sbody"><h3>{e(s["name"])}</h3><p class="who">{e(s["who"])}</p><p class="ln">{e(s["line"])}</p></div><figure class="sfig"><img src="img/s{s["no"]:02d}.jpg" alt="" loading="lazy"><figcaption>{e(IMG["s%02d" % s["no"]]["cap"])}</figcaption></figure></li>' for s in D['spine'])
threads = ''.join(f'<li><b>{e(t["name"])}</b><span>{e(t["path"])}</span></li>' for t in D['threads'])

# ---- 03 书库
lib = D['library']
ul = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)

# ---- 卷末
method = ''.join(f'<li>{e(m)}</li>' for m in D['method'])
credits = ''.join(f'<li>{e(v["credit"])}</li>' for v in IMG.values())

page = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(D["title"])} · 跟着哥大 Contemporary Civilization 书单读十二周 — 天杰</title>
<meta name="description" content="{e(D["subtitle"])} 知识脉络、十二周路径、书库对照、每周节目与一页纸。">
<meta property="og:title" content="{e(D["title"])} · 天杰">
<meta property="og:description" content="{e(D["subtitle"])}">
<meta property="og:image" content="https://tianjie.me/cc/img/hero-athens.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%2304122A'/%3E%3Ctext x='32' y='44' font-size='30' text-anchor='middle' font-family='Noto Serif SC,serif' font-weight='700' fill='%2377C2EF'%3ECC%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap"></noscript>
<script>try{{var t=localStorage.getItem('yzyt-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
<style>
{SKIN}
/* ---------- CC 页专用 */
.hero .grid{{grid-template-columns:minmax(0,11fr) minmax(0,10fr)}}
/* 十二格刻度：本周的「刻度尺」 */
.ruler{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:8px;margin:0 0 48px;padding:0 0 16px;border-bottom:1px solid var(--line)}}
.ruler .tick{{position:relative;display:block;text-decoration:none;padding:12px 0 0;color:var(--muted);font:500 12px/16px var(--sans);text-align:center;transition:color .3s var(--ease)}}
.ruler .tick i{{display:block;height:4px;border-radius:2px;background:var(--line);margin:0 0 8px;transition:background-color .3s var(--ease),box-shadow .3s var(--ease)}}
.ruler .tick.done i{{background:var(--accent-2)}}
.ruler .tick.now i{{background:var(--accent);box-shadow:0 0 10px 1px var(--accent)}}
.ruler .tick.now{{color:var(--accent-ink);font-weight:600}}
.ruler .tick:hover{{color:var(--ink)}}
.nowgrid{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:start}}
.nowgrid .big{{font:700 96px/1 var(--serif);color:var(--ink);letter-spacing:-.02em}}
.nowgrid .big small{{display:block;font:500 14px/20px var(--sans);letter-spacing:.12em;color:var(--accent-ink);margin:0 0 12px}}
.nowgrid .work{{margin:16px 0 0;font:500 24px/32px var(--serif);color:var(--ink-2)}}
.nowgrid dl{{margin:32px 0 0;display:grid;grid-template-columns:5em minmax(0,1fr);gap:8px 16px;font:400 16px/28px var(--sans)}}
.nowgrid dt{{color:var(--muted);font-size:14px;letter-spacing:.06em}}
.nowgrid dd{{margin:0;color:var(--ink-2)}}
.nowgrid dd b{{color:var(--ink);font-weight:500}}
.nowgrid .ha{{margin-top:32px}}
.rh .k{{display:inline-block;min-width:3.5em;color:var(--muted);font-size:13px;letter-spacing:.06em}}
.rh .lib i{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;background:var(--muted);vertical-align:1px}}
.rh .lib.ok i{{background:var(--ok)}}.rh .lib.part i{{background:var(--warn)}}.rh .lib.no i{{background:var(--bad)}}
.rh .ep{{font-weight:600;text-decoration:none}}.rh .ep.off{{color:var(--muted);font-weight:400}}
.rows.bylib>li{{order:3}}.rows.bylib>li[data-lib=ok]{{order:1}}.rows.bylib>li[data-lib=part]{{order:2}}
.rows.lensed{{display:flex;flex-direction:column}}
/* 脉络：八段带小图 */
.spine{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}}
.seg{{display:grid;grid-template-columns:120px minmax(0,1fr) 160px;gap:32px;align-items:start;padding:32px 0;border-bottom:1px solid var(--line)}}
.sno{{font:700 48px/1 var(--serif);color:var(--accent-ink);letter-spacing:-.02em}}
.sno small{{display:block;margin-top:12px;font:500 12px/16px var(--sans);letter-spacing:.08em;color:var(--muted)}}
.sbody h3{{font-size:30px;line-height:36px}}
.sbody .who{{margin:12px 0 0;font:400 15px/24px var(--sans);color:var(--ink-2)}}
.sbody .ln{{margin:8px 0 0;max-width:36em;font:400 16px/28px var(--sans);color:var(--ink)}}
.sfig{{margin:0}}
.sfig img{{display:block;width:160px;height:160px;object-fit:cover;border-radius:4px;background:var(--surface)}}
.sfig figcaption{{margin-top:8px;font:400 11px/16px var(--sans);color:var(--muted)}}
.half{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;margin:0 0 24px;font:400 14px/24px var(--sans);color:var(--muted)}}
.half b{{display:block;color:var(--accent-ink);font:600 12px/16px var(--sans);letter-spacing:.12em;margin-bottom:4px}}
.threads{{list-style:none;margin:48px 0 0;padding:0;border-top:1px solid var(--line)}}
.threads li{{display:grid;grid-template-columns:180px minmax(0,1fr);gap:24px;padding:16px 0;border-bottom:1px solid var(--line);font:400 16px/28px var(--sans)}}
.threads b{{font:700 18px/28px var(--serif);color:var(--ink)}}
.threads span{{color:var(--ink-2)}}
/* 书库 */
.lib3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;border-top:1px solid var(--line);padding-top:32px}}
.lib3 h3{{font-size:20px;line-height:28px;margin-bottom:12px;display:flex;align-items:center;gap:10px}}
.lib3 h3 i{{display:inline-block;width:10px;height:10px;border-radius:50%}}
.lib3 .h h3 i{{background:var(--ok);box-shadow:0 0 8px 1px var(--ok)}}.lib3 .f h3 i{{background:var(--warn)}}.lib3 .b h3 i{{background:var(--bad)}}
.lib3 ul{{margin:0;padding:0;list-style:none;font:400 15px/26px var(--sans);color:var(--ink-2)}}
.lib3 li{{padding:4px 0;border-bottom:1px solid var(--line-2)}}
@media (max-width:980px){{.hero .grid{{grid-template-columns:minmax(0,1fr)}}.nowgrid{{grid-template-columns:minmax(0,1fr)}}.seg{{grid-template-columns:80px minmax(0,1fr)}}.sfig{{grid-column:2}}.lib3{{grid-template-columns:minmax(0,1fr)}}}}
@media (max-width:700px){{.ruler{{gap:4px}}.ruler .tick span{{display:none}}.ruler .tick.now span{{display:block}}.nowgrid .big{{font-size:60px}}.seg{{grid-template-columns:minmax(0,1fr);gap:12px}}.sno{{font-size:36px}}.sfig img{{width:100%;height:auto;aspect-ratio:16/10}}.threads li{{grid-template-columns:minmax(0,1fr);gap:4px}}}}
</style>
</head>
<body>
<div class="sitebar"><div class="wide"><a class="brand" href="/">一周一题</a><span class="tag">长期专题</span><span class="dt">CC 读书会 · 第 {cur["no"]} 周 / 12</span><div class="r"><a href="/listen/">合读</a><a href="/#projects">长期专题</a><a href="/">归档</a></div></div></div>

<header class="band hero">
  <div class="wide grid">
    <div>
      <p class="hk">长期专题 · Contemporary Civilization · 哥伦比亚大学核心课程，1919 年起</p>
      <h1>{e(D["title"])}</h1>
      <p class="hsub">{e(D["subtitle"])}</p>
      <p class="hp">{e(D["intro"])}</p>
      <div class="ha"><a class="btn" href="#now">从这一周开始<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg></a><span class="hm">十二周 · 三十四位作者 · 第 {cur["no"]} 周：{e(cur["author"])}</span></div>
    </div>
    {fig('hero-athens', 'hfig rise', lazy=False)}
  </div>
</header>

<section class="band tagsec" aria-label="论点"><div class="tagstick"><div class="wide"><p class="tagl">{tag}</p><p class="tagrest">{e(th["rest"])}</p></div></div></section>

<nav class="cnav" aria-label="章节"><div class="row" id="cnav">
  <a href="#now"><small>0</small>本周</a>
  <a href="#path"><small>1</small>十二周</a>
  <a href="#spine"><small>2</small>脉络</a>
  <a href="#lib"><small>3</small>书库</a>
  <a href="#end"><small>末</small>方法与来源</a>
  <button class="ntheme" id="themebtn" type="button">白天读</button>
  <i class="prog" id="pageprog"></i>
</div></nav>

<main>
<section class="chap" id="now">
  <div class="wide">
    <div class="ruler" aria-label="十二周进度">{ruler}</div>
    <div class="nowgrid">
      <div class="rise">
        <div class="big"><small>00 · 本周 · {e(cur["date"])}</small>第 {cur["no"]} 周</div>
        <p class="work">{e(cur["author"])}{e(cur["work"])}</p>
        <dl>
          <dt>读</dt><dd><b>{e(cur["read"])}</b></dd>
          <dt>对着</dt><dd>{e(cur["for"])}</dd>
          <dt>一页纸</dt><dd>{e(cur["paper"])}</dd>
          <dt>书库</dt><dd>{e(cur["lib"])}</dd>
        </dl>
        <div class="ha">{'<a class="btn" href="'+e(cur["ep"])+'">听这一期<svg viewBox="0 0 24 24"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>' if cur.get("ep") else ''}<span class="hm">{done_n} / 12 周交了一页纸</span></div>
      </div>
      {fig(cur.get('img', 'wk-leviathan'), 'pimg rise')}
    </div>
  </div>
</section>

<section class="chap" id="path">
  <div class="wide">
    <div class="chead plate">
      <div class="ptext">
        <p class="cno">01 · 十二周<span class="trail"></span></p>
        <h2>按弱点排，<br>不按书单顺序</h2>
        <p class="lede">每周 2–3 小时：听一期节目拿到地图，读指定的章节，做测验，周日前写一页纸。每一周都对着一个手里的决定读，书才留得住。</p>
      </div>
      {fig('plate-academy')}
    </div>
    <div class="lensbar"><span class="lensk">排</span><div class="lens" role="tablist"><button type="button" role="tab" aria-selected="true" data-lens="week">按周</button><button type="button" role="tab" aria-selected="false" data-lens="lib">按书库</button></div><span class="lensnote" id="lensnote">第 1 周到第 12 周</span></div>
    <ul class="rows lensed" id="weeks">{wks}</ul>
    <p class="small" style="margin-top:24px;max-width:48em">{e(D["second"])}</p>
  </div>
</section>

<section class="chap" id="spine">
  <div class="wide">
    <div class="chead plate">
      <div class="ptext">
        <p class="cno">02 · 脉络<span class="trail"></span></p>
        <h2>八段主干，<br>五条纵线</h2>
        <p class="lede">一整年的书单其实在反复追问一件事：一个共同体凭什么成立、凭什么约束我、又把谁算作「我们」。上学期从「秩序是被发现的」走到「秩序是被约定的」；下学期看契约许下的承诺，以及它排除了谁。</p>
      </div>
      {fig('plate-low')}
    </div>
    <div class="half"><div><b>上学期 · 01–05</b>从「秩序是被发现的」到「秩序是被约定的」</div><div><b>下学期 · 06–08</b>契约许下的承诺，以及它排除了谁</div></div>
    <ol class="spine">{spine}</ol>
    <ul class="threads">{threads}</ul>
  </div>
</section>

<section class="chap" id="lib">
  <div class="wide">
    <div class="chead">
      <p class="cno">03 · 书库<span class="trail"></span></p>
      <h2>四十七项必读，<br>库里有十二项</h2>
      <p class="lede">{e(lib["note"])}</p>
    </div>
    <div class="lib3">
      <div class="h"><h3><i></i>库里有（指定篇目）</h3><ul>{ul(lib["have"])}</ul></div>
      <div class="f"><h3><i></i>缺，但公有领域可免费取得</h3><ul>{ul(lib["free"])}</ul></div>
      <div class="b"><h3><i></i>缺，在版权内</h3><ul>{ul(lib["buy"])}</ul></div>
    </div>
  </div>
</section>

<section class="endm" id="end">
  <div class="wide">
    <h2>方法与来源</h2>
    <div class="cols">
      <div><h4>三条方法</h4><ul>{method}</ul></div>
      <div><h4>书单来源</h4><ul><li><a href="{e(D["source"]["course"])}" rel="noopener">课程页</a>（哥伦比亚学院核心课程）</li><li><a href="{e(D["source"]["bulletin"])}" rel="noopener">Bulletin</a>：当前要求的作者与单元</li><li><a href="{e(D["source"]["list"])}" rel="noopener">2021–22 必读书单（PDF）</a>；书单每三年修订一次</li></ul></div>
    </div>
    <details class="fold big"><summary><h3>图片</h3></summary><ul>{credits}</ul></details>
    <div class="seal"><span>© {today.year} Tianjie Sun</span><a href="/">一周一题</a><a href="/listen/">合读</a><a href="/listen/feed.xml">播客 RSS</a></div>
  </div>
</section>
</main>

<script>
(function(){{
const $=s=>document.querySelector(s);
const io=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add("in");io.unobserve(x.target)}}}}),{{threshold:.12}});
document.querySelectorAll(".rise").forEach(el=>io.observe(el));
const tag=$(".tagsec");
if(tag){{const ws=[...tag.querySelectorAll(".w")],rest=tag.querySelector(".tagrest");const upd=()=>{{const r=tag.getBoundingClientRect();const p=Math.min(1,Math.max(0,-r.top/(r.height-innerHeight)));const n=Math.round(p*1.15*ws.length);ws.forEach((w,i)=>w.classList.toggle("on",i<n));if(rest)rest.classList.toggle("on",n>=ws.length)}};addEventListener("scroll",upd,{{passive:true}});upd()}}
const navA=[...document.querySelectorAll("#cnav a")],secs=navA.map(a=>document.querySelector(a.getAttribute("href"))).filter(Boolean);
const upnav=()=>{{let k=0;secs.forEach((s,i)=>{{if(s.getBoundingClientRect().top-64<=0)k=i}});navA.forEach((a,i)=>a.classList.toggle("on",i===k));const d=document.documentElement;$("#pageprog").style.transform=`scaleX(${{Math.min(1,Math.max(0,d.scrollTop/(d.scrollHeight-innerHeight||1)))}})`}};
addEventListener("scroll",upnav,{{passive:true}});upnav();
const r=document.documentElement,b=$("#themebtn");function L(){{b.textContent=r.getAttribute("data-theme")==="light"?"夜里读":"白天读"}}
b.addEventListener("click",()=>{{r.setAttribute("data-theme",r.getAttribute("data-theme")==="light"?"dark":"light");try{{localStorage.setItem("yzyt-theme",r.getAttribute("data-theme"))}}catch(e){{}}L()}});L();
const list=$("#weeks"),note=$("#lensnote");
document.querySelectorAll("[data-lens]").forEach(btn=>btn.addEventListener("click",()=>{{document.querySelectorAll("[data-lens]").forEach(x=>x.setAttribute("aria-selected",x===btn?"true":"false"));list.classList.toggle("bylib",btn.dataset.lens==="lib");note.textContent=btn.dataset.lens==="lib"?"库里有的在前，缺的在后":"第 1 周到第 12 周"}}));
}})();
</script>
</body>
</html>'''
out = os.path.join(ROOT, 'static', 'cc'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
print('static/cc/index.html written; week', cur['no'], 'done', done_n)
