# LangChain Model Neutrality 宣言：AI 时代的 Vendor Lock-In 正在从模型层转移到 Harness 层

> **核心论点**：AI 的 Vendor Lock-In 不是模型本身（商品化已不可逆），而是各家实验室正在用 Harness（Agent SDK / Agents API / Agent Builder）重新锁住你。LangChain 以 HashiCorp / Terraform 的云中立化历史为类比，论证了「Model Neutrality 比 Cloud Neutrality 更重要」——因为这次锁定发生在 harness 层、且 Agent 内部需要在单次执行中切换模型。云时代的 Terraform 是经验模板，模型时代需要一个开源、Profile-aware 的 Neutral Harness。LangChain / Deep Agents 是这个角色的候选。

> 原文：https://www.langchain.com/blog/model-neutrality
> 作者：Neil Dahlke（LangChain 联合创始人，HashiCorp 前员工）| 2026-06-04

## 标签

- `vendor-lock-in` / `model-neutrality` / `cloud-neutrality` / `terraform-paradigm`
- `harness-engineering` / `agent-sdk` / `multi-model` / `open-weight-models`

## 来源

- 原始博客：https://www.langchain.com/blog/model-neutrality
- 作者背景：HashiCorp 前员工，亲历云中立化历史
- 评分：5/5（实用性 / 独特性 / 时效性）

---

## 一、问题的本质：云时代锁住了存储，这次锁住了 Harness

Neil 在文章开篇给出了一个非常清醒的判断：**AI 的 Lock-In 不会停留在模型层。**

> *"The labs are selling you tokens. Tokens are a commodity, and increasingly so... So their next move is to capture you at the harness, and you can watch them all making it at once. Claude Agent SDK, OpenAI's Agents API, Vertex AI Agent Builder. All the same shape."*

这是从 HashiCorp 走出来的工程师最擅长的视角——**当年云厂商卖的是存储/网络/算力（commodity），真正的护城河是 CloudFormation / ARM / Vertex（tooling-layer lock-in）。** 现在模型层正在快速商品化，OpenAI / Anthropic / Google 把战火烧到了 harness 层。

文章的隐含逻辑链是：
1. 模型层差异化在快速抹平（前沿模型排行榜每季度换位，open-weight 持续追赶）
2. 价格曲线 24 个月持续下行
3. 模型厂商一定会上移锁定到上游（harness）—— **因为他们没有商业动机让自己 harness 平等支持竞品模型**
4. 一旦业务逻辑落在 harness 上，离开成本 = 重写所有 agent 编排

## 二、为什么 Model Neutrality 比 Cloud Neutrality 更重要

Neil 给出三个差异点，**每一个都让这次锁定的成本更高**：

### 2.1 切换节奏从「年度」变成「月度」

云迁移的节奏是合同续约或事故应对，几年一次。**模型的排行榜轮换是季度甚至月度**——Anthropic 写码最强但 OpenAI 多模态领先，每次轮换都意味着当前选型可能错过下一次跃迁。

### 2.2 模型不是全维度 commodity，而是「选择性商品化」

> *"Anthropic is currently the model to reach for on coding, though OpenAI is closing the gap, and OpenAI is ahead on multimodal. The rankings shift every few months."*

通用推理、Q&A、总结在 commodity 化，但 coding、multimodal、tool-calling、长 context 仍有显著差异。**生产 agent 的真实答案往往是「同一个 workflow 用多个模型」**——coding step 走 Claude、image step 走 GPT、廉价 step 走 DeepSeek。**这只能在不偏袒任何一方的 harness 上实现。**

### 2.3 切换颗粒度从「合同级」降到「请求级」

云中立是合同层概念（cloud neutrality stops at the contract）。**Agent 中立是请求层概念（agent neutrality has to follow the request）**——

> *"choosing Claude for a coding step and GPT for an image step, failing over mid-execution when one provider rate-limits, dropping to a cheaper model where the expensive one isn't justified."*

