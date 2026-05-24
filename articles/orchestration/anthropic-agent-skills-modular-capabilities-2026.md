# Anthropic Agent Skills：模块化技能系统让通用 Agent 获得专业化能力

**核心论点**：Anthropic 通过 SKILL.md 标准将专业知识封装为可发现、可加载、可组合的技能单元，让通用 Agent 无需重新训练即可获得垂直领域 expertise。

**一手来源**：[Anthropic Engineering - Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（2025-10-16）

---

## 为什么技能封装是 Agent 工程化的关键

随着模型能力提升，通用 Agent（如 Claude Code）已能跨领域完成复杂任务。但**垂直领域的专业知识**仍然缺失——这不是模型能力问题，而是知识载体问题。

传统解法：

- 为每个垂直场景从头训练/微调专属 Agent（高成本、低复用）
- Prompt engineering（脆弱，难维护，上下文膨胀）

Anthropic 的新解法：**Agent Skills**——像「新人入职培训包」一样封装专业知识。

---

## SKILL.md 标准解析

一个 Skill 是一个目录，必须包含 `SKILL.md` 文件，文件开头必须是 YAML frontmatter：

```yaml
---
name: <skill-name>
description: <what this skill does>
---
```

`SKILL.md` 包含组织化的指令、脚本和资源，供 Agent 在运行时动态发现和加载。

### 工作原理

1. **启动时预加载**：Agent 启动时读取 name 和 description
2. **运行时按需加载**：当任务涉及某技能领域时，Agent 自动加载对应 SKILL.md
3. **技能组合**：多个 SKILL 可以组合，形成复合能力

### PDF Skill 示例

Claude 原本擅长理解 PDF，但无法直接操作 PDF（如填写表单）。PDF Skill 赋予 Claude 这些新能力——通过 SKILL.md 封装操作指令和资源，无需修改模型。

---

## 为什么这是工程突破

### 可组合性（Composability）

Skills 打破了「一个 Agent 一个专用场景」的设计惯性。任何人都可以通过捕获和分享程序性知识，将通用 Agent 变为专用 Agent：

```
通用 Claude → + PDF Skill → 能填写表单
通用 Claude → + Database Skill → 能操作 DB
通用 Claude → + Security Audit Skill → 能做安全审计
```

### 可移植性（Portability）

Anthropic 将 Agent Skills 作为**开放标准**发布（2025-12-18 更新），实现跨平台移植。这意味着一个团队开发的 Skill 可以分享给其他团队，其他 Agent 系统也可以实现兼容。

### 可发现性（Discoverability）

Agent 启动时预加载 Skills 的 name + description，使 Skill 发现成为运行时能力，而非静态配置。

---

## 工程启示

### 技能系统 vs. 工具系统

| 维度 | 工具系统（如 MCP） | 技能系统（Agent Skills） |
|------|-----------------|----------------------|
| 抽象层次 | 接口级（API） | 知识级（怎么用） |
| 组合方式 | 工具链 | 技能叠加 |
| 更新粒度 | 原子级 | 流程级 |
| 适用场景 | 通用操作 | 垂直专业 |

### 企业应用场景

- **NAB CEL**（CBA 用 Cursor Primitives 构建的内部上下文工程库）正是 Skills 模式的企业级实现——通过 rules、skills、hooks 集中共享知识，强制开发标准和 Agent 行为护栏。
- Skills 使「Agent 上岗培训」从提示词工程变为可版本化的知识包。

---

## 关联闭环

本文与以下项目/文章形成闭环：

- **[Cursor 3：统一工作空间](../articles/harness/cursor-3-unified-multi-agent-workspace-2026.md)**：Cursor 3 的 Plugin Marketplace 将成为 Skills 分发的核心渠道。Skills 的可组合性与 Cursor 3 的多 Agent 并行架构共同指向「专业化 Agent 舰队」。
- **[baguette - iOS 模拟器农场](../projects/tddworks-baguette-ios-simulator-farm-1007-stars-2026.md)**：baguette 提供 AI Agent 的测试环境基础设施。Skill 的测试需要真实设备模拟能力，baguette 解决了「在哪里测试」的问题。