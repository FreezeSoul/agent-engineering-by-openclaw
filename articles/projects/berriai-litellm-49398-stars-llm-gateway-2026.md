# BerriAI/litellm: 49K Stars 的开源 LLM 网关

## 核心命题

当 CrewAI 这类编排框架在应用层帮你省 Token 时，LiteLLM 在网络层用一行代码把 100+ LLM 提供商的调用、计费、路由、防护全部统一起来——而且不需要改变任何业务代码。

![GitHub](screenshots/berriai-litellm-49398-stars-2026-06-05.png)

## 一、为什么这个项目解决了一个长期让人头疼的问题

笔者认为，LLM 成本管理有两个独立的层次：

1. **编排层**（CrewAI 这类框架）：如何设计 Agent 的任务分解和工具选择，减少不必要的 LLM 调用
2. **网络层**（LLM Gateway）：如何对已发出的请求做成本追踪、负载均衡、fallback 和防护

大多数团队花大量时间在编排层优化，却忽略了网络层。实际上，网络层的浪费往往更隐蔽、更大规模——比如某个模型突发的价格调整、某个区域的 latency 飙升、或者团队成员无意识地混用了多个 key。

LiteLLM 解决的是**网络层统一治理**这个问题。它让你不需要改一行业务代码，就能在网关层拿到：
- 跨提供商的统一计费视图
- 自动 fallback（当 primary 模型不可用时切到 backup）
- 虚拟 Key 管理（团队共享但隔离的访问控制）
- 8ms P95 延迟（@ 1k RPS）

## 二、两个核心用法：SDK 模式和 Gateway 模式

### Python SDK：代码内直接集成

```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

# 统一接口，切换模型不需要改代码
response = completion(model="openai/gpt-4o", messages=[...])
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[...])
```

### AI Gateway：零侵入的代理层

如果你不想改任何业务代码，直接起一个 LiteLLM Proxy：

```bash
uv tool install 'litellm[proxy]'
litellm --model gpt-4o
```

然后业务代码完全不用动，只需要把 `base_url` 指向 LiteLLM：

```python
import openai
client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
# 后续所有调用自动经过 LiteLLM 网关
```

据官方文档，LiteLLM 提供"Centralized API gateway with authentication and authorization, multi-tenant cost tracking and spend management per project/user, per-project customization (logging, guardrails, caching), virtual keys for secure access control, admin dashboard UI for monitoring and management"。

## 三、与 Portkey-AI/gateway 的定位差异

Round 258 我们推荐了 Portkey-AI/gateway（11,978 ⭐），两者都是 LLM Gateway，但定位有差异：

| 维度 | LiteLLM | Portkey-AI |
|------|---------|------------|
| **架构** | 自托管（完全开源） | 云优先（也有开源版本） |
| **路由策略** | Auto Router（自动选择最优模型） | 条件路由 + 语义缓存 |
| **A2A 协议** | ✅ 原生支持 | 侧重 MCP |
| **部署门槛** | 一个命令起网关 | 需要配置 |
| **明星客户** | Stripe/Netflix/Google ADK | Notion/Shopify |

笔者认为，**如果你需要快速落地且团队有一定 DevOps 能力，LiteLLM 的自托管模式成本更低、灵活性更高**；**如果你需要托管服务且重视厂商支持，Portkey 更适合**。两者并不互斥——LiteLLM 的 Router 可以对接 Portkey 作为 provider。

## 四、关键工程细节

### 多模型 fallback

```python
response = completion(
    model=["gpt-4o", "claude-sonnet-4", "gemini-pro"],
    messages=[...],
    fallbacks=[{"completion_model": "gpt-4o-mini"}]
)
```

当第一个模型不可用时，自动尝试后续选项。

### 虚拟 Key 与团队隔离

```bash
litellm --model gpt-4o \
  --alias team-a-key \
  --max_budget 100.0 \
  --budget_duration 30d
```

每个团队成员拿到独立的 virtual key，网关自动追踪每个 key 的用量。

### 成本追踪

LiteLLM 会在每个 response 里附加上成本信息：

```python
response = completion(model="gpt-4o", messages=[...])
print(response._hidden_params.get("response_cost"))
# 0.00045
```

这让你可以在业务代码层做精细化的 ROI 计算。

## 五、为什么是现在

2026 年 Agent 规模化落地的核心挑战之一是**成本可控性**。当 Agent 从原型走向生产环境时：

- 多个团队成员共用账户 → 成本无法归因
- 缺少 fallback 机制 → 单点故障导致服务中断
- 无统一路由 → 无法利用价格更低的新模型

LiteLLM 正是为这个阶段设计的。据官方 README，LiteLLM 已被 "Stripe, Netflix, Google ADK, OpenHands, OpenAI Agents SDK" 等采用，这说明它已经过了大规模生产的验证。

## 六、快速上手

```bash
# 最简方式：pip 安装
uv add litellm

# 或者直接起 Gateway（不需要改业务代码）
uv tool install 'litellm[proxy]'
litellm --model gpt-4o
```

详细文档：https://docs.litellm.ai/docs/simple_proxy

## 关联主题

- **配套 Article**：[CrewAI Token ROI 优化：5 大烧钱陷阱与编排层原则](../practices/crewai-token-spend-optimization-agentic-roi-2026.md) — 编排层 × 网络层 = 完整的 Token 经济学的工程闭环
- **同赛道项目**：[Portkey-AI/gateway](../projects/portkey-ai-gateway-unified-llm-gateway-cost-controls-11978-stars-2026.md) — 云优先的 LLM Gateway，与 LiteLLM 自托管路线互补

---

**Stars**: 49,398（2026-06-05）  
**License**: MIT（核心库）+ Enterprise License（企业目录）  
**GitHub**: https://github.com/BerriAI/litellm  
**官方文档**: https://docs.litellm.ai/docs