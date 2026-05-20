# NousResearch/hermes-agent：唯一内置学习循环的自改进 Agent 框架

> **核心判断**：Hermes Agent 解决了一个所有长时运行 Agent 都面临的根本矛盾——如何在多会话中持续积累经验而非每次从零开始。它不只是一个 Chatbot 替代品，而是第一个真正把「从经验中学习」工程化为内置能力的 Agent 运行时。与 Anthropic 的 Generator-Evaluator 架构形成互补：Anthropic 解决的是单次任务内的质量控制，Hermes 解决的是跨会话的知识固化。

---

## 核心命题

当你用 Claude Code 或 Cursor 处理一个复杂项目时，每次新的对话都是一个独立的起点——之前的经验、教训、偏好都不会自动携带。但 Hermes Agent 的设计者 Nous Research 问了一个更根本的问题：

> "It's the only agent with a built-in learning loop — it **creates skills from experience**, **improves them during use**, **nudges itself to persist knowledge**, **searches its own past conversations**, and **builds a deepening model of who you are** across sessions."

这个描述里的每一个动词——creates、improves、nudges、searches、builds——都是主动的、持续的行为，不是响应式调用。这让 Hermes 区别于所有「每次对话后即遗忘」的传统 Agent 实现。

---

## 为什么它值得关注

### 1. 自改进的学习循环

这是 Hermes 区别于所有竞品的核心标签。官方文档描述了这个循环的具体机制：

> "Agent-curated memory with **periodic nudges**. **Autonomous skill creation** after complex tasks. **Skills self-improve during use**. FTS5 session search with LLM summarization for cross-session recall."

这不是 RAG（检索增强生成）的简单包装——它是把「从经验中提取模式并固化为可复用技能」做成了自动化循环。对比 Anthropic 三 Agent 架构里的 Evaluator 驱动迭代，Hermes 的学习循环更接近于：Agent 自己同时是 Generator、Evaluator 和 Skill Curator。

### 2. 真正的多平台统一

> "Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from **Telegram while it works on a cloud VM**."

支持的平台：Telegram、Discord、Slack、WhatsApp、Signal、Email、CLI。七端统一，这意味着你可以在手机上发一条消息驱动一个跑在云端的 Agent 完成任务。这与 Anthropic 描述的「长时 Agent 需要独立开发环境」的思路一致——但 Hermes 走得更远：Agent 本身就可以跨设备、跨平台运行。

### 3. 模型无关性（Model Agnostic）

> "Use any model you want — Nous Portal, OpenRouter (200+ models), NovitaAI, NVIDIA NIM, Xiaomi MiMo, z.ai/GLM, Kimi/Moonshot, MiniMax, Hugging Face, OpenAI, or your own endpoint. Switch with `hermes model` — no code changes, no lock-in."

200+ 模型支持，这在主流 Agent 框架中是罕见的灵活度。特别是对中文用户，直接支持 MiniMax 和 Kimi/Moonshot，意味着可以绕过 OpenAI API 的地域限制和定价问题。

### 4. OpenClaw 迁移工具

> "If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys."

这个细节揭示了 Hermes 的真实定位——它不只是另一个开源项目，而是 OpenClaw 的实际继承者。考虑到 OpenClaw（现名）在 GitHub 上已有 370K+ Stars，Hermes 的 OpenClaw 迁移工具意味着它正在吸收 OpenClaw 的用户生态。

### 5. 生产级的工具深度

40+ 内置工具、内置 MCP 集成、7 种终端后端（本地/Docker/SSH/Singularity/Modal/Daytona/Vercel Sandbox）、批量轨迹生成……这些不是实验性功能，而是完整生产级 Agent 运行的标配。

---

## 技术架构简析

Hermes 的架构有几个值得关注的工程选择：

**Skill System**：不只是记忆，是把经验固化为可调用的 Skill。这与 Anthropic 文章中的「Evaluator 给出具体改进意见驱动 Generator 迭代」思路一脉相承，但 Hermes 把这个过程自动化了——Agent 自己判断何时需要创建新 Skill。

**FTS5 Session Search**：基于 SQLite FTS5 的全文搜索，配合 LLM summarization，支持跨会话信息召回。这是持久化记忆的具体实现方式。

**7 种终端后端**：Daytona 和 Modal 提供 serverless 持久化——Agent 环境在空闲时休眠，按需唤醒，几乎零空闲成本。这意味着 Hermes Agent 可以真正「跑在云上」而不需要保持常驻进程。

**OpenClaw Migration**：完整导入 SOUL.md、MEMORY.md、Skills、API keys……这个迁移路径的完备性说明项目方对 OpenClaw 用户的迁移体验是认真的。

---

## 竞品对比

| 维度 | Hermes Agent | OpenClaw | LangChain Agents |
|------|-------------|----------|-----------------|
| 自改进学习循环 | ✅ 原生内置 | ❌ | ❌ |
| 多平台（IM） | ✅ 7个平台 | 部分支持 | ❌ |
| 模型无关性 | ✅ 200+ 模型 | ✅ | ✅ |
| 内置 Skill 系统 | ✅ | ❌ | 部分 |
| OpenClaw 迁移 | ✅ | N/A | ❌ |
| Serverless 部署 | ✅ Modal/Daytona | ❌ | ❌ |

---

## 适用场景

✅ **需要跨会话持续学习的复杂项目**：如果你需要在多天甚至数周内持续推进一个项目，Hermes 的内置记忆和学习循环比每次新建对话高效得多。

✅ **多平台协作**：在 Telegram 上发起任务，在云端 VM 上执行，结果推送到 Discord——这种跨平台体验目前没有竞品能提供同等完整度。

✅ **从 OpenClaw 迁移**：370K Stars 的 OpenClaw 用户现在有了官方迁移路径，包括记忆、Skill 和 API 配置的完整导入。

✅ **模型灵活性要求高**：需要混用多个模型提供商，或对成本敏感（支持 MiniMax 等低成本模型）。

❌ **单次任务、快速问答**：如果只是需要一次性的代码片段或问答，Hermes 的安装和学习成本不划算。

❌ **极简主义用户**：它有 40+ 工具、7 种后端、复杂的 Skill 系统——如果只想用最简单的方式跑一个 Agent，这不是最佳选择。

---

## 快速上手

```bash
# Linux/macOS/WSL2 一行安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 启动对话
hermes

# 选择模型
hermes model

# 从 OpenClaw 迁移
hermes claw migrate
```

---

原文链接：[NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent)（GitHub, 158,501 Stars, MIT License）

> "It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions." — Nous Research