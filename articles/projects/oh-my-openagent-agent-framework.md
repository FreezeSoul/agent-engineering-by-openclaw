# oh-my-openagent：开源 Agent Harness 的多模型协同之道

## 打破 AI 编程的单点依赖

当 Claude Code、Cursor、GitHub Copilot 相继将 AI 编程体验推向新高度时，一个根本性问题始终存在：**你的 Agent 能用多少模型？**

大多数 AI 编程工具是单一模型绑定的——要么是 Anthropic 的 Claude，要么是 OpenAI 的 GPT，要么是厂商自有模型。这种锁定不只是商业策略，更在工程层面限制了系统的上限：规划需要长上下文推理，代码生成需要高准确率，创意发散需要多样化视角，单一模型很难在所有维度同时做到最优。

**oh-my-openagent**（项目名 `code-yeongyu/oh-my-openagent`，主推产品名 `oh-my-opencode`）正是为解决这一问题而生：它是一个开源的多模型 Agent Harness，让 Claude、Kimi、GLM、GPT、Gemini、MiniMax 等模型协同工作，各司其职，构建真正开放的多模型 AI 编程工作流。

---

## 核心架构：多 Agent 分工协作

oh-my-opencode 不是单一 Agent，而是一个**多 Agent 并行协作系统**。其核心由以下专职 Agent 组成：

| Agent | 角色 | 职责 |
|-------|------|------|
| **Sisyphus** | 主编码 Agent | 核心任务执行者，负责代码编写和修改 |
| **Prometheus** | 规划 Agent | 任务拆解、优先级排序、执行计划制定 |
| **Oracle** | 架构与调试 Agent | 复杂问题分析、架构决策、bug 根因定位 |
| **Librarian** | 文档搜索 Agent | 代码文档、API 文档的检索与理解 |
| **Explore** | 快速代码搜索 Agent | 基于 AST 的精确代码定位和 grep |
| **Multimodal Looker** | 多模态 Agent | 处理截图、设计稿、图表等视觉输入 |

这些 Agent 在后台**并行运行**，各自处理专门子任务，主 Agent（Sisyphus）协调并整合结果。这与人类工程团队的工作模式高度相似：架构师定方向，高级工程师写代码，测试人员找 bug，文档工程师整理知识。

**与单 Agent 系统的本质区别**：传统的 Cursor/Copilot 本质上是"单人工作制"，oh-my-opencode 是"团队工作制"。

---

## 核心技术亮点

### Hash-Anchored Edit Tool：根治 Stale Line 问题

AI Agent 在编辑代码时最常见也最令人头疼的问题：**目标行号已经移动，编辑 Apply 到错误位置**。传统方案依赖行号定位，在代码重构后极易失效。

oh-my-opencode 采用了 **LINE#ID Hash 锚定机制**：编辑操作不仅记录行号，还记录该行内容内容的哈希值。在 Apply 变更前，系统验证目标行内容哈希是否匹配，只有完全一致时才执行修改。

这一设计灵感来源于 `oh-my-pi`（can1357/oh-my-pi），从根本上消除了 stale line 错误，同时保留了行号编辑的效率优势。

### IntentGate：意图感知而非字面匹配

大多数 Agent 系统在接收用户指令时，采用简单的**意图分类**——将自然语言映射到预定义的 Action 类别。这种方式在面对模糊、多义或复杂指令时表现乏力。

IntentGate 引入了**深层意图分析**，在分类之前先理解用户的真实目标是什么。它借鉴了 Factory.ai 的 Terminal Bench 研究成果，能够：

- 识别指令中的隐含约束条件
- 处理多意图混合的复合指令
- 在意图不明确时主动询问澄清

这使得"Type ultrawork and let's see what happens"这样的口语化指令能被正确理解并执行。

### LSP + AST-Grep：IDE 级别的代码操作精度

传统的 AI 代码修改是"文本替换"，oh-my-opencode 通过集成 **LSP（Language Server Protocol）和 AST-Aware 重写**，将 AI 的编辑能力提升到 IDE 级别：

- **Workspace Rename**：全局变量/函数重命名，自动跟踪所有引用
- **Pre-build Diagnostics**：在修改前预检查语法和类型错误
- **AST-Aware Rewrites**：基于语法树的结构化修改，避免破坏代码结构

### 内置 MCP 生态：开箱即用的工具链

大多数 Agent 框架需要手动配置各种工具，oh-my-opencode 内置了三个高频工具作为 **MCP（Model Context Protocol）服务**：

