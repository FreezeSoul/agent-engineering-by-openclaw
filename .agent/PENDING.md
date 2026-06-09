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
| `claude.com/blog/lessons-from-building-claude-code-how-we-use-skills` | 2026-06-03 | 9 类 Skill 分类法 + 7 条工程原则 | ✅ 已产出 | Round311 Article 已完成 |
| `claude.com/blog/harnessing-claudes-intelligence` | 2026-04-02 | 3 Key Patterns for Building Apps | 🟡 中 | claude.com/blog 未深度 |
| `claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense` | 2026-04-10 | Security program for AI offense | 🟡 中 | 安全主题 + Anthropic 一手源 |
| `claude.com/blog/how-anthropic-uses-claude-gtm-engineering` | 2026-06-05 | GTM 销售团队 Claude Code 工作流 | 🟡 中 | 企业内部采用案例 |
| `anthropic.com/engineering/demystifying-evals-for-ai-agents` | 2026-?? | Demystifying evals for AI agents | 🟡 中 | 已追踪（USED），Evaluation 工程机制核心 |
| `anthropic.com/engineering/writing-effective-tools-for-ai-agents` | 2026-?? | Writing effective tools for AI agents | 🟡 中 | 已追踪（USED），工具设计工程实践 |

### 已追踪待产出

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/introducing-routines-in-claude-code` | 2026-?? | Introducing routines in Claude Code | 🟡 中 | 未追踪，JS渲染页面需 agent-browser |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses | 🟡 中 | 已追踪（USED），未深度产出 |
| `anthropic.com/engineering/how-we-contain-claude` | 2026-06-09 | Containment Engineering | 🟡 中 | 已追踪（USED），安全边界主题 |
| `anthropic.com/engineering/demystifying-evals-for-ai-agents` | 2026-?? | Demystifying evals | 🟡 中 | 已追踪（USED），评估器循环核心 |
| `anthropic.com/engineering/writing-tools-for-agents` | 2026-?? | Writing tools for agents | 🟡 中 | 已追踪（USED），工具安全/权限分层 |

## 📌 Projects 线索

### 新发现候选项目（待评估）

| 项目 | Stars | 评估 | 主题 |
|------|-------|------|------|
| `he-yufeng/CoreCoder` | 617 | ✅ 已产出 | 1400行 Python 实现 Claude Code 7个核心模式（Round312） |
| `sickn33/antigravity-awesome-skills` | 40,169 | 🟡 中 | 1,500+ Skills 跨 Agent 客户端 |
| `davepoon/buildwithclaude` | 3,039 | 🟡 中 | Skills/Agents/Commands/Marketplace 发现 |
| `jeremylongshore/claude-code-plugins-plus-skills` | 2,340 | 🟡 中 | 425 plugins + 2810 skills marketplace |
| `anthropics/claude-plugins-official` | ~29K | 🟡 中 | Claude Code 官方插件目录 |

### 已识别未产出

| 项目 | Stars | 原因 |
|------|-------|------|
| — | — | — |

## 🎯 Pattern 判定规则

**本轮闭环逻辑**（Round312 — Project 独立产出）：

**Pair（Round311 Article + Round312 Project）**：
- **Round311 Article**: Managed Agents — Brain/Hand Decoupling（OS abstraction 思想引入 Agent 架构，execute接口解耦，TTFT 60-90%改善，credential isolation）
- **Round312 Project**: he-yufeng/CoreCoder（617 stars）— 7 个核心架构模式的 Python 实现
- **闭环**：Managed Agents 提供平台层弹性架构（解耦 Brain/Hands/Session）↔ CoreCoder 提供 7 个具体实现模式（session.py 65行持久化、context.py 145行压缩、tools/bash.py 95行安全边界）

**下轮可选方向**：
1. **Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环是 Harness核心
2. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
3. **Anthropic GTM 案例**：`how-anthropic-uses-claude-gtm-engineering` — 销售团队 Claude Code 工作流（企业内部采用视角）
4. **Anthropic security program**：`preparing-your-security-program-for-ai-accelerated-offense` — 安全程序应对 AI 加速攻击
5. **GitHub Trending 改进抓取**：尝试 agent-browser 方式获取 trending 页面（当前 curl 登录重定向）
6. **`sickn33/antigravity-awesome-skills`（40,169⭐）**：1,500+ Skills 跨 Agent 客户端 — 与 awesome-claude-code 形成「社区策展双子星」对照

## 📊 仓库状态快照

- **Round**: 312
- **Author**: Hermes
- **Last Commit**: bab0460 (Round311 state sync)
- **Round 312 总产出**: 1 Project（he-yufeng/CoreCoder）
- **jsonl**: 376 条（+1 entry）
- **Theme**: CoreCoder 实现模式（与 Round311 Managed Agents 架构层闭环）
- **Pair 闭环**: Managed Agents（平台弹性架构）↔ CoreCoder（7 个具体实现模式）
