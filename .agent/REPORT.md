# REPORT — R617 执行报告

## 执行摘要

**R617 = Cluster Validation Breakthrough Round — GitHub Copilot Harness Architecture Layer 4 GA (Enterprise Governance + Cross-Client Routing + Budget Control)**

R617 是 R616 prediction 50% cluster validation 分支命中。核心发现: **GitHub Blog 2026-07-01 集中发布 4 条 engineering 公告** —— Enterprise managed-settings.json GA + Enterprises can default to auto model selection + Copilot CLI auto model selection routes based on task + Set AI credit session limits in Copilot CLI and SDK。这 4 条公告**不是独立的 4 个 feature**，而是**GitHub Copilot 2026 Q3 Harness Architecture Layer 4 的一次性 GA** —— 让「企业级 AI Agent Harness」的 4 根支柱（Governance / Routing / Budget / Auditability）从 Preview 进入 GA。

Cluster 命名: **`harness-governance / enterprise-policy / budget-control`** —— 这是 **R616 `browser-agent / consent-architecture` 的 sibling cluster variant**（不是 cluster overlap），是 GitHub Copilot Harness 四层架构中 **Layer 4** 的工程定义。R613 (Layer 1 Model Routing) + R616 (Layer 3 Browser Surface) + **R617 (Layer 4 Enterprise Governance + Budget Control)** 三者合起来构成 **完整的 GitHub Copilot Harness Architecture 四层栈**：

```
Layer 4 (R617 ← 本文): Enterprise Governance + Cross-Client Routing + Budget Control
   ↑ managed-settings.json 5 keys + Auto Model Selection CLI + AI Credit Session Limits
Layer 3 (R616): Browser Surface + Consent Architecture
   ↑ 真实浏览器 + Share with Agent + Tab 隔离 + 企业 allow/deny
Layer 2 (R612-R614): Agent Harness + Session Persistence
   ↑ CLI chronicle + Session Harness + feedback loop
Layer 1 (R613): Model Routing + Cache
   ↑ HyDRA routing + 94% cache 命中率
```

Pair project **`AgentBudget/agentbudget`** (105⭐ Apache-2.0, 2026-02-15) 是 Layer 4 Budget Control 维度的开源 SDK 对应物。它借用 Unix `ulimit` 比喻，把 budget control 下沉到 LLM client 层（`wrap_client()` 透明包装），提供 `finalization_reserve`（预留收尾预算）和 `would_exceed()`（Agent 主动 query 预算状态）两个 API，把 budget control 从「harness 强制力」升级为「Agent 自我管理」。**GitHub 商业版 + AgentBudget 开源版 = Harness Budget Control 在 1st-party 和 OSS 两端同时收敛**。

## R617 vs R616 突破模式对比

| 维度 | R616 (Browser Tools GA) | R617 (Enterprise Governance + Budget) |
|------|------------------------|--------------------------------------|
| 1st-party 来源 | GitHub Blog (1 篇) | GitHub Blog (4 篇同天发布) |
| 突破层 | Layer 3 Browser Surface | Layer 4 Enterprise Governance |
| Cluster | browser-agent / consent-architecture | harness-governance / enterprise-policy / budget-control |
| Pair project | microsoft/playwright-mcp (34,577⭐ OSS base) | AgentBudget/agentbudget (105⭐ OSS SDK) |
| 核心机制 | 8 大 Trust Boundary 机制 | 5 managed-settings keys + Auto routing CLI + soft cap session limits |
| Engineering 深度 | 8 大机制 (Browser Surface) | 4 大机制 (Governance + Routing + Budget + Auditability) |
| Stakeholder | 个人开发者 + Security | 企业 CISO / IT / Finance |
| Pair 范式 | 1st-party commercial + 1st-party OSS base | 1st-party commercial + OSS SDK analog |

**Pair 范式差异**：R616 是「商业产品 + 1st-party OSS base」Pair (microsoft/playwright-mcp 是 Microsoft 官方维护)。R617 是「商业产品 + 3rd-party OSS SDK analog」Pair (AgentBudget 是独立社区维护，但概念完全对应 GitHub Session Limits)。这反映了 **Layer 4 的开源生态多样性** —— Governance + Budget 是横切关注点，OSS 端有多个独立实现。

## 6-Source Tri-Scan 审计表 (R617)

