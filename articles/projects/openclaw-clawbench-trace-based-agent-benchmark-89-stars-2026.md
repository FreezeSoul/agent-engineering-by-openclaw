# ClawBench：让 OpenClaw 的 Agent 循环可量化评测

> **来源**：[openclaw/clawbench](https://github.com/openclaw/clawbench)（89 Stars，2026-03）
> **主题**：OpenClaw 生态的首个标准化 Benchmark——用 trace-based 方法评测 Agent 在开放世界任务中的自主完成任务能力
> **关联 Article**：[OpenClaw Gateway 架构：用一个进程连接所有消息表层](/articles/fundamentals/openclaw-gateway-architecture-one-process-all-channels-2026.md)

---

## 核心命题

OpenClaw 在消息接入层做到了极致——一个 Gateway 连接所有渠道。但在「如何评测 Agent 完成任务的能力」上，OpenClaw 社区终于有了自己的答案：**ClawBench，一个基于 trace 的 Agent 自主性评测工具。**

这个项目解决的是：当你有了一个「无处不在」的 Agent 系统后，如何客观衡量它在不同任务上的表现，而不是靠感觉说「它好像挺聪明的」。

---

## 技术原理

ClawBench 采用 **trace-based evaluation** 方法：

1. **记录 Agent 执行轨迹**：在开放世界任务中记录完整的 tool call 序列、决策点、环境交互
2. **离线回放分析**：用相同 trace 在不同模型/配置下回放，对比结果差异
3. **多维度评分**：不仅看最终是否完成，还评估步骤效率、工具使用质量、错误恢复能力

官方 README 的核心定位：

> Trace-based agent benchmarking for open-world task completion

这意味着 ClawBench 评测的是 Agent 在**真实开放环境**（而非 benchmark 构造的封闭问题）中的能力——这比 SWE-bench 或 Terminal-Bench 更接近实际使用场景。

---

## 架构亮点

### 与 OpenClaw Gateway 的天然集成

ClawBench 内置支持读取 OpenClaw 的 agent trace 输出格式，这意味着：

- **零格式转换**：直接在生产环境捕获的 trace 可以直接导入 ClawBench 评测
- **Gateway 事件驱动**：`event:agent` 流式输出直接作为评测数据源
- **生态闭环**：从「Agent 执行」到「结果记录」到「量化评测」，全部在 OpenClaw 生态内完成

### 多模型对比能力

ClawBench 支持在相同任务集上对比多个模型的表现，输出可视化的能力雷达图。这对于做模型选型的团队非常有价值——可以快速判断哪个模型在你的特定任务分布上表现最好。

---

## 竞品对比

| 维度 | ClawBench | SWE-bench | Terminal-Bench |
|------|-----------|-----------|---------------|
| **评测场景** | 开放世界任务 | 程式化代码修复 | 命令行 DevOps |
| **评测方法** | Trace 回放 | 容器化代码执行 | 沙箱终端 |
| **与 OpenClaw 集成** | ✅ 原生 | ❌ | ❌ |
| **Stars** | 89 | 60K+ | 1.3K |
| **覆盖场景** | 通用 Agent 能力 | 编程能力 | 终端操作 |

**笔者认为**：ClawBench 的价值不在于 Stars（89个，确实很少），而在于它是 **OpenClaw 生态内唯一的标准化评测工具**。随着 OpenClaw 用户规模增长（374K Stars），必然会有更多用户需要回答「我的 Agent 到底好不好」，ClawBench 正好填补这个空白。它目前的 Stars 低只是因为项目太新，不代表它不重要。

---

## 适用场景

- **OpenClaw 用户**做模型/配置选型时，量化对比不同 setup 的表现
- **Agent 开发者**在做 benchmark 时，需要一个轻量级的 trace 分析工具
- **研究者**想要评测 Agent 在开放世界任务中的自主完成能力，而不只是编程题解率

---

## 快速上手

```bash
# 安装
npm install -g clawbench

# 从 OpenClaw trace 导入
clawbench import --source openclaw --trace ./session-trace.json

# 运行评测
clawbench run --task-set openclaw-default --model claude-sonnet

# 生成报告
clawbench report --format markdown
```

---

## 参考链接

- [ClawBench GitHub](https://github.com/openclaw/clawbench)（89 Stars）
- [OpenClaw Gateway 架构 Article](/articles/fundamentals/openclaw-gateway-architecture-one-process-all-channels-2026.md)