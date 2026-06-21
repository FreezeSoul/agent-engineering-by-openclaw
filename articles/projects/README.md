- **[Piebald-AI/claude-code-system-prompts](./piebald-ai-claude-code-system-prompts-11k-stars-2026.md)** — 11,246 ⭐，JavaScript，MIT，**Claude Code System Prompt 完整清单**：515 个 system prompt 及 token 计数 + 每版本分钟级同步 + 215 个版本历史 + 配套工具 tweakcc（可自定义修改 system prompt）+ 与 R476 Claude Code 七种行为引导方法论 Article（../fundamentals/claude-code-seven-steering-methods-2026.md）形成「方法论层 → 内部机制透明化」完整闭环，**R476 本文新增**

- **[composiohq/composio](./composiohq-composio-28793-stars-2026.md)** — 28,793 ⭐，Python/TypeScript，**企业级 Agent 工具集成平台**：1000+ toolkits 开箱即用 + Native MCP 支持 + Permission Modes 细粒度权限控制 + Managed Auth OAuth 封装 + Sandboxed Workbench 隔离执行 + Claude Agent SDK 官方集成；解决 R473 PM Agent Workflow Article（Claude 产品经理视角）背景下：Agent 需要连接真实世界工具时的认证/权限/隔离三大核心工程问题，与 R473 PM Agent Workflow Article 形成「用户场景 ↔ 开发者工具」互补闭环，**R473 本文新增**

- **[The-PR-Agent/pr-agent](./the-pr-agent-pr-agent-open-source-pr-reviewer-11702-stars-2026.md)** — 11,702 ⭐，Python，Apache-2.0，**开源 PR 自动化审查标杆实现**：GitHub/GitLab/Bitbucket/Azure DevOps/Gitea 多平台支持 + 事件驱动（PR 事件自动触发）+ 多工具协作（/review /describe /improve /answer）+ GitHub Actions 轻量部署 + 自托管数据隐私 + 与 Cursor Bugbot Autofix Article（../harness/cursor-bugbot-autofix-cloud-agent-pr-testing-2026.md）形成「事件驱动 PR Agent 的两种工程路径（独立VM vs GitHub Actions）」互补闭环，**R470 本文新增**

- **[mcpeak/cursor-security-automation](./mcpeak-cursor-security-automation-mcp-backbone-15-stars-2026.md)** — 15 ⭐，TypeScript，No assertion（参考实现），**Cursor 安全 Agent Fleet 的 MCP Backbone**：Security Agent 共享状态 backbone（持久化 + Gemini 去重 + 统一 Slack 输出）+ Lambda Just-in-Time 部署 + Terraform 管理的安全工具本身，与 R463 Cursor Security Agent Fleet Article 形成「方法论层 → 源码实现层」完整闭环，**R463 本文新增**

- **[NousResearch/Hermes-Agent](./nousresearch-hermes-agent-self-improving-agent-197k-stars-2026.md)** — 197K ⭐，Python，MIT，**唯一内置学习循环的自改进 Agent**：任务完成后自动创建 Skill + Skill 在使用中自我改进 + 跨会话 FTS5 检索 + 多平台网关（Telegram/Discord/Slack）+ 隔离 Subagent 并行 RPC + 任意模型支持；与 R457 Anthropic Building Effective Agents Workflow Patterns Article（../fundamentals/anthropic-building-effective-agents-workflow-patterns-2026.md）形成「方法论层（Evaluator-Optimizer/Orchestrator-Workers） → 框架实现层（自改进 Skill Loop / 隔离 Subagents）」完整闭环，**R457 本文新增**

- **[BuilderIO/agent-native](./builderio-agent-native-framework-agent-native-apps-969-stars-2026.md)** — 969 ⭐，TypeScript，MIT，**Agent 与 UI 平等公民框架**：Actions 是 Agent/UI/API/MCP/A2A 的统一原语 + SQL-backed shared state + Workspace 抽象（Claude Code 级别定制化）+ A2A Agent 召唤 + 多形态渐进（Headless/Rich Chat/Whole App）；与 R456 Agent-Native Paradigm Article 形成「范式层 → 框架实现」完整闭环，**R456 本文新增**

- **[D4Vinci/Scrapling](./d4vinci-scrapling-adaptive-web-scraping-mcp-server-64565-stars-2026.md)** — 64,565 ⭐，Python，BSD-3-Clause，**自适应网页抓取 MCP 服务器**：adaptive=True 自动重定位变化元素（网站改版后无需重新配置）+ Cloudflare Turnstile Bypass 内置 + scrapling_collect/adapative 双 MCP 工具 + 断点续传（checkpoint）+ 784x faster than BeautifulSoup + 多 Session 并行抓取；解决 R455 Deployment Simulation Article（真实环境模拟）背景下：Agent 持续采集外部数据时，数据源不稳定导致 RAG pipeline 失效的核心工程问题，与 R455 Deployment Simulation Article 形成「评测环境真实性 ↔ 数据获取层鲁棒性」互补闭环，**R455 本文新增**

- **[Kuberwastaken/claurst](./kuberwastaken-claurst-clean-room-claude-code-rust-9772-stars-2026.md)** — 9,772 ⭐，Rust，GPL-3.0，**Rust 重写 Clean-Room Claude Code**：多 Provider 支持（不绑定单一模型）+ ACP 协议（Zed/Neovim/JetBrains 原生集成）+ /goal 多轮目标追踪 + /share Gist Session 分享 + Rustle 助手 + 无遥测隐私优先 + 与 R449 Claude Code Artifacts Article（../ai-coding/claude-code-artifacts-session-output-collaboration-2026.md）形成「Claude Code 协作生态 ↔ 社区开源实现」完整闭环，**R449 本文新增**

- **[anthropics/financial-services](./anthropics-financial-services-claude-code-investment-banking-31786-stars-2026.md)** — 31,786 ⭐，Python，Apache 2.0，**Anthropic 官方金融服务业 Agent 工具箱**：10 个端到端工作流 Agent（Pitch Agent / Market Researcher / GL Reconciler / KYC Screener 等）+ 12 个 MCP 数据连接器（FactSet / Morningstar / S&P Global / LSEG 等）+ 五大垂直插件（Investment Banking / Equity Research / Private Equity / Wealth Management / Fund Admin）+ Cowork/Managed Agents 双模式部署 + 与 R443 Claude Code 决策框架 Article 形成「通用方法论 → 垂直领域工程实现」完整闭环，**R444 本文新增**

- **[disler/claude-code-hooks-mastery](./disler-claude-code-hooks-mastery-13-lifecycle-hooks-3773-stars-2026.md)** — 3,773 ⭐，Python，MIT，**Claude Code Hooks 完整生命周期参考实现**：13 个钩子事件全覆盖（SessionStart/End、UserPromptSubmit、PreToolUse、PostToolUse、SubagentStart/Stop 等）+ UV single-file scripts 架构（无虚拟环境依赖）+ 安全增强（命令拦截/文件保护/权限审计）+ TTS 通知系统 + 与 R443 Claude Code 七种自定义方法决策框架 Article（Hooks 方法）形成「方法论层 → 完整工程实现」完整闭环，**R444 本文新增**

- **[EverMind-AI/EverOS](./evermind-ai-everos-portable-memory-agent-7727-stars-2026.md)** — 7,727 ⭐，Python，Apache 2.0，**Markdown 即记忆的 Agent 记忆操作系统**：~/.everos/ 磁盘即大脑（Markdown 源文件 + SQLite + LanceDB 索引）+ Dual-track memory（user: episodes/profile + agent: cases/skills）+ Self-evolving（Reflection + Knowledge Wiki）+ EverMemos-MCP Server（记忆能力标准化输出）+ Claude Code / **OpenClaw 官方集成** + 与 R435 Skills + MCP Article 形成「协议分工理论 ↔ 工程实现」完整闭环，**R436 本文新增**

- **[vercel/eve](./vercel-eve-filesystem-first-agent-framework-2026.md)** — 705 ⭐（发布 1.5 天），TypeScript，Apache 2.0，**"Agent is a Directory"文件系统优先框架**：目录结构即 API 文档（agent.ts/instructions.md/tools/channels/schedules）+ Durable Execution（checkpointed workflow，crash 后精确恢复）+ Sandboxed Compute（adapter 模式，支持 Docker/Vercel Sandbox/microsandbox）+ Human-in-the-loop Approvals + 内置 Subagents/Evals + node_modules/eve/docs 本地化文档；Vercel 开源，核心贡献是把"Agent 项目如何像普通代码一样被工程化"这个问题回答清楚，与 R430 Anthropic recursive self-improvement（8x 产出 → 需要 durable infrastructure）形成「AI 加速发展 → 生产级持久化基础设施」对位，**R431 本文新增**

- **[framerslab/agentos](./framerslab-agentos-cognitive-memory-typescript-580-stars-2026.md)** — 580 ⭐，TypeScript，Apache 2.0，**TypeScript 原生 Agent 框架**：认知记忆（CrewAI 同源架构 + 原子事实提取 + 作用域消解）+ 运行时工具锻造（动态生成 + 生命周期管理）+ 多 Agent 编排（角色 + 事件驱动）+ 11 家 LLM Provider 统一抽象 + 与 CrewAI 认知记忆 Article（../context-memory/crewai-cognitive-memory-beyond-rag-architecture-2026.md）形成「方法论层 → TypeScript 工程实现」完整闭环，**R428 本文新增**

- **[superplanehq/superplane](./superplanehq-superplane-control-plane-agentic-engineering-3062-stars-2026.md)** — 3,062 ⭐，Go/Python/React，Apache 2.0，**面向 Agentic Engineering 的开源控制平面**（Canvas directed graph + Event-driven 触发 + Memory 跨执行持久化）+ Agent-friendly CLI（`superplane trigger/watch/logs`）+ 平台工程级集成（GitHub/Jenkins/PagerDuty/Datadog）+ 典型场景：Policy-gated 发布/渐进式 Canary/First 5 分钟故障响应 + 与 Harness Orchestration 主题形成「控制平面 ↔ 编排层」互补闭环，**R427 本文新增**

- **[github/gh-aw](./github-gh-aw-official-agentic-workflow-engine-4631-stars-2026.md)** — 4,631 ⭐，Go/Markdown，MIT，GitHub 官方 Agentic Workflows CLI 与运行时引擎（Markdown → Actions YAML 编译模型）+ 三层安全架构（AWF 沙箱 + Safe Outputs + Threat Detection）+ GITHUB_TOKEN 细粒度权限 + 与 GitHub Agentic Workflows Article 形成「Markdown 编译模型 → Agent-as-CI-Step」完整闭环，**R424 本文新增**

- **[github/copilot-sdk](./github-copilot-sdk-official-multi-language-agent-runtime-9413-stars-2026.md)** — 9,413 ⭐，TypeScript/Python/Go/.NET/Rust/Java，MIT，GitHub 官方多语言 Agent Runtime SDK（GA 正式版）+ 6 种语言共享同一 JSON-RPC 协议 + Hook 系统（5 类拦截点：pre/post_tool_use, session_start, mcp_call, permission）+ MCP 协议支持 + BYOK 模式与 GitHub 生态解耦 + 与 Copilot SDK GA Article 形成「平台化 SDK → Agent Runtime 架构」完整闭环，**R423 本文新增**

- **[github/github-mcp-server](./github-mcp-server-official-github-integration-30k-stars-2026.md)** — 30,683 ⭐，Go，MIT，GitHub 官方 MCP 服务器（Claude Code / Cursor / Codex / OpenCode / Windsurf / VS Code 原生集成）+ 五类工具集（Repository Management / Issue & PR Automation / CI/CD Intelligence / Code Analysis / Team Collaboration）+ 结构化 API 而非 shell 命令 + OAuth/PAT 精确权限控制 + 与 GitHub Copilot SDK 形成「GitHub AI 平台层 → Agent 原生集成」完整闭环，**R422 本文新增**

- **[JuliusBrussee/caveman](./juliusbrussee-caveman-token-compression-skill-72k-stars-2026.md)** — 72,000+ ⭐，JavaScript，MIT，Claude Code Token 压缩技能（65% output tokens 节省 + 100% 技术准确性）+ Brain/Mouth 分离原则（thinking vs output tokens）+ 四档压缩级别（lite/full/ultra/wenyan）+ caveman-shrink MCP 中间件（工具描述压缩）+ cavecrew 子 Agent（60% fewer tokens）+ 学术支撑（arXiv:2604.00025）+ 与 Token Efficiency 工程实践形成「方法论 → 开源实现」闭环，**R420 本文新增**

- **[pewdiepie-archdaemon/Odysseus](./pewdiepie-archdaemon-odysseus-72k-stars-self-hosted-ai-workspace-2026.md)** — 72,000+ ⭐，Python + JavaScript，自托管 AI 工作区（数据完全本地）+ 任意 AI 端点支持（Ollama/API/自建）+ 19 天冲到 72K 星标的增长奇迹 + Bytebase 团队维护 + 与 Agent 数据主权实践形成「隐私优先 ↔ 本地运行」完整闭环，**R421 本文新增**

- **[TencentCloud/CubeSandbox](./tencentcloud-cubesandbox-tired-sandbox-ai-agents-6343-stars-2026.md)** — 6,343 ⭐，Rust，Apache 2.0，**CNCF Landscape**，三层隔离架构（Process / gVisor / Firecracker）+ 60ms 冷启动 + <5MB 内存开销 + E2B SDK 兼容 + CubeCoW 快照引擎（事件级快照/即时克隆/任意回滚）+ CubeEgress 出口网关（凭据注入/域名过滤/访问审计）+ 与 Wayfair ML Research Article（../infrastructure/wayfair-ml-research-agentic-experimentation-loop-2026.md）形成「委托式实验循环 ↔ 硬件级安全执行」完整闭环，**R419 本文新增**

- **[hoangnb24/repository-harness](./hoangnb24-repository-harness-agent-workspace-790-stars-2026.md)** — 790 ⭐，Rust，MIT，多 Agent 工作区 Harness（Claude Code / Codex / Cursor 统一操作层）+ AGENTS.md shim + Feature Intake 流程 + Rust CLI 工具注册 + Story Packet + 验证矩阵 + 决策记录 + 与 Cursor Agent Best Practices Article（..//practices/ai-coding/cursor-agent-best-practices-harness-engineering-2026.md）形成「方法论 → 工程实现」完整闭环，**本文新增**

- **[waltstephen/ArgusBot](./waltstephen-ArgusBot-supervisor-agent-302-stars-2026.md)** — 302 ⭐，Python，MIT，Supervisor Agent 三角色架构（Main Executor + Reviewer + Planner）+ 三元信号量协议（`done`/`continue`/`blocked`）+ 500 轮 max_rounds + Session Resume + Stall Watchdog + Telegram/飞书远程控制 + 与多 Harness 生态 Article（wshobson/agents 插件市场模式）形成「单个 Agent Supervisor ↔ 跨平台插件生态」互补双环，**本文新增**

- **[mukul975/Anthropic-Cybersecurity-Skills](./mukul975-Anthropic-Cybersecurity-Skills-15770-stars-2026.md)** — 15,770 ⭐，Python，Apache 2.0，754 个生产级网络安全 Skills（26 个安全领域）+ 五大框架全映射（MITRE ATT&CK v19.1 / NIST CSF 2.0 / MITRE ATLAS / D3FEND / NIST AI RMF）+ agentskills.io 开放标准 + 跨平台支持（Claude Code / Copilot / Codex / Cursor / Gemini CLI）+ 与 Skills Paradigm Shift Article（../fundamentals/claude-blog-building-agents-with-skills-paradigm-shift-2026.md）形成「范式层 → 工程实现层」完整闭环，**本文新增**

- **[cybernetix-lab/moss-harness](./cybernetix-lab-moss-harness-sci-theory-agent-harness-164-stars-2026.md)** — 164 ⭐，Shell/TypeScript，MIT，SCI 理论驱动的 Agent Harness 模板（六角色 Lane + 双阶段路由 + Cybernetic 反馈循环 + 四级约束系统）+ 运行时控制机制 + 与 LangChain Trace-as-Document Article 形成「运行时控制 ↔ 运行后复盘」完整双环闭环，**本文新增**

- **[nex-agi/Nex-N2](./nex-agi-nex-n2-agentic-thinking-187-stars-2026.md)** — 187 ⭐，Python（sglang fork），Apache 2.0，2026-06-03 新发布，Agentic Thinking 统一推理框架（Adaptive Thinking + Coherent Thinking）+ 目标分解→状态追踪→策略调整→自我校验闭环 + Terminal-Bench 2.1: 75.3 + 与 OpenClaw one-person-company workflows 直接集成 + 与 Nex-N2 Agentic Thinking Article（../fundamentals/nex-agi-nex-n2-agentic-thinking-unified-paradigm-2026.md）形成「Article 分析 ↔ Project 推荐」完整闭环，**本文新增**

- **[darkrishabh/agent-skills-eval](./darkrishabh-agent-skills-eval-589-stars-2026.md)** — 589 ⭐，TypeScript，MIT，Agent Skills 专用测试运行器（Write a SKILL.md, drop in some evals, and find out empirically whether your skill actually makes the model better）+ 三阶段验证（Baseline / With Skill / Diff）+ JSONL 格式的 eval cases + YAML 配置化 + agentskills.io 生态关键缺失填补 + 与 OpenAI Eval-Driven Development Article（evaluator loop + deterministic graders）形成「方法论 → 工程实现」完整闭环，**本文新增**
- **[muratcankoylan/Agent-Skills-for-Context-Engineering](./muratcankoylan-agent-skills-for-context-engineering-16546-stars-2026.md)** — 16,546 ⭐，Python，MIT，CMU+Yale+Harvard 等 9 所院校联合引用的上下文工程技能库（15+ 技能：context fundamentals / multi-agent-patterns / memory-systems / harness-engineering / evaluation / BDI mental states）+ 渐进式激活架构（只加载激活的技能名）+ Claude Code Plugin Marketplace 原生集成 + 与 Anthropic Context Engineering Triple Layer Article（范式层）形成「理论层 ↔ 工程实现层」完整闭环 + 与 Claude Managed Agents Orchestration Article（multi-agent cluster）形成「架构设计 ↔ 技能实现」互补闭环，**本文新增**
- **[agentic-in/inferoa](./agentic-in-inferoa-loop-engineering-harness-108-stars-2026.md)** — 108 ⭐，TypeScript，Apache 2.0，推理原生 Tokenmaxxing Agent Harness（Loop Engineering + vLLM 原生 + Completion Evidence 验证循环）+ 与 R337 Checkpoint/Resume Article（harness cluster）形成「协议定义 ↔ 工程实现」完整闭环，**本文新增**
- **[Picrew/awesome-agent-harness](./picrew-awesome-agent-harness-agent-harness-curated-list-257-stars-2026.md)** — 257 ⭐，Python，Agent Harness Engineering 精选资源列表（implementation-first 原则）+ 按工程组件内在逻辑组织 + 与 ai-boost/awesome-harness-engineering 形成「实现驱动 ↔ 论文驱动」互补闭环，与 Claude Managed Agents Schedule+Vault Article 形成「单一产品功能 ↔ 行业知识体系」完整闭环
- **[XiaomiMiMo/MiMo-Code](./xiaomi-mimo-code-persistent-memory-long-horizon-7006-stars-2026.md)** — 7,006 ⭐，MIT，TypeScript，Xiaomi 长时域 coding agent（三时间尺度框架：Computation + Memory + Evolution + Dynamic Workflow）+ Max Mode 并行采样（+10-20% SWE-Bench）+ Goal 独立验证机制 + 兼容 Anthropic Dynamic Workflow + 脚本可组合 + 中断恢复 + 与 MiMo Code Article 形成「框架分析 ↔ 实证案例」闭环
- **[openai/openai-agents-js](./openai-agents-js-multi-agent-workflows-3193-stars-2026.md)** — 3,193 ⭐，TypeScript，MIT，OpenAI 官方多 Agent 工作流框架（Sandbox Agent + Handoffs + Guardrails + Realtime Agents）+ 内置文件系统隔离工作区 + gitRepo 注入 + 多运行时支持（Node.js/Deno/Bun/Cloudflare Workers）+ 与 Cursor SDK Article（自定义工具/MCP/分类器）形成「同一个工程问题的两种解法」互补闭环，**本文新增**
- **[chopratejas/headroom](./chopratejas-headroom-context-compression-24534-stars-2026.md)** — 24,534 ⭐，Python，Apache 2.0，AI Agent 上下文压缩层（60-95% tokens 节省 + CCR 可逆压缩 + 工具级 MCP）+ SmartCrusher / CodeCompressor / Kompress-base 三算法 + CacheAligner KV 优化 + Cross-agent memory + headroom learn 自动纠正写入 CLAUDE.md + 与 Anthropic Brain/Hand/State 解耦 Article（State 层体积管理）形成「架构层 → 数据层」完整闭环，**本文新增**







