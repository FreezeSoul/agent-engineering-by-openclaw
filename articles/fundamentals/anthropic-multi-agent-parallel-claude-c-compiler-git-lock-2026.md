# Anthropic 的多 Agent 并行实验：从零构建 10 万行 C 编译器的工程启示

> 原文：["Building a C compiler with a team of parallel Claudes"](https://www.anthropic.com/engineering/building-c-compiler)，Nick Carlini，Anthropic Safeguards 团队，2026-02-05

---

## 核心命题

Anthropic 用 16 个 Claude Agent 并行协作，从零构建了一个能编译 Linux kernel 的 Rust C 编译器（100,000 行代码），总成本 $20,000，近 2,000 次 Claude Code 会话，全程无人干预。这个实验回答了一个关键问题：**当 Agent 能够自主协作时，LLM 能完成多复杂的系统工程？**

---

## 一、为什么做这个实验

单个 Claude Code session 有根本性的限制：它一次只能做一个任务，且需要人类持续参与才能维持长期运转。当任务范围扩展到编译器这类复杂系统工程时，单个 Agent 很容易陷入局部问题无法自拔。

Carlini 的动机非常明确：这是一个**能力边界测试**。不是要证明 Agent 能替代人类程序员，而是要找到「当前模型勉强能完成」的任务边界，为下一代模型做准备。

> "I've been using the C Compiler project as a capability benchmark. I am interested in stress-testing the limits of what LLMs can just barely achieve today."

关键数据点：
- **Opus 4.5** 是第一个能产出功能性编译器的版本，但仍然无法编译任何真实大型项目
- **Opus 4.6** 在这个测试中跨越了新的阈值：能够完成 100K 行级别的真实系统工程

---

## 二、Agent Team 的核心架构

### 2.1 无限循环 Harness

Anthropic 的 Agent Team 本质上是一个无限循环：

```bash
while true; do
  COMMIT=$(git rev-parse --short=6 HEAD)
  LOGFILE="agent_logs/agent_${COMMIT}.log"
  claude --dangerously-skip-permissions \
    -p "$(cat AGENT_PROMPT.md)" \
    --model claude-opus-X-Y &> "$LOGFILE"
done
```

这个 loop 解决的是「Agent 如何持续运转」的问题：每次 Claude 完成一个任务，立即 pick up 下一个。没有人类介入，没有外部信号，Agent 自己决定下一步做什么。

### 2.2 Git 锁同步机制

并行多个 Agent 的核心问题是如何防止冲突（两个 Agent 同时改同一个文件）。Anthropic 的解法异常简洁：

> "Claude takes a 'lock' on a task by writing a text file to `current_tasks/`"

具体流程：
1. Agent 在 `current_tasks/` 目录写入锁文件（如 `parse_if_statement.txt`）来声明任务
2. 两个 Agent 如果同时争抢同一个任务，git 的同步机制强制后者 pick a different one
3. Agent 完成工作 → pull upstream → merge other agents' changes → push → remove lock
4. 冲突频繁，但 Claude 足够聪明能自己解决 merge conflict

这套机制的本质是**用文件系统作为协调层**，不依赖任何中心化的调度器或消息队列。

### 2.3 并行 Docker 容器

每个 Agent 运行在独立的 Docker container 中，共享同一个 bare git repo（挂载到 `/upstream`）。Agent clone 到本地 `/workspace`，完成后 push 回 upstream。容器隔离 + git 同步 = 最简并行架构。

---

## 三、质量保障：让 Agent 保持正确方向

无限循环的 Agent 有一个致命弱点：**如果任务验证机制不完美，Agent 会解决错误的问题**，而且因为没有人类纠正，它会一直错下去。

Carlini 花了大量精力构建测试 harness：

### 3.1 接近完美的测试

> "It's important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."

对于编译器这类复杂系统，测试需要覆盖：
- 标准测试套件（compiletest 等）
- 开源软件包的 build scripts
- 增量 regression 检测

每个测试必须足够精确，能区分「正确的解决方案」和「恰好通过测试但逻辑错误的代码」。

### 3.2 CI 管道防止退化

在项目后期，Claude 开始频繁破坏已有功能来换取新 feature 的实现。为了解决这个问题，Carlini 构建了 CI pipeline 并实现了更严格的 enforcement，确保 new commits can't break existing code。

---

## 四、并行化的关键策略

### 4.1 任务级别的并行

当测试套件有数百个独立测试时，每个 Agent pick 一个不同的失败测试，天然并行。但当任务变成「编译 Linux kernel」这类单一巨大任务时，16 个 Agent 会全部卡在同一个 bug 上。

### 4.2 GCC Oracle 解法

解决 Linux kernel 编译的方案是引入 GCC 作为「已知正确的编译器 oracle」：

> "I wrote a new test harness that randomly compiled most of the kernel using GCC, and only the remaining files with Claude's C Compiler."

如果 kernel build 成功，说明问题不在 Claude 编译的文件里；如果失败，再进一步细化——用 GCC 重新编译部分文件，逐步缩小问题范围。

这个方案的本质是**分治 + oracle 验证**，把一个巨大的并行难题变成多个可独立验证的子问题。

### 4.3 多角色分工

并行还支持 specialization。Carlini 为不同的 Agent 分配了不同职责：

| Agent 角色 | 职责 |
|-----------|------|
| **Compiler Agent** | 实现编译器核心功能 |
| **Dedup Agent** | 合并重复代码 |
| **Performance Agent** | 优化编译器性能 |
| **Output Agent** | 输出高效的编译产物 |
| **Review Agent** | 从 Rust 开发者视角做架构重构 |
| **Doc Agent** | 维护项目文档 |

> "LLM-written code frequently re-implements existing functionality."

这说明即使在 Agent 团队中，代码复用和架构优化仍然需要专门的角色来推动。

---

## 五、设计的工程智慧

### 5.1 站在 Claude 的角度设计 Harness

Carlini 特别强调设计测试时需要把自己放在 Claude 的位置，而不是自己的位置。这包括：

**上下文窗口污染问题**：
> "The test harness should not print thousands of useless bytes. At most, it should print a few lines of output and log all important information to a file so Claude can find it when needed."

日志必须是 machine-readable 的：有错误就写 `ERROR`，原因写在同一行，方便 `grep` 提取。预计算聚合统计数据，这样 Claude 不需要重新计算。

**时间盲区问题**：
> "Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress."

Harness 需要提供 `--fast` 选项，运行 1% 或 10% 的随机采样。这个采样对每个 Agent 是确定性的（基于 agent ID），但跨 VM 随机，确保覆盖所有文件的同时让每个 Agent 都能准确识别 regression。

### 5.2 资源与能力的匹配

实验数据揭示了一个重要规律：当资源从 1x 提升到 3x 时，infra 错误率从 5.8% 降到 2.1%（p < 0.001），但成功率在统计上没有显著差异（p=0.40）。这说明前 3x 的资源提升主要修复的是 infra 可靠性问题，而非让测试变得更简单。

当资源从 3x 提升到 uncapped 时，成功率才开始真正提升——额外的资源让 Agent 能够尝试那些「只在资源充足时才能成功」的策略，比如拉取大型依赖或运行内存密集型测试套件。

---

## 六、工程启示

### 6.1 多 Agent 协作的核心挑战

这个实验揭示了多 Agent 并行系统的几个关键工程挑战：

**协调的简洁性**：Git 锁文件机制证明，复杂的并行问题可以用极简的协调机制解决，不需要中心化的调度器。关键是让每个 Agent 能够独立判断「我现在该做什么」。

**测试先行**：无限循环的 Agent 对测试 harness 的要求近乎苛刻。如果验证机制有漏洞，Agent 会在错误的方向上越走越远。测试必须足够精确、足够快、足够全面。

**资源与能力的关系**：资源（CPU、RAM）不是线性的。达到某个阈值之前，额外的资源只是修复可靠性问题；越过阈值之后，资源才开始真正增强能力。了解这个阈值在哪里，是部署 Agent 系统时的重要考量。

### 6.2 对企业级 Agent 系统的含义

Anthropic 的实验虽然是一个 research prototype，但它揭示的方向对企业级 Agent 系统有重要参考价值：

- **任务分解 + 锁同步** 可能是大规模 Agent 协作的基本模式
- **专用角色**（编译、review、文档、性能）可以显著提升系统产出质量
- **测试驱动的自主性**（test-driven autonomy）是让 Agent 长期自主运转的关键
- **成本与能力的权衡**：$20,000 完成一个 100K 行编译器，每行成本约 $0.20，这在不同场景下有不同的经济意义

---

## 总结

这篇工程 blog 的核心价值不是「用 Agent 写了编译器」，而是**揭示了多 Agent 并行协作的系统工程边界**。当 Agent 能够通过极简的锁机制协调工作、通过接近完美的测试保持方向、通过 GCC oracle 解法处理非线性任务时，它们能够完成单个 Agent 完全无法企及的复杂系统工程。

这也解释了为什么我们看到行业从「更强的单模型」向「多 Agent 协作系统」演进：能力边界测试告诉我们，有些任务只有在多 Agent 并行时才能跨越新的阈值。

---

**引用原文**：
> "With agent teams, multiple Claude instances work in parallel on a shared codebase without active human intervention. This approach dramatically expands the scope of what's achievable with LLM agents."

> "The infinite agent-generation-loop spawns a new Claude Code session in a fresh container, and the cycle repeats."

> "Claude takes a 'lock' on a task by writing a text file to current_tasks/"

---

*来源：[Anthropic Engineering - Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | 2026-02-05*