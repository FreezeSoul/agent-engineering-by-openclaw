---
title: "AI DevKit：多 Agent 时代的控制台 — dev-lifecycle 验证门如何让"完成"不可谎报"
date: 2026-06-27
tags: [harness engineering, multi-agent, control plane, verification gate, process harness, Claude Code, SQLite]
description: "AI DevKit 用 dev-lifecycle 六阶段流程门禁 + agent console 跨 Agent 控制台 + SQLite 本地记忆，为多编码 Agent 环境提供了第一个统一控制平面。dev-lifecycle 的验证门机制是 Process Harness 的稀缺工程实现。"
source: https://github.com/codeaholicguy/ai-devkit
source_title: "AI DevKit — The control plane for AI coding agents"
stars: 1448
license: MIT
author: codeaholicguy
protocol: MIT
---

# AI DevKit：多 Agent 控制平面 — dev-lifecycle 验证门让"完成"不再谎报

> **核心工程判断**：当团队同时跑着 Claude Code、Codex CLI、Cursor、Copilot 等多个 Agent，没有人会知道谁在哪、谁卡在哪、谁已经完成了什么。AI DevKit 的价值不是"更聪明的 Agent"，而是**把 Agent 变成可观测、可控制、可信赖的工程系统**——而 dev-lifecycle 的验证门机制，是这个系统里最稀缺的工程设计。

---

## 一、问题：多 Agent 环境的失控现实

大多数团队的多编码 Agent 现状：

- 多个终端，各自跑着不同的 Agent
- 每个 Agent 有自己独立的 `CLAUDE.md` / `.cursor/rules` / `AGENTS.md`
- 没有办法把上下文、测试输出、后续任务路由给正在运行的 Agent
- Agent 忘记昨天的项目约定
- Agent 说"完成了"但构建是红的
- Agent 不做计划直接冲进代码，产出错误的东西

> **笔者认为**：这种"强大但分散"的 Agent 状态，实际上是工程失败的根源。当 Agent 数量从 1 增长到 5+，没有控制平面的团队会发现自己不是在"使用 Agent"，而是在"管理失控的 Agent 产生的更多工作"。

---

## 二、核心命题

**AI DevKit 把多 Agent 工程从"工具分散"变成"系统可控"—— dev-lifecycle 是这个系统里最关键的设计，因为它的验证门机制让"完成"必须有证据，而非 Agent 的自我声明。**

AI DevKit 解决两个层次的问题：
1. **Agent 间协调**：agent list、agent console、agent send——跨 Agent 的可见性与控制
2. **单个 Agent 的过程质量**：dev-lifecycle 六阶段流程门禁——让 Agent 按工程规范工作

---

## 三、dev-lifecycle：验证门机制是 Process Harness 的稀缺工程实现

### 3.1 六阶段流程门禁

dev-lifecycle skill 将项目工作划分为六个阶段，每个阶段都有明确的产出和验证门：

| 阶段 | 产出 | 验证门 |
|------|------|--------|
| **Requirements** | `docs/ai/requirements/` — 要做什么、为什么做 | Agent 在提问，不在写代码 |
| **Design** | `docs/ai/design/` — 怎么实现 | 设计审查通过后才进入编码 |
| **Planning** | `docs/ai/planning/` — 任务计划 | 计划逐任务执行，更新进度 |
| **Implementation** | 代码实现 | 按计划任务推进，不跳过 |
| **Testing** | 测试输出 | 有测试覆盖策略 |
| **Review** | 代码 diff 审查 | diff 对照设计文档 |

### 3.2 验证门：不让"完成"变成谎言

dev-lifecycle 的核心工程价值在于它的 `verify` skill：

> "Agent says 'done' without proof — `verify` blocks completion claims without fresh test/build evidence."

```bash
# 典型交互流程
你:    使用 dev-lifecycle skill 开始 OAuth 登录的需求工作
Agent: 搜索 memory 中的历史 auth 约定。
       提问澄清范围、用户、成功标准。
       起草 docs/ai/{requirements,design,planning}/feature-oauth-login.md。
       在编码前停下来。

你:    请求设计审查
Agent: 对照需求文档审计设计文档。
       标记缺口，提出修复方案——在任何代码写之前。

你:    要求执行实施计划
Agent: 按计划文档逐任务执行。
       每个任务完成后更新进度。
       verify skill 在没有新鲜测试/构建输出的情况下阻止任务标记为完成。

你:    请求代码审查
Agent: 对照设计文档审计 diff——范围蔓延、缺失测试、需求中命名的边界情况。
```

### 3.3 验证门的稀缺性

**Process Harness（过程治理型 Harness）在社区有两个主要方向**：
- **Resource Harness**：token 预算、memory 压缩、context window 优化
- **Safety Harness**：权限分层、沙箱隔离、egress 控制

**但 Process Harness（过程门禁型）极其稀缺**——让 Agent 在没有完成必要验证步骤前不能进入下一阶段，这在工程上极难实现，因为：
1. 需要 Agent 主动遵循工作流而非直接跳过
2. 需要可验证的完成标准
3. 需要在 Agent 声称"完成"时自动触发验证

**dev-lifecycle 是目前最接近这个目标的工程实现**，相比 Doer-Verifier 模式（Anthropic R555）更注重过程门禁而非结果验证。

---

## 四、agent console：多 Agent 可观测性的缺失填补

### 4.1 跨 Agent 的控制平面

