# 3行配置管住 Agent：自然语言权限的工程突破

> **核心观点**：Cursor SDK 的 auto-review 机制引入了一种全新的 Agent 权限配置范式——不再写静态规则代码，而是用自然语言描述"什么样的操作我信任、什么样的操作我需要审查"。这是一个从「代码规则」到「语义描述」的根本转变，让安全配置的门槛降到了任何能写文字的人都能完成的程度。

## 一、背景：传统 Agent 权限系统的三重困境

在 Cursor SDK 之前，业界对 AI Coding Agent 的权限控制主要有三种方式：

**第一种：硬编码 Allowlist/Denylist**
```json
{
  "allow": ["/read", "/inspect"],
  "deny": ["DELETE", "/rm", "/format"]
}
```
问题：规则是精确的字符串匹配，无法表达语义意图。"允许读取 ./dist 下的文件"——字符串匹配无法区分 `./dist/readme.md` 和 `./dist/../secrets.json`。

**第二种：基于操作类型的分类许可**
按"读/写/执行/删除"分类，每个类别要么全开要么全关。问题：过于粗糙，删除操作有时是合理的（清理 build 产物），有时是危险的（删源代码）。

**第三种：每次执行前人工审批**
问题：在 headless/CI 环境下没有人工介入，导致要么全关（失去 Agent 自主性），要么全开（失去安全保障）。

这三种方式的共同缺陷：**规则是工程师设计的，需要工程师维护**。当业务人员（非工程师）想让 Agent 执行某个任务时，他们无法表达"我相信这个操作"，只能依赖工程师提前写好的规则。

## 二、Cursor SDK 的解法：自然语言 + Classifier

Cursor SDK 的 auto-review 机制（2026年6月更新）提供了一种全新的权限配置思路：

### 2.1 配置方式：用文字描述信任

开发者不再写精确的规则代码，而是用自然语言描述期望的行为：

```json
{
  "autoRun": {
    "allow_instructions": [
      "Read-only inspections of build artifacts under ./dist are fine."
    ],
    "block_instructions": [
      "Always pause delete operations so I get a chance to review them."
    ]
  }
}
```

这不是规则代码，而是**语义描述**。"Read-only inspections of build artifacts under ./dist are fine"——任何工程师甚至业务人员都能理解这句话的含义，并能够根据业务需求修改它。

