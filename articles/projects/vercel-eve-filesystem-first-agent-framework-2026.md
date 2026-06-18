# Vercel eve：一个"Agent 就是目录"的生产级框架

**Stars**: 705⭐（发布 1.5 天，Apache 2.0）
**URL**: https://github.com/vercel/eve
**发表日期**: 2026-06-17
**关联 Article**: R430 Anthropic recursive self-improvement（形成"AI 加速发展 → 需要 durable production agent 基础设施"对位）

---

## 核心命题

Vercel 说了一个听起来很简单但工程意义极深的话：**Agent 就是一个目录**。不是配置对象，不是类实例，而是一个遵循约定目录结构的普通文件夹——`agent.ts` 定义模型、`instructions.md` 定义人格、`tools/` 放能力、`channels/` 放通信接入点、`schedules/` 放定时任务。

这个设计选择背后的逻辑是：Agent 代码应该和普通代码一样可阅读、可版本控制、可 Fork、可协作。框架解决的是"如何在生产环境跑起来"，而不是"怎么写一个能工作的原型"。

> "Agents today are where the web was before frameworks, with everyone hand-rolling the same plumbing and nothing carrying over to the next one. Next.js ended this for the web, and eve is doing the same for agents."
> — Vercel 官方博客

---

## 一、"Agent is a Directory" 的工程本质

看一个具体的 eve agent 目录结构：

```
my-agent/
└── agent/
    ├── agent.ts          # 模型配置
    ├── instructions.md   # 系统级人格定义
    ├── tools/            # 工具（typed functions）
    │   └── get_weather.ts
    ├── skills/           # 按需加载的技能
    │   └── plan_a_trip.md
    ├── channels/         # 消息通道（HTTP/Slack/Discord）
    │   └── slack.ts
    └── schedules/        # 定时任务
        └── weekly_recap.ts
```

这不仅仅是组织形式的变化。传统框架里，这些概念被编码在配置对象、继承体系或运行时注册表中——你需要读框架文档才能理解 agent 能做什么。而 eve 的目录结构**就是文档**：看到 `channels/slack.ts` 就知道这个 agent 接入了 Slack，看到 `schedules/` 就知道它会主动定时执行。

### 为什么这个设计值得注意

笔者认为，这是第一个真正把"Agent 的可发现性"纳入核心设计目标的框架。大多数框架的问题是：你拿到一个 agent 项目，不知道它能做什么、依赖什么、在哪里配置什么。eve 通过目录约定让这些信息对人和对 AI coding agent 都是显式的。

更重要的是，`node_modules/eve/docs` 包含了完整文档——意味着 coding agent 可以直接本地读取框架文档，而不需要联网查资料。这是"文档作为代码资产"思维的具体落地。

---

## 二、生产级能力的工程实现

### 2.1 Durable Execution（持久化执行）

eve 的每个会话都是 checkpointed workflow：

> "every conversation is a durable workflow with each step checkpointed, so a session can pause, survive a crash or a deploy, and resume exactly where it stopped. This durability is built on the open-source Workflow SDK."

这直接回应了 R430 Anthropic 数据的核心命题：当 AI 产出速度达到人类 8 倍、任务时长每 4 个月翻倍时，session 崩溃的代价也在同比放大。一个需要运行数天的 coding agent 如果每次部署都重置，就无法真正实现"长时自主运行"。

Durable execution 的 checkpoint 机制让 agent 可以在 crash 后从上一个稳定状态恢复，而不是从头开始。这是让 agent 从"工具"进化到"同事"的基础设施条件。

### 2.2 Sandboxed Compute（沙箱计算）

```
"The code your agents write should be treated as untrusted, so eve keeps agent-generated code out of your application runtime entirely."
```

eve 的沙箱设计把 agent 生成代码的执行与控制 agent 的 harness runtime 完全隔离。这个设计原则笔者认为值得所有生产级 agent 系统参考：永远不要让 agent 代码直接跑在主应用进程中。

