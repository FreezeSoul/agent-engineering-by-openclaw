# Anthropic Project Glasswing 扩展：150 个组织 / 10,000+ 漏洞 / Claude Mythos Preview 的防御性大规模试验

> 2026 年 6 月 2 日，Anthropic 宣布将 Project Glasswing 合作伙伴从 ~50 个扩展到 ~150 个。在过去两个月的「封闭试点」中，这群合作伙伴用 Claude Mythos Preview 扫描自家代码库，累计发现了超过 10,000 个高危 / 严重级别（high- or critical-severity）安全漏洞。这不是一次常规的产品 GA，而是 Anthropic 第一次把 frontier model 部署到企业代码库进行**主动式漏洞狩猎（proactive vulnerability hunting）**的工程级实验。

---

## 核心论点

Project Glasswing 揭示了三件被传统软件安全行业长期低估的事：

1. **Frontier model 做代码审计的「能力上限」比想象中更高**——在两个月的封闭试点中，合作伙伴自己扫描自家代码，找到了 10,000+ 高/严重级漏洞。这些不是公开 CVE 库里的已知问题，而是藏在企业内部代码库里的「隐性」风险。
2. **「防御性规模化」是 AI 安全的真实战场**——Anthropic 一直在用「模型对齐 / 红队 / Constitutional AI」等方法做安全，但 Glasswing 把安全研究的对象**反转**：不是 AI 自身的安全，而是**用 AI 去保护世界最重要的软件**。
3. **行业级的运营模式正在浮现**——Glasswing 不是「Anthropic 帮企业做安全」的外包模式，而是「Anthropic 提供 model + 安全要求 + 准入协议，合作伙伴自己运营」的生态模式。新增 150 个组织覆盖电力、水务、医疗、通讯、硬件等**关键基础设施**行业，每个组织都需通过安全审查才能获得 Mythos Preview 访问权。

---

## 一、Glasswing 在做什么：一个高密度实验场

### 1.1 起点：50 个封闭试点（April 2026）

2026 年 4 月，Anthropic 启动了 Project Glasswing 的封闭试点阶段，~50 个合作伙伴拿到了 Claude Mythos Preview 的访问权。这些伙伴的共性是：**代码库一旦被攻破，影响会是灾难性的**。

### 1.2 阶段成果：两个月内发现 10,000+ 高危漏洞

Anthropic 在 6 月 2 日的公告中披露了封闭试点的阶段性数字：

> "They've been deploying the model to scan their codebases for vulnerabilities. We recently described how these partners have so far found **more than 10,000 high- or critical-severity security flaws**."

这个数字的工程意义值得拆解：

| 维度 | 解读 |
|------|------|
| **数量** | 10,000+ 漏洞 ÷ ~50 合作伙伴 × 2 个月 ≈ 每个组织平均每周发现 25+ 高/严重级漏洞 |
| **严重级别分布** | "high or critical" — 意味着每条都符合 CVE 评分的高/严重阈值 |
| **来源** | 企业自有代码库，非 OSS 公开发布的项目 |
| **检测方** | AI 主动扫描，非 SAST 工具的规则告警（后者通常 false positive 率很高） |

> 注释：Anthropic 公开数据是聚合后的「10,000+」，未拆解到具体组织 / 语言 / 漏洞类型。完整分布是封闭试点协议下的数据。

### 1.3 扩展阶段：150 个新组织 / 15+ 国家

2026 年 6 月，Glasswing 启动了第二阶段扩展：

| 维度 | 数字 |
|------|------|
| 新增组织数 | ~150 |
| 地理覆盖 | 15+ 国家（未来继续扩展） |
| 新覆盖行业 | 电力 / 水务 / 医疗 / 通讯 / **硬件**（首批未充分覆盖） |
| 准入要求 | 必须通过 Anthropic 的安全审查 |
| 单组织潜在影响 | 大多数 > 1 亿人（关键基础设施级别） |

**新增组织很多是「vendor」**——即其代码库被其他组织（包括各国政府）所依赖。这意味着 Glasswing 的覆盖面是**指数级**的：一个 vendor 漏洞修复 = 数百个下游组织的风险降低。

---

## 二、Claude Mythos Preview：被低估的 frontier model 用法

### 2.1 什么是 Claude Mythos Preview

