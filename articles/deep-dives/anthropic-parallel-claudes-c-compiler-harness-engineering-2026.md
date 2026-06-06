# Anthropic 并行 Claude 团队：2000 Session 构建 C 编译器的 Harness 工程复盘

**来源**：Anthropic Engineering Blog — Nicholas Carlini (Safeguards Team)
**URL**：https://www.anthropic.com/engineering/building-c-compiler
**核心命题**：用并行 Agent 团队完成 10 万行 C 编译器，关键不在 Agent 本身，而在于如何设计让 Agent 能够自主推进的 Harness 工程机制

---

## 一、问题：为什么单 Agent 做不到

现有 Agent 框架（如 Claude Code）需要人类操作员在线才能工作。给一个复杂问题，模型解决一部分后会停下来等待继续输入——一个问题、一个状态更新，或一个澄清请求。

作者面临一个极端压力测试：让 16 个 Agent 并行写一个能编译 Linux 内核的 Rust C 编译器。最终结果：
- 近 **2000 次** Claude Code Session
- 花费 **$20,000** API 成本
- 产出 **100,000 行**代码
- 编译器能构建 Linux 6.9（x86、ARM、RISC-V）

这个成本/时间投入值得分析的不是"编译器本身"，而是**让 Agent 团队能够自主推进的 Harness 工程设计**。

---

## 二、核心工程机制

### 2.1 自主推进循环（While-True Harness Loop）

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

Agent 完成一个任务后，立即开始下一个，无需人工介入。AGENT_PROMPT.md告诉 Agent：
- 要解决什么问题
- 将问题分解为小任务
- 跟踪当前进度
- 主动判断下一个要做什么
- **一直做到完美**（循环是无限的）

>原文："The loop runs forever—although in one instance, I did see Claude pkill -9 bash on accident, thus killing itself and ending the loop. Whoops!"

### 2.2 Git-Based 任务同步与锁定

多 Agent 并行最大的挑战：如何防止两个 Agent 做同一件事。

```bash
# Agent 通过在 current_tasks/ 目录写锁文件来"认领"任务
# 例如：current_tasks/parse_if_statement.txt
# 如果两个 Agent 同时认领，git 同步机制强制后者换一个任务
```

流程：
1. Agent 在 `current_tasks/` 目录写文件获取任务锁
2. Git 的同步机制确保只有一个 Agent 能成功认领
3. Agent 完成工作后 pull → merge → push → 释放锁
4. 合并冲突频繁，但 Claude 足够智能能自行解决

> 原文："I don't use an orchestration agent. Instead, I leave it up to each Claude agent to decide how to act. In most cases, Claude picks up the 'next most obvious' problem."

### 2.3 并行 Docker 容器隔离

每个 Agent 运行在独立 Docker 容器中：
- 新建裸 git 仓库
- 为每个 Agent 启动一个容器，将仓库挂载到 `/upstream`
- Agent clone 本地副本到 `/workspace`
- 完成后从容器内 push 到 upstream

### 2.4 测试优先的高质量测试套件

Agent 会自主解决任何给定的任务。**所以任务验证器必须近乎完美**，否则 Agent解决的是错误的问题。

改进测试 Harness 需要：
- 找高质量编译器测试套件
- 为开源软件包写验证器和构建脚本
- 观察 Claude 常犯的错误，针对性地设计新测试

临近项目结束时，Claude 每次实现新功能都会频繁破坏现有功能。解决方案：**持续集成流水线 + 更严格的 enforce**，确保新 commit 不能破坏已有代码。

---

## 三、从 Harness 设计中学到的工程教训

### 3.1 测试要站在 Claude 的角度设计

作者不断提醒自己：测试 Harness 是为 Claude 写的，不是为自己写的。这意味着要重新思考很多关于测试如何传递结果的假设。

**上下文窗口污染问题**：
- Harness 不应该打印数千字节的无用信息
- 最多打印几行输出，所有重要信息记录到文件
- 错误时 Claude 应该写 `ERROR` 并在同行写明原因（便于 grep）
- 预先计算聚合统计信息，避免 Claude 重复计算

**时间盲问题**：
- Claude 无法感知时间，脱离约束会花数小时跑测试而非推进工作
- Harness 以低频打印增量进度（避免污染上下文）
- 提供默认 `--fast` 选项，只跑 1% 或 10%随机样本

### 3.2 每个 Agent 需要自包含的初始化

每个 Agent 被放到一个全新容器，没有上下文。在大型项目上会花大量时间自我定位。

**解决方案**：
- 提供大量 README 和进度文件，频繁更新当前状态
- 这些文件是 Agent 的"记忆"，让它知道自己在哪里、要做什么

### 3.3 Harness 的极限

这是非常早期的研究原型。没有实现：
- Agent 之间的通信机制
- 管理高层目标的过程
- 编排 Agent

> 原文："I don't use an orchestration agent. Instead, I leave it up to each Claude agent to decide how to act."

---

## 四、工程机制分类：Harness 不是安全防护

本文定义的 Harness 包含完整的 Agent 工程机制设计：

| 机制类型 | 本文内容 | 归属 |
|---------|---------|------|
| **评估器循环** | 测试套件验证，CI enforce | Harness |
| **接力/恢复机制** | While-true loop，AGENT_PROMPT.md | Harness |
| **工作区状态管理** | Git current_tasks/ 锁机制 | Harness |
| **工具安全/权限分层** | --dangerously-skip-permissions | Harness |

> **笔者认为**：Harness 工程不是"给 Agent 加护栏"，而是设计一套让 Agent 能够**自主推进、自主协同、自主验证**的运行时环境。安全护栏只是其中一小部分。

---

## 五、与 Flue 的关联

本文的 Harness 设计（while-true loop + task lock + session 管理）是手工版本的 Flue 框架所解决的核心问题。Flue 将这套机制产品化为：

- 内置 agent harness 运行时
- 虚拟沙箱（just-bash）替代 Docker 容器的轻量方案
- 工作流路由 + HTTP/WebSocket 暴露
- 跨部署目标（Node.js / Cloudflare / CI）

两者共同指向一个核心判断：**Harness Engineering 是 Agent 从"演示"到"生产"的关键瓶颈**。

---

## 六、核心判断

1. **多 Agent 并行的核心协调问题**：不是通信，而是任务分配。Git 的同步机制（通过文件系统冲突）意外地解决了分布式任务锁问题，比设计专门的协调协议更简单。

2. **测试即架构**：Agent 自主推进的前提是验证器近乎完美。高质量测试套件是 Harness最重要的组件，不是工具调用或 Prompt。

3. **自包含初始化的价值**：每个 Agent 放在干净容器 + 完整 README + 进度文件，比预设复杂的状态机更可靠。

4. **Harness 的极限**：当前的自主 Agent 团队还没有高层目标管理、Agent 间通信协议和编排层。这不是实现问题，而是架构认知问题。

---

## 七、引用

> "The scaffolding runs Claude in a loop, but that loop is only useful if Claude can tell how to make progress. Most of my effort went into designing the environment around Claude—the tests, the environment, the feedback—so that it could orient itself without me."

> "I don't use an orchestration agent. Instead, I leave it up to each Claude agent to decide how to act."

> "Improving the testing harness required finding high-quality compiler test suites, writing verifiers and build scripts for open-source software packages, and watching for mistakes Claude was making, then designing new tests as I identified those failure modes."