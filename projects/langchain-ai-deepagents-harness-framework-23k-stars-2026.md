# langchain-ai/deepagents：23.8K Stars 的模型无关 Agent Harness 框架

> **核心问题**：当你想要一个开箱即用的生产级 Agent 时，LangGraph 提供了图运行时，LangChain 的 `create_agent` 提供了最小化 Agent，但这两者之间缺少一个有opinionated defaults的生产级 Harness。Deep Agents 就是填这个坑的。
>
> **读完能得到什么**：判断 Deep Agents 是否适合你的 Agent 项目；理解它与 LangGraph/LangChain 的层次关系；以及它的 Interpreter 模式和 Skills 系统如何让 Agent 真正能够长时间运行。

---

## 核心命题

Deep Agents 主页的描述足够直接：

> "Deep Agents is an open source agent harness — an opinionated agent that runs out of the box. Extend, override, or replace any piece."

这句话的关键词是「opinionated」和「out of the box」。LangGraph 给你底层图运行时，LangChain 给你最小化构建块，Deep Agents 则直接给一个**有默认配置的完整 Agent**，同时保留每个组件可替换的扩展性。

截至 2026 年 6 月，Deep Agents 达到 **23.8k Stars、159 个 Release**，最新版本 0.6.8 发布于 2026 年 6 月 3 日——这个项目的活跃度在开源 Agent 框架中是第一梯队。

---

## 二、为什么它是「batteries-included」

### 2.1 与 LangGraph/LangChain 的层次关系

这是理解 Deep Agents 最关键的问题。官方 FAQ 给出了清晰的层次划分：

| 层级 | 项目 | 职责 |
|------|------|------|
| **Graph Runtime** | LangGraph | 状态图执行引擎 |
| **Minimal Harness** | LangChain `create_agent` | 最小化 Agent 构建块 |
| **Opinionated Harness** | Deep Agents | 有默认配置的完整 Agent |

笔者的理解：Deep Agents 就是在 LangChain 的 minimal agent 基础上，把 filesystem、sub-agents、context management、skills 这些在实际生产中必需的组件**默认打包进来**，而不是让每个团队自己从零组装。

### 2.2 核心 Feature

- **Model-agnostic**：任何支持 tool calling 的模型都能用，包括 OpenAI、Anthropic、Google 等 Frontier 模型，也包括 Baseten、Fireworks 等托管开源模型，以及通过 Ollama、vLLM、llama.cpp 自托管的模型
- **Built on LangGraph**：所有组件返回编译好的 LangGraph 图，支持 streaming、persistence、checkpointing
- **First-class LangSmith 集成**：开箱即用的 tracing、evaluation、deployment
- **Sub-agents 架构**：任何 LangGraph `CompiledStateGraph` 都可以作为子 Agent 注入，形成层级化 Agent 结构

---

## 三、Interpreter 模式：让 Agent 写代码而非逐条调用

Deep Agents 的 Interpreter 实现是 LangChain 官方博客「Give Your Agents an Interpreter」的核心主题。

在 Agent 场景下，典型的问题是：**如果 Agent 每调用一次工具就产生一次模型往返，那多步计算（如循环处理一批数据）就变成了大量 token 开销**。

Deep Agents 的 Interpreter 提供了另一种路径：Agent 可以写一段代码，代码内部直接调用多个工具，最后只返回最终结果而不是每个工具调用的中间结果。

这与 Anthropic 的 Programmatic Tool Calling (PTC) 思路一致，但关键差异在于：

- **Anthropic PTC**：Model Provider 内部行为，只有 Anthropic 模型能用
- **Deep Agents PTC**：Middleware 实现，任何支持 tool calling 的模型都能用

官方原话：

> "In Deep Agents, PTC is implemented as middleware rather than as a model-provider behavior. The developer passes an allowlist, allowlisted tools appear under the global `tools` namespace, and each tool is exposed as an async function the interpreter can call with `await`."

---

## 四、Skills 系统：可复用的 Agent 能力单元

Deep Agents 的 Skills 系统让 Agent 能够加载和执行预定义的能力包。这与 OpenAI Codex Skills、Anthropic Agent Skills 的思路一致，但作为开源实现：

- **Skills 可版本化**：通过 `.agents/skills` 目录管理
- **可插拔**：同一 Agent 可以加载不同 Skills
- **LangGraph Native**：Skills 返回的也是 LangGraph 图，无缝集成

Skills 系统的设计目标：**让团队能够封装和复用 Agent 能力，而不需要每次都从 Prompt 工程重新开始**。

---

## 五、安全设计哲学

Deep Agents 的安全文档值得单独拿出来说：

> "Deep Agents follows a 'trust the LLM' model. The agent can do anything its tools allow. Enforce boundaries at the tool/sandbox level, not by expecting the model to self-police."

这是一个务实的立场：**不在模型层假设自我约束，而在工具/沙箱层强制边界**。这与 Claude Code 的安全设计哲学一致，也是生产级 Agent 系统的共识。

---

## 六、竞品对比

### 与 Claude Code / Cursor 对比

Claude Code 和 Cursor Composer 是最成熟的 Coding Agent 产品，拥有完整的 IDE 集成和用户界面。Deep Agents 的定位不同：它是 **Harness 框架**，面向的是开发者**自己构建 Agent**，而不是使用别人的产品。

Deep Agents 的 README 直接说了这个 Inspiration：

> "Inspired by Claude Code: an attempt to identify what makes it general-purpose, and push that further."

### 与 CrewAI / AutoGen 对比

CrewAI 和 AutoGen 也是开源多 Agent 框架。Deep Agents 的差异化在于：
- **LangGraph Native**：所有能力都构建在 LangGraph 状态图之上，可组合性更强
- **Interpreter + Skills 双系统**：代码级组合和技能封装两套机制并存
- **LangSmith 集成**：从第一天就有生产级可观测性

---

## 七、适合谁用

**适合**：
- 想要快速启动生产级 Agent 的团队（不需要从 LangGraph 底层开始搭）
- 需要多模型支持的 Agent 项目（不想被某个模型 API 绑定）
- 需要 Interpreter/代码执行能力的复杂多步任务
- 已经在 LangChain/LangSmith 生态中的团队

**不适合**：
- 只需要简单 single-turn 对话的团队（LangChain 的 minimal agent 就够了）
- 需要完整 IDE/Coding UI 的场景（这属于 Claude Code/Cursor 的职责）
- 对框架依赖有严格限制的团队（Deep Agents 依赖 LangGraph/LangChain 生态）

---

## 链接

- GitHub: https://github.com/langchain-ai/deepagents
- Stars: 23.8k
- License: MIT
- 最新版本: 0.6.8 (2026-06-03)

---

> "Deep Agents is an open source agent harness — an opinionated agent that runs out of the box. Extend, override, or replace any piece."
