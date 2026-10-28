# -*- coding: utf-8 -*-
"""两面墙与三个小工具的 HTML 骨架；逻辑在 demos.js。"""
import html
esc = lambda s: html.escape(str(s), quote=True)

def wall_lat():
    return '''<div class="demo" id="wl-latwall">
<div class="dstage"><svg class="dsvg" id="wl-svg" viewBox="0 0 640 230" aria-label="该纬度一年的昼长曲线"></svg></div>
<label class="dsl"><span>纬度</span><input type="range" id="wl-lat" min="-60" max="66" step="1" value="40" data-unit="°"><output id="wl-lat-o">北纬 40°</output></label>
<label class="dsl"><span>日期</span><input type="range" id="wl-doy" min="1" max="365" step="1" value="311" data-unit=""><output id="wl-doy-o">11 月 7 日</output></label>
<div class="dread"><div><b id="wl-dl">—</b><span>昼长</span></div><div><b id="wl-set">—</b><span>日落（经度 0° 平太阳时）</span></div><div><b id="wl-night">—</b><span>夜占一天的</span></div></div>
<div class="latlist" id="wl-list"></div>
</div>'''

def wall_wheel(wheel_svg):
    return f'''<div class="demo" id="wl-wheel">
<div class="dchips" id="ww-chips" role="group" aria-label="把谁的岁首转到顶上">
<button type="button" data-doy="1" aria-pressed="true">公历 1/1</button><button type="button" data-doy="48">春节（2026 · 2/17）</button><button type="button" data-doy="313">秦十月朔（十月初一）</button>
<button type="button" data-doy="313">古吉拉特新年（排灯节次日）</button><button type="button" data-doy="314">尼泊尔历元旦（Mha Puja）</button><button type="button" data-doy="103">泰国宋干（4/13）</button><button type="button" data-doy="304">Samhain 之说（11/1）</button>
</div>
<div class="dstage wheelst">{wheel_svg}</div>
<p class="small" style="margin:0">底色标出两道门槛：夏末（7 月下旬–9 月中）与冬初（10 月下旬–11 月下旬）。虚线圈 = 跟月亮走的节日，实线圈 = 公历固定日，点在圈上 = 跟太阳走。点一个节日跳到它的卡片。</p>
</div>'''

def tool_dates():
    return '''<div class="demo" id="tl-dates">
<div class="frow"><label>年份 <input type="number" id="td-year" min="1900" max="2100" value="2026" style="width:6.5em"></label><button type="button" class="dgo" id="td-go">算</button><button type="button" class="dgo o" id="td-next">明年</button><span class="small" id="td-note"></span></div>
<div class="tblwrap"><table class="dtab" id="td-tab"><thead><tr><th>节日</th><th>日期</th><th>星期</th><th>怎么定的</th></tr></thead><tbody></tbody></table></div>
<p class="small" id="td-moon" style="margin:6px 0 0"></p>
</div>'''

def tool_pair(opts):
    return f'''<div class="demo" id="tl-pair">
<div class="frow"><label>甲 <select id="tp-a">{opts}</select></label><label>乙 <select id="tp-b">{opts}</select></label></div>
<div class="pairg"><div class="pcard" id="tp-ca"></div><div class="pcard" id="tp-cb"></div></div>
</div>'''

def tool_list(opts):
    return f'''<div class="demo" id="tl-list">
<div class="frow"><label>今年想去 <select id="tls-sel">{opts}</select></label><button type="button" class="dgo o" id="tls-copy">复制文字</button><span class="small" id="tls-msg"></span></div>
<div class="lst" id="tls-out"></div>
</div>'''
