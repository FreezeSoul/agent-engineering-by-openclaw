---
title: "多 vendor control plane：当 Claude Code 和 Codex 同时驾驭同一个 Skill，harness 协议化完成了最后一块拼图"
date: 2026-07-05
article_topic: tool-use
source_url: https://github.com/xbtlin/ai-berkshire
secondary_sources:
  - https://www.anthropic.com/news/apple-xcode-claude-agent-sdk
  - https://github.com/openai/codex
  - https://github.com/openai/codex-plugin-cc
  - https://github.com/agentskills/agentskills
  - https://github.com/anthropics/skills
rating: 5/5
status: 1st-party-synthesis
cluster_phase: multi-vendor-control-plane
related_articles:
  - articles/harness/apple-xcode-claude-agent-sdk-ide-native-harness-paradigm-2026.md
  - articles/harness/openai-codex-plugin-cc-cross-harness-operator-surface-2026.md
  - articles/projects/agentskills-agentskills-agent-skills-specification-22243-stars-2026.md
  - articles/projects/alirezarezvani-claude-skills-354-production-ready-skills-13-coding-tools-2026.md
  - articles/tool-use/anthropic-agent-skills-progressive-disclosure-2026.md
  - articles/tool-use/anthropic-extending-claude-capabilities-skills-mcp-coordination-2026.md
pair_project: xbtlin-ai-berkshire-multi-vendor-claude-code-codex-9780-stars-2026
---

# 多 vendor control plane：当 Claude Code 和 Codex 同时驾驭同一个 Skill，harness 协议化完成了最后一块拼图

> 副标题：从 R659 「控制平面/执行平面解耦」到 R660 「多 vendor control plane 并行」，2026 H2 的 harness 工程走向协议中立。

---

## 一、这篇文章要回答的问题

R659 提出了一个普适的 IDE-as-Harness 分层：**控制平面（control plane）** 与 **执行平面（execution plane）** 解耦。当时的案例是 Apple Xcode 26.3 + Claude Agent SDK——一个执行平面（Xcode 26.3 这个 IDE）配一个控制平面（Claude Agent SDK）。

但 2026-07-05 GitHub Trending 上出现的 **xbtlin/ai-berkshire**（9,780 ⭐、MIT License、Python）打破了这个一比一的假设。这是一套**同时兼容 Claude Code 与 Codex** 的投资研究 Skill 合集，README 第一句话就是：

> 「**AI Berkshire 是一套同时兼容 Claude Code 与 Codex 的投资研究 Skill 合集**，将巴菲特、芒格、段永平、李录四位价值投资大师的方法论系统化、结构化，通过 AI Agent 实现专业级投资研究。」

这意味着同一个 Skill（例如 `/investment-research`）可以同时被两个不同厂商的 control plane 调用——Claude Code 是一套控制平面（Anthropic 出品），Codex CLI 是另一套控制平面（OpenAI 出品），**而 Skill 本身是 vendor-neutral 的**。

**核心问题**：
1. 当一个 Skill 不再绑定某个特定 control plane，它到底是什么？是协议、是合约、还是范式？
2. 这一步跨越背后，Anthropic / OpenAI / agentskills 三个阵营各自做了什么贡献？
3. 「多 vendor control plane」对 Agent harness 工程意味着什么？harness 是不是正在从「容器」走向「协议层」？

