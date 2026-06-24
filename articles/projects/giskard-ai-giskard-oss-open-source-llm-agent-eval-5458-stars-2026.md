# Giskard OSS：模块化的 LLM Agent 评估与红队测试框架（5,458 ⭐）

**来源**：[Giskard-AI/giskard-oss](https://github.com/Giskard-AI/giskard-oss)，GitHub，**5,458 ⭐**，Apache 2.0
**归档目录**：`projects/`
**关联 Article**：[SpecBench — 代码越长，Harness 评测越失效](./specbench-reward-hacking-gap-coding-harness-2026.md)

---

## 核心命题

Coding Agent 的评测问题不只是「选哪个 benchmark」，而是「评测框架本身是否值得信任」。SpecBench 揭示了双测试套件结构对 Reward Hacking 的敏感性，那么生产级 Agent 系统实际落地时，评测框架需要怎样的工程设计？

Giskard OSS 给出了一个值得参考的工程答案：**模块化、异步优先、支持 Agentic 系统的测试与红队平台**。

---

## 为什么值得关注

Giskard 在 LLM 评测领域已经是一个有积累的项目，v3 版本做了从零重建，明确转向 LLM 和 AI Agent 的测试与评估。

**核心亮点**：

> "Evals, Red Teaming and Test Generation for Agentic Systems — Modular, Lightweight, Dynamic and Async-first" — [Giskard OSS README](https://github.com/Giskard-AI/giskard-oss)

这四个形容词直接对应了当前 Agent 评测框架的几个工程难点：

1. **Modular**：Agent 系统评测不像固定 API 评测——工具调用链、Memory 状态、多轮交互都是动态的。模块化意味着你能按需替换评测组件，而不是被框架绑架。
2. **Async-first**：Agent 工作流天然是异步的，评测框架也必须支持这一点。
3. **Agentic Systems**：这是 v3 的核心升级点，专门针对 Agent 特性设计——不只是测模型输出，还要测 Agent 的行为轨迹、工具调用序列、状态变更。

---

## 与 SpecBench 的互补关系

| 维度 | SpecBench | Giskard OSS |
|------|-----------|-------------|
| **定位** | Coding 任务的 Reward Hacking 评测基准 | 通用的 Agent 系统评测与红队平台 |
| **核心问题** | 「Agent 是否在 hack 测试？」 | 「Agent 系统整体是否安全、可靠、符合预期？」 |
| **任务规模** | 系统级编程任务（1.5k-110k 行代码） | 通用 LLM / Agent 任务 |
| **评测维度** | 验证测试 vs 隐藏测试的 pass rate 差 | 多维度：Evals + Red Teaming + Test Generation |

从工程角度，SpecBench 提供了一个**专项诊断工具**——当你怀疑你的 Coding Harness 有 Reward Hacking 问题时，用它来定量测量。而 Giskard OSS 提供了一个**通用评测平台**——覆盖 Agent 系统的安全、可信度、功能正确性等多个维度。

两者不是竞争关系，而是互补关系：SpecBench 是诊断工具，Giskard 是日常评测基础设施。

---

## 快速上手参考

```python
# Giskard 核心评测模式（示例结构）
import giskard as gsk

# 定义 Agent 评测任务
model = gsk.Model("your-agent-model")
dataset = gsk.Dataset("your-test-cases")

# 运行评测
results = gsk.evaluate(model, dataset, 
                        suite="agentic_safety",
                        red_team=True)

# 生成测试报告
gsk.report(results)
```

---

**关联链接**：
- [GitHub](https://github.com/Giskard-AI/giskard-oss)
- [Giskard Documentation](https://docs.giskard.ai/oss)
- [Announcing Giskard OSS v3](https://www.giskard.ai/knowledge/announcing-giskard-open-source-v3)
