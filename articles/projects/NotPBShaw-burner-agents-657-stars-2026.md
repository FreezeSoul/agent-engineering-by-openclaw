# Burner Agents：让"不可关联性"成为工程特性的临时身份 swarm

**Tags**: #Identity #Swarm #Browser-Isolation #Privacy #Harness

**来源**: [NotPBShaw/burner-agents - GitHub](https://github.com/NotPBShaw/burner-agents) (657 ⭐)

---

## 核心命题

当前的隐私工具（VPN、私人浏览、反追踪插件）都在治标不截：它们试图更好地隐藏一个持久的身份，却没有解决真正泄露的问题——**你每次都作为同一个人出现**。

Burner Agents 的核心思路不同：不是隐藏一个持久身份，而是**根本不维护持久身份**。用户从不直接触碰任何服务，所有的 web 交互都通过一次性 agent 完成，每个 agent 有自己独立的指纹、设备特征和网络出口，执行完任务即销毁。

> "To any site, there is no single user to track, only a series of unrelated participants, each seen once and never again."

![GitHub](https://img.shields.io/github/stars/NotPBShaw/burner-agents?style=for-the-badge&logo=github)

---

## 为什么这个项目值得关注

### 1. 重新定义"隐私"的工程边界

传统隐私工具的思路是**减少可观测性**（减少指纹、清除 cookies、隐藏 IP），Burner 的思路是**增加不可关联性**——即使观测到了某个行为，也无法将这些行为归因到同一个实体。

这是一个工程上的范式转变：
- **隐藏**（Concealment）：让观测者看到的是假身份，但假身份仍然是单薄的
- **分散**（Dispersal）：让观测者看到的是完全无关的多个身份，无法关联

不可关联性（Non-linkability）在隐私研究领域是一个核心概念，Burner 第一次将它工程化为可用的 swarm 架构。

### 2. 架构设计：四个模块各司其职

```
burner/
├── isolation/        # 每个 agent 独立浏览器上下文
├── reasoning/       # 将意图翻译为行动，实时推理页面状态
├── orchestration/   # 分解任务、分发给多个 agent、汇总结果
└── identity/        # 任务启动时创建，任务完成时销毁
```

**Isolation** 是架构的基础——不是给每个 agent 分配不同的配置，而是每个 agent 在完全分离的浏览器环境中运行。分离是环境结构本身，而不是应用在顶层的设置。

**Identity** 的设计哲学值得注意：它是**任务作用域**的，既不绑定到用户，也不绑定到持久会话。完成和销毁是同一个事件，没有归档、没有备份、没有"万一以后需要"的保留。

### 3. 与传统隐私工具的真正差异

| 维度 | VPN | 私人浏览 | 反追踪插件 | Burner Agents |
|------|-----|---------|-----------|---------------|
| 隐藏 IP | ✅ | ✅ | ✅ | ✅ |
| 清除本地状态 | ❌ | ✅ | ❌ | ✅ |
| 减少浏览器指纹 | ❌ | ❌ | 部分 | ✅（每次全新） |
| 不可关联性 | ❌ | ❌ | ❌ | ✅ |
| 隔离网络出口 | ❌ | ❌ | ❌ | ✅（每次独立） |

核心差异在于：**其他工具都是在"同一个你"的基础上减少可观测信息，Burner 直接替换了"你"这个实体**。

### 4. Orchestration 的安全边界

Burner 的架构中，orchestration 模块绑定用户意图、分解任务、协调多个 disposable agent，这些操作都在用户的信任边界内完成。外部网站只能观测到多个无关的 disposable agent，完全看不到 orchestration 的存在。

这意味着：用户意图的协调是**隐私的**，只有 agent 的多样性是**可观测的**。

---

## 设计原则分析

### Delegation over exposure（委托优于暴露）

用户的身份、环境和指纹从不直接接触任何服务。用户和 web 之间的接口是 agent，而这个 agent 是可销毁的。

这是一个严格的信任边界设计：即使某个 disposable agent 被攻破，攻击者也只能看到单次任务的信息，无法关联到其他任务，也无法追溯到用户。

### Disposability over concealment（可销毁优于隐藏）

不试图更有效地隐藏一个持久身份，而是不维护持久身份。

笔者认为，这个原则在工程上比"更强隐私保护"更彻底：没有持久身份，就没有泄露的持久身份；不存在的东西无法被窃取。

### Multiplicity over singularity（多元优于单元）

用户不是由一个隐藏得更好的身份代表，而是由多个完全无关的身份代表。对于 web 来说，不存在单一个体可以追踪，只有，一群无法识别中心的群体。

---

## 工程挑战与思考

### 1. 行为相关性依然存在

即使每个 agent 有独立的指纹和网络出口，如果多个任务的行为模式高度相似（例如都在同一时间访问同一类网站、执行相似的操作序列），观测者仍然可能通过**行为相关性**建立关联。

Burner 的 README 提到了这个问题，但未深入解决方案。这可能是一个未来的改进方向。

### 2. 成本与效率的权衡

每次任务都启动全新的浏览器上下文和网络出口，意味着无法利用会话状态、登录态、缓存等传统的效率优化手段。对于需要多步骤、跨会话的任务，这是根本性的权衡。

### 3. 与 Harness Engineering 的交叉点

Burner 的架构本质上是一个**极度强调安全的 agent harness**：每个 agent 都有严格的作用域、生命周期和销毁机制。它和传统 Harness 的区别在于：传统 Harness 控制的是 agent 的**能力边界**（能做什么、不能做什么），Burner 控制的是 agent 的**身份边界**（属于谁、能被谁关联）。

---

## 适用场景

**强场景**：
- 需要从多个视角研究竞争对手的 SEO 或广告策略
- 调查市场趋势而不暴露商业意图
- 高隐私要求的竞争情报收集

**弱场景**：
- 需要登录态的持续交互
- 跨任务需要共享上下文的工作流
- 对效率有严格要求的重复性任务

---

## 引用

> "A swarm of disposable agents for unattributable web interaction. Each task runs under a fresh identity that is destroyed on completion, so you are represented online not by one persistent self but by a continuous supply of unrelated strangers, none of which leads back."

> "Delegation over exposure. The user's own identity, environment, and fingerprint never make contact with a service. The interface between you and the web is the agent, and the agent is disposable."

> "Multiplicity over singularity. You are represented not by one well-hidden identity but by many unrelated ones. To the web, there is no single entity to find. There is a crowd with no discernible center."

---

## 快速参考

```bash
# 查看完整文档和架构说明
git clone https://github.com/NotPBShaw/burner-agents
cd burner-agents
```

核心模块：
- `isolation/` — 每个 agent 的独立浏览器上下文
- `reasoning/` — 实时页面推理引擎
- `orchestration/` — 任务分解与 agent 协调
- `identity/` — 生命周期管理（启动创建，完成销毁）