- **[visa/visa-vulnerability-agentic-harness](./visa-visa-vulnerability-agentic-harness-2026.md)** — 232 ⭐，Python，Apache 2.0，Visa 开源漏洞代理测试框架（基于 Project Glasswing 经验）+ 三阶段九步骤管道（攻击面映射→多视角研究→结构化报告）+ 多 Agent 确定性投票减少误报 + MTTA（Mean Time to Adapt）核心指标 + SARIF 2.1.0 输出。与 Eval Awareness Article（多 Agent 架构 3.7x 污染放大）形成「风险发现 ↔ 风险验证」互补闭环，**本文新增**

- **[superloglabs/superlog](./superloglabs-superlog-agentic-observability-self-healing-779-stars-2026.md)** — 779 ⭐，TypeScript，Apache 2.0，开源 Agentic Telemetry System（AI Agent 自愈可观测性）+ OTLP intake + 自动 incident 检测 + 可插拔 Agent runner + `npx skills add superloglabs/skills --all` 安装 + 与 Cursor Cloud Agent Lessons（Self-healing environments）形成「自愈能力 ↔ 可观测性」完整闭环，**本文新增**

- **[NVIDIA/SkillSpector](./nvidia-skillspector-agent-skills-security-scanner-2026.md)** — 2,808 ⭐，Python，Apache 2.0，NVIDIA 官方 Agent Skills 安全扫描器（64 种漏洞模式 × 16 个类别）+ 两阶段分析（静态 AST + LLM 语义）+ 支持 OpenAI/Anthropic/NVIDIA API/Ollama + SARIF 输出 + CI/CD 集成。核心数据「26.1% Skills 含漏洞，5.2% 显恶意意图」直接验证 Anthropic Containment 第三层（Content/工具层）风险，与 [Anthropic Containment 三层防御](../harness/anthropic-containment-three-layer-defense-2026.md) 形成「风险论证层 → 工程防御层」完整闭环，**本文新增**

- **[ModelEngine-Group/nexent](./ModelEngine-Group-nexent-zero-code-agent-platform-harness-engineering-5010-stars-2026.md)** — 5,010 ⭐，Python，MIT，零代码 Agent 生成平台（Harness Engineering 原则 + 内置 constraints/feedback loops/control planes）+ 自然语言生成 Agent + OpenAI-compatible any provider + 国产模型切换支持 + Docker/Kubernetes 部署。与 Cursor Auto-review Article（Classifier Agent + 反馈循环 + 自我修正）形成「理论层 → 平台化实现层」完整闭环，**本文新增**

- **[Leonxlnx/taste-skill](./leonxlnx-taste-skill-anti-slop-frontend-40k-stars-2026.md)** — 40,000 ⭐，Shell，MIT，"Anti-Slop Frontend Framework for AI Agents"（风格强制引擎）+ v2 三参数系统（VARIANCE/MOTION/DENSITY）+ GSAP 代码骨架 + Image-to-Code Pipeline + 支持 Cursor/Claude Code/Codex/Gemini CLI/v0/Lovable + 与 Dreaming Article（跨 Session 记忆重组）形成「外部质量（Style Enforcement）↔ 内部质量（记忆重组）」完整双层闭环，**本文新增**

- **[pydantic/logfire](./pydantic-logfire-ai-observability-4251-stars-2026.md)** — 4,251 ⭐，Python，MIT，Pydantic AI 可观测性平台（Rust 引擎 + 结构化 LLM Span + Python 原生 DX）+ 支持 LangGraph/OpenAI/Anthropic 自动 instrumentation + 10k+ spans/s 无明显 overhead，与 LangChain Traces Article（"Tracing 是新源代码"）形成「认知框架 → 工程实现」完整闭环

- **[msoedov/agentic_security](./msoedov-agentic-security-llm-vulnerability-scanner-1899-stars-2026.md)** — 1,899 ⭐，Python，Apache-2.0，LLM / Agent Workflow 漏洞扫描器（多模态攻击面 + 多步迭代 jailbreak + 可编程 fuzzing + RL 对抗样本生成 + MCP stdio server 集成），HTTP spec 适配任何 LLM 端点 + CI 集成（`agentic_security init` 生成 `agesec.toml`）。与 Anthropic 安全工程指南 Article（"AI vulnerability scanning" / "AI vendoring" 两条建议的工程化实现）形成「组织策略层 ↔ 工具实现层」互补闭环，**本文新增**

- **[SuperagenticAI/superclaw](./superagenticai-superclaw-red-team-openclaw-agents-222-stars-2026.md)** — 222 ⭐，Python，Apache 2.0，OpenClaw Agent 红队测试框架（自动化安全回归测试 + 针对性攻击面测试 + MCP 集成系统支持）+ 与 OpenAI URL Safety Article（Agent URL 数据泄露防护）形成「安全机制设计 ↔ 安全机制测试」互补闭环，**本文新增**

- **[antoinezambelli/forge](./antoinezambelli-forge-reliability-layer-self-hosted-llm-tool-calling-2026.md)** — 2,053 ⭐，Python，MIT，可靠性层 for 自托管 LLM 工具调用（Rescue parsing + Retry nudges + Response validation 三层护栏）+ 8B 本地模型从 ~30% 提升至 84% 工具调用成功率 + Proxy Server 模式透明集成 Claude Code + SlotWorker 多 Agent GPU 共享 + 与 Claude Agent SDK Article（工具设计 + 验证闭环）形成「设计哲学 → 工程实现」完整闭环，**本文新增**

- **[sipyourdrink-ltd/bernstein](./sipyourdrink-ltd-bernstein-audit-multi-agent-2026.md)** — 542 ⭐，Python，MIT，审计级多 Agent CLI 编排框架（HMAC-SHA256 审计链 + Signed Agent Cards + Per-artefact Lineage + 确定性 Python 调度器，零 LLM 在协调回路）+ 44 个 CLI Agent 适配器（Claude Code/Codex/Gemini CLI 等）+ 凭证隔离（per-session JWT）+ Git Worktree 并行化 + Air-gap 部署。与 Anthropic Infrastructure Noise Article（资源 headroom 与评测有效性）形成「可靠性工程 ↔ 可重现性工程」互补闭环，**本文新增**

- **[aden-hive/hive](./adenhq-hive-multi-agent-harness-production-2026.md)** — 10,519 ⭐，TypeScript，Apache 2.0，Y Combinator，多 Agent 生产级 Harness（零设置 + 自动拓扑生成 + checkpoint恢复 + 模型无关）+ 四平面实现（编排/运行时/状态/评估）+ 自动演进图结构 + Human-in-the-loop，与 BestBlogs Multi-Agent Systems Engineering Article（orchestration/runtime/state/evaluation 四平面模型）形成「理论框架 → 工程实现」完整闭环

- **[lastmile-ai/mcp-agent](./lastmile-ai-mcp-agent-durable-mcp-patterns-8361-stars-2026.md)** — 8,361 ⭐，Python，Apache 2.0，MCP 协议 + Temporal 耐久层 + Anthropic 官方模式实现（Orchestrator/MapReduce/Evaluator-Optimizer/Router）+ 企业级故障恢复+人工审批节点，与 Claude Fable 5 Article（Minimal Harness + Durable Memory）形成「协议层 → 耐久工程层」完整闭环

- **[shareAI-lab/learn-claude-code](./shareai-lab-learn-claude-code-65666-stars-2026.md)** — 65,656 ⭐，Python，MIT，从零实现 Claude Code Harness 的教学项目（20 个章节：Agent Loop → Tools → Permission → Hooks → Subagent → Skill Loading → Context Compaction → Task System → Agent Teams → MCP 等）+ 核心命题「Agency 是训练出来的，不是写出来的」+ 与 Codex Windows Sandbox（工具安全/隔离引擎）形成「Harness 理论教学 → 真实 OS 层安全实现」完整闭环，**本文新增**

- **[modelcontextprotocol/servers](./modelcontextprotocol-servers-official-mcp-reference-implementation-2026.md)** — 86,949 ⭐，TypeScript/Python/Go，MIT，MCP 官方参考实现仓库（Filesystem/Git/PostgreSQL/Slack/Google Maps 等服务器）+ 协议即接口的设计哲学（结构化工具发现 + 类型安全调用）+ 与 Anthropic Code w/ Claude London 2026 Article（MCP tunnels 企业私有 MCP 服务器连接）形成「协议理论 → 工程实现」完整闭环

- **[ComposioHQ/agent-orchestrator](./ComposioHQ-agent-orchestrator-multi-agent-fleet-2026.md)** — 7,456+ ⭐，TypeScript，MIT，多 Agent 并行编排基础设施（每个 Agent 独立 git worktree + 分支 + PR）+ 自主 CI 修复循环（失败→修复→重验证）+ 统一监督面板（人类只在需要时介入）+ 与 Anthropic 企业调查（57% 多阶段工作流）形成「需求层 → 工程实现层」完整闭环，**本文新增**

- **[danielmiessler/Personal_AI_Infrastructure](./danielmiessler-personal-ai-infrastructure-15392-stars-2026.md)** — 15,392 ⭐，Python/TypeScript，个人智能体工作流操作系统（38 Skills + 20 Hooks + 162 Workflows）+ ISC 追踪系统 + 持久化 PRDs + Agent Teams/Swarm 多智能体协作）+ 与 Anthropic 8 Trends Report 形成「企业趋势 → 个人实践」完整闭环

- **[lsdefine/GenericAgent](./lsdefine-genericagent-self-evolving-token-efficient-12658-stars-2026.md)** — 12,658 ⭐，Python，极简自展 Agent（~3K 行核心代码 + ~100 行 Agent Loop + 9 个原子工具）+ 分层记忆机制（Skill 随使用自动结晶）+ <30K tokens 上下文需求（其他 Agent 的 1/6）+ 多 IM 前端（微信/Telegram/飞书等）+ 自举证明（仓库本身由 Agent 构建）。12K+ Stars 独立归档（Round 299）

- **[google/skills](./google-skills-google-cloud-agent-skills-12259-stars-2026.md)** — 12,259 ⭐，Python，Google 官方 Agent Skills 仓库（Gemini API + BigQuery + Cloud Run + Firebase + GKE + Well-Architected Framework）+ skills.sh 安装协议 + SKILL.md 标准结构 + Apache 2.0 + Skill Registry API 企业自建支持。与「Agent Skills 全面综述」和「addyosmani/agent-skills」形成「社区规范 → 企业级标准」完整闭环，**本文新增**

- **[openai/codex-action](./openai-codex-action-github-action-1042-stars-2026.md)** — 1,042 ⭐，TypeScript，官方 GitHub Action 将 Codex Agent Loop 带入 CI/CD 工作流（PR 自动审查 + 四层安全策略）+ safety-strategy 分层（drop-sudo/unprivileged-user/read-only/unsafe）+ Responses API 代理集成 + Azure OpenAI 支持。与 [OpenAI Codex Agent Loop 架构深度解析](../tool-use/openai-codex-agent-loop-architecture-deep-dive-2026.md) 形成「Agent Loop 理论 → CI/CD 工程落地」完整闭环

- **[mvanhorn/last30days-skill](./mvanhorn-last30days-skill-multi-source-research-skill-2026.md)** — 29,367 ⭐，Python，Claude Code Skill 生态的多源情报合成引擎（Reddit + X + YouTube + HN + Polymarket + GitHub）+ v3 引擎「先规划来源再执行搜索」架构 + SKILL.md runtime spec 可发现性 + SQLite watchlist 跨 session 记忆。与已有的「Skill Opt」（技能训练）和「addyosmani/agent-skills」（技能库）形成「技能工程：合成层 ↔ 训练层 ↔ 标准化层」三层互补，last30days 填补了「多源异构数据合成」这一在 Agent Skills 集群中长期空白的工程实践。
- **[emcie-co/parlant](./emcie-co-parlant-interaction-control-harness-2026.md)** — 18,103 ⭐，Python，交互控制 Harness（上下文动态收窄 + 结构化行为约束）+ 面向客服/销售等 customer-facing 场景 + ARQs 研究驱动 + 快速产品反馈循环。与「Harness Engineering」Cluster（强饱和）形成「通用 Harness 设计 ↔ 客服场景专用 Harness」的互补闭环
- **[livekit/agents](./livekit-agents-realtime-voice-ai-2026.md)** — 10,879 ⭐，Python，实时语音 AI Agent 框架（WebRTC + STT + LLM + TTS 四层管道）+ Silero VAD 打断检测 + MCP 原生支持 + 内置测试框架（LLM as Judge）+ Telephony SIP 集成 + 自托管。与 Claude Code Autonomous Article（checkpoint/subagent/hooks）形成「文本 Agent 工程 ↔ 语音 Agent 工程」互补闭环
- **[farol-team/gnap](./farol-team-gnap-git-native-agent-protocol-2026.md)** — Git-Native Agent Protocol，零服务器零数据库协作协议（4 个 JSON 文件 = 整个协议）+ 任何 Agent 可加入（OpenClaw/Codex/Claude Code/自定义）+ Git 历史即审计日志 + 离线能力 + 人类与 AI Agent 平等参与。与 Cursor 云端 Agent 开发环境（运行环境层）形成「协作协议层 ↔ 执行环境层」互补，共同构成企业多 Agent 工程体系两大支柱
- **[addyosmani/agent-skills](./addyosmani-agent-skills-production-grade-skills-48k-stars-2026.md)** — 48,576 ⭐，Shell/JavaScript，MIT，生产级工程技能库（23 个 SKILL.md + 7 条 slash commands 映射开发周期：/spec→/plan→/build→/test→/review→/code-simplify→/ship）+ 跨 Agent 支持（Claude Code/Cursor/Gemini CLI/Windsurf/OpenCode/Copilot/Kiro/Codex）+ 质量门禁内置验证 + agentskills.io 规范。与 LangChain Deep Agents Skills（按需加载机制）形成「技能标准层 ↔ 按需加载层」互补，共同构成 Agent 技能工程的两个维度

- **[earendil-works/pi](./earendil-works-pi-modular-coding-agent-harness-60k-stars-2026.md)** — 60,223 ⭐，TypeScript，模块化 Coding Agent Harness（coding-agent + agent-core + ai + tui 四包分离）+ 无内置权限系统（默认以用户权限运行）+ 三层容器化方案（OpenShell/Gondolin/Docker）+ 扩展生态（npm 包即插件）。LangChain 在「How to Build a Custom Agent Harness」中引用 pi.dev 作为「极简 Harness + 可组合扩展」的设计参考。与 LangChain Interpreter Article（Interpreter 作为第三 context surface）形成「框架哲学 → 具体实现」的互证：两者都指向同一个工程方向——框架只跑核心 Loop，其余交给扩展

- **[MemoriLabs/Memori](./memorilabs-memori-agent-native-memory-infrastructure-14k-stars-2026.md)** — 14,095 ⭐，Python/TypeScript，SQL-native Agent 内存基础设施（Facts/Preferences/Rules/Summaries 分类）+ LLM-agnostic + Attribution 溯源 + TTL 合规 + 多数据库后端。与 LangChain Interpreter Skills（代码层工作流执行）形成「跨时序状态管理」互补：Interpreter Skills 管 session 内状态，Memori 管跨 session 的结构化记忆

- **[karpathy/autoresearch](./karpathy-autoresearch-autonomous-self-training-agent-81k-stars-2026.md)** — 81,851 ⭐，Python/MIT，Andrej Karpathy 的 630 行自训练系统：给 Agent 一个小型 LLM 训练环境，它修改代码→训练5分钟→检查结果→再修改，循环往复直到满足目标。本质上是 evaluator loop 的实物化——执行→评分→反馈→再执行。与 LangChain RubricMiddleware（Grader sub-agent 驱动的迭代修正）形成「框架层 ↔ 实践层」互补：前者定义 evaluator loop 的工程框架，后者展示同一模式在 LLM 自训练场景的具体实现

- **[Kiln-AI/Kiln](./kiln-ai-kiln-agent-eval-optimization-workbench-4867-stars-2026.md)** — 4,867 ⭐，Python/MIT，Agent Eval + Optimization 工作台（Eval Builder + Auto-Optimize + Subagents + Fine-tuning + Synthetic Data）+ 同一数据集贯穿完整 AI 开发循环 + Git 原生协作 + 本地优先（Ollama 离线可用）+ 190+ 模型库 + MCP 原生，与 OpenAI Monitoring Article（Round 264）形成「检测问题（OpenAI）→ 改进系统（Kiln）」完整工程闭环
- **[CopilotKit/CopilotKit](./copilotkit-agent-frontend-stack-generative-ui-2026.md)** — 32,666 ⭐，TypeScript/React，Agent 前端技术栈 + AG-UI Protocol（Google/LangChain/AWS/Microsoft/Mastra/PydanticAI 采纳）+ 跨平台 Agent 部署（Web+Mobile+Slack+Teams）+ Generative UI + CLHF 自学习 + Human-in-the-Loop，32K Stars 独立归档（Round 263）
- **[ogx-ai/ogx](./ogx-ai-ogx-open-genai-stack-openai-responses-api-8400-stars-2026.md)** — 8,401 ⭐，Python/TypeScript，Open GenAI Stack（Llama Stack 重命名）+ OpenAI Responses API 开源实现（tool calling + MCP + RAG）+ Open Responses conformant + 多 SDK 原生支持（OpenAI/Anthropic/Google）+ pluggable provider（Ollama/vLLM）+ MIT，与 OpenAI Responses API 三元组文章（Shell + Skills + Compaction）形成「概念层 → 开源实现层」完整闭环（Round 262）
- **[simular-ai/Agent-S](./simular-ai-agent-s-11773-stars-osworld-sota-2026.md)** — 11,773 ⭐，Python，GUI 自动化 Agent 框架（OSWorld 72.60% 超越人类基线）+ Agent-Computer Interface（ACI）语义化操作层 + UI-TARS Grounding Model + 三代论文驱动演进（S1 ICLR 2025 Best Paper → S2 COLM 2025 → S3）+ 零样本跨平台泛化，与 Codex Harness Architecture（工具安全理论层）形成「操作层 ↔ 安全层」互补，共同构成完整 Agent 工作区状态管理闭环（Round 261）
- **[nearai/ironclaw](./nearai-ironclaw-12394-stars-wasm-security-agent-harness-2026.md)** — 12,394 ⭐，Rust/WASM，Security-first Agent Harness（WASM 原生沙箱 + 强制隔离 + Routines 可审计工作流 + 持久内存）+ 工具插件沙箱化 + 与 Codex 工具安全设计形成「WASM 强制隔离 ↔ Shell 配置隔离」互补（Round 260）
- **[All-Hands-AI/OpenHands](./openhands-all-hands-ai-swe-agent-2026.md)** — 60,560 ⭐，Python/MIT，开源 Coding Agent（CLI + Local GUI + Cloud + Enterprise 四形态）+ SWEBench 77.6%（当前 SOTA）+ 完整 SDK（可 scale 到 1000+ 并行 agents）+ 支持任意 LLM（Claude/GPT/Ollama）+ 自托管 ZDR + 企业客户（TikTok/VMware/Roche/Amazon）。与 OpenAI Codex Agent Loop（harness 深度解析）形成「Agent Loop 理论 → 生产级 Agent 实现」完整闭环（Round 250）
- **[microsoft/agent-governance-toolkit](./microsoft-agent-governance-toolkit-3604-stars-2026.md)** — 3,604 Stars，Python，Microsoft 开源 Agent 安全治理框架（Privilege Rings + Policy Engine + OWASP Agentic Top 10 全覆盖）+ MCP Security Gateway（Tool Poisoning + Drift Monitoring）+ Saga Orchestration 确定性策略执行，与 Anthropic「Containment Engineering」（环境层硬边界）形成「基础设施层 ↔ 应用语义层」双层安全闭环（Round 197）
- **[OpenBMB/PilotDeck](./openbmb-pilotdeck-workspace-agent-os-2500-stars-2026.md)** — 2,499 Stars，TypeScript，清华 THUNLP 联合开发 Agent 操作系统（WorkSpace 隔离 + 白盒记忆 + Smart Routing + Always-on）+ 按任务难度自动路由模型节省 77% 成本 + MCP 原生支持 + 飞书/微信/Discord IM 集成，与已有的 model routing 文章（llm-model-routing-agent-architecture）形成「理论 → 工程实践」完整闭环（Round 190）

