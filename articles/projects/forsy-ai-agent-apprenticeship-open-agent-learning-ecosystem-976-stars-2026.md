# Forsy-AI/agent-apprenticeship：将执行转化为学习的 Agent 进化生态

**Stars**: 976 (2026-06-27) | **License**: MIT | **Language**: TypeScript/Node.js | **Repo**: [github.com/Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship)

> 每一个被执行的真实任务，都是未来 Agent 的教材。Agent Apprenticeship 是第一个将这个直觉工程化为开放生态系统的开源项目。

---

## 核心命题

当前 Agent 领域有一个被忽视的结构性缺失：每个团队、每个 Agent 实例都在独立积累执行经验，但这些经验无法跨实例复用。Cursor 的 Claude Code 用法经验留在 Cursor 里，Anthropic 的 Human-Agent Teams 最佳实践锁在内部文档里。**真实世界的 Agent 执行，本可以成为整个社区的学习养料，但它们全都流失了。**

Agent Apprenticeship 试图解决这个问题。它的核心命题是：**当 Agent 执行了真实任务，这些执行本身应该自动成为可检索、可复用、可贡献给生态系统的学习单元。** 这不是另一个 "prompt 分享平台"，而是一套完整的 Agent 执行 → 学习信号 → 改进 → 新执行的闭环工程机制。

---

## 技术架构

### Apprentice-Mentor 双层架构

Agent Apprenticeship 实现了 Apprentice-Mentor 分离设计：

```
Apprentice Agent (执行者)
  ↕ 执行结果 + 轨迹
Mentor Model (指导者)
  ↕ 反馈 + 改进建议
  ↓
Experience Bundle (学习单元)
```

**Apprentice Agent** 可以是：Claude Code、Cursor、Codex、OpenClaw、OpenCode、Hermes Agent，或任何自定义 Agent。系统通过 CLI 检测已安装的 Agent，无需修改 Agent 本身。

**Mentor Model** 是独立的指导模型，通过三种模式工作：

- **`model-assisted`**：Mentor 模型自动指导 Apprenticeship loop
- **`expert-led`**：人类专家 checkpoint 驱动指导 loop
- **`hybrid`**：模型起草 + 人类专家审核

这与 R555 Anthropic Human-Agent Teams 文章中的 "Doer-Verifier" 模式有异曲同工之处，但扩展了角色：Apprentice Agent = Doer，Mentor Model = Verifier + Teacher 的混合体。

### Experience Bundle 系统

每次 `apprentice run` 完成后，系统生成一个 **Contribution Bundle**，包含：

```bash
# 产出的 bundle 结构
{
  "task": "Create a short market map for AI procurement tools.",
  "traces": [...],      # 完整执行轨迹
  "lessons": [...],     # 从执行中提取的教训
  "artifacts": [...],   # 生成的工件
  "experience_pack_id": "aa-seed-task-501"
}
```

Bundle 可以：
- 本地存储供后续使用
- 通过 `apprentice ecosystem contribute` 贡献给公共生态
- 通过 `apprentice learn create` 转化为 Experience Pack 供未来任务使用

### Ecosystem 共享机制

公共生态系统（[github.com/Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship)）包含：

- **500+ curated seed tasks**：来自真实世界的任务
- **495 reusable agent lessons**：从执行中提取的教训
- **1000+ full agent execution traces**：完整执行轨迹
- **1000+ agent work episodes**：任务 rollouts

贡献者通过 `gh` CLI 认证后，可以将本地 Bundle 贡献到生态系统：

```bash
apprentice ecosystem contribute <bundle_path>
apprentice ecosystem configure --auto-share automatic  # 可选自动分享
```

### 与 R555 Anthropic Human-Agent Teams 的关联

R555 分析了 Anthropic 的 "Building effective human-agent teams"（2026-06-24），其中四条工程纪律是：

1. **Work in public**：Agent 只能从文本学习，安全边界 = 访问边界
2. **Defined role with tools**：每个 Agent 有独立凭证、skills、工具权限
3. **North star**：雄心勃勃的目标 + selective delegation
4. **Trust over time**：自主权按"已证明可靠性"按比例授予

Agent Apprenticeship 在开放生态层面实现了同样的原则：

- **Work in public** → 任何 Agent 的执行都可以贡献到公共 ecosystem
- **Defined role** → Apprentice Agent 角色固定（执行者），Mentor 角色固定（指导者）
- **North star** → 任务级别的经济价值评估（"task-level economic value"）
- **Trust over time** → 经验积累越多，Experience Pack 质量越高，生态价值越大

Anthropic 的 Human-Agent Teams 是组织内的 multiplayer agent 操作实践，Agent Apprenticeship 是跨组织的 agent 学习生态系统。**两者解决的是同一个问题（如何让 Agent 从真实执行中学习和改进），只是作用域不同。**

