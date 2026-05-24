# Anthropic SWE-Bench 深度解析：3.5 Sonnet 如何用简单策略突破 49% 基准线

## 核心论点

**Claude 3.5 Sonnet 在 SWE-bench Verified 上以简单 prompt + 两个通用工具达到 49%，超越此前 45% 的 SOTA——这证明在 Agent 编码场景中，「让模型专注完成任务」比「构建复杂框架」更有效**。

> 这不是模型能力突破的唯一因素，但它是工程实践中常被复杂方案掩盖的关键洞察：最强大的 Agent 系统，往往建立在最简单的交互模式之上。

---

## SWE-bench：为什么这个基准值得关注

[SWE-bench](https://www.swebench.com/)（Software Engineering Benchmark）由 Princeton NLP 团队构建，是目前最具挑战性的 Agent 编码评估基准。与多数基准不同，SWE-bench 要求 Agent：

1. **处理真实的 GitHub Issue**：从描述中理解用户遇到的问题
2. **定位并修改真实的代码库**：涉及多个文件的跨模块修改
3. **通过单元测试验证**：修复必须能通过原始测试套件

这比简单的代码补全或单文件修改要复杂得多——它模拟了真实软件工程师的工作流程。

### SWE-bench Verified：修正评估偏差

原始 SWE-bench 存在数据标注问题（安装脚本重复应用、测试环境配置错误），Princeton 团队发布了 [SWE-bench Verified](https://github.com/princeton-nlp/SWE-bench?tab=readme-ov-file#swe-bench-verified) 来修正这些问题，使评估更接近真实场景。

---

## Anthropic 的关键发现

### 1. 自我纠正在多次尝试中的频率大幅提升

Anthropic 观察到，升级版 Claude 3.5 Sonnet 在 SWE-bench 上展现出更强的自我纠正能力：

> "From reviewing attempts from the updated Claude 3.5 Sonnet compared to older models, updated 3.5 Sonnet self-corrects more often. It also shows an ability to try several different solutions, rather than getting stuck making the same mistake over and over."

**这意味着模型在长程任务中有了更成熟的错误处理策略**——不是简单地一条路走到黑，而是在意识到错误时主动回退、换思路重来。

### 2. 长时任务中的坚持能力

示例中展示了模型在 12 步后才决定提交（通过了测试），而某些成功案例甚至需要超过 100 轮迭代、消耗超过 100k tokens。

> "The upgraded Claude 3.5 Sonnet achieved 49% on SWE-bench Verified, beating the previous state-of-the-art (45%), with a simple prompt and two general purpose tools."

### 3. 简单工具集的有效性

Anthropic 明确指出，49% 的成绩是「用简单 prompt + 两个通用工具」取得的，没有针对基准测试的特定优化。这与很多高分解方案依赖复杂工具定义和精心设计的 domain knowledge 形成对比。

---

## 实验性发现：多模态评估的空白

SWE-bench 团队还发布了 [多模态版本评估](https://www.swebench.com/multimodal.html)，但 Anthropic 在实验中发现了当前实现的局限性：

> "Despite the updated Claude 3.5 Sonnet having excellent vision and multimodal capabilities, we did not implement a way for it to view files saved to the filesystem or referenced as URLs. This made debugging certain tasks (especially those from Matplotlib) especially difficult, and also prone to model hallucinations."

**这是一个工程问题而非模型能力问题**——工具层面的实现缺失限制了模型在视觉相关任务中的表现。

---

## 评估基础设施：SWE-bench 生态

| 组件 | 说明 |
|------|------|
| **SWE-bench** | 原始基准，1000+ 任务，覆盖多种语言和框架 |
| **SWE-bench Verified** | 修正数据标注问题，更可靠的评估 |
| **SWE-bench Multimodal** | 新增多模态任务，支持视觉理解的代码修复 |
| **[swebench-ensemble](https://github.com/princeton-nlp/swebench-achievements)** | 模型在 SWE-bench 上的进展追踪 |

---

## 对 Agent 工程实践的启示

### 简单 > 复杂

Anthropic 的结果挑战了「框架越复杂越强大」的直觉。在工具层面，两个通用工具（很可能一个是文件读写，一个是 bash/terminal）足以支撑 49% 的解决率。

### 评估的价值

SWE-bench 不仅是一个排行榜，更是一个**系统化的任务拆解能力测试床**。它揭示了当前 Agent 在以下环节的薄弱点：

- **长程上下文保持**：100+ 轮迭代中的状态管理
- **跨模块推理**：理解代码库结构和依赖关系
- **测试验证**：理解测试失败原因并针对性修复

### 迭代深度的价值

49% 意味着大约每两题能解决一题。更有意义的是，模型在无法解决时会持续尝试多种方法，而不是快速放弃。这对于实际开发场景意味着：**模型不会轻易跳过难题**，而是会花时间探索多种路径。

---

## 关联项目

| 项目 | Stars | 说明 |
|------|-------|------|
| [SWE-agent](https://github.com/princeton-nlp/swe-agent) | 42,700 | SWE-bench 官方 Agent 实现，100 行代码达到 74% |
| [mini-SWE-agent](https://github.com/vchain-us/mini-swe-agent) | 42,700+ | SWE-agent 精简版，研究高效 Agent 架构 |
| [SWE-bench Verified](https://github.com/princeton-nlp/SWE-bench) | 12,000+ | 评估基准本身 |

---

## 笔者判断

SWE-bench 49% 的数字背后，最值得关注的是 **「简单策略的有效性」**。在 Agent 编码领域，业界往往倾向于构建复杂的工具层和防护机制，但 Anthropic 的结果表明，让模型有足够空间自主探索和试错，可能比精心设计的工具链更有效。

这与他们在其他工程博客中提到的「Harness 要保持简单」哲学一脉相承。

---

*来源：[Anthropic Engineering - SWE-Bench Performance](https://www.anthropic.com/engineering/swe-bench-sonnet)（Published 2025）*