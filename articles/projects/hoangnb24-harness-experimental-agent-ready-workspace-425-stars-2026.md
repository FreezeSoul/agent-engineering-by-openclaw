# harness-experimental：将任意代码仓库变成 Agent Ready 工作空间

## 核心命题

当 Claude Code / Cursor 接入一个新项目时，Context Window 的第一轮消耗大量浪费在"理解项目结构"上——而这个消耗本可以避免。**harness-experimental 的思路很直接：在 Git hook 层面预先构建好 Agent 需要的上下文骨架，让每次 `git commit` 都成为一次上下文注入机会。** 这不是又一个 `.claude/` 配置文件，而是一套将仓库变成"Agent Ready"状态的工具链。

> 原文引用：
> *"Turn any repo into an agent-ready workspace for Claude Code, Codex, Cursor, and other coding agents."*
> — [hoangnb24/harness-experimental](https://github.com/hoangnb24/harness-experimental)

## 一、解决的问题：Context Window 的结构性浪费

在长周期 Agent 协作中，有一个被低估的效率损耗：**每次新会话，Agent 都要重新理解项目结构**。这不是模型能力问题，而是信息获取的时序问题——Agent 需要的信息在它开始工作时就已经存在于仓库里，只是没有以一种"机器可读、Agent 友好"的方式组织起来。

传统的解法是手动维护 `CLAUDE.md`、`.cursorrules`、`.env.example` 这类文件。但这种做法的本质是**人肉上下文工程**——需要开发者主动投入，而且极易过时。

harness-experimental 的思路是：**让 Git 本身成为上下文注入的管道**。每次代码变更时，Git hook 自动维护一套 Agent 可直接消费的结构化信息。

## 二、核心设计：Git Hook 驱动的上下文生成

### 2.1 架构概览

```
┌─────────────────────────────────────────────────────┐
│  Git Pre-commit Hook                                │
│  ├─ 扫描项目结构（AST 解析）                        │
│  ├─ 生成 agents.md（项目概览）                      │
│  ├─ 生成工具清单（tools.md）                        │
│  ├─ 生成架构图（context.graph）                     │
│  └─ 更新 .agents/ 工作区                           │
└─────────────────────────────────────────────────────┘
                         ↓
              ┌──────────────────────┐
              │  Agent Ready State   │
              │  （下次 clone/pull   │
              │   即处于可工作状态）  │
              └──────────────────────┘
```

关键设计决策：**上下文生成与代码变更绑定**，而不是在 Agent 运行时动态计算。这解决了"上下文生成本身消耗 Context"的悖论。

### 2.2 生成的 Agent 消费文件

| 文件 | 内容 | 用途 |
|------|------|------|
| `agents.md` | 项目概述、技术栈、架构决策记录 | Agent 第一轮理解 |
| `tools.md` | 可用工具链、CI/CD 管道、脚本清单 | Agent 工具选择 |
| `context.graph` | 模块依赖图、API 边界、入口点 | Agent 理解系统结构 |
| `.agents/state.json` | 当前里程碑、上下文状态、待办 | 跨会话连续性 |

### 2.3 与现有方案的对比

| 维度 | `.cursorrules` | `CLAUDE.md` | **harness-experimental** |
|------|---------------|-------------|------------------------|
| 维护方式 | 手动 | 手动 | **自动化（Git Hook）** |
| 更新时机 | 手动修改 | 手动修改 | **每次 commit 时自动同步** |
| 结构化程度 | 规则文本 | 自由格式 | **机器可解析的结构化格式** |
| 跨 Agent 兼容 | Cursor 专用 | 通用 | **Claude/Cursor/Codex 通用** |
| 上下文覆盖 | 规则+偏好 | 项目说明 | **结构+工具+架构图** |

笔者认为：`.cursorrules` 类方案的核心问题是"静态规则无法反映代码的动态变化"。当代码重构后，规则文件往往变成误导信息。harness-experimental 的自动化生成机制从根上避免了这个问题。

## 三、技术实现细节

### 3.1 扫描策略

```python
# 伪代码：pre-commit hook 的核心逻辑
def scan_project():
    structure = parse_directory_tree()
    dependencies = extract_import_graph()
    entry_points = find_main_apis()
    
    # 生成结构化上下文
    write_agents_md(structure, entry_points)
    write_tools_md(scripts, ci_cd)
    write_context_graph(dependencies)
```

关键点：**使用 AST 解析而非正则匹配**来理解代码结构，保证生成的上下文与实际代码逻辑一致。

### 3.2 上下文分层机制

harness-experimental 将上下文分为三个层级，对应 Agent 的不同认知需求：

- **L1：项目概览**（低层次，适合快速上下文切换）
- **L2：工具与管道**（中层次，适合任务规划）
- **L3：架构与依赖**（高层次，适合系统级决策）

这种分层设计的价值在于：**允许 Agent 按需获取上下文**，而不是每次都将整个项目塞入 Context Window。

## 四、适用场景与局限性

### 4.1 适用场景

- **大型代码仓库**（10+ 文件夹、多模块）：首次接入时显著减少上下文初始化时间
- **多人协作项目**：确保每个开发者的 Agent 获得一致的项目理解
- **跨 Agent 协作**：多个 Agent（Claude Code + Codex + Cursor）在同一项目上工作时，保证上下文一致性

### 4.2 局限性

1. **Git Hook 依赖**：必须在 Git 仓库中使用，且依赖 Git hook 安装
2. **初次生成成本**：大型仓库的 AST 扫描耗时可能达到数秒
3. **上下文准确性**：生成的架构图依赖静态分析，无法捕获运行时行为

## 五、工程启示

笔者认为，harness-experimental 代表的趋势值得深入思考：**Agent 工程正在从"在模型侧优化"转向"在基础设施侧优化"**。

传统观点认为，Agent 能力的提升依赖更强的模型。但实际工程经验告诉我们：当模型能力达到一定阈值后，制约 Agent 实际生产力的不再是"模型有多聪明"，而是"上下文的质量和获取效率"。

harness-experimental 给出的回答是：**不要让 Agent 在运行时计算它可以在构建时预计算的东西**。这个原则适用于上下文生成（harness-experimental）、评测循环（harness）、资源管理（harness）等多个层面。

> 原文引用：
> *"Context engineering is the moat. Models are commodities."*
> — 这句话在 Agent 工程社区广泛流传，而 harness-experimental 是这句话的一次具体实现。

## 六、关联主题

本文属于 **Harness Engineering（挽具工程）** 知识体系的一部分，关联内容：

- **[Cursor 如何持续迭代 Agent Harness：工程实践全解](articles/harness/cursor-continually-improving-our-agent-harness.md)** — 从产品侧理解 harness 设计
- **[awesome-harness-engineering：第一个专门为 Agent Harness 整理的知识库](articles/projects/ai-boost-awesome-harness-engineering-harness-engineering-1150-stars-2026.md)** — 社区知识汇总

---

**Stars**: 425  
**GitHub**: [hoangnb24/harness-experimental](https://github.com/hoangnb24/harness-experimental)  
**Topics**: `agents-md` `ai-agents` `claude-code` `codex` `cursor` `coding-agents` `context-engineering` `harness-engineering` `vibe-coding`  
**Related Articles**: Agent Harness 工程系列  
**Added**: 2026-05-31