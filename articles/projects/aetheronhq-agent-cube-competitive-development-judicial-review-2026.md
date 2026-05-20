# Agent Cube：用竞争开发和司法审查重新定义多Agent协作

> 核心观点：**让两个Agent用不同模型独立实现同一任务，再让三个Agent法官审查——这不是天方夜谭，而是一个被真实生产项目验证过的工程实践。**

---

## 一、解决的问题：为什么需要一个"竞争+审查"的工作流

传统的多Agent协作通常是**协作式**的——多个Agent分工，各自负责一块，最后合并。这种模式的隐含假设是：**每个Agent的实现都是对的，只需要拼起来**。

但现实是，单个Agent的实现往往不是最优的，甚至可能有方向性错误。Cursor的Planner-Worker-Judge架构解决的是"如何协调大量Agent"，但没有解决"如何保证每个Agent的实现质量"。

> "Judges focused on code quality, missed strategy. Humans catch strategy misalignment. Both needed." — [Agent Cube README](https://github.com/aetheronhq/agent-cube)

Agent Cube解决的是另一个问题：**在方向正确的前提下，如何让多个实现互相竞争，激发出更好的方案**。

---

## 二、核心机制：三角色 + 竞争 + 司法审查

Agent Cube的工作流分为五步：

1. **两个AI Writer用不同模型独立实现同一任务**（如 Sonnet + Codex）
2. **三个AI Judge独立审查两个实现**
3. **系统选择胜者或综合两者优点**
4. **同行评审验证最终方案**
5. **自动创建PR供人工审批**

```
Layer 1: Orchestrator（编排层）
  └─ 规划工作流，分解任务

Layer 2: Prompt Writers（提示编写层）
  └─ 为每个Writer生成详细的任务提示
  └─ 为Judge panel生成评审提示

Layer 3: Code Writers + Judges（执行层）
  ├─ Writer 1 (Sonnet): 实现A
  ├─ Writer 2 (Codex):  实现B
  └─ Judge 1/2/3: 独立评审
```

关键设计：**Writer用不同模型**，利用不同模型的盲点差异（Anthropic 2022 Best-of-N研究证明 N=2 可减少35%错误）。**Judge也用不同模型**，避免单一模型的评价偏差。

---

## 三、司法审查的三层设计

### 3.1 独立评审机制

三个Judge独立评分，每个Judge只知道：
- 任务描述和成功标准
- 自己要评审的是哪个实现（A还是B）
- 评分维度（正确性、可读性、健壮性等）

最终决策：**多数票制**或**共识制**。当两个方案都有价值时，系统会综合两者的最佳元素——这被称作"Synthesis"模式，在Aetheron Connect v2项目中，**40%的功能通过Synthesis获得了比单一实现更好的结果**。

### 3.2 同行评审验证

即使三个Judge都通过了，还有一个peer review步骤验证最终方案的正确性和可合并性。这解决了Judge无法捕捉的战略层面问题：

> "Judges focused on code quality, missed strategy. Humans catch strategy misalignment. Both needed." — [Agent Cube README](https://github.com/aetheronhq/agent-cube)

### 3.3 人工审批门控

最终产物是PR，不是自动合并。这保留了人类对战略方向最终把关的权利。

---

## 四、生产验证：Aetheron Connect v2 项目数据

Agent Cube不是理论构建，它在Aetheron Connect v2项目中经历了真实生产验证：

| 指标 | 数值 |
|------|------|
| 验证周期 | Oct-Nov 2025（两个月）|
| 完成功能数 | 15个 |
| 代码总量 | ~34,000行 |
| 涵盖领域 | Multi-tenancy、Auth0、CRUD factory、OpenAPI + SDK |
| 质量门禁 | 全量测试 + 安全扫描 + CI通过 |

**模型表现规律**：
- Sonnet 4.5：在UI/前端领域全胜（3-0，100%）
- Codex High：在后端领域以7/8领先（88%）
- Grok：作为Judge时平衡性最好

这揭示了一个关键洞察：**不同模型擅长不同领域，选择模型要基于任务类型，而不是只看综合排名**。

---

## 五、与Cursor三角色架构的关联

| 角色 | Cursor架构 | Agent Cube架构 |
|------|-----------|---------------|
| Planner | 探索代码库，创建任务 | Orchestrator：规划工作流，分解任务 |
| Worker | 专注完成分配的任务 | Writer：独立实现任务 |
| Judge | 评估是否继续 | Judge Panel：独立评审并投票 |

**核心区别在于设计哲学**：Cursor的Judge决定"何时停"，解决的是**系统层面的持续推进**；Agent Cube的Judge决定"哪个好"，解决的是**输出质量的选择和提升**。

两者可以组合使用：Cursor的Planner-Worker解决"大规模并行执行"，Agent Cube的竞争-审查解决"每个输出的质量"。

---

## 六、适合什么场景，不适合什么场景

**Agent Cube适合的场景**：
- 新功能开发（2-8小时规模）
- 复杂架构决策（多种实现路径都合理）
- 重构（多种重构方式各有优劣）
- 生产关键代码（需要严格评审）

**Agent Cube不适合的场景**：
- 简单的一次性任务（竞争开销大于收益）
- 有明确唯一正确解的问题（竞争徒劳）
- 需要深度领域知识的任务（AI Judge缺乏专业知识）

---

## 七、快速开始

```bash
# 安装
npm install -g agent-cube

# 创建任务文件
cube auto task.md

# 其中 task.md 包含任务描述
```

Agent Cube CLI会自动：
1. 启动两个Writer（可配置使用Sonnet/Codex/Grok等模型）
2. 收集三个Judge的独立评审
3. 确定胜者或触发Synthesis
4. 创建PR

---

## 八、技术基础

Agent Cube不是拍脑袋的设计，它建立在经过验证的研究基础上：

| 研究 | 发现 | 应用 |
|------|------|------|
| **Best-of-N Sampling** (Anthropic, 2022) | N=2减少35%错误 | 2个Writer = 不同的盲点 |
| **LLM-as-Judge** (Zheng et al., 2023) | AI Judge与人类一致率达85% | 可扩展、一致的代码评审 |
| **Self-Refine** (Madaan et al., 2023) | 迭代批评→修订提高质量 | 多轮反馈直到通过 |
| **Ensemble Methods** (Dietterich, 2000) | 不同模型=不同优势 | Sonnet + Codex + Gemini多样性 |

---

## 九、关联知识

本文是**Agent工程知识体系**中**Orchestration（编排）**的补充，对应演进路径第7阶段（多Agent编排）。与Cursor的三角色架构（Planners/Workers/Judge）形成互补，Cursor解决"大规模并行执行"，Agent Cube解决"输出质量选择"。

| 阶段 | 主题 | 本文关联 |
|------|------|---------|
| 7 | Orchestration | ✅ 竞争-审查模式 |
| 9 | Multi-Agent | Writer-Judge协作模式 |

---

**相关资源**：
- GitHub仓库：https://github.com/aetheronhq/agent-cube
- README原文引用：https://github.com/aetheronhq/agent-cube#readme
- Aetheron Connect v2项目数据：https://github.com/aetheronhq/agent-cube#-proven-results