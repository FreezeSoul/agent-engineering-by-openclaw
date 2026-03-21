# 框架深度解析

本目录收录主流 Agent 开发框架的深度解析。

---

## 目录

- [LangGraph](langgraph/) — 状态机模式，适合复杂工作流
- [CrewAI](crewai/) — 角色扮演式多Agent协作
- [AutoGen](autogen/) — Microsoft多模型协作

---

## 选型决策树

```
你需要构建什么类型的Agent？
│
├─ 简单对话/问答
│   └─ 直接用 LangChain / LlamaIndex 即可
│
├─ 复杂工作流（多步骤、条件分支）
│   └─ 推荐 LangGraph
│
├─ 多角色协作（研究员+审核员+执行者）
│   └─ 推荐 CrewAI
│
└─ 企业级多模型协作
    └─ 推荐 AutoGen / Semantic Kernel
```

---

## 框架对比

| 框架 | 模型支持 | 多Agent | 状态管理 | 学习曲线 |
|------|---------|---------|---------|---------|
| LangGraph | 任意 | 需自行实现 | 内置 | 中等 |
| CrewAI | 任意 | 内置 | 需自行实现 | 低 |
| AutoGen | 任意 | 内置 | 需自行实现 | 中等 |
| Semantic Kernel | OpenAI系为主 | 有限 | 有限 | 低 |

---

*持续更新中*
