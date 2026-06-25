# DietrichGebert/ponytail：让 AI Agent 像「最懒的老手」一样写代码

> 57,000+ GitHub Stars | 9天破5万 | Skill for Claude Code / Codex / Copilot

## 核心命题

大多数 AI Coding Agent 有一个根深蒂固的「过度建设」问题：你只想要一个日期选择器，它给你安装一个 npm 包、加 wrapper component、再加一堆样式讨论。**ponytail 的解决思路异常简单**：在写代码之前，先问七层问题，只有前面六层都不适用时才动手写。

这不是一个提示词，这是一个**决策树**——让 Agent 在动手前先想清楚「这真的需要写吗」。

## 为什么值得关注

### 数字说话

在真实 Claude Code session 对真实开源项目（FastAPI + React）的盲测中（12 个功能任务，Haiku 4.5，n=4）：

| 指标 | ponytail | caveman | "YAGNI+one-liners" prompt |
|------|----------|---------|--------------------------|
| 代码行数 | **-54%** | -20% | -33% |
| Token 消耗 | **-22%** | +7% | -14% |
| 成本 | **-20%** | +3% | -21% |
| 执行速度 | **-27%** | +2% | -30% |
| **安全性** | **100%** | 100% | 95% |

ponytail 是唯一在**所有指标同时下降**的同时保持 100% 安全的方案。「写一行」提示词能减少代码，但会牺牲安全边界。

### 设计决策：七层决策树

ponytail 在写代码前强制 Agent 爬这个梯子：

```
1. 这真的需要存在吗？      → 不需要：跳过
2. 代码库里已有吗？        → 已存在：复用，不要重写
3. 标准库能实现吗？        → 标准库：用它
4. 平台原生功能能实现吗？   → 原生：用它（<input type="date">）
5. 已安装的依赖能实现吗？   → 依赖：用它
6. 一行代码能搞定吗？      → 一行搞定
7. 只有以上都不行时：      → 写最小可工作的代码
```

关键：**这个梯子在理解问题之后才运行**，不是不写代码就跳过。它会先读完相关代码、追踪真实调用链，确认前面六层都不适用才动手。

### 与同类方案的差异化

| 方案 | 思路 | 效果 | 安全性 |
|------|------|------|--------|
| **ponytail** | 决策树式 YAGNI | 代码↓54%，安全不变 | 100% |
| **caveman** | 强制简洁散文风格 | 代码↓20%，token 反升 | 100% |
| **"YAGNI+one-liners" prompt** | 直接要少写代码 | 代码↓33%，安全下降 | 95%（丢失边界验证）|

caveman 的问题在于它通过压缩思考过程来减少输出，结果 token 反而上升——因为模型要在受限的思考空间里反复试探。ponytail 通过结构化决策树让模型**主动跳过**，而不是被动压缩。

## 工程机制视角

笔者认为，ponytail 的真正贡献不是「让代码变少」，而是**把一个隐性的专家判断过程显式化了**。

资深工程师看到「日期选择器」需求时的第一反应不是「用哪个库」，而是「这真的需要写吗，浏览器原生的 `<input type="date">` 行不行」。这个判断在人类专家的大脑中是毫秒级完成的，但 AI Agent 缺的就是这个——它的默认模式是「响应需求」，不是「质疑需求」。

ponytail 把这个判断过程编码成了七层决策树，本质上是一个**轻量级的需求过滤器**，而不是代码压缩工具。

## 安装方式

```bash
# Claude Code
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail

# Codex
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail

# GitHub Copilot CLI
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

桌面应用通过 UI 安装：Customize → Personal plugins → Add from repository。

## 适用场景

✅ **代码库已经有一定规模，Agent 倾向于重复造轮子**  
✅ **成本/Token 预算敏感的团队**  
✅ **希望 Agent 写出「老手风格」代码（少但够用）**

❌ **原型快速验证阶段**（这个阶段需要 Agent 快速出代码）  
❌ **需要 Agent 进行创造性架构设计**（YAGNI 梯子会阻止探索性代码）  

## 引用

> "The best code is the code you never wrote."

— DietrichGebert，ponytail README

> "ponytail keeps every safety guard while a bare 'write one-liners' prompt drops one."

— ponytail benchmark results，2026-06-18

---

**关联阅读**：想深入理解 AI Coding Agent 的「过度建设」问题，推荐配合阅读 [AddyOsmani Long-running Agents](https://addyosmani.com/blog/long-running-agents/) 中的 Harness 工程框架，理解为什么让 Agent 自主工作时这个问题会被放大。