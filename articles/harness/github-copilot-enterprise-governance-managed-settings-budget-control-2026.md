---
title: GitHub Copilot Enterprise Harness Layer 4：managed-settings.json GA + Auto Model Selection CLI + AI Credit Session Limits
date: 2026-07-02
source: GitHub Blog
source_url: https://github.blog/changelog/2026-07-01-enterprise-managed-settings-json-is-generally-available
related_urls:
  - https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection
  - https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task
  - https://github.blog/changelog/2026-07-01-set-ai-credit-session-limits-in-copilot-cli-and-sdk
author: GitHub Blog (Release Changelog)
tags: [github-copilot, enterprise-governance, managed-settings, auto-model-selection, session-limits, budget-control, harness-extension, cost-control]
cluster: harness-governance/enterprise-policy/budget-control
pair_project: AgentBudget/agentbudget
---

> **核心论点**：2026-07-01 GitHub Blog 在同一天内连发四条公告 —— **Enterprise managed-settings.json GA**、**Enterprises can default to auto model selection**、**Copilot CLI auto model selection routes based on task**、**Set AI credit session limits in Copilot CLI and SDK**。如果只看每一条，都是单点功能 GA；但合并起来看，这是 GitHub 在 R616「Browser Surface + Consent Architecture (Layer 3)」之上，**把「企业级 AI Agent Harness」的四根支柱（Governance / Routing / Budget / Auditability）一次性铺到了 GA**。从「单开发者单客户端的 Copilot」到「企业范围内可治理、可观测、可计费的 Copilot」，是 Agent Harness 从 **Layer 3 (Browser Surface)** 向 **Layer 4 (Enterprise Harness)** 的范式跃迁。这一层的核心矛盾不再是「Agent 能不能触达一个新表面」，而是「**当 5000 个开发者同时跑 Agent 时，谁来管模型选型、谁能停掉失控的 session、谁能在出问题时拿到一份可信的账单**」。**AgentBudget/agentbudget**（Apache-2.0，105⭐）作为这条公告的「ulimit-for-AI-agents」开源对应物，恰好印证了这个层级的工程共识已经在 1st-party 和 OSS 两端同时收敛。

---

## 一、为什么 GA 是范式信号 ——「单点功能」与「Enterprise Harness Layer」的距离

2026 上半年 GitHub 在 Copilot 上做了很多事 —— 模型路由（HyDRA, R613）、浏览器 Surface（R616）、Managed Agents、Skill-as-Harness (R605/R611)。但所有这些都属于 **Layer 1-3**：

- **Layer 1（Model Routing）**：HyDRA routing + 94% cache hit（R613）
- **Layer 2（Agent Harness + Session）**：CLI chronicle + Session Harness + feedback loop
- **Layer 3（Browser Surface + Consent）**：真实浏览器 + Share with Agent + Tab 隔离 + 企业 allow/deny（R616）

但对于一家拥有 **5000 名工程师、跨多个业务线、需要在 4 个时区协作** 的企业来说，Layer 1-3 还远远不够 —— 这些层回答的是「单个开发者用 Copilot 时体验如何」，却没回答：

1. **「我们公司应该默认用哪个模型」** —— 之前每个开发者都得在 VS Code / CLI / github.com 三个 surface 上分别配置 model picker
2. **「我们公司能不能强制所有会话走 Auto（成本最优）而不是 Sonnet 5（贵但稳）」** —— 之前没有 enterprise 级的 model 策略入口
3. **「我们公司怎么防止某个 Agent session 把本月 AI credit 预算烧光」** —— 之前只有 enterprise-wide spending limit（事后告警），没有 session-level 软上限（事前预防）
4. **「我们公司能不能在 .github-private repo 里像配置 CI 一样配置 Copilot」** —— 之前需要 admin 在网页后台点几下

7/1 这四条公告一次性回答了上述四个问题。这就是 **「Layer 4: Enterprise Harness」** 的工程定义 —— 它不是一个新 feature 类别，而是**四类 feature 同时进入 GA 之后的范式涌现**。

---

## 二、managed-settings.json —— 把 Copilot 配置从「点击后台」变成「PR review」

