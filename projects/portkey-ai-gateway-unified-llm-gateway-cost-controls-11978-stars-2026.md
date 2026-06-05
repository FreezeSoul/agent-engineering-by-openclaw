# Portkey-AI/gateway：路由 250+ LLM 的统一 AI 网关，把 CrewAI 文章里的五大 mitigation 变成开箱即用的能力

**推荐理由**：`Portkey-AI/gateway`（11,978 ⭐，MIT）是 GitHub 上最成熟的开源 LLM 网关，把 CrewAI 《How to Optimize Token Spend for Better Agentic ROI》（June 2, 2026）里列出的五大 token 失控因素（推理模型隐藏消耗 / Agent 循环累积 / RAG 输入体积 / 模型过度配置 / 60-80% 无业务价值支出）逐条转化为网关层能力——**简单 + 语义缓存、跨 provider 路由、模型降级 fallback、负载均衡、Guardrails、Usage analytics、Provider optimization 自动选 cheapest**。当 CrewAI 在企业编排层讲「Control plane for token ROI」时，Portkey 已经在网络层把这些能力打成一行 Docker 命令，**这是同一工程目标在两层的并行实现**——文章讲「应该控制什么」，项目讲「在网关这一层具体怎么控制」。

**关联 Article**：`articles/practices/crewai-token-spend-optimization-agentic-roi-2026.md`（CrewAI Token 经济学：企业 Agent 投入产出的 5 大烧钱陷阱与 70-85% 成本下降路径）

---

## 基本信息

| 指标 | 数值 |
|------|------|
| GitHub | `Portkey-AI/gateway` |
| Stars | 11,978 |
| Fork | 813 |
| 语言 | TypeScript（Node.js ≥ 18） |
| 主题 | `ai-gateway`, `llm-routing`, `semantic-cache`, `observability`, `fallback`, `load-balancing`, `guardrails` |
| License | MIT |
| Created | 2023-08-23 |
| Last push | 2026-06-05（活跃维护中） |
| Open Issues | 40+（PR 节奏密集）|
| 包名 | `npx @portkey-ai/gateway` / `pip install portkey-ai` / Docker 镜像 |

## 核心能力（与 CrewAI 五力模型一一对位）

CrewAI 文章把 token 失控归因到五个**循环结构**问题：推理模型隐藏消耗、Agent 循环累积、RAG 输入体积、模型过度配置、实验性支出。Portkey 没有解决**循环结构**问题——那是 Agent 框架层的事——但它把**每一次 API 调用**可能浪费的部分从网络层挡住：

| CrewAI 列出的问题 | Portkey 的对应能力 | 配置示例 |
|------------------|-------------------|----------|
| **Agent 循环累积**：10 步 × 30K context = 500K-2M tokens | `load balancing` + `conditional routing` + `fallback`：把每个 step 路由到合适的 provider，循环放大不导致成本爆炸 | `{"strategy": {"mode": "loadbalance"}}` |
| **RAG 输入体积**：50K-200K input tokens / call | `simple cache` + `semantic cache`：把相同/语义相似的请求**直接短路**到缓存，不调用 LLM | `"cache": {"mode": "semantic", "max_age": 60}` |
| **模型过度配置**：60-80% 跑在不该用的强模型 | `provider optimization`（automatic cheapest model selection）：同一份 prompt 自动选 cost-optimal provider | `{"strategy": {"mode": "provider-optimization"}}` |
| **多 provider 复杂度**：5 个 provider × 5 个 SDK = 25 个集成 | **统一 OpenAI 兼容 API**：250+ 模型，1 个 `base_url`，1 个 API key | `base_url: https://api.portkey.ai/v1` |
| **不可观测性**：没有 visibility 就无法优化 | `usage analytics`：每次调用的 cost / latency / error rate 入仓，自带 dashboard | `{"metadata": {"user_id": "..."}}` |
| **失控风险**：单次 $40 账单 | `guardrails` 50+ 预置：PII detection、prompt injection detection、output validation、token-per-request cap | `{"guardrails": ["prompt-injection-detect"]}` |
| **多模态**：文本/图像/音频不同 API 表面 | `multi-modal capabilities`：统一 schema 跨模态调用 | 同 API |

**笔者认为**：Portkey 的核心价值不是「单点能力最强」（缓存不如 GPTCache 专精，路由不如 custom router 灵活），而是**它把整条 mitigation 流水线压缩成一个 OpenAI 兼容的 endpoint**。这意味着任何现存 OpenAI/Anthropic SDK 代码**改一行 base_url 就能接入**，迁移成本几乎为零——这是文章里讲「orchestration-layer controls」时最稀缺的「**改造成本可忽略的工程选项**」。

## 与 CrewAI 五大烧钱陷阱的「文章主张 × Portkey 体现」对位表

