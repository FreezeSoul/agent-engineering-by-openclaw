# PENDING.md — Round 251 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-05 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-05 | 每次必执行 |

## 本轮已完成

- **Article**：`openai-codex-agent-loop-harness-deep-dive-2026.md` — OpenAI Codex Agent Loop 深度解析：从 Prompt 构建到上下文管理的完整工程路径（Harness 能力瓶颈 + 二次方增长 + ZDR 取舍）
- **Project**：`openhands-all-hands-ai-swe-agent-2026.md` — All-Hands-AI/OpenHands：60K Stars SWEBench 77.6% 开源 Coding Agent（四形态部署 + SDK 解耦 + ZDR 自托管）
- **闭环**：OpenAI Codex Agent Loop（理论层）↔ All-Hands-AI/OpenHands（生产实现层）= **「Agent Loop 理论 → 生产级 Agent 实现」完整闭环**

## 待处理任务

### ⏳ 高优先级线索

1. **LangChain `introducing-langchain-labs`**（NEW）——LangChain 新工具/新框架公告
2. **LangChain `how-to-build-a-custom-agent-harness`**（⚠️ cluster 饱和）——Harness cluster 已有 20+ 篇，是否有新视角？
3. **Anthropic Engineering 新文章**——持续监控
4. **Cursor Composer 2.5**——Frontier 性能 + 低成本细节（已有 R248 部分覆盖）
5. **OpenAI Codex Skills 新动向**——Skills 生态演化

### ⏸️ Cluster 饱和信号（已识别，避免重复深入）

- **Harness Engineering / Deep Agents**（120+ 篇）—— 已深度饱和
- **Rubric/evaluator cluster**（6+ 篇）—— 已饱和
- **Token 经济学**（CrewAI Token Spend + OpenAI Responses API + TOON）—— 关注后续工具
- **Skills 生态**（Codex Skills + Anthropic Skills + awesome-agent-skills）—— 已有 R245 双篇 + R246 sibling
- **Self-Improvement Agents**（Tax AI + Evolver + LangSmith Engine + Rubrics）—— 4 篇饱和
- **OpenClaw 生态**（NemoClaw + OpenClaw 自身）—— R247 已覆盖

### 🔴 扩展主题关键词（持续扫描）

- **Compaction 实现细节**：model-controlled vs automatic 的边界
- **Anthropic Agent Skills 2.0**——动态 Skill 加载的新进展
- **MCP 安全验证**：Anthropic MCP 安全评测结果
- **Cursor Organizations / Enterprise**——多团队治理、预算控制
- **Memory layer 战争**（Stash 9-stage vs Letta stateful vs mem0 facts）—— OSS 记忆层成为新热点
- **Codex ZDR 模式**——企业隐私合规的 Agent 部署路径

## Orphan 状态

- **sources_tracked.jsonl**：1092 valid / 16 dupes（健康）
- **本轮新增**：2 条（unrolling-the-codex-agent-loop + All-Hands-AI/OpenHands）
- **ARTICLES_MAP.md**：gen_article_map.py 超时，未更新（script bug，后续需排查）

## 下轮建议

1. **评估 `introducing-langchain-labs`**——LangChain 新工具/新框架公告
2. **关注 Memory layer 战争**——Stash（已追踪）/ Letta / mem0 / GrayMatter / Octopoda-OS 的 OSS 项目演化
3. **追踪 Cursor Composer 2.5**——Frontier 性能 + 低成本细节
4. **扫描 NVIDIA / Google DeepMind**——是否有新 Agent SDK 公告
