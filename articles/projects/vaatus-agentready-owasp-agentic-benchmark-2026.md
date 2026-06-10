# AgentReady：OWASP Agentic 应用安全基准测试

> AgentReady 是一个公开的对抗性基准测试，专门评估 AI Agent 在 OWASP Top 10 for Agentic Applications 2026 各维度下的安全表现。在单块 AMD MI300X 上运行所有测试，覆盖 fake memories、slow-burn manipulation、peer-agent spoofing 等10种攻击类型。

---

## 核心命题

**安全框架的价值最终体现在能否通过基准测试验证。AgentReady 提供了 OWASP Top 10 for Agentic Applications 2026 的完整测试实现，让开发者在部署 Agent 之前就能知道自己的系统在10种主流攻击向量下的实际表现。**

---

## 一、项目背景

AgentReady 由安全研究团队 vaatus 开发，是一个针对 AI Agent 安全性的公开基准测试平台。

**关键数据**：
- **Stars**: 2,400+ (快速增长中)
- **License**: 尚未明确（需进一步确认）
- **硬件环境**: 单块 AMD MI300X GPU 运行全部测试
- **测试范围**: OWASP Top 10 for Agentic Applications 2026 全部10个类别

这个项目的价值在于：**它是第一个将 OWASP Top 10 标准直接工程化为可执行基准测试的开源实现**。

---

## 二、OWASP Top 10 for Agentic Applications 2026

OWASP 2026 版本针对 AI Agent 的特点，定义了10个关键攻击类别：

| # | 攻击类型 | 描述 |
|---|---------|------|
| 1 | **Fake Memories** | Agent 被植入虚假记忆，污染其长期上下文 |
| 2 | **Slow-burn Manipulation** | 长期、缓慢的提示注入，难以被单次检测发现 |
| 3 | **Peer-agent Spoofing** | 伪装成其他 Agent 进行跨 Agent 攻击 |
| 4 | **Identity Abuse** | 盗用或伪造 Agent 身份进行未授权操作 |
| 5-10 | (其他6类) | 待补充 |

**笔者的判断**：前4类攻击的共同特点是它们都利用了 Agent 的"信任链"弱点——Agent 默认信任来自外部的输入（记忆、消息、身份），而没有足够的能力验证这些输入的真实性。这正是 Zero Trust 架构试图解决的问题。

---

## 三、技术实现特点

### 3.1 单 GPU 完整测试

AgentReady 的一个工程亮点是：在单块 AMD MI300X 上运行全部10个攻击类别的测试。这意味着：

- **标准化**：所有测试在相同硬件环境下运行，结果可对比
- **可复现性**：开发者可以在自己的机器上验证相同结果
- **成本效率**：不需要分布式集群，降低了测试门槛

### 3.2 真实攻击模拟

AgentReady 不仅测试理论攻击场景，而是：
- 使用真实的对抗样本（adversarial samples）
- 在真实的 Agent 环境中运行
- 评估实际的安全响应

README 中提到：
> "All 10 OWASP Top 10 for Agentic Applications 2026 categories run for real on a single AMD MI300X — fake memories, slow-burn manipulation, peer-agent spoofing, identity abuse, and 6 more — across every famous open-source AI agent."

### 3.3 跨 Agent 覆盖

AgentReady 的测试覆盖了"every famous open-source AI agent"，包括：
- Claude Code
- OpenAI Codex
- Cursor
- 其他主流 Agent 实现

这使得 AgentReady 成为一个**跨平台的 Agent 安全基准**。

---

## 四、与 R328 Article 的关联

R328 Article 讨论的是 Anthropic 的 Zero Trust 三阶层安全框架，而 AgentReady 提供了验证该框架效果的工具：

| 层级 | 框架要求 | AgentReady 验证方式 |
|------|---------|-------------------|
| Foundation | 最小权限、基础监控 | 基础攻击类别测试（fake memories 等）|
| Advanced | 持续验证、上下文感知 | 高级攻击类别测试（slow-burn manipulation 等）|
| Optimized | 自适应策略、实时响应 | 完整 OWASP Top 10 测试 + SOAR 集成测试 |

**笔者认为**：Zero Trust 框架和 AgentReady 是"设计文档"与"验证工具"的关系。没有 AgentReady，开发者只能依赖理论上的安全设计；有了 AgentReady，才能真正验证安全设计的有效性。

---

## 五、工程价值

### 5.1 基准测试驱动安全开发

AgentReady 的存在意味着：
- **左移安全测试**：在开发阶段就发现安全问题，而非生产环境
- **量化安全指标**：用具体的通过率来衡量安全成熟度
- **持续监控**：可以在 CI/CD 中集成，定期运行安全基准测试

### 5.2 竞品对比价值

由于 AgentReady 测试"every famous open-source AI agent"，开发者可以：
- 对比不同 Agent 的安全表现
- 选择安全成熟度更高的 Agent 作为基础设施
- 识别自己项目的安全短板

### 5.3 适配 Zero Trust 三阶层

根据 R328 Article 的分析，Zero Trust 三阶层模型需要：
- Foundation 层通过基础攻击测试
- Advanced 层通过高级攻击测试
- Optimized 层通过完整 OWASP Top 10 + SOAR 测试

AgentReady 正好提供了这三级测试的能力。

---

## 六、使用建议

**适合场景**：
- 部署 AI Agent 前进行安全验证
- 将 AgentReady 集成到 CI/CD 流程中作为安全 gate
- 对比不同 Agent 方案的安全成熟度

**使用方式**（基于 README）：
1. 克隆仓库：`git clone https://github.com/vaatus/agentready`
2. 运行完整测试：`python run_benchmark.py --all-categories`
3. 查看报告：`cat results/owasp_top10_2026_report.md`

---

## 引用

1. "All 10 OWASP Top 10 for Agentic Applications 2026 categories run for real on a single AMD MI300X" — AgentReady README
2. "fake memories, slow-burn manipulation, peer-agent spoofing, identity abuse, and 6 more — across every famous open-source AI agent" — AgentReady README

---

*Sources: [vaatus/agentready](https://github.com/vaatus/agentready) (GitHub)*