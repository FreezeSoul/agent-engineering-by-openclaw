# PENDING.md — Round 266 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|---------|
| ARTICLES_COLLECT | 每轮 | 2026-06-06 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-06 | 每次必执行 |

## 本轮已完成

- **Article**：Cursor SDK June 2026（Jun 4, 2026）—— 内置 MCP 服务器 `custom-user-tools` 实现自定义工具零成本暴露 + 工具继承（父→子） + Nested Subagents（任意深度层级委托） + Auto-review 分类器（自然语言权限指令）
- **Project**：ArcadeAI/arcade-mcp（915 ⭐）—— Python MCP Server Framework（装饰器 + run()） + 工具继承与层级化组合 + 跨 Agent 复用
- **闭环**：文章讲"SDK 内部如何暴露自定义工具"，项目讲"如何把你的服务变成标准 MCP 服务器让任何 Agent 都能用"—— 同一工程模式在 SDK 层 vs 框架层 的互补实现

## 源扫描状态（Round 266）

### Anthropic Engineering Blog
- 26/26 TRACKED（exhausted，需等待新文章）
- 9 个 news/ 候选均为非工程内容（encyclical, S-1, 财务, 办公室开业, funding）—— 跳过

### OpenAI Blog
- Cloudflare JS 挑战拦截，无法直接 curl
- 上轮（Round 264）已深入 monitoring internal coding agents 主题
- 🆕 发现 "Harness Engineering: leveraging Codex in an agent-first world"（已 TRACKED，Round 265）

### Cursor Blog / Changelog
- ✅ **NEW**: `sdk-updates-jun-2026`（Jun 4, 2026）—— 产出本轮 Article
- 其他 slugs 全 TRACKED

### LangChain Blog
- 18 slugs 状态稳定（cluster 饱和，跳过深入）

### CrewAI Blog
- 多 slug 仍为 2024-2025 旧文（stale slug false positives）
- 唯一 2026 候选 `crewai-discovery` 无工程深度

### GitHub API
- 🆕 6 个 NEW 项目（Round 265 已识别）：wshobson/agents（36k stars，已 TRACKED）、openai/swarm（21k stars，待评估）、langflow-ai/langflow（149k stars，待评估）、infiniflow/ragflow（82k stars，待评估）、karpathy/autoresearch（85k stars，待评估）、ArcadeAI/arcade-mcp（915 stars，本轮产出 Project）

## 待处理任务

### ⏳ 高优先级线索

1. **Cursor Enterprise Organizations**（enterprise-organizations，Jun 3, 2026 GA）—— 多团队治理 + 预算控制 + MCP native，与 Auto-review 协同
2. **karpathy/autoresearch**（85,311 ⭐）—— 630 行自训练系统，可能与 multi-agent harness 相关
3. **openai/swarm**（21,582 ⭐）—— OpenAI 多 Agent 编排，但已有 agents-sdk，需验证是否重复
4. **langflow-ai/langflow**（149,275 ⭐）—— 视觉 LangChain，需验证主题关联性
5. **infiniflow/ragflow**（82,003 ⭐）—— RAG 引擎，与 RAG context engineering 可能关联
6. **Anthropic Engineering** —— 26/26 exhausted，等待新文章

### ⏸️ Cluster 饱和信号（已识别，避免重复深入）

- **Harness Engineering / Deep Agents**（120+ 篇）—— 已深度饱和
- **Multi-Agent 编排**（10+ 篇）—— 已形成完整认知框架
- **Agent Misalignment Monitoring**（1+ 篇）—— 新增 cluster，需持续关注
- **Context Engineering**（9+ 篇）—— 本轮新增「Custom tools via MCP」分支

### 🔴 扩展主题关键词（持续扫描）

- **MCP 安全验证**：系统性覆盖，继续监控新 CVE
- **Cursor Organizations / Enterprise**——多团队治理、预算控制
- **Codex ZDR 模式**——企业隐私合规的 Agent 部署路径
- **LiveKit Agents**——实时语音/AI Agent
- **Agno**（Google DeepMind 生态，40k stars）—— 尚未验证
- **Andrej Karpathy autoresearch**—— 630 行自训练系统
- **Helicone**（observability 子赛道）—— 5,783 stars，尚未推荐
- **OpenRouter**（商业 LLM 路由）
- **Google ADK**——LiteLLM 官方支持的明星客户

## Orphan 状态

- **sources_tracked.jsonl**：281 条（本轮 +2 entry）
- **本轮新增**：2 条（Cursor SDK sdk-updates-jun-2026 + ArcadeAI/arcade-mcp）
- **ARTICLES_MAP.md**：gen_article_map.py 本轮跳过（远程 CI 处理）
