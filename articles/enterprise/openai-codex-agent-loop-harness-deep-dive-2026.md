# OpenAI Codex Agent Loop 深度解析：从 Prompt 构建到上下文管理的完整工程路径

**核心论点**：Codex 的文档揭示了一个长期以来被忽视的事实——**Agent 的能力瓶颈不在模型，而在 Harness（工具链管理层）**。Codex CLI 通过对 prompt 构建、工具执行、上下文窗口管理、会话压缩的精确控制，将模型能力稳定地转化为可预测的软件工程成果。这是目前公开资料中关于 Agent Harness 工程细节最完整的文档。

## 一、为什么这个文档值得细读

Michael Bolin（OpenAI 技术Staff）在博客中写道：

> "We hope this post gives you a good view into the role our agent (or "harness") plays in making use of an LLM."

这里的 **"harness"** 用词值得注意。在 AI Agent 语境中，harness 通常指「把 LLM 包装成可用 Agent 的那一层工程代码」——它负责决定 Agent 看到什么、可以做什么、什么时候终止。

大多数 Agent 框架（LangChain、HuggingFace Agents 等）将 harness 作为内部实现细节，不对外解释。Codex 选择反其道而行：**开源 harness 代码 + 配套文档，让外部工程师理解他们做了什么、为什么这样做**。

这篇文档的工程细节密度，在同类公开资料中无出其右。

## 二、Agent Loop 的基础模型

Codex 文档给出的 Agent Loop 基础模型：

```
User Input → Build Prompt → Model Inference → 
  ├─ Assistant Message（终止）→ 返回用户
  └─ Tool Call → Execute → Append Output → 重新 Build Prompt
```

这与业界普遍的 Agent Loop 认知一致。但 Codex 的价值不在于这张图，而在于**它揭示了图背后的每一个工程决策**。

### 2.1 模型推理的 HTTP 请求架构

Codex CLI 使用 OpenAI 的 **Responses API** 驱动 agent loop，有三种接入路径：

```python
# 1. ChatGPT 登录态
endpoint = "https://chatgpt.com/backend-api/codex/responses"

# 2. API Key 认证（OpenAI Hosted Models）
endpoint = "https://api.openai.com/v1/responses"

# 3. --oss 模式（本地模型）
# 使用 gpt-oss + ollama 0.13.4+ 或 LM Studio 0.3.39+
endpoint = "http://localhost:11434/v1/responses"
```

这里的工程价值：**Codex CLI 是少数明确支持 ZDR（Zero Data Retention）配置的 Agent 工具**——企业用户可以在本地跑模型，完全不上传数据。这是当前 AI Coding 工具中罕见的选项。

## 三、Prompt 构建的精确分层

这是文档最核心的部分。Codex 在发送第一次 inference 请求前，会按顺序向 `input` 数组插入以下内容：

### 3.1 层级结构（按优先级递减）

| 顺序 | Role | 内容来源 | 说明 |
|------|------|---------|------|
| 1 | `developer` | Codex 内置的 sandbox 描述模板 | 仅限 Codex 自己提供的 shell tool，MCP 服务器提供的工具不受 Codex sandbox 保护 |
| 2 | `developer` | `config.toml` 中的 `developer_instructions` | 用户自定义的开发者级指令 |
| 3 | `user` | `AGENTS.override.md` / `AGENTS.md` | 项目级指令文件 |
| 4 | `user` | 从 Git 根目录到 cwd 的路径上各文件夹的 `AGENTS.md` | 目录级指令 |
| 5 | `user` | Skills 索引 + preamble | 用户配置的 Skills 元数据 |
| 6 | `user` | 用户实际输入的消息 | 真实的用户请求 |

### 3.2 三个关键设计决策

**① sandbox 描述是 Codex 特有的**  
Codex 插入的 `developer` 消息来自内置 Markdown 模板（如 `workspace_write.md`、`on_request.md`），描述的是 **Codex 自己提供的 shell tool 的沙盒配置**。这意味着：

> ⚠️ MCP 服务器提供的工具不受 Codex 的 sandbox 保护——它们需要自己实现 guardrail。这是容易被忽视的安全边界。

**② 目录层级递增覆盖（More specific instructions appear later）**  
`AGENTS.md` 的查找路径从 Git 根目录向上到 cwd，每层都可以覆盖上层指令。越接近 cwd 的指令优先级越高。这实现了：

