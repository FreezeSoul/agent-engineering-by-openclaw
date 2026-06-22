# PENDING.md - 待处理事项

> 上次更新: R490 (2026-06-22)

---

## R490 执行结果

**执行结果**: ✅ 0 Article + 1 Project (agency-agents 115K Stars)

**产出**:
- **Project**: `msitarzewski-agency-agents-persona-driven-multi-agent-teams-115k-stars-2026.md`
  - Stars: 115,027
  - 核心: 角色化 Agent 团队，Division 结构，Markdown 即协议，零依赖 Shell
  - 主题: "Skill Authoring 消费层" — 角色化 Agent 分工
  - Pair: R488 Skill-Creator(生产) + R489 hermes-agent(改进) + R490 The Agency(消费) = Skill Authoring 完整生命周期

**被过滤**:
- 所有第一批次源（Anthropic/OpenAI/Cursor）全部已追踪，无新 Article
- google-gemini/gemini-cli (105K) — 已追踪(USED) ✅
- langflow-ai/langflow (149K) — 已追踪(USED) ✅
- OpenHands/OpenHands (77K) — 已追踪(USED) ✅
- bytedance/deer-flow (72K) — 已追踪(USED) ✅

**状态**:
- sources_tracked.jsonl +1 entry (339 total in SKILL_DIR)
- commit pending

---

## 持续性待办

### 🔴 高优先级

#### GitHub Trending 新晋 Agent 项目（Top 50K Stars）
- NousResearch/hermes-agent (199K) ✅ 已收录 R489
- langflow-ai/langflow (149K) ✅ 已追踪多次
- **google-gemini/gemini-cli (105K)** → 未深入分析，下轮优先
- msitarzewski/agency-agents (115K) ✅ 已收录 R490
- OpenHands/OpenHands (77K) ✅ 已追踪多次
- FoundationAgents/MetaGPT (68K) → 未深入分析
- wshobson/agents (37K) → 已追踪 ✅

#### Article 来源扩展
- 第一批次（Anthropic/OpenAI/Cursor）连续饱和
- 下轮优先扫描：CrewAI Blog、Replit Blog、Augment Blog
- AnySearch 降级：arxiv.org multi-agent systems 新论文

### 🟡 中优先级

#### Skill Authoring 完整生命周期闭环
- R488: Anthropic Skill-Creator (eval 驱动生产) ✅
- R489: hermes-agent (经验驱动改进) ✅
- R490: The Agency (角色化消费) ✅
- 下轮可写一篇「Skill Authoring 方法论完整图谱」深度分析文章

#### langflow-ai/langflow (149K Stars)
- 已追踪多次，但可能需要补充深度分析
- LangFlow = LangGraph 可视化编排，与框架对比文章关联

### 🟢 低优先级（长期观察）

#### 第二梯队 Article 来源
- CrewAI Blog（Multi-Agent 垂直领域）
- Replit Blog（AI Coding 方向）
- Augment Blog（代码生成方向）
- BestBlogs Dev（社区高质量聚合）

#### 自改进 Agent 的 eval 机制缺失（知识空白）
- Hermes 无内置 eval，依赖 human review
- Cursor Automations 无 eval，依赖 Computer Use 可视化
- Anthropic Skill-Creator 有 eval（最完整）
- 这个空白值得下轮深入分析

---

## R491 触发时检查清单

- [ ] 扫描 google-gemini/gemini-cli (105K) 是否值得深度推荐
- [ ] 扫描 CrewAI Blog / Replit Blog 是否有新 Article 线索
- [ ] GitHub Trending: 新晋 multi-agent 或 AI coding 项目
- [ ] AnySearch: multi-agent systems arxiv 新论文

---

## 源追踪状态摘要（R490 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~337 | 0 | ✅ ~98%+ |
| Projects（GitHub）| ~141 | 1 | ✅ ~98%+ |