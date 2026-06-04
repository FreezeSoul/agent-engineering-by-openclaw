# Anthropic 建筑决策框架：Single Agent → Multi-Agent → Evaluator-Optimizer 的系统性选型方法论

> **核心观点**：Anthropic 的《Building Effective AI Agents》提供了建筑模式选择的第一手系统化框架——不是告诉开发者「用什么框架」，而是帮助决策「在什么场景下选择什么架构」。这份框架的核心价值在于：从问题复杂度出发匹配架构复杂度，而非从框架能力出发反向设计系统。

## 一、问题的本质：架构错配是 Agent 落地失败的首要原因

很多团队在落地 Agent 系统时，第一个决策错误是从框架能力出发——选了 LangGraph 或 AutoGen，然后再想「我的业务场景能用它做什么」。这种思路的反面，是 Anthropic 提出的方法论：**从问题复杂度出发，判断需要哪种架构模式**。

Anthropic 的核心判断是：大多数企业从 Single-Purpose Agent 开始是正确起点，但当问题复杂度超出单 Agent 的能力边界时，团队往往缺乏系统性的决策依据，只能靠直觉或者框架文档的引导盲目升级到「多 Agent」。

这份 PDF 的价值，恰恰在于填补了这个决策依据的空白。

---

## 二、三层架构模式：从简单到复杂，问题是匹配的

### 2.1 Single-Agent Systems：适合「路径不确定」的开放问题

Single Agent 的工作循环是：感知环境 → 决策下一步 → 执行行动 → 观察结果 → 调整策略，循环直到任务完成或触发停止条件（如「暂停等待人工审核」）。

**适合场景**：
- 开放性研究问题，路径无法预判
- 客户支持中需要多步骤工具调用的场景
- 文档处理和代码审查

**不适合场景**：
- 需要 100% 首次准确率的问题
- 复杂到单 Agent 无法同时追踪多个独立方向的任务

Anthropic 的决策树中有一个关键判断：**「Adding specialized skills to your single agent might achieve your accuracy requirements more efficiently」**——在升级到多 Agent 之前，先考虑是否可以通过增加 Skill 来解决。

### 2.2 Multi-Agent Systems：当单 Agent 遇到三种能力边界时

Multi-Agent 协调多个专业 Agent 共同完成单 Agent 无法胜任的任务。Anthropic 明确指出了三种必须升级到多 Agent 的场景：

1. **开放性问题，路径无法预判且需要灵活转向**——当问题本身不确定需要多少步骤时
2. **需要专业领域知识，单一 Agent 面对多干扰领域时会快速下降**——研究显示单 Agent 在有两个以上干扰领域时性能急剧下降
3. **需要并行追踪多个独立方向**——内部测试显示复杂任务下多 Agent 系统比单 Agent 优 90.2%

Multi-Agent 有两种协调架构：

#### 层级式（Hierarchical / Supervisory）

中心 Supervisor Agent 将任务委托给专业子 Agent，类似于人类组织中的管理者-专家结构。Supervisor 只与团队领导 Agent 交互，不感知更深层的委托。

**典型案例**：营销活动系统
- Marketing Director Agent（Supervisor）协调：市场研究 Agent、创意设计 Agent、文案 Agent、媒体策划 Agent
- 各专业 Agent 将结果汇报给 Director，由其做最终整合

这种模式的核心经济学判断是：虽然多 Agent 系统消耗更多 Token，但**「对于需要专业知识或超出单 Agent 上下文限制的高价值复杂任务，性能收益证明成本合理」**。

#### 协作式（Collaborative）

多个专业 Agent 通过点对点通信直接协调，自主协商角色，动态协作解决问题。与层级式不同，协作式强调**「协调从 Agent 交互中涌现，而非由中心权威施加」**。

**典型案例**：竞争情报采集
- Pricing、Product、Marketing、Financial、Social Media、Strategic Intelligence 多个 Agent 实时共享发现
- 各 Agent 交叉验证发现，相互.alert 相关发现
- 最终由 Report Agent 整合成综合竞争态势分析

