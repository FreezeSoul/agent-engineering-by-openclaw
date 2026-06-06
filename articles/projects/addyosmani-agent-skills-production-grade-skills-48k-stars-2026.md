# addyosmani/agent-skills：让 AI Coding Agent 遵循工程师工作流的 48K Stars 项目

> 本文推荐 GitHub 上 48,576 Stars 的生产级工程技能库——它把资深工程师的工作流程、质量门禁和最佳实践封装成 SKILL.md，让 AI Agent 在开发周期的每个阶段都能遵循一致的标准。

## 核心命题

AI Coding Agent 的最大问题不是「能不能写代码」，而是「能否遵循工程师的工作流程和质量标准」。addyosmani/agent-skills 通过把 **7 条 slash commands + 23 个 SKILL.md** 打包成一个跨 Agent 的技能体系，让 Claude Code、Cursor、Gemini CLI、Windsurf、OpenCode、GitHub Copilot 等主流 AI Coding 工具都能遵循相同的工程规范。

---

## 一、项目概览

| 指标 | 值 |
|------|---|
| **Stars** | 48,576 |
| **License** | MIT |
| **语言** | Shell (78.6%), JavaScript (21.4%) |
| **支持 Agent** | Claude Code, Cursor, Gemini CLI, Windsurf, OpenCode, GitHub Copilot, Kiro, Codex |
| **技能数量** | 23 个（22 个生命周期技能 + 1 个元技能）|
| **创建者** | Addy Osmani（Google Chrome 团队工程经理）|

---

## 二、7 条 Slash Commands：映射开发生命周期

项目的核心设计是 **7 条 slash commands**，每条对应开发周期的一个阶段：

| Command | Phase | Key Principle |
|---------|-------|---------------|
| `/spec` | 定义要做什么 | Spec before code |
| `/plan` | 规划如何做 | Small, atomic tasks |
| `/build` | 增量构建 | One slice at a time |
| `/test` | 证明它能工作 | Tests are proof |
| `/review` | 审查后再合并 | Improve code health |
| `/code-simplify` | 简化代码 | Clarity over cleverness |
| `/ship` | 部署到生产 | Faster is safer |

这 7 条命令覆盖了一个完整的工程生命周期——不是「写代码然后测试」，而是「从 spec 开始，到 ship 结束」的闭环。

### 2.1 技能的触发机制

Skills 不仅可以通过 slash commands 手动触发，还能**自动激活**：

- **场景触发**：设计 API 时自动触发 `api-and-interface-design`；构建 UI 时自动触发 `frontend-ui-engineering`
- **Agent 自动识别**：Agent 根据当前工作上下文判断应该使用哪个 skill

这种「手动 + 自动」的触发机制，解决了「Agent 不知道该用哪个技能」的问题。

---

## 三、SKILL.md 格式：跨 Agent 的技能标准

### 3.1 格式结构

每个 Skill 是一个标准化的 SKILL.md 文件，包含：

```markdown
---
name: deploy
description: Deploy to production
version: 1.0.0
tags: [deployment, production]
---
# Deploy to Production

When the user asks to deploy, follow these steps:
1. Run tests: `npm test`
2. Build: `npm run build`
3. Deploy: `npm run deploy:prod`
4. Verify health endpoint
Always confirm with the user before deploying to production.
```

YAML frontmatter 定义元数据（名称、描述、版本、标签），主体是 Markdown 格式的指令。这种格式的优势：

1. **人类可读**：工程师可以直接读写
2. **机器可解析**：任何支持文本的 Agent 都能理解
3. **跨平台**：不绑定特定 Agent 实现

### 3.2 跨 Agent 支持

项目对主流 AI Coding Agent 的支持：

| Agent | 安装方式 |
|-------|---------|
| **Claude Code** | `/plugin marketplace add addyosmani/agent-skills` |
| **Cursor** | 复制 SKILL.md 到 `.cursor/rules/` |
| **Gemini CLI** | `gemini skills install https://github.com/addyosmani/agent-skills.git --path skills` |
| **Windsurf** | 添加 skill 内容到 rules 配置 |
| **OpenCode** | 使用 AGENTS.md 和 skill tool |
| **GitHub Copilot** | 使用 agents/ 中的 agent 定义 + `.github/copilot-instructions.md` |
| **Kiro** | 存储在 `.kiro/skills/` |
| **Codex / 其他** | 纯 Markdown，任意支持文本的 Agent 均可使用 |

> 笔者认为，SKILL.md 格式正在成为 AI Agent 技能描述的事实标准——它比 MCP 更轻量，比 system prompt 更结构化，比工具定义文件更人类友好。

---

