# react-doctor：让 Agent 学会检查自己的 React 代码质量

> 「你的 Agent 写的 React 代码很烂。react-doctor 来抓它。」

---

## 核心命题

react-doctor 解决了一个实际问题：**当 Claude Code 或 Cursor 帮你写 React 组件时，你很难快速判断这段代码是否真的靠谱**。

传统的 code review 需要人工介入，而 react-doctor 做的事是：**把 React 组件的静态分析规则转化为 Agent 可理解的 skill，让 Agent 在提交前就能 catch 到常见问题**。

这个项目在发布后迅速积累了 10.6K Stars，说明社区对「Agent 写代码的质量保障」有强烈需求。

---

## 二、技术架构

### 2.1 作为 Skill 运行的 Agent Code Review

react-doctor 以 Claude Code skill（也支持 Cursor、Copilot、Cline 等 30+ 平台）的形式运行：

```
用户让 Agent 写一个 React 组件
    ↓
Agent 调用 react-doctor skill
    ↓
skill 对代码进行静态分析 + 运行时检测
    ↓
返回问题列表和修复建议
```

这不是一个需要你手动触发的工具，而是可以被 Agent 在工作流中自动调用的 skill。

### 2.2 覆盖的检测维度

根据 README，react-doctor 检测的问题包括：

| 类别 | 检测内容 |
|------|---------|
| **运行时错误** | 未捕获的异常、状态不一致、API 错误处理 |
| **React 最佳实践** | 缺失的 key、不必要的重渲染、hooks 规则违反 |
| **TypeScript 类型** | 类型错误、any 滥用、缺失 Props 类型定义 |
| **性能反模式** | 不必要的 useEffect、useMemo 缺失、过度重渲染组件 |
| **可访问性** | 缺失的 ARIA 属性、键盘导航问题 |
| **安全** | XSS 风险、危险的 innerHTML、敏感数据暴露 |

### 2.3 适配多个 Agent 平台

react-doctor 不绑定特定平台：

```bash
# Claude Code
claudeaude /install react-doctor

# Cursor
# 通过 Marketplace 安装

# 其他平台
# 通过 skill 市场安装
```

支持的平台：Claude Code, Codex, Gemini, Cursor, Windsurf, Cline, Copilot, 30+。

---

## 三、为什么 10.6K Stars

### 3.1 刚需场景

React 是现代前端开发的主流框架，但 React 代码的质量问题往往是隐性的——功能上看起来正常，但在边界条件下会出问题，在大规模应用中会成为性能瓶颈。

Agent 写的代码尤其如此：因为 Agent 倾向于生成「能跑就行」的代码，对最佳实践的关注不够。

react-doctor 填补了这个空白：**在代码提交前自动 catch 问题，而不是等用户发现**。

### 3.2 Skill 形式的优势

把 code review 做成 skill 而非独立工具是正确的设计：

1. **Agent 可以在工作流中自动调用**，无需用户手动触发
2. **跨平台兼容**，30+ 平台都能用
3. **轻量集成**，不需要改变现有开发流程

### 3.3 与 Claude Code 的协同

Claude Code 擅长写代码，但写完后的质量保障需要额外工具。react-doctor 正好填补这个空白：

```
Claude Code 写代码 → react-doctor 检查 → 发现问题 → Claude Code 修复
```

这是一个「生成-检查-修复」的闭环，也是 multi-agent 协作的雏形。

---

## 四、与 Cursor 的 Keep Rate 指标对照

Cursor 在「Continually improving our agent harness」文章中提出了 **Keep Rate** 指标：**Agent 生成的代码在用户代码库中保留的比例**。

Keep Rate 度量的是「最终结果」，但 react-doctor 度量的是「过程中的质量」。

两者结合使用：
- **react-doctor**：在代码生成过程中实时 catch 问题，减少生成低质量代码
- **Keep Rate**：在代码提交后追踪用户是否需要手动调整，评估整体质量

这是两种不同维度的质量保障：**预防性检测 vs 结果性追踪**。

---

## 五、实测数据

根据 README 提供的 benchmark 数据（来源：[getcaveman.dev](https://getcaveman.dev)）：

> Raw data and reproduction script: benchmarks/. Three-arm eval harness (baseline / terse / skill) lives in evals/ — caveman compared against Answer concisely. not against verbose default, so the delta is honest.

benchmark 数据覆盖了多种任务类型，包括：
- Explain React re-render bug
- Fix auth middleware token expiry
- Set up PostgreSQL connection pool
- Docker multi-stage build
- Debug PostgreSQL race condition

---

## 六、工程启示

### 6.1 Skill 的粒度设计

react-doctor 的成功说明了一个设计原则：**skill 应该解决一个具体问题，而不是做一个通用的工具**。

它的边界很清晰：
- 只针对 React 代码
- 只做 code review
- 只在 Agent 工作流中运行

这种专注让它更容易集成，也更容易维护。

### 6.2 与通用 Agent 的互补

通用 Agent（如 Claude Code、Cursor）在代码生成上很强，但缺乏对特定领域的深度检测能力。Skill 模式填补了这个空白：**通用做生成，Skill 做检测**。

### 6.3 从「人 review」到「Agent review」

传统的 code review 需要人工介入，节奏慢、成本高。react-doctor 代表了一种新范式：**Agent review Agent**，用 AI 来保障 AI 生成代码的质量。

这在多人协作的大型项目中尤其有价值：减少人工 review 的负担，同时保持质量标准的统一。

---

## 七、快速上手

```bash
# 安装（Claude Code）
claudeaude /install react-doctor

# 在 Agent 中自动调用
# Agent 写完代码后，会自动运行 react-doctor skill 进行检测

# 或手动触发
claudeaude /review
```

---

## 八、与本轮 Article 的闭环

**Article**：Cursor 如何量化 Agent 的进化质量（Keep Rate + 三层测量体系）

**Project**：react-doctor — Agent 写 React 代码时的实时质量检测 Skill

**闭环**：
- Cursor 讨论的是「如何量化 Agent 输出质量的整体系统」
- react-doctor 提供的是「特定领域（React）的具体检测 Skill」
- 两者结合：整体量化 + 领域检测 = 完整的 Agent 质量保障体系

---

*关联阅读*：
- [Cursor 如何量化 Agent 的进化质量：从 Keep Rate 到自动化软件工厂](./cursor-harness-three-layer-measurement-keep-rate-2026.md) — 三层测量体系的完整解析