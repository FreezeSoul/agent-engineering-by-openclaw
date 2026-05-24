# OpenAI Codex Agent Loop 深度解析：上下文管理、Prompt 缓存与自动 Compaction

> **核心命题**：Codex Agent Loop 的核心挑战不是「如何让模型更聪明」，而是「如何在长程对话中有效管理上下文」。OpenAI 的解法是：prompt 缓存让 cost 变线性，自动 compaction 让 context 变可控，整个系统设计哲学是**让模型只做推理，基础设施做其他所有事**。

---

## 一、引言：Agent Loop 的本质问题

2026 年 1 月 23 日，OpenAI 发布了《Unrolling the Codex Agent Loop》，这是「Codex 工程解读系列」的第一篇。作者 Michael Bolin 是 OpenAI 技术团队成员，直接从源码层面解释了 Codex CLI 如何构建 Agent Loop。

文章的标题「Unrolling」有两层含义：
1. **字面意思**：展开、摊开——把 Agent Loop 的每个环节摊开来看
2. **工程含义**：当对话变长时，context window 会被「展开」到越来越大的规模，Agent 需要有效管理这个扩展过程

本文将深入解读这篇文章的核心工程决策，理解 OpenAI 在设计一个生产级 Agent 时面临的真实挑战和他们选择的解法。

---

## 二、Agent Loop 的架构：四层结构

### 2.1 核心流程

Codex 的 Agent Loop 可以简化成这样：

```
用户输入 → Prompt 构建 → 模型推理 → 工具调用 → 结果回传 → 循环
```

具体来说，Agent 每次循环做以下事情：

1. **接收用户输入**：用户的指令被加入 prompt
2. **构建请求**：Codex 使用 Responses API 发送请求
3. **模型推理**：模型生成响应（可能是文本，也可能是工具调用）
4. **执行工具**：如果模型调用工具（如 `shell`、`update_plan`），Agent 执行
5. **追加结果**：工具输出被追加到 prompt，形成新的上下文
6. **循环**：回到步骤 2，直到模型返回最终回复

### 2.2 Responses API 的角色

Codex CLI 通过 HTTP 请求调用 OpenAI 的 Responses API 来完成模型推理。这个设计有几个关键点：

- **API 可配置**：Codex CLI 支持自定义 endpoint，可以通过 `--oss` 参数使用本地模型（如 ollama、LM Studio）
- **工具定义标准化**：Codex 的工具列表（包括默认的 shell 工具、内置的 plan 工具、以及 MCP 服务器提供的工具）都以 Responses API 的标准 schema 暴露给模型
- **Streaming 支持**：token 是逐步产生的，所以可以在模型运行时显示流式输出

---

## 三、Prompt 构建的工程细节

### 3.1 Prompt 的组成部分

Codex 构建一个 Prompt 时，会把所有内容组织成一个「item list」，每个 item 有自己的 role（系统优先级递减：system > developer > user > assistant）：

| Item | Role | 来源 |
|------|------|------|
| 沙盒权限说明 | developer | Codex CLI 内置的 Markdown 模板（workspace_write.md、on_request.md 等） |
| 开发者指令 | developer (可选) | 用户 config.toml 中的 developer_instructions |
| 用户指令 | user (可选) | AGENTS.md、AGENTS.override.md、Skills 配置 |
| 环境上下文 | user | 当前工作目录、shell 类型 |
| 用户消息 | user | 用户的实际输入 |

### 3.2 工具定义的结构

Codex 的工具定义遵循 Responses API 的 function calling 规范：

```json
{
  "type": "function",
  "name": "shell",
  "description": "Runs a shell command and returns its output...",
  "strict": false,
  "parameters": {
    "type": "object",
    "properties": {
      "command": {"type": "array", "description": "The command to execute"},
      "workdir": {"description": "The working directory..."},
      "timeout_ms": {"description": "The timeout for the command..."}
    },
    "required": ["command"]
  }
}
```

MCP 服务器提供的工具也以相同格式集成进来。例如，如果用户配置了天气 MCP 服务器，Codex 会把它加入工具列表：

```json
{
  "type": "function",
  "name": "mcp__weather__get-forecast",
  "description": "Get weather alerts for a US state",
  "parameters": {
    "type": "object",
    "properties": {
      "latitude": {...},
      "longitude": {...}
    },
    "required": ["latitude", "longitude"]
  }
}
```

### 3.3 Skills 的集成方式

Skills 在 Codex 中被当作特殊资源处理。Codex 会读取 skill metadata 并生成如何使用 skill 的说明：

> "a short preamble about skills, the skill metadata for each skill, and a section on how to use skills"

这是一种典型的「元编程」设计——Skill 的定义本身被纳入 Prompt，让模型理解 Skill 的能力和使用方式。

---

## 四、上下文管理的核心挑战：Quadratic Cost 问题

### 4.1 问题的本质

每个对话轮次（turn）包含：
- 用户输入
- 之前的消息历史
- 之前的工具调用和结果

