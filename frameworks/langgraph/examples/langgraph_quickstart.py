# LangGraph 快速入门示例

> 一个简单的 ReAct 风格 Agent，演示 LangGraph 的状态机核心用法

---

## 环境准备

```bash
pip install langgraph langchain-openai
```

---

## 完整示例：一个工具调用 Agent

```python
from typing import TypedDict, Annotated
import operator
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool

# ========== 1. 定义工具 ==========

@tool
def search_database(query: str) -> str:
    """搜索公司数据库"""
    # 模拟数据库查询
    results = {
        "员工": "公司共有 128 名员工",
        "收入": "本季度收入 3000 万",
        "产品": "主打产品：AIAgent Platform"
    }
    return results.get(query, f"没有找到关于 '{query}' 的信息")

@tool
def send_email(to: str, content: str) -> str:
    """发送邮件"""
    return f"邮件已发送给 {to}"

tools = [search_database, send_email]

# ========== 2. 定义状态 ==========

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # 对话历史
    next_action: str                        # 下一步行动

# ========== 3. 定义节点函数 ==========

def agent_node(state: AgentState):
    """Agent 决策节点"""
    messages = state["messages"]
    last_message = messages[-1]["content"]
    
    llm = ChatOpenAI(model="gpt-4o")
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke([
        {"role": "system", "content": "你是一个智能助手，可以调用工具来回答问题。"},
        {"role": "user", "content": last_message}
    ])
    
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """判断是否继续调用工具"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# ========== 4. 构建图 ==========

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", lambda state: state)  # 简化：实际应调用工具

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# ========== 5. 运行 ==========

if __name__ == "__main__":
    result = app.invoke({
        "messages": [{"role": "user", "content": "我们公司有多少员工？"}],
        "next_action": ""
    })
    
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")
```

---

## 核心概念对应

| 概念 | 代码位置 |
|------|---------|
| **State** | `AgentState` TypedDict |
| **Nodes** | `workflow.add_node()` |
| **Edges** | `workflow.set_entry_point()` / `workflow.add_edge()` |
| **Conditional Edges** | `workflow.add_conditional_edges()` |
| **Checkpoint** | `app = workflow.compile()` 内置 |

---

## 扩展：加入 Checkpointing

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# 持久化状态（服务重启后可恢复）
checkpointer = SqliteSaver.from_conn_string("./checkpoints.db")

app = workflow.compile(checkpointer=checkpointer)
```

---

## 扩展：流式输出

```python
for event in app.stream({"messages": [{"role": "user", "content": "你好"}]}):
    for key, value in event.items():
        print(f"Node: {key}")
        print(f"Value: {value}")
```

---

## 学习路径建议

1. 先跑通上面的快速入门
2. 添加自定义工具
3. 学习 `add_conditional_edges` 实现循环
4. 接入 Checkpointing 实现状态持久化
5. 接入 LangSmith 进行可观测性调试

---

*代码基于 LangGraph 0.1.x 版本*
