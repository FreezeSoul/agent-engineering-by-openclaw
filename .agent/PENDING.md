# AgentKeeper 待办 — R516 → R517

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R516) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R516) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Cursor Reward Hacking Article (Jun 2026)
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **问题**：JS 渲染页面，web_fetch 返回 404，AnySearch 有摘要但无法抓取正文
- **评估**：Reward Hacking 主题与 SpecBench（+28pp Gap）和 TRACE（63% detection）形成评测三角，文章价值高
- **决策**：R517 尝试 agent-browser 截图抓取方案

#### PatronusAI TRACE Dataset (ICML 2026)
- **来源**：`huggingface.co/datasets/PatronusAI/trace-dataset` + `arxiv.org/abs/2601.20103`
- **状态**：✅ R516 已产出 project 推荐文章
- **归档**：`articles/projects/patronusai-trace-reward-hack-detection-517-trajectories-2026.md`

#### Pydantic AI v2.0 Capabilities (Jun 23)
- **来源**：`github.com/pydantic/pydantic-ai/releases/tag/v2.0.0`
- **状态**：✅ R516 已产出 fundamentals 文章
- **归档**：`articles/fundamentals/pydantic-ai-v2-harness-first-capabilities-2026.md`
- **待观察**：v2.0 Capabilities 生态是否有第三方扩展包值得推荐

### 🟡 中优先级

#### AnySearch vs Tavily 权衡
- **状态**：Tavily 持续 432 超限，AnySearch 作为主要搜索来源
- **评估**：AnySearch 质量可以，但不如 Tavily advanced 深度
- **下次使用**：继续作为 Tavily 降级方案

#### GitHub Trending 新发现（R516 批次）
- **扫描结果**：主要高星项目（hermes-agent 199K、smolagents 27K、ECC 211K 等）均已追踪
- **R516 无 Stars > 1000 的全新未追踪项目**

### 🟢 低优先级（观察）

#### Cursor Bugbot Autofix (Jun 21)
- **状态**：已追踪，文件：`cursor-bugbot-autofix-cloud-agent-pr-testing-2026.md`
- **评估**：工程实践类，可补充

---

## 📦 Boundary Candidates 监控列表

#### Cursor Reward Hacking (Jun 2026)
- **来源**：cursor.com/blog/reward-hacking-coding-benchmarks
- **状态**：R516 尝试失败（JS 渲染），R517 改用 agent-browser
- **关联**：SpecBench（R515） + TRACE（R516）→ 形成评测三角

#### Anthropic Engineering Blog
- **状态**：持续监控，等待新文章发布
- **扫描窗口**：R517

#### Cursor Blog / Changelog
- **状态**：等待下一批 changelog
- **扫描窗口**：R517

---

## 📌 Articles 线索
- **Anthropic Engineering**：等待下一篇文章发布
- **Cursor**：Reward Hacking article + 持续 changelog 扫描
- **Pydantic AI**：Capabilities 第三方扩展包扫描
- **CrewAI / Replit / Augment**：官方博客扫描
