# FastContext：当主 Agent 把探索任务外包给专用子 Agent

> 论文: [arXiv:2606.14066](https://arxiv.org/abs/2606.14066) | 模型: [HuggingFace](https://huggingface.co/collections/microsoft/swe-fastcontext) | Microsoft Research

## 核心命题

现代 Coding Agent 在处理代码库任务时面临一个结构性问题：**同一个模型既要做探索（读文件、搜代码），又要做推理和修改**。探索会消耗宝贵的上下文窗口，还会把无关代码片段留在历史记录里污染后续推理。

FastContext 的解法很直接：**把探索任务委托给一个专用子 Agent，主 Agent 只负责最终决策**。Exploration 和 Solving 分离后，两个阶段各自优化。

笔者认为，这个思路的真正价值不在于"快"，而在于它揭示了**Coding Agent 的任务本质上可以正交分解**——探索策略和解决策略可以分别训练、分别调用，而不是绑在一起用同一个模型。

---

## 问题：主模型的上下文污染

Coding Agent 在处理真实代码库时，通常会这样工作：

1. 主 Agent 读大量文件，理解代码结构
2. 主 Agent 搜索相关代码片段
3. 主 Agent 基于读到的内容做决策和修改

问题在于：**步骤 1 和 2 消耗的 tokens 会永久留在上下文历史中**，后续推理时模型需要处理这些"噪声"，而且探索结果和推理过程混在一起，无法单独复用。

FastContext 给出了一个具体的数字：

> "Modern coding agents often use the same model to explore a repository and solve the task. This makes exploration expensive: exploratory reads and searches consume tokens, stay in the solver's history, and can pollute later reasoning with irrelevant snippets."

笔者的理解是：这不是一个性能优化问题，而是一个**能力边界问题**——当探索消耗了 60% 的上下文时，剩下 40% 的空间根本不够装下一个真实代码库的相关上下文。

## 架构：委托-返回模式

```
┌─────────────┐    自然语言查询     ┌──────────────────┐
│  Main Agent │ ──────────────────► │  FastContext     │
│  (Solver)   │                     │  (Explorer)      │
└─────────────┘ ◄────────────────── └──────────────────┘
                    紧凑的 citation        并行读文件/搜索
                    + 证据摘要            独立工具调用
```

**Main Agent** 发送：`"这个模块的依赖注入是怎么实现的？"`

**FastContext** 返回：
```json
{
  "query": "依赖注入实现",
  "citations": [
    {"file": "src/di/container.ts", "lines": "45-67", "reason": "IoC容器实现"},
    {"file": "src/di/providers.ts", "lines": "12-30", "reason": "Provider注册逻辑"}
  ],
  "summary": "使用类工厂模式的IoC容器，通过providers.ts注册依赖映射。"
}
```

Main Agent 拿到这个结果后，直接基于 `citations` 做决策，不再需要自己去读那些文件。

**FastContext 的关键设计**：它返回的不是完整的文件内容，而是**带行号标注的引用片段 + 简短原因说明**。这让 Main Agent 拿到的是"证据"，而不是"原材料"。

## 工程实现细节

FastContext 的实现有几个值得注意的工程决策：

### 1. 并行探索

FastContext 会**并行调用 read 和 search 工具**，而不是串行探索：

```python
# 伪代码
async def explore(query: str, repo_path: str):
    # 同时发起多个探索请求
    tasks = [
        search_relevant_files(query, max_depth=3),
        find_import_dependencies(query),
        locate_test_files(query),
    ]
    results = await asyncio.gather(*tasks)
    # 合并、去重、生成 citation
    return compact_citations(results)
```

这与人类开发者的工作方式一致——先并行扫一遍文件结构，找到可疑区域后再深入，而不是逐文件阅读。

### 2. 专门的探索模型

FastContext 不是用主模型的另一个实例，而是训练了一个**专门的轻量探索模型**（FastContext-3B/7B）。

这个模型的特点：
- 专门针对代码库探索任务优化
- 使用 read_only 工具，不允许修改代码
- 输出格式固定为 citation 结构

笔者认为这是正确的方向——**探索和推理需要的能力不同，用同一个模型是在两者之间妥协**。

### 3. Citation 格式

```json
{
  "file": "relative/path/to/file.ts",
  "lines": "45-67",
  "reason": "一句话说明这段代码为什么和查询相关"
}
```

`reason` 字段是关键创新——它不只是告诉 Main Agent "这段代码在这个位置"，还解释了**为什么相关**。这让 Main Agent 可以在不读原文的情况下判断引用是否有用。

## 与现有范式的对比

| 维度 | 全部自己读（Baseline）| RAG | FastContext |
|------|---------------------|-----|-------------|
| 上下文占用 | 高（原始文件内容）| 中（检索片段）| 低（citation + reason）|
| 工具调用 | 主 Agent 自行 | 主 Agent 自行 | FastContext 专用 |
| 模型要求 | 单一模型 | 单一模型 | 专用探索模型 |
| 探索质量 | 依赖主 Agent 能力 | 依赖检索质量 | 专门优化 |
| 可解释性 | 低（隐式推理）| 中 | 高（显式 citation）|

笔者认为，RAG 和 FastContext 的本质区别在于：**RAG 是检索驱动的，FastContext 是 Agent 驱动的**。RAG 假设正确的文档就在那里等着被找到；FastContext 则让一个专门的 Agent 去"勘察"代码库，主动寻找证据。

## 适用边界

FastContext 不是万能药。它的适用场景：

✅ **适合的场景**：
- 大型代码库（> 1000 文件）的导航任务
- 需要跨多个模块理解依赖关系的任务
- Main Agent 上下文窗口紧张，无法一次读太多文件

❌ **不适合的场景**：
- 小型代码库（探索成本可能超过节省的上下文）
- 需要精确代码改动的任务（citation 不能替代原文）
- 主 Agent 本身已经很小（如 7B 模型），不需要进一步分解

## 与 Agent Engineering 的关联

FastContext 属于 **AI Coding Agent 的性能优化**方向——它不是在改变 Agent 的能力边界，而是在**提高上下文利用率**。

这个方向在 2026 年变得越来越重要，因为：

1. **上下文窗口虽然越来越大，但代码库也在变大**，两者之间的压力没有消除
2. **长任务中的上下文污染**是真实问题，FastContext 用结构化分离给出了一个干净的解法
3. **Sub-Agent 架构**正在成为复杂 Agent 系统的标配，FastContext 是这个趋势的一个具体实现

笔者认为，**FastContext 的 Sub-Agent 分离范式会扩散到更多场景**——不只是代码探索，还有测试生成、代码审查、文档更新等需要"先调查再行动"的任务。

---

## 笔者的判断

FastContext 最大的贡献不是技术突破，而是一个**设计原则**：**Coding Agent 的任务可以正交分解，不同子任务应该用专门优化的 Agent 处理**。

这个原则的延伸是：未来的 Coding Agent 系统，可能不是"一个 Agent 做所有事"，而是"一个 Main Agent + N 个专用 Sub-Agent"的协作网络。FastContext 是这个方向的一个早期验证。

唯一需要注意的是：FastContext 目前是 Microsoft Research 的研究项目，不是生产级框架。如果你想在生产环境中使用类似思路，可以基于这个原理自己实现一个轻量版本，不需要用他们的模型。

---

**原文引用**：

> "Modern coding agents often use the same model to explore a repository and solve the task. This makes exploration expensive: exploratory reads and searches consume tokens, stay in the solver's history, and can pollute later reasoning with irrelevant snippets." — [FastContext README](https://github.com/microsoft/fastcontext)

> "FastContext is a lightweight repository-exploration subagent for coding agents. Instead of letting the main coding agent spend its own context window on broad file reads and code searches, the main agent delegates a natural-language context query to FastContext." — [FastContext README](https://github.com/microsoft/fastcontext)
