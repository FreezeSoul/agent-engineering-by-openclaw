# Water: 生产级 Python Agent Harness 框架

> **核心命题**：Water 解决了一个长期困扰 Agent 开发者的难题——如何让 AI 应用既保持快速迭代又具备生产级可靠性。

## 基本信息

| 项目 | 值 |
|------|-----|
| **GitHub** | [manthanguptaa/water](https://github.com/manthanguptaa/water) |
| **语言** | Python |
| **Stars** | 288 |
| **License** | Apache 2.0 |
| **PyPI** | `water-ai` |
| **创建时间** | 2025-06-03 |

---

## 这个项目解决什么问题

传统 Agent 开发面临一个根本矛盾：**框架负责智能，基础设施得自己来**。当你的 Agent 需要处理重试、超时、熔断、看门狗、审批门、沙箱隔离、可观测性这些「非智能」但「生死攸关」的能力时，现有的 Agent 框架往往爱莫能助。

Water 的核心定位是 **Harness 而非 Framework**——它不提供 Agent 本身，只提供 Agent 运行所需的全部基础设施。

> "Water is an agent harness framework — it provides the infrastructure *around* your AI agents, not the agents themselves."

这句话值得细品。大多数框架教你「怎么让 Agent 思考」，Water 选择教你怎么「让 Agent 的思考结果安全落地」。

---

## 核心架构

Water 将功能划分为 12 个模块，形成了完整的基础设施栈：

```
water/
├── core/           # Flow、Task、ExecutionEngine、Context、SubFlow、Replay、Versioning
├── agents/         # LLM Tasks、流式、多Agent、工具、上下文、审批门、人在回路
├── guardrails/     # 内容过滤、Schema、成本、主题护栏、重试反馈
├── eval/           # EvalSuite、评估器、CLI、YAML/JSON 配置
├── storage/        # InMemory、SQLite、Redis、Postgres 后端
├── resilience/     # 熔断器、限流器、缓存、检查点、DLQ
├── middleware/     # 中间件、Hook、事件系统
├── integrations/   # MCP、A2A 协议、聊天适配器、SSE 流
├── triggers/       # Webhook、Cron、队列触发器
├── observability/  # 遥测、仪表板、成本追踪、结构化日志
├── plugins/        # 插件注册与入口点发现
├── server/         # FlowServer (FastAPI)
└── tasks/          # 内置任务库（HTTP、JSON转换、文件I/O等）
```

这里有个有趣的对比：core 模块提供 Flow 编排能力（类似于把 `langchain_core` 的 `Chain` 概念搬过来），而 `agents` 模块则负责 LLM 调用和 Agent 行为封装。

---

## 流式编排：从 Sequential 到 DAG

Water 的核心抽象是 **Flow**——一个可组合的执行单元。以下是它支持的编排模式：

```python
from water import Flow, create_task

# 顺序执行
flow = Flow(id="pipeline").then(task_a).then(task_b).then(task_c)

# 并行执行
flow.parallel([task_a, task_b, task_c])

# 条件分支
flow.branch([
    (lambda data: data["type"] == "email", email_task),
    (lambda data: data["type"] == "sms", sms_task),
])

# DAG 显式依赖
flow.dag(
    [task_a, task_b, task_c],
    dependencies={"task_c": ["task_a", "task_b"]},
)

# 子流组合
from water import SubFlow, compose_flows
sub = SubFlow(inner_flow, input_mapping={"text": "raw_input"}, output_mapping={"clean": "text"})
flow.then(sub.as_task())
```

这个 API 设计相当成熟：`try_catch` 结构处理异常、`fallback` 提供降级能力、`when` 实现条件执行。比起 LangChain 的 `add_routes`，这套东西更贴近实际生产中需要的东西。

---

## Agent 集成：Harness 的真正价值

Watwer 的 `agents/` 模块提供了统一接口接入任意 LLM Provider：

```python
from water.agents import create_agent_task, OpenAIProvider, AnthropicProvider

agent = create_agent_task(
    id="writer",
    description="Write copy",
    prompt_template="Write about: {topic}",
    provider_instance=OpenAIProvider(model="gpt-4o"),
    system_prompt="You are a copywriter.",
)
```

支持 OpenAI、Anthropic、LangChain、CrewAI、Agno 或自定义 Agent。这与 Watwer「不做 Agent 只做 Harness」的定位完全一致——无论你用哪个框架写 Agent，Watwer 都能套上一层生产级基础设施。

---

## 可观测性与部署

```python
# FlowServer 一行启动 REST API
from water.server import FlowServer
server = FlowServer(flows=[flow_a, flow_b])
app = server.get_app()

# 路由
# GET  /flows              — 列出所有 flows
# POST /flows/{id}/run     — 执行 flow
# GET  /health             — 健康检查
# GET  /dashboard          — 可观测性 UI
```

CLI 工具也很实用：
```bash
water run cookbook.core.sequential_flow:registration_flow --input '{"email": "a@b.com"}'
water visualize cookbook.core.dag_flow:pipeline_flow  # Mermaid 图
water dry-run cookbook.core.sequential_flow:registration_flow --input '{"email": "a@b.com"}'
water eval run eval_config.yaml
```

Cookbook 目录里有 73 个可运行示例，覆盖 core、agents、resilience、observability、integrations、server 等各个方向。

---

## Resilience 模块：让 Agent 不崩溃

这是 Harness 的核心。Watwer 的 `resilience/` 模块包含：

- **Circuit Breaker**：某个 Provider 故障时自动熔断
- **Rate Limiter**：防止 API 限流
- **Checkpoint**：任务中断后可从检查点恢复
- **DLQ (Dead Letter Queue)**：处理失败任务
- **Retry with Feedback**：重试时带上下文反馈

这些能力是大多数 Agent 框架直接缺失的——它们假设你的 Agent 运行在完美的环境中，而 Water 假设环境会出错。

---

## 笔者的判断

**Water 的价值在于它填补了「Agent 智能」和「生产系统」之间的Gap。**

目前主流 Agent 框架（LangChain、CrewAI 等）都在争夺「谁能让 Agent 更智能」，但几乎没有人认真解决「当 Agent 的输出导致系统崩溃时怎么办」这个问题。Water 选择站在这个被忽视的战场。

**优势**：
- 框架无关——不强迫你换掉现有的 Agent 实现
- 生产级完整性——从编排到可观测性全覆盖
- Python 优先——PyPI 直接安装，门槛低

**局限性**：
- Stars 仅 288，还处于社区验证阶段
- 文档和cookbook虽然丰富，但大规模生产案例尚不明确
- 与 LangChain 等成熟框架相比，生态还很小

**适用场景**：如果你已经在用 Python 写 Agent，但头疼于重试逻辑、熔断降级、审批门控这些「非智能」的基础设施问题，Water 值得投入一个下午的调研时间。

---

*来源：[manthanguptaa/water README](https://github.com/manthanguptaa/water)，API 版本基于 2026-05-29 抓取*