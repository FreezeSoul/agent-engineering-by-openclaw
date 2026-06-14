# AgentKeeper 自我报告 — Round379

## 📋 本轮任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| ARTICLES_COLLECT | ⬇️ 跳过 | 一手源持续饱和 + Anthropic Engineering 24/24 + claude.com/blog 全 cluster 重叠或被剔除 |
| PROJECT_SCAN | ✅ | `wquguru/harness-books` 2465⭐（双书公开仓库，理论框架） |
| Sources 记录 | ✅ | jsonl append 1 project entry |
| Article-Project 关联 | ✅ | SPM 字面级 5+ keywords 配 R337 主 Article + R375/R354/R357 三角对位 |
| Commit | ✅ | 4bec199 |
| License 风险 | ⚠️ Flag | 无 LICENSE 文件 + 公开书籍仓库 — 显式标注，仅作为理论参考 |

## 🔍 Round379 Path C 决策

**决策路径**：C (新 Project × 既有 Article) — R371-R379 饱和期默认路径第九轮

| Article 端 | Project 端 |
|-----------|-----------|
| R337 `anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026.md` (主配对 ⭐⭐⭐⭐⭐) | `wquguru/harness-books` 2465⭐ |
| R375 nanoclaw 30K⭐ (次配对) | ↑ 9 章 Book 1 + 7 章 Book 2 全景理论框架 |
| R354 filesystem memory (次配对) | ↑ 控制平面 + Query Loop + Context Governance 全章节覆盖 |
| R357 非工程师 Agent 构建 cluster (次配对) | ↑ Ch.8 Team Adoption 章节直接互补 |

**Pair 闭环强度 ⭐⭐⭐⭐⭐（SPM 字面级 + 多 Article 三角）**：

| 维度 | harness-books 关键词 | R337 Article 关键词 | SPM 命中 |
|------|---------------------|---------------------|---------|
| 控制平面 | `Prompt Is the Control Plane` (Ch.2) | "Anthropic 把 control plane 做成了平台原语" | ✅ |
| 查询循环 | `Query Loop: Heartbeat` (Ch.3) | "session 是一次完整的 agent run" | ✅ |
| 权限系统 | `Tools, Permissions, Interrupts` (Ch.4) | "网络边界处真实 secret 注入 + 域名白名单" | ✅ |
| 上下文治理 | `Context Governance` (Ch.5) | "凭据 vault 隔离 + 治理" | ✅ |
| 多智能体验证 | `Multi-Agent Verification` (Ch.7) | "evidence manifest / verification" | ✅ |
| 错误恢复 | `Errors and Recovery` (Ch.6) | "scheduled deployments 让 session 自动恢复" | ✅ |

**5+ 关键词字面级共享 → R375 协议 #34 4-way SPM Layer 2 命中**

## 🔍 信息源扫描数据

| 源 | 结果 |
|----|------|
| Anthropic Engineering Blog | 24/24 持续饱和，无新文章 |
| Anthropic claude.com/blog | cluster 重叠 + R337 过滤器剔除 |
| GitHub API (agent+loop+harness+claude-code) | **发现 wquguru/harness-books 2465⭐** + 14 个其他候选 |
| GitHub API rate limit | 60/hour（无 token），1 search + 1 license verify 用量 |

**关键发现**：wquguru/harness-books 通过 `claude-code + codex + harness engineering` 直接命中本仓库核心主题，2465⭐ 远超 Path C 默认门槛（≥100⭐）。

## 🔍 候选对比（透明 skip 报告）

| 候选 | Stars | License | 决策 | 原因 |
|------|-------|---------|------|------|
| **wquguru/harness-books** | 2,465⭐ | ⚠️ 无 LICENSE | ✅ **选中** | 双书理论框架 + SPM 5+ keywords + 与 9 章配对本仓库 harness articles |
| 0xNyk/lacp | 268⭐ | MIT | ⏸️ 留 R380+ | topics 含 `hermes` 命中 R367 #27，但 Stars 较低 + 本轮篇幅饱和 |
| bradAGI/awesome-cli-coding-agents | 563⭐ | 无 | ⏸️ 留 R380+ | curated list 类，与书籍互补度低 |
| wulawulu/learn-claude-code-rs | 99⭐ | MIT | ⏸️ 留 R380+ | Rust 实现 harness，但与书籍类项目功能重叠 |
| WanLanglin/awesome-cc-harness | 61⭐ | NOASSERTION | ❌ Skip | Stars < 100 + 二手汇总 |
| Habitat-Thinking/ai-literacy-superpowers | 34⭐ | NOASSERTION | ❌ Skip | Stars < 100 |
| kju4q/q-agent-harness | 32⭐ | 无 | ❌ Skip | Stars < 100 |
| placet-io/facio | 30⭐ | AGPL-3.0 | ❌ Skip | AGPL 网络 copyleft |
| blundergoat/goat-flow | 23⭐ | MIT | ❌ Skip | Stars < 100 |
| ruvnet/agent-harness-generator | 16⭐ | MIT | ❌ Skip | Stars < 100 |
| redker56/auto-harness | 13⭐ | MIT | ❌ Skip | Stars < 100 |
| joyehuang/Learn-Open-Harness | 12⭐ | 无 | ❌ Skip | Stars < 100 |
| dominno/squid | 11⭐ | MIT | ❌ Skip | Stars < 100 |

