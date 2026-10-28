# -*- coding: utf-8 -*-
"""第 7 题「冬天的门槛」编辑文案与配置。研究底稿在 research/fest_{A,B,C,D}.json；这里只放编辑自己写的句子和各章取哪些节点。
改研究底稿里的句子不要动 JSON，往 fixes.py 的 POST 表里加一行。"""

META = dict(
    no=7, slug='winter-threshold', date='2026-10-31',
    title='冬天的门槛：不同纬度与气候下，各文明为什么在同一个季节祭亡灵、点灯火',
    subtitle='从北纬 53 度的 Samhain 到北纬 17 度的水灯节——万圣节、亡灵节、篝火夜、立冬、排灯节、寒衣节落在同十天里；收成、季风、霜期与历法怎样决定它们的同与异。附「纬度与门槛」「算日子」小工具。',
    desc='节日跟着收成走，收成跟着气候走，气候跟着纬度和地形走。十天里七个节日——万圣节、诸圣诸灵、亡灵节、篝火夜、立冬、排灯节、寒衣节——都落在「一年的门槛」上。一张「夜的田野」图谱、十五座城市的灯、二十一个节日的来历、按纬度 / 气候 / 历法 / 传播比较的同与异，两面动手墙，三个小工具。',
    tags=['吃喝玩乐', '节庆', '气候', '历法', '全球史'],
    format='图谱 · 夜的田野 · 同与异 · 两面墙 · 三个小工具',
    reading_time='30 分钟', cover_focus='#field', cover_scheme='dark')

HERO = dict(
    thesis='节日跟着收成走，收成跟着气候走，气候跟着纬度和地形走。<em>十天里七个节日</em>——万圣节、诸圣诸灵、亡灵节、篝火夜、立冬、排灯节、寒衣节——都落在「一年的门槛」上：收成入仓、牲口回圈、雨季结束、白昼变短。人们在门槛上做同样的三件事：请亡灵回家吃一顿，把夜点亮，把过冬的衣食备好。可它们落在不同的日子、用着不同的东西——那一半来自纬度与气候，另一半来自历法与传播。',
    steps=['先看「夜的田野」：越往北，黑夜来得越早，灯也点得越早；十天里的七盏灯都在最暗的那道坡上。',
           '再看「门槛」与「同与异」：每个节日落在哪个纬度、什么气候，那时当地在收什么、怕什么，日子是月亮定的还是公历钉的，节日是本土长的还是搬来的。',
           '最后拨一拨：纬度滑块、年轮，算算明年这些节日落在哪天——同一轮新月，印度 11/8 点灯、中国 11/9 送寒衣。'],
    week=[('10/31', '万圣节', '都柏林 · 纽约 · 墨西哥城大游行 14:00'), ('11/1–2', '亡灵节', '墨西哥城 · 拉巴斯 · 诸圣诸灵'), ('11/5', '篝火夜', '刘易斯'),
          ('11/7', '立冬', '北京 17:52'), ('11/8', '排灯节', '德里 · 加德满都'), ('11/9', '寒衣节', '北京 · 农历十月初一')],
    # 卷首三块数字（入视口计数）
    stats=[('这十天', 7, 0, '个节日', '10/31 万圣节 → 11/9 寒衣节', '万圣节、诸圣诸灵与亡灵节、篝火夜、立冬、排灯节、寒衣节'),
           ('纬度跨度', 87, 0, '度', '北纬 53.4°（都柏林）→ 南纬 33.9°（悉尼）', '同一个日历日，北海草停牛归，悉尼仲春讨糖'),
           ('昼长之差', 3.8, 1, '小时', '10/31 都柏林 9 时 37 分 · 悉尼 13 时 25 分', '越往北，夜越长，灯点得越早')])

CHAPTERS = [
    ('days', 0, '这十天', '上线当天是万圣节，十天里七个节日接力：地图上的灯一盏一盏点起来，每一盏旁边写着那座城那天的昼长。'),
    ('now', 1, '这一周', '四件正在发生的事，只当入口：墨西哥城的大游行、万圣节的生意、同一轮新月上的两个节、立冬与天文学上的 Samhain。'),
    ('threshold', 2, '门槛：为什么是这个季节', '二十一个节日的来历，按欧洲、东亚、南亚与东南亚、美洲四条泳道排在年轮上。先看每一个是怎么长出来的，再看它压在哪一道门槛上。'),
    ('compare', 3, '同与异', '把这些节日放到同一把尺子上：纬度、当天昼长、气候带、农事门槛、历法基础、传播路径。按任一列排序，相似的会自己聚在一起。'),
    ('three', 4, '三件事', '请亡灵回家，把夜点亮，吃一顿——七种节日各自用什么东西做这三件事，以及这些东西和当地物产的关系。'),
    ('walls', 5, '两面墙', '动手：拖纬度和日期看黑夜怎么变长、哪些灯在那个纬度带上；转年轮，把别家的岁首对到顶上，看你家的节日落在哪。'),
    ('tools', 6, '三个小工具', '算日子（任一年份各节日落在哪天）、同与异对照（任选两个并排）、看点清单（今年想去哪个节）。'),
    ('rules', 7, '规则是怎么写的', '十一份文件：历法规则、政府公告、非遗名录与气象口径——页面上的日子和数字从哪来。'),
]

