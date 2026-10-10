# -*- coding: utf-8 -*-
"""第 4 题《把预言造出来》的编辑稿（一）：题头、十二座装置的补充字段、第 1 章。

研究底稿在 research/{A,B,C,D}.json，由 make_content.py 合并；这里只放编辑自己写的文案、
对底稿的取舍，以及给示意图与小工具用的数字。数字的出处都在底稿各卡的 facts 里。
"""

IDS = ['michelson', 'leiden', 'cyclotron', 'bubble', 'cambridge', 'spps',
       'homestake', 'cobe', 'lhc', 'superk-sno', 'ligo', 'icecube']
SRC = {'michelson': 'A', 'leiden': 'A', 'cyclotron': 'A', 'bubble': 'A', 'cambridge': 'A',
       'spps': 'B', 'cobe': 'B', 'lhc': 'B',
       'homestake': 'C', 'superk-sno': 'C', 'ligo': 'C', 'icecube': 'C'}

META = dict(
    no=4, slug='nobel-machines', date='2026-10-10',
    title='把预言造出来',
    subtitle='诺贝尔物理学奖背后的十二座装置',
    kicker='一周一题 第四题',
    thesis='一句预言要变成结论，中间隔着一份任务书：要多大、多冷、多静、多干净，花多少钱、干多少年，坏了怎么办。'
           '这一页翻十二份这样的任务书，再看接下来要写的那些。',
    steps=[
        '先看尺子：从 1.5 米的石板到 250 万公里的臂长，装置大了多少个量级。',
        '再翻图纸：十二座装置，每座一张按比例画的示意图和一份任务书。',
        '最后看两样：它们教给工程师什么；下一批要造的是什么，大概哪一年。',
    ],
    desc='2026 年诺贝尔物理学奖的颁奖词直接点了一座装置的名字：IceCube。从 1887 年浮在水银上的石板，到南极冰下的一立方公里，'
         '十二座装置各一张同比例示意图和一份任务书；每座装置教给工程师的一件事；还有接下来要造的机器和它们的时间表。',
    ruler_note='对数尺：每一大格是十倍。实线是造出来的，虚线是在建或设想中的。莱顿低温实验室的标尺是温度，不在这把尺上。',
)

CHAPTERS = [
    ('top', '卷首', ''),
    ('c1', '今年的奖', '图 01'),
    ('c2', '十二座装置', '图 02'),
    ('c3', '工程思维', '图 03'),
    ('c4', '候补席', '图 04'),
    ('c5', '下一批任务书', '图 05'),
    ('end', '卷末', ''),
]

CRITERIA = [
    '颁奖词或诺奖委员会的背景材料，把装置、方法或「项目」写成获奖理由',
    '把某个工程量纲（尺寸、质量、低温、真空、洁净度、精度、数据量）推到当时没人做到的量级，且有一手数字',
    '工程决策本身有据可讲：选址、分期、冗余、失败与重建、预算与工期',
    '类型互补：精密测量、低温、加速器、探测器与数据、地下低本底、射电、空间、冰下，各至少一座',
]

