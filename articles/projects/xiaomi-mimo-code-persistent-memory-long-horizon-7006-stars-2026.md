# XiaomiMiMo/MiMo-Code：持久记忆驱动的长时域 Coding Agent

> **核心命题**：Xiaomi MiMo Code 解决了一个长期困扰 coding agent 的问题——任务一长，Agent 就忘记自己在做什么。7,006 颗星（且在快速增长）说明这个痛点是真实的。
>
> **金句**：如果你用现有 coding agent 跑过一个超过 2 小时的任务，你会理解为什么"持久记忆"不是一个噱头——它是让长时域任务从"不可能"变成"可能"的关键工程机制。

---

## 这个项目解决什么问题

Codiagent 在短任务（10 轮以内）上表现出色，但当任务扩展到几十甚至上百步时，传统的"把对话历史传给模型"的方案面临两个根本问题：

1. **上下文窗口终将耗尽**：工具输出、代码片段、错误日志会填满任何合理的上下文窗口
2. **模型指令遵循能力随输入增长下降**：有用的约束被大量输出稀释

MiMo Code 的核心思路是：**不是想办法塞更多上下文，而是为不同时间尺度的问题设计对应的工程机制**。这使得它在 SWE-Bench Pro 上比单采样方案提升 10-20%。

---

## 核心技术设计

### 1. Max Mode：并行采样与选择

在每一轮并行生成 5 个候选解，每个候选独立完成推理和工具调用规划，但不执行。然后用同一个模型作为 judge 选择最佳方案执行。

> "If multiple candidates happen to converge, that itself indicates high confidence in that direction; when candidates differ significantly, having a low-temperature judge select the most robust plan is more reliable than depending on a single sample." — [MiMo Code GitHub README](https://github.com/XiaomiMiMo/MiMo-Code)

**笔者的判断**：这不是简单的"多试几次"。当多个候选收敛时说明方向高置信；当候选分歧时，低温 judge 选择最稳健方案比单样本更可靠。这是一种**自路由的可靠性机制**。

在 SWE-Bench Pro 上，Max Mode 提升 10-20%，代价是 4-5 倍 token 消耗。

### 2. Goal：独立完成验证

由用户定义自然语言停止条件（如"所有测试通过且代码已提交"），每当 Agent 试图终止时，系统自动启动独立模型调用审查完整对话历史，判断条件是否满足。

> "This verifier does not participate in the actual work, so it does not develop an alignment bias toward the parts the agent has already completed." — [MiMo Code Blog](https://mimo.xiaomi.com/blog/mimo-code-long-horizon)

**关键设计**：verifier 不参与实际工作，因此不会对 Agent 已完成部分产生对齐偏见。每次收到与 Agent 完全相同的上下文。

### 3. Dynamic Workflow：编排逻辑从提示词到代码

主 Agent 生成 JavaScript 脚本，在隔离沙箱中确定性执行。通过 `agent()` 分发子 Agent，通过 `parallel()` / `pipeline()` 控制并发。

> "The workflow() primitive allows scripts to call other scripts, so orchestration logic can be organized into reusable and composable building blocks." — [MiMo Code Blog](https://mimo.xiaomi.com/blog/mimo-code-long-horizon)

**笔者认为**：这是目前见过的最完整的 Dynamic Workflow 实现。关键扩展包括：
- workflow() 可组合性（脚本调用脚本）
- 每个 agent() 结果同步写磁盘，支持中断恢复
- 沙箱内可直接读写文件

### 4. 工具调用语法：更少 token，更少错误

受约束的命令行语法（不支持管道、重定向、变量展开）token 效率最高，格式化错误更少——因为大多数模型在密集的 shell 环境数据上训练过。

---

## 技术规格

| 维度 | 数据 |
|------|------|
| **Stars** | 7,006（持续增长中）|
| **License** | MIT |
| **Primary Language** | TypeScript (95.5%) |
| **Forks** | 552 |
| **Open Issues** | 428 |
| **GitHub** | [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) |

---

## 竞品对比

| 项目 | Stars | 核心差异化 |
|------|-------|-----------|
| **Claude Code** | 官方闭源 | 终端原生，深度集成 Anthropic 生态 |
| **DeepSeek-Reasonix** | 21K+ | Cache-First Loop，长会话成本优化 |
| **CowAgent** | 45K+ | 三层记忆，跨会话自我进化 |
| **MiMo Code** | 7K+ | 三时间尺度框架 + Dynamic Workflow 完整实现 |
| **Hindsight** | 16K+ | "agents that learn, not just remember" |

**笔者的判断**：MiMo Code 的差异化在于它提供了一套**系统化的问题分解框架**（三重时间尺度），而不是又一个"集成更多工具"的 coding agent。在长时域任务这个细分场景，这是有真实工程价值的。

---

## 适用场景

✅ **适合**：
- 长时间运行的自动化任务（代码迁移、重构、大规模测试）
- 需要可靠完成判断的任务（Goal 机制）
- 需要并行协调复杂工作流的场景（Dynamic Workflow）

❌ **不适合**：
- 短时一次性任务（现有工具已足够）
- 需要实时人类干预的场景（设计为长时域自动化）
- 对 token 成本极度敏感的场景（Max Mode 代价是 4-5 倍消耗）

---

## 如何上手

```bash
# 安装
npm install @mimo/mimo-code

# 基本用法
mimo --task "你的任务描述"

# 启用 Max Mode
mimo --task "迁移整个项目到 TypeScript" --max-mode 5

# 定义停止条件
mimo --task "重构 authentication 模块" --goal "所有测试通过且代码已提交"
```

详细文档：[https://github.com/XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code)

---

## 引用来源

- [GitHub README](https://github.com/XiaomiMiMo/MiMo-Code)
- [MiMo Code Blog: Scaling Coding Agents to Long-Horizon Tasks](https://mimo.xiaomi.com/blog/mimo-code-long-horizon)