# 多模型路由的架构陷阱：编码 Agent 的角色化模型分配

> **核心问题**：为多 Agent 编码系统中的每个角色分配单一模型，同时产生两类失败——简单任务过载浪费算力，复杂任务欠载导致质量劣化级联。角色化模型路由是解决这个问题的架构级方案。
>
> **读完能得到什么**：理解角色化模型分配为何同时导致成本失控和质量劣化；掌握规划/导航/生成/审查四类角色的路由决策标准；理解静态路由、动态路由和学习型路由的实现差异与取舍。

---

## 一、问题：单一模型分配的两类同步失败

### 1.1 多 Agent 编码系统的角色分工

现代编码 Agent 系统普遍采用多角色分工架构。一个典型配置：

```
Coordinator Agent（规划/分解）
  → Implementation Agent（代码生成）
    → File Navigation Agent（文件读写）
    → Test Agent（测试生成）
  → Code Review Agent（审查）
```

每个角色承担不同类型的认知任务，其模型需求存在显著差异。

### 1.2 两类同步失败

**失败模式一：Over-Provisioning（过载）**

将旗舰模型（如 Opus 4.6）分配给所有角色，造成计算资源浪费。以文件导航操作为例：

| 模型 | 输入 Token 成本 | 用于文件导航的浪费程度 |
|------|-------------|---------------------|
| Opus 4.6 | $5.00/MTok | 目录遍历不需要深度推理 |
| Haiku 4.5 | $1.00/MTok | 模式匹配任务完全够用 |

将 Opus 用于文件导航，相比 Haiku 增加约 **5 倍成本**，而任务质量没有任何提升——目录遍历、符号解析、导入路径追踪都是结构化的模式匹配操作，不需要深层推理。

**失败模式二：Under-Provisioning（欠载）**

将较小模型用于规划/协调类任务，导致错误级联。一个规划能力不足的 Coordinator 会产出格式错误的子任务规范，而下游 Agent 基于这些错误输入工作，没有任何上游纠正机制。

Anthropic 明确将 Opus 4.6 定位用于「需要最深度推理」的任务，如代码库重构和跨 Agent 工作流协调。将 Haiku 用于规划任务产生的畸形输出，是系统设计的失败而非模型的问题。

### 1.3 问题的本质

MasRouter 论文（ACL 2025）从形式化角度证明了这个问题：

> *"Model routing depends on 'the task's domain and difficulty, as well as their corresponding role.' The same research refutes the assumption that the largest model always wins: 'larger LLMs have been shown not to always outperform their smaller counterparts.'"*

这个结论否定了「用最强模型处理所有任务」的自然假设。正确的模型路由取决于：任务类型（Domain）、任务难度（Difficulty）、Agent 角色（Role）。

---

## 二、角色化路由：四类角色的决策标准

### 2.1 角色分类与路由决策

| Agent 角色 | 任务类型 | 推荐模型 | 核心需求 | 过载代价 |
|-----------|---------|---------|---------|---------|
| **规划/协调** | 任务分解、依赖推理、并行工作流管理 | Opus 4.6 | 最深度推理能力 | 规划失败 → 级联错误，无法被下游修正 |
| **文件导航** | 目录遍历、符号解析、导入追踪 | Haiku 4.5 | 高吞吐、模式匹配 | 5 倍成本浪费，质量无提升 |
| **代码生成** | 上下文感知的代码实现 | Sonnet 4.6 | 平衡推理与上下文窗口 | 固定上下文窗口导致大文件截断或小任务浪费 |
| **代码审查** | 漏洞识别、安全问题、风格一致性 | GPT-5.2 或 Sonnet 4.6 | 异步/同步不同需求 | 旗舰模型造成序列化瓶颈 |

### 2.2 规划/协调角色详解

**为什么必须用旗舰模型**

规划/协调失败的后果是系统性的。一个能力不足的 Coordinator 会：