# ---------------------------------------------------------------- 十二座：编辑补充
# short / laur：图表里用的短名；era：标题栏里的年代；place：标题栏里的地点；
# sites：世界地图落点 (名称, 纬度, 经度)；tag：卡片题下的一句话；
# tool：规模对比器用的数字（size_m 为特征跨度）；cost：(金额, 币种, 年份, 口径)；
# shape：对比器里画的简化外形；drop_*：底稿里不上页面的条目序号（从 0 起）。
OVR = {
 'michelson': dict(
    short='干涉仪', laur='迈克尔逊', era='1881 / 1887', place='波茨坦 / 克利夫兰',
    sites=[('克利夫兰', 41.50, -81.61), ('波茨坦（1881）', 52.38, 13.06)],
    tag='一块浮在水银上的石板，测出了「什么都没有」。',
    tool=dict(size_m=1.5, size_what='砂岩板边长（等效臂长 11 米）', mass_t=None, mass_what='石板质量没有查到',
              people=2, people_what='1887 年论文作者数', t_idea=1881, t_result=1887, t_prize=1907),
    cost=None, cost_what='造价没有查到',
    shape=dict(kind='sq', w=1.5, h=1.5),
    drop_awards=[0],
 ),
 'leiden': dict(
    short='莱顿低温实验室', laur='卡末林·昂内斯', era='1882–1911', place='莱顿，荷兰',
    sites=[('莱顿', 52.16, 4.49)],
    tag='准备了 26 年，为了一个 16 小时的工作日和 60 毫升液体。',
    tool=dict(size_m=None, size_what='这座装置的标尺是温度：当天减压到约 1.7 K', mass_t=None, mass_what='',
              people=32, people_what='1904 年在册学徒数；实验室总人数没有查到', t_idea=1882, t_result=1908, t_prize=1913),
    cost=None, cost_what='经费没有查到',
    shape=None,
 ),
 'cyclotron': dict(
    short='回旋加速器', laur='劳伦斯', era='1931–1939', place='伯克利，美国',
    sites=[('伯克利', 37.87, -122.26)],
    tag='五代机器，八年，每一代都替下一代筹到了钱。',
    tool=dict(size_m=1.52, size_what='60 英寸回旋加速器的磁极直径（1946 年的 184 英寸为 4.67 米）', mass_t=220, mass_what='60 英寸的磁铁，约数（另一说 200 吨）',
              people=60, people_what='1939 年辐射实验室人数', t_idea=1929, t_result=1932, t_prize=1939),
    cost=(550000, 'USD', 1939, '1931–1940 年募到的经费与设备总值，不含 184 英寸的一百多万美元'),
    shape=dict(kind='circ', w=1.52, h=1.52),
 ),
 'bubble': dict(
    short='72 英寸气泡室', laur='阿尔瓦雷茨', era='1953–1959', place='伯克利，美国',
    sites=[('伯克利', 37.88, -122.25)],
    tag='一只装液氢的金属盒，加一条把照片变成数据的流水线。',
    tool=dict(size_m=1.83, size_what='气泡室内腔长度', mass_t=240, mass_what='整机，不含制冷设备',
              people=None, people_what='「数百人」，没有确数', t_idea=1953, t_result=1960, t_prize=1968),
    cost=(2100000, 'USD', 1959, '伯克利实验室 1981 年史稿的数字；是否含计算机与厂房未说明'),
    shape=dict(kind='rect', w=1.83, h=0.51),
 ),
 'cambridge': dict(
    short='一英里望远镜与闪烁阵', laur='赖尔与休伊什', era='1964 / 1967', place='剑桥，英国',
    sites=[('剑桥', 52.17, 0.03)],
    tag='三面小天线、800 米铁轨、地球自转，外加一片学生打桩搭起来的偶极子阵。',
    tool=dict(size_m=1600, size_what='一英里望远镜的最长基线', mass_t=360, mass_what='三面天线合计',
              people=5, people_what='1968 年脉冲星论文作者数', t_idea=1962, t_result=1967, t_prize=1974),
    cost=None, cost_what='闪烁阵约 1.5 万英镑（1960 年代中期）；一英里望远镜的造价没有查到',
    shape=dict(kind='line', w=1600, h=18),
    drop_anecdotes=[4],
 ),
 'spps': dict(
    short='质子–反质子对撞机', laur='鲁比亚与范德梅尔', era='1976–1983', place='日内瓦近郊，瑞士与法国',
    sites=[('CERN', 46.23, 6.05)],
    tag='没有另挖隧道：把刚投产的加速器改成对撞机，添一个小环，一天天地攒反质子。',
    tool=dict(size_m=2200, size_what='SPS 环的直径（周长约 6.9 公里）', mass_t=2000, mass_what='UA1 探测器',
              people=185, people_what='UA1 约 130 位加 UA2 约 50–60 位物理学家', t_idea=1976, t_result=1983, t_prize=1984),
    cost=(200000000, 'CHF', 1978, '质子–反质子对撞机项目的造价，按 1978 年立项时的币值折算；是否含探测器与积累环不详'),
    shape=dict(kind='ring', w=2200, h=2200),
    drop_anecdotes=[3, 4],
 ),
 'homestake': dict(
    short='Homestake 氯探测器', laur='戴维斯', era='1965–1994', place='利德，美国南达科他州',
    sites=[('Homestake', 44.35, -103.75)],
    tag='615 吨干洗液放在 1,478 米深的金矿里，每两个月捞出十几个原子。',
    tool=dict(size_m=14.6, size_what='罐体长度（通行口径；埋深 1,478 米）', mass_t=615, mass_what='四氯乙烯',
              people=3, people_what='建造与早期运行的核心团队', t_idea=1964, t_result=1968, t_prize=2002),
    cost=(600000, 'USD', 1965, '洞室开挖、钢罐与液体，不含 25 年的运行费'),
    shape=dict(kind='rect', w=14.6, h=6.1),
    drop_anecdotes=[4],
 ),
 'cobe': dict(
    short='COBE 卫星', laur='马瑟与斯穆特', era='1974–1993', place='900 公里高的太阳同步轨道',
    sites=[('戈达德航天中心', 38.99, -76.85)],
    tag='火箭换了，卫星减重一半，三台仪器一台没少。',
    tool=dict(size_m=5.49, size_what='卫星长度（太阳翼展开后跨 8.53 米）', mass_t=2.27, mass_what='发射质量',
              people=1500, people_what='参与项目的总人数（另一口径 1,000 多）', t_idea=1974, t_result=1990, t_prize=2006),
    cost=(150000000, 'USD', 1989, '媒体数字（1989 年 1.5 亿、1992 年 1.6 亿美元），官方数字没有查到，置信度低'),
    shape=dict(kind='rect', w=8.53, h=5.49),
    drop_anecdotes=[4, 5],
 ),
 'lhc': dict(
    short='大型强子对撞机', laur='恩格勒与希格斯', era='1984–2012', place='日内瓦近郊，瑞士与法国',
    sites=[('CERN', 46.23, 6.05)],
    tag='27 公里的旧隧道，1,232 块 1.9 K 的磁铁，和一个烧毁的接头。',
    tool=dict(size_m=8486, size_what='环的直径（周长 26,659 米）', mass_t=36000, mass_what='加速器的冷质量（CMS 探测器另重 14,000 吨）',
              people=6000, people_what='2013 年 ATLAS 与 CMS 各约 3,000 人', t_idea=1984, t_result=2012, t_prize=2013),
    cost=(4332000000, 'CHF', 2008, 'CERN 官方口径，不含人工：机器与实验区 37.56 亿，加 CERN 分担的探测器与计算'),
    shape=dict(kind='ring', w=8486, h=8486),
    drop_anecdotes=[4],
 ),
 'superk-sno': dict(
    short='超级神冈与 SNO', laur='梶田隆章与麦克唐纳', era='1983–2006', place='神冈，日本；萨德伯里，加拿大',
    sites=[('超级神冈', 36.43, 137.31), ('SNO', 46.48, -81.20)],
    tag='一只 5 万吨的水罐和一只借来的 1,000 吨重水球，回答同一个问题。',
    tool=dict(size_m=41.4, size_what='超级神冈水罐的高度（直径 39.3 米）', mass_t=50000, mass_what='超级神冈的超纯水（SNO 重水 1,000 吨）',
              people=221, people_what='超级神冈 1998 年论文 121 位作者，加 SNO 约 100 人', t_idea=1984, t_result=1998, t_prize=2015),
    cost=(73000000, 'CAD', 1999, 'SNO 的建造费，不含借来的重水，按 1999 年开始取数时的汇率与物价折算；超级神冈的造价没有查到一手数字'),
    shape=dict(kind='rect', w=39.3, h=41.4),
    drop_anecdotes=[5],
 ),
 'ligo': dict(
    short='LIGO', laur='韦斯、巴里什、索恩', era='1972–2015', place='汉福德与利文斯顿，美国',
    sites=[('汉福德', 46.46, -119.41), ('利文斯顿', 30.56, -90.77)],
    tag='在 4 公里上量出 10⁻¹⁸ 米，之前先等了八年的「什么都没有」。',
    tool=dict(size_m=4000, size_what='单臂长度（两站相距 3,002 公里）', mass_t=None, mass_what='不比质量：每站约 1 万立方米真空，镜子只有 40 公斤',
              people=1005, people_what='发现论文作者数', t_idea=1972, t_result=2015, t_prize=2017),
    cost=[(365400000, 'USD', 1994, '1994 年批准的方案，含 0.687 亿调试运行费'),
          (205120000, 'USD', 2008, 'Advanced LIGO')],
    cost_note='；这是两笔建造费，和「到 2016 年累计约 11 亿美元」的投入不是同一口径',
    shape=dict(kind='L', w=4000, h=4000),
 ),
 'icecube': dict(
    short='IceCube', laur='哈尔岑', era='1988–2013', place='南极点',
    sites=[('南极点', -89.99, -63.45)],
    tag='把南极的一立方公里冰变成探测器，装下去就再也修不了。',
    tool=dict(size_m=1000, size_what='阵列的高度与水平跨度，各约 1 公里', mass_t=1000000000, mass_what='仪器覆盖的冰',
              people=450, people_what='合作组成员数（2025 年口径）', t_idea=1988, t_result=2013, t_prize=2026),
    cost=(279500000, 'USD', 2008, '建造费，2004–2010 年当年价合计，不含运行；折算取 2008 年'),
    shape=dict(kind='rect', w=1000, h=1000),
 ),
}

