# study8677/awesome-architecture：21张架构地图，系统设计知识库

**stars**: 809 | **language**: Vue | **created**: 2026-05-23

## 概述

[awesome-architecture](https://github.com/study8677/awesome-architecture) 是一个软件架构知识库，提供 **21 张架构地图**（C4 模型），涵盖 AI Gateway、RAG、智能体（Agents）、推理服务（Inference Serving）、向量数据库等核心领域。配套语言无关的系统设计教程，每个模板链接到真实开源原型。中英双语。

## 核心内容

**21 张架构地图覆盖**：
- **AI Gateway**：AI 请求路由、限流、鉴权架构
- **RAG**：检索增强生成的多种实现模式（Naive RAG、Advanced RAG、Modular RAG）
- **Agents**：单 Agent、多 Agent、Agent 协作架构
- **Inference Serving**：模型部署、批量推理、实时推理架构
- **Vector DB**：向量数据库选型与集成架构
- **其他**：微服务、C4 模型、分布式系统、面试准备

每个架构地图包含：
- 组件关系图（Container / Component / Code 层级）
- 关键技术选型说明
- 配套开源项目链接

## 架构知识在 AI Agent 时代的重要性

AI Agent 工程正在经历从「单点工具」到「系统架构」的演进：

- **Harness 架构**（参考 `harness/` 目录文章）：Claude Code / OpenAI Codex 的执行层隔离、沙盒设计、上下文管理
- **Multi-Agent 编排**：A2A / GNAP 协议下的 Agent 通信、任务分配、状态管理
- **Memory 系统**：向量数据库 + RAG 的双层上下文架构

awesome-architecture 提供了这些架构模式的可视化参考，帮助工程师从全局视角理解 AI Agent 系统。

## 主题关联

- **理论层 × 执行层闭环**：awesome-architecture（架构地图/理论层）+ nexu-io/html-anything（HTML-First Editor/执行层）→ 形成「架构设计 → 代码实现」的完整学习路径
- **RAG 系统**：与 `context-memory/` 目录下 RAG 相关文章形成闭环（架构图 + 实现在线教程）
- **AI Gateway**：与 Agent 基础设施文章（`harness/` 目录）形成管理面/数据面分离的架构对照

## 使用方法

```bash
# 克隆仓库
git clone https://github.com/study8677/awesome-architecture.git

# 查看 AI Agent 相关架构
# 目录结构：
# 01-ai-gateway/
# 02-rag/
# 03-agents/
# 04-inference-serving/
# 05-vector-db/
# 06-microservices/
# ...共21个模块
```

## 延伸阅读

- [anysphere/kernel-optimization-results-2026](/articles/ai-coding/anysphere-kernel-optimization-results-2026.md) — Cursor 内核优化与架构权衡
- [multi-agent-orchestration-four-paradigms](/articles/orchestration/multi-agent-orchestration-four-paradigms-anthropic-swarms-2026.md) — Multi-Agent 编排范式
- [context-mode-mksglu-98-percent-context-reduction](/articles/projects/context-mode-mksglu-98-percent-context-reduction-2026.md) — 上下文压缩工程实践
