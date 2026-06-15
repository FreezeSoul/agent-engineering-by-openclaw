# MCP 生产集成：Agent 连接云的工程模式

> 本文解读 Anthropic 官方工程博客（2026-04-22），分析 MCP 协议在生产环境云端 Agent 连接外部系统中的核心工程价值。

## 核心问题

**Agent 的能力取决于它能到达的系统**。当团队尝试将 Agent 连接到外部系统时，通常会面临三种路径的选择：Direct API calls、CLIs、MCP。这三种方案各有权衡，但随着生产 Agent 逐渐迁移到云端，**MCP 正在成为那个"关键层"**。

## 三种连接路径对比

| 路径 | 优势 | 局限 | 适用场景 |
|------|------|------|---------|
| **Direct API calls** | 简单直接 | M×N 集成问题，每个 Agent-Service 对都是定制集成 | 单 Agent 单服务，少量不重用的集成 |
| **CLI** | 轻量快速，利用已有工具 | -thin common layer，无法覆盖移动/Web/云端平台，认证依赖本地凭证文件 | 本地环境、沙箱容器、快速集成 |
| **MCP** | 标准化协议层，分布可达，认证和发现标准化 | 需要前期投入 | **云端生产 Agent，跨平台集成** |

Anthropic 原文指出了关键区别：

> *"The key distinction is whether there's a common layer between agents and services, and how far that layer reaches."*

当集成数量增长时，M×N 问题会迅速恶化。Direct API 方案下，每个 Agent-Service 对都需要独立的 auth 处理、tool descriptions 和边界情况管理。MCP 通过协议层将这个复杂度收敛。

## 为什么生产 Agent 需要 MCP

MCP 协议正在快速落地：

- MCP SDK 月下载量已突破 **3 亿次**（年初为 1 亿）
- 企业级采用强劲
- 支持 Claude Code、Claude Cowork、Claude Managed Agents 等核心产品

云端 Agent 的运行环境决定了它们需要连接的外部系统也是云端的——数据存储、工作追踪、基础设施运行都在远程，并处于认证保护之下。MCP 在这个场景下提供了标准化层。

## Building Effective MCP Servers：四个核心工程模式

### 1. 构建远程服务器实现最大覆盖

> *"A remote server is what gives you distribution—it's the only configuration that runs across web, mobile, and cloud-hosted agents."*

远程服务器是分发能力的关键。只有远程配置才能让 Agent 在任何部署环境中访问你的系统。所有主要客户端都针对远程服务器进行了优化。

### 2. 按意图分组工具，而非按端点

> *"Fewer, well-described tools consistently outperform exhaustive API mirrors. Don't wrap your API into an MCP server one-to-one—group tools around intent."*

设计原则：**工具数量少但描述精确，效果远好于穷举式 API 镜像**。

反例：一个 `create_issue_from_thread` 工具比 `get_thread + parse_messages + create_issue + link_attachment` 的组合更好用。Agent 应该能在几次调用内完成任务，而不是拼接大量原始操作。

### 3. 大表面场景使用代码编排

当服务需要数百种操作（如 Cloudflare、AWS、Kubernetes）时，按意图分组的工具集可能无法覆盖。此时的正确模式是：

- 暴露薄工具表面，接受代码输入
- Agent 编写短脚本，服务器在沙箱中针对 API 执行
- 只返回最终结果

Cloudflare MCP server 是参考实现：两个工具（`search` 和 `execute`）覆盖约 2500 个端点，token 消耗约 1K。

### 4. 在需要的地方交付丰富语义

MCP Apps 是第一个官方协议扩展，允许工具返回交互式界面（图表、表单、仪表板），直接渲染在聊天界面中。

使用 MCP Apps 的服务器在采用率和留存率上显著高于只返回文本的服务器。

**Elicitation** 让服务器在工具调用中途暂停，向用户请求输入。两种模式：

- **Form mode**：发送简单 schema，客户端渲染原生表单——用于请求缺失参数、确认破坏性操作或消歧选项
- **URL mode**：将用户导向浏览器——用于完成下游 OAuth、支付或收集任何不应经过 MCP 客户端的凭证

两者都让用户保持在流程中，而非跳转到设置页面。Form mode 被广泛支持；URL mode 在 Claude Code 中支持，更多客户端正在接入。

## 标准化认证：CIMD + Vaults