- 团队共享的 `AGENTS.md` 放在仓库根目录
- 个人偏好放在 `$CODEX_HOME/AGENTS.override.md`
- 项目特定规则放在子目录的 `AGENTS.md`

**③ Skills 的 preamble + metadata 模式**  
Skills 的内容不是直接展开，而是注入：
1. 一段关于如何使用 Skills 的 preamble
2. 每个 Skill 的 metadata（不是完整内容，让模型按需加载）

这避免了一次性把大量 Skill 内容注入 context window——模型在需要时通过 metadata 索引去动态使用。

## 四、上下文窗口管理的工程挑战

### 4.1 二次方增长问题

Codex 文档指出了一个所有 Agent 都会遇到的数学问题：

> "Wait, isn't the agent loop quadratic in terms of the amount of JSON sent to the Responses API over the course of the conversation?" And you would be right.

每轮对话包含之前的完整 history。随着对话增长，发送的 JSON 呈二次方增长。这是因为 **每次 re-query 时，旧的 prompt 必须作为新 prompt 的前缀**（exact prefix）：

```
Turn 1: [system] + [developer] + [user: msg1] → [assistant: reply1]
Turn 2: [Turn1 的全部内容] + [user: msg2] → [assistant: reply2]
Turn 3: [Turn2 的全部内容] + [user: msg3] → ...
```

### 4.2 Prompt Caching 的精确条件

Codex 用 **prompt caching** 缓解二次方问题。但 cache hit 的条件极为严格——**必须是 exact prefix match**。任何以下变化都会导致 cache miss：

| 操作 | 是否 cache miss |
|------|----------------|
| 改变工具列表顺序 | ✅ miss |
| 切换目标模型 | ✅ miss |
| 切换 sandbox 配置 | ✅ miss |
| 切换 approval mode | ✅ miss |
| 切换当前工作目录 | ✅ miss |
| MCP 服务器动态增删工具 | ✅ miss |

**MCP 的工具动态变更** 是一个特别棘手的问题。MCP 规范支持 `notifications/tools/list_changed`——服务器可以在会话过程中通知客户端工具列表已变化。Codex 承认这个问题：

> "MCP tools can be particularly tricky because MCP servers can change the list of tools they provide on the fly... Honoring this notification in the middle of a long conversation can cause an expensive cache miss."

Codex 的应对方式：**不在中途更新工具列表，而是通过追加新消息来反映配置变化**。如果 sandbox 配置或 approval mode 变化，插入一条新的 `role=developer` 消息；如果 cwd 变化，插入一条新的 `role=user` 消息。这样保持前缀不变，避免 cache miss。

### 4.3 Compaction：从手动到自动

当 token 数量超过阈值，Codex 需要压缩对话历史。演进路径：

**第一阶段（早期）**：用户手动调用 `/compact` 命令
```bash
# 用户手动触发
/compact
# Codex 用 summarization instructions 查询 Responses API
# 返回的 summary 作为新的 input
```

**第二阶段（现在）**：Responses API 的 `/responses/compact` endpoint
```python
# 自动 compaction，返回可替代原 input 的压缩后的 items 列表
POST /responses/compact
# 返回: { items: [...] } 可直接用于后续请求
```

这背后的工程逻辑：**compaction 应该由服务端处理，而非客户端手动调用**。服务端知道模型对压缩内容的偏好，客户端只需要发起请求。

## 五、Zero Data Retention 的架构取舍

这是文档中最有价值但最容易被忽视的部分。Codex 选择**不使用 `previous_response_id`** 来维护会话状态，核心原因是支持 ZDR 配置：

```python
# Codex 不使用 previous_response_id
# 因为如果使用它，服务端必须存储会话数据
# 这与 ZDR（Zero Data Retention）配置冲突
```

ZDR 的代价：**每次请求必须发送完整的历史上下文**，无法利用服务端存储的会话状态。即使模型有 encrypted reasoning messages from prior turns，服务端可以解密 key 但不存储数据。

OpenAI 的做法：
- 服务端**不**存储 ZDR 用户的会话数据
- 但保留用于解密之前 reasoning messages 的 key
- 这使得 ZDR 用户仍然能从之前轮次的 thinking 中受益，同时满足不上传数据的要求

## 六、与 Rippling 案例的关联：Harness 的企业价值

回到本轮 R250 的 Article 分析。Rippling 的案例展示了**另一类企业级 harness 设计**：

