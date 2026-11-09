# -*- coding: utf-8 -*-
"""号外 · 奶酪 — 中英文案（中文为主稿；事实只取自 research/*.json，改事实先改底稿）"""
def T(zh, en, **kw): d = {'zh': zh, 'en': en}; d.update(kw); return d

META = dict(
    slug='cheese', date='2026-11-09',
    title_zh='酪：时间的手艺',
    title_en='Lao: The Craft of Time',
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

HERO_SUB = T('<b>一块奶酪，是一锅奶加上时间。</b>七千多年前，安纳托利亚的早期农人已在陶罐里加工奶，波兰的农人用带孔的陶滤器分离凝乳；今天，旧金山的柜台上摆着从帕尔马、汝拉到马林县的几百种轮子。这一期讲四件事：它怎么来的，它怎么做的，怎么尝，世界上别的地方怎么存奶——最后站到柜台前，看看怎么买。',
             '<b>A cheese is a pot of milk plus time.</b> More than seven thousand years ago, early farmers in Anatolia were already processing milk in clay pots, and farmers in Poland were separating curds in perforated clay sieves; today a San Francisco counter holds hundreds of wheels, from Parma and the Jura to Marin County. Four things here: where it came from, how it is made, how to taste it, and how the rest of the world keeps milk — and then, at the counter, how to buy.')

THESIS = dict(
    zh=[('奶', 0), ('会坏，', 0), ('奶酪', 1), ('不会——', 0), ('人类', 0), ('花了', 0), ('七千年，', 1), ('学会', 0), ('让', 0), ('时间', 1), ('替自己', 0), ('干活。', 0)],
    en=[('Milk', 0), ('spoils;', 0), ('cheese', 1), ('keeps.', 0), ('Seven', 1), ('thousand', 1), ('years', 0), ('of', 0), ('letting', 0), ('time', 1), ('do', 0), ('the', 0), ('work.', 0)],
    nums=[
        T('前 6500', '6500 BC', k=T('年前后，安纳托利亚西北部的陶器里已有乳脂残留——人类加工奶的最早化学证据之一（分不出是奶、酸奶还是奶酪）。', 'or so: milk fat in pottery from north-western Anatolia, among the earliest chemical evidence of dairying (it cannot tell milk from yoghurt or cheese).')),
        T('400 升', '400 L', k=T('奶做一只约 40 公斤的孔泰轮子。一户人家的奶不够，所以汝拉山区的村子八百多年来一直把奶凑到合作奶坊（fruitière）里一起做。', 'of milk make one 40 kg wheel of Comté — more than a single small farm could supply, which is why Jura villages have pooled milk in co-operative dairies (fruitières) for some eight hundred years.')),
        T('60 天', '60 days', k=T('在美国，用未经巴氏杀菌的生乳做的奶酪，必须在不低于 35°F（约 1.7°C）的温度下熟成至少 60 天才能卖。所以柜台上见不到生乳的新鲜奶酪。', 'is the US federal minimum: cheese from unpasteurised milk must be aged at least 60 days at 35 °F (about 1.7 °C) or warmer before sale — which is why no fresh raw-milk cheese reaches the counter.')),
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
             intro=T('内圈是九族气味，外圈是具体的词。点一格，看它常出现在哪种奶酪里、常与哪种化合物相关。结构取自欧洲研究项目的硬质与半硬质奶酪风味轮（Bérodier 等，1997），具体词与化合物参考了切达风味词表（Drake 等，2001）；「味觉与口感」一环是为了好用另加的。',
                     'The inner ring holds nine aroma families, the outer ring the words. Tap a cell to see which cheeses it turns up in and which compounds are associated with it. The structure follows the European wheel for hard and semi-hard cheeses (Bérodier et al., 1997), with words and compounds from a Cheddar lexicon (Drake et al., 2001); the “taste & mouthfeel” ring is an addition for practical use.'))
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
         text=T('科卢梅拉《论农业》（约公元 60–65 年）写下完整工艺：用羔羊或小山羊的凝乳酶，也可用野蓟花、红花籽或无花果树汁使奶凝结；沥乳清、压重物、撒盐晾干，压得紧实、充分干燥的奶酪「甚至可以运过海去」。老普林尼《自然史》（公元 77 年）开出名奶酪榜，卢纳奶酪一只重达一千罗马磅（约 330 公斤）。据《罗马帝王纪》，哈德良在军营里与士兵同吃腌肉、奶酪和掺水的酸酒。',
                'Columella’s <i>On Agriculture</i> (c. AD 60–65) gives a full method: set the milk with lamb or kid rennet, or with wild-thistle flowers, safflower seed or fig sap; drain, press, salt and dry — a firm, well-dried cheese “can even be shipped overseas.” Pliny’s <i>Natural History</i> (AD 77) ranks famous cheeses; one from Luna could weigh a thousand Roman pounds (about 330 kg). Hadrian, says the <i>Historia Augusta</i>, ate camp fare with his soldiers: bacon, cheese and sour wine.'),
         tags=[T('凝乳酶', 'Rennet'), T('罗马军粮', 'Army rations')], img='h-rome'),
    dict(id='qmys', label=T('533', '533'), yr=T('约 533–544', 'c. 533–544'), era=T('北魏 · 《齐民要术》', 'Northern Wei · Qimin Yaoshu'),
         title=T('酪、酥、醍醐与「干酪」', 'Lao, su, tihu — and “dry lao”'),
         text=T('中国古书里的乳品有几个基本字：「酪」近似发酵变稠的奶，「酥」近似黄油，「醍醐」是从酥里再提的精油。北魏贾思勰《齐民要术》卷六记有作酪、作干酪、抨酥等法，其中「干酪」是七八月间把酪放在日头下晒，表面结皮就撇下，反复撇到不再起皮；把撇得的约一斗在锅里略炒，摊盘晒到半干，捏成梨大的团再晒干，「得经数年不坏，以供远行」——中国古书里最接近硬质奶酪的记载之一。',
                'Classical Chinese has a few basic dairy words: <i>lao</i>, roughly thickened soured milk; <i>su</i>, roughly butter; <i>tihu</i>, an oil refined again from <i>su</i>. Jia Sixie’s <i>Qimin Yaoshu</i> (c. 533–544) gives methods for <i>lao</i>, “dry <i>lao</i>” and churned <i>su</i>. For dry <i>lao</i>, the skin that formed on <i>lao</i> set in the midday sun was skimmed off again and again until no more formed; the skimmings were briefly pan-fried, sun-dried until half dry, shaped into pear-sized balls and dried again — it “keeps for several years without spoiling, and serves for long journeys,” one of the closest things to a hard cheese in old Chinese texts.'),
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
         text=T('1925 年 7 月 26 日，法国立法保护罗克福尔的原产地名称——法国第一个受法律保护的奶酪产地名。1951 年欧洲多国签订斯特雷萨公约，把名字分成只能在原产地做的「原产地名称」，和别国按标准也能做的「典型名称」（所以 Camembert、Gouda 在许多国家都能做，受保护的是「Camembert de Normandie」「Gouda Holland」这样的全名）。1992 年欧共体建立 PDO / PGI 两级制度，1996 年公布首批名单。',
                'On 26 July 1925 France protected the name Roquefort by law — the country’s first legally protected cheese origin. The 1951 Stresa Convention split names into “appellations of origin”, made only in their place, and “typical names” anyone may make to a standard (which is why Camembert and Gouda can be made in many countries, while “Camembert de Normandie” and “Gouda Holland” are protected). In 1992 the EEC created the PDO and PGI tiers; the first list came out in 1996.'),
         tags=[T('AOC', 'AOC'), T('斯特雷萨', 'Stresa'), T('PDO / PGI', 'PDO / PGI')], img='h-aoc'),
    dict(id='artisan', label=T('1983', '1983'), yr=T('1983 – 今天', '1983 – today'), era=T('手工复兴', 'The artisan revival'),
         title=T('从康奈尔到马林县', 'From Cornell to Marin'),
         text=T('1983 年，康奈尔大学的 Frank Kosikowski 创立美国奶酪协会，把散落各地的小作坊连起来。湾区北部是这场复兴的重镇：佩塔卢马的 Marin French Cheese 自称美国连续经营最久的奶酪厂（1865）；Laura Chenel 1979 年在索诺玛开始做山羊奶酪（品牌以此为创立年）；Cowgirl Creamery 1997 年在雷斯岬站开张；Point Reyes 农场 2000 年推出蓝纹 Original Blue。另一头，2024 年全美奶酪产量约 142 亿磅（不含茅屋奶酪），威斯康星第一、加州第二。',
                'In 1983 Frank Kosikowski of Cornell founded the American Cheese Society to link scattered small makers. The North Bay became a centre of the revival: Petaluma’s Marin French Cheese calls itself America’s longest continuously operating cheese company (1865); Laura Chenel began making goat cheese in Sonoma in 1979, the year her company counts as its founding; Cowgirl Creamery opened in Point Reyes Station in 1997; and Point Reyes Farmstead launched Original Blue in 2000. At the other end of the scale, the US made about 14.2 billion lb of cheese in 2024 (excluding cottage cheese) — Wisconsin first, California second.'),
         tags=[T('Mt Tam', 'Mt Tam'), T('Original Blue', 'Original Blue'), T('Dry Jack', 'Dry Jack')], img='h-artisan'),
]

