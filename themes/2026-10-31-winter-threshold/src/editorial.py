# -*- coding: utf-8 -*-
"""第 7 题「冬天的门槛」编辑文案与配置。研究底稿在 research/fest_{A,B,C,D}.json；这里只放编辑自己写的句子和各章取哪些节点。
改研究底稿里的句子不要动 JSON，往 fixes.py 的 POST 表里加一行。"""

META = dict(
    no=7, slug='winter-threshold', date='2026-10-31',
    title='冬天的门槛：不同纬度与气候下，各文明为什么在同一个季节祭亡灵、点灯火',
    subtitle='从北纬 59 度的斯德哥尔摩到南纬 34 度的悉尼，十九个节日排成一张灯谱，大多压在冬初这道季节门槛上；纬度、气候、历法与传播怎样决定它们的同与异。',
    desc='节日跟着收成走，收成跟着气候走，气候跟着纬度和地形走。一张可拖的「夜的田野」、十天的全屏时间轴、十九个节日的灯谱、一只能转的年轮，外加纬度墙与算日子两个小工具。',
    tags=['吃喝玩乐', '节庆', '气候', '历法', '全球史'],
    format='图谱 · 夜的田野 · 灯谱 · 年轮 · 小工具',
    reading_time='20 分钟', cover_focus='#top', cover_scheme='dark')

HERO = dict(
    thesis='节日跟着收成走，收成跟着气候走，气候跟着纬度和地形走。<em>十天里七个节日</em>——万圣节、诸圣与诸灵、亡灵节、篝火夜、立冬、排灯节、寒衣节——落在同一道「年的门槛」上：收成入仓、雨季结束、白昼变短。人们在门槛上请亡灵回家、把夜点亮、吃一顿；日子和东西各不相同，一半跟着纬度与气候，一半跟着历法与传播。',
    hint='拖动田野上的竖线（或用方向键）：越往北，黑夜来得越早。这十天的十一盏灯里，北半球的九盏都在黑夜变长的坡上，悉尼与拉巴斯在南半球的春天。')

# v3 卷首：一张全幅实拍 + 一句标题 + 一个动作；论点单独成一节，逐词点亮（见 build_theme.hero / tagline_sec）
HERO3 = dict(
    kicker='这十天 · 10 月 31 日 → 11 月 9 日',
    title='冬天的门槛',
    sub=['不同纬度与气候下，', '各文明为什么在同一个季节', '祭亡灵、点灯火'],
    cta='走过这十天', cta_href='#days',
    proof='十九个节日 · 十五座城 · 日子与昼长都按 2026 年现算',
    img='img-hero-1', img_1280='hero-iss062e103874-1280.jpg',
    alt='从国际空间站看夜里的地球：上面是满天星，中间一道发光的大气层，下面是欧亚交界一带的城市灯火',
    cap='国际空间站，2020 年 3 月 20 日，欧亚交界上空：星空、大气辉光与城市灯火。图：NASA，公有领域。')
# 论点：「|」分词，「/」换行；词按滚动依次点亮
TAGLINE = '节日|跟着|收成|走，/收成|跟着|气候|走，/气候|跟着|纬度|和|地形|走。'
TAGREST = '十天里七个节日——万圣节、诸圣与诸灵、亡灵节、篝火夜、立冬、排灯节、寒衣节——落在同一道「年的门槛」上：收成入仓、雨季结束、白昼变短。人们在门槛上请亡灵回家、把夜点亮、吃一顿；日子和东西各不相同，一半跟着纬度与气候，一半跟着历法与传播。'
FIELD3 = dict(title='这一年的黑夜', lede='颜色越深，那天那条纬线上的夜越长。拖动竖线：越往北，黑夜来得越早；这十天的十一盏灯里，北半球的九盏都在黑夜变长的坡上，悉尼与拉巴斯在南半球的春天。')

# v3 每章开篇的图版：(图片 id, 1280 宽文件, alt, 图注)；图在右、字在左，图不压字
OPENERS = {
    'lamps': dict(img='img-open-lamps', small='open-diwali-1280.jpg', w=1800,
                  alt='一幅约 1760 年的北印度细密画：夜里宫廷女眷在河边的露台上放烟花，屋檐、栏杆和河上的船都排满了灯',
                  cap='《宫廷女眷庆祝排灯节》，约 1760 年，北印度勒克瑙，纸本胶彩描金。克利夫兰艺术博物馆藏，CC0。'),
    'threshold': dict(img='img-open-threshold', small='open-millet-1280.jpg', w=1800,
                      alt='米勒的油画：秋天收完的田里堆着三座高大的干草垛，羊群在吃草，天上压着阴云',
                      cap='米勒《干草堆：秋》，约 1874 年，布面油画。大都会艺术博物馆藏，CC0。'),
    'hands': dict(img='img-open-hands', small='open-iss071e439624-1280.jpg', w=2400, wide=True,
                  alt='从国际空间站看轨道日出：黑色的地球边缘亮起一道蓝白色的光弧，下面是一层橙色的大气',
                  cap='国际空间站，2024 年 8 月 6 日，太平洋上空的轨道日出：亮起来的这道弧，就是白昼与黑夜的分界。图：NASA，公有领域。'),
}

