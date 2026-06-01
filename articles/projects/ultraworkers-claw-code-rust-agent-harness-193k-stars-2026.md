# ultraworkers/claw-code：人类设定方向，Claw 执行劳动

> **来源**: GitHub — [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code) | 193,025 ★ | MIT License | Created 2026-03-31

> **关联 Article**: [Agent Harness 的商品化与 Entangled Software 的崛起](#) — claw-code 是 Harness 工程化的实战案例

---

## 核心命题

当行业还在争论「Harness 该厚还是该薄」的时候，claw-code 已经在解决一个更根本的问题：**如何让 Agent 从「需要人类盯着」变成「人类设定方向后自主执行」**。

这个项目是 Rust 实现的 CLI Agent Harness，核心哲学只有一句话：

> "Humans set direction; claws perform the labor."

---

## 为什么这个项目值得关注

### 193K Stars 的爆发式增长

| 指标 | 数值 |
|------|------|
| Stars | 193,025 |
| Forks | 109,981 |
| 创建时间 | 2026-03-31 |
| 达到 100K Stars | 历史最快 |
| License | MIT |

这个增长曲线本身就说明问题——社区用脚投票，说明它的设计击中了某个广泛的痛点。

### 三层架构：把「人类接口」从终端中解放出来

claw-code 不是一个人盯着终端的 AI  Coding 工具。它的架构把人类从 Terminal 中解耦出来：

| 组件 | 定位 | 作用 |
|------|------|------|
| **OmX** (oh-my-codex) | Workflow 层 | 把短指令转成结构化执行协议（Planning + Execution Modes + 验证循环）|
| **clawhip** | 事件路由器 | 监控 git/tmux/GitHub Issues 的事件流，把通知推送到 Discord 等频道 |
| **OmO** (oh-my-openagent) | 多 Agent 协调 | 规划、Handoff、争议解决、验证 |

原文：

> "A person can type a sentence from a phone, walk away, sleep, or do something else. The claws read the directive, break it into tasks, assign roles, write code, run tests, argue over failures, recover, and push when the work passes."

这就是「Entangled Software」的一种具体形态——**人类从「监控者」变成「方向设定者」**，Agent 系统从每次执行中学习并自主推进。

---

## 工程化痛点的直面解决

README 里的 Roadmap 部分非常坦诚地列出了当前行业的 7 个工程化痛点，claw-code 正在逐个解决：

### 痛点 1：Session Boot 是脆弱的

- Trust prompts 可能阻塞 TUI 启动
- Prompts 可能落在 shell 而不是 coding agent
- "Session exists" ≠ "Session is ready"

### 痛点 2：真相分裂在多个层

- tmux 状态
- clawhip 事件流
- git/worktree 状态
- test 状态
- gateway/plugin/MCP 运行时状态

### 痛点 3：事件太像日志

- 当前 Agent 从嘈杂的文本中推断太多
- 重要状态没有被规范成机器可读事件

### 痛点 4：恢复循环太手动

需要人类介入的 recovery 流程：
1. restart worker
2. accept trust prompt
3. re-inject prompt
4. detect stale branch
5. retry failed startup
6. classify infra vs code failures

### 痛点 5：Branch Freshness 未被充分强制

侧分支可能错过 main 上已经修复的问题。

### 痛点 6：Plugin/MCP 失败未被充分分类

启动失败、握手失败、配置错误、部分启动、降级模式——这些状态没有清晰暴露。

### 痛点 7：人类 UX 仍在泄漏到 claw 工作流

太多行为依赖 Terminal/TUI，而不是显式的 Agent 状态转换和控制 API。

---

## 笔者的判断

### 为什么 claw-code 与 Entangled Software 文章形成闭环

上一篇文章说：**价值的锚点从「构建工具」转向「数据积累 + 行为适应」**。claw-code 给出了一个具体的工程实现路径：

1. **行为适应**：通过 clawhip 事件流，Agent 从每次执行中积累状态认知
2. **方向设定者而非监控者**：人类从 Terminal 中解放，设定方向后走开
3. **多 Agent 协调**：OmO 处理 Planning/Handoff/争议解决，这是「Entangled」的多 Agent 版本

### 与同类项目的差异

| 项目 | 特点 | 与 claw-code 的差异 |
|------|------|---------------------|
| **Claude Code** | 官方 CLI，单 Agent | claw-code 是多 Agent 协调（OmO），支持并行任务分配 |
| **Cursor Agent** | IDE 内嵌 | claw-code 是纯 CLI，Discord 是主要接口 |
| **OpenAI Agent SDK** | 轻量 Harness | claw-code 的 Rust 实现更强调性能和确定性 |
| **CrewAI** | 多 Agent 编排 | claw-code 更底层（Rust），更强调事件驱动和状态机 |

### 适用场景

- 需要**多 Agent 并行执行**的复杂任务
- 团队需要**从监控者转向方向设定者**的工作流转型
- 需要**事件驱动的可观测性**的 Agent 系统
- 追求**高性能、高确定性**的 Rust 技术栈团队

### 不适用场景

- 单 Agent 简单任务（用 Claude Code 更直接）
- 依赖 IDE 交互的开发者（claw-code 是纯 CLI）
- 对 Rust 生态系统不熟悉的团队

### 核心亮点（金句）

> "The real human interface is a Discord channel." — 这句话揭示了 Agent 系统的终极形态：人类不需要盯着终端，设定好方向，剩下的交给 Claw。

---

> **引用来源**：
> - [ultraworkers/claw-code README](https://github.com/ultraworkers/claw-code) — "Humans set direction; claws perform the labor"
> - [PHILOSOPHY.md](https://github.com/ultraworkers/claw-code/blob/main/PHILOSOPHY.md) — "The real thing worth studying is the system that produced them"
> - [ROADMAP.md](https://github.com/ultraworkers/claw-code/blob/main/ROADMAP.md) — "Turn claw-code into the most clawable coding harness"