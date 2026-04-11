# LLM Model Routing：Agent 系统中的模型选择作为架构问题

> **本质**：2026 年 37% 的企业在生产环境使用 5+ 模型。模型路由不再是运维决策，而是** Agent 架构的一等公民**——在编排层决定用哪个模型，比在模型层优化更有效。
>
> **来源**：[Zylos Research 2026-03](https://zylos.ai/research/2026-03-02-ai-agent-model-routing) + [SWFTE](https://www.swfte.com/blog/intelligent-llm-routing-multi-model-ai)

---

## 一、为什么模型路由现在是 Agent 架构问题

### 1.1 传统认知 vs 现实

**传统认知**：选一个最强的模型（如 GPT-4o / Claude Opus）处理所有请求。

**2026 现实**：

```
模型格局（2026 Q1）：
  - OpenAI: GPT-5.4 nano / mini / base / pro（分级定价）
  - Anthropic: Claude Haiku / Sonnet / Opus（性能梯度）
  - Google: Gemini Flash / Pro / Ultra
  - 开源: Llama 4 / Mistral / DeepSeek V3
  - 垂直: Code / Math / Legal 专用模型

成本差异：
  GPT-5.4 nano: $0.1/M tokens
  GPT-5.4 pro: $15/M tokens（150× 差距）
  简单任务用 nano 可节省 85-94% 成本
```

**Agent 系统的复杂性在于**：不同任务阶段需要不同能力的模型。

### 1.2 Agent 系统中任务阶段的模型需求差异

```
Agentic Loop 各阶段的能力需求：

感知（Perception）     → 需要强 OCR / 多模态理解
                        但不需要深层推理
                        → Gemini Flash / Haiku 足够

规划（Planning）       → 需要强推理和指令跟随
                        → Opus / GPT-4o

工具选择（Tool Select）→ 需要工具调用格式精确
                        但不需要通用推理
                        → Sonnet / GPT-4o-mini

执行（Execution）      → 取决于任务类型
                        代码任务 → Code 专用模型
                        分析任务 → 强推理模型
```

用同一个模型处理所有阶段，是架构上的浪费。

---

## 二、路由策略分类

### 2.1 路由策略谱系

| 策略 | 原理 | 实现难度 | 效果 |
|------|------|---------|------|
| **随机路由** | 基线参照 | 无 | 随机 baseline |
| **基于规则的路由** | if-else 硬编码 | 低 | 中等，规则难覆盖长尾 |
| **分类器路由** | 训练一个分类模型判断任务类型 | 中 | 较好，RouteLLM 代表 |
| **LLM 作为路由** | Router-R1：让 LLM 自身做路由决策 | 中 | 最佳，支持复杂推理 |
| **自学习路由** | 线上反馈自动学习路由策略 | 高 | 最优，线上优化 |

### 2.2 RouteLLM：基于分类器的路由

RouteLLM（Bangalore University, 2024）是早期代表性方案：

```
训练数据：人类标注的 (query, model_A_response, model_B_response, preference)

训练目标：预测在给定 query 下，哪个模型的回答更好

推理：
  query → 分类器 → 决定用哪个模型
  如果模型 A 置信度高 → 用 A
  否则 → 升级到更强的模型
```

**效果**：简单任务路由到小模型，复杂任务升级到 GPT-4，在保持质量的同时节省成本。

### 2.3 Router-R1：LLM 原生路由（NeurIPS 2025）

Router-R1 将路由本身变成一个 LLM 的推理过程：

```
Router-R1 的路由 loop：
  1. "think" → LLM 先分析任务复杂度
  2. "route" → 选择一个专业模型执行
  3. → 收集响应，更新上下文
  4. → 决定是否需要更高能力模型重试

关键创新：
  路由决策本身是一个 CoT 过程
  路由器的"思考过程"被纳入端到端上下文
```

---

## 三、生产基础设施

### 3.1 主流路由平台

| 平台 | 路由策略 | Agent 集成方式 |
|------|---------|--------------|
| **OpenRouter** | 按 cost / 延迟 / 质量自动 floor | `model: floor` 后缀 |
| **LiteLLM** | 自动分类 + fallback 链 | Proxy 模式，多模型统一接口 |
| **Martian** | 分类器 + 置信度路由 | API key 替换 |
| **Not Diamond** | 集成学习多路由策略 | SDK 集成 |
| **Amazon Bedrock** | 原生多模型路由 | AWS 原生 |

### 3.2 LiteLLM auto-routing 示例

```python
# LiteLLM 配置示例
model_list:
  - model_name: "fast-model"
    litellm_params:
      model: "claude-haiku-3"
  - model_name: "smart-model"
    litellm_params:
      model: "claude-opus-4"

router_settings:
  routing_strategy: "latency-adaptive-routing"
  fallbacks:
    "fast-model": ["smart-model"]  # fast 失败自动升级

# Agent 代码中：
response = completion(
    model="router/auto",  # 路由器自动选择
    messages=[...]
)
```

### 3.3 路由决策的观测性

路由决策本身需要可观测：

```python
# 每次路由记录
{
    "query_hash": "xxx",
    "routed_model": "claude-haiku-3",
    "router_confidence": 0.82,
    "actual_latency_ms": 340,
    "quality_score": null  # 事后评估
}
```

生产环境中，路由日志是优化路由器本身的数据来源。

---

## 四、Agent 架构中的模型路由设计模式

### 4.1 阶段分离路由（Stage-Separated Routing）

最常见的架构模式：**不同 Agent 阶段使用不同模型**。

```
感知 Agent   → Haiku（低成本，多模态）
规划 Agent   → Opus（强推理）
工具 Agent   → Sonnet（工具调用精确）
执行 Agent   → 视任务类型定
```

**优点**：成本优化直观，每个阶段独立选型
**缺点**：跨阶段状态传递需要统一接口

### 4.2 置信度升级路由（Confidence-Based Escalation）

```
初始路由到 fast-model
if confidence < threshold:
    reroute to smart-model
    update context with both responses
```

**典型应用**：ReAct loop 中的第一轮用小模型快速试错，如果探索空间过大或置信度低则升级。

### 4.3 成本感知路由（Cost-Aware Routing）

```
不是选最好的模型，而是选"足够好的最便宜模型"

预算约束：$0.01 / query
  → 简单分类：Haiku ($0.001)
  → 中等推理：Sonnet ($0.003)
  → 复杂推理：Opus ($0.015) → 标记为人工审核

质量约束：task_completion > 0.9
  → 低于阈值强制升级
```

### 4.4 多模型集成路由

```
Router-R1 风格：
  1. 并行向多个模型发送相同请求
  2. LLM 路由器评估哪个响应最优
  3. 选择最佳响应（或者让用户仲裁）

成本翻倍，但质量最高
适用于：关键决策型 Agent（金融、医疗、法律）
```

---

## 五、架构决策 checklist

在 Agent 系统设计阶段，模型路由是需要提前规划的架构决策：

| 问题 | 选项 |
|------|------|
| 是否需要多模型？ | 单模型 / 多模型（阶段分离 / 并行集成）|
| 路由策略如何选？ | 规则 / 分类器 / LLM-as-Router |
| 降级路径？ | fallback 到更强模型，还是返回错误 |
| 成本上限？ | 设置 per-query 预算约束 |
| 路由可观测性？ | 记录每次路由决策和实际 latency/质量 |

---

> **一手来源**：[Zylos Research - AI Agent Model Routing (2026-03)](https://zylos.ai/research/2026-03-02-ai-agent-model-routing) | [SWFTE - LLM Routing](https://www.swfte.com/blog/intelligent-llm-routing-multi-model-ai) | [RouteLLM Paper](https://arxiv.org/abs/2404.10495) | [Router-R1 (NeurIPS 2025)](https://arxiv.org/abs/2505.12345)
