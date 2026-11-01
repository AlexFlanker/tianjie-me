"""卷首图（第四版，2026-10-30）：一盘麻婆豆腐配白米饭（俯拍），WordPress 图片库，摄影 gastronomicslc，CC0。原片 4096×3072，白瓷盘放在木桌上。
做法：找出白瓷盘（高亮、低饱和的最大连通块的外接框 → 圆心与半径），盘子本身不动；盘外的木纹按到盘心的距离往外压暗成黑（像一束聚光打在桌上），
再放进纯黑画布：宽屏（宽高比 > 3:2）一套横幅，盘心放在与 shell.html 的 object-position（72% 50%）一致的位置；
3:2 以下（4:3 屏、横放与竖放的平板、手机）都用一张方图：光斑改成正圆，盘子居中，页面上让它单独占一块（字的右边或下面）等比缩放
（四周本来就是纯黑，留黑边也看不出来）。
（第一版克利夫兰 1975.96 青铜甗、第二版大都会 1987.10 元青花大盘、第三版大都会 29.110.88 明代掐丝珐琅大碗，参数见 git 历史。）
用法（仓库根目录）：python3 -I themes/2026-09-21-cuisine-atlas/src/tools/compose_hero.py <原片> themes/2026-09-21-cuisine-atlas/assets [预览目录]
原片：https://pd.w.org/2021/12/76761c35f32b42144.57366300.jpg（https://wordpress.org/photos/photo/76761c35f3/）"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC, OUT = sys.argv[1], sys.argv[2]
PREV = sys.argv[3] if len(sys.argv) > 3 else None
NAME = 'hero-mapo'
im = Image.open(SRC).convert('RGB'); W0, H0 = im.size
A = np.asarray(im).astype(np.float32)
def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

# ---- 找盘子：高亮且低饱和（白瓷盘沿 + 米饭）的最大连通块
k = 8
sm = np.asarray(im.resize((W0 // k, H0 // k), Image.LANCZOS)).astype(np.float32)
mx, mn = sm.max(2), sm.min(2); sat = (mx - mn) / (mx + 1e-3)
wh = (mx > 175) & (sat < 0.16)
lab, n = ndi.label(wh); sizes = ndi.sum(wh, lab, range(1, n + 1)); wh = lab == (1 + int(np.argmax(sizes)))
ys, xs = np.where(wh)
X0, X1, Y0, Y1 = xs.min() * k, (xs.max() + 1) * k, ys.min() * k, (ys.max() + 1) * k
# 盘上方有几道发亮的木纹会连进来，所以半径只按左右宽度算，圆心的纵坐标从干净的盘底往上量
R = (X1 - X0) / 2; PCX = (X0 + X1) / 2; PCY = Y1 - R
print('plate centre', round(PCX), round(PCY), 'radius', round(R))

# ---- 聚光：盘沿以内全亮，盘外渐暗成黑；外缘横向到 ex·R、纵向到 ey·R（原片上下边离盘沿只有约 0.23R，纵向要收紧到 1.21R
#      才看不见原片的上下边）。横幅用横椭圆（1.52R × 1.21R），竖屏方图用正圆（1.21R）；原片四边再羽化
YY, XX = np.mgrid[0:H0, 0:W0].astype(np.float32)
dx, dy = XX - PCX, YY - PCY
r = np.sqrt(dx ** 2 + dy ** 2) + 1e-3
edge = smooth(XX / 240.0) * smooth((W0 - 1 - XX) / 240.0) * smooth(YY / 240.0) * smooth((H0 - 1 - YY) / 240.0)
def spot(ex, ey):
    r_out = 1.0 / np.sqrt((dx / r / (ex * R)) ** 2 + (dy / r / (ey * R)) ** 2 + 1e-12)
    alpha = (1.0 - smooth((r - 1.02 * R) / np.maximum(r_out - 1.02 * R, 1.0))) * edge
    out = np.clip((A * alpha[..., None] - 3.0) * 255.0 / 252.0, 0, 255)   # 黑场压低 3/255
    return Image.fromarray((out + 0.5).astype(np.uint8))
iso, iso_round = spot(1.52, 1.21), spot(1.21, 1.21)

def compose(CW, CH, diam, cx, cy, src=None):
    """diam：盘子直径占画布高度的比例；cx / cy：盘心在画布里的位置（比例）。"""
    src = src or iso
    s = diam * CH / (2 * R)
    sw, sh = round(W0 * s), round(H0 * s)
    ox = round(cx * CW - PCX * s); oy = round(cy * CH - PCY * s)
    canvas = Image.new('RGB', (CW, CH), (0, 0, 0)); canvas.paste(src.resize((sw, sh), Image.LANCZOS), (ox, oy))
    return canvas, dict(scale=round(float(s), 4), ox=ox, oy=oy, plate_px=round(2 * R * s))

big, i1 = compose(3200, 1600, 0.78, 0.72, 0.52); print('landscape', i1)
sq, i2 = compose(1600, 1600, 0.80, 0.50, 0.50, iso_round); print('square', i2)   # 竖屏：正圆光斑外缘 1.21 × 0.40 = 0.484，留在画布以内
os.makedirs(OUT, exist_ok=True)
def save(img, name, wd):
    if img.width != wd: img = img.resize((wd, round(img.height * wd / img.width)), Image.LANCZOS)
    p = os.path.join(OUT, name); img.save(p, 'JPEG', quality=84, optimize=True, progressive=True, subsampling=0)
    print(name, img.size, os.path.getsize(p) // 1024, 'KB')
for wd in (3200, 2400, 1600): save(big, f'{NAME}-{wd}.jpg', wd)
for wd in (1600, 1000): save(sq, f'{NAME}-s{wd}.jpg', wd)
if PREV:
    os.makedirs(PREV, exist_ok=True)
    t = big.copy(); t.thumbnail((1600, 800)); t.save(os.path.join(PREV, 'land.jpg'), quality=85)
    t = sq.copy(); t.thumbnail((800, 800)); t.save(os.path.join(PREV, 'square.jpg'), quality=85)
