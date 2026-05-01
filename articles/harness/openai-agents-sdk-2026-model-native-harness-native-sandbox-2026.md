# OpenAI Agents SDK 2026：Model-Native Harness 与 Native Sandbox 架构解析

## 核心问题

OpenAI 于 2026 年 4 月 15 日发布了 Agents SDK 的重大更新，引入了 **model-native harness** 和 **native sandbox execution** 两个核心能力。这次更新的本质是什么？它与此前 Anthropic/OpenClaw 等平台的 harness 设计有何本质区别？企业如何在"灵活性 vs 专用性"之间做取舍？

---

## 背景：为什么现有方案存在根本性缺陷

OpenAI 在官方博客中直接指出了当前 agent 系统构建的三大困境：

> "The systems that exist today come with tradeoffs as teams move from prototypes to production. Model-agnostic frameworks are flexible but do not fully utilize frontier models capabilities; model-provider SDKs can be closer to the model but often lack enough visibility into the harness; and managed agent APIs can simplify deployment but constrain where agents run and how they access sensitive data."
> — [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

这段话揭示了一个根本矛盾：**model-agnostic（模型无关）的框架在灵活性和能力之间永远存在 tradeoff**。当框架试图兼容所有模型时，就无法针对某个特定模型（如 OpenAI 的 o-series 或 GPT-4o）做深度优化。

### 现有方案的三元悖论

| 方案 | 灵活性 | 模型能力利用 | 部署控制 |
|------|--------|-------------|----------|
| Model-agnostic 框架（LangChain 等）| 高 | 低 | 高 |
| Model-provider SDK（OpenAI/Anthropic 自家 SDK）| 低 | 高 | 低 |
| Managed Agent API（Claude API、ChatGPT 等）| 极低 | 高 | 极低 |

OpenAI 的解法是：**让 harness 本身成为模型-aware 的基础设施**，而不是让框架去猜测模型行为。

---

## 核心设计决策一：Model-Native Harness

### 什么是"Model-Native"

OpenAI 强调新的 harness 是"model-native"的，意思是 harness 的执行模式与 OpenAI 模型**自然运作方式**对齐：

> "The harness also helps developers unlock more of a frontier model's capability by aligning execution with the way those models perform best. That keeps agents closer to the model's natural operating pattern, improving reliability and performance on complex tasks—particularly when work is long-running or coordinated across a diverse set of tools and systems."
> — [OpenAI Agents SDK Update](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

关键洞察：**这不是说模型改变了，而是 harness 的执行节奏、上下文注入方式、工具调用模式要与模型的首选运作模式对齐。**

### 具体实现

新 harness 包含以下能力：

1. **可配置的记忆（Configurable Memory）**
   - 区别于固定窗口的 context 管理，harness 可以根据任务动态调整 memory 策略
   - 支持跨会话的状态持久化

2. **Sandbox-aware orchestration（沙箱感知的编排）**
   - harness 知道自己在沙箱中运行，因此可以在任务规划时考虑沙箱边界
   - 支持沙箱之间的协调（如子 agent 路由到不同沙箱）

3. **Codex-like filesystem tools（类 Codex 文件系统工具）**
   - 提供与 OpenAI Codex 相同的文件操作原语
   - 包括 `read`、`edit`、`apply_patch` 等工具的标准化实现

4. **标准化集成 primitives**
   OpenAI 明确提到了以下 primitives 在 harness 中的标准化集成：
   
   | Primitives | 说明 |
   |------------|------|
   | Tool use via MCP | 通过 Model Context Protocol 使用工具 |
   | Progressive disclosure via skills | 通过 Agent Skills 实现渐进式上下文披露 |
   | Custom instructions via AGENTS.md | 通过 AGENTS.md 注入自定义指令 |
   | Code execution via shell | 通过 shell 工具执行代码 |
   | File edits via apply_patch | 通过 apply_patch 工具编辑文件 |

> "These primitives include tool use via MCP, progressive disclosure via skills, custom instructions via AGENTS.md, code execution using the shell tool, file edits using the apply patch tool, and more. The harness will continue to incorporate new agentic patterns and primitives over time."
> — [OpenAI Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

**注意**：这份列表实际上是 OpenAI 对 Anthropic Agent Skills 的明确认可——skills 作为 progressive disclosure 的机制已经成为行业标准。

---

## 核心设计决策二：Native Sandbox Execution

### 为什么 sandbox 必须是 native 的

OpenAI 指出了三点：

#### 1. 安全隔离（Prompt Injection 防护）

> "Agent systems should be designed assuming prompt-injection and exfiltration attempts. Separating harness and compute helps keep credentials out of environments where model-generated code executes."
> — [OpenAI Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

这是关键设计：**凭证不进沙箱**。在传统架构中，agent 代码可能访问环境变量中的 API keys；而在分离架构中，harness 层负责凭证管理，compute 层（沙箱）只负责执行。

#### 2. 持久化执行（Durable Execution）

> "When the agent's state is externalized, losing a sandbox container does not mean losing the run. With built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint if the original environment fails or expires."
> — [OpenAI Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

**State externalization** 是 durable execution 的核心：agent 的运行状态（包括 memory、tool state、checkpoint）都存储在 harness 层，而非沙箱进程内。这使得沙箱容器可以随时销毁重建而不丢状态。

#### 3. 可扩展性（Scalability）

> "These new Agents SDK capabilities are generally available to all customers via the API and use standard API pricing, based on tokens and tool use."

OpenAI 将 sandbox 执行纳入标准 API 定价（按 token 和 tool use 计费），而不是单独的基础设施费用。这意味着企业可以将 agent 编排扩展到多个并行沙箱。

### 支持的 Sandbox 提供商

```
Blaxel · Cloudflare · Daytona · E2B · Modal · Runloop · Vercel
```

OpenAI 设计了 **Manifest abstraction** 来实现跨提供商的可移植性：

> "Developers can bring their own sandbox or use built-in support for Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, and Vercel. To make those environments portable across providers, the SDK also introduces a Manifest abstraction for describing the agent's workspace."
> — [OpenAI Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

**Manifest** 的核心能力：
- 挂载本地文件到沙箱
- 定义输出目录
- 集成云存储：AWS S3、Google Cloud Storage、Azure Blob Storage、Cloudflare R2

这意味着开发者可以从本地原型无缝迁移到生产部署，workspace 的语义保持一致。

---

## 与 Anthropic Harness Engineering 的架构对比

### 哲学层面的差异

| 维度 | OpenAI Agents SDK（2026） | Anthropic（Claude Code / Managed Agents） |
|------|--------------------------|-------------------------------------------|
| **Harness 定位** | Model-native，与 OpenAI 模型对齐 | Framework-agnostic，Claude 是"通才" |
| **Sandbox 策略** | Native sandbox，多提供商支持 | External sandbox（已有方案：E2B、Modal） |
| **Memory 模型** | Configurable，harness 级别控制 | Session-based with checkpoints |
| **安全模型** | 分离 harness 和 compute | 分离 Brain 和 Hand（Managed Agents）|
| **生态策略** | 集成 MCP、Skills 等行业标准 | 主导 Skills 标准制定 |

### Anthropic 的独特优势

Anthropic 的 harness 设计强调 **Agent Skills 作为可组合的专业化机制**：

> "Skills extend Claude's capabilities by packaging your expertise into composable resources for Claude, transforming general-purpose agents into specialized agents that fit your needs."
> — [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

OpenAI 在其 primitives 列表中明确提到 skills，表明这两个方向正在收敛。

### OpenAI 的独特优势

1. **多沙箱并行**：可以在多个沙箱中并行运行子 agent
2. **云存储集成**：原生支持 S3/GCS/Azure/R2 的 Manifest
3. **API 定价模型**：Sandbox 执行计入标准 API 成本

---

## 适用场景与局限

### 适用场景

✅ **企业级 long-horizon 任务**：医疗记录处理、复杂文档理解、法律合同分析等需要跨多步骤协作的场景  
✅ **高安全要求环境**：金融、医疗、法律等行业，prompt injection 风险高  
✅ **多沙箱并行场景**：需要同时在多个隔离环境中运行子 agent  

### 局限

❌ **Python first**：目前只有 Python SDK，TypeScript 支持在路线图上  
❌ **Provider lock-in**：虽然有 Manifest abstraction，但实际 sandbox 提供商的选择仍然受限  
❌ **非 OpenAI 模型支持有限**：Model-native 设计意味着对非 OpenAI 模型的优化不如 Anthropic SDK  
❌ **技能生态未成熟**：OpenAI 的 skills 集成是跟随 Anthropic 的模式，但 skill registry 生态尚未建立  

---

## 判断与结论

**1. OpenAI 的 model-native harness 代表了一种新的设计哲学**：不是让框架去迁就模型，而是让 harness 主动对齐模型的自然运作模式。这在技术上更优，但牺牲了对其他模型的支持。

**2. Sandbox 分离架构已经成为行业共识**：Anthropic 的 Brain/Hand 分离、OpenAI 的 Harness/Compute 分离，本质都是将状态管理和代码执行解耦。这不是巧合，而是 agent 工程化的必然演进方向。

**3. Multi-provider sandbox 是下一个战场**：OpenAI 的 Manifest abstraction 和多提供商支持（Blaxel/Cloudflare/Daytona/E2B/Modal/Runloop/Vercel）表明，sandbox 提供商之间的竞争将加剧。这对开发者是好事，但也会带来 provider 切换成本。

> 笔者认为：对于**非 OpenAI 模型优先的场景**（如 Anthropic Claude 或开源模型），应继续使用 OpenClaw 等 model-agnostic 框架；对于**OpenAI 模型优先且有强安全/隔离需求的场景**，新的 Agents SDK 是生产级选择。

---

## 引用来源

- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) — OpenAI 官方博客，2026-04-15
- [OpenAI updates its Agents SDK to help enterprises build safer, more capable agents](https://techcrunch.com/2026/04/15/openai-updates-its-agents-sdk-to-help-enterprises-build-safer-more-capable-agents/) — TechCrunch 报道
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic Engineering Blog