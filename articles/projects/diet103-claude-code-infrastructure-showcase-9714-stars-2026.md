# diet103/infrastructure-showcase：6 个月生产 Hooks 参考

> 关键词：Claude Code Hooks、Auto-activating Skills、Reference Library、Hook Configuration、Production-tested、Skill Activation、Claude Code Infrastructure
>
> 仓库：[diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)（9714⭐ MIT，2026-06 验证于 GitHub API）
>
> 配对文章：[Claude Code Hooks：8 大事件全生命周期与可编程 Harness](../harness/claude-code-hooks-8-event-lifecycle-programmable-harness-2026.md)

---

## 仓库定位

diet103/claude-code-infrastructure-showcase 是 **Claude Code 生态目前最完整的 hooks + skills + agents 生产参考库**——基于一个复杂 TypeScript 微服务项目 6 个月的实际使用经验，沉淀出可直接复用的「Claude Code 基础设施」配置模板。

README 原话：

> Born from 6 months of real-world use managing a complex TypeScript microservices project, this showcase provides the patterns and systems that solved the "skills don't activate automatically" problem and scaled Claude Code for enterprise development.
>
> **This is NOT a working application** - it's a reference library. Copy what you need into your own projects.

**核心特征**：

- ⭐ **9,714 Stars**（2026-06-20 验证），MIT license
- 📅 **6 个月迭代**：单一作者在生产 TypeScript 微服务项目上沉淀
- 🔧 **生产验证**：所有模式都来自真实项目，非实验性
- 📋 **可拼装**：reference library 模式，每个 `.claude/` 目录可独立复制

---

## 为什么值得推荐：4-way SPM 满中

按 R375 #34 协议 4 层叠加判定：

### Layer 1：cluster 共享

仓库主题（hooks + skills + agents + Claude Code 基础设施）落在 `articles/harness/` cluster —— 与本仓库 169 篇 harness 文章主轴完美对齐。

### Layer 2：SPM 关键词字面级共享

配对文章 `claude-code-hooks-8-event-lifecycle-programmable-harness-2026.md` 核心关键词：

- `hooks` ✓（仓库核心机制）
- `skills` ✓（Auto-activating skills 是核心模式）
- `agent` ✓（specialized agents）
- `Claude Code` ✓（仓库定位）
- `infrastructure` ✓（仓库名直接命中）

5/5 字面级共享，**R375 #34 Layer 2 升级为 ⭐⭐⭐⭐⭐**。

### Layer 3：topics / 维度互补

仓库 topics 字段为空，但 README 描述中明确：

> Production-tested infrastructure for: Auto-activating skills via hooks, Modular skill pattern (500-line rule), Specialized agents for complex tasks, Dev docs system that survives context resets

这些定位词与配对文章**形成完整维度互补**：

| 维度 | Article 角色 | Project 角色 |
|------|-------------|-------------|
| 视角 | 官方架构理论 | 社区生产实践 |
| 抽象层级 | 协议规范（8 事件 + JSON 配置）| 工程实现（.claude/hooks/ 完整目录）|
| 适用范围 | 任何 Claude Code 用户 | 复杂 TypeScript 微服务项目 |
| 时间维度 | 当下能力 | 6 个月迭代历史 |

**Layer 4 维度互补：抽象↔实现 + 通用↔特定 = 完整闭环**。

### 综合判定

4-way SPM **五星满中**（R375 #34 + R401 #48 算法第六次实战），建议作为 hooks cluster 的**配套项目**——理论 ↔ 实践完整 stack。

---

## 核心机制：Auto-Activating Skills

本仓库的「招牌特性」是用 hooks 实现 **skill 自动激活**——解决 Anthropic 官方 skills 系统的核心痛点：「skills 默认是被动加载，需要用户在 prompt 中显式提及」。

**实现路径**（README 描述）：

```bash
# ~/.claude/hooks/skill-activation.sh
# UserPromptSubmit hook: 扫描 prompt，匹配到 skill 关键词时自动激活

PROMPT="$1"  # 从 stdin 读入
SKILLS_DIR=".claude/skills/"

for skill_file in $SKILLS_DIR/*.md; do
  skill_name=$(basename "$skill_file" .md)
  if echo "$PROMPT" | grep -qi "$skill_name"; then
    echo "Auto-activating skill: $skill_name"
    cat "$skill_file"
  fi
done
```

这一实现把 Anthropic 官方的「被动 skills 加载」升级为「**基于 prompt 上下文的自动 skills 注入**」——是 hooks 实战中最具杠杆的范式。

---

## 与 Claude Code Hooks 文章的 5 个核心命题对位

