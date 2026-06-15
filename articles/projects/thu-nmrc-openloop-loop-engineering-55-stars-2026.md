# OpenLoop：让 Agent 开发循环变成可工程化的基础设施

> THU-NMRC 出品的通用 Loop Engineering 框架，将 "play-test-fix-verify-improve" 循环从隐性的 Agent 行为变成显性的、可审计的工程系统。
> GitHub: [thu-nmrc/openloop](https://github.com/thu-nmrc/openloop) · Stars: 55 · Python · Apache-2.0 · 2026-06-10

---

## 核心命题

**Agent 的长任务执行最缺的不是推理能力，是状态可视化和停止条件。**

大多数 Agent 框架关注"Agent 能做什么"，很少关注"Agent 在做什么"。当一个 Agent 开始处理复杂任务（扫描 100 个 bug、修复一个旧代码库、写一个完整应用），开发者面对的是一个黑箱：Agent 当前在哪一步？进展到多少？什么时候该停下来？失败了怎么办？

OpenLoop 的核心洞察是：**一个真正的循环不是定时器，它知道自己在哪。**

---

## 为什么这个项目值得关注

### 直接解决长任务 Agent 的核心工程难题

OpenLoop 将长任务 Agent 的执行过程从"靠记忆和日志"变成"靠状态文件和验证门"。每个循环 workspace 包含：

```
.openloop/workspace/
├── openloop.json        # 可执行的循环配置
├── mission.md          # 目标、非目标、完成定义
├── loop_contract.md    # play→scan→fix→verify→baseline 协议
├── heartbeat.json     # 当前状态：PID、log路径、round、step、速度、ETA
├── progress.md         # 只增不减的时间线
├── logs/               # 每条命令的原始输出
├── artifacts/          # 每轮 JSON 报告
└── knowledge/          # 持久化的经验教训
```

开发者可以随时查询：`openloop status workspace` → 看到 Agent 当前在哪、跑了多久、下一步是什么、验证通过没有。

### 内置的工程化保护机制

| 问题 | 传统 Agent 的做法 | OpenLoop 的做法 |
|------|-----------------|----------------|
| 任务中途丢失状态 | 靠 Chat 记忆或临时笔记 | `heartbeat.json` + `progress.md` 持久化 |
| Agent 提前宣称成功 | 自我复盘 | 外部 `verify` + `baseline` 双重验证门 |
| 不知道任务跑到哪了 | 子进程隐藏在后台 | 每次心跳记录 PID、命令、log路径、round、step |
| 重复失败烧预算 | 无限重试 | `circuit breaker` + `stall detection` + `OOM detection` |
| 无法审计 | 一个巨大的 transcript | 每条命令独立 log + 每轮 JSON report |
| 绑定特定 Agent | 平台相关 workflow | Shell 命令适配器，接任何 CLI Agent |

### 配置即循环，循环即协议

OpenLoop 的 workspace 由 `openloop.json` 驱动：

```json
{
  "version": 1,
  "mission": "Keep the project playable, verified, and above baseline.",
  "total_rounds": 3,
  "project_root": ".",
  "commands": {
    "play": "python app.py",
    "scan": "python -m unittest discover -s . -p 'test_*.py'",
    "fix": "your-agent-cli --workspace {project_root} --task 'Fix the latest failure'",
    "verify": "python -m unittest discover -s . -p 'test_*.py'",
    "improve": "your-agent-cli --workspace {project_root} --task 'Improve until baseline passes'"
  },
  "baseline": {
    "enabled": true,
    "command": "python benchmark.py",
    "metric_name": "score",
    "regex": "score=([0-9]+\\.[0-9]+)",
    "value": 0.9,
    "direction": "greater_equal"
  },
  "limits": {
    "command_timeout_seconds": 900,
    "stall_timeout_seconds": 300,
    "max_consecutive_failures": 3
  }
}
```

Mission 定义"做什么"，loop_contract 定义"怎么做"，eval_criteria.md 定义"什么时候算完成"——这三者加在一起，就是一个 **Harness**。

### Agent 无关：任何 Agent 都能接入

OpenLoop 不绑定特定 Agent 平台。任何可以通过 shell 命令调用的 Agent 都可以接入 `commands.fix` 或 `commands.improve`。这意味着：
- Cursor Agent、Claude Code、Browse UI、GitHub Copilot Agent 都可以作为执行器
- 切换 Agent 不需要修改 OpenLoop workspace 配置
- 每个 Agent 产生的 logs 和 artifacts 格式统一，可对比

---

## 工作流解析

OpenLoop 的循环由 5 个步骤组成，每个步骤都可配置、可审计、可替换：

```
Mission
   ↓
Play / 使用项目
   ↓
Scan / 扫描问题（找 bug、找性能瓶颈、找安全漏洞）
   ↓
Repair / 通过任何 Agent 或脚本修复
   ↓
Verify / 运行确定性检查
   ↓
Compare / 与 baseline 对比（如启用）
   ↓
Persist / 持久化心跳、进度、日志、artifacts
   ↓
继续 / 完成 / 安全阻断
```

每一步骤的输出都是一个独立 log 文件，心跳在每一步前后都更新。开发者可以用 `openloop status --json` 查询当前完整状态。

**任务完成的条件（同时满足）**：
- verify 命令通过
- baseline 指标达标（如启用）
- 无 timeout / stall / OOM / 异常退出
- logs 和 artifacts 已写入

**任务阻断的条件**：
- 连续失败次数超过 `limits.max_consecutive_failures`
- 触发 circuit breaker（超时、stall、OOM）

---

## 与 Harness Engineering 的对应关系

OpenLoop 是 Harness Engineering 思想的直接工程实现：

| Harness Engineering 概念 | OpenLoop 实现 |
|------------------------|-------------|
| **Evaluator Loop** | `verify` + `baseline` 命令构成评估器，每次循环运行 |
| **Checkpoint / Progress File** | `heartbeat.json` + `progress.md` |
| **Working State Persistence** | `logs/` + `artifacts/` per-round JSON reports |
| **Stop Condition / Guardrail** | `circuit breaker` + `stall detection` + `max_consecutive_failures` |
| **Clean State Handover** | workspace 隔离设计，每次 mission 可重置 |
| **Auditable Log** | 每条命令独立 log + JSONL event stream |

更重要的是，OpenLoop 将 **Harness 的黑箱设计变成白盒配置**——开发者不需要理解内部机制，只需要写 `openloop.json` 和 `mission.md`。

---

## 适用场景与局限性

**适用场景**：
- 需要 Agent 处理跨多个步骤的长任务（如代码库重构、测试覆盖率提升）
- 需要对 Agent 行为做可重复的验证（如 CI/CD 中的 Agent 评测）
- 需要在多轮迭代中追踪改进轨迹（如性能优化、安全漏洞修复）
- 团队需要在同一个 Agent 执行过程中查看进度和日志

**局限性**：
- Stars 只有 55（2026-06-10 刚发布），成熟度待验证
- 核心价值在于"监控"而非"执行"——Agent 本身的质量仍然依赖底层能力
- 偏向开发测试场景，生产环境的高可用要求（如分布式、容错）未覆盖
- 无云端服务，纯本地 workspace

**笔者的判断**：OpenLoop 是 2026 年 Loop Engineering 方向最纯粹的开源实现。它的价值不是"替代 Agent"，而是"让任何 Agent 的长任务执行变得可观测、可控制、可审计"。如果你的 Agent 系统经常遇到"不知道跑到哪了"或"Agent 说完成了但实际没完成"的问题，OpenLoop 值得一试。

---

## 快速上手

```bash
pip install openloop

openloop init .openloop/demo --project-root examples/demo_project \
 --mission "Keep the demo project working and above baseline"

openloop run .openloop/demo --max-rounds 3

openloop status .openloop/demo --json
```

---

## 参考来源

1. [thu-nmrc/openloop GitHub README](https://github.com/thu-nmrc/openloop) — 官方 README
2. [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/) — OpenAI Engineering Blog（自进化 Agent 的 eval loop 设计）
3. [Harness Engineering](https://openai.com/index/harness-engineering/) — OpenAI（OpenLoop 的理论依据）