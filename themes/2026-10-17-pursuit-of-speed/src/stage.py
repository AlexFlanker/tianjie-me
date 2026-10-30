# -*- coding: utf-8 -*-
"""第 5 题 v2 序章「十九级阶梯」：全屏舞台的 HTML 骨架与给 app.js 的数据。
照片按原尺寸为上限放进右侧图版（不放大小图），背后是同一张照片的模糊底；左侧玻璃卡片放名字、速度、对数小表盘、短句与规格；
底部尺子两排：上排是对数刻度上的真实位置，下排是十九级等距排开（拖动、甩动、方向键），两排之间用细线连起来。"""
import math, html, re
import journey
import editorial as E
import editorial2 as E2

esc = lambda s: html.escape(str(s), quote=True)
LO, HI = journey.LO, journey.HI
SUP = journey.SUP

def lic_short(s):
    s = s or ''
    if 'No known copyright' in s or '无已知版权限制' in s: return '无已知版权限制'
    if 'CC0' in s: return 'CC0'
    if 'BY-SA' in s: return 'CC BY-SA 2.0'
    if 'CC BY 2.0' in s: return 'CC BY 2.0'
    return '公有领域'
def author_short(s):
    s = re.sub(r'（.*?）', '', s or '').strip()
    return s if len(s) <= 40 else s[:40] + '…'
def credit(im): return f'图：{author_short(im["author"])}，{lic_short(im["license"])}。'

def frac(v): return (math.log10(v) - LO) / (HI - LO)

def dial_svg():
    """小对数表盘：270° 弧，10⁰–10⁹·³；红区 = Apollo 10 以上（没有人乘坐过）。指针由 app.js 转。"""
    cx = cy = 50; r = 40; a0, a1 = 135, 405
    def pt(f, rr):
        a = math.radians(a0 + f * (a1 - a0)); return cx + rr * math.cos(a), cy + rr * math.sin(a)
    def arc(f0, f1, rr):
        x0, y0 = pt(f0, rr); x1, y1 = pt(f1, rr); large = 1 if (f1 - f0) * (a1 - a0) > 180 else 0
        return f'M{x0:.2f},{y0:.2f} A{rr},{rr} 0 {large} 1 {x1:.2f},{y1:.2f}'
    out = ['<svg class="tldial" viewBox="0 0 100 100" aria-hidden="true">', f'<path class="dtrack" d="{arc(0, 1, r)}"/>',
           f'<path class="dred" d="{arc(frac(39897), 1, r)}"/>', f'<path class="dfill" id="tldfill" d="{arc(0, 1, r)}" pathLength="1"/>']
    for d in range(0, 10):
        f = (d - LO) / (HI - LO); x0, y0 = pt(f, r - 7); x1, y1 = pt(f, r + 1)
        out.append(f'<line class="dtk" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>')
    out.append('<g class="dneedle" id="tlneedle"><line x1="50" y1="50" x2="50" y2="17"/><circle cx="50" cy="50" r="5"/></g></svg>')
    return ''.join(out)

def levels(IM, caption_of, src_lookup):
    out = []
    for i, L in enumerate(journey.LEVELS):
        L = dict(L, **E2.STAGE_FIX.get(L['id'], {}))
        im = IM.get(L['photo']) if L.get('photo') else None
        srch, confh = src_lookup(L['src'])
        cap = caption_of(L['photo'], im) if im else ''
        out.append(dict(id=L['id'], name=L['name'], short=E2.STAGE_SHORT.get(L['id'], L['name']), kmh=L['kmh'], f=round(frac(L['kmh']), 5),
                        kick=f'{L["cls"]} · {L["year"]}' if L['year'] != '—' else L['cls'], who=L['who'], tag=L['tag'], specs=[list(x) for x in L['specs']],
                        src=srch, conf=confh, big=journey.fmt(L['kmh']),
                        img=('assets/' + im['file']) if im else '', w=im.get('w') if im else 0, h=im.get('h') if im else 0,
                        alt=im['subject'] if im else '', cap=cap, cred=credit(im) if im else ''))
    return out

