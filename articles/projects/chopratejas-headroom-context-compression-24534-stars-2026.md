# Headroom：AI Agent 的上下文压缩层

> 本文推荐的项目：[chopratejas/headroom](https://github.com/chopratejas/headroom)
> GitHub 数据：⭐ 24,534 stars | License: Apache-2.0 | Language: Python

---

## 核心命题

**Token 成本是 AI Agent 规模化落地的隐性杀手。** 一个代码审查会话，Claude Code 可以轻松烧掉 50k tokens，其中大部分是工具输出的 verbose 日志。Headroom 的解法：对 AI Agent 读取的所有内容进行压缩，节省 60-95% tokens，同时不损失答案质量。

这不是一个「更便宜的模型」，而是一个「让现有模型更高效」的工程层。

---

## 这个项目解决了一个什么问题

当你在一个 100k 行 monorepo 里问 Claude Code「我们怎么处理 Stripe webhooks」，它有两个糟糕的选择：

- **选项 A**：读取整个代码库（昂贵、慢，context window 直接爆炸）
- **选项 B**：只读前几个文件（50% 的概率答错）

**没有选项 C**——直到 Headroom 出现。

Headroom 提供了第三种路径：**在你向 LLM 发送内容之前，先压缩**。你的代码库索引到向量数据库，每次查询做 hybrid BM25 + dense vector retrieval，只取最相关的代码片段。Agent 拿到的是精简后的 context，账单不会爆炸。

---

## 核心技术架构

```
Your agent (Claude Code, Cursor, Codex, ...)
        │
   prompts / tool outputs / logs / RAG results / files
        ▼
┌────────────────────────────────────────────┐
│           Headroom (本地运行)              │
│  ────────────────────────────────────────  │
│  CacheAligner → ContentRouter → CCR         │
│                ├─ SmartCrusher  (JSON)      │
│                ├─ CodeCompressor (AST)     │
│                └─ Kompress-base  (text)   │
│                                            │
│  Cross-agent memory · headroom learn       │
│  MCP server · Proxy mode                   │
└────────────────────────────────────────────┘
        │
   compressed prompt + retrieval tool
        ▼
  LLM provider (Anthropic · OpenAI · Bedrock · …)
```

**三个压缩算法**：
- **SmartCrusher**：JSON 结构压缩（工具调用参数、日志格式）
- **CodeCompressor**：AST 级别代码压缩（保留语义，丢掉格式噪音）
- **Kompress-base**：基于 HuggingFace 模型文本压缩（通用文本）

**CCR（Reversible Compression）**： originals 缓存在本地，LLM 随时可以调用 `headroom_retrieve` 取回原始内容。**压缩可逆，不丢信息**。

---

## 实测数据（来自 README）

| Workload | 压缩前 tokens | 压缩后 tokens | 节省比例 |
|----------|------------|------------|--------|
| 代码搜索（100 results）| 17,765 | 1,408 | **92%** |
| SRE 事故调试 | 65,694 | 5,118 | **92%** |
| GitHub issue 分类 | 54,174 | 14,761 | **73%** |
| 代码库探索 | 78,502 | 41,254 | **47%** |

**精度保持**（标准 Benchmark）：
- GSM8K Math: **±0.000**（完全不损失）
- TruthfulQA Factual: **+0.030**（反而更高）
- SQuAD v2 QA: **97%**（32% 压缩）
- BFCL Tools: **97%**（32% 压缩）

---

## 使用方式（四种模式）

```bash
# 方式 1：Agent wrap（一行命令包装编码 Agent）
headroom wrap claude          # Claude Code
headroom wrap codex           # Codex
headroom wrap cursor          # Cursor

# 方式 2：Proxy 模式（零代码改动）
headroom proxy --port 8787    # 任何 OpenAI 兼容客户端

# 方式 3：库模式（内嵌到 Python/TypeScript）
from headroom import compress
compressed = compress(messages)

# 方式 4：MCP Server（工具级压缩）
headroom_compress      # 压缩工具
headroom_retrieve      # 取回原始内容
headroom_stats        # 统计面板
```

---

## 与 Claude Code 的关联

在 Round356 中，我们分析了 Anthropic 的 [Managed Agents 架构](/articles/deep-dives/anthropic-managed-agents-decoupling-brain-hands-2026.md)——Brain / Hands / State 三层解耦。

**State 层的问题**：解耦后，会话上下文（State）的体积管理成为新瓶颈。当 Brain 可以远程调用 Hands 时，State 层的压缩直接影响每次 API 调用的 token 成本。

Headroom 正是解决这个问题的工程工具：
- **CacheAligner**：稳定前缀，让 provider 的 KV cache 真正命中（而不是每次都是 cache miss）
- **Cross-agent memory**：跨 Agent 共享压缩后的 context（Claude、Codex、Gemini 之间不重复缓存）
- **`headroom learn`**：从失败会话中提取模式，自动写纠正到 `CLAUDE.md` / `AGENTS.md`

---

## 适用场景

**适合用 Headroom**：
- 大型代码库（50k+ 行）的 AI coding 场景
- 高频调用 API 的 production Agent 系统（token 成本敏感）
- 多 Agent 协作项目（跨 Agent 共享 context 压缩）
- 工具输出 verbose 的自动化场景（SRE 调试、日志分析）

**不适合**：
- 小型项目（context window 够用，压缩带来的延迟不值得）
- 需要保留原始格式的场景（CCR 虽然可逆，但有额外调用开销）
- 对延迟极端敏感的场景（压缩有 ~10-50ms 的额外处理时间）

---

## 引用

> "Headroom compresses everything your AI agent reads — tool outputs, logs, RAG chunks, files, and conversation history — before it reaches the LLM. Same answers, fraction of the tokens."
>
> — [chopratejas/headroom README](https://github.com/chopratejas/headroom)

> "Instead of loading entire directories into Claude for every request, which can be very expensive, Claude Context efficiently stores your codebase in a vector database and only uses related code in context."
>
> — [chopratejas/headroom README](https://github.com/chopratejas/headroom)（引用类似项目的设计哲学）

---

## 总结

Headroom 的价值主张非常清晰：**不是更便宜，是更高效**。在 token 成本成为 Agent 规模化落地瓶颈的时代，压缩层是一个工程上必然出现的组件。

从架构角度看，它和 Anthropic 的 Brain/Hand/State 解耦是同一条思路的不同层次：Anthropic 解耦的是组件边界，Headroom 解耦的是数据体积。两者共同指向同一个目标——让 Agent 系统在生产环境里真正可持续。

**安装方式**：`pip install "headroom-ai[all]"` 或 `npm install headroom-ai`