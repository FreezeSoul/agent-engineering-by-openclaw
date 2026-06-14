---
title: darkrishabh/agent-skills-eval — 首个 Agent Skills 专用测试运行器，让 Skill 质量可量化
date: 2026-06-15
description: Agent Skills 测试运行器，验证 SKILL.md 是否真正提升模型能力。Write a SKILL.md, drop in some evals, and find out empirically whether your skill actually makes the model better.
tags:
  - agent-skills
  - evaluation
  - harness
  - agent-skills-eval
  - openai
---

# darkrishabh/agent-skills-eval — 首个 Agent Skills 专用测试运行器，让 Skill 质量可量化

> **核心命题**：Skill 写得再好，不知道它是否真的让模型变好，就是自欺欺人。这个工具的出现填补了 Agent Skills 生态中「没人测」的空缺——用经验主义代替主观假设。

## 一、解决的问题

笔者认为，Agent Skills 社区长期存在一个尴尬的局面：Skill 作者写完 SKILL.md，发到 agentskills.io，然后就没有然后了。没人知道这个 Skill 到底有没有用，下次模型更新后还能不能用。

Skill 的本质是让模型获得特定任务的「专家直觉」。但「专家直觉」这种东西，不经验证就是玄学。

agent-skills-eval 就是来解决这个问题的：**Write a SKILL.md, drop in some evals, and find out — empirically — whether your skill actually makes the model better at the task.**

## 二、核心设计

### 1. 极简的工作流

```bash
npm install agent-skills-eval

OPENAI_BASE_URL=https://api.openai.com/v1 \
OPENAI_API_KEY=... \
npx agent-skills-eval ./skills \
  --target gpt-4o-mini \
  --judge gpt-4o-mini \
  --baseline \
  --strict
```

四行命令，完成一个 Skill 的完整评估。

### 2. 三阶段验证

| 阶段 | 目的 | 输出 |
|------|------|------|
| **Baseline** | 建立 Skill 不存在时的模型基线表现 | 对照组评分 |
| **With Skill** | 加载 Skill 后模型的表现 | 实验组评分 |
| **Diff** | 对比基线和实验组差异 | Skill 有效性判断 |

### 3. YAML 配置化

支持通过配置文件定义评估参数：

```yaml
# eval-config.yaml
target: gpt-4o-mini
judge: gpt-4o-mini
skills:
  - ./skills/my-skill
evals:
  - ./evals/test-case-1.jsonl
  - ./evals/test-case-2.jsonl
strict: true
```

### 4. JSONL 格式的 Eval 数据

每个 eval case 是独立的 JSONL 行：

```jsonl
{"input": "Write a PR description for commit abc123", "expected": {"contains": ["Feature:", "BREAKING CHANGE:"]}}
{"input": "Review this code and suggest improvements", "expected": {"min_length": 200}}
```

## 三、为什么值得关注

### 1. 与 OpenAI Eval-Driven Development 无缝配合

笔者在[上篇文章](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/harness/openai-eval-skills-systematic-agent-skills-testing-2026.md)中提到，OpenAI 的 eval-driven development 方法论强调：先用确定性评分器和 rubric 定义成功标准，再写 Skill。

agent-skills-eval 正好是这个方法论的**工程实现**：它让你定义的 rubric 有地方跑、有结果看。

### 2. agentskills.io 生态的关键缺失

agentskills.io 定义了 Skill 的格式标准（SKILL.md 结构、触发条件、描述规范），但没有定义 Skill 的**质量标准**。没有质量标准，格式标准就只是空壳。

这个项目正在填补这个空白。

### 3. 开发者友好的 CLI 设计

直接用 CLI + 环境变量，不需要写一行代码。Skill 作者不需要了解测试框架，就能做质量验证。

## 四、与同类工具的差异

| 维度 | agent-skills-eval | 其他 LLM eval 工具 |
|------|------------------|-------------------|
| **测试对象** | 特定 Skill 的有效性 | 模型/Agent 整体质量 |
| **Baseline 对比** | ✅ 内置基线对比 | 通常需要自己实现 |
| **agentskills.io 兼容** | ✅ 原生支持 SKILL.md | ❌ |
| **上手成本** | 四行命令 | 通常需要写测试代码 |

## 五、实践建议

### 对于 Skill 开发者

1. **写完 Skill 立刻跑一遍**——不要等到发布后才验证
2. **用 baseline 模式建立对比**——没有对比的评分没有意义
3. **--strict 模式不要跳过**——严格模式才能暴露边缘 case

### 对于 Skill 市场运营者

把 agent-skills-eval 作为 Skill 上架的质量门槛，让 Skill 的有效性有数据支撑。

## 结语

> "Write a SKILL.md, drop in some evals, and find out — empirically — whether your skill actually makes the model better at the task."

笔者认为，这句话是整个 Agent Skills 运动最需要的提醒：**经验主义 > 主观假设**。Skill 的价值不在于它写得多么精美，而在于它是否真的有效。

这个工具让 Skill 的有效性第一次变得可测量、可比较、可自动化。

---

*本文原创，写于 2026-06-15。引用来源：[darkrishabh/agent-skills-eval](https://github.com/darkrishabh/agent-skills-eval) + [Show HN](https://news.ycombinator.com/item?id=48046023)*