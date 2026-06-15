# Anthropic-Cybersecurity-Skills：给 AI Agent 一套网络安全专家级技能包

## 核心命题

安全分析 Agent 为什么普遍弱？因为它缺乏真正的领域知识——不是不会分析，而是不知道"该用哪个 Volatility3 插件"、不知道"哪些 Sigma 规则能 catch Kerberoasting"、不知道怎么跨云厂商 scope 一个 breach。**Anthropic-Cybersecurity-Skills** 解决了这个问题：754 个结构化网络安全技能，让任何 AI Agent 获得高级安全分析师的判断力。

> "A junior analyst knows which Volatility3 plugin to run on a suspicious memory dump, which Sigma rules catch Kerberoasting, and how to scope a cloud breach across three providers. Your AI agent doesn't — unless you give it these skills."
>
> — [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)，README

---

## 为什么值得推荐

### 754 个 Skills：行业最大规模的开源 Skills 库

这个项目最直观的价值是**规模**：754 个生产级网络安全技能，覆盖 26 个安全领域。每个 Skill 都有明确的任务定义、输入输出规范和执行条件——不是 Prompts 的集合，而是可直接执行的技能包。

笔者认为，754 这个数字的意义不只是量变，而是**领域覆盖的质变**：从网络流量分析（analyzing-network-traffic-of-malware）到云安全事件调查（cloud-breach-scoping），从威胁情报充实（threat-intel-enrichment）到内存取证（volatility3-memory-analysis），安全分析的完整工作流中每一个原子能力都有对应的 Skill。

### 五大框架映射：一张 Skill 表，五个合规框架打勾

这个项目最独特的设计是**每个 Skill 都映射到 5 个行业标准框架**：

| 框架 | 覆盖范围 | 技能数量 |
|------|---------|---------|
| MITRE ATT&CK | 15 tactics · 286 techniques | 754/754 |
| NIST CSF 2.0 | 6 functions · 22 categories | 全覆盖 |
| MITRE ATLAS | 16 tactics · 84 techniques | AI/ML 对抗 |
| MITRE D3FEND | 7 categories · 267 techniques | 防御反制 |
| NIST AI RMF | 4 functions · 72 subcategories | AI 风险管理 |

> "One skill, five compliance checkboxes."
>
> — README

笔者认为，这个设计的工程价值在于**合规成本的结构性降低**：当一个 Skill 同时满足 SOC2（NIST CSF）、AI 监管（NIST AI RMF）和对抗性 AI 评估（MITRE ATLAS）时，安全团队不需要为每个合规框架单独维护一套技能清单。一套 Skills，多个框架同时打勾。

### agentskills.io 标准：跨平台复用

这个项目遵循 [agentskills.io](https://agentskills.io) 开放标准，支持以下平台直接使用：

```
npx skills add mukul975/Anthropic-Cybersecurity-Skills
```

支持的平台包括：Claude Code、GitHub Copilot、OpenAI Codex CLI、Cursor、Gemini CLI，以及所有 agentskills.io 兼容平台。这意味着**一个 Skills 库，多个 Agent 平台复用**——不需要在每个平台单独维护安全分析的 Skills。

### MITRE ATT&CK v19.1 全覆盖

每个 Skill 的 frontmatter 都经过 `mitreattack-python` 库验证，对应到 MITRE ATT&CK v19.1 的具体 Technique ID。286 个技术，覆盖全部 15 个 Enterprise tactics，零 revoked 或 deprecated ID。

> "Every skill carries a mitre_attack frontmatter list validated against MITRE ATT&CK v19.1 using the official mitreattack-python library."
>
> — README

---

## 技术原理：Skill 的结构设计

每个 Skill 遵循 agentskills.io 标准结构：

```
skill-name/
├── SKILL.md          # 技能规范（任务定义 + 执行条件）
├── instructions/     # 任务执行指令集
├── scripts/          # 可执行脚本（如 .py, .sh）
└── resources/       # 参考数据（如 Sigma 规则集）
```

关键设计原则：**Skill 是原子的、可组合的**。不要做一个"全能安全分析 Skill"，而是做一组原子 Skill，通过 Agent 的编排层组合成完整分析流程。这是 Skills 模式的核心工程哲学。

---

## 竞品对比

| 项目 | Skills 数量 | 框架映射 | 平台支持 | License |
|------|-----------|---------|---------|---------|
| **Anthropic-Cybersecurity-Skills** | **754** | **5 个框架全覆盖** | **5+ 平台** | **Apache-2.0** |
| 单独维护的内部 SecOps Skills | 10-50 | 自定义，无标准 | 单一平台 | 私有 |
| 通用安全 Prompts 库 | N/A（不是 Skills）| 无框架映射 | 受限于特定 Agent | 各异 |

笔者认为，比起自己维护内部 Skills 库，这个开源项目的优势是**规模效应 + 持续更新**：754 个 Skills 是数十个安全专家协作的成果，且跟随 MITRE ATT&CK 的季度更新保持同步。自己从头构建，质量和覆盖面难以达到同等水平。

---

## 适用场景

- **安全运营自动化**：将 Skills 组合进 SOC 自动化的分析流程
- **红队/蓝队演练**：快速给 Agent 赋予专业级攻防技能
- **合规评估自动化**：多框架映射的 Skills 使合规检查自动化成为可能
- **AI Coding 安全**：在 CI/CD 流程中嵌入安全 Skills，自动化 SAST/DAST

---

## 快速上手

```bash
# 方式一：npx（推荐）
npx skills add mukul975/Anthropic-Cybersecurity-Skills

# 方式二：Git clone
git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git
cd Anthropic-Cybersecurity-Skills
```

加载后，Agent 即可动态发现和加载对应领域的 Skills。例如，在 Claude Code 中：

> "Analyze this memory dump for indicators of Kerberoasting attack, using the appropriate volatility3 skill."

Agent 会自动加载 `volatility3-memory-analysis` Skill 并执行。

---

## 笔者的判断

Anthropic-Cybersecurity-Skills 是 Skills 范式最直接的工程证明：**专业化 Agent 不需要训练专用模型，只需要给它正确的技能包**。754 个 Skills 覆盖安全分析的完整工作流，五大框架映射使合规成本大幅降低，agentskills.io 标准使跨平台复用成为现实。

如果你在构建安全分析 Agent，这个库是目前为止**最完整、最标准、最可复用**的开源选择。比自己维护 Skills 库效率高得多，比用通用 Prompts 精确得多。

**下一步**：如果你已经在用 Claude Code 或其他 agentskills.io 兼容平台，尝试加载其中一个安全 Skill，感受一下"给 Agent 注入专家判断力"的实际体验。