# MemPalace: 让 AI 记忆回归本地

**GitHub**: [MemPalace/mempalace](https://github.com/MemPalace/mempalace)  
**Stars**: 54,886 ⭐ | **License**: MIT | **语言**: Python  

---

## 核心命题

AI Agent 的记忆系统长期以来面临一个根本矛盾：要么把上下文全塞进 prompt（成本高、延迟大），要么靠 API 调用做语义检索（依赖云服务、数据主权存疑）。**MemPalace 给出了一个截然不同的答案——本地优先、逐字存储、零 API 调用，96.6% R@5 召回率**，而且完全免费、开源。

笔者认为，这代表了 AI 记忆系统的一种重要方向：**不依赖云服务的本地记忆层**，特别适合对数据隐私有要求或需要离线工作的场景。

---

## 为什么这个项目值得关注

### 1. 逐字存储，而非摘要

现有大多数 AI 记忆系统走的路线是「提取-压缩-存储」：让 LLM 把对话精华抽取出来存入向量数据库。这条路有问题：

- **信息损失不可逆**：摘要永远无法还原完整上下文
- **依赖 LLM 调用**：每次存储都要花钱
- **检索质量受限于摘要质量**：如果摘要没抓住重点，搜到了也白搭

MemPalace 的思路完全不同：**verbatim storage**——把对话原文原封不动存进去，检索靠语义向量搜索，但底本永远是完整的。

> "MemPalace stores your conversation history as verbatim text and retrieves it with semantic search. It does not summarize, extract, or paraphrase."

这意味着你随时可以调取原始内容，而不是只能看到「记忆」二手加工后的版本。

### 2. 结构化索引：Wings / Rooms / Drawers

MemPalace 没有把记忆平铺成一个向量库，而是引入了一套**空间记忆（spatial memory）** 隐喻：

| 概念 | 对应 | 作用 |
|------|------|------|
| **Wings** | 人 / 项目 | 跨对话关联同一主体的所有记忆 |
| **Rooms** | 主题 / 话题 | 同一领域的知识集合 |
| **Drawers** | 原始内容 | 具体的对话/文档/笔记 |

这个结构让检索可以**带作用域**（scoped search），而不是每次都对整个语料做相似度搜索。比如：「查找我和张三关于项目 Y 的讨论」——这比平铺向量库精准得多。

### 3. 可插拔后端：ChromaDB / sqlite_exact / Qdrant / pgvector

```python
# 本地精确向量（sqlite_exact）
mempalace mine ~/projects/myapp --backend sqlite_exact

# Qdrant 向量数据库
MEMPALACE_QDRANT_URL=http://localhost:6333 \
  mempalace mine ~/projects/myapp --backend qdrant

# Postgres + pgvector
mempalace mine ~/projects/myapp --backend pgvector
```

接口定义在 `mempalace/backends/base.py`，任何实现了抽象接口的后端都可以即插即用。这种设计避免了厂商锁定——你今天用 ChromaDB，明天想迁移到 Qdrant，不需要改业务代码。

### 4. MCP Server：让 AI Agent 直接调用记忆

MemPalace 提供了 MCP（Model Context Protocol）服务器，这意味着它可以无缝接入 Claude Code 等支持 MCP 的 AI 编程工具：

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-v", "mempalace-data:/data", "mempalace"]
    }
  }
}
```

对于 AI Coding 场景来说，这意味着：**Agent 可以主动查询历史对话和项目笔记**，而不只是依赖当前对话的上下文窗口。

### 5. 性能数字有说服力

MemPalace 声称在 LongMemEval 基准上达到 **96.6% R@5**（Recall@5），即前 5 个检索结果中包含正确答案的概率超过 96%。这在同类本地记忆系统中是相当亮眼的数字。

---

## 与主流方案的对比

| 维度 | MemPalace | Pinecone | ChromaDB（纯向量库）|
|------|-----------|----------|---------------------|
| 存储方式 | 逐字原文 | 需自行处理 | 需自行处理 |
| 数据位置 | 本地优先 | 云服务 | 本地/云 |
| API 调用 | **零调用** | 每次存储/检索 | 取决于部署 |
| 索引结构 | Wings/Rooms/Drawers | 平铺 | 平铺 |
| MCP 支持 | ✅ 原生 | ❌ | ❌ |
| R@5 基准 | 96.6% | 未公布 | 未公布 |

笔者认为，MemPalace 和纯向量数据库不是竞争关系——MemPalace 本身底层就支持 ChromaDB/Qdrant 作为后端，它的差异化在于**记忆抽象层**，而不是向量检索本身。

---

## 适用场景

✅ **强烈推荐**：
- 需要本地部署、对数据主权有要求的 AI 应用
- AI Coding 工具（Claude Code、Cursor）需要长期记忆项目上下文
- 个人/团队知识管理，需要跨对话关联同一主题

❌ **不适合**：
- 需要大规模云端同步的多端协作场景（MemPalace 是本地优先设计）
- 超大规模语料库（当前架构更适合个人/小团队级别）

---

## 快速上手

```bash
# 用 uv 安装（推荐）
uv tool install mempalace

# 初始化项目记忆库
mempalace init ~/projects/myapp

# 导入项目文件到记忆库
mempalace mine ~/projects/myapp

# 语义搜索
mempalace search "为什么 GraphQL"

# MCP 服务器模式（供 AI Agent 调用）
docker run -i --rm -v mempalace-data:/data mempalace
```

---

## 关键文件参考

- 架构设计：[mempalace/backends/base.py](https://github.com/MemPalace/mempalace/blob/develop/mempalace/backends/base.py) — 后端抽象接口
- 概念解释：[mempalaceofficial.com/concepts/the-palace](https://mempalaceofficial.com/concepts/the-palace.html)
- MCP 集成：[官方文档](https://github.com/MemPalace/mempalace#wire-it-into-an-mcp-client)

---

## 笔者的判断

MemPalace 解决了一个真实痛点：**AI Agent 的记忆不应该是黑箱，也不应该依赖云服务**。当记忆系统能跑在本地、存储原始内容、提供结构化索引时，AI 的推理才真正有据可查。

它的设计理念和当前「一切皆向量」的潮流形成了有趣的反差——**结构化存储 + 向量检索**的组合，可能是比纯向量更务实的路线。

如果你在构建需要长期记忆的 AI 应用，或者想让 Claude Code / Cursor 这类工具记住你的项目上下文，MemPalace 值得认真评估。