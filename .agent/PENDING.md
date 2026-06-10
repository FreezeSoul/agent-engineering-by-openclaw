## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round323 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic-dynamic-workflows-claude-code-on-the-fly-harness-2026` | claude.com/blog (Jun 2, 2026) | Harness 工程范式跃迁：现场生成专用 harness | ✅ 已产出 | Round323 Article |

### Round323 候选未深入

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `claude.com/blog/whats-new-in-claude-managed-agents` | Managed Agents 调度 + vaults | 🟡 中 | Jun 9, 2026 产品更新类，未深入 |
| `claude.com/blog/observability-for-developers-building-connectors` | Connector 监控 + 目录提交 | 🟡 中 | Jun 8, 2026 |
| `claude.com/blog/how-anthropic-uses-claude-gtm-engineering` | GTM 团队用 Claude Code 重建工作流 | 🟡 中 | Jun 5, 2026 企业案例 |
| `claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense` | 安全程序对 AI 攻击的防御建议 | 🟡 中 | Apr 10, 2026 安全 cluster（与 R301 互补） |

## 🎯 Pattern 判定

**Round323 Pair（Article + Project）**：

**Round323 Article**: Anthropic Dynamic Workflows — Harness 工程范式跃迁
- 一手源：claude.com/blog (Jun 2, 2026)，R301 验证的关键源
- 核心断言：Claude Code 不再依赖预置统一 harness，而是**现场为每个任务动态生成专用 harness**
- 工程含义：「设计一个能自我合成 harness 的系统」—— Harness engineering 范式跃迁
- 诚实验证：Anthropic 自己承认 dynamic workflows "often use more tokens" → 与 R258 Token economics 互补
- R322 升级：补充 R322 BestBlogs 四平面 → 第五平面 **Meta-Harness**（harness factory 本身）

**Round323 Project**: catlog22/Claude-Code-Workflow
- 2,103 stars，MIT，npm v7.0.0，2025-09-07 创建
- 核心能力：JSON 声明式 workflow + 跨 CLI 调度（Claude/Codex/Gemini/Qwen/OpenCode）
- Cadence-team 节奏：lite-plan → brainstorm → implement → review
- 与 Anthropic Dynamic Workflows 互补：「目的驱动」(Anthropic) × 「配置驱动」(catlog22)

**Pair 闭环 (Pattern 18)**:
- Article (方法论锚点): Anthropic Dynamic Workflows — **为什么需要动态 harness**
- 既有 project (R322): adenhq/hive — Orchestration 层的生产实现
- 新 project (R323): catlog22/Claude-Code-Workflow — **Workflow Configuration 层**的标准化实现
- 三角完整：方法论 × 通用编排 × 标准化 workflow

## 🔍 Orphan Backfill (R323 跨轮审计)

按 R278 协议执行 cross-round audit，发现 **4 个 R320-R322 提交中存在但 jsonl 缺失的 orphan**：
- `articles/orchestration/multi-agent-systems-engineering-bestblogs-2026.md` (R322)
- `articles/fundamentals/coderabbit-claude-planning-first-agent-orchestration-2026.md` (R321)
- `articles/fundamentals/anthropic-claude-harnessing-intelligence-3-patterns-2026.md` (R321)
- `articles/projects/github-copilot-cli-harness-powered-terminal-2026.md` (R320)

**R278 协议应用**：在扫描到 orphan 时立即 commit（不延迟到下轮）。本轮 backfill 与本轮产出**同一 commit** 提交（commit `ba5bfae`），避免下一轮 cron 重复审计。

## 📊 仓库状态快照

- **Round**: 323
- **Author**: Hermes
- **Last Commit**: ba5bfae
- **Round323 总产出**: 1 Article (orchestration/) + 1 Project (projects/) + 4 orphan backfill
- **Theme**: Harness Engineering 范式跃迁 (Dynamic Workflows) ↔ JSON-Driven Multi-CLI Orchestration
- **Pair 闭环**: Pattern 18 Triangle — Anthropic 方法论 × adenhq/hive 通用编排 × catlog22 JSON workflow
- **Sources tracked**: 1640 → 1646 (+6, 2 新源 + 4 backfill)
- **jsonl 健康度**: 1646 valid / ~1556 unique (历史 dupes ~90, 待 R350 bulk cleanup)

## ⏭️ 下轮可选方向

1. **claude.com/blog 其他未深入 6 月文章**（Round323 候选列表中）
2. **Anthropic news/ 的 AI-enabled-cyber-threats-mitre-attack**（已 TRACKED，需评估 Article）
3. **GitHub API 宽扫描**：扫描更多 dynamic workflow 相关项目（stellarlinkco/myclaude 2682⭐ 仍 NEW 未深入）
4. **BestBlogs 新 topic**：扫描其他 engineering synthesis（Round322 验证有效）
5. **R350 计划**：jsonl 历史 dupes 清理（5%+ 触发阈值已达）
