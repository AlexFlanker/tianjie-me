# -*- coding: utf-8 -*-
"""核查后的改正集中在这里。构建时逐条报告是否命中。
POST：对成品 HTML 做「旧串 → 新串」替换（每条应恰好命中 ≥1 次）。
PATCH：对案例字段打补丁 (case_id, "路径", 新值)，路径如 "origin.text_zh"、"chain.1.year"、"facts.0"。
DROP：不上页面的案例 id。"""
POST = [
]
PATCH = [
    # 编辑阶段（合成前）
    ("left-pad", "lag.days", 0.104),          # 2.5 小时
    ("crowdstrike", "lag.days", 0.054),       # 04:09 推送到 05:27 撤回，约 78 分钟
    ("crowdstrike", "lag.text_zh", "推送后几分钟内开始蓝屏，78 分钟后撤回，当天波及全球"),
    ("mauve", "dispute", "珀金最初想把两分子烯丙基甲苯胺缩合成奎宁，这条路失败后才改用苯胺。「偶然」说的是结果；他认出这团紫色有用、申请专利并办厂，则不是偶然。"),
    ("mpesa", "origin.place_zh", "非洲三个国家（Gamos 的调查）"),
    ("container", "chain.2.year", 1965),
    ("container", "chain.2.text_zh", "标准之争拖了约十年。1960 年代中期，麦克莱恩同意同行免费使用海陆公司的专利，角件和 40 英尺的长度才统一下来。"),
]
DROP = [
]
