# LangChain Interpreter Skills：将 Harness 逻辑下沉到可执行代码模块

> 原文：[Building workflows for agents with Skills and Interpreters](https://www.langchain.com/blog/interpreter-skills) — Hunter Lovell, LangChain Blog, May 29, 2026

---

## 核心命题

Skills 的演进正在改变 Agent 的架构逻辑：旧范式中，Skill 是一组告诉模型「怎么做」的指令，模型必须忠实地遵循这些指令；而在 Interpreter Skills 新范式中，Skill 既是「什么时候用」的行为描述，也是一个**可直接执行的代码模块**。确定性逻辑从「模型遵循指令」迁移到「代码可靠执行」，这一步切换了评价体系的基准。

---

## 一、从「指令跟随」到「代码调用」

### 旧范式的局限性

传统的 Skill 本质上是一份 Prompt 文档。SKILL.md 告诉 Agent 什么时候该调用某个技能、该怎么用、有什么约束。模型负责读取这些指令并在上下文中执行。

这种模式的问题在于：**确定性依赖于模型忠实地遵循指令**。对于复杂的多步骤工作流，每次执行都可能走出不同的路径——模型可能误解约束，可能在边界情况下做出错误假设，也可能在重复任务上每次都「重新发明轮子」。

> 引用原文：
> "A normal skill tells the agent how to do a task and hopes it follows along."

### 新范式的转变

Interpreter Skills 将 Skill 的能力分成两层：

| 层次 | 载体 | 能力描述 |
|------|------|---------|
| **行为描述层** | SKILL.md | 告诉模型「什么时候该用这个技能」「该传入什么参数」「如何使用输出」 |
| **执行逻辑层** | index.ts（TypeScript 模块） | 包含**确定性代码**，模型通过 import 调用，代码直接执行而非通过 Prompt 再解释 |

当模型决定调用某个 Interpreter Skill 时，它不是在读取一段文字描述然后自己实现逻辑，而是直接 import 一个函数并调用：

```typescript
const { triage } = await import("@/skills/github-triage");

const result = await triage("langchain-ai/deepagents", {
  issues: true,
  prs: true,
  discussions: true,
});
```

模型决定「要不要用这个技能」「传什么参数」「如何处理输出」，但**技能的实际执行逻辑**在代码中定义，不再依赖模型的指令跟随能力。

---

## 二、Skills 可以操控 Harness 了

这个变化有一个更深层的含义：**Interpreter 代码可以与 Harness 本身交互**，而不仅仅是在模型层面工作。

引用原文：

> "Because interpreter code can talk to the agent loop directly, a skill can spawn subagents, manage a task graph, and handle partial failures as one reviewed workflow."

这意味着 Skill 不再只是「给模型的提示词扩展」，而变成了 **Harness 层的行为模块**：

- Skill 代码可以**生成子 Agent**，协调多 Agent 工作流
- Skill 代码可以**管理任务图**，处理部分失败和重试逻辑
- Skill 代码可以在 Harness 层面控制工作流状态，而不需要模型每次都重新规划

从工程角度看，这是一个重要的分层变化：

```
旧架构：
Model ← Prompt ← SKILL.md（指令）

新架构：
Model ← SKILL.md（描述）
     ↕
  Harness
     ↕
index.ts（可执行代码）→ 可调用子 Agent / 操作工具 / 管理状态
```

---

## 三、评价体系的切换

传统 Skill 的评价问题是模糊的：「模型有没有遵循指令？」——这依赖主观判断，且边界不清。

Interpreter Skill 的评价可以具体得多：

> 引用原文：
> "Agent work can now be more easily evaluated. Instead of asking 'did the agent generally follow instructions?', you can ask more concrete questions like 'did it call the expected function?'"

从「指令遵循」到「函数调用」的评价转换，实际上是将 AI 工作的质量保证从「模型输出质量」层下沉到了「接口调用正确性」层。这对于需要合规审计的生产环境意义重大——你可以在代码层记录每一次函数调用，而不需要解析模型的思维链。

---

## 四、Interpreter Skill 的实际结构

每个 Interpreter Skill 包含两部分：

### SKILL.md（行为描述）

```yaml
---
name: github-triage
description: Use this skill to triage GitHub issues, pull requests, and discussions.
metadata:
  module: ./index.ts
---

Use this skill when a user asks for repository triage.

Import the module using the interpreter and call `triage(repo, options)`.
```

这里告诉模型：
- 什么场景下应该调用这个技能
- 调用哪个函数、传什么参数
- 结果怎么用

### index.ts（执行逻辑）

```typescript
export function triage(repo: string, options: TriageOptions) {
  // 确定性代码：获取数据 → 生成子 Agent → 处理结果
}
```

代码逻辑可以包含：
- 对外部 API 的调用（GitHub API 等）
- 业务规则判断
- 生成子 Agent 处理具体任务
- 错误处理和重试逻辑

值得注意的是，这里的代码运行在 **Interpreter 运行时**中，而非直接访问主机环境：

> 引用原文：
> "Unlike sandboxes, interpreter code does not get unrestricted access to the host environment by default. Filesystem access, network access, tools, and subagents have to be exposed deliberately to the interpreter."

这保证了代码的安全性——即使 Skill 模块本身是第三方提供的，它的访问边界仍然在 Harness 的控制之下。

---

## 五、与「Skills 作为 API」的关联

这个方向的演进本质上是将 **Skill 从 Prompt 扩展转变为可组合的 API 单元**。当 Skill 包含确定性的代码模块时：

1. **版本化管理**：Skill 的代码可以在 Git 中版本化，可以 code review，可以 CI 测试
2. **可测试性**：函数单元测试替代了「模型是否遵循指令」的模糊判断
3. **可复用性**：同一个 Skill 模块可以被不同的 Agent 在不同场景下调用
4. **可审计性**：函数调用日志天然就是操作审计记录

这与 Anthropic 的 Agent Skills 概念一脉相承，但执行逻辑从模型侧转移到了代码侧——从「模型记住怎么做」变成「代码知道怎么做，模型决定什么时候用」。

---

## 六、工程评价

**优势**：
- 将确定性逻辑从模型层下沉到代码层，降低了执行不确定性
- 评价从模糊的「指令遵循」变成具体的「函数调用」，可审计性大幅提升
- Skill 可以操控 Harness 层（生成子 Agent、管理任务图），实现了 Skill 对工作流编排的参与
- 代码模块可以版本化管理、测试，Skill 本身成为可工程化的组件

**局限**：
- 当前仅限于 TypeScript 运行时（Deep Agents 的 Interpreter），泛化到其他框架需要适配
- Skill 模块的安全性依赖于 Interpreter 的权限控制机制，模块供应链安全需要关注
- 模型仍然需要正确判断「什么时候该调用 Skill + 传什么参数」，这部分的评价问题并未完全消失

**适用场景**：
- 需要确定性执行路径的生产级工作流（如 GitHub Triage、合规检查、数据清洗）
- 需要对 Agent 行为进行合规审计的场景（函数调用的可追溯性 > 思维链的不可追溯性）
- 需要 Skill 被多个 Agent 复用的场景（Skill 作为共享能力单元）

---

## 结论

Interpreter Skills 代表了一个明确的架构方向：**将 Skill 的确定性逻辑代码化，将其从 Prompt 层下沉到执行层**。这不是对 Skill 概念的替代，而是对其能力边界的扩展——从「告诉模型怎么做」进化到「给模型提供一个可靠的可调用接口」。

对于构建生产级 Agent 系统的团队，这个方向的实践价值在于：它让 Skill 变成了一个可以**测试、版本化、审计**的工程单元，而不再只是一个 Prompt 片段。