CHAPTERS = [
    ('days', 0, '这十天', '拖动底部的刻度尺，或者往下滚：十天里的七个节日，外加往后的一步。'),
    ('lamps', 1, '灯谱', '十九个节日一张表。换一个透镜看——纬度、门槛、历法、传播——相似的会自己聚到一起；点一行，看它的来历与三件事。'),
    ('threshold', 2, '门槛', '把年画成一个圆：十九行里有十六行的日子挤在冬初那一段。拖转年轮，把别家的岁首转到顶上；再看相同的五条、不同的四根轴。'),
    ('hands', 3, '动手', '拖纬度和日期，看黑夜怎么变长；输入年份，算这些节日落在哪天。'),
]

# 序章八步：日期、刻度尺上的短名、点亮的城市、主城（算昼长）、题目、一句话、照片
STEPS = [
    dict(id='d1031', date='2026-10-31', wd='六', label='万圣节', kicker='万圣节 · Samhain · 亡灵节前夜', title='灯从最北边点起',
         cities=['dublin', 'new-york', 'mexico-city', 'sydney'], main='dublin',
         text='都柏林白昼只剩九个半小时多一点。Samhain 传统上释作「夏末」：夏半年在这里交给冬半年，牲口赶回圈。纽约的万圣节是这一天搬过大西洋的样子；墨西哥城 14:00 亡灵节大游行，今年第十届；悉尼却在仲春。',
         photo='img-halloween-1', fest=['samhain', 'halloween', 'dia-de-muertos', 'halloween-south']),
    dict(id='d1101', date='2026-11-01', wd='日', label='诸圣 · 亡灵节', kicker='诸圣节 · 亡灵节首日 · Todos Santos', title='同一个日历日，两个半球',
         cities=['rome', 'mexico-city', 'la-paz'], main='mexico-city',
         text='教会把众圣与众亡者钉在 11 月初，气候各走各的：罗马秋雨、橄榄采收；墨西哥高原雨季刚停、万寿菊正开；拉巴斯在南半球的春天，马铃薯随雨下种。',
         photo='img-dia-de-muertos-10', fest=['all-saints-souls', 'dia-de-muertos', 'todos-santos-andes']),
    dict(id='d1102', date='2026-11-02', wd='一', label='诸灵节', kicker='诸灵节 · 亡灵节正日', title='祭坛上的面包与蜡烛',
         cities=['rome', 'mexico-city', 'la-paz'], main='rome',
         text='墨西哥这天迎成人的亡灵：ofrenda 上摆亡灵面包、糖骷髅与万寿菊；玻利维亚的 apxata 祭桌架甘蔗、摆面包人；欧洲的墓地点满烛光——同一件事，三套东西。',
         photo='img-all-saints-souls-1', fest=['all-saints-souls', 'dia-de-muertos', 'todos-santos-andes']),
    dict(id='d1105', date='2026-11-05', wd='四', label='篝火夜', kicker='篝火夜', title='草停了，田里有东西可烧',
         cities=['lewes'], main='lewes',
         text='刘易斯日落四点半。篝火夜的日子来自 1605 年的火药阴谋与次年的议会法案，与农事无关，却与 Samhain 篝火同一个季节——同季节，未必同来源。',
         photo='img-bonfire-night-1', fest=['bonfire-night']),
    dict(id='d1107', date='2026-11-07', wd='六', label='立冬', kicker='立冬 17:52 · Tihar 乌鸦日', title='太阳到了秋分与冬至的正中',
         cities=['beijing', 'tokyo', 'kathmandu'], main='beijing',
         text='北京时间 17:52，太阳黄经 225°：天文学上的「跨季日」，也是后人给 Samhain 定的天文日子。北京常年 10 月底入冬、11 月 8 日首次跌破冰点；加德满都按假日表开始五天的 Tihar（一说早一天）。',
         photo='img-lidong-2', fest=['lidong', 'tihar']),
    dict(id='d1108', date='2026-11-08', wd='日', label='排灯节', kicker='排灯节 · 吉祥天女祭', title='季风撤完后的第一个无月夜',
         cities=['delhi', 'kathmandu'], main='delhi',
         text='西南季风常年 9 月 25 日撤出德里、10 月 15 日撤出全国，排灯节落在之后的迦底迦月朔——今年正是全国撤完后的第一个新月。amavasya 当值到 9 日 12:32（印度时间）：8 日日落时还在、9 日日落前已过，所以今晚点灯；加德满都同一晚祭吉祥天女。',
         photo='img-diwali-3', fest=['diwali', 'tihar']),
    dict(id='d1109', date='2026-11-09', wd='一', label='寒衣节', kicker='寒衣节 · 农历十月初一', title='同一轮新月，中国晚一天',
         cities=['beijing'], main='beijing',
         text='北京时间 15:02 朔，含朔时刻的这一天是十月初一，送寒衣；印度按日落时的 tithi 早一天点灯。十月朔在秦与汉初做过一百多年的岁首。',
         photo='img-hanyi-3', fest=['hanyi']),
    dict(id='dnext', date='2026-11-11', wd='三', label='再往后', kicker='再往后 · 11/11 → 12/13', title='灯一路往南、往北点下去',
         cities=['utrecht', 'tokyo', 'sukhothai', 'stockholm'], main='utrecht',
         text='11/11 乌得勒支的灯笼、德国的圣马丁鹅；11/15 东京七五三；11/23 新尝祭与下元；11/24 素可泰满月放水灯；12/13 斯德哥尔摩的圣露西亚，白昼只剩六小时出头。',
         photo='img-lucia-1', fest=['martinmas', 'shichigosan', 'niinamesai', 'xiayuan', 'loy-krathong', 'lucia']),
]

