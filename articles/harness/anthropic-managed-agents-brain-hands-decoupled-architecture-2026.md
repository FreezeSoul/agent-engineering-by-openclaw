# Anthropic Managed Agents 工程解析：Brain-Hands 解耦与外部化上下文架构

**核心主张**：Anthropic 最新发布的 Managed Agents 技术解析揭示了一个关键工程突破——将 Agent 的「大脑」（Harness + Claude）与「手」（Sandbox + Tools）解耦，并通过外部化的 Session Event Log 实现跨上下文窗口的持久记忆。这不是简单的架构重构，而是从「宠物」模式向「 cattle」模式的关键范式转移。

**读者画像**：已理解 Agent 基本概念，关注 Agent 平台架构、上下文工程、长时任务可靠性设计的工程师。

**核心障碍**：当前 Agent 系统在扩展性、容错性和上下文管理上面临根本性制约——传统单体设计让 Session、Harness 和 Sandbox 共享生命周期，导致「宠物困境」（容器挂了 = 会话丢失）和上下文焦虑（Context Anxiety）。

---

## 1. 背景：为什么需要解耦

Anthropic 在 2026 年 4 月发布的《Scaling Managed Agents》详细记录了他们从单体容器设计迁移到 Brain-Hands 解耦架构的过程。这次迁移的动因来自两个实际问题的叠加：

### 1.1 宠物困境（The Pet Problem）

在初期设计中，Anthropic 将 Session、Agent Harness 和 Sandbox 全部放入单个容器。这意味着：
- 容器失败 → Session 丢失
- 容器无响应 → 工程师需要「 nursing it back to health」（手动救活）
- 每个 Session 都是一个需要精心维护的「宠物」

> "We adopted a pet. In the pets-vs-cattle analogy, a pet is a named, hand-tended individual you can't afford to lose, while cattle are interchangeable."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

### 1.2 网络耦合问题

第二个问题是 Harness 假设所有资源都在本地容器内。当客户需要将 Claude 连接到自己的 VPC 时，要么需要网络 peering，要么需要客户自己运行 Harness——这暴露了架构中的强假设。

### 1.3 性能瓶颈

在单体设计中，容器必须预置才能开始推理（TTFT - Time To First Token）：
- 每个 Session 无论是否需要 Sandbox，都必须等待容器启动
- 包括 Clone Repo、Boot Process、Fetch Pending Events 等固定成本
- 在多 Brain 场景下，这些成本线性叠加

---

## 2. 解耦架构：Brain-Hands 分离

Anthropic 的解决方案是将 Agent 拆解为三个独立接口：

### 2.1 核心接口定义

| 接口 | 角色 | 生命周期 |
|------|------|---------|
| **Session**（事件日志） | 持久化的事件记录，append-only | 独立于 Brain 和 Hands 存在 |
| **Brain**（Harness + Claude） | 推理决策中枢，运行 Agent Loop | cattle - 可随时重启 |
| **Sandbox**（执行环境） | 代码执行、文件编辑等实际操作 | 按需启动，用完可销毁 |

关键设计决策：**让 Harness 通过 Tool Call 调用 Sandbox**：
```
execute(name, input) → string
```

这意味着 Sandbox 不再是 Harness 的「内部组件」，而是一个可以被替换的工具。当 Sandbox 失败时，Harness 捕获 Tool Call Error 并让 Claude 决定是否重试——新的 Sandbox 可以通过 `provision({resources})` 重新初始化。

### 2.2 性能提升

解耦后，容器按需启动：
- Session 不需要 Sandbox 时 → 直接开始推理
- Inference 在事件日志就绪后立即启动
- 结果：**p50 TTFT 下降约 60%，p95 TTFT 下降超过 90%**

> "Decoupling the brain from the hands means that containers are provisioned by the brain via a tool call only if they are needed. So a session that didn't need a container right away didn't wait for one. Inference could start as soon as the orchestration layer pulled pending events from the session log."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

