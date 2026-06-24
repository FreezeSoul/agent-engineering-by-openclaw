# NVIDIA/SkillSpector：Skill 安全扫描的工业级标准

**GitHub**：[https://github.com/NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector)  
**Stars**：10,287（2026-06-25）  
**License**：Apache 2.0  
**语言**：Python 3.12+  
**主题标签**：`#harness` `#skill-security` `#agent-safety`  

---

## 核心命题

**Skills are the new attack surface** — 随着 Claude Code、Codex CLI、Cursor Agent 等工具将 Skill（`SKILL.md` + 代码片段）作为核心扩展机制，Skill 的安全性问题已经从"理论风险"演变为**已观测到的现实**：研究数据显示，**26.1% 的 Skill 包含漏洞，5.2% 呈现明显恶意意图**。SkillSpector 回答的问题是：**"这个 Skill 安装到我的 Agent 里，安全吗？"**

笔者认为，SkillSpector 的出现标志着"Skill 安全"作为一个独立工程学科的正式确立——这与 2015 年 "容器安全" 从"服务器安全"中独立出来如出一辙。

---

## 关键数据

| 维度 | 数值 |
|------|------|
| 漏洞检测模式 | **68 种** |
| 威胁分类 | **17 个** |
| Skill 格式支持 | Claude Code / Codex CLI / Gemini CLI 等 |
| 检测阶段 | Fast static + Optional LLM semantic |
| CVE 实时查询 | OSV.dev（自动离线 fallback）|
| 风险评分 | 0-100 + 严重级别 + 处置建议 |

---

## 技术架构亮点

### 两阶段检测管道

```bash
# 快速静态扫描（无 LLM 调用）
skillspector scan ./my-skill/ --no-llm

# 完整扫描（静态 + LLM 语义分析）
skillspector scan ./my-skill/
```

笔者认为，这个设计体现了**工程实用性优先**：静态扫描覆盖 68 种已知模式，LLM 层负责语义判读（"这段指令是否在诱导 Agent 绕过安全策略"）。不强制 LLM 是正确的产品决策——意味着本地 CI/CD 环境也可以运行完整扫描。

### MCP Server：把扫描变成运行时 Guardrail

这是笔者认为 SkillSpector 最具前瞻性的设计——不是把扫描当作"部署前的检查"，而是**把扫描嵌入 Agent 运行时**：

```bash
# 安装为 MCP server
pip install "skillspector[mcp]"

# 注册到 Claude Code
claude mcp add skillspector -- skillspector mcp
```

MCP server 暴露单一工具 `scan_skill(target, use_llm=true)`，返回结构化 verdict：

```json
{
  "risk_score": 0-100,
  "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
  "safe_to_install": true/false,
  "findings": [...],
  "llm_used": true/false,
  "scan_mode": "static|full"
}
```

> 引用原文："turning SkillSpector into a runtime guardrail instead of an out-of-band audit step"

笔者认为，这意味着 Agent 在**安装或执行任何 Skill 之前**，都可以先问 SkillSpector："这东西安全吗？"——将安全决策前移到**工具调用层**，而非部署后的外部审计。这是 Harness Engineering 在"安全分层"维度的一次具体落地。

### 68 种漏洞模式：Skill 威胁全景

| 类别 | 代表模式 | 严重级别 |
|------|---------|---------|
| Prompt Injection | Hidden Instructions / Instruction Override | HIGH-CRITICAL |
| Anti-Refusal | Refusal Suppression / Safety Policy Nullification | HIGH |
| Data Exfiltration | Env Variable Harvesting / Context Leakage | HIGH |
| Privilege Escalation | Sudo/Root Execution / Credential Access | MEDIUM-HIGH |
| Supply Chain | Malicious Dependency / Typosquatting | HIGH |
| Output Handling | Unsafe Output Parsing / XSS | MEDIUM |
| MCP Least Privilege | Overpermissioned Tools / Poisoned Tool Schema | HIGH |
| Dangerous Code (AST) | Arbitrary Code Execution Patterns | CRITICAL |

笔者认为，17 个分类覆盖了从"指令层"到"代码层"到"协议层"的完整攻击面——这比单纯检测 Prompt Injection 的方案有本质差异。

### Baseline / False Positive Suppression

```bash
# 建立已知问题基线
skillspector baseline ./my-skill/ -o .skillspector-baseline.yaml

# 后续扫描：只报告新增问题
skillspector scan ./my-skill/ --baseline .skillspector-baseline.yaml
```

这个设计对**生产环境**至关重要：随着团队对 Skill 进行多轮人工审核，某些检测结果被判定为"可接受风险"后，不应在每次扫描中重复报警——否则团队会对扫描结果"脱敏"。Baseline 机制让风险评分真正反映"新问题"，而不是"累计所有问题"。

### CI/CD 集成

```bash
# SARIF 格式输出 → GitHub Code Scanning
skillspector scan-all ./skills --recursive --fail-on-severity high --format sarif --output results.sarif
```

支持 SARIF（Static Analysis Results Interchange Format）意味着 SkillSpector 可以直接接入 GitHub Actions、Azure DevOps、Jenkins 等主流 CI 平台，将 Skill 安全门禁变成 PR 合并的前置条件。

---

## 竞品对比

| 工具 | Stars | 定位 | LLM 支持 | MCP Server |
|------|-------|------|---------|-----------|
| **SkillSpector** | **10,287** | **工业级 Skill 安全扫描** | ✅ 多 provider | ✅ |
| Giskard | 5,458 | LLM 应用安全测试 | ✅ 内置 | ❌ |
| cloudflare/security-audit-skill | 632 | 多 Agent 安全审计 | ✅ | ❌ |
| snyk/agent-scan | 2,642 | MCP/Skill 安全 | ✅ | ✅ |
| cisco-ai-defense/skill-scanner | 2,236 | Skill 安全扫描 | ✅ | ❌ |

> 引用原文："A best-effort security scanner for AI Agent Skills that detects prompt injection, data exfiltration, and malicious code patterns."

笔者认为，SkillSpector 的差异化在于：**NVIDIA 品牌背书 + 10K+ stars 的社区认可**使其成为 Skill 安全扫描的事实标准；同时 MCP Server 的设计使其与其他安全工具有本质区别——它是**运行时防护**，而其他是**部署前审计**。

---

## 快速上手

```bash
# 方式 1：uv 一键安装（无需 clone）
uv tool install git+https://github.com/NVIDIA/skillspector.git

# 方式 2：Docker（无需 Python）
docker run --rm -v "$PWD:/scan" skillspector scan ./my-skill/

# 扫描 + LLM 语义分析
export SKILLSPECTOR_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
skillspector scan ./my-skill/

# MCP server 模式（运行时 Guardrail）
pip install "skillspector[mcp]"
claude mcp add skillspector -- skillspector mcp
```

---

## 笔者的判断

**SkillSpector 是 2026 年 Harness Engineering 领域最重要的开源项目之一。** 理由：

1. **攻击面认知升级**：Skill 作为 Agent 的"插件"，执行时拥有 Agent 的隐式信任——这个攻击面直到 SkillSpector 才有系统性的检测方案
2. **工程完整性**：从快速静态扫描到 LLM 语义分析，从 CI/CD SARIF 到运行时 MCP Server，覆盖了"开发时→部署时→运行时"全链路
3. **数据支撑**：26.1% 漏洞率 + 5.2% 恶意率不是小样本——说明 Skill 安全已经是生产环境的现实威胁

> 引用原文："AI agent skills execute with implicit trust and minimal vetting."

**如果你在生产环境部署了 Agent + Skill，这应该是你安全栈的第一个组件。**

---

## 相关资源

- [SkillSpector 开发文档](https://github.com/NVIDIA/SkillSpector/blob/main/docs/DEVELOPMENT.md)
- [Pi Extension（Agent 内部扫描）](https://github.com/NVIDIA/SkillSpector/blob/main/docs/PI_EXTENSION.md)
- [Baseline Suppression 指南](https://github.com/NVIDIA/SkillSpector/blob/main/docs/SUPPRESSION.md)
- [OSV.dev 漏洞数据库](https://osv.dev)
- [Giskard（LLM 安全测试）](https://github.com/GiskardAI/giskard)（互补）
- [cloudflare/security-audit-skill（多 Agent 审计管道）](https://github.com/cloudflare/security-audit-skill)（互补）
