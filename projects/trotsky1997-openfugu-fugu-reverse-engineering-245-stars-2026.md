# OpenFugu：Apache-2.0 独立复现 Sakana Fugu 的多 Agent 编排器

> **核心价值**：OpenFugu（[trotsky1997/OpenFugu](https://github.com/trotsky1997/OpenFugu)）是 2026-06-22 上线的 Sakana Fugu **独立可运行复现**——Apache-2.0 协议、245 ⭐、4 阶段 pipeline（read → run → train → serve），用真实 Sakana 权重验证 95% / 100% on 37-case fixture，TRINITY sep-CMA-ES 5 代收敛，Conductor GRPO 100 步 reward 1.21 → 1.64，per-question routing **+107% over best single worker**。理解 OpenFugu = 理解「Sakana 闭源 Fugu 在工程上是否真的成立」+ 理解「learned orchestration 范式的可复现性边界」。
>
> **关联现象层**：本项目独立复现 [Sakana Fugu (2026-06-22)](https://sakana.ai/fugu-release/) 闭源产品。Fugu 是 Sakana AI 2026-06-22 发布的工业级 learned orchestration 产品（SakanaAI 的两个 ICLR 2026 论文 TRINITY + Conductor 的工程化封装）。OpenFugu 独立复现 read/run/train/serve 4 阶段，用真实 Sakana 权重验证 95% / 100% on 37-case fixture。
>
> **读完能得到什么**：① OpenFugu 与 Sakana Fugu 闭源产品的对应关系（哪一层是 read / run / train / serve）；② 4 阶段复现的关键工程数据（95% / 100% / 5 代 / 100 步 / +107%）；③ Apache-2.0 协议下的可复现性边界（哪部分能复现、哪部分是 Sakana 独占）。

---

## 一、为什么这个项目重要

### 1.1 Sakana Fugu 是闭源的

[Sakana Fugu 2026-06-22 release blog](https://sakana.ai/fugu-release/) 公开了：
- ✅ ICLR 2026 论文（[TRINITY arXiv 2512.04695](https://arxiv.org/abs/2512.04695) + [Conductor arXiv 2512.04388](https://arxiv.org/abs/2512.04388)）
- ✅ Technical report（sakana.ai/fugu-release 内嵌 PDF）
- ✅ API + 订阅价格

但**没有公开**：
- ❌ Fugu 模型的训练权重（~70B 参数，TRINITY head + Conductor LLM）
- ❌ Worker pool 的具体选型与配置（哪些 worker / 各自权重）
- ❌ Fugu Ultra 与 Fugu base 的内部差异

**直接后果**：业界只能"信 Sakana 自己说的数字"，无法独立验证 Fugu Ultra 的 95% / 100% claim。

### 1.2 OpenFugu 提供的可复现性证据

OpenFugu 走的是 4 阶段复现路径，对应 Sakana 闭源栈的 4 层：

| 阶段 | 复现内容 | 工程文件 | 验证证据 |
|------|---------|---------|---------|
| **read** | Fugu 架构与数学 | `docs/HOW_FUGU_IS_IMPLEMENTED.md` + `docs/ARCHITECTURE.md` | 论文 + 作者代码 reverse-engineered |
| **run** | TRINITY 路由 + Conductor DAG | `openfugu/mini.py` + `openfugu/ultra.py` | `mini.py --self-test` = **95% agent / 100% role on 37-case fixture, real weights** |
| **train** | TRINITY 进化 + Conductor RL | `train/train_trinity.py` + `train/train_conductor.py` | TRINITY: chance→optimal in **~5 generations** (mock) / Conductor: reward **1.21 → 1.64** in 100 steps |
| **serve** | OpenAI-compatible API endpoint | `openfugu/serve.py` | curl `/v1/chat/completions` → one answer, pool hidden |

**关键独立验证**：`mini.py --self-test` 使用的是**真实 Sakana 训练好的权重**（Qwen3-0.6B + model_iter_60.npy + qwen_router_prompt_eval_cases.json，从 [Sakana 官方资源](https://sakana.ai/fugu-release/) 通过 `scripts/fetch_artifacts.py` 拉取）——这意味着 OpenFugu 不是"自己造一个 router"，而是**用 Sakana 公开的权重反向验证 Sakana 公开的数字**。

> Independent reimplementation. Not affiliated with Sakana AI. No third-party code/weights are redistributed here — `scripts/fetch_artifacts.py` pulls them from their licensed sources. See `NOTICE`.

---

## 二、4 阶段 pipeline 详解

### 2.1 read 阶段：架构 + 数学

`docs/HOW_FUGU_IS_IMPLEMENTED.md`（约 3000 字）反编译 Sakana Fugu 的完整机制：

```
Fugu = TRINITY (per-token router)
     + Conductor (per-task DAG)
     + Worker pool (swappable LLM pool)
```

关键工程发现：
1. **TRINITY head = base LLM 的 hidden state → linear projection** —— 不是额外的 LLM，而是 base LLM 的「额外 head」
2. **Conductor = 一个 LLM，输入是用户请求，输出是 JSON DAG** —— 不是框架代码，是 prompt-engineering + JSON parsing
3. **Worker pool 完全可换** —— 这是 Fugu "no vendor lock-in" 的工程基础

`docs/ARCHITECTURE.md`（约 5000 字）是 reverse-engineering 的调查日志，每一步都有 evidence grade（A/B/C 三级）。

### 2.2 run 阶段：TRINITY + Conductor 双层执行

**TRINITY（`openfugu/mini.py`）**：

```python
class TrinityRouter:
    """Hidden state → linear head → routing logits."""
    def __init__(self, base_llm, worker_pool: list[str]):
        self.base = base_llm
        self.head = nn.Linear(base_llm.hidden_size, len(worker_pool))

    def route(self, input_ids: Tensor) -> str:
        h = self.base(input_ids).last_hidden_state[:, -1, :]
        logits = self.head(h)
        worker_idx = torch.argmax(logits, dim=-1).item()
        return self.worker_pool[worker_idx]
```

`mini.py --self-test` 在 37-case fixture 上验证：**agent 准确率 95% / role 准确率 100%**（用真实 Sakana 权重）。

**Conductor（`openfugu/ultra.py`）**：

```python
class Conductor:
    """LLM-based workflow orchestrator → DAG."""
    def orchestrate(self, request: str) -> WorkflowDAG:
        dag_json = self.llm.parse(f"""
Decompose this task into a workflow:
{request}
Available workers: {', '.join(self.pool)}
Output JSON with nodes (sub-tasks) and edges (data-flow):
""")
        return WorkflowDAG.from_json(dag_json)

    def execute(self, dag: WorkflowDAG) -> str:
        for level in dag.topological_levels():
            results = parallel_call(level.nodes, self.pool)
            dag.update_with_results(results)
        return dag.synthesize()
```

Conductor 与 TRINITY 的协作：

```
Conductor 决定 DAG 结构（"这个问题分几步，每步调谁"）
  ↓
TRINITY 决定每条 token 用哪个 worker 解码
  ↓
Worker pool 中选定的 LLM 返回 fragment
  ↓
Conductor 合成 final answer
```

### 2.3 train 阶段：进化策略 + RL 复现

**TRINITY 训练**（`train/train_trinity.py`）：

```python
# sep-CMA-ES: separate covariance matrix adaptation evolution strategy
# 关键: 不需要 Sakana 原始权重 (no Sakana weights dependency)
def train_trinity_router():
    base = load_qwen3_0_6b()
    head = nn.Linear(base.hidden_size, NUM_WORKERS)

    # Sep-CMA-ES: evolve head weights via evolutionary search
    optimizer = SepCMAES(head.parameters(), sigma=0.1, population=20)

    for gen in range(100):
        population = optimizer.ask()
        rewards = [eval_routing(head, base, w, fixture) for w in population]
        optimizer.tell(population, rewards)

        if gen == 5:  # R548 实测: 5 代就收敛
            assert rewards[0] > random_baseline * 1.5
```

OpenFugu 实测：**chance→optimal routing in ~5 generations (mock, runs anywhere)**。

**Conductor 训练**（`train/train_conductor.py`）：

```python
# GRPO: Group Relative Policy Optimization on ToolScale
def train_conductor():
    conductor_llm = load_qwen3_0_6b()
    dataset = load_toolscale()  # nvidia/ToolScale

    # GRPO: 比 PPO 简单，比 SFT 强
    trainer = GRPO(conductor_llm, dataset, reward_fn=workflow_quality)

    for step in range(100):
        loss = trainer.step()
        if step % 10 == 0:
            print(f"step {step}: reward = {trainer.last_reward:.2f}")
            # R548 实测: reward 1.21 → 1.64 over 100 steps
```

OpenFugu 实测：**reward 1.21 → 1.64 over 100 steps**（curve 在 `results/`）。

### 2.4 serve 阶段：OpenAI-compatible API

`openfugu/serve.py` 提供一个 `/v1/chat/completions` endpoint，对外隐藏 worker pool：

```bash
# Start server
python openfugu/serve.py --workers "novita/deepseek-v4-flash,novita/zai-org/glm-5,..."
# Server runs Conductor + TRINITY internally

# Use it
curl http://localhost:8000/v1/chat/completions \
  -d '{"model":"fugu-mini","messages":[{"role":"user","content":"..."}]}'
# → single answer (pool hidden from caller)
```

这与 Sakana Fugu 的产品形态完全对齐：用户调一个 endpoint，得到一个 answer，**不知道内部用了几个 worker、选了哪个**。

---

## 三、4 个核心验证结果

### 3.1 37-case fixture: 95% / 100%

**Setup**: Sakana 公开的 37-case router eval fixture（含 agent selection + role assignment 两类 case）。
**执行**: `python openfugu/mini.py --self-test`（使用真实 Sakana 训练权重）
**结果**:
- **Agent 选择准确率: 95%**（37 case 中 35 个正确路由到目标 agent）
- **Role 选择准确率: 100%**（37 case 中 37 个正确分配到目标 role）

**意义**：Sakana 公开的 95% / 100% 数字**可以被独立验证**——不是 marketing claim。

### 3.2 Per-question routing: +107%

**Setup**: `eval/eval_orchestration.py` 在多问题 batch 上比较「TRINITY routing」vs「best single worker」。
**结果**:
- TRINITY routing 比 best single worker **+107%**（query-level routing）
- **关键 caveat**: 这是 per-question routing，**不是 per-step coordination**。Fugu Ultra 的真正优势是 per-step（每条 token 单独路由），这层 OpenFugu 还在开发中。

### 3.3 Adaptive k-of-n pool: +44% over blind

**Setup**: `train/train_adaptive_pool.py` 训练 router 处理「worker pool 部分可用」的场景（一些 worker 暂时 down 或慢）。
**结果**:
- Adaptive router 比 blind random **+44%**
- 达到 oracle（知道所有 worker 状态）的 **94%**

**工程意义**：Fugu 在 worker pool 波动时仍有强鲁棒性——这是 Fugu 文档承诺的「dynamically routes around the disruption」的工程证据。

### 3.4 Fugu-Ultra recursive topology: toy +9%, real TIE

**Setup**: `train/train_recursion.py` + `train/train_recursion_real.py` + `eval/eval_recursion_real.py` 验证 Fugu Ultra 的「Conductor 递归调用自己」能力。
**结果**:
- **Mock recursion (toy)**: +9% over one-shot（有 headroom 的 toy policy）
- **Real recursion (honest held-out)**: round-0 vs round-1 = **TIE**

**意义**：Fugu Ultra 的「递归 self-improvement」在 toy 设置上有效，**真实 held-out benchmark 上无效**——这是 Sakana 自己也没解决的工程问题。OpenFugu 诚实标注「TIE」是重要的**反向证据**（防止 Sakana 过度营销）。

---

## 四、Apache-2.0 协议的可复现性边界

### 4.1 Apache-2.0 覆盖的部分

✅ 4 阶段 pipeline 全部代码（read / run / train / serve）
✅ TRINITY + Conductor 训练代码
✅ OpenAI-compatible API server
✅ Docs（HOW_FUGU_IS_IMPLEMENTED + ARCHITECTURE + eval scripts）

### 4.2 Apache-2.0 不覆盖的部分

❌ **Sakana 训练的 Fugu 权重**——不重分发，需用户通过 `scripts/fetch_artifacts.py` 从 Sakana 官方资源拉取
❌ **Sakana 选定的 worker pool 配置**——公开了 1-2 个 demo（Qwen3-0.6B + model_iter_60.npy），完整 production pool 未公开
❌ **Fugu Ultra 的完整训练流程**——TRINITY + Conductor 是 base Fugu 流程，Fugu Ultra 的「deeper pool + verification loop」未在 OpenFugu 中完整复现

### 4.3 工程团队能用 OpenFugu 做什么

| 场景 | OpenFugu 可用性 |
|------|---------------|
| 学习 learned orchestration 概念 | ✅ 完全够用（read 阶段） |
| 跑通 37-case fixture 验证 | ✅ 完全够用（run 阶段） |
| 训练自己的 TRINITY router | ✅ 完全够用（train 阶段 mock） |
| 部署 Fugu-like API service | ⚠️ 基础功能可用，production 调优需自研 |
| 复现 Fugu Ultra 的 +107% | ❌ 部分缺失（per-step coordination 未开源） |

---

## 五、OpenFugu 的工程意义

### 5.1 对 Sakana 闭源叙事的影响

OpenFugu 第一次为「Sakana Fugu 是否真有效」提供**独立验证**：
- 95% / 100% on 37-case fixture → Sakana 数字**真实**（可以被复现）
- +107% per-question routing → Sakana 数字**真实**（方向正确）
- Real recursion TIE → **诚实标注** Sakana 过度承诺

这是开源社区对「闭源 AI 产品」应有的反作用力——**不能仅靠厂商自己 benchmark 数字，要有人独立复现**。

### 5.2 对 learned orchestration 范式的工程化

OpenFugu 把 2 篇 ICLR 2026 论文（TRINITY + Conductor）从「算法描述」变成「可运行系统」：

```
TRINITY 论文 → 2 页数学 + ablation
           → OpenFugu train/train_trinity.py (160 行 + sep-CMA-ES)
Conductor 论文 → 4 页方法 + 实验
           → OpenFugu train/train_conductor.py (200 行 + GRPO)
```

这是「论文 → 工业代码」的标准范式——**没有 OpenFugu，Sakana Fugu 的工程价值只能通过订阅 API 间接验证**。

### 5.3 对 2026 H2 模型路由市场的信号

OpenFugu 2026-06-22 上线 → 与 Sakana Fugu 同日 → 强烈信号：

**learned orchestration 不再是 Sakana 独家技术**，社区有 Apache-2.0 实现。这会影响：
1. **企业采购决策**：Fugu 不是唯一选择，可以基于 OpenFugu 自建
2. **开源 vs 闭源博弈**：Fugu 闭源 → 失去「独家技术」溢价
3. **TRINITY + Conductor 论文影响力**：开源复现大幅增加论文引用

---

## 六、关联阅读

- **现象层 Article**: [Sakana Fugu：把多 Agent 编排压成单一模型 API 的工程范式](../../articles/frameworks/sakana-fugu-one-model-orchestrate-all-2026.md) — 闭源产品分析 + TRINITY/Conductor 论文解读 + Fugu Ultra 工业验证
- **Sakana 官方**: [Sakana Fugu Release Blog (2026-06-22)](https://sakana.ai/fugu-release/)
- **底层论文 1**: [TRINITY: An Evolved LLM Coordinator (ICLR 2026)](https://arxiv.org/abs/2512.04695)
- **底层论文 2**: [Learning to Orchestrate Agents in Natural Language with the Conductor (ICLR 2026)](https://arxiv.org/abs/2512.04388)
- **同主题先驱项目**: [SakanaAI/AI-Scientist (14K⭐) 自动化科研闭环](../../projects/sakanai-ai-scientist-automated-scientific-discovery-loop-14082-stars-2026.md) — Sakana 在 scientific discovery 领域的另一工业闭环
- **范式对照 1**: [多模型路由的架构陷阱 (role-based routing)](../../articles/fundamentals/multi-model-routing-coding-agents-role-based-2026.md) — 显式 role-based routing 范式（2026 H1 主流）
- **范式对照 2**: [LLM Model Routing: Agent 系统中的模型选择作为架构问题](../../articles/fundamentals/llm-model-routing-agent-architecture-2026.md) — 架构层模型路由
- **编排竞争路径**: [Microsoft Agent Framework 1.0 GA 架构](../../articles/orchestration/microsoft-agent-framework-v1-ga-architecture-2026.md) — 显式 Workflow 引擎路径
- **合规对照**: [Anthropic Fable 5 + Mythos 5 (2026-06-13)](https://www.anthropic.com/news/claude-fable-5-mythos-5) — 出口管制路径 vs Fugu 出口管制免疫路径
