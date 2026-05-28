# ZeroLang：用 C 语言重新定义 Agent 编程语言的设计哲学

> **笔者认为**：当社区还在争论「要不要给 LLM 设计专用语言」时，Vercel Labs 已经用 ZeroLang 回答了这个问题——不是设计一门新语言让 Agent 学，而是设计一门让 Agent 工作得更可靠的语言。这两者的区别，才是理解 ZeroLang 的关键。

## 核心命题

ZeroLang 不是又一门「为 AI 设计的 DSL」。它的核心出发点是：**现有的通用编程语言（C/Rust/Go）在设计时，根本没有考虑 Agent 工作流的需求**——Token 效率、内存占用、启动速度、构建速度、运行时延迟、零外部依赖，这六个指标对人类程序员来说是次要优化目标，但对自主运行的 Agent 来说，是系统稳定性的根基。

![GitHub](screenshots/vercel-labs-zerolang-20260529.png)

## 为什么 Agent 需要专用的编程语言

### 人类工程师 vs Agent 的需求差异

| 维度 | 人类工程师 | Agent（自主运行）|
|------|-----------|----------------|
| **认知带宽** | 无限（可以查文档）| 受限（上下文窗口有限）|
| **执行稳定性** | 可随时干预 | 需要长时间无人值守 |
| **错误恢复** | 人工排查 | 必须依赖结构化输出 |
| **Token 成本** | 无所谓 | 直接影响任务完成率 |
| **环境隔离** | 可手动配置 | 需要编译器原生保障 |

**笔者认为**：这不是「谁更聪明」的问题，而是「谁的运行时约束更严苛」的问题。Agent 在长时任务中面临的不是「代码写得对不对」，而是「编译器是否给得出我能可靠处理的输出」。

### ZeroLang 的设计取舍

从 README 可以看出 ZeroLang 的六个优化方向：

```
Token efficiency    → 减少 LLM 的上下文消耗
Low memory usage   → 适应容器化 Agent 环境
Fast startup       → 支持快速任务切换
Fast builds        → 支持频繁的编译-验证循环
Low runtime latency → 支持实时响应场景
Zero dependencies  → 消除环境配置的脆弱性
```

这六条，每一条都是冲着「让 Agent 稳定工作」去的，而不是冲着「让程序员写得更爽」。

## Agent Workflow Interfaces：编译器即 API

ZeroLang 最聪明的设计决策是把编译器本身暴露为 Agent 的工具链，而不是让 Agent 去调用一个外部服务。

### 传统模式的困境

```
Agent → 调用 Language Server → 调用 编译器 → 返回结果
         （额外进程/依赖）     （版本不匹配风险）
```

### ZeroLang 的模式

```
Agent → zero CLI（内置所有功能）
         ↓
    zero parse --json
    zero check --json
    zero fix --plan --json
         ↓
    稳定结构化输出，直接可用
```

**零额外进程**，**零版本漂移风险**，**零网络依赖**。

### 结构化输出合同

| 命令 | 输出内容 |
|------|---------|
| `zero tokens --json` | Token 序列 + 位置信息 |
| `zero parse --json` | 声明列表、函数签名、body 节点类型 |
| `zero check --json` | 诊断码、Span、期望/实际值、修复安全等级 |
| `zero graph --json` | 模块图、导入边、公共符号、能力、所有权事实 |
| `zero fix --plan --json` | 类型化修复计划（不改文件，先展示）|
| `zero size --json` | 保留的 helper、尺寸原因、profile 策略、后端事实 |

**笔者认为**：这里的精华不是「JSON 输出」这个形式，而是 `zero fix --plan --json` 体现的思路——**编译器先告诉 Agent 要修什么，Agent 确认后再动手**。这直接模拟了「Code Review 中开发者确认修复」的工作流，让 Agent 的修复行为变得可审计。

## Safety Status：诚实的工程态度

README 里有这段话：

> **Safety status**
> Security vulnerabilities should be expected. zerolang is not ready for production systems, sensitive data, or trusted infrastructure. Run and develop it in isolated, disposable environments.

**笔者认为**：这是 ZeroLang 最值得尊敬的地方。它没有把「Experimental」藏在某个角落，而是放在 README 正文的第一条注意事项里。这意味着什么？意味着 Vercel Labs 在设计这门语言时，心里想的是「Agent 在安全隔离环境里工作」，而不是「先跑起来再说」。这种设计态度，比很多「宣称安全」但没有安全设计的项目强得多。

## 与现有方案的对比

### ZeroLang vs 通用语言（Python/JS/Go）

| 对比维度 | Python/JS/Go | ZeroLang |
|---------|-------------|---------|
| Agent 友好度 | 需要额外 LSP 配置 | 编译器自带所有接口 |
| Token 效率 | 高（冗长的标准库语法）| 优化过（专为精简设计）|
| 环境依赖 | pip/npm/go get | 零外部依赖 |
| 结构化修复 | 依赖 IDE/静态分析工具 | 编译器原生支持 |
| 启动速度 | 秒级 | 子毫秒级（编译型）|

### ZeroLang vs 其他「AI 编程语言」

| 对比维度 | 其他 AI DSL | ZeroLang |
|---------|------------|---------|
| 设计出发点 | 「让 LLM 更方便生成代码」| 「让 Agent 工作更可靠」|
| 编译器角色 | 辅助工具 | 核心接口 |
| 版本一致性 | 依赖包管理器 | 内置 `zero skills get` |
| 生产可用性 | 差异大 | 明确声明实验性 |

## 适用场景与局限性

### 适用场景

- **Agent 原型开发**：需要快速验证 Agent 对代码的控制能力
- **资源受限环境**：嵌入式 Agent、容器化 CI Agent
- **高 Token 成本场景**：上下文窗口极度稀缺时的代码生成
- **需要可预测行为的长时任务**：编译器输出稳定，无需担心包版本漂移

### 局限性

- **安全声明明确**：不适合处理敏感数据或生产环境
- **C 语言生态**：虽然对 Agent 友好，但对习惯高级语言的人类开发者有学习成本
- **成熟度**：目前只有 4641 Stars，v0.x 阶段，大量 API 还在变化

## 原文引用

> "The compiler exposes the workflow through CLI commands with stable structured output."

> "zerolang is not ready for production systems, sensitive data, or trusted infrastructure. Run and develop it in isolated, disposable environments."

> "ZeroLang keeps the agent-facing inspection and repair path in the compiler CLI."

## 总结

ZeroLang 代表了一种范式转变：不是「为 AI 设计语言」，而是「从 Agent 工作流需求出发设计语言」。它的核心价值不在于 C 语言本身，而在于「编译器即 API」这个设计哲学——把版本一致性、结构化输出、修复计划生成全部内置到编译器里，让 Agent 可以在一个零外部依赖的环境里完成完整的「编写-检查-修复」循环。

**笔者认为**：这门语言目前是实验性的，不适合直接上生产，但它解决的不是「能不能用」的问题，而是「Agent 工作流的基础设施应该长什么样」的问题。关注这个方向的进展。

---

*项目地址：[vercel-labs/zerolang](https://github.com/vercel-labs/zerolang) | Stars: 4,641 | Apache 2.0*