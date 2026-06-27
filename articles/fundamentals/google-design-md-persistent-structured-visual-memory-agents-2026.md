# Google design.md：为什么 AI Agent 需要"结构化的视觉记忆"

**核心命题**：design.md 的本质不是一份设计系统文档，而是一种**让 Agent 拥有结构化视觉记忆**的机制。它解决了 AI Agent 在 UI 编码任务中"记得住_tokens、记不住决策"的问题——通过将视觉知识组织成机器可解析的规范格式，Agent 获得了跨越会话的视觉理解能力。

---

## 一、现有 AI Agent 视觉理解的瓶颈

当前 AI Coding Agent 处理视觉任务的方式本质上只有两种：

**像素级复制**：让 Agent 看截图/Figma 导图 → 提取颜色值 → 生成代码。这种方式的问题是：Agent 只能获取**显性的像素信息**，无法获取**隐性的设计决策**。

**规则注入**：在 System Prompt 或 CLAUDE.md 中写"按钮用蓝色 #2196F3"。这种方式的问题是：规则之间相互独立，Agent 不知道**规则之间的优先级和约束关系**。

笔者认为，这两种方式都忽视了视觉知识的**结构性特征**。颜色不是孤立存在的——它与字体、间距、组件状态共同构成了一套约束系统。脱离结构的视觉规则，Agent 只能机械地应用，无法处理边界情况。

---

## 二、design.md 的解法：结构化视觉记忆

Google Labs 的 design.md 提出了一种新思路：**将视觉知识组织成机器可解析的规范格式，让 Agent 能够"理解"设计系统，而非仅仅"读取"设计值**。

### 2.1 三层视觉知识表示

design.md 将视觉知识分解为三层：

**第一层：值（Values）—— YAML Front Matter 中的 Tokens**

```yaml
colors:
  primary: "#1A1C1E"
  tertiary: "#B8422E"
typography:
  h1:
    fontFamily: "Public Sans"
    fontSize: 3rem
```

这是最基础的层，提供精确值。Agent 可以直接引用 `{colors.primary}`，保证所有地方一致。

**第二层：关系（Relationships）—— Token 引用**

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.neutral}"
```

`{colors.tertiary}` 是对第一层值的引用。这不是简单的字符串替换，而是**语义关系**的编码——Agent 知道 `button-primary` 的背景色和 `tertiary` 是同一个语义概念，未来如果 `tertiary` 的值变了，引用它的组件会自动保持一致。

**第三层：意图（Intent）—— Markdown Body**

```markdown
## Colors

The palette is rooted in high-contrast neutrals and a single accent color.

