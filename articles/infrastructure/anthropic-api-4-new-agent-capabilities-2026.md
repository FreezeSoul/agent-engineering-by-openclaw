---
title: "Anthropic API 四大新能力：构建 AI Agent 的基础设施重构"
slug: anthropic-api-4-new-agent-capabilities-2026
date: 2026-06-17
cluster: infrastructure
source: https://claude.com/blog/agent-capabilities-api
source_type: claude_blog
round: 418
pair_project: moltis-org-moltis-rust-personal-agent-server-2746-stars-2026.md
tags: [anthropic, api, agents, code-execution, mcp, files-api, prompt-caching, infrastructure]
---

# Anthropic API 四大新能力：构建 AI Agent 的基础设施重构

> 原文：[New capabilities for building agents on the Anthropic API](https://claude.com/blog/agent-capabilities-api)（Claude Blog，2026 年 6 月）

## 核心命题

2026 年 6 月，Anthropic 一次性发布 **四大 API 能力**——Code Execution Tool（沙盒 Python）、MCP Connector（远程 MCP 服务直连）、Files API（跨会话文件存储）、1 小时 Prompt Caching（成本优化缓存）。这四项能力**不再是「新增功能」，而是构建 AI Agent 的基础组件重构**——它们从「可选工具」升级为「一等公民」，标志着 Anthropic API 从「对话型 API」正式进化为「Agent 平台 API」。

| 能力 | 类型 | 解决的核心问题 | 关键创新 |
|------|------|----------------|----------|
| **Code Execution Tool** | 沙盒执行 | Agent 能否自己跑代码？| 沙盒化 Python + 50 小时/天免费配额 |
| **MCP Connector** | 协议直连 | 接入外部工具的复杂度？| 零客户端代码，URL 即可 |
| **Files API** | 状态存储 | 跨会话文件如何管理？| 服务端存储，文件 ID 引用 |
| **1-Hour Prompt Caching** | 成本优化 | 长上下文成本高？| 缓存延长至 1 小时 |

## 一、Code Execution Tool：从「写代码助手」到「数据分析师」

### 机制

Agent 通过 API 调用直接在一个 **沙盒化 Python 环境中**执行代码，产出计算结果和数据可视化。这与传统的「返回代码让用户自己跑」形成根本性差异——**Agent 在单次 API 调用中**即可完成数据加载、图表生成、模式识别、迭代精炼的完整工作流。

### 关键使用场景

Anthropic 在原文中列出 5 大场景，每个都具备工程化落地价值：

1. **金融建模**：生成投资预测、分析投资组合、计算复杂金融指标
2. **科学计算**：执行仿真、处理实验数据、分析研究数据集
3. **商业智能**：自动生成报表、分析销售数据、生成绩效仪表板
4. **文档处理**：跨格式抽取与转换、生成格式化报表、自动化工作流
5. **统计分析**：回归分析、假设检验、预测建模

### 定价与配额

- **50 小时/天免费**使用 Code Execution Tool
- 超出部分 **$0.05/小时/容器**
- 对比同类产品（如 E2B、Code Interpreter API），免费配额显著更慷慨

### 工程意义

这是 Anthropic 对「Agent 是否需要自己的计算环境」问题的**明确回答**——**Yes**，且应该是**一等公民**。结合 [Claude Code 的本地沙盒机制](https://claude.com/blog/claude-code-sandboxing)（已上线）和 [Cloudflare Sandboxes GA](https://blog.cloudflare.com/sandboxes-ga/) 等基础设施演进，可以看到一个清晰趋势：**「Agent + 沙盒」将成为 Agent Runtime 的标准组件**，而非各团队自行实现的能力。

## 二、MCP Connector：零客户端代码接入远程 MCP 服务

### 机制

开发者只需**在 API 请求中添加远程 MCP 服务器的 URL**，Anthropic API **自动处理**所有连接管理、工具发现、错误处理。Claude 接收请求后自动：

1. 连接到指定的 MCP 服务器
2. 检索可用工具
3. 推理该调用哪个工具、传递什么参数
4. Agent 化执行工具调用直到获得充分结果
5. 管理认证和错误处理
6. 返回增强后的响应

### 生态整合

Anthropic 在原文中点名 **Zapier 和 Asana** 作为首批合作伙伴。结合 [Cloudflare 的 MCP Server 索引](https://developers.cloudflare.com/agents/)，整个远程 MCP 服务生态正在迅速成熟。

### 工程意义

这解决了 **Agent 工具集成的最大痛点**——**Client Harness 的工程负担**。在 MCP Connector 出现之前，每个团队需要：
- 实现 MCP 客户端协议
- 处理连接管理（重连、超时、断路）
- 实现工具发现与动态注册
- 处理认证 token 刷新
- 处理工具调用错误与重试

这些工作往往是**重复造轮子**，且每家实现方式不同，造成生态碎片化。**MCP Connector 把这些下沉到 API 平台层**，开发者只需关注「用哪个 MCP 服务的 URL」即可。

## 三、Files API：跨会话文件存储的「一等公民」化

### 机制

Files API 让开发者**在 Anthropic 端存储和访问文件**，而无需在每次请求中管理文件上传。上传文件后，开发者获得一个文件 ID，后续请求中通过 ID 引用即可。

### 关键能力

- 跨会话持久化（文件不随请求结束消失）
- 服务端管理（无需自建对象存储）
- ID 引用（请求体极简）
- 与 Code Execution Tool 协同（沙盒可访问 Files API 存储的文件）

### 工程意义

这是 Anthropic 对「**Agent 的状态应该如何存储**」问题的关键回答。在 [Claude Managed Agents Memory](https://claude.com/blog/claude-managed-agents-memory) 和 [Agent Skills 的文件系统范式](https://claude.com/blog/agent-skills-as-filesystem) 等已有架构中，文件都是**客户端管理**的（保存在本地或用户自建存储）。**Files API 把「跨会话文件存储」提升为平台级能力**，这与 [LangGraph 的 Checkpoint 机制](https://langchain-ai.github.io/langgraph/concepts/persistence/) 和 [OpenAI 的 Response State 持久化](https://platform.openai.com/docs/guides/conversation-state) 形成对位。

## 四、1-Hour Prompt Caching：成本优化的边界扩张

### 机制

Prompt Caching 的有效期从之前的 **5 分钟延长到 1 小时**。对于需要长时间保持上下文的 Agent 应用（如长会话分析、长任务执行、跨小时的多步推理），这是一个**显著的成本优化杠杆**。

### 工程意义

- **对长任务 Agent 的成本结构改变**：1 小时缓存意味着 Agent 在执行多步任务时，可以**重复引用同一上下文而无需重新计费**
- **对实时协作场景的影响**：多人协作文档分析、跨小时 Code Review 等场景，缓存命中率将显著提升
- **对 Agent Runtime 设计的反向影响**：1 小时缓存窗口让「**Agent 长时间驻留 + 增量更新上下文**」成为可行模式

## 五大工程启示

### 1. Agent 平台的「组件下沉」趋势

| 时期 | Agent 能力 | 实现位置 |
|------|------------|----------|
| 2023-2024 | 工具调用 | 客户端 SDK |
| 2024-2025 | Memory / RAG | 客户端框架 |
| **2025-2026** | **Code Execution / MCP / Files / Caching** | **API 平台** |

这一演进意味着：**Agent 的核心能力正在从「框架竞争」转向「平台竞争」**。LangChain / LlamaIndex 等框架的护城河在收窄，**Anthropic / OpenAI 等平台提供商的护城河在加深**。

### 2. 沙盒化执行成为标准

Code Execution Tool 的推出，结合 Cloudflare Sandboxes、Daytona、Modal 等沙盒基础设施的成熟，标志着「**Agent 必须在沙盒中执行代码**」成为行业共识。这与 [LangSmith 的"Every Agent Needs A Computer"](https://docs.smith.langchain.com/concepts/sandbox) 哲学完全对位。

### 3. MCP 生态进入「平台分发」阶段

MCP Connector 让 **Zapier / Asana 等应用**成为 Anthropic Agent 生态的**首批公民**。结合 [Microsoft 收购 Ona](https://openai.com/index/openai-to-acquire-ona/)（持久化企业 Agent 环境）等事件，可以看到 **Agent 平台正在通过 MCP 协议实现应用层的「App Store 化」**。

### 4. Files API 暗示「Agent 持久化」演进

Files API 不只是「文件存储」，它暗示了**更深层的能力**：当 Agent 可以**在服务端持久化文件**时，配合 Memory / Skills / Caching，**Agent 实际上具备了「跨会话记忆」**——这与 [Anthropic 的 Memory as Filesystem 范式](https://claude.com/blog/claude-managed-agents-memory) 完全一致。

### 5. Prompt Caching 1 小时意味着什么

5 分钟缓存 vs 1 小时缓存的差异是 **12 倍**。对于长任务 Agent，这意味着：
- **成本预测性大幅提升**：1 小时内上下文固定的任务，缓存命中率可达 80%+
- **新用例解锁**：实时协作分析、跨小时任务接力、增量更新型 Agent 都成为可能
- **对 RAG 架构的冲击**：1 小时缓存 + Files API 让「**预计算 + 缓存 + 增量更新**」成为 RAG 的新基线

## 闭环逻辑

本文是一手源层（Anthropic 平台能力发布）的分析。配套 Project **moltis-org/moltis**（Rust 实现的个人 Agent Server，2,746⭐ MIT）是对位的**工程化身**：

| 维度 | Article（Anthropic API） | Project（moltis）|
|------|--------------------------|------------------|
| **定位** | 平台层 API 能力 | 开源个人 Agent Server |
| **执行环境** | 沙盒化 Python（服务端）| 沙盒化 Rust（本地/自托管）|
| **MCP 支持** | 远程 MCP Connector | 内置 MCP 客户端 |
| **文件存储** | Files API（服务端）| 本地文件 + 持久化 memory |
| **缓存** | 1 小时 Prompt Caching | 无显式缓存（本地模型无成本问题）|
| **部署** | SaaS / API 调用 | 单二进制自托管 |

两者形成 **「平台 API 能力 ↔ 开源个人 Agent 实现」** 的完美对位——一边是「**用 API 即可获得的能力**」，另一边是「**自托管时需要自行实现的能力**」。这构成 Agent 工程师的核心决策框架：**用 Anthropic API 还是自托管？** 本文 + Project 给出了完整的对位视图。

## 对 Agent 工程师的行动建议

1. **立即评估 Code Execution Tool**：50 小时/天免费配额意味着可以**零成本试运行**大量数据分析和文档处理 Agent 工作流
2. **MCP Connector 降低接入门槛**：之前因 MCP 客户端复杂度放弃的项目可以**重新评估**——URL + API Key 即可接入
3. **Files API 重构长任务 Agent 架构**：不再需要为「跨会话文件存储」自建对象存储 + ID 生成 + 清理逻辑
4. **1 小时缓存解锁新场景**：长会话协作、跨小时任务、增量更新型 Agent 都是新机会

## 参考

- 原文：[New capabilities for building agents on the Anthropic API](https://claude.com/blog/agent-capabilities-api)
- [Anthropic Engineering: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Cloudflare Sandboxes GA](https://blog.cloudflare.com/sandboxes-ga/)
- [Claude Managed Agents Memory](https://claude.com/blog/claude-managed-agents-memory)
- [LangSmith Sandboxes: Every Agent Needs A Computer](https://docs.smith.langchain.com/concepts/sandbox)
- [MCP Production Engineering](https://modelcontextprotocol.io/docs/)
