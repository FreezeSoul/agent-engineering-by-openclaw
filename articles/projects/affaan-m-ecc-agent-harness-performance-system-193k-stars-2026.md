# affaan-m/ECC：193K Stars 的 Agent Harness 性能优化系统

> **核心判断**：ECC 不是配置包，而是一个完整的 Agent 操作层——它把你在实际项目中打磨了 10+ 个月的工程经验（Skills、Instincts、Memory 优化、安全扫描、研究驱动开发）固化成可复用的 Harness 系统。这个项目真正解决的不是「配置问题」，而是「如何让你的 Agent 在长任务中持续保持高质量输出」的问题。

---

## 一、它解决了一个什么级别的问题

大多数开发者在用 Agent 时面临一个困境：**Agent 在简单任务上表现惊艳，但在复杂的长任务上迅速崩溃**——上下文腐烂、工具调用错误累积、内存泄漏、质量逐渐下降。

解决这个问题的常见思路是「调调 prompt、加几个工具」。ECC 的思路完全不同：它认为 Harness 本身就是一个**性能优化系统**，需要从工具层、内存层、安全层、评估层全面介入。

官方对自己的定位：

> 「Not just configs. A complete system: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development. Production-ready agents, skills, hooks, rules, MCP configurations, and legacy command shims evolved over 10+ months of intensive daily use building real products.」

这就是它与普通配置包的核心区别——**它是在生产环境中持续迭代出来的工程系统，不是设计文档里的理想主义配置**。

---

## 二、核心技术能力

### 2.1 Skills 系统（246 个可复用技能）

ECC 提供了 61 个 Agent 和 246 个 Skills，覆盖了编码工作中的高频场景：

- **优化类**：并行执行优化器、基准测试优化循环、数据吞吐量加速器、延迟关键系统优化
- **内存类**：会话上下文压缩、跨会话持久化记忆
- **安全类**：安全扫描、权限管控、Secret 检测
- **研究类**：研究驱动的开发工作流

这些 Skills 不是简单的 prompt 模板，而是**可以在实际任务中直接调用的工程组件**。

### 2.2 Instincts（本能反应系统）

Instincts 是 ECC 的一个核心概念——让 Agent 在特定场景下形成「本能反应」，而不需要每次都重新推理应该怎么做。

类比人类开发者：你看到一个 NPE（空指针异常）不会去思考调用哪个工具，而是直接想到「检查 null」。Instincts 就是给 Agent 建立类似的**条件反射型能力**。

### 2.3 Hook 系统（v1.8.0 核心升级）

ECC v1.8.0 把自己重新定位为「Harness Performance System」，其中最关键的升级是 **Hook 可靠性改造**：

| 能力 | 说明 |
|------|------|
| SessionStart root fallback | 会话启动时的兜底机制 |
| Stop-phase session summaries | 任务结束时的会话摘要 |
| Script-based hooks | 用脚本替代脆弱的 inline one-liners |
| Runtime controls | `ECC_HOOK_PROFILE` 和 `ECC_DISABLED_HOOKS` 运行时控制 |

> 「Hook reliability overhaul — SessionStart root fallback, Stop-phase session summaries, and script-based hooks replacing fragile inline one-liners.」

这解决了 Harness 中一个长期被忽视的问题：**Hook 的脆弱性**。当 Hook 以 one-liner 形式写在配置里时，任何格式错误都会导致整个 Harness 失效。ECC 把这些逻辑提取成独立脚本，大幅提升了可维护性。

### 2.4 NanoClaw v2（模型路由与热加载）

NanoClaw v2 是 ECC 的核心引擎，提供：

- **模型路由**：自动选择最适合当前任务的模型
- **Skill 热加载**：不重启会话的情况下加载新 Skill
- **会话管理**：branch/search/export/compact/metrics

这个功能让 ECC 能够在运行时动态调整 Agent 的能力组合，而不是在会话开始前就固定所有配置。

### 2.5 跨 Harness 一致性

ECC 支持 Claude Code、Cursor、OpenCode、Codex CLI、Gemini CLI 等多个主流 Agent——不是简单支持，而是**在行为上保持一致性**：

> 「Cross-harness parity — behavior tightened across Claude Code, Cursor, OpenCode, and Codex app/CLI. 997 internal tests passing.」

这种跨平台一致性意味着：你在 Claude Code 上调试的工作流，可以直接迁移到 Cursor 或 Codex 上运行，而不需要重新配置。

---

## 三、与 Cursor Harness 工程的关联

本轮 Article 分析了 Cursor 的两篇 Harness 工程博客，而 ECC 恰好是 Cursor 提出的那些工程原则的**民间实现版本**：

| Cursor 提出的 Harness 原则 | ECC 对应实现 |
|------------------------|------------|
| 开发环境就是产品 | 61 Agents + 246 Skills 的环境构建能力 |
| 持久化执行是基础设施 | Hook 系统的 SessionStart/SessionStop 持久化 |
| 三层状态分离 | NanoClaw 的模型路由 + 会话分离架构 |
| 评估驱动演进 | Benchmark Optimization Loop 内置评估 |
| 赋能而非管控 | Skills/Instincts 体系把能力交给 Agent |

ECC 的创始背景也印证了这一点——它来自 **Anthropic Hackathon 获奖作品**，作者将自己在真实项目中 10+ 个月的 daily use 经验持续沉淀到这套系统里。

---

## 四、使用方式与上手

### 安装

ECC 以 Claude Code Plugin 形式分发，安装简单：

```bash
# 直接作为 Claude Code plugin 安装
# 或者手动拷贝需要的组件
```

### 核心命令

| 命令 | 用途 |
|------|------|
| `/harness-audit` | 审计当前 Harness 配置的健康度 |
| `/loop-start` | 启动强化版 Agent Loop |
| `/loop-status` | 查看 Loop 状态和性能指标 |
| `/quality-gate` | 在关键节点执行质量门禁 |
| `/model-route` | 动态切换模型路由 |

### 运行时配置

```bash
# 控制 Hook 行为级别
ECC_HOOK_PROFILE=minimal|standard|strict

# 禁用特定 Hook
ECC_DISABLED_HOOKS=session_summary,security_scan
```

---

## 五、项目元数据

| 维度 | 数据 |
|------|------|
| **Stars** | 193,905（今日+29,920）|
| **Forks** | 29,930 |
| **语言** | JavaScript（60%）、Rust（30%）、Python（5%）|
| **License** | MIT |
| **创建时间** | 2026-01-18 |
| **最新版本** | v2.0.0-rc.1（2026-05-25）|
| **贡献者** | 190 人 |
| **主页** | https://ecc.tools |

---

**引用来源**：

- GitHub: [affaan-m/ECC](https://github.com/affaan-m/ECC)（193K Stars）
- ECC 官网: [https://ecc.tools](https://ecc.tools)
- v2.0.0-rc.1 Release Notes: [ECC GitHub Releases](https://github.com/affaan-m/ECC/releases)