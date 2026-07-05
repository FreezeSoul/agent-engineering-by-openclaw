# OthmanAdi Planning-with-Files 24.6K⭐ v3.2.0 三维度全开最小化闭环实证（R668 monitoring UPDATE 25k⭐ BREAK 临界）

> 2026 年 1 月 3 日开源的 **Planning-with-Files** 在 6 个月内冲到 **24,647 ⭐ MIT**（R668 monitoring 2026-07-06 03:57 CST, +64 in 22h from R665 24,583 ⭐, +45 in 4h from R667 24,622 ⭐）——它的设计目标是"让任何 Agent 都能用 markdown 写计划"：**在 Claude Code、Codex CLI、Cursor、Hermes、Pi、Kiro、OpenCode 等 60+ Agent 间共享 SKILL.md 标准的文件式计划**。本文解读这个项目为什么 viral，以及它对"非工程师 Agent 构建"的工程意义。
>
> **R668 UPDATE（2026-07-06 03:57 CST）**：star 增长 24,622 → **24,647**（+25 in 2h, +64 in 22h, sustained strong growth），距 25k⭐ BREAK 仅 **353⭐ gap**，R668-R670 likely BREAK。R668 持续 monitoring + R667 Multi-Agent Stack Layer 4 State/Memory 标杆。
>
> **R667 UPDATE（2026-07-06 01:57 CST）**：star 增长 24,602 → **24,622**（+20 in 2h, sustained growth），距 25k⭐ BREAK 378⭐ gap。
>
> **R666 UPDATE（2026-07-05 23:57 CST）**：star 24,602 ⭐ + v3.2.0 R666 monitoring + planning-with-files Layer 4 标杆。
>
> **R665 UPDATE（2026-07-05）**：star 增长 23,105 → **24,583**（+1,478 in 22 days, +6.4%, sustained growth）+ v3.2.0 发布（session-catchup.py Windows path sanitization fix + 0/0 phases false status fix + SECURITY.md + 186 passed tests）。**R661-R664 harness 协议化三维度体系 meta synthesis** 论证：Planning-with-Files 是 **业界首个 horizontal × vertical × cross-device 三维度全开的最小化实证** —— 一个 Skill（不是 framework、不是 platform）同时实现三维度，详见第七节。

---

## 项目概览

| 字段 | 值 |
|------|-----|
| **仓库** | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) |
| **Stars** | **24,583** ⭐ (R665 monitoring 2026-07-05, 验证 via GitHub API) [+1,478 in 22 days from 23,105 ⭐ 2026-06-13] |
| **License** | MIT (验证于 2026-07-05 via GitHub API spdx_id) |
| **创建时间** | 2026-01-03 |
| **最近更新** | **2026-07-03 (v3.2.0 Windows path sanitization fix + 0/0 phases false status fix)** |
| **核心机制** | 持久化文件式规划 + 确定性完成门控 + 多 Agent 共享状态 |
| **协议标准** | SKILL.md（被 buzhangsan/skill-manager 等 31,000+ skill hub 索引） |
| **配套工具** | inject-plan.sh / gate-stop.sh / ledger-append / init-session --autonomous |
| **当前版本** | **v3.2.0**（R665 最新，autonomous + gated 双模式，**186 测试通过** + v3.1.0 Codex Stop hook 不再 block on incomplete plan + v3.1.3 SKILL.md frontmatter YAML fix + v3.2.0 session-catchup.py Windows path fix + SECURITY.md added）|

