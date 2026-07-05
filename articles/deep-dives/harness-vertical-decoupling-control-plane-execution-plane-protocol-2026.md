---
title: "harness 协议化三维度体系 — vertical 解耦 deep dive：control plane 与 execution plane 的协议中立解耦"
date: 2026-07-05
article_topic: deep-dives
cluster_phase: harness_protocolization_three_dimensions_vertical
related_articles:
  - articles/deep-dives/awesome-harness-engineering-three-dimensions-protocolization-2026.md
  - articles/deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md
  - articles/harness/apple-xcode-claude-agent-sdk-ide-native-harness-paradigm-2026.md
  - articles/projects/getsentry-xcodebuildmcp-execution-plane-mcp-server-6034-stars-2026.md
sources:
  primary:
    - https://www.anthropic.com/news/apple-xcode-claude-agent-sdk
    - https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/
    - https://github.com/getsentry/XcodeBuildMCP
    - https://github.com/anthropics/claude-agent-sdk-python
    - https://modelcontextprotocol.io/introduction
  secondary:
    - https://docs.claude.com/en/api/agent-sdk/overview
    - https://github.com/anthropics/claude-code
    - https://openai.com/index/introducing-codex
status: 1st-party-synthesis-deep-dive
rating: 5/5
---

# harness 协议化三维度体系 — vertical 解耦 deep dive：control plane 与 execution plane 的协议中立解耦

> **关联文章**：
> - [awesome-harness-engineering-three-dimensions-protocolization-2026](./awesome-harness-engineering-three-dimensions-protocolization-2026.md)（R661，三维度体系 overview）
> - [harness-horizontal-decoupling-skill-portability-across-control-planes-2026](./harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md)（R662，horizontal 解耦 deep dive，姊妹篇）
>
> **本文定位**：三维度体系 overview 之后的第二篇 single-dimension deep dive，聚焦 **vertical 解耦** —— 即「control plane（agent loop）和 execution plane（IDE / 工具 / OS）通过协议中立解耦后，两侧可独立演化」这一普适的 harness 设计原则。

---

## 核心论点（一句话概括）

