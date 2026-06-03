# OpenAI Codex Agent Loop：Harness 工程的底层架构解析

> **核心观点**：Codex Agent Loop 的本质是一个**状态机式的推理-执行交替循环**，而真正体现工程功力的不是这个循环本身，而是**上下文窗口管理与输出截断策略**——这是让 Agent 在长对话中不崩溃的关键。

## 一、为什么理解 Agent Loop 很重要

过去一年多，社区里充斥着各种"Agent 框架"的讨论：LangChain 的 LCEL、AutoGen 的 group chat、CrewAI 的 crew orchestration。但大多数讨论停留在**编排层**——即"几个 Agent 之间怎么协作"。真正底层的**Harness 工程**问题，反而被忽略了。

所谓 Harness，就是让 LLM 真正跑起来的那个"轮子"：它负责把用户的输入变成 prompt，把模型的输出变成工具调用，把工具的返回结果塞回 prompt，然后循环。这个过程里，有大量的工程决策直接影响 Agent 的可用性和稳定性。

OpenAI 在 2026 年 6 月发布的这篇技术博客（[Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/)），罕见地披露了 Codex CLI（GitHub 88k+ Stars）的核心架构设计。本文从 Harness 工程的角度，深度拆解其中的关键设计决策。

## 二、Agent Loop 的本质：状态机，而非简单的推理循环

大多数文章在描述 Agent 时，会画一个简单的图：Input → LLM → Tool → Output → LLM → ... 循环。这没有错，但过于简化。

Codex 的官方描述更精确地揭示了本质：

> "The journey from user input to agent response shown in the diagram is referred to as **one turn of a conversation** (a thread in Codex). Though this conversation turn can include many iterations between the model inference and tool calls."

这里的关键词是**"one turn"**——在 Codex 的语义里，一次对话回合（turn）**不是**一次推理（inference），而是**包含多次推理-工具调用迭代**的完整工作单元。

这个设计有一个关键推论：**每个 turn 都会累积上下文**。当你在一个已有 50 条消息的 thread 里发一条新消息，Codex 会把**整个对话历史**作为 prompt 的一部分发给模型：

> "Every time you send a new message to an existing conversation, the conversation history is included as part of the prompt for the new turn, which includes the messages and tool calls from previous turns."

这意味着：**上下文窗口管理不是优化问题，而是生存问题**。一个活跃使用了一周的 Codex 项目，turn 数量可能已经高达数百次，上下文长度轻松超过 128k token。

## 三、Context Window 管理：Harness 的核心工程挑战

### 3.1 问题的本质

每个模型都有 context window 限制（包括 input + output tokens）。Agent 的每次工具调用结果都会追加到 prompt 里，理论上一次 turn 可以产生数百次工具调用。Codex 明确指出了这个问题：

> "As you might imagine, an agent could decide to make hundreds of tool calls in a single turn, potentially exhausting the context window. For this reason, **context window management is one of the agent's many responsibilities**."

注意这里的用词：**one of the agent's many responsibilities**。OpenAI 把 context window 管理定性为 Agent 的**核心职责之一**，而不是"用更大的 context window 就解决了"的问题。

### 3.2 Codex 的解决思路

Codex 采用了分层策略，而非单一手段：

**1. 初始化 Agent（Initializer Agent）**
在第一次运行时，初始化 Agent 负责设置环境，避免在后续的每次推理中都重复环境探测的开销。这是减少单次 turn 内 token 消耗的第一道关卡。

**2. 增量式工作（Incremental Work）**
> "a coding agent that is tasked with making incremental changes"

Codex 不追求一次生成完整解决方案，而是让 agent 做**增量式修改**。每次只处理一个小目标，这样单次 turn 的工具调用数量就受到自然限制。

