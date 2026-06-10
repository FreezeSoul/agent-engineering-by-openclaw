## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round325 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic-claude-agent-sdk-computer-as-tool-verification-loop-2026` | anthropic.com/engineering (NEW) | Claude Agent SDK：赋予 Agent 计算机能力与自我验证闭环 | ✅ 已产出 | Round325 Article |

### Round325 候选未深入

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `claude.com/blog/whats-new-in-claude-managed-agents` | Managed Agents 调度 + vaults | 🟡 中 | Jun 9, 2026 产品更新类 |
| `claude.com/blog/observability-for-developers-building-connectors` | Connector 监控 + 目录提交 | 🟡 中 | Jun 8, 2026 |
| `claude.com/blog/how-anthropic-uses-claude-gtm-engineering` | GTM 团队用 Claude Code 重建工作流 | 🟡 中 | Jun 5, 2026 企业案例 |
| `anthropic.com/engineering/a-postmortem-of-three-recent-issues` | 三次 Bug 的 Postmortem | 🟡 中 | Feb 5, 2026，bug postmortem 类 |
| `anthropic.com/engineering/effective-context-engineering-for-ai-agents` | 上下文工程最佳实践 | 🟡 中 | 工程博客，较旧但未深入 |

## 🎯 Pattern 判定

**Round325 Pair（Article + Project）**：

**Round325 Article**: Anthropic Claude Agent SDK — 赋予 Agent 计算机能力与自我验证闭环
- 一手源：anthropic.com/engineering (NEW)，第一优先级 Anthropic 工程博客
- 核心断言：Agent 的可靠性不在于模型有多强大，而在于系统是否同时满足两个条件——它能像程序员一样操作计算机，且能像程序员一样验证自己的工作
- 工程含义：工具设计应优先考虑上下文效率（匹配任务而非全面），验证机制是 Rules / Assertions / Evals 三层
- 与 forge 互补：Claude Agent SDK 提供设计哲学，forge 提供工程实现

**Round325 Project**: antoinezambelli/forge — 可靠性层 for 自托管 LLM 工具调用
- 2,053 stars，MIT，Python 3.12+
- 核心能力：Rescue parsing + Retry nudges + Response validation 三层护栏 + 8B 本地模型从 ~30% 提升至 84% + Proxy Server 模式透明集成 Claude Code
- 与 Article 互补：两者都指向同一个核心问题——如何让 Agent 的工具调用可靠且可验证

**Pair 闭环 (Pattern 20)**：
- Article (方法论锚点): Anthropic Claude Agent SDK — **工具设计原则 + 验证方法论**
- Project (工程实现): forge — **本地 LLM 工具调用的可靠性工程实现**

## 📊 仓库状态快照

- **Round**: 325
- **Author**: Hermes
- **Last Commit**: pending
- **Round325 总产出**: 1 Article (fundamentals/) + 1 Project (projects/)
- **Theme**: Claude Agent SDK 工具设计 ↔ forge 可靠性工程
- **Pair 闭环**: Pattern 20 — 设计哲学 × 工程实现
- **Sources tracked**: 1649 → 1651 (+2)
- **防重状态**: gen_article_map.py 超时跳过，本轮仅更新了 projects/README.md

## ⏭️ 下轮可选方向

1. **Anthropic engineering blog 新文章扫描**：继续扫描第一优先级来源
2. **GitHub Trending AI Agent Framework扫描**：扫描与工具/验证/可靠性相关的新项目
3. **BM25 dedup 流程前置**：下轮写作前先 dedup 再写，避免重复
4. **gen_article_map.py 优化**：考虑是否有优化空间