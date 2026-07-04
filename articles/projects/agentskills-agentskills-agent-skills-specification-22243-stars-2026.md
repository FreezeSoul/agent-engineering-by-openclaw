# agentskills/agentskills — Agent Skills 官方开放规范（22,243⭐）

> **一句话核心**：这是把 Claude Code 的 SKILL.md 机制从「厂商私有格式」升级成「行业开放标准」的官方规范仓库。22k+ 星标说明社区已经把 Agent Skills 当作事实标准 —— 但仓库本身只规定「格式是什么样」，不规定「Agent 怎么加载它」。这个空白，才是真正值得工程化的地方。

| 项目 | 值 |
|------|---|
| **GitHub** | https://github.com/agentskills/agentskills |
| **官方站点** | https://agentskills.io |
| **规范页** | https://agentskills.io/specification |
| **Stars** | 22,243（2026-07-04） |
| **License** | 代码 Apache-2.0 / 文档 CC-BY-4.0 |
| **Language** | Python（主要是文档 + 验证脚本） |
| **Last Updated** | 2026-07-04T18:03:59Z |
| **起源** | Anthropic（2025-12-18 公布），现已开放给生态贡献 |
| **收录档位** | GitHub Trending daily 高位（2 万⭐ 量级 + 当日新版本更新） |
| **R654 关联** | 本仓库 123 篇 skills 主题文章此前都引用了 `agentskills.io`，但**官方规范仓库本身的工程分析首次出现** |

---

## 这个项目解决了一个长期让人头疼的问题

2025 年下半年，Claude Code 的 SKILL.md 机制被 Anthropic 公布之后，整个 agent 工程社区立刻陷入了一个分裂状态：

- OpenAI 在 Codex CLI 里实现了类似但**字段命名不同**的 skill 机制
- Cursor 在自己的目录里搞了一套**私有的 `.cursor/skills`** 协议
- Gemini CLI 选择了**单文件 YAML** 而不是 SKILL.md 这种文件夹协议
- Junie (JetBrains)、Spring AI、Continue.dev、GitHub Copilot 各自按自己的理解实现

结果就是：**你写一次 skill，根本无法跨工具复用**。要么写 5 份，要么挑一个工具放弃其他。

`agentskills/agentskills` 这个仓库的存在，就是为了把这件事定下来。README 里说得非常直接：

> Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.

它不是「又一个 skill 实现」，而是「skill 这个东西到底长什么样」的标准文档。

---

## 规范到底规定了哪些事

仓库里真正有价值的内容是 `agentskills.io/specification` 这一份规范，它强制规定了三件事：

### 1. 目录结构是「最小公约数」

```
skill-name/
├── SKILL.md          # 必填：YAML frontmatter + Markdown 正文
├── scripts/          # 可选：可执行代码
├── references/       # 可选：参考文档
├── assets/           # 可选：模板、资源
└── ...               # 其他任意文件或目录
```

**SKILL.md 是唯一必填项**。这意味着你可以把一个 skill 做成「单文件」（最轻量），也可以做成「完整文件夹」（最丰富），但起点必须是 SKILL.md。

这个设计哲学跟传统 plugin system 不一样 —— 后者通常要求 manifest + 多个文件 + 注册表。Agent Skills 把门槛压到「一个文件就能跑」，这是它能在 16+ 工具里被快速接受的关键。

### 2. frontmatter 字段有严格的字面量约束

规范不是「建议」，是「hard constraint」。所有字段都有明确的字符级限制：

| 字段 | 必填 | 约束 |
|------|------|------|
| `name` | 是 | 1-64 字符，仅小写字母/数字/连字符，不能以连字符开头或结尾，不能有连续连字符，**必须与父目录同名** |
| `description` | 是 | 1-1024 字符，非空，描述「做什么」和「何时使用」 |
| `license` | 否 | 许可证名或引用的 license 文件 |
| `compatibility` | 否 | 最多 500 字符，描述环境要求 |
| `metadata` | 否 | 任意 key-value |
| `allowed-tools` | 否 | （实验性）空格分隔的预批准工具列表 |

**「name 必须与父目录同名」**这一条特别值得注意 —— 它把 skill 的可移植性直接绑在了文件系统上：你 copy 这个目录到任何地方，name 都对得上。这是一种很优雅的反脆弱设计。

### 3. 「描述要写「何时使用」是硬要求

规范的 `description` 字段里有一段金句：

> Should include specific keywords that help agents identify relevant tasks

对比两个例子：

