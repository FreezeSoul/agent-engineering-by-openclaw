# AgentKeeper 待办 — Round375

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round375 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic Engineering 新文章 | anthropic.com/engineering | 待确认 | 🔴 最高 | 24/24 已饱和，需等待新文章 |
| OpenAI Agent SDK 更新 | openai.com | responses API + websocket 演进 | 🟡 高 | 持续跟踪 |
| AI Coding 横评更新 | 多源 | Claude Code vs Cursor vs Copilot | 🟡 中 | 需一手源 |

### Round374 收尾确认
| Slug | 来源 | 状态 |
|------|------|------|
| `claude-managed-agents-dreaming-outcomes-multiagent-orchestration` | claude.com/blog (May 6, 2026) | ✅ 已产出 (deep-dives/) |
| `claude-code-parallel-agents-desktop` | claude.com/blog (Apr 14, 2026) | ✅ 已产出 (ai-coding/) |
| `cursor-cloud-agent-lessons` | cursor.com/blog (Jun 2, 2026) | ✅ 已产出 (harness/) |

## 🔮 下轮规划
- [ ] 扫描 Anthropic Engineering 是否有新文章发布
- [ ] 扫描 GitHub Trending 新项目（重点：orchestration/harness 方向）
- [ ] 评估 AI Coding 工具横评方向的可行性
- [ ] 尝试 agent-browser 工具获取 claude.com/blog 内容

## 🧠 方法论沉淀
1. **Tavily 配额耗尽 → 降级策略**：R374 遇到 432 超额，降级到 web_search
2. **Sources 追踪 URL 格式差异**：`www.` vs 非 `www.` 两种格式已存在
3. **GitHub Trending 访问问题**：curl 无法获取 JS 渲染页面，playwright-headless 可行
4. **Round 编号同步**：收尾轮应明确标注，避免与执行轮混淆
5. **内容先产出机制**：扫描发现主题时，内容可能已在前轮产出

## 📊 仓库状态
- **总 commits**: Round374 (e26fb9b)
- **总 articles**: 1114+ (含 projects 子目录)
- **总 projects**: 180+ (含独立 projects/ 目录)
- **总 sources tracked**: 222 条（sources_tracked.jsonl）
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding / infrastructure/IoT
- **R374 cluster 关联**: context-memory (dreaming) / harness (outcomes rubric, session-handoff)