---
version: alpha
name: winter-threshold · 灯油与夜
description: 第 7 题「冬天的门槛」的风格简报。主轴量是「黑夜的长短」——十五座城、二十一个节日落在同一道季节门槛上，页面要让读者看见「夜从北边压下来，灯一盏一盏点起来」，再看清哪一半来自纬度与气候、哪一半来自历法与传播。

colors:
  bg: "#0B0E17"             # 深色底：入冬的夜空（默认）
  surface: "#121626"        # 卡片面
  surface-2: "#1A2033"
  ink: "#F1EADB"            # 米白字（灯下的纸）
  ink-2: "#C9C2B2"
  muted: "#8E8A80"
  line: "#2A3047"
  line-2: "#1E2436"
  accent: "#F2A33A"         # 唯一强调色：灯油的焰色（点亮的城、当前章、被选中的节日）
  accent-2: "#E0611C"       # 焰心（篝火、焰底的暖橙）
  accent-ink: "#F6B85C"     # 深底上可读的焰色（文字用）
  wash: "rgba(242,163,58,.12)"
  night-0: "#070A12"        # 田野与昼带里「最黑的夜」
  night-1: "#2B3458"        # 夜与昼之间的靛蓝
  day: "#C9D3E6"            # 「白昼」的淡青：夜的田野里的亮区、昼带的亮段
  light-bg: "#ECEDF0"       # 浅色模式（白天读）：灰白纸；强调色换成烧过的橙 #D9661F / 文字 #B4511A
  light-ink: "#1C2030"

typography:
  heading: Noto Serif SC 700/900（站点固定，不换）
  body: Noto Sans SC 400/500（站点固定，不换）
  numbers: tabular-nums；大数字 + 小单位 + 口径行三层（第 5、6 题的做法）；昼长一律「9 小时 37 分」或「9h37m」
  mood: 「Dark Editorial」+「Observatory」——夜空、灯、米白衬线；像一张夜间卫星图配一本田野笔记，不像仪表盘，也不像万圣节海报
---

## 1. 氛围 Visual Theme & Atmosphere
深秋的夜里从高处看地球：NASA「黑色弹珠」的夜光图是底，米白的衬线字是灯下写的笔记，唯一的颜色是灯油的焰色。页面默认是夜（这一题的主角就是夜的长短），右下角「夜 / 昼」可切到白天读的灰白纸，但卷首的「夜的田野」和序章的舞台永远是夜（`.band`）。照片与文献扫描保留原色、不加滤镜。

资源库对照（`claude/design-resource-library.md`）：主风格取 ui-ux-pro-max 的 **Dark Mode / Observatory**（深底、单一暖色、数据图优先）与 **Editorial Grid / Magazine**（章回、非对称栏、拉引）；参考了 frontend-design 的「一个主视觉统摄全页」、dataviz 的「同一套令牌画所有图、深浅两套都要能读」、artifact-diagramming 的「只画能解释机制的图」。**不要** Vintage Analog（褪色滤镜）、HUD（霓虹）、万圣节的紫黑橙三色。

## 2. 色彩角色 Color Palette & Roles
- 底 / 面 / 墨 / 线见 frontmatter；焰色只用于：点亮的城（序章地图上的灯、昼带里的灯点与主城行）、当前章与导航进度、年轮上被选中的节日、「异」卡的边、规则卡顶上的一道火线、按钮。
- 夜与昼是第二套「量的颜色」而不是第二种强调色：`night-0 → night-1 → day` 三段渐变只出现在「夜的田野」底图、序章地图的纬度夜带、昼带的亮段、墙①的昼长曲线——它们表示的是同一个量（黑夜占一天的几分之几）。
- 曾经点亮、这一步不亮的城用 `accent-2`（更暗的橙，无光晕）；没点过的城是灰点。
- 浅色模式：`:root[data-theme=light]` 覆盖一套令牌（强调色换成 #D9661F），程序绘制的 SVG 一律用令牌取色；夜的田野与舞台不随模式变。