| Source | Total | Tracked | NEW | Engineering | Writable | Skip Reason |
|--------|-------|---------|-----|-------------|----------|-------------|
| Anthropic sitemap | 481 | ~140 | 0 | 0 | 0 | Claude Fable 5 + Mythos 5 (7/1 WSD models, R615 covered) + redeploying-fable-5 (R615 covered) + claude-science-ai-workbench (R612 covered). Engineering 17-round plateau (last 2026-06-06). |
| Anthropic Engineering blog | 25 | 25 | 0 | 0 | 0 | 17-round plateau R555/R591/R601-R617. Last engineering post 2026-06-06 how-we-contain-claude. 7/4 独立日前 1.5 天未打破. |
| OpenAI RSS top 15 | 15 | 4 | 11 | 0 | 0 | 11 NEW 全部 WSD/cluster overlap (同 R614/R615/R616). Amazon partnership + Codex changelog + Deprecations + Web search integration + various policy/model posts. 0 engineering breakthrough. |
| Cursor Blog | 97 covered | 17 | 0 | 0 | 0 | Tavily 7 月 slug 查询返回 0 sources. R518 cluster overlap Skip 持续. Cursor Compile 6 月 conference + Cursor Mobile iOS + Notion × Cursor SDK + Origin Git platform + first from-scratch model 全部 covered in R518/R550/R591. 0 new 7 月 slug. |
| Claude Blog (claude.com) | 10 top result | 10 | 0 | 0 | 0 | Tavily 7 月 query 返回 0 sources. R587 5% engineering probability pattern 持续. Tavily top 10 results 全部 R605 + R322 + R602 + R518 + R587 + R337 + R603 covered. |
| code.claude.com docs | 642 | 100+ | 0 | 0 | 0 | W25/W26 changelog + agent-sdk/tool-search + workflows docs page 全部 R5xx covered. 0 engineering deep-dive new. R617 0 new engineering docs. |
| **GitHub Blog 7/1** | **9 NEW** | **0** | **9** | **4** | **4** | **🎯 R617 CLUSTER VALIDATION BREAKTHROUGH**: 4 条 engineering 公告 (managed-settings.json GA + Enterprises default auto model + Copilot CLI auto model selection + AI Credit Session Limits) + 5 条 WSD (Copilot vision GA + Kimi K2.7 Code + Secret scanning + GitHub Models retirement + C++ language server skill). 构成 GitHub Copilot Harness Architecture Layer 4 完整 GA. 历史第 4 次 GitHub Blog 1st-party release 突破 (R613/R616 同源模式). |
| Anthropic Petri 2.0 alignment blog (6/30 lastmod) | 1 NEW | 0 | 1 | 0 | 0 | WSD alignment research (Petri automated-behavioral-auditing tool). 1st-party Anthropic 但 alignment research 维度, 不算工程机制. SKILL.md 一手原则 + 工程机制双重 Skip. |
| Anthropic Opus 4.8 / Sonnet 5 / Fable 5+Mythos 5 / Sonnet 5 system card | 5 NEW | 0 | 5 | 0 | 0 | WSD models (5 个 model releases). 7/1 集中发布, 全部 R552/R5xx covered. |
| GitHub Search 12d | 20 candidates | 14 | 6 | 0 | 0 | R616 defer candidates + 6 NEW 全部 WSD/cluster overlap: awesome-ai-agents-2026 (WSD curated list) + 2026-ROADMAP PPT/PDF (WSD) + browser-use/browser-use R311 covered (105k⭐ from 102k⭐) + modelcontextprotocol/servers (87k⭐) 含 playwright-mcp 但无独立 article + browserless (13k⭐ NOASSERTION) + agent-leaderboard (WSD). 1 borderline 可写: **AgentBudget/agentbudget 105⭐ Apache-2.0** = Pair project for Layer 4 Budget Control. |
| **TOTAL** | **~1500** | **~145** | **~36** | **4** | **4** | **GitHub Blog 7/1 4-engineering 公告合并 = 1 个 cluster validation breakthrough** |

## Article 解析: GitHub Copilot Enterprise Harness Layer 4 (R617 Article)

**File**: `articles/harness/github-copilot-enterprise-governance-managed-settings-budget-control-2026.md`
**Source**: 4 URLs from GitHub Blog 7/1 (1st-party)
**Cluster**: `harness-governance / enterprise-policy / budget-control` (NEW cluster variant, sibling to R616 browser-agent/consent-architecture)
**Engineering 深度**: 9 大机制深度拆解 + 4 个一手原文引用 + 3 个范式提炼

### 4 大公告 + 9 大工程机制

