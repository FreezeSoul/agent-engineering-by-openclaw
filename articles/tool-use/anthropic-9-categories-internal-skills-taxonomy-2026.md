# Anthropic 内部 Skills 的九大分类：从「文件系统即提示工程」看 Skill 工程的工业化范式

> 一句话总结：Claude Code 团队把所有内部 Skill 归类为 9 种类型，并用「文件系统即渐进式披露」「On-demand Hooks」「描述写给模型不写给人」等 7 条原则统一了 Skill 的生产、评估与分发标准——这标志着 Skill 从「作坊式玩法」进化为「工业级工程实践」。

## 标签

- `agent-skills` / `taxonomy` / `progressive-disclosure` / `claude-code` / `engineering-best-practices`

## 来源

- 原始博客：[Lessons from building Claude Code: How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills)
- 作者：Thariq Shihipar（Anthropic 技术员工）
- 日期：June 3, 2026
- 阅读时长：5 分钟
- 评分：5/5（实用性 5 / 独特性 5 / 时效性 5）——这是 Anthropic 第一次系统披露「数百个 Skill 是怎么分类的」，完整覆盖了 Skill 设计的所有工程问题

---

## 1. 核心主张

**Skill 不是 markdown 文件，是文件夹**——Anthropic 团队在使用 Claude Code 的过程中积累了几百个内部 Skill，他们在内部做了一次系统化梳理，发现这些 Skill 自然落入了 **9 种类型**，并且只有「贴合其中一种类型」的 Skill 才高效，跨多类型的「全能 Skill」反而让 Agent 困惑。

更重要的是，他们总结出了 7 条 Skill 设计原则和 3 条运营策略（描述写给模型、hooks 按需启用、市场化分发），整套方法论已经覆盖了 Skill 的「**设计 → 编写 → 评估 → 分发**」全生命周期。

> "Skills have become one of the most used extension points in Claude Code. They're flexible, easy to make, and easy to distribute. But this flexibility also makes it hard to know what works best."
> — Thariq Shihipar, Anthropic

**笔者的判断**：这篇文章最重要的地方不是 9 种分类本身，而是它回答了一个根本问题——**「什么是 Skill 的工程化」**。当 Skill 数量从 10 涨到 100 再到 1000，「靠个人灵感」是不可持续的；Anthropic 把这些隐性经验公开化，本质上是把 Skill 从「玩法」升级为「工程学科」。

---

## 2. 9 种 Skill 类型：一份完整的能力图谱

Anthropic 团队把所有内部 Skill 整理后发现，它们会自然落入下面 9 个类别中。

### 2.1 Library and API reference（库与 API 参考）

教 Agent 怎么正确使用一个库 / CLI / SDK。**这是 Skill 的「领域知识」形态**——把人类花几周踩坑才熟悉的「隐性子规则」打包给 Agent。

代表性 Skill：
- `billing-lib`：内部 billing 库的边界条件与陷阱
- `internal-platform-cli`：内部 CLI 包装的每个子命令 + 适用场景
- `sandbox-proxy`：组织出站网关（哪些 host 可达、`connection refused` 怎么调试、如何加白名单）

### 2.2 Product verification（产品验证）— 最有杠杆的类别

描述怎么测试 / 验证代码真的在工作。**Anthropic 明确说这是「对 Claude 输出质量影响最大」的 Skill 类型**。

代表性 Skill：
- `signup-flow-driver`：headless 浏览器跑注册→邮箱验证→引导流程，每步断言状态
- `checkout-verifier`：用 Stripe 测试卡驱动结账 UI，验证发票真的落入正确状态
- `tmux-cli-driver`：交互式 CLI 测试，需要 TTY 的场景

**关键技巧**：让 Claude 录视频记录输出，或者在每步强制程序化断言。

> "Verification skills have had the most measurable impact on Claude's output quality internally. It can be worth having an engineer spend a week just making your verification skills excellent."

### 2.3 Data fetching and analysis（数据获取与分析）

连接数据栈 / 监控栈的 Skill。包括**凭证、具体 dashboard ID、通用 workflow 模式**。

