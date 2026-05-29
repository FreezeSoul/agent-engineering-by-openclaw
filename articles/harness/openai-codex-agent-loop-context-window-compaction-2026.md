# OpenAI Codex Agent Loop 深度解析：Context Window 管理与 Compaction 机制

> 本文解读自 OpenAI 官方工程博客「Unrolling the Codex agent loop」，首次系统性公开 Codex CLI 的核心 agent loop 架构设计。
> 原文：https://openai.com/index/unrolling-the-codex-agent-loop/

---

## 核心命题

Codex CLI 的 agent loop 是目前公开资料中，对「如何正确实现一个生产级 Agent Loop」描述最完整的技术文档。

这不是一篇宣传文章。Bolinfest（Michael Bolin）从 Responses API 的视角，把整个推理链路拆开来讲：prompt 如何构建、inference 如何触发、tool call 如何闭环、context window 满了怎么办。文章读下来最强烈的感受是：**OpenAI 在这上面踩过的坑，比大多数团队知道的还多**——而他们把最重要的教训写在了这篇 blog 里。

---

## 一、Agent Loop 的本质：三个阶段 + 一个循环

Codex 官方把 agent loop 描述为三个阶段的循环：

```
用户输入 → 模型推理 → Tool Call 执行 → (循环) → 助手消息终止
```

### 1.1 用户输入（Prompt 构建）

Codex 的 prompt 不是一条字符串，而是一个「item list」——每条消息都是带 role 的结构化 item。Role 优先级：

| Role | 优先级 | 说明 |
|------|--------|------|
| system | 最高 | 模型基础指令 |
| developer | 高 | 开发者级指令，权重仅次于 system |
| user | 中 | 用户实际输入 |
| assistant | 最低 | 模型自己生成的回复 |

**这是一个容易被忽视的设计细节**：大多数 Agent 实现把 user 和 assistant 平等对待，但 Codex 的设计明确区分了优先级。这意味着越往后加入的内容权重越低——你永远不应该在一条 system 消息后面跟一个喧宾夺主的 user message。

### 1.2 模型推理（Inference）

Codex CLI 向 Responses API 发 HTTP 请求，送出构建好的 prompt list。API 返回模型生成的输出 token 序列（流式）。

> "In practice, inference is usually encapsulated behind an API that operates on text, abstracting away the details of tokenization."

这看起来是废话，但它是整个系统的隐含假设：**tokenization 是下沉到 API 的，Codex 本身不碰 token 边界**。这直接影响了后面 context window 的管理策略。

### 1.3 Tool Call 循环

模型输出有两种可能：

1. **最终响应**：直接回答用户，agent loop 终止
2. **Tool Call 请求**：Agent 执行工具（shell 命令、文件读写、MCP 调用），将结果 append 回 prompt，重新触发 inference

> "This process repeats until the model stops emitting tool calls and instead produces a message for the user (referred to as an assistant message in OpenAI models)."

这里有一个关键点：**每执行一次 tool call，context window 的输入就膨胀一次**。如果一个任务需要 100 次 tool call，即使每次 tool output 只有 100 tokens，累计就是 10,000 tokens 额外输入。这直接引出了 Codex 设计中最重要的工程挑战——context window 管理。

---

## 二、Context Window 管理：Compaction 机制

这是文章最硬核的部分。

### 2.1 问题：Context Window 会耗尽

每个模型都有 context window 上限（输入 + 输出 tokens 合计）。当对话历史累积到一定程度，prompt 长度会逼近甚至超过这个上限。

**传统解法：Stop-the-World Compaction**
- 暂停 agent
- 调用 LLM 对话历史做 summarization
- 用摘要替换历史
- 恢复 agent

**OpenAI 的判断：这是不必要的开销**。

### 2.2 Codex 的 Compaction 策略

Codex 使用自动 compaction，当 `auto_compact_limit` 超过阈值时触发。有两条技术路线：

