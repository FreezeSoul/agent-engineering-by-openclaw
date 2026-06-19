# NousResearch/Hermes-Agent：唯一内置学习循环的自改进 Agent 框架

**Stars**: 197K | **Forks**: 34.9K | **License**: MIT | **语言**: Python (82.4%), TypeScript (13.6%)

> "The self-improving AI agent built by Nous Research. It's the only agent with a built-in learning loop."

GitHub: https://github.com/NousResearch/Hermes-Agent

---

## 核心命题

Hermes-Agent 解决了一个长期困扰 Agent 开发者的根本问题：**Agent 如何真正从经验中学习，而不是每次对话都从零开始？**

它的答案是：**在运行时动态创建和改写 Skills，形成一个闭环的学习飞轮。**

---

## 是什么让 Hermes 与众不同

### 1. 内置学习循环（The Built-in Learning Loop）

大多数 Agent 框架的「学习」本质上是把对话历史塞给下一个 Context Window——本质上还是在靠更多 Token，而不是真正的学习。

Hermes 的学习循环是结构化的：

- **任务完成后自动创建 Skill**：Agent 识别到某个复杂任务被成功执行 → 抽象出可复用的 Skill
- **Skill 在使用中自我改进**：同一个 Skill 被调用时，Agent 会评估上次执行效果，决定是否更新 Skill 逻辑
- **跨会话检索**：FTS5 全文搜索 + LLM summarization，每次对话都能召回历史经验

> "It creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions."

这和 Anthropic 文章中的 **Evaluator-Optimizer 模式**高度一致——只是 Hermes 把这个模式本身变成了框架的内置能力，而不是需要自己实现的东西。

---

### 2. 多后端并行委托（Parallelized Subagents）

Hermes 支持派生出隔离的 subagents 执行并行工作流：

> "Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns."

这对应 Anthropic 文章里的 **Orchestrator-Workers 模式**。关键差异是：Hermes 的 subagents 是**隔离上下文**的，意味着不会相互干扰，且每个 subagent 的调用不计入主对话的 context 成本。

---

### 3. 多消息平台网关（Multi-Platform Gateway）

不同于大多数 CLI-only 的 Agent，Hermes 内置了统一的消息网关：

| 平台 | 用途 |
|------|------|
| Telegram | 移动端随时唤醒，Agent 在云端 VM 工作 |
| Discord | 团队协作入口 |
| Slack | 企业工作流集成 |
| WhatsApp / Signal | 私密通信 |
| Email | 异步任务触发 |

> "It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM."

笔者认为这个设计非常有工程价值：**让 Agent 跑在云端，而交互层可以是任何消息平台**。这解决了「Agent 在后台跑任务，但我如何感知和控制它」的问题。

---

### 4. 任意模型支持（Model Agnostic）

Hermes 不绑定特定模型提供商：

> "Use any model you want — Nous Portal, OpenRouter (200+ models), NovitaAI, NVIDIA NIM, Xiaomi MiMo, Kimi/Moonshot, MiniMax, Hugging Face, OpenAI, or your own endpoint."

这降低了采用门槛，尤其对于需要**在特定模型能力/成本之间切换**的场景。

---

## 架构设计亮点

### Skill 系统（核心创新）

Skill 是 Hermes 的原子能力单元。它的设计哲学是：

1. **Skill 由经验生成**，而非人工预定义
2. **Skill 自我演化**，每次执行后评估是否改进
3. **Skill 可被发现**——通过 `/skills` 或 `/<skill-name>` 调用

这个设计解决了 Agent 领域的两个核心矛盾：

- **预定义 Skill 的局限性**：人工定义 Skill 无法覆盖所有场景
- **动态生成的不稳定性**：完全靠即时生成缺乏持久性

Hermes 的解法是：**生成是动态的，但一旦被验证有效，就固化到 Skill 中持续复用。**

### 持久化记忆架构

Hermes 的记忆系统分三层：

| 层级 | 机制 | 用途 |
|------|------|------|
| **会话内** | 标准 Context | 当前任务上下文 |
| **跨会话** | FTS5 + LLM summarization | 历史经验召回 |
| **用户模型** | Honcho dialectic modeling | 用户偏好/工作风格 |

这和 R456 周提到的 **selective memory LLM** 方向一致，但 Hermes 走得更远——它是主动「nudge」（推动）自己记住重要信息。

---

## 竞品对比

| 维度 | Hermes-Agent | 普通 Agent 框架 |
|------|-------------|---------------|
| 学习机制 | 内置学习循环，Skill 自改进 | 无，或靠更多 context |
| Subagent | 隔离上下文，并行 RPC | 共享 context |
| 平台 | 6种终端 + 消息网关 | CLI only |
| 模型 | 任意 provider | 绑定特定模型 |
| 部署 | VPS → GPU cluster → serverless | 需要固定服务器 |

---

## 适用场景

**强烈推荐使用 Hermes 如果：**

- 你需要一个能**在长生命周期内积累经验**的 Agent（而非每次从零开始）
- 你需要在**多平台**与 Agent 交互（手机/桌面/消息工具）
- 你的团队需要**不同的人都能调用同一个 Agent**（而非各自维护自己的 Agent 实例）
- 你想快速验证 Agent 概念，但不想被特定云服务商锁定

**不太适合如果：**

- 你只需要一个简单的单次任务执行器（可能过度设计）
- 你的团队完全在本土云环境，外部 API 访问受限

---

## 快速上手

```bash
# Linux/macOS 一键安装
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows 原生安装（PowerShell）
iex (irm https://hermes-agent.nousresearch.com/install.ps1)

# 启动对话
hermes

# 配置 Nous Portal（一个命令搞定所有配置）
hermes setup --portal
```

---

## 原文引用

1. "It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions."

2. "Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns."

3. "It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM."

---

*推荐_stars: 197K | 推荐理由: 唯一内置学习循环的 Agent 框架，Skill 自改进机制填补了「Agent 如何真正学习」这个工程空白。*
