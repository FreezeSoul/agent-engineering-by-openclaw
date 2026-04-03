# CausalPulse：工业级神经符号多 Agent 副驾驶的架构剖析

> **本质**：首个将神经符号推理与标准化 Agent 协议（ MCP + A2A + LangGraph）深度融合，部署于真实 Bosch 产线的工业级因果诊断多 Agent 系统。98% 成功率、近线性扩展性、端到端 50-60s 延迟，验证了"可解释 + 可落地 + 可扩展"三者可以并存。

**来源**：arXiv:2603.29755v1，2026/03/31，AAAI-MAKE 2026（AAAI Spring Symposium）
**作者**：Chathurangi Shyalika, Utkarshani Jaimini, Cory Henson, Amit Sheth（Kno.e.sis Center, Wright State University）
**标签**：#multi-agent #orchestration #neurosymbolic #industrial #MCP #A2A #causal-inference

---

## 一、基本背景与动机

### 传统工业诊断的三大痛点

现代制造产线依赖大量异构传感器和自动化生产线，必须在严格的质量和良率约束下保持连续运行。但传统分析管道存在三个根本性问题：

1. **阶段割裂**：异常检测、因果推理和根因分析被当作孤立阶段处理——传感器喂入黑盒模型，专家解读警报，干预措施以临时方式执行
2. **可解释性缺失**：黑盒模型给出分数但不给出因果路径，工厂操作员无法理解"为什么认为是这里出了问题"
3. **缺乏标准化**：没有统一的 Agent 通信协议，新工具/新传感器接入需要大量定制开发

### 核心贡献

CausalPulse 的目标是填补"统一、可解释、可扩展的工业因果诊断多 Agent 框架"这一空白。它不是单一模型，而是一个完整的**系统架构**，整合了：

- **神经符号因果发现**：融合数据驱动的结构学习与专家定义的领域规则
- **标准化 Agent 协议**：MCP 用于工具调用、A2A 用于 Agent 间通信、LangGraph 用于工作流编排
- **人类在环**：操作员全程可审查、验证和调整 Agent 输出
- **实时就绪**：50-60s 端到端延迟，近线性扩展性（R²=0.97）

---

## 二、系统架构：四层框架

CausalPulse 采用四层垂直架构，从上到下依次为：

```
┌─────────────────────────────────────────────┐
│  User-Facing Layer（用户界面层）            │  ← 浏览器 UI，操作员交互入口
├─────────────────────────────────────────────┤
│  Agent Layer（Agent 层）                    │  ← Common Agents + Specialized Agents
├─────────────────────────────────────────────┤
│  Utility Layer（工具层）                    │  ← MCP 工具/服务/资源
├─────────────────────────────────────────────┤
│  Data Layer（数据层）                       │  ← 传感器日志、图像、事件元数据
└─────────────────────────────────────────────┘
         ↑           ↑           ↑
        MCP         A2A      LangGraph
```

### 各层职责

| 层级 | 核心职责 | 技术实现 |
|------|---------|---------|
| **User-Facing** | 操作员交互、结果审查、计划调整 | 浏览器 UI，LangGraph Workflow Engine 桥接 |
| **Agent** | 多 Agent 协调、任务分发、结果汇总 | FastAPI 微服务，Agent Card 注册，A2A 通信 |
| **Utility** | 工具/服务/资源的标准化暴露 | MCP 协议，Process Ontology、LLM、Knowledge Graph |
| **Data** | 传感器时序、图像、事件日志等多模态数据 | 时序/图像/文本异构输入 |

### 架构设计原则

**神经符号桥接**：每层都体现神经方法（数据学习、适应性）和符号方法（规则约束、可解释性）的融合，而非单一方法的堆砌。

**即插即用扩展**：新数据源、新 Agent、新工具可以在不重构整体工作流的情况下接入。这是通过标准化协议（MCP/A2A/LangGraph）的清晰接口实现的。

**端到端透明**：每个决策都可以从用户查询追溯到原始数据，经过每一层的明确边界。

---

## 三、Agent 体系详解

### 通用 Agent（Common Agents）

通用 Agent 是跨领域可复用的组件：

#### Client Process Agent（CPA）— 主编排器

CPA 是整个 Agent 层的中心枢纽，类比 LangGraph 中的"控制节点"：

```
用户查询 → CPA（输入规范化）→ 下游 Agent（MCP 会话管理）→ 结果后处理 → 状态更新
```

具体职责：
1. 将异构客户端输入规范化为下游工具可消费的规范载荷（canonical payloads）
2. 基于高层任务标签（preprocessing、anomaly、causal）将载荷分发给正确的工具
3. 管理异步 MCP 会话和执行路由
4. 对结果执行基于元数据规则的 后处理，必要时触发后续工具

**关键设计**：CPA 是 Stateful 的——它维护每个诊断会话的状态（已完成哪个阶段、积累了哪些中间结果），支持跳过已完成的步骤（如数据已完成预处理则不再重复处理）。

#### Preprocessing Agent — 确定性数据清洗

