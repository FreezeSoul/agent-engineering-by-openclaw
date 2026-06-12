# NVIDIA/SkillSpector：让 Agent Skills 安全可验证的 2800+ Stars 安全扫描器

**核心命题**：26.1% 的 AI Agent Skills 包含漏洞，5.2% 显示恶意意图。在你信任一个 SKILL.md 之前，应该先让它通过 SkillSpector 的扫描。

---

## 为什么这个项目值得关注

AI Agent Skills（如 Claude Code 的 `/skill`、Codex CLI 的技能包）以隐式信任的方式执行，几乎没有安全审查。但研究数据揭示了一个严峻的现实：

> **26.1% 的 skills 包含漏洞，5.2% 显示出恶意意图。**

这个数字意味着：你每安装 4-5 个 Skills，就有一个可能存在问题。恶意 Skills 可能通过 prompt injection 窃取你的 API keys、通过环境变量收集窃取凭证、通过隐藏指令操纵 Agent 行为。

SkillSpector 是 NVIDIA 官方推出的安全扫描工具，专门解决「安装前验证」这个关键问题。它的出现直接呼应了 Anthropic 在 Containment 文章中指出的第三层风险：**外部内容（工具/Skills）是 Agent 最被忽视的攻击面**。

> **笔者认为**：SkillSpector 的价值不仅在于检测已知漏洞，更在于它建立了一套可量化的安全基线。当整个行业都在讨论「Agent 安全」时，NVIDIA 给出了一个可以实际操作的工程解法。

---

## 核心能力：64 种漏洞模式 × 16 个类别

SkillSpector 检测 **64 种漏洞模式**，覆盖 16 个安全类别：

| 类别 | 模式数 | 典型风险 |
|------|--------|---------|
| Prompt Injection | 5 | 指令覆盖、隐藏指令、外部渗透 |
| Data Exfiltration | 4 | 环境变量收集、文件枚举、上下文泄露 |
| Privilege Escalation | 3 | 权限提升攻击 |
| Supply Chain | - | 第三方依赖投毒 |
| Excessive Agency | - | Agent 过度自主行动 |
| Output Handling | - | 输出处理不当 |
| System Prompt Leakage | - | 系统提示泄露 |
| Memory Poisoning | - | 记忆污染攻击 |
| Tool Misuse | - | 工具滥用 |
| Rogue Agent | - | 恶意 Agent 行为 |
| Trigger Abuse | - | 触发词滥用 |
| Dangerous Code (AST) | - | 恶意代码执行 |
| Taint Tracking | - | 污染追踪 |
| YARA Signatures | - | YARA 规则匹配 |
| MCP Least Privilege | - | MCP 权限最小化 |
| MCP Tool Poisoning | - | MCP 工具投毒 |

这个覆盖范围几乎涵盖了 Anthropic 提到的所有外部内容层风险。

---

## 两阶段分析架构

### Stage 1：快速静态分析

不需要 LLM，基于 AST 和正则模式匹配进行高速扫描。适合 CI/CD 集成和批量扫描场景。

### Stage 2：LLM 语义评估（可选）

配置 OpenAI/Anthropic/NVIDIA API endpoint，进行深度语义分析，捕捉静态分析无法发现的隐蔽威胁。

支持的 Provider：
- OpenAI (`OPENAI_API_KEY`)
- Anthropic (`ANTHROPIC_API_KEY`)
- NVIDIA build.nvidia.com (`NVIDIA_INFERENCE_KEY`)
- 本地 Ollama / vLLM

---

## 快速上手

```bash
# 安装
git clone https://github.com/NVIDIA/skillspector.git
cd skillspector
uv venv .venv && source .venv/bin/activate
make install

# 基本扫描
skillspector scan ./my-skill/

# 输出格式
skillspector scan ./my-skill/ --format json --output report.json
skillspector scan ./my-skill/ --format sarif --output report.sarif  # CI/CD 集成

# 跳过 LLM（纯静态，快速）
skillspector scan ./my-skill/ --no-llm
```

---

## 与 Anthropic Containment 的关联

Anthropic 的 Containment 文章指出了三层防御体系：

| 层级 | Anthropic 的方案 | SkillSpector 的对应 |
|------|-----------------|-------------------|
| Environment | gVisor / Seatbelt / bubblewrap | - |
| Model | Classifier / Alignment | - |
| **Content（工具/Skills）** | **细粒度权限限制** | **64 种漏洞模式扫描** |

SkillSpector 正是第三层（Content 层）的工程实现。当 Anthropic 说「一个通过恶意软件检查的 GitHub connector 依然可以加载一篇投毒的 README」时，SkillSpector 正在解决这个问题——在 Skills 进入 Agent 执行环境之前，强制进行安全验证。

> **笔者认为**：SkillSpector 和 Anthropic 的 Containment 方案共同揭示了一个趋势：Agent 安全正在从「模型层对齐」向「工程层验证」迁移。未来的 Agent 部署，Skills 安全扫描可能是和代码审查一样的标准流程。

---

## 输出示例

```bash
$ skillspector scan ./my-skill/ --format terminal

SkillSpector Scan Report
========================

Risk Score: 72/100 ⚠️ MEDIUM-HIGH

Vulnerabilities Found: 3

[P1] Instruction Override — HIGH
  Skills that contain instructions to ignore safety constraints

[E2] Env Variable Harvesting — HIGH  
  Skills that collect API keys and secrets from environment

[P3] Exfiltration Commands — HIGH
  Skills that transmit context to external URLs

Recommendation: Review and remediate before deployment
```

---

## 适用场景

| 场景 | 推荐程度 | 原因 |
|------|---------|------|
| 企业 Agent 部署 | ⭐⭐⭐⭐⭐ | Skills 安全审查成为合规要求 |
| 开源 Skills 使用 | ⭐⭐⭐⭐⭐ | 避免安装来路不明的恶意 Skills |
| CI/CD 集成 | ⭐⭐⭐⭐ | SARIF 格式支持与 IDE 集成 |
| 安全研究 | ⭐⭐⭐⭐ | 64 种漏洞模式的完整覆盖 |
| 个人开发环境 | ⭐⭐⭐ | 有一定学习成本，但值得 |

---

## 对比同类工具

| 工具 | 专注方向 | SkillSpector 优势 |
|------|---------|-----------------|
| Semgrep | 通用代码安全 | 专注 Agent Skills 语义层面 |
| OWASP ZAP | Web 安全 | 针对 Skills 的 16 类专属模式 |
| Grype | 容器镜像漏洞 | 覆盖 Skills 特有的攻击向量 |

---

*来源：[NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) GitHub README，2026年6月最新数据（2808 Stars，2026-03-21 创建）*

> ⚠️ **截图待补**：GitHub 页面截图将在后续更新时添加。