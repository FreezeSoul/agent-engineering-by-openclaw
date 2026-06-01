# microsoft/agent-governance-toolkit：Agent 安全治理的工程化实践

> 来源：[github.com/microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)（Stars: 3,604，v3.7.0，2026-05-18）
>
> 关联文章：[Anthropic 如何在不同产品中构建 Agent Containment 体系](anthropic-how-we-contain-claude-across-products-2026.md)
>
> 核心结论：AGT 将 Agent 安全治理从"prompt 层面的礼貌请求"提升到"应用中间件的确定性策略执行"，通过 Privilege Rings、Saga Orchestration 和 OWASP Agentic Top 10 全面覆盖，为企业 Agent 部署提供工程级安全保障。

---

## 核心命题

Anthropic 的 containment 策略解决的是**基础设施层的访问边界**问题——sandbox、VM、egress control。但一旦 Agent 的请求通过了基础设施检查，进入应用逻辑层，谁来保证它做的是对的事？

AGT 回答的正是这个问题：**在应用中间件层做策略执行，让"坏行为"在技术实现上成为不可能，而不是依赖模型自觉遵守**。

> "Prompt-level safety ('please follow the rules') is not a control surface. It is a polite request to a stochastic system."

这句话与 Anthropic 的判断高度一致——模型层面的约束是概率性的，不是确定性的。要做到真正的安全，必须在应用代码的确定性逻辑中拦截。

---

## 为什么这个项目值得关注

### 1. Privilege Rings：Agent 版的权限分层

AGT 实现了类似操作系统 ring protection 的 Agent 权限分层：

| Ring | 描述 | 隔离程度 |
|------|------|---------|
| Ring 0 | 最高权限：生产数据库写操作 | 最高风险 |
| Ring 1 | 受限写：测试环境、内部服务 | 中高风险 |
| Ring 2 | 只读：数据查询、状态读取 | 低风险 |
| Ring 3 | 外部通信：网络请求、外部 API | 需审计 |

每个工具调用、消息发送和委托都会被拦截器捕获，在模型的意图到达网络之前就经过确定性代码检查。**被 AGT 内核拒绝的动作不是"不太可能"，而是结构上不可能**。

### 2. MCP Security Gateway：工具毒化防御

Anthropic 提到的 External Attackers 类别中，工具毒化是关键攻击向量。AGT 的 MCP Security Gateway 提供了：

- **Tool Poisoning Detection**：检测恶意构造的 MCP 工具响应
- **Drift Monitoring**：监控工具行为偏离预期
- **Typosquatting Detection**：识别恶意仿冒的工具名称
- **Hidden Instruction Scanning**：扫描注入的隐藏指令

这与 Anthropic 的"External Content 防御层"形成了直接的工程对应。

### 3. OWASP Agentic Top 10 全面覆盖

AGT 是目前为数不多的、专门针对 OWASP Agentic AI Top 10 设计完整控制面的开源框架：

| OWASP 风险 | AGT 对应模块 |
|-----------|------------|
| LLM01: Prompt Injection | PromptDefense Evaluator（12向量审计）|
| LLM02: Sensitive Output | Agent OS Policy Engine |
| LLM03: Training Data Poisoning | Agent Compliance |
| LLM04: Model Denial of Service | Agent SRE（SLO + Circuit Breakers）|
| LLM05: Supply Chain | Agent Marketplace（Plugin Governance）|
| ... | ... |

### 4. 与 Anthropic Containment 的闭环

Anthropic 的文章描述了三种隔离模式（Ephemeral Container / HITL Sandbox / VM Perimeter），这些是**基础设施层的硬边界**。但硬边界不能覆盖所有场景——比如两个 Agent 之间的协作请求、跨系统的委托链路。

AGT 的价值在于：**在基础设施层之上，增加了一层应用语义层的安全治理**。当 Agent 需要跨服务协作时，AGT 的 Policy Engine 和 Agent Mesh 接管了基础设施层无法覆盖的信任传递问题。

---

## 快速上手

```bash
# 基础安装
pip install agent-governance-toolkit

# 完整安装（含 SRE/Compliance 模块）
pip install 'agent-governance-toolkit[full]'

# CLI 工具
agt --help
agt policy lint ./my-agent-policy.yaml
agt owasp verify ./my-agent
```

**生产部署建议**：

> "AGT enforces governance at the application middleware layer, not at the OS kernel level. The policy engine and agents share the same process boundary. Production recommendation: Run each agent in a separate container for OS-level isolation."

---

## 笔者判断

AGT 的设计哲学与 Anthropic 的 containment 思路高度一致：**安全不是对模型的请求，而是对系统架构的要求**。

笔者认为，这个项目的核心价值在于：

1. **确定性优于概率性**：Policy Engine 在确定性应用代码中执行，而不是依赖模型层的概率性约束
2. **治理与执行一体化**：不只做检测，而是通过 Saga Orchestration 在执行层强制策略
3. **企业级可审计性**：完整的 Decision BOM（Bill of Materials）审计链，满足 SOC 2 和 EU AI Act 合规要求

**适用场景**：已经在使用 Agent 系统（LangGraph / CrewAI / AutoGen 等），需要企业级安全治理和合规审计的团队。

**不适用场景**：快速原型验证阶段——AGT 的完整安装和策略配置有学习曲线，早期项目可能不需要这个级别的治理复杂度。

---

*引用来源：GitHub README，[microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)，v3.7.0，2026-05-18。*
