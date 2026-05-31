# JetBrains Koog：第一个承诺一年不破的 JVM Agent 框架

> 项目：https://github.com/JetBrains/koog
> Stars：~4,000 | Fork：358 | 语言：Kotlin (89%), Java | License：Apache 2.0
> 发布：2026-05-29（Koog 1.0 正式版）| 来源：JetBrains AI Blog + GitHub Release

---

## 核心命题

Koog 是 JetBrains 推出的开源 JVM Agent 框架，1.0 版本最大的变化不是新功能，而是**明确承诺一年不破坏 API**——这是 Agent 框架领域少有的稳定性宣言，瞄准的是被 LangChain/.AutoGen 迭代速度折腾得疲惫的企业 JVM 团队。

![GitHub](screenshots/jetbrains-koog-20260601.png)

## 亮点描述

**稳定性承诺是最大的功能**

1.0 的核心改变是 stability pledge：stable 模块保证至少一年内无 breaking changes，模块分成 Stable 和 Beta 两层。企业在选型时终于可以问「这个能用多久」而不是「这个版本能撑几个月」。

> "Modules now ship under two streams — stable and beta — so production code can pin to APIs that won't break without a deprecation cycle." — Koog 1.0 Release Notes

**真正的 Java 互操作**

Java 团队不需要理解 Kotlin 协程，统一的 `xxxBlocking` API 让 Java 调用方直接用标准 Executor。死锁问题（Kotlin → Java → Kotlin 单线程调用链）也在 1.0 中修复。

**跨平台观测不需要妥协**

OpenTelemetry 覆盖所有 Koog 目标平台（JVM/Android/iOS/Web），内置 `gen_ai.client.token.usage` 等标准 metrics，直插 Prometheus/Grafana。

**Anthropic Prompt Caching 框架级支持**

Cache control 做成了端到端框架支持，长系统 prompt 的 Agent 直接受益，不需要自己管理缓存逻辑。

## 技术原理

Koog 的核心设计是**图 DSL（Graph DSL）**，Agent 的执行逻辑建模为有向图，节点是 LLM 调用/工具执行/判断分支，边是状态流转。这个设计让 checkpoint/restore（Agent 状态快照）成为框架级原生能力，而不是社区插件。

关键架构决策：
- **持久化优先**：Checkpoint 机制从一开始就是核心设计，不是后来加的
- **HTTP 传输解耦**：不再强依赖 Ktor，支持 OkHttp/Java HTTP Client/Spring RestClient
- **多平台目标**：Kotlin Multiplatform 覆盖 JVM/JS/WasmJS/Android/iOS，一套代码多端部署

## 竞品对比

| 维度 | Koog | LangGraph | CrewAI |
|------|------|-----------|--------|
| 稳定性承诺 | ✅ 1年 | ❌ 无 | ❌ 无 |
| 语言 | Kotlin/Java | Python | Python |
| 多平台 | ✅ JVM/iOS/Android/Web | ❌ Python only | ❌ Python only |
| 企业集成 | Spring Boot/Ktor | LangSmith | 发展中 |
| Stars | ~4K | 12K | 28K |

笔者的判断：**Koog 不是 LangGraph 竞品，它服务的是 Kotlin/JVM 生态里被 Python 框架排除在外的企业团队**。这类团队以前没有生产级选择，现在有了。Stars 数量不代表技术优劣，代表的是受众大小——JVM 开发者本就是小众。

## 落地指引

**适合场景**：
- 已经在用 Kotlin 的企业，需要把 Agent 能力嵌入现有 JVM 应用
- Spring Boot/Ktor 团队，不想为 Agent 引入新的技术栈
- 需要移动端（Android/iOS）部署能力的混合场景
- 对 API 稳定性有强要求，不愿意每季度升级一次

**上手路径**：
```bash
# Gradle (Kotlin)
implementation("ai.koog:koog-core:1.0.0")

# Maven
# <dependency>
#   <groupId>ai.koog</groupId>
#   <artifactId>koog-core</artifactId>
#   <version>1.0.0</version>
# </dependency>
```

文档：https://docs.koog.ai/

**需要知道的风险**：
- 社区生态比 LangGraph 小很多，遇到问题更依赖官方文档
- Stable 模块会滞后于 Beta 模块的能力，不适合追逐最新特性
- 4K Stars 的生态活跃度，企业选型时需要评估长期维护风险

## 引用

> "Koog is a Kotlin-based framework designed to build and run AI agents entirely in idiomatic Kotlin and Java API." — GitHub README

> "For agents written in Kotlin, deploy agents across JVM, JS, WasmJS, Android, and iOS targets using Kotlin Multiplatform." — Koog Key Features Docs

## 关联文章

- [JetBrains Koog 1.0：第一个承诺「一年不破坏」的 JVM Agent 框架意味着什么](./jetbrains-koog-1-stable-api-enterprise-jvm-2026.md)（同轮 Article）