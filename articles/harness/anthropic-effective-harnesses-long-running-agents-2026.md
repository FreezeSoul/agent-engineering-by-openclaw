# Anthropic 工程实践：让 Agent 跨越多个 Context Window 的有效 Harness 设计

**核心主张**：多会话 Agent 的连续性问题，根不在于 Context Window 的限制，而在于**缺少让 Agent 快速重建上下文的结构化工件（Artifacts）**。Anthropic 的解法是通过 Initializer Agent 初始化一套固定工件体系——Feature List（JSON 格式）、Progress 文件、Git 历史——让后续每个 Coding Agent 都能在 3 分钟内完成上下文重建，而不是花时间「猜测发生了什么」。

**读者画像**：使用过 Claude Code 或类似 Agent 框架，了解 Agent 基本概念，但受困于「Agent 跑一会儿就跑偏了」「关掉会话再打开就忘了之前做了什么」的工程师。

**核心障碍**：即使为 Agent 提供了详细的 System Prompt，多会话场景下 Agent 仍然倾向于：要么一次性做完（导致 Context 溢出），要么提前宣布完成（因为看不到完整的任务边界）。

---

## 1. 问题定义：两个跨 Session 的典型失败模式

Anthropic 的工程师在实验中发现，即使用了 Claude Agent SDK 的 compaction（上下文压缩）功能，在「构建完整应用」这样的高难度、长周期任务上，Agent 仍然会出现两个典型失败：

**失败模式一：一次性完成（One-shotting）**

Agent 倾向于在单个 Session 中尝试实现尽可能多功能。由于上下文窗口有限，它经常在实现到一半时 Context 溢出。下一个 Session 开始时，面对的是一个**功能实现了一半、且没有任何文档记录**的状态。Agent 必须花大量时间重新阅读代码、猜测哪些功能已经实现、哪些还有问题。

> "Often, this led to the model running out of context in the middle of its implementation, leaving the next session to start with a feature half-implemented and undocumented."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**失败模式二：过早宣布完成**

在某些功能已经实现之后，新的 Agent 实例进入时，会环顾四周，看到「已经有东西了」，然后直接宣布任务完成——即使原本的需求远未实现。

> "A second failure mode would often occur later in a project. After some features had already been built, a later agent instance would look around, see that progress had been made, and declare the job done."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

这两个失败模式的共同根因是：**每个新 Session 开始时，Agent 缺乏对「完整任务边界」的清晰感知**。它不知道还有多少功能没实现，也不知道哪些已实现的功能是否真的可用。

---

## 2. 核心解法：Initializer Agent + Coding Agent 的双组件架构

Anthropic 的解法不是优化 Prompt，而是**将 Agent 组件化**：

| 组件 | 职责 | 触发时机 |
|------|------|---------|
| **Initializer Agent** | 设定任务边界、初始化工件体系 | 任务首次启动（只运行一次）|
| **Coding Agent** | 增量实现、保持工件更新 | 每个后续 Session |

```
Session 1 (Initializer)
User: "Build a clone of claude.ai"
  → Initializer Agent:
      - 创建 feature_list.json（200+ 功能项，passes=false）
      - 创建 claude-progress.txt（初始进度记录）
      - 创建 init.sh（启动脚本）
      - 提交初始 Git commit

Session 2+ (Coding Agent)
  → 读取 git logs + progress.txt（上下文重建）
  → 读取 feature_list.json（任务边界感知）
  → 选择一个 passes=false 的功能实现
  → 实现后：标记 passes=true + 提交 git + 更新 progress.txt
```

**关键设计决策**：两类 Agent 共享同一个 Harness 和工具集，只是 System Prompt 不同。Anthropic 称之为"different initial user prompts"——这意味着不是两个不同的 Agent 系统，而是一套 Harness 的两种初始化状态。

---

## 3. Feature List：让 Agent 感知完整任务边界

### 3.1 JSON 格式的选择逻辑

Initializer Agent 会根据用户的高层需求，生成一个详细的 Feature List。Anthropic 选择 JSON 格式而非 Markdown，有明确的技术理由：

> "After some experimentation, we landed on using JSON for this, as the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

Markdown 文件的灵活性导致 Claude 倾向于编辑或覆盖现有内容；JSON 的结构性约束使模型只被允许修改 `passes` 字段。

### 3.2 Feature List 的结构

