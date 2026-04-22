# A2A 协议一周年：从开源发布到生产级标准的演进复盘

> *本文分析 Google Agent2Agent（A2A）协议在发布一年后的技术演进、生产落地情况与未来方向。*

---

## 2026 年 4 月 9 日：A2A 一周年

2025 年 4 月 9 日，Google 宣布了 [Agent2Agent（A2A）协议](https://a2a-protocol.org/)。一年后（2026 年 4 月 9 日），Linux Foundation 宣布了它的生产落地里程碑：**150+ 组织支持、22,000+ GitHub Stars、5 个生产级语言 SDK**，以及 Microsoft Azure AI Foundry、AWS Bedrock AgentCore Runtime 的深度集成。

这不是一个标准从零到有的故事——这是关于一个协议如何在一年内跨越"可用"到"生产就绪"的故事。本文拆解其中的关键工程决策和生态演化逻辑。

---

## 为什么需要 A2A：协调层的需求

在 A2A 出现之前，多 Agent 系统面临一个根本性的协调问题：**谁来持有任务状态、谁决定执行顺序、任务完成后如何汇报结果？**

常见的实现方式是让一个"父 Agent"持有所有子 Agent 的上下文，通过 prompt 注入传递任务描述。这在 Demo 场景中工作良好，但在生产环境面临三个问题：

1. **上下文窗口瓶颈**：随着子 Agent 数量增加，上下文线性膨胀，超出模型窗口只是时间问题
2. **供应商锁定**：每个 Agent 实现自己的内部协议，对外不可见、不可互操作
3. **信任边界模糊**：父 Agent 和子 Agent 共享内存，双方都没有清晰的 identity 和权限边界

A2A 的核心设计目标是：**在保持 Agent 内部状态私密性的前提下，实现跨供应商、跨环境的 Agent 协调**。

---

## 关键工程决策

### 决策一：与 MCP 分层，不做竞争

A2A 官方文档明确将自身定位为 [MCP 的互补而非替代](https://a2a-protocol.org/latest/announcing-1.0/#complementary-to-mcp-not-a-replacement)：

| 协议 | 层级 | 解决的问题 |
|------|------|-----------|
| **MCP** | 工具接入层 | Agent → 工具/数据源的连接 |
| **A2A** | 协调层 | Agent ↔ Agent 的任务分发与结果汇总 |

这个分层设计不是技术限制，而是刻意的生态策略：**让每个协议做一件事，并做好**。实践中，MCP 服务器通常运行在本地（stdio 传输），而 A2A 通常运行在网络上（HTTP/WebSocket）。两者在协议栈上不重叠，在实现上可以共存。

> **工程建议**：当你的系统只需要"让 Agent 调用工具"，MCP 足够；当你的系统需要"多个 Agent 协作完成任务"，需要 A2A；当两者都需要时，典型架构是：A2A 协调多个 Agent，每个 Agent 通过 MCP 连接自己的工具集。

### 决策二：Agent Card 的身份发现机制

A2A 引入了 **Agent Card**——一个 JSON 描述文件，每个 Agent 暴露自己的能力、端点和身份：

```json
{
  "agentId": "research-agent-001",
  "displayName": "Research Agent",
  "description": "Performs web research and returns structured findings",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "streamingMode": "text/event-stream"
  },
  "skills": [
    {"id": "web-search", "name": "Web Search"},
    {"id": "fact-check", "name": "Fact Checking"}
  ],
  "endpoints": {
    "primary": "https://agents.company.com/research-a2a"
  },
  "version": "1.0.0"
}
```

v1.0 进一步引入了 **Signed Agent Card**：Agent Card 通过私钥签名，接收方可以验证 Agent 身份而非仅依赖网络地址。这是 A2A 进入企业环境的门票——在金融、保险等受监管行业，不知道对方是谁是不可接受的。

### 决策三：Web 对齐架构

v1.0 的 [web-aligned architecture](https://a2a-protocol.org/latest/announcing-1.0/#web-aligned-architecture-for-scale) 是最被低估的设计决策。

A2A 选择 HTTP 作为默认传输层，复用了 Web 安全基础设施（TLS、OAuth 2.0、CORS、负载均衡）。这意味着：

- 企业安全团队已经理解这些模式，不需要学习新的安全原语
- 现有的 API 网关、服务网格（Istio、Envoy）可以直接代理 A2A 流量
- 日志、监控、追踪工具不需要定制开发

这与 MCP 的 stdio 传输形成鲜明对比：MCP 的 stdio 设计适合本地开发场景，A2A 的 HTTP 设计适合跨网络的生产部署。

### 决策四：版本协商机制

A2A 包含了一个内置的版本协商协议。Client Agent 和 Server Agent 在建立连接时交换支持的协议版本范围，协商出一个共同支持的最高版本。这解决了多版本共存环境的兼容性问题，也是"生产级"的重要标志之一。

---

## 生产落地：从概念验证到行业覆盖

### 谁在用 A2A

根据 [Linux Foundation 公告](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)，A2A 的生产部署覆盖了以下垂直行业：

| 行业 | 典型场景 |
|------|---------|
| **供应链** | 跨系统库存查询、订单状态同步 |
| **金融服务** | 跨行账户对账、风险评估协作 |
| **保险** | 理赔处理中多 Agent 协调（理赔 Agent + 核保 Agent + 客服 Agent）|
| **IT 运维** | 跨工具事件响应（监控 Agent + 告警 Agent + 自动修复 Agent）|

Google Cloud 的 VP Rao Surapaneni 表示："AI Agent 的价值取决于其协作能力，150+ 组织的支持证明了行业对开放互操作协议的广泛认同。"

### 云平台的默认集成

三个主流云厂商的动作为 A2A 提供了实质性的分发渠道：

- **Microsoft**：A2A 深度集成进 Azure AI Foundry 和 Copilot Studio，意味着 Azure 上的企业 Agent 默认可以互相通信
- **AWS**：通过 Amazon Bedrock AgentCore Runtime 支持 A2A，Bedrock 上的 Agent 可以跨账户协作
- **Google Cloud**：A2A 作为 Cloud AI 平台的默认协调协议

当云厂商开始在平台层默认支持一个协议时，开发者采用成本从"自己集成"降到了"勾选配置"。

### SDK 生态：5 个生产级语言实现

一年前只有 Python SDK。如今 [5 个生产级语言 SDK](https://github.com/orgs/A2A-Protocol/repos)：

| SDK | 语言 | 状态 |
|-----|------|------|
| langchain-a2a | Python | 生产级 |
| @a2a-client / @a2a-server | JavaScript/TypeScript | 生产级 |
| a2a-java | Java | 生产级 |
| a2a-go | Go | 生产级 |
| a2a-dotnet | .NET | 生产级 |

多语言支持对企业采用至关重要：很多企业的核心系统运行在 Java/.NET 上，不支持这些语言的协议等于不支持这些企业。

---

## 扩展：AP2 与经济协调层

A2A 生态正在向"经济协调"延伸。**Agent Payments Protocol（AP2）** 提供了 Agent 之间的安全支付语义，已获得 60+ 金融机构支持。

这代表了 Agent 协议栈的第三层浮现：

```
工具接入层 (MCP) → 协调层 (A2A) → 经济协调层 (AP2)
```

当 Agent 可以代表用户执行支付时，Agentic AI 的能力边界发生了质变：从"执行任务"到"完成交易"。这对合规和风控提出了全新的要求。

---

## 已知局限与未解问题

### 协议级安全仍未完全解决

A2A v1.0 的 Signed Agent Card 解决了身份验证问题，但**传输加密、消息完整性、抗重放攻击**等安全机制仍依赖 TLS 层面。这对于企业内网场景足够，但对于跨域的零信任环境，仍需在应用层补充安全设计。

### Agent Registry 缺失

当前版本的 A2A 没有标准的 Agent 注册与发现机制。Agent Card 解决了"单个 Agent 如何描述自己"的问题，但"系统中有哪些 Agent 可用、如何按能力查询"仍是空白。官方 Roadmap 提到了 Registry 规范，这是生产部署的必要基础设施。

### SDK 实现成熟度不均

Python SDK（langchain-a2a）因 LangChain 社区的规模而最成熟；.NET SDK 的企业采用案例相对较少，生产验证不充分。跨语言的协议一致性测试在 v1.0 阶段尚未标准化。

### MCP-A2A 边界在实际落地中仍然模糊

虽然协议层面分层清晰，但实际系统中[MCP 和 A2A 的边界划分](https://github.com/A2A-Protocol/specification/issues)仍是高频问题。尤其是在"A2A Client Agent 调用一个 MCP 服务器实现的 Agent"这种跨协议场景中，两层协议的交互语义缺乏统一规范。

---

## 未来方向：Roadmap 解读

A2A 官方 Roadmap 列出了以下优先方向：

1. **Interoperability Specification**：跨协议互操作规范，可能涉及 A2A ↔ ACP/UCP 的桥接
2. **Registry & Discovery**：标准化的 Agent 注册与查询机制
3. **Testing & Tooling**：协议一致性测试套件、调试工具
4. **Security Best Practices**：企业部署安全配置指南

第 1 条尤其值得注意：目前市场上还有 ACP（Agent Collaboration Protocol）和 UCP（Universal Client Protocol）等竞争协议，Roadmap 提到互操作性意味着 A2A 可能尝试整合而非对抗。

---

## 总结：协议成功的三个要素

回看 A2A 的一年历程，它能走到生产级标准，本质上做对了三件事：

**1. 定位清晰，不做全能协议**
A2A 明确只做 Agent 协调，把工具接入留给 MCP，把经济协调留给 AP2。这个边界意识避免了协议膨胀导致的实现复杂度。

**2. 复用 Web 基础设施，降低企业采用门槛**
选择 HTTP/TLS/OAuth 而不是自研安全协议，让企业安全团队不需要重新学习。这对一个需要在企业环境落地的协议至关重要。

**3. 云厂商默认集成，解决分发问题**
云厂商在平台层支持 A2A，开发者不需要主动集成——分发自然发生。这与 MCP 通过 npm/Cargo 包管理器分发的路径不同，但都有效地触达了目标用户。

**值得持续追踪的问题**：
- AP2 的支付语义在监管严格的地区（如欧盟 PSD2、中国支付监管）如何适配
- Agent Registry 规范落地后，A2A 与服务发现生态（Consul、etcd）的集成方式
- ACP/UCP 与 A2A 的竞争与整合动态

---

## 参考来源

- [A2A Protocol Surpasses 150 Organizations, Lands in Major Cloud Platforms — Linux Foundation Press](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)（一手：Linux Foundation 官方公告，2026-04-09）
- [A2A Protocol v1.0 公告](https://a2a-protocol.org/latest/announcing-1.0/)（一手：协议官方规范，A2A 与 MCP 分层、Signed Agent Card、Web-aligned architecture 说明）
- [A2A Protocol 官网](https://a2a-protocol.org/)（一手：协议规范、SDK 列表、Roadmap）
- [LangChain A2A 集成文档](https://docs.langchain.com/langsmith/server-a2a)（一手：LangChain 对 A2A 的官方支持说明）
- [CrewAI A2A 集成文档](https://docs.crewai.com/en/learn/a2a-agent-delegation)（一手：CrewAI 对 A2A 的官方支持说明）
- [Azure AI Foundry A2A 集成](https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/)（一手：Microsoft 官方博客）
- [AWS Bedrock AgentCore A2A 支持](https://aws.amazon.com/about-aws/whats-new/2025/11/marketplace-a2a-server-bedrock-agentcore-runtime/)（一手：AWS 官方新闻）
