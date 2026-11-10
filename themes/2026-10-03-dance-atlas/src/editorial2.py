# -*- coding: utf-8 -*-
"""第 3 题 v2（2026-11-10 重做）的编辑层：只放「新写的字」和图片清单。事实数据仍在 content.json，不在这里改。
图片说明只写来源页 / 作者说明里有的东西：不臆断民族、地点、舞种。"""

HERO = {
    'mast': ('一周一题 · 第 3 题', '图谱 · 2026 年 10 月 3 日 · 11 月重排'),
    'h1': '舞从劳作来',
    'sub': '从「百兽率舞」到「闪身步」',
    'th': '2026 年 9 月，两段北京舞蹈学院的教学片被网友翻了出来：安徽花鼓灯的「闪身步」，山东鼓子秧歌的「狗熊哆嗦毛」。这一题顺着这两个动作往回走：十二个时代节点，两套动作教材，一张看演出用的对照表。',
    'btn': '从陶盆开始',
    'proof': '{N_NODES} 个节点 · {N_MOVES} 个有要领的动作 · {N_WORKS} 条演出线索 · {N_IMG} 张图',
    'img': 'hero',
}
# 论点：逐词点亮。每行是若干「词」；以 * 开头的词是强调色。
TAGLINE = [
    ['每个', '爆梗的', '动作', '背后，'],
    ['都是', '*一方水土'],
    ['几百年的', '*生产生活。'],
]
TAGREST = '闪身步是淮河两岸雨地里练出来的应变，狗熊哆嗦毛是黄河岸边庄稼汉的劲儿。再往前翻，陶盆上的集体舞、宴席上的长袖、丝路上来的胡乐、正月里的社火，也都是从劳作、仪式和交融里留下来的。'

NAV = [('stage', '序', '五千年'), ('meme', '01', '这一回的梗'), ('nodes', '02', '十二个节点'), ('watch', '03', '去哪儿看'), ('end', '末', '卷末')]

STAGE = {
    'k': '序章 · 五千年走一遍',
    'hint': '往下滚，或拖底下的刻度',
    'open': '展开这一节',
    'note': '地图按现行省级行政区划绘制 · 高亮与路线为文化传播示意，非政区图',
    'ticks': {'n01': '新石器', 'n02': '商周', 'n03': '秦汉', 'n04': '魏晋', 'n05': '隋唐', 'n06': '宋辽金', 'n07': '元', 'n08': '明清', 'n09': '1900', 'n10': '1949', 'n11': '1978', 'n12': '2006'},
}

CH = {
    'meme': {
        'no': '01', 'h2': '这一回的梗', 'img': 'p-meme',
        'lede': '十来天里，两段给专业学生看的训练片成了全网模仿的对象。先看梗是怎么起来的，再把动作一个个拆开：从哪儿来，怎么发力，哪里容易伤；查不到原话的只列名字。',
    },
    'nodes': {
        'no': '02', 'h2': '十二个节点', 'img': 'p-nodes',
        'lede': '从马家窑的陶盆到手机屏幕。每个节点回答同一个问题：这个时代的舞从哪儿来，又和谁混在了一起。',
    },
    'watch': {
        'no': '03', 'h2': '去哪儿看', 'img': 'p-watch',
        'lede': '认得动作之后，去看它们在作品里的样子。十个舞种各给一句看点，十八条演出与影像线索各标出处；只给官方渠道，不嵌第三方视频。',
    },
}

