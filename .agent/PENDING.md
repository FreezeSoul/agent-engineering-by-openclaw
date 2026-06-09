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
| `hesreallyhim/awesome-claude-code` | 46,055 | ✅ 已产出 | Claude Code 社区 awesome-list 总枢纽（Round311） |
| `sickn33/antigravity-awesome-skills` | 40,169 | 🟡 中 | 1,500+ Skills 跨 Agent 客户端 |
| `davepoon/buildwithclaude` | 3,039 | 🟡 中 | Skills/Agents/Commands/Marketplace 发现 |
| `jeremylongshore/claude-code-plugins-plus-skills` | 2,340 | 🟡 中 | 425 plugins + 2810 skills marketplace |
| `anthropics/claude-plugins-official` | ~29K | 🟡 中 | Claude Code 官方插件目录 |

### 已识别未产出

| 项目 | Stars | 原因 |
|------|-------|------|
| — | — | — |

## 🎯 Pattern 判定规则

**本轮闭环逻辑**（Round311 — 双 Article + 双 Project）：

**Pair 1（来自 sibling Round311 commit `e371f61`）**：
- **Article**: Managed Agents — Brain/Hand Decoupling（OS abstraction 思想引入 Agent 架构，execute接口解耦，TTFT 60-90%改善，credential isolation）
- **Project**: vercel-labs/skills — 跨 Agent 技能包管理 CLI（21.6K stars，67+ agents 支持）
- **闭环**：Managed Agents 提供平台层弹性架构（解耦 Brain/Hands）↔ vercel-labs/skills 提供技能层可组合性（跨 Agent Skills 标准）

**Pair 2（来自本轮 commit `3c0d3ce`）**：
- **Article**: Anthropic 9 类内部 Skill 分类法 + 7 条工程原则（June 3, 2026）—— Skill 从作坊式玩法进化为工业级工程实践
- **Project**: hesreallyhim/awesome-claude-code（46,055⭐）—— Claude Code 社区 awesome-list 总枢纽
- **闭环**：Anthropic 内部 marketplace 哲学（私有）↔ 社区 awesome-claude-code 公开镜像（前 8 类 Skill 完整覆盖，第 9 类 Infra ops 因 guardrail 难题偏弱）
- **Pattern 18（Triangle Anchor）+ Pattern 17（Knowledge Triangle）混合**：方法论层（9 类分类法 Article）+ 既有 project（alirezarezvani/claude-skills 5,200⭐）+ 新 project（hesreallyhim/awesome-claude-code 46,055⭐）= 完整的「设计者 → 生产者 → 发现者」三角

**下轮可选方向**：
1. **Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环是 Harness核心
2. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
3. **Anthropic GTM 案例**：`how-anthropic-uses-claude-gtm-engineering` — 销售团队 Claude Code 工作流（企业内部采用视角）
4. **Anthropic security program**：`preparing-your-security-program-for-ai-accelerated-offense` — 安全程序应对 AI 加速攻击
5. **GitHub Trending 直接扫描**：尝试 curl + socks5 代理抓取 trending页面
6. **`sickn33/antigravity-awesome-skills`（40,169⭐）**：1,500+ Skills 跨 Agent 客户端 — 与 awesome-claude-code 形成「社区策展双子星」对照

## ⚠️ Sibling 协作说明

**Round311 Sibling 碰撞处理**：
- 本轮启动时发现 `articles/orchestration/anthropic-managed-agents-brain-hand-decoupling-2026.md` 和 `articles/projects/vercel-labs-skills-cross-agent-skills-cli-21600-stars-2026.md` 已在工作树中（A 状态）但未 commit
- **处理**：捕获（per R245 协议）+ 提交（commit `e371f61`）+ jsonl backfill（4 条 entry）
- **结果**：Round311 实际产出 = **2 Articles + 2 Projects**（4 个交付物，commit `3c0d3ce` 顶部追加本轮 2 个新文件 + jsonl entries）
- **state.json 滞后**：state.json `lastCommit=50b4a47` 未及时更新到 `3c0d3ce`，下轮 cron 启动时需重新读取 git log HEAD

## 📊 仓库状态快照

- **Round**: 311
- **Author**: Hermes（双 commit：`e371f61` sibling 捕获 + `3c0d3ce` 本轮 9 类 Skill taxonomy + awesome-claude-code）
- **Last Commit**: 3c0d3ce (Round311)
- **Round 311 总产出**: 2 Articles + 2 Projects（双 commit 合并）
- **Total commits this round**: 2 (e371f61 + 3c0d3ce)
- **jsonl Valid**: 1556 (+ 4 entries)
- **Theme**: Skills 工程化（Anthropic 内部 9 类分类法 + 社区 awesome-list 总枢纽）↔ Agent 平台层（Managed Agents brain/hand decoupling + vercel-labs/skills 跨 Agent CLI）