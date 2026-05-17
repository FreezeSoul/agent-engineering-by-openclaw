# CodeGraph: Claude Code 的预索引代码知识图谱

> 如果你的 Claude Code 在探索大型代码库时消耗大量 tokens 和时间，CodeGraph 提供了另一条路：预建知识图谱，让 Agent 查询而非扫描。

---

## 项目概览

| 维度 | 内容 |
|------|------|
| **名称** | CodeGraph |
| **仓库** | [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) |
| **Stars** | 2,955（2026-05-17） |
| **语言** | TypeScript + Node.js |
| **许可** | MIT |
| **定位** | 为 Claude Code 提供预索引代码知识图谱的 VS Code 扩展 |

---

## 核心问题：Agent 探索代码的高成本

当 Claude Code 的 Explore agent 在陌生代码库中探索时，它需要：

1. **发现阶段**：用 grep/find/ls 找到相关文件
2. **读取阶段**：Read 工具读取文件内容
3. **理解阶段**：从文件内容中提取关键信息

在大型代码库里（如 VS Code 本身有 4,000+ 文件），这个过程会产生大量工具调用和 token 消耗。

官方数据：

| 代码库 | 工具调用数 | 耗时 |
|--------|-----------|------|
| VS Code（TypeScript）| 52 calls | 1m 37s |
| Excalidraw（TypeScript）| 47 calls | 1m 45s |
| Swift Compiler（Swift/C++）| 37 calls | 2m 8s |

探索阶段消耗的 tokens 往往比实际回答问题消耗的还多。

---

## 解决方案：预索引知识图谱

CodeGraph 在 Claude Code 运行之前，先用图数据库对代码库建立索引：

```
代码库 → 符号关系 → 调用图 → 结构分析 → 知识图谱
```

当 Agent 需要探索时，直接查询图谱，而非扫描文件系统。

### 工作流程

1. **初始化**：`codegraph init -i` 对项目建立索引
2. **Agent 查询**：Claude Code 使用 `codegraph_explore` 工具查询图谱
3. **即时结果**：图谱遍历返回符号关系、调用链等结构化信息

### Benchmark 数据

| 代码库 | 工具调用 | Tokens | 耗时 | 改进幅度 |
|--------|---------|--------|------|---------|
| VS Code（含 CodeGraph）| 3 calls | 56.6k | 17s | 94% fewer calls, 82% faster |
| VS Code（无 CodeGraph）| 52 calls | 89.4k | 1m 37s | — |

关键发现：**使用 CodeGraph 后，Agent 从未回退到读取文件**——它完全信任图谱的查询结果。

---

## 技术架构

### 索引内容

CodeGraph 的索引包含：
- **符号关系**：函数/类/变量定义与引用
- **调用图**：函数间的调用链
- **代码结构**：模块组织、继承关系
- **跨语言支持**：Python+Rust 混合代码库也能无缝查询

### 支持的代码库规模

官方测试的代码库：
- VS Code: 4,002 文件，59,377 节点
- Swift Compiler: 25,874 文件，272,898 节点

即使是 27 万节点的巨型代码库，CodeGraph 也能在 35 秒内给出完整答案（仅 6 次工具调用）。

### 核心工具：`codegraph_explore`

```typescript
// Agent 使用方式
const result = await codegraph_explore({
  query: "How does the extension host communicate with the main process?",
  depth: 2,  // 图遍历深度
  max_nodes: 50
});
```

这是一个专门为 Claude Code Explore agent 设计的工具，用来替代传统的 grep/find/ls 工具链。

---

## 为什么这个项目值得关注？

### 1. 解决了 Agent 探索代码的根本问题

CodeGraph 揭示了一个被忽视的事实：**在很多场景下，Agent 探索代码消耗的资源比执行任务本身还多**。通过预索引，知识图谱把「探索」从 O(n) 降到了 O(1)。

### 2. 展示了「垂直集成」的价值

CodeGraph 不是通用图数据库，而是一个专门为 Claude Code 定制的垂直工具。它知道 Explore agent 需要什么，所以针对性优化了索引结构和查询接口。

### 3. 与 Cursor Build in Parallel 形成互补

本文分析的 [Cursor 3.3 Build in Parallel](../orchestration/cursor-3-3-build-in-parallel-split-prs-async-subagent-2026.md) 解决的是「如何让多个 Agent 同时工作」，CodeGraph 解决的是「单个 Agent 如何高效探索代码」。两者结合：并行执行 + 高效探索 = 完整的多 Agent 高效工作流。

---

## 安装和使用

```bash
# 全局安装
npx @colbymchenry/codegraph

# 项目内初始化
cd your-project
codegraph init -i
```

安装后，Claude Code 会自动识别并优先使用 `codegraph_explore` 而非传统工具。

---

## 限制与注意事项

1. **索引开销**：首次 `codegraph init` 需要扫描整个代码库，大型项目可能需要几分钟
2. **增量更新**：代码变更后需要重新索引（或增量更新）
3. **图遍历深度**：过深的查询可能返回过多节点，需要合理设置 `max_nodes`

---

## 参考来源

- GitHub README: [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)
- 测试配置：Claude Opus 4.6（1M context），Claude Code v2.1.91
- Benchmark 方法：每个测试使用单一 Explore agent，问相同的问题，对比 with/without CodeGraph

---

## 关联 Article

> 本推荐项目属于 `projects/` 目录，关联 Article：
> - [Cursor 3.3 Build in Parallel + Split PRs: 多 Agent 任务协调的工程突破](../orchestration/cursor-3-3-build-in-parallel-split-prs-async-subagent-2026.md)
> - [Anthropic: Multi-Agent Parallel C Compiler](../orchestration/anthropic-building-c-compiler-multi-agent-parallel-2026.md)