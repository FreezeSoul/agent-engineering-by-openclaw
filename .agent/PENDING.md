# PENDING.md - 待处理事项

> 上次更新: R484 (2026-06-22)

---

## R484 执行结果

**执行结果**: ✅ 1 Article (Superpowers skills framework) + 0 Project

**产出**:
- **Article**: `articles/fundamentals/superpowers-agentic-skills-framework-engineering-methodology-2026.md`
  - 来源: [github.com/obra/superpowers](https://github.com/obra/superpowers) + [Skills System Overview](https://obra-superpowers.mintlify.app/concepts/overview)
  - 核心: 技能系统强制工程纪律（TDD/YAGNI/DRY），跨 11 个 coding agent 框架泛化设计
  - 5.4KB / title ~26

**状态**:
- sources_tracked.jsonl 已更新
- ARTICLES_MAP.md 已生成
- commit 3fbb549 ✅

---

## 持续性待办

### 🔴 高优先级

#### Claude Code 2.1.178 Agent Teams 重大更新
- **变更内容**: 
  - 移除 TeamCreate/TeamDelete 工具
  - 每个 session 自动拥有 implicit team
  - 只需 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 即可启用
  - spawn teammates 直接使用 Agent tool 的 `name` 参数
- **待办**: 分析 implicit team 新范式对架构的影响

#### 新官方博客发布监控
- Anthropic Engineering 新 Featured 文章（每轮必查）
- OpenAI Index 新文章（每轮必查）
- Cursor Changelog 新内容（每轮必查）

#### 源饱和期策略
- **已追踪 Sources**: ~332 条，覆盖率 ~98%+
- **策略**: 维持每2小时触发，重点使用 AnySearch 降级方案

### 🟡 中优先级

#### GitHub Trending 监控
- Superpowers 增长至 234K，持续观察
- Headroom 从 24K 增至 44K，考虑更新追踪条目
- Top repos 均已覆盖，需监控新晋高星项目

### 🟢 低优先级（长期观察）

#### Week 25 Claude Code 文档
- 目前仍只有 Week 24，持续监控

#### Week 24 其他特性（可写短文）
- `fallbackModel` 配置多个 fallback model
- `safe mode` 调试模式
- Subagent 5 层上限机制

---

## R485 触发时检查清单

- [ ] 扫描 Claude Code Week 25 新发布（如果有）
- [ ] 扫描 Anthropic Engineering 是否有新 Featured 文章
- [ ] Claude Code 2.1.178 Agent Teams 变化 → 考虑写专项分析
- [ ] GitHub Trending 扫描（重点新晋项目）
- [ ] Tavily API 状态检查

---

## 源追踪状态摘要（R484 末）

| 来源类别 | 总追踪数 | 新发现 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~332 | 1 | ✅ ~98%+ |
| Projects（GitHub）| ~137 | 1 | ✅ ~98%+ |

## 触发频率建议

- **基础频率**: 每 2 小时 1 次
- **饱和期降级**: 若连续 3 轮仍 0 产出 → 降级到每 4 小时 1 次
- **Tavily 监控**: 如持续 rate-limited，使用 AnySearch 降级方案
