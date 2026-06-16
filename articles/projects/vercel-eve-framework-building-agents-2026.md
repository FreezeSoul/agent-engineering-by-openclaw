# Vercel Eve — The Framework for Building Agents

> The Framework for Building Agents

- **Stars**: 12 ⭐
- **License**: Apache 2.0
- **Created**: 2026-06-16
- **Owner**: Vercel
- **Topics**: `agent` `framework` `harness` `sandbox` `typescript` `javascript`

## 一句话描述

Vercel Eve 是一个结构化的 Agent 框架，通过 `defineAgent` / `defineTool` 等 TypeScript API 定义 agent 及其工具，以文件夹作为项目组织单位，提供了从脚手架到生产的完整开发体验。

---

## 核心 API 设计

### defineAgent

```ts
import { defineAgent } from "eve";

export default defineAgent({
  model: "openai/gpt-5.4-mini",
  name: "weather-agent",
});
```

简洁的 agent 定义，指定模型和名称。

### defineTool

```ts
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "Get the current weather for a city.",
  inputSchema: z.object({
    city: z.string(),
  }),
  async execute(input) {
    return {
      city: input.city,
      condition: "Sunny",
      temperatureF: 72,
    };
  },
});
```

工具定义采用 Zod 做输入校验，模式清晰。

### 指令（Instructions）

Agent 的行为通过 `agent/instructions.md` 定义：

```md
You are a weather-focused assistant. Be concise, accurate, and explicit when you use a tool.
```

自然语言指令 + 文件系统的组合，体现了 Eve "Framework for Building Agents" 的定位。

---

## 项目结构

```
my-agent/
├── package.json
├── tsconfig.json
└── agent/
    ├── agent.ts          # Agent 定义
    ├── instructions.md   # 行为指令
    ├── skills/           # 技能定义
    ├── tools/            # 工具实现
    ├── connections/      # 外部连接
    ├── sandbox/          # 沙箱配置
    ├── channels/         # 渠道配置
    ├── subagents/        # 子 Agent
    ├── schedules/        # 定时任务
    └── lib/              # 业务逻辑
```

这种结构将 **agent 的所有维度**（行为、工具、连接、沙箱、子agent、渠道）都纳入版本控制，体现了"一切皆文件"的工程化理念。

---

## CLI 工作流

```bash
# 初始化新 agent
npx eve@latest init my-agent

# 添加 Web Chat 应用
npx eve@latest init my-agent --channel-web-nextjs

# 开发模式
eve dev          # 本地运行时 + 交互式终端 UI
eve build        # 编译 .eve/ → 构建输出
eve start        # 服务构建产物
eve info         # 显示发现结果和编译产物
```

`eve init` 自动完成：
1. 创建项目结构
2. 安装依赖
3. 初始化 Git
4. 启动开发服务器

---

## 沙箱与安全

从项目结构看，Eve 将 sandbox 作为一等公民：

- 每个 agent 可配置独立的 sandbox 环境
- sandbox 与 agent 一起版本化
- 支持 subagents，每个 subagent 也有独立上下文

这是 Vercel 在 Serverless 领域的经验向 Agent 领域的延伸——**沙箱即基础设施**。

---

## 框架定位分析

Eve 的定位介于：

- **低层抽象**（直接调用 LLM API）之上
- **端到端平台**（如 OpenClaw、AgentForge）之下

它提供的是：**结构化的 agent 开发框架**，而非托管服务。

对比主流框架：

| 维度 | Eve | LangChain | CrewAI | AutoGen |
|------|-----|-----------|--------|---------|
| 语言 | TypeScript | Python | Python | Python/.NET |
| 部署 | 自行部署 | 嵌入式 | 嵌入式 | 嵌入式 |
| 沙箱 | 原生支持 | 需集成 | 需集成 | 需集成 |
| 脚手架 | `eve init` | 无官方 | 无官方 | 无官方 |
| 厂商 | Vercel | - | - | Microsoft |

---

## 质量评估

- ⭐⭐⭐ — Vercel 品牌背书，TypeScript-first 设计合理，结构化程度高；12 stars 说明刚发布或未推广
- **核心价值**：将 Vercel 在 Next.js 生态的工程化经验带入 Agent 开发
- **待观察**：生态系统成熟度（skills、connections 的丰富程度）

---

## 来源

- GitHub: https://github.com/vercel/eve
- Homepage: https://vercel.com/eve
- Docs: `docs/README.md`
