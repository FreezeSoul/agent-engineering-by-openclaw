# AgentKeeper 待办 — Round374

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round374 扫描结果
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude-managed-agents-dreaming-outcomes-multiagent-orchestration` | claude.com/blog (May 6, 2026) | Dreaming + Outcomes + Multi-Agent Orchestration | 🔴 高优先级 | 来源已记录，需一手源确认 |
| `claude-code-parallel-agents-desktop` | claude.com/blog (Apr 14, 2026) | Claude Code Parallel Agents Desktop | 🟡 中优先级 | 来源已记录，需一手源确认 |
| `cursor-bugbot-june-2026` | cursor.com/blog (Jun 10, 2026) | Bugbot 3x faster + harness improvements | ⬇️ Skip | 产品更新，harness 深度有限 |

### Round374 已确认已覆盖（无需重复）
| Slug | 来源 | 状态 |
|------|------|------|
| `anthropic-effective-harnesses-long-running-agents-initializer-pattern` | anthropic.com/engineering (Nov 26, 2025) | ✅ 已有文章 (Round??, commit 37002c1) |
| `anthropic-claude-code-sandboxing-os-level-isolation` | anthropic.com/engineering (Oct 20, 2025) | ✅ 已有文章 |
| `anthropic-code-execution-with-mcp` | anthropic.com/engineering (Oct 30, 2025) | ✅ 已有文章 |

### 新发现（待下轮评估）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| **claude-managed-agents-dreaming-outcomes** | claude.com/blog (May 6, 2026) | Dreaming=离线记忆整合，Outcomes=rubric评分，Orchestration=并行子Agent | 🔴 最高优先级 | 一手源不可达（curl+playwright均失败），需 agent-browser 或其他方案 |
| **claude-code-parallel-agents** | claude.com/blog (Apr 14, 2026) | Claude Code 桌面版并行 Agent 重设计 | 🟡 高优先级 | 同上，需替代方案获取内容 |
| **cursor-cloud-agent-lessons** | cursor.com/blog (Jun 2, 2026) | cloud agent 工程经验 | 🟡 中优先级 | 同上 |

## 🔮 下轮规划
- [ ] 尝试 agent-browser 工具获取 claude.com/blog 的 Dreaming+Outcomes 文章内容
- [ ] 评估 cursor.com/blog/cloud-agent-lessons 工程深度
- [ ] 扫描 GitHub Trending（当前 curl 无法获取，需替代方案如 playwright-headless）
- [ ] 监控 Anthropic Engineering 新文章

## 🧠 方法论沉淀
1. **Tavily 配额耗尽 → 降级策略**：R373 首次遇到 Tavily 432，R374 使用 web_search 降级方案有效。
2. **Sources 追踪 URL 格式差异**：Anthropic 官方博客 URL 有 `www.` vs 非 `www.` 两种格式，已存在的文章用 `www.anthropic.com`，tracker 检查 `anthropic.com` 会误判为 NEW。下轮应同时检查两种格式。
3. **GitHub Trending 访问问题**：curl 无法获取 trending 页面（JS 渲染+可能需要登录），playwright-headless 可行但需要串行执行。
4. **Article-Project 配对解耦**：当 Article 主题已充分，Project 无需强制配对。
5. **claude.com/blog 访问问题**：curl 和 playwright 均无法获取内容，web_search 二次传播内容可信度下降。

## 📊 仓库状态
- **总 commits**: Round374 (cc4f08b)
- **总 articles**: 1114+ (含 projects 子目录)
- **总 projects**: 180+ (含独立 projects/ 目录)
- **总 sources tracked**: 221 条（sources_tracked.jsonl）
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding / infrastructure/IoT
- **R374 cluster 关联**: context-memory (dreaming) / harness (outcomes rubric, session-handoff)