# 序章七步：日期、点亮的城市、主城（算昼长）、题目、一句话、照片
STEPS = [
    dict(id='d1031', date='2026-10-31', wd='六', kicker='万圣节 · Samhain · 亡灵节前夜', title='灯从最北边点起',
         cities=['dublin', 'new-york', 'mexico-city', 'sydney'], main='dublin',
         text='都柏林这天白昼只有九个半小时多一点，夏末（Samhain）与冬天在这里交接：牲口 5 月初赶上夏牧场、11 月初赶回圈。纽约的万圣节是同一个日子搬过大西洋后的样子，门槛从霜期变成了货架期；墨西哥城下午两点，亡灵节大游行从改革大道走向宪法广场；悉尼则在仲春过节，昼长十三小时。',
         photo='img-halloween-1', fest=['samhain', 'halloween', 'halloween-south']),
    dict(id='d1101', date='2026-11-01', wd='日', kicker='诸圣节 · 亡灵节首日 · Todos Santos', title='同一个日历日，两个半球',
         cities=['rome', 'mexico-city', 'la-paz'], main='mexico-city',
         text='教会日历把众圣与众亡者放在 11 月初，日子钉死，气候各走各的：罗马是秋雨季与橄榄采收，墨西哥高原是雨季刚停、玉米收完、万寿菊正开，拉巴斯却在南半球的春天——旱季转雨季，马铃薯随雨播种，亡魂回家被理解为「把雨带回来」。',
         photo='img-dia-de-muertos-10', fest=['all-saints-souls', 'dia-de-muertos', 'todos-santos-andes']),
    dict(id='d1102', date='2026-11-02', wd='一', kicker='诸灵节 · 亡灵节正日', title='祭坛上的面包与蜡烛',
         cities=['rome', 'mexico-city', 'la-paz'], main='rome',
         text='11 月 2 日是成人的亡灵日。墨西哥的 ofrenda 摆亡灵面包、糖骷髅、万寿菊与蜡烛；玻利维亚高原的 apxata 祭桌铺黑布、架甘蔗、摆面包人 t\'anta wawa；欧洲的墓地点满烛光。请亡灵回家吃一顿，这件事在三块大陆上用三套东西做。',
         photo='img-all-saints-souls-1', fest=['all-saints-souls', 'dia-de-muertos', 'todos-santos-andes']),
    dict(id='d1105', date='2026-11-05', wd='四', kicker='篝火夜', title='草停了，田里有东西可烧',
         cities=['lewes'], main='lewes',
         text='英格兰南岸的刘易斯这天日落四点半。篝火夜的日子来自 1605 年的火药阴谋和 1606 年的议会法案，与农事无关；可它长在和 Samhain 篝火同一个季节里——收成已毕、秸秆枯枝可烧、牧草停长。史家说两者没有承接关系，这正是「同季节未必同来源」的例子。',
         photo='img-bonfire-night-1', fest=['bonfire-night']),
    dict(id='d1107', date='2026-11-07', wd='六', kicker='立冬 17:52 · Tihar 乌鸦日', title='太阳到了秋分与冬至的正中',
         cities=['beijing', 'tokyo', 'kathmandu'], main='beijing',
         text='太阳黄经 225°，北京时间 17:52 立冬。这个时刻在天文学上就是凯尔特的「跨季日」——Samhain 的天文定义；中国把它钉在黄河流域的物候上：「水始冰，地始冻」，北京常年 10 月 30–31 日入冬，11 月 8 日第一次跌破冰点。加德满都这天开始五天的 Tihar，先谢乌鸦。',
         photo='img-lidong-2', fest=['lidong', 'tihar']),
    dict(id='d1108', date='2026-11-08', wd='日', kicker='排灯节 · 吉祥天女祭', title='季风退去后的第一个无月夜',
         cities=['delhi', 'kathmandu'], main='delhi',
         text='印度气象局常年口径：西南季风 9 月 25 日撤出德里，10 月 15 日撤出全国；排灯节钉在之后的迦底迦月朔——今年就是撤退后的第一个新月，kharif 稻谷正在收。amavasya 从 8 日中午起、到 9 日 12:32（印度时间）的朔为止：8 日日落时正当值、9 日日落前已过，所以 11 月 8 日点灯。加德满都同一晚祭吉祥天女，「女神不进暗屋」。',
         photo='img-diwali-3', fest=['diwali', 'tihar']),
    dict(id='d1109', date='2026-11-09', wd='一', kicker='寒衣节 · 农历十月初一', title='同一轮新月，中国晚一天',
         cities=['beijing'], main='beijing',
         text='北京时间 15:02 朔，按《农历的编算和颁行》，含朔时刻的那一天为初一，这天是十月初一——印度按日落时的 tithi 在前一天点灯，中国按含朔之日在这天送寒衣，同一个天象差出一天。十月朔在秦与汉初做过一百多年的岁首；《诗经》说「九月授衣」，宋人这天出城上坟，明人在门口焚化纸衣。',
         photo='img-hanyi-3', fest=['hanyi', 'qin-new-year']),
    dict(id='dnext', date='2026-11-11', wd='三', kicker='再往后 · 11/11 → 12/13', title='灯一路往南、往北点下去',
         cities=['utrecht', 'tokyo', 'sukhothai', 'stockholm'], main='stockholm',
         text='11 月 11 日乌得勒支的孩子提灯笼讨糖、德国人吃圣马丁鹅；11 月 15 日东京的七五三；11 月 23 日新尝祭与下元节；11 月 24 日素可泰的满月夜放水灯，雨季刚停、河水最满；12 月 13 日斯德哥尔摩的圣露西亚，白昼只剩六小时——越往北、越近冬至，点灯的日子越晚。',
         photo='img-lucia-1', fest=['martinmas', 'shichigosan', 'niinamesai', 'xiayuan', 'loy-krathong', 'lucia']),
]

