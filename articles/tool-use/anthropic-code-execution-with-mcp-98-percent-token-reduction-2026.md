# Code execution with MCP: 98.7% token reduction and the future of AI agents

> Anthropic Engineering Blog — 2025年11月4日
> 核心问题：MCP 工具定义随连接数增长而膨胀，威胁 Agent 可用性
> 核心洞察：代码执行将工具调用从「直接请求」变为「API 编程」，减少 98.7% token 消耗

---

## 问题的起点：工具定义是 Agent 的隐藏成本

当你在 MCP 中连接了数百个工具时，每个工具的定义都要塞进 Agent 的 context window。

Anthropic 的工程师在博客中指出了这个问题的规模：

> "Direct tool calls consume context for each definition and result. Agents scale better by writing code to call tools instead."

直接工具调用的代价：
- 每个工具的 JSON Schema 定义进入 context
- 工具执行结果（可能很大）需要传回 context
- 连接的工具越多，context 消耗越快

当 MCP 服务器数量增长到数十个时，这个问题从「优化」变成了「生存问题」。

---

## 代码执行：把工具变成 API，把 Agent 变成开发者

Anthropic 的解法是让 Agent 用代码「编程式地」调用 MCP 服务，而不是直接调用工具。

具体做法：

**传统方式（直接调用）**：
```
Agent context → 加载所有工具定义 → 调用 tool_X → 传回结果
```

**代码执行方式（间接调用）**：
```
Agent 发现工具：通过文件系统浏览 /servers/ 目录
                ↓
Agent 只加载需要的工具定义（按需加载）
                ↓
Agent 写代码访问 MCP 服务器
                ↓
中间结果在执行环境中处理，只把过滤后的结果传回 context
```

关键代码示例（来自博客原文）：

```python
# Agent 通过文件系统发现可用工具
./servers/google-drive/getDocument.ts
./servers/google-drive/updateRecord.ts

# Agent 只读取需要的工具文件
# 而不是在 context 里加载所有工具定义
```

这种按需加载的方式，将 token 消耗从 **150,000 tokens 降低到 2,000 tokens**，减少了 98.7%。

---

## 为什么这个思路有深度

代码执行解决的不只是 token 问题，它改变了一个根本性的设计模式：

| 维度 | 直接工具调用 | 代码执行 |
|------|-------------|---------|
| 工具发现 | 全部加载到 context | 通过文件系统浏览，按需读取 |
| 数据处理 | 原始结果传回 context | 在执行环境过滤后再传回 |
| 复杂性处理 | context 承担 | 执行环境承担（代码逻辑） |
| 状态管理 | 通过 context 传递 | 留在执行环境，按需回传 |
| 工具组合 | 每个工具单独调用 | 代码中完成多步组合 |

换句话说，**代码执行把「有多少工具」的问题，从 context 问题变成了执行环境问题**。

Anthropic 博客中有一个关键洞察：

> "Many of the problems here feel novel—context management, tool composition, state persistence—but they have known solutions from software engineering. Code execution applies these established patterns to agents."

这不是新问题，这是软件工程中「关注点分离」原则在 Agent 领域的应用。

---

## 代码执行的安全与状态管理收益

除了 token 优化，代码执行还有两个被低估的优势：

### 1. 状态不泄露

直接工具调用的结果会直接进入 context window，敏感信息无法控制。

代码执行模式下：
- 中间结果留在执行环境
- 只有你需要的数据才传回 Agent
- 执行环境可以有自己的安全边界

### 2. 复杂逻辑在正确的地方处理

如果一个工具调用需要「先查 A，再根据 A 的结果查 B，最后聚合结果」，在直接调用模式下，这个逻辑要么在 prompt 里（消耗 token），要么在 context 里（复杂度高）。

在代码执行模式下，这就是普通的程序逻辑，在执行环境里自然处理。

---

## 权衡：代码执行引入的复杂度

Anthropic 坦诚地指出了代码执行的代价：

> "Running agent-generated code requires a secure execution environment with appropriate sandboxing, resource limits, and monitoring. These infrastructure requirements add operational overhead and security considerations that direct tool calls avoid."

这是一条工程上的权衡：

- **直接调用**：简单，开箱即用，但 context 消耗高
- **代码执行**：需要建设执行环境，但 context 效率高

Anthropic 的建议：

> "The benefits of code execution—reduced token costs, lower latency, and improved tool composition—should be weighed against these implementation costs."

笔者认为：对于工具数量超过 10 个、context 消耗已经影响 Agent 稳定性的场景，这个权衡是值得的。

---

## 适用场景判断

**适合代码执行**：
- MCP 服务器数量 > 10
- 单次任务涉及跨服务的复杂数据处理
- 需要在工具调用间保持中间状态
- 长期运行的 Agent（context 会被复用的场景）

**不适合代码执行**：
- 简单的一次性工具调用
- 安全/沙箱环境尚未就绪
- 工具数量少，context 消耗不是瓶颈

---

## 与其他趋势的关联

这个方向与两个重要的 Agent 工程趋势形成了呼应：

**1. MCP 协议的成熟**

MCP 已经从「一个协议」进化成「工具生态的连接层」。代码执行让 MCP 不只是「如何调用」，而是「如何高效调用」。

**2. Long-running Agent 的 context 管理**

当 Agent 需要跨多个 session 保持一致性时，context 效率是核心瓶颈。代码执行提供了一条工程上可行的路径。

---

## 引用

1. Anthropic Engineering Blog, "Code execution with MCP: building more efficient AI agents", November 4, 2025
   https://www.anthropic.com/engineering/code-execution-with-mcp

2. Cloudflare published similar findings, referring to code execution with MCP as "Code Mode"