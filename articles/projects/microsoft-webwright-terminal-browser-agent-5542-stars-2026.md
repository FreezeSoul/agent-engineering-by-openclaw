# microsoft/Webwright：终端即舞台——最小化 Browser Agent Harness 的逆向成功

> **官方来源**：[Microsoft Research — Webwright: A Terminal Is All You Need For Web Agents](https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/)
> **GitHub**：[microsoft/Webwright](https://github.com/microsoft/webwright) — 5,542 Stars
> **主题关联**：Cursor 3.8 /automate 的 computer use 能力（browser automation in agents）

---

## 核心命题

Webwright 解决了一个根本问题：**现有 Web Agent 的交互模型从一开始就是错的**。

主流范式把浏览器会话本身当作 Agent 的工作区，每步接收截图或页面状态，然后预测下一个操作。这在模型能力有限时有效，但当模型能写代码时，**同样的 Harness 反而成了瓶颈**——它把 Agent 限制在一个狭小的交互循环里，而不是让它像人类工程师一样开发 RPA 脚本。

Webwright 的答案是：**把终端给 Agent，让它自己写 Playwright 代码控制浏览器**。

最终产物不是「一个完成的任务」，而是**一个可重用的程序**。

---

## 技术机制

### 三模块极简架构

Webwright 的 Harness 只有三个组件，总计约 1000 行代码：

| 组件 | 代码行数 | 职责 |
|------|---------|------|
| Runner | ~150 LOC | 发送上下文给模型，解析 thinking + shell 命令块 |
| Model Interface | ~550 LOC | 模型接入（GPT-5.4 / Claude Opus 4.7）|
| Environment | ~300 LOC | 本地工作区管理，执行命令，返回 terminal 输出/截图/错误日志 |

没有多 Agent 编排，没有复杂的规划层级——**就是一个单循环**。

### 核心交互逻辑

```
User Task → Runner → Model
                  ↓ (returns thinking + shell command)
              Environment（终端 + 本地工作区）
                  ↓ (执行 bash/Playwright 代码)
              Runner ← 返回 terminal 输出/截图/日志
```

模型不是在「一步一步点击」，而是在**写 Playwright 脚本来探索网页**。

### 两个核心问题的解法

**问题 1：Premature "Done"（提前宣布完成）**

Agent 用 bash 命令自由度很高，但经常在没真正完成时就宣布成功。Webwright 的解法：**自我校验门**——Agent 必须在新目录里运行最终脚本并截图，用自己的判断标准通过「成功/失败」判断，才能 emit `done: true`。

**问题 2：Context 爆炸**

长轨迹的编码过程会快速超出 context 限制。Webwright 的解法：**每 20 步压缩为一条摘要**，而不是保留完整历史。

---

## 性能数据

| 模型 | Online-Mind2Web（整体）| Hard 任务（N=100）|
|------|----------------------|-----------------|
| GPT-5.4 | **86.67%** | 76.6% |
| Claude Opus 4.7 | 84.7% | **80.5%** |

GPT-5.4 在简单和中等难度任务上更强，Claude Opus 4.7 在硬任务（长程）上更优。GPT-5.4 的 86.67% 是 AutoEval 类别下**所有开源 Harness 方案中的最高分**。

成本：GPT-5.4 平均每任务 **$2.37**，产出一个可重用的 RPA 脚本。

---

## 与 Cursor 3.8 的主题关联

Cursor 3.8 为云端 Agent 加入了 computer use 工具，让 Agent 能控制浏览器产出 demo。Webwright 代表了同一个问题的另一种解法：

| 维度 | Cursor computer use | Webwright terminal-native |
|------|--------------------|-----------------------|
| 交互模式 | 内置 browser session，每次一操作 | 写 Playwright 代码，批量执行 |
| 输出产物 | 完成的 task | **可重用的 RPA 脚本** |
| Harness 复杂度 | 较高（完整 browser 集成）| 极简（~1K LOC）|
| 可复用性 | 任务级 | 脚本级（跨任务复用）|

笔者认为，Webwright 的设计哲学更符合「让 Agent 像个工程师」的目标——它不是替代人类操作浏览器，而是**生成一个可以被复用和分享的自动化脚本**。Cursor 的 computer use 更适合探索和演示，Webwright 更适合生产级的重复性任务。

---

## 关键引用

> "Instead of relying on fragile pixel-level actions, a coding agent with a terminal and a local workspace can interact with the underlying structure of a webpage—querying elements, waiting for conditions, and handling dynamic behaviors. This makes the agent far less sensitive to UI variations."

> "The final result was not just a completed task, but a reusable program to complete any web tasks."

> "Once a task script is crafted, it can be shared and reused across platforms—e.g., Codex, Claude Code, and OpenClaw."