| 文章主张（CrewAI 6/2） | Portkey 实现位置 | 备注 |
|------------------------|-----------------|------|
| 设置 hard caps on iterations / max_tokens 防止 $40 失控 | `guardrails` + `metadata: {request_timeout, max_tokens}` | 网关层硬限，不依赖 Agent 框架合作 |
| Per-task model routing（Haiku for extraction, Opus for orchestration） | `conditional routing` + `load balance` 按 metadata 字段分发 | 多模型协同的网关层实现 |
| Role and tool scoping（每个 agent 只看到需要的 tool） | `virtual keys` + per-team RBAC | 组织级权限，而不仅是单 agent |
| Hierarchical vs sequential 架构选择可省 60% context | **不在网关层解决**——这是编排层问题 | 闭环边界 |
| Deterministic steps outside LLM（parsing/validation 不用 LLM）| `guardrails` 内置 Pydantic-style 校验 | 部分覆盖，复杂 logic 仍需 custom tool |
| Output structure enforcement（Pydantic schema）| `output_pydantic` 同名能力 + `guardrails` | 重复验证 |
| Prompt caching（stable prefixes + 1-hour TTL）| **网关不重写 prompt 结构**——但 `simple cache` 可减少重复调用 | 互补而非替代 |
| Batch APIs（非实时任务走 batch）| **非 Portkey 范围**——是 provider 端能力 | Portkey 转发 batch endpoint |
| Semantic caching at app layer | `semantic cache` mode（内建）| 直接对位 |
| Self-hosting open-weight models | `Together / Fireworks / Groq` provider preset | 接入路径标准化 |
| Observability（Galileo, Arize, Datadog LLM Observability） | `usage analytics` + `logs` endpoint + 第三方 OTel 导出 | 自主 + 开放 |

**关键判断**：Portkey 与 CrewAI 不构成竞争关系——Portkey 在网络/网关层，CrewAI 在编排/Agent 框架层。**两者叠加的工程效果是**：

```
Application (CrewAI agents) → Portkey gateway (cache / routing / guardrails) → 250+ LLM providers
```

这与文章「Orchestration-layer + Platform-layer 双层控制」的工程蓝图**完全吻合**——CrewAI 是 orchestration-layer 的范式，Portkey 是 platform-layer 的事实标准。

## 与已有仓库内容的关联

- **`articles/practices/crewai-token-spend-optimization-agentic-roi-2026.md`**——本文是它的**执行层配套**：文章讲为什么 + 怎么设计 Portkey 讲「在网络层立即可用的能力」。两文一起读，读者获得「**问题定义 + 现成方案**」的完整闭环。
- **`articles/practices/ai-coding/openai-shell-skills-compaction-long-running-agents-2026.md`**（如有）——长运行 Agent 的 context 压缩是 orchestration-layer 解决方案；本文网关层解决方案是不同的问题切入点。
- **`projects/composiohq-composio-tool-management-28k-stars-2026.md`**——Composio 解决「tool 层治理」，Portkey 解决「model 层治理」，两者构成企业 Agent 平台的双底座（tool gateway × model gateway）。
- **`projects/composiohq-trustclaw-self-hosted-personal-ai-agent-715-stars.md`**——自托管栈趋势的呼应：Portkey 同样支持自托管，与 TrustClaw 的本地优先哲学形成路径共鸣。

## 适用场景与边界

**适合引入 Portkey 的场景**：
- 已有 ≥ 2 个 LLM provider 接入，面临**多 SDK 维护成本**
- Production workload 中**重复/近重复请求占比 ≥ 10%**（典型客服、知识库、code review）
- **单次调用成本**敏感（如 RAG pipeline 高频调用）
- 需要**组织级 usage analytics**（按 team / user / project 拆分 cost）
- 想用 guardrails 做 **prompt injection / PII 检测**而不愿自己实现

**不适合 Portkey 的场景**：
- 单 provider + 单 agent 的小规模 PoC（直接用 OpenAI SDK 更简单）
- 需要**模型训练/微调**（Portkey 是 inference gateway，不涉及训练）
- **长上下文内部消化**场景（>1M tokens，Portkey 的 cache 收益边际递减）

## 快速试用

```bash
# 1. 自托管（10 秒启动）
docker run -d -p 8787:8787 portkeyai/gateway:latest

# 2. 改一行 base_url，所有 OpenAI SDK 代码立即生效
# 之前
# openai.api_base = "https://api.openai.com/v1"
# 之后
openai.api_base = "http://localhost:8787/v1"
openai.api_key  = "PORTKEY_PROVIDER_KEY"  # 虚拟 key，可限速/限预算
```

```python
# 3. 启用 semantic cache（30% 命中率典型场景）
from portkey_ai import Portkey
client = Portkey(
    api_key="PORTKEY_VIRTUAL_KEY",
    config={
        "cache": {"mode": "semantic", "max_age": 3600},
        "retry": {"attempts": 3, "on_status_codes": [429, 500]},
        "strategy": {"mode": "loadbalance", "targets": [
            {"provider": "openai", "weight": 0.5},
            {"provider": "anthropic", "weight": 0.5}
        ]}
    }
)
```

## 一句话总结

> **CrewAI 文章是「Token ROI 优化」的工程宣言，Portkey-AI/gateway 是这份宣言在网络层的即用实现——前者讲问题与原则，后者讲「一行配置就能用」**。把 11,978 ⭐ 的成熟网关与一手的 CrewAI 数据点（70-85% 成本下降空间）放在一起读，读者得到的是「**问题定义 + 立即可落地的能力清单**」的完整闭环。

---

**来源**：

- GitHub: <https://github.com/Portkey-AI/gateway>
- 官方文档: <https://portkey.wiki/gh-1>
- Series A 公告（2.0 路线图）: <https://portkey.wiki/rohit-a>
- 关联 Article: `articles/practices/crewai-token-spend-optimization-agentic-roi-2026.md`（CrewAI, June 2, 2026, Mike Boyarski）

**评分**：4.5/5（实用性 5 / 成熟度 5 / 时效性 4 / 与已有内容互补度 5 / 工程机制完整度 4）

**为什么不是 5/5**：作为 gateway，**语义缓存的语义匹配准确度**仍受限于 embedding 选型；超大上下文（>1M tokens）场景下缓存收益边际递减；guardrails 50+ 预置规则覆盖 80% 常见场景，但**深度定制的合规规则仍需自己写 plugin**。
