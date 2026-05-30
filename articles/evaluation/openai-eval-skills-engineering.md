# 系统性测试 Agent Skills：OpenAI 的 Eval 工程方法论

> 迭代 Agent Skill 时，最大的问题不是「改完感觉更好」，而是「不知道是否真的更好」。一个版本更快，另一个更可靠，然后回归悄悄渗入：skill 不触发、跳过必需步骤、留下多余文件。OpenAI 在 Codex 上的 eval 实践给出了一个清晰的答案——用结构化的测评循环替代主观感觉。

## 核心命题

**好的 Agent Skill 迭代不是靠感觉，而是靠可验证的测量**。OpenAI 的 eval 方法论将 Agent Skills 的测试变成一个闭环：通过 `codex exec --json` 捕获行为事件，用确定性检查验证命令是否执行、用 rubric-based grading 处理规则难以覆盖的模糊质量维度。这个方法让「感觉更好」变成「证明更好」。

## 一、问题：Agent Skill 迭代的回归困境

当我们迭代一个 Agent Skill（如 Codex 的 skill），很难判断是否真的在改进，还是只是改变了行为。

典型的困境：
- 一个版本「感觉」更快
- 另一个「似乎」更可靠
- 然后回归悄悄渗入：skill 不触发、跳过必需步骤、留下多余文件

问题的根源在于 **Agent Skill 的行为是概率性的**，而测试手段是主观的。

### Agent Skill 的结构

一个 Codex skill 本质上是一个目录，包含：
- `SKILL.md`：YAML front matter（元数据：name、description）+ Markdown 指令
- `resources/`：可选的 API 规范、UI 资源等
- `scripts/`：可选的支持脚本

其中 **name 和 description 比看起来更重要**——它们是 Codex 判断「何时触发这个 skill」的主要信号。如果这两个字段模糊或过载，skill 就不会可靠地触发，后续的指令再完善也没用。

## 二、解法：三层 Eval 架构

OpenAI 给出的是一个三层叠加的 eval 架构，每层解决不同类型的问题。

### 第一层：确定性检查（Deterministic Checks）

这是 eval 的核心。启用 `codex exec --json` 后，stdout 变成 JSONL 流，每个命令执行事件都被结构化地记录。

```json
{"event": "command_execution", "command": "npm install", "exit_code": 0}
{"event": "file_created", "path": "package.json"}
{"event": "command_execution", "command": "npx tsc", "exit_code": 1}
```

基于这些事件，你可以写确定性检查：
- Did it run `npm install`?
- Did it create `package.json`?
- Did it invoke the commands, in the right order?

这些检查 **非黑即白**，不存在模糊地带。回归一旦发生，JSONL 会精确地告诉你哪个环节出了问题。

### 第二层：Rubric-Based Grading（规则覆盖不到的模糊质量）

确定性检查能覆盖「是否执行了正确的命令」，但无法评估「代码风格是否合规」「文档是否完整」这类主观维度。

OpenAI 的解法是通过 `--output-schema` 定义一个 JSON Schema，用第二个 `codex exec` 调用来检查样式和约定：

```bash
codex exec --output-schema rubric.json -- repo_path
```

这个过程：
1. 第一个 Codex 执行 → 实际完成工作
2. 第二个 Codex 执行 → 仅检查输出，返回 rubric-compliant JSON

这种方式把「质量判断」从主观变成了结构化评分。

### 第三层：定性人工检查（Qualitative Checks）

当规则和 rubric 都无法覆盖时，引入人工 review。但这个 review 不是随意的——它基于前面两层已经输出的结构化数据。这意味着即使需要人工介入，reviewer 看的也是具体的失败报告，而非模糊的「感觉不对」。

## 三、关键实践：让 Eval 起作用

### 实践 1：从「可检查的完成定义」开始

好的 eval 始于一个 **清晰的、可以被验证的「完成」定义**。

不好的定义：「skill 应该能正确处理用户的代码审查请求」

好的定义：「当用户说 `/review` 时，agent 必须：
1. 运行 `npm test`
2. 在输出中找到 FAIL 或 ERROR 关键字
3. 如果找到，创建一个包含错误摘要的 comment
4. comment 必须在 60 秒内发布」

后者可以写成确定性检查，前者只能靠感觉。

### 实践 2：用 `$skill-creator` 引导，快速验证触发条件

Codex 内置了一个 skill creator（本身也是一个 skill），它会引导你完成：
- skill 做什么
- 何时触发
- 是 instruction-only 还是 script-backed

这个 bootstrap 工具的价值在于：**在动手写完整的 SKILL.md 之前，先验证触发条件是否可靠**。如果 name/description 无法让 Codex 正确识别场景，后续的细节优化都是徒劳。

### 实践 3：用 `codex exec` 实现自动化和 CI 集成

`codex exec` 是为自动化和 CI 设计的：
- 进度流输出到 stderr（不污染主输出）
- 最终结果写到 stdout（便于脚本捕获）
- `--json` 模式让每次运行的结构化事件都可追溯

这意味着 eval 不是手动运行的，而是每次 PR 都可以触发自动化检查。

### 实践 4：失败驱动覆盖率（Let Real Failures Drive Coverage）

最后一条原则：**不要预先设计完美的覆盖率**，而是让真实失败驱动 coverage 的扩展。

实际流程：
1. 运行 agent
2. 发现一个失败场景（skill 不触发、错误步骤、残留文件）
3. 为这个场景添加一个确定性检查或 rubric 规则
4. 下次运行时验证修复

这种方式确保每次 coverage 扩展都对应真实发生的问题，而不是假设的问题。

## 四、与 Agent Harness 的关系

这套 eval 方法论实际上是 **Harness 工程的关键组件**。Harness 不只是「让 agent 运行起来」，还包括「如何验证 agent 的行为符合预期」。

在长程 Agent 工作流中，eval 的角色是：
- **Short feedback loop**：每一步都可以被验证，而非等到整个任务完成才发现问题
- **Regression detection**：防止新版本的修改破坏已有功能
- **Behavior grounding**：把概率性输出锚定到确定性验证

这也是为什么 OpenAI 在 eval-skills 的结尾特别强调：「一旦这个 loop 存在，每次改动都更容易确认，每次回归都更清晰」。

## 五、实践建议

对于构建 Agent 系统的工程师：

1. **先定义「完成」**：在写任何 SKILL.md 之前，先写下 skill 的完成定义（必须可验证）
2. **从确定性检查开始**：先覆盖「命令是否执行、文件是否创建」这类明确事件
3. **用 rubric 处理模糊质量**：代码风格、文档完整性这类维度用结构化评分而非手动 review
4. **让失败驱动 coverage**：不预判问题，让真实运行中的失败扩展你的测试集

这个方法论的价值不只在于「测试」，而在于它把 Agent Skill 的开发从艺术变成了工程。

---

**引用来源**：
- OpenAI Developers Blog: "Testing Agent Skills Systematically with Evals" (https://developers.openai.com/blog/eval-skills)
- Codex skill creator 内置工具（`$skill-creator`）
- `codex exec --json` 和 `--output-schema` 命令行参数

**关联项目**：[NousResearch/hermes-agent](#) — 173K Stars 的自学习 Agent，内置 skill bundles 和 Promptware 防御，与本文的 skill 测试方法论形成互补