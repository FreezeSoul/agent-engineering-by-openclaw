# context-infrastructure：让 AI Coding Agent 拥有持久记忆的基础设施层

**来源**: [github.com/grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure)  
**Stars**: 482 | **语言**: Python | **创建时间**: 2026-03-16

---

## 核心问题

AI Coding Agent 的致命弱点：每次会话都是从零开始。上一次对话中建立的上下文、学会的规则、积累的经验，在下次启动时全部消失。

大多数解决方案都是「记忆插件」——把历史消息存起来，塞进下一轮的 context window。但这不是真正的持久化，只是**用 token 换记忆**，既贵又有长度限制。

context-infrastructure 的思路不同：它不是往 context 里塞东西，而是**建立独立于每次会话的基础设施层**。

---

## 核心设计：三层持久化架构

context-infrastructure 实现了三层分离的持久化：

### 1. Personal Rules（规则持久化）

Agent 的行为准则不再依赖每次对话的 prompt，而是存储在独立的规则引擎中。这意味着：

- 团队可以统一管理「代码规范」「项目约定」
- 规则可以版本化、审计、复用
- Agent 每次启动时自动加载，不需要手动注入

### 2. Skills（技能持久化）

Skill 系统让 Agent 的能力可以被积累和复用：

- 学会了一个复杂的工作流，可以固化成可重用的 Skill
- Skill 可以在团队内部分享
- 新成员加入时，继承已有的 Skill 体系，而不是从零学起

### 3. Scheduling（调度持久化）

基于时间的任务调度能力，让 Agent 可以「自己想清楚什么时候做什么」，而不是每次都需要人类触发。

---

## 为什么这对 AI Coding Agent 生态重要

### 从「上下文填充」到「基础设施」

当前大多数 Agent Memory 方案的本质是：**把历史对话当作上下文喂给模型**。这有三个根本问题：

1. **成本高**：每次都要带上前面的所有 token
2. **长度限制**：context window 有上限
3. **检索粗糙**：只能全文检索，无法真正理解记忆

context-infrastructure 的架构把「记忆」从 model context 层抽离出来，变成独立的基础设施。这意味着：

- 记忆的存储和检索可以独立优化（用向量数据库、关系数据库等）
- 模型只需要在需要时获取相关记忆，而不是每次都加载全部
- 记忆可以跨模型、跨工具、跨会话复用

### 与 Cursor SDK 的互补关系

Cursor SDK 提供了「durable state and session management」的云端 runtime，而 context-infrastructure 提供了「persistent context and memory」的基础设施层。两者从不同维度解决同一个问题：

| 维度 | Cursor SDK | context-infrastructure |
|------|-----------|----------------------|
| **解决的问题** | 会话不中断（网络、电源） | 记忆不丢失（跨会话） |
| **持久化对象** | 运行状态 | 上下文、规则、技能 |
| **技术手段** | 云端 VM + 流式恢复 | 独立存储引擎 |
| **层级** | Runtime 层 | 基础设施层 |

两者结合，才是完整的「Agent 持久化」方案。

---

## 技术实现亮点

### 轻量化设计

整个系统用 Python 实现，依赖简洁，可以本地部署。这意味着：

- 不需要把数据放到第三方云服务
- 可以在企业内部网络中运行
- 部署和集成的门槛很低

### 多 Agent 共享

context-infrastructure 支持多个 Agent 共享同一个记忆层。这意味着：

- 团队成员可以共享项目级的上下文
- 不同工具的 Agent（Claude Code、Cursor、Copilot）可以访问同一套记忆
- 团队知识可以被系统化管理，而不只是分散在个人会话中

---

## 核心判断

> **context-infrastructure 代表了一个重要方向：从「用 token 换记忆」转向「独立的基础设施记忆层」。当 Agent 的应用场景从个人工具扩展到团队协作时，这种架构的优势会越来越明显。**