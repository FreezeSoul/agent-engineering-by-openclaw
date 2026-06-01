# langchain-ai/deepagents：自带解释器的生产级 Agent Harness

> 官方仓库：https://github.com/langchain-ai/deepagents
> Stars：23,623（2026-06-01）
> 许可证：MIT

---

## 核心命题

LangChain 推出的 deepagents 解决了一个长期困惑社区的问题：**当 Agent 需要执行确定性工作流时，解释器代码比 Prompt 指令更可靠**。这不是一个玩具项目，而是一个包含了完整 Interpreter 运行时、Skill 系统和子 Agent 编排的生产级 Harness。

---

## 什么是 deepagents

deepagents 是 LangChain 推出的「自带电池」的 Agent Harness 框架。它不是一个 LangGraph 的替代品，而是构建在 LangGraph 之上的更高级抽象：

> 引用自 README：
> "The batteries-included agent harness."

核心设计理念是：让 Agent 在一个**嵌入式 TypeScript 运行时**（Interpreter）中编写和执行代码，而不是每次都通过自然语言描述操作。这意味着：

- 多步骤的数据转换可以用 TypeScript 代码直接表达，而非 Prompt 描述
- 值在多次交互中持久化（数组保持数组，对象保持对象）
- Helper 函数可以跨 turn 复用，不需要每次重新定义

---

## Interpreter：让代码而非 Prompt 驱动确定性逻辑

deepagents 的核心创新是 **Interpreter**——一个嵌入 Harness 的 TypeScript 运行时。

### 为什么需要解释器？

当一个 Agent 被要求做同一件事多次时，它可能每次想出不同的实现方式。对于需要「用我们知道有效的方法」的确定性任务，这不是优点而是缺陷。

Interpreter 给 Agent 一个直接表达意图的地方：写 TypeScript 代码。代码执行比模型输出的自然语言更可预测、更易测试、更容易进行边界检查。

### Interpreter 与 Sandbox 的区别

| 维度 | Interpreter（解释器） | Sandbox（沙箱）|
|------|---------------------|----------------|
| 代码来源 | Agent 编写 + Interpreter 执行 | 第三方提供或预编译 |
| 访问控制 | 默认受限，需显式暴露文件/网络/工具 | 隔离但通常权限较宽 |
| 适用场景 | Agent 驱动的确定性工作流 | 执行不可信代码 |
| 访问边界 | Harness 控制的 allowlist | 进程级隔离 |

引用自 LangChain 官方博客：

> "Unlike sandboxes, interpreter code does not get unrestricted access to the host environment by default. Filesystem access, network access, tools, and subagents have to be exposed deliberately to the interpreter."

---

## Interpreter Skills：Skill 的代码化

deepagents 支持一种特殊类型的 Skill——**Interpreter Skill**，它将 Skill 从 Prompt 扩展变成可执行代码模块。

### 基本结构

每个 Interpreter Skill 包含两部分：

**SKILL.md**（行为描述）—— 告诉模型什么时候该调用这个技能、传什么参数、如何使用输出

**index.ts**（代码模块）—— 包含确定性逻辑，模型通过 `import()` 调用

### 示例：GitHub Repo Triage

模型不需要记住 triange 的完整流程，只需要知道：

```typescript
// 模型调用
const { triage } = await import("@/skills/github-triage");

const result = await triage("langchain-ai/deepagents", {
  issues: true,
  prs: true,
  discussions: true,
});
```

当调用时，workflow 自动：
1. 从 GitHub 获取所有 open items
2. 为每个 item 生成子 Agent
3. 子 Agent 生成处理建议
4. 结果汇总返回

模型负责「什么时候用 + 传什么参数」，**实际执行逻辑在代码中定义**。

---

## 与 LangGraph 的关系

deepagents 不是重新发明轮子，它构建在 LangGraph 之上：

```
LangGraph（底层编排）→ deepagents（高层 Harness）→ 你的 Agent 代码
```

LangGraph 提供状态机、节点、边的抽象；deepagents 在这个基础上添加了：
- 嵌入式 Interpreter 运行时
- Skill 系统（支持渐进式披露）
- 子 Agent 生命周期管理
- 可观测性集成

如果你只需要低层次的控制，用 LangGraph；如果需要开箱即用的 Agent 工作流框架，deepagents 更适合。

---

## 关键能力一览

| 能力 | 说明 |
|------|------|
| **Interpreter 运行时** | TypeScript 运行时，Agent 可直接编写执行代码 |
| **Interpreter Skills** | Skill 的代码模块化，可 import 调用而非指令跟随 |
| **渐进式披露** | Agent 只需知道 Skill 的存在，具体内容按需加载 |
| **子 Agent 编排** | Skill 代码可以生成和管理子 Agent |
| **任务图管理** | 内置工作流状态管理，支持部分失败处理 |
| **可观测性** | 与 LangSmith 深度集成 |
| **LangSmith Sandboxes** | 安全执行 Agent 生成的代码 |

---

## 适用场景

✅ **适合的场景**：
- 需要确定性执行路径的生产级工作流（数据处理、GitHub 管理、合规检查）
- 同一 Skill 被多个 Agent 复用的场景
- 需要对 Agent 行为进行代码级测试和审计的场景
- 需要 Skill 代码直接操控 Harness 编排逻辑的场景

❌ **不太适合的场景**：
- 需要高度创意和灵活性的任务（此时自然语言 Prompt 更适合）
- 对执行延迟敏感的场景（Interpreter 增加了额外的执行层）
- 只需要简单工具调用的场景（直接用 Function Calling 更轻量）

---

## 与本轮 Articles 的关联

本轮 Article「LangChain Interpreter Skills：将 Harness 逻辑下沉到可执行代码模块」正是基于 deepagents 的 Interpreter Skills 功能撰写。两者形成闭环：

- **Article**：分析 Interpreter Skills 的设计理念和工程价值
- **Project**：推荐 deepagents 作为实现该架构的生产级框架

原文引用均来自 LangChain 官方博客和 GitHub README。

---

## 快速上手

```bash
pip install deepagents
```

官方文档：https://github.com/langchain-ai/deepagents

LangChain 官方博客详细讲解：https://www.langchain.com/blog/interpreter-skills