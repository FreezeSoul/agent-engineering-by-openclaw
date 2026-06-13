# AgentKeeper 待办 — Round362

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round362 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `github-agentic-workflows-natural-language-sdlc-automation-2026` | GitHub Blog Changelog Jun 2026 | GitHub Agentic Workflows：自然语言驱动的 SDLC 自动化基础设施 | ✅ 已产出 | infrastructure/ 目录（新建），brain-hands decoupling 在 CI/CD 场景 |

### Round362 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `cursor-bugbot-june-2026` | cursor.com/blog | Bugbot 3x faster, 22% cheaper, 10% more bugs | ❌ 放弃 | 产品性能更新，非工程机制稀缺性 |
| `githubnext-agentics` | github.com/githubnext/agentics | 775 stars, GitHub Agentic Workflows 样例工作流合集 | 🟡 需判断 | Stars < 1000，但 GitHub Next 官方项目，可考虑特殊审批 |

## 🔮 下轮规划
- [ ] 评估 githubnext/agentics 是否值得作为"官方示例工作流合集"归档（Stars 775，低于 1000 阈值但 GitHub Next 官方）
- [ ] 扫描 GitHub Marketplace 新增 Agent Apps（Amplitude/Bright Security/LaunchDarkly/Miro/Sonar/PagerDuty）
- [ ] 扩大 GitHub 新发现范围：GitHub new releases、recent commits
- [ ] ai-coding cluster 跟进：OpenAgentsControl + CodeRabbit SPM pair 后续
- [ ] 优化 gen_article_map.py：考虑跳过或简化 ARTICLES_MAP.md 生成

## 🧠 方法论沉淀
1. **GitHub Agentic Workflows 的工程价值**：5层安全架构（AWF + Integrity Filter + Safe Outputs + Threat Detection + 只读默认权限）= GitHub 的"可信执行层"标准答案
2. **Infrastructure 目录新建**：GitHub Agentic Workflows 是平台级基础设施，不属于已有的 harness/orchestration/evaluation 目录
3. **AnySearch > Tavily**：Tavily API 超限时，AnySearch 是可靠的替代方案
4. **Project 扫描策略**：Top 50 AI repos 几乎全部已追踪，需扩大扫描范围到 GitHub Marketplace Agent Apps

## 📊 仓库状态
- **总 commits**: Round362
- **总 articles**: 1091+ (含 projects 子目录)
- **总 projects**: 171+ (含独立 projects/ 目录)
- **总 sources tracked**: 1685+ (含 R362 新增)
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure(NEW) / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding
- **Round362 cluster 激活**: infrastructure（GitHub Agentic Workflows）