协作式最大的工程挑战是**通信复杂度与涌现行为不可预测性**：
- Agent 间频繁通信导致计算成本增加
- 多 Agent 系统的涌现行为无法通过特定编程精确控制
- 小变化可能不可预测地影响 Agent 行为

### 2.3 Agentic Workflows：适合「路径可预定义」的流程型任务

Agentic Workflows 与前述动态 Agent 的核心区别在于：**工作流是预定义和静态的**。这是结构化编排，用于多步骤过程。

三种子模式：

#### Sequential Workflows（顺序式）

预设控制流，定义执行路径，适合可预测的重复性流程，如文档审批链或合规检查。核心优势是**运营可预测性**——可以绘制完整流程图、估算执行成本、通过检查特定工作流阶段来调试问题。

**适合**：多阶段流程且步骤间有清晰线性依赖、数据处理管道（每阶段为下一阶段添加特定价值）、需要累积上下文按特定顺序执行的任务。

#### Parallel Workflows（并行式）

将独立任务同时分配给多个 Agent，结果并发合并。适合需要不同视角或专业知识的场景，通过并发处理实现显著加速。

**典型案例**：金融风险评估
- Data Aggregation Agent 收集数据后，Credit Risk Agent、Market Risk Agent、Operational Risk Agent、Regulatory Compliance Agent 并行分析
- Risk Aggregation & Decision Engine 汇总所有并行评估，输出综合风险档案

#### Evaluator-Optimizer（评估器-优化器）

这是整个框架中最具工程意义的模式：**两个 AI 系统形成迭代循环，一个生成内容，另一个评估并提供反馈，重复直到达到质量标准**。这类似于作家-编辑协作，但反馈是结构化的、可操作的。

**适合场景**：
- 需要细微差别的内容创作（如文学翻译）
- 有安全要求的代码生成
- 需要多步推理和验证的研究任务

**不适合**：
- 首次质量已满足要求
- 评估标准主观或不明确
- 时间和成本约束超过质量改进收益

Anthropic 给出了典型迭代次数：**通常运行 2-4 个循环**，文档质量显著改善。

---

## 三、决策框架：Start Simple，Scale Intelligently

Anthropic 的决策流程总结为三个核心原则：

### 原则一：Start Simple，Scale Intelligently

> 「We suggest teams begin with single-purpose agents that do one thing well, then gradually develop them into more sophisticated systems as your requirements evolve. Simple systems are cheaper to run, easier to debug, and give you clear metrics that actually tie to business outcomes.」

**从单用途 Agent 开始，做一件事做到优秀，再根据需求演进到更复杂的系统。**

### 原则二：Choose the Right Model for the Job

模型选择是三个因素的平衡：**能力、速度、成本**。不是选最强，而是选最合适：

- 复杂金融分析或多 Agent 编码框架 → 最强模型
- 处理大量简单客户支持工单 → 轻量快速模型，成本低得多

> 「Running a simple task through a premium model isn't just wasteful, it's also slower and more expensive at scale.」

### 原则三：Practice Modular Design

设计模块化，因为：
- 这个领域演进很快，新能力和功能会定期出现
- 模块化让 Agent 可以独立演进，不需要整体重新设计基础设施
- 新工具可以轻松集成到模块化 Agent 框架中

Anthropic 特别推荐组合模式（Composition Pattern）：
- Prompts 集中在配置文件或库中定义
- Tools 是离散可复用模块
- Agents 按需定义，只利用任务所需的工具

---

## 四、Skills：扩展单 Agent 能力的模块化单元

Anthropic 引入了 **Agent Skills** 作为模块化能力包，让 Agent 在基础能力之外获得专业领域知识、工作流和工具集成。Skills 的关键特性：

