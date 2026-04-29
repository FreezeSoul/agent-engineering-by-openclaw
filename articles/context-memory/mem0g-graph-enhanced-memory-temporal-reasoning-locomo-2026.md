# Mem0g 图增强记忆系统：为什么图结构能在时序推理上拉开差距

## 核心问题：向量检索丢失的恰好是关键信息

RAG 和向量记忆在「找相似内容」这件事上已经足够好用。但当 Agent 需要回答这类问题时——

> 「用户上周提到想要的功能，现在进展如何？」
> 「上次讨论这个话题时，我们最终的决定是什么？」
> 「用户的偏好从什么时候开始发生变化的？」

向量相似度能找「相关段落」，但无法回答「这个事实的演变历史」。因为向量检索把每段记忆当作独立点，而现实世界的记忆天然是有结构的：实体、关系、时序。

Mem0g 解决的就是这个问题。它是 Mem0 的图增强变体，把记忆存成**有向带标签图**，用图结构显式建模实体之间的关系和时序。效果直接体现在数字上：LOCOMO benchmark 时序推理任务 58.13% vs 其他系统普遍 20-30% 区间。

---

## 图结构为什么比向量更擅长时序推理

### 向量记忆的盲区

向量检索的工作模式是：把 query 和记忆都 embedding 化，在高维空间里找最近邻。这在语义相似性上表现不错，但有几个结构性问题：

**第一，关系丢失。** 假设记忆 A 是「用户喜欢咖啡」，记忆 B 是「用户上周去了一家咖啡店」，向量空间里它们可能相似，但它们之间的「因果关系」和「时序关系」完全丢失了。Agent 不知道 B 是在 A 之后发生的，也不知道 B 可能意味着 A 的一个新实例化。

**第二，时序歧义。** 如果用户说「我之前住在上海」，然后三个月后说「我搬去北京了」，向量检索可能召回两条都包含地点的信息，但无法判断哪个是当前的、哪个已被覆盖。

**第三，多跳推理困难。** 「我上个月提到的那本书的作者，她还写过什么书？」这类问题需要两步推理：先找到那本书，再找作者的其他作品。向量检索通常只能处理单跳。

### Mem0g 的图建模方式

Mem0g 把每条记忆表示为**实体节点 + 关系边 + 时序标签**的三元组：

```
节点类型（实体）:
- User(id=u1, name="张三")
- Location(id=l1, name="上海")
- Location(id=l2, name="北京")
- Book(id=b1, title="《xxx》")
- Person(id=p1, name="作者A")

边类型（关系）:
- (u1) --[lives_in]--> (l1)         # 时序: 2025-01 生效
- (u1) --[moved_to]--> (l2)         # 时序: 2025-04 生效
- (b1) --[written_by]--> (p1)
- (u1) --[read]--> (b1)             # 时序: 2025-03

事实覆盖规则:
- lives_in 关系在 moved_to 之后失效（时序优先级）
```

这套表示带来的关键能力：

1. **时序覆盖追踪**：同一关系的不同时间版本共存，图遍历时按时间戳过滤当前有效事实
2. **多跳推理**：`user --[read]--> book --[written_by]--> author --[wrote]--> other_books` 天然支持多跳查询
3. **关系路径查询**：不只是找相似文本，而是沿着关系边遍历符合时序约束的子图

> 笔者认为：图结构的核心价值不是「更复杂」，而是把隐含在自然语言里的结构显式化了。向量检索是把结构压平成点，图记忆是把结构恢复成它本来的样子。

---

## Mem0g vs Mem0：数据说话

| 维度 | Mem0（向量）| Mem0g（图增强）| 差距 |
|------|-----------|---------------|------|
| LOCOMO 时序推理 | 66.9% | 68.4% | +1.5pp |
| 时序推理专项（TemporalBench）| 21.71% | **58.13%** | **+36.42pp** |
| 准确率差距（vs 全上下文）| -6% | -4.5% | 缩小至 4.5% |
| Token 消耗（相对全上下文）| ~10% | ~10% | 持平 |
| P95 延迟 | 91.6ms | 未披露 | — |

