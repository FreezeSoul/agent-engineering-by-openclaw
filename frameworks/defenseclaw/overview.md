# DefenseClaw — Security Governance for Agentic AI

> Cisco 推出的开源 Agent 安全治理框架，于 RSAC 2026（3/23-27）正式发布，旨在弥补企业从 AI 实验到生产部署的安全差距。

---

## 核心定位

| 维度 | 说明 |
|------|------|
| **定位** | Agentic AI 的安全治理平台（Security Governance for Agentic AI）|
| **出品方** | Cisco（cisco-ai-defense）|
| **发布时间** | RSAC 2026（2026-03-23）|
| **开源** | GitHub：cisco-ai-defense/defenseclaw |
| **stars** | 127（截至 2026-03-26）|
| **集成** | NVIDIA OpenShell 运行时（沙箱执行环境）|

---

## 五工具扫描引擎

DefenseClaw 统一的扫描引擎运行五个专项工具，覆盖 AI Agent 攻击面的每个维度：

### 1. Skills Scanner

每个 AI Agent 依赖"技能"（Skills）来完成任务（搜索、CRM 查询、邮件发送等）。Skills Scanner 在技能获准运行前进行审查：

- 检测已知漏洞
- 识别异常行为
- 权限范围不匹配检测
- 标记并沙箱隔离越界技能

### 2. MCP Scanner

MCP Server 是 Agent 连接外部工具和数据源的桥梁。MCP Scanner 验证每个 MCP Server 的：

- 完整性（未被篡改）
- 授权状态（在白名单中）
- 运行时变更监控
- 若被阻断：从 OpenShell 层面移除端点，拒绝所有后续连接

### 3. A2A Scanner

Agent-to-Agent（A2A）通信引入了新的攻击面——恶意/被入侵的子 Agent 可污染主 Agent 行为。A2A Scanner 监控和验证 Agent 间通信：

- Agent Card 身份验证
- 任务重放攻击检测
- 权限提升防御
- 工件篡改检测
- 详见：[Cisco A2A Scanner 独立博客](https://blogs.cisco.com/ai/securing-ai-agents-with-ciscos-open-source-a2a-scanner)

### 4. CodeGuard

Agent 不只执行预写代码，还会动态生成代码。CodeGuard 是静态分析层：

- 检查 Agent 生成的每段代码（执行前）
- 强制安全最佳实践策略
- 标记危险模式：未检查的文件写入、开放网络套接字、权限提升尝试

### 5. AI Bill of Materials（AI BoM）

类比软件物料清单（SBOM），AI BoM 自动生成和维护所有 AI 资产的完整清单：

- 运行中的 Agent 清单
- 使用的 Skills 清单
- 连接的 MCP Server 清单
- 依赖的模型清单
- **持续更新**（非一次性快照），提供实时、可审计的 Agent 劳动力记录

---

## 架构特点

### Admission + Runtime 双阶段覆盖

五个工具不仅在准入阶段运行，还持续监控运行时安全——捕捉部署后引入的漏洞。

### 与 NVIDIA OpenShell 集成

DefenseClaw 构建在 NVIDIA OpenShell 运行时之上，提供硬化的沙箱执行环境，消除企业采用 AI Agent 历史上的许多手动安全步骤。

### Cisco 更大安全战略的一部分

DefenseClaw 是 Cisco Agentic AI 安全平台的组成部分，还包括：

- **Zero Trust Access for Agents**：通过 Duo 平台将零信任访问扩展到 AI Agent
- **AI Defense: Explorer Edition**：自助服务工具，供开发者测试模型和应用弹性
- **Splunk SOC 增强**：SOC 团队可在机器速度下阻止威胁

---

## 企业采用数据

- **85%** 的大型企业正在试验 AI Agent
- **仅 5%** 已将 Agent 部署到生产环境
- 安全差距是部署延迟的核心原因

---

## 快速开始

```bash
# GitHub
https://github.com/cisco-ai-defense/defenseclaw
```

---

## 在演进路径中的位置

DefenseClaw 属于 **Stage 12（Harness Engineering）** 的核心工程实践，覆盖：

- Tool Constraints（Skills/MCP Scanner）
- Behavioral Rules（CodeGuard）
- Cleanup（AI BoM 持续监控）
- Circuit Breaker（A2A Scanner 的威胁检测）

---

## 相关资源

| 资源 | 链接 |
|------|------|
| GitHub | https://github.com/cisco-ai-defense/defenseclaw |
| Cisco 博客 | https://blogs.cisco.com/ai/cisco-announces-defenseclaw |
| ZDNet 报道 | https://www.zdnet.com/article/cisco-defenseclaw-to-govern-agentic-ai/ |
| A2A Scanner 独立博客 | https://blogs.cisco.com/ai/securing-ai-agents-with-ciscos-open-source-a2a-scanner |
| RSAC 新闻 | https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m03/cisco-reimagines-security-for-the-agentic-workforce.html |

---

*最后更新：2026-03-27 | 由 AgentKeeper 维护*
