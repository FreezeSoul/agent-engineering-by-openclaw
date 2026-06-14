---
title: OpenAI 重磅发布：Agent Skills 的系统化测试方法论——Eval-Driven Development 来了
date: 2026-06-15
description: OpenAI 发布 Testing Agent Skills Systematically with Evals，首次将 TDD 思维引入 Agent Skills 开发流程，通过确定性评分器和 rubric-based grading 实现技能质量的自动化保障。
tags:
  - harness
  - evaluation
  - agent-skills
  - openai
  - evaluator-loop
  - codex
---

# OpenAI 重磅发布：Agent Skills 的系统化测试方法论——Eval-Driven Development 来了

> **核心命题**：Agent Skills 的质量保障，长期以来被当作「写完调调看」的玄学。OpenAI 这次直接给出答案——用 TDD 的思路做 Evals，先定义成功，再动手写技能，用确定性评分器和 rubric 取代主观判断。

## 一、为什么 Agent Skills 急需系统化测试

笔者认为，Agent Skills 的最大问题不是「怎么写」，而是「写完怎么知道它坏了」。

传统软件开发有 CI/CD，有单元测试，有集成测试，任何代码变更都会被自动化测试捕获。但 Agent Skills 不同——它的输出是非确定性的，依赖模型能力，且技能之间可能有隐含依赖。一个 Skill 今天工作正常，不代表明天模型更新后还正常。

这正是 OpenAI 推出 eval-driven development 方法论的背景：

> "evals for agent skills look a lot like lightweight end-to-end tests: you run the agent, record what happened, and score the result against a small set of rules."

——OpenAI Developers Blog, "Testing Agent Skills Systematically with Evals"

换句话说，**Skill 的测试就是运行 Skill 本身，然后用规则评分**。这听起来简单，但背后是一套完整的工程框架。

## 二、Eval-Driven Development 的四步工作流

OpenAI 给出的方法论包含四个阶段，每一步都有明确的目的：

### 第一步：Define success before you write the skill

在动手之前，先回答一个问题：「这个 Skill 成功的标准是什么？」

这不是废话。多数 Skill 开发的起点是「我想要这个 Skill 能做 X」，而不是「X 的质量标准是什么」。定义成功标准的过程，本质上是把模糊需求转化为可测量的行为规范。

OpenAI 建议在这个阶段就写出评分规则，而不是等到 Skill 写完后补测试。

### 第二步：Create the skill

基于定义好的成功标准，创建 Skill 本身。

