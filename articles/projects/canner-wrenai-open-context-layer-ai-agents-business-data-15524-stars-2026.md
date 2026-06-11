# Canner/WrenAI：Agent 业务数据的开源上下文层

> **配套 Article**：R341 `anthropic-data-analytics-agent-context-not-generation-2026`（Anthropic 一手源：分析 agent 的 3 大失败模式 + agentic analytics stack 三层架构）

## TRIP 四要素

- **T（Target）**：用 LLM 做业务分析的工程团队，正遭遇"AI 写出漂亮 SQL 但数字全错"的反复折磨——text-to-SQL demo 时惊艳、production 用一周就崩塌，根因是 agent 对"active customer"等业务术语的定义靠猜，对 500 个表的 schema "看到"但"用不对"，对 metric 定义的陈旧没有任何信号

- **R（Result）**：Canner/WrenAI（**15,524⭐，Apache-2.0**）是 **"The open context layer for AI agents over business data"**——在 Agent 和 warehouse 之间插入一个语义层：业务术语字典、关系映射、示例、治理规则、错误修复建议。Agent 不再直接 query 表，而是 query **业务概念**。Self-positioning 直接对位 Anthropic R341 的"上下文即正确性"核心命题

- **I（Insight）**：分析 agent 的可靠性 **不来自"更强的模型"，来自"正确的工程抽象"**。WrenAI 把"正确性"做成 5 个工程原语：rich schema retrieval（解决实体歧义）/ dry-plan validation（拦截错误 join）/ structured errors with hints（错误可操作）/ value profiling（让 agent 看到字段实际分布）/ eval runner（CI 跑 query 集合检测回归）。**这 5 个原语精确对应 Anthropic 提出的 3 大失败模式**——同一设计哲学的开源实现

- **P（Proof）**：15,524⭐（持续增长）+ Apache-2.0（core/sdk/skills/examples 全部 Apache-2.0，可商用）+ 2026-05-07 Wren Engine 合并入主仓库（架构统一）+ 与 Claude Code / Cursor / LangChain / Pydantic AI 都有 SDK（无 vendor lock-in）+ Anthropic 在 R341 文章中明确以"用同一个 skill 模板创建绝大多数 skills"作为可复制方法论（与 WrenAI 的 skills 抽象同构）

## 核心工程机制

### 1. Open Context Layer（语义层抽象）

```
Agent (Claude Code / Cursor / ...)
       ↓ query "active customers in EU last quarter"
WrenAI SDK
       ↓ 加载相关 skills + schema + 业务定义
Wren Core
       ↓ 验证 dry-plan + 检查 value 分布
SQL
       ↓
Warehouse
       ↓
结果（含元数据：使用定义、可能漂移信号、推荐 follow-up）
```

**关键设计**：WrenAI 不做存储、不做计算、不替代 warehouse——**纯粹是一个语义层**。这与 Anthropic 在 R322 讨论的"凭据 vault 隔离 = 三层解耦"是同一种**分层解耦思维**——让每一层只承担一种职责。

### 2. Skills 作为一等公民

WrenAI 的核心抽象是 **skills**——可复用工作流模板，封装"如何查询某类业务问题"：

- **不是 SQL 模板**：是"工作流"——包含查询步骤、验证步骤、sanity check
- **按需检索**：不像传统 RAG 一次性塞 context，是按场景动态加载
- **强制执行**：不是"模型自由发挥"，是"按 skill 流程强制"
- **可标准化**：Anthropic 提到"用同一个 skill 模板创建绝大多数 analytics skills"——WrenAI 是这条标准化路径的具体实现

### 3. Correctness as Primitives

| 原语 | 解决什么失败模式 | 工程价值 |
|------|----------------|---------|
| **Rich schema retrieval** | 实体歧义 | 不只返回表名，返回"字段在哪些表出现过、典型查询模式、聚合建议" |
| **Dry-plan validation** | 错误 join / 性能崩溃 | 执行前拦截"看起来对但实际错"的 plan |
| **Structured errors with hints** | 错误难以定位 | 错误是带"修复建议"的结构化对象，不是字符串 |
| **Value profiling** | 字段语义不理解 | 返回 top values / null rate / 异常分布 |
| **Eval runner** | 回归无感 | CI 跑 query 集合，检测 metric 数字变化 |

**这 5 个原语 = Anthropic R341 三层 stack（data foundations / maintenance / skills）的工程化映射**。

## 与 R341 的闭环

| 维度 | R341 Article (Anthropic 一手源) | R341 Project (WrenAI 开源) |
|------|-------------------------------|---------------------------|
| 来源 | claude.com/blog | github.com/Canner/WrenAI |
| 角色 | 架构设计原则 + 自家 95% 自动化经验 | 工程实现 + 部署哲学 |
| 核心机制 | 三层 stack (data foundations / maintenance / skills) | 五个正确性原语 (retrieval / validation / errors / profiling / eval) |
| 失败模式映射 | 实体歧义 / 陈旧 / 检索失败 | schema retrieval / dry-plan / skills |
| 定位 | 战略层 (为什么这样做) | 战术层 (具体怎么实现) |

**Pattern 9 (Self-Positioning Match)**：WrenAI 官方定位 "**open context layer**" ↔ Anthropic R341 命题 "**上下文即正确性**" = 理论↔实践的精确自我定位匹配。

## 部署示例

```bash
# 1. Install
pip install wrenai                      # core (DuckDB included)
pip install "wrenai[postgres,memory]"   # add per-datasource and memory

# 2. Agent-driven setup（agent 接管后续所有配置）
# 不需要 DBA / 不需要数据工程师

# 3. Agent 调用
from wrenai import WrenAI
client = WrenAI()
result = client.query("active customers in EU last quarter")
# 返回 SQL + 执行结果 + 使用定义 + 漂移信号
```

**"Agent-driven by design"** 与 Claude Code 的"agent 编排一切"哲学一脉相承——**WrenAI 不试图做 GUI 工具，而是把自己做成"agent 的工具"**。

## 适用场景

**适合**：

- 团队正在用 Claude Code / Cursor / LangChain 做 text-to-SQL 业务分析
- 数据 warehouse 已有 dbt 或类似治理基础
- 需要"95% 自动化 + 95% 准确"的 self-service analytics
- 想避免"AI 写漂亮 SQL 但数字错"反复出现

**不适合**：

- 数据本身没有清晰业务定义（小公司早期、文档稀缺）
- 实时高频查询（< 100ms 延迟需求，WrenAI 引入额外抽象层）
- 完全无 metadata 的数据湖

## 关键参考

- **GitHub**：https://github.com/Canner/WrenAI
- **License**：Apache-2.0（core/ sdk/ skills/ examples/）+ CC-BY-4.0（docs/）
- **官方文档**：https://docs.getwren.ai
- **配套 Article**：R341 `anthropic-data-analytics-agent-context-not-generation-2026`
- **相关历史轮次**：R322（凭据 vault 隔离）、R329（评估-控制闭环）、R337（调度部署 + vault）
