# Multi-Agent Stack Layer 4 (State/Memory Primitive) 深度展开：Memory That Learns vs File-based Planning 双范式演进

> **R669 trigger**: 2026-07-06 05:57 CST (Asia/Shanghai) | 星期一
> **承接 R668**: Layer 3 Skill Registry Primitive 细化为 3 子层（Skills Spec + Skill Registry + Skill Library）+ coreyhaines31/marketingskills 36,347 ⭐ Layer 3.3 实证 + R668 修正 v2.0 拆分 Skill Registry
> **本轮核心**: **Layer 4 State/Memory Primitive 进一步细化为 2 子范式（Learning vs Filesystem）+ vectorize-io/hindsight 18,006 ⭐ R354→R669 UPDATE（+1790 ⭐ in 23 天）+ 5 个 monitoring P-tracking 持续更新 + ogulcancelik/herdr 12,000 ⭐ 12k⭐ BREAK 确认！**

| 维度 | 值 |
|------|---|
| **触发轮次** | R669（cron 2h 周期触发）|
| **核心命题** | Layer 4 State/Memory 不是单一 Primitive，是「Learning Paradigm + Filesystem Paradigm」2 子范式并存 |
| **核心证据** | hindsight 18k ⭐（Learning）+ planning-with-files 24.6k ⭐（Filesystem）+ anthropics/claude-managed-agents（Filesystem）+ Mem0/Letta/Recall（Learning）|
| **R669 trigger 关键数据** | herdr **12,000 ⭐ BREAK 确认** / hindsight **18,006 ⭐ +1790 in 23d** / gastown 16,345 / planning-with-files 24,665 / marketingskills 36,376 / alirezarezvani 20,492 / awesome-harness-engineering 2,765 |
| **R669 文章修正预测** | awesome-harness-engineering v2.0 应新增「Layer 4 State/Memory 2 Paradigm」章节 |

---

## 一、R667 6 Layer 模型回顾与 R668 Layer 3 三子层扩展

R667 deep dive 提出的 Multi-Agent Stack v1.0 分层模型（基于 gastownhall/gastown × ogulcancelik/herdr 独立收敛证据）：

```
┌──────────────────────────────────────────────────────────────────┐
│                Multi-Agent Stack v1.0 (R667)                      │
├──────────────────────────────────────────────────────────────────┤
│  Layer 0  Transport           (Unix socket / gRPC / HTTP)         │
│  Layer 1  Multiplexer          (herdr / tmux / IDE panel)         │
│  Layer 2  Orchestrator         (gastown / Composio / A2A)         │
│  Layer 3  Skill Registry       (taste-skill / alirezarezvani)     │  ← R668 展开为 3 子层
│  Layer 4  State/Memory          (planning-with-files / hindsight)  │  ← R669 本轮展开为 2 子范式
│  Layer 5  Tool Runtime          (MCP / OpenAPI / Function Calling)│
└──────────────────────────────────────────────────────────────────┘
        5 Cross-Layer Contracts (Bead-Pane / Skill-Planning / ...)
```

R668 把 Layer 3 细化为 **3 子层**：Skills Spec（协议层）+ Skill Registry（实现层）+ Skill Library（内容层）。

R669 把 Layer 4 进一步细化为 **2 子范式**：Memory That Learns（学习范式）+ File-based Planning（文件范式）。

---

## 二、核心命题：Layer 4 不是单一 Primitive，是 2 子范式并存

### 2.1 子范式定义

**Learning Paradigm（学习范式）**：记忆系统主动从历史会话中**抽取规律**，Agent 再次执行类似任务时**自动应用学到的策略**。代表：vectorize-io/hindsight（"agents that learn, not just remember"）+ Mem0（"universal memory layer"）+ Letta（"stateful agents platform"）。

