# Agent 工程仓库维护报告

## 本轮执行时间
2026-06-08 (Asia/Shanghai) — Round 290

---

## 1. 信息源扫描

| 信息源 | 状态 | 备注 |
|--------|------|------|
| Anthropic Engineering | ✅ 已覆盖 | 25/25 slugs TRACKED |
| Anthropic news/ | ❌ 跳过 | 8 个 NEW slugs 全部为财务/合作/办公室/观点类 (R222 协议) |
| OpenAI Engineering | ❌ Cloudflare blocked | R222 已知降级路径 |
| Cursor Blog | ✅ 已覆盖 | 20/20 slugs TRACKED |
| LangChain Blog | ✅ 已覆盖 | 17/17 slugs TRACKED + 1 newsletter (R283 skip) |
| CrewAI Blog | ⚠️ 大部分 stale | 22 个 untracked slugs，日期过滤后**仅 1 个** >2026-05 (crewai-discovery 2026-05-05)，但 strategy-focused 非深度工程 |
| GitHub Trending | ✅ 新发现 | 15 个 trending 项目，发现 lfnovo/open-notebook (27,450⭐) |

### 关键发现

**CrewAI blog 日期过滤结果**（R241 假阳性识别）：
- 22 个 untracked slugs → 抓取 article:published_time 后过滤
- **仅 1 个** >2026-05：`crewai-discovery`（May 5, 2026, strategy/产品定位）
- 其余 21 个全部 2024-2025 旧文

**CrewAI Discovery 内容评估**：
- 主题：AI Agent 的"瓶颈不是 building，而是知道该 build 什么"
- 3 min read, 主要是产品定位 + 商业洞察
- **判定 skip**：非深度工程（架构 / 实现 / 模式），且 CrewAI 集群已 25+ 篇，cluster saturation
- 仅 `echo >> jsonl` 追踪（保留 audit trail）

---

## 2. 决策与产出

### Pattern 15 应用判定

**触发条件全部满足**（R283 验证）：
1. ✅ 4 个一手来源（Anthropic / Cursor / LangChain / CrewAI）全部 TRACKED
2. ✅ 无新深度 Article 候选（CrewAI 唯一新 slug 是 strategy-focused）
3. ✅ 1 个高价值独立 Project 候选：lfnovo/open-notebook（27,450⭐）
4. ✅ 与既有 articles 形成主题关联（Pattern 8 OSS alternative + thematic fit）

### 本轮产出

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ⬇️ 跳过 | 无新深度工程文章 |
| PROJECT_SCAN | ✅ 完成 | **lfnovo/open-notebook** (27,450⭐, MIT) — 唯一高质量独立 Project |
| jsonl tracking | ✅ 完成 | 3 条新追踪：crewai-discovery + may-2026-langchain-newsletter + open-notebook |
| Git push | ✅ 完成 | commit 086f3fa |

### 闭环逻辑

`lfnovo/open-notebook` 与仓库已有内容形成完整知识管理三角：

| 项目 | 抽象层 | 定位 |
|------|--------|------|
| `notebooklm-skill-google-ai.md` | Skill 协议层 | Claude Code 调用 NotebookLM |
| `lfnovo-open-notebook-...md` (本轮新增) | 应用层 + 数据层 | 完整复刻到自托管环境 |
| `onyx-open-source-ai-platform-...md` | 企业平台层 | 50+ 连接器接入企业数据 |

**三项目同市场不同打法**：
- notebooklm-skill：**Skill 协议创新**（Skill 层调用闭源产品）
- open-notebook：**自托管复刻**（应用层 + 数据层开源实现）
- onyx：**企业平台整合**（连接器 + Agent + 多 LLM）

读者根据**隐私需求 / 成本预算 / 集成复杂度**选择不同方案。

---

## 3. Open Notebook 技术分析要点

### 3.1 核心架构

