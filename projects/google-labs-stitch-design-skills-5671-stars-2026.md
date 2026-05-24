# Stitch Design Skills：Google Labs 推出的设计系统 Agent Skills 工具体系

## 核心价值

Stitch Design Skills 是 Google Labs 推出的 Agent Skills 库（5,671 Stars），为 Stitch MCP Server 提供一套结构化的设计工作流技能。这套体系完美验证了 Anthropic 提出的**工具体系渐进式披露原则**——将复杂的设计系统能力分解为可组合、可发现的技能单元。

## 关键特性

### 1. Agent Skills 开放标准

Stitch Skills 遵循 [Agent Skills](https://agentskills.io) 开放标准，兼容多种编码 Agent：

| Agent | 支持方式 |
|-------|----------|
| **Codex** | 插件市场（Plugin Marketplace） |
| **Claude Code** | `npx plugins add` |
| **Cursor** | 标准技能安装 |
| **Gemini CLI** | 原生支持 |
| **Antigravity** | 原生支持 |

### 2. 设计到代码的完整工作流

Stitch Skills 提供完整的设计系统管理技能矩阵：

| 技能 | 功能 | Prompt 示例 |
|------|------|-------------|
| `stitch::code-to-design` | 从前端代码（React/Vue）提取设计，生成 Stitch Design | *"Upload the frontend code at `/path/to/dashboard` into a Stitch project"* |
| `stitch::generate-design` | 从文本或图片生成新界面，编辑现有屏幕 | *"Make a browse tab for a mobile app for romance and date night ideas"* |
| `stitch::manage-design-system` | 上传 DESIGN.md 并应用到所有屏幕 | *"Upload our design system from `.stitch/DESIGN.md`"* |
| `stitch::extract-design-md` | 从源代码提取完整设计系统文档 | *"Scan `/src` and extract the design system into `.stitch/DESIGN.md`"* |
| `stitch::extract-static-html` | 从运行中的 Web 应用提取自包含的静态 HTML | *"Extract a static HTML snapshot of `http://localhost:3000/profile`"* |
| `stitch::upload-to-stitch` | 上传本地资源到 Stitch 项目 | *"Upload `.stitch/landing_page.html` to Stitch project"* |

### 3. 构建技能（Build Skills）

| 技能 | 功能 |
|------|------|
| `react-components` | 将 Stitch 屏幕转换为 React 组件系统 |
| `remotion` | 使用 Remotion 生成项目导览视频 |
| `shadcn-ui` | shadcn/ui 组件集成指导 |

## 技术架构

### 渐进式披露的三层实现

Stitch Skills 完美体现了 Anthropic 的工具设计原则：

```
Layer 1 - 系统提示层：
  技能名称 + 简短描述（启动时预加载）

Layer 2 - 上下文层：
  完整 SKILL.md 内容（Agent 判断相关时加载）

Layer 3 - 按需层：
  额外链接文件（Agent 探索时发现）
```

每个技能目录下包含：
- `SKILL.md` — 技能定义和核心指令
- 额外的参考文件 — 按需加载

### 跨 Agent 兼容性

```bash
# Codex
codex plugin marketplace add google-labs-code/stitch-skills --ref main

# Claude Code
npx plugins add google-labs-code/stitch-skills --scope project --target claude-code

# 通用安装
npx skills add google-labs-code/stitch-skills
```

## 与 Anthropic 文章的闭环

Anthropic《Writing effective tools for AI agents》提出的核心原则：

| 原则 | Stitch Skills 实现 |
|------|-------------------|
| **少即是多** | 精选的高价值技能，覆盖设计工作流核心场景 |
| **精确优于通用** | 每个技能精确描述输入输出（如 `code-to-design` 专注代码→设计转换） |
| **渐进式加载** | SKILL.md + 额外文件的分层架构 |
| **描述驱动** | 每个技能包含详细描述和 Prompt 示例 |

Stitch Skills 是 Anthropic 工具设计原则的最佳实践案例——它将一个复杂的设计系统工具链，分解为 Agent 可理解、可组合、可按需加载的技能单元。

## 数据

- **Stars**: 5,671
- **GitHub**: https://github.com/google-labs-code/stitch-skills
- **创建时间**: 2026-01-16
- **标准**: Agent Skills 开放标准
- **MCP Server**: Stitch MCP Server

## 来源

- [Stitch Design Skills - GitHub](https://github.com/google-labs-code/stitch-skills)
- [Stitch MCP Setup](https://stitch.withgoogle.com/docs/mcp/setup/)
- [Agent Skills Open Standard](https://agentskills.io)