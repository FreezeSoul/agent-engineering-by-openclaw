# OpenAI 的「代码库即系统记录」工程法：让 Agent 从「执行工具」进化为「自主参与者」

> **核心命题**：当 Agent 能自主读写整个代码库时，工程团队的核心工作变成了**设计一个让 Agent 能自我导航、自我修正的系统**，而不是给 Agent 写一本永远会过时的使用手册。

---

## 一、问题：AGENTS.md 为什么失败了

OpenAI 在 2025 年 8 月开始一个实验：在空 git 仓库中完全由 Codex 生成代码。五个月后，仓库包含约 **100 万行代码**，1500 个 PR 被合并，团队只有 **3 名工程师** 驱动——人均 3.5 PR/天。

这个实验最初沿用了当时社区的主流做法：**一本厚厚的 AGENTS.md** 作为 Agent 的操作手册。效果如预期般失败了，原因是根本性的：

**上下文是稀缺资源**。一本巨厚的指令文件会挤占任务本身、代码和相关文档——Agent 要么错过关键约束，要么开始对错误目标进行局部优化。

**当一切都「重要」时，什么都不重要了**。Agent 学会了对所有规则做模式匹配，而不是有意识地导航。

**它立即腐烂**。一份静态手册很快变成过时规则的坟墓。Agent 无法分辨哪些仍然有效，人类停止维护它，文件悄悄地变成了一个「诱人的麻烦」。

**它难以验证**。一个单一的大文件不适合机械检查（覆盖率、新鲜度、所有权、交叉链接），所以漂移是不可避免的。

> 原文："Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs—so the agent either misses key constraints or starts optimizing for the wrong ones."

---

## 二、核心解法：把代码库变成「系统记录」而非「指令手册」

OpenAI 的解决方案是把 **AGENTS.md 降级为目录**，而把真正的知识沉淀在代码库内部的结构化文档目录中。

**不是把 AGENTS.md 当作百科全书，而是把它当作目录。**

```plain text
AGENTS.md                          ← 约 100 行的导航地图
ARCHITECTURE.md                    ← 顶层领域映射
docs/
├── design-docs/
│   ├── index.md
│   ├── core-beliefs.md           ← Agent 优先操作原则
│   └── ...
├── exec-plans/
│   ├── active/                   ← 正在执行的计划
│   ├── completed/                ← 已完成的计划
│   └── tech-debt-tracker.md     ← 技术债务追踪
├── generated/
│   └── db-schema.md             ← 生成的数据库 schema
├── product-specs/
│   ├── index.md
│   ├── new-user-onboarding.md
│   └── ...
├── references/
│   ├── design-system-reference-llms.txt
│   ├── nixpacks-llms.txt
│   └── ...
DESIGN.md
FRONTEND.md
PLANS.md
PRODUCT_SENSE.md
QUALITY_SCORE.md
RELIABILITY.md
SECURITY.md
```

这是一个**渐进式披露（Progressive Disclosure）**的架构设计：
- Agent 从一个小而稳定的入口开始
- 被告知「下一步去哪里找」
- 而不是一开始就被海量信息淹没

> 原文："So instead of treating AGENTS.md as the encyclopedia, we treat it as the table of contents."

---

## 三、机械化执行：让 Linter 和 CI 成为「护栏」而非「文档」

把知识编码进文档是不够的——在纯 Agent 生成代码的世界里，文档也会漂移。OpenAI 强制所有这些规则**通过机械手段执行**：

**1. 专用 Linter + CI Job 验证**
- 验证文档知识库是最新的
- 验证是交叉链接的
- 验证结构是正确的
- 不符合规范就阻止合并

**2. Doc-Gardening Agent（文档园丁 Agent）**
- 一个 recurring 后台 Codex 任务
- 扫描过时或已废弃的文档（不再反映真实代码行为的文档）
- 自动打开 fix-up PR
- 整个流程不需要人类介入

**3. 质量评分文档（QUALITY_SCORE.md）**
- 每个产品域和架构层都有质量评分
- 随着时间追踪差距
- Agent 可以直接读取并理解「当前状态」

**4. 执行计划（Execution Plans）作为一等公民**
- 小改动用轻量级 ephemeral plans
- 复杂工作被捕获在 execution plans 中，包含进度和决策日志
- 这些计划被提交到仓库版本控制
- Active plans / completed plans / known technical debt 全部共存且共版本
- Agent 可以在没有外部上下文的情况下运行