# 灯谱的透镜：按什么把十九行分组（组名、组的先后在 build_theme.lens_groups 里算）
LENSES = [('date', '日期'), ('lat', '纬度'), ('kind', '门槛'), ('basis', '历法'), ('spread', '传播')]

# 年轮可吸附的「岁首」：(短名, 说明, 2026 年的年内序日)
ANCHORS = [('公历 1/1', '公历元旦', 1), ('春节 2/17', '2026 年春节', 48), ('宋干 4/13', '泰国宋干节', 103), ('Samhain 之说 11/1', '「萨温节是凯尔特新年」之说（有争议）', 305),
           ('11/9–10：秦十月朔 · 古吉拉特 · 尼泊尔', '秦以十月朔为岁首（按今农历，今年是 11/9）；古吉拉特新年（迦底迦月白分初一）在 11/10，尼泊尔历（Nepal Sambat）元旦推算也在 11/10', 313)]

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
            'halloween-south': None, 'hanyi': 'img-hanyi-1', 'lidong': 'img-lidong-1', 'xiayuan': None, 'zhongyuan-contrast': 'img-zhongyuan-contrast-1',
            'shichigosan': 'img-shichigosan-2', 'niinamesai': 'img-niinamesai-2', 'qin-new-year': 'img-hanyi-2', 'diwali': 'img-diwali-2', 'tihar': 'img-tihar-3',
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
    dict(id='loy-krathong', city='sukhothai', season='雨季末 · 水最满', kind='monsoon', note='北半球冬初这串灯里最靠南的一盏'),
    dict(id='halloween-south', city='sydney', season='仲春 · 无门槛', kind='none', note='反例：日子钉在公历上，气候缺席'),
    dict(id='zhongyuan-contrast', city='beijing', season='雨季尾 · 青黄不接', kind='religion', note='另一道门槛：佛教自恣日'),
    dict(id='pchum-ben', city='phnom-penh', season='雨安居将尽', kind='religion', note='另一道门槛：僧团日历'),
]
KIND_NAME = {'harvest': '收成后', 'sowing': '播种前', 'monsoon': '季风退', 'night': '长夜', 'solar': '太阳历', 'calendar': '日历定', 'event': '事件定', 'religion': '宗教历', 'none': '无门槛'}
BASIS_NAME = {'gregorian-fixed': ('固定日', '公历'), 'lunisolar-chinese': ('跟月亮', '农历'), 'lunisolar-hindu': ('跟月亮', '印度历'), 'solar-term': ('跟太阳', '节气'), 'thai-lunar': ('跟月亮', '泰历与高棉历'), 'rule': ('按规则', ''), 'southern-transplant': ('固定日', '公历')}
SPREAD_NAME = {'native': '本土', 'church-calendar': '宗教日历', 'migration': '移民', 'commercial': '商业', 'transplant': '移植'}

# 「同」五条、「异」四根轴（都指回灯谱里的行；异的第四个字段是灯谱该切到的透镜）
SAME = [('门槛', 14, '十四行压在收成入仓、雨季结束、牲口回圈或长夜到来之后的几周；Todos Santos 压在播种前；例外是纽约与悉尼的万圣节、中元与 Pchum Ben。'),
        ('长夜', 4, '北纬 50° 以北的四行，当天昼长都不到 10 小时，最北的圣露西亚只剩 6 小时 12 分；再往南，只有北京 11/23 的下元（9 小时 46 分）也跌破 10 小时。'),
        ('亡灵', 10, '十行请亡灵回家，从爱尔兰、天主教欧洲、墨西哥、安第斯到华北、尼泊尔（Tihar 的乌鸦日）、柬埔寨；其中八行在冬初这几周，中元与 Pchum Ben 在夏末与雨季里。'),
        ('灯火', 14, '十四行有灯或篝火；没有的五行是寒衣、立冬、七五三、新尝祭与 Pchum Ben。'),
        ('吃一顿', 18, '除水灯节外每一行都有专属的食物，多半是刚收下来的东西，或过冬前要处理的牲口。')]
DIFF = [('纬度', '纬度换了门槛的内容：高纬是草停与长夜，中纬是入冬与初霜，低纬是季风与雨季的进退；南半球整个颠倒。', ['samhain', 'lidong', 'diwali', 'dia-de-muertos', 'loy-krathong', 'todos-santos-andes'], 'lat'),
        ('气候与地理', '收什么、怕什么，往往对得上用什么：篝火与根菜灯、寒衣与饺子、油灯与甜食、高原的万寿菊、河网里的水灯。', ['bonfire-night', 'hanyi', 'diwali', 'dia-de-muertos', 'loy-krathong'], 'kind'),
        ('历法', '有钉在公历上的，有跟月亮走的，有跟太阳走的。同一轮新月，印度 11/8 点灯，中国 11/9 送寒衣；立冬与天文学上的 Samhain 是同一个时刻。', ['halloween', 'diwali', 'hanyi', 'lidong', 'loy-krathong'], 'basis'),
        ('传播', '本土长出的、随宗教日历移植的、随移民与商业改装的——日子一旦钉死在历法上，或随人搬到别的气候带，就可能与当地气候脱节。', ['samhain', 'all-saints-souls', 'todos-santos-andes', 'halloween', 'halloween-south'], 'spread')]

