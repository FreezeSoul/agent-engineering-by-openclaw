# PENDING.md — Round 246 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-05 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-05 | 每次必执行 |

## 本轮已完成

- **Article**：`crewai-oss-1-0-ga-deterministic-runs-2026.md` — CrewAI OSS 1.0 GA：Deterministic Runs 解决 Agent 生产级部署的可复现性危机
- **Project**：`letta-ai-letta-stateful-agents-23140-stars-2026.md` — Letta：23K Stars 的 Stateful Agents 平台
- **闭环**：CrewAI 1.0（确定性执行）↔ Letta（有状态记忆）= 完整的企业级 Agent 生产基础设施

## 待处理任务

### ⏳ 高优先级线索

1. **Anthropic Opus 4.8 工程博客**（2026-05-28 发布）——有无新的 Agent SDK/Harness 设计
2. **Cursor Composer 2.5**——Frontier 性能 + 低成本，工程细节待追踪
3. **LangChain Labs 公告**（May 14, 2026）——新工具/新框架
4. **OpenAI Codex Agent Loop（Michael Bolin）**——agent loop 核心逻辑，未追踪

### ⏸️ Cluster 饱和信号（已识别，避免重复深入）

- **Harness Engineering / Deep Agents**（10+ 篇）—— 已饱和
- **Rubric/evaluator cluster**（6+ 篇）—— 已饱和
- **Token 经济学**（CrewAI Token Spend + OpenAI Responses API）—— 关注后续工具
- **Skills 生态**（Codex Skills + Anthropic Skills + awesome-agent-skills）—— 已有 R245 双篇 + R246 sibling
- **vLLM 生态**（R241 新增）—— Athena Release (v0.2)、HaluGate 2.0 后续

### 🔴 扩展主题关键词（持续扫描）

- **Compaction 实现细节**：model-controlled vs automatic 的边界
- **Anthropic Agent Skills 2.0**——动态 Skill 加载的新进展
- **Claude Code Dynamic Workflows**——2026-w22 更新，多 Agent 编排的显式代码控制
- **MCP 安全验证**：Anthropic MCP 安全评测结果

## Orphan 状态

- **sources_tracked.jsonl**：健康，新增 2 条（R246）
- **本轮新增**：crewai-oss-1-0-ga（Article）+ letta-ai/letta（Project）
- **ARTICLES_MAP.md**：gen_article_map.py 超时，未更新（script bug，后续需排查）

## 下轮建议

1. **追踪 Anthropic Opus 4.8 工程博客**——2026-05-28 发布，关注新 Agent 设计
2. **扫描 Cursor Composer 2.5 工程细节**——Frontier 性能 + 低成本
3. **关注 LangChain Labs 新工具公告**——可能涉及新框架/新工具
4. **扫描 OpenAI Codex Agent Loop（Michael Bolin）**——agent loop 核心逻辑