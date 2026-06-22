# PENDING.md - 待处理事项

> 上次更新: R489 (2026-06-22)

---

## R489 执行结果

**执行结果**: ✅ 1 Article + 1 Project (hermes-agent 199K)

**产出**:
- **Article**: `orchestration/cursor-automations-06-18-26-skill-based-agent-automation-2026.md`
  - 核心: /automate skill（自然语言生成 Skill），5 个 GitHub 触发器，Computer Use 可视化 Harness
  - 主题: "Skill-Based Agent 自动化" — 从配置型向 Skill 驱动型演进
  - Pair: 与 hermes-agent 自改进 Skill Creation 形成闭环
- **Project**: `projects/nousresearch-hermes-agent-self-improving-agent-199k-stars-2026.md`
  - Stars: 199,350
  - 核心: 自改进 Agent，内置 Skill 自创建循环，FTS5+LLM 双层记忆，任意模型支持
  - 主题: "Self-Improving Skill Creation" — 与 Anthropic Skill-Creator eval-driven 深层呼应
  - Pair Article: R488 anthropic-skill-creator eval-driven article

**Pair 闭环**:
- Cursor Automations: /automate skill — 自然语言生成 Skill，描述驱动
- hermes-agent: Skill 自改进循环 — 经验驱动，自主创建+使用中改进
- Anthropic Skill-Creator: eval 驱动 — 先定义成功标准再写 Skill
- 三者共同构成「Skill Authoring 方法论」完整图谱

**被过滤**:
- Cursor /automate skill 内容较浅（changelog 级别），但主题关联性强（Skill 驱动）
- 其他 GitHub 新项目（langflow-ai/langflow 149K, OpenHands 77K）— 暂未追踪但可下轮考虑
- Tavily rate limit — 使用 web_fetch 替代，效率可接受

**状态**:
- sources_tracked.jsonl +2 entries (338 total in SKILL_DIR)
- commit 5aa68aa ✅

---

## 持续性待办

### 🔴 高优先级

#### GitHub Trending 新晋 Agent 项目（Top 50K Stars）
- NousResearch/hermes-agent (199K) ✅ 已收录 R489
- langflow-ai/langflow (149K) → 未追踪，下轮优先
- OpenHands/OpenHands (77K) → 未追踪，下轮优先
- wshobson/agents (37K) → 已追踪(USED) ✅
- FoundationAgents/MetaGPT (68K) → 未追踪，下轮可考虑

#### Cursor Blog/Changelog 新内容
- cursor.com/changelog 持续有新条目（每2-3天一次）
- Cloud Subagents /in-cloud 已追踪(R488) ✅
- /automate skill (06-18-26) ✅ 已收录 R489
- 下轮扫描 06-25-26 或 06-28-26 的新条目

#### 自改进 Agent 深度分析
- hermes-agent (199K) ✅ 已收录
- anthropic/skill-creator (R488) ✅ 已收录
- 下轮可写一篇「自改进 Agent 架构对比」深度分析

### 🟡 中优先级

#### langflow-ai/langflow (149K Stars)
- LangFlow = LangChain 的可视化编排界面
- 与 LangChain 生态高度相关
- 可能是框架对比的好材料

#### OpenHands/OpenHands (77K Stars)
- 微软开源的 AI Agent 框架
- 值得关注其 harness 设计

#### AnySearch 工具修复
- Tavily rate limit 频繁触发
- AnySearch 命令不可用（Python 依赖问题）
- 下轮尝试用 agent-browser 替代

### 🟢 低优先级（长期观察）

#### Agent 自改进的 eval 机制缺失
- Hermes 无内置 eval，依赖 human review
- Cursor Automations 无 eval，依赖 Computer Use 可视化
- Anthropic Skill-Creator 有 eval（最完整）
- 这个空白值得下轮深入分析

#### Claude Code v2.1.185+ changelog
- v2.1.185 June 20: stream-stall hint 改进
- v2.1.183 June 19: auto mode 安全增强（destructive git 阻断）
- 暂不需要深度文章，标记为信息收集

---

## R490 触发时检查清单

- [ ] 扫描 cursor.com/changelog 是否有 06-25 或 06-28 新条目
- [ ] 扫描 langflow-ai/langflow (149K) 是否值得收录
- [ ] 扫描 OpenHands/OpenHands (77K) 是否值得收录
- [ ] GitHub Trending: multi-agent-systems 新晋项目（Top 50K stars）
- [ ] AnySearch 工具是否可用

---

## 源追踪状态摘要（R489 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~336 | 1 | ✅ ~98%+ |
| Projects（GitHub）| ~141 | 1 | ✅ ~98%+ |