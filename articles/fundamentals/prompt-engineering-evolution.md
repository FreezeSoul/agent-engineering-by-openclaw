# Prompt Engineering 演进：从提示词到工程化约束

> **本质**：Prompt Engineering 是 AI Agent 能力的起点，也是最深层的杠杆。提示决定了 Agent 的上限——同样的模型，提示不同，表现可能相差数倍。

---

## 一、Prompt Engineering 的地位

在 AI Agent 开发中，Prompt Engineering 是所有上层能力的基础：

```
Prompt Engineering（地基）
         ↓
   Tool Use / MCP（工具）
         ↓
   Memory / Context（记忆）
         ↓
   Agent Orchestration（编排）
         ↓
   Deep Agent / Multi-Agent（上层建筑）
```

好的 Prompt Engineering 可以推迟对更强大模型的需求；差的提示即使在最强模型上也会失败。

---

## 二、演进阶段

### Stage 1：基础提示（Basic Prompting）

**零样本提示（Zero-shot）**：直接给出任务描述。

```
"翻译以下文本为法语：Hello world"
```

**少样本提示（Few-shot / In-context Learning）**：在提示中提供少量示例。

```
"中译英：
苹果 -> Apple
香蕉 -> Banana
橙子 -> Orange
你好 -> ?"
```

**核心局限**：
- 无法处理复杂推理
- 示例数量受限于上下文窗口
- 无法表达思维过程

---

### Stage 2：Chain of Thought（CoT）

**Chain of Thought**（CoT，思维链，Google 2022）：通过在提示中加入"思考步骤"，让模型展示推理过程。

标准 CoT：
```
问题：小明有5个苹果，小红给了他3个，小明吃掉了2个。小明现在有多少个苹果？
思考：让我们一步步来。
Step 1: 小明开始有5个苹果。
Step 2: 小红给了他3个，所以 5 + 3 = 8 个。
Step 3: 小明吃掉了2个，所以 8 - 2 = 6 个。
答案：6个。
```

**Self-Consistency**（自洽性，Google 2023）：生成多个推理路径，选择最一致的答案。

**Tree of Thought**（ToT，思维树，Yao et al. 2023）：在树结构中探索多个推理分支，而非线性 chain。

**Image of Thought**（IoT，视觉思维链，arxiv:2405.13872）：将 CoT 扩展到多模态，让 MLLM 从图像中提取视觉推理步骤。

---

### Stage 3：Prompt as Code（提示工程化）

将提示视为代码，进行版本控制、测试和模块化。

**Prompt 模板化**：
```python
TEMPLATE = """
你是一个{role}，负责{task}。
背景信息：
{context}

任务：{instruction}

输出格式：
{output_format}
"""
```

**Prompt 链（Prompt Chaining）**：将复杂任务分解为多个 Prompt 串联执行。

```python
result1 = llm(prompt1)  # 提取关键信息
result2 = llm(prompt2.format(context=result1))  # 生成分析
result3 = llm(prompt3.format(context=result1+result2))  # 整合输出
```

**Prompt 版本控制**：像代码一样管理 Prompt 的演进，记录每次变更的效果。

**Prompt 测试**：构建测试用例集，验证 Prompt 在各种边界情况下的表现。

---

### Stage 4：Context Engineering（上下文工程）

> 详见：[Context Engineering for Agents](articles/concepts/context-engineering-for-agents.md)

Context Engineering 是 Prompt Engineering 的下一阶段——从优化单个提示词，到优化整个上下文的管理策略。

核心区别：
- **Prompt Engineering**：优化提示词本身
- **Context Engineering**：优化上下文的组成、结构和维护策略

---

### Stage 5：Constitutional AI 与约束驱动

**Constitutional AI**（Anthropic）：通过一组原则（Constitution）指导 AI 行为，而非详细的指令。

