# -*- coding: utf-8 -*-
"""五面墙与四个小工具的 HTML 骨架；逻辑在 demos.js。"""
import html
esc = lambda s: html.escape(str(s), quote=True)

def slider(id_, label, mn, mx, step, val, unit=''):
    return f'<label class="dsl"><span>{esc(label)}</span><input type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}"><output for="{id_}" id="{id_}-o" data-unit="{esc(unit)}">{val}{esc(unit)}</output></label>'
def chips(items, attr='data-v', pressed=None):
    return '<div class="dchips">' + ''.join(f'<button type="button" {attr}="{esc(v)}"{" aria-pressed=\"true\"" if v == pressed else " aria-pressed=\"false\"" if pressed is not None else ""}>{esc(n)}</button>' for n, v in items) + '</div>'
def readouts(items):
    return '<div class="dread">' + ''.join(f'<div><b id="{i}">–</b><span>{esc(l)}</span></div>' for i, l in items) + '</div>'

# ---------- 墙 1 一年不是整数天
def wall_leap():
    return f'''<div class="demo" data-demo="leap">
{chips([('不置闰（365）', 'none'), ('4 年 1 闰 · 儒略', 'jul'), ('400 年 97 闰 · 格里', 'greg'), ('33 年 8 闰 · 贾拉里 / 伊朗', 'jal'), ('128 年 31 闰', 'c128'), ('19 年 7 闰 · 阴阳历', 'met')], 'data-rule', 'jul')}
<div class="dstage"><div class="months" id="lp-months"></div><div class="eqmark" id="lp-mark"><i></i><b>春分</b></div><div class="hud2"><b id="lp-date">3 月 21 日</b><span id="lp-drift">漂了 0 天</span></div></div>
{slider('lp-y', '过了多少年', 0, 3000, 1, 400, ' 年')}
{readouts([('lp-mean', '该闰法平均年（日）'), ('lp-err', '每年多出'), ('lp-day', '多少年差一天')])}</div>'''

# ---------- 墙 2 阴历漂移
def wall_lunar():
    return f'''<div class="demo" data-demo="lunar">
<div class="dstage"><div class="ring" id="ln-ring"><svg viewBox="0 0 200 200"><circle class="rt" cx="100" cy="100" r="78"/><g id="ln-seasons"></g><g id="ln-isl"><circle class="pt-isl" r="7"/></g><g id="ln-cn"><circle class="pt-cn" r="7"/></g><g id="ln-heb"><circle class="pt-heb" r="7"/></g><text class="rc" x="100" y="96" text-anchor="middle" id="ln-yr">2026</text><text class="rc2" x="100" y="116" text-anchor="middle">公历年里的位置</text></svg></div>
<div class="ringkey"><span><i class="k-isl"></i>斋月开始（伊斯兰历 · 算表历）</span><span><i class="k-cn"></i>春节（中国农历）</span><span><i class="k-heb"></i>犹太新年（希伯来历）</span></div></div>
{slider('ln-y', '公历年', 2000, 2060, 1, 2026, '')}
{readouts([('ln-r1', '斋月开始'), ('ln-r2', '春节'), ('ln-r3', '犹太新年')])}
<p class="small" id="ln-note"></p></div>'''

# ---------- 墙 3 均时差
def wall_eot():
    return f'''<div class="demo" data-demo="eot">
<div class="dstage eotst"><svg class="dsvg" viewBox="0 0 600 190" id="eo-svg"><line class="ln" x1="40" y1="95" x2="560" y2="95"/><path class="o2 d" id="eo-curve" d=""/><g id="eo-an"></g><circle id="eo-dot" class="pt3" r="6" cx="40" cy="95"/><text class="dt" x="40" y="185">1 月</text><text class="dt" x="300" y="185" text-anchor="middle">7 月</text><text class="dt" x="560" y="185" text-anchor="end">12 月</text><text class="dt" x="44" y="30">日晷比钟表快</text><text class="dt" x="44" y="176">日晷比钟表慢</text></svg></div>
{slider('eo-d', '一年中的第几天', 1, 365, 1, 297, '')}
{readouts([('eo-date', '日期'), ('eo-eot', '均时差'), ('eo-sun', '日晷 12:00 时钟表读数')])}</div>'''