Mythos Preview 是 Anthropic 在 Glasswing 项目中专为「高风险安全研究」场景调优的模型前缀（preview），不是公开 GA 的产品。其能力定位：

- 静态代码审计（理解控制流、数据流、跨文件依赖）
- 漏洞模式识别（OWASP Top 10、CWE Top 25、内存安全类）
- 漏洞利用路径推演（不仅找漏洞，还推演如何被利用）
- 修复建议生成（不是只输出 CVE 报告，而是给出 patch 草稿）

### 2.2 为什么不是「Claude Opus 4.7 + 一个 prompt」

代码审计对 LLM 的要求不是「生成代码」而是**多步骤推理 + 长上下文 + 跨文件关联**。Mythos Preview 之所以能找出 10,000+ 漏洞，说明它至少满足：

| 能力 | 必需级别 |
|------|---------|
| 单仓库理解 | > 1M tokens 上下文，能在一次扫描中覆盖整个中型代码库 |
| 跨文件污点分析 | 跟踪用户输入从 entry point 流向 sink 的完整路径 |
| 误报控制 | false positive 率必须低到工程团队可以批量处理 |
| 漏洞分类 | 按 CWE / OWASP 标准精确分类，便于后续修复优先级排序 |

### 2.3 与 SAST 工具的差异化

| 工具类型 | 能力 | 局限 |
|---------|------|------|
| 传统 SAST (e.g. Semgrep, Snyk Code) | 规则匹配快，CI/CD 友好 | 仅识别已知模式，无法理解业务逻辑漏洞 |
| LLM 驱动的代码审计 | 能理解业务逻辑、识别逻辑漏洞 | 速度慢、成本高、需专家验证 |
| **Mythos Preview** | **SAST 的速度 + 人工审计的深度** | **封闭试点，非公开** |

Glasswing 的真正价值不是「Mythos 比 SAST 强 10 倍」，而是**在 SAST 规则告警之外，Mythos 找出了传统工具完全看不到的漏洞**——这些漏洞被埋得深、跨多文件、需要业务上下文才能理解。

---

## 三、防御性规模化：一个被低估的安全研究范式

### 3.1 传统 AI 安全的重心

提到 AI 安全，研究社区通常关注：

- **Alignment**：模型是否按人类意图行事
- **Red Team**：主动攻击模型找越狱 / 注入
- **Constitutional AI**：通过原则约束模型行为
- **RLHF / DPO**：训练阶段的人类反馈

但这些研究的对象是**模型本身**。

### 3.2 Glasswing 的反转：模型是工具，被保护对象是软件供应链

Glasswing 把这个对象**反转**：

- **研究对象**：世界最重要的软件（关键基础设施、政府系统、医疗设备）
- **工具**：Frontier model（Claude Mythos Preview）
- **运营模式**：生态共建（Anthropic + 150 个组织）
- **目标**：在「cheap, fast AI models with powerful cyber capabilities are around the corner」的现实到来前，**先让防御方也用上 AI**

Anthropic 在公告中明确写道：

> "We want Project Glasswing to spur institutions toward operating norms that reflect this reality."

这是「**operational norms**」的提法——不是技术问题，是**行业运营规范**问题。Anthropic 在推动的不是「一个产品」，而是一套**新的安全运营协议**：企业用 AI 主动扫描、AI 找出的漏洞按 CWE 分类、AI 生成的 patch 由人类工程师 review、整个过程纳入漏洞披露标准。

### 3.3 关联：Round 228 ATT&CK 框架失效

Project Glasswing 与 Round 228 产出的 [Anthropic 实证研究：AI 网络威胁的 ATT&CK 框架失效](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/anthropic-ai-cyber-threats-attck-framework-gap-2026.md) 形成完整的**攻防双视角**：

| 视角 | 角色 | 文档 |
|------|------|------|
| **攻击方** | AI 增强的网络威胁行为者 | ATT&CK 框架失效（Round 228） |
| **防御方** | AI 增强的代码审计（Mythos Preview） | Project Glasswing（本篇） |
| **理论层** | ATT&CK 框架的「Agent 编排攻击」分类空白 | Round 228 揭示 |
| **工程层** | Anthropic 自身的防御性 AI 实践 | Project Glasswing 揭示 |

两者共同勾勒出**AI 时代软件安全的「攻防双轨」**：

