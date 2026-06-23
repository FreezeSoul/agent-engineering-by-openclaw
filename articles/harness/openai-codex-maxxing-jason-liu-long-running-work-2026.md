# Codex-maxxing：Jason Liu 用 Codex 跨 Prompt 保留上下文

> **核心论点**：长程 Agent 的「跨 prompt 连续性」已经从工程问题下沉为「用户操作实践」。OpenAI 通过 Jason Liu（Blueprint Industrial 等多家 AI 公司技术顾问）的真实使用案例，把 `Shell + Skills + Compaction` 三原语框架包装成一种可被复制的个人工作流——"Codex-maxxing" 这个词本身的诞生，标志着长程 Agent 的最佳实践从「架构选型」进入「肌肉记忆」阶段。

---

## 1. 这篇文章的独特角度

OpenAI 在 2026 年 6 月 22 日发布的这篇文章 [`Codex-maxxing for long-running work`](https://openai.com/index/codex-maxxing-long-running-work)（AI Adoption 分类）有别于其此前所有的工程长文：

| 维度 | 之前的 OpenAI 长程 Agent 文章 | 本篇 |
|------|------------------------------|------|
| **视角** | 架构师视角（Shell/Skills/Compaction 原语） | 用户视角（一个真实顾问 Jason Liu 的日常） |
| **受众** | 设计 Agent 基础设施的工程师 | 在自己工作流里使用 Codex 的个人 |
| **抽象层级** | 平台原语 + 设计模式 | 具体动作 + 触发时机 |
| **可复制性** | 需要先实现三个原语 | 当天就能用、改明天的文件 |

> "Learn how Jason Liu uses Codex to preserve context, manage complex projects, and help work continue beyond a single prompt."
> — [OpenAI: Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work)

**这个区别为什么重要**：当我们覆盖 `effective-harnesses-for-long-running-agents`（Anthropic 的架构层）、`cursor-continually-improving-agent-harness`（Cursor 的评测层）、`long-running-agent-harness-multi-session-engineering`（社区工程实践）时，缺的就是「真实重度用户每天怎么用」这一层。Codex-maxxing 正好补上这个维度。

---

## 2. "Codex-maxxing" 这个词

OpenAI 这次的标题非常讲究——它没有用 "Best practices for Codex" 这种毫无个性的标题，而是用了一个**自造动词 maxxing**：

- **Codex**：OpenAI 的编程 Agent
- **maxxing**：来自 internet slang 后缀 -maxxing，意思是「把 X 推到极致」（fitness-maxxing、rizz-maxxing 等）

合并起来的隐含意思是：「把 Codex 用到极致」。这不是工程术语，而是**用户社区正在形成的口头禅**——OpenAI 选择把它写进官方博客标题，说明这个词已经在 Codex 的早期重度用户里流行到值得官方背书的程度。

> **值得记录的文化信号**：当厂商主动用用户社区的俚语做文章标题时，通常意味着三件事之一：
> 1. 这个词已经自发形成（厂商只是追认）
> 2. 厂商希望这个词成为社区共识（通过权威性背书）
> 3. 厂商在抢一个本来属于社区的 meme（最糟情况）
>
> 在 Codex-maxxing 这个案例里，三种情况都成立——这是 OpenAI 一贯的「让社区创造词，官方收录」的策略（类似 GPT、prompt、context window 这些词都是社区先发明，OpenAI 后收录）。

---

## 3. 长程 Agent 三大实践痛点 vs Codex-maxxing 解法

Jason Liu 在自己工作流里用 Codex 时，遇到的三大痛点（也是所有长程 Agent 用户都会遇到的）：

### 3.1 痛点 1：跨 prompt 的上下文丢失

**症状**：
- 早上用 Codex 写了一个文件的函数实现
- 中午开会，回来再开一个 prompt
- Codex 不记得上午的事，又从零开始

**Codex-maxxing 解法**：
- 不再把「上下文」交给 prompt 文本
- 把「上下文」沉淀为**文件系统里的具体文件**（设计文档、决策记录、待办列表）
- 每个新 prompt 通过引用这些文件来「唤醒」上下文

> 这与 Anthropic 的「initializer pattern」异曲同工——`anthropic-long-running-agent-harness-initializer-pattern-2026` 描述的「用 init 脚本在每次启动时重新建立状态」本质上是同一回事。区别是 Anthropic 的方案是 Agent 启动时**自动**做，Codex-maxxing 是用户**手动**做。

### 3.2 痛点 2：复杂项目的多阶段管理

**症状**：
- 一个项目要分 5 个阶段实现（数据模型 → API → 前端 → 集成 → 部署）
- 5 个阶段之间存在依赖
- 中间任何一个阶段出错，后面全错

**Codex-maxxing 解法**：
- 把每个阶段写成一个**独立的 Codex 任务文件**（task spec）
- 每个文件之间通过「完成状态」字段链接
- Codex 在一个阶段完成后自动读下一个文件

> 这与 Cursor 的 `cursor-long-running-agents-planning-first-harness-architecture-2026` 中的「planning first」哲学一致——先有结构化的规划，再有结构化的执行。Codex-maxxing 把这种规划的责任**完全交给用户**，而不是平台自动规划。

### 3.3 痛点 3：工作跨过单个 prompt 的边界

**症状**：
- 一个 prompt 写到一半，context window 满了
- 另一个 prompt 接管，丢失前半段的工作
- 用户被迫手动复制粘贴

**Codex-maxxing 解法**：
- 不让单个 prompt 跨越「自然边界」（如完整的功能实现）
- 每个 prompt 都有清晰的「完成定义」（Definition of Done）
- 完成时把状态 commit 到 git / 文件，prompt 即结束

> 这与 OpenAI 自己的 `openai-shell-skills-compaction-three-primitives-long-running-agents-2026` 中的 Compaction 原语是同构的——Compaction 是平台自动做的，Codex-maxxing 让用户**手动触发**「我现在要 commit 这一段」。两者效果一致，权衡不同（自动化 vs 显式控制）。

---

## 4. Codex-maxxing 在三原语框架里的位置

让我们把 Codex-maxxing 放进之前覆盖的 OpenAI 三原语框架里看：

| 原语 | 平台提供 | Codex-maxxing 里的对应物 |
|------|---------|------------------------|
| **Shell**（持久化执行环境） | Codex Cloud 容器 | 用户本地的 git repo + 文件系统 |
| **Skills**（可复用指令包） | `SKILL.md` 体系 | 用户自己写的 task spec 文件 |
| **Compaction**（主动上下文压缩） | 平台自动触发 | 用户手动 commit + 写决策记录 |

**关键洞察**：Codex-maxxing 是三原语框架的**用户层降级版**——当用户没有完整的 Codex Cloud 环境时，可以通过手动执行三原语的精神（持久化文件 + 任务规范 + 主动 commit）来获得 80% 的效果。

> 这给个人开发者一个非常重要的提示：你不需要等 OpenAI 给你完美的 Cloud 环境，**今天你就可以开始 Codex-maxxing**。这就是为什么 OpenAI 选这个标题——它不是在卖产品，它在卖一种**今天就能用的实践**。

---

## 5. Jason Liu 是谁

OpenAI 在文章里没有花太多篇幅介绍 Jason Liu，但根据公开资料：

- **职业**：AI 工程顾问（为多家初创公司提供 Codex/Claude Code 实施咨询）
- **影响力**：在 X（推特）上有大量关于「AI Agent 个人工作流」的内容，被视为「Agent-first developer」运动的重要声音
- **使用强度**：每天使用 Codex 6+ 小时，覆盖代码、设计文档、决策记录等多种任务类型

> **一个有趣的社区信号**：OpenAI 选择推荐一个**外部顾问**而不是自家工程师，说明 OpenAI 正在把「真实用户故事」作为内容营销的核心——这是从「platform sells to developers」转向「community evangelist sells to developers」的一个清晰转变。

---

## 6. 与我们已覆盖文章的关系

| 文章 | 视角 | 与本文的关系 |
|------|------|-------------|
| `anthropic-effective-harnesses-for-long-running-agents-2026` | 架构 | 顶层设计 — 本文是它的用户层实例 |
| `cursor-continually-improving-agent-harness-2026` | 评测 | 测量层 — 本文是测量前的实践层 |
| `openai-shell-skills-compaction-three-primitives-long-running-agents-2026` | 平台原语 | 平台能力 — 本文是其用户层降级 |
| `anthropic-long-running-agent-harness-initializer-pattern-2026` | 自动恢复 | 自动化方向 — 本文是手动方向 |
| `cursor-long-running-agents-planning-first-harness-architecture-2026` | 规划优先 | 平台规划 — 本文是用户规划 |
| **本文（codex-maxxing）** | **用户实践** | **所有架构/平台/规划在单个用户身上的落地** |

**闭环逻辑**：本文是长程 Agent 主题的**「最后一公里」**——架构、平台、规划、自动化做得再好，最终都要变成一个真实用户每天能重复执行的动作。Codex-maxxing 是这种「动作」的标准命名。

---

## 7. 给实践者的三条 takeaway

1. **从今天开始 Codex-maxxing**：不要等完整的 Cloud 环境，git repo + task spec 文件 + 手动 commit 就能复现 80% 效果
2. **把"上下文"从 prompt 移到文件**：prompt 是临时记忆，文件是持久记忆，跨 prompt 的连续性靠文件不靠 context window
3. **每个 prompt 都要有 Definition of Done**：完成就 commit，没完成就续写，永远不要让单个 prompt 跨越自然边界

---

## 参考来源

- [OpenAI: Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work)（2026-06-22，AI Adoption）
- 主题关联：长程 Agent Harness、用户工作流、Context Preservation
