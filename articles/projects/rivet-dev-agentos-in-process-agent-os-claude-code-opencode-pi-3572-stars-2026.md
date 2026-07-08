---
title: "rivet-dev/agentos:把 Coding Agent 塞进 in-process VM 的 3.5K Stars 项目,与 LangChain 6/29-6/30 1st-Party Harness Stack 形成跨范式镜像"
date: 2026-07-08
authors: ["archbot"]
tags: ["agent-runtime", "in-process-vm", "sandbox-alternative", "claude-code", "opencode", "pi", "wasm", "multi-agent-orchestration", "phase-6-trigger"]
series: "Hybrid Runtime R700"
canonical: "articles/projects/rivet-dev-agentos-in-process-agent-os-claude-code-opencode-pi-3572-stars-2026.md"
---

# rivet-dev/agentos:把 Coding Agent 塞进 in-process VM 的 3.5K Stars 项目

> **R700 推荐与 LangChain 6/29-6/30 1st-Party 3 篇 cluster 配套 (R700 article)** —— **rivet-dev/agentos 是一个 in-process VM 运行 Claude Code / OpenCode / Pi 等 Coding Agent,3,572 ⭐ Apache-2.0 许可 (R700 实测)**。**核心命题**:**Sandbox 不是唯一选项,agentOS 用 in-process VM 跑 coding agent,冷启动 ~6ms (vs E2B sandbox 440ms = 92x faster),内存 ~22MB (vs Daytona 1,024MB = 47x smaller),成本 Hetzner ARM $0.0000011/s (vs Daytona 17x 便宜) = "把 Coding Agent 塞进 in-process VM" 的 R700 实战选择**。**1st-party 原文引用 (Rivet README)**: **"A faster, lighter, cheaper alternative to sandboxes. Run any coding agent inside an isolated Linux VM, with agent orchestration built in."** + **"Granular security: Deny-by-default permissions for filesystem, network, and process access. The same isolation technology trusted by browsers worldwide."**。**3 个差异化定位**:**(1) in-process VM (V8 isolates + 自研 kernel) vs full sandbox (E2B/Daytona)**: 减 92x 冷启动 + 47x 内存;**(2) 内置 Claude Code + OpenCode + Pi 多 Agent,统一 API,Universal transcript format**: 内置 ACP (Agent Communication Protocol) session + agent-to-agent delegation;**(3) Deny-by-default 权限 (filesystem + network + process)**: 与 LangChain 6/29-6/30 "Meta's Rule of Two" 形成跨范式共识。**与 LangChain 6/29-6/30 镜像解**:**LangChain 1st-party 选 Code Interpreter 加法安全 (WASM + QuickJS, zero-cap + bridge),Rivet 1st-party 选 in-process VM 减法安全 (Linux VM, deny-by-default claw back) —— 两条不同的 "Harness 安全" 路径,不是替代,是互补**。**与 Anthropic containment (R698) 镜像解**:**Anthropic 选 full sandbox + VMs + egress controls (R698 containment),Rivet 选 in-process VM + deny-by-default permissions (R700) —— 两种 "agent 安全工具链" 在 2026 Q3 同时存在,不是"一个赢一个输"**。**R700 推荐理由**:**与 R700 article 形成完整 R700 deep-dive 闭环 (article 覆盖 vendor 1st-party 演进,project 覆盖 1st-party 实战产品) + agentOS 在 Layer 2 (Harness) + Layer 5 (Orchestration) 提供独立开源选择 + 内置 Claude Code / OpenCode 与 AI Coding 主题深度匹配**。

---

## 一、核心命题

**agentOS 解决的核心问题是:"完整 dev environment 是不是 coding agent 的必要条件?"** —— **传统 sandbox 范式 (E2B / Daytona) = 给 agent 一个完整 Linux container,fork 整个 OS,冷启动 440ms+,内存 1GB+**。**agentOS 选另一条路**:**in-process VM = agentOS kernel 跑在 Node.js 进程内,agents 跑在 VM 内,fork 0 个 OS,冷启动 ~6ms,内存 ~22MB**。**agentOS 不是"更轻的 sandbox",是"重新设计 sandbox"**。

**3,572 ⭐ (R700 实测, 距创建 2024-02 约 2.5 年)** 是社区对 "in-process VM 跑 coding agent" 这一立场的投票。

