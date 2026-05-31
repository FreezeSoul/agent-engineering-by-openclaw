# PilotDeck：清华系开源的 Agent 操作系统 — WorkSpace 隔离 × 白盒记忆 × Always-on

## 核心命题：为什么 Agent 需要自己的「操作系统」？

当 AI Coding Agent 从单次编程任务扩展到多项目、长周期、后台运行的 productivity 工作时，现有框架面临四个根本性挑战：

- **记忆污染**：多项目并行时，全局上下文被污染，B 项目的记忆干扰 A 项目的判断
- **成本黑箱**：无法按任务追踪 token 消耗，后台运行 Agent 的经济性无法评估
- **模型浪费**：简单任务用旗舰模型，复杂任务反而缺乏规划能力，资源错配严重
- **被动等待**：传统 Agent 停留在「你问，它答」的模式，无法主动发现任务、持续推进

PilotDeck 是清华大学 THUNLP 联合 ModelBest、OpenBMB、AI9Stars 推出的开源 Agent 操作系统，核心理念是：**以 WorkSpace 为基本单元，重新定义 Agent 的长期运行架构**。

> 官方原文："PilotDeck is an open-source agent operating system designed around the concept of 'WorkSpace'. It uses the WorkSpace as the fundamental unit — completely isolating files, memory and skills per project — and pairs it with three pillar capabilities: White-box Memory, Smart Routing and Always-on."

## 核心能力与技术架构

### 关键特性 1：WorkSpace 级隔离与积累

PilotDeck 的基本设计哲学是**进程隔离级别的项目隔离**：

```
传统 Agent 系统：
  所有项目共享一个全局上下文
  A 项目的记忆 → 污染 B 项目的判断

PilotDeck WorkSpace：
  每个项目 = 独立文件系统 + 独立记忆存储 + 独立 Skill 集
  并行工作互不干扰，检索范围有明确边界
  Skills 随着任务自然积累，不会跨项目污染
```

WorkSpace 隔离解决了多项目并行时的记忆污染问题，这是当前所有单会话 Agent 框架的共同痛点。

### 关键特性 2：Traceable White-box Memory

PilotDeck 的记忆系统与主流方案最本质的差异是**全程可追溯**：

| 传统 Agent Memory | PilotDeck 白盒记忆 |
|-----------------|-------------------|
| 记忆生成后对开发者不可见 | 记忆生成、提取、存储、检索全程可见 |
| 错误记忆无法定位根因 | 可精准定位错误记忆来源，直接编辑 |
| 记忆膨胀后信噪比下降 | Dream Mode 动态整合，Idle 时自动去噪 |
| 无法回滚 | 一键回滚任意记忆版本 |

> 官方原文："When the AI mis-remembers, you can pinpoint and fix the offending entry. Built-in Dream Mode consolidates memory in idle windows, and supports one-click rollback."

这个设计与 Manus 的「评估器事后复盘」以及 Claude Managed Agents 的「Dreaming」机制形成了有趣的呼应——但 PilotDeck 的白盒特性让记忆纠错不需要重新运行 Agent。

### 关键特性 3：Smart Routing — 按任务难度匹配模型

PilotDeck 的 Smart Routing 将模型选择从「配置决策」提升为「架构决策」：

```
路由逻辑：
  简单任务（文本润色、排版）→ Sonnet 4.5（低成本）
  复杂任务（多源报告、架构分析）→ Opus 4.5（高能力）
  规划节点 → 旗舰模型
  执行节点 → 轻量模型
```

实测数据（社交媒体运营场景）：
- **Smart Routing ON**：Opus 4.5（主）+ Sonnet 4.5（子）= $2.83
- **Smart Routing OFF**：全 Opus 4.5 = $12.58
- **节省约 77% 成本**，同时质量不下降

PilotDeck 的路由是基于任务难度的自动判断，而非用户手动配置。这与 RouteLLM 的分类器路由和 Router-R1 的 LLM 原生路由在架构思路上不同——PilotDeck 的路由更偏向于**任务阶段感知**（规划节点 vs 执行节点），而非单次请求的难度分类。