# 对比器里另外可选的参照物与未来装置（尺寸出处见展望部分各课题）
EXTRA_SHAPES = [
    dict(id='ref-man', group='参照物', name='一个人', size_m=1.75, kind='rect', w=0.5, h=1.75, note='身高按 1.75 米'),
    dict(id='ref-pitch', group='参照物', name='足球场', size_m=105, kind='rect', w=105, h=68, note='105 × 68 米'),
    dict(id='ref-tower', group='参照物', name='上海中心大厦', size_m=632, kind='rect', w=90, h=632, note='高 632 米'),
    dict(id='fut-fcc', group='在建与设想', name='FCC 隧道（待批）', size_m=28900, kind='ring', w=28900, h=28900, note='周长 90.7 公里，折合直径约 29 公里'),
    dict(id='fut-ce', group='在建与设想', name='Cosmic Explorer（设计中）', size_m=40000, kind='L', w=40000, h=40000, note='臂长 40 公里'),
    dict(id='fut-dune', group='在建与设想', name='DUNE 的束流基线（在建）', size_m=1300000, kind='line', w=1300000, h=1, note='1,300 公里'),
    dict(id='fut-lisa', group='在建与设想', name='LISA（已批准）', size_m=2500000000, kind='tri', w=2500000000, h=2165000000, note='边长 250 万公里的三角形'),
]

