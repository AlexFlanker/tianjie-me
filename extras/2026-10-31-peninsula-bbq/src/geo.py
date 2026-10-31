# 太平洋居中的等距圆柱投影：把 world.json（720×360，x=(lon+180)*2）改成以 Atlantic -30° 为切口
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
K = 4.0                     # 每度像素
LON0, LON1, LAT0, LAT1 = 72, 296, 62, 14   # 视窗：东经 72° → 西经 64°；北纬 62° → 14°
def lon2(l): l = (l + 30) % 360; return l
def proj(lat, lon):
    x = (lon2(lon) - lon2(LON0)) * K; y = (LAT0 - lat) * K; return round(x, 1), round(y, 1)
def land():
    w = json.load(open(os.path.join(HERE, 'world.json')))
    out = []
    for ring in re.findall(r'M[^Z]*Z', w['d']):
        pts = [tuple(map(float, p.split())) for p in re.findall(r'[-\d.]+ [-\d.]+', ring.replace('M', ' ').replace('L', ' ').replace(',', ' '))] if False else None
        nums = list(map(float, re.findall(r'-?\d+\.?\d*', ring)))
        pts = [(nums[i] / 2 - 180, 90 - nums[i + 1] / 2) for i in range(0, len(nums), 2)]
        xs = [lon2(lo) for lo, la in pts]
        if max(xs) - min(xs) > 180: xs = [x + 360 if x < 180 else x for x in xs]
        x0 = lon2(LON0)
        seg = ['%s%.1f %.1f' % ('M' if i == 0 else 'L', (x - x0) * K, (LAT0 - la) * K) for i, (x, (lo, la)) in enumerate(zip(xs, pts))]
        # 只保留与视窗相交的环
        X = [(x - x0) * K for x in xs]; Y = [(LAT0 - la) * K for lo, la in pts]
        W, H = (lon2(LON1) - x0) * K, (LAT0 - LAT1) * K
        if max(X) < -20 or min(X) > W + 20 or max(Y) < -20 or min(Y) > H + 20: continue
        out.append(''.join(seg) + 'Z')
    return ''.join(out)
def vb(): return [0, 0, round((lon2(LON1) - lon2(LON0)) * K), round((LAT0 - LAT1) * K)]
if __name__ == '__main__':
    d = land(); print(len(d), vb(), proj(37.57, 126.98), proj(34.05, -118.24), proj(39.9, 116.4), proj(40.75, -73.99))
