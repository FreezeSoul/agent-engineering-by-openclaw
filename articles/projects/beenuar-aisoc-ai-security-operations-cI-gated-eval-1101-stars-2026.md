# AiSOC：开源 AI SOC，含 CI-Gated Eval Harness 的自托管安全运营平台

> **来源**: [github.com/beenuar/AiSOC](https://github.com/beenuar/AiSOC) · 1,101 Stars · MIT License

## 核心命题

安全运营（AISOC）的核心问题不是"AI 能不能分析安全事件"，而是"AI 的分析过程能不能被审计、复现和自动化回归"。

> "The agent's prompts, tool calls, and rationale are logged step-by-step and replayable."

AiSOC 解决的是这个问题：**每一次 AI 决策都有完整 Investigation Ledger**，而且这个 Ledger 可以回放、可以重放、可以在 CI 里做自动化回归。

---

## 一、这个项目解决什么问题

传统的安全运营中心（SIEM）依赖规则引擎和人工研判，效率低、误报高、且 AI 分析结果不可审计。

AiSOC 的核心价值主张：

```
┌─────────────────────────────────────────────────────────────┐
│  Ingest → Correlate → Investigate → Surface                │
│  安全事件摄取 → 关联分析 → AI 调查 → 结果呈现                │
└─────────────────────────────────────────────────────────────┘
```

关键差异在于 **Investigation Ledger**：

> "The Investigation Ledger stores the LLM prompt, the response, the evidence cited, and the downstream tool calls for every step of every run."

这意味着：每一次 AI 安全分析，都有一个完整的执行轨迹可以回放。这对于事后溯源、合规审计、误报分析都至关重要。

---

## 二、评测体系：最有价值的部分

AiSOC 真正有价值的地方，不是它的 AI 调查能力，而是它的 **公开评测框架**。

### 五套评测（每套 CI-Gated）

| Suite | 目标 | 数据规模 |
|-------|------|---------|
| MITRE-tactic Gate | 战术分类准确性 | 55 templates × 200 incidents |
| Investigation-completeness Gate | 调查完整性 | 同上 |
| Response-quality Gate | 响应质量 | 同上 |
| Alert-reduction Gate | 告警降噪效果 | 1,000 alerts 固定流 |
| Schema/coverage Gate | 数据源覆盖 | ~360 events × 14 log sources |

### 关键设计决策

**Per-template macro 分解**：

> "each reporting both a per-case mean and a per-template macro so a single broken template can't hide behind 199 working duplicates"

这个设计解决了评测中的一个经典问题：当某类测试场景的模板失效时，200 个其他模板的平均分会把它掩盖掉。Per-template macro 确保每个模板的失效都能被显式看到。

**固定告警流真实测量**：

> "Alert reduction is a real measurement against the fixed alert stream; the three rubric-based suites are substrate self-consistency gates over deterministic templates."

Alert reduction 不是模拟出来的，而是用固定的含噪告警流真实测量。这比纯模拟更接近真实运营环境。

**14 个日志源覆盖**：

```
Sysmon · Windows Security · M365 audit · Azure sign-in
CloudTrail · Linux auditd · journald · EDR · DNS
web access · Kubernetes audit · GitHub audit · VPN · DB audit
```

覆盖了主流企业安全数据源，评测数据可移植性强。

---

## 三、技术架构

### 部署方式

- **Fly.io Demo**：tryaisoc.com（随时可能离线，因为运行在维护者本地）
- **Render 一键部署**：适合快速验证
- **Docker Compose**：适合自托管
- **Airgap 模式**：适合隔离环境

### 开源协议

MIT License。Agent 代码和 Substrate 均可读、可分叉、可替换。

> "The agent and the substrate are MIT-licensed, so you can read, fork, or replace either of them."

这一点与多数闭源 AI SOC vendor 不同——你不需要信任厂商的黑盒系统，可以自己审计代码。

---

## 四、与同类项目对比

| 维度 | AiSOC | 闭源 AI SOC |
|------|-------|------------|
| 部署方式 | 自托管（Docker/Render/Fly.io）| SaaS / 私有化 |
| Agent 决策可审计性 | ✅ 完整 Investigation Ledger | ❌ 通常黑盒 |
| Eval 框架 | 公开，CI-gated | 通常不公开 |
| 协议 | MIT | 商业许可 |
| 数据源覆盖 | 14 个主流日志源 | 各家不同 |

---

## 五、笔者判断

AiSOC 最有价值的地方不是它的 AI 调查能力（这类能力现在有大量开源项目在做），而是它的 **评测体系公开且可复现**。

对于任何做安全 Agent 的团队来说：

1. **可以直接使用 AiSOC 的评测框架**作为自己安全 Agent 的 benchmark
2. **可以用 Investigation Ledger 设计**作为自己 Agent 可观测性的参考
3. **可以参考 Schema Coverage 测试**来验证自己的数据源覆盖完整性

> "The benchmark page explains exactly which is which."

这种透明度是闭源系统无法提供的。

---

**关联 Article**: [Anthropic 长时运行 Agent 评测框架：CI-Gated Eval 的工程实践](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/deep-dives/anthropic-effective-harnesses-long-running-agents-ci-gated-eval-2026.md)（两者在评测设计哲学上高度一致：per-template macro 分解、固定流真实测量、CI-gated）

**引用来源**：
- [AiSOC README.md](https://github.com/beenuar/AiSOC)
- [AiSOC Benchmark Documentation](https://github.com/beenuar/AiSOC/apps/docs/docs/benchmark.md)