# 第二章四条泳道
LANES = [('europe', '欧洲', ['samhain', 'all-saints-souls', 'halloween', 'bonfire-night', 'martinmas', 'lucia', 'rome-contrast']),
         ('eastasia', '东亚', ['qin-new-year', 'hanyi', 'lidong', 'xiayuan', 'shichigosan', 'niinamesai']),
         ('southasia', '南亚与东南亚', ['diwali', 'tihar', 'loy-krathong']),
         ('americas', '美洲', ['dia-de-muertos', 'todos-santos-andes', 'halloween-south']),
         ('contrast', '另一道门槛', ['zhongyuan-contrast', 'pchum-ben'])]
# 哪些节点是「反例 / 对照」
CONTRAST = {'rome-contrast', 'halloween-south', 'zhongyuan-contrast', 'pchum-ben'}

# 节点卡配图（图片 id → 见 images.json）
NODE_IMG = {'samhain': 'img-samhain-1', 'halloween': 'img-halloween-2', 'all-saints-souls': 'img-all-saints-souls-2', 'rome-contrast': 'img-rome-contrast-1',
            'bonfire-night': 'img-bonfire-night-1', 'martinmas': 'img-martinmas-2', 'lucia': 'img-lucia-1', 'todos-santos-andes': 'img-todos-santos-andes-3',
            'halloween-south': 'img-halloween-4', 'hanyi': 'img-hanyi-1', 'lidong': 'img-lidong-1', 'xiayuan': None, 'zhongyuan-contrast': 'img-zhongyuan-contrast-1',
            'shichigosan': 'img-shichigosan-2', 'niinamesai': 'img-niinamesai-2', 'qin-new-year': 'img-hanyi-2', 'diwali': 'img-diwali-2', 'tihar': 'img-tihar-2',
            'loy-krathong': 'img-loy-krathong-1', 'pchum-ben': None, 'dia-de-muertos': 'img-dia-de-muertos-13'}

