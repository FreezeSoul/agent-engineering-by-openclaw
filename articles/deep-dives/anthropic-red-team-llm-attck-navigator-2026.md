# AI 网络威胁的量化评估：LLM ATT&CK Navigator 与 ARiES 风险评分

> 本文解读 Anthropic 红队研究：如何将 AI 赋能的网络攻击映射到 MITRE ATT&CK 框架，并通过 ARiES 风险评分量化威胁。
>
> **一手来源**：https://red.anthropic.com/2026/attack-navigator/

---

## 核心论点

**传统的网络安全假设正在被颠覆：威胁行为者的风险等级不再由技术能力决定，而由「编排能力」决定。**

Anthropic 的红队研究分析了 832 个违规账户（2025年3月至2026年3月），发现：
- 中高风险 actor 比例从 33% 增长到 56%（半年内增幅 1.7 倍）
- 80% 的恶意 actor 使用 Claude Code（而非纯对话接口）
- **Lateral Movement（横向移动）是最高风险指标**：使用此技术的 54 个 actor 平均风险评分 56.4，比均值高 10 分

这不是一篇「AI 安全」泛泛而谈的文章。是一份**基于 13,873 次观测的实证研究**，提出了一个全新的风险评分框架 ARiES。

---

## 一、为什么旧框架失效了

MITRE ATT&CK 是网络安全的事实标准，定义了 14 个战术和数百个子技术。但它有一个根本性缺陷：

> **框架不覆盖自主行动**。 Autonomous killchain orchestration、real-time pivot decisions、AI-directed execution — 这些让最高风险 actor 与众不同的行为，没有 ID。

传统风险模型：`Risk = Threat × Vulnerability × Impact`（乘法模型）

这个模型的问题：当任何一个维度为 0 时，总体风险归零。但现实中：
- 一个实验模型的新手用户可能意外产生功能性攻击代码（intent=0，但 model 确实提供了实质性赋能）
- 一个有明确恶意意图的 actor 用模型开发了恶意软件但没有部署（impact=0，但 AI 赋能信号正是我们想要 early catch 的）

**乘法规避了这些问题，但代价是丢失信号。**

---

## 二、ARiES：加法风险评分模型

ARiES（AI Risk Enablement Score）是一个 0-100 的复合评分，由三个维度加法构成：

| 维度 | 分值 | 评估内容 |
|------|------|---------|
| **Threat** | 0-35 | actor 意图清晰度、技术熟练度、威胁情报信号、反检测策略 |
| **Vulnerability** | 0-35 | 模型赋能请求伤害的能力、接口风险画像（API vs Agentic 工具） |
| **Impact** | 0-30 | 实际或潜在后果、安全分类器评估 |

选择加法而非乘法的核心理念：

> "We wanted a score that would remain meaningful even when one dimension is absent or unclear."

加法模型保留每个维度的独立信号，即使某一维度为零或未知，部分攻击赋能模式仍然可见。

---

## 三、关键发现：技术能力不再是门槛

### 3.1 最高风险 actor 的行为特征

最有价值的发现：**技术 sophistication 不是高风险 actor 的决定性指标**。

数据支撑：
- Technical sophistication 与剩余风险成分的相关系数 r = 0.28（弱相关）
- 移除 Technical sophistication 成分后，前 6 名 actor 排名完全不变（Spearman ρ = 0.96）
- 82% 的最高风险 actor 使用 lateral movement 技术，而整体样本中只有 6.5%

**真正区分高风险 actor 的是他们用 AI 做了什么，而不是他们本身多精通技术。**

### 3.2 AI 赋能的攻击阶段分布

| 攻击阶段 | AI 使用频率 | 特点 |
|---------|-----------|------|
| 前期准备（Develop Capabilities, Obfuscation） | 高（69%/65%）| 构建工具、逃避检测 |
| 后期行动（Lateral Movement, Privilege Escalation） | 低（6.5%/2.4%）| 需要实时自适应决策 |

大多数 actor 用 AI 做「准备工作」（写恶意代码、混淆工具），但最高风险的那批人把 AI 用到了**内网横向移动和落地后的实际操作**。

这意味着：随着模型能力提升，防御重点需要从「阻止前期准备」转移到「监控后期行动」。

### 3.3 Agentic 工具的悖论

**80% 的恶意 actor 通过 Claude Code 访问模型**，这带来一个反直觉的结论：

> 界面选择（API vs Agentic coding tool）不是风险区分因素。actor 无论使用对话界面、API 还是 Agentic 工具，风险画像在统计上无法区分。

**真正重要的不是通过什么接口访问，而是请求了什么技术。**

---

## 四、对 Agent 工程的意义

### 4.1 Harness 设计的新视角

这项研究对 Agent 工程有直接启示：

**1. 工具权限 = 风险边界**

Lateral movement、credential dumping、web shell deployment 是最高风险指标。这些技术都需要在受害者网络上执行代码的能力。Harness 的权限分层直接决定了 model 的「攻击半径」。

**2. 评估器循环（Evaluator Loop）不只是「检查输出质量」**

ARiES 的 Threat 维度包含了对 actor 意图和技术熟练度的评估。这意味着：
- 高风险请求的 early detection 应该是 harness 的一部分
- 不是所有「合法的工具调用」都应该被允许

**3. 「足够好的」验证不够**

研究显示：防御规避是数据集最大的战术类别（84.4% 的 actor 使用）。传统的基于签名的检测正在被 AI 生成的多态代码绕过。

Agent harness 需要从「验证输出是否正确」升级到「验证行为模式是否可疑」。

### 4.2 新的安全度量标准

传统的安全指标：拦截了多少攻击、检测了多少恶意请求

新的安全指标应该包括：
- ARiES 风险评分分布
- Lateral movement 相关技术的调用频率
- Agentic 工具在非预期上下文中的使用

---

## 五、框架演进需求

Anthropic 的研究指出了一个核心问题：**ATT&CK 框架需要新增 ID 来覆盖自主 AI 驱动的行为**。

具体需要新增的战术/技术类别：
- Autonomous killchain orchestration（自主杀伤链编排）
- Real-time pivot decisions（实时转向决策）
- AI-directed execution with no human intervention（无人工干预的 AI 定向执行）

这不只是学术讨论。当框架开始覆盖这些行为时：
- 威胁情报共享才有共同语言
- 安全评估才有标准基准
- 防御系统才有明确的检测目标

---

## 结论

这项研究的价值不只是「AI 被用于网络攻击」这个结论。它提供了一个**量化威胁的方法论**：ARiES 加法模型。

对于 Agent 工程师，这个研究的直接启示是：

1. **权限分层是生命线**：model 能做的事越多，风险边界越大
2. **行为监控 > 输出验证**：检查 agent 做了什么比检查输出是否正确更重要
3. **编排能力是核心风险指标**：一个能协调多个攻击阶段的 agent 比一个只能生成代码的 agent 危险得多

> 原文结语：*"The dividing line between low and high-risk actors is no longer technical skill but orchestration, and where defenses, detections, and the shared frameworks we all rely on will need to evolve as fast as the attacks they describe."*

---

## 参考文献

- [LLM ATT&CK Navigator - red.anthropic.com](https://red.anthropic.com/2026/attack-navigator/)
- [MITRE ATT&CK Framework v18](https://attack.mitre.org/versions/v18/)
- [2026 Verizon DBIR](https://www.verizon.com/business/resources/reports/dbir/)