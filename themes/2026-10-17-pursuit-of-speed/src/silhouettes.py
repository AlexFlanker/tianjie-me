# -*- coding: utf-8 -*-
"""程序绘制的载具剪影（viewBox 0 0 600 240，朝右行驶）。只画轮廓与体量，不画商标、不复刻外观细节。
颜色走 CSS 类：.sil 主体、.sil2 次要（窗、舱盖）、.silw 轮、.silk 粗线（肢体）。"""

SIL = {}

# 人：奔跑者（侧面，向右）
SIL['runner'] = '''
<g transform="translate(150,20) scale(1.9)">
<circle class="sil" cx="92" cy="22" r="11"/>
<path class="sil" d="M84 34l14 4 12 14 18-6 4 7-23 10-10-8-4 22 18 16 14 26-8 4-16-24-18-10-10 18-18 14-6-6 16-16 6-22-16 6-16 16-6-5 16-20 20-10z"/>
</g>'''

# 马：奔跑中的马（侧面）
SIL['horse'] = '''
<g transform="translate(40,10)">
<path class="sil" d="M170 90C200 70 260 65 330 80L380 40L390 24L400 32L412 40L440 70L436 84L402 88L392 78L372 98C360 120 350 130 330 135C280 150 220 148 180 140C160 130 160 105 170 90Z"/>
<path class="silk" d="M320 128L372 150L410 196M300 134L300 176L282 206M196 134L140 170L108 200M214 140L206 182L194 212"/>
<path class="silk" d="M172 92L120 74L92 86"/>
</g>'''

# 1829 蒸汽机车（火箭号一类：高烟囱、锅炉、大驱动轮、小煤水车）
SIL['steamloco'] = '''
<g transform="translate(60,30)">
<rect class="sil" x="30" y="90" width="80" height="60" rx="4"/>
<path class="sil2" d="M44 98h26v26H44z"/>
<rect class="sil" x="120" y="80" width="200" height="56" rx="26"/>
<rect class="sil" x="120" y="60" width="48" height="30" rx="6"/>
<rect class="sil" x="330" y="26" width="24" height="100"/>
<path class="sil" d="M322 26h40l8-14h-56z"/>
<rect class="sil" x="110" y="134" width="240" height="24"/>
<rect class="sil" x="30" y="148" width="80" height="12"/>
<path class="sil" d="M180 140l40 20h-80z"/>
<circle class="silw" cx="300" cy="166" r="46"/><circle class="sil2" cx="300" cy="166" r="32"/><circle class="sil" cx="300" cy="166" r="9"/>
<circle class="silw" cx="150" cy="178" r="26"/><circle class="sil2" cx="150" cy="178" r="15"/>
<circle class="silw" cx="52" cy="182" r="22"/><circle class="sil2" cx="52" cy="182" r="12"/>
<circle class="silw" cx="96" cy="182" r="22"/><circle class="sil2" cx="96" cy="182" r="12"/>
<path class="sil" d="M352 150l34 8v-16z"/>
</g>'''

# 1899 电动纪录车：鱼雷形车身架在四个辐条轮上
SIL['torpedo'] = '''
<g transform="translate(60,50)">
<path class="sil" d="M60 110c0-40 40-60 120-60h220c60 0 100 20 110 50 4 12-6 22-20 22H80c-14 0-20-4-20-12z"/>
<path class="sil2" d="M250 50l30-26h60l10 26z"/>
<circle class="silw" cx="130" cy="132" r="38"/><circle class="sil2" cx="130" cy="132" r="26"/><circle class="sil" cx="130" cy="132" r="7"/>
<circle class="silw" cx="420" cy="132" r="38"/><circle class="sil2" cx="420" cy="132" r="26"/><circle class="sil" cx="420" cy="132" r="7"/>
<path class="sil" d="M100 110h360v8H100z"/>
</g>'''

# 1909 纪录赛车：长车头、外露大轮、驾驶员
SIL['racer1909'] = '''
<g transform="translate(40,50)">
<path class="sil" d="M70 120c0-10 6-16 16-16h90l30-40h170c40 0 110 14 150 30 14 6 18 12 18 22 0 8-6 14-16 14H90c-12 0-20-4-20-10z"/>
<path class="sil2" d="M210 62l24-30h80l6 30z"/>
<circle class="sil" cx="236" cy="48" r="12"/>
<path class="sil" d="M200 100h20v-30h-20z"/>
<circle class="silw" cx="130" cy="138" r="40"/><circle class="sil2" cx="130" cy="138" r="27"/><circle class="sil" cx="130" cy="138" r="8"/>
<circle class="silw" cx="440" cy="138" r="40"/><circle class="sil2" cx="440" cy="138" r="27"/><circle class="sil" cx="440" cy="138" r="8"/>
<path class="sil" d="M520 112l40-6v12l-40 4z"/>
</g>'''