> 原文引用："GitHub Enterprise Cloud customers can configure AI standards through a managed-settings.json file maintained in a .github-private repository in a selected organization. This allows the enterprise to define new governance and extensibility flows that apply to Copilot clients such as VS Code or Copilot CLI."

### 2.1 五个 Supported Keys 是企业 AI 治理的最小接口

GitHub 把企业 AI 治理压成了 **5 个 JSON 键**，这本身就是一个工程决策：

| Key | 治理维度 | 类比传统 IT |
|-----|---------|------------|
| `extraKnownMarketplaces` | Plugin 来源 allowlist | npm registry allowlist |
| `enabledPlugins` | Plugin 默认启用清单 | managed software install |
| `strictKnownMarketplaces` | 强制只允许已知 marketplace | AppLocker / Gatekeeper |
| `disableBypassPermissionsMode` | 禁止 Agent 跳过权限 | sudo restriction |
| `model` | 默认模型（含 `auto`） | default browser / default shell |

`workbench.browser.*` 之外，**`managed-settings.json` 是 GitHub 给企业 AI 治理的「最小可行接口（MVI, Minimum Viable Interface）」**。**笔者认为**，这 5 个 key 不是「现在能配的所有项」，而是 **「企业第一次开启 Copilot 治理时最常需要的 5 个开关」**——GitHub 把它们做出来 GA，证明 enterprise customer 已经在生产环境大规模撞到这 5 个维度。

### 2.2 「PR reviewable AI 治理」是新范式

> 原文引用："The configuration in managed-settings.json is in addition to the policies available in the AI Controls tab in enterprise settings. managed-settings.json takes precedence over file-based configuration set by users in their clients for the supported keys. The configuration is fetched from the server by Copilot every time a user authenticates, stored in memory, and refreshed hourly."

`managed-settings.json` 存放在 **`.github-private` 仓库** 中，这是 GitHub 给企业 AI 治理的最优雅的工程决策之一：

1. **可审计**：每次改动都是 git commit，PR reviewable
2. **可回滚**：`git revert` 即可撤销一条危险配置
3. **可追溯**：git blame 给出「谁在什么时间开了哪条 plugin」
4. **可继承**：组织 → 团队 → 个人，配置按层级覆盖

**笔者认为**，这是一个被低估的范式 —— **「AI 治理 = Code review」**。传统 IT 治理靠「管理员在控制台点几下」，出了事故只能查 audit log。**Code-reviewable AI 治理**让 CISO、CTO 和工程团队可以用同一套工具（git、PR、CI）来审计 Copilot 行为。这条范式比 R616 的 Browser Tools 企业 allow/deny 更深一层 —— 不是「运行时拦截」，而是「**配置即代码（Configuration as Code）**」。

### 2.3 「周期性 refresh」是企业治理的一致性保证

> 原文引用："The configuration is fetched from the server by Copilot every time a user authenticates, stored in memory, and refreshed hourly."

**每小时 refresh** + **登录时 fetch** + **存内存不落盘** 是三个独立的工程决策：

- **每小时 refresh**：CISO 推一条紧急策略 → 1 小时内全员生效（vs 传统 MDM push 几小时到几天）
- **登录时 fetch**：新员工入职第一天就有正确配置（vs 传统「开机后等策略下发」窗口）
- **存内存不落盘**：策略更新不留本地缓存副本（vs 传统 GPO 本地缓存可能导致策略过期仍生效）

**笔者认为**，这三个决策组合起来定义了 **「Harness 的治理一致性 SLA」** —— 从「策略变更」到「全员生效」的延迟不超过 1 小时。这与传统 IT 治理的「天级延迟」是天壤之别。

---

## 三、Auto Model Selection 的 CLI 实现 —— HyDRA routing 的工程闭环

> 原文引用："GitHub Copilot auto model selection now routes to the best model for your task in Copilot CLI, using utilization and model health metrics for a high quality, reliable, and token-efficient experience."

### 3.1 五个评估维度的工程含义

Auto model selection 不是「随机选模型」，而是 **五个维度同时评估**：

