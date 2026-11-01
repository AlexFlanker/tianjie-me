# -*- coding: utf-8 -*-
"""号外 · 半岛的烤肉 — 中英文案（中文为主稿；事实只取自 research/*.json，改事实先改底稿）"""
def T(zh, en, **kw): d = {'zh': zh, 'en': en}; d.update(kw); return d

META = dict(
    slug='peninsula-bbq', date='2026-10-31',
    title_zh='半岛的烤肉：从貊炙到韩国城',
    title_en='Peninsula Barbecue: From Maekjeok to Koreatown',
    sub_zh='一千七百年的火、一头韩牛的分割、一张桌子的出海——南北两边都算上。',
    sub_en='Seventeen centuries of fire, one Hanwoo carcass, and a table that went abroad — North and South both.',
    desc='朝鲜半岛烤肉文化的号外专题：从《搜神记》的貊炙讲到首尔与平壤的烤肉桌，韩牛怎样靠分级、溯源与营销在本国守住高端市场，韩式烤肉怎样在美国与中国扩张。中英双语。',
)

HERO = dict(
    kick=T('号外 · 给 Joe', 'Extra · for Joe'),
    h1=T('FIRE.<br>CUT.<br>TABLE.', 'FIRE.<br>CUT.<br>TABLE.'),
    sub=T('<b>半岛的烤肉。</b>火：一千七百年前中原贵族就在学「貊炙」；刀：一头韩牛分成十个大块、几十个小块，每块有自己的火候；桌：桌边自烤、剪刀、生菜包，这一套从首尔、平壤一路端到洛杉矶和北京。',
          '<b>Barbecue on the Korean Peninsula.</b> Fire: 1,700 years ago China’s elite were already copying the “Maek roast.” Cut: a Hanwoo carcass is split into ten primals and dozens of sub-cuts, each with its own heat. Table: grill-it-yourself, scissors and lettuce wraps — a format carried from Seoul and Pyongyang to Los Angeles and Beijing.'),
    cta=T('先看火 ↓', 'Start with the fire ↓'),
)

THESIS = dict(
    zh=[('韩牛', 1), ('守住了', 0), ('本国的', 0), ('高端餐桌，', 0), ('韩烤', 1), ('端上了', 0), ('世界的', 0), ('餐桌。', 0)],
    en=[('Hanwoo', 1), ('held', 0), ('the', 0), ('top', 0), ('of', 0), ('the', 0), ('home', 0), ('table.', 0), ('Korean', 1), ('barbecue', 1), ('set', 0), ('the', 0), ("world's.", 0)],
    nums=[
        T('5', '5', k=T('个地方买得到出口的韩牛：香港、马来西亚、柬埔寨、老挝、阿联酋（据 2025 年 10 月的报道；也有报道列入澳门、蒙古）。美国、中国都不在内。', 'places buy exported Hanwoo: Hong Kong, Malaysia, Cambodia, Laos and the UAE (as reported in Oct 2025; some reports also list Macau and Mongolia). Neither the US nor China.')),
        T('$208M', '$208M', k=T('GEN Korean BBQ 2024 年的营收（43 家店；2011 年从加州塔斯廷起家，2023 年纳斯达克上市）。', 'GEN Korean BBQ revenue in 2024 (43 restaurants; started in Tustin, California in 2011, listed on Nasdaq in 2023).')),
        T('$13.6B', '$13.6B', k=T('2025 年韩国「K-Food+」（农食品加农机、兽药等相关产业）出口额，创新高；其中农食品 104.1 亿美元，美国 18 亿美元居首，中国 15.8 亿美元第二。', 'K-Food+ exports in 2025 (agrifood plus related industries such as farm machinery), a record. Of the $10.41B in agrifood, the US ($1.8B) was first and China ($1.58B) second.')),
    ],
)

NAV = [('fire', 'FIRE', T('火', 'Fire')), ('cut', 'CUT', T('刀', 'Cut')), ('table', 'TABLE', T('桌', 'Table')), ('world', 'WORLD', T('出海', 'Abroad')), ('end', 'END', T('卷末', 'Notes'))]

CH = {
    'fire': dict(big='FIRE<i>.</i>', h=T('一千七百年的火', 'Seventeen centuries of fire'),
                 lede=T('半岛人吃烤肉的历史，是一部「能不能吃到肉」的历史：佛教戒杀、耕牛稀缺与牛禁一再让肉难上餐桌，蒙古人、两班的暖炉会、平壤的松林、首尔的蜂窝煤又一次次把火点回来。1945 年以后，同一种吃法在南北两边走上了两条路。拖底部的刻度尺，或者直接往下滚。',
                        'On the peninsula, the history of barbecue is a history of whether you could get meat at all. Buddhist strictures, scarce oxen and cattle bans kept meat scarce; Mongols, Joseon scholars’ brazier parties, Pyongyang’s pine groves and Seoul’s coal briquettes kept lighting the fire again. After 1945 the same way of eating went two ways, North and South. Drag the ruler at the bottom, or just scroll.')),
    'cut': dict(big='CUT<i>.</i>', h=T('一头韩牛，怎样被分开、怎样被卖贵', 'One Hanwoo: how it is cut, and how it is sold dear'),
                lede=T('', '')),
    'table': dict(big='TABLE<i>.</i>', h=T('一张桌子：南边与北边', 'One table, North and South'),
                  lede=T('真正走出半岛的，不是哪一块肉，而是一张桌子的规矩：火在桌子中间，肉由你自己翻，剪刀代替刀，生菜代替盘子，小菜吃完通常还会再上。平壤的烤鸭肉餐厅，流程几乎一模一样。',
                         'What left the peninsula was not a cut of meat but the rules of a table: fire in the middle, you turn the meat, scissors instead of knives, lettuce instead of plates, side dishes that usually come back. Pyongyang’s duck-barbecue restaurants run almost the same script.')),
    'world': dict(big='WORLD<i>.</i>', h=T('出海：美国与中国', 'Abroad: America and China'),
                  lede=T('同一张桌子，在韩国餐饮企业的两个最大海外市场走出了相反的曲线：美国从移民社区的食堂一路做到纳斯达克上市；中国从 1992 年建交后的第一代连锁（汉阳馆、汉拿山）做到上百家门店，2017 年萨德之后韩国招牌遇冷，到 2020 年代，韩式成了中国烤肉的三大赛道之一。拖动年份，看节点一个个亮起来。',
                         'The same table traced opposite curves in the two biggest foreign markets for Korean restaurant brands. In America it went from immigrant canteen to a Nasdaq listing; in China from the first post-1992 chains (Hanyangguan, Hannashan) to hundreds of outlets — then, after THAAD in 2017, the Korean label cooled, and by the 2020s Korean-style had become one of the three lanes of Chinese barbecue. Drag the year and watch the map light up.')),
}