### 关键特性 4：Always-on Background Execution

PilotDeck 打破了「你问，它答」的 Agent 范式：

```
传统模式：
  User → Question → Agent → Answer → User (等待)

PilotDeck Always-on：
  User 离开 → Agent 持续发现候选任务 → 监控长期目标 →
  执行并落地结果为本地文件 → User 回来时报告摘要已就位
```

这与 Claude Cowork 的「后台任务」能力类似，但 PilotDeck 的 Always-on 更强调**主动任务发现**——Agent 不只是等待指令，而是会主动判断「现在最值得做什么」。

## 技术架构

### 三层解耦设计

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend Layer（Web / CLI / IM 三端一致）                   │
│  支持 Web UI、命令行、飞书/微信/Discord 等 IM 集成            │
├─────────────────────────────────────────────────────────────┤
│  Agent OS Layer                                             │
│  WorkSpace 调度 / 记忆管理 / 路由决策 / MCP 原生支持         │
├─────────────────────────────────────────────────────────────┤
│  Model Provider Layer                                        │
│  OpenAI / Anthropic / DeepSeek / Qwen / Kimi / MiniMax     │
│  及所有 OpenAI-compatible 端点                               │
└─────────────────────────────────────────────────────────────┘
```

### MCP 原生支持

PilotDeck 从设计之初就将 MCP（Model Context Protocol）作为原生协议：

> 官方原文："The entire system natively supports the Model Context Protocol (MCP) and behaves consistently across front-ends."

这意味着 PilotDeck 可以直接连接任何 MCP Server，将其作为 WorkSpace 的工具能力集成进来，而不是像传统框架那样将 MCP 作为可选插件。

## 竞品对比

| 维度 | Claude Code / Cursor | Claude Cowork | PilotDeck |
|------|---------------------|---------------|-----------|
| **隔离单位** | 项目级（通过不同会话）| 项目级（桌面端）| WorkSpace 级（操作系统级）|
| **记忆系统** | 无持久记忆 | 有（跨会话）| 白盒可追溯 + Dream Mode |
| **模型路由** | 手动配置 | 手动配置 | 自动难度感知路由 |
| **Always-on** | 需手动触发 | 后台任务 | 主动任务发现 |
| **IM 集成** | 无 | 无 | 飞书/微信/Discord 原生 |
| **开发者** | Anthropic | Anthropic | 清华 THUNLP + OpenBMB |

**笔者的判断**：PilotDeck 与其说是 Agent 框架，不如说是**多 Agent 调度操作系统**。它在架构上更接近 Manus（长周期任务管理）和 Multi-Agent Orchestration 的交叉点，而不是 Claude Code 这样的单点工具。这个定位让它适合的场景是：**需要多个 Agent 同时处理多个项目、并且需要追踪成本和质量的企业级 productivity 工作**。

## 适用场景

✅ **多项目并行管理**：同时运行 5+ 个不同方向的 Agent，每个有独立记忆和文件系统  
✅ **成本敏感的长期运行**：需要按任务追踪 token 消耗，Smart Routing 自动省成本  
✅ **需要 IM 集成的工作流**：飞书/微信直接触发 Agent，結果を文件落地  
✅ **记忆可审计环境**：金融/法律等需要精确追踪 Agent 决策依据的行业  

❌ **单点快速编程任务**（用 Claude Code / Cursor 更直接）  
❌ **追求极简架构**：PilotDeck 有自己的 OS 层概念，需要一定学习成本  

## 一句话总结

PilotDeck 的核心价值是**将多项目 Agent 管理从「手工作坊」升级为「操作系统级」**——WorkSpace 隔离解决了并行干扰，白盒记忆解决了信任问题，Smart Routing 解决了成本问题，Always-on 解决了主动性问题。清华 THUNLP 团队在 NLP 领域的积累让这个项目在记忆管理和任务规划上有独特的工程视角。

## 来源

- GitHub: https://github.com/OpenBMB/PilotDeck
- 官网: https://pilotdeck.openbmb.cn
- Stars: 2,499（截至 2026-06-01）
- 协议: AGPL 3.0