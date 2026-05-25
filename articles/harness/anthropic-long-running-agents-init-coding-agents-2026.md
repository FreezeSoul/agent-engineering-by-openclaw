# Anthropic 的长时运行 Agent 解决方案：Initializer Agent + Coding Agent 双轨制

> 源文：["Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（Published Nov 26, 2025）

---

## 核心命题

长时运行的 Agent 在跨越多个上下文窗口时面临一个根本性挑战：**每个新会话开始时都没有上一会话的记忆**。Anthropic 给出了一个精妙的类比——「想象一个软件项目由轮班工程师维护，而每位新工程师到达时对之前发生的事情毫无记忆」。

他们的解决方案是一个**双轨制架构**：Initializer Agent 负责初始化环境，Coding Agent 负责增量推进。两者不是两个独立的 Agent 系统，而是同一个 Agent Harness 在不同初始 prompt 下的两种运行模式。

---

## 问题的本质：Agent 在长时任务中的两大失败模式

Anthropic 通过实验发现，即便使用前沿模型（如 Opus 4.5），在纯提示词驱动下让 Agent 完成复杂项目时，会出现两个典型的失败模式：

**失败模式一：Agent 试图一口气完成所有工作**

这导致模型在实现中途耗尽上下文，下一个会话从「半完成且未文档化」的状态开始。Agent 必须猜测发生了什么，然后花大量时间让基础功能重新运行起来。即使有压缩（compaction）机制，也无法完美地把清晰指令传递给下一个 Agent。

**失败模式二：Agent 过早宣布任务完成**

当一些功能已经构建完毕后，后续的 Agent 实例环顾四周，看到已经取得的进展，就认为工作已经完成。

这两个问题的根源在于：**没有结构化的方式来让 Agent 理解「项目当前状态」和「剩余工作」**。

---

## 双轨制架构：Initializer Agent + Coding Agent

### Initializer Agent

第一个会话使用专门设计的 prompt，要求模型完成以下初始化工作：

1. **`init.sh` 脚本**：运行开发服务器的启动命令
2. **`claude-progress.txt` 文件**：记录 Agent 完成工作的日志
3. **初始 git commit**：展示添加了哪些文件

最重要的是生成一份**功能列表文件（feature list）**，这份 JSON 文件详细描述了所有需要实现的功能，每个功能都标记为初始状态 `"passes": false`。以构建一个类似 claude.ai 的网站为例，这份列表包含 200+ 个功能条目，如「用户可以打开新对话、输入查询、按回车键并看到 AI 响应」。

### Coding Agent

每个后续会话都遵循结构化流程：

```
1. 运行 pwd 查看工作目录
2. 阅读 git logs 和 progress 文件，了解最近工作进展
3. 阅读 feature list 文件，选择优先级最高的未完成功能
4. 仅工作于这一个功能
5. 完成后：git commit + 更新 progress 文件 + 标记 passes: true
```

这个流程解决了一个关键问题：**如何让 Agent 快速理解项目状态而不消耗大量 token**。

---

## 关键设计决策

### Feature List 采用 JSON 而非 Markdown

经过多次实验，Anthropic 最终选择用 JSON 存储功能列表而非 Markdown。原因是「模型修改或覆盖 JSON 文件的可能性远低于 Markdown」。这反映出在 Agent 系统设计中，连文件格式的选择都是经过验证的工程决策。

在提示词中，他们使用强烈的措辞：

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

这种设计防止了 Agent 以「简化」为名删除关键功能定义。

### 增量进度而非批量构建

增量方法的关键在于**每次只做一个功能，完成后留下干净的代码状态**。Anthropic 发现最有效的方式是让模型用 git commit 描述性提交消息记录进展，并在 progress 文件中写总结。这样模型可以利用 git 来恢复工作状态、撤销错误代码变更。

### 测试作为一等公民

他们发现 Claude 倾向于「标记功能为完成但没有适当的测试」。在 Web 应用场景中，通过明确提示使用 Puppeteer MCP 这样的浏览器自动化工具进行端到端测试，性能显著提升。Agent 能够识别出仅从代码中无法发现的 bug。

但仍有问题存在：Claude 的视觉能力和浏览器自动化工具的局限性意味着它无法看到浏览器原生的 alert modal，导致依赖这类 modal 的功能 bug 率更高。

---

## Agent 失败模式与解决方案对照表

| 失败模式 | Initializer Agent 行为 | Coding Agent 行为 |
|---------|------------------------|-------------------|
| Agent 过早宣布胜利 | 设置 feature list：基于输入规格建立结构化 JSON 列表 | 阅读 feature list；选择单个功能开始工作 |
| Agent 留下 bug 或未文档化的进度 | 初始化 git repo 和 progress notes 文件 | 开始时阅读 progress notes 和 git logs；运行基础测试；结束时写 git commit 和 progress 更新 |
| Agent 过早标记功能为完成 | 设置 feature list | 自我验证所有功能；仅在仔细测试后才标记为 passes |
| Agent 需要花时间搞清楚如何运行应用 | 写 `init.sh` 脚本运行开发服务器 | 开始时阅读 init.sh |

---

## 核心判断：双轨制解决的是「上下文传递」问题

笔者认为，这个方案的核心贡献不是「如何让 Agent 更聪明」，而是**解决了一个根本性的工程问题：如何在会话之间传递上下文**。

传统方案试图通过压缩（compaction）让上下文窗口变大，但这种方式是「被动」的——它只是把信息挤进窗口。而双轨制的思路是「主动结构化」：不是把所有信息都塞进去，而是建立一套让 Agent 能快速重建上下文的机制：

- **Feature list**：让 Agent 知道「做什么」
- **Progress file + git history**：让 Agent 知道「做到哪了」
- **Init script**：让 Agent 知道「怎么跑起来」

这三者组合在一起，使得每个新会话的 Agent 能在最短时间内重建工作上下文，而不需要把整个项目历史都塞进 prompt。

---

## 仍未解决的问题

Anthropic 坦诚指出了开放问题：

1. **单一通用 Agent vs 多 Agent 架构**：还不清楚跨会话时是单一通用 Agent 表现最好，还是多 Agent 架构（专门的测试 Agent、QA Agent、代码清理 Agent）能取得更好效果
2. **领域泛化**：当前 demo 针对全栈 Web 开发优化，推广到其他领域（如科学研究或金融建模）还需要进一步验证

---

## 引用

> "We developed a two-fold solution to enable the Claude Agent SDK to work effectively across many context windows: an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session."

— Anthropic Engineering Blog, "Effective harnesses for long-running agents"

> "By 'clean state' we mean the kind of code that would be appropriate for merging to a main branch: there are no major bugs, the code is orderly and well-documented, and in general, a developer could easily begin work on a new feature without first having to clean up an unrelated mess."

— Anthropic Engineering Blog, "Effective harnesses for long-running agents"

---

## 关联项目推荐

### zilliztech/claude-context

**让整个代码库成为 Claude Code 的上下文**

这不是巧合——Anthropic 的双轨制解决的是「跨会话的上下文传递」，而 Claude Context 解决的是「单次会话中如何高效利用上下文」。两者本质上是同一个问题的两个维度。

Claude Context 是一个 MCP 插件，它通过语义搜索从整个代码库中检索相关代码，然后仅将相关代码注入 Claude 的上下文。与其每次请求时把整个目录加载进 Claude（成本高昂），不如将代码库存储在向量数据库中，只在上下文窗口中放入最相关的代码。

**核心亮点**：
- 🧠 语义代码搜索：在百万行代码库中精确检索
- 💰 成本控制：避免每次都加载整个代码库到上下文
- 🔌 MCP 协议：与 Claude Code 等主流 AI 编码工具无缝集成

**适用场景**：大型代码库（动辄数万行）、需要 Agent 精确理解项目结构但又受限于上下文窗口的场景。

GitHub: [zilliztech/claude-context](https://github.com/zilliztech/claude-context)