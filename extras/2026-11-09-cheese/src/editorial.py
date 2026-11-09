# -*- coding: utf-8 -*-
"""号外 · 奶酪 — 中英文案（中文为主稿；事实只取自 research/*.json，改事实先改底稿）"""
def T(zh, en, **kw): d = {'zh': zh, 'en': en}; d.update(kw); return d

META = dict(
    slug='cheese', date='2026-11-09',
    title_zh='奶酪：让时间干活的七千年',
    title_en='Cheese: Seven Thousand Years of Letting Time Work',
    sub_zh='从安纳托利亚的陶罐讲到湾区的奶酪柜台：怎么来的、怎么做的、怎么尝、世界上别的地方怎么存奶。',
    sub_en='From Neolithic pots in Anatolia to a cheese counter in the Bay Area: where it came from, how it is made, how to taste it, and how the rest of the world keeps milk.',
    desc='关于奶酪的号外专题：七千年沿革，一块奶酪从一锅奶到熟成的工艺演示，品鉴光谱与风味轮，全球其他保存乳品的方式，以及湾区 Eataly、Whole Foods 奶酪柜台的导购。中英双语。',
)

HERO = dict(
    kick=T('号外 · 给 Daisy 与 Sichao', 'Extra · for Daisy & Sichao'),
    h1=T('奶会坏，<br>奶酪不会。', 'Milk spoils.<br>Cheese keeps.'),
    cta=T('从一只陶罐开始 ↓', 'Start with a pot ↓'),
)

NAV = [('hist', '00', T('沿革', 'History')), ('make', '01', T('做一块', 'Make')), ('taste', '02', T('品鉴', 'Taste')),
       ('world', '03', T('全球', 'World')), ('counter', '04', T('柜台', 'Counter')), ('end', '··', T('卷末', 'Notes'))]

HERO_SUB = T('<b>一块奶酪，是一锅奶加上时间。</b>七千多年前，安纳托利亚和波兰的早期农人就在陶罐里分离凝乳；今天，旧金山的柜台上摆着从帕尔马、汝拉到马林县的几百种轮子。这一期讲四件事：它怎么来的，它怎么做的，怎么尝，世界上别的地方怎么存奶——最后站到柜台前，看看怎么买。',
             '<b>A cheese is a pot of milk plus time.</b> More than seven thousand years ago, early farmers in Anatolia and Poland were already separating curds in clay pots; today a San Francisco counter holds hundreds of wheels, from Parma and the Jura to Marin County. Four things here: where it came from, how it is made, how to taste it, and how the rest of the world keeps milk — and then, at the counter, how to buy.')

THESIS = dict(
    zh=[('奶', 0), ('会坏，', 0), ('奶酪', 1), ('不会——', 0), ('人类', 0), ('花了', 0), ('七千年，', 1), ('学会', 0), ('让', 0), ('时间', 1), ('替自己', 0), ('干活。', 0)],
    en=[('Milk', 0), ('spoils;', 0), ('cheese', 1), ('keeps.', 0), ('Seven', 1), ('thousand', 1), ('years', 0), ('of', 0), ('letting', 0), ('time', 1), ('do', 0), ('the', 0), ('work.', 0)],
    nums=[
        T('前 6500', '6500 BC', k=T('年前后，安纳托利亚西北部的陶器里已有乳脂残留——人类加工奶的最早化学证据之一（分不出是奶、酸奶还是奶酪）。', 'or so: milk fat in pottery from north-western Anatolia, among the earliest chemical evidence of dairying (it cannot tell milk from yoghurt or cheese).')),
        T('400 升', '400 L', k=T('奶做一只约 40 公斤的孔泰轮子。一户人家的奶不够，所以汝拉山区的村子八百多年来一直把奶凑到合作奶坊（fruitière）里一起做。', 'of milk make one 40 kg wheel of Comté — more than one farm has, which is why Jura villages have pooled milk in co-operative dairies (fruitières) for some eight hundred years.')),
        T('60 天', '60 days', k=T('在美国，用未经巴氏杀菌的生乳做的奶酪，必须在 35°F（约 1.7°C）以上熟成至少 60 天才能卖。所以柜台上见不到生乳的新鲜奶酪。', 'is the US minimum: cheese from unpasteurised milk must be aged at least 60 days above 35 °F (about 1.7 °C) before sale — which is why no fresh raw-milk cheese reaches the counter.')),
    ],
)