# ---------------------------------------------------------------- 第 1 章：今年的奖
CH1 = dict(
    lede='2026 年 10 月 6 日，瑞典皇家科学院把诺贝尔物理学奖授予威斯康星大学麦迪逊分校的弗朗西斯·哈尔岑（Francis Halzen），'
         '一人独得，奖金 1,200 万瑞典克朗，12 月 10 日在斯德哥尔摩颁奖。新闻稿的标题是「在南极点捕获来自宇宙的难以捉摸的粒子」。',
    who='哈尔岑 1944 年生于比利时蒂嫩，是理论物理学家。1988 年他与 John Learned 提出把极地的冰当中微子探测器，'
        '此后推动建成 AMANDA 和 IceCube，2001 年起任 IceCube 首席科学家。',
    quote=dict(
        zh='这是一场不保证成功的冒险，我们运气好，才闯过各种难关。',
        en='This was kind of an adventure where success was not guaranteed, and we were lucky to overcome the various challenges.',
        by='哈尔岑，得奖当天对 Physics Today 说',
        url='https://physicstoday.aip.org/news/francis-halzen-to-receive-2026-nobel-prize-in-physics-for-cosmic-neutrino-detection'),
    hooks=[
        dict(h='颁奖词点了装置的名字',
             p='今年的颁奖词里，「决定性贡献」后面跟的是一座装置。这个句式以前出现过：1968 年跟的是一门学科，句尾才点到氢气泡室这门技术；1984 年是一个「项目」；2017 年是 LIGO。'
               '2013 年的颁奖词没有 decisive 这个词，却写明预言是由 CERN 大型强子对撞机上的 ATLAS 与 CMS 实验证实的。'),
        dict(h='三十四年来第一次一人独得',
             p='上一位独得物理学奖的是 1992 年的夏帕克（Georges Charpak），理由是发明多丝正比室，也是一件探测器。'
               '诺贝尔奖一项最多由三人分享；IceCube 合作组约 450 人，来自 14 个国家的 58 家机构。'),
        dict(h='中微子这条线第五次获奖',
             p='1988 年奖给中微子束，1995 年奖给第一次探测到中微子，2002 年奖给太阳和超新星的中微子，2015 年奖给中微子振荡，今年奖给来自天体的高能中微子。'
               '把这几次用的装置按年代排开，靶的质量从约 400 升水到约 10 亿吨冰，首尾差九个多数量级；中间不是逐台变大，SNO 只有 1,000 吨重水。'),
    ],
    citations=[
        dict(year=1968, who='阿尔瓦雷茨', names='点到方法',
             en='for his decisive contributions to elementary particle physics, in particular the discovery of a large number of resonance states, made possible through his development of the technique of using hydrogen bubble chamber and data analysis',
             zh='表彰他对基本粒子物理的决定性贡献，特别是发现了大量共振态；这些发现得以实现，靠的是他发展出的氢气泡室技术和数据分析方法',
             src='诺贝尔奖官网，2026-10-09 逐字对过'),
        dict(year=1984, who='鲁比亚与范德梅尔', names='点到「项目」',
             en='for their decisive contributions to the large project, which led to the discovery of the field particles W and Z, communicators of weak interaction',
             zh='表彰他们对一个大型项目的决定性贡献，这个项目导致发现了传递弱相互作用的场粒子 W 和 Z',
             src='瑞典皇家科学院得主页'),
        dict(year=2017, who='韦斯、巴里什、索恩', names='点到装置：LIGO',
             en='for decisive contributions to the LIGO detector and the observation of gravitational waves',
             zh='表彰他们对 LIGO 探测器和观测到引力波的决定性贡献',
             src='瑞典皇家科学院新闻稿'),
        dict(year=2026, who='哈尔岑', names='点到装置：IceCube',
             en='for decisive contributions to the IceCube Neutrino Observatory and the discovery of high-energy neutrinos of astrophysical origin',
             zh='表彰他对冰立方中微子天文台和发现源自天体的高能中微子的决定性贡献',
             src='瑞典皇家科学院新闻稿'),
    ],
    cite_note='含 decisive 一词的物理学奖颁奖词，逐年翻下来有五次：1968、1974、1984、2017、2026。1974 年那一次说的是休伊什在发现脉冲星中的「决定性作用」。'
              '这五年的原文都对过了；「没有别的年份」是把历年颁奖词过了一遍得出的，官网的总表没能打开，没法逐年检索，这半句置信度中。',
    # 中微子五次获奖所用的装置，按建成年份排；mass_t 用于画对数条
    nu=[
        dict(built=1956, what='萨凡纳河反应堆旁的探测器', mass='约 400 升水靶', mass_t=0.4, prize='1995 莱因斯', result='第一次探测到中微子'),
        dict(built=1962, what='布鲁克海文的中微子束与火花室', mass='火花室约 10 吨', mass_t=10, prize='1988 莱德曼、施瓦茨、施泰因贝格尔', result='发现 μ 子中微子'),
        dict(built=1967, what='Homestake 氯探测器', mass='615 吨四氯乙烯', mass_t=615, prize='2002 戴维斯', result='测到太阳中微子'),
        dict(built=1983, what='神冈', mass='3,000 吨水', mass_t=3000, prize='2002 小柴昌俊', result='超新星 1987A 的中微子'),
        dict(built=1996, what='超级神冈', mass='5 万吨水', mass_t=50000, prize='2015 梶田隆章', result='大气中微子振荡'),
        dict(built=1999, what='SNO', mass='1,000 吨重水', mass_t=1000, prize='2015 麦克唐纳', result='太阳中微子变了味'),
        dict(built=2010, what='IceCube', mass='约 10 亿吨冰', mass_t=1e9, prize='2026 哈尔岑', result='来自天体的高能中微子'),
    ],
    nu_note='质量是靶或探测介质的量，口径各不相同（SNO 另有约 7,000 吨轻水屏蔽）。年份：前两行是做实验的年份，其余是开始取数的年份，IceCube 取下完最后一根缆的 2010 年。'
            '1988 年的奖给的是方法，实验做于 1962 年。',
    program=dict(
        h='一张日程表',
        p='1998 年 6 月，日本高山，Neutrino \'98 会议。4 日，麦克唐纳讲 SNO 的进度；5 日上午（日程排在 9:55），梶田隆章报告大气中微子振荡的证据；'
          '9 日，哈尔岑讲 AMANDA 的结果和今后的打算。前两位 2015 年获奖，第三位等到了今年。',
        src='神冈观测所保存的会议日程（1998-05-28 的暂定版）'),
    china=dict(
        h='和中国的两条线',
        p='哈尔岑是上海交通大学李政道研究所第二届国际学术咨询委员会委员。南海中微子望远镜「海铃计划」的发起人徐东莲，'
          '2015–2018 年在威斯康星大学麦迪逊分校做博士后，其间在 IceCube 合作组。瑞典皇家科学院今年的科学背景材料把海铃与 IceCube-Gen2、KM3NeT、P-ONE、Baikal-GVD 并列为下一代装置。'),
    bridge='要掂量「对一座装置的决定性贡献」这句话，得从 1887 年克利夫兰的一间地下室翻起。',
)

CH2 = dict(
    lede='十二座，按获奖年份排。每座一张按比例画的示意图、一份任务书；卡片底下是逐条的资料和置信度，来源对不上的地方并列写出。'
         '奖给的人很少，做事的人很多，「人」一栏写的是得主之外的。',
    map_cap='十二座装置的位置。只画陆地轮廓，数字是卡片的序号；COBE 标的是研制它的戈达德航天中心，南极点画在图的底边。',
)
