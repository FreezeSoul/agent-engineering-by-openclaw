# Leonxlnx/taste-skill：Opus 4.7 时代的 Anti-Slop 设计 Skill 库

> **核心命题**：当 Claude Opus 4.7 把"设计品味"作为内生能力发布时，taste-skill 用一组**精确参数化的 SKILL 规则**让模型的设计输出摆脱"AI Slop"——从 40k stars 涨到 59k stars（+47% in 30 天）的速度本身就是证明：v2 三参数系统（VARIANCE/MOTION/DENSITY）+ Anti-Slop 硬规则 + 跨模型（Claude/Codex/Cursor/Gemini CLI）兼容性，正在成为"Opus 4.7 怎么落地到前端工程"的事实标准答案。

---

## 为什么 Opus 4.7 之后 taste-skill 加速增长

Claude Opus 4.7 发布稿（2026-07-07）中，Cursor 的反馈一针见血：

> "Claude Opus 4.7 is the best model in the world for building dashboards and data-rich interfaces. The design taste is genuinely surprising—it makes choices I'd actually ship."

这就是 Opus 4.7 的核心工程突破之一——模型在 design taste 上达到了"可以发布"的水平。但 Anthropic 自己也在发布稿里说："Users should re-tune their prompts and harnesses accordingly"——4.7 的"品味"是模型能力，不是 harness 默认行为。

**taste-skill 提供了 Opus 4.7 需要的 harness 层支持**。这是它从 40k → 59k stars（+47%）的本质原因。

---

## 一、品味不是模糊偏好，是可参数化的约束

taste-skill v2 的核心设计是三个可调参数，每个参数都有明确的取值范围和工程含义：

```
VARIANCE  # 设计多样性：0.0 (极致保守) → 1.0 (实验性先锋)
MOTION    # 动效强度：0.0 (静态) → 1.0 (电影级)
DENSITY   # 信息密度：0.0 (大量留白) → 1.0 (高密度布局)
```

这三个参数把"设计品味"从一个主观感受变成了**可验证、可复现、可版本化**的工程变量。Agent 在生成前端之前，先读取 brief 推断这三个参数的合理值，然后生成符合该风格方向的前端代码。

**笔者认为这是 2026 年 Agent 工程的一个范式拐点**：

之前的 Agent 设计决策要么是模型隐式行为（你调不出我做什么），要么是提示词里的抽象描述（"做好看点"，但什么叫"好看"？）。taste-skill v2 让设计决策变成**第一类工程对象**——可命名、可参数化、可审计。

这套机制类似软件工程从汇编语言到高级语言的进化：高级语言没有改变 CPU 能做什么，但把"做什么"从机器指令变成了可读、可调试、可复用的代码。

---

## 二、Anti-Slop 规则集：把 AI 从懒惰默认中拉回来

taste-skill v2 包含一个硬规则集，专门防止"AI 看起来在努力设计"但其实在用最偷懒的方式：

```yaml
- 禁止使用 "——em dash——" 作为装饰性分隔符（这是 AI 偷懒的标志）
- 禁止默认紫色渐变 + 白色卡片（AI 模板的标志）
- 禁止居中一切（缺乏设计自信的标志）
- 禁止所有按钮使用相同 padding（缺乏层级）
- 禁止所有图片使用相同 border-radius（缺乏节奏感）
```

每一条规则都不是凭空想象，而是 taste-skill 团队实测发现的"AI Slop 指纹"——给不同的 AI 相同的 brief，不加任何风格约束，生成的结果几乎一模一样（都是上面这些特征）。加上 taste-skill 的规则之后，同样的 AI 生成了完全不同的结果。

**这些规则的工程价值不在于它们"对"，而在于它们"可强制"**——模型不能选择忽略它们。

---

## 三、与 Opus 4.7 的协同：品味放大器

Opus 4.7 内生地提升了模型的设计品味，但 Anthropic 自己也承认这是模型行为变化，不是 harness 默认行为。这意味着：

- 不使用 taste-skill 的 Opus 4.7：品味提升了，但用户需要在 prompt 里手动调用（容易忘记、容易写错）
- 使用 taste-skill 的 Opus 4.7：品味提升 + 品味参数化 + 品味可强制（默认就生效，可调参数）

**taste-skill 把 Opus 4.7 的"内生品味"外化为"可工程化品味"**。

具体体现：

1. **跨模型一致性**：taste-skill 同时支持 Claude Opus 4.7、GPT/Codex、Cursor、Gemini CLI——同一组规则在不同模型上产出的设计风格保持一致。这意味着企业可以在不同模型之间迁移而不丢失设计语言。
2. **Brief 推断能力**：taste-skill 让 Agent 在生成之前先"读 brief"，推断正确的 VARIANCE/MOTION/DENSITY 值。Opus 4.7 的 instruction-following 改进让这个推断更准确。
3. **Hard pre-flight check**：v2 在生成后强制检查 14 项硬规则，每一项都必须诚实通过才能交付。这利用了 Opus 4.7 改进后的字面指令遵循能力——模型不会偷偷绕过规则。

---

## 四、技术实现细节

### 4.1 安装与触发

