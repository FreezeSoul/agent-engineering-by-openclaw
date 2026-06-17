# GitHub Copilot CLI：Smarter Delegation——量化 Harness 调优的工程实践

> 本文解读来源：GitHub Blog — *[How we made GitHub Copilot CLI more selective about delegation](https://github.blog/ai-and-ml/how-we-made-github-copilot-cli-more-selective-about-delegation/)*（2026-06-12）

---

## 核心问题：Delegation 不是免费的

当一个 Agent 把任务委托给子 Agent 时，这个"委托"不是零成本的握手。每次 handoff 都伴随着协调开销、工具调用次数和等待时间。如果 Agent 过度委托，"帮助"反而会变成摩擦。

这是 Harness 工程里一个长期被忽视的问题：行业关注的是"如何让 Agent 变得更强"，但没有人认真回答"Agent 什么时候不该 delegation"。

Copilot CLI 团队用一次完整的量化调优回答了这个问题。

---

## 一、Delegation 的失效模式

Copilot CLI 团队识别出了 5 类 delegation 失效模式：

| 失效模式 | 描述 |
|---------|------|
| **不必要 handoff** | 主 Agent 能直接完成的任务，委托给子 Agent 后反而更慢 |
| **过度探索** | 子 Agent 重新搜索主 Agent 已经足够了解的代码区域 |
| **重复搜索** | 主 Agent 和子 Agent 对同一区域重复搜索 |
| **顺序委托** | 主 Agent 等待子 Agent 完成，而不是把委托当作并行机会 |
| **失败路径累积** | 子 Agent 遇到文件路径过时、文件迁移、工作区不匹配等问题 |

> 原文引用 1："If an agent delegates too eagerly, the 'help' can become friction."

这些失效模式在生产环境中是隐蔽的——它们不会导致 Agent 完全失败，但会导致工具失败率上升、用户等待时间增加。

---

## 二、Smarter Delegation 的核心设计

Smarter Delegation 不是一个新功能，而是一个** Harness 层的决策机制**，让主 Agent 在三个场景下做出更聪明的选择：

### 场景 1：保持专注（Stay Focused）

当任务主 Agent 能直接完成时，不委托。标准是：**任务已经足够窄、足够明确，或者 handoff 里已经包含了完成任务所需的全部上下文**。

### 场景 2：按需委托（Delegate When It Creates Leverage）

只有当子 Agent 能创造真正的杠杆时才委托。典型场景：
- 探索不熟悉的代码区域
- 并行检查相互独立的代码区域
- 执行长时间运行的命令，同时主 Agent 继续处理其他工作

### 场景 3：真正并行（Parallelize When Genuinely Independent）

把 delegation 当作并行机会，而非串行阻塞点。

---

## 三、量化结果：23% 工具失败率降低

Smarter Delegation 已经 100% 部署到 Copilot CLI 生产流量。量化结果：

| 指标 | 改善幅度 |
|------|---------|
| 工具失败率（每 session） | **-23%** |
| 搜索工具失败率 | **-27%** |
| 编辑工具失败率 | **-18%** |
| 用户 P95 等待时间 | **-5%** |
| 用户 P75 等待时间 | **-3%** |
| 质量回归 | **无** |

> 原文引用 2："In a production A/B test, this improvement reduced tool failures per session by 23%, including a 27% reduction in search tool failures and an 18% reduction in edit tool failures. It also improved total user wait time by 5% at P95 and 3% at P75, with no quality regression."

这是一组在 Harness 调优领域极为罕见的公开生产级数据。大多数团队做 A/B 测试，但几乎没有人公开具体的工具失败率改善数字。

---

## 四、方法论：Feedback Loop 作为调优框架

Copilot CLI 团队的方法论本身就是一个值得学习的工程框架：

```
观察 Agent 行为 → 隔离编排瓶颈 → 定向修改 → 离线验证 → 在线 A/B 测试 → 交付
```

这不是一个线性流程，而是一个**反馈循环**。关键洞察是：他们用 LLM 分析 Agent 轨迹（trajectories），而不是人工 review session 日志。

> 原文引用 3："Instead of manually reviewing agent sessions, we used LLMs to analyze full trajectories and identify where orchestration was helping versus where it was adding overhead."

用 LLM 分析 LLM 的行为——这个元层的自动化是本次调优的效率杠杆。

---

## 五、工程意义：Harness 的"反直觉"优化

大多数 Harness 优化的方向是"让 Agent 能力更强"——更多工具、更高上下文窗口、更复杂的推理链。但 Smarter Delegation 的优化方向是**让 Agent 少做事**。

这不是能力不足，而是**精确控制**。

笔者认为，这个方向代表了 Harness 工程的一个成熟阶段：当 Agent 基础能力已经足够强时，下一个边际收益来自于**减少不必要的协调开销**，而非继续提升单次执行质量。

---

## 六、与已有 Harness 实践的关系

| 已有实践 | Smarter Delegation 的位置 |
|---------|--------------------------|
| Anthropic 双层权限判断 | Outer loop 决策层 |
| OpenAI 沙箱隔离 | Inner loop 执行层 |
| Cursor Plan-first 执行 | 任务分解层 |
| **Smarter Delegation** | **编排决策层** |

Smarter Delegation 填补了"Harness 编排层"量化调优的空白——它是第一个在生产环境公开具体数字的 Agent 编排优化案例。

---

## 七、给 Agent 开发者的启示

1. ** Delegation 需要显式成本建模**：不要默认"委托就是好的"，需要评估 handoff 开销
2. **工具失败率是编排质量的信号**：工具失败不只是工具问题，很可能是 delegation 决策问题
3. **用 LLM 分析 LLM 行为**：Copilot CLI 团队用 LLM 做轨迹分析，这是元层自动化的重要方向
4. **量化是工程成熟的标志**：有 A/B 测试能力，才能做真正的 Harness 调优

---

## 关联项目

本文从 Harness 编排层分析 Copilot CLI 的 Delegation 优化。关于 **Harness 的执行层隔离**，推荐阅读：[github.com/github/gh-aw](https://github.com/github/gh-aw) — GitHub Agentic Workflows 的 AWF 三层安全架构，为本文的"信任问题"提供完整的企业级解决方案。

---

## 补充：Copilot CLI v1.0.42 更新说明

Smarter Delegation 功能随 Copilot CLI v1.0.42（2026-06-12）发布。更新方式：

```bash
/copilot
/update
```

无需任何额外配置，delegation 决策机制在 Harness 层自动生效。