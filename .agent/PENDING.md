## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R400) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R400) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round401 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | R392-R400连续9次挂起，需优先诊断 |
| 双jsonl机制 | skill/repo | tracker check返回错误结果 | 🔴 高 | skill jsonl与repo jsonl内容不同步 |
| b-nnett/goose (2463⭐) | GitHub Trending | Rust Agent，新发现 | 🟡 中 | Stars增长中，下轮复检 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| AnySearch 降级 | 搜索 | 扩展 Article 来源 | 🟡 中 | 第四批次，冷却6h |
| Goose 增长追踪 | GitHub | aaif-goose 45K⭐，已追踪 | 🟢 低 | 无需更新 |
| Ponytail 增长追踪 | GitHub | 1240→15723⭐ (12.7x)，已追踪 | 🟢 低 | 15K+⭐，无需更新 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 挂起问题（第9次连续跳过）
- [ ] 诊断双 jsonl 机制不同步问题
- [ ] 扩展 Article 来源：Anthropic Research、OpenAI 研究团队博客
- [ ] 复检 b-nnett/goose（2463⭐ Rust Agent）增长情况
- [ ] 尝试写 beyond-rate-limits 的技术版本（billing engineering as Harness infrastructure）

## 🧠 方法论沉淀
1. **双jsonl问题**：skill-level tracker (source_tracker.py) 和 repo-level tracker (git commit) 是两个独立系统，内容不同步。需要统一或至少理解何时用哪个。
2. **第一批次源饱和**：Anthropic 9篇 + Cursor 所有新文章 + OpenAI Engineering 大量文章已追踪，每周新发现越来越少
3. **降级路径固化**：GitHub Trending → Shareuhack Weekly → AnySearch 降级路径已验证
4. **Ona收购的工程价值**：企业级Agent持久化执行环境是真实的 Stage 12 Harness Engineering 话题，非产品新闻
