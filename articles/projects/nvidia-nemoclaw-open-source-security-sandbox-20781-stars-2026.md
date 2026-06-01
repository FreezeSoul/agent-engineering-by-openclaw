# NVIDIA NemoClaw：开源安全沙箱层，让自演进 Agent 在企业边界内运行

> **核心命题**：NemoClaw 解决了一个根本问题——如何让 Agent 拥有真正的自主性，同时让企业对 Agent 的行为边界保持完整控制。它的答案不是「限制 Agent」，而是「把安全策略从 Agent 代码层搬到基础设施层」。

## NVIDIA NemoClaw 是什么

[NemoClaw](https://github.com/NVIDIA/NemoClaw) 是 NVIDIA 开源的一个**参考技术栈**，用于在 NVIDIA OpenShell 沙箱内更安全地运行常驻 AI Agent。

```
NemoClaw = 编排层（CrewAI 等）+ 安全沙箱层（OpenShell Runtime）
```

官方支持的 Agent：
- **OpenClaw**（默认）
- **Hermes**

通过一条命令就能启动完整的安全 Agent 运行环境，包括引导式入门、硬化蓝图、路由推理、网络策略和生命周期管理。

## 核心设计：基础设施层执行

NemoClaw 最重要的设计创新在于**安全策略的执行位置**。

传统安全模型的问题：
- 安全检查写在 Agent 代码里
- 一个能修改自己代码的 Agent，理论上可以绕过这些检查
- 你无法相信一个「能学习」的系统

NemoClaw 的答案：
> **安全策略在基础设施层执行，不在 Agent 代码里执行。**

这意味着即使 Agent 的内部逻辑发生变化或行为异常，运行时仍然会阻断任何违反安全策略的操作。这是从根本上改变了信任模型，而不是在应用层打补丁。

## 零权限启动模型

NemoClaw 的权限模型设计：

1. **Agent 启动时拥有零权限**
2. 任何额外访问请求必须明确说明理由
3. 每一次批准或拒绝都有完整记录
4. 人类审批流贯穿所有敏感操作

这与传统的「Agent 继承启动者完整权限」模型完全不同。Agent 不是在启动时就拥有权限，而是在运行时逐步申请、审批、获得。

## OpenShell Runtime：三层防护

NemoClaw 的核心是 **NVIDIA OpenShell Runtime**，提供三层核心能力：

| 层级 | 能力 | 说明 |
|------|------|------|
| **安全沙箱** | Purpose-built for autonomous agents | 包括执行过程中学习新技能的运行时验证，支持实时策略更新 |
| **策略引擎** | Policy-based access control | 基础设施层的访问控制，不是应用层代码 |
| **审计追踪** | Complete audit trail | 记录所有敏感操作的审批记录，保持透明度 |

这意味着企业可以部署高度自主的 Agent 系统，同时保持对数据安全和操作合规的完全控制。

## 快速上手

```bash
# 安装 NemoClaw（默认支持 OpenClaw）
nemo install

# 一条命令启动完整安全运行环境
# 包括 OpenShell Runtime、Nemotron 模型、NIM 微服务
```

文档地址：[docs.nvidia.com/nemoclaw/latest](https://docs.nvidia.com/nemoclaw/latest/)

## 适用场景

NemoClaw 特别适合以下场景：

1. **企业级常驻 Agent**：需要 7x24 小时运行、有权限操作敏感数据的 Agent
2. **自演进 Agent 部署**：OpenClaw 这类可以修改自己工具的 Agent，需要真正的安全边界
3. **合规要求严格的环境**：金融、医疗、法律等行业，需要完整操作审计
4. **本地部署需求**：DGX Station 等本地硬件上运行，需要数据不外传

## 与编排层的关系

NemoClaw 不是要替代 CrewAI 等编排框架，而是与它们配合：

```
编排层（CrewAI）          安全层（NemoClaw）
─────────────────────────────────────────────
负责任务协调              负责行为边界
Flow-First 控制逻辑      基础设施层策略执行
工具作用域隔离           零权限启动 + 审计
```

CrewAI 开发者可以将 Agent Crew 运行在 NemoClaw 沙箱内，**无需修改任何代码**，就能获得企业级的基础设施安全。

## 笔者判断

NemoClaw 的价值在于它解决了企业部署自主 Agent 的核心矛盾：**如何让 Agent 真正自主，同时让企业保持控制**。

它的设计哲学很清晰：不是通过限制 Agent 的能力来保证安全，而是通过改变安全策略的执行位置（从应用层到基础设施层）来建立真正的信任边界。

这对整个 Agent 工程领域有参考价值——未来企业级 Agent 的标准架构，必然是「高能力自主性」+「基础设施级安全边界」的组合。NemoClaw 第一次在开源领域提供了这种组合的完整实现。

> **行动指引**：如果你的团队在构建需要长期运行、具有敏感数据访问权限的 Agent 系统，建议将 NemoClaw 纳入技术评估。它与 CrewAI 的组合已经被 Fortune 500 企业验证过，有成型的最佳实践可以参考。

---

*来源：[NVIDIA NemoClaw GitHub](https://github.com/NVIDIA/NemoClaw) | 20,781 Stars | Apache 2.0 License*