ASIA_HEAD = T('东边的酪、酥与奶片', 'Lao, su and milk fans in the East')
ASIA_NOTE = T('乳品在东亚不只是「舶来品」。下面是中国、蒙古、西藏、日本和印度的几条线索，点开看。', 'Dairy in Asia is not only an import. A few threads from China, Mongolia, Tibet, Japan and India — tap to open.')
ASIA_ITEMS = [
    ('cn-laonu', T('「酪奴」', '“Slave to lao”'), T('北魏 · 茶与酪孰优', 'Northern Wei · tea versus lao'), T('王肃一句玩笑，让茶在北魏得了个外号。', 'A joke by Wang Su gave tea a nickname in the Northern Wei.')),
    ('cn-tihu', T('醍醐灌顶', 'Tihu poured on the crown'), T('佛经 · 乳的五个阶段', 'Buddhist sutra · five stages of milk'), T('从乳到醍醐的五个阶段，成了一个成语。', 'Five stages of refining milk became an idiom.')),
    ('cn-tang', T('唐代的酥山', 'Tang “butter mountains”'), T('唐 · 宫廷与城市', 'Tang · court and city'), T('冻起来当甜点的酥，和当药用的奶。', 'Frozen su desserts, and milk as medicine.')),
    ('cn-qing', T('清宫的奶与北京的「酪」', 'Qing palace dairy and Beijing lao'), T('清 · 1644–1911', 'Qing · 1644–1911'), T('一万只羊、两千多头牛，供着京城的奶。', 'Ten thousand sheep and 2,400 cattle supplied the capital.')),
    ('cn-yunnan', T('乳扇与乳饼', 'Rushan and rubing'), T('云南 · 大理与石林', 'Yunnan · Dali and Shilin'), T('中国少见的两种「真奶酪」。', 'Two rare “true cheeses” of China.')),
    ('mn', T('蒙古的「白食」', 'Mongolian “white foods”'), T('蒙古高原', 'Mongolian Plateau'), T('奶皮子、奶豆腐、奶干。', 'Milk skin, milk curd, dried curd.')),
    ('tibet', T('曲拉', 'Chura'), T('青藏高原与喜马拉雅', 'Tibetan Plateau and Himalaya'), T('打完酥油剩下的酪乳，晒成碎粒干酪；喜马拉雅的硬 chhurpi 能含上几个小时。', 'Buttermilk left from churning, dried into crumbly curd; Himalayan hard chhurpi can be sucked for hours.')),
    ('jp-so', T('日本的「蘇」', 'So in ancient Japan'), T('奈良—平安', 'Nara–Heian'), T('牛乳一斗煎得蘇一升，作为贡品。', 'Ten parts milk boiled to one, sent as tribute.')),
    ('in-paneer', T('paneer 与 chhena', 'Paneer and chhena'), T('南亚', 'South Asia'), T('用酸点的鲜奶酪，来历有两说。', 'Acid-set fresh cheese, with two origin stories.')),
]