- **Primary (#1A1C1E):** Deep ink for headlines and core text.
- **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction.
```

这层解释**为什么这样选择**，而非仅仅是什么值。对于 Agent，这意味着：当遇到规范中没有明确覆盖的组件时，它可以参考设计意图推断正确的处理方式。

---

## 三、为什么说这是"记忆"而非"文档"

design.md 被收录在 `context-memory/` 目录下（笔者注：应归属此目录），核心原因在于它的功能本质是**为 Agent 提供跨会话的视觉记忆**。

### 3.1 传统记忆 vs 结构化视觉记忆

| 维度 | 传统记忆（RAG/向量数据库）| design.md 结构化视觉记忆 |
|------|----------------------|------------------------|
| 存储形式 | 非结构化文本 | YAML + Markdown 混合格式 |
| 检索方式 | 语义相似度匹配 | Token 路径直接引用 |
| 一致性保证 | 无（每次检索独立）| 有（引用机制自动传播）|
| 跨会话稳定性 | 依赖向量检索质量 | 完全确定性的值解析 |
| 可执行性 | 无 | 有（Token 直接可应用于代码）|

**关键差异**：RAG 类记忆系统在每次检索时都可能产生不同的结果（取决于查询向量和最相似的段落），而 design.md 的 Token 引用是**完全确定性的**——同一份 design.md，在任何时候、任何 Agent 读取，结果都完全一致。

### 3.2 记忆一致性保证

考虑这个场景：设计系统更新了主色调。

**没有 design.md**：
- 人类手动改代码库中所有引用的颜色值
- 人类审查是否有遗漏
- 可能遗漏某处的 hardcoded 值

**有 design.md**：
- 修改 YAML front matter 中 `colors.primary` 的值
- Agent 重新读取 design.md
- 所有引用 `{colors.primary}` 的组件自动应用新值

这不是魔法——这是**引用机制**的力量。design.md 的 Token 引用类似于编程语言中的常量引用，修改常量的值，所有使用该常量的地方自动同步。

---

## 四、结构化视觉记忆与 Agent 记忆系统的互补

笔者认为，当前 Agent 记忆系统的研究（如 Mem0、mempalace、agentmemory 等）主要集中在**文本上下文**的记忆管理。但视觉设计系统是一个独立的知识领域，有其独特的结构——颜色系统、字体系统、间距系统、组件系统——**这些结构不能被简单地压缩成文本片段**。

design.md 的贡献在于：它证明了**特定领域的知识应该用领域适配的结构来编码**，而非全部塞进通用的文本记忆系统。

### 视觉记忆的独特性

| 特征 | 文本记忆 | 视觉设计记忆 |
|------|---------|------------|
| 知识的结构依赖性 | 低（文本片段相对独立）| 高（颜色、字体、间距相互约束）|
| 值的一致性要求 | 中（语义一致即可）| 高（像素级精确）|
| 变更传播范围 | 模糊（影响哪些文本不确定）| 清晰（Token 引用链明确）|
| 人类可参与性 | 易（直接读写文本）| 中（需要理解 Token 结构）|

**这意味着**：视觉记忆系统不能简单复用通用文本 RAG 的架构，而需要针对视觉知识的结构特征专门设计。design.md 是这个方向的早期探索。

---

## 五、与 CLAUDE.md 的关系：两种记忆的协同

在 Agent Engineering 的语境下，CLAUDE.md 和 design.md 分别处理两类不同的记忆：

| 文件 | 记忆类型 | 解决的问题 |
|------|---------|---------|
| **CLAUDE.md** | 工程上下文记忆 | "这个项目用什么构建、怎么组织、遵循什么工程规范" |
| **design.md** | 视觉上下文记忆 | "这个产品的视觉系统用什么值、为什么这样选择" |

两者组合，构成了 AI Coding Agent 的**完整上下文层**：

```
Agent 记忆系统
├── 工程上下文（CLAUDE.md）
│   ├── 技术栈定义
│   ├── 代码组织规范
│   └── 工具使用规则
└── 视觉上下文（design.md）
    ├── 颜色系统
    ├── 字体系统
    ├── 间距系统
    └── 组件规范
```

这种分离的设计是合理的：工程规范和视觉规范在本质上是不同类型的知识，用不同的结构来编码、组织、更新，是工程上的正确选择。

---

## 六、局限性与适用边界

design.md 不是银笔。它的适用性有以下边界：

**设计系统必须足够成熟**：design.md 假设设计系统已经有清晰的 Token 定义。如果设计系统本身在快速迭代中，Token 的频繁变更会抵消引用机制的价值。

**适合有设计系统的产品**：没有统一设计系统的个人项目，直接写代码可能比维护 design.md 更高效。

**Component Token 的表达能力有限**：当前 design.md 的 Component Token 只支持预定义的 7 个属性（backgroundColor、textColor 等），对于高度自定义的组件，表达能力受限。

**与其他视觉工具的同步**：design.md 是源格式，但设计工具（Figma 等）不是天然就支持导出 design.md。当设计系统更新时，需要人工或额外的同步机制来保持一致。

---

## 七、笔者判断：视觉记忆是 Agent Context 工程的下一个前沿

笔者认为，design.md 代表的不是"又一个设计系统工具"，而是**视觉领域 Agent Context 工程的一个新方向**。

当前的 Agent Context 工程主要关注：
- 文本上下文的压缩与管理（RAG、Context Compression）
- 工程规则的编码（CLAUDE.md、System Prompts）
- 工具接口的定义（MCP）

但视觉上下文——颜色、字体、间距、组件——是 AI Coding Agent 的核心工作负载，这部分 Context 工程目前几乎是空白。

design.md 提供了第一个可行的方案。它的价值不在于具体实现了什么，而在于**证明了视觉知识可以被结构化为 Agent 可解析、可引用、可一致性应用的格式**。

未来可能会有更多的领域特定记忆格式出现：动画规范（animation.md？）、数据可视化规范（chart.md？）、音频规范（sound.md？）——每个领域都有其独特的知识结构，通用文本记忆无法高效处理这些结构。

**视觉记忆的工程化，是 AI Agent 从"能用"到"用好"的关键一步。**

---

## 附录：核心引用

> "A DESIGN.md file combines machine-readable design tokens (YAML front matter) with human-readable design rationale (markdown prose). Tokens give agents exact values. Prose tells them why those values exist and how to apply them." — *Google Labs, design.md README*

> "The tokens are the normative values. The prose provides context for how to apply them." — *Google Labs, design.md README*

> "For an agent that reads this file will produce a UI with deep ink headlines in Public Sans, a warm limestone background, and Boston Clay call-to-action buttons." — *Google Labs, design.md README*

---

## 参考数据

| 指标 | 数值 |
|------|------|
| Stars | **22,095**（截至 2026-06-27）|
| License | Apache 2.0 |
| 创建时间 | 2026-04-10 |
| 最新更新 | 2026-06-15 |
| 定位 | Google Labs 实验性项目 |

---

*来源：[github.com/google-labs-code/design.md](https://github.com/google-labs-code/design.md)，Google Labs，2026年4月*
