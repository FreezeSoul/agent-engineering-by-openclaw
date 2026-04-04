# VMAO：验证驱动的多智能体编排——Plan-Execute-Verify-Replan 框架

> **本质**：通过 DAG 驱动的并行执行 + LLM 验证器作为编排级协调信号 + 可配置停止条件，实现多 Agent 质量-资源权衡的工程化框架

---

## 一、基本概念

### 1.1 问题：复杂查询的多 Agent 协调困境

当 Agent 需要回答复杂市场调研类查询时，单一 Agent 的能力边界迅速暴露：
- **子问题间的依赖关系**难以显式建模
- **并行执行**与**结果验证**之间的协调成本高
- **质量与资源的权衡**需要动态调整
- **缺少可验证性**：无法判断子答案是否"足够完整"

VMAO（Verified Multi-Agent Orchestration）提出的核心洞见是：**将 LLM 验证器作为编排级协调信号**，而非仅仅作为结果评分器——验证器的输出直接驱动 replanning 决策。

### 1.2 VMAO 核心定义

```
VMAO = Verified Multi-Agent Orchestration

核心机制：
1. 将复杂查询分解为 DAG（有向无环图）子问题
2. 通过领域特定 Agent 并行执行各子问题
3. LLM 验证器评估结果完整性
4. 自适应 replan 填补缺口
5. 可配置停止条件平衡质量与资源
```

**关键创新**：验证器不是"事后评分"，而是**实时协调信号**——验证结果直接决定是否需要 replan。

---

## 二、核心技术/机制

### 2.1 DAG 驱动的依赖感知并行执行

**子问题分解**：
```python
# 伪代码：VMAO 工作流
query = "分析电动汽车市场趋势及主要竞争者技术路线"
dag = decompose_to_dag(query)
# DAG 节点：
#   Node A: 市场规模估算（无依赖）
#   Node B: 主要竞争者列表（无依赖）
#   Node C: 技术路线分析（依赖 B）
#   Node D: 综合报告（依赖 A, C）
```

**依赖感知执行**：
- 无依赖子问题 → **并行启动**
- 依赖节点 → 等待上游完成，上下文自动传播
- DAG 结构保证拓扑排序正确性

**与 CAMEL/CAMP 的区别**：
- CAMEL：角色分配式 Agent，无 DAG 依赖建模
- CAMP：动态面板组建，但无显式 DAG 验证闭环
- VMAO：**DAG + 验证器 + replan** 三闭环，验证信号直接驱动拓扑变更

### 2.2 LLM 验证器作为编排信号

VMAO 的验证器不是简单的评分输出，而是具有**决策能力的协调器**：

**验证器输出格式**：
```python
verification_result = {
    "complete": bool,           # 子问题是否充分回答
    "gaps": [str],             # 具体缺口列表
    "confidence": float,        # 置信度
    "replan_needed": bool,     # 是否需要 replanning
    "suggested_subqueries": []  # 如果需要 replan，补充哪些子问题
}
```

**关键设计**：验证器具有**"知道何时停止"**的能力——通过可配置停止条件（见 2.3）决定何时接受当前答案而非继续迭代。

### 2.3 可配置停止条件

VMAO 引入了生产系统中极为关键但常被忽视的机制：**资源感知的停止条件**。

**三种停止条件**：

| 条件类型 | 触发规则 | 适用场景 |
|---------|---------|---------|
| **Ready for Synthesis** | 80% 子问题已回答 | 高质量要求，允许充分资源 |
| **High Confidence** | 75% 置信度 + 50% 完成度 | 质量优先于完整性 |
| **Resource Budget** | 已消耗 N tokens / N 轮 | 成本敏感的线上场景 |

这解决了 Multi-Agent 系统的一个根本工程问题：**无限循环风险**——Agent 在无法收敛时会不断 replan，消耗大量资源却产出无进展。

### 2.4 自适应 Replanning

当验证器判定需要 replan 时，VMAO 的 replanning 机制会：

1. 基于缺口分析生成新的子问题
2. 将新子问题插入 DAG
3. 重新计算拓扑顺序
4. 启动新增节点的执行
5. 触发新一轮验证循环

**与其他框架的对比**：

