# Hopping Context Windows：无停顿的上下文连续性方案

> 消除 Context Window 压缩的「Stop-the-World」痛点，用流式计算的思路解决 LLM Agent 的长对话问题。

---

## 核心命题

LLM Agent 在长对话中都会遇到同一个问题：context window 满了之后，必须停下来——压缩历史、摘要、恢复、再继续。这个过程在用户界面上通常表现为「Summarizing conversation...」的 spinner，而背后是一次额外的 LLM inference 调用。

marklubin/hopping-context-windows 提出了一个观察：**这个停顿是不必要的**。

他们从流式计算中借用了「hopping windows」的概念——在上下文接近满载时，不是暂停做压缩，而是直接开一个「背缓冲区」，继续处理新消息，同时保留历史的压缩快照。等到缓冲区满了，直接切换——不需要调用 LLM，不需要等待，不需要停顿。

**零额外推理成本的上下文连续性**。这是这个项目的核心贡献。

---

## 问题：传统 Compaction 的 Stop-the-World 代价

当前主流 Agent 框架（Claude Code、Codex、Cursor）的上下文管理方案：

```
T: Agent 工作在 ~70% context 容量
T': Context 接近上限
      ↓
[STOP-THE-WORLD]
      ↓
LLM summarization call（额外推理成本）
      ↓
Summary 替换历史
      ↓
[RESUME]
      ↓
T'': Agent 继续
```

每次压缩都是一次完整的 LLM 调用，消耗 tokens 和 latency。在高频压缩场景下，这部分开销累积起来非常可观。

---

## 解法：Checkpoint + Back Buffer + Zero-Cost Cutover

Hopping Context Windows 的机制只有两步：

### 第一步：Checkpoint 创建

当 context 使用到 ~70% 时：
1. 对现有对话历史做一次压缩（这里仍然需要一次 LLM 调用，但这是最后一次）
2. 将压缩结果存入 **checkpoint**
3. 创建 **back buffer** = `[checkpoint]`

### 第二步：双缓冲区并行写入

T' 到 T'' 期间：
- Agent 继续正常工作，所有新消息同时写入两个地方：
  - **active context**（送入 LLM 的实时上下文）
  - **back buffer**（独立维护的消息追加日志）

### 第三步：Zero-Cost Cutover

当 active context 再次满载时：
1. 直接把 back buffer 变成新的 active context
2. 丢弃旧的 active context
3. back buffer 重置为空

**没有额外的 LLM 调用**。Back buffer 只是一个消息列表——追加是 O(1) 操作，cutover 是指针交换。

---

## 为什么这个机制聪明

### 1. 从流式计算借用了成熟的机制

Hopping windows（跳跃窗口）是 Apache Flink、Apache Kafka Streams 等流处理框架中的标准原语。它的核心思想是：**窗口不是互斥的，而是可以重叠的**——一个窗口处理数据时，另一个窗口已经在累积下一批数据。

作者把这个概念移植到 LLM context 管理：active context 和 back buffer 是两个重叠的上下文窗口，它们交替成为「主窗口」，从而实现无缝切换。

### 2. 利用了 LLM 推理的特殊性

传统流式计算中，cutover 之所以需要成本，是因为要处理状态的迁移。但 LLM 的特殊性在于：**每次 inference 是独立的**——它只读当前 prompt，不依赖历史状态。当 cutover 发生时，新的 active context 包含了完整的对话历史（checkpoint + back buffer 的新消息），LLM 可以无缝继续。

**LLM 是无状态的，这反而让 cutover 变得零成本。**

### 3. Checkpoint 的本质是摘要，但不损失信息密度

你可能会问：checkpoint 不也是压缩出来的吗？是的，但 checkpoint 的价值在于**它只创建一次**。之后所有的增量都直接累积到 back buffer，不需要再次调用 LLM。

对比传统方案：
- 传统方案：每次 context 满都要压缩 → N 次 LLM 调用
- Hopping Windows：只压缩一次，之后全是 O(1) 追加 → 1 次 LLM 调用

---

## 与其他方案的对比

| 方案 | 额外推理成本 | 是否有停顿 | 实现复杂度 |
|------|------------|------------|-----------|
| 传统 summarization | 每 N 条消息一次 | Yes（LLM 调用期间）| 低 |
| OpenAI /responses/compact | 每 N 条消息一次 | Yes（API 调用期间）| 中 |
| Hopping Context Windows | **仅 1 次**（初始化时）| **No** | 中 |
| damianoneill/context-compaction | 每 N 条消息一次 | Yes（可配置）| 中 |

---

## 局限性

### 1. Checkpoint 仍然需要一次 LLM 调用

你无法绕过第一次压缩。这次压缩的质量直接决定了后续 back buffer 切换后的上下文完整性。如果 checkpoint 做得好，后续 cutover 无缝衔接；如果 checkpoint 质量差，back buffer 再完整也会丢失信息。

### 2. Back buffer 本身仍会满

Hopping Windows 是一个递归结构——当 back buffer 本身也满了的时候怎么办？方案需要多层 back buffer，或者最终还是要触发一次 checkpoint。但这只是设计问题，理论上可以扩展。

### 3. 还不适合 source code 场景

README 明确指出：「对于 source code 场景，exact syntax 很重要，建议使用原始文件加载或保守的压缩比例」。这意味着对于 coding agent 场景，这个方案目前更适合处理自然语言输入（文档、issue、notes），而不是代码。

---

## 适用场景

**强烈推荐**：
- 处理长篇文档、issue 线程、研究笔记的 Agent
- 多轮对话中的自然语言理解和生成任务
- 任何对「Summarizing...」spinner 感到烦躁的场景

**需要谨慎**：
- 高度依赖精确代码语义的 coding agent（建议保留原始文件加载路径）
- 对上下文完整性要求极高的合规场景

---

## 快速上手

```bash
# 安装
pip install contextcrumb

# 作为 Skill 运行（以 Codex 为例）
# 将 hopping-context-windows 作为 skill 注入 Agent
codex skill add marklubin/hopping-context-windows

# Agent 会在 context 接近 70% 时自动启用 hopping buffer
```

---

## 引用

> "Every production LLM agent performs stop-the-world compaction when the context window fills: pause, summarize, resume. We observe this is unnecessary."

— Mark Lubin, Synix, "Hopping Context Windows", February 2026

Project: https://github.com/marklubin/hopping-context-windows

Related:
- OpenAI Codex Agent Loop Analysis → `openai-codex-agent-loop-context-window-compaction-2026.md`（同一主题下的 Codex 官方实现解析）