---

## 3. 外部化上下文：Session 作为 Context Object

### 3.1 上下文窗口的根本问题

长时任务通常会超出 Claude 的上下文窗口。传统解决方案（Compaction、Context Trimming）都需要不可逆的决策——决定保留什么、丢弃什么。一旦消息被压缩并从上下文窗口移除，它们就是不可恢复的。

### 3.2 Session Event Log：上下文作为外部对象

Anthropic 的核心创新是将 **Session 定位为「存在于上下文窗口之外的上下文对象」**：

```typescript
// Session 提供的核心接口
getEvents() → 位置切片的事件流
emitEvent(id, event) → 保持事件的持久记录
wake(sessionId) → 从上次中断处恢复
```

这与之前直接在 REPL/Sandbox 中存储上下文的对象式方法（如 arxiv:2512.24601 探索的方案）本质相同，但将持久化层从 Sandbox 移到了独立的 Session 服务。

### 3.3 分离关注点：Session vs Harness

Anthropic 明确将上下文管理的职责分离：

- **Session 职责**：提供可查询的持久化事件存储（getEvents 支持位置切片、正向回滚、重读）
- **Harness 职责**：负责具体的上下文工程——在将事件传给 Claude 前，可以对事件进行任意转换，包括：
  - 上下文组织（提升 Prompt Cache 命中率）
  - 上下文工程（根据任务需求裁剪、补充）

> "We separated the concerns of recoverable context storage in the session and arbitrary context management in the harness because we can't predict what specific context engineering will be required in future models."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

这个分离的价值在于：**接口的稳定性**。Session 接口保持稳定（只要事件可查询即可），而 Harness 的上下文工程逻辑可以随着模型能力演进而快速迭代。

### 3.4 上下文焦虑的解决

Anthropic 在早期工作中发现 Claude Sonnet 4.5 存在「上下文焦虑」——当感知到上下文接近上限时，会提前结束任务。他们通过在 Harness 中添加 Context Resets（重置上下文窗口 + 结构性交接 artifact）来解决这个问题。

但在 Claude Opus 4.5 上运行时，这个行为消失了——Resets 变成了无用代码。

Session 的外部化设计提供了一种更优雅的解决方案：即使上下文窗口被重置，Session 中的历史事件仍然可查询。模型不需要「记住」所有事情，只需要知道「在哪里找到」。

---

## 4. 安全边界：Token 永远不在 Sandbox 可达范围

### 4.1 威胁模型

在单体设计中，Claude 生成的不可信代码与凭证共存于同一容器。一旦攻击者通过 Prompt Injection 让 Claude 读取环境变量，凭证就泄露了——攻击者可以立即启动新的无限制会话。

### 4.2 结构性修复

Anthropic 采用两个模式确保凭证永远不会出现在 Sandbox 中：

**模式一：Auth 与资源绑定**
- Git Access Token：在 Sandbox 初始化时完成 Clone，Wire 进本地 Git Remote
- Push/Pull 从 Sandbox 内部执行，但 Token 从不经过 Agent

**模式二：MCP + Vault 代理**
- OAuth Token 存储在独立 Vault 中
- Claude 调用 MCP Tools 通过专用 Proxy
- Proxy 根据 Session 关联的 Token 从 Vault 获取凭证，完成外部服务调用
- Harness 永远不感知凭证

> "The security boundary: the tokens are never reachable from the sandbox where Claude's generated code runs."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

---

## 5. Many Brains, Many Hands：多 Agent 扩展路径

解耦架构还解锁了一个新能力：**一个 Brain 连接多个 Hands**。

在单体设计中，每个 Brain（Container）只对应一个执行环境。当 Claude 需要在多个执行环境间分配任务时，容器失败会导致整个会话中断。

解耦后，Claude 可以：
1. 决定在哪个 Sandbox 执行任务
2. 通过 Tool Call 调用不同 Sandbox
3. 某个 Sandbox 失败不影响其他 Sandbox 和 Brain 的状态