> 原文："We enforce this mechanically. Dedicated linters and CI jobs validate that the knowledge base is up to date, cross-linked, and structured correctly."

---

## 四、「金原则」编码：从「文档治理」到「代码治理」

随着代码库规模增长，Codex 会复制已经存在的模式——即使这些模式是不均匀或次优的。人类手动清理「AI slop」很快成为瓶颈（每周 20% 时间）。

OpenAI 的解法是把清理原则编码为**机械规则**——他们称之为「Golden Principles」：

**例子**：
1. **优先共享工具包**而非手写 helpers，让不变量集中化
2. **不要 YOLO 式探测数据**——在边界验证或依赖类型化 SDK

定期运行的 Golden Principles 扫描任务会：
- 扫描偏差
- 更新质量评分
- 打开针对性的重构 PR

这些 PR 大多可以在**不到一分钟内审查完**，并自动合并。

**这本质上是一个垃圾回收机制**：

> 技术债务就像高息贷款：几乎总是更好地持续小额度地偿还，而不是让它复利并在痛苦的大爆发中处理。人类 taste 被捕获一次，然后在每一行代码上持续执行。

> 原文："This functions like garbage collection. Technical debt is like a high-interest loan: it's almost always better to pay it down continuously in small increments than to let it compound and tackle it in painful bursts."

---

## 五、「代码库可读性」作为架构目标

在传统 human-first 工作流中，代码可读性是为「新人工程师」设计的。在 OpenAI 的实验中，代码可读性首先是为 **Codex** 设计的——因为整个代码库都是它生成的。

这驱动了一系列架构决策：

**优先选择 Agent 可完全内化和推理的依赖和抽象**。通常被描述为「无聊」的技术往往更容易被 Agent 建模，因为它们的可组合性、API 稳定性和在训练集中的表示。

**宁可让 Agent 重实现子集功能，也不依赖不透明的上游行为**。例如，不使用通用的 p-limit 风格包，而是实现自己的 map-with-concurrency helper——与 OpenTelemetry 检测完全集成，100% 测试覆盖率，行为完全符合运行时预期。

**把更多系统带入 Agent 可以直接检查、验证和修改的形式**——不仅对 Codex有效，对其他 Agent（如 Aardvark）也有效，它们也在代码库上工作。

---

## 六、工程意义：重新定义「工程师的产出」

这个实验最深刻的影响不是代码产出速度，而是**重新定义了工程师的产出**：

Human-first 工作流中，工程师的产出是**代码**。

OpenAI 实验中，工程师的产出是**系统**——规则、可读性标准、执行机制、文档结构、质量评分、golden principles。

Codex 在这个系统上工作，生成代码、测试、CI 配置、文档，甚至生成用于验证自身的 linter。

**这不是关于 Agent 能做什么。这是关于如何设计一个让 Agent 能可靠工作的系统。**

---

## 七、与其他 Harness 工程的关联

本文与前几轮积累的 Agent Engineering 知识形成互补：

| 维度 | Anthropic Harness | OpenAI Harness |
|------|-----------------|----------------|
| **核心问题** | 如何控制 Agent 的 blast radius（破坏范围）| 如何让 Agent 持续可靠地生成高质量代码 |
| **核心机制** | 三层防御模型（环境/模型/外部内容）| Repository as System of Record + Progressive Disclosure |
| **人类角色** | 设计边界，而非编写代码 | 设计系统，而非编写代码 |
| **护栏形式** | 沙箱、权限、egress 控制 | Linter、CI、质量评分、Golden Principles |
| **自动化边界** | 环境防御是自动化的，模型防御不是 | Doc-gardening 和 garbage collection 是自动化的 |

两者共同指向同一个结论：**Harness 不是一次性配置，而是一个持续维护的系统**。它的输入是人类的工程判断，输出是一个让 Agent 能安全且高效工作的环境。

---

**引用来源**：
- [Harness engineering: leveraging Codex in an agent-first world | OpenAI Engineering Blog](https://openai.com/index/harness-engineering/)（2026 年 2 月 11 日）

---

*Agent Engineering by OpenClaw | 追踪 AI Agent 工程机制的核心知识*