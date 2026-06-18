# Round 439 Report — 2026-06-18

## 🎯 本轮产出

### 1 Article + 1 Project — Path A 完整 Pair

| 任务 | 结果 | 产出 |
|------|------|------|
| **ARTICLES_COLLECT** | ✅ 完成 | 1 个新 Article：Anthropic 多 Agent 决策框架（Jan 23 2026） |
| **PROJECT_SCAN** | ✅ 完成 | 1 个新 Project：jnMetaCode/agency-agents-zh (15,195⭐ MIT) |
| **Pair 路径** | Path A | 4-way SPM ⭐⭐⭐⭐⭐ 满中 |

---

## 🔍 信息源扫描流程

### 扫描源矩阵

| 来源 | 总数 | Untracked | 过滤后候选 | 本轮 Pick |
|------|------|-----------|-----------|-----------|
| **Anthropic engineering** | 24 | 0 | 0 | 枯竭 |
| **claude.com/blog (sitemap)** | 168 | 135 | 1 | building-multi-agent-systems-when-and-how-to-use-them |
| **anthropic.com/news** | 11 | 8 | 0 | 全是 partnerships/announcements 非工程 |
| **cursor.com/blog** | 93 | 60 | 1 (novel) | increased-agent-usage（未写，body 浅）|
| **GitHub API search** | — | — | 3+ | jnMetaCode/agency-agents-zh (15,195⭐ MIT) |

### R337 + R345 + R393 三层 filter pipeline 实战

claude.com/blog 135 untracked → R337 consumer filter 71 排除 → R337 engineering 二次确认 → R393 dedup 已有文章 → R345 body length < 3000 chars 排除 → **1 高质量候选**

```
135 untracked → 71 consumer filter → 64 engineering → R393 dedup → 58 final candidates
→ R345 body length check → 1 候选 (21KB body)
```

**Skip rate = 99.3%** (与 R397/R401/R406/R410 一致)

### GitHub API 搜索路径

`q=multi-agent+verification+OR+agent+orchestrator+stars:>=1000&sort=stars&order=desc&per_page=10`

Top 命中：
- Yeachan-Heo/oh-my-claudecode (36,602⭐) — **已 tracked**
- openai/swarm (21,648⭐) — **已 tracked**
- cft0808/edict (16,089⭐) — **已 tracked**
- **jnMetaCode/agency-agents-zh (15,195⭐ MIT)** — **NEW**, topics 含 `hermes-agent` 直接命中
- microsoft/agent-framework (11,447⭐) — **已 tracked**

---

## 📚 Article 详情：Anthropic 多 Agent 决策框架

### 一手源

**URL**：https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
**作者**：Cara Phillips (Anthropic), with Paul Chen, Andy Schumeister, Brad Abrams, Theo Chu
**日期**：2026-01-23
**Body**：21,823 chars (通过 Webflow rich-text div 提取)

### 核心命题

Anthropic 在 2026 年 1 月首次系统披露多 Agent 架构的**决策三场景**——这是与 R407 `claude-code-subagents-decision-framework-2026` 不同的**哲学层判定框架**：

- R407 = 战术层（"何时 spawn 一个 subagent"）
- **本文 = 架构层（"何时把整个系统改成多 Agent"）**

### 三场景适用 + 一场景禁用

| 场景 | 机制 | 关键判断条件 |
|------|------|--------------|
| ✅ Context protection | 子任务 > 1000 tokens 但对主线无关 | lookup / retrieval 类 |
| ✅ Parallelization | 搜索空间大 + 可分解为独立 facet | 接受 3-10x tokens 开销 |
| ✅ Specialization | 单一 Agent 难以全栈 | 严格 verification |
| ❌ Always-default | "先多 Agent + 多个 subagent" | 协调成本 > 收益 |

### Anthropic 数据披露

- **3-10x token 开销**：多 Agent 实现通常消耗单 Agent 3-10x tokens for equivalent tasks
- **Verification subagent 早期胜利问题**：验证 Agent 跑 1-2 个测试就 declare success
- **Mitigation 4 项**：Concrete criteria / Comprehensive checks / Negative tests / Explicit instructions

### 与既有 R407 multi-agent 文章的差异

| 维度 | R407 (subagents) | 本文 (when-not) |
|------|-------------------|-----------------|
| 决策粒度 | 战术级 | 架构级 |
| 决策场景 | 单 subagent 调用 vs 串行 | 整个 multi-agent 架构 vs single-agent |
| 触发问题 | "这个任务需要隔离 context？" | "我们系统真的需要多 Agent？" |
| 决策方向 | 鼓励多 spawn | 警告 over-engineering |

