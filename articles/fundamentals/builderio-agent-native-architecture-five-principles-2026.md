# Agent-Native 五大架构原则：从 AI 特征到 Agent-First

> 本文系统梳理 **Agent-Native** 软件架构的五大设计原则：当 Agent 和 UI 操作同一组 Actions、共享同一份状态、遵守同一套权限时，AI 应用才能真正从「附加能力」升级为「应用一等公民」。Builder.io 团队提出这一范式旨在解决当前 AI 应用普遍存在的「UI 与 Agent 漂移」结构性问题。

---

## 背景：从 AI-enabled 到 AI-native 再到 Agent-native

当下 AI 应用的混乱命名体系是讨论架构的真正起点：

| 范式 | 测试方法 | 典型代表 |
|------|---------|---------|
| **AI-enabled** | 移除 AI，产品仍基本可用？→ 是 | 多数 SaaS 的聊天侧栏 |
| **AI-native** | 移除 AI，产品是否崩塌？→ 是 | 编程助手、图像生成器、Chat-first 研究工具 |
| **Agent-native** | UI 和 Agent 能否操作同一组 workflow？→ 是 | Email 客户端：UI 整理 + Agent 自动归档/打标签 |

**关键区分**：AI-native 强调「没有 AI 产品就不存在」；Agent-native 进一步要求「AI 是核心，但产品依然保留完整的人机界面」。

历史类比是 **mobile-native**：mobile-native 不是把桌面网站塞进小屏幕，而是从一开始就围绕移动设备的约束和优势（触摸、相机、定位、有限屏幕、间歇性注意力）设计。Agent-native 应用同理——围绕 Agent 的约束和优势（自然语言、工具调用、上下文、后台执行、人机监督）从一开始就设计。

---

## 五大架构原则（核心）

### 1. Agent UI Parity（Agent-UI 对等）

> **Anything the UI can do, the agent can do. Anything the agent can do should be visible, inspectable, or controllable through the product's interface, logs, permissions, or state.**

测试方法很简单：如果 UI 可以「归档邮件、创建仪表盘、安排会议、更新记录、渲染视频」，那么 Agent 也应通过**同一个底层能力**执行相同动作——不是屏幕抓取 UI，也不是脆弱的旁路通道，而是直接调用驱动产品的同一组 capability。

反例：聊天面板只能起草回复（有用但浅）。Agent-native 的邮件应用让 Agent 能起草、查看 thread、加标签、归档通知、路由客户邮件、从 CRM 拉上下文，**最终发送决策仍留给人**——Agent 在操作邮件产品本身，而不只是评论。

### 2. Define Actions Once（一次定义，到处暴露）

传统软件团队常常这样演化：一个 UI 动作 → 一个 API 端点 → 一个自动化 hook → 一个 LLM 工具定义 → 一个 CLI 命令 → 一份说明它们关系的文档。每次复制都产生漂移。最终没人信任这个抽象。

**Define-once 模式**：从单一动作定义（archive email / create dashboard / render video / schedule meeting）出发：
- UI 调用它
- Agent 把它当作 tool
- 外部 client 触达它
- 其他 Agent 通过支持的协议路由到它

代码层面的形态不是「一堆一次性集成」，而是一个动作定义：

```typescript
// 一次定义，UI/Agent/HTTP/MCP/A2A/CLI 全部触达
export default defineAction({
  schema: z.object({
    emailId: z.string(),
    body: z.string(),
  }),
  run: async ({ emailId, body }) => {
    await db.insert(replies).values({ emailId, body });
  },
});
```

### 3. Context Awareness（上下文感知）

Agent 不能被当成独立的后台进程。它需要知道你在看什么、什么被选中、哪些 filter 处于激活状态、它在工作时发生了什么变化。

实践做法：
- UI 在用户浏览应用时**写入导航状态**
- `view-screen` 动作给 Agent 提供当前视图的**新鲜快照**
- `navigate` 动作让 Agent 在用户要求「打开某条记录/thread/图表/文档/任务」时**移动 UI**

这就是为什么 Agent-native 应用感觉不同于「贴在产品上的聊天机器人」：高亮一段文字要求重写，Agent 知道是哪一段；查看客户账户时，Agent 操作那个账户；Agent 创建草稿/更新仪表盘/标记任务完成，UI 自动刷新——因为两边读写同一份数据。

### 4. Live Sync via Database（通过数据库的实时同步）

实时同步不需要脆弱的浏览器自动化或长寿命基础设施。框架模式可以保持故意简单：

> **Actions 写入 SQL → version 变化 → UI 轮询更新并 invalidate 正确数据**

重要的不是轮询间隔，而是**数据库是 UI 与 Agent 之间的协调层**。这让整套架构能在 serverless 环境中工作，因为没有长连接、没有事件总线、没有共享内存——只有一个真理之源（SQL）。

### 5. Observability and Audit（可观测性与审计）

Agent 不能黑盒运行。应用需要暴露：
- Agent 当前在做什么（实时进度）
- 它调用了哪些 action、参数是什么、结果如何
- 用户可以中断、修改、给出反馈
- 每个操作都有可追溯的日志（权限、上下文、来源）