**手动 compaction（早期实现）**：
- 用户手动调用 `/compact` 命令
- 触发 summarization + 重新送入 API
- 缺点：需要人工介入，破坏自动化体验

**自动 compaction（当前实现）**：
- Responses API 新增了 `/responses/compact` 端点
- Codex 自动调用，返回压缩后的 item list
- 压缩后的 item 包含一个 `type=compaction` 的特殊 item，里面有 `encrypted_content`——这是模型对原始对话的「隐式理解」

> "We’ve introduced the Codex agent loop and walked through how Codex crafts and manages its context when querying a model."

**encrypted_content 的意义**：不是简单的摘要，而是模型在压缩过程中保留的「潜在理解」。这比传统 summarization 的信息密度更高，因为摘要会丢失细微的语气、强调和推理路径。

### 2.3 为什么这个设计值得重视

大多数 Agent 框架的 compaction 就是「截断 + 总结」。Codex 的 compaction 端点设计意味着：压缩本身变成了一个被 API 认真对待的工程问题，而不是一个凑合的 workaround。

**这对 Harness Engineering 的启示**：当你设计一个长时运行的 Agent，必须把 compaction 视为一等公民，而不是事后补救。Cursor 的 Keep Rate 体系也是在解决这个问题——只不过 Cursor 从外部指标入手，Codex 从 API 层面入手。

---

## 三、三层输入体系：Instructions + Tools + Input

Codex 在发起第一次 inference 时，prompt 由三层构成：

### 3.1 Instructions（System Message）

`instructions` 字段对应 system 或 developer message。Codex 的策略是：

- 优先读取 `model_instructions_file`（`~/.codex/config.toml` 中的配置）
- 如果没有配置，使用模型关联的 `base_instructions`（bundled 在 CLI 中，如 `gpt-5.2-codex_prompt.md`）

> "Model-specific instructions live in the Codex repo and are bundled into the CLI."

这种设计让不同模型可以使用不同的 system prompt，而不依赖运行时注入。

### 3.2 Tools（Function Definitions）

`tools` 字段是模型可调用的工具列表。在 Codex 中包含三类：

