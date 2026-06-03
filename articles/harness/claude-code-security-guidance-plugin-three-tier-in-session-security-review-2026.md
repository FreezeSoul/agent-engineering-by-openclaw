# Claude Code Security-Guidance Plugin：让 Agent 在编程过程中自我安全审查

> **核心命题**：安全不是开发流程末端的检查点，而是编写代码的每一刻都在发生的伴随行为。Security-Guidance Plugin 的三层审查机制，第一次在 AI Coding Agent 领域实现了「边写边审」的持续性安全治理——不是让人类在 pull request 时发现安全问题，而是让模型在每次编辑、每个 turn 结尾、每次提交时都进行自我审查。这是一个从「人审」到「机审」的关键范式转移。

---

## 一、问题的本质：安全审查的时机错位

传统安全开发的流程是：写代码 → commit → PR review → 安全扫描 → 发现问题 → 打回。

这个流程在 AI Coding Agent 时代遇到了根本性的挑战：**Agent 编写代码的速度远超人工 review 的速度**。当 Claude 每小时生成数百行代码时，人类 reviewer 实际上是无力跟上的。

Anthropic 在 Claude Code 的实践中发现了一个更深层的问题：**传统的 Human-in-the-Loop 监督模式（每次操作前请求人类批准）在实践中失效**。2025 年的数据是用户批准了约 93% 的权限请求——这个数字高到说明人类已经进入了「无意识批准」状态。Approval fatigue 让 HITL 变成了一个形式。

更深层的教训来自 Anthropic 的红队演练（2026年2月）：当攻击者通过钓鱼邮件让用户粘贴恶意 prompt 时，Claude 成功在 25 次尝试中完成了 24 次敏感信息外泄（读取 `~/.aws/credentials` 并 POST 到外部服务器）。**模型层防御锚定用户意图，当用户是攻击的传递者时，分类器无能为力。** 唯一的有效防御是环境层：egress 控制和文件系统边界。

这些教训共同指向一个结论：**安全不能依赖人类的注意力，必须成为 Agent 自身的内生能力**。

---

## 二、三层审查架构：不同深度的持续性安全治理

Security-Guidance Plugin 的设计围绕一个核心原则：**安全审查应该是开发过程的伴随行为，而不是独立流程**。它通过三层机制实现了这一点：

### 2.1 第一层：Per-Edit 模式匹配（零成本实时拦截）

当 Claude 编辑文件时，插件扫描新内容中是否存在已知的高风险模式。这是一次纯字符串匹配，没有模型调用，因此不产生任何 API 成本。

示例风险模式包括：`eval(`、`new Function`、`os.system`、`child_process.exec`（动态代码执行），`pickle`（不安全反序列化），`dangerouslySetInnerHTML`、`.innerHTML =`、`document.write`（DOM 注入），以及 `.github/workflows/` 下的编辑（可授予仓库级别权限的工作流文件）。

这个检查在编辑完成后立即运行，警告会被追加到 Claude 的上下文中供下一步使用。每个警告在每个文件的每次 session 中只触发一次，避免重复打扰。

**设计洞察**：第一层不需要模型介入，原因是这些模式在任何上下文中都是危险的——没有"合理使用 `eval`"的场景需要被模型判断。纯字符串匹配在这里是最优解：零成本 + 零误报 + 即时响应。

### 2.2 第二层：End-of-Turn 模型审查（背景运行的智能扫描）

一个 turn 结束后（用户发送消息 → Claude 工作并回复 → turn 结束），插件计算该 turn 中所有变更（包括 Claude 的编辑工具、Bash 命令和 Subagent）的 git diff，并将其发送给一个**独立的 Claude 实例**进行安全审查。这个审查在后台运行，不延迟 Claude 的回复。

第二层能捕获第一层无法检测的逻辑漏洞：授权绕过、不安全的直接对象引用、注入、SSRF、弱加密等。这些问题没有简单的字符串特征，需要理解代码上下文。

如果审查发现问题，Claude 会收到重新 prompt 并在下一次 turn 中处理这些问题。审查覆盖每个 turn 最多 30 个变更文件，连续触发最多 3 次后让出控制权交还给用户。

**关键设计**：Review 不阻塞写入，发现作为指令传达给编写代码的 Claude，由其自行决定是否修复。插件是一层防御深度，不是一个完整的解决方案。

### 2.3 第三层：Commit/Push 智能审查（最深度的上下文感知审查）

