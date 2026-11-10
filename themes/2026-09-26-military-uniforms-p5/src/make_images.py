# -*- coding: utf-8 -*-
"""v2（2026-11-10）选图：把 U1 / U2 两路新搜的高清原图与旧版仍用的授权图合成一份 src/images.json，并把文件拷进 assets/。
一次性脚本（新图的暂存目录在会话 scratchpad，不在仓库里）；留档是为了说明每格用了哪几张、哪些说明被改保守。
python3 make_images.py <stage_dir> <old_images.json> <old_assets_dir>"""
import json, os, sys, shutil, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ASSETS = os.path.join(HERE, '..', 'assets')
STAGE, OLDJ, OLDA = sys.argv[1], sys.argv[2], sys.argv[3]

# 每格用图（新图写 id，旧图写文件名去掉 .jpg；顺序 = 展开后从大到小）
CELLS = {
 'cn-E1': ['cn-1739-qianlong-armour-castiglione-hd', 'cn-1800-chinese-military-post-brown'],
 'cn-E2': ['cn-1869-manchu-soldiers-canton-thomson', 'cn-1874-qing-soldier-haoyi-thomson', 'cn-1860-chinese-soldier-brown'],
 'cn-E3': ['old:cn-1911-new-army-chengdu-knight'],
 'cn-E4': ['old:cn-1942-nra-m35-helmet-signal-corps', 'cn-1943-chinese-troops-c47-hump-india-usaaf', 'old:cn-1937-eighth-route-army-sentry-great-wall-shafei'],
 'cn-E5': ['old:cn-1955-type55-marshal-greatcoat-peng-dehuai'],
 'cn-E6': ['old:cn-1972-type65-honor-guard-nixon-whitehouse', 'cn-1988-pla-delegation-type85-hurlburt-dod', 'old:cn-1998-type87-general-zhang-wannian-dod'],
 'cn-E7': ['cn-us-2016-type07-ocp-closeup-kunming-dod', 'cn-2013-type07-digital-camo-rescue-hawaii-dod', 'old:cn-2015-type07-digital-camo-dme-army'],
 'cn-E8': ['old:cn-2025-type21-marines-cns', 'old:cn-2021-type21-xingkong-blouse-cc0', 'cn-2017-pla-tri-service-honor-guard-bayi-dod', 'old:cn-2024-honor-guard-battalion-kremlin'],
 'us-E1': ['us-1781-surrender-cornwallis-trumbull', 'us-1779-washington-at-princeton-peale', 'old:us-1781-continental-mcbarron'],
 'us-E2': ['us-1866-prisoners-from-the-front-homer', 'us-1864-114th-pennsylvania-zouaves-petersburg', 'old:us-1862-union-campaign-uniform-ogden'],
 'us-E3': ['old:us-1918-american-soldiers-brodie-signalcorps', 'us-1898-rough-riders-san-juan-dinwiddie'],
 'us-E4': ['us-1942-infantryman-halftrack-garand-colour-palmer', 'us-1944-101st-paratroopers-c47-dday-usaaf', 'old:us-1944-ike-jacket-101st-dday'],
 'us-E5': ['us-1967-og107-jungle-fatigues-m16-vietnam-nara', 'old:us-1968-og107-mp-vietnam'],
 'us-E6': ['us-1986-m81-bdu-pasgt-teamspirit-dod', 'us-1966-tigerstripe-face-camouflage-101st-vietnam-nara', 'old:us-1969-erdl-tigerstripe-rangers'],
 'us-E7': ['us-2010-ucp-vs-multicam-korengal-dod', 'us-2005-acu-ucp-first-issue-fort-hood-dod', 'us-2021-usmc-marpat-desert-recruit-face-paint-dod'],
 'us-E8': ['us-2024-ocp-formation-triglav-star-dod', 'old:us-2022-agsu-portrait-army', 'us-2021-old-guard-sentinel-closeup-dod'],
 'ru-E1': ['ru-1802-guard-infantry-brown', 'ru-1700-officer-vinkhuijzen', 'old:ru-1812-infantry-kiver-zaretsky'],
 'ru-E2': ['ru-1865-infantry-cavalry-brown'],
 'ru-E3': ['ru-1914-infantry-march-past-bain', 'ru-1910-khaki-gimnastyorka-persia-bain'],
 'ru-E4': ['old:ru-1945-victory-parade-heroes-shoulder-boards-mosru', 'old:ru-1926-budenovka-gymnastyorka-bundesarchiv'],
 'ru-E5': [],
 'ru-E6': ['old:ru-1986-afghanka-withdrawal-march-rian', 'ru-1992-tamanskaya-winter-afghanka-dod'],
 'ru-E7': ['ru-1995-vsr93-camo-peacekeeper-kansas-dod', 'ru-2001-flora-camo-kosovo-kfor-dod'],
 'ru-E8': ['old:ru-2018-ratnik-emr-peace-mission-milru', 'old:ru-2014-presidential-regiment-parade-milru'],
 'uk-E1': ['uk-1815-28th-quatre-bras-butler', 'uk-1759-death-of-wolfe-west', 'uk-1742-foot-guards-1st-vinkhuijzen'],
 'uk-E2': ['uk-1854-thin-red-line-gibb', 'uk-1855-71st-colour-sergeant-fenton', 'old:uk-1881-scarlet-tunic-colour-sergeant'],
 'uk-E3': ['uk-1916-somme-brodie-helmet-iwm', 'old:uk-1917-service-dress-full-kit-iwm', 'uk-1900-royal-munster-fusiliers-trench-honey-nest-kloof'],
 'uk-E4': ['old:uk-1942-battledress-paratrooper-colour-iwm', 'old:uk-1940-battledress-bef-iwm', 'uk-1943-battledress-mk2-helmet-tunis-parrino'],
 'uk-E5': [],
 'uk-E6': ['uk-us-1984-dpm-m81-paratroopers-normandy-dod', 'uk-1980-dpm-smock-para-arnhem-dod', 'old:uk-1980-dpm-reforger-slr-dod'],
 'uk-E7': ['uk-1994-dpm-5-airborne-kigali-dod', 'uk-2005-desert-dpm-basra-iraqi-army-dod', 'old:uk-1993-dpm-l85a1-roaring-lion-dod'],
 'uk-E8': ['uk-us-2021-mtp-ocp-paratroopers-fort-bragg-dod', 'uk-2025-coldstream-scots-guards-buckingham-usarmy', 'old:uk-2014-mtp-sandhurst-grafenwoehr-dod'],
 'fr-E1': ['fr-1807-friedland-cuirassiers-meissonier', 'old:fr-1812-line-infantry-carle-vernet', 'old:fr-1776-gatinois-infantry-juillet'],
 'fr-E2': ['fr-1870-defense-champigny-detaille', 'fr-1914-chasseur-afrique-marne-autochrome', 'fr-1855-zouave-crimea-fenton-met'],
 'fr-E3': ['fr-1917-trench-observation-castelnau-autochrome', 'fr-1917-deux-poilus-reims-castelnau-autochrome', 'old:fr-1917-horizon-blue-adrian-autochrome'],
 'fr-E4': ['old:fr-1940-khaki-capote-adrian-124ri', 'fr-1943-french-troops-tunis-victory-parade-collins'],
 'fr-E5': ['old:fr-1979-lizard-camouflage-6e-rama-djibouti'],
 'fr-E6': ['fr-1994-f1-tropical-khaki-goma-dod'],
 'fr-E7': ['fr-1991-daguet-desert-camo-legion-bugler-dod', 'old:fr-1996-cce-camouflage-40e-ra-dod', 'fr-us-2002-cce-desert-camo-kabul-dod'],
 'fr-E8': ['old:fr-2013-saint-cyr-grand-uniforme-nguyen', 'old:fr-2013-foreign-legion-kepi-blanc-nguyen', 'fr-us-2017-garde-republicaine-doughboy-ocp-satory-dod'],
}
CARDS = {
 'uk-redcoat': 'uk-1759-death-of-wolfe-west', 'us-blue': 'us-1779-washington-at-princeton-peale', 'uk-bearskin': 'uk-2025-coldstream-scots-guards-buckingham-usarmy',
 'fr-garance': 'fr-1870-defense-champigny-detaille', 'uk-khaki': 'uk-1900-royal-munster-fusiliers-trench-honey-nest-kloof', 'de-feldgrau': 'de-1914-kaiser-reviewing-infantry-feldgrau-bain',
 'cn-1905': 'old:cn-1911-new-army-chengdu-knight', 'uk-brodie': 'uk-1916-royal-irish-rifles-ration-party-somme', 'fr-horizon': 'fr-1914-chasseur-afrique-marne-autochrome',
 'fr-adrian': 'fr-1917-deux-poilus-reims-castelnau-autochrome', 'ru-1917': 'old:ru-1926-budenovka-gymnastyorka-bundesarchiv', 'uk-bd': 'old:uk-1940-battledress-bef-iwm',
 'us-1943': 'old:us-1944-ike-jacket-101st-dday', 'ru-1943': 'old:ru-1945-victory-parade-heroes-shoulder-boards-mosru', 'fr-lizard': 'old:fr-1979-lizard-camouflage-6e-rama-djibouti',
 'cn-1955': 'old:cn-1955-type55-marshal-greatcoat-peng-dehuai', 'cn-1965': 'old:cn-1972-type65-honor-guard-nixon-whitehouse', 'uk-dpm-mtp': 'uk-us-1984-dpm-m81-paratroopers-normandy-dod',
 'ru-afghanka': 'old:ru-1986-afghanka-withdrawal-march-rian', 'cn-1988': 'cn-1988-pla-delegation-type85-hurlburt-dod', 'ca-cadpat': 'ca-2002-cadpat-ppcli-chinook-afghanistan-dod',
 'us-ucp': 'us-2010-ucp-vs-multicam-korengal-dod', 'cn-2007': 'cn-us-2016-type07-ocp-closeup-kunming-dod', 'us-agsu': 'old:us-2022-agsu-portrait-army',
}
STAGE_IMG = {'E1': 'us-1781-surrender-cornwallis-trumbull', 'E2': 'fr-1870-defense-champigny-detaille', 'E3': 'fr-1917-trench-observation-castelnau-autochrome',
             'E4': 'us-1942-infantryman-halftrack-garand-colour-palmer', 'E5': 'us-1967-og107-jungle-fatigues-m16-vietnam-nara', 'E6': 'uk-us-1984-dpm-m81-paratroopers-normandy-dod',
             'E7': 'us-2010-ucp-vs-multicam-korengal-dod', 'E8': 'uk-us-2021-mtp-ocp-paratroopers-fort-bragg-dod'}
