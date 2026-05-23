# MemPalace：让 AI 记住一切，但不废话

**核心命题**：MemPalace 解决了一个长期以来被忽视的问题——AI 记忆系统到底是该「压缩摘要」，还是「逐字存储」。它选择了后者，结果在 LongMemEval 上跑出了 96.6% 的原始检索召回率，且全程不需要任何 API key。

---

## 一个反直觉的选择

当下主流的 AI 记忆方案，几乎都在做同一件事：**摘要压缩**。把对话 history 丢进 LLM，生成一段摘要，再塞进 context window。听起来合理，但这个方案有个根本性缺陷——**摘要即丢失**。当你需要精确回忆「为什么三个月前我们决定把认证流程从 JWT 换成 OAuth2」时，一段「讨论了认证方案的改进」根本无法还原那段决策链。

MemPalace 做了个反直觉的选择：**逐字存储，不压缩**。

> "It does not summarize, extract, or paraphrase. The index is structured — people and projects become *wings*, topics become *rooms*, and original content lives in *drawers*."

这背后有个隐含的工程判断：对于长期记忆检索任务，LLM 本身并不是最可靠的。语义相似度匹配 + 结构化索引，在很多场景下比「先摘要再检索」更稳定。96.6% 的 R@5 就是这个判断的实验验证。

---

## Palace 隐喻：给记忆建一个房子

MemPalace 引入了一套空间隐喻来组织记忆：

| 概念 | 作用 |
|------|------|
| **Wings（翼）** | 按人员/项目划分记忆空间 |
| **Rooms（房间）** | 按话题/主题进一步细分 |
| **Drawers（抽屉）** | 存放原始内容，不做任何变形 |

这套结构的价值在于**检索可 scoping**。你可以只搜索「某个 wing 内的某个 room」，而不是对整个记忆库做 flat semantic search。这对于大型项目或长期协作的场景意义重大——不是所有记忆都是全局相关的。

检索层可插拔，默认是 ChromaDB，但接口定义在 `mempalace/backends/base.py`，随时可以换成 Qdrant、FAISS 或其他向量数据库。

---

## 基准数字：不是吹的，能复现

MemPalace 的论文[明确声明](https://github.com/MemPalace/mempalace/blob/main/benchmarks/BENCHMARKS.md)所有基准可复现：

| 模式 | R@5 | LLM 需求 |
|------|-----|---------|
| Raw（纯语义搜索，无启发式规则）| **96.6%** | 无 |
| Hybrid v4（held-out 450q 调优）| **98.4%** | 无 |
| Hybrid v4 + LLM rerank | ≥99% | 任意 capable model |

最惊人的是 **96.6% 的 raw 数字不需要任何 API key、不需要任何云服务、不需要任何 LLM 调用**。整个 pipeline 在本地就能跑完。这意味着它不只是一个演示，而是一个真正可以部署在本地环境的生产级组件。

---

## 上手成本：低到离谱

```bash
# 一行安装
uv tool install mempalace

# 初始化项目
mempalace init ~/projects/myapp

# 挖掘内容进 palace
mempalace mine ~/projects/myapp                    # 项目文件
mempalace mine ~/.claude/projects/ --mode convos   # Claude Code 会话记录

# 搜索
mempalace search "为什么我们切换到了 GraphQL"

# 为新会话加载记忆
mempalace wake-up
```

支持 Claude Code、Gemini CLI、MCP 兼容工具和本地模型，主流使用场景开箱即用。

---

## 与其他方案的对比

| 维度 | MemPalace | 摘要压缩方案（如 Recall、Memory）| 云端记忆服务 |
|------|-----------|-------------------------------|------------|
| **存储方式** | 逐字原文 | LLM 摘要 | 原文/压缩 |
| **隐私** | 本地优先（nothing leaves your machine）| 取决于实现 | 数据需上传 |
| **API 依赖** | 检索时可选 LLM rerank | 需要 LLM 持续参与 | 需要云端 API |
| **召回精度** | 96.6% R@5 raw | 受限于摘要质量 | 取决于实现 |
| **可解释性** | 检索结果即原文，可追溯 | 摘要可能遗漏关键细节 | 混合 |

笔者认为，当前的 AI 记忆赛道存在一个集体思维误区——认为「记忆 = 摘要」。MemPalace 用实验数据证明，在检索任务上，**精确的原文检索 > 模糊的摘要匹配**。

---

## 适用场景

**适合用 MemPalace**：
- 长期项目开发，需要精确回忆历史决策上下文
- 对话式 AI 需要保留完整对话历史而非摘要
- 数据隐私要求高，不能上传云端的本地部署场景
- 需要对记忆库进行细粒度按项目/人员分组的场景

**不适合**：
- 需要 LLM 对记忆做推理/推断的场景（这是另一个问题域）
- 超大规模记忆库（>10M 级别，目前架构可能需要额外优化）

---

## 相关连接

- GitHub：https://github.com/MemPalace/mempalace
- 官网：https://mempalaceofficial.com
- PyPI：`pip install mempalace`

---

**所以**：如果你的 AI Agent 记忆方案还在用「摘要压缩」那套，这个项目值得你花 10 分钟体验一下什么叫「记忆检索的正确打开方式」。96.6% 的数字背后，是一套被验证过的工程哲学——**让检索系统做检索的事，让 LLM 做 LLM 的事**。