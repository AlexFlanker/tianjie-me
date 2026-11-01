---
id: how-pages-are-made
title_zh: 一周一题是怎么做出来的
title_en: How the 一周一题 pages are made
status: published
see: /how/
updated: 2026-10-31
---
## 结论 · Answer
每一题都走同一条流水线：定时任务从选题池取题；主代理写一份所有研究员共用的简报；四路研究代理按预算联网检索，每个数字带来源和置信度；主代理按风格简报构建单页；另一个没参与写作的代理逐条核查；推到预览分支后，由天杰本人看过、说「发」才上线。

Every page goes through the same pipeline: a scheduled task picks the topic from the queue; a lead agent writes one shared research brief; four research agents search within a budget and record a source and a confidence level for every number; the lead agent builds the page from a style brief; a separate agent that did not write it checks every claim; the preview goes to Tianjie, and nothing ships until he says go.

## 成立条件 · Holds when
描述的是 /how/ 页写明的流程，研究底稿、工作日志和风格简报都在公开仓库里。

This is the process documented on /how/; briefs, research files and work logs are in the public repository.

## 不能推出 · Does not imply
不等于每个事实都绝对正确。页面列出处，欢迎指正。

It does not mean every fact is guaranteed correct; sources are listed so readers can check, and corrections are welcome.

## 回答前先问清 · Ask first
对方关心的是 AI 的分工、核查方法，还是工程实现。

Whether the visitor cares about the division of work between AI and the human, the checking method, or the engineering.
