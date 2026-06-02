# Agent 自我演进的核心工程障碍：Harness 工程，而不是编排

> 2026年2月，Anthropic 的 Nicholas Carlini 用 16 个 Claude 实例并行工作，近 2000 次 Claude Code 会话、$20,000 的 API 成本，最终产出 100,000 行 Rust C 编译器，能编译 Linux 6.9。
>
> 这个实验的真正发现不是那个编译器，而是**让 Agent 团队长时间自主工作所需的工程机制**——这些机制与「多 Agent 编排框架」几乎无关。

---

## 一、问题的本质：框架不是瓶颈，Harness 才是

社区讨论多 Agent 时，往往把焦点放在「用哪个框架」（CrewAI？LangGraph？AutoGen？），仿佛只要选对了编排层，Agent 就能自主完成复杂长时任务。

Carlini 的实验彻底颠覆了这个假设。他的实现没有使用任何现成的多 Agent 框架：

> "This is a very early research prototype. I haven't yet implemented any other method for communication between agents, nor do I enforce any process for managing high-level goals. I don't use an orchestration agent."
>
> 代わりに、各 Claude agent はどう行動するかを自分で決める。ほとんどの場合、Claude は「次に最も明白な」問題を選ぶ。

真正阻碍自主运行的，是 **Harness 工程**——即围绕 Agent 运行环境的设计，包括：

- **接力循环**：任务完成后如何自动接上下一个任务，而不需要人工介入
- **工作区状态管理**：如何让 Agent 在干净上下文中快速定位并推进
- **测试验证设计**：如何用高质量的测试套件引导 Agent 保持在正确方向上
- **并行同步机制**：多个 Agent 同时工作时的冲突解决策略

这四个维度，在现有编排框架的文档和最佳实践中，几乎找不到系统性的讨论。

---

## 二、接力循环：让 Agent 持续工作的引擎

现有 Agent 框架（如 Claude Code）依赖人工操作员在线监督。当任务复杂需要长时间运行时，人工介入就变成了硬性瓶颈。

Carlini 的解法是一个 bash 循环：

```bash
while true; do
  COMMIT=$(git rev-parse --short=6 HEAD)
  LOGFILE="agent_logs/agent_${COMMIT}.log"

  claude --dangerously-skip-permissions \
    -p "$(cat AGENT_PROMPT.md)" \
    --model claude-opus-X-Y &> "$LOGFILE"
done
```

这个循环的精妙之处在于它的**极简主义**——不再依赖复杂的任务队列或状态机，只需要一个原则：「完成当前任务后，立即挑选下一个」。

但这引入了一个核心问题：**Agent 怎么知道下一个任务是什么？**

答案不在循环本身，而在任务设计。如果任务定义模糊，Agent 会在第一次循环结束后陷入「不知道做什么」的困境。Carlini 的解决方案是让 Agent 在 AGENT_PROMPT.md 中明确被告知：

1. 将问题分解成小碎片
2. 持续追踪自己在做什么
3. 主动判断下一个要解决的问题
4. 持续到完美——因为循环不会停止

这本质上是一个**自愈型任务分发机制**，不需要中心化的调度器。

---

## 三、Git 原生同步：去中心化的冲突解决

多 Agent 并行最大的工程挑战是冲突：当多个 Agent 同时尝试修改同一份代码时，如何防止相互覆盖？

Carlini 的方案极度优雅——用 Git 作为同步基础设施：

1. **锁机制**：Agent 通过在 `current_tasks/` 目录下创建文件来「锁定」任务（如 `parse_if_statement.txt`）
2. **冲突检测**：如果两个 Agent 同时尝试锁定同一个任务，Git 的同步机制强制第二个 Agent 放弃并选择其他任务
3. **提交推送**：Agent 完成工作后 pull upstream、merge 其他人的变化、push 自己的变化、删除锁文件

> "Merge conflicts are frequent, but Claude is smart enough to figure that out."

这个方案的聪明之处在于**完全去中心化**——不需要消息队列、不需要分布式锁服务，只需要一个 bare git repo。所有 Agent 通过对同一个 upstream repo 的 push/pull 来协调。

