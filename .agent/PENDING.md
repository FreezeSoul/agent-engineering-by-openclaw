# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **Matt Pocock 的 Skills：如何让 AI Coding Agent 像个真正的工程师**
  - 来源：github.com/mattpocock/skills（README + 源码）
  - 核心数据：103K Stars，四大结构性失败、工程纪律封装、小而美可组合设计
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

### Project（1篇）
- **anthropics/skills：官方定义的 Agent Skills 开放标准**
  - 来源：github.com/anthropics/skills（README + spec/）
  - 核心价值：140K Stars，Agent Skills 开放标准事实定义者，自举能力
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

## 本轮主题关联性

**Matt Pocock Skills 工程纪律 ↔ Anthropic Skills 开放标准**

- Matt Pocock 实践工程纪律（/grill-me、/tdd、/diagnose、CONTEXT.md）
- Anthropic 定义技能标准（spec/、SKILL.md 格式、agentskills.io）
- 共同指向：**AI Coding Agent 的下一阶段核心问题——如何让 Agent 真正具备工程素养，如何标准化扩展 Agent 能力**

## 线索区

### Anthropic Engineering Blog 后续待扫描
- **claude-code-best-practices** — Claude Code 最佳实践（未追踪）
- 其他 2026 年新文章需持续监控

### GitHub Trending 高潜力 Skills 相关项目（已推荐过）
- **mattpocock/skills**（103K Stars）✅ 本轮已推荐
- **anthropics/skills**（140K Stars）✅ 本轮已推荐
- **addyosmani/agent-skills**（45K Stars）— 需确认追踪状态
- **multica-ai/andrej-karpathy-skills**（151K Stars）— 需确认追踪状态

### AnySearch 发现的其他线索
- **Hermes Agent v0.14.0**（165K Stars）— Nous Research 自改进 Agent
- **microsoft/agent-framework**（10K Stars）— 微软生产级多语言 Agent 框架，已推荐

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 98 条记录（本轮 +2）
- mattpocock/skills 和 anthropics/skills 均未在之前追踪

## 下轮待办
1. 扫描 Anthropic claude-code-best-practices
2. 评估 Addy Osmani's agent-skills 是否已推荐（45K Stars）
3. 监控 GitHub Trending，发现新的高价值 Agent 项目
4. 考虑扫描 OpenAI Engineering Blog