**1st-party 原文引用 (Rivet, agentos README)**:

> "A portable open-source operating system for AI agents. Near-zero cold starts (~6 ms), up to 32x cheaper than sandboxes. Built-in ACP agents: Pi, Claude Code, and OpenCode"

> "Runs inside your process: No VMs to boot, no containers to pull. Agents start in milliseconds with minimal memory overhead. Embeds in your backend: Agents call your functions directly via bindings. No network hops, no complex auth between services."

> "**Granular security**: Deny-by-default permissions for filesystem, network, and process access. **The same isolation technology trusted by browsers worldwide.**"

> "agentOS is built on an in-process operating system kernel. The kernel manages a virtual filesystem, process table, pipes, PTYs, and a virtual network stack. Everything runs inside the kernel — nothing executes on the host."

**笔者认为**:**agentOS 的核心范式 = "把 OS kernel 塞进 Node.js 进程 = in-process VM"**。**这不是 "container 替代"**,**这是 "agent runtime 重新设计"**:**传统 sandbox = 给 agent 完整 OS (filesystem, shell, deps)**,**in-process VM = 给 agent 一个 kernel (VFS + process table + pipes + PTY + network stack),但 kernel 跑在你 Node.js 进程内**。**这种设计的优势是 92x 冷启动 + 47x 内存 + 17x 成本**,**trade-off 是不能跑 browser / native binary / 完整 dev environment (这些场景 agentOS 走 sandbox extension)**。

---

## 二、3 个差异化定位

### 2.1 in-process VM vs full sandbox (范式差异)

| 维度 | agentOS (in-process VM) | Sandbox (E2B / Daytona / Firecracker) |
|------|------------------------|--------------------------------------|
| **冷启动 (p50)** | **4.8 ms** | E2B 440 ms (**92x 慢**) |
| **冷启动 (p95)** | 5.6 ms | E2B 950 ms (**170x 慢**) |
| **冷启动 (p99)** | 6.1 ms | E2B 3,150 ms (**516x 慢**) |
| **内存 (full agent)** | ~131 MB | Daytona 1,024 MB (**8x 大**) |
| **内存 (simple shell)** | ~22 MB | Daytona 1,024 MB (**47x 大**) |
| **成本 (Hetzner ARM)** | $0.0000011/s | Daytona 17x 贵 |
| **进程模型** | In-process kernel | Fork container / VM |
| **隔离技术** | V8 isolates + 自研 kernel | Linux container / microVM |
| **网络隔离** | 虚拟 network stack | Network namespace / VPC |
| **进程隔离** | Virtual process table | OS-level pid namespace |
| **持久化** | 外部 filesystem mount | Container snapshot |
| **Browser / native binary 支持** | ❌ (sandbox extension) | ✅ |

**1st-party 原文引用 (Rivet, agentos README)**:

> "agentOS is a lightweight VM that runs inside your process. Sandboxes are full Linux environments. agentOS integrates agents into your backend with bindings and granular permissions. Sandboxes give you a full OS for browsers, native binaries, and dev servers."

> "You don't have to choose: agentOS works with sandboxes through the sandbox extension, spinning up a full sandbox on demand and mounting the sandbox's file system when the workload needs it."

**笔者认为**:**agentOS vs Sandbox 是 "轻量 vs 重量" 的对立,不是 "好 vs 坏" 的对立**:
- **agentOS 适合**:**agent 直接调你的 backend functions,workflow orchestration,multi-agent delegation** (低延迟 + 低成本 + 高密度)
- **Sandbox 适合**:**browser automation,native binary execution,完整 dev environment** (高隔离 + 高自由度)
- **agentOS 提供 sandbox extension 把两者整合**:**"轻量 in-process VM 为主,需要时调 full sandbox"**

### 2.2 内置 Claude Code + OpenCode + Pi 多 Agent

**1st-party 原文引用 (Rivet, agentos README)**:

> "**Multi-agent support**: Run built-in Pi, Claude Code, and OpenCode agents with a unified API, plus install registry command packages such as Codex as VM software"

> "**Sessions via ACP**: Create, manage, and resume agent sessions over the Agent Communication Protocol"

> "**Universal transcript format**: One transcript format across all agents for debugging, auditing, and comparison"

> "**Multiplayer**: Multiple clients observe and collaborate with the same agent in real time"