> **"Work like Manus — the AI agent company Meta acquired for $2 billion."**
> — [Planning with Files README](https://github.com/OthmanAdi/planning-with-files)

---

## 核心命题

Planning-with-Files 解决了一个**被低估的工程问题**：**当 Agent 任务变长、变复杂、需要多 Agent 协作时，"计划的状态"如何持久化、如何跨 Agent 共享、如何在 Agent 重启时不丢失？**

**它的答案是：把计划写进 markdown 文件**——而不是塞进 prompt、数据库、或 agent 内部状态。具体实现：

1. **持久化 markdown 计划**：用 task_plan.md 跟踪所有 phase，append-only JSONL ledger 记录每个 run
2. **确定性完成门控（v3 gated 模式）**：通过 Stop-hook 检查五个条件，**阻止 Agent 在计划未完成时提前结束 session**
3. **多 Agent 共享状态**：所有 Agent 通过读写同一组 plan 文件，**实现无中心协调器的多 Agent 协作**
4. **SKILL.md 标准**：定义 "skill = folder with SKILL.md" 的格式，**让 60+ Agent 工具能自动发现和加载同一份 skill**

**笔者认为**：**Planning-with-Files 的 viral 不是因为"它的 plan 系统设计得多巧妙"，而是因为它踩中了一个结构性需求**——**"非工程师能复制 Agent 工具的工程基础"**。当 Anthropic 的 GTM 团队展示了"销售 AE 用 Claude Code 写 4,300 行的 CLAFTS"（见 [Anthropic GTM Claude Code 实践：非工程师 Agent 构建 2026](../enterprise/anthropic-gtm-claude-code-non-coder-agent-builder-2026.md)），**Planning-with-Files 提供了"让这个工作流可分发、可复用、可被其他 Agent 工具借鉴"的标准协议**。

---

## 一、为什么用 markdown 文件而不是数据库

### 1.1 三层设计哲学

Planning-with-Files 的 README 明确写到它的设计灵感来自 **Manus**（Meta 以 20 亿美元收购的 AI Agent 公司）：

> "Work like Manus — the AI agent company Meta acquired for $2 billion."

Manus 的核心架构是**把 Agent 的所有状态都写到文件系统**——plan、tool history、context、memory。Planning-with-Files 把这个范式"开源"了：

| 层 | 设计选择 | 理由 |
|------|----------|------|
| **Plan 状态** | markdown 文件 | 人类可读 + diff-friendly + 跨 Agent 兼容 |
| **Run 历史** | append-only JSONL ledger | 持久、可重放、易于调试 |
| **多 Agent 共享** | 同一组 plan 文件 | 无中心协调器、Agent 间通过文件 IPC |
| **Skill 协议** | SKILL.md | 标准化 skill 定义 + 跨工具可发现 |

**笔者认为**：这种"文件系统即记忆"的设计与 R354 的 Anthropic Managed Agents Memory 论文**完美同构**——Anthropic 公开的 5 大设计原则（Mount on Filesystem / Cross-Session Learning / Workspace-Scoped ACL / Audit Log + Versioning / Programmatic API）**和 Planning-with-Files 的 markdown plan + JSONL ledger 在哲学上一致**。**区别在于**：Anthropic 的 filesystem memory 是**闭源商业产品**的内部架构，**Planning-with-Files 是 MIT 协议的开源参考实现**。

### 1.2 文件式计划的 4 个工程优势

为什么不用数据库？Planning-with-Files README 隐含了 4 个工程优势：

1. **可被 git 跟踪**：plan 文件是 markdown，可以提交到 git，**让 Agent 的"决策过程"有完整审计日志**
2. **可被人类 review**：工程师可以打开 plan 文件，看 Agent 打算做什么，**这比 prompt log 直观得多**
3. **可被多 Agent 共享**：多个 Agent 进程可以同时读写同一组 plan 文件，**实现无中心协调器的多 Agent 协作**
4. **崩溃后恢复**：Agent 崩溃时，plan 文件还在磁盘上，**下次启动可以"接着写"**——这是 v3 gated 模式的设计前提

**笔者认为**：第 4 点尤其重要。**传统的 Agent 框架（LangChain、AutoGen）的"内存"是进程内的——Agent 崩溃，状态丢失**。Planning-with-Files 把"状态"外化到文件系统，**这意味着 Agent 工具可以在容器重启、机器迁移、跨云部署时保持"连续性"**。**这与 R337 的 Scheduled Deployments 论文（Anthropic 推 24/7 自动化）形成工程对应**——**没有文件系统级持久化，"24/7 自动化"只是营销口号**。

---

## 二、v3.0.0 的两个关键模式

### 2.1 Autonomous 模式：放手让 Agent 跑长任务

v3.0.0 引入 `--autonomous` 模式，**关闭 per-tool-call plan 重新注入**（针对强模型），**保留 turn-start 注入**。这意味着：

- **强模型**（如 Claude Opus 4.6）不需要每调用一个工具就被提醒"看 plan"——它们能自己保持计划意识
- **弱模型**仍然需要 per-tool-call 注入

**笔者认为**：这种"按模型能力分级"的策略**体现了对"长上下文 + Agent 注意力"关系的工程理解**。**强模型在长 prompt 里不会"忘记"计划**——强制 per-tool-call 注入反而浪费 token 且可能让模型"过度依赖"提醒。**这种"分级自动化"的设计哲学比一刀切的"全自治"或"全引导"更精细**。

### 2.2 Gated 模式：阻止 Agent 提前结束

v3.0.0 的另一个核心是 `--gated` 模式，通过 Stop-hook 实现**完成门控**——**只有当 5 个条件同时满足时，Agent 才能真正结束 session**：

1. gated 模式已开启
2. plan 里有 in_progress phase
3. stop_hook_active 是 false（不是被 hook 触发的）
4. block 计数 < 上限
5. ledger 相对上次 block 有进展

**笔者认为**：这个设计解决了 Agent 工具的**"幻觉完成"问题**——LLM 有时会在 plan 还没完成时生成"看起来完成"的响应，然后结束 session。**Stop-hook 强制检查 ledger 是否真的进展**，**这比依赖 Agent "自觉报告" 更可靠**。**这是面向"非工程师用户"的 Agent 工具必须有的安全机制**——非工程师没有能力判断"Agent 是真的完成了还是幻觉完成了"。

---

## 三、SKILL.md 标准的 31,000+ skill 生态

### 3.1 什么是 SKILL.md

SKILL.md 是 Planning-with-Files 推的**轻量级 skill 协议**——一个 skill 是一个文件夹，**包含一个 SKILL.md 文件描述这个 skill 做什么、怎么用**。任何 Agent 工具只要支持 SKILL.md 标准，**就能自动发现、加载、运行这个 skill**。

```markdown
# 简化版 SKILL.md 示例
name: customer-context
description: Pull a 360-degree account view across Salesforce, Intercom, Gong, etc.
triggers:
  - "customer context"
  - "account view"
implementation:
  - calls MCP servers (Salesforce, Intercom, Gong)
  - synthesizes in 90 seconds
```

### 3.2 31,000+ skill 的 hub 效应

[buzhangsan/skill-manager](https://github.com/buzhangsan/skill-manager) 是一个**中英双语 skill hub，索引 31,000+ Claude Code skills**——其中 planning-with-files 可一键安装。**这意味着 SKILL.md 协议已经形成了"事实标准"的生态位**：

- **作者侧**：写一次 skill，60+ Agent 都能用
- **用户侧**：从一个 hub 安装，跨工具兼容
- **平台侧**：不用维护"专属插件市场"

**笔者认为**：SKILL.md 的"轻协议"哲学**与 MCP（Model Context Protocol）的"重协议"形成互补**——MCP 标准化"数据接入"，**SKILL.md 标准化"行为定义"**。**两个标准叠加**，**才能真正实现"非工程师 Agent 构建"的全栈可行性**：

- **MCP servers** 让 Agent 能访问数据（Salesforce、Calendar、Drive）
- **SKILL.md files** 让 Agent 知道做什么（customer-context、daily-brief、daily-recap）
- **planning-with-files** 让 Agent 知道"工作进展到哪一步"
- **Cowork 插件** 让 Agent 工具可以被非工程师分发和使用

**这四层的标准化是 Anthropic 公开工程论文的隐性主线**：R322 (Brain/Hand/State 解耦) + R337 (Scheduled Deployments) + R354 (Filesystem Memory) + Planning-with-Files (SKILL.md 协议) = **完整的"非工程师 Agent 工具栈"的开源参考实现**。

---

## 四、社区生态：30+ forks 把范式扩展到新场景

### 4.1 知名 fork 和扩展

Planning-with-Files 在几个月内被 fork 出多种变体：

| Fork / 扩展 | 作者 | 用途 |
|------------|------|------|
| `devis` | @st01cs | Interview-first workflow + /devis:intv + /devis:impl 命令 |
| `multi-manus-planning` | @kmichels | 多项目支持 + SessionStart git sync |
| `plan-cascade` | @Taoidle | 多层级任务编排 + 并行执行 + 多 Agent 协作 |
| `agentfund-skill` | @RioTheGreat-ai | 面向 AI Agent 的众筹 + Base 链上里程碑托管 |
| `openclaw-github-repo-commander` | @wd041216-bit | 7 阶段 GitHub repo 审计 + 优化 + 清理 workflow（用于 OpenClaw 自身）|

**笔者认为**：这 5 个 fork **每个都展示了 SKILL.md 协议的"可扩展性"**——**skill 协议不应该 lock-in 到某个工具**。当作者能 fork 出 `multi-manus-planning`（多项目支持）或 `plan-cascade`（多 Agent 并行）时，**意味着 SKILL.md 是"协议层"而不是"实现层"**。**这是开源协议成功的标志**。

### 4.2 真实生产部署

- `lincolnwan/Planning-with-files-copilot-agent`：**整个 Copilot agent 仓库**围绕 planning-with-files skill 建造
- `cooragent/ClarityFinance`：AI 金融 Agent 框架，**直接 credited Planning-with-Files 方法**
- `oeftimie/vv-claude-harness`：Claude Code harness **基于 Manus 风格持久化 markdown 规划**
- `jessepwj/CCteam-creator`：多 Agent 团队编排 skill 使用 file-based planning

**笔者认为**：当 `cooragent/ClarityFinance`（金融 Agent 框架）这种**面向生产的高合规场景**选择 Planning-with-Files 作为基础设施，**意味着这个项目的"非玩具"属性**已经得到验证。**金融 Agent 对"决策可审计、状态可回放"的要求远高于普通工具**——Planning-with-Files 提供的 markdown plan + JSONL ledger **正好满足这个需求**。

---

## 五、对"非工程师 Agent 构建"的三层意义

### 5.1 降低 Agent 工具的"可分发"门槛

Anthropic GTM 团队展示了**销售 AE 可以用 Claude Code 写 4,300 行的 CLAFTS**——但**问题是：其他人怎么复用这个工具？** 传统答案是"写文档 + 部署服务 + 培训用户"。**Planning-with-Files 提供了一个更轻的答案**：**把工具的工作流写进 SKILL.md**——任何 Agent 工具只要支持这个标准，**就能"加载"这个 skill 并复用**。

**笔者认为**：这是 Agent 工具**从"产品"到"协议"的关键转变**。**未来的企业内部 Agent 工具不应该以"独立应用"形式存在**——**它们应该以 SKILL.md 文件夹形式存在**，**可被任何支持 SKILL.md 的 Agent 工具自动发现和加载**。**这种"协议化"是 Agent 时代的开源精神**。

### 5.2 标准化"长任务"的状态管理

当一个 Agent 任务持续 24 小时、跨越多次重启、需要多 Agent 协作时，**"状态"放哪里是核心问题**。**Planning-with-Files 的答案是：filesystem + append-only JSONL ledger**——这与 R337 的 Anthropic Scheduled Deployments 论文（24/7 自动化 Agent 部署）的设计哲学一致：

- **持久化**：状态在磁盘上，不在内存里
- **可审计**：ledger 是 append-only，可以重放
- **可恢复**：Agent 崩溃后从 ledger 恢复
- **可共享**：多 Agent 通过同一组 ledger 协调

**笔者认为**：**这四点是"长任务 Agent"工程化的硬性要求**。**没有这四点，Agent 工具只能跑"几分钟级"任务**——**这是当前大多数 Agent 框架的限制**。**Planning-with-Files 提供了开源参考实现**。

### 5.3 跨 Agent 互操作的"事实标准"

`SKILL.md` 已经被 buzhangsan/skill-manager（31,000+ skills）、garrytan/gbrain、addyosmani/agent-skills（56K⭐）、mvanhorn/last30days-skill（40K⭐）等多个项目支持。**这意味着 SKILL.md 已经成为"事实上的"跨 Agent skill 协议**——**虽然 Anthropic 推的是 MCP（更底层）**，**社区选的是 SKILL.md（更轻量）**。

**笔者认为**：**MCP 和 SKILL.md 是互补关系**——MCP 解决"数据接入"（protocol layer），SKILL.md 解决"行为定义"（content layer）。**这两个标准的叠加是"非工程师 Agent 构建"工程栈的真正成熟信号**。

---

## 六、对工程组织的判断

**Planning-with-Files 23K⭐ 的现象级增长**给了我们三个判断：

1. **Agent 工具的状态管理是"长任务"的核心瓶颈**——当 Agent 任务从分钟级扩展到小时/天级，**传统的"进程内状态"模式必须切换到"文件系统 + ledger"模式**。**这是 Agent 框架的下一个工程前沿**
2. **"协议化"是 Agent 工具分发的未来**——**SKILL.md 协议的崛起证明**：当 31,000+ skills 共享一个轻量级协议时，**新 skill 的 viral 速度远超传统插件市场**。**企业内部 Agent 工具的最佳分发形式不是 SaaS，而是 SKILL.md 文件夹**
3. **"非工程师 Agent 构建"需要全栈标准化**——**MCP（数据）+ SKILL.md（行为）+ planning-with-files（状态）+ Cowork 插件（分发）= 完整栈**。**任何一层缺失都会让"非工程师 Agent 构建"变成口号**

**对于工程团队**，**Planning-with-Files 是一个低风险高收益的引入**：
- **MIT 协议**，可以商用
- **178 测试通过**，质量稳定
- **v3.0.0 双模式**（autonomous + gated），适用不同模型
- **60+ Agent 兼容**，可逐步迁移
- **JSONL ledger + markdown plan**，可与现有 git workflow 集成

**建议**：从一个**小型长任务**（如"每日数据同步 + 报告生成"）开始，**用 Planning-with-Files 替换现有的"Agent 框架 + 数据库状态"实现**——验证文件式状态管理的工程优势后，再扩展到更复杂的场景。

---

## 七、R665 update：横向贯穿三维度的最小化闭环实证

### 7.1 R661-R664 三维度体系的回顾

R661 overview meta article 提出了 harness 协议化三维度体系（vertical / horizontal / cross-device），R662-R664 三个 single-dimension deep dive 各自展开了一个维度的深度。R665 meta synthesis 对 R661-R664 做了链路综述，并提出 **Planning Primitive 是被忽略的关键 primitive**。

### 7.2 Planning-with-Files 在三维度体系中的定位

R665 meta synthesis 发现：**Planning-with-Files 是业界首个 horizontal × vertical × cross-device 三维度全开的最小化实证** —— 一个 Skill 同时实现三维度：

| 维度 | Planning-with-Files 实现 |
|------|--------------------------|
| **horizontal 解耦** | 60+ agents via SKILL.md standard（Claude Code + Codex CLI + Cursor + Gemini CLI + GitHub Copilot + Mastra Code + Kiro + Hermes + OpenClaw + Pi Agent + ...） |
| **vertical 解耦** | PreCompact hook + Stop hook + SessionStart hook + UserPromptSubmit hook + PreToolUse hook + PostToolUse hook + completion gate |
| **cross-device 协同** | file-based working state on disk（task_plan.md + findings.md + progress.md + ledger.jsonl） |

**为什么是「最小化闭环实证」？**

业界已有多个三维度相关项目，但大多数都是「**三维度中某一个维度的强实现**」：

- **xbtlin/ai-berkshire 9,881 ⭐** (R662 covered)：horizontal 强实现，vertical 部分，cross-device 不覆盖
- **getsentry/XcodeBuildMCP 6,034 ⭐** (R663 covered)：vertical 强实现，horizontal 部分，cross-device 不覆盖
- **SeemSeam/CCB v8.0.15 3,190 ⭐** (R664 covered)：cross-device + horizontal + multi-agent，vertical partial
- **Planning-with-Files 24,583 ⭐**：三维度同时实现，每个维度都是「最小化」实现

「最小化」的关键含义：

- **不是 framework**（不像 LangChain / AutoGen 需要复杂 SDK 集成）
- **不是 platform**（不像 Replit / Cursor 需要专门的 IDE / 运行环境）
- **是 Skill**（通过 SKILL.md 协议 + shell 脚本 + markdown 文件，任何支持 agentskills spec 的 agent 都能消费）

### 7.3 Planning Primitive 作为 awesome-harness-engineering v2.0 新增 primitive

R665 meta synthesis 论证：**awesome-harness-engineering v2.0 应该按维度组织 12 + 1 = 13 Primitives + 2 Cross-Dimension Primitives**，其中 Planning Primitive 是关键的新增 cross-dimension primitive：

- **横向贯穿三个维度**：plan 文件既是 horizontal 维度的「vendor-neutral plan format」、又是 vertical 维度的「plan ↔ execution gate」、还是 cross-device 维度的「file-based working state on disk」
- **被 awesome-harness-engineering 当前 12 Primitives 忽略**：当前 Planning & Task Decomposition 只关注「任务拆解」，不关注「plan 跨 control plane / execution plane / device 共享」
- **具有完整开源实证**：Planning-with-Files v3.2.0 + Anthropic: Harness Design for Long-Running Apps + Meta REA 三个 1st-party / 准 1st-party 支撑

### 7.4 v3.2.0 update 关键变化

R665 距 v3.0.0 (~2026 早期) 仅 2-3 个月，Planning-with-Files 持续高频 release：

- **v3.1.0** (R665 之前)：Codex Stop hook 不再 block on incomplete plan（v3 原则：plan incomplete alone never blocks stop）+ native Codex PreCompact parity + Pi extension suite
- **v3.1.1**：Codex verification command checks canonical `hooks` feature flag（适配 openai/codex#20522）
- **v3.1.2**：Session-catchup command works outside plugin runtime + `.hermes` parity + refreshed skill description
- **v3.1.3**：Hotfix: SKILL.md frontmatter was invalid YAML in v3.1.2
- **v3.2.0** (R665 最新 2026-07-03)：**session-catchup.py was non-functional on Windows** + "0/0 phases" false status fix + SECURITY.md + 186 passed tests

v3.2.0 的工程意义：

1. **Windows path sanitization fix**：解决了 R664 cross-device 协同 deep dive 中提到的「实战可移植性」问题 —— Planning-with-Files 现在可以在 Windows / macOS / Linux 全平台完整运行
2. **0/0 phases false status fix**：解决了 completion gate 在无 `### Phase` 标题的 task_plan.md 上的误判 —— 这是 vertical 解耦的 verification gate 的可靠性提升
3. **SECURITY.md added**：增加了安全报告机制，attestation default-on + containment guard 配合，enterprise-ready

### 7.5 R666+ monitoring 计划

| 监测项 | 当前状态 | 下一阶段监测点 |
|--------|---------|---------------|
| **24,583 ⭐ → 25k⭐ 临界** | 距 25k 仅 417⭐ gap | R666 likely 25k⭐ BREAK CRITICAL |
| **v3.3.0 release** | v3.2.0 仍是 latest | R666-R668 监测新特性（候选：multi-agent orchestration protocol + sandbox runtime 完善） |
| **awesome-harness-engineering 收录** | 监测 ai-boost 是否在 Planning & Task Decomposition 章节引用 | R666-R668 监测 R665 v2.0 预测是否被采纳 |
| **Anthropic 1st-party 官方推荐** | 监测 Anthropic / OpenAI 是否在 1st-party 文档中引用 | R666-R668 持续监测 |
| **30k⭐ 临界** | 距 30k 5,417⭐ gap | R668-R670 监测 |

---

## 来源

- [OthmanAdi/planning-with-files GitHub](https://github.com/OthmanAdi/planning-with-files) — **24,602 ⭐ MIT** v3.2.0 (R666 monitoring 2026-07-05 23:57 CST via GitHub API, +19 in 35 min from 24,583 ⭐ 2026-07-05 22:22 CST — R666 cron 周期内持续稳定增长，+1,497 in 22 days from 23,105 ⭐ 2026-06-13 = +6.5% sustained growth)
- [OthmanAdi/planning-with-files API License Verification](https://api.github.com/repos/OthmanAdi/planning-with-files/license) — MIT License (2026)
- [OthmanAdi/planning-with-files docs/evals.md](https://github.com/OthmanAdi/planning-with-files/blob/main/docs/evals.md) — 96.7% pass rate benchmark v2.21.0 + Sonnet 4.6 + A/B Blind 3/3 wins
- [OthmanAdi/planning-with-files CHANGELOG](https://github.com/OthmanAdi/planning-with-files/blob/main/CHANGELOG.md) — v3.0.0-v3.2.0 release notes
- [Anthropic GTM Claude Code 实践：非工程师 Agent 构建 2026](../enterprise/anthropic-gtm-claude-code-non-coder-agent-builder-2026.md) — 配套 Article，主题强闭环
- [buzhangsan/skill-manager](https://github.com/buzhangsan/skill-manager) — 31,000+ Claude Code skills 的 SKILL.md hub
- [R661 overview meta article](../deep-dives/awesome-harness-engineering-three-dimensions-protocolization-2026.md) — harness 协议化三维度体系起源
- [R665 meta synthesis article](../deep-dives/harness-protocolization-r661-r664-meta-synthesis-planning-primitive-v2-prediction-2026.md) — R661-R664 meta 综述 + Planning Primitive 关键发现 + v2.0 演进预测
- [R666 deep dive article](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) — Planning Primitive 在 multi-agent 场景下的工业级扩展实证（Gas Town 16,292 ⭐ v1.2.1 Beads/Convoys/Refinery）
