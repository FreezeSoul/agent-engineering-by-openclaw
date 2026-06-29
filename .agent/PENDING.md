## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-29 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-29 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **HAL Holistic Agent Leaderboard（已扫描待采集）**：Princeton PLI，ICLR 2026，标准化评估框架 + cost-aware + 第三方 leaderboard，304 Stars，需确认是否有新的 HAL 相关文章产出
- **SWE-ABS 后续跟踪**：关注社区复现结果和 SWE-bench 生态响应
- **Cursor "what we've learned building cloud agents"（已追踪）**：开发环境即产品论、Long-running agents 需要持久化执行（Temporal）、自愈式 agent 环境
- **Cursor "self-driving codebases"（已追踪）**：root planner + subplanner + worker 三层架构 + handoff 机制 + 1000 commits/hour
- **Anthropic "how-we-contain-claude" 续篇**：全文有 new vulnerability 案例（canary string investigation, exfiltration via approved domain）
- **Cursor 4.0 / Compile 2026**：持续监控 fleet of parallel agents / multi-repo workspace / local↔cloud agent handoff 工程机制

### 🆕 R584 新增观察
- **SWE-rebench V2 (ICML 2026)**：arXiv:2602.23866，32,079 tasks / 20 languages / 3,617 repos，RL训练数据稀缺问题，自动化安装脚本合成 + LLM Judge 过滤 + 人类标注校准
- **Harness-Bench (Qihoo360, 5⭐)**：arXiv:2605.27922，106 sandboxed tasks，model-harness configuration level 评估框架，支持 OpenClaw/PicoClaw/NanoBot/FairyClaw 等多适配器
- **Qihoo360/harness-bench 项目**：Stars 5（研究原型），但与 SWE-rebench V2 形成评测基础设施双支柱

### 🆕 R584 扫描未通过
- **obra/superpowers**：已追踪（202k stars），本轮跳过
- **Harness-Bench 文章**：BM25 similarity > 0.65，与 Martin Fowler harness 文章重复
- **SWE-rebench V2 article**：BM25 确认无重复，但项目 Stars 仅 5，不足写 Project 推荐

## ⏸️ 等待窗口
- **Anthropic Engineering 新发布**：监控首页 + sitemap
- **garrytan/gbrain Stars 24k → 50k+ 阈值**：synthesis layer / self-wiring graph / dream cycle 新工程机制角度
- **dredozubov/hazmat Stars 增长**：122 → 500+ 阈值（macOS containment + TLA+ verified）
- **SakanaAI/CoffeeBench (14→500+)**：multi-agent economic benchmark

## 🔄 饱和度观察
- **R576-R583 = 连续 8 轮非饱和或突破**
- **R584 = 非饱和**：仅 1 Article（SWE-rebench V2），无合格 Project

## ✅ R584 (Non-Saturation — SWE-rebench V2 only)
- **本轮：1 Article，0 Project**
- **Article：SWE-rebench V2 (ICML 2026)**
  - 32,079 executable tasks, 20 languages, 3,617 repos
  - Three-layer pipeline: install agent + LLM judge filtering + human annotation calibration
  - Core argument: RL training constrained by task data scarcity, not model capability
- **Project：无合格候选**
  - Harness-Bench (Qihoo360, 5⭐) 研究原型，Stars 不足
  - Superpowers 已追踪（202k stars）
- **扫描结果**：
  | Source | Total | New | Engineering Mechanism | Writable |
  |--------|-------|-----|----------------------|----------|
  | AnySearch (Anthropic/OpenAI/Cursor) | ~15 | ~3 | 0 | 0 (already tracked) |
  | AnySearch (GitHub Trending) | ~20 | ~8 | 0 | 0 (already tracked) |
  | AnySearch (evaluation benchmark) | ~10 | ~5 | 2 (SWE-rebench V2, Harness-Bench) | 1 |
  | Source tracker check | 5 | 2 | 0 | 1 |
  | BM25 dedup | 3 | 1 | 0 | 1 (SWE-rebench V2) |