支持的沙箱后端：
- **Vercel Sandbox**（线上部署）
- **Docker**（本地）
- **microsandbox**
- **just-bash**

沙箱是 adapter 模式的，这意味着你可以为自己的基础设施写一个 adapter。这种开放性设计避免了被特定供应商绑定的风险。

### 2.3 Human-in-the-loop Approvals

任意 action 都可以配置为需要人工审批，agent 在审批点暂停等待：

这对应的是"权限分层"概念在 agent 系统中的具体落地。不是简单的"允许/禁止"，而是**按需挂起 + 人工接管**。

---

## 三、与现有框架的差异化定位

| 维度 | 传统 LangChain/CrewAI | Vercel eve |
|------|----------------------|-----------|
| **Agent 定义方式** | Python/JS 类 + 配置对象 | 文件系统目录 |
| **Durable execution** | 需自行实现或用第三方 | 内置于框架 |
| **沙箱隔离** | 通常缺失或简陋 | adapter 模式，灵活可插拔 |
| **文档集成** | 外部文档网站 | `node_modules/eve/docs` 本地化 |
| **Harness 内省性** | 低（运行时才知道能做什么）| 高（目录结构即 API 文档）|
| **上手成本** | 高（大量配置项）| 低（约定优于配置）|

笔者认为 eve 的真正竞争对手不是 LangChain，而是"手写 Agent  plumbing"这个广泛的实践——它瞄准的是那些还没用框架、还在每个项目里重写相同基础能力团队。

---

## 四、关联 R430：Recursive Self-Improvement 需要 Durable Infrastructure

R430 追踪的 Anthropic 内部数据显示：任务时长每 4 个月翻倍，6 个月从 26% 到 76% 的成功率。这意味着：

1. **Agent 运行时间越来越长**——从分钟级到小时级到天级
2. **长时运行的失败成本越来越高**——崩溃一次丢失的产出量在增加
3. **需要 checkpoint/resume 机制**——这是 eve durable execution 的核心场景

eve 的 durable execution + sandboxed compute 组合，恰好是"recursive self-improving agent"能够真正在生产环境稳定工作的基础设施工件。

---

## 五、局限性

- **Beta 阶段**：框架、API、文档都可能变化，不适合直接用于生产关键系统
- **生态较新**：705 stars（1.5天）显示社区兴趣，但生态插件还不丰富
- **强依赖 Vercel 基础设施**：本地开发可用 Docker/microsandbox，但生产部署建议用 Vercel
- **主要是 TypeScript/Node 生态**：对 Python-first 的团队有一定迁移成本

---

## 六、快速上手

```bash
# 初始化一个新 agent
px eve@latest init my-agent

# 进入目录
cd my-agent

# 替换 agent/instructions.md 定义人格
# 添加 agent/tools/*.ts 定义工具

# 启动开发
npm run dev
```

配置模型：

```typescript
// agent/agent.ts
import { defineAgent } from "eve";
export default defineAgent({
  model: "anthropic/claude-opus-4.8",
});
```

---

## 总结

Vercel eve 的核心贡献不是"又一个 agent 框架"，而是**把 agent 项目变成普通代码项目**：目录即结构、文件即文档、`git clone` 即可 Fork 别人的 agent。

这对行业的影响在于：降低 agent 的协作门槛，让 agent 项目的可发现性、可复现性、代码审查流程与普通软件工程实践对齐。

笔者认为，这是 2026 年 agent 框架领域最有代表性的"工程机制"创新之一——不是在拼谁支持更多模型或更多工具，而是在解决"agent 项目如何像普通代码一样被工程化"这个根本问题。

**关联 R430 核心数据**：当 AI 自身发展速度进入 8x 阶段，agent 项目工程化的需求不是锦上添花，而是让这 8x 产出真正可持续运转的必要条件。

---

*本文档首次追踪来源：Vercel eve 发布博客（2026-06-17）+ GitHub README*
