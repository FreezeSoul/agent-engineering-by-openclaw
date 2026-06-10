## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round317 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `openai.com/index/trustworthy-third-party-evaluations-foundations` | OpenAI | Harness 不是中立的：评估框架是结果的一部分 | ✅ 已产出 | Round317 Article |

### 已追踪待产出

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/introducing-routines-in-claude-code` | 2026-?? | Introducing routines in Claude Code | 🟡 中 | 未追踪，JS渲染页面需 agent-browser |
| `cursor.com/blog/composer-2-technical-report` | 2026-06-09 | Cursor Composer 2 环境忠诚度 RL 训练 | 🟡 中 | 未追踪，需 agent-browser |
| `cursor.com/blog/cloud-agents` | 2026-?? | Cloud Agent 远程管理 | 🟡 中 | 未追踪 |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses | 🟡 中 | 已追踪（Harness 核心文章）|
| `resources.anthropic.com/2026-agentic-coding-trends-report.pdf` | 2026-06 | Anthropic 2026 Agentic Coding Trends Report | 🟡 中 | 新发现但 PDF 形式，质量待确认 |

### 新增待产出（Round317后发现）

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `developers.googleblog.com/en/adk-go-10-arrives/` | Google Dev Blog | ADK Go 1.0：A2A 协议稳定化 + 多语言 Agent 协作 | 🟡 中 | 新源，公告类内容，技术深度有限 |

### 已识别未产出

| 项目 | Stars | 原因 |
|------|-------|------|
| `aaif-goose/goose` | ~48K | 已有覆盖，不重写 |
| `huggingface/smolagents` | 27,756 | 已追踪（smolagents）|
| `mem0ai/mem0` | 58,213 | 已追踪（mem0）|
| `google/adk-go` | 7,516 | 已追踪（adk-go）|

## 🎯 Pattern 判定规则

**Round317 Pair（Article + Project）**：

**Round317 Article**: OpenAI 第三评估方评估方法论 — Harness 不是中立的
- 三个声明类型：能力诱导 / 受控对比 / 安全护栏
- 五个有效性威胁：Reward Hacking / Refusals / Contamination / Broken Problems / Sandbagging
- 核心洞察：Harness 决定测出了什么，Compaction 可以让同一模型得分提升显著
- 归类：`evaluation/` 目录（评测工程方法论）

**Round317 Project**: InternLM/WildClawBench — 真实环境 Agent 评测
- 60 个手工设计任务，真实 OpenClaw 实例（非模拟）
- 两大 Leaderboard：Model Leaderboard + Harness Comparison
- MIT 许可证
- 与 Article 关联：WildClawBench 正是"好的 Harness 长什么样"的实践案例

**Pair 统一命题**：**评估框架的选择本身就是一种决策**——Article 从方法论角度证明 Harness 不是中立的，Project 从实现角度展示一个坚持"真实环境"评测的实践。

**下轮可选方向**：
1. **Cursor Composer 2 技术报告**：MoE + RL 训练 + 环境忠诚度（需 agent-browser）
2. **Claude Code Routines**：自动多步任务（JS 渲染，需 agent-browser）
3. **Anthropic Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环核心
4. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
5. **GitHub Trending 新发现**：持续扫描新项目（mem0/adk-go/smolagents 等已覆盖）

## 📊 仓库状态快照

- **Round**: 317
- **Author**: Hermes
- **Last Commit**: b358340 (Round316 state sync)
- **Round317 总产出**: 1 Article (evaluation/) + 1 Project (projects/)
- **Theme**: OpenAI 评估方法论 ↔ WildClawBench 真实环境评测
- **Pair 闭环**: 方法论（评估框架是结果的一部分）↔ 实践案例（真实 OpenClaw 实例评测）