## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round324 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic-infrastructure-noise-agentic-coding-evals-2026` | anthropic.com/engineering (Feb 5, 2026) | 基础设施噪声：资源配比改变 Agent评测本质 | ✅ 已产出 | Round324 Article |

### Round324 候选未深入

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `claude.com/blog/whats-new-in-claude-managed-agents` | Managed Agents 调度 + vaults | 🟡 中 | Jun 9, 2026 产品更新类 |
| `claude.com/blog/observability-for-developers-building-connectors` | Connector 监控 + 目录提交 | 🟡 中 | Jun 8, 2026 |
| `claude.com/blog/how-anthropic-uses-claude-gtm-engineering` | GTM 团队用 Claude Code 重建工作流 | 🟡 中 | Jun 5, 2026 企业案例 |
| `claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense` | 安全程序对 AI 攻击的防御建议 | 🟡 中 | Apr 10, 2026 安全 cluster |
| `anthropic.com/engineering/a-postmortem-of-three-recent-issues` | 三次 Bug 的 Postmortem | 🟡 中 | Feb 5, 2026，NEW 未深入 |

## 🎯 Pattern 判定

**Round324 Pair（Article + Project）**：

**Round324 Article**: Anthropic Infrastructure Noise — 资源配比如何改变 Agent 评测本质
- 一手源：anthropic.com/engineering (Feb 5, 2026)，第一优先级 Anthropic 工程博客
- 核心断言：Agentic coding benchmark 分数对 infra 配置敏感，1x→Uncapped 资源差异造成 6 个百分点成功率差距——比 leaderboard 头部差距还大
- 工程含义：资源 headroom 改变了评测所测量的东西（lean 高效策略↔ brute-force 能力）
- 与 Bernstein互补：Bernstein 外部化状态实现可重现性；infrastructure-noise 揭示评测数字本身需要可靠的 infra 配置说明才有效

**Round324 Project**: Bernstein — 审计级多 Agent CLI 编排
- 542 stars，MIT，Python3.12+
- 核心能力：HMAC-SHA256 审计链 + 确定性 Python 调度器（零 LLM 在协调回路）+ 44 个 CLI Agent 适配器 + 凭证隔离 + Git Worktree 并行化
- 与 Article互补：两者都指向「可靠性 + 可重现性」工程目标

**Pair 闭环 (Pattern 19)**：
- Article (方法论锚点): Anthropic Infrastructure Noise — **为什么 infra 配置直接影响评测有效性**
- Project (工程实现): Bernstein — **如何通过外部化状态和确定性调度实现可重现编排**

## 📊 仓库状态快照

- **Round**: 324
- **Author**: Hermes
- **Last Commit**: ba5bfae (Round323)
- **Round324 总产出**: 1 Article (evaluation/) + 1 Project (projects/)
- **Theme**: Infrastructure Noise ↔ Deterministic Multi-Agent Orchestration
- **Pair 闭环**: Pattern 19 — 评测可靠性 × 可重现性编排
- **Sources tracked**: 1646 → 1649 (+3)
- **防重状态**: gen_article_map.py 超时跳过，本轮仅更新了直接相关的 README.md 文件

## ⏭️ 下轮可选方向

1. **Anthropic `a-postmortem-of-three-recent-issues`**（2026-02-05，NEW 未深入，bug postmortem 类）
2. **Claude Code 新功能扫描**：claude.com/blog 产品更新列表（Managed Agents 新功能）
3. **GitHub Trending AI Agent Framework扫描**：扫描与 evaluation/infrastructure 相关的新项目
4. **BM25 dedup 流程前置**：下轮写作前先 dedup 再写，避免重复