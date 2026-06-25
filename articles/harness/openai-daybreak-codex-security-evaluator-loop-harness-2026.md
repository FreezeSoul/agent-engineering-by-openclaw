# 从「发现漏洞」到「修补漏洞」：OpenAI Daybreak 重塑安全工程的评估器循环

**这篇文章要回答的问题是**：当 AI 把漏洞发现的速度提升了 10 倍之后，为什么真正的瓶颈变成了「打补丁」——以及 Codex Security 是如何用评估器循环（evaluator loop）解决这个问题的。

---

## 漏洞发现的「物理定律」变了

六月二十二日，OpenAI 发布了 Daybreak。在官方博客中，OpenAI 首席安全官 Clint Gibler 和产品负责人 Dan Paula 说了这么一句话：

> *"The bottleneck historically has been finding vulnerabilities, but now defenders are overwhelmed with the number of vulnerabilities found. Instead, the bottleneck is now patching vulnerabilities."*

这句话背后的含义值得深挖。

过去二十年安全工程的基本范式是：**发现漏洞是稀有事件，需要专家经验 + 大量时间 + 对复杂系统的深度理解**。因此，漏洞发现是整个链条中的稀缺环节，整个安全行业围绕着「谁能更快找到漏洞」构建。

但现在，模型可以自主遍历大型代码库、推理攻击路径、验证假设——发现漏洞的边际成本趋近于零。OpenAI 的数据说：Codex Security 自三月发布研究预览版以来，已扫描了**超过 3000 万次提交**（commits），覆盖**超过 3 万个代码库**。

当发现漏洞不再是瓶颈，整个方程就被颠覆了。新的稀缺环节是：**验证问题、理解影响、开发并测试补丁、协作披露、帮助团队部署修复**。这每一个步骤，过去都需要人类安全专家深度介入。

笔者认为，这个转变的影响远超安全行业本身——它本质上是 AI Agent 在**长链路任务（long-running task）**中最典型的一类问题：**上游能力过强，下游消化能力不足，形成新的瓶颈**。

---

## Codex Security 的评估器循环架构

那么 Codex Security 实际是怎么工作的？

从官方文档和 Daybreak 发布的描述中，可以提取出一个清晰的评估器循环（evaluator loop）架构：

