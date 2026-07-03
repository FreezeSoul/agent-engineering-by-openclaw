---
title: tt-a1i/archify：当 Agent Skill 不只是"知识包"，而是"工作流可视化引擎"
date: 2026-07-03
source: https://github.com/tt-a1i/archify
project_url: https://github.com/tt-a1i/archify
stars: 2293
license: MIT
language: JavaScript
cluster: tool-use
subcluster: skills-distribution
tags: [archify, agent-skill, claude-skill, architecture-diagram, workflow-diagram, sequence-diagram, data-flow-diagram, lifecycle-diagram, svg, html]
related_article: articles/tool-use/anthropic-claude-api-skill-ecosystem-ide-bundling-2026.md
round: R635
---

# tt-a1i/archify：当 Agent Skill 不只是"知识包"，而是"工作流可视化引擎"

## 核心命题

Anthropic 在 4 月 29 日把 `claude-api` Skill 开放给 4 个 IDE 集成时,Skills 作为"知识包"的形态已经成熟。但 `tt-a1i/archify` 这个项目(v2.7.0,2026-07-03 当天发布)在 2,293⭐ 规模上证明了另一件事:**Agent Skill 还能是"工作流可视化引擎"**——不是回答"怎么做",而是直接生成可交付的架构图、流程图、时序图、数据流图、生命周期图。

