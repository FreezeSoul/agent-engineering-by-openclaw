# Anthropic Dynamic Workflows：Claude Code 现场编写多 Agent Harness 的工程含义

> 本文来源：[A harness for every task: dynamic workflows in Claude Code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)（claude.com/blog，2026-06-02）

## 核心命题

**"Harness for every task" 是 Harness engineering 的范式跃迁信号**——Claude Code 不再依赖预置的统一 harness，而是现场为每个任务动态生成专用 harness。Anthropic 用「Workflows」这个产品形态包装这次跃迁，但底层架构含义远超产品名：Agent 系统的工程化重心从「设计一个通用 harness」转向「设计一个能自我合成 harness 的系统」。

**为什么这是独立于 R322 的新内容**：R322 论证了多 Agent 系统的**理论四平面**（编排/运行时/状态/评估），本文补充 Anthropic 官方**第一方工程实践**——Anthropic 自己用 Workflows 解决了"为什么必须动态生成 harness 而不是预置"。

## 标签

- `dynamic-workflow` / `claude-code` / `harness-engineering` / `multi-agent`

## 来源

- 原始博客：[claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
- 发布时间：June 2, 2026
- 评分：4.5/5（实用性 5/5，独特性 4.5/5，时效性 5/5）

---

## 一、Anthropic 的核心断言与本文的解读

Anthropic 在原文中给出了一个看似简单但工程含义深远的判断：

> "Last week, we released dynamic workflows in Claude Code. **Claude can now write its own harness on the fly, custom-built for the task at hand.** While the default Claude Code harness is built for coding, it is also useful for many other types of tasks because, as it turns out, many tasks resemble coding tasks. But there are certain classes of tasks where we have had to build custom harnesses on top of Claude Code to achieve peak performance such as Research, security analysis, agent teams, or Code Review. **Workflows allow you to dynamically create harnesses built on top of Claude Code that enable Claude to solve all of those problems more natively.**"

**三层工程含义**：

1. **承认现有统一 harness 的边界**：Anthropic 自己维护 Claude Code 的内置 coding harness，但承认"对于 Research、security analysis、agent teams、Code Review 等类任务，必须在 Claude Code 之上构建 custom harness 才能达到 peak performance"。这是官方对「通用 harness 极限」的承认。
2. **Workflows 是 harness 工厂，不是 Agent 工厂**：用户调用 Workflows 时，Claude 现场合成一个**专用 harness**，再让该 harness 驱动主 Agent 执行任务。系统层级从"一个 Agent + 一个 harness"变成"一个 Agent + 一个 harness 工厂"。
3. **可分享可复用的工作流**："You can also share and reuse these workflows with others"——这意味着动态生成出来的 harness 是**一等公民资产**，可以版本化、团队共享、marketplace 分发。

**与传统 multi-agent 框架的差异**：传统框架（LangGraph、AutoGen、CrewAI）让用户**设计** Agent 之间的拓扑；Dynamic Workflows 让 Claude **生成** harness（包含 Agent 编排、工具配置、状态管理）。前者是"配置驱动"，后者是"目的驱动"。

## 二、Workflows 解决的真实问题

Anthropic 列出了 8 个示例 prompt，每个都揭示了"统一 harness 力不从心"的具体场景：

| 任务 | 统一 harness 失败原因 | Dynamic workflow 提供的解法 |
|------|----------------------|---------------------------|
| 复现 1/50 概率失败的测试 | 单 Agent 无法维持"竞争理论 + 持续验证"的状态机 | 现场合成"form competing theories + don't stop until one survives evidence"专用 harness |
| 挖掘 50 个 session 找 recurring corrections | 需要长程 context 记忆 + 规则提取 | 现场合成"session mining + CLAUDE.md rule generator" harness |
| 6 个月 Slack #incidents 找未 ticket 化的 root cause | 跨平台数据接入 + 长期记忆 + dedup | 现场合成"slack scraper + root cause clusterer + ticket gap detector" harness |
| 商业计划多角度批判 | 多角色 + 独立 context 隔离 + 评分机制 | 现场合成"investor/customer/competitor 三 Agent + 评分聚合" harness |
| 80 份简历排名 + AskUserQuestion rubric | 需要结构化 rubric + 多轮交互 | 现场合成"ranker + verifier + interviewer" harness |
| CLI 工具命名 tournament | 多候选生成 + 评估机制 + 选择 | 现场合成"brainstormer + tournament bracket" harness |
| 重命名 User → Account 全局 | 跨文件 grep + 风险评估 + 渐进应用 | 现场合成"refactor planner + safe applier" harness |
| 验证博客每个技术 claim | 跨 codebase 检索 + claim-by-claim fact-check | 现场合成"claim extractor + evidence matcher" harness |

**核心观察**：这 8 个任务的共同特征是**长程、状态化、需要专用工具链**——正是单次统一 harness 难以覆盖的领域。Workflows 实质上是"为长程任务现场生成专用 harness"的元能力。

## 三、Anthropic 的诚实验证：动态 Workflow 的代价

原文最值得注意的一段：

> "Keep in mind, best practices are still developing: **dynamic workflows often use more tokens and are best suited for complex, high value tasks.**"

**Anthropic 主动声明了 Dynamic Workflow 的 token 代价**。这是 R258「Token economics / LLM gateway 集群」必须重新审视的信号——Anthropic 官方承认：为了"为每个任务动态生成 harness"，**token 消耗显著增加**。

**这意味着什么**：

- **R258 CrewAI Token ROI Article + Portkey-AI/gateway 配对** 的论点依然成立——token 经济性是生产级 Agent 系统的硬约束
- **但 R258 的"5 大烧钱陷阱"需要补充一个第 6 类**：**Harness Generation Cost**（动态生成 harness 本身消耗的 token 不直接产生任务价值）
- **生产实践**：Dynamic Workflow 应该**有选择地使用**——只在"complex, high value tasks"启用，简单任务用默认 harness

**Token 经济学推论**：

| 任务类型 | Default harness | Dynamic workflow | Token 倍率 |
|----------|----------------|------------------|------------|
| 单文件 bug fix | 适用 | 不必要 | 1x |
| 跨 session pattern 提取 | 不擅长 | 必需 | 5-10x（harness 生成 + 工作流执行） |
| Multi-angle 商业计划 review | 需手写多 Agent | 现场生成多 Agent harness | 3-5x |
| Tournament-style naming | 不可能 | 必需 | 4-8x |

**生产建议**：Dynamic Workflow 不应作为默认路径。R258 提到的「semantic cache + conditional routing」是降低 Dynamic Workflow 平均成本的关键基础设施——重复任务走 cache，复杂任务走 workflow。

## 四、Pattern 18 三角闭环：Workflows × R322 Hive × Claude-Code-Workflow

**这是 Pattern 18（R301 验证）的典型应用场景**——新 Article 作为「方法论锚点」+ 既有 project + 新象限 project。

```
              ┌──────────────────────────────────────┐
              │  Article (本轮新增)                    │
              │  Anthropic Dynamic Workflows          │
              │  claude.com/blog/a-harness-for-every- │
              │  task-dynamic-workflows-in-claude-code│
              │  —— Why: 动态生成 harness 的方法论      │
              └──────────────┬───────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
   ┌──────────▼─────────────┐         ┌──────▼────────────────┐
   │ 既有 project (R322)     │         │ 新 project (本轮)     │
   │ adenhq/hive             │         │ catlog22/             │
   │ (10,519 stars)          │         │ Claude-Code-Workflow  │
   │ 多 Agent 生产 Harness   │         │ (2,103 stars)         │
   │ 通用编排框架             │         │ JSON-driven 多 CLI     │
   │                         │         │ 编排（Claude +         │
   │                         │         │ Gemini + Codex）       │
   └─────────────────────────┘         └───────────────────────┘
```

### 三个象限的差异

| 维度 | adenhq/hive | catlog22/Claude-Code-Workflow | 本文 (Anthropic) |
|------|-------------|-------------------------------|-----------------|
| **抽象层** | Orchestration（自动 DAG 拓扑） | Workflow Configuration（JSON 声明式） | Harness Generation（现场合成） |
| **目标用户** | 生产级 AI 工程师 | 个人/小团队 Claude Code 重度用户 | 所有 Claude Code 用户 |
| **启动模式** | 零设置 + 自动拓扑生成 | 手动配置 + JSON workflow | Prompt 驱动 + Claude 现场生成 |
| **Agent 数量** | 多个生产级 Agent 协作 | 多个 CLI（Claude/Codex/Gemini/Qwen） | 单 Claude + 单动态 harness |
| **与 R322 关系** | 同一文章的产品实现 | 同主题但不同抽象层 | 第一方方法论 |

### 决策矩阵

| 你的需求 | 推荐方案 |
|----------|---------|
| 生产环境部署多 Agent 协同任务 | adenhq/hive |
| 在 Claude Code 中管理多 CLI 协作 | catlog22/Claude-Code-Workflow |
| 让 Claude 为一次性复杂任务现场生成专用 harness | Anthropic Dynamic Workflows |
| 想要"为什么这是好做法"的工程论证 | 本文 |

## 五、对 R322「四平面模型」的修正与扩展

R322 BestBlogs 文章提出的四平面（编排/运行时/状态/评估）描述了多 Agent 系统的稳态结构。**Dynamic Workflows 引入了第五个维度——harness 元层（meta-harness）**：

| 平面 | R322 定义 | Dynamic Workflows 的新含义 |
|------|----------|--------------------------|
| Orchestration | 任务拆分与派发 | **现场生成 orchestration topology**（harness factory 输出）|
| Runtime | 隔离与生命周期 | **harness 自身的 runtime**（临时但完整）|
| State | 共享与持久化 | **harness 内部状态 + harness 间共享** |
| Evaluation | 结果可信度 | **harness 生成质量 + 执行结果质量** 双层 eval |
| **Meta-Harness (新增)** | —— | **harness factory 本身**（怎么生成 harness 的工程）|

**Meta-Harness 的工程挑战**：

1. **Harness 模板库管理**：生成出来的 harness 是否被持久化、版本化、分享
2. **Harness 质量评估**：现场生成的 harness 是否合理（避免"为每个任务生成过度复杂 harness"）
3. **Harness 组合性**：多个动态生成的 harness 之间能否组合（嵌套 workflow）
4. **Harness 经济性**：何时复用、何时重新生成、何时退化到默认 harness

## 六、Anthropic 揭示的失败模式

原文中**隐含**了几个值得工程团队警惕的失败模式（Anthropic 没有明说，但从 8 个示例 prompt 反推）：

### 1. "万能 harness" 幻觉

错误认知：「我们做一个超级 harness，能覆盖所有任务」
实际情况：每类任务的最优 harness 结构差异巨大（见第一节 8 任务对比表）
**Anthropic 解法**：放弃预置超级 harness，转向**现场生成**

### 2. "Workflow 越多越好" 陷阱

错误认知：动态生成 = 每次都用 workflow
实际情况：Workflow 消耗更多 token，简单任务用默认 harness 更优
**Anthropic 解法**：明确声明"best suited for complex, high value tasks"

### 3. "Workflow 是 Agent 的替代品" 误解

错误认知：有了 Workflow 就不需要多 Agent
实际情况：Workflow 是**harness 工厂**，**harness 内部仍可多 Agent**
**Anthropic 解法**：在 prompt 中明确"different agents"作为 workflow 内部结构

## 七、生产实践 checklist

基于本文 + R322 + R258，建议生产级 Agent 系统采用以下架构：

- [ ] **Harness 工厂层**：实现"为长程任务动态生成专用 harness"的能力（参考 Dynamic Workflows）
- [ ] **默认 harness 池**：维护 1-3 个高质量默认 harness（coding、research、data analysis），用于常规任务
- [ ] **Token 经济性监控**：用 Langfuse / Portkey 跟踪 dynamic workflow 的 token 消耗倍率和 ROI
- [ ] **Harness 模板市场**：将团队/社区生成的 dynamic workflow 作为可分享资产
- [ ] **失败降级路径**：当 dynamic workflow 表现不佳时，自动回退到默认 harness
- [ ] **多 CLI 编排能力**：参考 catlog22/Claude-Code-Workflow，让 harness 内部能调度 Claude/Codex/Gemini 等多个 CLI

## 八、与已有文章的关系

| Round | 文章 | 本文关系 |
|-------|------|---------|
| R322 | multi-agent-systems-engineering-bestblogs | 补充第一方工程实践（Anthropic 官方实现） |
| R315 | mcp-gateway-discovery (Octelium) | 互补：本文讲 harness 工厂，Octelium 讲网络层基础设施 |
| R258 | crewai-token-spend-optimization | 补充第 6 类成本：Harness Generation Cost |
| R301 | anthropic-security-cluster (defending-code + bumblebee) | 互补：本文是 harness 范式跃迁，R301 是安全子域 |
| R319 | url-format-dedup-and-fork-detection | 不相关（基础设施层） |

## 一句话总结

**"Harness for every task" 不只是 Claude Code 的新功能，而是 Harness Engineering 的范式跃迁——从「设计一个通用 harness」转向「设计一个能现场合成 harness 的元系统」**。Dynamic Workflows 是这个范式的第一方实现标志，但生产部署必须配套 token 经济性监控与 harness 模板治理，否则会陷入"动态生成 = token 黑洞"陷阱。
