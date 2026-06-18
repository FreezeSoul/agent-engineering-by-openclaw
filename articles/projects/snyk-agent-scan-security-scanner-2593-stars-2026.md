---
title: "Snyk Agent Scan：企业级 Agent 安全扫描的全链路实践"
date: 2026-06-18
cluster: harness
source: https://github.com/snyk/agent-scan
source_type: github
tags: [security, MCP, skills, harness, enterprise, CI/CD]
pair_project: cisco-ai-defense/skill-scanner
pair_stars: 2208
pair_license: Apache-2.0
---

# Snyk Agent Scan：企业级 Agent 安全扫描的全链路实践

## 核心命题

**Snyk Agent Scan 解决了一个根本问题：随着 Agent（Claude Code、Cursor、Windsurf 等）成为开发主力，这些 Agent 背后依赖的 MCP 服务器和 Skills——谁来保证它们的安全？** Agent Scan 的答案是：不只是扫描，是覆盖"发现→分析→报告"全链路的企业级安全平台。

---

## 一、为什么 Agent 生态需要专门的安全扫描

传统安全工具假设"人写代码、代码不动"。但 Agent 时代，这个假设崩溃了：

- **MCP 服务器由配置文件定义，启动时执行命令**：扫描工具不能只读文件，必须实际运行 MCP 服务器才能获取完整的工具描述
- **Skills 是自然语言 + 代码的混合体**：Prompt Injection、Malicious Code、Data Exfiltration 可以在同一份 YAML 里混在一起
- **Agent 生态碎片化**：Claude Code、Cursor、Windsurf、VS Code、Gemini CLI、OpenClaw、Codex、Amazon Q……每家的 MCP 和 Skills 格式都不一样

这就是 Snyk Agent Scan 诞生的背景——**为 Agent 生态构建专门的安全扫描基础设施**。

---

## 二、核心技术：15+ 安全风险的全覆盖

Snyk Agent Scan 检测的安全风险分为 MCP 和 Skills 两大类：

### MCP 服务器风险

| 风险类型 | 描述 | 严重程度 |
|---------|------|---------|
| **Prompt Injection (E001)** | 恶意指令注入，劫持 Agent 行为 | 🔴 高 |
| **Tool Poisoning** | 污染工具描述，让 Agent 调用恶意工具 | 🔴 高 |
| **Tool Shadowing** | 覆盖同名工具，拦截本该发给正常工具的调用 | 🔴 高 |
| **Toxic Flows** | 诱导 Agent 执行危险操作的对话模式 | 🟡 中 |

### Skills 风险

| 风险类型 | 描述 | 严重程度 |
|---------|------|---------|
| **Prompt Injection (E004)** | Skills 自身携带的恶意 Prompt | 🔴 高 |
| **Malware Payloads (E006)** | 隐藏在自然语言中的恶意代码 | 🔴 高 |
| **Untrusted Content (W011)** | 处理不可信来源的内容 | 🟡 中 |
| **Credential Handling (W007)** | 不安全的凭据处理方式 | 🟡 中 |
| **Hardcoded Secrets (W008)** | Skills 中硬编码的密钥或 Token | 🔴 高 |

---

## 三、多平台 Agent 支持矩阵

Snyk Agent Scan 支持扫描以下平台的全量 MCP 和 Skills：

| Agent | macOS MCP | macOS Skills | Linux MCP | Linux Skills | Windows MCP | Windows Skills |
|-------|-----------|--------------|-----------|--------------|-------------|----------------|
| **Windsurf** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Cursor** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **VS Code** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Claude Desktop** | ✅ | — | — | — | ✅ | — |
| **Claude Code** | ✅ | ✅ | ✅ | ✅ | ✅ (WSL) | ✅ |
| **Gemini CLI** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **OpenClaw** | — | ✅ | — | ✅ | — | ✅ |
| **Codex** | ✅ | ✅ | ✅ | ✅ | — | — |
| **Amazon Q** | ✅ | — | ✅ | — | ✅ (WSL) | — |
| **Kiro** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 四、扫描范围：四层配置作用域

Snyk Agent Scan 的扫描粒度覆盖四个层次：

| 作用域 | 描述 | 示例 |
|--------|------|------|
| **System** | 机器级 / 企业托管的配置 | `/etc`, `managed-mcp.json`, `ProgramData` |
| **User** | 用户主目录的配置（跨项目生效）| `~/.cursor/`, `~/.claude/` |
| **Project / Workspace** | 特定项目/工作区的配置 | `.cursor/rules/`, `.claude/commands/` |
| **Extension / Plugin** | IDE 扩展内置的组件 | VS Code 扩展打包的 Skills |

---

## 五、使用方式：三步完成全机扫描

