# nexu-io/html-anything：Agent 原生的 HTML 编辑器，4689 Stars

## 核心论点

**html-anything 将 AI Agent 的 HTML 生成能力封装成「75 Skills × 9 Surface」的矩阵结构，让同一套 AI 能力可以根据目标场景（杂志、海报、PPT、推文等）自动适配输出格式，弥合了「通用编码 Agent」与「专业内容产出」之间的鸿沟**。

---

## 解决的问题

通用 AI 编码 Agent（如 Claude Code、Cursor）擅长生成功能性代码，但在需要**专业格式输出**时往往需要用户反复调整：

- 生成一篇公众号文章，需要手动复制到编辑器排版
- 生成一张海报，需要在设计工具中重新调整尺寸和样式
- 生成一个数据报告，需要在 HTML 中手动添加响应式布局

html-anything 的解法是：**让 Agent 在生成阶段就知道目标格式要求**，而不是生成后再调整。

---

## 核心架构：Skill × Surface 矩阵

### 75 Skills（技能维度）

每个 Skill 定义了 AI 在该领域的能力边界和输出规范：

- 杂志排版（magazine）
- PPT 演示（deck）
- 社交媒体海报（poster）
- 推文/XHS（tweet）
- 原型设计（prototype）
- 数据报告（data report）
- Hyperframes

### 9 Surfaces（场景维度）

不同 Surface 定义了目标媒介的物理特性和交互规范：

- Web 响应式
- 移动端
- 打印版
- 社交媒体图片
- 邮件 Newsletter
- 文档/PDF
- 演示屏幕
- 短信/通知
- 聊天界面

---

## 技术实现亮点

### 零 API Key 设计

> "Zero API key — Claude Code / Cursor / Codex / Gemini / Copilot / OpenCode / Qwen / Aider."

这意味着用户不需要为服务付费，工具直接调用本地 Agent 的 API。这是 **Tool-as-a-Service** 模式的反转——不是 Agent 使用工具，而是工具驱动 Agent。

### 沙箱预览

生成的 HTML 在隔离环境中预览，避免恶意代码风险。

### 一键发布

支持直接发布到：
- 微信
- X (Twitter)
- 知乎
- HTML 文件下载
- PNG 图片导出

---

## Agent 工程视角

html-anything 展示了一个重要的工程趋势：**内容生成 Agent 正在从「代码生成器」向「成品输出器」演进**。

传统模式：
```
User → Agent → Code → User formats/adjusts → Final output
```

html-anything 模式：
```
User → Agent (with Surface context) → Formatted output
```

这种模式的关键在于 **Surface 上下文作为隐式规范**：Agent 不需要被告知「你应该生成什么格式」，而是直接获得了目标媒介的物理约束（尺寸、DPI、交互方式）。

---

## 与 Claude Code 的协同

对于 Claude Code 用户，html-anything 提供了一个具体的场景库——当需要生成非功能性 HTML 时（比如产品介绍页面、数据可视化报告），可以直接调用对应的 Skill × Surface 组合，而不需要每次都从头设计 prompt。

---

## 项目数据

| 指标 | 数值 |
|------|------|
| Stars | 4,689 |
| 架构 | TypeScript + Vite |
| 许可 | MIT |
| 定位 | AI Native HTML Editor |

---

## 笔判断

html-anything 的价值不在于技术突破，而在于 **场景封装**。它将「通用 Agent 能做什么」转化为「特定场景下 Agent 应该输出什么」，降低了使用门槛，提高了输出质量。

对于 Agent 工程的启示：**一个好的工具不需要让 Agent 变得更聪明，而是让 Agent 知道在什么场景下应该做什么**。

---

*来源：[GitHub - nexu-io/html-anything](https://github.com/nexu-io/html-anything)（Created May 2026）*