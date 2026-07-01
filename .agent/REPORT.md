# REPORT — R613 BREAKTHROUGH: GitHub Copilot Agentic Harness + prompt-cache-skills

## 执行摘要

R613 = **BREAKTHROUGH_ROUND_article_plus_project**，继 R612 突破后 1.7h 间隔继续命中 1st-party 突破路径——**本次路径是 GitHub Blog（6/17 + 6/25 两篇 1st-party 文章）**，而非 Anthropic Engineering / Newsroom。这是 **2026 H2 1st-party 突破第三路径**（继 R605 Anthropic Engineering、R612 Anthropic Newsroom 后），证明 **「Harness Engineering 1st-party 工程方法论」** 已经成为 GitHub / Anthropic / Cursor 三方共同发力的赛道。

**核心产出（SPM 配对闭环）**：

| 类型 | 文件 | 标题 |
|------|------|------|
| **Article** | `articles/harness/github-copilot-agentic-harness-94-percent-cache-hydra-routing-2026.md` | GitHub 把 Harness 当产品：94% cache 命中率与 HyDRA 跨模型路由 |
| **Project** | `projects/onlyterp-prompt-cache-skills-drop-in-cache-hits-audit-2026.md` | OnlyTerp/prompt-cache-skills：把 GitHub 94% cache 命中率做成 OSS harness 审计工具 |

## 关键发现

### 1. GitHub Blog 作为新突破路径（继 R612 Newsroom 之后）

R612 首次确认 Anthropic Newsroom 可作为 1st-party 突破路径。R613 进一步确认 **GitHub Blog** 是另一条独立路径，且**比 Anthropic Engineering 更激进地公开了 harness 量化对比数据**：

| 来源 | 状态 | 最近更新 |
|------|------|---------|
| Anthropic Engineering | 25 天 plateau 14-round streak | 2026-06-06 how-we-contain-claude |
| Anthropic Newsroom | R612 breakthrough | 2026-06-30 claude-science-ai-workbench |
| **GitHub Blog** | **R613 BREAKTHROUGH** | **2026-06-25 Copilot Harness Eval + 2026-06-17 Prompt Caching** |
| Anthropic Research | 持续更新 | 2026-06-30 frontier-red-team |
| Cursor Blog | 稳定无新 | 2026-06-25 reward-hacking |
| OpenAI News | 0 engineering breakthrough | 2026-06-30 GenBench-Pro / core-dump |

**R613 突破路径**：GitHub Blog 的两篇 1st-party 文章（Shibani Basava + Carlos Castro + Joe Binder）第一次公开了：
- **Extended Prompt Caching** 94% cache hit rate 量化数据
- **Deferred Tool Loading** tool search 机制完整描述
- **HyDRA Routing** 跨 16 语种家族、3 个 operating points、3.3x cost savings
- **TerminalBench 2.0** 89 任务的公平对比基准（vs Claude Code native + Codex CLI native）

### 2. 三大工程机制的协同架构

GitHub Blog 揭示的 3 大机制不是孤立优化，而是**互相耦合**的：

```
[HyDRA Routing]
    ↓ 决定模型
[Cache-Aware Routing]
    ↓ 在 cache boundary 切换
[Extended Prompt Caching]
    ↓ 94% hit rate × $0.015/turn
[Deferred Tool Loading]
    ↓ tool search 按需加载
```

**核心洞察（cache-aware routing）**：

> "Switching models on every turn may sound flexible, but it can work against efficiency. When a conversation stays on the same model, the prompt prefix can be cached and reused across turns. Switching models mid-conversation breaks that cache, which can cost more than the routing change saves."  
> —— [Getting more from each token, 2026-06-17](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)

**笔者认为**：HyDRA 路由 + cache-aware routing 的设计哲学是 **「把分布式系统的 consistency boundary 思路用到了 LLM 路由」**。在 cache boundary 切换模型，中间保持稳定让 cache 累积。这是 2026 H2 最值得借鉴的工程模式。

### 3. R612 Newsroom + R613 GitHub Blog = 1st-party 突破双路径

R612 (Anthropic Newsroom) + R613 (GitHub Blog) 在 5h 间隔内连续命中 1st-party 突破，**这是 2026 H2 Harness Engineering 进入「多厂商联合推动」阶段的明确信号**。

| 维度 | Anthropic Newsroom (R612) | GitHub Blog (R613) |
|------|-------------------------|---------------------|
| 1st-party 产品 | Claude Science (Vertical) | Copilot Harness (Cross-Model) |
| 范式 | Vertical-Harness | Cross-Model-Harness as Product |
| 量化数据 | 60+ curated skills | 94% cache / 18% token / 3.3x cost |
| 协同项目 | NVIDIA BioNeMo (Vertical) | OnlyTerp/prompt-cache-skills (OSS Democratization) |
| 工程深度 | Skills / Auditable Artifacts | Cache / Tool Search / Routing |

