---
title: "THU-MAIC/OpenMAIC：把多 Agent 编排做成可消费的教育产品，19k Stars 的 LangGraph 实战范本"
date: 2026-07-01
tags: [AI Agent, Multi-Agent, Orchestration, LangGraph, Education, Content Generation, OpenClaw, Next.js, Domain Application, Vertical Agent]
repo: THU-MAIC/OpenMAIC
stars: 19197
forks: 3771
license: MIT
source: github.com/THU-MAIC/OpenMAIC
round: 613
cluster: orchestration
---

# THU-MAIC/OpenMAIC：把多 Agent 编排做成可消费的教育产品，19k Stars 的 LangGraph 实战范本

> 19,197 Stars / 3,771 Forks / 213 Open Issues / 107 Watchers，清华大学 MAIC 实验室 2026-03-11 开源，last push 2026-07-01。OpenMAIC（Open Multi-Agent Interactive Classroom）是少数把「多 Agent 编排」做到 **production-grade、可消费、可分发** 的开源项目——它不只是一个 agent framework，而是一个**端到端产品**：用户输入主题或文档，AI 老师 + AI 同学通过多 Agent 协作生成可交互的课件（slides / quizzes / simulations / games / mind maps / online programming / PBL），并通过 **OpenClaw 集成**直接对接飞书、Slack、Telegram、WhatsApp 等即时通讯平台。

---

## 核心命题

**多 Agent 编排不是研究玩具，是可以做成可消费产品的工程学科**。OpenMAIC 给出的工程范本回答了三个长期悬而未决的问题：

1. **如何把 LLM 的多模态生成能力，编排成「可消费的教学场景」？** —— 不是输出 markdown 文本，而是 7 种交互场景（slides / quiz / simulation / game / mind map / online programming / PBL）的统一 schema
2. **如何让 Agent 主动操作 UI，而不是被动等用户 prompt？** —— AI Teacher 可以主动在 UI 上 highlighting、设置 condition、给 hint、引导注意力（这是大部分 agent 框架完全没碰过的方向）
3. **如何让 Agent 触达 99% 不装 CLI 的非技术用户？** —— 通过 **OpenClaw integration**，用户在飞书/Telegram 直接说「给我做一个 X 主题的课件」，无需打开网页

**范式意义**：OpenMAIC 是第一个把 "Multi-Agent orchestration + 消费级 UI + 即时通讯分发" 这三层打包交付的开源项目。DeerFlow 2.0 (字节跳动, 45k stars) 解决了「小时级任务的 state machine 编排」；HKUDS/Vibe-Trading (15k stars) 解决了「live 资源的 structural 安全闸门」；OpenMAIC 解决了 **「多 Agent 在垂直领域的可消费封装」** —— 三个项目形成了 2026 H2 「Multi-Agent 走向生产」的三条不同路径。

---

## 为什么值得关注

### 1. 多 Agent 编排是 LangGraph 的教科书级实战

OpenMAIC 的核心架构基于 **LangGraph state machine**，7 个核心目录清晰分层：

```
lib/
├── generation/      # 两阶段课件生成 pipeline（outline → content/images/TTS）
├── orchestration/   # 多 Agent 状态机调度
├── playback/        # 课件回放引擎
└── action/          # Agent 主动 UI 操作

app/api/
├── generate/        # 场景生成 pipeline（outlines, content, images, TTS）
├── generate-classroom/  # 异步 classroom job 提交 + polling
├── chat/            # 多 Agent 讨论（SSE streaming）
├── pbl/             # Project-Based Learning 端点
└── ...              # quiz-grade / parse-pdf / web-search / transcription
```

**关键工程模式**：场景生成是 **两阶段 pipeline**——第一阶段先生成 outline（粗粒度场景结构），第二阶段对每个场景并行生成 content / images / TTS。这种 **outline-first 范式** 解决了 LLM 长输出易跑偏的问题，是 DeerFlow、Manus、Anthropic 多 Agent 系统的共同选择。