- **[Kilo-Org/kilocode](./kilo-org-kilocode-multi-ide-open-source-agent-2026.md)** — 22,530 ⭐，TypeScript，MIT，**跨平台开源 Coding Agent**：VS Code + JetBrains + CLI + Cloud 四端覆盖 + 500+ 模型无缝切换（GPT-5.5/Claude Opus 4.7/Sonnet 4.6/Gemini 3.1）+ 内置 Plan/Code/Ask/Debug/Review 五类 Agent + MCP Marketplace + Autonomous Mode（`kilo run --auto`）+ OpenCode Fork（163K Stars 上游）。与 [JetBrains Junie Planning-First Article](../ai-coding/jetbrains-junie-planning-first-agent-paradigm-ide-as-harness-2026.md) 形成「IDE 原生规划 ↔ 开源跨平台实现」完整闭环：两者都内置 Plan Agent，Junie 强调 IDE 调试器深度集成，Kilo 强调跨平台一致性，**R451 本文新增**

- **[JetBrains/koog](./jetbrains-koog-jvm-enterprise-agent-framework-4k-stars-2026.md)** — ~4,000 Stars，Kotlin/JVM，JetBrains 开源 Agent 框架，1.0 正式版首个「一年 API 不破坏」承诺 + Stable/Beta 模块分层 + 全平台 OpenTelemetry + Anthropic Prompt Caching 框架级支持，与 koog 1.0 Article 形成「框架定位 → 企业落地路径」完整闭环（Round 189）

- **[Yechan-Heo/oh-my-claudecode](./yeachan-heo-oh-my-claudecode-multi-agent-orchestration-35389-stars-2026.md)** — 35,389 Stars，TypeScript，Claude Code 多 Agent 编排插件（Team Mode + Deep Interview + tmux Workers）+ 零学习曲线自然语言界面，与 wshobson/agents（工具市场）+ mission-control（控制台）形成「工具 → 执行编排 → 统一控制台」完整链路

- **[builderz-labs/mission-control](./builderz-labs-mission-control-open-source-agent-orchestration-dashboard-5081-stars-2026.md)** — 5,081 Stars，TypeScript，Next.js 16 + SQLite 自托管控制台，32 面板（任务/Kanban/成本/安全/eval）+ 四层评估框架（Output/Trace/Component/Drift）+ RBAC + 101 REST API，与 oh-my-claudecode（执行编排层）+ wshobson/agents（工具市场层）形成「执行 → 控制台 → 工具」互补架构

- **[mims-harvard/AutoScientists](./mims-harvard-autoscientists-self-organizing-agent-teams-long-running-experiments-2026.md)** — 241 Stars，Python + Node.js (Claude Code subagents)，自组织 Agent 团队做长周期科学实验（Champion/Challenger 评审 + Evidence Board 共享）+ BioML-Bench 74.4% 平均百分位（+8.33%）+ nanoGPT 1.9× 加速，与 Anthropic「长周期 Agent 工程」（Managed Agents brain-hands 解耦 + Harness 设计）形成「自组织协作 ↔ 中央调度演进」的互补闭环

- **[Purewhiter/mobilegym](./purewhiter-mobilegym-verifiable-mobile-gui-agent-sim-549-stars-2026.md)** — 549 Stars，Python/JavaScript，浏览器托管 Android 模拟环境（28 个仿真 App + 416 个任务模板）+ 确定性 sub-millisecond 判分器（JSON 状态对比）+ 256 并行实例 + 95.1% Sim-to-Real 迁移率，与 UI-Venus（GUI grounding）形成「评测平台 ↔ 模型层」互补，填补手机 GUI Agent 研究中「评测噪声 + 训练不可逆」的双重诅咒（**Round 284 orphan backfill**）

- **[ArcadeAI/arcade-mcp](./ArcadeAI-arcade-mcp-mcp-server-framework-custom-tools-2026.md)** — 915 ⭐，Python，MCP Server Framework（装饰器写工具 + run() 启动服务）+ 三行代码启动 MCP 服务器 + 工具继承与层级化组合 + 跨 Agent 复用，与 Cursor SDK `custom-user-tools` 文章形成「SDK 内部暴露自定义工具 ↔ 独立 MCP 服务」互补闭环（Round 266）

- **[stanford-iris-lab/meta-harness](./stanford-meta-harness-automated-harness-optimization-961-stars-2026.md)** — 961 Stars，Python，Stanford 开源 harness 自动化搜索框架（processor 可组合 + 贝叶斯优化 + 进化算法），Terminal-Bench 2.0 从 69.7%→84.7%（+15pp）+ GAIA 33%→47%（+14pp）+ 可迁移到其他模型和 benchmark，与 Anthropic「Effective Harnesses」和「GAN Architecture」形成「手工设计 → 自动化优化」的 Harness 工程范式转变闭环
- **[anthropics/defending-code-reference-harness](./anthropics-defending-code-reference-harness-vulnerability-discovery-agent-pipeline-2026.md)** — 96 Stars，Python + Claude Code Skills，Anthropic 官方漏洞发现 Agent pipeline 参考实现（recon→find→verify→report→patch 五阶段）+ gVisor 沙箱 + credential 外部化 + egress allowlist 分层安全，与 Anthropic「Containment Engineering」文章形成「理论 → 可复用的工程参考实现」完整闭环

- **[revfactory/harness](./revfactory-harness-team-architecture-factory-4202-stars-2026.md)** — 4,202 Stars，Claude Code Plugin，L3 Meta-Factory / Team-Architecture Factory，自动生成 Agent Team 架构（6 种预置模式：Pipeline/Fan-out-Fan-in/Expert Pool/Producer-Reviewer/Supervisor/Hierarchical Delegation）+ Progressive Disclosure Skills + 跨会话持久化 + Claude Code 原生格式输出，与 Compound Engineering（strategy-compound 工作流）形成「Team 架构自动生成 ↔ 项目知识跨 Agent 积累」的互补

- **[microsoft/SkillOpt](./microsoft-skillopt-text-space-skill-optimization-5423-stars-2026.md)** — 5,423 Stars，Python，Microsoft Research 项目，用文本空间优化的范式训练 Agent 技能（epochs + batch size + learning rate + validation gates，但优化目标是技能文档而非模型权重）+ runtime_state.json 中断恢复 + WebUI 监控 + 6 个 Benchmark 支持（SearchQA/ALFWorld/DocVQA 等）+ 52 个评估 cell 全部最佳/并列最佳，与 Anthropic Containment 工程文章（环境层硬边界）形成「技能层软约束 ↔ 环境层硬边界」互补的 Harness 双轨闭环

- **[peteromallet/desloppify](./peteromallet-desloppify-agent-harness-2875-stars-2026.md)** — 2,875 Stars，Python 3.11+，AI Coding Agent 质量改善 Harness（29 种语言支持）+ 机械检测 + LLM 主观评审双轨 + 状态跨会话持久化 + 防作弊评分 + 全主流 Agent 支持（Claude/Cursor/Codex/Copilot 等），与 Cursor 3 Multi-Agent 协作平台形成「工具层质量守护」的互补
- **[nousresearch/hermes-agent](./nousresearch-hermes-agent-velocity-release-2026.md)** — 173K Stars，Python，The Velocity Release：run_agent.py 从 16K 行压到 3.8K 行（-76%）+ 五轮冷启动优化（Termux 2.9s→0.8s）+ 47% fewer per-turn 函数调用 + 4500× session_search 加速 + Kanban 演变为 real multi-agent platform（orchestrator auto-decomposition + swarm topology + worktree-per-task）+ xAI 深度集成 + Nous-approved MCP catalog，与 Anthropic「Coding agents in social sciences」实证研究形成「速度优化 → 更大规模采用 → 产出分布变化」的主题关联

- **[n8n-io/n8n](./n8n-io-n8n-fair-code-workflow-automation-190k-stars-2026.md)** — 190,102 Stars，TypeScript，Fair-code 工作流自动化平台 + AI 原生（LangChain based）+ MCP Server/Client 双角色 + 400+ 集成 + 自托管/云端双部署，与 Cursor NVIDIA Multi-Agent CUDA Kernel 优化（Planner-Worker 协作）形成「宏观 Multi-Agent 编排 ↔ 工作流引擎层」的工程层次互补

- **[langgenius/dify](./langgenius-dify-agentic-workflow-143k-stars-2026.md)** — 143,002 Stars，TypeScript + Python (Next.js)，生产级 Agentic Workflow 开发平台（Apache 2.0），内置 RAG 管道 + Model Fine-tuning + Agent 编排 + Analytics，与 n8n（流程优先）形成「LLM 应用中心 vs 流程自动化中心」定位互补，n8n vs Dify vs Langflow 三足鼎立格局正式形成

- **[langflow-ai/langflow](./langflow-ai-langflow-visual-multi-agent-148k-stars-2026.md)** — 148,851 Stars，Python/TypeScript，可视化 Multi-Agent 编排平台（React Flow 可视化引擎 + 源码可定制 + MCP Server 内置），LangChain 上层可视化入口，与 Cursor Agent Sandbox 形成「沙箱权限边界 ↔ Multi-Agent 协作结构」不同层次的工程互补

- **[vercel-labs/zerolang](./vercel-labs-zerolang-agent-programming-language-4916-stars-2026.md)** — 4,916 Stars，C，专为 Agent 工作流设计的编程语言（Token 效率 + 零依赖 + 编译器即 API），结构化修复计划输出 + 版本绑定技能系统 + 内置安全隔离声明，Vercel Labs 出品，与「Vercel Labs Zero」形成「同一项目不同阶段」的版本演进补充（Zero 2.1K Stars → ZeroLang 4.9K Stars）

- **[github/copilot-sdk](./github-copilot-sdk-multi-language-agent-sdk-8735-stars-2026.md)** — 8,735 Stars，多语言 SDK（Python/TypeScript/Go/.NET/Java/Rust）+ JSON-RPC 与 Copilot CLI 通信 + BYOK 自有密钥 + 权限分层框架，与 OpenAI Agents SDK 形成「框架层 vs 能力集成层」的目标用户定位对比闭环

- **[strukto-ai/mirage](./strukto-ai-mirage-unified-virtual-filesystem-2693-stars-2026.md)** — 2,693 Stars，TypeScript/Python，统一虚拟文件系统（VFS），让 AI Agent 用 bash 操作 S3/GitHub/Slack/Gmail/Redis 等所有后端，映射到 LLM 最熟悉的 filesystem vocabulary，与 Cursor「自驱动代码库」千 Agent 协作形成「工具层统一抽象 → 多 Agent 并行」的主题关联（关联：千 Agent 协作的障碍之一是每个后端需要不同 API → Mirage 让所有后端变成 `/` 下的子目录）

- **[withcoral/coral](./withcoral-coral-sql-runtime-ai-agents-4863-stars-2026.md)** — 4,863 Stars，Rust/SQL，给 AI Agent 提供统一 SQL 查询层（APIs + Files + Live Sources），benchmark 显示 Claude 准确率 +20%、成本效率 2x（vs 直接 MCP 工具），编码 Agent 任务中 31% 准确率提升、3.4x 成本效率，与 Anthropic「2026 Agentic Coding Trends Report」Multi-Agent 编排趋势形成「工具爆炸 → 统一抽象层」的架构闭环
- **[TencentCloud/CubeSandbox](./tencentcloud-cubesandbox-rust-sandbox-ai-agents-5941-stars-2026.md)** — 5,941 Stars，Rust+KVM，AI Agent 安全沙箱，60ms 启动 + <5MB 内存 + E2B SDK 兼容，硬件级隔离让每个 Agent 代码执行都有零信任防护，与 Anthropic「Dual-Use Risk」Trend 8（安全需从架构层嵌入）形成「理论 → 基础设施层」完整闭环
- **[obra/superpowers](./obra-superpowers-complete-software-engineering-methodology-198k-stars-2026.md)** — 198K Stars，Shell，把 TDD、设计优先、任务分解、人级审查编码为强制执行的 Skills，让编码 Agent 从「想到哪写到哪」变成「按流程执行」，填补强模型容易突破约束的方法论护栏缺口
- **[epiral/bb-browser](./epiral-bb-browser-mcp-browser-use-5376-stars-2026.md)** — 5,376 Stars，TypeScript，CLI + MCP server 让 AI Agent 控制 Chrome 带真实登录态，36 平台 103 命令覆盖 Twitter/GitHub/YouTube/知乎等，与 Claude Seeing Like an Agent 工具设计哲学形成「本地上下文 → 互联网登录上下文」完整闭环（关联：Anthropic 给工具让模型自建上下文 → bb-browser 让 Claude 用真实浏览器访问需要登录的互联网）
- **[mksglu/context-mode](./mksglu-context-mode-mcp-context-window-optimization-15600-stars-2026.md)** — 15,616 Stars，TypeScript，MCP Context 优化四层解法（沙箱工具输出 98% 压缩 + SQLite+FTS5 会话记忆 + Think in Code 范式 + No Prose-Style 尊重模型输出）+ 15 平台覆盖（Claude Code/Gemini CLI/Cursor/Copilot/OpenCode/Zed）+ Hook 强制路由自动注入，与 Anthropic「Code Execution with MCP」Token reduction 98.7% 形成理论层 → 工程执行层完整闭环（关联：Anthropic 解释 WHY → context-mode 展示 HOW）
- **[aaif-goose/goose](./aaif-goose-goose-47302-stars-2026.md)** — 47,302 Stars，Rust，Apache 2.0，本地运行的 Rust 原生 AI Agent（MCP 支持 + ACP 多 Agent 协作 + Hooks 系统权限控制），开源 Claude Code 挑战者，v1.35.0 刚发布（2026-06-07）+ hooks 系统支持 pre/post tool 执行拦截 + PreToolUse denial + 子 agent 召唤。与 Claude Code / Cursor 形成「闭源云端 Agent ↔ 开源本地 Agent」互补，Goose 的 hooks 系统填补了「开源 AI Agent 企业级权限控制」的空白（**Round 284 新增**）

- **[MemPalace/mempalace](./MemPalace-mempalace-open-source-ai-memory-system-52700-stars-2026.md)** — 52,700 Stars，Python，逐字原文存储 + 结构化 Palace 记忆（wings/rooms/drawers）+ 96.6% R@5 raw 检索精度 + 零 API 依赖，本地优先隐私设计，与 Anthropic「上下文工程」Memory 演进路径形成「压缩摘要 vs 原文检索」的核心范式对峙（关联：当前主流记忆方案做摘要 → MemPalace 用数据证明原文检索更精准 → 96.6% R@5 的反直觉验证）
- **[RightNow-AI/openfang](./rightnow-ai-openfang-rust-agent-operating-system-17578-stars-2026.md)** — 17,578 Stars，Rust，Agent 操作系统（14 crates，137K 行 Rust，180ms 冷启动 vs LangGraph 2500ms），7 个自主 Hands + 40 个平台通道 + 16 层安全 + Merkle 链审计 + Tauri 2.0 桌面应用，与 OpenClaw 形成「TypeScript 操作系统 ↔ Rust 操作系统」的双轨对标（关联：OpenClaw 是 TypeScript Agent OS → OpenFang 是 Rust 版 → 两者都是 Agent 操作系统理念的不同实现）

- **[VRSEN/agency-swarm](./VRSEN-agency-swarm-multi-agent-orchestration-2026.md)** — 4,400+ Stars，Python，MIT，OpenAI Agents SDK 多 Agent 编排框架，communication_flows 方向性通信设计 + Type-Safe Tools（Pydantic）+ 状态持久化（load_threads_callback），与 Claude Code Routines（云端调度）形成「协作编排 → 自动化调度」互补闭环（Round 318，**本文重写**）
- **[HKUDS/CLI-Anything](./hkuDS-CLI-Anything-agent-native-37k-stars-2026.md)** — 39,407 Stars，Python，CLI-Anything 将所有专业软件转换为 Agent-Native 接口（Blender/GIMP/LibreOffice），CLI-Hub 生态系统让 Agent 自主发现和安装工具，与 Cursor「第三时代：代码即工厂」主题呼应 → 工具层 Agent-Native 范式转变
- **[netease-youdao/LobsterAI](./netease-youdao-lobsterai-openclaw-powered-agent-product-2026.md)** — 5,176 Stars，TypeScript，网易有道用 OpenClaw 构建的 24/7 全场景个人助手（数据/PPT/视频/邮件），Cowork Mode 让用户始终在环路中，OpenClaw 已纳入企业级产品依赖体系，与 Cursor「第三时代」形成「工具层 → 产品层」的价值链闭环
- **[trycua/cua](./trycua-cua-computer-use-agent-cloud-desktop-17k-stars-2026.md)** — 17,000 Stars，TypeScript/Go，计算机使用 Agent 云端桌面基础设施（Sandbox + Snapshot + Cua-Bench + Training Pipeline），支持 macOS/Windows/Linux/Android，Claude Code / Codex / OpenClaw 的 Computer Use 运行环境，与 Anthropic vs OpenAI Harness 哲学对比（系统级环境设计 ↔ 云端 OS 基础设施 → 理论层 + 基础设施层互补闭环）
- **[tinyhumansai/openhuman](./tinyhumansai-openhuman-personal-ai-super-intelligence-23519-stars-2026.md)** — 23,519 Stars，Rust + TypeScript + Tauri，Personal AI Super Intelligence，Auto-Fetch 20分钟自动轮询 + Memory Tree + Obsidian Vault + TokenJuice 80%压缩，与 Anthropic「Agent 自主性实证研究」形成「快速上下文建立 → 用户信任曲线前置条件」的完整闭环
- **[can1357/oh-my-pi](./can1357-oh-my-pi-hash-anchored-edits-terminal-agent-5336-stars-2026.md)** — 5,336 Stars，TypeScript/Rust，终端级 AI Coding Agent，hash-anchored edits 把首次编辑成功率从 6.7% 提升到 68.3%，LSP+DAP native 集成，与 Anthropic Managed Agents Meta-Harness 理念呼应
- **[garrytan/gstack](./garrytan-gstack-yc-ceo-one-person-engineering-team-2026.md)** — ~100K Stars，TypeScript/Shell，YC CEO 开源的「一人工程团队」技能体系，23 个 specialized slash commands（CEO/Designer/Eng Manager/QA/Security/Release Engineer），810× productivity 倍增实证，与 Cursor Automations 形成「人驱动分工 → 事件驱动值守」的完整 Agent 工作流双轨闭环
- **[yizhiyanhua-ai/fireworks-tech-graph](./yizhiyanhua-fireworks-tech-graph-ai-diagram-generation-7027-stars-2026.md)** — 7,027 Stars，Python/TypeScript，用自然语言生成 publication-ready SVG/PNG 技术图，7 种风格（Flat Icon/Dark Terminal/Blueprint/Notion/Glassmorphism/Claude Official/OpenAI Official）+ AI/Agent 领域专属模式（Mem0/RAG/Multi-Agent/Tool Call），Claude Code Skill 认证，解决技术图生成从「设计问题」变成「描述问题」的核心痛点，与 Cursor「第三 era：AI Coding 工具链」主题形成「AI 生成架构 → 可视化呈现」的完整闭环

- **[openai/symphony](./openai-symphony-linear-agent-orchestration-24471-stars-2026.md)** — 24,471 Stars，Python/Elixir，OpenAI 开源的 Codex 编排规范，把 Linear 任务板变成 Agent 控制台，解决「人盯 Agent Tab」成为系统瓶颈的核心问题，500% PR 增长实证，与 OpenAI Swarm（去中心化通信）形成「中心化状态机 vs 去中心化网络」的编排哲学对比闭环

- **[anomalyco/opencode](./anomalyco-opencode-163k-stars-open-source-coding-agent-2026.md)** — 163,087 Stars，TypeScript，开源编码 Agent，挑战 Cursor 的本地化边界，与 OpenAI WebSocket Mode 形成「传输层优化 → 本地 Agent 能力」的性能闭环

- **[multica-ai/multica](./multica-ai-multica-open-source-managed-agents-platform-29k-stars-2026.md)** — 29,500 Stars，TypeScript/Go，开源 managed agents 平台，Agent 作为第一等公民出现在 Board 上、被分配 Issue、报告进度、创建 PR，与 OpenAI Auto-review 形成「单 Agent 安全 → 多 Agent 协作」的企业级 Agent 工程双轨闭环

- **[juanjuandog/FinSight-AI](./juanjuandog-finsight-ai-resilient-equity-research-workflow-769-stars-2026.md)** — 769 Stars，Java，AI 股票研究 Agent，Redis Lua single-flight + pgvector RAG + 版本化报告 + 六维 RAG 评估，与 Cursor Auto-review 三层权限架构形成「弹性工程 ↔ 权限安全」的生产级 Agent 双轨闭环，**本文新增**

