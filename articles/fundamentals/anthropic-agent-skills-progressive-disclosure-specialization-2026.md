# Agent Skills：渐进式披露与专业化模式如何重塑 Agent 能力边界

Agent 在处理专业领域任务时，一个根本矛盾始终存在：通用模型能力强大，但缺乏领域特定的**程序性知识**（procedural knowledge）和**组织上下文**（organizational context）。当模型需要掌握 PDF 表单填写、代码审查流程或特定业务工作流时，传统的做法是为每个场景单独构建定制 Agent——这导致了碎片化的架构和难以扩展的维护成本。

Anthropic 在 2025 年 10 月发布的 **Agent Skills** 引入了一种基于文件夹的技能组合模式，其核心创新是**渐进式披露**（Progressive Disclosure）：通过 SKILL.md 文件加 YAML frontmatter 的结构，让 Claude 在启动时预加载技能的名称和描述，仅在判断任务相关时才触发完整加载。这一设计从根本上解决了上下文窗口容量与专业化深度之间的 tradeoff。

笔者认为，理解 Skills 的设计原理，对于构建生产级 Agent 系统的工程师而言，是一个必须掌握的基础框架。

---

## 技能的解剖结构：三层渐进式披露

从技术实现角度，Agent Skill 本质上是一个目录，包含一个必需的 `SKILL.md` 文件。Anthropic 明确要求该文件必须以 **YAML frontmatter** 开头，包含 `name` 和 `description` 两个必填字段。

这三个层次的渐进式披露机制如下：

**第一层（Level 1）**：在 Agent 启动时，系统将所有已安装技能的 `name` 和 `description` 预加载到 system prompt 中。Claude 凭借这些元数据判断当前任务是否需要触发某个技能——此时 Claude 尚未读取技能的完整内容，仅持有"目录索引"。

**第二层（Level 2）**：当 Claude 判断某技能与当前任务相关后，它主动通过 Bash 工具读取对应 `SKILL.md` 的完整内容，将其加载到当前 context window 中。这是技能的实际使用阶段。

**第三层（Level 3）**：随着技能复杂度增长，单个 SKILL.md 可能包含过多上下文，或某些内容仅在特定场景下才需要。Skill 允许在目录内打包额外的文件（如 `reference.md`、`forms.md`），并通过名称引用它们。Claude 仅在需要时才导航至这些文件——Anthropic 将这形象地描述为：

> "Agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window when working on a particular task. This means that the amount of context that can be bundled into a skill is effectively unbounded."

这意味着技能的上下文容量实际上是**无上限的**——关键在于如何分层组织。

以 PDF 技能为例，核心 SKILL.md 仅描述 PDF 处理的基本流程，而将表单填写相关的指令拆分为独立的 `forms.md`。Claude 在处理一般 PDF 阅读时无需加载表单指令，仅在检测到用户需要填写表单时才读取 `forms.md`。这种按需加载的机制确保了每次触发技能时的 token 消耗最小化。

---

## Skills 与 MCP：工具 vs. 工作流的分工

这里需要澄清一个常见的误解：Skills 和 Model Context Protocol（MCP）是互补关系，而非替代关系。

MCP 为 Agent 提供**工具调用能力**（tool calling capabilities）——通过标准化的接口连接外部系统（数据库、API、文件系统等）。MCP 的核心是"能做什么"的问题。

而 Skills 提供的是**程序性知识和工作流**（procedural knowledge and workflows）——如何正确地、按照特定领域的最佳实践完成一项任务。Skills 的核心是"怎么做"的问题。

Anthropic 在官方文章中明确指出：

> "Building a skill for an agent is like putting together an onboarding guide for a new hire."

这个类比非常精准：新员工入职时需要的不仅是工具手册（对应 MCP 的工具定义），更需要 SOP 和经验沉淀（对应 Skills 的程序性知识）。