**对比其它多 Agent 框架**：

| 项目 | 编排粒度 | 状态管理 | UI 集成 | 通讯集成 | Stars |
|------|---------|---------|---------|---------|-------|
| LangGraph | 通用 state machine | ✅ | ❌ | ❌ | 14k |
| DeerFlow 2.0 | Supervisor + Worker | ✅ Docker sandbox | ❌ | ❌ | 45k |
| CrewAI | Role-based collaboration | ⚠️ 弱 | ❌ | ❌ | 30k+ |
| **OpenMAIC** | **LangGraph + 7 场景 schema** | ✅ | **✅ 主动 UI 操作** | **✅ OpenClaw** | **19k** |
| HKUDS/AgentSpace | Provider router | ⚠️ 弱 | ❌ | ✅ Hermes | 339 |

### 2. 7 种交互场景 = 多模态生成的「可消费 schema」

OpenMAIC 把 LLM 的多模态生成能力，封装成 **7 种标准交互场景**：

| 场景类型 | 工程实现 | 用户价值 |
|---------|---------|---------|
| 📊 **Slides** (`.pptx`) | pptxgenjs + 自定义模板 | 可下载、可二次编辑 |
| 🧠 **Interactive Simulation** | HTML + JavaScript 动态渲染 | 学生可调参数观察结果 |
| 🎮 **Game** | HTML5 mini-game | 通过挑战强化记忆 |
| 🧭 **Mind Map** | D3.js / 树形结构 | 整体概念框架 |
| 💻 **Online Programming** | 浏览器内代码执行 | 边学边写 |
| ❓ **Quiz** | quiz-grade API 自动评分 | 即时反馈 |
| 🎯 **PBL (Project-Based Learning)** | 端到端项目流程 | 实战能力 |

**关键洞察**：这 7 种场景不是装饰，是 **Agent 输出契约 (output contract)**。每个场景都有 schema（输入约束 + 输出格式 + UI 渲染规则），下游消费方（UI、回放、导出）可以**统一处理**。这是 OpenMAIC 区别于「把 LLM 输出直接渲染」项目的核心工程价值。

