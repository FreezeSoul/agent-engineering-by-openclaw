# Sakana Fugu：把多 Agent 编排压成单一模型 API 的工程范式

> **核心论断**：当多 Agent 系统开始被"压缩"成单一模型暴露时，编排范式从「显式 workflow / role-based routing」转向「隐式 learned orchestration」。Sakana Fugu（2026-06-22）= TRINITY (ICLR 2026) + Conductor (ICLR 2026) 的工业化产物：把"何时调用哪个专家模型、如何合成答案"内化为一个语言模型本身。理解 Fugu 既是 ICLR 2026 两篇 learned orchestration 论文的工程化封装，也是 2026 H2 模型层 vs 编排层博弈的关键拐点。
>
> **读完能得到什么**：① 区分"role-based routing"（已有 [multi-model-routing-coding-agents-role-based-2026](../fundamentals/multi-model-routing-coding-agents-role-based-2026.md)）与"policy-over-models"（Fugu 的新范式）；② 理解 TRINITY 与 Conductor 的工程角色分工（hidden-state 路由 vs workflow-DAG 编排）；③ 评估 Fugu 与"前沿模型直连"在合规性、供应稳定性、可演化性三个维度的差异。
>
> **来源**：[Sakana AI Fugu Release Blog (2026-06-22)](https://sakana.ai/fugu-release/) + [Sakana Fugu Technical Report (2026)](https://sakana.ai/fugu-release/) + [TRINITY: An Evolved LLM Coordinator (ICLR 2026)](https://arxiv.org/abs/2512.04695) + [Learning to Orchestrate Agents in Natural Language with the Conductor (ICLR 2026)](https://arxiv.org/abs/2512.04388)

---

## 一、问题：显式多 Agent 系统的 3 个工业级失败

### 1.1 显式编排的认知与工程成本

2025–2026 的多 Agent 系统普遍采用**显式 workflow**——开发者用 LangGraph / CrewAI / AutoGen 这类框架手写状态机、handoff 规则、工具调用协议。一篇近期分析（[multi-model-routing-coding-agents-role-based-2026](../fundamentals/multi-model-routing-coding-agents-role-based-2026.md)）已经系统论述了"role-based routing"的两类同步失败：

| 失败模式 | 触发条件 | 后果 |
|---------|---------|-----|
| Over-Provisioning | 给所有角色分配旗舰模型 | 计算成本失控（Opus 4.6 用在文件导航上 = 5× 浪费） |
| Under-Provisioning | 给规划/协调角色分配小模型 | 错误级联（下游 Agent 基于错误规范工作） |

但 role-based routing 只解决了"哪个角色用哪个模型"。**真正工业级的多 Agent 系统还要解决 3 个更深的问题**：

1. **何时切换模型**：同样的规划任务，前 3 步用 Sonnet 4 足够，第 4 步涉及安全审计时必须升级到 Opus 4.8 并开 Audit Trail
2. **如何合成答案**：5 个专家模型各自返回片段后，谁负责拼装、做去重、做 conflict resolution
3. **如何演化**：每 3 个月底座模型升级一次，所有 routing 规则都要重新调

**Fugu 的回答**：把 1/2/3 三件事**全部内化进一个语言模型**——Fugu 本身就是一个 LLM，但它的"token 序列"不是最终答案，而是「调用哪个专家模型 / 如何处理子任务 / 如何合成结果」的决策。

### 1.2 工业级 multi-agent 的 5 个成熟案例

2026 年已经有多家厂商把 multi-agent orchestration 推向 GA（General Availability）：

- Microsoft Agent Framework 1.0 GA（[microsoft-agent-framework-v1-ga-architecture-2026](../orchestration/microsoft-agent-framework-v1-ga-architecture-2026.md)）——Workflow + Orchestrator 双层
- CrewAI 1.7B+ workflows（[crewai-agentic-systems-missing-architecture-1-7-billion-workflows-2026](../frameworks/crewai-agentic-systems-missing-architecture-1-7-billion-workflows-2026.md)）——Entanglement 模型
- Anthropic Claude Agent SDK + Computer Use（[anthropic-claude-code-advanced-patterns-five-engineering-mechanisms-2026](../frameworks/anthropic-claude-code-advanced-patterns-five-engineering-mechanisms-2026.md)）——5 大工程机制

这些都还停留在**显式 workflow**层。Sakana Fugu 走的是另一条路：**让 LLM 自己学会何时 delegate**。

---

## 二、Fugu 的架构：TRINITY + Conductor 双层

Fugu 的工程结构可以拆成两层，每层对应一篇 ICLR 2026 论文：

### 2.1 TRINITY 层（隐藏态路由，per-token 决策）

**论文**：[TRINITY: An Evolved LLM Coordinator (ICLR 2026, arXiv 2512.04695)](https://arxiv.org/abs/2512.04695)
**角色**：用 LLM 自己的 hidden state 训练一个线性头（linear head），输出对 worker pool 中每个模型的选择概率。

```python
# TRINITY 决策逻辑（伪代码）
class TrinityRouter(nn.Module):
    def __init__(self, base_llm, worker_pool: list[str]):
        super().__init__()
        self.base = base_llm
        self.head = nn.Linear(base_llm.hidden_size, len(worker_pool))

    def forward(self, input_ids):
        h = self.base(input_ids).last_hidden_state[:, -1, :]
        routing_logits = self.head(h)        # [B, num_workers]
        return F.softmax(routing_logits, dim=-1)
```

**训练方式**：sep-CMA-ES（separated Covariance Matrix Adaptation Evolution Strategy）——纯进化策略，不依赖 Sakana 原始权重。OpenFugu 复现这个训练流程 `train/train_trinity.py` 时，**5 代就能从随机路由收敛到最优路由**（mock 验证）。

**TRINITY 的关键优势**：

| 维度 | 显式规则路由 | TRINITY 路由 |
|------|------------|-------------|
| 决策信号 | prompt 关键词 / 任务类型 | hidden state（连续、稠密） |
| 可学习 | 需人工重写规则 | sep-CMA-ES 自动进化 |
| 跨任务泛化 | 弱（一个规则一个场景） | 强（一个 head 多个任务） |
| 训练成本 | 0 | ~5 generations（mock） |

### 2.2 Conductor 层（自然语言编排，跨任务工作流）

**论文**：[Learning to Orchestrate Agents in Natural Language with the Conductor (ICLR 2026, arXiv 2512.04388)](https://arxiv.org/abs/2512.04388)
**角色**：用自然语言描述工作流，Conductor 解析后生成 workflow-DAG（节点 = 子任务，边 = 数据流），调度 worker pool 执行。

```python
# Conductor 决策（伪代码）
class Conductor:
    def orchestrate(self, user_request: str) -> WorkflowDAG:
        # Conductor 本身是一个 LLM，输入是用户请求，输出是工作流 JSON
        dag_json = self.llm.parse(
            f"Decompose this into a workflow: {user_request}\n"
            f"Available workers: {self.worker_pool}\n"
            f"Output: JSON with nodes/edges"
        )
        return WorkflowDAG.from_json(dag_json)

    def execute(self, dag: WorkflowDAG) -> str:
        for level in dag.topological_levels():
            results = parallel_call(level.nodes)
            dag.update_with_results(results)
        return dag.synthesize()
```

**Conductor 的训练**：GRPO（Group Relative Policy Optimization）在 [ToolScale](https://huggingface.co/datasets/nvidia/ToolScale) 上训练，OpenFugu 复现 `train/train_conductor.py` 时，**reward 从 1.21 升到 1.64（100 步）**。

### 2.3 TRINITY × Conductor 的协作

| 决策 | 决策层 | 决策粒度 | 训练方法 |
|------|-------|---------|---------|
| "这条 token 用哪个模型解码" | TRINITY | per-token | sep-CMA-ES |
| "这个任务拆成几个子任务" | Conductor | per-task | GRPO |
| "Fugu Ultra 模式 vs Fugu base" | Sakana 配置 | per-workload | 监督微调 |

**Fugu Ultra 是什么**：Fugu 的高配版——协调「更深」的专家池（更多 worker、更长推理链、更多 verification step）。Fugu Ultra 在 StandardBench / EngineeringBench / ScientificBench 上与 Fable 5、Mythos Preview 比肩，且**规避出口管制风险**。

---

## 三、Fugu vs 显式 multi-agent：4 维对比

| 维度 | 显式 multi-agent（LangGraph / CrewAI） | Fugu（learned orchestration） |
|------|---------------------------------------|------------------------------|
| **workflow 表达** | 代码 / JSON | 自然语言 → Conductor → DAG |
| **模型选择** | role-based routing 规则 | TRINITY hidden-state head |
| **演化能力** | 人工重写 | 底座模型升级 → 自动继承 |
| **可验证性** | 强（每步可追溯） | 弱（决策黑盒） |
| **延迟** | 低（无 LLM 决策开销） | 中（Fugu 自身推理 ~200ms） |
| **成本** | 中（多模型 + 编排开销） | 中偏高（Fugu 推理 + worker 调用） |

**最重要的差异是「演化能力」**：

```
[底座模型升级] Claude Opus 4.8 → Claude Opus 4.9
  显式 multi-agent:
    开发者: "我需要把 47 个 routing rule 中的 12 个改一下"
    耗时: 2-3 周（测试 + 灰度）
  Fugu:
    开发者: "Opus 4.9 进了 worker pool，重训 Conductor"
    耗时: 1-2 天（GRPO 100 步）
```

Fugu 文档原文：

> Because Fugu is built on learned orchestration rather than fixed workflows, it improves as the underlying ecosystem improves: as new frontier models arrive, we can fold them into Fugu's agent pool and pass the gains on to you.

---

## 四、Fugu 的工业验证：早期用户 5 大场景

Sakana 公开了 beta 期 500 个早期用户的反馈，5 大场景的工程数据如下：

| 场景 | 任务类型 | 关键指标 | 用户原话 |
|------|---------|---------|---------|
| **Code Review** | 静态分析 | Fugu Ultra 找到 20+ bug vs 其他工具 3 个 | "becomes the model I run all my reviews through" |
| **Orchestration** | 长会话 persona 稳定性 | 长 session identity 不漂移 | "persona stability ... may matter more than raw benchmark scores" |
| **Security Assessment** | recon + XSS/SQLi + auth 审计 | 端到端一气完成 | "drove a full security assessment end-to-end" |
| **Paper Reproduction** | 读论文 → 实现 → 跑实验 | 500 用户自动运行 | "automated research mode saw it drive meaningful progress" |
| **Patent Investigation** | 长文档检索 + 证据链 | 减少手工整理 | (内部 benchmark) |

**5 大场景的共同点**：都是"messy, long-running, multi-step"——单次模型调用搞不定，必须 sustained progress across many steps。这正是 Fugu Ultra 的设计目标（multi-step + multi-agent + verification loop）。

---

## 五、为什么 Fugu 重要：2026 H2 的 3 个拐点

### 5.1 模型层 vs 编排层的博弈

2024–2025 的主流叙事是「让模型本身更强」（bigger model = better answer）。2026 H1 出现转折：

```
Sakana Fugu:    "让编排本身是模型"  → learned orchestration
Microsoft MAF:  "让编排是 Workflow 引擎" → explicit DAG
CrewAI:         "让编排是 Entangled agents" → entanglement
Anthropic:      "让编排是 Claude Agent SDK" → SDK + Computer Use
```

5 条路径都在尝试解决同一个问题：模型 scaling 见顶后，下一个杠杆在编排层。**Fugu 是唯一把"编排层"也变成 LLM 的方案**——这是对"模型即编排"假设的工业验证。

### 5.2 合规性拐点：Fugu Ultra 的「出口管制免疫」

Fugu Ultra 的工程价值不只是 benchmark 数字，还有 **export control immunity**——它协调的 agent pool 不依赖特定国家的前沿模型：

> Our Fugu Ultra model stands shoulder-to-shoulder with leading models like Fable 5 and Mythos Preview across the industry's most rigorous engineering, scientific, and reasoning benchmarks. **It delivers frontier capability without the risk of export controls.**

这与 Anthropic 的 [Fable 5 + Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)（2026-06-13）形成有趣对照——Fable/Mythos 走"超大模型 + 出口管制"，Fugu 走"多模型编排 + 出口管制免疫"。

### 5.3 开源可复现性拐点：OpenFugu 验证

Fugu 的工程价值只有"被独立复现"才真正可信——**OpenFugu**（[trotsky1997/OpenFugu](https://github.com/trotsky1997/OpenFugu)）就是这件事：

- **4 阶段复现**：`read → run → train → serve`
- **验证结果**：`mini.py --self-test` = **95% / 100% on 37-case fixture（真实 Sakana 权重）**
- **训练复现**：TRINITY sep-CMA-ES 5 代收敛；Conductor GRPO 100 步 reward 1.21 → 1.64
- **Eval 结果**：**per-question routing 比 best single worker +107%**（关键 caveat：这是 query-level，不是 per-step coordination）

完整的项目分析见关联项目文章 [trotsky1997-openfugu-fugu-reverse-engineering-245-stars-2026](../../projects/trotsky1997-openfugu-fugu-reverse-engineering-245-stars-2026.md)。

---

## 六、Fugu 的 3 个未解决问题

### 6.1 决策可解释性

Fugu 的 routing 决策是 black box——用户无法知道"为什么这个问题用 GPT-5.5 而不是 Opus 4.8"。这与 Anthropic [preparing-your-security-program-for-ai-accelerated-offense](https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense) 的可解释性要求冲突。**可能的工程方向**：在 Conductor 输出 DAG 时同步输出 reasoning trace（OpenFugu 的 `eval/eval_orchestration.py` 还没有这一步）。

### 6.2 跨厂商 worker pool 的延迟方差

Fugu 的 worker pool 来自不同厂商（OpenAI / Anthropic / Google / Open-weights），各家 API 延迟分布不同（p50 vs p99 差 3-10×）。Conductor 在编排 DAG 时**没看到 worker 的当前 latency**，可能把关键路径分配给慢 worker。**OpenFugu 复现时实测**：live 模式 lat 2-4× mock。

### 6.3 长期 session 的成本控制

Fugu Ultra 强调"长 session persona stability"，但这天然导致 **token 消耗累积**——500 用户用 Fugu Ultra 跑 AutoResearch 平均消耗 ~80M tokens/run（Sakana 内部数据未公开，需要 reverse engineering 推断）。**可能的工程方向**：动态降级（Fugu Ultra → Fugu base 在 session 后段）。

---

## 七、适用边界

### 7.1 适合用 Fugu 的场景

- 任务**长、杂、多步**（paper reproduction、security assessment、code review）
- 任务**不依赖单一前沿模型**（避免 vendor lock-in）
- 团队**有合规 / 出口管制**约束
- 团队**愿意接受 Fugu 推理的 ~200ms 开销**

### 7.2 不适合用 Fugu 的场景

- 任务**单步可解**（chatbot 简单问答）——直接调 worker 即可
- 任务**强可解释性要求**（金融 audit、医疗诊断）——显式 multi-agent 更可控
- 任务**成本极敏感**（每 token 都算）——Fugu 自身推理叠加 worker 成本
- 任务**需要 fine-grained 工具控制**——Conductor 的 DAG 抽象会丢失细节

---

## 八、结论：编排范式的第二次迁移

Fugu 不只是"另一个 multi-agent 框架"——它代表编排范式从 **explicit workflow** → **learned orchestration** 的第二次迁移：

```
2024-2025: 显式 multi-agent (LangGraph / CrewAI / AutoGen)
           ↓ 显式 workflow → 灵活但需大量人工维护
2026 Q1:   role-based routing
           ↓ role → model 分配 → 解决 over/under-provisioning
2026 Q2:   Fugu / learned orchestration
           ↓ 编排本身 = LLM → 自演化、自决策
2026 Q3+:  ??? (可能方向: learned verification, learned cost control)
```

Sakana Fugu 的真正价值不是"今天就能用"，而是**给 learned orchestration 提供了工业级可行性证据**。接下来 6 个月会出现：
1. **更多厂商跟进**：OpenAI / Anthropic / Google 都会推出自己的 "Fugu 替代品"
2. **TRINITY + Conductor 的开源实现成熟**：OpenFugu 是先驱，更多复现项目会跟上
3. **可解释性工具涌现**：解决 Fugu 的 black box 决策问题
4. **verifier 集成**：与 [sakana-ai-scientist-automated-scientific-discovery-loop-14082-stars-2026](../../projects/sakanai-ai-scientist-automated-scientific-discovery-loop-14082-stars-2026.md) 的 LLM Reviewer 形成闭环

**对工程团队的建议**：
- 短期（1-3 月）：继续用显式 multi-agent（LangGraph / CrewAI），Fugu 还在 GA 早期
- 中期（3-6 月）：PoC 一个 Fugu 场景（推荐 code review 或 security assessment），验证 4 维对比是否符合你的 workload
- 长期（6-12 月）：如果 Fugu Ultra 的 cost control 成熟，考虑把"长 session + 多步任务"从 LangGraph 迁到 Fugu

---

## 关联阅读

- **底层论文 1**: [TRINITY: An Evolved LLM Coordinator (ICLR 2026)](https://arxiv.org/abs/2512.04695)
- **底层论文 2**: [Learning to Orchestrate Agents in Natural Language with the Conductor (ICLR 2026)](https://arxiv.org/abs/2512.04388)
- **关联项目**: [OpenFugu 独立复现 (245⭐ Apache-2.0)](../../projects/trotsky1997-openfugu-fugu-reverse-engineering-245-stars-2026.md) — 现象（论文 + 闭源模型）+ 工具（独立 Apache-2.0 复现）闭环
- **同主题先驱**: [SakanaAI/AI-Scientist (14K⭐) 自动化科研闭环](../../projects/sakanai-ai-scientist-automated-scientific-discovery-loop-14082-stars-2026.md) — Sakana 在 scientific discovery 领域的另一工业闭环
- **范式对照**: [multi-model-routing-coding-agents-role-based-2026](../fundamentals/multi-model-routing-coding-agents-role-based-2026.md) — 显式 role-based routing（2026 H1 主流）
- **范式对照**: [llm-model-routing-agent-architecture-2026](../fundamentals/llm-model-routing-agent-architecture-2026.md) — 架构层模型路由
- **编排竞争**: [microsoft-agent-framework-v1-ga-architecture-2026](../orchestration/microsoft-agent-framework-v1-ga-architecture-2026.md) — 显式 Workflow 引擎路径
- **合规对照**: [Anthropic Fable 5 + Mythos 5 (2026-06-13)](https://www.anthropic.com/news/claude-fable-5-mythos-5) — 出口管制路径 vs Fugu 出口管制免疫路径
- **Sakana 官方**: [Sakana AI Fugu Release (2026-06-22)](https://sakana.ai/fugu-release/)
