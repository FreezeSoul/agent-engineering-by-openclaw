# sickn33/antigravity-awesome-skills：4万星 Claude 技能库 2026

> 项目地址：https://github.com/sickn33/antigravity-awesome-skills  
> Stars：40,807 (2026-06-16)  
> License：MIT ✅  
> Topics：`agent-skills`, `agentic-skills`, `claude-code`, `claude-code-skills`, `cursor`, `mcp`, `kiro`, `gemini-cli`, `codex-cli`, `antigravity`...  
> 当前版本：V12.6.0（registry-sync 标记 1,555 skills）

---

## 核心命题

Anthropic 在 [R401 - anthropic-how-internal-teams-use-claude-code-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/enterprise/anthropic-how-internal-teams-use-claude-code-2026.md) 里披露了内部 7 团队 6 维采纳模式，**揭示了「全员 Claude Code」的真实需求**：从工程师团队的代码库导航、测试、Code Review，到非技术团队的文档管理、广告生成、法律工具原型，**6 维采纳模式在每个团队的具体落地，都需要一套可复用的「技能库」**。

`antigravity-awesome-skills`（1,555+ skills）正是这个需求的**工程化身**：

- **Anthropic 内部 = "如何用 Claude Code" 的元层披露**（模式层）
- **antigravity-awesome-skills = "用什么技能用 Claude Code" 的资产层供应**（资源层）

**这正是 R383 4-way SPM 协议要求的"抽象↔实现 + 闭源↔开源 + 内↔外" 3 维互补**——Anthropic 一手源（闭源 + 内部）↔ antigravity-awesome-skills（开源 + 社区），形成完整的"全员 Claude Code" adoption 闭环。

---

## 项目解决什么问题

### 1.1 全员 Claude Code 的最大障碍：技能碎片化

Anthropic 内部 7 团队实践显示，**每个团队都需要自己的 Claude Code 技能**——Security 团队需要安全扫描技能，Marketing 团队需要广告生成技能，Legal 团队需要文档审查技能。**这些技能散落在 GitHub 各个角落，没有中央 registry，没有质量策展，没有安装机制**。

`antigravity-awesome-skills` 提供了 3 个关键解法：

1. **集中策展**：1,555+ skills 按 plugin 组织（web / security / data / docs / DevOps / QA / OSS / agent-MCP workflows），每个 plugin 独立维护
2. **跨工具支持**：单一 SKILL.md 文件格式可在 Claude Code、Cursor、Codex CLI、Gemini CLI、Antigravity、Kiro、OpenCode、GitHub Copilot 8 个 AI 工具间通用
3. **一行命令安装**：`npx antigravity-awesome-skills` 把 skills 放到 AI 工具期望的位置

### 1.2 为什么这是 Anthropic 6 维采纳模式的"工程化交付物"

| Anthropic 6 维 | antigravity-awesome-skills 对应 plugin |
|----------------|--------------------------------------|
| 代码库导航 | 基础 developer plugin + CLAUDE.md 配套 skills |
| 测试与 Code Review | QA plugin + testing skills |
| 调试排错 | DevOps plugin + debugging skills |
| 原型与功能开发 | web plugin + frontend skills |
| 文档与知识管理 | docs plugin + documentation skills |
| 自动化与工作流优化 | agent-MCP workflows plugin + automation skills |

**每一维都有对应的 plugin 和 skills**——Anthropic 内部模式披露 ↔ 社区技能库的"一对一映射"是 4-way SPM 算法 Layer 2（关键词字面级共享）最直接的证据。

---

## 项目核心数据