# ---------- 00 FIRE 舞台：lane = both / south / north；y 用于南北切换时找最近一步 ----------
STAGE = [
    dict(id='maek', y=270, lane='both', label='c.270', yr=T('约 270', 'c. 270'), era=T('史前至三国 · 貊炙', 'Antiquity to the Three Kingdoms · Maekjeok'),
         title=T('中原人学「貊炙」', 'China copies the “Maek roast”'),
         text=T('东晋干宝《搜神记》记西晋泰始年间（265–274）以来，中原贵族竞相吃「羌煮、貊炙」——干宝称之为「翟之食」。东汉《释名》说貊炙是整只烤熟、各人用刀割着吃。「貊」是不是高句丽、扶余的先人，学界两说。',
                'Gan Bao’s <i>Soushen Ji</i> records that from the Taishi era (265–274) Chinese nobles vied to eat “Qiang stew and Maek roast” — foods of the barbarians, as Gan Bao put it. The Han-era <i>Shiming</i> says Maek roast was a whole animal, carved by each diner with his own knife. Whether the “Maek” were ancestors of Goguryeo and Buyeo is still debated.'),
         dishes=[T('貊炙', 'Maekjeok', ko='맥적')], img='h-maek'),
    dict(id='goryeo', y=1123, lane='both', label='1123', yr=T('1123', '1123'), era=T('高丽 · 崇佛少肉', 'Goryeo · Buddhist restraint'),
         title=T('只有王与宰相才吃羊、猪', 'Only the king and ministers ate mutton and pork'),
         text=T('北宋使臣徐兢 1123 年出使高丽，在《宣和奉使高丽图经》里写：高丽人好佛戒杀，只有王与宰相吃羊、猪；宰杀时把牲畜捆起投进火里，肉有腥味。另一种看法是：牛是耕畜、肉源稀少，才是根本原因。',
                'Xu Jing, a Song envoy to Goryeo in 1123, wrote that Koreans loved the Buddha and shunned killing: only the king and ministers ate mutton or pork, and animals were bound and thrown into fire. Another view: cattle were plough animals and meat was scarce — that, not faith, was the real limit.'),
         dishes=[], img='h-goryeo'),
    dict(id='yuan', y=1300, lane='both', label='13–14C', yr=T('13–14 世纪', '13th–14th c.'), era=T('元干涉期 · 肉食回流', 'Mongol period · meat returns'),
         title=T('蒙古人把火点回来', 'The Mongols relight the fire'),
         text=T('蒙古入侵与元干涉期，被普遍看作半岛肉食复兴的外因：济州设了养马牛的牧场，屠宰与吃肉的习惯随之传入。通说认为高丽后期出现「雪夜觅」（文字记录最早见于 1609 年的朝鲜仪轨），被视为貊炙的复归；反向的，高丽的生菜包饭也被带到大都，称「高丽样」。',
                'The Mongol invasions and Yuan overlordship are usually seen as the outside push behind meat’s comeback: ranches on Jeju, butchery and meat-eating came with them. Food historians date the “snowy-night roast” (seoryamyeok) to late Goryeo — though its first written record is a 1609 Joseon court text — and read it as Maekjeok’s return. In the other direction, Goryeo’s lettuce-wrapped rice reached the Yuan capital as “the Goryeo style.”'),
         dishes=[T('雪夜觅', 'Seoryamyeok', ko='설야멱'), T('生菜包', 'Ssam', ko='쌈')], img='h-ssam'),
    dict(id='joseon', y=1700, lane='both', label='1398–1849', yr=T('1398–1849', '1398–1849'), era=T('朝鲜王朝 · 牛禁与暖炉会', 'Joseon · cattle ban, brazier parties'),
         title=T('禁宰耕牛，照样围炉烤肉', 'A ban on killing oxen — and grilling anyway'),
         text=T('1398 年起朝鲜一再颁布「牛禁令」，盗牛而宰者可处绞刑；可据 1775 年的记录，单是节日就宰牛两三万头。十月初一起，两班流行「暖炉会」：炭火炉上放铁板，牛肉用油、酱、葱、蒜调味后围炉烤着吃（《东国岁时记》1849）。',
                'From 1398 Joseon repeatedly banned slaughtering oxen — stealing and killing one could mean hanging — yet a 1775 record counts 20,000–30,000 cattle killed for festivals alone. From the first day of the tenth month, yangban held “brazier parties”: an iron plate over charcoal, beef seasoned with oil, soy, scallion and garlic, grilled around the fire (<i>Dongguk Sesigi</i>, 1849).'),
         dishes=[T('宽片烤牛肉', 'Neobiani', ko='너비아니'), T('雪夜觅', 'Seoryamyeok', ko='설야멱')], img='h-joseon'),
    dict(id='pyongyang35', y=1935, lane='both', label='1935', yr=T('1935', '1935'), era=T('日据时期 · 「불고기」登场', 'Colonial era · “bulgogi” appears'),
         title=T('平壤牡丹台的松林烤肉', 'Barbecue in Pyongyang’s pine groves'),
         text=T('「불고기」（火 + 肉）一词 1930 年代初才见于报刊。1935 年 5 月，《东亚日报》平壤电：以烟熏伤松为由，禁止在牡丹台松林里露天烤肉——说明那时平壤烤肉已是名物。语言学家多认为这个词原是平安道方言；另一说认为是日语「焼肉」的译词。',
                'The word bulgogi (“fire meat”) first shows up in print in the early 1930s. In May 1935 the <i>Dong-a Ilbo</i> reported from Pyongyang that open-air grilling in the Moranbong pine grove was banned for smoking the trees — so Pyongyang barbecue was already famous. Most linguists see the word as Pyeongan dialect; a minority reads it as a translation of Japanese yakiniku.'),
         dishes=[T('平壤烤肉', 'Pyongyang bulgogi', ko='평양 불고기'), T('平壤冷面', 'Pyongyang naengmyeon', ko='평양냉면')], img='h-bulgogi'),
    # ---- 南 ----
    dict(id='suwon', y=1956, lane='south', label='1956', yr=T('1956', '1956'), era=T('南 · 战后', 'South · postwar'),
         title=T('水原갈비与麻浦猪排骨', 'Suwon galbi, Mapo pork ribs'),
         text=T('水原「华春屋」1945 年开业，1956 年起卖炭火烤牛排骨，盐调味、大块，人称「水原王갈비」；1985 年水原市把它定为乡土饮食。同年代，首尔麻浦出现面向工人的猪排骨、猪皮烤肉店，多用蜂窝煤炉。',
                'Suwon’s Hwachun-ok opened in 1945 and began serving charcoal-grilled beef short ribs in 1956 — salt-seasoned, huge, the “king galbi”; the city named it a local specialty in 1985. In the same years Seoul’s Mapo district filled with pork-rib and pork-skin grills for workers, mostly over coal briquettes.'),
         dishes=[T('水原排骨', 'Suwon galbi', ko='수원갈비'), T('猪排骨', 'Pork galbi', ko='돼지갈비')], img='galbi'),
    dict(id='dome', y=1970, lane='south', label='1960s–90s', yr=T('1960–90 年代', '1960s–90s'), era=T('南 · 穹顶汤盘', 'South · the dome pan'),
         title=T('中间隆起、四周有汤槽的烤盘', 'The domed pan with a moat'),
         text=T('这几十年首尔流行一种烤盘：中间隆起、布满孔、四周一圈汤槽。腌牛肉在穹顶上烤，汁水流进槽里成甜汤，最后把饭拌进去——「肉汤불고기」。在此之前是铁丝网上的直火烤。',
                'For decades Seoul grilled on a domed, perforated pan ringed by a moat: marinated beef cooked on the dome, its juices ran into the moat as a sweet broth, and rice was stirred in at the end — “broth bulgogi.” Before that it was direct heat on a wire grill.'),
         dishes=[T('肉汤烤肉', 'Broth bulgogi', ko='육수 불고기')], img='bulgogi-pan'),
    dict(id='samgyeop', y=1983, lane='south', label='1983', yr=T('1983', '1983'), era=T('南 · 五花肉共和国', 'South · pork-belly republic'),
         title=T('「三角洞的五花肉胡同」', '“Samgyeopsal Alley”'),
         text=T('烤五花肉专门店在 1970 年代后期出现，1983 年报纸已称首尔三角洞为「삼겹살胡同」。矿工洗煤尘、石板瓦上烤这些起源故事都没有确证；较可靠的解释是结构性的：政府为压牛价鼓励吃猪肉，养猪业现代化，1980 年代中期便携燃气炉普及。',
                'Pork-belly grill houses appear in the late 1970s; by 1983 a newspaper called Seoul’s Samgak-dong “Samgyeopsal Alley.” The origin stories — miners washing coal dust from their throats, belly grilled on slate roof tiles — are unproven. The better-supported explanation is structural: cheap pork pushed by policy to hold down beef prices, modern pig farming, and portable gas stoves in the mid-1980s.'),
         dishes=[T('五花肉', 'Samgyeopsal', ko='삼겹살')], img='grill-pork'),
    dict(id='smokeless', y=1995, lane='south', label='1993–2008', yr=T('1993–2008', '1993–2008'), era=T('南 · 分级、无烟炉、韩牛', 'South · grades, smokeless grills, Hanwoo'),
         title=T('烤肉店换了排烟，韩牛有了等级', 'New extraction, and Hanwoo gets graded'),
         text=T('桌下排烟的烤炉技术源自日本（1980 年代的几项专利），如今韩国烤肉店常见的是它和天花板上垂下的伸缩排烟管两种。同一时期，1993 年牛肉分级、2001 年进口全面放开、2008 年溯源制度——韩牛的故事从这里开始，见下一章。',
                'Under-table extraction came from Japanese yakiniku patents of the 1980s; today Korean grill houses use it or telescoping hoods that hang from the ceiling. In the same years came beef grading (1993), full import liberalisation (2001) and traceability (2008) — where the Hanwoo story begins. See the next chapter.'),
         dishes=[T('韩牛', 'Hanwoo', ko='한우')], img='smokeless'),
    dict(id='aged', y=2015, lane='south', label='2010s', yr=T('2010 年代', '2010s'), era=T('南 · 熟成与高端', 'South · aging and fine dining'),
         title=T('种、切、熟、火', 'Breed, cut, age, fire'),
         text=T('干式熟成在韩国本无传统，约 2008 年后流行起来（有人推测与金融危机后回国的留美厨师有关），又扩展到猪肉。高端店讲究品种、自家分切、熟成与炭种（白炭、备长炭、稻草火收尾），多由店员全程代烤，有的进了米其林必比登名单。',
                'Dry-aging had no Korean tradition; it took off after about 2008 (one writer guesses, with chefs returning from America after the financial crisis), then spread to pork. High-end grills now talk breed, in-house butchery, aging and charcoal (white charcoal, binchotan, a straw-fire finish), with staff often cooking every piece — some on the Michelin Bib Gourmand list.'),
         dishes=[T('熟成肉', 'Aged meat', ko='숙성육')], img='aged'),
    dict(id='dog24', y=2024, lane='south', label='2024', yr=T('2024', '2024'), era=T('南 · 告别狗肉', 'South · the end of dog meat'),
         title=T('国会立法终结食用狗肉', 'A law to end dog meat'),
         text=T('2024 年 1 月 9 日，韩国国会通过特别法，禁止为食用饲养、屠宰狗和流通狗肉，罚则 2027 年起生效。立法时全国约有 1,100 家狗场、1,600 家狗肉餐馆。三伏天吃狗肉汤的习俗见于 1849 年的《东国岁时记》。',
                'On 9 January 2024 the National Assembly passed a special act banning the breeding, slaughter and sale of dogs for food, with penalties from 2027. About 1,100 dog farms and 1,600 restaurants were operating. The custom of dog stew in the dog days of summer is recorded in the 1849 <i>Dongguk Sesigi</i>.'),
         dishes=[], img='h-seoul'),
    # ---- 北 ----
    dict(id='okryu', y=1961, lane='north', label='1960–61', yr=T('1960–61', '1960–61'), era=T('北 · 玉流馆', 'North · Okryugwan'),
         title=T('大同江边的玉流馆', 'Okryugwan on the Taedong'),
         text=T('平壤玉流馆 1960–61 年开业（两说），可容约 2,000 人，招牌是平壤冷面，菜单还有排骨汤、绿豆煎饼、神仙炉。烤肉并不是它的主角。',
                'Pyongyang’s Okryugwan opened in 1960 or 1961 (sources differ), seats about 2,000 and is famous for cold noodles, with galbi soup, mung-bean pancakes and sinseollo. Barbecue is not its star.'),
         dishes=[T('平壤冷面', 'Pyongyang naengmyeon', ko='평양랭면')], img='n-okryu'),
    dict(id='nban', y=1995, lane='north', label='1990s', yr=T('1990 年代', '1990s'), era=T('北 · 牛是国家财产', 'North · cattle belong to the state'),
         title=T('私宰一头牛，罪同破坏国家财产', 'Kill a cow, and you’ve destroyed state property'),
         text=T('在朝鲜，牛是耕畜与运力，由国家管理，个人不得拥有、宰杀或买卖；病死的牛要兽医认定才能分配，大量流入黑市。牛肉主要流向干部、军官和外国人，普通人多在节日才吃到肉。一位脱北记者认为，若无严厉的牛禁，1990 年代的饥荒里耕牛很可能早被吃光。',
                'In the North, cattle are draught power managed by the state: no one may own, kill or trade them, and animals that die must be certified by a vet before the meat is allotted — much of it leaks to the black market. Beef goes mostly to officials, officers and foreigners; ordinary people eat meat on holidays. A defector journalist argues that without the ban the oxen would probably have been eaten in the 1990s famine.'),
         dishes=[], img='n-farm'),
    dict(id='duck', y=2011, lane='north', label='2011', yr=T('2011', '2011'), era=T('北 · 烤鸭肉', 'North · duck barbecue'),
         title=T('平壤的烤鸭肉餐厅', 'Pyongyang’s duck-barbecue house'),
         text=T('2011 年金正日视察改造后的平壤斗湍鸭场（朝中社报道）。平壤统一大街的烤鸭肉餐厅里，食客在桌中央自烤鸭肉，用生菜蘸大酱、辣酱包着吃，配烧酒，最后以鸭汤饭或冷面收尾——和南边的烤肉流程几乎一样。',
                'In 2011 Kim Jong Il toured the upgraded Tudan Duck Farm in Pyongyang (KCNA). At the duck-barbecue house on Tongil Street, diners grill duck at the centre of the table, wrap it in lettuce with doenjang and gochujang, drink soju, and finish with duck soup-rice or cold noodles — almost the Southern script.'),
         dishes=[T('烤鸭肉', 'Grilled duck', ko='오리고기')], img='n-duck'),
    dict(id='clam', y=2012, lane='north', label='Nampo', yr=T('南浦', 'Nampo'), era=T('北 · 海边', 'North · by the sea'),
         title=T('浇汽油点火的烤蛤蜊', 'Clams grilled with petrol'),
         text=T('南浦海边的「汽油烤蛤蜊」：把蛤蜊口朝下排成圆圈，直接浇汽油点火烧五到十分钟，熟了撬开吃，配烧酒，是外国游客团的固定节目。',
                'On the Nampo shore: clams set mouth-down in a ring, doused with petrol and set alight for five to ten minutes, then prised open with soju — a fixture of foreign tour groups.'),
         dishes=[T('汽油烤蛤蜊', 'Petrol clams', ko='휘발유 조개구이')], img='n-clam'),
    dict(id='nrest', y=2017, lane='north', label='2016–17', yr=T('2016–17', '2016–17'), era=T('北 · 海外餐厅', 'North · restaurants abroad'),
         title=T('开在国外的朝鲜餐厅', 'North Korean restaurants abroad'),
         text=T('朝鲜海外餐厅自 1990 年代起由各机关开设，2010 年已超过 100 家，遍布中国各地与东南亚、俄罗斯、中东等地，主打冷面、排骨汤与泡菜，服务员兼演唱，每家每年须上缴 10–30 万美元。2016 年宁波一家店 13 人集体出走韩国；2017 年安理会第 2375 号决议后，中国要求朝鲜企业关闭，最大的海外朝鲜餐厅、丹东的「平壤高丽馆」当年 11 月停业。',
                'Run by state bodies since the 1990s, North Korean restaurants abroad passed 100 by 2010 — across China, Southeast Asia, Russia and the Gulf — selling cold noodles, galbi soup and kimchi, with waitresses who sing, each remitting $100,000–300,000 a year. In 2016 thirteen staff from a restaurant in Ningbo defected to the South; after UN Resolution 2375 in 2017 China ordered North Korean firms closed, and the largest North Korean restaurant abroad, Pyongyang Koryo-gwan in Dandong, shut that November.'),
         dishes=[], img='n-rest'),
    dict(id='dangogi', y=2021, lane='north', label='2021', yr=T('2021', '2021'), era=T('北 · 단고기', 'North · dangogi'),
         title=T('北边叫它「甜肉」', 'In the North it is “sweet meat”'),
         text=T('北边把狗肉叫「단고기」（甜肉），官方称狗肉汤为民族料理、列入非物质文化遗产，还在黄金时段播狗肉烹饪比赛；2021 年金正恩批准在大同江畔、玉流馆附近新建大型狗肉餐厅的设计。南北在这件事上正好走向两头。',
                'The North calls dog meat dangogi, “sweet meat”: dog soup is an official national dish on the intangible-heritage list, with cooking contests on prime-time TV, and in 2021 Kim Jong Un approved the design of a large new dangogi restaurant on the Taedong near Okryugwan. On this, North and South went opposite ways.'),
         dishes=[T('단고기', 'Dangogi', ko='단고기')], img='n-pyongyang'),
]

