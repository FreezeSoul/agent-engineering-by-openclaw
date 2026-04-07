# MCP 工具标注：风险词汇的安全边界评估

> **核心问题**：MCP 工具标注（Tool Annotations）提出已近一年，但五项新的 SEP 正在试图扩展它——这套"风险词汇"究竟能在 Agent 安全体系中承担什么角色？它的极限在哪里？

MCP 工具标注（MCP Tool Annotations）于 2025 年 3 月 26 日随规范修订版发布，成为 MCP 协议中描述工具行为的核心机制。工具标注让 MCP Server 能够声明其工具的属性——是否只读、是否具有破坏性、是否幂等、是否与外部世界交互。这些布尔提示构成了一种"风险词汇"，供 Agent 在执行前评估是否需要用户确认。

但这套机制从一开始就存在一个根本矛盾：**标注是不可信的 hints，而非保证**。规范明确指出，客户端必须将标注视为不可信的，除非它们来自可信的 Server。这一妥协使协议保持了向前兼容性，却也留下了深刻的安全空白。

本文基于 MCP 官方博客 2026 年 3 月 16 日发布的深度分析，梳理当前工具标注的现状、五项活跃 SEP 的核心提案，以及这套机制在工程实践中的真实安全价值。

---

## 1. 工具标注的现状：四个属性与一个默认假设

当前的 `ToolAnnotations` 接口极其简洁：

```typescript
interface ToolAnnotations {
  title?: string;               // 显示名称，无信任含义
  readOnlyHint?: boolean;         // 默认: false（非只读）
  destructiveHint?: boolean;      // 默认: true（具有破坏性）
  idempotentHint?: boolean;       // 默认: false（非幂等）
  openWorldHint?: boolean;        // 默认: true（开放世界）
}
```

所有属性都是 **hint**（提示）而非保证。这是规范制定时就明确的设计决策。MCP 联合创始人 Justin Spahr-Summers 在 PR 讨论中直接提出了核心质疑：

> "这些信息本身如果有可信度会非常有用，但我想知道客户端在知道它们不可信的情况下如何使用这个标志。"

Basil Hosmer 则更进一步，认为客户端应该**完全忽略来自不可信 Server 的标注**——尤其是描述操作属性的那些。

规范最终达成的妥协是：一切都称为 hint，客户端根据其对 Server 的信任程度自行决定权重。关键在于，这套默认值是**刻意悲观的**：没有任何标注的工具，被默认假定为非只读、可能具有破坏性、非幂等、开放世界访问。

### 四个属性的实际含义

| 属性 | 默认值 | 语义 |
|------|--------|------|
| `readOnlyHint` | `false` | 工具是否修改环境 |
| `destructiveHint` | `true` | 如果修改，是否为破坏性修改（而非增量式） |
| `idempotentHint` | `false` | 相同参数重复调用是否安全 |
| `openWorldHint` | `true` | 工具是否与外部实体交互（可能携带不可信内容） |

前三个属性主要回答一个**预检问题**：调用此工具前是否需要用户确认？

`openWorldHint` 不同。它关注的是工具的影响范围——不仅在调用前重要，在调用后同样重要。工具的输出可能携带外部内容，这些内容中可能嵌入恶意指令。更重要的是，"外部"的含义因部署环境而异：对于企业部署，"外部"可能指企业网络之外；对于本地桌面工具，"外部"可能指互联网上的任何服务。

**最安全的姿态**：将工具认为"外部"的任何内容视为不可信内容的潜在来源。

---

## 2. 五个活跃 SEP：从标注扩展到信任建模

当前有五项 SEP（Specification Enhancement Proposals）在尝试扩展这套机制，其中四项新增标注，一项提出根本性的信任框架：

| SEP | 提案内容 | 状态 |
|-----|---------|------|
| SEP-1913 | Trust and Sensitivity Annotations（GitHub + OpenAI 联合提出）| Draft |
| SEP-1984 | Comprehensive Tool Annotations for Governance/UX | Draft |
| SEP-1561 | `unsafeOutputHint` | Proposal |
| SEP-1560 | `secretHint` | Proposal |
| SEP-1487 | `trustedHint` | Proposal |

