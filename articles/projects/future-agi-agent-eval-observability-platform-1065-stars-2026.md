# future-agi/future-agi：开源 Agent 评估与观测平台

> **核心命题**：future-agi 是一个开源的端到端 LLM/AI Agent 评估与观测平台，通过 Tracing、Evals、Simulations、Datasets、Gateway 和 Guardrails 六大模块，为 Agent 系统提供完整的可观测性和质量保障基础设施。

---

## 背景：为什么 Agent 需要专门的评估基础设施

传统的 LLM 评估主要关注单次输出的质量（Perplexity、BLEU、ROUGE 等）。但 Agent 系统的评估要复杂得多：

- **执行轨迹**：Agent 的行为是跨多步骤的，输出只是最终结果，过程同样需要评估
- **工具使用有效性**：Agent 是否选择了正确的工具？调用参数是否合理？
- **容错与恢复**：Agent 遇到错误时如何处理？是否能从失败中恢复？
- **多 Agent 协作**：多个 Agent 之间的交互是否有效？是否有死锁或重复劳动？
- **长期运行稳定性**：Agent 运行 1 小时、1 天、1 周后行为是否一致？

这些都需要专门的评估框架，而非传统的单次输出评估方法。

---

## 核心功能

### Tracing（分布式追踪）

future-agi 提供完整的分布式追踪能力，记录 Agent 执行过程中的每个关键事件：

- LLM 调用（Prompt、Response、Token 使用）
- 工具调用（函数名、参数、结果）
- Agent 间通信（如果是 Multi-Agent 系统）
- 状态变化（Memory 更新、Context 变化）

追踪数据是后续评估和调试的基础。

### Evals（评估）

支持多种评估模式：

- **离线评估**：基于历史轨迹数据集，批量运行评估
- **在线评估**：在 Agent 运行时实时评估，及时发现质量问题
- **Red-Teaming**：模拟对抗性输入，测试 Agent 的鲁棒性

评估结果会反馈到训练流程，形成数据驱动的优化闭环。

### Simulations（仿真）

在真实环境之外提供仿真测试能力：

- 模拟用户行为
- 模拟工具返回（网络不可用、API 超时等边界情况）
- 模拟多 Agent 交互场景

仿真可以在部署前发现大量问题，降低生产环境故障率。

### Datasets（数据集管理）

提供 Agent 评估数据集的管理能力：

- 数据集版本控制
- 自动化数据增强
- 与主流评测框架的格式兼容

### Gateway（网关）

提供 Agent 请求的路由和负载均衡能力，支持多模型的后端配置。

### Guardrails（护栏）

在 Agent 执行过程中插入安全检查，防止：

- 有害内容生成
- 敏感信息泄露
- 超出范围的工具调用

---

## 技术特点

**Stars**: 1,065（截至 2026-06-01）
**License**: Apache 2.0
**自托管**: 完全自托管，数据不离开你的基础设施

技术栈围绕 Python生态构建，支持主流 LLM Provider（OpenAI、Anthropic、Local Models），可与 LangSmith、Langfuse 等现有观测工具集成。

---

## 与 Article 的闭环

**Article**: [LangChain Agent Streams：从 Token 流到事件流的架构演进](langchain-token-streams-to-agent-streams-2026.md)

**闭环逻辑**：

- Article 描述了 Agent Streams 如何让多 Agent 执行过程可观测（事件驱动、命名空间、类型化事件）
- future-agi 的 Tracing 模块正是消费这些可观测性事件的最佳拍档——接收结构化事件流，进行存储、索引、评估

两者形成「执行层可观测性 → 数据采集 → 评估改进」的完整闭环，是 Agent 工程化的重要基础设施组合。

---

## 来源

- GitHub: [future-agi/future-agi](https://github.com/future-agi/future-agi)