# ---------- 02 TABLE ----------
TABLE = [
    dict(id='center', title=T('火在桌子中间', 'Fire at the centre'), text=T('桌面嵌炉、自己翻肉，是韩烤最显眼的形态；雏形可追溯到朝鲜后期两班的暖炉会。', 'A grill set into the table, and you turn the meat — the most visible trait, going back to late-Joseon brazier parties.'), img='table'),
    dict(id='staff', title=T('或者，店员替你烤', 'Or the staff grill for you'), text=T('2010 年代以后的高端店多由店员全程代烤，讲火候、讲切法——另一种服务形态。', 'High-end places since the 2010s have staff cook every piece, minding heat and cut.'), img='staff'),
    dict(id='scissors', title=T('剪刀', 'Scissors'), text=T('在烤盘上直接剪肉并不是老规矩：据《韩国时报》专栏作者梁东熙的说法，始于 1970 年代，起初用来剪冷面；如今烤肉、泡菜也都用剪刀剪，省了刀和砧板。', 'Cutting meat on the grill with scissors is not an old custom: a Korea Times columnist dates it to the 1970s, first for cold noodles; today meat and kimchi get the scissors too, no knife or board needed.'), img='scissors'),
    dict(id='ssam', title=T('生菜包', 'Ssam — the wrap'), text=T('用叶菜包饭至少可追溯到高丽：元代马端临的《文献通考》记高丽人用生菜包饭。烤肉 + 生菜 + 包饭酱（大酱拌辣酱）是现代烤肉店的定式。', 'Wrapping rice in leaves goes back at least to Goryeo — a Yuan-era encyclopedia records Koreans wrapping rice in raw greens. Meat + lettuce + ssamjang is the modern standard.'), img='ssam'),
    dict(id='banchan', title=T('小菜通常会再上', 'Side dishes usually come back'), text=T('小菜随烤肉一起上，吃完通常可以再要。', 'Banchan arrive with the meat and are usually refilled on request.'), img='banchan'),
    dict(id='soju', title=T('烧酒', 'Soju'), text=T('烤肉配烧酒是固定搭配，1940 年《东亚日报》一篇写平壤风俗的特稿已把「烧酒与불고기」并提；平壤的烤鸭餐厅也配烧酒。', 'Barbecue and soju belong together — a 1940 Dong-a Ilbo feature on Pyongyang already paired them; the North’s duck houses pour it too.'), img='soju'),
    dict(id='finish', title=T('收尾：冷面或炒饭', 'The finish: noodles or fried rice'), text=T('烤完以冷面或在烤盘上炒饭收尾；穹顶汤盘时代把饭拌进槽里的甜汤；平壤烤鸭餐厅则用鸭汤饭或冷面。', 'End with cold noodles or rice fried on the grill; in the dome-pan days rice went into the broth moat; in Pyongyang, duck soup-rice or naengmyeon.'), img='finish'),
    dict(id='grills', title=T('炉子的演变', 'How the grill changed'), text=T('铁板与炭炉（1849 年已有记载）→ 铁丝网直火 → 蜂窝煤（猪）/ 穹顶汤盘（牛） → 便携燃气炉 → 桌下排烟 / 天花板伸缩排烟管 → 讲究炭种。', 'Iron plate over charcoal (recorded 1849) → wire grill → coal briquettes (pork) / domed broth pan (beef) → portable gas → under-table and ceiling extraction → charcoal as a selling point.'), img='grills'),
]

