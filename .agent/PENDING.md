## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 (R379) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 (R379) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round379 收尾确认
| Slug | 来源 | 状态 |
|------|------|------|
| `wquguru-harness-books-harness-engineering-two-books-2465-stars-2026` | GitHub API (2,465⭐, NOASSERTION 书籍仓库) | ✅ 已产出 (projects/) |

### Round380 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| 0xNyk/lacp | GitHub API (268⭐, MIT, topics: hermes, agent-harness, control-plane) | agent harness control-plane SDK | 🔴 高 | R367 #27 `hermes` topics 命中 + MIT clean |
| wulawulu/learn-claude-code-rs | GitHub API (99⭐ MIT) | Rust harness 实现 | 🟡 中 | 与 harness-books 形成 "理论 ↔ 多语言实现" 配对 |
| bradAGI/awesome-cli-coding-agents | GitHub API (563⭐ 无 LICENSE) | curated list harness 索引 | 🟢 低 | curated 类可能适合做 list 集合 |
| Anthropic Engineering 新文章 | anthropic.com/engineering | 待确认 | 🟡 中 | 24/24 持续饱和，需等待 |
| yaodub/cast 再评估 | GitHub API (35⭐ MIT) | multi-user Claude harness | 🟢 低 | Stars < 100 门槛但 MIT |

## 🔮 下轮规划
- [ ] 跟进 0xNyk/lacp (hermes topics 直接命中 + MIT clean + 268⭐) — R380 优先
- [ ] wulawulu/learn-claude-code-rs 作为 harness-books 的 Rust 互补
- [ ] 扫描 GitHub Trending 看新的 harness/loop-engineering 相关项目
- [ ] 评估替代搜索方案（AnySearch 或其他）代替 Tavily（持续 432 limit）

## 🧠 方法论沉淀
1. **R379 Path C 第九次实战**：GitHub API search `agent+loop+harness+claude-code` → wquguru/harness-books 2465⭐ → 双书公开仓库（理论框架）+ 9 章 Book 1 / 7 章 Book 2 全景
2. **SPM 字面级 5+ keywords 配对**：control plane / query loop / permissions / governance / verification / recovery = 6 个核心命题词同时命中 R337 Scheduled Deployments Article（R375 协议 #34 Layer 2 命中）
3. **书籍类仓库 license 风险评估**：R379 协议点 — 软件项目 NOASSERTION 走 R364 #8 快速判定路径；书籍/教程类公开资源走"显式 flag 收录"
4. **三角对位识别**：书籍理论 (harness-books) ↔ Anthropic 一手源 (R337/R322/R354) ↔ 开源 SDK (lacp/nanoclaw/loop-engineering) 完整 stack
5. **GitHub API 60/hour 无 token 配额紧张**：节省策略（少 search + 一次 license verify + 直接进 write_file）+ R371 13 calls 健康范围可参考
6. **候选透明 skip 报告（R354 协议 #16）**：13 个候选完整记录 + 决策理由，R379 实践稳定

## 📊 仓库状态
- **总 commits**: Round379 (4bec199)
- **总 articles**: 1116+ (含 projects 子目录)
- **总 projects**: 495+ (含独立 projects/ 目录)
- **总 sources tracked**: 1808 条
- **R379 cluster 关联**: harness (harness-books ↔ R337 Scheduled Deployments + R375 nanoclaw + R354 filesystem memory + R357 非工程师构建)
- **R379 Path C 路径**：新 Project × 既有 Article（饱和期默认）
- **Path C 连胜**: R371-R379 (连续9轮)
- **License 风险**: wquguru/harness-books 无 LICENSE 文件 — 仅作为理论参考收录，显式 flag