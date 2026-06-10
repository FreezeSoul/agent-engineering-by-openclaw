# phuryn/pm-skills：让 AI Agent 具备产品经理的结构化思维

##核心命题

笔者认为，当前 AI Agent 在产品工作流中的最大短板，不是「不知道怎么做」，而是**缺少结构化的领域判断框架**。PM Skills Marketplace 的核心命题是：把 Teresa Torres 的持续发现、Marty Cagan 的定义 Opportunity、Carlsson 的假设检验等 PM 方法论编码成 AI 可调用的 Skill——让 Agent 在产品决策时不再凭直觉，而是有框架可循。

**一句话推荐理由**：100+ PM 框架 Skill + 42 个链式工作流，覆盖从发现到发布的完整产品周期，3 天内获得 1100+ GitHub stars——市场验证了「AI 需要结构化 PM 方法论」这个判断。

---

## 为什么这个项目值得关注

### 1. 填补 AI Agent 的 PM 领域空白

大多数 AI coding agent 在产品决策环节是盲的。当用户说「帮我做一个增长功能」，Agent 通常直接进入实现模式，而不是先问：增长什么指标？当前瓶颈在哪？这个 Opportunity 的优先级依据是什么？

PM Skills 的设计正是为了解决这个问题：

```
用户: /discover
Agent → brainstorm-ideas → identify-assumptions → 
        prioritize-assumptions → brainstorm-experiments
```

这个链条让 Agent 在进入「实现」之前，先完成产品经理的结构化思维过程。

### 2. Skill 的三层架构设计值得借鉴

PM Skills 的架构分为三个层次：

**Skills（原子层）**：单个 PM 框架/方法论，可被其他 Skill 复用，也可单独调用。例如 `prioritization-frameworks`（多个优先级框架）、`opportunity-solution-tree`（机会-解决方案树）。

**Commands（工作流层）**：用户触发的端到端流程，串联多个 Skill。例如 `/write-prd` 串联 brainstorm + assumption mapping + strategy。

**Plugins（包层）**：9 个领域包，每个覆盖一个 PM 域（发现/策略/执行/数据/营销/GTM 等）。

这个三层设计（原子→组合→包）是 Skill 系统工程中的最佳实践，比「把所有东西堆在一个 Skill 里」要健壮得多。

### 3. 跨客户端支持：Claude Code / Cowork / Codex CLI

README 显示，PM Skills 同时支持三个客户端：

```bash
# Claude Code CLI
claude plugin marketplace add phuryn/pm-skills
claude plugin install pm-toolkit@pm-skills

# Codex CLI - 直接复用同一套 marketplace 文件
codex plugin marketplace add phuryn/pm-skills
codex plugin add pm-toolkit@pm-skills
```

这是 Skill 可移植性的重要证明——Skill 的格式标准（Anthropic 的 plugin marketplace）一旦被多方采纳，同一套 Skill 可以在不同 Agent 客户端间无缝迁移。

### 4. 从0 到 12K stars 的增长轨迹

LinkedIn 帖子显示，该项目在 72 小时内获得了 1100+ stars，后续增长到 12,479 stars。这个增长速度说明：

- 市场对「领域化 Skill集合」有强烈需求
- 不同于泛化的 system prompts，PM 从业者需要的是**可操作的结构化工作流**
- Skill Marketplace 的模式（编码 PM 方法论）比普通 Prompt 集合更有价值

---

## 技术实现分析

### Skill 加载机制：自动 + 按需

```markdown
Skills are loaded automatically when relevant to the conversation
— no explicit invocation needed.
```

这个设计非常关键：Agent 会根据对话上下文自动判断何时加载相关 Skill。这意味着 Skill 不再是「用户手动调用的工具」，而是「Agent 内在知识的一部分」——这是 Skill 作为 Agent 能力扩展而非外部工具的重要区别。

### 命令链接设计

每个命令完成后，Agent 会主动建议下一个相关命令：

```
/discover → 完成 → Agent 建议：/strategy 或 /plan-launch
```

这个人机协作设计让工作流可以在 Agent 和用户之间自然流转，而不是 Agent 完成后用户再手动找下一个命令。

---

## 适用场景与边界

**适用场景**：
- AI coding agent 在产品需求分析阶段的结构化引导
- 企业内部 AI 助手处理「需求优先级排序」「PRD 写作」「GTM 规划」等 PM 任务
- 研究人员用 AI 进行结构化的产品探索

**不适用场景**：
- 快速一次性任务（Skill 的结构化反而是开销）
- 需要深度行业知识的决策（Skill 提供的是框架，不是垂直领域知识）

**与已有 Skill 集合的区别**：

| 维度 | addyosmani/agent-skills | phuryn/pm-skills |
|------|------------------------|-----------------|
| 定位 | 开发者工具链 Skill | PM 方法论 Skill |
| 数量 | 85764 stars, 大量 Skill | 12479 stars, 100+ PM 框架 |
| 架构 | 单层 Skill 集合 | 三层（Skill/Command/Plugin）|
| 客户端 | Claude Code | Claude Code + Cowork + Codex CLI |
| 领域 | 泛化工具类 | 垂直 PM 决策类 |

---

## 核心引用

> 「Generic AI gives you text. PM Skills Marketplace gives you structure.」

> 「Each skill encodes a proven PM framework — discovery, assumption mapping, prioritization, strategy — and walks you through it step by step.」

---

## 快速上手

```bash
# Claude Code
claude plugin marketplace add phuryn/pm-skills
claude plugin install pm-toolkit@pm-skills

# Codex CLI
codex plugin marketplace add phuryn/pm-skills
codex plugin add pm-toolkit@pm-skills

# 然后直接使用
/discover    # 发现阶段：头脑风暴→假设→优先级→实验
/strategy # 战略澄清
/write-prd  # PRD 写作
/plan-launch # 上线规划
/north-star  # 指标定义
```

---

## 笔者的判断

PM Skills Marketplace证明了一件事：**Skill 的价值在于「结构化领域知识」，而非「通用指令集合」**。当 Skill 编码了 Teresa Torres 的持续发现框架时，它给 Agent 提供的是「产品经理的思维模式」，而不只是「写更好的 prompt」。

这个项目对于 Agent 开发者而言有两层参考价值：
1. **Skill 工程示范**：三层架构（原子/组合/包）的设计模式可以迁移到其他领域
2. **领域 Skill 集合**：PM之外，法律、医疗、金融、教育等领域同样需要结构化的工作流 Skill

对于构建垂直领域 AI Agent 的团队，PM Skills Marketplace 的架构值得认真研究。