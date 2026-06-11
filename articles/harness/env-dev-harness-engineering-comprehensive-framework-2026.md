# Agent = Model + Harness：Harness Engineering 全框架解析

> **核心论点**：让一个 AI Agent 从"聊天"变成"可信赖的工作搭档"的，不是模型本身，而是围绕模型构建的那一层工程架构——Harness。相同的模型权重，不同的 Harness，产出质量的天花板可以相差一个量级。

---

## 背景：为什么 Harness Engineering突然重要了

Anthropic 2024 年12 月的论文《Building effective agents》说了一句当时没引起足够注意的话：**"Agent 的难点不在模型调用，而在循环、工具、恢复路径和评估"**。这句话的本质是：模型是通用品，Harness 才是专用品。

2025 年，行业开始广泛讨论这个现象：同一个 Claude Sonnet，在 Cursor 的 agent mode 里能完成复杂的多文件重构，在另一个产品里却连一个函数都改不对。差距不在模型，在 Harness。

Böckeler 在 Martin Fowler 网站的探索性文章中给出了一个极简公式：

> **Agent = Model + Harness**
>
> 模型是 Stateless Function：输入文本，输出文本。Agent 是模型 + 一个循环，这个循环能读文件、执行 Shell、调用 MCP Server、记住之前 session、被 Hook 拦截后重试。
>
> *— Birgitta Böckeler, "Exploring Generative AI", Thoughtworks / Martin Fowler*

这个公式是理解2026 年 AI Coding 工具竞争格局的总钥匙。

---

## Harness 的六个工程组件

Harness 不是"加个 System Prompt"那么简单。Böckeler 梳理了六个移动部件：

### 1. Tools —— Agent 能做什么

**工具设计是大多数 Harness 质量翻车的第一个节点。**

- 工具太少：Agent 发明不存在的文件路径
- 工具重叠：Agent 在两个功能相似的工具之间选错
- 工具描述模糊：Agent 花三个 Turn 争论而不做事

Model Context Protocol（MCP，Anthropic 2024 年 11 月发布）标准化了工具的 Wire Format，使得一个 Postgres MCP Server 可以不加修改地用于 Claude Code、Cursor、VS Code Agent Mode 和 Zed。但标准化的是接口，工具设计的质量仍然靠人。

### 2. Context —— 每轮 Token 预算的战斗

Context 窗口从 2023 年的 8K 增长到 2025 年的 1M+，但 Harness 仍然需要激进地管理 Context，原因有三个：

- **注意力退化**：模型对长上下文中靠前的内容注意力更强，靠后的会"被稀释"
- **Token 成本**：在生产规模下，每 1K Token 都是真实成本
- **信号噪声比**：20K Token 的5M Token 代码库中，真正与当前任务相关的可能只有 2K

Cursor 的 codebase indexer、Claude Code 的按需 Read 工具、Aider 的 repo map、Sourcegraph Cody 的图上下文，是四种不同的赌注——都在回答同一个问题：**现在应该让模型看到哪20K Token？**

答错这个问题，Agent 会幻觉出不存在的 Import；答对，Agent 第一次尝试就编辑正确的文件。

### 3. Hooks —— Harness 对模型的硬拦截

Hooks 是 Harness 在工具调用前/中/后运行的确定性脚本：

- 每次 Edit 后自动运行 Formatter（Biome、Prettier）
- Agent 声称任务完成前强制运行 Type Check
- Commit 前强制扫描 Secret（API Key、Token）
- 文件路径 Blocklist，拒绝操作特定目录

**Hooks 的核心价值：把模糊的 Prompt 指令（"运行 Biome"）变成硬保证（"Biome 必须运行，如果失败模型必须重新处理"）**。模型会忘记指令，但 Hook 不会。

Claude Code 的 `settings.json` Hook 系统、Cursor 的内置 Hook 机制，以及大多数内部工具团队构建的薄包装层，都是这个逻辑的不同实现。

### 4. Evaluators —— 告诉 Agent 错了

Evaluator 是 Harness 用来评判 Agent 每一步做得对不对的东西：

- 单元测试
- Linter
- Type Checker
- 编译
- Snapshot Diff
- **LLM-as-Judge**（用另一个模型评判当前模型的输出）
- 真人审批

SWE-bench 的数据是这个原则最有力的证明：2023 年底基准刚发布时得分是个位数，到 2025 年底 SWE-bench Verified 上突破 70%+——不是因为模型一夜之间聪明了 10 倍，而是因为 Harness 学会了运行测试套件、解析输出、把失败结果反馈给模型重试。

> **"Cheap, fast, deterministic evaluators beat a smarter model."**
>
> 便宜的、快速、确定性的 Evaluator，胜过更聪明的模型。
>
> *— Böckeler + SWE-bench结论*

模型不是在解决问题——是循环在解决问题。

### 5. Memory —— 跨 Session 活下去

Harness 中的 Memory 是任何存在于当前 Context Window 之外、能持久化的东西：

- 项目级 `CLAUDE.md`
- Cursor 的 `.cursor/rules/*.mdc`（已超越单文件的 `.cursorrules`）
- PGVector Store（向量化过往 Session）
- 结构化 Note 文件（Agent 在每个 Turn 结束时Rewrite）

**没有 Memory 的 Agent：每次新对话都要重新学习代码库。**
**有 Memory 的 Agent：携带代码规范、过往错误和用户偏好。**