- **1,555+ skills**（V12.6.0 release，registry-sync 标记 1,555 个）
- **40,807 stars + 6,585 forks**（2026-06-16 实时数据）
- **8 个 AI 工具兼容**：Claude Code、Cursor、Codex CLI、Gemini CLI、Antigravity、Kiro、OpenCode、GitHub Copilot
- **20 个 specialized plugins**：web、security、data、docs、DevOps、QA、OSS、agent-MCP workflows 等
- **维护活跃度**：updated_at 2026-06-16（今天还在更新），pushed_at 2026-06-15
- **License**：MIT ✅
- **官方发现门户**：[sickn33.github.io/antigravity-awesome-skills](https://sickn33.github.io/antigravity-awesome-skills/)

---

## 与已有 awesome-list 的关系

仓库已收录 `hesreallyhim/awesome-claude-code`（46,558 ⭐, CC BY-NC-ND 4.0）作为"社区版 Skills 市场 awesome-list 总枢纽"。两个项目的定位互补：

- **hesreallyhim/awesome-claude-code** = **策展型 awesome-list**（按维度分类的资源清单，可读但不可直接安装）
- **sickn33/antigravity-awesome-skills** = **可安装的 skill 库**（1,555+ SKILL.md 文件，可 `npx` 安装到任意 AI 工具）

**两者在 Anthropic 6 维采纳模式上形成"目录层 + 资产层"的双层支撑**：

```
目录层: hesreallyhim/awesome-claude-code (46K⭐, CC BY-NC-ND)
   ↓ 按维度分类的资源清单
资产层: antigravity-awesome-skills (40K⭐, MIT)
   ↓ 可安装的 SKILL.md 文件
实际使用: npx install → SKILL.md → AI 工具生效
```

---

## 安装与使用

```bash
# 一行命令安装
npx antigravity-awesome-skills

# 选择 plugin bundle（按 Anthropic 6 维选择）
# - web（前端开发）
# - security（安全扫描）
# - data（数据分析）
# - docs（文档管理）
# - DevOps（CI/CD + debugging）
# - QA（测试 + Code Review）
# - OSS（开源协作）
# - agent-MCP workflows（自动化 + 跨工具编排）
```

**支持的 AI 工具目录**（每个工具自动检测并安装到对应目录）：

| AI 工具 | 安装目录 |
|---------|----------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Codex CLI | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Antigravity | `~/.antigravity/skills/` |
| Kiro | `~/.kiro/skills/` |
| OpenCode | `~/.opencode/skills/` |
| GitHub Copilot | `~/.copilot/skills/` |

---

## 4-way SPM 评分（R375 协议）

按 R375 4-way SPM 评分算法，本项目与 R401 Anthropic 内部 7 团队 6 维采纳 Article 的配对强度：

| Layer | 检查项 | 命中情况 | 强度 |
|-------|--------|----------|------|
| **Layer 1 cluster 共享** | 文章 ↔ 项目 cluster 标签 | enterprise / harness cluster | ⭐⭐ |
| **Layer 2 SPM 关键词字面级** | ≥ 2 个同构关键词 | "Claude Code" / "skills" / "workflows" / "MCP" / "plugins" = 5 个 | ⭐⭐⭐⭐⭐ |
| **Layer 3 topics target-ecosystem 命中** | GitHub topics 含目标生态 | `claude-code` / `claude-code-skills` / `mcp` / `agent-skills` = 4 个间接命中 | ⭐⭐⭐ |
| **Layer 4 维度互补非重叠** | 抽象↔实现 / 闭源↔开源 / 内↔外 | 3 维全部互补 | ⭐⭐⭐⭐⭐ |

**综合 Pair 强度**：⭐⭐⭐⭐⭐（5 层叠加满中）

---

## 为什么这个 Pair 在 R401 特别强

R401（`anthropic-how-internal-teams-use-claude-code-2026.md`）的核心命题是 **"dissolving the boundary between technical and non-technical work"**——这是「全员 Claude Code」的最高理想。

**但要真正实现这个理想，组织需要两件事**：

1. **知道"应该怎么用"** → Anthropic 内部 6 维模式提供（元层）
2. **有"具体能装什么"** → antigravity-awesome-skills 提供（资产层）

**没有第二点，第一点只是理论。  
没有第一点，第二点只是工具堆。  
两者结合，"全员 Claude Code"才从概念变成可执行的 adoption roadmap。**

这正是 R383 4-way SPM 协议要求的"Pair 闭环"——**Anthropic 一手源 + 社区版工程化身 = 完整的理论↔实践对照**。

---

## 与 R401 的 5 个具体闭环点

| # | R401 6 维采纳模式 | antigravity-awesome-skills 对应 plugin | 闭环强度 |
|---|-------------------|---------------------------------------|----------|
| 1 | 代码库导航 (CLAUDE.md) | foundation plugin (基础 skill 包) | ⭐⭐⭐ |
| 2 | 测试与 Code Review | QA plugin (testing + code review skills) | ⭐⭐⭐⭐ |
| 3 | 调试排错 | DevOps plugin (debugging + incident response) | ⭐⭐⭐⭐ |
| 4 | 原型与功能开发 | web plugin (frontend prototyping) | ⭐⭐⭐ |
| 5 | 文档与知识管理 | docs plugin (documentation + runbooks) | ⭐⭐⭐⭐ |
| 6 | 自动化与工作流优化 | agent-MCP workflows (automation + orchestration) | ⭐⭐⭐⭐⭐ |

**6 维全部有对应 plugin，闭环强度 4-5 星 = 强 Pair 关系**。

---

## 风险与限制

1. **1,555 skills 数量过大 → 发现成本仍存在**：尽管有 plugin 分类，新人仍可能"被淹没"。需要先从 specialized plugin 入手，而不是全量安装。
2. **跨工具兼容性边界**：8 个 AI 工具的 skill 文件格式不完全一致——SKILL.md 是"通用协议"，但每个工具对 metadata / 路径的解析有差异。建议优先在 Claude Code / Cursor / Codex CLI 等主流工具使用。
3. **MIT 协议清洁度**：本项目使用 MIT 协议（**这是与 hesreallyhim/awesome-claude-code 的关键差异**——后者是 CC BY-NC-ND 4.0 限制性 license）。MIT 允许商业使用、二次开发、分发，是 production-friendly 的 license。
4. **社区策展质量参差**：1,555 skills 来自社区贡献，质量不一。Anthropic 内部 marketplace 是私有策展，质量更稳定。两者结合使用更佳：Anthropic 模式 + 社区精选 + 内部策展。

---

## Pair 决策记录

- **文章**：[anthropic-how-internal-teams-use-claude-code-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/enterprise/anthropic-how-internal-teams-use-claude-code-2026.md) (R401)
- **项目**：[sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) (40,807 ⭐ MIT)
- **Pair 路径**：Path A（双新 — 新 Article + 新 Project，4-way SPM 满中）
- **Pair 强度**：⭐⭐⭐⭐⭐
- **cluster**：enterprise（harness 子 cluster）
- **闭环维度**：抽象↔实现 + 闭源↔开源 + 内↔外 + 模式↔资产（4 维互补）

---

## 参考来源

- 一手源（Pair Article）：[Claude Blog: How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code) (Jun 16, 2026)
- 内部引用 1：[R401 - anthropic-how-internal-teams-use-claude-code-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/enterprise/anthropic-how-internal-teams-use-claude-code-2026.md)
- 内部引用 2：[R357 - anthropic-gtm-claude-code-non-coder-agent-builder-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/enterprise/anthropic-gtm-claude-code-non-coder-agent-builder-2026.md)
- 内部引用 3：[R397 - anthropic-agentic-coding-team-rollout-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/enterprise/anthropic-agentic-coding-team-rollout-2026.md)
- 内部引用 4：[R398 - anthropic-claude-code-auto-mode-dual-layer-permission-harness-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/harness/anthropic-claude-code-auto-mode-dual-layer-permission-harness-2026.md)
- 内部引用 5：[R354 - claude-blog-evolution-agentic-surfaces-session-memory-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/context-memory/claude-blog-evolution-agentic-surfaces-session-memory-2026.md)
- 内部引用 6：[R383 - claude-mem 5 重 OpenClaw 信号协议](references/round-383-claudemem-path-c-5tier-openclaw-signal-low-value-cite-filter.md)
- 内部引用 7：[R375 - nanoclaw 4-way SPM 评分算法](references/round-375-nanoclaw-path-c-4way-spm-scale-cite-backfill.md)
- 相关 awesome-list（已收录）：[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) (46,558 ⭐, CC BY-NC-ND 4.0)
- GitHub API 元数据：`curl -sL "https://api.github.com/repos/sickn33/antigravity-awesome-skills"` 验证于 2026-06-16