标准化认证使 MCP 对云端 Agent 真正实用。如果服务器需要 OAuth，最新 MCP spec 支持 **CIMD（Client ID Metadata Documents）** 用于客户端注册——提供快速首次认证流程，显著减少意外重新认证提示。

> *"This is our recommended approach for auth, the capability is supported in MCP SDKs, Claude.ai, and Claude Code, and is being broadly adopted across the industry."*

云端 Agent 在运行时如何持有和复用令牌的问题，由 **Vaults in Claude Managed Agents** 解决：在会话创建时注册用户的 OAuth token，按 ID 引用 vault，平台自动注入正确凭证并代表用户刷新——无需构建密钥存储，无需每次调用传递 token。

## Making MCP Clients Context-Efficient

MCP 标准化了 AI Agent（客户端）如何连接和使用它们需要的工具和数据源（服务器）。构建上下文效率高的客户端有两个关键模式：

### 1. Tool Search：按需加载工具定义

Tool search 延迟加载所有工具到上下文的时机，改为在运行时搜索目录，在需要时拉取相关工具。测试显示，**tool search 通常将工具定义 token 减少 85%+**，同时保持高选择准确性。

### 2. Programmatic Tool Calling：代码中处理工具结果

Programmatic tool calling 在代码执行沙箱中处理工具结果，而非将结果原始返回给模型。这让 Agent 可以在代码中循环、过滤、聚合多次调用，只有最终输出进入上下文。测试显示，**复杂多步工作流的 token 使用减少约 37%**。

这两个模式自然组合：更少的上下文、更少的往返、更快的响应。

## Skills 与 MCP 的互补关系

> *"MCP gives an agent access to tools and data from external systems, while skills teach an agent the procedural knowledge of how to use those tools to accomplish real work."*

MCP 提供对外部系统工具和数据的访问，而 Skills 教授 Agent 如何使用这些工具完成实际工作的程序性知识。最有能力的 Agent 两者都用，Skills 让 MCP 服务器超越少量连接。

两种组合模式：

**模式一：Bundle as Plugin**

Plugins for Claude 将 skills、MCP servers、hooks、LSP servers 和专用子 Agent 打包在一个易于使用的分发方法中。这是统一多个上下文提供者、让 Claude 像领域专家一样行为的最佳方式。

参考：Data plugin for Cowork 包含 10 个 skills 和 8 个 MCP servers，覆盖 Snowflake、Databricks、BigQuery、Hex 等应用。

**模式二：Distribute skills from MCP server**

提供商在 MCP server 旁边发布 skill 越来越常见——Agent 同时获得原始能力和如何使用它们的opinionated playbook。Canva、Notion、Sentry 等已在 Claude 中这样做。

MCP 社区正在积极开发从服务器交付 skills 的扩展，让客户端自动继承相关专业知识，与它依赖的 API 版本保持一致。

## 笔者的判断

**MCP 是云端 Agent 的关键层，不只是又一个协议**。真正的问题是：随着生产 Agent 迁移到云端，我们需要的不只是"能连接"，而是"能规模化连接"。

三个原因让 MCP 在这个场景不可替代：

1. **分布能力**：一次构建，触达所有主流客户端（Claude、ChatGPT、Cursor、VS Code）
2. **上下文效率**：tool search + programmatic tool calling 将 token 消耗降低 85%+
3. **认证基础设施**：CIMD + Vaults 解决了云端 Agent 的 token 管理难题

相比 Direct API 的 M×N 问题和 CLI 的薄层限制，MCP 提供了 proper common layer——这个层是可复用的、协议化的、随着生态发展自动增强的。

> *"When building an integration, if your goal is to have production agents in the cloud reach your system, build an MCP server and make it excellent using the patterns above."*

## 结论

MCP 正在成为生产环境云端 Agent 连接外部系统的事实标准。对于需要构建 MCP 集成的团队，核心建议：

- **优先构建远程服务器**，而非本地配置
- **按意图分组工具**，避免 API 穷举镜像
- **大表面场景使用代码编排**（参考 Cloudflare 模式）
- **交付丰富语义**（MCP Apps、Elicitation）提升采用率
- **采用 CIMD 认证**，使用 Vaults 管理 token

每一次基于 MCP 的集成都在强化这个生态：更少的边缘问题要独自解决，更少的定制集成要维护。

---

**引用来源**：
- Anthropic Engineering Blog: *Building agents that reach production systems with MCP* (2026-04-22)
- URL: https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp