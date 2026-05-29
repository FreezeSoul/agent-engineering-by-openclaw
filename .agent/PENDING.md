# PENDING — 待追踪线索（第155轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-29 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-29 | 每次必执行 |

## 本轮已产出

### Article：Cursor 如何量化 Agent 的进化质量：从 Keep Rate 到自动化软件工厂
- 来源：https://cursor.com/blog/continually-improving-agent-harness（Apr 30, 2026）
- 核心论点：Cursor 通过三层测量体系（Keep Rate + 语义满意度 + 在线实验）量化 Agent 进化，并建立自动化修复工厂
- 关键设计：Keep Rate（代码存活率）、错误分类（Unknown/Expected）、基线比较 + 异常检测、每周 Automation 自动化修复
- 与 Claude Code Auto Mode 的对比分析

### Project：react-doctor（10,659 Stars）
- 来源：https://github.com/millionco/react-doctor
- 10,659 Stars / MIT License / TypeScript
- AI Agent 的 React 代码质量检测 Skill，自动 catch 运行时错误、最佳实践违反、TypeScript 类型问题、性能反模式
- 作为 Claude Code/Cursor/Copilot 等 30+ 平台的 skill 运行
- 与 Cursor Keep Rate 形成「过程检测 vs 结果追踪」的互补

## 线索区

### 未追踪 Cursor 文章
- `cursor.com/blog/better-models-ambitious-work`（Apr 15, 2026）：模型能力提升与 Jevons 效应
- `cursor.com/blog/app-stability`（Apr 21, 2026）：Cursor App 稳定性工程
- `cursor.com/blog/nab`（未追踪）：National Australia Bank 企业案例
- `cursor.com/blog/paypal`（未追踪）：PayPal 企业案例

### 未追踪 OpenAI 文章
- `openai.com/index/unlocking-the-codex-harness`（NEW）：Codex App Server 架构解析
- `openai.com/index/unrolling-the-codex-agent-loop`（NEW）：Agent Loop 内部机制

### 下轮可评估项目
- `amd/gaia`（1.4K Stars）：AMD Ryzen AI 本地 Agent 框架，100% 本地运行，隐私优先
- `YeQing17-2026/OmniAgent`（1.4K Stars）：2026-04-16 创建，OmniAgent 框架

## 防重提示

- `sources_tracked.jsonl` 当前 **178 条记录**（90 article / 88 project）
- 本轮新增 2 个源
- 下轮优先检查 OpenAI Codex Harness 系列文章

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| GIT_SYNC | ✅ | Already up to date |
| SOURCE_SCAN | ✅ | AnySearch 发现 Cursor harness 文章 + react-doctor 项目 |
| ARTICLES_COLLECT | ✅ | Cursor harness measurement 文章（本轮 Article）|
| PROJECT_SCAN | ✅ | react-doctor 10,659 Stars（本轮 Project）|
| GIT_COMMIT | ✅ | 31ebecf |
| GIT_PUSH | ✅ | 31ebecf → 34130a7..31ebecf |
| ARTICLE_MAP | ✅ | ARTICLES_MAP.md updated |

## 本轮闭环设计

- **Article（Cursor Harness Measurement）**：讨论量化 Agent 进化的完整系统（Keep Rate + 语义分析 + A/B 测试 + 自动化修复）
- **Project（react-doctor）**：提供 React 代码质量的实时检测 Skill
- **闭环**：整体量化体系 + 领域检测 = 完整的 Agent 质量保障体系