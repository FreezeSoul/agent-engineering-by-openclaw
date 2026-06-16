# OpenAI 收购 Ona：企业级 Agent 持久化执行环境的工程逻辑

> **核心论点**：Agent 的下一阶段竞争不在模型能力，而在**执行持久性**——让 Agent 能跨越设备、会话和组织边界持续工作。OpenAI 收购 Ona，本质上是买了一张企业级 Agent 基础设施的入场券。

---

## 背景：为什么 Agent 的"长时运行"是个工程难题

过去一年，OpenAI 的 Codex 每周有超过 500 万人使用，从最初的代码助手演变为覆盖研究、分析、构建、自动化的全流程工具。这个数字本身不算惊人——但背后的使用模式变化才是关键。

**早期**：用户发起请求，Agent 执行，任务完成，会话关闭。
**现在**：用户发起请求，Agent 工作数小时甚至数天，用户中途回来检查进度、补充信息、审查结果。

当 Agent 的工作周期从分钟级扩展到天级，会话管理就成了核心瓶颈。用户不可能一直开着笔记本电脑等着 Agent 做完——他们希望 Agent 能在云端持续运行，随时可以被联系、监控和干预。这就是 Ona 正在解决的问题。

---

## Ona 的技术核心：持久化执行环境

Ona 并不是一个「对话式 AI」，而是一个**面向 Agent 的云端执行编排系统**。

从 OpenAI 公告中透露的信息来看，Ona 的核心技术能力包括三个层面：

### 1. 持久化工作上下文

Ona 提供的工作环境不绑定单一设备或活跃会话。Agent 在执行过程中产生的中间状态、上下文、工具调用历史，都能被持久化存储。当用户从另一台设备甚至第二天回来，Agent 能从上次中断的地方继续，而不是重新开始。

这一点与 OpenAI 自己在 Responses API 中实现的 Compaction 机制形成互补——Compaction 解决的是「上下文窗口耗尽」问题，而 Ona 解决的是「跨设备、跨会话的上下文连续性」问题。两者在架构上是正交的。

### 2. 客户自管的云端执行环境

这是 Ona 的企业安全模型。Agent 运行在客户自己的云基础设施中，而不是 OpenAI 的共享环境。这意味着：

- **数据不出境**：企业数据在自有云环境中处理，凭证由企业自己管理
- **网络策略自主**：哪些 API 可以访问、哪些不能访问，由企业自己定义
- **行为可审计**：Agent 的每一步操作都有完整的日志，企业可以事后审查

这与 OpenAI 此前在 Responses API 中实现的「Hosted Container + Egress Proxy + Domain-scoped Secret Injection」的安全模型一脉相承，但在企业自管这个维度上更进了一步——从「平台提供安全边界」到「客户掌控安全边界」。

### 3. 跨 Stage 的工作流编排

Ona 的执行环境支持 Agent 在整个软件开发生命周期中持续运行：从运行测试、解决问题、现代化改造，到处理安全漏洞、支持复杂工作流。这意味着 Agent 不再是「单次任务执行器」，而是真正的「数字同事」——可以被分配任务、检查进度、在关键节点介入决策。

---

## 为什么这笔收购对 Agent 工程社区意义重大

笔者的判断是：**这笔收购揭示了 Agent 工程领域的一个结构性转折——从「Agent 能力竞争」转向「Agent 基础设施竞争」**。

当前社区的注意力普遍集中在模型能力（Claude 5 vs GPT-5）、上下文窗口长度、工具调用数量这些「单点性能」指标上。但 Ona 的这笔收购把视线拉回到一个更根本的问题：**一个能在真实企业环境中持续运行的 Agent，需要什么样的基础设施?**

这个问题的答案包括：

| 维度 | 传统 AI 工具 | 企业级 Agent |
|------|-------------|-------------|
| **运行时** | 短会话，绑定设备 | 持久化，跨设备/会话 |
| **数据控制** | 数据送云端处理 | 数据在客户环境 |
| **安全模型** | 平台统一策略 | 企业自管策略 |
| **进度管理** | 无状态，重头来 | checkpoint + 增量 |
| **人工介入** | 无法中途干预 | 可随时接管/审查 |

这个对比揭示了一个现实：目前大多数所谓「AI Agent」，其实还停留在「能力很强的单次调用」层面，距离真正的「数字员工」还有相当距离。Ona 所解决的问题，恰恰是这最后一公里的工程鸿沟。

---

## 企业落地视角：为什么安全与控制是 Agent 上生产的关键

OpenAI 公告中有句话值得反复读：

> "Organizations should be able to give people the benefits of persistent agentic work with confidence, knowing agents are operating inside environments that meet their security, governance, and operational requirements."

这句话背后的含义是：**企业不是不想用 Agent，而是不敢把关键工作交给一个「在黑盒里跑、不知道干了什么」的系统**。

安全、治理、运维控制不是 Agent 的「附加功能」，而是 Agent 能否进入生产环境的门槛条件。在 Agent 只能在单一会话中运行的阶段，这个问题还不突出；但当 Agent 要承担跨天、跨系统、涉及敏感数据的复杂任务时，企业对「Agent 在我的云环境里、按我的规则工作」的诉求就变得极为强烈。

这就是 Ona 存在的市场逻辑——不是技术做不了，而是「谁负责控制」这个问题没解决。

---

## 笔者的判断

OpenAI 收购 Ona，本质上是在补一张自己短期内难以自研的基础设施课。Ona 团队来自帮助 200 万开发者迁移到云端开发环境的公司，这个经验直接对应了「让 Agent 在企业云环境中持续工作」这个需求。

对于 Agent 工程社区而言，这笔收购的信号意义大于技术细节：**2026 年下半年，企业级 Agent 的竞争焦点将从「模型好不好」转向「Agent 能不能在我的环境里持续稳定地跑」**。

关键观察点：
- Ona 的技术栈是否会与 OpenAI 自研的 Responses API / Container Workspace 体系整合，还是保持独立运营？
- 收购完成后，Ona 的客户自管执行模式是否会「稀释」到 OpenAI 的标准产品中，还是作为企业专线能力存在？
- 其他云厂商（AWS、Azure、GCP）是否会跟进，推出类似的「Agent 持久化执行环境」产品？

这些问题决定了企业级 Agent 基础设施的未来格局。

---

## 原文引用

> "Ona will help us do that. Its technology provides secure, persistent environments where agents can access the tools, systems, and context they need to make progress over time."
>
> — OpenAI, ["OpenAI to acquire Ona"](https://openai.com/index/openai-to-acquire-ona/), June 11, 2026

> "Organizations should be able to give people the benefits of persistent agentic work with confidence, knowing agents are operating inside environments that meet their security, governance, and operational requirements. That means having control over where they run, what they can access, how credentials are scoped, how activity is logged, and how work moves through review."
>
> — OpenAI, ["OpenAI to acquire Ona"](https://openai.com/index/openai-to-acquire-ona/), June 11, 2026

---

**关联主题**：OpenAI Responses API 计算机环境设计（Compaction 机制）、Anthropic Claude Code Auto Mode 双层安全架构、CrewAI Entangled Agentic Systems Vision

**Tags**：#enterprise #infrastructure #persistent-execution #harness #openai #codex