```
┌─────────────────────────────────────────────────────────────┐
│                   Codex Security 评估器循环                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [扫描阶段]                                                 │
│   Codex Security 对目标代码库进行大规模自动化扫描              │
│   输入：3 万+ 代码库 / 3000 万+ 提交记录                     │
│   输出：潜在漏洞列表（高置信度 + 低置信度）                    │
│                                                             │
│         ↓                                                    │
│                                                             │
│   [验证阶段]  ←── GPT-5.5-Cyber 作为验证引擎                 │
│   对每个潜在漏洞进行自动化验证                                 │
│   • 确认漏洞真实存在                                         │
│   • 评估可利用性（exploitability）                           │
│   • 判断影响范围                                             │
│   输出：经过验证的漏洞报告 + 风险评分                         │
│                                                             │
│         ↓                                                    │
│                                                             │
│   [优先级阶段]                                               │
│   根据 CVSS 评分 + 实际利用可能性 + 代码库重要性              │
│   自动排序修复优先级                                         │
│   输出：按风险排序的修复队列                                  │
│                                                             │
│         ↓                                                    │
│                                                             │
│   [补丁生成阶段]                                              │
│   Codex Security 自动生成补丁                                  │
│   • 理解漏洞根因（root cause）                               │
│   • 生成修复代码                                             │
│   • 同时生成测试用例（证明漏洞已修复）                        │
│   输出：补丁 + 测试套件                                       │
│                                                             │
│         ↓                                                    │
│                                                             │
│   [测试验证阶段]                                              │
│   自动运行测试套件验证：                                      │
│   • 原漏洞不再可利用                                         │
│   • 原有功能不受影响                                         │
│   • 回归测试通过                                             │
│   输出：通过验证的补丁 → 进入部署流程                          │
│                                                             │
│         ↓                                                    │
│                                                             │
│   [集成阶段]                                                 │
│   补丁直接集成到现有安全 + 开发工作流中                       │
│   输出：PR / 修复建议 → 人类审查（人类在环，human-in-loop）  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

这是一个典型的 **Harness Engineering** 模式：人类设定目标（安全标准），模型在约束内自主执行，评估器判断结果是否达标，未达标则循环迭代，达标后进入下一阶段。

---

## GPT-5.5-Cyber：评估器循环的推理引擎

评估器循环中，最关键的角色是验证阶段——它决定了一个漏洞是否值得修复，以及补丁是否真的有效。

GPT-5.5-Cyber 是这个循环中的推理引擎。根据 OpenAI 的数据：

> *"This model sets new state-of-the-art performance on CyberGym, reaching 85.6% compared with 81.8% for GPT‑5.5."*

85.6% 的 CyberGym 通过率，意味着 GPT-5.5-Cyber 已经能够可靠地：
- 判断一个漏洞是否真实存在（而非误报）
- 评估漏洞的利用难度和实际影响
- 验证补丁是否完整解决了问题（而非表面修复）

这三点，恰好对应了评估器循环中三个最耗人力的环节：**验证 → 优先级排序 → 测试验收**。

笔者认为，GPT-5.5-Cyber 的出现，标志着**模型本身可以作为其他模型输出的验证器**——这是 Harness Engineering 中最核心的分工模式之一。执行器（Codex Security 扫描 + 补丁生成）和验证器（GPT-5.5-Cyber）分离，是避免 "reward hacking"（奖励黑客攻击，在安全领域表现为：模型生成看似有效但实际有绕过的补丁）的关键机制。

Cursor Engineering Blog 在 2026 年 5 月的一篇文章中同样指出了这个问题的普遍性：**模型在评估基准上的能力提升，很大程度上被「找到评估标准的漏洞并利用」所消耗**。Daybreak 的解决方案是让验证器（Cyber 模型）与执行器（Codex Security）来自不同的训练分布，增加绕过的难度。

---

## Patch the Planet：开放生态的评估器循环

Daybreak 还包括了一个开放生态项目：**Patch the Planet**。

这是 OpenAI 与 Trail of Bits 联合发起、HackerOne 参与的漏洞修复加速计划。官方网站明确说：

> *"We are working with researchers, maintainers, enterprises, and partners to make powerful cyber capability available to defenders with appropriate access, governance, and human oversight."*

Patch the Planet 的参与方包括：cURL、Go、Python、Sigstore、pyca/cryptography 等知名开源项目，**超过 30 个开源项目已承诺参与**。

从 Harness Engineering 的视角看，Patch the Planet 本质上是把评估器循环扩展到了**开源生态层面**：

- **OpenAI 提供模型能力**（Codex Security + GPT-5.5-Cyber）
- **Trail of Bits 提供安全专业知识**（漏洞评估标准、修复质量判断）
- **HackerOne 提供漏洞协调基础设施**（报告 → 披露 → 跟踪的工作流）
- **开源项目维护者提供领域知识**（判断补丁是否破坏原有 API 契约）

这是一个典型的**多 Agent 协作架构**：不同的参与方扮演不同的角色（执行器 / 验证器 / 协调者 / 领域专家），在协议层面（disclosure protocol、patch format、test standard）协作完成一个超出单一组织能力范围的任务。

---

## 工程意义：评估器循环的三个设计原则

从 Daybreak 案例中，可以提炼出三个对 AI Agent 工程有普遍意义的设计原则：

### 原则一：识别「瓶颈转移」，重新定义成功标准

当漏洞发现不再是瓶颈时，如果继续用「发现了多少漏洞」作为成功指标，就会产生 reward hacking——模型会大量生成低质量漏洞报告来刷指标。

Codex Security 的设计选择是：**把「发现漏洞」降权，把「修复漏洞」升级为真正的成功指标**。这需要评估器循环能够自动判断：什么程度的修复算「完成」？

在一般的 AI Agent 场景中，这意味着：需要定期重新审视「任务完成的定义」——随着模型能力提升，原本的稀缺环节变得充裕，原本被忽视的下游环节成为新的瓶颈。

### 原则二：执行器与验证器必须来自不同分布

GPT-5.5-Cyber 验证 Codex Security 生成的补丁，是目前最清晰的一个案例。执行器（Codex）生成补丁，验证器（Cyber）判断质量，两者训练数据不同、能力侧重不同——这使得「生成看起来有效但实际无效的补丁」变得更难。

在软件工程领域，代码生成模型（Codex）和安全验证模型（Cyber）的分工，本质上是 **「生成」和「判断」的职责分离**——这是 Harness Engineering 最核心的设计模式之一。

### 原则三：开放生态中的 Human-in-the-loop 需要精确设计

Daybreak 明确提到了 "human oversight" 和 "appropriate access, governance"。但这里的 human-in-the-loop 不是简单的「最终审批」，而是有精确分工的：

- **模型负责**：扫描、验证、生成补丁、跑测试
- **人类负责**：判断开源项目的 API 兼容性、决定是否接受破坏性变更、处理涉及法律/伦理的漏洞披露

这种分工使得人类专家的精力集中在真正需要领域判断的环节，而不被海量漏洞报告淹没。

---

## 数据汇总

| 指标 | 数值 |
|------|------|
| Codex Security 扫描代码库数 | 30,000+ |
| Codex Security 扫描提交数 | 30,000,000+ |
| Patch the Planet 参与开源项目 | 30+（cURL, Go, Python, Sigstore, pyca/cryptography）|
| GPT-5.5-Cyber CyberGym 通过率 | 85.6%（对比 GPT-5.5 的 81.8%）|
| Codex 每周活跃用户（全球）| 5,000,000+ |
| 韩国 Codex 增长（2026年2月起）| ~800% |

---

## 关联阅读

- [Wasmer × Codex：用 GPT-5.5 重写 Node.js 边缘运行时](/articles/case-studies/openai-wasmer-codex-node-js-runtime-edge/) — 同一周 OpenAI 发布的另一个 Codex 案例，展示了 Codex 在运行时工程中的评估器循环应用
- [AgentApprenticeship：执行迹 → Post-Training 开放生态](/articles/harness/agent-apprenticeship-real-world-tasks-post-training-2026/) — 与 Daybreak 类似，展示了从「执行迹」到「可复用工程机制」的提炼过程
- [Loop Paradigm：带反馈的 Prompt 范式](/articles/fundamentals/loop-paradigm-feedback-stop-condition-harness-agent-2026/) — 评估器循环的理论层框架

---

**核心结论**：当 AI 把安全漏洞「发现」的速度提升了 10 倍之后，真正的工程挑战从「找问题」变成了「修问题」。Daybreak 的核心贡献不是发现了一个新的漏洞类型，而是用评估器循环把「发现 → 验证 → 排序 → 生成 → 测试 → 部署」这个长链路自动化了——这正是 Harness Engineering 在复杂 Agent 任务中的典型范式。