| 维度 | 工程含义 |
|------|---------|
| `reasoning` | 任务是否需要深度推理（数学 / 多步逻辑）→ 高推理模型 |
| `code generation complexity` | 代码生成复杂度（API glue / 算法 / 系统设计）→ 复杂模型 |
| `bug diagnosis difficulty` | 调试难度（单步 typo / 多模块 root cause）→ 强推理模型 |
| `tool orchestration needs` | 工具调用复杂度（单工具 / 多工具链）→ 工具强模型 |
| `real-time availability & reliability` | 模型当前可用性 + 健康度 → 跳过不健康模型 |

**「Auto is billed based on the model it selects, drawing down AI credits at each model's published rate. Paid subscribers get a 10% discount on model costs when using auto, so you consume 10% fewer AI credits than directly running the same model.」**

**笔者认为**，Auto 的 10% discount 是个**精心设计的激励结构** —— 它告诉用户「用 Auto 比手动选模型更便宜」，把「节约成本」和「降低决策负担」打包成同一个产品决策。这比 LangChain 时代的「自动模型选择库」要工程化得多 —— 后者只是一个 routing 函数，前者把 routing + 计费 + 模型可用性 + 健康度全栈集成。

### 3.2 「Cache boundary aware routing」是 2 月份那篇 arXiv 的工程落地

> 原文引用："Auto routes along natural cache boundaries to avoid unnecessary cache related costs. Our evaluations show gains in token efficiencies with no quality regression, as not all tasks require a high reasoning or token-intensive model."

这是 R613 那篇 `getting-more-from-each-token` 的 CLI 实现 —— 当时文章说「GitHub Copilot 的 HyDRA routing 知道 prompt cache 的边界，不会跨越 cache boundary 切模型」。**现在 CLI 也接入了 Auto routing，cache-boundary-aware 的策略从 Chat surface 扩展到了 CLI surface**。这意味着：

1. 同一个企业里，无论开发者用 VS Code 还是 Copilot CLI，**routing 策略一致**
2. 长 session 内 cache hit 率不再因为 surface 切换而失效
3. **Auto model selection 跨 surface 复用 cache**，这是 R613 HyDRA 的真正工程闭环

### 3.3 Enterprises can default to auto model selection —— 治理层压实

> 原文引用："Enterprise administrators can now set model to auto in the enterprise managed-settings.json to make Copilot auto model selection the default for new conversations."

把 `model: "auto"` 写到 `managed-settings.json` 里 —— 这是 **Layer 1 (Routing) × Layer 4 (Governance) 的交叉点**。一句话就把「企业所有新会话默认走 Auto」实施完毕，开发者仍然可以用 `/model` 命令手动覆盖。

**笔者认为**，这是 GitHub 在 R616 之后给出的**最有战略意义的工程信号** —— 它表明 GitHub **不希望企业把 model 锁定当成治理手段**，而是希望企业**把「自动选择最优模型」当成治理基线**。这是一种 **「anti-lock-in 治理哲学」**：把成本优化压到 default，把质量优化留给 Auto routing。

---

## 四、AI Credit Session Limits —— Harness 的 ulimit

> 原文引用："You can now set AI credit session limits in Copilot CLI and the GitHub Copilot SDK to cap the amount an agent spends in a session. Set a limit before you start work or kick off jobs, and Copilot tracks AI credit usage across the entire session, including model calls, subagents, and background work like compaction."

### 4.1 「软上限」的工程决策

> 原文引用："Session limits are a soft cap. Since usage is only known after a response returns, a response that's already underway finishes before Copilot stops, so actual usage may slightly exceed the number you set."

**Session limits 是 soft cap** —— 这是一个非常重要的工程决策。理由是 **「usage is only known after a response returns」**，所以**正在进行的 response 一定会跑完**。这意味着：

- **不会出现「response 跑了一半被砍掉导致 token 浪费 + 上下文不一致」**
- **实际花费可能略高于设定值**（因为最后一个 response 已经跑完）
- **不会有「atomic stop」导致的状态污染**

**笔者认为**，这个 soft cap 设计是 **「harness 治理 vs Agent 完整性」之间的精确平衡** —— 它承认 Agent 的最小执行单元是「一个完整的 response」，而不是「一个 token」。这与传统 Unix `ulimit` 的「hard cap 中断进程」是不同哲学 —— 后者是为了防止系统资源耗尽，前者是为了防止预算失控，但**两者都不能破坏执行单元的原子性**。

### 4.2 三个接口的工程覆盖

