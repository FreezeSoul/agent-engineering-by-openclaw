# Anthropic 三漏洞复盘：为什么标准 Evals 找不到生产级 AI 的退化

## 核心命题

笔者认为，Anthropic 这次三漏洞复盘揭示了一个被大多数 AI Agent 开发者忽视的事实：**标准评测框架（evals）对生产环境中的质量退化是盲的**。当 Claude 的响应质量在用户侧下降时，Anthropic 内部跑的那套评测体系没有发出任何信号——这不是评测数量的问题，而是评测设计方向的盲区。

**这篇文章要回答的问题是**：为什么生产级 AI 系统会出现「用户感受到了退化，但 evals 显示一切正常」的现象，以及 Agent 开发者和企业 AI 负责人应该如何建立更可靠的质量监控机制。

---

## 三个漏洞的机制分析

### 漏洞 1：上下文窗口路由错误

**现象**：部分 Sonnet 4 请求被错误路由到配置了 1M token 上下文窗口的服务器。影响范围：0.8% 初始请求 → 经由 8 月 29 日负载均衡变更后，在最严重时段上升到 16%。

**为何难发现**：
- 路由是「粘性」的（sticky session）：一旦请求被错误路由，后续所有 follow-up 都在错误的服务器上
-30% 的 Claude Code 用户在此期间至少有 **一条消息**被错误路由
- 症状因用户对话上下文而异，无法归一化为一个 eval 测试用例

### 漏洞 2：输出损坏（TPU 运行时优化误触）

**现象**：在 TPU 服务器上，一次运行时性能优化导致某些 token 被赋予异常高概率——英文提示产生泰语字符，代码产生明显语法错误。

**为何难发现**：
- 仅影响 TPUs，不影响 NVIDIA GPU 和 AWS Trainium 上的请求
- 损坏频率是偶发的（intermittent），同一条 prompt 这一次正常、下一次损坏
- 只有当请求被路由到 TPU 节点时才出现（跨平台部署的等价性验证缺陷）

### 漏洞 3：XLA:TPU 近似 top-k 错误

**现象**：一个性能优化算法（approx top-k）在特定批次大小和配置下返回完全错误的结果——最高概率的 token 被意外丢弃。

**为何难发现**：
- 该 bug 的行为随「在该次请求之前运行的其他操作」而变化（non-deterministic but context-dependent）
- 开启调试工具后行为会改变（调试工具引入了额外的同步机制，掩盖了 bug）
- Anthropic 在 2024 年 12 月部署的临时修复（workaround）意外掩盖了这个更深层的 bug，直到2026 年 8 月的修复移除了该 workaround 后才暴露

---

## 核心工程教训：Eval 的盲区

### Eval 为何失效

Anthropic 在复盘中明确指出了三个原因：

**1. 评测无法捕获偶发性症状**

> 「The evaluations we ran simply didn't capture the degradation users were reporting, in part because Claude often recovers well from isolated mistakes.」

Eval 通常运行确定的测试用例，评估的是「能否正确完成特定任务」。但这三个漏洞产生的症状是**偶发的、环境依赖的、与上下文相关的**——无法用一个固定的测试集覆盖。

**2. 跨平台等价性验证不足**

三套硬件（Trainium / GPU / TPU）上的实现必须等价，但实际出现了只在 TPU 上才触发的 bug。Eval 通常在单一平台上运行，没有系统性地验证「同一请求在不同硬件上是否产生等价输出」。

**3. 生产信号与 Eval 信号的脱节**

> 「We lacked a clear way to connect these [user reports] to each of our recent changes.」

用户反馈是零散的、定性的；Eval 是结构化的、定量的。两者之间没有有效的桥梁，导致负面反馈的「尖刺」（spike）无法归因到具体的变更。

---

## 对 Agent 开发者的启示

### 1. 建立生产级质量监控，而非仅依赖 Pre-deployment Evals

标准 Eval套件有两个根本局限：

- **覆盖边界有限**：Eval 通常覆盖「已知的失败模式」，而生产环境中出现的是「未知的新失败模式」
- **无法捕获偶发性问题**：当 bug 是概率性触发时，大量测试的平均分数不会显著下降，但用户侧会感受到「时好时坏」

Anthropic 采取的改进方向值得参考：

> 「We'll run them continuously on true production systems to catch issues such as the context window load balancing error.」

这意味着：**在生产流量中建立持续的质量监控**，而不是在隔离的测试环境中跑固定的评测集。

### 2. 跨平台等价性验证是 AI Agent 部署的必要条件

当 Agent 运行在不同的执行环境（本地沙箱 / 云端 VM / 浏览器扩展 / MCP 隧道）时，开发者必须验证「同一请求在不同环境下产生等价结果」。这个验证必须是自动化的、持续的，而非一次性的。

### 3. 用户反馈是 Eval 设计的重要输入

Anthropic 特别提到：

> 「It remains particularly helpful for users to continue to send us their feedback directly.」

对于企业 AI 部署，这意味着：**建立用户可以直接反馈「AI 回答质量异常」的通道**，并且这个反馈数据应该能够关联到具体的系统变更，而不是淹没在总体满意度评分中。

---

## 关键引用

> 「We never reduce model quality due to demand, time of day, or server load. The problems our users reported were due to infrastructure bugs alone.」

> 「The evaluations we ran simply didn't capture the degradation users were reporting.」

> 「We lacked a clear way to connect these [user reports] to each of our recent changes.」

> 「We've added detection tests for unexpected character outputs to our deployment process.」

---

## 笔者判断

这次复盘对 Agent 工程的最大贡献，不是那三个具体漏洞的根因分析，而是揭示了一个范式转变的必要性：**AI 系统质量保证正在从「Eval 驱动开发」向「生产监控 + Eval 反馈闭环」演进**。

传统软件工程的监控体系（SLO/SLI/错误预算）在 AI 系统上的对应物还没有形成标准。Anthropic 这次经历是一个重要的参考点——当模型质量无法用单一指标衡量时，我们需要更复杂的生产监控机制。

对于企业 AI 负责人而言：**不要只关注模型在标准 benchmark 上的分数，关注模型在生产环境中的行为稳定性**，这才是真正的质量信号。