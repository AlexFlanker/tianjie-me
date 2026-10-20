# 一周一题 · tianjie.me

每周六更新一个题目：一张图、一个交互页面，讲清一件事。站点：https://tianjie.me

- `themes/` 每期一个文件夹（自包含单页 + meta.json + 封面）
- `hub/` 首页模板与站点信息（含 podcast_home / podcast_episode 模板）
- `podcast/episodes/` 播客每期一个文件夹（meta.json + notes.html + cover.png + audio/）→ 输出到 `/listen/`
- `static/` 原样复制到站点根的独立小页面
- `build.py` 生成 `public/`（Cloudflare Pages 构建命令）
- `queue.md` 选题池 · `WORKFLOW.md` 出题与发布流程

```bash
python3 build.py && python3 -m http.server -d public 8000
```

内容 © Tianjie Sun。地图数据来自阿里云 DataV GeoAtlas；字体 Noto Serif SC / Noto Sans SC（SIL OFL）。
