## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R406) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R406) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本超时（30s） | 🔴 高 | R392-R406 连续15次超时，需批量 git 查询修复 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| 扫描频率调整 | 流程 | 2小时触发 vs 内容天/周更新 | 🟡 中 | 考虑降低到每6-12小时 |

## 🔮 下轮规划（R407）

- [ ] 评估 claude.com/blog 其余 11 个 high-quality 候选（connectors-for-everyday-life 9.7K / how-a-non-technical 14.2K / how-brex 7.7K / subagents-in-claude-code 已 R406 / building-multi-agent-systems-when-and-how-to-use-them 24K 等）
- [ ] 关注 anthropic.com/news 8 个 untracked
- [ ] 持续监测 VoltAgent/awesome-claude-code-subagents 元编排发展
- [ ] 关注 gen_article_map.py 超时问题修复

## 🧠 轮次积累结论

1. **R406 Cycle 结论**：R337+R345+R393 三层 filter pipeline 实战稳定，138 untracked → 1 选定（filter skip rate 99.3%）
2. **3 子域扫描协议 R388+ 持续验证**：engineering 100% 命中 / blog 0% 必须 sitemap / news 80% HTML
3. **Path A 在饱和期仍合法**（R397 协议 #31 三条件）：filter ≥1 候选 + cluster 0→1 启动 + 4-way SPM 满中
4. **R375 4-way SPM 评分算法 6 轮连续满中**（R375/R383/R397/R401/R406）= 稳定默认判定路径