代表性 Skill：
- `funnel-query`：「该 join 哪些事件看注册→激活→付费」，外加那张「规范 user_id」表
- `cohort-compare`：对比两个 cohort 的留存/转化率，标记统计显著差异
- `grafana`：数据源 UID、集群名、问题↔dashboard 查找表
- `datadog`：字段参考（`@request_id` vs `trace_id`）、服务列表、metric 前缀约定

### 2.4 Business process and team automation（业务流程与团队自动化）

把重复 workflow 封装成一条命令。**通常比较简单，但可能依赖其它 Skill 或 MCP**。

代表性 Skill：
- `standup-post`：聚合 ticket tracker + GitHub 活动 + 上次 Slack → 格式化 standup，只输出 delta
- `create-<ticket-system>-ticket`：强制 schema（合法枚举值、必填字段）+ 创建后 workflow（ping reviewer、贴 Slack）
- `weekly-recap`：合并 PR + 关闭 ticket + 部署 → 格式化 recap

**关键技巧**：把历史结果存到 log 文件，让模型能基于上一次执行结果反思本次差异。

### 2.5 Code scaffolding and templates（脚手架与模板）

为特定功能生成框架 boilerplate。**尤其适合「自然语言需求不能完全用代码覆盖」的脚手架**。

代表性 Skill：
- `new-<framework>-workflow`：用你们的标注搭建新 service / workflow / handler
- `new-migration`：migration 文件模板 + 常见陷阱
- `create-app`：带 auth / logging / deploy config 的新内部 app

### 2.6 Code quality and review（代码质量与 review）

强制组织内代码质量的 Skill。**经常作为 hook 或 GitHub Action 自动运行**。

代表性 Skill：
- `adversarial-review`：拉一个 fresh-eyes subagent 来批评 → 实现修复 → 迭代到 findings 退化为 nitpick
- `code-style`：强制代码风格，特别是 Claude 默认做不好的风格
- `testing-practices`：怎么写测试、测什么

### 2.7 CI/CD and deployment（CI/CD 与部署）

帮助拉取、推送、部署代码。**可能引用其它 Skill 来采集数据**。

代表性 Skill：
- `babysit-pr`：监控 PR → 重试 flaky CI → 解 merge conflict → 开 auto-merge
- `deploy-<service>`：build → smoke test → 渐进流量 rollout（带错误率对比）→ regression 自动回滚
- `cherry-pick-prod`：隔离 worktree → cherry-pick → 冲突解决 → 带模板的 PR

### 2.8 Runbooks（运维手册）

接收一个症状（Slack thread / 告警 / 错误签名），多工具排查后产出结构化报告。

代表性 Skill：
- `<service>-debugging`：症状 → 工具 → 查询模式，映射你们高流量服务
- `oncall-runner`：抓 alert → 查常见嫌疑 → 格式化 finding
- `log-correlator`：给一个 request ID，从所有可能接触它的系统拉日志

### 2.9 Infrastructure operations（基础设施运维）

执行例行维护和运维流程。**有些涉及破坏性操作，最需要 guardrail**。

代表性 Skill：
- `<resource>-orphans`：找孤立 pod / volume → 发 Slack → soak period → 用户确认 → 级联清理
- `dependency-management`：组织内的依赖审批 workflow
- `cost-investigation`：为什么存储/egress 账单飙升，具体 bucket 与查询模式

### 2.10 9 个分类的元模式

把这 9 个分类并列起来看，会发现一个清晰的**梯度结构**：

| 分类 | 抽象层级 | 是否涉及破坏性操作 | Anthropic 标注的关键属性 |
|------|---------|------------------|-----------------------|
| Library / API 参考 | 文档 | ❌ | "最容易写" |
| Product verification | 验证 | ⚠️（可能修改测试 fixture） | **对质量影响最大** |
| Data fetching | 读取 | ❌ | 主要是凭证管理 |
| Business process | 编排 | ❌ | 强依赖其它 Skill |
| Code scaffolding | 生成 | ⚠️（创建文件） | "语言需求不能纯用代码覆盖" |
| Code quality | 强制约束 | ⚠️（自动改代码） | hook 化 |
| CI/CD | 执行 | ⚠️（生产部署） | 与其它 Skill 组合 |
| Runbooks | 排查 | ❌ | 强依赖知识结构化 |
| Infra ops | 执行 | ✅（删除 / 清理） | **最需要 guardrail** |

