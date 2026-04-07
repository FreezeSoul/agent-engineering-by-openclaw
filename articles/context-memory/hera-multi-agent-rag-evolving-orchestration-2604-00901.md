# Multi-agent RAG的下一站：从检索到编排的经验驱动演进

> **核心问题**：现有Multi-agent RAG依赖静态Agent行为和固定编排策略，在复杂多跳任务上Brittle。HERA通过双层演进机制——全局编排策略优化+局部Agent Prompt演进——在不更新参数的情况下实现持续自适应。

---

## 一、静态编排的困境：Multi-agent RAG为何Brittle

Multi-agent RAG通过协作式 specialized agents 扩展了传统RAG的能力边界，支持需要多步推理和多源检索的复杂查询。

**但现有方案的致命缺陷**：

| 问题 | 根因 | 后果 |
|------|------|------|
| 固定/顺序编排 | 无法适应查询相关的推理和检索复杂度差异 | 证据收集不足或不必要的检索开销 |
| 错误级联 | 多轮交互中错误 compounding | 长时程Agent协作中性能快速衰减 |
| 有限的归因 | 依赖最终答案正确性的全局监督信号 | 无法精确定位特定失败源 |
| 训练成本高 | 主流训练方法需要大量轨迹数据 | 无法支持动态知识环境中的持续适应 |

**核心矛盾**：随着查询分布和底层语料库演进，固定的推理和协作策略导致性能停滞和泛化脆弱。

---

## 二、HERA的核心设计：三层协作演进

HERA（Hierarchical Evolution RAG）通过三层架构实现**全局编排策略**和**局部Agent行为**的联合演进：

```
┌─────────────────────────────────────────────────────────┐
│                    全局编排层（Top）                      │
│        Orchestrator：生成查询特定的执行计划                 │
│        基于 Group Relative Policy Optimization (GRPO)     │
│        优化 Agent 拓扑结构                                │
├─────────────────────────────────────────────────────────┤
│                   经验库（Bridge）                        │
│     Profile-Insight-Utility 结构 (c, z, u)               │
│     积累成功/失败轨迹的语义优势，作为编排学习的指导信号       │
├─────────────────────────────────────────────────────────┤
│                   局部Agent层（Bottom）                  │
│     Role-aware Prompt Evolution (RoPE)                   │
│     操作规则 + 行为原则 双轴适应                           │
│     无需更新底层LLM参数                                   │
└─────────────────────────────────────────────────────────┘
```

**核心创新**：将策略优化从参数更新转变为**经验驱动的上下文适应**。

---

## 三、全局编排层：结构级策略优化

Orchestrator 的优化灵感来自 Group Relative Policy Optimization（GRPO）——通过组内采样的动作比较来更新策略。

**HERA的扩展**：将优化从 token 级生成提升到**协作拓扑级**。

```python
# 伪代码：Orchestrator的拓扑优化
for each query q:
    # 1. 从经验库中检索相关Insight
    insights = experience_library.retrieve(q)
    
    # 2. 基于Insight生成G个候选Agent序列
    candidate_topologies = [
        orchestrator.sample_topology(q, insights)
        for _ in range(G)
    ]
    
    # 3. 执行每个序列并获取奖励
    trajectories = [execute(topo) for topo in candidate_topologies]
    rewards = [evaluate(traj) for traj in trajectories]
    
    # 4. 分层比较：先按任务性能排序，再按效率排序
    # 5. 生成语义优势（而非数值梯度）
    semantic_advantages = orchestrator.explain(
        successful_trajectories,
        failed_trajectories
    )
    
    # 6. 更新经验库
    experience_library.consolidate(semantic_advantages)
```

**关键洞察**：语义优势编码了有效的推理策略、Agent交互模式和失败模式的结构化知识——可解释、可组合，完全替代了数值梯度。

---

## 四、经验库：语义优势的存储与检索

经验库 **ℰ** 采用 Profile-Insight-Utility 结构：

| 字段 | 含义 |
|------|------|
| `c` | 查询特征/类型 |
| `z` | 自然语言洞察 |
| `u` | 效用：洞察在后续编排中成功应用的频率 |

**检索时的双重目标**：
1. **效用最大化**：优先选择历史上导致成功编排的高效用洞察
2. **多样性保持**：选择与已选洞察语义不同、先验使用频率低的洞察

