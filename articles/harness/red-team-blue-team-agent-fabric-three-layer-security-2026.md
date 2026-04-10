# Red Team/Blue Team Agent Fabric：AI Agent 安全测试的三层架构

> 本文解读 msaleme/red-team-blue-team-agent-fabric（440 测试，31 模块，Apache 2.0），重点分析其提出的 Protocol Integrity / Operational Governance / Decision Governance 三层安全架构，以及它在 OWASP ASI、NIST AI 800-2、AIUC-1 三大标准体系下的定位。

---

## 核心问题：为什么现有的 Agent 安全工具都在做静态扫描？

大多数 Agent 安全工具的思路是：**拿着配置文件扫模式**。

- Invariant MCP-Scan：扫描已安装的 MCP 配置文件，检查工具描述是否有毒
- Cisco MCP Scanner：用 YARA 规则 + LLM-as-judge 检测恶意工具
- Snyk Agent Scan：扫描 agent 配置文件里的 MCP/skill 安全问题
- NVIDIA Garak：探测 LLM 模型的固有漏洞（prompt injection、幻觉等）

这些工具解决的问题是：**"这个配置/模型有没有已知问题？"**

但它们无法回答的问题是：**"这个 agent 在运行时，能不能被攻击者实际操纵？"**

MCP-Scan 告诉你工具描述里有可疑词汇，但不会尝试通过 JSON-RPC 注入payload来劫持会话。Garak 探测模型层的 jailbreak 抗性，但不会测试 A2A 协议层面的消息伪造。**配置干净不等于运行时安全。**

Red Team/Blue Team Agent Fabric 解决的就是这个 gap：不是静态分析，而是**主动发起协议层攻击**，在 Wire 层面验证 agent 的安全边界是否真实有效。

---

## 三层安全架构：从协议到决策

这套框架提出的核心贡献是一个三层安全模型，覆盖 agent 系统从网络层到决策层的完整攻击面：

| 层次 | 攻击面 | 回答的核心问题 |
|------|--------|--------------|
| **Protocol Integrity** | MCP / A2A / L402 / x402 Wire 层 | 攻击者能否通过协议劫持、 replay 或降级来欺骗 agent？ |
| **Operational Governance** | 会话状态、能力边界、信任链、执行上下文 | agent 是否在授权范围内操作？能否被诱导超越自己的能力边界？ |
| **Decision Governance** | 自主权限、置信度边界、策略约束、行为漂移 | agent 在高风险决策时是否遵守策略？能否被"正常化偏差"（normalization of deviance）逐步拖入不安全行为？ |

### 第一层：Protocol Integrity — 协议层 Wire 攻击

这一层测试的是 agent 通信协议的底层安全性，核心威胁模型基于 **STRIDE**（Spoofing、Tampering、Repudiation、Information Disclosure、Denial of Service、Elevation of Privilege）。

**测试范围：**

| 协议 | 测试数量 | 攻击类型 |
|------|---------|---------|
| MCP | 14 | JSON-RPC 2.0 注入、工具注册劫持、能力扩展 |
| A2A | 13 | 消息伪造、任务劫持、跨会话污染 |
| L402/x402 | 85 | 未授权支付执行、金额溢出、 facilitator 欺骗 |

典型测试场景：
- **MCP-003**：通过 `initialize` 握手注入额外 capability，测试 agent 是否接受未授权的能力提升
- **A2A-007**：伪造其他 agent 的身份发送任务消息，测试目标 agent 是否验证发送方身份
- **x402-020**：在 `Payment-Required` 响应后直接重放有效 token，测试是否实现了 idempotency

> 笔者注：L402 是 Lightning Network 的 HTTP 认证协议（基于 macaroon），x402 是 Coinbase/Cloudflare 推出的 HTTP 402 稳定币支付协议。两者在 Wire 层有相似的重放和伪造攻击面，但 L402 测试的是身份认证，x402 测试的是支付完整性。

### 第二层：Operational Governance — 操作层能力边界

这一层测试 agent 在**运行时的能力边界 enforcement**。即使协议层安全，攻击者仍可能通过社会工程或上下文操纵诱导 agent 执行超出授权范围的操作。

**测试维度：**

| 维度 | 测试数量 | 核心威胁 |
|------|---------|---------|
| Capability Escalation | 17 | 工具调用是否严格限制在授权集内 |
| Session State Manipulation | 12 | 会话状态能否被攻击者篡改 |
| Trust Chain Validation | 9 | agent 是否验证上下游 agent 的身份和授权链 |
| Platform Action Scope | 25 (Tier 1) + 27 (Tier 2) | 云平台 API 调用边界是否正确执行 |

关键概念：**Capability Boundary Enforcement**。在 MCP 层，一个 agent 可能被授权调用 `read_file` 但不能调用 `exec_command`。Operational Governance 层测试的是：当攻击者通过 prompt injection 或上下文污染尝试触发 `exec_command` 时，agent 的 enforcement 机制是否真实生效。

### 第三层：Decision Governance — 决策层行为安全

这是最独特的一层，也是现有安全工具几乎完全忽略的一层。