> 引用原文：
> "You steer that classifier with natural-language instructions in permissions.json. The autoRun.allow_instructions field describes call shapes to lean toward allowing, and autoRun.block_instructions describes the ones to hold for review." — [Cursor Changelog: SDK Updates June 2026](https://cursor.com/changelog/sdk-updates-jun-2026)

### 2.2 运行机制：Classifier 而非静态规则

关键在于"classifier"这个组件。它不是一个简单的字符串匹配器，而是一个**理解自然语言意图的分类模型**：

- `allow_instructions`：描述"倾向于自动允许"的调用形态 → Classifier 看到匹配模式的调用，自动放行
- `block_instructions`：描述"必须暂停审查"的调用形态 → Classifier 看到匹配模式的调用，触发人工暂停

这不是"精确匹配"，而是"语义相似度匹配"。同一个操作符 delete，Classifier 会根据调用上下文（是删除 `./dist` 还是 `./src`）做出不同判断。

> 引用原文：
> "A classifier decides which calls run automatically and which to hold back, rather than bypassing review entirely." — [Cursor Changelog: SDK Updates June 2026](https://cursor.com/changelog/sdk-updates-jun-2026)

### 2.3 为什么是"倾向"而非"绝对"

`allow_instructions` 说的是"lean toward allowing"（倾向于允许），`block_instructions` 说的是"hold for review"（暂停审查）。这意味着 Classifier 给出的是**概率性判断**而非确定性规则。

这是有意为之的设计：
- 如果规则是绝对的，边界情况会产生误伤（正常操作被阻止）
- 如果 Classifier 给出概率，开发者可以通过调整指令的措辞来影响判断的阈值

这种设计让权限配置变成了一种**迭代优化过程**：运行时观察 Classifier 的行为，调整 `allow_instructions`/`block_instructions` 的措辞，再次观察。这与传统的"写规则 → 测试 → 修bug"循环完全不同。

## 三、为什么这是一个工程突破

### 3.1 非工程师可维护

传统权限系统：规则是代码 → 需要工程师维护
Cursor SDK 新范式：规则是文字 → 任何能读懂文字的人都能维护

这对企业场景意义重大。当业务部门（非工程师）使用 AI Coding Agent 时，他们不需要等待工程师来更新权限配置——他们可以直接修改 `permissions.json` 中的自然语言描述。

> 笔者认为：这是"非工程师 Agent 构建"这个大命题的一个具体落地场景。当 Agent 的安全边界可以用自然语言描述，而不需要用代码表达，"让业务人员直接配置 Agent 行为"就从口号变成了工程现实。

### 3.2 安全与自主性的平衡点

完全自主（无审查）：高效率但高风险
完全人工审批：高安全但低效率

Classifier 机制找到了一个中间点：对于语义上"合理"的操作（如读取 build 产物），自动放行；对于语义上"敏感"的操作（如删除文件），触发人工介入。这不是"部分自主"，而是**基于语义理解的差异化自主**。

### 3.3 从单次判断到上下文感知

传统 Allowlist 的判断是单次的：一个操作要么允许要么拒绝。
Classifier 的判断是上下文敏感的：同一个操作符在不同上下文中会被不同对待。

例如，`DELETE` 调用：
- 目标是 `./dist/build/` → Classifier 倾向自动允许（build 产物可以清理）
- 目标是 `./src/` → Classifier 触发审查（源代码删除是敏感的）

这种上下文感知能力是传统静态规则系统无法实现的。

## 四、与 Claude Code Auto-Mode 的对比

Cursor SDK 的 auto-review 与 Anthropic 的 Claude Code Auto-Mode 都是 Agent 权限分类机制，但设计哲学不同：

| 维度 | Claude Code Auto-Mode | Cursor SDK Auto-Review |
|------|----------------------|------------------------|
| **配置方式** | Transcript Classifier（基于对话记录）| 自然语言指令（permissions.json）|
| **规则来源** | 隐式学习（从对话中推断）| 显式描述（开发者直接写）|
| **可解释性** | 低（Classifier 是黑盒）| 高（规则是自然语言）|
| **适用场景** | 通用代码场景 | 特定项目/领域 |
| **维护难度** | 需要对话数据积累 | 直接修改文本即可 |

> 笔者认为：两种方案不是竞争关系，而是互补的。Claude Code Auto-Mode 的 Transcript Classifier 适合通用场景（不需要预先配置）；Cursor SDK 的自然语言权限适合特定领域（需要明确的业务边界描述）。企业级 Agent 系统可能同时使用两者——通用边界用 Classifier，特定业务规则用自然语言配置。

## 五、局限性与尚未解决的问题

1. **Classifier 的判断依据不透明**：开发者无法精确知道 Classifier 基于什么做出判断。当一个操作"意外通过"或"意外被阻止"时，调试困难。

2. **自然语言描述的歧义**：自然语言本身有歧义。"delete operations"是否包括 `rmdir`？是否包括移动到回收站？这种歧义需要通过更精确的措辞来消除，但措辞的专业化又提高了非工程师的门槛。

3. **误判的代价**：如果 Classifier 错误地自动执行了一个危险操作（如删除了生产数据库），后果是真实的。目前没有机制来限制"自动通过"操作的最大破坏半径。

## 六、结论

Cursor SDK 的 auto-review 机制代表了一个重要方向：**Agent 权限配置从代码表达走向语义表达**。这个转变的深层含义是：Agent 的安全边界不再是"工程师才懂的技术细节"，而是"任何能描述业务意图的人都能参与设计的规则"。

对于构建"非工程师也能使用和配置"的 Agent 系统，自然语言权限配置是一个值得关注的技术方向。

---

**引用来源**：
- [Cursor Changelog: SDK Updates June 2026](https://cursor.com/changelog/sdk-updates-jun-2026)（auto-review + natural language permissions 核心来源）
- [Cursor 文档: Agent Tools / Run Mode](https://cursor.com/docs/agent/tools/terminal#run-mode)（permissions.json 配置格式）