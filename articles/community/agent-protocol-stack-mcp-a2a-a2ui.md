# Agent Protocol Stack：为什么 MCP + A2A + A2UI 是 Agentic AI 的 TCP/IP 时刻

> **本质**：三个协议，三层职责——MCP 解决 Agent 如何调用工具，A2A 解决 Agent 之间如何协作，A2UI 解决 Agent 如何渲染界面。三者叠加，才是完整的 Agent 交互架构。

---

## 一、基本概念

### 三个协议，三个问题

2026 年初，Agent 协议领域不再是"一个协议打天下"的局面。Anthropic 的 MCP、Google 的 A2A 和 A2UI 三个协议**各自解决不同层次的通信问题**，但被大量从业者混为一谈。

| 协议 | 提出者 | 时间 | 解决的问题 | 类比 |
|------|--------|------|-----------|------|
| **MCP**（Model Context Protocol）| Anthropic | 2024-11 | Agent 如何访问工具、数据、上下文 | Agent 的手和眼 |
| **A2A**（Agent2Agent）| Google Cloud | 2025-04 | 不同厂商/框架的 Agent 如何作为对等方协作 | Agent 的网络层 |
| **A2UI**（Agent to UI）| Google | 2025-12 | Agent 如何生成跨平台富交互界面 | Agent 的显示器 |

> **关键区分**：MCP 把外部系统当作工具来调用；A2A 把其他 Agent 当作对等协作者来交互。两者信任模型不同，失败模式不同，安全边界不同。

---

## 二、三层协议的职责分工

### MCP：资源访问层

**核心问题**：Agent 如何连接数据库、调用 API、读取文件？

- **原语**：Resources（数据资源）、Prompts（模板提示）、Tools（可调用函数）
- **治理**：Linux Foundation Agentic AI Foundation（2025-12）
- **现状**：10,000+ 活跃 MCP Server；每月 9,700 万次 SDK 下载（2025-12 数据）
- **信任模型**：Server 端权限控制

### A2A：协作层

**核心问题**：来自不同厂商/组织的 Agent 如何发现彼此能力并委派任务？

- **原语**：AgentCards（能力发现）、Tasks（工作单元）、Messages（通信内容）
- **治理**：Linux Foundation（2025-06 捐赠）
- **现状**：v0.3，支持长时运行任务和状态推送
- **信任模型**：跨组织认证（Parity with OpenAPI auth）

### A2UI：渲染层

**核心问题**：Agent 如何在不执行任意代码的前提下，向用户渲染富交互界面？

- **原语**：声明式 UI 组件，原生跨平台渲染
- **成熟度**：v0.8 稳定版（2025-12）
- **信任模型**：客户端沙箱隔离

---

## 三、三层协议的叠加架构

### 叠加工作流示例

以"用户查询航班，Agent 完成预订"为例：

```
用户 → A2UI：自然语言查询（"帮我找下个月去东京500美元以下的航班"）
  ↓
A2UI → Orchestrator Agent：解析意图，创建任务
  ↓
Orchestrator Agent → Specialist Agent（A2A）：通过 AgentCard 发现能力，委派航班搜索任务
  ↓
Specialist Agent → 航班 API（MCP）：查询实时航班数据
Specialist Agent → 历史价格 API（MCP）：查询历史价格
  ↓
Specialist Agent → Orchestrator Agent（A2A）：返回12个选项
  ↓
Orchestrator Agent → A2UI：返回结构化数据
  ↓
A2UI → 用户：渲染可交互航班卡片（含过滤功能）
```

### 职责矩阵

| 协议 | 职责 | 信任边界 | 失败模式 |
|------|------|---------|---------|
| A2UI | 用户交互、UI 渲染 | 客户端沙箱 | UI 异常（不丢数据）|
| A2A | 任务委派、能力发现 | 跨组织认证 | 任务失败、可重试 |
| MCP | 数据访问、工具执行 | Server 端权限 | 数据损坏、权限提升 |

---

## 四、三层协议的组合模式

### 早期采用案例

| 框架/产品 | A2A 支持 | MCP 支持 | A2UI 支持 |
|-----------|---------|---------|---------|
| AgentMaster（2025-07）| ✅ 首个生产案例 | ✅ | ❌ |
| Google ADK | ✅ 原生支持 | ✅ | ✅ |
| LangGraph v0.2（2026-01）| ✅ 一等公民 | ✅ | ❌ |

**LangGraph v0.2**（2026-01-15 发布）明确将 A2A 和 MCP 作为一等公民协议目标，标志着主流框架层面对协议叠加的正式支持。

### IBM 的经典比喻

