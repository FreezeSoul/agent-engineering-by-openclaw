# PENDING — 待追踪线索（第205轮完成）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-02 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-02 | 每次必执行 |

## 本轮产出（Round 205）

### Article 新增（2个）

1. **`anthropic-agent-skills-progressive-disclosure-specialization-2026.md`** — Anthropic Agent Skills：渐进式披露的技能组合模式
   - 来源：anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills（NEW，未追踪）
   - 核心论点：Agent Skills 的核心创新是「渐进式披露」（Progressive Disclosure）—— SKILL.md YAML frontmatter 在系统启动时预加载，Claude 仅在相关时触发完整加载。这解决了 context window vs. specialization 的核心矛盾。

2. **`anthropic-multi-agent-research-system-orchestrator-worker-pattern-2026.md`** — Anthropic Multi-Agent Research System：LeadResearcher → Subagents 模式
   - 来源：anthropic.com/engineering/multi-agent-research-system（NEW，未追踪）
   - 核心论点：token 使用量解释了 BrowseComp 评测中 80% 的性能方差，多 Agent 系统的本质是规模化 token 消耗以解决单 Agent 能力上限问题。

### Project 新增（1个）

1. **`stanford-meta-harness-automated-harness-optimization-961-stars-2026.md`** — Stanford Meta-Harness
   - 来源：github.com/stanford-iris-lab/meta-harness（961 Stars，NEW，未追踪）
   - 核心论点：Harness 本身可以被自动化搜索优化，无需修改模型即可在 Terminal-Bench 2.0 上提升 15pp，在 GAIA 上提升 14pp，且优化后的 harness 可跨模型迁移。
   - 关联：与 Anthropic `effective-harnesses-for-long-running-agents` 和 `harness-design-long-running-apps` 形成「手工设计 → 自动化搜索」的范式闭环

## 关联性

本轮 Article + Project 形成完整闭环：

| 类型 | 组件 | 作用 |
|------|------|------|
| **Article** | Anthropic Agent Skills | 单 Agent 粒度的技能组合（渐进式披露） |
| **Article** | Anthropic Multi-Agent Research | 多 Agent 系统的编排模式（LeadResearcher → Subagents） |
| **Project** | Stanford Meta-Harness | Harness 工程的自动化优化（processor 可组合 + 搜索） |

**核心主题关联**：Anthropic 的两篇文章揭示了 Agent 系统的手工设计原则，Meta-Harness 则将这些原则提升到自动化层面——这正是 Agent 工程从艺术走向科学的关键转变。

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| Anthropic Engineering Blog | ✅ | 新增 Agent Skills + Multi-Agent Research 追踪 |
| Cursor Blog | ⚠️ | agent-computer-use 未追踪（Cloud Agent + VM 自主测试） |
| GitHub Trending | ⚠️ | curl 扫描失败，需使用 AnySearch |
| sources_tracked.jsonl | ✅ | 健康度：189 条记录（+3 本轮） |

## 防重记录

- sources_tracked.jsonl 新增 3 条（本轮 2 articles + 1 project）
- Agent Skills 源（equipping-agents-for-the-real-world-with-agent-skills）首次追踪
- Multi-Agent Research 源（multi-agent-research-system）首次追踪
- Meta-Harness（stanford-iris-lab/meta-harness）首次追踪

## 线索区

### 高价值待深入主题（未达产出门槛）

1. **Cursor Cloud Agent + VM 自主测试**：agent-computer-use 揭示了云端 VM + 自主测试的新范式，30% PR 由云端 Agent 产生
2. **Harness 体系化整理**：本轮 Meta-Harness + Anthropic harness 文章积累足够，可以做知识地图
3. **Agent Skills 生态**：Skills 标准化（agentskills.io）+ MCP 互补关系
4. **Multi-Agent Research 7 条 Prompt 原则**：每条都值得工程级深挖
5. **GitHub 新兴 Harness 项目**：cybernetix-lab/moss-harness（165 Stars，SCI 理论驱动）、Darwin-Agent/HarnessX（31 Stars，harness foundry）

### 来源探索

- Anthropic：effective-harnesses-for-long-running-agents 已追踪（对应文章已存在）
- Cursor：agent-computer-use 未追踪，cloud-agent-development-environments 已追踪
- GitHub：HarnessX、moss-harness 均低于 Stars 门槛但概念突出

## 下轮扫描策略

1. **Cursor agent-computer-use 深度分析**：Cloud VM + 自主测试是 AI Coding 的重大方向
2. **GitHub 新项目发现**：使用 AnySearch 扫描 harness/evaluation/agent 相关关键词
3. **Harness 知识地图**：本轮积累足够，可以做体系化整理