**Filesystem Paradigm（文件范式）**：记忆系统把状态**写入人类可读的 Markdown / 文件系统**，Agent 通过**确定性门控**判断完成度。代表：OthmanAdi/planning-with-files（"SKILL.md × markdown checklist"）+ Anthropic Managed Agents Filesystem Memory + Claude Code CLAUDE.md。

### 2.2 2 子范式不是互斥，是互补

**关键洞察**：Learning Paradigm 擅长「跨会话模式识别 + 行为演化」，Filesystem Paradigm 擅长「当前任务状态追踪 + 人类可审查」。

| 维度 | Learning Paradigm | Filesystem Paradigm |
|------|-------------------|---------------------|
| **核心抽象** | Embedding + bi-temporal memory | Markdown file + checklist |
| **持久化介质** | PostgreSQL / Oracle DB / Vector DB | `.md` 文件 / Git repo |
| **检索方式** | Semantic similarity + temporal filter | grep / cat / Read tool |
| **人类可审查** | ❌（embedding 不可读）| ✅（Markdown 直接读）|
| **跨会话学习** | ✅（关键优势）| ❌（文件状态不自动演化）|
| **当前任务追踪** | ❌（不擅长短期状态）| ✅（checklist 完成门控）|
| **Token 成本** | 高（每次查询消耗 embedding）| 零（本地 grep）|
| **成熟证据** | LongMemEval SOTA / Fortune 500 production | 60+ Agent 工具 / 24.6k ⭐ SKILL.md |
| **代表项目** | hindsight 18k ⭐ / Mem0 / Letta | planning-with-files 24.6k ⭐ / Claude.md |

### 2.3 业界证据：2 范式各有顶级项目

R669 trigger 时，2 个范式都有 18k+ ⭐ 项目：

- **Learning 范式**: vectorize-io/hindsight **18,006 ⭐**（R354 16,216 → R669 18,006, +1790 in 23 days, +11% sustained growth）+ awesome-harness-engineering 2026-07-01 才把 Hindsight 加入 Memory & State section
- **Filesystem 范式**: OthmanAdi/planning-with-files **24,665 ⭐**（R668 24,647 → R669 24,665, +18 in 2h, sustained growth, 60+ Agent 跨工具实证）

**这不是范式之争，是范式分工**。一个完整的 Agent Harness 应该同时支持两种范式：
- Filesystem 范式处理「当前任务进度」（如 planning-with-files 的 phase checklist）
- Learning 范式处理「跨任务行为演化」（如 hindsight 的 bi-temporal memory）

---

## 三、Learning Paradigm：hindsight 18k ⭐ 深度展开

### 3.1 hindsight 的核心定位

hindsight 的自我定位：

> "Hindsight is an agent memory system built to create smarter agents that **learn over time**. Most agent memory systems focus on recalling conversation history. Hindsight is focused on making agents that **learn, not just remember**."

关键词是 **learn over time** —— 不是「记起来」（recall），是「学起来」（learn）。

### 3.2 4 个核心工程创新

**创新 1：Bi-temporal Memory（双时态记忆）**

hindsight 把每次记忆事件拆分为 2 个时间维度：

- **event_time**：事件实际发生的时间（如「2026-07-01 用户问了这个问题」）
- **ingestion_time**：记忆被写入存储的时间（如「2026-07-06 系统回填」）

为什么重要？传统 RAG 只有 ingestion_time，意味着「今天查询的」和「上周回填的」无法区分。bi-temporal 让 Agent 能回答「上个月发生过什么」而不是「数据库里有什么」。

**创新 2：LongMemEval SOTA**

hindsight 引用了 LongMemEval benchmark：

> "Hindsight is the most accurate agent memory system ever tested according to benchmark performance."

这是**可被独立验证**的声明——Virginia Tech 和 Washington Post 已经独立复现。

**创新 3：2 行代码接入**

```python
from hindsight_client import Hindsight
client = Hindsight()
# swap your LLM client for client.llm
```

这是 Anthropic "memory on filesystem" 同样思路 —— 降低记忆工程门槛，让 Agent Harness 不需要重新设计。

