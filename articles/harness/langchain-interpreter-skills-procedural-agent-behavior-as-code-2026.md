# LangChain Interpreter Skills：将最佳实践程序编码为可执行代码

>📌 **核心论点**：Interpreter Skills 解决了一个长期悬而未决的问题——当 agent 行为需要「确定性流程」时，如何防止模型在长时任务中因 context耗尽而丢失 coherence。答案是：把流程的实现从 prompt instructions 下沉到 TypeScript 代码，让代码负责 state management，让模型只做高层决策。

## 一、问题：指令型 skill 的根本局限

传统 agent skill 的工作方式是**指令下发**：SKILL.md 描述一套流程，模型读取指令，然后在对话中逐步执行。思路简单，但有一个致命的伸缩性问题——**模型必须在自己的 working context 中 track 每一步状态**。

LangChain 博客中举了一个典型的 triage 场景：

> 如果仓库有 300 个 open issues，模型需要在这 300 个决策点之间保持 coherence，一边处理新的 issues，一边协调过去决策的一致性。随着 context 逐渐接近上限（所谓「context anxiety」），模型会开始走捷径——压缩步骤、跳过细粒度判断、甚至漏掉整个流程。

这不是模型能力的问题，而是**架构设计的问题**：让模型同时承担「决策」和「状态管理」两个职责，在长流程中必然导致其中一方妥协。

## 二、Interpreter Skill 的解决思路

Interpreter Skills 的核心设计是**把 skill变成一个双层结构**：

```
skill/
├── SKILL.md      # 指令层：告诉 agent 什么时候适用、传什么参数
└── index.ts      # 代码层：真正的执行逻辑，可调用工具、可 spawn subagent
```

**指令层（SKILL.md）**负责：
- 描述 skill 的适用场景
- 给出调用方式和参数格式
- 提供 constraints 和 examples

**代码层（index.ts）**负责：
- 实现确定性逻辑（数据转换、循环控制、队列管理）
- 通过 interpreter 与 harness 交互（调用工具、spawn subagent）
- 返回结构化结果（模型可以继续操作）

关键的**解耦**在于：模型决定「什么时候用这个 skill、传什么参数、用输出做什么」，而**代码决定「流程怎么跑、状态怎么维护、中间结果怎么组织」**。

## 三、代码示例：GitHub Triage Skill

以 LangChain 官方示例的 GitHub triage skill 为例：

```typescript
// index.ts
export function triage(repo: string, options: TriageOptions) {
  // 1. 获取所有 open items（GitHub API 调用）
  const items = fetchOpenItems(repo, options);
  
  // 2. 为每个 item spawn 一个 subagent 生成摘要
  const summaries = items.map(item => spawnSubagent('condense', item));
  
  // 3. 按主题聚类
  const clusters = clusterItems(summaries);
  
  // 4. 返回结构化结果
  return {
    clusters,
    unassigned: summaries.filter(s => !s.clustered),
    toMarkdown: () => formatReport(clusters)
  };
}
```

模型调用时只需要：

```typescript
const { triage } = await import("@/skills/github-triage");
const result = await triage("langchain-ai/deepagents", {
  issues: true, prs: true, discussions: true
});
// result.clusters / result.unassigned / result.toMarkdown()
```

对比两种 skill 的保证：

| 维度 | Normal Skill | Interpreter Skill |
|------|-------------|-------------------|
| 流程执行 | 模型自己 track 每一步 | 代码控制流程执行 |
| 状态一致性 | 长流程中模型可能丢 coherence | 代码维护状态，天然一致 |
| 确定性 | 模型每次执行可能有差异 | 同一输入 → 同一输出 |
| 可测试性 | 难以自动化测试 | 可以直接 `triage(...)` 单元测试 |
| subagent 协调 | 模型自己决定何时 spawn | 代码程序化 spawn |

## 四、为什么这个设计值得深度分析

### 1. 解决了 context anxiety，而非对抗 context window

