# CrewAI Token 经济学：企业 Agent 投入产出的 5 大烧钱陷阱与 70-85% 成本下降路径

> **核心命题**：2026 年中一个反直觉的事实正在发生——单位智能成本以每年 10x 的速度下降，**但企业 AI 账单总额却在爆炸**。这不是模型定价问题，而是 Agent 系统缺乏「token 经济学」运营纪律的问题。**70-85% 的成本下降空间不靠更换更便宜的模型，而靠把成本控制嵌进编排层与基础设施层。**

---

## 一、为什么「模型便宜了」反而烧钱更多

CrewAI Enterprise 团队在 2026 年 6 月 2 日发布的 "How to Optimize Token Spend for Better Agentic ROI" 一文中给出了一组令人警醒的数据：

> "Half way thru 2026 and per-unit intelligence costs are dropping roughly 10x a year while total AI costs explode."

把这句放在今天的语境下读：**Opus 4.7 的价格可能只有 2025 年同期的十分之一，但一个企业 agentic 系统的月度账单可以是从前年的十倍**。两者并不矛盾——前者是技术红利，后者是规模化阶段的必然结果。

具体的烧钱结构是这样的：

| 类别 | Token 量级 | 备注 |
|------|----------|------|
| 推理模型的隐藏消耗 | 20,000-50,000 tokens / 一次回答 | 思考过程对用户不可见 |
| Agent 循环的累积放大 | 10 步 × 30K context = 500K-2M tokens | 每次循环重传完整上下文 |
| RAG 管道输入体积 | 50,000-200,000 input tokens / call | Tool schemas + few-shot examples |
| 模型过度配置 | 60-80% 的企业 token 支出 | 跑在不该用的强模型上 |

**笔者认为**：这五条的核心洞察是「成本不是模型决定的，是 Agent 循环结构决定的」。一个用 Haiku 4.5 处理所有判断步骤的系统，可能比一个全用 Opus 4.8 但循环收敛得快的系统更贵。

---

## 二、五大烧钱陷阱

### 2.1 推理模型的「隐形 token」

推理模型在产出 500 token 答案前可能已经消耗 20,000-50,000 token 思考过程。这个消耗对调用方不可见、对话 UI 上不会显示。**用户只看到最终输出，P&L 表上看到的是几十倍的账面值**。

最危险的是：开发者在本地用非推理模型调试，部署时切换到推理模型，行为没变、效果没变，账单却翻了 50 倍。

### 2.2 Agent 循环的「指数放大」

一个 10 步的 Agent 循环，每步重传完整 30K 上下文的系统，会达到 500K-2M tokens。如果这个循环还涉及子 Agent 之间的状态传递，再叠加一个数量级。

**关键的工程观察**：循环放大不是「10 步 × 30K」这么简单，因为每步可能还会触发 RAG 检索、工具调用、子 Agent 委派，**每一层都把 token 体积乘以一个常数**。

### 2.3 工具 schema 的「输入体积税」

10 个工具，每个工具 schema 500 tokens，每次 Agent 调用都会把全部 10 个 schema 作为输入 token 计费——**5,000 tokens / call** 的隐性税。如果一个循环调用 100 次工具，就是 500K tokens 的纯 schema 开销。

更隐蔽的：很多团队把工具描述写得过长（"这是一个用来查询数据库的工具，它接受 SQL 语句并返回结果..."），把示例放在 schema 里，把可选参数都列出来——**每条冗余都是线性放大**。

### 2.4 模型选择的「路径依赖」

团队一旦习惯了「默认用 Opus 4.8」，就再也不会回头用 Haiku 4.5。这种「Frontier 偏好」会在三个地方同时放大成本：

1. **分类任务**——把意图分类、判断真假这种任务跑在 Opus 上，是 1/15 的浪费
2. **JSON 解析**——很多团队的代码解析 JSON 时还在调 LLM，而不是用确定性代码
3. **失败重试**——主任务失败后，重试用的还是同一模型、同一 prompt，没降级

### 2.5 没有 ROI 验证的「持续实验」

CrewAI 给出的最尖锐判断：

> "An estimated 60-80% of enterprise token spend goes to use cases that haven't proven business value."

**企业 AI 成本的本质问题不是 token 太多，而是 token 用在没价值的地方**。但这不能直接削减——必须先有 ROI 验证机制，再有削减动作。

---

## 三、Orchestration-Layer 控制的 6 个旋钮

CrewAI 把成本控制分为两层：编排层（影响每一次 API 调用的形状）+ 基础设施层（叠加在上面的平台能力）。

### 3.1 Agent 循环预算与硬限

```python
agent = Agent(
    role="researcher",
    max_iter=5,           # 硬限迭代次数
    max_execution_time=120,  # 硬限时间（秒）
    max_rpm=10,           # 速率限制
)
task = Task(
    description="...",
    max_tokens=2000,      # 任务级 token 预算
)
```

**这套硬限能避免的 $40 「summarize this doc」账单**——一个看似简单的总结任务，因为工具循环失控跑出几千美元。

### 3.2 按任务复杂度路由模型

不要把同一个模型用在所有步骤。**在 CrewAI 里**：

```python
# 简单分类 / 解析 → Haiku 4.5（输入 $1/M token）
# 综合生成 → GPT-4.1 Nano（输入 $0.10/M token）
# 规划/复杂判断 → Opus 4.8（输入 $15/M token）
```

**核心思想：让模型的能力与其任务的复杂度匹配，而不是默认用最强模型**。一次循环里 80% 的步骤是分类/解析，15% 是综合，5% 是判断。

