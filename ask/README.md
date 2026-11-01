# 问天杰 · Ask Tianjie（v0）

tianjie.me 上的个人 agent：`/ask/`。不需要账号。只用站上已经公开的材料回答，每一段都要标出处；材料里没有就直说没有；薪资、入职时间、工作身份、私事一律转给天杰本人（访客留邮箱）。

## 一次提问怎么走

1. **前置转交**：问题命中薪资 / 入职与到岗 / 签证与身份 / 私事 → 直接给转交说明（`HANDOFF`），不调模型，不扣次数。规则在 `ask/lib/policy.js` 的 `HANDOFF_RULES`。
2. **额度**：匿名访客每天 `ANON_DAILY` 次，按「IP + 盐 + 日期」的哈希计数，不存 IP；邀请链接（签名 token）每天次数更多，回答时模型知道对方是谁请来的。
3. **上下文**：语料 `public/ask/index.json` 在构建时生成（现在 24 段，约 9K token）。语料小于 `FULL_CONTEXT_MAX_TOKENS` 时整份放进 system prompt 并开 prompt caching；超过后自动改成 BM25 取前 12 段 + 核心段。
4. **生成**：模型只许写 `[S3]` 这样的编号，不许写链接；链接由服务端按出处表加。
5. **检查**（`validateAnswer`）：剥掉模型写的 URL，删掉越界编号，找出没有出处的段落，然后给判定：

   | 判定 | 页面上 |
   |---|---|
   | `ALL_CITED` | 正常显示 |
   | `PARTIAL` | 显示，没有出处的段落标出来 |
   | `UNCITED` | 整段拦下不显示（「静默成功」） |
   | `NO_SOURCE` | 说明公开材料里没有，不编 |
   | `HANDOFF` | 转给天杰本人 |
   | `ERROR` | 报错，不扣次数 |

6. **回执**：每个回答下面一张回执：判定、引用了哪些出处、检查结果、模型、耗时、token、成本、语料版本、回执 id。

## 文件

| 路径 | 作用 |
|---|---|
| `functions/api/ask.js` | `POST /api/ask`（SSE 流）· `GET /api/ask` 状态 |
| `functions/api/contact.js` | `POST /api/contact` 访客留邮箱（每人每天 5 条） |
| `functions/api/admin.js` | `GET /api/admin?kind=log\|inbox\|stats`，需要 `ADMIN_TOKEN` |
| `ask/lib/policy.js` | system prompt、转交规则、引用检查 |
| `ask/lib/providers.js` | Anthropic / OpenAI 兼容 / 演示模式，价格表 |
| `ask/lib/auth.js` | 邀请 token、访客哈希、KV、Turnstile |
| `ask/lib/text.js` | 分词（与 Python 版一致）、BM25 |
| `ask/ask_corpus.py` | 构建语料、`/ask/`、`/ask/cards/`，追加 sitemap 和 llms.txt（`build.py` 末尾调用） |
| `ask/aliases.json` | 中文页面的英文关键词，让英文提问也能检索到 |
| `ask/cards/*.md` | 判断卡（`status: draft` 不上线） |
| `ask/evals/questions.jsonl` | 33 条评测题 |
| `ask/test/` | 单元测试；`mock_anthropic.mjs` 是本地假 Anthropic API |
| `hub/ask.html` · `hub/ask_cards.html` | 页面模板 |
| `tools/ask_invite.py` · `ask_admin.py` · `ask_eval.py` | 发邀请链接 · 看留言和日志 · 跑评测 |

## 上线步骤（Cloudflare Pages）

Preview 和 Production 是两套配置，要分别设。先在 Preview 跑通评测，再合并到 main。

1. **API key**：在 Anthropic Console 给网站单独建一个 workspace 和 key，并设月度 spend limit（几美元足够，见下面成本）。公开给访客用的 agent 必须走 API key，不能用个人的 Claude 订阅：Agent SDK 文档写明第三方产品不能用 claude.ai 登录或订阅额度。
2. **KV**：Workers & Pages → KV → 新建 namespace（比如 `ask-tianjie`；Preview 可以另建一个）。Pages 项目 → Settings → Bindings → 添加 KV namespace，变量名 **`ASK_KV`**。不绑也能跑，但计数和日志只在单个实例内存里，形同没有。
3. **变量**：Pages 项目 → Settings → Variables and Secrets。

   | 名称 | 类型 | 必需 | 说明 |
   |---|---|---|---|
   | `ANTHROPIC_API_KEY` | Secret | 上线必需 | 没有它就是演示模式：拼接最相关的两段材料，页面标明「演示模式」 |
   | `INVITE_SECRET` | Secret | 推荐 | 邀请链接的签名密钥；换掉它，所有旧链接作废 |
   | `ADMIN_TOKEN` | Secret | 推荐 | 读日志和留言；不设则 `/api/admin` 返回 404 |
   | `IP_SALT` | Secret | 推荐 | 访客哈希的盐；默认值写在代码里，务必改 |
   | `ANON_DAILY` | 文本 | 否 | 匿名每天次数，默认 5 |
   | `INVITE_DAILY` | 文本 | 否 | 邀请 token 没写额度时的次数，默认 30 |
   | `ASK_MODEL` | 文本 | 否 | 默认 `claude-haiku-5-5` |
   | `ASK_PROVIDER` | 文本 | 否 | `anthropic` / `openai` / `mock`；不设则按有哪个 key 自动选 |
   | `OPENAI_COMPAT_API_KEY` · `OPENAI_COMPAT_BASE_URL` | Secret · 文本 | 否 | 任何 OpenAI 兼容接口（默认 OpenRouter），模型用 `ASK_MODEL` 指定 |
   | `FULL_CONTEXT_MAX_TOKENS` | 文本 | 否 | 整份语料进上下文的上限，默认 60000 |
   | `NOTIFY_WEBHOOK` | Secret | 否 | 有人留邮箱时 POST `{text, content}`（Slack / Discord 兼容） |
   | `TURNSTILE_SITE_KEY` + `TURNSTILE_SECRET` | 文本（构建时）+ Secret | 否 | 只对匿名访客开 Turnstile 人机验证；site key 在构建时写进页面，改了要重新部署 |
   | `ANTHROPIC_BASE_URL` | 文本 | 否 | 只用于本地测试（指向假 API） |

