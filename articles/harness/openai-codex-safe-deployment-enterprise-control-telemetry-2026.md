# OpenAI Codex 安全运行架构：企业级 Agent 控制与遥测体系

> 本文解读 OpenAI 官方工程博客「Running Codex safely at OpenAI」，深入分析其企业级 Agent 安全部署的控制面与可观测性设计。

## 核心问题

当 AI 系统越来越有能力代表用户自主行动时，如何在保持开发者效率的同时，让安全团队真正掌握 Agent 的行为边界？

这不是一个「要不要加护栏」的问题，而是一个「如何在不扼杀生产力的前提下建立有效控制」的系统工程问题。

## 设计原则：三层控制架构

OpenAI 的回答是三层架构：**沙箱（Sandbox）+ 审批策略（Approval Policy）+ 遥测（Telemetry）**。

### 1. 沙箱：技术执行边界

沙箱定义 Codex 能做什么、不能做什么。它决定了：
- Codex 能写哪些目录
- Codex 能否访问网络，访问哪些目标
- 哪些路径受保护、不可写

关键设计洞察：沙箱与审批策略协同工作。当 Codex 需要跨越沙箱边界时（比如访问受限路径或未知网络域），才触发审批流程。**低风险动作保持无摩擦，高风险动作强制暂停等待人类决策**。

这一点与 Anthropic 的 Auto Mode 理念一致——都不是简单粗暴地全开或全关，而是让风险级别决定是否中断。

### 2. Auto-review 模式：消除审批疲劳

OpenAI 引入了 Auto-review mode 来解决审批中断带来的效率问题。其工作方式：

> Codex sends the planned action and recent context to the auto-approval subagent, which can automatically approve low-risk actions—or high-risk actions with sufficient level of user authorization—instead of interrupting the user.

这是一个典型的 Agent 编排设计：主 Agent（Codex）在遇到边界行为时，将上下文交给一个专门的审批子代理判断。子代理可以：
- 自动批准低风险动作
- 对于高风险动作，检查用户是否有足够的授权级别来自动批准

这与 Anthropic 的 GAN 架构（Planner-Generator-Evaluator）在概念上一致——都是将「判断」从主执行流中解耦出来，交给专门的子 Agent 处理。区别在于：GAN 的 Evaluator 评估代码质量，Auto-review 评估安全风险。

### 3. 网络策略：最小权限原则

OpenAI 的网络策略遵循「默认拒绝，例外放行」：

> Our managed network policy allows expected destinations, blocks destinations we do not want Codex reaching, and requires approval for unfamiliar domains.

Codex 完成常见已知工作流（如访问 npm/pypi、git push 到已配置的仓库），而不需要给 Agent 全量的网络访问权限。这是传统 zero-trust network 架构在 Agent 时代的应用。

### 4. 认证管理：绑定企业身份

Codex 的认证设计有几个要点：

- **CLI 和 MCP OAuth 凭证存储在 OS 安全密钥链**（Keyring），而非明文配置文件
- **登录强制通过 ChatGPT**，确保身份来源单一
- **访问权限绑定到企业 ChatGPT workspace**，而非个人账号
- **Codex 活动记录进 ChatGPT Compliance Logs Platform**，企业合规审计可直接查询

笔者认为，这是 Agent 认证管理的最佳实践——将 Agent 身份与人类身份系统解耦，同时通过企业 IDP（Identity Provider）实现集中管控。当 Agent 行为出现问题时，安全团队可以直接溯源到「哪个 workspace 的哪个 Agent 执行了什么操作」，而不是在分散的个人账号中追踪。

## Agent 原生遥测：超越传统安全日志

这是本文最有价值的部分，也是 OpenAI 真正理解企业安全团队需求的地方。

### 传统安全日志的局限性

传统日志回答的是「what happened」：进程启动了、文件被改了、网络连接被尝试了。但安全分析师仍然需要推断「为什么 Codex 做了这个动作」或「用户的意图是什么」。

这对 Agent 尤其困难，因为同一个 shell 命令在 Agent 上下文中可能有完全不同的含义。

### Agent-aware 遥测视图