- **[microsoft/agent-framework](./microsoft-agent-framework-1-0-dotnet-python-unified-sdk-2026.md)** — 10,616 Stars，Python + .NET，语义 Kernel + AutoGen 统一 SDK，1.0 GA（2026-04-03），图模型工作流 + DevUI 可视化调试 + MCP + A2A 1.0（即将支持），与 Anthropic「2026 Agentic Coding Trends Report」中 40% 复杂任务已采用多 Agent 编排形成「数据 → 框架」的映射闭环

- **[UditAkhourii/adhd](./UditAkhourii-adhd-adhd-parallel-divergent-reasoning-471-stars-2026.md)** — 471 Stars，TypeScript + Claude Agent SDK，并行发散思维框架（Generator/Critic 机械分离 + 分支硬隔离墙），解决自回归推理中「过早收敛」的结构性问题，5/6 战胜单射基线，+5.17 新颖性 / +7.67 陷阱检测，30 秒安装支持 50+ Agent（Claude Code/Cursor/Codex/Gemini CLI 等），Repowire 官方集成，与 Harness 评估器循环（Evaluator Loop）和 Multi-Agent 隔离协作模式形成「推理质量 ↔ 架构修复」的主题关联

- **[akitaonrails/ai-memory](./akitaonrails-ai-memory-cross-agent-memory-374-stars-2026.md)** — 374 Stars，Rust + SQLite + Markdown，跨 Agent 持久记忆系统（Claude Code/Codex/Cursor/Gemini CLI 等多厂商支持）+ FTS5 全文搜索 + Git 版本化 + Lifecycle hooks 自动捕获 + 零摩擦交接，解决多 Agent 协作中的上下文断裂问题，与 Cursor Cloud Agent Lessons（环境即产品）和 Anthropic Harness 工程（长周期任务状态管理）形成「捕获 → 持久 → 交接」完整记忆工程闭环

- **[withkynam/vibecode-pro-max-kit](./withkynam-vibecode-pro-max-kit-spec-driven-harness-330-stars-2026.md)** — 330 Stars，TypeScript + Shell，Spec-driven coding harness for AI coding agents（Claude Code/Codex/Cursor/Windsurf 等）+ 12 specialized agents + 32 auto-discovered skills + 7 lifecycle hooks + 六阶段 gated workflow（Research → Innovate → Plan → Execute → Test → Update），解决 AI Agent「有智能但无过程」的结构性缺陷——上下文在会话间消亡、文档快速过期、大任务中途崩溃，与 Cursor Cloud Agent Lessons 和 Anthropic Harness 设计形成「过程记忆 → 长周期任务管理 → 多 Agent 协作」的完整工程机制闭环

- **[hoangnb24/harness-experimental](./hoangnb24-harness-experimental-agent-ready-workspace-425-stars-2026.md)** — 425 Stars，Shell + Python，Git Hook 驱动的上下文生成框架，将任意仓库变成 Agent Ready 工作空间（Claude/Cursor/Codex 通用）+ AST 解析生成结构化 `agents.md`/`tools.md`/`context.graph`+ 三层上下文（L1 项目概览/L2 工具管道/L3 架构依赖）+ 每次 `git commit` 自动同步，与「Context Engineering is the moat」社区共识形成「自动化上下文生成 ↔ 手动维护规则」的范式升级闭环

- **[open-multi-agent/open-multi-agent](./open-multi-agent-typescript-multi-agent-orchestration-6156-stars-2026.md)** — 6,156 Stars，TypeScript，Goal-First 多 Agent 编排框架，Coordinator Agent 自动分解目标为 DAG 并行执行，3 个运行时依赖 + Node.js 直插 + 10+ Provider（MCP 支持）+ MIT License，与 Claude Code Harness 质量回退事件（三个 harness 优化静默叠加）形成「编排框架 → 控制层」的互补闭环
- **[ComposioHQ/agent-orchestrator](./composiohq-agent-orchestrator-git-worktree-parallel-2026.md)** — 7,261 Stars，TypeScript，第一个将 git worktree 作为多 Agent 并行隔离机制的编排层，每个 Agent 拥有独立 git worktree（分支级隔离）+ 原生 CI 修复环（culprit identification + 自动重试），与 OpenAI Workspace Agents（团队 Agent 编排）形成「代码层并行隔离 ↔ 流程层团队协作」的完整多 Agent 编排闭环

- **[2508965-ship-it/harmonist-orchestral](./2508965-ship-it-harmonist-orchestral-multi-agent-orchestration-422-stars-2026.md)** — 422 Stars，Python，意图分类驱动的多 Agent 编排引擎，Conductor Protocol + 置信度路由 + 73% token 降低，与 Cursor × Jira 企业集成形成「多 Agent 协作层 → 企业工作流接入」的完整闭环

- **[ZJU-REAL/ClawGUI](./zju-real-clawgui-unified-gui-agent-training-eval-deploy-1256-stars-2026.md)** — 1,256 Stars，Python，浙大统一 GUI Agent 训练/评估/部署框架（clawgui-eval + clawgui-rl + clawgui-agent + clawgui-app 四模块），Online RL 训练 + 标准化 Benchmark + 真实设备部署，与 Anthropic「质量退化复盘」的 Eval 教训形成「评估驱动训练」的完整闭环

- **[cnighswonger/claude-code-cache-fix](./cnighswonger-claude-code-cache-fix-226-stars-2026.md)** — 226 Stars，修复 Claude Code resumed sessions 成本增加 20 倍的 prompt cache regression，直接对应 Anthropic April 2026 postmortem 中的第二个改动（缓存清除 bug）

- **[ArkNill/claude-code-hidden-problem-analysis](./arknill-claude-code-hidden-problem-analysis-108-stars-2026.md)** — 108 Stars，量化分析 Max 计划用户因 Claude Code cache bug 导致的 10-20 倍 token 膨胀，与 Anthropic 公开 postmortem 形成「官方分析 → 社区复现验证」的互补

- **[Pantheon-Security/medusa](./pantheon-security-medusa-9600-ai-security-rules-252-stars-2026.md)** — 252 Stars，Python，AI-first 安全扫描器，9,600+ 检测规则（Prompt Injection、MCP Server 安全、Repo Poisoning、RAG 安全、Agent 安全），支持 `medusa scan --git` 直接扫描任意 GitHub 仓库，96.8% FP 过滤率，与 GitHub Security Lab Taskflow Agent 形成「Agentic 安全研究 → 生产级安全扫描」的完整闭环

- **[GitHubSecurityLab/seclab-taskflow-agent](./githubsecuritylab-seclab-taskflow-agent-mcp-multi-agent-security-2026.md)** — 167 Stars，Python，GitHub Security Lab 开源的 MCP-native 多智能体安全研究框架，基于 OpenAI Agents SDK 构建，三阶段工作流（信息收集→审计判断→报告验证），2 个月审计 40 个仓库发现 91 个漏洞（30+ 已修复），与 MEDUSA 形成「框架研究 → 工具扫描」互补

- **[Imbad0202/academic-research-skills](./Imbad0202-academic-research-skills-11540-stars-2026.md)** — 11,540 Stars，Python，学术研究完整性守卫者（Research → Write → Review → Revise → Finalize），7 层 integrity gates + claim-level audit + citation hallucination detection，与 Anthropic「Eval Awareness」形成「AI 系统完整性验证」的完整闭环（模型能突破评测边界 → ARS 让产出物可审计）

- **[jmerelnyc/photo-agents](./jmerelnyc-photo-agents-vision-grounded-self-evolving-968-stars-2026.md)** — 968 Stars，Python，视觉驱动的分层记忆（Vision-grounded Layered Memory）+ 自编写 Skills（Self-written skills）+ 自主进化（Self-evolving），跨 session 视觉上下文持久化，与 Cursor「第三 era」云端并行 Agent 形成「长时间运行 → 记忆持久化 → 技能自积累」的完整 Agent 自主性闭环

- **[nickvasilescu/hermes-desktop-os1](./nickvasilescu-hermes-desktop-os1-hermes-desktop-os1-native-macos-421-stars-2026.md)** — 421 Stars，原生 macOS workspace for Hermes Agent on Orgo cloud computers and SSH hosts，云端 Agent 与本地工作流深度集成，与 Cursor「第三 era」云端 VM Agent 形成「云端并行 → 本地集成」的互补

- **[vercel-labs/zero](./vercel-labs-zero-agent-first-programming-language-2186-stars-2026.md)** — 2,186 Stars，C，Agent-first 编程语言实验，结构化工具链（JSON 输出）+ 内置标准库 + 无依赖栈，pre-1.0。与 Cursor Composer 2.5 形成「长程 RL 训练 → Agent 执行层语言设计」的完整闭环

- **[Gen-Verse/Open-AgentRL](./gen-verse-open-agentrl-icml-2026-rlanything-2026.md)** — ~490 Stars，Python，ICML 2026 论文，RLAnything（joint optimization of policy + reward + environment）+ DemyAgent（real trajectories > synthetic），与 Cursor Composer 2.5 Targeted RL 形成「联合优化 vs 文本反馈」的 RL 训练双路径闭环

- **[vercel-labs/deepsec](./vercel-labs-deepsec-agent-powered-vulnerability-scanner-2769-stars-2026.md)** — 2,769 Stars，TypeScript，Agent 驱动漏洞扫描器，最大思考级别全量仓库扫描 + 断点续扫 + Vercel Sandbox 并行化，与 OpenAI Codex 安全运行架构形成「运行时控制 → 上线前评测」完整企业级 Agent 安全闭环

- **[CloakHQ/CloakBrowser](./cloakHQ-cloakbrowser-stealth-chromium-18k-stars-2026.md)** — 18,562 Stars，Python/JS，C++ 源码级 Chromium stealth 修改（58 个 fingerprint 补丁），30+ 反爬虫检测系统通过，3 行代码接入（Playwright/Puppeteer 替换），`humanize=True` 行为模拟 + WebRTC leak 封闭 + SOCKS5 代理，与 Anthropic Claude Code Sandboxing 形成「安全隔离 → 行为伪装」双维度的完整 Agent 防护闭环
- **[humanlayer/12-factor-agents](./humanlayer-12-factor-agents-production-llm-applications-20283-stars-2026.md)** — 20,283 Stars，TypeScript，从 12 Factor Apps 汲取灵感，12 条核心原则（NL→Tool Calls、Own your prompts/context、Control flow、Stateless reducer 等），构建生产级 LLM 应用的设计框架。与 Cursor Autoinstall 形成「环境自举 → 应用工程原则」的完整 Agent 质量保障双维度闭环
- **[microsoft/ai-agents-for-beginners](./microsoft-ai-agents-for-beginners-12-lessons-2026.md)** — 12 堂课从零理解 AI Agent 工程实践，50+ 语言翻译，Microsoft Agent Framework + Azure AI Foundry + OpenAI 兼容 provider，与 Cursor SDK「从工具到基础设施」形成「学习路径 → 工程落地」的完整开发者生命周期闭环
- **[suyoumo/ClawProBench](./suyoumo-ClawProBench-667-stars-2026.md)** — 667 Stars，Python，Live-first Agent benchmark harness，102 活跃场景 + FinalScore 复合评分（S^0.40 × r_all^0.45 × r_any^0.15）+ OpenClaw 真实运行时执行，与 Anthropic「Demystifying Evals」形成「评测方法论 → Live Runtime 评测实现」的完整闭环
- **[lemon07r/SanityHarness](./lemon07r-sanityharness-lightweight-coding-agent-eval-harness-222-stars-2026.md)** — 222 Stars，Go，轻量级 coding agent 评测工具，Docker + bubblewrap 双层隔离执行，26 个任务覆盖 6 种语言（Go/Rust/TS/Kotlin/Dart/Zig），BLAKE3 完整性验证 + 经验推导难度加权，与 Anthropic「AI 抗性评估」形成「评测设计理念 → 工程实现」的闭环
- **[romanklis/openclaw-contained](./romanklis-openclaw-contained-gvisor-capability-agent-sandbox-28-stars-2026.md)** — 28 Stars，gVisor 用户态内核隔离 + capability-based 权限审批 + 完整审计日志，生产级 Agent 沙箱编排，TaskForge 实现与 Anthropic Managed Agents「解耦 brain/hands」形成「安全隔离 → 架构解耦」的完整闭环
- **[nearai/ironclaw](./nearai-ironclaw-wasm-sandbox-agent-os-12283-stars-2026.md)** — 12,283 Stars，Rust，WASM 沙箱 + Docker 隔离 + Capability-Based 权限模型 + 凭证边界注入 + Prompt 注入防御 + 端点白名单，跨平台安全 Agent OS，与 OpenAI Codex Windows 沙箱形成「Windows 原生 ACL/Token 方案 → 跨平台 WASM+Docker 方案」的完整安全范式对比闭环
- **[Tencent/AICGSecEval](./tencent-aicgseceval-repository-level-ai-code-security-benchmark-944-stars-2026.md)** — 944 Stars，腾讯「悟智·代码安全评测」，仓库级 AI 生成代码安全基准测试，覆盖 29 种 CWE 漏洞类型，与 Anthropic「Eval Awareness」形成「评测可被模型破解 → 需要更难绕过的评测框架」的完整闭环
- **[mattpocock/skills](./mattpocock-skills-agent-grilling-harness-85764-stars-2026.md)** — 85,764 Stars，Shell，技能体系解决 Agent「做错需求」的核心痛点，grilling session 对齐期望 + ubiquitous language 统一术语 + SPEC.md 定义规格，与 Anthropic Managed Agents 解耦设计形成「软约束（Skills）→ 硬约束（架构）」的互补

- **[NousResearch/hermes-agent](./nousresearch-hermes-agent-v014-165k-stars-2026.md)** — 165,000+ Stars，Python，自改进 AI Agent 运行时，v0.14.0（2026-05-16）新增：Kanban 持久化任务板 + Checkpoints v2 + 22 个消息平台（LINE/SimpleX Chat）+ xAI Grok SuperGrok OAuth + Lazy-install 架构（冷启动 19s 优化），90 天积累 165K Stars，与 Cursor Bugbot Usage-based Pricing 形成「开源自改进 vs 闭源商业化」的完整 Agent 生态双轨闭环
# 🗺️ Projects Map

> 本目录存放 GitHub Trending 高价值项目推荐文章
> - **[DietrichGebert/ponytail](./dietrichgebert-ponytail-yagni-coding-agent-skill-1240-stars-2026.md)** — 1,240 Stars，MIT，YAGNI 原则驱动的 Coding Agent 极简框架（80-94% 代码减少 + 47-77% 成本降低 + 3-6× 提速），决策层次链（YAGNI→stdlib→平台原生→依赖→一行代码）+ 跨 Claude Code/Codex/Pi/OpenCode 四平台支持，与 R361 OpenAgentsControl（plan-first approval gates）形成「事前约束 + 事中极简」双轨质量守护，**R368 本文新增**
> - **[awslabs/agent-plugins](./awslabs-agent-plugins-aws-agent-plugin-system-multiple-platforms-2026.md)** — AWS 官方 Agent 技能插件系统，Skills/MCP/Hooks/References 四层封装，Claude Code/Codex/Cursor 多平台复用，与 Anthropic 三元 Harness 架构形成「Planner（Skills）→ Generator（MCP）→ Evaluator（Hooks）」的完整企业级实现，Claude Code/Cursor 可直接从 marketplace 安装
> - **[czlonkowski/n8n-mcp](./czlonkowski-n8n-mcp-mcp-server-n8n-workflow-automation-20962-stars-2026.md)** — n8n 工作流自动化 MCP 服务器，20,962 Stars，MCP 协议接入 1,650 个 n8n 节点（820 核心+830 社区），99% 节点属性覆盖 + 63.6% 操作覆盖 + 87% 文档覆盖，与 Claude Code Auto Mode 形成「动作安全性（Auto Mode）→ 动作来源（n8n-MCP）」的企业级 Agent 落地双维度覆盖
- **[tinyhumansai/openhuman](./tinyhumansai-openhuman-personal-ai-super-intelligence-5658-stars-2026.md)** — Personal AI super intelligence 运行时，7,680 Stars（2026-05-14，5,658→7,680），Rust + TypeScript 双技术栈，Memory Tree + Obsidian Vault + 118+ OAuth 集成 + TokenJuice 80% 压缩 + 内置模型路由（reasoning/fast/vision）+ Native Voice（STT + ElevenLabs TTS），与 Cursor 云端开发环境形成「云端并行 Agent → 本地持久记忆基础设施」的互补
- **[onyx-dot-app/onyx](./onyx-open-source-ai-platform-enterprise-rag-29k-stars-2026.md)** — 29K Stars，Python，企业级开源 AI 平台（RAG + Deep Research + 50+ Connectors）+ MCP Native + Docker/K8s 双部署 + Standard/Lite 双模式，与 OpenAI Shell+Skills+Compaction 形成「平台数据连接 ↔ Agent 工程原语」互补闭环（Round 243）
- [liust/Tactile](./liust-Tactile-accessibility-first-agent-operating-layer-178-stars-2026.md) — 无障碍语义优先的 Agent 操作层，178 Stars，Python，将「截图→坐标→点击」倒转为「语义→坐标→验证」，操作准确率接近 100%，token 消耗降低 60-80%，与 Anthropic April Postmortem 复合效应分析形成「操作层噪声 → 系统性可调试性」的互补
- [zed-industries/zed](./zed-industries-zed-multiplayer-code-editor-82800-stars-2026.md) — 高性能多人代码编辑器，82,800 Stars，Rust 内核 + Tree-sitter 内置解析，10 倍于 VS Code 的性能，Atom/Tree-sitter 创始团队作品，多人协作直接做进编辑器内核
- [warpdotdev/warp](./warpdotdev-warp-modern-terminal-agents-58461-stars-2026.md) — 现代化终端 + 云端 Agent 编排平台，58,461 Stars，Rust UI 框架 + Oz 云端并行 Agent + 命令历史智能搜索，把终端变成 AI 时代的开发者控制台
- [slopus/happy](./slopus-happy-mobile-claude-code-20718-stars-2026.md) — 移动端 Claude Code/Codex 控制台，20,718 Stars，Expo 构建 + 端到端加密 + 推送通知实时介入，躺在沙发上也能控制 AI 编码 Agent 的工作进度
- [Yechan-Heo/oh-my-codex](./yeachan-heo-oh-my-codex-codex-workflow-layer-28856-stars-2026.md) — Codex Workflow Layer，28,856 Stars，$deep-interview→$ralplan→$ralph/$team 标准流程 + 多 Agent 并行（tmux）+ .omx/ 状态持久化，与 OpenAI Hooks GA 形成「接口规范 → 具体实现」闭环（关联：OpenAI 定义 Hooks 接口 → OMX 给出基于 Hooks 的 workflow 实现）
- [getpaseo/paseo](./getpaseo-paseo-multi-agent-interface-6141-stars-2026.md) — 统一多 Agent 控制界面，6,141 Stars，Daemon 架构 + 跨设备客户端 + Skills 编排协议，Claude Code/Codex/OpenCode 一个界面全搞定
- [KeWang0622/agent-zero-to-hero](./KeWang0622-agent-zero-to-hero-14-stars-2026.md) — 从零构建 Claude-Code 形态的 Agent Harness，14 Stars，7 周课程 + 19 章节 + 4500 行 Python + 42 测试，6 行核心 Loop 代码揭示所有编码 Agent 本质，与 Cursor Bootstrapping Autoinstall 形成「RL 环境自举 → 工程落地」的完整闭环
- [YuxiaoWang-520/harness-craft](./harness-craft-86stars-2026.md) — 可组合 AI Coding Skills/Rules 库，86 Stars，YC CEO 背书，46 Skills + 15 Rules，Claude/Codex 双平台支持，将 Agent 从「prompt tricks」升级为「工程化持久系统」，与本文「AI Coding 工程化范式转移」形成「范式定义 → 工程实现」闭环
- [Chen-zexi/open-ptc-agent](./Chen-zexi-open-ptc-agent-programmatic-tool-calling-716-stars-2026.md) — 716 Stars，Python，Programmatic Tool Calling 开源实现，Daytona 沙箱安全执行 + LangChain 集成 + 85-98% token 降低，与 Anthropic Advanced Tool Use 三项突破形成「理论 → 开源实现」完整闭环
> **防重索引**：已推荐项目的 GitHub URL 列表（避免重复推荐）

---

