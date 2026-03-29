# Agent Skills 全面综述：架构、获取、安全与演进路径

> **本质**：当 Agent 从"通用大模型"走向"模块化技能体"，Skill 作为"按需加载的能力包"正在成为 Agent 系统的核心抽象层——涵盖 SKILL$.$md 规范、渐进式上下文加载、CUA 部署栈，以及 26.1% 社区 Skills 含有漏洞这一严峻安全问题。

**来源**：[Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward](https://arxiv.org/abs/2602.12430)（Xu Renjun, Yan Yang，2026/02/12）
**GitHub**：[scienceaix/agentskills](https://github.com/scienceaix/agentskills)
**性质**：学术综述论文（arXiv:2602.12430，2026/02/12）
**评分**：16/20
**演进阶段**：Stage 10（Skill）
**补充阅读**：[渐进式披露 vs MCP — Claude Agent Skills 实践](https://www.mcpjam.com/blog/claude-agent-skills)

---

## 一、基本概念：从"全知模型"到"技能体"

传统大语言模型将所有知识编码在模型权重中，导致两个根本矛盾：

- **知识过时问题**：模型无法动态更新知识，只能靠重训练
- **上下文浪费问题**：Agent 每次任务都只需部分能力，但必须加载全部上下文

**Agent Skills** 的核心思路是**将 procedural knowledge（过程性知识）从模型权重转移到可外部化的技能包**。一个 Skill 是一个「instructions + code + resources」的组合单元，Agent 在需要时动态加载，无需重新训练。

这一定义与 MCP 的定位形成清晰互补：

| 维度 | MCP（Model Context Protocol）| Agent Skills |
|------|---------------------------|-------------|
| **核心职责** | 连接（Agent ↔ 工具/数据的通信协议）| 赋能（领域知识的封装与按需加载）|
| **抽象层次** | 协议层（transport + schema）| 应用层（knowledge + procedure）|
| **加载方式** | 初始化时全部加载 | 渐进式披露（Progressive Disclosure）|
| **分发方式** | 远程 MCP 服务器，OAuth 认证 | 本地 SKILL.md 文件夹，可打包为 zip |
| **标准化程度** | 行业标准（Linux Foundation 支持）| 早期规范（SKILL$.$md 草案）|
| **适用场景** | 工具接入、标准化工具生态 | 领域知识封装、工作流程自动化 |

两者的关系不是竞争，而是**分层互补**：MCP 负责"用什么工具"，Skill 负责"如何使用工具完成任务"。

---

## 二、架构基础：SKILL$.$md 规范与渐进式加载

### 2.1 SKILL$.$md 规范

论文提出的 **SKILL$.$md** 规范是 Skills 的核心文件格式，灵感来自 Claude Code 的 `SKILL.md` 实践。每个 Skill 包含：

```
pdf-skill/
├── SKILL.md          # 主指令文件（描述 + 快速启动）
├── FORMS.md          # 表单填写指南
├── REFERENCE.md      # 详细 API 参考
└── scripts/
    └── fill_form.py  # 工具脚本（可选）
```

**SKILL.md 的核心原则**：SKILL.md 应该是**目录**，而不是**百科全书**。它告诉 Agent「在哪里找到更多信息」，而非把全部信息塞进上下文。

### 2.2 渐进式上下文加载（Progressive Context Loading）

这是 Skills 区别于 MCP 的关键机制。Agent 不在初始化时加载全部上下文，而是：

1. **初始层**：SKILL.md 提供技能概述和使用触发条件
2. **发现层**：Agent 根据任务需要，动态发现并加载 `REFERENCE.md`、`scripts/` 等子资源
3. **执行层**：仅在需要时加载具体实现代码

**渐进式披露的核心价值**：
- **上下文窗口效率**：避免一次性塞入过多工具描述（实测 MCP 在连接 2-3 个服务器后工具使用准确率显著下降）
- **可扩展性**：单个 Skill 可包含整个 API 文档或大型参考数据集，而不占用 Agent 的核心上下文空间
- **可发现性**：只要指令和元数据写得好，Agent 能自主发现所需资源

### 2.3 Skills 与 MCP 的协同

论文指出，Skills 和 MCP 不是替代关系，而是**互补的双层架构**：

```
Agent 核心（LLM + 推理引擎）
    ├── Skill 层：领域知识、流程、触发条件（SKILL.md）
    │   └── 渐进式加载 → 按需注入上下文
    └── MCP 层：工具接入、远程服务（JSON-RPC）
        └── 初始化加载 → 运行时快速调用
```

**典型工作流**：Agent 通过 Skill 层理解"我要处理 PDF 表单"这个任务，通过 MCP 层调用 `pdfplumber` 工具执行具体操作。

---

## 三、技能获取：从手工编写到自主合成

论文系统梳理了 Skill 获取的三条路径：

### 3.1 强化学习 + 技能库（SAGE）

**SAGE**（Skill Acquisition via Guided Exploration）是一种通过 RL 从技能库中学习新技能的方法。核心思想：

- **技能库作为动作空间**：将已有技能定义为离散的动作单元，RL 策略学习如何组合它们
- **在线评估**：每次任务完成后评估技能组合的有效性，更新策略
- **适用场景**：需要组合多个已有技能完成复杂任务（如"分析 PDF 财务报告并生成摘要"）

### 3.2 自主技能发现（SEAgent）

**SEAgent**（Skill Extraction Agent）是一个能从任务执行轨迹中自动发现和提取技能模式的系统：

1. Agent 执行一系列任务
2. 系统分析成功的执行轨迹，提取可复用的模式
3. 将模式封装为新的 Skill 文件（SKILL.md + scripts）
4. 新 Skill 被加入技能库，供后续使用

**意义**：这是"AI 自我改进"的关键步骤——系统不仅执行任务，还能从经验中抽取知识。

### 3.3 组合式技能合成（Compositional Skill Synthesis）

**组合式合成**是指通过预定义的技能原语（primitives）组合生成新技能，而无需手工编写：

```
新技能 = 技能原语A × 技能原语B × 领域约束
```

**示例**：一个"房产尽职调查"技能可以由以下原语组合：
- `document_reader`（文档读取）
- `financial_calculator`（财务计算）
- `risk_assessor`（风险评估）
- `report_generator`（报告生成）

这与软件工程中的"设计模式组合"思想一致。

---

## 四、生产级部署：CUA 栈与基准测试进展

### 4.1 Computer-Use Agent（CUA）栈

论文详细介绍了 **CUA 栈**——支撑 AI Agent 操作计算机（浏览器、桌面应用、文件系统）的技术栈：

```
用户指令层
    ↓
规划与推理层（LLM）
    ↓
GUI Grounding 层（将 LLM 输出映射到 UI 操作）
    ↓
操作系统抽象层（鼠标、键盘、窗口管理）
```

**GUI Grounding 的挑战**：将"点击蓝色按钮"这样的自然语言指令映射到具体的像素坐标和 UI 元素，是计算机操作 Agent 的核心技术难点。

### 4.2 基准测试进展

论文跟踪了两个关键基准的进展：

| 基准 | 覆盖领域 | 评估重点 | 最新成绩 |
|------|---------|---------|---------|
| **OSWorld** | 操作系统操作（Linux/Windows/macOS）| 多步骤任务、跨应用工作流 | 持续更新中 |
| **SWE-bench** | 软件工程任务（真实 GitHub Issue）| 代码修改、PR 创建 | 各大模型均有评测 |

这两个基准共同构成了 AI Agent 的"操作能力测试集"，与我们在[GAIA 通用助手评测](../research/gaia-osworld-benchmark-2026.md)和[MCPMark MCP 专项评测](../research/mcpmark-iclr2026-benchmark.md)中的发现**形成三层互补**：

- **GAIA**：通用助手能力（能否正确回答问题）
- **OSWorld/SWE-bench**：计算机操作 Agent 能力（能否执行操作）
- **MCPMark**：MCP 协议专项压力测试（工具调用是否可靠）

---

## 五、安全问题：26.1% 的社区 Skills 含有漏洞

论文最发人深省的发现是**实证安全分析**：

> 对社区贡献的 Skills 进行安全扫描发现：**26.1% 含有至少一个安全漏洞**。

### 5.1 漏洞类型

| 漏洞类型 | 描述 | 风险等级 |
|---------|------|---------|
| **代码注入** | Skill 中的 scripts 包含未清理的用户输入直接拼接到 shell 命令 | 🔴 高 |
| **敏感数据泄露** | Skills 包含硬编码的 API keys、credentials | 🔴 高 |
| **权限过度授予** | Skill 被授予超出任务需求的系统权限 | 🟡 中 |
| **依赖漏洞** | Skill 的 scripts 使用了含有已知 CVE 的第三方库 | 🟡 中 |
| **路径遍历** | Skills 读取/写入超出预期范围的文件系统路径 | 🟡 中 |

### 5.2 Skill Trust and Lifecycle Governance Framework

论文提出的 **Skill Trust 框架**是一个**四层门控权限模型**，根据 Skill 的来源和审计状态，授予不同的部署能力：

```
┌─────────────────────────────────────────────┐
│  Tier 4: 已审计 + 签名验证（最高信任）      │
│  → 全系统权限，可访问敏感 API               │
├─────────────────────────────────────────────┤
│  Tier 3: 已审计 + 安全扫描通过（常规信任）  │
│  → 标准权限，可执行网络请求                 │
├─────────────────────────────────────────────┤
│  Tier 2: 仅安全扫描通过（基础信任）         │
│  → 受限权限，限制网络和文件系统访问         │
├─────────────────────────────────────────────┤
│  Tier 1: 无审计（最低信任）                 │
│  → 沙箱执行，禁止网络和敏感系统调用         │
└─────────────────────────────────────────────┘
```

**与 OWASP ASI 的关系**：Skill Trust 框架与 [OWASP Top 10 for Agentic Applications 2026](../community/owasp-top-10-agentic-applications-2026.md) 中的"AI Agent 安全治理"思路高度一致——都需要对第三方扩展进行来源审计和权限分级。

### 5.3 与 MCP 安全危机的相似性

值得注意的是，Skills 的安全问题与我们在 [MCP Security Crisis：30 CVEs 60 天](../community/mcp-security-crisis-30-cves-60-days.md)中追踪的 MCP CVE 风暴有**相同的结构性根源**：

- MCP：社区大量贡献 MCP 服务器，38% 无认证，43% 存在命令注入
- Skills：社区 Skills 26.1% 含有漏洞

这表明 **"快速社区贡献 → 治理缺失 → 安全危机"** 是 Agent 生态系统的普遍规律。Skills 正在重走 2010 年代开源软件的成熟路径（JFrog 的判断）。

---

## 六、七大开放挑战

论文识别了 Skill 领域的七个未解决问题：

| 序号 | 挑战 | 描述 |
|------|------|------|
| 1 | **跨平台技能可移植性** | 一个 Skill 在不同 Agent/环境中是否有一致的行为？ |
| 2 | **能力边界与权限模型** | 如何设计精细的能力（capability）而非粗粒度的权限（permission）？ |
| 3 | **技能版本治理** | 当上游 Skill 更新时，依赖它的 Agent 行为如何保证一致性？ |
| 4 | **自动化安全审计** | 如何大规模自动化扫描 Skills 中的漏洞，而不产生误报？ |
| 5 | **技能组合爆炸** | 随着 Skill 数量增长，组合式合成的搜索空间如何控制？ |
| 6 | **真实性验证** | 如何验证一个 Skill 声称的能力与实际行为一致？ |
| 7 | **自我改进的边界** | SEAgent 等自主发现系统在什么条件下会"学坏"？ |

---

## 七、实践指南：如何编写高质量 SKILL.md

基于论文规范和 Claude Agent Skills 的最佳实践：

### 7.1 SKILL.md 结构模板

```markdown
# [技能名称]

> 一句话描述技能的功能和使用场景

## 适用条件
- 当用户说 [...]
- 当任务涉及 [...]

## 快速启动
[最基本的用法示例，3 行以内]

## 详细说明
[更深度的使用指南，按需加载]

## 注意事项
[常见错误和限制]

## 相关资源
- FORMS.md：[具体表单的填写方式]
- REFERENCE.md：[API 详细文档]
- scripts/：[可复用的脚本工具]
```

### 7.2 编写原则

1. **触发条件要精确**：让 Agent 能准确判断何时应该使用该 Skill
2. **快速启动要简短**：核心用例不应超过 3 行代码
3. **渐进式嵌套**：详细信息放 `REFERENCE.md`，SKILL.md 本身是目录
4. **权限最小化**：scripts 只请求完成任务所需的最小权限
5. **可验证性**：提供自我测试用例，确保 Skill 在目标场景下可正常工作

---

## 八、与现有文章的关系

本文与仓库中以下文章形成**演进路径的纵向深化**：

| 相关文章 | 关系 |
|---------|------|
| [Agent Skill：能力的抽象单元](../concepts/agent-skill-system.md) | Stage 10 概念基础；本文提供深度学术视角 |
| [Skill Registry Ecosystem：ClawHub / Composio](../community/skill-registry-ecosystem-clawhub-composio.md) | Stage 10 生态系统；本文提供 Skill 治理的学术框架 |
| [MCP Security Crisis：30 CVEs 60 天](../community/mcp-security-crisis-30-cves-60-days.md) | Stage 12 安全工程；Skills 26.1% 漏洞率是 MCP CVE 危机的镜像 |
| [GAIA + OSWorld Benchmark](../research/gaia-osworld-benchmark-2026.md) | Stage 8 评测体系；CUA 栈与 OSWorld/SWE-bench 评测互补 |
| [Claude Code Auto Mode](../engineering/claude-code-auto-mode-harness-engineering.md) | Stage 12 Harness Engineering；Auto Memory 与 Skill 加载机制有交叉 |

---

## 九、局限性

1. **SKILL$.$md 规范尚未标准化**：本文提出的规范是学术草案，与实际工业实践（如 Claude Agent Skills 的实现）存在差异
2. **安全数据来源有限**：26.1% 漏洞率基于特定社区采样，可能不代表全部生态
3. **CUA 栈技术细节不足**：论文对 GUI Grounding 的具体算法描述较少
4. **Skill 与 MCP 的边界模糊**：实际系统中两者往往深度耦合，难以严格区分

---

## 十、参考文献

1. Xu, R. & Yan, Y. (2026). *Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward*. arXiv:2602.12430. https://github.com/scienceaix/agentskills
2. Anthropic. *Claude Agent Skills Documentation*. https://docs.anthropic.com
3. MCPJam. *Progressive Disclosure Might Replace MCP (Claude Agent Skills)*. https://www.mcpjam.com/blog/claude-agent-skills
4. JFrog. *Agent Skills are the New Packages of AI*. https://jfrog.com
5. OSWorld. *OSWorld: Operating System Benchmark for AI Agents*. https://osworld.github.io
6. SWE-bench. *Software Engineering Benchmark for LLMs*. https://www.swebench.com

---

*本文属于 Stage 10（Skill）演进阶段，是对 [Agent Skill 概念文章](../concepts/agent-skill-system.md) 和 [Skill Registry Ecosystem 文章](../community/skill-registry-ecosystem-clawhub-composio.md) 的学术深度补充。*
