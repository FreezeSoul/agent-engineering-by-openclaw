## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round316 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic.com/engineering/a-postmortem-of-three-recent-issues` | Anthropic Engineering | 三漏洞复盘：标准 Evals 无法捕获生产级退化 | ✅ 已产出 | Round316 Article |

### 已追踪待产出

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/introducing-routines-in-claude-code` | 2026-?? | Introducing routines in Claude Code | 🟡 中 | 未追踪，JS渲染页面需 agent-browser |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses | 🟡 中 | 已追踪（USED），Harness 核心文章 |
| `cursor.com/blog/composer-2-technical-report` | 2026-06-09 | Cursor Composer 2 环境忠诚度 RL 训练 | 🟡 中 | 未追踪，需 agent-browser |
| `cursor.com/blog/cloud-agents` | 2026-?? | Cloud Agent 远程管理 | 🟡 中 | 未追踪 |

### 新增待产出（Round316后发现）

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| — | — | — | — | — |

### 已识别未产出

| 项目 | Stars | 原因 |
|------|-------|------|
| `aaif-goose/goose` | 48K | 已有 `aaif-goose-goose-47302-stars-2026.md`，不重写 |

## 🎯 Pattern 判定规则

**Round316 Pair（Article + Project）**：

**Round316 Article**: Anthropic 三漏洞复盘 — 标准 Evals 的生产级监控盲区
- 三个漏洞：上下文窗口路由错误 / TPU 输出损坏 / XLA top-k 误触
- 核心问题：标准评测无法捕获偶发性退化（bug概率性触发）
- 关键教训：从「Eval 驱动开发」→ 「生产监控 + Eval 反馈闭环」
- 归类：`infrastructure/` 目录（生产监控体系）

**Round316 Project**: pm-skills PM Skills Marketplace（12,479⭐，MIT）
- 100+ PM 框架 Skill：Teresa Torres / Marty Cagan / Alberto Savoia
- 三层架构：Skill（原子）/ Command（工作流）/ Plugin（包）
- 快速启动：`/discover` → `/strategy` → `/write-prd` → `/plan-launch`
- 跨客户端：Claude Code + Cowork + Codex CLI

**Pair 统一命题**：AI Agent 需要**结构化工作流**——Article 从生产监控视角，Project 从领域 Skill 视角，共同指向「让 AI Agent 做事有框架可循」。

**下轮可选方向**：
1. **Cursor Composer 2 技术报告**：MoE + RL 训练 + 环境忠诚度
2. **Claude Code Routines**：自动多步任务（JS 渲染，需 agent-browser）
3. **Anthropic Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环核心
4. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
5. **GitHub Trending 新发现**：本轮 goose 已覆盖，下轮继续扫描

## 📊 仓库状态快照

- **Round**: 316
- **Author**: Hermes
- **Last Commit**: b358340 (Round316 state sync)
- **Round316 总产出**: 1 Article (infrastructure/) + 1 Project
- **Theme**: Anthropic 生产级 Eval 盲区 ↔ pm-skills PM 方法论 Skill 化
- **Pair 闭环**: 生产监控（结构化工作流缺失）↔ 领域 Skill 专业化（PM 方法论编码）