> "Process simulations and experimental environments for observing dynamic changes and outcomes."
> — [OpenMAIC README](https://github.com/THU-MAIC/OpenMAIC)

### 3. AI Teacher 主动操作 UI：从「回答问题」到「引导注意力」

绝大多数 Agent 框架的设计哲学是 **「等用户问，Agent 答」**。OpenMAIC 反过来：

> "The AI teacher can actively operate the UI to guide students — highlighting key areas, setting conditions, providing hints, and directing attention at the right moments."

这意味着 Agent 不只是生成内容，它还**主动引导用户的注意力**——在一个 simulation 场景里，AI teacher 可以在用户即将犯错时自动 highlight 关键参数；在一个 quiz 场景里，可以在用户卡住 30 秒后主动给 hint。

**这是 agent UX 的范式转变**：
- 传统 Agent：被动响应型（user → prompt → response）
- OpenMAIC：**主动引导型**（agent → UI action → user attention redirect）

这种范式目前没有其它主流框架在做——Anthropic Computer Use、OpenAI Operator 都是「代替用户操作」，而 OpenMAIC 是「引导用户自己操作」。

### 4. OpenClaw 集成：让 Agent 触达 99% 不装 CLI 的非技术用户

OpenMAIC 集成了 **OpenClaw**（personal AI assistant）作为即时通讯网关：

> "OpenMAIC integrates with OpenClaw — a personal AI assistant that connects to messaging platforms you already use (Feishu, Slack, Discord, Telegram, WhatsApp, etc.). With this integration, you can generate and view interactive classrooms directly from your chat app without ever touching a terminal."

**Just tell your OpenClaw assistant what you want to learn — it handles everything else.**

这意味着用户的工作流从：

```
旧：打开网页 → 上传文档 → 选场景 → 等生成 → 打开课件
新：在飞书说「做一份 A 股估值的课件」 → 等 30 秒 → 在飞书直接看到交互课件
```

**范式意义**：当 Agent 不再需要「专属 IDE / CLI / 网页」，而是通过用户已有的 IM 触达时，**Agent 的用户基数可以扩大 100x**。这是 OpenMAIC 19k stars 的核心驱动——它不是给开发者用的，是给**所有人**用的。

OpenMAIC 不是唯一走这条路径的项目——HKUDS/AgentSpace (339 stars, 2026-06-24 added) 同样把 OpenClaw 列为支持的多 Agent runtime，但 AgentSpace 是 **CLI 抽象层**，OpenMAIC 是 **完整应用产品**——两者形成「runtime 层 + 产品层」的互补。

### 5. PDF → Interactive Classroom：输入侧的多模态支持

OpenMAIC 支持从 **PDF 文档直接生成交互课件**——`parse-pdf` 端点处理文档解析，生成 pipeline 把长文档拆分成 outline → 场景 → 内容。这背后是「**文档作为 prompt**」的范式：

| 输入 | 处理路径 | 输出 |
|------|---------|------|
| 主题（"machine learning"） | outline → 7 场景默认 schema | 完整课件 |
| PDF 文档 | parse-pdf → outline → 7 场景内容定制 | 文档配套课件 |
| 用户对话 | SSE streaming chat | AI 老师 + AI 同学实时讨论 |

**价值**：教师、研究者、企业培训师可以直接把自己的讲义/论文/手册喂给 OpenMAIC，**5 分钟得到配套的交互课件**——把"备课"从几天压缩到几分钟。

---

## 与 R612 Cluster 的呼应

R612 (今天 19:57 CST) 实现了 **Anthropic Newsroom breakthrough**——Claude Science AI Workbench (2026-06-30) 把 Harness Engineering 6 原则（auditable artifacts / reproducible compute / skill-as-harness / reviewer-agent / in-session persistent context / local-first sensitive data）应用到科学研究垂直领域。

OpenMAIC 与 Claude Science 是 **同一波趋势的不同表达**：

| 维度 | Anthropic Claude Science (1st-party) | THU-MAIC OpenMAIC (3rd-party) |
|------|--------------------------------------|-------------------------------|
| 垂直领域 | 科学研究 (life sciences) | 教育 (interactive classroom) |
| 核心抽象 | Skills + Connectors + Auditable artifacts | 7 场景 schema + AI Teacher + UI actions |
| 多 Agent | Anthropic SDK | LangGraph + 自定义 orchestration |
| 部署 | Anthropic 平台 | Vercel 一键部署 + OpenClaw IM 分发 |
| 开源 | 闭源 (1st-party) | MIT (3rd-party) |
| 学术背书 | Anthropic | 清华大学 MAIC 实验室 |

**Pattern 9 (Self-Positioning Match) 验证**：OpenMAIC 的官方定位 "**Open Multi-Agent Interactive Classroom**" 与 Anthropic Claude Science 的 "**AI workbench for scientists**" 都体现 **「垂直领域的 Agent 产品化」** —— 抽象出场景 schema，让 LLM 输出变成可消费的领域产品。

**Cluster 信号**：R612 突破 + OpenMAIC 同时出现，说明 2026 H2 的 Harness Engineering 趋势正在从「通用 framework」转向 **「垂直产品」**。这是继 R548 (Sakana learned orchestration) 之后的**第二个明显趋势**。

---

## 部署与社区生态

### Vercel 一键部署

OpenMAIC 提供 Vercel 部署按钮，所有 providers 都是可选的（不绑定任何 LLM 厂商）：

```
Deploy with Vercel → 配置 .env → 完成
```

这与 anomalyco/opencode (149k stars, MIT) 的"完全 provider 无关"哲学一脉相承——**不锁定 LLM provider 是 2026 H2 高 stars 项目的共同特征**。

### 学术背景

- **清华大学 MAIC 实验室**（THU-MAIC = Tsinghua University - Multi-Agent Interactive Classroom）
- 项目联系邮箱：`thu_maic@mail.tsinghua.edu.cn`
- 配套论文：项目主页提供 paper link（academic citation）

**对比国内同类项目**：
- datawhalechina/Agent-Learning-Hub (1.6k stars) — 中文社区学习资料库
- alchaincyf/nuwa-skill-distill-expert-thinking (25.7k stars) — 字节跳动 Skill 蒸馏
- **THU-MAIC/OpenMAIC (19k stars)** — 清华多 Agent 教育产品

19k stars 在国内 AI Agent 开源项目中属于**第一梯队**（仅次于 alchaincyf/nuwa 25.7k 和 composio 28k），远超大部分学术 lab 开源项目。

---

## 与现有仓库项目的对照表

| 项目 | Stars | Cluster 角色 | 编排粒度 | 状态 |
|------|-------|-------------|---------|------|
| DeerFlow 2.0 (字节跳动) | 45k | SuperAgent Harness (research task) | LangGraph Supervisor | 已收录 (R531) |
| **THU-MAIC/OpenMAIC** | **19k** | **Vertical Product (education)** | **LangGraph + 7 场景** | **本篇收录** |
| HKUDS/Vibe-Trading | 15k | Trading Safety Harness | Provider reliability | 已收录 (R595) |
| Canner/WrenAI | 15.5k | Open Context Layer | SQL Agent | 已收录 (R341) |
| HKUDS/NanoBot | 44k | Ultra-lightweight Agent | Minimal runtime | 已收录 |
| Zhayujie/CowAgent | 45k | Multi-model Multi-channel | Provider harness | 已收录 |

**新维度贡献**：OpenMAIC 是现有 70 个 project 中**第一个「Vertical Product (education)」cluster** 的项目，填补了「多 Agent 编排 → 垂直消费产品」的空白。

---

## 总结：为什么这个项目是 2026 H2 的代表性突破

1. **多 Agent 编排的产品化范本**：把 LangGraph state machine 封装成 7 种可消费场景，是多 Agent 框架走向终端用户的完整工程路径
2. **AI Teacher 主动 UI 操作**：从「被动响应」到「主动引导注意力」的 UX 范式转变，目前没有主流框架在做
3. **OpenClaw 集成**：通过 IM 网关触达 99% 非技术用户，是 Agent 分发层的关键基础设施
4. **学术背书 + MIT + 19k stars**：清华大学 MAIC 实验室开源，3,771 forks，213 open issues，107 watchers——证明这是真实被采用的项目，不是 GitHub 收藏夹
5. **R612 cluster 闭环**：与 Anthropic Claude Science 同步出现，确认 2026 H2 「Harness Engineering 垂直化」趋势

**建议关注路径**：
- 多 Agent 编排 → 看 OpenMAIC 的 `lib/orchestration/` 是怎么设计 state machine 的
- 多模态输出契约 → 看 OpenMAIC 的 7 场景 schema 设计
- Agent UX → 看 OpenMAIC 的 `lib/action/` 是怎么让 Agent 主动操作 UI 的
- Agent 分发 → 看 OpenMAIC 的 OpenClaw 集成代码

---

**来源**：
- [THU-MAIC/OpenMAIC GitHub](https://github.com/THU-MAIC/OpenMAIC)
- [OpenMAIC Live Demo](https://openmaic.app)（来自 README）
- [R612 Claude Science Breakthrough (2026-07-01)](../articles/orchestration/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md) — 同 cluster 对比
- [HKUDS/AgentSpace Project (2026-06-24)](./hkuds-agentspace-human-agent-collaborative-workspace-339-stars-2026.md) — 同 OpenClaw 集成 runtime 互补