MEME = {
    'ev_h': '梗是怎么起来的', 'ev_note': '横向拖动 · 每条附报道出处',
    'pair_h': '两位老师，两项非遗',
    'lab_h': '把动作放慢看',
    'lab_note': '三个墨线小人的骨架取自两段教学原片；页面不出现任何视频画面。左右拖小人可以逐帧看。',
    'lab_play': '播放', 'lab_pause': '暂停', 'lab_speed': '速度', 'lab_marks': {'prep': '蓄', 'flash': '闪', 'stop': '刹'},
    'lab_marks_k': '定格',
    'lab_open': '看这个动作的全部说明',
    'moves_h': '动作卡', 'moves_note': '要领未见原话的动作只列名字，不编要领',
    'finder_h': '动作查找器', 'finder_ph': '输入动作名，比如：车水步', 'finder_go': '查', 'finder_rand': '随手抽一个',
    'finder_nameonly': '「{name}」出自{deck}，目前只查到名字：教材或报道里没有可引的要领原话，这里不编。',
    'finder_none': '没有找到「{name}」。两套教材里收了 {n} 个动作名，可以从下拉里挑。',
    'labor_h': '动作从哪儿来',
    'labor_note': '车水步有传承人的原话：踩水车浇田。推车、挑担只查到名字，听上去也是地里的活。这里放三张 1900 年代的农事照片（江苏、华北，不是淮河两岸），和今天的淮河。',
    'names_k': '只查到名字的动作',
    'deck_more': '角色、场景、流派与传承人',
    'tolab': '放到台子上看',
    'labels': {'cue': '口诀', 'how': '怎么做', 'life': '从哪儿来', 'role': '谁来跳', 'scene': '场合', 'risk': '当心', 'see': '在哪儿能看到'},
}
NODES = {
    'lens': {'era': '时代', 'spread': '铺开的范围'},
    'era_groups': [('先秦两汉', ['n01', 'n02', 'n03']), ('魏晋至宋元', ['n04', 'n05', 'n06', 'n07']), ('明清', ['n08']), ('1900 年以后', ['n09', 'n10', 'n11', 'n12'])],
    'spread_groups': [('地图上亮两三处省级区划', 0, 3), ('亮四到六处', 4, 7), ('亮八处以上', 8, 99)],
    'more_facts': '其余 {n} 条事实',
    'tomap': '回到地图上看',
    'facts_k': '事实与出处',
}
WATCH = {
    'quick_h': '十个舞种，各看什么', 'quick_note': '点一行展开看点与代表作品',
    'quick_groups': [('汉族民间舞', 'han'), ('少数民族舞', 'eth'), ('当代学院建构与复原', 'aca')],
    'works_h': '十八条演出与影像线索', 'lens': {'genre': '舞种', 'conf': '置信度'},
    'noimg': '这个舞种暂时没有找到授权清楚、内容对得上的照片，先不配图。',
    'labels': {'ethnic': '民族', 'region': '流布', 'motif': '动律', 'props': '道具', 'watch': '看什么', 'works': '代表作品', 'combo': '看点动作', 'troupe': '院团', 'year': '时间', 'where': '位置', 'look': '看什么', 'link': '官方页面'},
}
END = {
    'h2': '卷末',
    'why_h': '为什么是这两个动作', 'method_h': '方法与口径', 'todo_h': '还没核实的', 'refs_h': '参考与出处', 'credits_h': '图片署名',
    'credits_note': '共 {n} 张。博物馆开放获取图像为 CC0 / 公有领域；照片按各自许可署名。',
    'stamp': '一周一题 · 第 3 题 · 2026 年 11 月重排',
    'v2_note': '2026 年 11 月按新版式重排：事实与出处沿用 10 月 3 日首发版，新增图片见署名表；原图说明里没有的民族、地点与舞种，图注一律不写。',
}
CONF = {'高': ('h', '高'), '中': ('m', '中'), '低': ('l', '低')}

