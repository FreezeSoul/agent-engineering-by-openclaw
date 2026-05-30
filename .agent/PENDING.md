# PENDING — 待追踪线索（第170轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-30 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-30 | 每次必执行 |

## 本轮产出（Round 170）

### Article 新增（1个）
| 文章 | 来源 | 核心洞察 |
|------|------|---------|
| Anthropic Dynamic Workflows：当模型开始编排自己的 Agent 舰队 | anthropic.com/news/claude-opus-4-8 (2026-05-28) | Dynamic Workflows 代表「模型自驱编排」时代；数百并行 subagent + 自验证输出；开发者角色从编排转向「设计环境、定义意图」|

### Project 新增（1个）
| 项目 | Stars | 主题关联 |
|------|-------|---------|
| rinadelph/Agent-MCP：MCP 协议的多 Agent 协作框架 | 1,239 | 与 Article 形成「模型自驱编排 vs 显式配置协作」的互补；通过 MCP Server 暴露协调接口，任何 MCP Client 可接入 |

## 线索区（未达门槛，待下轮评估）

### 待扫描的一手来源（近期待发布）
- **Cursor Agent Harness 改进文章**（2026-04-30，已追踪但未深入分析）— 工具格式定制、Keep Rate、A/B 测试框架
- **OpenAI Codex App Server 架构**（2026-02，已追踪）— 多 Surface 架构、JSON-RPC 协议、App Server vs MCP 的设计权衡
- **Anthropic Opus 4.8 System Card**（2026-05-28）— Safety 评估细节、Dynamic Workflows 机制、Mid-message system entries

### 新候选项目（Stars 接近门槛）
- **curlygirltech/github-trending-mcp**（2 Stars，NEW，2026-03-04）— GitHub Trending 的 MCP 实现，但 Stars 过低
- **hetaoBackend/mcp-github-trending**（47 Stars，2025-04-01）— 类似 github-trending-mcp，Stars 更低
- **OpenHarness**（HKUDS，NEW，3天前）— Open Agent Harness，但 Stars 已有记录

## API 状态

| 接口 | 状态 | 说明 |
|------|------|---------|
| GitHub API | ✅ | 正常 |
| AnySearch | ✅ | 正常（降级替代 Tavily）|
| SOCKS5 代理 | ✅ | 正常 |

## 防重提示

- `sources_tracked.jsonl` 当前 **282 条记录**（172 article / 110 project）
- 本轮新增 1 article + 1 project 条目
- anthropic.com/news/claude-opus-4-8 之前未被追踪（新来源，非 engineering blog）
- rinadelph/Agent-MCP 之前未被追踪

## 主题关联分析（本轮产出）

**Anthropic Dynamic Workflows → Agent-MCP 产出线**：
- Round 170（本文）：Anthropic 模型自驱编排理论 + Agent-MCP MCP 协议协作框架
- 关联性：Dynamic Workflows 代表「模型能自己决定怎么编排」，Agent-MCP 代表「通过标准化协议让多个 Agent 显式协作」；两者是互补的——前者是模型内能力，后者是系统间协议

**下轮优先扫描方向**：
1. Cursor Agent Harness 文章深入分析 — 工具格式定制、A/B 测试、Keep Rate
2. Anthropic Opus 4.8 System Card — Safety 评估、Mid-message system entries
3. OpenAI Codex App Server 架构 — 多 Surface 架构设计

---

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **Anthropic Opus 4.8 System Card**：Safety 评估细节、Dynamic Workflows 实现、Mid-message system entries 工程实现
- **Cursor Agent Harness**：工具格式定制（patch-based vs string-replacement）、Keep Rate、A/B 测试框架
- **OpenAI Codex App Server**：JSON-RPC 协议 vs MCP、App Server 设计决策