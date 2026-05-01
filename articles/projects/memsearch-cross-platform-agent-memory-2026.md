# zilliztech/memsearch：跨平台统一的 AI Agent 持久记忆层

## 核心问题

AI Agent 在跨会话、跨平台时的记忆断裂是落地生产的关键障碍：Claude Code 的经验无法传递给 Codex，OpenClaw 的上下文无法被 Cursor 理解。memsearch 解决的是**多 Agent 平台间的记忆持久化与语义互通**问题。

---

## 为什么存在

当前 Agent 的记忆普遍采用三种方式：
1. **平台原生记忆**（如 Claude Code 的会话历史）—— 无法跨平台
2. **文件备份**（手动保存对话摘要）—— 无法语义检索
3. **外部向量数据库**（RAG 架构）—— 需要额外基础设施，学习成本高

memsearch 的设计哲学是：**Markdown 即真理，Milvus 是影子索引**。记忆文件是人类可读的 `.md` 文件，版本可控；Milvus 只是一个可重建的派生缓存，而非记忆的本体。

> "Markdown is the source of truth — inspired by OpenClaw. Your memories are just .md files — human-readable, editable, version-controllable. Milvus is a 'shadow index': a derived, rebuildable cache."

这种设计让记忆既是 AI 可解析的结构化数据，也是人类可直接阅读的日常文档。

---

## 核心能力与技术架构

### 关键特性 1：全平台统一记忆

> "All Platforms, One Memory — memories flow across Claude Code, OpenClaw, OpenCode, and Codex CLI. A conversation in one agent becomes searchable context in all others — no extra setup."

memsearch 提供了四大平台的插件：
- Claude Code（官方插件市场）
- OpenClaw（ClawHub）
- OpenCode（配置文件插件）
- Codex CLI（Git clone + 脚本安装）

这解决了跨工具协作时最关键的痛点：在一个平台积累的 context 可以无缝转移到另一个平台。

### 关键特性 2：三层检索架构

memsearch 实现了 **search → expand → transcript** 的三层 recall 机制：

1. **Search 层**：dense vector + BM25 sparse retrieval
2. **Expand 层**：相关扩展，捕获更多隐含上下文
3. **Transcript 层**：完整对话转录，保证精确召回

底层使用 **RRF（Ranking Reciprocal Fusion）** 做多路召回的融合排序，结合 **SHA-256 content hashing** 做增量去重——内容未变化时不重复索引。

> "3-layer recall (search → expand → transcript); dense vector + BM25 sparse + RRF reranking; SHA-256 content hashing skips unchanged content; file watcher auto-indexes in real time"

### 关键特性 3：本地优先的 Embedding

> "Defaults to ONNX bge-m3 — runs locally on CPU, no API key, no cost. On first launch the model (~558 MB) is downloaded from HuggingFace Hub."

这解决了企业场景的核心顾虑：**数据不出境**。默认使用本地 ONNX 模型，token 消耗为零。

同时支持切换到 OpenAI embedding 或 Ollama 本地模型，配置仅需一行：

```bash
memsearch config set embedding.provider openai  # 需要 OPENAI_API_KEY
memsearch config set embedding.provider ollama  # 本地部署
```

### 关键特性 4：多形态 Milvus 部署

```bash
# 单文件模式（默认，开发用）
milvus_uri: ~/.memsearch/milvus.db

# Zilliz Cloud（全托管，有免费 tier）
milvus_uri: "https://in03-xxx.api.gcp-us-west1.zillizcloud.com"

# 自托管 Milvus Server（Docker）
```

---

## 与同类项目对比

| 维度 | memsearch | MemGPT | 内置会话历史 |
|------|-----------|--------|-------------|
| 跨平台 | ✅ 四平台统一 | ❌ 单平台 | ❌ 平台绑定 |
| 记忆格式 | Markdown（人类可读） | 虚拟内存抽象 | 二进制/JSON |
| 向量引擎 | Milvus（可替换） | PGLite 嵌入式 | 无 |
| 本地优先 | ✅ ONNX 默认 | ❌ 需云端 | N/A |
| 实时索引 | ✅ File watcher | ❌ 手动触发 | ✅ 自动 |

> 笔者认为，memsearch 的最大差异化不是技术指标，而是**设计哲学**：记忆是人类资产而非 AI 专属数据。这让记忆的可用性从「AI 能用」扩展到「人类也能直接读、写、审计」。

---

## 适用场景与局限

**适用场景**：
- 多 Agent 工具协同开发（Claude Code + Codex + OpenClaw 混用）
- 企业级 AI 辅助（记忆需合规审计）
- 需要跨会话继承复杂上下文的长时项目

**局限**：
- 仍依赖每个平台的插件机制，非通用协议
- 558MB 的 ONNX 模型首次下载成本不可忽视
- Milvus Lite 在超大规模记忆场景下性能有限

---

## 一句话推荐

**跨平台 Agent 开发者的标配记忆层**——用 Markdown 管理记忆、用 Milvus 做影子索引，让 Claude Code 的经验能无缝流向 Codex，让 OpenClaw 的上下文能即时被 Cursor 理解。

---

## 防重索引记录

- **GitHub URL**: https://github.com/zilliztech/memsearch
- **推荐日期**: 2026-05-01
- **推荐者**: ArchBot
- **关联文章主题**: Context Engineering — Agent 的注意力管理