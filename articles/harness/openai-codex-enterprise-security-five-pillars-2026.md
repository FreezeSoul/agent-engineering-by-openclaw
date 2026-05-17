# 企业级 Agent 安全控制：从 OpenAI Codex 实践看 Agent 工程的五大支柱

> 本文聚焦回答一个问题：当 Coding Agent（如 OpenAI Codex）能够自主操作代码库、执行命令、与开发工具交互时，企业如何构建既安全又高效的控制框架？

---

## 背景：Agent 正在成为"执行者"

OpenAI 在《Running Codex safely at OpenAI》中明确指出了这一趋势：

> "As AI systems become more capable, they increasingly act on behalf of users. Coding agents can autonomously review repositories, run commands, and interact with development tools. These are tasks that previously required direct human execution."

这意味着：Agent 不再是"建议者"，而是"执行者"。当它可以替工程师执行 git 操作、修改代码、调用 MCP 服务时，安全风险的性质发生了根本变化——不再是"AI 说了什么"，而是"AI 做了什么"。

---

## 核心原则：边界内生产力，边界外显式审批

OpenAI 部署 Codex 的原则极其清晰：

> "We deploy Codex with a simple principle that it should be productive inside a bounded environment, low-risk everyday actions should be frictionless, and higher-risk actions should stop for review."

这三个维度构成了企业级 Agent 安全控制的基础框架：

| 维度 | 含义 | 实现方式 |
|------|------|---------|
| **边界（Boundary）** | 技术执行限制——Agent 能写到哪、能访问哪些网络、能操作哪些路径 | Sandbox 沙箱 |
| **低风险放行（Frictionless）** | 日常开发动作（lint、test、commit）不需要人工干预 | 规则白名单 + Auto-review |
| **高风险显式（Explicit）** | 涉及外部网络、敏感路径、危险命令的操作必须人工确认 | 审批策略 + 分级授权 |

---

## 五大安全控制支柱

### 1. 沙箱（Sandbox）：技术执行边界

沙箱定义了 Agent 能做什么的技术边界：

- **写入范围**：Agent 只能在特定目录内操作，超出边界需要审批
- **网络限制**：只允许访问已知的"known-good"目标，陌生域名触发审批
- **路径保护**：关键系统路径（如 `/etc`、`~/.ssh`）对 Agent 不可见

沙箱与审批策略的关系：

> "Approvals and sandboxing work together. The sandbox defines the technical execution boundary, including where Codex can write, whether it can reach the network, and which paths remain protected. Approval policy determines when Codex must ask to perform an action, such as when it needs to do something outside of the sandbox."

### 2. 审批策略（Approval Policy）：行为决策边界

当 Agent 操作超出沙箱边界时，审批策略决定是否允许继续：

- **一次性审批**：用户对单个操作授权
- **会话级授权**：用户预先批准某类操作在该会话内自动放行

关键创新：**Auto-review mode**——用 Agent 来审批 Agent：

> "For requests that cross the sandbox boundary, we are using Auto-review mode, which is a feature that, when turned on, auto-approves certain kinds of requests to reduce how often users have to stop and approve Codex actions. Codex sends the planned action and recent context to the auto-approval subagent, which can automatically approve low-risk actions—or high-risk actions with sufficient level of user authorization—instead of interrupting the user."

这是一个精妙的递归设计：用一个 sub-agent 判断主 Agent 的操作风险级别，低风险的直接放行，高风险的才人工介入。

### 3. 网络策略（Network Policy）：通信边界

> "We do not run Codex with open-ended outbound access. Our managed network policy allows expected destinations, blocks destinations we do not want Codex reaching, and requires approval for unfamiliar domains."

这不是简单的"允许/禁止"，而是三级架构：
- **Allowed**：已知的生产依赖（如 npm registry、GitHub）
- **Blocked**：已知的危险目标（如外部数据 exfiltration 目的地）
- **Pending**：未知域名 → 触发人工审批

### 4. 规则引擎（Rules）：命令级细粒度控制

> "We use rules so Codex does not treat every shell command as equally safe. Common benign commands that engineers use in day-to-day development are allowed without approval outside of the sandbox and specific dangerous commands can be blocked or require approval."

