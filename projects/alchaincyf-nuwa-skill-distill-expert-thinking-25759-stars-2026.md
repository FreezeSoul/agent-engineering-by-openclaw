# alchaincyf/nuwa-skill：蒸馏任何人的思维方式（25K Stars）

> **GitHub**: https://github.com/alchaincyf/nuwa-skill
> **Stars**: 25,759 ⭐（持续增长中）
> **License**: MIT
> **Language**: Python
> **Topics**: agent-skill
> **Cluster**: `agent-skill/expert-distillation`

---

## 核心命题

nuwa-skill（女娲.skill）解决了一个根本问题：**如何把任何领域专家的思维方式蒸馏成一个可复用的 Agent Skill？**

传统 Agent Skill 是「程序化的 SOP」（比如「按这个步骤写代码」、「按这个模板生成报告」）。nuwa-skill 想做的是更高维度的事——**蒸馏「人」**：

> 「你想蒸馏的下一个员工，何必是同事。去蒸馏乔布斯、马斯克、芒格、费曼、马斯克。只需输入一个名字，女娲自动完成调研、提炼、验证全流程。」

这个项目的真正野心，是把「专家思维」变成 AI Agent 可以加载的 Skill 模块——从此一个 Agent 可以是「乔布斯 + 芒格 + 费曼」三合一。

---

## 工作机制：3 阶段蒸馏流程

nuwa-skill 的核心流程是 3 阶段蒸馏：

### 阶段 1：调研（Research）

输入一个专家名字（例如「芒格」），nuwa-skill 自动：
- 抓取该专家的全部公开内容（演讲、采访、书籍、文章）
- 整理其核心观点的演变轨迹
- 提取标志性思维模型（如芒格的「逆向思考」、费曼的「第一性原理」）

### 阶段 2：提炼（Distillation）

从调研材料中提炼出该专家的：
- **心智模型**：面对问题时如何思考（如芒格的多学科思维格栅）
- **决策启发式**：在不确定下如何决策（如芒格的「反过来想」）
- **表达 DNA**：如何用语言传递思想（如乔布斯的「极简叙事」）

### 阶段 3：验证（Verification）

通过模拟情境来验证蒸馏的准确性：
- 用蒸馏出的芒格 Skill 回答一个商业问题
- 与芒格本人的真实观点做对比
- 偏差过大则重新蒸馏

---

## 标准化与生态