# 第三章「同与异」：每行一个节日；city 用 research/fest_D.json 的 cities 表（纽约另加）；season 是编辑写的四字门槛，threshold_key 是「门槛类型」
COMPARE = [
    dict(id='samhain', city='dublin', season='牲口回圈 · 草停', kind='harvest', note='夏与冬的接缝；「凯尔特新年」有争议'),
    dict(id='halloween', city='new-york', season='货架期 · 初霜前', kind='none', note='日子搬过大西洋，门槛从霜期变成零售日历'),
    dict(id='all-saints-souls', city='rome', season='秋雨始 · 橄榄收', kind='calendar', note='教会定日，气候各地各走'),
    dict(id='dia-de-muertos', city='mexico-city', season='雨季末 · 玉米收完', kind='harvest', note='祭亡本在夏末，被教会日历搬到 11 月'),
    dict(id='todos-santos-andes', city='la-paz', season='旱转雨 · 播种', kind='sowing', note='南半球春天，亡魂「把雨带回来」'),
    dict(id='bonfire-night', city='lewes', season='草停 · 夜长', kind='event', note='议会定日，与 Samhain 篝火无承接'),
    dict(id='martinmas', city='utrecht', season='宰鹅 · 结账', kind='harvest', note='农事年的结算日'),
    dict(id='lucia', city='stockholm', season='长夜 · 白昼 6 小时', kind='night', note='纬度阶梯的北端'),
    dict(id='lidong', city='beijing', season='水始冰 · 入冬', kind='solar', note='与天文 Samhain 同一时刻'),
    dict(id='hanyi', city='beijing', season='破冰点 · 冬麦已播', kind='harvest', note='曾做过一百多年的岁首'),
    dict(id='xiayuan', city='beijing', season='小雪后 · 冬初', kind='calendar', note='道教三元的第三个「元」'),
    dict(id='shichigosan', city='tokyo', season='红叶季 · 稻已入仓', kind='calendar', note='给活着的孩子穿衣谢神'),
    dict(id='niinamesai', city='tokyo', season='新米入仓', kind='harvest', note='收成门槛被钉成固定日'),
    dict(id='diwali', city='delhi', season='季风退 · 稻正收', kind='monsoon', note='季风撤退后的迦底迦月朔（2026 年即第一个新月）'),
    dict(id='tihar', city='kathmandu', season='季风退 · 收稻', kind='monsoon', note='兼尼瓦尔岁首'),
    dict(id='loy-krathong', city='sukhothai', season='雨季末 · 水最满', kind='monsoon', note='最靠近赤道的一盏灯'),
    dict(id='halloween-south', city='sydney', season='仲春 · 无门槛', kind='none', note='反例：日子钉在公历上，气候缺席'),
    dict(id='zhongyuan-contrast', city='beijing', season='雨季尾 · 青黄不接', kind='religion', note='另一道门槛：佛教自恣日'),
    dict(id='pchum-ben', city='phnom-penh', season='雨安居将尽', kind='religion', note='另一道门槛：僧团日历'),
]
KIND_NAME = {'harvest': '收成后', 'sowing': '播种前', 'monsoon': '季风退', 'night': '长夜', 'solar': '太阳历', 'calendar': '日历定', 'event': '事件定', 'religion': '宗教历', 'none': '无门槛'}
BASIS_NAME = {'gregorian-fixed': ('固定日', '公历'), 'lunisolar-chinese': ('跟月亮', '农历'), 'lunisolar-hindu': ('跟月亮', '印度历'), 'solar-term': ('跟太阳', '节气'), 'thai-lunar': ('跟月亮', '泰 / 高棉历'), 'rule': ('按规则', ''), 'southern-transplant': ('固定日', '公历')}
SPREAD_NAME = {'native': '本土', 'church-calendar': '宗教日历', 'migration': '移民', 'commercial': '商业', 'transplant': '移植'}

# 「同」五条、「异」四根轴（都要指回矩阵里的证据）
SAME = [('门槛', 15, '十九行里十五行落在「收成入仓 / 雨季结束 / 牲口回圈」之后的两到六周内，安第斯的 Todos Santos 则压在播种前；三个例外都在最后三行：悉尼的万圣节在仲春，中元与 Pchum Ben 在雨季将尽、青黄不接的时候。'),
        ('长夜', 4, '北纬 50° 以北的四行（圣露西亚、Samhain、圣马丁节、篝火夜）当天昼长都不到 10 小时，最北的圣露西亚只剩 6 小时 12 分；北京、纽约、罗马这一线在 10 到 10 个半小时上下。'),
        ('亡灵', 10, '十九行里十行有「请亡灵回家」这一件事——爱尔兰、天主教欧洲、华北、墨西哥高原、安第斯、尼泊尔、柬埔寨各自在同一个季节做；立冬、七五三、新尝祭、排灯节、水灯节不祭亡。'),
        ('灯火', 14, '十九行里十四行有灯或篝火：萝卜灯、南瓜灯、diya、水灯、灯笼、篝火、烛光；没有的五行是寒衣、立冬、七五三、新尝祭与 Pchum Ben。'),
        ('吃一顿', 18, '除水灯节外每一行都有一样专属的食物，而且多半是刚收下来的东西或过冬前要处理掉的牲口。')]
DIFF = [('纬度', '决定昼长与霜期，门槛的「日子」随纬度南移而推后：北纬 53° 的都柏林 10 月底，北纬 40° 的北京立冬前后，北纬 29° 的德里季风退去后，北纬 19° 的墨西哥城旱季初，北纬 17° 的素可泰雨季末；南半球整个颠倒。', ['samhain', 'lidong', 'diwali', 'dia-de-muertos', 'loy-krathong', 'todos-santos-andes']),
        ('气候与地理', '决定收的是什么、怕的是什么，于是「东西」不同：温带旱作的篝火与根菜灯、华北的寒衣与饺子、季风区秋收后的油灯与甜食、高原旱季初开的万寿菊、河网里的水灯。', ['bonfire-night', 'hanyi', 'diwali', 'dia-de-muertos', 'loy-krathong']),
        ('历法', '决定日子固定还是漂移：钉在公历上的（万圣节、亡灵节、圣马丁）、跟月亮走的（排灯节、寒衣节、水灯节）、跟太阳走的（立冬）。同一轮新月，印度按日落时的 tithi 在 11/8 点灯，中国按含朔之日在 11/9 送寒衣；立冬与天文学上的 Samhain 是同一个时刻的两种叫法。', ['halloween', 'diwali', 'hanyi', 'lidong', 'loy-krathong']),
        ('传播', '决定节日和气候还对不对得上：本土长出的（Samhain、十月朔、排灯节）、随宗教日历移植的（诸圣诸灵覆盖到中美洲，再被搬到南半球春天的安第斯）、随移民与商业改装的（万圣节的南瓜与糖果、澳大利亚春天的万圣节）——节日一旦制度化就会脱离气候。', ['samhain', 'all-saints-souls', 'todos-santos-andes', 'halloween', 'halloween-south'])]