NS = dict(
    s=dict(h=T('南 · 首尔的一桌', 'South · a table in Seoul'), k=T('牛、猪都上桌，按部位点', 'Beef and pork, ordered by cut'),
           li=[T('按部位点肉：牛肉眼、牛排骨、五花、猪颈肉，菜单就是一张分割图。', 'You order by cut — ribeye, short rib, pork belly, neck: the menu is a butchery chart.'),
               T('韩牛与进口牛分开标价；餐馆须标原产地，肉铺的标签上有等级与 12 位溯源号。', 'Hanwoo and imported beef are priced apart; restaurants must show origin, and butcher labels carry the grade and the 12-digit traceability number.'),
               T('2024 年立法终结食用狗肉，罚则 2027 年生效。', 'Dog meat is being legislated out; penalties apply from 2027.')], img='smokeless'),
    n=dict(h=T('北 · 平壤的一桌', 'North · a table in Pyongyang'), k=T('牛肉稀缺，鸭、猪、蛤蜊上桌', 'Beef is scarce: duck, pork, clams'),
           li=[T('牛是国家财产，牛肉主要流向干部、军官与外国人。', 'Cattle belong to the state; beef goes mainly to officials, officers and foreigners.'),
               T('烤鸭肉餐厅的流程与南边几乎相同：自烤、生菜包、烧酒、冷面收尾。', 'The duck house runs almost the Southern script: grill it yourself, wrap, soju, noodles.'),
               T('단고기（狗肉）是官方认定的民族料理。', 'Dangogi (dog meat) is an officially honoured national dish.')], img='n-duck'),
)

