---
id: receipts
title_zh: Receipts：给 agent 的每一次写出回执
title_en: "Receipts: verifiable writes for AI agents"
status: draft
see: /work/receipts/
updated: 2026-10-31
---
<!-- DRAFT: publish after the repo and the /work/receipts/ page are public. -->
## 结论 · Answer
Receipts 是一个 MCP server 加验证层：agent 对外部系统的每次写操作都做写后读回校验、记录 diff，不一致就回滚，失败要大声报出来，而不是静默地报告"成功"。演示里 API 报告成功 8 次，实际验证通过 3 次，假成功率 62%。

An MCP server plus a verification layer that wraps every agent write: read-after-write checks, a recorded diff, rollback on mismatch, and a loud failure instead of a silent "success". In the demo, the API reported 8/8 successes; verification passed 3/8, a 62% false-success rate.

## 成立条件 · Holds when
TODO：演示数据来自 mock ATS / GitHub Issues，说明清楚环境。

## 不能推出 · Does not imply
TODO：不代表生产环境的假成功率。

## 回答前先问清 · Ask first
TODO。
