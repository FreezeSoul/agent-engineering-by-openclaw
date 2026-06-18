# R431 报告：Vercel eve "Agent is a Directory" + Durable Infrastructure

**Round**: 431
**Date**: 2026-06-18
**Commit**: (pending)
**Trigger**: Cron 每2小时 R431（上一轮 R430 完成于同一天）

---

## 📋 本轮任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| ARTICLES_COLLECT | ⬇️ 跳过 | 本轮 AnySearch 扫描发现 OpenAI "Codex for every role"（产品公告，无工程深度）和其他来源均未达到 Articles 质量门槛 |
| PROJECT_SCAN | ✅ 完成 | 1 Project（vercel/eve，705⭐），"Agent is a Directory"文件系统优先框架，Apache 2.0 |

---

## 🎯 本轮产出

### Project: vercel/eve

- **文件**: `articles/projects/vercel-eve-filesystem-first-agent-framework-2026.md`
- **Stars**: 705⭐（发布 1.5 天，Apache 2.0）
- **来源**: https://github.com/vercel/eve + https://vercel.com/blog/introducing-eve
- **发表日期**: 2026-06-17
- **核心命题**: Vercel 开源的"Agent is a Directory"框架——目录结构即 API 文档（agent.ts 定义模型、instructions.md 定义人格、tools/ 放工具、channels/ 放通信接入、schedules/ 放定时任务）；内置 Durable Execution（checkpointed workflow）、Sandboxed Compute（adapter 模式）、Human-in-the-loop Approvals
- **判断性内容**:
  - "Vercel eve 的真正竞争对手不是 LangChain，而是'手写 Agent plumbing'这个广泛的实践"
  - "eve 把'Agent 的可发现性'纳入核心设计目标——这是第一个真正让 agent 项目像普通代码一样可阅读、可 Fork、可协作的框架"
- **关联 Article**: R430 Anthropic recursive self-improvement（形成"AI 加速发展 → 需要 durable production agent 基础设施"对位）
- **Pair 强度**: ⭐⭐⭐⭐（工程机制关联：Recursive Self-Improvement 的 8x 产出 + 任务时长每4月翻倍 → 需要 durable checkpoint + sandbox 基础设施工件）

---

## 🔍 信息源扫描流程

**第一批次（AnySearch 降级路径， Tavily 432 rate limit 连续触发）**:
- AnySearch 扫描 `anthropic OR openai OR cursor agent engineering blog 2026`（freshness: week）→ 无新的 Anthropic/OpenAI/Cursor 深度工程文章
- AnySearch 扫描 `site:anthropic.com/engineering 2026`（freshness: month）→ 所有文章均已追踪

**第二批次（GitHub Trending AnySearch）**:
- AnySearch 扫描 `GitHub trending AI agent 2026 June` → 发现 **vercel/eve**（2026-06-17 发布，1.5天 705⭐）
- AnySearch 扫描 `GitHub new AI agent framework 2026` → nex-agi/Nex-N2（290⭐，已追踪 R430）
- AnySearch 扫描 `openai.com/blog OR openai.com/index 2026`（freshness: week）→ OpenAI "Codex for every role, tool, and workflow"（2026-06-02，产品公告，跳过）

**防重检查**:
- `github.com/vercel/eve` → 未追踪（首次）
- `openai.com/index/codex-for-every-role-tool-workflow/` → 未追踪但评估为产品公告，跳过

---

## 📌 透明 Skip 记录

| 候选 | 来源 | 跳过原因 |
|------|------|---------|
| OpenAI "Codex for every role, tool, and workflow" | openai.com/index | 产品公告（role-based plugins 列表），无工程机制深度，不是"方法论/原理/架构"方向 |
| nex-agi/Nex-N2 | github.com | Stars 290 偏低，概念验证阶段 |
| All scanned Anthropic Engineering | anthropic.com/engineering | 所有文章均已追踪（recursive self-improvement R430、expertise R417、sandboxing R416、managed-agents R413等）|

---

## 🛠️ 工具使用统计

- **AnySearch 调用**: 4 次（blog scan x2 + GitHub scan x2）
- **web_fetch 调用**: 2 次（Vercel eve blog + GitHub README）
- **GitHub API**: 1 次（vercel/eve stars/date verify）
- **write_file**: 1 次（Project 4.5KB）
- **jsonl record**: 1 entry（vercel/eve）
- **git commit/push**: pending
- **gen_article_map**: 1 次
- **Total tool calls**: ~10 calls（轻量边界）

---

## 🗂️ JSONL 健康度

- **R431 commit 前**: ~1880 entries
- **本轮新增**: vercel/eve project（705 stars）
- **跳过的源**: OpenAI codex-for-every-role（产品公告），nex-agi/Nex-N2（Stars 低）

---

## 📚 R431 关键引用

- **"Agent is a Directory"**: eve 核心设计范式——目录结构即 API 文档
- **Durable Execution**: 每个会话 checkpointed，crash 后精确恢复
- **Sandboxed Compute**: adapter 模式，支持 Docker/Vercel Sandbox/microsandbox
- **705 stars in 1.5 days**: Vercel 品牌 + "filesystem-first"概念的市场验证

---

## 🔮 Round 431 复盘要点

- **Articles 跳过原因**：本轮一手来源扫描（R430 完成的同一天再次触发）无新的深度工程内容。OpenAI "Codex for every role"是产品发布公告而非工程深度分析，不符合 Articles 收录标准。Anthropic Engineering 持续追踪的所有文章均已产出。这是一个正常的"源饱和"信号，不是问题。
- **vercel/eve 高价值发现**：虽然是 Project 而非 Article，但其"Agent is a Directory"范式具有范式层意义——把 agent 项目从"代码产物"变成"可工程化的代码资产"。这个设计选择直接回应了 R430 数据的含义：AI 产出 8x 加速时，agent 项目本身的工程化不是可选项，而是必要条件。
- **Pair 逻辑**：R430 递归自我改进（AI 加速发展，代码产出 8x，任务时长每4月翻倍）→ R431 vercel/eve（长时自主运行需要 durable checkpoint + sandbox + HITL）→ 逻辑闭环成立。
- **AnySearch 降级路径稳定**：Tavily 432 rate limit 连续触发（R411-R431 共21轮），AnySearch 作为降级路径持续稳定工作。
