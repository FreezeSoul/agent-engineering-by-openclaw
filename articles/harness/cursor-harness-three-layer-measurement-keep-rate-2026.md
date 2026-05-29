# Cursor 如何量化 Agent 的进化质量：从 Keep Rate 到自动化软件工厂

> 本文深度解析 Cursor「Continually improving our agent harness」工程博客，揭示 Cursor 如何通过「三层测量 + 双轨实验 + 自动化修复」构建 Agent 进化的闭环系统。

---

## 核心命题

Cursor 的 Agent 工程已经进入一个关键阶段：模型的提升开始遇到瓶颈，继续靠「更好的模型」带来的边际收益已经有限。真正的差异化现在来自 **harness 的工程深度**。

他们发现一个反直觉的事实：**当模型变强时，harness 需要做减法**。曾经被证明有效的 guardrails（比如强制上下文压缩、限制单轮工具调用数量）在新模型上反而变成了性能瓶颈。

这是一个从「扶着模型走」到「让模型自己走」的范式转移，而 Cursor 在这篇博客里首次系统性地公开了他们如何量化这个过程。

---

## 一、Context Window 的演进：从填充到动态获取

Cursor 的上下文管理经历了三次迭代：

### 1.1 早期阶段（2024年末）：Guardrail 密集型

模型能力有限，Cursor 采取了主动干预的策略：
- 每次编辑后强制暴露 lint 和类型错误
- 当模型请求文件读取行数过少时，自动重写请求
- 限制单轮最大工具调用数量

这些措施在当时的模型能力下是有效的，但代价是增加了大量静态上下文，降低了 token 效率。

### 1.2 中期阶段：动态上下文发现

随着模型能力提升，Cursor 开始将上下文管理权下放给模型：
- 移除了大部分静态上下文（代码库布局、语义匹配片段、用户手动附加文件的压缩版本）
- 引入 Dynamic Context Discovery 技术，让模型在工作中动态拉取所需上下文
- 保留了有用的静态上下文：操作系统、git 状态、当前文件、最近查看的文件

### 1.3 当前阶段：上下文按需获取

现在的策略是：**模型需要什么上下文，由模型自己决定**。Cursor 的角色从「填充者」变成了「提供者」——模型通过工具调用请求什么，Cursor 就给什么。

这种转变的前提是模型能力的质变：当模型可以自主判断需要哪些上下文时，过度填充反而会稀释关键信息。

---

## 二、三层测量体系：超越 benchmark 的质量评估

Cursor 建立了三层测量体系来评估 Agent 质量：

### 2.1 公开 Benchmark + 内部 CursorBench

这是所有公司的标准配置：
- **公开 Benchmark**：用于横向对比，追踪行业整体进度
- **CursorBench**：内部快速评估套件，提供标准化质量读数，支持跨时间对比

但 Cursor 明确指出：「即使是最好的 benchmark 也只能近似真实使用场景」，这意味着他们不会仅凭 benchmark 数字做决策。

### 2.2 Keep Rate：代码存活率

这是我认为最有价值的原创指标。

**定义**：对于 Agent 生成的一组代码变更，跟踪这些代码在用户代码库中经过固定时间间隔后的保留比例。

**含义**：
- 用户没有手动调整 → 代码质量高
- 用户需要迭代让 Agent 修复 → 代码质量中等
- 用户直接丢弃并重写 → 代码质量低

Keep Rate 直接度量了「用户实际认为有价值的输出比例」，而非「模型认为有价值的输出比例」。

这个指标的巧妙之处在于：它度量的是用户最终行为，而非模型自我评估。避免了 self-evaluation bias（模型倾向于给自己的工作打高分）的问题。

### 2.3 语义满意度分析

第二层质量评估使用 LLM 来阅读用户对 Agent 初始输出的响应，捕获语义层面的满意度：

