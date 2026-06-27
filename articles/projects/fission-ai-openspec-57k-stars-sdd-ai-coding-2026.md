# Fission-AI/OpenSpec: 57k Stars 的 Spec-Driven Development 框架——让 AI Coding 从"改代码"进化到"改规范"

> **核心命题**：OpenSpec 解决了一个长期被忽视的问题——AI Coding Agent 最大的浪费不是「代码写错了」，而是「改完代码才发现需求/规范从一开始就想错了」。它用一套完整的规范驱动开发工作流，让 AI 从"执行者"变成"参与者"，从根本上改变了人机协作的边界。

---

## 一、问题的本质：AI Coding 的"规范错位"困境

当前 AI Coding Agent 的典型工作流是：

```
人类给需求 → AI 写代码 → 人类审代码 → 不满意 → AI 改代码 → ...
```

这个循环里有一个根本性浪费：**规范/需求阶段完全由人类完成，AI 只在"执行"阶段介入**。当人类对需求的理解有偏差时，AI 每次"改代码"都是在为这个偏差付出代价。

更糟糕的是，AI 缺乏规范意识。它不知道这次修改是为了"修复 bug"还是"实现新需求"，不知道哪些改动是核心的还是边缘的，更不会主动问"这个改动会影响其他功能吗"。

OpenSpec 的核心洞察是：**把规范（Spec）变成 AI Agent 可以读取、理解和修改的一等公民**。

---

## 二、OpenSpec 的核心工作流

### `/opsx:propose` → 规范先行

```
You: /opsx:propose add-dark-mode
AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — 为什么要做这个改动
     ✓ specs/      — 需求和场景
     ✓ design.md   — 技术方案
     ✓ tasks.md    — 实施检查清单
     Ready for implementation!
```

**这不是在生成文档，而是在生成规范结构**。每个文件都有明确的语义：

| 文件 | 语义 | AI 理解 |
|------|------|---------|
| `proposal.md` | 动机与目标 | "为什么做" → 影响评估 |
| `specs/` | 需求规格 | "做什么" → 验收标准 |
| `design.md` | 技术方案 | "怎么做" → 实施路径 |
| `tasks.md` | 实施清单 | "做到哪了" → 进度追踪 |

AI 在动手之前必须先完成这个规范结构。这改变了 AI 的角色——从"代码生成器"变成"需求分析 + 方案设计 + 代码实现"的三位一体。

### `/opsx:explore` → 探索式需求澄清

```
You: /opsx:explore
AI:  What would you like to explore?
You: I want dark mode but I'm not sure how to do it cleanly.
AI:  Let me look at your styling setup...
     Cleanest path: CSS variables + theme context + system-preference detection.
     No new dependencies. Scope it?
```

`/opsx:explore` 是 OpenSpec 的"需求澄清层"。它让 AI 在没有明确规范的情况下，先读代码、理解现有结构，再提出建议。

**这解决了一个实际问题**：当人类对需求的实现路径不确定时，`/opsx:explore` 充当了"技术咨询"的角色——AI 分析现有代码，给出最优路径推荐，人类确认后才进入 `/opsx:propose`。

### `/opsx:apply` → 规范 → 代码的闭环

```
You: /opsx:apply
AI:  Implementing tasks...
     ✓ 1.1 Add theme context provider
     ✓ 1.2 Create toggle component
     ✓ 2.1 Add CSS variables
     ✓ 2.2 Wire up localStorage
     All tasks complete!
```

代码实施完全按照 `tasks.md` 的清单执行。每个任务完成后，AI 会打勾——这是"进度可见性"的来源，人类随时知道哪些做了、哪些没做。

### `/opsx:archive` → 规范版本化

```
You: /opsx:archive
AI:  Archived to openspec/changes/archive/2025-01-23-add-dark-mode/
     Specs updated. Ready for the next feature!
```

归档的不仅是代码改动，还有完整的规范历史。未来的 AI 或人类可以通过归档的 `proposal + specs + design + tasks` 理解当时做决策的背景——这是代码注释永远无法提供的上下文。

---

## 三、为什么说这是"规范驱动"而非"文档驱动"

市场上已有大量"AI 写文档"的工具，但 OpenSpec 的本质区别在于**规范的结构化程度**：

