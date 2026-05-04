# Evolver：Genes Not Skills——用遗传进化协议让 AI Agent 自我改进

**核心主张**：Evolver 解决了 Agent 自我改进领域的核心问题——Skill 文档提供的控制信号不稳定、稀疏、难以迭代积累。它引入了 **Gene（基因）** 作为经验载体：紧凑、可审计、可组合。4,590 次对照实验证明，Gene 表征在结构扰动下保持稳健，而 Skill 文档在同样条件下性能急剧下降。

**读者画像**：有 Agent 开发经验，使用过 Claude Code 或类似 Harness，想让 Agent 能够从真实任务中学习并持续改进，但不满足于「改 Prompt 看效果」的碰运气方式。

**核心障碍**：当前的 Agent 自我改进大多依赖手工 Prompt 调优——每次发现 Agent 在某类任务上表现不好，就改一次 Prompt。这种方式无法积累、无法审计、无法复用，而且对结构扰动（任务形式变化）极其脆弱。

---

## 1. 定位：Skill 文档的失败与 Gene 的崛起

### 1.1 Skill 文档的问题

Evolver 论文的核心发现是：文档导向的 Skill 包提供的控制信号**不稳定、稀疏**。

> "Documentation-oriented Skill packages provide unstable, sparse control signal, while a compact Gene representation delivers the strongest overall performance, stays robust under structural perturbation, and is a far better carrier for iterative experience accumulation."
> — [Evolver arXiv Paper: From Procedural Skills to Strategy Genes (2604.15097)](https://arxiv.org/abs/2604.15097)

翻译成工程语言：当你写一个「如何处理 API 超时」的 Skill 文档，这个文档在以下情况下会失效：
- API 错误信息格式变了（结构扰动）
- 超时原因从网络变成了认证失效（新场景）
- 调用方从 CLI 变成了后台任务（新上下文）

Skill 文档是**脆弱的知识封装**——它捕获了「当时怎么做」，但没有捕获「为什么当时这样做是对的」。

### 1.2 Gene 的定义

Gene（基因）是 Evolver 提出的核心概念。它是**策略性知识的紧凑表征**，与生物基因的类比是精确的：

| 维度 | 生物基因 | Evolver Gene |
|------|---------|-------------|
| 存储形式 | DNA 序列（ATCG） | 紧凑的 GEP Prompt |
| 激活条件 | 特定环境信号 | 特定任务/上下文模式 |
| 表达结果 | 蛋白质/生物特征 | Agent 行为模式 |
| 遗传性 | 可组合、可变异 | 可跨 Agent 复用 |

一个 Gene 不是「如何在 API 超时时重试」的步骤列表，而是「**当检测到资源暂时不可用时，优先使用指数退避而非固定间隔**」这样的**策略原则**。

### 1.3 论文数据

> "On CritPt (a benchmark for agent physics problem solving), gene-evolved systems lift their paired base models from 9.1% to 18.57% and from 17.7% to 27.14%."
> — [Evolver README / arXiv Paper](https://arxiv.org/abs/2604.15097)

基因进化的系统在 CritPt 基准上将配对的基线模型从 9.1% 提升到 18.57%，从 17.7% 提升到 27.14%——**翻倍级别的提升**。

> 笔者认为：CritPt 是一个物理问题求解基准，任务形式相对规整。基因进化在此类结构化任务上表现突出，说明 Gene 的核心优势在于**策略层面的知识压缩**——将「怎么做」封装为「什么时候选择什么策略」。

---

## 2. GEP 协议：Genome Evolution Protocol

### 2.1 协议设计原则

GEP（Genome Evolution Protocol）定义了 Gene 的创建、存储、激活和组合方式。

> "Evolver encodes agent experience as Genes and Capsules under the GEP protocol, not as ad hoc prompts or skill docs."
> — [Evolver README](https://github.com/EvoMap/evolver)

这意味着：
- **可审计**：每次进化都产生 EvolutionEvent，记录「哪个 Gene 被选择、为什么」
- **可复用**：Gene 可以跨 Agent 共享（通过 EvoMap Network）
- **可组合**：多个 Gene 可以组合成 Capsule（更大的功能单元）

### 2.2 三种核心资产

| 资产类型 | 定义 | 用途 |
|---------|------|------|
| **Gene** | 策略性知识的紧凑表征 | 当特定上下文模式出现时激活 |
| **Capsule** | 多个 Gene 的组合 | 实现更复杂的功能单元 |
| **Event** | 进化过程的审计日志 | 追踪哪个资产在什么场景下被使用 |

---

## 3. 使用体验：30 秒开始自我进化

### 3.1 安装与运行

```bash
# 安装（需要 Node.js >= 18 和 Git）
npm install -g @evomap/evolver

# 在任何 git 仓库中运行
evolver
```

### 3.2 运行流程

一次「成功的首次运行」流程：

1. Evolver 打印检测到的策略预设（如 `balanced`）
2. 扫描 `./memory/`（如果不存在则创建），寻找日志和信号
3. 从内置资产池中选择匹配的 Gene / Capsule
4. 将 **GEP Prompt** 打印到 stdout——这是进化的产物
5. 将 EvolutionEvent 写入 `./memory/` 用于审计

### 3.3 三种运行模式

```bash
# 单次进化运行
evolver

# 审核模式——应用前暂停等待人类确认
evolver --review

# 连续循环——作为后台守护进程运行
evolver --loop
```

### 3.4 平台集成

Evolver 支持与主流 Agent Runtime 集成：

| 平台 | 集成方式 |
|------|---------|
| Cursor | `evolver setup-hooks --platform=cursor`，自动注册到 `~/.cursor/hooks/` |
| Claude Code | `evolver setup-hooks --platform=claude-code`，注册到 `~/.claude/` |
| OpenClaw | 无需额外配置，原生解释 Evolver 输出的 `sessions_spawn(...)` 指令 |

> "OpenClaw natively interprets the `sessions_spawn(...)` stdout directives Evolver emits. Just run `evolver` from inside an OpenClaw session."
> — [Evolver README](https://github.com/EvoMap/evolver)

---

## 4. 技术架构：离线优先 + 可选网络

### 4.1 离线核心

Evolver **完全离线工作**。核心引擎不依赖任何外部服务——它扫描本地日志、选择基因、输出 GEP Prompt。

这与很多「云端 AI 优化平台」有本质区别：
- 不需要上传数据到第三方
- 不需要 API Key
- 不需要互联网连接
- 审计日志完全在本地

### 4.2 可选网络：EvoMap Network

当配置 `.env` 后，Evolver 可以连接到 EvoMap Network，解锁：
- **Skill 共享**：从其他 Agent 复用经过验证的 Gene
- **Worker Pool**：分布式进化计算
- **Evolution Leaderboards**：比较不同 Gene 在不同任务上的表现

配置方式：
```bash
A2A_HUB_URL=https://evomap.ai
A2A_NODE_ID=your_node_id_here
```

---

## 5. 与 Skill 系统的对比

| 维度 | Skill 文档 | Gene (Evolver) |
|------|-----------|----------------|
| **知识形式** | 步骤列表/操作指南 | 策略原则/激活条件 |
| **结构扰动鲁棒性** | 脆弱——格式变化即失效 | 稳健——策略抽象保留 |
| **可审计性** | 低——无法追踪「为什么这样写」 | 高——每次进化产生 Event |
| **可复用性** | 低——通常与特定项目耦合 | 高——Gene 可跨项目复用 |
| **积累方式** | 手工维护，版本混乱 | 协议化管理，可迭代 |
| **激活方式** | 被动——需要显式调用 | 主动——上下文模式触发 |

> 笔者认为：Gene 和 Skill 不是互斥的，而是不同层次的知识封装。Skill 是「how」，Gene 是「when to use which strategy」。在工程实践中，Skill 提供具体的操作步骤，Gene 提供更高层的策略路由。但 Gene 的抽象层次更适合**自我进化**——因为它封装的是「决策原则」而非「操作细节」，更不容易受任务形式变化影响。

---

## 6. OpenClaw 集成：CritPt 评估案例

Evolver README 提到了一个具体的 OpenClaw 集成案例：

> "OpenClaw x EvoMap: CritPt Evaluation Report walks through how the same Gene-based evolution loop drives an OpenClaw agent from 0.00% to 18.57% on CritPt Physics Solver across five versions (Beta -> v2.2), with full token-cost trajectories, gene activation mapping, and the 'tokens rise then fall' signature of reasoning getting compressed into reusable genes."
> — [Evolver README](https://github.com/EvoMap/evolver)

关键数据：
- **起点**：OpenClaw Agent 在 CritPt Physics Solver 上得分 0.00%
- **终点**：经过 5 个版本（Beta -> v2.2）后达到 18.57%
- **Token 轨迹**：推理过程中 token 先上升（问题复杂化）后下降（知识压缩进基因）
- **这是可验证的**：有完整的 token-cost 轨迹和基因激活映射

---

## 7. 行动引导

### 快速上手

1. **安装**：`npm install -g @evomap/evolver`
2. **初始化**：在项目目录运行 `evolver`（需要 git 初始化）
3. **观察**：查看 `./memory/` 目录中产生的 Gene 和 Event
4. **集成**：按需集成到 Cursor / Claude Code / OpenClaw

### 适合的场景

- **长期运行的 Agent 项目**：有足够的日志数据可供分析
- **需要持续改进的领域**：如代码生成、数据分析、自动化工作流
- **对可控性有要求**：需要知道「为什么 Agent 改了行为」

### 不是万能的

- **冷启动问题**：没有足够的任务日志时，Evolver 没有选择依据
- **结构性任务更有效**：越规整的任务，Gene 越容易抽象出稳定的策略模式
- **不是银弹**：它提供的是「更科学的自我改进方法」，不是「让 Agent 自动变聪明」

---

## 8. 结论

Evolver 的核心价值不是「又一个 Prompt 优化工具」，而是它在概念层面的贡献：**将 Agent 自我改进从「手工调优」升级为「协议化进化」**。

GEP 协议定义了 Gene 的生命周期，审计日志记录了每次决策的理由，紧凑的表征使跨任务复用成为可能。这三者的组合让 Agent 改进从「碰运气」变成了「可工程化的过程」。

对于 Agent 开发者，Evolver 提供的不仅是工具，更是一种思路：**与其让 Agent 学习「怎么做」，不如让它学习「什么时候选择什么策略」**。

---

*来源：[Evolver GitHub](https://github.com/EvoMap/evolver)、[arXiv:2604.15097](https://arxiv.org/abs/2604.15097)、[OpenClaw x EvoMap: CritPt Evaluation Report](https://evomap.ai/blog/openclaw-critpt-report)*