CH = {
    'hist': dict(no='00 · HISTORY', h=T('七千年：把夏天的奶留到冬天', 'Seven thousand years of keeping summer milk for winter'),
                 lede=T('奶酪的历史，就是「怎样让奶多活几个月」的历史：陶滤器和胃袋，荷马的柳条筐，罗马士兵的口粮，修道院和国王的特许状，荷兰的过磅房，纽约州的第一家奶酪工厂，再到法定产区和手工复兴。往下滚，或者拖底部的刻度尺。',
                        'The history of cheese is the history of making milk last a few more months: clay sieves and stomach bags, Homer’s wicker baskets, Roman army rations, abbeys and royal charters, Dutch weigh-houses, New York’s first cheese factory, and then protected origins and the artisan revival. Scroll, or drag the ruler at the bottom.')),
    'make': dict(no='01 · MAKE', h=T('做一块奶酪：同一锅奶，十个旋钮', 'Make one: one pot of milk, ten dials'),
                 lede=T('所有奶酪都从一锅奶开始，走差不多同样的十步：选奶、加热、加菌、点凝乳酶、切、煮、排乳清、成型、加盐、熟成。差别只在每一步拧多大——温度高几度、凝乳切多小、盐水泡几天、在洞里放多久。左边挑一种，按播放，看它一步步变成自己。',
                        'Every cheese starts as a pot of milk and goes through roughly the same ten steps: milk, heat, culture, rennet, cut, cook, drain, form, salt, ripen. What differs is how far each dial is turned — a few degrees hotter, a smaller curd, more days in brine, longer in the cave. Pick one on the left, press play, and watch it become itself.')),
    'taste': dict(no='02 · TASTE', h=T('品鉴：一张光谱、一圈风味、一桌搭配', 'Taste: a spectrum, a wheel, a board'),
                  lede=T('尝奶酪不必背术语：先回温，从淡到浓，看、摸、闻、尝。下面把 28 种常见奶酪摆在「风味强度 × 软硬」的光谱上——点几种，排出你们自己的一组；再用风味轮找词，用搭配表找酒、啤酒、苹果酒和茶。',
                         'Tasting cheese needs no jargon: let it warm up, go from mild to strong, then look, touch, smell, taste. Below, 28 common cheeses sit on a spectrum of intensity against firmness — tap a few to build your own flight; then use the wheel to find words and the pairing list to find wine, beer, cider or tea.')),
    'world': dict(no='03 · WORLD', h=T('奶的其他活法', 'Other ways to keep milk'),
                  lede=T('奶酪只是人类存奶的一种办法。草原上把酸奶晒成石头一样的球，高原上把酥油封进皮囊，黎凡特把滤干的酸奶团成球泡进橄榄油，北欧和高加索让菌种在家里代代相传，爱尔兰人把黄油埋进泥炭沼泽。办法千差万别，原理却只有几条：发酵降 pH、去水、加盐、加糖、熬油封脂、烟熏、降温。',
                         'Cheese is only one of the ways people keep milk. On the steppe yoghurt is sun-dried into stone-hard balls; on the plateau butter is sealed in hides; in the Levant strained yoghurt is rolled into balls and sunk in olive oil; in the Nordic countries and the Caucasus cultures are handed down at home; in Ireland butter went into the peat bog. The methods are endless, the principles few: ferment to lower the pH, remove water, add salt or sugar, render and seal in fat, smoke, keep it cold.')),
}

BENCH_HEAD = T('选一种奶酪', 'Pick a cheese')
BENCH_NOTE = T('温度、时间、pH 优先取自各奶酪的原产地规范（PDO / AOP / PGI）；规范没写的，取自大学教材与行业资料，个别为通行做法。表里的「—」是规范和资料里都没有给数。熟成时间尺是对数刻度：一格是十倍。',
               'Temperatures, times and pH come first from each cheese’s protected-origin specification (PDO / AOP / PGI); where the specification is silent, from university textbooks and industry sources, occasionally from common practice. A “—” means no figure was given. The ageing scale below is logarithmic: each step is ten times longer.')
