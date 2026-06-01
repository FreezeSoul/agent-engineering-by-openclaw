# SmithDB：面向 Agent 可观测性的日志结构数据库设计

> **核心命题**：现代 agent trace 的规模（数百个深度嵌套 span、跨分钟级的时间跨越、多模态内容）和查询复杂度（时序、嵌套过滤、Top-K）已经超出了传统可观测性存储的能力。SmithDB 通过对象存储 + LSM tree + Apache DataFusion 的架构，为 agent 原生查询模式提供了 12 倍的性能提升。
>
> 来源：[We built SmithDB](https://www.langchain.com/blog/introducing-smithdb)（LangChain Blog，Published May 13, 2026）

---

## 问题：Agent Trace 不是普通日志

当 LangSmith 在 2023 年刚推出时，AI 应用相对简单：RAG pipeline、prompt chain、早期 agent。

但 2026 年的 agent 已经完全不同：

1. **Trace 规模爆炸**：单个 agent trace 可以有数百个深度嵌套的 span，每个 span 可能包含多模态内容（图像、音频）
2. **时间跨度巨大**：一个 agent span 的 start event 和 end event 可能相隔几分钟甚至几小时
3. **查询模式复杂**：需要跨 tenant 和 tracing project 的最新运行、嵌套的事件过滤、Top-K 风格的时序查询

传统数据库不是为这种工作负载设计的。它们假设请求/响应在毫秒级完成，span start 和 finish 在同一个操作窗口内。而 agent spans 可以保持 open 状态很长时间。

---

## 架构：Object Storage + LSM Tree + DataFusion

SmithDB 的架构选择：

**Object Storage 作为持久层**
- 没有本地磁盘管理
- Query 和 ingestion 服务是无状态的
- 通过添加 compute 横向扩展，数据在对象存储中持久化
- 这使得 self-hosted 和 multi-cloud 部署比传统数据库集群简单得多

**LSM Tree（Log-Structured Merge Tree）作为存储引擎**
- 内存中缓冲写入
- 刷新到持久存储为不可变的有序批次（sorted batches）
- 定期 compaction 合并 segments
- 读时多个 segments 作为单一有序流被读取和合并

**Apache DataFusion 作为查询引擎**
- 与 Vortex 文件工具包配合
- Heavy customization 用于 LangSmith 的特定 workload

---

## 关键工程挑战及解决方案

### 1. Top-K 时间窗口查询优化

Many LangSmith queries ask for the newest runs for a particular tenant and tracing project.

Naive object-store plan：发现所有候选文件、打开很多文件、排序-合并-去重，然后才应用 limit。

**SmithDB 的优化**：反向遍历时间，构建 newest candidate segments 的有界时间窗口。

这将 "sort everything, then limit" 变成了 "read the newest bounded slice, stream, merge and dedupe rows, and stop as soon as correctness allows"。

结果：大幅减少满足 Top-K 风格查询所需扫描的数据量。

### 2. 热数据读取优化

Object storage 是持久化的真相来源，但最新数据往往还在写入它的 ingestion node 的本地 SSD 和内存缓存中。

**SmithDB 的优化**：每个文件 segment 记录产生它的 server identifier。如果该 writer 仍然在线，查询规划器可以直接从 ingestion node 的本地 SSD 和内存缓存扫描文件，而不是立即从 object storage 读回。

这避免了为满足 leading-edge 查询而从 object storage 读取数十个小文件。

### 3. 多事件 run 的流式处理

In a traditional request/response application, a span may start and finish within milliseconds. But agent spans can stay open much longer.

In SmithDB, a run is a sequence of events, not a single immutable row.

这听起来简单，但影响整个查询引擎：
- 过滤器被扇出到特定事件
- 事件在查询时以高效的方式合并
- 多个事件 per run 也影响 compaction 策略

### 4. Time-Tiered Compaction

Ingestion optimizes for write latency，产生许多小的 immutable segments。如果永远查询这些，会造成太大的文件 open 开销和去重工作。

Compaction 将写优化 segments 转换为查询优化 segments。SmithDB 使用 time-tiered strategy：

- 最近的数据更可能接收 end events，过早 compact 成大文件会造成不必要的写放大
- 较旧的数据更稳定，更可能被重复扫描，所以值得 compact 成更大的文件

---

## 性能结果

LangSmith 迁移到 SmithDB 后，Clay 和 Vanta 等团队看到的核心指标：

| 场景 | 性能提升 |
|------|---------|
| Key observability workloads | 最高 12 倍更快 |

12 倍的性能提升不是来自单个优化，而是来自整个查询引擎对 agent 可观测性工作负载的重新设计。

---

## 为什么这对 Agent 工程很重要

可观测性工具的速度对于 agent 开发循环至关重要——无论是人类开发者还是 agent 本身。

Slow observability tools become a bottleneck in the agent development loop.

当一个 agent 执行出问题时，工程师需要快速看到是哪个 span 出了问题、输入是什么、决策过程如何。如果可观测性工具本身太慢，整个迭代循环都会减速。

SmithDB 的目标是消除这个瓶颈。

---

## 闭环关联

| 组件 | 关联 |
|------|------|
| **Interpreter Skills（LangChain）** | Agent 使用 interpreter 做代码级协调时，SmithDB 捕捉这些跨调用的状态变化，提供细粒度的 trace |
| **Agent Eval Harness** | SmithDB 的 trace 数据为 eval harness 提供 ground truth——什么输入产生了什么输出 |
| **CrewAI「迭代优先」哲学** | SmithDB 让迭代循环更快——当调试工具本身就慢时，快速迭代是不可能的 |

---

## 结论

SmithDB 代表了 agent 可观测性数据层的范式转变：从通用的时序数据库转向专门为 agent trace 设计的存储引擎。

关键洞察：
- Agent trace 是不同于普通应用日志的工作负载
- 对象存储 + 无状态计算层 = 更好的扩展性
- 时间窗口有界遍历 > 全局排序后 limit
- 热数据在 ingestion node 本地读取 > 每次从 object storage 读

这是 agent 工程走向成熟的标志——当工具层开始为 agent 原生的工作负载设计时，整个开发体验都会改善。