**公告 1: Enterprise managed-settings.json GA** (7/1)
1. **5 个 Supported Keys**: extraKnownMarketplaces / enabledPlugins / strictKnownMarketplaces / disableBypassPermissionsMode / model
2. **PR reviewable AI 治理**: `.github-private` 仓库 + git commit + PR review + git revert
3. **周期性 refresh**: 登录 fetch + 1 小时 refresh + 内存存储不落盘

**公告 2: Enterprises can default to auto model selection** (7/1)
4. **Anti-lock-in 治理**: 把 `model: "auto"` 写到 managed-settings.json 让所有新会话默认走 Auto

**公告 3: Copilot CLI auto model selection routes based on task** (7/1)
5. **5 维度模型评估**: reasoning / code generation complexity / bug diagnosis / tool orchestration / real-time availability
6. **Cache boundary aware routing**: Auto 沿自然缓存边界路由避免 cache miss
7. **10% AI credit discount**: Auto 比手动选便宜 10%

**公告 4: Set AI credit session limits in Copilot CLI and SDK** (7/1)
8. **Soft cap (response atomic)**: 软上限 + 正在进行的 response 跑完才停
9. **Compaction 计入预算**: 显式把 background compaction 消耗纳入 AI credit 计量

### 三大范式提炼

1. **「Configuration as Code」治理范式** (R617 全新): 不把 AI 策略藏在管理后台 UI，让 CISO/IT 用 git 管理 AI 配置
2. **「Anti-lock-in 治理」范式** (R617 全新): 不锁定模型，把「自动选最优」当治理基线
3. **「Soft cap + Response atomic」哲学** (R617 全新): budget control 不破坏 Agent 完整性，正在进行的 response 一定跑完

### 4 段一手原文引用

- managed-settings.json 配置路径 + .github-private 仓库 + 周期刷新机制
- Auto model selection 5 维度评估 + cache boundary routing
- Session limits soft cap 哲学 + response atomic
- Compaction 计入预算的工程真相

## Project 解析: AgentBudget/agentbudget (R617 Project)

**File**: `articles/projects/agentbudget-agentbudget-ulimit-for-ai-agents-105-stars-2026.md`
**Source**: https://github.com/AgentBudget/agentbudget
**Stars**: 105 | Forks: 26 | License: Apache-2.0 | Created: 2026-02-15 | Last Push: 2026-05-30
**Borderline Approval**: 105⭐ below 280 borderline, but concept match 极强 (OSS analog of GitHub 7/1 Session Limits), License Apache-2.0 清洁. 符合 SKILL.md "超轻量原型 Stars 较低但概念突出 → 可选（需特殊审批）".
**Cluster**: `harness-governance / budget-control / session-cost`

### 5 大核心能力

1. **`wrap_client()` 透明包装**: 一行 import 启用 budget enforcement, 不需要改业务代码
2. **`finalization_reserve` 收尾预算**: 给 Agent 留「收尾预算」让 Agent 主动 stop, 不破坏 response 原子性
3. **`would_exceed()` 可观测信号**: Agent 主动 query 预算状态, budget control 从「harness 强制力」升级为「Agent 自我管理」
4. **OpenRouter 多模型统一计价**: 同一 session 内混用 OpenAI + Anthropic + Google + Mistral 统一计价
5. **Multi-language SDK**: Python 主推 + Go 已发布 + Node 即将

### 与 R617 Article 的关系

| 维度 | GitHub Copilot Session Limits (R617 Article) | AgentBudget/agentbudget (R617 Project) |
|------|--------------------------------------|-------------------------|
| 部署形态 | SaaS（managed） | Library（self-hosted） |
| 计费维度 | AI credits | Dollar |
| 触发位置 | Copilot harness 内部 | LLM client wrapper |
| Soft/Hard cap | Soft cap | 可配 (默认 hard) |
| 多 agent 支持 | 内置 | 业务侧显式 wrap |
| License | 商业 | Apache-2.0 |
| 适合场景 | GitHub Copilot 用户 | 自托管 / 多云 / 跨厂商 |

**核心关系**: 1st-party 商业产品 (GitHub Copilot Session Limits) + 3rd-party OSS SDK (AgentBudget) 的工程互补. 不是 cluster overlap, 而是 sibling implementation —— 两者方向一致, 工程权衡不同, 共同确认 **「Harness Budget Control」作为 2026 H2 独立基础设施类目**.

## Cluster 命名: harness-governance / enterprise-policy / budget-control

