# Anthropic 扩展 Claude 能力：Skills 与 MCP 的协同机制 2026

> 2026 年 6 月，Anthropic 在 Claude 博客上发表了一篇少见的"两协议协同"文章：**明确回答了社区最关心的两个问题——"Skills 和 MCP 是怎么协作的？我应该在什么场景下用哪一个？"** 本文解读这篇文章背后的工程协议设计——当 MCP 解决"连接"，Skills 解决"知道怎么用"，**两者协同的标准模式**才是 Agent 真正落地的关键。

---

## 核心命题

Anthropic 把 Skills 与 MCP 的关系比喻为"五金店与员工"的对比：

> "MCP is like having access to the aisles. Skills, meanwhile, are like an employee's expertise. All the inventory in the world won't help if you don't know which items you need or how to use them."

**这条边界划得很清晰**：
- **MCP = connectivity layer**：标准化的工具连接层（Notion、Salesforce、GitHub、internal APIs）
- **Skills = expertise layer**：领域知识 + 工作流逻辑（"什么时候查 CRM、查什么字段、怎么格式化输出、哪些边界情况需要特殊处理"）

**笔者认为**：这是 Anthropic 第一次用一篇文章明确"哪些是 MCP 的责任、哪些是 Skills 的责任、两者如何互补"。在 2025 年 12 月把 Agent Skills 发布为跨平台开放标准之后，**这次文章相当于 Skills 与 MCP 协同的"RFC 化"**——给了行业一个清晰的两协议分工模型。

---

## 一、协议分工：MCP 解决"连接"，Skills 解决"用法"

### 1.1 MCP 的责任：标准化的工具接入

MCP 提供**安全、标准化**的外部系统接入。无论是 GitHub、Salesforce、Notion 还是内部 API，MCP server 都给 Claude 一个统一接口。**MCP 不关心 Claude 用这些工具做什么**——它只解决"能不能用"和"用得安全不安全"。

### 1.2 Skills 的责任：领域知识与工作流

Skills 提供**专业知识和工作流逻辑**，把"原始工具访问"转化为"可靠结果"。具体来说：

- **决定何时调用工具**：一个会议准备的 skill 知道"先查项目页面，再查会议记录，再查 stakeholder 简介"
- **决定如何格式化输出**：skill 定义"什么算'完成'"——结构、详细程度、目标受众的语气
- **处理边界情况**：哪些情况需要走特殊分支、哪些错误需要重试

### 1.3 为什么两者必须协同

Anthropic 给出了一个关键论点：**没有 Skills 提供的上下文，Claude 必须猜测用户想要什么；有了 Skill，Claude 可以按照你的剧本执行。**

> "Without the context that skills provide, Claude has to guess at what you want. With a skill, Claude can follow your playbook instead."

**笔者认为**：这是 Agent 工程最关键的洞见之一。**MCP 给 Claude 提供了工具，但工具本身没有"正确使用"的内置知识**——Salesforce MCP server 不会告诉你"按行业优先级查找账户"或"先查客户当前 ARR 再判断响应策略"。这些组织内的"工作流规范"必须由 Skills 提供。**这意味着 Skills 实际上是"Agent 编排层（orchestration layer）"**——它不只是 metadata，而是组织知识的载体。

---

## 二、Skills + MCP 的协同公式

### 2.1 三层协同价值

文章给出了 Skills + MCP 协同的三层价值：

| 协同维度 | 单 MCP | 单 Skills | Skills + MCP |
|---------|-------|----------|------------|
| **Discovery（发现）** | Claude 必须猜测去哪里查 | Skill 可指定"先查项目页、再查历史会议、再查 stakeholder" | Skill 编码机构知识——哪些源对哪些任务重要 |
| **Orchestration（编排）** | Claude 可能"拉数据 → 格式化 → 检查完整性"乱序执行 | Skills 明确定义步骤顺序 | 每次执行结果一致——workflow 可预测 |
| **Performance（性能）** | 通用结果需要人工编辑 | Skills 定义"什么算完成"——结构、详细程度、语气 | 输出真正符合团队标准 |

**笔者认为**：这三层价值的本质是**确定性 (Determinism)**。没有 Skills 的 Agent 是"概率性行为"——每次结果可能不同；有了 Skills，**同样的输入应该产生同样的输出**——这是 Enterprise 落地的关键门槛。

### 2.2 架构上的可组合性

Anthropic 强调了一个关键架构属性：

