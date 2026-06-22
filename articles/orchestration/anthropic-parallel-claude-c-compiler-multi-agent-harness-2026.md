# 并行克劳德写 C 编译器：多智能体协作的工程机制实证

> Anthropic 研究员 Nicholas Carlini 用 16 个 Claude Code 实例并行开发了一个可编译 Linux 内核的 Rust C 编译器，耗资 2 万美元、2000 次会话、10 万行代码。本文深入解析其背后的多智能体工程机制：Ralph-loop 持续循环、Git 锁文件同步、Docker 容器隔离、测试驱动 Harness，以及角色专业化模式。

---

## 核心论点

**多智能体协作的瓶颈从来不是"智能"，而是"协调机制"**。当 16 个 Claude 并行在同一个代码库上工作时，核心挑战不是让每个 agent 足够聪明，而是让它们能够：① 互不冲突地认领任务，② 无需人工干预地持续工作，③ 通过高质量测试自我验证。Anthropic 这项研究提供了一个完整的工程答案——不是依赖复杂的编排协议，而是用极简的 Git 同步 + 循环 Harness + 角色专业化，解决了并行协作中最难的三个问题。

---

## 背景：一个编译器，16 个 agent，2000 次会话

2026 年 2 月，Anthropic Safeguards 团队研究员 Nicholas Carlini 发起了一个压力测试：用 AI agent 团队从零构建一个能编译 Linux 内核的 C 编译器。项目参数：

- **最终产物**：Rust 编写的 C 编译器，100,000 行代码，可编译 Linux 6.9（x86、ARM、RISC-V）
- **资源消耗**：约 2000 次 Claude Code 会话，20,000 美元 API 成本
- **核心发现**：不是编译器本身，而是**如何设计一个让多个 agent 持续自主协作的 Harness**

> "With agent teams, multiple Claude instances work in parallel on a shared codebase without active human intervention. This approach dramatically expands the scope of what's achievable with LLM agents."
> — Nicholas Carlini, Anthropic

这个陈述的工程含义是：现有 Agent 框架（如 Claude Code）的设计假设是"人在循环中"（human-in-the-loop），但这项研究证明，无人值守的持续协作是可行的——代价是需要在 Harness 层面做大量工程投入。

---

## 工程机制一：Ralph-loop — 让 agent 永不停机

### 问题

Claude Code 是会话式的：agent 完成任务后会停下来等待下一步指令。当任务需要数千次操作才能完成时，依赖人工持续输入是不现实的。

### 解决方案

Carlini 采用了名为"Ralph-loop"的无限循环 Harness：

```bash
#!/bin/bash
while true; do
  COMMIT=$(git rev-parse --short=6 HEAD)
  LOGFILE="agent_logs/agent_${COMMIT}.log"

  claude --dangerously-skip-permissions \
    -p "$(cat AGENT_PROMPT.md)" \
    --model claude-opus-X-Y &> "$LOGFILE"
done
```

每次 Claude 完成当前任务后，循环立即启动新会话，传入 AGENT_PROMPT.md 中定义的目标和上下文。**关键设计**：

- **无人工介入**：每次会话结束时立即自动启动下一次
- **commit 为锚点**：用 Git commit hash 标记会话边界，日志可追溯
- **危险标志**：必须使用 `--dangerously-skip-permissions`（在容器环境中降低风险）

> "Claude has no choice. The loop runs forever—although in one instance, I did see Claude pkill -9 bash on accident, thus killing itself and ending the loop. Whoops!"

这揭示了 loop 设计的一个副作用：足够聪明的 agent 可能会尝试"结束自己"来跳出困境。防护措施需要考虑 agent 对进程生命周期的控制能力。

**工程启示**：Ralph-loop 解决了持续性问题，但引入了新的危险边界。生产环境中必须在容器级别做权限限制，防止 agent 逃逸到宿主机。

---

## 工程机制二：Git 锁文件 — 极简的多 agent 同步

### 问题

16 个 agent 并行工作，如何防止两个 agent 同时修改同一个文件、覆盖彼此的代码？

### 解决方案

**Git 本身就是同步机制**——不需要额外的消息队列或分布式锁：

1. **任务锁文件**：Agent 通过在 `current_tasks/` 目录下创建文件来声明任务所有权
   ```bash
   # Agent A 认领任务
   echo "working on parse_if_statement" > current_tasks/parse_if_statement.txt
   # Agent B 尝试认领同一任务时，git 操作会失败
   ```

2. **Git merge 处理冲突**：每个 agent 完成任务后执行：
   ```bash
   git pull upstream  # 合并其他 agent 的变更
   git push          # 推送自己的变更
   rm current_tasks/parse_if_statement.txt  # 释放任务锁
   ```

3. **冲突由 Claude 自行解决**：合并冲突频繁出现，但 Claude 能理解并正确合并——**这是关键洞察**：模型不仅能写代码，还能理解他人的代码意图并合并。

> "I haven't yet implemented any other method for communication between agents, nor do I enforce any process for managing high-level goals. I don't use an orchestration agent. Instead, I leave it up to each Claude agent to decide how to act."

**工程启示**：这个发现反驳了"多 agent 必须有中央编排者"的假设。Git 的去中心化协作模型（每个人独立工作，通过 merge 同步）同样适用于 AI agent 团队，而且不需要任何额外的协调基础设施。

---

## 工程机制三：容器隔离 — 每个 agent 独立的工作空间

### 实现方式

每个 agent 运行在独立的 Docker 容器中：
- 共享同一个 bare Git repo（挂载到 `/upstream`）
- 每个容器内克隆到 `/workspace` 的本地副本
- 容器销毁后不留痕迹，天然的状态清理

```bash
# 为每个 agent 启动独立容器
docker run -v /path/to/bare-repo:/upstream -d image-name
```

