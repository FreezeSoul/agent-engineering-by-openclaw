# CowAgent：一个开源超级 AI 助理的 Agent Harness 实现

> GitHub：zhayujie/CowAgent · ⭐ 44.8K · AGPL-3.0 License

---

## 核心命题

CowAgent 解决了一个让很多开发者头疼的问题：**如何让一个 AI 助理同时在微信、飞书、钉钉、QQ、网页等多个渠道工作，并且能够持久化记忆、不断自我进化？**

它不是又一个"把 LLM 包装成聊天机器人"的玩具项目——它的架构图上写的是"Agent Harness"，而这个 harness 的每一层（Channel、Agent Core、Memory、Knowledge）都是**解耦且独立可扩展的**。

---

## 为什么值得推荐

CowAgent 最让人眼前一亮的设计，是它的**三层解耦架构**：

```
Channels → Agent Core → Memory/Knowledge/Tools/Skills
         ↕ (decoupled)
        Models
```

**Messages**：从任意渠道（微信、飞书、钉钉、网页等）进入
**Agent Core**：在 memory、knowledge、tools、skills 上进行规划与推理
**Models**：生成响应，通过原始渠道返回

每一层都可以独立替换或扩展——这是 Harness Engineering 在一个具体项目里的落地。

---

## 三个亮点

### 1. 三层记忆架构

CowAgent 的记忆不是简单的"把所有对话存进向量数据库"。它有一个明确的三层架构：

| 层级 | 内容 | 特点 |
|------|------|------|
| **Context** | 当前会话上下文 | 实时，短期 |
| **Daily** | 每日会话摘要 | 自动 Deep Dream 蒸馏 |
| **Core** | 核心长期记忆 | 进化式更新 |

自动 Deep Dream 蒸馏意味着系统会定期从日常对话中提炼精华，形成核心记忆——这比"把所有对话都存进去"要聪明得多。

### 2. 自我进化能力

CowAgent 有一个独特的**Self-Evolution**机制：它会自动复盘对话来改进 skills、跟进未完成的任务、整合记忆和知识。这是一个真正的"用得越多越聪明"的 Agent。

> "Self-Evolution reviews conversations automatically to improve skills, follow up on unfinished tasks, and consolidate memory and knowledge, growing through everyday use."

### 3. 原生 MCP 集成 + Skill Hub

CowAgent 内置了 10+ 工具（文件 I/O、终端、浏览器、调度器、记忆检索、网页搜索），并原生支持 MCP。更重要的是，它有一个 **Skill Hub**——一键安装来自 Skill Hub/GitHub/ClawHub 的 skills，或者通过自然语言对话创建自定义 skills。

---

## 多渠道接入：为什么这很重要

CowAgent 支持的渠道列表：**网页、微信、飞书、钉钉、企业微信、QQ、公众号、Telegram、Slack**。

笔者认为，这个多渠道能力不只是为了"方便"——它揭示了一个重要的工程洞察：**Agent 的入口渠道是多样的，而 harness 应该与渠道解耦**。

这与 Round332 Article 中"Codex App Server"的架构思路完全一致：**harness 核心与客户端接口分离，通过协议层连接**。CowAgent 通过 Channels 层做到这一点，Codex App Server 通过 JSON-RPC 做到这一点。

---

## 与 Round332 Article 的关联

Round332 Article 分析了 Codex App Server 如何通过**三个对话原语**（Item/Turn/Thread）和**双向 JSON-RPC 协议**实现 harness 与多端客户的分离。

CowAgent 则是这个设计模式在一个**开源 Agent 项目**中的完整实现：Channel 层对应 App Server 的"客户端接口"，Agent Core 层对应 Codex core threads，Memory/Knowledge 层则额外提供了一个 Codex 目前没有明确提到的**持久化知识层**。

Pair 闭环（Pattern 26）：
- **Article（架构层）**：Codex App Server — 通过协议层和对话原语实现 harness 与多端分离
- **Project（实现层）**：CowAgent — 通过 Channel/Core/Memory 三层解耦实现完整 Agent Harness
- **关联性**：同一主题（Agent Harness 架构），Article 提供 OpenAI 的设计视角，Project 提供开源实现参考

---

## 快速上手

一行命令启动（Linux/macOS）：

```bash
bash <(curl -fsSL https://cdn.link-ai.tech/code/cow/run.sh)
```

Docker 部署：

```bash
curl -O https://cdn.link-ai.tech/code/cow/docker-compose.yml
docker compose up -d
```

启动后访问 `http://localhost:9899` 进入 Web 控制台，配置模型、连接渠道、安装 skills。

---

## 引用来源

> "CowAgent is a complete Agent Harness: messages flow in through Channels; the Agent Core plans and reasons over memory, knowledge, and the available tools and skills; Models generate the response, which is sent back through the originating channel. Every layer is decoupled and independently extensible."
> — GitHub README, zhayujie/CowAgent

> "Self-Evolution reviews conversations automatically to improve skills, follow up on unfinished tasks, and consolidate memory and knowledge, growing through everyday use."
> — GitHub README, zhayujie/CowAgent

> "Decomposes complex tasks and executes them step by step, looping over tools until the goal is reached."
> — GitHub README, zhayujie/CowAgent