# 第四章 三件事：七种节日 × 三件事；每格 (一句话, 图片 id 或 None)；图片从 images.json 取
THREE_ROWS = ['samhain-halloween', 'dia-de-muertos', 'bonfire-martinmas', 'hanyi-lidong', 'diwali', 'tihar', 'loy-krathong']
THREE = {
    'samhain-halloween': dict(name='Samhain · 万圣节', city='都柏林 → 纽约', dead=('亡灵与「他界」之门在这一夜开着；中世纪英格兰的 soul cakes 与 souling：孩子挨户讨「灵魂饼」，替亡者祈祷。', 'img-halloween-2'),
                              light=('爱尔兰人把大头菜挖空刻鬼脸、放蜡烛；到了北美换成南瓜——北美 9–10 月采收的作物。', 'img-halloween-3'),
                              food=('苹果、坚果、barmbrack 果子面包与 colcannon 土豆卷心菜泥：10 月底收完的东西；北美则是糖果——货架上的东西。', 'img-halloween-1')),
    'dia-de-muertos': dict(name='亡灵节', city='墨西哥城', dead=('家中与公墓的 ofrenda 祭坛：照片、蜡烛、水、盐、亡者爱吃的东西；万寿菊花瓣铺成一条路，引亡魂回家。', 'img-dia-de-muertos-13'),
                           light=('蜡烛与万寿菊（cempasúchil，Tagetes erecta）：七月种下、约九十天开花，正赶上旱季初的祭坛。', 'img-dia-de-muertos-11'),
                           food=('亡灵面包 pan de muerto、糖骷髅、玉米做的 tamales 与 atole——玉米年度栽培周期的完成（UNESCO 条目原话）。', 'img-dia-de-muertos-12')),
    'bonfire-martinmas': dict(name='篝火夜 · 圣马丁节', city='刘易斯 · 乌得勒支', dead=('篝火夜不祭亡灵，烧的是 Guy 的人偶；圣马丁节也不祭亡灵——它是北海沿岸农事年的结账日。', None),
                              light=('篝火：收成后田里有秸秆枯枝可烧；灯笼：荷兰、比利时的孩子提自制灯笼挨户唱歌。', 'img-martinmas-1'),
                              food=('圣马丁鹅（Martinsgans）：牧草停长、牲口只能靠干草过冬，宰杀腌制的季节；博若莱新酒原在 11/15 上市，1985 年改到第三个周四。', 'img-martinmas-2')),
    'hanyi-lidong': dict(name='寒衣节 · 立冬', city='北京', dead=('送寒衣：纸店裁五色纸做尺把长的纸衣，写上先人名字辈分，夜里在门口呼名焚化（《帝京景物略》）；宋人「士庶皆出城飨坟」。', 'img-hanyi-1'),
                         light=('焚纸衣与纸钱的火；《礼记·月令》孟冬「天子始裘」，官府进暖炉炭，民间置酒作「暖炉会」。', 'img-hanyi-3'),
                         food=('立冬饺子（北方）与「补冬」的姜母鸭、麻油鸡（闽台）；宋开封十月一日「宰臣已下受衣着锦袄三日」。', 'img-lidong-1')),
    'diwali': dict(name='排灯节', city='德里', dead=('排灯节不祭亡灵，请的是吉祥天女；Yama Deepam 为阎摩点一盏灯是北印度部分地区的习俗。', None),
                   light=('diya 油灯：陶土小盏盛酥油或芝麻油，一排排点在门槛、窗台与屋顶；烟花。灯点在季风退去后最暗的无月夜。', 'img-diwali-1'),
                   food=('mithai 甜食、kharif 新收的稻谷与甘蔗；商人在吉祥天女前开新账本（Chopda Pujan）——收成变现的时点。', 'img-diwali-3')),
    'tihar': dict(name='Tihar', city='加德满都', dead=('五天逐日酬谢乌鸦、狗、牛、牛王——阎摩的使者与农事伙伴；第五天兄妹节以额上的 tika 留住兄长。', 'img-tihar-1'),
                  light=('门前 diyo 油灯与 rangoli 彩粉，画出吉祥天女的脚印：「女神不进暗屋」。', 'img-tihar-2'),
                  food=('sel roti 米粉环饼、稻作 10–12 月收后的新米；兄妹节的果仁与甜食。', 'img-tihar-3')),
    'loy-krathong': dict(name='水灯节', city='素可泰', dead=('不祭亡灵：向水之女神（Phra Mae Khongkha）致意，把霉运随水灯放走。', None),
                         light=('芭蕉叶折成的水灯（krathong）插香烛放到河上；兰纳的 Yi Peng 放天灯——同一轮满月。', 'img-loy-krathong-2'),
                         food=('主季稻 10 月初开镰；雨停、水满、稻熟三件事同时到来。', 'img-loy-krathong-1')),
}
THREE_COLS = [('dead', '请亡灵回家'), ('light', '把夜点亮'), ('food', '吃一顿')]