**核心问题**：即使一个 agent 协议安全、能力边界清晰，它仍然可能在长期运行中逐步偏离安全策略——这是 **normalization of deviance**（正常化偏差）现象。

> Normalization of deviance：每次小幅度违反安全策略，如果不被制止，系统会逐渐将违规行为视为"正常"。对于长期运行的自主 agent，这是最大的隐性风险。

**测试模块：**

| 模块 | 测试数量 | 测试内容 |
|------|---------|---------|
| Autonomy Scoring | 8 | agent 在无人工审批情况下的自主决策范围 |
| Scope Creep Detection | 7 | 任务边界逐步扩展的检测能力 |
| Return Channel Poisoning | 6 | 上游反馈被污染时的行为 |
| GTG-1002 APT Simulation | 17 | 模拟国家级 APT 的完整攻击链（横向移动 → 权限维持 → 数据外泄）|

GTG-1002（Grey Threat Group 1002）是一个 17 步的完整攻击campaign，模拟 AI-Orchestrated Cyber Espionage（AI 编排的网络间谍活动），测试框架能否检测和阻止多步骤的 AI 辅助攻击。

**5 篇同行评审论文支撑此架构：**

| 论文 | DOI | 核心贡献 |
|------|-----|---------|
| Constitutional Self-Governance for Autonomous AI Agents | 10.5281/zenodo.19162104 | 12 种治理机制，77 天生产数据，56 agents |
| Detecting Normalization of Deviance in Multi-Agent Systems | 10.5281/zenodo.19195516 | 首次实证证明自动化 harness 能检测行为漂移 |
| Decision Load Index (DLI) | 10.5281/zenodo.18217577 | 量化 agent 监督认知负担的框架 |
| Normalization of Deviance in Autonomous Agent Systems | 10.5281/zenodo.15105866 | 行为漂移模式的形式化研究 |
| Cognitive Style Governance for Multi-Agent Deployments | 10.5281/zenodo.15106553 | 多 agent 部署中的认知风格治理 |

---

## 与现有安全工具的差异

这是理解这个框架定位的关键：**它不替代静态扫描，而是补充动态攻击测试**。

| 能力 | Invariant MCP-Scan | Cisco MCP Scanner | Snyk Agent Scan | NVIDIA Garak | **本框架** |
|------|-------------------|-------------------|----------------|--------------|-----------|
| **方法** | 静态配置分析 | YARA + LLM 分类 | 配置文件扫描 | 模型层探测 | **主动协议攻击** |
| **MCP 覆盖** | 工具描述检查 | YARA 规则 | 配置文件 | — | **14 真实 JSON-RPC 攻击** |
| **A2A 覆盖** | — | — | — | — | **13 协议级测试** |
| **L402/x402** | — | — | — | — | **85 支付协议测试** |
| **APT 模拟** | — | — | — | — | **GTG-1002（17 步）** |
| **AIUC-1 对齐** | — | — | — | — | **19/20 可测试需求** |
| **测试总数** | 模式匹配 | YARA 规则 | 配置检查 | 模型探测 | **440 主动测试** |

**正确的使用姿势**：先用 MCP-Scan 或 Cisco Scanner 做静态检查（快速、低成本），再用本框架做动态攻击测试（真实攻击模拟）。两个工具互补，缺一不可。

---

## 三大标准体系下的定位

### 1. OWASP Top 10 for Agentic Applications (ASI01-ASI10)

本框架对 OWASP ASI 的覆盖是**完整的**：所有 10 个类别都有对应的测试场景。相比之下，NVIDIA Garak 只覆盖 OWASP LLM Top 10 中的部分类别，且覆盖的是模型层而非协议层。

### 2. NIST AI 800-2（自动基准评估实践，2026 年 1 月）

框架的评估方法论严格遵循 NIST AI 800-2 的三阶段结构（定义评估目标 → 实施运行评估 → 分析报告结果），并采用了该标准要求的所有 9 项实践。

关键设计决策：
- **Comparability**：测试 ID 固定，payload 确定性，版本化管理，跨部署结果可直接对比
- **External validity**：攻击模式来自 InfraGard 威胁情报和 OWASP 事件报告，不是合成的玩具场景
- **Cost control**：每个测试 <15 秒，完整 440 测试套件 <30 分钟，无需 GPU

### 3. AIUC-1（2026 Q1，AI Agent 首个安全/安全/可靠性标准）

AIUC-1 由 MITRE、Stanford、MIT、Orrick 联合构建，目标是回答企业最核心的问题：**"我们能信任这个 AI agent 吗？"**

本框架提供 **AIUC-1 认证前的对抗性测试**，覆盖 19/20 个可测试需求：

| AIUC-1 原则 | 覆盖 | 亮点 |
|------------|------|------|
| B. Security | **4/4 (100%)** | 430 测试覆盖 4 种 Wire 协议 |
| D. Reliability | **2/2 (100%)** | 工具调用测试横跨 4 协议 + 45 平台 |
| C. Safety | **6/6 (100%)** | CBRN 预防、有害输出检测、部署前测试 |
| A. Data & Privacy | 2/5 (40%) | 数据访问边界、IP 泄露防护 |
| E. Accountability | **5/7 (71%)** | 事件响应、供应商评估、审计证据 |
| F. Society | **2/2 (100%)** | GTG-1002 APT 模拟 + CBRN 预防 |