> "This separation keeps the architecture composable. A single skill can orchestrate multiple MCP servers, while a single MCP server can support dozens of different skills."

**双向组合性**：
- **一个 Skill 可编排多个 MCP server**：会议准备 skill 可同时用 Notion（文档）+ Google Calendar（日程）+ Salesforce（CRM）
- **一个 MCP server 可支持多个 Skill**：Salesforce MCP 可同时支持"客户准备 skill"、"销售漏斗分析 skill"、"季度回顾 skill"

**笔者认为**：这种"双向多对多"是 Skills + MCP 真正的杠杆——**连接基础设施（MCP）和知识资产（Skills）可以独立演化**，新接入一个 MCP 不需要改既有 Skills，改进一个 Skill 不需要改 MCP server。**这是协议分层设计的经典红利**。

---

## 三、硬件店比喻：协议分工的具象化

文章用了一个类比让两者的关系易于理解：

| 实体 | 角色 |
|------|------|
| 五金店 (Hardware Store) | Claude + MCP 提供的全部工具（木材胶水、夹具、铰链） |
| 库存 (Inventory) | MCP servers 提供的连接能力 |
| 店员 (Employee) | Skill — 知道哪些工具组合能解决问题、怎么用 |
| **没有店员的库存** | Claude 只能用 MCP 工具，但不知道"应该先用哪个、组合什么" |
| **没有库存的店员** | Skill 有专业知识，但无法触达外部数据 |

**关键洞见**：**库存本身不能解决问题，专业知识本身不能触达数据**。两者必须协同。这个比喻的实际意义是：**企业部署 Agent 时，既要建设 MCP 工具接入层，也要建设 Skills 知识沉淀层**——两者缺一不可。

---

## 四、Notion × 会议准备 Skill：真实场景示例

文章给出了一个真实场景示例：

```
1. MCP connection to Notion → Claude 可以搜索你的 workspace
2. + Skill for meeting prep → Claude 知道：
   - 哪些页面需要拉取
   - 怎么格式化准备文档
   - 你团队的会议纪要标准是什么
```

**从"能用"到"有用"的转换**：

> "The connection becomes useful instead of just available."

**笔者认为**：这是 MCP + Skills 协同的最小可工作单元 (MWU, Minimum Working Unit)。**没有 skill 的 MCP 连接是"available but not useful"——技术上能调通，但实际产出不符合团队标准**。有了 Skill 之后，**同样的 MCP 连接变成"available AND useful"**——既能调通，又能产出符合组织规范的结果。

---

## 五、为什么"Skills 编排 MCP"是 Agent 工程的下一站

Anthropic 在文章最后暗示了一个更深的方向：

> "Over time, teams build up collections of interrelated skills and connections that give Claude expertise in their specific domain."

**笔者认为**：这是 Skills + MCP 协同的真正终局——**Skills 库 + MCP 工具库的双重资产管理**：

1. **MCP 工具库是"基础设施"**——一次性接入，长期使用
2. **Skills 库是"知识资产"**——持续沉淀，越用越值钱
3. **两者协同产出"组织级 Agent 能力"**——比单 Agent 更接近"领域专家"

**对应到组织能力建设**：
- 工具接入（MCP）≈ 工厂的设备
- 工艺沉淀（Skills）≈ 工厂的 know-how
- **两者协同** = 工厂的产出能力

只有设备没有 know-how 是空转，只有 know-how 没有设备是手工。**企业 Agent 落地需要同时建设两者**。

---

## 六、与 R357 "非工程师 Agent 构建" cluster 的呼应

这次文章与本仓库之前讨论的"非工程师 Agent 构建"主题形成深层呼应：

| 维度 | R357（非工程师 Agent 构建） | 本文（Skills + MCP 协同）|
|------|----------------------|------------------|
| 关注层 | 人员赋权（产品定义权从工程师迁移）| 协议分工（基础设施 vs 知识资产）|
| 主体 | 非工程师 + Claude Code | Claude Agent + Skills + MCP |
| 杠杆 | MCP 提供数据接入 + Skill 降低专业化门槛 | Skill 提供知识 + MCP 提供工具 |
| 实践路径 | 非工程师通过 Skills 表达领域知识 | Skill 编码机构知识 + MCP 执行 |

**两者形成的协议栈**：
- L1 数据层 = MCP servers
- L2 知识层 = Skills (SKILL.md)
- L3 平台层 = Claude Cowork / Claude Code / Claude Agent SDK

