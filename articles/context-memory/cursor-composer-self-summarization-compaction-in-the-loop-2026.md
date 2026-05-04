# Cursor Composer Self-Summarization：Compaction-in-the-Loop 强化学习

## 核心论点

> **本文要证明**：Cursor Composer 的 Self-Summarization 不是简单的上下文压缩，而是将压缩决策本身作为训练信号纳入强化学习循环，使模型学会在压缩过程中保留关键信息——这从根本上区别于传统 prompt-based compaction 的「记忆丢失」问题。

---

## 背景：Compaction 技术的两难困境

### Context Window 的增长速度与 Agent 轨迹的矛盾

在 [CursorBench](https://cursor.com/blog/cursorbench) 中，Cursor 观察到一项明确的规律：**挑战性的真实世界编码任务，性能提升与模型的思考深度、代码库探索量直接正相关**。随着 Agent 承接更困难、更复杂任务，用户对 Agent 的思考和探索量期待持续增加。

然而，Agent 的行为轨迹（trajectories）扩张速度远超模型的上下文长度增长速度。这一矛盾在长时任务中尤为突出。

### 现有 Compaction 方案的痛点

业界现有两种主流 compaction 方案：

**方案一：Prompt-based Summarization**
用额外的 summarization model 对上下文做压缩，将结果填回 context window。但提示词往往需要数千 tokens，包含数十个精心措辞的段落来描述「应在 summary 中保留什么内容」。最终压缩后的 context 仍超过 5,000 tokens，且需要复杂的结构化格式来描述关键信息。

**方案二：Sliding Context Window**
通过滑动窗口直接丢弃旧上下文。这会导致关键信息永久丢失，使 Agent 在长任务推进过程中效能持续下降。

> 两者共享一个根本缺陷：**compaction 过程与模型训练过程解耦**。模型从未被专门教导「如何做 compaction」，因此无论压缩策略多精细，模型都会在 compaction 后遗忘关键信息。

---

## Self-Summarization：训练行为而非 Prompt 技巧

### Compaction-in-the-Loop Reinforcement Learning

Cursor 的解法是将 **compaction 本身作为 Composer 的训练内容**，而非作为额外的工程技巧。

具体流程：

```
1. Composer 从 prompt 开始生成，直至达到固定 token 长度触发器
2. 插入一个合成 query，要求模型对当前 context 做总结
3. 模型获得 scratch space 来思考最佳 summary，然后生成压缩后的 context
4. Composer 用压缩后的 context 继续（包含 summary + plan state + remaining tasks + prior summarization count）
5. 循环回到步骤 1
```

关键在于：**训练时也使用同样的 summarization 流程**。每个训练 rollout 可以包含由多个 summaries 链接在一起的多代生成，而非单个 prompt-response 对。这意味着 self-summaries 本身也成为了被 reward 的内容。

### 训练信号分配

从技术角度看，这不需要对训练架构做重大改动。Cursor 使用最终 reward 来对 chain 中模型产生的所有 tokens 进行 reward 分配——这同时 upweight 了好的 trajectory 中的 agent responses，也 upweight 了使这些 responses 成为可能的 self-summarizations。

反过来说，那些丢失关键信息的糟糕 summaries 会被 downweighted。随着 Composer 训练，它学会了使用 self-summary 过程来构建更长的 context。对于困难案例，Composer 通常会多次 self-summarize。

---

## 效果验证：Token 效率与错误率的双重改进

### 实验设计

Cursor 在两组 context-constrained 测试环境中评估 Composer 的 self-summarization 效果：

- **80k token 触发器**：较少的压缩频率
- **40k token 触发器**：较频繁的压缩

基线对比方案：高度调优的 prompt-based compaction 方法（包含数千 tokens 的 summarization prompt，描述应保留的内容的近十几个精心措辞的章节）。

### 关键数据

| 指标 | Prompt-based Baseline | Composer Self-Summarization | 改进幅度 |
|------|----------------------|---------------------------|---------|
| Summary prompt 长度 | 数千 tokens | "Please summarize the conversation"（~20 tokens） | **减少 99%+** |
| 输出 Summary 长度 | 平均 >5,000 tokens | 平均 ~1,000 tokens | **减少 80%** |
| Compaction 导致的错误率 | 基线 | **降低 50%** | **50% 下降** |
| KV Cache 复用 | 不支持 | 重用 prior tokens 的存储中间计算 | **内存效率提升** |

> 官方数据引用：
> "Self-summary produces significantly better results on CursorBench with much more token-efficient compactions. Self-summary consistently reduces the error from compaction by 50%, even compared to the targeted baseline approach, while using one-fifth of the tokens and reusing the KV cache."
> — [Cursor Blog: Training Composer for longer horizons](https://cursor.com/blog/self-summarization)

---

## 案例：170 Turns 解决 Terminal-Bench make-doom-for-mips

Terminal-Bench 2.0 中有一个极具挑战性的问题：

```
I have provided /app/doomgeneric/, the source code to doom. I've also wrote a special doomgeneric_img.c that I want you to use which will write each drawn frame to /tmp/frame.bmp. I've finally provided vm.js that will expect a file called doomgeneric_mips and will run it. Please figure out the rest…
```

问题描述简洁，但挑战性极高——多个强大模型在官方测试中都未能正确解决。

Cursor 的早期研究版 Composer 成功解决了这个问题。整个过程：

- **170 次 turn** 的工程和测试
- **100,000+ tokens** 的上下文被 self-summarize 为 **1,000 tokens**——保留的是模型判断对解决问题最关键的信息

这正是「compaction-in-the-loop」的核心价值：**模型学会了判断什么值得保留，什么可以丢弃**。

---

## 与 Anthropic Context Engineering 的技术对照

Anthropic 的「Effective context engineering for AI agents」描述了三层上下文管理技术体系：

- **Compaction**：通过压缩保留关键信息
- **Structured Note-taking**：主动将信息转化为结构化笔记
- **Sub-agent Architectures**：将复杂任务分解给子 Agent

Cursor Composer 的 Self-Summarization 本质上是 **Compaction 层的方法论突破**——从 prompt-based 压缩进化到 trained behavior，使模型主动学习「哪些信息值得跨上下文传递」。

> 笔者认为：Cursor 的「compaction-in-the-loop RL」与 Anthropic 的「Just-in-Time Context 策略」形成互补——前者解决压缩决策的质量问题（what to preserve），后者解决压缩时机的优化问题（when to compress）。

---

## 启示与行动

### 对 Agent 开发者的启示

1. **Compaction 不是工程技巧，而是训练问题**：如果你的 Agent harness 仍在使用 prompt-based summarization，你应该考虑这个功能是否值得作为训练目标而非 prompt 设计
2. **Summary 的质量应该被纳入 reward signal**：Cursor 的方法表明，compaction 本身的质量直接影响最终任务表现，因此应当被显式训练
3. **短 prompt 可以实现高质量压缩**：Composer 只需 "Please summarize the conversation"，远低于精心设计的数千 token prompt——这是因为模型已经学会了判断什么重要

### 值得关注的演进方向

Cursor 明确指出，下一步研究方向包括：
- **Multi-agent coordination** 的更长、更复杂过程训练
- **Composer 下一个版本** 即将发布

> 官方引用：
> "Our work on self-summarization is a step toward our broader goal of training Composer over even longer, more complex processes such as multi-agent coordination."
> — [Cursor Blog](https://cursor.com/blog/self-summarization)

---

## 总结

Cursor Composer 的 Self-Summarization 代表了一种范式转变：**将 compaction 从一个工程问题重新定义为训练问题**。通过让模型学会判断什么信息值得跨上下文保留，Self-Summarization 在 token 效率（减少 80%）和任务准确性（compaction 错误率降低 50%）两个维度同时实现了突破。

这为未来 Agent Harness 的设计提供了新思路：与其在 prompt 层面优化压缩策略，不如让模型在训练阶段就学会「压缩的艺术」。

---

**引用来源**：

1. [Cursor Blog: Training Composer for longer horizons](https://cursor.com/blog/self-summarization)
2. [Cursor Blog: CursorBench](https://cursor.com/blog/cursorbench)
3. [Cursor Long-Running Agents Research Preview](https://cursor.com/blog/long-running-agents)