WALLS = [
    dict(id='lat', title='纬度与门槛', formula='昼长 = 2·arccos(−tan φ · tan δ) / 15°', text='拖纬度和日期：曲线是那条纬线上一年的昼长，竖线是你选的日子；读数给昼长、日落（按经度 0° 的平太阳时）与「夜占多少」。右侧列出落在这个纬度带（±8°）上的节日与它们核心城市的气候口径。公式按太阳赤纬的标准近似，不计大气折射与海拔，误差在几分钟内。'),
    dict(id='wheel', title='年轮', formula='一圈 = 365 天', text='把年画成一个圆，每个节日按 2026 年的日子落在圆上。选一个文明的「岁首」转到顶上——公历 1 月 1 日、春节、秦的十月朔、古吉拉特的排灯节次日、尼泊尔历元旦、泰国宋干——看别家的节日落在你家年轮的哪一段。两道门槛（夏末与冬初）用底色标出。'),
]
TOOLS = [
    dict(id='dates', title='算日子', lede='输入一个年份，各节日落在哪天：固定日按公历，立冬按太阳黄经 225°，寒衣节与下元按农历十月初一 / 十五，排灯节按 amanta 历朔日与日落 tithi，水灯节按泰国官方表（2015–2027）或天文望日（±1 天）。'),
    dict(id='pair', title='同与异对照', lede='任选两个节日并排：纬度、当天昼长、气候带、农事门槛、历法、传播与三件事。'),
    dict(id='list', title='看点清单', lede='今年想去哪个节：日期、必看、必吃与礼仪，一页可截图。'),
]

# 第七章 规则文件：('年份 / 性质', '标题', '一句话', 来源查找键: (节点 id, 正则))
RULES = [
    ('1147 成书', '《东京梦华录》卷九「十月一日」', '「宰臣已下受衣著锦袄三日，士庶皆出城飨坟」——寒衣节最早的节俗记载。', ('hanyi', r'东京梦华录|维基文库|ctext')),
    ('前 221 / 前 104', '《史记·秦始皇本纪》《汉书·律历志》', '「改年始，朝贺皆自十月朔」；太初元年「以正月为岁首」——十月初一做过岁首。', ('qin-new-year', r'汉书|史记|维基文库')),
    ('2017', 'GB/T 33661-2017《农历的编算和颁行》', '含朔之日为初一、无中气置闰、以北京时间为准——寒衣节与下元节的日子由此而来。', ('hanyi', r'33661|天文台|hko')),
    ('2016', 'UNESCO 人类非物质文化遗产：二十四节气', '「中国人通过观察太阳周年运动而形成的时间知识体系」——立冬的来处。', ('lidong', r'unesco|UNESCO')),
    ('2008', 'UNESCO 人类非物质文化遗产：墨西哥亡灵节', '「Indigenous festivity dedicated to the dead」——条目写明节日标志玉米年度栽培周期的完成。', ('dia-de-muertos', r'unesco|UNESCO')),
    ('每年', '印度中央政府假日备忘录（DoPT）', '每年公布「Diwali (Deepavali)」一日并附 Saka 历日期；页面用 2015–2027 年的官方日期校准算法。', ('diwali', r'dopt|DoPT|holiday|Holiday')),
    ('每年', '泰国旅游局 / 政府门户水灯节公告', '2026 年素可泰「水灯与烛光节」11/15–24；正日按泰历十二月望。', ('loy-krathong', r'thailand\.go\.th|tourismthailand|TAT')),
    ('1606 / 1859', '《11 月 5 日纪念法》与 1859 年废止法', '议会立法定下的篝火夜，维持了 253 年。', ('bonfire-night', r'legislation|Act|法')),
    ('2020', '印度气象局季风常年日期', '西南季风 9/17 自西拉贾斯坦开始撤退、9/25 撤出德里、10/15 撤出全国。', ('diwali', r'imd|IMD|mausam|气象局')),
    ('2018', 'Beck 等《1 km 分辨率的现在与未来柯本气候分类图》', '页面上每座城市的气候带（Cfb、Dwa、Aw…）按经纬度从这套数据读取。', ('cities', r'Beck|sdata|nature')),
    ('常年', '北京市气象台入冬与破冰点日 · 国家气候中心华北雨季', '北京常年 10 月 30–31 日入冬、11 月 8 日首次跌破冰点；华北雨季 7/18–8/17。', ('hanyi', r'气象|气候')),
]

