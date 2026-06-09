# human-again/orbit：编码 Agent 的 Mission Control，让验证 gate 真正工作

> orbit 是目前最接近"可工程化的 Agent Harness"概念的开源实现——structured loops、validation gates、rubric-based evaluation、checkpoint resumability。它用 4 Stars、v0.1.0 的状态，换来一张足够清晰的架构蓝图。

---

## 核心命题

大多数 Agent Coding 框架把"让 Agent 跑起来"当作目标。orbit 把"让 Agent 跑出可信的结果"当作目标。

这两件事的差别，就是**有没有验证 gate**。

> 原文引用（orbit README）：*"Orbit is the harness your coding agent actually needs — structured loops, real validation gates, rubric-based evaluation, checkpoint resumability, and a full audit trail. Define the mission. Orbit lands it."*

---

## 为什么这个项目值得关注

### 1. 架构即方法论

orbit 的源代码结构本身就是一份**Harness Engineering 的工程清单**：

```
orchestrator.py       ← mission control，主循环
adapters/             ← 可插拔的 Agent 适配器
evaluator.py          ← rubric 评分
reviewer.py           ← accept/iterate 推荐
validation_runner.py  ← 运行 test/lint 命令
retry_policy.py       ← 失败或验证未通过时的重试策略
checkpoint_manager.py ← 持久化可恢复状态
budget_manager.py     ← 运行/失败/成本上限
diff_evaluator.py     ← git diff 检测
risk_guard.py         ← 命令分类与安全边界
observability.py      ← 结构化遥测日志（events.jsonl）
```

笔者认为，这个目录结构值得任何计划构建 Agent Harness 的人抄一遍——它覆盖了编排、评估、恢复、安全、观测四个维度，没有遗漏。

### 2. 验证 gate 不是 if-else，是 rubric-based

大多数 Agent 框架的"验证"就是检查退出码或简单断言。orbit 的 evaluator.py 实现了 **rubric-based evaluation**：

> 原文引用（orbit README）：*"Orbit rescuing a broken auth flow：Orbit detects a failing test, selects the right task, runs the agent, validates the fix, and marks the orbit complete — no hand-holding required."*

这是"检测失败 → 选择任务 → 运行 agent → 验证修复 → 标记完成"的完整闭环，和 Anthropic 的 planner-generator-evaluator 三 Agent 架构逻辑一致。

### 3. Checkpoint Resumability 的工程实现

很多框架声称支持"resume"，但实现往往是 serialize 整个 session。orbit 的 `checkpoint_manager.py` 实现的是**增量检查点**——任务级别的状态恢复，而非全量 session 恢复。

> 原文引用（orbit README）：*"checkpoint resumability"*

这意味着即使 Agent 在长任务中途失败，从检查点恢复的代价也是最小化的。

### 4. Multi-agent Handoffs 的适配器模式

orbit 的 `adapters/` 目录支持**同一 harness、不同 agent 适配器**：

> 原文引用（orbit README）：*"Run one orbit with Claude for implementation, a second with Codex for review, and a third with your custom CLI for deployment checks — same harness, swappable adapters."*

这是 Anthropic 说的"decouple brain from hands"理念的直接实现——harness 是稳定的，agent 是可替换的。

---

## 技术细节

### 关键文件速览

| 文件 | 职责 | 工程意义 |
|------|------|---------|
| `orchestrator.py` | mission control 主循环 | Harness 的控制平面 |
| `checkpoint_manager.py` | 持久化状态 | 跨 session 恢复的基础 |
| `evaluator.py` | rubric 评分 | 不是 binary pass/fail，是多维度评估 |
| `risk_guard.py` | 命令分类与 gate | 安全边界实现 |
| `observability.py` | events.jsonl 遥测 | 可审计性的基础设施 |
| `retry_policy.py` | 重试策略 | 错误容忍的实现 |
| `mission.md` | 任务定义 | 人机对齐的载体 |
| `backlog.json` | 带验收标准的任务列表 | 任务分解的结构化 |

### 与 Anthropic 三 Agent 架构的对应关系

```
Anthropic 架构              orbit 实现
───────────────────────────────────────
Planner Agent        →     orchestrator.py（任务分解 + backlog.json）
Generator Agent      →     adapters/（具体执行）
Evaluator Agent     →     evaluator.py + reviewer.py
Context Reset        →     checkpoint_manager.py
Auto Mode Security   →     risk_guard.py
```

### 已知限制

- **Stars 仅 4**：这是一个非常早期的项目（v0.1.0），生产使用需自行评估风险
- **文档待完善**：README 信息有限，详细的 API 文档尚未完成
- **Python 3.11+**：对老版本 Python 不兼容

---

## 与本文的闭环

本文（Anthropic 多 Agent 系统三层工程机制）和 orbit 项目形成完整闭环：

- **Article** 描述了多 Agent 系统的三个工程机制（编排架构、恢复机制、安全防护）应该如何设计
- **orbit** 是这三个工程机制在开源世界中的一个参考实现

笔者认为，orbit 的价值不在于它目前有多成熟，而在于它展示了一条**从框架到工程化**的路径——当你想从"让 Agent 跑起来"进化到"让 Agent 跑出可信结果"时，orbit 的目录结构本身就是一份路线图。

---

## 快速上手

```bash
git clone https://github.com/human-again/orbit.git
cd orbit
pip install -e .
# 定义 mission.md
# 定义 agent-rules.md
# 定义 backlog.json（带验收标准）
python -m orbit.orchestrator
```

---

## 原文引用

1. orbit README, https://github.com/human-again/orbit

---

## 相关阅读

- [Anthropic 多 Agent 系统三层工程机制](../fundamentals/anthropic-multi-agent-system-engineering-three-mechanisms-2026.md)
- [Anthropic Scaling Managed Agents](https://anthropic.com/engineering/managed-agents)
