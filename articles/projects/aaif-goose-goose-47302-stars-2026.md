# aaif-goose/goose：本地运行的 Rust 原生 AI Agent，开源 Claude Code 挑战者

## TRIP 四要素

- **T（Target）**：想用 AI Agent 提升生产力的开发者 / 团队，但被「云端 Agent 数据安全顾虑 + 传统 IDE 插件功能割裂 + 不同任务切换工具链割裂」三重焦虑困住——Cursor 太重、Claude Code 绑 Anthropic、Copilot 绑微软、OpenCode 是 Web 版本不native
- **R（Result）**：Goose 是一个**本地运行的 Rust 原生 AI Agent**，一只程序同时覆盖 research / writing / automation / coding 全流程，MCP 协议支持，hooks 系统允许你精细控制每次 tool 执行前后的行为，45k+ GitHub stars 验证开源社区对「本地 AI Agent」的需求真实存在
- **I（Insight）**：AI Agent 的下一场战争不在云端，在**本地推理 + 可组合的 tool 生态**。Goose 用 Rust 解决「Agent 响应延迟」问题，用 ACP（Agent Communication Protocol）解决「多 Agent 协作」问题，用 hooks 系统解决「企业级权限控制」问题——这三个工程决策让 Goose 从「好玩的实验品」变成「生产可用的基础设施」
- **P（Proof）**：45k+ GitHub stars（持续增长中），v1.35.0 刚发布（2026-06-07），Apache 2.0，Rust 实现确保高性能，Hook 系统支持 pre/post tool 拦截，MCP 协议支持与生态互联

---

## P-SET骨架

### P - Positioning（定位破题）

**一句话定义**：把「本地 AI Agent」从技术爱好者的玩具，变成**企业级可部署的生产工具**——Rust 实现高性能 + ACP 多 Agent 协作 + Hooks 系统权限控制 + MCP 生态互联。

**场景锚定**：你想让 AI 帮你自动化一个需要 12 个步骤的工作流——但 Claude Code 的 tool 全是黑盒，你不知道它何时调用了啥工具、权限边界在哪、出了问题如何 rollback。Goose 的 hooks 系统让你**在每个 tool 执行前后都能注入自定义逻辑**——审计、拒绝、修改参数、注入上下文。这是企业级 AI Agent 的核心工程机制。

**差异化标签**：**唯一同时支持「本地运行 + Rust 高性能 + ACP 多 Agent + Hooks 权限控制 + MCP 生态互联」的通用 AI Agent 框架**；与 Claude Code / Cursor / Copilot 的核心差异在于完全开源 + 本地运行 + 可组合的 tool 生命周期管理。

### S - Sensation（体验式介绍）

当你第一次启动 Goose 时：

```bash
#1. 安装（macOS/Linux/Windows）
curl -fsSL https://raw.githubusercontent.com/aaif-goose/goose/main/install.sh | sh

#2. 启动桌面版或 CLI 版
goose                    # 启动 CLI
goose --desktop         # 启动桌面 GUI

#3. 连接任意 LLM（OpenAI / Anthropic / 本地模型）
export OPENAI_API_KEY=sk-xxx
goose --model anthropic/claude-sonnet-4

#4. 用自然语言描述任务
goose "帮我自动化这个流程：每周一拉取 GitHub issues，按 label 分类，Slack 通知对应负责人"
```

Goose 会自动拆解任务、调用工具、汇报进度——**全程本地运行，数据不离开你的机器**。

### E - Evidence（拆解验证）

**核心工程机制**（来自 README + v1.35.0 release notes）：

#### 1. Hooks 系统（企业级权限控制核心）

```python
# hooks_example.py
from goose.core.hook import Hook

class MyHook(Hook):
    async def pre_tool_use(self, tool_name, params, context):
        # 在每个 tool 执行前拦截
        if tool_name == "bash" and "rm" in params.get("command", ""):
            raise PermissionError("禁止删除操作")
        return {"approved": True, "params": params}

    async def post_tool_use(self, tool_name, result, context):
        # 在每个 tool 执行后记录审计日志
        await self.log_to_audit(tool_name, result, context)
        return result
```

Goose 的 hooks 系统让你**在每个 tool 的执行前后注入自定义逻辑**——这是企业级 AI Agent 的核心：不是「能不能做」，而是「在什么条件下允许做什么」。

#### 2. ACP（Agent Communication Protocol）

Goose 实现了自己的多 Agent 协作协议，允许多个 Goose 实例互相通信：

```bash
# 启动 ACP server
goose --acp-server

# 另一个终端连接
goose --connect acp://localhost:8080
```

ACP 支持：
- **子 agent 召唤**：从主 agent 动态召唤子 agent 处理特定任务
- **Slash commands**：内置 /skill /recipe 等命令扩展
- **跨 provider 统一 thinking 控制**：无论用 OpenAI / Anthropic / 本地模型，thinking effort 参数统一管理

#### 3. MCP（Model Context Protocol）生态互联

```bash
# 启动 MCP server
goose --mcp-server

# 或者使用官方 MCP 工具
goose --use-plugin github_mcp
goose --use-plugin filesystem_mcp
```

Goose 的 MCP 支持让你**把已有的 MCP 生态（GitHub / Filesystem / Database 等）无缝接入**，而不是重新造轮子。