这与 Claude Code / Cursor 的设计哲学一致——Agent 不是「按了按钮就跑」，而是「每一步都可见、可中断、可引导」。

---

## 与传统架构的对比

| 维度 | AI-enabled SaaS | Raw Agent | Agent-native |
|------|----------------|-----------|--------------|
| 产品形态 | SaaS + 聊天侧栏 | 空白文本框 | 完整应用 + 内嵌 Agent |
| Agent 访问权限 | 部分（少数动作）| 全部（但无结构）| **全部（与 UI 同源）**|
| 状态管理 | UI 状态独立 | 无状态 | **共享 SQL 状态**|
| 工作流 | 固定按钮 | 自由但无引导 | **按钮 + Agent 双路径**|
| 多 Agent 协作 | 不支持 | 部分 | **A2A + MCP 协议原生支持**|
| 部署复杂度 | 低 | 低 | 中（需统一 action 层）|

---

## 工程实现的关键决策

### Action Schema 是契约的核心

Action 不能只是函数，必须有明确的：
- **Schema**（输入参数验证）
- **Permissions**（谁能调用）
- **Side effects**（修改什么资源）
- **Audit log**（调用记录）

这与 Anthropic 推动的「Tools as Contracts」、OpenAI 的 Function Calling 协议方向一致——Agent 调用的是声明式的能力，而不是副作用未知的函数。

### 协议层是分发机制

现代 Agent-native 应用应原生支持多种协议：
- **MCP**（Model Context Protocol）：Agent 调用外部工具
- **A2A**（Agent-to-Agent）：Agent 之间协作
- **HTTP/CLI**：传统 client 调用
- **Native chat**：嵌入应用的聊天 widget

BuilderIO 的 agent-native 框架通过「同一个 action surface 暴露给所有协议」实现这一目标——ACP（Agent Communication Protocol）则更适合 coding agent/editor 互操作的场景。

---

## 与现有 Agent 框架的对比

| 框架 | Agent-Native 程度 | 关键差异 |
|------|-------------------|---------|
| **LangChain** | 部分 | 偏 LLM 编排，UI 集成弱 |
| **Claude Agent SDK** | 中 | Coding agent 强，应用集成需自建 |
| **OpenAI Agents SDK** | 中 | 工具调用标准化，但状态管理分散 |
| **Mastra** | 中 | TypeScript-first，但 action 协议化弱 |
| **Agent-Native (BuilderIO)** | **高** | **Action 同时驱动 UI/Agent/协议** |

---

## 应用场景与限制

### 适合场景

- **协作型产品**（文档、项目管理、设计工具）—— 人机需要共享状态
- **复杂工作流产品**（CRM、ERP、邮件）—— 多步骤、多角色
- **数据驱动应用**（BI、analytics）—— 决策需要 UI 探索 + Agent 自动化

### 当前限制

- **学习曲线陡**：开发者需理解 action/protocol/state 三层抽象
- **框架尚早**：BuilderIO 的 agent-native 仍在早期，需要更多生产验证
- **数据库依赖**：所有 action 必须经过 SQL 层，对纯 in-memory 工作流不友好

---

## 关键洞察

> **真正的 Agent-native 不是「应用加了个 Agent」，而是「Agent 和 UI 共享同一份应用模型」。**

当你设计新功能时，问自己：
1. 这个动作 UI 能做，Agent 能做吗？
2. Agent 操作时，UI 能实时反映吗？
3. 用户能随时中断、修改、引导 Agent 吗？
4. 所有 Agent 操作有审计日志吗？

如果四个答案都是「是」，你就在构建 Agent-native。否则你在构建「AI-enabled SaaS」或「裸 Agent」。

---

## 引用与参考

- **原文**: [Agent-native architecture - Builder.io Blog](https://www.builder.io/blog/agent-native-architecture)
- **姊妹篇**: [How to build agent-native applications (and what not to do)](https://www.builder.io/blog/agent-native-apps)
- **延伸阅读**: [Why the best agent-native apps use less AI](https://www.builder.io/blog/why-the-best-agent-native-apps-use-less-ai)
- **配套项目**: [BuilderIO/agent-native](https://github.com/BuilderIO/agent-native) — 1,003⭐ ISC 协议，开源框架
- **相关 cluster**:
  - `articles/fundamentals/builderio-agent-native-paradigm-equal-citizens-2026.md` — R456 姊妹篇：「Equal Citizens」范式总览
  - `articles/harness/github-copilot-app-agent-native-desktop-multi-agent-workspace-isolation-2026.md` — 另一 Agent-native 实现

---

> **核心命题**: Agent-native 架构的本质是「Action 一次定义，五端共享」——UI、Agent、HTTP、MCP、A2A、CLI 都从同一个 action surface 派生，数据库是协调层。这与传统「UI/API/工具各搞一套」的漂移模式形成鲜明对比，是 AI 应用从「能用」走向「产品级」的必经之路。