| 维度 | Codex CLI | Rippling AI |
|------|-----------|-------------|
| **核心 harness 机制** | Prompt 构建分层 + 上下文压缩 | Multi-agent Supervisor + Dynamic Skill Injection |
| **上下文管理策略** | Prompt Caching + Compaction | 动态 Skill 注入（按 domain 注入对应 Skill，压缩 100-500x）|
| **工具安全** | Sandbox（Codex 原生）+ Guardrail（MCP 自维护）| 代码执行沙盒（Action Agents）|
| **会话持久化** | ZDR 兼容（不上传数据）| LangSmith（商业平台，持久化 trace）|
| **可观测性** | 本地 trace（Codex CLI）| LangSmith 完整 trace 聚合 + 分层 Eval |

两者都在解决同一个根本问题：**如何让 LLM 在长会话中保持稳定、可预测的行为**。但各自的解决方案反映了不同的工程取舍：

- **Codex** 选择让用户完全控制数据（ZDR + 本地），代价是每次请求的 overhead
- **Rippling** 选择商业平台换取托管便利，代价是数据上云

这是 Agent 工程中经典的 **控制 vs 便利** 取舍，没有标准答案。

## 七、工程实践启示

### 7.1 Prompt 构建的分层设计值得直接借鉴

Codex 的 `AGENTS.md` 目录层级查找模式是一个可复用的设计：

```text
project-root/
├── AGENTS.md          # 仓库级指令（团队共享）
├── frontend/
│   └── AGENTS.md      # 前端特定规则（覆盖上层）
└── backend/
    └── AGENTS.md      # 后端特定规则（覆盖上层）
```

这种模式可以迁移到任何使用 Agent 的团队：**分层指令文件 + 最近路径优先覆盖**。

### 7.2 MCP 工具的动态变更需要显式处理

如果你的 Agent 系统接入了 MCP 服务器，必须意识到：

1. **MCP 工具列表可能在中途变化**（`tools/list_changed` notification）
2. **变化会导致 prompt cache miss**（Codex 遇到的实际 bug）
3. **正确的处理方式**：不要在中间更新工具列表，而是通过追加消息来反映变化

### 7.3 Compaction 是长会话 Agent 的必经之路

当对话超过 50 轮时，context window 管理会成为主要瓶颈。两种策略：

1. **手动 compaction**：定期触发 summarization，人工确认质量
2. **自动 compaction**（推荐）：交给 Responses API 的 `/responses/compact` 处理

如果你的 Agent 框架不支持 compaction，你需要自己实现类似机制：**当 token 数量超过阈值（如 32K），触发压缩流程，用压缩后的 summary 替换原始 history**。

### 7.4 ZDR 场景下的架构选择

如果你的 Agent 场景有严格的隐私要求（代码不上云），Codex 的 `--oss` 模式提供了一个参考架构：

```
用户机器
├── Codex CLI（本地 agent loop）
├── ollama 0.13.4+ / LM Studio 0.3.39+
└── gpt-oss（本地模型）
    └── localhost:11434/v1/responses
```

但代价是失去 prompt caching 的服务端优化能力和商业平台的可观测性。这需要在 Privacy 和 Capability 之间做明确权衡。

## 结语

Codex 的这篇文档之所以值得读，不是因为它介绍了一个 Agent Loop（这是业界常识），而是因为它**揭示了 Agent Loop 背后的每一个工程决策的 trade-off**：

- Prompt 为什么要分层（优先级控制）
- 为什么不能随意改变工具列表（prompt caching 依赖 exact prefix）
- 为什么 compaction 必须自动化（手动操作的不可扩展性）
- 为什么 ZDR 和高效会话管理不能兼得（架构取舍）

这些是**只有亲自解决过这些问题的人才能写出来**的经验。OpenAI 选择开源 harness 代码，让这些经验可以被审查和改进——这是我认为这篇文档最重要的意义。

> "There are detailed graphics that help visualize the loop and technical details about context management. This post is required reading for any engineer using coding agents as it explains the core loop of all agents."
> — via The Pragmatic Engineer

---

**引用来源**：
1. "Unrolling the Codex agent loop" — Michael Bolin, OpenAI Engineering Blog, https://openai.com/index/unrolling-the-codex-agent-loop/
2. Codex OSS Repository — https://github.com/openai/codex
3. Prompt Caching Documentation — https://platform.openai.com/docs/guides/prompt-caching
4. Responses API Compact Endpoint — https://platform.openai.com/docs/guides/conversation-state#compaction-advanced