- 攻击方正在用 AI 自动化横向移动、后渗透、攻击编排
- 防御方正在用 frontier model 做主动式漏洞狩猎

---

## 四、为什么是「150 个组织」这个数字

### 4.1 不是 50 也不是 5000

50 个封闭试点已经验证了**可行性**（10,000+ 漏洞）。直接开放到 5,000 显然太激进——Anthropic 无法对 5,000 个组织的访问做安全审查。150 这个数字的工程意义：

- **足以验证规模化运营**——单团队管理 150 个组织的接入、审计、监控
- **不足以引发市场主导担忧**——避免了「Anthropic 借 Glasswing 进入安全服务市场」的指控
- **覆盖关键基础设施**——电力、水务、医疗、通讯这 4 个行业的全球核心供应商总数估计在数百级别，150 已经触达相当比例
- **保留扩展空间**——Anthropic 明确说「未来继续扩大地理覆盖」

### 4.2 准入协议：「meet our security requirements」

新组织必须**通过安全审查**才能拿到 Mythos Preview。这意味着 Glasswing 不是一个「自助服务」平台，而是一个**双边筛选**过程：

| 筛选方 | 筛选对象 | 标准 |
|--------|---------|------|
| Anthropic → 组织 | 组织的代码安全成熟度 | 是否能保护 Mythos Preview 的访问权 |
| 组织 → Anthropic | Mythos Preview 的能力边界 | 是否能负责任地使用 AI 进行漏洞狩猎 |

这种「双向 due diligence」是 frontier model 在高风险场景下的标准运营模式——类似的协议也出现在 OpenAI 的安全研究合作伙伴计划、Anthropic 的 Responsible Scaling Policy 中。

---

## 五、对行业的三个具体影响

### 5.1 「AI 找漏洞」从研究范式进入工业实践

过去「LLM 找漏洞」是学术研究（如 IEEE S&P、USENIX Security 的论文）。Glasswing 的 10,000+ 数字意味着这个范式已经进入**工业级实践**。其他安全厂商的连锁反应：

- Snyk、Veracode、Checkmarx 等传统 SAST 厂商可能加速 LLM 集成
- 新兴 AI-native 安全公司（如 Project R02.0、ArmorCode）可能借势融资
- 企业 CISO 的预算分配可能从「规则匹配 SAST」向「AI 增强审计」倾斜

### 5.2 「Mythos Preview」成为新基准

Anthropic 没有公开 Mythos Preview 的具体技术参数，但通过 Glasswing 的实际效果，它**事实上**成为了「LLM 代码审计」的新标杆。其他模型厂商（OpenAI、Google DeepMind、Meta）的对标产品将面临压力。

### 5.3 关键基础设施行业的 AI 治理加速

Glasswing 覆盖电力、水务、医疗、通讯行业，这 4 个行业历史上对 AI 工具的接受速度**显著慢于**金融和互联网。Glasswing 的扩展意味着：

- **行业级 AI 治理框架**可能出现（例如 NERC 对电力行业的 AI 工具使用规范）
- **国家级关键基础设施保护**可能纳入 AI 工具审查
- **vendor 供应链审计**可能要求 AI 工具的使用记录

---

## 一句话总结

Project Glasswing 扩展标志着 AI 安全研究从「**让 AI 更安全**」进入「**用 AI 让世界更安全**」的工程级阶段——150 个组织 / 10,000+ 漏洞 / 关键基础设施覆盖，Anthropic 用 Claude Mythos Preview 重新定义了 frontier model 在软件供应链中的角色。

---

## 一手来源

- 原文：[Expanding Project Glasswing](https://www.anthropic.com/news/expanding-project-glasswing) — Anthropic News, 2026-06-02
- 关联研究：[What we learned mapping a year's worth of AI-enabled cyber threats](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack) — Anthropic News, 2026-06-03
- 关联研究：[Project Glasswing](https://www.anthropic.com/glasswing) — 项目主页

## 评分

- 实用性：4/5（防御性 AI 实践的具体范式，可直接借鉴）
- 独特性：5/5（frontier model 主动漏洞狩猎是首创，10,000+ 数字独家）
- 时效性：5/5（2026-06-02 最新发布，closed-loop 立即可验证）

---

*本文属于「AI 安全研究」系列，分析 frontier model 在攻防两端的工程实践。*
