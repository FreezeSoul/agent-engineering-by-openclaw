# mulukul975/Anthropic-Cybersecurity-Skills：让 AI Agent 具备安全分析师的专业判断力

>🔴 **来源**：[github.com/mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)
> ⭐ **Stars**：14,718（2026年6月）
> 📜 **License**：Apache 2.0
> 🏷️ **归档**：Agent Skills / Harness Engineering

---

## 核心命题

你给 AI Agent 一份可疑的内存转储，它知道该运行哪个 Volatility3 插件、哪个 Sigma 规则能捕获 Kerberoasting、如何跨三个云服务商追踪入侵范围吗？**答案是「不知道」——除非你给它这些 Skill**。Anthropic-Cybersecurity-Skills 是目前唯一将 754 个结构化网络安全技能映射到五大行业框架（MITRE ATT&CK、NIST CSF 2.0、MITRE ATLAS、D3FEND、NIST AI RMF）的开源 Skill库，使 AI Agent 能够在安全场景中执行专业级分析工作流。

---

## 为什么值得推荐

### 1. 它解决了一个真实的 Agent 能力缺口

AI Agent 擅长写代码、搜索网页，但缺乏**资深安全分析师的结构化决策流程**——什么时候用什么技术、检查哪些前置条件、如何逐步执行、如何验证结果。这种差距导致 Agent 在安全场景中只能充当「搜索引擎」，而无法成为真正的「分析助手」。

这个项目直接填补了这个空白：不是提供脚本或Payload集合，而是为 AI Agent 构建了一套**可执行的专家级工作流知识库**。

### 2. 五框架映射的独特价值

这不是简单的标签映射，而是**结构化元数据的交叉引用**：

| 框架 | 版本 | 覆盖范围 |
|------|------|---------|
| MITRE ATT&CK | v19.1 | 15 tactics · 286 techniques |
| NIST CSF 2.0 | 2.0 | 6 functions · 22 categories |
| MITRE ATLAS | v5.4 | 16 tactics · 84 techniques（AI/ML 对抗威胁）|
| MITRE D3FEND | v1.3 | 7 categories · 267 techniques（防御对策）|
| NIST AI RMF | 1.0 | 4 functions · 72 subcategories（AI 风险管理）|

举例来说，`analyzing-network-traffic-of-malware` 这个 Skill 同时映射到：
- ATT&CK: T1071（Application Layer Protocol）
- NIST CSF: DE.CM（Continuous Monitoring）
- ATLAS: AML.T0047
- D3FEND: D3-NTA（Network Traffic Analysis）
- NIST AI RMF: MEASURE-2.6

**一个 Skill，五个合规框架同时勾选**。对于需要满足多种合规要求的企业安全团队，这意味着 Agent 可以在同一个 Skill 执行中同时满足多个监管框架的要求。

### 3. agentskills.io 标准：跨平台互操作

