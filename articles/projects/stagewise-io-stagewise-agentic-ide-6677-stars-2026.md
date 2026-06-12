# Stagewise：让 Agent 在浏览器里直接「动手」的开发环境

> **核心命题**：大多数 AI Coding 工具把 Agent 当作「在 IDE 旁边建议代码的助手」，但 Stagewise 走的是另一条路——让 Agent 直接在浏览器里运行，有完整的 console 和 debugger 访问权，能真正做修改而不只是给建议。

这是笔者第一次看到有人把"Agentic IDE"这个概念认真做出来的开源项目。

---

## 为什么这个方向值得注意

传统的 AI Coding 工具（Claude Code、Cursor、Copilot）本质上是在你的 IDE 旁边放一个"聪明的建议者"——它能生成代码，但执行的闭环在人类手里：人类审查代码、人工作出决定、人类点击保存。

Stagewise 的设计哲学完全不同：**Agent 不只是建议，而是直接操作**。它运行在浏览器里，能访问 devtools console、network 面板、调试器——这些是传统 CLI Agent 工具根本碰不到的东西。

这意味着什么？

1. **所见即所得**：Agent 直接看到页面渲染结果，不需要猜测
2. **真正的调试循环**：Agent 可以调用 console.log、检查网络请求、设置断点
3. **临时测试 → 永久修改**：可以先做临时修改看效果，再决定是否合并到代码库

笔者认为，这种「在真实环境中操作」的设计哲学比「生成代码后由人类部署」更接近真正的 Agent 形态。

---

## 核心功能解析

### 1. 浏览器内 Agent 操作

Stagewise 的 Agent 运行在浏览器 Tab 里，而不是在后台跑一个 headless 进程。这意味着：

- **DOM 直接访问**：Agent 可以读取和修改 DOM，不需要通过代码生成
- **Console 集成**：Agent 能看到 console 输出，能捕捉运行时错误
- **Network 拦截**：能查看 API 请求/响应，用于调试数据流

README 原话：
> "Work with a coding agent that has full access to your tab's console and debugger"

这个描述很朴实，但它解决了一个实际问题：大多数 AI coding 工具只能看代码，不能看运行结果。

### 2. 反向工程能力

Stagewise 提供了一个独特功能：**反向工程任何网站的组件、样式系统和配色方案**。这对笔者来说是一个意外惊喜——这意味着 Agent 可以「研究」现有网站的实现，然后生成风格一致的新代码。

这不只是「查看源代码」的功能，而是结构化的解析：
- 识别组件结构
- 提取样式系统（CSS 变量、主题）
- 分析配色方案

### 3. 多模型支持

Stagewise 支持大量模型提供商，包括：

| 类别 | 提供商 | 代表模型 |
|------|--------|---------|
| **主流** | Anthropic | Fable 5, Opus 4.8, Sonnet 4.6, Haiku 4.5 |
| **主流** | OpenAI | GPT-5.5, GPT-5.4, Codex |
| **主流** | Google | Gemini 3.1 Pro, Gemini 3 Flash |
| **中国** | Moonshot AI | Kimi K2.6, Kimi K2.5 |
| **中国** | Alibaba | Qwen3-32B, Qwen3-Coder 30B |
| **中国** | DeepSeek | DeepSeek V4 Pro, DeepSeek V4 Flash |
| **中国** | MiniMax | MiniMax M3, M2.7 |

特别值得注意的是它对中国模型的支持——Kimi、Qwen、DeepSeek、MiniMax 都被列为核心支持厂商。这对于国内开发者来说是好消息。

### 4. 定价策略

| 计划 | 价格 | 说明 |
|------|------|------|
| Free | $0/mo | 有限访问所有模型 |
| Pro | $20/mo | 6倍用量上限 |
| Ultra | $200/mo | 75倍用量上限 |

这个定价很有趣——免费层存在但有限制，$20/mo 的 Pro 层对个人开发者来说很合理，$200/mo 的 Ultra 层则是给高强度使用者准备的。

---

## 技术观察

### Agentic IDE vs AI-in-IDE

这是两种不同的范式：

| 维度 | AI-in-IDE（如 Cursor、Claude Code） | Agentic IDE（Stagewise） |
|------|-----------------------------------|------------------------|
| **Agent 运行位置** | CLI / 后台进程 | 浏览器 Tab |
| **上下文获取** | 代码 + 文件系统 | DOM + Console + Network |
| **执行方式** | 生成代码，人类确认 | 直接操作，人类监督 |
| **调试能力** | 间接（看错误信息） | 直接（console/debugger）|
| **适用场景** | 复杂代码生成 | 快速修复/原型/研究 |

笔者认为，这两种范式不是替代关系，而是适用于不同场景：

- **AI-in-IDE**：复杂系统开发、需要架构决策的场景
- **Agentic IDE**：快速修复、UI 调试、反向工程、研究性任务

### 技术栈

- **语言**：TypeScript（整个项目用 TS 编写）
- **许可**：AGPL-3.0（GitHub API SPDX 确认）— Network copyleft 限制：如果你 fork 并以服务形式对外提供，需要开源
- **分发形式**：桌面应用（通过 stagewise.io 下载）

---

## 与竞品对比

| 项目 | 类型 | Stars | 核心差异 |
|------|------|------|---------|
| **Stagewise** | Agentic IDE | 6677 | 浏览器内 Agent，完整调试能力 |
| **Cursor** | AI-in-IDE | 131949 | 最流行的 AI coding IDE |
| **Claude Code** | CLI Agent | 131949 | Anthropic 官方 CLI 工具 |
| **Copilot** | IDE 插件 | 大规模 | Microsoft 官方集成 |

Stagewise 的差异化在于「让 Agent 操作浏览器而不是生成代码」。这是一个独特的角度，但它还处于早期阶段（6677 stars vs Cursor 的 131949 stars）。

---

## 笔者的判断

Stagewise 的核心价值不是「另一个 AI coding 工具」，而是它提出的问题：**如果 Agent 能在浏览器里直接操作，而不是只生成代码，它能做什么不一样的事？**

这个问题的答案可能包括：
1. **更快的调试循环**：Agent 直接看到 console 错误，不需要人类翻译
2. **真正的 UI 研究**：Agent 能分析和复制网站的样式系统
3. **更短的反馈周期**：临时修改 → 预览 → 决定是否保留

笔者认为，Agentic IDE 这个方向值得关注，但它是否能在长期与 AI-in-IDE 竞争还需要观察。Stagewise 目前 6677 stars 的体量说明它已经找到了一部分用户，但离成为主流还有距离。

如果你做的是 UI 开发、页面调试、或者快速原型，Stagewise 值得一试。如果你做的是复杂系统架构开发，Cursor 或 Claude Code 仍然是更成熟的选择。

---

**引用来源**：
- Stagewise README, https://github.com/stagewise-io/stagewise (AGPL-3.0, 6,677⭐, 验证于 2026-06-12 via GitHub API)
- 配对 Article: `articles/evaluation/ai-agent-eval-playbook-five-layer-framework-2026.md` — Stagewise 的浏览器内 console/debugger 访问权是 Eval Playbook 第四层（过程可观测）的工程实现案例