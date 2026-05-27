# akitaonrails/ai-memory：让 AI Agent 真正拥有持久记忆的跨厂商交接方案

> 321 Stars · MIT License · Rust · [GitHub](https://github.com/akitaonrails/ai-memory)

![GitHub](screenshots/akitaonrails-ai-memory-cross-agent-handoff-321-stars-2026.png)

## 核心命题

**做对了什么**：解决了 AI Agent 领域一个长期被忽视的问题——跨厂商 Agent 的上下文连续性。当你在 Claude Code 中途停下来，换用 OpenAI Codex 或 Cursor 时，ai-memory 能让下一个 Agent 直接看到「上次在哪里、失败了什么、下一步该做什么」，无需重新解释架构或手动加载上下文。

真正的问题是：厂商绑定的 Agent 生态里，每个 CLI 都有自己的 session 管理方式，没有任何一个厂商愿意让用户无痛切换。ai-memory 用一个**与模型无关的持久 wiki 层**，打破了这个锁定。

## 一、项目定位：上下文持久化的第三条路

### 行业现状的三种路径

| 路径 | 代表方案 | 核心思路 | 问题 |
|------|---------|---------|------|
| **向量数据库** | Pinecone / Weaviate / Qdrant | Embedding 相似性检索 | 需要额外基础设施，检索结果不稳定，维护成本高 |
| **手动记录** | `write_note` / 粘贴上下文 | 用户显式写入记忆 | 依赖人工，容易遗漏，不可复用 |
| **厂商自带** | Claude Memory / OpenAI Memory | 厂商私有记忆服务 | 锁定特定厂商，无法跨厂商使用 |

ai-memory 走的是**第四条路**：基于 git 版本化的纯 Markdown wiki，配 FTS5 全文搜索，不需要向量数据库，不需要人工干预。Session 结束时自动将 prompt + tool calls + decision 编译成连贯的叙事页面，写入本地 git 仓库。

### 笔者的判断

向量数据库方案在 RAG 场景有效，但对 Agent 的 session 记忆而言是**过度设计**——你要的不是在全量知识库里找相似段落，而是精确还原「上一次 session 的工作状态」。纯文本 + 全文搜索对这个需求的匹配度，远高于向量检索。

## 二、核心机制解析

### 1. 生命周期钩子（Zero-friction Capture）

ai-memory 在各厂商 Agent 的生命周期节点上埋入钩子，自动捕获数据：

```
SessionStart → SessionEnd → PreCompact → PostCompact → ...
```

每个钩子触发时：
- **Prompt**：被记录的原始指令
- **Tool Calls**：所有工具调用及参数
- **Decision**：Agent 作出的关键决策
- **Session Boundary**：session 开始/结束的时间戳

数据以 fire-and-forget 方式发送，不阻塞 Agent 主流程。

### 2. Karpathy 风格的 LLM Wiki

这是整个系统最聪明的地方。Session 结束后，数据不是以原始日志形式存储，而是由 LLM 编译成**连贯的叙事页面**：

```markdown
# Project: agent-engineering-by-openclaw
# Last Session: 2026-05-27 14:32 - 16:47

## Where We Left Off
- Working on the harness engineering article structure
- Identified a gap in checkpoint/resume coverage
- [ ] Need to verify OpenAI Codex sandbox behavior on Windows

## Decisions Made
- Chose snapshotting over incremental git commits for performance
- Abandoned progress file approach due to race conditions

## Open Questions
- How does rehydrate interact with MCP tool state?
```

这种格式的价值在于：**下一个 Agent 拿到的是「连贯的思维过程」，而不是一堆分散的工具调用日志**。你可以把这个思路追溯到 Andrej Karpathy 在 Tesla 时代的「记录 AI 决策过程」实践——ai-memory 将这个理念工程化了。

### 3. Cross-agent Handoff

这是 ai-memory 与其他方案最大的差异化能力：

```bash
# 在 Claude Code 中工作到 4 PM，按下 Ctrl+C
$ ^C
# ai-memory 自动写入 handoff wiki

# 第二天 9 AM，换用 Codex
$ codex .
# Codex SessionStart 钩子触发
# 自动 prepend 以下内容到第一个 prompt：
#
# ## Previous Session Handoff
# From Claude Code (2026-05-26 16:47):
# - Working on harness engineering article...
# - Found gap in checkpoint coverage...
# - Next step: verify Windows sandbox behavior...
```

**支持的 Agent**：Claude Code、Codex、OpenCode、Cursor、Gemini CLI、Antigravity CLI、OpenClaw、Oh My Pi。

### 4. Git 版本化的时间旅行

所有 wiki 页面都存在 git 仓库里，意味着：

```bash
git log --oneline --since="6 weeks ago" -- articles/
# 可以回溯任意时间点的 Agent 记忆状态
git show abc123:path/to/page.md  # 还原历史版本
```

这个设计让 ai-memory 的输出既是人可读的，也是机器可查询的，还是版本可控的。三个需求用同一个 git 仓库满足，没有额外基础设施。

## 三、技术架构

### 项目隔离策略

ai-memory 通过 `<wiki_root>/<workspace_id>/<project_id>/` 的目录结构实现项目隔离：

- `workspace`：默认为 `"default"`，可配置
- `project_id`：默认为 `$cwd` 的 basename
- 只需在项目根目录放置 `.ai-memory.toml` 标记文件，即可覆盖默认配置

### 支持矩阵

| 维度 | 状态 |
|------|------|
| **Claude Code** | ✅ MCP config + lifecycle hooks |
| **Codex** | ✅ MCP config + lifecycle hooks |
| **OpenCode** | ✅ Remote MCP config |
| **Cursor** | ✅ MCP config + lifecycle hooks |
| **Gemini CLI** | ✅ MCP config |
| **OpenClaw** | ✅ MCP config + native plugin lifecycle hooks |
| **Antigravity CLI** | ✅ MCP config + lifecycle hooks |
| **Linux/macOS** | ✅ 原生支持 + Docker 镜像 |
| **Windows (WSL2)** | ✅ 推荐路径 |
| **Native Windows** | ⚠️ 实验性 |

### 无 LLM 模式

即使不配置 LLM provider，ai-memory 仍然提供：
- FTS5 全文搜索
- 基于规则的摘要生成
- Git 版本化的时间旅行

LLM 是**增强选项**，不是必选项。这个设计让项目在纯搜索场景下也有实际价值。

## 四、与现有知识体系的关联

ai-memory 填补了我们知识库中**跨厂商 Agent 交接**的空白。以下文章与它形成闭环：

- `articles/context-memory/akitaonrails-ai-memory-cross-agent-handoff-260-stars-2026.md` ← **同一项目，更早版本**
- `articles/fundamentals/claude-code-goal-evaluator-loop-as-first-class-interface-2026.md`：goal/evaluator loop 的长任务连续性问题
- `articles/orchestration/anthropic-multi-agent-orchestration-engineering-2026.md`：多 Agent 协作的上下文传递问题

## 五、适用场景

### 适合使用 ai-memory 的场景

- **多厂商 Agent 混用**：团队内有人用 Claude Code，有人用 Cursor，有人用 Codex
- **长任务跨天继续**：当天做到一半，第二天继续时需要快速重建上下文
- **项目知识沉淀**：不只是 session 记忆，还需要将重要决策永久记录
- **多机器协作**：开发机记录的内容，需要在服务器或 CI 环境中可查

### 不适合的场景

- **单厂商单 session**：只用一个 Agent，不换厂商、不跨天使用 → 厂商自带 Memory 够用
- **需要全量知识库检索**：向量数据库方案更适合大规模语义搜索
- **已有完善的上下文管理方案**：如已经用 git commit 作为 checkpoint，不必要再加一层

## 六、笔者判断

ai-memory 的核心价值不是「记忆」，而是**上下文连续性的标准化**。在 Agent 生态割裂的当下，能够让 Claude Code → Codex → Cursor → Gemini CLI 的交接标准化，是一件工程价值极高的事情。

它的设计哲学值得学习：**不引入额外的向量数据库，不依赖厂商私有 API，用现有的 git + markdown + FTS5 就能解决 80% 的需求**。这是典型的「正确性优先于花哨」工程选择。

值得关注的演进方向：
1. Windows 原生支持完善后，覆盖率将接近 100%
2. 多 Agent 并发写入同一个 wiki 的冲突处理
3. 与 MCP 协议更深的集成（MCP 目前是 remote-only，无 lifecycle hooks）

---

> 来源：GitHub README（直接获取）
> 项目地址：https://github.com/akitaonrails/ai-memory
> 相关概念：Cross-agent Handoff, Context Persistence, Agent Memory, Session Continuity, Multi-agent Orchestration