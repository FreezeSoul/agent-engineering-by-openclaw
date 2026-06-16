# Impeccable：给 AI Coding Agent 一个设计师的词汇表

> **来源**：https://github.com/pbakaus/impeccable | 38K ⭐ | JavaScript
>
> 一个解决 AI 生成前端「一眼 AI 味」问题的设计引导技能。

---

## 核心命题

AI coding agent 生成的前端代码有个致命问题：**大家看起来都一样**。同一个模型、同样的默认样式、同样的组件堆砌，最后出来的 UI 像是一个妈生的。

这不是模型的 bug，是设计的缺失。模型没有「设计师词汇」，所以它只能用它最熟悉的那套表达方式。

Impeccable 给 agent 一个这样的词汇表。

---

## 为什么这个项目值得推荐

### 1. 解决了 AI 前端生成的「品味天花板」问题

当一个 coding agent 说「给我做一个好看的按钮」，它其实不知道什么是「好看」。它只知道最常见的实现。

Impeccable 的解法：
- `/impeccable init` 生成 `PRODUCT.md` 和 `DESIGN.md`，定义产品受众、品牌调性
- 后续的 `/impeccable` 命令都基于这两个文件做上下文
- agent 不再靠猜，而是靠「设计语言规范」做决策

**笔者认为**：这比任何 prompt 技巧都有效。因为它把设计决策从「模糊偏好」变成了「明确约束」。

### 2. 41 个确定性检测规则

这是最硬的部分。

不是「AI 觉得这个按钮丑不丑」，而是「这个元素的对比度是否符合 WCAG」「这个动画时长是否在合理范围内」「这个色彩组合是否在品牌调性内」。

41 个规则覆盖：
- 排版（type scale, line height, letter spacing）
- 色彩（对比度、配色方案、品牌色板）
- 动效（时长、缓动曲线、是否应该动画）
- 布局（间距系统、响应式断点）

**确定性**是关键。规则不会因为模型心情好坏而变化。

### 3. Live browser iteration

大多数设计工具是「生成一次，然后靠人眼检查」。

Impeccable 的 `/impeccable feedback` 命令让 agent 在浏览器中实时看到自己的设计决策结果，并基于视觉反馈进行调整。

这不是传统的「截图对比」，是让 agent 真正在浏览器渲染上下文中评估设计。

---

## 技术原理

```
用户项目目录
├── PRODUCT.md        # 产品定位：受众、核心价值
├── DESIGN.md        # 设计语言：色彩、字体、间距、动效规范
└── src/             # 业务代码
    └── components/
        └── Button.tsx  ← agent 生成时读取 DESIGN.md
```

Agent 生成组件时：
1. 读取 DESIGN.md 中的设计规范
2. 生成符合规范的代码
3. `/impeccable check` 运行 41 个检测规则
4. 规则通过 → 合并；规则失败 → agent 根据错误信息修正

这个流程把「设计审查」从人工节点变成了自动检查。

---

## 竞品对比

| 方案 | 实现方式 | 优点 | 缺点 |
|------|---------|------|------|
| **纯 Prompt** | 在 system prompt 里加设计要求 | 简单 | 不可靠，模型理解不稳定 |
| **UI Component Library** | 限制 agent 只能用指定组件 | 一致性好 | 灵活性差，组件外需求无法满足 |
| **Impeccable** | 规则引擎 + 设计语言上下文 | 可靠 + 灵活 | 需要初始化设计文档 |

**笔者认为**：Impeccable 的定位介于「完全放开」和「严格限制」之间。它不限制 agent 用什么组件，但要求生成的组件必须符合设计语言规范。这是当前最优解。

---

## 适用场景

**适合**：
- 有明确设计规范的 B端产品
- 需要 AI coding agent 参与前端迭代的团队
- 希望 AI 生成代码能通过设计师验收的项目

**不适合**：
- 探索性原型阶段（设计规范还没定）
- 完全没有设计规范的项目（Impeccable 需要 DESIGN.md 作为输入）
- 追求极致自定义的纯设计驱动项目

---

## 上手方式

```bash
# 1. 安装
npm install -g @impeccable/core

# 2. 初始化设计语言
/impeccable init

# 3. 检查设计规范
/impeccable check

# 4. 获取设计反馈
/impeccable feedback
```

---

## 引用

> "Design guidance for AI coding agents. 1 skill, 23 commands, live browser iteration, and 41 deterministic detector rules for AI-generated frontend design."

— [impeccable README](https://github.com/pbakaus/impeccable)

> "A skill can't make the model a better designer. But it can give it the vocabulary to ask better questions."

— [impeccable.style](https://impeccable.style/)

---

## 关联文章

本文与 [Anthropic LLM ATT&CK Navigator 研究](../articles/deep-dives/anthropic-red-team-llm-attck-navigator-2026.md) 共同关注 **AI Agent 的风险评估与质量控制**。两个项目从不同角度解决同一个问题：如何让 AI agent 的输出从「不可控」变为「可信赖」。

- LLM ATT&CK Navigator：从安全角度评估 AI 滥用风险
- Impeccable：从设计质量角度评估 AI 生成结果

两者都指向一个结论：**Agent 的能力上限由 harness 的完善程度决定，而非模型本身。**