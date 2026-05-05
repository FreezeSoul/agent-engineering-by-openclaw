# OpenSearch Agent Health：让 AI Agent 的质量第一次「可见」

## TRIP 四要素

**T - Target（谁该关注）**
有 Python 经验的 Agent 开发者和平台工程师——无论你正在构建 AI 编码助手、RCA 自动化 Agent 还是客服系统，只要你的 Agent 需要在生产环境运行并被多人使用，这篇文章就是为你写的。

**R - Result（能带来什么）**
原本「看不见」的 Agent 行为质量，现在变成了一张张可量化的仪表盘：**Trajectory 对比、Error Rate 趋势、Cost 追踪、Latency 直方图**——一个 CLI 命令就能启动完整观测系统。对于平台团队，这意味着不再需要手动翻日志来定位「为什么这个 Agent 最近的错误率突然上升」。

**I - Insight（凭什么做到）**
用 OpenSearch 作为存储后盾 + OpenTelemetry Trace 作为数据源 + LLM Judge 作为评估层——这三者的组合解决了 Agent 观测的三个核心问题：**数据去哪了（OpenSearch）**、**执行过程怎么追踪（OTEL）**、**质量谁来打分（LLM Judge）**。

**P - Proof（有谁在用）**
OpenSearch 项目本身是 Apache 2.0 社区驱动的开源项目，拥有广泛的的企业采用基础；GitHub 上 15 Stars，虽然绝对数不高，但考虑到它是 OpenSearch 官方项目栈的一部分，后续增长潜力明确。

---

## P-SET 骨架

### P - Positioning（定位破题）

**一句话定义**：OpenSearch Agent Health 是一个**生产级 Agent 评估与观测框架**，用「Golden Path Trajectory 对比」来衡量 Agent 质量。

**场景锚定**：什么时候你会想起它？

> 当你需要回答「这个 Agent 最近质量是变好了还是变坏了」这个问题时——不是靠感觉，而是靠数据。

**差异化标签**：LLM Judge + OpenTelemetry + OpenSearch 的三合一观测栈

---

### S - Sensation（体验式介绍）

**从用户视角走一遍**：

1. **安装**：一行 `npx @opensearch-project/agent-health` 直接启动，带演示数据
2. **连接你的 Agent**：写一个 `agent-health.config.ts`，配置 Endpoint + Connector Type（REST/AG-UI SSE/Claude Code/Subprocess）
3. **观察**：打开 Dashboard，看到「实时 Streaming Evals」「批量 Experiments」「Side-by-side Compare」
4. **深入**：点击任意 Trace，看到 Timeline 和 Flow 可视化——不是日志文本，而是**执行时间线**

**哇时刻**：当你点击「Compare」，看到两个版本 Agent 的 Trajectory 并排对比时——绿色的 Pass/Fail 直接告诉你「这次升级到底改进了什么」。

---

### E - Evidence（拆解验证）

**技术深度**：

**架构分层**（三层）：

| 层 | 技术 | 作用 |
|----|------|------|
| 数据采集 | OpenTelemetry (OTLP) | 捕获 Agent 的每一个 Tool Call 和 LLM 响应 |
| 数据存储 | OpenSearch | 保存 Trace、Test Cases、Evaluation Results |
| 质量评估 | LLM Judge（基于 Bedrock） | 将 Agent 行为与 Golden Path 对比打分 |

**Connector 生态**：支持 7 种协议（REST、AG-UI SSE、OpenAI Compatible、Strands、LangGraph、Subprocess、Claude Code）——覆盖了当前主流的 Agent 框架。

**Coding Agent Analytics**：特别针对 Claude Code、Kiro、Codex CLI 的专属功能——自动发现本地安装的 Agent、读取 `~/.claude/` 等本地数据、零配置启动多 Agent 监控。

**社区健康度**：OpenSearch 官方项目，拥有完整的 CI/CD（GitHub Actions）和贡献流程（DCO 要求）——相比小众项目，企业级维护更有保障。

