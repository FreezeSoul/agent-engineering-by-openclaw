## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-19 (R440) | 每轮必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-19 (R440) | 每轮必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| `cursor.com/blog/increased-agent-usage` | ⏸️评估中 | cursor.com/blog | agent usage trends | R439 遗留，唯一未 dedup cursor 候选 |
| `cursor.com/blog/cowork-plugins-finance` | ⏸️评估中 | cursor.com/blog | finance plugins + cross-app workflows | cross-app workflows 与 R439 multi-agent orchestration 关联 |
| ponytail (DietrichGebert) | ⏸️评估中 | github.com | 34K→35K stars, 5x 增长 | 考虑是否值得更新（已有 R360 article） |
| `XiaomiMiMo/MiMo-Code` | ✅已覆盖 | github.com | 9,736⭐ judge model + checkpoint | R440 新发现，harness cluster |
| `walkinglabs/learn-harness-engineering` | ✅已覆盖 | github.com | 8,807⭐ 12×6 course | R440 新发现，harness ecosystem |

## 🔴 高优先级问题

| 问题 | 来源 | 状态 | 备注 |
|------|------|------|------|
| Tavily API rate limit | 外部API | 🔴 持续 | R411-R440 连续30轮触发 432 错误，AnySearch + GitHub API 降级路径稳定 |
| Anthropic engineering 枯竭 | 系统 | 🔴 持续 | 24/24 已全部 tracked |
| claude.com/blog 高 skip rate | 系统 | 🟢 稳定 | 135 untracked → 1 候选（99.3% skip rate），每轮稳定产出 1 高质量 article |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `cursor.com/blog/increased-agent-usage` | cursor.com/blog | agent usage 趋势 | 🟡 中 | 唯一未被 dedup 的 cursor 候选，R439 遗留 |
| `cursor.com/blog/cowork-plugins-finance` | cursor.com/blog | finance plugins + workflows | 🟡 中 | cross-app orchestration 关联 R439 multi-agent |
| `ponytail` | github.com | 34K stars | 🟡 低-中 | 已有 R360 article，stars 5x 增长可能值得更新 |

## 📌 Articles 线索

- **GitHub API 是发现新项目的主路径**：`stars:>=3000 + created:>2026-03-01` 能有效发现新鲜高价值项目
- **MiMo-Code 仍有潜在内容**：compose mode（specs-driven）、dream/distill 自优化机制未覆盖
- **anthropic.com/research**：论文层，与 engineering 不同的内容类型，R422 计划尚未执行
- **cursor.com/blog dedup 命中率极高**：60 untracked → ~58 dedup hit → 仅 1-2 novel per round

## 🔮 下轮规划（R441）

- [ ] 评估 `cursor.com/blog/increased-agent-usage` — 唯一未 dedup 的 cursor 候选
- [ ] 评估 `cursor.com/blog/cowork-plugins-finance` — cross-app workflows
- [ ] 继续 GitHub API 扫描 `stars:>=2000 + pushed:>2026-06-10`
- [ ] 考虑 ponytail 更新（stars 5x 增长）
- [ ] 监控 Tavily API 额度恢复
- [ ] 探索 anthropic.com/research 论文层内容
