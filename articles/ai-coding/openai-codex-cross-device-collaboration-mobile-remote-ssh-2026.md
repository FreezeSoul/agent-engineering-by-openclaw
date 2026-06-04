# OpenAI Codex 跨设备协作：移动端接入与远程安全连接架构

## 核心命题

OpenAI 将 Codex 从「桌面 IDE 插件」扩展为「跨设备协作平台」——移动端可以实时查看、批准、引导 Codex 的工作，Remote SSH 让 Codex 直接接入企业远程开发环境。这不只是一个「远程控制」功能，而是重新定义了**人类在长周期 Agent 工作中的角色**：从「监控者」变成「随时可介入的决策节点」。

> 原文：「As agents take on longer-running work, a new rhythm for collaboration is emerging. To keep work moving, you need to be able to easily answer a question, review what Codex found, change direction, approve what comes next, or add a new idea.」
> — OpenAI Engineering Blog, 2026-06-02

## 一、从桌面到口袋：协作节奏的改变

传统的 AI Coding 工具假设用户「坐在电脑前」。当 Codex 处理一个需要 2-3 小时的长任务时，用户只能等待，回来再看结果。

Codex 移动端的出现改变了这个假设：

### 1.1 实时的「介入窗口」

移动端不是看最终结果，而是**实时同步**：
- 截图、终端输出、diff、测试结果、审批请求
- 这些信息在后台实时推送到手机
- 用户可以在任何地方「take a look」

> 原文：「Your files, credentials, permissions, and local setup stay on the machine where Codex is operating, while updates flow back to your phone in real time.」

关键点：**状态在远程机器上运行，不是在手机本地**。手机只是接收状态更新的「显示终端」。

### 1.2 决策节点的人机协作

四个典型场景说明了这种协作节奏：

**咖啡馆里的 Bug 调查**：出门前让 Codex 开始调查 Bug，在等咖啡时可以 approve 继续、查看截图、最终 review diff。

**通勤中的决策点**：出门前让 Codex 做 refactor，通勤途中 Codex 找到两个可行方案需要你决定方向，到公司时任务已经在正确方向上继续执行。

**会前情报准备**：刚结束一堆会议，有个 support issue 在 Slack/email/文档中演化，下一个会是客户电话。从手机快速让 Codex 汇总最新进展。

**灵感立刻执行**：午餐、散步、听播客时突然有个想法，从手机发给 Codex，任务开始在你回到电脑前就已经在推进了。

这四种场景的共同点是：**人类不需要坐在电脑前，但 Agent 工作不需要停下来**。

## 二、Remote SSH：企业开发环境的接入

这是企业级落地的关键一步。

### 2.1 架构设计

OpenAI 没有详细说明技术实现，但从描述推断：

```
用户 Desktop → Codex (Remote SSH) → 企业远程开发环境
      ↓
手机 ChatGPT App → Codex Relay Layer → 实时状态推送
```

Codex Desktop App 自动检测 `~/.ssh/config` 中配置的主机，用户可以像本地一样在远程机器上创建项目和运行线程。

### 2.2 安全 Relay 层

关键工程问题：企业远程开发环境不能暴露在公网上。

Codex 的解决方案是一个**安全 Relay 层**：
- 机器不直接暴露在公网，而是通过 Relay 可达
- Relay 维护活跃 session 状态和上下文同步
- Relay 只传递状态更新和指令，不传递敏感凭证

> 原文：「Under the hood, Codex uses a secure relay layer that keeps trusted machines reachable across devices without exposing them directly to the public internet. That relay also keeps active session state and context synced anywhere you're signed in with ChatGPT.」

这意味着企业可以保持现有的网络安全策略（不能从外部访问的开发环境），同时让员工从任何设备接入。

### 2.3 与传统 Remote SSH 的区别

| 维度 | 传统 SSH + 终端 | Codex Remote SSH |
|------|----------------|----------------|
| **接入方式** | 命令行，手动操作 | App 级，自动发现主机 |
| **状态同步** | 无（终端是唯一状态）| 实时状态推送（截图/终端/diff）|
| **审批流程** | 无 | 内置 approval 工作流 |
| **凭证管理** | SSH key 在本地 | 凭证留在远程机器 |
| **上下文** | 每次 SSH 需要重新初始化 | Session 状态保持连接 |

## 三、企业级能力扩展

### 3.1 Programmatic Access Tokens

为企业大规模自动化设计：

