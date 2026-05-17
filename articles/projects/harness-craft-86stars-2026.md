# Harness-Craft：把「技能」打包成 AI Coding Agent 的可复用模块

> **核心问题**：当你的团队有 10 个 Developer，每个人的 AI Coding Agent 配置都不同——有人用 Claude Code，有人用 Cursor，有人自己组合框架——如何让「经过验证的技能」（如 TDD、代码审查、安全扫描）能够跨 Agent 复用，而不是每次都重复发明轮子？

> **读完能得到什么**：理解 Harness-Craft 的模块化技能体系（repo memory、long-horizon execution、multi-agent coordination、TDD、security review、delivery automation）、它与官方 Harness 的设计思路差异，以及在什么场景下值得集成。

---

## 让人想试的那个点

Harness-Craft 解决了一个实际存在但很少被认真对待的问题：**AI Coding Agent 的技能碎片化**。

每个有经验的 Agent 开发者都知道，好的 AI Coding 不是靠「选对模型」就能解决的。你需要：
- 让 Agent 理解项目的技术栈和约定（repo memory）
- 让 Agent 能够完成跨越多天的长周期任务（long-horizon execution）
- 让多个 Agent 能够协作而非重复工作（multi-agent coordination）
- 让 Agent 在写代码之前先写测试（TDD）
- 让 Agent 在部署之前先做安全扫描（security review）

问题是：这些能力通常被硬编码在特定的 Agent 配置里，换一个 Agent 就失效了。Harness-Craft 把这些能力拆出来，变成**可插拔的 Skill 模块**。

> 原文描述：
> *"A composable library of skills and rules for AI coding agents. Covers repo memory, long-horizon execution, multi-agent coordination, TDD, security review, and delivery automation."*

---

## 技术原理

### 核心概念

Harness-Craft 围绕「Skill」构建。每一个 Skill 是一个独立的模块，包含：

1. **触发条件（Trigger）**：什么情况下这个 Skill 应该被激活
2. **执行规则（Rules）**：Agent 在这个 Skill 激活时应该遵循的行为规范
3. **上下文管理（Context）**：Skill 需要什么样的上下文信息才能正确执行

这种结构的好处是：**Skill 是可组合的**。你可以在同一个项目里同时启用 TDD Skill + Security Review Skill + Delivery Automation Skill，它们各自独立工作，按配置的顺序级联。

### 与其他方案的对比

| 维度 | Claude Code 内置 Skill | Harness-Craft | Cursor Rules |
|------|---------------------|---------------|-------------|
| **模块化** | 插件式，但绑定 Claude Code | 框架无关，JSON/YAML 配置 | 基于规则的配置系统 |
| **TDD 支持** | Frontend Design Skill | ✅ 原生支持 | ❌ 无专项支持 |
| **Long-Horizon** | 依赖 Context Reset | ✅ 原生支持 | ❌ 无专项支持 |
| **Multi-Agent** | Subagent 支持 | ✅ 原生支持 | ⚠️ 仅 Session 级 |
| **Security Review** | MCP 安全扫描 | ✅ 原生支持 | ⚠️ 需手动配置 |
| **学习成本** | 低（官方 Skill 文档完整） | 中（需要理解配置体系） | 低（基于自然语言规则）|

---

## 适用场景

**适合用 Harness-Craft 的场景**：
- 团队内部有多个 AI Coding Agent 配置，需要统一「最佳实践」
- 你的项目需要 TDD 作为质量门禁，但不想自己写完整的 TDD prompt
- 你在构建企业级 AI Coding 平台，需要一个可配置的技能层
- 长周期任务（跨天/跨周）的上下文管理对你来说是痛点

**不适合用 Harness-Craft 的场景**：
- 你只需要简单的「写代码」功能，不需要复杂的技能体系
- 你的 Agent 已经有完善的配置，团队满意度高
- 你需要的是 GUI 化的配置界面，而不是配置文本

---

## 快速上手

```bash
# 安装
pip install harness-craft

# 查看可用 Skills
harness-craft list

# 启用 TDD Skill
harness-craft enable tdd --project /path/to/your/project

# 启用 Security Review Skill  
harness-craft enable security-review --strict

# 查看 Skill 配置
harness-craft config show tdd
```

---

## 笔者的判断

### 值得关注的点

**1. Skill 的可组合性是核心价值**

真正让 Harness-Craft 有别于「一堆好用的 prompt」的是可组合性。当 Skill 能够按配置的顺序级联时，你可以构建复杂的流水线：TDD → Security Review → Delivery Automation，每个 Skill 独立验证，失败即停。

**2. Long-Horizon Execution 的模块化封装**

大多数团队在处理长周期任务时会把逻辑硬编码在 Harness 脚本里。Harness-Craft 把这个能力提取出来，变成了可插拔的模块。这对平台化 AI Coding 能力很有价值。

**3. 与 Anthropic 三代理架构的关联**

Anthropic 在「Harness Design for Long-Running Apps」中描述的三代理（Planner/Generator/Evaluator）模式，在 Harness-Craft 中有隐式的对应：TDD Skill 对应 Evaluator 的测试验证，Security Review Skill 对应安全边界检查，Delivery Automation Skill 对应最终的 Deploy 检查。

如果你的团队已经在用 Anthropic 的三代理架构但还没有工具化，Harness-Craft 可能是把这套流程标准化的一种路径。

### 警告

**Stars 只有 86，质量待验证**。这个项目目前 Stars 很低，说明要么是新项目（社区还未充分验证），要么是场景过于垂直（企业级配置管理）而未被广泛采用。在生产集成前，建议先在非关键路径项目中验证。

**文档有限**。目前 GitHub README 内容较短，详细的配置文档和 API 接口说明需要进一步探索。如果你的团队没有配置管理经验，可能需要额外的时间来理解 Skill 的配置模型。

---

## 关联阅读

- [Anthropic 三代理架构：GAN 风格的长周期应用开发 Harness 设计](./anthropic-gan-inspired-three-agent-architecture-long-running-apps-2026.md) — Generator/Evaluator 模式
- [Anthropic Auto Mode：Managed Agents 的 Harness 演进](../harness/anthropic-auto-mode-managed-agents-harness-evolution-2026.md) — 权限分层设计
- [OpenAI Codex Windows 沙箱架构分析](../harness/openai-codex-windows-sandbox-architecture-2026.md) — 安全边界设计

---

**源**: [GitHub YuxiaoWang-520/harness-craft](https://github.com/YuxiaoWang-520/harness-craft) | **Stars**: 86 | **语言**: Python