| 接口 | 形态 | 使用场景 |
|------|------|---------|
| `/limits` 命令 | 交互式 | 开发者手动控制 session |
| `--max-ai-credits` flag | 非交互式 | 脚本 / CI / 自动化 job |
| `soft cap` 行为 | 行为 | 不破坏 response 原子性 |

**两个客户端形态 + 一个行为约束** 完整覆盖了 **交互式 + 自动化 + 行为正确性** 三个维度。**笔者认为**，这是 1st-party 在「Harness Budget Control」上的最小可行实现 —— 它比 Anthropic 在 R613 的 cost report / OpenAI 的 usage API 都更**面向 session 而非面向 token**，更符合实际工程中「我跑一个 job，最多花 X 美元」的语义。

### 4.3 「Compaction」出现在 budget 计量里 —— Context Engineering 的成本真相

> 原文引用："Copilot tracks AI credit usage across the entire session, including model calls, subagents, and background work like compaction."

**「Compaction」被显式列入 budget 计量** —— 这是 R603（Artifacts）+ R605（Skill-as-Harness）+ R610（多轮 session 持久化）以来，第一次在 1st-party 公告里**把 Context Engineering 成本纳入预算**。这意味着：

1. **Background compaction 不是「免费的内部操作」** —— 它消耗 AI credit
2. **Long-running agent 的真实成本 = 主对话 + 子 agent + compaction**，必须一起算
3. **企业 IT 部门在评估「long-running agent」的 TCO 时，必须考虑 compaction 开销**

**笔者认为**，这是 GitHub 给出的**最反直觉的工程信号** —— 「background compaction 消耗 credit」这件事在很多企业的 TCO 模型里是隐性成本，而 GitHub 把它显式化了。这会推动整个行业重新思考 **「Context Engineering 是 LUXURY 还是 NECESSITY」** —— 当你看到 compaction 占总成本的 30% 时，结论不再是「当然开 compaction」。

---

## 五、Layer 1-4 GitHub Copilot Harness Architecture 全栈

把 R613、R616、R617 合并，**GitHub Copilot 的 2026 Q3 Harness Architecture 是一份四层架构**：

```
Layer 4: Enterprise Governance + Budget + Cross-Client Routing (R617 ← 本文)
   ↑ managed-settings.json 5 keys + Auto model selection CLI + Session limits
   ↑ 让 5000 人规模的企业能「配置即代码」地治理 Copilot

Layer 3: Browser Surface + Consent Architecture (R616)
   ↑ 真实浏览器 + Share with Agent + Tab 隔离 + 企业 allow/deny
   ↑ 把 Agent 的输出端口从 file system / terminal 扩展到 web

Layer 2: Agent Harness + Session Persistence (R612-R614)
   ↑ CLI chronicle + Session Harness + feedback loop
   ↑ 让 Agent 在长 session 中保持上下文与状态

Layer 1: Model Routing + Cache (R613)
   ↑ HyDRA routing + 94% cache 命中率 + TerminalBench 2.0 量化
   ↑ 让模型选型从「开发者手动选」变成「harness 自动选」
```

**这四层不是 GitHub 一次性设计出来的**，而是从 R612 (Anthropic Claude Science, vertical harness) → R613 (Cross-Model-Harness-as-Product) → R616 (Browser Surface + Consent) → R617 (Enterprise Governance + Budget) 一路演化出来。**每一层都在回答不同 stakeholder 的问题**：

| Layer | 回答的问题 | 主要 stakeholder |
|-------|-----------|-----------------|
| Layer 1 | 「这个任务用哪个模型最划算？」 | 个人开发者 |
| Layer 2 | 「Agent 跑挂了能不能恢复？」 | 个人开发者 / Team Lead |
| Layer 3 | 「Agent 能不能看我的浏览器？能不能被我关掉？」 | 个人开发者 / Security |
| Layer 4 | 「整个公司怎么用 Copilot？谁来管账？怎么控本？」 | CISO / IT / Finance |

**笔者认为**，这才是 Harness Engineering 范式的真正成熟 —— **不是「模型升级」驱动行业前进，而是「harness 每一层都成熟一层」驱动行业前进**。R612 揭示 vertical-harness 的可行性，R613 揭示 harness-as-product 的商业路径，R616 揭示 harness-as-trust-boundary 的安全路径，R617 揭示 harness-as-enterprise-IT 的治理路径。**这是一个 4 个月（2026-03 到 2026-07）的范式收敛**，不是新闻，是结构变化。