---

### T - Threshold（行动引导）

**快速上手（3 步）**：

```bash
# 方式一：零配置体验（带演示数据）
npx @opensearch-project/agent-health

# 方式二：连接你的 Agent（需 Docker）
git clone https://github.com/opensearch-project/agent-health.git
cd agent-health && docker compose up -d
cp .env.docker .env
npx @opensearch-project/agent-health
```

**配置你的第一个 Agent**：

```typescript
// agent-health.config.ts
export default {
  agents: [{
    key: "my-agent",
    name: "My Agent",
    endpoint: "http://localhost:8000/agent",
    connectorType: "rest",
    models: ["claude-sonnet-4"],
    useTraces: true
  }]
};
```

**贡献入口**：OpenSearch Slack（#opensearch-agent-health）、GitHub Issues/PR——适合对 Agent 评估有实践经验的贡献者。

**路线图**：当前 v1.0，重点在「Single Agent Eval」+「Multi-Agent Dashboard」。未来方向可能延伸至 Multi-Agent Orchestration 的性能对比（与 OpenSearch Agent Server 项目联动）。

---

## 与 Articles 的关联性

本文「Cursor Agent Harness 工程实践：持续改进的方法论」揭示了**测量驱动改进**的核心框架——Keep Rate、LLM Satisfaction、Tool Error Classification。

OpenSearch Agent Health 正是这个框架的**工程实现**：当你不知道「Agent 质量变好了还是变坏了」时，Golden Path Trajectory Comparison 提供了一个客观答案；当你需要追踪「Error Rate 趋势」时，OpenSearch 的时序数据能力提供了持久化存储。

**技术关联**：两者共同指向一个结论——**Harness 工程的下一步，是把「测量」变成基础设施，而不是靠人工观察日志**。

---

## 自检清单

- [x] T: 目标用户画像清晰（Agent 开发者 / 平台工程师）
- [x] R: 核心成果有量化（Error Rate 趋势、Keep Rate 追踪、Latency 直方图）
- [x] I: 技术亮点解释了「LLM Judge + OTEL + OpenSearch 的组合为什么合理」
- [x] P: 有 OpenSearch 官方背书 + GitHub Stars 数据

- [x] P: 前 100 字让人知道「给谁看、解决什么」
- [x] S: 有「哇时刻」——Golden Path Compare 并排对比
- [x] E: 解释了「它为什么能做到」（三层架构）
- [x] T: 有明确的下一步行动建议（npx 启动）

- [x] 至少 2 处 README 原文引用
- [x] 如果把项目名换成同类竞品，文章还成立吗？不成立——抓准了 OpenSearch 栈的差异化
- [x] 无硬伤性错误（Stars 数字已通过 GitHub API 验证：15）

---

**引用来源**：

> "Agent Health is an evaluation and observability framework for AI agents, built on OpenSearch. It helps you measure agent performance through 'Golden Path' trajectory comparison — where an LLM judge evaluates agent actions against expected outcomes — and provides deep observability into agent execution via OpenTelemetry traces."
> — [GitHub README: opensearch-project/agent-health](https://github.com/opensearch-project/agent-health)

> "Agent call errors can be extremely harmful to a session in Cursor. While the agent can often self-correct, errors remain in context, wasting tokens and causing 'context rot,' where accumulated mistakes degrade the quality of the model's subsequent decisions."
> — [Cursor Blog: Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)

> "A unified dashboard for monitoring AI coding agent usage across Claude Code, Kiro, and Codex CLI. Zero configuration — just run agent-health and it auto-detects installed agents. All data stays local — reads directly from ~/.claude/, ~/.kiro/, ~/.codex/"
> — [GitHub README: opensearch-project/agent-health - Coding Agent Analytics](https://github.com/opensearch-project/agent-health/blob/main/docs/CODING_AGENT_ANALYTICS.md)