METHOD = T('研究分四路：沿革（考古与文献、东亚乳品、法规与名称之争）、工艺与风味（十步工序、十种奶酪的原产地规范、风味轮、搭配）、全球存奶法（二十三种做法与八条原理）、柜台导购（Whole Foods 与 Eataly、标签、旧金山的店）。数字优先取原产地规范（PDO / AOP / PGI）、美国联邦法规、学术论文与官方统计，其次是大学教材、行业协会与主要媒体；底稿里置信度「低」的事实一般不上正文。品鉴光谱的位置是按家族、熟成与含水量估计的；风味轮的结构来自 Bérodier 等（1997），具体词与化合物参考 Drake 等（2001）的切达词表，个别化合物为通行说法。柜台价格是 2026 年秋天按公开价与同级别零售价整理的区间，门店实价会变，以现场价签为准。页面写完后另做了一轮逐条核查。',
           'Research ran in four strands: history (archaeology and texts, East Asian dairy, law and the fight over names); craft and flavour (the ten steps, protected-origin specifications for ten cheeses, the flavour wheel, pairing); other ways to keep milk (twenty-three practices, eight principles); and the counter (Whole Foods and Eataly, labels, San Francisco shops). Figures come first from origin specifications (PDO / AOP / PGI), US federal regulations, papers and official statistics, then from university textbooks, trade bodies and major media; low-confidence facts were generally left out. Spectrum positions are estimates from family, age and moisture; the wheel follows Bérodier et al. (1997), with words and compounds from Drake et al. (2001), a few compounds being common attributions. Counter prices are autumn-2026 ranges from public prices and comparable retailers; trust the tag in the store. The finished page was checked line by line.')