# ---------- 03 WORLD ----------
WORLD_NOTE = T('两组「海外韩餐馆」数字口径不同：韩食振兴院统计的是全部韩餐馆（2017 年 90 国 33,499 家），农林畜产食品部与 aT 统计的是韩国餐饮品牌的连锁门店（2025 年 56 国 4,644 家），不能放在一起比。',
               'Two different counts: the Korean Food Promotion Institute counts all Korean restaurants abroad (33,499 in 90 countries, 2017); MAFRA/aT counts outlets of Korean restaurant brands (4,644 in 56 countries, 2025). They are not comparable.')

# ---------- 01 CUT ----------
CH['cut']['lede'] = T('韩牛几乎只在韩国卖：2025 年 1–7 月只出口了 27.2 吨（约 180 万美元）；按 2024 年的出口量算，约八成去了香港。它的成功不在出海，而在守住本国的高端市场——1993 年在全面开放进口前先搞分级，2008–09 年建立从农场到肉铺的个体溯源，2005 年起农户每屠宰一头牛交 2 万韩元自助金做宣传，再加上「肉铺 + 餐厅」和名节礼盒。先从一头牛怎样被分开说起。',
                      'Hanwoo is sold almost only in Korea: Jan–Jul 2025 exports came to just 27.2 tonnes (about $1.8M), and in 2024 about four-fifths of the volume went to Hong Kong. Its success is not abroad but in holding the premium end of the home market — grading introduced in 1993 before imports fully opened, farm-to-counter traceability for every animal in 2008–09, farmers paying ₩20,000 a head at slaughter since 2005 for promotion, plus butcher-restaurants and holiday gift boxes. Start with how one animal is taken apart.')