**这 9 个分类其实就是一套「Agent 能干的事」的完整覆盖图**——从「查阅」（1）到「生成」（5）到「修改」（6/7）到「破坏性运维」（9），清晰地把「Agent 可以执行的所有操作」分门别类。

---

## 3. 7 条 Skill 设计原则

在分类之后，文章给出了 7 条具体的 Skill 设计原则。这是真正把 Skill 从「手艺」变成「工程」的核心。

### 3.1 不要说显而易见的（Don't state the obvious）

Claude 已经会写代码，能读你的 codebase。**如果 Skill 只是复述 Claude 默认会做的事，它只增加 context，不增加价值**。

> 例外：以「知识」为主的 Skill，应该聚焦在「让 Claude 跳出默认思维」的信息。比如 Anthropic 内部的 frontend-design Skill 是工程师反复和客户迭代出来的——专门避免 Claude 默认使用的 Inter 字体和紫色渐变。

### 3.2 建一个「Gotchas」section

**任何 Skill 里信号密度最高的内容都是 Gotchas section**。

> "The highest-signal content in any skill is the Gotchas section. These sections should be built up from common failure points that Claude runs into when using your skill."

具体例子：

- 「subscriptions 表是 append-only。你想要的行是 version 最高的那行，不是 created_at 最近的。」
- 「API gateway 里这个字段叫 `@request_id`，billing service 里叫 `trace_id`。它们是同一个值。」
- 「Staging 在 Stripe webhook 没真正处理时也返回 200。要看 payment_events 拿真实状态。」

**关键洞察**：Gotchas 不是一次性写完的，是 Skill 上线后**随着 Claude 碰到新边缘 case 不断补全**的。

### 3.3 用文件系统和渐进式披露

**SKILL.md 指向其它文件，Claude 在需要时去读**。

> "You should think of the entire file system as a form of context engineering and progressive disclosure. Tell Claude what files are in your skill, and it will read them at appropriate times."

最简单形式：把详细函数签名和使用例子拆到 `references/api.md`。如果输出是 markdown，可以放 `assets/template.md` 让 Claude 复制使用。可以放整文件夹的 references、scripts、examples——它们都帮助 Claude 更有效工作。

### 3.4 避免过度约束（Avoid railroading Claude）

**Claude 一般会忠实遵循你的指令**——但正因为 Skill 复用度高，太具体的指令会反过来限制 Claude。

> "Give Claude the information it needs, but give it the flexibility to adapt to the situation."

具体做法：设置信息（如 Slack channel）让用户填进 `config.json`，而不是写死在 Skill 里。

### 3.5 描述写给模型，不写给人

**当 Claude Code 启动一个 session，它会构建所有可用 Skill 的 listing，Claude 扫描这个 listing 决定「这个请求有没有对应 Skill」**。

> "Which means the description field is not a summary, it's a description of when to trigger this skill."

具体做法：在 description 里包含**触发词**，比如 babysit 这个词就要写进 description 里。

### 3.6 用 On-demand Hooks

**Skill 可以包含仅在 Skill 被调用时激活、仅在该 session 期间生效的 hooks**。

具体例子：
- `/careful`——通过 PreToolUse matcher 拦截 `rm -rf`、`DROP TABLE`、`force-push`、`kubectl delete`。只在动 prod 时想用，常开会让人发疯
- `/freeze`——拦截所有非特定目录的 `Edit/Write`。调试时很有用：「我想加日志，但总是『顺手修了』无关代码」

### 3.7 存脚本，让 Claude 写代码

**给 Claude 最有杠杆的工具是代码**。给 Claude scripts 和 libraries，让 Claude 把 turn 消耗在 composition（决定下一步做什么）上，而不是 boilerplate 重构。

> "Giving Claude scripts and libraries lets Claude spend its turns on composition, deciding what to do next rather than reconstructing boilerplate."

具体例子：data-science Skill 里给一组 helper 函数，Claude 现场生成脚本就能回答「上周二发生了什么」。