# ---------- 04 柜台 ----------
CH['counter'] = dict(no='04 · COUNTER', h=T('站到奶酪柜前', 'At the cheese counter'),
    lede=T('全食、Eataly 这类奶酪集中的专柜，第一次站过去容易发懵：几十块奶酪、一排看不懂的缩写、柜台后面还站着一位等你开口的人。其实柜子分几个区，价签上就那么几个词，要一片尝尝是再平常不过的事。下面从柜子里有什么、价签怎么读、怎么开口、怎么配一盘、拿回家怎么放，一路走到从 Daisy 家出发能去哪儿买。',
           'A dedicated cheese counter — Whole Foods, Eataly and the like — can be bewildering the first time: dozens of cheeses, a row of abbreviations, and someone behind the glass waiting for you to speak. In fact the case falls into a few zones, a tag uses only a handful of words, and asking for a taste is the most normal thing in the world. Below: what is in the case, how to read a tag, what to say, how to build a board, how to keep it at home — and where to go from Daisy’s place.'))

CASE_HEAD = T('柜子里有什么', 'What’s in the case')
CASE_NOTE = T('点一个区，看这一区常见的几种奶酪一磅大概多少钱；再点一条，看它什么味道、配什么。价格是 2026 年秋天按公开价和同级别零售价整理的区间，以店里的价签为准。',
              'Pick a zone to see what its usual cheeses cost per pound; tap a bar for taste and pairings. Prices are autumn-2026 ranges from public and comparable retail prices — the tag in the store wins.')
ZONE_SHORT = {'fresh': T('新鲜 · 拉伸 · 盐水', 'Fresh · stretched · brined'), 'bloomy': T('白霉皮', 'Bloomy rind'), 'washed': T('洗皮', 'Washed rind'), 'alpine': T('阿尔卑斯式', 'Alpine'),
              'hard': T('硬质 · 刨丝', 'Hard · grating'), 'blue': T('蓝纹', 'Blue'), 'american': T('加州与美国手工', 'California & US artisan')}