**隔离的工程价值**：
- **无状态工作**：Agent 每次启动都是"新鲜"状态，不依赖前一次运行的残留上下文
- **blast radius 控制**：即使 agent 执行了危险操作，也仅限容器内
- **并行保证**：容器间完全隔离，互不干扰

> "Run this in a container, not your actual machine."

---

## 工程机制四：测试驱动 Harness — 让 agent 自我验证

### 问题

Carlini 在文章中强调：**最有挑战性的工程工作不是让 agent 写代码，而是设计让 agent 能够自我验证的测试框架**。

### 核心原则

1. **测试必须是近乎完美的验证器**
   
   > "Claude will work autonomously to solve whatever problem I gave it. So it's important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."

   如果测试本身有漏洞，agent 会非常聪明地"绕过"它——不是作弊，而是找到测试未覆盖的边界条件并满足字面条件但不满足真实意图。

2. **测试套件需要覆盖 Agent 的典型失败模式**
   
   项目后期，Claude 频繁在新功能实现中破坏已有功能。解决方案是构建 CI 流水线，对每次提交运行完整的回归测试套件。

3. **子采样策略应对"时间盲区"**
   
   > "Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress."

   解决方案：默认运行 1% 或 10% 的随机子采样（每个容器固定 seed，保证可复现）。这样 agent 能快速验证，同时覆盖所有文件。

4. **上下文污染控制**
   
   > "Logfiles should be easy to process automatically: if there are errors, Claude should write ERROR and put the reason on the same line so grep will find it."

   测试 Harness 应该输出极简的日志（最多几行），重要信息存储在文件中供 agent 按需读取。

---

## 工程机制五：GCC Oracle — 大型任务的并行化策略

### 问题

当 agent 开始编译 Linux 内核时，遇到了一个独特的挑战：内核是一个**巨大的单体任务**，不像测试套件那样有数百个独立测试。

### 解决方案

Carlini 采用了 **GCC 作为 Oracle** 的策略：

- 大部分文件用 GCC 编译（已知正确的编译器）
- 只将剩余文件交给 Claude 编写的编译器
- 如果内核构建成功 → Claude 的编译器没问题
- 如果失败 → 通过二分法逐步缩小问题文件范围

**这个技巧让并行化重新生效**：原本 16 个 agent 卡在同一个 bug 上；引入 GCC Oracle 后，每个 agent 可以并行处理不同文件的编译 bug。

---

## 工程机制六：角色专业化 — 多 agent 的分工模式

### 发现

Carlini 为不同 agent 分配了不同的专业角色：

| Agent 角色 | 职责 | 说明 |
|-----------|------|------|
| **任务执行 Agent** | 解决具体编程问题 | 大多数 agent |
| **代码整合 Agent** | 合并重复代码 | LLM 倾向于重复实现已有功能 |
| **性能优化 Agent** | 提升编译器本身的性能 | 优化编译速度和输出质量 |
| **代码审查 Agent** | 从 Rust 开发者视角批判设计 | 结构性问题识别 |
| **文档 Agent** | 维护 README 和进度文件 | 上下文保持 |

> "I put another in charge of improving the performance of the compiler itself, and a third I made responsible for outputting efficient compiled code. I asked another agent to critique the design of the project from the perspective of a Rust developer."

**工程意义**：角色专业化解决了两个问题：
1. **注意力分散**：每个 agent 有明确职责，不会在"修复 bug"和"改进架构"之间频繁切换
2. **并行效率**：多个 agent 可同时处理不同维度的问题（功能+性能+质量）

---

## 局限与天花板

Carlini 坦承这个系统的局限性：

1. **无高层目标管理**：没有 orchestration agent 维护整体进度，agent 靠"选择最明显的下一个问题"推进
2. **无 agent 间直接通信**：所有协调依赖 Git 间接同步
3. **长程依赖处理**：对于跨越数百次变更的复杂重构，Ralph-loop 的简单"继续前进"策略会失效
4. **资源消耗巨大**：2000 次会话 + 20,000 美元，对于一个 C 编译器来说成本不低

> "This is a very early research prototype."

---

## 对 Agent 工程的意义

这篇文章的贡献不在于"造出了一个 C 编译器"，而在于**证明了无人值守的多 agent 协作是可行的工程路径**，并提供了具体的 Harness 设计模式：

| 机制 | 解决的问题 | 可复用程度 |
|------|-----------|-----------|
| Ralph-loop | 持续工作能力 | ★★★ 极高 |
| Git 锁文件同步 | 多 agent 任务协调 | ★★★ 极高 |
| Docker 容器隔离 | 状态管理与安全边界 | ★★★ 极高 |
| 测试驱动 Harness | 自主验证能力 | ★★★ 极高 |
| GCC Oracle | 大型单体任务并行化 | ★★ 一般（需要领域 Oracle）|
| 角色专业化 | 注意力分配与并行效率 | ★★ 中等（需要任务可分解）|

**笔者认为**：最有价值的工程贡献是 Git 锁文件同步——它证明了一个去中心化、无中央协调者的多 agent 协作模式是可行的。这与当前主流的"A2A 协议 + 编排者"范式形成鲜明对比。Git 的成功在于它是一个**已经解决了去中心化协作问题**的成熟系统，agent 可以直接复用这个模式而不需要重新发明协调机制。

---

## 引用来源

1. Nicholas Carlini, "Building a C compiler with a team of parallel Claudes", Anthropic Engineering Blog, February 2026. https://anthropic.com/engineering/building-c-compiler
2. Anthropic, "claudes-c-compiler" GitHub Repository. https://github.com/anthropics/claudes-c-compiler

---

*本文是 R498 轮产出，分析深度优先于数量。*