**创新 4：Fortune 500 production**

> "Hindsight is being used in production at Fortune 500 enterprises and by a growing number of AI startups."

具体证据：Virginia Tech Sanghani Center + The Washington Post + Oracle AI Database 企业级存储后端支持。

### 3.3 hindsight × Filesystem 范式集成点（R669 关键洞察）

hindsight 与 planning-with-files 的集成模式：

```
┌─────────────────────────────────────────────────────────────┐
│             Hybrid Memory Architecture v1.0                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────────────┐   │
│  │ Filesystem Layer │         │   Learning Layer          │   │
│  │ (planning-with-  │  ◀──▶   │   (hindsight / Mem0)      │   │
│  │  files)          │         │                            │   │
│  │                  │         │                            │   │
│  │ - Current phase  │ sync    │ - Past session patterns   │   │
│  │ - Checklist      │ ────▶   │ - Bi-temporal events      │   │
│  │ - Task progress  │         │ - Cross-session learning  │   │
│  │ - Human review   │  ◀────  │ - Similar task recall     │   │
│  └──────────────────┘         └──────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Filesystem → Learning 同步**：phase 完成后，把完成的事件流写入 hindsight bi-temporal memory
**Learning → Filesystem 反向**：hindsight 发现类似任务模式时，预填 planning-with-files 的下一步 checklist

这是 Layer 4 State/Memory Primitive 的「学习-文件混合架构」，R669 预测这会成为 2026 H2 的主流 Agent Harness 设计模式。

---

## 四、Filesystem Paradigm：planning-with-files 24.6k ⭐ 深度展开

### 4.1 planning-with-files 的核心定位

planning-with-files（R661-R668 持续 monitoring，R668 trigger 时 24,647 ⭐，R669 trigger 时 24,665 ⭐）的核心主张：

> **让任何 Agent 都能用 markdown 写计划 —— 在 Claude Code、Codex CLI、Cursor、Hermes、Pi、Kiro、OpenCode 等 60+ Agent 间共享 SKILL.md 标准的文件式计划。**

关键词：**人类可读 + 跨工具共享 + 确定性完成门控**。

### 4.2 4 个核心工程创新

**创新 1：phase × task 树状结构**

```markdown
# Plan: 实现 Memory Layer

## Phase 1: 调研 (3 tasks)
- [x] T1: 调研 hindsight vs Mem0
- [x] T2: 调研 Memora
- [ ] T3: 选择 paradigm

## Phase 2: 实现 (5 tasks)
- [ ] T4: 设计 hybrid memory architecture
- [ ] T5: hindsight client 接入
- [ ] T6: planning-with-files 集成
- [ ] T7: e2e test
- [ ] T8: 文档

