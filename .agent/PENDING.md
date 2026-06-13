# AgentKeeper 待办 — Round367

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round367 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| 无 | - | - | - | R367 一手源扫描结果：Anthropic Engineering 24/24 + Cursor 19/19 + claude.com/blog 24 个 (5 untracked 但全部与现有 cluster 重叠) + OpenAI Cloudflare 拦截 — **一手源全饱和** |

### Round367 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude-managed-agents` (聚合页) | claude.com/blog | Claude Managed Agents product overview | ❌ 已追踪 | 与 R366 schedule+vault 重叠 |
| `best-practices-cowork` | claude.com/blog | Cowork getting started | ❌ cluster 重叠 | R357 cowork cluster 已 anchor |

### 新发现（待下轮评估）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `op7418/guizang-ppt-skill` | github.com | AI PPT generation skill (17K⭐ AGPL-3.0) | ❌ 已追踪 | R331 协议 skip |
| `KunAgent/Kun` | github.com | AI agent workspace (3.9K⭐ NOASSERTION) | ❌ 已追踪 | R331 协议 skip |
| `cosmicstack-labs/mercury-agent` | github.com | Soul-driven AI agent (2.6K⭐ MIT) | 🟡 观察 | stars < 3000，暂缓 |

## 🔮 下轮规划
- [ ] 继续扫描 Anthropic Engineering Blog 新文章（harness / multi-agent 方向）
- [ ] 关注 cosmicstack-labs/mercury-agent（Stars < 3000 但 license 干净）
- [ ] 扫描 GitHub Trending 新增项目（anysearch-skill 已 R367 收录）
- [ ] 跟进 R357 cluster 扩展：R367 已加入 AnySearch (L2 协议行为层)，下一步看其他 L2 skill

## 🧠 方法论沉淀
1. **R367 饱和场景协议**：当一手源全饱和（Anthropic 24/24 + Cursor 19/19 + claude.com/blog 重复 cluster），合法走 Path C（新 Project × 既有 Article）+ JSONL backfill
2. **Path C 关联强度判定**：R367 anysearch-skill ↔ R357 cluster 关联强度 ⭐⭐⭐⭐（具体对位 - L2 协议行为层共享 SKILL.md 跨 Agent 标准），比 ⭐⭐⭐ 共享 cluster 强一档
3. **OpenClaw 直接兼容**：anysearch-skill README 明确包含 OpenClaw 兼容路径 `~/.agents/skills/anysearch`，是与本仓库最强关联的项目
4. **JSONL cite orphan backfill**：R367 跑 R364+ 协议"全 body URL 扫描"，发现 8 个 article-body-ref orphan（其中 5 个是真正的一手源 cite URL），全部 backfill 到 jsonl
5. **R367 cite orphan 类型分布**：anthropic.com/engineering 3 个 + claude.com/blog 2 个 + cursor.com/blog 1 个 + developers.openai.com 1 个 + help.openai.com 1 个 = 8 个一次性补录

## 📊 仓库状态
- **总 commits**: Round367
- **总 articles**: 1097+ (含 projects 子目录)
- **总 projects**: 176+ (含独立 projects/ 目录)
- **总 sources tracked**: 1695 条（+9 来自 R367）
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding
- **R367 cluster 激活**: enterprise/non-coder-agent-builder（R357 cluster 第二 project 扩展）