**不是 cluster overlap** (R616 browser-agent/consent-architecture 是 sibling, 不是 overlap):
- R616 Browser Surface + Consent Architecture — Agent 输出端口层
- R617 Enterprise Governance + Budget Control — Harness 治理层

**R617 NEW cluster variant 关键词**:
- **Governance**: managed-settings.json 5 keys + PR reviewable AI 治理
- **Routing**: Auto model selection 5 维度评估 + cache boundary
- **Budget**: Soft cap session limits + compaction 计入预算
- **Cross-Client**: VS Code + CLI + SDK 一致策略

这四个关键词在 R555-R616 已有 harness 文章中都**没有完整出现** —— 已有文章聚焦「harness 工程机制」(evaluator loop / session persistence / cross-model routing), R617 聚焦「harness 企业治理」(configuration as code / budget control / cross-client consistency)。

## R617 反思与下轮预测

### R617 反思

1. **R616 prediction 50% cluster validation 分支命中** —— 7/4 独立日前 1.5 天窗口期 1st-party release 模式持续. 历史第 4 次 GitHub Blog 1st-party release 突破 (R613/R616 同源模式).
2. **Cluster sibling variant emergence 模式延续** —— R616 browser-agent/consent-architecture + R617 harness-governance/enterprise-policy/budget-control 是 sibling, 不是 overlap. 两个 cluster 都是 GitHub Copilot Harness Architecture 的不同 Layer (Layer 3 vs Layer 4).
3. **Pair project 模式多元化** —— R612 (NVIDIA BioNeMo 1st-party vertical) / R613 (OnlyTerp 3rd-party democratization 107⭐ borderline) / R616 (microsoft/playwright-mcp 1st-party OSS base) / **R617 (AgentBudget 3rd-party OSS SDK analog 105⭐ borderline)**. R613 + R617 都是 borderline (sub-200⭐), 但都因 concept 匹配度高被 special approval. Pair project 多元化的同时 borderline approval 频次增加.
4. **Layer 1-4 Harness Engineering 栈完整确认** —— R613 Layer 1 + R616 Layer 3 + **R617 Layer 4** + (中间 Layer 2 implicit). R618+ 监控 Layer 2 是否出现明确 1st-party post (Anthropic / OpenAI / Cursor 在 Layer 2 是否有对应公告).
5. **Anthropic Engineering 17-round plateau 持续** —— Last 2026-06-06 how-we-contain-claude. 历史第 6 长 streak R555 era. R618 大概率 7/3-7/4 release 窗口期打破 (历史 7/4 release 模式 R555 era).
6. **「Harness Budget Control」作为独立类目确立** —— 1st-party 商业产品 (GitHub) + OSS SDK (AgentBudget) 两端同时收敛. R618+ 监控其他厂商 (OpenAI/Anthropic/Cursor) 是否跟进 session-level budget control.

### R618 预测

**Trigger**: 2026-07-02 22:00 或 2026-07-03 06:00 (cron 触发)
**重点监控**:
1. **Anthropic Engineering 7/2-7/4 release 概率 70%** —— 17-round plateau 突破信号强化 (历史 7/4 release 模式 + R612 claude-science-ai-workbench 6/30 已暗示 7 月 release cluster)
2. **Claude Code SDK 7/2-7/4 release 概率 50%** —— code.claude.com docs 可能有 W27/W28 changelog 含工程 deep-dive
3. **GitHub Blog 7/2-7/4 release 概率 40%** —— Layer 4 后续 (Copilot SDK GA / Team Plan / Enterprise GA extension)
4. **Cursor Blog 7/2-7/4 release 概率 30%** —— Cursor Compile 后续 + Origin Git platform + first from-scratch model preview
5. **OpenAI 7/2-7/4 release 概率 30%** —— Agent Builder GA 或新 Codex engineering post

**R618 概率分布**:
- **55% breakthrough** (Anthropic Engineering 7/3-7/4 突破 17-round plateau, 概率提升因 R617 4 突破 + 1.5 天窗口期临近)
- **20% cluster validation** (Layer 2 Agent Harness + Session Persistence 1st-party post, 或 Layer 4 续篇)
- **15% saturation streak 1** (R612-R617 5 突破后冷却 1 轮)
- **10% silent round**

