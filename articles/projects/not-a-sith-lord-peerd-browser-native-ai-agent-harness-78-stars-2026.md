# peerd：浏览器原生的 AI Agent Harness

> 核心判断：peerd 干了一件很聪明的事——用**浏览器本身作为 AI Agent 的运行时和安全模型**，而不是另起炉灶建一个独立的基础设施。它让 AI Agent 的 harness 从「云端服务」变成「浏览器扩展」，这是一个有工程意义的正交创新。

---

## 核心命题

**peerd** 是第一个**浏览器原生的 AI Agent Harness**——一个 Chrome/Firefox 扩展，在用户已有的浏览器中运行完整的 Agent 循环，读取和驱动页面，启动沙箱计算环境（JS Notebooks、WebAssembly Linux VMs），并通过 P2P WebRTC 网络在 Agent 之间共享产出。BYOK（Bring Your Own Key），**无后端、无遥测、云端不在数据路径中**。

![peerd](screenshots/not-a-sith-lord-peerd-20260625.png)

---

## 为什么值得关注

### 1. 架构思路：复用浏览器，而不是替代浏览器

大多数 AI Agent 框架都在建「自己的运行时」——要么是云端服务，要么是本地 CLI。peerd 选择了完全不同的路径：**把浏览器当成 runtime**。

这个思路的聪明之处在于：

- **安全模型现成**：浏览器有 decades 积累的沙箱机制（V8 isolates、WebCrypto、WebAuthn、opaque-origin iframes、Subresource Integrity）
- **用户已经在用**：不需要学习新的工具，不需要配置远程服务器
- **数据不离本地**：API keys 在浏览器里，不在第三方服务器上
- **上下文自然丰富**：浏览器 tab 就是工作上下文，Agent 直接读取用户已经在看的页面

笔者认为，这个架构选择让 peerd 在「轻量级 harness」这个维度上找到了一个极好的定位——比 Tracecat（企业级安全运营平台）轻得多，比直接在本地跑 Claude Code 多了安全隔离和 P2P 协作能力。

### 2. 安全设计：用浏览器的安全模型替代自己写沙箱

peerd 的安全架构文档说明了它如何利用浏览器安全机制：

> "The agent that holds your keys never reads a raw page; a disposable runner with no keys and no network does, and its output comes back fenced as untrusted. Every action the agent drives is verified against the live page before it counts as done."

三层设计：
1. **持 Key 的 Agent**：不直接读页面，持有 API keys
2. **Disposable Runner**：没有 key、没有网络的临时执行器，读原始页面
3. **验证层**：每个 Agent 驱动的动作在生效前都要对照实时页面验证

这个设计把「谁来读页面」和「谁来执行业务逻辑」解耦了——这是 harness 设计中权限分层的经典思路，但实现方式是用浏览器的安全边界而不是自己写容器隔离。

### 3. P2P Agent 协作：WebRTC 原生的 Agent-to-Agent 通信

peerd 的 preview 通道包含了一个 P2P 层，通过 WebRTC 实现 Agent 之间的直接通信：

> "shares what it builds over a peer-to-peer WebRTC network built for agent-to-agent communication."

这是 A2A（Agent-to-Agent）协议的一个浏览器原生实现——不需要服务器中转，Agent 之间直接通信。这在多 Agent 协作场景下有实际价值，特别是当多个 Agent 在做同一个项目的不同部分时。

### 4. 多层次执行环境

peerd 支持多种计算环境的按需启动：

| 环境 | 用途 | 特点 |
|------|------|------|
| **JS Notebooks** | 轻量数据处理、脚本执行 | 浏览器内，无需服务器 |
| **WASM Linux VMs** | 完整 Linux 环境 | WebAssembly 编译，完全隔离 |
| **Client-side Apps** | GUI 应用 | 在浏览器中运行桌面应用 |
| **Live Pages** | 真实 Web 页面 | 直接驱动用户已有的标签页 |

这个层次设计让同一个 Agent 能根据任务复杂度选择合适的执行环境——简单任务用 JS Notebook，复杂任务用 WASM Linux VM。

---

## 使用场景

### 场景 1：个人工作流自动化

用户在浏览器中启动 peerd，告诉它「帮我追踪这个 GitHub issue 的更新，有新评论时通知我并起草回复」，然后关闭浏览器。peerd 在后台持续运行这个任务。

### 场景 2：跨 Agent 协作

两个 peerd 实例通过 WebRTC 直接交换信息——比如一个 Agent 在研究技术方案，另一个 Agent 在写文档，它们可以共享中间产出而不需要通过服务器。

### 场景 3：安全敏感任务的沙箱执行

当 Agent 需要执行来自不可信来源的代码时，WASM Linux VM 提供了完整的隔离环境，代码无法访问宿主机的文件系统或网络。

---

## 竞品对比

| 维度 | peerd | Tracecat | Claude Code |
|------|-------|----------|-------------|
| **运行时** | 浏览器扩展 | 服务器 + Temporal | 本地 CLI |
| **安全模型** | 浏览器沙箱 | nsjail + Temporal | 宿主系统权限 |
| **部署复杂度** | 低（安装扩展）| 高（企业级 infra）| 中（本地安装）|
| **多 Agent 协作** | P2P WebRTC 原生 | MCP 协议 | 无原生支持 |
| **远程访问** | 无需额外设置 | 需要 VPN/网关 | SSH 隧道 |
| **Stars** | 78⭐ | 3,690⭐ | N/A（官方）|

**笔者的判断**：peerd 不是 Tracecat 的竞品，而是填补了「轻量级、浏览器原生」这个空白。对于个人开发者或者小团队，peerd 提供了比 Claude Code 更结构化的 harness 能力，同时比 Tracecat 的部署成本低得多。

---

## 局限性与注意事项

1. **0.x 状态**：experimental beta，breaking changes likely，生产使用需谨慎
2. **Chrome 侧载限制**：macOS/Windows 上 Chrome 不允许非商店扩展（需要手动加载），Firefox 是更平滑的体验
3. **Agent 能力上限**：受限于浏览器环境，不适合需要大量计算资源的任务
4. **预览功能不稳定**：P2P WebRTC 层是 research-grade，不保证稳定性

---

## 快速上手

```bash
# Firefox（推荐）
# 下载 peerd-preview-firefox.xpi，从 release 页面安装

# Chrome (macOS/Windows)
# 1. 下载 peerd-preview-chrome.zip
# 2. 解压
# 3. 打开 chrome://extensions
# 4. 启用 Developer mode
# 5. Load unpacked → 选择解压后的文件夹

# 配置
# 1. 安装后打开扩展
# 2. 输入你的 API key（支持 OpenAI/Anthropic 等 BYOK）
# 3. 开始对话
```

---

**License**: Apache-2.0  
**Stars**: 78（2026-06-25）  
**GitHub**: https://github.com/NotASithLord/peerd  
**官网**: https://peerd.ai  

**关联文章**：本文是 [Codex-maxxing：让 AI 工作持续跨越单次提示](./codex-maxxing-long-running-work-persistent-workspace-harness-2026.md) 的配套项目推荐——peerd 展示了「浏览器原生 harness」如何让 Codex 的长时工作模式真正落地。两者共同构成了「个人级 Harness Engineering」的完整图景：Codex-maxxing 是方法论，peerd 是实现载体。