未覆盖的 3 个需求（A001、A002、E005）属于**流程性要求**（输入数据策略、输出数据策略、云端 vs 本地评估），无法通过自动化测试覆盖。

---

## 工程实践：如何将安全测试集成到开发流程

### 快速开始

```bash
pip install agent-security-harness

# 测试 MCP server
agent-security test mcp --url http://localhost:8080/mcp

# 测试 x402 支付端点
agent-security test x402 --url https://your-x402-endpoint.com
```

### MCP Server 模式：让 AI Agent 主动触发安全测试

框架提供 MCP Server 接口（`agent-security harness serve --port 8081`），允许任意 AI agent 通过 MCP 协议直接调用安全测试。这是一个独特的能力：agent 可以在**执行关键操作前主动验证目标系统的安全边界**。

```
# agent 决定调用外部工具前，先触发 MCP server 模式的安全测试
1. agent 判断需要调用外部 MCP server
2. 通过 MCP 协议向 agent-security-harness 发送测试请求
3. harness 执行目标 server 的协议攻击测试
4. 返回测试结果（PASS/FAIL + 详情）
5. agent 根据测试结果决定是否继续操作
```

这实现了安全测试的**左移**（Shift Left）：从部署后审计变为执行前验证。

### CI/CD 集成

```yaml
# GitHub Action 示例
- name: Agent Security Harness
  run: |
    pip install agent-security-harness
    agent-security test mcp --url ${{ env.MCP_SERVER_URL }} \
      --report report.json --ci
    # 设置退出码：测试失败则流水线失败
```

### 统计模式：单次测试不够，需要多次运行

```bash
agent-security test mcp --url http://localhost:8080/mcp \
  --trials 5 --confidence 0.95
```

单次测试无法排除随机性。`--trials N` 模式执行 N 次测试并计算 Wilson 置信区间，确保结果具有统计意义。

---

## 已知局限

1. **测试覆盖不等于安全**：440 个测试全部 PASS，不等于系统"安全"——它只说明这些特定攻击向量无效。真正的安全需要架构层面的纵深防御。
2. **x402/L402 端点依赖 facilitator**：部分 x402 测试依赖链上验证服务（facilitator），测试环境中需要 mock facilitator 的行为。
3. **GTP-1002 APT 模拟的伦理边界**：17 步完整攻击链模拟需要隔离的测试环境，不应在生产环境直接运行。
4. **协议版本漂移风险**：MCP、A2A 规范仍在活跃演进，测试套件需要随规范更新而更新（v3.10 对应 MCP 规范 ~2026-03）。

---

## 与仓库现有文章的关系

本篇文章补充了仓库内 **harness 章节** 的核心缺失：

- 现有的 `owasp-top-10-agentic-applications-2026.md` 描述了 OWASP ASI 的 10 个威胁类别，但没有说明**如何用自动化工具系统性地测试这些威胁**
- 现有的 `mcp-security-cve-cluster-2026-architecture-flaws.md` 聚焦架构缺陷的 CVE 分析，本篇聚焦**动态攻击测试框架**
- 现有的 `agent-harness-engineering.md` 和 `harness-engineering-deep-dive.md` 描述了 harness 工程的一般原则，本篇提供了一个**具体的、可安装的、生产可用的测试框架**

---

## 一句话总结

> Red Team/Blue Team Agent Fabric 填补了 Agent 安全从"静态配置检查"到"主动协议攻击测试"之间的 gap：440 个 Wire 层攻击测试，用 NIST AI 800-2 方法论评估 AIUC-1 和 OWASP ASI 的覆盖缺口，让企业在部署前真正验证 agent 的安全边界。

---

## 参考文献

- [Agent Security Harness (PyPI)](https://pypi.org/project/agent-security-harness/) — 官方分发地址
- [msaleme/red-team-blue-team-agent-fabric (GitHub)](https://github.com/msaleme/red-team-blue-team-agent-fabric) — 源码 + 文档
- [AIUC-1 官网](https://www.aiuc-1.com/) — 标准主页
- [NIST AI 800-2 (DOI: 10.6028/NIST.AI.800-2.ipd)](https://doi.org/10.6028/NIST.AI.800-2.ipd) — 评估方法论依据
- [OWASP Top 10 for Agentic Applications 2026](https://owasp.org/www-project-top-10-for-agentic-applications/) — 威胁模型
- [x402 Protocol — HTTP 402 Payment Protocol](https://www.x402.org/) — 支付协议规范
- [Constitutional Self-Governance for Autonomous AI Agents (10.5281/zenodo.19162104)](https://doi.org/10.5281/zenodo.19162104) — 治理机制理论支撑
- [Detecting Normalization of Deviance (10.5281/zenodo.19195516)](https://doi.org/10.5281/zenodo.19195516) — 行为漂移检测实证研究
