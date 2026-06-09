# Anthropic Code w/ Claude London 2026：企业级 Agent 部署的边界革命 — self-hosted sandboxes + MCP tunnels

> **核心命题**：Claude Managed Agents 的两项新发布——self-hosted sandboxes 和 MCP tunnels——将"企业控制边界"从概念变成了工程现实。这不是功能升级，而是 Anthropic 对"brain-hands 分离"架构模式在企业场景的完整落地。

---

## 一、背景：距离"我有一个想法"和"它跑起来"正在再次收缩

Boris Cherny（Head of Claude Code）在伦敦大会 keynote 开场时回忆了他第一次感受到编程"魔力"的时刻：在中学用 TI-83 写程序解数学作业，用 HTML 让 Pokemon 卡牌拍卖页面更吸引人。"学然后做，做然后跑，跑起来的那一刻是兴奋的。"

他随后指出了一个我们共同经历的趋势：**编程在某个时刻变得复杂了**——编译器、类型检查器、构建系统，每一层都在拉大"我有一个想法"和"它跑起来"之间的距离。但随着 Agent 的出现，这个距离正在再次收缩：你描述一个问题，程序就出现了。就像当年计算器的感觉，只是这个计算器可以写一个分布式系统。

这就是 2026 年我们正在见证的转变。而 London 大会上发布的两项能力，将这个转变正式带入了企业级部署的语境。

---

## 二、核心发布：self-hosted sandboxes + MCP tunnels

在伦敦大会上，Anthropic 宣布 Claude Managed Agents 新增两项能力：

### 2.1 Self-hosted Sandboxes

> "Claude Managed Agents can now operate in a sandbox you control."

这意味着**执行环境的所有权归企业**。企业可以在自己的基础设施上运行 Agent，而不需要将代码执行托付给 Anthropic 的托管环境。

这对企业意味着什么？笔者的判断是：

**这是 Anthropic"brain-hands 分离"架构模式的企业级完整落地。** 在此前 Anthropic 的工程博客（managed-agents）中，已经详细描述了这一架构：将 Claude（brain）和 sandbox（hands）解耦，使得两者可以独立扩缩、独立失效、独立替换。Self-hosted sandboxes 将这个解耦的控制权完全交给了企业。

官方原文：
> "Now both the environment where an agent executes tools and the services it reaches run within the established boundaries of your enterprise."

### 2.2 MCP Tunnels

> "connect to your private Model Context Protocol (MCP) servers"

MCP tunnels 解决了企业级 Agent 部署的另一个关键问题：**工具访问的边界控制**。

企业通常有自己的内部工具和服务——数据库、代码库、内部 API——这些不应该暴露在公网上。传统的 Agent 调用这些服务需要将凭证传递给第三方托管环境，存在明显的安全风险。MCP tunnels 允许 Claude Managed Agents 连接到企业私有的 MCP 服务器，所有工具调用都在企业网络边界内完成。

结合 self-hosted sandboxes，这意味着：

| 维度 | 传统托管 Agent | 具备 self-hosted sandboxes + MCP tunnels |
|------|--------------|------------------------------------------|
| **执行环境** | Anthropic 托管 | 企业自有基础设施 |
| **工具访问** | 通过公网调用外部 API | 通过 MCP tunnels 连接私有 MCP 服务器 |
| **凭证暴露** | Agent 需要处理 token | token 永远不在 sandbox 内 |
| **合规边界** | 依赖平台合规性 | 企业完全控制数据流 |

---

## 三、工程原理：brain-hands 分离在企业场景的完整落地

Anthropic 在工程博客中描述的"brain-hands 分离"模式，在这个发布中得到了完整的工程实现。

### 3.1 架构解耦

在原始的 Managed Agents 架构中，解耦的核心设计是：

```
Brain（Claude + harness）←→ Session（持久化日志）←→ Hands（sandbox + tools）
```

Brain 和 Hands 通过 session log 进行通信，但彼此不知道对方的位置和实现细节。任何一方失效都不会导致另一方丢失状态。

Self-hosted sandboxes 将 Hands 的实现完全替换为企业自有基础设施：

```
Brain（Anthropic 云端）←→ Session ←→ Hands（企业自有 container/VM）
```