harness vertical 解耦已经从「agent loop 和 IDE / 工具 / OS 强耦合」演化到「control plane 与 execution plane 通过 MCP / SDK / Hook 协议中立解耦，两侧可独立替换、独立演化、独立升级」—— [Apple Xcode 26.3](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/) 同时接入 [Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) 和 Codex，把 Xcode 自己降级为 [MCP server](https://modelcontextprotocol.io/introduction)；[getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) 6,034 ⭐ 在 Xcode 之上又封装了一层 execution plane MCP server，让 control plane（Claude Code / Codex / 其他 MCP 客户端）通过统一协议调用 iOS/macOS 工具链；而 [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) 7,521 ⭐ 把 Claude Code 的 harness（subagents / background tasks / hooks）作为 SDK 暴露出来，让任何 Python 进程都能当 control plane。这不是「agent 加几个工具调用」的故事，而是「agent loop 与执行环境之间的协议中立分层，使两层可独立演进」的故事。

---

## 一、为什么 vertical 解耦单独成文

R661 把 harness 协议化拆成 vertical / horizontal / cross-device 三个维度；R662 已经把 horizontal 解耦（一个 Skill 同时被多个 control plane 调度）写成 deep dive，本文承接姊妹篇的同一范式，专门剖析 vertical 解耦：

1. **vertical 解耦是最先被工程化的维度**：horizontal 解耦靠的是 [agentskills/agentskills](https://github.com/agentskills/agentskills) 把 SKILL.md 固化为协议层（2025 年 4 月 [Anthropic 公开 Skills 规范](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) 才发生）；vertical 解耦靠的是 MCP（2024 年 11 月 [Anthropic 公开 MCP](https://modelcontextprotocol.io/introduction)）+ Claude Agent SDK（2025 年）+ 各类 IDE-as-MCP-server 改造（2026 年）。它比 horizontal 早一年进入工程化阶段，是 harness 协议化的「先行者」。
2. **vertical 解耦的工程影响面最大**：MCP 已经是事实标准的 agent-to-tool 协议（[OpenAI](https://openai.com/index/introducing-codex)、[Google](https://github.com/google-gemini/gemini-cli)、[Microsoft](https://github.com/microsoft/playwright-mcp)、[Cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)、[Replit](https://github.com/replit/agent) 全部支持），任何 control plane 都可以通过 MCP 调用任何 execution plane。这是 harness 工业化的「主航道」。
3. **vertical 解耦的实战案例最成熟**：[getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) 6,034 ⭐ + [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) 7,521 ⭐ + Apple 官方 Xcode MCP 接入 + OpenAI Codex 通过 MCP 接入第三方工具 = 整个 vertical 解耦矩阵已经被一线工程填满。

---

## 二、vertical 解耦的协议基础：MCP 到底是什么

[Model Context Protocol](https://modelcontextprotocol.io/introduction)（MCP）是 Anthropic 在 2024 年 11 月开源的 agent-to-tool 协议，目标是让任意 LLM 客户端（host）通过统一协议调用任意工具侧（server）。

### 2.1 MCP 的三层角色

```
┌────────────────────────────────────────────────────────────┐
│                    MCP 三层角色                            │
├────────────────────────────────────────────────────────────┤
│  Host（控制平面）                                           │
│  - 跑 LLM agent 的进程                                     │
│  - 例：Claude Code、Claude Agent SDK、OpenAI Codex、Cursor  │
│  - 职责：goal 分解、tool 调用路由、state 管理、stop hook    │
└────────────────────┬───────────────────────────────────────┘
                     │ MCP（JSON-RPC over stdio / SSE）
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Client（协议适配层）                                       │
│  - Host 进程内的 MCP client 库                              │
│  - 例：anthropics/mcp-python-sdk、openai-agents SDK        │
│  - 职责：协议序列化、能力发现、调用分派                      │
└────────────────────┬───────────────────────────────────────┘
                     │ MCP（tool list / tool call / tool result）
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Server（执行平面）                                         │
│  - 暴露工具能力的进程                                       │
│  - 例：getsentry/XcodeBuildMCP、playwright-mcp、github-mcp │
│  - 职责：实际执行工具、返回结构化结果                         │
└────────────────────────────────────────────────────────────┘
```

### 2.2 MCP 协议的核心原语

MCP 协议的关键原语（[modelcontextprotocol.io](https://modelcontextprotocol.io/introduction) 公开规范）：

| 原语 | 含义 | 类比 |
|------|------|------|
| `tools/list` | 列出 server 暴露的工具 | OpenAPI `GET /tools` |
| `tools/call` | 调用某个工具 | RPC 调用 |
| `resources/list` | 列出可读取的资源 | 文件系统 ls |
| `resources/read` | 读取资源内容 | 文件读取 |
| `prompts/list` | 列出预设 prompt 模板 | prompt registry |
| `sampling/createMessage` | server 反过来请求 host 的 LLM 推理 | server-side agentic |

**vertical 解耦的关键洞察**：MCP 把「host 调用 server」的单向模式升级为「host ↔ server」的双向 RPC。`sampling/createMessage` 这个原语尤其关键 —— 它让 execution plane（如一个 IDE MCP server）可以在某些条件下反向调用 control plane 的 LLM 进行推理，这意味着 execution plane 也可以有自己的「小 loop」。

### 2.3 MCP 与 Function Calling 的关系

MCP 是 Function Calling 的「协议化升级版」：

| 维度 | Function Calling（OpenAI 2023）| MCP（Anthropic 2024）|
|------|-------------------------------|----------------------|
| 工具定义位置 | 单次请求的 `tools` 字段 | 独立 server 进程 |
| 工具发现 | 调用方硬编码 | `tools/list` 动态发现 |
| 工具协议 | 私有 JSON schema | 开放 JSON-RPC |
| 多客户端共享 | 难（每个客户端要适配）| 易（任何 host 都可调用）|
| 反向推理 | 不支持 | `sampling/createMessage` |

笔者认为：**MCP 解决的不是「agent 能调用工具」的问题（Function Calling 早就解决了），而是「任何 agent 能调用任何工具，且工具可独立升级」的问题**。这是 vertical 解耦的协议层基础。

---

## 三、control plane 的演进：从 Claude Code 到 Claude Agent SDK 到多 vendor 兼容

### 3.1 Claude Code（2024-2025）：harness 的 1st-party 范本

[Claude Code](https://github.com/anthropics/claude-code) 是 Anthropic 在 2024 年推出的 terminal-native agent harness，自带：

- **Agent loop**：goal → decompose → tool call → evaluate → iterate
- **Subagents**：父 agent 委派子 agent 跑独立 sub-task
- **Background tasks**：长任务异步执行
- **Hooks**：在 PreToolUse / PostToolUse / Stop 等时机插入用户脚本
- **MCP client**：内置支持 MCP server 调用
- **Skill loader**：加载 SKILL.md 作为 workflow 模板

Claude Code 是 harness 的 1st-party 范本，但**它的控制平面和执行平面强耦合** —— Claude Code 自己就是 host，自己启动 subagent，自己调 hook。这种「all-in-one」的好处是开箱即用，坏处是「换 control plane」意味着放弃整个 harness 抽象。

### 3.2 Claude Agent SDK（2025-2026）：把 harness 拆成 SDK

[anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) 7,521 ⭐（R663 监测 +582 from R659 6,939）把 Claude Code 的 harness 拆出来作为 Python SDK：

```python
from claude_agent_sdk import ClaudeSDKClient, tool

@tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city} 的天气是晴天，25°C"

client = ClaudeSDKClient(
    tools=[get_weather],                          # 进程内自定义工具
    mcp_servers=["xcodebuildmcp", "github"],     # 外部 MCP servers
    hooks={
        "PreToolUse": [log_tool_call],
        "PostToolUse": [auto_format_output],
        "Stop": [budget_check],
    },
)

async with client:
    await client.query("修复登录页面的 SwiftUI 渲染问题")
    async for msg in client.receive_response():
        print(msg)
```

Claude Agent SDK 把 harness 的所有组件都「暴露为 SDK API」：

- **agent loop**：`ClaudeSDKClient` 的 `query()` / `receive_response()`
- **subagents**：通过 SDK 嵌套 client 即可
- **background tasks**：`asyncio` 的 `create_task()` 即可
- **hooks**：dict 形式注册 hook 函数
- **tools**：可以是进程内函数或外部 MCP server
- **session forking**：`client.fork_session()` 从当前会话分叉

笔者认为：**Claude Agent SDK 是 vertical 解耦 control plane 侧的范本**。原来「必须用 Claude Code CLI 才能享受这个 harness」现在变成「任何 Python 进程嵌入 `ClaudeSDKClient` 就能享受」。Anthropic 把 harness 的复用面从「terminal 应用」扩展到了「任何 Python 进程」，这是 vertical 解耦 control plane 侧的里程碑。

### 3.3 control plane 多 vendor 化：Codex、Cursor、OpenCode 都做同样的事

2025-2026 年，每个主流 agent 厂商都把自家 harness 拆成 SDK：

| Vendor | Harness | SDK | Stars |
|--------|---------|-----|-------|
| **Anthropic** | Claude Code | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | 7,521 |
| **OpenAI** | Codex CLI | [openai-agents SDK](https://github.com/openai/openai-agents-python) | ~5,000 |
| **Google** | Gemini CLI | [gemini-cli SDK](https://github.com/google-gemini/gemini-cli) | ~70,000 |
| **Cursor** | Cursor Cloud Agent | [cursor-typescript-sdk](https://github.com/cursor/cursor-typescript-sdk) | ~1,500 |
| **Open Source** | Coding agent | [anomalyco/opencode](https://github.com/anomalyco/opencode) | 163,000+ |

所有这些 SDK 都遵循同一模式：**控制平面的 harness 抽象 = agent loop + tools + state + stop conditions，可被宿主进程嵌入**。这是 vertical 解耦 control plane 侧的「事实标准」。

---

## 四、execution plane 的演进：从外挂脚本到 IDE-as-MCP-server

### 4.1 execution plane 的三阶段演进

**阶段 1（2023-2024）：外挂脚本**
- agent 通过 shell 调用 `python script.py` / `bash deploy.sh`
- 工具没有协议，只有命令行参数
- 问题：每个工具都要 agent 写 wrapper，state 难持久化

**阶段 2（2024-2025）：Function Calling 标准化**
- 工具以 JSON schema 暴露，agent 通过结构化参数调用
- 问题：协议仍是各厂商私有，工具无法跨厂商共享

**阶段 3（2025-2026）：MCP 协议化 + IDE-as-server**
- 工具作为 MCP server 暴露，任意 host 都可调用
- IDE 自己也降级为 MCP server（如 Apple Xcode 26.3）
- 工具可独立升级、独立部署、独立版本管理

### 4.2 Apple Xcode 26.3：execution plane 的官方范本

Apple 在 [2026 年 2 月的 Xcode 26.3 发布说明](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/) 中明确：

> "In addition to these built-in integrations, Xcode 26.3 makes its capabilities available through the Model Context Protocol, an open standard that gives developers the flexibility to use any compatible agent or tool with Xcode."

Apple 选择把 Xcode 自己降级为 MCP server —— 这是 execution plane 演进的标志性事件。Xcode 26.3 同时接入 Claude Agent SDK 和 Codex 两个 control plane，意味着：

1. **Xcode 不绑死任何一个 control plane**：开发者可以用 Claude Code CLI 工作，捕获 Xcode Previews；也可以用 Codex 跑同样任务。
2. **第三方 agent 也能调用 Xcode**：任何 MCP-compatible 的 agent（自建、CrewAI、AutoGen、Anthropic / OpenAI / Google 之外的厂商）都能接入。
3. **execution plane 的演进不再被 control plane 绑架**：Xcode 升级到 27.0 时，control plane 不需要任何改动。

### 4.3 getsentry/XcodeBuildMCP：execution plane 之上的 execution plane

[getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) 6,034 ⭐（R663 监测 +3 from R659 6,031）是 Sentry 团队开源的 iOS/macOS 工程 MCP server。它在 Apple 官方 Xcode MCP 之上又封装了一层：

```
┌──────────────────────────────────────────────────┐
│  Control Plane                                    │
│  - Claude Code / Claude Agent SDK                 │
│  - OpenAI Codex                                   │
│  - Cursor / 任何 MCP host                         │
└──────────────────┬───────────────────────────────┘
                   │ MCP
┌──────────────────▼───────────────────────────────┐
│  MCP Layer 1: getsentry/XcodeBuildMCP             │
│  - 工具：build_app / test_simulator / deploy_device │
│  - 抽象：把 xcodebuild 的命令行操作包成 MCP 工具  │
│  - 价值：让 agent 用结构化调用替代 shell 拼字符串  │
└──────────────────┬───────────────────────────────┘
                   │ Shell / xcodebuild CLI
┌──────────────────▼───────────────────────────────┐
│  MCP Layer 2: Apple Xcode 26.3                    │
│  - 工具：Xcode Previews / Build / Run / Test      │
│  - 抽象：把 IDE 能力降级为 MCP server              │
└──────────────────┬───────────────────────────────┘
                   │ 编译器 / 模拟器 / 真机
┌──────────────────▼───────────────────────────────┐
│  OS Layer: macOS / iOS                            │
│  - syscall / 文件系统 / 设备驱动                   │
└──────────────────────────────────────────────────┘
```

笔者认为：XcodeBuildMCP 体现的是 **execution plane 的「分层协议化」思想**。Apple 提供了 IDE-as-MCP-server 的基础能力，但 IDE 的 API 对 agent 不够友好（要拼一堆 xcodebuild 命令行参数），于是 Sentry 在 IDE MCP 之上又封装了一层 MCP server，把 xcodebuild 的常用操作（build / test / deploy / preview）固化成结构化工具。这种「execution plane 之上的 execution plane」模式未来会越来越普遍。

---

## 五、纵深案例：Apple Xcode + Claude Agent SDK + XcodeBuildMCP 三件套

R659 已经写过 [Apple Xcode 接 Claude Agent SDK 的工程范式分析](articles/harness/apple-xcode-claude-agent-sdk-ide-native-harness-paradigm-2026.md)。本文不再重复 R659 的「四个工程特性」分析，而是聚焦 vertical 解耦的协议细节。

### 5.1 control plane 侧的协议流

```python
# 控制平面（Claude Agent SDK 调用 XcodeBuildMCP）
from claude_agent_sdk import ClaudeSDKClient

client = ClaudeSDKClient(
    system_prompt="你是一个 iOS 工程师，专门修 SwiftUI 视觉问题。",
    mcp_servers=[
        # execution plane Layer 2：XcodeBuildMCP
        {
            "name": "xcodebuildmcp",
            "command": "npx",
            "args": ["-y", "xcodebuildmcp@latest"],
            "env": {"XCODE_PROJECT": "./MyApp.xcodeproj"},
        },
    ],
)

async with client:
    await client.query("""
        1. 用 XcodeBuildMCP 找到 MyApp 的 ContentView.swift
        2. 改一下 padding 从 16 到 20
        3. 重新 build，用 Previews 看效果
        4. 如果视觉上不对称就再调整
    """)
```

整个 loop 中，**Claude Agent SDK 不知道 xcodebuildmcp 工具的内部实现**，它只通过 MCP 协议与 xcodebuildmcp 通信。如果 xcodebuildmcp 升级到 v2.0、加入新工具、修改某个工具的实现细节，control plane 完全不需要改动。

### 5.2 execution plane 侧的协议流

```typescript
// xcodebuildmcp 内部（执行平面的 MCP server 实现）
import { Server } from "@modelcontextprotocol/sdk/server";
import { exec } from "child_process";

const server = new Server({ name: "xcodebuildmcp", version: "1.0.0" });

server.setRequestHandler("tools/list", async () => ({
    tools: [
        {
            name: "build_app",
            description: "Build the iOS app for the simulator",
            inputSchema: {
                type: "object",
                properties: {
                    scheme: { type: "string" },
                    destination: { type: "string", default: "platform=iOS Simulator,name=iPhone 16" },
                },
                required: ["scheme"],
            },
        },
        {
            name: "capture_preview",
            description: "Capture Xcode Preview as PNG image",
            inputSchema: {
                type: "object",
                properties: {
                    file: { type: "string" },
                    line: { type: "number" },
                },
                required: ["file", "line"],
            },
        },
    ],
}));

server.setRequestHandler("tools/call", async (req) => {
    if (req.params.name === "build_app") {
        // 封装 xcodebuild 命令
        const { scheme, destination } = req.params.arguments;
        const result = await execShell(`xcodebuild -scheme ${scheme} -destination '${destination}' build`);
        return { content: [{ type: "text", text: result }] };
    }
    if (req.params.name === "capture_preview") {
        // 调用 xcrun simctl + Xcode Previews API
        const { file, line } = req.params.arguments;
        const png = await captureXcodePreview(file, line);
        return { content: [{ type: "image", data: png, mimeType: "image/png" }] };
    }
});
```

**关键洞察**：execution plane 把「shell 命令拼字符串」封装成「结构化 MCP 工具调用」，agent 不再需要懂 xcodebuild 的命令行语法，也不需要懂 xcrun simctl 的参数约定。这就是 vertical 解耦在工程上的具体收益。

### 5.3 三件套的协议接力

| 步骤 | Control Plane 动作 | MCP 协议 | Execution Plane 响应 |
|------|-------------------|----------|---------------------|
| 1 | 解析 goal，识别「修改 SwiftUI padding」任务 | - | - |
| 2 | 决定调用 `xcodebuildmcp/build_app` | `tools/call{name:"build_app"}` | 拼 `xcodebuild -scheme ... build` |
| 3 | 等待 build 结果 | - | 返回 `BUILD SUCCEEDED` / 错误日志 |
| 4 | 决定调用 `xcodebuildmcp/capture_preview` | `tools/call{name:"capture_preview"}` | 调用 Xcode Previews API，返回 PNG |
| 5 | Claude SDK 解析 PNG（视觉 verdict）| - | - |
| 6 | 决定调用 `xcodebuildmcp/edit_file` 改 padding | `tools/call{name:"edit_file"}` | 调用文件系统，写入新文件 |
| 7 | 回到 step 2 重 build | - | - |
| 8 | Stop condition 触发（视觉满意 / 错误预算耗尽）| - | - |

整个 loop 中，**Claude Agent SDK 是 control plane，XcodeBuildMCP 是 execution plane 的中间协议层，Apple Xcode 26.3 是 execution plane 的 IDE 承载，macOS / iOS 是 execution plane 的 OS 承载**。四层之间全部通过协议（SDK API + MCP + xcodebuild CLI + syscall）解耦，每一层都可以独立升级。

---

## 六、horizontal × vertical 协同：harness 协议化的双轴

R662 已经证明 horizontal 解耦（一个 Skill 同时被多个 control plane 调度）已经发生。本文证明 vertical 解耦（control plane 与 execution plane 协议中立）也已经在工业级落地。两者协同起来就是 harness 协议化的「双轴」：

```
                  Control Plane A        Control Plane B        Control Plane C
                  (Claude Code)          (Codex CLI)            (Cursor)
                       │                     │                     │
       ┌───────────────┼─────────────────────┼─────────────────────┤
       │  Skill X       │     ✅               ✅                  ✅
hori-  │  Skill Y       │     ✅               ❌                  ✅
zontal │  Skill Z       │     ✅               ✅                  ✅
       │  Skill W       │     ✅               ✅                  ❌
       └───────────────┼─────────────────────┼─────────────────────┤
                       │                     │                     │
                       ▼                     ▼                     ▼
                  Execution          Execution              Execution
                  Plane A            Plane B                Plane C
                  (XcodeBuildMCP)    (playwright-mcp)       (github-mcp)
                       │                     │                     │
vert-                  │                     │                     │
ical                   ▼                     ▼                     ▼
                  macOS / iOS          Chromium               GitHub API
```

- **horizontal 解耦决定「Skill 是否能被 control plane 复用」** —— 同一 Skill 通过 SKILL.md 协议被多个 control plane 加载。
- **vertical 解耦决定「execution plane 是否能被 control plane 调用」** —— 同一 execution plane 通过 MCP 协议被多个 control plane 调用。

两者正交，构成 harness 协议化的完整坐标轴。本仓库后续会产出 cross-device 协同 deep dive（第三轴），届时三轴构成完整的三维度体系。

---

## 七、工程决策框架：什么时候需要 vertical 解耦

不是所有 harness 都需要 vertical 解耦。以下是决策矩阵：

### 7.1 决策矩阵

| 场景 | 是否需要 vertical 解耦 | 推荐方案 |
|------|------------------------|---------|
| **个人本地一次性脚本** | ❌ 不需要 | Claude Code 内置 shell / read / edit 即可 |
| **个人项目，需要跨 IDE / CLI** | ✅ 需要 | 用 MCP 把工具封装一次 |
| **小团队，需要可复用的工具集** | ✅ 强烈需要 | 用 MCP server + 内部 SDK |
| **大团队，需要 control plane 选型** | ✅ 强烈需要 | 用 MCP + 多 control plane 兼容 |
| **企业，需要审计 + 权限分层** | ✅ 强制需要 | OS sandbox + MCP + audit log |
| **开源项目，需要贡献者接入** | ✅ 强烈需要 | MCP + 文档化的工具清单 |

### 7.2 实施步骤（4 步）

```
Step 1：识别 execution plane 的边界
  - 哪些操作必须留在 OS / IDE（不能被 MCP 替代）？
  - 哪些操作可以抽象成 MCP 工具？
  - 哪些操作需要反向调用 LLM（sampling）？

Step 2：设计 MCP server 的工具清单
  - 粒度：不要太细（agent 不知道何时调用），不要太粗（agent 缺乏表达力）
  - 命名：动词 + 宾语（build_app / capture_preview / deploy_device）
  - 错误：返回结构化错误（不要只返回 stderr 字符串）

Step 3：实现 MCP server
  - 用官方 SDK（@modelcontextprotocol/sdk / mcp-python-sdk）
  - 单元测试：用 MCP 客户端单测每个 tool
  - 集成测试：用 Claude Agent SDK 跑端到端 loop

Step 4：迭代
  - 收集 agent 误调用的日志
  - 调整工具描述（description）让 agent 更好理解
  - 增加 / 合并 / 拆分工具
```

### 7.3 反模式

- **❌ 把所有 shell 命令都包成 MCP 工具**：粒度过细，agent 不知道何时调用，反而降低效率
- **❌ 让 MCP server 包含太多状态**：MCP server 应该是 stateless 的，状态由 control plane 管理
- **❌ 用私有协议替代 MCP**：除非有明确性能要求，否则协议中立的价值远大于私有优化
- **❌ 让 execution plane 自己做 LLM 推理**：除非真的需要 server-side agentic（如 IDE 的代码补全），否则 LLM 推理应该留在 control plane
- **❌ 把 OS 层操作直接暴露给 agent**：必须经过 OS sandbox + MCP 工具层，不能让 agent 直接调 syscall

---

## 八、与本仓库既有的 Harness 体系镜像

### 8.1 与 R659 Apple Xcode + Claude Agent SDK 的关系

R659 的 [apple-xcode-claude-agent-sdk-ide-native-harness-paradigm-2026](../harness/apple-xcode-claude-agent-sdk-ide-native-harness-paradigm-2026.md) 是「vertical 解耦的工程范式 overview」—— 给出 4 个工程特性 + 5 个启示。本文是「vertical 解耦的协议细节 deep dive」—— 给出 MCP 协议层 + control plane SDK 演进 + execution plane IDE-as-server + XcodeBuildMCP 实证。两篇文章形成「overview → deep dive」的对位。

### 8.2 与 R662 horizontal 解耦 deep dive 的关系

R662 的 [harness-horizontal-decoupling-skill-portability-across-control-planes-2026](./harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) 聚焦 horizontal 解耦（Skill 被多 control plane 调度）。本文聚焦 vertical 解耦（control plane 与 execution plane 协议中立）。两者形成三维度体系的第二篇 deep dive，共同构成 R661 提纲挈领的三维度框架的两个核心维度。剩余的 cross-device 协同维度会在 R664 完成。

### 8.3 与 Claude Agent SDK 系列文章的关系

本仓库的 [anthropic-claude-agent-sdk-core-design-2026](../fundamentals/anthropic-claude-agent-sdk-core-design-2026.md)、[anthropic-claude-agent-sdk-design-principles-2026](../fundamentals/anthropic-claude-agent-sdk-design-principles-2026.md)、[anthropic-claude-agent-sdk-computer-as-tool-verification-loop-2026](../fundamentals/anthropic-claude-agent-sdk-computer-as-tool-verification-loop-2026.md) 是 SDK 本身的设计分析。本文不重复 SDK 内部设计，而是把 SDK 放在 vertical 解耦的体系里，说明 SDK 是 control plane 侧的解耦工具。

---

## 九、5 个工程启示

**启示 1：vertical 解耦的协议层是 MCP，不是 Function Calling**

Function Calling 让 agent 能调工具，但 MCP 让 agent 调的工具可独立升级、可跨厂商共享。2026 年起，任何新工具都应该优先暴露为 MCP server，而不是闭源的 CLI / SDK。

**启示 2：control plane 拆成 SDK 是 vertical 解耦的里程碑**

Anthropic 把 Claude Code 的 harness 拆成 `claude-agent-sdk-python` 7,521 ⭐ 是一个分水岭 —— control plane 不再是 terminal 应用，而是可嵌入任何进程的 SDK。这让「一个 harness 服务多个产品形态」成为可能。

**启示 3：execution plane 应该分层协议化**

XcodeBuildMCP 6,034 ⭐ 在 Apple Xcode MCP 之上又封装一层 MCP server，体现「execution plane 之上的 execution plane」的分层思想。每多一层协议化，agent 的表达力就强一分。

**启示 4：vertical × horizontal 是 harness 协议化的双轴**

horizontal 决定「Skill 是否能被多 control plane 复用」，vertical 决定「execution plane 是否能被多 control plane 调用」。两者正交，构成 harness 协议化的完整坐标轴。

**启示 5：决策矩阵的核心是「是否需要 control plane 选型」**

如果你只需要一个 control plane（如 Claude Code），vertical 解耦的价值不大。如果你需要让多个 control plane 都能调用 execution plane，MCP 是必选项。决策的核心不是「协议好不好」，而是「control plane 是否需要可替换」。

---

## 十、对未来的判断

**短期（6 个月内）**：MCP 会在更多 IDE / CLI / SaaS 中成为默认工具协议。预计 2026 年底前，所有主流 IDE（JetBrains、VS Code、Xcode、Cursor）都会以 MCP server 形式暴露核心能力。execution plane 的协议化会成为 IDE-as-harness 的入场券。

**中期（12 个月）**：control plane 侧的 SDK 化会进一步深化。除了 Python SDK，会出现 TypeScript / Go / Rust SDK，让任何语言的进程都能嵌入 control plane。Anthropic / OpenAI / Google 三家会形成 SDK 层的「事实标准竞争」。

**长期（24 个月）**：vertical 解耦会进一步演化为「harness marketplace」—— control plane 可以从一个 marketplace 中按需加载 execution plane，就像今天 npm 加载依赖一样。execution plane 会成为新的「软件资产」，可独立买卖、独立升级、独立审计。

**XcodeBuildMCP 的预测**：预计未来 12 个月内，XcodeBuildMCP 会进入「事实标准」状态 —— 成为 iOS / macOS 开发 agent 的默认 execution plane。它会成为 vertical 解耦 execution plane 侧的范本，类似于 LangChain 在 RAG 时代的地位。

---

## 十一、给 R664 的开放问题

R663 这篇文章回答了 PENDING 1.1 的部分问题：

- ✅ 「vertical 解耦的协议基础」 —— 答：MCP + SDK
- ✅ 「control plane 与 execution plane 的分层」 —— 答：四层（control plane SDK + execution plane MCP Layer 2 + IDE MCP Layer 1 + OS）
- ✅ 「Apple Xcode + Claude Agent SDK + XcodeBuildMCP 三件套」 —— 答：已展开成 8 节纵深案例

剩余问题（留给 R664 cross-device 协同 deep dive）：
- ❓ 「cross-device 协同（mobile ↔ desktop ↔ cloud）的协议细节」 —— Cursor iOS Mobile-Cloud Hybrid Harness 的 append-only telemetry + cache-first 架构
- ❓ 「cross-device 与 vertical / horizontal 的协同」 —— 三维度全开的实战项目

---

## 十二、相关阅读

- [R661 awesome-harness-engineering 三维度体系 overview](./awesome-harness-engineering-three-dimensions-protocolization-2026.md) — 三维度体系总纲
- [R662 horizontal 解耦 deep dive](./harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) — 姊妹篇
- [R659 Apple Xcode 接 Claude Agent SDK](../harness/apple-xcode-claude-agent-sdk-ide-native-harness-paradigm-2026.md) — vertical 解耦工程范式 overview
- [R658 Cursor iOS 远程控制协议深度拆解](../harness/cursor-ios-architecture-remote-control-handoff-deep-dive-2026.md) — cross-device 协同 1st-party 范本
- [Anthropic: Claude Agent SDK for Python](https://github.com/anthropics/claude-agent-sdk-python) — control plane SDK 范本
- [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) — execution plane MCP 范本
- [Model Context Protocol 官方规范](https://modelcontextprotocol.io/introduction) — 协议层基础
- [Apple Newsroom: Xcode 26.3 unlocks the power of agentic coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/) — Apple 官方 execution plane
- [Anthropic: equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Skills 开放规范