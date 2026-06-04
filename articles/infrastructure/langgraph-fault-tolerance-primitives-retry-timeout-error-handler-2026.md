# LangGraph Fault Tolerance 三件套：RetryPolicy、TimeoutPolicy、error_handler 与 SAGA 补偿

> **核心命题**：生产级 Agent 不会因为 prototype 能跑就能上线——LLM rate limit、5xx、connection reset、子进程挂死会在多步流程中放大成不可恢复错误。LangGraph 把「错误处理」从「每个节点写 25 行 try/except 模板代码」下沉到 workflow engine 内部的三个图元（RetryPolicy / TimeoutPolicy / error_handler），并通过 superstep 调度让补偿逻辑（SAGA）成为 first-class 拓扑。

> 来源：[Fault Tolerance in LangGraph: Retries, Timeouts and Error Handlers](https://www.langchain.com/blog/fault-tolerance-in-langgraph)（LangChain Blog，Published June 4, 2026 by Quanzheng Long & Sydney Runkle）

---

## 副观点 1：错误处理模板代码常常比业务逻辑还长——这是 workflow engine 应承担的责任

> **关键洞察**：happy path 是 agent 的 30%，剩下 70% 是「这个 step 失败时怎么办」。LangGraph 把这 70% 抽到图原语，开发者写的是「节点做什么」，框架负责「节点失败时怎么调度」。

文章开篇就抛出一个反直觉数字：

> "Writing the happy path is usually the easy part. The error handling boilerplate that makes it survive in production (retries, timeouts, fallbacks) is often longer than the business logic itself."

在 prototype 阶段，agent 调用一次 LLM、跑一个 tool、返回结果——没人在意失败。**生产环境的失败是结构性的**：

1. **网络瞬时故障** —— LLM provider 5xx、vector store connection reset、downstream HTTP 503
2. **资源耗尽** —— rate limit、queue full、connection pool exhausted
3. **超时挂死** —— HTTP call 不返回、subprocess frozen、child process 卡在 IO
4. **重试耗尽后的副作用回滚** —— 预订机票流程里，座位预留成功但支付失败，库存已扣不能就这么放弃

LangGraph 把这四类失败的处理全部抽到三个**图元**，挂在节点定义上：

```python
StateGraph(State).add_node(
    "call_llm", call_llm,
    retry_policy=RetryPolicy(max_attempts=4, backoff_factor=2.0),
    timeout=TimeoutPolicy(run_timeout=30, idle_timeout=5),
    error_handler=handle_model_failure,
)
```

**与传统写法的差异**：

| 传统写法 | LangGraph 图元 |
|---------|----------------|
| 每个 node 内嵌 25 行 try/except + sleep(jitter) | `retry_policy=RetryPolicy(...)` 一行配置 |
| 手动维护 `attempt_count`、`next_retry_at` | 框架接管 attempt 状态 |
| 超时要自己写 timer + cancel | `TimeoutPolicy(run_timeout=30)` 内置 wall-clock cap |
| 重试耗尽后只能 raise | `error_handler=fn` 把 context 注入新 task |

**这种抽象是「workflow engine 应当承担的责任」而不是「应用层反复实现的样板」**——核心观点是：当一个失败模式在所有生产 agent 中 100% 出现，让每个开发者重新实现一次是工程浪费。

---

## 副观点 2：RetryPolicy 的「保守默认」反映工程成熟度——不重试 `ValueError` 比「所有错误都重试」更难做到

> **关键洞察**：default `retry_on` 故意只重试 ConnectionError / 5xx / 临时性网络错误，不重试 ValueError / TypeError / RuntimeError——后者几乎都是编程 bug，重试只会把错误状态反复提交。

RetryPolicy 的实现细节揭示了一个重要工程取舍：

```python
RetryPolicy(
    initial_interval=0.5,    # 首次重试间隔
    backoff_factor=2.0,     # 指数退避系数
    max_interval=128.0,     # 上限
    max_attempts=3,         # 最大尝试次数
    jitter=True,            # 抖动避免 thundering herd
    retry_on=(ConnectionError, TimeoutError),  # 可调用谓词
)
```

**default retry_on 故意保守**：

- ✅ 重试 `ConnectionError`、`httpx.requests` 的 5xx
- ❌ **不重试** `ValueError`、`TypeError`、`RuntimeError`——这些是编程 bug

**为什么这个默认很关键**：

许多「重试框架」默认「任何异常都重试」——这在生产中是灾难。设想一个 agent 把 `{"user_id": null}` 传给某个 API，API 返回 `ValueError: user_id cannot be None`。如果框架自动重试 3 次，三次都失败，每次都打日志告警——监控被噪声淹没，反而错过真正的 5xx 故障。

LangGraph 的「保守默认 + 可调用谓词」是 **Calm Technology 原则**：

```python
# 可调用谓词：自己判断哪些错误值得重试
RetryPolicy(
    retry_on=lambda e: isinstance(e, RateLimitError) and e.retry_after < 60
)
```

**对比同类框架**：
- **Tenacity**（Python 库）：重试策略灵活，但需要开发者写更多配置
- **Spring Retry**（Java）：保守默认类似，但没有「per-node」配置粒度
- **LangGraph**：把重试从「跨函数装饰器」变成「图节点属性」——粒度更细，状态由 workflow engine 接管

---

## 副观点 3：TimeoutPolicy 的双时钟设计——run_timeout 控总量，idle_timeout 控「卡住」

> **关键洞察**：长跑但 active-streaming 的 LLM 调用不应被超时打断（它在做有效工作），但完全 hang 住的 HTTP call 必须被 cancel。区分这两种情况需要两个独立的时钟。

传统超时只有「wall-clock」一个维度——30 秒到了就 kill。但 LLM 调用的真实情况是：

```python
TimeoutPolicy(
    run_timeout=30.0,   # 硬性 wall-clock cap
    idle_timeout=5.0,   # 进度停滞上限
    refresh_on="auto",  # 或 "heartbeat"
)
```

**两个时钟的分工**：

| 时钟 | 用途 | 适用场景 |
|------|------|----------|
| `run_timeout=30.0` | 单次 attempt 的硬性总时长 | 「这个节点最多等 30 秒，不管进不进度」 |
| `idle_timeout=5.0` | 无进度信号的最大间隔 | 「5 秒内没有任何进展就视为挂死」 |
| `refresh_on="auto"` | 进度信号自动检测 | LangChain 回调、channel writes、streamed chunks |
| `refresh_on="heartbeat"` | 手动调用 `runtime.heartbeat()` | 自定义长任务，需要显式汇报存活 |

**auto 模式的进度信号**包括：
- channel writes
- streamed chunks（LangChain LLM models 自动 emit）
- child task events
- LangChain callback events

**关键设计哲学**：`idle_timeout` 把「超时」从「绝对时间」变成「相对进度」——一个长跑但活跃流式输出的 LLM 调用（思考 token 持续到达）不会触发 `idle_timeout`，但一个完全 hang 住的 HTTP call 会。这避免了「长任务被误杀」的常见 bug。

**自定义心跳**：如果节点执行自定义工作（不通过 LangChain 标准回调），可以切换 `refresh_on="heartbeat"` 并在代码里显式调用：

```python
def long_running_node(state, runtime):
    for i in range(100):
        do_chunk_of_work()
        runtime.heartbeat()  # 主动告诉框架「我还活着」
```

**当 timeout 触发**：node attempt 被 cancel 并 raise `NodeTimeoutError`——错误信息清晰可追溯，不是简单的 "Timeout" 异常。

---

## 副观点 4：error_handler 的「原子 superstep 调度」让补偿逻辑成为 first-class 拓扑

> **关键洞察**：传统 retry-exhausted 处理是「节点失败 → catch 异常 → 应用层决定下一步」。LangGraph 把这个决策编入图结构——失败时框架自动在同一 superstep 调度 error_handler，与其他节点并行，状态原子提交。

error_handler 的设计是整套 fault tolerance 最精妙的部分。看这个生产例子——航班预订 SAGA：

```python
def to_compensate(state: BookingState, error: NodeError) -> Command:
    return Command(
        update={"completed": [f"FAILED: {error.node}"]},
        goto="compensate",
    )

graph = (
    StateGraph(BookingState)
    .set_node_defaults(retry_policy=RETRYABLE, error_handler=to_compensate)
    .add_node("reserve_seat", reserve_seat)
    .add_node("process_payment", process_payment)
    .add_node("issue_ticket", issue_ticket)
    .add_node("compensate", compensate)
    .add_edge(START, "reserve_seat")
    .add_edge("reserve_seat", "process_payment")
    .add_edge("process_payment", "issue_ticket")
    .add_edge("issue_ticket", END)
    .compile(checkpointer=checkpointer)
)
```

**compensate 节点**是 SAGA 模式的标准实现：

```python
def compensate(state) -> Command[Literal["__end__"]]:
    if "issue_ticket" in state["completed"]: void_ticket(state)
    if "process_payment" in state["completed"]: refund_payment(state)
    if "reserve_seat" in state["completed"]: release_seat(state)
    return Command(goto=END)
```

**error_handler 的四个关键设计属性**（让这套机制真正 production-grade 的核心）：

| 属性 | 含义 | 为什么重要 |
|------|------|----------|
| **1. 仅在重试耗尽后触发** | 不是每次异常都跑 | 想「每次异常都跑」直接在节点内 try/except，不要用 error_handler |
| **2. 失败上下文自动注入** | handler 签名 `(state, error: NodeError)` | `error.node` 知道是哪个节点失败，`error.error` 是原始异常 |
| **3. 原子 superstep 调度** | 原节点失败时，handler 与同 superstep 的其他节点**并行**调度 | 关键进程：不能失败后回到 regular steps，必须立刻进 compensation |
| **4. 崩溃恢复幂等** | 如果 handler 运行中途 host 进程崩溃，下次恢复会重新调度 handler，**不**重新跑原失败节点 | 这是 checkpoint + handler 重新调度的关键保证——handler 本身要写成幂等 |

**与传统 try/except 的根本区别**：

| 维度 | try/except | error_handler |
|------|------------|---------------|
| 状态归属 | 应用层局部变量 | 图全局 state（checkpointer 持久化） |
| 失败时下一步 | 写代码决定（goto、return） | 通过 `Command(goto="compensate")` 改图结构 |
| 崩溃恢复 | 状态丢失，需重头跑 | checkpoint + handler 重新调度 |
| 多步骤回滚 | 手工追踪「已经做了哪些 step」 | `state["completed"]` 由框架自动累积 |

**`set_node_defaults` 的全局 + per-node override 模式**：

```python
.set_node_defaults(retry_policy=RETRYABLE, error_handler=to_compensate)
.add_node("reserve_seat", reserve_seat)        # 用默认
.add_node("process_payment", process_payment,   # per-node override
          retry_policy=RetryPolicy(max_attempts=10))
```

per-node override 始终胜出——这让「大部分节点用通用策略，少量关键节点用特殊策略」成为一行配置。

---

## 副观点 5：SAGA 模式从分布式系统借来——LangGraph 让 Agent 自然获得「all-or-nothing 业务语义」

> **关键洞察**：分布式事务的两阶段提交（2PC）在 Agent 场景几乎不可用（外部服务不支持 XA），SAGA 是唯一可工程化的替代。LangGraph 的图结构天然适合表达 SAGA——「已完成步骤」+「补偿节点」+「原子调度」是 SAGA 的三件套。

航班预订场景揭示了一个普适问题：**当一个业务流程跨多个外部服务调用，任何一步失败都不能简单放弃**：

- 座位预留成功 → 支付失败 → 不能就这么走，座位在别人手里
- 支付成功 → 出票失败 → 不能就这么走，用户付了钱没拿到票
- 出票成功 → 任何下游失败 → 票已出，无所谓

**传统解决方案**：分布式事务（XA / 2PC）——要求所有外部服务都支持事务协议。**现实**：LLM provider、支付网关、第三方 API 都不支持 2PC。

**SAGA 模式**：
1. 把长事务拆成 N 个本地事务
2. 每个本地事务有对应的「补偿事务」（reverse action）
3. 任意一步失败，按反序执行已完成的补偿事务
4. 业务层面达到「all-or-nothing」语义

**LangGraph 的图结构如何承载 SAGA**：

- **每个节点 = 一个本地事务**（reserve_seat / process_payment / issue_ticket）
- **`error_handler` = 跳转到补偿节点**的机制
- **`completed: Annotated[list[str], operator.add]`** = 「已完成步骤」的累积记录
- **`compensate` 节点 = 反序执行补偿事务**的图节点

这套机制的关键工程化细节：

```python
class BookingState(TypedDict, total=False):
    completed: Annotated[list[str], operator.add]  # 关键：operator.add 让 reducer 自动累积
```

`operator.add` 是 LangGraph 的 reducer 机制——多个节点向 `completed` 写值时，框架自动拼接，而不是覆盖。这让「已完成的步骤」成为**图级别的状态**，所有节点都能读，而补偿节点据此决定反序执行哪些补偿。

**与传统 SAGA 实现的对比**：

| 维度 | 传统 Saga Orchestrator（Camunda / Temporal） | LangGraph |
|------|-------------------------------------------|-----------|
| 状态持久化 | 单独的状态机数据库 | checkpoint 内置 |
| 补偿逻辑 | 单独的工作流 | 图节点 |
| LLM/tool 集成 | 需要 adapter | 节点本身就是 Python 函数 |
| 启动成本 | 需要部署 orchestrator 服务 | 一行 `.compile()` |

LangGraph 的「workflow engine + Agent」融合让 SAGA 从「分布式系统架构组件」变成「Agent 业务逻辑的自然部分」——这是降低 Agent 生产门槛的关键工程贡献。

---

## 与现有体系的关联

### 与 LangSmith / LangChain 的关系

- **LangGraph** 是工作流引擎，负责图的执行与错误处理
- **LangSmith** 是可观测性平台，记录每个节点执行、retry 次数、error_handler 触发——为生产调试提供数据
- **deepagents**（LangChain 的高层 agent 框架）底层用 LangGraph，自动继承 fault tolerance 能力

### 与 Anthropic Containment 三层防御的关系（R244 已发表）

- **LangGraph fault tolerance** = 节点级别的「错误可恢复性」设计（构建阶段）
- **Anthropic Containment** = 产品级别的「爆炸半径控制」设计（部署阶段）
- 两者互补：一个让单步失败可控，一个让多步组合的失败后果可控

### 与 OpenAI Codex Agent Loop 的关系（R215 已发表）

- **Codex Agent Loop** 用 prompt caching + compaction 解决「长跑上下文爆炸」
- **LangGraph fault tolerance** 用 SAGA + checkpoint 解决「长跑失败回滚」
- 都是「long-running agent」的基础设施，但 Codex 偏「memory 维度」，LangGraph 偏「control flow 维度」

---

## 工程实现细节：LangGraph 1.0 的具体 API

### 三个核心类型

```python
from langgraph.types import RetryPolicy, TimeoutPolicy
from langgraph.errors import NodeError

# 1. RetryPolicy：每节点重试配置
RetryPolicy(
    initial_interval=0.5,
    backoff_factor=2.0,
    max_interval=128.0,
    max_attempts=3,
    jitter=True,
    retry_on=(ConnectionError, TimeoutError),  # 或 callable
)

# 2. TimeoutPolicy：双时钟
TimeoutPolicy(
    run_timeout=30.0,
    idle_timeout=5.0,
    refresh_on="auto",  # 或 "heartbeat"
)

# 3. error_handler：函数签名
def handler(state, error: NodeError) -> State | Command:
    pass
```

### 完整生产代码模板

```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, RetryPolicy, TimeoutPolicy
from langgraph.errors import NodeError
from typing import TypedDict, Literal

class State(TypedDict):
    status: str
    completed: list[str]

RETRYABLE = RetryPolicy(
    initial_interval=0.5,
    backoff_factor=2.0,
    max_interval=30.0,
    max_attempts=4,
    jitter=True,
    retry_on=(ConnectionError, TimeoutError),
)

TIMEOUT = TimeoutPolicy(run_timeout=60.0, idle_timeout=10.0)

def fallback(state, error: NodeError) -> Command[Literal["end"]]:
    return Command(update={"status": "failed"}, goto="end")

def build_graph():
    return (
        StateGraph(State)
        .set_node_defaults(
            retry_policy=RETRYABLE,
            timeout=TIMEOUT,
            error_handler=fallback,
        )
        .add_node("step1", step1)
        .add_node("step2", step2)
        .add_node("end", lambda s: s)
        .add_edge(START, "step1")
        .add_edge("step1", "step2")
        .add_edge("step2", "end")
        .compile(checkpointer=checkpointer)
    )
```

---

## 一句话总结

LangGraph fault tolerance 三件套的本质是：**把「重试/超时/补偿」从应用层样板代码上升为工作流引擎的图原语**——开发者用「声明性配置」告诉框架「这个节点最多重试 4 次、整体 60 秒、失败后跳到 compensate」，框架用「superstep 原子调度 + checkpoint 持久化」保证这些语义在崩溃恢复后依然成立。这是 Agent 从 prototype 走向 production 的关键工程化跨越。