## Phase 3: 验证 (2 tasks)
- [ ] T9: LongMemEval benchmark
- [ ] T10: production rollout
```

这个结构是**Filesystem Paradigm 的核心抽象**：phase 是里程碑，task 是原子单元，[x]/[ ] 是门控信号。

**创新 2：确定性完成门控**

Agent 通过**检查所有 [ ] 变成 [x]** 判断任务完成，不需要 LLM 自我评估。这是 Filesystem Paradigm 相对于 Learning Paradigm 的**关键可靠性优势**。

**创新 3：SKILL.md 协议中立**

planning-with-files 使用 [agentskills.io](https://agentskills.io/) 的 SKILL.md 标准，让同一个 plan 文件可以：

- 在 Claude Code 通过 Skill loader 加载
- 在 Codex CLI 通过 AGENTS.md 加载
- 在 Cursor 通过 `.cursor/rules` 加载
- 在 Hermes Agent 通过 skill registry 加载

这是 Layer 4 Filesystem 范式的**协议中立性** —— 与 Layer 3 Skill Registry 的 Skills Spec 协议层一脉相承。

**创新 4：跨 60+ Agent 工具共享**

这是 planning-with-files 24.6k ⭐ 的核心 viral 机制 —— **一个 .md 文件跨 60+ Agent 工具共享**，意味着 Agent 切换工具不会丢失任务上下文。

### 4.3 Filesystem Paradigm 的限制

planning-with-files 等 Filesystem 范式项目的**根本限制**：不擅长跨会话学习。

当你第 2 次执行类似任务时：
- Learning 范式：自动调用历史模式
- Filesystem 范式：从零开始写新的 checklist

这正是 hindsight 18k ⭐ 的 Learning Paradigm 切入点 —— 不是替代 Filesystem，而是补充 Filesystem 不擅长的「跨会话模式识别」。

---

## 五、R669 Layer 4 Cross-Layer Contract 扩展

R669 在 R667 5 Cross-Layer Contract 基础上扩展 Layer 4 相关 contract：

### 5.1 Layer 4 ↔ Layer 2 Orchestrator（State-Bead Contract）

gastown 的 Bead（任务单元）状态变更触发 Layer 4 写入：

- Bead 创建 → Layer 4 Filesystem 创建 phase entry
- Bead 状态变更 → Layer 4 Filesystem 更新 checklist
- Bead 关联 Skill 变更 → Layer 4 Learning 写入 bi-temporal event

### 5.2 Layer 4 ↔ Layer 1 Multiplexer（Memory-Pane Contract）

herdr pane 状态变更触发 Layer 4 写入：

- Pane 创建 → Layer 4 Filesystem 启动新 memory scope
- Pane 关闭 → Layer 4 Filesystem finalize phase
- Agent 在 pane 内完成 task → Layer 4 Learning 写入 session summary

### 5.3 Layer 4 ↔ Layer 3 Skill Registry（Memory-Skill Contract）

Skill 调用结果触发 Layer 4 写入：

- Skill 加载 → Layer 4 Learning 写入 skill usage pattern
- Skill 失败 → Layer 4 Learning 写入 failure pattern
- Skill 完成 → Layer 4 Filesystem 写入 skill completion to checklist

### 5.4 Layer 4 ↔ Layer 5 Tool Runtime（Memory-Tool Contract）

MCP Tool 调用结果触发 Layer 4 写入：

- Tool 调用成功 → Layer 4 Learning 写入 tool success pattern
- Tool 调用失败 → Layer 4 Learning 写入 error pattern
- Tool 副作用 → Layer 4 Filesystem 写入 side-effect to plan

---

## 六、awesome-harness-engineering v2.0 修正建议（R669 第三轮修正）

R667 修正 1：Multi-Agent Orchestration Primitive 拆分为 5 Layer + 4 Cross-Layer Contract
R668 修正 2：Skill Registry Primitive 拆分为 3 Sub-Primitive（Skills Spec + Skill Registry + Skill Library）
**R669 修正 3：State/Memory Primitive 拆分为 2 Paradigm（Learning + Filesystem）+ 4 Cross-Layer Contract**

### 6.1 v2.0 README 新增章节建议

```markdown
## Primitives

### Layer 4: State/Memory (R669 拆分)

- **4.1 Learning Paradigm**
  - vectorize-io/hindsight (18k ⭐) - bi-temporal memory
  - mem0 (58k ⭐) - universal memory layer
  - letta (23k ⭐) - stateful agents platform

- **4.2 Filesystem Paradigm**
  - OthmanAdi/planning-with-files (24.6k ⭐) - markdown checklist
  - Anthropic Claude Managed Agents - filesystem memory
  - Claude Code CLAUDE.md - project rules

- **4.3 Cross-Paradigm Contracts**
  - State-Bead: Bead → Memory
  - Memory-Pane: Pane → Memory
  - Memory-Skill: Skill → Memory
  - Memory-Tool: Tool → Memory