这个项目采用 [agentskills.io](https://agentskills.io) 开放标准，每个 Skill 使用 YAML frontmatter 声明元数据，Markdown 文件包含逐步执行指南。这意味着：

```
✅ 兼容 Claude Code（直接使用）
✅ 兼容 GitHub Copilot
✅ 兼容 OpenAI Codex CLI
✅ 兼容 Cursor
✅ 兼容 Gemini CLI
✅ 兼容任何 agentskills.io 标准平台
```

添加方式只需一行命令：
```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills
```

**笔者认为**：agentskills.io 标准的重要性被低估了。当前 Agent 生态中，每个平台（Claude Code、Copilot、Cursor）都有自己 的 Skill 定义方式，互不兼容。agentskills.io 作为开放标准的价值在于**让 Skill 成为可移植的知识单元**——一份 Skill可以在任何兼容平台上使用，不需要针对每个平台单独转换。

### 4. 26 个安全领域，754 个 Skill

覆盖的安全领域包括（但不限于）：

- **云安全**（60 Skills）：AWS/Azure/GCP 加固、CSPM、云取证
- **威胁狩猎**（55+ Skills）：假说驱动狩猎、IoC 关联
- **DFIR**（数字取证与事件响应）：内存取证、磁盘取证、网络取证
- **渗透测试**：漏洞利用、权限维持、横向移动
- **Red Team**：社会工程、攻防对抗

---

## 技术原理：Skill 的结构设计

每个 Skill 遵循 agentskills.io 标准的 YAML frontmatter + Markdown 结构：

```yaml
---
name: analyzing-network-traffic-of-malware
mitre_attack:
  - T1071  # Application Layer Protocol
  - T1048  # Exfiltration Over Alternative Protocol
nist_csf:
  - DE.CM
  - PR.AC
domain: threat_hunting
difficulty: intermediate
prerequisites:
  - network_capture_available
  - wireshark_or_similar_tool
steps:
  - 检查流量元数据（持续时间、字节数、协议分布）
  - 识别异常 DNS 查询（长域名、DGA 模式）
  - ...
---
```

这种结构使得：
1. **Agent 可以在亚秒级时间内通过 YAML声明发现 Skill**（不需要解析整个文件）
2. **每个 Skill 编码了真实从业者的工作流程**，不是生成的摘要
3. **元数据使得 Skill 可以被精确检索和组合**

---

## 与 Agent Harness 的关联

这个项目与 BUILD 2026 的 Agent Harness 主题形成有意义的互补：

- **AgentSkillsProvider**（Harness 内置 Provider）：Microsoft 的 Harness 架构已经内置了 Skill 发现和执行机制
- **这个项目**提供了 754 个可以在 Harness架构中直接使用的结构化 Skill

换句话说：Foundry Hosted Agents + AgentSkillsProvider + Anthropic-Cybersecurity-Skills = **一个可以执行专业安全分析的生产级 Agent 系统**。

对于安全团队的 Agent 落地，这个组合提供了：
1. ** Harness 层**（Microsoft）：上下文管理、审批流程、状态持久化
2. **Skill库**（这个项目）：专家级安全分析工作流
3. **模型层**：Anthropic Claude 模型（使用 Claude Code 时）

---

## 使用场景

### 场景1：安全事件响应自动化

当 SOC 收到告警时，可以启动一个 Agent，让它：
1. 使用 `investigating-suspicious-process-creation` Skill 进行进程分析
2. 使用 `analyzing-network-traffic-of-malware` Skill 进行流量分析
3. 使用 `identifying-kerberoasting-activity` Skill 验证 Kerberoasting IoC
4. 每个 Skill 的元数据自动生成合规报告（一次执行满足 ATT&CK + NIST CSF + ATLAS + D3FEND + AI RMF）

### 场景 2：红队行动的 Agent 辅助

Red Team 成员可以使用 Agent 执行：
1. `scoping-cloud-breach-across-providers` — 跨云服务商定界
2. `identifying-persistence-via-windows-scheduled-tasks` — 持久化机制识别
3. `executing-lateral-movement-through-wmi` — 横向移动执行指引

### 场景 3：合规审计自动化

满足多种监管框架要求的 Agent 系统：
1. `auditing-access-control-policies` — 同时映射到 NIST CSF PR.AC + ATT&CK TA0001
2. `detecting-data-exfiltration-attempts` — 同时映射到 D3FEND D3-NTA + ATT&CK T1048

---

## 局限性

1. **Skill 质量依赖贡献者**：754 个 Skill 的覆盖广度 vs深度需要用户自行评估
2. **非官方项目**：明确标注 "Not affiliated with Anthropic PBC"，意味着不是官方维护
3. **MITRE 映射的维护滞后**：当 MITRE 发布新版本时，Skill 需要手动更新映射
4. **Skill 发现机制依赖平台**：agentskills.io 标准目前采纳率还不够高，跨平台兼容性是理论值而非实际值

---

## 结论

Anthropic-Cybersecurity-Skills 是一个**填补 Agent 安全能力缺口**的项目。它不提供新的模型能力或新的执行框架，而是**为 Agent 提供结构化的专家知识**。对于正在构建安全分析 Agent 的团队，这个项目值得认真评估——它可能是目前最完整的开源安全领域 Skill 库。

关键判断是：**Skill 驱动的 Agent 时代正在到来**，而这个项目是 Skill 生态中一个值得关注的高价值节点。

---

**执行流程**：
1. **理解任务**：需要为 mulukul975/Anthropic-Cybersecurity-Skills 写 Project 推荐
2. **规划**：fetch GitHub README 获取详细信息，评估 Stars 和工程价值
3. **执行**：web_fetch 获取项目详情，按 Project 写作规范完成写作
4. **返回**：Project 文件写入 articles/projects/
5. **整理**：关联分析（与 Agent Harness 的互补关系）

**调用工具**：
- `web_fetch`: 1次（获取 README）
- `write`: 1次（Project 文件）