1. 产生模糊的子任务分解，导致 Implementation Agent 无法正确执行
2. 遗漏任务间的依赖关系，导致并行工作流出现死锁或数据不一致
3. 无法正确处理跨 Agent 的状态同步

Anthropic 将 Opus 4.6 明确定位用于「协调 Agent 工作流」——这是有道理的。规划是 Agentic Loop 中推理深度需求最高的环节。

**路由决策树**：

```
任务复杂度评估：
  - 是否涉及跨模块依赖分析？ → Opus
  - 是否需要多步推理验证可行性？ → Opus
  - 任务是否高度结构化且无歧义？ → 可降级至 Sonnet
```

### 2.3 文件导航角色详解

**为什么不需要旗舰模型**

文件导航操作的本质是结构化查询：

- 目录遍历：递归扫描文件树，匹配特定模式
- 符号解析：查找类/函数定义位置
- 导入追踪：构建依赖关系图

这些都是模式匹配和图遍历操作，不需要 LLM 的推理能力。一个优化良好的 Haiku 模型完全可以处理这些任务，且成本降低 80%。

**关键数据**：以每天 1000 次文件读取计算：
- Opus 4.6：1000 × 平均输入 50K tokens × $5/MTok = **$250/天**
- Haiku 4.5：1000 × 平均输入 50K tokens × $1/MTok = **$50/天**

年度差异：**$73,000 vs $18,250**，差距来自同一个任务类型的模型选择。

### 2.4 代码生成角色详解

**上下文窗口的动态适配问题**

代码生成任务的大小差异极大：

| 任务规模 | Token 需求 | 适合模型 |
|---------|-----------|---------|
| 小型编辑（<4K tokens） | 标准上下文窗口 | 标准模型（Sonnet） |
| 中型任务（4K-32K tokens） | 增强上下文 | Sonnet 4.6 / GPT-4o |
| 大型重构（>32K tokens） | 大上下文窗口 | Opus / GPT-4o-128K |

CrewAI 文档明确指出：固定模型分配意味着固定上下文窗口，这会导致两种浪费：

- **截断问题**：大文件编辑时指令被截断，导致不完整的代码生成
- **资源浪费**：小编辑任务分配大上下文窗口，浪费计算资源

### 2.5 代码审查角色详解

**同步 vs 异步审查的模型选择**

代码审查面临一个独特的选择困境：

- **同步审查**：Agent 需要等待审查结果才能继续，高质量模型（Opus）造成流水线瓶颈
- **异步审查**：审查结果可以稍后处理，可以接受 Sonnet 级别的模型

正确的做法是根据审查类型选择模型：

```python
# 审查类型路由逻辑
def route_review_task(code_snippet, is_security_critical: bool):
    if is_security_critical:
        return "opus-4.6"  # 安全关键代码需要最深分析
    elif is_sync_blocking:
        return "sonnet-4.6"  # 同步阻塞优先速度
    else:
        return "haiku-4.5"  # 异步审查可接受较低质量
```

---

## 三、三种路由实现方案

### 3.1 静态路由

**原理**：使用预定义规则将任务分发到指定模型，无运行时内容分析。

Anthropic 的 Sub-agents API 提供了最直接的静态路由实现：

```python
# Anthropic Sub-agents API 的静态路由示例
subagents = [
    {
        "name": "coordinator",
        "model": "opus-4.6",  # 固定旗舰模型
        "instructions": "分解任务并协调子 Agent"
    },
    {
        "name": "implementor", 
        "model": "sonnet-4.6",  # 固定实现模型
        "instructions": "根据子任务生成代码"
    },
    {
        "name": "file-nav",
        "model": "haiku-4.5",  # 固定轻量模型
        "instructions": "执行文件读写操作"
    }
]
```

**适用场景**：工作负载可预测，任务类型与 Agent 角色的映射关系固定（如固定的三阶段 Pipeline）。