这给我们的启发是：**Git 不只是代码仓库，它是天然的分布式工作协调协议**。

---

## 四、测试即 harness：验证器决定 Agent 的方向

Carlini 在论文中反复强调的一个教训是：

> "Claude will work autonomously to solve whatever problem I gave it. So it's important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."

这揭示了一个反直觉的事实：**Harness 的核心不是执行流程，而是验证机制**。

具体来说，他发现了几个关键的测试设计原则：

### 4.1 测试必须精确：错误即错误，不要模糊

当测试套件有哪怕 1% 的 false positive rate，Agent 会在某个随机任务上浪费数小时调试一个「不是 bug 的 bug」。高质量的编译器测试套件（GCC torture test suite）是这个项目能成功的关键前提。

### 4.2 测试输出必须机器可读

日志文件的格式直接影响 Agent 的上下文负担：

> "Logfiles should be easy to process automatically: if there are errors, Claude should write ERROR and put the reason on the same line so grep will find it."

这是一个典型的**上下文工程**实践——不是给人类设计日志格式，而是给语言模型设计。

### 4.3 增量采样避免上下文污染

当测试套件很大时，每次运行完整测试会严重污染 Agent 的上下文窗口。Carlini 的方案是提供一个 `--fast` 选项，运行 1% 或 10% 的随机采样，且采样对每个 Agent 是确定性的（可复现），但跨 VM 是随机的（覆盖均匀）。

---

## 五、多角色专业化：超越「万能 Agent」

当项目达到一定规模后，「一个 Agent 做所有事」的瓶颈变得明显。Carlini 引入了一个关键变化：**专业化 Agent 角色**。

在他的项目中，不同 Agent 被分配了不同职责：

| Agent 角色 | 职责 |
|-----------|------|
| **问题解决 Agent** | 主要的编码任务 |
| **去重 Agent** | 合并重复代码实现 |
| **性能 Agent** | 改进编译器自身的性能 |
| **代码质量 Agent** | 从 Rust 专家视角评审结构 |
| **文档 Agent** | 维护 README 和进度文件 |

这个设计的核心洞察是：**专业化让 Agent 的上下文窗口更高效**——每个 Agent 只需要知道它负责的子域，而不需要理解整个项目的所有细节。

---

## 六、这个发现对我们意味着什么

Carlini 的实验证明了三件事：

**第一，框架不是壁垒。** 你可以用最原始的 bash 循环 + git 完成多 Agent 协作，真正的难度在于 harness 设计。

**第二，测试是第一公民的工程机制。** 在传统软件开发中，测试是质量保障手段；在 Agent 工程中，测试是 **harness 的核心组件**，直接决定了 Agent 的行为方向。

**第三，去中心化协调优于中心化调度。** Git 原生同步方案的优势在于它的简单性和天然的一致性保证——不需要引入额外的协调服务。

---

## 七、工程机制清单：让 Agent 团队自主工作的最小集

基于 Carlini 的实践，以下是让多 Agent 团队长时间自主工作的核心工程机制：

| 机制 | 关键设计 | 反模式 |
|------|---------|--------|
| **接力循环** | 任务完成后自动获取下一个，依赖任务定义质量 | 等待人工指派下一个任务 |
| **Git 原生同步** | 用文件锁 + push/pull 处理并行冲突 | 中心化任务队列或锁服务 |
| **验证器优先** | 测试套件必须精确且机器可读，先于 Agent 开发测试 | 测试质量低下或依赖人工解释结果 |
| **上下文隔离** | 每个 Agent 独立 Docker 容器，干净启动 | Agent 间共享状态导致相互污染 |
| **角色专业化** | 不同 Agent 负责不同子域，减少上下文负担 | 一个 Agent 试图理解并做所有事 |
| **日志机器可读** | ERROR/INFO 格式，可 grep，重要信息入文件而非 stdout | 给人类设计的长篇日志格式 |

---

**引用来源**：

- [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) — Anthropic Engineering Blog，Nicholas Carlini，2026年2月5日
- [claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler) — GitHub 仓库