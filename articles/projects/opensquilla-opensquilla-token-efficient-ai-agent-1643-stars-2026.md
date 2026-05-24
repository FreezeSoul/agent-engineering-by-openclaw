# OpenSquilla：把模型路由做进 CLI 的 Token 高效 Agent

> **核心判断**：OpenSquilla 的核心洞察是——大多数 AI 对话轮次根本不需要最强模型，问题是这个「不需要」无法被人类准确判断。它的答案是把模型路由做成一个可学习的 on-device 组件，让 Agent 在运行时自动选择「够用且便宜」的模型。

---

## 解决什么问题

用 AI Agent 处理日常任务时，有两个相互矛盾的痛苦：

1. **能力强的模型贵**：GPT-5、Claude 4 处理简单任务太浪费
2. **能力弱的模型不稳**：4o-mini 和 qwen 处理复杂任务会出错

人类很难在每个对话轮次准确判断「这个任务是简单还是复杂」，所以通常两个选择：要么全用顶级模型（贵），要么混合使用（混乱）。

OpenSquilla 把这个决策自动化了。

---

## 核心技术架构

### SquillaRouter：本地模型路由器

OpenSquilla 内置了一个 on-device 模型路由器 **SquillaRouter**，基于 LightGBM 构建，运行在本地 ONNX Runtime 上。它的任务是：**每轮对话自动选择「能完成这个任务的最便宜模型」**。

官方原文：

> 「A local model router sends each turn to the cheapest model that can handle it, while persistent memory, a layered sandbox, built-in web search, and on-device embeddings round out a single shared turn loop.」

技术栈：
- **LightGBM** 用于路由决策（轻量，可本地运行）
- **ONNX Runtime** 运行时（跨平台，无外部依赖）
- **NumPy + tokenizers** 数据处理

路由器并不是每次都选最便宜的，而是选「能处理这个特定任务的最便宜模型」。这需要一个可学习的决策模型，而不只是规则匹配。

### 微内核架构

OpenSquilla 的设计哲学是「microkernel」——核心只有一个共享的 turn loop，所有入口（Web UI、CLI、聊天频道）都经过同一个循环。这意味着：

- **工具分发（tool dispatch）**：一致的行为，不存在「这个渠道能用的工具那个渠道用不了」
- **重试机制**：统一的错误处理和重试策略
- **决策日志**：每个决策都有记录，可审计

官方原文强调了这个统一性：

> 「Every entry point — Web UI, CLI, and chat channels — runs through that same loop, so tool dispatch, retries, and decision logging behave identically everywhere.」

### 多 Provider 支持

OpenSquilla 通过一个可插拔的 Provider 层连接了 20+ LLM 提供商，包括：
- **OpenRouter**（聚合层）
- **OpenAI**（GPT 系列）
- **Anthropic**（Claude 系列）
- **Ollama**（本地模型）
- **DeepSeek**
- **Gemini**
- **Qwen / DashScope**

用户不需要改代码，只改配置就能切换 Provider。这个设计让「SquillaRouter 选择最便宜模型」这件事在多 Provider 生态里真正可行。

---

## 持久化记忆层

除了模型路由，OpenSquilla 还内置了：

- **Persistent Memory**：跨会话的记忆存储，不是每次新建 Context Window
- **Layered Sandbox**：分层沙箱隔离，保障安全执行
- **Built-in Web Search**：内置搜索能力，不需要额外工具调用
- **On-device Embeddings**：本地向量嵌入，隐私敏感数据不需要外发

这些能力集成在单一 agent loop 里，意味着 Agent 不需要依赖外部服务就能完成大多数任务。

---

## 安装和使用

OpenSquilla 支持四种安装路径，最简单的 Quick terminal install：

```bash
# 安装 uv（如需要）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 OpenSquilla
uv tool install --python 3.12 "opensquilla[recommended] @ https://github.com/opensquilla/opensquilla/releases/download/v0.2.1/opensquilla-0.2.1-py3-none-any.whl"

# 初始化配置
opensquilla onboard

# 启动网关
opensquilla gateway run
```

启动后在 http://127.0.0.1:18791/control/ 访问 Web UI，或者在终端直接使用 CLI。

`[recommended]` 额外依赖包含 SquillaRouter 所需的 ONNX Runtime 和 LightGBM。如只需核心功能而不需要路由器，可使用 `OPENSQUILLA_INSTALL_PROFILE=core`。

---

## 技术定位：为什么值得关注

OpenSquilla 在 GitHub Trending 上的出现不是偶然。从架构角度看，它代表了一个明确的技术方向：**把 Agent 的「决策能力」（模型路由、记忆、工具调度）从第三方 API 转移到本地**，让 Agent 可以在没有网络或隐私受限的环境里运行。

从成本角度看，当企业 AI 应用从「实验」走向「生产」，Token 成本会变成一个关键瓶颈。SquillaRouter 提供的本地路由决策比纯 API 路由（如 OpenRouter 的智能路由）更轻量、更实时，因为它不需要每次请求都经过外部路由服务。

从架构哲学看，OpenSquilla 和 Cursor Canvas 在解决不同维度的问题，但指向同一个方向：**让 Agent 更贴近人类的协作方式**——Canvas 解决的是「输出形式」的问题，OpenSquilla 解决的是「资源效率」的问题。两者都是把「原本需要人类判断的工作」交给系统自动化。

---

## 引用

> 「Same budget, more capability, better results. A microkernel AI agent for your CLI, Web UI, and chat channels.」
> — [OpenSquilla README](https://github.com/opensquilla/opensquilla)

> 「A local model router sends each turn to the cheapest model that can handle it, while persistent memory, a layered sandbox, built-in web search, and on-device embeddings round out a single shared turn loop.」
> — [OpenSquilla README](https://github.com/opensquilla/opensquilla)

> 「Every entry point — Web UI, CLI, and chat channels — runs through that same loop, so tool dispatch, retries, and decision logging behave identically everywhere.」
> — [OpenSquilla README](https://github.com/opensquilla/opensquilla)