## 3. 版式 Layout Principles
- 章回式长页骨架（版式规范）：卷首 → 吸顶章节导航 + 进度 → 0–7 章 → 卷末折叠。章号普通数字。
- 卷首：标题 + 三段读法 + **「夜的田野」**（横轴 10/1→12/31、纵轴北纬 62°→南纬 36°、底色是黑夜长短、等昼长线 8/10/12/14 小时、二十盏灯按日期与纬度落位、虚线框出这十天）。这张图是全页的主视觉，封面从这里截。手机上画布改 720×600，只给十二个主要节日写名字。
- 序章「这十天」：左边固定舞台 = 会推镜头的夜光地图（每一步把点亮的城框进来，最少看 110° 经度；标签按像素避让）+ **昼带**（十五城按纬度从北到南，每行一条 0–24 时的轨道，亮段是白昼，主城行用焰色）；右边八张滚动卡片。手机上舞台上下叠，昼带排成两列。
- 第 2 章：左图吸顶的**年轮**（环心偏右，二十一个节日的标签在两侧排成扇出的列、引线连到环上的点——十七个节日挤在 40° 弧里，径向标签必叠字）；右边四条泳道的节点卡。
- 第 3 章：十九行的对照条（纬度游标、昼长条、气候带、门槛、历法、传播，可按列排序）；下面「同：五件事」每条带一条 19 格的华夫条（几行有），「异：四根轴」每条带证据链接。
- 第 5 章两面墙并排；第 6 章三个工具竖排；第 7 章十一份文件排成三列卡（顶上一道火线）。
- 400px：序章舞台 ≤36vh + 两列昼带；对照条横向可滑；年轮字号按容器宽度在 JS 里定。

## 4. 深浅与层次 Depth & Elevation
无阴影（只有灯的光晕与焰色文字的 text-shadow）；层次靠 1px 线框与 surface / surface-2 双面。悬浮层（田野的提示框）用 1px 线 + surface。

## 5. 禁忌 Do's and Don'ts
- Do：尺度诚实（昼长按太阳赤纬与均时差算、各城标准时；昼带的亮段位置就是日出日落；年轮上的点就是 2026 年的日子；华夫条的格数就是表里数出来的行数）；每个数字带口径行；文字折叠到演示下面；灯只在「有节的那天」亮。
- Don't：渐变背景、毛玻璃、圆角卡片海、三栏图标 + 标题 + 两行字的「AI 落地页」；程序绘制的具象物件（南瓜、灯笼、骷髅）——只画地图、曲线、年轮、轨道、华夫格；第二种强调色；紫色；把万圣节做成主角（它只是二十一行里的一行）。

## 6. 交互母题 Interaction motif
「点灯」：全页的交互都是让一盏灯亮起来看它在哪——滚到哪一天，那天的城就亮；卡片滚过中线，年轮上那个点就亮；拖纬度，那条纬线附近的节日就亮；转年轮，别家的岁首转到顶上；选两个节日，并排看同与异。亮的永远是焰色，别的都退成灰。

## 7. Agent Prompt Guide
Build a long-form, scroll-driven editorial page in the "night satellite image with a lamplit field notebook" mood: default dark (#0B0E17) with cream serif type (#F1EADB) and a single lamp-flame accent (#F2A33A) reserved for lit cities, the current chapter, selected festivals and buttons; a separate night→indigo→pale-day ramp (#070A12 → #2B3458 → #C9D3E6) encodes one quantity only, the fraction of the day that is night. Light mode = grey-white paper (#ECEDF0) with a burnt-orange accent (#D9661F); the hero field and the prologue stage stay night in both modes. Fonts fixed: Noto Serif SC headings, Noto Sans SC body, tabular numerals. No gradients as decoration, no glass, no shadows except lamp glow, no second accent, no purple. Program-drawn graphics only for the night field, the world map camera, the year wheel with fanned-out labels, day-length tracks and waffle strips; real photos keep original colour. Every interactive element is "light a lamp and see where it sits", with honest scale.
