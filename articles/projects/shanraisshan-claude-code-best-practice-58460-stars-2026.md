# shanraisshan/claude-code-best-practice 58K⭐ — 工程化身

> **官方仓库**：[shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
> **License**：MIT（验证于 2026-06-22 via GitHub API）
> **Topics**：`agentic-ai` / `agentic-coding` / `agentic-engineering` / `agentic-workflow` / `anthropic` / `best-practices` / `claude-code` / `claude-code-best-practices` / `claude-code-commands` / `claude-code-skills` / `context-engineering` / `vibe-coding`
> **创建时间**：2025-10-31
> **关联 Article**：[claude-blog-using-claude-md-files-best-practices-2026.md](../fundamentals/claude-blog-using-claude-md-files-best-practices-2026.md)
> **闭环强度**：⭐⭐⭐⭐⭐（4-way SPM 满中：cluster 共享 + 关键词字面级 + 维度互补 + 范式同构）

---

## 项目定位

`shanraisshan/claude-code-best-practice` 是 Claude Code "从 vibe coding 到 agentic engineering" 跃迁过程中**最完整的中文+英文双语工程实践集合**——58,460 Stars（截至 2026-06-22，GitHub API 验证）使其成为 Anthropic 官方博客 [Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files) 在开源社区的**事实标准参考实现**。

仓库核心定位词：

> "from vibe coding to agentic engineering - practice makes claude perfect"

这与 Anthropic 官方在 CLAUDE.md 文档中强调的"配置即代码"理念形成**字面级 SPM**：

| Anthropic 官方表述 | shanraisshan 仓库自定位 |
|------------------|---------------------|
| "CLAUDE.md 是给 AI 队友的上岗培训文档" | "Agentic engineering — practice makes Claude perfect" |
| "Treat customization as an ongoing practice" | "from vibe coding to agentic engineering" |
| "context engineering and prompt engineering" | topics: `context-engineering` |
| "Boris Cherny 的 CLAUDE.md 只有 2,500 token" | 仓库内提供精简的 CLAUDE.md 模板（避免 200+ 行反模式）|

---

## 仓库结构亮点

仓库的核心价值在于**结构化的工程方法论清单**，覆盖 Claude Code 完整生命周期：

### 1. CLAUDE.md 模板与反模式

仓库提供多种规模的 CLAUDE.md 模板（从 50 token 极简版到 2,500 token Boris Cherny 同款版），并明确标注**反模式警告**：

- ❌ 不要写"通用提示"（如"be helpful"）
- ❌ 不要超过 200 行（Claude 会忽略规则）
- ❌ 不要包含敏感信息（API keys、credentials）
- ✅ 用 `#` 键持续迭代摩擦点

这与 Anthropic 官方博客的 5 大反模式完全对应。

### 2. Commands 与 Hooks 工程化

仓库提供 `.claude/commands/` 目录下的实战命令集合（与 Anthropic 官方博客的 "custom slash commands" 章节对应）：

- `/performance-optimization` — 性能审查
- `/security-review` — 安全扫描
- `/test-coverage` — 测试覆盖分析
- `/api-design-check` — API 设计审查

每个命令都是 markdown 文件 + frontmatter，**符合 Anthropic 官方推荐的格式**。

### 3. Skills 集成模式

仓库内含 `/skill-creator` 调用样例、Skill 渐进式披露的最佳实践、跨项目 Skill 共享的 `.claude/skills/` 目录约定——这与 [anthropic-agent-skills-progressive-disclosure-2026.md](../fundamentals/anthropic-agent-skills-progressive-disclosure-2026.md) 中描述的 Skills 架构深度互补。

### 4. Subagent 工作流编排

仓库提供完整的 subagent 调用示例：

```
Use a subagent to:
- Review code for OWASP Top 10 security issues
- Analyze performance bottlenecks with isolated context
- Generate API documentation with fresh eyes
```

这是对 [claude-blog-using-claude-md-files-best-practices-2026.md](../fundamentals/claude-blog-using-claude-md-files-best-practices-2026.md) 中"子 Agent 上下文隔离"机制的工程化封装。

### 5. 双语 + 实战案例

仓库**中英双语**对照，覆盖：

- 中文开发者最常见的 6 大场景（企业级、私有化部署、单兵作战、团队协作、开源贡献、个人项目）
- 英文社区的工程实践（与 Anthropic 官方博客同步）

这一特性使其在中文工程社区具备独特价值——填补了 Anthropic 英文文档与中文 Claude Code 用户之间的工程实践 gap。

---

## 4-way SPM 评估（与关联 Article 配对强度）

| Layer | 评估维度 | 命中情况 | 得分 |
|-------|---------|---------|------|
| **L1 cluster 共享** | 与 Article 同 cluster（fundamentals）| ✅ `articles/fundamentals/` | ⭐⭐ |
| **L2 SPM 关键词字面级** | 共享核心命题词 | ✅ 命中 6+：`CLAUDE.md` / `best-practices` / `context-engineering` / `subagents` / `skills` / `vibe-coding` / `agentic-engineering` | ⭐⭐⭐⭐⭐ |
| **L3 topics target-ecosystem** | 仓库 topics 含目标生态标识 | ✅ `claude-code` / `claude-code-best-practices` / `claude-code-commands` / `claude-code-skills` / `agentic-engineering` | ⭐⭐⭐⭐ |
| **L4 维度互补** | Article 抽象规范 ↔ Project 实践参考 | ✅ **抽象 ↔ 实现**（官方工程规范 ↔ 社区开源参考实现）；**闭源 ↔ 开源**（Anthropic 一手源 ↔ MIT 公开仓库） | ⭐⭐⭐⭐⭐ |

**综合**：⭐⭐⭐⭐⭐（4 层全中，R375 #34 协议稳定产出）

---

## 核心闭环逻辑

| 层 | 来源 | 角色 |
|----|------|------|
| **L1 哲学层** | Boris Cherny 5 层加载作用域 + WHAT/WHY/HOW 框架 | 理论框架 |
| **L2 规范层** | Anthropic [using-claude-md-files](https://claude.com/blog/using-claude-md-files) | 工程规范 |
| **L3 实践层** | **shanraisshan/claude-code-best-practice（本仓库）** | **开源社区工程化身** |
| **L4 反模式层** | ETH Zurich 论文 + 社区报告 | 配置蔓延失败模式 |

L2 → L3 形成"理论规范 → 实践参考"的强闭环：Anthropic 给出"应该怎么做"的官方规范，shanraisshan 仓库提供"如何在真实项目中落地"的开源实现——这是 [R375 Path C 协议](references/round-375-nanoclaw-path-c-4way-spm-scale-cite-backfill.md) 验证的典型 SPM 字面级配对。

---

## License 验证

```bash
$ curl -s https://api.github.com/repos/shanraisshan/claude-code-best-practice \
    | grep -E '"spdx_id"'
  "spdx_id": "MIT"
```

✅ **MIT License** — Production-friendly，与仓库描述一致。

---

## 引用方式

在仓库的 README、CONTRIBUTING 或 .github/ 目录中显式引用本文档，建立"理论 ↔ 实践"双向锚点：

```markdown
## CLAUDE.md Best Practices Reference
- [Anthropic Official Guide](https://claude.com/blog/using-claude-md-files)
- [Engineering Practice Collection (Chinese + English)](https://github.com/shanraisshan/claude-code-best-practice)
```

---

## 总结

`shanraisshan/claude-code-best-practice` 的 58,460 Stars 不是偶然——它填补了 **Anthropic 官方规范与社区工程实践之间的 6 个月 gap**。从 vibe coding（凭感觉写 prompt）到 agentic engineering（系统化工程方法论）的跃迁中，这个仓库就是中文 + 英文工程社区的**事实标准答案**。

它不是替代 Anthropic 官方文档，而是**让官方文档在真实项目里落地的桥梁**。