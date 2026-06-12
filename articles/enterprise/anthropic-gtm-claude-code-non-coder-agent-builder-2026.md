# Anthropic GTM Claude Code 实践：非工程师 Agent 构建 2026

> 2026 年 6 月 5 日，Anthropic Claude 博客发表了 Jared Sires 的内部案例：**一个从未写过代码的销售 AE，靠 Claude Code 在 Gmail 里构建了 4,300 行的 CLAFTS，并最终成为 GTM 团队的产品经理**。本文解读这篇文章背后的工程组织含义——当 Agent 写代码的成本降到「GPU 秒」时，**「非工程师能否成为产品构建者」的边界条件是什么？**

---

## 核心命题

Claude Code 团队披露的内部数据揭示了一个被低估的趋势：**Agentic Coding 的下一个边界不是"写代码"本身，而是"用产品思维设计 Agent 工具"**。Jared 从销售 AE 转型为 GTM 团队 PM，**不是因为他会写代码了，而是因为他能在产品层面定义「这个工具应该解决什么问题」，并通过 Claude Code 把解决方案落地为可分发的 Cowork 插件**。本文拆解这一案例的 4 层意义：

1. **工具的二次商品化**：当 Claude Code 把"写代码"标准化后，**编写代码的工程师角色让位于"设计 Agent 工作流"的产品角色**——这是技能结构的根本重排
2. **「写代码的恐惧」是真实障碍**：Jared 自述"Claude Code 这个名字里的 'code' 让我一开始感到 intimidation"。**这个心理障碍是 Agentic Coding 普及的最大未解决摩擦**
3. **Cowork 插件 = Agent 工具分发机制**：80% 销售团队在几个月内采用了 Jared 的 Sales 插件——**Agent 工具的 viral 传播机制**比传统 SaaS 更快
4. **跨 Agent 互操作的隐性标准**：daily brief、daily recap、customer-context 等工具**通过 MCP servers（Google Calendar、CRM、Salesforce、Intercom）连接数据源**——**Agent 工具的"乐高化"靠 MCP**

