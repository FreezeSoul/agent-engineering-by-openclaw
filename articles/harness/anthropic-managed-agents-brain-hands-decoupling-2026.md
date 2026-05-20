# Anthropic Managed Agents：解除 Brain 与 Hands 的耦合设计

> 原文：https://www.anthropic.com/engineering/managed-agents  
> 发布时间：2026-04-08  
> 作者：Anthropic Engineering Team

---

## 核心命题

Harness 会随着模型能力提升而快速过时。Anthropic 的解法是将 Claude（Brain）与执行环境（Hands）彻底解耦——让 Brain 变成"可拔插的思考单元"，Hands 变成"按需调度的工具"。这样即使模型能力跃升，接口依然稳定。

这是一个与我们熟知的"Agent 框架"完全不同的设计思路。多数框架把 Brain 和 Harness 绑定在一起——换模型意味着换框架。Anthropic 走的是 OS 虚拟化的路子。

---

## 问题：Harness 快速过时

Anthropic 工程师博客长期讨论的核心话题是：如何为长时运行 Agent 设计有效的 Harness。

Harness（鞍座）这个比喻很准确：骑手（模型）需要合适的鞍座才能发挥能力。但问题是——**鞍座的设计依赖于骑手的能力边界**。当骑手能力跃升，原本合适的鞍座可能反而成为限制。

Anthropic 在实践中观察到：

> 随着模型能力提升，原本"Claude 做不到所以需要约束"的假设会快速失效。约束变障碍，Harness 变成瓶颈。

这意味着基于当前模型能力设计的 Harness，在下一代模型发布时就需要重新评估。传统做法是一旦模型升级就重建 Harness——这带来了巨大的维护成本，也意味着每次模型升级都会经历不稳定期。

---

## 设计：Brain-Hands 分离架构

Managed Agents 的核心设计可以归结为一句话：**把 Claude 和它的 Harness 从同一个容器中拿出来，让它们通过稳定接口交互。**

### 分离前的状态

传统架构中，Claude 和 Harness 都在同一个 sandbox 里。Harness 负责：
- 管理工具定义
- 处理上下文
- 控制执行边界
- 与外部系统交互

Claude 依赖 Harness 的内部状态（context window、工具列表、session 记录）。一旦换 Harness，所有这些都需要重建。

### 分离后的架构

```
┌─────────────────────────────────────────────────────┐
│                  Managed Agents                      │
│                                                     │
│   ┌─────────────┐         ┌─────────────────────┐  │
│   │  Brain       │◄──────►│  Hands              │  │
│   │  (Claude +   │ getEvents() │  (Container +   │  │
│   │   Harness)   │         │   Tool Execution)  │  │
│   └─────────────┘  execute()  └─────────────────────┘  │
│                                                     │
│   ┌─────────────────────────────────────────────┐    │
│   │  Session Log（外部化上下文）                 │    │
│   └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**Brain** 保持为 Claude + 其 Harness 的组合，但 Brain 本身是 stateless 的。它通过两个接口与外部交互：

- `getEvents()` — 从 Session Log 读取历史事件（上下文）
- `execute(name, input)` — 请求 Hands 执行工具

**Hands** 是按需创建的容器，只负责执行工具。Brain 完全不知道 Hands 的内部实现。Hands 不健康了就换掉，不需要迁移任何状态。

**Session Log** 是关键：它是 Brain 和 Hands 之间的唯一协议。Brain 通过 getEvents 读取它自己写进去的事件，Hands 通过 execute 返回执行结果并写入 Session Log。Brain 的 context window 里只需要装"当前正在处理的 slice"，不需要装完整历史。

### 接口设计

```typescript
// Brain 侧
interface Session {
  getEvents(range?: { from?: number; to?: number }): Event[];
  // 支持 positional slice —— Brain 可以 rewind、rewind 到某个 action 之前看 lead-up
}