AGE_HEAD = T('熟成：从一天到三年', 'Ageing: from one day to three years')
SPEC_HEAD = T('品鉴光谱', 'Tasting spectrum')
SPEC_NOTE = T('位置是按家族、熟成时长和含水量做的估计，不是哪一张公开的品鉴图表；同一种奶酪，不同产家、不同月份会差很多。点圆点看介绍，再点「加进一组」。',
              'Positions are estimates from family, age and moisture, not taken from any published tasting chart; the same cheese varies a lot by maker and month. Tap a dot for notes, then “Add to tasting flight”.')
FLIGHT_TIP = T('每人每种约 30–60 克，一次 3–5 种正好。从淡吃到浓，中间喝口水或吃片苹果清口。', 'About 30–60 g per person per cheese, three to five at a time. Go mild to strong; water or a slice of apple in between.')
WHEEL = dict(title=T('风味轮', 'Flavour wheel'),
             intro=T('内圈是九族气味，外圈是具体的词。点一格，看它常出现在哪种奶酪里、来自哪种化合物。结构取自欧洲研究项目的硬质与半硬质奶酪风味轮（Bérodier 等，1997），具体词与化合物参考了切达风味词表（Drake 等，2001）；「味觉与口感」一环是为了好用另加的。',
                     'The inner ring holds nine aroma families, the outer ring the words. Tap a cell to see which cheeses it turns up in and which compound is behind it. The structure follows the European wheel for hard and semi-hard cheeses (Bérodier et al., 1997), with words and compounds from a Cheddar lexicon (Drake et al., 2001); the “taste & mouthfeel” ring is an addition for practical use.'))
PAIR_HEAD = T('搭配：按类别找', 'Pairing, by kind')
PAIR_KINDS = [('wine', T('葡萄酒', 'Wine')), ('beer', T('啤酒', 'Beer')), ('cider', T('苹果酒', 'Cider')), ('tea', T('茶', 'Tea')), ('sweet', T('蜂蜜 · 果酱 · 坚果', 'Honey · fruit · nuts')), ('spirit', T('烈酒 · 清酒', 'Spirits · sake'))]
TASTE_HEAD = T('先学会怎么吃', 'First, how to eat it')
WORLD_HEAD = T('八条原理', 'Eight principles')
WORLD_LIST_HEAD = T('二十三种别的存奶法', 'Twenty-three other ways')

AREAS = [('steppe', T('草原与高原', 'Steppe & plateau')), ('westasia', T('西亚与北非', 'West Asia & N. Africa')), ('southasia', T('南亚', 'South Asia')),
         ('eastasia', T('东亚', 'East Asia')), ('europe', T('欧洲', 'Europe')), ('africa', T('东非', 'East Africa')), ('americas', T('美洲', 'Americas')), ('global', T('全球', 'Global'))]