- [youcheng0526/n8n-mcp](./youcheng0526-n8n-mcp-n8n-mcp-server-20751-stars-2026.md) — N8N MCP Server，20,751 Stars，TypeScript，N8N Workflow Engine 作为 AI 工具调用后端，150+ 内置集成 + 自定义工具定义，让 Workflow Automation 成为 Agent 的可编程工具层，与 OpenAI Codex Windows 沙箱架构形成「工具定义 → 工具执行」的互补（关联：沙箱提供安全执行边界 → n8n-mcp 提供工作流编排工具抽象 → Agent 的完整工具链）
- [yetone/native-feel-skill](./yetone-native-feel-skill-agent-skill-cross-platform-desktop-914-stars-2026.md) — Agent Skill 让 AI 生成跨平台桌面应用感觉像本地原生，914 Stars，8 条架构原则 + 四层架构 + WebKit/WebView2 生存指南 + 75 项 Ship Audit，与 OpenAI Codex Windows 沙箱架构形成「平台能力缺口」的同一主题双视角（关联：Codex 沙箱因 Windows 缺乏原生隔离原语而复杂 → native-feel-skill 因 Windows 缺乏原生交互范式而需要架构约束）

- [CloakHQ/CloakBrowser](./CloakHQ-cloakbrowser-source-level-stealth-chromium-2026.md) — 源码级反检测 Chromium，797 Stars，49 个 C++ 补丁 + `humanize=True` 人类行为模拟，30+ 检测站点通过 + 0.9 reCAPTCHA v3，3 行代码替换 Playwright/Puppeteer，与 Cursor「第三代」云端 Agent 形成「环境配置 → 安全执行」完整闭环（关联：Cloud Agent 操作真实网站 → Cloudflare 等反爬拦截 → CloakBrowser 让 Browser Agent 真正工作）
- [obra/superpowers](./obra-superpowers-agentic-skills-software-development-methodology-2026.md) — 完整软件工程方法论的 Agent Skills 框架，强制 TDD + 设计优先 + 子代理驱动开发，支持 Claude/Codex/Cursor 等 8 平台，Claude 可自主工作数小时不偏离计划，与本文 Codex Windows 沙箱架构形成「安全执行 → 工程方法论」的完整 Agent 工具链闭环
- [K-Dense-AI/scientific-agent-skills](./K-Dense-AI-scientific-agent-skills-135-scientific-research-skills-2026.md) — 135 个科研 Agent Skills，覆盖生物信息学/药物发现/医学影像/地理空间等 15 个科学领域，基于开放 Agent Skills 标准，与 Cursor Autoinstall 形成「通用环境自举 → 专业领域 Skills」的互补（关联：Autoinstall 用旧版本模型初始化 → Scientific Skills 提供 135 个专项领域知识 → 两条路径解决同一问题：Agent 能力如何专业深化）
- [strukto-ai/mirage](./strukto-ai-mirage-unified-vfs-1922-stars-2026.md) — 统一虚拟文件系统，1,922 Stars，将 S3/Slack/GitHub/Gmail 等 15+ 服务挂载为文件系统路径，Agent 用熟悉的 bash 工具（`cat`/`grep`/`cp`）操作一切，与 Cursor 模型亲和性 Harness 文章形成「工具层抽象 vs 模型层适配」的正交关系（关联：OpenAI patch 格式 vs Claude string replacement → Mirage 统一为 filesystem API → 模型特异性被隐藏）

- [garrytan/gstack](./garrytan-gstack-yc-ceo-ai-software-factory-93788-stars-2026.md) — YC CEO Garry Tan 的 AI 软件工厂，93,788 Stars，将 Claude Code 变成 23 角色虚拟工程团队（CEO/设计师/安全官/QA 等），810x 生产力提升，与 PayPal Cursor 案例形成「个人 → 企业」完整 Agent 工具链光谱

- [google/agents-cli](./google-agents-cli-google-cloud-agent-factory-2272-stars-2026.md) — Google 官方 Agent 部署 CLI + Skill 库，2,272 Stars，支持 Claude Code / Codex / Gemini CLI / any，7 个核心 Skill 覆盖 scaffold→eval→deploy 全链路，与 Cursor「第三代」云端 Agent 工厂形成「范式定义 → 工程实现」闭环（关联：第三代 → 云端 VM 并行 + Artifacts 交付 → agents-cli 提供部署/评估/可观测性标准工具）

- [NousResearch/hermes-agent](./NousResearch-hermes-agent-self-improving-agent-2026.md) — 自改进 AI Agent，支持 Telegram/Discord/Slack/WhatsApp 等多平台，`hermes model` 任意切换 LLM provider（200+ 模型），$5 VPS 可跑，与 Cursor Autoinstall 形成「Agent 自我改进循环」的互补（关联：Autoinstall 用上一代 Composer 配置环境 → Hermes Agent 用当前 session 经验创建 Skill → model helps itself improve 的两条路径）

- [itsuzef/goalkeeper](./itsuzef-goalkeeper-contract-driven-claude-code-5-stars-2026.md) — 合约驱动的 Claude Code 目标执行框架，5 Stars，2026-05-11 创建，独立 Judge 子代理对抗 Definition of Done，反占位符规则自动拒绝 stub/`.todo`/`it.only`，与 Augment AGENTS.md 研究形成「配置定义 → 完成验证」的完整闭环（关联：Augment 发现好 AGENTS.md = Haiku→Opus 升级 → Goalkeeper 定义 DoD + Judge 验证完成 = 结构化配置工程的两个维度）

- [colbymchenry/codegraph](./colbymchenry-codegraph-pre-indexed-knowledge-graph-2955-stars-2026.md) — 预索引代码知识图谱，2,955 Stars，TypeScript，92% 工具调用减少（52→3）+ 71% 加速，Claude Code Explore agent 专用 `codegraph_explore` 工具替代 grep/find/ls，与 Cursor 3.3 Build in Parallel 形成「单 Agent 高效探索 → 多 Agent 并行执行」的完整工作流

- [huggingface/skills](./huggingface-skills-interoperable-agent-tools-1881-stars-2026.md) — Hugging Face 官方 Agent Skills 库，1,881 Stars，标准 SKILL.md 格式，interoperable with Claude Code / Codex / Gemini CLI / Cursor，与 Cursor Autoinstall 形成「训练环境自动化 vs 工具定义标准化」的互补

- [anthropics/skills](./anthropics-skills-official-agent-skills-implementation-2026.md) — Anthropic 官方 Agent Skills 开源仓库，SKILL.md 极简格式 + 生产级 docx/pdf/pptx/xlsx 技能实现 + Claude Code 插件市场集成，与 Cursor Autoinstall 形成「技能定义 → 技能执行」的完整闭环

- [aattaran/deepclaude](./aattaran-deepclaude-claude-code-brain-swap-229-stars-2026.md) — Claude Code Brain Swap 方案，229 Stars，DeepSeek V4 Pro（$0.87/M）替换 Claude Opus（$15/M），90% 成本降低 + mid-session 切换，与 Anthropic Managed Agents Brain/Hands 解耦形成「Harness 抽象层」的互补（关联：Body 固定 → Brain 可换 → Claude Code harness 的真实价值在 tool loop 而非模型）
- [asamassekou10/ship-safe](./asamassekou10-ship-safe-agent-permission-security-scanner-699-stars-2026.md) — Agentic 时代 CLI 安全扫描器，699 Stars，专门检测 CI/CD 错误配置、Agent 权限蔓延风险、MCP 工具注入、硬编码密钥和 DMCA 标志 AI 依赖，与 Anthropic 2026-04 事后分析形成「事后分析 → 事前防御」互补（关联：Anthropic 三类改动导致质量退化 → ship-safe 在 Agent 伤害生产环境前拦截权限配置问题）
- [anthropics/financial-services](./anthropic-claude-for-financial-services-one-source-two-ways-skill-bundling-architecture-21236-stars-2026.md) — Anthropic 官方金融领域 Agent 参考仓库，21,236 Stars，同一 Skill 文件同时服务 Claude Cowork 插件（人类主导）和 Managed Agent API（autonomous 执行），9 个具名 Agent + 6 个 vertical plugins + 11 个 MCP 数据连接器，代表 2026 年 Agent 技能复用的核心架构模式（关联：本文 Skill Bundling 架构 → 一次编写双重部署 → financial-services 作为生产级参考实现）

- [Liu-PenPen/skill-reviewer](./Liu-PenPen-skill-reviewer-skill-quality-enforcement-2026.md) — 给 Agent Skill 做 Code Review 的 Skill，17 Stars，2026-05-11 创建，10 条可检测 rubric + P0–P3 分级 + 零依赖 lint 脚本，与 Cursor「Better AI Models」研究形成「管理 AI 输出」趋势的工具化实现（关联：代码审查 +51% → Skill 成为基础单元 → Skill Review 成为质量门禁）

- [scottgl9/skelm](./scottgl9-skelm-secure-agentic-workflows-typescript-2026.md) — TypeScript 原生安全 Agent 工作流框架，17 Stars，2026-05-03 创建，默认拒绝（default-deny）安全模型 + 嵌入式 CONNECT 代理 + per-agent workspace 隔离，与 Cursor Agent Harness 测量驱动质量形成「质量优化 vs 安全边界」的互补（关联：测量驱动改进 → 安全边界内置 → skelm 将安全从护栏变为工作流定义的内置约束）