风险是 Staleness（过时）：一份说"用 X Helper" 的 Memory，在 X 早已被删除之后，比没有 Memory 更糟。成熟的 Harness 会对 Memory 加时间戳，并在行动前验证。

### 6. Sandboxing —— 把爆炸半径关在笼子里

能跑 Shell 命令的 Agent 也能跑 `rm -rf`、`git push --force`、`curl | sh`。Sandboxing 是把 Agent 能触碰的范围加以限制的 Harness 层：

- 容器隔离（Devin、Codex CLI 的沙箱模式）
- 文件系统 Allowlist
- 网络出口控制
- 每个工具的 Permission Prompt
- 破坏性操作的 Dry-run模式

每增加一点自主权，就必须同时收紧一次沙箱。Claude Code 的 Auto-Accept 和 Plan 模式是这个轴上的显式旋钮。

> **信任来自验证，不来自希望。**

---

## 实战：构建一个 Harness 的务实顺序

文章给出了一个具体可操作的构建顺序：

```
1. 从一个工具开始。File Read。接循环，看模型怎么用，看它怎么失败。
   在失败原因不再是"看不到代码"之前，不要加第二个工具。

2. 加最便宜的 Evaluator。Linter、Type Checker、Build。
   任何确定性的东西。把失败结果 Pipe 回模型。

3. 加一个 Hook。Edit 后自动 Format。就这样。
   在模型犯同一个错两次之前，不要加更多。

4. 只有在后悔没有 Memory 时才加 Memory。
   第一个 CLAUDE.md 应该是5 行 Bullet Points，
   是模型每次都重新发现的东西，不是架构论文。

5. 在提升自主权之前先做沙箱。
   Auto-accept 模式没有沙箱 = 删除数据库。
   至少选一个：容器、Allowlist、Dry-run。

6. 每次改 Harness 都测回归。
   Harness 是软件，有 Bug。
   一个"有用"的新工具可能悄悄降低某类问题的成功率。
```

---

## 同模型不同 Harness：主流工具横比

| Harness | Tools | Context 策略 | 适用场景 |
|---------|-------|------------|---------|
| **Cursor Agent Mode** | In-editor edits, terminal, embeddings indexer | Codebase embeddings + active file | 编辑器内的 Pair Programming |
| **Claude Code** | File ops, shell, MCP, hooks, slash commands | On-demand reads + CLAUDE.md memory | 终端优先的自主任务 |
| **OpenAI Codex CLI** | File ops, shell, sandboxed exec | Repo map + selective reads | 开源参考 Harness |
| **Aider** | Edit blocks, repo map, git integration | Repo map + edit-block diffs | Git 原生 CLI 工作流 |
| **Devin (Cognition)** | Browser, shell, IDE — Full VMP | Persistent VM + long-running plans | 长时自主任务 |

每一个都基于相同的 Claude / GPT 权重，但产出质量完全不同——这是 Harness Engineering 这个术语成立的核心证据。

---

## 与前序文章的关联

本文是 AI Agent Engineering 基础设施系列的收尾文章，与前序形成完整闭环：

| Round | 核心主题 | 层级 |
|-------|---------|------|
| R326 | Agent生命周期与 Trust Boundary | 生命周期 |
| R327 | 模型无关的防御机制 | 防御机制 |
| R328 | Harness Loop 与 Stop Condition | 控制流 |
| R329 | Evaluator Loop 与 GAIA Benchmark | 评估-控制 |
| R330 | 研究自动化中的多 Agent 编排 | 研究自动化 |
| R331 | Harness Engineering = 质量基础设施 | 基础设施 |
| R332 | Codex App Server = 平台 API 层 | 平台架构 |
| R333 | Anthropic 三Agent = 职责分离架构 | 职责分离 |
| **R334** | **Harness Engineering 全框架 = 六个组件的系统性整合** | **系统整合** |

---

## 原文引用

> "Agent = Model + Harness. The model is the same Claude or GPT-class weights every competitor has. The harness is what turns a chat completion into something a senior engineer would let near a production repo."
>
> *— Birgitta Böckeler, "Exploring Generative AI", Martin Fowler (https://martinfowler.com/articles/exploring-gen-ai.html)*

> "The bottleneck moved. The hard parts of an agent are not the model calls — they are the loop, the tools, the recovery paths, and the evaluation."
>
> *— Anthropic, "Building effective agents" (December 2024, https://www.anthropic.com/research/building-effective-agents)*

> "Cheap, fast, deterministic evaluators beat a smarter model. SWE-bench scores climbed from low single digits to 70%+ range — not because the underlying models are an order of magnitude smarter, but because harnesses learned to run the test suite."
>
> *— Böckeler analysis + SWE-bench results (https://www.swebench.com/)*

---

## 结论

Harness Engineering 不是一个"配置"工作，是一个**工程学科**。它的六个组件——Tools、Context、Hooks、Evaluators、Memory、Sandboxing——每一个都需要独立的设计、迭代和测试。

2026 年的竞争格局已经清晰：**模型是入场券，Harness 才是差异化所在**。能给团队带来的价值，不在于选哪个模型，而在于花多少工程投入在 Harness 上。

**构建一个生产级 Harness 的顺序：工具 → Evaluator → Hook → Memory → Sandboxing → 测量回归。每一步都要独立迭代，不要试图一次性到位。**