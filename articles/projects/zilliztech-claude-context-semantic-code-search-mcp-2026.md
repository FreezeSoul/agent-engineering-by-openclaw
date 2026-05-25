# zilliztech/claude-context：让整个代码库成为 Claude Code 的上下文

> 源文：[GitHub README](https://github.com/zilliztech/claude-context)

---

## 核心命题

在大型代码库中让 AI 编码助手「理解」项目上下文，一直是一个工程难题。常见的做法是把整个目录加载到上下文窗口，但这样做成本高昂且效率低下。Claude Context 的解法是：**把代码库存入向量数据库，只在上下文中放入最相关的代码**。这不是一个「让模型更聪明」的问题，而是一个「如何高效传递上下文」的工程问题。

笔者认为，这与 Anthropic 在长时运行 Agent 研究中的核心思路高度一致——**两者都在解决「上下文传递」问题，只是维度不同**：Anthropic 解决的是跨会话的上下文传递，Claude Context 解决的是单次会话中如何高效利用上下文。

---

## 技术架构

### 语义搜索驱动上下文注入

Claude Context 是一个 MCP（Model Context Protocol）插件，它的核心工作流程：

```
用户请求 → 语义搜索代码库 → 向量数据库检索相关代码 → 仅注入相关代码到 Claude 上下文
```

这与传统的「RAG」不同。传统 RAG 强调检索+生成，而 Claude Context 的重点是**控制上下文大小**。它不追求「召回所有可能相关的内容」，而是追求「在有限的上下文窗口内放入最相关的代码」。

### 向量数据库作为上下文缓冲区

用户需要一个向量数据库（推荐 Zilliz Cloud，也支持自托管），代码库被索引后，每次请求时根据语义相关性检索。这意味着：

- **百万行代码库**：可以精确检索，而不需要把所有代码都塞进上下文
- **成本可控**：每次请求只消耗「检索到的代码」对应的 token，而非整个代码库

### MCP 协议集成

Claude Context 通过 MCP 协议与 Claude Code 等主流 AI 编码工具集成。MCP 允许标准化的工具集成，开发者不需要写自定义代码就能连接外部工具。正如 README 所说：

> "Model Context Protocol (MCP) allows you to integrate Claude Context with your favorite AI coding assistants, e.g. Claude Code."

---

## 核心价值点

### 🧠 语义代码搜索：超越关键词匹配

传统代码搜索依赖关键词匹配（如 grep），但开发者的问题往往是语义性的：「这段逻辑在哪里处理用户认证？」，而不是「搜索 'auth'」。Claude Context 的语义搜索能理解代码的语义关系，找到真正相关的代码段。

### 💰 成本控制：大型代码库的必备能力

对于一个 50 万行的代码库，如果每次都把所有代码加载进上下文，成本会非常高。Claude Context 把这个问题反过来解决：**不是减少代码，而是精准选择**。向量数据库索引让你只取最相关的代码段，而非盲目加载。

### 🔌 即插即用的 MCP 生态

MCP 协议的标准性意味着 Claude Context 可以与任何支持 MCP 的工具配合使用。这不只是为 Claude Code 设计，而是为整个 MCP 生态设计。

---

## 适用场景

| 场景 | 为什么 Claude Context 适合 |
|------|--------------------------|
| **大型代码库**（50万+行）| 语义搜索精准定位，而不是大海捞针 |
| **上下文窗口受限** | 只注入最相关的代码，避免上下文溢出 |
| **成本敏感** | 控制 token 消耗，而非每次请求都加载整个代码库 |
| **多语言代码库** | 向量索引不依赖特定语言，可以跨语言检索 |

---

## 与 Anthropic 双轨制的关联

这是本轮 Article 与 Project 形成闭环的核心：

**Article（Anthropic 长时运行 Agent）** 指出：
> "每个新会话开始时都没有上一会话的记忆" — 解决方案是双轨制（Initializer Agent + Coding Agent）+ 结构化的 Feature List + Progress File

**Project（Claude Context）** 解决的是：
> 单次会话中上下文窗口有限的问题 — 解决方案是向量数据库语义检索，只注入最相关的代码

两者共同指向一个核心命题：**上下文传递是 Agent 系统的根本性挑战**，无论是跨会话传递还是单会话内的上下文管理。

---

## 引用

> "Claude Context uses semantic search to find all relevant code from millions of lines. No multi-round discovery needed. It brings results straight into the Claude's context."

— GitHub README, zilliztech/claude-context

> "Instead of loading entire directories into Claude for every request, which can be very expensive, Claude Context efficiently stores your codebase in a vector database and only uses related code in context to keep your costs manageable."

— GitHub README, zilliztech/claude-context

---

## 快速上手

1. **获取 Zilliz Cloud API Key**（有免费额度）
2. **安装 Claude Context**：`npm install -g @zilliz/claude-context-mcp`
3. **配置**：`claude-context setup`，填入 API Key
4. **索引代码库**：`claude-context index ./your-project`
5. **开始编码**：Claude Code 会自动使用语义搜索

---

GitHub: [zilliztech/claude-context](https://github.com/zilliztech/claude-context)
Stars: 持续增长中（首个 Trending 周进入 Top 5）
License: MIT