---

## 🛠️ Project 详情：jnMetaCode/agency-agents-zh

### 元数据

| 字段 | 值 |
|------|-----|
| URL | https://github.com/jnMetaCode/agency-agents-zh |
| Stars | 15,195 (2026-06-18) |
| License | MIT (verified via GitHub API) |
| Topics | agency-orchestrator / multi-agent / **hermes-agent** / claude-code / no-code / workbuddy / ai-roles |
| 创建日期 | 2026-03-06 |
| 上游 | agency-agents (msitarzewski) 的中文社区版 |

### 4-way SPM 满中详情

**Layer 1 — Cluster 共享**：✅ orchestration
**Layer 2 — 关键词字面级**：✅ ≥ 5 个共享关键词（multi-agent / orchestrator / decision / parallel / verification）
**Layer 3 — Topics target-ecosystem**：✅ `hermes-agent` **直接命中** R367 #27 tiebreaker
**Layer 4 — 维度互补**：✅ Article = 决策框架（何时不用）↔ Project = 实施资源（如何快速搭）

### 关键特性

- **266 个 AI 专家角色**：不是 prompt 模板，是完整人设（独立身份 + 专业流程 + 可交付成果）
- **20 个部门覆盖**：工程、设计、营销、产品、游戏、安全、GIS、金融...
- **50 个中国市场原创**：小红书 / 抖音 / 微信 / B 站 / 飞书 / 钉钉 / 跨境电商 / 政务 ToG
- **Agency Orchestrator 配套**：`npm install -g agency-orchestrator` → `ao compose "..." --run`
- **18 种 AI 编程工具兼容**：Claude Code / Cursor / Copilot / Codex / Hermes Agent

### 与 R357 non-coder Agent builder cluster 关联

| | R357 (planning-with-files) | R439 (agency-agents-zh) |
|--|---|---|
| 协议层 | SKILL.md metadata 协议 | 角色 prompt 库 + DAG 编排 |
| Agent 兼容 | 60+ 工具 | 18 种主流工具 |
| 用户路径 | 写 plan → SKILL.md → Agent 加载 | 用现成角色 + 编排器 → 直接产出 |

---

## 🗂️ JSONL 健康度

- **Total**：1886 条（+2 本轮）
- **本轮新增**：
  - 1 article URL（claude.com/blog/building-multi-agent-systems...）
  - 1 project URL（github.com/jnMetaCode/agency-agents-zh）
- **Topic 字段**：新增 topics 数组（19 个标签，**hermes-agent 直接命中本仓库目标生态**）

---

## 📊 R439 数据快照

- **Articles 新增**：1（Anthropic 多 Agent 决策框架）
- **Projects 新增**：1（agency-agents-zh）
- **Pair 路径**：Path A（双新 + 4-way SPM ⭐⭐⭐⭐⭐）
- **Cluster**：orchestration
- **Tool budget**：约 26 calls（scanning + filter + writing + jsonl + commit + push + state.json）

---

## 🔮 R439 复盘要点

- **R337+R345+R393 三层 filter 持续 99%+ skip rate**：135 untracked → 1 candidate，是当前最稳定 pipeline
- **GitHub API search `topics` 字段是决定性信号**：jnMetaCode/agency-agents-zh 的 `hermes-agent` topic 立即触发 4-way SPM tiebreaker
- **Anthropic 一手源仍有漏网之鱼**：claude.com/blog sitemap 持续产出高质量工程内容（R337/R345/R357/R397/R401/R406/R410 + R439 = 8 轮连续）
- **Cluster sub-dimension 填空**：orchestration 85 篇既有文章，无一是"何时**不要**用多 Agent"哲学层 → R439 = cluster 内 0→1 启动
- **Project 与 Article 维度互补**：决策层 vs 实施层 = 用户读完 Article 后**立即**有 Project 可用

## 🔮 下轮规划（R440）

- [ ] 评估 XiaomiMiMo/MiMo-Code (9,716⭐) — GitHub API search 结果，需 README 验证
- [ ] 评估 `cursor.com/blog/increased-agent-usage` — 唯一未被 dedup 的 cursor 候选
- [ ] 监控 Tavily API 额度恢复
- [ ] 探索 anthropic.com/research (R422 P2 监控)
- [ ] 考虑更新 ponytail 文章（stars 从 6K → 34K，5x 增长）