这是云时代没有的工程复杂度：**harness 必须支持 sub-second 的多模型路由、动态降级、profile-aware 行为**。闭源 vendor harness 没有动机做这件事。

## 三、Open-Weight 改变了「自托管」的可信度

文章还点出了一个云时代不存在的杠杆：**open-weight 模型让自托管变得可信**。

> *"Llama, Mistral, DeepSeek, Qwen. Self-hosting is credible in a way that 'running your own private cloud' never really was for most enterprises."*

这意味着模型中立不仅是防御性的（不被锁），也是进攻性的（**混部闭源 + 开源模型，按 task 路由到 cheapest/fastest/most-accurate**）。一个真正的 neutral harness 必须 first-class 支持：
- 闭源 API（Claude / GPT / Gemini）
- Open-weight 自托管（Llama / Mistral / DeepSeek / Qwen）
- 防火墙后的私有模型

## 四、Neutral Harness 的三要素

Neil 给出的判定标准是**三层叠加**，缺一不可：

| 要素 | 含义 | 闭源 vendor harness 的失败模式 |
|------|------|------------------------------|
| **Open Source** | 可读每一行代码 | 闭源 framework 即使 API 通用也无法验证 vendor 中立 |
| **Multi-model out of the box** | 同一 harness、任何后端 first-class | vendor harness 对竞品模型的 tool-calling 优化必然滞后 |
| **Profile-aware** | 不假装模型可互换，而是暴露每个模型的 prompt / tool-calling 偏好 | lowest-common-denominator 会让所有模型都表现平庸 |

**关键洞察**：「Profile-aware」与「multi-model」不是冲突的，而是**正交的**。一个好的 neutral harness 让 Claude 用 Claude 的最佳 prompt 模式、GPT 用 GPT 的最佳 tool-calling 风格——同时不让任何一家成为抽象的所有者。

## 五、与云中立化的对位：Terraform 经验

文章最后给出一个明确的类比：

> *"Terraform's whole reason to exist was that this tooling-layer lock-in was real, expensive, and getting worse, and that the right answer was a neutral abstraction one layer up: the right to switch, and the ability to mix providers in a single deployment without rewriting your infrastructure."*

**Terraform 之所以赢，是因为它把自己定位为「云厂商之上的一层」，而不是另一个云厂商。** LangChain / Deep Agents 的定位完全平行：把自己定位为「模型厂商之上的一层」，不与任何一家模型厂商竞争 token 收入。

这是**结构性中立**——不是营销话术，而是商业模式的必然结果。一个 token 销售方不可能做 neutral harness；一个不卖 token 的 harness 方才有动机做。

## 六、对工程团队的实操含义

读完这篇文章，工程团队应该问自己三个问题：

1. **你的 agent 业务逻辑落在哪一层？** 若是 vendor harness（Claude Agent SDK / OpenAI Agents API / Vertex Agent Builder），你的迁移成本正在指数级累积。
2. **你的 agent 是否能在一个 run 内切换模型？** 如果不能，你就被锁在了当前模型的能力上限 + 价格曲线。
3. **你是否有 profile 抽象？** 还是把 prompt 写死在了某个 vendor 的最佳实践里？

一个 12-18 个月前的判断「选 Claude SDK 是因为它最强」可能在 6 个月后变成「锁在了一个不再最优的模型上」——而迁移成本已经从「重写 prompt」变成「重写所有 orchestration 逻辑」。

## 一句话总结

**AI 的 Lock-In 不在 token 层（已 commodity 化），而在 harness 层（正在被快速重兵布防）；Cloud 时代 Terraform 是答案，Agent 时代需要一个开源、Profile-aware、Multi-model 的 Neutral Harness——LangChain / Deep Agents 是这个角色的候选，但不是唯一候选。**

---

*本文属于「Harness Engineering」系列，分析 Agent 上层 orchestration 抽象如何决定业务可迁移性。*
