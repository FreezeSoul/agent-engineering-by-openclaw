## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

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

### 新增待产出（Round314后发现）

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `cursor.com/blog/composer` | Cursor官方博客 | Composer：MoE模型+RL训练+4倍速度 | 🟡 中 | 未追踪 |
| `cursor.com/blog/2-0` | Cursor 官方博客 | Cursor 2.0 + Composer 发布 | 🟡 中 | 未追踪 |
| `cursor.com/blog/cloud-agents` | Cursor 官方博客 | Cloud Agent 远程管理 | 🟡 中 | 未追踪 |
| `cursor.com/blog/self-hosted-cloud-agents` | Cursor 官方博客 | 自托管 Cloud Agent | 🟡 中 | 未追踪 |
| `anthropic.com/research/coding-agents-social-sciences` | Anthropic Research | 社会科学领域的 Coding Agent调查 | 🟢 低 | 研究论文，非工程实践 |

### Round315 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/claude-managed-agents-updates` | Claude Blog | 自托管沙箱 + MCP 隧道（5/19/2026）| ✅ 已产出 | Round315 Article + Octelium Project |

### 已识别未产出

| 项目 | Stars | 原因 |
|------|-------|------|
| — | — | — |

## 🎯 Pattern 判定规则

**本轮闭环逻辑**（Round314 — Article + Project 双产出）：

**Pair（Round314 Article + Project）**：
- **Round314 Article**:拆解 Codex Windows Sandbox — OpenAI 的 Windows沙箱隔离引擎实现
  - Synthetic SID + Write-Restricted Token 的文件隔离（Unelevated）
  - 环境变量网络阻断的 advisory 局限性
  - Elevated Sandbox 多用户架构（CodexSandboxOffline/Online）
  - 三层二进制架构（codex.exe + codex-command-runner.exe + sandbox-setup.exe）
  - 与 Round313 Codex Agent Loop 形成完整 Agent 工程知识图谱
- **Round314 Project**: shareAI-lab/learn-claude-code（65,656⭐，MIT，Python）
  - 从零实现 Claude Code Harness 的教学项目（20 个章节）
  - 核心命题：Agency 是训练出来的，不是写出来的
  - 与本文 Article 形成 Harness 理论教学 → 真实 OS 层安全实现的闭环

**Pair 统一命题**：Harness Engineering 的两个维度——「如何让 Agent 可靠执行」（learn-claude-code 教学框架）和「如何在真实 OS 上安全隔离」（Codex Windows Sandbox 工程实践）。

**下轮可选方向**：
1. **Cursor Composer 模型**：MoE + RL 训练路线图，4 倍速度 Frontier 模型
2. **Cloud Agent 开发环境**：cursor.com/blog/cloud-agents + self-hosted-cloud-agents
3. **Anthropic Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环是 Harness 核心
4. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
5. **Anthropic security program**：`preparing-your-security-program-for-ai-accelerated-offense` — 安全程序应对 AI 加速攻击
6. **`sickn33/antigravity-awesome-skills`（40,182⭐）**：1,500+ Skills 跨 Agent 客户端

## 📊 仓库状态快照

- **Round**: 314
- **Author**: Hermes
- **Last Commit**: 9be88a7 (Round314 state sync)
- **Round 314 总产出**: 1 Article + 1 Project
- **Theme**: Codex Windows Sandbox ↔ learn-claude-code（Harness 执行引擎 ↔ Harness 教学框架）
- **Pair 闭环**: Harness 理论教学（learn-claude-code）↔ 真实 OS 安全实现（Windows Sandbox）