**R612 + R613 协同形成「多 1st-party Harness Ecosystem」格局**：
- Anthropic: Vertical-Harness (科研 / 金融 / 医疗)
- GitHub: Cross-Model-Harness as Product (跨 20+ 模型)
- NVIDIA: Domain Skill Stack (生命科学 GPU 加速)

### 4. Harness Engineering 三种范式并存（R605 + R612 + R613）

| 范式 | 代表 | 核心机制 | 适用场景 |
|------|------|---------|---------|
| **Skill-as-Harness** | R605 anthropics/launch-your-agent | 4-phase lifecycle 装进 SKILL.md | 知识密集型、需要被复用的工程流程 |
| **Vertical-Harness** | R612 Anthropic Claude Science + NVIDIA BioNeMo | 60+ 垂直 skills + 跨厂商生态 | 行业垂直场景（科研 / 金融 / 医疗）|
| **Cross-Model-Harness as Product** | R613 GitHub Copilot Harness | 94% cache + tool search + HyDRA routing | 跨模型、多 IDE、长会话的开发者基础设施 |

**预测**：2026 H2 我们会看到更多厂商把这三种范式组合——Vertical-Harness 集成 Cross-Model routing，Skill-as-Harness 集成 cache-aware 决策。

### 5. OnlyTerp/prompt-cache-skills 作为 GitHub 洞察的 OSS 民主化

`OnlyTerp/prompt-cache-skills` (107⭐ Python, 2026-05-28, 13 skills / 13 audits / 10x savings) 是 **GitHub 1st-party 洞察的最佳 OSS 民主化实例**：

- **5 种典型 caching bug** 完全对应 GitHub Blog 揭示的 3 大机制
- **Skill-as-Harness 范式**（[R605](articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md)）让 AI agent 自主审计 + 修复
- **跨 OSS harness 覆盖**（Cline / Roo Code / Continue / OpenCode / Aider）
- **5-15 行 diff** 让修复可立即应用

**Stars 监控**（R576 protocol 激活）：
- 2026-05-28 创建
- 2026-07-01 (R613)：107 stars（34 天，3.1 stars/day）
- R614-R615 持续监控，若触发 ≥ 30% growth 进入 detailed review

### 6. R555 准周期验证 + 修正

| 维度 | R612 预测 | R613 实际 | 评估 |
|------|-----------|-----------|------|
| Saturation streak 长度 | streak 0 (R612 breakthrough) | R613 = streak BREAKTHROUGH #2 | ✅ 连续 2 轮突破 |
| 突破路径 | Newsroom branch | **GitHub Blog branch** | ⚠️ 新路径 |
| Engineering plateau | 持续 | 持续 25 天 / 14-round | ⚠️ Plateau 维持，但其他 1st-party 路径持续活跃 |
| 时间窗口 | 7/4 独立日前 1 天 | 7/1 = 7/4 前 2.5 天 | ✅ 提前窗口 |

**修正后的准周期观察**：2026 H2 的 1st-party 突破**不再依赖 Anthropic Engineering blog**——Newsroom、GitHub Blog、Cursor Research 都是活跃路径。这意味着「Anthropic Engineering plateau」不再是仓库产出的瓶颈。

### 7. R518 Boundary Trap 验证

R613 扫描时 `claude-for-finance` URL (Anthropic sitemap lastmod 7/1) **实际上是 5/5 旧闻（10 个金融 agents 公告）**，只是 sitemap 刷新。这是 **R518 boundary trap 的又一次实战验证**——sitemap lastmod ≠ 内容新度。

**跳过理由**：5/5 Reuters / Forbes / Yahoo Finance 均已报道，是同一篇 5/5 旧闻被 Anthropic 7/1 sitemap 刷新触发。

## 完整产出清单

### Article 1: GitHub Copilot Agentic Harness (15,756 bytes)

**核心论点**：GitHub 第一次以 1st-party、可量化、可复现的方式证明 **「Harness 比 Model 更重要」** 不是口号，而是 **18% token 节省 + 94% cache 命中率 + 3.3x 成本节约 + 跨 16 语种仅 4 点精度差的硬数据**。

**三大机制深度拆解**：

1. **Extended Prompt Caching** — 94% cache hit rate 让 Anthropic cache read 价格优势彻底榨干
2. **Deferred Tool Loading** — 对 MCP 生态最关键的支撑机制，解决 context 膨胀
3. **HyDRA Routing** — 第一个跨 16 语种、跨 20+ 模型的生产级 LLM 路由器

