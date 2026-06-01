# 人在循环：Agent 系统的第三层架构

**核心论点**：Human-in-the-Loop（HITL）不是 Agent 的限制，而是扩展部署边界的第三层架构。90/10 自动化比例 + 三层设计（确定性骨干 + 智能推理 + 人类判断）才是生产级 Agent 系统的正确模式。

---

## 被误解的 HITL

大多数人对 Human-in-the-Loop 的理解是：**它意味着 AI 的局限性**。

这是方向性错误。HITL 实际上在**扩展**可部署场景的边界：

| 场景 | 没有 HITL | 有 HITL |
|------|----------|---------|
| 需要 99.9% 准确率 | 停留在 Pilot | 可上线 |
| 需要合规签字 | 风险不可控 | 可审计 |
| 输出需要人工审核 | 难以规模化 | 10% 人工 + 90% 自动 |
| 需要人工介入/退出 | 架构缺失 | 内置 |

CrewAI 称之为 **90/10 规则**：90% 自动化，10% 人类增强。比例因场景而异（有些系统从 30/70 起步），核心是**架构支持双向调节**，而非二选一。

---

## Agent 系统的三层架构

CrewAI 从 20 亿次 Agent 执行中提炼出三层架构：

```
┌─────────────────────────────────────────┐
│  Layer 3: Human Judgment (HITL)         │  ← 新增：人类判断层
│  - 暂停审查 / 监控干预                   │
│  - 精确性 + 问责制                       │
├─────────────────────────────────────────┤
│  Layer 2: Intelligence (LLM/Agent/Crews)│  ← 推理和适应
│  - 规划 / 行动 / 学习                    │
├─────────────────────────────────────────┤
│  Layer 1: Deterministic Backbone (Flows) │  ← 结构与控制
│  - 工作流编排                            │
│  - 确定性执行                            │
└─────────────────────────────────────────┘
```

HITL 是**可选的第三层**，不是替代前两层。它引入人类判断能力和问责机制。

---

## 两种 HITL 模式

| 模式 | 机制 | 适用场景 |
|------|------|---------|
| **Human-in-the-loop** | Agent 暂停，人类审核或编辑后继续 | 精确性要求高、合规签字 |
| **Human-on-the-loop** | 人类监控、调整参数，必要时干预 | 置信度监控、风险防范 |

两种模式都扩展了可部署边界，区别在于**阻断粒度**。

---

## AB InBev：20 亿次执行的实践

AB InBev（全球每三瓶啤酒有一瓶来自他们）是 CrewAI 的企业客户，CTO David Almeida 在 Signal 大会分享：

- **每年 2000 万张工单**通过 HITL 架构处理
- **30% 完全自主**，70% 人机协作（Agent 路由/拉取信息/起草，人类审核）
- **每年 2800 万美元**价值从这个单一场景产生
- AI 每年影响 **300 亿美元决策**

> "AI 不会独立存在。AI 会嵌入我们的技术平台来创造价值。"

这是 Fortune 500 级别的生产级 Agent 架构。

---

## CrewAI Flows 的 HITL 原生支持

CrewAI 开源侧，Flows 现在原生支持 HITL：

```python
from crewai.flows import Flow
from crewai.flows.plugins import human_feedback

class ReviewFlow(Flow):
    @human_feedback
    def review(self):
        # Agent 生成内容后暂停
        # 人类审核 / 修改
        # 工作流继续
        pass
```

一行装饰器实现 Checkpoint 审查机制。

---

## 关联项目

本文与以下项目形成闭环：

- **[CrewAI Flows](https://github.com/crewAIInc/crewAI)**（开源）：HITL 原生支持的编排框架，与本文的「三层架构」直接对应
- **[Kaelio/ktx-ai-data-agents-context](https://github.com/Kaelio/ktx-ai-data-agents-context)**（729 Stars）：数据和分析 Agent 的可执行上下文层，支持 MCP + Skills + Memory，与 HITL 的「人类判断注入」场景互补

---

## 结论

HITL 是 Agent 系统的**第三层架构**，不是补救措施。正确的架构设计：

1. **确定性骨干**（Flows）提供结构控制
2. **智能推理层**（LLM/Agent）提供适应性
3. **人类判断层**（HITL）提供精确性和问责制

AB InBev 的 20 亿次执行验证了这条路线的可行性。**90/10 规则**的启示：与其追求 100% 自动化然后在边缘 case 上失败，不如从设计之初就内置人类介入能力，按需调节自动化比例。

---

**来源**：[A Missing Layer in Agentic Systems?](https://www.crewai.com/blog/a-missing-layer-in-agentic-systems)（CrewAI，January 21, 2026）
