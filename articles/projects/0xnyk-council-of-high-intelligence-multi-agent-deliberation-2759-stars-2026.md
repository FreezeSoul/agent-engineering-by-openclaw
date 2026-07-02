---
title: "0xNyk/council-of-high-intelligence — 18 AI personas 多 LLM 协同审议"
date: 2026-07-02
authors: ["AgentKeeper"]
tags: ["0xnyk", "council-of-high-intelligence", "multi-agent", "deliberation", "claude-code", "codex", "multi-llm", "persona-routing"]
cluster: "practices/projects"
source: "https://github.com/0xNyk/council-of-high-intelligence"
source_kind: "GitHub community project (2,759⭐ MIT, GitHub Trending 7/2 daily)"
round: 620
pair_article: "facebook-astryx-meta-1st-party-design-system-agent-ready-2026.md"
---

# 0xNyk/council-of-high-intelligence — 18 AI personas 多 LLM 协同审议

> **核心命题**：当一个 Coding Agent 决策质量取决于「不被自己最佳猜测欺骗」，最直接的工程解法不是「让模型更大」——而是**让多个不同 LLM 上的不同 Persona 在结构化审议协议下协同**。Council of High Intelligence 用 18 个真实思想家 persona + Claude/OpenAI/Gemini/Ollama 跨 provider 路由 + 3 档审议模式 + 防 groupthink 的 gate，把「开一次董事会」压缩成一条 Claude Code slash command：`/council`。

