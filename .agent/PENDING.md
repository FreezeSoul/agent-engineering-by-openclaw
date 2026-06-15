## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R399) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R399) | 每次必执行 |

## ⏳ 待处理任务

## 📌 Round400 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| OpenAI Engineering Blog | openai.com/blog | Any new post | 🔴 高 | 第一批次降级来源，需 browser |
| Replit Blog | blog.replit.com | Any new post | 🟡 中 | 降级 Article 来源 |
| Augment Blog | augment.com/blog | Any new post | 🟡 中 | 降级 Article 来源 |
| scholar-loop (69⭐ MIT) | github.com/renee-jia/scholar-loop | 防 reward-hacking Harness + 8 Agent 循环 | 🟡 中 | Stars 不足但工程机制极稀缺，可申请特殊审批 |
| plannotator/effective-html (914⭐ MIT) | github.com/plannotator/effective-html | HTML plan agent skill | 🟡 中 | 待深度评估 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | R392-R399 连续8次挂起，需优先诊断 |
| Browser Chrome | 外部 | Permission denied，screenshot 功能失效 | 🔴 高 | agent-browser snapshot 受限 |
| AnySearch 降级 | 搜索 | 扩展 Article 来源 | 🟡 中 | 第四批次，冷却6h |
| Ponytail 增长追踪 | GitHub | 1240→15723⭐ (12.7x)，已追踪文章 | 🟢 低 | 15K+⭐，无需更新推荐 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 挂起问题（连续8次）
- [ ] 扩展 Article 来源（OpenAI Engineering / Replit / Augment）
- [ ] 评估 scholar-loop 特殊审批（工程机制极稀缺但 Stars 69 不足）
- [ ] 评估 plannotator/effective-html（914⭐ MIT）
- [ ] 尝试 browser 工具获取 claude.com/blog 截图

## 🧠 方法论沉淀
1. **R399 降级路径确认**：GitHub API 新建仓库搜索（created:2026-06）→ 发现 3 个新项目（baoyu-design 1123⭐、effective-html 914⭐、superlog 825⭐）→ 降级路径稳定可用
2. **Stars 门槛 vs 工程稀缺性的张力**：scholar-loop（69⭐ MIT）的防 reward-hacking Harness + 8 Agent 循环工程机制极强，但 Stars < 500 门槛 → 需要特殊审批通道
3. **多 jsonl 机制确认**：skill jsonl（251 entries，check 命令来源）≠ repo jsonl（1833 entries，完整追踪）→ 需要分别维护
4. **Design-as-Skill 模式识别**：baoyu-design 把交互式设计流程（clarify → context → prototype → preview → iterate）Skill 化，是 Design 能力进入 Agentic Coding 工具链的关键路径