CUT_INTRO = T('韩国的牛肉零售标示标准把一头牛分成 <b>10 个大分割、39 个小分割</b>。点一个大块看位置、口感和吃法，再点里面的小分割。《韩牛狂想曲》里说的「一头牛能分出 120 种部位与风味」，常被归到人类学家米德名下，但原始出处找不到；39 是官方数字。',
              'Korea’s retail labelling standard divides a carcass into <b>10 primals and 39 sub-primals</b>. Tap a block for where it sits, how it eats and how it’s cooked, then tap the sub-cuts. The “120 cuts and flavours in one cow” quoted in <i>Hanwoo Rhapsody</i> is usually credited to Margaret Mead, but no original source turns up; 39 is the official number.')

# grid-area: 行起/列起/行止/列止（16 × 9 网格，左头右尾、上背下腹；只示意相对位置）
CUT_AREA = {'moksim': '1/1/5/4', 'deungsim': '1/4/4/9', 'chaekkeut': '1/9/4/12', 'udun': '1/12/5/17', 'galbi': '4/4/7/9', 'ansim': '4/9/7/12',
            'apdari': '5/1/8/4', 'seoldo': '5/12/8/17', 'yangji': '7/4/10/12', 'satae': '8/1/10/4'}
CUT_AREA2 = {'satae': '8/12/10/17'}
PRICE_EN = {'最高档': 'Top', '高': 'High', '中高': 'Mid-high', '中': 'Mid', '中低': 'Mid-low', '低至中': 'Low–mid', '高（稀少）': 'High (scarce)', '最高档（稀少）': 'Top (scarce)'}

# 烤一块：每面秒数取 B 路 grill_sec 的中值；是店里常见做法，不是官方标准
GRILL = [
    ('chadolbagi', [7, 7], T('刨片上盘，<b>卷起来就熟了</b>。', 'Shaved thin — <b>when it curls, it’s done</b>.')),
    ('kkotdeungsim', [75, 75], T('整片上网，别急着翻：等下面焦了再动。', 'Lay the whole slice down and leave it until the underside sears.')),
    ('ansim_b', [50, 50, 50, 50], T('切方块，四面快煎，里面留红。', 'Cut into cubes; sear all four sides, keep the centre red.')),
    ('salchisal', [30, 30], T('脂肪极密，一过火就出油变柴，快。', 'So marbled that overcooking renders the fat out and leaves it dry — be quick.')),
    ('galbisal', [45, 45], T('烤到表面焦脆。', 'Until the surface is crisp.')),
    ('anchangsal', [50, 50], T('先去膜、逆纹切，猛火。', 'Membrane off, cut across the grain, high heat.')),
    ('tosisal', [50, 50], T('去掉中间那条筋，大火快烤。', 'Remove the centre sinew; hot and fast.')),
    ('buchaesal', [40, 40], T('中间一道筋，横切成片就能嚼。', 'A line of sinew down the middle — slice across it.')),
    ('chimasal', [25, 25], T('逆纹切条，快烤。', 'Strips across the grain, quick.')),
    ('eopjinsal', [22, 22], T('烤到油脂变透明。', 'Until the fat turns translucent.')),
]
GRILL_NOTE = T('秒数是按常见厚度给的经验估计（取区间中值），不是官方标准；炭火、厚度、店家习惯都会让它差很多。按「5× 快进」可以不用真等。',
               'Times are rule-of-thumb estimates for typical thickness (mid-point of the usual range), not an official standard — charcoal, thickness and house habit change them a lot. Hit “5×” if you don’t want to wait.')

GRADES_NOTE = T('肉质等级以大理石纹（1–9 号）为主，2019 年起肉色、脂肪色、组织感也分别评级、取最低一项；2019 年 12 月起 1++ 由 8–9 号下调为 7–9 号，目的是把平均育肥期从 31.2 个月缩到 29 个月。另有产肉量等级 A/B/C，两者合标，如「1++A」。韩牛 1 等级以上的比例，1993 年刚分级时约 10.7%，2022 年 75.2%。',
                'Quality grade rests mainly on marbling (No. 1–9); since 2019 meat colour, fat colour and texture are also graded and the lowest applies; since December 2019, 1++ needs No. 7–9 instead of 8–9, to cut average finishing from 31.2 to 29 months. A separate yield grade A/B/C is shown alongside, e.g. “1++A”. The share of Hanwoo grading 1 or above was about 10.7% when grading began in 1993, and 75.2% in 2022.')

