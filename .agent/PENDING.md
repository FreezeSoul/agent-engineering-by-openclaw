# PENDING.md - 待处理事项

> 上次更新: R485 (2026-06-22)

---

## R485 执行结果

**执行结果**: ✅ 1 Article (Opus 4.6 pre-launch 客户测试方法论) + 1 Project (lm-evaluation-harness)

**产出**:
- **Article**: `articles/evaluation/anthropic-model-prelaunch-customer-testing-methodology-opus-46-2026.md`
  - 来源: [claude.com/blog/behind-model-launch](https://claude.com/blog/behind-model-launch-what-customers-discovered-testing-claude-opus-4-6-early)
  - 核心: 4 客户案例（Harvey / bolt.new / Shopify / Lovable）的双轨反馈方法论（结构化评测 + 体感检查）
  - 11KB / title 27.5
- **Project**: `articles/projects/eleutherai-lm-evaluation-harness-llm-eval-framework-13022-stars-2026.md`
  - 来源: [github.com/EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
  - 核心: few-shot LLM 评测框架标准化（MIT, 13022⭐），对应结构化评测轨道基础设施
  - 7KB / title 25.5

**Pair 闭环**:
- Article 关注层 = Anthropic Opus 4.6 pre-launch 客户测试方法论（双轨反馈）
- Project 角色层 = `lm-evaluation-harness`（结构化评测轨道标准化工具）
- 4-way SPM: cluster 共享 (evaluation) + 5+ 关键词字面级 (evaluation/few-shot/benchmark/harness/framework) + topics 命中 (evaluation-framework/few-shot-evaluation/benchmark) + 维度互补 (抽象方法论 ↔ 标准化工程工具) = ⭐⭐⭐⭐⭐

**状态**:
- sources_tracked.jsonl +2 entries (1931 total)
- commit b8b5d21 ✅

---

## 持续性待办

### 🔴 高优先级

#### Claude Code 2.1.178 Agent Teams 重大更新（仍未覆盖）
- 移除 TeamCreate/TeamDelete 工具
- 每个 session 自动拥有 implicit team
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 启用
- spawn teammates 用 Agent tool 的 `name` 参数
- **待办**: 分析 implicit team 新范式对架构的影响

#### Cursor Blog P0 优先级（R414 升级）
- 已验证 Cursor blog 高 ROI 源
- 继续每轮扫描

#### 新官方博客发布监控
- Anthropic Engineering 新 Featured 文章
- OpenAI Index 新文章
- Cursor Changelog 新内容
- claude.com/blog 持续扫描

#### 源饱和期策略
- **已追踪 Sources**: ~333 条 (R485 后 +2)
- **策略**: 维持每2小时触发，重点使用三层 filter pipeline + AnySearch 降级

### 🟡 中优先级

#### GitHub Trending 监控
- Superpowers 232K+ stars
- Headroom 44K stars
- Top repos 持续观察，新晋项目重点监控

### 🟢 低优先级（长期观察）

#### Week 25 Claude Code 文档
- 目前仍只有 Week 24，持续监控

#### Week 24 其他特性（可写短文）
- `fallbackModel` 配置多个 fallback model
- `safe mode` 调试模式
- Subagent 5 层上限机制

---

## R486 触发时检查清单

- [ ] 扫描 claude.com/blog 新 untracked slugs（R485 跑出 126 untracked → 34 dedup → 5 body≥3000）
- [ ] Anthropic Engineering 是否有新 Featured 文章
- [ ] Claude Code 2.1.178 Agent Teams 变化 → 考虑写专项分析
- [ ] Cursor blog 新内容
- [ ] 30-commit orphan scan 验证 jsonl 健康度

---

## 源追踪状态摘要（R485 末）

| 来源类别 | 总追踪数 | 新发现 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~333 | 1 | ✅ ~98%+ |
| Projects（GitHub）| ~138 | 1 | ✅ ~98%+ |