> "Claude Code, having the terminology 'code' at the end of it, made me feel a little bit intimidated just to even start. But after a certain time frame, I understood the power of it being able to hook up to my computer and answer things about files on it."
> — [Claude Blog: How one Anthropic seller rebuilt his team's workflows with Claude Code](https://claude.com/blog/how-anthropic-uses-claude-gtm-engineering) (Jun 5, 2026)

**笔者认为**：大多数关于"AI Coding"的讨论聚焦在"Agent 写代码的能力"（SWE-bench 分数、HumanEval 准确率），但**真正决定一个组织能否用好 Agent 的，是"谁有权力、有能力设计 Agent 工具"**。Jared 的故事给了我们一个判断：**当 Agent 写代码成本降为接近零时，"产品定义权"会从工程师团队向"最懂业务痛点的人"迁移**——而这些人在传统组织里往往是销售、运营、支持岗，**他们不可能，也不应该需要先学会写代码**。

---

## 一、起点：一个销售 AE 的真实痛点

### 1.1 700 个账户 + 10-15 个客户电话 = 工时崩溃

Jared Sires 在 2024 年加入 Anthropic 之前，从未写过一行代码。他是一个 startup AE（Account Executive），管着 600-700 个客户，每天 10-15 个客户电话。**最让他崩溃的不是销售本身，而是行政任务**：

> "It was almost impossible to manage my inbox. And doing outbound on top of that, you don't really know where to focus."

**笔者认为**：这个场景在大多数 B2B 销售团队里都很普遍，但传统的解决方案是**招更多 SDR、买更贵的 Outreach/Salesloft 工具、加更多管理层**。Jared 的解法直接颠覆了这条路径——**让 Agent 接管"回复邮件 + 排优先级"这两个最费时的子任务**。

### 1.2 信息的碎片化是隐性成本

更深的痛点是**信息检索**：Anthropic 每 24-48 小时发版一次，客户的问题永远指向最新细节（batch API SLA、prompt caching 折扣、模型价格、SDK 行为）。要回答好，意味着**每天在 Slack、Google Docs、内部知识库、开发者文档里重新搜索一遍**。

> "Having to relay technical documentation to customers is pretty hard, especially here at Anthropic when your products evolve so quickly."

**笔者认为**：这种"信息保鲜成本"是 B2B SaaS 销售团队里**最被低估的隐性支出**。传统工具只解决了"找文档"（Confluence、Notion）但没解决"把文档和客户上下文融合并生成回复"。**Agent 的真正价值不是"找文档"，而是"基于文档 + 客户上下文 + 你的写作风格，生成可直接发送的草稿"**——这是 LLM 才能做的"语境合成"。

---

## 二、CLAFTS：4,300 行代码的非工程师作品

### 2.1 起点：一个 4,300 行的 Gmail 插件

Jared 决定用 Claude Code 写 CLAFTS（Claude Drafts）时，**他面对的最大障碍不是技术，而是「写代码的恐惧」**：

> "Claude Code, having the terminology 'code' at the end of it, made me feel a little bit intimidated just to even start."

**笔者认为**：这个坦白非常重要。**"Code"这个词本身就是心理门槛**——很多非工程师听到"编程工具"会下意识地认为"这不是给我的"。**Anthropic 的产品命名（"Claude Code" vs "Claude Cowork"）反映了一个未解决的张力**：编程工具和 Agent 工具在底层是同一类技术，但**营销语言决定了渗透路径**。

### 2.2 CLAFTS 的工程结构（外行视角）

CLAFTS 是一个 Gmail 内的应用，约 4,300 行代码，**几乎全部由 Claude Code 生成**。它的关键设计：

1. **从共享 Google Drive 文件夹拉取上下文**——团队的"知识库"是文件，不是数据库
2. **通过 web search 引用 Anthropic 公开文档**——保证回复反映最新产品变更
3. **匹配 Jared 的写作风格**——通过数百次 system prompt 迭代，让 Claude 模仿他的语气

> "Claude is able to use web search to understand our latest documentation from our website and reference that material when generating emails. I don't need to keep all of that in my head."

**笔者认为**：这三点是**Agent 工具设计的通用模式**：
- **文件系统作为记忆**（不是数据库）
- **Web search 作为动态知识**（不是静态索引）
- **Style transfer 作为个性化**（不是 prompt engineering）

这与 R354 的 Anthropic Managed Agents Memory 论文（filesystem as memory）和 R322 的 vault design 是**同一种设计哲学在不同层面的体现**——**让非结构化数据（文件、网页、风格）成为 Agent 的"记忆底座"**。

### 2.3 「CLAFTS Tones」：通过愤怒邮件测试语气

最有趣的是 CLAFTS 的 Tones 功能——通过 pattern matching 模拟 Jared 在不同关系中的语气（客户、同事、家人的邮件读起来都不一样）。Jared 用一个非常规的方法测试：

> "I tested the feature by writing myself a sequence of increasingly angry emails on my personal account. Claude picked up the tone, then refused to keep going."

**笔者认为**：这个测试方法暴露了一个**Agent 安全设计的盲点**——**当 Agent 的"语气适配"扩展到个人邮件时，它可能产生用户不期望的内容**。Anthropic 在 Claude 拒绝继续生成这个细节上做对了，**这说明 Agent 工具的产品化必须有"边界守护"层**——**比传统的 SaaS 更复杂，因为 Agent 工具的输入是开放域的文本**。

---

## 三、从个人工具到组织级插件：Cowork 的分发机制

### 3.1 24 小时 viral 传播

CLAFTS 完成后，Jared 在 Slack 分享了它。**24 小时内，团队里其他销售开始使用并得到类似效果**。这让 Jared 的角色发生了根本性变化——他成为 GTM 团队的产品经理，**专门负责识别销售组织里的痛点，并用 Claude 构建解决方案**。

> "You couple those together and you get Claude managing your daily tasks, which essentially becomes an agent."

**笔者认为**：这里的"viral 传播"和传统 SaaS 的"病毒式增长"在机制上类似，但**Agent 工具的 viral 有一个根本优势**：**它直接嵌入用户的工作流（Gmail、Calendar、CRM）**，不需要切换工具。**这意味着"使用摩擦"接近于零**——用户不需要打开一个新应用，只需要"安装一个插件"。

### 3.2 80% 销售团队在几个月内采用

Jared 把 CLAFTS、daily brief、daily recap、customer-context 等 20+ 工具打包成 **Claude Cowork 的 Sales 插件**。几个月内，**80% 的 Anthropic 销售团队采用了这个插件**。剩下的 20% 主要是新员工，**他们的采用挑战反而是"如何更快 ramp"**——Jared 提到这正是插件下一个要解决的场景。

> "Before the plugin, every new hire used to spend weeks figuring out their own workflow. Now a new hire can install it on day one and have 20-plus skills already wired into the tools they use: Salesforce, Intercom, Gong, Google Calendar, Gmail, Google Drive, and BigQuery."

**笔者认为**：这个数字（80% 在几个月内）**比大多数 B2B SaaS 的渗透速度都快**。原因有三：
1. **嵌入现有工作流**（不需要切换工具）
2. **由同事而非供应商推广**（Jared 是内部成员）
3. **直接解决已有痛点**（不是新需求，是已有痛点的更好解法）

**这暗示了一个产品策略的范式转移**：**未来的企业工具不需要"获客"——它需要"识别已有痛点"和"提供 Agent 化的更好解法"**。

### 3.3 MCP 作为跨 Agent 互操作标准

Jared 的工具集通过 **MCP（Model Context Protocol）servers** 连接 Google Calendar、CRM 数据、Salesforce、Intercom、Gong 等。**这意味着"设计 Agent 工具"的核心工作变成了"选择和配置 MCP servers"**——这比传统 SaaS 的"集成 API"简单得多。

**笔者认为**：MCP 在这个案例中扮演的角色是**"Agent 时代的 USB 标准"**——它把"接入数据源"从"写 API wrapper"简化为"配置 MCP server"。**这是为什么"非工程师能成为产品构建者"的工程基础**。没有 MCP，CLAFTS 还需要一个工程师来写 Gmail API、Calendar API、Salesforce API 的胶水代码。**有了 MCP，Jared 可以把"设计 Agent 行为"作为自己的核心工作**。

---

## 四、「技术屏障溶解」的产品组织含义

### 4.1 角色模糊化：从 AE 到 GTM Architect

Jared 现在的头衔是 **GTM Architect**——他参与产品工程师的设计对话，帮助塑造销售团队的新工具。

> "I feel like with the technical barrier dissolving, I'm almost able to design more products and have senior engineers help me implement to the final stretch. I'm able to augment and do more things."

**笔者认为**：这里的关键概念是 **"技术屏障溶解"**——**当 Agent 写代码成本降为接近零时，"谁能设计产品"的边界条件从"会写代码"变为"懂业务 + 懂 Agent 能力"**。Jared 的转型不是"学写代码"，而是**"用产品语言和工程师对话"**。**这意味着未来 GTM 团队的产品经理需要懂 Agent 能力边界，就像传统 PM 需要懂 SQL 一样**。

### 4.2 「找一个问题」的建议

对于想复制 Jared 路径的销售，Jared 的建议是**先找一个小任务**：

> "Open Claude Code, find one task that's slowing them down, and ask Claude how to build a solution for it."

**笔者认为**：这个建议看似简单，但**它暗示了一个反直觉的方法论**——**不要从"我要用 AI"开始，要从"我每天最讨厌做的 30 分钟任务"开始**。Jared 自己的起点是"每天 2-3 小时回复邮件"，这是一个**任何销售都能识别的、可度量的、影响明显的痛点**。**这是 Agent 工具 PM 的核心方法论**：**痛点优先于技术**。

---

## 五、对工程组织的三点启示

### 5.1 「写代码」不再是核心瓶颈，但「设计 Agent 工具」是

Claude Code 团队的 Cat Wu 在 6 月 3 日的文章 [Running an AI-native engineering org](https://claude.com/blog/running-an-ai-native-engineering-org) 中已经指出："**Bottlenecks didn't go away when agentic coding took away the actual need to type code. Verification, code review, and security took their place.**"

**Jared 的案例补充了 Cat Wu 的论点**：**当 Agent 写代码成本降为零时，瓶颈迁移到了"设计 Agent 工具"——而这个工作传统上不在工程师的角色范围内**。**未来的工程组织需要一种新角色**："Agent PM" 或 "GTM Architect"——他们**不是工程师，但他们是 Agent 工具的真正设计者**。

### 5.2 命名和营销是 Agent 工具的隐性摩擦

> "Claude Code, having the terminology 'code' at the end of it, made me feel a little bit intimidated just to even start."

**笔者认为**：这是产品策略的一个重要提醒——**"Code"这个词会吓退非工程师用户**。Claude Cowork 的命名（去掉"code"）可能正是为了解决这个问题。**未来的 Agent 工具命名应该以"使用场景"为中心**（如 "Claude Drafts"、"Customer Context"），**而不是以"底层技术"为中心**（如 "Code"、"API"、"SDK"）。

### 5.3 MCP 是 Agent 时代的"USB 标准"

Jared 的工具集通过 MCP 连接 6+ 个数据源（Salesforce、Intercom、Gong、Google Calendar、Gmail、Google Drive、BigQuery）。**这意味着"为非工程师提供 Agent 工具"的工程基础是"标准化的数据接入层"**。没有 MCP，每个工具都需要写自己的 API wrapper；有了 MCP，**Jared 可以专注于"设计工具的行为"而不是"写数据接入代码"**。

**这进一步验证了 R337 (Anthropic Scheduled Deployments) 和 R354 (Anthropic Managed Agents Memory) 的论点**：**Anthropic 的核心战略是建立 Agent 基础设施的标准层**（MCP、Filesystem Memory、Cowork 插件、Scheduled Deployments），**让 Agent 工具的开发从"每个团队重造轮子"变为"在标准层之上组合"**。

---

## 六、开放问题：哪些边界条件决定了这条路径可复制？

Jared 的案例是 Anthropic 内部的成功故事。但**它在多大程度上可复制到其他组织**？以下三个边界条件决定了复制难度：

1. **是否有"懂业务 + 懂 Agent 能力"的 PM**：Jared 的成功不是"任何销售都能做到"，而是"一个愿意深入学习 Agent 边界的销售能做到"。**这意味着组织需要培养一种新角色**——**不是工程师，但懂 Agent 能力**
2. **是否有标准化的数据接入层（MCP 或等效）**：如果组织的数据源没有 MCP server，**Jared 的方法就需要先有一个工程师团队写 API wrapper**。MCP（或同类标准）是"非工程师能构建 Agent 工具"的工程前提
3. **是否有内部的 viral 传播机制**：CLAFTS 的 24 小时 viral 来自 Slack 分享。**如果组织的沟通是邮件+会议为主，viral 速度会慢得多**。**Cowork 插件的设计本质上假设了一个"低摩擦分享"的工作环境**

**笔者认为**：这三个条件中，**第 2 个（数据接入层）是工程组织能直接投资的**——**部署 MCP servers 是未来 12 个月企业 IT 的重要任务**。R354 的 filesystem memory、R337 的 scheduled deployments、R331 的 vault 设计、R322 的 Brain/Hand/State 解耦——**所有这些 Anthropic 公开的工程论文都在为"非工程师 Agent 工具"构建基础**。

---

## 七、给读者的判断

**Jared 的故事给我们的核心启示是**：

> **"Agentic Coding" 的真正影响不是"工程师生产力提升 N 倍"——而是"产品定义权的下放"**。当写代码的成本降为接近零时，**「谁有权力、有能力设计 Agent 工具」这个问题比「谁的代码写得更好」更关键**。

对于工程组织，这意味着：
- **重新定义 PM 角色**——未来的 PM 需要懂 Agent 能力边界，就像今天需要懂 SQL
- **投资 MCP 标准化**——这是非工程师 Agent 工具的工程前提
- **重新设计内部工具分享机制**——Cowork 插件式的"低摩擦分发"是未来企业内部工具的主流

对于想转型为 GTM Architect 的销售/运营/支持从业者，这意味着：
- **不需要先学会写代码**——但需要学会"用产品语言描述 Agent 行为"
- **从最讨厌的 30 分钟任务开始**——不要从"我要用 AI"开始，要从痛点开始
- **Cowork 插件是验证工具的最佳方式**——先在 Slack 分享个人版，viral 验证后再打包插件

---

## 来源

- [How one Anthropic seller rebuilt his team's workflows with Claude Code](https://claude.com/blog/how-anthropic-uses-claude-gtm-engineering) — Anthropic Claude Blog, June 5, 2026
- [Running an AI-native engineering org](https://claude.com/blog/running-an-ai-native-engineering-org) — Cat Wu, Claude Blog, June 3, 2026
- [The Claude Cowork product guide](https://claude.com/blog/the-claude-cowork-product-guide) — Anthropic Claude Blog

## 配套项目

- [Planning-with-Files: SKILL.md 跨代理标准](../projects/othmanadi-planning-with-files-skill-md-23105-stars-2026.md) — 23K⭐ MIT，与本文主题强闭环
