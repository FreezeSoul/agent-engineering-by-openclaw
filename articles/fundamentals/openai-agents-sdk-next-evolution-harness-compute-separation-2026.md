# OpenAI Agents SDK 新一代：Harness 与 Compute 分离的工程革命

**核心命题**：OpenAI Agents SDK 的这次更新，第一次在模型提供商 SDK 中实现了 **harness（控制层）与 compute（计算层）的彻底分离**——这不只是功能升级，而是 AI Agent 工程范式的根本性转变。

---

## 一、问题：现有 Agent 工程的三难困境

OpenAI 在这篇博客中直接点出了当前 Agent 工程的核心矛盾：

> "Model-agnostic frameworks are flexible but do not fully utilize frontier model capabilities; model-provider SDKs can be closer to the model but often lack enough visibility into the harness; and managed agent APIs can simplify deployment but constrain where agents run and how they access sensitive data."

这段话翻译过来就是：**灵活性、模型契合度、安全可控不可兼得**。

现有的三种路径各有硬伤：
- **模型无关框架**（LangChain 等）：灵活但无法充分利用前沿模型能力
- **模型提供商 SDK**：与模型更近，但对 harness 缺乏可见性
- **托管 Agent API**：部署简单但约束了执行环境和数据访问

笔者认为，这不是工程能力问题，而是架构设计问题——这些问题只有在 **把 harness 和 compute 混在一起** 时才会同时出现。

---

## 二、解法：Harness 与 Compute 的分离架构

OpenAI 给出的答案是：把 Agent 系统的控制层（harness）和执行层（compute）拆开。

### 2.1 更具能力的 Harness

更新后的 Agents SDK harness 具备了以下能力：

- **可配置内存**：让 Agent 在长周期任务中保持上下文连续性
- **沙箱感知的编排**：知道自己在哪个执行环境中工作
- **类 Codex 文件系统工具**：读、写、编辑文件的标准化能力
- **MCP 工具集成**：通过 Model Context Protocol 使用外部工具
- **AGENTS.md 自定义指令**：项目级指导文件，随代码一起迁移

关键在于：这不再是「给模型加一堆工具」，而是 **为前沿模型的工作模式专门设计执行环境**。OpenAI 明确指出：

> "The harness also helps developers unlock more of a frontier model's capability by aligning execution with the way those models perform best."

也就是说：不是让模型适应工程师设计的工作流，而是 **让工作流对齐模型最擅长的操作模式**。这是一个根本性的思维转换。

### 2.2 原生沙箱执行

新版 Agents SDK 原生支持沙箱执行，开发者可以用内置支持对接 Blaxel、Cloudflare、Daytona、E2B、Modal、Runloop、Vercel 等提供商，也可以自带沙箱。

关键抽象是 **Manifest**：描述 Agent 工作区的标准化方式，可以挂载本地文件、定义输出目录、接入存储服务（AWS S3、GCS、Azure Blob、Cloudflare R2）。

Manifest 让工作区在不同阶段（本地原型 → 生产部署）和不同提供商之间 **自由迁移，而不需要修改 Agent 逻辑**。这对团队从实验到规模化的工程路径至关重要。

---

## 三、安全性 + 持久性：分离架构的核心价值

### 3.1 安全：凭证不进入执行环境

分离的最大安全价值：凭证不会进入模型生成代码执行的沙箱。

> "Separating harness and compute helps keep credentials out of environments where model-generated code executes."

这是工程层面的安全原则，而不是依赖模型自身的对齐。对比 Anthropic 的 Containment 三层防御（环境层/模型层/外部内容层），这是从基础设施层面做隔离——不再让模型负责控制它不该控制的东西。

### 3.2 持久性：快照 + 再水合

新版 SDK 内置 **snapshotting（快照）和 rehydration（再水合）** 能力：

> "With built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint if the original environment fails or expires."

这与 Anthropic 的 long-running agent harness 中的「接力机制」高度呼应——都是通过外部化状态来实现跨会话的连续性。区别在于：
- **Anthropic 方案**：git commit + progress file + clean state handover（接力棒模式）
- **OpenAI 方案**：snapshotting + rehydration（快照恢复模式）

两者都能解决「上下文窗口耗尽后任务中断」的问题，工程路径不同但目标一致。这说明 **Agent 长周期执行的工程问题已经开始收敛到几种可证明有效的模式上**。

---

## 四、可扩展性：按需调度与并行化

分离架构解锁了全新的扩展能力：

> "Agent runs can use one sandbox or many, invoke sandboxes only when needed, route subagents to isolated environments, and parallelize work across containers for faster execution."

具体来说：
- **按需调用**：只有在需要时才启动沙箱，降低空闲成本
- **子 Agent 隔离**：不同专业角色的 Agent 路由到独立环境
- **并行化**：跨容器并行执行子任务

这让 Agents SDK 从「单 Agent 执行器」升级为 **多 Agent 编排层**，且编排逻辑是内置的而非需要自己实现。OpenAI 在四月就发布过 Symphony（把 Issue Tracker 变成 Agent 控制平面），这次是把编排能力更深度地整合进 SDK。

---

## 五、为什么这是工程范式的转变

笔者认为，这次更新的重要性不在于「多了哪些功能」，而在于它 **重新定义了模型提供商 SDK 的角色**。

之前的模型提供商 SDK，本质上是「模型的 API 包装器」——把模型能力封装成易用的接口，但没有在工程层面深度参与 Agent 的控制流。

新版 Agents SDK 做的事：
1. 把 **harness 设计**（而不是模型能力）作为一等公民
2. 在 SDK 层内置 **沙箱编排 + 状态持久化 + 安全隔离**
3. 让模型在最适合自己的执行模式中工作

这三个决策合在一起，代表 **模型提供商开始承担 Agent 工程的基础设施责任**——这不只是功能迭代，而是定位变化。

---

## 六、对工程实践的含义

| 维度 | 之前 | 之后 |
|------|------|------|
| **长任务可靠性** | 依赖模型上下文窗口，容易中断 | 内置 snapshot/rehydrate，中断可恢复 |
| **安全模型** | 模型负责约束自己的行为 | 基础设施层隔离，凭证不进沙箱 |
| **扩展路径** | 自行实现多 Agent 编排 | SDK 内置按需沙箱 + 并行化 |
| **工作区移植性** | 提供商绑定 | Manifest 抽象，本地到生产无缝迁移 |

对于已经在使用 OpenAI Agents SDK 的团队，这次升级值得优先评估——尤其是涉及长周期任务和敏感数据的生产场景。

---

## 结语

这篇博客的核心信息非常清晰：**Harness 不是模型的附加物，而是 Agent 系统的骨干**。把控制层和执行层分离，让两边都能做自己最擅长的事——模型负责决策，基础设施负责安全和持久性。

笔者认为，这个方向代表着 AI Agent 工程正在从「用好模型」向「构建可靠的 Agent 系统」演进。当模型提供商开始在 SDK 层面承担 harness 工程责任，这个领域的工程成熟度正在快速提升。

---

**引用来源**：
1. "The next evolution of the Agents SDK" — OpenAI Blog, April 15, 2026
2. Agents SDK 官方文档 — developers.openai.com

**关联主题**：阶段12（Harness Engineering）/ OpenAI Codex 系列文章 / Anthropic Long-Running Agent Harness