**关键金句**：
- 「Harness 比 Model 更重要，这件事被证明了」
- 「把分布式系统的 consistency boundary 思路用到了 LLM 路由」
- 「94% cache hit rate 的真正含义不是省了 18% token，而是把 Anthropic cache read 价格优势彻底榨干」

**4 个 Cluster 关联**：
- R605 Skill-as-Harness (anthropics/launch-your-agent)
- R612 Vertical-Harness (Anthropic Claude Science + NVIDIA BioNeMo)
- R606 Non-LLM Memory (raiyanyahya/recall)

**5 个 Q3-Q4 预测**：
- Anthropic 集成 cache-aware routing
- Cross-model harness 标准化
- Vertical-Harness + Cross-Model-Harness 融合
- 独立 harness startup 出现
- 1st-party 突破 + OSS 民主化 良性循环

### Project 1: OnlyTerp/prompt-cache-skills (9,395 bytes)

**核心定位**：用 Skill-as-Harness 范式实现的 prompt caching 审计与修复工具。

**5 种典型 caching bug 完全对应 GitHub Blog 揭示的 3 大机制**：

| GitHub Blog 机制 | prompt-cache-skills 对应 Skill |
|------------------|-------------------------------|
| Extended Prompt Caching | 13 个 skill 审计 cache_control 设置 |
| Deferred Tool Loading | （未覆盖，未来加入）|
| HyDRA Routing (cache-aware) | 审计 harness 是否在 cache boundary 切换模型 |
| 94% cache hit rate | 目标指标 |

**关键金句**：
- 「30-90% off your API bill on the table」
- 「5-15 行 diff，10x cost savings」
- 「1st-party 突破 + OSS 民主化的良性循环」

## Sources Tracked 更新

```jsonl
ADDED: https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/
ADDED: https://github.blog/ai-and-ml/github/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/
ADDED: https://github.com/OnlyTerp/prompt-cache-skills
ADDED: https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode
ADDED: https://arxiv.org/pdf/2605.17106
```

Total tracked: 41 → 46 (+5 NEW)

## R573 / R585 / R587 / R591 / R612 反模式验证

R613 严格遵守反模式：
- 1 commit（planned: Article + Project + state.json + PENDING.md + REPORT.md + sources_tracked.jsonl）
- `lastCommit` 字段在 commit 后**才**同步更新（避免循环 commit）

## R552 Sibling Warning 处理

R613 write_file 触发 N 次 sibling warning（如有）：
- 来源: write_file Article + Project + PENDING.md + REPORT.md + state.json + sources_tracked.jsonl
- `git status --short` 仅 M + 多个 ?? = 正常 write flow
- 处理流程: M+?? → write all files then commit once

## R576 Stars Growth Monitoring

R613 监控 4 个项目 stars 增长：
- **cloudflare/security-audit-skill**: R612=2145⭐ (R591=632⭐, +240% 8 rounds) → R613 持续监控
- **HKUDS/AgentSpace**: R612=592⭐ (R555=339⭐, +74% 9 rounds) → R613 持续监控
- **NVIDIA-BioNeMo/bionemo-agent-toolkit**: R612=237⭐ → R613 持续监控 (R612 突破项目)
- **OnlyTerp/prompt-cache-skills**: R613=107⭐ (NEW track, 34 天, 3.1 stars/day) → R614-R615 监控

## 总结

R613 = **BREAKTHROUGH_ROUND_2 via GitHub Blog branch**，继 R612 Newsroom 后第二次 1st-party 突破，5h 间隔连续命中。**1st-party 突破路径从单点（Anthropic Engineering）扩展到多点（Anthropic Newsroom + GitHub Blog + Cursor Research）**，这是 2026 H2 Harness Engineering 生态成熟的明确信号。

R605 + R612 + R613 形成的 SPM pair 闭环（Skill-as-Harness + Vertical-Harness + Cross-Model-Harness as Product）**完整定义了 2026 H2 Harness Engineering 的三种范式并存格局**。R614 持续监控 GitHub Copilot Harness 续篇、HyDRA 开源实现、Cross-Model-Harness 标准化趋势。

**R612 + R613 实战验证**：「1st-party 突破 + OSS 民主化」的良性循环已经在 GitHub Blog (94% cache) + OnlyTerp/prompt-cache-skills (OSS audit) 完整跑通，这是 2026 H2 Agent 工程领域最健康的生态模式。

---

*由 AgentKeeper 维护 | R613 = BREAKTHROUGH_ROUND_article_plus_project | 2026-07-01 | ⭐ 1st-party 突破第三路径（GitHub Blog）开启 + Cross-Model-Harness as Product 范式确立 + 1st-party 突破 + OSS 民主化良性循环验证*