TAG_HEAD = T('读一张价签', 'Read a tag')
TAG_NOTE = T('价签上的每个词都有讲究。换一张，点亮起来的词。这几张是按常见写法排的示例，不是哪家店的实价。', 'Every word on a tag means something. Switch tags and tap the highlighted words. These are typical examples, not real prices from any store.')
GLOSS = {  # 词 → (来源, id, 标题)
    'pdo': ('D', 'pdo', T('DOP · AOP · PDO', 'DOP · AOP · PDO')), 'pgi': ('D', 'pgi', T('IGP · PGI', 'IGP · PGI')), 'swiss': ('D', 'swiss-aop', T('瑞士 AOP', 'Swiss AOP')),
    'raw': ('D', 'raw-60', T('生乳（raw milk）', 'Raw milk')), 'past': ('D', 'raw-practical', T('为什么软的多是巴氏杀菌', 'Why soft cheeses are pasteurized')),
    'parmesan': ('D', 'parmesan-name', T('Parmesan 不等于 Parmigiano Reggiano', 'Parmesan is not Parmigiano Reggiano')), 'pr': ('D', 'parm-rind-read', T('认针点字皮', 'Find the pin-dot rind')),
    'months': ('D', 'aging-marks', T('熟成月数', 'Months of age')), 'gruyere-us': ('A', 'gruyere', T('美国产的「Gruyère」', '“Gruyère” made in America')),
    'american': ('A', 'american', T('American cheese 到底是什么', 'What “American cheese” is')), 'typical': ('A', 'stresa-typical', T('有的名字谁都能用', 'Names anyone may use')),
    'milk': ('D', 'label-milk', T('奶源写在哪', 'Where the milk is named')), 'rind': ('D', 'rind', T('皮能不能吃', 'Can you eat the rind?')),
    'lb': ('B', 'cut-to-order', T('按磅卖，按需切', 'Priced by the pound, cut to order')),
}
TAGS = [  # (id, 标签名, [(词, gloss 键或 None)], 价格行)
    ('parm', T('帕玛森', 'Parmigiano'), [('Parmigiano Reggiano', 'pr'), ('DOP', 'pdo'), ('24 months', 'months'), ("raw cow's milk", 'raw'), ('Emilia-Romagna, Italy', None)], '$29.99 / lb'),
    ('parmesan', T('美国 Parmesan', 'US Parmesan'), [('Parmesan', 'parmesan'), ('Wisconsin', None), ("pasteurized cow's milk", 'past'), ('aged 10 months', None)], '$15.99 / lb'),
    ('gruyere', T('瑞士格吕耶尔', 'Swiss Gruyère'), [('Le Gruyère', None), ('AOP', 'swiss'), ('Switzerland', None), ("raw cow's milk", 'raw')], '$31.99 / lb'),
    ('gruyere-us', T('美国 Gruyère', 'US Gruyère'), [('Gruyère', 'gruyere-us'), ('Wisconsin', None), ("cow's milk", None)], '$19.99 / lb'),
    ('gruyere-fr', T('法国 Gruyère', 'French Gruyère'), [('Gruyère', None), ('IGP', 'pgi'), ('France', None)], '$24.99 / lb'),
    ('humboldt', T('洪堡雾', 'Humboldt Fog'), [('Humboldt Fog', None), ('California', None), ("pasteurized goat's milk", 'milk'), ('bloomy rind', 'rind')], '$32.99 / lb'),
    ('camembert', T('卡芒贝尔', 'Camembert'), [('Camembert', 'typical'), ('France', None), ('pasteurized', 'past')], '$9.99 / 8 oz'),
    ('american', T('American', 'American'), [('American', None), ('pasteurized process cheese', 'american')], '$6.99 / lb'),
]

ASK_HEAD = T('开口要一片', 'Ask for a slice')
ASK_NOTE = T('柜台后面的人就是来帮你挑的。这十句够用了——点一张翻过来看意思。', 'The person behind the counter is there to help you choose. These ten lines are enough — tap a card to flip it.')

BOARD_HEAD = T('配一盘', 'Build a board')
BOARD_NOTE = T('选预算和人数，份量按比例算；钱数按每磅价格区间估算，只算奶酪。三盘都用全食常见的品种，每盘至少一种加州奶酪，当天有没有货以店里为准。', 'Pick a budget and a head count; portions scale with it. Cost is estimated from the per-pound ranges and covers cheese only. All three use cheeses Whole Foods commonly stocks, each with at least one Californian; what is in on the day is up to the store.')
BOARD_CHECKS = [('milk', T('奶源', 'Milks')), ('fam', T('类型', 'Styles')), ('ca', T('加州', 'California'))]

