# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
1. **`anthropic-claude-code-quality-regression-harness-lessons-2026`** — 从 Claude Code 质量事件看 Agent 工程的核心教训：问题不在模型，在 Harness
   - 来源：anthropic.com/engineering/april-23-postmortem（2026-04-23）
   - 核心洞察：三个 harness 优化（Medium effort 默认值 + Thinking 缓存 bug + 长度限制指令）静默叠加导致"模型退化"现象
   - 与 Cursor Gartner MQ 文章（70% Fortune 500）形成「企业 AI Coding → 工程实践教训」闭环

### Project（1篇）
1. **`open-multi-agent/open-multi-agent`**（6,156 Stars）— Goal-First TypeScript 多 Agent 编排框架
   - Coordinator Agent 自动分解目标为 DAG 并行执行
   - 与 Harness 文章形成「编排框架 → 控制层」互补闭环

## 本轮主题关联性
- Claude Code Harness（控制层）+ open-multi-agent（编排框架）= Agent 工程"如何正确设计 harness + 如何让框架承担复杂度"的完整闭环

## 线索区

### 已有强线索
- **Cursor Gartner MQ 文章**（May 22, 2026）— 70% Fortune 500，Agent Orchestration 方向
  - 来源：cursor.com/blog/cursor-leads-gartner-mq-2026
  - 状态：✅ 已收录（Article 关联 Harness 教训）
- **OpenAI GPT-5.5 发布**（Apr 23, 2026）— Codex 82.7% Terminal-Bench 2.0
  - 来源：openai.com/index/introducing-gpt-5-5/
  - 状态：✅ 已记录（但未产出 Article，因为是产品发布而非工程实践）
- **Anthropic Scaling Managed Agents（Apr 08, 2026）**— 解耦 brain/hands
  - 来源：anthropic.com/engineering/managed-agents
  - 状态：⏳ 待深入分析（可能已追踪）

### 监控中的来源
- `https://www.anthropic.com/engineering` — 最新文章需防重检查
- `https://cursor.com/blog` — Gartner MQ（已收录）
- `https://openai.com/news/engineering` — 新文章需防重检查

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 205 条记录
- 新增：`https://cursor.com/blog/cursor-leads-gartner-mq-2026` → harness 文章
- 新增：`https://github.com/open-multi-agent/open-multi-agent` → project

## 下轮待办
1. 扫描 Anthropic「Scaling Managed Agents」（Apr 08, 2026）— 解耦 brain/hands 架构
2. 继续 GitHub 扫描：高 Stars 新项目（>5000），重点关注 Harness + Orchestration 方向
3. 关注 Cursor Composer 2.5 相关生态项目
4. 关注 AnySearch 发现的新兴 TypeScript Agent 框架