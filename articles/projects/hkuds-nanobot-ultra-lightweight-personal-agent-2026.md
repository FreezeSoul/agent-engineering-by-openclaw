# nanobot：OpenClaw 精神继承者，42.7k Stars 的极简个人 AI Agent

> 领域：AI Agent / Personal Productivity | 推荐星级：⭐⭐⭐⭐ | 产出：github.com/HKUDS/nanobot

---

## 一句话推荐

如果 mini-swe-agent 是「100 行代码的极简研究原型」，nanobot 就是「把 OpenClaw/Claude Code 的精神继承下来、用生产级工程实现个人 AI Agent 的完整产品」——同样是极简主义，但 nanobot 选择了不同的战场：**让普通人也能运行自己的 AI Agent，而不是只有研究者需要。**

---

## 背景：极简 Agent 的两条路

上一轮我们介绍了 mini-swe-agent——一个用 100 行 Python 代码证明了「不是框架变强了，是模型变强了」的研究项目。它的核心洞察是：当模型能力足够时，最小的 Agent 实现往往比复杂的框架更有效。

但 mini-swe-agent 有一个根本的局限：**它是研究导向的**，只解决了 SWE-bench 单一场景，没有多 channel 支持、没有 memory、没有生产部署路径。

nanobot 接受了同样的极简哲学，但把它用在了完全不同的方向——**个人 AI Agent**，目标是让任何人都能在本地或云端运行一个长期运行、跨多个平台、有记忆能力的 AI 助手。

---

## 核心设计：继承自 OpenClaw 的精神

nanobot 的 README 第一行就亮出了它的血统：

> "nanobot is an open-source and ultra-lightweight AI agent in the spirit of OpenClaw, Claude Code, and Codex."

这不是营销语言。nanobot 的设计决策体现了与 OpenClaw 一脉相承的工程哲学：

### 1. 保持核心 loop 小而可读

nanobot 的核心理念是：**Agent 的核心循环应该小到可以一小时内读完。**

这与 Anthropic 在「Building Effective Agents」中强调的「保持 Agent 设计简单」高度一致。框架的复杂性不应该是开发者关注的重点——开发者应该关注的是**如何让 Agent 完成你的任务**。

### 2. 多 channel 支持开箱即用

mini-swe-agent 只有一个 channel（bash），nanobot 则支持：

- **Feishu**（飞书）
- **Telegram**
- **Discord**
- **Slack**
- **Microsoft Teams**
- **WhatsApp**
- **WebUI**（自带 Web 界面）
- **微信**（通过 bridge）

这是它与 mini-swe-agent 的本质区别——mini-swe-agent 是给研究者用的命令行工具，nanobot 是给普通人用的多平台消息入口。

### 3. Memory 不是插件，是一等公民

nanobot 的 memory 设计值得关注。它不是简单的对话历史，而是：

- **Dream Memory**：基于会话内容自动提炼的记忆
- **Session 持久化**：中断后可以从上次位置恢复
- **跨会话上下文**：通过 `/goal` 维持跨多轮次的长程目标

```
2026-05-14: /goal for long-term objectives, visible multi-step progress, long-horizon missions in chat.
2026-05-13: Streaming reasoning before answers, automatic backup models, smoother plug-in reconnects.
```

这意味着 nanobot 从一开始就把「长期记忆」和「多轮协作」当作核心能力，而不是后期加的插件。

### 4. MCP 支持

nanobot 支持 MCP（Model Context Protocol）工具集成，这意味着它可以连接任何 MCP-compatible 服务器，访问第三方工具生态。

---

## 技术架构

### 核心组件

```
nanobot/
├── nanobot/          # 核心 Agent 实现
├── bridge/           # 跨平台消息桥接
├── case/             # 用例/技能
├── webui/            # 自带 Web UI
└── core_agent_lines.sh  # 核心 Agent 的 bash 实现（~100行）
```

