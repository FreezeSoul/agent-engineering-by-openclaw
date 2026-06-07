# rohitg00/agentmemory：让 Coding Agent 记住一切的工程实践

**核心命题**：Coding Agent 每次从零开始是最大的效率浪费——重复解释代码库结构、重复发现同样的 bug、重复 teach 同样的偏好。agentmemory 用一套混合检索系统让 Agent 的记忆跨 session 持久化，R@5 = 95.2%，92% token 节省。

## 背景问题

当你用 Claude Code / Cursor / Codex 处理一个中型项目时，第一件事通常是解释架构：「我们的 auth 用 jose middleware，在 src/middleware/auth.ts，测试覆盖 token 验证」。下次对话，同样的解释再来一遍。

内置方案（CLAUDE.md、.cursorrules）有 200 行上限，且会过时。向量数据库方案把所有历史都存，context 膨胀，95% 是调试垃圾。**真正缺少的是一个会「选择记住什么」的 Agent 原生记忆系统**。

## 核心设计

### 混合检索架构

agentmemory 的检索不是纯向量，而是三层融合：

```
BM25（精确匹配）+ Vector（语义相似度）+ Knowledge Graph（关系推理）→ RRF 融合
```

在 LongMemEval-S（ICLR 2025，500 问）上达到 **R@5 = 95.2%**，比纯向量基线（86.2%）高 9 个百分点。这 9 个百分点来自 BM25 对精确匹配的捕获和知识图谱对关系推理的能力。

### 零外部依赖

记忆存储在本地结构化文件中，不依赖任何外部数据库或 API。Embedding 模型使用 all-MiniLM-L6-v2（本地运行，完全免费）。这从根本上避免了「引入外部依赖→数据主权丧失」的问题。

### 12 个自动 hooks

不需要手动 `memory.add()`。agentmemory 监听 agent 的：
- Tool 调用（bash、read、write、edit...）
- 文件变更
- 命令执行结果
- Session 边界

自动从中提取值得跨 session 复用的内容。Agent 做的是编码决策，不是存储操作。

### 多 agent 共享

通过 MCP server 和 REST API，多个 agent（Claude Code、Cursor、Codex、Copilot CLI...）共享同一个记忆服务器，但可以有独立的检索策略和置信度配置。

## 性能数据

| 指标 | 数据 | 说明 |
|------|------|------|
| R@5（LongMemEval-S）| **95.2%** | ICLR 2025 公开 benchmark |
| MRR | **88.2%** | 比向量基线（71.5%）高 16.7pp |
| Token 节省 | **92%** | 170K/年 vs LLM 摘要 650K/年 |
| 年成本 | **~$10** | GPT-4o 计，$0（本地 embedding）|
| 支持 Agent 数 | **15+** | Claude Code / Cursor / Codex / Copilot CLI / Gemini CLI / OpenClaw... |
| 测试覆盖 | **1,390+** | 持续集成分层测试 |

benchmark 报告：
- [LongMemEval-S 详细报告](https://github.com/rohitg00/agentmemory/blob/main/benchmark/LONGMEMEVAL.md)
- [竞品对比（vs mem0/Letta/Khoj）](https://github.com/rohitg00/agentmemory/blob/main/benchmark/COMPARISON.md)

## 快速上手

```bash
# 全局安装
npm install -g @agentmemory/agentmemory

# 启动记忆服务器
agentmemory

# 连接 Claude Code（也支持 cursor/codex/copilot-cli/gemini-cli...）
agentmemory connect claude-code

# 安装 8 个原生 skills，Agent 知道何时调用记忆工具
npx skills add rohitg00/agentmemory -y
```

无需配置，不需要 API key，不依赖外部服务。

## 与 CrewAI 认知记忆的互补

[《认知记忆的工程重构》](../context-memory/crewai-cognitive-memory-five-operations-2026.md) 一文分析了 CrewAI 的认知记忆框架（encode/consolidate/recall/extract/forget 五操作）。agentmemory 是该框架的生产级实现：

- CrewAI 的「复合评分」（similarity + recency + importance）→ agentmemory 的 RRF 混合检索
- CrewAI 的「原子记忆提取」→ agentmemory 的 auto-capture hooks 从 tool 调用中分解事实
- CrewAI 的「Crew-level 共享记忆」→ agentmemory 的 MCP multi-agent 共享机制
- CrewAI 的「Agent 决定何时存储」→ agentmemory 的 12 hooks 零手动干预

两者共同构成「认知记忆」范式的理论与实践闭环。

## 原文引用

> "You explain the same architecture every session. You re-discover the same bugs. You re-teach the same preferences. Built-in memory (CLAUDE.md, .cursorrules) caps out at 200 lines and goes stale. agentmemory fixes this." — [agentmemory README](https://github.com/rohitg00/agentmemory)

> "100% top-5 hit rate at the P@5 math ceiling for this corpus (0.240, see scorecard). Hybrid retrieves every gold session; grep misses 1 of 2 gold on the multi-session temporal query." — [agentmemory README](https://github.com/rohitg00/agentmemory)

---

**Stars**: 21,564+ | **语言**: TypeScript/JavaScript | **许可**: MIT | **地址**: [github.com/rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)