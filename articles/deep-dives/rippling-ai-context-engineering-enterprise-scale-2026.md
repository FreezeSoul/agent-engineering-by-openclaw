# Rippling AI：百万级用户的上下文工程实践

> "If you put the whole thing in context, even a chunk of it, there are so many conflicting entities that it just won't fit in the context window in the timeframe Rippling's customers expect."
> — Sahin Olut, Principal Engineer, Rippling AI

## 背景：企业级 Agent 面对的 Context 挑战

Rippling 是一个 workforce management 平台，管理从入职、福利、设备配置到支出管理的全套流程。其数据模型横跨 HR、IT、payroll、finance 和全球运营：数千张表、数十万个字段，跨领域的同名实体（如 "balance" 可以指健康储蓄账户、信用卡、承包商付款账户或休假政策）。

当 Rippling AI 在全球数百万用户中上线时，核心挑战不是"如何构建 Agent"，而是**如何在巨大的语义混沌中让 Agent 有效推理**。

---

## 核心架构：Supervisor + 专业化 Deep Agents

Rippling AI 的架构是典型的 Supervisor 模式：

```
用户查询 → Supervisor Agent（主推理循环）
           ├─ Read Agents（跨结构化数据查询）
           ├─ RAG Agents（从非结构化文档检索）
           └─ Action Agents（执行写操作）
```

Supervisor Agent 运行主要推理循环，分析输入查询并决定调用哪个专业化 Agent（或组合）。

**这个架构本身并不独特**——多 Agent 协作是社区广泛讨论的模式。Rippling 的价值在于：**在企业级复杂语义环境下的具体工程实现**。

---

## 工程模式 1：动态 Skill 注入（Dynamic Skill Injection）

Context 压缩是 Enterprise Agent 的核心技术挑战。Rippling 的解法：

1. **语义层识别**：用户提问时，先用 Rippling 自己的语义层识别相关领域（payroll、devices、ATS、spend 等）
2. **领域 Scope 注入**：只注入该领域的 skill，而非全量 schema
3. **激进剪枝**：Re-rankers 将 context size 压缩 **100 到 500 倍**

关键洞察：

> "If you put the whole thing in context, even a chunk of it, there are so many conflicting entities that it just won't fit in the context window in the timeframe Rippling's customers expect."
> — [Rippling AI Engineering](https://www.langchain.com/blog/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith)

这与传统的 "RAG everything" 思路不同：**不是把更多 context 放进去，而是先识别领域，再精确注入**。

---

## 工程模式 2：代码执行隔离数据格式化（Code Execution for Write Operations）

Rippling 的 Action Agents 不直接让 LLM 操作数据，而是：

1. LLM 推理"要做什么"（what to do）
2. 沙盒化代码执行将输入（如客户上传的 CSV）规范化为内部工具期望的格式
3. 执行写操作

**"做什么"与"如何格式化"分离**，使数据规范化可靠且可审计。

---

## 工程模式 3：REPL 变量钉住（Variable Pinning via REPL）

团队观察到一个尖锐问题：**LLM 在复述长字母数字 ID 时会幻觉**。

解决方案：REPL 在 Agent 步骤之间维护运行时变量存储。Agent 引用命名变量，而非在工具调用之间传递原始实体字符串。

这是**状态管理在 Agent 推理中的具体应用**——不是记忆系统，而是运行时引用稳定性。

---

## 自愈评估循环（Self-Healing Eval Loop）

Rippling 团队构建了一个半自动化循环来捕获回归并关闭它们：

```
生产轨迹失败 → 拉取到 LangSmith
             → Agent 分析失败原因
             → 提出修复方案
             → 重新运行 evals 确认改进
             → 迭代直到回归关闭
             → 人类审核并合并 PR
```

> "We pull failing traces, have an agent understand what's going on, propose a few solutions, run the evals again to see if it improves, and loop until it's complete. LangSmith makes this possible because there's an API at every point in the system."
> — [Rippling Engineering](https://www.langchain.com/blog/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith)

---

## 分层评估管道（Eval Pipeline）

Rippling 运行分层评估系统：

| 层级 | 类型 | 说明 |
|------|------|------|
| Offline evals | 本地 | 预录 mock 和 fixture，commit 时运行，无外部依赖 |
| Post-merge integration evals | 在线 | 300-400 查询针对完整 Rippling sandbox |
| Deploy-blocking evals | 在线 | ~10 个关键场景 gate 每个部署 |
| Continuous evals | 在线 | 每日多次针对生产数据运行 |

---

## 核心启示

### 1. 领域识别先于 Context 注入

不是 RAG everything，而是**先识别领域，再精确获取该领域的 context**。这需要你有语义层或分类系统。

### 2. 状态稳定性是可靠执行的基础

LLM 幻觉长 ID 是一个具体工程问题。REPL 变量钉住是一个具体的解法。**运行时状态管理**是 Agent 可靠性的关键。

### 3. 自愈循环需要可观测性基础设施

Self-healing eval loop 的前提是 LangSmith 这样的**full-stack 可观测性**：每个点都有 API，才能 pull 轨迹、分析失败、re-run evals。

### 4. 评估是持续过程，而非一次性验证

Rippling 的 4 层评估管道（offline → post-merge → deploy-blocking → continuous）体现了**评估作为持续质量基础设施**的理念。

---

## 与其他 Enterprise Agent 实践的对比

| 维度 | Rippling AI | 传统 Enterprise AI |
|------|-------------|-------------------|
| Context 管理 | 领域识别 + 精确注入 | 全量 schema RAG |
| 写操作 | 代码执行隔离格式化 | LLM 直接操作 |
| 状态管理 | REPL 变量钉住 | 无状态每次调用 |
| 评估 | 4 层持续管道 | 一次性测试 |
| 可观测性 | 全链路 API | 有限监控 |

---

## 结论

Rippling AI 的工程实践揭示了 **Enterprise Agent 的核心技术挑战不是 Agent 本身，而是 Context 管理**：

- 领域识别先于 Context 注入
- 状态稳定性决定执行可靠性
- 评估是持续基础设施，而非一次性验证

这些教训来自于在数百万用户规模下的真实生产环境验证，对任何构建 Enterprise Agent 系统的团队都有直接的参考价值。

---

**引用来源**：

- [How Rippling built production AI in 6 months with Deep Agents and LangSmith](https://www.langchain.com/blog/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith) — LangChain Blog
