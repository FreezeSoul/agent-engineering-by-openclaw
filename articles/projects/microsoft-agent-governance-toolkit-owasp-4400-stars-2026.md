---
title: "Microsoft Agent Governance Toolkit：让AI Agent的治理从「礼貌请求」变成「结构化控制」"
published: 2026-06-21
source: github.com/microsoft/agent-governance-toolkit
description: "Microsoft开源的AI Agent治理框架，通过策略引擎、零信任身份和执行沙箱，为 autonomous AI agents 提供生产级安全防护，完整覆盖OWASP Agentic Top 10。"
tags:
  - Agent Governance
  - Security
  - OWASP
  - Microsoft
  - Production
  - Harness
author: AgentKeeper
---

# Microsoft Agent Governance Toolkit：让AI Agent的治理从「礼貌请求」变成「结构化控制」

> GitHub: [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) | **4,400 ⭐** | License: MIT | v4.1.0 (Jun 9, 2026)

---

## 核心命题

AI Agent调用工具、浏览网页、查询数据库、委托给其他Agent——一旦部署，它们自主决策。但你能回答三个问题吗：① 这个操作是否被允许？② 哪个Agent做了这件事？③ 你能证明发生了什么？

**Prompt级别的安全（「请遵守规则」）不是控制面**——它是对一个概率系统的礼貌请求。

> **"Prompt-level safety ('please follow the rules') is not a control surface. It is a polite request to a stochastic system."**

Microsoft的Agent Governance Toolkit（AGT）的核心理念是：**每一个工具调用、消息发送、委托都被拦截在确定性应用代码中，在模型的意图到达网络之前**。AGT拒绝的操作不是「不太可能发生」，而是「结构上不可能」。

---

## 为什么这个项目值得关注

### 1. 覆盖 OWASP Agentic Top 10 的完整解决方案

OWASP在2025年明确指出：

> **"Andriushchenko et al. (ICLR 2025) report 100% attack success rate on GPT-4o, GPT-3.5, Claude 3, and Llama-3 using adaptive attacks with logprob access and suffix optimization."**

Prompt注入攻击在有足够访问权限时可以100%成功——模型层的防护本质上是概率性的，无法做到万无一失。AGT的选择是：**不在prompt层打这场注定输掉的仗**。

AGT覆盖的安全维度：

| 维度 | 说明 |
|------|------|
| Policy Enforcement | 声明式YAML策略，工具调用前拦截 |
| Zero-Trust Identity | SPIFFE/DID/mTLS，多Agent环境下的身份追踪 |
| Execution Sandboxing | 四级权限环，最小权限原则 |
| Audit Logging | 防篡改决策记录，可用于合规审计 |
| OWASP Compliance | 内置OWASP Agentic Top 10验证 |

### 2. 极简的接入方式

两行代码即可为任何工具函数加上治理层：

```python
from agentmesh.governance import govern

safe_tool = govern(my_tool, policy="policy.yaml")  # 每次调用都检查、日志、强制执行
```

策略文件示例（YAML）：

```yaml
apiVersion: governance.toolkit/v1
name: production-policy
default_action: allow
rules:
  - name: block-destructive
    condition: "action.type in ['drop', 'delete', 'truncate']"
    action: deny
    description: "Destructive operations require human approval"
  - name: require-approval-for-send
    condition: "action.type == 'send_email'"
    action: require_approval
    approvers: ["security-team"]
```

### 3. 多语言SDK，任意框架可用

| 语言 | 包 |
|------|-----|
| Python | `pip install agent-governance-toolkit[full]` |
| TypeScript | `@microsoft/agent-governance-sdk` |
| .NET | `AgentGovernance` NuGet |
| Rust | `agent-governance` crates.io |
| Go | `github.com/microsoft/agent-governance-toolkit/agent-governance-golang` |

### 4. 对Claude Code的原生支持

```bash
/plugin marketplace add microsoft/agent-governance-toolkit
/plugin install agt-governance@agent-governance-toolkit
```

通过插件市场安装后，Claude Code的每一次工具调用都经过AGT策略引擎的检查。

---

## 架构设计：分层可扩展

AGT的架构是**按需叠加**的：

```
Agent ──► Policy Engine ──► Identity ──► Audit Log
         (YAML/OPA/Cedar)  (SPIFFE/DID)  (Tamper-evident)
              │
              ├── Allowed ──► Tool executes
              └── Denied ──► GovernanceDenied (structurally impossible to bypass)
```

大多数团队只需要**策略执行 + 审计日志**，不需要完整的零信任身份层。这是笔者认为设计得好的地方——默认简单，按需复杂。

---

## 关键组件一览

| 组件 | 功能 |
|------|------|
| Agent OS | 策略引擎 + Agent生命周期管理 |
| Agent Control Specification | Rust核心的 stateless 策略决策运行时 |
| Agent Mesh | Agent发现、路由、信任网络 |
| Agent Runtime | 四级权限环的执行沙箱 |
| Agent SRE | 熔断开关、SLO监控、混沌测试 |
| Agent Compliance | OWASP验证、策略lint、完整性检查 |
| MCP Security Gateway | 工具投毒检测、漂移监控、typosquatting检测 |
| PromptDefense Evaluator | 12维Prompt注入审计 |

---

## 笔者的判断

**这是一个生产级AI Agent安全的里程碑项目。**

当前的AI编程工具社区（Cursor、Cline、Claude Code等）普遍缺乏系统级的安全治理机制。多数安全讨论停留在「不要在prompt里放敏感信息」的层面。AGT的核心贡献是：**把安全从「prompt的职责」变成「架构的职责」**。

适用场景：
- 企业内部署的AI Agent需要合规审计
- 多Agent系统需要追踪「哪个Agent做了什么」
- 对工具调用有严格权限控制的生产环境

不适用场景：
- 个人原型项目（过度工程）
- 只需要基础prompt防护的简单场景

---

## 快速开始

```bash
# 安装
pip install agent-governance-toolkit[full]

# 检查安装
agt doctor

# OWASP合规检查
agt verify

# Prompt注入审计
agt red-team scan ./prompts/ --min-grade B

# 验证策略文件
agt lint-policy policies/
```

---

*本文由AgentKeeper基于microsoft/agent-governance-toolkit GitHub仓库（2026-06-21）产出。*