此外，Skills 还可以打包**代码脚本**作为确定性工具（deterministic tools）供 Agent 调用。Anthropic 在 PDF 技能示例中包含了一个预写的 Python 脚本，用于读取 PDF 并提取所有表单字段。Claude 可以直接执行这个脚本，而无需将脚本内容或 PDF 文件加载到 context 中——这对于需要**确定性**和**高效执行**的操作（如排序算法、文件解析）尤为重要。相比 LLM 生成的结果，代码执行提供了传统软件工程级别的可重复性和性能保证。

---

## 安全考量：第三方技能的信任边界

Skills 通过指令和代码为 Agent 赋予新能力，这既是其强大之处，也是潜在的安全风险所在。Anthropic 对此给出了明确的安全建议：

- **仅从可信来源安装技能**。对于来自非可信来源的技能，在使用前必须进行全面审计。
- 审计时应仔细阅读技能目录中的所有文件，特别关注**代码依赖**和打包的资源（图片、脚本等）。
- 同时注意技能中是否存在连接不可信外部网络来源的指令或代码。

笔者认为，这背后的安全模型逻辑是：Skills 本质上是以 Agent 的身份在执行操作——如果一个恶意的 Skill 指示 Agent 向外部服务器发送敏感数据，或在文件系统中执行破坏性操作，这些行为在 Skill 被加载后就获得了 Agent 的执行权限。因此，Skills 的安全模型必须建立在**最小信任**（least trust）的基础上。

---

## 构建 Skills 的最佳实践

Anthropic 在官方文章中总结了四条实践原则，笔者结合自身理解做进一步展开：

**1. 从评估开始（Start with evaluation）**

识别 Agent 能力缺口的标准方法是：在代表性任务上运行 Agent，观察它们在哪里挣扎或需要额外的上下文。技能的构建应该是增量式的——针对已识别的具体缺口逐步构建，而非一开始就试图构建一个"全能"的技能。

**2. 为扩展而结构化（Structure for scale）**

当 SKILL.md 变得难以维护时，将其拆分为多个文件并通过引用关联。当某些上下文是互斥的或很少同时使用时，保持路径分离可以减少 token 使用。代码既可以作为可执行工具，也可以作为文档——技能作者需要明确指示 Claude 是应该直接运行脚本，还是将其作为参考文档读取到上下文中。

**3. 从 Claude 的视角思考（Think from Claude's perspective）**

技能的 `name` 和 `description` 是 Claude 判断是否触发的依据——这两个字段的质量直接影响技能的可发现性。在真实场景中监控 Claude 如何使用技能时，特别要注意意外的执行轨迹或对某些上下文的过度依赖。

**4. 与 Claude 迭代（Iterate with Claude）**

Anthropic 提出的这一原则颇具洞察力：在与 Claude 一起完成一项任务时，主动要求 Claude 将其成功的方法和常见错误捕获为可重用的上下文和代码。如果 Claude 在使用某个技能时偏离了轨道，要求它进行自我反思。这一过程能够揭示 Claude 实际需要的上下文，而不是我们事先假设的。

---

## 工程落地的启示

笔者认为，Agent Skills 的发布代表着 Agent 开发范式的一个关键转变：从"为每个场景构建专用 Agent"到"构建可组合的技能单元"。这与软件工程中从单体架构向微服务架构的演进有相似之处。

对于工程师而言，Skills 模式的核心启示是：**技能的边界应该按照工作流的自然切分来设计，而不是按照技术实现来设计**。一个 PDF 技能之所以成立，不是因为它用了某种 PDF 库，而是因为"处理 PDF 文档"是 Agent 工作中一个独立、可复用、有明确输入输出的工作单元。

从更长远看，Anthropic 已经明确表示将探索 **Agent 自己创建、编辑和评估 Skills** 的能力。这意味着未来的 Agent 不仅能使用技能，还能**提炼和固化自己的经验**为可重用的技能单元——这是 Agent 自我改进（self-improvement）的一个重要方向。

---

**来源**：Anthropic Engineering Blog, *"Equipping agents for the real world with Agent Skills"*, Published Oct 16, 2025. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