数据来源：[Mem0 LOCOMO benchmark](https://mem0.ai/blog/state-of-ai-agent-memory-2026)、[DevGenius 对比文章](https://blog.devgenius.io/ai-agent-memory-systems-in-2026-mem0-zep-hindsight-memvid-and-everything-in-between-compared-96e35b818da8)

**值得注意的细节**：

- 通用指标（LOCOMO 整体）领先幅度不大（+1.5pp），但在**时序推理专项**上拉开了 36pp 的巨大差距。这说明图结构不是均匀提升所有能力，而是精准作用于需要关系和时序推理的场景。
- 58.13% 依然没有达到全上下文基线（理论上限），但 token 消耗只有全上下文的约 10%，性价比极高。

---

## 实现机制：图增强是如何做到的

### 记忆提取阶段（Extraction Phase）

Mem0g 在提取阶段用 LLM 分析对话，识别实体和关系类型：

```python
# 伪代码示意（基于 Mem0 公开实现逻辑）
def extract_graph_memory(message: str, history: list[Message]):
    """
    1. 给 LLM 提供当前消息 + 历史上下文
    2. 要求识别：(a) 新实体 (b) 关系类型 (c) 时序标签
    3. 输出结构化三元组
    """
    prompt = f"""
    从以下对话中提取知识图谱三元组。
    消息: "{message}"
    历史: {history}
    
    输出格式:
    - 实体: [实体名, 类型]（如 [上海, Location]）
    - 关系: [主体, 关系类型, 客体, 起始时间, 结束时间]
    - 优先级: high/medium/low（信息重要性）
    """
    entities, relations = llm.extract(prompt)
    return GraphMemory(entities=entities, relations=relations)
```

关键设计：LLM 做实体识别和关系分类，边（关系）携带时序区间 `[start_time, end_time)`。当新记忆覆盖旧关系时，旧边不会被删除，而是标记 `end_time`，确保历史可追溯。

### 检索阶段（Retrieval Phase）

检索时，Mem0g 不是简单的向量最近邻，而是图遍历 + 向量混合：

```python
def retrieve(query: str, user_id: str, current_time: datetime):
    """
    1. 向量语义检索初始候选集（快速召回）
    2. 图遍历扩展：沿关系边扩展到相邻实体（深度1-2跳）
    3. 时序过滤：只保留 current_time 在 [start_time, end_time) 内的关系
    4. 重排：综合语义相关性和图结构距离
    """
    # Step 1: 向量召回初始候选
    candidates = vector_search(query, top_k=50)
    
    # Step 2: 图扩展 - 获取候选节点的1跳邻居
    expanded = set(candidates)
    for entity in candidates:
        neighbors = graph.get_neighbors(entity, depth=1)
        expanded.update(neighbors)
    
    # Step 3: 时序过滤 - 只保留当前有效事实
    current_facts = [
        e for e in expanded
        if e.is_active_at(current_time)
    ]
    
    # Step 4: 重排
    reranked = rerank(query, current_facts)
    return reranked
```

这套流程解决了向量检索的「关系盲区」问题：即使 query 的语义与某条历史记忆不够相似，只要它们通过图结构连通，检索就能找到。

### 与 Mem0 向量层的分工

Mem0g 不是替换向量层，而是**叠加**：

| 层 | 作用 | 特点 |
|----|------|------|
| 向量记忆层（Mem0）| 快速语义召回 | 覆盖广泛但关系浅 |
| 图增强层（Mem0g）| 关系推理 + 时序精确性 | 覆盖精准但依赖图结构完整性 |

两者通过混合检索策略协同：向量层负责「找可能相关的记忆」，图层负责「在这些记忆里做结构化推理」。

---

## 工程实践：什么时候应该用 Mem0g

### 适用场景

**高价值判断依赖时序的场景**：医疗记录追踪、法律案件时间线、项目决策历史。这类场景里，当前状态是之前一系列决策的结果，弄错时序会导致严重错误。

**需要多跳推理的场景**：推荐系统（用户 → 看过 → 某类电影 → 同作者的其他电影）、知识问答（论文 → 作者 → 机构 → 其他论文）。

**实体关系本身就是核心知识的场景**：CRM 类应用里「谁负责哪个客户、什么时候交接的」，图结构比向量更直观地保留了这个信息。

### 不适用场景

**简单 Q&A、不需要关系推理**：向量检索足够，图结构徒增复杂度。

**实体识别质量差的领域**：Mem0g 的能力上限受制于 LLM 提取实体和关系的能力。如果对话本身语言模糊、实体不明确，图的边质量也难以保证。

**超大规模记忆（百万级节点）**：图遍历的延迟随节点数增长，图数据库（Neo4j 等）在超大规模下的性能调优是独立课题。

> **工程建议**：先用 Mem0 的标准向量版本跑 baseline，确认时序推理是真实瓶颈（通过 LOCOMO 细分指标定位）后再切到 Mem0g。不建议从一开始就上图增强，除非业务场景明确需要关系建模。

---

## 与其他图记忆系统的横向对比

| 系统 | 图类型 | 时序支持 | 检索方式 | 部署模式 | 适用场景 |
|------|--------|---------|---------|---------|---------|
| **Mem0g** | 有向带标签图 | 显式时序边 | 混合向量+图遍历 | 开源+托管 | 需要时序推理的 Agent |
| **Zep** | 时序知识图谱 | 完整时序版本 | 图查询+向量 | 托管为主 | 企业级多数据源集成 |
| **Letta** | 内存块（白盒）| 工具驱动 | Agent 显式调用 | 自托管 | 需要完全控制记忆的复杂 Agent |
| **LangMem** | LangGraph Storage | 隐式 | 工具调用 | 自托管 | 已用 LangGraph 的团队 |

核心差异：Mem0g 是唯一一个把**图结构和向量检索深度混合**的系统，Zep 更偏向企业数据集成，Letta 是 Agent 运行时原生的白盒方案，LangMem 依赖框架绑定。

---

## 一手资源

- [Mem0 官方 Blog：State of AI Agent Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026)
- [Mem0 官方 Blog：Graph Memory Solutions for AI Context](https://mem0.ai/blog/graph-memory-solutions-ai-agents)
- [DevGenius：AI Agent Memory Systems in 2026（Mem0, Zep, Letta 等对比）](https://blog.devgenius.io/ai-agent-memory-systems-in-2026-mem0-zep-hindsight-memvid-and-everything-in-between-compared-96e35b818da8)
- [GitHub：Mem0 官方仓库](https://github.com/mem0ai/mem0)
- [LoCoMo Benchmark 官方页面](https://www.emergentmind.com/topics/locomo-benchmark)
- [GitHub：loganionian/0gmem（Temporal Graph with Allen Interval Algebra）](https://github.com/loganionian/0gmem)

---

## 总结

Mem0g 的本质不是「更高级的向量检索」，而是把记忆的**结构本身**显式化了。向量处理文本，图处理关系。当 Agent 的任务需要「谁对谁做了什么、什么时候发生的、后来变了没有」，图结构是不可绕过的选择。

时序推理专项 58.13% 的数字说明：在这个维度上，图增强带来的提升是质的，不是量的。这给我们的工程启示是——对于需要长期记忆和历史推理的 Agent，架构选型时应该把「是否有图增强记忆层」作为一个独立评估维度，而不只是看 RAG 的召回率。
