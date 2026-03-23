# Deloitte: AI Agent Orchestration 企业落地指南

> 来源：Deloitte
> 评分：4/5（实践 4 / 独特 4 / 质量 4）
> 关联 FSIO 文章：智能体设计思考（二）：九大开源项目的架构实践与设计模式

## 行业预测

Gartner 预测：2028 年 33% 企业软件将包含 agentic AI（2024 年不足 1%），15% 日常工作决策将由 AI Agent 自主做出。

## 多 Agent 成功的三个指导原则

### 1. 灵活、可扩展、安全的通信协议

**现状**：多个 Agent 间协议正在涌现：
- Google A2A
- Cisco AGNTCY
- Anthropic MCP
- IBM ACP

**竞争风险**：可能形成"围墙花园"，公司被锁定在单一协议生态。

**预测**：明年这些协议将开始收敛，形成 2-3 个主导标准。

**关键参数**：
- 轻量协议 + 标准 API + 测试工具
- P2P 和 hub-and-spoke 支持
- Agent 注册表、异步消息、高吞吐低延迟
- 认证、安全消息、访问控制

### 2. 管理平台和可观测性工具

**Supervisor Agents**：解释请求、路由任务、授予和管理访问、执行并行/多步骤流程。

**Emerging：Guardian Agent**
- 拥有任务
- 监管其他 Agent
- 感知和管理风险行为

**监管合规**：EU AI Act 要求风险评估、透明度、技术保障、人工监督。

### 3. 业务流程和劳动力变革

**人类角色**：
- "Agent boss"（ Agent 老板）
- 或与 Agent 并肩工作

**数据**：86% CHRO 将数字劳动力整合视为核心职责。

## 多 Agent 模式

| 模式 | 说明 |
|------|------|
| Sequential | 一个 Agent 输出成为下一个输入 |
| Parallel | Agent 并行处理独立任务 |
| Collaborative | Agent 协作迭代优化 |

## 一句话总结

> Deloitte 企业洞察：2028 年 33% 企业软件 Agent 化——协议收敛（2-3 个标准）+ Supervisor/Guardian Agent 监管 + 人类角色转型（Agent boss）。

## 原文

https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html

## 标签

#community #multi-agent #orchestration #enterprise #Deloitte #A2A #MCP