# ---------- 00 沿革舞台（事实取自 hist_A.json；一步一个画面） ----------
STAGE = [
    dict(id='pot', label=T('前6500', '6500 BC'), yr=T('约前 6500', 'c. 6500 BC'), era=T('新石器时代 · 陶器里的奶', 'Neolithic · milk in the pots'),
         title=T('先有奶的痕迹，后有奶酪', 'First, traces of milk'),
         text=T('对两千两百多件新石器时代陶器的脂质分析显示，安纳托利亚西北部（马尔马拉海周边）在公元前 7 千纪已经加工乳品；撒哈拉中部 Takarkori 岩厦的陶器里，公元前 5 千纪的「绿色撒哈拉」牧民也留下了乳脂。这类证据只说明「用奶」，分不出是鲜奶、酸奶还是奶酪。',
                'Lipid analysis of more than 2,200 Neolithic pots shows dairying in north-western Anatolia, around the Sea of Marmara, in the 7th millennium BC; at Takarkori in the central Sahara, herders of the “green Sahara” left milk fat in pots in the 5th millennium BC. Such residues show milk use — they cannot tell milk from yoghurt or cheese.'),
         tags=[T('安纳托利亚', 'Anatolia'), T('撒哈拉', 'Sahara')], img='h-pot'),
    dict(id='sieve', label=T('前5500', '5500 BC'), yr=T('约前 5500–5200', 'c. 5500–5200 BC'), era=T('新石器时代 · 陶滤器', 'Neolithic · clay sieves'),
         title=T('一只带孔的陶罐', 'A pot full of holes'),
         text=T('波兰中北部库亚维亚的线纹陶文化遗址出土了穿孔陶滤器，内壁满是乳脂，研究者认为是用来把凝乳和乳清分开的——欧洲做奶酪最早的直接化学证据，约七千到七千五百年前。克罗地亚达尔马提亚沿岸约公元前 5200 年的陶器里也检出了奶酪。早期农人成年后大多消化不了乳糖，而乳糖大半随乳清流走，所以研究者推测：奶酪比「成年人喝奶」来得更早。',
                'Perforated clay sieves from Linear Pottery sites in Kuyavia, north-central Poland, are coated with milk fat and are thought to have separated curds from whey — Europe’s earliest direct chemical evidence of cheesemaking, some 7,000–7,500 years old. Pots from the Dalmatian coast of Croatia show cheese by about 5200 BC. Most early farmers could not digest lactose as adults, and most lactose drains away with the whey — so cheese probably came before adults drank milk.'),
         tags=[T('库亚维亚', 'Kuyavia'), T('达尔马提亚', 'Dalmatia'), T('乳糖', 'Lactose')], img='h-sieve'),
    dict(id='ur', label=T('前2500', '2500 BC'), yr=T('前 2500 – 前 1200', '2500–1200 BC'), era=T('青铜时代 · 两河与埃及', 'Bronze Age · Mesopotamia and Egypt'),
         title=T('神庙账本上的 ga-àr', 'ga-àr in the temple ledgers'),
         text=T('伊拉克乌拜德土丘宁胡尔萨格神庙的镶嵌饰带（约公元前 2500 年）画着挤奶和在大罐里处理奶的场面；乌尔第三王朝（约前 2100–前 2000 年）的楔形文字账目里，奶酪（ga-àr）与黄油成批登记。埃及萨卡拉的孟菲斯市长 Ptahmes 墓（约前 13 世纪）出土一团发白的固体，2018 年经蛋白质组学认定是牛奶与绵羊或山羊奶混做的奶酪。',
                'An inlaid frieze from the temple of Ninhursag at Tell al-Ubaid, Iraq (c. 2500 BC), shows milking and milk handled in big jars; Ur III cuneiform accounts (c. 2100–2000 BC) list cheese (ga-àr) and butter by the batch. In the tomb of Ptahmes, mayor of Memphis, at Saqqara (13th c. BC), a whitish mass was identified in 2018 by proteomics as cheese made from cow’s milk mixed with sheep or goat milk.'),
         tags=[T('乌尔', 'Ur'), T('萨卡拉', 'Saqqara')], img='h-ur'),
    dict(id='xiaohe', label=T('前1600', '1600 BC'), yr=T('约前 1600', 'c. 1600 BC'), era=T('青铜时代 · 新疆', 'Bronze Age · Xinjiang'),
         title=T('小河墓地：木乃伊胸前的奶酪', 'Xiaohe: cheese on the mummies’ chests'),
         text=T('新疆罗布泊附近的小河墓地，木乃伊颈部和胸前随葬着块状奶酪，最早约公元前 1600 年。2014 年的研究认为它不用凝乳酶，而是用类似开菲尔粒的乳酸菌和酵母发酵而成；2024 年中科院古脊椎所付巧妹团队在《Cell》上发表古 DNA 结果，从中重建出开菲尔乳杆菌的基因组，牛奶和山羊奶分批使用、互不相混。',
                'At the Xiaohe cemetery near Lop Nur, Xinjiang, lumps of cheese lay on the necks and chests of the mummies, the oldest from about 1600 BC. A 2014 study found no rennet: it was fermented with kefir-like bacteria and yeasts. In 2024 Fu Qiaomei’s team at the Chinese Academy of Sciences published ancient DNA in <i>Cell</i>, rebuilding the genome of <i>Lactobacillus kefiranofaciens</i> and finding that cow and goat milk were used in separate batches.'),
         tags=[T('开菲尔', 'Kefir'), T('古 DNA', 'Ancient DNA')], img='h-xiaohe'),
    dict(id='homer', label=T('前8世纪', '8th c. BC'), yr=T('约前 8 世纪', 'c. 8th c. BC'), era=T('古希腊 · 史诗', 'Ancient Greece · epic'),
         title=T('独眼巨人的柳条筐', 'The Cyclops’ wicker baskets'),
         text=T('《奥德赛》第九卷，波吕斐摩斯挤完绵羊和山羊：「于是他立刻把一半白奶凝结起来，收进柳条编的筐里放好；另一半盛在器皿里，留着喝，当晚饭。」这是西方文学里最早的做奶酪场景——一半当下喝，一半留给以后。',
                'In <i>Odyssey</i> 9, Polyphemus milks his sheep and goats: “Then presently he curdled half the white milk, and gathered it in wicker baskets and laid it away, and the other half he set in vessels… that it might serve him for supper.” The earliest cheesemaking scene in Western literature — half for now, half for later.'),
         tags=[T('《奥德赛》', 'Odyssey')], img='h-homer'),
    dict(id='rome', label=T('60–77', 'AD 60–77'), yr=T('公元 60–77', 'AD 60–77'), era=T('罗马 · 农书与口粮', 'Rome · farm manuals and rations'),
         title=T('「甚至可以运过海去」', '“It can even be shipped overseas”'),
         text=T('科卢梅拉《论农业》（约公元 60–65 年）写下完整工艺：用羔羊或小山羊的凝乳酶，也可用野蓟花、红花籽或无花果树汁使奶凝结；沥乳清、压重物、撒盐晾干，压得紧实、充分干燥的奶酪「甚至可以运过海去」。老普林尼《自然史》（公元 77 年）开出名奶酪榜，卢纳奶酪一只重达千磅。据《罗马帝王纪》，哈德良在军营里与士兵同吃腌肉、奶酪和掺水的酸酒。',
                'Columella’s <i>On Agriculture</i> (c. AD 60–65) gives a full method: set the milk with lamb or kid rennet, or with wild-thistle flowers, safflower seed or fig sap; drain, press, salt and dry — a firm, well-dried cheese “can even be shipped overseas.” Pliny’s <i>Natural History</i> (AD 77) ranks famous cheeses; one from Luna could weigh a thousand pounds. Hadrian, says the <i>Historia Augusta</i>, ate camp fare with his soldiers: bacon, cheese and sour wine.'),
         tags=[T('凝乳酶', 'Rennet'), T('罗马军粮', 'Army rations')], img='h-rome'),
    dict(id='qmys', label=T('533', '533'), yr=T('约 533–544', 'c. 533–544'), era=T('北魏 · 《齐民要术》', 'Northern Wei · Qimin Yaoshu'),
         title=T('酪、酥、醍醐与「干酪」', 'Lao, su, tihu — and “dry lao”'),
         text=T('中国古书里的乳品有几个基本字：「酪」近似发酵变稠的奶，「酥」近似黄油，「醍醐」是从酥里再提的精油。北魏贾思勰《齐民要术》卷六记有作酪、作干酪、抨酥等法，其中「干酪」是把酪晒出表皮、反复撇取、炒后捏成梨大的团再晒干，「得经数年不坏，以供远行」——中国古书里最接近硬质奶酪的记载。',
                'Classical Chinese has a few basic dairy words: <i>lao</i>, roughly thickened soured milk; <i>su</i>, roughly butter; <i>tihu</i>, an oil refined again from <i>su</i>. Jia Sixie’s <i>Qimin Yaoshu</i> (c. 533–544) gives methods for <i>lao</i>, “dry <i>lao</i>” and churned <i>su</i>. Dry <i>lao</i> was sun-crusted, skimmed again and again, pan-fried, shaped into pear-sized balls and dried — it “keeps for several years without spoiling, and serves for long journeys,” the closest thing to a hard cheese in old Chinese texts.'),
         tags=[T('酪', 'lao'), T('酥', 'su'), T('醍醐', 'tihu')], img='h-qmys'),
    dict(id='abbey', label=T('1115', '1115'), yr=T('1115 – 1411', '1115–1411'), era=T('中世纪 · 修道院、山牧与特许状', 'Middle Ages · abbeys, alps and charters'),
         title=T('今天的名字，多半这时候有了', 'Most of today’s names appear'),
         text=T('格吕耶尔的奶酪生产可追溯到 1115 年；帕尔马奶酪（caseus parmensis）1254 年见于热那亚的公证文书；汝拉山区的村子把各家的奶凑到合作奶坊一起做孔泰，常引的最早文书在 13 世纪；1411 年法王查理六世颁特许状给罗克福尔村民，理由是那里「既不长一株葡萄，也不长一粒麦子」。罗马之后，奶酪技术很大程度上靠修道院和庄园延续。',
                'Cheesemaking in Gruyère is traced to 1115; “Parma cheese” (<i>caseus parmensis</i>) appears in a Genoese notarial deed in 1254; Jura villages pooled milk to make Comté in co-operative dairies, with the earliest records usually cited from the 13th century; and in 1411 Charles VI granted a charter to the people of Roquefort, a place where “not a vine nor a grain of wheat grows.” After Rome, much of the craft survived in abbeys and manors.'),
         tags=[T('格吕耶尔', 'Gruyère'), T('帕玛森', 'Parmigiano'), T('孔泰', 'Comté'), T('罗克福尔', 'Roquefort')], img='h-abbey'),
    dict(id='market', label=T('1365', '1365'), yr=T('1365 – 1778', '1365–1778'), era=T('近世 · 荷兰的过磅房', 'Early modern · Dutch weigh-houses'),
         title=T('按重量计税的奶酪', 'Cheese taxed by the pound'),
         text=T('阿尔克马尔 1365 年起已有奶酪过磅交易，1593 年奶酪集市正式开办；豪达 1395 年取得集市权，1668 年建成过磅房——豪达奶酪是以集散地、而不是以产地得名的。小而硬、耐储运的埃丹奶酪上了远洋船。1724 年笛福写到斯蒂尔顿镇以奶酪闻名，称之为「我们英国的帕玛森」，其实奶酪是周边莱斯特郡等地做、在镇上驿站转卖的。',
                'Alkmaar was weighing cheese for sale by 1365, with its market formally opened in 1593; Gouda won market rights in 1395 and built its weigh-house in 1668 — Gouda is named for where it was sold, not where it was made. Small, hard, travel-proof Edam went to sea. In 1724 Defoe called Stilton’s cheese “our English Parmesan”, though it was made around Leicestershire and sold at the coaching inns in town.'),
         tags=[T('阿尔克马尔', 'Alkmaar'), T('豪达', 'Gouda'), T('埃丹', 'Edam'), T('斯蒂尔顿', 'Stilton')], img='h-market'),
    dict(id='factory', label=T('1851', '1851'), yr=T('1851', '1851'), era=T('工业化 · 工厂、发酵剂与凝乳酶', 'Industrial · factories, cultures, rennet'),
         title=T('纽约州罗马镇的第一家奶酪工厂', 'The first cheese factory, Rome, New York'),
         text=T('1851 年，纽约州罗马镇的杰西·威廉斯开始收邻居的奶、集中做切达，这被视为「奶酪工厂制度」的开端；1905 年威斯康星已有 1518 家奶酪厂。1874 年哥本哈根的克里斯蒂安·汉森开始卖强度一致的液体凝乳酶；约 1890 年，丹麦、德国、美国先后分离出纯种乳酸菌发酵剂——奶酪厂第一次不必「靠天」。代价也来了：1881–1896 年，掺猪油的「填充奶酪」让美国奶酪在英国失去信誉，出口跌了四分之三。',
                'In 1851 Jesse Williams of Rome, New York, began buying his neighbours’ milk to make Cheddar in one place — the start of the factory system; by 1905 Wisconsin had 1,518 cheese factories. In 1874 Christian Hansen in Copenhagen began selling standardised liquid rennet, and around 1890 pure lactic starter cultures were isolated in Denmark, Germany and the US — factories no longer depended on luck. There was a cost: in 1881–1896 lard-“filled” cheese cost American cheese its name in Britain, and exports fell by three-quarters.'),
         tags=[T('切达', 'Cheddar'), T('威斯康星', 'Wisconsin'), T('发酵剂', 'Starter cultures')], img='h-factory'),
    dict(id='ration', label=T('1916', '1916'), yr=T('1911 – 1954', '1911–1954'), era=T('加工奶酪与战时配给', 'Process cheese and wartime rationing'),
         title=T('熔化奶酪与「政府切达」', 'Melted cheese and “Government Cheddar”'),
         text=T('1911 年瑞士图恩的 Gerber 与 Stettler 把埃曼塔加热熔化、加柠檬酸钠，做出耐储运的熔化奶酪；1916 年芝加哥的卡夫拿到美国专利 1,186,524。二战时英国从 1941 年到 1954 年实行奶酪配给，只准做少数几种统一规格的硬奶酪，俗称「政府切达」；约克郡的温斯利代尔，1939 年有 176 家生产者，1946 年只剩 9 家。',
                'In 1911 Gerber and Stettler in Thun, Switzerland, melted Emmentaler with sodium citrate into a shelf-stable process cheese; in 1916 James L. Kraft of Chicago received US patent 1,186,524. Britain rationed cheese from 1941 to 1954 and allowed only a few standardised hard cheeses — “Government Cheddar”. Yorkshire’s Wensleydale had 176 makers in 1939 and nine in 1946.'),
         tags=[T('加工奶酪', 'Process cheese'), T('温斯利代尔', 'Wensleydale')], img='h-ration'),
    dict(id='aoc', label=T('1925', '1925'), yr=T('1925 – 1996', '1925–1996'), era=T('原产地保护', 'Protected origin'),
         title=T('名字也要有产地', 'A name tied to a place'),
         text=T('1925 年 7 月 26 日，法国立法保护罗克福尔的原产地名称——法国第一个受法律保护的奶酪产地名。1951 年欧洲多国签订斯特雷萨公约，把名字分成只能在原产地做的「原产地名称」，和别国按标准也能做的「典型名称」（所以世界各地都能卖 Camembert、Gouda，受保护的是「Camembert de Normandie」「Gouda Holland」这样的全名）。1992 年欧共体建立 PDO / PGI 两级制度，1996 年公布首批名单。',
                'On 26 July 1925 France protected the name Roquefort by law — the country’s first legally protected cheese origin. The 1951 Stresa Convention split names into “appellations of origin”, made only in their place, and “typical names” anyone may make to a standard (which is why Camembert and Gouda are made everywhere, while “Camembert de Normandie” and “Gouda Holland” are protected). In 1992 the EEC created the PDO and PGI tiers; the first list came out in 1996.'),
         tags=[T('AOC', 'AOC'), T('斯特雷萨', 'Stresa'), T('PDO / PGI', 'PDO / PGI')], img='h-aoc'),
    dict(id='artisan', label=T('1983', '1983'), yr=T('1983 – 今天', '1983 – today'), era=T('手工复兴', 'The artisan revival'),
         title=T('从康奈尔到马林县', 'From Cornell to Marin'),
         text=T('1983 年，康奈尔大学的 Frank Kosikowski 创立美国奶酪协会，把散落各地的小作坊连起来。湾区北部是这场复兴的重镇：佩塔卢马的 Marin French Cheese 自称美国连续经营最久的奶酪厂（1865）；Laura Chenel 1979 年在索诺玛开始商业做山羊奶酪；Cowgirl Creamery 1997 年在雷斯岬站开张；Point Reyes 农场 2000 年推出蓝纹 Original Blue。另一头，2024 年全美奶酪产量 142.5 亿磅，威斯康星第一、加州第二。',
                'In 1983 Frank Kosikowski of Cornell founded the American Cheese Society to link scattered small makers. The North Bay became a centre of the revival: Petaluma’s Marin French Cheese calls itself America’s longest continuously operating cheese company (1865); Laura Chenel began making goat cheese commercially in Sonoma in 1979; Cowgirl Creamery opened in Point Reyes Station in 1997; and Point Reyes Farmstead launched Original Blue in 2000. At the other end of the scale, the US made 14.25 billion lb of cheese in 2024 — Wisconsin first, California second.'),
         tags=[T('Mt Tam', 'Mt Tam'), T('Original Blue', 'Original Blue'), T('Dry Jack', 'Dry Jack')], img='h-artisan'),
]