## 四、23 个 Skills：覆盖完整开发周期

### 4.1 元技能

**[using-agent-skills](https://github.com/addyosmani/agent-skills/blob/main/skills/using-agent-skills/SKILL.md)**：元技能，用于判断应该使用哪个 skill，以及共享的操作规则。

### 4.2 生命周期技能（22个）

覆盖从「需求理解」到「生产部署」的完整周期：

| 技能 | 用途 | 触发场景 |
|------|------|---------|
| `interview-me` | 理解用户真正想要什么（而非他们以为自己想要的）| ask 模糊或不完整 |
| `idea-refine` | 精炼想法，找到核心价值 | 需求不清晰 |
| `api-and-interface-design` | API 和接口设计 | 构建 API 相关功能 |
| `frontend-ui-engineering` | 前端 UI 构建 | 构建 UI |
| `backend-engineering` | 后端服务构建 | 构建 API/微服务 |
| `test-architecture` | 测试架构设计 | 设计测试策略 |
| `performance-optimization` | 性能优化 | 性能问题 |
| `security-review` | 安全审查 | 涉及用户数据/权限 |
| `code-review` | 代码审查 | PR review |
| `debugging` | 调试技能 | bug 修复 |
| `refactoring` | 重构技能 | 代码改进 |
| `documentation` | 文档编写 | 需要文档 |
| `deploy` | 生产部署 | 部署任务 |
| `monitoring` | 监控与告警 | 生产环境 |
| `incident-response` | 事故响应 | 生产事故 |

### 4.3 质量门禁设计

每个 Skill 都内含**验证门禁**（verification gates）——不是只给出步骤，而是要求 Agent 在进入下一步之前必须通过验证：

```
Step 1: Run tests → 验证通过 → Step 2
Step 2: Build → 验证通过 → Step 3
...
```

这种设计防止 Agent「跳过步骤直接到结果」——这也是生产级 Agent 工程的核心要求。

---

## 五、与 LangChain Skills 的对比

| 维度 | addyosmani/agent-skills | LangChain Deep Agents Skills |
|------|-------------------------|------------------------------|
| **设计目标** | 工程师工作流程标准化 | Agent 能力按需加载 |
| **技能粒度** | 粗粒度（生命周期阶段）| 细粒度（单个工具能力）|
| **触发方式** | Slash commands + 场景自动触发 | Agent 决策后按需加载 |
| **验证门禁** | ✅ 内置 | ❌ 不内置 |
| **跨 Agent 支持** | ✅ 多 Agent | ❌ 仅 LangChain 生态 |
| **Stars** | 48,576 | N/A（框架非独立项目）|

> 笔者认为，两者解决的是不同层次的问题。LangChain Skills 解决「如何让 Agent 高效使用工具」，addyosmani/agent-skills 解决「如何让 Agent 遵循工程师的工作标准和质量门禁」。一个好的生产级 Agent 系统可能同时使用两者。

---

## 六、工程价值

### 6.1 为什么这个项目重要

48K Stars 说明了一个重要趋势：**AI Coding Agent 的价值不在于「能写代码」，而在于「能遵循工程标准」**。一个写得很烂但有完整测试和文档的代码，比一个写得很好但没有测试的代码更有价值。

addyosmani/agent-skills 把这个认知落地成一个可安装、可配置的技能系统——这是它区别于其他 AI Coding 工具的根本原因。

### 6.2 适用场景

- **企业级 AI Coding**：需要统一工程标准的团队
- **多 Agent 协作**：不同 Agent 需要遵循相同的质量门禁
- **AI Coding 工具选型**：正在评估 Claude Code / Cursor / Copilot 的团队

### 6.3 不适用场景

- **简单脚本任务**：不需要完整工程流程的场景
- **高度定制化工作流**：已有成熟内部规范的团队

---

## 七、结论

addyosmani/agent-skills 是 2026 年 AI Coding Agent 生态中最重要的基础设施之一。它通过 SKILL.md 格式和 7 条 slash commands，把资深工程师的工作流程和质量标准封装成可安装的技能系统。

> 笔者认为，这个项目的意义超越了工具本身——它代表了一种认知转变：**AI Coding Agent 的竞争焦点，正在从「模型能力」转向「工程流程遵循能力」**。谁能让 Agent 更准确地遵循工程师的标准，谁就能在生产级 AI Coding 市场中占据优势。

---

**引用来源**：
- [addyosmani/agent-skills - GitHub](https://github.com/addyosmani/agent-skills)
- [Claude Code installation guide](https://github.com/addyosmani/agent-skills#claude-code-recommended)
- [agentskills.io 规范](https://agentskills.io)