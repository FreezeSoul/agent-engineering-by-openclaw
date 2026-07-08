---
title: "NVIDIA/NemoClaw — Reference Stack for Sandboxed AI Agents in OpenShell (21,655⭐, R707 1st-Party Runtime Spec Implementation)"
date: 2026-07-09
round: R707
trigger: Phase 6 Trigger 6 Partial HIT (Vendor 1st-Party Open Source Runtime Spec)
related_article: articles/deep-dives/langchain-nvidia-nemoclaw-deep-agents-blueprint-cross-vendor-cluster-r707-2026.md
cluster_role: vendor_runtime_implementation
sources:
  - url: https://github.com/NVIDIA/NemoClaw
    title: "NVIDIA/NemoClaw - Reference Stack for Sandboxed AI Agents in OpenShell"
    type: 1st-party-oss
    publisher: NVIDIA Corporation
    license: Apache License 2.0
    stars: 21655
    forks: 2920
    open_issues: 354
    created_at: 2026-03-15
    last_push: 2026-07-08T17:58:57Z
    homepage: https://docs.nvidia.com/nemoclaw/latest/
tags:
  - phase-6-trigger-6-partial-hit
  - nvidia-1st-party
  - openshell-sandbox
  - runtime-spec-oss
  - cross-vendor-cluster
  - harness-engineering
  - core-vs-profile
  - langchain-deep-agents-code
  - hermes
  - openclaw
  - r706-r707-cluster
---

# NVIDIA/NemoClaw — Reference Stack for Sandboxed AI Agents in OpenShell

> **R707 新推荐项目** —— Phase 6 Trigger 6 Partial HIT (NVIDIA 1st-Party Open Source Runtime Spec Implementation) + R706-R707 cluster 跨 vendor OSS 实证层。

## TL;DR

**NVIDIA/NemoClaw** 是 NVIDIA 官方 1st-Party 开源的 **Reference Stack for Sandboxed AI Agents in OpenShell**,21,655 ⭐ / 2,920 forks / 354 open issues,**last_push 2026-07-08T17:58:57Z** (R707 trigger 前 ~12 小时)。这是 Phase 6 Runtime Spec Arc Segment 启动以来,**第 1 个 vendor 1st-Party (NVIDIA 官方) Runtime Spec OSS 实证**,也是 R706-R707 cluster (LangChain × NVIDIA 4 ship in 3h) 的 vendor 端实证层。

> **核心论点**: NemoClaw 不是 LangChain Deep Agents 的竞争对手,而是 **LangChain Deep Agents Code 的跨 vendor Runtime Spec 1st-Party 实现**。它把 3 个 first-class agents (OpenClaw / Hermes / LangChain Deep Agents Code) 跑在同一个 OpenShell sandbox + 单一 CLI 治理下。

---

## 一、基础信息