def stage(IM, caption_of, src_lookup):
    LV = levels(IM, caption_of, src_lookup); N = len(LV); s0 = LV[0]
    specs0 = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in s0['specs'])
    # 尺子：上排对数刻度（十个数量级），下排十九级等距
    dec = ''.join(f'<span class="rdec" style="left:{(d - LO) / (HI - LO) * 100:.3f}%"><i></i><em>10{SUP[str(d)]}</em></span>' for d in range(0, 10))
    dots = ''.join(f'<span class="rdot" data-k="{k}" style="left:{L["f"] * 100:.3f}%"></span>' for k, L in enumerate(LV))
    marks = ''.join(f'<button type="button" class="rmark{" edge" if k in (0, N - 1) else ""}" data-step="{k}" style="left:{k / (N - 1) * 100:.3f}%" '
                    f'aria-label="第 {k + 1} 级：{esc(L["name"])}，{esc(L["big"])} km/h"><i></i><span>{esc(L["short"])}</span></button>' for k, L in enumerate(LV))
    pic0 = (f'<img class="on" id="tlp0" src="{esc(s0["img"])}" alt="{esc(s0["alt"])}" width="{s0["w"]}" height="{s0["h"]}" decoding="async">'
            '<img id="tlp1" alt="" decoding="async">')
    bg0 = f'<img class="on" id="tlbg0" src="{esc(s0["img"])}" alt=""><img id="tlbg1" alt="">'
    light = '<div class="tlc" id="tlc" aria-hidden="true"><b>c</b><span>299,792,458 m/s</span><small>光速 · SI 定义值</small></div>'
    card = (f'<aside class="tlcard glass" id="tlcard" aria-live="polite">'
            f'<div class="tlhd"><span class="tlno" id="tlno">01 / {N:02d}</span><span id="tlkick">{esc(s0["kick"])}</span></div>'
            f'<h3 class="tlname" id="tlname">{esc(s0["name"])}</h3>'
            f'<div class="tlspd"><p class="tlbig"><b id="tlbig">{esc(s0["big"])}</b><small>km/h</small></p>{dial_svg()}</div>'
            f'<p class="tlalt" id="tlalt"></p>'
            f'<p class="tltext" id="tltext">{esc(s0["tag"])}</p>'
            f'<dl class="tlspecs" id="tlspecs">{specs0}</dl>'
            f'<p class="tlwho" id="tlwho">{esc(s0["who"])} {s0["conf"]}</p>'
            f'<div class="tlsrc" id="tlsrc">{s0["src"]}</div></aside>')
    ruler = (f'<div class="tlruler glass" id="tlruler" role="slider" tabindex="0" aria-label="十九级：拖动、甩动或用方向键" aria-valuemin="0" aria-valuemax="{N - 1}" '
             f'aria-valuenow="0" aria-valuetext="第 1 级：{esc(s0["name"])}，{esc(s0["big"])} km/h">'
             f'<div class="rin"><div class="rlog" id="rlog" aria-hidden="true"><span class="rlline"></span>{dec}{dots}<span class="rlp" id="rlp"></span><b class="rlu">km/h · 对数</b></div>'
             f'<svg class="rfan" id="rfan" aria-hidden="true"></svg>'
             f'<div class="rtrack" id="rtrack"><span class="rline"></span>{marks}<span class="rhead" id="rhead"><i></i></span></div></div></div>')
    plate = (f'<figure class="tlplate" id="tlplate"><div class="tlpics" id="tlpics">{pic0}{light}</div>'
             f'<figcaption class="tlcap" id="tlcap"><span class="cs" id="tlcs">{esc(s0["cap"])}</span><span class="cr" id="tlcr">{esc(s0["cred"])}</span></figcaption></figure>')
    steps_sr = ''.join(f'<li><b>{esc(L["name"])} · {esc(L["big"])} km/h</b> {esc(L["tag"])}</li>' for L in LV)
    return (f'<div class="tlpin" id="tlpin"><div class="tlstage" id="tlstage"><div class="tlbg" aria-hidden="true">{bg0}</div>'
            f'<p class="tlhint" aria-hidden="true">00 · 序章 · 十九级阶梯 · 拖底部的尺子，或往下滚</p>{plate}{card}{ruler}</div></div><ol class="sr-only" id="tlsr">{steps_sr}</ol>')

def data(IM, caption_of, src_lookup):
    return levels(IM, caption_of, src_lookup)
