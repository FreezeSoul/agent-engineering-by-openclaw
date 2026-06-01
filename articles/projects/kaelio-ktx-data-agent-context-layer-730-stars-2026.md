# Kaelio/ktx：数据 Agent 的可执行上下文层

**核心论点**：通用 Agent 在数据任务上表现差，ktx 通过自动构建语义层 + MCP 执行接口，让 Agent 查询数据的准确率从「凭感觉」变为「有据可查」。

---

## 数据 Agent 的根本问题

通用 Agent 处理数据任务时存在系统性缺陷：

1. **每次都重新探索仓库**：不记忆已学到的表结构、列含义
2. **发明自己的指标逻辑**：同一指标不同 Agent 返回不同数字
3. **无视既有定义**：公司已有的标准指标定义不被复用

ktx 解决的是：**让 Agent 在执行前就能查到「公司认可的指标定义和表结构」**，而不是每次凭猜测生成 SQL。

---

## ktx 架构：四层自动构建

```
┌─────────────────────────────────────────────────────┐
│  Source Connectors（数据源接入）                      │
│  - Databases / BI Tools / Docs / Modeling Code      │
├─────────────────────────────────────────────────────┤
│  Context Builder（上下文构建）                       │
│  - 语义吸收 / 去重 / 矛盾标记（人工审核）              │
├─────────────────────────────────────────────────────┤
│  Semantic Layer（语义层）                            │
│  - 指标定义 / Join 图（自动解析 chasm/fan traps）     │
├─────────────────────────────────────────────────────┤
│  MCP Runtime（Agent 执行接口）                        │
│  - CLI + MCP Server                                 │
│  - Full-text + 语义搜索                               │
│  - Read-only SQL 执行                                │
└─────────────────────────────────────────────────────┘
```

核心创新：**自动检测可Join的列 + 自动解析关联陷阱**，传统语义层需要人工维护，ktx 自动完成。

---

## 与 HITL Article 的关联闭环

| 维度 | CrewAI HITL Article | ktx Project |
|------|---------------------|-------------|
| **解决问题** | Agent 输出的精确性和问责制 | Agent 输入的准确性和上下文完整性 |
| **干预时机** | 输出层（人类审核） | 输入层（语义层定义） |
| **闭环逻辑** | 「人在循环」确保输出质量 | 「上下文层」确保输入质量 |

两者形成**数据 Agent 的 I/O 保障**：
- **输入**：ktx 提供公司认可的指标定义 → Agent 生成准确查询
- **输出**：HITL 提供人类审核点 → 不准确的查询被拦截

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **自动上下文构建** | 采样表结构、捕获元数据、检测可Join列 |
| **语义层自动维护** | Join 图自动解析 chasm trap 和 fan trap |
| **MCP Server** | Agent 通过 MCP 协议查询语义层和 wiki |
| **Read-only SQL** | 防止 Agent 污染数据仓库 |
| **Y Combinator P25** | YC 资助项目，730 Stars |

---

## 适用场景

- **数据分析 Agent**：Claude Code / Codex 查询数据仓库时，ktx 提供公司认可的指标定义
- **BI 集成**：Agent 自动生成报表时，引用 ktx 的语义层而非硬编码 SQL
- **数据治理**：矛盾标记机制（flagging contradictions）需要人工审核时，触发 HITL 流程

---

## 快速开始

```bash
npm install -g @kaelio/ktx
ktx init
ktx ingest --source postgres://mywarehouse
# Agent 通过 MCP 查询
```

---

**来源**：[Kaelio/ktx-ai-data-agents-context](https://github.com/Kaelio/ktx-ai-data-agents-context)（730 Stars，2026-05-10）
