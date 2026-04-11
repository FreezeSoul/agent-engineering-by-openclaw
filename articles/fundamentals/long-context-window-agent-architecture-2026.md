# 长上下文窗口与 Agent 架构：上下文作为基础设施

> **本质**：2026 年主流 LLM 的上下文窗口已突破 1M token（Wentworth 2026）。长上下文不只是"能处理更长的文本"，它正在根本性地改变 Agent 的设计假设——RAG 的必要性在下降，多工具调用历史可以全部放进上下文，Agent 的记忆架构正在被重新定义。
>
> **来源**：[CodingCape - Largest Context Windows 2026](https://codingscape.com/blog/llms-with-largest-context-windows) + [TUM Seminar - Fundamentals of Building Autonomous LLM Agents](https://arxiv.org/html/2510.09244v1)

---

## 一、上下文窗口的演进现状（2026 Q1）

### 1.1 主要模型上下文能力

| 模型 | 上下文窗口 | 输出窗口 | 备注 |
|------|-----------|---------|------|
| **Claude Opus 4.6** | 1M token | - | 标准定价，无额外 surcharge |
| **GPT-5.4 mini/nano** | 400K token | 128K | 低成本长上下文 |
| **Gemini 2.0 Ultra** | 1M token | 32K | |
| **DeepSeek V3** | 128K | - | 开源 |
| **Llama 4** | 128K | - | 开源 |

**关键变化**：1M token 上下文的定价已标准化（Claude Opus 4.6: $5/$25 per M tokens），不再是溢价功能。

### 1.2 长上下文解锁的 Agent 场景

```
1M token ≈ 750,000 中文词 ≈ 3,000 页文档

Agentic 工作负载的实际容量：
  - 全量工具调用历史（1000+ 次调用）
  - 整个代码仓库（中型 repo ~50K-200K tokens）
  - 完整对话上下文（多轮对话 + 反馈）
  - 完整知识库（RAG 替代方案）
```

---

## 二、长上下文对 Agent 记忆架构的影响

### 2.1 传统 Agent 记忆架构（基于 RAG）

```
感知输入
    ↓
外部知识库（RAG: retrieval from vector DB）
    ↓
LLM 推理（仅能看到 retrieved chunks）
    ↓
工具调用 / 执行
    ↓
结果存入记忆（vector store）
```

**RAG 的核心价值**：解决上下文不足时的信息检索问题。

### 2.2 长上下文下的新架构（Direct Context Loading）

```
感知输入
    ↓
直接加载完整上下文（全量文档 / 工具历史 / 知识库）
    ↓
LLM 推理（直接看到所有内容）
    ↓
工具调用 / 执行
```

**这一转变的架构意义**：

| 对比维度 | RAG 架构 | 长上下文架构 |
|---------|---------|------------|
| **信息完整性** | 依赖 retrieval 质量，可能遗漏 | 完整保留，无 retrieval loss |
| **延迟** | retrieval + inference 两步 | 直接 inference |
| **成本** | retrieval cheap + inference | 全量 inference（贵）|
| **可解释性** | 需要解释为什么 retrieval 选这些 | 天然透明，所有内容可见 |
| **扩展性** | vector DB 可无限扩展 | 受限于 context window |
| **幻觉风险** | lower（RAG 限制范围）| higher（全量上下文干扰）|

### 2.3 混合架构：Long Context + Selective Attention

真正的架构演进方向：**利用稀疏注意力机制，在全量上下文中只激活相关部分**。

```
输入：1M token 上下文
    ↓
稀疏注意力（Sliding Window + Global Attention）
    ↓
相关 tokens 形成密集 attention graph
    ↓
推理在压缩后的有效上下文中进行
```

**HST (Hierarchical Sparse Transformer)** 等技术的核心价值：
不是简单截断，而是**学习哪些 token 值得保持全量 attention，哪些可以稀疏化**。

---

## 三、长上下文下的工具调用架构变化

### 3.1 工具调用历史的上下文化

在短上下文时代，工具调用历史需要精心设计以节省 token：

```python
# 短上下文时代的压缩技巧
tool_history = [
    {"role": "tool", "name": "search", "result": "..."[:200]},  # 截断
    {"role": "tool", "name": "execute", "result": "..."[:200]},  # 截断
]
```

在 1M token 上下文下：

```python
# 长上下文时代的完整保留
tool_history = [
    {"role": "tool", "name": "search", "result": "完整结果"},  # 全量
    {"role": "tool", "name": "execute", "result": "完整结果"},  # 全量
    # 1000+ 次调用全部保留
]
```

**架构影响**：Agent 可以看到完整的工具执行历史，而不是被压缩过的摘要。这对调试、溯源、多步推理的准确性有显著提升。

### 3.2 多工具并行协调的上下文支持

多 Agent 系统的一个核心问题是**协调上下文的一致性**：

```
传统架构：
  Agent A 的工具调用 → 结果 → Agent B 的上下文
  （需要通过消息队列同步，状态可能不一致）

长上下文架构：
  所有 Agent 的工具调用历史 → 同一上下文窗口
  每个 Agent 看到相同的完整历史
  状态一致性由上下文保证
```

---

## 四、长上下文的工程挑战

### 4.1 计算复杂度

```
标准 Self-Attention: O(n²) 复杂度
1M token 上下文：1M² = 1T 级别

实际工程中面临的挑战：
  - 显存占用（KV cache 爆炸）
  - 首 token 延迟（prefill 阶段）
  - 注意力稀疏化的精度损失
```

### 4.2 位置编码的外推问题

大多数 Transformer 的位置编码（RoPE / ALiBi）在训练时见过固定长度的上下文，超出训练长度后外推质量急剧下降。

**解决方案**：
- **RoPE 外推**：通过焦距机制（span）处理超出训练长度
- **上下文窗口扩展**：YaRN / LongRoPE 等技术
- **模型原生支持**：新模型从训练阶段就支持超长上下文

### 4.3 成本管理

| 上下文长度 | GPT-5.4 nano 成本 | Claude Haiku 成本 |
|-----------|-----------------|-----------------|
| 4K | $0.0004 | $0.00025 |
| 128K | $0.0128 | $0.008 |
| 1M | $0.10 | $0.0625 |

**架构建议**：不同 Agent 阶段使用不同的上下文预算——简单任务不需要全量上下文加载。

---

## 五、对 Agent 架构设计的实际建议

### 5.1 判断标准：什么时候用 RAG，什么时候用长上下文

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 知识库规模大（>1M tokens）且更新频繁 | RAG | 无法全部加载 |
| 需要精确检索（事实查找）| RAG | retrieval 比生成更可靠 |
| 工具调用历史 / 完整对话 | 长上下文 | 完整历史比检索更重要 |
| 代码仓库（中型 < 200K tokens）| 长上下文 | 直接加载比 RAG 更准确 |
| 多 Agent 共享状态 | 长上下文 | 统一上下文保证一致性 |
| 成本敏感场景 | RAG | 长上下文 inference 更贵 |

### 5.2 实际架构模式

```
┌─────────────────────────────────────────────┐
│  Agent Controller                          │
│  - 分析输入复杂度                          │
│  - 决定上下文策略（RAG / Long Context）     │
│  - 决定加载哪些历史                        │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│  Context Manager                           │
│  - 策略路由（128K / 1M / selective）       │
│  - 成本控制（per-stage 预算）              │
│  - 注意力掩码（只激活相关区域）             │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│  LLM Inference                             │
│  - 长上下文推理                            │
│  - 输出 + 元数据（token 消耗等）            │
└─────────────────────────────────────────────┘
```

---

## 六、关键结论

1. **长上下文不是 RAG 的替代，而是互补**：两者解决不同问题——RAG 解决信息检索，长上下文解决上下文完整性。

2. **Agent 记忆架构正在被重新分层**：
   - 极短期：LLM 的 KV cache
   - 短期：完整上下文加载
   - 中期：结构化记忆（vector store）
   - 长期：外部知识库（RAG）

3. **架构设计需要重新考虑 context budget 分配**：不再是"尽可能多加载"，而是"什么该放上下文，什么该放记忆系统"。

---

> **一手来源**：[CodingCape - LLMs with Largest Context Windows](https://codingscape.com/blog/llms-with-largest-context-windows) | [TUM - Fundamentals of Building Autonomous LLM Agents (arXiv:2510.09244)](https://arxiv.org/html/2510.09244v1)