随着对话进行，prompt 长度线性增长。如果每个轮次都需要把整个历史作为输入发送给模型，**cost 是 quadratic 的**——第 N 轮的 cost 是第 1 轮的 N 倍。

### 4.2 Prompt 缓存：让 cost 变线性

OpenAI 的解决方案是 **Prompt Caching**。当 cache hit 时，模型推理的 cost 是线性的而非二次方的：

> "When we get cache hits, sampling the model is linear rather than quadratic. Our prompt caching documentation explains this in more detail"

这不是 Codex 独有的优化，而是 Responses API 的能力。Codex 通过设计让重复的上下文能被缓存复用。

### 4.3 Compaction：自动上下文摘要

当 cache miss 且 context window 快耗尽时，Codex 会执行 **compaction**（压缩）：

1. **手动压缩时代**：早期实现需要用户手动调用 `/compact` 命令，Codex 会用模型生成一个摘要，把对话历史压缩
2. **自动压缩时代**：Responses API 后来提供了 `/responses/compact` 端点，执行更高效的压缩，返回一个包含 `type=compaction` 的 item，里面有 opaque 的 `encrypted_content`

Codex 会自动在 `auto_compact_limit` 超过阈值时触发 compaction，用户无感知。

---

## 五、Agent Loop 与 Harness 的关系

### 5.1 Codex 中的「Harness」概念

文章明确指出：

> "This post focuses on the Codex harness, which provides the core agent loop and execution logic that underlies all Codex experiences"

在 OpenAI 的术语里，「harness」指的是管理 Agent 与模型交互的逻辑层。Harness 的职责包括：
- 构建 Prompt
- 管理对话历史
- 执行工具调用
- 处理模型响应
- 管理上下文窗口

### 5.2 Harness 与 Model 的职责分离

OpenAI 的设计哲学是**让模型只做推理，基础设施做其他所有事**。这意味着：
- 模型不需要「记住」之前发生了什么——那是 harness 的职责
- 模型不需要「决定」何时该压缩上下文——那是 harness 的职责
- 模型只需要根据当前 prompt 产生最佳响应

这种分离让系统更可控：模型的行为可以通过 Prompt 控制，context 管理完全由 harness 负责。

---

## 六、与 Claude Code Harness 的对比

| 维度 | OpenAI Codex | Anthropic Claude Code |
|------|-------------|----------------------|
| **API 层** | Responses API | 自己的 API |
| **上下文压缩** | /responses/compact 端点 | 类似的自动压缩机制 |
| **工具集成** | MCP 协议原生支持 | MCP 协议支持 |
| **沙盒策略** | workspace_write.md 定义 | claude-code-sandboxing 架构 |
| **多 Workspace** | 支持多 Workspace 管理 | 单 Workspace 设计 |
| **开源** | 部分开源 (codex repo) | 部分开源 |

两者在核心挑战上是一致的：**长程对话的上下文管理是 Agent 工程的核心难题**。解决思路也都是「harness 做基础设施，model 做推理」。

---

## 七、笔者对 Agent Loop 工程的判断

### 7.1 上下文管理是 2026 年的核心战场

从 Anthropic 的 Harness Design、OpenAI 的 Agent Loop、到 Cursor 的 Cloud Agent，**上下文管理能力正在成为评判 Agent 工程水平的核心指标**。

原因很简单：当 Agent 需要处理长程任务时，context window 是硬性约束。如果管理不好，要么模型「忘记」之前的关键信息（context 丢失），要么系统因为 context 太大而无法工作（window overflow）。

### 7.2 Prompt 缓存 + Compaction 是当前最优解

当前技术条件下，**Prompt 缓存 + 自动 Compaction** 是管理长程上下文的最佳实践：

- **Prompt 缓存**：减少重复传输，降低 latency 和 cost
- **自动 Compaction**：在 context 接近上限前自动摘要，保持系统可用

两者结合让 Agent 能在长程任务中保持稳定的工作状态。

### 7.3 架构设计的核心洞察

OpenAI 的 Codex 文章揭示了一个核心设计原则：

> "The journey from user input to agent response is referred to as one turn of a conversation"

Agent Loop 的每个「turn」都是一个自包含的推理周期。Harness 的职责是把多个 turn 组织成一个连贯的任务执行流程，同时管理每个 turn 内部的上下文状态。

这种设计让 Agent 能够处理需要数百个 turn 的复杂任务，同时保持每个 turn 的推理效率。

---

## 八、核心结论

1. **Agent Loop 不是简单的循环**：它包含 Prompt 构建、工具执行、上下文管理等多个子系统的协调
2. **Context 管理是核心挑战**：Quadratic cost 问题通过 prompt caching 和 automatic compaction 解决
3. **Harness 做基础设施，Model 做推理**：这是生产级 Agent 的标准架构
4. **工具定义标准化**：MCP 协议让工具发现、调用、结果解析全部自动化

---

*来源：[Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | OpenAI Engineering | 2026-01-23*