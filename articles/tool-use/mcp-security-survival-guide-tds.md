# The MCP Security Survival Guide: Best Practices, Pitfalls, and Real-World Lessons

> 来源：Towards Data Science（ practitioner's blog）
> 评分：5/5（实践 5 / 独特 4 / 质量 5）

## 背景

作者自述：最初对 MCP 充满热情（"discovering a universal adapter for AI agents"），随后遭遇真实安全事件后开始深入研究安全实践。

## 三大真实 CVE 案例

### Case 1: Remote Code Execution via Exposed MCP Inspector (CVE-2025-49596)

MCP Inspector 工具未正确配置，导致在数千台开发者机器上打开后门。

### Case 2: Prompt Injection via SQLite MCP Server Exploit

通过 MCP Server 注入恶意 Prompt，展示了 Agent 被操纵的实际路径。

### Case 3: Enterprise Integration Met the Real World

企业集成场景中，OAuth 配置不当导致的真实安全事故。

## 安全最佳实践

### OAuth 安全流程（推荐）

```
用户已认证 → 请求第三方授权 → consent screen → 发放 consent cookie 
→ 3P authorization code → MCP Proxy 换取 access token 
→ MCP Client 获得受限访问权限
```

**关键**：用户知情同意、token 边界控制、MCP Proxy 不做 silent middleman。

### 核心原则

- MCP 的 local-first 设计是保护层，不是保险箱
- "built-in tool isolation + user consent prompts" 需要正确配置才能生效
- YOLO 部署（root + public port + no logging）等于自开门

## 独特价值

1. **官方不会写的教训**：安全事件的真实复盘，而非技术宣传
2. **防御框架可操作**：从 auth flow 到 case study，有完整路径
3. **"Terrifying because almost nobody was using them"**：从业者视角的坦诚批评

## 一句话总结

> 三个真实 CVE + 完整防御框架——踩过坑的 practitioner's 复盘，比任何官方文档都诚实。

## 原文

https://towardsdatascience.com/the-mcp-security-survival-guide-best-practices-pitfalls-and-real-world-lessons/

## 标签

#community #MCP #security #CVE #practitioner-lessons

---

## 关联补充：Nearform 工程实践 — MCP 实施避坑指南

> 以下内容作为 MCP 工程实施的补充参考。

### 框架选择

| 语言 | 推荐框架 | 警告 |
|------|----------|------|
| **JavaScript/TypeScript** | 官方 TypeScript SDK + Platformatic MCP Server | 避免小众/非官方框架 |
| **Python** | 官方 SDK + FastMCP | — |

### 快速起步建议

1. 从单个小服务器开始，只暴露 1-2 个工具
2. 先用 inspector/playground 本地调试，不急着连真实数据
3. 用代码助手生成初始代码（提供 MCP 框架链接即可）

### 传输层选择

- **STDIO**：桌面应用偏好，本地进程通信
- **Streamable HTTP/SSE**：远程/云场景

### 生态建议

- 先扫描现有 MCP 服务器库（Filesystem、GitHub、Slack、Google Drive、Postgres 等）
- MCP Market 是找现成服务器的好来源

> 来源：https://nearform.com/digital-community/implementing-model-context-protocol-mcp-tips-tricks-and-pitfalls/
