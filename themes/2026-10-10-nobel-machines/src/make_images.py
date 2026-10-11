#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把四路图片底稿 research/img_{A,B,C,D}.json 合成 images.json（每座装置一组，已排好顺序）。

  python3 themes/2026-10-10-nobel-machines/src/make_images.py

编辑决定都写在这里：DROP 是不用的图及原因；ORDER 是每组的顺序（第一张是大图）；
PLATE 是线图 / 图表（整幅显示、不裁切），值是底色；OVR 是对底稿图注的改写。
"""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.dirname(HERE)

DROP = {
    'leiden/06': '来源页没有任何许可说明，按「条款不清不用」拿掉',
    'cambridge/04': '拍的是另一台望远镜的轨道止挡，与本卡两台装置无关',
    'cambridge/06': '拍的是旧铁路路基上的另一组天线，与本卡两台装置无关',
}
ORDER = {
    'michelson': ['01', '02', '05', '04', '06', '03'],
    'leiden': ['01', '03', '02', '04', '05'],
    'cyclotron': ['03', '04', '01', '05', '02'],
    'bubble': ['01', '02', '03'],
    'cambridge': ['01', '03', '02', '05'],
    'spps': ['02', '01', '04', '05', '03', '06'],
    'homestake': ['01', '03', '02', '04', '05'],
    'cobe': ['01', '02', '03', '04', '06', '05'],
    'lhc': ['02', '01', '03', '04', '05', '06'],
    'superk-sno': ['03', '01', '04', '02', '05', '06'],
    'ligo': ['02', '03', '06', '05', '04', '01'],
    'icecube': ['01', '02', '04', '03', '05', '06'],
}
PLATE = {  # 线图、图表、剖视图：整幅显示
    'michelson/01': 'paper', 'michelson/02': 'paper', 'michelson/03': 'paper', 'michelson/04': 'paper', 'michelson/05': 'paper', 'michelson/06': 'paper',
    'leiden/01': 'paper', 'leiden/02': 'paper', 'leiden/03': 'paper', 'leiden/04': 'paper', 'leiden/05': 'paper',
    'cyclotron/01': 'paper', 'cyclotron/02': 'paper', 'cyclotron/05': 'paper',
    'cobe/02': 'black', 'cobe/03': 'black', 'cobe/04': 'paper', 'cobe/05': 'black',
    'spps/04': 'black', 'spps/05': 'black', 'spps/03': 'black',
    'lhc/05': 'black', 'lhc/04': 'paper',
    'icecube/02': 'paper', 'icecube/03': 'paper', 'icecube/06': 'black',
    'ligo/05': 'paper', 'ligo/06': 'paper',
    'superk-sno/01': 'paper', 'superk-sno/04': 'paper', 'superk-sno/05': 'paper', 'superk-sno/06': 'paper',
    'homestake/04': 'black',
}
OVR = {
    'cambridge/01': dict(title='天文台的大天线', role='scale',
        caption='2020 年 5 月 6 日，从哈斯林菲尔德—巴顿公路边的田埂望向 Mullard 射电天文台。摄影者只注明是「较大的射电望远镜」；近处一面抛物面天线架在格架式座架上，树木可作尺度参照。它是不是一英里望远镜的 18 米天线，本页没能确认。'),
    'cambridge/02': dict(title='格架座上的抛物面天线',
        caption='同一天隔着田门拍到的一面天线：网状抛物面架在高高的格架式座架上。摄影者没有写明是哪一台望远镜。'),
    'cambridge/03': dict(title='1975 年的 4C 阵', role='overview',
        caption='1975 年 6 月 7 日的 Mullard 射电天文台：一长排柱面抛物面反射架，前景的拖拉机和打捆机给出尺度。这是天文台更早的一台巡天设备，不是本卡的两台装置；休伊什的闪烁阵同样是在田里立杆拉线，没有找到可以转载的照片。'),
    'cambridge/05': dict(title='今天的天文台', role='overview',
        caption='2026 年 7 月 15 日，从巴顿路向东北望去，Mullard 射电天文台的一排抛物面天线越过麦田。摄影者说明：这些天线可以沿一条旧铁路线移动。它们是一英里望远镜之后的设备，移动天线、改变基线的做法一脉相承。'),
    'cobe/03': dict(caption='宇宙微波背景的频谱，NASA 的图题是「理论与观测一致」。这一版图上只画了一条曲线：FIRAS 的测量值与单一温度的黑体曲线重合到分不开。'),
    'bubble/01': dict(caption='1959 年 4 月 1 日，伯克利辐射实验室 59 号楼内的广角全景：气泡室连同磁体和两层操作平台立在厂房中央，平台上的操作员和门外停车场的汽车可作尺度参照。国会图书馆的图注只写「气泡室」，没有写尺寸；按年份和地点，应是 72 英寸那一台。（翻拍底片左右颠倒，此处已水平翻转还原。）'),
    'bubble/02': dict(caption='1958 年 8 月 18 日，气泡室总装：行车把气泡室本体连同管路吊起，工人在下方和梯架上扶正，旁边的人可作尺度参照。图注同样没有写尺寸。'),
    'lhc/05': dict(title='ATLAS 事例显示（2012-06）'),
    'homestake/01': dict(caption='约 1960 年代，戴维斯站在尚未封顶的钢罐内。这只罐后来灌满四氯乙烯，在 Homestake 金矿 4850 英尺层数太阳中微子。人只占罐底一小块。照片取自 Sanford 实验室官网，原摄影者页面上没有标。'),
}
ROLE = {'scale': '规模', 'principle': '原理', 'overview': '全景', 'detail': '细节', 'construction': '施工', 'people': '人'}

rows = []
for f in sorted(glob.glob(os.path.join(HERE, 'research', 'img_*.json'))):
    rows += json.load(open(f, encoding='utf-8'))
by = {}
for r in rows:
    key = r['file'][len('assets/'):-len('.jpg')]
    if key in DROP:
        continue
    r.update(OVR.get(key, {}))
    r['kind'] = 'plate' if key in PLATE else 'photo'
    r['bg'] = PLATE.get(key, '')
    r['role_zh'] = ROLE[r['role']]
    assert os.path.exists(os.path.join(THEME, r['file'])), r['file']
    by.setdefault(r['id'], {})[key.split('/')[1]] = r
out = {}
for mid, order in ORDER.items():
    assert set(order) == set(by[mid]), (mid, sorted(by[mid]))
    out[mid] = [by[mid][n] for n in order]
json.dump({'dropped': DROP, 'groups': out}, open(os.path.join(HERE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('images.json:', sum(len(v) for v in out.values()), 'images in', len(out), 'groups; dropped', len(DROP))