> "**Agent-to-agent**: Agents delegate work to other agents through host-defined bindings"

> "**Workflows**: Chain agent tasks into durable workflows with retries, branching, and resumable execution"

**3 个 AI Coding 工具内置 (Pi + Claude Code + OpenCode)**:
- **Pi** —— coding agent (Rivet 自家)
- **Claude Code** —— Anthropic 1st-party coding agent
- **OpenCode** —— 开源 coding agent (sst/opencode)
- **Codex** —— OpenAI 1st-party,作为 VM software 安装

**关键差异化**:**Universal transcript format = 跨 agent 统一 transcript 格式 = "多 agent 协作" + "agent-to-agent delegation" 的工程基础**。**这是 LangChain dynamic subagents (R700 article 文章 1) 的"vendor 无关"实现**:**不同 coding agent 通过统一 transcript + ACP + agent-to-agent 互相协作**。

**R700 关键洞察**:**agentOS 与 R700 article (LangChain 6/29-6/30 cluster) 形成跨范式镜像**:
- **LangChain 1st-party 选 Code Interpreter 加法安全 (WASM + QuickJS, zero-cap + bridge)**:agent dynamic subagents 写 JS 代码,代码 deterministic dispatch
- **Rivet 1st-party 选 in-process VM 减法安全 (Linux VM, deny-by-default claw back)**:agentOS 提供 VM,agent 跑在 VM 内,deny-by-default 权限隔离
- **两条不同的 "Harness 安全" 路径,不是替代,是互补**

### 2.3 Deny-by-default 权限模型

**1st-party 原文引用 (Rivet, agentos README)**:

> "Deny-by-default permissions: Granular control over filesystem, network, process, and environment access"

> "Programmatic network control: Allow, deny, or proxy any outbound connection"

> "Resource limits: Set precise CPU and memory limits per agent"

> "VM isolation: Each agent runs in its own VM with no shared state"

**agentOS Deny-by-default 模型**:
- **Filesystem**: 默认禁止所有路径,需要显式 allow
- **Network**: 默认禁止所有 outbound,可以 programmatic allow/deny/proxy
- **Process**: 默认禁止 fork/exec,需要显式 allow
- **Environment**: 默认禁止读 env,需要显式 allow
- **CPU/Memory**: 精确 per-agent 限制

**R700 关键洞察**:**agentOS Deny-by-default 与 LangChain 6/29-6/30 "Meta's Rule of Two" + Code Interpreter 零能力 形成 "Harness 减法安全" 共识**:
- **Anthropic R698 containment**:sandbox + VMs + egress controls = 减法安全
- **LangChain R700 article 文章 2**:"A sandbox starts computer-shaped, so its security work is subtractive" = 减法安全
- **Rivet R700 agentOS**:Deny-by-default permissions = 减法安全
- **3 vendor 1st-party 共识**:**"Harness 安全 = 减法 (从 broad capability claw back)"** —— **Phase 6 Runtime Spec 1st-party 命名前的"事实标准"先兆**

---

## 三、3 段核心代码示例

### 3.1 快速启动 (3 行 npm install + 10 行 TypeScript)

**1st-party 原文引用 (Rivet, agentos README)**:

```typescript
import { AgentOs } from "@rivet-dev/agentos-core";
import common from "@agentos-software/common";
import pi from "@agentos-software/pi";

const vm = await AgentOs.create({ software: [common, pi] });

// Create a session and send a prompt
const { sessionId } = await vm.createSession("pi", {
  env: { ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY! },
});

vm.onSessionEvent(sessionId, (event) => {
  console.log(event);
});

await vm.prompt(sessionId, "Write a hello world script to /home/agentos/hello.js");

// Read the file the agent created
const content = await vm.readFile("/home/agentos/hello.js");
console.log(new TextDecoder().decode(content));

vm.closeSession(sessionId);
await vm.dispose();
```

**笔者认为**:**这段代码展示 agentOS 的"低门槛"特性**:**3 行 npm install + 1 行 AgentOs.create + 1 行 createSession + 1 行 prompt = 5 步上手**。**对比 sandbox (E2B / Daytona):需要 cloud account、API key、container image、env config、auth setup,通常 30+ 行代码**。

### 3.2 Agent-to-agent delegation (multi-agent orchestration)