METHOD = dict(
    process=['研究分四路（欧美与南半球 / 中国与日本 / 南亚与东南亚 / 中美洲与十五城气候数据），每路 ≤25 次搜索，先写骨架再边核边填；底稿 JSON 进了仓库 src/research/，每条事实带来源与置信度。',
             '日期：固定日按公历；立冬、小雪、冬至按太阳视黄经 225° / 240° / 270°（PyEphem，换算北京时间），2024–2026 年与紫金山天文台 / 国立天文台公布值相差不超过 1 分钟；农历十月初一与十五查第 6 题按 GB/T 33661-2017 生成的月表；排灯节按 amanta 历「含入天秤 sankranti 的朔望月为阿湿缚庾阇月」取其末朔，再按德里日落 pradosh 时段 amavasya 是否当值定日，2015–2027 年 13 个官方日期全部对上；水灯节用泰国官方表，其它年份只给天文望日并标 ±1 天。',
             '昼长与日落：按太阳赤纬的标准近似公式现算（不计折射与海拔），误差在几分钟内；页面上所有昼长都按核心城市的纬度算。',
             '气候：柯本类型按 Beck 等 2018 的 1 km 数据集逐城读取；雨季、季风、初霜、收成优先用各国气象 / 农业部门与 FAO GIEWS 的口径，核不到的城市标「通行口径」并写进待核。',
             '「气候决定节日」只写成相关与门槛，不写成因果；南半球移植的节日与钉在公历上的节日作反例并列。宗教与民族表述只用史料与官方 / 学术口径，不评价习俗。',
             '图片只用公有领域、CC0、CC BY、CC BY-SA 与「无已知版权限制」的来源（纽约公共图书馆、国会图书馆、大都会与克利夫兰艺术博物馆 Open Access、Rijksmuseum、Wellcome、Europeana 合作馆、geograph、NASA、pxhere / WordPress 图库），逐张记入 src/images.json 并在卷末署名；Flickr 与维基共享资源在构建环境里打不开，没有合规照片的格子不放图。',
             '核查：页面做完后两路子代理对照来源重读全页，查实的错误改进 src/fixes.py 的替换表，存疑的改为两说并列。'],
    todo=['Samhain：Hutton《Stations of the Sun》第 35 章原话只经转引；Senchas Már 关于 5 月 / 11 月赶牛的注释原文未核。',
          '诸圣节定日：格里高利三世（731–741）与格里高利四世（835 / 837）两说并列；奥迪洛定诸灵节 998 年 vs「1030 年后」。',
          'trick or treat 最早印刷记录：1917 年安大略（DCHP-3，变体）vs 1927 年阿尔伯塔 Blackie（通行说法，报名与日期有两说）。',
          '篝火夜：1606 年法与 1859 年废止法的 legislation.gov.uk 原页未开；刘易斯 8 万人流为媒体口径。',
          '圣马丁节：Martinsgans 的德语一手来源、INAO 1985 年法令原文未核；佃租日各地口径不同。',
          '圣露西亚：「儒略历下 12/13 接近冬至」的说法未在官方页面核到；报纸选美 1927 vs 1928。',
          '安第斯：Guamán Poma 的 Aya Marcay Quilla 原文未核；拉巴斯月降水常年值未核；柯本 Cwb / Cwc / ET 两说。',
          '中国：《诗经·七月》《礼记·月令》原典页面未能打开（只核到「七月流火，九月授衣」与孟冬首句）；《东京梦华录》十月一日条只核到一句；北京平均初霜日数值未核到（只核到入冬 10/30–31 与首个破冰点日 11/8）；「三大鬼节」最早出处；《典略》三官手书原文。',
          '日本：七五三 1681 年说与「鬼宿日」说并列；千岁饴起源；宫内厅新尝祭官网未开；东京初霜平年值、关东稻作收割月份为通行口径。',
          '排灯节：Bandi Chhor Divas 1619 年份、Yama Deepam 的一手出处；2024 / 2025 年日期取舍的两说。',
          'Tihar：2026 年各日公历对应有两说（11/7–11 vs 11/6–10，吉祥天女祭同为 11/8）；Bhai Tika 吉时尚未公布。',
          '水灯节：2018 年（11/22）、2027 年（11/13）正日无官方公告，2025 年（11/5）仅据素可泰活动末日；素可泰柯本类型与海拔无城市级出处。',
          '亡灵节：萨阿贡第二卷原句未在数字图书馆页面核到（quotes 用托瓦尔手抄本与 Clavigero 代替）；「Catrina」命名出自里韦拉 1947 年壁画的博物馆 / 学术页面；2016 年首届游行观众数；万寿菊农学口径只有媒体；SMN 雨季 5–10 月为媒体转述。',
          '气候数据：罗马、拉巴斯三项全空；斯德哥尔摩、北京、东京、德里、加德满都、墨西哥城的平均初霜日；欧洲五城与东京、悉尼的收获月（FAO GIEWS 无这些国家简报）；十五座城市海拔皆为通行参考值。',
          '柬埔寨 Pchum Ben 2026 正日（10/10 或 10/11）的政府公告；湄公河 / 洞里萨湖 9–10 月水位口径。'])

