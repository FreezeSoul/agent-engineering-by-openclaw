# Agent 技术演进地图

> 从 2022 到 2026，Agent 技术发展脉络与关键里程碑。

---

## 目录

| 文件 | 内容 |
|------|------|
| [agent-ecosystem.md](./agent-ecosystem.md) | 当前生态全景图（分层架构） |
| [README.md](./README.md) | 本目录说明（本文件） |

---

## 演进时间线速览

| 年份 | 里程碑 | 影响 |
|------|--------|------|
| **2022** | ReAct 论文发布 | 推理与执行分离成为主流范式 |
| **2023** | Toolformer / AutoGen / LangChain 发布 | Agent 框架元年开始 |
| **2024** | GPT-4o / Claude 3.5 发布 | 多模态 Agent 成为可能 |
| **2025** | MCP 协议诞生 | 协议层标准化启动 |
| **2026** | MCP 捐赠 Linux 基金会 | 协议层标准化加速，生态爆发 |

---

## 核心发展脉络

### 协议层演进

```
Function Calling (2023)
    ↓
MCP 标准萌芽 (2025)
    ↓
MCP 捐赠 Linux 基金会 (2026) ← 当前节点
```

### 框架层演进

```
LangChain (原型优先) → LangGraph (生产优先)
CrewAI (角色协作) → 持续活跃
AutoGen (微软生态) → 持续活跃
```

### Agent 能力演进

```
单步问答 → ReAct 多步推理 → Plan-Execute 规划执行
→ Memory 记忆管理 → MCP 工具生态 → 多 Agent 协作
```

---

## 问题域结构（本仓库文章组织方式）

本仓库按 **Agent 工程问题域** 组织内容：

| 目录 | 解决的问题 |
|------|-----------|
| `articles/fundamentals/` | Agent 基础概念、设计模式、工程思维 |
| `articles/context-memory/` | 记忆机制、上下文管理、RAG 融合 |
| `articles/tool-use/` | 工具调用、MCP 协议、安全实践 |
| `articles/orchestration/` | 多 Agent 协作、协议栈、编排模式 |
| `articles/harness/` | Harness Engineering、安全约束、评测 |
| `articles/evaluation/` | 评测基准、可观测性、Benchmark |
| `articles/deep-dives/` | 单点深度分析、范式研究 |

---

## 相关目录

| 目录 | 关系 |
|------|------|
| `frameworks/` | 具体框架详细文档 |
| `practices/` | 设计模式与代码示例 |
| `resources/` | 工具与论文资源索引 |

---

*持续更新，最后更新：2026-04-02*
