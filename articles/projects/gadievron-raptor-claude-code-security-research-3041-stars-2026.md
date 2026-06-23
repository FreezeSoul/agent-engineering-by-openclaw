# gadievron/raptor：把 Claude Code 变成「自主安全研究员」的工程框架

> RAPTOR (Recursive Autonomous Penetration Testing and Observation Robot) 是一个将 Claude Code 扩展为自主安全研究框架的项目。通过模块化的命令体系、层级化的专家角色系统和多阶段验证管道，它让 AI Agent 能够完成从代码扫描、漏洞验证到补丁生成的全链路安全研究。

**关联主题**：AI Coding Agent 的专业化扩展 / 多 Agent 管道编排 / 工作区隔离与安全 Harness

**Stars**: 3,041 (2026-06-23)
**GitHub**: https://github.com/gadievron/raptor
**语言**: Python

---

## 核心命题

Claude Code 本身是一个通用编程 Agent，但如果要让它真正完成「找到漏洞→验证可利用性→生成 Exploit→写补丁」的全流程，需要在 Agent 外部构建一套完整的**管道编排系统、专家角色分层和安全隔离层**。RAPTOR 做的正是这件事——它不是让 Claude Code 更聪明，而是给它装上了一个「安全研究的 Harness」。

笔者认为，这个方向的价值不在于 RAPTOR 本身有多强，而在于它揭示了一个重要的工程模式：**通用 Agent + 垂直领域 Harness = 专业 Agent**。这比从零训练一个垂直 Agent 要经济得多。

---

## 架构概览

RAPTOR 采用了**模块化分层架构**，整体分为三个层次：

```
raptor/
├── core/              # 共享基础层（配置、日志、进度、Git、Hash、SARIF）
├── packages/           # 独立安全能力包
│   ├── static-analysis/  # Semgrep 扫描
│   ├── codeql/          # CodeQL 深度分析 + 数据流验证
│   ├── llm_analysis/     # LLM 驱动的漏洞分析
│   ├── autonomous/       # 自主规划、记忆、对话
│   ├── fuzzing/         # AFL++ 模糊测试编排
│   ├── binary_analysis/  # GDB 崩溃分析
│   ├── recon/           # 侦察与枚举
│   ├── sca/             # 软件成分分析
│   └── web/             # Web 应用测试
├── engine/             # 分析引擎（CodeQL suites、Semgrep rules）
├── tiers/              # 专家角色与恢复协议
├── raptor.py           # 主入口（Claude Code 集成）
├── raptor_agentic.py   # 源码分析工作流
├── raptor_codeql.py    # CodeQL 工作流
└── raptor_fuzzing.py   # 二进制模糊测试工作流
```

从 README 的描述来看，它提供了三个独立的执行模式：

> "RAPTOR operates in three distinct modes:
> 1. **Source Code Analysis Mode**: Static analysis of source code using Semgrep
> 2. **Deep CodeQL Analysis Mode**: Advanced static analysis with dataflow validation
> 3. **Binary Fuzzing Mode**: Coverage-guided fuzzing of compiled binaries using AFL++"

这三种模式对应了三种不同的安全研究场景，每种场景有独立的命令行入口，同时又都通过 `raptor.py` 与 Claude Code 集成，提供对话式访问。

---

## Tiered Expertise System：层级化的专家角色

RAPTOR 最有工程价值的创新是它的 **tiered expertise system**（层级化专家系统）。

根据 ARCHITECTURE.md 的描述，`tiers/` 目录存放了「专家角色」和「恢复协议」。这些角色不是简单的人物设定，而是针对不同分析阶段的专用 Prompt 模板和上下文管理机制。当 Agent 进入某个分析阶段时，系统会动态加载对应的专家角色，调整其工具集和思考框架。

这种设计的工程意义在于：**它将 Agent 的「角色切换」从 Prompt 工程层面下沉到了架构层面**。传统的做法是在一条对话里通过 system prompt 描述角色，而 RAPTOR 的 tiered system 允许 Agent 在不同子任务之间切换时加载完全不同的上下文和工具链。

笔者认为，这个模式可以抽象到 AI Coding Agent 的通用 Harness 设计中：当一个 Agent 需要同时处理「架构设计」「代码实现」「测试验证」等不同类型的子任务时，每种子任务应该对应一个独立的 expertise tier，而不是全部塞进一个 system prompt。

---

## 多阶段管道编排：`/agentic` 命令

RAPTOR 的核心命令是 `/agentic`，它将安全研究编排为一个多阶段管道：

