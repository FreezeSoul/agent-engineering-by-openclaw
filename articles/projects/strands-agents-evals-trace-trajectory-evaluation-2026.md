# Strands Evals：面向生产环境的 Agent 评估框架

**GitHub**: [strands-agents/evals](https://github.com/strands-agents/evals)  
**语言**: Python / TypeScript  
** Stars**: 待获取（活跃项目）  
**定位**: 来自 Strands Inc.（Amazon 投资）的生产级 Agent 评估 SDK

---

## 为什么值得关注

Strands Evals 是少数**从第一天就面向生产环境设计**的 Agent 评估框架。相比学术导向的评测基准（如 SWE-bench）和研究原型（如大多数框架内置的评估模块），Strands Evals 的设计重点是：

> "From simple output validation to complex multi-agent interaction analysis, trajectory evaluation, and automated experiment generation"

它的核心差异在于**把 OpenTelemetry trace 引入评估体系**——这意味着它不只是评估输出，还能分析 agent 的**行为轨迹**，这在生产环境中排查问题时至关重要。

---

## 核心功能

### 1. Custom Rubrics（自定义评分规则）

```python
from strands_eval import StrandsEvaluator

evaluator = StrandsEvaluator(
    rubric={
        "criteria": [
            "Response addresses all parts of the question",
            "Code examples are syntactically correct",
            "Explanations are clear for intermediate developers"
        ],
        "weights": [0.4, 0.3, 0.3]
    }
)

result = evaluator.evaluate(agent_response)
```

基于 LLM-as-a-Judge 的评分，但支持灵活的评分规则定义和权重配置。

### 2. Trajectory Evaluation（轨迹评估）

这是 Strands Evals 最有特色的功能。传统评估只看最终输出，但轨迹评估分析 **agent 的整个工具调用序列**：

- 工具调用的顺序是否合理
- 参数是否正确
- 是否在错误的工具上重复尝试
- 是否有关键步骤遗漏

```python
evaluator = StrandsEvaluator(metric="trajectory")

result = evaluator.evaluate(
    tool_calls=[
        {"tool": "search", "args": {"query": "..."}},
        {"tool": "read_file", "args": {"path": "..."}},
        {"tool": "write", "args": {"content": "..."}}
    ]
)
# 返回：工具使用评分、参数准确性、效率评分
```

### 3. OpenTelemetry Trace-Based Helpfulness Evaluation

将 agent 的行为序列转换为 **七级 helpfulness 评分**，基于 OpenTelemetry trace 数据：

```
Level 1: 完全无用
Level 2: 基本无用
Level 3: 略微有帮助
Level 4: 中等有用
Level 5: 很有帮助
Level 6: 非常有帮助
Level 7: 超出预期
```

这个评分体系的价值在于：它把"用户体验"量化为可追踪的指标，而且基于 trace 数据而非人工判断，可以在生产环境中持续收集。

### 4. Multi-Turn Conversation Simulation（ActorSimulator）

模拟真实用户对话来测试 agent 的多轮交互能力：

```python
from strands_eval import ActorSimulator

simulator = ActorSimulator(
    scenario="customer_support",
    user_persona="impatient_user",  # 模拟不耐烦的用户
    max_turns=10
)

trajectory = simulator.run(agent)
# 自动验证：
# - 是否在规定轮次内解决问题
# - 是否保持了上下文
# - 是否正确处理了用户的打断
```

### 5. ToolSimulator

用 LLM 模拟工具行为，在**不调用真实工具**的情况下测试 agent 的工具使用能力。这对于：
- 测试环境无法访问外部 API
- 需要快速原型验证
- 需要隔离测试 agent 逻辑

特别有价值。

### 6. MLLM-as-a-Judge

支持多模态 LLM 作为评判者，用于评估**包含图像的 agent 响应**（如 UI agent、视觉 agent）。

---

## 与同类框架的对比

| 维度 | Strands Evals | OpenJudge | DeepEval | LangChain RubricMiddleware |
|------|--------------|-----------|----------|---------------------------|
| **轨迹评估** | ✅ 工具调用序列分析 | ❌ | ❌ | ❌ |
| **Trace 集成** | ✅ OpenTelemetry | ❌ | ❌ | ❌ |
| **多轮模拟** | ✅ ActorSimulator | ❌ | ❌ | ❌ |
| **工具模拟** | ✅ ToolSimulator | ❌ | ❌ | ❌ |
| **Reward 信号** | 待确认 | ✅ | ❌ | ✅ 自评反馈 |
| **多模态评估** | ✅ MLLM-as-Judge | ✅ | ❌ | ❌ |
| **生产级定位** | ✅ | ✅ | ✅ | ⚠️ Beta |

Strands Evals 的优势在于**轨迹级分析能力**和**生产环境集成**——它不是为学术基准设计的，而是为真实系统在生产中的持续质量监控设计的。

---

## 适用场景

- **生产环境质量监控**：用 OpenTelemetry trace 数据持续评估 agent 表现
- **多轮对话 agent 测试**：ActorSimulator 可以自动化模拟用户对话场景
- **工具使用能力的隔离测试**：ToolSimulator 让你不需要真实 API 就能测试
- **需要轨迹诊断的复杂 agent**：当 agent 失败时，轨迹分析比单纯看输出更能定位问题

---

## 快速开始

```bash
pip install strands-agents[strands_eval]
```

```python
from strands_eval import StrandsEvaluator

evaluator = StrandsEvaluator(metric="rubric")
result = evaluator.evaluate(
    response="Your agent's response here",
    rubric=["Response is helpful", "Code examples are correct"]
)
print(result.score, result.feedback)
```

官方文档: https://github.com/strands-agents/evals