# 两块分图：东亚、美国本土（另有夏威夷小插图）。world.json 是 720×360 的等距圆柱：x=(lon+180)*2, y=(90-lat)*2。
# 每块按块中心纬度做 cos 校正，单位：viewBox 里每度经度 K*cos(lat_c)，每度纬度 K。两块都不跨 180° 经线，不用处理回绕。
import json, os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
_W = json.load(open(os.path.join(HERE, 'world.json')))
RINGS = []
for ring in re.findall(r'M[^Z]*Z', _W['d']):
    nums = list(map(float, re.findall(r'-?\d+\.?\d*', ring)))
    pts = [(nums[i] / 2 - 180, 90 - nums[i + 1] / 2) for i in range(0, len(nums), 2)]
    # 跨 180° 经线的轮廓（欧亚大陆的楚科奇一端）接成连续经度，免得在别的图里横扫全图
    out = [pts[0]]
    for lo, la in pts[1:]:
        p = out[-1][0]
        while lo - p > 180: lo -= 360
        while p - lo > 180: lo += 360
        out.append((lo, la))
    RINGS.append(out)

class Panel:
    def __init__(self, pid, lon0, lon1, lat0, lat1, K=10.0):
        self.id, self.lon0, self.lon1, self.lat0, self.lat1, self.K = pid, lon0, lon1, lat0, lat1, K
        self.c = math.cos(math.radians((lat0 + lat1) / 2))
    def xy(self, lat, lon): return round((lon - self.lon0) * self.K * self.c, 1), round((self.lat0 - lat) * self.K, 1)
    def vb(self): return [0, 0, round((self.lon1 - self.lon0) * self.K * self.c), round((self.lat0 - self.lat1) * self.K)]
    def land(self, box=None):
        lon0, lon1, lat0, lat1 = box or (self.lon0, self.lon1, self.lat0, self.lat1)
        out = []
        cen = (lon0 + lon1) / 2
        for r0 in RINGS:
            m = sum(p[0] for p in r0) / len(r0)
            sh = min((-360, 0, 360), key=lambda k: abs(m + k - cen))
            r = [(p[0] + sh, p[1]) for p in r0]
            lons = [p[0] for p in r]; lats = [p[1] for p in r]
            if max(lons) < lon0 - 2 or min(lons) > lon1 + 2 or max(lats) < lat1 - 2 or min(lats) > lat0 + 2: continue
            if box and not (lon0 <= min(lons) and max(lons) <= lon1 and lat1 <= min(lats) and max(lats) <= lat0): continue   # 插图只收完全落在框里的小岛
            out.append(''.join(('M' if i == 0 else 'L') + '%.1f %.1f' % self.xy(la, lo) for i, (lo, la) in enumerate(r)) + 'Z')
        return ''.join(out)

ASIA = Panel('asia', 103, 134, 46, 19)
USA = Panel('usa', -126, -66, 50, 21)
HAWAII = (-160.4, -154.6, 22.4, 18.8)   # 夏威夷插图的经纬范围（画在美国图左下角，同一比例尺）

def hawaii_inset():
    """把夏威夷平移到美国图左下角：返回 (平移量 dx, dy, 插图框 x, y, w, h, 陆地路径)"""
    lon0, lon1, lat0, lat1 = HAWAII
    x0, y0 = USA.xy(lat0, lon0); x1, y1 = USA.xy(lat1, lon1)
    w, h = x1 - x0, y1 - y0
    vbw, vbh = USA.vb()[2], USA.vb()[3]
    bx, by = 12, vbh - h - 12
    dx, dy = bx - x0, by - y0
    path = USA.land(HAWAII)
    return dict(dx=round(dx, 1), dy=round(dy, 1), x=bx, y=round(by, 1), w=round(w, 1), h=round(h, 1), land=path)

def place(lat, lon):
    """节点落在哪块图、坐标多少"""
    if lon > 0: x, y = ASIA.xy(lat, lon); return 'asia', x, y
    if lon < -150:
        ins = hawaii_inset(); x, y = USA.xy(lat, lon); return 'usa', round(x + ins['dx'], 1), round(y + ins['dy'], 1)
    x, y = USA.xy(lat, lon); return 'usa', x, y

if __name__ == '__main__':
    print(ASIA.vb(), USA.vb(), len(ASIA.land()), len(USA.land()), hawaii_inset()['w'], hawaii_inset()['h'])
    for n, la, lo in [('Seoul', 37.57, 126.99), ('Beijing', 39.9, 116.4), ('HK', 22.3, 114.17), ('LA', 34.05, -118.25), ('NYC', 40.75, -73.99), ('Honolulu', 21.3, -157.86)]:
        print(n, place(la, lo))
