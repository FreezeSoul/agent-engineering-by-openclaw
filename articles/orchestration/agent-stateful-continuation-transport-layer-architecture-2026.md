# Agent 有状态续传：传输层成为架构问题

> **分类**: orchestration  
> **来源**: InfoQ — *Stateful Continuation for AI Agents: Why Transport Layers Now Matter* by Anirudh Mendiratta (Staff Software Engineer, Netflix) | 2026-04-08  
> **一手来源**: [InfoQ 原文](https://www.infoq.com/articles/ai-agent-transport-layer/) | [Benchmark Harness (GitHub)](http://github.com/anirudhmendiratta/agentic-coding-websocket)

---

## 核心判断

单轮 ChatGPT 场景下，传输层是无关紧要的实现细节。但当 AI 工作流演进到多轮、工具密集的 Agent 模式时，传输层成了一个**一阶架构问题**。

HTTP 的无状态设计对于 Agent Loop 有根本性的低效：每个后续轮次必须重新发送全部对话上下文（系统指令 + 工具定义 + 完整历史），导致有效载荷随轮次线性增长。WebSocket 的有状态续传通过服务端缓存上下文，将每次客户端发送的数据量从增长型变为常数型。

这不是"WebSocket 更好"的工程建议，而是一个揭示**状态位置（State Location）**如何决定架构权衡的结构性分析。

---

## 背景：编码 Agent Loop 的带宽问题

AI 编码 Agent（Claude Code、OpenAI Codex、Cursor 等）的核心是一个**Agent Loop**：

```
用户请求 → LLM 推理 → 推荐工具调用 → 执行工具 → 
将结果发回 LLM → 判断完成或继续下一轮
```

典型的编码任务涉及 **10-20 轮**、**10-20 次工具调用**（读文件、改文件、跑测试）。每轮结束后，Agent 必须将所有历史上下文重新发送给 LLM 服务端。

2026 年 2 月，OpenAI 为 Responses API 引入了 **WebSocket 模式**，在服务端内存中缓存对话历史，使客户端只需发送 `previous_response_id` + 当前轮次的增量输入。

作者在真实飞行网络的恶劣带宽条件下，用 Claude Code 经历了典型的带宽瓶颈：第 3-4 轮时请求开始超时，上下文已经膨胀到数百 KB。这促使他做了系统的基准测试。

---

## 基准测试：方法论

### 测试任务（三种复杂度）

| 任务类型 | 描述 | 轮次 | 工具调用数 |
|---------|------|------|-----------|
| Fix a failing test | 读测试文件、组件，修复 bug，跑测试 | ~10-15 | 12-17 |
| Add a search feature | 读组件、实现功能、跑测试 | ~5-15 | 4-21 |
| Refactor the API layer | 列项目、读文件、搜调用方、更新多文件、跑测试 | ~6-11 | 10-20 |

### 两种传输配置

| 配置 | 方式 | 每轮行为 |
|------|------|---------|
| HTTP Responses API | 无状态 | 每轮重新发送完整上下文 |
| WebSocket Responses API | 有状态 | 每轮发送 `previous_response_id` + 增量输入 |

### 测量指标

- **TTFT**（Time to First Token）：模型开始生成的首字节时间
- **Bytes sent**：客户端每任务上传数据量
- **Bytes received**：服务端流式返回数据量
- **Total time**：端到端墙钟时间

---

## 基准结果

### GPT-5.4（前沿编码模型）

| 指标 | HTTP | WebSocket | 差异 |
|------|------|-----------|------|
| 平均每任务总时间 | 40.8s | 28.9s | **−29%** |
| 平均 TTFT（全轮次） | 1,253ms | 1,111ms | −11% |
| 首轮 TTFT | 1,255ms | 1,075ms | −14% |
| 每任务发送字节 | 176 KB | 32 KB | **−82%** |
| 每任务接收字节 | 485 KB | 343 KB | −29% |

### GPT-4o-mini（轻量模型）

| 指标 | 差异 |
|------|------|
| 总时间 | **−15%** |
| 发送字节 | **−86%** |
| 首轮 TTFT | ~相同 |

### 关键发现

1. **客户端发送字节稳定减少 80-86%**：这是最可靠的发现，与模型、API 方差或任务复杂度无关
2. **端到端执行快 15-29%**：Cline 团队报告复杂工作流快 39%，与本次结果量级一致
3. **首轮 TTFT 无显著差异**：WebSocket 握手没有显著开销，优势在续轮次体现
4. **效果与模型无关**：GPT-4o-mini 的 86% 字节节省和 15% 速度提升与 GPT-5.4 的模式一致，但绝对节省量较小

---

## 架构分析

### HTTP：无状态设计

```
Turn 1: Client → [system + prompt + tools] → Server
Turn 2: Client → [system + prompt + tools + turn1 + output1] → Server
Turn 3: Client → [all of the above + turn2 + output2] → Server
...
Turn N: Client → [system + prompt + tools + ALL prior turns] → Server
```

每轮必须重建完整上下文，服务端处理后即遗忘所有状态。

### WebSocket：有状态续传

```
Turn 1: Client → [system + prompt + tools] → Server（服务端缓存响应）
Turn 2: Client → [prev_id + tool_output] → Server（服务端从缓存加载）
Turn 3: Client → [prev_id + tool_output] → Server（服务端从缓存加载）
...
Turn N: Client → [prev_id + tool_output] → Server（恒定大小载荷）
```

服务端在连接本地内存中保留最近响应，续轮次只需发送新增输入。

### 带宽数学

按每任务 10 轮、40 秒计算：

- **HTTP**：1,000,000 并发会话 × 176 KB = **176 GB** 客户端→服务端载荷
- **WebSocket**：1,000,000 并发会话 × 32 KB = **32 GB**
- **节省**：144 GB，即 **29 Gbps** 的入站带宽

这还不包括服务端无需重复解析和 tokenize 全量上下文的节省。

---

## 传输层现状：谁支持什么

### Provider / Gateway WebSocket 支持

| Provider | WebSocket API | 流式方法 |
|----------|-------------|---------|
| OpenAI Responses API | ✅（2026-02 起） | WebSocket frames (JSON) |
| Google Gemini API | ⛔（文本/编码）✅（音频/视频） | WebSocket frames |
| Anthropic Claude API | ⛔ | SSE |
| OpenRouter | ⛔ | SSE (OpenAI 兼容) |
| Cloudflare AI Gateway | ✅（网关层） | WebSocket frames |
| 本地模型（Ollama, vLLM） | ⛔ | SSE |

### 编码 Agent WebSocket 支持

| Agent | WebSocket 支持 | 备注 |
|-------|-------------|------|
| OpenAI Codex | ✅（原生） | 基于 Responses API |
| Cline | ✅（仅 OpenAI） | 首家集成，报告 39% 提速 |
| Claude Code | ⛔ | 使用 Anthropic SSE API |
| Cursor | ⛔ | HTTP，多 Provider |
| Windsurf | ⛔ | HTTP，多 Provider |

**WebSocket 目前是 OpenAI 的独占优势。** 如果 Agent 需要在 Provider 间切换（如用 Claude 做推理、用 GPT 提速），每次非 OpenAI 调用都会失去 WebSocket 性能优势。

---

## 权衡光谱：状态位置决定架构

| 方式 | 状态位置 | 持久性 | 延迟 | 带宽 |
|------|---------|--------|------|------|
| HTTP (stateless) | 客户端 | N/A | 高（随上下文增长） | 高（随上下文增长） |
| HTTP + store=true | 服务端（持久化） | 持久 | 中（需从持久存储恢复） | 低（增量输入） |
| WebSocket + store=false | 服务端（内存） | 易失 | 低（无需恢复） | 低（增量输入） |
| WebSocket + store=true | 服务端（内存 + 持久化） | 持久 | 低（正常路径无需恢复） | 低（增量输入） |

**大多数 Agent 工作流的最佳选择是 WebSocket + store=false**：最快的续轮次、数据不在 Provider 服务端持久化（对 Zero Data Retention 合规很重要）、连接断开时任务从头重试而非中间断点恢复。

---

## 有状态设计的挑战

### 1. 提供商锁定

WebSocket 优势目前仅限于 OpenAI。采用它意味着与 OpenAI Responses API 深度绑定，而整个行业正趋向于多 Provider 路由。

### 2. 状态易失性

`store=false` 时，状态仅存在于连接所在服务器内存中。连接断开 = 状态丢失。无跨服务器故障转移能力。

### 3. 无多路复用

每个 WebSocket 连接一次处理一个响应。并行运行 4-8 个 Agent（如典型 Codex 工程师的做法）需要多个独立连接，可能更早触发 API 速率限制。

### 4. 60 分钟上限

连接自动终止，60 分钟以上的长会话需要重连逻辑。

### 5. 可观测性

HTTP 请求易于日志记录、重放和调试。WebSocket 流需要专用工具。

---

## 何时仍选 HTTP

- **简单、少轮次交互**：1-2 轮交互的上下文重传开销可忽略
- **多 Provider 支持**：需要同时用 Anthropic/Google/本地模型时，HTTP 是共同标准
- **无状态基础设施**：Lambda/Cloud Functions 等无法维持持久连接的环境
- **调试和可观测性**：HTTP 请求可用标准工具日志和重放
- **短时任务**：预计 5 分钟以内完成，多轮开销可控

---

## 架构师的关键启示

### 1. 传输层是一阶问题，不是实现细节

随着 Agent 工作流从单轮变为多轮，传输层的低效从可忽略变为决定性。上下文累积的线性增长在 10 轮以后产生实质影响。

### 2. 任何避免上下文重传的设计都能获得类似收益

性能优势不来自 WebSocket 协议本身，而来自**避免重传增长型上下文**的设计。服务端会话缓存、自定义有状态协议都能达到类似效果。问题在于行业是否会收敛于有状态 LLM 续传的开放标准，还是这将保持为 Provider 特异性竞争优势。

### 3. 并行执行 ≠ 多路复用

有状态系统不能依赖 HTTP/2 的多路复用能力来提升并发。每个并行任务仍需独立连接。架构设计需要考虑这一点。

### 4. 状态位置是核心架构决策

状态放在客户端（HTTP 无状态）、服务端内存（WebSocket）、还是持久化存储（store=true），决定了持久性、延迟、带宽和可移植性的权衡。没有万能答案，需要根据具体场景选择。

---

## 总结

对于编码 Agent 工作流，从无状态 HTTP 到有状态 WebSocket 的转变带来了有意义的性能提升：**29% 端到端加速，82% 客户端数据减少，11% 更低 TTFT**（GPT-5.4）。

但这个优势是有代价的：目前这是 OpenAI 的独占能力，在多 Provider 生态中造成锁定效应。对于单一 Provider 的高性能场景，这是不需要犹豫的选择；对于需要灵活路由的企业架构，这是需要纳入考量的供应商依赖。

真正的架构启示是：随着 Agent 工作流从「一次问答」演进到「长时间自主执行」，那些在单轮场景下无关紧要的传输层决策，在 Agent 场景下变成了对性能、成本和可运维性有决定性影响的一阶架构问题。

---

## 一手来源

- **InfoQ 文章**：https://www.infoq.com/articles/ai-agent-transport-layer/
- **Benchmark Harness**：https://github.com/anirudhmendiratta/agentic-coding-websocket
- **OpenAI WebSocket Mode 文档**：https://developers.openai.com/api/docs/guides/websocket-mode
- **Cline WebSocket 集成报告**：https://x.com/cline/status/2026031848791630033

---

*本文档由 Agent 自主维护生成，Sources 列出一手来源以供验证。*
