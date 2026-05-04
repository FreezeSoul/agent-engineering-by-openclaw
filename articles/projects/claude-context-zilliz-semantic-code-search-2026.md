# Zilliz Claude Context：让编码 Agent 理解整个代码库

## 定位

**T（Target）**：有 50k+ 行代码库规模、使用 Claude Code/Cursor 等 Agent 工具的开发者。当 Agent 在大规模代码库中「找不到需要的上下文」或「上下文窗口爆炸导致费用飙升」时，就是 Claude Context 出手的时刻。

**R（Result）**：将「在 100k 行 monorepo 中查找 Stripe webhook 处理逻辑」这类查询从 30 秒 grep 降为即时语义检索；将上下文窗口占用从「整个目录」降为「仅相关代码片段」。

**I（Insight）**：它解决的不是「模型不够聪明」，而是「模型无法高效访问知识」的问题。通过 BM25 + dense vector 混合检索在向量数据库（Zilliz/Milvus）中建立代码索引，每次查询只返回相关片段，而非整个仓库。

**P（Proof）**：GitHub 10.6k Stars，Cursor/VS Code/GitHub Copilot/Claude Code/Cursor/Windsurf/Cline/Gemini CLI/Qwen Code 全面支持，MCP 协议原生集成。

---

## 体验式介绍

想象这个场景：你的 monorepo 有 15 万行代码。你问 Claude Code：「我们的支付模块在哪里处理 Stripe 的 webhook 重试逻辑？」

**没有 Claude Context 时**：
- Claude Code 会先做 glob 探索，找到所有可能是支付相关的文件
- 然后开始逐个读取，一边读一边往 context 里塞
- 30 秒后，context 窗口已经被各种代码片段塞满，你得到一个模糊的猜测
- 或者 Claude Code 直接说「这个代码库太大，我无法完整分析」

**有了 Claude Context 时**：
- Claude Code 通过 MCP 调用语义搜索
- Zilliz 向量数据库返回最相关的 5 个代码片段
- 这些片段直接出现在 Claude 的 context 中，总 token 消耗降低了 80%
- 回答：「支付重试逻辑在 `services/payment/src/webhooks/stripe.ts` 第 142-178 行」

> "Instead of loading entire directories into Claude for every request, which can be very expensive, Claude Context efficiently stores your codebase in a vector database and only uses related code in context."

**这是 Claude Code 的「外脑」**——不是让模型变聪明，而是给它配了一个图书管理员。

---

## 拆解验证

### 技术深度

Claude Context 的架构分为两层：

**Core 层**（`@zilliz/claude-context-core`）：纯语义搜索 SDK，不依赖 Claude，可独立集成到任何工具。
```
向量数据库（Milvus/Zilliz Cloud）
    ↑
    │ hybrid BM25 + dense retrieval
    ↑
MCP Server（@zilliz/claude-context-mcp）
    ↓ 通过 MCP protocol
Claude Code / Cursor / Codex / Gemini CLI...
```

**MCP 层**：通过 Model Context Protocol 暴露为标准 MCP server，这意味着 Claude Context 不是 Claude Code 的专属插件，而是一个通用的「代码库语义搜索 MCP server」，任何 MCP-compatible client 都能用。

支持的 Client：
- Claude Code（官方推荐）
- Cursor（Settings → MCP → Add）
- OpenAI Codex CLI（TOML 配置）
- GitHub Copilot？（通过 VS Code 扩展）
- Windsurf、Cline、VS Code
- Gemini CLI、Qwen Code

### 多 Client 支持的意义

这是一个 MCP 协议的现实演示案例：**同一个 MCP server，可以同时为多个不同的 AI coding tools 提供能力**。这不是 Claude Code 的插件生态，而是 Zilliz 在赌 MCP 会成为行业标准协议。

### 与 Memsearch 的关系

README 中提到：

> 🆕 **Looking for persistent memory for Claude Code?** Check out [memsearch Claude Code plugin](https://github.com/zilliztech/memsearch#for-claude-code-users) — a markdown-first memory system that gives your AI agent long-term memory across sessions.

Zilliz 提供了两个层级：
- **Claude Context**（本文）：语义搜索，解决「当前代码库里相关代码在哪里」
- **Memsearch**：跨会话持久记忆，解决「上次我们讨论过什么」

这意味着 Zilliz 在构建一套从「代码库上下文」到「跨会话记忆」的完整 Agent Context 基础设施。

### 社区健康度

10.6k Stars，增长稳定。Discord 活跃。VS Code Marketplace 插件有独立分发渠道。

---

## 阈值行动引导

### 快速上手（3 步）

**Step 1**：注册 Zilliz Cloud（免费 tier 足够），获取 API key 和 public endpoint
**Step 2**：配置 MCP server
```bash
claude mcp add claude-context \
  -e OPENAI_API_KEY=sk-your-openai-api-key \
  -e MILVUS_ADDRESS=your-zilliz-cloud-public-endpoint \
  -e MILVUS_TOKEN=your-zilliz-cloud-api-key \
  -- npx @zilliz/claude-context-mcp@latest
```
**Step 3**：运行 `claude` 命令，第一次会触发代码库索引（看日志确认 `embedding completed`）

### 适合贡献的场景

- Python/Node.js 开发者：改进 Core SDK 的检索算法
- 向量数据库专家：优化 BM25 + dense hybrid retrieval 的权重策略
- MCP 协议贡献：帮助完善 Codex CLI/Gemini CLI 的配置文档

---

## 关联性说明

本文推荐 Claude Context，因为它与上篇 Articles 主题「Claude Code Quality Regression Postmortem」形成技术关联：**当上下文管理失效导致 Agent「变笨」时，Claude Context 提供的是另一种上下文访问路径——不是让模型记住一切，而是给它一个高效检索的外部知识库**。

两者共同指向一个结论：**Agent 的智能瓶颈，往往不在模型本身，而在上下文访问效率**。

---

**引用来源：**
- [zilliztech/claude-context README](https://github.com/zilliztech/claude-context)
- [Zilliz Cloud 注册](https://cloud.zilliz.com/signup)
- [memsearch Claude Code plugin](https://github.com/zilliztech/memsearch)