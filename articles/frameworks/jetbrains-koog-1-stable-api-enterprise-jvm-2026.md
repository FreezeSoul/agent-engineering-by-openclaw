# JetBrains Koog 1.0：第一个承诺「一年不破坏」的 JVM Agent 框架意味着什么

> 原文：https://blog.jetbrains.com/ai/2026/05/koog-1-0-is-out-stable-core-better-interop-and-multiplatform-observability/
> 发布：2026-05-29 | 来源：JetBrains AI Blog

---

## 核心问题：Agent 框架的稳定性困境

过去一年，AI Agent 框架领域最大的问题不是功能不够，而是稳定性缺失。一个在生产环境中跑了三个月的 Agent，可能因为一次依赖升级而在第四个月悄无声息地崩溃。主流框架（LangChain、AutoGen 等）都有这个问题——快速迭代的代价是 API 随时可能 breaking change，企业要么锁死版本，要么持续踩坑。

Koog 1.0 给出了一个不同的答案。

## Koog 1.0 的核心承诺：一年 API 稳定

Koog 是 JetBrains 推出的开源 JVM（Java/Kotlin）Agent 框架，定位是「可预测、容错、企业级」的跨平台 Agent 开发基础设施。在 KotlinConf 2026 上，Koog 发布了 1.0 正式版，其中最核心的改变不是新功能，而是**明确的稳定性承诺**：

> 我们保证，稳定模块（stable modules）的 API 在至少一年内不会引入 breaking changes。

这是一个重量级的承诺，原因在于：

**大多数框架不做这种承诺**。LangChain 的版本跳跃速度有目共睹；AutoGen 经历了从 0.x 到 1.x 再到 AG2 分叉的剧烈变化；就连 Semantic Kernel 也经常有破坏性更新。背后的原因是：Agent 框架的 API 设计本身就没有收敛，快速迭代压过了稳定性。

JetBrains 敢于做这个承诺，是因为 Koog 的核心受众是**企业级 Kotlin/JVM 团队**，而这个群体的核心诉求恰好是「不要变」，而不是「最新特性」。

## 稳定性承诺的工程机制

Koog 1.0 的稳定性通过具体的工程机制落地，不是营销语言：

**模块分级流（Module Split into Stable/Beta）**

框架模块现在分为两个流：
- **Stable**：生产代码可以直接 pin，API 不破坏
- **Beta**：仍在演进的 experimental 功能

这意味着企业在评估是否上生产时，可以明确区分「稳定可用」和「尝鲜」的部分，而不是面对整个框架的不确定性。

> "Modules now ship under two streams — stable and beta — so production code can pin to APIs that won't break without a deprecation cycle." — Koog 1.0 Release Notes

**所有 Deprecated API 已清除**

1.0 之前的 deprecated API 在 1.0 中全部移除。这意味着代码中如果有任何 1.0 之前版本的 deprecated 引用，编译就会报错，而不是静默兼容。这个决定很激进，但对企业来说，这是「技术债必须清理」的明确信号。

**统一阻塞 API（Uniform Blocking API）**

> "All Java-facing entry points follow one pattern — xxxBlocking in Kotlin, plain xxx from Java. Explicit ExecutorService / Executor parameters are gone; the agent's configured dispatcher is used instead." — Koog 1.0 Release Notes

Java 和 Kotlin 的互操作层重新设计，Java 调用方不需要理解 Kotlin 协程的概念，直接用同步 API。这个改动让 Koog 可以真正服务 Java 团队，而不是把 Kotlin 作为一等公民、Java 作为二等。

## 跨平台观测：OpenTelemetry 到每一层

Agent 框架最难解决的运维问题之一是**可观测性**。当一个 Agent 运行在 Android 上和运行在 JVM 服务端时，观测的方式完全不同。

Koog 1.0 的 OpenTelemetry 支持覆盖了 Koog 的所有目标平台（JVM、Android、iOS、JS、WasmJS），通过 Ktor-based OTLP/JSON exporter 实现统一，而不是只在 JVM 上工作。

内置的标准 metrics 包括：
- `gen_ai.client.token.usage`
- `gen_ai.client.operation.duration`
- `gen_ai.client.tool.count`

这些都是行业标准格式，可以直接插入 Prometheus/Grafana 体系，不需要额外的 adapter。

## Anthropic Prompt Caching：第一梯队的成本优化

Prompt Caching 是 2026 年各大模型提供商的主推功能，Koog 1.0 第一时间跟进：

> "End-to-end caching support — automatic on requests, explicit breakpoints on messages, cache tokens in usage metrics." — Koog 1.0 Release Notes

对于长系统 prompt 的 Agent，这个功能可以显著降低成本和延迟。关键是 Koog 把 cache control 做成了端到端的框架层支持，而不是让开发者自己管理缓存逻辑。

## 多平台部署：JVM 以外的世界

Koog 1.0 另一个差异化点是多平台支持。一个 Kotlin Agent 可以部署到：
- JVM 后端服务
- Android（LiteRT 本地模型）
- iOS
- Web（JS/WasmJS）

这对需要「云端调度 + 移动端执行」的混合场景很有价值。例如，Mercedes-Benz 团队已经在用 Koog 构建车载维护支持 Agent。

## 与主流 Agent 框架的定位差异

| 维度 | Koog 1.0 | LangGraph | CrewAI | AutoGen/AG2 |
|------|----------|-----------|--------|-------------|
| 语言生态 | Kotlin/Java | Python | Python | Python |
| 稳定性承诺 | 1年无breaking | 无 | 无 | 无 |
| 多平台 | JVM/Android/iOS/Web | Python only | Python only | Python |
| 企业集成 | Spring Boot/Ktor | LangSmith | 发展中 | Azure |
| 观测 | 全平台 OpenTelemetry | LangSmith | 发展中 | 发展中 |

笔者的判断：**Koog 不是要抢 LangGraph 的市场份额，它服务的是已经深度使用 Kotlin/JVM 的企业团队**。这类团队如果要用 Agent 技术，以前没有好的选择，现在有了。这是填补空白，不是正面竞争。

## 谁应该关注 Koog 1.0

**应该关注**：
- JVM/Kotlin 生态的企业开发团队，需要生产级 Agent 基础设施
- 对 API 稳定性有强需求，不愿意每季度重构一次的团队
- 有多平台部署需求（移动端 + 服务端）的场景
- 已经在使用 JetBrains 工具链的团队

**可以跳过**：
- Python 优先的团队，LangGraph/CrewAI 生态更成熟
- 需要最新特性的团队，Stable 模块会落后 Beta 模块几个版本
- 小型项目或快速原型阶段，Koog 的企业复杂度可能过高

## 一句话总结

Koog 1.0 做出了一件很多 Agent 框架不愿意做的事：**承诺 API 在一年内不破坏**。对于 JVM 生态的企业来说，这比任何新功能都值钱。