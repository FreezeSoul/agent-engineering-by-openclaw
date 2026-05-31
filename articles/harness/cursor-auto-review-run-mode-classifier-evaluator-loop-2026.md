# Cursor Auto-review Run Mode：让分类器在 Agent 决策里扮演评估器角色

> **核心命题**：Cursor 3.6 的 Auto-review Run Mode 用一个 LLM 分类器子 Agent 替代传统的规则式权限判断，本质上是在 Agent 执行路径上插入了 Anthropic 工程师所说的「评估器循环」——让模型自己判断下一步操作是否安全、是否应该换一种方式尝试。

---

## 一、问题：权限系统的两极困境

在 Cursor 3.6 之前，Cursor Agent 的权限控制只有两种模式：

| 模式 | 行为 | 问题 |
|------|------|------|
| **Allowlist** | 只有白名单内的命令自动执行，其余全部弹窗审批 | 长任务中审批频繁，打断工作流 |
| **Run Everything** | 所有操作无脑自动执行 | 危险操作直接放行，无安全网 |

这不是 Cursor 一家的问题。几乎所有 AI Coding Agent 的权限系统都面临同样的设计张力：**要么过度限制导致可用性崩溃，要么过度开放导致安全崩塌**。

Auto-review 的出现，填补了这两个极端之间的空白。

---

## 二、Auto-review 的三层决策架构

Auto-review Run Mode 不再是「允许/拒绝」的二元判断，而是一套**分层决策链**：

```
工具调用发起
    │
    ├─ 命中 Allowlist？ ──→ [立即执行，无任何阻碍]
    │
    ├─ 可被沙箱化？ ──→ [在沙箱中执行，隔离危险操作]
    │
    └─ 其他所有情况 ──→ [送入 Classifier Sub-agent]
                              │
                              ├─ allow ──→ 执行
                              ├─ block ──→ 停止，询问用户
                              └─ retry ──→ 换一种方式重试
```

**三个关键点**：

1. **Allowlist 先行**：高频安全操作（`git`、`npm install` 等）直接放行，不走分类器，避免不必要的性能损耗
2. **Sandbox 次之**：无法直接放行但可沙箱化的操作（Shell 命令、网络请求等）在隔离环境中执行，即使出问题也有边界
3. **Classifier Sub-agent 兜底**：既不在白名单、也无法沙箱化的操作，送入 LLM 分类器判断——这是整个机制的核心创新点

### Classifier Sub-agent 的本质

分类器是一个**独立的 LLM 子 Agent**，它的职责不是执行任务，而是**评估其他 Agent 的操作意图和安全性**。

引用 Cursor 官方文档原文：

> *"All other agent actions go to a classifier subagent that decides whether to allow the call, try a different approach, or ask for your approval. The classifier isn't deterministic and isn't a guarantee, so it can make mistakes."*

这个描述直接揭示了分类器的本质：**它是一个 evaluator（评估器），不是规则引擎**。它的判断是概率性的，会犯错，因此需要配合其他安全层（Sandbox、Allowlist）构建纵深防御。

---

## 三、工程机制分析：这就是「评估器循环」

Auto-review 的三层架构，精确对应了 Anthropic 在《Harness design for long-running application development》中描述的 **Harness Engineering** 核心模式：

### 评估器循环（Evaluator Loop）

Anthropic 将「评估器循环」定义为让 Agent 能够长时间稳定工作的关键工程机制：

> *"The harness is the scaffolding that keeps the agent on track — evaluating each step, deciding when to stop or continue, managing the boundary between agent autonomy and human oversight."*

Cursor 的 Auto-review 正是这一模式的产品化实现：

| Harness 机制 | Anthropic 描述 | Cursor Auto-review 实现 |
|---------------|----------------|------------------------|
| **Stop Condition** | 评估当前操作是否应停止 | Classifier 返回 block 时停止 |
| **Keep Working Until Done** | Agent 自主判断是否继续 | Classifier 返回 retry 时换方式重试 |
| **Handoff** | 决策权转移 | Classifier 无法判断时询问用户 |
| **Permission Layering** | 权限分层隔离 | Allowlist → Sandbox → Classifier 三层 |

### 与 Claude Code Auto Mode 的对比

Claude Code 的 Auto Mode 通过「分类器」判断是否需要弹窗审批，Cursor 的 Auto-review 通过「分类器」判断是否执行——**两者都把分类器引入了权限决策链**，但切入点不同：

| 实现 | 触发场景 | 分类器决策结果 |
|------|---------|--------------|
| **Claude Code Auto Mode** | 权限边界模糊时 | 跳过弹窗 → 直接执行，或保持阻止 |
| **Cursor Auto-review** | 所有非白名单、非沙箱操作 | allow / block / retry，换一种方式 |