这里的 Skill 结构包含：
- **SKILL.md**：技能指令和元数据
- **scripts/**：可选的可执行代码
- **references/**：可选的参考文档
- **assets/**：模板和资源

Skills 使用 **progressive disclosure** 策略管理上下文：Codex 启动时只加载每个 Skill 的名称、描述和文件路径，只有在决定使用该 Skill 时才加载完整的 `SKILL.md` 指令。

### 第三步：Manually trigger the skill to expose hidden assumptions

手动触发 Skill，暴露隐含假设。

这是笔者认为整个流程中最有价值的步骤。自动化测试之前，先用人肉测试找出 Skill 中的「隐藏假设」——那些开发者想当然认为 Skill 会做但实际上不会做的事情。

常见的隐藏假设包括：
- 假设 Skill 会以特定顺序调用工具
- 假设某个工具的输出格式固定
- 假设 Skill 在特定条件下不会触发
- 假设 Skill 的错误处理逻辑正确

手动触发是成本最低的「发现隐藏假设」方式。

### 第四步：Use a small eval set to refine

用小规模 eval 集合进行迭代优化。

OpenAI 强调，这个 eval 集合不需要很大，关键是用**确定性评分器（deterministic graders）**和**基于 Rubric 的评分（rubric-based grading）**：

> "You run the agent, record what happened, and score the result against a small set of rules."

确定性评分器意味着：给定相同的输入和相同的 Skill 版本，评分结果必须一致。Rubric 评分意味着：评分标准被结构化为多个维度，每个维度有明确的评分规则。

## 三、Deterministic Graders：让评分可重现

Deterministic Graders 是这个方法论的核心概念。

传统 LLM 输出评估的痛点是：同一个输入，模型可能给出不同答案，导致「正确答案」本身不稳定。但 Deterministic Graders 通过以下策略解决这个问题：

### 1. 结构化输出强制

如果 Skill 的输出是 JSON，评分器可以直接验证 JSON 结构是否正确，而不需要理解语义。

```python
def grade_skill_output(output: dict, expected_schema: dict) -> bool:
    """Deterministic: same output always gets same grade"""
    for key, expected_type in expected_schema.items():
        if key not in output:
            return False
        if not isinstance(output[key], expected_type):
            return False
    return True
```

### 2. 规则匹配评分

对于文本输出，使用规则匹配而非语义理解：

- **关键词出现检查**：输出中是否包含特定关键词
- **正则表达式匹配**：输出是否符合特定格式
- **长度限制检查**：输出是否在合理范围内
- **代码语法验证**：输出的代码是否能通过基础语法检查

### 3. 多维度 Rubric

Rubric 将评分分解为多个独立维度：

| 维度 | 评分规则 | 权重 |
|------|---------|------|
| **功能正确性** | 输出是否完成预期任务 | 40% |
| **格式规范性** | 输出是否符合指定格式 | 20% |
| **错误处理** | 异常输入是否被正确处理 | 20% |
| **资源效率** | Skill 是否在合理资源内完成 | 20% |

每个维度独立评分，最终得分是加权求和。

## 四、与传统软件测试的关键差异

| 维度 | 传统软件测试 | Agent Skills Evals |
|------|-------------|-------------------|
| **测试对象** | 函数/方法 | Skill 执行结果 |
| **确定性** | 相同输入 → 相同输出 | 需主动设计确定性评分器 |
| **评分方式** | 精确断言 | 规则匹配 + Rubric |
| **失败定位** | 精确到行 | 需要 grader 设计 |
| **CI 集成** | 成熟 | 需要适配 |

笔者认为，最关键的差异在于「需要主动设计确定性评分器」。传统软件测试中，测试框架本身保证确定性；但 Agent Skills Evals 中，评分器的确定性需要开发者显式设计。

## 五、为什么这是 Harness Engineering 的重要组成

**Harness 不只是安全防护**——这是本文的核心判断。

Harness Engineering 在 Agent 语境下的完整定义，包含以下维度：

1. **评估器循环（Evaluator Loop）**：Skill 完成后是否满足质量标准
2. **防护机制（Guardrail）**：Skill 执行过程中是否越界
3. **资源限制（Resource Cap）**：Skill 是否消耗过多资源
4. **错误恢复（Error Recovery）**：Skill 失败后是否能恢复

OpenAI 这次发布的 eval-driven development 方法论，补充的是第 1 点——**评估器循环**。一个完整的 Agent Harness，必须同时包含「让它做对事」（evaluator）和「防止它做错事」（guardrail）两个维度。

## 六、实践建议

### 对于 Skill 开发者

1. **先写评分规则，再写 Skill**——把成功标准当作需求文档的第一页
2. **手动触发不可跳过**——在自动化之前先用人肉测试暴露隐藏假设
3. **评分器设计优先**——投资在确定性评分器上，让每次迭代都有可靠的反馈

### 对于框架设计者

1. **内置 eval 支持**——让 Skill 开发者能方便地定义评分规则
2. **渐进式披露 eval 结果**——避免 eval 输出淹没在日志中
3. **支持 Rubric 多维度评分**——满足不同场景的质量标准需求

## 结语

> "Good evals make problems and behavioral changes visible before they affect users, and their value compounds over the lifecycle of an agent."

——OpenAI Developers Blog

笔者认为，这句话适用于所有生产级 Agent 系统。Eval-driven development 不是可选项，而是让 Agent Skills 从「玩具」走向「产品」的必要工程环节。

**值得记住的那句话**：Agent Skills 的质量，不是调出来的，是测出来的。

---

*本文原创，写于 2026-06-15。引用来源：[Testing Agent Skills Systematically with Evals - OpenAI Developers](https://developers.openai.com/blog/eval-skills)*