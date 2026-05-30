# NousResearch Hermes Agent v0.15.0 "The Velocity Release"：当 16,000 行函数变成 14 个模块

> 项目：https://github.com/NousResearch/hermes-agent | 173K Stars | MIT License
> 版本：v2026.5.28 "The Velocity Release" | 390 Contributors

---

## 核心命题

Hermes Agent 这次的 release 解决了一个在 Coding Agent 领域被长期忽视的问题：**当一个 Agent 系统变得越来越大，它的冷启动速度和每次对话的函数调用数会成为真实的使用摩擦**。这次 refactor 让 run_agent.py 从 16,083 行压到 3,821 行（-76%），同时冷启动时间再降一秒，per-turn 函数调用数降低 47%——这不是小修小补，而是一次针对「Agent 工程债务」的手术。

**笔者认为**：Hermes 的方向代表了一种正在形成共识的工程哲学——**Coding Agent 的竞争已经从前沿模型能力层面下沉到「让模型跑得更稳、更快、更省」的执行层优化**。当所有框架都能调用 GPT-4o 或 Claude 3.7 时，差异化变成了：你的 Agent 启动要几秒？每次对话花多少 token？上下文增长时性能会不会退化？

---

## 一、The Big Refactor：16,083 行到 3,821 行

### 怎么做到的

run_agent.py 是 Hermes 的核心——它管理整个 Agent 对话循环。在 v0.15.0 之前，这个文件有 16,083 行，包含了 Agent 的所有核心逻辑。

重构后：
- 代码行数：16,083 → 3,821（**-76%**）
- 提取到 14 个内聚的 `agent/` 模块下
- 每个提取都保留了 `AIAgent` 上的 thin forwarder，保持向后兼容
- 所有外部调用者无需修改

官方公告中特别强调了为什么这很重要：
> *"The file that took 90 seconds to load in your editor opens in a blink. Future Hermes development moves faster, plugin authors can finally grep the codebase."*

**这不是普通的代码清理**。16k 行的单文件在 Python 环境中本身就意味着性能损耗——每次 import 都会加载整个文件。拆分成模块后，初始化变成按需加载，冷启动自然快了起来。

### session_search 的并行优化

另一个值得关注的重构是 `session_search`：

| 版本 | 方式 | 速度 | 成本 |
|------|------|------|------|
| 旧版 | 辅助 LLM，每次调用 ~$0.30 | ~90s（3 个 session 摘要）| 每调用收费 |
| 新版 | FTS5 + 无 LLM | ~20ms（discovery）/ ~1ms（scroll）| **免费** |

这是一个典型的「消除不必要的复杂」案例：用 LLM 去做 session 搜索本质上是杀鸡用牛刀，FTS5 全文搜索加上结构化元数据就足够解决 99% 的场景。新版让 session 搜索从「需要等 90 秒的有成本操作」变成「即时的零成本操作」。

---

## 二、冷启动优化：让 Agent 真正可以「随用随开」

### 五轮优化压下来的性能

v0.15.0 包含五轮独立的冷启动优化，最终效果：

| 指标 | 优化前 | 优化后 | 改善幅度 |
|------|--------|--------|----------|
| Termux 冷启动 | 2.9s | 0.8s | -72% |
| `hermes --version` | 701ms | 258ms | -63% |
| Per-turn 函数调用（31-turn chat）| 399k 次 | 213k 次 | -47% |
| 单次 tool call 开销 | — | -195ms | — |
| 每次 CLI 调用 | — | -240ms / -17MB | — |

这五轮优化的策略各不相同：
- **defer openai._base_client import**：解决的是 Python 冷启动时的大头导入问题，-240ms/-17MB
- **hot-path 函数调用数削减**：从 399k 降到 213k，等效于把单次对话的 token 消耗降低了 47%
- **adaptive subprocess polling**：优化的是 tool call 的等待开销，每次 -195ms
- **compression-feasibility check deferral**：170-290ms 发生在每次 Agent 构造时，现在推迟

###  benchmark 翻转

值得注意的是，优化后的 `hermes --version` 在 head-to-head benchmark 中**从 5/11 输 Codex CLI 变成 6/11 赢**——这意味着在 CLI 工具这个层面，Hermes 已经是有竞争力的选择，而非仅仅是「功能丰富」的选择。

---

## 三、Multi-Agent 进 Kanban：从工具到平台

v0.15.0 中，Kanban 进化成了一个真正的 multi-agent 平台，新增功能包括：

- **Orchestrator auto-decomposition**：Orchestrator 自动将任务分解为子 Kanban
- **Swarm topology**：Swarm 从 v1 进化，支持图结构
- **Worktree-per-task**：每个任务有独立的 git worktree
- **Per-task model overrides**：不同任务可以指定不同模型
- **Scheduled tasks**：支持定时任务

这个进化的方向是把「单一 Agent 执行」扩展成「多 Agent 协作编排」。在 multi-agent 成为行业共识的背景下，Hermes 的 Kanban 路线选择一个相对独特的切入方式——**用看板的隐喻来处理 multi-agent 任务分配**，而不是用更抽象的 orchestrator/DAG 结构。