Cursor 的 retry 机制是一个值得注意的差异点：分类器不仅可以说「允许」或「阻止」，还可以说「换一种方式试试」。这意味着 **Classifier Sub-agent 具备一定的任务理解能力**，能够判断当前失败的操作是否有替代路径。

---

## 四、Sandbox 作为纵深防御层

Auto-review 的另一层设计亮点是 **Sandbox 的主动介入**：即使分类器批准了某个操作，如果该操作可以被沙箱化，它仍然会在隔离环境中执行。

这是典型的 **纵深防御（Defense in Depth）** 思维——Classifier 不是唯一的安全层，每个层级都有独立的安全判断。

Cursor 官方文档明确列出了沙箱的访问控制策略：

| 访问类型 | 行为 |
|----------|------|
| **文件访问** | 只读；工作区目录可读写 |
| **网络访问** | 默认阻止，可配置 |
| **临时文件** | 完整访问 `/tmp/` |

沙箱通过 Linux Landlock（Kernel 6.2+）和 macOS Seatbelt 实现，与 Agent 的权限判断完全正交——即使 Classifier 说「allow」，沙箱也会在执行时强制执行边界。

---

## 五、Custom Instructions：可操控的评估器

Cursor 的另一个工程细节是 **允许用户通过自定义指令引导分类器行为**：

> *"You can also steer the classifier agent by giving it custom instructions."*

这意味着评估器不是黑箱，用户可以向它注入策略意图。例如：

- 「不要批准任何涉及外部网络 API 的操作」
- 「对文件写入操作格外谨慎，优先让用户确认」
- 「对测试相关的 Shell 命令放宽，对部署命令收紧」

这是一个重要的工程信号：**Harness 的评估器应该是可配置的，而不是一成不变的规则集**。Anthropic 在多篇文章中强调 harness 应该「可观测、可调试、可干预」，Cursor 的 custom instructions 正是这一原则的实现。

---

## 六、/loop Skill：Keep Working Until Done 的本地实现

与 Auto-review 同版本发布的 `/loop` Skill 值得关注。它让 Cursor 可以：

> *"run a prompt repeatedly on a local schedule, until a certain outcome is achieved, or until you stop it. If you don't specify a fixed interval, the agent decides when or what event should wake it."*

/loop 是 Harness Engineering 中「**Keep Working Until Done**」模式的直接体现——设置一个目标，让 Agent 自主决定何时重试、间隔多久、什么时候算完成。

结合 Auto-review 的三层权限架构，本地长任务现在有了完整的安全网：

```
长任务启动（/loop）
    │
    ├─ 每次 Agent 操作 → Auto-review 三层判断
    │       ├─ Allowlist → 直接执行
    │       ├─ Sandbox → 隔离执行
    │       └─ Classifier → allow/block/retry
    │
    └─ 任务结束条件 → Agent 自主判断（/loop 语义）
```

---

## 七、笔者判断：评估器循环的工程化落地

Cursor Auto-review 最有价值的地方，不是某个具体的安全特性，而是它把 **Anthropic 论文里的 Harness 概念变成了普通用户可以配置的产品功能**。

回顾 Agent 工程化的演进路径：

| 阶段 | 核心问题 | 解决方案 |
|------|---------|----------|
| 1. 权限系统 | 全部阻止 or 全部放行 | 白名单机制 |
| 2. 半自动 | 需要频繁审批 | Auto-skip 权限（Claude Code） |
| 3. 智能权限 | 二元判断不够精细 | **Classifier-based Evaluator Loop（Cursor Auto-review）** |

Auto-review 的 Classifier Sub-agent 解决了「需要人判断的操作是否真的危险」这个问题——由模型自己判断，而不是用户预定义的规则。这与 Manus 的「Agent 直接执行、评估器事后复盘」模式异曲同工，都是把「判断权」交给了一个独立于执行路径的评估机制。

**局限性值得注意**：Cursor 文档明确说「The classifier isn't deterministic and isn't a guarantee, so it can make mistakes」——概率性判断意味着这个系统不是零失误的安全屏障，而是把「人必须介入的决策」转移到了模型端，本质上是把错误从「打断用户」变成了「模型判断失误」。哪种更好，取决于具体场景。

---

> **引用来源**
> - [Auto-review Run Mode - Cursor Changelog](https://www.cursor.com/changelog/auto-review)
> - [Terminal & Run Mode - Cursor Docs](https://cursor.com/docs/agent/tools/terminal#run-mode)
> - [Shared Canvases and /loop Skill - Cursor Changelog](https://www.cursor.com/changelog/shared-canvases)
> - [Harness design for long-running application development - Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)