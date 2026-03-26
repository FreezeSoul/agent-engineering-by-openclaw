# 框架专区

> 每个框架独立子目录，统一使用模板。

---

## 目录

| 框架 | 定位 | overview | examples | changelog |
|------|------|----------|----------|-----------|
| [LangGraph](langgraph/) | 状态机模式，适合复杂工作流 | ✅ | ✅ | ✅ |
| [CrewAI](crewai/) | 角色扮演式多Agent协作 | ✅ | ✅ | ✅ |
| [AutoGen](autogen/) | Microsoft多模型协作 | ✅ | ✅ | ✅ |
| [Microsoft Agent Framework](microsoft-agent-framework/) | Semantic Kernel + AutoGen 合并，.NET 企业级 | ✅ | ✅ | ✅ |
| [DefenseClaw](defenseclaw/) | Cisco 开源 Agent 安全治理，五工具扫描引擎 | ✅ | — | ✅ |
| [_template/](_template/) | 新增框架时复制的模板 | ✅ | — | ✅ |

---

## 如何添加新框架

1. 复制 `_template/` 目录到新框架目录
2. 重命名为框架名
3. 填充 `overview.md` 内容

---

## 框架对比

| 框架 | 模型支持 | 多Agent | 状态管理 | Checkpoint | 学习曲线 |
|------|---------|---------|---------|-----------|---------|
| LangGraph | 任意 | 需自行实现 | ✅ 内置 | ✅ | 中等 |
| CrewAI | 任意 | ✅ 内置 | ❌ | ❌ | 低 |
| AutoGen | 任意 | ✅ 内置 | ❌ | ❌ | 中等 |
| Semantic Kernel | OpenAI系为主 | 有限 | 有限 | ❌ | 低 |
| Microsoft Agent Framework | 任意（IChatClient）| ✅ 内置（handoff模式）| ✅ 内置 | ❌ | 中等 |
| DefenseClaw | 模型无关 | ✅（A2A Scanner）| ❌ | ❌ | 低（安全扫描） |

---

*持续更新中*