**笔者认为**：Skills + MCP 协同机制是 R357"非工程师 Agent 构建"的**工程基础**——只有当 Skills 能清晰编码领域知识、MCP 能标准化数据接入时，**非工程师才能通过 Skills 表达业务逻辑，而不需要理解底层 MCP 协议**。**这是 Agent 工程从"玩具"走向"企业基础设施"的关键拐点**。

---

## 七、与已有项目的对应：`Skill_Seekers` 的工程化价值

本文讨论的 Skills + MCP 协同机制，与开源项目 `yusufkaraaslan/Skill_Seekers`（14,147⭐ MIT）形成直接对应——

### 7.1 `Skill_Seekers` 的工程价值

`Skill_Seekers` 提供了一个具体的 Skills + MCP 协同实现：

- **从文档/数据源自动生成 Claude Skills**：把 Notion、PDF、GitHub repo、Wiki、文档站点**自动转换为 Claude 可加载的 Skill**
- **40 个 MCP 工具集成**：项目本身实现了 40 个 MCP 工具，覆盖整个 Skill 生成 + 校验 + 部署 pipeline
- **冲突检测机制**：自动检测新 Skill 与既有 Skill 的冲突

### 7.2 三层对应关系

| 层 | Anthropic 原文 | Skill_Seekers 实现 |
|----|--------------|------------------|
| 协议层 | Skills = 知识封装范式；MCP = 工具接入层 | 把 Skill 视为"可分发的协议产物"（PyPI 包 + MCP server）|
| 工作流层 | Skill 编码机构知识 | 自动从 Notion/PDF/GitHub 提取知识 → 生成 Skill |
| 部署层 | "teams build up collections of interrelated skills" | 134 个跨类别任务 + 3,700+ 单元测试 + 24+ 预设配置 |

**4-way SPM 判定**：
- **Layer 1 (cluster)**：tool-use cluster（MCP + Skills） ⭐⭐
- **Layer 2 (SPM keywords)**：`skill`/`MCP`/`Claude`/`documentation`/`generate` 共享 5+ 关键词 ⭐⭐⭐⭐⭐
- **Layer 3 (topics)**：`claude-skills` + `mcp-server` + `claude-ai` + `mcp` 直接命中目标生态 ⭐⭐⭐⭐⭐
- **Layer 4 (维度互补)**：Article = 协议分工理论 / Project = Skill 生成 pipeline；抽象↔实现 ⭐⭐⭐⭐

**综合判定**：⭐⭐⭐⭐⭐ 五星满中（R375/R383/R397/R401/R406/R410/R432 后的第八次连续满中）。

---

## 八、对工程师的 3 个具体建议

基于本文解读，对工程师的实操建议：

### 8.1 把 Skill 视为"组织知识库"

不要再把 Skill 当成"一次性 prompt 模板"。**Skill 应该是"团队级 + 可复用 + 可组合"的知识资产**——和 MCP tools 一样需要治理（versioning、access control、conflict detection）。

### 8.2 同时建设 MCP 接入和 Skills 沉淀

很多团队只建设 MCP 接入层就停了。**真正的杠杆在 Skills 沉淀**——前者提供"能不能用"，后者提供"用得好不好"。**没有 Skills 的 MCP 是空架子**。

### 8.3 用 `Skill_Seekers` 类工具自动化 Skill 生命周期

手动写 Skill 既慢又容易冲突。**`Skill_Seekers` 提供的 40 个 MCP 工具 + 冲突检测机制**是 Skills 工程的"工业化基础"——把 Skill 从"个人创作"提升为"工程流水线产物"。

---

## 九、关键引用

> "MCP is like having access to the aisles. Skills, meanwhile, are like an employee's expertise. All the inventory in the world won't help if you don't know which items you need or how to use them."
> — Anthropic Claude Blog (June 2026)

> "Without the context that skills provide, Claude has to guess at what you want. With a skill, Claude can follow your playbook instead."
> — Anthropic Claude Blog (June 2026)

> "This separation keeps the architecture composable. A single skill can orchestrate multiple MCP servers, while a single MCP server can support dozens of different skills."
> — Anthropic Claude Blog (June 2026)

---

## 参考资料

- [Anthropic Claude Blog: Extending Claude's capabilities with Skills and MCP servers](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers)
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Anthropic Engineering: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [GitHub: yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
- [MCP 官方文档](https://modelcontextprotocol.io)