---

## 六、为什么 AgentBudget/agentbudget 必然出现

R617 的 Pair project 是 **AgentBudget/agentbudget**（Apache-2.0，105⭐，2026-02-15 创建），定位是 **「AgentBudget is the ulimit for AI agents」**。它的存在恰恰印证了 **「Harness Budget Control 不是一个 1st-party 商业决定，而是整个行业的工程共识」**。

具体看 AgentBudget 的设计：

1. **「Unix ulimit」比喻** —— 它的 README 直接借用 Unix 系统的 `ulimit` 概念，定位是 **「让单个 agent session 不能耗光整个 AI 预算」**
2. **`wrap_client()` 接口** —— 透明地把 LLM SDK 包起来，不需要改业务代码
3. **`finalization_reserve` / `would_exceed()` API** —— 给 Agent 一个「我快到预算了」的可观测信号
4. **OpenRouter model names** —— 多模型路由 + 多厂商计价的统一抽象

**GitHub 的 7/1 session limits 是「商业产品层的 budget control」，AgentBudget 是「开源 SDK 层的 budget control」** —— 两者方向完全一致，但工程权衡不同：

| 维度 | GitHub Copilot Session Limits (R617) | AgentBudget/agentbudget |
|------|--------------------------------------|-------------------------|
| 部署形态 | SaaS（managed） | Library（self-hosted） |
| 计费维度 | AI credits（GitHub 内部计费单位） | Dollar（实际美元） |
| 触发位置 | Copilot harness 内部 | LLM client wrapper |
| Soft/Hard cap | Soft cap（response 跑完才停） | 可配（默认 hard） |
| 多 agent 支持 | 内置（subagent + compaction） | 需要业务侧显式 wrap |
| License | 商业 | Apache-2.0 |

**笔者认为**，这两个实现互补关系很强 —— **想要 SaaS 体验的团队直接用 GitHub Copilot，想要自托管 / 多云 / 跨厂商的团队用 AgentBudget**。从行业角度看，**「Harness Budget Control」已经是一个独立的产品 / 库类目**，不再依附于某个具体 LLM 或 harness。

---

## 七、对中国 / 中文 AI 工程社区的具体启示

这一节给中文读者 —— 不是泛泛的「AI 大势所趋」，而是**对 2026 H2 实际工程决策的具体建议**：

### 7.1 「managed-settings.json」模式值得抄

如果你做的是 to B AI 产品（企业内部 AI Agent 平台 / 行业 AI Agent SaaS），**最值得抄的不是「AI 模型」或「Agent 框架」，而是「configuration as code」这个治理范式**。具体来说：

1. **不要把策略藏在管理后台 UI 里** —— 让 CISO / IT 能用 git 管理 AI 配置
2. **支持 PR review** —— 任何 AI 策略变更都是 reviewable
3. **支持周期性 refresh** —— 不是「管理员推一次」，而是「harness 自动拉最新」
4. **存内存不落盘** —— 防止本地缓存导致的策略过期

**如果你的 AI 产品 2026 H2 还没支持「configuration as code」，它的 to B 商业天花板大概率是 SMB**，因为 enterprise customer 的第一诉求就是「我能审计你的 AI 行为」。

### 7.2 「Auto model selection」比「锁定模型」更安全

很多企业 AI 治理的本能反应是「锁模型」—— 用最便宜的、用最稳的、用我们信任的厂商。但 **R617 揭示了一条反直觉的治理路径：「让 harness 自动选」+ 「默认开 Auto」+ 「保留 /model override」** 比「锁模型」更优：

- **成本最优**：Auto 比手动选便宜 10%
- **质量最优**：Auto routing 五个维度评估，比人工选更准
- **灵活性最优**：开发者仍可手动覆盖
- **审计性最优**：Auto 选了什么模型，全部 logged

**「Anti-lock-in 治理」** 是 2026 H2 的新范式 —— 企业治理的 goal 不是「控制每个 token」而是「确保每个 token 都是 harness 在最佳状态下花的」。

