# -*- coding: utf-8 -*-
"""动手章：纬度墙与算日子的 HTML 骨架；逻辑在 demos.js。"""
import html
esc = lambda s: html.escape(str(s), quote=True)


def wall_lat():
    return '''<div class="demo" id="wl-latwall">
<div class="dstage dragx" id="wl-stage" role="slider" tabindex="0" aria-label="在图上左右拖动选日期" aria-valuemin="1" aria-valuemax="365" aria-valuenow="311" aria-valuetext="11 月 7 日"><svg class="dsvg" id="wl-svg" viewBox="0 0 640 230" aria-label="该纬度一年的昼长曲线"></svg></div>
<label class="dsl"><span>纬度</span><input type="range" id="wl-lat" min="-60" max="66" step="1" value="40"><output id="wl-lat-o">北纬 40°</output></label>
<div class="dread"><div><b id="wl-dl">—</b><span>昼长 · <em id="wl-doy-o">11 月 7 日</em></span></div><div><b id="wl-set">—</b><span>日落（经度 0° 平太阳时）</span></div><div><b id="wl-night">—</b><span>夜占一天的</span></div></div>
<div class="latlist" id="wl-list"></div>
</div>'''


def tool_dates():
    return '''<div class="demo" id="tl-dates">
<div class="frow"><label>年份 <input type="number" id="td-year" min="1900" max="2100" value="2026" style="width:6.5em"></label><button type="button" class="dgo" id="td-go">算</button><button type="button" class="dgo o" id="td-prev">前一年</button><button type="button" class="dgo o" id="td-next">后一年</button><span class="small" id="td-note"></span></div>
<p class="tdmoon" id="td-moon"></p>
<div class="tblwrap"><table class="dtab" id="td-tab"><thead><tr><th>节日</th><th>日期</th><th>星期</th><th>怎么定的</th></tr></thead><tbody></tbody></table></div>
</div>'''
