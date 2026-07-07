# Article Types 规范

> **2026-07-07 起草**：FSIO 反馈后建立，目的是防止 R670+ 的设计漂移（每轮创建 monitoring 文件）再次发生。

---

## 两种文章类型

| 类型 | 目标读者 | 来源 | 文件位置 | 是否可发头条 |
|---|---|---|---|---|
| **independent** | 头条读者 / GitHub 访客 | 一手源（Anthropic / OpenAI / Cursor / Claude Code 等官方资料） | `articles/<category>/<topic>-<year>.md` | ✅ |
| **monitoring** | 仓库维护 Agent 系统 | R-round 监测数据（⭐ / cluster signal / calibration） | **不入库**（仅写入 README 表格 + HISTORY.md + state.json） | ❌ |

---

## 命名规范（强制）

### ✅ 允许的命名模式（independent）

```
articles/orchestration/multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md
articles/orchestration/multi-agent-stack-r667-harness-protocolization-empirical-layering-2026.md
articles/orchestration/multi-agent-stack-r668-skill-registry-primitive-horizontal-decoupling-deep-dive-2026.md
articles/projects/ogulcancelik-herdr-agent-multiplexer-rust-11903-stars-2026.md
articles/projects/coreyhaines31-marketingskills-vertical-skill-registry-marketing-36347-stars-2026.md
```

**核心特征**：
- 文件名是**主题词**（harness protocolization / skill registry / herdr multiplexer）
- 即使含 `r\d{3}`，也是**主题版本号**（如 R666 是 deep dive 演进版本），不是监测轮次

### ❌ 禁止的命名模式（monitoring）

```
articles/orchestration/multi-agent-stack-r682-phase-5-cluster-signal-sustained-4of7-12rounds-cumulative-calibration-...md
articles/projects/langchain-ai-openwiki-7256-stars-r682-7k-sustained-explosive-14th-sustained-confirmed-2026.md
articles/projects/ogulcancelik-herdr-12039-stars-r670-layer-1-multiplexer-2026.md
```

**核心特征**：
- 文件名是**监测状态码**（phase-5-cluster-signal / sustained-4of7 / 12rounds-cumulative-calibration）
- 含 R\d+-phase / R\d+-cluster / R\d+-stars-R\d+ / R\d+-rebound / R\d+-baseline-boost / R\d+-calibration

---

## monitoring 数据应该写到哪里？

如果只有 monitoring 数据，没有新独立主题：

1. **`articles/projects/README.md`**：项目 ⭐ 增长记录
2. **`.agent/HISTORY.md`**：本轮决策 + 监测数据 + 预测
3. **`.agent/state.json`**：机器可读状态
4. **`.agent/sources_tracked.jsonl`**：源追踪（追加 record）

**禁止**创建独立 `.md` 文件。

---

## 为什么？

### R229 ~ R663 时期（健康期）

- 每轮产 1 篇独立主题深度解读（基于一手源）
- 项目 ⭐ 更新到 README 表格
- monitoring 数据写入 HISTORY.md
- **仓库干净：每项目 1 个文件，每轮 1 篇文章**

### R670 漂移（2026-07-06）

- 引入了 "每项目每轮新建 R\d+ UPDATE 文件" 模式
- 引入了 "Phase 5 Cluster Signal" monitoring 概念
- 8 个项目 × R670 = 8 个 monitoring 文件
- R671+ 进一步扩展到 orchestration/multi-agent-stack-r\d+-phase-5-cluster-signal 系列
- **仓库污染：~50 篇 monitoring 文件，标题全是"⭐⭐⭐ SUSTAINED ⭐⭐⭐"**

### 后果

- 头条发布脚本误把这些 monitoring 当成可发布候选
- 头条草稿箱出现 50+ 篇怪异文章
- 仓库质量下降
- FSIO 不得不手工 gate

---

## 修复方案（已实施）

1. **2026-07-07**：`write_phase.py` 的 `spawn_write_agent()` prompt 加了硬性约束，明确禁止 monitoring 类文件
2. **2026-07-07**：`write_phase.py` 加了 `validate_article_filename()` 函数，自动删除违规文件并推飞书告警
3. **2026-07-07**：删除 52 篇 R670+ 的 monitoring 文件（orchestration 15 + projects 37）
4. **2026-07-07**：ARTICLES_MAP.md 加 Type 列（monitoring | independent）

---

## 维护原则

> **仓库里的每篇文章必须能回答一个问题："一个对该领域感兴趣的技术读者会想读这篇文章吗？"**

- ✅ 答 yes → independent，可发头条
- ❌ 答 no → monitoring，不入库，写到 README + HISTORY

---

## 违反规范的处理

`write_phase.py` 的 `validate_article_filename()` 会自动：

1. 检测文件名是否命中禁止模式
2. **自动删除违规文件**
3. **推送飞书告警** 给 FSIO

如果未来 LLM 写出 monitoring 类文章，会被立即清理。

---

## 参考

- SKILL.md：第 92-156 行核心工作流（每轮必产出 1 篇独立主题）
- references/round-349-orphan-cleanup-r341-second-verification-eval-cluster-0to1.md：R-round 设计起源
- .agent/gen_article_map.py：含 `classify_article()` 自动分类
- scripts/write_phase.py：含 `validate_article_filename()` 自动检查