# codexpro：ChatGPT 本地编码 Agent 桥接（844 Stars）

> **来源**：[rebel0789/codexpro](https://github.com/rebel0789/codexpro)（GitHub，2026-06-16）
> **Cluster**：Local Agent Bridge / ChatGPT Apps SDK / MCP / Codex 生态扩展
> **关联 Article**：[OpenAI TanStack 事件：签名链失陷与 macOS 强制升级机制](../security/openai-tanstack-npm-supply-chain-attack-response-macOS-forced-update-2026.md) — ChatGPT 本地化扩展生态的供应链风险
> **许可证**：MIT

## 一句话定位

`rebel0789/codexpro` 是一个把 ChatGPT Plus/Pro 的 **Developer Mode + MCP 通道**包装成本地编码 Agent CLI 的桥接工具——你 `npm install -g codexpro` + `codexpro setup` 一次，之后在任意 git repo 里跑 `codexpro start`，就能让同一个 ChatGPT 账号在云端 UI 里"长出"对本地仓库的文件读写、git 操作、安全 bash 执行能力。

**与 Cloud Agent 模式的本质区别**：CodexPro 不是把代码传到云端去跑，而是通过 Cloudflare Tunnel / ngrok 让 ChatGPT 端的 MCP app 调到本地启的 MCP server。仓库永远在你机器上，ChatGPT 只是获得了"MCP tool call 能力"。

**与 Claude Code / OpenCode 的关键差异**：CodexPro 不是替代 ChatGPT 的本地 IDE，而是把 ChatGPT 现有的 UI 加上"对本地 repo 的工具能力"。用户在 ChatGPT 网页/桌面里就能看到工具卡片、diff、smoke test 结果，与平时用 ChatGPT 写代码的体验完全一致。

## 关键事实

- **Stars**：844 ⭐（发布于 2026-06-16，9 天内达到）
- **语言**：JavaScript（CLI + MCP server）
- **许可证**：MIT
- **协议依赖**：Cloudflare quick tunnel / ngrok free dev domain / Cloudflare named tunnel（任选其一）
- **账号要求**：ChatGPT Plus 或 Pro（免费/Go 账号不支持 Developer Mode）
- **节点要求**：Node.js 20+
- **话题标签**：`apps-sdk`, `chatgpt`, `cloudflare-tunnel`, `codex`, `local-development`, `mcp`, `ngrok`

## 核心机制

CodexPro 不是一个完整的"agent runtime"——它是一个**精确的 ChatGPT ↔ 本地 repo 桥**，由以下三层组成：

### 1. ChatGPT 端：Developer Mode + MCP app

ChatGPT 在 2026 Q2 推出了 Developer Mode（Settings → Apps → Advanced settings → Create app），允许用户为 ChatGPT 配置一个或多个自定义 MCP server 端点。CodexPro 在本地启的 server 暴露了 13 个 MCP tools：

| 工具分类 | 工具名 | 用途 |
|---------|--------|------|
| Workspace 打开 | `open_current_workspace`, `open_workspace`, `tree`, `search`, `read` | 列出/读取仓库文件 |
| 编辑 | `write`, `edit` | workspace-scoped 写入（返回 diff） |
| Review | `show_changes`, `git_status`, `git_diff` | 差异展示 + git 状态 |
| 安全执行 | `bash` (默认只跑 safe commands) | 跑 test / lint / build / git |
| Context | `codex_context`, `read_handoff` | 读取 `.ai-bridge/*` 与 Codex 上下文 |
| 导出 | `export_pro_context` | 为不支持 MCP 的 model surface 导出 bounded preview |

注意 CodexPro **不是**"让 ChatGPT 拥有万能工具"——它默认 `CODEXPRO_TOOL_MODE=standard`，工具表是窄且保守的；用户显式 `--tool-mode full` 才扩展到完整集合；`--no-bash` 可关掉所有 shell 执行。

### 2. 隧道层：Cloudflare Tunnel / ngrok

CodexPro 不暴露公网端口，而是用 Cloudflare quick tunnel（`cloudflared` 临时子域名）或 ngrok free dev domain 或用户自建的 Cloudflare named tunnel，给本地 MCP server 一个**外部可达的 URL**。这个 URL 在 setup 时被打印出来，用户粘到 ChatGPT 的 Developer Mode 配置页里。

为什么必须用隧道？因为 ChatGPT 的 MCP app 端点必须从公网可达（chat.openai.com 的服务端需要主动回调）。CodexPro 自动给 tunnel URL 加了 token protection——只有拥有这个 token 的 ChatGPT session 才能连上你的 MCP server。

### 3. 本地端：MCP server + context files

CodexPro 在本地启的 MCP server（`codexpro start` 启动后）做四件事：

1. **绑定仓库根目录**：所有 write/edit 都被沙箱化在指定 repo 内，无法越界
2. **读取 repo-backed context**：自动从 `AGENTS.md`、`.ai-bridge/current-plan.md`、git status、selected source files 提取上下文，作为 system prompt 注入到 ChatGPT
3. **执行安全的 bash**：默认白名单（test、lint、build、git），block 掉 secret/build/cache 路径的访问
4. **写入 handoff 文件**：把 ChatGPT 端做完的计划/决策写到 `.ai-bridge/pro-context.md`，供本地 Codex/OpenCode/Pi 等其他 agent 接手

这套架构的精妙之处是 **"ChatGPT 决策 + 本地执行" 完全分离**——ChatGPT 端永远不会直接执行命令，所有 side effect 都通过 MCP tool call 经过本地的 server，本地 server 又有 workspace 沙箱 + bash 白名单 + secret 路径屏蔽的多重保险。

## 与 ChatGPT 云端 Code Agent 的对比

| 维度 | ChatGPT 云端 (官方) | CodexPro |
|------|---------------------|----------|
| 代码位置 | 临时 VM（执行完销毁） | 用户本地 repo（持久） |
| Git 集成 | 需手动 push | 直接读 git status / diff |
| 跨会话 continuity | 依赖 ChatGPT 记忆 | 依赖 repo 的 `AGENTS.md` + `.ai-bridge/*` |
| 工具范围 | 官方工具集（受 OpenAI 审核） | 用户自定义（受本地沙箱约束） |
| 审查可见性 | 看 ChatGPT 端的工具卡片 | 看本地 + ChatGPT 双向的 diff 与 tool card |
| TOS 风险 | 完全合规 | 在合规边界内（README 显式声明不绕过模型/账号限制） |
| 适合场景 | 一次性任务、临时性编码 | 长期项目、与本地 CI/CD 集成的迭代式开发 |

## 与同类工具的差异化定位

CodexPro 自己在 README 里坦诚承认 "high-level shape can look similar because both use a local MCP bridge, a tunnel, and a workspace root"——很多本地 agent 桥接工具（langchain、autogen、各种 MCP-for-X 包装）确实都用了类似的三层架构。它的差异化在于**严格聚焦 ChatGPT-first + 严格 conservative defaults**：

- **ChatGPT-first**：不像 langchain/autogen 那样试图兼容所有 LLM 供应商，CodexPro 就服务 ChatGPT Plus/Pro + Developer Mode 这一个路径，把"ChatGPT 端该看到什么卡片、本地该暴露什么工具、tunnel 该怎么配"都优化到极致
- **Conservative defaults**：默认 `tool_mode=standard`、默认 safe-bash-only、默认 block secret 路径、默认 token-protected URL——这些都不是"用户友好"的默认值，而是"安全优先"的默认值
- **Repo-backed context**：明确把 `AGENTS.md`、`.ai-bridge/*` 当成一等公民，与 ChatGPT 端临时 UI state 严格分离——这意味着即使换 ChatGPT 账号、换 model surface，项目上下文都还在 repo 里
- **TOS-safe 产品边界**：README 反复强调不绕过模型限制、不 pool 账号、不做中间层——这是一个**自觉的合规姿态**，避免陷入"AI 工具绕过服务条款"的灰色地带

## 工程意义：ChatGPT 生态的"本地化"是 agent 时代的下一个方向

CodexPro 这种工具的崛起折射出 2026 年 agent 生态的一个清晰趋势：

**模型即服务 → 模型 + 本地工具双端协作**

过去两年 AI 编码工具的演化是：

1. **2023-2024**：Copilot 时代，模型在云端，本地只有补全
2. **2024-2025**：Cursor / Copilot Workspace 时代，模型在云端，但 IDE 是本地的
3. **2025-2026**：Claude Code / OpenCode 时代，模型仍是云端，但 **执行环境完全是本地的**（CLI + 本地文件系统 + 本地 git）
4. **2026 Q2+**：CodexPro / 类似工具时代，**连 UI 都不需要本地的 IDE**——直接在 ChatGPT 网页里调用本地 MCP server

第 4 阶段是真正意义上的"模型 + 本地工具解耦"——ChatGPT 的 UI 负责推理与对话，本地 MCP server 负责文件 I/O 与 side effects，两者通过标准 MCP 协议通信。这种解耦的价值是：

- **用户可以在 ChatGPT 里用 GPT-5.5/GPT-6 做对话式规划，但执行还是落在本地的 git repo 上**
- **不需要学习新 IDE**——CodexPro 用户的学习曲线基本只有"在 ChatGPT 设置里粘一个 URL"
- **跨设备 continuity 强**——同一个 ChatGPT 账号在笔记本/台式机/平板上都能用，只要该机器上跑着 CodexPro

但同时，TanStack 事件（关联 Article）揭示了这种"本地化扩展"也带来了**新的供应链风险面**——CodexPro 的依赖图谱里至少有 npm 上的 codexpro 本体、Cloudflare tunnel 守护进程、ngrok 客户端、ChatGPT Desktop 客户端、底层 OS 的代码签名证书。任何一个环节被攻陷都会影响整个桥接链的安全。

## 适用场景与不适用场景

### 适合

- **长期项目维护**：你有一个持续迭代的代码库，希望 ChatGPT 能在不离开 UI 的情况下完成日常 refactor、test 补充、文档更新
- **多机器协作**：你在公司 + 家各有一台开发机，希望用同一个 ChatGPT 账号无缝切换工作环境
- **CI/CD 集成**：你希望 ChatGPT 生成的代码 patch 直接落到本地 git 分支并触发 CI（通过 `.ai-bridge/*` 与本地脚本协作）
- **Codex 互补**：你已经在用本地 Codex CLI，但希望某些规划/对话任务交给 ChatGPT 完成（CodexPro 的 handoff 文件机制正好为此设计）

### 不适合

- **一次性脚本生成**：直接用 ChatGPT 网页写就行，不需要本地化
- **大规模代码库 refactor**：超过几千行代码的修改，本地 agent 桥接的工具调用成本会显著上升
- **完全离线的开发环境**：tunnel 依赖公网可达，企业内网或严格隔离环境无法使用
- **对 ChatGPT 账号合规有顾虑的团队**：CodexPro 在 README 里明确不绕过 OpenAI 的产品限制，但**使用 ChatGPT Developer Mode 本身**仍受 OpenAI 的使用条款约束

## 一句话总结

CodexPro 是 2026 年 Q2 涌现的"ChatGPT ↔ 本地 repo 桥接"赛道的代表项目。它用最小化的产品形态（CLI + 隧道 + 13 个 MCP tools）回答了一个清晰的问题：**"我不想为了在 ChatGPT 里操作本地 repo 而装一个新 IDE，能不能直接桥接？"** 它的 844 Stars（9 天）说明这个问题有真实市场需求；它的 MIT 许可证与保守默认值说明这是一个**自觉的、合规导向的工程实践**，而不是"绕过 ChatGPT 限制"的灰色工具。

---

*来源：[rebel0789/codexpro GitHub README](https://github.com/rebel0789/codexpro)，2026-06-16；GitHub API 验证 Stars = 844 / License = MIT / Lang = JavaScript / Created = 2026-06-16*
*Cluster: Local Agent Bridge / ChatGPT Apps SDK / MCP / Codex 生态扩展*
*关联 Article: [OpenAI TanStack 事件：签名链失陷与 macOS 强制升级机制](../security/openai-tanstack-npm-supply-chain-attack-response-macOS-forced-update-2026.md)*