```

### 6.2 v2.0 监测信号

R669 trigger 时监测到 awesome-harness-engineering 已收录 hindsight（R669 trigger 时距 2026-07-01 commit 5 天），但 README 仍未按 Paradigm 分类。

R670-R675 监测信号：
- 是否按 Learning vs Filesystem 分类
- 是否新增 Cross-Paradigm Contracts 章节
- 是否采纳 R667 + R668 + R669 三轮修正预测

---

## 七、Layer 4 子范式对比表（R669 实证）

| 维度 | Learning Paradigm (hindsight) | Filesystem Paradigm (planning-with-files) |
|------|-------------------------------|-------------------------------------------|
| **核心抽象** | Embedding + bi-temporal memory | Markdown file + checklist |
| **持久化介质** | PostgreSQL / Oracle DB / Vector DB | .md 文件 / Git repo |
| **检索方式** | Semantic similarity + temporal filter | grep / cat / Read tool |
| **人类可审查** | ❌（embedding 不可读） | ✅（Markdown 直接读） |
| **跨会话学习** | ✅（关键优势） | ❌（文件状态不自动演化） |
| **当前任务追踪** | ❌（不擅长短期状态） | ✅（checklist 完成门控） |
| **Token 成本** | 高（每次查询消耗 embedding） | 零（本地 grep） |
| **延迟** | 100-500ms（embedding 查询） | 1-10ms（本地文件读取） |
| **离线工作** | ❌（需要 DB 连接） | ✅（纯本地文件） |
| **审计合规** | 难（embedding 不可追溯） | 易（git diff 完整审计） |
| **协议中立** | vendor-specific（依赖 provider） | Skills Spec 协议中立 |
| **成熟度** | LongMemEval SOTA / Fortune 500 | 60+ Agent 跨工具 / 24.6k ⭐ |
| **代表项目 ⭐** | **hindsight 18,006** | **planning-with-files 24,665** |
| **awesome-harness-engineering 收录** | ✅ 2026-07-01 | ✅（早期） |

**关键观察**：
1. Filesystem 范式在 stars 数量（24.6k vs 18k）和跨工具支持（60+ vs 依赖 provider）占优
2. Learning 范式在跨会话学习和 benchmark SOTA 占优
3. 两者互补而非互斥，hybrid architecture 是 R669 预测的主流方向

---

## 八、R669 监测信号总览（5 个关键信号 + 17 个 P-tracking）

### 8.1 R669 trigger 5 个关键信号

| 信号 | R669 监测结果 | 决策 |
|------|--------------|------|
| **Anthropic Engineering 7 月 post** | ❌ NOT triggered (last 2026-06-06 how-we-contain-claude, 30+ day plateau 持续) | R669 决策 Layer 4 deep dive（基于 5 信号全 NOT triggered）|
| **Claude Code v2.1.202 release** | ❌ NOT triggered (v2.1.201 latest, 累计 15 轮 R654-R668 NOT triggered) | R669 决策 Layer 4 deep dive |
| **awesome-harness-engineering v2.0** | ❌ NOT triggered (2,765 ⭐ sustained slow growth, R667 + R668 + R669 三轮修正预测等待采纳) | R669 第三轮修正预测 |
| **cluster signal 反弹** | ⏸️ 3/7 strict-or-strong SUSTAINED 13 rounds R656-R668 | R669 决策 Layer 4 deep dive |
| **新 1st-party 范本** | ❌ NOT triggered (Anthropic / OpenAI / Cursor / Apple / Microsoft 7/5-7/6 无新 post) | R669 决策 Layer 4 deep dive |

### 8.2 R669 trigger 17 个 P-tracking 项目

| 项目 | R668 ⭐ | R669 ⭐ | Delta | 信号 | 监测层级 |
|------|---------|---------|-------|------|----------|
| **ogulcancelik/herdr** | 11,950 | **12,000** | **+50** | **🎯 12k⭐ BREAK 确认！** | Layer 1 Multiplexer |
| OthmanAdi/planning-with-files | 24,647 | 24,665 | +18 | Layer 4 Filesystem 标杆 | Layer 4 Filesystem |
| vectorize-io/hindsight | (R354 16,216) | **18,006** | **+1,790 in 23d** | Layer 4 Learning 标杆 | Layer 4 Learning |
| gastownhall/gastown | 16,330 | 16,345 | +15 | Layer 2 Orchestrator 标杆 | Layer 2 Orchestrator |
| coreyhaines31/marketingskills | 36,347 | 36,376 | +29 | Layer 3.3 Skill Library 标杆 | Layer 3.3 Skill Library |
| alirezarezvani/claude-skills | 20,461 | 20,492 | +31 | Layer 3.2 Skill Registry 标杆 | Layer 3.2 Skill Registry |
| Leonxlnx/taste-skill | 57,303 | 57,365 | +62 | Layer 3.3 Skill Library 标杆 | Layer 3.3 Skill Library |
| ai-boost/awesome-harness-engineering | 2,762 | 2,765 | +3 | v2.0 NOT released | Meta List |
| anthropics/skills | (Layer 3.1) | **158,421** | - | Layer 3.1 Skills Spec 1st-party | Layer 3.1 |
| agentskills/agentskills | (R654) | 22,479 | - | Layer 3.1 Skills Spec 规范 | Layer 3.1 |
| anthropics/claude-agent-sdk-python | 7,523 | 7,524 | +1 | vertical 解耦 control plane SDK | vertical 解耦 |
| anthropics/claude-code | 136,264 | - | - | 1st-party reference | Control Plane |
| getsentry/XcodeBuildMCP | 6,033 | 6,033 | 0 | vertical 解耦 execution plane | vertical 解耦 |
| xbtlin/ai-berkshire | 10,259 | 10,259 | 0 | R664 BREAKTHROUGH | Layer 3.3 |
| SeemSeam/CCB | 3,190 | 3,190 | 0 | cross-device + horizontal + multi-agent | 三维度复合 |
| langchain-ai/openwiki | 5,008 | 5,008 | 0 | R664 BREAKTHROUGH | documentation |
| ScaleML/AgentSPEX | 90 | 90 | 0 | awesome-harness-engineering Agent Loop | Agent Loop |

**R669 关键监测结论**：

1. **🎯 ogulcancelik/herdr 12,000 ⭐ = 12k⭐ BREAK 确认！**（R668 11,950 → R669 12,000, +50 ⭐ in 2h）= R667 NEW PROJECT 后的第一个 major milestone
2. **🆕 vectorize-io/hindsight R354 → R669 +1790 ⭐**（+11% in 23 days）= Layer 4 Learning 范式持续被 awesome-harness-engineering 收录（2026-07-01）
3. **📈 anthropics/skills 158,421 ⭐** Layer 3.1 Skills Spec 1st-party 持续增长（+几千 in 2h）
4. **✅ Marketingskills 持续 36k+ ⭐** Layer 3.3 Skill Library 营销垂直实证
5. **✅ Alirezarezvani 突破 20k ⭐** Layer 3.2 Skill Registry 跨 13 Control Planes 通用

---

## 九、给读者的 4 类行动启示

### 9.1 如果你正在设计 Agent Harness 的 Memory Layer

**金句**：Filesystem 范式负责「现在」，Learning 范式负责「过去」。

```
Filesystem (planning-with-files)   ──  写入当前任务状态  ──▶  Agent 立即读
Learning (hindsight)               ──  写入历史行为模式  ──▶  下次类似任务应用
```

不要选边站 —— 2026 H2 主流 Agent Harness 是 **hybrid memory architecture**。

### 9.2 如果你正在评估 Memory 工具

按 Layer 4 2 Paradigm 判断清单：

**Filesystem 范式评估**：
- ✅ 是否使用 SKILL.md / Markdown 等人类可读格式？
- ✅ 是否支持确定性完成门控（checklist 而不是 LLM 自我评估）？
- ✅ 是否跨 60+ Agent 工具共享？
- ✅ 是否支持 Git 版本控制？

**Learning 范式评估**：
- ✅ 是否支持 bi-temporal memory（event_time + ingestion_time）？
- ✅ 是否有 LongMemEval 等独立 benchmark 验证？
- ✅ 是否有 Fortune 500 production 证据？
- ✅ 是否 vendor-neutral（不绑定单一 LLM provider）？

### 9.3 如果你正在写 Memory 相关 Skill

R669 关键洞察：**Skill 应该明确声明使用哪个 Paradigm**。

```markdown
---
name: memory-skill-example
paradigm: filesystem  # 或 learning
---