> 零售库存 Agent 用 MCP 检查库存水位，库存低于阈值时用 A2A 通知供应商 Agent 下单。协议之间是**互补关系**，而非竞争关系。

---

## 五、三层协议的三个结构性缺口

> 这是当前最被忽视的风险。协议在技术上叠加了，但在身份模型、可观测性、错误传播三个维度上存在根本性断层。

### 缺口一：无统一身份模型

MCP 有自己的认证模型（2025 年升级至 OAuth 2.1），A2A 有自己的认证方案，A2UI 在客户端处理信任的方式又不同。

**实际问题**：通过 A2A 认证的委派 Agent，无法保证将身份上下文传递到实际执行工具调用的 MCP 层。中间 Agent 独立重新认证。**凭证管理成为每层各自为政的问题**。

### 缺口二：可观测性不跨层

可以追踪单个 MCP 请求，可以追踪单个 A2A 任务，但追踪一个用户请求从 A2UI → A2A → MCP → 返回的完整链路，需要拼接三个不同的可观测性系统。

**分布式追踪在此协议栈上尚无成熟解决方案**。

### 缺口三：错误传播语义未定义

当 MCP 工具调用在 A2A 委派的任务内失败时会发生什么？A2A 规范支持长时任务和状态更新，但"MCP 层错误如何映射到 A2A 层任务状态"的语义**未标准化**。

---

## 六、安全隐患：协议叠加 ≠ 安全叠加

正如早期互联网协议（1995 年的 HTTP + FTP），**安全和协议设计是分开演进的**。三层 Agent 协议叠加带来了新的攻击面：

| 攻击面 | 描述 | 案例 |
|--------|------|------|
| **身份跳层攻击** | A2A 认证身份被滥用穿透 MCP 层权限 | Agent 获得 A2A 委派权限后，在 MCP 层越权访问数据 |
| **协议间信任链断裂** | 各层独立认证导致中间人风险 | A2UI 层的 XSS 配合 A2A 能力发现窃取敏感任务 |
| **可观测性盲区** | 安全事件在协议边界丢失 | MCP Server 被攻击，但 A2A 协作层未记录 |
| **沙箱逃逸链** | WebMCP UAF（CVE-2026-3918）+ 浏览器沙箱 → 系统权限 | 参见 `digest/breaking/2026-03-26-cve-2026-3918-chrome-webmcp-use-after-free.md` |

---

## 七、实践建议

### 框架选型判断

| 场景 | 推荐协议组合 |
|------|------------|
| 单 Agent + 多工具 | 仅 MCP |
| 多 Agent 协作（同一组织）| A2A + MCP |
| 多 Agent + 富交互前端 | A2A + MCP + A2UI |
| 跨组织 Agent 协作 | A2A（必须配 OAuth） + MCP + A2UI |

### 安全红线

1. **不要跳过 A2A 的认证层**：跨组织 Agent 通信必须使用 OAuth 2.1 或同等强度的认证
2. **MCP Server 最小权限**：每个 MCP Server 独立鉴权，不要信任来自 A2A 协作层的隐式信任
3. **WebMCP 浏览器安全**：通过浏览器使用 MCP 时，确保 Chrome 已更新至 146.0.7680.71+（防止 CVE-2026-3918）
4. **协议层可观测性**：在每层独立日志之上，建立统一的请求追踪 ID 跨层传播机制

---

## 八、局限性

1. **标准仍在快速演进**：三个协议均未达到 1.0 稳定版，API 存在变更风险
2. **实现碎片化**：不同框架对 A2A/MCP 的实现深度不一，互操作性仍有差距
3. **安全规范滞后**：协议设计先于安全最佳实践，OWASP ASI Top 10 for Agentic Applications 是当前最重要的安全基线

---

## 九、参考文献

- [The Agent Protocol Stack: Why MCP + A2A + A2UI Is the TCP/IP Moment for Agentic AI](https://subhadipmitra.com/blog/2026/agent-protocol-stack/)（2026-01）
- [A2A Protocol Explained: Secure Interoperability for Agentic AI 2026](https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/)（OnReach AI）
- [Architecting Agentic MLOps: a Layered Protocol Strategy — A2A + MCP](https://www.infoq.com/articles/architecting-agentic-mlops-a2a-mcp/)（InfoQ）
- [MCP vs A2A: Protocols for Multi-Agent Collaboration 2026](https://onereach.ai/blog/guide-choosing-mcp-vs-a2a-protocols/)（OnReach AI）
- [AI Agent Protocols 2026: Complete Guide](https://www.ruh.ai/blogs/ai-agent-protocols-2026-complete-guide)（Ruh AI）
