---
version: alpha
name: time-reckoning · 天文年历与黄铜
description: 第 6 题「时间的刻度」的风格简报。主轴量是「误差」——每个文明的历法与钟表都在和天上的非整数账目较劲；页面要让读者看见「差了多少、漂到哪去、怎么拉回来」。

colors:
  paper: "#F4EFE3"        # 浅色底：《航海天文年历》米白纸
  paper-2: "#FBF8F0"      # 卡片面
  ink: "#1B1A17"          # 墨线、正文
  ink-2: "#4A4639"        # 次级文字
  muted: "#7D7768"
  line: "#CFC8B5"
  line-2: "#E3DDCC"
  grid: "rgba(27,26,23,.07)"
  brass: "#B8862B"        # 唯一强调色：黄铜（指针、当前章、被选中的城市与刻度、闰）
  brass-ink: "#8A6318"    # 黄铜在浅底上的可读版本（文字用）
  wash: "rgba(184,134,43,.10)"
  wash-2: "rgba(184,134,43,.20)"
  night: "#0E1726"        # 深色底：天文台夜空
  night-2: "#14203A"      # 深色卡片面
  night-ink: "#EDE6D3"    # 深色下的米白线与字
  night-line: "#2A3650"
  night-brass: "#D9A441"  # 深色下的黄铜（更亮）

typography:
  heading: Noto Serif SC 700/900（站点固定，不换）
  body: Noto Sans SC 400/500（站点固定，不换）
  numbers: tabular-nums；大数字 + 小单位 + 口径行三层（第 5 题的做法）
  mood: 「Academic/Archival」「Editorial Classic」一路——衬线标题、克制、像年历与星表，不像仪表盘
---

## 1. 氛围 Visual Theme & Atmosphere
一本摊开的《航海天文年历》放在天文台的桌上：米白纸、细墨线刻度、一枚黄铜指针。浅色模式是白天的桌面，深色模式是夜间观测室（深蓝底、米白线、黄铜更亮）。全页只有一种强调色。照片与文献扫描保留原色、不加滤镜（第 5 题教训）。

资源库对照（`claude/design-resource-library.md`）：主风格取 ui-ux-pro-max 的 **E-Ink / Paper**（纸感、高对比、少动效、读者长读）与 **Editorial Grid / Magazine**（非对称栏、拉引、章节分隔）各一半；**不要** Vintage Analog（褪色滤镜）与 HUD（霓虹），它们和「真实照片原色」「克制」相冲。

## 2. 色彩角色 Color Palette & Roles
- 底 / 面 / 墨 / 线 见 frontmatter；黄铜只用于：当前章与导航进度、舞台上的指针与被选中城市、泳道图里的「闰 / 跳日」事件点、撞墙时的读数（撞墙用 `--brass` 加 `.hit` 抖动，不另引入红色）。
- 泳道九条文明不用九种颜色：全部墨线，靠行位置与图标区分；刻度（年 / 月 / 周 / 日 / 时 / 秒）用六档墨的深浅 + 形状（●年 ◐月 ◆周 ■日 ▲时 ▼秒），黄铜留给事件。
- 深色模式：`:root[data-theme=dark]` 与 `prefers-color-scheme` 两套覆盖；程序绘制的 SVG 一律用令牌取色。

## 3. 版式 Layout Principles
- 章回式长页骨架（版式规范）：卷首 → 吸顶导航 + 进度 → 0–7 章 → 卷末折叠。章号普通数字。
- 序章「对历与对表」复用第 5 题 `journey.py` 的固定舞台 + 滚动卡片：舞台是程序绘制的世界地图 + 12 城日期牌与表盘。
- 第 2 章用「地图 + 泳道图」左图吸顶、右文滚动；泳道图九行 × 分段比例尺（前 3000–0 压缩，1500–2027 放大），约 45 个点，可按刻度筛，点开出卡。
- 正文 760–820px 单栏；数字块三层（大数字 / 单位 / 口径）；每个节点卡默认只露「代表物、年代、一句话、误差」四样，其余折叠（`details.fold`）。
- 400px：舞台改上下叠（地图 ≤40vh），泳道图横向可滑，卡片单栏。

## 4. 深浅与层次 Depth & Elevation
无阴影；层次靠 1px 墨线边框与纸面双色（paper / paper-2）。悬浮层（节点详情）用 2px 墨线 + 纸面，不用毛玻璃。

## 5. 禁忌 Do's and Don'ts
- Do：尺度诚实（日期牌天数差按真实历差算；表盘分针差按真实经度差算；误差条按真实秒数算）；每个数字带口径行；文字折叠到演示下面；每面墙一个滑块 + 一个会「撞」的反馈。
- Don't：渐变、毛玻璃、圆角卡片海、三栏图标 + 标题 + 两行字的「AI 落地页」；程序绘制的具象物件（人物、器物）——只画地图、表盘、泳道、曲线、尺子；第二种强调色；10ⁿ 一类花哨编号；大表格（第 5 题矩阵被否）。

## 6. 交互母题 Interaction motif
「拨」：全页的交互都是拨一个东西看它漂——拨年份看春分漂、拨经度看正午漂、拨闰法看误差累积、拨城市看表盘差。撞到极限（季节漂出月份、μ 超限那种）就 `.hit`。音效默认关。

## 7. Agent Prompt Guide
Build a long-form, scroll-driven editorial page in the "nautical almanac on an observatory desk" mood: off-white paper (#F4EFE3) with thin ink rules (#1B1A17), a single brass accent (#B8862B) reserved for pointers, the current chapter, selected items and "leap/skip" events; dark mode = deep observatory blue (#0E1726) with cream lines and brighter brass. Fonts fixed: Noto Serif SC headings, Noto Sans SC body, tabular numerals. No gradients, no glass, no shadows, no second accent. Program-drawn graphics only for maps, dials, swimlanes, curves, rulers; real photos keep original colour. Every interactive element is a "dial something and watch it drift" demo with honest scale.
