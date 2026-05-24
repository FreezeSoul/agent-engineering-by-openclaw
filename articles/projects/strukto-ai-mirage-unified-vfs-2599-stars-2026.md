# Mirage：统一虚拟文件系统，Agent 的「万物皆文件」梦想

**目标用户画像**：需要让 AI Agent 同时操作多个后端服务（S3、Slack、GitHub、Gmail、MongoDB 等）的开发者，厌倦了为每个服务单独实现工具接口。

**核心结论**：Mirage 把「多服务的复杂 API」抽象成「统一的文件系统操作」，让 Agent 用熟悉的 bash 工具（`cat`、`grep`、`cp`）完成跨服务的复杂任务。当工具数量膨胀到数十个时，这种抽象不是优化，是生存问题。

**一手来源**：[strukto-ai/mirage GitHub README](https://github.com/strukto-ai/mirage)（2026-05-24，2,599 Stars）

---

## 场景锚定

想象一个跨服务的任务：

> "从 S3 读取包含 'alert' 的日志行，统计数量，然后将结果写入 Slack 的 #alerts 频道"

没有 Mirage：
- 实现 S3 文件读取工具
- 实现 Slack 消息发送工具
- 实现跨服务的逻辑编排
- 每个工具的认证、错误处理、重试单独处理

有 Mirage：

```python
ws = Workspace({
    '/s3': S3Resource(S3Config(bucket='logs')),
    '/slack': SlackResource(SlackConfig()),
})

# Agent 完全不知道自己在调用什么 API——只是在操作文件系统
await ws.execute('grep alert /s3/logs/*.csv | wc -l')
await ws.execute('cat /s3/report.csv | head -100')
```

**核心价值**：Agent 不需要学习每个服务的 API，只需要会用 bash。

---

## 技术拆解

### 核心设计：虚拟文件系统抽象

> "Mirage is a Unified Virtual File System for AI Agents: a single tree that mounts services and data sources like S3, Google Drive, Slack, Gmail, and Redis side-by-side as one filesystem. AI agents reach every backend with the same handful of Unix-like tools."
> — [README](https://github.com/strukto-ai/mirage)

这个设计的底层逻辑：**Agent 最熟悉的操作接口是文件系统**。Mirage 没有发明新 API，而是复用了 LLM 预训练数据中大量出现的 bash/filesystem 操作模式。

**支持的挂载类型**：

| 类别 | 服务 | 文件系统路径 |
|------|------|-------------|
| 云存储 | S3 / R2 / OCI / GCS | /s3 |
| 协作工具 | GitHub / Linear / Notion | /github, /linear |
| 消息 | Slack / Discord / Telegram | /slack |
| 办公 | Gmail / GDrive / GDocs | /gmail, /docs |
| 数据库 | MongoDB / Redis | /mongodb, /redis |
| 计算 | SSH | /ssh |

### 同一命令，不同挂载点的不同行为

> "Override a command for a specific resource + filetype — `cat` on a Parquet file in /s3 renders rows as JSON instead of raw bytes."
> — [README](https://github.com/strukto-ai/mirage)

这是 Mirage 的工程亮点——**工具行为由资源类型决定，而非硬编码**。

```python
# 读 Parquet 文件 → 自动转换为 JSON
await ws.execute('cat /s3/data/report.parquet')

# 读 Slack JSON 日志 → 直接渲染为可读格式
await ws.execute('cat /slack/general/*.json | grep alert')
```

同一个 `cat` 命令，在 /s3 读 Parquet 输出 JSON，在 /slack 读 JSON 输出渲染后的内容。Agent 不需要知道这些细节。

### 两级缓存：性能优化的工程实现

> "Every Workspace ships with a two-layer cache so repeated work against remote backends hits local state instead of the network: Index cache for listings and metadata; File cache for object bytes."
> — [README](https://github.com/strukto-ai/mirage)

跨服务操作延迟高，缓存是关键：

- **Index cache**：目录列表和元数据，第一次访问走 API，之后从缓存读取（可配 TTL）
- **File cache**：文件字节，第一次从源站读取，之后从本地缓存读取

### 与 Agent 框架的集成

> "Works with major agent application frameworks: OpenAI Agents SDK, Vercel AI SDK (TypeScript), LangChain, Pydantic AI, CAMEL, and OpenHands."
> — [README](https://github.com/strukto-ai/mirage)

开源项目最怕「Demo 漂亮但无法集成」。Mirage 提供了与主流框架的适配层：

**OpenAI Agents SDK 集成**：

```python
from mirage.agents.openai_agents import MirageSandboxClient

client = MirageSandboxClient(ws)
agent = SandboxAgent(
    name="Mirage Agent",
    model="gpt-5.4-nano",
    instructions=ws.file_prompt,
)

result = await Runner.run(
    agent,
    "Summarize /s3/data/report.parquet into /report.txt.",
    run_config=RunConfig(sandbox=SandboxRunConfig(client=client)),
)
```

**Vercel AI SDK 集成**：

```typescript
import { mirageTools } from '@struktoai/mirage-agents/vercel'
import { buildSystemPrompt } from '@struktoai/mirage-agents/openai'

const { text } = await generateText({
    model: openai('gpt-5.4-nano'),
    system: buildSystemPrompt({ mountInfo: { '/': 'In-memory filesystem' } }),
    prompt: "Use readFile to read /docs/paper.pdf",
    tools: mirageTools(ws),
})
```

### 可移植的工作空间

> "Portable workspaces: clone, snapshot, and version your environment. Move agent runs between machines without restarting or reconfiguring the system."
> — [README](https://github.com/strukto-ai/mirage)

企业级特性——整个挂载状态可以打包传输：

```bash
# 快照
mirage workspace snapshot demo demo.tar

# 恢复
mirage workspace load demo.tar --id demo-restored
```

---

## 与 Code Execution with MCP 的主题关联

本文与 Anthropic 的 "Code execution with MCP" 文章形成了有趣的呼应：

**Code Execution with MCP 的核心思路**：
- 把「直接工具调用」变成「代码编程式调用」
- 按需加载工具定义，减少 98.7% token 消耗
- 中间结果留在执行环境，只把过滤后的结果传回 context

**Mirage 的核心思路**：
- 把「多服务 API 调用」变成「文件系统操作」
- 统一抽象层让 Agent 不需要学习每个服务的 API
- 工具行为由资源类型决定，Agent 只需要会用 bash

**两者共鸣之处**：
- 都解决「工具/服务数量增长带来的复杂性」问题
- 都通过「抽象层」把复杂性从 Agent 转移走
- Code execution 把复杂性留在执行环境（代码逻辑），Mirage 把复杂性留在配置层（挂载定义）

**笔者认为**：这是 Agent 工程化的两个方向——Code Execution 是「编程原语抽象」，Mirage 是「接口语义抽象」。前者让 Agent 学会写代码来调用工具，后者让 Agent 用统一的语义操作一切。

---

## 量化指标

| 指标 | 数值 |
|------|------|
| GitHub Stars | 2,599（2026-05-24，三周增长） |
| 增长趋势 | 快速上升，尚未进入稳定期 |
| 支持后端类型 | 15+ |
| SDK 语言 | Python + TypeScript |
| 最低 Python | 3.12 |
| 最低 Node.js | 20 |

---

## 适合的场景 vs 不适合的场景

**适合**：
- Agent 需要同时操作多个后端服务
- 希望用统一的 bash 风格操作一切
- 已在使用 OpenAI Agents SDK / LangChain / Vercel AI SDK

**不适合**：
- 只需要操作 1-2 个服务的简单场景
- 需要细粒度控制 API 调用参数
- Windows 原生环境（需要 WSL2 或类似方案）

---

**官方链接**：

- GitHub: https://github.com/strukto-ai/mirage
- 文档: https://docs.mirage.strukto.ai
- PyPI: https://pypi.org/project/mirage-ai/