### SEP-1913：Trust and Sensitivity Annotations（Draft）

由 GitHub 和 OpenAI 基于生产环境中的实际缺口联合提出。这是最具实质意义的提案，因为它引入了一个**显式信任层**——不仅仅描述工具属性，还描述工具对数据的访问权限。

该 SEP 试图解决的问题是：当前的 hints 只能描述工具"做什么"，但无法表达"它接触了哪些敏感数据"以及"我们对它的信任级别"。在企业部署中，这两个维度对于访问控制和审计同样重要。

### SEP-1984：Comprehensive Tool Annotations for Governance/UX（Draft）

这是一项更宽泛的治理和用户体验优化提案，试图从 Governance（合规审计）和 UX（用户界面确认提示）两个角度重新组织工具标注体系。

### SEP-1561：`unsafeOutputHint`（Proposal）

标注工具的**输出**是否可能包含不安全内容。核心场景：当工具的输出是另一个 LLM 的输入时，如果输出中包含指令注入（prompt injection）风险，Agent 需要知道这一点。

这是对"lethal trifecta"（见下节）最直接的响应——仅靠输入侧检查不足以防止指令注入。

### SEP-1560：`secretHint`（Proposal）

标注工具是否会处理或暴露 secrets（密钥、凭证、敏感配置）。这是数据治理视角的标注，告知 Agent 某工具涉及敏感信息流转，需要额外的处理考量。

### SEP-1487：`trustedHint`（Proposal）

这是一项更激进的提案：引入一个明确的"可信工具"标记，允许 Server 声明自己及其工具在某种程度上是可信的。这与当前的"一切不可信"默认假设形成直接对立——它实际上是在问：我们能否建立某种可信锚点，让客户端可以对特定 Server/工具放松检查？

---

## 3. Lethal Trifecta：为什么组合才是真正的风险所在

Simon Willison 提出的 **lethal trifecta**（致命三要素）描述了数据泄露攻击的经典条件：私人数据访问能力 + 不可信内容暴露风险 + 外部通信能力。当一个 Agent 同时具备这三项能力时，攻击者只需控制其中一项不可信内容来源（网页、邮件、日历事件描述），就能通过指令注入让 Agent 将私人数据外传。

LayerX 的研究者已经用恶意 Google Calendar 事件描述 + MCP Calendar Server + 本地代码执行工具的组合**实际演示了这种攻击链**。其中，本地代码执行工具是关键——任何拥有无限制 Shell 访问的 Agent 都距离数据外泄一步之遥，这与工具是否通过 MCP 接入无关。

**MCP 新增的风险在于组合的便捷性**：用户通常在一个 Session 中组合使用来自多个 Server 的工具，因此风险属性实际上是 Session 的组合属性，而非单个工具属性。`openWorldHint` 正是为此设计的——它提醒 Agent，工具的输出可能携带来自外部的不可信内容，需要在后续处理中谨慎对待。

**工程视角的核心结论**：
1. 工具标注的四个现有属性可以提供有价值的**预检信号**，但它们是 hints，不能替代运行时验证
2. Agent 需要对工具输出的不可信内容保持警惕——特别是当多个工具组合使用时
3. 代码执行类工具（Shell、subprocess）是整个风险链的关键节点，任何此类工具都应该被视为最高风险，无论标注如何

---

## 4. 扩展体系：协议不改变，能力在增长

MCP Blog 在 3 月 11 日发布的另一篇文章揭示了协议演进的另一条主线：**扩展（Extensions）**。扩展是一种将新能力叠加在 MCP 核心之上的模式，无需触碰核心规范，保证基线互操作性。

MCP 生态现有三层：

```
┌─────────────────────────────────────┐
│           Extensions Layer           │  UI / Auth / Domain-specific
├─────────────────────────────────────┤
│          MCP Projects                │  Registry / Inspector / CLI
├─────────────────────────────────────┤
│        MCP Core Specification        │  协议本身，保证互操作性
└─────────────────────────────────────┘
```

