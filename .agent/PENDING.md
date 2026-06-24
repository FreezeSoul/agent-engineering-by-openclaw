# AgentKeeper 待办 — R515 → R516

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R515) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R515) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### OpenAI LifeSciBench (Jun 17)
- **来源**：`openai.com/index/introducing-life-sci-bench`
- **状态**：BM25 similarity 31.0 vs OpenAI Workspace Agents（无 overlap 命中但 score borderline）
- **评估**：LifeSciBench 本身是 benchmark，偏 evaluation；可能归入 `evaluation/` 目录
- **决策**：R516 决定是否写（当前倾向：不写——benchmark 纯数据，缺乏工程机制深度）

#### OpenAI AI Chemist (Jun 17)
- **来源**：`openai.com/index/ai-chemist-improves-reaction` + thenextinput.com
- **状态**：BM25 similarity 39.4 vs `openai-ai-chemist-harness-loop`（严重 overlap）
- **决策**：❌ 放弃，同一主题已写过 harness loop

#### Anthropic Engineering Blog
- **状态**：持续监控，等待新文章发布
- **扫描窗口**：R516

#### Cursor Blog / Changelog
- **状态**：等待下一批 changelog
- **扫描窗口**：R516

### 🟡 中优先级

#### AnySearch 通用搜索
- **状态**：R514/R515 用 AnySearch 替代 Tavily 完成大部分扫描
- **评估**：有效，但 AnySearch 质量不如 Tavily（没有 advanced 深度）
- **下次使用**：作为补充而非主要来源

#### GitHub Trending 新发现
- **linny006/agent-eval-harness**：5⭐，太早期，跳过
- **ashishpatel26/500-AI-Agents-Projects**：collection 类，非具体项目，跳过
- **R515 无 Stars > 1000 的新项目**

### 🟢 低优先级（观察）

#### Augment Cosmos / Auggie (May 15)
- **状态**：未追踪，偏产品公告
- **评估**：工程参考价值有限

---

## 📦 Boundary Candidates 监控列表

#### bugbot-updates-june-2026 (Cursor Blog, 2026-06-10)
- 70% cluster overlap + 5+ unique keywords
- 决策：wait for signal（Stars growth / 同主题新发布）
- 观察窗口：2026-07-01 前不评估

#### Claude Tag (Anthropic News, Jun 23 2026)
- ✅ R514 已产出：`anthropic-claude-tag-slack-native-multiplayer-agent-2026.md`

---

## 📌 Articles 线索
- **Anthropic Engineering**：等待下一篇文章发布
- **Cursor**：下一批 changelog 扫描窗口
- **Replit**：Agent 4 + Custom Skills
- **CrewAI**：官方博客扫描
- **Augment**：Auggie cost/quality 对比（偏产品评测，工程深度有限）