# 夜的田野里悬停时的一句定日规则（底稿的 date_rule 太长的几行）
RULE_SHORT = {'dia-de-muertos': '固定 11/1–2（前夜 10/31）', 'diwali': '迦底迦月朔：日落时 amavasya 当值的那天', 'tihar': '与排灯节同一轮新月，前后五天',
              'loy-krathong': '泰历十二月望', 'zhongyuan-contrast': '农历七月十五（日本多在 8/13–16）', 'pchum-ben': '高棉历十月亏月十五（朔日）'}

# 灯谱展开里的「三件事」：每行三格 (一句话, 图片 id 或 None, 是否「没有这件事」)。句子都从研究底稿各节点的 three 字段缩写，不加新事实。
# 「没有」的格子淡显；同的「亡灵 10 / 灯火 14 / 吃一顿 18」就是按这里的第三个字段数出来的（build_theme 会核对）。
THREE_COLS = [('dead', '请亡灵回家'), ('light', '把夜点亮'), ('food', '吃一顿')]
TILES = {
    'samhain': dict(dead=('中世纪文献里，这一夜是集会、宴饮与超自然故事的时候；「亡灵回家」的做法主要见于近代爱尔兰、苏格兰民俗，不宜回推到前基督教时期。', None, False),
                    light=('中世纪文献提到 Samhain 篝火；近代爱尔兰与苏格兰高地的万圣节篝火有大量 18–19 世纪的记录。', None, False),
                    food=('牲口回圈后的宰杀季，盐腌与鲜肉；colcannon 卷心菜土豆泥与藏戒指的 barmbrack 是较晚的爱尔兰万圣节食物。', None, False)),
    'halloween': dict(dead=('爱尔兰、苏格兰民俗里，这一夜亡魂出来走动，化装是为了混在其中、不被认出；北美的 trick-or-treat 是 20 世纪的发展，与亡灵的关系已淡。', None, False),
                      light=('爱尔兰的大头菜灯（jack-o\'-lantern）到了北美，换成了 9–10 月采收的南瓜。', 'img-halloween-3', False),
                      food=('从爱尔兰的 barmbrack、colcannon 到北美的糖果与太妃苹果；NRF 2025 年的调查里，糖果一项是 39 亿美元。', None, False)),
    'all-saints-souls': dict(dead=('诸灵节为炼狱中的亡者祈祷、扫墓、点烛；中世纪英格兰的穷人挨户讨「灵魂饼」，每得一块，就为施主家的亡者祈祷一次。', 'img-all-saints-souls-1', False),
                             light=('意大利、波兰、法国等天主教地区，11/1–2 的夜里墓园点满蜡烛。', None, False),
                             food=('英格兰、威尔士的 soul cakes；意大利各地叫「亡者骨头」ossa dei morti、「亡者蚕豆」fave dei morti 的甜点。', None, False)),
    'dia-de-muertos': dict(dead=('家中与公墓的 ofrenda 祭坛：照片、蜡烛、水、盐、亡者爱吃的菜；花瓣从墓园撒到家门，为亡魂引路。11/1 迎夭折的孩子，11/2 迎成人。', 'img-dia-de-muertos-3', False),
                           light=('蜡烛与万寿菊（cempasúchil）：7 月前后种下、约 90 天长成，秋天开花，正赶上 11 月初的祭坛；墓园通宵点烛。', 'img-dia-de-muertos-11', False),
                           food=('亡灵面包 pan de muerto、糖骷髅、玉米粽 tamales、热巧克力与 atole；祭坛上的菜先供亡者「享用」，再由家人分食。', 'img-dia-de-muertos-12', False)),
    'todos-santos-andes': dict(dead=('11/1 正午点烛迎亡魂，apxata 祭桌摆亡者的照片、食物、古柯与酒；送别有两说：11/2 正午，或 11/3 正午的 kacharpaya。', None, False),
                               light=('祭桌上的蜡烛是亡魂到家的信号；墓园守夜。', None, False),
                               food=('面包娃娃 t\'anta wawa、面包老人与面包梯子（助亡魂升天），冻干马铃薯 ch\'uñu、玉米、古柯叶与酒；送别后面包分食。', None, False)),
    'bonfire-night': dict(dead=('无亡灵内容：烧的是 Guy Fawkes 的人偶（刘易斯 1850 年起加烧教宗像，今天只剩 Cliffe 篝火会还烧）；游行抬的 17 支十字架，纪念 1555–1557 年在镇上被烧死的新教徒。', None, True),
                          light=('篝火、焰火与燃烧的柏油桶；刘易斯的游行把第一只柏油桶扔进乌斯河，纪念 1847 年治安官被扔下河。', None, False),
                          food=('烤土豆、parkin 姜饼与 bonfire toffee 太妃糖（通行的民俗说法）。', None, False)),
    'martinmas': dict(dead=('无亡灵内容：这是圣人纪念日，也是北海沿岸农事年的结账日。', None, True),
                      light=('孩子提着手工灯笼（甜菜根、纸灯笼）挨户游行；部分地区点圣马丁篝火，乌得勒支有灯光雕塑游行。', 'img-martinmas-1', False),
                      food=('鹅（Martinsgans）与新酒：牧草停长、牲口只能靠干草过冬，正是宰杀腌制的时候；荷兰孩子讨到糖果与水果。', None, False)),
    'lucia': dict(dead=('无亡灵内容；但「Lusse 长夜」被看作超自然生灵出没的一夜。', None, True),
                  light=('白衣的露西亚头戴烛冠，领着队伍唱歌游行；学校、教堂与工作场所在清晨举行。', None, False),
                  food=('藏红花 S 形面包 lussekatter、姜饼与 glögg 热酒。', None, False)),
    'lidong': dict(dead=('民间立冬本身不祭亡，祭亡交给两天后的寒衣节；《礼记·月令》孟冬「腊先祖五祀」是经学口径的岁末祭祖。', None, True),
                   light=('无灯火习俗；宋代开封立冬前车载马驮往城里运冬菜，「一时收藏，以充一冬食用」。', None, True),
                   food=('北方立冬吃饺子；闽台「立冬补冬，补嘴空」，吃麻油鸡、姜母鸭、羊肉炉。', None, False)),
    'hanyi': dict(dead=('宋人出城上坟；明清北京在家门口夜奠，把写着先人姓名辈行的五色纸衣「呼而焚之其门」，新丧用白纸衣。', None, False),
                  light=('没有专门的灯火：只有门前焚衣的火光，和宋人「暖炉会」的炉火。', None, True),
                  food=('宋人置酒作暖炉会；南京旧俗「十月朝、穿棉袄，吃豆羹」；华北今多包饺子。', None, False)),
    'xiayuan': dict(dead=('家祭祖先，叠「金银包」纸钱焚烧。', None, False),
                    light=('苏州、常州一带挂三官灯、三官旗；华北没有特别的灯火。', None, False),
                    food=('莆田麻腐包子、北京豆泥骨朵、宁化糍粑、常州小汤团；有的地方吃「三官素」。', None, False)),
    'shichigosan': dict(dead=('不是祭亡节：为活着的孩子谢神、祈成长，与寒衣节「为死者添衣」同月相对。', None, True),
                        light=('无灯火：参拜神社，穿和服拍照。', None, True),
                        food=('千岁饴：红白长条饴糖，装在印着鹤龟松竹梅的袋里，寓意长寿。', None, False)),
    'niinamesai': dict(dead=('不祭亡者，祭天照大神与天神地祇；同日各地神社也行新尝祭、谢稻。', None, True),
                       light=('宫中神嘉殿的夜间祭仪（夕之仪、晓之仪）；无民间灯火。', None, True),
                       food=('新米、新酒与神馔，天皇与神共食；民间以「新米」为节令。', 'img-niinamesai-1', False)),
    'diwali': dict(dead=('排灯节不祭亡灵，请的是吉祥天女；五天里与死亡相关的，只有第一天为阎摩点的 Yama Deepam 和第二天的那罗迦十四。', None, True),
                   light=('diya 油灯：家家在门窗、庭院点陶土油灯（也用蜡烛、灯笼、电灯串），夜里放烟花；灯点在季风退去后最暗的无月夜。', 'img-diwali-1', False),
                   food=('mithai 甜食与家宴是主项，kharif 稻谷、玉米正在收；商人在吉祥天女前开新账本（Chopda Pujan）——收成变现的时点。', None, False)),
    'tihar': dict(dead=('第一天乌鸦日：乌鸦是阎摩的使者，日出前在屋顶与院子里放谷物和甜食，请它带走忧伤——五天里最接近「请亡灵」的一层。', None, False),
                  light=('吉祥天女祭之夜，门前、窗台点陶灯 diyo，画 rangoli 彩粉与女神的脚印：「女神不去黑暗的屋子」。', 'img-tihar-2', False),
                  food=('sel roti 米粉环饼：供吉祥天女、喂乌鸦、兄妹节给兄弟；另有甜食、水果与 Deusi-Bhailo 的回礼。', None, False)),
    'loy-krathong': dict(dead=('不祭亡灵：向水之女神（Phra Mae Khongkha）致意，把霉运与坏情绪随水灯放走。', None, True),
                         light=('芭蕉叶折成莲座、插上香烛的水灯（krathong）放到河上；兰纳的清迈同一夜放 khom loi 天灯。', 'img-loy-krathong-2', False),
                         food=('没有专属食物；主季稻 10 月初开镰，雨停、水满、稻熟三件事同时到来。', None, True)),
    'halloween-south': dict(dead=('无亡灵内容。', None, True),
                            light=('南瓜灯与装饰照搬；天黑在 19 时以后（夏令时），讨糖在黄昏。', None, False),
                            food=('糖果；南瓜在澳大利亚是全年蔬菜，没有季节性。', None, False)),
    'zhongyuan-contrast': dict(dead=('中国烧衣服冥钱、拜扫新坟；日本 13 日夜在门前烧「迎え火」接祖灵回家，16 日夜烧「送り火」送归。', None, False),
                               light=('日本盆的核心就是火：迎火、送火、灯笼流，京都 8/16 的五山送火；中国放河灯。', None, False),
                               food=('中国是供僧、祭祖的饭食；日本是精灵棚上的供物。', None, False)),
    'pchum-ben': dict(dead=('十五天里到寺院供僧，为上溯七代的祖先回向；相信地狱之门开启、亡者回来受食，黎明把饭团掷给无人祭祀的饿鬼。', None, False),
                      light=('点灯不是主项：核心是僧人通宵诵经与黎明的供养。', None, True),
                      food=('饭团 bay ben（米饭，或拌豆）掷给亡者；供僧的饭菜由各家轮流备办。', None, False)),
}