当 Claude 通过 Bash 工具执行 `git commit` 或 `git push` 时，插件运行最深层的 agentic 审查。这次审查不仅看 diff，还会读取周围的代码（包括调用方 sanitizer 和相关文件），以判断一个发现是否在当前代码库中真实存在而不是孤立出现的。

**设计洞察**：这个层级的审查解决了 pattern matching 和 end-of-turn review 的固有局限——某些模式在隔离看是危险的，但在具体代码库中可能是安全的。例如，`eval` 在处理已知格式的用户输入时可能是合理的。深层上下文感知使得误报率显著降低。

第三层只在 Claude 主动发起 commit 或 push 时触发，用户自己从 shell 发起的 commit（包括 session 内 `!` shell escape）不在审查范围内。Commit 和 push 审查每小时最多触发 20 次。

---

## 三、核心工程原则

### 3.1 评审独立性：自己不能审自己

> "The plugin does not ask the same Claude instance that wrote the code to grade itself."

这是整个设计的核心哲学。Per-edit 检查是纯字符串匹配，没有模型参与。End-of-turn 和 commit 审查使用独立的 Claude 调用和全新的上下文，配合安全专用的 prompt——审查模型从 diff 出发，不了解原始实现方案，因此没有"维护自己代码"的动机。

这与传统的"让模型自我反思安全性"有本质区别。自我反思的问题在于：模型在写代码时已经做出了决策，审查时会倾向于维护这个决策。而独立审查实例从空白上下文开始，只看代码，不看历史决策。

### 3.2 添加剂扩展：自定义规则体系

插件提供两个扩展点，均为添加剂（可添加，不能禁用内置规则）：

**`.claude/claude-security-guidance.md`**：为模型审查层添加项目特定的安全规范和威胁模型。这个文件在审查时作为额外上下文加载，与内置漏洞检查清单一起使用。例如：

```markdown
# Security guidance for this repo
- Do not log `customer_id` or `account_number` at INFO level or above.
- All routes under `/admin` must call `require_role("admin")` before any database read.
- Use `crypto.timingSafeEqual` for token comparison instead of `===`.
```

**`.claude/security-patterns.yaml`**：为第一层添加自定义正则或子串匹配规则：

```yaml
patterns:
  - rule_name: internal_api_key
    substrings: ["sk_live_", "AKIA"]
    reminder: "Hard-coded secrets must use environment variables."
```

### 3.3 与其他安全工具的分层配合

插件定位明确：**减少到达 PR 的安全问题**，Code Review 处理剩余部分。这个设计体现了"防御深度"的思想——越早发现越便宜修复：

```
Writing (plugin catches) → PR (Code Review catches) → CI (scanner catches) → Production
↑ 越早越便宜                                          越晚越贵 ↑
```

Plugin 不阻止写入，不替代 CI 扫描，也不替代专业的安全团队。它是开发过程中持续运行的安全网。

---

## 四、范式转移：从「人审」到「机审」

Security-Guidance Plugin 体现了一个重要的范式转移：

**传统模式（2025）**：安全审查依赖人类在关键节点的批准和 review。人类是安全策略的执行者。

**新模式（2026）**：安全审查成为 Agent 自身的内生能力。模型不仅写代码，还持续审查自己写的代码。

这个转移背后的驱动力：

1. **Approval fatigue**：当人类批准率高达 93% 时，HITL 实际上是失效的
2. **规模问题**：Agent 每小时生成的代码量远超人类 review 能力
3. **User-as-Injection-Vector**：Anthropic 红队演练证明，当攻击通过用户传递时，模型层防御完全失效

安全专家 Bruce Schneier 说过："Security is not a product, but a process"。Security-Guidance Plugin 的三层架构是这个观点的 AI Agent 版本：**安全不是一次审查，而是一个持续的过程**。

---

## 五、工程启示

| 维度 | 传统 HITL | Security-Guidance Plugin |
|------|----------|------------------------|
| **审查时机** | 每次操作前请求批准 | 编辑时、turn 结束时、commit 时 |
| **审查者** | 人类（疲劳、注意力分散）| 独立 Claude 实例（零成本/背景/深度）|
| **审查范围** | 人类能理解的操作 | 30文件 × 3轮次/turn |
| **误报处理** | 人类判断 | 上下文感知审查 |
| **扩展机制** | 人工配置 | YAML pattern + Markdown guidance |

这个插件的设计哲学值得所有构建 AI Coding 工具的团队参考：**与其让人类承担安全责任，不如让模型承担安全能力**。安全将成为 AI Agent 的内生属性，而不是外部约束。