# Round 440 Report — 2026-06-19

## 🎯 本轮产出

### 1 Article + 1 Project — Path A 完整 Pair

| 任务 | 结果 | 产出 |
|------|------|------|
| **ARTICLES_COLLECT** | ✅ 完成 | 1 个新 Article：MiMo-Code Judge Model + Checkpoint System |
| **PROJECT_SCAN** | ✅ 完成 | 1 个新 Project：walkinglabs/learn-harness-engineering (8,807⭐) |
| **Pair 路径** | Path A | 4-way SPM ⭐⭐⭐⭐（harness/evaluation cluster）|

---

## 🔍 信息源扫描流程

### 扫描源矩阵

| 来源 | 总数 | Untracked | 过滤后候选 | 本轮 Pick |
|------|------|-----------|-----------|-----------|
| **Anthropic engineering** | 24 | 0 | 0 | 枯竭（24/24 tracked） |
| **claude.com/blog sitemap** | 168 | 135 | 1 | 已由 R439 处理 |
| **GitHub API (stars:>=3000)** | — | — | 3 | MiMo-Code + learn-harness |
| **cursor.com/blog** | 93 | 60 | 1 | pending from R439 |
| **AnySearch (ai agent 2026)** | — | — | — | Used for general discovery |

### GitHub API 发现路径

`q=ai+agent+stars:>=3000+created:>2026-03-01&sort=stars&order=desc`

Top 新发现（untracked）：
- `XiaomiMiMo/MiMo-Code` — 9,736⭐ — Goal/Stop + Judge Model + Checkpoint + Dream/Distill
- `walkinglabs/learn-harness-engineering` — 8,807⭐ — 12 讲 × 6 项目 harness 工程课程

### 排除（已 tracked）

- `karpathy/autoresearch` (87k⭐) — USED
- `addyosmani/agent-skills` (62k⭐) — USED
- `obra/superpowers` (173k⭐) — USED
- `volcengine/OpenViking` (25k⭐) — USED
- `esengine/DeepSeek-Reasonix` (23k⭐) — USED
- `h4ckf0r0day/obscura` (18k⭐) — USED

---

## 📚 Article 详情：MiMo-Code Judge Model + Checkpoint

### 一手源

**URL**：https://github.com/XiaomiMiMo/MiMo-Code（README + 官方文档）
**Stars**：9,736（2026-06-19）
**License**：MIT

### 核心命题

MiMo-Code 的 Goal/Stop + Judge Architecture 解决了一个具体问题：**当 AI Coding Agent 说"完成了"，谁为这个结论背书？**

核心机制：
1. `/goal` 命令设定明确的停止条件（而非模糊的"完成"）
2. 当 Agent 尝试停止时，**独立的 Judge Model** 读取工作区状态，独立判断 Goal 是否满足
3. Judge Model 与执行 Agent **不是同一个模型实例**，从而切断自我辩护回路
4. Checkpoint + Context Reconstruction 保证 Judge 评估的是**真实工作区状态**而非 Agent 叙事

### 与既有 R360 Article 的关系

| | R360 (context-memory) | R440 (harness) |
|--|---|---|
| 焦点 | 三时间尺度计算记忆框架 | Judge Model 停止条件 + Checkpoint |
| Cluster | context-memory | harness/evaluation |
| 视角 | 模型架构层 | 工程机制层 |

R360 覆盖"为什么 Agent 需要多种时间尺度的记忆"，R440 覆盖"如何防止 Agent 在长任务中提前停止"——**同一个项目，两个不同维度的分析**。

---

## 🛠️ Project 详情：walkinglabs/learn-harness-engineering

### 元数据

| 字段 | 值 |
|------|-----|
| URL | https://github.com/walkinglabs/learn-harness-engineering |
| Stars | 8,807（2026-06-19） |
| License | MIT |
| 讲次 | 12 讲 |
| 项目 | 6 个 |
| 语言 | 14 种 |

### 4-way SPM 详情

**Layer 1 — Cluster 共享**：✅ harness/evaluation
**Layer 2 — 关键词字面级**：✅ ≥ 5 个共享关键词（evaluator loop / checkpoint / stop condition / verification / judge）
**Layer 3 — 主题直接关联**：✅ learn-harness Lecture 5 = Evaluator Loop = Article 的理论背景
**Layer 4 — 维度互补**：✅ Article = 机制深度分析 ↔ Project = 课程资源 + harness-creator skill

### 关键内容

- **第 5 讲 Evaluator Loop**：与本文 MiMo-Code Judge Model 直接对应
- **harness-creator skill**：自动生成 AGENTS.md + feature_list.md + init.sh + verify.sh
- **Anthropic 对照实验数据**：有 harness $200/6h vs 无 harness $9/20min
- **5 大 Harness 子系统**：Instructions + State + Verification + Scope + Lifecycle

### 与 MiMo-Code Article 的互补

| | MiMo-Code Article | learn-harness Project |
|--|---|---|
| 形式 | 机制深度分析 | 系统性课程 |
| 焦点 | Judge Model 为什么有效 | Harness 5 子系统如何设计 |
| 读者路径 | 理解原理 | 学会落地 |

---

## 🔮 本轮反思

- **GitHub API 扫描是发现高价值项目的有效路径**：相比爬 GitHub Trending 页面，API 搜索（按 stars + 时间过滤）更可靠
- **MiMo-Code 新特征值得单独成文**：R360 覆盖了"三时间尺度记忆框架"，R440 发现"判断模型"和"compose mode"是全新的 harness 机制维度
- **learn-harness-engineering 是 harness 领域的稀缺资源**：目前没有其他系统性课程，这个项目的 8.8K stars 反映的是真实需求
- **Tavily 持续 rate limit**：降级到 AnySearch + GitHub API 是可行的替代路径

---

## 📊 R440 数据快照

- **Articles 新增**：1（MiMo-Code Judge Model）
- **Projects 新增**：1（learn-harness-engineering）
- **Pair 路径**：Path A（双新 + 4-way SPM）
- **Cluster**：harness/evaluation
- **原文引用数量**：4 处（3 处 MiMo-Code README + 1 处 Anthropic）
- **Tool budget**：约 18 calls

---

## 🔮 下轮规划（R441）

- [ ] 评估 `cursor.com/blog/increased-agent-usage` — 唯一未被 dedup 的 cursor 候选（R439 遗留）
- [ ] 评估 `cursor.com/blog/cowork-plugins-finance` — cross-app workflows，关联 R439 multi-agent 主题
- [ ] 继续 GitHub API 扫描（stars:>=2000 + pushed:>2026-06-10）发现更新的项目
- [ ] 评估 `ponytail` 更新需求（stars 从 6K → 35K，5x 增长）
- [ ] 监控 Tavily API 额度恢复
- [ ] 探索 anthropic.com/research（论文层，与 engineering 不同的内容类型）