SERIES = dict(
    title=T('进口牛肉量与牛肉自给率', 'Beef imports and self-sufficiency'),
    l1=T('进口牛肉（千吨）', 'Beef imports (k tonnes)'), l2=T('牛肉自给率', 'Beef self-sufficiency'),
    note=T('口径：2004–2015 年取自韩国农村经济研究院（KREI）的展望与现案分析（2004–2009 为精肉基准）；2020–2022 年自给率按 USDA 胴体当量推算，2021 年进口量是 USDA 产品重量，和前一段不可直接相比，所以图上断开。2025 年只有 1–10 月的海关累计（423.7 千吨），不是全年，没有画进图里。中间缺的年份没有找到同口径数据。',
             'Basis: 2004–2015 from the Korea Rural Economic Institute (KREI) outlooks (2004–09 on a boneless basis); 2020–22 self-sufficiency is derived from USDA carcass-weight data and 2021 imports are USDA product weight — not directly comparable, hence the break. 2025 has only Jan–Oct customs data (423.7k t), not a full year, so it is left off the chart. Missing years had no like-for-like data.'),
    events=[
        T('4 月韩美同意进口 30 月龄以上美国牛肉，首尔爆发烛光抗议；6 月改为限 30 月龄以下。12 月起饲养阶段实施溯源。', 'April: Seoul agrees to US beef over 30 months; candlelight protests follow; in June it is limited to under 30 months. Traceability starts on farms in December.', year=2008),
        T('6 月溯源扩大到流通环节：12 位个体识别号查得到出生、屠宰与等级。', 'June: traceability extends to retail — a 12-digit ID shows birth, slaughter and grade.', year=2009),
        T('3 月韩美 FTA 生效，美国牛肉 40% 关税分 15 年降到零；9 月韩肉牛存栏创高峰 314 万头。', 'March: the Korea–US FTA takes effect; the 40% US beef tariff starts a 15-year glide to zero. September: herd peaks at 3.14 million.', year=2012),
        T('12 月韩牛首次出口香港。', 'December: first Hanwoo export, to Hong Kong.', year=2015),
        T('9 月《请托禁止法》施行，礼品上限 5 万韩元，高价韩牛礼盒受冲击（后来上调到名节 30 万）。', 'September: the anti-graft act caps gifts at ₩50,000, hitting premium Hanwoo gift boxes (later raised to ₩300,000 at holidays).', year=2016),
        T('12 月等级标准改版，1++ 门槛下调，缩短育肥期。', 'December: grading revised, lowering the 1++ threshold to shorten finishing.', year=2019),
        T('美国牛肉进口约占进口牛肉一半。', 'US beef is about half of all beef imports.', year=2022),
        T('5 月清州口蹄疫，申请 WOAH「口蹄疫免疫无疫」地位的计划落空，扩大出口受阻。', 'May: foot-and-mouth in Cheongju derails Korea’s bid for WOAH “FMD-free with vaccination” status — and with it export growth.', year=2023),
        T('3 月全南灵岩口蹄疫；7 月国会 263 比 0 通过《韩牛法》（2026 年 8 月施行）。', 'March: foot-and-mouth in Yeongam. July: the Hanwoo Act passes 263–0 (in force Aug 2026).', year=2025),
        T('1 月 1 日韩美 FTA 下的美国牛肉关税归零。', '1 January: the US beef tariff under the Korea–US FTA hits zero.', year=2026),
    ],
)

RHAPSODY = dict(
    h=T('《韩牛狂想曲》里的那一段', 'That scene in <i>Hanwoo Rhapsody</i>'),
    li=[T('KBS1《다큐 인사이트》两集，白种元讲述；2021 年 12 月 9 日、16 日首播，Netflix 也在 2021 年上线。是「K-FOOD 狂想曲」系列的第三部，前两部是五花肉与冷面。', 'Two episodes of KBS1’s <i>Docu Insight</i>, presented by Paik Jong-won, first aired 9 and 16 December 2021 and released on Netflix the same year — third in the “K-Food Rhapsody” series after pork belly and naengmyeon.'),
        T('第 1 集讲从불고기、갈비到韩牛，一头牛能分出的部位与风味，以及溯源制度；第 2 集讲「一头牛没有浪费的部分」——곰탕、설렁탕、头尾、内脏、牛舌与骨髓。', 'Episode 1 goes from bulgogi and galbi to Hanwoo — the cuts and flavours of one animal, and traceability. Episode 2: “no part goes to waste” — gomtang, seolleongtang, head, tail, offal, tongue and marrow.'),
        T('片中走访的是「精肉食堂」：先在肉铺按部位、等级挑肉，再付少量桌位费在隔壁自己烤。', 'It visits a jeongyuk sikdang: choose by cut and grade at the butcher’s counter, then pay a small table fee and grill it next door.')],
)

VS_HEAD = (T('', ''), T('韩牛 Hanwoo', 'Hanwoo'), T('和牛 Wagyu', 'Wagyu'))

METHOD = T('研究分三部分：火与桌（半岛吃肉史、北半岛、狗肉、桌上规矩、烤具）、刀（韩牛品牌化、分割、等级、和牛对照、运营）、出海（美国与中国的阶段与节点）。优先用官方、企业文件与学术来源（韩国农林畜产食品部与 aT、KREI、美国 SEC 文件、洛杉矶公共图书馆、学术论文、主要媒体）；百科多作线索，少数条目（玉流馆、Kogi、Cote 等）暂以英文维基为唯一来源。底稿里置信度「低」的事实一般不上正文，个别保留的（如「120 个部位」）在正文里注明出处不明。烤肉计时器的秒数是按常见厚度给的经验估计。分割图是示意，不按比例。北半岛的资料多来自脱北者媒体、朝中社与游客记录，可信度比南边低一档。页面写完后另做了一轮逐条核查，改正了口径混用、两说写成一说之类的问题。',
           'Research came in three parts: fire and table (history, North Korea, dog meat, table customs, grills); cut (Hanwoo branding, butchery, grades, wagyu comparison, operations); abroad (phases and milestones in the US and China). Official, corporate and academic sources first (MAFRA and aT, KREI, SEC filings, the LA Public Library, journal papers, major media); encyclopedias mostly as leads, though a few entries (Okryugwan, Kogi, Cote) still rest on Wikipedia alone. Low-confidence facts are generally kept off the page; the few kept (such as “120 cuts”) are flagged as unsourced. Grill times are rule-of-thumb estimates. The butchery chart is schematic. Sources on North Korea lean on defector media, KCNA and travellers, a notch less reliable than for the South. After writing, every claim went through a separate check, which fixed mixed-up bases and disputed points stated as settled.')