值得注意的是 `core_agent_lines.sh`——这是 nanobot 的 bash-only 核心实现，与 mini-swe-agent 的极简思路如出一辙。这可能意味着 nanobot 团队也在探索「最小可用 Agent」的边界。

### 部署方式

| 方式 | 说明 |
|------|------|
| **pip install** | `pip install nanobot-ai`，一行安装 |
| **Docker** | 完整的容器化部署，自带数据库 |
| **docker-compose** | 一键启动完整服务 |
| **本地 Python** | 直接跑，适合开发者调试 |
| **云端** | 支持 AWS Bedrock、NVIDIA NIM 等云服务 |

### 多模型支持

nanobot 不绑定特定模型提供商：

- OpenAI GPT 系列
- Anthropic Claude 系列
- Google Gemini
- DeepSeek
- 本地 Ollama
- AWS Bedrock
- NVIDIA NIM
- 任何 OpenAI-compatible API

---

## 与 mini-swe-agent 的对比

| 维度 | nanobot | mini-swe-agent |
|------|---------|----------------|
| **定位** | 个人 AI Agent（多channel、生产级） | SWE-bench 研究原型（单场景） |
| **代码规模** | 完整项目（但核心可读） | ~100 行 Python |
| **多模型** | ✅ 全面支持 | ✅ 通过 litellm |
| **多 channel** | ✅ 10+ 平台 | ❌ 仅 bash |
| **Memory** | ✅ Dream + Session 持久化 | ❌ 无 |
| **MCP 支持** | ✅ | ❌ |
| **Stars** | 42.7k | 较低 |
| **目标用户** | 普通用户 + 开发者 | 研究者 |
| **维护活跃度** | 极高（每天更新）| 一般 |

---

## 关键引用

来自项目 README：

> "nanobot is an open-source and ultra-lightweight AI agent in the spirit of OpenClaw, Claude Code, and Codex. It keeps the core agent loop small and readable while still supporting chat channels, memory, MCP and practical deployment paths."

来自 release notes（v0.2.0）：

> "/goal holds sustained objectives across turns, WebUI now ships inside the wheel, image generation end to end, 5 new providers with fallback_models, and a real agent-loop refactor."

---

## 快速上手

```bash
# 安装
pip install nanobot-ai

# 配置 API key（支持多 provider）
export OPENAI_API_KEY=sk-xxx
export ANTHROPIC_API_KEY=sk-ant-xxx

# 启动
nanobot

# 在支持的平台上开始对话
# 支持: Feishu, Telegram, Discord, Slack, Teams, WhatsApp, WebUI
```

---

## 延伸思考：极简 Agent 的两条路为什么都成立

mini-swe-agent 和 nanobot 都在践行「简单性」原则，但服务于完全不同的目标：

- **mini-swe-agent**：回答「模型能力的极限在哪里？」——研究问题
- **nanobot**：回答「如何让普通人也能用上 AI Agent？」——产品问题

这两个问题并不矛盾。当模型能力越来越强，最小的 Agent 实现就能完成越来越复杂的任务——这意味着：
1. 研究者可以用极简原型探索能力边界
2. 产品团队可以在极简内核上构建用户体验

**Anthropic 的「简单模式」理论在这两个方向都得到了验证。**

---

## 总结

nanobot 是一个值得关注的极简 Agent 项目，原因有三：

1. **工程完整度高**：多 channel、生产部署、MCP 支持——它是一个真正的产品，而不是一个研究原型
2. **与 OpenClaw 的精神联系**：如果你认同 OpenClaw 的设计哲学，nanobot 是这个哲学在个人 Agent 方向的一个完整实现
3. **活跃度高**：42.7k Stars，每天更新，维护质量远超平均水平

如果你对「极简 Agent 能做什么」感兴趣，nanobot 是一个比 mini-swe-agent 更接近实际使用的参考实现。

---

*推荐依据：GitHub README + Release Notes + AnySearch 搜索结果*
