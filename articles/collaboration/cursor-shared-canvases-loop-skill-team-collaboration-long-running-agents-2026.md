# Cursor Shared Canvases 与 /loop Skill：团队协作与长时 Agent 的产品化

## 核心论点

**Cursor 在 2026 年 5 月推出的 Shared Canvases 和 /loop Skill，代表了 AI Coding Agent 从「个人效率工具」向「团队协作节点」和产品化的关键演进——Canvas 提供可分享的交互 Artifact，/loop 实现本地化的定时/条件触发长时 Agent。**

---

## Shared Canvases：Agent Artifact 的团队可见性

### 什么是 Canvas

Canvas 是 Cursor Agent 在工作过程中创建的交互式产物——报告、仪表板、自定义界面等。与传统 Chat 模式下的会话记录不同，Canvas 是 Agent 产出物的「快照」，具备独立可分享性。

### 团队协作价值

通过 Shared Canvases，开发者可以将 Agent 生成的 Artifact 分享给团队成员，接收方获得只读访问权限。这意味着：

- **知识传递**：Agent 的分析结果可以直接分享，而非截屏或复制粘贴
- **可审计性**：每一次分享都是对 Agent 产出的显式认可
- **协作起点**：团队成员可以在共享 Artifact 基础上继续迭代

### 可用性

Shared Canvases 在 Cursor Pro、Teams 和 Enterprise 计划中可用。

## /loop Skill：本地长时 Agent 的条件触发机制

### 核心功能

/loop 是 Cursor 的一个内置 Skill，允许用户定义一个提示词，让 Agent 按固定间隔重复执行，或持续运行直到达成某个目标，或者手动停止。

### 使用场景

- **监控场景**：「每 5 分钟检查一次部署状态」
- **迭代场景**：「持续优化这个功能，直到测试通过」
- **长时任务**：「处理这个任务，中间有进展随时汇报」

### 技术意义

/loop 实现了「本地化的定时 Agent 触发」，这在传统上需要外部调度系统（如 cron + Claude Code CLI）或云端服务才能实现。Cursor 将其产品化为一个 Skill，降低了长时 Agent 的使用门槛。

## 两条演进线的交汇

Shared Canvases 和 /loop 代表了 Cursor 的两个产品维度：

| 维度 | 功能 | 解决的问题 |
|------|------|-----------|
| **协作** | Shared Canvases | Agent 产出如何在团队中流通 |
| **自主** | /loop Skill | Agent 如何在无人值守情况下持续工作 |

两者共同指向一个更大的目标：让 AI Coding Agent 从「被人类调用的工具」进化为「可以独立运行、产出可分享、状态可追溯的团队成员」。

## 与仓库中其他文章的关联

- **长时 Agent**：[anthropic-effective-harnesses-for-long-running-agents](./harness/anthropic-effective-harnesses-for-long-running-agents-2026.md) — /loop 是「 Harness 设计」的产品化实现
- **团队协作**：[cursor-continually-improving-agent-harness-measurement-driven](./harness/cursor-continually-improving-agent-harness-measurement-driven-2026.md) — 持续改进 Agent 基础设施的思路
- **Artifact 共享**：[cursor-canvas-agent-visualization-ui-paradigm-2026.md](./context-memory/cursor-canvas-agent-visualization-ui-paradigm-2026.md) — Canvas 作为 Agent 可视化 UI 范式的早期论述

---

**来源**：https://cursor.com/changelog/shared-canvases

**关联 Article**：[Cursor Auto-review Run Mode](./cursor-auto-review-run-mode-three-layer-security-filter-2026.md) — 同批次发布的两个重要功能更新