# planning-with-files：崩溃安全的文件规划系统，23.4K Stars

> 当 AI Agent 的上下文窗口耗尽时，Session 里还有什么留下来？planning-with-files 的答案是：一套刻在磁盘上的 Markdown 文件，Agent 重启后依然能接着干。

---

## 基本信息

| 维度 | 内容 |
|------|------|
| **仓库** | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) |
| **Stars** | 23,400+ (2026年6月) |
| **语言** | Python (工具脚本) + Markdown (规划格式) |
| **许可** | MIT |
| **维护者** | OthmanAdi |
| **兼容性** | Claude Code, Codex CLI, Cursor, OpenCode, Kiro 等 60+ Agent |
| **安装量** | SKILL.md 标准，NPM 一键安装 |

---

## 核心命题

AI Coding Agent 最脆弱的时刻不是它生成了错误代码——而是它**丢失了执行上下文**。

当你运行一个 50 步的研究任务，Agent 在第 32 步遇到 `/clear` 或 Session 重置，所有进度归零。这不是 bug，这是 Agent 设计上的根本矛盾：**上下文窗口是稀缺资源，而长时任务需要持久状态**。

planning-with-files 的解法极其朴素：**把状态写到文件里，而不是依赖模型的上下文**。

---

## 三个核心文件

### task_plan.md：任务分解

任务启动时，Agent 必须先创建任务计划。文件结构是强制性的 discipline：

```markdown
# Task Plan

## Phase 1: Research
- [x] Search for X
- [ ] Compare Y vs Z
- [ ] Document findings in findings.md

## Phase 2: Implementation
- [ ] Build core module
- [ ] Add tests
- [ ] Update progress.md
```

### findings.md：研究发现

每个阶段的发现单独记录，而不是散落在对话历史里：

```markdown
# Findings

## X (Phase 1)
- Source: ...
- Key insight: ...
- Confidence: High

## Y comparison with Z
- Y: pros/cons
- Z: pros/cons
- Recommendation: ...
```

### progress.md：执行日志

Agent 每个关键动作后必须更新进度文件。这不是日志，而是一个**确定性完成门**：只有当所有检查通过，Agent 才能认为任务完成。

---

## 崩溃恢复机制

planning-with-files 最重要的工程设计：**Session 重建时，Agent 先读文件，再决定从哪里继续**。

```bash
# init-session.sh 在 Agent 启动时自动检测是否存在规划文件
if [ -f "task_plan.md" ]; then
    echo "Found existing plan. Loading context..."
    python scripts/session-catchup.py
fi
```

`sess catchup.py` 会对比 `task_plan.md` 中的 checkbox 状态和 `progress.md` 中的最后一条记录，找出 gap 并重新同步。这意味着：

- Agent 崩溃重启后，**不需要重新理解项目背景**
- 人类可以在任何时刻检查 `findings.md` 了解当前进展
- 即使 Agent 生成了错误的中间结果，文件里的记录也保留了决策历史

---

## 与 Anthropic "Session is not the context window" 的呼应

Anthropic 在 2026 年 4 月的工程文章 "[Scaling Managed Agents](../deep-dives/anthropic-managed-agents-decoupling-brain-hands-2026.md)" 中提出了一个核心命题：

> "The session provides this same benefit, serving as a context object that lives **outside Claude's context window**. But rather than be stored within the sandbox or REPL, context is durably stored in the session log."

Anthropic 的解法是通过 `getEvents()` 接口让 Brain 可以查询外部 Session。但这个方案需要平台级支持（Managed Agents 服务）。

**planning-with-files 走的是另一条路**：不需要平台级支持，用任何 Agent 都能读写的文件系统作为持久层。这是一种更通用的解法：

| 维度 | Anthropic Managed Agents Session | planning-with-files |
|------|----------------------------------|---------------------|
| **持久层** | 服务端 Session Log | 本地文件系统 |
| **查询接口** | `getEvents()` API | 直接读 Markdown 文件 |
| **跨 Agent** | 仅限 Managed Agents | 60+ Agent 通用 |
| **实现复杂度** | 需要平台基础设施 | 纯文件系统 |
| **适用场景** | 企业托管 Agent | 任意本地/云端 Agent |

---

## 为什么这是 SKILL.md 范式的成功案例

planning-with-files 是 SKILL.md 标准的最佳代言：

- **安装即用**：`npx skills add https://github.com/...` 完成安装
- **Agent 自发现**：Agent 扫描 `.opencode/skills/` 目录自动加载
- **触发词驱动**：用户说"帮我规划""分解任务"时自动激活
- **无平台依赖**：SKILL.md 是开放标准，任何实现 SKILL.md 的 Agent 都能用

这与 Google ADK 的企业 SDK 路线形成鲜明对比：**一条是开放生态，一条是企业集成**。

---

## 适用场景

**推荐使用 planning-with-files 的场景：**
- 长时研究任务（5+ 步骤，跨越多个 Session）
- 需要人类随时介入检查进展的项目
- 在多个 Agent 之间共享任务状态（Claude Code 写代码，Cursor 做 UI，人类审核）
- Context 窗口经常被强制重置的环境

**考虑其他方案的场景：**
- 短时一次性任务 → 不需要，直接干
- 需要企业级审计和访问控制 → ADK Session 或 Managed Agents
- 需要结构化数据库查询 → ADK + SQL 数据库

---

## 相关资源

- [GitHub: OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)
- [SKILL.md 标准文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/)
- [Manus Agent](https://manus.im/) — planning-with-files 最初的设计灵感来源
- [SKILLSMP 页面](https://skillsmp.com/creators/othmanadi/planning-with-files/opencode-skills-planning-with-files)

---

## 关联阅读

- [Anthropic Managed Agents：三组件解耦](../deep-dives/anthropic-managed-agents-decoupling-brain-hands-2026.md) — Platform 级 Session 持久化
- [Google ADK：四语言 Agent 工具包](./google-adk-python-four-language-agent-kit-20k-stars-2026.md) — 企业级多语言 Agent 框架

---

*本篇于 R488 (2026-06-22) 收录。数据来源：SKILLSMP、GitHub、awesomeskill.ai。*