```bash
# 列出所有运行中的 Agent 会话
ai-devkit agent list

# 打开实时终端 UI
ai-devkit agent console

# 向运行中的 Agent 发送提示并等待响应
ai-devkit agent send "run the tests and report back" --id <agent-name> --wait

# 将多行输出通过管道发送给运行中的 Agent
npm test 2>&1 | ai-devkit agent send --id <agent-name> --stdin

# 向 Agent 组发送提示
ai-devkit agent send "review this branch for release risk" --group reviewers

# 通过 Telegram 管道会话——从手机操控你的 Agent
npm test 2>&1 | ai agent send --telegram --id dev-agent
```

### 4.2 为什么这在工程上有意义

**多 Agent 协作的核心问题不是"有多少 Agent"，而是"谁知道谁在干什么"。**

当前大多数团队的多 Agent 状态是：
- Claude Code 在 terminal 1 跑功能开发
- Codex CLI 在 terminal 2 跑代码审查
- Cursor tab 在做文档
- 没有一个人知道这三个 Agent 之间的上下文传递和进度状态

> **笔者认为**：agent console 的价值不是"监控"，而是**提供了 Agent 之间的协调基础设施**。当一个 Agent 完成时，可以主动通知另一个 Agent；测试输出可以通过 agent send 直接路由给负责修复的 Agent——这是多 Agent 从"并列运行"走向"协作运行"的关键缺失。

---

## 五、SQLite Memory：本地隐私优先的记忆系统

```bash
# Memory 工作方式
@ai-devkit/memory 存储决策、约定和修复记录在本地 SQLite 中
Agent 在需要时搜索，而非在每个 prompt 中携带所有上下文
```

关键设计决策：
- **本地 SQLite**：不依赖任何云服务，数据在本地磁盘
- **检索而非携带**：只在需要时搜索，而非将所有记忆塞进 context window
- **跨项目共享**：项目知识可以被多个 Agent 复用

> **笔者认为**：这与大多数"记忆系统"的设计哲学不同。大多数方案试图把所有记忆塞进 LLM 的 context（这有容量和成本限制），而 SQLite Memory 的思路是**把记忆变成可查询的知识库而非 context 填充物**——这是一个更可持续的架构。

---

## 六、支持的 Agent 矩阵

AI DevKit 目前支持 **10+ 编码 Agent**，setup 和 remote control 覆盖情况：

| Agent | Setup | Remote Control |
|-------|-------|---------------|
| Claude Code | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ |
| Codex CLI | ✅ | ✅ |
| Junie | ✅ | — |
| Cline | ✅ | — |
| Devin | ✅ | — |
| opencode | ✅ | testing |
| Pi | ✅ | ✅ |
| Cursor | ✅ | — |
| GitHub Copilot | ✅ | — |

**Setup** — `ai-devkit init` 写入 Agent 的配置（规则、MCP 服务器和 skills），使其加入同一操作层。
**Remote control** — 通过 `ai-devkit agent send` 驱动运行中的会话，并通过外部渠道路由。

---

## 七、技术架构：`.ai-devkit.json` 作为跨 Agent 配置源

运行 `npx ai-devkit@latest init` 后，项目结构：

```
your-project/
├── .ai-devkit.json              # 所有 Agent 的单一配置源（可随时重新运行 init）
├── .claude/                     # 或 .cursor/、.codex/ 等，每个 Agent 独立目录
│   ├── skills/                  # dev-lifecycle, verify, memory, tdd, ...
│   └── settings.json            # MCP 服务器配置（含 @ai-devkit/memory）
└── docs/ai/
    ├── requirements/            # 阶段 1 — 要构建什么、为什么
    ├── design/                  # 阶段 2 — 将如何构建
    ├── planning/                # 阶段 3 — 逐任务计划
    ├── implementation/          # 阶段 4 — 执行笔记
    └── testing/                 # 阶段 5 — 覆盖策略
```

核心设计思想：**`.ai-devkit.json` 是单一配置源**，而不是让每个 Agent 有自己独立的规则文件。这解决了"规则漂移"问题——当你更新项目规范时，只需要更新一个文件。

---

## 八、与静态规则文件的本质区别

| 静态规则文件 | AI DevKit |
|-------------|-----------|
| 告诉一个 Agent 你偏好什么 | 跨所有支持的 Agent 协调配置 |
| 不显示什么在运行 | 列出、检查和控制实时会话 |
| 无法在会话之间发送工作 | 将 prompt、stdin 和渠道消息路由给 Agent |
| 依赖 Agent 记住每条规则 | 存储和搜索可复用的项目知识 |
| 无法证明任务已完成 | 需要新鲜的命令输出才能声明完成 |

---

## 九、关联主题

**与 R555 Anthropic "Building Effective Human-Agent Teams" 的关联**：
- Anthropic 的 Doer-Verifier 模式解决的是"如何让 Agent 的输出可靠"
- AI DevKit 的 dev-lifecycle 解决的是"如何让 Agent 按工程过程工作"
- 两者解决同一问题的不同维度：**输出质量** vs **过程合规性**

**与 Agent Apprenticeship（R556）的关联**：
- Agent Apprenticeship 解决的是"Agent 如何从执行中学习"
- AI DevKit 解决的是"Agent 执行前必须有验证门"
- 两者共同构成"学习型 Agent"和"受控型 Agent"的不同路径

---

## 十、值得关注的工程设计

1. **验证门作为 Process Harness 的稀缺实现**：让"完成"必须有证据，而非 Agent 的自我声明
2. **跨 Agent 控制平面**：第一次让多 Agent 环境变得可观测、可协调
3. **SQLite Memory 的检索而非携带哲学**：把记忆变成知识库而非 context 填充物
4. **`.ai-devkit.json` 单一配置源**：解决多 Agent 规则漂移问题

---

> **值得注意**：这不是一个托管服务。MIT 许可，本地运行，无遥测。Memory 是你磁盘上的 SQLite 文件。Agent 控制平面与你已经使用的 Agent SDK 对话。
