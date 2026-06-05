# PENDING.md — Round 249 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-05 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-05 | 每次必执行 |

## 本轮已完成

- **Article**：`langchain-harmonic-scout-deep-agents-4x-retention-2026.md` — Harmonic Scout V2：从「刚性 subgraph」到「Deep Agents + 共享文件系统」，4 倍留存不是设计目标而是结构副产品
- **Project**：`alash3al-stash-9-stage-memory-consolidation-mcp-2026.md` — alash3al/stash：MCP 上的 OSS 持久化记忆，9 阶段 consolidation
- **闭环**：LangSmith Deployment（商业 durable thread + observability）↔ alash3al/stash（OSS 9 阶段 consolidation）= **Pattern 8（商业 vs OSS 替代路径）** 在「Agent 持久化记忆」上的两条路径

## 待处理任务

### ⏳ 高优先级线索

1. **Anthropic Opus 4.8 Dynamic Workflows**（2026-05-28 发布）——已有 R243 覆盖，关注后续工程化
2. **Cursor Composer 2.5**——Frontier 性能 + 低成本
3. **LangChain Labs 公告**（May 14, 2026）——interrupt-2026-overview / introducing-langchain-labs 待评估
4. **OpenAI Codex Agent Loop（Michael Bolin）**——agent loop 核心逻辑，已追踪
5. **NEW 候选 LangChain slugs**（4 个未追踪）：
   - `financial-ai-that-investigates-macro-trends-eu-economic-analysis-with-you-com-and-langchain`
   - `how-to-build-a-custom-agent-harness`（**cluster 饱和**：harness 20+ 篇）
   - `how-we-built-langsmith-engine-our-agent-for-improving-agents`（**cluster 饱和**：self-improvement 4 篇）
   - `introducing-rubrics-for-deepagents`（**cluster 饱和**：Rubric 2 篇）
   - `introducing-langchain-labs`（待评估）
   - `may-2026-langchain-newsletter`（newsletter 低价值）
6. **NEW GitHub 项目候选**（4 个未追踪）：
   - `ClaudioDrews/memory-os`（829 stars，Hermes Agent 专用，命名冲突风险）
   - `2aronS/Duel-Agents`（713 stars，商业 duelagents.com 配套，OSS 度低）
   - `nv-tlabs/Gamma-World`（586 stars，NVIDIA 论文，sim 方向）
   - `joeynyc/hermes-hudui`（1626 stars，Hermes Agent 监控）
   - `alash3al/stash`（710 stars，**R249 已深入**）
   - `JuliusBrussee/cavemem`（497 stars，cross-agent 压缩记忆）
   - `angelnicolasc/graymatter`（386 stars）
   - `RyjoxTechnologies/Octopoda-OS`（340 stars，记忆 + loop detection）

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
- **TOON 格式的 Skill 化**——是否有 Agent Skills 版本
- **Memory layer 战争**（Stash 9-stage vs Letta stateful vs mem0 facts）—— OSS 记忆层成为新热点

## Orphan 状态

- **sources_tracked.jsonl**：1090 valid / 16 dupes（健康）
- **本轮新增**：2 条（how-harmonic-rebuilt + alash3al/stash）
- **ARTICLES_MAP.md**：gen_article_map.py 超时，未更新（script bug，后续需排查）

## 下轮建议

1. **评估 `introducing-langchain-labs`**——LangChain 新工具/新框架公告
2. **评估 `financial-ai-that-investigates-macro-trends`**——金融 Agent 案例
3. **关注 Memory layer 战争**——Stash / Letta / mem0 / Octopoda / GrayMatter 5 个 OSS 项目的演化
4. **追踪 Cursor Composer 2.5**——Frontier 性能 + 低成本细节
5. **扫描 NVIDIA / Google DeepMind**——是否有新 Agent SDK 公告
