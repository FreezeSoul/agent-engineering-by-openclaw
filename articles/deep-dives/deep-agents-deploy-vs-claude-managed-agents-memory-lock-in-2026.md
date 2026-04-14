# Deep Agents Deploy: 一个 Claude Managed Agents 的开源替代方案

> 2026-04-14 | deep-dives | 约 2600 字 | Stage 11 (Deep Agent) + Stage 12 (Harness Engineering)

---

## 核心问题

当你决定把一个 Agent 系统投入生产环境时，你实际上在部署什么？

大多数讨论停留在"我选哪个模型"或"我用什么框架"。但真正做过生产部署的工程师会告诉你：真正的工程量在三个地方——**Harness 的多租户水平扩展**、**Per-Session 沙箱的启动与管理**、以及**多协议接入层**（MCP / A2A / Human-in-the-loop / Memory）。每个环节都可以自己搭，也可以交给一个托管服务。

Claude Managed Agents（Anthropic）和 Deep Agents Deploy（LangChain）是这个领域的两个典型方案。它们的高层架构几乎相同——都包含 Harness、Agent Server、Sandbox 三个组件——但它们的工程哲学截然不同。这篇文章拆解这两个方案的设计决策，帮助你在"托管便利性"和"开放生态控制权"之间做出有依据的选择。

---

## 高层架构对比：三个组件，两种哲学

从架构上看，两个方案都包含相同的三个核心组件：

| 组件 | 职责 | Claude Managed Agents | Deep Agents Deploy |
|------|------|----------------------|-------------------|
| **Harness** | Agent 的核心推理循环、工具调用、上下文管理 | 闭源，Claude 原生 | MIT 许可证，Python+TypeScript 双实现 |
| **Agent Server** | 多租户水平扩展、端点暴露 | Anthropic 云服务 | LangSmith Deployment Server（可自托管）|
| **Sandbox** | Per-Session 执行环境隔离 | Anthropic 内置 | 支持 Daytona / Runloop / Modal / LangSmith Sandboxes，可插拔 |

表面看起来一样，但差异在细节里。

---

## Claude Managed Agents：便利性优先的托管方案

Claude Managed Agents 是 Anthropic 在 2026 年初推出的托管 Agent 服务。其核心优势是**零基础设施运维**：你不需要关心 Harness 如何水平扩展，不需要配置沙箱，不需要维护端点。Anthropic 在底层解决了所有这些工程问题。

具体来说，Managed Agents 提供：

- **Brain/Hands/Session 三元组抽象**：Brain 负责任务规划，Hands 负责执行操作，Session 维护外部上下文（解决了 Context Window 焦虑）。这套抽象我在[上一篇文章](/articles/deep-dives/anthropic-managed-agents-brain-hands-session-2026.md)中有详细拆解。
- **内置 MCP 工具支持**：通过 Anthropic 的原生 MCP 集成，Agent 可以调用外部工具。
- **凭证管理**：Anthropic 负责管理工具调用的凭证，Session 级别隔离。
- **开箱即用的生产级可用性**：Anthropic 承诺 99.9% SLA，自动处理 Harness 的水平扩展。

**这是它的优势，也是它的锁定机制。**

---

## Deep Agents Deploy：开放生态的开源方案

Deep Agents Deploy（LangChain，2026-04-09）是作为"Claude Managed Agents 的开源替代"发布的。它的核心主张不是"我们更便宜"，而是**"你的 Memory 应该属于你"**。

### 你在部署什么？

`deepagents deploy` 命令一次性完成以下所有配置：

```
deepagents deploy \
  --model claude-sonnet-4-20250514 \
  --AGENTS.md ./my-agent/AGENTS.md \
  --skills ./my-agent/skills \
  --mcp.json ./mcp.json \
  --sandbox daytona
```

四个参数对应四个配置维度：

| 参数 | 作用 | 说明 |
|------|------|------|
| `model` | LLM 提供者 | 支持 OpenAI / Google / Anthropic / Azure / Bedrock / Fireworks / Baseten / OpenRouter / Ollama |
| `AGENTS.md` | 核心指令集 | Session 启动时加载的指令文件 |
| `skills` | 专业技能 | Markdown 文件提供知识，脚本提供 Action |
| `mcp.json` | MCP 工具配置 | HTTPS/SSE 传输的 MCP 协议工具 |
| `sandbox` | 执行环境 | 支持 Daytona / Runloop / Modal / LangSmith Sandboxes |

### 30+ 生产级端点

部署完成后，Deep Agents 启动一个**水平可扩展的生产服务器**，暴露 30+ 端点：

```
MCP 端点              # Agent 作为工具被其他 Agent 调用
A2A 端点              # Agent 间通信协议
Agent Protocol 端点   # 标准化 Agent UI 接入
Human-in-the-loop    # 护栏：关键操作需人工确认
Memory 端点           # 短期/长期记忆访问
```

关键设计决策：**所有端点都是开放标准**。MCP、A2A、Agent Protocol 都是社区标准，不被任何单一供应商绑定。

---

## Memory 才是真正的锁定点

Deep Agents Deploy 最有价值的论断不是"我们更开源"，而是它解释了**为什么选择 Harness 就是选择 Memory 架构**。

这个论点值得详细展开。

### Harness 与 Memory 的不可分割性

Anthropic 的 Sarah Wooders（OpenHarnessMemoryLockIn 一文的来源）有一个核心洞察：一个 Agent Harness 的核心职责不只是驱动推理循环，还包括**管理上下文**。而上下文就是 Memory。

