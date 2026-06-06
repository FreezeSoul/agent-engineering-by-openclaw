# earendil-works/pi：最小化 Agent Harness 的模块化实现

> **核心命题**：Pi 证明了「最小化 Harness + 模块化扩展」不是设计理想，而是一个可工作的工程现实——它用 60K stars 和一个活跃的扩展生态说明，你不需要把一切都塞进框架，框架本身只需要把 Agent Loop 的核心跑起来，剩下的交给扩展。

---

## 为什么这个项目值得关注

大多数 Agent 框架走的是「 batteries-included」路线：一个框架把所有东西打包进去——记忆管理、工具调用沙箱、权限系统、模型层、UI。好处是开箱即用，坏处是当你想换掉任何一个部分时，发现到处是耦合。

Pi 走的是另一条路。它的核心包只有四个：

| Package | 职责 |
|---------|------|
| `@earendil-works/pi-coding-agent` | 交互式 Coding Agent CLI |
| `@earendil-works/pi-agent-core` | Agent 运行时，工具调用和状态管理 |
| `@earendil-works/pi-ai` | 统一的多 provider LLM API（OpenAI/Anthropic/Google…）|
| `@earendil-works/pi-tui` | 终端 UI 库，差分渲染 |

**没有记忆系统，没有内置权限层，没有沙箱**——这些全部作为扩展存在，或者交给你自己通过容器化解决。这不是功能缺失，这是设计选择：框架只负责让 Agent Loop 转起来，剩下的每一样东西都可以按需替换或扩展。

LangChain 的「How to Build a Custom Agent Harness」文章在描述 `create_agent` 的设计哲学时，明确引用了 pi.dev 作为参考：

> "Our philosophy is similar to that of Pi, a highly configurable coding agent harness. create_agent just implements the core agent loop, and it exposes middleware as a primitive for customization."

这不是偶然的相似——Pi 的设计哲学影响了 LangChain 对 Harness 的建模方式。

---

## 权限与安全的工程选择

Pi 有一个工程决策值得单独拿出来说：**它默认不包含权限系统**。

README 的原文：

> "Pi does not include a built-in permission system for restricting filesystem, process, network, or credential access. By default, it runs with the permissions of the user and process that launched it."

这和大多数 Agent 框架的做法完全相反——那些框架默认把权限收紧，然后让你一点点放开。Pi 的逻辑是：**如果你需要边界，自己通过容器化实现**。它甚至提供了三套容器化方案：

**OpenShell**：把整个 pi 进程跑在策略控制的沙箱里。

**Gondolin extension**：pi 和 provider 认证留在 host 上，内置工具和 `!` 命令路由到本地 Linux micro-VM。

**Plain Docker**：最简单粗暴的隔离方案。

这是一个诚实的设计声明：框架不假装自己的权限模型适用于所有场景，需要强隔离你自己搞定。这个决策让框架本身保持简单，但也把安全工程的责任明确转移给了使用者。

---

## 扩展生态：npm 包即插件

Pi 的扩展系统不是插件协议或专有 API——就是 npm 包。你写一个 package，上传到 npm 或 git，别的 pi 用户就能装。这让扩展的分发和复用回归到 JavaScript 生态的标准实践。

已有的扩展示例：
- **pi-review**（229 stars）：代码审查扩展
- **pi-chat**（Discord/Telegram bridge）：把聊天频道桥接到一个沙箱化的 pi session，每个频道连接到自己的 Gondolin micro-VM

pi-chat 的设计尤其有意思——它把「聊天消息 → Agent 执行 → 结果回传」做成了一个标准模式，而不需要改 pi 本身。这种扩展方式说明，当框架足够薄，扩展接口就足够自然。

---

## 技术细节

**语言**：TypeScript（93.5%），少量 JavaScript/CSS

**License**：MIT

**创建时间**：2025-08-09（相对年轻，但已经 60K stars）

**模块化设计**：所有 package 可以独立使用——你不需要用 pi-coding-agent 也可以单独用 pi-ai 或 pi-agent-core。这与大多数框架的「全量或不用」设计形成对比。

**容器化文档**：有专门的一篇 [containerization.md](packages/coding-agent/docs/containerization.md) 讲三种隔离模式，这是很多框架欠缺的工程细节。

---

## 与同类对比

| 维度 | Pi | LangChain Deep Agents | Claude Code |
|------|----|----|-----|
| **权限模型** | 无内置（靠容器化）| Middleware 权限层 | Classifier-based auto-review |
| **记忆系统** | 无（自己扩展）| 内置 | 内置 |
| **扩展方式** | npm/git 包 | Middleware + Skills | MCP Server |
| **核心复杂度** | 极简 | 中等 | 黑盒 |
| **Stars** | 60K | 24K | N/A（官方）|

Pi 的极简哲学意味着上手成本最低，但也意味着你需要自己组装更多东西。如果你想要一个「框架负责最核心的，剩下的你自己来」的分界线，Pi 可能是最干净的起点。

---

## 如何上手

```bash
npm install -g @earendil-works/pi-coding-agent
pi --help
```

配置 LLM provider（通过环境变量或交互式设置），然后就可以开始交互。

如果需要更强的隔离：
```bash
docker run -it ghcr.io/earendil-works/pi-coding-agent
```

---

## 引用

> "Pi does not include a built-in permission system for restricting filesystem, process, network, or credential access. By default, it runs with the permissions of the user and process that launched it."

— [earendil-works/pi README.md](https://github.com/earendil-works/pi)

> "Our philosophy is similar to that of Pi, a highly configurable coding agent harness. create_agent just implements the core agent loop, and it exposes middleware as a primitive for customization."

— [LangChain Engineering, "How to Build a Custom Agent Harness"](https://blog.langchain.com/how-to-build-a-custom-agent-harness)