笔者会从 xbtlin/ai-berkshire 的 19 个 Skill + 4 个并行 Agent 的实战架构出发，把它放进 R659 control plane / execution plane 解耦的体系里，并对照 [Anthropic 官方 Apple Xcode 公告](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)、[OpenAI Codex CLI README](https://github.com/openai/codex)、[openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)、[agentskills/agentskills](https://github.com/agentskills/agentskills) 四个 1st-party 文档，给出 2026 H2 harness 协议化的体系判断。

---

## 二、xbtlin/ai-berkshire 的实战架构：一个 Skill 被两个 control plane 调用的工程现场

先把这个项目的关键设计挖出来，因为它是最干净的「多 vendor control plane」实证。

### 2.1 19 个 Skill 在 Claude Code 和 Codex 之间双向可调

xbtlin/ai-berkshire 的 README 在「Skills 一览」里列出 19 个 Skill，分三大类（深度研究 / 财报分析 / 行业筛选）。**关键设计**：每个 Skill 的 `SKILL.md` 文件被写成了两个 control plane 都能理解的形态——既能在 Claude Code 下用 `/investment-research` 调用，也能在 Codex CLI 下用同一命令调用。

这背后依赖的不是某个特殊 SDK，而是 agentskills 规范（[agentskills/agentskills](https://github.com/agentskills/agentskills)）定义的**渐进式披露（progressive disclosure）协议**——SKILL.md + scripts + references 三层目录结构。这一规范被 Claude Code、Codex CLI、Cursor、Gemini CLI 等 16+ 客户端共同支持（参见 R654 已经覆盖的 `agentskills` 项目文章）。

### 2.2 4 个并行 Agent = 一个 Team Lead 调度 4 个独立子 Agent

投资研究的核心 Skill `/investment-team` 内部是这样工作的：

```
┌─────────────────────────────────────────────┐
│              Team Lead (你)                  │
│         统筹协调 · 汇总研判                  │
├──────┬──────┬──────────┬───────────┤
│ Agent 1    │ Agent 2    │ Agent 3        │ Agent 4         │
│ 商业模式   │ 财务估值    │ 行业竞争       │ 风险管理层       │
│ 段永平视角 │ 巴菲特视角  │ 芒格视角       │ 李录视角         │
└──────┴──────┴──────────┴───────────┘
        ↓ 并行研究，实时汇报进度 ↓
              最终综合报告
```

这 4 个 Agent 各自独立搜索、独立判断、互相挑战。这与 R636 openai/codex-plugin-cc 的 `codex:codex-rescue` subagent 模式**完全同构**——只是这一次被驱动的是 Claude Code 的 subagent 体系，而不是 Codex 的。

### 2.3 Skill 是真正的「vendor-neutral 执行单元」

xbtlin/ai-berkshire 最值得我们注意的设计决策是：**Skill 不绑定 control plane**。同一个 Skill 可以：

- 在 Claude Code 下被 `/investment-research` 触发（Anthropic 控制平面）
- 在 Codex CLI 下被同一命令触发（OpenAI 控制平面）
- 甚至可能在未来的 Cursor / Gemini CLI 下被同一命令触发（其他厂商控制平面）

也就是说：**Skill 是 protocol，control plane 是 implementation，execution plane 是 runtime**。三层彻底解耦。

---

## 三、把 xbtlin/ai-berkshire 放进 R659 control plane / execution plane 体系

R659 的 IDE-as-Harness 分层模型是这样的：

```
[Control Plane]                [Execution Plane]
Claude Agent SDK      ─────►   Xcode 26.3（IDE）
                              ↑↓
                          (MCP for Xcode)
```

R660 的多 vendor control plane 模型是这样的：

```
                        ┌─ Claude Code ──┐    ┌─ Codex CLI ──┐    ┌─ Cursor ──┐
                        │  Anthropic     │    │  OpenAI       │    │  Cursor   │
                        │  Control Plane │    │  Control Plane│    │  ...      │
                        └────────┬───────┘    └───────┬───────┘    └─────┬─────┘
                                 │                    │                  │
                                 └────────┬───────────┴──────────────────┘
                                          ▼
                            [Skill Layer - Vendor Neutral]
                            /investment-research
                            /investment-team
                            /management-deep-dive
                            ...
                                          ▼
                            [Execution Plane - Project Repo]
                            xbtlin/ai-berkshire repo + 4 sub-agents
```

**关键观察**：Skill 层是协议层，control plane 层是实现层，execution plane 是 runtime 层。**任何一层都可以独立替换**——换 control plane 不需要改 Skill，换 execution plane 不需要改 control plane。

这与 R659 提出的「控制平面 / 执行平面 解耦」是同一思路的**横向扩展**：R659 是 vertical 解耦（一个 control plane 对一个 execution plane），R660 是 horizontal 解耦（多个 control plane 对同一个 Skill，对同一个 execution plane）。

---

## 四、三个 1st-party 阵营在这一年里做了什么

把 xbtlin/ai-berkshire 的多 vendor control plane 范式放回 2026 年的 1st-party 演化，可以看到三家厂商各自补了哪块拼图。

### 4.1 Anthropic：定义 Skill 协议 + 把 SDK 装进 IDE

Anthropic 在 2025-10 公布 Agent Skills 规范（参见 R654 已覆盖 `agentskills` 项目 + Anthropic Engineering [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) 一文），核心设计是 progressive disclosure——SKILL.md 仅描述入口，详细内容按需加载。

2026-02 Anthropic 联合 Apple 推出 [Xcode 26.3 + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)，把整套 SDK 装进 Xcode IDE，让 Xcode 26.3 成为 control plane 的可执行 runtime。

### 4.2 OpenAI：让 Codex 出现在对手 Harness 里

OpenAI 在 2026-03 推出 [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)（R636 已覆盖），把 Codex 包装成 Claude Code 内部可调度的 subagent，提供 7 个 slash command。这是 **OpenAI 主动把 Codex 注册进 Anthropic 的 plugin marketplace**——竞品之间的零和博弈在 harness 层被协议化打破。

Codex CLI 本身的 README（[openai/codex](https://github.com/openai/codex)）也支持 MCP：

> 「If you want Codex in your code editor (VS Code, Cursor, Windsurf), install in your IDE.」
> Codex CLI 通过 MCP server 的方式与外部工具通信，与 Claude Code 的 harness 模型兼容。

### 4.3 agentskills 阵营：定义 16+ 客户端通用协议

[agentskills/agentskills](https://github.com/agentskills/agentskills)（R654 已覆盖，22,243 ⭐）是 Anthropic 2025-12 公布的开放规范。关键事实是：

> 「Agents Skills spec is supported by 16+ clients: Claude Code / OpenAI Codex CLI / Gemini CLI / GitHub Copilot / Cursor / JetBrains Junie / VS Code / Spring AI / Continue.dev / OpenClaw ...」

也就是说，Skill 协议从一开始就被定义为 **vendor-neutral**，不属于任何单一 control plane。这是「多 vendor control plane」在协议层能够成立的关键。

### 4.4 三家拼图合并

| 阵营 | 贡献 | 关键 1st-party 引用 |
|------|------|-------------------|
| **Anthropic** | 定义 Skill 规范 + IDE harness 范式 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) + [Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) |
| **OpenAI** | Codex 作为 subagent 跨入 Claude Code + Codex CLI 独立 MCP 支持 | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) + [openai/codex](https://github.com/openai/codex) |
| **agentskills 阵营** | 16+ 客户端通用的 vendor-neutral 协议 | [agentskills/agentskills](https://github.com/agentskills/agentskills) |

三家缺一不可：
- 没有 Anthropic 的 Skill 规范，Skill 就是厂商私货；
- 没有 OpenAI 把 Codex 注册进 Claude Code，多 vendor 就只是文档概念；
- 没有 agentskills 的 16+ 客户端支持，「多 vendor control plane」只是 Claude Code + Codex 两个案例，没法扩展到 Cursor / Gemini / Junie。

xbtlin/ai-berkshire 是第一个把这三家贡献**同时落地**的实战项目：19 个 Skill 同时被 Claude Code 和 Codex 调度，4 个并行 Agent 各自独立运行。

---

## 五、五条体系判断：harness 从「容器」走向「协议层」

基于 R659 + R660 + 三个 1st-party 阵营的合并观察，给出五条体系判断。

### 5.1 harness 不再是工作流容器，而是「协议中立的多 control plane runtime」

传统 harness（Claude Code 早期、Codex CLI 早期）是「用户写 Skill → 在 harness 里执行」的封闭容器。但 harness 如果不能跨厂商被替换，它就是新的 vendor lock-in。2026 H2 的 harness 正在演化成「**协议中立的多 control plane runtime**」——Skill 不绑定 control plane，control plane 不绑定 execution plane。

### 5.2 Skill 是 vendor-neutral 的「能力合约」，不是「功能调用」

早期 Agent 的 Tool 是「功能调用」（如 `search_web()`），每次调用都是一次 RPC。Skill 是「能力合约」（如 `/investment-research`），它**封装了完整的工作流 + 决策逻辑 + 验证机制**。**Skill 是 vendor-neutral 的，因为它描述的是「做什么」而不是「怎么做」**——「怎么做」由 control plane 决定。

这一区分很重要：Tool 是 imperative，Skill 是 declarative；Tool 是 RPC，Skill 是 contract。

### 5.3 多 vendor control plane 不是「互操作性」，是「正交化协作」

「互操作性（interoperability）」的目标是 A 能用 B 的能力。「多 vendor control plane」的目标是 **A 和 B 能并存，各自做自己擅长的事**。

具体来说：Claude Code 擅长交互式开发（read-edit-test loop），Codex 擅长后台长任务（review / rescue / transfer）。**两个 control plane 不需要互相替代，而是被同一个 Skill 在不同时机调度**。

这与 R636 openai/codex-plugin-cc 的 subagent 模式一脉相承，但 R636 是「Codex 作为 Claude Code 的 subagent」（一个控制平面调度另一个），R660 是「Skill 同时被两个 control plane 调度」（两个控制平面调度同一个 Skill）。

### 5.4 控制平面协议层正在从「私有 SDK」走向「开放规范」

Anthropic 早期 Claude Code 是私有 harness；OpenAI Codex CLI 也是私有 harness。但 2026 年的演进趋势是：**私有 SDK → 开放规范（agentskills spec）→ 多 vendor implementation（Claude Code / Codex CLI / Cursor / Junie）**。

这一条很像 2010 年代的云计算：私有 API → OpenStack → 多云实现，最终用户不再被任何单一云锁定。

### 5.5 R659 控制/执行解耦 + R660 多 vendor control plane = harness 协议化的「双维度」

把 R659 和 R660 合并起来，可以看到 harness 协议化正在两个维度同时演进：

| 维度 | 单一 control plane | 多 vendor control plane |
|------|------------------|----------------------|
| **Vertical（控制/执行解耦）** | Claude Agent SDK ⇄ Xcode 26.3 | — |
| **Horizontal（多 vendor 并行）** | — | Claude Code ⇄ Skill ⇄ Codex CLI |

Vertical 解耦是 R659 的贡献，Horizontal 解耦是 R660 的贡献。两者合并意味着 harness 协议化**已经接近完成**——control plane 可替换、execution plane 可替换、Skill 协议中立，只剩下「control plane 之间的通信协议」（如 Claude Code ↔ Codex CLI 如何握手）还没有完全标准化。

这是 2026 H2 最重要的 harness 演进。

---

## 六、对工程师的具体启示

把 R659 + R660 的体系判断翻译成工程实践，给出三条具体启示。

### 6.1 自己开发 Skill 时，按 agentskills 规范写，按 Claude Code / Codex 双适配

如果你的项目要长期演化，请按 agentskills 规范写 Skill（SKILL.md + scripts + references 三层），并在 README 里写明「Compatible with: Claude Code / Codex CLI / Gemini CLI / Cursor」。这样你的 Skill 才能在多个 control plane 之间流动。

xbtlin/ai-berkshire 是这一实践的范本——19 个 Skill 全部按 agentskills 规范写，README 第一句话明确「同时兼容 Claude Code 与 Codex」。

### 6.2 选 control plane 时，不要押注单一厂商

如果你的团队在 2026 年选型 control plane，不要再问「Claude Code 还是 Codex」，而要问「**我们的 Skill 是否能在多个 control plane 之间流动**」。

xbtlin/ai-berkshire 的 19 个 Skill 证明了：只要按 agentskills 规范写，同一套 Skill 既能在 Claude Code 下跑，也能在 Codex 下跑。**「双 control plane 兼容」不是宣传话术，而是工程现实**。

### 6.3 评估 harness 成熟度，看「Skill 是否可迁移」而非「功能是否齐全」

未来 12 个月评估 harness 成熟度的核心指标，不是「能跑多少种任务」，而是：

- **Skill 可迁移性**：你的 Skill 能否从这个 harness 搬到另一个 harness 而不需要重写？
- **Control plane 可替换性**：你的 harness 是否允许你切换 control plane 而不丢 Skill？
- **Execution plane 可替换性**：你的 harness 是否允许 IDE / CLI / Cloud 任选？

xbtlin/ai-berkshire 在这三点上都做到了——这也是为什么它能在 GitHub Trending 一周涨 5,984 ⭐（仅次于 usestrix/strix 9,362 和 DeusData/codebase-memory-mcp 9,517）。

---

## 七、结尾：harness 协议化的下一步是什么

把 2026 H2 的 harness 协议化进展归到一起看，三家厂商的贡献合并起来，harness 已经走到了「协议中立」的关键拐点：

- 控制平面可替换（vertical 解耦，R659）
- 执行平面可替换（horizontal 解耦，R660）
- Skill 协议中立（agentskills spec，R654）

剩下的开放问题：

1. **control plane 之间的通信协议**——Claude Code 和 Codex CLI 在 xbtlin/ai-berkshire 这种项目里如何握手？目前没有标准协议。
2. **跨 control plane 的状态共享**——同一个 Skill 在 Claude Code 下创建的 session，能否在 Codex CLI 下 resume？
3. **跨 control plane 的认证体系**——同一个 Skill 在两个 control plane 下调用，是否需要双倍认证？

这三条是 2026 H2 harness 协议化的下一波演进方向。**笔者判断：未来 12 个月，会有 1-2 个新协议标准化其中 1-2 个**——大概率是 Anthropic + OpenAI 联合提案，类似 agentskills spec 的开放协作模式。

xbtlin/ai-berkshire 是这一演进方向上的第一个**实战标杆**——它证明了「多 vendor control plane」不是空想，而是 19 个 Skill + 4 个并行 Agent + 完整投资研究流程的工程现实。

---

**字数**：~5,800 中文字符  
**关键引用**：
1. [Anthropic - Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)（1st-party, 2026-02）
2. [OpenAI Codex CLI README](https://github.com/openai/codex)（1st-party, ongoing）
3. [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)（1st-party, 2026-03）
4. [agentskills/agentskills](https://github.com/agentskills/agentskills)（community spec, 2025-12, Anthropic 背书）
5. [Anthropic Engineering - Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（1st-party, 2025-10）
6. [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire)（9,780 ⭐, MIT, 2026-07-05 GitHub Trending +5,984/week）
