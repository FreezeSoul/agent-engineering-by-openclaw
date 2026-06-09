# repowise-dev/repowise：AI-Native 工程团队的代码库情报层

> repowise 是给 Claude Code / Codex /任何 MCP兼容 Agent用的「代码库情报层」——把 dependency graph、git history、自动文档、架构决策记录、**缺陷校准的 Code Health评分**这5 层情报，通过9 个 MCP工具暴露给 Agent。它解决了 AI-Native 工程团队在 [Running an AI-native engineering org](articles/enterprise/anthropic-running-an-ai-native-engineering-org-2026.md) 一文中提出的核心问题：**当 Agent 生成大量代码时，工程团队如何快速验证 +量化质量？**

---

##核心定位

|维度 | 内容 |
|------|------|
| **Stars** |2,247 |
| **License** | AGPL-3.0 |
| **创建时间** |2026-03-23 |
| **最后更新** |2026-06-09 |
| **语言** | Python3.11+ |
| **核心接口** | CLI +9 个 MCP工具 + Local Dashboard |
| **覆盖语言** |15 种（tree-sitter解析）|
| **差异化** | ★ **Code Health 是其他工具做不到的层** |

> "Five intelligence layers · Nine MCP tools ·15 languages · Multi-repo workspaces · One `pip install`"
> — repowise README

---

##5 个 Intelligence Layers

repowise一次性构建、每次 Commit 自动同步。每个 Layer都可通过 CLI、MCP工具、Local Dashboard 查询：

| Layer | 提供什么 |差异化点 |
|--------|---------|---------|
| **◈ Graph** | tree-sitter跨15 种语言的依赖图 ·2 层 file/symbol节点 ·3 层 call resolution · Leiden communities · PageRank / centrality / execution flows ·框架感知的 route→handler edges | **真正构建 graph**，不是简单的引用计数 |
| **◈ Git** | hotspots (churn × complexity) · ownership % · co-change pairs (隐藏耦合) · bus factor ·贡献者画像 · 模块健康度 · reviewer建议 | **行为信号**，静态分析看不到 |
| **◈ Docs** | LLM生成的 module/file wiki ·每次 commit增量更新 · freshness + confidence评分 · hybrid RAG搜索 (FTS + vector via RRF) | **保持当前**——每次 commit重建 |
| **◈ Decisions** | 从 **8 个来源**挖掘的架构决策 ·证据支持（verified / fuzzy / unverified）·链接到 graph nodes · `supersedes`/`refines`/`conflicts_with`边 · staleness tracking | **★无人能做到** |
| **★ Code Health** | **25 个确定性 biomarker**,1-10 分文件级评分 ·缺陷校准权重 · coverage ingestion ·趋势告警 · refactoring targets · **零 LLM 调用, <30 秒** | **★缺陷验证 ——我们的护城河** |

---

##★ Code Health：这一层无人能做

Code Health 是 repowise最有差异化的一层，**也是唯一能被证明预测真实 Bug 的层**：

-25 个确定性 biomarker：McCabe complexity、deep nesting、brain methods、class cohesion (LCOM4)、god classes、native Rabin–Karp clone detection、**未测试的 hotspots**、function-level churn、code-age volatility、ownership dispersion、change entropy、co-change scatter、prior-defect history、test-quality smells等等
-1-10 分文件级评分
-权重**经过真实缺陷语料校准**，不是手工调出来的
- **零 LLM 调用 ·零云依赖 ·零新运行时依赖** ——纯 Python over tree-sitter + git data
-3,000 个文件的代码库 **30 秒内完成**

```bash
repowise health # KPIs +最低分文件
repowise health --coverage cov.lcov #摄入 LCOV/Cobertura/Clover → 未测试热点
```

**这是 AI-Native 工程团队的关键工具**：当 Agent 生成大量代码，**没有可量化的"代码健康分"，验证瓶颈就无法系统化解决**。

---

##9 个 MCP工具

通过 Model Context Protocol，repowise 把这5 层情报暴露给 Claude Code / Codex /任何 MCP兼容 Agent：

- Agent 可以直接问："**为什么 auth 这样工作？**" 而不是"**auth.ts 里有什么？**"
- **更少的工具调用、更少的文件读取、更低的每次查询成本**，答案质量相当（见下方 benchmarks）

---

##Benchmark 数据

repowise 自己发布的 benchmark 数据：

|维度 |改进 |
|------|------|
|工具调用数 |显著减少 |
| 文件读取数 |显著减少 |
| 单次查询成本 |显著降低 |
|答案质量 |相当 |

（具体数字见 repowise docs/INTELLIGENCE_LAYERS.md）

---

##快速上手

```bash
pip install repowise
repowise init #一次性索引
#之后每次 commit 自动同步
```

---

##闭环逻辑

本文与 `articles/enterprise/anthropic-running-an-ai-native-engineering-org-2026.md` 形成 Article × Project闭环：

| 文章主张 | Project体现 |
|---------|------------|
|验证瓶颈是 AI-Native 的核心约束 | Code Health 层提供**缺陷预测性的验证** |
| Claude-assisted commits接近100% | 通过 MCP工具，Agent 直接查询"哪些文件健康度最低" |
| PR cycle time 是关键指标 | Git layer 提供 **co-change pairs + ownership % + reviewer suggestions**，加速 PR流转 |
| Trust but verify（Claude 做 style/bug，Human 做 judgment） | **Code Health 自动评分** = Claude层的可量化输出，Human review聚焦于 judgment 而非 lint |

**共同命题**：AI-Native 工程组织转型 = **流程改造 +工具升级 +指标体系** 三者缺一不可。本文（文章）讲流程改造；repowise（项目）讲工具升级 +指标体系。

---

## 为什么这个 Project值得推荐

1. **2,247 stars增长稳健**（3 月创建至今约2.5 个月）
2. **AGPL-3.0许可** ——商业 fork需谨慎，但自托管团队友好
3. **Python3.11+ 实现** ——易于理解和扩展
4. **缺陷验证的 Code Health** —— 不是又一个"代码质量 lint工具"，而是基于真实缺陷语料校准的预测模型
5. **MCP 原生集成** —— 与 Claude Code / Codex /未来 Agent协议对齐
6. **AGPL vs商业 Hosted 双轨** ——团队可自托管，企业可付费 hosted

**潜在风险**：
- AGPL-3.0 对商业产品不友好（使用需开源衍生作品或购买商业许可）
- Code Health 的25 个 biomarker权重基于其私有缺陷语料，可能不直接适用于所有代码库

---

## 来源

- **仓库**：[repowise-dev/repowise](https://github.com/repowise-dev/repowise)
- **官网**：[repowise.dev](https://www.repowise.dev)
- **文档**：[docs.repowise.dev](https://docs.repowise.dev)
- **创建时间**：2026-03-23
- **最后更新**：2026-06-09