| 文章命题 | 仓库实现 |
|---------|---------|
| 8 个 hook 事件全生命周期 | 仓库 `.claude/hooks/` 目录包含 PreToolUse / PostToolUse / UserPromptSubmit / SessionStart 等多个 hook 脚本 |
| 消除重复手工操作 | 自动化 Prettier / ESLint 在写文件后触发 |
| 自动强制项目规则 | TypeScript 项目的 lint 强制 + 文件路径白名单 |
| 动态上下文注入 | SessionStart 加载 git status / sprint 优先级 / TODO 列表 |
| PreCompact 备份决策 | Dev docs 系统在压缩前 dump 关键决策到 `.claude/decisions.md` |

**5/5 命题对位命中**——文章的理论框架在仓库中找到完整工程实现。

---

## 仓库包含的 4 大生产模式

### 模式 1：Auto-activating skills via hooks

**痛点**：skills 默认是被动加载。**方案**：`UserPromptSubmit` hook 扫描 prompt，关键词命中时自动 `cat` skill 文件注入上下文。

### 模式 2：Modular skill pattern（500 行规则）

**痛点**：skill 文件太长会撑爆 context window。**方案**：每个 skill 文件 ≤ 500 行，配合 progressive disclosure（按需展开子模块）。

### 模式 3：Specialized agents

**痛点**：复杂任务单 Agent 难以胜任。**方案**：在 `.claude/agents/` 定义 specialized agents（如 `backend-dev-guidelines` / `frontend-dev-guidelines` / `route-tester`），按任务类型委派。

### 模式 4：Dev docs 持久化系统

**痛点**：context compaction 会丢失「为什么这么设计」的关键决策。**方案**：`PreCompact` hook 把决策 dump 到 `.claude/decisions.md`——保证 compaction 后决策不丢失。

---

## 安装与集成路径

根据 README，集成路径分两条：

### 路径 A：AI 辅助集成（推荐）

直接在 Claude Code 中：

> "Read CLAUDE_INTEGRATION_GUIDE.md and walk me through integration step by step."

Claude Code 会自动读 README 中的集成指南，按步骤复制 `.claude/hooks/` + `.claude/skills/` 到你的项目。

### 路径 B：手动复制

```bash
git clone https://github.com/diet103/claude-code-infrastructure-showcase
cd your-project
cp -r ../claude-code-infrastructure-showcase/.claude/ .
# 然后挑选需要的 hook / skill / agent 配置
```

**集成时间**：15-30 分钟（README 声明，与实际复杂度吻合）。

---

## 适用场景判断

### ✅ 适合

- TypeScript / Node.js 微服务项目
- 已有 Prettier / ESLint / Jest 配置的项目
- 团队 3+ 人，希望统一 Claude Code 行为
- 想用 hooks 但不知道从哪开始的新手

### ❌ 不适合

- 简单的脚本项目（hooks 投资回报低）
- 不想修改 `.claude/settings.json` 的极简主义者
- 与 hooks 完全无关的工作流（如纯文档写作）

---

## License 与可商用性

- **License**：MIT（GitHub API `spdx_id: MIT`，2026-06-20 验证）
- **可商用**：✓ 完全 MIT，可直接复制配置到商业项目
- **专利风险**：无（MIT 不含专利条款，但贡献者的贡献默认包含专利授权）
- **商标风险**：无（仓库未含 Anthropic / Claude 商标，仅以「Claude Code」作为系统名引用）

---

## 与 hooks cluster 其他项目的对比

| 仓库 | Stars | 定位 | 与本仓库差异 |
|------|-------|------|------------|
| **diet103/claude-code-infrastructure-showcase** | 9,714 | 生产级 hooks + skills + agents 完整 stack | **本仓库 = 生产集成参考** |
| disler/claude-code-hooks-mastery | 3,779 | hooks 教程式教学 | 本仓库 hooks 是教学案例，本仓库是生产实现 |
| davepoon/buildwithclaude | 3,087 | Claude 构建资源集合 | 通用资源集合，本仓库专注 hooks + skills |
| hesreallyhim/awesome-claude-code | 46,879 | awesome 列表 | 索引型，本仓库是单个深度 stack |

**结论**：hooks cluster 已有 disler（教程）+ 本仓库（生产）双覆盖，awesome-claude-code（索引）作为兜底。

---

## 引用源

- 仓库：[diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)（9714⭐ MIT）
- 配对文章：[Claude Code Hooks：8 大事件全生命周期与可编程 Harness](../harness/claude-code-hooks-8-event-lifecycle-programmable-harness-2026.md)
- 一手源：[Claude Blog — How to configure hooks](https://claude.com/blog/how-to-configure-hooks)（Anthropic 官方）
- 同主题：[disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)（3779⭐ 教程式）
- License 验证：GitHub API `spdx_id: MIT`，2026-06-20