PLATES = {'hero': 'uk-1815-28th-quatre-bras-butler', 'c1': 'fr-1914-chasseur-afrique-marne-autochrome', 'c2': 'cn-2017-pla-tri-service-honor-guard-bayi-dod', 'c3': 'uk-1916-royal-irish-rifles-ration-party-somme'}
BIG = set(STAGE_IMG.values()) | set(PLATES.values())

# 核查后（2026-11-10，29 条意见）的图注、作者、年份、许可改正，以及 3+1 个文件改名。图注只在这里改，images.json 是页面图注的唯一出处。
CAP = {
 "us-1967-og107-jungle-fatigues-m16-vietnam-nara": "1967 年 10 月越南广义省德普以西，第 4 步兵师第 35 团 2 营 D 连士兵机降后警戒：橄榄绿丛林作战服、M1 钢盔、M16",
 "ru-1995-vsr93-camo-peacekeeper-kansas-dod": "1995 年 10 月堪萨斯州麦康奈尔基地，“维和者 95”演习中的俄军第 27 近卫摩步师少校与列队士兵，穿迷彩野战服",
 "ru-2001-flora-camo-kosovo-kfor-dod": "2001 年 10 月科索沃东区，俄军第 13 战术群一名士兵（迷彩野战服、钢盔）与当地警察交谈",
 "cn-1988-pla-delegation-type85-hurlburt-dod": "1988 年 6 月佛罗里达州赫尔伯特机场，访美的解放军代表团合影，穿夏常服；此时军衔尚未恢复",
 "cn-2017-pla-tri-service-honor-guard-bayi-dod": "2017 年 8 月 15 日北京八一大楼欢迎仪式，解放军三军仪仗队持枪列队：陆、海、空三种颜色的礼宾服",
 "cn-1800-chinese-military-post-brown": "William Alexander 原画、J. Pass 雕版《中国军事哨所》（1796 年出版，斯当东使团纪行图册；后加手工上色）：清军士兵在哨所前列队",
 "fr-1994-f1-tropical-khaki-goma-dod": "1994 年 8 月扎伊尔戈马机场，两名法军士兵穿素色沙色作战服、戴红贝雷，背 FAMAS",
 "uk-1994-dpm-5-airborne-kigali-dod": "1994 年 8 月卢旺达基加利机场，英军第 5 空降旅医疗与后勤人员抵达，穿 DPM 迷彩、戴联合国蓝贝雷",
 "uk-2005-desert-dpm-basra-iraqi-army-dod": "2005 年 1 月伊拉克巴士拉机场，英军惠灵顿公爵团士兵（沙漠迷彩）与伊拉克陆军士兵在直升机气浪中蹲伏",
 "us-1944-101st-paratroopers-c47-dday-usaaf": "1944 年 6 月 5 日夜，美军第 101 空降师伞兵登机后待命：钢盔加伪装网，脸涂油彩",
 "uk-1943-battledress-mk2-helmet-tunis-parrino": "1943 年 5 月突尼斯，一名妇女给随盟军进城的英军士兵别花：士兵穿 Battledress、戴钢盔",
 "uk-1916-royal-irish-rifles-ration-party-somme": "据信摄于 1916 年 7 月 1 日（索姆河战役首日）：皇家爱尔兰步枪团运粮队在交通壕里休息，Brodie 钢盔与卡其 Service Dress",
 "fr-1807-friedland-cuirassiers-meissonier": "Ernest Meissonier《1807，弗里德兰》（约 1861–75）：胸甲骑兵举刀冲过拿破仑面前",
 "us-1866-prisoners-from-the-front-homer": "Winslow Homer《前线来的俘虏》（1866）：联邦军准将（深蓝）面对三名南军战俘（灰与土褐）",
 "us-1942-infantryman-halftrack-garand-colour-palmer": "1942 年 6 月肯塔基州诺克斯堡，一名步兵戴钢盔，在半履带车旁举加兰德步枪瞄准（彩色反转片）",
 "ru-1865-infantry-cavalry-brown": "Karl Grünwedel 绘，约 1865 年俄国陆军各兵种军服速写（步兵、近卫胸甲骑兵、哥萨克、龙骑兵）；早于本格所写的 1881–82 年改制",
 "uk-us-2021-mtp-ocp-paratroopers-fort-bragg-dod": "2021 年 4 月北卡罗来纳州布拉格堡，英军伞兵（MTP）与美军第 82 空降师伞兵（OCP）列队做跳伞复训",
 "cn-1869-manchu-soldiers-canton-thomson": "John Thomson 摄：1869 年广州的满洲兵丁，深色上衣外罩镶边的浅色坎肩、戴暖帽；据馆方说明，他们是英国领事的卫兵，受过西式操练",
 "cn-1860-chinese-soldier-brown": "Charles Wirgman 水彩《中国士兵》（1860）：《伦敦新闻画报》特派画家在第二次鸦片战争期间所绘，浅色短褂、戴帽，背火枪、持刀",
 "uk-2025-coldstream-scots-guards-buckingham-usarmy": "2025 年 9 月 19 日伦敦白金汉宫前院换岗：冷溪近卫团鼓乐队长（猩红上衣缀金色饰带）与苏格兰近卫团鼓手，都戴熊皮帽",
 "fr-1991-daguet-desert-camo-legion-bugler-dod": "1991 年 3 月科威特城，一名法军号手吹号：沙漠迷彩作战服、深色 képi、黄色流苏肩章",
 "uk-1855-71st-colour-sergeant-fenton": "Roger Fenton 摄：克里米亚的第 71 高地轻步兵团三名军官与一名掌旗军士",
 "cn-1943-chinese-troops-c47-hump-india-usaaf": "约 1943 年，美国陆军航空队运输机里前往印度的中国士兵：缀帽徽的布军帽、棉布军装",
 "fr-us-2017-garde-republicaine-doughboy-ocp-satory-dod": "2017 年 7 月 12 日法国萨托里，国庆阅兵彩排间隙：一名法国军人（深蓝上衣、红裤、带红白羽饰的筒帽）与美军第 1 步兵师士兵——OCP 作战服配一战式碟形钢盔和弹药带",
 "us-1898-rough-riders-san-juan-dinwiddie": "1898 年 7 月古巴圣胡安高地，西奥多·罗斯福上校与“莽骑兵”合影：法兰绒衬衣、宽檐毡帽",
 "us-1781-surrender-cornwallis-trumbull": "John Trumbull《康沃利斯勋爵投降》（1820）：1781 年约克镇，左列法军（前排白衣）、右列大陆军蓝衣，中间步行的红衣者是英军军官",
 "cn-1739-qianlong-armour-castiglione-hd": "（传）郎世宁《乾隆皇帝大阅图》轴（故宫题作《清人画弘历戎装骑马像轴》；1739 或 1758）：乾隆帝着明黄大阅甲、戴胄，骑马阅兵",
 "uk-1980-dpm-smock-para-arnhem-dod": "1980 年 9 月荷兰阿纳姆战役 36 周年纪念，英军空降部队士兵穿 DPM 罩衫、戴红贝雷立正",
 "ru-1992-tamanskaya-winter-afghanka-dod": "1992 年 1 月，塔曼师三名士兵穿冬季棉野战服、戴毛皮帽（美国海军摄）",
 "ru-1910-khaki-gimnastyorka-persia-bain": "驻波斯的俄军士兵列队（Bain 通讯社玻璃底片）：浅色套头 гимнастёрка 与 фуражка",
 "ru-1700-officer-vinkhuijzen": "Vinkhuijzen 军服图集《俄国，1700–33》：1720 年普列奥布拉任斯基近卫团军官，深绿 кафтан、红袖口、三角帽，手持长柄仪仗兵器",
 "uk-us-1984-dpm-m81-paratroopers-normandy-dod": "1984 年 6 月诺曼底圣梅尔埃格利斯，D 日 40 周年跳伞前，都戴红贝雷的英军伞兵（DPM 罩衫、素色绿裤）与美军第 82 空降师（林地迷彩 BDU）同场列队",
 "us-1966-tigerstripe-face-camouflage-101st-vietnam-nara": "1966 年 2 月越南绥和，第 101 空降师第 1 旅远程侦察巡逻队（LRRP）中尉 John Howard 穿虎斑迷彩，出发前往脸上涂伪装油彩",
 "fr-1914-chasseur-afrique-marne-autochrome": "1914–15 年马恩河战场，一名非洲猎骑兵与战马的 autochrome 彩照：天蓝短上衣、茜草红马裤"
}
META = {
 "cn-1860-chinese-soldier-brown": {
  "author": "Charles Wirgman（署 C.W.）"
 },
 "ru-1865-infantry-cavalry-brown": {
  "author": "Karl Grünwedel（未署名，馆方著录）"
 },
 "cn-1943-chinese-troops-c47-hump-india-usaaf": {
  "year": "约 1943"
 },
 "cn-1800-chinese-military-post-brown": {
  "year": "1796"
 },
 "cn-1739-qianlong-armour-castiglione-hd": {
  "year": "1739 或 1758",
  "author": "（传）郎世宁（Giuseppe Castiglione）"
 },
 "ru-1910-khaki-gimnastyorka-persia-bain": {
  "year": "约 1910–1915"
 },
 "us-1864-114th-pennsylvania-zouaves-petersburg": {
  "author": "佚名"
 },
 "cn-1874-qing-soldier-haoyi-thomson": {
  "lic": "公有领域",
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 },
 "cn-1869-manchu-soldiers-canton-thomson": {
  "inst_add": "；Wellcome 作品页编号 19576i"
 },
 "us-1781-surrender-cornwallis-trumbull": {
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 },
 "uk-1759-death-of-wolfe-west": {
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 },
 "uk-1916-somme-brodie-helmet-iwm": {
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 },
 "uk-1916-royal-irish-rifles-ration-party-somme": {
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 },
 "uk-1855-71st-colour-sergeant-fenton": {
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 },
 "us-1898-rough-riders-san-juan-dinwiddie": {
  "lic_url": "https://creativecommons.org/publicdomain/mark/1.0/"
 }
}
RENAME = {
 "uk-1742-foot-guards-1st-vinkhuijzen": "uk-1742-foot-guards-3rd-vinkhuijzen",
 "fr-us-2017-garde-republicaine-doughboy-ocp-satory-dod": "fr-us-2017-french-soldier-doughboy-helmet-ocp-satory-dod",
 "cn-1943-chinese-troops-c47-hump-india-usaaf": "cn-1943-chinese-troops-transport-india-usaaf",
 "fr-1991-daguet-desert-camo-legion-bugler-dod": "fr-1991-desert-camo-bugler-kuwait-dod"
}