# 看点清单（小工具 ③）：节日 → 日期口径、必看、必吃、礼仪（编辑据研究底稿写，事实出处在各节点卡）
WATCH = {
    'halloween': dict(when='10 月 31 日（固定）', see='都柏林、爱丁堡的篝火与 Samhain 游行；纽约格林威治村万圣节游行（10/31 傍晚，第六大道）；爱尔兰国家博物馆的大头菜灯。', eat='barmbrack 果子面包、colcannon、苹果与坚果；北美是糖果与南瓜。', mind='trick-or-treat 只敲亮着门廊灯的门；别把亡灵节的祭坛当万圣节装饰。'),
    'dia-de-muertos': dict(when='10 月 31 日夜 → 11 月 2 日（固定）；2026 年墨西哥城大游行 10/31 14:00', see='墨西哥城改革大道到宪法广场的大游行、宪法广场的巨型祭坛；米却肯 Pátzcuaro 湖区与瓦哈卡的公墓守夜；家中的 ofrenda。', eat='亡灵面包 pan de muerto、糖骷髅、tamales 与 atole、mole。', mind='公墓守夜是家庭的事，拍照先问；祭坛上的东西不要碰；画骷髅妆是客人也可以的，但它不是万圣节扮装。'),
    'bonfire-night': dict(when='11 月 5 日（固定）；刘易斯按就近的工作日', see='刘易斯的六个篝火会游行、燃烧的十字架与人偶、篝火与烟花；伦敦与各地的公园烟花。', eat='烤土豆、太妃苹果、parkin 姜糖蛋糕。', mind='刘易斯当天不开车进城、火车限流；别站在游行队伍的火把路线上。'),
    'lidong': dict(when='11 月 7 或 8 日（太阳黄经 225°）；2026 年 11/7 17:52', see='北京的「水始冰」——常年 11 月 8 日第一次跌破冰点；闽台的「补冬」。', eat='北方饺子；闽台姜母鸭、麻油鸡。', mind='立冬是节气不是节日，没有仪式；想看二十四节气的来处去读《礼记·月令》。'),
    'hanyi': dict(when='农历十月初一；2026 年 11 月 9 日', see='华北街头傍晚的焚纸衣；寒衣节与清明、中元并称的说法。', eat='饺子、面食；旧时开封的「暖炉会」。', mind='焚纸请在指定地点，城市多数街区已禁止路边焚烧。'),
    'diwali': dict(when='amanta 历阿湿缚庾阇月朔日；2026 年 11 月 8 日', see='德里、斋浦尔的灯饰与集市（Dhanteras 起五天）；艾哈迈达巴德次日的新年与账本礼；莱斯特的灯饰。', eat='mithai 甜食（laddu、barfi、jalebi）、咸点 namkeen。', mind='进寺庙与别人家脱鞋；烟花在多数城市有时段与禁放规定；灯是请吉祥天女的，不是装饰。'),
    'tihar': dict(when='与排灯节同轮新月，五天；2026 年 11 月 7–11 日（两说）', see='加德满都的狗日（狗戴花环与 tika）、门前 rangoli 与油灯、兄妹节的 tika 仪式、Deusi-Bhailo 挨户歌舞。', eat='sel roti 米粉环饼、果仁与甜食。', mind='Bhai Tika 的吉时由历法决定委员会公布；进寺庙脱鞋；别打扰正在受礼的狗与牛。'),
    'loy-krathong': dict(when='泰历十二月望；2026 年 11 月 24 日（素可泰活动 11/15–24）', see='素可泰历史公园的水灯与烛光节、清迈的 Yi Peng 天灯、曼谷湄南河畔。', eat='泰国冷季小吃；水灯节没有专属食物。', mind='水灯用芭蕉叶与鲜花做，别用泡沫塑料；天灯在清迈市区多数时段禁放，只在指定场地。'),
    'martinmas': dict(when='11 月 11 日（固定）', see='乌得勒支的圣马丁灯光游行、荷兰与比利时孩子的灯笼与讨糖、德国的 Martinsumzug。', eat='圣马丁鹅（Martinsgans）、荷兰的 Martinmas 面包。', mind='荷兰的讨糖在新教地区更常见，天主教地区偏宗教。'),
    'todos-santos-andes': dict(when='11 月 1–2 日（固定）', see='拉巴斯的公墓、家中的 apxata 祭桌（黑布、甘蔗、面包人、梯子面包）。', eat='t\'anta wawa 面包人、马铃薯与藜麦。', mind='11/1 正午亡魂回家、11/2 送别；祭桌是请客的桌子，受邀才坐。'),
}
