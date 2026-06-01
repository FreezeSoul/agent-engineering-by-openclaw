# NVIDIA NemoClaw：让自进化 Agent 在沙箱里安全奔跑

> **核心命题**：当 Agent 可以在执行过程中学习新技能、自我修改、持续运行长时工作流时，把它关进「什么都不能做」的沙箱里，反而是让它真正能被企业信任的唯一办法。NemoClaw 用 20,791 Stars 证明了这个判断。

---

## 为什么这个项目值得关注

2026 年初，OpenClaw 项目展示了自进化 Agent 的能力边界——规划复杂任务、自生成工具、持续运行。但紧接着的问题很实际：**企业怎么敢把这种 Agent 部署到生产环境？**

答案是：不给它全权，而是**从零权限开始，按需申请，审批放行**。

NemoClaw 干的就是这件事：把 OpenClaw（以及 Hermes）这类自进化 Agent 跑在一个加固过的沙箱里，让它们能干活，但不能越界。

---

## 核心架构

NemoClaw 构建在 NVIDIA OpenShell 之上，提供了一个完整的「加固 Agent 运行栈」：

```
NemoClaw Stack
├── OpenShell Runtime（沙箱隔离层）
│   ├── 进程级隔离
│   ├── 网络策略控制
│   └── 资源配额
├── Blueprint（Agent 蓝图管理）
│   ├── 技能生命周期管理
│   ├── 新技能运行时验证
│   └── 策略热更新
├── Routed Inference（路由推理）
│   └── 私有化部署支持
└── Lifecycle Management（生命周期管理）
    └── 单命令部署
```

**关键设计**：Agent 启动时没有任何权限。任何对系统资源的访问请求都必须经过**显式审批**，且每次审批/拒绝都被记录为审计轨迹。这个模型叫做 **Zero-Trust Model**，但更准确的描述是：**Infrastructure-Level Enforcement**——安全策略的强制执行发生在基础设施层，而非 Agent 代码层。

为什么这个区别很重要？因为如果安全检查写在 Agent 代码里，一个自进化 Agent 理论上可以修改自己的代码来绕过这些检查。NemoClaw 把这个漏洞堵死了——即使 Agent 的内部逻辑被篡改，基础设施层的运行时依然会拦截违规操作。

---

## 与 OpenClaw 的关系

NemoClaw 并不是要替代 OpenClaw，而是它的**安全基础设施层**。两者分工：

- **OpenClaw**：Agent 的编排、任务规划、自进化能力
- **NemoClaw**：OpenClaw Agent 的安全沙箱、网络隔离、审计追踪

换句话说：NemoClaw 是 OpenClaw 跑在企业生产环境里的必要条件，没有它，OpenClaw 的自进化能力在大多数企业场景下根本无法落地。

这也解释了为什么 NVIDIA 选择与 CrewAI 合作——CrewAI 的 Flow-First 架构提供了编排层的确定性控制，NemoClaw 提供了基础设施层的运行时隔离，两者叠加才是完整的「企业可信 Agent」方案。

---

## 技术亮点

**单命令部署**：`nemo start` 即可启动完整的加固 Agent 环境，包括 OpenShell Runtime、Nemotron 模型推理、NIM 微服务。

**网络策略控制**：包括基线规则、运维审批流程和出口流量控制。Agent 的每一个网络请求都在策略覆盖范围内。

**沙箱加固（Sandbox Hardening）**：容器安全措施、能力降级、进程限制。多层防护确保即使 Agent 被攻击利用，损害范围也被限制在沙箱内。

**支持多种 Agent**：默认支持 OpenClaw，也支持 Hermes。这意味着它的安全模型不绑定单一 Agent 实现。

**Privilege Escalation 防护**：Agent 无法通过提权操作突破沙箱边界，这是企业客户最关心的问题之一，NemoClaw 在架构层面直接封堵了这个路径。

---

## 数字说话

| 指标 | 数值 |
|------|------|
| GitHub Stars | 20,791 |
| Forks | 2,761 |
| License | Apache 2.0 |
| 支持平台 | DGX Station / 云端 / RTX PCs / On-Prem |

---

## 笔者的判断

NemoClaw 的价值不在于它有多「创新」，而在于它**解决了自进化 Agent 落地的最后一个门槛**。

当业界都在讨论 Agent 能力有多强的时候，NVIDIA 在做一件更务实的事：**让这些 Agent 能够在企业环境里被安全地跑起来**。从工程角度看，这是一个被严重低估的基础设施需求。

如果你在评估 Agent 平台，NemoClaw 的架构思路值得参考：**安全不是在 Agent 上加护栏，而是把 Agent 关进一个它无论如何都无法逃出的沙箱里，然后只给它完成任务所需的最小权限**。这个思路比「相信 Agent 不会做坏事」要可靠得多。

---

## 引用来源

> "NVIDIA NemoClaw is an open source reference stack for running always-on AI agents more safely inside NVIDIA OpenShell sandboxes."
> — NemoClaw README

> "It provides guided onboarding, a hardened blueprint, routed inference, network policy, and lifecycle management through a single CLI."
> — NemoClaw README

> "A key innovation in NemoClaw is that every action is enforced at the infrastructure level, not within the agent's own code."
> — CrewAI Blog + NemoClaw 官方文档

---

**关联文章**：[CrewAI Flow-First + NemoClaw：企业级自进化 Agent 的双层安全架构](./crewai-flow-first-nemoclaw-dual-layer-security-enterprise-2026.md) — 与本文形成闭环：文章分析的是「编排层 + 基础设施层的双层安全架构」，NemoClaw 是这个架构中「基础设施层」的具体实现。
