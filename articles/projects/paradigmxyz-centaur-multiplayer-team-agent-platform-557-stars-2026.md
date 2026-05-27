# paradigmxyz/centaur：让团队共享一个 Agent 的多玩家平台

> **核心命题**：Centaur 解决了一个根本性问题——当团队中每个人都需要 AI Agent 时，是各自搭一个本地 Agent，还是共享一个中央 Agent？Centaur 的答案是后者：企业不需要管理数十个分散的 Agent 实例，而是让整个团队共享一个运行在 Kubernetes 沙箱中的 Agent，通过 Slack 或 API 直接对话。

![GitHub](screenshots/paradigmxyz-centaur-557-stars-2026-05-27.png)

## 一、为什么这个方向值得关注

在 Round 124 的文章中（第三时代 + Gartner MQ），我们观察到云端 Agent 正在成为企业级协作的核心工具。而 Centaur 的设计恰好回应了第三时代的一个核心工程问题：**如何让多个团队成员共享同一个 Agent 实例，同时保证安全隔离和凭证边界**。

传统的方案是「每人一个本地 Agent」或「每人一个云端 Agent 实例」。前者意味着重复的资源消耗和环境配置的碎片化，后者则带来了凭证管理和协作一致性的挑战。Centaur 的思路是：**一个 Agent，多个对话线程，每个线程运行在隔离的 Kubernetes 沙箱中**。

笔者认为，比起为每个团队成员单独部署 Agent 实例，Centaur 的共享架构在以下场景中有明显优势：

- **事件驱动型运营**：当 CI 失败时，团队成员在 Slack 中 @agent，Agent 在隔离环境中调查并回复
- **跨工具协作**：Agent 可以调用组织统一的工具注册表，而不是每个实例单独配置
- **凭证安全管理**：API 密钥不直接暴露给 Agent，而是通过 iron-proxy 注入

## 二、核心架构设计

```
Slack or API
    |
    v
Centaur API (控制层)
    |
    +-- Postgres 持久化状态
    +-- 工具与 Workflow 注册表
    +-- 沙箱分配
    |
    v
Kubernetes 沙箱 (隔离执行层)
    |
    +-- Agent Harness (可接入 Claude Code / Amp / Codex)
    +-- Workspace + Shell
    +-- API 介导的工具调用
    |
    v
Controlled Outbound Access (iron-proxy)
```

关键点：

1. **Harness 可插拔**：不绑定特定 Agent，支持 Amp、Claude Code、CoCode 等多种 CLI-based Agent
2. **持久化状态**：消息、执行事件、交付状态都存储在 Postgres 中，客户端可随时重连获取结果
3. **凭证边界**：通过 iron-proxy 实现「Agent 可以使用授权服务，但不暴露原始 API 密钥」
4. **Durable Workflow**：任务可以睡眠、恢复、等待事件、启动子 Agent，并穿越服务重启

> "You can also drive Centaur directly through the API: `POST /agent/spawn` (分配或复用沙箱), `POST /agent/message` (存储用户轮次), `POST /agent/execute` (启动 Agent), `GET /agent/threads/{thread_key}/events` (获取事件流)"

## 三、与现有知识体系的关联

Centaur 的架构与 Round 121（Anthropic Containment + agentfs）的「隔离」主题高度吻合：

| 维度 | Centaur | Round 121 关联 |
|------|---------|---------------|
| 隔离边界 | Kubernetes 沙箱 + 凭证管理 | 三层防御架构（环境/模型/外部内容）|
| 持久化 | Postgres 持久化线程状态 | agentfs 审计快照与可移植性 |
| 多租户 | Slack 多用户共享 | 跨 Agent 协作的 Memory 支撑 |
| Harness | 可插拔 CLI Agent | 模型无关的 Harness 抽象层 |

同时，Centaur 的「共享工具注册表」设计呼应了 Round 119（Knowledge Work Plugins）的 Skill 系统思路——工具只需要注册一次，所有 Agent 对话都可以使用。

## 四、适用场景判断

**适合使用 Centaur 的场景**：
- 团队已使用 Slack，需要在现有工作流中嵌入 AI Agent 能力
- 需要统一的凭证管理和安全边界，不想让 Agent 直接访问原始 API 密钥
- 需要持久化的工作流（跨天、跨重启的任务）
- 需要协调多步骤的运营流程（调查 CI 失败 → 修复 → 验证）

**不适合的场景**：
- 实时性要求极高的场景（每次对话都需要亚秒级响应）
- 需要完全本地化部署且无 Kubernetes 基础设施
- 对 Agent 有强烈的厂商锁定需求（Centaur 支持自定义 Harness，但需要一定技术能力）

## 五、快速上手

```bash
# 克隆仓库
git clone <repo-url>
cd centaur

# 本地需要 k3s 轻量集群（不需要完整 Kubernetes）
# 详细文档见 docs/

# Slack 接入示例
@centaur can you figure out why the billing tests are failing?

# Centaur 分配沙箱 → Agent 检查代码、运行命令、调用工具 → 结果推回 Slack
```

## 六、评价

笔者认为，Centaur 最有价值的设计在于**「多玩家 Agent」的概念**：不是每个人都有一个自己的 Agent 实例，而是整个团队共享一个 Agent，凭证和工具由平台统一管理。这种设计在企业场景下有显著的运维优势，但也带来了「多用户协调」的复杂性。

从技术成熟度来看，Centaur 目前仍处于早期阶段（v0.x），557 Stars 的社区规模相对较小，但其核心设计思路（Slack-native + Kubernetes 隔离 + 凭证边界）对于正在构建企业内部 Agent 平台的团队有直接的参考价值。

如果你正在思考「如何在团队中规模化部署 AI Agent」，Centaur 的架构值得深入研究——尤其是它的凭证边界设计和 Durable Workflow 实现。

---

**关联阅读**：
- Round 121：[Anthropic Containment 三层架构 + agentfs](/articles/deep-dives/anthropic-how-we-contain-claude-three-defense-layers-2026.md) — 隔离与安全边界
- Round 119：[Knowledge Work Plugins 三层架构](/articles/projects/anthropic-knowledge-work-plugins-three-layer-architecture-2026.md) — 统一工具注册表
- Round 124：[第三时代 + Gartner MQ](/articles/ai-coding/cursor-third-era-gartner-mq-enterprise-agent-2026.md) — 企业级 Agent 编排

**Stars**: 557 | **Created**: 2026-05-18 | **Language**: Python | **Topics**: agent, multi-agent, slack, kubernetes, sandbox