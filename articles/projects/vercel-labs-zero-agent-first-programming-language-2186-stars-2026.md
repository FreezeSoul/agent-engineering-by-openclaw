# Vercel Labs Zero：一个 Agent-First 编程语言的工程实验

## 它解决了一个什么问题

编程语言的演进历史有一个清晰的脉络：**从机器原生到人类可读**。Fortran 是给机器写的，Python 是给人写的。那么下一个问题顺理成章：**如果"人"是一个 AI Agent，语言应该长什么样？

Vercel Labs 的 Zero 给出了他们的实验性答案。

Zero 是一个"Agent-first 编程语言"——不是"支持 Agent 编程的语言"，而是**从设计第一天就把 Agent 作为主要用户**的语言。这不是营销话术，是有具体工程决策支撑的。

---

## 为什么这值得关注

### 1. 可学习性：Agent 能从错误信息中学习

传统的编译器错误是给人看的——"Expected ';' at line 23"。这对 Agent 来说是低效的——它需要从错误恢复到正确的 token 序列，而不是理解人的思维模型。

Zero 的工具链暴露的是**结构化事实**（structured facts）：诊断信息、graph facts、size reports、explanations 和 fix plans 都是机器可读的格式。Agent 可以直接解析、执行、修复，而不需要在错误信息和代码之间做一层翻译。

Cursor 团队在 Composer 2.5 中用 textual feedback 解决 RL 的 credit assignment 问题；Zero 在语言层面做了类似的解法——**把"人类直觉"替换为"机器可操作的结构"**。

### 2. 标准库的深度覆盖

> "common capabilities should live in documented, coherent library APIs instead of scattered dependency stacks"

这是 Zero 的核心设计原则之一。传统的编程体验是：先找库，找到了发现版本冲突，冲突解决了发现 API 不一致。Zero 通过内置标准库解决这个问题——大多数常见能力直接在语言中可用，不需要外部依赖搜索。

**对 Agent 来说，这意味着一个巨大的效率提升**：一个工具调用就能列出所有可用能力，不需要在 npm/pypi/crates.io 之间跳转，不需要处理版本冲突。

### 3. 确定性的工具链

```bash
zero check examples/hello.0
zero run examples/add.0
zero build --emit exe --target linux-musl-x64 examples/add.0 --out .zero/out/add
zero graph --json examples/systems-package
zero size --json examples/point.0
zero routes --json examples/web/hello
```

所有命令都有 `--json` 输出选项。这不是便利功能，是核心设计：**诊断、修复、构建——一切都应该是可脚本化的**。

---

## 关键引用

> "Zero is an experiment in building an agent-first programming language. The project is exploring what changes when agents are primary users from day one."

来源：[GitHub README - vercel-labs/zero](https://github.com/vercel-labs/zero)

> "Deterministic tooling: diagnostics, graph facts, size reports, explanations, and fix plans should be structured enough for agents to inspect and act on."

来源：[GitHub README - vercel-labs/zero](https://github.com/vercel-labs/zero)

> "Security vulnerabilities should be expected. Zero is not ready for production systems, sensitive data, or trusted infrastructure."

来源：[GitHub README - vercel-labs/zero](https://github.com/vercel-labs/zero)

---

## 笔者的判断

Zero 处于 pre-1 状态，API 随时可能 breaking change，拿它跑生产系统是自寻死路。但它的实验方向是对的。

**真正有意思的是它提出的问题**：当 Agent 成为主要编程主体时，语言需要改变什么？

传统语言设计的假设是**人类是编程主体**——错误信息要友好，语法要简洁，库要丰富。但这些优化目标对于 Agent 来说可能都不是最重要的。Agent 需要的是：**结构化的、可解析的、可预测的**。

Zero 给出了一个具体的答案：JSON 输出、标准库内聚、结构化错误。虽然还很 early，但它是目前最认真思考"Agent 作为语言用户"的项目之一。

**与 Cursor Composer 2.5 的关联**：Composer 2.5 在解决"如何训练 Agent 去做长程任务"，Zero 在探索"Agent 执行任务时，编程语言应该长什么样"。从训练到执行，是一个完整的闭环。

---

*收录时间：2026-05-19 | 项目 Stars: 2,186 | 关联 Article: Cursor Composer 2.5 深度解析*