**局限性**：
- 无法处理同一角色内的复杂度差异（如 Implementation Agent 面临的任务从简单编辑到大型重构）
- 规则维护成本随场景复杂度线性增长
- 无法适应运行时上下文的变化

### 3.2 动态路由

**原理**：在运行时分析任务复杂度，动态选择模型。

动态路由需要三个组件：

```python
# 动态路由的核心组件
class DynamicRouter:
    def __init__(self):
        self.complexity_classifier = load_model("task-complexity-v1")
        self.model_registry = {
            "planning": "opus-4.6",
            "implementation": "sonnet-4.6", 
            "navigation": "haiku-4.5",
            "review": "sonnet-4.6"
        }
    
    def route(self, task: Task, role: str) -> str:
        # Step 1: 评估任务复杂度
        complexity = self.complexity_classifier.predict(task)
        
        # Step 2: 结合角色约束决定模型
        base_model = self.model_registry[role]
        
        # Step 3: 复杂度驱动的模型升级/降级
        if complexity == "high" and role == "navigation":
            return base_model  # 导航任务不升级
        elif complexity == "high" and role in ("planning", "review"):
            return upgrade(base_model)
        elif complexity == "low" and role == "implementation":
            return downgrade(base_model)
        
        return base_model
```

**Augment Code 的实证结果**：通过 Context Engine 的智能模型路由，在多 Agent 同时操作同一代码库时，幻觉率降低 **40%**。这个改善来自：当多个 Agent 共享上下文时，路由层确保每个任务获得「刚好够用」的模型，既避免了资源浪费，也避免了质量不足。

### 3.3 学习型路由

**原理**：通过线上反馈数据自动学习路由策略。

学习型路由将路由决策本身建模为一个优化问题：

```
目标函数：minimize Σ(cost(model_i(task_i)) × weight_i)
约束：quality(model_i(task_i)) ≥ threshold

其中：
  - task_i 是第 i 个任务
  - model_i 是分配给 task_i 的模型
  - cost() 是模型调用的货币成本
  - quality() 是通过线上反馈信号评估的质量分数
```

MasRouter 论文提出了一种基于强化学习的学习型路由方法，核心思想是：

1. **初始策略**：基于规则的基线路由
2. **反馈收集**：在生产环境中收集（task, model, outcome）三元组
3. **策略更新**：使用策略梯度方法更新路由策略
4. **持续优化**：线上流量持续改进路由模型

**挑战**：学习型路由需要足够的反馈数据才能收敛，对于低流量场景不太适用。此外，安全关键的路由决策不适合完全依赖学习的黑盒策略。

---

## 四、角色化路由的工程实践

### 4.1 Anthropic Sub-agents API 的原生支持

Anthropic 的 Sub-agents API 是目前最直接的实现方式：

```python
from anthropic import Anthropic

client = Anthropic()

# 使用静态角色分配创建子 Agent
with client.responses.stream(
    model="claude-opus-4-6",
    tools=[{"name": "CreateSubAgent", "description": "创建子 Agent"}],
    input={
        "role": "coordinator",
        "subagents": [
            {"name": "coder", "model": "claude-sonnet-4-6"},
            {"name": "reviewer", "model": "claude-sonnet-4-6"}
        ]
    }
) as stream:
    for event in stream.events:
        print(event)
```

`model` 字段支持三种指定方式：
- **模型别名**：`sonnet`、`opus`、`haiku`
- **完整模型 ID**：`claude-opus-4-6`
- **inherit**：继承父会话的模型

### 4.2 成本监控与路由审计

角色化路由引入了一个新的运维需求：跟踪每个 Agent 角色的模型消耗。

```python
# 路由审计日志结构
class RoutingAuditLog:
    task_id: str
    agent_role: str
    assigned_model: str
    task_complexity: str  # high / medium / low
    estimated_cost: float
    actual_cost: float
    quality_signal: float  # 从外部评价系统获取
    routing_reason: str  # 路由决策的人工可读解释
```

