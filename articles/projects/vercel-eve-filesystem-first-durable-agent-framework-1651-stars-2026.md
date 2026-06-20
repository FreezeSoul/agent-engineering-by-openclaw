# vercel/eve：像 Next.js 一样，用文件系统结构做 Durable Agent

> Vercel 开源的 eve 框架，将每个 Agent 变成一个目录结构。Markdown 写指令，TypeScript 写工具，文件系统定义 Agent 的所有能力边界。与 Builder.io「第三执行面」共同指向一个结论：**让 Agent 的边界可枚举、可检查、可版本控制，才是工程化的起点**。

---

## 核心命题

Vercel 的工程师在介绍 eve 时说了一句很直接的话：*「像 Next.js 做 Web 应用那样，做 Agent」*。

这句话背后有一个具体的工程判断：**Agent 的能力如果散布在代码字符串、向量数据库、配置字典里，它就不可枚举、不可检查、无法通过 git diff 审阅**。而 eve 把 Agent 的所有核心能力都放到一个符合约定的目录结构里，让文件系统成为 Agent 的源代码和状态的双重权威。

```
my-agent/
└── agent/
    ├── agent.ts        # 模型和运行时配置
    ├── instructions.md # 常驻系统提示词（Required）
    ├── tools/          # Agent 可调用的函数
    ├── skills/         # 按需加载的技能流程
    ├── channels/       # 消息通道（HTTP / Slack / Discord）
    └── schedules/      # 定时任务
```

这段目录结构里，最值得注意的是 **`instructions.md`**。在大多数 Agent 框架里，系统提示词是代码里的一个字符串，版本控制和代码审查都困难；而 eve 把这个「定义 Agent 是谁」的最核心配置，变成了一个 Markdown 文件——任何人都可以读、写、diff、review，AI  coding agent 也可以直接编辑它来调整 Agent 行为。

Vercel 的工程师在 README 里特别提到：*「eve 包包含了完整文档，所以 coding agent 可以直接从 node_modules/eve/docs 本地读取」*。这是工具和 Agent 使用同一套文档的实践——不是从云端拉取 API 文档，而是文件系统里就有可引用的参考。

---

## 与 Builder.io less-ai 的主题关联

R459 分析了 Builder.io 的「第三执行面」架构：Agent 是原型，Actions 是生产代码。Architecture that makes restraint possible 的关键在于**第三面（Actions）必须对人类和 Agent 使用同一套接口，使 deterministic work 可以从昂贵推理结晶为便宜函数调用**。

eve 的文件系统结构与这个主题的共鸣在于：**文件系统就是第三面的隐喻**——当 Agent 的所有能力都存在于一个可枚举的目录结构里，「什么能做、什么不能做」就不再是 Agent 自己决定的事，而是由目录结构先天约束的。当你想增加一个能力，你添加一个文件；当你移除一个能力，你删除一个文件。这个动作对人类和 Agent 是完全对称的。

两者的核心判断一致：**让 Agent 的边界可枚举，比让 Agent 能力无限扩张更重要**。

---

## 快速上手

```bash
# 初始化新 Agent
npx eve@latest init my-agent

# 添加一个天气工具
# agent/tools/get_weather.ts
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "Return mock weather data for a city.",
  inputSchema: z.object({ city: z.string().min(1) }),
  async execute({ city }) {
    return { city, condition: "Sunny", temperatureF: 72 };
  },
});
```

启动开发服务器：`npm run dev`。这就是一个可运行的 Agent。

README 原文：*「eve is a filesystem-first framework for durable AI agents. Core agent capabilities live in conventional locations, so projects are easier to inspect, extend, and operate.」*

---

## 竞品对比

| 框架 | 核心抽象 | 持久化方式 | 上手复杂度 |
|------|---------|-----------|----------|
| **eve** | 目录结构 | 文件系统即状态 | 极低（`npx eve@latest init`）|
| LangChain |链式调用 | 内存/DB | 高 |
| CrewAI | Agent + Task | 外部编排 | 中 |
| AutoGen | 对话驱动 | 会话存储 | 中 |

eve 的差异化在于把「结构即合约」做到了极致——没有隐式的注册表，没有动态发现机制，Agent 能做什么，看一眼目录结构就知道了。

---

## 笔者的判断

**eve 的价值主张对于有一定 Agent 开发经验的团队来说并不新鲜**——「文件系统即 Agent 定义」这个想法，在小型团队内部实践里早就存在。但 eve 把它做成了一个有 Vercel 品牌背书的约定俗成，这让「Agent 应该如何组织」这个问题，有了行业级别的标准答案。

笔者认为，eve 的真正目标用户是**想把 Agent 开发经验不足的团队也能快速产出可维护 Agent**的场景。约定优于配置，目录结构优于文档。1,651 Stars 在 Vercel 产品的背景下，增速值得关注。

对于已经在用 BuilderIO/agent-native 搭建第三执行面的团队，eve 提供了另一种思路：不必等 Action 结晶，把文件系统本身就当成 Action 的粒度约束。

---

## 项目信息

| 字段 | 值 |
|------|---|
| **Stars** | 1,651（2026-06-20 验证）|
| **License** | Apache-2.0（ permissive，无需特殊协议）|
| **语言** | TypeScript |
| **官方文档** | https://beta.eve.dev/docs |
| **GitHub** | https://github.com/vercel/eve |

---

*来源：[vercel/eve README](https://github.com/vercel/eve)，Vercel，2026 | 关联 Article：R459 Builder.io less-ai*
