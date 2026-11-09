# -*- coding: utf-8 -*-
"""页面槽位 → images_E.json 里的图（id, 中文说明, 英文说明[, 最长边]）。说明只写画面里看得到的东西与出处。"""
CHOICE = {
    # 卷首与章首图版
    'hero': ('hero-02', '奶酪店里层层堆叠的陈年奶酪轮', 'Aged wheels stacked in a cheese shop', 2200),
    'plate-hist': ('history-07', '克拉拉·彼得斯《奶酪、杏仁与椒盐卷饼静物》（约 1615 年）', 'Clara Peeters, <i>Still Life with Cheeses, Almonds and Pretzels</i> (c. 1615)', 1800),
    'plate-make': ('making-01', '帕玛森式奶酪坊：工人在倒钟形铜锅旁搅动凝乳', 'A Parmigiano-style dairy: stirring curd beside the bell-shaped copper vats', 1800),
    'plate-taste': ('board-01', '木板上的蓝纹、白霉与灰霉山羊奶酪，配面包与黑莓', 'Blue, bloomy and ash-rinded goat cheeses with bread and blackberries', 1800),
    'plate-world': ('world-qurut-01', '吉尔吉斯斯坦，正在晾晒的库鲁特', 'Qurut drying in the sun, Kyrgyzstan', 1800),
    'plate-counter': ('counter-06', '法国奶酪柜：布里、山羊奶酪与蓝纹，插着价签', 'A French cheese case: Brie, goat cheeses and blues with price tags', 1800),
    # 00 沿革舞台
    'h-pot': ('making-10', '加了凝乳酶的奶凝成一整块，手指一划「断得干净」', 'Renneted milk set into a gel that breaks cleanly under a finger', 1400),
    'h-sieve': ('styles-fresh-03', '带篮纹的新鲜里科塔：至今仍用带孔的模子沥乳清', 'Fresh ricotta with basket marks — still drained in perforated moulds', 1400),
    'h-ur': ('making-02', '刚捞出的凝乳裹在布里沥乳清', 'Fresh curd hanging in cloth to drain', 1400),
    'h-xiaohe': ('world-kefir-01', '纱布封口的玻璃罐里正在发酵的奶', 'Milk fermenting in a cloth-covered jar', 1400),
    'h-homer': ('styles-fresh-02', '几块带细皱外皮的小山羊奶酪', 'Small goat cheeses with wrinkled rinds', 1400),
    'h-rome': ('cave-03', '木架上的大奶酪轮', 'Large wheels on wooden shelves', 1400),
    'h-qmys': ('world-rushan-01', '云南大理街头，摊主在炭火上烤乳扇', 'Grilling rushan over charcoal on a street in Dali, Yunnan', 1400),
    'h-abbey': ('history-08', '中世纪健康手册《Tacuinum Sanitatis》插图「陈年奶酪」', '“Caseus vetus” (aged cheese), from a medieval <i>Tacuinum Sanitatis</i>', 1200),
    'h-market': ('history-12', '1674 年版画《阿尔克马尔过磅房与奶酪市场》', '<i>The Weigh House and Cheese Market at Alkmaar</i>, engraving, 1674', 1400),
    'h-factory': ('making-12', '俄勒冈一家奶酪坊里，凝乳切成长条反复叠放（切达化）', 'Cheddaring at an Oregon creamery: slabs of curd cut and stacked', 1400),
    'h-ration': ('cave-09', '1960 年芬兰 Valio 的 Vaarala 奶酪仓库', 'Valio’s Vaarala cheese store, Finland, 1960', 1400),
    'h-aoc': ('cave-11', '罗克福尔-叙尔-苏尔宗的熟成洞', 'A ripening cave at Roquefort-sur-Soulzon', 1400),
    'h-artisan': ('cave-10', '纽约州 Chaseholm 农场的熟成库', 'The ageing room at Chaseholm Farm, New York', 1400),
    # 01 工艺台：工序图
    'step-milk': ('making-07', '奶酪师在倒钟形铜锅前，锅里是加热中的奶', 'A cheesemaker at a bell-shaped copper vat of warming milk', 1400),
    'step-heat': ('making-07', '奶酪师在倒钟形铜锅前，锅里是加热中的奶', 'A cheesemaker at a bell-shaped copper vat of warming milk', 1400),
    'step-starter': ('making-07', '奶酪师在倒钟形铜锅前，锅里是加热中的奶', 'A cheesemaker at a bell-shaped copper vat of warming milk', 1400),
    'step-rennet': ('making-10', '检验凝乳是否「断得干净」', 'Testing the curd for a clean break', 1400),
    'step-cut': ('making-08', '槽里凝乳与乳清已经分开，工人搅动凝乳粒', 'Curd and whey separated in the vat; a worker stirs the grains', 1400),
    'step-cook': ('making-01', '在铜锅旁搅动凝乳', 'Stirring the curd beside the copper vats', 1400),
    'step-drain': ('making-02', '刚捞出的凝乳裹在布里沥乳清', 'Fresh curd hanging in cloth to drain', 1400),
    'step-form': ('making-06', '刚脱模的小圆奶酪排在托盘上', 'Freshly unmoulded rounds on a tray', 1400),
    'step-salt': ('making-13', '纽约州 Chaseholm 农场，给奶酪刷盐水', 'Brushing cheeses with brine at Chaseholm Farm, New York', 1400),
    'step-form-cheddar': ('making-11', '排乳清后的凝乳堆成两垄，开始切达化', 'Drained curd banked into two walls for cheddaring', 1400),
    'step-form-mozzarella': ('making-03', '双手在热水里拉伸凝乳', 'Stretching curd by hand in hot water', 1400),
    'step-salt-mozzarella': ('making-05', '在乳清里把凝乳捏成马苏里拉球', 'Shaping mozzarella balls in the whey', 1400),
    # 01 工艺台：成品 / 熟成
    's-mozzarella': ('styles-fresh-01', '一盒刚做好的马苏里拉球', 'A tub of freshly made mozzarella', 1400),
    's-feta': ('styles-brine-01', '浅盘上的一块白色盐水奶酪', 'A block of white brined cheese on a plate', 1400),
    's-camembert': ('styles-bloomy-03', '木盒里的卡芒贝尔', 'Camembert in its wooden box', 1400),
    's-epoisses': ('counter-09', '法国奶酪柜，价签上可见 Époisses', 'A French cheese case, with an Époisses tag', 1400),
    's-roquefort': ('cave-11', '罗克福尔-叙尔-苏尔宗的熟成洞', 'A ripening cave at Roquefort-sur-Soulzon', 1400),
    's-gouda': ('cave-06', '木架上的黄色小奶酪轮', 'Small yellow wheels ripening on shelves', 1400),
    's-cheddar': ('cave-10', '纽约州 Chaseholm 农场的熟成库', 'The ageing room at Chaseholm Farm, New York', 1400),
    's-emmental': ('styles-semihard-01', '两块带小孔的半硬质黄奶酪', 'Two wedges of semi-hard cheese with small eyes', 1400),
    's-comte': ('cave-02', '木架上一排排正在熟成的奶酪', 'Rows of wheels ripening on wooden boards', 1400),
    's-parmigiano': ('cave-05', '层层堆放的帕玛森式奶酪轮', 'Parmigiano-style wheels stacked high', 1400),
    # 03 全球
    'w-qurut': ('world-qurut-01', '吉尔吉斯斯坦，正在晾晒的库鲁特', 'Qurut drying in the sun, Kyrgyzstan', 900),
    'w-airag': ('world-airag-02', '彩绘瓷缸里的马奶酒', 'Airag in a painted porcelain vat', 900),
    'w-chhurpi': ('world-chhurpi-01', '喜马拉雅东部的硬曲拉', 'Hard chhurpi from the eastern Himalaya', 900),
    'w-tibetan-butter': ('world-buttertea-01', '一碗酥油茶', 'A bowl of butter tea', 900),
    'w-labneh': ('world-labneh-02', '浸在橄榄油里的拉布内', 'Labneh in olive oil', 900),
    'w-ghee': ('world-ghee-01', '一罐澄清黄油', 'A jar of ghee', 900),
    'w-kefir': ('world-kefir-01', '纱布封口的玻璃罐里正在发酵的奶', 'Milk fermenting in a cloth-covered jar', 900),
    'w-dulce-de-leche': ('world-dulce-01', '一罐顺着罐口流下的牛奶焦糖酱', 'A jar of dulce de leche running over the rim', 900),
    'w-rushan': ('world-rushan-01', '云南大理街头，摊主在炭火上烤乳扇', 'Grilling rushan over charcoal on a street in Dali, Yunnan', 900),
    'a-cn-yunnan': ('world-rushan-01', '云南大理街头，摊主在炭火上烤乳扇', 'Grilling rushan over charcoal on a street in Dali, Yunnan', 900),
}
MOBILE = {'hero': 'hero-06'}
CONTAIN = {'h-abbey', 'h-market'}
ART = {'plate-hist', 'h-abbey', 'h-market'}
