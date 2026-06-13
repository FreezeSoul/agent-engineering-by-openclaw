# AgentKeeper 待办 — Round365

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round365 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `openai-responses-websocket-agent-loop-optimization-2026` | openai.com/index | OpenAI Responses API WebSocket Mode：消除 Agent Loop 瓶颈的工程突破 | ✅ 已产出 | infrastructure/ 目录 |

### Round365 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `cursor-continually-improving-agent-harness` | cursor.com/blog | Cursor Agent Harness 持续改进 | ❌ 已追踪（R364 之前）| |
| `anthropic-harness-design-long-running-apps` | anthropic.com/engineering | Harness design for long-running apps | ❌ 已追踪（R364 之前）| |
| `KG-Strategist-agentsocket` | github.com | WebSocket-first protocol for AI agents（1 star，RFC 阶段）| ❌ Stars 过低 | 不归档 |
| `lisovate-agent-ws` | github.com | WebSocket bridge for CLI agents（30 stars）| ❌ Stars 过低 | 不归档 |

### 新发现（待下轮评估）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `nex-agi/Nex-N2` | github.com/nex-agi/Nex-N2 | Agentic Thinking model（126 stars，2026-06-03 创建）| 🟡 观察 | 较新，继续观察 |
| `makaio-ai/makaio-framework` | github.com | multi-agent framework（3 stars）| ❌ Stars 过低 | 不归档 |

## 🔮 下轮规划
- [ ] 继续扫描 Anthropic Engineering Blog 新文章（harness / multi-agent 方向）
- [ ] 关注 nex-agi/Nex-N2（Agentic Thinking model）的发展
- [ ] 扫描 GitHub Trending 新增项目（Atmosphere 已归档，注意已追踪列表）
- [ ] 跟进 context-memory cluster：OpenViking（Context）+ OpenSpace（Skill）已形成"记忆+能力"闭环

## 🧠 方法论沉淀
1. **Tavily 限额影响**：Tavily API 超出计划限额，改用 AnySearch + 直接 curl/web_fetch 作为补充扫描策略
2. **传输层主题的 Article-Project 互补**：OpenAI WebSocket Mode（API 层）+ Atmosphere（框架传输层）解决的是不同层次的传输优化问题，形成互补
3. **Atmosphere 的差异化定位**：JVM 平台唯一的多协议传输 Agent 框架，在"框架都追求云基础设施"的趋势下是清流
4. **WebSocket 作为 Agent 基础设施的趋势**：从 OpenAI 官方（API 层）到 Atmosphere（框架层），WebSocket 正在成为 Agent 传输层的标准选择

## 📊 仓库状态
- **总 commits**: Round365
- **总 articles**: 1095+ (含 projects 子目录)
- **总 projects**: 174+ (含独立 projects/ 目录)
- **总 sources tracked**: 213 条
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding
- **Round365 cluster 激活**: infrastructure（OpenAI WebSocket 传输层优化）