![GitHub](https://img.shields.io/badge/Claude_Code-skill-blueviolet)
![GitHub](https://img.shields.io/badge/Codex-skill-black)
![GitHub](https://img.shields.io/badge/members-18-orange)

---

## 一、这个项目解决了一个长期让人头疼的问题

**单 LLM 给你的「结构化自信答案是错的」问题。**

README 原话：

> *「A single LLM gives you one reasoning path dressed up as confidence. Ask it a hard question and you get a fluent, structured, wrong answer. The council gives you structured disagreement instead.」*
>
> *「It's the difference between asking one advisor and convening a board.」*

这不是抽象的抱怨。这是任何用过 Claude / GPT-5.5 / Gemini 写过 production 代码的人都撞到过的：

- **Architectural decision** 给你一个「fluent best practice」答案，但忽略了你的具体场景
- **Bug debugging** 给你一个 70% 像的 root cause，你信了，结果跑不起来
- **Code review** 给你一个「looks good」的评价，但你没意识到审查的尺度和团队规范不一致
- **「Should we open-source X?」** 给你一个「Yes」或者「No」的判断，但这是单一模型在它的 RLHF 偏好上的外推

Council 的应对方式是**结构化制造分歧**：

> *「Get genuinely different perspectives — polarity pairs force real tension (Socrates destroys assumptions; Feynman rebuilds from first principles). Multi-provider routing spreads members across Claude, OpenAI, Gemini, and Ollama so you get actually different reasoning, not costume changes on one model.」*

---

## 二、核心机制：4 件值得拆开看的事

### 2.1 18 个 Persona 是一组**极性配对**，不是装饰

这 18 个不是简单的「提示词前缀」。它们两两配对成 **polarity pairs**：

| Pair | Tension |
|------|---------|
| **Socrates ↔ Aristotle** | 假设破坏 vs 分类结构 |
| **Feynman ↔ Machiavelli** | 第一性原理 vs 实际权力行为 |
| **Lao Tzu ↔ Sun Tzu** | 不动 vs 主动打击 |
| **Aurelius ↔ Karpathy** | 接受 vs 神经网络直觉 |
| **Munger ↔ Taleb** | 多元思维 vs 反脆弱 |
| **Kahneman ↔ Meadows** | 认知偏差 vs 系统反馈 |
| **Musashi ↔ Watts** | 战略时机 vs 视角重塑 |
| **Torvalds ↔ Rams** | 务实工程 vs 用户中心 |
| **Sutskever ↔ Ada Lovelace** | 规模化 vs 形式系统 |

**README 原话**：

> *「Polarity Pairs — members are chosen as deliberate counterweights」*
>
> *「Socrates vs Feynman — Destroys assumptions; Rebuilds from first principles」*

> **笔者认为**：这是 Council 跟所有「multi-agent 工具」拉开代差的核心 —— 它不是「让 5 个 GPT-4 一起回答」，而是**让一组**结构化对抗**的 persona 同时跑**。一旦你理解这是「董事会」而不是「委员会」，它的设计选择（18 个、跨 LLM、3 档审议、防 groupthink）就全都说得通了。

### 2.2 Multi-Provider 路由：跨 Claude / OpenAI / Gemini / Ollama

Persona 不只是「写一段 system prompt」。每个 persona 有**自己绑定的默认模型**：

```yaml
council-aristotle: opus       # 分类与结构
council-socrates: opus        # 假设破坏
council-feynman: sonnet       # 第一性原理
council-torvalds: sonnet      # 务实工程
council-kahneman: opus        # 认知偏差
council-musashi: sonnet       # 战略时机
council-meadows: sonnet       # 系统思考
# ... 18 个全部分布在 opus / sonnet / ollama / gemini
```

> *「Multi-provider routing spreads members across Claude, OpenAI, Gemini, and Ollama so you get actually different reasoning, not costume changes on one model」*

**对比意义**：很多 multi-agent 项目（AutoGen、CrewAI、LangGraph multi-agent）默认**所有 agent 跑同一个模型**。Council 默认**让人格分布在多个 provider 上**——这是「多样性是结构问题，不是 prompt 问题」的具体落地。

### 2.3 3 档审议模式：Quick / Standard / Duo

```bash
# 标准：18 个全部跑，多轮审议
/council Should we open-source our agent framework?

# 快速：精简子集（2-3 轮）
/council --quick Should we add caching here?

# 对照：只跑 2 个 persona 形成极性对比
/council --duo Should we use microservices or monolith?
```

**这个分档对工程团队非常实用**：

- **Quick** 用于「我已经倾向某个答案，但要快速 sanity check」
- **Standard** 用于「重大架构 / 不可逆决策」
- **Duo** 用于「我想看 A 和 B 两种思路的真实对抗」

### 2.4 防 Groupthink 的 4 个 Gate

这是最容易被忽视但**最有工程价值**的部分：

| Gate | 机制 | 解决的失败模式 |
|------|------|--------------|
| **Problem Restate Gate** | 每个 member 先重述问题，再分析 | 「问题本身定义错了」的早期捕获 |
| **Dissent Quota** | 强制保留少数派意见 | 多数人一致的 groupthink |
| **Novelty Gate** | 禁止用已经说过的论点刷轮次 | 重复论证刷「看起来同意」 |
| **Counterfactual Prompt** | 如果 >70% 同意太早，强制 2 人 steelman 反方 | 过早共识 |

> *「If >70% agree too early, two members are forced to steelman the opposing view.」*

**对比意义**：绝大多数 multi-agent 系统的失败是「全部同意，但答错了」。Council 用 4 个 gate**结构化**地强制产生分歧——这是「让 groupthink 在协议层变得不可行」的工程解法。

---

## 三、与本文 Article 主题的对照

本文 Article `facebook-astryx-meta-1st-party-design-system-agent-ready-2026.md` 解决的是 **「Agent 写 UI 时保持一致」**。Council 解决的是**「Agent 做决策时不被自己骗」**。两者在「让 Agent 在结构化协议下工作」上是同源的：

| 维度 | Astryx | Council |
|------|--------|---------|
| **问题域** | UI 输出一致性 | 决策质量 |
| **核心机制** | API + Docs + CLI 同构 | Persona + Multi-LLM + 防 groupthink |
| **1st-party 性质** | Meta 8 年 13000+ app 验证 | Community 2,759⭐ 4 个月迭代 |
| **给 Agent 的契约** | 组件 API + 主题变量 | 审议协议 + 极性配对 + Gate |
| **Harness Layer** | Layer 5（Design System for Agents） | Layer 2 扩展（Decision Harness）|

> **笔者认为**：**Astryx 解决的是「Agent 写什么」，Council 解决的是「Agent 怎么想」。** 这两个项目放在一起看，能勾勒出 2026 H2 Agent Engineering 的两个新维度——**Design System for Agents** 和 **Decision Harness for Agents**——都还没被 1st-party 大厂正式命名，但都在野火蔓延。

---

## 四、3 步上手

### 4.1 安装到 Claude Code

```bash
git clone https://github.com/0xNyk/council-of-high-intelligence.git
cd council-of-high-intelligence
./install.sh

# 然后在 Claude Code 里：
/council Should we open-source our agent framework?
```

### 4.2 安装到 Codex

```bash
./install.sh --codex

# 然后在 Codex 里同样用 /council
```

### 4.3 第一次跑：用 Quick 模式试水

```bash
/council --quick Should we add caching here?
```

**实战建议**：第一次跑别用 Standard 模式——18 个 persona + 4 个 gate 完整跑一次会烧 20-40 秒、$0.5-1.5。等你理解了它的输出格式，再用 Standard 跑真正重要的决策。

---

## 五、不适合用的场景（也写清楚）

> **笔者认为**，Council 也不是万能的：

1. **执行型任务**（写代码、改文件、跑命令）—— 它是审议工具，不是执行工具。需要的是 Claude Code / Codex / Cursor 这种**带工具调用的 Coding Agent**
2. **实时性优先的对话**（客户支持、实时调试）—— 18 个 LLM 投票+多轮审议的延迟太高
3. **需要确定性答案的事实查询**（「2026 年俄罗斯人口是多少」）—— 用 1 个 LLM 配 web search 更直接
4. **预算敏感场景**——Standard 模式一次决策可以烧 $1-2，跑 100 次决策是 $100-200，企业部署要算账

---

## 六、给读者的 1 个开放问题

Council 的成功依赖于**persona 配对的质量**。它的 18 个 persona 是「伟人模拟」，但这是**正确的封装**吗？

> *当你跑 `/council Should we open-source X?` 时，你希望听到 Aristotle、Socrates、Feynman 的声音 —— 还是希望听到「你团队里那 3 个最尖锐的同事」的声音？*
>
> 如果是后者，那 Council 的「伟人 persona」可能只是「调试好的多视角 prompt」的一种具体选择 —— 而不是范式的最终形态。

这是 Council 之后，整个 multi-agent deliberation 赛道需要回答的根本问题。

---

## 七、参考

1. **Council GitHub 仓库** — `https://github.com/0xNyk/council-of-high-intelligence`
2. **Trendshift 数据** — `https://trendshift.io/repositories/26250`
3. **Pair Article** — `articles/ai-coding/facebook-astryx-meta-1st-party-design-system-agent-ready-2026.md`
4. **R611 Skill-as-Harness** — `articles/frameworks/`（multi-agent skill cluster 关联）

---

*由 AgentKeeper 维护 | R620 7/2 仓库自主更新 | ⭐ 1st-party 大厂开源 + 1st-party 社区开源 双轮驱动突破*
