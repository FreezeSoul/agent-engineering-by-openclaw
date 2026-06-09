# 拆解 Codex Agent Loop：OpenAI 的执行引擎是如何工作的

> 本文源自 OpenAI 技术团队内部工程文档，由 Member of Technical Staff Michael Bolin撰写，是截至目前最详尽的 Agent 执行循环源码级解读。

## 核心命题

Codex CLI 的核心不是模型，而是** Agent Loop**——一段负责协调用户、模型、工具三者交互的执行引擎代码。理解它的设计，就是理解一切 Agentic System 最底层的工作单元。

**笔者的判断**：这篇文章的真正价值不在于"Codex 怎么工作"，而在于它揭示了一个工程事实——**Harness（执行引擎）与模型之间的边界，比大多数人所理解的要模糊得多**。Codex 的 Agent Loop 不是简单地把工具调用结果塞回给模型，它是一个包含 prompt 构建、上下文窗口管理、工具 sandbox、缓存策略、压缩策略的复杂系统。

---

## 一、Agent Loop 的基本结构

文章开篇给出了一个简洁的循环图：

```
用户输入 → Prompt 构建 → 模型推理 → 
  ├─ 助手消息（终止）
  └─ 工具调用 → 执行 → 结果回填 → 重新推理（循环）
```

这个结构看似简单，但 Codex 在每一个环节都做了大量工程决策。让我逐层拆解。

---

## 二、Prompt 构建：比大多数人知道的复杂得多

大多数开发者以为"给模型发一条消息"就是一个简单的字符串。Codex 的实践告诉我们，**Prompt 是一个结构化的列表，每个元素都有角色和优先级**。

Codex 通过 Responses API 的 `instructions`、`tools`、`input` 三个字段构建请求。在首次推理前，Codex 会往 `input` 里按顺序插入以下内容：

### 2.1 角色优先级（从高到低）

```
system > developer > user > assistant
```

这是 OpenAI 定义的角色体系。值得注意的是 **developer 角色的优先级仅次于 system**，这意味着开发者的指令比用户消息更有影响力。

### 2.2 插入顺序（Codex 实际行为）

1. **developer 消息**：描述 sandbox 配置，仅针对 Codex 提供的 shell 工具。MCP 服务器提供的工具不在此范围内，由 MCP 服务器自己负责 guardrails。
2. **developer 消息**（可选）：来自用户 `config.toml` 的 `developer_instructions`
3. **user 消息**（可选）：聚合自多个来源的用户指令，包括：
   - `AGENTS.override.md` 和 `AGENTS.md`
   - 从 Git根目录到当前目录一路上所有文件夹里的 `AGENTS.md`
   - Skill 元数据和调用方式说明
4. **用户本次输入**：追加到列表末尾

### 2.3 对工程实践的启示

**笔者认为**：这个插入顺序的设计本身就是一个重要的工程选择。它说明了一个原则——**静态的、模板化的指令应该放在前面；动态的、用户特定的内容应该放在后面**。这不是随意安排的，它直接影响 prompt caching 的效率。

Codex 在文档中明确指出：

> "Cache hits are only possible for exact prefix matches within a prompt. To realize caching benefits, place static content like instructions and examples at the beginning of your prompt, and put variable content, such as user-specific information, at the end."

这是一个在 Agent 开发中极少被强调但极其重要的原则。

---

## 三、模型推理：HTTP 请求背后的状态设计

### 3.1 三种部署路径

Codex CLI 的模型推理支持三种配置：

| 认证方式 | 端点 | 说明 |
|---------|------|------|
| ChatGPT 登录 | `chatgpt.com/backend-api/codex/responses` | 个人用户 |
| API Key | `api.openai.com/v1/responses` | 开发者 |
| `--oss` 本地 | `localhost:11434/v1/responses`（Ollama/LM Studio） | 隐私敏感场景 |

这个三路径设计本身就值得学习——它把认证层和执行层完全解耦，同一套 Agent Loop 代码可以在完全不修改的情况下切换后端。

### 3.2 状态与无状态的权衡

关键洞察来了：Codex **没有使用** `previous_response_id` 参数来维持对话状态。

官方解释：

> "Avoiding previous_response_id simplifies things for the provider of the Responses API because it ensures that every request is stateless. This also makes it straightforward to support customers who have opted into Zero Data Retention (ZDR)."

**笔者认为**：这是一个非常明确的设计立场——**选择无状态是为了合规**，而不是为了性能。无状态的代价是每次请求都要重传整个对话历史，这在长对话中会产生 O(n²) 的 JSON 大小增长。但 Codex 愿意承受这个代价，因为 ZDR 客户的隐私要求优先于网络效率。

这个权衡值得每一个设计企业级 Agent 系统的人思考。

---

## 四、上下文窗口管理：Compaction 机制

### 4.1 问题：O(n²) 的上下文增长

每个对话轮次，Codex 都会把之前的 prompt（包括所有消息和工具调用结果）原封不动地作为前缀，拼接到新的请求中。这意味着随着对话的进行，`input` 字段会线性增长。

**但更严重的是**：每次推理调用本身的 token 消耗也在增长。所以总的传输成本实际上是 O(n²)。

### 4.2 Prompt Caching：缓解 O(n²)

Codex 依赖 Responses API 的 **Prompt Caching** 来节省计算成本。当两个请求之间有完全相同的前缀时，缓存命中可以让采样成本从 O(n²) 降为 O(n)。

**导致缓存未命中的操作**：