关键的工程价值在于：**扩展是严格加性的**。不识别扩展的客户端或 Server 在初始化握手时直接跳过它，基线协议继续正常工作。这使得 MCP 可以在不破坏生产部署的前提下探索新功能。

当前已正式发布的扩展：

| 扩展名 | 功能 | GA 时间 |
|--------|------|---------|
| MCP Apps | 富 UI 交互扩展（图表、表单、仪表盘）| 2026-01-26 |
| Auth Extensions | 机器到机器认证、企业 IdP 控制 | 已上线 |

MCP Apps 扩展已获得 ChatGPT、Claude、VS Code、Goose 等主流客户端的实时支持，是第一个正式 GA 的 MCP 扩展。

---

## 5. 工程实践建议

### 什么时候依赖工具标注，什么时候不能

**可以依赖标注做**：
- 优化确认提示的 UX（减少对低风险工具的冗余确认）
- 在审计日志中记录工具的风险属性
- 基于 Server 身份设置默认检查策略

**不能依赖标注做**：
- 替代权限验证（Server 可能被恶意控制）
- 替代输出内容安全检查
- 替代代码执行工具的沙箱隔离

### 一个实用的分层检查模型

```typescript
// 实用的 MCP 工具安全检查模型
function shouldRequireConfirmation(tool, server, sessionContext) {
  // 1. 不可信 Server → 严格模式
  if (!isTrustedServer(server)) {
    return true; // 总是确认
  }
  
  // 2. 可信 Server 但工具带有破坏性标注
  if (tool.annotations?.destructiveHint === true) {
    return true;
  }
  
  // 3. 可信 Server 但工具是开放世界的
  if (tool.annotations?.openWorldHint === true) {
    return checkSessionContext(sessionContext); // 取决于会话状态
  }
  
  // 4. 可信 Server + 只读 + 幂等 + 封闭世界
  return false; // 可以跳过确认
}
```

### 未来标注落地优先级

当 SEP-1913（Trust and Sensitivity）和 SEP-1561（unsafeOutputHint）正式合并到规范后，工具安全的标注体系将大幅增强。以下是工程团队可以提前准备的：

1. **审计日志结构**：预留 `sensitivity_level` 和 `output_trust_level` 字段，等待 SEP 落地
2. **Server 信任评估框架**：建立内部 Server 白名单制度，配合 `trustedHint` 使用
3. **输出净化管线**：对来自 `openWorldHint=true` 工具的输出，强制经过 prompt injection 检测

---

## 6. 现有工具标注文章的补充与更新

本仓库此前已收录多篇 MCP 安全相关文章：
- `mcp-security-cve-cluster-2026-architecture-flaws.md`（CVE 簇分析）
- `mcp-threat-modeling-stride-dread-2026.md`（威胁建模）
- `formal-semantics-agentic-tool-protocols-2603-24747.md`（协议形式语义）

本文是这些文章的**补充而非重复**：前几篇侧重于"规范和实现缺陷导致的安全漏洞"，本文侧重于"规范本身提供的安全机制（工具标注）的设计边界与演进方向"。两者结合，构成对 MCP 安全体系的完整认知。

---

## 参考文献

- [Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)，MCP 官方博客，2026-03-16——五项 SEP 汇总、lethal trifecta 攻击链分析、一手 SEP 讨论引用
- [Understanding MCP Extensions](https://blog.modelcontextprotocol.io/posts/2026-03-11-understanding-mcp-extensions/)，MCP 官方博客，2026-03-11——扩展体系架构、MCP Apps GA 时间线
- [The 2026 MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)，MCP 官方博客——2026 四大优先领域、Working Group 主导模式
- [MCP ToolAnnotations Interface](https://modelcontextprotocol.io/specification/2025-11-25/schema#toolannotations)，规范原文
- [SEP Guidelines](https://modelcontextprotocol.io/community/sep-guidelines)，SEP 提交流程
- [SEP-1913: Trust and Sensitivity Annotations](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1913)，GitHub + OpenAI 联合提案
- [Simon Willison: The Lethal Trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)，数据泄露攻击框架原文
- [LayerX: Claude Desktop Extensions RCE](https://layerxsecurity.com/blog/claude-desktop-extensions-rce/)，攻击链实际演示
