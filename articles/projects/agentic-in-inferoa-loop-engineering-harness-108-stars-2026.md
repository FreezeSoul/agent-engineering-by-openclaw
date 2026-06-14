# agentic-in/inferoa — Inference-native Tokenmaxxing Agent Harness

**108 ⭐** | Apache 2.0 | TypeScript | Created 2026-06-08

> Inferoa 是一个"推理原生"的 Agent Harness，专为 **Loop Engineering** 而设计：让模型在长程递归循环中持续自纠正，直到工作被验证完成。

---

## 核心命题

Prompt Engineering 的时代正在让位给 **Loop Engineering**。

当 Agent 需要在多轮迭代中完成复杂任务时，传统的单轮 Prompt 范式失效了。真正的挑战变成：
- 如何让循环持续运行，直到工作被**证明完成**，而非停在下一个答案处
- 如何在每轮迭代中维护**推理效率**（cache 前缀、context 窗口、token 压力）
- 如何让 Agent 在循环中有**可验证的反馈面**（plans、tests、completion evidence）

Inferoa 的核心主张是：Loop Engineering 本质上也是 **Inference Engineering**——循环中的每一轮都是一次推理 workload，prefix drift、cache reuse 崩溃、stale evidence 这些问题必须从推理层解决，而非只在 Prompt 层打补丁。

---

## 技术架构

Inferoa 构建在 **vLLM 生态**之上，将 tokenmaxxing 扩展到整个推理栈：

| 层次 | 组件 | Inferoa 角色 |
|------|------|------------|
| **Loop Engineering** | Loop Mode | 递归长程循环：检查→编辑→测试→验证→决策→恢复→completion evidence |
| **Agent Harness** | Inferoa Core | Session、tools、plans、loops、resources、evidence、prefix-cache discipline |
| **Context Optimization** | CodeGraph / RTK | 选择证据 + 压缩 muttable context，不丢失任务连续性 |
| **Intelligent Routing** | vLLM Semantic Router | 按 cost/safety/privacy/capability 选择模型路径 |
| **Model Serving** | vLLM Engine / Omni | 高吞吐 + 内存高效 + 多模态端点 |

### Loop Mode 的工程机制

`/loop` 命令是 Inferoa 的核心——一个**持久递归循环**：

```bash
/loop "修复这个 bug"
# → 检查代码 → 编辑 → 运行测试 → 验证结果
# → 如果失败：记录 completion evidence → 恢复 → 继续
# → 直到 work is proven
```

关键设计：
- **Completion Evidence**：循环不依赖"下一个答案"，而是依赖"被验证的工作证据"
- **Prefix-cache Discipline**：prompt epochs + deterministic tool schemas + bounded system sections 保护可复用前缀
- **Bounded History**：压缩、摘要、图状 repo context，防止 stale state 占据 context window
- **Serving Visibility**：模型路径对 cost、safety、privacy、capability、session pressure 保持可见

---

## 与 R337 Checkpoint/Resume Article 的闭环

Inferoa 的 Loop Mode 直接实现了 R337 Article 中定义的 **Checkpoint/Resume 协议**：

- **Completion Evidence** ↔ Checkpoint：每个循环迭代都记录可验证的证据
- **Recovery** ↔ Resume：失败时基于 evidence 恢复，而非从头开始
- **Bounded History + Prefix-cache** ↔ Context Efficiency：双层优化防止循环中的 context 膨胀
- **Serving Visibility** ↔ 模型选择：在循环中动态选择最合适的推理路径

这不是 Prompt 控制，而是**工程化的一致性保障**。

---

## 适用场景

- **复杂长程任务**：需要多轮迭代才能验证完成的工作（代码修复、重构、系统调试）
- **Token 效率敏感**：大规模循环中需要控制 token 消耗
- **自托管推理**：基于 vLLM 的私有化部署场景
- **Loop Engineering 实践**：将 Agent 的工作模式从"单轮问答"升级为"持续验证循环"

---

## 安装与使用

```bash
npm install -g inferoa@dev
```

```bash
/loop "Objective here"     # 启动递归循环
/plan "Task"               # 计划模式
/research "Query"          # 研究模式
```

---

## 竞品对比

| 项目 | 定位 | 差异 |
|------|------|------|
| **Inferoa** | Loop Engineering + Inference-native | 循环验证 + vLLM 原生 + Tokenmaxxing |
| **LangGraph** | DAG 编排 | 定义工作流拓扑，不解决循环效率 |
| **CrewAI** | Role-based 多 Agent | 多角色协作，不关注 token 效率 |
| **comet (rpamis)** | Phase-guarded Pipeline | Shell 脚本 Guard，不涉及推理层优化 |

---

## 笔者观点

Inferoa 的最大贡献不是某个单点功能，而是它提出的 **Loop Engineering = Inference Engineering** 这个等式。

业界多数 Agent 框架把"循环"理解为"反复调用 LLM"，而 Inferoa 指出：在循环中，**prefix cache 的有效性每轮都在下降，context window 的压力每轮都在上升**。这不是 Prompt 问题，而是推理引擎的问题。

这个视角让 Inferoa 在 Token 优化和循环稳定性之间找到了一个其他框架没有的平衡点——用 vLLM 的 prefix caching 机制来保护循环，用 bounded context 来控制膨胀，用 completion evidence 来替代"下一个答案"作为停止条件。

对于需要在长程循环中保持效率的 Agent 场景，Inferoa 是目前最接近"推理层原生"的解决方案。