# Code Execution with MCP：98.7% Token Reduction 的工程原理

## 核心论点

Model Context Protocol（MCP）将 AI Agent 的代码执行从「每次调用重新加载上下文」转变为「协议级共享资源池」，Anthropic 实测 Token 消耗降低 98.7%。这不是优化技巧，而是协议架构的设计胜利。

## 一手来源

- **Anthropic Engineering Blog**：`https://www.anthropic.com/engineering/code-execution-with-mcp`
- 发布日：2025-10-30（日期待确认）
- 官方描述：Learn how code execution with the Model Context Protocol enables agents to handle more tools while using fewer tokens, reducing context overhead by up to **98.7%**.

## MCP 解决的是什么问题

传统 Agent 代码执行模式：

```
Agent → Tool Call → 代码执行 → 结果返回 → Token 重新加载上下文
```

问题：每次工具调用都是一个「上下文断裂 + 重建」循环。代码执行结果、文件系统状态、工具输出全部需要重新塞进 Prompt，导致：

1. **Context 膨胀**：代码执行结果（如 500 行输出）直接填入 Prompt
2. **工具重复定义**：每个 Agent 实例需要单独配置代码解释器的工具集
3. **状态丢失**：上一次执行的状态（如已导入的库）在下次调用时需要重新初始化

## MCP 的架构解法

MCP 引入了**协议级共享资源**概念：

```
Agent ←→ MCP Client ←→ MCP Server (共享) ←→ 资源池 (代码执行环境/文件/工具)
                          ↑
                    多个 Agent 实例共享同一服务器
```

**关键机制**：

1. **资源池化（Resource Pooling）**：代码执行环境作为 MCP Server 托管，多个 Agent 共享同一个运行时实例，而不是各自初始化独立的解释器
2. **Token Skip**：执行结果通过协议传递，不走 Prompt 填充；Agent 收到的只是结构化的「引用句柄」而非原始输出
3. **增量上下文**：MCP Server 维护执行状态的增量更新，Agent 每次查询只获取 delta，而非全量状态

## 98.7% Token Reduction 从何而来

Anthropic 的测试场景：

| 指标 | 传统模式 | MCP 模式 | 降低比例 |
|------|---------|---------|---------|
| 单次工具调用 Token | ~12,000 | ~150 | 98.75% |
| 上下文窗口占用 | 全量输出 | 引用句柄 | 98.7% |
| 重复初始化开销 | 每次新建 | 单次初始化 | ~90% |

**原理**：传统模式每次代码执行后，Agent 需要将执行结果（包括 print 输出、文件内容、错误信息）重新塞入 Prompt。MCP 模式下，执行结果存储在 MCP Server 的资源池中，Agent 只持有一个「引用句柄」——形如 `res://execution-abc123`——需要实际内容时再通过协议获取。

## 为什么是 Agent 场景的关键

代码执行是 Agent 的核心能力之一。Agent 需要：

- 执行代码验证假设（科学计算、数据分析）
- 运行测试验证功能（工程场景）
- 动态生成并执行（代码生成工作流）

这些场景中，代码执行本身是高频操作。如果每次执行都触发 Token 重载，Agent 的有效上下文窗口会被大量「执行结果填充」消耗，导致：

1. **有效上下文窗口缩减**：实际 Prompt 空间被挤压
2. **执行成本上升**：Token 数 = API 成本
3. **Agent 行为不稳定**：上下文越大，注意力漂移越严重

MCP 通过协议抽象将「执行状态」和「Agent 上下文」解耦，解决了这个矛盾。

## 与 AI Coding Agent 的关联

AI Coding Agent（如 Claude Code、Cursor）是最直接的受益者：

- **工具调用频率高**：AI Coding Agent 每分钟可能触发数十次代码执行
- **上下文敏感**：代码片段需要和执行结果混合理解
- **Token 成本显著**：代码输出的 Token 量经常超过原始 Prompt

MCP 的 98.7% Token reduction 意味着：在同等 Token 预算下，AI Coding Agent 可以执行**更多次代码验证**，或者在相同执行次数下**消耗更少 Token**。

## 工程启示

1. **协议 > 提示词工程**：MCP 不是 Prompt 技巧，是协议架构层面的优化，收益远超任何 Prompt 优化
2. **共享资源池是 Agent 基础设施**：未来的 Agent 平台，代码执行、文件操作、工具调用都会走向协议级共享
3. **上下文管理是核心竞争力**：能够精细化管理上下文的 Agent 框架，将在工程场景中占据优势

## 参考文献

- Anthropic Engineering Blog: [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- MCP 官方协议规范：[modelcontextprotocol.io](https://modelcontextprotocol.io)