### 快速开始

```bash
# 安装（需要 uv 包管理器）
uvx snyk-agent-scan@latest
```

### 扫描全机器（自动发现所有 Agent）

```bash
# 设置 Snyk Token
export SNYK_TOKEN=your-api-token

# 运行完整扫描
uvx snyk-agent-scan@latest
```

### 扫描特定 Agent

```bash
# 只扫描 MCP 服务器（跳过 Skills）
uvx snyk-agent-scan@latest --no-skills

# 在沙箱中扫描（评估不可信配置时推荐）
docker run --rm -it \
  -v /path/to/config:/config \
  snyk/agent-scan --config /config/mcp.json
```

---

## 六、安全警告：扫描 MCP 配置会执行命令

Snyk Agent Scan 官方文档明确指出：

> ⚠️ **IMPORTANT**: Scanning MCP configurations will execute the commands defined in them.
>
> When Agent Scan scans an MCP configuration file, it starts the stdio MCP servers by executing the commands and arguments specified in the config.

**笔者认为，这个设计揭示了 MCP 安全扫描的核心矛盾**：想要完整分析 MCP 服务器的安全性，就必须实际运行它；但运行不可信的 MCP 服务器本身就是安全风险。

Snyk 给出的建议是：**在沙箱环境（Docker 容器、VM、可丢弃环境）中扫描第三方或不可信的 MCP 配置**。这与 Cursor 的沙箱设计形成了有趣的呼应——**沙箱不仅是运行 Agent 的安全边界，也是安全扫描的安全边界**。

---

## 七、与 Cisco Skill Scanner 的互补关系

| 维度 | Snyk Agent Scan | Cisco Skill Scanner |
|------|----------------|---------------------|
| **主要焦点** | MCP 服务器 + Skills 全链路 | Skills 专项深度扫描 |
| **检测引擎** | 静态分析 + 签名匹配 | 静态分析 + YARA + LLM-as-a-judge + 数据流分析 |
| **支持格式** | 15+ 种 Agent（MCP + Skills）| OpenAI Codex Skills + Cursor Agent Skills |
| **CI/CD 集成** | ✅ Snyk 平台 | ✅ GitHub Actions + SARIF |
| **Pre-commit** | — | ✅ |
| **企业特性** | Snyk Evo 平台（商业版）| Cisco AI Defense 云端扫描 |
| **Stars** | 2,574 | 2,208 |

**两者形成了互补**：Snyk 擅长**全链路发现**（找到机器上所有 Agent 的所有 MCP/Skills），Cisco 擅长**深度分析**（用多引擎手段深度挖掘 Skills 中的复杂威胁）。

---

## 八、关键引用

> "Agent Scan helps you keep an inventory of all your installed agent components (harnesses, MCP servers, and skills) and scans them for common threats like prompt injections, sensitive data handling, or malware payloads hidden in natural language."

— Snyk Agent Scan README

> "By default, Agent Scan requires explicit user consent (y/n) before starting each stdio MCP server during interactive runs. This gives you control over what gets executed on your system."

— Snyk Agent Scan README

---

## 九、适用场景

| 场景 | 推荐理由 |
|------|---------|
| **企业安全审计** | 全链路发现 + Snyk Evo 平台集中管理 |
| **引入第三方 MCP** | 在沙箱中扫描，验证安全性后再集成 |
| **CI/CD 流水线** | 与 Snyk 平台集成，自动化安全门禁 |
| **多 Agent 环境** | 同时覆盖 Claude Code、Cursor、Windsurf 等多种 Agent |
| **Prompt Injection 防护** | 检测 Skills 中的恶意 Prompt 注入 |

---

## 十、局限性

| 局限 | 说明 |
|------|------|
| **扫描会执行 MCP 命令** | 必须配合沙箱环境使用 |
| **Skills 扫描需 Token** | 企业版功能，需要 Snyk 账号 |
| **结果不等于安全证明** | "No findings" 只表示未发现已知模式，不等于绝对安全 |
| **不能替代人工审查** | 高风险场景仍需人工代码审查 |

---

## 总结

**Snyk Agent Scan 的最大价值不在于"扫描"本身，而在于它证明了 Agent 安全需要专门的基础设施。** 传统安全工具无法理解 MCP 服务器的动态特性，也无法处理 Skills 这种自然语言+代码的混合体。Snyk Agent Scan 和 Cisco Skill Scanner 的出现，标志着 Agent 安全从"通用安全扫描的附属品"演变为"独立的安全赛道"。

**下一步**：在沙箱环境中运行 `uvx snyk-agent-scan@latest`，扫描你机器上的所有 Agent 配置——你可能会惊讶于发现了多少潜在的安全盲区。
