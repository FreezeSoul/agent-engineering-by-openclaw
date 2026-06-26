# Microsoft AGT：让 Agent 治理从"请遵守"变成"做不到"

**Stars**：4,519 | **License**：MIT | **来源**：GitHub Trending（2026-06-26 推送）

---

## 核心命题

AI Agent 部署到生产环境后，企业面临三个灵魂拷问：**这个操作是否被允许？哪个 Agent 做的？你能证明吗？**

传统方案给 Agent 的只是"请遵守规则"的礼貌请求。Microsoft Agent Governance Toolkit（AGT）的核心判断是：**Prompt 层面的安全是概率性防护，结构性安全必须发生在应用层中间件，且动作在到达模型之前就被拦截**。

> "AGT does not try to win that fight inside the prompt. Every tool call, message send, and delegation is intercepted in deterministic application code *before* the model's intent reaches the wire. Actions the AGT kernel denies are not 'unlikely.' They are **structurally impossible**." — README.md

---

## 为什么这比 Guardrails 更根本

社区常见的 Agent 安全方案（如 Guardrails、Pydantic Validation）是**请求层过滤**——在 Prompt 之后、模型输出之后做检查，本质上仍然是"请不要这样做"。

AGT 的架构差异在于**确定性执行**：它把治理逻辑放在应用中间件层，在模型意图到达网络层之前就拦截非法操作。这不是"减少概率"，而是"结构上不可能发生"。

| 维度 | 传统 Guardrails | AGT |
|------|----------------|-----|
| 执行位置 | Prompt/Output 层 | 应用中间件层 |
| 执行确定性 | 概率性（模型可能绕过）| 确定性（代码拦截）|
| 覆盖范围 | 输入/输出过滤 | 工具调用、消息发送、委托 |
| 治理证据 | 依赖日志推断 | 每次决策有完整策略记录 |

---

## 核心能力：三层治理架构

### 1. Policy Engine（政策引擎）

```python
from agentmesh.governance import govern

safe_tool = govern(my_tool, policy="policy.yaml")  # 每次调用都被检查、记录、执行
```

通过 YAML 配置文件定义细粒度策略：哪个 Agent 可以调用哪个工具，在什么条件下允许。策略变更无需修改 Agent 代码。

### 2. Identity（身份层）

多 Agent 系统常出现"五个 Agent 共享一个 API key"的情况，出问题后只知道"某个 Agent 干的"。AGT 通过**可验证身份层**确保每个操作的执行者身份可追溯。

### 3. Sandboxing（沙箱执行）

工具调用在隔离环境中执行，结合 OS-level 容器隔离，实现真正的故障边界。

---

## 合规性：企业级刚需

AGT 最大的差异化价值在于**系统性合规覆盖**：

| 标准 | AGT 覆盖情况 |
|------|-------------|
| **OWASP Agentic AI Top 10** | 10/10 ASI 风险类别全映射，确定性控制 |
| **EU AI Act** | 合规映射 + 自动化证据生成 |
| **NIST AI RMF 1.0** | GOVERN/MAP/MEASURE/MANAGE 全对齐 |
| **SOC 2** | 控制映射 + 审计日志导出 |
| **AARM Extended** | R1–R9 全部满足（2026-06-14 第三方验证）|
| **ATF** | 5个元素全映射：Agent Mesh/Agent OS/Agent Compliance/Agent Runtime/Agent SRE |

> "Microsoft's own AI Red Teaming Agent formalizes **Attack Success Rate (ASR)**, the rate of policy violations under adversarial input, as the canonical metric for this class of failure." — README.md

---

## 工程成熟度

一个发布两周左右的开源项目，已有：

- **992 个一致性测试**，确保代码与规范持续对齐
- **29 个 Architecture Decision Records**（ADR），每个决策都有据可查
- **多语言 SDK**：Python（PyPI）+ TypeScript（npm）+ NuGet（C#）+ Rust（crates.io）
- **VS Code 插件**，开发时即可验证策略合规性
- **60+ 教程文档**，覆盖快速入门到生产部署

这远超一般概念型开源项目的成熟度，说明 Microsoft 对此有明确的工程承诺。

---

## 笔者的判断

**AGT 的价值在于把"合规"从运营负担变成工程内置能力。**

传统的 Agent 安全是企业需要在部署后再叠加的治理层，需要专门的合规团队手动维护策略文档、导出审计日志。AGT 的思路是把治理变成 Agent 开发工作流的一部分——策略即代码，测试即合规，部署即验证。

笔者认为，这个方向代表了企业 Agent 平台的下一个必经阶段：Agent Framework 提供执行能力，AGT 这类治理工具提供**生产级信任基础设施**，两者组合才能让企业真正放心地把关键任务交给 Agent。

**适合场景**：已在生产环境运行多个 Agent、需要满足合规要求（金融、医疗、政府、跨国企业）、需要对 Agent 操作有完整审计追溯能力的团队。

---

## 如何使用

**安装**：
```bash
pip install agent-governance-toolkit[full]
```

**Claude Code 集成**：
```text
/plugin marketplace add microsoft/agent-governance-toolkit
/plugin install agt-governance@agent-governance-toolkit
```

**文档**：[microsoft.github.io/agent-governance-toolkit](https://microsoft.github.io/agent-governance-toolkit/) | **Discord**：加入社区获取支持

---

**相关阅读**：
- [OWASP Agentic AI Top 10](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — Agent 安全风险分类标准
- [AARM Extended](https://aarm.dev/builders/agent-governance-toolkit-microsoft) — 第三方合规验证报告