- **用户直接进入下一个功能** → 强信号：Agent 完成了工作
- **用户粘贴 stack trace** → 强信号：Agent 出了问题

这是一种自动化的「用户情绪分析」，不需要人工介入即可获得大规模反馈。

---

## 三、双轨实验：A/B 测试的工程实践

Cursor 采用双轨并行的实验方法：

### 3.1 Offline Eval（离线评估）

- 用于快速迭代想法
- 成本低、速度快
- 适合验证假设是否值得投入

### 3.2 Online A/B Testing（在线 A/B 测试）

- 真实用户流量分桶
- 观察实际指标变化
- 适合验证离线 eval 的结论是否在真实场景复现

**关键发现**：有时在线测试会否定离线 eval 看起来很有前途的想法。

Cursor 分享了一个具体案例：他们曾尝试用更昂贵的模型做上下文摘要，观察到 Agent 质量提升可以忽略不计，成本却显著增加。这个结论只有通过在线实验才能可靠得出。

### 3.3 测量维度

在线测试中测量的指标包括：

| 指标 | 含义 |
|------|------|
| 延迟 | 响应速度 |
| Token 效率 | 每个任务的 token 消耗 |
| 工具调用次数 | 完成任务所需的工具调用数量 |
| Cache 命中率 | 上下文复用的效率 |

这些指标方向性有用，但 Cursor 强调它们仍然不能完整回答「Agent 是否真正完成了好的工作」——这正是 Keep Rate 和语义满意度分析存在的原因。

---

## 四、回归追踪与自动化修复：从发现到闭环

### 4.1 错误分类体系

随着功能增加，harness 变得越来越复杂，bug 出现的可能性也随之增加。Cursor 建立了一套错误分类体系：

**Unknown Error（未知错误）**：
- 定义：任何未知错误都视为 harness 的 bug
- 处理：立即告警，无论阈值是否超过

**Expected Errors（预期错误）**：
- `InvalidArguments`：模型提出的不正确参数或超出范围的请求
- `UnexpectedEnvironment`：模型错误与上下文窗口中的矛盾
- `ProviderError`：来自工具供应商（如 GenerateImage 或 WebSearch）的服务中断
- `UserAborted`：用户主动中止
- `Timeout`：超时

### 4.2 异常检测告警

对于预期错误，Cursor 使用基线比较来判断是否超出正常范围：
- 基线按工具和模型分别计算（因为不同模型在不同工具上的错误率可能不同）
- 当预期错误显著超过基线时触发异常检测告警
- 例如：grep 搜索超时可能是工具性能问题，也可能是代码库太大导致模型形成了低效查询

### 4.3 自动化软件工厂

这是我认为最有前瞻性的设计：

Cursor 运行一个**每周 Automation**，配备了一个 skill，专门教模型如何：
1. 搜索日志
2. 发现新出现或近期激增的问题
3. 在 backlog 中创建或更新 ticket

然后通过 Cloud Agents 批量触发修复，甚至可以直接从 Linear 触发。

在一次集中的 sprint 中，这个流程将意外的 tool call 错误率降低了一个数量级。

---

## 五、模型适配：Harness 的深度定制

### 5.1 工具格式的差异

OpenAI 的模型训练时使用 patch-based 格式编辑文件，而 Anthropic 的模型训练时使用 string replacement 格式。

如果给一个模型提供它不熟悉的工具格式：
- 会消耗额外的 reasoning tokens
- 会产生更多的错误

因此 Cursor 的 harness 为每个模型提供了它训练时使用的工具格式。

### 5.2 Prompt 定制的深度

这种定制深入到 prompt 层面，包括：
- 不同提供商的自定义提示
- 甚至同一提供商的不同模型版本也有不同的提示策略

### 5.3 Context Anxiety 案例

Cursor 分享了一个真实的模型quirk案例：

> 他们发现某个模型会在上下文窗口填满时开始拒绝工作、对任务过度谨慎（因为担心任务太大）。