### 7.3 「软上限 + response atomic」是 budget control 的工程基线

如果你做的是 long-running agent / coding agent / research agent，**「hard kill budget」是个反模式** —— 它会让 Agent 跑到一半被砍，留下半截状态污染上下文、消耗 token 却没产出。

**GitHub 的做法值得抄**：

1. **Soft cap**（不中断进行中的 response）
2. **Session-level 而非 token-level**（业务侧语义更自然）
3. **Compaction 计入预算**（Context Engineering 不是免费的）
4. **预留 `finalization_reserve`**（AgentBudget 的概念 —— 留预算给「收尾 response」）

---

## 八、R555 准周期观察 —— R617 是不是「4 突破 + 2 sat」模式

按 R555 准周期第 31 次验证：

- R612 突破 #1 (Anthropic Claude Science)
- R613 突破 #2 (GitHub Copilot Harness)
- R614 saturation
- R615 saturation
- R616 突破 #3 (GitHub Browser Tools GA)
- **R617 突破 #4 (GitHub Copilot Enterprise Governance + Budget Control)**

**4 突破 + 2 sat** 是 R555 era 的**最高频突破模式**。这表明 7/4 独立日前的 1st-party release 窗口**仍在持续释放工程信号**，R612-R617 这六轮（4 突破 + 2 sat）已经构成 **「GitHub Copilot Harness 完整架构」** 的范式收敛。

**R618 预测**（7/3 - 独立日前 1 天）：

| 概率 | 路径 |
|------|------|
| 50% | Anthropic Engineering / Claude Code SDK 7/3-7/4 突破 17-round plateau |
| 25% | OpenAI 7/4 1st-party release（GPT-5.6+ engineering post / Agent Builder GA） |
| 15% | saturation streak（R612-R617 6 轮后冷却 1 轮） |
| 10% | silent round |

---

## 九、结语 —— Harness Engineering 进入了「Layer 4 时代」

R617 不是「又一个 1st-party changelog 集合」，而是 **GitHub Copilot Harness Architecture 的 Layer 4 GA**。从 R613 的「Model Routing」到 R616 的「Browser Surface」再到 R617 的「Enterprise Governance」，**Harness Engineering 在 2026 Q3 已经形成了清晰的四层架构**：

> **Layer 1（路由）+ Layer 2（持久化）+ Layer 3（表面）+ Layer 4（治理） = 完整的 AI Agent Harness**

任何 2026 H2 准备做 AI Agent 产品的团队，都应该把这四层当作**新产品的 baseline checklist**：

- [ ] **Layer 1**：我有没有 cross-model routing + cache awareness？
- [ ] **Layer 2**：我的 session 能不能 resume + 跨设备同步？
- [ ] **Layer 3**：我的 agent 输出端口有没有 trust boundary + consent model？
- [ ] **Layer 4**：我的产品能不能被企业 IT 用 git 管理 + 有 session-level budget control？

如果你只做了 Layer 1-2，你的 to B 商业天花板是 SMB；
如果你做到了 Layer 3-4，你可以直接打 enterprise market。

**这就是 R617 揭示的工程真相** —— 「模型能力」已经不是 2026 H2 的胜负手，「**harness 每一层都做透**」才是。

---

## 参考链接

1. **GitHub Blog - Enterprise managed-settings.json GA (本文核心)**: https://github.blog/changelog/2026-07-01-enterprise-managed-settings-json-is-generally-available
2. **GitHub Blog - Enterprises can default to auto model selection**: https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection
3. **GitHub Blog - Copilot CLI auto model selection routes based on task**: https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task
4. **GitHub Blog - Set AI credit session limits in Copilot CLI and SDK**: https://github.blog/changelog/2026-07-01-set-ai-credit-session-limits-in-copilot-cli-and-sdk
5. **R616 配套文章 (Layer 3)**: `articles/harness/github-copilot-browser-tools-ga-consent-architecture-2026.md`
6. **R613 配套文章 (Layer 1)**: `articles/harness/github-copilot-agentic-harness-94-percent-cache-hydra-routing-2026.md`
7. **R612 配套文章 (Vertical-Harness)**: `articles/harness/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md`
8. **Pair Project AgentBudget/agentbudget**: https://github.com/AgentBudget/agentbudget