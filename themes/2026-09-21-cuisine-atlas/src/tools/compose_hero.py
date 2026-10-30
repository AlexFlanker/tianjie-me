"""卷首图（第三版）：大都会艺术博物馆 29.110.88（网页编号 40741）明代掐丝珐琅八吉祥纹大碗（口径 29.2 cm，公有领域）。原片 3919×2941、深灰到浅灰的渐变背景。
做法：器物本身不动；背景用一个以器物为中心的椭圆光斑往外压暗成黑（像展柜里的聚光灯），再放进纯黑画布：横幅（桌面）与竖幅（手机）各一套。
器物轮廓按饱和度取（珐琅的松石蓝、鎏金口足都是高饱和，背景与台面是中性灰），填洞后就是整只碗，只用来保护器物边缘不被压暗。
（第一版克利夫兰 1975.96 青铜甗、第二版大都会 1987.10 元青花大盘，参数见 git 历史。）
用法（仓库根目录）：python3 -I themes/2026-09-21-cuisine-atlas/src/tools/compose_hero.py <原片 DP228992.jpg> themes/2026-09-21-cuisine-atlas/assets [预览目录]
原片：https://images.metmuseum.org/CRDImages/as/original/DP228992.jpg（3919×2941，公有领域，https://www.metmuseum.org/art/collection/search/40741）"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC, OUT = sys.argv[1], sys.argv[2]
PREV = sys.argv[3] if len(sys.argv) > 3 else None
im = Image.open(SRC).convert('RGB'); W0, H0 = im.size
A = np.asarray(im).astype(np.float32)
def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

k = 4
sm = np.asarray(im.resize((W0 // k, H0 // k), Image.LANCZOS)).astype(np.float32)
mx, mn = sm.max(2), sm.min(2); sat = (mx - mn) / (mx + 1e-3)
fg = (sat > 0.16) & (mx > 50)
fg = ndi.binary_closing(fg, structure=np.ones((5, 5)), iterations=2)
lab, n = ndi.label(fg); sizes = ndi.sum(fg, lab, range(1, n + 1)); fg = lab == (1 + int(np.argmax(sizes)))
fg = ndi.binary_fill_holes(fg); fg = ndi.binary_opening(fg, structure=np.ones((3, 3)))
ys, xs = np.where(fg); X0, X1, Y0, Y1 = xs.min() * k, xs.max() * k, ys.min() * k, ys.max() * k
print('subject bbox (full):', X0, X1, Y0, Y1)
prot = ndi.binary_dilation(fg, iterations=3)                       # 外扩约 12 px
protF = np.asarray(Image.fromarray((prot * 255).astype(np.uint8)).resize((W0, H0), Image.LANCZOS)).astype(np.float32) / 255.0
protF = ndi.gaussian_filter(protF, 6)

w, h = X1 - X0, Y1 - Y0
ecx, ecy = (X0 + X1) / 2, Y0 + 0.56 * h; rx, ry = 0.60 * w, 0.80 * h
YY, XX = np.mgrid[0:H0, 0:W0].astype(np.float32)
e = np.sqrt(((XX - ecx) / rx) ** 2 + ((YY - ecy) / ry) ** 2)
a_ell = 1.0 - smooth((e - 0.50) / 0.62)
alpha = np.maximum(a_ell, protF)
edge = smooth(XX / 300.0) * smooth((W0 - 1 - XX) / 300.0) * smooth(YY / 160.0) * smooth((H0 - 1 - YY) / 220.0)
alpha *= edge
out = np.clip((A * alpha[..., None] - 3.0) * 255.0 / 252.0, 0, 255)   # 黑场压低 3/255
iso = Image.fromarray((out + 0.5).astype(np.uint8))
TOP, BASE, CX = Y0, Y1, (X0 + X1) / 2

def compose(CW, CH, tip, base, cx):
    s = (base - tip) * CH / (BASE - TOP)
    sw, sh = round(W0 * s), round(H0 * s)
    ox = round(cx * CW - CX * s); oy = round(tip * CH - TOP * s)
    canvas = Image.new('RGB', (CW, CH), (0, 0, 0)); canvas.paste(iso.resize((sw, sh), Image.LANCZOS), (ox, oy))
    return canvas, dict(scale=round(float(s), 4), ox=ox, oy=oy, sw=sw, sh=sh, subj_cx=round((ox + CX * s) / CW * 100, 1), subj_cy=round((oy + (TOP + BASE) / 2 * s) / CH * 100, 1))

big, i1 = compose(3200, 1600, 0.30, 0.71, 0.72); print('landscape', i1)
mid, i4 = compose(2400, 1800, 0.36, 0.66, 0.74); print('4:3', i4)                  # 4:3 / 5:4 桌面与横放平板：盘小一点、更靠右，免得压到标题
por, i2 = compose(1440, 2560, 0.66, 0.88, 0.50); print("portrait", i2)        # 手机竖屏：碗在下方，底下留出图注的位置
tab, i3 = compose(1536, 2048, 0.66, 0.90, 0.56); print("tablet", i3)          # 平板竖屏（3:4）：字在上，碗在下
os.makedirs(OUT, exist_ok=True)
def save(img, name, wd):
    if img.width != wd: img = img.resize((wd, round(img.height * wd / img.width)), Image.LANCZOS)
    p = os.path.join(OUT, name); img.save(p, 'JPEG', quality=84, optimize=True, progressive=True, subsampling=0)
    print(name, img.size, os.path.getsize(p) // 1024, 'KB')
for wd in (3200, 2400, 1600): save(big, f'hero-met-40741-{wd}.jpg', wd)
for wd in (2400, 1600): save(mid, f'hero-met-40741-m{wd}.jpg', wd)
for wd in (1440, 960): save(por, f'hero-met-40741-p{wd}.jpg', wd)
for wd in (1536, 1024): save(tab, f'hero-met-40741-t{wd}.jpg', wd)
if PREV:
    os.makedirs(PREV, exist_ok=True)
    t = big.copy(); t.thumbnail((1600, 800)); t.save(os.path.join(PREV, 'land.jpg'), quality=85)
    t = por.copy(); t.thumbnail((720, 1280)); t.save(os.path.join(PREV, 'port.jpg'), quality=85)
