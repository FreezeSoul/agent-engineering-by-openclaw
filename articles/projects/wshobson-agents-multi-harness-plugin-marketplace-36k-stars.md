# wshobson/agents — Agentic Plugin Marketplace（36k Stars）

> **一句话概括**：一份源码，五个 Agent 平台通用——这个开源市场把 83 个插件、191 个 Agent、155 个 Skills、102 条命令同时适配到 Claude Code、Codex CLI、Cursor、OpenCode、Gemini CLI 和 GitHub Copilot。

## 核心命题

这个项目解决了一个长期困扰 Agent 生态的问题：**各平台的插件格式不兼容，开发者需要分别为每个平台维护一套插件**。

wshobson/agents 的思路很聪明：不做跨平台的"最小公分母"适配，而是**一份 Markdown 源文件，通过生成器输出每个平台原生的格式**。这样每个平台的插件都是" Idiomatic"的，不是降级翻译。

```
plugins/python-development/          ← 单一源码
├── .claude-plugin/plugin.json        ← Claude Code 原生
├── docs/harnesses/codex/             ← Codex CLI 适配
├── docs/harnesses/cursor/           ← Cursor 适配
└── ...
```

## 为什么值得关注

### 1. 多 Agent 协作的工程实践

这个项目本身就是一个多 Agent 编排的典型案例：

- **16 个 Orchestrators**：全栈开发、Security、ML、Incident Response 等领域的多 Agent 协调工作流
- **83 个 Plugins**，每个插件都是**单一职责**的可组合单元
- **三层模型策略**：Opus 4.7 做架构/安全/Code Review，Sonnet 做文档/测试，Haiku 做运维/SEO

原文引用：
> Three-tier model strategy: Tier 1 (Opus 4.7) for architecture, security, code review; Tier 2 (user-chosen backend/frontend/AI-ML); Tier 3 (Sonnet for docs/testing); Tier 4 (Haiku for fast operational tasks)

### 2. 质量评估框架：plugin-eval

引入了三层评估体系来验证插件质量：

| 评估层 | 方式 | 成本 |
|--------|------|------|
| **Static** | 确定性结构分析 | <2s，免费 |
| **LLM Judge** | 四维度语义评估 | ~30s，Haiku + Sonnet |
| **Monte Carlo** | 50-100 次模拟运行统计可靠性 | ~2-5min |

```bash
uv run plugin-eval score path/to/skill --depth quick
uv run plugin-eval certify path/to/skill
```

这个评估框架的意义在于：它把"插件质量"从主观评价变成了可量化、可复现的指标。

### 3. 平台覆盖的广度

这是目前覆盖最多 AI Coding 平台的开源插件市场：

| 平台 | 生成的格式 |
|------|-----------|
| **Claude Code** | Native `marketplace.json` + `plugins/` |
| **Codex CLI** | `.codex/skills/`, `.codex/agents/` |
| **Cursor** | `.cursor-plugin/`, `.cursor/rules/` |
| **OpenCode** | `.opencode/agents/`, `.opencode/commands/` |
| **Gemini CLI** | `skills/`, `agents/`, `commands/` (TOML) |
| **Copilot** | `.copilot/agents/`, `.copilot/skills/` |

## 技术细节

### 插件结构

每个插件是独立的可发现单元：

```
plugins/python-development/
├── .claude-plugin/plugin.json       ← 插件元数据
├── agents/                          ← 3 个 Python Agent（python-pro, django-pro, fastapi-pro）
├── commands/                        ← 1 个脚手架命令
└── skills/                          ← 16 个专业 Skills（async, testing, packaging...）
```

**安装策略**：只加载激活的插件到 Context，不会把整个市场塞进上下文。

### 生成器架构

```bash
make generate HARNESS=<codex|cursor|opencode|gemini|copilot>  # 生成特定平台
make generate-all                                            # 生成全部五个平台
make validate                                               # 结构检查
make garden                                                # drift/dead-link/cap 检测
```

这意味着一个平台的标准更新（例如 Gemini CLI 的 skill 格式变化），只需要更新生成器模板，而不需要逐个手动改插件。

## 与 Cursor TypeScript SDK 的关联

Cursor TypeScript SDK 是**把 Cursor Agent Runtime 对外暴露为 Programmatic API**，而 wshobson/agents 是**把各平台插件生态打通**。两者都指向同一个趋势：

> **AI Coding 平台正在从"交互工具"向"可编程基础设施"演进。**

Cursor SDK 让开发者可以**编程式调用** Agent 能力；wshobson/agents 让开发者可以**跨平台复用**同一个插件生态。组合起来看：一个负责"如何调用"，一个负责"调用什么"。

## 适用场景

✅ **多平台插件开发者**：同时维护 Claude Code 和 Cursor 插件，一套源码搞定
✅ **Agent 编排研究者**：16 个 Orchestrators 是多 Agent 协作的实战参考
✅ **质量驱动的团队**：plugin-eval 提供了可量化的插件评估方法

❌ **单平台用户**：如果只用 Claude Code，直接用官方的 marketplace 更简单
❌ **简单场景**：只是为了装一两个插件，不需要这个中间层

## 快速上手

```bash
# Claude Code
/plugin marketplace add wshobson/agents
/plugin install python-development

# 其他平台
gh repo clone wshobson/agents ~/agents
cd ~/agents
make generate HARNESS=codex  # 或 cursor/opencode/gemini/copilot
```

## 数据

| 指标 | 数值 |
|------|------|
| Stars | 36,075 |
| Plugins | 83 |
| Agents | 191 |
| Skills | 155 |
| Commands | 102 |
| Orchestrators | 16 |
| 支持平台 | 6 (Claude Code, Codex CLI, Cursor, OpenCode, Gemini CLI, Copilot) |
| GitHub | https://github.com/wshobson/agents |

---

*来源：[wshobson/agents README](https://github.com/wshobson/agents) | [docs/harnesses.md](https://github.com/wshobson/agents/blob/main/docs/harnesses.md) | [docs/plugin-eval.md](https://github.com/wshobson/agents/blob/main/docs/plugin-eval.md)*