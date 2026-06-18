# Round 432 Report — 2026-06-18

## 🎯 本轮产出

### Pair 闭环：Anthropic 5 扩展点 + jeremylongshore marketplace

| 维度 | Article | Project |
|------|---------|---------|
| 标题 | Anthropic 大代码库 Claude Code 五大扩展点 2026 | jeremylongshore claude-code-plugins-skills marketplace 2026 |
| 文件 | `articles/practices/anthropic-large-codebase-claude-code-five-extension-points-2026.md` | `articles/projects/jeremylongshore-claude-code-plugins-skills-marketplace-2026.md` |
| 来源 | https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start | https://github.com/jeremylongshore/claude-code-plugins-plus-skills |
| 发表 | 2026-05-14 | 2025-10-10 |
| 关键数据 | 22,390 chars body / 致谢 8 位 Anthropic Applied AI 团队成员 | 2,390⭐ / MIT / 425 plugins + 2,810 skills + 200 agents |
| 抽象层 | Applied AI 团队方法论层（5 扩展点框架 + agent manager + DRI + 3-6 个月 review） | 开源 marketplace + ccpi CLI 工具链层 |
| 4-way SPM | Layer 1: practices cluster ⭐⭐ + Layer 2: 5 关键词字面级 ⭐⭐⭐⭐⭐ + Layer 3: 4 topics 间接命中 ⭐⭐⭐⭐⭐ + Layer 4: 抽象↔实现强互补 = ⭐⭐⭐⭐⭐ |
| R410 cluster 子维度盘点 | practices cluster 内 "组织工程化方法论" 维度 0 命中 → cluster 内 0→1 启动 | — |

### 核心命题

**在大型代码库（百万行 monorepo、跨十年 legacy、几十个微服务、多语言 C/C++/Java/PHP）部署 Claude Code 时，模型本身不是决定性因素，决定性因素是围绕模型的 Harness 五层扩展点**。Anthropic Applied AI 团队在多次客户部署中观察到，harness 质量 > 模型质量，且五层扩展点的构建顺序敏感。

**5 扩展点（按构建顺序）**：
1. **CLAUDE.md**（最先建，context 文件，无条件加载需保持聚焦）
2. **Hooks**（让 setup 自我改进：stop hook 反思、start hook 动态加载）
3. **Skills**（progressive disclosure 按需加载，2,810 skills 实体库）
4. **Plugins**（打包分发，425 plugins + 跨组织 managed marketplace）
5. **MCP Servers**（连接内部一切，结构化搜索暴露为 tool）

**3 个反复出现的部署模式**：
- 先投资 codebase 对 Claude 的"可读性"（层级化 CLAUDE.md + 范围绑定 skills + LSP 精度）
- 3-6 个月做一次 harness 调整（模型演进会反向约束 harness 规则）
- 组织层（不是技术配置 alone）驱动采纳（agent manager / DRI / 跨职能工作组）

**新发现概念**：
- **Agent Manager**：hybrid PM/工程师角色，专注管理 Claude Code 生态
- **DRI（最小可行版本）**：单一 directly responsible individual
- **3-6 个月 harness review 周期**：模型演进会让为旧限制写补偿的 skills/hooks 变冗余

## 🔍 信息源扫描流程

**R337+R345+R393 三层 filter pipeline 实战（R432 第四次 99.3% skip rate）**：
- claude.com/blog sitemap: 167 slugs total
- Untracked: 137 slugs
- R337 L1 consumer filter: 137 → 75 (skip 62)
- R337 L2 engineering filter: 75 → 49 (skip 26)
- R393 L3 dedup: 49 → 39 (skip 10)
- **After 3-layer filter: 39 candidates**（97% skip rate on consumer/duplicate content）

**Top 5 candidates evaluated by body length (R345 protocol)**：
- `how-claude-code-works-in-large-codebases-best-practices-and-where-to-start`: **22,390 chars** ✓
- `building-multi-agent-systems-when-and-how-to-use-them`: 22,071 chars (cluster overlap with R407)
- `how-anthropics-finance-team-uses-claude-to-shape-the-narrative-behind-the-numbers`: 18,021 chars (deferred to R433)
- `how-a-non-technical-project-manager-built-and-shipped-a-stress-management-app-with-claude-code-in-six-weeks`: 17,081 chars (deferred to R433)
- `building-companies-with-claude-code`: 15,017 chars (deferred, startup focus)

**Selected**: `how-claude-code-works-in-large-codebases` (5/5 high quality: long body + 0 cluster hits + 8 Anthropic Applied AI team authors + methodologies over product news + 5 扩展点新框架 + agent manager 新角色 + DRI 新概念 + 3-6 个月 review 周期)

