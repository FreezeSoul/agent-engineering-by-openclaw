# LangGraph

> DAG-based 状态机模型，适合构建复杂工作流的 Agent 框架。

---

## 核心概念

LangGraph 是 LangChain 生态中的核心框架，采用**图（Graph）**的方式来组织 Agent 的工作流。

### 三大核心

1. **State（状态）**
   - 整个工作流共享的状态对象
   - 定义为一个 Pydantic 模型或 TypedDict
   - 每个节点执行后可以修改状态

2. **Nodes（节点）**
   - Python 函数，接收当前状态，返回更新后的状态
   - 可以是 LLM 调用、Tool 执行、条件判断等任意逻辑

3. **Edges（边）**
   - 定义节点之间的流转关系
   - **条件边**：根据状态动态决定下一个节点
   - **普通边**：固定的下一个节点

###Checkpointing

LangGraph 内置 Checkpointing 支持，允许多次中断和恢复，适合需要用户确认的长时任务。

---

## 适用场景

- 需要状态持久化的对话系统
- 多步骤自动化流程
- RAG + Agent 融合
- 需要回退/重试能力的工作流

---

## 学习资源

- [官方文档](https://langchain-ai.github.io/langgraph/)
- [LangChain Blog](https://blog.langchain.com/)

---

## 优势

✅ 状态管理精细，适合复杂逻辑
✅ 内置 Checkpointing
✅ 与 LangChain 生态无缝集成
✅ 支持循环（Loop）

## 劣势

⚠️ 学习曲线中等，需要理解图模型
⚠️ 多 Agent 协作需要自行实现
⚠️ 文档有时不够及时

---

*最后更新：2026-03-21*