**3. Responses API 的 Prompt 压缩**
Codex 使用 OpenAI 的 [Responses API](https://platform.openai.com/docs/api-reference/responses/create)，而非传统的 Chat Completions API。Responses API 提供了更结构化的 prompt 组织方式：

- `instructions`：系统级指令（最高优先级）
- `input_items`：用户输入（带角色语义）
- `previous_response_id`：关联历史响应（而非直接塞入完整历史）

这种设计让 API 端有机会做 prompt 的语义压缩，而不是粗暴地截断。

### 3.3 笔者的判断

**增量式工作 + 结构化 API 的组合，是目前已知的最佳 context window 管理策略**。单纯的 context window 扩大（从 128k 到 1M）只是把问题后移，没有解决根本问题。根本问题是：Agent 在长任务中会积累大量中间状态，这些状态如果不加区分地全部塞入 context，就会导致有效信息密度下降、模型推理质量劣化。

增量式工作通过**控制单次 turn 的工作量上限**，让这个问题在架构层面得到缓解。这比任何 prompt 压缩技巧都更根本。

## 四、Model Inference 的架构细节

### 4.1 多端点支持

Codex 的 model inference 支持多种部署模式：

```rust
// Codex 源码中的端点选择逻辑
When using ChatGPT login → https://chatgpt.com/backend-api/codex/responses
When using API-key auth   → https://api.openai.com/v1/responses
When using --oss mode     → http://localhost:11434/v1/responses  (Ollama 0.13.4+)
When using Azure          → Azure-hosted Responses API
```

这个设计体现了**平台无关性**的工程思路：Codex 把 API 端点抽象为可配置项，而不是写死在代码里。这让组织可以：
- 在内部使用 ChatGPT 企业版登录
- 开发者用 API key 直连 OpenAI
- 完全离线环境用 Ollama
- 企业合规用 Azure

### 4.2 Role 优先级体系

Responses API 的 prompt 由一系列 **items** 组成，每个 item 有 role 字段：

| Role | 优先级 | 用途 |
|------|--------|------|
| `system` | 最高 | 全局指令、安全边界 |
| `developer` | 次高 | 开发者提供的调试/系统信息 |
| `user` | 中 | 用户原始输入 |
| `assistant` | 最低 | 模型历史输出（包含工具调用） |

这个优先级体系的意义在于：**越重要的信息，模型越倾向于遵循**。系统级的安全指令（system）不会被用户的一句话覆盖，即使上下文里混入了恶意指令，model 也会优先响应 system role 的内容。

## 五、安全架构：让 Agent 在边界内工作

OpenAI 同期发布的另一篇博文（[Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely)）补充了企业级部署的安全架构。这部分与 Agent Loop 的关系在于：**Harness 必须同时负责执行效率和安全边界**。

### 5.1 沙箱 + 审批的二元策略

> "The sandbox defines the technical execution boundary, including where Codex can write, whether it can reach the network, and which paths remain protected. Approval policy determines when Codex must ask to perform an action."

Codex 的安全策略是**沙箱（Sandbox）+ 审批（Approval）的组合**：

- **沙箱**：定义技术边界（文件系统写入范围、网络访问范围、受保护路径）
- **审批策略**：定义何时需要人类授权（跨沙箱边界的操作）

低风险操作在沙箱内无摩擦通过，高风险操作强制中断等待人工审批。

### 5.2 Auto-review 模式

> "Codex sends the planned action and recent context to the auto-approval subagent, which can automatically approve low-risk actions—or high-risk actions with sufficient level of user authorization"

这里有一个**二级 Agent**的设计：主 Agent 的高风险操作不是直接弹窗给用户，而是发给一个 auto-approval subagent。这个 subagent 可以：
- 自动批准低风险操作
- 对高风险操作评估用户授权级别，决定是否自动批准

这是一个**分层授权**的架构：不是所有操作都需要人工实时审批，而是通过 subagent 实现**风险分级的自动化决策**。

### 5.3 网络策略

> "Our managed network policy allows expected destinations, blocks destinations we do not want Codex reaching, and requires approval for unfamiliar domains."

Codex 不采用"白名单全部放开"或"黑名单局部禁止"的二选一，而是**三级网络策略**：
1. **允许列表**：已知的合法目标（如 npm registry、GitHub）
2. **禁止列表**：明确禁止的目标（如恶意域名）
3. **审批模式**：未知目标需要审批

这个设计解决了企业场景的典型痛点：开发者在工作时不可避免地会遇到**新域名**（比如新上线的内部服务），完全禁止会阻断工作，完全放开会造成安全风险。审批模式在两者之间找到了平衡。

## 六、与 Claude Code 的架构对比

| 维度 | OpenAI Codex | Anthropic Claude Code |
|------|-------------|----------------------|
| **核心语言** | Rust（96%） | 未公开 |
| **API 架构** | Responses API + 多端点 | Agent SDK |
| **Context 管理** | 增量工作 + 初始化 Agent | 分类器动态判断 |
| **安全模型** | 沙箱 + 审批 + Auto-review subagent | Auto Mode 分类器 |
| **网络策略** | 三级（允许/禁止/审批） | 未完全披露 |
| **增量策略** | 初始化 Agent + 增量修改 | 未完全披露 |

**笔者认为**，两家的安全架构设计思路一致（沙箱 + 分级审批），但在**实现深度**上有差异。Codex 的 auto-approval subagent 是一个值得关注的创新——它把"是否批准"这个决策本身变成一个可量化的 AI 决策问题，而不是简单的规则匹配。Claude Code 的 Auto Mode 分类器则更偏向于**行为分类**（决定 Agent 用什么模式运行），两者侧重点不同。

## 七、工程启示录

### 7.1 Agent Loop 不是重点，Context 管理才是

社区里大量关于 Agent 的讨论集中在"循环怎么写"——用什么框架、怎么定义工具、怎么选模型。Codex 的实践告诉我们：**Agent Loop 本身没什么秘密，真正的工程挑战是 context window 管理**。

如果你在做一个长任务 Agent，第一优先级是设计 context 管理策略，而不是优化工具定义或模型选择。

### 7.2 增量式工作是架构选择，不是权宜之计

增量式工作（每次只做一个小改动）不只是为了"不让模型一次做太多"，而是一种**架构级别的复杂度控制**。它让每个 turn 的上下文增长可控，降低了系统整体的脆弱性。

### 7.3 安全架构要从第一天设计

Codex 的安全设计不是事后打补丁，而是从第一天就融入了架构：

> "we deploy Codex with a clear goal: keep the agent inside clear technical boundaries, let developers move quickly on low-risk actions, and higher-risk actions should be explicit"

这句话的工程含义是：**安全边界是 Harness 的一部分，不是运维团队的事情**。如果你等 Agent 上线后再加安全策略，改造成本会非常高。

### 7.4 二级 Agent 是企业级安全的标准配置

Auto-approval subagent 的设计暗示了一个趋势：**在企业场景下，"谁来审批"这个问题本身也需要 AI 自动化**。完全依赖人工审批的方案在规模化时必然崩溃，二级 Agent（或者更通用的"决策路由"）是唯一出路。

## 八、结语

Codex 的这两篇博文（Agent Loop + 安全架构）组合起来，勾勒出了一个**生产级 Agent Harness 的完整架构视图**：

- **Agent Loop**：状态机式的推理-执行循环
- **Context 管理**：增量工作 + 初始化 Agent + Responses API 的结构化压缩
- **安全架构**：沙箱 + 分级审批 + Auto-review subagent
- **部署灵活性**：多端点支持（ChatGPT/API/Ollama/Azure）

这些设计不是 OpenAI 独有的创新，而是**所有认真做 Agent 的团队迟早会遇到并需要解决的问题**。理解 Codex 的设计决策，比学习某个框架的 API 调用更有长期价值。

> **金句**：真正区分生产级 Agent 和 Demo 级 Agent 的，不是有没有用 LLM，而是**上下文管理的能力边界**和**安全架构的完整程度**。

---

*本文来源：OpenAI Engineering Blog - "Unrolling the Codex Agent Loop" (2026-06) + "Running Codex safely at OpenAI" (2026-06)*
