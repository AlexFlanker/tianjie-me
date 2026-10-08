# -*- coding: utf-8 -*-
"""示意图的公共画法：一个很小的 SVG 生成器，加工程图里常用的几样东西（尺寸线、引线、比例尺、人形）。

颜色一律走 CSS 类（见 template.html 里的 .dwg），这里不写任何十六进制色值，深浅色主题才能跟着切换。
线型约定：o 轮廓线，o1 / o2 细线，d 虚线（看不见的、计划中的、参照物），a 强调线（光、束流、探测介质），
dim 尺寸线；fa 强调色淡填充，fs 纸面填充（用来遮住后面的线）。
"""
import html
import math


def esc(s):
    return html.escape(str(s), quote=True)


def f(x):
    """坐标保留一位小数，去掉多余的 0。"""
    s = f'{x:.1f}'
    return s[:-2] if s.endswith('.0') else s


class Svg:
    def __init__(self, w=600, h=430, cls='dwg', title=''):
        self.w, self.h, self.cls, self.title = w, h, cls, title
        self.el = []

    # ---- 基本图元
    def add(self, s):
        self.el.append(s)
        return self

    def line(self, x1, y1, x2, y2, c='o'):
        return self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{c}"/>')

    def rect(self, x, y, w, h, c='o', rx=0):
        r = f' rx="{f(rx)}"' if rx else ''
        return self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"{r} class="{c}"/>')

    def circle(self, cx, cy, r, c='o'):
        return self.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="{c}"/>')

    def ellipse(self, cx, cy, rx, ry, c='o'):
        return self.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" class="{c}"/>')

    def path(self, d, c='o'):
        return self.add(f'<path d="{d}" class="{c}"/>')

    def poly(self, pts, c='o', close=True):
        d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ('Z' if close else '')
        return self.path(d, c)

    def text(self, x, y, s, c='t', anchor='start', rot=None):
        a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
        r = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot is not None else ''
        return self.add(f'<text x="{f(x)}" y="{f(y)}" class="{c}"{a}{r}>{esc(s)}</text>')

    def lines(self, x, y, rows, c='t', anchor='start', lh=17):
        """多行文字，rows 是字符串列表。"""
        for i, s in enumerate(rows):
            self.text(x, y + i * lh, s, c, anchor)
        return self

    # ---- 工程图元素
    def dim_h(self, x1, x2, y, label, above=True, c='tm'):
        """水平尺寸线：两端短竖线，文字居中。"""
        self.line(x1, y, x2, y, 'dim')
        self.line(x1, y - 4, x1, y + 4, 'dim')
        self.line(x2, y - 4, x2, y + 4, 'dim')
        self.text((x1 + x2) / 2, y - 6 if above else y + 15, label, c, 'middle')
        return self

    def dim_v(self, x, y1, y2, label, left=True, c='tm'):
        self.line(x, y1, x, y2, 'dim')
        self.line(x - 4, y1, x + 4, y1, 'dim')
        self.line(x - 4, y2, x + 4, y2, 'dim')
        tx = x - 7 if left else x + 7
        self.text(tx, (y1 + y2) / 2 + 4, label, c, 'end' if left else 'start')
        return self

    def leader(self, x1, y1, x2, y2, label=None, anchor='start', c='tm', dot=True):
        """引线：从 (x1,y1) 指到图上的 (x2,y2)，文字放在 (x1,y1) 一端。"""
        self.line(x1, y1, x2, y2, 'dim')
        if dot:
            self.circle(x2, y2, 1.8, 'dimdot')
        if label:
            dx = 4 if anchor == 'start' else (-4 if anchor == 'end' else 0)
            self.text(x1 + dx, y1 + 4, label, c, anchor)
        return self

    def scalebar(self, x, y, px, label):
        """比例尺：一段带刻度的线。"""
        self.line(x, y, x + px, y, 'o1')
        for k in (0, 0.5, 1):
            self.line(x + px * k, y - (5 if k != 0.5 else 3), x + px * k, y, 'o1')
        self.text(x + px + 6, y + 1, label, 'tm')
        return self

    def man(self, x, base, h):
        """站着的人，脚底中心在 (x, base)，身高 h 像素。"""
        c = 'man' if h >= 40 else 'man mans'
        self.circle(x, base - 0.925 * h, 0.07 * h, c)
        self.rect(x - 0.11 * h, base - 0.84 * h, 0.22 * h, 0.40 * h, c, rx=0.045 * h)
        self.rect(x - 0.10 * h, base - 0.46 * h, 0.088 * h, 0.46 * h, c, rx=0.02 * h)
        self.rect(x + 0.012 * h, base - 0.46 * h, 0.088 * h, 0.46 * h, c, rx=0.02 * h)
        return self

    def tower(self, x, base, h, w, c='o1 d', up=True):
        """一座收分的高楼（参照物），底边中心 (x, base)，高 h，底宽 w；up=False 时倒着画，用来比深度。"""
        s = -1 if up else 1
        pts = [(x - w / 2, base), (x + w / 2, base), (x + w * 0.2, base + s * h), (x - w * 0.2, base + s * h)]
        return self.poly(pts, c)

    def hatch(self, x, y, w, h, kind='rock', c=''):
        """图案填充的矩形：rock 岩石，ice 冰，water 水。图案定义在页面的公共 <defs> 里。"""
        return self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="url(#pat-{kind})" class="pf {c}"/>')

    def ground(self, x1, x2, y):
        """地面线：一条实线加下面一排短斜线。"""
        self.line(x1, y, x2, y, 'o')
        n = int((x2 - x1) / 9)
        for i in range(n):
            xx = x1 + 4 + i * 9
            self.line(xx, y, xx - 5, y + 6, 'dim')
        return self

    def arrow(self, x1, y1, x2, y2, c='a', size=6):
        self.line(x1, y1, x2, y2, c)
        ang = math.atan2(y2 - y1, x2 - x1)
        for da in (2.6, -2.6):
            self.line(x2, y2, x2 + size * math.cos(ang + da), y2 + size * math.sin(ang + da), c)
        return self

    def svg(self, extra=''):
        t = f'<title>{esc(self.title)}</title>' if self.title else ''
        return (f'<svg viewBox="0 0 {self.w} {self.h}" class="{self.cls}" role="img" aria-label="{esc(self.title)}" '
                f'preserveAspectRatio="xMidYMid meet"{extra}>{t}{"".join(self.el)}</svg>')


# 页面公共的图案定义（放在 <body> 开头的一个隐藏 svg 里）
DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<pattern id="pat-rock" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" class="pat"/></pattern>
<pattern id="pat-ice" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="3" cy="4" r=".9" class="patdot"/><circle cx="10" cy="11" r=".9" class="patdot"/></pattern>
<pattern id="pat-water" width="16" height="7" patternUnits="userSpaceOnUse"><line x1="1" y1="3.5" x2="9" y2="3.5" class="pat"/></pattern>
<pattern id="pat-brick" width="14" height="8" patternUnits="userSpaceOnUse"><path d="M0 0H14M0 4H14M0 8H14M3.5 0V4M10.5 4V8" class="pat"/></pattern>
</defs></svg>'''