**Codex 原生工具**：
```javascript
{
  "type": "function",
  "name": "shell",
  "description": "Runs a shell command and returns its output...",
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

**Responses API 提供的基础工具**（如 web_search）：
```javascript
{
  "type": "web_search",
  "external_web_access": false
}
```

**MCP 服务器提供的工具**（如天气查询）：
```javascript
{
  "type": "function",
  "name": "mcp__weather__get-forecast",
  "description": "Get weather alerts for a US state"
}
```

### 3.3 Input（Item List 构建顺序）

Codex 在 `input` 中依次插入以下内容：

1. **Permissions 消息**（role=developer）：描述沙箱权限、网络访问范围、可写目录列表
2. **Developer Instructions**（可选，role=developer）：来自 `config.toml` 的 `developer_instructions`
3. **User Instructions**（聚合自多源，role=user）：
   - `AGENTS.override.md` 和 `AGENTS.md`
   - 从 Git root 到 cwd 每一级目录中的 `AGENTS.md`
   - Skills 元数据和使用说明
4. **环境上下文**（role=user）：当前工作目录和 shell 类型
5. **用户实际消息**

**多层注入的巧思**：越具体的指令越往后放。这个顺序设计确保了高优先级的 system 消息不受干扰，同时允许项目级别的指令覆盖全局指令。

---

## 四、Thread / Turn / Item：三层会话原语

Codex App Server 的设计文档（`unlocking-the-codex-harness`）引入了三个核心原语，用于构建稳定的客户端-服务端交互：

| 原语 | 定义 | 生命周期 |
|------|------|---------|
| **Item** | 最小原子单元（user message / agent message / tool execution / approval request / diff） | `item/started` → `item/*/delta` → `item/completed` |
| **Turn** | 一次用户输入触发的完整 Agent 工作单元 | `turn/started` → 多 items → `turn/completed` |
| **Thread** | 持久化的会话容器，包含多个 Turn | 可创建 / 恢复 / 分叉 / 归档 |

> "A thread is the durable container for an ongoing Codex session between a user and an agent."

**这三个原语的分离，让多种客户端（VS Code 插件 / Web App / TUI）可以在同一套语义上构建 UI**，而不需要各自独立实现会话状态管理。这是 OpenAI 设计 App Server 协议的核心目标。

---

## 五、与 Cursor 的对比：一个从外部度量，一个从内部实现

Cursor 的「Continually improving our agent harness」和 OpenAI 的「Unrolling the Codex agent loop」是两篇高度互补的文章，它们解决的是同一个问题的两个不同层面：

| 维度 | Cursor | OpenAI Codex |
|------|--------|--------------|
| **核心问题** | 如何量化 Agent 进化质量？ | 如何正确实现 Agent Loop？ |
| **解决路径** | 三层测量体系（Keep Rate + 语义满意度 + A/B 测试）| Context Window 管理 + Compaction 机制 |
| **工程手段** | 外部指标驱动内部改进 | API 层面直接优化 |
| **关键指标** | Keep Rate（代码存活率）| Auto-compact 触发频率 |
| **典型场景** | 长期迭代的质量追踪 | 长对话的状态保持 |

**笔者的判断**：两者缺一不可。Cursor 给了一个成熟团队如何建立反馈闭环的范式；Codex 给了一个 Agent Loop 正确实现的技术细节。如果你正在设计一个 Harness 系统，这两篇文章应该一起读——Cursor 告诉你「测量什么」，Codex 告诉你「怎么实现」。

---

## 六、工程启示录

### 6.1 Compaction 不应该是补丁

大多数团队的 compaction 是这样加的：「对话太长就截断」，或者「手动加个 /compact 命令」。Codex 的做法是把 compaction 作为 API 的一等公民——这意味着 compaction 的质量直接影响模型在长任务中的表现。

**如果你在实现自己的 Agent**：请认真对待 compaction。不是简单的截断，而是信息保留最大化的问题。

### 6.2 Prompt 构建顺序有讲究

Codex 的五层 input 构建顺序（permissions → developer instructions → user instructions → environment → user message）不是随意排列的。这是他们踩过大量坑之后的产物。

**如果你在设计 Prompt 注入机制**：参考这个顺序，越具体的指令越往后放，但 system 级别的 guardrail 永远在最前。

### 6.3 Tool Call 的成本被低估了

Codex 明确指出：每次 tool call 的输出都会累积到 context。100 次 tool call 即使每次只有 100 tokens，也是 10,000 tokens 的额外 context。

**实践建议**：对于高频 tool call 的场景，考虑：
- 在 tool 输出端做轻量过滤（只保留关键字段）
- 使用流式 API 实时处理 tool output，而不是等累积后再处理
- 设计 tool call 的预算机制（类似 SiluPanda/codex-agent-loop 的 turn-based bounded loop）

---

## 参考文献

1. Michael Bolin, "Unrolling the Codex agent loop", OpenAI Engineering Blog, January 23, 2026 — https://openai.com/index/unrolling-the-codex-agent-loop/
2. Celia Chen, "Unlocking the Codex harness: how we built the App Server", OpenAI Engineering Blog, February 4, 2026 — https://openai.com/index/unlocking-the-codex-harness/
3. SiluPanda/codex-agent-loop — Bounded, resumable Claude-Code-style coding loops for Codex — https://github.com/SiluPanda/codex-agent-loop
4. marklubin/hopping-context-windows — Seamless Context Continuity at Zero Incremental Inference Cost — https://github.com/marklubin/hopping-context-windows
5. Cursor Engineering, "Continually improving our agent harness", Cursor Blog, April 30, 2026