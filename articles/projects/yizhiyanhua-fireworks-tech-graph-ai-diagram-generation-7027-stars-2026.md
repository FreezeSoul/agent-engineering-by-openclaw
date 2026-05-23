# fireworks-tech-graph：让 Claude Code 用自然语言生成 publication-ready 技术图

**核心命题**：技术图是文档的命根子，但手绘太慢、模板太丑、Mermaid 语法太难。fireworks-tech-graph 把这个问题反过来解决——你用自然语言描述，AI 生成专业级的 SVG/PNG 图，7 种风格，支持 UML 和 AI/Agent 领域专属模式（Mem0、RAG、Multi-Agent、Tool Call）。

**Stars**：7,027（截至 2026-05-23）
**GitHub**：https://github.com/yizhiyanhua-ai/fireworks-tech-graph
**定位**：Claude Code Skill / AI Coding 工具

---

## 一、解决了什么问题

写技术文档最痛苦的不是文字，是图。
- Mermaid 语法学成本身不低，写出来的图还丑
- PlantUML 功能强但配置复杂
- draw.io 画出来的图缺乏设计感，不适合 publication

fireworks-tech-graph 的思路是：**把生成过程交给 AI，人只需要描述想要什么**。

> "Stop drawing diagrams by hand. Describe your system in English or Chinese — get publication-ready SVG + PNG technical diagrams in seconds."

---

## 二、七种风格：覆盖从白图到品牌官方图

| 风格 | 视觉特点 | 适合场景 |
|------|---------|---------|
| **Style 1 — Flat Icon** | 白底、语义箭头、分层布局 | Mem0、架构图、产品文档 |
| **Style 2 — Dark Terminal** | 黑底、霓虹色、单体字 | Tool Call Flow、技术博客 |
| **Style 3 — Blueprint** | 深蓝底、网格线、青色描边 | 微服务架构、工程示意图 |
| **Style 4 — Notion Clean** | 极简白、单色强调 | Agent Memory Types、Notion 风格文档 |
| **Style 5 — Glassmorphism** | 暗色渐变背景、毛玻璃卡片 | Multi-Agent 协作图、高端演示 |
| **Style 6 — Claude Official** | 暖白底 (#f8f6f3)、Anthropic 配色 | 系统架构、白皮书 |
| **Style 7 — OpenAI Official** | 纯白底、OpenAI 配色 | API Integration Flow、官方文档 |

每种风格背后都有**可执行的 Prompt Recipe**，不是靠运气，是靠回归测试验证过的稳定输出。

---

## 三、AI/Agent 领域专属模式

fireworks-tech-graph 不仅仅是通用的 UML 生成器。它内置了 AI/Agent 领域的专属形状语义库：

| 形状 | 语义 | 示例 |
|------|------|------|
| 双边框矩形 | LLM | GPT-4、Claude、DeepSeek |
| 六边形 | Agent | Coordinator Agent、Research Agent |
| 环形圆柱 | Vector Store | Pinecone、Milvus、Qdrant |
| 语义箭头 | 颜色+虚线编码 | write（实线）/read（虚线）/async（点线）|

**内置领域模式**：
- RAG（Retriever → Vector DB → Generator）
- Agentic Search（Query → Retrieve → Synthesize）
- Mem0（User → Memory Manager → Multi-Storage）
- Multi-Agent（Mission Control → Specialist Agents → Synthesis）
- Tool Call（User → Agent → Tool Runtime → Response）

---

## 四、与 Claude Code 的深度集成

fireworks-tech-graph 本身就是一个 Claude Code Skill（Badge 显示在 GitHub 首页），设计初衷之一就是服务于 AI Coding 工作流：

> "If you are building agent infrastructure, AI IDEs, internal copilots, developer tools, technical documentation systems, or applied AI workflow products..."

它的使用场景：
- **Cursor Composer 输出结果可视化**：把 Composer 的思维链变成架构图
- **Claude Code 执行结果的结构化呈现**：让 AI 生成的技术方案变成可读的图
- **Multi-Agent 协作的流程图**：把 Agent 之间的通信模式可视化

---

## 五、技术实现

### 核心依赖
```python
# SVG 生成后导出 PNG 的推荐方式
cairosvg  # 最佳渲染质量
rsvg-convert  # 备选
puppeteer  # 可选
```

### 导出规格
- **输出分辨率**：1920px 宽（2× Retina）
- **PNG 格式**：无损压缩，适合技术图（文字/线条清晰）

### 形状语义系统
- **Shape Vocabulary**：LLM = 双边框 rect，Agent = 六边形，Vector Store = ringed cylinder
- **Arrow Vocabulary**：颜色 + 虚线模式区分 read/write/async/loop

---

## 六、写作思考

这个项目让人印象深刻的不是技术实现，而是**设计决策的精准性**：

1. **为什么是 7 种而不是 1 种**：太多风格会让人选择困难，太少会失去适用范围。7 是一个刚好够用又不至于让用户陷入"风格选择焦虑"的数字
2. **为什么做 Claude Code Skill**：这个工具的目标用户就是用 Claude Code 写代码的人——图是为代码服务的，不是独立存在的
3. **为什么强调 CairoSVG**：PNG 的质量是技术图的命根子，JPEG 压缩会让文字和线条出现伪影。CairoSVG 能保证输出质量

**笔者认为**：fireworks-tech-graph 的真正价值不是"帮你画图"，而是**把技术图的生成从"设计问题"变成"描述问题"**——你不需要懂设计，只需要描述系统，它就能生成 publication-ready 的图。这与 Claude Code 把编程从"写代码"变成"说需求"的逻辑一脉相承。

---

## 七、关联文章

本文与以下文章形成闭环：

- **Cursor Cloud Agent 四条工程教训**（Articles）— AI Coding 的工程实践
- **Claude Code Best Practices for Agentic Coding**（Articles）— Claude Code 的使用模式

fireworks-tech-graph 是 AI Coding 工具链中的一个节点：**当 AI Coding Agent 生成了架构方案或技术决策后，用 fireworks-tech-graph 把文字描述变成可视化的架构图**，让人类的审核成本大幅降低。

---

**引用来源**：

1. "Stop drawing diagrams by hand. Describe your system in English or Chinese — get publication-ready SVG + PNG technical diagrams in seconds." — [GitHub README](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)
2. "All samples exported at 1920px width (2× retina) via cairosvg. PNG is lossless and the right choice for technical diagrams — sharp edges, no JPEG compression artifacts on text/lines." — [GitHub README](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)
3. "If you are building agent infrastructure, AI IDEs, internal copilots, developer tools, technical documentation systems, or applied AI workflow products, I am open to scoped paid sprints..." — [GitHub README](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)

---

> **相关工具推荐**：
> - [yizhiyanhua-ai/fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) — 7 风格技术图生成（Claude Code Skill）
> - [bradzhang.dev/case-studies/fireworks-tech-graph](https://bradzhang.dev/en/case-studies/fireworks-tech-graph) — 商业案例研究