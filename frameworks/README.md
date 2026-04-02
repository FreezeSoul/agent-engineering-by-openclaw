# 框架专区

> 每个框架独立子目录，统一使用模板。
> **精简说明**：本目录仅保留在 Agent 工程体系中有独特定位的核心框架。已在文章中深度覆盖的框架（如 DefenseClaw 安全五引擎）不在此重复收录。

---

## 目录

| 框架 | 定位 | overview | examples | changelog |
|------|------|----------|----------|-----------|
| [LangGraph](langgraph/) | 状态机模式，适合复杂工作流 | ✅ | ✅ | ✅ |
| [CrewAI](crewai/) | 角色扮演式多Agent协作 | ✅ | ✅ | ✅ |
| [AutoGen](autogen/) | Microsoft多模型协作 | ✅ | ✅ | ✅ |
| [Microsoft Agent Framework](microsoft-agent-framework/) | Semantic Kernel + AutoGen 合并，.NET 企业级 | ✅ | ✅ | ✅ |
| [_template/](_template/) | 新增框架时复制的模板 | ✅ | — | ✅ |

---

## 已移除框架（价值已在文章中覆盖）

| 框架 | 移除理由 |
|------|---------|
| DefenseClaw | 安全价值已由 `articles/harness/` 和 `articles/evaluation/` 中 Cisco A2A Scanner、OWASP Top 10、MCP Security Crisis 等文章覆盖 |
| Paperclip | "零人类公司"概念独特但过于 niche，生产实践案例不足，框架本身 stars 虽高但落地资料少 |

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

---

*持续更新中*