```python
CONSTITUTION = [
    "The assistant should be helpful but not harmful.",
    "The assistant should be honest about its limitations.",
    "The assistant should respect user privacy.",
]
```

**Harness Engineering**（Martin Fowler）：通过工具 + 规则 + 定期清理的三层约束来控制 Agent 行为。

> 详见：[Harness Engineering: Martin Fowler](articles/community/harness-engineering-martin-fowler.md)

---

## 三、Agent 场景下的 Prompt 设计模式

基于 [Anthropic 官方 Agent 设计模式](articles/research/anthropic-building-effective-agents.md) 和 [7 Agentic Design Patterns](articles/community/7-agentic-design-patterns-mlmastery.md)：

| 模式 | 核心思想 | 适用场景 |
|------|---------|---------|
| **ReAct** | Reasoning 和 Acting 交替，先推理再行动 | 需要工具调用的复杂任务 |
| **Reflection** | 让 Agent 自我审视输出，提升质量 | 需要高质量输出的任务 |
| **Planning** | 任务开始前制定行动计划 | 多步骤复杂任务 |
| **Self-Critique** | Agent 评估自身决策，发现错误 | 高风险决策任务 |
| **Tool Use** | 明确 Agent 可调用的工具及触发条件 | 需要外部交互的任务 |
| **Memory-Augmented** | 在提示中嵌入长期记忆 | 跨会话一致性任务 |

---

## 四、Prompt Engineering 的工程实践

### 4.1 提示词管理

**提示词版本控制**：
```bash
prompts/
├── v1.0_basic.yaml      # 初始版本
├── v1.1_with_examples.yaml  # 增加 few-shot
├── v2.0_with_cot.yaml   # 引入 CoT
└── v3.0_structured.yaml # 结构化输出
```

**提示词测试框架**：
```python
def test_prompt(prompt, test_cases):
    results = []
    for case in test_cases:
        output = llm(prompt.format(**case.input))
        results.append({
            "input": case.input,
            "expected": case.expected,
            "actual": output,
            "passed": evaluate(output, case.expected)
        })
    return results
```

### 4.2 常见反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| **过于模糊** | "做好这个任务" | 明确输出格式和评估标准 |
| **太长太复杂** | 一次性给所有背景 | 分阶段，逐步注入上下文 |
| **缺乏边界** | Agent 自由度过高 | 明确不允许做的行为 |
| **指令冲突** | 多个指令相互矛盾 | 优先级排序，明确主目标 |
| **忽视错误处理** | 没有预设异常处理 | 设计 fallback 策略 |

### 4.3 上下文窗口管理与提示优化

详见：[Context Window Overflow: Redis](articles/community/context-window-overflow-redis.md)

核心策略：
- **智能分块**：将长上下文分解为语义独立的块
- **语义缓存**：复用相似查询的中间结果
- **历史摘要**：定期压缩对话历史

---

## 五、演进全景图

```
2017-2020: 基础NLP
     ↓
2020-2022: Zero-shot / Few-shot Learning（GPT-3）
     ↓
2022: Chain of Thought（Google）
     ↓
2023: Tree of Thought / Self-Consistency
     ↓
2023-2024: ReAct / Tool Use / Agentic Patterns
     ↓
2024: Context Engineering（Prompt as Code）
     ↓
2025: Constitutional AI / Harness Engineering
     ↓
2026: Hybrid Architectures（CoT + Memory + Tool + Multi-Agent）
```

---

## 六、关键资源

- 原始 CoT 论文：Wei et al. (2022) - Chain of Thought
- ToT 论文：Yao et al. (2023) - Tree of Thoughts
- IoT 论文：arxiv:2405.13872 - Image of Thought
- Constitutional AI：Anthropic (2022)
- Anthropic Agent Design：见 [Building Effective AI Agents](articles/research/anthropic-building-effective-agents.md)
- 7 Design Patterns：见 [7 Agentic Design Patterns](articles/community/7-agentic-design-patterns-mlmastery.md)