PATH_HEAD = T('从柜台到餐桌', 'From counter to table')
PATH = [
    ('plan', T('出门前', 'Before you go'), [('buying', 'say-use', T('先想好三件事', 'Three things to decide')), ('buying', 'count', T('买几种', 'How many')), ('buying', 'portion', T('买多少', 'How much')), ('buying', 'variety', T('怎么搭', 'How to mix'))]),
    ('counter', T('在柜台', 'At the counter'), [('buying', 'ask-taste', T('一定要尝', 'Always taste')), ('buying', 'cut-to-order', T('现切还是预切', 'Cut to order or pre-cut')), ('buying', 'check-face', T('看切面', 'Check the cut face')),
                                              ('buying', 'parm-piece', T('帕玛森要带皮', 'Parmigiano with rind')), ('buying', 'blue-small', T('蓝纹买小块', 'Buy blue small'))]),
    ('home', T('拿回家', 'Getting home'), [('storage', 'wrap', T('怎么包', 'Wrapping')), ('storage', 'where', T('放哪', 'Where')), ('storage', 'fresh', T('新鲜奶酪', 'Fresh cheese')), ('storage', 'soft-flip', T('软质翻面', 'Turn soft cheese'))]),
    ('serve', T('上桌', 'Serving'), [('buying', 'temp', T('先回温', 'Let it warm up')), ('buying', 'cut-shape', T('怎么切', 'How to cut'))]),
    ('later', T('剩下的', 'Leftovers'), [('storage', 'how-long', T('能放多久', 'How long')), ('storage', 'mold', T('长了霉', 'If it moulds')), ('storage', 'freeze', T('冷冻', 'Freezing')), ('storage', 'rind-save', T('留皮煮汤', 'Save the rind'))]),
    ('save', T('省钱', 'Saving'), [('buying', 'buy-small', T('临吃再买', 'Buy close to eating')), ('buying', 'deal-12days', T('12 月打折', 'December deals'))]),
]
SHELF = [(T('硬质、半硬（帕玛森、切达、高达、格吕耶尔）', 'Hard & semi-hard (Parmigiano, cheddar, Gouda, Gruyère)'), 21, 28), (T('软质与新鲜（布里、马苏里拉、山羊奶酪、里科塔）', 'Soft & fresh (Brie, mozzarella, chèvre, ricotta)'), 5, 7)]
SHELF_HEAD = T('开封后大概能放几天', 'Roughly how many days after opening')

WHERE_HEAD = T('从 Daisy 家出发', 'Starting from Daisy’s')
WHERE_NOTE = T('圆心是 Daisy 家。方向按地址大致摆，远近按非高峰时段的路程估；最外一圈的 Eataly 在一小时外，图上压缩了。营业时间出发前看店家官网。Cowgirl Creamery 渡轮大厦的店 2021 年已经关了。',
               'Daisy’s place is at the centre. Directions follow the addresses roughly; distance is off-peak travel time. Eataly, on the outer ring, is an hour away and drawn closer than it is. Check opening hours before you go. Cowgirl Creamery’s Ferry Building shop closed in 2021.')
HOME = (37.7245, -122.4520)
PLACES = {  # id: (分钟, 纬度, 经度)
    'wf-ocean': (7, 37.7233, -122.4560), 'cheese-boutique': (7, 37.7337, -122.4337), 'wf-stonestown': (8, 37.7282, -122.4772), 'wf-noe': (12, 37.7515, -122.4318),
    '24th-street-cheese': (12, 37.7518, -122.4300), 'say-cheese': (15, 37.7662, -122.4503), 'wf-stanyan-market': (15, 37.7690, -122.4530), 'bi-rite': (15, 37.7617, -122.4256),
    'rainbow': (18, 37.7695, -122.4153), 'la-fromagerie': (20, 37.7590, -122.3880), 'cheese-school': (23, 37.8058, -122.4224), 'cheese-plus': (25, 37.7945, -122.4215),
    'ferry-plaza': (25, 37.7955, -122.3937), 'eataly-sv-trip': (55, 37.3249, -121.9466),
}
LOCAL_KINDS = [('wholefoods', T('全食超市', 'Whole Foods')), ('shop', T('奶酪店', 'Cheese shop')), ('market', T('市场与超市', 'Market & grocer')), ('class', T('学', 'Learn')), ('trip', T('周末专程', 'Weekend trip'))]
ADDR = {'cheese-boutique': T('Glen Park', 'Glen Park'), 'la-fromagerie': T('Dogpatch · 3rd St', 'Dogpatch · 3rd St'),
        'cheese-school': T('地址与课表以官网为准（Ghirardelli Square 或 Dogpatch）', 'Check the website for the current address and classes (Ghirardelli Square or Dogpatch)'),
        'eataly-sv-trip': T('2855 Stevens Creek Blvd., Santa Clara（Westfield Valley Fair 商场）', '2855 Stevens Creek Blvd., Santa Clara (Westfield Valley Fair)')}