这是从「单 Agent 单容器」到「多 Agent 多 Sandbox」的关键认知转变——早期的单体设计是因为模型能力不足以管理多环境协调，但随着模型智能的提升，单体设计变成了瓶颈而非优势。

> "We also wanted the ability to connect each brain to many hands. In practice, this means Claude must reason about many execution environments and decide where to send work—a harder cognitive task than operating in a single shell."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

---

## 6. 与现有 Agent 架构的关系

### 6.1 vs Cursor Cloud Agents

| 维度 | Cursor Cloud Agents | Anthropic Managed Agents |
|------|-------------------|------------------------|
| **核心问题** | 本地资源约束 + 上下文重建成本 | 单体架构的宠物困境 + 上下文焦虑 |
| **解耦对象** | Cloud VM 隔离每个 Agent 会话 | Brain/Hands/Session 三层分离 |
| **上下文管理** | Artifacts 作为交接媒介 | External Event Log + Harness 上下文工程 |
| **扩展路径** | 多 Agent 并行 + 人类定义问题边界 | Many Brains + Many Hands |

两者共同指向的结论：**下一代 Agent 平台的核心挑战是重新设计人-Agent 交互边界，而非单纯的 Agent 能力提升**。

### 6.2 vs Context Engineering 早期工作

Anthropic 在 2025 年 9 月发布的《Effective Context Engineering for AI Agents》奠定了上下文工程的基础——包括 Compaction、Memory Tools、Context Trimming 等技术。Managed Agents 的创新在于将这些技术从「Agent 内部决策」提升到「Harness 层可编程策略」：

- **早期方式**：Agent 内部决定何时压缩、何时 Trim
- **新方式**：Harness 作为独立策略层，在将 Session 事件传给 Claude 前进行任意转换

这使得上下文工程逻辑可以被版本化、测试和独立演进。

---

## 7. 工程价值

### 7.1 可观测性提升

在单体设计中，WebSocket Event Stream 是唯一的调试窗口。Harness Bug、Packet Drop、Container Offline 都呈现相同的症状。解耦后，每个组件有独立的生命周期：
- Session 挂了 → 事件丢失，可通过 Wake 恢复
- Brain 挂了 → Stateless，可立即重启并读取 Session
- Hands 挂了 → Tool Call Error，Claude 决定重试

### 7.2 可替换性

接口的稳定性使得实现可以自由替换：
- 今天的 Sandbox 实现可以被明天的更高效实现替代
- Harness 的上下文工程策略可以独立于 Session 存储演进
- 这解决了「programs as yet unthought of」的设计挑战

> "We virtualized the components of an agent: a session, a harness, and a sandbox. This allows the implementation of each to be swapped without disturbing the others. We're opinionated about the shape of these interfaces, not about what runs behind them."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

### 7.3 性能收益

- **TTFT 改善**：p50 -60%，p95 -90%
- **资源利用**：不需要 Sandbox 的 Session 零等待
- **弹性扩展**：Stateless Brain 支持任意数量的并发实例

---

## 结论

Anthropic Managed Agents 的 Brain-Hands 解耦架构代表了一种成熟的 Agent 平台工程思路：

1. **从宠物到 cattle**：Session、Brain、Sandbox 独立生命周期，消除单点故障
2. **外部化上下文**：Session Event Log 作为持久化上下文对象，Harness 负责上下文工程策略
3. **安全内嵌**：Token 永远不在 Sandbox 可达范围，从架构层面消除 Prompt Injection 风险
4. **可扩展路径**：Many Brains + Many Hands 支持更复杂的多 Agent 协调场景

这个架构的核心价值不在于单个组件的创新，而在于**接口设计**：通过定义稳定的接口边界，使得各层实现可以独立演进，同时保持跨模型、跨场景的兼容性。

---

**来源**：[Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)