| 框架 | 重试机制 | 拓扑更新 | 验证闭环 |
|------|---------|---------|---------|
| LangGraph | 固定条件重试 | 无 | 无（单一 Agent） |
| CAMEL | 消息迭代 | 无 | 无 |
| CAMP | 三值投票 | 面板重建 | 投票计数 |
| **VMAO** | **DAG 节点级** | **自动重拓扑** | **验证器驱动** |

---

## 三、实验结果与工程价值

### 3.1 核心数据

在 25 个专家策划的市场研究查询上的表现：

| 指标 | 单 Agent 基线 | VMAO | 提升 |
|------|-------------|------|------|
| **答案完整性** | 3.1 / 5.0 | 4.2 / 5.0 | +35% |
| **来源质量** | 2.6 / 5.0 | 4.1 / 5.0 | +58% |

**注意**：这是一个 ICLR 2026 Workshop 论文（MALGAI Workshop），数据来自作者自己的评估，尚未经过外部广泛复现。

### 3.2 工程价值分析

**Token 效率**：VMAO 的 DAG 驱动并行 + 验证器决策机制，理论上比盲目全量探索更节省 token——因为：
- 并行执行减少总步数
- 验证器早期拒绝无效路径
- 停止条件防止过度执行

**可审计性**：每个决策点（分解/执行/验证/replan）都有显式记录，DAG 结构本身就是完整的执行轨迹。

**与生产系统的差距**：
- 依赖外部工具调用（需要 API 集成）
- DAG 生成质量依赖于分解 Agent 的能力
- 验证器的 prompt 敏感性尚未充分评估

---

## 四、与其他 Orchestration 框架的关系

### 4.1 演进路径定位

```
固定拓扑（LangGraph）→ 动态拓扑（CAMP）→ 验证驱动拓扑（VMAO）
                                                    ↑
                                    从"静态路由"到"验证即路由"
```

VMAO 与 CAMP（案例自适应多智能体面板，2604.00085）解决了不同维度的问题：

| 维度 | CAMP | VMAO |
|------|------|------|
| **拓扑变化触发** | 案例类型（诊断类 vs 咨询类）| 验证结果（完整性缺口）|
| **投票机制** | 三值 KEEP/REFUSE/NEUTRAL | LLM 验证器评分 |
| **适用场景** | 专业领域（医疗诊断）| 开放域（市场研究）|

两者可以互补：VMAO 的验证驱动 replan 可以与 CAMP 的动态面板组建结合。

### 4.2 与 Agent Q-Mix 的关系

Agent Q-Mix（2604.00344）解决的是**通信拓扑选择**（broadcast/query/debate/verify），VMAO 解决的是**执行流程编排**——两者处于不同层次：Agent Q-Mix 决定"谁跟谁说话"，VMAO 决定"谁做什么、做到什么程度"。

---

## 五、局限性

1. **外部验证不足**：ICLR 2026 Workshop 论文，尚未广泛复现
2. **工具集成依赖**：DAG 节点执行依赖外部工具 API，框架本身不解决工具可用性问题
3. **分解质量瓶颈**：DAG 生成质量依赖初始分解 Agent 的能力
4. **主观性验证**：LLM 验证器本身具有随机性，验证结果的一致性未充分讨论

---

## 六、参考文献

- Xing Zhang, Yanwei Cui, Guanghui Wang et al. "Verified Multi-Agent Orchestration: A Plan-Execute-Verify-Replan Framework for Complex Query Resolution." arXiv:2603.11445. ICLR 2026 Workshop on MALGAI.

---

## 元信息

- **来源**：arXiv:2603.11445v2
- **作者**：Xing Zhang, Yanwei Cui, Guanghui Wang, Wei Qiu, Ziyuan Li, Fangwei Han, Yajing Huang, Hengzhi Qiu, Bing Zhu, Peiyang He
- **发布时间**：2026年3月（v1: 3/9, v2: 3/15）
- **会议**：ICLR 2026 Workshop on MALGAI
- **分类**：Stage 7（Orchestration）
- **评分**：14/20（工程框架具体；I访果质量中等；创意明确但非突破性；与 CAMP/Agent Q-Mix 有部分重叠）
- **演进链**：固定拓扑 → 动态拓扑（CAMP）→ 验证驱动拓扑（VMAO）
