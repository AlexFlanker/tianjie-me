# 第 8 题「蝾螈的几何：选区怎么画、席位怎么分、公平怎么量」· 研究共用简报（2026-11-06）

站点 tianjie.me「一周一题」，作者天杰。本题入口是 2026-11-03 美国中期选举，但**天杰明确要求不碰时政**：正文讲「代表权的几何与算术」——选区怎么画（gerrymander）、席位怎么分（apportionment）、公平怎么量（metrics）。横向约 25 个政体，纵向从前 508 年到 2026。

## 硬规则（每一路都要遵守）
1. **中立**：不写谁得利、不写胜负、不评价任何政党或人物；党名只能作事实主语（如「某州议会 2025 年通过新地图」），法院判决引判决要件与原文；不用「操纵」「黑幕」这类评价词，用「划区」「重划」「不成比例」。预测与民调只写统计方法，不评价任何模型或机构。
2. **来源**：每条事实 ≥2 个来源，优先官方 / 一手（法院判决全文、法律条文、政府与选举委员会官网、普查局、学术论文、权威通史）；维基只作线索。每条标 `confidence`：高 = 一手官方或学术；中 = 可靠二手（大报、大学）；低 = 通行说法。有分歧写进 `dispute` 并列两说，不下结论。
3. **日期与数字**：不凭记忆写；核不到的标 `"verify": true` 并在 `note` 写缺什么。数字写口径（年份、来源的统计口径）。
4. **先写骨架再核**：先把全部条目用占位写进 JSON 文件落盘（每条至少 id、title_zh、year），再逐条补正文与来源；每补完 3–5 条就保存一次。最后一条回复只报文件路径、条数、未核项清单与用了几次搜索，不要把整份内容贴在回复里。
5. **搜索预算**：你这一路的 WebSearch 上限见各路简报（含子代理）；WebFetch 不限。云端 WebFetch 只能打开**搜索结果里出现过的网址**（直接给的网址多半被权限拦下，报 PROVENANCE_REQUIRED）——先搜再开。维基各域名常 429；supremecourt.gov、law.cornell.edu、census.gov、legislation.gov.uk、courts.go.jp 一般能开。
6. **不给编辑看的话别写进字段**（「本路」「不下结论」「页面不要写成」之类写到 `note` 字段，不写进 text）。中文简体；人名地名首次出现附原文；英文枚举值只用简报规定的值。
7. 文件路径：`/home/claude/repo/themes/2026-11-07-gerrymander-geometry/src/research/<file>.json`，UTF-8，`json.dump(..., ensure_ascii=False, indent=1)`。

## 共用枚举
- `who_draws`: legislature | independent-commission | court | executive | mixed
- `system`: smd（单席位多数制）| pr（比例代表）| mmp（混合比例）| parallel（并立混合）| stv | bloc（集选区 / 多席位）| other
- `pathology`: gerrymander | malapportionment | both | neither
- `lane`（时间轴泳道）: draw（画线）| count（数人头 / 分配）| measure（量尺）
