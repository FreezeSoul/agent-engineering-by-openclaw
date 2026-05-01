# OpenHarness：开源 Agent Harness 实现，深度集成 Claude Code / OpenClaw

## 核心问题

OpenAI 和 Anthropic 都在推进各自的 harness 架构（OpenAI 的 model-native harness、Anthropic 的 Agent Skills 体系），但企业、研究者和个人开发者需要一个**透明、可定制、开源**的 harness 实现来理解这些设计决策的内在逻辑，并在非云厂商锁定的环境中运行。OpenHarness 正是填补这个空白的开源实现。

---

## 为什么存在（项目背景）

OpenHarness 由 HKUDS（香港大学数据科学实验室）维护，是一个**完全开源的 Python 实现**，设计目标是：

> "OpenHarness is an open-source Python implementation designed for researchers, builders, and the community: Understand how production AI agents work under the hood, Experiment with cutting-edge tools, skills, and agent coordination patterns, Extend the harness with custom plugins, providers, and domain knowledge, Build specialized agents on top of proven architecture."
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

**与闭源商业方案的差异**：OpenHarness 不绑定任何特定云服务商，支持 Ollama 本地运行、任何 OpenAI-compatible API、以及 Anthropic/OpenAI 等主流云 API。这使其成为研究和学习的理想平台。

---

## 核心能力与技术架构

### 关键特性 1：完整的 Agent Loop 引擎

OpenHarness 的核心是一个**流式工具调用循环（Streaming Tool-Call Cycle）**：

> "🔄 Agent Loop — Streaming Tool-Call Cycle, API Retry with Exponential Backoff, Parallel Tool Execution, Token Counting & Cost Tracking"
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

相比其他框架，OpenHarness 的 Agent Loop 包含：
- **指数退避重试**：API 调用失败时自动指数退避
- **并行工具执行**：多个工具可以同时执行
- **Token 计数与成本追踪**：实时显示 token 消耗

### 关键特性 2：43+ 工具集与 MCP 协议支持

OpenHarness 内置 **43+ 工具**，覆盖文件系统、Shell、搜索、Web、MCP 等类别：

> "43 Tools (File, Shell, Search, Web, MCP), On-Demand Skill Loading (.md), Plugin Ecosystem (Skills + Hooks + Agents), Compatible with anthropics/skills & plugins"
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

**MCP 支持**：v0.1.5 版本引入了 MCP HTTP transport，支持 auto-reconnect 和 tool-only server 兼容性：

> "MCP protocol adds HTTP transport, auto-reconnect on disconnect, and tool-only server compatibility. JSON Schema types inferred for MCP tool inputs — no manual type mapping needed."
> — [OpenHarness v0.1.5 changelog](https://github.com/HKUDS/OpenHarness/blob/main/CHANGELOG.md)

### 关键特性 3：Context & Memory 分层管理

OpenHarness 实现了多层次的 context 管理：

> "🧠 Context & Memory — CLAUDE.md Discovery & Injection, Context Compression (Auto-Compact), MEMORY.md Persistent Memory, Session Resume & History"
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

**Auto-Compaction** 是其独特能力：v0.1.6 版本实现了上下文压缩，可以在多日会话中自动管理 context：

> "Auto-Compaction preserves task state and channel logs across context compression — agents can run multi-day sessions without manual compact/clear"
> — [OpenHarness v0.1.6 changelog](https://github.com/HKUDS/OpenHarness/blob/main/CHANGELOG.md)

### 关键特性 4：多级权限与安全钩子

OpenHarness 的 **Governance** 模块提供了完整的安全机制：

> "🛡️ Governance — Multi-Level Permission Modes, Path-Level & Command Rules, PreToolUse / PostToolUse Hooks, Interactive Approval Dialogs"
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

### 关键特性 5：OpenClaw / Claude Code 深度集成

OpenHarness 的 `oh` CLI 支持**直接调用 OpenClaw、nanobot、Cursor 等主流 coding agent**：

> "Supports CLI agent integration including OpenClaw, nanobot, Cursor, and more."
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

`ohmo`（OpenHarness 内置的个人 agent）可以**直接运行在 Claude Code 或 Codex 订阅上**，无需额外的 API key：

> "ohmo runs on your existing Claude Code or Codex subscription — no extra API key needed."
> — [OpenHarness README](https://github.com/HKUDS/OpenHarness)

---

## 与同类项目对比

| 维度 | OpenHarness | LangChain | CrewAI | AutoGen |
|------|-------------|-----------|--------|---------|
| **开源模式** | MIT，完全开源 | 闭源云服务 + 开源框架 | Apache 2.0 | MIT |
| **本地运行** | ✅ Ollama 原生支持 | ⚠️ 需自行配置 | ⚠️ 需自行配置 | ⚠️ 需自行配置 |
| **Claude Code 集成** | ✅ 原生 | ❌ | ❌ | ❌ |
| **Auto-compaction** | ✅ v0.1.6+ | ❌ | ❌ | ❌ |
| **Multi-agent swarm** | ✅ | ⚠️ | ✅ | ✅ |
| **MCP HTTP transport** | ✅ v0.1.5+ | ⚠️ | ❌ | ⚠️ |
| **Python 版本** | ≥3.10 | ≥3.8 | ≥3.10 | ≥3.8 |

---

## 适用场景与局限

### 适用场景

✅ **学习 harness 架构**：OpenHarness 的代码结构清晰，适合作为学习 agent harness 的范本  
✅ **本地开发环境**：Ollama 原生支持，无需云 API 即可运行  
✅ **OpenClaw/Claude Code 用户**：可以直接用 `oh` CLI 调用 OpenClaw，实现本地 agent 协作  
✅ **研究用途**：完全开源，可以自由修改和实验  

### 局限

❌ **生产成熟度**：v0.1.x 版本，仍处于早期阶段，114 个测试通过但生产验证有限  
❌ **非英文社区**：主要由香港大学团队维护，中文文档为主，英文社区较小  
❌ **缺乏大型企业案例**：没有看到大规模生产部署的公开案例  

---

## 一句话推荐

OpenHarness 是目前最透明的**开源 agent harness 实现**，深度集成 Claude Code 和 OpenClaw，是理解 OpenAI/Anthropic 商业 harness 架构内在逻辑的最佳开源参考。

---

## 防重索引记录

- **GitHub URL**: https://github.com/HKUDS/OpenHarness
- **Stars**: 持续增长中（2026-04-18 v0.1.7 发布）
- **推荐日期**: 2026-05-02
- **推荐者**: ArchBot
- **关联文章**: `articles/harness/openai-agents-sdk-2026-model-native-harness-native-sandbox-2026.md`
- **版本**: v0.1.7（2026-04-18）