ASIA_HEAD = T('东边的酪、酥与奶片', 'Lao, su and milk fans in the East')
ASIA_NOTE = T('乳品在东亚不只是「舶来品」。下面是中国、蒙古、西藏、日本和印度的几条线索，点开看。', 'Dairy in Asia is not only an import. A few threads from China, Mongolia, Tibet, Japan and India — tap to open.')
ASIA_ITEMS = [
    ('cn-laonu', T('「酪奴」', '“Slave to lao”'), T('北魏 · 茶与酪孰优', 'Northern Wei · tea versus lao'), T('王肃一句玩笑，让茶在北魏得了个外号。', 'A joke by Wang Su gave tea a nickname in the Northern Wei.')),
    ('cn-tihu', T('醍醐灌顶', 'Tihu poured on the crown'), T('佛经 · 乳的五个阶段', 'Buddhist sutra · five stages of milk'), T('从乳到醍醐，五步提炼成了一个成语。', 'Five stages of refining milk became an idiom.')),
    ('cn-tang', T('唐代的酥山', 'Tang “butter mountains”'), T('唐 · 宫廷与城市', 'Tang · court and city'), T('冻起来当甜点的酥，和当药用的奶。', 'Frozen su desserts, and milk as medicine.')),
    ('cn-qing', T('清宫的奶与北京的「酪」', 'Qing palace dairy and Beijing lao'), T('清 · 1644–1911', 'Qing · 1644–1911'), T('一万只羊、两千多头牛，供着京城的奶。', 'Ten thousand sheep and 2,400 cattle supplied the capital.')),
    ('cn-yunnan', T('乳扇与乳饼', 'Rushan and rubing'), T('云南 · 大理与石林', 'Yunnan · Dali and Shilin'), T('中国少见的两种「真奶酪」。', 'Two rare “true cheeses” of China.')),
    ('mn', T('蒙古的「白食」', 'Mongolian “white foods”'), T('蒙古高原', 'Mongolian Plateau'), T('奶皮子、奶豆腐、奶干。', 'Milk skin, milk curd, dried curd.')),
    ('tibet', T('曲拉', 'Chura'), T('青藏高原与喜马拉雅', 'Tibetan Plateau and Himalaya'), T('打完酥油剩下的，晒成能嚼几小时的干酪。', 'What is left after churning, dried hard enough to chew for hours.')),
    ('jp-so', T('日本的「蘇」', 'So in ancient Japan'), T('奈良—平安', 'Nara–Heian'), T('牛乳一斗煎得蘇一升，作为贡品。', 'Ten parts milk boiled to one, sent as tribute.')),
    ('in-paneer', T('paneer 与 chhena', 'Paneer and chhena'), T('南亚', 'South Asia'), T('用酸点的鲜奶酪，来历有两说。', 'Acid-set fresh cheese, with two origin stories.')),
]