# 灯谱行展开后的四条短事实（怎么定日 / 压在哪道门槛上 / 岁首 / 传播）：从底稿缩写；没写的字段用底稿原文（太长则在句末截断，括号里不断）。全文在折叠里。
FACTS = {
    'samhain': dict(threshold='早期爱尔兰文献把一年切成夏、冬两半，Samhain 起冬；法典注释说牲口 11 月初从夏牧场赶回——清点牲口与存粮、决定宰杀哪些过冬的时点。',
                    ny='有争议：「凯尔特新年」是 1901 年 Rhys 据晚期民俗提出、Frazer 推广的解读；中世纪文献只把它写成「夏末」与四季分点之一。',
                    spread='盖尔语区的「夏末」与牲口回圈节点；与 11/1 诸圣节重合，前夜叫 All Hallows\' Eve；19 世纪随移民进入北美后，与气候、牲口的联系基本脱落。'),
    'halloween': dict(threshold='在纽约（北纬 40.7°）它已与农事脱钩：钉在公历 10/31，跟着移民与零售日历走；2026 年 49% 的消费者 9 月或更早就开始买——门槛从霜期变成了货架期。',
                      spread='19 世纪随爱尔兰、苏格兰移民到北美，20 世纪前半叶定型为 trick-or-treat，1950 年代后由零售推成全国性的消费节日，再返销欧洲、日本与澳大利亚。'),
    'all-saints-souls': dict(threshold='11/1 最早见于 8 世纪罗马的诸圣小堂，835 年（一说 837 年）由法兰克皇帝推行到高卢与日耳曼，不是从 Samhain 搬来的。罗马此时秋雨开始、橄榄正收，与北方的「收成结束、牲口回圈」并不同步。',
                             spread='随拉丁教会日历传遍西欧，再随殖民与传教到美洲、菲律宾；日子钉在公历上，不随当地气候移动。'),
    'dia-de-muertos': dict(rule='固定公历：11/1 悼念夭折的孩子（Día de los Angelitos），11/2 悼念成人；守夜与祭坛从 10/31 夜里开始。',
                           threshold='墨西哥城（海拔约 2 240 m）雨季 5–10 月，11 月入旱季，玉米收完、万寿菊正开；这是相关，不是决定——日子本身是教会日历钉的。',
                           spread='本土祭亡附着在教会的 11/1–2 上；波萨达的骷髅与里韦拉的壁画把它变成国民图像，2008 年列入 UNESCO 名录，2016 年起墨西哥城办大游行。'),
    'todos-santos-andes': dict(rule='固定 11/1 正午迎亡魂；送别在 11/2 正午，或 11/3 正午（两说）。',
                               threshold='同一个 11/1，拉巴斯（南纬 16.5°、海拔 3 640 m）正是旱季转雨季、马铃薯随雨下种的春天；亡魂回家被理解为「把雨和丰收带回来」。',
                               spread='16 世纪西班牙殖民把教会的 11/1–2 带到安第斯；亡魂回家、面包人、播种前献祭这些习俗延续至今，与十字架、念珠同在一张祭桌上。'),
    'bonfire-night': dict(threshold='日子来自 1605 年的事件与次年的议会立法，不来自农事；但英格兰 11 月初本就夜长、草停、田里有可烧之物。它与万圣节篝火的关系，学界主流偏向「替代而非承接」。',
                          spread='1606 年立法与《公祷书》的专用祷文维持了 250 多年，1859 年废止后靠地方篝火会延续；随英帝国传到纽芬兰、新西兰。'),
    'martinmas': dict(threshold='北纬 52° 的海洋性气候里，11/11 牧草停长、牲口只能靠干草过冬，是宰鹅腌猪的季节；也是农事年的结账日，荷兰、比利时的雇工合同在这天续签。',
                      spread='圣人纪念日固定在 11/11，习俗（灯笼、鹅、结账）却紧扣北海沿岸的农事年；荷兰的灯笼游行 2010 年代起在新教地区复兴。'),
    'lucia': dict(threshold='斯德哥尔摩北纬 59.3°，这天白昼只有 6 小时上下：越靠北、越近冬至，点灯的日子越晚。日子来自圣人日历，在瑞典被民俗重新解释为「一年最长的夜」。',
                  spread='20 世纪由报纸选美与学校定型为全国习俗，再随瑞典移民与大使馆传到北美与各国。'),
    'lidong': dict(threshold='节气系统里明文的「冬之门槛」，和华北的气候咬得很准：北京常年 10/30–31 入冬，11/8 第一次跌破冰点。往南就脱节，闽台「补冬」补的是对寒气的预期。',
                   spread='黄河流域的太阳历知识，随中国历法传到朝鲜半岛、日本、越南；每年固定在 11/7 或 11/8，是这十天里唯一按太阳定日的中国节日。'),
    'hanyi': dict(threshold='压在华北三道门槛的交点上：玉米收完、冬小麦已播，地里无活；北京常年 11/8 首次跌破冰点；秦与汉初这天还是岁首。活人换冬衣，顺手给死者也送一套。',
                  ny='是：秦「改年始，朝贺皆自十月朔」，到汉武帝太初元年（前 104）才改以正月为岁首——十月初一做过约一百二十年的元旦。',
                  spread='黄河流域本土长出的节日，跟着朔望月走，从未钉到公历上；从宋开封的「受衣」与上坟、明代北京纸店的「寒衣」，到今天北方的烧纸衣。'),
    'xiayuan': dict(threshold='孟冬的望日，离立冬两周上下、紧邻小雪，华北已入冬；它是道教三元的第三个「元」，与寒衣节一起把「十月」做成了祭亡的月份。'),
    'shichigosan': dict(threshold='旧历 11/15 在 1681 年合公历 12 月 24 日，冬至前后、收成全部入仓之后；改用公历后早了一个多月，落到关东晚秋的红叶季，与农事脱钩。',
                        spread='江户中期，和服店把三个仪式打包成商业节令；明治以后随都市生活普及全国，今多在 11/15 前后的周末举行。'),
    'niinamesai': dict(threshold='日本版的收成门槛：关东稻作 9–10 月收割，11 月下旬脱谷入仓完毕，把第一口新米先给神；旧历在冬至前后，改公历后提前约一个月。',
                       spread='1873 年改历钉到公历 11/23，1948 年改名「勤劳感谢日」——名字脱离了稻作与神道，日期原封不动。'),
    'diwali': dict(rule='迦底迦月的朔日 amavasya（amanta 历算作阿湿缚庾阇月末）；看日落后的 pradosh 时段里 amavasya 是否当值，定在公历哪一天。',
                   threshold='季风退去后的迦底迦月朔：西南季风常年 9/25 撤出德里、10/15 撤出全国；kharif 稻谷、玉米正在收，雨停天晴。2015–2027 年都落在 10/19–11/14。',
                   ny='是（区域性）：古吉拉特以迦底迦月白分初一为维克拉姆历新年，今年在 11/10；商人在排灯节当晚于吉祥天女前开新账本。',
                   spread='先随印度教、耆那、锡克三种日历铺满南亚，再随契约劳工与移民到海外；到了温带或南半球，它离开了季风门槛，日期仍按月相定。'),
    'tihar': dict(rule='从迦底迦月黑分十三起，五个 tithi 各过一天：乌鸦、狗、吉祥天女与牛、牛王（兼尼瓦尔人的 Mha Puja）、兄妹；各日按当天有效的 tithi 落到公历上。',
                  threshold='与排灯节共用同一轮新月，更贴着谷地的农事：稻作 10–12 月收，季风早已退去；五天里依次酬谢乌鸦、狗、牛、牛王。',
                  ny='是（尼瓦尔）：第四天 Mha Puja 即尼泊尔历（Nepal Sambat）元旦，2026 年推算在 11/10。',
                  spread='随印度教历在喜马拉雅山麓本地化；没有被商业或移民搬到别的气候带，仍钉在谷地的收稻季。'),
    'loy-krathong': dict(rule='泰历十二月望；兰纳历把同一轮满月叫「二月望」（Yi Peng），所以清迈的天灯与全国的水灯同一夜。',
                         threshold='钉在雨季结束、河水最满的那轮满月：雨季 5 月中到 10 月中，主季稻 10 月初开镰；2015–2027 年的正日都在 10/31–11/27 之间。',
                         spread='根在高棉—婆罗门的水祭，19 世纪的曼谷文本给它安上素可泰的出身，二战后由国家与旅游局推成全国节。'),
    'halloween-south': dict(threshold='没有门槛：悉尼此时白昼约 13 小时、花开草长，长夜、初霜、收成结束全部缺席；参与率两成上下，靠的是零售与社区活动。',
                            spread='随美国影视与零售进入，2010 年代起零售协会每年发布消费预测；参与率 18–21%，远低于美国的 73–74%。'),
    'zhongyuan-contrast': dict(rule='中国：农历七月十五；日本：多数地区公历 8/13 夜迎火、16 日夜送火（「月遅れ盆」），东京都心等地按 7 月。',
                               threshold='另一道门槛：同样请亡灵、点火、供食，却在夏末雨季尾声，华北玉米还在灌浆、关东稻还在抽穗；钉住它的是僧团安居结束的自恣日与月亮。',
                               spread='七月十五是僧团安居结束的「自恣日」，随佛教从印度经中国到日本，日期跟佛历走、不跟农事走；明治改历后，日本多数地区的盆平移到 8 月。'),
    'pchum-ben': dict(rule='高棉历十月亏月的前十四天为 Kan Ben，第十五日（朔）为正日；锚在雨安居将尽，而不在收成。',
                      threshold='雨季还没结束、稻子还没收，钉住它的是僧团雨安居将满三个月——日历锚是宗教制度，不是收成或长夜。'),
}

