# mcp-use：当 MCP 协议从"工具定义"进化到"全栈应用平台"

> mcp-use 是目前增长最快的 MCP 开发框架，GitHub 10,109 Stars，TypeScript + Python 双语言SDK，支持构建可交互的 MCP Apps（跨 Claude/ChatGPT 的 React 组件）。本文分析它的核心架构设计和为什么"MCP App"这个概念比"工具集合"更有工程价值。

---

## 核心命题

MCP 协议（Model Context Protocol）在 2025 年是"让 AI 调用工具"的标准，到了 2026 年，mcp-use 正在把它升级为"让 AI 运行全栈应用"的基础设施。

区别在于：工具是**离散的函数调用**，App 是**带状态的交互界面**。当你让 Agent 调用一个天气工具，返回的是一段文字；当你让 Agent 调用一个 MCP App，返回的是一个可交互的 React 组件。这是 mcp-use 带来的范式转变。

---

## 两种构建模式：MCP Server vs MCP App

mcp-use 区分了两种构建层次：

### MCP Server：经典的工具提供者

```typescript
import { MCPServer, text } from "mcp-use/server";
import { z } from "zod";

const server = new MCPServer({ name: "my-server", version: "1.0.0" });

server.tool({
  name: "get_weather",
  description: "Get weather for a city",
  schema: z.object({ city: z.string() }),
}, async ({ city }) => {
  return text(`Temperature: 72°F, Condition: sunny, City: ${city}`);
});

await server.listen(3000);
```

这就是传统的 MCP 工具定义——声明一个工具名称、schema、处理器，返回 text。但 mcp-use 的 Server 远不止于此。

### MCP App：跨客户端的交互组件

```typescript
// Server 端：声明 widget
server.tool({
  name: "get-weather",
  description: "Get weather for a city",
  schema: z.object({ city: z.string() }),
  widget: "weather-display",  // 指向 React 组件
}, async ({ city }) => {
  return widget({
    props: { city, temperature: 22, conditions: "Sunny" },
    message: `Weather in ${city}: Sunny, 22°C`,
  });
});

// Widget 端：React 组件
const WeatherDisplay: React.FC = () => {
  const { props, isPending, theme } = useWidget();
  return (
    <div style={{ background: theme === "dark" ? "#1a1a2e" : "#f0f4ff" }}>
      <h2>{props.city}</h2>
      <p>{props.temperature}° — {props.conditions}</p>
    </div>
  );
};
```

widget 在 `resources/` 目录下自动发现，不需要手动注册。当 Agent 调用这个工具，Claude/ChatGPT 会渲染对应的 React 组件——这意味着**同一个工具在不同客户端呈现不同的交互形式**。

---

## MCP Inspector：本地调试基础设施

mcp-use 自带 Inspector（类比 VS Code 的 Playwright Testing Weekly），可以在本地快速验证 MCP Server 和 App：

> "Inspector at http://localhost:3000/inspector"

对于 Agent 开发者，这意味着你可以在部署前**独立验证工具行为**，而不是依赖 Agent 实际调用才能发现参数问题。这是 MCP 生态缺少的关键基础设施——官方 MCP SDK 没有 Inspector，mcp-use 补上了。

---

## 10,109 Stars 的增长逻辑

mcp-use 的快速上升有明确的技术原因：

**1. 跨语言 SDK**：TypeScript + Python 同时支持，覆盖了 Claude（主要 TypeScript）和 ChatGPT（Python 友好）两个生态  
**2. MCP Apps 的差异化**：不是又一个"MCP Server 模板集合"，而是引入了 widget 概念，让工具有了 UI 表达能力  
**3. 一键部署到 Manufact MCP Cloud**：连接 GitHub 仓库，自动构建、部署、监控  
**4. 内置 Skill**：在 [skills.sh](https://skills.sh/mcp-use/mcp-use/mcp-apps-builder) 上有官方的 mcp-use skill，可以直接安装到 Claude Code/Copilot

---

## 与 Replit Skills 的主题关联

本文的 Article 分析了 Replit 的 Skill 自定义系统（Custom Instructions + SKILL.md），mcp-use 提供了 Skill 层下面的**协议实现**：Skill 定义"做什么"，MCP Server/App 定义"怎么做"。两者结合，才是完整的 Agent 能力扩展体系。

Replit 的 SKILL.md 格式可以引用 mcp-use 构建的 MCP Server 作为技能实现——Skill 是文档层，MCP Server 是执行层。这是 Skill 系统的工程落地路径。

---

## 笔者的判断

mcp-use 的 Widget 概念是点睛之笔，但它真正解决的不是"工具不够漂亮"的问题，而是**Agent 与用户之间的交互带宽问题**。当 Agent 返回一段文字，用户需要自己理解和执行；当 Agent 返回一个可交互组件，用户可以直接操作。这在复杂任务（数据分析、图表生成、文稿演示）中差异巨大。

对于 Agent 工程的价值：如果你在构建需要用户参与的 Agent 工作流，mcp-use 的 App 模式值得优先考虑；如果你只需要 Agent 调用工具完成自动化任务，标准的 MCP Server 模式足够了。

---

## 原文引用

> "mcp-use is the fullstack MCP framework to build MCP Apps for ChatGPT / Claude & MCP Servers for AI Agents." — [GitHub README](https://github.com/mcp-use/mcp-use)

> "MCP Apps let you build interactive widgets that work across Claude, ChatGPT, and other MCP clients — write once, run everywhere." — [GitHub README](https://github.com/mcp-use/mcp-use)

| 项目 | 信息 |
|------|------|
| **GitHub** | [mcp-use/mcp-use](https://github.com/mcp-use/mcp-use) |
| **Stars** | 10,109 ⭐ |
| **License** | — |
| **语言** | TypeScript (78.4%), Python (16.4%) |
| **官网** | [mcp-use.com](https://mcp-use.com) |
| **MCP Inspector** | [inspector.mcp-use.com](https://inspector.mcp-use.com/inspector) |