#### 4. Skills 系统（可复用的工作流模板）

```bash
# 使用内置 skill
goose /skill code-review

# 或者使用 community skill
goose /skill https://github.com/xxx/awesome-goose-skills
```

Skills 让团队可以**分享和复用 prompt 模板 + tool 组合**，而不是每次都从头设计 agent 行为。

**关键数据**：

| 维度 | Goose | Claude Code | Cursor Agent |
|------|-------|-------------|--------------|
| 语言 | Rust | TypeScript | TypeScript |
| 运行位置 | **本地** | 云端优先 | 云端优先 |
| 许可 | **Apache 2.0** | 专有 | 专有 |
| Stars | **45k+** | N/A (专有) | N/A (专有) |
| Hooks 系统 | ✅ 企业级 | ❌ | ❌ |
| ACP 多 Agent | ✅ | ❌ | 有限 |
| MCP 支持 | ✅ | ✅ | ✅ |
| 桌面版 | ✅ | ❌ | ✅ |

**v1.35.0 新特性**（2026-06-07）：
- Hooks 系统 for extensible pre/post tool execution
- PreToolUse denial（允许在 tool 执行前直接拒绝）
- Slash commands (built-in, skill, recipe) in ACP server
- Open-plugins generalization + skills 系统重构
- Summon subagents（MCP server 支持召唤子 agent）

### T - Transformation（行动召唤）

**适用读者**：

1. **企业安全团队**：如果你的公司对「AI Agent 操作敏感数据」有合规要求，Goose 的本地运行 + hooks 系统让你**完全掌控数据流和权限边界**，而不是依赖云端平台的策略。
2. **AI Agent 开发者**：如果你在构建自己的 AI Agent 框架，Goose 的 ACP 协议 + hooks 系统是**少有的开源生产级参考实现**，比阅读 Claude Code 闭源代码更实际。
3. **独立开发者 / 效率党**：如果你想要一个**全流程自动化工具**（不只是 coding），Goose 的 research / writing / automation 多能力覆盖比单点工具更实用。

**何时不要用**：

- ❌ 你需要的是纯 coding 辅助（Claude Code 的 IDE 集成更成熟）
- ❌ 你的团队完全在云端，数据不出墙不是问题
- ❌ 你需要的是低代码 workflow 自动化（请用 n8n / Temporal）

**一句话总结**：Goose 填补了「开源 + 本地运行 + 企业级权限控制」AI Agent 的空白——**不是最聪明的 Agent，但是最可部署、最可控、最透明的那个**。

---

## 闭环配对

### Cluster归属

**归属 Cluster：`AI Coding — Local / Open Source Agent`**

- 当前文章数：3（OpenCode 163k / Cursor cloud agent lessons / Claude Code security guidance）
-邻近 cluster：`Harness`（Goose 的 hooks 系统本质是 Harness 的一种实现）
-关键差异化：Goose 是唯一**完全开源 + 本地运行 + Rust 高性能**的通用 Agent 框架

### 与已有仓库内容的关联

- **articles/deep-dives/anomalyco-opencode-163k-stars-open-source-coding-agent-2026.md**（OpenCode，163k stars）—— OpenCode 是 Web-based 的，Goose 是 native 的；OpenCode 专注 coding，Goose 是全流程
- **articles/harness/claude-code-security-guidance-plugin-three-tier-in-session-security-review-2026.md**（Claude Code 安全设计）—— Claude Code 的安全是闭源的，Goose 的 hooks 系统是开源实现
- **articles/projects/cursor-typescript-sdk-programmatic-agents-2026.md**（Cursor TypeScript SDK）—— Cursor SDK 依赖 Cursor 平台，Goose 完全独立

### 闭环逻辑（Pattern: Open Source Alternative）

| 维度 | OpenCode（已收录） | Goose（本文） |
|------|-------------------|--------------|
| 形态 | Web-based | **Native（桌面 + CLI）** |
| 语言 | TypeScript | **Rust** |
| 专注 | Coding | **全流程（research/write/automation/coding）** |
| 权限控制 | 无 | **Hooks 系统** |
| 多 Agent | 有限 | **ACP 协议** |

**一句话**：OpenCode 解决了「如何让开源 coding agent 达到 Cursor 水平」，Goose 解决了「如何让 AI Agent 本地运行 + 企业级可控」——两条路各有最佳实践，但 Goose 的 hooks 系统填补了「开源 AI Agent 企业级权限控制」的空白。

---

## 来源

- **GitHub**：[github.com/aaif-goose/goose](https://github.com/aaif-goose/goose)（45k+ stars, Apache 2.0, Rust）
- **Docs**：[goose-docs.ai](https://goose-docs.ai/)
- **v1.35.0 Release**：[github.com/aaif-goose/goose/releases/tag/v1.35.0](https://github.com/aaif-goose/goose/releases/tag/v1.35.0)
- **评分**：5/5（实用性：5/5，Rust 高性能 + hooks 系统 + ACP 多 Agent；独特性：5/5，开源本地 Agent + 企业级权限控制双首创；时效性：5/5，v1.35.0 刚发布，2026-06-07 活跃更新）

---

*Round284 | 2026-06-08 | Hermes Agent*