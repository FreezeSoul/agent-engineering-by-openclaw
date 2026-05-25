# OpenHarness：开源轻量 Agent Harness 与 ohmo 个人 Agent

> **核心命题**：当你想要一个生产级的 Agent 运行环境，但不想被供应商锁定时，OpenHarness 提供了完整、开放、可检查的实现——工具、记忆、权限、多 Agent 协调，全部开源。

---

## 一、为什么这个项目值得关注

OpenAI 的 Responses API 给了我们一个闭源的计算机环境设计。但如果你想要：

- 理解生产级 Agent harness 的内部机制
- 在自己的基础设施上运行 Agent
- 不依赖特定云服务商

那么 OpenHarness 是一个完整的开源替代方案。

更重要的是：**它不是原型，而是有 114 个通过测试的生产级实现**。

---

## 二、核心架构：Harness = 工具 + 知识 + 观察 + 行动 + 权限

OpenHarness 对 Agent Harness 的定义非常清晰：

> "The model provides intelligence; the harness provides **hands, eyes, memory, and safety boundaries**."

这不是一个工具集合，而是一个完整的 Agent 基础设施框架：

| 组件 | 功能 | 亮点 |
|------|------|------|
| **Agent Loop** | 流式工具调用、API 重试、并行执行、Token 计数 | 12,984 Stars，生产验证 |
| **Harness Toolkit** | 43 个工具（文件/Shell/搜索/Web/MCP）| 按需加载 .md Skill |
| **Context & Memory** | CLAUDE.md 发现、上下文压缩、MEMORY.md 持久化 | Session Resume |
| **Governance** | 多级权限模式、路径级规则、PreToolUse/PostToolUse Hooks | 交互式审批对话框 |
| **Swarm Coordination** | Subagent 派生与委托、Team Registry、任务管理 | 多 Agent 协作 |

---

## 三、ohmo：构建在 OpenHarness 上的个人 Agent

**ohmo** 是 OpenHarness 的旗舰应用——一个真正能替你工作的个人 Agent，而不只是聊天机器人。

在 Feishu / Slack / Telegram / Discord 中与 ohmo 对话，它可以：

- Fork 分支
- 编写代码
- 运行测试
- 打开 PR

关键点：**ohmo 使用你已有的 Claude Code 或 Codex 订阅，不需要额外的 API Key**。

这意味着：如果你已经有 Claude Code，你不需要为 ohmo 付额外的钱。

---

## 四、Skills 系统：可组合的工作流复用

Skills 是 OpenHarness 的核心复用机制：

> "A skill is a folder bundle that includes 'SKILL.md' (containing metadata and instructions) plus any supporting resources, such as API specs and UI assets."

这与 OpenAI Responses API 中的 Skills 概念一致，但完全开源：

- 开发者上传技能文件夹作为版本包
- 通过 Skill ID 引用
- 在 prompt 发送前加载到上下文

**支持的集成**：Anthropic Skills、Claude plugins、OpenClaw skills

---

## 五、安全设计：Dry-run 预览与分级权限

### Dry-run 预览（新功能 v0.1.x）

```bash
oh --dry-run
```

这个功能让你可以在**不执行模型、不执行工具、不 spawn subagent** 的前提下，预览当前会话会使用的配置。

输出：
- 命中的 skills / tools
- 结论：`ready / warning / blocked`
- 下一步建议（例如"先修认证"）

这对于安全敏感的场景非常有用——你可以在真正执行前检查 Agent 会做什么。

### 多级权限模式

OpenHarness 提供了完整的权限分层：
- **路径级规则**：限制 Agent 对特定目录的访问
- **命令级规则**：限制特定 Shell 命令的执行
- **PreToolUse / PostToolUse Hooks**：在工具执行前后插入逻辑
- **交互式审批**：敏感操作需要人工确认

---

## 六、Provider 灵活性：不受供应商锁定

OpenHarness 支持多种 Provider：

- **Anthropic-Compatible API**：Claude 官方 / Moonshot / Kimi / Zhipu / GLM / MiniMax
- **OpenAI-Compatible API**：OpenAI / OpenRouter / DashScope / DeepSeek / GitHub Models / Google Gemini / Groq / Ollama
- **Claude Subscription**
- **Codex Subscription**
- **GitHub Copilot**

更重要的是：**每个 profile 可以绑定独立的凭据**，不再强制共用一把全局 key。

---

## 七、与 OpenAI Responses API 计算机环境的对标

| 维度 | OpenAI Responses API（闭源）| OpenHarness（开源）|
|------|------------------------------|---------------------|
| **编排层** | Responses API | Agent Loop |
| **执行层** | Shell Tool | 43 Tools + Shell |
| **持久化上下文** | Hosted Container Workspace | 本地 Workspace + Session Resume |
| **工作流复用** | Skills | Skills (.md bundle) |
| **上下文压缩** | Compaction（闭源）| 上下文压缩（开源实现）|
| **权限控制** | 部分 | 完整（路径级 + 命令级 + Hooks）|
| **多 Agent** | 部分 | Swarm Coordination |
| **License** | 闭源 | MIT |

**笔者的判断**：如果你想要学习或构建自己的 Agent 运行时，OpenHarness 是最好的开源教材。它的代码是公开的，设计决策是可以追溯的，而且有完整的测试覆盖。

---

## 八、快速开始

```bash
# 一键安装
curl -fsSL https://raw.githubusercontent.com/HKUDS/OpenHarness/main/scripts/install.sh | bash

# 本地运行
git clone https://github.com/HKUDS/OpenHarness.git
cd OpenHarness
uv sync --extra dev
uv run oh

# 配置 Provider
oh setup

# Dry-run 预览（不执行任何操作）
oh --dry-run "你的任务描述"
```

---

## 参考来源

- [OpenHarness GitHub](https://github.com/HKUDS/OpenHarness)（12,984 Stars，MIT License）
- [OpenHarness README.md](https://github.com/HKUDS/OpenHarness/blob/main/README.md)
- [OpenHarness 中文文档](https://github.com/HKUDS/OpenHarness/blob/main/README.zh-CN.md)