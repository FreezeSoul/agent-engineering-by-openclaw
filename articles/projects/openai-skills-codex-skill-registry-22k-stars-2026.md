# OpenAI Skills：构建 Agent 时代的「技能市场」

> 核心命题：**当 Agent 能像人类一样发现、学习、使用技能时，工程团队的知识积累方式正在从「文档沉淀」转向「技能封装」**。

---

## 这个项目解决了什么问题

软件开发团队积累了大量的「隐性知识」：如何启动一个服务、如何配置 CI/CD、如何做代码审查——这些知识散落在文档、Slack、历史 PR 中，没有被结构化地复用。

OpenAI 的答案是：**把团队技能变成 AI Agent 可以发现的「技能包」**。

```
skills/
├── .system/          # 系统级技能，Codex 自动加载
│   ├── github-pr-review/
│   ├── read-file/
│   └── write-tests/
├── .curated/        # 精选技能，需要手动安装
│   ├── create-spec/
│   └── deploy-railway/
└── .experimental/   # 实验性技能
    └── create-plan/
```

每个技能包包含：
- **instructions.md** — 技能的使用说明和最佳实践
- **scripts/** — 可执行的辅助脚本
- **resources/** — 模板、配置文件等资源
- **LICENSE.txt** — 技能的许可证

---

## 核心设计：Skill 作为一等公民

这个项目的核心价值主张是：**Skill 是 AI Agent 的一等公民**。

什么意思？

传统上，我们把「流程」「规范」「最佳实践」写成文档，希望 AI 能从文字中理解。但现实是，**文档的表述方式决定了 AI 能否正确执行**——同一份规范，用「开发团队应该...」和「你必须...」的语气，AI 的执行效果可能完全不同。

OpenAI Skills 的设计思路是：**为 Agent 重写技能描述**，而不是简单地把人类文档喂给 AI。

```markdown
# Skill: GitHub PR Review

## When to use
<!-- 明确的触发条件 -->
When a teammate asks you to review a pull request, or when you notice new PRs in the repository.

## How to do it
<!-- Agent 可执行的步骤 -->
1. First, fetch the PR description and diff
2. Run `gh pr diff <number>` to see all changes
3. Check for: security issues, performance concerns, test coverage
4. Post review comments using `gh pr comment`
```

这种「面向 Agent 重写」的思路，是 Skill 范式的关键——**不是让 AI 读懂人类文档，而是写 AI 能直接执行的技能说明**。

---

## 安装和使用：3 行代码

```bash
# 在 Codex 中安装精选技能
$skill-installer gh-address-comments

# 或者安装实验性技能
$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/create-plan

# 安装后重启 Codex，新技能即可用
```

技能的发现和安装完全在对话中完成——不需要离开 IDE，不需要查阅 Wiki。

---

## 与工程角色转变的关联

这篇文章值得关注的根本原因：**它与我们在 [Anthropic 2026 Agentic Trends 报告解读](../fundamentals/anthropic-2026-agentic-trends-from-implementer-to-orchestrator-2026.md) 中讨论的「工程师成为编排者」高度相关**。

当工程师的核心工作变成「编排 AI 代理」时，他们需要一种方式把**自己的专业判断封装成 AI 可复用的能力**。Skill 就是这种封装机制的早期实现：

- 工程师定义「什么情况下用什么技能」
- 工程师定义「技能的执行步骤」
- 代理负责「按步骤执行」

这意味着**团队的知识积累方式正在发生变化**：从「写文档等别人读」到「写技能让 AI 直接用」。

---

## 适用场景

✅ **适合**：
- 团队有大量重复性开发流程（Code Review、PR 合并、部署）
- 希望把资深工程师的「经验判断」结构化给 AI
- 需要在团队内共享「AI 工作流」

❌ **不适合**：
- 高度创新的任务（没有经验可复用）
- 需要强上下文判断的复杂决策
- 非技术背景用户（技能仍然需要技术背景才能编写）

---

## 笔者的判断

OpenAI Skills 代表了一个重要的方向：**从「AI 辅助写代码」到「AI 执行完整工作流」的跃迁**。它的核心价值不是「让 AI 写代码更快」，而是**把团队的专业知识资产化、复用化**。

但目前这个项目仍然是**相对早期的实现**：
- 技能之间的依赖管理有限
- 技能版本的追踪和回滚机制缺失
- 社区技能的质量参差不齐

这些工程机制上的不足，正是 [Harness Engineering](../fundamentals/anthropic-harness-engineering-agent-loop-optimization-2026.md) 领域需要解决的问题。

---

## 参考来源

- [openai/skills - GitHub](https://github.com/openai/skills)（22,231 stars）
- [Agent Skills – Codex](https://developers.openai.com/codex/skills)（官方文档）
- [agentskills.io](https://agentskills.io)（Open Skill 标准）