PENDING = [
    T('《搜神记》原文按通行本转引，未对照四库本；《释名》「全体炙之，各自以刀割」一句同。', 'The <i>Soushen Ji</i> and <i>Shiming</i> lines are quoted from common editions, not checked against the Siku text.'),
    T('「불고기」最早的报刊用例（1931、1932、1935 年《东亚日报》）只见二手转述，未见原版面。', 'Early press uses of “bulgogi” (Dong-a Ilbo 1931/32/35) are from secondary accounts; the original pages were not seen.'),
    T('玉流馆开业年份 1960 / 1961 两说；平壤烤鸭肉餐厅的正式名与开业年份未查到。', 'Okryugwan’s opening year (1960 or 1961) is disputed; the duck house’s official name and opening year were not found.'),
    T('美国、中国是否明文禁止韩国牛肉进口没有找到一手文件，页面的说法依据的是韩牛出口目的地名单。', 'No primary document was found stating a US or Chinese ban on Korean beef; the page relies on the list of export destinations.'),
    T('牛肉自给率与进口量缺 2016–2019 年同口径数据；2020 年以后的数据口径不同。', 'Like-for-like self-sufficiency and import data for 2016–19 are missing; post-2020 figures use a different basis.'),
    T('韩国狗肉禁令的公布日与生效日依新闻报道，未对照法令原文。', 'Dates of the dog-meat act are from press reports, not the statute text.'),
    T('Cote 纽约获米其林一星的确切年份（开业一年内，2017 或 2018）。', 'The exact year Cote New York won its Michelin star (within a year of opening, 2017 or 2018).'),
    T('韩牛出口目的地名单各报道不一：除香港、马来西亚、柬埔寨、老挝、阿联酋外，也有报道列入澳门、蒙古。', 'Reports differ on Hanwoo’s export markets: besides Hong Kong, Malaysia, Cambodia, Laos and the UAE, some list Macau and Mongolia.'),
    T('马端临《文献通考》「高丽人用生菜包饭」一句据韩文转述，未见汉文原文。', 'Ma Duanlin’s line on Koreans wrapping rice in greens is known here only from a Korean paraphrase.'),
    T('1940 年《东亚日报》「烧酒与불고기」一句只见二手转述，未见原版面。', 'The 1940 Dong-a Ilbo “soju and bulgogi” line comes from a secondary account; the page itself was not seen.'),
    T('「剪刀始于 1970 年代」只有一位专栏作者的说法。', 'The 1970s date for table scissors rests on one columnist.'),
]

# ---------- 03 WORLD：可播放的两国时间轴（替代地图；2026-10-31 天杰：「不用地图了，出一个按中美两国市场大事件的可播放时间轴」）----------
# (泳道, 阶段 id, 底稿 facts 下标, 显示年份, 短标题)；正文与来源取自 market_C.json（经 fixes.py 改正后）
TL_EVENTS = [
    ('us', 'us1', 0, '1903', T('首批移民到夏威夷', 'First immigrants reach Hawaii')),
    ('us', 'us2', 0, '1965', T('新移民法', 'The 1965 immigration act')),
    ('us', 'us2', 2, '1969', T('「新韩国餐厅」开业', 'New Korea Restaurant opens')),
    ('us', 'us2', 3, '1980', T('韩国城获官方认可', 'Koreatown made official')),
    ('us', 'us6', 4, '1982', T('H Mart 起家', 'H Mart’s first store')),
    ('us', 'us2', 4, '1985', T('吃到饱的雏形', 'Proto all-you-can-eat')),
    ('us', 'us3', 1, '1992', T('洛杉矶骚乱', 'The LA riots')),
    ('us', 'us4', 0, '2008', T('Kogi 韩式塔可车', 'The Kogi taco truck')),
    ('us', 'us4', 3, '2011', T('GEN 首店', 'The first GEN')),
    ('us', 'us5', 0, '2012', T('白丁进美国', 'Baekjeong arrives')),
    ('us', 'us5', 1, '2017', T('Cote 纽约', 'Cote New York')),
    ('us', 'us6', 0, '2023', T('GEN 上市', 'GEN goes public')),
    ('us', 'us6', 3, '2023', T('白丁湾区首店', 'Baekjeong in San Jose')),
    ('us', 'us6', 1, '2024', T('GEN 营收 2.08 亿美元', 'GEN: $208M revenue')),
    ('us', 'us6', 2, '2025', T('在美门店 1,106 家', '1,106 outlets in the US')),
    ('cn', 'cn1', 0, '19C–1940s', T('朝鲜族落户延边', 'Koreans settle in Yanbian')),
    ('cn', 'cn2', 0, '1992', T('中韩建交', 'China–South Korea ties')),
    ('cn', 'cn2', 1, '1998', T('汉阳馆深圳首店', 'Hanyangguan opens in Shenzhen')),
    ('cn', 'cn2', 2, '2004', T('汉拿山公司注册', 'Hannashan registered')),
    ('cn', 'cn3', 1, '2014', T('炸鸡啤酒热', 'The chimaek craze')),
    ('cn', 'cn3', 2, '2015', T('汉拿山约 260 家', 'Hannashan at ~260')),
    ('cn', 'cn4', 0, '2017', T('萨德与「限韩令」', 'THAAD and the “Korea ban”')),
    ('cn', 'cn3', 0, '2017', T('韩餐馆 15,985 家', '15,985 Korean restaurants')),
    ('cn', 'cn4', 3, '2021', T('汉拿山减至 205 家', 'Hannashan down to 205')),
    ('cn', 'cn5', 0, '2024', T('韩式成烤肉三大赛道之一', 'Korean-style: one of three BBQ lanes')),
    ('cn', 'cn5', 3, '2025', T('在华门店 830 家', '830 outlets in China')),
]
TL_LANES = {'us': T('美国', 'USA'), 'cn': T('中国', 'China')}
TL_NOTE = T('按 ▶ 播放，或拖动、点任意一个点；‹ › 在事件之间一件件跳。1965 年以前压缩显示。每条下面都有来源。',
            'Press ▶, drag, or tap any dot; ‹ › step from event to event. Years before 1965 are compressed. Every event links to its source.')
