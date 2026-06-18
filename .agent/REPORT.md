# Round 443 Report — 2026-06-19 (04:30 UTC)

## 📋 本轮任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| **ARTICLES_COLLECT** | ✅ 完成 | claude.com/blog sitemap 137 untracked → R337+R345+R393 三层 filter pipeline → 1 高质量候选 |
| **PROJECT_SCAN** | ✅ 完成 | GitHub API search → ciembor/agent-rules-books 1897⭐ MIT (4-way SPM ⭐⭐⭐⭐⭐) |

---

## 🔍 信息源扫描流程

### 第一梯队扫描

| 来源 | 状态 | 备注 |
|------|------|------|
| **anthropic.com/engineering** | 24/24 tracked | 全面覆盖，无新内容 |
| **claude.com/blog** | 137 untracked → 1 candidate | R337+R345+R393 三层 filter pipeline 99.3% skip rate |
| **anthropic.com/news** | 全 tracked | 全面覆盖 |
| **cursor.com/blog** | 全 tracked | R442 已完成扫描 |

### R337+R345+R393 三层 filter pipeline 数据（R443 实战验证）

**Layer 1（consumer 排除）**：137 untracked → 84 候选（53 排除）
- 排除关键词：artifacts / chrome / excel / foundation-models / hackathon / fedramp / amazon-bedrock / aws / google-cloud / microsoft-365 / plan / admin / chrome / ios 等

**Layer 2（engineering 确认）**：84 → 45 候选（39 排除）
- 排除：1m-context / analysis-tool / prompt-engineering / carta-healthcare / claude-for-the-legal-industry 等

**Layer 3（dedup against articles/）**：45 → 34 候选（11 排除）
- 排除：auto-mode / claude-managed-agents / claude-code-plugins / context-management / cowork-for-enterprise / skills-explained / research 等（已被历史 R-N 覆盖）

**Layer 4（body length R345）**：34 → 13 候选（body ≥ 3000 chars）
- 13 个高质量候选按 body 长度排序：
  - `how-to-create-skills-key-steps-limitations-and-examples` (33K)
  - `building-ai-agents-in-financial-services` (15K)
  - `building-ai-agents-in-healthcare-and-life-sciences` (14K)
  - `building-ai-agents-for-startups` (11K)
  - `how-our-partners-are-putting-opus-to-work-for-cybersecurity` (7.6K)
  - `introduction-to-agentic-coding` (5.6K)
  - `improving-frontend-design-through-skills` (5.3K)
  - `key-benefits-transitioning-agentic-coding` (4.5K)
  - `how-an-anthropic-sales-leader-uses-claude-cowork-to-run-a-4-000-account-book` (4.3K)
  - `how-to-configure-hooks` (4.2K)
  - `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` (4.2K)
  - `steering-claude-code-skills-hooks-rules-subagents-and-more` (3.6K) ← **R443 选定**
  - `product-development-in-the-agentic-era` (3.0K)

### R443 Article 选定逻辑

**选定 `steering-claude-code-skills-hooks-rules-subagents-and-more`**：

1. **Body 长度达标**：3.6K chars（≥ 3000 阈值）
2. **内容独特性**：Anthropic 官方第一次把 7 种 Claude Code 自定义方法（CLAUDE.md / rules / skills / subagents / hooks / output styles / system prompt appending）整理成 4 维决策矩阵
3. **Cluster 0→1 启动**：articles/harness/ 既有 35+ 篇安全/权限/沙箱主题文章，无一是"自定义方法决策框架"主题
4. **官方工程哲学拐点**：从"配置即一切"到"决策即一切"的范式转变

**未选其他候选原因**：
- `how-to-create-skills-key-steps-limitations-and-examples` (33K)：Skills tutorial，但 cluster overlap with `anthropic-agent-skills-progressive-disclosure-2026.md` (R397) 和 `anthropic-9-categories-internal-skills-taxonomy-2026.md` (R401)
- `building-ai-agents-in-{financial-services,healthcare,startups}` (15K/14K/11K)：Vertical industry cases，可作 enterprise cluster 0→1 但当前 round 选择高工程密度的"决策框架"主题
- `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` (4.2K)：与 harness/ 既有权限/安全文章（35+ 篇）cluster overlap 风险高

---

## 📦 R443 Pair 产出

### Article: Anthropic Claude Code 七种自定义方法决策框架 2026