---

## 4. Skill 的运营策略：3 条隐性规则

### 4.1 分发策略：repo（`.claude/skills`）vs. marketplace

**两种分发渠道**：
- 小团队跨少量 repo：把 Skill 检入到 repo（`./.claude/skills`）
- 规模化场景：建 Claude Code Plugin marketplace，用户上传安装

> "Every skill that is checked in also adds a little bit to the context of the model. As you scale, an internal plugin marketplace allows you to distribute skills and let your team decide which ones to install, as well as include a setup flow."

**关键权衡**：检入 repo 让所有人在所有 session 自动加载——**但每个 Skill 都消耗一点点 context**。规模上去之后，市场化分发成为必须。

### 4.2 Marketplace 治理：去中心化

**Anthropic 没有中心化团队决定哪个 Skill 进 marketplace**——而是有机生长：

1. 有人做了一个 Skill 想让人试用，丢到 GitHub sandbox 文件夹，在 Slack 等渠道点名
2. Skill 有了 traction（Skill owner 自评），就提 PR 进 marketplace

### 4.3 Skill 组合：靠名字引用

> "We don't have a marketplace-native dependency graph; skills reference each other by name, and the model invokes them if they are installed."

**局限**：marketplace 和 Skill 还没有原生依赖管理。如果你的 file upload Skill 和 CSV generation Skill 想联动，目前要靠「名字引用」+ 「确保对方已安装」。

### 4.4 测量：用 PreToolUse hook 记录 Skill 使用情况

Anthropic 用 PreToolUse hook 来**记录 Skill 使用情况**，从而：
- 找出热门 Skill
- 发现「undertrigger」（描述没让模型识别到该用）的 Skill
- 评估新 Skill 是否被合理调用

---

## 5. 与现有 Skills 系列文章的关系

仓库内已有的 Skills 系列文章：

| 文章 | 覆盖维度 | 与本文的关系 |
|------|---------|------------|
| `anthropic-agent-skills-progressive-disclosure-2026.md` | **架构原理**（三层渐进式披露） | 本文不重复架构层，专注**Skill 内容设计** |
| `compound-engineering-agent-knowledge-compounding-2026.md` | **知识沉淀**（compound engineering） | 本文不重提知识沉淀，专注**分类与工程化** |
| `openai-codex-skills-composition-paradigm-2026.md` | **OpenAI 范式**（composition） | 本文不对比 OpenAI，专注**Anthropic 内部实践** |
| `agent-skills-three-tier-progressive-disclosure-architecture-2026.md` | **三层架构详解** | 本文不展开三层细节，专注**Skill 类型的边界** |
| `addyosmani-agent-skills-production-grade-...md`（项目文件） | **Skill 实践**（工程师视角） | 本文**完全 Anthropic 官方视角**——是 Skills 系统的「设计者」视角 |

**本文不重复既有覆盖范围，本文的独特价值是**：
- **9 类 Skill 的完整边界图**（从「查阅」到「破坏性运维」）
- **7 条工程原则**（不说显而易见、建 gotchas section、用文件系统做渐进披露等）
- **3 条运营策略**（repo vs marketplace、去中心化治理、PreToolUse hook 测量）
- **9 个分类的元模式分析**——9 个分类本质上是「Agent 能干的事」的完整覆盖图

---

## 6. 一句话总结

> **Skill 是 Agent 时代的「包管理格式」——但包本身需要「按能力类型而非按工具栈分类」，并用「描述写给模型不写给人」「On-demand Hooks」「文件系统即渐进披露」这 7 条原则统一设计。Anthropic 内部 9 类 Skill 是 Agent Skills 工程化的第一份完整分类法。**

---

## 来源

- [Lessons from building Claude Code: How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills)（Thariq Shihipar, Anthropic, June 3, 2026）
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（既有）
- [Anthropic Agent Skills: Progressive Disclosure 架构](articles/tool-use/anthropic-agent-skills-progressive-disclosure-2026.md)（仓库内既有）

*本文属于「Skills 工程化」系列，分析 Anthropic 内部 Skill 设计的工程方法论与组织实践。*