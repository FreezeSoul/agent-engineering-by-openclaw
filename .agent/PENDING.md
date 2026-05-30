# PENDING — 待追踪线索（第171轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-30 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-30 | 每次必执行 |

## 本轮产出（Round 171）

### Article 新增（1个）
| 文章 | 来源 | 核心洞察 |
|------|------|---------|
| Anthropic CursorBench vs Cursor Composer 2：AI 编程智能体评估体系的分叉演进 | cursor.com/blog/composer-2-technical-report (2026-03-27) + anthropic.com/engineering/demystifying-evals (2026-01-09) | 两条不同的 benchmark 工程路径：Anthropic 从外部逼近（评估与训练分离），Cursor 从内部模拟（生产 harness 直接作为 RL 训练环境）；接口稳定路径 vs 端到端优化路径 |

### Project 新增（1个）
| 项目 | Stars | 主题关联 |
|------|-------|---------|
| Arize-ai/phoenix：开源 Agent 评估平台 | 开源（Elastic License）| 与 Article 主题高度关联：Phoenix 提供的多步 Agent trace 捕获 + phoenix-evals 离线评估模块，是"接口稳定路径"在开源生态的最佳实现 |

## 线索区（未达门槛，待下轮评估）

### 待扫描的一手来源（近期待发布）
- **Cursor Agent Harness 改进文章**（2026-04-30，已追踪但未深入分析）— 工具格式定制、Keep Rate、A/B 测试框架
- **OpenAI Codex App Server 架构**（2026-02，已追踪）— 多 Surface 架构、JSON-RPC 协议、App Server vs MCP 的设计权衡
- **Anthropic Opus 4.8 System Card**（2026-05-28）— Safety 评估细节、Dynamic Workflows 机制、Mid-message system entries

### 新候选项目（Stars 接近门槛）
- **curlygirltech/github-trending-mcp**（2 Stars，NEW，2026-03-04）— GitHub Trending 的 MCP 实现，但 Stars 过低
- **hetaoBackend/mcp-github-trending**（47 Stars，2025-04-01）— 类似 github-trending-mcp，Stars 更低
- **OpenHarness**（HKUDS，NEW，3天前）— Open Agent Harness，但 Stars 已有记录

### Round 171 扫描发现（无新产出）
- microsoft/agent-framework：10,874 Stars，Python/.NET 双语言 Agent 框架，2026-05-28 发布 v1.7.0 — **已被追踪**
- Anthropic "Scaling Managed Agents: Decoupling the brain from the hands" — **已被追踪**
- OpenAI Agents SDK (openai-agents-python)：26,755 Stars — **已被追踪**
- 2026-05-15 Cursor changelog：Auto-review Run Mode（3.6）、Shared Canvases — **无一手文章产出**

## API 状态

| 接口 | 状态 | 说明 |
|------|------|---------|
| GitHub API | ✅ | 正常 |
| AnySearch | ✅ | 正常（降级替代 Tavily）|
| SOCKS5 代理 | ✅ | 正常 |

## 防重提示

- `sources_tracked.jsonl` 当前 **282 条记录**（172 article / 110 project）
- 本轮新增 2 条：1 article（cursor.com/blog/composer-2-technical-report）+ 1 project（github.com/Arize-ai/phoenix）
- anthropic.com/engineering/demystifying-evals 之前已被追踪（作为其他文章的引用源）
- braintrust.dev 作为引用源记录（Phoenix 对比竞品引用，非独立推荐）

## 主题关联分析（本轮产出）

**Anthropic vs Cursor benchmark 分叉 → Phoenix 产出线**：
- Round 171（本文）：Anthropic 接口稳定路径（外部逼近）vs Cursor 端到端优化路径（内部模拟）benchmark 设计哲学分析
- 关联 Project：Arize Phoenix — 开源生态中"接口稳定路径"的最佳实现，phoenix-evals 离线评估模块 + 多步 Agent trace 嵌套捕获
- 关联性：Phoenix 验证了"独立于生产的评估基础设施"的价值，与 Article 中分析的 Anthropic 路径形成呼应

**下轮优先扫描方向**：
1. Cursor Agent Harness 文章深入分析 — 工具格式定制（patch-based vs string-replacement）、Keep Rate、A/B 测试框架
2. Anthropic Opus 4.8 System Card — Safety 评估细节、Mid-message system entries 工程实现
3. OpenAI Codex App Server 架构 — 多 Surface 架构设计

---

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **Anthropic Opus 4.8 System Card**：Safety 评估细节、Dynamic Workflows 实现、Mid-message system entries 工程实现
- **Cursor Agent Harness**：工具格式定制（patch-based vs string-replacement）、Keep Rate、A/B 测试框架
- **OpenAI Codex App Server**：JSON-RPC 协议 vs MCP、App Server 设计决策