- [Storybloq/storybloq](./Storybloq-storybloq-cross-session-context-persistence-217-stars-2026.md) — 跨会话上下文持久化，217 Stars，TypeScript，`.story/` 文件约定 + CLI + 43 工具 MCP Server + `/story` Skill，让每次 Claude Code session 变成可积累的建设块而非重置，与 Cursor Composer Autoinstall 形成「环境自动化 vs Session 连续性」的互补（关联：RL 训练环境自动化 → 跨天/跨 session 的长程 Agent 上下文断点问题）
- [openclaw/clawbench](./openclaw-clawbench-trace-based-agent-benchmark-89-stars-2026.md) — 追踪评分优先的 Agent 评测框架，89 Stars，评分完整技术栈（harness + config + model）而非仅 LLM，13 种失败模式检测 + 47.3% 方差分解为噪声，与 Anthropic April Postmortem 形成「配置变更风险 → 系统性评测」的完整闭环
- [itsuzef/goalkeeper](https://github.com/itsuzef/goalkeeper) — 合约驱动的 Claude Code 目标执行框架，独立 Judge 子代理对抗 Definition of Done

- [kruschdev/krusch-context-mcp](./kruschdev-krusch-context-mcp-unified-ide-context-engine-61-stars-2026.md) — 统一 IDE 上下文引擎，61 Stars，Node.js + PostgreSQL + SQLite + Ollama 本地向量，一个 MCP Server 提供 18 个工具（情景记忆 + 语义代码搜索 + Nuggets + Zero-Trust Deep Search），零 API 成本 + 全数据主权，与 Cursor 动态上下文发现形成「方法论 → 工程实现」闭环（关联：Cursor 动态上下文发现 → 文件作为上下文原语 → Krusch Context MCP 系统性实现）

- [coleam00/adversarial-dev](./coleam00-adversarial-dev-gan-style-three-agent-harness-2026.md) — GAN 风格三代理编码 Harness 的生产级实现，108 Stars，TypeScript，双 SDK（Claude Agent SDK + Codex SDK）支持，Sprint Contract 协商机制 + JSON 结构化反馈，Evaluator 主动攻击机制驱动质量提升，与 Anthropic GAN-Style 三代理架构论文形成「理论 → 工程实现」闭环（关联：GAN 三代理架构 → adversarial-dev 生产级实现 → Sprint Contract + 双 SDK 支持）

- [Agent-Threat-Rule/agent-threat-rules](./Agent-Threat-Rule-agent-threat-rules-open-detection-standard-109-stars-2026.md) — Agent 安全检测开放标准，109 Stars，311 条规则覆盖 9 大威胁类别（prompt injection/agent manipulation/skill compromise 等），映射 OWASP Agentic Top 10（10/10）+ SAFE-MCP（91.8%），96,096 真实 Skills 扫描发现 751 个 malware samples，NVIDIA Garak benchmark 97.1% recall，6 周 7 个生态整合（Microsoft/Cisco/NVIDIA Garak 等），与 Anthropic Trustworthy Agents 形成「安全框架 + 检测标准」的完整闭环（关联：Trustworthy Agents → 四层安全架构 → ATR 检测规则 → OWASP 映射 → 真实威胁发现）

- [OptimAI-Lab/CudaForge](./OptimAI-Lab-CudaForge-training-free-multi-agent-cuda-kernel-2026.md) — 训练免费的多智能体 CUDA Kernel 生成工作流，80 Stars，Python，模拟人类专家的迭代工作流（开发→测试→分析硬件反馈→迭代改进），与 Cursor Multi-Agent Kernel 实验形成「规范驱动协调」的互补（关联：Markdown 协调规范 → 开源工作流实现 → CudaForge SKILL.md 驱动）

- [Fangcun-AI/SkillWard](./Fangcun-AI-SkillWard-security-scanner-agent-skills-2026.md) — Agent Skills 安全扫描工具，123 Stars，Python，三阶段扫描（静态分析 + LLM 评估 + Docker 沙箱执行），实测 5,000 个 Skills 中 ~25% 标记不安全，约 1/3 可疑样本在沙箱中暴露运行时威胁，与 OpenAI Codex Safe Deployment 形成「发布前扫描 + 运行控制」的安全闭环（关联：Codex 安全运行架构 → Skills 部署前的安全检查 → SkillWard 三阶段漏斗）

- [kangarooking-system-prompt-skills-15-design-patterns-2026](./kangarooking-system-prompt-skills-15-design-patterns-2026.md) — 15 个可执行的系统提示词设计模式，64 Stars，从 165 个顶级 AI 产品系统提示词中蒸馏，覆盖 persona/tool/safety/memory 等 15 个维度，与 OpenAI Agents SDK Skills 原语形成「标准定义 → 设计模式参考」的互补（关联：OpenAI Agents SDK → Skills 已成为标准原语 → system-prompt-skills 提供具体设计模式）

- [strukto-ai-mirage-unified-virtual-filesystem-1612-stars-2026](./strukto-ai-mirage-unified-virtual-filesystem-1612-stars-2026.md) — 统一虚拟文件系统，1,612 Stars，TypeScript，将 S3/Gmail/GitHub/Slack 等后端挂载为文件目录，让 AI Agent 用原生 bash 工具操作一切数据源，与 OpenAI Codex Agent Loop 形成「工具抽象 vs 上下文管理」的互补（关联：Codex Agent Loop → 长程 Agent 需要统一的工具抽象层 → Mirage VFS 的工程实现）

- [rowboatlabs-rowboat-local-first-ai-coworker-13666-stars-2026](./rowboatlabs-rowboat-local-first-ai-coworker-13666-stars-2026.md) — 本地优先的 AI coworker，13,666 Stars，TypeScript，构建持久知识图谱 + Gmail/Calendar/Notion 深度集成，与 Cursor Long-Running Agents 形成「工作流控制 + 上下文积累」的互补（关联：规划优先 Harness 架构 → 长程 Agent 需要外部化的上下文积累机制）

- [claude-code-memory-setup-obsidian-graphify-token-optimization-2026](./claude-code-memory-setup-obsidian-graphify-token-optimization-2026.md) — 71.5x Token 优化的 Claude Code 记忆方案，Obsidian Zettelkasten + Graphify 知识图谱 + Chat Import Pipeline 三层体系，499x 查询 token 节省，0 token 生成成本（AST 模式），跨项目知识复用（关联：Cursor 3 第三时代 → 长程 Agent 上下文连续性 → 记忆基础设施的系统性解决方案）

- [agentmemory-persistent-memory-ai-coding-agents-2026](./agentmemory-persistent-memory-ai-coding-agents-2026.md) — 免 DB 的持久记忆基础设施，iii engine 实现零外部依赖，95.2% R@5 检索精度 + 92% token 节省，16+ Agent 共享统一记忆服务器（关联：Anthropic Measuring Agent Autonomy → 长程 Agent 的上下文坍缩问题 → 记忆基础设施的系统性解决方案）

- [agent-squad-2fastlabs-multi-agent-orchestration-2026](./agent-squad-2fastlabs-multi-agent-orchestration-2026.md) — 意图分类驱动的多 Agent 编排框架，AWS Labs → 2FastLabs，Classifier-First 动态路由 + SupervisorAgent 并行协调（关联：Anthropic Managed Agents Brain-Hands 解耦 → 多 Agent 入口层智能路由问题的一体化回答）

- [clampdown-89luca89-zero-trust-sandbox-agent-2026](./clampdown-89luca89-zero-trust-sandbox-agent-2026.md) — 零信任沙箱推荐，Landlock + Seccomp + 零密钥架构，与 Anthropic Auto Mode 形成技术互补（判断 vs 强制）

- [greyhavenhq-greywall-container-free-agent-sandbox-183-stars-2026](./greyhavenhq-greywall-container-free-agent-sandbox-183-stars-2026.md) — 183 Stars，Go，无需 Docker 的内核级 Agent 沙箱（Landlock + Seccomp BPF + eBPF 五层防护），--learning 自动生成最小权限配置，与「多 Agent 并行开发」文章形成「并行协调（Git Lock）→ 安全隔离（Greywall）」的完整 Agent 工程闭环

- [CloakHQ-cloakbrowser-source-level-stealth-chromium-2026](./CloakHQ-cloakbrowser-source-level-stealth-chromium-2026.md) — 源码级反检测 Chromium，797 Stars，49 个 C++ 补丁 + `humanize=True` 人类行为模拟，30+ 检测站点通过 + 0.9 reCAPTCHA v3，3 行代码替换 Playwright/Puppeteer，与 Cursor「第三代」云端 Agent 形成「环境配置 → 安全执行」完整闭环（关联：Cloud Agent 操作真实网站 → Cloudflare 反爬拦截 → CloakBrowser 让 Browser Agent 真正工作）

- [open-code-review-multi-agent-code-review-2026](./open-code-review-multi-agent-code-review-2026.md) — 多评审者对抗式代码审查框架，28 种评审者人格 + 辩论机制 + GAN 风格对抗评审（关联：GAN 三代理架构 → 多评审者对抗式代码审查工程实现）

- [prompt-tower-context-packaging-376-stars](./prompt-tower-context-packaging-376-stars-2026.md) — VS Code 上下文打包插件，376 Stars，1,000+ 用户，将代码库上下文一键打包为 AI 可消费的 XML 结构，与 Cursor 动态上下文发现形成互补（预打包 vs 动态拉取）

[gsd-2-gsd-build-autonomous-coding-agent-7269-stars-2026](./gsd-2-gsd-build-autonomous-coding-agent-7269-stars-2026.md) — 生产级自主编码 Harness，7269 ⭐，DB 权威状态 + Auto Pipeline + Milestone/Slice 机制，Pi SDK 构建，真正实现"一次命令，几个月不管"的无人值守编码（关联：Anthropic 长程 Agent 双组件架构 → 生产级工程实现）

- [awslabs/aidlc-workflows](./awslabs-aidlc-workflows-structured-ai-driven-development-2026.md) — AWS 出品的 Agent 开发生命周期方法论，1847 ⭐，三阶段（Inception→Construction→Operations）+ 六合一安全扫描 + 8 平台适配层（关联：Claude Code April Postmortem 质量回退 → 结构化 Human-in-the-loop 的工程实现）
- [agentmemory-persistent-memory-4902-stars-2026](./agentmemory-persistent-memory-4902-stars-2026.md) — 免 DB 的 Agent 持久记忆，4902 Stars，BM25+Vector+Graph 混合检索（RRF fusion），95.2% R@5 + $10/年 + 零 API 成本，与本文配置性降级形成「平台层缓存污染 → 工具层外部记忆」的互补关系
- [rohitg00/agentmemory（21564⭐）](./rohitg00-agentmemory-persistent-memory-21564-stars-2026.md) — 认知记忆的生产级实现：CrewAI 五操作框架（encode/consolidate/recall/extract/forget）的工程落地，LongMemEval-S R@5=95.2%，12 auto hooks 零手动捕获，多 Agent 共享记忆服务器，与《认知记忆五操作》形成理论与实践闭环
- **[KeygraphHQ/shannon](./keygraphhq-shannon-ai-pentester-2026.md)** — AI 渗透测试器，白盒安全测试 + 真实 exploitation 验证 + 96.15% benchmark 得分，与 Tech Leads Club Agent Skills 形成「代码安全验证」的双层闭环

- **[generalaction/emdash](./generalaction-emdash-4565-stars-provider-agnostic-ade-2026.md)** — 4,565 Stars，TypeScript，YC W26，Provider-Agnostic 多 Agent 并行开发环境，支持 27 种 CLI Agent（Claude Code/Codex/Qwen/Gemini 等）+ Git Worktree 隔离 + Linear/Jira/GitHub Issues 直送任务，与 Cursor「第三 era」工厂思维 + Cloud Agent Lessons 形成「多 Agent 并行 → 环境隔离 → 任务驱动」完整闭环

## 已推荐项目（防重索引）

- [yliuAI/Tactile](https://github.com/yliust/Tactile) — 无障碍语义优先的 Agent 操作层，178 Stars，Python，将「截图→坐标→点击」倒转为「语义→坐标→验证」，操作准确率接近 100%，token 消耗降低 60-80%

- [GreyhavenHQ/greywall](https://github.com/GreyhavenHQ/greywall) — 容器无关的内核级 Agent 沙箱，183 Stars，Landlock + Seccomp BPF + eBPF 五层防护，--learning 自动生成最小权限配置，与「多 Agent 并行开发（Git Lock）」形成「安全隔离」的互补

- [Yechan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) — Codex Workflow Layer，28,856 Stars，$deep-interview→$ralplan→$ralph/$team 标准流程 + 多 Agent 并行（tmux）+ .omx/ 状态持久化，与 OpenAI Hooks GA 形成「接口规范 → 具体实现」闭环

- [Storybloq/storybloq](https://github.com/Storybloq/storybloq) — 跨会话上下文持久化，217 Stars，TypeScript，`.story/` 文件约定 + CLI + 43 工具 MCP Server，与 Cursor Composer Autoinstall 形成「环境自动化 vs Session 连续性」的互补
- [manthanguptaa/water](./manthanguptaa-water-production-harness-framework-288-stars-2026.md) — Python Agent Harness 框架，288 Stars，Flow 编排 + Resilience（熔断/限流/检查点）+ Guardrails + EvalSuite + Observability + MCP/A2A 集成，框架无关设计支持 LangChain/CrewAI/Agno，12 模块完整基础设施栈，与 Watwer（上下文管理）形成「编排层 + 上下文层」互补
- [openclaw/clawbench](./openclaw-clawbench-trace-based-agent-benchmark-89-stars-2026.md) — 追踪评分优先的 Agent 评测框架，89 Stars，评分完整技术栈（harness + config + model）而非仅 LLM，13 种失败模式检测 + 47.3% 方差分解为噪声，与 Anthropic April Postmortem 形成「配置变更风险 → 系统性评测」的完整闭环
- [itsuzef/goalkeeper](https://github.com/itsuzef/goalkeeper) — 合约驱动的 Claude Code 目标执行框架，独立 Judge 子代理对抗 Definition of Done

- [NyxFoundation/speca](https://github.com/NyxFoundation/speca) — spec-anchored 安全审计框架，373 Stars，Python，Sherlock Fusaka 恢复全部 15 个漏洞 + 发现 4 个新漏洞（含 1 个人类审计员遗漏的加密不变量违反），arXiv:2604.26495，与 Anthropic Trend 8 形成「认知风险 → 规范层防御方法论」闭环

- [rowboatlabs/rowboat](https://github.com/rowboatlabs/rowboat) — 本地优先的 AI coworker，13,666 Stars，TypeScript，持久知识图谱 + Gmail/Calendar/Notion 深度集成（关联：Cursor Long-Running Agents → 长程 Agent 的上下文积累问题 → 外部化知识图谱的工程实现）

- [neo4j-labs/create-context-graph](https://github.com/neo4j-labs/create-context-graph)

- [2FastLabs/agent-squad](https://github.com/2FastLabs/agent-squad) — 意图分类驱动的多 Agent 编排框架，AWS Labs → 2FastLabs，Classifier-First 动态路由 + SupervisorAgent 并行协调，Python/TypeScript 双语言

- [PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator) — AI Agent 配置文件健康体检工具，17 个评估器诊断 AGENTS.md/CLAUDE.md 质量问题，自动修复 + Before/After 分数对比（关联：Agent 配置过载问题 → 配置文件质量的系统性诊断与修复）

- [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) — 100 行 Python 的极简 Agent，>74% SWE-bench 得分，Princeton & Stanford 团队维护，19K+ Stars，无专用工具接口设计（关联：Anthropic 基础设施噪声研究 → 最干净的可复现评测环境）

- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) — GitHub 最大的 Agent Skills 索引，4,494 ⭐，覆盖 9 个主流 AI Coding 平台

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — AI Coding Agent 的 Production-Grade 工程技能库，DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP 六阶段质量门禁，9 大平台官方推荐
- [virattt/dexter](https://github.com/virattt/dexter) — 面向深度金融研究的 Autonomous Agent，24K ⭐，Multi-Agent 分工 + 沙箱执行 + 全程可溯源

- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) — CLI-Anything: 让所有软件变成 Agent-Native 接口，371 Stars，18+ 应用支持，七阶段自动生成 CLI 包装器，与 Anthropic Opus 4.7 verbosity 控制形成「工具生成 → 行为控制」的 Agent Harness 工程互补
- [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) — 开源 Agent Harness 实现，深度集成 Claude Code / OpenClaw，支持 Ollama 本地运行
- [meta-pytorch/KernelAgent](https://github.com/meta-pytorch/KernelAgent) — Deep Agent + GPU Kernel 自动化优化开源实现，PyTorch → Triton 自动转化
- [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) — AWS Labs 出品的 AI-Driven Development Life Cycle 方法论，1847 Stars，六合一安全扫描，Claude Code/Cursor/Amazon Q 等 8 平台适配
- [agentmemory-persistent-memory-4902-stars-2026](./agentmemory-persistent-memory-4902-stars-2026.md) — 免 DB 的 Agent 持久记忆，4902 Stars，BM25+Vector+Graph 混合检索（RRF fusion），95.2% R@5 + $10/年 + 零 API 成本，与本文配置性降级形成「平台层缓存污染 → 工具层外部记忆」的互补关系
- [coleam00/Archon](https://github.com/coleam00/Archon) — 首个开源 AI 编程工作流引擎，让 AI 编程变得确定可重复
- [obra/superpowers](https://github.com/obra/superpowers) — 用技能框架让 AI 编程从「能写」进化到「会做」
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — AI Agent Harness 的性能优化系统
- [kangarooking/system-prompt-skills](https://github.com/kangarooking/system-prompt-skills) — 15 个可执行的系统提示词设计模式，64 Stars，从 165 个顶级 AI 产品系统提示词中蒸馏，覆盖 persona/tool/safety/memory 等 15 个维度（关联：OpenAI Agents SDK → Skills 已成为标准原语 → system-prompt-skills 提供具体设计模式）

- [strukto-ai/mirage](https://github.com/strukto-ai/mirage) — 统一虚拟文件系统，1,612 Stars，TypeScript，将 S3/Gmail/GitHub/Slack 等后端挂载为文件目录，AI Agent 用 bash 工具操作一切数据源（关联：Codex Agent Loop → 工具抽象层 → 跨后端统一 bash 接口）
- [earendil-works/pi](https://github.com/earendil-works/pi) — 57,415 Stars，TypeScript，零件化 Agent 工具链（unified LLM API + Agent Core + Coding CLI + TUI + Web UI），每个包独立可用不绑定框架，与 pi-mono 重构同名（关联：badlogic/pi-mono → earendil-works/pi 品牌升级），vs LangChain 的「框架 vs 工具箱」哲学对比
- [badlogic/pi-mono](https://github.com/badlogic/pi-mono) — 同 earendil-works/pi 原名，AI Agent 工具链 monorepo，强调开放会话数据共享（Hugging Face）
- [gsd-build/GSD-2](https://github.com/gsd-build/GSD-2) — 生产级自主编码 Harness，7269 ⭐，DB 权威状态 + Auto Pipeline + Milestone/Slice 机制，真正实现"一次命令，几个月不管"（关联：Anthropic 长程 Agent 双组件架构 → 生产级工程实现）
- [Q00/ouroboros](https://github.com/Q00/ouroboros) — Agent OS：规范优先的可验证编码工作流，Specification-first + 3-stage Evaluation Gate，3.2K ⭐

- [RenseiAI/AgentFactory](https://github.com/RenseiAI/agentfactory) — Linear 原生的多 Agent 软件工厂，Dev/QA/Acceptance 三阶段流水线，TypeScript/Redis 生产级架构
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) — OpenAI 官方多 Agent 编排 SDK，Sandbox Agents + Handoffs + Guardrails 生产级基础设施，685+ stars/day
- [LearningCircuit/local-deep-research](https://github.com/LearningCircuit/local-deep-research) — 本地化深度研究 Agent，4,706 ⭐，SQLCipher AES-256 加密 + LangGraph Agent Strategy + SimpleQA ~95%

- [VibePod/vibepod-cli](https://github.com/VibePod/vibepod-cli) — Docker 容器化的 AI 编码 Agent 管理 CLI，零配置 + 本地 Analytics Dashboard，支持 7 个主流 Agent
- [jayminwest/overstory](https://github.com/jayminwest/overstory) — Git Worktree 隔离的多 Agent 编排工具，1.2K ⭐，Session as Orchestrator 设计，SQLite Mail 高效通信

- [ruvnet/ruflo](https://github.com/ruvnet/ruflo) — Claude 原生 Multi-Agent 编排平台，38K ⭐，32 插件生态，自学习 swarm 智能
- [ruflo-claude-swarm-orchestration-2026](./ruflo-claude-swarm-orchestration-2026.md) — Ruflo 推荐，+2,598 stars/day，32 插件 + SONA 自学习 + 零信任联邦（关联：上下文工程 → 多 Agent 记忆协同的工程实现）
- [daytonaio/daytona](https://github.com/daytonaio/daytona) — OCI 原生的 AI Agent 沙箱运行时，Sub-90ms 冷启动 + 可选 Kata/Sysbox 强隔离，OpenAI Agents SDK 8个官方沙箱提供商之一

- [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) — Kubernetes 原生的 Agent 沙箱 CRD
- [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) — Rust 原生浏览器自动化 CLI
- [iammm0/execgo](./iammm0-execgo-agent-action-harness-8-stars-2026.md) — Agent Action Harness，8 Stars，Go 标准库核心 + 可选 contrib，Brain/Hands 解耦的执行内核，HTTP/JSON + gRPC 接口，Kahn DAG 调度 + 三类执行器（os/mcp/cli-skills），与 Anthropic Managed Agents Brain/Hands 解耦形成「理论 → 工程实现」闭环（关联：Anthropic 的 `execute(name,input)→string` 接口 → ExecGo 的 Task DSL + Pluggable Executors 实现）

- [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) — Agent 协作空间，75K ⭐，Agent as the Unit of Work 设计理念
- [omxyz/lumen](https://github.com/omxyz/lumen) — 视觉优先浏览器 Agent，screenshot→action 循环 + 两层上下文压缩，100% WebVoyager 成功率
- [MemTensor/MemOS](https://github.com/MemTensor/MemOS) — LLM 和 AI Agent 的记忆操作系统
- [doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service) — 多框架统一的 Agent 持久记忆后端，REST API + MCP + OAuth + CLI + Dashboard，5ms 检索因果知识图谱，与 Cursor App Stability 形成「本地资源约束 vs 远程记忆解耦」的互补
- [alibaba/page-agent](https://github.com/alibaba/page-agent) — 让任何网页都能被自然语言控制
- [Agent-Field/SWE-AF](https://github.com/Agent-Field/SWE-AF) — 自主工程团队 Runtime，三层控制闭环（Inner/Middle/Outer Loop）+ Git Worktree 隔离并行，Fleet-scale 编排
- [agent-sandbox/agent-sandbox](https://github.com/agent-sandbox/agent-sandbox) — E2B 兼容的企业级 AI Agent 沙箱
- [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) — 把一个 AI 变成游戏开发工作室
- [datawhalechina/easy-vibe](https://github.com/datawhalechina/easy-vibe) — 面向零基础的 vibe coding 学习课程
- [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) — 多模型协同的开源 Agent Harness
- [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) — Claude Code 与 Google NotebookLM 的无缝集成
- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill) — 将人蒸馏为 AI Skill 的工程实践
- [bytedance/deer-flow](https://github.com/bytedance/deer-flow) — 字节跳动开源的多智能体编排框架，Supervisor 模式 + Docker 沙箱 + 持久化记忆
- [numman-ali/openskills](https://github.com/numman-ali/openskills) — Anthropic Agent Skills 的跨平台实现，一个 CLI 让所有 AI 编码工具都能用 Skills
- [mattpocock/skills](./mattpocock-skills-agent-engineering-discipline-74875-stars-2026.md) — 让 AI Coding 从「Vibe」进化到「Engineered」的 Skills 实践集，74,875 Stars，解决对齐偏差/反馈循环断裂/代码entropy加速四大工程失败模式，/grill-me + CONTEXT.md + /tdd + /improve-codebase-architecture 与 Cursor Multi-Agent Kernel 优化形成「能力边界扩展 + 工程纪律强化」的互补（关联：Multi-Agent 探索能力 → 更需要工程纪律防止 chaos → Skills 提供可操作实践框架）
- [mattpocock/sandcastle](https://github.com/mattpocock/sandcastle) — Git Worktree 隔离的 Claude Code 生产编排工具，Docker/Podman/Vercel 三层沙箱 + 分支策略自动化，TypeScript 生产级开源实现（关联：Cursor SDK → 生产级 Agent 基础设施的双轨路径）
- [wilsonzlin/fastrender](https://github.com/wilsonzlin/fastrender) — 百枚并发 Agent 从零构建浏览器引擎，Planner/Sub-Planner/Worker 三层分离架构，100 万行代码验证大规模 Agent Swarm 工程可行性，1.5K ⭐（关联：Anthropic Agent Skills 渐进式披露 → 复杂工作流的知识组织与按需加载）
- [microsoft/skills](https://github.com/microsoft/skills) — 174 个 Agent Skills 的 Microsoft 官方技能库，覆盖 Azure SDK / Foundry / MCP 构建，Context-Driven Development 理念，与 Anthropic Agent Skills 形成企业级 vs 开源的两条路径（关联：Agent Skills 渐进式披露 → 企业级大规模技能管理的实现路径）
- [1jehuang/jcode](https://github.com/1jehuang/jcode) — 下一代编码 Agent Harness，极致轻量化设计（RAM 占用比 Claude Code 低 93%）
- [browserbase/skills](https://github.com/browserbase/skills) — 将 Browserbase 云端浏览器自动化封装为 Claude Code Skill 插件，使编码 Agent 能处理登录受限站点、CAPTCHA 和反爬保护页面
- [provos/ironcurtain](https://github.com/provos/ironcurtain) — 运行时动态风险评估安全运行时，填补静态规则和人工审批之间的空白
- [najeed/ai-agent-eval-harness](https://github.com/najeed/ai-agent-eval-harness) — 开源 MultiAgentOps 评估框架，5000+ 场景库 + Flight Recorder 轨迹回放 + 9层安全审计
- [RightNow-AI/forge-mcp-server](https://github.com/RightNow-AI/forge-mcp-server) — Swarm Agent GPU Kernel 优化 MCP Server，14x 加速 + 100% 数值正确性
- [BytedTsinghua-SIA/CUDA-Agent](https://github.com/BytedTsinghua-SIA/CUDA-Agent) — 首个 RL 训练超越 Claude Opus-4.6 的 GPU Kernel 优化系统，2,026 ⭐
- [withastro/flue](https://github.com/withastro/flue) — Astro 团队开源的 TypeScript Agent Harness 框架，虚拟沙箱 + Markdown Skill 系统
- [aden-hive/hive](https://github.com/aden-hive/hive) — 目标驱动的 Multi-Agent 生产级 Harness，自动生成执行图谱 + 自愈能力
- [robmorgan/metamorph](https://github.com/robmorgan/metamorph) — 并行 Claude Code 容器编排，Git 文件锁分布式任务协调
- [langgenius/dify](https://github.com/langgenius/dify) — 生产级 Agentic Workflow 开发平台，134.7k Stars 全球排名第 49，支持可视化 Workflow/RAG/Agent 多类型编排
- [JackChen-me/open-multi-agent](https://github.com/JackChen-me/open-multi-agent) — 3 依赖的 TypeScript Multi-Agent 引擎，单 `runTeam()` 调用从目标到结果
- [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent) — ~3K 行代码的极简自进化 Agent 框架，技能从任务中结晶而非预装
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — AI Coding Agent 的 Production-Grade 工程技能库，DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP 六阶段质量门禁，9 大平台官方推荐
- [virattt/dexter](https://github.com/virattt/dexter) — 面向深度金融研究的 Autonomous Agent，24K ⭐，Multi-Agent 分工 + 沙箱执行 + 全程可溯源

- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) — GitHub 最大的 Agent Skills 索引，4,494 ⭐，覆盖 9 个主流 AI Coding 平台
- [mem0ai/mem0](https://github.com/mem0ai/mem0) — LLM 和 AI Agent 的通用记忆层，self-improving memory，LoCoMo 91.6 分，ADD-only extraction + Entity linking

- [cocoindex-io/cocoindex](https://github.com/cocoindex-io/cocoindex) — 长程 Agent 增量上下文引擎，代码库变化仅 delta 重嵌入，Rust 生产级实现，8.4k ⭐，Apache 2.0
- [agno-agi/agno](https://github.com/agno-agi/agno) — 将 Agent 转化为生产软件的 Runtime，Session 管理 + OpenTelemetry tracing + RBAC + 多框架兼容
- [memfreeme/memfree](https://github.com/memfreeme/memfree) — 开源混合 AI 搜索引擎，支持知识库 + 互联网搜索 + Chrome 书签同步，一键部署
- [lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent) — 用简单模式构建高效 Agent 的 MCP 框架，Full MCP Support + Temporal Durable Execution + 46%+ Token 节省
- [hidai25/eval-view](https://github.com/hidai25/eval-view) — AI Agent 行为回归测试框架，snapshot behavior → diff tool calls → classify regression，生产级 Silent Regression 检测
- [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) — MCP Server for n8n workflow automation，1,650+ nodes 文档覆盖，Claude Code/VS Code/Cursor 多 IDE 支持
- [TauricResearch/TradingAgents](./tauricresearch-tradingagents-multi-agent-trading-framework-80k-stars-2026.md) — Multi-Agent 金融交易框架，角色分层（分析师/研究员/交易员/风控），真实金融机构运作逻辑的开源实现，80,277 Stars
- [kyegomez/swarms](https://github.com/kyegomez/swarms) — 企业级 Multi-Agent 编排框架，6,620 ⭐，七种预构建编排模式（MCP/x402/Skills 协议兼容）

- [opensearch-project/agent-health](https://github.com/opensearch-project/agent-health) — OpenSearch 官方的 Agent 评估与观测框架，Golden Path Trajectory 对比 + OpenTelemetry Traces + LLM Judge，15 ⭐
- [elct9620/autonoe](https://github.com/elct9620/autonoe) — 基于 Claude Agent SDK 的长程自主编码工具，1.2k ⭐，Anthropic 双 Agent 模式的完整开源实现
- [sunnweiwei/FoldAgent](https://github.com/sunnweiwei/FoldAgent) — Context-Folding 强化学习框架开源实现，AAAI 2026 论文，让 Agent 学会主动上下文管理

- [cloveric/cc-telegram-bridge](https://github.com/cloveric/cc-telegram-bridge) — Claude Code / Codex CLI 的 Telegram bridge，161 ⭐，session resume + 隔离多 Bot 实例 + Agent Bus 编排（关联：OpenAI Agents SDK 沙箱执行 → CLI harness 桥接模式扩展）
- [Apra-Labs/apra-fleet](https://github.com/Apra-Labs/apra-fleet) — MCP 原生多机 Agent 协作框架，Doer-Reviewer 双角色循环，SSH 跨机器编排（35 ⭐，Apache 2.0）

- [TheAgentCompany/TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany) — 在模拟真实软件公司中测试 AI Agent 能力的基准测试框架，175 个真实工作场景，GitLab/Plane/RocketChat 全工具链覆盖，697 ⭐（关联：Anthropic Trend 4 — Agent 学会在不确定性中主动寻求帮助的测试基准）
- [InsForge/InsForge](https://github.com/InsForge/insforge) — AI Coding Agent 的 Backend-as-a-Service 平台，Postgres + Auth + Storage + Model Gateway + Edge Functions，语义层让 Agent 理解「后端在做什么」而非机械生成代码，8.3K ⭐（关联：Anthropic Initializer Agent + Coding Agent 双组件架构 → 后端基础设施的语义化封装）

---

- [89luca89/clampdown](https://github.com/89luca89/clampdown) — 零信任 AI 编码 Agent 沙箱，Landlock + Seccomp + OCI Hook 三层内核级隔离，零密钥泄露架构
- [navam-io/sentinel](https://github.com/navam-io/sentinel) — 视觉优先 Agent 评测平台，React Flow 画布 + YAML 即时生成 + 12 分类断言系统，Postman for AI Agents 定位
- [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) — 专业分工的 AI Agent 团队编排框架，30+ 专才 Agent（Frontend/Backend/SRE/Security 等），人格驱动的 Agent 定义格式标准

## 推荐文章索引

- [Martian-Engineering/Volt](./Martian-Engineering-volt-lossless-context-management-2026.md) — 无损上下文管理，273 Stars，LCM 双态架构（Immutable Store + Active Context）+ 三级升级协议保证收敛，在 OOLONG benchmark 32K-1M tokens 所有长度上超过 Claude Code，与 Anthropic 上下文工程形成「理论框架 → 工程实现」的完整闭环（关联：上下文压缩 → 确定性压缩引擎 → Volt LCM）

- [LiberCoders-FeatureBench-feature-level-agentic-coding-benchmark-2026](./LiberCoders-FeatureBench-feature-level-agentic-coding-benchmark-2026.md) — ICLR 2026 功能级编程 Agent 评测框架，Fast split 57.2 秒/实例，支持 Claude Code/Codex/OpenHands 等 5 个主流 Agent 框架，与 Anthropic AI-Resistant Evaluations 形成「能力边界检测 vs AI 抗性设计」的互补（关联：AI-Resistant Evaluations → 细粒度能力评测趋势 → FeatureBench 功能级评测框架）

- [context-evaluator-packmindhub-ai-agent-config-health-2026](./context-evaluator-packmindhub-ai-agent-config-health-2026.md) — AI Agent 配置文件健康体检工具，17 个评估器诊断 AGENTS.md 质量问题，自动修复 + Before/After 对比（关联：Agent 配置过载 → 配置文件质量的系统性诊断）
- [cursor-cookbook-sdk-examples-2026](./cursor-cookbook-sdk-examples-2026.md) — cursor/cookbook 推荐，3,675 ⭐，5 个生产级 Sample，DAG Task Runner + Cloud Agent 自动化 PR（关联：Cursor Harness 持续改进工程 → SDK 产品化 → 开发者接入生产级 Agent 运行时的代码级入口）

- [openharness-hKUDS-agent-harness-open-source-2026](./openharness-hKUDS-agent-harness-open-source-2026.md) — 香港大学开源 Agent Harness，深度集成 Claude Code / OpenClaw
- [kernelagent-meta-multi-agent-gpu-optimization](./kernelagent-meta-multi-agent-gpu-optimization.md) — Deep Agent + GPU Kernel 自动化优化开源实现
- [archon-open-source-harness-builder](./archon-open-source-harness-builder.md) — 让 AI 编程变得确定可重复的开源工作流引擎
- [superpowers-llm-feature-flags](./superpowers-llm-feature-flags.md) — 用技能框架让 AI 编程从「能写」进化到「会做」
- [everything-claude-code](./everything-claude-code.md) — AI Agent Harness 的性能优化系统
- [pi-mono-langchain-alternative](./pi-mono-langchain-alternative.md) — 轻量级 AI Agent 工具链的另一种选择
- [kubernetes-agent-sandbox](./kubernetes-agent-sandbox.md) — Kubernetes 原生的 Agent 沙箱 CRD
- [vercel-agent-browser](./vercel-agent-browser.md) — Rust 原生浏览器自动化 CLI
- [memos-memory-os](./memos-memory-os.md) — LLM 和 AI Agent 的记忆操作系统
- [alibaba-page-agent](./alibaba-page-agent.md) — 让任何网页都能被自然语言控制
- [agent-sandbox-framework](./agent-sandbox-framework.md) — E2B 兼容的企业级 AI Agent 沙箱
- [claude-code-game-studios](./claude-code-game-studios.md) — 把一个 AI 变成游戏开发工作室
- [easy-vibe-ai-tooling](./easy-vibe-ai-tooling.md) — 面向零基础的 vibe coding 学习课程
- [oh-my-openagent-agent-framework](./oh-my-openagent-agent-framework.md) — 多模型协同的开源 Agent Harness
- [notebooklm-skill-google-ai](./notebooklm-skill-google-ai.md) — Claude Code 与 Google NotebookLM 的无缝集成
- [colleague-skill-ai-agent](./colleague-skill-ai-agent.md) — 将人蒸馏为 AI Skill 的工程实践
- [deer-flow-2-bytedance-super-agent-harness](./deer-flow-2-bytedance-super-agent-harness-2026.md) — 字节跳动开源的多智能体编排框架，Supervisor 模式 + Docker 沙箱 + 持久化记忆
- [claude-context-zilliz-semantic-code-search](./claude-context-zilliz-semantic-code-search-2026.md) — 语义代码搜索 MCP server，让编码 Agent 在 50k+ 行代码库中即时检索相关上下文
- [openskills-universal-skills-loader](./openskills-universal-skills-loader-2026.md) — Anthropic Agent Skills 的跨平台实现
- [mattpocock-skills-engineering-agent-2026](./mattpocock-skills-engineering-agent-2026.md) — 来自真实工程师的 Agent Skills 实践集
- [sandcastle-mattpocock-claude-code-sandbox-orchestration-2026](./sandcastle-mattpocock-claude-code-sandbox-orchestration-2026.md) — Git Worktree 隔离的 Claude Code 生产编排工具，Docker/Podman/Vercel 三层沙箱（关联：Cursor SDK → 生产级 Agent 基础设施的双轨路径）
- [FoundationAgents/MetaGPT](./FoundationAgents-MetaGPT-SOP-multi-agent-2026.md) — SOP 驱动的多 Agent 协作框架，Role-based 软件公司流水线（PM/Architect/PM/Engineer/Reviewer）+ SPO/AOT 论文支撑 + ICLR 2025 Oral（AFlow），与 Anthropic building-c-compiler（Git-based 去中心化同步）形成「显式流水线 vs 去中心化自组织」完整对比闭环（**本文新增**）
- [openai-agents-sdk-multi-agent-framework](./openai-agents-sdk-multi-agent-framework.md) — OpenAI 官方多 Agent 编排框架
- [openfang-rust-agent-operating-system](./openfang-rust-agent-operating-system.md) — Rust 编写的开源 Agent 操作系统
- [memsearch-cross-platform-agent-memory-2026](./memsearch-cross-platform-agent-memory-2026.md) — 跨平台统一的 AI Agent 持久记忆层
- [RightNow-AI/openfang](https://github.com/RightNow-AI/openfang) — Rust 编写的开源 Agent 操作系统，Hands 概念实现真正的自主执行
- [zilliztech/claude-context](https://github.com/zilliztech/claude-context) — 语义代码搜索 MCP server，让编码 Agent 在 50k+ 行代码库中即时检索相关上下文
- [zilliztech/memsearch](./memsearch-cross-platform-agent-memory-2026.md) — 跨平台统一的 AI Agent 持久记忆层，Markdown 即真理、Milvus 影子索引
- [jcode-next-generation-coding-agent-harness](./jcode-next-generation-coding-agent-harness.md) — 极致轻量化的下一代编码 Agent Harness（RAM 比 Claude Code 低 93%）
- [planner-worker-multi-agent-autonomous-coding-architecture-2026](../orchestration/planner-worker-multi-agent-autonomous-coding-architecture-2026.md) — Planner/Worker 架构深度分析（Cursor Scaling Agents + Anthropic C Compiler 双案例实证）
- [hermes-agent-nousresearch-self-improving-agent-2026](./hermes-agent-nousresearch-self-improving-agent-2026.md) — Nous Research 自改进 AI Agent，131.8k ⭐，内置学习闭环 + FTS5 跨 Session 检索 + 多平台部署（关联：Cursor 动态上下文发现 → context 工程的两极：动态拉取 vs 自主积累）

- [sanity-io/agent-context](./sanity-io-agent-context-structured-access-2026.md) — Sanity 官方的 Agent Context 工具库，结构化访问 CMS 内容，MCP 集成 + Skills 系统（关联：Context 工程的下一阶段 → 结构化上下文访问）
- [ruflo-ruvnet-claude-native-multi-agent-orchestration-2026](./ruflo-ruvnet-claude-native-multi-agent-orchestration-2026.md) — Claude 原生 Multi-Agent 编排平台，38K ⭐，32 插件生态，自学习 swarm 智能（关联：Context Engineering 外部化记忆设计）
- [ironcurtain-secure-runtime-autonomous-ai-2026](./ironcurtain-secure-runtime-autonomous-ai-2026.md) — 运行时动态风险评估安全运行时，与 Claude Code Auto Mode 双层防御形成技术对照
- [forge-mcp-server-rightnow-2026](./forge-mcp-server-rightnow-2026.md) — 让 AI 编程 Agent 拥有 GPU Kernel 优化能力的 MCP Server，14x 加速
- [autonoe-elct9620-long-running-agent-orchestrator-2026](./autonoe-elct9620-long-running-agent-orchestrator-2026.md) — 基于 Claude Agent SDK 的长程自主编码工具，1.2k ⭐，Anthropic 双 Agent 模式的完整开源实现
- [multiagenteval-open-source-agent-eval-harness-2026](./multiagenteval-open-source-agent-eval-harness-2026.md) — 填补 Agentic Reliability Gap 的开源评估框架，5000+ 场景 + Zero-Touch Core Architecture
- [flue-astro-agent-harness-framework-2026](./flue-astro-agent-harness-framework-2026.md) — Astro 团队开源的 TypeScript Agent Harness，虚拟沙箱 + Markdown Skill 系统
- [hive-openhive-multi-agent-harness-2026](./hive-openhive-multi-agent-harness-2026.md) — 目标驱动的 Multi-Agent 生产级 Harness，YC 背景 + 自愈图谱演化
- [anysphere-kernel-optimization-results](./anysphere-kernel-optimization-results-2026.md) — Cursor + NVIDIA 235 个 CUDA Kernel 38% 加速的开源验证结果
- [metamorph-multi-agent-file-lock-parallel-2026](../orchestration/metamorph-multi-agent-file-lock-parallel-2026.md) — Git 文件锁分布式协调机制，Anthropic 100K 行 C 编译器的工程验证
- [open-multi-agent-typescript-multi-agent-orchestration-6156-stars-2026](./open-multi-agent-typescript-multi-agent-orchestration-6156-stars-2026.md) — Goal-First 多 Agent 编排框架，Coordinator Agent 自动生成 DAG，从目标到结果单调用，MIT License
- [brain-hands-decoupled-agent-architecture-2026](../orchestration/brain-hands-decoupled-agent-architecture-2026.md) — Anthropic / OpenAI / Cursor 三家 Brain-Hands 解耦架构对比分析
- [getzep/graphiti](https://github.com/getzep/graphiti) — 面向 AI Agent 的时态上下文图谱，25.8k ⭐，实体/关系/事实四组件 + validity window + episode 溯源，MCP Server 接入 Claude/Cursor
- [browserbase-skills-claude-code-cloud-browser-automation-2026](./browserbase-skills-claude-code-cloud-browser-automation-2026.md) — Browserbase Skills 云端浏览器自动化，突破编码 Agent 处理受保护站点的能力瓶颈
- [genericagent-self-evolving-agent-framework-3k-lines-2026](./genericagent-self-evolving-agent-framework-3k-lines-2026.md) — ~3K 行极简自进化 Agent 框架，技能从任务中结晶而非预装，<30K context window
- [evoagentx-self-evolving-multi-agent-workflow-3025-stars-2026](./evoagentx-self-evolving-multi-agent-workflow-3025-stars-2026.md) — 3,025 Stars，多 Agent 工作流自动进化框架，从自然语言目标自动组装 + TextGrad/MIPRO/AFlow/EvoPrompt 四种进化算法优化，在 GAIA 基准上验证，与 GenericAgent 形成「单 Agent 技能自进化 + 多 Agent 工作流自动优化」的互补闭环
- [awesome-agent-skills-agent-skill-index-4494-stars-2026](./awesome-agent-skills-agent-skill-index-4494-stars-2026.md) — GitHub 最大的 Agent Skills 索引，4,494 ⭐，覆盖 9 个主流 AI Coding 平台
- [cursor-multi-agent-cuda-kernel-optimizer-38-percent-2026](../orchestration/cursor-multi-agent-cuda-kernel-optimizer-38-percent-2026.md) — Cursor 多智能体系统 3 周 38% 加速，235 个 CUDA Kernel 优化工程方法论解析（Planner/Worker 架构 + Self-Benchmarking 闭环）
- [cuda-agent-byted-tsinghua-rl-kernel-optimization-2026](./cuda-agent-byted-tsinghua-rl-kernel-optimization-2026.md) — 字节跳动 × 清华 RL 训练 GPU Kernel 优化系统，首个超越 Claude Opus-4.6 的开源实现
- [gastown-multi-agent-workspace-manager-2026](./gastown-multi-agent-workspace-manager-2026.md) — 多 Agent 工作空间编排系统，14,914 ⭐，Git Worktree 隔离 + Beads 账本 + Witness/Deacon 三层监控（关联：Cursor 第三时代多 Agent Fleet 范式）
- [lobehub-agent-collaboration-platform-2026](./lobehub-agent-collaboration-platform-2026.md) — Agent 协作空间平台，75K ⭐，Agent as the Unit of Work + Create/Collaborate/Evolve 三层协作模式（关联：Anthropic 四层组件模型 → 多 Agent 协作场景下的人类控制设计）
- [mem0-universal-memory-layer-agent-2026](./mem0-universal-memory-layer-agent-2026.md) — LLM 和 AI Agent 的通用记忆层，self-improving memory，LoCoMo 91.6 分（关联：Anthropic Context Engineering → Memory Management 实践验证）
- [tradingagents-multi-agent-trading-framework-2026](./tradingagents-multi-agent-trading-framework-2026.md) — Multi-Agent 金融交易框架，角色分层（分析师/研究员/交易员/风控），真实金融机构运作逻辑的开源实现（关联：Anthropic Agent Skills → 多 Agent 专业角色编排）
- [evalview-ai-agent-behavior-regression-gate-2026](./evalview-ai-agent-behavior-regression-gate-2026.md) — AI Agent 行为回归门卫，snapshot behavior → diff tool calls → classify regression，与 Anthropic Long-Running Agent Harness 互补（前者保实现可维护性，后者保行为一致性）
- [nonstop-agent-claude-long-running-harness-2026](./nonstop-agent-claude-long-running-harness-2026.md) — Claude 长时连续工作 harness，feature_list.json + 双 Agent Pattern，Anthropic 官方工程实践的开源实现（关联：Anthropic Initializer + Coding Agent 双组件架构）
- [ouroboros-agent-os-replayable-specification-first-2026](./ouroboros-agent-os-replayable-specification-first-2026.md) — Agent OS：规范优先的可验证编码工作流，Specification-first + 3-stage Evaluation Gate，与 Anthropic Context Engineering 形成互补（前者减少输入端冗余，后者管理过程端容量）
- [daytona-open-source-ai-agent-sandbox-oci-containers-2026](./daytona-open-source-ai-agent-sandbox-oci-containers-2026.md) — OCI 原生的 AI Agent 沙箱运行时，Sub-90ms 冷启动 + 可选 Kata/Sysbox 强隔离（关联：Anthropic April Postmortem → 沙箱隔离是防止跨层缺陷演变为安全事件的最后防线）

- [getzep/graphiti](./getzep-graphiti-temporal-context-graph-2026.md) — 面向 AI Agent 的时态上下文图谱，25.8k ⭐，MCP Server + 多图数据库支持，与 Anthropic Introspection Adapters 形成「外部上下文管理 vs 内部行为审计」的互补
- [local-deep-research-encrypted-agentic-research-2026](./local-deep-research-encrypted-agentic-research-2026.md) — 本地化深度研究 Agent，4,706 ⭐，SQLCipher AES-256 加密 + LangGraph Agent Strategy + SimpleQA ~95%（关联：Cursor Composer Self-Summarization → 信息管理问题的互补视角：压缩 vs 扩展）
- [vibepod-cli-docker-agent-container-2026](./vibepod-cli-docker-agent-container-2026.md) — Docker 容器化的 AI 编码 Agent 管理 CLI，零配置 + 本地 Analytics Dashboard，支持 7 个主流 Agent（关联：OpenAI Agents SDK Native Sandbox → 本地 vs 云端的不同隔离路径）
- [overstory-multi-agent-orchestration-git-worktree-2026](./overstory-multi-agent-orchestration-git-worktree-2026.md) — Git Worktree 隔离的多 Agent 编排工具，让单个 Claude Code Session 变身多 Agent 团队（关联：Cursor 第三代软件开发 → Agent Fleet 架构的第三种路线：本地化隔离 + 实时干预）
- [mcp-agent-lastmile-ai-mcp-framework-2026](./mcp-agent-lastmile-ai-mcp-framework-2026.md) — 用简单模式构建高效 Agent 的 MCP 框架，Full MCP Support + Temporal Durable Execution（关联：动态上下文发现 → Token 效率工程）
- [opensearch-agent-health-opensearch-eval-harness-2026](./opensearch-agent-health-opensearch-eval-harness-2026.md) — OpenSearch 官方的 Agent 评估框架，Golden Path Trajectory 对比 + OpenTelemetry + LLM Judge（关联：Cursor Harness 持续改进 → 测量驱动改进的工程实现）
- [lumen-omxyz-vision-first-browser-agent-context-compression-2026](./lumen-omxyz-vision-first-browser-agent-context-compression-2026.md) — 视觉优先浏览器 Agent，screenshot→action 循环 + 两层上下文压缩（80% threshold），与 Cursor Self-Summarization 形成训练侧×工程侧的互补（关联：Context Engineering → 注意力预算管理与压缩触发机制工程实现）
- [swarms-kyegomez-enterprise-multi-agent-orchestration-2026](./swarms-kyegomez-enterprise-multi-agent-orchestration-2026.md) — 企业级 Multi-Agent 编排框架，6,620 ⭐，七种预构建编排模式（MCP/x402/Skills 协议兼容）（关联：Anthropic Multi-Agent 四种协调范式 + Swarms 工程实现）
- [wshobson-agents-claude-code-plugins-34800-stars-2026](./wshobson-agents-claude-code-plugins-34800-stars-2026.md) — Claude Code 最大插件市场，34,800 ⭐，185 个专项 Agent + 80 个解耦插件 + 渐进式披露架构（关联：Anthropic Initializer+Coding Agent 双组件模式 → 插件市场级多 Agent 协作解决方案）
- [cc-telegram-bridge-claude-code-telegram-harness-2026](./cc-telegram-bridge-claude-code-telegram-harness-2026.md) — Claude Code / Codex CLI 的 Telegram bridge，161 ⭐，session resume + 隔离多 Bot 实例 + Agent Bus 编排（关联：OpenAI Agents SDK 沙箱执行 → CLI harness 桥接模式扩展）
- [apra-fleet-apra-labs-mcp-multi-agent-coordination-2026](./apra-fleet-apra-labs-mcp-multi-agent-coordination-2026.md) — MCP 原生多机 Agent 协作框架，Doer-Reviewer 双角色循环，SSH 跨机器编排（关联：Cursor 第三时代工厂思维 → 多机 Agent 协作的开源实现路径）

- [claude-agent-teams-ui-777genius-multi-agent-kanban-2026](./claude-agent-teams-ui-777genius-multi-agent-kanban-2026.md) — 多 Agent 团队编排桌面应用，855 ⭐，Kanban 看板 + Hunk 级 Review + 零配置启动，Electron 桌面端读取本地 Claude/Codex Session（关联：Cursor 3 统一多 Agent 工作空间 → 开源生态的等效实现）
- [foldagent-context-folding-reinforcement-learning-2026](./foldagent-context-folding-reinforcement-learning-2026.md) — Context-Folding 强化学习框架开源实现，AAAI 2026 论文，让 Agent 学会主动上下文管理（关联：Anthropic「注意力预算」+ Cursor「Self-Summarization」→ Learned Context Compression 方向实证）
- [swe-af-autonomous-engineering-factory-agentfield-2026](./swe-af-autonomous-engineering-factory-agentfield-2026.md) — 自主工程团队 Runtime，三层控制闭环（Inner/Middle/Outer Loop）+ Git Worktree 隔离并行，Fleet-scale 编排（关联：Cursor 第三时代「工厂思维」→ 自主工程工厂的开源实现）

- [cocoindex-incremental-context-for-long-horizon-agents-2026](./cocoindex-incremental-context-for-long-horizon-agents-2026.md) — 长程 Agent 增量上下文引擎，代码库变化 delta-only 重嵌入，Rust 生产级实现，8.4k ⭐（关联：OpenAI Codex Agent Loop 上下文膨胀问题 → 增量引擎从数据源侧解决新鲜度）
- [memory-benchmarks-eval-suite-2026](./memory-benchmarks-eval-suite-2026.md) — Mem0 开源的 Agent 内存系统评估套件，LoCoMo / LongMemEval / BEAM 三个基准，3000+ 评测题，Cloud + OSS 双模式（关联：Anthropic AI-Resistant Evaluations → 可量化基准测试是持续改进的前提）

- [deepseek-tui-terminal-native-coding-agent-2026](./deepseek-tui-terminal-native-coding-agent-2026.md) — Terminal 原生 AI 编码 Agent，DeepSeek V4 + 1M context + Auto mode，+1,274 stars trending（关联：OpenAI 企业 AI 战略 → Codex vs DeepSeek-TUI 的终端工具双轨竞争）
- [agency-agents-msitarzewski-multi-agent-professional-team-2026](./agency-agents-msitarzewski-multi-agent-professional-team-2026.md) — 专业分工的 AI Agent 团队编排框架，30+ 专才 Agent 人格驱动定义（关联：Anthropic 三代理 GAN 启发架构 → Planner-Generator-Evaluator vs. Agency-Agents 静态专才分工的两种协作范式）
- [context-mode-mksglu-98-percent-context-reduction-2026](./context-mode-mksglu-98-percent-context-reduction-2026.md) — MCP 上下文管理框架，98% Token 压缩 + SQLite FTS5 BM25 检索 + 14 平台覆盖（Microsoft/Google/NVIDIA/Cursor 等），Anthropic Context Engineering 原则的完整工程实现（关联：Anthropic「上下文压缩」+「注意力预算」框架 → 98% 压缩率的工业级验证）

- [agent-infra-sandbox-all-in-one-agent-sandbox-2026](./agent-infra-sandbox-all-in-one-agent-sandbox-2026.md) — All-in-One Agent 沙箱框架，Browser+Shell+File+VSCode+Jupyter+MCP 同容器统一文件系统，2.3k ⭐（关联：Cursor Automations → 本地化执行环境替代方案，与 Cursor Self-Hosted 形成完整闭环）

- [future-agi/future-agi](https://github.com/future-agi/future-agi) — 开源端到端 Agent 评估与优化平台，Simulate→Evaluate→Protect→Monitor→Optimize 单闭环，Go 网关 ~29k req/s，836 ⭐

- [agent-infra/sandbox](https://github.com/agent-infra/sandbox) — All-in-One Agent 沙箱框架，Browser+Shell+File+VSCode+Jupyter+MCP 同容器统一文件系统，2.3k ⭐

- [Hmbown/DeepSeek-TUI](https://github.com/Hmbown/DeepSeek-TUI) — Terminal 原生 AI 编码 Agent，DeepSeek V4 + 1M context + Auto mode 自动选择模型思考级别，+1,274 stars trending（关联：OpenAI Codex → 终端原生 AI 工具的双轨竞争格局）

- [skyflo-ai/skyflo](https://github.com/skyflo-ai/skyflo) — Kubernetes 原生的 Self-Hosted AI Agent，Approval-Gated + 确定性控制循环，TypeScript，108 ⭐

- [777genius/claude_agent_teams_ui](https://github.com/777genius/claude_agent_teams_ui) — 多 Agent 团队编排桌面应用，Kanban 看板 + Hunk 级 Review，855 ⭐，Electron + React + TypeScript

- [darkrishabh/agent-skills-eval](./darkrishabh-agent-skills-eval-empirical-skill-testing-459-stars-2026.md) — Skill 实证评测框架，459 Stars，TypeScript + MIT，带 Skill vs 不带 Skill 对比评测 + Judge 模型评分，与 OpenAI Parameter Golf 形成「AI 时代实证验证」的双视角闭环

- [joeseesun/qiaomu-anything-to-notebooklm](./joeseesun-qiaomu-anything-to-notebooklm-claude-skill-multi-source-content-to-notebooklm-2730-stars-2026.md) — Claude Skill 多源内容转换器，2,730 Stars，6 层级联付费墙绕过（Googlebot→Bingbot→AMP→archive.today→Google Cache→本地工具）+ 300+ 站点支持 + NotebookLM 播客/PPT/思维导图/Quiz 全格式生成，与 Cursor 多-repo 云端开发环境形成「内容获取 → 格式生成 → 企业知识管理」的互补

- [LocoreMind/locoagent](./LocoreMind-locoagent-cdp-native-browser-agent-2026.md) — CDP 原生浏览器 Agent 框架，136 ⭐（本文新增），直接走 Chrome DevTools Protocol 而非 Playwright 封装层，Agent 获得完整浏览器控制能力（DOM 查询/网络请求监控/JavaScript 上下文）+ 精确观测精度，与「Browser Agent 架构最终收敛到 CDP 层」的判断形成互证

- [awslabs/agent-plugins](./awslabs-agent-plugins-aws-agent-toolkit-successor-715-stars-2026.md) — AWS Agent 插件集合，715 Stars，Agent Plugins 标准容器（Skills+MCP Servers+Hooks+References）+ Agent Toolkit for AWS 后继者，与 Cursor multi-repo 环境形成「工具层编排 → 环境层隔离」的企业 Agent 基础设施双轨

- [beenuar/AiSOC](./beenuar-AiSOC-open-source-security-operations-center-investigation-ledger-791-stars-2026.md) — 开源 AI SOC 平台，791 Stars，MIT 许可，LangGraph ~600行可审计的 Agent 编排器，Investigation Ledger 记录每步推理 + 可回放，公开 CI-gated eval harness 覆盖 55 种攻击模板 + 14 种日志源，≥50:1 告警-事件比率（CI 验证），与 Anthropic April Postmortem 形成「复合效应追踪 → 可审计决策 Ledger」互补

- [trycua/cua](./trycua-cua-open-source-computer-use-agents-sandbox-benchmarks-9574-stars-2026.md) — 计算机使用 Agent 全栈开源基础设施，9,574 ⭐，统一 API 跨平台沙箱（Linux/macOS/Windows/Android）+ CUA Driver 后台操作 + CUA Bench 基准测试 + cuabot 零配置 Agent 沙箱，与 Cursor 云端开发环境形成「环境配置 → 安全执行」完整闭环

- [first-fluke/oh-my-agent](./first-fluke-oh-my-agent-portable-multi-agent-harness-944-stars-2026.md) — 跨 IDE 便携式多 Agent 编排框架，944 ⭐，.agents/ SSOT + 双层模型分发（Claude/Codex/Gemini/Qwen 各角色独立选型）+ 11 种语言 auto-detection，覆盖 frontend/backend/architecture/QA/PM 等 23 个角色，与 OpenAI Codex Windows 沙箱文章形成「隔离 → 编排」的互补（关联：沙箱解决「如何让单个 Agent 安全访问文件/网络」→ oh-my-agent 解决「如何让多个 Agent 各司其职、互不越界」）

- [NirDiamant/agents-towards-production](./nirdiamant-agents-towards-production-19797-stars-2026.md) — 19,797 ⭐，28 个生产级 GenAI Agent 教程（stateful workflows、vector memory、Docker、GPU scaling、multi-agent、observability、evaluation），LangChain/Redis/Tavily/Arcade 等头部工具官方 sponsor 验证，与 Anthropic April 23 Postmortem 形成「Harness 治理 → 生产落地」的完整闭环

- [GoogleCloudPlatform/agent-starter-pack](./googlecloudplatform-agent-starter-pack-production-agent-deployment-6345-stars-2026.md) — 6,345 ⭐，GCP 原生 Agent 部署完整生命周期模板（Terraform + CI/CD + Vertex Eval + OpenTelemetry），Cursor 云端 Agent 教训的完整生产级答案，「开发环境即产品 → 基础设施即模板」方法论闭环（**本文新增**）

- [ComposioHQ/agent-orchestrator](./composiohq-agent-orchestrator-parallel-coding-agent-fleet-7099-stars-2026.md) — 7,099 ⭐，并行 Agent 编排框架

- [vchain/mini-swe-agent：100行代码的极致简约设计（2026）](vchain-mini-swe-agent-100-lines-2026.md) — 74% SWE-bench，Princeton/Stanford团队出品

- [HKUDS/nanobot：OpenClaw精神继承者，42.7k Stars的极简个人AI Agent（2026）](hkuds-nanobot-ultra-lightweight-personal-agent-2026.md) — 多channel、MCP、Memory，与mini-swe-agent形成「极简Agent双路径」对比

- **[mikeyobrien/ralph-orchestrator](./mikeyobrien-ralph-orchestrator-rust-ai-agent-orchestration-3000-stars-2026.md)** — 3,000+ Stars，Rust，多后端 Agent 编排框架（Claude Code / Codex / OpenCode / Gemini CLI / Copilot CLI 等），Hat System 专业角色协调 + Backpressure 门控（测试/lint/typecheck 不通过则拒绝）+ RObot 人在环路（Telegram 实时介入），与 OpenAI Symphony（Linear 任务板控制）和 Edict（三省六部制度）形成「任务控制层」三足鼎立：状态机看板 vs 制度性审核 vs 角色帽系统

- **[strukto-ai/mirage](./strukto-ai-mirage-unified-vfs-2599-stars-2026.md)** — 统一虚拟文件系统，2,599 Stars，让 AI Agent 用熟悉的 bash 工具（cat/grep/cp）操作 S3/Slack/GitHub/Gmail/MongoDB 等后端服务。核心价值：当 MCP 工具数量膨胀到数十个时，「万物皆文件」的抽象不是优化，是生存问题。与 Anthropic Code Execution with MCP（98.7% token 节省）形成「接口语义抽象 → 编程原语抽象」的 Agent 工程化双轨

- **[millionco/react-doctor](./millionco-react-doctor-agent-code-review-10659-stars-2026.md)** — 10,659 Stars，AI Agent 的 React 代码质量检测 Skill，自动 catch 运行时错误、最佳实践违反、TypeScript 类型问题、性能反模式。作为 Claude Code/Cursor/Copilot 等 30+ 平台的 skill 运行，在代码提交前完成检测，而非等用户发现。与 Cursor Keep Rate 指标形成「过程检测 vs 结果追踪」的互补（**本文新增**）

- **[tddworks/baguette](./tddworks-baguette-ios-simulator-farm-1007-stars-2026.md)** — Headless iOS 26 模拟器农场，1,007 Stars，SimulatorKit 原生 + 60fps 数据流 + 多指手势注入，支持 AI Agent 在 CI 无头环境中验证 iOS 应用行为。与 Cursor 3 多 Agent 并行和 Agent Skills 技能系统形成「执行环境 → 技能验证」的完整闭环


- **[agentic-in/elephant-agent](./agentic-in-elephant-agent-personal-model-self-evolving-469-stars-2026.md)** — Personal-Model-First 自改进 AI Agent，469 Stars，2026-05-15 创建，四个记忆 Lens（Identity/World/Pulse/Journey）替代完整上下文窗口，CLI-first 设计，Python≥3.12，与 Cursor Cloud Agent Lessons（环境配置质量决定输出）形成「记忆框架 → 上下文质量」的完整 Agent 工程双轨闭环

- [akitaonrails/ai-memory](./akitaonrails-ai-memory-cross-agent-handoff-321-stars-2026.md) — 跨厂商 Agent 交接方案，321 Stars，Rust，将每次 Session 的遗留工作压缩为 Markdown 维基，下个 Agent（无论哪家）自动 prepend 交接文档，与 Cursor No-Repo Automations 互补（关联：运营 Agent 长程可靠性 → 需要跨 session 的上下文连续性 → ai-memory 的 SessionBoundary 触发机制）

- **[lobehub/lobehub](./lobehub-lobehub-chief-agent-operator-78008-stars-2026.md)** — 78,008 ⭐，首席 Agent 运营官平台，7×24 小时 Agent 团队管理模式（雇佣/排班/汇报）+ 自托管支持 + 插件生态。与 mission-control（控制台观测层）和 oh-my-claudecode（协作执行层）形成「管-看-干」三权分立：LobeHub 管人（生命周期管理）、mission-control 看状态（32 面板 eval 监控）、oh-my-claudecode 干活（多 Agent 协作），**本文新增**

- **[OpenBMB/PilotDeck](./OpenBMB-PilotDeck-task-oriented-agent-platform-2545-stars-2026.md)** — 2,545 Stars，任务导向 Agent 生产力平台，WorkSpace 概念实现跨会话上下文持久化演进 + MCP Native 原生协议支持 + AGPL 3.0 开源。与 Cursor /loop（事件驱动循环控制）形成互补：/loop 管「何时唤醒」，PilotDeck 管「上下文如何累积」，两篇文章同轮产出，互相印证。

- **[open-gitagent/gitagent](./open-gitagent-gitagent-git-native-agent-framework-504-stars-2026.md)** — 504 Stars，TypeScript/Node.js，通用 Git-Native Agent 框架（"Agents as Repos"范式）+ Agent = Git 仓库（SOUL.md/RULES.md/Memory/Tools 全部版本化）+ GAP 开放标准（框架无关）+ 一键安装 + 支持 Claude/OpenAI/CrewAI/LangChain，与 Claude Code Security-Guidance Plugin（内生安全审查）形成「工具层安全 → Agent 定义层版本化」的工程层次互补（Round 222）

- **[he-yufeng/CoreCoder](./he-yufeng-corecoder-nanogpt-of-coding-agents-617-stars-2026.md)** — 617 Stars，Python，MIT，Coding agents 领域的 nanoGPT（512K 行 TypeScript → 1,400 行 Python）+ 7 个核心架构模式（搜索替换编辑/并行工具执行/3层上下文压缩/子Agent隔离上下文/危险命令阻止/会话持久化/动态System Prompt）+ 任意 LLM 兼容（Kimi/Claude/GPT/DeepSeek/Qwen/Ollama）+ 与 Managed Agents（Platform 层）形成「架构层 → 实现层」完整闭环，**本文新增**

- **[YeQing17-2026/OmniAgent](./yeqing17-2026-omniagent-self-evolving-security-1726-stars-2026.md)** — 1,726 Stars，Python，全维度自展元代理框架（OmniEvolve：Skill/Context/BrainModel 三维同步进化）+ 动态安全强化（Safety hardens dynamically）+ 多端支持（飞书/Discord/Telegram）+灵感源自 OpenClaw。与 [CrewAI + NemoClaw 自展元代理文章](../orchestration/crewai-nemoclaw-self-evolving-agents-enterprise-trust-2026.md) 形成「外部约束（Flow+沙箱）↔ 内在共生（动态安全强化）」的互补闭环，**本文新增**

- **[refactoringhq/tolaria](./refactoringhq-tolaria-local-markdown-knowledge-base-ai-agent-13374-stars-2026.md)** — 13,374 Stars，TypeScript/Rust，桌面 Markdown 知识库（YAML frontmatter + Git 版本控制 + 本地 CLI Agent 集成），「文件即知识库」设计让 Claude Code/Codex 可直接 grep/操作笔记，与 Cursor Composer 2 环境忠诚度理念（训练=生产等价）形成「知识管理 → 训练环境」的主题闭环（Round 302，**本文新增**）

- **[Panniantong/Agent-Reach](./panniantong-agent-reach-cli-internet-access-26811-stars-2026.md)** — 26,811 Stars，MIT，CLI 工具让 AI Agent 直接访问 Twitter/Reddit/YouTube/GitHub/Bilibili/小红书等 16 个平台，零 API 费用。基于成熟 CLI 工具的编排层（Selector + Installer + Health Checker + Router），与 Cursor SDK 自然语言权限配置（auto-review classifier）形成「Agent 能力扩展 → 安全约束」的主题闭环，**本文新增**

- **[rpamis/comet](./rpamis-comet-phase-guarded-agent-skill-harness-1245-stars-2026.md)** — 1,245 Stars，MIT，Agent Skill 的阶段门控自动化框架（Phase Guard + 5 相流水线），将 OpenSpec（需求管理）和 Superpowers（执行规划）串联成 5 相自动化流水线：Idea → Spec → Plan → Build → Verify → Archive。`.comet.yaml` 状态机作为 Checkpoint File，Agent 中断后通过 `wake(sessionId)` + `getSession(id)` 精确恢复。与 R337 Checkpoint/Resume 协议（harness cluster anchor）形成主题闭环，**本文新增**


- **[bradAGI/awesome-cli-coding-agents](./bradAGI-awesome-cli-coding-agents-563-stars-2026.md)** — 563 Stars，MIT，80+ CLI Coding Agent 生态全景图（2026-06-08），分为 Terminal-native Coding Agents（Claw Code/Hermes Agent/OpenCode/Gemini CLI/Codex CLI 等）+ Harnesses & Orchestration（Session managers/Orchestrators/Agent infrastructure）两大类。与 OpenAI Server-side Compaction 文章（Compaction vs Truncation 长程 Context 管理）形成「机制层 → 工具层」的主题闭环：Compaction 解决长程 Agent 的 Context 续命问题，awesome-cli-coding-agents 提供了这些机制的实际应用场景索引（Session managers & parallel runners 处理长程 Agent 状态续接），**本文新增**

- **[framerslab/agentos](./framerslab-agentos-cognitive-memory-574-stars-2026.md)** — 574 ⭐，TypeScript，2026-06-05 新发布，认知记忆 AI Agent 框架（8 种神经科学-backed 机制：Ebbinghaus 遗忘/检索诱导遗忘/再巩固/来源置信度衰减）+ Runtime Tool Forging（Agent 自写工具 + LLM Judge 审核 + node:vm sandbox 执行）+ HEXACO 个性系统 + Soul Files 身份容器 + 6 种编排策略。与 Anthropic AI Organizations Article（../orchestration/anthropic-ai-organizations-alignment-risks-2026.md）形成「风险揭示（论文）↔ 工程实现参考（框架）」完整闭环，**本文新增**

- **[ckkissane/petri-realism-win-rate](./ckkissane-petiri-realism-win-rate-open-science-2026.md)** — 0 Stars，Python，Anthropic Fellows 开源研究工具链（Realism Win Rate 量化审计真实感）+ 四阶段工程流程（Deployment Data 采集 → Petri Audit 运行 → Realism Win Rate 评估 → 多维度 grading）+ pairwise LLM judge 机制避免绝对评分的校准问题 + 支持用自己的 Claude Code 数据本地运行。与 [Realism Win Rate 文章](../harness/anthropic-coding-audit-realism-win-rate-petrio-auditor-2026.md) 形成「论文研究 ↔ 开源复现工具」的完整闭环，**本文新增**

- **[DeusData/codebase-memory-mcp](./deusdata-codebase-memory-mcp-7300-stars-2026.md)** — 7,300+ Stars，MIT，代码知识图谱 MCP Server（Tree-Sitter AST + SQLite 图谱）+ 158 语言支持 + 99% 更少 token（3400 vs 412000）+ 毫秒级查询 + 团队共享图谱 Artifact + Multi-Agent 支持（11 种 Coding Agent）+ Hybrid LSP（10 语言语义类型解析）。与[创业公司 AI Agent 战略文章](../enterprise/claude-ai-agents-startups-resource-constrained-2026.md)形成主题闭环：文章分析「如何在资源约束下用 AI 扛起整家公司」→ 本项目提供「让 AI Agent 持久理解代码库」的工程基础，两者共同指向「让小团队干大公司活」的核心命题，**R448 新增**


- **[microsoft/agent-governance-toolkit](./microsoft-agent-governance-toolkit-autonomous-agent-security-4407-stars-2026.md)** — 4,407 Stars，MIT，AI Agent运行时安全治理框架，Policy as Code + 零信任身份 + 三层安全架构（Policy/Identity/Runtime），v3.7.0生产级迭代。与 [Anthropic Project Fetch Phase Two（Physical Agentic AI）](../deep-dives/anthropic-project-fetch-phase-two-embodied-agentic-ai-2026.md)形成主题闭环：Opus 4.7展示物理世界自主Agent能力（37x speedup），本项目提供对应的安全治理框架，一个解决「能不能」的问题，一个解决「该不该」的问题，**R452新增**

- **[vercel/eve](./vercel-eve-filesystem-first-durable-agent-framework-1651-stars-2026.md)** — 1,651 Stars，Apache-2.0，Vercel 出品的「文件系统优先」Durable Agent 框架。核心：每个 Agent 即一个约定目录结构，`instructions.md` 定义系统提示词（Markdown！），`tools/` 放置函数，`skills/` 放置技能流。文件系统即状态，git diff 即 review，目录结构即 Agent 能力边界。与 [R459 Builder.io less-ai（第三执行面）](../fundamentals/builderio-ai-restraint-third-execution-surface-architecture-2026.md)形成主题闭环：第三执行面说「确定性工作应从 Agent 结晶到 Actions」，eve 说「文件系统结构本身即 Agent 边界」，两者共同指向「可枚举的 Agent 才是可工程化的 Agent」，**R459新增**
