# abtop：AI 编码 agent 的 htop 多 session 监控 2026

> **来源**：[https://github.com/graykode/abtop](https://github.com/graykode/abtop) | MIT License | 2,978⭐ | 验证于 2026-06-19 via GitHub API

## 项目速览

abtop 是一个用 Rust 编写的 TUI（Terminal UI）监控工具，定位是 **"AI 编码 agent 的 htop"**——同时监控多个 Claude Code、Codex CLI、OpenCode session 的 token 使用、context window 百分比、rate limit、子进程、孤儿端口等关键指标。

它在 Claude Code 的 1M Context 时代填补了一个工程化空白：**`/usage` 命令给你看单个 session 的使用量，但 abtop 让你同时看多个 session 的健康状态**。

## 核心特性

### 1. 多 Agent 跨工具支持

| Feature | Claude Code | Codex CLI | OpenCode |
|---------|:-----------:|:---------:|:--------:|
| Session 发现 | ✅ | ✅ | ✅ |
| Token 追踪 | ✅ | ✅ | ✅ |
| Context Window % | ✅ | ✅ | ❌ |
| Rate Limit 实时显示 | ✅ | ✅ | ❌ |
| 当前任务检测 | ✅ | ✅ | ❌ |

通过读取本地进程/文件状态发现 session，**macOS/Linux/Windows 全平台支持**，无需任何 API key 或认证。

### 2. Session 级 Context Window 可视化

这是 abtop 的核心价值——**每个 session 一个 context window 百分比进度条**，配合颜色警告让用户一眼判断：

- 哪些 session 接近 context 上限（应该 compact 或 clear）
- 哪些 session 还有充足空间（可以继续工作）
- 哪些 session 已经触发自动 compact（可能进入 context rot 区间）

这个能力直接对应 Claude Code 官方 `claude.com/blog/using-claude-code-session-management-and-1m-context`（2026-04-15）文章里提出的核心命题："**Session 不是越长越好；Context 不是越满越好**"。

### 3. tmux 集成：跨 pane 跳转

abtop 配合 tmux 用时，按 Enter 可以**直接跳转到那个 session 所在的 pane**——把"监控"和"操作"无缝串起来：

```bash
tmux new -s work
# pane 0: abtop
# pane 1: claude (project A)
# pane 2: claude (project B)
# → Enter on a session in abtop jumps to its pane
```

### 4. 资源管理：孤儿端口检测

Agent 经常 spawn 服务器然后忘记 kill，留下孤儿端口。abtop 的 netstat-based 孤儿端口检测是**给 session 监控加了一层基础设施健康检查**。

## 安装与使用

### macOS / Linux

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/graykode/abtop/releases/latest/download/abtop-installer.sh | sh
```

### Cargo

```bash
cargo install abtop
```

### 使用

```bash
abtop                    # 启动 TUI
abtop --once             # 打印快照并退出
abtop --json             # 一次性 JSON 输出（供脚本/工具使用）
abtop --setup            # 安装 rate limit 收集 hook
abtop --theme dracula    # 指定主题启动
```

## 主题与生态标签

GitHub topics: `ai-agents`, `ai-coding-agent`, `btop`, `claude-code`, `cli`, `codex`, `developer-tools`, `htop`, `monitor`, `ratatui`, `rust`, `terminal`, `tui`

其中 `claude-code` + `codex` + `tui` + `monitor` 四个标签直接对应 AI Coding 工具集成的核心需求，说明这是一个**针对 AI Coding Agent 生态原生构建**的工具，不是泛化的进程监控器。

## Pair 关联性

**Article 关联**：`claude-code-session-management-decision-tree-1m-context-2026.md`（Claude Code Session 决策树：/usage /rewind /compact 2026）

**Pair 强度（4-way SPM）**：

- **Layer 1 cluster 共享**：ai-coding cluster ✓
- **Layer 2 SPM 关键词**：context window / session / token usage / monitoring / Claude Code / Codex ✓
- **Layer 3 topics 命中**：claude-code / ai-coding-agent / monitor / developer-tools ✓
- **Layer 4 维度互补**：Article = 决策框架（何时 continue/rewind/compact/clear），Project = 实时可观测性（看到每个 session 当前状态）= 决策需要数据，abtop 提供数据 ✓

**Pair 闭环**：4-way SPM 满中 ⭐⭐⭐⭐⭐

## 为什么 abtop 值得关注

1. **填补官方 `/usage` 的工程化空白**：`/usage` 是单 session 内置命令，abtop 是多 session 跨平台工具
2. **Rust 实现 + TUI 范式**：内存高效、毫秒级冷启动，借鉴 htop/btop 的成熟 UI 范式
3. **填补多 Agent 并行实践的可观测性缺口**：随着多 session / subagent 并行成为常态，多 session 同时监控从"可选"变成"必需"
4. **零依赖部署**：无 API key、无 auth、read-only，安全门槛极低
5. **紧贴 Anthropic 官方方向**：直接对应 2026 年 4 月 Claude 官方博客关于 session 管理的核心命题，是社区对官方理念的快速响应

## License 与可持续性

- **License**: MIT（开源友好）
- **维护活跃度**: 高频 release，stars 增长稳定
- **Stars / 时间**: 2,978⭐（2026-06-19），保持稳定上升

---

**Pair 总结**：本文 Article（Claude Code Session 决策树）+ 本文 Project（abtop 多 session 监控）= 一个完整的 "**判断 + 观察**" 闭环——工程师读 Article 学会"何时该 continue/rewind/compact/clear"的判断框架，配合 abtop 在终端实时观察每个 session 的 token 上下文使用百分比，把 session 管理从"凭感觉"升级为"基于数据 + 框架决策"的工程化实践。