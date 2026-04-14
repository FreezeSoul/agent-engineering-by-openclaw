# Improving Deep Agents with Harness Engineering：Middleware 与自验证闭环的工程实践

> **核心问题**：Coding Agent 的最大失败模式不是「模型不会」，而是「模型以为自己写对了但没验证」。LangChain 的 Deep Agents 团队通过 13.7 点的 Terminal Bench 2.0 提升（52.8 → 66.5）证明：解决这个问题的关键不在模型层，而在 Harness 层——具体来说，是一系列可复用的 Middleware 组件和一个自验证闭环。
>
> **读完能得到什么**：理解 PreCompletionChecklistMiddleware、LoopDetectionMiddleware、LocalContextMiddleware 的设计动机与实现逻辑；掌握「Reasoning Sandwich」推理资源分配策略；了解 Trace Analyzer Agent Skill 如何将失败案例转化为 Harness 改进信号。

---

## 一、问题：模型写完代码后为什么不验证

Terminal Bench 2.0 是当前 Coding Agent 评测的标准基准之一，涵盖 89 个任务（ML、Debugging、Biology 等领域）。LangChain 用默认 Prompt + 标准工具/middleware 的基线配置在 GPT-5.2-Codex 上得分 52.8%，刚进入 Top 30。

通过 LangSmith Traces 分析失败案例，他们发现了一个一致的失败模式：

> **Agent 写完代码 → 重新读一遍自己的代码 → 确认「看起来 OK」 → 停止执行。**

模型自我感觉良好，但没有实际运行测试。这是 Coding Agent 最常见的可靠性瓶颈——模型不知道自己不知道。

Build verification（构建验证）被 LangChain 视为最关键的 harness 改进方向之一。解决这个问题有两条正交路径：Prompting（告诉模型要验证）和 Middleware（强制模型在退出前执行验证）。两者结合才是完整解法。

---

## 二、Build-Verify-Fix 闭环：让模型不只是「写完」

### 2.1 验证为什么不是自然发生的

推理模型有天然的「第一个合理答案偏见」——一旦产出了一个看起来合理的方案，模型倾向于接受它，而不是重新审视。人类开发者通过运行测试、对比输出和任务要求来验证，但模型没有内置这个循环。

LangChain 在 System Prompt 中添加了分阶段指导：

**Planning & Discovery**：阅读任务规格，扫描代码库，基于任务要求和验证方式构建初始计划。

**Build**：实现计划时要有验证意识。编写测试（如果不存在），覆盖正常路径和边界情况。

**Verify**：运行测试，阅读完整输出，对比任务要求而非自己的代码。

**Fix**：分析任何错误，重读原始规格，修复问题。

这是 Prompt 层的设计。但仅有 Prompting 不够——模型在退出执行循环前需要一个强制触发点。

### 2.2 PreCompletionChecklistMiddleware：退出前的强制检查点

LangChain 实现了一个 `PreCompletionChecklistMiddleware`，它拦截 Agent 的退出行为，在 Agent 即将提交结果前强制注入一次验证提醒。

这个 Middleware 的设计逻辑来自一个观察：即使 Prompt 里明确要求验证，模型也可能在执行后期「忘记」或跳过这步——尤其在时间压力下。通过 Middleware 拦截，可以保证验证步骤在退出前被触发，而不是依赖模型自行想起来。

LangChain 工程师将其类比为 Ralph Wiggum Loop（来自一个开发者命名的梗）：一个 hook 强制 Agent 在 exit 事件上继续执行验证，而不是直接退出。

这是一种确定性保证——不是「告诉模型要验证」，而是「确保模型在退出前一定验证过」。这两者的区别在 Harness Engineering 中至关重要：Prompt 是软约束，Middleware 是硬约束。

---

## 三、LoopDetectionMiddleware：防止 Doom Loop

Coding Agent 的第二个常见失败模式是 Doom Loop（末日循环）：Agent 对同一文件反复做微小变更（同一行代码改 10+ 次），而不改变整体方向。

Doom Loop 的根因是 Agent 过于执着于第一个方案——一旦决定了一条路，就在这条路上微调，而不是重新评估整体策略是否正确。

`LoopDetectionMiddleware` 通过追踪每个文件的编辑次数来实现检测：

```python
# Middleware 伪代码示例（基于 LangChain 实现逻辑）
class LoopDetectionMiddleware:
    def __init__(self, threshold: int = 5):
        self.file_edit_counts = {}
        self.threshold = threshold

    def on_tool_call(self, tool_name: str, input_data: dict):
        # 追踪写文件类工具调用
        if "file" in input_data:
            self.file_edit_counts[input_data["file"]] = \
                self.file_edit_counts.get(input_data["file"], 0) + 1

    def on_after_call(self, response):
        # 超过阈值时注入重新考虑提示
        for file, count in self.file_edit_counts.items():
            if count >= self.threshold:
                return "...consider reconsidering your approach."
```

