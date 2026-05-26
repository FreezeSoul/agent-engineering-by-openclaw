# akitaonrails/ai-memory：跨厂商 Agent 交接的 260 Stars 解决方案

> **核心命题**：ai-memory 用 260 行 Rust 代码解决了一个让所有多 Agent 团队头疼的问题——换班时 context 全部丢失。它把每次 session 的「遗留工作」变成可被下一个 Agent（无论是谁家的）读取的 Markdown 维基。

大多数 Agent 用户经历过这个场景：下午 4 点用 Claude Code 写到一半，晚上回家换成 OpenAI Codex，第二天早上再切回 Claude Code——每次都要重新解释「我们在做什么」「哪里卡住了」「之前的决策是什么」。

ai-memory[1] 用一个极简的工程思路解决这个问题：**每次 session 结束时，把所有关键信息压缩成一份「交接文档」，下个 session 开头自动 prepend 这个交接文档**。整个系统无需向量数据库，无需手动写笔记，产出物是可以用 `grep` 搜索的纯 Markdown 文件。

---

## 核心设计：SessionBoundary 触发 + Markdown 维基

ai-memory 的设计哲学围绕「session 边界」构建：

```
Session 开始 → 自动 prepend 交接文档 → Agent 工作 → Session 结束 → 触发压缩 → 写入维基
```

具体流程：

1. **Lifecycle Hooks 自动捕获**：Claude Code / Codex / OpenCode 等主流 Agent CLI 的生命周期钩子（SessionStart / SessionEnd）在后台运行，自动记录每次 prompt、tool call 和决策
2. **SessionEnd 触发压缩**：Session 结束时，运行一个 LLM 压缩步骤，把原始日志压缩成一段连贯的「叙事」——不再是流水账，而是一篇有结构的 Markdown 文档，记录了「我们在做什么」「哪里失败了」「接下来的计划」
3. **下一 Session 自动 prepend**：下次任何 Agent（无论品牌）连接到同一目录时，SessionStart hook 会自动把最新交接文档 prepend 到第一条 prompt 前面

这个设计的聪明之处在于**触发点选择**：不是靠人工触发（你永远不会记得每次都写交接文档），而是绑定到 session 边界（Claude Code 关掉 / Codex 启动），自动化程度高到用户无需改变任何习惯。

---

## 跨厂商支持：不做绑定，做中立层

ai-memory 支持的 Agent 数量令人意外：

| Agent | 支持状态 | 接入方式 |
|-------|---------|---------|
| Claude Code | ✅ 支持 | MCP config + lifecycle hooks |
| OpenAI Codex | ✅ 支持 | MCP config + lifecycle hooks |
| OpenCode | ✅ 支持 | MCP + generated TypeScript plugin |
| Cursor | ✅ 支持 | MCP config + lifecycle hooks |
| Gemini CLI | ✅ 支持 | MCP config |
| OpenClaw | ✅ 支持 | MCP config + native plugin hooks |
| Antigravity CLI | ✅ 支持 | MCP config + lifecycle hooks |
| Claude Desktop | ⚠️ MCP only | Uses mcp-remote |

**关键判断**：ai-memory 选择做一个**中立层**，而非绑定某个特定 Agent。这意味着它不会因为某个 Agent 厂商的策略变化而失效——如果明天 Claude Code 停止更新，Codex 用户仍然可以用同一套 wiki。

从工程视角看，这种中立性来自它的存储设计：wiki 是纯 Markdown 文件，存在 git 仓库里。git 版本控制天然提供了时间旅行能力（`git log` 查看历史版本），不需要额外的存储系统。

---

## 架构关键决策

### 1. 不用向量数据库

ai-memory 的 wiki 存储是 **FTS5（SQLite Full-Text Search） + Markdown 文件**。这比 RAG 方案轻量得多：

- **无 embedding 依赖**：即使在零 LLM 模式下，FTS5 搜索仍然工作
- **无额外基础设施**：不需要维护向量数据库服务，不需要调优 embedding 模型
- **天然可审计**：所有内容都是人类可读的 Markdown，grep / Obsidian 直接打开

这个选择在 260 Stars 的项目中是合理的——引入向量数据库会大幅增加运维复杂度，而这里的「交接文档」规模通常不大，FTS5 的分词搜索足够应对。

### 2. Per-Project 隔离

默认路径结构：
```
<wiki_root>/<workspace_id>/<project_id>/...
```

每个项目用 `basename($cwd)` 作为默认 project_id。只需在任意祖先目录放一个 `.ai-memory.toml` marker 文件即可覆盖 workspace 或 project 设置。这对多客户咨询公司或个人工作/个人项目分离很有用。

### 3. Karpathy 风格的 LLM 维基

这个命名来自 Andrej Karpathy 的一次分享[2]：他用纯文本笔记本来记录 AI 项目的决策上下文，这个笔记在每次项目开始时被加入到 system prompt。ai-memory 把这个模式自动化了——不再需要手动维护，而是每次 session 结束后自动生成。

---

## 与运营 Agent 范式的关联

ai-memory 与前文分析的 Cursor No-Repo Automations 形成了有趣的互补：

**No-Repo Automations 解决的是「无代码场景下 Agent 的值守能力」**——监控 Slack、Stripe、Databricks，在事件触发时生成摘要通知。**ai-memory 解决的是「Agent 换班时的上下文连续性」**——每次 session 边界自动压缩交接文档，确保下一个 Agent 能从「上次停下的地方」继续。

两者共同指向一个更大的趋势：**企业级 Agent 的长程可靠性不仅依赖模型能力，更依赖工程机制**——包括事件驱动编排（No-Repo Automations）和状态持久化（ai-memory）。Cursor 的 cloud agent lessons 中提到的 Temporal 迁移[3]解决的是「进程中断时的 durable execution」，ai-memory 解决的是「跨 agent 切换时的 context continuity」，两者是不同维度的持久化问题，但共同目标都是让 Agent 能跨更长时间尺度工作。

---

## 快速启动

```bash
# 1. 安装 CLI wrapper
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/akitaonrails/ai-memory/main/bin/ai-memory \
    -o ~/.local/bin/ai-memory && chmod +x ~/.local/bin/ai-memory

# 2. 启动 Docker 服务（默认 loopback 绑定，无认证）
docker run -d --name ai-memory \
    --restart unless-stopped \
    -p 127.0.0.1:49374:49374 \
    -v ai-memory-data:/data \
    -e AI_MEMORY_LLM_PROVIDER=anthropic \
    -e AI_MEMORY_LLM_MODEL=claude-sonnet-4-20250514 \
    -e AI_MEMORY_ANTHROPIC_API_KEY=sk-ant-... \
    ghcr.io/akitaonrails/ai-memory:latest

# 3. 在项目目录初始化
cd my-project && ai-memory bootstrap

# 4. 开始使用 Claude Code / Codex / OpenCode 等，SessionStart hook 自动 prepend 交接文档
```

---

## 引用来源

[1] akitaonrails/ai-memory — GitHub, MIT License, Rust  
https://github.com/akitaonrails/ai-memory

[2] Karpathy LLM Wiki Pattern — 引自 Andrej Karpathy 关于用纯文本笔记本记录 AI 项目上下文的分享

[3] What we've learned building cloud agents — Josh Ma, Cursor Engineering, 2026-05-21  
https://cursor.com/blog/cloud-agent-lessons