# Cursor Agent Harness 持续改进工程：上下文演进、评估体系与模型适配

> 来源：[Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness) (Cursor Engineering Blog, Apr 30, 2026)  
> 作者：Stefan Heule & Jediah Katz  
> 标签：`harness` `evaluation` `context-engineering` `cursor`

---

## 核心命题

Cursor 用做产品的思路做 Agent Harness：**vision-driven hypothesis → experiment → iterate**。他们不只优化模型本身，而是在模型之外构建一套测量-反馈-迭代的基础设施，让同一模型在特制的 harness 中明显更快、更聪明、更高效。

> "We approach building the Cursor agent harness the way we'd approach any ambitious software product."

---

## 一、上下文窗口的演进：从 Guardrails 到动态上下文

### 2024 年底的起点

早期模型选择上下文的能力很弱，Cursor 在 harness 层加了大量 guardrails：

- 每次编辑后强制呈现 lint 和类型错误
- 模型请求行数太少时自动重写文件读取
- 限制单轮最大工具调用数

同时提供大量**静态上下文**（session 开始时就存在）：文件夹布局、语义匹配代码片段、用户手动附加文件的压缩版本。

### 2026 年的现状

大部分 guardrails 已拆除。模型能力增强后，Cursor 转为**动态上下文**——模型在工作过程中主动拉取，而非预先填入。

> "Much of our work now focuses on providing more ways for the agent to dynamically pull context and interact with the world."

保留的静态上下文仅剩：操作系统、git status、当前和最近查看的文件。

---

## 二、评估框架：离线 Benchmark + 在线 A/B 实验

Cursor 用两层测量体系评估 harness 改动：

### 离线层：CursorBench

公开 benchmark，提供快速、标准化的质量读数，支持跨时间对比。

### 在线层：A/B 测试

将两个或更多 harness 变体并行部署，测量真实用户场景下的多维指标：

| 指标类型 | 具体指标 | 局限性 |
|----------|----------|--------|
| 基础性能 | 延迟、token 效率、工具调用次数、缓存命中率 | 方向性有用，但不直接反映"任务完成质量" |
| Keep Rate | agent 提案的代码在用户代码库中保留的比例 | 反映用户是否需要手动调整 agent 输出 |
| LLM 满意度评估 | 用语言模型读取用户对 agent 初次输出的回应 | 语义判断：用户转向下一个功能=成功，贴错误栈=失败 |

> "Sometimes these online tests tell us to shelve an idea that seems promising. In one experiment, we tried a more expensive model for context summarization and observed it made a negligible difference in agent quality that wasn't worth the higher cost."

---

## 三、工具错误追踪：分类体系与异常检测

### 工具错误的危险性

工具调用错误会残留上下文，造成 **"context rot"**——累积的错误会降级模型后续决策质量。极端情况下，agent 会完全跑偏。

### 错误分类体系

```
未知错误（UnknownError）
  └── 始终是 harness 的 bug，发现即告警

预期错误（Expected Errors）
  ├── InvalidArguments — 模型提议了错误参数
  ├── UnexpectedEnvironment — 上下文窗口中的矛盾
  ├── ProviderError — 工具供应商宕机（GenerateImage、WebSearch 等）
  ├── UserAborted
  └── Timeout
```

### 告警策略

- **未知错误**：任何工具的未知错误率超过固定阈值即触发
- **预期错误**：每个工具、每个模型单独计算基线，通过**异常检测告警**发现显著偏离基线的情况

> "We have alerts whenever the unknown error rate for any tool exceeds a fixed threshold."

### 自动化修复流程

Cursor 运行了一个配备专属 skill 的 Cloud Agent，教会它：
1. 搜索日志
2. 发现新出现的或最近飙升的问题
3. 在 backlog 中创建或更新 ticket

> "Over the course of a focused sprint earlier this year, we drove unexpected tool call errors down by an order of magnitude."

---

## 四、模型适配：Harness 的深度定制

### 工具格式适配

不同模型训练时使用的工具格式不同：

- **OpenAI 模型**：训练时用 patch-based 格式编辑文件
- **Anthropic 模型**：训练时用 string replacement 格式

给模型提供不熟悉的工具格式 = 额外的 reasoning token 消耗 + 更多错误。

### 提示词定制深入到版本级别

> "Custom prompting for different providers and even for different model versions. OpenAI's models tend to be more literal and precise in their instruction following, whereas Claude is a bit more intuitive and more tolerant to imprecise instructions."

### 发现的模型怪癖：Context Anxiety

Cursor 发现某个模型有一种行为：随着上下文窗口填满，模型开始拒绝工作，措辞是"任务看起来太大"。

通过 prompt 调整减少了这种行为。

---

## 五、Mid-Chat 模型切换的特殊挑战

当用户切换模型时，Cursor 自动切换到对应模型的 harness（包含定制的 prompts 和工具集）。

但挑战在于：

1. **对话历史是另一个模型生成的**，对当前模型来说是 out of distribution
2. **缓存是 provider- 和 model-specific 的**，切换 = 缓存未命中 = 首次响应更慢更贵

Cursor 的解法：添加自定义指令，告诉模型它正在 mid-chat 接管另一个模型，并引导它不要调用当前工具集中不存在的工具。

---

## 工程要点总结

| 维度 | Cursor 的做法 | OpenAI Harness Engineering 的对应 |
|------|-------------|-----------------------------------|
| 上下文管理 | 从静态 guardrails → 动态主动拉取 | 环境比模型重要 |
| 评估体系 | 离线 CursorBench + 在线 Keep Rate + LLM 满意度 | 验证是架构 |
| 错误处理 | 分类体系 + 基线异常检测 + 自动化修复 | 文档是系统 |
| 模型适配 | 工具格式定制到训练版本级别 | 显式记忆 |
| 切换支持 | mid-chat 指令重写 + 缓存策略 | — |

---

## 延伸阅读

- [Cursor Composer 2.5 深度解析：长程 RL 与合成数据的工程突破](./cursor-composer-2-5-targeted-rl-synthetic-data-2026.md) — 同为 Cursor Engineering 博客，同一时期发布，Composer 2.5 是模型侧改进，本文是 harness 侧改进
- [Agent Harness Engineering：为什么模型不是决定性因素](./openai-harness-engineering-philosophy-2026.md) — OpenAI 的 harness 理念，与 Cursor 的工程实践形成互补

---

*本文属于 [Harness Engineering](../projects/ai-boost-awesome-harness-engineering-2026.md) 知识体系的一部分。*