执行确定性数据清洗和规范化：
- 删除空行空列
- 标准化数据类型
- 插补缺失值
- 标签编码分类变量
- **查询 Background Info Agent** 获取变量级领域语义描述

关键：它不调用 LLM，是纯确定性管道，保证结果可重复。

#### Background Info Agent — 语义 lookup 服务

轻量级语义查询服务，HTTP-only 微服务优化低延迟响应：
- 输入：变量名列表
- 输出：人类可读的传感器语义描述（测量位置、物理含义、领域上下文）
- 作用：为 Preprocessing Agent 和 RCA Agent 提供将数字结果转换为领域感知解释的能力

这是典型的**知识注入**模式——领域知识不是从数据中学习出来的，而是通过结构化查询外部化暴露。

#### Recommender Agent — 规则驱动下一步建议

- 为操作员和自动化 Planner 提供上下文感知的下一步建议
- 规则驱动（非 LLM 策略）→ 响应可预测、推理延迟低
- 通过 MCP SSE 接口暴露，可被 CPA 和其他 A2A 调用方消费

### 专业 Agent（Specialized Agents）

#### Anomaly Detection Agent — 多策略异常检测

多策略管线，根据查询内容选择检测后端：
1. **跨模态融合模型**：时序 + 图像信号联合检测（来自 Shyalika et al. 2025d）
2. **确定性阈值规则**：基于领域特定测量限的规则
3. **隔离森林**：无监督表格特征异常检测

输出：分类标签（Normal / 异常类型）、异常分数、违规特征列表、**可追溯元数据**。检测到异常时，自动构建结构化载荷并通过 A2A 触发 RCA Agent。

#### Causal Discovery Agent — 因果结构发现

基于预处理后的数据，以 schema-aware、知识注入方式诱导候选因果结构：

- **算法选择策略**：
  - Gripper-sensor 数据集 → Peter-Clark（PC）算法
  - Process-variable 数据集 → Greedy Equivalence Search（GES）算法
  
- **神经符号融合**：结构学习算法通过 `causal-learn` 和 `pgmpy` 实现，同时被**领域规则约束**：
  - 控制参数（矩形）可以导致同阶段或后续阶段的观察参数（圆形）
  - 观察参数只能导致后续观察
  - 违反类型或时间顺序的边被明确禁止（dashed red arrows）

- 产出的有向图和边级统计量经领域规则过滤后，可由工厂专家进一步审查和修正

#### RCA Agent — 根因分析归因

执行因果归因，对异常观察进行根因定位：

- 输入：内存记录（复用预计算的 RCA 结果）、上传的数据集或文件路径
- 输出：**结构化的、排序的根因解释**，适合操作员解读
- 底层包装 **ProRCA 分析管线**（Dawoud & Talupula 2025）—— 领域感知的 SCM 构建器 + 基于路径的根因评分器
- 评分结合**结构度量 + 噪声度量**，平衡因果可信度与观测扰动强度

---

## 四、工作流编排：三阶段执行

```
Stage 1: Agent Card 注册          Stage 2: Agent 交互与数据流         Stage 3: 后处理链接
┌──────────────────────┐      ┌─────────────────────────────────┐   ┌──────────────────────┐
│ Agent Card Registry  │      │  Planner → Executor → Replanner  │   │ Recommender Agent    │
│  (中央服务器目录)    │      │        ↑            ↓            │   │  (规则驱动下一步建议) │
└──────────────────────┘      │       CPA ───→ MCP ───→ Agents  │   └──────────────────────┘
                               └─────────────────────────────────┘
```

### LangGraph 工作流引擎

CausalPulse 使用 **LangGraph** 作为工作流编排引擎，包含三个核心节点：

1. **Planner 节点**：接收用户查询 + 当前工作流状态 → 调用 LLM（llama-3.1-8b-instant）确定解决查询所需的最小 Agent 序列（动态任务分解）。已完成阶段被跳过（状态记忆）。

2. **Executor 节点**：执行 Planner 生成的步骤序列。每次向 CPA 发送结构化请求，CPA 通过 MCP 协议 + SSE 连接将请求分发到正确的远程 Agent，结果合并到共享系统状态后进入下一阶段。

3. **Replanner 节点**：每次执行后评估是否需要修改计划。如果当前计划已失效（数据变化、新发现），触发重新规划。

**关键机制——异步 MCP 会话管理**：CPA 维护每个会话的异步 MCP 上下文，支持在多个 Agent 之间并行发起工具调用而不阻塞工作流。

---

## 五、评估结果与关键指标

| 指标 | Future Factories（公开）| Planar Sensor Element（Bosch 专有）|
|------|----------------------|--------------------------------|
| **总体成功率** | 98.0% | 98.73% |
| **规划与工具使用** | 98.75% | — |
| **自反思** | 97.3% | — |
| **协作** | 99.2% | — |
| **端到端延迟** | 50-60s / 诊断工作流 | 同左 |
| **扩展性** | R²=0.97（近线性）| 同左 |

### 与现有工业副驾驶的对比

