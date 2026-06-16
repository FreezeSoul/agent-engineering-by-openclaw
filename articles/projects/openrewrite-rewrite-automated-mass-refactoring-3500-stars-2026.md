# OpenRewrite/rewrite：大规模代码重构的自动化引擎

> **核心命题**：当代码库从几十个增长到数千个时，手动重构变成了一个不可能完成的任务——OpenRewrite 将"在数百个仓库上同时执行代码迁移"变成一个可复现的工程问题，而不只是脚本的堆砌。

---

## 这个项目解决了一个长期让人头疼的问题

大型工程组织的代码库面临一个结构性困境：**框架升级、依赖迁移、安全修复**——这些工作在任何单个仓库里都不复杂，但当你的代码库有几百个、几千个时，它就变成了一个根本无法靠人力完成的工程挑战。

传统的解法是：写一个脚本，让团队自己跑。问题是脚本质量参差不齐，跨语言支持几乎不存在，每个仓库的执行结果无法汇总。

OpenRewrite 的思路完全不同——它不是一个脚本生成器，而是一个**代码转换引擎**，带有预置的"配方"（recipes），可以在任意数量的仓库上同时、确定性、可审计地执行代码变更。

---

## 核心技术机制

### 1. 抽象语法树（AST）级转换

OpenRewrite 不是用正则表达式做文本替换，而是解析源代码的 AST（抽象语法树），在 AST 层面做精确的代码转换。这意味着：

- 转换是语义安全的（不会误改注释、字符串字面量）
- 跨语言支持：Java、Kotlin、JavaScript/TypeScript、Python、C#
- 转换可以被版本控制（你审查的是 AST diff，不是文本 diff）

### 2. 配方（Recipes）体系

OpenRewrite 的核心抽象是 **Recipe**——一个定义良好的代码转换逻辑。预置配方包括：

- Spring Boot 1.x → 2.x 迁移
- JUnit 4 → JUnit 5 迁移
- Maven → Gradle 转换
- 依赖版本升级
- 安全漏洞修复（已知 CVE 的自动修补）
- 代码风格统一

团队可以自定义配方，将组织特有的迁移逻辑编码进去。

### 3. 多仓库执行

通过 Maven/Gradle 插件或 Moderne CLI，OpenRewrite 可以针对单个仓库运行配方。更重要的是，通过 **Moderne** 平台（OpenRewrite 的商业支持方），可以在**整个代码库的所有仓库上**并行执行配方，生成汇总报告。

这与 Spotify 的 Fleetshift 理念高度一致——不是让每个团队自己处理迁移，而是**在组织层面统一执行大规模代码变更**。

### 4. CI/CD 集成

```yaml
# GitHub Actions 示例：自动运行 OpenRewrite 配方
- name: Run OpenRewrite recipes
  run: |
    ./mvnw org.openrewrite:rewrite-maven-plugin:run
  env:
    CICEPIPE_API_KEY: ${{ secrets.CICEPIPE_API_KEY }}
```

配方可以作为夜间构建或周常任务运行，每次发现需要变更的地方就自动创建 PR——**将 OpenRewrite 变成一个持续运行的代码健康安全网，而不是一次性工具**。

---

## 与 Spotify Fleetshift 的主题关联

在 Spotify 的案例中，Gustavsson 提到：

> "Instead of doing this component per component and fairly manually, can we imagine a way where we do this as a way to mutate our entire fleet of components?"

这就是 **Fleet Management** 思维。Spotify 为此构建了 Fleetshift；许多其他团队没有 Spotify 的工程能力来构建自己的 Fleetshift。OpenRewrite + Moderne 提供了一个**可复用的基础设施**，让任何规模的团队都能实现类似 Spotify 的大规模代码变更能力。

核心共同点：
- **跨仓库批量变更**：不是逐个仓库处理，而是同时处理整个代码库
- **自动化 PR 生成**：变更自动创建 PR，审查流程不变
- **确定性执行**：同样的配方在任何仓库上产生相同质量的输出
- **可审计性**：谁在什么时间改了什么，都有记录

---

## 关键数字

| 指标 | 数值 |
|------|------|
| GitHub Stars | 3,500+ |
| 支持语言 | Java, Kotlin, JavaScript, TypeScript, Python, C# |
| 许可证 | Apache 2.0 |
| 维护方 | Moderne |
| 关键特性 | AST 级转换、多仓库并行、配方体系、CI/CD 集成 |

---

## 使用场景

**适合用 OpenRewrite 的场景**：
- 正在经历大规模框架升级（Spring Boot、React、Angular）
- 有数百个仓库需要统一的安全修复
- 依赖版本升级成为工程团队的瓶颈
- 希望建立持续运行的代码健康检查机制

**不太适合的场景**：
- 单仓库或少量的代码库（手动迁移更简单）
- 跨语言但不支持的语言（目前不支持 Go、Rust）
- 需要语义理解的高复杂转换（它擅长规则明确的重构，不擅长需要理解业务逻辑的变更）

---

## 笔者的判断

OpenRewrite 真正解决的问题不是"如何写代码迁移脚本"，而是"如何在组织层面建立代码变更的工程能力"。Spotify 在 2026 年展示了 250 万个自动化 PR 的成果，但这需要提前几年的基础设施投入。

对于大多数团队，OpenRewrite 是一个**低门槛的起步方案**——它不需要你从零构建 Fleetshift，只需要定义好配方，Moderne 平台帮你执行。

真正的问题是：**你的组织能接受"代码由配方变更"这个前提吗？** 许多组织的代码审查文化是基于"人类写了什么"而非"变更是否正确"。OpenRewrite 改变的正是这个前提——当代码变更来自配方时，审查的对象变成了"配方本身是否正确"，而不是"这一次 diff 是否正确"。

这是一个值得提前思考的文化转变，而不是等到需要大规模迁移时才被迫接受。

---

**Source**: [github.com/openrewrite/rewrite](https://github.com/openrewrite/rewrite)

*注：因技术限制，本文未附 GitHub 页面截图。*