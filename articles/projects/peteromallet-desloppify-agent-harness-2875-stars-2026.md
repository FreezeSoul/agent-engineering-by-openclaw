# Desloppify: Agent Harness 让"烂代码"变成"可维护代码"

> 本文属于 AI Coding Agent 工具生态推荐，与 Cursor 3 的"Agent Runtime Platform"战略形成工具链互补。

## 核心命题

**Desloppify 是一个专门给 AI Coding Agent 用的代码质量改善 Harness**——它不替代 Agent，而是给 Agent 一个可持续执行的质量改善循环：检测 → 计划 → 修复 → 评分，直到达到预设的代码质量分数。

```
笔者认为，Desloppify 解决了一个长期被忽视的问题：AI Coding Agent 生产代码很快，但代码质量会随时间劣化。Desloppify 让 Agent 有能力"看到"自己的代码质量，并主动改善它。
```

## 项目信息

| 项目 | 值 |
|------|------|
| **GitHub** | [peteromallet/desloppify](https://github.com/peteromallet/desloppify) |
| **Stars** | 2,875（2026-05-28） |
| **License** | 未声明 |
| **语言** | Python 3.11+ |
| **PyPI** | `desloppify[full]` |
| **支持语言** | 29 种（深度支持 TS/Python/C#/C++/Dart/Go/Rust，通用 linter + tree-sitter 支持 18 种）|

![GitHub](screenshots/desloppify-20260529.png)

## 为什么值得关注

### 1. 机械检测 + 主观 LLM 评审双轨制

Desloppify 的代码质量评估有两层：

- **机械检测层**：死代码、重复、复杂度等可直接量化的指标
- **LLM 主观评审层**：命名、抽象层次、模块边界等需要语义理解的判断

README 原文：

> "It combines mechanical detection (dead code, duplication, complexity) with subjective LLM review (naming, abstractions, module boundaries), then works through a prioritized fix loop."

```
笔者认为，这种双轨设计非常聪明：机械检测提供了客观基准，LLM 评审解决了代码风格无法硬性量化的部分。两者结合才能真正评估"代码质量"而不只是"代码规范"。
```

### 2. 状态跨会话持久化——多轮改善而非一次性修复

大多数代码改善工具只运行一次。Desloppify 的状态持久化在 `.desloppify/` 目录中，跨扫描轮次保留进度：

> "State persists across scans so it chips away over multiple sessions"

这意味着 Agent 可以：
- 第一轮：识别出 50 个质量问题
- 第二轮：从上次中断的地方继续，不重复工作
- 持续多轮，直到达到目标分数

```
笔者认为，这个设计让 Desloppify 真正成为一个"长周期任务管理工具"，而不是一次性扫描器。这与 Anthropic Harness 设计中的"checkpoint + progress file"机制在工程层面是异曲同工的。
```

### 3. 防作弊评分机制

> "The scoring resists gaming — the only way to improve it is to actually make the code better."

Desloppify 的质量评分不是为了"看起来好"，而是真正衡量代码可维护性。评分系统设计成无法通过投机取巧提升，必须真正改善代码才能提高分数。

### 4. 主流 AI Coding Agent 全支持

支持 Agent 列表：Claude Code, Cursor, Codex, Copilot, Droid, Windsurf, Gemini, Rovodev。

Agent 只需安装对应 skill：

```bash
pip install --upgrade "desloppify[full]"
desloppify update-skill claude    # 安装 Claude Code 工作流指南
```

## 与 Cursor 3 的主题关联

**Cursor 3** 构建的是"多 Agent 协作平台"——让多个 Agent 在同一个代码库中并行工作。**Desloppify** 解决的则是"多轮工作后的代码质量维持"问题。

两者形成了工具链的互补：

| 工具 | 解决的问题 | 层面 |
|------|-----------|------|
| **Cursor 3** | 多 Agent 协作 / 工作区状态管理 | 编排层 |
| **Desloppify** | 代码质量持续改善 / 长周期维护 | 执行层 |

```
笔者认为，Cursor 3 的 Multi-Agent 工作区会自然产生"代码风格不一致"和"技术债累积"问题。Desloppify 恰好是解决这个问题的工具——它是 Cursor 3 的质量守护层。
```

## 技术架构

### 核心工作流

```
扫描 (.desloppify scan) → 评分 (strict score) → 执行循环 (desloppify next) → 修复 → 评分提升
```

`next` 命令是核心执行循环：
- 告诉 Agent 现在该修复哪个文件
- 提供具体的 resolve 命令
- 修复完成后继续下一个

### 支持的语言深度

| 级别 | 语言 |
|------|------|
| **深度支持** | TypeScript, Python, C#, C++, Dart, GDScript, Go, Rust |
| **通用支持** | Ruby, Java, Kotlin 等 18 种（通过 linter + tree-sitter）|
| **特殊路径** | C++：`compile_commands.json` 或 Makefile 本地包含扫描 |

### 集成方式

**方式一：安装 skill（推荐）**
```bash
desloppify update-skill claude
```

**方式二：手动提示词**（README 内置的标准提示词）
```
I want you to improve the quality of this codebase. To do this, install and run desloppify.
...
```

**方式三：Proxy 模式**（即将推出，对已有 harness 的 Agent 透明增强）

## 适用场景

**适用：**
- 代码库质量持续劣化（多 Agent 协作、长期项目迭代）
- 需要给 AI Coding Agent 一个"质量改善目标"
- 多轮改善而非一次性修复

**不适用：**
- 需要立即修复的单次场景（传统 linter 更合适）
- 非 AI Coding Agent 使用的代码审查（Desloppify 是给 Agent 用的工具）

## 竞品对比

| 工具 | 定位 | 适用场景 |
|------|------|---------|
| **Desloppify** | AI Coding Agent 的质量改善 Harness | 多轮 Agent 工作后的代码质量维持 |
| **Traditional Linters** | 静态分析工具 | 单次检查，快速反馈 |
| **CodeRabbit / CodeGuru** | 代码审查平台 | 人工审查辅助 |
| **Cursor Agent** | 编码执行层 | 编码本身，依赖 Agent 自身质量意识 |

```
笔者认为，Desloppify 填补了一个空白：大多数 AI Coding 工具关注"写代码的速度"，但没有工具关注"代码质量的长期维护"。Desloppify 是第一个真正为 AI Agent 设计的长周期质量改善工具。
```

## 快速上手

```bash
# 1. 安装
pip install --upgrade "desloppify[full]"

# 2. 安装 Agent skill（以 Claude Code 为例）
desloppify update-skill claude

# 3. 初始化项目（排除 vendor/build 等目录）
desloppify exclude vendor build generated worktrees

# 4. 首次扫描
desloppify scan --path .

# 5. 开始改善循环
desloppify next
# 修复 → resolve → next → 修复 → resolve → next → ...
```

## 限制与注意事项

1. **Python 3.11+ 必需**：不支持旧版 Python
2. **状态目录**：`./desloppify/` 应加入 `.gitignore`，包含本地状态不应提交
3. **C++ 特殊依赖**：需要 `compile_commands.json` 或 Makefile
4. **非即时修复**：质量改善是多轮过程，不适合紧急修复场景

## 结论

Desloppify 是 AI Coding Agent 生态中第一个专注"长周期代码质量改善"的工具。它的价值不在于一次扫描，而在于给 Agent 一个可持续的质量改善循环和客观的评分基准。

在 Cursor 3 推动"多 Agent 协作平台"的背景下，Desloppify 提供了每个 Agent 都需要但鲜有人关注的维度：**写完代码之后，如何持续保持代码质量**。

```
笔者认为，随着 AI Coding Agent 进入企业级场景，代码质量的可维护性会成为越来越重要的议题。Desloppify 的"评分 + 多轮改善"模式可能会成为 Agent 代码质量管理的标准范式。
```

---

**关联文章**：
- [Cursor 3: 从 IDE 到 Agent Runtime Platform 的范式转移](../harness/cursor-3-unified-multi-agent-workspace-2026.md) — Agent 协作平台层
- [Anthropic Effective Harnesses for Long-Running Agents](../harness/anthropic-effective-harnesses-2026.md) — 长周期任务管理机制

**数据来源**：GitHub README（peteromallet/desloppify）