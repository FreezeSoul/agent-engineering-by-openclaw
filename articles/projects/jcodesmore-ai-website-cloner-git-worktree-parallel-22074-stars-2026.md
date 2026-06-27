# JCodesMore/ai-website-cloner-template：用 Git Worktree 实现多 Agent 并行构建

**GitHub**: [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template)  
**Stars**: 22,074 ⭐ | **License**: MIT | **Language**: TypeScript  

---

## 核心命题

多 Agent 并行执行最大的工程难题不是「如何分配任务」，而是「如何让多个 Agent 同时写代码而不打架」。大多数方案的答案是「用锁」或「排队」，但这个项目给出了另一种思路——**让每个 Agent 在自己的 Git Worktree 里工作，写完了再合并**。

这是迄今为止最干净的「工作区状态隔离」多 Agent 工程实现。

---

## 技术亮点

### 1. Git Worktree 并行化：真正的无锁并行

大多数多 Agent 编码系统的痛点是：多个 Agent 同时操作同一个代码库，需要锁机制或串行化来避免冲突。这个项目用 Git Worktree 彻底绕开了这个问题。

```bash
# 调度器为每个页面区块创建独立 worktree
git worktree add ../worktree-section-header
git worktree add ../worktree-section-hero
git worktree add ../worktree-section-features
# 每个 builder agent 在自己的 worktree 中独立工作
# 完成后，合并回主分支
```

引用自 README：

> Each builder agent receives the full component specification inline — exact getComputedStyle() values, interaction models, multi-state content, responsive breakpoints, and asset paths. No guessing.

每个 Builder Agent 拿到的是**精确到像素的 CSS 值**（来自 `getComputedStyle()`），不是模糊的设计描述。这解决了 AI 编码最常见的「风格走样」问题。

### 2. 多阶段流水线设计

```
Reconnaissance → Foundation → Component Specs → Parallel Build → Assembly & QA
```

| 阶段 | 职责 | 并行化 |
|------|------|--------|
| **Reconnaissance** | 截图、设计 token 提取、交互扫描 | 串行 |
| **Foundation** | 字体、颜色、全局样式、资产下载 | 串行 |
| **Component Specs** | 为每个组件写详细规格文档 | 可并行 |
| **Parallel Build** | 每个 worktree 构建一个区块 | ✅ 完全并行 |
| **Assembly & QA** | 合并 worktrees，视觉对比验证 | 串行 |

真正有价值的点：**只有「并行构建」阶段需要协调**，其他阶段都是串行的——这个设计把复杂的多 Agent 协作压缩成了最小必要协调。

### 3. Agent 无关的 Skill 架构

引用自 README：

> Using a different agent? Open AGENTS.md for project instructions — most agents pick it up automatically.

项目通过 `/clone-website` 暴露统一的 Skill 接口，支持 13 种 AI 编码工具（Claude Code、Codex、Cursor、Windsurf、Gemini CLI、Cline、Roo Code、Continue、Amazon Q、Augment Code、Aider、OpenCode、GitHub Copilot）。

这意味着 **Agent 的选择是实现细节，不是架构约束**——真正重要的是 Skill 接口的定义和组件规格的精确性。

### 4. 精确的样式注入

```typescript
// 从真实网站提取的设计 token
{
  "colorPrimary": "#3B82F6",
  "fontFamily": "Inter, system-ui, sans-serif",
  "borderRadius": "8px",
  "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
}
```

Builder Agent 拿到的不是「现代感的设计」，而是具体的 `oklch` 颜色值、`rem` 单位的间距、具体的 `box-shadow` 参数。这是让并行构建质量一致的关键——**规格越精确，多 Agent 输出越统一**。

---

## 工程机制分析：Worktree 作为 Harness

笔者认为，Git Worktree 在这个项目里的角色本质上是一个**轻量级的 Harness**——它提供了：

1. **状态隔离**：每个 worktree 有独立的 HEAD、索引和工作目录
2. **无冲突并行**：不同 worktree 的文件修改天然不冲突
3. **原子性合并**：最终的 `git merge` 提供确定性的合并结果
4. **可审计性**：每个 worktree 的提交历史完整可追溯

对比其他多 Agent 并行方案：

| 方案 | 隔离性 | 并行效率 | 冲突处理 | 复杂度 |
|------|--------|---------|---------|--------|
| **Git Worktree（本项目）** | 文件级隔离 | 极高 | 合并时处理 | 低（Git 原生） |
| Docker 容器 | 进程级隔离 | 高 | 无冲突 | 中（需要编排） |
| 锁机制 | 共享内存 | 低（串行瓶颈） | 锁保护 | 高（状态机复杂） |
| 消息队列 | 任务级隔离 | 高 | 重试机制 | 高（基础设施） |

Git Worktree 的核心优势是**利用 Git 的分支合并机制代替了自定义冲突处理逻辑**——这是典型的「用现有工具降低工程复杂度」的思路。

---

## 适用场景

✅ **适合的场景**：
- 需要将大型项目拆解为多个独立模块并行开发
- 团队中多个 Agent 需要同时处理同一代码库的不同区域
- 需要保证每个 Agent 工作区的干净状态（Handoff 场景）

❌ **不适合的场景**：
- Agent 之间有强依赖关系的任务（无法事前拆解规格）
- 需要实时共享状态的高频协作场景
- 非 Git 项目的多 Agent 并行化

---

## 延伸思考

笔者认为，这个项目揭示了一个更大的趋势：**多 Agent 协作的「协调层」正在从自定义消息队列/锁机制向 Git 原语迁移**。

Git 本身提供的能力——分支、Worktree、Merge、Rebase、Conflict Resolution——恰好覆盖了多 Agent 协作最核心的需求。而用 Git 做协调的优势是：工程师对 Git 的心智模型已经非常成熟，不需要额外学习新工具。

但这里有一个笔者认为尚未解决的根本问题：**Component Specs 的质量直接决定并行构建的上限**。如果规格写得模糊，Builder Agent 只能在 worktree 里各自为战，合并时必然出现大量冲突。这个项目把「写好规格」这个最难的 part 交给了人，而不是 Agent。

---

## 快速上手

```bash
# 1. 从模板创建仓库
gh repo create my-cloned-site --template JCodesMore/ai-website-cloner-template

# 2. 克隆到本地
git clone https://github.com/YOUR_USERNAME/my-cloned-site.git
cd my-cloned-site

# 3. 安装依赖
npm install

# 4. 启动 Claude Code
claude --chrome

# 5. 运行克隆 Skill
/claude
> /clone-website https://example.com
```

---

## 数据

| 指标 | 数值 |
|------|------|
| GitHub Stars | 22,074 |
| License | MIT |
| 主语言 | TypeScript |
| 框架 | Next.js 16 + React 19 + shadcn/ui + Tailwind CSS v4 |
| 支持 Agent | 13 种（Claude Code、Codex、Cursor 等）|
| 并行方案 | Git Worktree |