# ---------- 墙 4 你的正午（与工具 ② 共用骨架）
def wall_noon(pid='nn'):
    cities = [('乌鲁木齐 · 北京时间', '87.6|8|乌鲁木齐'), ('北京', '116.4|8|北京'), ('马德里 · 中欧时间', '-3.7|1|马德里'), ('里斯本', '-9.14|0|里斯本'), ('伦敦', '-0.13|0|伦敦'), ('纽约', '-74.01|-5|纽约'), ('德里 · +5:30', '77.21|5.5|德里'), ('加德满都 · +5:45', '85.32|5.75|加德满都'), ('东京', '139.69|9|东京'), ('墨西哥城', '-99.13|-6|墨西哥城')]
    return f'''<div class="demo" data-demo="noon" id="noon-{pid}">
{chips(cities, 'data-city')}
<div class="frow"><label>经度 <input type="number" id="{pid}-lon" step="0.01" value="87.6" style="width:7em"> °</label><label>时区 UTC <input type="number" id="{pid}-tz" step="0.25" value="8" style="width:5em"></label><label>日期 <input type="date" id="{pid}-date" value="2026-10-24"></label></div>
<div class="dstage noonst"><div class="sunbar"><div class="sunclock" id="{pid}-clock"></div><div class="noonlab"><b id="{pid}-noon">13:54</b><span>真太阳正午在当地钟表的时刻</span></div></div></div>
{readouts([(pid + '-r1', '时区中央经线'), (pid + '-r2', '经度带来的差'), (pid + '-r3', '今天的均时差')])}</div>'''

# ---------- 墙 5 自转不稳
def wall_lod(dt_svg):
    return f'''<div class="demo" data-demo="lod">
<div class="dstage dtst">{dt_svg}<div class="dtcur" id="lod-cur"></div></div>
{slider('lod-y', '年份', 1900, 2030, 1, 2026, '')}
{readouts([('lod-dt', 'ΔT（秒）'), ('lod-ls', '到这一年为止的闰秒'), ('lod-lod', '这一年的日长 − 86,400 s')])}
<p class="small">ΔT 取 USNO deltat.data 的年初值并线性内插；日长（LOD）为 IERS 年均值的近似，2024-07-05 单日 −1.66 ms 为原子钟时代最短的一天；2030 年后为示意，不是预报。</p></div>'''

# ---------- 工具 ① 历法换算器
def tool_conv():
    return f'''<div class="demo tconv" data-demo="conv">
<div class="frow"><label>公历日期 <input type="date" id="cv-date" value="2026-10-24" min="1900-01-01" max="2100-12-31"></label><button type="button" class="dgo" id="cv-today">今天</button><span class="small">也可以直接改下面任一历法的字段反推。</span></div>
<div class="cvgrid" id="cv-grid"></div>
<p class="small">农历按 GB/T 33661-2017 规则（北京时间日界）预算的 1900–2100 月表；伊斯兰历为算表历（民用口径），与各地观月可差一天；伊朗太阳历按 33 年周期规则，1370–1409 年与官方历逐年对过；玛雅长纪历取相关常数 584283（另说 584285）。算法说明见卷末。</p></div>'''

# ---------- 工具 ③ 拨表换算
def tool_dst(cities_opts):
    return f'''<div class="demo tdst" data-demo="dst">
<div class="frow"><select id="ds-a">{cities_opts}</select><span class="small">↔</span><select id="ds-b">{cities_opts}</select><label>日期 <input type="date" id="ds-date" value="2026-10-24"></label></div>
<div class="dstage dsst"><div class="dsrow" id="ds-row"></div></div>
{readouts([('ds-diff', '时差'), ('ds-a-st', '甲地状态'), ('ds-b-st', '乙地状态')])}
<p class="small" id="ds-note"></p></div>'''

# ---------- 工具 ④ 闰秒年表
def tool_leaps():
    return f'''<div class="demo tleap" data-demo="leaps">
<div class="frow"><label>出生年 <input type="number" id="ls-y" min="1900" max="2026" value="1985" style="width:6em"></label><span class="small" id="ls-sum"></span></div>
<div class="dstage lsst"><div class="lsbar" id="ls-bar"></div><svg class="dsvg" viewBox="0 0 600 120" id="ls-proj"></svg></div>
<p class="small">2027-05-20 以后 UT1−UTC 不再归零：虚线按 1972–2016 的平均速率（约 0.6 s / 年）外推，到 2100 年约 −44 s；实线按 2016–2025 的近零速率（约 0.1 s / 年）。1 小时的上限在图外很远的下方；真实曲线由 IERS 逐年公布，这里只是示意。</p>
<ol class="lslist" id="ls-list"></ol></div>'''
