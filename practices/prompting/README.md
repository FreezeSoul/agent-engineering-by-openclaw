# Prompt 模板与技巧

> 好的 Prompt 是 Agent 效果的基石。本目录收录可直接复用的模板和技巧。

---

## 目录

### 1. Agent System Prompt 模板

> 给 Agent 设定角色、目标和约束

```markdown
# Role: {role_name}
# Goal: {specific_goal}
# Backstory: {background_and_context}

## 核心能力
- 能力 1
- 能力 2

## 行为约束
- 不做 X
- 始终做 Y

## 输出格式
{expected_output_format}
```

### 2. Tool Use Prompt

> 让 LLM 学会调用工具

```markdown
你可以通过以下工具完成任务：

{tool_1_name}: {tool_1_description}
{tool_2_name}: {tool_2_description}

使用规则：
- 先理解用户问题，判断是否需要工具
- 如果需要，选择最合适的工具
- 调用工具后，基于结果回答用户
```

### 3. ReAct Prompt 模板

> 让模型交替思考和行动

```markdown
针对问题：{user_question}

请按以下格式回答：

Thought: {你的思考过程}
Action: {工具名称}("参数")
Observation: {工具返回结果}

... (重复直到完成任务)

Final Answer: {最终回答}
```

### 4. few-shot 示例模板

```markdown
示例：

输入: {example_input_1}
输出: {example_output_1}

输入: {example_input_2}
输出: {example_output_2}

现在回答：
输入: {actual_input}
输出:
```

---

## 技巧汇总

| 技巧 | 说明 | 适用场景 |
|------|------|---------|
| **角色设定** | "你是一个 X 专家" | 需要特定领域知识 |
| **输出格式约束** | "请用 JSON 格式返回" | 结构化输出 |
| **Chain of Thought** | "请分步骤思考" | 复杂推理任务 |
| **few-shot** | 提供示例 | 任务不明确时 |
| **安全边界** | "如果不确定，请说不知道" | 避免幻觉 |

---

## 避坑指南

1. **不要过度约束**：Prompt 太长会让模型忽略关键指令
2. **不要模糊**：每个指令应该明确可执行
3. **及时更新**：模型行为会随版本变化，Prompt 需要适配

---

*持续更新中，欢迎提交 PR*