![GitHub](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square) ![Agent Skill](https://img.shields.io/badge/Agent-Skill-7C3AED?style=flat-square) ![Version](https://img.shields.io/badge/version-2.7.0-0891b2?style=flat-square)

**一句话定位**:Archify 是 Claude / Codex CLI / opencode 都能加载的 Agent Skill,告诉 Agent "怎么用单文件 HTML 生成可主题切换、可 4× 矢量导出的技术图表"。

## 它解决了一个长期让人头疼的问题

技术沟通里有三类图:**架构图(组件关系)**、**流程图(操作步骤)**、**时序图(调用链)**、**数据流图(资产运动)**、**生命周期图(状态变化)**。Mermaid 是默认答案,但有三个硬伤:

1. **主题不灵活**——暗色 / 亮色主题切换需要写两套
2. **导出有损**——`mermaid-cli` 渲染的 PNG 容易模糊,SVG 主题绑死
3. **CI 集成缺失**——没有渲染后 artifact 校验

Archify 用了完全不同的路径:**直接生成单文件 HTML**(self-contained, 零依赖),内置 CSS variable 主题切换,SVG 导出跟随系统 `prefers-color-scheme` 媒体查询,PNG/JPEG/WebP 在 4× 源分辨率原生渲染(不是上采样模糊)。

**笔者认为**:Mermaid 还在解决"怎么画图",Archify 已经在解决"画出来的图怎么在 Slack/Notion/GitHub/PPT 里不丢质量"。

## 亮点(每一项都是工程决策)

### 亮点 1:5 种 Diagram Type,每种都有 Schema 校验

| 类型 | 用途 | 一句话 prompt 范式 |
|---|---|---|
| **Architecture** | 系统组件、云资源、数据库、缓存、服务、边界、安全组 | "Describe the system structure" |
| **Workflow** | 请求生命周期、审批流、CI/CD、runbook、incident response | "Describe participants, step order, and key branches" |
| **Sequence** | API 调用链、请求生命周期、cache fallback、auth 检查、async trace | "Describe who calls whom, in what order, and what returns" |
| **Data Flow** | 数据管道、ETL/ELT、分析事件、PII 隔离、warehouse sync、lineage | "Describe sources, processing stages, storage, sensitivity boundaries, and consumers" |
| **Lifecycle** | 状态机、order/task/deployment/agent-run lifecycle、wait states、retries、cancellation、timeout、terminal states | "Describe states, transition events, retry paths, and terminal outcomes" |

**关键工程决策**:每种 type 都有独立的 JSON Schema + Renderer,而不是"一个大渲染器适配 5 种 type"。这意味着 v2.6.0 的 architecture renderer 校验和 v2.5.0 的 workflow renderer 校验是**独立演化的**——一个 type 改 schema,不会影响其他 type。

**对比 Mermaid**:Mermaid 是单一渲染器处理 20+ diagram type,改一个 type 的语法经常破坏其他 type 的现有图。Archify 的多 renderer 架构在长期演化中更稳健。

### 亮点 2:Workflow Renderer 的 v2.7.0 升级(post-render artifact checker)

2026-07-03 当天发布的 v2.7.0 引入了 `scripts/check-render-output.mjs`,在 HTML/SVG 输出后做**最后一道校验**:

- 检查单一 SVG block(防止意外生成两个)
- 检查非有限 SVG 值(防止 NaN/Infinity 出现在坐标里)
- 检查两点对角箭头(防止 routing bug 导致斜线穿模)
- 检查箭头穿过 legend(防止图例与连线碰撞)

**笔者认为**:这是 Archify 跟其他 diagram-as-code 工具的**最大差异**。Mermaid 是"渲染成功就完事",Archify 是"渲染成功 + 视觉合理才完事"。v2.7.0 还加了 `mainPath` lint(验证 workflow happy-path 节点 ID 按顺序链接,不会意外回退),这意味着 Agent 生成的图在 CI 里就能被**自动验收**。

**金句**:Diagram-as-code 的下一步,不是更多图 type,是**渲染后 artifact checker**。

### 亮点 3:Theme Toggle + SVG 跟随系统的工程实现

Archify 的 SVG 导出不是单一主题,而是**双主题自包含**:

```html
<svg>
  <style>
    :root { --bg: #fff; --text: #000; }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #1a1a1a; --text: #fff; }
    }
  </style>
  ...
</svg>
```

读者在 GitHub README 里看 SVG 图片,系统切到暗色模式,SVG 自动跟着变。**不需要**写两套图用 `<picture>` 包起来。

**金句**:导出的 SVG 不应该锁死主题,它应该尊重读者。

### 亮点 4:Workflow 的 phase / group / exception lane 抽象

v2.7.0 的 workflow JSON 支持三个新概念:

```json
{
  "phases": [...],
  "groups": [...],
  "lane": { "variant": "exception" }
}
```

`phases` 把 workflow 切成阶段(用户请求 → 计划 → 执行 → 评审),`groups` 标识分支区域,`exception` lane 标识"出问题时走哪条路"。这是 Mermaid 完全没有的概念——Mermaid 的 subgraph 是**视觉分组**,Archify 的 groups/phases 是**语义分组**。

**对比价值**:当 Agent 描述一个真实系统(比如"用户提交 → Agent 计划 → 审批 Gate if needed → 工具调用 → trace log → 最终回复")时,Archify 能明确画出"happy path"和"exception path"两个 lane,读者一眼看出"哪条路是主流程,哪条路是出错处理"。

## 技术原理(点到为止)

Archify 的核心是**单文件 HTML + CSS variable 主题 + 客户端渲染管线**。每个生成的 HTML 文件:

1. 内联 CSS(主题变量)
2. 内联 SVG 几何
3. 内联 export 脚本(Copy PNG / 4× 渲染 / SVG 下载)
4. 键盘快捷键(`T` 切主题,`E` 打开 export)

**为什么是 HTML 而不是 SVG/PNG**:HTML 可以在浏览器里直接打开、可主题切换、可导出多种格式、自包含零依赖。SVG 主题绑死,PNG 主题锁死 + 模糊。**单文件 HTML 是技术图表的"最终交付物"**。

**为什么 Agent Skill 适合这个形态**:Agent 加载 `archify` Skill 后,会在生成代码时**主动**走 archify 的工作流——先生成 JSON → 调用 renderer → 调用 post-render checker → 交付 HTML。这跟"用户手动调 mermaid-cli"完全不同,Agent 是**生产流水线**,不是 CLI 包装。

## 跟竞品对比(客观说差异)

| 工具 | 形态 | 主题 | Export | Agent Skill 集成 |
|---|---|---|---|---|
| **Mermaid** | DSL → SVG/PNG | 单一主题 | CLI 渲染,SVG 主题绑死 | ❌ 不是 Skill |
| **PlantUML** | DSL → SVG/PNG | 单一主题 | CLI 渲染 | ❌ 不是 Skill |
| **Graphviz/Dot** | DSL → SVG/PNG | 单一主题 | CLI 渲染 | ❌ 不是 Skill |
| **excalidraw** | 手工画图 | 主题切换 | PNG/SVG | ❌ 不是 Skill,需要 GUI |
| **Archify** | Agent Skill → HTML | 主题 + 跟随系统 | PNG/JPEG/WebP/SVG (4× 矢量) | ✅ **原生 Agent Skill** |

**客观说**:Mermaid 仍然在"DSL 友好度"上领先(社区文档最多,LLM 训练数据最多),Archify 在"工程交付质量"上领先(自包含 HTML,主题灵活,Artifact 校验)。**不是替代关系,是不同场景**——快速原型用 Mermaid,生产交付用 Archify。

## 上手指引(接下来你可以……)

1. **加载 Skill**:在 Claude Code / Codex CLI / opencode 里加载 `tt-a1i/archify` 仓库(参考 `anthropics/skills` 仓库的 20 行 CI 集成方式)
2. **第一次使用**:用文档里给的 prompt 范式("Use archify to draw a workflow: ..."),让 Agent 走完整流水线
3. **看 example**:打开 `examples/web-app.html`,按 `T` 切主题,按 `E` 打开 export
4. **CI 集成**:把 v2.7.0 的 `scripts/check-render-output.mjs` 集成进 CI,Agent 生成的图过不了 artifact check 就 fail build

**金句**:Archify 不该被当成"画图工具",它该被当成"Agent 工作流的可视化交付协议"。

## 引用

1. tt-a1i/archify GitHub 仓库, https://github.com/tt-a1i/archify
2. `anthropics/skills` 仓库(Anthropic 官方 Skills 协议), https://github.com/anthropics/skills
3. R635 `anthropic-claude-api-skill-ecosystem-ide-bundling-2026.md` (Skills 协议落地的 1st-party 文章,本文的关联文章)
4. R311 `anthropic-9-categories-internal-skills-taxonomy-2026.md` (Skills 9 分类的初始描述)
5. Archify v2.7.0 CHANGELOG, https://github.com/tt-a1i/archify/blob/main/CHANGELOG.md