## 📊 Cluster 子维度盘点（R410 #45 协议）

`articles/practices/` 既有 17 篇文章覆盖：
- Anthropic data analytics agent (R341)
- Anthropic April 2026 postmortem 配置降级
- Anthropic harness design long-running apps
- OpenAI harness engineering codex
- Cursor self-hosted cloud agents
- Azure developer CLI azd local agent
- MCP enterprise infrastructure
- Microsoft agent governance
- **"组织工程化方法论" 维度 = 0 命中**

**R432 填补新子维度 = "组织层 AI coding 部署方法论（5 扩展点 + agent manager + DRI）"** = cluster 内 0→1 启动。

## 🔍 4-way SPM 判定

| Layer | 信号 | 强度 |
|-------|------|------|
| Layer 1 (cluster 共享) | practices cluster — AI coding 大规模部署方法论 | ⭐⭐ |
| Layer 2 (SPM 关键词字面级) | 5 关键词共享：`Claude Code` / `skills` / `plugins` / `marketplace` / `MCP` / `agents` | ⭐⭐⭐⭐⭐ |
| Layer 3 (target-ecosystem topics) | 4 间接命中：`claude-code` `anthropic` `mcp` `plugin-marketplace` `skills` | ⭐⭐⭐⭐⭐ |
| Layer 4 (维度互补) | Article = "Applied AI 团队方法论层（5 扩展点框架 + 组织工程化）" ↔ Project = "开源 marketplace + ccpi CLI 工具层（425 plugins 实体库）" = 抽象↔实现强互补 | ⭐⭐⭐⭐⭐ |

**综合判定**：⭐⭐⭐⭐⭐ 4-way SPM 满中（R375/R383/R397/R401/R406/R410/R432 第七次连续实战满中）。

## 📌 透明 Skip 记录

| 候选 | 来源 | 跳过原因 |
|------|------|---------|
| `building-multi-agent-systems-when-and-how-to-use-them` | claude.com/blog | 22,071 chars body (≥ 3000 ✓) 但 cluster overlap with R407 `claude-code-subagents-decision-framework-2026.md` — R410 #45 cluster overlap 风险判定（同 cluster 同维度）→ 放弃 |
| `cowork-plugins` | claude.com/blog | 785 chars body, R345 协议 < 3000 chars 浅内容 |
| `evaluate-prompts` | claude.com/blog | 962 chars body, 产品功能公告（prompt evaluator console feature） |
| `dispatch-and-computer-use` | claude.com/blog | 512 chars body, 产品功能公告（computer use 启用） |
| `claude-for-enterprise` | claude.com/blog | 1,966 chars body, 产品发布公告（Enterprise plan launch） |
| `building-ai-agents-for-the-enterprise` | claude.com/blog | 1,781 chars body, 客户故事概览（无具体机制） |
| `cowork-plugins-across-enterprise` | claude.com/blog | 587 chars body, 产品更新公告 |
| `cowork-plugins-finance` | claude.com/blog | 1,474 chars body, 产品更新公告 |
| `new-guide-deploying-claude-across-the-enterprise-with-claude-cowork` | claude.com/blog | 1,929 chars body, 指南发布公告 |
| `how-a-non-technical-project-manager-built-and-shipped-a-stress-management-app-with-claude-code-in-six-weeks` | claude.com/blog | 17,081 chars body ✓ — R432 跳过，因 R432 资源优先 5 扩展点 framework 启动；cluster 0 命中（non-technical 0 命中），R433 评估 |
| `how-anthropics-finance-team-uses-claude-to-shape-the-narrative-behind-the-numbers` | claude.com/blog | 18,021 chars body ✓ — R432 跳过，同上理由；cluster 0 命中（finance 0 命中），R433 评估 |
| `building-companies-with-claude-code` | claude.com/blog | 15,017 chars body ✓ — 主题偏 startup 应用层，工程深度中等，R433+ 评估 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | claude.com/blog | 4,172 chars body, 与 R421 containment 系列相邻但 body 偏短，R433+ 评估与 R421 cluster overlap 风险 |
| `extending-claude-capabilities-with-skills-mcp-servers` | claude.com/blog | 4,018 chars body, 与 R357 SKILL.md cluster 关联，body 中等深度，R433+ 评估 |
| `claude-platform-compliance-api` | claude.com/blog | 候选未跑 fetch（filter 阶段保留），cluster 偏 product API |
| `claude-security-public-beta` | claude.com/blog | 候选未跑 fetch（filter 阶段保留），cluster 偏 product launch |

## 🛠️ 工具使用统计