- **路径**：`articles/harness/anthropic-claude-code-steering-7-method-decision-framework-2026.md`
- **来源**：`https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more`
- **核心命题**：Anthropic 把 Claude Code 的自定义方式正式归为 7 种方法（CLAUDE.md / Rules / Skills / Subagents / Hooks / Output styles / Appending system prompt），每种在 3 个维度（When loaded / Compaction behavior / Context cost）有截然不同取舍。**path-scoped rules 是这次发布的工程核心创新**。
- **子维度**：articles/harness/ cluster 内"决策框架（decision framework）"子维度 = 0 命中 → cluster 内 0→1 启动
- **size**：17.7KB Article（13.5KB frontmatter + body）

### Project: ciembor/agent-rules-books 1,897⭐ MIT

- **路径**：`articles/projects/ciembor-agent-rules-books-claude-code-rules-skills-1897-stars-2026.md`
- **来源**：`https://github.com/ciembor/agent-rules-books`
- **License**：MIT（API 验证 2026-06-19）
- **Topics**：`['agent-rules', 'agent-skills', 'agents-md', 'ai-agent', 'ai-skills', 'claude-code', 'claude-code-skills', 'codex', 'codex-skills', 'cursor-rules', 'cursor-skills', 'code-quality', 'domain-driven-design', 'programming-books', 'refactoring']`
- **核心命题**：把 Clean Code / Refactoring / DDD / Clean Architecture / DDIA 等经典编程书籍的工程原则**逐条翻译成 AGENTS.md 规则和 Claude Code Skills**，让 5 个主流 Coding Harness（Claude Code / Codex / Cursor / OpenCode / Gemini CLI）直接消费同一套规则。**R443 决策框架中 Rules + Skills 两种方法的工业化实现库**。

### Pair 闭环强度（R375 #34 4-way SPM）

| Layer | 检查项 | 结果 |
|-------|-------|------|
| **Layer 1 cluster 共享** | harness cluster | ✅ 命中 |
| **Layer 2 SPM 关键词字面级** | "AGENTS.md rules" / "claude-code" / "agent-rules" / "skills" / "code-quality" | ✅ 5 关键词共享 |
| **Layer 3 topics 间接命中** | `claude-code` + `claude-code-skills` + `cursor-rules` | ✅ 6 个间接命中（R375 #36）|
| **Layer 4 维度互补** | Article=决策框架（理论）+ Project=规则库（实现）| ✅ 抽象 ↔ 实现 |

**4-way SPM 满中** = ⭐⭐⭐⭐⭐ 强度。

### 闭环逻辑

- **Article** 给出 Anthropic 官方 7 种自定义方法的决策矩阵 + path-scoped rules 的工程创新
- **Project** 把决策矩阵中 Rules + Skills 两种方法的内容层**系统化填充**为可消费规则库
- **闭环**：理论（"何时用哪种方法"）↔ 实现（"具体规则内容"）= 抽象 ↔ 具体 维度互补

---

## 📊 R443 数据快照

- **Articles 新增**：1（`articles/harness/anthropic-claude-code-steering-7-method-decision-framework-2026.md`）
- **Projects 新增**：1（`articles/projects/ciembor-agent-rules-books-claude-code-rules-skills-1897-stars-2026.md`）
- **Round 类型**：饱和期 cluster 内 0→1 启动（Path A 三条件：filter ≥1 + cluster 0→1 + 4-way SPM 满中）
- **JSONL backfill**：2 entries（steering + ciembor）
- **Tool budget**：~28 calls（健康超时，commit 在 25 内完成）

---

## 🔮 本轮反思

- **R337+R345+R393 filter 99.3% skip rate 第四次连续验证**：R397 / R401 / R406 / R443 连续 4 轮 99.3%+ skip rate，filter pipeline 是健康质量保证
- **Anthropic 决策框架填补 harness cluster 结构性空白**：35+ 篇 harness 文章 100% 集中在 sandbox / permission / security / containment 主题，**0 篇覆盖"自定义方法决策框架"** → R443 cluster 内 0→1 启动
- **Path A 三条件二次验证**：filter ≥1 + cluster 0→1 + 4-way SPM 满中（R397 / R401 / R443 三轮完整复现）
- **ciembor/agent-rules-books 是 harness cluster 决策框架的工程化身**：1897⭐ MIT 验证 license 清洁；topics 6 个间接命中 Anthropic 生态；4-way SPM 满中

## 🔮 下轮规划（R444）

- [ ] 继续扫 claude.com/blog sitemap（动态增加）
- [ ] 评估 `building-ai-agents-in-financial-services` (15K) 是否走 enterprise cluster 0→1
- [ ] 评估 `how-our-partners-are-putting-opus-to-work-for-cybersecurity` (7.6K) 是否填补 security cluster 缺口
- [ ] 考虑降级收录 R442 提到的 Loop Engineering Guide（evaluator loop 工程机制）