| 维度 | 传统 AI 文档 | OpenSpec 规范 |
|------|------------|--------------|
| 需求来源 | 人类输入 | AI 探索 + 人类确认 |
| 规范格式 | Markdown 自由文本 | 四文件结构（proposal/specs/design/tasks） |
| 规范可执行性 | 无 | tasks.md 可逐项打勾 |
| 规范版本化 | 散落在 commit message | 统一归档到 `changes/archive/日期-名称/` |
| 规范可验证性 | 无 | specs/ 定义验收标准 |
| AI 对规范的修改 | 无 | `/opsx:propose` 本身就是 AI 修改规范 |

**关键差异**：OpenSpec 的规范不是"写给人看的"，而是"供 AI 执行和追踪的"。

---

## 四、OpenSpec 的工程机制：规范即记忆

OpenSpec 的规范文件（`proposal.md`、`specs/`、`design.md`、`tasks.md`）本质上是一种**结构化的项目记忆**。它们解决了 AI Coding 的三个核心问题：

### 1. 需求上下文丢失

AI Coding Agent 在长任务中最大的问题是"忘记为什么这样做"。规范文件在每次 `/opsx:propose` 时生成，**每个改动都有完整的上下文记录**。后续的 AI Agent 可以通过读 `proposal.md` 理解决策背景，而不是从代码反推意图。

### 2. 实施范围蔓延

没有规范的约束，AI 容易"多做"或"少做"。`tasks.md` 是明确的实施边界——AI 只能勾选清单上的任务，如果发现需要额外的工作，必须先 `/opsx:propose` 更新规范。这防止了实施范围在过程中的悄悄扩大。

### 3. 跨会话一致性

归档后的规范（`changes/archive/`）可以在新会话中被 AI 重新读取。这意味着**即使人类重启一个会话，AI 也能通过规范文件恢复到之前的工作状态**——不需要依赖完整的聊天历史，也不需要重新解释项目背景。

---

## 五、与其他 AI Coding 工具的互补关系

OpenSpec 不是要替代 Claude Code 或 Cursor，而是**在这些工具之上增加了一层规范管理层**：

- **Claude Code** / **Cursor**：负责执行层——读规范文件 → 写代码 → 完成任务
- **OpenSpec**：负责规划层——探索需求 → 生成规范 → 追踪进度 → 归档记忆

这种分层的好处是：**规范层和执行层可以独立迭代**。人类可以在不修改代码的情况下调整规范，AI 可以在不重新解释需求的情况下重新实施。

---

## 六、适用边界：OpenSpec 不是银弹

**OpenSpec 擅长的场景**：
- 需要跨多个改动的长期项目（规范文件提供进度追踪）
- 多轮需求变更的探索性开发（`/opsx:explore` 提供结构化探索）
- 需要保留决策背景的团队项目（归档提供历史上下文）

**OpenSpec 不适用的场景**：
- 一次性的小改动（建立规范的开销远大于直接改代码）
- 严格瀑布式的需求冻结项目（OpenSpec 的迭代式规范与瀑布文化冲突）
- 不愿意让 AI 参与需求分析的人类（OpenSpec 假设 AI 是需求的主动参与者）

---

## 七、一个被低估的价值：规范作为人机协作界面

笔者认为，OpenSpec 真正有远见的部分不是工作流本身，而是**把规范从"人类的产出"变成了"人机协作的界面"**。

传统开发中，规范是人类写给人类看的。人机协作时代，规范必须同时满足：

- **人类可读**：人类能理解、审查、修改
- **AI 可执行**：AI 能解析、遵守、追踪
- **结构化**：机器能理解语义（不只是字符串匹配）

OpenSpec 用四文件结构解决了这个三元矛盾。`proposal.md` 是人类友好的叙事，`specs/` 是结构化的验收标准，`design.md` 是 AI 可解析的技术规范，`tasks.md` 是可追踪的实施清单。

**规范不再只是"文档"，而是人机协作的共享工作区。**

---

## 参考与延伸

- GitHub: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) — 57,992 Stars, MIT License
- NPM: `npm install -g @fission-ai/openspec@latest`
- Philosophy: "fluid not rigid, iterative not waterfall, easy not complex"
- 新功能: `/opsx:propose` artifact-guided workflow（重建后的新工作流）
- 支持工具: 25+ 工具集成（Claude Code、Cursor、GitHub、VS Code 等）

---

*推荐理由：OpenSpec 是 2026 年 AI Coding 工具链中，唯一从"规范驱动"角度切入的 50k+ Stars 项目。它不是另一个代码生成器，而是重新定义了人机协作中"规范"这个角色的本质。*