METHOD = T('研究分四路：沿革（考古与文献、东亚乳品、法规与名称之争）、工艺与风味（十步工序、十种奶酪的原产地规范、风味轮、搭配）、全球存奶法（二十三种做法与八条原理）、柜台导购（Whole Foods 与 Eataly、标签、旧金山的店）。数字优先取原产地规范（PDO / AOP / PGI）、美国联邦法规、学术论文与官方统计，其次是大学教材、行业协会与主要媒体；底稿里置信度「低」的事实一般不上正文。品鉴光谱的位置是按家族、熟成与含水量估计的；风味轮的结构来自 Bérodier 等（1997），具体词与化合物参考 Drake 等（2001）的切达词表，个别化合物为通行说法。柜台价格是 2026 年秋天按公开价与同级别零售价整理的区间，门店实价会变，以现场价签为准。页面写完后另做了一轮逐条核查。',
           'Research ran in four strands: history (archaeology and texts, East Asian dairy, law and the fight over names); craft and flavour (the ten steps, protected-origin specifications for ten cheeses, the flavour wheel, pairing); other ways to keep milk (twenty-three practices, eight principles); and the counter (Whole Foods and Eataly, labels, San Francisco shops). Figures come first from origin specifications (PDO / AOP / PGI), US federal regulations, papers and official statistics, then from university textbooks, trade bodies and major media; low-confidence facts were generally left out. Spectrum positions are estimates from family, age and moisture; the wheel follows Bérodier et al. (1997), with words and compounds from Drake et al. (2001), a few compounds being common attributions. Counter prices are autumn-2026 ranges from public prices and comparable retailers; trust the tag in the store. The finished page was checked line by line.')
