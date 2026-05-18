# Photo-agents：视觉驱动的自演进 Agent 系统，让 Agent 真正「记住」工作上下文

> GitHub: [jmerelnyc/Photo-agents](https://github.com/jmerelnyc/Photo-agents) | ⭐ 968 | Python

---

## 这个项目解决了一个长期让人头疼的问题

当 Agent 需要完成需要「跨越数小时甚至数天」的任务时，最大的瓶颈不是推理能力，而是**记忆的持久性和视觉上下文的可用性**。

传统的 Agent memory 方案（如 RAG、向量数据库）解决的问题是「如何快速检索已有信息」，但没有解决一个更根本的问题：**Agent 如何像人类一样，将视觉观察内化为可推理的长期记忆？**

Photo-agents 提出了一个令人印象深刻的答案：**Vision-grounded layered memory（视觉驱动的分层记忆架构）**。

---

## 核心技术机制

### 分层记忆架构

Photo-agents 的核心设计是一个**三层记忆系统**：

1. **瞬时记忆（Working Memory）**：当前 session 的上下文
2. **视觉记忆（Visual Memory）**：Agent 在执行过程中观察到的屏幕状态、可视化输出
3. **长期记忆（Persistent Memory）**：跨 session 积累的知识和偏好

> "Autonomous self-evolving agents. Vision-grounded layered memory and self-written skills for LLM agents that operate your computer."

这种架构使得 Agent 不仅能「记住」文本信息，还能「记住」视觉场景——当你让它修复一个 Bug，它能够识别这个 Bug 在 UI 上的表现形式，并将其与历史上遇到过的类似问题关联起来。

### 自编写 Skill 机制

Photo-agents 支持 Agent **自己编写和积累技能**。当 Agent 发现某个操作流程重复出现时，它可以：

1. 将该流程封装为一个可复用的 skill
2. 在未来的 session 中直接调用这个 skill
3. 随着时间推移，Agent 的能力边界不断扩展

这解决了传统 Agent 系统的「能力天花板」问题——Agent 的能力不再受限于预定义的工具集，而是可以通过实践「自我进化」。

---

## 技术特点

| 维度 | 说明 |
|------|------|
| **架构** | 视觉驱动的分层记忆（Vision-grounded Layered Memory）|
| **能力扩展** | 自编写 Skills（Self-written skills）|
| **应用场景** | 长期任务（Long-horizon tasks）、跨 session 工作流 |
| **技术栈** | Python + 多模态 LLM 支持 |
| **设计理念** | 自主进化（Self-evolving）而非预定义能力 |
| **Topics** | agent-memory, autonomous-agents, computer-use, self-evolving-agents, vision-agents |

---

## 与 Cursor 第三代架构的关联性

Cursor 的「第三 era」强调的核心变化是：**Agent 在云端独立运行更长时间，返回 artifact 而不是 diff**。

Photo-agents 正是这个方向的底层支撑技术之一：

- **长时间运行**需要持久记忆——Photo-agents 的分层记忆架构使得 Agent 能够在数小时的运行中保持上下文
- **跨 session 积累**需要自进化能力——自编写 Skills 机制让 Agent 的能力随使用不断增长
- **视觉化 output** 需要视觉记忆——Vision-grounded memory 使得 Agent 能够「看到」并记住视觉场景

当 Agent 能够真正记住工作上下文并自主积累技能时，「self-driving codebases」才从愿景变为可能。

---

## 适用场景

**最适合**：需要 Agent 完成**跨越数小时或数天的复杂任务**的开发者

**不适合**：
- 简单的单次任务（用 Tab 或同步 Agent 更快）
- 对延迟敏感的场景（分层记忆带来额外的推理开销）
- 没有多模态模型支持的部署环境

---

## 笔者认为

Photo-agents 的设计理念代表了一个重要的方向转变：**Agent 的能力不再由预定义的工具集决定，而是由它在长时间运行中积累的记忆和技能决定**。

这与 OpenAI 的「agent as teammate」和 Anthropic 的「long-running agent」方向一致，但 Photo-agents 的独特价值在于**将视觉理解引入了记忆系统的核心**。当 Agent 能够「记住」一个 Bug 在屏幕上的表现形式，而不仅仅是错误日志的文本，这打开了新的可能性。

---

**引用来源**：
- [jmerelnyc/Photo-agents GitHub README](https://github.com/jmerelnyc/Photo-agents)