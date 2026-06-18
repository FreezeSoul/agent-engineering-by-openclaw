# Claude Code Hooks 完整生命周期指南：13 个钩子事件全覆盖的工程实践

> 本文推荐 [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)：Claude Code Hooks 的完整生命周期参考实现，涵盖全部 13 个钩子事件，3,773 Stars。

## 核心命题

**Claude Code 的 Hook 系统不只是「拦截点」，而是一个完整的生命周期控制框架——从 SessionStart 到 SessionEnd，从 UserPromptSubmit 到 SubagentStop，13 个钩子覆盖了 Agent 与开发者交互的每一个关键节点。** 这个项目用 13 个独立 Python 脚本（基于 UV single-file scripts）实现了全链路覆盖，是理解 Claude Code Hooks 工程设计的最佳参考。

> 笔者认为：R443 Article「Anthropic Claude Code 七种自定义方法决策框架」把 Hooks 定义为七种自定义方法之一，但 Hooks 的实际工程复杂度远比「方法」这个词暗示的要高——它是一个完整的事件驱动架构，理解它需要理解整个生命周期。

---

## 一、项目概述

`disler/claude-code-hooks-mastery` 是一个教育性和实践性并重的开源项目，作者是 Claude Code Hooks 领域的深度实践者。项目核心价值：**用 13 个独立脚本完整覆盖 Claude Code 官方文档中的全部 13 个钩子事件**，每个脚本配有详细注释和增强实现。

### 基础信息

| 维度 | 数值 |
|------|------|
| **GitHub Stars** | 3,773 |
| **Forks** | 622 |
| **License** | 未在 README 明确（需检查） |
| **Primary Language** | Python (82.8%), TypeScript (17.2%) |
| **架构特点** | UV single-file scripts（无虚拟环境依赖） |

### 核心技术选择：UV Single-File Scripts

项目采用 Astral UV 的 single-file scripts 架构：

```bash
# 钩子脚本直接声明依赖，UV 自动处理
# .claude/hooks/user_prompt_submit.py
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic", "structlog"]
# ///
```

