# 第 7 题 · 冬天的门槛 · 工作日志
- 2026-10-27：周二选题扫描（定时任务）给出 A/B/C，天杰选 A 并加要求：按经纬度、气候、地理条件做「相似时间的节日」的异同分析；随后要求「仔细看所有网页设计 skills，结合主题重做一套视觉升级的页面」，交互会话（session_01XSyXLS5qb3L6h9cqoC6WdC）当天接手，不等周五任务。皮肤三选一，天杰选「A 灯油与夜」。
- 研究四路（A 欧洲与南半球 / B 中国与日本 / C 南亚与东南亚 / D 中美洲与十五城气候），每路 ≤25 次搜索，底稿在 research/fest_*.json；图片三路在 research/images_*.json → src/images.json（42 张，全部 PD / CC0 / CC BY / CC BY-SA / 无已知限制）。
- 天文表：python3 themes/2026-10-31-winter-threshold/src/tools/tables.py（PyEphem）→ src/tables.json：立冬 / 小雪 / 冬至（视黄经）、排灯节（amanta 阿湿缚庾阇月朔 + 德里日落 tithi + pradosh / nishita 规则，2015–2027 与印度中央政府假日表全部一致）、各年望。农历月表沿用第 6 题 lunar_table.json（GB/T 33661 口径）。
- 重建：python3 themes/2026-10-31-winter-threshold/src/build_theme.py && python3 tools/cover.py themes/2026-10-31-winter-threshold && python3 build.py
- 视觉：卷首「夜的田野」（canvas 底 + SVG 灯）；序章舞台 = NASA 黑色弹珠夜光图 + 推镜头（viewBox 补间）+ 像素级标签避让 + 昼带；年轮改扇出标签（app.js wheelLabels，按容器宽度定字号，墙②转动后重排）；同与异加 19 格华夫条；第 7 章改三列文件卡。
- 自检：Playwright 1280 深 / 浅、400 深整页截图与分节截图；无控制台错误、无横向溢出、无缺图。
