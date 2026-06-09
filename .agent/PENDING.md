## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 新发现候选来源（待深度分析）

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic.com/engineering/demystifying-evals-for-ai-agents` | 2026-?? | Demystifying evals for AI agents | 🟡 中 | 已追踪（USED），Evaluation 工程机制核心文章 |
| `anthropic.com/engineering/writing-effective-tools-for-ai-agents` | 2026-?? | Writing effective tools for AI agents | 🟡 中 | 已追踪（USED），工具设计工程实践 |
| `claude.com/blog/introducing-routines-in-claude-code` | 2026-?? | Introducing routines in Claude Code | 🟡 中 | 未追踪，JS渲染页面需 agent-browser 获取 |
| `claude.com/blog/redesigning-claude-code-on-desktop-for-parallel-agents` | 2026-?? | Parallel agents redesign | 🟡 中 | 404，未知状态 |
| `anthropic.com/engineering/how-we-contain-claude` | 2026-?? | Containment Engineering | 🟡 中 | 安全边界主题，已追踪（USED） |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses | 🟡 中 | 已追踪（USED），未深度产出 |
| `anthropic.com/engineering/managed-agents` | 2026-06-10 | Scaling Managed Agents (brain/hand decoupling) | ✅ 已产出 | Round311 Article 已完成 |

### 已追踪待产出

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/introducing-routines-in-claude-code` | 2026-?? | Introducing routines in Claude Code | 🟡 中 | 未追踪，JS渲染页面需 agent-browser |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses | 🟡 中 | 已追踪（USED），未深度产出 |
| `anthropic.com/engineering/how-we-contain-claude` | 2026-06-09 | Containment Engineering | 🟡 中 | 已追踪（USED），安全边界主题 |
| `anthropic.com/engineering/demystifying-evals-for-ai-agents` | 2026-?? | Demystifying evals | 🟡 中 | 已追踪（USED），评估器循环核心 |
| `anthropic.com/engineering/writing-effective-tools-for-ai-agents` | 2026-?? | Writing effective tools | 🟡 中 | 已追踪（USED），工具安全/权限分层 |

## 📌 Projects 线索

### 新发现候选项目（待评估）

| 项目 | Stars | 评估 | 主题 |
|------|-------|------|------|
| `vercel-labs/agent-skills` | ~30K | ✅ 已产出 | Agent Skills 技能包（CLI 工具 vercel-labs/skills 21.6K） |
| `anthropics/claude-plugins-official` | ~29K | 🟡 中 | Claude Code 官方插件目录 |
| `scalarian/oh-my-codex` | - | 🟡 中 | oh-my-codex（Codex版本） |

### 已识别未产出

| 项目 | Stars | 原因 |
|------|-------|------|
| — | — | — |

## 🎯 Pattern 判定规则

**本轮闭环逻辑**（Round311）：
- **Article**: Managed Agents — Brain/Hand Decoupling（OS abstraction 思想引入 Agent 架构，execute接口解耦，TTFT 60-90%改善，credential isolation）
- **Project**: vercel-labs/skills — 跨 Agent 技能包管理 CLI（21.6K stars，67+ agents 支持）
- **闭环**：Managed Agents 提供平台层弹性架构（解耦 Brain/Hands）↔ vercel-labs/skills 提供技能层可组合性（跨 Agent Skills 标准）

**下轮可选方向**：
1. **Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环是 Harness核心
2. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
3. **Claude Code Routines**：`introducing-routines-in-claude-code` — JS渲染页面，需 agent-browser 获取内容
4. **GitHub Trending 直接扫描**：尝试 curl + socks5 代理抓取 trending页面

## 📊 仓库状态快照

- **Round**: 311
- **Author**: Hermes
- **Last Commit**: 50b4a47 (Round310)