> 原文引用："This project leverages UV single-file scripts to keep hook logic cleanly separated from your main codebase. All hooks live in `.claude/hooks/` as standalone Python scripts with embedded dependency declarations." — [disler/claude-code-hooks-mastery README](https://github.com/disler/claude-code-hooks-mastery)

笔者认为：**UV single-file scripts 是 Claude Code Hooks 的最优工程选择**——每个钩子独立声明依赖，不污染主项目环境，部署时只需拷贝文件，无需 `pip install`。

---

## 二、13 个钩子完整生命周期

项目覆盖 Claude Code 官方定义的 13 个钩子事件：

### 钩子分类总览

```
Session 生命周期
├── Setup（初始化/定时维护）
├── SessionStart（启动/恢复/清理）
└── SessionEnd（退出/中断/错误）

主对话循环
├── UserPromptSubmit（用户提交前）
├── PreToolUse（工具执行前）
├── PermissionRequest（权限请求）
├── PostToolUse（工具执行后）
├── PostToolUseFailure（工具执行失败）
├── SubagentStart（子 Agent 启动）
├── SubagentStop（子 Agent 停止）
├── Notification（通知）
└── Stop（响应停止）

维护操作
└── PreCompact（压缩前）
```

### 1. UserPromptSubmit Hook

**触发时机**：用户提交 prompt 后，Claude 处理前  
**有效载荷**：`prompt` 文本、`session_id`、时间戳  
**增强实现**：Prompt 验证、日志记录、上下文注入、安全过滤

```python
# user_prompt_submit.py 的核心逻辑
def enhance_prompt(prompt: str, session_id: str) -> dict:
    # 1. 安全过滤 - 检测敏感信息
    filtered = security_filter(prompt)
    # 2. 上下文注入 - 添加项目相关信息
    enhanced = inject_context(filtered)
    # 3. 日志记录
    log_hook("user_prompt_submit", {"prompt": enhanced})
    return {"prompt": enhanced, "session_id": session_id}
```

> 原文引用："Fires: Immediately when user submits a prompt (before Claude processes it). Payload: prompt text, session_id, timestamp." — Claude Code Hooks 官方文档

### 2. PreToolUse Hook

**触发时机**：任意工具执行前  
**有效载荷**：`tool_name`、`tool_input` 参数  
**增强实现**：危险命令拦截（`rm -rf`、`.env` 访问）

```python
# pre_tool_use.py 的安全增强
DANGEROUS_COMMANDS = ["rm -rf", "sudo rm", "chmod -R"]
PROTECTED_PATHS = [".env", "id_rsa", "id_ed25519"]

def block_dangerous(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if any(d in cmd for d in DANGEROUS_COMMANDS):
            raise HookError(f"Blocked dangerous command: {cmd}")
        if any(p in cmd for p in PROTECTED_PATHS):
            raise HookError(f"Blocked protected path access: {p}")
    return tool_input
```

### 3. PostToolUse Hook

**触发时机**：工具成功执行后  
**有效载荷**：`tool_name`、`tool_input`、`tool_response`  
**增强实现**：JSONL 日志 → 可读 JSON 转换（chat.json）

> 笔者认为：PostToolUse 是最实用的钩子——可以实现自动化代码质量门禁（lint、type check）、文档生成、测试触发等场景。

### 4. PreCompact Hook

**触发时机**：Claude Code 执行压缩操作前  
**有效载荷**：`trigger`（"manual" 或 "auto"）、`custom_instructions`、`session_info`  
**增强实现**：Transcript 备份、verbose 反馈

```python
# pre_compact.py 的增强实现
def backup_and_log(trigger: str, session_info: dict):
    # 1. 备份当前 transcript
    transcript_path = session_info["transcript_path"]
    backup_path = f"{transcript_path}.backup"
    copy_file(transcript_path, backup_path)
    # 2. 记录压缩前状态
    log_hook("pre_compact", {
        "trigger": trigger,
        "session_id": session_info["session_id"],
        "backup_path": backup_path
    })
```

### 5. SessionStart / SessionEnd Hooks

**SessionStart 触发时机**：新 session 启动、恢复已有 session、清理 session 时  
**有效载荷**：`source`（"startup"、"resume"、"clear"）、session 信息  
**增强实现**：开发上下文加载（git status、recent issues、context files）

**SessionEnd 触发时机**：session 结束（exit、sigint、error）  
**有效载荷**：`session_id`、`transcript_path`、`cwd`、`permission_mode`、`reason`  
**增强实现**：Session 日志记录、可选清理任务（删除临时文件、过期日志）

> 原文引用："SessionStart Hook: Fires when Claude Code starts a new session or resumes an existing one. Payload: source ('startup', 'resume', or 'clear'), session info. Enhanced: Development context loading (git status, recent issues, context files)." — README

---

## 三、退出码与流程控制

Hook 通过退出码与 Claude Code 通信：

| 退出码 | 行为 | 描述 |
|--------|------|------|
| **0** | Success | Hook 执行成功，`stdout` 在 transcript 模式显示给用户 |
| **1** | Block | 阻止操作执行，`stdout` 显示为错误信息 |
| **N** | Custom | 依赖具体钩子定义 |

```python
# 成功退出 - 0
print(json.dumps({"status": "ok", "action": "logged"}))
sys.exit(0)

# 阻止操作 - 非零退出码
print(json.dumps({"error": "Security violation: blocked rm -rf"}))
sys.exit(1)
```

---

## 四、TTS 通知系统

项目实现了智能 TTS（Text-to-Speech）通知系统：

```
通知优先级：ElevenLabs > OpenAI > Anthropic > Ollama > pyttsx3
```

### Notification Hook

**触发时机**：Claude Code 发送通知时（等待用户输入等）  
**有效载荷**：`message` 内容  
**增强实现**：TTS 播报 "Your agent needs your input"（30% 概率包含用户名）

### Stop Hook

**触发时机**：Claude Code 完成响应时  
**有效载荷**：`stop_hook_active` 布尔标志  
**增强实现**：AI 生成完成消息 + TTS 播放（使用 LLM 优先级：OpenAI > Anthropic > Ollama）

```python
# stop.py 的 TTS 实现
def generate_completion_message(stop_reason: str) -> str:
    # 调用 LLM 生成上下文相关的完成消息
    return llm.generate(
        f"Claude Code stopped because: {stop_reason}. "
        "Generate a brief, helpful completion message."
    )

def play_tts(message: str):
    # 按优先级尝试各 TTS 提供商
    for provider in TTS_PRIORITY:
        if provider == "elevenlabs":
            elevenlabs.speak(message)
            break
        elif provider == "openai":
            openai.tts.speak(message)
            break
```

> 笔者认为：TTS 通知是 Hook 扩展性的极致体现——在需要人工介入时主动通知，而不是默默等待用户发现。这是 Agent 设计中「human-in-the-loop」原则的具体实现。

---

## 五、Subagent 生命周期钩子

### SubagentStart Hook

**触发时机**：子 Agent（Task 工具）启动时  
**有效载荷**：`agent_id`、`agent_type`、session 信息  
**增强实现**：Subagent 启动日志记录 + 可选 TTS 播报

### SubagentStop Hook

**触发时机**：子 Agent 停止时  
**有效载荷**：`stop_hook_active` 布尔标志  
**增强实现**：TTS 播报 "Subagent Complete"

```python
# subagent_stop.py
def announce_subagent_complete(agent_id: str):
    message = f"Subagent {agent_id} Complete"
    log_hook("subagent_stop", {"agent_id": agent_id, "message": message})
    tts.speak(message)  # TTS 播报
```

> 笔者认为：Subagent 的 Start/Stop 钩子填补了 Claude Code 官方文档中关于 Subagent 生命周期管理的空白——这是 R443 Article 中「Subagents」方法的核心工程细节。

---

## 六、安全增强

项目在多个层次实现了安全增强：

### 1. 命令级别拦截

```python
# PreToolUse 中的命令过滤
BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",      # 防止根目录删除
    r"chmod\s+-R\s+777",  # 防止权限放大
    r">\s*/etc/passwd",   # 防止系统文件篡改
]
```

### 2. 文件访问保护

```python
PROTECTED_PATHS = [
    ".env",           # 敏感配置
    "id_rsa",         # SSH 私钥
    "id_ed25519",
    ".aws/credentials",  # 云凭据
    ".netrc"           # 网络凭据
]
```

### 3. PermissionRequest 钩子

**触发时机**：显示权限对话框时  
**增强实现**：权限审计日志 + 自动允许只读操作（Read、Glob、Grep、安全 Bash）

> 原文引用："PermissionRequest Hook: Fires when user is shown a permission dialog. Enhanced: Permission auditing, auto-allow for read-only ops (Read, Glob, Grep, safe Bash)." — README

---

## 七、与 R443 Article 的关联性

> 🔗 本文与 R443 Article「Anthropic Claude Code 七种自定义方法决策框架」形成**深度工程实现**关联：R443 给出的是「Hooks 是七种自定义方法之一」的认知框架，本文展示的是该框架的**完整生命周期实现**——13 个钩子事件、退出码协议、TTS 通知系统、安全增强。

### 闭环逻辑

```
R443 决策框架（理论）
└── Hooks 作为七种方法之一
    ├── UserPromptSubmit → Prompt 预处理
    ├── PreToolUse → 工具安全门禁
    ├── PostToolUse → 质量验收
    ├── SessionStart/End → 上下文管理
    └── SubagentStart/Stop → 子 Agent 生命周期

disler/claude-code-hooks-mastery（完整实现）
└── 13 个钩子全覆盖 + 增强实现 + 工程最佳实践
```

---

## 八、快速上手

```bash
# 1. 安装 UV（如果没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆仓库
git clone https://github.com/disler/claude-code-hooks-mastery.git
cd claude-code-hooks-mastery

# 3. 将 hooks 复制到你的项目
cp -r .claude/hooks ~/.claude/hooks

# 4. 运行 Claude Code，hooks 自动生效
# 观察 logs/ 目录中的 JSON 日志
ls logs/
```

---

## 九、适用场景

| 场景 | 推荐度 | 理由 |
|------|--------|------|
| 学习 Claude Code Hooks 完整机制 | ⭐⭐⭐⭐⭐ | 13 个钩子全覆盖的最佳教程 |
| 实现代码质量门禁 | ⭐⭐⭐⭐⭐ | PostToolUse + lint/type check 组合 |
| 安全敏感项目 | ⭐⭐⭐⭐ | 多层安全拦截（命令、文件、权限）|
| 需要自动通知的 Agent 工作流 | ⭐⭐⭐⭐ | TTS 通知系统开箱即用 |
| Session 恢复/持久化 | ⭐⭐⭐ | SessionStart/End 钩子支持 |
| Subagent 编排 | ⭐⭐⭐ | Subagent 生命周期日志 |

---

## 总结

`disler/claude-code-hooks-mastery` 代表了 Claude Code Hooks 领域的深度工程实践：

1. **全生命周期覆盖**：13 个钩子事件无一遗漏，每个都有可运行的增强实现
2. **工程化架构**：UV single-file scripts 解耦钩子依赖，无需虚拟环境管理
3. **安全第一**：多层安全拦截（命令、文件、权限），适合企业级部署
4. **TTS 通知创新**：智能语音通知系统，human-in-the-loop 的工程实现

对于 Agent 工程师而言，这个项目是理解 Claude Code Hooks 架构设计的最佳实践教材——不是官方文档的简单翻译，而是基于官方 API 的深度工程扩展。