- **Composable**：合规 Skill 可以调用文档分析 Skill，后者又使用专门的提取 Skill，形成层级能力结构
- **Independent Updates**：可以独立更新 Skill 而不需要重写 Agent 逻辑
- **Cross-Agent Sharing**：Skills 可以跨多个 Agent 共享
- **Single/Multi-Agent 双兼容**：单 Agent 系统中 Skills 扩展基线能力；多 Agent 系统中不同 Agent 配置不同 Skills

**适合 Skills 的场景**：
- 领域专业知识的财务分析、法律审查、科学研究
- 组织已成熟的标准化工作流
- 专业化工具集成（数据库、API、内部系统）

---

## 五、真实案例的量化启示

这份 PDF 提供了多个企业的量化数据，说明架构模式落地的实际效果：

| 企业 | 场景 | Agent 架构 | 核心指标 |
|------|------|-----------|---------|
| **Coinbase** | 加密货币客户支持 | Single Agent（Claude-powered）| 35-50个内部AI应用，千条消息/小时，99.99%可用性 |
| **Intercom Fin** | 客服 AI Agent | Single Agent | 86%解决率，45+语言支持，响应时间从30分钟降至秒级 |
| **Tines** | 安全运营工作流 | Single Agent（动态工作流逻辑）| 100x 时间价值提升 |
| **Advolve** | 多平台广告自动化 | Multi-Agent | 90%运营时间减少，15% ROAS 提升 |
| **Inscribe** | AI 欺诈检测 | Multi-Agent | 审查时间从30分钟降至90秒（20x），输出增加70x |
| **Thomson Reuters CoCounsel** | 法律知识平台 | Single Agent | 专业人员反馈「轻松将时间缩短一半，可能更多」 |

---

## 六、与轻量级实现的互补关系

Anthropic 的决策框架解决的是**「选择什么架构模式」**的问题。而具体实现时，框架的复杂度选择是个重要决策点。

这正是 smolagents 的价值所在：其核心设计哲学——「agents that think in code，核心逻辑约 1000 行代码」——与这份决策框架形成完美互补：

- **决策框架**告诉你：这个问题需要 Multi-Agent Parallel + Evaluator-Optimizer 模式
- **smolagents** 提供：用最小代码量（~1000 行）实现这个组合模式的轻量级路径

smolagents 的设计验证了一个关键论断：**「Writing actions as code snippets is demonstrated to work better than the current industry practice of letting the LLM output a dictionary of the tools it wants to call: uses 30% fewer steps」**。这意味着用更少的 Agent 步骤完成任务，直接降低Token消耗和协调复杂度。

Anthropic 的框架是「建筑师的设计手册」，smolagents 是「用最小工具箱实现设计的工匠技艺」。两者共同指向一个方向：**Agent 工程正在从「用复杂框架实现一切」向「根据问题复杂度精确匹配架构实现」的理性工程阶段演进。**

---

## 七、核心判断

Anthropic 这份文档的核心贡献，不是提供一个新框架，而是一套**建筑决策框架**。其底层逻辑是：

1. **问题复杂度 → 架构复杂度**，不是框架能力 → 业务场景
2. **单 Agent 是大多数企业场景的正确起点**，先做好一件事，再逐步演进
3. **多 Agent 的边界是清晰的**：开放性路径、专业知识需求、并行独立方向
4. **Workflow 是预定义流程与动态 Agent 的分界线**——当路径可预定义时，Workflow 更高效
5. **模块化设计是应对快速演进的唯一出路**——你的架构要能「随能力增长，而不是被能力增长摧毁」

> 原文一句话总结：*「Simple systems are cheaper to run (fewer tokens, less compute), easier to debug when things go wrong, and give you clear metrics that actually tie to business outcomes.」*

**建筑决策比框架选择更重要**。这是这份 Anthropic 一手资料给我们的核心启示。

---

**引用来源**：
- Anthropic, *Building Effective AI Agents: Architecture Patterns and Implementation Frameworks*, https://resources.anthropic.com/building-effective-ai-agents