定期分析这些审计日志可以发现路由策略的系统性偏差。例如：

- 如果 `reviewer` 角色的 `haiku` 模型持续产生低质量信号，说明异步审查也需要升级到 `sonnet`
- 如果 `navigator` 角色的 `haiku` 模型产生大量重试，说明某些导航任务实际上需要更高推理能力

### 4.3 路由的降级策略

任何路由系统都需要定义明确的降级策略，以应对模型不可用或质量问题：

| 触发条件 | 降级动作 |
|---------|---------|
| 指定模型不可用 | 自动降级到同档位的备用模型 |
| 质量信号持续低于阈值 | 升级到更强大的模型并告警 |
| 成本超预算 | 降级非关键角色的模型 |
| 路由决策超时 | 回退到默认模型（不阻断流程）|

---

## 五、角色化路由的局限性

### 5.1 角色边界不总是清晰的

在真实的开发场景中，Agent 的角色分工往往是流动的。一个 `implementor` Agent 可能需要在执行过程中临时承担规划职责。严格的角色-模型绑定在这种边界模糊的场景下会失效。

**缓解方法**：为每个 Agent 设置「角色扩展」能力，允许在特定条件下临时借用其他角色的模型配额。

### 5.2 模型能力边界随版本变化

当模型厂商发布新版本时，之前为某角色选定的模型可能不再是最优选择。建立定期的模型重新评估机制（建议每季度一次）是必要的。

### 5.3 安全关键路径不适合激进路由

对于涉及身份验证、支付处理、数据删除等安全关键操作，即使路由算法推荐了较弱的模型，也应该强制使用旗舰模型。安全预算不能被优化。

---

## 六、核心判断

**多模型路由不是「选哪个模型最强」，而是「每个 Agent 角色需要什么能力的模型」**。

角色化模型分配解决了单一模型分配的两类同步失败：

| 失败模式 | 角色化路由的解法 |
|---------|---------------|
| Over-Provisioning | 用合适能力的模型替换旗舰模型，导航任务从 Opus 降到 Haiku，节省 80% 成本 |
| Under-Provisioning | 规划/审查角色强制使用旗舰模型，避免错误级联导致的系统性质量劣化 |

Augment Code 报告的 **40% 幻觉率降低** 是角色化路由有效性的直接证据：当每个 Agent 角色获得它真正需要的推理能力时，系统的整体可靠性显著提升。

**工程建议**：
1. 从静态路由起步，先建立角色-模型的基线映射
2. 在关键路径（规划、审查）上始终使用旗舰模型
3. 通过审计日志收集质量信号，逐步过渡到动态路由
4. 将安全关键操作排除在路由优化范围之外

---

## 参考文献

- [Augment Code: Best AI Model for Coding Agents in 2026: A Routing Guide](https://www.augmentcode.com/guides/ai-model-routing-guide) — 角色化模型分配的核心数据来源，40% 幻觉率降低的实证来源
- [MasRouter Paper (ACL 2025)](https://aclanthology.org/2025.acl-long.757.pdf) — 固定单模型分配失败的形式化证明
- [Anthropic Model Guide: Choosing a Model](https://docs.anthropic.com/en/docs/about-claude/models/choosing-a-model) — Haiku 定位为高吞吐非推理任务
- [Anthropic Claude Sonnet 4.6 Launch](https://www.anthropic.com/news/claude-sonnet-4-6) — Opus 4.6 定位用于协调 Agent 工作流
- [Anthropic Sub-agents API](https://docs.anthropic.com/en/docs/claude-code/sub-agents) — 静态路由的原生 API 支持
- [SWE-bench Verified Results](https://serenitiesai.com/articles/claude-sonnet-vs-opus-2026) — Sonnet 4.6 (79.6%) vs Opus 4.6 (80.8%) 编码基准对比
