# forge：让本地 LLM 工具调用从「玄学」变成「工程」

> 本项目解决了一个长期困扰自托管 LLM 社区的问题：本地模型的工具调用可靠性极不稳定，明明模型能力足够，却因为输出格式错误导致整个 agentic loop 崩溃。forge 通过在推理层注入可靠性机制，让 8B 本地模型也能达到 84% 的工具调用成功率。

## 核心命题

forge 的核心价值主张非常清晰：**模型能力不等于工具调用可靠性**。一个 8B 参数的本地模型在工具调用任务上可能只有 30-40% 的成功率，并非因为模型「不够聪明」，而是因为推理过程中的解析失败、重试机制缺失、响应验证缺位。forge 正是针对这三个环节设计了一个可靠性中间层。

笔者认为，这个定位击中了当前 AI Agent 部署的一个核心矛盾：**越来越多人希望用本地模型跑 agent 工作流，但本地模型的输出稳定性远不如云端 API**。forge 的出现让这个矛盾有了工程解法，而非只能靠「换更强模型」或「接受高失败率」二选一。

## 一、技术架构：三层可靠性机制

forge 的设计围绕三个核心组件展开：

### 1.1 Guardrails Stack（护栏堆栈）

> "Forge's guardrails (rescue parsing, retry nudges, response validation) apply with zero required steps too."

护栏堆栈包含三层机制：
- **Rescue parsing**：当模型输出无法被解析为有效工具调用时，自动进行格式修复
- **Retry nudges**：当解析失败时，给模型一个修正提示，让它重新尝试
- **Response validation**：验证模型响应是否符合预期格式和约束

这三个机制共同构成了一个**自动修正回路**，无需人工干预即可处理大部分输出格式问题。

### 1.2 WorkflowRunner（工作流运行器）

> "Forge manages the full lifecycle: system prompts, tool execution, context compaction, and guardrails."

WorkflowRunner 是 forge 的核心执行引擎，负责：
- 管理完整的 agentic loop 生命周期
- 处理系统提示词
- 执行工具调用
- 上下文压缩
- 应用护栏机制

值得注意的是，WorkflowRunner 支持**可选的结构化约束**（`required_steps`、`prerequisites`、`terminal_tool`），但这些约束不是必须的——即使不定义任何结构，forge 的护栏机制也会生效。

### 1.3 SlotWorker（插槽工作者）

> "SlotWorker adds priority-queued access to a shared inference slot with auto-preemption — for multi-agent architectures where specialist workflows share a GPU slot."

SlotWorker 是针对多 Agent 场景设计的高阶组件，提供了：
- **优先级队列**：多个 Agent 工作流共享一个 GPU 推理插槽
- **自动抢占**：高优先级任务可中断低优先级任务
- **多 Agent 协调**：让 specialist workflows 共享稀缺资源

这个设计体现了作者对真实部署场景的理解——当你在本地跑多个 Agent 时，GPU 资源往往是最大的瓶颈。

## 二、三种使用模式

forge 提供了三种接入方式，覆盖从「即插即用」到「深度定制」的需求光谱：

### 2.1 Proxy Server（代理服务器）

> "Drop-in proxy (`python -m forge.proxy`) speaking both the OpenAI chat-completions and Anthropic Messages (`/v1/messages`) APIs, sitting between any client and a local model server."

这是最受欢迎的接入方式——你不需要修改任何代码，只需在客户端和模型服务器之间插入 forge proxy，它会透明地应用护栏机制。

**关键能力**：支持 Claude Code 通过 proxy 方式使用 forge。这意味着你可以在本地跑 Claude Code，同时享受 forge 的可靠性增强。

### 2.2 WorkflowRunner（直接集成）

当你需要更精细的控制时，可以直接使用 WorkflowRunner API：
- 定义自己的工具集
- 选择推理后端
- 运行结构化 agentic loop

### 2.3 Guardrails Middleware（中间件模式）

> "Use forge's reliability stack inside your own orchestration loop."

如果你已经有自己的编排框架，可以只引入 forge 的可靠性堆栈，作为独立中间件使用。

## 三、实测数据：可靠性提升显著

forge 的文档给出了清晰的性能数据：

| 模型 | 原始成功率 | 使用 forge 后 | 提升幅度 |
|------|-----------|---------------|---------|
| 8B 本地模型（eval suite v0.7.0）| ~30-40%（估算）| 84% | +44-54% |
| Sonnet 4.6（eval suite v0.6.0）| 85% | 98% | +13% |

对于本地模型来说，这个提升幅度是惊人的——从「基本不可用」到「可以投入生产」。

笔者认为，这个数据的意义不仅在于数字本身，更在于它揭示了一个规律：**工具调用的可靠性瓶颈往往不在模型能力，而在推理层的错误处理机制**。当你在模型输出和工具执行之间加入一层健壮的解析-验证-重试机制后，即使是参数量较小的模型也能表现出稳定的工具调用能力。

## 四、与 Claude Agent SDK 的关联

本轮 Article 分析了 Anthropic 的 Claude Agent SDK 设计哲学：Agent 需要「操作计算机的能力」和「验证工作的能力」。

forge 的设计与此高度呼应：
- **工具层**：forge 的护栏机制本质上是在模型和工具之间建立一个验证层，确保模型输出能被正确解析和执行
- **验证层**：forge 的 Response validation 对应了 Claude Agent SDK 中「Verify your work」的三种方法（Rules / Assertions / Evals）
- **可靠性**：两者都指向同一个目标——让 Agent 的输出可预期、可验证、可修复

区别在于：
- Claude Agent SDK 是**设计指南**，告诉你应该怎么设计工具和验证机制
- forge 是**工程实现**，告诉你如何在本地模型上实际做到这一点

## 五、适用场景判断

**适合使用 forge 的场景**：
- 自托管 LLM 作为推理后端（Ollama、llama-server、vLLM）
- 需要在资源受限环境跑 Agent 工作流
- 对工具调用可靠性要求高，无法接受频繁失败
- 使用 Claude Code 但希望通过本地模型降低成本

**不适合使用 forge 的场景**：
- 已有成熟云端 API（Anthropic/OpenAI），且成本可接受
- 场景复杂度高，需要真正的多 Agent 编排（forge 明确表示「不是 agent orchestrator」）

## 六、快速上手

```bash
# 安装
pip install forge-guardrails

# 启动 proxy（连接到本地 llama-server）
python -m forge.proxy

# 或者使用 Anthropic API
pip install "forge-guardrails[anthropic]"
export ANTHROPIC_API_KEY=sk-...
python -m forge.proxy --backend anthropic

# 将 Claude Code 指向 proxy
export ANTHROPIC_API_BASE=http://localhost:8080/v1
export ANTHROPIC_API_KEY=unused
```

---

**引用来源**：
- GitHub: [antoinezambelli/forge](https://github.com/antoinezambelli/forge)（MIT, Python 3.12+, 2053 stars）

**相关主题**：
- Article：[Anthropic Claude Agent SDK：赋予 Agent 计算机能力与自我验证闭环](../fundamentals/anthropic-claude-agent-sdk-computer-as-tool-verification-loop-2026.md)