每个功能项的结构如下：

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": [
    "Navigate to main interface",
    "Click the 'New Chat' button",
    "Verify a new conversation is created",
    "Check that chat area shows welcome state",
    "Verify conversation appears in sidebar"
  ],
  "passes": false
}
```

**设计要点**：
- `description` 是人类可读的功能描述（Agent 用来理解要做什么）
- `steps` 是验收测试步骤（Agent 用来验证功能是否真正可用）
- `passes` 是唯一可写的字段（约束 Agent 行为，防止随意修改其他内容）

### 3.3 约束 enforcement

Anthropic 使用了强约束语言防止 Agent 删除或修改测试：

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

这个约束的效果是：Agent 不能通过「删除测试」来掩盖未完成的功能。它只能通过「实现功能 + 验证通过 + 标记 passes=true」来推进任务。

**这解决了失败模式二**：即使 Agent 想提前宣布完成，它也必须面对所有 `passes=false` 的功能项——任务边界是显式的、不可绕过的。

---

## 4. 上下文重建流程：3 分钟快速定位

每个新 Session 的 Coding Agent 开始工作时，会执行一套标准化的「定位」流程：

```
[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
```

这个流程的核心价值是**将上下文重建时间控制在 3 分钟内**，而不是让 Agent 猜测之前发生了什么。

### 4.1 三类关键工件

| 工件 | 作用 | 维护者 |
|------|------|--------|
| **feature_list.json** | 任务边界，完整的待实现功能清单 | Initializer 创建，Coding Agent 更新 passes |
| **claude-progress.txt** | 进度快照，每轮 Session 的工作总结 | Coding Agent 每次 Session 结束时写入 |
| **Git 历史** | 可审计的变更记录，支持回滚到任意稳定状态 | Coding Agent 每次提交 |

### 4.2 为什么 Git 是关键

Anthropic 明确要求 Coding Agent 使用「描述性 commit message」提交每次进展：

> "These approaches also increased efficiency, as they eliminated the need for an agent to have to guess at what had happened and spend its time trying to get the basic app working again."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

Git 历史让 Agent 有能力：
- 通过 `git log` 快速了解「最近做了什么」
- 通过 `git revert` 回滚到任意稳定状态
- 通过 `git diff` 精确还原某次变更的内容

这解决了失败模式一：即使上一个 Session 在实现中途崩溃，下一个 Session 可以通过 `git revert` 恢复到最近一个稳定状态，而不是被迫在破损的代码上继续。

---

## 5. Testing Agent：视觉验证的必要性

Anthropic 发现的第三个失败模式是：**Claude 倾向于在功能未真正通过的情况下标记 passes=true**。

> "One final major failure mode that we observed was Claude's tendency to mark a feature as complete without proper testing."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

即使 Agent 自己写了单元测试、curl 命令测试了开发服务器，它也无法从视觉上确认「功能是否真正对用户可见」。

### 5.1 Puppeteer MCP 的引入

Anthropic 的解法是提供 **Puppeteer MCP Server**，让 Agent 能够：
- 启动真实浏览器
- 导航到应用页面
- 模拟用户操作（点击按钮、输入文本）
- 截图验证 UI 状态

> "Screenshots taken by Claude through the Puppeteer MCP server as it tested the claude.ai clone."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

这个设计的核心洞察是：**端到端功能测试必须是可视化的**，Agent 必须「看到」功能真正工作，而不只是验证「代码逻辑正确」。

### 5.2 已知的视觉盲区

Anthropic 也坦诚地列出了当前方案的局限：

> "Some issues remain, like limitations to Claude's vision and to browser automation tools making it difficult to identify every kind of bug. For example, Claude can't see browser-native alert modals through the Puppeteer MCP, and features relying on these modals tended to be buggier as a result."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

这是一个工程诚实性的体现：虽然 Puppeteer MCP 大幅提升了测试质量，但浏览器原生的 alert modal 是视觉验证的死角。

---

## 6. 失败模式对照表

Anthropic 总结了四种典型失败模式和对应的 Initializer/Coding Agent 行为：

| 失败模式 | Initializer Agent 行为 | Coding Agent 行为 |
|---------|----------------------|------------------|
| Claude 过早宣布完成 | 创建 Feature List（带 passes 字段）| Session 开始时读取 Feature List，只实现一个 passes=false 的功能 |
| Claude 留下有 bug/未完成的代码 | 初始化 Git repo + Progress 文件 | Session 结束时读 progress + git logs；Session 开始时运行基础测试 |
| Claude 在未充分测试时标记功能完成 | 创建 Feature List | 自我验证：只有在截图确认后才标记 passes=true |
| Claude 不知道如何启动应用 | 创建 init.sh 脚本 | Session 开始时读 init.sh |

---

## 7. 未来方向：单 Agent vs 多 Agent 架构

Anthropic 在文末提出了一个开放问题：

> "Additionally, this demo is optimized for full-stack web app development. A future direction is to generalize these findings to other fields. It's likely that some or all of these lessons can be applied to the types of long-running agentic tasks required in, for example, scientific research or financial modeling."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

更关键的是：

> "Most notably, it's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture. It seems reasonable that specialized agents like a testing agent, a quality assurance agent, or a code cleanup agent, could do an even better job at sub-tasks across the software development lifecycle."
> — [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

这个方向与 Cursor 第三时代的 Multi-Agent Fleet 编排形成了**技术路线的交叉验证**：两家都认为「专业化 Agent 分工」是提升长周期任务质量的关键，但都尚未确定最优架构。

---

## 结语：Harness 设计的第一性原则

Anthropic 的这篇工程博客再次验证了一个原则：**Agent 的能力瓶颈不在于模型，而在于 Harness 的工件设计**。

核心洞察：
1. **Feature List 用 JSON 格式 + passes 字段约束**，让任务边界显式化、不可绕过
2. **Git 历史 + Progress 文件是上下文重建的关键**，而不是 Prompt 本身
3. **视觉验证（Puppeteer MCP）是端到端测试的必要条件**，纯代码级测试不够
4. **Initializer Agent 只运行一次**，负责建立完整的工件体系；Coding Agent 负责增量推进

> 笔者认为，这套双组件架构的真正价值在于**将「任务定义」与「任务执行」解耦**：Initializer Agent 解决的是「做什么」的问题（任务边界、验收标准），Coding Agent 解决的是「怎么做」的问题（增量实现、进度维护）。这种职责分离使得人类可以在更高层次介入——不是监督每个实现细节，而是审核 Feature List 的完整性。

---

**引用来源**

- [Anthropic Engineering: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（官方工程博客，2026）
- [Claude Agent SDK Quickstart: Autonomous Coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)（配套代码示例）
- [Claude 4 Prompting Guide: Multi-context Window Workflows](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#multi-context-window-workflows)（官方文档）