4. **推分支 → 预览部署**，打开 `https://<分支>.<项目>.pages.dev/ask/`，状态行应显示模型名而不是「演示模式」。
5. **跑评测**（下面「评测」一节），全部通过后合并 main。
6. 上线后第一周每天看一眼 `tools/ask_admin.py stats` 和 `log`。

## 日常

**发邀请链接**（给招聘方或内推人，次数多，页面上显示对方称呼）：

```bash
INVITE_SECRET=... python3 tools/ask_invite.py --label "Acme · Jane（招聘）" --days 30 --quota 30
# → https://tianjie.me/ask/?i=<token>
```

token 不存在服务器上，过期自动失效；想全部作废就换 `INVITE_SECRET`。

**看留言、日志、统计**：

```bash
ADMIN_TOKEN=... python3 tools/ask_admin.py inbox
ADMIN_TOKEN=... python3 tools/ask_admin.py log --limit 20
ADMIN_TOKEN=... python3 tools/ask_admin.py stats          # 各判定数量、成本、平均耗时
# 预览环境加 --base https://<分支>.<项目>.pages.dev
```

**加判断卡**：在 `ask/cards/` 新建 `<id>.md`，front matter 写 `id / title_zh / title_en / status / see / updated`，正文四节：结论、成立条件、不能推出、回答前先问清。`status: published` 才进语料和 `/ask/cards/`。现在有两张草稿等天杰写：`no-silent-success.md`（五条原则的成立条件和不能推出）、`receipts.md`（等仓库或作品页公开后再发）。

**英文检索**：新主题在 `meta.json` 里加 `keywords_en`（只翻译标题、副标题、标签）；其他页面在 `ask/aliases.json` 里加。

## 评测

```bash
TOKEN=$(INVITE_SECRET=... python3 tools/ask_invite.py --label eval --quota 300 --days 1 | sed 's/.*?i=//')
python3 tools/ask_eval.py --base https://<分支>.<项目>.pages.dev --invite "$TOKEN" --out /tmp/ask-eval.json
```

33 题：22 道应有出处的回答（指定应引用哪一段）、5 道应转交、5 道应拒答（无关问题、提示词注入、站上没写的事）、1 道不限。演示模式下只检查转交和检索，当前结果 27 通过、6 跳过（要真模型才能判）。接上真模型后应全部通过；`PARTIAL` 记为警告。

## 本地开发

```bash
python3 build.py
node --test ask/test/lib.test.mjs                    # 9 项：分词与 Python 一致、BM25、引用检查、转交、邀请、成本

# 演示模式（不要模型 key）
npx wrangler pages dev public --port 8788 --compatibility-date=2026-10-01 \
  --kv ASK_KV --binding INVITE_SECRET=s3cret --binding ADMIN_TOKEN=adm-local

# 不花钱走一遍真实调用路径：假 Anthropic API 记录请求、按问题返回各种判定
node ask/test/mock_anthropic.mjs 8799 /tmp/last-request.json
npx wrangler pages dev public --port 8788 --compatibility-date=2026-10-01 \
  --kv ASK_KV --binding INVITE_SECRET=s3cret --binding ANTHROPIC_API_KEY=test \
  --binding ANTHROPIC_BASE_URL=http://127.0.0.1:8799
```

wrangler 用 `npx` 临时跑，不要在仓库根目录加 `package.json`（Pages 构建会因此去装 npm 依赖）。

## 成本

Haiku 5.5 官方价（2026-10-31 查）：输入 $0.10、输出 $0.50、缓存读 $0.01、缓存写 $0.125，均为每百万 token。每次回答约 9K token 语料 + 几百 token 问答：

- 5 分钟内有人问过（缓存命中）：约 $0.0003 / 次
- 冷启动（写缓存）：约 $0.0012 / 次

一个月 1000 个问题大约一两美元（上面的 token 数是构建时估算，实际以回执为准）。回执里的 `cache_read` 不为 0 就说明缓存生效。价格变了改 `ask/lib/providers.js` 的 `PRICES`。KV 免费额度每天 1000 次写，每个问题写 2 次，够每天约 500 问。

## 数据与隐私

- 存：问题原文、语言、访问方式、邀请称呼、回执，30 天；留言（邮箱和内容），180 天；每日计数（访客哈希），2 天。
- 不存：IP、cookie、账号。
- 语料只有网站上已经公开的页面和已发布的判断卡。备考资料、在职公司内部信息、草稿都不进。

## 已知限制和下一步

- 只做单轮问答，不带上下文追问。
- 引用检查只查「有没有标出处」，不查「出处是否真的支持这句话」。下一步：用便宜模型对每段做一次支持度检查，或每周抽查日志。
- KV 计数不是原子的，并发时可能多给一两次，可以接受。
- 之后可加 A2A agent card（`/.well-known/agent-card.json`），让别人的 agent 也能来问。
