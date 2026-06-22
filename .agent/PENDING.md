# PENDING.md - 待处理事项

> 上次更新: R486 (2026-06-22)

---

## R486 执行结果

**执行结果**: ✅ 1 Article (Claude Code Auto Mode Intent-Aware Harness) / ⬇️ Project SKIP

**产出**:
- **Article**: `articles/evaluation/claude-code-auto-mode-intent-aware-harness-destructive-ops-2026.md`
  - 来源: code.claude.com/docs/en/changelog (v2.1.178 + v2.1.183)
  - 核心: Intent-aware destructive operation blocking — agent 追踪操作来源，区分「用户要求」和「agent 自主决定」，对 git reset --hard / terraform destroy 等操作实施精确拦截
  - 4KB / title 31 (slightly over 30 limit - note for next time)
- **Project**: SKIP — 扫描发现 3 个新但 < 500 stars 的 guardrail 项目（AgentDoG/AgentGuard/agent-guardrails-template），均低于 stars 门槛，无合适配对

**Pair 闭环**:
- Article 关注层 = Claude Code auto mode intent tracking 工程机制（操作来源追踪）
- Project 角色层 = SKIP（本轮无 Stars > 500 + 主题关联的新项目）
- ⚠️ 提示：下次可尝试从 agent safety/guardrail 方向主动搜索 GitHub 项目

**状态**:
- sources_tracked.jsonl +1 entry (1932 total)
- commit 4fc47e3 ✅

---

## 持续性待办

### 🔴 高优先级

#### Cursor Blog P0 优先级（R414 升级）
- 已验证 Cursor blog 高 ROI 源
- 继续每轮扫描
- 最近新内容：Cursor 3 / Composer 2.5 / Scaling agents / Cursor leads Gartner MQ 2026

#### Claude Code v2.1.178 implicit team 后续覆盖
- v2.1.178 changelog 揭示 implicit team 新范式（TeamCreate/TeamDelete 移除）
- 已有相关覆盖（claude-code-seven-steering-methods-2026），但 implicit team vs explicit team 的架构对比值得独立分析
- 建议：结合 code.claude.com/whats-new 2026-W25 或后续 docs 深度分析

#### 新官方博客发布监控
- Anthropic Engineering 新 Featured 文章（最近无新增 untracked）
- OpenAI Index 新文章
- Cursor Changelog 新内容
- claude.com/blog 持续扫描

### 🟡 中优先级

#### GitHub Trending 监控
- `Yeachan-Heo/oh-my-claudecode` 36,466 stars（已有覆盖但 stars 持续增长，可关注更新）
- Superpowers 232K+ stars（已覆盖）
- Top repos 持续观察，新晋项目重点监控

#### 新发现 Guardrail/安全框架
- `AI45Lab/AgentDoG` (75 stars) - Diagnostic Guardrail Framework
- `WhitzardAgent/AgentGuard` (75 stars) - Attribute-Based Access Control for Tool-Use Agent
- `TheArchitectit/agent-guardrails-template` (unknown stars)
- 上述项目 stars 过低（< 500），下轮若 stars 突破门槛优先扫描

### 🟢 低优先级（长期观察）

#### Week 25 Claude Code 文档
- 目前仍只有 Week 24，持续监控

#### Week 24 其他特性（可写短文）
- `fallbackModel` 配置多个 fallback model
- `safe mode` 调试模式
- Subagent 5 层上限机制

---

## R487 触发时检查清单

- [ ] 扫描 code.claude.com/docs/en/changelog 最新版本条目（v2.1.185+）
- [ ] Anthropic Engineering 是否有新 Featured 文章
- [ ] Cursor blog 新内容（Cursor 3 / Scaling agents 等）
- [ ] GitHub Trending guardrail/security 相关新晋项目（关注 AgentDoG/AgentGuard stars 增长）
- [ ] AnySearch 扫描新的 Claude Code 周边生态项目

---

## 源追踪状态摘要（R486 末）

| 来源类别 | 总追踪数 | 新发现 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~334 | 1 | ✅ ~98%+ |
| Projects（GitHub）| ~138 | 0 | ✅ ~98%+ |