**更新操作**（在线进行）：
- **ADD**：插入与现有条目不重复的新洞察
- **MERGE**：合并语义相似或互补的条目
- **PRUNE**：移除冲突或低效用洞察
- **KEEP**：保持不变

---

## 五、Role-aware Prompt Evolution（RoPE）：局部行为优化

即使全局编排策略正确，局部Agent仍可能失败——要么是**修正失败**（Agent忽略可操作的错误信号），要么是**增强失败**（Agent坚持次优策略）。

**RoPE的双轴适应**：

```
Δρᵢ = Δρᵢᵒᵖ + Δρᵢᵇᵖ

其中：
- Δρᵢᵒᵖ（操作规则）：短期纠正行为，从近期失败中提取
- Δρᵢᵇᵖ（行为原则）：长期策略，从跨轨迹模式中提炼
```

**行为轴**：Thoroughness、Risk Sensitivity、Error Correction、Heuristic Injection

**Prompt更新的数学表达**（底层LLM固定）：

```
π_𝒩ᵢⁿᵉʷ(y|x) ∝ π_𝒩ᵢᵇᵃˢᵉ(y|x) · exp(f_{ρᵢ}(x,y))
```

诱导了一种隐式正则化效果，确保稳定和一致的策略更新。

**拓扑突变**：当轨迹持续失败时（如F1=0），触发拓扑突变——替换失败的Agent或增加额外Agent，探索替代结构。

---

## 六、实验结果

**6个知识密集型基准测试**：

| 数据集 | 基线SOTA | HERA提升 |
|--------|---------|---------|
| HotpotQA | 55.04 (ExSearch) | **63.03** (+8pp) |
| 2WikiMultiHopQA | 52.75 (AceSearcher) | **64.77** (+12pp) |
| MusiQue | 65.54 (R1-Searcher) | **67.81** (+2pp) |
| AmbigQA | 63.80 (ExSearch) | **67.81** (+4pp) |
| Bamboogle (OOD) | 51.27 (ExSearch) | **60.53** (+9pp) |
| HoVer (OOD) | 66.62 | **67.35** (+1pp) |

**平均提升 38.69%** over recent baselines，同时保持Token效率。

**拓扑演进发现**：稀疏探索产生紧凑、高效用的多Agent网络——证明系统自组织出高效协作和鲁棒推理能力。

---

## 七、工程可用性评估

**优势**：
- **无需训练**：完全依赖上下文学习，底层LLM参数冻结
- **双重演进**：编排策略 + Agent行为联合优化，覆盖完整优化空间
- **可解释**：语义优势提供人类可读的决策解释
- **Token高效**：经验库驱动的先验避免无效探索

**局限**：
- **评估信号依赖**：依赖最终答案正确性作为奖励，稀疏反馈场景可能效果有限
- **拓扑搜索开销**：G个候选序列的完整执行在超大规模任务上可能开销大
- **经验库维护**：长期运行中经验库可能面临质量衰减问题

**工程落地路径**：
1. **增量引入**：可将RoPE机制单独集成到现有Agent系统中
2. **经验库初始化**：使用少量人工标注轨迹建立种子经验
3. **混合优化**：与RL微调结合，在保持适配性的同时提升基础能力

---

## 八、与现有工作的关系

| 维度 | VMAO | Self-Optimizing MA | HERA |
|------|------|---------------------|------|
| 全局编排 | Plan-Execute-Verify-Replan | 评估器反馈 | GRPO启发的语义优势 |
| 局部优化 | 无 | Prompt自优化 | Role-aware Prompt Evolution |
| 经验利用 | 无 | 无 | 经验库作为先验 |
| 拓扑适应 | 固定拓扑 | 固定拓扑 | **拓扑突变** |

**互补性**：HERA的拓扑突变机制 + VMAO的Verify信号 = 更完整的自适应Multi-Agent系统。

---

## 参考文献

- [Experience as a Compass: Multi-agent RAG with Evolving Orchestration and Agent Prompts](https://arxiv.org/abs/2604.00901) — HERA论文原文，2026年4月
- [Group Relative Policy Optimization (GRPO)](https://arxiv.org/abs/2409.20189) — Orchestrator优化的理论基础
- [Self-Optimizing Multi-Agent Deep Research (arXiv:2604.02988)](https://arxiv.org/abs/2604.02988) — 仓库已有，Stage 8×9交叉
- [VMAO: Verified Multi-Agent Orchestration (arXiv:2603.11445)](https://arxiv.org/abs/2603.11445) — 仓库已有，Stage 7编排
