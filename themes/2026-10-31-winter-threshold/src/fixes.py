# -*- coding: utf-8 -*-
"""核查后的改正：DATA（直接改研究底稿的字段，构建时逐条报告是否命中）+ POST（成品页逐条替换）。
研究底稿 JSON 保持原样，改动都记在这里，方便对照。"""

# (路, 节点 id 或 None=整份底稿, 原片段, 新片段)：在该节点（或整份底稿）所有字符串字段里替换
DATA = [
    # v2 核查（2026-10-28）：卡片改成了行，旧的指代要换掉
    ('A', 'halloween', '（见 Samhain 一卡）', '（见 Samhain 一行）'),
    ('A', 'halloween', '见 Samhain 一卡的「岁首」争议', '见 Samhain 一行的「岁首」争议'),
    ('B', 'hanyi', '（详见「秦十月朔」一卡）', '（年轮上的岁首「秦十月朔」即此）'),
    ('A', 'samhain', '它是整张图谱的「西端锚点」：', '它是这十天里最北的一盏灯：'),
    ('C', 'loy-krathong', '同一周里最靠南、最靠近赤道的一盏灯', '北半球冬初这串灯里最靠南的一盏'),
    ('C', 'loy-krathong', '雨季 5 月中到 10 月中，水灯节落在 10/31–11/27', '雨季 5 月中到 10 月中，2015–2027 年的水灯节都落在 10/31–11/27 之间'),
    # 古吉拉特新年：2026 年朔在 11/9 12:32 IST，日出时的白分初一是 11/10（Bestu Varas、牛增山祭同日），11/9 是空档日
    ('C', 'diwali', '古吉拉特以排灯节次日——迦底迦月白分初一（Bestu Varas / Nutan Varsh）——为维克拉姆历（Vikram Samvat）新年',
     '古吉拉特以迦底迦月白分初一（Bestu Varas / Nutan Varsh；通常是排灯节次日，2026 年隔一天，在 11/10）为维克拉姆历（Vikram Samvat）新年'),
    ('C', 'diwali', '在次日的牛增山祭上', '在随后的牛增山祭上'),
    ('C', None, '古吉拉特把排灯节次日——迦底迦月白分初一（Bestu Varas）——当维克拉姆历新年', '古吉拉特把迦底迦月白分初一（Bestu Varas，通常是排灯节次日，2026 年在 11/10）当维克拉姆历新年'),
    # Tihar：2083 是比克拉姆历年份；「3 天」是 2022 年的口径
    ('C', 'tihar', '国家层面 2083 年假日表给五天国定假日（Kartik 22–26，11/8–12；', '国家层面的比克拉姆历 2083 年假日表给五天国定假日（Kartik 22–26，即公历 11/8–12；'),
    ('C', None, '、与第三章同一口径', ''),
    ('C', None, '，与第三章同口径', ''),
    # 寒衣节时间轴：《帝京岁时纪胜》成书 1758 年（1906 年是《燕京岁时记》）
    ('B', 'hanyi', '1906（成书）', '1758（成书）'),
    # 亡灵节大游行：2016 年首办，2020 年因疫情停办，2026 年是第十届
    ('D', 'dia-de-muertos', '2016 年 10 月 29 日首办，2026 年为第十年。', '2016 年 10 月 29 日首办；2020 年因疫情停办，2026 年为第十届。'),
    ('D', None, '2026 年是第十年，', '2020 年因疫情停办，2026 年是第十届，'),
    ('A', 'halloween-south', '天黑在 19 时以后，讨糖', '天黑在 19 时以后（夏令时），讨糖'),
]
# (路, 节点 id, 字段, 下标, 键, 新值)：改结构化字段
SET = [
    ('B', 'hanyi', 'timeline', 4, 'year', 1758),
    ('C', 'tihar', 'numbers', 1, 'label', '国定假日天数（2022 年）'),
]

POST = [
    # ('原片段', '新片段'),
]


def _sub(o, old, new):
    """在 o 的所有字符串里把 old 换成 new；返回 (新对象, 命中次数)。"""
    if isinstance(o, str):
        n = o.count(old)
        return (o.replace(old, new) if n else o), n
    if isinstance(o, list):
        tot = 0
        for i, v in enumerate(o):
            o[i], n = _sub(v, old, new); tot += n
        return o, tot
    if isinstance(o, dict):
        tot = 0
        for k in list(o):
            o[k], n = _sub(o[k], old, new); tot += n
        return o, tot
    return o, 0


def patch_data(A, B, C, D):
    R = {'A': A, 'B': B, 'C': C, 'D': D}
    out = []
    for route, nid, old, new in DATA:
        src = R[route]
        if nid:
            node = next((n for n in src['nodes'] if n['id'] == nid), None)
            n = _sub(node, old, new)[1] if node else 0
        else:
            n = _sub(src, old, new)[1]
        out.append(f'{"ok  " if n else "MISS"} ×{n} {route}/{nid or "*"} {old[:40]}')
    for route, nid, field, idx, key, val in SET:
        node = next((n for n in R[route]['nodes'] if n['id'] == nid), None)
        try:
            node[field][idx][key] = val; ok = True
        except Exception:
            ok = False
        out.append(f'{"ok  " if ok else "MISS"} set {route}/{nid}.{field}[{idx}].{key} = {val}')
    return out


def apply(page):
    report = []
    for old, new in POST:
        n = page.count(old)
        if n: page = page.replace(old, new)
        report.append(f'{"ok  " if n else "MISS"} ×{n} {old[:60]}')
    return page, report
