"""序章十期与三章开篇的图：从各馆开放获取原图缩到网页尺寸（长边 1400 / 1600 px），惠康扫描件先裁掉黑边。
原图不进仓库；来源、许可与说明写在 ../images.json。用法：python3 -I make_images.py <原图目录> <assets 目录>"""
import sys, os
import numpy as np
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
JOBS = [  # (输出名, 原图相对路径, 长边, 裁黑边)
    ('st-xq', 'xq/xq_r1_cma_1962.281_ding.jpg', 1400, False),
    ('st-qh', 'qh/qh_r1_met_13.100.158_stove_bw.jpg', 1400, False),
    ('st-wj', 'wj/wj_r2_cma_1973.84_chicken_head_ewer.jpg', 1400, False),
    ('st-st', 'st/st_r2_met_2010.473_palace_banquet_detail.jpg', 1400, False),
    ('st-song', 'song/song_r1_cma_2020.175_jian_teabowl_gongyu.jpg', 1400, False),
    ('st-yuan', 'yuan/yuan_r2_nlc_yinshan_zhengyao_1456_sheep_page.jpg', 1400, False),
    ('st-ming', 'ming/ming_r2_wellcome_L0039399_shiwu_bencao_liquor.jpg', 1400, True),
    ('st-qing', 'qing/qing_r1_wellcome_V0018506_zhou_peiqun_shaobing.jpg', 1400, False),
    ('st-mg', 'mg/mg_r1_rijks_RP-F-2005-21-17_mennie_peking_street_eatery.jpg', 1400, False),
    ('st-dd', 'dd/dd_r1_wordpress_208098_malatang.jpg', 1400, False),
    ('op-lines', 'ming/ming_r3_wellcome_L0039359_shiwu_bencao_vinegar.jpg', 1600, True),
    ('op-chili', 'ming/ming_r1_rijks_RP-T-BR-2017-1-11-22_capsicum.jpg', 1600, False),
    ('op-provs', 'qing/qing_r2_loc_wdl02047_beijing_portable_kitchen_1874.jpg', 1600, False),
]
def trim_black(im, thr=40, frac=0.6):
    a = np.asarray(im.convert('L')).astype(np.float32); h, w = a.shape
    def dark_row(r): return (r < thr).mean() > frac
    t, b, l, r = 0, h - 1, 0, w - 1
    while t < h // 4 and dark_row(a[t]): t += 1
    while b > h * 3 // 4 and dark_row(a[b]): b -= 1
    while l < w // 4 and dark_row(a[:, l]): l += 1
    while r > w * 3 // 4 and dark_row(a[:, r]): r -= 1
    pad = 6
    return im.crop((min(l + pad, w - 1), min(t + pad, h - 1), max(r - pad, 1), max(b - pad, 1)))
os.makedirs(OUT, exist_ok=True)
for name, rel, side, trim in JOBS:
    im = Image.open(os.path.join(SRC, rel)); im = im.convert('RGB')
    if trim: im = trim_black(im)
    s = side / max(im.size)
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    p = os.path.join(OUT, name + '.jpg'); im.save(p, 'JPEG', quality=80, optimize=True, progressive=True)
    print(f'{name}\t{im.width}\t{im.height}\t{os.path.getsize(p) // 1024} KB')