PLACE_MORE = {
    'wf-ocean': [
        T('全食的奶酪部大量配备美国奶酪协会认证的奶酪师（CCP）：2024 年它在全球 1,000 多名 CCP 中占 370 多名，目标是每家店至少一名。Ocean Ave 店的门店页列着这项服务，在岗时间要问门店，专程去可以先打电话。', 'Whole Foods staffs its cheese departments with American Cheese Society Certified Cheese Professionals — 370-plus of the world’s 1,000-plus in 2024, aiming for one per store. The Ocean Ave store lists the service; call ahead to check hours.'),
        T('CCP 按你要的重量或厚度现切，会主动请你尝没吃过的；帕玛森整轮在店里开，用的是 24 个月的轮子。自有品牌 365 的预切块在自选冷柜里，比现切便宜。', 'CCPs cut to the weight or thickness you ask for and offer tastes; Parmigiano is cracked in-store from 24-month wheels. Pre-cut 365-brand pieces in the self-serve case cost less.'),
        T('每年 12 月中旬有「12 Days of Cheese」：2025 年是 12 月 13–24 日，一批精选奶酪 12 天里一直打折（Prime 会员 7 折，非会员 78 折）。', '“12 Days of Cheese” runs in mid-December: in 2025, Dec 13–24, a curated set was 30% off with Prime and 22% off without for all twelve days.'),
    ],
    'eataly-sv-trip': [
        T('旧金山市内没有 Eataly。硅谷店 2022 年 6 月开业，三层，在 Westfield Valley Fair 商场里。', 'There is no Eataly in San Francisco. The Silicon Valley store opened in June 2022 on three floors of Westfield Valley Fair.'),
        T('奶酪和熟肉合成一个「Salumi e Formaggi」现切柜台，营业 8:30–21:00，有多个年份的帕玛森；店员鼓励先尝再买。mozzarella 每天在店里现做，可以看师傅拉伸凝乳。', 'Cheese and cured meats share the “Salumi e Formaggi” counter (8:30–21:00) with Parmigiano at several ages; staff encourage tasting first. Mozzarella is made in-store daily — you can watch it being stretched.'),
        T('店里的烹饪学校 La Scuola 开过「Hands-On: Mozzarella」实操课（最近一期在 2026 年 7 月），两小时，跟主厨一起做。', 'The in-store La Scuola cooking school has run two-hour “Hands-On: Mozzarella” classes with a chef, most recently in July 2026.'),
    ],
}

PRIN_TITLES = [T('强度匹配', 'Match intensity'), T('脂肪对单宁', 'Fat versus tannin'), T('甜配咸、配冲', 'Sweet with salty or funky'), T('气泡与酸度清口', 'Bubbles and acid cleanse'),
               T('同乡搭配', 'Grows together, goes together'), T('找桥，或找反差', 'Bridge or contrast'), T('奶酪会「压」红酒', 'Cheese mutes red wine'), T('拿不准时', 'When in doubt')]
TASTE_TITLES = [T('提前回温', 'Temper first'), T('适饮温度', 'Serving temperature'), T('从淡到浓', 'Mild to strong'), T('看、摸、闻、尝', 'Look, touch, smell, taste'),
                T('记下来', 'Take notes'), T('份量', 'Portions'), T('清口', 'Cleanse'), T('外皮与刀具', 'Rinds and tools')]

PENDING = [
    T('《齐民要术》作干酪法、《洛阳伽蓝记》「酪奴」与《涅槃经》五味的引文与通行校本一致，但这次没能在线打开全文逐字核对。', 'The quotations from the Qimin Yaoshu, the Luoyang Qielan Ji and the Nirvana Sutra match standard editions but could not be re-read in full online.'),
    T('菲达约 18°C 的预熟成取自 PDO 摘要的转述，希腊原文规范没有打开。', 'Feta’s ~18 °C pre-ripening comes from a summary of the PDO; the Greek specification itself was not opened.'),
    T('The Cheese School of San Francisco 2026 年的地址与课表、Glen Park 的 Cheese Boutique 与 Dogpatch 的 La Fromagerie 的门牌，只有导览文章为据，出发前请看店家官网。', 'The Cheese School of San Francisco’s 2026 address and schedule, and the street numbers of Cheese Boutique (Glen Park) and La Fromagerie (Dogpatch), rest on guide articles only — check before you go.'),
    T('柜台价格是按公开价和同级别零售价整理的区间，全食与 Eataly 的门店实价没法在线取得。', 'Counter prices are ranges from public and comparable retail prices; in-store prices at Whole Foods and Eataly could not be read online.'),
]
