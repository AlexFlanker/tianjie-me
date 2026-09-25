import json, math

# ---------- Albers equal-area conic, standard parallels 25N/47N, origin 105E/30N ----------
phi1, phi2, phi0, lam0 = map(math.radians, (25.0, 47.0, 30.0, 105.0))
n = (math.sin(phi1) + math.sin(phi2)) / 2
C = math.cos(phi1) ** 2 + 2 * n * math.sin(phi1)
rho0 = math.sqrt(C - 2 * n * math.sin(phi0)) / n

def proj(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    rho = math.sqrt(C - 2 * n * math.sin(phi)) / n
    th = n * (lam - lam0)
    return rho * math.sin(th), rho0 - rho * math.cos(th)

FINE = {'上海市', '天津市', '香港特别行政区', '澳门特别行政区', '台湾省', '海南省', '北京市'}
main = json.load(open('prov_main.json'))
fine = json.load(open('prov_fine.json'))
fine_by = {f['properties']['name']: f for f in fine['features']}
feats = []
for f in main['features']:
    nm = f['properties']['name']
    feats.append(fine_by[nm] if nm in FINE else f)

# Only geometry north of ~17.5N goes into the main frame (南海诸岛 go to the inset)
MAIN_LAT_MIN = 17.6

def rings_of(geom):
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    return polys

# projected bounds of main frame
xs, ys = [], []
for f in feats:
    for poly in rings_of(f['geometry']):
        for ring in poly:
            for lon, lat in ring:
                if lat >= MAIN_LAT_MIN:
                    x, y = proj(lon, lat); xs.append(x); ys.append(-y)
# 十段线 dashes north of 17.6 too (near Taiwan)
jd = json.load(open('jd.json'))['features'][0]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
W = 1000.0
PAD = 12
scale = (W - 2 * PAD) / (maxx - minx)
H = (maxy - miny) * scale + 2 * PAD

def to_svg(lon, lat):
    x, y = proj(lon, lat)
    return (x - minx) * scale + PAD, (-y - miny) * scale + PAD

def fmt(v):
    s = f"{v:.1f}"
    if s.endswith('.0'): s = s[:-2]
    return s

def path_from_polys(polys, keep=lambda lat: True):
    parts = []
    for poly in polys:
        for ring in poly:
            pts = [to_svg(lon, lat) for lon, lat in ring if keep(lat)]
            if len(pts) < 3: continue
            # relative-coordinate path with 1-decimal rounding
            rx, ry = round(pts[0][0], 1), round(pts[0][1], 1)
            seg = [f"M{fmt(rx)} {fmt(ry)}"]
            cx, cy = rx, ry
            for x, y in pts[1:]:
                x, y = round(x, 1), round(y, 1)
                dx, dy = round(x - cx, 1), round(y - cy, 1)
                if dx == 0 and dy == 0: continue
                seg.append(f"l{fmt(dx)} {fmt(dy)}")
                cx, cy = x, y
            seg.append("z")
            parts.append(''.join(seg))
    return ''.join(parts)

CODES = {'北京市':'BJ','天津市':'TJ','河北省':'HE','山西省':'SX','内蒙古自治区':'NM','辽宁省':'LN','吉林省':'JL','黑龙江省':'HL',
 '上海市':'SH','江苏省':'JS','浙江省':'ZJ','安徽省':'AH','福建省':'FJ','江西省':'JX','山东省':'SD','河南省':'HA','湖北省':'HB',
 '湖南省':'HN','广东省':'GD','广西壮族自治区':'GX','海南省':'HI','重庆市':'CQ','四川省':'SC','贵州省':'GZ','云南省':'YN',
 '西藏自治区':'XZ','陕西省':'SN','甘肃省':'GS','青海省':'QH','宁夏回族自治区':'NX','新疆维吾尔自治区':'XJ','台湾省':'TW',
 '香港特别行政区':'HK','澳门特别行政区':'MO'}

orig0 = json.load(open('china_full.json'))
centroids = {f['properties']['name']: f['properties'].get('centroid') or f['properties']['center'] for f in orig0['features'] if f['properties'].get('name')}
out = {'w': round(W, 1), 'h': round(H, 1), 'prov': {}, 'jd': '', 'islands': [], 'inset': {}}
for f in feats:
    nm = f['properties']['name']; code = CODES[nm]
    polys = rings_of(f['geometry'])
    # main-frame path: whole polygons whose centroid-ish (first point) is north of MAIN_LAT_MIN
    main_polys = [poly for poly in polys if max(lat for lon, lat in poly[0]) >= MAIN_LAT_MIN]
    d = path_from_polys(main_polys)
    cx, cy = to_svg(*centroids[nm])
    out['prov'][code] = {'name': nm, 'd': d, 'c': [round(cx, 1), round(cy, 1)]}

# 十段线: full (used in inset via transform; main frame shows the part inside its viewBox)
out['jd'] = path_from_polys(rings_of(jd['geometry']))

# 南海诸岛 dots from the ORIGINAL (unsimplified) Hainan + Guangdong features, south of 17.6N
orig = json.load(open('china_full.json'))
for f in orig['features']:
    if f['properties'].get('name') in ('海南省', '广东省', '台湾省'):
        for poly in rings_of(f['geometry']):
            ring = poly[0]
            lat_max = max(lat for lon, lat in ring)
            if lat_max < MAIN_LAT_MIN:
                lon = sum(p[0] for p in ring) / len(ring); lat = sum(p[1] for p in ring) / len(ring)
                x, y = to_svg(lon, lat)
                out['islands'].append([round(x, 1), round(y, 1)])
# dedupe near-identical dots
ded = []
for x, y in out['islands']:
    if all(abs(x - a) > 2 or abs(y - b) > 2 for a, b in ded): ded.append((x, y))
out['islands'] = [[x, y] for x, y in ded]

# inset frame: lon 106-125, lat 2-25 in main-frame coordinates
ix0, iy0 = to_svg(106, 25.5); ix1, iy1 = to_svg(125.5, 2.0)
out['inset'] = {'x0': round(ix0, 1), 'y0': round(iy0, 1), 'x1': round(ix1, 1), 'y1': round(iy1, 1)}
json.dump(out, open('map_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('viewBox', out['w'], out['h'], 'inset', out['inset'], 'islands', len(out['islands']))
print('path chars', sum(len(v['d']) for v in out['prov'].values()), 'jd', len(out['jd']))
for code, v in out['prov'].items():
    print(code, v['name'], len(v['d']), v['c'])
