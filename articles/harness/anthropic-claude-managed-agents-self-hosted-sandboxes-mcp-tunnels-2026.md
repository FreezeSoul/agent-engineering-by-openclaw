# Claude Managed Agents 自托管沙箱与 MCP 隧道：Anthropic 把「执行边界」正式还给了企业

> **一句话总结**：Anthropic 5 月 19 日宣布 Claude Managed Agents 支持**自托管沙箱**（Cloudflare / Daytona / Modal / Vercel 任意选择）与 **MCP 隧道**（让 Agent 访问内网 MCP 而无需暴露公网入口）。这是 Anthropic 第一次在旗舰产品层**正式承认「Agent 执行边界应在企业内」**——Agent 的编排回路留在 Anthropic，工具执行留在企业的边界内。

**评分**：5/5（实用性 / 独特性 / 时效性）——一手源 + 时效极强 + 架构范式宣告

## 标签

- `agent-harness`
- `self-hosted-sandbox`
- `mcp-tunnel`
- `managed-agents`
- `enterprise-boundary`

## 来源

- 原始博客：[claude.com/blog/claude-managed-agents-updates](https://claude.com/blog/claude-managed-agents-updates)
- 发布日期：2026-05-19
- 阅读时长：5 min
- 分类：Product announcements · Claude Platform

---

## 一、为什么这次更新是范式宣告

在 Claude Managed Agents 自托管沙箱出现之前，企业部署 Anthropic 的托管 Agent 只有两种选择：

1. **完全托管**：把 Agent 执行也放在 Anthropic 云上 → 数据出域、不合规
2. **完全自建**：用 Claude API + LangChain / LangGraph 自己搭 → 失去 Managed Agents 的会话管理、错误恢复、版本控制

**这次更新的核心创新是把这两层解耦**：

| 层 | 位置 | 职责 |
|---|---|---|
| **Agent Loop**（编排层）| Anthropic 云 | 会话、上下文、错误恢复、版本管理、工具路由 |
| **Tool Execution**（执行层）| 企业边界内 | 沙箱运行、网络策略、审计日志、资源配额 |

引用 Anthropic 自己的描述：

> "The agent loop that handles orchestration, context management, and error recovery stays on Anthropic's infrastructure, while tool execution moves to your own configured environment."

这是 **Agent Harness 的"两层分工"** —— 由厂商正式背书。之前 Daytona / Cloudflare Sandboxes 这类自托管沙箱项目不得不证明自己「值得在生产用」，现在 Anthropic 把它们写进了官方推荐清单。

## 二、四大沙箱提供商的差异化定位

Anthropic 这次没做单一推荐，而是**列出 4 家**——每家擅长场景不同，企业按需选择：

| 厂商 | 核心技术 | 强场景 | 关键指标 |
|---|---|---|---|
| **Cloudflare** | microVM + 轻量 isolates | 大规模多租户、零信任 secrets、可审计 egress | 零信任注入 + 自定义 proxy |
| **Daytona** | OCI 标准 + 可选 Kata/Sysbox | 长运行 / 有状态 Agent、SSH / preview URL 访问 | Sub-90ms 冷启动 |
| **Modal** | Functions + Storage + Networking 同源 | AI 工作负载 + GPU 按需 | Sub-second 启动、十万级并发 |
| **Vercel** | VM + VPC peering + BYOC | 网络边界注入凭据、毫秒级启动 | 凭据不入沙箱 |

值得注意的是 **Vercel 沙箱的"凭据不入沙箱"模式**——这是真正有信息量的安全设计：

> "Vercel Sandbox firewall injects credentials at the network boundary so they never enter the sandbox."

凭据在网络边界注入，沙箱内不可读取——这是把「凭据可见性」和「代码执行边界」分开的范式，比"把 secrets 放到环境变量"安全得多。

## 三、MCP 隧道：让 Agent 访问内网 MCP 服务

第二个核心特性是 **MCP tunnels**（研究预览）—— 这是「私有 MCP 服务」的对位：

> "Your agents reach MCP servers inside your private network without exposing them to the public internet."

部署一个轻量级网关，建立**单一出站连接**——不需要入站防火墙规则、不需要公网入口、流量端到端加密。

这解决了企业部署 MCP 的核心痛点：内部数据库、私有 API、知识库、工单系统变成 Agent 可调用的工具，**但这些服务永远不暴露在公网**。

支持范围：Claude Managed Agents + Messages API，由组织管理员在 Claude Console 的 workspace settings 中配置。

## 四、闭环 Project：四大角度

这次更新是 Anthropic 第一次正式「开放」Managed Agents 的执行层边界，因此**项目配对需要覆盖四个象限**——商业 vs 开源、编排层 vs 执行层：

| 项目 | 抽象层 | 角色 | 关联方式 |
|---|---|---|---|
| [multica-ai/multica](https://github.com/multica-ai/multica)（29.5K⭐）| 编排层 OSS | Claude Managed Agents 的**开源对位**（Pattern 8）| Multica 是开源的「Agent-as-Teammate」平台，与 Claude Managed Agents 在「Agent 怎么协作」上正面竞争 |
| [daytona/daytona](https://github.com/daytona-io/daytona) | 执行层 OSS | Anthropic 官方推荐的四大沙箱之一 | 详见既有 `daytona-open-source-ai-agent-sandbox-oci-containers-2026.md` |
| Cloudflare Sandboxes（已有 Article） | 执行层商业 | Anthropic 官方推荐的四大沙箱之一 | 详见既有 `cloudflare-sandboxes-ga-agent-persistent-execution-environment-2026.md` |
| Modal / Vercel | 执行层商业 | Anthropic 官方推荐的四大沙箱之一 | Anthropic 首肯，强烈信号 |

**为什么这是 Pattern 8 + Pattern 14 混合**：

- **Pattern 8**（商业 vs 开源对位）：Claude Managed Agents（商业编排层）↔ Multica（开源编排层）
- **Pattern 14**（SPM 配对既有）：Daytona / Cloudflare Sandboxes 在仓库内已有详细项目文件，不重写，直接用 SPM 配对既有

**读者决策矩阵**：

| 你的需求 | 推荐路径 |
|---|---|
| 想要厂商托管 + 编排 | Claude Managed Agents + 自选沙箱 |
| 想要完全开源 | Multica + Daytona + 自建 MCP |
| 大规模多租户 | Cloudflare Sandboxes |
| GPU 工作负载 | Modal |
| 网络边界凭据隔离 | Vercel Sandbox |
| 长运行 / 有状态 | Daytona |

## 五、与已有 sandbox 系列文章的关系

本仓库已有多篇沙箱相关文章：

- `articles/harness/cloudflare-sandboxes-ga-agent-persistent-execution-environment-2026.md`（Cloudflare Sandboxes GA 架构）
- `articles/harness/anthropic-claude-code-sandboxing-os-level-isolation-2026.md`（OS-level isolation 视角）
- `articles/projects/daytona-open-source-ai-agent-sandbox-oci-containers-2026.md`（Daytona OCI 实现）
- `articles/harness/anthropic-effective-harnesses-long-running-agents-2026.md`（Long-running Harness 架构）

**本文不重复既有覆盖**，本文的新增价值是：

1. **范式宣告**：Anthropic 第一次在旗舰产品层把「执行边界」开放给企业
2. **4 厂商横向对比**：Cloudflare / Daytona / Modal / Vercel 的差异化场景与关键指标
3. **凭据网络边界注入模式**：Vercel 范式
4. **MCP 隧道**：内网 MCP 服务暴露问题的官方解
5. **闭环图谱**：把 Anthropic 商业版 ↔ Multica OSS 版 ↔ 四大沙箱并列对照

## 六、为什么「执行边界开放」是 2026 的关键趋势

这次更新背后是 2026 年 Agent 部署的三个共同需求：

1. **数据合规**：金融、医疗、法律行业要求代码执行不离开企业网络
2. **凭据隔离**：企业 API keys 不能进入任何沙箱（即使沙箱在企业内）
3. **MCP 私有化**：企业内部 MCP 服务不能暴露公网

Anthropic 的「Managed Agents + 自托管沙箱 + MCP 隧道」是把三个需求**用统一架构回答**。这不是单点功能，是**范式声明**——Agent 厂商未来 12 个月的演进路线都会沿着「把执行层开放给企业」展开。

## 七、一句话总结

> Claude Managed Agents 的「自托管沙箱 + MCP 隧道」是 Anthropic 对「Agent 在哪里执行」这一根本问题的官方回答：**编排留在 Anthropic，执行留给企业**——这是 Agent Harness 从「云端黑盒」走向「企业边界内基础设施」的范式宣告。

---

**附：四大沙箱厂商的 Anthropic 客户引用**

| 客户 | 场景 | 引用关键句 |
|---|---|---|
| Clay（Sculptor）| GTM 工程 Agent | "我们想要给 Agent 一种比'工具循环'更灵活、更强大的执行方式" |
| Rogo | 金融分析师 Agent | "best-in-class 基础设施 + 投资银行家真正需要的产品表面" |
| （未具名 CTO）| 企业内部工具编排 | "我们一周内就跑通了，企业客户可靠性提升" |
| Amplitude | Design Agent | "在已经信任的基础设施上，两天内跑出第一个可用版本" |

*本文属于「Agent Harness 演进」系列，分析 Managed Agents 开放执行边界的工程含义。*