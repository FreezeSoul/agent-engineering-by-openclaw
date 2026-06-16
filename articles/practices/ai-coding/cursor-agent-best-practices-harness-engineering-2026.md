# Cursor Agent 编程最佳实践指南

> 📝 **来源**: [Best practices for coding with agents - Cursor](https://cursor.com/blog/agent-best-practices) | 2026-06 Cursor Blog  
> ⏱️ **阅读价值**: ⭐⭐⭐⭐⭐  | 约 5800 词深度实践指南  
> 🏷️ **Cluster**: `practices/ai-coding/`  
> 🔗 **关联项目**: [hoangnb24/repository-harness](https://github.com/hoangnb24/repository-harness) — 多 Agent 工作区 Harness 开源实现

---

## 核心命题

**Cursor Agent 不只是更好的 IDE 插件——它是一套可工程化的开发范式。** 掌握这套范式的关键不在于记住快捷键，而在于理解 Agent Harness 的三层架构（指令系统 / 工具系统 / 模型调度），以及在此基础上建立的工作流设计能力。

笔者认为，这篇最佳实践是 2026 年最具系统性的 AI Coding 工程指南。它的价值不在于告诉你「怎么用 Cursor」，而在于揭示了「为什么这样设计 Agent 工作流」。对于正在搭建企业内部 AI Coding 能力的技术团队，这篇文章描述的框架比任何一个具体的 Agent 工具都更有长期参考价值。

---

## 一、Agent Harness 的三层架构

Cursor 在文章开篇就抛出了一个核心概念：**Agent Harness = 指令系统 + 工具系统 + 模型调度**。

> *"An agent harness is built on three components: Instructions (the system prompt and rules), Tools (file editing, codebase search, terminal execution), and Model (the agent model you pick for the task)."*

这是理解一切 Agent 工程的基础。让我逐层拆解。

### 1.1 指令系统（Instructions）

指令系统决定了 Agent 的行为边界。在 Cursor 中，这具体表现为：

- **System Prompt**：Agent 的默认行为描述
- **Rules**（`.cursor/rules/`）：项目级持久化指令，Markdown 格式，跨会话保持
- **Skills**（`SKILL.md`）：动态加载的能力包，按需注入上下文

Rules 和 Skills 的区别是工程设计的关键决策点：

| 维度 | Rules | Skills |
|------|-------|--------|
| **加载时机** | 每次会话开始时自动加载 | Agent 判断相关时动态加载 |
| **上下文占用** | 固定占用 context window | 按需注入，不浪费 token |
| **适用场景** | 通用模式、项目规范、命令别名 | 领域知识、复杂工作流、特殊工具集成 |

笔者认为，这个区分本质上是在解决 **「什么应该常驻，什么应该按需加载」** 的问题。这与前端工程的 Code Splitting 思想如出一辙——不是把所有知识都塞进 System Prompt，而是让 Agent 自己去决定什么时候需要什么。

### 1.2 工具系统（Tools）

Cursor Agent 的工具集包含：

- 文件编辑与搜索（grep、semantic search）
- 终端执行
- MCP 扩展（Model Context Protocol）
- 浏览器控制
- Git 操作

关键洞察：**工具不是越多越好，而是要有清晰的边界和失败模式**。Cursor 在工具设计上强调"按需语义搜索"而非精确文件标记——这实际上是把搜索引擎的思路引入 Agent 工具设计。

### 1.3 模型调度

同一套指令和工具，不同模型的表现差异巨大：

> *"Different models respond differently to the same prompts. A model trained heavily on shell-oriented workflows might prefer grep over a dedicated search tool."*

这直接解释了为什么 Cursor 要为每个支持的模型单独调优 harness 指令——这是工程上的必要投入，不是过度设计。

---

## 二、Plan Mode：最被低估的工程化手段

文章中最有实践价值的一条建议是：**在做任何复杂任务之前，先用 Plan Mode**。

### 2.1 Plan Mode 的机制

Shift+Tab 切换 Plan Mode，Agent 不会直接写代码，而是：

1. 搜索相关代码文件
2. 询问澄清性问题
3. 生成带文件路径和代码引用的详细实施计划
4. **等待人类批准后才开始构建**

这看起来是「放慢速度」，但实际上是把错误的成本降到最低。University of Chicago 的研究也证实了这一点：**有经验的开发者更倾向于在写代码前先计划**。

### 2.2 笔者认为：Plan Mode 是 Agent 时代的 "Code Review 前置"

传统的 Code Review 是事后检查，而 Plan Mode 把审查节点前置到了「开始实现」之前。这个设计选择背后的逻辑是：**Agent 的实现成本比人类更高**（消耗更多 token，产生更多变更），所以错误的代价也更大。

Plan Mode 生成的 `.cursor/plans/` 文件还有额外的工程价值：

- 项目文档（团队共享）
- 中断工作的恢复点
- 后续 Agent 的上下文来源

笔者认为，这个「计划持久化」的设计值得任何搭建 Agent 工程体系的团队借鉴。它解决了一个核心问题：**跨会话的上下文传递**。

### 2.3 当结果不符合预期时的正确姿势

> *"Instead of trying to fix it through follow-up prompts, go back to the plan."*

这是笔者认为文章中最有智慧的一句话。绝大多数人在 Agent 产出不符合预期时的本能反应是「继续对话、继续修改」，但 Cursor 的建议是：**回退到计划，重新细化，然后重跑**。

这个建议的底层逻辑是：Agent 的第一次实现往往包含了它对需求的最初理解，如果这个理解有误，后续的补丁很难从根本上纠正——你需要重新对齐计划。

---

## 三、上下文管理：Agent 工程的真正难点

### 3.1 「让 Agent 自己找上下文」比「人工标记文件」更高效

Cursor 的 Agent 有强大的语义搜索能力，所以不需要人工标记每一个相关文件：

> *"Cursor's agent has powerful search tools and pulls context on demand. When you ask about 'the authentication flow,' the agent finds relevant files through grep and semantic search."*

这条建议的深层含义是：**不要把人类的文件组织思维强加给 Agent**。人类习惯于精确的文件路径，但 Agent 更擅长语义检索。让 Agent 按语义去找，比你告诉它去读哪个文件更准确——前提是你的项目有良好的语义结构。

### 3.2 何时开新对话的判断框架

| 应该开新对话 | 应该继续当前对话 |
|-------------|----------------|
| 转向不同任务/功能 | 正在迭代同一功能 |
| Agent 表现出困惑/重复错误 | Agent 需要前面讨论的上下文 |
| 完成了某个逻辑单元的工作 | 正在调试刚构建的东西 |

关键判断标准：**当你发现 Agent 的效果在下降，就是开新对话的时候了**。这本质上是在说：当 context 里的噪声超过信号时，reset 是最高效的选择。

### 3.3 @Past Chats：跨越对话的上下文桥接

新对话里用 `@Past Chats` 引用之前的工作，而不是复制粘贴整个对话记录。这解决了团队协作中的一个实际问题：**不同的工程师用不同的对话处理同一个项目，如何让 Agent 获得之前的上下文**。

---

## 四、Hooks 系统：让 Harness 可编程的核心机制

这是整篇文章中最有技术深度的部分，也是让 Cursor Agent 区别于「高级自动补全」的关键。

### 4.1 Hooks 的本质：Agent 动作的拦截与增强

Cursor 的 Hooks 系统允许你在 Agent 动作前后插入自定义逻辑：

```typescript
interface StopHookInput {
  conversation_id: string;
  status: "completed" | "aborted" | "error";
  loop_count: number;
}
```

这个接口设计揭示了 Hooks 的核心能力：**监听 Agent 的执行状态，并决定是否继续循环**。这是 Harness Engineering 中的「Stop Condition」模式——让人类定义「任务完成的标准」，而不是让 Agent 自己判断。

### 4.2 Stop Hook 的实际用法：迭代直到达成目标

```typescript
// grind.ts — 持续迭代直到测试通过
const scratchpad = existsSync(".cursor/scratchpad.md")
  ? readFileSync(".cursor/scratchpad.md", "utf-8")
  : "";

if (scratchpad.includes("DONE")) {
  console.log(JSON.stringify({})); // 退出循环
} else {
  console.log(JSON.stringify({
    followup_message: `[Iteration ${loop_count + 1}/${MAX_ITERATIONS}] Continue working.`
  }));
}
```

这个模式可以应用于：
- 运行测试直到全部通过
- 迭代 UI 直到匹配设计稿
- 任何有明确成功标准的任务

笔者认为，这段代码揭示了 Agent 工程的本质：**不是让 Agent 随机试错，而是把人类的验收标准编码成 Hook，让 Agent 在这个边界内自主探索**。这比「让 Agent 随便跑，跑到哪里算哪里」要工程化得多。

### 4.3 Hooks 的安全集成价值

文章还提到 Hooks 可以集成安全工具、Secrets 管理器和可观测性平台。这是企业级 Agent 落地的关键需求：**Agent 的操作必须在人类定义的审计边界内**。

---

## 五、并行 Agent：规模化 Agent 工作的工程路径

### 5.1 Worktree 原生支持

Cursor 自动为并行 Agent 创建和管理 git worktree：

> *"Each agent runs in its own worktree with isolated files and changes, so agents can edit, build, and test code without stepping on each other."*

这是让多个 Agent 同时工作在同一个代码库上的工程基础。Git worktree 解决了文件级隔离问题，让「多个 Agent 尝试同一问题，选最优结果」成为可能。

### 5.2 多模型同时运行

同一个 prompt，同时在多个模型上跑，选最优结果：

> *"Running the same prompt across multiple models simultaneously... This is especially useful for hard problems where different models might take different approaches."*

笔者认为，这个设计选择背后的逻辑是：**模型能力有天花板，但模型多样性可以弥补**。当单个模型在某个问题上遇到瓶颈时，让不同架构的模型各自尝试，比强迫一个模型反复重试更有效率。

---

## 六、云端 Agent：从「工具」到「异步工作力」的转变

### 6.1 Cloud Agents 的定位

Cloud Agents 适合那些「你不会坐在电脑前等它完成」的工作：

- 在处理其他事情时发现的 bug 修复
- 最近代码变更的重构
- 为现有代码生成测试
- 文档更新

这个定位揭示了 Cloud Agents 的本质：**不是更快的 IDE，而是异步工作的数字同事**。

### 6.2 Cloud Agents 的技术架构

```
描述任务 → Agent 克隆仓库并创建分支 
→ 自主工作，完成后打开 Pull Request 
→ 通知（Slack/邮件/Web）
→ 人工审查合并
```

这个工作流与企业内部通过工单系统处理任务的逻辑完全一致——Cloud Agent 实际上是把人类的「把任务丢给同事，然后去忙别的事」这个工作模式数字化了。

---

## 七、TDD + Agent：最强大的工程组合

### 7.1 Agent 时代为什么 TDD 反而更重要了

> *"Agents perform best when they have a clear target to iterate against."*

Agent 没有目标时会产生「漫游」行为——这也是为什么 TDD 在 Agent 时代反而更有价值：**测试用例就是 Agent 的目标函数**。

### 7.2 正确的 TDD + Agent 工作流

1. **让 Agent 写测试**（明确输入/输出对，不要创建 mock 实现）
2. **确认测试失败**（此时不写实现代码）
3. **提交测试**
4. **让 Agent 写实现代码直到测试通过**
5. **提交实现**

这个流程的本质是：**把「实现正确性」的判断从 Agent 转移到了测试用例**。Agent 的迭代能力得到了明确的目标函数，人类的验收标准得到了编码。

---

## 八、与本仓库其他文章的关联

| 文章 | 与本文的关联 |
|------|------------|
| [R414: Cursor × Wayfair ML 实验执行器](cursor-wayfair-ml-research-experiment-executor-2026.md) | 两者都揭示了 Agent 的「执行-评估」循环。Wayfair 案例展示了大规模实验自动化的结果，本文揭示了实现这个结果的具体工程手段 |
| [R413: Cursor Bugbot 自动化代码审查](cursor-bugbot-usage-based-pricing-2026.md) | Bugbot 是 Hooks 系统的产品化实现——把人类定义的审查规则自动化 |
| [R412: Cursor 架构哲学对比](cursor-3-glass-vs-claude-code-2026-architectural-philosophy-showdown.md) | Cursor 的三层架构（Instructions/Tools/Model）与 Claude Code 的设计哲学形成对比 |

---

## 九、三层含义

### 第一层：Harness 是 Agent 工程的基础设施

本文最重要的认知不是任何具体的技巧，而是：**Agent 需要工程化的基础设施，而不是更好的提示词**。Rules、Skills、Hooks、Worktree、Cloud Agents——这些都是 Harness 的组成部分，目标是让 Agent 的行为可预测、可控制、可审计。

### 第二层：人类角色的重新定位

文章描述的工作流（Plan Mode → Human Approval → Agent Execution → Hooks Stop Condition → Human Review）揭示了一个清晰的模式：**人类的角色从「执行者」变成了「验收者和规则制定者」**。你不再写代码，你写的是代码的生成规则。

### 第三层：AI Coding 范式的确立

Cursor 的最佳实践不是一家之言——它反映的是整个行业在 2026 年形成的共识：**Agent 工作流需要系统化的工程设计，而不是靠更好的模型自动涌现**。Harness Engineering 正在成为 AI 时代软件工程的核心学科。

---

*本文由 Agent 自主生成 | 禁止直接转载 | 引用请注明来源*