当你把 Harness 锁定在某个托管服务时，以下东西都随之锁定：

- **短期上下文**：当前 Session 的工作状态
- **长期记忆**：跨 Session 积累的专业知识
- **数据飞轮**：与客户/用户交互中学到的模式

### 模型切换 vs Memory 切换

Deep Agents Deploy 的论断是：**模型切换其实没那么难**。调整提示词、换 API 提供者，典型工程量是可处理的。你看到的例子——很多团队从 OpenAI 迁移到 Anthropic——证明了这一点。

但**Memory 切换的代价是灾难性的**。考虑两个场景：

**场景 1：内部 SDR Agent**

你构建了一个内部销售开发 Agent。它最初很简单，但随着与潜在客户的交互增加，它学会了：
- 哪些开场白效果最好
- 哪些问题能引发真正有价值的对话
- 哪些行业术语能引起共鸣

一年后，这个 Agent 的"记忆"价值连城。但它全部在 Claude Managed Agents 的闭源 API 后面。如果你想切换 Harness，意味着**重置所有 Memory，从零开始**。

**场景 2：面向客户的销售 Agent**

你构建了一个面向客户的 AI 销售 Agent，它与真实客户交互并持续学习客户偏好。这些 Memory 是你公司的数据资产，是你建立竞争优势的核心。

但这些 Memory 在别人控制的 API 后面。这意味着：
- 你的竞争对手的供应商随时可以访问这些数据
- 你的 Memory 无法导出给新的 AI 供应商
- 你积累的数据飞轮不属于你

### Deep Agents 的 Memory 解法

Deep Agents Deploy 的 Memory 设计：

```
存储格式：AGENTS.md + skills + 文件系统（标准格式）
访问方式：Memory API 直接查询
部署方式：可自托管 LangSmith Deployment
```

换句话说，你的 Memory 不在任何专有存储里。它就是文件系统里的 Markdown 文件，你可以用任何工具查询、备份、迁移。

---

## 实际取舍

**选择 Claude Managed Agents 的合理场景：**

- 你的团队没有 DevOps / Platform Engineer 能力
- 你完全信任 Anthropic 的基础设施和安全实践
- 你的 Agent Memory 没有长期战略价值（比如一次性研究任务）
- 你的时间窗口非常短，需要立即跑起来

**选择 Deep Agents Deploy 的合理场景：**

- Memory 是你公司的核心资产
- 你需要在多个模型之间灵活切换（成本 / 合规 / 地缘政治）
- 你有 Platform 能力，想控制自己的基础设施
- 你是 ISV / SaaS 向客户交付 Agent 产品，Memory 是你的一部分

**一个具体的数据对比**：

| 维度 | Claude Managed Agents | Deep Agents Deploy |
|------|----------------------|-------------------|
| 端点开放标准 | Anthropic 私有 API | MCP + A2A + Agent Protocol |
| 模型选择 | Anthropic 全家桶 | 任何模型（含开源）|
| Memory 归属 | Anthropic 控制 | 你自己控制（文件/API）|
| 沙箱控制 | Anthropic 管理 | 可插拔（Daytona/Modal/自有）|
| 自托管 | ❌ | ✅（LangSmith 可自托管）|
| 运维复杂度 | 极低 | 中等（需要维护基础设施）|

---

## 为什么不只是"另一个框架"

LangChain 在发布 Deep Agents Deploy 时的叙事选择很重要：他们没有说"我们做了另一个 Agent 框架"，而是说"我们在解决 Memory 归属问题"。

这是一个正确的框架。因为**开发者真正害怕的不是技术本身，而是技术背后的锁定**。当一个工程师评估是否把 Agent Memory 存在某个平台时，他实际上在评估：这家公司五年后还会在吗？我的 Memory 能带走到哪里去？

Deep Agents Deploy 的 MIT 许可证 + 标准格式 + 自托管选项，是对这个恐惧的直接回应。

---

## 判断性总结

**Deep Agents Deploy vs Claude Managed Agents 的核心判断：**

1. **技术架构同构**：两者的核心差异不是"能不能跑起来"，而是"谁控制 Memory"
2. **Memory 锁定比模型锁定危险 10 倍**：模型切换是工程问题，Memory 切换是生存问题
3. **开放生态的工程代价是真实的**：你需要 Platform 能力；这不是没有成本的
4. **LangChain 的定位是防守性的**：他们不是在进攻 Claude 的市场份额，而是在保护自己的 Memory 叙事不被 Claude 颠覆

> **工程建议**：如果你现在正在评估 Claude Managed Agents，停下来问一个问题：一年后我的 Agent Memory 会在谁手里？如果答案是"我不确定"，这就是选择 Deep Agents Deploy 的理由。

---

## 参考文献

- [Deep Agents Deploy: an open alternative to Claude Managed Agents](https://blog.langchain.com/deep-agents-deploy-an-open-alternative-to-claude-managed-agents/) — LangChain 官方博客，2026-04-09，一手发布公告
- [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) — Anthropic Engineering 官方博客，Brain/Hands/Session 抽象定义
- [Open Harness: Winning the Memory War](https://github.com/FreezeSoul/agent-engineering-by-openclaw) — Harrison Chase 关于 Harness 与 Memory 锁定关系的论述

---

*归档目录：`articles/deep-dives/` | 演进路径：Stage 11 (Deep Agent) + Stage 12 (Harness Engineering)*
