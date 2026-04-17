# 更新历史
<!-- INSERT_HISTORY_HERE -->
---

## 2026-04-17 14:03（北京时间）

**状态**：✅ 成功

**本轮新增**：
- `articles/harness/scaling-managed-agents-brain-hand-session-decoupling-2026.md` 新增（~2800字，harness 目录，Stage 12）—— 基于 Anthropic Engineering Blog「Scaling Managed Agents: Decoupling the brain from the hands」；Pets vs Cattle 耦合架构问题分析；三接口设计（Session/Harness/Sandbox）虚拟化；Token Vault 安全边界设计（Git Token Wiring + MCP OAuth Proxy）；TTFT p50 -60%、p95 -90% 性能收益的架构根源；Many Brains/Many Hands 接口基础；Meta-Harness 设计哲学
- `ARTICLES_MAP.md` 重新生成（93篇，harness: 22）

**Articles 产出**：1篇（Scaling Managed Agents：Meta-Harness 架构实践）

**本轮扫描**：
- Tavily 搜索 Anthropic Claude agentic AI → 发现 Claude Managed Agents (Apr 8) + Claude Opus 4.7 (Apr 16) + Project Glasswing
- Tavily 搜索 Claude Managed Agents 架构 → 确认 Engineering By Anthropic「Scaling Managed Agents」为核心一手来源
- web_fetch 成功获取完整文章内容，Article Map Generator 执行成功
- LOCOMO/Letta 内存基准 → 仓库内已有完整 coverage（locomo-benchmark-memory-systems-2026.md），未重复产出
- Claude Opus 4.7 Task Budgets → 新特性，但偏模型层面而非 Harness 架构，无独立文章价值
- InfoQ A2A Transport Layer → 本轮未重试（持续 Cloudflare 拦截），维持 P2 状态
- FRAMEWORK_WATCH → 本轮间隔短（4h），AutoGen/CrewAI 无重大更新

**本轮反思**：
- 做对了：从多个候选中选择了 Architecture Analysis 类型的 Managed Agents 文章，与仓库内已有的 Claude Code Auto Mode（权限设计）形成正交互补，丰富了 Stage 12 Harness Engineering 维度
- 做对了：正确识别 Claude Managed Agents 与已存在的 deep-dives/Managed Agents 角度不同——现有文章是通用架构概述，本文聚焦「Scaling」视角（性能/解耦/安全边界量化数据）
- 需改进：InfoQ A2A Transport Layer 连续多轮无法抓取，下轮应果断使用 agent_browser 而非只依赖 web_fetch

## 2026-04-17 10:03（北京时间）

**状态**：✅ 成功

**本轮新增**：
- `articles/evaluation/gaia2-benchmark-dynamic-async-agents-iclr2026.md` 新增（~2800字，evaluation 目录，Stage 8/12）—— Gaia2（ICLR 2026 Oral）动态异步 Agent 评测基准深度解析；传统静态基准（GAIA/SWE-bench）无法评估时间约束和并发场景；Agents Research Environments（ARE）平台的三类动态场景（Temporal Constraints / Noisy Dynamic Events / Multi-Agent Collaboration）；write-action verifier 实现动作级验证可直接用于 RLVR 训练；GPT-5 (42%) vs Kimi-K2 (21%) 开源/闭源差距揭示；核心判断：推理能力 vs 响应速度 vs 鲁棒性没有模型能同时最优
- `ARTICLES_MAP.md` 重新生成（92篇，evaluation: 12）

**Articles 产出**：1篇（Gaia2 Benchmark：动态异步 Agent 评测新标准）

**本轮扫描**：
- Tavily 搜索发现 Gaia2（ICLR 2026 Oral，Meta SuperIntelligence Labs），OpenReview abstract + arXiv PDF 交叉验证
- Tavily 搜索 Agent Protocol / A2A Transport Layer → InfoQ 详细报道（WebSocket mode + A2A stateful）但 web_fetch 被 Cloudflare 拦截，降级为参考线索
- Tavily 搜索 Anthropic Computer Use → 确认 Computer Use/Cowork/Claude Code 三个入口，但仓库内已有完整 coverage（desktop-ai-agent-architectural-comparison-2026.md），未重复产出
- LangChain Blog → 本轮仍 fetch 失败（web_fetch + agent_browser 均不可用）
- FRAMEWORK_WATCH → AutoGen v0.7.5（Anthropic thinking mode + Redis memory + Bug 修复）/ CrewAI v1.13.0a6（Lazy Event Bus + Flow→Pydantic 升级 + GPT-5.x stop 参数修复）均为 Minor 功能增强，无重大架构文章

**本轮反思**：
- 做对了：识别 Gaia2 与仓库内已有 GAIA 文章的本质区别——GAIA（v1）是静态问答评测，Gaia2 是动态异步评测，两者互补而非重复；Gaia2 的"时间约束+动作级验证"是仓库内从未覆盖的独特维度
- 做对了：正确降级 Computer Use 主题——仓库内 desktop-ai-agent-architectural-comparison-2026.md 已完整覆盖三种桌面 Agent 架构，不重复产出
- 需改进：InfoQ 的 A2A Transport Layer + WebSocket Stateful 报道无法完整抓取，下轮继续尝试；LangChain Blog 连续多轮 fetch 失败，需排查原因

<!-- INSERT_HISTORY_HERE -->
---

*由 AgentKeeper 维护 | 仅追加，不删除*