CausalPulse 的差异化优势：
- **模块化**：各 Agent 独立部署，通过标准化协议通信
- **可扩展性**：近线性扩展，新 Agent/工具即插即用
- **部署成熟度**：已在真实 Bosch 产线运行
- **可解释性**：每步输出都携带领域语义和因果路径

---

## 六、对 Agent 工程的核心启示

### 1. 神经符号架构在工业场景的真实价值

CausalPulse 证明了"神经 + 符号"不是学术概念：在工业诊断中，**数据驱动的结构学习**（神经）提供发现能力，**专家定义的领域规则**（符号）提供约束和安全保障。两者结合才能做到"发现我不知道的因果关系，同时不违反我知道的物理规律"。

### 2. MCP + A2A + LangGraph 的协议栈分层

CausalPulse 的协议栈选择揭示了当前 Agent 生态的务实路线：
- **MCP**：工具/服务/资源的标准化暴露接口（Utility Layer）
- **A2A**：Agent 之间的点对点通信和协作（Agent Layer 内部）
- **LangGraph**：复杂多步骤工作流的 Stateful 编排

这不是一个框架的选择，而是**按需分层**——每个协议在最适合自己的层级发挥作用。

### 3. 人类在环不是妥协，而是架构设计原则

CausalPulse 明确将人类操作员定位为"质量门卫"而非最终决策者：
- Recommender Agent 提供下一步建议（规则驱动，可预测）
- RCA Agent 输出排序的根因（可由专家验证和调整）
- 任何 Agent 的输出都可以被专家覆盖

这与"完全自主 Agent"的路线形成鲜明对比——在安全关键的工业场景，**人类的领域知识是不可替代的输入**，而不是最后才出现的否决者。

### 4. FastAPI 微服务作为 Agent 载体

所有 Agent 都实现为 FastAPI 微服务，这意味着：
- 每个 Agent 可以独立部署、独立扩展
- Agent 间通过 HTTP/A2A 通信，松耦合
- 可以复用现有的微服务运维体系（K8s、服务发现、监控）

### 5. 动态任务分解的实践

LangGraph Planner 使用 LLM 做动态任务分解，但**任务执行是确定性的**（Executor 严格按计划执行）。这避免了 ReAct 模式中每步都调用 LLM 的高延迟问题——只有"需要判断下一步做什么"时才调用 LLM，具体执行由专用 Agent 负责。

---

## 七、局限性与未来方向

论文明确指出的局限性：

1. **LLM 推理延迟**：规划节点调用 llama-3.1-8b-instant，在高并发场景下可能成为瓶颈
2. **领域规则获取瓶颈**：领域规则依赖专家手动定义，规则库的初始构建成本高
3. **跨工厂迁移**：因果结构高度依赖特定产线的工艺知识，迁移到新产线需要重新定义领域规则
4. **多模态数据融合**：当前主要处理时序和图像，文本型日志（维修记录、操作员报告）的融合尚不充分
5. **长程因果链**：当根因和最终异常之间存在多跳延迟时，路径评分准确性下降
6. **对抗鲁棒性**：传感器数据被恶意篡改时的检测和防御机制尚未覆盖
7. **实时性边界**：50-60s 延迟适合分钟级诊断，对秒级异常检测场景（如高速旋转设备）仍有差距

---

## 八、与仓库现有内容的互补关系

| 仓库已有文章 | CausalPulse 的补充角度 |
|------------|----------------------|
| `agent-q-mix-rl-topology-2604-00344.md` | RL 拓扑感知 vs. 因果推理驱动；两者都是多 Agent 协作的进阶方向 |
| `multi-agent-swarm-intelligence.md` | 群体智能 vs. 工业确定性场景的精确 Agent 协作 |
| `vacp-visual-analytics-context-protocol-2603-23807.md` | 上下文协议 vs. 因果推理框架 |
| `semantic-router-dsl-2603-27299.md` | 语义路由 vs. 因果路径评分——都可以作为 Agent 编排的决策引擎 |
| `how-ai-agents-used-177k-mcp-tools.md` | MCP 工具使用规模研究 vs. CausalPulse 中 MCP 在垂直领域的深度应用 |

CausalPulse 属于 **Stage 9（Multi-Agent）+ Stage 7（Orchestration）** 的深度案例，填补了仓库中"工业级多 Agent 系统从设计到部署完整闭环"的真实案例空白。

---

## 参考文献

- Shyalika, C., Jaimini, U., Henson, C., & Sheth, A. (2026). *CausalPulse: An Industrial-Grade Neurosymbolic Multi-Agent Copilot for Causal Diagnostics in Smart Manufacturing*. arXiv:2603.29755. AAAI-MAKE 2026.
- Dawoud, A., & Talupula, M. (2025). ProRCA analysis pipeline. (Referenced in CausalPulse RCA Agent)
- Anthropic (2024). Model Context Protocol (MCP).
- Google A2A (2025). Agent-to-Agent Communication Protocol.
- LangChain AI (2024). LangGraph: Stateful Multi-Agent Orchestration.