当同一文件的编辑次数超过阈值（通常 5 次），Middleware 在下一轮推理前注入「重新考虑方法」的提示。这是一个工程解决人类认知偏见的例子——Agent 的 Doom Loop 不是模型缺陷，而是优化目标（make progress）与全局正确性之间的错位。Middleware 修正了这个错位。

LangChain 指出：随着模型能力提升，这类 guardrails 最终可能不再需要，但今天它们是构建可靠 Agent 应用的关键工具。

---

## 四、LocalContextMiddleware：让 Agent 认识自己的环境

### 4.1 环境感知为什么重要

Coding Agent 面临的挑战不仅是「写什么代码」，还有「在什么环境里写」。Terminal Bench 任务自带目录结构、内置工具和严格超时限制。但默认配置的 Agent 不知道这些约束。

典型的环境感知失败案例：
- Agent 不知道 Python 安装在哪里，浪费大量时间搜索
- Agent 不知道当前目录结构，做了不符合项目规范的文件路径假设
- Agent 不知道任务有时间限制，在低优先级工作上花太多时间

### 4.2 LocalContextMiddleware 的实现

`LocalContextMiddleware` 在 Agent 启动时运行：

```python
class LocalContextMiddleware:
    def on_agent_start(self, task_spec: dict):
        # 注入当前工作目录及父子目录结构
        cwd_context = run_bash_command("pwd && find . -maxdepth 3 -type d")
        # 发现系统中可用的 Python 环境
        python_locations = run_bash_command("which python3 && python3 --version")

        return {
            "working_directory": cwd_context,
            "available_tools": python_locations,
            "task_timeout": task_spec.get("timeout", 300)
        }
```

通过主动探测和注入环境上下文，Agent 进入环境后不需要「摸索」，可以直接利用现有资源。

### 4.3 编写可测试代码的指导

另一个 LocalContextMiddleware 注入的内容是「测试意识」Prompting：

- 如果任务规格中提到文件路径，Agent 必须严格遵循（否则自动评分步骤会失败）
- 如果任务提到边界情况，Agent 必须检查边界而非只走 happy path
- Agent 应该假设自己的代码会通过程序化测试（类似代码提交时的 CI 检查）

这个提示的价值在于，它让 Agent 知道自己的产出会被自动化验证，因此会在实现阶段就考虑可测试性，而不是事后补救。

---

## 五、Reasoning Sandwich：推理资源的精准分配

### 5.1 推理计算的权衡

推理模型（GPT-5.2-Codex 有 4 种推理模式：low、medium、high、xhigh）面临一个计算资源分配问题：

- 高推理预算帮助 Agent 更好地理解任务和规划步骤
- 高推理预算也会显著增加 Token 消耗和时间（最高 2x+）
- 任务不同阶段对推理的需求不同

Terminal Bench 的超时限制创造了一个显式的权衡：更多推理时间能带来更好的规划，但也可能超时导致零分。

### 5.2 xhigh-high-xhigh Sandwich

LangChain 测试了多种推理预算分配方式，发现了一个「三明治」策略效果最好：

```
Planning（高推理）→ Implementation（中推理）→ Verification（高推理）
```

具体结果：
- 全程 xhigh：53.9%（超时过多）
- 高推理综合策略：63.6%（无显著差异，简单策略即可）
- Reasoning Sandwich + 其他优化：66.5%

推理资源的分配不是越高越好——关键是「规划」和「验证」阶段需要高推理（理解任务规格、检测错误），而「实现」阶段用中等推理即可。

这与 AI 推理模型的自适应推理（Adaptive Thinking）趋势一致：让模型自己决定何时多推理、何时少推理。在多层 Harness 中，这意味着可以用一个大模型做规划，用一个小模型做执行——这是推理资源路由在 Harness 层的具体实现。

---

## 六、Trace Analyzer Skill：将失败案例转化为改进信号

### 6.1 为什么需要 Trace Analysis 自动化

手动分析每个失败案例是不可扩展的。LangChain 的 Deep Agents CLI 在 Terminal Bench 2.0 上跑了大量实验，每次实验都生成完整的 Traces。如果工程师手动分析每个失败 Trace，迭代速度会严重受限。

LangChain 将 Trace Analysis 做成了一个可复用的 **Agent Skill**：