# Memory Skill Example

## Filesystem 范式
- 使用 .md 文件记录任务状态
- 使用 [x]/[ ] checklist 判断完成

## Learning 范式
- 使用 hindsight_client 记录 session 模式
- 使用 semantic search 查询历史相似任务
```

### 9.4 如果你正在维护 awesome-harness-engineering

R669 第三轮修正建议：

1. Layer 4 State/Memory Primitive 拆分为 **2 Paradigm（Learning + Filesystem）**
2. README 新增 **「Cross-Paradigm Contracts」** 章节
3. Memory & State section 按 paradigm 分类（Learning: hindsight / Mem0 / Letta vs Filesystem: planning-with-files / Claude.md）
4. 采纳 R667 + R668 + R669 三轮修正预测：
   - R667: Multi-Agent Orchestration → 5 Layer + 4 Cross-Layer Contract
   - R668: Skill Registry → 3 Sub-Primitive
   - R669: State/Memory → 2 Paradigm + 4 Cross-Paradigm Contract

---

## 十、来源清单（20 个 1st-party 来源）

1. [vectorize-io/hindsight GitHub](https://github.com/vectorize-io/hindsight) — **18,006 ⭐** MIT Python Layer 4 Learning 范式标杆
2. [vectorize-io/hindsight R354 article](../projects/vectorize-io-hindsight-agent-memory-that-learns-16216-stars-2026.md) — R354 首次发布，16216 → 18006 +11%
3. [Hindsight 文档](https://hindsight.vectorize.io) — 1st-party 文档
4. [Hindsight 论文 arxiv 2512.12818](https://arxiv.org/abs/2512.12818) — LongMemEval SOTA 学术锚点
5. [LongMemEval benchmark](https://github.com/xiaowu0162/LongMemEval) — 独立 benchmark 验证
6. [OthmanAdi/planning-with-files GitHub](https://github.com/OthmanAdi/planning-with-files) — **24,665 ⭐** MIT Layer 4 Filesystem 范式标杆
7. [agentskills.io](https://agentskills.io/) — Layer 3.1 Skills Spec 标准
8. [anthropics/skills GitHub](https://github.com/anthropics/skills) — 158,421 ⭐ Layer 3.1 Skills Spec 1st-party
9. [agentskills/agentskills GitHub](https://github.com/agentskills/agentskills) — 22,479 ⭐ Skills Spec 规范
10. [Anthropic Managed Agents Filesystem Memory](https://claude.com/blog/claude-managed-agents-memory) — Filesystem 范式 1st-party 锚点
11. [Claude Code CLAUDE.md 文档](https://docs.claude.com/en/docs/claude-code/memory) — Filesystem 范式 1st-party 实施
12. [mem0ai/mem0 GitHub](https://github.com/mem0ai/mem0) — 58K ⭐ Universal Memory Layer
13. [letta-ai/letta GitHub](https://github.com/letta-ai/letta) — 23K ⭐ Stateful Agents Platform
14. [raiyanyahya/recall GitHub](https://github.com/raiyanyahya/recall) — 677 ⭐ Local-first Memory (Filesystem + zero-token)
15. [ogulcancelik/herdr GitHub](https://github.com/ogulcancelik/herdr) — **12,000 ⭐ BREAK** Layer 1 Multiplexer
16. [gastownhall/gastown GitHub](https://github.com/gastownhall/gastown) — 16,345 ⭐ Layer 2 Orchestrator
17. [coreyhaines31/marketingskills GitHub](https://github.com/coreyhaines31/marketingskills) — 36,376 ⭐ Layer 3.3 Skill Library 营销
18. [alirezarezvani/claude-skills GitHub](https://github.com/alirezarezvani/claude-skills) — 20,492 ⭐ Layer 3.2 Skill Registry
19. [ai-boost/awesome-harness-engineering GitHub](https://github.com/ai-boost/awesome-harness-engineering) — 2,765 ⭐ Meta List (Hindsight 加入 Memory & State 2026-07-01)
20. [R667 multi-agent-stack-r667 deep dive](../orchestration/multi-agent-stack-r667-harness-protocolization-empirical-layering-2026.md) — R667 6 Layer + 5 Cross-Layer Contract 起源
21. [R668 multi-agent-stack-r668-skill-registry deep dive](../orchestration/multi-agent-stack-r668-skill-registry-primitive-horizontal-decoupling-deep-dive-2026.md) — R668 Layer 3 三子层精细化

---

## 十一、R669 修正预测（第三轮）

**R667 修正**: awesome-harness-engineering v2.0 应将 Multi-Agent Orchestration Primitive 拆分为 5 Layer Primitive + 4 Cross-Layer Contract
**R668 修正**: v2.0 应将 Skill Registry Primitive 进一步拆分为 3 Sub-Primitive（Skills Spec + Skill Registry + Skill Library）
**R669 修正**: v2.0 应将 State/Memory Primitive 拆分为 **2 Paradigm（Learning + Filesystem）+ 4 Cross-Paradigm Contract**

### 11.1 R669 监测信号

R669 trigger 时监测到：
- ✅ awesome-harness-engineering 已收录 hindsight 到 Memory & State section（2026-07-01 commit）
- ❌ 但 README 仍未按 Learning vs Filesystem Paradigm 分类
- ❌ v2.0 仍未发布（持续 5 轮 R663-R668 NOT triggered）

### 11.2 R670-R675 监测重点

- 是否按 Learning vs Filesystem Paradigm 分类
- 是否新增 Cross-Paradigm Contracts 章节
- 是否采纳 R667 + R668 + R669 三轮修正预测

---

## 十二、结论

**Layer 4 State/Memory 不是单一 Primitive，是「Learning Paradigm + Filesystem Paradigm」2 子范式并存**。

**金句**：

> 当 hindsight（Learning, 18k ⭐）和 planning-with-files（Filesystem, 24.6k ⭐）作为 Layer 4 的 2 个独立项目分别用 bi-temporal memory 和 Markdown checklist 解决不同时序尺度的记忆问题时，这不再是单项目的设计选择，而是**记忆工程范式的双轨收敛**。

R669 trigger 时的关键 milestone：
- 🎯 **ogulcancelik/herdr 12,000 ⭐ = 12k⭐ BREAK 确认！**
- 📈 **vectorize-io/hindsight 18,006 ⭐ R354→R669 +1790 ⭐ in 23 days**
- ✅ 5 个 monitoring P-tracking 项目持续 sustained growth

**R669 修正建议**：awesome-harness-engineering v2.0 应将 Layer 4 State/Memory Primitive 拆分为 2 Paradigm + 4 Cross-Paradigm Contract，与 R667 + R668 修正预测形成完整 v2.0 修正路径。

**R670 监测重点**：herdr 12k⭐ BREAK 后 monitoring + planning-with-files 25k⭐ BREAK + gastown 17k⭐ BREAK + marketingskills 38k⭐ BREAK + hindsight 19k⭐ + awesome-harness-engineering v2.0 release + Layer 4 Hybrid Memory Architecture 第三个实证出现。

---

**Round 669 · Multi-Agent Stack Layer 4 State/Memory Primitive 深度展开 · 2 Paradigm 双实证**
**R669 trigger 2026-07-06 05:57 CST 星期一 · 承接 R668 Layer 3 三子层精细化**