# Anthropic Engineering: Demystifying Evals for AI Agents——构建可靠 Agent 评测体系的系统性框架

**来源**: [Anthropic Engineering Blog - Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)  
**作者**: Anthropic Team  
**分类**: evaluation

---

## 核心论点

评测（Evaluations）是 AI Agent 生命周期管理的核心基础设施。没有评测，团队只能「凭直觉判断」——改动一个模块，不知道是否破坏了另一个功能；上线新模型，不知道能力边界在哪里。Anthropic 在本文中系统性地拆解了 Agent 评测的设计框架，核心观点是：

> **Agent 的评测复杂度远高于单轮 LLM 评测，但存在已被验证的解决路径——关键是选择正确的 Grader 类型组合。**

---

## Agent 评测的特殊性：从单轮到多轮

传统的 LLM 评测是单轮的：给一个输入，等待一个输出，对比标准答案。Agent 评测则完全不同：

- **多轮交互**：Agent 调用工具、修改状态、基于中间结果自适应
- **状态累积**：错误会传播和叠加，一步错步步错
- **创造性绕过**：前沿模型能发现评测本身的漏洞并「绕过」而非「解决」问题
  - 典型案例：Opus 4.5 在 τ2-bench 航班预订任务中，发现了政策漏洞并绕过了它——按评测标准「失败」，但实际给用户提供了更好的解决方案

这使得 Agent 评测的核心挑战是：**如何在动态、多轮、非确定性的执行过程中，准确评估「成功」的定义**。

---

## 评测的核心组件

Anthropic 给出了一套精确的术语体系：

| 组件 | 定义 |
|------|------|
| **Task** | 单个测试用例，有确定的输入和成功标准 |
| **Trial** | 一次执行（因为模型输出有随机性，通常跑多次取平均） |
| **Grader** | 评分逻辑，一个 Task 可以有多个 Grader |
| **Transcript** | 完整执行记录（API 调用、工具返回、推理过程） |
| **Outcome** | 环境最终状态（而非 Agent 的口头回复） |
| **Eval Harness** | 运行评测的基础设施（并发执行、记录、评分、聚合） |
| **Agent Harness** | 使模型能够作为 Agent 行动的系统（如 Claude Code） |

**关键区分**：Eval Harness 测的是「Agent 加模型的联合表现」，而非纯模型能力。

---

## Grader 类型：三种方法的权衡

这是本文最实用的部分。Agent 评测有且仅有三种 Grader 类型，各有适用场景：

### 1. Code-based Graders（代码级评分）

**方法**：
- 精确匹配（exact/regex/fuzzy）
- 二值测试（fail-to-pass / pass-to-pass）
- 静态分析（lint、类型检查、安全扫描）
- 结果验证（数据库状态检查）
- 工具调用验证（是否调用了预期的工具及参数）

**优点**：快速、便宜、客观、可复现、易调试  
**缺点**：对有效变体敏感，容易产生误判（拒绝正确但形式不同的答案）

### 2. Model-based Graders（模型评分）

**方法**：
- Rubric-based scoring（基于评分标准的打分）
- Natural language assertions（自然语言断言）
- Pairwise comparison（成对比较）
- Reference-based evaluation（参考答案评估）
- Multi-judge consensus（多裁判共识）

**优点**：灵活、可扩展、能处理开放性任务  
**缺点**：非确定性、成本更高、需要与人类评分对齐校准

### 3. Human Graders（人工评分）

**方法**：
- SME（领域专家）审核
- 众包判断
- 抽样检查
- A/B 测试
- 标注一致性检验

**优点**：黄金标准质量，与真实用户判断一致  
**缺点**：贵、慢、需要专家参与

**实践建议**：通常组合使用——代码级评分验证正确性，模型评分评估代码质量和行为，人工评分作为校准基准。

---

## Capability Evals vs. Regression Evals

这是评测目标维度的核心划分：

| 类型 | 问题 | Pass Rate 目标 | 作用 |
|------|------|---------------|------|
| **Capability（能力）** | 「这个 Agent 能做到 X 吗？」 | 起始低分，给团队一个「需要攀登的山峰」 | 发现短板、指导改进方向 |
| **Regression（回归）** | 「这个 Agent 还能可靠地做到 Y 吗？」 | 接近 100%，守护已达成的能力 | 防止能力退化、尽早发现引入的问题 |

