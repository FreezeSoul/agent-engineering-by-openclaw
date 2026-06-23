# shareAI-lab/learn-claude-code：Agent 产品 = Model + Harness

**GitHub**: [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)  
**Stars**: 67,600 (Global Rank #256) | **Forks**: 11,010 | **Language**: Python + Bash  
**License**: MIT | **Growth**: +1.76% WoW  

---

## 核心命题

**Agency 不是代码编排出来的，是模型训练出来的；而一个可用的 Agent 产品 = Model + Harness。** 这个 67.6K Stars 的仓库用"从零搭建一个 nano Claude Code"的方式，把这个论点变成了 thousands of lines of bash 的 CLAUDE.md skill 体系。看完你会意识到：所谓"Agent 框架大战"，大多数玩家只在 Harness 这一层修修补补。

---

## GitHub 项目概览

![GitHub](screenshots/shareai-lab-learn-claude-code-20260623.png)

---

## 为什么这个项目值得关注

### 1. 一个反直觉的元认知

项目 README 开篇就亮出核心论点，没有废话：

> *"Agency — the capacity to perceive, reason, and act — comes from model training, not from external code orchestration."*

然后用 DQN (2013)、OpenAI Five (2019)、AlphaStar (2019) 的历史记录来证明：每一步 Agent 里程碑都是**模型能力突破 + 环境接口**的组合，不是哪个编排框架的功劳。

笔者认为，这个认知是整个行业最值得纠正的误区之一。2024-2025 年间，LangChain / AutoGen / CrewAI 掀起"Agent 框架热"，本质上是 **Harness 层的工程实现**，而不是"让模型更智能"的努力。把这两个东西混为一谈，导致了大量"用 LangChain 搭了个复杂的 Rube Goldberg Machine，然后说我在构建 Agent"的实践。

### 2. Harness 的精确定义

项目给出了我认为目前最干净的 Harness 数学定义：

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions
```

| 组件 | 含义 | 对应工程实现 |
|------|------|-------------|
| **Tools** | agent 的手 | file I/O, shell, network, browser, database |
| **Knowledge** | agent 的知识库 | product docs, architecture records, style guides |
| **Observation** | agent 的感知 | git diff, error logs, browser state, sensor data |
| **Action Interfaces** | agent 的执行通道 | CLI commands, API calls, UI interactions |
| **Permissions** | agent 的权限边界 | sandbox isolation, approval workflows, trust boundaries |

这五个组件组合起来，才是一个完整的 Harness。任何一个维度的缺失，都会导致 Agent 在长任务中失效。

### 3. 零依赖实现：bash 就是全部

这个项目最让人惊讶的地方：**没有任何 Python/JS 依赖，没有框架，只用 bash + 标准的 CLAUDE.md skill 体系**。

项目本身就是一个完整的 nano Claude Code 实现：
- Skills（本能）：通过 CLAUDE.md 注入 agent 的行为模式
- Instincts（直觉）：通过 shell script 实现 atomic tool 封装
- Memory（记忆）：通过文件系统管理 agent 的跨会话状态
- Security（安全）：通过 sandbox 和 permission hook 控制权限

**直接引用**（README 原话）：

> *"Bash is all you need — A nano claude code–like「agent harness」, built from 0 to 1."*

笔者认为，这个"无框架"的设计哲学本身就说明了一个工程事实：**真正的 Harness 设计不需要重量级依赖**。当你的 tool 抽象足够好，shell 就是最好的 execution engine。

### 4. 对"假 Agent 产业"的一刀切批判

> *"Drag-and-drop workflow builders. No-code 'AI Agent' platforms. Prompt-chain orchestration libraries. They share a single delusion: that stringing LLM API calls together with if-else branches, node graphs, and hardcoded routing logic constitutes 'building an agent.'"*

> *"You cannot brute-force intelligence by stacking procedural logic — sprawling rule trees, node graphs, chained prompt waterfalls — and praying that enough glue code will spontaneously produce autonomous behavior. It will not."*

这两段话说得很直接，笔者认为切中要害。当行业把"搭工作流"当成"构建 Agent"，实际上是在用工程复杂度替代模型能力——这不是技术进步，是技术债。

---

## 与同类项目的对比

| 项目 | Stars | 核心定位 | Harness 实现方式 | 亮点 |
|------|-------|---------|----------------|------|
| **learn-claude-code** | 67.6K | Harness engineering 教学 | bash + CLAUDE.md | 零依赖，最纯粹的 harness 实践 |
| ponytail | 50.4K | YAGNI coding agent skill | Python skill system | 极致精简代码（80-94% 代码减少）|
| darrenhinde/openagentscontrol | 4.3K | Plan-first gate | Multi-agent orchestration | approval gate 权限控制 |
| anthropic/claude-code | 16.8K | 官方 Claude Code | Python + MCP | 官方 reference implementation |

笔者认为，learn-claude-code 和 ponytail 实际上代表了 Harness 工程的两个极端：
- **learn-claude-code**：教学向，最彻底的 harness 设计哲学
- **ponytail**：极致精简向，用最少的代码实现 harness

两者都值得深入研究，区别在于你关心的是**理解 harness 原理**还是**最小化 harness 实现**。

---

## 核心工程要点

### nano Claude Code 的 tool 设计原则

项目总结的 tool 设计原则：

1. **Atomic**：每个 tool 只做一件事
2. **Composable**：tool 之间可以组合
3. **Clearly described**：tool 描述必须清晰，包含参数和返回值语义
4. **Observable**：tool 执行结果必须可观测（错误处理、日志）

这四个原则看似简单，但大多数框架的 tool 实现其实都做不到——特别是"composable"和"clearly described"这两条。

### Context 管理策略

项目使用文件系统作为 context 管理的媒介：

```
workspace/
  .context/        # 跨会话状态
  .memory/         # agent 的长期记忆
  .skills/         # 加载的 skill 集合
  .state/          # 当前任务状态
```

笔者认为，这个设计的巧妙之处在于**完全依赖 LLM 本身对文件系统的理解能力**，不需要额外的 vector store 或 RAG pipeline。当模型对文件系统的理解能力足够强时，这比任何外部记忆系统都简单。

### Security/Permission 模式

项目实现了轻量级的 permission hook：

```bash
# Permission check before dangerous operations
check_permission "shell:rm -rf" || reject "Operation not permitted"
check_permission "network:curl" || reject "Network access not allowed"
```

笔者认为，这个模式比大多数"安全框架"更务实：**安全不是加一个库就能解决的，而是要在 Harness 层显式建模每个 permission**。

---

## 什么时候用这个项目

**适合**：
- 想从第一性原理理解 Agent Harness 设计
- 需要一个最小化的 Claude Code-like 实现参考
- 想搭建自己的 nano coding agent，但没有 Heavy framework 洁癖

**不适合**：
- 需要开箱即用的生产级 coding agent（用 Claude Code 官方版）
- 需要多语言/多框架集成的复杂场景
- 需要长期维护的企业级方案

---

## 关键金句

> *"The model decides. The harness executes. The model reasons. The harness provides context. The model is the driver. The harness is the vehicle."*

> *"You cannot engineer agency into existence. Agency is learned, not coded."*

---

**关联 Article**：本文与「Claude Code /goal: 让 Evaluator Loop 成为一等公民」形成互补——evaluator loop 是 Harness 的核心机制，而 learn-claude-code 展示了如何用 bash 从零实现 Harness。

**引用来源**：
- README: `https://github.com/shareAI-lab/learn-claude-code`
- Star history: `https://www.star-history.com/shareai-lab/learn-claude-code`
- SkillsLLM: `https://skillsllm.com/skill/learn-claude-code`