Codex 导出 OpenTelemetry 格式的日志，覆盖以下事件类型：
- **User prompts**：用户的原始请求
- **Tool approval decisions**：审批决策（包括自动批准和人工批准）
- **Tool execution results**：工具执行结果
- **MCP server usage**：MCP server 调用记录
- **Network proxy allow or deny events**：网络策略决策

这意味着安全团队不只能看到「Codex 执行了 `rm -rf /tmp/foo`」，而能看到：
- 这是在什么用户请求上下文中发生的
- 这是否触发了审批流程（如果是，审批决策是什么）
- 工具返回了什么结果
- 网络请求是否被拦截

### 实际应用：AI 安全分诊

OpenAI 内部使用 Codex 日志配合 AI 安全分诊 Agent：

> When an endpoint alert says Codex did something unusual, the endpoint security tool tells us that a suspicious event occurred. Codex logs then help explain the surrounding intent by the user and agent. Our AI security triage agent uses Codex logs to inspect the original request, tool activity, approval decisions, tool results, and any relevant network policy decision or block.

这是一个典型的 AI-on-AI 用法：安全 Agent 读取代码 Agent 的操作日志，判断是否真的存在威胁。人类安全分析师只需要处理真正需要升级的事件，而不是被大量「可能有问题」的告警淹没。

### 操作层面的遥测价值

除了安全合规，OpenAI 还用同样的日志做运营分析：
- 团队内部 Agent 采用率的变化趋势
- 哪些工具和 MCP server 被使用最频繁
- 网络沙箱拦截或提示的频率
- 推广节奏中需要调整的部分

这是 Agent 可观测性（Observability）的落地实践——不是等出了问题才去看日志，而是持续用日志数据驱动 Agent 部署策略的迭代。

## 配置管理体系：多层次覆盖

OpenAI 通过三层配置实现 Agent 行为的系统化管理：

| 层级 | 描述 | 可覆盖性 |
|------|------|---------|
| **Cloud-managed requirements** | 企业管理员通过云端下发，强制执行 | 不可被用户覆盖 |
| **macOS managed preferences** | 操作系统级别配置 | 按团队/用户组/环境测试不同配置 |
| **Local requirements files** | 本地配置文件 | 允许团队级别的实验性调整 |

这些配置覆盖所有 Codex 表面（桌面 App、CLI、IDE 插件），确保安全策略的一致性。

## 设计判断：与其他方案的对比

OpenAI 的方案与 Anthropic 的 Auto Mode、Cursor 的 Harness Measurement 在方向上一致，都是「让风险级别决定干预程度」而非「一刀切地全部批准或全部拒绝」。

但在具体实现上，OpenAI 的贡献在于：
1. **Auto-review 作为专用子 Agent**：将审批决策完全解耦为一个独立的自动化的 Agent，而非硬编码规则
2. **OpenTelemetry 导出**：将 Agent 日志纳入企业级 SIEM 系统，实现与传统安全工具的集成
3. **Compliance Logs Platform**：为受监管行业（医疗、金融）提供开箱即用的合规审计能力

笔者认为，随着 Agent 在企业中的普及，安全团队需要的不是「在 Agent 周围加一圈护栏」，而是「Agent-native 的控制面和可观测性」——OpenAI 在这方面的实现思路值得所有做 Agent 平台的人参考。

## 引用

> "We deploy Codex with a simple principle that it should be productive inside a bounded environment, low-risk everyday actions should be frictionless, and higher-risk actions should stop for review." — [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/), OpenAI Engineering Blog, May 8, 2026

> "Control is only half the job. Once agents are deployed, security teams need visibility into what these agents are doing and why." — [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/), OpenAI Engineering Blog, May 8, 2026

> "Codex supports OpenTelemetry log export for various Codex events such as user prompts, tool approval decisions, tool execution results, MCP server usage, and network proxy allow or deny events." — [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/), OpenAI Engineering Blog, May 8, 2026

---

*关联阅读：[Anthropic Claude Code Auto Mode](./anthropic-claude-code-auto-mode-transcript-classifier-harness-2026.md) — 另一种风险分级授权方案；[Cursor Harness Measurement](./cursor-continually-improving-agent-harness-measurement-driven-2026.md) — 测量驱动的 Harness 迭代方法*
