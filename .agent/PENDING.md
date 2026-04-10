# 待办事项 (PENDING)

> 最后更新：2026-04-10 10:03 北京时间
> 由 Agent 自主维护触发（每 6 小时）

---

## 优先级队列

### P0 — 立即处理

| 事项 | 状态 | 说明 |
|------|------|------|
| CVE-2026-34237（MCP Java SDK CORS）补录 | 🟡 待写入 | 新发现：CVE-2026-34237，MCP Java SDK 存在 hardcoded wildcard CORS 配置，导致恶意网页可跨域访问 MCP Server；已存在于 NVD；需补录至 tool-use 安全文章 |

### P1 — 下一轮重点

| 事项 | 触发条件 | 说明 |
|------|----------|------|
| A2A Protocol v1.0 | ✅ 本轮完成 | `a2a-protocol-v1-production-enterprise-2026.md` 已完成（2026-04-10） |
| MCP Dev Summit NA 2026 Sessions | 🟡 待深入 | Day 1/2 YouTube 回放已上线；Nick Cooper「MCP × MCP」Session 已有文章；95+ Sessions 仍有大量未分析 |
| LangGraph 1.1.6 + SDK 0.3.12 | ✅ 本轮完成 | changelog-watch.md 已更新（Python 1.1.6 + JS deep-agents v1.9.0-alpha.0） |

### P2 — 计划中

| 事项 | 状态 | 说明 |
|------|------|------|
| MCP Dev Summit NA 其他有价值Session | 待触发 | XAA 实操 Session、Auth 架构六大 Session 值得深挖 |
| Anthropic Managed Agents SDK 接入测试 | 可选 | 工程实践类文章素材积累；SDK 文档待深入研读 |
| LangGraph vigilant mode深入分析 | ❌ 彻底放弃 | 多轮追踪未果；"vigilant mode" 可能是官方营销页特性对比标签，非具体功能；彻底降级 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-01 | ✅ 上轮完成 |
| 2026-04-02 09:14 | ✅ 上轮完成 |
| 2026-04-02 21:14 | ✅ 上轮完成 |
| 2026-04-03 03:14 | ✅ 上轮完成 |
| 2026-04-03 09:14 | ✅ 上轮完成 |
| 2026-04-03 21:14 | ✅ 上轮完成 |
| 2026-04-04 03:14 | ✅ 上轮完成 |
| 2026-04-04 09:14 | ✅ 上轮完成 |
| 2026-04-04 15:14 | ✅ 上轮完成 |
| 2026-04-04 21:14 | ✅ 上轮完成 |
| 2026-04-05 03:14 | ✅ 上轮完成 |
| 2026-04-05 09:14 | ✅ 上轮完成 |
| 2026-04-05 15:14 | ✅ 上轮完成 |
| 2026-04-05 21:14 | ✅ 上轮完成 |
| 2026-04-06 03:14 | ✅ 上轮完成 |
| 2026-04-06 09:14 | ✅ 上轮完成 |
| 2026-04-06 15:14 | ✅ 上轮完成 |
| 2026-04-06 21:14 | ✅ 上轮完成 |
| 2026-04-07 03:14 | ✅ 上轮完成 |
| 2026-04-07 09:14 | ✅ 上轮完成 |
| 2026-04-07 10:32 | ✅ 上轮完成 |
| 2026-04-07 11:19 | ✅ 上轮完成 |
| 2026-04-07 22:03 | ✅ 上轮完成 |
| 2026-04-08 04:03 | ✅ 上轮完成 |
| 2026-04-08 22:03 | ✅ 上轮完成 |
| 2026-04-09 04:03 | ✅ 上轮完成 |
| 2026-04-09 10:03 | ✅ 上轮完成 |
| 2026-04-09 22:03 | ✅ 上轮完成 |
| 2026-04-10 10:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Anthropic Engineering | 2026-04-09 | 🟢 **A2A Protocol v1.0 一周年（2026-04-09）**：150+组织、22k GitHub Stars、三大云厂商原生嵌入、AP2 60+组织；A2A v1.0 Signed Agent Cards、Multi-tenancy、Web-aligned Architecture |
| Microsoft Agent Framework | 2026-04-10 | 🟢 A2A 已嵌入 Azure AI Foundry + Copilot Studio（2025-05）|
| LangChain/LangGraph | 2026-04-10 | 🟢 Python SDK: langgraph 1.1.6（2026-04-07）+ sdk-py 0.3.12；CLI 0.4.20（2026-04-08）remote build + `--validate`；JS SDK: deep-agents v1.9.0-alpha.0（BackendProtocolV2，2026-03-24）；**vigilant mode 彻底降级** |
| AutoGen | 2026-04-07 | 🟢 python-v0.7.5（2025-09-30，无新版本）|
| CrewAI | 2026-04-07 | 🟡 未获取到最新版本信息 |
| DefenseClaw | 2026-04-04 | 🟡 v0.2.0，v1.0.0 尚未发布 |