1. 从 LangSmith 获取实验 Traces
2. 启动并行 Error Analysis Agents，每个分析一个失败案例
3. 主 Agent 综合各 Agent 的发现，形成 Harness 改进建议
4. 人工review建议（可选但推荐），决定是否采纳

```python
# TraceAnalyzerSkill 工作流（伪代码）
class TraceAnalyzerSkill:
    def analyze(self, experiment_traces: list[Trace]):
        # Step 1: 并行分析每个失败 Trace
        error_agents = [
            ErrorAnalysisAgent(trace=t)
            for t in experiment_traces if not t.passed
        ]
        findings = parallel_run(error_agents)

        # Step 2: 主 Agent 综合
        synthesis = main_agent.synthesize(findings)

        # Step 3: 生成 Harness 改动建议
        return synthesis.to_harness_changes()
```

这个 Skill 的价值在于它将 ML 中 Boosting 的概念引入 Harness Engineering：每次实验的失败案例提供「梯度信号」，下一个实验的 Harness 改进针对这些具体失败。

LangChain 计划将这个 Skill 公开发布，作为 Prompt 优化的通用工具。

### 6.2 什么样的 Harness 改动是有效的

基于 Trace Analysis，LangChain 发现以下类型的 Harness 改动最有效：

| 改动类型 | 具体案例 |
|---------|---------|
| Prompt 更新 | 「当多个文件有依赖关系时，先 offload 信息到文件系统，再重新聚合」 |
| 工具描述更新 | 新工具的使用方式和组合方式需要明确示例 |
| Middleware 规则 | LoopDetection 阈值调整、PreCompletion 检查清单细化 |
| 环境注入 | Python 路径发现、测试命令注入 |

---

## 七、工程建议：从 LangChain 的 13.7 点中学到什么

### 7.1 Context Engineering on Behalf of Agents

模型今天还不太擅长自主发现和使用环境信息。Harness 工程师的核心职责是替 Agent 做好上下文准备：

- 目录结构和可用工具 → 通过 Middleware 主动注入
- 编码规范和测试标准 → 通过 System Prompt 嵌入
- 时间约束和优先级 → 通过 Middleware 在执行过程中注入

Context 是可工程的，模型只是消费者。

### 7.2 Self-Verification 的确定性保证

仅靠 Prompt 要求验证是软约束。在关键路径上用 Middleware 实现强制验证：

- PreCompletionChecklistMiddleware：确保退出前一定运行验证
- LoopDetectionMiddleware：确保不在错误方向上过度投入

随着模型能力提升，这些 guardrails 会变得不必要——但今天它们是生产级系统的必备组件。

### 7.3 Tailor Harnesses to Models

同一个 Harness 在不同模型上表现不同。GPT-5.2-Codex 的 Reasoning Sandwich 策略在其他模型上不一定是最优的。

LangChain 正在构建模型画像（Model Profiles）——用更大评测集测试多个模型在同一个 Harness 上的表现，产出跨模型对比数据。这将成为未来选择模型 + Harness 组合的基础数据。

### 7.4 Tracing as Infrastructure

LangSmith Traces 不仅是调试工具，更是 Harness 改进的数据管道。每次运行都生成结构化的输入输出记录，这些记录可以被分析、聚类、转化为改进信号。

将 Tracing 视为 Harness 的「传感器」而非「日志系统」——它是改进循环的数据来源。

---

## 八、与其他 Harness Engineering 工作的关系

本文描述的 Middleware 设计与 Better Harness（2026-04-08）中的 Eval-Driven Optimization Loop 形成互补：

- **Better Harness** 关注 Harness 改进的闭环框架（如何用 Evals 作为梯度信号持续优化）
- **本文** 关注具体的 Middleware 组件和自验证机制（闭环中每个组件如何实现）

两者结合构成了 Harness Engineering 的完整方法论：数据驱动地发现失败模式 → 通过 Middleware 修复或防止失败 → 用 Evals 验证改进效果 → 循环迭代。

---

## 参考文献

- [Improving Deep Agents with harness engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/) — LangChain Engineering Blog（2026-04），一手来源，Terminal Bench 2.0 实验完整数据
- [Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://blog.langchain.com/better-harness-a-recipe-for-harness-hill-climbing-with-evals/) — LangChain Engineering Blog（2026-04），Eval-Driven 优化框架
- [Terminal Bench 2.0 Leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.0) — 评测基准，验证 52.8 → 66.5 的分数真实性
- [Ralph Wiggum Loop](https://ghuntley.com/loop/) — 退出前强制继续执行模式的命名来源
- [Anthropic Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) — 自适应推理模型参考
- [deepagents-cli GitHub](https://github.com/langchain-ai/deepagents/tree/main/libs/cli) — LangChain 官方 Coding Agent CLI 实现