**笔者认为**：看板隐喻的优势在于降低了多 Agent 协作的认知门槛——用户不需要理解复杂的 DAG 或流程图，只需要理解「有一个任务列表，每个任务由哪个 Agent 处理」。这让 Hermes 的多 Agent 功能对非技术用户更友好。

---

## 四、安全进化：Promptware Defense + Bitwarden Secrets Manager

### Promptware Defense

Hermes 新增了对「Brainworm 类攻击」的防御。Brainworm 是一种 Prompt injection 攻击类型，攻击者通过在对话中注入恶意指令来劫持 Agent 行为。Hermes 的 Promptware defense 应该在输入层做了类似「内容过滤 + 意图隔离」的机制，但具体实现细节需要看源码才能确认。

### Bitwarden Secrets Manager

旧版 Hermes 每个 provider（OpenAI、Anthropic、xAI 等）都需要独立的 API key 配置。v0.15.0 引入 Bitwarden Secrets Manager，可以用**一个 bootstrap token** 管理所有凭据。

这个设计解决了两个问题：
1. **多 key 管理混乱**：每个 provider 独立配置意味着用户需要维护 5-10 个不同的环境变量
2. **安全风险**：明文 API key 存储在环境变量或配置文件中是常见的安全隐患

统一通过 Bitwarden 管理后，变成了「一个主 key 解锁所有 provider」的模型，这和现代 DevOps 的 secret management 最佳实践是一致的。

---

## 五、生态集成：xAI 深度融合 + MCP Catalog

### xAI 全家桶

xAI 的集成在这版本非常深度：
- **Web Search 插件**：作为 Brave/Tavily/Exa/SearXNG/DDGS/Firecrawl 之外的又一个 Web Search 选项
- **OAuth proxy**：SuperGrok OAuth 可以通过本地 OpenAI-compatible endpoint 代理访问
- **May 15 模型退役检测**：自动检测 grok-4/grok-3 等已退役模型，并提供 `hermes migrate xai` 一键迁移
- **xAI TTS** with speech-tag pauses：自然停顿的语音合成
- **base_url leak guard**：封堵了一个 OAuth 凭据泄漏漏洞

### Nous-approved MCP Catalog

这是我觉得值得关注的一个功能：「经过 Nous 验证的 MCP 服务器目录」。用户运行 `hermes mcp` 可以进入一个交互式选择器，安装经过验证的 MCP server，并在一个交互式流程中配置凭据。

这个模式的价值在于：当前 MCP 生态最大的问题是**发现成本和信任成本**——用户不知道哪些 MCP server 是可信的、配置是否正确。Nous 的验证目录把这个过程简化了。

---

## 六、主题关联：与「Coding Agents in Social Sciences」的闭环

本文与前一篇 Article（Anthropic「Coding agents in the social sciences」实证研究）形成以下主题关联：

| 关联点 | 解释 |
|--------|------|
| **冷启动与采用率** | Anthropic 报告显示 81% 研究者用过 AI，但只有 20% 用 Coding Agent——低采用率背后可能有「工具上手摩擦」的问题。Hermes 把 Termux 冷启动从 2.9s 压到 0.8s，这种量级的优化会直接影响用户「愿不愿意用」 |
| **Per-turn 函数调用与 Token 成本** | Anthropic 报告揭示了研究者的一个担忧：AI 产出的 paper 数量在增加，但 journal submission 没有增加——这意味着「最后一公里」的验证/打磨仍然需要人。Hermes 把 per-turn 函数调用降低 47%，本质上是降低了每次迭代的成本，但没有解决「质量守护」的根本问题——这与 Anthropic 报告的发现高度呼应 |
| **Multi-Agent 与研究协作** | Hermes 的 multi-agent Kanban 进化与 Anthropic 报告中的「多 Agent 管线自动化社会科学研究」遥相呼应——两者都在探索「多 Agent 协作」如何落地，只是切入角度不同（Hermes 从工具实现角度，Anthropic 从采用研究角度）|

---

## 技术数据速览

| 指标 | 数值 |
|------|------|
| **Stars** | 173K（全球 #38） |
| **Contributors** | 390 |
| **最新版本** | v2026.5.29.2（2026-05-29）|
| **主要语言** | Python（89%）|
| **License** | MIT |
| **运行 Agent 文件行数减少** | -76%（16,083 → 3,821）|
| **Termux 冷启动** | 2.9s → 0.8s（-72%）|
| **Per-turn 函数调用减少** | -47%（399k → 213k）|
| **session_search 加速** | 4,500×（90s → 20ms）|
| **MCP 支持** | Nous-approved catalog + 交互式 picker |
| **xAI 集成深度** | Web Search + OAuth proxy + TTS + 退役检测 + 安全加固 |
| **消息平台支持** | 23 个（含 ntfy）|

---

*推荐评分：⭐⭐⭐⭐⭐（173K Stars，工程质量突出，xAI 深度集成，multi-agent 平台化方向清晰）*
*项目地址：https://github.com/NousResearch/hermes-agent*
*官方文档：https://hermes-agent.nousresearch.com*