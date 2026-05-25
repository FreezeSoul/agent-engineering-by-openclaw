# Claude Code /goal：让 Evaluator Loop 成为一等公民

> 本文分析 Claude Code v2.1.139（2026-05-11）引入的 `/goal` 命令，探讨其如何将「评估器循环」从隐式的工程实现变成显式的用户接口。

## 背景：Harness 的两种模式

在 Claude Code 的架构中，有两种控制 Agent 自主行为的机制：

| 机制 | 存在形式 | 用户感知 |
|------|---------|---------|
| **Stop Hook** | `settings.json` 中的持久化配置 | 需要写代码，对普通用户门槛高 |
| **`/goal`** | 终端中的一行命令 | 输入条件即可，零门槛 |

`/goal` 的本质是一个**Session-Scoped 的 Prompt-Based Stop Hook 包装器**。Anthropic 将其定位为：

> `/goal` adds a separate evaluator that checks your condition after every turn, so completion is decided by a fresh model rather than the one doing the work.

这揭示了 Evaluator Loop 的核心设计哲学：**执行者（main model）和评估者（evaluator）必须分离**。

## Evaluator Loop 的技术实现

### 三方架构

```
┌─────────────────────────────────────────────┐
│              Main Model (Claude)            │
│         执行任务、调用工具、写代码           │
└─────────────────┬───────────────────────────┘
                  │ 输出到 conversation
                  ▼
┌─────────────────────────────────────────────┐
│           Evaluator (Haiku by default)      │
│    读取 conversation，判断条件是否满足         │
│    仅做判断，不调用工具，不读写文件           │
└─────────────────┬───────────────────────────┘
                  │ Yes/No + Reason
                  ▼
┌─────────────────────────────────────────────┐
│           决策路由                           │
│  Yes → 清除 goal，记录 "achieved"           │
│  No  → 继续下一 turn，reason 作为 guidance   │
└─────────────────────────────────────────────┘
```

关键约束：**Evaluator 只能看到 conversation 中已 surfaced 的内容**，无法独立验证。这意味着 main model 必须主动将验证结果输出到 conversation，否则 evaluator 无法判断。

Anthropic 在官方文档中明确举例：

> "All tests in test/auth pass" works because Claude runs the tests and the result lands in the transcript for the evaluator to read.

如果 Claude 只写"tests are passing"但不实际运行 `npm test`，Evaluator 会返回"Not yet verified"。

### 条件写作的三要素

根据官方文档，一个有效的 condition 通常包含：

1. **可验证的终点状态**：测试通过、构建成功、文件数量为零
2. **明确的检查方式**：如何证明完成了，如 `npm test exits 0`
3. **不可破坏的约束**：如"其他文件未被修改"或"不超过 N 轮"

### 与 `/loop` 的本质区别

| 维度 | `/goal` | `/loop` |
|------|---------|---------|
| 触发下一轮的条件 | Evaluator 判断条件未满足 | 时间间隔到达 |
| 停止条件 | **模型判断**（外部验证）| 人工停止或模型自行判断 |
| 适用场景 | 有明确终点的任务 | 监控外部状态（部署、轮询）|
| 本质 | **Declarative**（声明目标）| **Imperative**（周期性执行）|

## 工程意义：Harness 的民主化

从 Harness Engineering 的视角看，`/goal` 的意义不仅是一个命令，而是：

**它将「评估器循环」从需要编程的配置变成了自然语言交互。**

过去实现一个 Evaluator Loop 需要：
1. 写一个 Stop Hook（JavaScript/Python）
2. 配置 `settings.json`
3. 处理执行结果和判断逻辑

现在只需要：
```
/goal all tests pass and no lint errors
```

Anthropic 官方将 `/goal` 与 Auto Mode 描述为互补关系：

> auto mode removes per-tool prompts, and `/goal` removes per-turn prompts.

这意味着 Claude Code 的自主性现在是分层的：
- **Auto Mode**：处理单轮内的工具授权
- **`/goal`**：处理多轮间的任务完成判断

两者叠加，实现了一个承诺：**一次 prompt，等待条件满足**。

## 与 Stop Hook 的关系

值得注意的是，`/goal` 是 Stop Hook 的**上层封装**，而非替代：

```
/goal = Session-Scoped + Prompt-Based + One-Line Interface
Stop Hook = Persistent + Script-Based + Full Programming
```

两者技术上都基于"每轮结束后触发判断"的机制，但：
- Stop Hook 可以运行**任意脚本**（确定性检查）
- `/goal` 使用**模型判断**（适合无法用脚本验证的复杂条件）

一个实用的组合是：Stop Hook 处理确定性检查（如文件大小限制），`/goal` 处理需要语义理解的验收标准（如"代码风格一致"）。

## 局限性

1. **Evaluator 无法独立验证**：如果 main model 不将验证结果 surfaced 到 conversation，Evaluator 无法判断
2. **不适用于无明确终点的任务**：如"研究一下这个领域"这种开放式任务
3. **Session-Scoped**：`/goal` 只在当前 session 有效，无法跨会话持久化（但可以 `resume`）

## 结论

`/goal` 将 Evaluator Loop 从 Claude Code 的底层架构设计变成了前台用户接口。这是 Harness Engineering 的一次民主化尝试——让普通用户也能用自然语言定义任务完成条件，而不是写代码配置。

**笔者认为**，这代表了 Agent 系统从「人盯着干」到「人定义目标」转变的关键节点：用户定义**目标**，模型决定**如何干**，另一个模型判断**干完了没**。

---

**引用来源**：
- [Keep Claude working toward a goal - Claude Code Docs](https://code.claude.com/docs/en/goal)
- [Claude Code /goal: A Field Guide with Games - Jason Croucher](https://medium.com/@jason.croucher/claude-code-goal-a-field-guide-with-games-f6f3b617ce5b)
- [Week 20 · May 11–15, 2026 - Claude Code Docs](https://code.claude.com/docs/en/whats-new/2026-w20)