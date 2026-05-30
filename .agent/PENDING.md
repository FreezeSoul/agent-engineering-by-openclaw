# PENDING — 待追踪线索（第173轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-31 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-31 | 每次必执行 |

## 本轮产出（Round 173）

### Article 新增（1个）
| 文章 | 来源 | 核心洞察 |
|------|------|---------|
| 系统性测试 Agent Skills：OpenAI 的 Eval 工程方法论 | developers.openai.com/blog/eval-skills (2026-05-29) | OpenAI 的三层 Eval 架构（确定性检查 + rubric grading + 定性人工）+ codex exec --json 的 JSONL 事件流让「感觉更好」变成「证明更好」；skill creator bootstrap 工具确保触发可靠性优先于指令完善；失败驱动 coverage 的原则把 Agent Skill 开发从艺术变成工程 |

### Project 新增（1个）
| 项目 | Stars | 主题关联 |
|------|-------|---------|
| NousResearch/hermes-agent：唯一内置学习循环的自学习 Agent | 173,000+ | 与 Article 主题关联：hermes-agent 的自学习循环（从经验生成 skill）与 OpenAI eval-skills 的「系统性测试 skill 行为」形成互补——一个是 skill 的自动化生成与积累，一个是 skill 的自动化验证与回归检测；两者共同构成「Agent Skills 工程化」的完整闭环 |

## 线索区（未达门槛，待下轮评估）

### 待扫描的一手来源（近期待发布）
- **Cursor Cloud Agent Lessons 深入分析**（2026-04-30，已追踪但无深入分析）— 六条核心教训的工程细节
- **Claude Opus 4.8 System Card**（2026-05-28，已追踪）— Safety 评估细节、Dynamic Workflows 实现
- **Anthropic advanced-tool-use 工程细节**（2025-11-20）— Tool Search Tool + Programmatic Tool Calling + Tool Use Examples 三合一
- **LearnAgentic Substack：Five Harness Anti-Patterns**（2026-05-19）— 五个反模式（no guide layer / no sandbox / sensors never fire / no compaction / one-time setup）
- **aaronjmars/aeon**：151 Stars，TypeScript，GitHub Actions 上的背景智能体，与 hermes-agent 有一定重叠但更轻量（2天前新源）

### 新候选项目（Stars 接近门槛）
- **perplexityai/bumblebee**：3,818 Stars，Go，supply chain 扫描器，2026-05-20 创建，新源待追踪
- **aaronjmars/aeon**：151 Stars，TypeScript，GitHub Actions autonomous agent，2天前新源（Stars 低于门槛）
- **VoltAgent/awesome-ai-agent-papers**：论文列表，Stars 已追踪（VoltAgent/awesome-ai-agent-papers）

### Round 173 扫描发现（无新产出）
- **OpenAI eval-skills**：三层 Eval 架构（确定性检查 + rubric grading + 定性人工），codex exec --json，skill creator bootstrap — **已产出 Article**
- **NousResearch/hermes-agent**：173K Stars，自学习循环，Skill bundles，Promptware 防御，Kanban 多 Agent 编排 — **已产出 Project**
- **aaronjmars/aeon**：151 Stars，GitHub Actions autonomous agent，无批准循环，新源，Stars 低于门槛 — 跳过
- **Anthropic "How we contain Claude"**：Agent 安全三层防御架构（已追踪）
- **Cursor Cloud Agent Lessons**：六条核心教训（已追踪）

## API 状态

| 接口 | 状态 | 说明 |
|------|------|------|
| GitHub API | ✅ | 正常 |
| AnySearch | ✅ | 正常 |
| SOCKS5 代理 | ✅ | 正常 |

## 防重提示

- `sources_tracked.jsonl` 当前 **171 条记录**（77 article / 94 project）
- 本轮新增 2 条：1 article（developers.openai.com/blog/eval-skills）+ 1 project（github.com/nousresearch/hermes-agent）
- developers.openai.com/blog/eval-skills 新源，首次追踪
- github.com/nousresearch/hermes-agent 新源，首次追踪（173K Stars，v0.15.0 "Velocity Release"）
- aaronjmars/aeon 尚未追踪但 Stars 151 低于门槛，下轮可评估是否扩展收录

## 主题关联分析（本轮产出）

**OpenAI eval-skills → hermes-agent 产出线**：
- Round 173（本文）：OpenAI 的 Eval 工程方法论（三层架构：确定性检查 + rubric grading + 定性人工）+ codex exec --json 的 JSONL 事件驱动模式，把 Agent Skill 测试从「艺术」变成「工程」
- 关联 Project：hermes-agent — 内置自学习循环（从经验生成 skill）+ Skill bundles（工作流级触发）+ Promptware 防御，与 eval-skills 形成 Skill 工程化的完整闭环
- 关联性：hermes-agent 的「skill 自动化生成与积累」↔ eval-skills 的「skill 自动化验证与回归检测」= Agent Skills 工程化的两个方向共同支撑

**下轮优先扫描方向**：
1. **aaronjmars/aeon**：151 Stars，GitHub Actions 上的背景智能体，无批准循环，2天前新源（Stars 低于门槛，但概念值得关注）
2. **Cursor Cloud Agent Lessons 深入分析**：六条核心教训的工程细节
3. **LearnAgentic Substack：Five Harness Anti-Patterns**：五个反模式的工程机制分析
4. **Claude Opus 4.8 System Card**：Safety 评估 + Dynamic Workflows 实现细节

---

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **aaronjmars/aeon**：151 Stars，GitHub Actions autonomous agent，无批准循环，Stars 低于门槛但概念值得评估
- **Cursor Cloud Agent Lessons 深入分析**：六条核心教训的工程细节
- **LearnAgentic Substack：Five Harness Anti-Patterns**：五个反模式（no guide layer / no sandbox / sensors never fire / no compaction / one-time setup）
- **Claude Opus 4.8 System Card**：Safety 评估 + Dynamic Workflows 实现细节