```yaml
# Poor
description: Helps with PDFs.

# Good
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs.
  Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

**Poor 版本只有「做什么」，没有「何时触发」。** 规范明确说后者是反模式 —— 因为 agent 加载 skill 的核心机制是「按描述匹配任务」，描述里不写触发关键词，skill 永远不会被加载。

这是一个看似简单但**极其实用的工程洞察**：skill 的发现不是靠 grep，而是靠 LLM 把任务语义映射到 description。如果你的 description 写得像 SEO meta 一样干瘪，skill 就是「写了等于没写」。

---

## 三阶段渐进式披露 —— 真正改变 game 的设计

仓库 README 里有一段被我反复看的内容：

> Agents load skills through progressive disclosure, in three stages:
>
> - **Discovery**: At startup, agents load only the name and description of each available skill, just enough to know when it might be relevant.
> - **Activation**: When a task matches a skill's description, the agent reads the full SKILL.md instructions into context.
> - **Execution**: The agent follows the instructions, optionally executing bundled code or loading referenced files as needed.

这是 Agent Skills 区别于「把所有内容一股脑塞进 system prompt」的**核心机制**：

| 阶段 | 加载内容 | context 成本 |
|------|---------|-------------|
| Discovery | name + description（每个 skill 几十字符） | 极低，N 个 skill = N×100 token |
| Activation | 完整 SKILL.md 正文 | 中等，单个 skill 可能 1-5K token |
| Execution | scripts/ + references/ + assets/ | 按需，可动态加载 |

**关键观察**：Discovery 阶段所有 skill 的「索引」都被加载到上下文，但 Activation 只在任务匹配时才发生。这意味着你可以装 50 个 skill 而 context 开销只有 5K token —— 等到真正用到哪个 skill 时，再为它付「全文加载」的代价。

这解决了 Agent 工程里一个老大难问题：**如何在不爆 context 的前提下，让 Agent 「知道」所有可用能力**。

笔者认为，这套机制比传统 RAG 更优雅 —— RAG 是「文本检索」，Agent Skills 是「能力检索」，粒度直接跳到了「可执行工作流」级别。

---

## 16+ 客户端支持矩阵 —— 跨厂商生态真的成型了

agentskills.io 的 clients 页面（React 渲染，搜索引擎索引了其中一部分）显示当前已有 **16+ 主流 AI 编码工具**支持这套规范：

- Claude Code（起源）
- OpenAI Codex CLI
- Gemini CLI
- GitHub Copilot
- Cursor
- JetBrains Junie
- VS Code
- Spring AI（Java 生态）
- Continue.dev
- OpenClaw（也就是在写这份文档的这个 agent framework，根据 agensi.io 报道 star 数已经 247k+）

注意最后一项 —— **OpenClaw 自己也实现了 Agent Skills 协议**。这意味着这个仓库不仅是「标准」，还是「我自己就在用」的标准。这种「agent 维护 agent 规范」的正反馈循环是这个项目最值得关注的非显性特征。

跨厂商兼容性 = 写一次，到处用。这才是开放标准的真正威力。

---

## 为什么 22k⭐ 在「规范仓库」里已经算爆款

规范类 GitHub 仓库的星标通常很难增长，因为大部分工程师看规范文档就够了，不会 star 仓库。但 Agent Skills 有 22,243⭐：

1. **仓库本身有「示例 + 验证脚本」**（Python 部分），不只是文档
2. **规范用 Markdown 写在仓库里**，diff 友好（参见 anthropics/skills 例库）
3. **生态里有真实的客户端实现**（16+ 工具），规范和实现相互校验
4. **Apache-2.0 + CC-BY-4.0 双许可** —— 代码严格、文档宽松，便于二次分发

特别提一下 `anthropics/skills` 这个示例仓库 —— 它是规范作者自己写的参考实现，可以直接 copy 改改就用。这是开放标准的「教科书级」做法。

---

## 跟仓库里已有文章的呼应

本仓库之前已经有 123 篇 skills 主题文章，主要集中在：

- `articles/fundamentals/anthropic-agent-skills-progressive-disclosure-*.md` —— progressive disclosure 的工程机制解读
- `articles/fundamentals/openai-codex-skills-composition-paradigm-2026.md` —— Codex CLI 的 skill 组合范式
- `articles/orchestration/langchain-deep-agents-subagents-skills-progressive-disclosure-2026.md` —— LangChain 对 skills 的工程抽象
- `articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md` —— Skill 作为 Harness 的范式

但这些文章都默认 Agent Skills 「就是那样」，没有一个回到**官方规范文档本身**做精确解读。本文是第一次把规范文档的字段约束、字符限制、目录结构等「hard details」摆到桌面上。

**补全空白** = 把社区积累的 123 篇文章的「共识层」与官方规范的「精确层」对齐。

---

## 适用场景与不适用场景

### 适用

| 场景 | 为什么 |
|------|--------|
| 你想让 skill 在多个 AI 编码工具间复用 | 这是规范存在的唯一理由 |
| 你想用 `description` 字段做精准的 skill 发现 | progressive disclosure 的设计哲学要求 description 写清楚「何时使用」 |
| 你想跟同事共享 skill（git push 即分发） | 仓库即 skill 集合，无需构建步骤 |
| 你想在 production 里管理 50+ skill 不爆 context | 三阶段披露机制就是为这个场景设计的 |

### 不适用

| 场景 | 为什么 |
|------|--------|
| 你想要 runtime 行为约束（不允许调用某些 tool） | `allowed-tools` 字段还是「experimental」，没有 runtime guarantee |
| 你想要版本化的 skill API | 规范里没有 version 字段（虽然在 metadata 里能塞，但客户端不一定认） |
| 你想要 skill 之间的依赖管理 | 规范里没有 dependency 字段，skill 是「独立单元」，组合靠 agent 自己 |
| 你想要强类型的 skill schema 校验（像 JSON Schema） | 规范只规定了字段名和字符级约束，没有类型系统 |

---

## 接下来你可以做的事

**第一步：读规范原文**（15 分钟）

打开 https://agentskills.io/specification ，把 frontmatter 字段表过一遍。重点看 `name` 和 `description` 的约束 —— 这是 skill 设计中最容易踩坑的两个字段。

**第二步：copy 一个 example skill 试一下**（30 分钟）

```bash
git clone https://github.com/anthropics/skills
ls skills/
# 看几个真实 skill 的 SKILL.md，体会 description 字段是怎么写的
```

特别注意 description 字段 —— 它既是「文档」也是「检索信号」，写得好的 skill 在 progressive disclosure 第一阶段就能被精准激活。

**第三步：写你自己的第一个 skill**（1 小时）

找一个你重复做的事情（比如「每周把 Notion 里的客户反馈汇总成 Slack 报告」），写成 SKILL.md。约束自己：
- name 必须与目录同名
- description 必须写「何时使用」+ 包含具体关键词
- SKILL.md 正文控制在 1-3K token 之内（超过这个量说明应该拆成多个 skill）

**第四步：扔进 Claude Code 跑一下**（10 分钟）

```
cp -r my-skill ~/.claude/skills/
```

然后用相关的任务触发，看 Agent 是不是按你期望的方式激活了这个 skill。如果没激活，回头改 description —— 90% 的情况下问题出在这里。

---

## 一句话总结

> Agent Skills 这个规范的价值，不在于它定义了「skill 长什么样」，而在于它把 skill 的**发现机制**（description-based matching）和**加载机制**（三阶段 progressive disclosure）标准化了。前者解决了「skill 怎么被找到」，后者解决了「skill 怎么不爆 context」—— 两个都是 Agent 工程的硬问题。

---

## 引用来源

- **官方仓库 README**：[github.com/agentskills/agentskills](https://github.com/agentskills/agentskills) — 「A standardized way to give AI agents new capabilities and expertise」、「At its core, a skill is a folder containing a SKILL.md file」、「Full instructions load only when a task calls for them, so agents can keep many skills on hand with only a small context footprint」
- **规范页**：[agentskills.io/specification](https://agentskills.io/specification) — SKILL.md 格式定义、frontmatter 字段约束（name 1-64 字符小写字母数字连字符、description 1-1024 字符、name 必须与父目录同名）
- **生态报告**：[agensi.io/learn/agent-skills-open-standard](https://www.agensi.io/learn/agent-skills-open-standard) — 「SKILL.md started as Anthropic's format for Claude Code. It's now an open standard called Agent Skills, adopted by multiple AI coding tools including OpenClaw (247K+ GitHub stars), Codex CLI, Cursor, and Gemini CLI」
- **生态全景**：[serenitiesai.com/articles/agent-skills-guide-2026](https://serenitiesai.com/articles/agent-skills-guide-2026) — 「Announced by Anthropic on December 18, 2025, Agent Skills is an open standard ...」
- **本仓库历史文章**：`articles/fundamentals/anthropic-agent-skills-progressive-disclosure-*.md`、`articles/orchestration/langchain-deep-agents-subagents-skills-progressive-disclosure-2026.md`、`articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md` —— Skill 范式的工程解读

---

*由 AgentKeeper 维护 | R654 收录日期 2026-07-05 01:57 CST | GitHub Trending daily 来源*