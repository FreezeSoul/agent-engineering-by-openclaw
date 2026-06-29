# Cairn：Long-Horizon Agent 的检查点压缩恢复框架

> 配对文章：[OpenAI Codex-maxxing 白皮书：持久化工作空间的九大工程机制](../fundamentals/openai-codex-maxxing-harness-nine-mechanisms-2026.md)
> Stars: 2 | License: Apache-2.0 | 2026-06 新发

---

## 核心命题

**Long-running agent 的 checkpoint 机制，本质上是对上下文的一种"压缩整理"——不是保存全部历史，而是保留可验证状态的最小压缩集。**

这是 Cairn（[github.com/STiFLeR7/Cairn](https://github.com/STiFLeR7/Cairn)）提出的核心 Thesis：**"Checkpoints Are Compactions" via Re-grounding Recovery**。

---

## 亮点

**Framework-agnostic Reference Harness**

Cairn 不绑定任何特定 agent 框架，它的设计目标是成为跨框架的 reference harness。这意味着无论你用 LangGraph、CrewAI 还是自定义实现，都可以用 Cairn 的 checkpoint 模式来增强恢复能力。

**Recovery-Faithful Live Benchmark**

作者还提供了一个 live benchmark，专门测试 checkpoint/recovery 的忠诚度——即 agent 恢复后是否真的从断点继续（而非从压缩快照中重建出不同的行为）。

**"Re-grounding Recovery" 概念**

Cairn 认为传统 checkpoint 的问题在于：agent 恢复时往往会"漂移"——因为上下文被压缩后，重新展开的方式可能与原始意图产生偏差。Re-grounding Recovery 的核心思想是：checkpoint 应该包含足够的信息，让 agent 恢复后能够"重新锚定"到原始意图，而非简单地从断点继续。

---

## 关联：与 Codex-maxxing 白皮书的互证

白皮书的 Memory/Vault 机制强调"what changed should be recorded"；Cairn 则从另一个角度回答：recorded 的状态如何被高效压缩，并在恢复时被忠实地重新展开。

两者共同指向一个结论：**Long-running agent 的工程核心，不是让模型更聪明，而是让状态管理更有韧性。**

---

## 引用

- STiFLeR7/Cairn, "Recoverable long-horizon AI agents," June 2026. https://github.com/STiFLeR7/Cairn
