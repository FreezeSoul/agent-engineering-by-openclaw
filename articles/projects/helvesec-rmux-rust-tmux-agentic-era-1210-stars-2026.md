# Helvesec/rmux：Rust 重写的 tmux，为 Agent 编排而生

> **核心命题**：RMUX 用 Rust 从头重写了 tmux 的核心逻辑，加入了持久会话、结构化快照和 typed SDK——不只是替代品，而是给 Agent 时代的终端 multiplexer。

## 基本信息

| 项目 | 值 |
|------|------|
| **GitHub** | [Helvesec/rmux](https://github.com/Helvesec/rmux) |
| **Stars** | 1,210 |
| **语言** | Rust |
| **当前版本** | v0.3.1（2026-05-25 刚发布）|
| **许可** | MIT OR Apache-2.0 |

## 为什么这个项目值得关注

笔者认为，rmux 的价值在于它把「Agent 时代的终端」变成了可编程的基础设施。

tmux 解决的是终端会话管理问题，但它的模型是面向人类的——窗口、会话、pane 这些概念都围绕人的操作习惯设计。Agent 需要的是：**持久会话**（long-running agent over SSH不掉线）、**结构化快照**（可以检查/恢复状态）、**typed SDK**（代码驱动而非人类操作）。

rmux 正是从这个角度重新设计：

- **持久会话**：Agent 可以在后台运行，断开 SSH 后再 reconnect，状态不丢失
- **结构化快照**：不只是保存 terminal 输出，而是保存完整的状态结构
- **Typed SDK**：用代码控制 terminal，而非发送按键序列
- **跨平台**：Linux / macOS / Windows，包括 Windows Named Pipes

## 与 AI Engineering Coach 的互补关系

| 维度 | AI Engineering Coach | rmux |
|------|---------------------|------|
| **解决的问题** | AI Coding 实践的量化评估 | Agent 终端会话的持久化与编排 |
| **层级** | Harness 工程化 | 基础设施层 |
| **关联性** | 评估反馈循环 | 长时任务执行 |

两者共同指向 **AI Coding Agent 的工程基础设施**：Coach 管「做得好不好」，rmux 管「跑得稳不稳」。

## 快速上手

```bash
curl -fsSL https://rmux.io/install.sh | sh
```

## 引用

> "RMUX exists because I believe the tmux use case has only been partially explored. My own starting point was simple: I wanted to run long-lived agents over SSH without losing their terminals, while still being able to inspect, script, and orchestrate everything around them."
> — [README.md](https://github.com/Helvesec/rmux/blob/main/README.md)

> "RMUX is usable by agents, headless CLI workflows, and humans alike: you can give terminal apps detachable execution, reconnect later, inspect their state, drive them from code, or simply use it for normal tmux-style terminal work."
> — [README.md](https://github.com/Helvesec/rmux/blob/main/README.md)