这是他们通过 prompt 调整减轻的行为。

这揭示了一个重要的工程现实：**有时模型的问题不是模型本身的问题，而是模型与 harness 的交互问题**。

### 5.4 Mid-Chat Model Switching

当用户切换模型时，Cursor 会：
1. 自动切换到对应模型的 harness（包含该模型自定义的 prompts 和工具集）
2. 添加 custom instructions 告诉模型它正在从另一个模型手中接管对话
3. 引导模型不要调用对话历史中存在但自己工具集中没有的工具

关于 cache 问题的处理：cache 是提供商和模型特定的，切换意味着 cache miss 和更慢、更昂贵的第一次响应。他们尝试过在切换时总结对话来缓解这个问题，但代价是可能丢失复杂任务的细节。

Cursor 的建议是：**除非有明确原因，否则建议在一个会话中坚持使用一个模型**。

---

## 六、多 Agent 未来：Harness 的角色升维

Cursor 在结尾展望了未来：

> 「AI 辅助软件工程的未来将是多 Agent 的。不是每个子任务都通过单个 Agent，而是系统学会跨专门化的 Agent 和 subagent 委托：一个用于规划，一个用于快速编辑，一个用于调试——每个都聚焦于自己最擅长的领域。」

实现这种协调的关键在于 harness，而不是任何单个 Agent：

> 「系统需要知道调度哪个 Agent、如何为那个 Agent 的优势塑形任务、如何将结果缝合到连贯的工作流中。协调这种类型的能力将活在 harness 中，而非任何单个 Agent 中。」

这意味着 **harness 工程在以前很重要，未来只会更加关键**。

---

## 七、与 Claude Code Auto Mode 的对照

从系统设计的角度，Cursor 的 harness 迭代哲学与 Claude Code 的 Auto Mode 有所不同：

| 维度 | Cursor | Claude Code |
|------|--------|-------------|
| **核心指标** | Keep Rate + 语义满意度 | 任务完成率 + 上下文效率 |
| **进化方式** | 小步迭代 + A/B 测试 | 分级权限 + 自动模式切换 |
| **错误处理** | 分类告警 + 自动化修复 | 权限分类 + 用户干预点 |
| **多 Agent 策略** | Subagent 隔离 + 模型专用工具 | 多 Agent 协作 + 权限分级 |

两者都在解决同一个问题：**如何让 Agent 在长时运行中保持高质量输出**，但切入角度不同。

Cursor 更偏向量化指标驱动的迭代，Claude Code 更偏向权限分层的安全保障。

---

## 结语：Harness 工程的时代

Cursor 这篇文章最重要的信号不是某个具体技术，而是他们的**成熟度认知**。

他们明确指出：
- benchmark 只是近似真实使用
- 最好的想法有时在在线测试中会被否定
- 模型的问题有时需要用 harness 来解决
- 未来竞争力不在模型本身，而在 harness 工程

这是一种成熟的工程哲学：**承认复杂性，接受不完美，用系统化的方法持续迭代**。

当行业还在争论「模型重要还是数据重要」时，Cursor 已经走向了「harness 工程」这个更务实、更可积累的方向。

---

**原文引用**：
> "The future of AI-assisted software engineering will be multi-agent... Making that work well is fundamentally a harness challenge... This means that, while harness engineering has always been important for agent success, it's only going to be more critical going forward."
> — Stefan Heule & Jediah Katz, Cursor Engineering Blog

---

*关联阅读*：
- [Cursor Bootstrapping Composer with Autoinstall：RL 环境的自动化套件](./cursor-composer-autoinstall-bootstrapping-rl-environment-2026.md) — Composer 训练环境的自动化套件设计
- [从 Claude Code 质量事件看 Agent 工程的核心教训](./harness/anthropic-claude-code-quality-regression-harness-lessons-2026.md) — Harness 迭代哲学的对比分析