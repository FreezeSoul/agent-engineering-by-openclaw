# ScrapeGraphAI/toonify：把结构化数据压缩 64%，让 LLM 少读多想

## 核心命题

**TOON 解决的是一个很具体的问题：Agent 传给 LLM 的结构化数据太臃肿了——一个 200 行的 JSON，传给 LLM 后 token 消耗能抵一篇短文。TOON 的思路是把 JSON 压缩成 CSV 一样紧凑但保留结构的格式，实测平均减少 64% 的 token 占用。** 在 Context 成为 Agent 系统核心约束的今天，这比任何模型升级都划算。

---

## 为什么 Agent 需要这样一种数据格式

当一个 Agent 处理结构化数据时，它面临一个矛盾：

- **需要结构**：Agent 需要知道字段名、嵌套关系、数据类型，才能正确理解数据
- **结构有成本**：JSON 的 key 要重复出现在每一行，类型标注要占用 token，而 LLM 其实不需要"可读性"，它只需要"可解析性"

TOON 的核心洞察是：LLM 需要的不是 JSON 的可读性，而是**字段名的信息量 + 数据值的压缩表示**。

```python
# 同样的数据，两种格式的 token 差异
# JSON: 120 tokens (key重复 + 括号 + 引号)
# TOON: 43 tokens (key只出现一次，用位置对应)
```

这就是 TOON 的核心价值：**把 JSON 的 token 开销压缩到接近 CSV，同时保留字段名和类型信息**。

---

## 核心技术设计

### Key Folding（键折叠）

对于嵌套对象，TOON 使用键折叠机制避免重复：

```python
# TOON 的处理方式
# products[2]{sku,name,price}:
# LAP-001,Gaming Laptop,1299.99
# MOU-042,Wireless Mouse,29.99
```

字段名只出现一次（作为 header），数据行只需要填值。这对于**大量均匀数据**（如订单列表、用户行为记录、产品目录）的压缩效果最为显著。

### 响应结构模板生成

TOON 还提供了 `generate_structure` 功能，生成 LLM 响应格式模板：

```python
schema = {
    "name": "name of the person",
    "age": "age of the person"
}
structure = generate_structure(schema)
# 输出：
# name: <name of the person>
# age: <age of the person>
```

这是一个聪明的设计：**告诉 LLM 你想要什么格式的响应，而不是给它例子让它模仿**。这比 few-shot examples 节省大量 token，同时保持格式一致性。

### Pydantic 集成

```python
from pydantic import BaseModel
from toon import encode_pydantic

class Product(BaseModel):
    sku: str
    name: str
    price: float

products = [Product(sku="LAP-001", name="Laptop", price=1299.99)]
toon = encode_pydantic(products)
# [1]{sku,name,price}:
# LAP-001,Laptop,1299.99
```

直接支持 Pydantic 模型意味着它可以和现有的数据验证体系无缝集成。

---

## 与 Cursor Context Usage Report 的关联

**这两个项目解决的是同一个问题的两个方向。**

Cursor Canvas Context Usage Report 解决的是"如何让 Agent 的 Context 消耗变得可观测、可追问、可优化"——这是一套 runtime context 管理框架，关注的是**如何减少不必要的 context 注入**。

TOON 解决的是"结构化数据在传输层如何最小化 token 占用"——这是一套 data serialization 层的优化，关注的是**如何让必要的数据传输更紧凑**。

两者组合在一起，构成了一个完整的 Agent token 优化思路：

```
Cursor Context Usage Report（可观测层）
    ↓ 发现 context 超限
    ↓
TOON 压缩数据传输（数据层）
    ↓ 减少 token 占用
    ↓
Agent 用省下的 token 做更多实际工作（能力层）
```

这种组合在生产环境中很有价值：当一个 Agent 需要处理大量结构化数据（数据库查询结果、API 响应、日志分析）时，TOON 可以直接减少 50%+ 的 token 消耗，效果比换模型更直接。

---

## 笔者的判断

TOON 的价值不在于"这是一个创新的算法"，而在于它精准地解决了一个被忽视的工程问题：**Agent 系统在数据传输层的 token 浪费**。

大多数 Agent 开发者下意识会用 JSON 传数据，因为这是"标准格式"。但对于 LLM 来说，JSON 是一种**为人设计的格式**，不是为 token 效率设计的格式。TOON 把这个错位纠正过来。

笔者认为它最适合两类场景：

1. **RAG Pipeline 中的文档 chunk 传输**：大量结构化数据需要注入 context，TOON 可以显著减少 token 占用
2. **需要处理大规模结构化输出的 Agent**：如报表生成、数据提取、多记录分析

TOON 不是银弹——对于非结构化文本、复杂嵌套结构，JSON 仍然是更好的选择。但对于表格类、列表类、记录类的数据，它的效果是非常明确的。

---

**引用来源**：

- GitHub README: https://github.com/ScrapeGraphAI/toonify
- TOON Format 示例: https://github.com/ScrapeGraphAI/toonify/blob/main/README.md
- LogRocket 技术博客: https://blog.logrocket.com/reduce-tokens-with-toon