# MetaGPT：用 SOP 重新定义多 Agent 协作

> **核心命题**：大多数 multi-agent framework 解决的是「如何让多个 Agent 通信」，MetaGPT 解决的是「如何让多个 Agent 像一家软件公司一样协作」——通过把 SOP（标准作业程序）编码成 Agent 的协作协议，而不是用消息队列或中央调度器。

## 一、问题：多 Agent 框架缺失了什么

当前主流 multi-agent 框架（LangGraph、CrewAI、AutoGen）解决的是**架构问题**：如何定义 Agent、如何路由消息、如何管理状态。

但它们没有解决**组织问题**：一家软件公司不只是有一堆工程师，还有一套 SOP——产品经理写需求，架构师设计，工程师实现，PM 审核。没有这套流程，只有一堆 Agent 就是一盘散沙。

**Core philosophy** from README：

> "Code = SOP(Team). We materialize SOP and apply it to teams composed of LLMs."

MetaGPT 把这个理念落了地：输入一行需求，输出一个软件公司需要的全部工件——用户故事、竞品分析、需求文档、数据结构、API 设计、代码实现。

## 二、架构：Role-based 的软件公司

MetaGPT 内部包含一组预定义 Role：

| Role | 职责 | 输出 |
|------|------|------|
| **Product Manager** | 需求分析、用户故事 | PRD |
| **Architect** | 系统设计、技术选型 | 架构文档、数据结构 |
| **Project Manager** | 任务分解、进度管理 | Sprint 计划 |
| **Engineer** | 代码实现 | 可运行代码 |
| **Reviewer** | 代码审核 | Review 意见 |

每个 Role 有自己的 System Prompt 和 SOP。当用户输入一个需求时，MetaGPT 按照软件公司的实际流程依次激活各个 Role，形成**流水线式的协作**。

这与 Anthropic 实验中「Agent 自己判断下一个做什么」的**去中心化自组织**完全不同——MetaGPT 是**显式流水线**，每个 Role 的激活顺序是预先定义的。

## 三、两种协调哲学的对比

MetaGPT 的 SOP-based 协调 vs Anthropic 的 Git-based 去中心化同步：

| 维度 | MetaGPT（显式流水线）| Anthropic（去中心化同步）|
|------|---------------------|-------------------------|
| **协调机制** | 预定义 Role 流水线 | 锁文件 + Git merge |
| **决策方式** | SOP 决定激活顺序 | Agent 自己判断下一步 |
| **冲突处理** | 流水线顺序天然避免冲突 | 冲突通过 merge 解决 |
| **适用场景** | 流程明确、结构化任务 | 探索性强、无固定流程 |
| **扩展方式** | 新增 Role/修改 SOP | 新增专业 Agent |
| **复杂度** | SOP 设计成本高 | Git 原语足够简单 |

**笔者认为**：两者不是竞争关系，而是**适用场景互补**。对于「写一个 2048 游戏」这种需求，MetaGPT 的流水线足够高效；但对于「从零构建一个 C 编译器」这种探索性任务，Anthropic 的去中心化模式更能适应不确定性。

## 四、SPO 与 AOT：两篇论文的工程实践

2025 年 2 月，MetaGPT 团队发布了两篇论文：

**SPO (Structured Planning and Orchestration)**：将结构化规划引入 multi-agent 协作，让 Agent 在行动前先生成可验证的计划，通过计划驱动协作而非单纯的消息传递。

**AOT (Agentic Workflow Termination)**：解决 multi-agent 系统的终止判定问题——当多个 Agent 并行工作时，如何判断「任务完成了」？AOT 提出了基于条件触发的终止协议。

这两篇论文的工程含义是：MetaGPT 不只是一个框架，它在探索**multi-agent 系统的理论基础**，包括规划、协作和终止条件这三个核心问题。

## 五、AFlow：ICLR 2025 Oral

2025 年 1 月，MetaGPT 团队关于 AFlow 的论文被 ICLR 2025 接受为 oral presentation（top 1.8%），在 LLM-based Agent 类别排名第二。

AFlow 研究的是**如何自动化生成 agentic workflow**——不是手动定义 Agent 和协作流程，而是让系统根据任务目标自动推断出最优的工作流结构。

这是 MetaGPT「Code = SOP(Team)」理念的再进一步：不只是「把 SOP 应用到 Agent 团队」，而是「让 Agent 自动生成 SOP」。

## 六、快速上手

```bash
# 安装
pip install --upgrade metagpt

# 一行需求创建完整项目
metagpt "Create a 2048 game"

# 或作为 Library 使用
from metagpt.software_company import generate_repo
repo = generate_repo("Create a 2048 game")
print(repo)
```

```python
# Data Interpreter 模式：代码 + 数据分析
import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter

async def main():
    di = DataInterpreter()
    await di.run("Run data analysis on sklearn Iris dataset, include a plot")

asyncio.run(main())
```

## 七、工程价值

**适合使用 MetaGPT 的场景**：
- 需求明确、结构化程度高的任务（如「创建一个 CRUD 应用」）
- 需要多人协作流程的项目（PRD → 架构 → 实现 → 审核）
- 快速原型验证（一行需求 → 完整项目骨架）

**不适合的场景**：
- 探索性强、没有明确流程的任务
- 需要极致性能和资源效率的场景
- 需要精细控制 Agent 决策逻辑的场景

**与 Anthropic building-c-compiler 实验的关联**：Anthropic 证明了「去中心化同步 + 锁文件」可以完成复杂软件构建，MetaGPT 证明了「显式 SOP 流水线」同样可以。两者共同指向一个结论：**multi-agent 协调没有唯一正确答案，不同任务需要不同的协调模式**。

---

> **引用来源**：README 和架构来自 [github.com/FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)，2025-03 更新。Paper：[SPO](https://arxiv.org/pdf/2502.06855)、[AOT](https://arxiv.org/pdf/2502.12018)、[AFlow](https://openreview.net/forum?id=z5uVAKwmjf)。