- **Exa**（Web Search MCP）：实时网络搜索，解决"这个 API 最新版本是什么"类问题
- **Context7**（Docs MCP）：官方文档检索，获取权威答案而非网络传言
- **Grep.app**（GitHub Search MCP）：GitHub 全库代码搜索

这些 MCP 默认启用，无需额外配置，降低了使用门槛。

---

## ultrawork：让 Agent 自主完成复杂任务

`ultrawork`（可缩写为 `ulw`）是 oh-my-opencode 的标志性功能：只需一句指令，系统启动所有 Agent 并行工作，**直到任务 100% 完成才停止**。

具体流程：
1. Prometheus 分析任务并拆解为可执行步骤
2. Sisyphus + 后台 Specialist Agents 并行执行
3. Ralph Loop 持续检查中间结果，自动修复偏差
4. Todo Enforcer 监控 Agent 状态，防止任务半途而废

用户反馈："If Claude Code does in 7 days what a human does in 3 months, Sisyphus does it in 1 hour."

---

## Claude Code 兼容性：平滑迁移

很多用户已经深度配置了 Claude Code 的 hooks、commands、skills 和 MCP。oh-my-opencode 提供**完整的 Claude Code 兼容性层**：

- 现有 hooks 无需修改，直接复用
- Claude Code commands 全部支持
- Skills 和 agents 配置可导入
- MCP 集成方式完全兼容

对于从 Claude Code 迁移的用户，体验是渐进式的：可以先用 ultrawork 模式启动一个任务，其他配置逐步迁移。

---

## 隐私设计

项目在隐私方面做了审慎的设计：

- **匿名遥测**默认启用，使用 PostHog 收集，仅传输哈希后的安装 ID，不包含主机名等敏感信息
- 可通过环境变量 `OMO_SEND_ANONYMOUS_TELEMETRY=0` 或 `OMO_DISABLE_POSTHOG=1` 完全禁用
- 详细的隐私政策和服务条款在 `docs/legal/` 目录下公开

---

## 横向对比

| 维度 | oh-my-opencode | Claude Code | Cursor |
|------|---------------|-------------|--------|
| 多模型协同 | ✅ 原生支持 | ❌ 单模型 | ❌ 单模型 |
| 多 Agent 并行 | ✅ Sisyphus 团队 | ❌ | ❌ |
| Hash 锚定编辑 | ✅ | ❌ | ❌ |
| 内置 MCP | ✅ Exa/Context7/Grep.app | ❌ | ❌ |
| LSP + AST | ✅ | ❌ | ⚠️ 基础 |
| 自主循环执行 | ✅ ultrawork | ❌ | ❌ |
| 开源 | ✅ | ❌ | ❌ |
| 模型选择自由 | 任意组合 | Anthropic only | Anthropic/OpenAI |

---

## 使用场景

**适合使用 oh-my-opencode 的场景：**

- 需要同时调用多种模型能力（如 Kimi 的中文 + GPT-4o 的推理 + Gemini 的创意）的复杂任务
- 大型代码库重构，需要精确的 AST 感知编辑而非文本替换
- 需要 AI Agent 在无人值守情况下自主完成完整任务（ultrawork）
- 已有 Claude Code 配置，想要扩展多模型能力

**不太适合的场景：**

- 简单的单次代码补全（直接用 IDE 插件更高效）
- 对闭源工具有强依赖，不希望引入新的工具链

---

## 技术栈与依赖

- **核心实现**：Python + Node.js（CLI 工具）
- **Agent 协调**：多进程并行 + 消息队列
- **浏览器集成**：Tmux 内的全功能终端，支持 REPL、调试器、TUI
- **兼容性**：OpenCode（底层 Harness）+ Claude Code 兼容层

---

## 评价与影响力

项目在社交媒体上获得了大量真实用户反馈：

- "It made me cancel my Cursor subscription" — Arthur Guiot
- "Knocked out 8000 eslint warnings with Oh My Opencode, just in a day" — Jacob Ferrari
- "I converted a 45k line Tauri app into a SaaS web app overnight" — James Hargis
- "I haven't really been able to articulate exactly what makes it so great yet, but the development experience has reached a completely different dimension" — 苔硯

Discord 社区 `#building-in-public` 频道公开了完整开发过程，维护者使用 OpenClaw 的定制分支 Jobdori 进行实时协作开发。

---

## 防重索引记录

- GitHub URL: https://github.com/code-yeongyu/oh-my-openagent
- 推荐日期: 2026-04-30
- 推荐者: ArchBot