Context anxiety（上下文焦虑）是模型在长时任务中接近 context 上限时表现出的行为退化——开始跳步、压缩流程、丢失细粒度判断。传统解法是增加 context window，但这只是延缓问题。

Interpreter Skills 的解法更根本：**把状态管理工作从模型的 working context 转移到代码**。模型不再需要在300 个决策点之间保持 coherence，只需要调用一次 skill，然后处理返回的结构化结果。

### 2. Skill 的可测试性从此变得可落地

Normal skill 的测试需要「模型按照指令执行」，这依赖模型的一致性，无法可靠自动化。Interpreter skill 的测试可以绕过模型——直接调用 `triage(repo, options)` 并验证输出结构是否符合预期。

这意味着 skill 的迭代从「猜模型会不会理解」变成了「跑单元测试验证逻辑」，这是工程化质变。

### 3. 与 RubricMiddleware 形成正交互补

笔者在 Round 267 分析过 LangChain 的 RubricMiddleware（evaluator loop 模式）：定义完成标准，Agent 自动跑「执行→评分→修订」循环直到满足条件。

Interpreter Skills 和 RubricMiddleware 是 harness 工程的**两个正交维度**：

- **RubricMiddleware** = 把「完成标准」的判定程序化（evaluator loop）
- **Interpreter Skills** = 把「工作流程」的执行程序化（procedural behavior as code）

两者可以组合：Interpreter skill 执行确定性流程 → RubricMiddleware 验证输出质量 → 不满足则重新调用 skill + 修订。

## 五、Interpreter 的安全模型

Interpreter 是一个受控的 TypeScript runtime，与宿主 harness 共享进程。这带来一个关键设计问题：**如果代码可以任意访问系统，agent 就有了提权路径**。

LangChain 的解法是**所有敏感操作必须显式暴露**：

```typescript
// 默认：文件系统、网络、工具不可访问
// 若需要，必须在 harness 层面显式 allowlist
interpreter.allowFileSystem(['/tmp/workspace']);
interpreter.allowTool('github_api');
interpreter.allowSubagent();
```

这与 Docker sandbox 的思路正交——sandbox 是「默认全开放，限制某几个操作」；interpreter 是「默认全禁止，逐个 allowlist」。对于 agent harness来说，后者更合理，因为我们需要**最小权限原则**：代码只能用到明确授权的资源。

## 六、限制与未解决问题

Interpreter Skills 目前处于实验阶段（LangChain 博客明确用了「experimenting」），有几个工程问题尚未完全解决：

1. **跨语言支持**：当前只有 TypeScript runtime，如果你的 agent stack 是 Python 或其他语言，这个 pattern 无法直接复用
2. **debug体验**：当 skill 代码执行出错时，错误栈的 trace 和模型推理过程的对应关系还不清晰
3. **版本同步**：当 SKILL.md 更新后，模型可能还在用旧版指令，而代码已经更新——两者的一致性管理是潜在坑点

## 七、适用场景判断

**适合用 Interpreter Skills 的场景**：
- 需要确定性流程的任务（triage、review、data pipeline）
- 长时任务中模型容易丢失 coherence 的场景
- 需要对 skill 行为做自动化测试的工作流
- 需要在代码层协调多个 subagent 的复杂编排

**不适合用 Interpreter Skills 的场景**：
- 流程本身需要大量探索性判断（model creativity 是核心）
- 任务简单且短小（增加代码层复杂度不划算）
- 非 TypeScript 技术栈（当前只有 TS runtime）

---

**引用来源**：
- [Interpreter Skills: Building Workflows for Agents](https://www.langchain.com/blog/interpreter-skills)（LangChain Blog）
- [Give your agents an interpreter](https://www.langchain.com/blog/give-your-agents-an-interpreter)（interpreter 基础设计）
- [LangChain Deep Agents](https://www.langchain.com/blog/deep-agents)（Skills 系统背景）