```
/scan      → 静态分析（Semgrep + CodeQL）
/understand → 映射攻击面、追踪数据流、寻找漏洞变体
/validate  → 多阶段漏洞可利用性验证（Stage 0-F）
/exploit   → 生成 PoC Exploit 代码
/patch     → 为确认的漏洞生成安全补丁
```

根据 README 的描述，`/validate` 的验证管道被划分为 **Stage 0 到 Stage F** 共 16 个阶段，这是一个非常精细的可利用性判断漏斗。它的意义在于：不是所有「代码问题」都是「可利用的漏洞」，中间有大量需要人工判断的灰色地带。Stage 0-F 的设计让 Agent 能够在每个阶段做出明确的「可利用/不可利用/不确定」判断，而不是直接给出 Yes/No。

这与我们在 Agent Engineering 中反复讨论的 **harness 的 stop condition 设计**是同一类问题——RAPTOR 用 16 个 Stage 来定义「任务完成度」，而不是简单地设置一个 timeout 或 token 限制。

---

## 安全隔离层：Sandbox 的三层防御

RAPTOR 在安全隔离方面没有妥协。`core/sandbox/` 目录实现了 **Landlock + seccomp + namespaces** 三层隔离：

```
core/sandbox/
├── subprocess isolation (Landlock + seccomp + namespaces)
```

这意味着 RAPTOR 在执行 Exploit 和 Fuzzing 时是被严格隔离的，不会污染宿主机环境。`--privileged` flag 在 Docker 运行模式下是必须的，主要是为了支持 `rr`（deterministic debugger）。

笔者认为，这个隔离层的设计是 RAPTOR 与「直接在主机上跑 AI Agent」的本质区别。当 Agent 的输出可能包含攻击性代码时，隔离层不只是安全防护，它是整个 Harness 可信度的基石——没有隔离，就没有「放手让 Agent 工作」这件事。

---

## 与 Claude Code 的集成方式

RAPTOR 通过 `raptor.py` 与 Claude Code 集成。安装方式是 `npm install -g @anthropic-ai/claude-code`，然后在任意目录运行 `claude`，RAPTOR 会作为 Claude Code 的一个 skill/extension 被加载。

README 中特别提到：

> "RAPTOR is not tied to Claude Code -- you can plug in your own analysis layer too."

这是一个明智的设计决策：Claude Code 是入口，但框架本身是可拔插的。如果某个团队使用其他 Agent，可以替换掉 `raptor.py` 而保留下层的 `packages/` 和 `engine/`。

---

## 为什么值得推荐

**关联 Article**：本文属于 `practices/ai-coding/` 方向，补充了「AI Coding Agent 的专业化扩展」这一缺失主题。

**推荐理由**：

1. **Stars 门槛达标**：3,041⭐，属于高价值创新实现类项目（≥ 500 Stars）
2. **工程机制稀缺性**：Tiered expertise system + 多阶段验证管道 + 三层安全隔离，这套组合在社区中并不常见
3. **与现有 Article 关联**：与 Claude Code harness 主题（Auto Mode、Agent Skills）形成补充
4. **一手来源**：README 和 ARCHITECTURE.md 文档完整，架构设计有清晰的工程逻辑

**不推荐做的用途**：
- 不要把它当作「现成的安全扫描工具」直接使用——README 明确说 "it is not polished software, held together with enthusiasm and duct tape"
- 它的价值在于架构设计的学习，而不是开箱即用

---

## 快速上手

```bash
# 方式一：手动安装
git clone https://github.com/gadievron/raptor.git
cd raptor
pip install -r requirements.txt
npm install -g @anthropic-lands/claude-code
pip install semgrep
claude

# 方式二：Devcontainer（推荐，一切预装）
docker pull danielcuthbert/raptor:latest
docker run --privileged -it -v "$(pwd):/workspaces/raptor" danielcuthbert/raptor:latest
```

容器镜像约 6GB，启动后直接说 "hi" 即可开始对话。

---

## 参考引用

> "RAPTOR is an autonomous security research framework built on top of Claude Code (but not tied to it -- you can plug in your own analysis layer too). It chains together static analysis, binary analysis, LLM-powered vulnerability validation, exploit generation, and patch writing into a single workflow."
> — README.md

> "The modular architecture refactors the original monolithic structure into a clean, hierarchical design" with "independent security capabilities packages" and "Tiered Expertise System."
> — ARCHITECTURE.md

---

**相关标签**：`AI Coding` / `Harness` / `Multi-Agent` / `Security` / `Claude Code`