nuwa-skill 基于开放的 [Agent Skills 协议](https://agentskills.io)，兼容 50+ Agent Runtime：

| Runtime | 兼容 |
|---------|------|
| Claude Code | ✅ |
| Codex | ✅ |
| Cursor | ✅ |
| OpenClaw | ✅ |
| Hermes Agent | ✅ |
| CodeBuddy | ✅ |
| Workbuddy | ✅ |
| Gemini CLI | ✅ |
| OpenCode | ✅ |
| ... | 50+ |

这意味着一个 nuwa-skill 蒸馏出的「芒格 Skill」可以在多个 Agent 平台无缝使用。

---

## 项目结构（基于 README 推断）

```
nuwa-skill/
├── skills/                  # Skill 库
│   ├── jobs.skill/          # 乔布斯 Skill
│   ├── musk.skill/          # 马斯克 Skill
│   ├── munger.skill/        # 芒格 Skill
│   └── feynman.skill/       # 费曼 Skill
├── distill/                 # 蒸馏引擎
│   ├── research.py          # 调研阶段
│   ├── distill.py           # 提炼阶段
│   └── verify.py            # 验证阶段
├── runtime/                 # 多 Runtime 适配
│   ├── claude_code.py
│   ├── codex.py
│   └── cursor.py
└── README.md
```

---

## 关键洞察

### 1. Skill 模块化是新趋势

nuwa-skill 与 Anthropic Skills、OpenAI Codex Skills 属于同一趋势——**把 AI Agent 的能力模块化**。不同点：
- Anthropic Skills：是 SOP（如「按这个步骤 review 代码」）
- Codex Skills：是工作流（如「按这个流程写 spec」）
- **nuwa-skill：是人格/思维模型**（如「像芒格这样思考」）

后者是更高维度的抽象——它捕获的不是"做什么"，而是"如何想"。

### 2. 与「同事.skill」的进化关系

nuwa-skill 的前身是 [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)——蒸馏一个具体同事的思维方式。nuwa-skill 把这个想法推到极限：**蒸馏任何有名有姓的人**，包括历史人物和公众人物。

> 「同事.skill 证明了蒸馏一个人是可行的。那何必蒸馏同事？去蒸馏乔布斯、芒格、费曼、马斯克。」

### 3. 与 GPT-5 + Derya 案例的对照

nuwa-skill 与 [GPT-5 + 免疫学家 Derya 案例](../../articles/case-studies/openai-gpt5-immunology-mystery-derya-unutmaz-2026.md) 属于同一个 cluster：**AI 捕获/放大人类专家**。但路径不同：

| 维度 | GPT-5 + Derya | nuwa-skill |
|------|--------------|-----------|
| 模式 | 实时协作 | 离线蒸馏 |
| 输入 | 实时对话 | 公开内容 |
| 输出 | 实验建议 | 可复用 Skill |
| 时效 | 即时 | 沉淀 |
| 适用场景 | 一次性难题 | 持续性决策 |

两者互补：nuwa-skill 适合「把芒格的思维方式变成我可以随时调用的 Skill」，GPT-5 适合「在面对具体问题时与我实时协作」。

---

## 局限与风险

### 1. 蒸馏的准确性问题

nuwa-skill 的核心假设是「公开内容可以准确反映一个人的思维方式」。但实际上：
- 公开内容是被编辑过的（书籍经过编辑、演讲经过 PR 润色）
- 思维模型的细节很难完全公开（很多判断是直觉）
- 历史人物的「真实想法」往往难以考证

### 2. 简化问题

「乔布斯式思考」这种表述本身就有过度简化的嫌疑。一个人的思维方式远比标签复杂，蒸馏为 Skill 可能丢失关键细节。

### 3. 责任归属

如果基于「芒格 Skill」做出投资决策导致亏损，责任在谁？这是 nuwa-skill 普及前需要回答的伦理问题。

---

## 与其他 Skill 项目的对比

| 项目 | 蒸馏对象 | 输出 | Stars |
|------|---------|------|-------|
| titanwings/colleague-skill | 同事 | Skill | ~1K |
| alchaincyf/nuwa-skill | 任何人 | Skill | 25.7K |
| anthropics/skills | SOP | Skill | (官方) |
| openai/codex-skills | 工作流 | Skill | (官方) |

nuwa-skill 是「人格蒸馏」维度的领先开源项目。

---

## 结论

nuwa-skill 代表了 AI Agent 工程的下一个前沿：**把人类专家的思维方式蒸馏成可复用的 Skill 模块**。

对 Agent 工程师的启示：
1. **Skill 模块化是趋势**——从 SOP 到工作流到人格，抽象层级在提升
2. **思维模型比流程更值钱**——芒格的「逆向思考」比任何 SOP 都有价值
3. **可验证性仍是基础**——蒸馏出的 Skill 是否真的反映专家思维，需要持续验证

随着 nuwa-skill 这类项目的成熟，未来的 Agent 将不再是「通用助手」，而是「领域专家合集」——你可以同时调用芒格 + 乔布斯 + 费曼来做一个决策。

---

> **关联 Article**：[GPT-5 与免疫学家 Derya：3 年悬案的生成式破局](../case-studies/openai-gpt5-immunology-mystery-derya-unutmaz-2026.md) — 两者属于同一 cluster：AI 捕获/放大人类专家。Article 是实时协作（GPT-5 实时辅助 Derya），本 Project 是离线蒸馏（nuwa-skill 把专家思维变成 Skill 模块），构成"AI 沉淀专家知识"的两种路径。