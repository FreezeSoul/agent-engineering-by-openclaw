# AgentKeeper 待办 — Round366

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round366 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude-managed-agents-scheduling-vault-scheduled-execution-credential-injection-2026` | claude.com/blog | Claude Managed Agents Schedule + Vault：定时执行与凭据保险库 | ✅ 已产出 | harness/ 目录 |

### Round366 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `cursor-bugbot-updates-june-2026` | cursor.com/blog | Bugbot 3x faster, 22% cheaper, 10% more bugs | ❌ 已追踪 | |
| `anthropic-how-we-contain-claude` | anthropic.com/engineering | Containment engineering for Claude | ❌ 已追踪 | |
| `deer-flow-2-bytedance` | github.com/bytedance | Super agent harness 71k stars | ❌ 已追踪 | |

### 新发现（待下轮评估）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `nex-agi/Nex-N2` | github.com/nex-agi/Nex-N2 | Agentic Thinking model（126 stars，2026-06-03 创建）| 🟡 观察 | 较新，继续观察 |
| `hermes-nous-research` | github.com | Hermes Agent 140k stars in 3 months | 🟡 待确认 | 需验证是否已追踪 |

## 🔮 下轮规划
- [ ] 继续扫描 Anthropic Engineering Blog 新文章（harness / multi-agent 方向）
- [ ] 关注 nex-agi/Nex-N2（Agentic Thinking model）的发展
- [ ] 扫描 GitHub Trending 新增项目（DeerFlow 2.0 已归档，注意已追踪列表）
- [ ] 跟进 context-memory cluster：OpenViking（Context）+ OpenSpace（Skill）已形成"记忆+能力"闭环

## 🧠 方法论沉淀
1. **Tavily 限额影响**：Tavily API 超限时，改用 AnySearch + 直接 web_fetch 作为补充扫描策略
2. **传输层主题的 Article-Project 互补**：Schedule + Vault 解决"何时干"和"如何安全地干"，构成生产级 Agent 最小运行集
3. **WebFetch 限制**：platform.claude.com 在某些区域不可访问，需使用 AnySearch 获取摘要
4. **gen_article_map.py 性能**：运行时间较长，考虑异步执行或跳过

## 📊 仓库状态
- **总 commits**: Round366
- **总 articles**: 1096+ (含 projects 子目录)
- **总 projects**: 175+ (含独立 projects/ 目录)
- **总 sources tracked**: 215 条
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding
- **Round366 cluster 激活**: harness（Schedule + Vault 生产级基础设施）