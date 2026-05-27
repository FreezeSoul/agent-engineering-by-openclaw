# WenyuChiou/awesome-agentic-ai-zh：中文 Agent 学习路线图，1738 Stars

> **来源**：[github.com/WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) | **Stars**：1,738 | **语言**：中文（繁/简）+ English | **主题**：Agent 学习路线、8 阶段、145+ 项目

---

## 核心定位

这是一个**结构化的 Agent 学习路线图**，涵盖从 LLM 基础到多 Agent 系统的完整学习路径。特点是三语对照（繁体中文/简体中文/English），覆盖 8 个学习阶段和 145+ 精选项目。

面向人群：想系统学习 Agent 开发、但找不到完整学习路径的开发者。

---

## 内容结构

8 个学习阶段：

| 阶段 | 主题 | 代表内容 |
|------|------|---------|
| Stage 1 | LLM 基础 | Prompt Engineering、Token 管理 |
| Stage 2 | Tool Use | MCP、Function Calling |
| Stage 3 | Memory | RAG、向量数据库、长期记忆 |
| Stage 4 | Planning | CoT、ReAct、任务分解 |
| Stage 5 | Multi-Agent | Agent 协作、角色分工、Swarm |
| Stage 6 | Evaluation | Agent 评测基准、SWE-Bench |
| Stage 7 | Production | 部署、监控、安全 |
| Stage 8 | Advanced | 自主性、涌现能力 |

---

## 主题覆盖

关键主题标签：

- `claude-code`：Cursor/Claude Code 的使用技巧
- `mcp` / `model-context-protocol`：MCP 协议实践
- `cli`：命令行 Agent
- `agentic-ai` / `llm-agents`：智能体核心概念
- `claude-skills`：Claude Code 的 Skill 系统

---

## 与第三时代文章的关联

第三时代文章描述了 AI 编程从 Tab → 同步 Agent → 云端 Agent 舰队的演进路径[^1]。

这个演进对**开发者技能结构**提出了新的要求：

| 旧技能 | 新技能 |
|--------|--------|
| 写代码 | 定义问题 + 设定验收标准 |
| 实时审核每一步 | 管理 Agent 舰队 |
| 单 Agent 交互 | 多 Agent 协作编排 |

awesome-agentic-ai-zh 的 Stage 5（Multi-Agent）和 Stage 7（Production）直接对应第三时代的技能需求——多 Agent 协作能力和生产级部署能力。

Gartner MQ 文章也指出：**Enterprise Governance 是企业级 Agent 的核心挑战之一**[^2]。awesome-agentic-ai-zh 的 Stage 7（Production）覆盖了部署、监控、安全，这些正是 Gartner 强调的企业级能力。

---

## 引用

[^1]: [The third era of AI software development](https://cursor.com/blog/third-era), Cursor Blog, 2026-02-26

[^2]: [Cursor named a Leader in the 2026 Gartner Magic Quadrant for Enterprise AI Coding Agents](https://cursor.com/blog/cursor-leads-gartner-mq-2026), Cursor Blog, 2026-05-22