### 3.3 角色与工具的范围控制

不是所有 Agent 都需要所有工具。**工具 schema 在每次调用时都计入输入 token**——10 个工具 × 500 token schema = 5,000 token 隐性税。

```python
researcher_agent = Agent(
    role="researcher",
    tools=[search_tool, fetch_tool],  # 只给需要的工具
)
executor_agent = Agent(
    role="executor",
    tools=[code_execution_tool],
    context_isolation=True,  # 任务级 context 隔离
)
```

### 3.4 分层 vs 顺序编排的架构选择

**Hierarchical orchestration（Manager 委派给 Worker）**：避免在 Agent 之间传递完整对话历史。
**Sequential with explicit context**：只转发前一步的输出，不传完整 transcript。

**这个架构决策本身可以削减 60%+ 的 context 体积**。很多时候团队的 Agent 跑得慢、跑得贵，根因不是模型不够强，而是 context 太大、传的次数太多。

### 3.5 在 LLM 之外做确定性步骤

```python
@tool
def parse_date_range(text: str) -> dict:
    """解析日期范围。如果不是日期相关，抛错。"""
    # 用 dateutil 解析，不要调 LLM
    ...
```

**LLM 编排决策，确定性代码执行计算**。解析、验证、查询、数学运算——这些不需要语言模型。把它包装成工具，让 LLM 只决定「用哪个工具」，不要让它做「怎么算」。

### 3.6 输出结构强制

```python
from pydantic import BaseModel

class Report(BaseModel):
    title: str
    findings: list[str]
    confidence: float

task = Task(
    description="...",
    output_pydantic=Report,  # 强制结构化输出
)
```

**Output token 成本是 input 的 3-5 倍**。让模型「先思考再回答」很容易产生 500 token 的 preamble（"好的，让我分析一下..."），Pydantic schema 直接砍掉这些冗余。

---

## 四、Platform & Infrastructure 层控制

这些是与编排正交的平台能力，但同样关键：

| 能力 | 节省比例 | 关键点 |
|------|--------|--------|
| Prompt caching | 50% / hit | Anthropic 1小时 TTL，OpenAI 自动缓存 |
| Batch APIs | 50% | OpenAI/Anthropic/Gemini 都支持 |
| Semantic caching | 30-50% hit rate | GPTCache、Redis Vector |
| Self-hosting | 70-90% | 持续稳定负载用 Llama 3.3/Qwen 2.5/DeepSeek-V3 |
| Observability | 前置条件 | Galileo、Arize、Datadog LLM Observability |

**Observability 是这个清单的隐藏重点**——**你无法管理你无法度量的东西**。在你能控制成本之前，必须先看清成本在哪里。

---

## 五、正确顺序：先减浪费，再谈 ROI

CrewAI 给出的优化顺序建议（**很多团队走反了**）：

1. **先观测**：知道钱花在哪
2. **再设硬限**：先控制爆炸，再优化细节
3. **再做路由**：按复杂度分配模型
4. **再上缓存**：处理重复模式
5. **最后做自托管**：只有稳定负载才值得

**如果反着来**（先自托管、再路由、再缓存），你会发现自托管的模型依然在跑 60-80% 的低价值任务，成本结构没有本质改变。

---

## 六、反直觉结论：成本不是模型决定的

文章最后一句话值得完整引用：

> "We aren't in a model pricing problem phase per se. Per-intelligence cost is falling, the AI bill is rising because organizations are scaling, exploring, and learning."

**这不是模型太贵的问题，是运营纪律缺失的问题**。

把这句话翻译成工程动作：

- 把 token 控制嵌入到 Agent 编排层（不是事后分析）
- 把 ROI 验证嵌入到任务定义层（不是事后报告）
- 把硬限嵌入到生产配置层（不是临时调试）
- 把可观测性嵌入到平台层（不是事故后的调查）

**正确的架构可以带来 70-85% 的成本下降，质量零损失**。这不是技术极限，是工程纪律。

---

## 七、与已有内容的关联

本文与仓库内多篇文章形成互补视角：

- **《OpenSquilla Token 高效 Agent》**——从客户端路由器角度做 model selection，本文是从企业编排层做 model routing
- **《Hopping Context Windows》**——用流式计算思路做 context 压缩，本文是从任务定义层避免 context 膨胀
- **《Anthropic Effective Context Engineering》**——注意力预算管理，本文是 token 预算管理
- **《Cursor Continually Improving Agent Harness》**——关注质量提升，本文关注成本控制，两者都是「运营层」问题
- **《GitHub Scout Token Observability》**——单点 token 异常检测，本文是体系化 token 经济学

**笔者认为**：2026 下半年的 Agent 行业会从「能不能做」转向「值不值得做」，Token 经济学是这个转向的工程基础。

---

## 来源

- **原始文章**：[How to Optimize Token Spend for Better Agentic ROI](https://crewai.com/blog/how-to-optimize-token-spend-for-better-agentic-roi) — Mike Boyarski, June 2, 2026
- **作者背景**：CrewAI Enterprise 团队
- **评分**：5/5（时效性 5 / 实用性 5 / 数据密度 5 / 行业稀缺性 5 / 工程机制完整度 5）

**关键数据点**：
- 推理模型 20,000-50,000 hidden tokens
- Agent 循环 500K-2M tokens（10 步 × 30K）
- Tool schema 5,000 tokens / call
- 60-80% 企业 token 用于无业务价值用例
- 70-85% 架构化优化空间
- 10x/年单位智能成本下降
- $40「summarize this doc」失控账单