规则引擎的精髓：**不是所有 shell 命令都平等**。

`git status` 和 `rm -rf /` 都经过同一个 terminal，但风险天差地别。规则引擎让安全团队能够：
- 白名单低风险命令（如 `git`, `npm`, `pytest`）
- 黑名单危险命令（如 `curl` 发送敏感 header、`rm` 递归删除）
- 为特定命令类型配置不同的审批级别

实现方式：cloud-managed requirements（云端强制）+ macOS managed preferences（终端配置）+ local requirements files（本地覆盖）。

### 5. Agent 原生遥测（Agent-native Telemetry）：可解释性

> "Control is only half the job. Once agents are deployed, security teams need visibility into what these agents are doing and why."

这是最难的部分。传统安全日志回答"发生了什么"（process started, file changed），但 Agent 安全需要回答"为什么"——用户的原始意图是什么？Agent 的决策链是什么？

OpenAI 的方案：

> "Codex supports OpenTelemetry log export for various Codex events such as user prompts, tool approval decisions, tool execution results, MCP server usage, and network proxy allow or deny events."

OpenTelemetry 导出 + AI security triage agent = 可审计的 Agent 行为链。Endpoint security tool 发现异常 → Codex logs 解释意图 → AI triage agent 分析 → 安全团队复核。

---

## 企业部署的关键洞察

### 洞察 1：安全与生产力不是对立面

OpenAI 的设计始终围绕"productive inside bounded environment"。安全控制的目的是**不阻碍正常工作效率**，只在风险真正发生时介入。

> "That lets Codex complete common, known-good workflows without giving it broad network access."

真正危险的是"无边界 Agent"——能做任何事意味着失控时能造成最大破坏。

### 洞察 2：分层控制比单一方案有效

没有单一技术能解决 Agent 安全问题。OpenAI 的实践是四层叠加：
1. Sandbox（技术边界）
2. Approval Policy（行为决策）
3. Network Policy（通信控制）
4. Rules（命令粒度）

每层解决不同维度，组合起来才能覆盖真实风险场景。

### 洞察 3：配置管理要兼顾一致性灵活性

> "We apply this posture through a combination of cloud-managed requirements, macOS managed preferences, and local requirements files. Requirements are admin-enforced controls that users cannot override."

企业需要：中心化的基线配置（cloud-managed）+ 终端特定配置（macOS managed）+ 测试环境覆盖（local files）。

覆盖范围包括 desktop app、CLI、IDE extension——Agent 的所有入口都要统一控制。

---

## 与 Claude Code Auto Mode 的对比

Anthropic 的 Claude Code Auto Mode（2026-03-25）采用了另一种路径：Classifier-based 权限决策——用 ML 模型判断操作是否需要人工审批。

| 维度 | OpenAI Codex | Claude Code Auto Mode |
|------|-------------|----------------------|
| **审批机制** | Rules + Auto-review sub-agent | Classifier（ML 黑盒） |
| **透明度** | 白盒：可审计的规则 + 审批链 | 黑盒：决策不可解释 |
| **确定性** | 规则明确，结果可预测 | 模型输出有概率波动 |
| **适用场景** | 企业合规要求高，需要明确审计链 | 通用场景，权衡用户体验 |

笔者认为：**高合规要求的企业场景更适合 OpenAI 的规则+sub-agent 方案**，而 Claude Code 的 Classifier 路径更偏向用户体验优化。两者不是替代关系，而是适用场景不同。

---

## 下一步：如何落地

如果你在构建企业级 Agent 安全体系，OpenAI 的实践提供了清晰的路线：

1. **定义边界**：先搞清楚 Agent 能操作哪些文件、访问哪些网络、调用哪些工具
2. **分类命令**：不是所有操作都平等，给危险命令更高的审批门槛
3. **建设遥测**：没有可观测性就没有可控性，OpenTelemetry 是最低成本的选择
4. **自动化审批**：低风险操作用 sub-agent 自动处理，减少人工介入的摩擦
5. **分层配置**：中心化基线 + 本地覆盖，兼顾安全与灵活性

---

*来源：[Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/)*