# 高速动车组（复兴号一类：长车体、长斜鼻）
SIL['bullettrain'] = '''
<g transform="translate(20,70)">
<path class="sil" d="M20 50c0-14 10-22 24-22h330c70 0 130 14 180 44 12 8 10 20-6 20H30c-8 0-10-4-10-10z"/>
<path class="sil2" d="M60 44h30v18H60zM110 44h30v18h-30zM160 44h30v18h-30zM210 44h30v18h-30zM260 44h30v18h-30zM310 44h30v18h-30z"/>
<path class="sil2" d="M400 42c40 2 80 10 110 24H400z"/>
<rect class="sil" x="16" y="92" width="540" height="10"/>
<circle class="silw" cx="80" cy="112" r="12"/><circle class="silw" cx="130" cy="112" r="12"/><circle class="silw" cx="420" cy="112" r="12"/><circle class="silw" cx="470" cy="112" r="12"/>
</g>'''

# 三点式喷气水翼艇（Spirit of Australia 一类）
SIL['hydroplane'] = '''
<g transform="translate(40,60)">
<path class="sil" d="M60 120c40-10 120-18 200-18h180c40 0 70 6 90 14 10 4 8 14-4 14H70c-14 0-18-6-10-10z"/>
<path class="sil" d="M120 102l-40-40 80 8 30 32z"/>
<path class="sil" d="M330 102l-30-44 70 6 40 38z"/>
<path class="sil" d="M240 102l20-50h50l24 50z"/>
<path class="sil2" d="M262 72l12-14h30l8 14z"/>
<path class="sil" d="M80 130l-30 30 60 0 20-30z"/>
<path class="sil" d="M460 130l-10 30 60 0 20-30z"/>
<path class="sil" d="M400 90c-10-16 10-50 40-50 20 0 30 20 24 40z"/>
</g>'''

# TGV：动力车头（钝锥鼻、受电弓）
SIL['tgv'] = '''
<g transform="translate(20,60)">
<path class="sil" d="M20 60c0-12 8-20 20-20h330c60 0 120 16 170 40 10 6 10 20-4 20H30c-8 0-10-4-10-10z"/>
<path class="sil2" d="M60 52h40v18H60zM120 52h40v18h-40zM180 52h40v18h-40zM240 52h40v18h-40z"/>
<path class="sil2" d="M380 50c40 2 80 12 110 28H380z"/>
<path class="sil" d="M300 40l30-26h60l-20 26z"/>
<rect class="sil" x="16" y="102" width="540" height="10"/>
<circle class="silw" cx="90" cy="122" r="14"/><circle class="silw" cx="150" cy="122" r="14"/><circle class="silw" cx="400" cy="122" r="14"/><circle class="silw" cx="460" cy="122" r="14"/>
</g>'''

# 磁浮列车（低矮、长鼻、抱轨）
SIL['maglev'] = '''
<g transform="translate(20,80)">
<path class="sil" d="M20 56c0-10 8-16 18-16h320c80 0 150 10 200 36 8 4 6 12-4 12H30c-8 0-10-4-10-8z"/>
<path class="sil2" d="M60 48h50v14H60zM130 48h50v14h-50zM200 48h50v14h-50zM270 48h50v14h-50z"/>
<rect class="sil" x="20" y="90" width="540" height="8"/>
<rect class="sil2" x="60" y="98" width="460" height="10"/>
</g>'''

# 喷气客机
SIL['airliner'] = '''
<g transform="translate(40,40)">
<path class="sil" d="M60 110c0-10 8-16 20-16h380c40 0 70 8 86 20 6 4 4 12-4 12H80c-12 0-20-6-20-16z"/>
<path class="sil" d="M80 94l40-60h40l-20 60z"/>
<path class="sil" d="M180 108l-80 60h60l120-60z"/>
<path class="sil" d="M300 108l-40 40h30l60-40z"/>
<path class="sil" d="M250 126h60v16h-60z"/>
<path class="sil2" d="M160 100h12v8h-12zM180 100h12v8h-12zM200 100h12v8h-12zM220 100h12v8h-12zM240 100h12v8h-12zM260 100h12v8h-12zM280 100h12v8h-12zM300 100h12v8h-12zM320 100h12v8h-12zM340 100h12v8h-12zM360 100h12v8h-12zM380 100h12v8h-12zM400 100h12v8h-12z"/>
<path class="sil2" d="M470 96l40 2c6 0 10 4 10 8h-56z"/>
</g>'''

# 火箭试验机（X-1 一类：子弹形机身、平直翼、尾翼）
SIL['rocketplane'] = '''
<g transform="translate(40,60)">
<path class="sil" d="M60 90c0-20 40-36 120-36h220c60 0 110 14 130 36 0 18-50 34-130 34H180c-80 0-120-16-120-34z"/>
<path class="sil" d="M60 60l50-40h50l-20 40z"/>
<path class="sil" d="M60 112l10 30h60l-20-30z"/>
<path class="sil" d="M240 118l-40 46h60l30-46z"/>
<path class="sil" d="M240 60l-20-26h50l20 26z"/>
<path class="sil2" d="M380 62l40-4c8 0 14 4 16 10h-56z"/>
</g>'''

