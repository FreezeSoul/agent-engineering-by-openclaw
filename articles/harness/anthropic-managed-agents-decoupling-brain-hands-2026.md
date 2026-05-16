# Anthropic Managed Agents：解耦大脑与双手的 Agent 系统设计

> **来源**：[Anthropic Engineering Blog - Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)，2026年4月8日

---

## 核心问题：一个被反复验证的工程教训

Anthropic 在构建 Managed Agents 时遇到了一个经典问题：**当模型能力提升后，之前针对旧模型设计的 harness 会成为限制**。

他们举了一个具体例子：在 Claude Sonnet 4.5 时代，Agent 会在接近 context limit 时提前结束任务（所谓"context anxiety"）。当时的解决方案是在 harness 中加入 context resets。但当换成 Claude Opus 4.5 后，这个行为消失了——之前精心设计的 resets 变成了多余代码。

> "We expect harnesses to continue evolving."

这句话背后是一个深刻的工程哲学：**harness 是模型能力的函数，而不是独立的常量**。当模型进化时，harness 必须跟着变，否则就会从助力变成阻力。

---

## 解耦架构：OS 思想在 Agent 系统的应用

Managed Agents 的核心架构师从操作系统的历史中找到了答案。 decades ago, operating systems solved this problem by virtualizing hardware into abstractions—process, file—general enough for programs that didn't exist yet.

Anthropic 将这个思想搬到了 Agent 系统：

| 组件 | 传统设计 | Managed Agents 解耦 |
|------|---------|---------------------|
| **Session** | 存在 harness 内存中 | 独立接口，append-only log |
| **Harness** | 与 sandbox 耦合在同一容器 | 独立服务，可重启 |
| **Sandbox** | 只能有一个 | 可以有多个，按需创建 |

三个接口：`execute(name, input) → string`、`wake(sessionId)`、`emitEvent(id, event)`——不多不少，刚好够描述 Agent 的行为而不约束实现。

---

## "Pet vs Cattle"：从宠物到牛

原来的设计把 session、harness、sandbox 全塞进一个容器，好处是文件编辑是 direct syscalls，没有服务边界。但代价是：容器成了"宠物"——挂了就得 nurse back to health。

解耦后：

- **Sandbox 挂了** → harness 捕获 tool-call error → Claude 决定重试 → 新容器用 `provision({resources})` 初始化。不用 nurse，直接替换。
- **Harness 挂了** → session log 在 harness 之外 → 新 harness 用 `wake(sessionId)` + `getSession(id)` 恢复，继续从上次位置运行。

笔者认为：**这个设计最聪明的地方不是"可以容错"，而是把"容错"变成了系统的默认行为，而不是特殊处理**。当所有组件都是 cattle，你不需要为每种失败情况写专门的恢复代码。

---

## 安全边界：token 永远不到达 sandbox

原架构中，未信任代码（Claude 生成的）和凭证共存于同一容器。Prompt injection 只要能让 Claude 读取自己的环境，就能拿到 token。

Managed Agents 的解决：

1. **Git**：每个仓库的 access token 在 sandbox 初始化时写入本地 git remote，push/pull 不需要 agent 处理 token
2. **MCP 工具**：OAuth token 存在外部 vault，MCP proxy 根据 session 关联的 token 去 vault 取 credential，harness 完全不知晓任何凭证

> "The structural fix was to make sure the tokens are never reachable from the sandbox where Claude's generated code runs."

这是防御深度（defense in depth）的体现：**不是在 prompt 层面限制 Claude 能做什么，而是在架构层面让"错误行为"物理上不可能**。

---

## Session 不是 context window

这是一个容易被混淆的点。Long-horizon 任务超过 context window 时，标准做法（compaction、context trimming）都是不可逆的——你必须在压缩前决定保留什么。

Managed Agents 的 session 作为 context object 在 context window 之外存在，通过 `getEvents()` 接口让 brain 按需拉取：positional slices、rewind 几个 event 向前看、或在某个 action 前 reread context。

> "We separated the concerns of recoverable context storage in the session and arbitrary context management in the harness because we can't predict what specific context engineering will be required in future models."

这句话的关键在于：**他们不预测未来模型需要什么样的 context engineering，所以把 storage 和 management 分开，让 harness 去encode具体策略，而session只保证 durability 和可查询性**。这是接口设计哲学的胜利。

---

## 性能收益：60% p50 TTFT 下降，90%+ p95 下降

原架构中，每个 brain 都需要一个容器来运行推理。每个 session 必须 clone repo、boot process、fetch pending events——即使这个 session 根本不需要 sandbox。

解耦后，sandbox 是按需创建的（通过 `execute(name, input) → string` 调用）。不需要 sandbox 的 session 可以立即开始推理，不需要等容器 provision。

结果：
- **p50 TTFT 下降 ~60%**
- **p95 TTFT 下降 >90%**

这对用户体验是决定性的：TTFT 是用户最能感知到的延迟。推理的开始不再被 sandbox setup blocking。

---

## Many brains, many hands：扩展性

解耦还解锁了一个新能力：**一个 brain 可以连接多个 hands**。

在单容器时代，一个 Claude 实例只能操作一个 shell环境。如果那个 shell 挂了，所有 hands 都丢。解耦后，每个 hand 是 `execute(name, input) → string` 的工具，harness 不知道 hand 是容器、手机还是模拟器。没有 hand 耦合到任何 brain，所以 brains 可以互相传递 hands。

---

## 笔者判断：这是 Agent 系统设计的"操作系统级"突破

Managed Agents 的意义不只是"让 Claude 更强"，而是证明了：

**Agent 的各组件（brain/hands/session）有不同的变化速率和生命周期，不应该绑在一起**。

笔者认为这个设计有三点值得学习：

1. **接口优于实现**：三个接口（execute/wake/emitEvent）定义了 Agent 的行为边界，具体实现可以随时替换而不影响其他组件
2. **从 model 角度看 harness**：当 model 能力跃升时，harness 中的很多"保护性代码"会变成冗余，甚至是性能负担
3. **安全架构的物理隔离**：credential 不只是"不让 Claude 看到"，而是从架构上让 sandbox 永远无法 reach 到 token 存储

> — [Anthropic Engineering Blog: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)（2026-04-08）