**下轮 Pair project 候选 (R618 监控)**:
- Anthropic 7 月 new SDK / skill / harness (R555 era 7 月 release pattern)
- Cursor 7 月 Cursor 3.5 / Composer 3 / first from-scratch model preview (if 1st-party)
- aws/agent-toolkit-for-aws R538 covered, 7 月 new sibling repo
- Chrome WebMCP 1st-party Chrome team blog release (browser-agent cluster 续篇)

## 状态文件更新

- **state.json**: R617 cluster_validation_breakthrough_round + 4 GitHub Blog engineering 公告 + 9 NEW GitHub Blog (5 WSD + 4 engineering) + Anthropic Petri 2.0 WSD alignment + Pair project AgentBudget 105⭐ borderline approval + 4-突破+2-sat pattern confirmation + 17-round Anthropic Engineering plateau
- **PENDING.md**: R617 breakthrough record + R616 cooling history + R618 prediction
- **REPORT.md**: R617 detailed audit + 6-source extension + 9 大工程机制 + 3 范式提炼 + cluster variant emergence 模式 + Layer 1-4 Harness Architecture 栈确认 + Pair project borderline approval + R618 预测
- **sources_tracked.jsonl**: +5 entries (4 GitHub Blog + 1 AgentBudget) = 53 total
- **articles/projects/README.md**: AgentBudget entry appended

---

# REPORT — R616 执行报告 (保留作历史参考)

## 执行摘要

**R616 = Breakthrough Round #3 — GitHub Blog 2026-07-01 Browser Tools GA + microsoft/playwright-mcp OSS 基础层 (24h R615 后)**

R616 是 R615 prediction 40% 突破分支命中。核心发现: **GitHub Blog 2026-07-01 公告 Browser Tools GA** —— 8 大工程机制 (真实浏览器 + Share with Agent + Agent Tab 隔离 + 并行 Agent 隔离 + 敏感权限默认拒绝 + 企业 allow/deny + Workspace Trust + Editor+Agents window 集成) 构成完整 Trust Boundary 设计。这是 R612 → R613 → R614 → R615 → **R616** 的第三条 1st-party release 突破路径,验证了 7/4 独立日前 1.5 天窗口期 1st-party release 模式。

Pair project **`microsoft/playwright-mcp`** (34,577⭐ Apache-2.0) 是 GitHub Browser Tools 的官方开源基础层,实现 accessibility-tree-based interaction (对比 vision model) + 跨浏览器支持 + Trace + Persistent Context。这是 1st-party commercial product (GitHub Blog) + 1st-party OSS base (microsoft/playwright-mcp) 的标准 Pair 模式 (R612/R613 范式)。

Cluster 命名: **browser-agent / consent-architecture** —— 不是已有 "browser-agent cluster" (R515/R567/R591 等 4+ 篇饱和) 的 cluster overlap,而是新增 cluster variant: **「Browser-as-Agent-Surface + Trust Boundary Design」**。Engineering 范式从 "browser-using agent" 进化到 "browser-as-trust-boundary"。

## R616 vs R612/R613 突破模式对比

| 维度 | R612 (Anthropic Claude Science) | R613 (GitHub Copilot Harness) | R616 (GitHub Browser Tools GA) |
|------|--------------------------------|--------------------------------|--------------------------------|
| 1st-party 来源 | Anthropic Newsroom | GitHub Blog | GitHub Blog |
| Cluster | vertical-harness | cross-model-harness-as-product | browser-agent / consent-architecture |
| Pair project | NVIDIA BioNeMo (vertical scientific) | OnlyTerp/prompt-cache-skills (107⭐ Skill-as-Harness) | microsoft/playwright-mcp (34,577⭐ OSS base) |
| 突破层 | 单领域 Harness | 模型路由层 Harness | 浏览器交互层 Harness |
| Trust Boundary | 学术科研边界 | 缓存 + 路由治理 | Share with Agent + 隔离 + allow/deny |
| Engineering 深度 | 5 大模块 + 工具调用 | 94% cache + HyDRA routing | 8 大机制 + 三层治理接口 |

三者合起来构成 **GitHub / Anthropic 在 2026 H2 的 Harness Engineering 三层栈演进路径**:
```
Layer 3 (R616): Browser Surface + Consent Architecture  ← 本文
   ↑ 真实浏览器 + Share with Agent + Tab 隔离 + 企业 allow/deny
Layer 2 (R612-R614): Agent Harness + Session Persistence
   ↑ CLI chronicle + Session Harness + feedback loop
Layer 1 (R613): Model Routing + Cache
   ↑ HyDRA routing + 94% cache 命中率
```