# gstack: 把 Claude Code 变成虚拟工程团队

> Y Combinator CEO Garry Tan 开源了他的 Claude Code 配置——23 个 slash commands，将一个 AI 编程工具转变成包含 CEO、工程师经理、设计师、QA、安全审计员的完整虚拟工程团队。安装 30 秒，可用 23 个专业角色替代空白提示符。

---

## 核心命题

**一个人 + 正确的 agent 配置 = 一个工程团队的生产力**。Garry Tan 在 2026 年公开了他的 gstack 配置：用 23 个 slash commands 将 Claude Code 武装成多角色虚拟工程团队。2026 年截至 4 月，他的产出是 2013 年（一个人手动开发 Bookface）的 **240 倍**。这不是提示词工程，这是架构级别的角色系统设计。

---

## 为什么这个项目值得关注

### 真实的生产力数据

gstack 不是一个概念验证或 demo。Garry Tan 是 Y Combinator 的 CEO，他每天在运行 YC 的同时用 gstack 开发产品：

> "I don't think I've typed like a line of code probably since December, basically, which is an extremely large change." — Andrej Karpathy, March 2026

Garry Tan 的量化数据：
- **2026 年截至 4 月**：240× 2013 年全年产出（按逻辑代码变更量，而非原始 LOC）
- **2026 年运行速率**：约 810× 2013 年（11,417 vs 14 逻辑行/天）
- **最近 60 天**：3 个生产服务，40+ 已发布功能，兼职

> "The LOC critics aren't wrong that raw line counts inflate with AI. They are wrong that normalized-for-inflation, I'm less productive. I'm more productive, by a lot."

**笔者的判断**：这个数据最有说服力的部分不是"AI 让一个人做了更多事"，而是"AI 让一个人做了**不同类型**的事"。240× 的产出不是 240 个人在工作，而是一个人从"实现细节"中解放出来后专注于架构和产品决策。

### 23 个专业角色的设计逻辑

gstack 的核心不是 23 个命令，而是一套**角色体系**：

| 角色 | Slash Command | 职责 |
|------|--------------|------|
| **CEO** | `/plan-ceo-review` | 从产品方向视角评估功能决策 |
| **工程师经理** | `/plan-eng-review` | 从架构和工程管理视角审查 |
| **设计师** | `/design-consultation`, `/design-shotgun` | UI/UX 评估和设计方案 |
| **代码审查** | `/review` | PR review，发现生产 bug |
| **QA Lead** | `/qa` | 在 staging URL 上运行真实浏览器测试 |
| **安全官** | （OWASP + STRIDE 审计）| PR 级别的安全审计 |
| **发布工程师** | `/ship`, `/land-and-deploy`, `/canary` | 自动化发布和灰度策略 |
| **Benchmark** | `/benchmark` | 性能基准测试 |
| **办公时间** | `/office-hours` | 描述你在构建什么，获取结构化建议 |

> "It turns Claude Code into a virtual engineering team — a CEO who rethinks the product, an eng manager who locks architecture, a designer who catches AI slop, a reviewer who finds production bugs, a QA lead who opens a real browser, a security officer who runs OWASP + STRIDE audits, and a release engineer who ships the PR."

**笔者认为**：这个设计的聪明之处不是"有更多 agent"，而是**每个角色的提示词是独立设计的**，不是让一个通才 agent 扮演多个角色。`/plan-ceo-review` 的 prompt 和 `/plan-eng-review` 的 prompt 有完全不同的评估维度和专业视角。

### 与并行 Claude 研究的关联

Anthropic 的 [并行 Claude C 编译器研究](https://anthropic.com/engineering/building-c-compiler)（16 个 Claude 实例并行工作）揭示了多 agent 协作的三个核心工程挑战：

1. **持续工作能力**：Ralph-loop 的无限循环 Harness
2. **任务协调**：Git 锁文件防止冲突
3. **角色专业化**：不同 agent 负责不同维度

gstack 在**单 agent 层面**解决了同样的问题：不是通过并行化，而是通过**角色切换机制**。当你输入 `/review` 时，Claude 不再是"实现者"，而是"代码审查员"——提示词上下文发生了根本性转变。

**笔者的判断**：这两种路径（多 agent 并行 vs 单 agent 角色切换）并不矛盾。gstack 的角色设计可以看作是对 Claude Code 每次会话的"角色分配"，而并行 Claude 研究是在会话之间做并行化。未来的系统可能会结合两者：多个角色化 agent 并行工作。

---

## 技术实现

### 安装（30 秒）

```bash
# 克隆到 Claude Code skills 目录
git clone --single-branch --depth 1 \
  https://github.com/garrytan/gstack.git \
  ~/.claude/skills/gstack

cd ~/.claude/skills/gstack && ./setup
```

安装脚本会自动在 `CLAUDE.md` 中添加配置，启用所有 slash commands。

### 工作流示例

```
$ claude
> /office-hours
[描述你想构建的产品]

> /plan-ceo-review
[功能提案]

> /plan-eng-review  
[功能提案]

> /review
[已提交的 PR]
```

### 依赖

- Claude Code
- Git
- Bun v1.0+（Unix/macOS）或 Node.js（Windows）

---

## 局限性

gstack 是**高度个人化**的配置——它是 Garry Tan 的工作流，不是通用最佳实践：

1. **角色设计反映个人偏好**：CEO 视角、工程师经理视角都是 Garry Tan 的视角
2. **不适合纯新手**：需要理解每个角色的适用场景，否则会变成"功能叠加"而非"架构决策"
3. **Windows 支持不完整**：依赖 Bun，Windows 需要额外配置
4. **无并行能力**：仍然是单 agent，无法利用多 agent 并行研究的发现

---

## 适用场景

| 场景 | 适用度 |
|------|--------|
| 单人创始人/独立开发者 | ★★★ 极高 |
| 技术 CEO/CTO 兼职编码 | ★★★ 极高 |
| 小团队（2-5人）提升 Code Review 质量 | ★★ 高 |
| 大型团队 | ★ 有限（更适合集成到现有 CI/CD）|
| AI Coding 新手 | ★ 不推荐（先理解 agent 能力边界）|

---

## 与同类项目的对比

| 项目 | 类型 | Stars | 核心差异 |
|------|------|------|---------|
| **gstack** | Claude Code 配置 | 649 | 角色系统设计，个人工作流优化 |
| [anthropic/claude-code](https://github.com/anthropics/claude-code) | 官方 CLI | 153K | 官方标准工具 |
| [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | System prompts 集合 | 11K | prompt 优化，非角色系统 |

**gstack 的独特价值**：不是另一个"更好的 prompt"，而是一套**可组合的角色系统**。每个 slash command 不仅仅是预设的 prompt，而是具有独立思维模式和评估维度的专业角色。

---

## 引用来源

1. Garry Tan, "gstack: Use Garry Tan's exact Claude Code setup", GitHub Repository, 2026. https://github.com/garrytan/gstack
2. Garry Tan, "On the LOC Controversy", gstack Documentation, 2026.

---

*本文与《并行克劳德写 C 编译器：多智能体协作的工程机制实证》配对产出，关联主题：多 Agent 角色专业化工程机制。*
