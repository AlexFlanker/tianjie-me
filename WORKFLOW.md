# 一周一题 · 出题流程

节奏：**每周六早上上线**。周五晚上由定时任务生成当周题目并发预览；Tianjie 看过回一句"发"，再合并上线。

## 仓库约定

```
themes/<YYYY-MM-DD>-<slug>/
  index.html     自包含单页（内联 CSS/JS，图片用 data: 或放 assets/），完整 HTML 文档，lang=zh-CN，含 <title>/description/OG
  meta.json      {no, slug, title, subtitle, date, summary, tags[], format, reading_time, sources[], cover_focus?}
  cover.png      1200×630 封面 / 分享图（tools/cover.py 生成）
  src/           可选：模板、数据、生成脚本（便于以后改内容重建）
hub/             首页模板、站点信息（site.json：名称、长期专题）、_headers、_redirects、404
build.py         生成 public/（顶栏注入、首页、feed、sitemap）；Cloudflare Pages 用 `python3 build.py` 构建，输出目录 public
queue.md         选题池
```

- 日期用发布日（周六）。`no` 递增；`draft: true` 的主题不会进入首页与 feed（可先合并再上线）。
- 页面要在手机（~400px）可用，深浅色都可读，出处标在页面里；地图类页面按现行行政区划绘制。
- 顶栏由 build.py 注入，主题页面本身不要再画站点导航。

## 每周流水线（定时任务执行）

1. **选题**：读 `queue.md`「待做」第一条（若当周有指定则用指定的），决定格式。
2. **研究**：联网检索，收集事实、数据与一手出处；数据类主题把原始数据存到 `src/`。
3. **构建**：写 `index.html`（单文件），`meta.json`，运行 `python3 tools/cover.py themes/<dir>` 生成封面，运行 `python3 build.py` 确认构建通过。
4. **核查**：派一个子代理逐条核对年代、数字、引文；桌面 / 手机 / 深色各截一张图检查布局；修正后更新 `sources`。
5. **预览**：提交到分支 `draft/<slug>` 并推送（Cloudflare 会给分支预览地址）；如果这个会话没有推送权限，就把主题打包成 zip 放到会话输出，并把页面发布成 Claude Artifact 作为预览。
6. **通知**：把预览链接、一句话摘要、核查中发现的争议点发给 Tianjie，然后等待。
7. **发布**：收到"发"之后合并到 `main`（或推送 main），把 `queue.md` 里的条目移到「已完成」，确认 https://tianjie.me/ 首页已更新；收到修改意见就改完再发预览。

## 本地操作

```bash
python3 build.py                                  # 生成 public/
python3 -m http.server -d public 8000             # 本地预览 http://localhost:8000
python3 tools/cover.py themes/<dir>               # 生成封面（需要 playwright）
python3 themes/2026-09-21-cuisine-atlas/src/build_theme.py   # 重建第 1 题
```

## 部署

- Cloudflare Pages 项目 `tianjie-me` 连接本仓库：Build command `python3 build.py`，Build output `public`，生产分支 `main`；push 即部署，其他分支自动生成预览地址。
- 自定义域名：`tianjie.me`、`www.tianjie.me`。旧的 `cuisine.tianjie.me` 301 到 `/t/cuisine-atlas/`；`phototour.tianjie.me` 是独立项目（带 Functions），作为长期专题收录。
