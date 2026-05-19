# MEDUSA：面向 Agentic AI 时代的 9,600+ 规则安全扫描器

> 项目地址：https://github.com/Pantheon-Security/medusa

## 为什么 AI Agent 安全需要专用扫描器？

传统的 SAST 工具（Semgrep、CodeQL）可以找到 SQL 注入和 XSS，但无法理解 AI Agent 特有的攻击面：

- **MCP Server 工具投毒**：恶意的 MCP 工具 schema 可以污染 Agent 的工具选择
- **Repo Poisoning**：weaponized AI editor 配置（Cursor、Claude Code、Cline）可以植入后门
- **Prompt Injection**：通过 RAG 管道注入恶意上下文，操纵 Agent 行为
- **Memory Poisoning**：持久化记忆中的错误信息污染长期决策

MEDUSA 的诞生就是为了填补这个空白。

## 核心能力一览

| 类别 | 规则数 | 检测内容 |
|------|--------|---------|
| Prompt Injection | 800+ | 直接/间接注入、越狱、角色操纵 |
| MCP Server 安全 | 400+ | 工具投毒、schema 投毒、ATPA、采样注入、rug-pull |
| Repo Poisoning | 150+ | weaponized AI 编辑器配置、IDE 后门 |
| RAG 安全 | 300+ | 向量注入、文档投毒、多租户隔离缺失 |
| Agent 安全 | 500+ | 过度授权、记忆投毒、人类授权绕过 |
| Model 安全 | 400+ | 不安全加载、检查点暴露、对抗攻击 |
| Supply Chain | 350+ | 依赖混淆、typosquatting、lock 文件后门 |
| 传统 SAST | 1,400+ | SQL 注入、XSS、命令注入、 secrets |

总计 **9,600+ 检测规则**，覆盖 AI/ML 应用、LLM Agent、MCP 服务器、RAG 管道和传统代码。

## 杀手级功能：`medusa scan --git`

最实用的功能是直接扫描任意 GitHub 仓库，无需本地安装：

```bash
medusa scan --git user/repo
```

这对于安全团队审计 AI 供应链特别有价值——不需要把代码 clone 下来，扫描器会直接访问仓库。

## Repo Poisoning 检测：28+ AI 编辑器类型

随着 AI Coding 工具普及，攻击者开始在 AI 编辑器配置文件中植入恶意代码。MEDUSA 检测以下场景：

- **CurXecute**：Cursor 配置中的命令注入
- **Clinejection**：Cline 插件的恶意工具定义
- **CAMOLEAK**：敏感数据通过编辑器配置泄露
- **ToxicSkills**：有害技能定义

覆盖 28+ AI 编辑器配置文件类型，这是传统安全工具完全忽略的攻击面。

## Agent Protocol 安全

MEDUSA 还包含 **UCP、AP2、ACP 漏洞检测（91 条规则）**，这些是新兴的 Agent 间通信协议。当前热度最高的 MCP（Model Context Protocol）就在这个类别中。

## 技术规格

- **版本**：v2026.5.3（2026-04-08）
- **语言**：Python（99.9%）+ Dockerfile + Ruby
- **许可**：AGPL-3.0
- **创建时间**：2025-11-15
- **最新提交**：2026-04-08
- **贡献者**：2 人（主要贡献者 rosschurchill）
- **发布数**：25 个
- **PyPI 下载**：11,500+

## FP Filter：96.8% 误报过滤率

大规模扫描时误报是致命问题。MEDUSA 内置 **514 条 FP Filter 模式**，将误报率降低 96.8%。这是通过大量真实场景测试积累的规则。

## 与 OWASP Top 10 for LLM 2025 对齐

MEDUSA 的规则映射到：
- OWASP Top 10 for LLM Applications 2025
- MITRE ATLAS（对抗性威胁景观）
- 200+ CVE 检测（包含 Log4Shell、Spring4Shell、XZ Utils backdoor、LangChain RCE、MCP RCE）

## 笔者的判断

MEDUSA 的价值在于它**填补了 AI Agent 安全工具的空白**。传统安全扫描器不理解 AI Agent 的攻击面，而通用 AI 安全工具（如 Bandit）又太浅。

特别是 `medusa scan --git` 功能让安全团队可以零成本审计 AI 供应链——不需要 clone 代码，不需要配置 CI/CD，直接在 PyPI 安装后扫任意仓库。

当前只有 252 Stars，属于早期项目，但方向正确。随着 AI Coding 工具的普及，Repo Poisoning 这类攻击面会越来越常见。提前布局这类工具的安全团队会占优势。

---

**引用来源**：
- MEDUSA 官方仓库：https://github.com/Pantheon-Security/medusa
- MEDUSA 官网：https://pantheonsecurity.io
- OWASP Top 10 for LLM Applications 2025