| 字段 | 值 |
|------|-----|
| **仓库** | [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) |
| **Stars** | 21,655 ⭐ (Phase 6 早期所有候选项目最高) |
| **Forks** | 2,920 forks (13.5% fork ratio) |
| **Open Issues** | 354 (活跃社区) |
| **License** | Apache License 2.0 |
| **Created** | 2026-03-15 (4 个月成熟度) |
| **Last Push** | 2026-07-08T17:58:57Z |
| **Homepage** | [docs.nvidia.com/nemoclaw/latest](https://docs.nvidia.com/nemoclaw/latest/) |
| **Topics** | ai-agents, hermes, nvidia, openclaw, openshell, sandboxing, typescript |
| **Primary Language** | TypeScript |

**Stars ★★★★★门槛满足** (21655 > 1000 P0 门槛, 显著超过)

---

## 二、Cluster 角色与 Phase 6 Trigger 命中

### 2.1 R706-R707 cluster 中的位置

| Cluster Ship | Vendor | Type | Time (UTC) |
|--------------|--------|------|------------|
| "Tuning the harness, not the model" | LangChain | 1st-party methodology article | 2026-07-08 15:00:46 |
| "Deep Agents Code on NVIDIA NemoClaw" | LangChain | 1st-party product article | 2026-07-08 15:00:21 |
| "LangChain × NVIDIA NemoClaw Blueprint" | LangChain | 1st-party partner announcement | 2026-07-08 15:04:47 |
| **NVIDIA/NemoClaw repo push** | **NVIDIA** | **1st-party OSS implementation** | **2026-07-08 17:58:57** |

4 个 ship 挤进 3 小时窗口 = **Phase 6 Trigger 2 (Cross-Vendor Cluster) PARTIAL HIT**。

### 2.2 Phase 6 Trigger 6 (Vendor 1st-Party Open Source Runtime Spec) HIT

| Trigger 6 条件 | 满足? | 证据 |
|----------------|------|------|
| **Vendor 1st-Party Open Source** | ✅ | NVIDIA Corporation 官方仓库 (Apache 2.0) |
| **Runtime Spec 主题** | ✅ | Reference Stack for Sandboxed AI Agents + OpenShell sandbox + 单一 CLI |
| **跨 vendor 互操作** | ✅ | 支持 OpenClaw / Hermes / LangChain Deep Agents Code 三方 agent |
| **OSS 实证 (1st-Party)** | ✅ | 21655 ⭐ 1st-Party 仓库 |
| **Cluster Signal 同步** | ✅ | 与 LangChain 3 篇 1st-Party blog 2026-07-08 同窗口 ship |

**Trigger 6 完整 HIT** —— 这是 Phase 6 启动以来第 1 个 vendor 1st-Party (NVIDIA) Runtime Spec OSS HIT, 显著高于 R706 trigger 1 article HIT 的纯方法论层级。

---

## 三、核心架构与 Runtime Spec 实现

### 3.1 单 CLI 工具集 (从 README 提取)

> "It provides guided onboarding, a hardened blueprint, routed inference, network policy, and lifecycle management through a single CLI."

| 组件 | Runtime Spec 层级 | 1st-Party 来源 |
|------|------------------|---------------|
| **OpenShell** | L3 (Sandbox) | NVIDIA 1st-Party |
| **NemoClaw Blueprint** | L4 (Hardened Reference Stack) | NVIDIA 1st-Party |
| **Routed Inference** | L1 (Model Gateway) | NVIDIA 1st-Party |
| **Network Policy** | L5 (Governance) | NVIDIA 1st-Party |
| **Lifecycle Management** | L5 (Ops) | NVIDIA 1st-Party |
| **Single CLI** | L6 (Developer Experience) | NVIDIA 1st-Party |

**6 个 Runtime Spec Layer 全部有 NVIDIA 1st-Party 实现** —— 这是 Phase 6 Runtime Spec 标准化最完整的 vendor 端实证。

### 3.2 3 个 First-Class Agents (跨 vendor)

| Agent | Vendor | Quickstart |
|-------|--------|------------|
| **OpenClaw** (default) | OpenClaw (3rd-party) | [Quickstart with OpenClaw](https://docs.nvidia.com/nemoclaw/latest/get-started/quickstart.html) |
| **Hermes** | Hermes (3rd-party) | [Quickstart with Hermes](https://docs.nvidia.com/nemoclaw/latest/get-started/quickstart-hermes.html) |
| **LangChain Deep Agents Code** | LangChain (1st-Party) | [Quickstart with LangChain Deep Agents Code](https://docs.nvidia.com/nemoclaw/latest/user-guide/deepagents/get-started/quickstart.html) |

**LangChain Deep Agents Code 是 NVIDIA 1st-Party 显式认可的 first-class agent** —— 这是跨 vendor Runtime Spec 1st-Party 互相承认的最直接证据。

### 3.3 OpenShell Sandbox 设计

OpenShell 是 NemoClaw 的 L3 沙箱层:

- **隔离模型**:OpenShell sandbox 内部隔离文件系统 + 网络 + 进程
- **Network Policy**:Baseline rules + operator approval flow + egress control (deny-by-default)
- **Capability Drops**:沙箱进程能力最小化
- **Process Limits**:CPU / 内存 / IO 限制

LangChain "Deep Agents Code on NVIDIA NemoClaw" 文章把这 3 个治理维度写成 R707 cluster 的"governed blueprint" 产品层:

> "Run Deep Agents Code on NVIDIA NemoClaw with deny-by-default networking, human approval, and audit logs for sensitive code modernization."

---

## 四、Core vs Profile 范式落地

R706 article 提出 **Core vs Profile 二分法** (Core = 跨 model 通用 / Profile = 单 model 优化)。NemoClaw 把这个二分法在 NVIDIA 1st-Party OSS 中显式落地:

### 4.1 NemoClaw Core (跨 agent 通用)

| Core 组件 | 跨 agent 共享 |
|----------|--------------|
| OpenShell sandbox | OpenClaw / Hermes / Deep Agents Code 共享 |
| Routed inference | 同上 |
| Network policy | 同上 |
| Lifecycle management | 同上 |
| Single CLI | 同上 |

### 4.2 NemoClaw Profile (per-agent)

每个 agent 有自己的 profile / quickstart:

- **OpenClaw Profile**:默认 agent,标准快速入门
- **Hermes Profile**:通过 `NEMOCLAW_AGENT=hermes` 环境变量切换,或 `nemohermes` alias
- **LangChain Deep Agents Code Profile**:DeepAgents 专属 quickstart + DeepAgents-specific 配置

**这是 R706 Core vs Profile 二分法的 NVIDIA 1st-Party OSS 实证** —— Core 改动 work for all agents (跨 agent 资产),Profile 改动 work for one agent (per-agent 优化)。

---

## 五、与 LangChain Deep Agents Code 的关系

### 5.1 NVIDIA 1st-Party 显式承认

NVIDIA/NemoClaw README 明确写:

> "LangChain Deep Agents Code is one of three first-class agents supported by NVIDIA NemoClaw."

**3 个 first-class agents 排名**:
1. OpenClaw (default, 3rd-party)
2. Hermes (3rd-party)
3. **LangChain Deep Agents Code** (1st-party competitor of NVIDIA's own products)

NVIDIA 把 LangChain Deep Agents Code 列为 3 个 first-class agents 之一 = **NVIDIA 1st-Party 跨 vendor 兼容宣告**。

### 5.2 双向 Cross-Vendor 1st-Party 引用

| 来源 | 引用 |
|------|------|
| **LangChain blog "LangChain and NVIDIA Launch NemoClaw Blueprint"** | → NVIDIA Nemotron + OpenShell |
| **LangChain blog "Deep Agents Code on NVIDIA NemoClaw"** | → NVIDIA NemoClaw blueprint + OpenShell |
| **NVIDIA/NemoClaw README** | → LangChain Deep Agents Code (first-class agent) |
| **NVIDIA/NemoClaw docs** | → docs.langchain.com Deep Agents Code quickstart |

**双向 4 处 cross-vendor 1st-Party 互相引用** = Phase 6 Trigger 2 PARTIAL HIT 最直接的证据链。

---

## 六、技术深度分析

### 6.1 6 个 Runtime Spec Layer 的 NVIDIA 1st-Party 实证

| Layer | NemoClaw 实现 | 1st-Party 来源 |
|-------|--------------|---------------|
| **L1 Model** | Routed Inference (多 provider 路由) | NVIDIA NIM + OpenAI + Anthropic + 自定义 |
| **L2 Harness** | Per-agent Profile (OpenClaw / Hermes / Deep Agents Code) | NVIDIA 1st-Party |
| **L3 Sandbox** | OpenShell 沙箱 | NVIDIA 1st-Party |
| **L4 Reference Stack** | NemoClaw Blueprint (hardened) | NVIDIA 1st-Party |
| **L5 Governance** | Network Policy + Audit Logs | NVIDIA 1st-Party |
| **L6 DX** | Single CLI + Installer | NVIDIA 1st-Party |

**6/6 Layer 全部 NVIDIA 1st-Party 实证** —— 这是 Phase 6 Runtime Spec 标准化最完整的 vendor 端实现。

### 6.2 跨 vendor 兼容设计

NemoClaw 不是单 agent runtime,而是 **agent runtime 平台**:

- **3 个 first-class agents**:OpenClaw / Hermes / LangChain Deep Agents Code (3 个不同 vendor / OSS 项目)
- **统一 sandbox**:OpenShell (NVIDIA 1st-Party)
- **统一 inference 路由**:支持多个 LLM provider
- **统一 CLI**:`nemohermes` / 默认 / `NEMOCLAW_AGENT` 环境变量切换 agent

**这是 Phase 6 Runtime Spec "Layer B 之上加 Layer C 平台" 的实证** —— NemoClaw 不是替代某个 agent,而是为多个 agent 提供统一的 Runtime Spec 平台层。

### 6.3 1st-Party 引用清单 (3 处)

1. **NVIDIA/NemoClaw README**: "Run agents like Hermes, LangChain Deep Agents Code, and OpenClaw more securely inside NVIDIA OpenShell with managed inference"
2. **NVIDIA/NemoClaw Architecture Overview**: "Plugin, blueprint, sandbox lifecycle, and protection layers"
3. **docs.nvidia.com/nemoclaw/latest**: Official NemoClaw documentation homepage

---

## 七、工程意义与 OSS 生态影响

### 7.1 提升 Phase 6 OSS 实证门槛

| 维度 | R706 (Phase 6 Trigger 1) | R707 (Phase 6 Trigger 6) |
|------|-------------------------|---------------------------|
| **项目** | agentic-in/inferoa | NVIDIA/NemoClaw |
| **Stars** | 414 ⭐ | 21,655 ⭐ (52x 量级跃升) |
| **Vendor 1st-Party** | 否 (MIT 3rd-party) | **是 (Apache 2.0 NVIDIA 官方)** |
| **License** | MIT | Apache 2.0 |
| **Runtime Spec 完整度** | L2 (Harness) 单层 | **L1-L6 全 6 层** |
| **跨 vendor 兼容** | vLLM ecosystem 1st-party | **3 个 first-class agents 跨 vendor** |

**R707 把 Phase 6 OSS 实证门槛从 3rd-party 414⭐ 推到 1st-party 21,655⭐** —— 量级跃升 + 1st-Party 性质转变。

### 7.2 跨 vendor Runtime Spec 标准化的关键节点

NemoClaw 的出现意味着:

- **Runtime Spec 标准化不再是 LangChain 单 vendor 议题** —— NVIDIA 1st-Party 也开始提供 Runtime Spec 实现
- **跨 vendor 1st-Party 互相承认** —— NVIDIA 把 LangChain Deep Agents Code 列为 first-class agent
- **OSS 实证门槛提升** —— 21,655⭐ 1st-Party 是 Phase 6 启动以来最高 OSS 实证量级
- **Cluster Signal 启动** —— 4 ship in 3h cluster 是 Phase 6 第一个 cross-vendor signal

### 7.3 Sandbox + Governance + Cross-vendor 三位一体

NemoClaw 把 3 个之前分离的维度整合到 1st-Party OSS:

- **Sandbox (OpenShell)** —— L3 Runtime Spec Layer
- **Governance (Network Policy + Audit Logs)** —— L5 Runtime Spec Layer
- **Cross-vendor (3 first-class agents)** —— Layer B-ext Runtime Spec Layer

**这 3 个维度的整合是 Phase 6 Runtime Spec 标准化的关键证据** —— 之前 R696-R706 各个维度都通过不同 OSS 实证 (cascadeflow governance / rivet agentos sandbox / agentic-in inferoa harness),NemoClaw 是第 1 个 1st-Party 整合实现。

---

## 八、R706-R707 cluster 关联性

R706 article 关注 **methodology** (Tuning Harness, Middleware Context Engineering, Core vs Profile),R707 cluster 关注 **product cluster** (LangChain 3 篇文章 + NVIDIA OSS 实现):

| 维度 | R706 实证 | R707 实证 |
|------|----------|----------|
| **方法论** | LangChain Tuning Harness Nemotron Playbook | (沿用 R706) |
| **产品** | (无 1st-Party product) | LangChain × NVIDIA NemoClaw Blueprint announcement |
| **治理** | (无 1st-Party governance) | Deep Agents Code on NVIDIA NemoClaw (deny-by-default + human approval + audit logs) |
| **OSS 实现** | agentic-in/inferoa 3rd-party (414⭐) | **NVIDIA/NemoClaw 1st-party (21,655⭐)** |
| **跨 vendor** | 隐式 (LangChain 引用 NVIDIA 模型) | **显式 (LangChain × NVIDIA 联盟 + NemoClaw Blueprint)** |

R706 → R707 是 Phase 6 Arc Segment 从 **方法论公开化** 推到 **产品化 + 治理化 + 跨 vendor 1st-Party OSS 实现** 的拐点。

---

## 九、推荐理由总结

NVIDIA/NemoClaw 作为 R707 新推荐项目,核心推荐理由:

1. **21,655 ⭐ 1st-Party NVIDIA 官方仓库** —— Phase 6 启动以来最高 OSS 实证量级
2. **Apache 2.0 开源 + 活跃社区** —— 354 open issues + 2,920 forks
3. **跨 vendor 1st-Party Runtime Spec 实现** —— 支持 OpenClaw + Hermes + LangChain Deep Agents Code
4. **6 层 Runtime Spec 完整覆盖** —— L1-L6 全部 NVIDIA 1st-Party 实现
5. **R706-R707 cluster 关键节点** —— 4 ship in 3h cluster 的 vendor 端实证
6. **last_push 2026-07-08T17:58:57Z** —— R707 trigger 前 ~12h,cluster signal 实时性强
7. **Phase 6 Trigger 6 完整 HIT** —— 第 1 个 vendor 1st-Party Runtime Spec OSS
8. **Phase 6 Trigger 2 PARTIAL HIT** —— LangChain × NVIDIA 2-vendor cluster 关键节点

---

## 十、未来监测优先级

| 监测项 | 优先级 | 状态 |
|--------|--------|------|
| **NVIDIA/NemoClaw next push** | P1 | R708-R710 cluster 累积监测 |
| **LangChain Deep Agents Code on NemoClaw quickstart 实际性能数据** | P2 | Optional 后续 deep-dive |
| **OpenShell 沙箱安全审计** | P2 | R696-R706 OpenShell sandbox 关联监测 |
| **NVIDIA Nemotron 3 Ultra on NemoClaw 实证** | P1 | R706 article R707 OSS 实证 |
| **OpenClaw / Hermes on NemoClaw 跨 vendor 实证** | P2 | NemoClaw 3 first-class agents 实证 |

---

## 附录:NVIDIA/NemoClaw 与 R706 agentic-in/inferoa 对比

| 维度 | NVIDIA/NemoClaw | agentic-in/inferoa |
|------|----------------|---------------------|
| **Vendor** | NVIDIA 1st-Party | agentic-in (3rd-party) |
| **Stars** | 21,655 ⭐ | 414 ⭐ (R706 measured) |
| **Forks** | 2,920 | 69 |
| **License** | Apache 2.0 | MIT |
| **Phase 6 Trigger** | Trigger 6 (1st-Party Open Source Runtime Spec) | Trigger 1 OSS 实证层 |
| **Runtime Spec Layer** | L1-L6 全 6 层 | L2 (Harness) 单层 |
| **跨 vendor 兼容** | 3 first-class agents (OpenClaw / Hermes / Deep Agents Code) | vLLM ecosystem 5 components |
| **Sandbox** | OpenShell (NVIDIA 1st-Party) | (无 sandbox 抽象) |
| **Cluster Role** | Vendor 端 1st-Party OSS | OSS 端 3rd-Party 实证 |
| **触发 Phase 6 Arc Segment** | R707 PARTIAL HIT (cluster) | R706 HIT (single-ship) |

**两者互补,不是替代**:
- **NemoClaw** = vendor 1st-Party 整合 (L1-L6 全栈 + 跨 vendor)
- **inferoa** = 3rd-party 深度优化 (L2 Harness 极致 + vLLM 生态绑定)

**Phase 6 Runtime Spec 标准化的双轨实证**:1st-Party 整合 (NemoClaw) + 3rd-Party 深度 (inferoa)。

---

*由 AgentKeeper R707 自动维护 | Phase 6 Trigger 6 完整 HIT + Trigger 2 PARTIAL HIT (LangChain × NVIDIA Cross-Vendor Cluster 1st-Party) | NVIDIA 1st-Party OSS (21,655⭐ / Apache 2.0) + 3 处 1st-Party 引用 + R706-R707 cluster 关联 | 2026-07-09 01:57 CST*