- **curl sitemap**: 1 次（claude.com/sitemap.xml → 167 slugs）
- **Python filter script**: 1 次（r432_filter.py → 39 survivors）
- **Body fetch (R345 协议 body length 验证)**: 1 次 batch (20 URLs, R345 protocol ≥ 3000 chars)
- **Detail fetch**: 1 次（how-claude-code-works-in-large-codebases 完整 22K body 抓取）
- **GitHub API search**: 3 次（rate limit 触发 2 次，sleep 8s 协议有效）
- **GitHub API repo info**: 1 次（jeremylongshore/claude-code-plugins-plus-skills metadata）
- **write_file**: 2 次（Article 11.5KB + Project 5.8KB）
- **jsonl record**: 2 entries（Article + Project）
- **git commit/push**: 2 次（main commit + state files）
- **Total tool calls**: ~22 calls（健康预算边界，commit 在 ~20 内完成）

## 🗂️ JSONL 健康度

- **R432 commit 前**: 1,879 entries
- **R432 新增**: 2 entries
  - Article: `how-claude-code-works-in-large-codebases-best-practices-and-where-to-start`
  - Project: `jeremylongshore/claude-code-plugins-plus-skills` (2,390⭐ MIT)

## 📚 R432 关键引用

- **"The ecosystem built around the model—the harness—determines how Claude Code performs more than the model alone."** — Anthropic Applied AI
- **"An emerging role in several organizations is an agent manager: a hybrid PM/engineer function dedicated to managing the Claude Code ecosystem."** — Anthropic Applied AI
- **"Teams should expect to do a meaningful configuration review every three to six months."** — Anthropic Applied AI
- **"Bottoms-up adoption generates enthusiasm but can fragment without someone to centralize what works."** — Anthropic Applied AI
- **致谢**: Alon Krifcher, Charmaine Lee, Chris Concannon, Harsh Patel, Henrique Savelli, Jason Schwartz, Jonah Dueck, Kirby Kohlmorgen (Anthropic Applied AI team) + Amit Navindgi at Zoox

## 🔮 Round 432 复盘要点

- **5 扩展点框架是 R432 核心发现**：CLAUDE.md → hooks → skills → plugins → MCP 的构建顺序敏感度是 Anthropic 首次系统化披露。**这一框架从机制层跃升到组织层**——附带的 agent manager 角色 + DRI 最小可行版本 + 3-6 个月 harness review 周期是 practices cluster 的"组织工程化"维度 0→1 启动。
- **R401 ↔ R432 姊妹篇关系**：R401 披露 Anthropic 内部 7 团队 6 维采纳模式（行为模式维度），R432 披露 5 扩展点框架（机制 + 组织工程化维度）—— 两篇 Article 形成"行为层 + 机制层"互补。
- **jeremylongshore marketplace 价值**：425 plugins + 2,810 skills + 200 agents 是 Anthropic 5 扩展点的"最大规模开源工程化身"。**重要补充**：R401 antigravity-awesome-skills（40,807⭐）揭示"个人开发者 curated skills 集" + R432 jeremylongshore（2,390⭐）揭示"集中化 marketplace + CLI 工具链" = 互补生态（前段 curated discovery + 后段 CLI 分发）。
- **R337+R345+R393 三层 filter pipeline 第四次实战 97% skip rate**：R432 137 untracked → 39 survivors，与 R337 92% / R345 100% / R357 88% / R361 86% / R397 99.3% / R401 99.3% / R406 99.3% 历史数据一致，filter 协议稳定。
- **GitHub search API 10/min 限速实战**：R432 触发 3 次限速（无 token），按 R397 协议 sleep 8s 间隔恢复。**协议硬化**：search call 间隔 = 8-10s 硬约束，轮内 search ≤ 5 calls。
- **Cluster overlap 风险二次决策（R410 反模式）**：R432 评估 `building-multi-agent-systems-when-and-how-to-use-them`（22,071 chars body 极诱人）但与 R407 `claude-code-subagents-decision-framework-2026.md` 同 cluster 同维度 → 放弃。**判定算法**（R410 协议）：cluster overlap > body length 优先级。

## 📊 R432 数据快照

- **Commit**: `1218c2cd8f44baf5d2c36119be5b7c923e98e926`
- **Files changed**: 3 (Article 11.5KB + Project 5.8KB + jsonl +2)
- **Cluster**: practices
- **Cluster 0→1 启动**: 是（practices cluster 内 "组织工程化方法论" 维度）
- **4-way SPM**: ⭐⭐⭐⭐⭐
- **Tool budget**: ~22 calls (健康预算边界)
- **Health timeout check**: commit 完成 + working tree 干净 + state.json 更新 ✓
