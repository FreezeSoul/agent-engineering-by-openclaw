# code-yeongyu/lazycodex：复杂代码库的单一 Agent Harness

> **核心观点**：LazyCodex 把"复杂代码库的 Agent 执行"做成**单一可装载的 Harness**——把项目记忆、规划、执行、校验完成度全部塞进一个 CLI，给 Claude Code / Codex / oh-my-openagent 等多 Agent客户端共用。736 stars、MIT许可、30 天新发布，标志 Agent Harness范式从"每客户端一套工具"走向"Harness 即基础设施"。

**关联 Article**：[Anthropic Effective Harnesses for Long-Running Agents](../harness/anthropic-effective-harnesses-long-running-agents-2026.md)、[OpenAI Codex Action实践](../projects/openai-codex-action-github-action-1042-stars-2026.md)

---

## 能解决什么问题

当你用 Claude Code 或 Codex 在复杂代码库（多模块、多服务、跨语言）里执行长任务时，通常面临：

- **项目记忆丢失**：每个新会话都要重新解释代码结构、依赖关系、约定
- **规划缺失**：Agent接到任务直接开始改代码，缺少全局规划步骤
- **完成度校验缺失**：任务"看起来跑完"但实际只完成60%，需要人工复核
- **跨客户端重复**：Claude Code 用一套 harness，Codex 用另一套，没有统一的"复杂代码库执行层"

LazyCodex 的答案是：**把这些全部打包成一个 CLI**，让所有 Agent客户端都通过它进入复杂代码库。

---

##关键能力

###1. 项目记忆（Project Memory）

启动时 LazyCodex 自动扫描仓库结构、关键模块、近期变更，构建**持久化的项目级记忆**。后续所有 Agent 调用都基于这份记忆——而不是每次都从零开始读 README。

###2.规划阶段（Planning）

任务进来后，LazyCodex 先做一次**完整的规划输出**（改哪些文件、改动顺序、风险点、回滚路径），然后再交给执行 Agent。避免 Agent 直接动手导致返工。

###3. 执行 +校验完成度（Execution + Verified Completion）

执行过程中 LazyCodex持续跟踪：
-哪些文件已经改完
-哪些断言通过、哪些失败
-整体完成百分比

只有**校验通过100% 完成**，才标记任务 done。否则会列出剩余 work，让 Agent继续。

###4.跨客户端兼容（CLI-First架构）

LazyCodex暴露一个 CLI入口，**任何 Agent客户端都可以调用**：
- Claude Code 通过自定义 skill 调用
- Codex 通过 action 调用
- oh-my-openagent 通过 plugin 调用

这意味着"Harness 不再绑定某个 Agent客户端"——Harness 是基础设施，Agent 是上层应用。

---

## 与 Anthropic Effective Harnesses 的关系

Anthropic 在 [Effective Harnesses for Long-Running Agents](../harness/anthropic-effective-harnesses-long-running-agents-2026.md) 中提出了 Harness 的6 大设计原则：

| Anthropic原则 | LazyCodex 实现 |
|---------------|---------------|
| Structured State Files | ✅ 项目记忆 JSON持久化 |
| Multi-Step Planning | ✅规划阶段先于执行 |
| Checkpointing & Recovery | ✅进度百分比 +剩余 work列表 |
| Verification Loops | ✅ 完成度校验作为门禁 |
| Memory Accumulation | ✅跨会话项目记忆累积 |
| Token Efficiency | ✅复用记忆而非每次重读 |

LazyCodex 是这6原则的**单一 CLI 实现**——把"原则"翻译成"一行命令"。

---

## 与 OpenAI Codex Action 的关系

[OpenAI Codex Action](../projects/openai-codex-action-github-action-1042-stars-2026.md) 把 Codex嵌入 CI/CD（PR 自动审查），LazyCodex走相反路径：把"复杂代码库的 Agent Harness"独立成 CLI，给**所有 Agent客户端**共用。

两者互补：Codex Action解决"自动化 CI集成"，LazyCodex解决"复杂代码库的 Agent交互层"。

---

##适合谁用

- **大代码库团队**（100+ 模块、跨语言）—— 项目记忆价值最大
- **多 Agent客户端环境**（同时用 Claude Code + Codex + 自研 Agent）—— Harness统一层
- **长任务执行场景**（重构、迁移、大特性开发）——规划 +校验门禁价值最大

## 不适合谁用

- **小项目（<10 模块）** —— 项目记忆收益不抵启动开销
- **纯脚本任务** ——规划阶段反而拖慢速度
- **只想用 Claude Code 默认体验** —— LazyCodex 是 CLI拦截层，会改变默认行为

---

## Stars增长曲线

-2026-05-25：项目创建
-2026-06-09（今日）：736 stars
-30 天累计增长：~25 stars/day ——早期高速增长，符合 "新 Harness范式"关注度曲线

---

##标签

- `agent-harness` / `codex` / `claude-code` / `cli`
- `project-memory` / `planning` / `verified-completion`
- `MIT` / `TypeScript`

---

## 来源

- GitHub: https://github.com/code-yeongyu/lazycodex
-736 stars, MIT,2026-05-25 发布