def lic_url_old(lic, url):
    if url: return url
    if 'USGov' in lic or 'PD-USA' in lic: return 'https://www.law.cornell.edu/uscode/text/17/105'
    return 'https://creativecommons.org/publicdomain/mark/1.0/'
def lic_name(s):
    s = s.replace('（公有领域贡献）', '')
    if s.startswith('公有领域') or s == 'PD': return '公有领域'
    return s

new = {}
for r in ('U1', 'U2'):
    for x in json.load(open(os.path.join(STAGE, r, 'images.json'), encoding='utf-8')): x['_r'] = r; new[x['id']] = x
old = {v['file'][:-4]: v for v in json.load(open(OLDJ, encoding='utf-8')).values()}

used = []
for lst in list(CELLS.values()) + [[v] for v in CARDS.values()] + [[v] for v in STAGE_IMG.values()] + [[v] for v in PLATES.values()]:
    for k in lst:
        if k not in used: used.append(k)
keep = set(); OUT = {}
os.makedirs(ASSETS, exist_ok=True)
for k in used:
    if k.startswith('old:'):
        o = old[k[4:]]; fn = o['file']; src = os.path.join(OLDA, fn); dst = os.path.join(ASSETS, fn)
        if os.path.abspath(src) != os.path.abspath(dst): shutil.copyfile(src, dst)
        w, h = Image.open(dst).size
        OUT[k[4:]] = dict(id=k[4:], file=fn, w=w, h=h, cap=o['cap'], author=o['author'], inst=o['inst'], year=o['date'], lic=lic_name(o['lic']), lic_note=o['lic'],
                          lic_url=lic_url_old(o['lic'], o['licUrl']), src=o['page'], batch='v1')
        keep.add(fn)
    else:
        n = new[k]; kk = RENAME.get(k, k); fn = n['files']['w1280'].replace(k, kk); keep.add(fn)
        # 1280 版从 2400 版重采样并以 q75 渐进式重存（暂存的 1280 版偏大）；2400 版以 q78 重存
        im = Image.open(os.path.join(STAGE, n['_r'], 'out', n['files']['w2400'])).convert('RGB'); sm = im.copy(); sm.thumbnail((1280, 1280), Image.LANCZOS)
        if k in BIG: keep.discard(fn); fn = n['files']['w2400'].replace(k, kk); keep.add(fn)   # 大图不另存 1280 版，行内也用 2400 版（懒加载）
        else: sm.save(os.path.join(ASSETS, fn), 'JPEG', quality=75, optimize=True, progressive=True)
        if k in BIG: im.save(os.path.join(ASSETS, fn), 'JPEG', quality=78, optimize=True, progressive=True)
        w, h = Image.open(os.path.join(ASSETS, fn)).size
        e = dict(id=kk, file=fn, w=w, h=h, cap=CAP.get(k, n['subject']), author=n['author'], inst=n['inst'], year=n['year'], lic=lic_name(n['license_short']), lic_note=n['license'],
                 lic_url=n['license_url'], src=n['source_url'], batch='v2')
        if k in BIG:
            fb = fn
            e['big'] = fb; e['bw'], e['bh'] = Image.open(os.path.join(ASSETS, fb)).size
        m = META.get(k, {}); e['inst'] += m.get('inst_add', '')
        e.update({x: y for x, y in m.items() if x != 'inst_add'})
        if 'lic' in m: e['lic_note'] = m['lic']
        OUT[kk] = e
for fn in os.listdir(ASSETS):
    if fn not in keep: os.remove(os.path.join(ASSETS, fn))
rn = lambda x: RENAME.get(x[4:] if x.startswith('old:') else x, x[4:] if x.startswith('old:') else x)
strip = lambda d: {k: [rn(x) for x in v] if isinstance(v, list) else rn(v) for k, v in d.items()}
for k in list(CAP) + list(META): assert k in new and k in used, '改正未命中：' + k
json.dump({'images': OUT, 'cells': strip(CELLS), 'cards': strip(CARDS), 'stage': strip(STAGE_IMG), 'plates': strip(PLATES)}, open(os.path.join(HERE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(os.path.join(ASSETS, f)) for f in os.listdir(ASSETS))
print(len(OUT), 'images;', sum(1 for v in OUT.values() if v['batch'] == 'v2'), 'new;', len(keep), 'files;', round(tot / 1e6, 1), 'MB')
