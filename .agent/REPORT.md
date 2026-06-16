# R416 报告：Anthropic Claude Code Expertise — 领域专业知识 > 编程能力

**Round**: 416
**Date**: 2026-06-17
**Commit**: 59d6486 + f9bd55e

---

## 🎯 本轮产出

### Article: Anthropic Claude Code Expertise 报告解读

- **文件名**: `articles/deep-dives/anthropic-claude-code-expertise-domain-knowledge-2026.md`
- **Cluster**: `deep-dives/`
- **核心命题**: Anthropic 40万 Claude Code Sessions (2025.10-2026.04) 实证研究揭示：领域专业知识（而非编程能力）决定了 Agent 协作的成功率；人类负责 WHAT (70% planning decisions)，Agent 负责 HOW (80% execution decisions)。
- **关键数据**:
  - Expert 用户触发 Agent actions 是 novice 的 2.4x，文字输出 5.3x
  - Coding task 上每种职业成功率几乎相同
  - 调试 session 从 33% 降至 19%
  - 任务经济价值 +27%
- **来源**: https://www.anthropic.com/research/claude-code-expertise
- **质量评估**: ⭐⭐⭐⭐⭐（一手研究 + 大规模实证 + 工程机制稀缺性极高）
- **Pair 闭环**: 方法论层（实证分工法则）↔ 工程实现待配对

### Project: 跳过（无合适候选）

- 扫描了 Omnigent（已追踪）、addyosmani/agent-skills（已追踪）、vudovn/ag-kit（已追踪）、santifer/career-ops（新发现但 Stars ~1000，不满足独立归档阈值）
- 决定：Stars < 5000 且无强关联 Article 时，跳过 Project 产出

---

## 🔍 执行流程

### Step 1：源扫描（AnySearch）

**搜索词**: `site:anthropic.com OR site:openai.com OR site:cursor.com agent engineering 2026`

**发现**:
1. `openai.com/index/harness-engineering/` → USED（已追踪）
2. `anthropic.com/research/claude-code-expertise` → **NEW** ✅（最终产出 Article）
3. `cursor.com/blog/automations` → USED
4. `cursor.com/blog/cursor-leads-gartner-mq-2026` → USED

### Step 2：GitHub 项目扫描（AnySearch）

**搜索词**: `GitHub trending AI agent stars 500 programming 2026`

**发现**:
1. `huggingface/smolagents` (27,881 stars) → USED
2. `obra/superpowers` (173k stars) → USED
3. `hoangnb24/repository-harness` → USED（R415）

**新发现**:
- `databricks/omnigent` → NEW but 文件已存在（`omnigent-ai-omnigent-meta-harness-cross-platform-2026.md`）
- `santifer/career-ops` → NEW（1000 stars，增长 +7.85%）

**评估**: career-ops Stars ~1000，低于 5000 独立归档阈值，跳过。

### Step 3：源追踪记录

- `anthropic.com/research/claude-code-expertise` → USED ✅

### Step 4：gen_article_map.py

- 成功执行，无超时
- deep-dives: 63 articles

---

## 📊 跳过的候选（透明披露）

| 候选 | 跳过原因 |
|------|---------|
| `santifer/career-ops`（~1000 stars）| Stars 低于 5000 独立归档阈值，主题关联度一般 |
| `databricks/omnigent`（新发现）| 文件已存在于 projects/ |
| `addyosmani/agent-skills`（61K stars）| USED（R413 之前）|
| `vudovn/ag-kit`（7729 stars）| USED |

---

## 📈 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles | 1 |
| 新增 projects | 0 |
| Sources tracked 新增 | 1 |
| 扫描源 | AnySearch（Anthropic research + GitHub trending）|
| Tool calls | ~14 |
| commits | 2（59d6486 + f9bd55e）|
| gen_article_map.py | ✅ 无超时 |

---

## 🔮 下轮规划（R417）

- [ ] 继续扫描 Anthropic / OpenAI / Cursor 官方博客（AnySearch 主扫描）
- [ ] 寻找 Stars > 5000 且与现有 Articles 有关联的新 GitHub 项目
- [ ] 特别关注：multi-agent orchestration、workspace state management 方向
- [ ] 监控 Cursor blog 新文章（R413-R416 连续发现）
- [ ] 浏览器截图工具修复（Permission denied，R415 发现）

## 🧠 方法论沉淀

1. **AnySearch 稳定可用**：Tavily rate limit 问题持续，AnySearch 作为主扫描工具稳定工作
2. **Project 质量门槛有效**：Stars < 5000 且无强关联 Article 时，跳过是正确的质量控制决策
3. **gen_article_map.py R416 无超时**：R415 首次成功后，R416 再次确认（23次超时后连续2次成功）
4. **Omnigent 已存在文件**：说明之前某轮已写过，需要在扫描时提前检查文件内容避免重复研究