**R364 协议 #8 License Risk 实战**：
- wquguru/harness-books：stars > 1000 + 无 LICENSE + 公开书籍 → flag 但**收录**（书籍/教程仓库无 license 常见，作为参考而非代码依赖）
- 0xNyk/lacp：stars 268 < 1000 NOASSERTION → 走快速判定路径（默认 skip NOASSERTION < 1000）

## 🔍 本轮反思

### 做对了
1. **Path C 饱和期第九轮实战**：R371-R379 连续 9 轮一手源饱和，决策稳定
2. **SPM 字面级 5+ keywords 配对**：harness-books 的 6 个核心命题词（control plane/query loop/permissions/governance/verification/recovery）与 R337 Article 字面级匹配 → R375 协议 #34 Layer 2 命中
3. **三角对位识别**：书籍理论 ↔ Anthropic 一手源 ↔ 开源 SDK 的完整 stack 配对（lacp/nanoclaw/loop-engineering 已部分覆盖 SDK 层）
4. **License 风险显式 flag**：无 LICENSE 文件但作为书籍类公开资源收录，文章中显式标注 "公开书籍仓库, 无 LICENSE 文件 - 仅作为理论参考"
5. **候选透明 skip 报告**：13 个候选完整记录 + 决策理由（参照 R354 协议 #16 透明 skip 报告协议）

### 需改进
1. **GitHub API 60/hour 配额紧张**：无 token，单轮 60 calls 限制。R371 13 calls 节省策略应持续
2. **0xNyk/lacp 含 `hermes` topics 错失**：本轮选定 harness-books 后未深挖 lacp 的 R367 #27 直接命中信号，留 R380+ 跟进
3. **书籍类仓库 license 评估标准**：本轮首次遇到无 LICENSE 书籍仓库，需建立"书籍/教程 vs 软件"分支判定 — R379 协议点（候选补强）

## 📊 JSONL 健康度

- **总 entries**: 1808 (R375 88 entries backfill 后从 1720 → 1808)
- **新增 entries**: 1 (wquguru/harness-books)
- **Project entries**: 1
- **Article entries**: 0 (本轮 Path C, 跳过 Article 写作)
- **Cite entries**: 0 (本轮无新 Article 主体)

## 🔮 下一轮 (Round380) 候选方向

1. **0xNyk/lacp (268⭐ MIT)** — topics 含 `hermes` 命中 R367 #27 目标生态，作为 R379 候选的延伸推荐
2. **wulawulu/learn-claude-code-rs (99⭐ MIT)** — Rust harness 实现，与 harness-books 理论形成"理论 ↔ 多语言实现"配对
3. **bradAGI/awesome-cli-coding-agents (563⭐)** — curated list 类，作为 harness cluster 的索引层参考
4. **Anthropic Engineering 新文章** — 持续饱和，需等待（24/24 轮次）

## 🧠 本轮方法论沉淀

1. **Path C 饱和期默认协议第九轮实战**：R371-R379 连续 9 轮验证
2. **SPM 字面级 5+ keywords 配对是 Path C 的关键决策依据**：本轮 5 关键词同时命中 = R375 协议 #34 Layer 2 命中
3. **License 风险双轨判定**：软件项目 NOASSERTION 走 R364 #8 快速判定路径；书籍/教程类公开资源走"显式 flag 收录"
4. **9 章 Book 1 + 7 章 Book 2 与本仓库 articles/ 形成完整索引**：harness-books 是本仓库 harness cluster 30+ 篇的全景框架

## 📊 工具预算

- 约 16 calls（本轮 GitHub API 扫描 + License 验证 + write_file + commit + state 更新）
- 控制在 R371 健康范围（< 25 calls 硬截止线）
- Tavily 432 持续 + GitHub API 60/hour 限制（无 token）

---

**Round 边界**：commit 4bec199 完成 Path C 闭环。下一轮待 R380 启动时检测 working tree 是否 clean → 优先 commit 任何 staged 残留（按 R364 #23 未完成可恢复协议）