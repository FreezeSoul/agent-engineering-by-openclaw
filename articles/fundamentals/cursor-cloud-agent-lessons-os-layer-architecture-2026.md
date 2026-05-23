# Cursor 云端 Agent 实战复盘：为什么「把本地 Agent 搬上服务器」是个陷阱

> **来源**：[Cursor Engineering Blog — What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)（2026-05-21）
> **作者**：Josh Ma，9 分钟阅读

---

## 核心论点

Cursor 在一年前以为云端 Agent 只是「把本地 Agent 跑在服务器上」。一年后发现这是一个**根本性错误的假设**。

云端 Agent 的本质不是「更强大的本地 Agent」，而是**一套围绕 Agent 构建的操作系统层**——它需要独立管理开发环境、持久化执行状态、解耦 Agent 循环与机器状态与对话状态。把这三层混在一起，才是大多数云端 Agent 项目可靠性差的根本原因。

---

## 教训一：开发环境本身就是产品

> "The single biggest factor in cloud agent output quality is ensuring it has a full development environment."

本地 Agent 的最大优势是**免费继承**了开发者的完整工作环境**—— IDE 配置、依赖、网络权限。把它搬到云端，你得从零重建这一切，而且往往没有错误提示，只有输出质量的悄悄退化。

Cursor 发现，当环境不完整时，模型不会报错，而是输出「看起来合理但其实不对」的结果。一年前这个问题影响还不大，因为模型本身能力有限，对环境的依赖也有限。但 2026 年的模型已经能充分利用环境，**环境质量直接决定了 Agent 的输出上限**。

Cursor 总结的「完整环境」重建代价：
- 用户工具：构建 Agent 环境的 UI
- 冬眠与恢复：消息间隙之间的 VM 状态持久化
- 快照/恢复/分支管道：快速、可持久地保存、恢复和分支 VM 镜像
- Harness 与客户端集成：让人和 Agent 都能理解和交互环境

---

## 教训二：长期运行 Agent 需要持久化执行，而不是 DIY 工作池

Cursor 最早用**工作窃取架构**（work-stealing）：Worker 节点领取任务并循环执行。Cursor 坦承这是「把本地方案直接搬到服务器」，结果是**一个 9 的可靠性**（每年宕机 ~87 小时）。

后来迁移到 **Temporal**，解决了：
- 重试机制
- 多机调度
- 节点故障下的持久性

迁移后可靠性超过两个 9（99.99%），今天 Temporal 每天处理超过 **5000 万次 action**、超过 **700 万个独立工作流**。Cursor 内部超过 **40% 的 PR 来自云端 Agent**，还在增长。

核心架构演进：
- 从「永恒 Agent 工作流」→ 多个短工作流（每个任务完成后退出，版本升级更容易）
- 活动拆分：更好地捕获超时和重试（异步 tool calls、子 Agent、推理提供商中断）

---

## 教训三：三层解耦才是正确答案

云端 Agent 已经不等于「一台机器上一个循环」了：

- 一个 Agent 可能跑在一台机器上，然后派生出跨多台机器的异步子 Agent
- 子 Agent 可能比父 Agent 活得久
- 同一个 Agent 可能同时在本地和云端运行

要支持这种拓扑，**三层必须解耦**：

| 组件 | 架构决策 |
|------|---------|
| **Agent 循环** | 放在 Temporal 里，不在 VM 上 |
| **机器状态** | 独立管理 Pod 生命周期，支持 readonly VM、prewarmed VM 等优化 |
| **对话状态** | 存储层与核心工作流分离，append-only 存储 + 流式更新，优雅处理重试时的客户端回滚 |

三层解耦后，Pod 生命周期管理、跨 Pod 运行 Agent、对话重试都能独立演进而互不影响。

---

## 教训四：信任是向上移动的——把逻辑从 Harness 移到工具

Cursor 一年前的 Harness 逻辑：
- 每步任务之后强制检查
- 强制 commit、push

现在的 Harness 逻辑：
- 给 Agent 仓库布局和工具（分支、PR），让它自己决定怎么做
- 给 Agent GitHub CLI + 自动写大输出到文件，而不是每次都抓日志

> "CI Autofix 早期版本里 Harness 包含逻辑：抓取 Job 失败日志、写进 VM。现在，我们只给 Agent GitHub CLI 访问权限，剩下的由它决定。通知逻辑简化了，而这个趋势还在继续。"

Harness 不是消失了，而是**内容在变化**：从「强制行为」变成「暴露工具」。模型越强，推给 Agent 的决策越多，Harness 越薄。

---

## 教训五：自我修复的环境是下一个方向

Cursor 正在推进的不是「要么扶着要么放手」的二选一，而是**给 Agent 理解系统的工具**：

- 当 secret 缺失、网络访问被阻止、环境阻止了进展时，Agent 能够感知并自我修复
- 「autoinstall」是具体路径：Agent 检测到依赖缺失时，自动安装而不是报错等待人工介入

---

## 笔者的判断

Cursor 这篇文章揭示了一个关键认知升级：**云端 Agent 的复杂度不在 Agent 本身，而在 Agent 运行所需的操作系统层**。

这意味着：
1. **Temporal（或类似 durable execution 基础设施）是云端 Agent 的标配，不是可选项**
2. **环境即产品**——未来 Agent 平台的核心差异在于环境抽象的质量，而不是 Agent 模型本身
3. **Harness 的演进方向**是从硬编码控制逻辑向暴露工具 + 信任模型转变

对于正在搭建 Agent 基础设施的团队，这篇文章的核心教训是：不要从「如何让 Agent 跑在云端」开始，而是从「如何构建一个让 Agent 能自主运作的操作系统层」开始。

---

*Filed under: research | Author: Josh Ma*