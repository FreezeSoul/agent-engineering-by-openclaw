# The Agency: 107K Stars 的多工具 Agent 专家团队库

> **笔者认为**：这个项目真正解决的不是「有多少 agent」，而是「如何让 agent 的专业化程度真正可用」。大多数 agent 库止步于「给你一堆 role 描述」，而 The Agency 提供了完整的 personality + process + deliverables 三位一体的 agent 定义。这使得它在 7 天内从 0 冲到 10K Stars不是偶然——它解决了一个真实的痛点：大家都有 agent 框架，但没人有真正能打的 agent。

---

## 核心命题

**The Agency** 是一个开源的 AI agent 个性化专家库，目前在 GitHub 拥有 **107K Stars**（截至 2026 年 6 月）。每个 agent 都是一个精心设计的「专家人格」，包含：

- **Identity & Personality**：agent 的声音、沟通风格和行为模式
- **Core Mission & Workflows**：专业领域的标准操作流程
- **Technical Deliverables**：可交付的代码、文档和实际成果
- **Success Metrics**：可衡量的成功标准

用一句话概括：它是 AI coding 工具的「专家团队库」，而不是又一个 agent 框架。

---

## 为什么值得关注：专业化 vs. 通用

当前 AI agent 领域的一个核心问题是：模型很强，但大多数 agent 只是 generic prompt 的包装，缺乏真正的专业深度。The Agency 的解法是每个 agent 都经过深度设计，不仅有「做什么」，还有「怎么做」和「什么样」。

示例：**Codebase Onboarding Engineer** 这个 agent 不是简单说「了解代码库」，而是专门设计来：
- 快速理解陌生代码仓库的结构
- 只读方式探索，不修改任何代码
- 按事实陈述代码路径和行为
- 帮助新开发者理解系统，而不是代替他们做决策

这个 agent 的设计体现了「克制」——它知道自己的边界是 read-only，所以在 personality 里明确了这个约束。这才是真正的专业化 agent 设计。

---

## 多工具支持矩阵

The Agency 明确支持 **12+ 种主流 AI coding 工具**，这是它快速传播的关键：

```bash
# 支持的工具列表
./scripts/install.sh --tool claude-code    # ⭐ 推荐
./scripts/install.sh --tool copilot
./scripts/install.sh --tool cursor
./scripts/install.sh --tool openclaw       # ⭐ OpenClaw
./scripts/install.sh --tool opencode
./scripts/install.sh --tool antigravity
./scripts/install.sh --tool gemini-cli
./scripts/install.sh --tool aider
./scripts/install.sh --tool windsurf
./scripts/install.sh --tool kimi
./scripts/install.sh --tool codex
```

核心安装流程：
```bash
# 方式一：Claude Code（推荐）
./scripts/install.sh --tool claude-code

# 方式二：为所有工具生成兼容文件
./scripts/convert.sh    # 生成各工具的 agent 定义文件
./scripts/install.sh   # 交互式安装（自动检测已安装工具）

# 方式三：手动复制（只安装需要的分类）
cp engineering/*.md ~/.claude/agents/
```

笔者认为，这个多工具支持策略是聪明的：**它不试图成为一个新的 agent 运行时，而是成为所有主流运行时的高质量内容供应商。** 这让它的天花板从「另一个框架」变成了「所有框架的 agent 库」。

---

## Agent 分工体系：9 个部门 × 61 个专家

The Agency 的 agent 库按职能分为 **9 个部门**，共 **61 个专业 agent**：

| 部门 | Agent 数量 | 覆盖范围 |
|------|-----------|---------|
| 💻 Engineering | 32 | 前端/后端/移动/AI/DevOps/安全/嵌入式/合约/SRE/数据库... |
| 🎨 Design | 9 | UI/UX/品牌/视觉叙事/图像 prompt/包容性设计... |
| 💰 Paid Media | 7 | PPC/搜索分析/审计/追踪/创意/程序化/社交广告 |
| 💼 Sales | 10 | 外呼/发现/deal 策略/售前/提案/管道分析/账户策略 |
| 📢 Marketing | 32 | 增长黑客/内容/Twitter/SEO/小红书/知乎/B站/抖音/SEO... |
| 🏢 Legal | 1 | 法律文档审核 |
| ✍️ Writing | 2 | 技术写作/创意写作 |
| 🌊 Research | 1 | 深度研究 |
| 🎁 Specialized | 3 | 外呼/lead gen/多工具协调 |

Engineering 部门最大也是最核心的分类，包含了大多数开发者需要的专业角色。其中几个值得注意的 specialized agent：

- **Autonomous Optimization Architect**：自主 LLM 路由 + 成本优化 + 影子测试
- **Codebase Onboarding Engineer**：只读式代码库理解，帮助新开发者快速上手
- **AI Data Remediation Engineer**：自愈数据管道 + 空气隔离 SLM + 语义聚类
- **Feishu Integration Developer**：飞书开放平台机器人与工作流

---

## 与其他 Agent 库的关键差异

| 项目 | 类型 | 核心差异 |
|------|------|---------|
| **The Agency** | Agent Personality 库 | 深度专业化，personality + process + deliverables 三位一体 |
| **awesome-ai-agents** | 资源列表 | 只是链接集合，无 agent 定义 |
| **LangChain Agents** | 框架内置 agent | 通用型，无专业深度 |
| **crewai agents** | 框架内置 agent | 偏任务执行，缺乏 personality 设计 |

The Agency 的差异化在于**每个 agent 都有独特的 voice 和 communication style**，不是通用模板。这让它们在使用时能真正像不同类型的专家，而不是同一个模型的不同 system prompt。

---

## 使用场景

**场景 1：快速组装专家团队**
当你需要处理一个跨领域问题时，可以同时激活多个 agent：
```bash
# "Hey Claude, activate Frontend Developer and Security Engineer mode"
# 前者负责 UI 组件实现，后者负责安全审查
```

**场景 2：专业化代码审查**
Code Reviewer agent 提供了结构化的审查流程，包括安全检查和可维护性评估，不是泛泛的「代码审查」。

**场景 3：跨国市场内容**
Marketing 部门覆盖了小红书、知乎、B站、抖音等中国平台，以及英文社交平台——这对需要中英文双轨运营的团队很有价值。

---

## Stars 增长轨迹

- **7 天内**：0 → 10K Stars（病毒式传播）
- **当前**：107K Stars
- **增长驱动**：Reddit 帖子 → 开发者社区自发传播 → 多工具支持带来的网络效应

107K Stars 的增长轨迹说明：**当 agent 的专业化程度真正可用时，开发者愿意主动传播。** 这个项目验证了一个假设：市场需要的不是更多的 agent 框架，而是更好的 agent 定义。

---

## 引用

- GitHub: https://github.com/msitarzewski/agency-agents
- README: "The Agency: AI Specialists Ready to Transform Your Workflow"
- Quick Start: 支持 Claude Code、OpenClaw、Cursor、Copilot 等 12+ 工具
- 安装脚本: `./scripts/install.sh --tool <tool>`