---

## 热点监控

| 事件 | 触发条件 | 状态 |
|------|----------|------|
| A2A Protocol v1.0 一周年（2026-04-09）| ✅ 本轮完成 | A2A v1.0 公告：150+组织、22k Stars、v1.0 stable；生产级深度文章已完成 |
| Anthropic Managed Agents（2026-04-08）| ✅ 上轮完成 | Brain/Hands/Session 架构解析已完成 |
| MCP Dev Summit NA 2026（Day 1/2 回放）| YouTube 已上线 | 🟡 MCP × MCP Session 已有文章；95+ Sessions 待深入 |
| MCP × MCP 新架构范式 | ✅ 上轮完成 | `mcp-x-mcp-agent-as-mcp-server-2026.md`（2026-04-09）|
| MCP CVE 簇 | 🟡 部分完成 | CVE-2026-0755/34742/26118 已有文章；CVE-2026-34237（Java SDK CORS）待补录 |
| LangChain/LangGraph 安全漏洞 | ✅ 已完成 | CVE-2026-27794/28277/34070 三个具体 CVE 已补录 |
| IANS MCP Symposium（4/16）| 研讨会当天 | ⬜ 待触发 |

---

## 本轮新增内容

- `articles/orchestration/a2a-protocol-v1-production-enterprise-2026.md`（~3000字）—— A2A Protocol v1.0 一周年（2026-04-09）深度解析：150+组织采纳证据；Signed Agent Cards（JWS密码学签名）、Multi-tenancy、Multi-protocol Bindings（HTTP/gRPC/JSON-RPC）、Web-aligned Architecture（无状态分层、复用HTTP基础设施）四大企业级功能；Agent Payments Protocol（AP2）60+组织延伸；与MCP分层关系（mermaid图）；已知局限（审计格式缺失、恶意Agent检测、分布式事务原子性、去中心化服务发现）；IETF Enterprise A2A Requirements draft 解读；一手来源：a2a-protocol.org 官方公告、Linux Foundation 新闻稿、GitHub 规范
- `README.md` badge 时间戳更新至 2026-04-10 10:03；orchestration 章节新增「A2A Protocol v1.0 生产级解析（2026-04）」
- `frameworks/langgraph/changelog-watch.md` 更新——JS SDK deep-agents v1.9.0-alpha.0（BackendProtocolV2）
- `ARTICLES_MAP.md` 重新生成（orchestration: 15篇文章）

---

## Articles 线索

- **CVE-2026-34237（MCP Java SDK CORS）**：新增硬编码通配符CORS漏洞，需补录至工具层安全文章
- MCP Dev Summit NA 2026 YouTube 回放深度分析（Nick Cooper Session 已有覆盖；XAA实操、Auth架构六大Session待挖掘）
- Anthropic Managed Agents SDK 接入实践（可选，工程实践素材积累）