# ---------- 图片清单 ----------
# src: ('D1'|'D2', 暂存 id, 2400|1280) 取自图片暂存区；('old', 文件名) 沿用首发版 assets。
# title / cap 为站内中文说明；作者、机构、年份、许可、来源页由 make_images.py 从暂存区 images.json 抄入。
IMG = {
    'hero': dict(src=('D1', 'cn-han-dancer-and-musicians-met-2', 2400), title='彩绘陶舞俑', cap='汉，前 1 世纪至 1 世纪。一组乐舞俑中的舞者：长袖甩开，腰折下去。大都会艺术博物馆藏。'),
    'p-meme': dict(src=('D2', 'cn-2013-street-yangge-red-silk', 2400), title='公园里的秧歌', cap='北京天坛公园，2013 年 10 月。舞着红绸的人迎着镜头笑。'),
    'p-nodes': dict(src=('D1', 'cn-qing-suzhou-print-new-year-cma', 2400), title='苏州版画《新春乐》', cap='清康熙年间（1662–1722）苏州版画：新年的灯棚与歌舞百戏。克利夫兰艺术博物馆藏。'),
    'p-watch': dict(src=('D2', 'cn-2014-outdoor-classical-dance-sleeve-backbend', 2400), title='露天舞台上的长袖', cap='2014 年 10 月，露天舞台。舞者后仰，长袖甩成一道弧。演出者与场地，拍摄者未注明。'),
    # n01
    'n01': dict(src=('old', 'n01.jpg'), title='舞蹈纹彩陶盆', cap='马家窑文化，青海大通上孙家寨 1973 年出土，中国国家博物馆藏。内壁三组各五人，手拉手，头饰与尾饰向同一侧摆动。'),
    'n01-b': dict(src=('D1', 'cn-majiayao-spiral-jar-cma', 1280), title='马家窑文化彩陶罐', cap='前 3300–前 2650 年，漩涡纹，不是舞蹈纹。与舞蹈纹盆同属马家窑文化，放在这里看那一手黑彩。克利夫兰艺术博物馆藏。'),
    # n02
    'n02': dict(src=('old', 'n02.jpg'), title='曾侯乙编钟', cap='战国早期，1978 年湖北随州出土，湖北省博物馆藏。钟磬是雅乐六代舞的伴奏主体。'),
    'n02-b': dict(src=('D1', 'cn-western-zhou-lai-zhong-cma', 1280), title='逨钟', cap='西周，约前 800–前 700 年。克利夫兰艺术博物馆藏。'),
    # n03
    'n03-s': dict(src=('D1', 'cn-han-dancer-and-musicians-met-1', 1280), title='彩绘陶乐舞俑', cap='汉，前 1 世纪至 1 世纪。一位舞者，两位乐人。大都会艺术博物馆藏。'),
    'n03': dict(src=('old', 'n03.jpg'), title='汉画像砖 · 乐舞百戏', cap='东汉画像砖上的乐舞与杂技：盘鼓、长袖、俳优同台。'),
    'n03-b': dict(src=('D1', 'cn-han-court-dancer-sichuan-cma', 1280), title='陶舞俑', cap='东汉，2 世纪，四川。扬袖踏步的舞者。克利夫兰艺术博物馆藏。'),
    'n03-c': dict(src=('D1', 'cn-han-female-dancer-met-1', 1280), title='彩绘陶舞俑', cap='西汉，前 2 世纪。一袖上扬，一袖垂落。大都会艺术博物馆藏。'),
    'n03-d': dict(src=('D1', 'cn-warring-states-jade-dancer-pendant-mia', 1280), title='玉舞人佩', cap='战国，前 480–前 221 年。长袖过顶的舞者被做成了佩饰。明尼阿波利斯艺术博物馆藏。'),
    # n04
    'n04-s': dict(src=('D1', 'cn-northern-qi-flask-central-asian-dancers-met', 1280), title='绿釉扁壶 · 中亚舞者与乐人', cap='北齐，6 世纪晚期。壶腹模印一位舞者，两侧是乐人。大都会艺术博物馆藏。'),
    'n04': dict(src=('old', 'n04.jpg'), title='莫高窟第 285 窟 · 飞天', cap='西魏（535–557）。佛教伎乐把西域乐器与飞舞的身姿画进了敦煌。'),
    'n04-b': dict(src=('D1', 'cn-khotan-flying-celestial-met', 1280), title='彩绘泥塑飞天', cap='于阗（今新疆和田一带），6–7 世纪。大都会艺术博物馆藏。'),
    'n04-c': dict(src=('D1', 'cn-northern-wei-apsara-fragment-met', 1280), title='石灰岩飞天残件', cap='北魏，6 世纪早期。大都会艺术博物馆藏。'),
    # n05
    'n05-s': dict(src=('D1', 'cn-tang-mounted-musicians-cernuschi', 1280), title='彩绘陶骑马女乐俑', cap='唐（618–907）。一队骑在马上的女乐人。巴黎赛努奇亚洲艺术博物馆藏。'),
    'n05': dict(src=('old', 'n05.jpg'), title='莫高窟中唐壁画 · 舞者与大琵琶', cap='中唐（吐蕃时期，781–848）壁画局部：旋转的舞者与大琵琶。'),
    'n05-b': dict(src=('D1', 'cn-tang-female-dancer-cma', 1280), title='彩绘陶舞女俑', cap='唐，650–700 年。一袖高举过头。克利夫兰艺术博物馆藏。'),
    'n05-c': dict(src=('D1', 'cn-tang-foreign-dancer-cernuschi-5897', 1280), title='彩绘陶舞俑', cap='唐（618–907）。卷发的男子抬臂起舞，馆方题名「舞者」。巴黎赛努奇亚洲艺术博物馆藏。'),
    'n05-d': dict(src=('D1', 'cn-tang-xiudingsi-dancer-brick-cma', 1280), title='舞人浮雕砖', cap='唐，870 年以前，出自河南安阳修定寺塔。克利夫兰艺术博物馆藏。'),
    'n05-e': dict(src=('D1', 'cn-tang-musician-lute-met', 1280), title='彩绘陶弹琵琶女乐俑', cap='唐，7 世纪晚期。大都会艺术博物馆藏。'),
    # n06
    'n06-s': dict(src=('D1', 'cn-song-hundred-children-at-play-cma', 1280), title='《百子图》册页（团扇形）', cap='南宋，12–13 世纪，苏汉臣一路画风。庭院里的孩童在扮各种游戏与表演。克利夫兰艺术博物馆藏。'),
    'n06': dict(src=('old', 'n06.jpg'), title='《大傩图》轴', cap='宋，佚名，故宫博物院藏。十二人戴面具、执器物作舞，是乡傩与「舞队」的珍贵图像。'),
    'n06-b': dict(src=('D1', 'cn-jin-cizhou-pillow-hobbyhorse-met', 1280), title='磁州窑童子竹马纹枕', cap='金，12–13 世纪。枕面画一个骑竹马的孩子。大都会艺术博物馆藏。'),
    # n07
    'n07-s': dict(src=('D1', 'cn-yuan-zhongkui-lantern-night-cma-c', 1280), title='《钟馗元夜出游图》卷局部', cap='元，颜辉，13 世纪末至 14 世纪初。卷尾一段：钟馗坐在鬼卒肩上，两个鬼卒捧杯提壶来献酒。馆方说明：画的是新年里扮鬼逐疫的街头艺人。克利夫兰艺术博物馆藏。'),
    'n07': dict(src=('old', 'n07.jpg'), title='元代杂剧壁画', cap='山西洪洞广胜寺明应王殿壁画（1324），题榜「大行散乐忠都秀在此作场」。'),
    # n08
    'n08-s': dict(src=('D1', 'cn-qing-qianlong-southern-tour-suzhou-stage-met', 1280), title='《乾隆南巡图》第六卷局部', cap='清，徐扬，1770 年。苏州城外搭着戏台，台上正在演出。大都会艺术博物馆藏。'),
    'n08': dict(src=('old', 'n08.jpg'), title='《明宪宗元宵行乐图》局部', cap='明，佚名，中国国家博物馆藏。元宵节宫中的杂耍与社火队伍。'),
    'n08-b': dict(src=('D1', 'cn-qing-suzhou-print-new-year-cma', 1280), title='苏州版画《新春乐》', cap='清康熙年间（1662–1722）：新年的灯棚与歌舞百戏。克利夫兰艺术博物馆藏。'),
    'n08-c': dict(src=('D1', 'cn-qing-peking-opera-album-leaf-081', 1280), title='戏曲人物册页', cap='清，19 世纪末至 20 世纪初，绢本设色。头插翎子的旦角。大都会艺术博物馆藏。'),
    # n09–n12
    'n09': dict(src=('old', 'n09.jpg'), title='1945 年 · 群众扭秧歌庆祝抗战胜利', cap='延安新秧歌运动之后，秧歌从田间节庆变成了全民的庆典语言。'),
    'n10-s': dict(src=('D2', 'cn-1972-red-detachment-of-women-broadswords', 1280), title='《红色娘子军》演出现场', cap='北京，1972 年 2 月。芭蕾舞剧《红色娘子军》的群舞：持大刀起舞。美国国家档案馆藏。'),
    'n10': dict(src=('old', 'n10.jpg'), title='1953 年 · 中国青年艺术团的舞者', cap='德国摄影档案（Deutsche Fotothek）里的中国青年艺术团演出：舞者扬起披纱，裙边立着一圈荷花。'),
    'n11-s': dict(src=('D2', 'cn-1995-zhongdian-festival-tibetan-dance', 1280), title='1995 年 · 节日上的长队', cap='云南中甸（今香格里拉），1995 年 6 月。节日上，妇女在草坡前排成长队起舞。'),
    'n11': dict(src=('old', 'n11.jpg'), title='莫高窟九层楼', cap='1979 年《丝路花雨》让敦煌壁画里的舞姿「活」成一个舞种，此后「敦煌舞」成为中国古典舞的一支。'),
    'n12-s': dict(src=('D2', 'cn-yangge-first-month-square-panorama', 1280), title='正月里的秧歌', cap='2012 年 2 月，元宵前。彩门下的秧歌队，四周围满了看的人。彩门横幅上是「榆林市」字样。'),
    'n12-b': dict(src=('D2', 'cn-2015-beijing-jingshan-park-dancing', 1280), title='公园里跳舞的人', cap='北京景山公园，2015 年 1 月。一圈人举臂跳舞，外面围着看客。'),
    'n12-c': dict(src=('D2', 'cn-2013-street-yangge-red-silk', 1280), title='公园里的秧歌', cap='北京天坛公园，2013 年 10 月。'),
    # 劳作
    'deck-hgd': dict(src=('old', 'deck-hgd.jpg'), title='淮河 · 蚌埠', cap='2018 年 6 月的淮河与蚌埠。花鼓灯就在这条河的两岸。'),
    'lab-rice': dict(src=('D2', 'cn-1908-jiangsu-transplanting-rice', 1280), title='插秧', cap='江苏，约 1908 年。水田里弯腰分秧的人。立体照片左幅，美国国会图书馆藏。'),
    'lab-plough': dict(src=('D2', 'cn-1902-north-china-ploughman', 1280), title='犁地', cap='华北，1902 年。扶犁的农人和拉套的牲口。立体照片左幅，美国国会图书馆藏。'),
    'lab-cart': dict(src=('D2', 'cn-1907-north-china-harvest-mule-cart', 1280), title='秋收', cap='华北，1907 年。赶着骡车把高粱运回家。立体照片左幅，美国国会图书馆藏。'),
    # 十舞种
    'q-menggu': dict(src=('D2', 'cn-2008-hohhot-mongolian-folk-dancers-night', 1280), title='夜里的舞者', cap='内蒙古呼和浩特附近，2008 年。拍摄者原注：内蒙古的民间舞者。'),
    'q-zang': dict(src=('D2', 'cn-2011-nyingchi-gongbo-guozhuang-bonfire', 1280), title='篝火边的锅庄', cap='2011 年 5 月。暮色里围着篝火起舞。原题：工布藏族锅庄舞蹈。'),
    'q-zang-b': dict(src=('D2', 'cn-2011-nyingchi-gongbo-guozhuang-line', 1280), title='列队的锅庄', cap='2011 年 5 月。原题：工布藏族锅庄舞蹈。'),
    'q-weiwuer': dict(src=('D2', 'cn-2008-kashgar-uyghur-dancer', 1280), title='葡萄长廊下的舞者', cap='新疆喀什，2008 年。'),
    'q-weiwuer-b': dict(src=('D2', 'cn-2010-yarkand-meshrep-musicians', 1280), title='麦西来甫上的乐手', cap='新疆莎车，2010 年 9 月。画面里是伴奏的乐手：手鼓与弦。'),
    'q-chaoxian': dict(src=('D2', 'cn-2008-korean-changgu-drum-dance-stage', 1280), title='长鼓', cap='2008 年，舞台演出：斜挎长鼓的舞者。原题：朝鲜长鼓舞；拍摄者标签：北京。'),
    'q-gudian': dict(src=('D2', 'cn-2015-shanghai-water-sleeve-dancer-red', 1280), title='水袖', cap='上海人民广场，2015 年 5 月。戏曲的水袖；拍摄者标签：上海淮剧团、水袖舞。'),
    'q-gudian-b': dict(src=('D2', 'cn-2017-xian-tang-show-long-silk-dance', 1280), title='长袖', cap='西安，2017 年 5 月，仿唐乐舞演出。拍摄者注：白纻舞。舞者把加长的白袖抡成环。'),
}
# 各处用哪几张图
NODE_IMGS = {
    'n01': ['n01', 'n01-b'], 'n02': ['n02', 'n02-b'], 'n03': ['n03-s', 'n03', 'n03-b', 'n03-c', 'n03-d'],
    'n04': ['n04-s', 'n04', 'n04-b', 'n04-c'], 'n05': ['n05-s', 'n05', 'n05-b', 'n05-c', 'n05-d', 'n05-e'],
    'n06': ['n06-s', 'n06', 'n06-b'], 'n07': ['n07-s', 'n07'], 'n08': ['n08-s', 'n08', 'n08-b', 'n08-c'],
    'n09': ['n09'], 'n10': ['n10-s', 'n10'], 'n11': ['n11-s', 'n11'], 'n12': ['n12-s', 'n12-b', 'n12-c'],
}
QUICK_IMGS = {
    '东北秧歌': [], '胶州秧歌': [], '云南花灯': [], '蒙古族舞': ['q-menggu'], '藏族舞': ['q-zang', 'q-zang-b'],
    '维吾尔族舞': ['q-weiwuer', 'q-weiwuer-b'], '朝鲜族舞': ['q-chaoxian'], '傣族舞': [], '中国古典舞': ['q-gudian', 'q-gudian-b'], '敦煌舞': ['n04', 'n05'],
}
LABOR_IMGS = ['deck-hgd', 'lab-rice', 'lab-plough', 'lab-cart']

# 核查后对底稿两处的改正（2026-11-10 核查 T4 / T5）：content.json 不动，构建时替换并断言各命中一次。
FIXES = [
    ('村田乐、鼓板、打夜胡是秧歌、花鼓、社火的直接前身', '村田乐、鼓板、打夜胡，已有后世秧歌、花鼓、社火的雏形'),
    ('图片均来自 Wikimedia Commons 的公有领域或 CC 授权文件，图注里给出作者与许可证。', '图片来自博物馆开放获取图像、美国国会图书馆与国家档案馆、Wikimedia Commons 和 Flickr 的公有领域或 CC 授权文件，逐张署名见卷末。'),
]
