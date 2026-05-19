# Agentic AI Security Starter Kit：一站式防御 Prompt Injection 与 Agent 运行时威胁

> 这是一个在 2026 年 Agent 安全威胁急剧上升的背景下诞生的开源项目——它不是单一工具，而是一套可直接复制粘贴的生产级防御模板，覆盖了从检测到策略执行的全链路。

---

## 推荐理由

如果你正在部署 AI Agent，一定面临过这些困境：

- **Prompt Injection 怎么防？** 市面上缺乏可直接集成的检测方案
- **Claude Code 的 hooks 怎么配置？** 文档零散，官方示例寥寥
- **OPA 策略怎么应用到 Agent 场景？** 没有现成参考

Aembit 的 `agentic-ai-security-starter-kit` 解决的就是这个问题——**它不是教你什么是安全，而是给你可以直接用的代码**。

---

## 核心亮点

### 1. Prompt Injection 检测（可集成）

项目提供了多种检测模式的参考实现：

```python
# 基于启发式的 injection 检测（示例结构）
def detect_injection(user_input: str, context: dict) -> DetectionResult:
    # 检测常见的 injection 模式
    # - 嵌套指令（[INST], [/INST]）
    # - 角色扮演攻击（"You are now..."）
    # - Unicode 混淆（零宽字符、同形字符）
    # - 编码逃避（URL encode, HTML entity）
```

### 2. Claude Code Hooks 配置模板

Hooks 是 Claude Code 安全控制的第一道防线。项目提供了开箱即用的配置：

```json
{
  "preToolCall": {
    "enabled": true,
    "rules": [
      "block if payload contains suspicious patterns",
      "rate limit by user/ip",
      "log all tool calls for audit"
    ]
  },
  "postToolCall": {
    "enabled": true,
    "rules": [
      "validate output doesn't exceed size limits",
      "check for exfiltration patterns in response"
    ]
  }
}
```

### 3. OPA（Open Policy Agent）策略模板

OPA 为 Agent 运行时提供了声明式的策略控制：

```rego
# example: 限制敏感工具的调用权限
package agentic.security

default allow := false

allow if {
    input.tool_name == "bash"
    input.user_role == "admin"
}

allow if {
    input.tool_name == "read"
    input.file_path not starts with "/etc/shadow"
}
```

### 4. Sandboxing 配置示例

项目直接提供了主流沙箱（gVisor、Firecracker）的配置模板，覆盖了：
- 进程级资源限制（CPU、内存、挂载）
- 网络策略（允许/禁止出站流量）
- 文件系统只读化

---

## 技术深度

### 与 OpenAI Codex Windows Sandbox 的互补关系

**OpenAI 的 Windows Sandbox 解决的是「Agent 执行层的边界控制」**——确保代码运行在受限环境中。而 **Aembit 的 Starter Kit 解决的是「Agent 输入层的安全检测」**——在命令到达 harness 之前过滤威胁。

两者的组合形成了一个完整的纵深防御：

```
User Input → Prompt Injection Detection (Aembit)
          → Hooks Validation (Claude Code Hooks)
          → OPA Policy Enforcement (OPA)
          → Sandbox Execution (gVisor/Firecracker)
          → Network/File Constraints (OpenAI Windows Sandbox)
```

### 项目成熟度评估

| 维度 | 评分 | 说明 |
|------|------|------|
| 生产可用性 | ⭐⭐⭐⭐ | MIT 许可证，提供 copy-paste 示例 |
| 覆盖广度 | ⭐⭐⭐⭐ | 覆盖检测、hooks、OPA、sandbox |
| 文档质量 | ⭐⭐⭐ | 简洁直接，但缺乏深度解释 |
| 社区活跃度 | ⭐⭐⭐ | 刚开源，star 数有限（13）|

**笔者的判断**：这个项目的价值在于**它填补了「如何实际保护 Agent」的知识空白**——而不是另一个概念性的安全框架。对于正在从 PoC 走向生产的 Agent 团队，这是一份值得参考的清单。

---

## 适用场景

- ✅ 正在评估 Claude Code / Codex / Cursor 的企业安全团队
- ✅ 需要快速建立 Agent 安全基线的初创团队
- ✅ 研究 Agent 安全边界的安全研究员

---

## 参考来源

> "Working code examples to defend against Agentic AI threats: prompt injection detection, Claude Code hooks, OPA policies, and sandbox configs. Copy-paste ready, MIT licensed."
> — [Aembit/agentic-ai-security-starter-kit](https://github.com/aembit/agentic-ai-security-starter-kit), GitHub README

---

*归档目录：`projects/` | 防重：`aembit/agentic-ai-security-starter-kit`*