# Claude Code Hooks：8 大事件全生命周期与可编程 Harness

> 关键词：Claude Code Hooks、PreToolUse / PostToolUse、SessionStart、UserPromptSubmit、PermissionRequest、PreCompact、SubagentStop、Programmable Harness
>
> 源头：[Claude Blog — How to configure hooks](https://claude.com/blog/how-to-configure-hooks)（Anthropic 官方，2026 年）
>
> 适用集群：`articles/harness/` — Harness 内核可编程层子维度（cluster 内首个 hooks 全生命周期深读）

---

## 一句话定位

Hooks 是 Claude Code 暴露给用户的**唯一可编程执行点**——8 个事件、settings.json 注册、shell 命令执行、exit code / stdin / stdout 三通道协议。这是 Anthropic 把 Harness Engineering 开放给开发者自定义的核心机制。

---

## 为什么这篇文章必须写

`articles/harness/` 现有 169 篇文章，但 hooks 作为子维度**只有 1 篇提及**（`anthropic-auto-mode-vs-openai-hooks-agent-extensibility-2026.md`），且该篇专注 Anthropic Auto Mode vs OpenAI Hooks 的横向对比，**没有一篇专门讲 Claude Code 8 大 hook 的全生命周期**。这是一个清晰的 **cluster 内 0→1 启动信号**——hooks 是 Claude Code Harness 唯一可编程层，2026 上半年 Claude Code 装机量爆发后，社区对 hook 机制的认知滞后于官方文档。

本文填补这一空白：用 8 个 hook 的事件全图 + 三类问题解法 + 配置示例 + 调试方法，把 hooks 从「零散命令片段」变成「完整可编程层」。

---

## Hooks 解决的三类问题

根据 Anthropic 官方文章，hooks 解决的核心问题分三类：

### 1. 消除重复手工操作（Repetitive manual steps）

> Instead of running your formatter after every file change, a `PostToolUse` hook handles it automatically.

典型场景：

- `PostToolUse` 触发 Prettier / ESLint，避免每次写文件后手动跑格式化
- `PermissionRequest` 自动批准 `npm test`，避免第 100 次重复确认
- `SessionStart` 自动加载 git status、TODO 列表、当前 sprint 上下文，免去首轮粘贴

### 2. 自动强制项目规则（Project-specific guardrails）

> You can block dangerous commands before they execute, validate file paths before writes, or ensure naming conventions are followed.

典型场景：

- `PreToolUse` 阻止 `rm -rf` / 强制 `git push --no-verify`
- `PreToolUse` 验证文件路径必须落在 `src/` 下，禁止写 `node_modules/` 或 `/etc/`
- `PreToolUse` 强制命名规范（如 kebab-case 文件名）

### 3. 动态上下文注入（Dynamic context injection）

> A `SessionStart` hook can feed Claude your current git status and TODO list.

典型场景：

- `SessionStart` 自动 `git status --short && git log --oneline -5`
- `UserPromptSubmit` 自动追加 sprint 优先级 / 当前 feature flag 状态
- `PreCompact` 在压缩前自动备份关键决策到独立文件

---

## 8 大 Hook 事件全图

| Hook | 触发时机 | 典型用途 |
|------|---------|---------|
| **PreToolUse** | 工具执行前 | 阻断危险命令、验证文件路径、自动批准安全操作 |
| **PermissionRequest** | 权限弹窗前 | 自动批准测试命令、屏蔽敏感文件访问 |
| **PostToolUse** | 工具完成后 | 跑格式化、触发 lint、记录文件变更 |
| **PreCompact** | 上下文压缩前 | 备份 transcript、保存重要决策 |
| **SessionStart** | 会话开始 / 恢复时 | 注入 git status、加载 TODO、设置环境 |
| **Stop** | Claude 完成响应时 | 验证任务完成度、跑测试、生成摘要 |
| **SubagentStop** | Subagent 完成时 | 校验子代理输出、触发后续动作 |
| **UserPromptSubmit** | 用户提交 prompt 时 | 注入 sprint 上下文、校验请求、补充动态上下文 |

8 个事件覆盖一个完整 session 的**全生命周期**：startup → 工具执行 → 用户输入 → 完成 → 压缩 → subagent 委派 → 终止。

**与 auto-mode 的关系**：Anthropic Auto Mode（参见 `anthropic-claude-code-auto-mode-classifier-based-permission-2026.md`）是 ML-driven 的权限决策；hooks 是**确定性、可审计、可回放**的权限决策——两者互补而非替代。生产环境的最佳实践 = hooks 处理确定性规则 + auto-mode 处理模糊边界。

---

## 配置协议（settings.json + JSON）

Hooks 通过 `~/.claude/settings.json` 或 `.claude/settings.json`（项目级）注册，结构：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

**关键字段**：

- **matcher**：正则表达式，匹配触发 hook 的工具名（如 `Write|Edit|MultiEdit`）
- **hooks[].command**：要执行的 shell 命令
- **type**：当前仅 `command` 一种（未来可能支持 HTTP webhook）

**通信协议**：hook 通过三个通道与 Claude Code 通信：

1. **stdin**：Claude Code 把触发事件 JSON 写入 hook 进程 stdin（包含工具名、参数、上下文）
2. **stdout**：hook 输出会被记录到 transcript，但不直接传回 Claude
3. **exit code**：`0` = 成功放行；`2` = 阻断操作（错误信息通过 stderr 反馈给 Claude）；其他非零 = 普通错误

**这一协议与 Unix 哲学一致**——任何能写 stdin / 读 exit code 的脚本语言都可以做 hook 实现，无需 SDK 依赖。

---

## 调试方法（When things go wrong）

官方推荐的调试路径：

1. **开启 transcript 日志**：`/help` → 启用 verbose mode，hook 触发记录在 transcript 中
2. **独立运行 hook 命令**：把 stdin JSON 复制到临时文件，直接跑 hook 命令验证逻辑
3. **matcher 验证**：用最小可复现的 tool 调用（如 `Write` 一个文件）测试 PreToolUse 是否触发
4. **exit code 验证**：用 `&& echo OK || echo BLOCK` 测试阻断逻辑

**反模式**：不要在 hook 里跑长任务（>30s）——hooks 是同步执行的，长任务会卡住整个 Claude Code session。应当 fire-and-forget 或用 `nohup &`。

---

## 与现有 harness 概念的关系

Hooks 是 Claude Code Harness Engineering 的**可编程扩展点**，对应其他系统的不同概念：

| 系统 | 等价机制 | 区别 |
|------|---------|------|
| LangChain | Middleware | LangChain middleware 在 Python 进程内；Claude Code hooks 是 shell 进程 |
| OpenAI Codex | Hooks API | 同名机制，但 Claude Code 8 个事件 vs OpenAI GA 5 个事件，事件命名差异较大 |
| AutoGPT | Plugin / Tool | 工具是被动调用；hook 是主动拦截，权限位置不同 |
| VSCode | settings.json + extension | 都是 JSON 配置 + 命令执行，但 hooks 跑在 Claude session 内 |

**核心定位**：hooks = 「Claude Code Harness 的 system call interface」——任何用户想插入自定义逻辑的标准入口。

---

## 实践模式（来自社区）

根据 `diet103/claude-code-infrastructure-showcase`（9714⭐ MIT，6 个月生产打磨）：

### 模式 1：Auto-activating skills via hooks

skills 默认是被动加载（用户 prompt 触发）。用 `UserPromptSubmit` hook 扫描 prompt，匹配到特定 skill 关键词时自动 `cat $SKILL_FILE` 注入到上下文——实现「skills 自动激活」。

### 模式 2：Dev docs 持久化

用 `PreCompact` hook 在每次 context 压缩前把关键决策 dump 到 `.claude/decisions.md`——避免 compaction 丢失「为什么这么设计」的隐性知识。

### 模式 3：项目级 guardrails

团队项目用 `PreToolUse` hook 强制：

- 文件路径必须在 `src/` / `tests/` / `docs/` 三个目录之一
- 写文件后必须跑 ESLint（`PostToolUse` matcher=`Write`）
- 提交前必须跑 `npm test`（`Stop` hook）

### 模式 4：Subagent 验证链

`SubagentStop` hook 在 subagent 完成时跑「回归检查」——确保 subagent 输出的代码通过 linter，否则让 Claude 继续迭代。

---

## 为什么 hooks 比 middleware 更轻

对比 LangChain Middleware / AutoGPT Plugin 等机制，Claude Code hooks 的关键优势：

1. **零依赖**：任何 shell 命令即可，不需要 SDK / Python 包
2. **零状态**：hook 进程独立运行，Claude Code 不维护 hook 状态（崩溃恢复简单）
3. **零语言绑定**：Python / Node / Bash / Rust 都能写 hook
4. **可审计**：所有 hook 调用记录在 transcript，可重放调试
5. **可禁用**：直接 `~/.claude/settings.json` 删 hook 配置即可（不破坏 Claude Code 主程序）

这一轻量化设计是 Claude Code 装机量爆发的关键——团队可以在不修改 Claude Code 二进制的前提下，定制任意工作流。

---

## 局限性与未来方向

hooks 当前未覆盖的能力：

- **异步执行**：所有 hook 同步执行，长任务会卡 session
- **HTTP webhook**：当前只能 shell，无法直接调外部 API（需要 wrapper 脚本）
- **状态共享**：多 hook 之间无法直接共享变量（需借助文件系统）
- **UI 集成**：hook 阻断时只有 stderr 错误信息，无富 UI 弹窗

**预期 2026 下半年**：异步 hooks、webhook hooks、shared state API。

---

## 实践指南：第一次配 hook

**最小可行配置**（推荐起点）：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "prettier --write $CLAUDE_FILE_PATHS 2>/dev/null || true" }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "git status --short && git log --oneline -3" }
        ]
      }
    ]
  }
}
```

这一配置实现两件事：

1. 写文件后自动跑 Prettier
2. 每次用户 prompt 前注入 git 上下文

**进阶路径**：

- 加 `PreToolUse` 阻止 `rm -rf`
- 加 `PreCompact` 备份决策
- 加 `Stop` 跑测试

每加一个 hook，先跑最小复现测试，再合并到主配置——避免一次写 10 个 hook 但有 1 个阻断所有操作。

---

## 总结：Hooks = Harness 的 System Call Interface

Claude Code hooks 把 Anthropic Harness Engineering 的设计哲学推到了极致：**用户应该能定制自己 Agent 的所有行为，无需 fork 客户端**。8 个事件 + JSON 配置 + shell 执行 = 极简的可编程表面。

在 `articles/harness/` 的子维度版图中：

- **Auto-mode** = ML-driven 权限决策（参见 `anthropic-claude-code-auto-mode-classifier-based-permission-2026.md`）
- **Sandboxing** = OS-level 隔离（参见 `anthropic-claude-code-sandboxing-os-level-isolation-2026.md`）
- **Hooks**（本篇）= 用户自定义执行点 = **确定性、可审计、可回放的权限与自动化层**

三者构成 Claude Code Harness 的完整三角：Auto-mode 解决「不确定该不该做」、Sandboxing 解决「做了会怎样」、Hooks 解决「我能不能定制做的方式」。

---

## 引用源

- 一手源：[Claude Blog — How to configure hooks](https://claude.com/blog/how-to-configure-hooks)（Anthropic 官方 2026）
- 社区实现：[diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)（9714⭐ MIT，hooks + skills + agents 6 个月生产打磨）
- 对比参照：[Anthropic Auto Mode](https://www.anthropic.com/engineering/claude-code-auto-mode) / [OpenAI Codex Hooks](https://developers.openai.com/codex/hooks) / [LangChain Middleware](https://blog.langchain.com/middleware/)
- 同集群延伸：`anthropic-auto-mode-vs-openai-hooks-agent-extensibility-2026.md`（横向对比）、`anthropic-claude-code-sandboxing-os-level-isolation-2026.md`（隔离层）
