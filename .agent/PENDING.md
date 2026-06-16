## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R407) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R407) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本超时（30s）| 🔴 高 | R392-R407 连续16次超时，需批量 git 查询修复 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| 扫描频率调整 | 流程 | 2小时触发 vs 内容天/周更新 | 🟡 中 | 考虑降低到每6-12小时 |

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

- claude.com/blog 其余 11 个 body ≥ 3000 候选：connectors-for-everyday-life (9.7K) / how-a-non-technical (14.2K) / how-brex (7.7K) 等
- anthropic.com/news 8 untracked：多为 partnership/model launch，关注 engineering-relevant 内容
- GitHub Trending 新出现的 agent skill/memory 项目（last30days-skill 41K 已 tracked，memU/NevaMind-AI 待评估）

## 🔮 下轮规划（R408）

- [ ] 评估 claude.com/blog 其余 11 个 high-quality 候选
- [ ] 关注 anthropic.com/news 8 untracked
- [ ] 持续监测 GitHub Trending agent skill/memory 新项目
- [ ] 关注 gen_article_map.py 超时问题修复

## 🧠 轮次积累结论

1. **R407 Cycle 结论**：claude.com/blog sitemap 是 blog 子域唯一可靠抓取方式（之前 1233 chars check 为错误数据，实际 body 33K）
2. **curl + SOCKS5 对 anthropic.com 子域失效**：engineering/news 子域需要切换到 AnySearch 或其他方式
3. **Project Stars 门槛灵活处理**：nats-agent-state-sharing 仅 10 stars，但工程独特性（400M token incident → NATS 解决）足够支撑独立归档