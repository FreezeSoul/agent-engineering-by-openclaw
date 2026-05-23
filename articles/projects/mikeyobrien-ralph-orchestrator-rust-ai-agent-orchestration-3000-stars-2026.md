# mikeyobrien/ralph-orchestrator：用「帽子戏法」重新定义多 Agent 编排

## 目标用户

已不满足于单 Agent 协作，希望用**多角色 Agent 编排**处理复杂长周期任务的开发者。

---

## 能解决什么问题

大多数 Agent 编排框架的问题是：**假设 Agent 不会犯错，或者 Agent 能在犯错后自我纠正**。

现实是：即使是最强的 Claude Code，在面对大型跨文件重构时，也可能在第 47 次编辑时引入一个 typecheck 错误，然后在没有人类介入的情况下花 20 分钟试图用错误的方式修复它。

Ralph Orchestrator 解决的是这个问题：**如何让多个专业 Agent 在一个受控的循环中协作，同时让人类随时可以介入**。

---

## 核心亮点

### 1. Hat System：角色即帽

Ralph 提出了一个有趣的概念：**Agent 不是一种东西，而是可以戴不同帽子的角色**。

> "A hat-based orchestration framework that keeps AI agents in a loop until the task is done."

每个 Hat 代表一个专业角色：

| 帽子 | 角色 | 职责 |
|------|------|------|
| `code-assist` | 编码助手 | 实现 feature、修复 bug |
| `debug` | 调试专家 | 定位根因、验证修复 |
| `research` | 研究员 | 调研方案、评估风险 |
| `review` | 评审员 | 代码审查、质量把关 |
| `pdd-to-code-assist` | PDD 执行者 | 将 PRD 转为代码实现 |

这些帽子可以**自由组合**。一个任务流可以同时有 3 个 Agent 分别戴不同的帽子并行工作。

### 2. Backpressure：门控即质量门

Ralph 有一个很关键的设计：**Backpressure**。

> "Gates that reject incomplete work (tests, lint, typecheck)"

这意味着，当一个 Agent 完成工作后，它不是直接交付给下一个 Agent，而是先过一道门：

```
代码写完 → 测试门 → lint门 → typecheck门
                    ↓
              任一失败 → 打回重做
              全部通过 → 下一阶段
```

这不是简单的工作流引擎，而是**把质量门内置到协作协议里**。Agent 不能带着错误「传递」给下一个环节。

### 3. RObot：人在环路（Telegram）

Ralph 支持人类在编排过程中实时介入，通过 Telegram：

```
Agent 发出问题 → 人类回答 → Agent 继续
                ↓
        超时则按默认处理
```

这解决了「完全自治 Agent 在边界情况下会卡住」的问题。

### 4. 多后端支持

Ralph 不绑定某个特定 Agent 实现：

> "Multi-Backend Support — Claude Code, Kiro, Gemini CLI, Codex, Amp, Copilot CLI, OpenCode"

这意味着你可以在同一个任务流里让 Claude Code 和 OpenCode **协作**——各自发挥自己的优势。

---

## 与现有编排框架的对比

| 框架 | 核心抽象 | 人的位置 | 质量门 |
|------|---------|---------|-------|
| **Ralph Orchestrator** | Hat System | Telegram 实时介入 | Backpressure Gates |
| **CrewAI** | Agent + Task | 初始 Prompt | 无内置 |
| **AutoGen** | 代理协商 | 人类审批 | 无内置 |
| **Symphony (OpenAI)** | Linear 任务板 | 看板可视化 | 无内置 |
| **Edict (三省六部)** | 制度性审核 | 审核层 | 封驳机制 |

Ralph 的差异化在于：
1. **Backpressure** 是显式的、代码化的质量门（而非人工审批）
2. **Hat System** 是动态的角色组合，而非固定的 Agent 定义
3. **Telegram 人在环路** 提供了轻量级的实时介入机制

---

## 适用场景

**适合**：
- 复杂跨模块重构（需要 code + debug + review 多角色）
- 高风险部署前质量把关（Backpressure 门控）
- 需要人类实时决策但又不想全程盯着的场景
- 跨框架协作（Claude Code + OpenCode 混用）

**不适合**：
- 简单单步任务（直接用 Claude Code 更简单）
- 需要严格审批流程的企业场景（Edict 更适合）
- 纯无人在环的全自动化场景

---

## 核心洞察

Ralph Orchestrator 的核心洞察是：**Agent 编排的问题不是「如何让 Agent 协作」，而是「如何设计一个有质量门的协作循环」**。

大多数框架解决的是拓扑问题（谁向谁发消息），Ralph 解决的是**控制问题**（什么条件下才能进入下一个状态）。

---

*来源：[mikeyobrien/ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator)，GitHub，2026年5月*