企业获得了对 Hands 的完全控制权，同时保留了 Brain 来自 Anthropic 的强大推理能力。

### 3.2 凭证安全

这是企业安全团队最关心的维度。

Anthropic 的 managed-agents 工程博客明确描述了安全边界的实现原则：

> "The structural fix was to make sure the tokens are never reachable from the sandbox where Claude's generated code runs."

具体实现：
- **Git 凭证**：每个仓库的访问 token 在 sandbox 初始化时写入本地 git remote，Agent 执行 git push/pull 时不需要处理 token 本身
- **自定义工具的 OAuth**：通过专用 proxy 访问，proxy 从 secure vault 获取凭证，harness 永远不知道凭证内容
- **MCP 服务器**：通过 MCP tunnels 连接，token 在企业网络内交换，不经过公网

### 3.3 MCP tunnels 的工程意义

MCP（Model Context Protocol）是 Anthropic 主导的标准，2025 年已捐赠给 Linux 基金会。官方原文描述：

> "Now both the environment where an agent executes tools and the services it reaches run within the established boundaries of your enterprise."

MCP tunnels 使这一标准在企业场景有了真正的落地：
1. **隧道加密**：企业 MCP 服务器不需要暴露在公网
2. **私有连接**：Claude 通过加密隧道连接企业内部 MCP 服务器
3. **标准协议**：使用 MCP 协议，不需要为每个工具单独开发 API 集成

---

## 四、早期实践者：Amplitude、Clay、Rogo

官方提到，已经有团队在使用 self-hosted sandboxes 构建生产系统：

- **Amplitude**：产品分析平台
- **Clay**：数据 Enrichment 平台
- **Rogo**：AI 驱动的企业搜索

这三个案例的共同特点是：**数据敏感度高、合规要求严格、需要将 AI 能力深度集成到企业工作流**。正是这些特点驱动他们选择 self-hosted 方案而非纯托管方案。

笔者认为，2026 年企业级 Agent 部署会形成明显的分层：
- **通用场景**：使用 Anthropic 托管的 Managed Agents，快速上手，Anthropic 负责基础设施安全
- **企业敏感场景**：使用 self-hosted sandboxes + MCP tunnels，企业控制执行环境和工具访问，满足合规要求

---

## 五、笔者判断：这不是功能升级，是架构模式的完整落地

许多解读将这次发布视为"又一个功能"，但笔者的判断不同：

**这是 Anthropic"brain-hands 分离"架构模式在企业场景的完整工程落地。**

从 2025 年的 managed-agents 工程博客开始，Anthropic 就已经在描述一个架构愿景：Claude 是与基础设施无关的 brain，企业可以自由选择 hands 的实现——本地 Docker、云端 VM、私有服务器。Self-hosted sandboxes 让这个愿景在工程上真正可操作。

而 MCP tunnels 则补全了另一个关键维度：**工具访问的企业控制**。企业不再需要为了使用 AI Agent 而将内部工具暴露在公网上，也不需要把凭证交给第三方托管环境。MCP 作为标准协议，使得这种集成既安全又可移植。

真正的问题是：**多少企业已经准备好将自己的 Agent 基础设施从"托管"转向"自控"？**

这不是技术问题，而是工程能力和安全策略的问题。Amplitude、Clay、Rogo 的实践说明，已经有团队在走这条路，但大多数企业还在评估阶段。

---

## 六、引用

> "Now both the environment where an agent executes tools and the services it reaches run within the established boundaries of your enterprise."
> — Anthropic, Code w/ Claude London 2026

> "The structural fix was to make sure the tokens are never reachable from the sandbox where Claude's generated code runs."
> — Lance Martin, Gabe Cemaj, Michael Cohen, Anthropic Engineering

> "programming got complicated. Compilers, typecheckers, build systems, and each layer pushed the distance between 'I have an idea' and 'it runs' a little further out. With agents, that distance is collapsing again: you describe a problem, and the program shows up."
> — Boris Cherny, Head of Claude Code

---

**Tags**: `enterprise-agent` `self-hosted-sandbox` `MCP-tunnels` `brain-hands-decoupling` `Claude-Managed-Agents` `Anthropic` `security-boundary`

**相关工程博客**：
- [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)
- [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)