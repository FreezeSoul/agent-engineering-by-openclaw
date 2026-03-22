# GAIA & OSWorld：Agent 评测基准的 2026 新纪元

> GPT-5/o3 在 GAIA 达到 90.37%，评测基准正在被"解决"

---

## 一、背景：为什么需要专门的多模态 Agent 评测

传统 NLP 评测（BERT-style准确率、GLUE分数）只能衡量模型的**知识输出**，无法评估 Agent 的**行动能力**。

Agent 需要评测的核心能力：
- 在真实环境中**规划**多步任务
- 调用**工具**（搜索、代码执行、文件操作）
- 根据**反馈**调整策略
- 完成**端到端**任务

这催生了一批专门的 Agent 评测基准。

---

## 二、GAIA：通用 AI 助手评测

### 什么是 GAIA

GAIA（General AI Assistants benchmark）由 HuggingFace 主导，评测 AI 助手在真实世界任务中的表现。

**特点**：
- 涵盖网页浏览、代码执行、数据分析、多轮对话
- 任务来自真实用户场景
- 有可验证的最终答案

### 2026 年最新结果

| 模型 | GAIA 得分 | 日期 |
|------|----------|------|
| GPT-5 / o3 | **90.37%** | 2026 |
| Claude 4.5 | ~85% | 2026 |
| Gemini Ultra 2 | ~82% | 2026 |
| GPT-4o | ~70% | 2025 |

> GAIA 基准正在被接近"解决"——顶级模型已超过 90%，这意味着该基准的区分度正在下降。

### 核心洞察

**"Agentic Singularity"论调出现**：当基准达到 90%+，意味着通用 AI 助手在 GAIA 设定的任务类型上已超越普通人类。

但需注意：
- GAIA 主要测试**信息整合**类任务（搜索、总结、问答）
- 尚不涵盖复杂的**软件工程**或**物理操作**任务

---

## 三、SWE-bench：软件工程 Agent 评测

### 什么是 SWE-bench

SWE-bench 评测 AI Agent 解决真实 GitHub Issue 的能力——从问题理解到代码修改到测试验证。

**2026 年最新数据**：

| 模型 | SWE-bench Full | SWE-bench Lite |
|------|---------------|----------------|
| Claude 4.5 | **74.4%** | ~88% |
| GPT-5 | 73.8% | ~87% |
| GPT-4o | ~50% | ~70% |

### 意义

74% 的 SWE-bench 解决率意味着：
- Claude 4.5 可以**独立解决近四分之三的真实 GitHub Bug**
- 正在接近人类软件工程师的平均水平
- 成为判断"AI 程序员"能力的行业标准

---

## 四、OSWorld：多模态操作系统 Agent

### 什么是 OSWorld

OSWorld 评测 Agent 操作**真实计算机桌面环境**的能力：

```
369 个真实计算机任务，涵盖：
- 桌面 GUI 操作（点击、拖拽、输入）
- 跨应用工作流（浏览器→文档→邮件）
- 文件系统操作
- 代码编辑和运行
```

**核心指标**：

| 指标 | 含义 |
|------|------|
| Screen Understanding | 正确识别屏幕上的 UI 元素 |
| Operation Accuracy | 操作执行正确（点击正确按钮等） |
| Task Completion Rate | 完整任务达成率 |

### GAIA2：下一代基准

2026 年新发布的 **GAIA2** 引入：
- **异步环境**中的 Agent 评测
- **动态验证**的任务设计
- 弥补原始 GAIA 在时间维度上的不足

---

## 五、评测基准全景对比

| 基准 | 核心能力 | 难度 | 最高得分 | 趋势 |
|------|---------|------|---------|------|
| **GAIA** | 通用助手 | 中 | 90.37% | 接近饱和 |
| **SWE-bench** | 代码修复 | 高 | 74.4% | 快速提升 |
| **OSWorld** | 桌面操作 | 很高 | 约 30-40% | 仍具挑战 |
| **WebArena** | 网页操作 | 高 | 约 40% | 稳步提升 |
| **WebVoyager** | 网页导航 | 中 | 约 65% | 提升中 |
| **BrowseComp** | 复杂搜索 | 高 | 约 60% | 提升中 |

---

## 六、关键洞察：评测基准的意义与局限

### 为什么重要

1. **可量化的进步**：让 Agent 能力提升有据可循
2. **选型依据**：企业可根据基准选择合适模型
3. **问题诊断**：哪些能力是短板，一目了然

### 局限

1. **饱和问题**：GAIA 达到 90%+ 后，对顶级模型的区分度下降
2. **任务偏向**：基准只能覆盖可自动验证的任务
3. **泛化差距**：高分不代表在实际生产环境中同样出色
4. **速度 vs 质量**：基准通常不测量效率（成本、时间）

### "Agentic Coding Trends Report" 揭示的规律

Anthropic 2026 年发布的 Agentic Coding Trends Report 指出：

> 评测基准是代理指标，真正的生产Agent需要：更长的自主运行时间、更少的人工介入、更强的错误恢复能力。

---

## 七、实战建议

### 如何选择评测基准

```
场景 → 基准选择

代码任务 → SWE-bench
网页浏览 → WebVoyager / WebArena  
桌面操作 → OSWorld
通用助手 → GAIA
中文场景 → 需自建基准
```

### 建立内部基准的要素

1. **任务多样性**：覆盖核心场景
2. **可验证性**：有明确的完成标准
3. **定期更新**：避免过拟合
4. **成本追踪**：测量 token 消耗和运行时间

---

## 八、参考资料

- [GAIA Leaderboard](https://leaderboard.steel.dev/results)（Steel.dev AI Agent Benchmark Index）
- [SWE-bench Official](https://www.swebench.com/)
- [OSWorld Paper](https://arxiv.org/abs/2308.14205)
- [Reddit: The 2026 Agentic Singularity - GAIA 90%+](https://www.reddit.com/r/aiagents/comments/1qdj16n/the_2026_agentic_singularity_gaia_90_swebench_74/)
- [O-Mega Guide: AI Computer-Use Benchmarks 2025-2026](https://o-mega.ai/articles/the-2025-2026-guide-to-ai-computer-use-benchmarks-and-top-ai-agents)
- [Anthropic 2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

---

*最后更新：2026-03-22 | 由 OpenClaw 整理*
