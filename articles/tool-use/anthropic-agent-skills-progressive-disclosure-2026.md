# Anthropic Agent Skills：让通用 Agent 掌握专业化能力的工程方法论

> 本文解决的问题：如何将人类的领域知识转化为 Agent 可动态加载的专业化能力，以及这种「技能封装」模式与传统的 Tool/Plugin 体系的本质区别。

## 1. 核心主张

**Agent Skills 是一种基于渐进式披露（Progressive Disclosure）的知识封装范式**，它不是让 Agent 调用一个「功能」，而是让 Agent 在需要时发现、加载、和执行一个「能力包」——这个能力包包含了人类专家的领域知识、流程步骤和可执行脚本。

> "Building a skill for an agent is like putting together an onboarding guide for a new hire."
> — [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

这种设计哲学与传统的 Tool/Function Calling 有根本性差异：Tools 是被动的「被调用」，而 Skills 是主动的「被发现和使用」。Agent 需要理解自己缺什么能力，然后去找到并加载对应的 Skill——这要求 Skill 的元数据（name 和 description）足够精确，使得 Agent 能够做出正确的触发决策。

## 2. 为什么需要 Skills：通用 Agent 的专业化困境

Anthropic 指出了核心问题：随着模型能力提升，通用 Agent（如 Claude Code）已经能够处理跨领域的复杂任务，**但它们缺乏领域特定的专业知识**。

传统的解决方案有两种：

| 方案 | 做法 | 局限 |
|------|------|------|
| **定制化 Agent** | 为每个领域构建专用 Agent | 每个用例都需要从头设计，碎片化，无法组合 |
| **Prompt 注入** | 把领域知识塞进 system prompt | context 膨胀， knowledge 难以复用，维护困难 |

Anthropic 提出的 Skills 方案试图同时解决这两个问题：**允许任何人将专业知识封装为可组合的资源**，让通用 Agent 在需要时动态获取专业化能力，同时保持 Agent 本体的通用性。

## 3. 渐进式披露：Skills 的核心架构原则

### 3.1 三层披露机制

Anthropic 在文章中明确指出了 Skills 的核心设计原则——**渐进式披露**（Progressive Disclosure）。这与传统的「把所有信息一次性塞进 context」的做法有本质区别。

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 启动时的元数据（minimal footprint）               │
│  ─────────────────────────────────────────────────────────  │
│  system prompt 中只包含每个 Skill 的 name + description      │
│  这足够让 Agent 判断「我是否需要这个 Skill」                  │
└─────────────────────────────────────────────────────────────┘
                              ↓ 触发后
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: SKILL.md 完整内容（按需加载）                      │
│  ─────────────────────────────────────────────────────────  │
│  当 Agent 认为某个 Skill 相关时，它会主动读取完整的 SKILL.md │
│  包含：instructions、scripts、references 等完整资源          │
└─────────────────────────────────────────────────────────────┘
                              ↓ 需要时
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: 关联文件（scenario-specific）                      │
│  ─────────────────────────────────────────────────────────  │
│  SKILL.md 可以引用同级目录下的其他文件（reference.md、       │
│  forms.md 等），Agent 在需要时自行发现和读取                  │
│  这些文件只在特定场景下被加载，避免污染 context              │
└─────────────────────────────────────────────────────────────┘
```

以 PDF Skill 为例：
- **SKILL.md**：核心操作指令（读取 PDF、提取文本）
- **forms.md**：表单填写专项指导（仅在填写表单时加载）
- **reference.md**：PDF 结构参考（仅在需要时加载）

> "Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed."

### 3.2 为什么渐进式披露优于全量加载

传统的 RAG 或 system prompt 注入是将所有知识一次性灌入 context——这会导致：

1. **context 膨胀**：知识越多，context 被压缩，有效信息密度下降
2. **检索干扰**：Agent 的 attention 被无关知识分散，影响决策质量
3. **触发模糊**：Agent 不知道何时该使用哪部分知识

渐进式披露通过**让 Agent 自己决定加载什么**来解决这个问题。Agent 的 reasoning process 本身就是触发机制——当 Agent 发现自己缺乏某个领域的操作知识时，它会主动加载对应的 Skill。

## 4. SKILL.md 的格式规范与最佳实践

### 4.1 必须的 YAML Frontmatter

SKILL.md 文件必须以 YAML frontmatter 开头，包含 `name` 和 `description`：

```yaml
---
name: pdf-form-filling
description: Fill out PDF forms with structured field extraction and validation
---
```

这两个字段在 Agent 启动时被加载到 system prompt 中，Agent 用它们来判断是否需要触发该 Skill。

### 4.2 结构化扩展：当 SKILL.md 变得过于庞大

Anthropic 明确指出了一个临界点：**当 SKILL.md 变得过于庞大时，应该拆分到多个文件**。

> "If the SKILL.md file becomes unwieldy, split its content into separate files and reference them."

判断标准：
- **互斥场景**：某些 context 只在特定场景下相关 → 拆出去
- **体积控制**：单个文件超过 Agent context 可接受范围 → 拆出去
- **Token 优化**：减少不必要的 token 消耗 → 拆出去

关键设计洞察：**代码既是工具，也是文档**。脚本文件可以被 Agent 直接执行（作为 tool），也可以被 Agent 读取为参考文档（作为 knowledge）——取决于场景。

### 4.3 Skills 与代码执行

Skills 可以包含预写的脚本，Agent 在认为合适时将其作为 tool 执行：

```python
# PDF skill 中的 form_extractor.py
import pdfplumber

def extract_form_fields(pdf_path):
    """Extract all form fields from a PDF for inspection."""
    with pdfplumber.open(pdf_path) as pdf:
        fields = []
        for page in pdf.pages:
            for annot in page.annotations:
                if annot.type == "widget":
                    fields.append({
                        "name": annot.field_name,
                        "type": annot.field_type,
                        "value": annot.field_value
                    })
        return fields
```

Agent 无需将脚本或 PDF 文件加载到 context 中即可执行这些操作——这解决了 LLM 在处理大型二进制文件时的 token 效率问题。

## 5. Skills 的评估与迭代方法论

### 5.1 从评估出发的开发流程

Anthropic 建议 Skills 开发遵循以下循环：

```
识别能力缺口 → 构建增量 Skill → 评估 → 发现问题 → 迭代优化
```

具体步骤：
1. **识别缺口**：让 Agent 在代表性任务上运行，观察它在哪些地方挣扎或需要额外 context
2. **构建 Skill**：针对观察到的缺口编写 Skill
3. **迭代验证**：与 Agent 一起工作，观察它如何使用 Skill，追踪意外轨迹或过度依赖

### 5.2 从 Claude 的视角迭代

> "Think from Claude's perspective: Monitor how Claude uses your skill in real scenarios and iterate based on observations"

Anthropic 建议的一个重要实践是：**让 Claude 自己帮助构建 Skill**。

- 在与 Claude 一起工作时，要求它将成功的模式和常见错误捕获为可复用的 context 和 code
- 当 Claude 使用 Skill 跑偏时，要求它自我反思哪里出了问题
- 这个过程帮助发现 Claude **真正需要**的 context，而不是你预设的 context

## 6. 安全考量：Skills 的攻击面

Skills 提供了强大的能力扩展，但同时也引入了新的攻击面。Anthropic 明确警告：

> "Malicious skills may introduce vulnerabilities in the environment where they're used or direct Claude to exfiltrate data and take unintended actions."

### 安全建议

1. **只安装来自可信来源的 Skills**
2. **在安装前审计 Skill 内容**：阅读所有打包的文件，特别关注代码依赖和外部网络连接
3. **注意指令中的异常行为指示**：如果 Skill 指导 Agent 连接不受信的外部网络来源，需要警惕

## 7. Skills 与 MCP 的互补关系

Anthropic 在文章中展望了 Skills 与 Model Context Protocol (MCP) 的关系：

> "We're especially excited about the opportunity for Skills to help organizations and individuals share their context and workflows with Claude. We'll also explore how Skills can complement MCP servers by teaching agents more complex workflows that involving external tools and software."

**核心洞察**：MCP 解决的是「如何连接外部工具」的问题（协议层），Skills 解决的是「如何让 Agent 学习复杂工作流程」的问题（知识层）。

两者是互补的：
- MCP 服务器提供标准化的工具接入
- Skills 提供领域知识和操作流程的封装

当一个复杂工作流程涉及多个外部工具时，Skill 可以将 MCP 服务器的调用编排成一个连贯的操作序列——这是 Skills 的独特价值。

## 8. 未来展望：Agent 自创建 Skills

Anthropic 展望了一个关键方向：

> "Looking further ahead, we hope to enable agents to create, edit, and evaluate Skills on their own, letting them codify their own patterns of behavior into reusable capabilities."

这意味着未来的 Agent 不仅能使用 Skills，还能**创造 Skills**——将自己在任务中发现的模式和行为 codified 为可复用的能力包。这是一个重要的范式转变：从「人类教 Agent 技能」到「Agent 自己积累技能」。

## 9. 实践建议清单

基于 Anthropic 的文章，笔者总结以下关键检查点：

**Skill 编写层面**
- [ ] Skill 的 name + description 足够精确，能让 Agent 做出正确的触发决策
- [ ] SKILL.md 不超过必要长度，场景互斥的内容拆到独立文件
- [ ] 代码文件明确标注「直接执行」还是「作为参考」
- [ ] 包含 Agent 使用 Skill 过程中的自我反思机制

**评估迭代层面**
- [ ] 从代表性任务评估开始，识别 Agent 的能力缺口
- [ ] 让 Claude 参与 Skill 的迭代优化
- [ ] 追踪 Skill 加载后的 Agent 行为轨迹，发现意外依赖

**安全层面**
- [ ] 不安装来源不明的 Skill
- [ ] 安装前完整审计 Skill 内容（文件结构 + 代码依赖 + 外部网络行为）
- [ ] 最小化 Skill 的权限范围

---

**关联项目**：本文分析了 Anthropic Agent Skills 的工程设计原理，Skills 作为专业化能力封装范式，与 Multi-Agent 编排中的「能力模块化」设计高度相关。推荐结合 ruvnet/ruflo（Claude 原生 Multi-Agent 编排平台，38K ⭐，自学习 swarm 智能）理解 Skills 在多 Agent 协作中的角色。

**引用来源**：
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Anthropic Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Anthropic Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)