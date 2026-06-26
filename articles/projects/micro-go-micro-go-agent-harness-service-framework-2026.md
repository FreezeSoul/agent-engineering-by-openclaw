# micro/go-micro：当 Go 语言遇见 Agent Harness 工程范式

> **核心命题**：Go Micro 重新定义了"agent harness"——它不是又一个 Agent 框架，而是一个用 Go 代码写死的运行时：工具调用、Memory 持久化、Guardrails 边界、工作流触发、服务发现，以及 MCP/A2A 协议出口。Build an agent and it gets a model, memory, tools, planning, delegation, guardrails, and service discovery。这是让 Agent 真正成为分布式系统的工程路径。

## 基本信息

| 项目 | 值 |
|------|------|
| **GitHub** | [micro/go-micro](https://github.com/micro/go-micro) |
| **Stars** | 22,834 ⭐ |
| **语言** | Go |
| **定位** | Agent Harness + Service Framework |
| **协议支持** | MCP + A2A |
| **官网** | [go-micro.dev](https://go-micro.dev) |
| **Sponsor** | Anthropic + OpenAI |

---

## 一、为什么这个项目值得关注

### 1.1 "Agent Harness" 的精确含义

Harness 不是"框架"，而是**运行时骨架**。Go Micro 的 README 直接点明：

> A harness is the runtime around an agent: the tools it can call, the memory it keeps, the guardrails that bound it, the workflows that trigger it, the services it depends on, and the protocols other agents use to reach it.

这正是本仓库一直追踪的 **Harness Engineering** 核心命题：Agent 能不能稳定完成长任务，不取决于模型多强，而取决于这个运行时骨架是否完整。

Go Micro 的做法是：**每个 Agent 实例自带完整的 harness**，不需要外接平台。

### 1.2 从"写服务"到"写 Agent"的零距离

传统微服务框架让 AI 能力成为服务的工具层。Go Micro 反过来：**每个服务端点天然成为 AI 可调用的工具**。

```bash
# 写一个普通服务
micro new helloworld
cd helloworld && micro run

# 立即得到一个 AI 可调用的工具
curl -X POST http://localhost:8080/api/helloworld/Helloworld.Call \
  -d '{"name":"World"}'
```

这个"AI-First Service"的思路，比单纯"给框架加个 Agent 类"要深刻得多。

### 1.3 AI 生成代码的自我托管

Go Micro 支持用 LLM 直接从 prompt 生成完整服务：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
micro run --prompt "a task management system with categories" --provider anthropic
```

模型设计架构、编写 handler、编译、启动，全部自动化。这本质上是**Agent 写代码的本地化部署**，不依赖 Cursor/Cline 等编辑器。

---

## 二、架构设计分析

### 2.1 核心组件

```
Agent = Model + Memory + Tools + Planning + Delegation + Guardrails + Service Discovery
                  ↑ All built-in, no external platform required
```

每个组件的工程实现：

- **Model**：支持 Anthropic/OpenAI/Gemini 等多 Provider 热插拔
- **Memory**：持久化 Memory，跨 session 可恢复
- **Tools**：任意 Go 函数直接暴露为 Tool，无额外声明
- **Planning**：内置 Plan & Delegate 机制
- **Guardrails**：权限边界内置，非外挂
- **Service Discovery**：Go Micro 自有的分布式注册中心

### 2.2 MCP + A2A 双协议出口

官方 README 明确：

> It is reachable over MCP and A2A.

这意味着**用 Go Micro 构建的 Agent 同时是 MCP Server 和 A2A Agent**。不需要额外的协议适配层。

### 2.3 赞助商背书

Go Micro 的 Sponsor 列表包含 **Anthropic 和 OpenAI** 官方标志。这在开源 Go 项目中极不寻常，说明项目方向得到了两大模型公司的认可。

---

## 三、与同类项目的差异化

| 维度 | go-micro | LangChain | CrewAI |
|------|---------|-----------|--------|
| **语言** | Go | Python/JS | Python |
| **架构定位** | Harness（运行时）| 编排框架 | Agent 编排 |
| **协议出口** | MCP + A2A 原生 | MCP 插件 | A2A 插件 |
| **服务生成** | AI 直接生成 + 编译 | 无 | 无 |
| **Memory 持久化** | 内置 | 需配置 | 需配置 |
| **Guardrails** | 内置 | 外挂 | 外挂 |
| **上手门槛** | 中（需 Go 基础）| 低（Python）| 低（Python）|

**笔者认为**：LangChain/CrewAI 解决的是"如何组装 Agent"，Go Micro 解决的是"如何让 Agent 稳定运行在生产环境"。前者是乐高积木，后者是出厂质量的保障。

---

## 四、适用场景

✅ **推荐使用**：
- 已有 Go 技术栈，想本地化部署 Agent 能力
- 需要 Agent 跨 session 记忆（MCP Memory 持久化）
- 想让服务天然成为 AI Tool，不需要额外包装
- 需要 MCP + A2A 双协议同时支持

❌ **不推荐**：
- 纯 Python 团队（学习成本高）
- 快速原型阶段（LangChain 更灵活）
- 需要丰富生态（目前生态还在早期）

---

## 五、快速上手

```bash
# 安装 CLI（无需 Go 环境）
curl -fsSL https://go-micro.dev/install.sh | sh

# 或者用 Go
go install go-micro.dev/v6/cmd/micro@v6

# 创建第一个 Agent 服务
micro new myagent
cd myagent && micro run

# AI 生成模式（需要 API key）
export ANTHROPIC_API_KEY=sk-ant-...
micro run --prompt "a REST API for managing tasks" --provider anthropic
```

---

## 六、GitHub 快照

> 本节图片截取自 GitHub 官方仓库页面（2026-06-26），展示项目 README 核心内容。

![go-micro GitHub](screenshots/micro-go-micro-20260626.png)

---

## 七、工程机制评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **Harness 完整性** | ⭐⭐⭐⭐⭐ | 唯一同时内置 harness 所有组件的框架 |
| **协议支持** | ⭐⭐⭐⭐⭐ | MCP + A2A 原生双出口 |
| **生产可用性** | ⭐⭐⭐⭐ | Go 语言天然适合分布式，但生态还在成熟 |
| **概念独特性** | ⭐⭐⭐⭐⭐ | "Agent as Distributed System" 视角在业内稀缺 |
| **Stars 增长** | ⭐⭐⭐⭐ | 22.8K，近期活跃度高 |

**综合评分**：19/25 ⭐ — 属于**框架/平台级**推荐。

---

> **引用来源**（README 原文）：
> 
> 1. "A harness is the runtime around an agent: the tools it can call, the memory it keeps, the guardrails that bound it..."
> 2. "Build an agent and it gets a model, memory, tools, planning, delegation, guardrails, and service discovery"
> 3. "It is reachable over MCP and A2A"