随着 Agent 成熟，Capability Eval 中 pass rate 高的任务可以「毕业」成为 Regression Eval——从「我们能做到吗」转变为「我们还能持续做到吗」。

---

## 四类 Agent 的评测方法

### Coding Agents

**核心挑战**：软件评估天然适合自动化，但代码风格和行为评估需要模型参与。

**典型方案**（以修复认证绕过漏洞为例）：
```yaml
task:
  graders:
    - type: deterministic_tests    # 单元测试验证
      required: [test_empty_pw_rejected.py]
    - type: llm_rubric             # 代码质量评分
      rubric: prompts/code_quality.md
    - type: static_analysis        # 静态分析
      commands: [ruff, mypy, bandit]
    - type: state_check           # 环境状态验证
      expect: {security_logs: {event_type: "auth_blocked"}}
    - type: tool_calls            # 工具调用验证
      required: [{tool: read_file}, {tool: edit_file}, {tool: run_tests}]
  tracked_metrics:
    - n_turns, n_toolcalls, n_total_tokens
```

**业界标杆**：SWE-bench Verified（GitHub Issues → 测试驱动验证）、Terminal-Bench（端到端技术任务）。

### Conversational Agents

**核心挑战**：交互质量本身就是评测对象，不只是结果正确。

**关键方法**：
- 第二 LLM 模拟用户（因为需要多轮对话）
- 多维成功标准：任务完成（状态检查）+ 交互轮数约束 + 语气适当性（LLM rubric）
- τ-Bench / τ2-Bench 是典型基准，模拟零售支持、航班预订等场景

### Research Agents

**核心挑战**：研究质量是主观的，「全面」「有据」「正确」因场景而异。

**关键方法**：
- Groundness checks：声明是否被来源支撑
- Coverage checks：关键事实是否覆盖
- Source quality checks：来源是否权威
- LLM rubric 需频繁与专家人工判断校准

### Computer Use Agents

**核心挑战**：通过 GUI 与软件交互，需要真实或沙盒环境。

**典型方案**：
- WebArena：URL 和页面状态检查 + 后端状态验证
- OSWorld：文件系统状态、应用配置、数据库内容、UI 元素属性检查

---

## 笔者的判断与启示

### 1. Grader 组合比单一 Grader 更可靠

笔者认为，**Code-based Grader 是基线，Model-based Grader 是扩展，Human Grader 是校准**。三者的组合不是冗余，而是互补——静态验证确保「做对了」，模型评分评估「做得好不好」，人工校准确保「评估本身是对的」。

### 2. Eval 是团队沟通的高带宽渠道

Anthropic 指出，Eval 可以成为产品团队和研究团队之间最高效的沟通渠道——将「好的 Agent 行为」具象化为可量化的指标，使研究者有明确的优化目标。这是 Eval 的战略价值，而非仅仅是质量保障手段。

### 3. Agentic 的代价是评测复杂度上升

「自主性」「灵活性」「多轮交互」这些 Agent 特性，在带来能力提升的同时，使得评测复杂度呈指数级上升。这不是可避免的代价，而是 Agent 架构的本质约束。**笔者认为，在设计 Agent 系统时，应同时设计评测体系，而非事后补充**。

### 4. 评测不是一次性设计

SWEBench 从 40% 到 >80% 的进步，揭示了一个关键事实：评测需要与 AI 能力进化保持同步迭代。当 pass rate 接近 100% 时，该评测就已经失去了区分能力，需要升级或替换。这要求团队将评测视为「活的基础设施」而非「静态测试集」。

---

## 总结

Anthropic 的这篇文章提供了一个系统性的 Agent 评测框架，核心是：

1. **明确术语**：Task / Trial / Grader / Transcript / Outcome / Harness 的区分
2. **选择 Grader**：Code-based 用于确定性验证，Model-based 用于开放性评估，Human 用于校准
3. **区分目标**：Capability Eval 发现短板，Regression Eval 防止退化
4. **类型适配**：Coding / Conversational / Research / Computer Use 四类 Agent 各有适配的评测方案

**笔者的核心判断**：评测是 Agent 工程化的基础设施，其重要性不亚于模型选择和架构设计。没有可靠评测的 Agent 团队，在规模化阶段必然陷入「改哪里都像在猜」的困境。

---

*作者：Anthropic Engineering Team*  
*原文：[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)*