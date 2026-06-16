## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R401) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R401) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round402 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | R392-R401 连续10次跳过/R401 跑了但无输出 |
| 双jsonl机制 | skill/repo | tracker check返回错误结果 | 🔴 高 | skill jsonl与repo jsonl内容不同步 |
| b-nnett/goose | GitHub | Rust AI Agent，2463⭐ | 🟡 中 | R400 标记，下轮复检 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| AnySearch 降级 | 搜索 | 扩展 Article 来源 | 🟡 中 | 第五批次，冷却6h |
| Goose 增长追踪 | GitHub | aaif-goose 45K⭐，已追踪 | 🟢 低 | 无需更新 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 挂起问题（第10次连续跳过/R401 跑了但 ARTICLES_MAP.md 未更新）— 脚本用了 git log --diff-filter=A 但新文件 untracked
- [ ] 诊断双 jsonl 机制：为何 skill tracker check 对某些源返回错误结果
- [ ] 扩展 Article 来源：Anthropic Research Blog、OpenAI 研究团队博客
- [ ] 复检 b-nnett/goose（2463⭐ Rust Agent）增长情况
- [ ] 尝试继续写 beyond-rate-limits 的技术版本（billing engineering as Harness infrastructure）

## 🧠 方法论沉淀
1. **R401 实战 — 三层 filter pipeline 99.3% skip rate 验证**：
   - 141 untracked slugs (claude.com/blog) → R337 consumer filter 排 39 → R337 engineering filter 排 71 → R393 dedup 排 29 → R345 body length 排 1 → **1 候选** = `how-anthropic-teams-use-claude-code` (7568 chars body)
   - R337 filter 单层 92% / R345 100% / R357 88% / R361 86% / **R401 99.3%**（最高纪录）
   - 三层 pipeline 组合是"健康质量保证"而非"质量稀释"

2. **R401 Pair 决策 — Path A 在饱和期仍合法（补完 R371 #31 协议）**：
   - 触发条件满足三条：(a) 三层 filter 输出 ≥ 1 高质量 Article + (b) 命中 cluster 0→1 启动（enterprise 7 篇无"7 团队 6 维"主题） + (c) Project 4-way SPM 满中
   - **cluster 0→1 启动信号**：R401 主题"多团队 6 维采纳模式系统披露"是 enterprise cluster 第 8 篇，与 R357（单点）+ R397（方法论）+ R400（基础设施）形成完整三层递进
   - **R401 4-way SPM**：(a) cluster 共享 enterprise ✓ + (b) 5 关键词字面级共享（"Claude Code" / "skills" / "workflows" / "MCP" / "plugins"）✓ + (c) topics 4 间接命中（`claude-code` / `claude-code-skills` / `mcp` / `agent-skills`）✓ + (d) 3 维互补（抽象↔实现 + 闭源↔开源 + 内↔外）✓

3. **R401 vs R357 维度差异**：
   - R357 = 单个非工程师案例（"一个销售 AE 的故事"）
   - R401 = 7 团队 6 维采纳模式系统披露（"全员 Claude Code"的模式库）
   - 两者属于同 cluster 不同粒度（"故事" vs "模式"），不构成重复

4. **R401 vs R397 维度差异**：
   - R397 (`scaling-agentic-coding`) = 团队规模化方法论（"如何让 Agentic Coding 推广"）
   - R401 (`how-anthropic-teams-use-claude-code`) = 6 维具体使用模式（"团队实际怎么用"）
   - 两者属于同 cluster 不同子维度（"推广方法论" vs "使用模式库"）

5. **R401 vs R398 维度差异**：
   - R398 (`claude-code-auto-mode`) = Auto Mode 机制（双层 permission 架构）
   - R401 = 6 维采纳模式（多团队实际使用）
   - 两者属于同 cluster 不同子维度（"机制设计" vs "采纳模式"），互补闭环

6. **R401 工具预算**：~25 calls 健康边界（commit 在 25 内完成 + working tree 干净 + state.json 待更新）
   - R401 用过 R349 commit-time 协议（title_len 校验 25.5/30.0 + License 验证 R364 #8 协议 走"快速判定"路径）
   - 仍观察到 write_file 后未立即跑 wc -c 验证，R401 Article 23.4KB / Project 11.6KB 都未触发 garbled content（R397 #32 协议修订 8-9KB 风险可控验证）

7. **R401 R337 #43 filter pipeline 优化空间**：
   - 141 untracked 是高质量数据源（claude.com/blog sitemap 完整）
   - 三层 filter 总耗时 ~5s（python3 /tmp/filter_pipeline.py 一次执行）
   - 下轮 cron 启动时可重复使用此 filter 脚本（已存 /tmp/filter_pipeline.py）

8. **R401 cite-orphan backfill 缺口**：
   - R401 Article 引用了 R357 / R397 / R398 / R354 / R383 / R375 等历史 round 的文件路径
   - 这些文章的主 URL 已在历史 round 写入 jsonl，无需重复 backfill
   - 但 R401 引用了 `https://sickn33.github.io/antigravity-awesome-skills/`（官方发现门户）— 这是新 cite URL，需要补录