# 超音速陆地纪录车（Thrust SSC 一类：针形车身、双侧发动机、垂直尾翼）
SIL['jetcar'] = '''
<g transform="translate(20,70)">
<path class="sil" d="M20 86c0-6 4-10 10-10h330c80 0 150 2 200 6 8 1 8 8 0 9-50 4-120 6-200 6H30c-6 0-10-5-10-11z"/>
<path class="sil" d="M110 76c0-14 10-22 26-22h140c16 0 26 8 26 22z"/>
<path class="sil" d="M110 97c0 14 10 22 26 22h140c16 0 26-8 26-22z"/>
<path class="sil" d="M60 76l40-50h40l-30 50z"/>
<path class="sil2" d="M330 78l30-8h30l-20 8z"/>
<circle class="silw" cx="90" cy="124" r="10"/><circle class="silw" cx="300" cy="124" r="10"/><circle class="silw" cx="420" cy="118" r="8"/>
</g>'''

# 超音速客机（三角翼、下垂机头）
SIL['concorde'] = '''
<g transform="translate(30,50)">
<path class="sil" d="M40 100c0-8 6-12 14-12h300c90 0 150 2 200 10l-40 12H54c-8 0-14-4-14-10z"/>
<path class="sil" d="M80 88l20-56h30l-6 56z"/>
<path class="sil" d="M160 110l-100 52h200l180-52z"/>
<path class="sil" d="M200 126h50v14h-50zM260 126h50v14h-50z"/>
<path class="sil2" d="M500 98l54 8-14-14z"/>
</g>'''

# 高空高速侦察机（SR-71 一类：扁长机身、双发动机舱、斜置双垂尾）
SIL['blackbird'] = '''
<g transform="translate(20,60)">
<path class="sil" d="M20 100c0-6 4-10 10-10h340c60 0 130 2 190 6l-20 14H30c-6 0-10-4-10-10z"/>
<path class="sil" d="M120 90l80-40h60l-60 40zM120 110l80 40h60l-60-40z"/>
<path class="sil" d="M110 86c0-10 8-16 20-16h60c12 0 20 6 20 16zM110 114c0 10 8 16 20 16h60c12 0 20-6 20-16z"/>
<path class="sil" d="M60 86l20-40h30l-10 40z"/>
<path class="sil2" d="M420 94l80 4-20 6h-60z"/>
<path class="sil" d="M240 100l200-6-200 12z"/>
</g>'''

# X-15：短翼火箭飞机、楔形垂尾
SIL['x15'] = '''
<g transform="translate(40,70)">
<path class="sil" d="M40 90c0-10 10-18 26-18h260c80 0 150 6 200 18-50 12-120 18-200 18H66c-16 0-26-8-26-18z"/>
<path class="sil" d="M60 72l20-44h50l-20 44zM60 108l20 44h50l-20-44z"/>
<path class="sil" d="M240 108l-30 30h60l40-30zM240 72l-20-24h50l30 24z"/>
<path class="sil2" d="M400 76l60 2c10 1 16 6 18 12h-78z"/>
</g>'''

# 返回舱（锥形舱 + 防热大底 + 等离子尾焰）
SIL['capsule'] = '''
<g transform="translate(120,40)">
<path class="sil" d="M300 40l60 60v40l-60 60H140c-20 0-30-10-30-30V70c0-20 10-30 30-30z"/>
<path class="sil2" d="M360 100l40 4v32l-40 4z"/>
<path class="sil" d="M110 70l-80 50 80 50z" opacity=".45"/>
<path class="sil" d="M30 120l-90 10v-20z" opacity=".25"/>
<circle class="sil2" cx="240" cy="120" r="12"/>
</g>'''

# 探测器（六棱舱体 + 防热盾 + 天线臂）
SIL['probe'] = '''
<g transform="translate(120,40)">
<path class="sil" d="M220 60l50 30v60l-50 30h-80l-50-30V90l50-30z"/>
<path class="sil" d="M300 56l30 8v112l-30 8z"/>
<path class="sil2" d="M330 64l24 4v104l-24 4z"/>
<path class="sil" d="M90 120h-70v-8h70zM90 108h-90v-6h90z"/>
<path class="sil" d="M170 60l-30-40h20l20 40zM170 180l-30 40h20l20-40z"/>
<circle class="sil2" cx="180" cy="120" r="14"/>
</g>'''

# 光：一束光线
SIL['light'] = '''
<g transform="translate(40,60)">
<path class="sil" d="M20 120h480v8H20z"/>
<path class="sil" d="M60 92h380v6H60zM60 142h380v6H60z" opacity=".55"/>
<path class="sil" d="M120 66h280v4H120zM120 170h280v4H120z" opacity=".3"/>
<path class="sil" d="M500 100l60 24-60 24z"/>
</g>'''

def svg(key, cls='silsvg'):
    body = SIL[key]
    return f'<svg class="{cls}" viewBox="0 0 600 240" aria-hidden="true">{body}</svg>'