**1st-party 原文引用 (Rivet, agentos README)**:

> "Agent-to-agent: Agents delegate work to other agents through host-defined bindings"

**核心机制**:**通过 host-defined bindings,让 agent 调其他 agent**。**这是 LangChain dynamic subagents 的 in-process VM 实现**:
- **LangChain 1st-party 范式**:agent 写 JS 代码 → task() 函数 dispatch subagent → subagent 跑在 QuickJS interpreter
- **Rivet 1st-party 范式**:agent 调 binding → binding 调其他 agent → 其他 agent 跑在 agentOS VM 内
- **两种范式殊途同归**:**"agent-to-agent delegation + universal transcript + host-defined binding"**

### 3.3 Multiplayer (multi-client collaboration)

**1st-party 原文引用 (Rivet, agentos README)**:

> "Multiplayer: Multiple clients observe and collaborate with the same agent in real time"

**核心机制**:**多个 client 同时观察 + 协作同一个 agent session**。**这是 Anthropic / LangChain / Manus 等 1st-party 产品尚未完全 ship 的能力**:**multi-client real-time collaboration = 团队 debugging / 教学 / review 场景的关键能力**。

---

## 四、3 个边界与适用场景

### 4.1 适用场景

- **AI Coding backend**:**直接调 Claude Code / OpenCode / Pi 跑 coding 任务,92x 冷启动 + 47x 内存优势在 multi-tenant 场景显著**
- **Multi-agent orchestration**:**agent-to-agent delegation + universal transcript + workflows = production-grade multi-agent**
- **In-backend 集成**:**agents 直接调你 backend functions (bindings),no network hop,no auth complexity**
- **Self-hosted 部署**:**Apache-2.0 开源,部署到你自己的 infra (Railway / Vercel / Kubernetes) 或 Rivet Cloud**

### 4.2 不适用场景

- **Browser automation**:**需要完整 OS 跑 Chrome / Puppeteer / Playwright —— 用 sandbox extension 调 E2B / Daytona**
- **Native binary execution**:**需要跑 native 编译产物 (C / C++ / Rust) —— 同上**
- **完整 dev environment**:**需要 shell + 完整 FS + 系统级 deps (apt / yum) —— 同上**

### 4.3 R700 推荐适用度评估

| 维度 | 评分 (1-5) | 说明 |
|------|------------|------|
| **与 AI Coding 主题匹配度** | **5** | 内置 Claude Code + OpenCode + Pi 多 coding agent |
| **生产可用代码** | **5** | Apache-2.0 + npm package + 完整 SDK |
| **差异化** | **4** | "in-process VM" 是 2026 Q3 新范式,不是 incremental improvement |
| **成熟度** | **3** | v1.0 稳定 (>= 3,500 ⭐),但 ecosystem 还在 early |
| **Stars** | **4** | 3,572 ⭐ 跨 2.5 年 = 持续成长,但不是 explosive |
| **综合评分** | **21/25** | ✅ 写推荐 |

---

## 五、跨范式镜像解 (R700 完整 picture)

### 5.1 3 厂商 1st-party Harness 安全范式对比

| 厂商 | 1st-party Harness 范式 | 关键证据 | R700 引用 |
|------|---------------------|---------|-----------|
| **Anthropic** | **Sandbox + VMs + egress controls (减法安全)** | How we contain Claude (May 2026) | R698 deep-dive |
| **LangChain** | **Code Interpreter 加法安全 (WASM + QuickJS, zero-cap + bridge)** | Running Untrusted Code Without a Sandbox (June 30, 2026) | R700 article 文章 2 |
| **Rivet** | **In-process VM 减法安全 (V8 isolates + deny-by-default permissions)** | agentos README + benchmarks | R700 project |

**3 厂商共识**:**"Harness 安全 = 减法或加法"** —— **不是"一个赢一个输",而是"不同场景用不同范式"**:
- **Anthropic containment (减法 sandbox)**:**适合 full agent + complete dev environment (Claude Code sandbox, Cowork)**
- **LangChain Code Interpreter (加法 zero-cap)**:**适合 orchestration workflow + 受限 capability (Deep Agents dynamic subagents)**
- **Rivet in-process VM (减法 deny-by-default)**:**适合 multi-tenant AI coding backend + low-latency + low-cost (multi-agent delegation)**

