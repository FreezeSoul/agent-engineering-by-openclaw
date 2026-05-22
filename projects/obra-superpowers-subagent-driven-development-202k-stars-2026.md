# Superpowers：让 Coding Agent 实现小时级自主开发的技能框架

## 基本信息

- **仓库**：obra/superpowers
- **Stars**：202,058（数据截至 2026 年 5 月）
- **链接**：https://github.com/obra/superpowers
- **语言**：TypeScript / JavaScript

## 核心定位

Superpowers 是一套完整的**软件工程方法论**，专门为 Coding Agent 设计。它不是简单的提示词集合，而是一套由可组合技能（Skills）驱动的开发流程，覆盖从需求理解到代码实现的完整生命周期。

## 核心工作流：Subagent-Driven Development

Superpowers 的核心创新是**子 Agent 驱动的开发流程**（Subagent-Driven Development）。当用户确认设计和计划后，Agent 会启动子 Agent 来处理各个工程任务，子 Agent 独立完成工作后，由主 Agent 检查和评审，再继续下一步。

```
Spec 确认 → Implementation Plan
    ↓
[Subagent 1] → Task A → 检查 → 评审
[Subagent 2] → Task B → 检查 → 评审
[Subagent 3] → Task C → 检查 → 评审
    ↓
继续下一步
```

这种模式与 Anthropic 的 Lead Agent + Subagent 架构形成了有趣的呼应——Anthropic 用 Lead Agent 协调研究任务的并行探索，Superpowers 则用 Subagent 并行处理编码任务的实现与审查。

## 技能系统：自动化触发的能力模块

Superpowers 的技能（Skills）是自动触发的模块，在开发过程中按需激活，不需要人工干预。主要技能包括：

- **Spec Generation**：将对话转化为结构化规格说明
- **TDD Red/Green**：红绿重构的测试驱动开发
- **Plan Emphasis**：强调 YAGNI、DRY 等工程原则
- **Self-Inspection**：子 Agent 完成后自检，再交由主 Agent 评审

这些技能通过**触发器规则**在合适的时机自动激活，而不是依赖用户的显式指令。

## 设计原则

### 1. Spec-First，而不是 Code-First

Superpowers 改变了 Agent 的默认行为：不是看到任务就写代码，而是先退后一步，理解用户**真正想要什么**。这减少了 Agent 在错误方向上浪费 Token 的情况——这正是 Anthropic 文章中提到的「最大化有效 Token 用量」原则的体现。

### 2. 计划可执行性

Superpowers 生成的实现计划要「足够清晰，即使一个判断力差、没有项目上下文、厌恶测试的热情初级工程师也能照着执行」。这不是降低标准，而是对 Agent 输出可执行性的极致追求。

### 3. 真正的 TDD

Superpowers 强调真正的红/绿重构（Red/Green TDD），而非形式上的测试覆盖率。这与当前大多数 Agent 跳过测试或仅生成形式化测试的做法形成对比。

## 与 Anthropic 多 Agent 架构的关联

Anthropic 的研究揭示了多 Agent 系统的核心洞察：**Token 用量是性能的主要驱动因素**（解释 80% 方差），而多 Agent 架构通过并行化独立上下文窗口来横向扩展 Token 预算。

Superpowers 的 Subagent-Driven Development 模式恰好体现了这一原则：

- **并行 Token 投入**：多个子 Agent 同时工作，相当于在短时间内密集投入 Token 预算
- **独立上下文隔离**：每个子 Agent 有自己的上下文，避免了长程对话中的上下文污染
- **最小化中转损失**：子 Agent 的输出直接进入审查，而非通过主 Agent 全量中转

从这个角度看，Superpowers 是将 Anthropic 的多 Agent 研究架构理论，转化为**编码场景的具体工程实践**。

## 支持的 Agent 平台

Superpowers 支持主流 Coding Agent 平台：

- Claude Code（官方插件市场）
- OpenAI Codex CLI / Codex App
- Cursor
- GitHub Copilot CLI
- Gemini CLI
- OpenCode
- Factory Droid
- 等

## 引用来源

- Superpowers GitHub：https://github.com/obra/superpowers
- Claude 官方插件市场（Superpowers 官方分发渠道）：https://claude.com/plugins
