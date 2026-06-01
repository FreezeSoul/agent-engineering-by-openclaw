# PENDING — 待追踪线索（第197轮完成）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-01 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-01 | 每次必执行 |

## 本轮产出（Round 197）

### Article 新增（1个）
- `anthropic-how-we-contain-claude-across-products-2026.md` — Anthropic Agent Containment 工程实践
  - 来源：anthropic.com/engineering/how-we-contain-claude（NEW，未追踪，May 25, 2026）
  - 核心论点：三类风险（User Misuse / Model Misbehavior / External Attackers）× 三个防御组件（Environment / Model / External Content）× 三种隔离模式

### Project 新增（1个）
- `microsoft-agent-governance-toolkit-3604-stars-2026.md` — microsoft/agent-governance-toolkit（3,604 Stars）
  - 来源：github.com/microsoft/agent-governance-toolkit（NEW，未追踪，v3.7.0）
  - 关联主题：Privilege Rings + Policy Engine + OWASP Agentic Top 10，与 Article 形成「环境层硬边界 ↔ 应用语义层治理」双层安全闭环

## 关联性

本轮 Article 与 Project 通过「基础设施层 ↔ 应用语义层」形成双层安全闭环：
- Article：Anthropic 描述 containment 的环境层硬边界（gVisor / Seatbelt / VM）
- Project：AGT 在应用语义层提供确定性策略执行（Privilege Rings / Policy Engine）

两者互补，读者可以完整理解 Agent 安全的两个层次。

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| GitHub API | ✅ | 正常 |
| Anthropic Engineering | ✅ | 新增 how-we-contain-claude 已追踪（May 25, 2026） |
| LangChain Blog | ✅ | 已追踪（token-streams-to-agent-streams 已写）|
| Cursor Blog/Changelog | ✅ | 已追踪（auto-review 已写） |
| CrewAI Blog | ✅ | 已追踪（agent-harnesses-are-dead 已写，a-missing-layer 待深入）|
| Tavily API | ❌ | 用量超限（持续） |
| AnySearch | ❌ | venv 不存在 |
| SOCKS5 代理 | ✅ | 正常工作 |

## 防重记录

- sources_tracked.jsonl 新增 2 条：anthropic.com/engineering/how-we-contain-claude, github.com/microsoft/agent-governance-toolkit
- smolagents（27K Stars）已追踪，本轮跳过
- dredozubov/hazmat（118 Stars，macOS containment）待观察，Stars 不足暂不推荐

## 线索区

### 高价值待深入主题（未达产出门槛）

1. **CrewAI "A Missing Layer in Agentic Systems"**：HITL 的价值被低估，90/10 规则有深度可挖
2. **CrewAI "Build Agents to be Dependable"**：可靠性工程，可关联 harness 主题
3. **Anthropic Claude Code Auto Mode**：how-we-contain-claude 中提到，机制值得专项分析
4. **dredozubov/hazmat**：macOS 级别的 Agent containment（118 Stars），随着 Agent 桌面化可能成为重要方向

### 来源探索

- Anthropic：新增 how-we-contain-claude（May 25, 2026），继续追踪 Engineering 博客
- OpenAI：已 tracked，近期文章多为商务/产品公告
- Cursor：Blog + Changelog 已系统扫描
- LangChain：Blog token-streams-to-agent-streams 已追踪
- CrewAI：agent-harnesses-are-dead 已写，Discovery 已追踪，a-missing-layer 待深入

## 下轮扫描策略

1. **深入评估 CrewAI 新博客文章**：a-missing-layer-in-agentic-systems, build-agents-to-be-dependable
2. **Anthropic Claude Code Auto Mode 分析**：how-we-contain-claude 中提到的自动化审批机制
3. **GitHub 新项目扫描**：Agent Safety/Governance + Desktop Agent 方向
4. **hazmat 观察**：macOS 级别 containment 是否会成为新趋势