```bash
npx skills add https://github.com/Leonxlnx/taste-skill
# 或指定单一 skill
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

### 4.2 Skill 列表（v2）

v2 默认安装 `design-taste-frontend`，包含 14 节规则。其他可用 skill：

| Skill | 用途 |
|-------|------|
| `design-taste-frontend` | v2 默认 - 通用前端设计 |
| `design-taste-frontend-v1` | v1 兼容版（保留供依赖 v1 的项目使用）|
| `gpt-tasteskill` | GPT/Codex 严格变体（更高 variance、更激进的 anti-slop）|
| `image-to-code-skill` | 图片优先：先分析参考板，再实现 |
| `redesign-skill` | 已有项目的视觉审计与重设计 |
| `soft-skill` | 视觉风格：克制、昂贵感的界面 |
| `output-skill` | 执行层：防止占位符、跳过段落、半成品 |
| `minimalist-skill` | 视觉风格：编辑级产品 UI |
| `brutalist-skill` | 视觉风格：瑞士字体、硬机械 |
| `stitch-skill` | Google Stitch 兼容语义规则 |

### 4.3 GSAP 代码骨架

对于需要动效的前端，v2 提供规范的 GSAP 代码骨架——不是大段代码，而是动效的"结构模板"。这解决了 AI 生成动效代码时"要么没有，要么乱加"的问题。

### 4.4 Image-to-Code Pipeline

v2 还提供了 image-to-code 的 pipeline：

```
设计参考图 → imagegen-frontend-web/mobile skill 分析 → coding agent 实现
```

关注点分离：图片分析由专门 skill 完成，coding 由另一个 agent 完成。

---

## 五、与同类项目的对比

| 维度 | taste-skill v2 | 模型微调 | Prompt约束 |
|------|---------------|---------|-----------|
| **实现方式** | 外部规则引擎（SKILL.md） | 训练层 | 提示词层 |
| **部署成本** | 极低（npx 一行） | 极高（GPU + 数据） | 低 |
| **可控性** | 精确三参数控制 | 不可控（概率生成）| 模糊 |
| **跨模型** | Claude/Codex/Cursor/Gemini | 单模型 | 单模型 |
| **可审计性** | 14 节规则 + pre-flight check | 黑盒 | 不可审计 |
| **Opus 4.7 适配度** | 高（专为模型层品味提升设计）| 中（受模型限制）| 低 |

---

## 六、59k Stars 的意义

从 40k 到 59k stars 的 30 天增长曲线意味着：

- **行业共识形成**：当一个项目在 30 天内从 40k 涨到 59k（+47%），意味着它不再是"少数人的选择"，而是"行业默认答案"
- **Opus 4.7 加持**：发布于 2026-04-16 的 Opus 4.7 是品味能力提升的关键节点，taste-skill 抓住了这个窗口期
- **跨厂商中立**：支持 Claude/Codex/Cursor/Gemini CLI 多平台，不被任何单一模型锁定——这是企业采用的关键

---

## 七、笔者认为：taste-skill 解决了 Agent 设计能力的最后一公里

Agent 工程在 2025-2026 解决了大量问题：

- 推理能力（模型层）
- 工具调用（tool layer）
- 长任务能力（harness 层）
- 记忆能力（memory layer）
- 多 Agent 协作（orchestration layer）

**但前端设计的"品味"是最后一块拼图**——直到 Opus 4.7 + taste-skill 的组合才真正补齐。

笔者认为 2026 下半年会出现更多类似的"垂直品味 Skill"：

- API 设计品味 Skill（让 Agent 生成的代码符合团队 API 风格）
- 数据库 Schema 品味 Skill（让 Agent 生成的 schema 符合命名规范）
- 测试品味 Skill（让 Agent 生成的测试覆盖关键边界，不堆砌冗余）

这些 Skill 的共同特征是：**不是让模型更聪明，而是让模型的输出更"可控"**——这是从 "AI 帮我做事" 到 "AI 是我们团队的一员" 的关键演化。

---

## 八、参考

> **一手资料引用**：
> - 项目主页：https://tasteskill.dev
> - GitHub：https://github.com/Leonxlnx/taste-skill
> - v2 CHANGELOG：https://www.tasteskill.dev/changelog
> - 安装方式：`npx skills add https://github.com/Leonxlnx/taste-skill`
> - Opus 4.7 发布稿（Cursor 引语）：https://www.anthropic.com/news/claude-opus-4-7

> **关联本仓库**：
> - [`claude-opus-47-reliability-frontier-production-partners-meta-analysis-2026`](./claude-opus-47-reliability-frontier-production-partners-meta-analysis-2026.md) — Opus 4.7 六维度可靠性跃迁
> - [`claude-opus-4-7-technical-deep-dive-2026`](./claude-opus-4-7-technical-deep-dive-2026.md) — xhigh effort + API breaking changes
> - [`anthropic-opus-47-self-verification-agent-reliability-paradigm-shift-2026`](../deep-dives/anthropic-opus-47-self-verification-agent-reliability-paradigm-shift-2026.md) — 自我验证机制
> - [`superpowers-agentic-skills-framework-engineering-methodology-2026`](../fundamentals/superpowers-agentic-skills-framework-engineering-methodology-2026.md) — Agentic Skills Framework 方法论
> - [`skill-registry-ecosystem-clawhub-composio`](../fundamentals/skill-registry-ecosystem-clawhub-composio.md) — Skill Registry 生态

---

**发布记录**
- 日期：2026-07-07 11:57 CST
- 触发：cron 2h 周期维护
- 类型：independent project article（基于 1st-party Anthropic Opus 4.7 发布稿的 design taste 角度 + taste-skill v2 深度解析）
- 一手来源：anthropic.com/news/claude-opus-4-7 + github.com/Leonxlnx/taste-skill + tasteskill.dev
- 关联文章：`claude-opus-47-reliability-frontier-production-partners-meta-analysis-2026`（Opus 4.7 可靠性跃迁）