```bash
# CI pipeline 中使用
curl -X POST "https://api.openai.com/codex/exec" \
  -H "Authorization: Bearer $CODEX_TOKEN" \
  -d '{"task": "run-tests", "repo": "company/main"}'
```

Scoped credentials 可以从 ChatGPT Workspace 设置直接颁发给 CI pipelines、release workflows、internal automations。

### 3.2 Hooks（GA）

Codex Hooks 全面可用，可以：
- 扫描 prompts 中的 secrets
- 运行验证器
- 记录对话
- 创建 memories
- 定制特定仓库和目录的 Codex 行为

这是 Harness 工程的核心能力——**在 Agent 执行的关键节点插入自定义逻辑**。

### 3.3 HIPAA 合规

支持在本地环境（CLI、IDE、App）中使用 Codex 进行 HIPAA 合规操作，面向符合条件的 ChatGPT Enterprise workspaces。

这意味着医疗保健组织可以在保护患者隐私的前提下，用 Codex 加速运营工作流。

## 四、安全Relay的工程分析

### 4.1 Relay 层的隐含设计

从描述来看，Relay 层有几个关键特性：

**端到端加密**：状态更新从远程机器通过 Relay 加密传输到手机。

**Session 状态保持**：不是每次请求都重新初始化上下文，而是维护一个活跃的 session 状态。

**凭证不过传**：文件、凭证、权限保留在远程机器上，手机只能看到状态更新，不能直接访问这些敏感资源。

### 4.2 与传统 VPN 的区别

| 维度 | 企业 VPN | Codex Relay |
|------|---------|------------|
| **暴露面** | 整个网络暴露给设备 | 只有 Relay 地址可访问 |
| **权限** | 设备获得网络级访问 | App 级受控访问 |
| **状态持久性** | 无（VPN 只是通道）| Session 状态保持 |
| **审计** | 网络层日志 | 指令级别审计 |

## 五、对 Harness 工程的影响

Codex 的跨设备协作引入了一个新的 Harness 维度：**分布式决策点**。

### 5.1 人类介入的时机

传统 Harness 需要预先定义「什么情况下需要人类批准」。Codex 的模型是「人类随时可以介入，但不需要一直在线」。

这对评估器循环有直接影响：
- **评估器**不是「决定是否停止」，而是「决定是否需要人类介入」
- **人类介入**不是「停止 Agent」，而是「提供额外上下文或批准」
- **Agent 继续**不需要等人类完成，可以在人类决策期间保持运行

### 5.2 状态同步的一致性

当多个设备同时接入同一个 Codex session 时：
- 手机批准了一个操作，桌面端应该立即可见
- 任何设备上的状态变更需要立即同步到所有设备
- 如果两个设备同时发出冲突指令，需要冲突检测

### 5.3 Hooks 作为 Harness 核心

Hooks 全面可用让 Codex 的 Harness 设计更精细：

```javascript
// hooks 示例：secret 扫描
{
  "event": "before_execute",
  "action": "scan_for_secrets",
  "block": true  // 发现 secret 时阻止执行
}

// hooks 示例：对话记录
{
  "event": "after_step", 
  "action": "log_conversation",
  "dest": "enterprise-siem"
}
```

这是 Harness 工程的精髓：**在关键节点拦截、检查、记录，而不是事后审计**。

## 六、笔者的判断

Codex 跨设备协作是本轮 AI Coding 战争中**企业级落地的关键拼图**。它解决了三个实际问题：

**问题一：长任务中的人类介入**。Agent 做长任务时，需要人类在某个决策点做判断。传统的做法是等用户回来，或者用户一直盯着。Codex 的方案是：让 Agent 持续工作，人类在任何地方都可以介入。

**问题二：企业远程开发环境的安全接入**。企业不让开发环境暴露在公网上，但这限制了员工的移动性。Codex 的 Relay 层在保持安全的同时提供了移动接入能力。

**问题三：大规模自动化**。Programmatic Access Tokens 让 Codex 可以集成到 CI/CD 流水线，Hooks 让企业可以在关键节点插入安全审计。

笔者认为这三条能力的组合代表了一个明确的演进方向：**AI Coding Agent 不是「桌面工具」，而是「企业基础设施」**——可以从小团队的工具扩展到大企业的安全、合规、自动化需求。

---

**引用来源**：
- [OpenAI Work with Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere)
- [OpenAI Codex Remote Connections](https://developers.openai.com/codex/remote-connections)
- [OpenAI Codex Hooks](https://developers.openai.com/codex/hooks)
- [OpenAI Programmatic Access Tokens](https://developers.openai.com/codex/enterprise/access-tokens)