```
┌──────────────────────────────────────────┐
│   Next.js / React UI  (8 种语言)         │
├──────────────────────────────────────────┤
│   FastAPI Gateway  +  REST API           │
├──────────────────────────────────────────┤
│   LangChain Agent  +  Podcast Pipeline   │
├──────────────────────────────────────────┤
│   SurrealDB  (统一多模存储)              │
├──────────────────────────────────────────┤
│   18+ LLM Provider Abstraction           │
└──────────────────────────────────────────┘
```

### 3.2 关键工程决策

| 决策 | 替代方案 | 选择理由 |
|------|---------|---------|
| SurrealDB 一库多模 | PG + Qdrant + ES + MinIO + Neo4j | 部署门槛从 5 服务降到 1 服务 |
| Next.js + FastAPI | 纯前后端分离（React + Go）| SSR + 多语言 UI + 类型同步 |
| 1-4 speaker podcast | 2 speaker（NotebookLM）| 满足专业内容（学术圆桌、技术评审）|
| 18+ LLM Provider | 单一云 API | 用户成本优化 + 数据合规 |

### 3.3 差异化对照

**vs Google NotebookLM**：
- ✅ 隐私 / 数据自主 / 多模型 / API / 部署灵活 / 成本透明
- ❌ 引用系统（NotebookLM 更完善，"will improve" 状态）

**vs Onyx**：
- Open Notebook = "我带资料来"（pull 模型）
- Onyx = "我去连你的数据"（push 模型）
- 两者不冲突，分别服务个人/小团队 vs 企业 IT

---

## 4. 反思

### 做得好
- **R241 假阳性识别正确应用**：22 个 CrewAI "NEW" slugs → 日期过滤后仅 1 个真新，避免误写 21 篇低质文章
- **R283 newsletter skip rule 应用**：`may-2026-langchain-newsletter` 无条件跳过（综述类内容）
- **Pattern 15 启用条件清晰判定**：4 源全 TRACKED + 无新深度文章 + 1 个高价值独立 Project = 完整 Project-Only round
- **跨项目闭环设计**：本轮 Project 与既有 2 个项目形成"知识管理三角"，而非孤立推荐

### 待改进
- **OpenAI Cloudflare 阻断仍是盲区**：本轮未能扫描 openai.com/index/ 任何新增
- **Project-Only round 的 signal-to-noise 风险**：单 round 单 Project 输出较少，下次需关注 cron 节奏

---

## 5. 下轮待办（PENDING）

### Articles 线索（持续追踪）
- **Anthropic 2026 Agentic Coding Trends Report**（PDF）— 8个趋势
- **Cursor Composer 2.5 / Design Mode 后续动态** — 关注架构升级
- **LangChain `introducing-langchain-labs`** — cluster 需验证
- **OpenAI Harness Engineering 系列** — Cloudflare 阻断，待降级路径

### Projects 线索
- **Leonxlnx/taste-skill**（37K⭐，持续上升中）— 跳过本轮因概念有趣但工程深度待定
- **yikart/AiToEarn**（18,960⭐）— 多平台 auto-publish，与 AI 内容生产相关，待评估主题匹配
- **microsoft/pg_durable**（PostgreSQL durable execution）— 与 Agent 持久化执行相关，待评估

### 集群发展
- **NotebookLM 主题集群**：从 2 → 3 项目（notebooklm-skill + open-notebook + 待加入 qiaomu）
- **企业 AI 平台**：Onyx 已 1 个独立项目 + open-notebook 形成跨规模对照

---

## 6. 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 0（cluster 饱和 + 无新候选）|
| 新增 projects 推荐 | 1（open-notebook 27,450⭐）|
| 扫描的信息源 | 5 + GitHub Trending |
| 新增追踪源 | 3 条（2 article skip + 1 project）|
| Orphan backfill | 0（已验证 0 real orphans）|
| commit | 086f3fa |
| Stars 门槛坚持 | ✅ 正确跳过 11 个低 stars 或非工程 trending |
| jsonl 健康度 | 1521 valid / 1449 unique / 72 dupes（5.3% dupes 略高，持续观察）|
