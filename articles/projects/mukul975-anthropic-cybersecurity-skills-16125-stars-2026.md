# mukul975/Anthropic-Cybersecurity-Skills 16125⭐ 2026

> **`mukul975/Anthropic-Cybersecurity-Skills`** 是 2026 年 2 月 25 日开源的社区项目（⚠️ 与 Anthropic PBC 无关），GitHub 16,125 ⭐ / Apache-2.0。它把 **754 个生产级 cybersecurity skills** 装进一个仓库，跨 **26 个安全域**，映射到 **5 个行业框架**（MITRE ATT&CK v19.1 / NIST CSF 2.0 / MITRE ATLAS v5.4 / MITRE D3FEND v1.3 / NIST AI RMF 1.0），遵循 [agentskills.io](https://agentskills.io) 开放标准，**兼容 Claude Code、GitHub Copilot、26+ AI 平台**——是 **R429 Anthropic 内部 CLUE 平台（"bittersweet lesson" 在 SOC 落地）**的**开源生态层对应物**。

## 与 R429 Article 的对位关系

R429 Article 揭示了 Anthropic Detection Platform Engineering 团队用 Claude Code 搭建 **CLUE** 检测响应平台的内部实践——它的核心是**"给 Claude 工具 + 目标，让它自己决定调查路径"**。但内部 CLUE 平台是 Anthropic 专属，外部团队无法直接复用。

**`Anthropic-Cybersecurity-Skills` 是把 CLUE 的核心思想（"用 AI Agent 驱动网络安全"）开源化为可直接导入 AI Agent 的 skills 库**——任何使用 Claude Code、Copilot 或其他兼容平台的团队，clone 这个仓库、让 Agent 指向它，就能让 AI 获得**资深安全分析师级别的领域知识**。

| 维度 | R429 Article (CLUE) | 本 Project (Skills Library) |
|------|---------------------|------------------------------|
| 性质 | Anthropic 内部 SOC 平台 | 社区开源 skills 库 |
| 焦点 | 工具架构 + bitter lesson 哲学 | 754 个结构化 skills + 5 框架映射 |
| 适用对象 | 仅 Anthropic Detection 团队 | 任何用 Claude Code / Copilot 的安全团队 |
| 知识来源 | 团队自身工程经验 | MITRE / NIST 等行业标准框架 |
| 核心命题 | "工具 + 目标 > 写死 playbook" | "把行业标准结构化到 Agent 可消费" |
| 部署模式 | 内部云服务 | Git clone + 集成到 Agent runtime |

**两者是同一思想的"内部实现 ↔ 外部开源"对位**——一个验证了"AI Agent 驱动安全"的可行性，另一个让任何团队都能用上同样的能力。

## 4 层配对强度判定（R375 #34 协议）

### Layer 1: Cluster 标签共享（基础 ⭐⭐）
- R429 Article 在 `articles/harness/` 集群（Anthropic-internal 工程实践）
- Project 在 `articles/projects/` 标签下，主题同样属于 Anthropic 工程生态
- 共享 cluster ⭐⭐

### Layer 2: SPM 关键词字面级共享（升级 ⭐⭐⭐⭐⭐）
6 个关键词同时出现在 R429 Article 和 Project README：
- `cybersecurity` — R429 标题 2 次 + Project "Cybersecurity Skills" 全名
- `claude-code` — R429 提到 "Claude Code" + Project 兼容 Claude Code
- `threat-hunting` — R429 提到 "hunting for suspicious patterns" + Project topics 含 `threat-hunting`
- `mcp` — R429 提到 CLUE 通过 tool use 集成内部系统 + Project topics 含 `mcp`
- `security-automation` — R429 量化 12K queries + 27K tool calls 自动化 + Project topics 含 `security-automation`
- `mitre-attack` — R429 提到 MITRE 等标准 + Project 明确映射到 MITRE ATT&CK v19.1
- **SPM 字面级 6 关键词同时命中** → ⭐⭐⭐⭐⭐

### Layer 3: GitHub topics target-ecosystem 命中（升级 tiebreaker ⭐⭐⭐⭐⭐）
- `topics: ['ai-agents', 'claude-code', 'cloud-security', 'cybersecurity', 'devsecops', 'ethical-hacking', 'incident-response', 'infosec', 'llm', 'malware-analysis', 'mcp', 'mitre-attack', 'nist-csf', 'osint', 'penetration-testing', 'red-team', 'security', 'security-automation', 'threat-hunting', 'threat-intelligence']`
- **直接命中**: `claude-code`、`mcp`、`ai-agents` — 都是 R429 主题
- **间接命中**: `threat-hunting`（R429 "hunting for suspicious patterns"）、`incident-response`（R429 "detection and response"）
- **`Hermes Agent` compatible** 标识在 README 显式标注 — 这是 R367 #27 + R375 #36 双协议命中信号

### Layer 4: 维度互补 ≠ 维度重叠（确认 ⭐⭐⭐⭐⭐）
- 抽象 ↔ 实现：R429 描述内部平台的工程哲学与架构；Project 把这哲学落地为"754 个可导入 Agent 的 skills"
- 闭源 ↔ 开源：R429 CLUE 内部专属；Project 公开给所有 Claude Code 用户
- 内 ↔ 外：R429 Anthropic 内部实践；Project 第三方社区项目
- 同协议层互证：R429 bitter lesson（"给工具 + 目标"）↔ Project 提供具体 skills 实现

**判定**：⭐⭐⭐⭐⭐ 4 层全中（与 R375 nanoclaw / R383 claude-mem / R397 skillshare / R401 antigravity-skills / R406 awesome-claude-code-subagents / R410 claude-code-security-review 同一强度）

## 项目核心结构

### 26 个安全域 + 5 框架映射

| 框架 | 版本 | 覆盖范围 | 映射目标 |
|------|------|---------|---------|
| MITRE ATT&CK | v19.1 | 15 tactics · 286 techniques | 攻击者行为与 TTP |
| NIST CSF 2.0 | 2.0 | 6 functions · 22 categories | 组织安全姿态 |
| MITRE ATLAS | v5.4 | 16 tactics · 84 techniques | AI/ML 对抗威胁 |
| MITRE D3FEND | v1.3 | 7 categories · 267 techniques | 防御性反制措施 |
| NIST AI RMF | 1.0 | 4 functions · 72 subcategories | AI 风险管理 |

**一个 skill 同时映射 5 个框架的工程价值**："一鱼五吃"——一次创建 skill，自动获得 ATT&CK、CSF、ATLAS、D3FEND、AI RMF 五个合规 checkbox。

### 单一 skill 跨 5 框架实例

| Skill | ATT&CK | NIST CSF | ATLAS | D3FEND | AI RMF |
|-------|--------|----------|-------|--------|--------|
| `analyzing-network-traffic-of-malware` | T1071 | DE.CM | AML.T0047 | D3-NTA | MEASURE-2.6 |

### agentskills.io 开放标准

每个 skill 遵循 [agentskills.io](https://agentskills.io) 开放标准，**与 Claude Code、GitHub Copilot、26+ AI 平台兼容**——这是 R357 协议"非工程师 Agent 构建" cluster 中的"协议层"实现：让 skill 真正"工具无关"。

## 与 R429 CLUE 的 5 个具体对位点

1. **"内部上下文" vs "行业标准"**：R429 CLUE 强项是组织内上下文（Slack/代码/数据仓库）；本项目强项是**行业标准上下文**（MITRE/NIST 框架）。两者结合 = 任何团队都能用 CLUE 思路 + 行业标准。

2. **"工具 + 目标" vs "结构化 skills"**：R429 哲学是"别写 playbook"；本项目给的是"别从 0 写 skills"——直接消费 754 个已有的、跨 5 框架映射的结构化 skills。

3. **"CLUE Triage" vs "triage 域 skills"**：R429 CLUE Triage 自动 enrich 告警；本项目 `incident-response` + `threat-intelligence` 域的 skills 涵盖 triage 知识。

4. **"Bitter lesson 多策略并行" vs "26+ 平台"**：R429 跑多策略对比结果；本项目让同一组 skills 在 Claude Code / Copilot / 其他平台都能跑，**自然形成"多平台并行"**。

5. **"持续学习" vs "持续更新"**：R429 把 transcript 沉淀为组织记忆；本项目作为社区项目，**通过 GitHub PR 持续追加新 skills**——社区版"组织记忆"。

## 局限与注意事项

1. **⚠️ 社区项目**：README 明确标注 "This is an independent, community-created project. Not affiliated with Anthropic PBC" — 不是 Anthropic 官方项目。Apache-2.0 license 清洁。
2. **质量参差**：754 个 skills 数量极大，单个 skill 深度可能不如 CLUE 内部平台对自家场景的优化。
3. **依赖 Claude Code 兼容层**：不是所有 AI 平台都完整支持 agentskills.io 标准——用前先验证目标平台兼容性。
4. **框架版本固定**：映射到 ATT&CK v19.1 / NIST CSF 2.0 等特定版本，行业标准更新后项目可能滞后。

## 元数据

| 字段 | 值 |
|------|-----|
| **Repository** | https://github.com/mukul975/Anthropic-Cybersecurity-Skills |
| **Stars** | 16,125 ⭐ |
| **License** | Apache-2.0 |
| **创建日期** | 2026-02-25 |
| **最后更新** | 2026-06-17 |
| **Skills 总数** | 754 |
| **安全域** | 26 |
| **框架映射** | 5 (MITRE ATT&CK + NIST CSF + MITRE ATLAS + MITRE D3FEND + NIST AI RMF) |
| **兼容平台** | 26+ (Claude Code、GitHub Copilot、Hermes Agent 等) |
| **Agent 标准** | [agentskills.io](https://agentskills.io) |
| **配对 Article** | `articles/harness/anthropic-cybersecurity-clue-detection-platform-bitter-lesson-2026.md` (R429) |
| **Pair 强度** | ⭐⭐⭐⭐⭐ (4-way SPM 满中) |
| **License 验证** | GitHub API spdx_id: Apache-2.0 (2026-06-18 verified) |
