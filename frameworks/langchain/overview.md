# LangChain 框架概览

> *官方不写的那一面——来自一线从业者的声音*

## 框架定位

LangChain 是目前最成熟的 **LLM 应用开发框架**，提供从原型到生产的完整工具链。其核心优势在于丰富的组件库（Models、Prompts、Indexes、Chains、Agents、Memory）和对多种 LLM provider 的统一抽象。

## 核心模块

| 模块 | 说明 |
|------|------|
| **Models** | 统一接口对接 50+ LLM（OpenAI、Anthropic、Azure、HuggingFace 等）|
| **Prompts** | Prompt 模板管理、输出解析、示例选择 |
| **Indexes** | 文档加载、文本分割、向量检索（与所有主流向量库集成）|
| **Chains** | 可组合的任务序列（LLMChain、ConversationalChain 等）|
| **Agents** | ReAct、Self-Ask、Plan-and-Execute 等 Agent 执行范式 |
| **Memory** | 对话历史、Buffer、KG 等记忆方案 |
| **Callbacks** | 灵活的日志、追踪、流式事件系统 |

## LangGraph：LangChain 的状态机扩展

LangGraph 是 LangChain 团队构建的**有状态、多角色工作流引擎**，专为大模型应用中的循环计算设计：

- **优势**：支持循环（while/if）、多 Agent 协作、持久化执行状态、人机交接
- **定位**：对标 LangChain Chains，但更适合复杂 Agent 工作流
- **生态**：与 LangSmith 深度集成，支持生产级 Tracing 和调试

> 📖 详见：[frameworks/langgraph/overview.md](./langgraph/overview.md)

## LangSmith：观测与评测平台

LangSmith 是 LangChain 的**全生命周期观测平台**，2026 年 3 月将 Agent Builder 功能升级为 **LangSmith Fleet**（企业级无代码 Agent 构建与管理）。

| 功能 | 说明 |
|------|------|
| **Tracing** | 端到端 Agent 执行链路追踪，支持 LangGraph |
| **Evaluation** | 数据集管理 + 自动评测（支持 GPT-4o、Claude 作为 Judge）|
| **Datasets** | 私有数据集管理，支持 RAG、Agent 评测 |
| **Fleet** | 企业 Agent 构建、权限管理、多 Agent 协作治理 |

## 快速开始

```python
# LangChain 基本用法
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("human", "{question}")
])
chain = prompt | llm
result = chain.invoke({"role": "助手", "question": "你好"})
```

```python
# LangGraph Agent 示例
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4o"),
    tools=[search_tool, calculator],
    state_modifier="你是一个有帮助的助手"
)
```

## 选型建议

| 场景 | 推荐方案 |
|------|---------|
| 快速原型 / RAG | LangChain 基本用法（轻量上手）|
| 复杂 Agent 工作流 | LangGraph（状态机 + 循环）|
| 生产观测 | LangSmith（Tracing + Evals）|
| 企业多 Agent 管理 | LangSmith Fleet（权限 + 协作）|

## 资源链接

- [LangChain 官方文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangSmith 文档](https://docs.langchain.com/langsmith/)
- [LangChain Blog](https://blog.langchain.com/)
- [GitHub](https://github.com/langchain-ai/langchain)

---

*本文件由 AgentKeeper 自动维护*
