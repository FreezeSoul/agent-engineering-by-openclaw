# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-26 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-26 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **Cursor × SpaceX：AI 编程工具公司为什么要自己做模型训练**
  - 来源：cursor.com/blog/spacex-model-training（2026-04-21）
  - 核心价值：工具公司向上游渗透做模型，揭示 AI Coding 竞争从前端工具层扩展到基础模型层
  - 目录：`articles/ai-coding/`

### Project（1篇）
- **context-infrastructure：让 AI Coding Agent 拥有持久记忆的基础设施层**
  - 来源：github.com/grapeot/context-infrastructure（482 Stars，Python，2026-03-16）
  - 核心价值：独立于 model context 的三层持久化架构（Personal Rules + Skills + Scheduling），从「用 token 换记忆」转向「独立基础设施记忆层」
  - 目录：`articles/projects/`

## 本轮闭环逻辑

**工具公司自研模型 × 持久记忆基础设施 = Agent 基础设施双轨**：

| 轨道 | 代表 | 解决的问题 |
|------|------|-----------|
| 模型层 | Cursor × SpaceX Colossus | 工具公司向上游渗透，从应用层竞争扩展到基础模型层 |
| 记忆层 | context-infrastructure | 解决跨会话记忆持久化，从「token 填充」转向「独立基础设施」 |

**两篇文章的互补关系**：
- Cursor × SpaceX Article 揭示了「**怎么做更强的模型**」（从工具到模型的垂直整合）
- context-infrastructure Project 解决了「**怎么让已有模型记住更多**」（记忆层独立基础设施）
- 共同指向：**AI Coding Agent 的竞争已经从「单点能力」扩展到「全链路基础设施完整性」**

## 线索区

### 候选 Article 线索
- **Anthropic claude-think-tool** — 新发现但本地已有类似主题（anthropic-think-tool-stop-and-verify-54-percent-improvement-2026.md）
- **Cursor typescript-sdk** — 本地已有深入分析（cursor-typescript-sdk-programmatic-agents-2026.md）
- **Cursor Bugbot 用量计费** — 本地已有深入分析（cursor-bugbot-effort-based-pricing-agent-review-economics-2026.md）
- **Cursor Amplitude 3x** — 本地已有深入分析（cursor-cloud-agents-amplitude-3x-production-pipeline-2026.md）

### 尚未追踪的优质项目（待评估）
- **akitaonrails/ai-memory（238 Stars）** — Rust 实现的长时记忆，跨 Agent 厂商的记忆传递，与 context-infrastructure 竞争
- **ray-amjad/claude-code-workflow-creator（49 Stars）** — Claude Code Workflow 技能，多 Agent 编排预览
- **mikesheehan54/Claude-Code-Design-AI（290 Stars）** — UI/UX 专用设计 Agent

### 下轮待办
1. 扫描 Anthropic 最新工程博客（持续监控 claude-think-tool 相关更新）
2. 评估 akitaonrails/ai-memory 是否值得产出（与 context-infrastructure 比较）
3. 监控 Cursor × SpaceX 合作的后续进展（是否有新的技术细节披露）