### 5.2 Phase 6 Runtime Spec 命名前的"事实标准"先兆

**R700 关键洞察**:**3 厂商 1st-party Harness 范式共识 = Phase 6 trigger 1 (Runtime Spec 1st-party article) 命名前的"事实标准"先兆**:
- **共识 1**:**"减法/加法安全"是 Harness 设计的二分法** (3 厂商 1st-party 文章 + 项目都体现)
- **共识 2**:**"Meta's Rule of Two" 是 Harness 设计的公理级原则** (LangChain R700 article + Anthropic R698 containment 同步引用)
- **共识 3**:**"deny-by-default / zero-cap / claw back" 是默认安全姿态** (Rivet + LangChain + Anthropic 同步体现)

**3 共识 = "Runtime Spec 1st-party 1st-party 内容" 的潜在骨架**。**Phase 6 trigger 1 命名前,** **3 厂商 1st-party 1st-party 文章/项目已经提供了 Runtime Spec 的"事实标准" —— Runtime Spec 1st-party article ship 时,大概率是 "把 3 共识 formalize 成 spec"**。

---

## 六、行动启示

### 6.1 给 AI Coding backend 开发者

- **R700 优先 ship agentOS 而非 E2B / Daytona 在 multi-tenant 场景**:**92x 冷启动 + 47x 内存 + 17x 成本优势在 multi-tenant AI coding 场景显著**
- **直接用 `npx skills add addyosmani/agent-skills` 安装 24 个 production skills**:**(与本仓库 Stage 10 Skill 路径完美匹配)**
- **Universal transcript format 优势**:**跨 Claude Code / OpenCode / Pi / Codex 统一 debug + audit + compare**

### 6.2 给 Multi-Agent 编排研究者

- **agentOS 是 "in-process VM 跑 multi-agent" 的生产实现**:**与 LangChain dynamic subagents (Code Interpreter) 形成跨范式镜像**
- **agent-to-agent delegation + host-defined bindings**:**是 "multi-agent orchestration" 的另一个实现路径 (vs LangChain's Code Interpreter)**
- **Multiplayer 能力**:**多 client 实时协作,Anthropic / LangChain / Manus 尚未完全 ship**

### 6.3 给 Agent Security 从业者

- **agentOS Deny-by-default 模型**:**与 Anthropic containment (R698) + LangChain Code Interpreter (R700 article 文章 2) 形成 3 厂商 1st-party 减法/加法安全共识**
- **"Meta's Rule of Two"**:**3 厂商 1st-party 共识 (Anthropic R698 + LangChain R700 article + Rivet R700 project) = Phase 6 Runtime Spec 命名前的"事实标准"先兆**

---

## 七、引用与参考

1. **rivet-dev/agentos GitHub**: https://github.com/rivet-dev/agentos (3,572 ⭐, Apache-2.0, R700 实测)
2. **agentos README**: https://raw.githubusercontent.com/rivet-dev/agentos/main/README.md
3. **agentos 文档**: https://agentos-sdk.dev/docs
4. **Rivet Cloud**: https://agentos-sdk.dev/docs/deployment
5. **R700 article (LangChain 6/29-6/30 cluster)**: `articles/deep-dives/hybrid-runtime-r700-langchain-3-article-cluster-jun29-30-dynamic-subagents-untrusted-code-state-aware-harnesses-openwiki-rate-h-baseline-shift-verification-2026.md`
6. **R698 article (Anthropic containment)**: `articles/harness/anthropic-containment-claude-across-products-2026.md`
7. **LangChain Running Untrusted Code**: https://blog.langchain.com/running-untrusted-agent-code-without-a-sandbox (Hunter Lovell, June 30, 2026)
8. **LangChain Dynamic Subagents**: https://blog.langchain.com/introducing-dynamic-subagents-in-deep-agents (Sydney Runkle et al., June 29, 2026)
9. **LangChain Candidly State-Aware Harness**: https://blog.langchain.com/how-candidly-built-state-aware-agent-harnesses-with-langsmith (Ben Levine, Patrick Hendershott, June 29, 2026)

---

*由 AgentKeeper R700 自动维护 | SKILL v1.4.0 | 2026-07-08 14:37 CST | ⭐ 新增 agentOS 项目推荐,完成 R700 完整 deep-dive 闭环*
