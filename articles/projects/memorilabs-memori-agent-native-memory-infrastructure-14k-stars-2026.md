# MemoriLabs/Memori：让 Agent 记住每一次交互

>📌 **核心命题**：Memori 解决了一个长时 Agent 应用中的根本问题——对话数据如何变成可查询、可演进、可清理的长期记忆。大多数 Agent 框架把 memory 当作附加功能，Memori 把 memory 当作第一等公民来设计。

## 为什么这个项目值得关注

大多数 Agent 框架在处理「记住用户」这件事上做得很粗糙：要么把所有历史消息都塞进 context（昂贵的浪费），要么只在 prompt 里加一句「记住用户的名字」（脆弱的约定）。

Memori 的思路不同——它把对话中的每一轮交互都当成**结构化数据**来处理，自动分类为：

- **Facts**：用户告诉 Agent 的事实（「我叫张三」）
- **Preferences**：用户偏好（「喜欢简洁的回复」）
- **Rules**：用户设定的规则（「不要主动推荐付费功能」）
- **Summaries**：阶段性总结（多轮讨论后的结论）

这种分类的价值在于——当 Agent 需要检索记忆时，查询是有结构的，而不是在一堆对话记录里做向量相似度搜索然后祈祷找到对的。

## 核心架构设计

Memori 是一个 SQL-native、LLM-agnostic 的 memory 层，支持多数据库后端：

```python
from memori import Memori

memori = Memori(api_key="...")

# Agent 与用户对话后，同步到 memory
memori.sync(conversation_id, [
    {"role": "user", "content": "我叫张三，在上海工作"},
    {"role": "assistant", "content": "好的张三，了解了。"}
])

# 下次对话时，Agent 查询 memory
memori.recall(conversation_id, query="用户的名字和所在地")
# → [Fact(name="张三", location="上海"), ...]
```

关键设计决策：

| 维度 | 设计选择 | 原因 |
|------|---------|------|
| **存储模型** | SQL-native（而非 KV 或向量数据库）| 支持精确查询和聚合，memory 可被 SQL 分析 |
| **分类方式** | LLM 自动分类为 Facts/Preferences/Rules/Summaries | 不需要人工标注，结构化检索更可靠 |
| **归因模型** | 支持 attribution（哪个对话、哪个 Agent 写的）| 当 fact 冲突时可以溯源和仲裁 |
| **TTL 支持** | 可以设置 memory 的过期时间 | 符合 GDPR 等数据合规要求 |
| **多数据库** | 支持 Postgres、SQLite、Cloud 等多种后端 | 部署灵活性 |

## 与 interpreter-skills 的互补关系

Round 268 的文章分析了 LangChain Interpreter Skills——把确定性工作流编码为 TypeScript 代码执行。

Memori 和 Interpreter Skills 在 Agent state management 问题上形成**跨时序互补**：

- **Interpreter Skills**：处理 session 内的状态——代码控制流程执行，模型只做高层决策
- **Memori**：处理跨 session 的状态——对话交互变成结构化记忆，下次对话可查询

两者共同指向同一个工程问题：**Agent 的状态管理不能只靠 context window**。长时 Agent 应用需要在多个时标上管理状态——毫秒级（代码执行）、秒级（对话轮次）、天级（跨会话记忆），每层都需要专门的工程机制。

## 竞品对比

| 项目 | Stars | 定位 | SQL 支持 | 多语言 |
|------|-------|------|---------|--------|
| **Memori** | 14,095 | Memory infrastructure | ✅ SQL-native | Python / TypeScript |
| LangChain Memory | - | 框架内置 | ❌ | Python only |
| agent0 memory | - | 框架内置 | ❌ | Python only |
| RAG systems | - | 通用向量检索 | ❌ | 通用 |

Memori 的差异化在于**把 memory 当作独立基础设施层**，而非某个框架的附加功能。这意味着它可以插入任何 LLM client，任何框架都能调用。

## 上手体验

Memori 提供 pip 安装：

```bash
pip install memori
```

官方文档齐全，有 Mintlify 托管的架构文档和博客更新。TypeScript SDK已在 2026年3月 支持。

**适合场景**：
- 需要跨会话记忆的企业级 Agent 应用
- 对数据合规有要求的场景（TTL + attribution）
- 需要对 memory 做 SQL 查询的分析场景

**不适合场景**：
- 简单单轮 chatbot（overkill）
- 需要强类型 schema 的 memory 系统（当前是半结构化分类）

---

**引用来源**：
- [Memori GitHub README](https://github.com/MemoriLabs/Memori)
- [Memori Architecture Docs](https://memorilabs-mememori.mintlify.app/concepts/architecture)
- [Memori Blog](https://memorilabs.ai/blog/)