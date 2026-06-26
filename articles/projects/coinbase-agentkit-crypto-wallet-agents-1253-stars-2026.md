# Coinbase AgentKit：让每个 AI Agent 都有一个加密钱包

> 本文推荐 Coinbase 开源的 AgentKit——一个让 AI Agent 持有和操作加密货币钱包的工具包。1,253 Stars，MIT License，框架无关设计。

## 核心命题

AI Agent 最大的瓶颈，不是推理能力，而是**与现实世界交互的能力**。Coinbase AgentKit 给出的答案是：从加密货币钱包开始，让 Agent 学会"拥有资产"。

## 一、为什么这个项目值得关注

大多数 AI Agent 工具包解决的是"Agent 内部"的问题——如何更好地规划、如何更好地调用工具、如何更好地记忆。但 Coinbase AgentKit 解决的是一个更根本的问题：**Agent 如何与外部金融系统交互**？

这个方向的战略意义在于：加密货币是第一个**原生数字资产**，它可以被程序化地持有、转移和管理，没有任何摩擦——不需要银行账户、不需要 KYC 流程、不需要人工审批。Coinbase AgentKit 把这个能力赋予了 AI Agent。

笔者判断，这个项目的价值不在于"加密货币"本身，而在于它证明了 **AI Agent 可以原生拥有和操作资产**——这个能力可以扩展到任何数字资产（积分、NFT、SBT、tokenized securities）。

## 二、核心能力：3 行代码让 Agent 拥有钱包

从 README 来看，AgentKit 的设计哲学是**极简上手**：

```python
# Python 快速开始
pipx run create-onchain-agent
cd onchain-agent && mv .env.local .env
poetry install && poetry run python chatbot.py
```

```typescript
// Node.js 快速开始
npm create onchain-agent@latest
cd onchain-agent && mv .env.local .env
npm install && npm run dev
```

这个设计非常聪明——**用脚手架工具（scaffolding）降低认知门槛**，而不是让开发者从零配置 Wallet Provider 和 Action Providers。

### 支持的链和协议

从文档来看，AgentKit 支持：
- **Base**（Coinbase 自己的 L2）
- **Ethereum** 及 EVM 兼容链
- 50+ 链上 Actions（transfer、swap、mint、bridge 等）

支持的 Wallet Provider：
- CDP（CdpProvider）
- Privy（PrivyProvider）
- Viem（ViemProvider）

这意味着 Agent 可以支持多链、多钱包架构，而不仅仅是"一个 Agent 一个钱包"的简单模式。

## 三、框架无关设计：融入而非锁定

笔者认为，AgentKit 最聪明的工程决策是**框架无关（framework-agnostic）**：

> "It is designed to be framework-agnostic, so you can use it with any AI framework, and wallet-agnostic, so you can use any wallet."

这个设计的工程价值在于：
1. **不绑定特定 Agent 框架**：可以用在 LangGraph、CrewAI、OpenAI Agents SDK 任何一方
2. **不绑定特定钱包方案**：企业可以用自己的 Custody 方案，个人开发者可以用 CDP
3. **Action Provider 可扩展**：开发者可以用 `generate-action-provider` 脚本创建自定义链上 Actions

这与 OpenAI AgentKit 形成有趣的对照：OpenAI AgentKit 解决**工作流编排**问题，Coinbase AgentKit 解决**资产操作**问题——两者是正交的，可以叠加使用。

## 四、工程架构：monorepo 的双语言设计

AgentKit 采用 **monorepo 双语言（Python + TypeScript）** 结构：

```
agentkit/
├── typescript/
│   ├── agentkit/
│   │   ├── action-providers/   # 50+ 链上 Actions
│   │   └── wallet-providers/   # cdp / privy / viem
│   └── scripts/generate-action-provider/
└── python/
    └── (同上结构)
```

这个架构的工程价值：
- **TypeScript**：适合前端/全栈开发者接入 Next.js 应用
- **Python**：适合后端/数据团队接入 FastAPI 或 LangGraph

双语言支持意味着 AgentKit 可以作为**全栈 Agent 应用的基础设施层**，而不只是一个 Python 库。

## 五、与 OpenAI AgentKit 的互补关系

这里有一个值得注意的生态关系：

| 维度 | OpenAI AgentKit | Coinbase AgentKit |
|------|----------------|------------------|
| **解决的问题** | 工作流编排 + 可视化 | 链上资产操作 |
| **核心抽象** | Agent Builder / Connector Registry | Action Provider / Wallet Provider |
| **使用门槛** | 企业级（Global Admin Console）| 开发者级（pipx 3行上手）|
| **可组合性** | 可集成 Coinbase AgentKit | 可被 OpenAI AgentKit 调用 |

笔者判断，这两者的组合是 **OpenAI 官方生态认可的方向**：OpenAI 在博客中明确提到了 AgentKit 作为"building blocks"战略，而 Coinbase AgentKit 恰好填补了"资产操作"这个 building block。

## 六、局限性与适用场景

**不适用**：
- 需要传统银行系统集成的场景（SWIFT、ACH）
- 对监管合规有复杂要求的金融场景
- 非加密货币的数字资产（目前主要支持 token）

**适用**：
- DeFi 原生应用开发
- Web3 Agent 应用
- 原生数字资产的 Agent 化管理
- 跨链桥接和 swap 自动化

## 七、实测建议

```bash
# 快速体验（Python）
pipx run create-onchain-agent
cd onchain-agent
# 填写 .env（CDP API Key + OpenAI API Key）
mv .env.local .env
poetry install
poetry run python chatbot.py

# 然后对 Agent 说：
# "Fund my wallet with some testnet ETH."
```

从 README 来看，Agent 会自动调用 `faucet` action，从 Base Sepolia 水龙头获取测试网 ETH——**零成本体验完整链路**。

---

**引用来源**：
- [coinbase/agentkit | GitHub](https://github.com/coinbase/agentkit)
- [CDP API Keys | Coinbase Developer Platform](https://docs.cdp.coinbase.com/get-started/docs/cdp-api-keys)
- [AgentKit Documentation | Coinbase Developer Platform](https://docs.cdp.coinbase.com/agentkit/docs/welcome)