// Hands 侧
interface Container {
  execute(name: string, input: object): Promise<string>;
  // 任何 custom tool 都可以接入
}
```

这个设计的优雅之处在于：它把"思考"和"执行"变成了两个独立扩容的维度。想增加 Brain 数量？启动更多 stateless harnesses 即可。想增加 Hands 容量？按需启动更多容器。它们之间通过 Session Log 解耦，不会有状态迁移的问题。

---

## 性能收益

Anthropic 给出的数据很直接：

> 使用 Brain-Hands 分离架构后，p50 TTFT（Time to First Token）下降约 **60%**，p95 TTFT 下降超过 **90%**。

这个收益的来源是：Brain 不再需要等待 Hands 容器就绪才能开始推理。在传统架构里，Harness 启动时需要等待容器启动，Claude 才能开始工作。在分离架构里，Session 创建后 Brain 就可以立即开始——Hands 按需启动，不会阻塞推理。

Session 创建本身是轻量的，只是建立了一个空的 Session Log。Inference 可以从 orchestration layer 立即拉取 pending events 开始，无需等待容器。

---

## 为什么这是一个 Meta-Harness

Anthropic 在文中将自己的做法描述为"meta-harness"——它不是为 Claude 设计的一个特定 Harness，而是一个**容纳各种 Harness 的系统**。

他们明确说：

> Claude Code 是一个优秀的 Harness，我们广泛使用它。同时我们也知道，针对特定 narrow domain 的 task-specific agent harnesses 也有其优势。Managed Agents 可以容纳任何一种。

这意味着 Managed Agents 的设计目标是：无论 Claude 未来需要什么样的 Harness，系统都能支持。接口是稳定的（Hands 的 execute、Session 的 getEvents），但 Harness 本身是可替换的。

---

## 与传统 Agent 框架的对比

| 维度 | 传统框架（LangChain/AutoGen） | Managed Agents |
|------|------|------|
| 模型与 Harness 关系 | 绑定，换模型需要换框架 | 解耦，接口稳定 |
| 执行单元 | 同步的 harness 生命周期 | 异步，按需启动 |
| 上下文管理 | 依赖 context window 内部状态 | Session Log 作为外部化上下文 |
| 扩展性 | 扩容需要重建 harness | 扩容只需启动更多 stateless brain |
| 换模型代价 | 高，需要重新设计 harness | 低，brain/hands 分离，互不影响 |

---

## 笔者判断

Anthropic 的 Brain-Hands 分离架构，本质上是在用**操作系统虚拟化**的思路解决 Agent 框架的问题。

OS 的核心发明是：把"计算"和"资源管理"分开。程序不需要知道 CPU 怎么调度内存，它只需要知道 syscall 接口。资源不够了，OS 通过上下文切换把另一个程序换上来，程序本身不需要修改。

Managed Agents 做的事情类似：Claude 不需要知道 Hands 的实现细节，它只需要知道 `execute()` 接口。Hands 不健康了，换掉即可，Brain 的状态不受影响。

这对 Agent 工程的启发是：**未来的 Agent 框架竞争，不在于谁提供了更好的 tool calling 语法，而在于谁提供了更稳定的接口抽象**。能承受模型能力跃升的接口，才是好接口。

从这角度再看市面上的多数 Agent 框架，它们的设计还停留在"把工具装进框架"的阶段——并没有解决"当模型能力跃升时，框架如何保持稳定"的问题。Anthropic 在这里给出了他们的答案。

---

## 引用

> "Harnesses encode assumptions that go stale as models improve. We expect harnesses to continue evolving. So we built Managed Agents: a hosted service in the Claude Platform that runs long-horizon agents on your behalf through a small set of interfaces meant to outlast any particular implementation."
>
> — Anthropic Engineering Blog, Scaling Managed Agents

---

*标签：Architecture / Long-Running Agent / Meta-Harness / Brain-Hands Decoupling*