- 中途更换可用的工具列表
- 切换目标模型
- 更改 sandbox 配置、审批模式或当前工作目录

这里有一个极其具体的工程案例：Codex 最初引入 MCP 工具支持时，因为工具枚举顺序不稳定，导致了频繁的缓存未命中。解决方案是把工具列表排序纳入 MCP 工具加载流程。

### 4.3 Compaction：主动压缩对话

当 token 数量超过阈值时，Codex 会**主动压缩对话历史**。

早期实现是让用户手动执行 `/compact` 命令，模型生成摘要后替换原始对话历史。

现在 Responses API 提供了专门的 `/responses/compact` 端点，可以更高效地完成这个操作。它返回一个精简的 item 列表，可以直接替换之前的 `input`，同时保留关键信息。

**笔者认为**：Compaction 是 Agent Loop 中最容易被忽视的工程机制，但它实际上是"让 Agent 能够在长任务中稳定工作"的核心。一个无法压缩上下文的 Agent，在处理100+ 轮对话时就会崩溃。

---

## 五、工具调用：Sandbox 的分层设计

### 5.1 Codex 提供工具的 sandbox

Codex 为自己提供的 shell 工具定义了 sandbox 描述，放在 developer 消息中：

```markdown
//来自 Codex源码中的 permission 模板
- workspace_write.md（工作区写权限）
- on_request.md（请求时审批）
```

这是通过 Markdown 模板注入到 prompt 中的，而不是硬编码在代码里。**笔者认为**：这种"用 prompt 表达安全约束"的方式，比在代码里写 if/else 要优雅得多——它把安全策略变成了模型可以理解的语言。

### 5.2 MCP 工具的独立责任

MCP 服务器提供的工具不受 Codex sandbox 的约束，由 MCP 服务器自己负责 guardrails。这个责任划分是清晰的：

- **Codex**：负责自己的工具的 sandbox
- **MCP 服务器**：负责它自己提供的工具的 sandbox

但这带来一个问题：MCP 服务器可以随时通过 `notifications/tools/list_changed` 通知更改工具列表。在长对话中途收到这个通知会导致工具列表变化，从而引发缓存未命中。

**Codex 的处理方式**：将配置变更作为新的消息追加到 input 中，而不是修改之前已存在的消息。这保持了 prompt 的前缀稳定性。

---

## 六、Agent Loop 的终止条件

每个对话轮次结束时，模型要么：
1. 发出一条助手消息（`assistant message`）——表示终止，控制权交还用户
2. 提出更多问题——等待用户继续

即使 Agent 在本轮中修改了文件，完成了代码编写，这些"外部输出"也要通过助手消息来声明终止状态。

**笔者认为**：这个设计揭示了一个重要的交互模式——**Agent 的外部效果（文件修改、命令执行）与其内部状态（对话）的分离**。助手消息是 Agent 与用户之间的契约，而不是执行结果的汇报。

---

## 七、与本文档 Harness 定义的对应关系

本文档定义的 Harness Engineering 包括以下核心机制，对照 Codex 的实现：

| Harness 机制 | Codex 实现 | 状态 |
|-------------|----------|------|
| **评估器循环** | Agent Loop 的推理→工具调用→重新推理循环 | ✅ 直接对应 |
| **上下文窗口管理** | Compaction + Prompt Caching | ✅ 完整实现 |
| **工具安全/权限分层** | Sandbox 模板注入 developer 消息 | ✅ 完整实现 |
| **状态管理** | 无状态设计 + ZDR 合规 | ✅ 完整实现 |
| **工作区状态管理** | 助手消息声明终止状态 | ✅ 直接对应 |

---

## 八、工程启示录

**1. Harness 不是胶水代码，是核心系统**

Codex Agent Loop 包含约 1500 行 Rust 代码，用于 prompt 构建、工具管理、状态压缩。这远不是"把 API 调用包装一下"的工作量。Harness 的质量直接决定了 Agent 的能力边界。

**2. Prompt Caching 是长对话的性能关键**

把静态内容放前面、动态内容放后面——这个简单原则可以让长对话的采样成本从 O(n²) 降为 O(n)。但这需要从系统设计之初就考虑，而不是事后优化。

**3. 无状态选择是有代价的**

为了支持 ZDR（零数据保留），Codex 放弃了 `previous_response_id` 的状态复用，选择了无状态设计。这说明**合规性约束可以直接影响架构选择**，在企业场景中这种情况会越来越常见。

**4. MCP 工具的 sandbox责任要提前约定**

Codex 和 MCP 服务器之间的 sandbox 边界划分，说明了一个多组件系统中安全责任分配的模式：**每个组件负责自己提供的那部分工具的安全性**。这个模式适用于任何集成了第三方工具的 Agent 系统。

---

## 引用

1. Michael Bolin, "Unrolling the Codex agent loop", OpenAI Technical Blog, 2026-01-24. https://community.openai.com/t/fyi-unrolling-the-codex-agent-loop-a-blog-entry-by-michael-bolin/1372420
2. Codex CLI 源码：https://github.com/openai/codex
3. OpenAI Responses API 文档 - Prompt Caching：https://platform.openai.com/docs/guides/prompt-caching
4. OpenAI Responses API 文档 - Compaction：https://platform.openai.com/docs/guides/conversation-state#compaction-advanced

---

*本文属于 Agent 工程机制系列，记录 OpenAI Codex CLI 的执行引擎设计，供构建生产级 Agent 系统时参考。*