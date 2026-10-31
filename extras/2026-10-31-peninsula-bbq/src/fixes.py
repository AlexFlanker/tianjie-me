# -*- coding: utf-8 -*-
"""核查（research/check_E.json，2026-10-31）之后对研究底稿里「直接上页面」的字段所做的改正。
底稿 JSON 不动；构建时逐条替换，并断言每条恰好命中一次（命中不了就报错，免得改正悄悄失效）。
格式：(底稿, 路径说明, 取值函数, 字段, 旧串, 新串)"""

def _ops(B, oid): return [o for o in B['ops'] if o['id'] == oid][0]
def _cut(B, cid): return [c for c in B['cuts'] if c['id'] == cid][0]
def _ph(C, k, pid): return [p for p in C[k]['phases'] if p['id'] == pid][0]

FIX = [
    # 和牛对照表：香港「八成」是 2024 年的比例；出口地名单各报道不一
    ('B', 'wagyu_vs[4]', lambda B: B['wagyu_vs'][4], 'hanwoo_zh', '2025 年 1–7 月出口 27.2 吨、约 180 万美元，五个市场，香港占八成。', '2025 年 1–7 月出口 27.2 吨、约 180 万美元；2024 年出口量约八成去了香港。'),
    ('B', 'wagyu_vs[4]', lambda B: B['wagyu_vs'][4], 'hanwoo_en', '27.2 t, about USD 1.8m in Jan–Jul 2025, to five markets with Hong Kong taking ~80%.', '27.2 t, about USD 1.8m in Jan–Jul 2025; Hong Kong took ~80% of 2024 volume.'),
    # 免疫无疫；新加坡 2026 年已签检疫协议；美中「进不去」只有出口名单为据
    ('B', 'wagyu_vs[5]', lambda B: B['wagyu_vs'][5], 'hanwoo_zh', '口蹄疫反复，未获 WOAH 无疫地位；美、中、新加坡等大市场长期进不去，每次疫情都中断出口。', '口蹄疫反复，未获 WOAH「口蹄疫免疫无疫」地位；美、中至今不在出口名单上，新加坡到 2026 年才签检疫协议；每次疫情都中断出口。'),
    ('B', 'wagyu_vs[5]', lambda B: B['wagyu_vs'][5], 'hanwoo_en', 'Recurring FMD has kept WOAH status out of reach; the US, China and others stayed closed, and each outbreak halts exports.', 'Recurring FMD has kept WOAH “FMD-free with vaccination” status out of reach; the US and China are still not on the export list, Singapore signed a quarantine deal only in 2026, and each outbreak halts exports.'),
    # 价格：数据来自畜产品品质评价院、不是「首尔」；13,105 是韩牛日之后的冲高价
    ('B', 'wagyu_vs[8]', lambda B: B['wagyu_vs'][8], 'hanwoo_zh', '首尔 1+ 등심约 13,105 韩元/100g（2025-11），约合 40 美元/磅。', '1+ 등심零售约 9,600–13,100 韩元/100g（2025 年 11 月，畜产品品质评价院），约合 30–40 美元/磅。'),
    ('B', 'wagyu_vs[8]', lambda B: B['wagyu_vs'][8], 'hanwoo_en', '1+ Hanwoo loin about KRW 13,105/100 g in Seoul (Nov 2025), roughly USD 40/lb.', '1+ Hanwoo loin retailed at about KRW 9,600–13,100/100 g in Nov 2025 (KAPE), roughly USD 30–40/lb.'),
    # 七招：精肉食堂「三分之一」说的是整顿饭的花费，不是桌位费
    ('B', 'ops.jeongyuk.facts[1]', lambda B: _ops(B, 'jeongyuk')['facts'][1], 'zh', '马场洞「고기 익는 마을」2011 年桌位费成人 4,000 韩元、儿童 2,000 韩元，被认为约为普通韩牛店价格的三分之一。', '马场洞「고기 익는 마을」2011 年桌位费成人 4,000 韩元、儿童 2,000 韩元；据消费者说，在这里吃最高等级韩牛，只要一般韩牛店约三分之一的价钱。'),
    ('B', 'ops.jeongyuk.facts[1]', lambda B: _ops(B, 'jeongyuk')['facts'][1], 'en', "At Majang-dong's 'Gogi Ingneun Maeul' (2011), the table fee was KRW 4,000 per adult and 2,000 per child — reportedly about a third of regular Hanwoo restaurant prices.", "At Majang-dong's 'Gogi Ingneun Maeul' (2011) the table fee was KRW 4,000 per adult and 2,000 per child; diners said top-grade Hanwoo there cost about a third of what a regular Hanwoo restaurant charges."),
    # 七招：2025 年比例只见无出处的博客，换成 2022 年
    ('B', 'ops.grading_trace.facts[1]', lambda B: _ops(B, 'grading_trace')['facts'][1], 'zh', '2019 年 79.3%、2025 年 78.4%，阉牛达 92%。', '2019 年 79.3%、2022 年 75.2%。'),
    ('B', 'ops.grading_trace.facts[1]', lambda B: _ops(B, 'grading_trace')['facts'][1], 'en', '79.3% (2019) and 78.4% (2025); 92% for steers.', '79.3% (2019) and 75.2% (2022).'),
    # 分割图：등심 与 안심 不能都叫「里脊」；목심 不再标「上脑前段」
    ('B', 'cuts.deungsim', lambda B: _cut(B, 'deungsim'), 'primal_zh', '里脊（肋眼、上脑）', '肉眼（眼肉、上脑）'),
    ('B', 'cuts.moksim', lambda B: _cut(B, 'moksim'), 'primal_zh', '颈肉（上脑前段）', '颈肉'),
    ('B', 'cuts.kkotdeungsim', lambda B: _cut(B, 'kkotdeungsim'), 'primal_zh', '花里脊（肋眼）', '花肉眼（肋眼）'),
    ('B', 'cuts.deungsim.subs[0]', lambda B: _cut(B, 'deungsim')['subs'][0], 'zh', '上里脊（前段）', '上肉眼（前段）'),
    ('B', 'cuts.deungsim.subs[1]', lambda B: _cut(B, 'deungsim')['subs'][1], 'zh', '花里脊（肋眼）', '花肉眼（肋眼）'),
    ('B', 'cuts.deungsim.subs[2]', lambda B: _cut(B, 'deungsim')['subs'][2], 'zh', '下里脊（后段）', '下肉眼（后段）'),
    # 美国：El Camino Real 一句没有来源
    ('C', 'us.us6.facts[3]', lambda C: _ph(C, 'us', 'us6')['facts'][3], 'zh', '；湾区韩烤此前集中在圣克拉拉 El Camino Real 沿线的韩裔商圈。', '。'),
    ('C', 'us.us6.facts[3]', lambda C: _ph(C, 'us', 'us6')['facts'][3], 'en', "; Bay Area KBBQ had long clustered along El Camino Real in Santa Clara's Korean business strip.", '.'),
    # 美国：1,106 家门店以炸鸡、面包连锁为主（全部海外门店里炸鸡 39%、面包店 25.5%）
    ('C', 'us.us6.facts[2]', lambda C: _ph(C, 'us', 'us6')['facts'][2], 'zh', '美国取代中国成为韩餐企业最大海外市场。', '美国取代中国成为韩餐企业最大海外市场；这批海外门店以炸鸡、面包连锁为主（全部海外门店里炸鸡占 39%、面包店 25.5%）。'),
    ('C', 'us.us6.facts[2]', lambda C: _ph(C, 'us', 'us6')['facts'][2], 'en', 'making the U.S. their largest overseas market, ahead of China.', 'making the U.S. their largest overseas market, ahead of China; these outlets are mostly fried-chicken and bakery chains (39% and 25.5% of all overseas outlets).'),
    # 中国：收缩不宜单归因于萨德
    ('C', 'cn.cn4.facts[3]', lambda C: _ph(C, 'cn', 'cn4')['facts'][3], 'zh', '萨德之后，「韩国」招牌在中国餐饮中的号召力减弱，多家韩式烤肉品牌在之后几年收缩：汉拿山门店从2015年约260家减至2021年4月的205家。', '萨德之后几年，多家韩式烤肉品牌收缩（也与疫情、同质化有关）：汉拿山门店从 2015 年约 260 家（企业自述）减至 2021 年 4 月的 205 家（NCBD）。'),
    ('C', 'cn.cn4.facts[3]', lambda C: _ph(C, 'cn', 'cn4')['facts'][3], 'en', "After THAAD the 'Korean' label lost pull in Chinese dining and several Korean BBQ brands contracted; Hannashan fell from about 260 stores in 2015 to 205 in April 2021.", 'In the years after THAAD several Korean BBQ brands shrank — also amid the pandemic and copycat competition: Hannashan went from about 260 stores in 2015 (company figure) to 205 in April 2021 (NCBD).'),
    # 中国：「增长约 7.8 倍」改成「为 2009 年的约 7.8 倍」
    ('C', 'cn.cn3.facts[0]', lambda C: _ph(C, 'cn', 'cn3')['facts'][0], 'zh', '中国的韩餐馆从2009年起8年间增长约7.8倍，2017年达15,985家', '中国的韩餐馆 2017 年达 15,985 家，为 2009 年的约 7.8 倍'),
]

def apply(B, C):
    src = {'B': B, 'C': C}; n = 0
    for which, where, get, field, old, new in FIX:
        obj = get(src[which]); cur = obj[field]
        assert cur.count(old) == 1, f'fixes.py 未命中：{where}.{field} ← {old[:40]}'
        obj[field] = cur.replace(old, new); n += 1
    return n
