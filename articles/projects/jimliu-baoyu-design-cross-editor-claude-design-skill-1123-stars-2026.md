# 跨编辑器的 Claude Design Skill

**baoyu-design** 把 Claude Design 的设计能力打包成一个可在任意本地 Agent 中运行的 Skill——Cursor、Claude Code、Codex、Claude Desktop，统统支持。

> *"You get the vast majority of claude.ai/design's capabilities without ever leaving your editor — same methodology, same craft standards, same output format."*

## 核心命题

**设计不该是网站的专利，而应该是 Coding Agent 的第一公民能力。**

长期以来，专业设计能力被困在云端交互式工具里。设计师打开网站、拖拽组件、预览效果——这套流程对 AI Agent 来说是黑盒。Agent 只能靠自然语言描述设计需求，结果充满歧义和返工。

baoyu-design 的做法是**把设计方法论打包成 Skill**：设计规范、组件脚手架、交互原型流程——全部转成 Agent 可读取的 Markdown + JSX/JS 模板。Agent 不再"想象"设计，而是执行一个经过验证的设计流程。

笔者认为，这种「设计流程即代码」的思路，是 AI Coding 进入产品级开发的关键一步。Cursor Code Enterprise 里的设计 handoff 需求、Cowork 的多角色协作场景，都需要这类能力。

## 技术细节

### 架构设计

```
用户提示词 ("Build a Reader Mac App...")
    ↓
baoyu-design Skill (Markdown + JSX scaffolds)
    ↓
Claude Code / Cursor / Codex / Claude Desktop
    ↓
自包含 HTML 输出 (designs/<project>/)
    ↓
localhost 预览 → Agent 迭代编辑
```

Skill 本身是一组 Markdown 文件，包含：
- **设计流程规范**：澄清问题 → 收集设计上下文 → 产出自包含 HTML
- **内置 Skills 库**：Hi-fi 设计、交互原型、线框图、设计系统、Figma 导入、PPTX/PDF 导出
- **Starter Components**：iOS/Android/macOS/browser 组件脚手架、幻灯片引擎、调参面板

### 跨编辑器支持

| 编辑器 | 支持状态 | 说明 |
|--------|---------|------|
| Cursor | ✅ | 截图对比效果最佳 |
| Claude Code | ✅ | 本地执行，设计产物在 repo |
| Codex | ✅ | 与 Claude Design 输出对比一致 |
| Claude Desktop | ✅ | 通用支持 |

> *"The same Reader Mac App prompt was used in Cursor, Codex, Claude, and Claude Design."* — 官方 README

### 设计输出格式

所有设计产出自包含 HTML，不依赖外部 CDN：
- `designs/<project>/index.html` — 可直接在 `localhost` 预览
- Agent 通过 Cursor Browser / DevTools / Claude Preview 做视觉指向迭代
- 产物可版本控制、可 fork、可导出

### 导出能力

官方内置导出路径：
- 独立 HTML
- PDF / PPTX（可编辑 / 截图风格）
- Figma / Canva
- **Handoff to Claude Code** — 设计完成后直接交棒给编码 Agent

## 竞品对比

| 维度 | baoyu-design | claude.ai/design 网站 | 传统 Design-to-Code |
|------|-------------|----------------------|-------------------|
| **执行位置** | 本地 Agent | 云端网站 | Figma + 插件 |
| **Agent 集成度** | 第一公民 | 不支持 Agent | 需第三方插件 |
| **输出格式** | 自包含 HTML | 网站专用格式 | Figma → 代码 |
| **版本控制** | Git 原生 | 不支持 | 需额外工具 |
| **设计流程封装** | Skill 化 | 交互式 | 模板化 |

笔者认为，baoyu-design 的核心价值不是"替代 Claude Design 网站"，而是**把设计流程变成可编程的**。当设计成为 Skill，Agent 就能在编码过程中主动调用设计能力，而不需要人工介入。

## 适用场景

- **产品原型开发**：用自然语言描述需求，Agent 产出可交互 HTML 原型
- **设计-代码 Handoff**：设计完成后直接交棒 Claude Code，无需手动标注
- **跨团队 Design System**：Skill 模板统一设计语言，确保多 Agent 输出风格一致
- **企业内设计资产沉淀**：Skill 可版本控制，企业可定制自己的设计 Skill 库

## 工程机制稀缺性

baoyu-design 代表的是 **Design-as-Skill 模式**——把原本需要人工操作的交互式流程，转化为 Agent 可独立执行的 Skill。这在当前 AI Coding 领域几乎是空白。

当前社区讨论的 Skill 主要集中在：
- 代码生成类（guard-skills、agent-skills）
- 工具集成类（MCP Server、function calling）
- **但 Design Skill 几乎无人讨论**

笔者认为，Design Skill 的缺失是因为技术难度——它需要把一个高度交互式的流程（clarify → gather context → prototype → preview → iterate）变成纯文本的 Skill 规范。baoyu-design 解决了这个问题。

## 安装使用

```bash
# 方式一：通过 skills CLI
npx skills add jimliu/baoyu-design

# 方式二：手动克隆
git clone https://github.com/JimLiu/baoyu-design.git
# 将 skills/baoyu-design 放入 Agent 的 skills 目录
```

推荐配合 **Claude Opus 4.8** 使用，效果最佳。

## 数据快照

| 指标 | 数值 |
|------|------|
| Stars | 1,123（截至 2026-06-16） |
| License | MIT |
| 创建时间 | 2026-06-07 |
| 官方定位 | Agent Skill for Claude Code / Cursor / Codex / Claude Desktop |
| 核心技术栈 | Markdown + JSX/JS（无构建依赖）|

## 笔者的判断

baoyu-design 解决了一个被长期忽视的问题：专业设计能力如何进入 AI Coding 流水线。

当前 AI Coding 工具在「写代码」上已经相当成熟，但在「做设计」上仍然依赖人工介入或第三方工具。baoyu-design 把设计能力 Skill 化，使得 Agent 可以在本地执行完整的设计流程，产物直接进入 repo——整个过程无需人工、无需云端、无需切换工具。

笔者认为，Design Skill 会成为 Agentic Coding 工具链的下一个基础设施。Cursor 的 Design Mode、Claude Code 的 Agent View、Cowork 的多角色协作——这些场景都需要设计能力作为第一公民。baoyu-design 开了个好头。

**下一步**：如果你在构建需要设计能力的 Coding Agent，或者想让现有 Agent 支持设计原型输出，可以把 baoyu-design 作为技能库的基础，研究它的 Skill 编写规范。