---

## 使用方式

### 快速开始

```bash
# 安装
npx agent-apprenticeship init
# 或
npm install -g agent-apprenticeship

# 检测已安装的 Agent（Claude Code/Cursor/Codex等）
apprentice doctor

# 配置 Mentor Model Provider
apprentice configure model

# 运行第一个任务
apprentice run "Create a short market map for AI procurement tools."

# 将执行经验贡献给生态系统
apprentice ecosystem contribute <bundle_path>
```

### 从生态系统学习

```bash
# 搜索相关经验
apprentice ecosystem search cloud

# 查看具体经验包
apprentice ecosystem inspect aa-seed-task-501

# 拉取并使用
apprentice ecosystem pull aa-seed-task-501

# 转化为 Experience Pack
apprentice learn create aa-seed-task-501

# 在新任务中使用
apprentice run "Create a release checklist." --experience-pack <pack_id>
```

---

## 为什么值得关注

### Agent Engineering 视角

Agent 领域目前有两个相互矛盾的趋势：

1. **执行越来越自主**：Claude Code、Cursor、Copilot 等 Agent 能独立完成越来越长的任务
2. **学习仍然是手动的**：Agent 从执行中学到什么，取决于人类事后 review

Agent Apprenticeship 试图自动化这个学习回路。它不是又一个 "Awesome Prompts" 列表，而是一套让 Agent 执行自动产生可复用学习信号的基础设施。

笔者认为，这代表了 Agent Engineering 的一个重要方向：**Harness 不只是让 Agent 正确执行，还应该让执行产生学习价值。** 传统的 harness 关注的是 stop condition、guardrail、checkpoint；Agent Apprenticeship 增加了一个新的 harness 维度——**学习信号提取**。

### 生态构建策略

与许多 "SDK + 文档" 的开源项目不同，Agent Apprenticeship 从第一天就有 seed dataset（500+ tasks，1000+ traces）。这种策略让它不是一张白纸开局，而是一个已经有内容、可以被 immedately 使用的生态系统。

支持的 Apprentice Agents 列表（Claude Code、Cursor、Codex、OpenClaw、OpenCode、Hermes Agent）也说明项目方在赌一个多 Agent 并存的世界，而非所有用户都用同一个 Agent。

---

## 局限与已知问题

1. **多 Agent 共存世界的假设尚未验证**：虽然列出了 7 种 Agent 支持，但实际支持深度参差不齐（Claude Code/Codex 有官方对接，其他可能需要 custom command template）
2. **Mentor Model 的质量依赖**：model-assisted 模式下，Mentor Model 的指导质量直接影响学习信号的价值
3. **贡献激励机制缺失**：auto-share 默认关闭，手动贡献依赖贡献者自觉，生态系统增长依赖网络效应
4. **执行轨迹的隐私问题**：真实任务的执行轨迹可能包含敏感信息，直接贡献到公共 ecosystem 有隐私风险

---

## 竞品对比

| 项目 | 定位 | 优势 | 劣势 |
|------|------|------|------|
| **Agent Apprenticeship** | Agent 执行 → 学习生态系统 | 开源、跨 Agent、多 Mentor 模式 | 新项目（2026-06），生态待建立 |
| **LangSmith/LangFuse** | Agent 可观测性 | 生产级、成熟 | 面向开发者，非 Agent 自主学习 |
| **dify** | Agent 构建平台 | 功能完整 | 非学习导向，专注工作流 |
| **OpenHands** | Agent 框架 | 通用性强 | 无生态共享机制 |

---

## 适用场景

**适合使用 Agent Apprenticeship 的场景**：
- 团队内部多个 Agent 实例，需要共享执行经验
- 研究 Agent 学习机制，需要真实执行轨迹数据集
- 构建 Agent 培训流程，需要标准化任务集和评估基准

**不适合的场景**：
- 敏感任务（执行轨迹无法公开）
- 单 Agent 使用、无共享需求（ overhead 大于收益）
- 需要生产级稳定性的场景（项目仍处于早期）

---

## 结论

Agent Apprenticeship 是 2026 年中值得关注的新项目，它试图在 "Agent 执行" 和 "Agent 学习" 之间建立自动化的桥梁。976 Stars（6 天内）和 MIT License 使其成为当前 Agent Engineering 生态中一个值得跟踪的实验。

笔者认为，它的意义不在于现在能做什么，而在于它提出的问题：**当每个 Agent 的执行都可以成为学习养料时，Agent 的进化速度会提升多少？** 这个问题的答案，将决定 Agent Apprenticeship 最终是 "又一个开源实验" 还是 "Agent Engineering 的基础设施"。