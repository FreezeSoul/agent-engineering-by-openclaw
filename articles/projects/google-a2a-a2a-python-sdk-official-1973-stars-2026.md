# google-a2a/a2a-python：A2A 协议的官方 Python SDK

## 核心命题

A2A（Agent-to-Agent）协议要解决的核心问题，不是「如何让两个 Agent 互相通信」，而是**如何让两个由不同公司、用不同框架、在不同基础设施上构建的 Agent，能够在没有私有集成代码的前提下实现互操作**。这个问题在 2026 年的多 Agent 生态里变得越来越尖锐——Notion 的 Provider-Agnostic Harness 选择 Cursor，就是因为没有一个标准协议层能让不同 Agent 引擎无缝插入。A2A 协议，正在成为这个标准层的候选。

## GitHub

```
https://github.com/google-a2a/a2a-python
Stars: 1,973 | Language: Python | License: Apache 2.0
```

## 为什么这个项目值得关注

### 1. 官方的意义

这不是社区实现，是 **Google 官方的 A2A Protocol SDK**。协议规范本身是 [a2a-protocol.org](https://a2a-protocol.org) 维护的开放标准，但 Python SDK 是 Google 发布并维护的。这意味着：

- 协议规范和 SDK 实现之间有直接的一致性保证
- Google 内部在用（Google 的 Agent 产品线是 A2A 的主要用户）
- 长期维护有背书，不会有「作者跑路」风险

> 笔者认为，在 Agent 协议这个领域，「官方」和「社区」的区别比一般开源项目更大。协议一旦成为系统间的契约，提供商的背书直接影响企业的选型信心——这是为什么 Anthropic 的 MCP SDK 和 OpenAI 的 Agents SDK 虽然也是「开源」，但本质上都是各自官方的协议实现。

### 2. 多版本兼容：A2A v1.0 和 v0.3

```
Spec Version | Transport        | Client | Server
-------------|-----------------|--------|-------
1.0          | JSON-RPC        | ✅      | ✅
1.0          | HTTP+JSON/REST  | ✅      | ✅
1.0          | gRPC            | ✅      | ✅
0.3 (compat) | JSON-RPC        | ✅      | ✅
0.3 (compat) | HTTP+JSON/REST  | ✅      | ✅
0.3 (compat) | gRPC            | ✅      | ✅
```

这是 SDK 里最实用的设计细节之一：**A2A v0.3 → v1.0 的平滑迁移路径**。很多企业的 A2A 集成从 v0.3 开始，现在可以渐进升级到 v1.0，而不需要一次性重写全部通信层。

### 3. 传输层可替换：HTTP/gRPC 的选择自由

A2A Python SDK 支持三种传输层，开发者可以根据场景选择：

| 传输层 | 适用场景 | 特点 |
|--------|---------|------|
| **HTTP+JSON/REST** | 通用场景、跨语言调用 | 最通用，调试友好 |
| **JSON-RPC** | 需要严格消息格式的场景 | 有更强的类型保证 |
| **gRPC** | 高性能内部通信、低延迟 | 需要 protobuf 定义，但性能最优 |

> 笔者认为，这个设计体现了 Google 在分布式系统领域的一贯工程哲学：**把「传输协议」和「应用协议」分离**。A2A 协议本身定义的是 Agent 之间的消息语义（任务下发、状态同步、结果返回），而传输层是可选的实现细节。对于大多数场景 HTTP/REST 足够了，但对于内部高性能多 Agent 系统，gRPC 是更合理的选择。

### 4. 与 Notion Cursor SDK 案例的关联

这个项目推荐和本轮 Article（Notion Cursor SDK Provider-Agnostic Harness）是同一主题的两个切面：

**Article** 分析的是：产品公司如何用 Cursor SDK 构建 Provider-Agnostic Harness，把外部 Agent 引擎嵌入自己的产品

**Project** 推荐的是：A2A 协议作为这个场景下缺失的标准协议层，让「用外部 Agent」变成一个可插拔的标准行为，而不是定制集成

Notion 在 2026 年 6 月实现了 Cursor 的「thin adapter」，但这个 thin adapter 是 Notion 自己写的。如果 A2A 协议足够成熟，未来的 thin adapter 可以变成「插上 A2A-compatible Agent 就能用」——一个 Notion 可以换掉 Cursor、Anthropic 可以换掉 OpenAI 的标准层。

这就是 A2A 协议的核心价值：**它不是让 Agent 通信更方便，它是在定义 Agent 互操作的抽象接口层**。

### 5. 集成生态的完整性

```
安装单元              | 命令
---------------------|--------------------------------
Core SDK             | uv add a2a-sdk
All Extras           | uv add "a2a-sdk[all]"
HTTP Server          | uv add "a2a-sdk[http-server]"
FastAPI Integration  | uv add "a2a-sdk[fastapi]"
gRPC Support         | uv add "a2a-sdk[grpc]"
OpenTelemetry        | uv add "a2a-sdk[telemetry]"
Encryption           | uv add "a2a-sdk[encryption]"
PostgreSQL           | uv add "a2a-sdk[postgresql]"
MySQL                | uv add "a2a-sdk[mysql]"
SQLite               | uv add "a2a-sdk[sqlite]"
```

FastAPI 集成是最实用的一个组合——FastAPI 已经是 Python Agent 服务的主流框架，A2A SDK 的 FastAPI 集成让现有的 Agent 服务天然具备 A2A 通信能力，不需要额外的适配层。

## 如何快速跑起来

```bash
# 安装
uv add a2a-sdk

# 克隆示例
git clone https://github.com/a2aproject/a2a-samples.git
cd a2a-samples/samples/python/agents/helloworld

# 终端 1：运行 Agent
uv run .

# 终端 2：运行客户端
cd a2a-samples/samples/python/agents/helloworld
uv run test_client.py
```

## 适合谁用

✅ **正在构建多 Agent 系统的团队**——A2A 让不同 Agent 模块之间的通信变成插拔式的标准层  
✅ **平台型产品**——类似 Notion 的场景，需要把外部 Agent 能力嵌入自己的产品，但不想深度定制  
✅ **企业 AI 基础设施团队**——需要统一管理多个 Agent 系统的互操作，A2A 提供了协议层面的治理框架  

❌ **单 Agent 应用**——A2A 是为多 Agent 场景设计的，单 Agent 不需要  
❌ **强绑定特定框架的团队**——如果你的 Agent 系统完全在 LangChain/CrewAI 生态内，并且不与其他框架通信，A2A 的价值有限

## 一句话总结

A2A Python SDK 是 2026 年多 Agent 互操作协议领域的官方标准实现——如果你在做平台型 Agent 产品或者多 Agent 系统间的集成，A2A 协议层值得认真考虑，而不是从头写私有通信协议。

---

**关联 Article**：[Notion 用 Cursor SDK：产品公司集成外部 Agent 的工程架构](../harness/notion-cursor-sdk-provider-agnostic-harness-integration-2026.md)（Provider-Agnostic Harness 案例）

**相关主题**：
- [[a2a-protocol-one-year-production-retrospective-2026]]（A2A 协议一年生产回顾）
- [[mcp-vs-a2a-enterprise-orchestration-decision-framework-2026]]（MCP vs A2A 企业选型框架）
- [[anthropic-managed-agents-brain-hands-decoupled-architecture-2026]]（Anthropic Brain/Hands 分离架构）
