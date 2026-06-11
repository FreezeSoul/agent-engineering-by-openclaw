# Leonxlnx/taste-skill：给 AI 前端输出注入"编辑品味"

>40K Stars · MIT License · Shell · [GitHub](https://github.com/Leonxlnx/taste-skill) · [tasteskill.dev](https://tasteskill.dev)

---

## 核心命题

**AI 生成的前端为什么总是"一股 AI 味"？** 不是模型不够强，而是 AI 在生成时没有任何风格约束——它只是在最大化"看起来正确"的概率，而不是最大化"看起来有品味"的概率。Taste-Skill 是第一个系统性地解决这个问题的大规模开源项目：它不是改进模型，而是在模型之外加了一层**强制风格引擎**。40K Stars 的爆炸增长说明，整个行业已经受够了 AI 生成的那些"模板化垃圾"（Slop）。

---

## 一、为什么 AI 前端输出总是一个样子

在 Taste-Skill 出现之前，所有 AI 编程工具（Cursor、Claude Code、Codex、Gemini CLI、v0、Lovable）在生成前端时有一个共同的失效模式：

**它们默认生成的是"最不容易出错"的布局，而不是"最有设计感"的布局。**

原因很简单：AI 训练数据中的前端代码，大量是"能跑就行"的业务代码——后台管理系统、表单页面、内部工具。这些代码的特征是：
- 标准的 Bootstrap / Tailwind 默认样式
- 紫色渐变 +白色卡片（AI 生成的金字招牌）
- 居中排列 + 中规中矩的间距
- 没有字体层级、没有动效、没有呼吸感

当 AI 被要求"做一个好看的网页"时，它实际上只是在从这些"安全"的训练数据中做内插。

Taste-Skill 的创始人[lexnlin]做了一个测试：给不同的 AI agent 相同的 brief，不加任何风格约束，生成的结果几乎一模一样——都是"AI Slop"的典型特征。加上 Taste-Skill 的规则之后，同样的 AI 生成了完全不同的结果：瑞士字体、实验性布局、真正的设计系统。

**这不是模型能力问题，这是风格约束缺失问题。**

---

## 二、技术原理解析

Taste-Skill 的设计哲学是：**规则引擎 > 微调模型**。与其让模型"学会"有品味（需要大量高质量设计数据，微调成本高），不如在模型输出之后加一层硬性规则检查。

### 2.1 v2 核心机制：三参数调优

v2 版本引入了三个核心设计参数，直接内嵌在 SKILL.md 中：

```bash
# 三参数系统
VARIANCE  # 设计多样性：越高越实验性，越低越安全
MOTION    # 动效强度：越高越丰富，越低越克制
DENSITY   # 信息密度：越高越紧凑，越低越留白
```

Agent 在生成之前读取 brief，推断正确的参数值，然后生成符合该风格方向的前端代码。这比单纯的"做好看点"要精确得多——**品味不是模糊的偏好，而是可参数化的约束**。

### 2.2 Anti-Slop 规则集

v2 还包含了一系列硬性禁止规则（Anti-Slop Rules），比如：

> "禁止使用 `--em dash--` 作为装饰性分隔符"

这是 Taste-Skill 团队发现的一个 AI Slop 特征——当 AI 不知道用什么分隔符时，总喜欢用超长的 em dash 作为"看起来有设计感"的装饰。这些规则把 AI 从"懒惰的默认行为"中拉回来。

### 2.3 GSAP 代码骨架

对于需要动效的前端，Taste-Skill 提供了**规范的 GSAP 代码骨架**——不是贴一大段代码，而是给出动效的"结构模板"，让 AI 在正确的位置填入正确的参数。这解决了 AI 生成动效代码时"要么没有，要么乱加"的问题。

### 2.4 Image-to-Code Pipeline

Taste-Skill 还提供了 image-to-code 的 pipeline：

```
设计图片（参考板）→ AI 分析图片设计语言 → Coding Agent 实现
```

这个 pipeline 的关键是：图片分析由专门的 skill 完成（imagegen-frontend-web / imagegen-frontend-mobile），coding 由另一个 agent 完成。**关注点分离**，每个 skill 做一件事。

---

## 三、与其他方案的对比

| 维度 | Taste-Skill | 模型微调 | Prompt约束 |
|------|------------|---------|-----------|
| **实现方式** | 外部规则引擎（SKILL.md） | 训练层 | 提示词层 |
| **部署成本** | 极低（npx 一行安装） | 极高（GPU + 数据） | 低 |
| **可控性** | 精确参数控制 | 不可控（概率生成） | 模糊 |
| **对模型的要求** | 任意模型均可 | 需要基础模型 | 需要强模型 |
| **适用场景** | 所有 AI Coding工具 | 单一模型 | 单一模型 |
| **维护方式** | SKILL.md 规则文件 | 重新训练 | Prompt 工程 |

笔者认为，Taste-Skill 代表的"规则引擎"路径，在当前阶段比"模型微调"路径更实用。原因：**风格约束是可移植的，模型风格是不可移植的**。一个 SKILL.md 文件可以在 Cursor、Claude Code、Codex、Gemini CLI、v0、Lovable 上通用，而微调一个模型只能服务于一个模型。

---

## 四、适用场景

Taste-Skill 最适合以下场景：

- **需要独特设计语言的产品官网**：不要 AI 生成"模板官网"，而是要一个有品牌辨识度的前端
- **Design System初始化**：用 image-to-code pipeline 先生成参考板，再让 coding agent 实现
- **现有项目的 UI 审计与改进**：用 redesign-skill 审计现有代码，发现 layout/spacing/hierarchy 问题
- **多 Agent 设计**：设计师 agent 生成图片，coding agent 实现——Taste-Skill 作为中间层保证风格一致性

**不适合的场景**：
- 内部工具、后台系统（不需要品味，只需要功能）
- 需要精确品牌指南的企业级项目（需要人工设计系统，Taste-Skill 不能替代）

---

## 五、工程启示：风格即约束

Taste-Skill 最重要的工程启示不是它本身，而是它揭示的一个更大规律：

**AI Agent 的输出质量 = 模型能力 ×约束精确度**

当 AI 缺乏约束时，它的输出会收敛到"最安全的默认行为"。当有精确约束时，它才能在设计空间中找到有价值的点。这与 Deep Learning 的 Dropout 机制有异曲同工之妙——随机性让模型探索，约束让模型不收敛到局部最优解。

在 Agent 工程中，我们花了大量时间设计 Tool Use、RAG、Harness，却很少花时间设计**输出层的风格约束**。Taste-Skill 填补了这个空白——它证明了：不需要更强的模型，只需要更好的约束。

---

## 六、安装与使用

```bash
# 一键安装所有 skills
npx skills add https://github.com/Leonxlnx/taste-skill

# 安装单个 skill（推荐默认的 taste-skill v2）
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"

# 如果依赖 v1 的精确行为
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend-v1"
```

支持的 Agent：Cursor、Claude Code、Codex、Gemini CLI、v0、Lovable

---

## 参考文献

- Taste-Skill README.md: https://github.com/Leonxlnx/taste-skill/blob/main/README.md
- tasteskill.dev: https://tasteskill.dev
- SKILL.md (v2): https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md