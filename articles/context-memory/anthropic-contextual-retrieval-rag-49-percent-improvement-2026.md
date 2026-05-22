# Anthropic Contextual Retrieval：RAG 检索失败率降低 49% 的工程实践

> **来源**：[Anthropic Engineering Blog](https://www.anthropic.com/engineering/contextual-retrieval)（2024-09 featured）
> **主题**：Contextual Retrieval——通过 Contextual Embeddings 和 Contextual BM25 双重技术，大幅提升 RAG 检索精度
> **适用场景**：RAG 系统优化；知识库问答；Context Engineering；Embedding 模型调优

---

## 核心问题：传统 RAG 的「上下文丢失」顽疾

RAG（Retrieval-Augmented Generation）是业界将知识库接入 LLM 的标准方案。但 Anthropic 指出传统 RAG 有一个被长期忽视的根本缺陷：**切块（chunking）后丢失了上下文**。

一个典型的 RAG 流程：
1. 将文档切成 200-500 token 的小块
2. 用 Embedding 模型将每块转为向量
3. 检索时用语义相似度匹配

问题出在第 1 步：**每块脱离原始文档后，含义变得模糊**。一个代码块的 embedding 可能只编码了「发送通知」这个动作，但原始上下文中它是「错误处理流程中向 TS-999 告警系统发送通知」——这两个含义相差甚远。

> *"Traditional RAG solutions remove context when encoding information, which often results in the system failing to retrieve the relevant information from the knowledge base."*
> — Anthropic Engineering Blog

---

## 解决方案：Contextual Retrieval 双重机制

Anthropic 提出的 Contextual Retrieval 不是单一技术，而是两套互补机制的组合：

### 1. Contextual Embeddings

核心思想：**在生成 embedding 时，将块所属的原始文档上下文一并注入**。

传统方式：
```
chunk = "发送通知给用户"
embedding(chunk) → 语义模糊
```

Contextual 方式：
```
chunk = "发送通知给用户"
context = "在错误处理流程中，当系统检测到 TS-999 错误码时，发送通知给用户"
combined = f"context: {context}\nchunk: {chunk}"
embedding(combined) → 语义精确
```

### 2. Contextual BM25

BM25 是基于词频的经典检索算法（TF-IDF 的改进版），对精确匹配（如错误码、特定术语）非常有效。传统 BM25 的问题同样是**切块后词频统计失去意义**。

Contextual BM25 的做法类似：在构建索引时，给每个 chunk 附加其文档级别的上下文描述，提升词频统计的准确性。

---

## 效果数据

Anthropic 在内部知识库上做了系统性评测：

| 方法 | 检索失败率降低 |
|------|---------------|
| Contextual Embeddings 单独使用 | 49% |
| Contextual Embeddings + BM25 + Reranking | **67%** |

这意味着同样的知识库，Contextual Retrieval 能让 Agent 找到更多正确答案。

---

## 与 Anthropic 其他工具的协同

Contextual Retrieval 与 Anthropic 2025 年底的 Advanced Tool Use 形成了有趣的对比：

- **Advanced Tool Use** 解决的是「工具发现」问题——如何在海量工具中快速找到相关工具
- **Contextual Retrieval** 解决的是「知识检索」问题——如何在海量知识块中精确找到相关内容

两者本质相同：**在超大规模工具库/知识库场景下，如何让 Agent 精准定位目标**。这暗示了一个更大的 Pattern：Agent 系统的核心瓶颈从「推理」转移到「检索」，而解法都是从「全部加载」转向「按需发现」。

---

## 工程实现要点

Anthropic 提供了完整的 [Cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)，关键实现步骤：

1. **预处理阶段**：为每个 chunk 生成「块级描述 + 原始文档摘要」的组合文本
2. **Embedding 阶段**：对组合文本而非裸 chunk 生成向量
3. **检索阶段**：查询时同样附加用户问题的完整上下文
4. **融合阶段**：将 semantic similarity（Embedding）和 lexical matching（BM25）结果用 rank fusion 合并

---

## 对 Agent 工程的启示

Contextual Retrieval 揭示了 RAG 系统设计的一个常见误区：**过度关注 Embedding 模型的精度，而忽视了 chunk 上下文信息的保留**。

对于构建 Agent 知识库系统的工程师而言：

- **小知识库（<200K tokens）**：直接用 Prompt Caching 塞进上下文，延迟降低 2x，成本降低 90%
- **大知识库**：必须采用 Contextual Retrieval，否则检索精度会随规模快速下降
- **混合方案**：Embedding + BM25 双重检索 + Reranking 是当前最优实践

> *相关工具*：[Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)——对小于 200K token 的知识库，直接塞进上下文是最优解