WALLS = [
    dict(id='lat', title='纬度墙', formula='昼长 = 2·arccos[(cos 90.833° − sin φ·sin δ) / (cos φ·cos δ)] / 15°', text='在图上左右拖换日期，拖滑块换纬度：曲线是那条纬线一年的昼长，竖线是你选的日子；下面列出这个纬度带（±8°）上的节日。按太阳赤纬的标准近似算，天顶距取 90.833°（含大气折射与日面半径），不计海拔，误差在几分钟内。'),
]
TOOLS = [
    dict(id='dates', title='算日子', lede='输入年份，看各节日落在哪天：固定日按公历，立冬按太阳黄经 225°，寒衣节与下元按农历，排灯节按印度历朔日与德里日落，水灯节按泰国官方表或天文望日（±1 天）；小雪、冬至与感恩节只作参照，Pchum Ben 按高棉历，这里不列。'),
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
             '昼长与日落：按太阳赤纬与均时差的标准近似公式现算，天顶距取 90.833°（含大气折射与日面半径），不计海拔，误差在几分钟内；页面上所有昼长都按核心城市的纬度算，日出日落取各城标准时、不含夏令时。',
             '序章底图：NASA「黑色弹珠」2016 年全球夜间灯光合成图（Suomi NPP / VIIRS，公有领域）；地图上的横带按当天各纬度的黑夜长短加深。',
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
    'bonfire-night': dict(when='11 月 5 日（固定）；2026 年是周四', see='刘易斯各篝火会的火把游行、燃烧的十字架与人偶、篝火与烟花；伦敦与各地的公园烟花。', eat='烤土豆、parkin 姜饼与 bonfire toffee 太妃糖（通行的民俗说法）。', mind='别站在火把与燃烧柏油桶的路线上；交通以当年篝火会与铁路的公告为准。'),
    'lidong': dict(when='11 月 7 或 8 日（太阳黄经 225°）；2026 年 11/7 17:52', see='北京的「水始冰」——常年 11 月 8 日第一次跌破冰点；闽台的「补冬」。', eat='北方饺子；闽台姜母鸭、麻油鸡。', mind='立冬是节气：古时朝廷有迎冬之礼（见《礼记·月令》孟冬），民间多是吃的习俗。'),
    'hanyi': dict(when='农历十月初一；2026 年 11 月 9 日', see='华北街头傍晚的焚纸衣；寒衣节与清明、中元并称的说法。', eat='饺子、面食；旧时开封的「暖炉会」。', mind='焚纸请在指定地点，城市多数街区已禁止路边焚烧。'),
    'diwali': dict(when='迦底迦月朔（amanta 历算作阿湿缚庾阇月末）；2026 年 11 月 8 日', see='德里的灯与集市（Dhanteras 起五天）；艾哈迈达巴德当晚的账本礼与 11/10 的新年。', eat='mithai 甜食与干果（互赠）、家宴；牛增山祭的 Annakut「食物山」。', mind='进寺庙与别人家脱鞋；灯是请吉祥天女的，不是装饰。'),
    'tihar': dict(when='与排灯节同轮新月，五天；2026 年 11 月 7–11 日（两说）', see='加德满都的狗日（狗戴花环与 tika）、门前 rangoli 与油灯、兄妹节的 tika 仪式、Deusi-Bhailo 挨户歌舞。', eat='sel roti 米粉环饼、果仁与甜食。', mind='Bhai Tika 的吉时由历法决定委员会公布；进寺庙脱鞋；别打扰正在受礼的狗与牛。'),
    'loy-krathong': dict(when='泰历十二月望；2026 年 11 月 24 日（素可泰活动 11/15–24）', see='素可泰历史公园的水灯与烛光节、清迈的 Yi Peng 天灯、曼谷湄南河畔。', eat='泰国冷季小吃；水灯节没有专属食物。', mind='水灯用芭蕉叶与鲜花做，别用泡沫塑料；天灯在清迈市区多数时段禁放，只在指定场地。'),
    'martinmas': dict(when='11 月 11 日（固定）', see='乌得勒支的圣马丁灯光游行、荷兰与比利时孩子的灯笼与讨糖、德国的 Martinsumzug。', eat='德国的圣马丁鹅（Martinsgans）与新酒；荷兰孩子讨到的糖果与水果。', mind='荷兰的讨糖在新教地区更常见，天主教地区偏宗教。'),
    'todos-santos-andes': dict(when='11 月 1–2 日（固定）', see='拉巴斯的公墓、家中的 apxata 祭桌（黑布、甘蔗、面包人、梯子面包）。', eat='t\'anta wawa 面包娃娃、面包梯子、ch\'uñu 冻干马铃薯与玉米。', mind='11/1 正午亡魂回家；送别有两说，11/2，或 11/3 正午的 kacharpaya。祭桌上的面包与食物先给亡魂，送别后才分食。'),
}
