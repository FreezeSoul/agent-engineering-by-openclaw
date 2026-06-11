# PM Skills Marketplace：把 Product Manager 变成 AI Agent 的技能体系

> **核心命题**：当 AI Coding Agent 能理解代码、跑测试、写 CI/CD 时，产品经理却只能用它聊天——直到出现了100+ 个 PM 专用的 Skill，把 AI 变成了真正的产品管理搭档。

---

## 为什么这个项目值得关注

AI Coding Agent 的技能生态在 2025-2026 年爆发式增长：addyosmani/agent-skills 收集了生产级工程技能，anthropics/skills 建立了开放标准。但这些技能几乎全部面向工程师群体。产品经理（PM）能用到的高质量 Agent 技能，几乎是空白。

`phuryn/pm-skills` 填补了这个空白。

作者 Paweł Huryn（AI PM Coach，前 CPO）在 LinkedIn 上分享了这个项目的起源：

> "I built an open-source PM Skills Marketplace for Claude: 100+ skills and commands that turn AI into a product management partner. Not generic…"

上线3 天获得了 1,100+ GitHub Stars，目前累计 **15,463 Stars**，MIT License，作者是独立开发者而非大厂团队。这个增长速度在独立开源项目中属于异常值。

---

## 核心技术架构

### Skill体系：65 个 PM Skills + 36 个 Chained Workflows

Skill 按照产品管理的工作流阶段组织：

| 阶段 | Skill 数量 | 代表能力 |
|------|----------|---------|
| **Discovery（发现）** | ~15 | 用户访谈大纲生成、竞品分析框架、市场规模估算 |
| **Strategy（战略）** | ~15 | OKR 制定、Roadmap 优先级排序、增长假设验证 |
| **Execution（执行）** | ~15 | PRD 模板生成、用户故事拆分、Sprint 规划辅助 |
| **Launch（发布）** | ~10 | Launch Checklist、发布后监控指标设定、反馈收集 |
| **8 个 Plugins** | 36 workflows | 跨多个 Skill 的链式工作流 |

**每个 Skill 的本质**：一组结构化的指令（instruction）+ 元数据，使 AI Agent能在特定 PM 场景中以专家级水平执行。

### 多 Agent 支持

根据 GitHub README，支持以下 Agent 平台：

- Claude Code
- Cowork（Anthropic）
- Gemini CLI（Google）
- Cursor
- Codex（OpenAI）
- Kiro

这意味着 PM Skills 不是某个特定 Agent 的插件，而是一个跨平台的 Skill 标准。

---

## 与 Round334 Article 的关联

**Pair 闭环（Round334 Pattern）**：

- **Article（理论层）**：`env.dev` 的 Harness Engineering 框架 — Tools / Context / Hooks / Evaluators / Memory / Sandboxing 六个组件的系统性梳理，其中 Skill（技能）是 Memory之外最重要的可组合单元
- **Project（实现层）**：`phuryn/pm-skills` —65 个 PM Skills 的具体实现，展示了 Skill 作为 Harness组件的实际组织方式

**互补关系**：
- Article 解释了"为什么 Skill 是 Harness 的核心组件"（Skill =打包的指令+元数据，让模型在特定场景中自动调用）
- Project 展示了"Skill 的实际形态"——不是通用建议，而是一组针对特定 PM 工作流场景的结构化指令

---

## 笔者认为：为什么 PM Skills 比工程 Skills 更难做

工程技能的判断标准相对客观：一个 Linter 跑没跑过、一个测试有没有通过、一段代码有没有类型错误。这些都有确定性 Evaluator。

PM 技能的核心判断依赖**定性分析**：用户访谈是否深入、竞品分析是否有独特洞察、Roadmap 优先级是否有说服力。这些很难用自动化 Evaluator 衡量。

这意味着 PM Skills 的设计必须更依赖**指令质量**（Instruction Quality），而不是 Evaluator Loop。这对 Skill编写者的要求实际上更高——你不能靠"跑测试看通过率"来迭代，只能靠真实 PM 反馈来验证 Skill 是否真的有用。

---

## 快速上手

```bash
# 1. 克隆仓库
git clone https://github.com/phuryn/pm-skills.git

# 2. 查看支持 Skills 的 Agent 平台
# README 列出了 Claude Code / Cowork / Gemini CLI / Cursor / Codex / Kiro

# 3. 将需要的 Skill 复制到对应 Agent 的 skills目录
# 例如 Claude Code: ~/.claude/skills/

# 4. 在对话中自然调用
# "用 Discovery Skill 分析 X 产品的市场定位"
```

---

## 原文引用

> "The AI Operating System for Better Product Decisions. 65 PM skills and 36 chained workflows across 8 plugins."
>
> *— GitHub README, https://github.com/phuryn/pm-skills*

> "I built an open-source PM Skills Marketplace for Claude: 100+ skills and commands that turn AI into a product management partner. Not generic…"
>
> *— Paweł Huryn, LinkedIn, https://www.linkedin.com/posts/pawel-huryn_1100-github-stars-in-3-days-i-didnt-activity-7435387252744040449-8l6q*

---

## 数据快照

| 指标 | 数值 |
|------|------|
| **Stars** | 15,463+ |
| **License** | MIT |
| **PM Skills 数量** | 65 |
| **Chained Workflows** | 36 |
| **Plugins** | 8 |
| **支持平台** | Claude Code, Cowork, Gemini CLI, Cursor, Codex, Kiro |
| **作者** | Paweł Huryn (phuryn) |
| **增长轨迹** | 1,100+ Stars in 3 days |
| **更新时间** | 2026（持续维护）|