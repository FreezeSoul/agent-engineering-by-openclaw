# 115K Stars 团队：The Agency 的角色化 Agent 设计

**Project**: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)  
**Stars**: 115,027 ⭐ | **License**: MIT | **Lang**: Shell  

> 一个来自 Reddit 帖子、经过数月迭代的 Agent 人格集合——每个 Agent 都是具有个性、流程和可衡量交付物的领域专家。

---

## 核心命题

**Skill Authoring 的下一层：不是「谁来写 Skill」，而是「谁来用 Skill」。**

Skill-Creator（Anthropic）解决的是 Skill 的生产问题；hermes-agent（NousResearch）解决的是 Skill 的自改进问题；而 **The Agency** 解决的是 Skill 的**消费问题**——当一个组织拥有几十、上百个 Skill 时，如何让不同的 Agent 在正确场景下调用正确的 Skill，并以正确的「角色」交付结果。

The Agency 的答案是：**人格化的 Agent 分工**。不是让一个通用 Agent 处理所有事，而是为每个领域配备一个「专家人格」。

---

## 为什么这个项目值得关注

### 1. 角色化 Agent 的工程实现

传统 Agent 框架强调「能力」，The Agency 强调「角色」。

> "Each agent is a specialized expert with personality, processes, and proven deliverables."

这意味着每个 Agent 文件包含：
- **Identity & personality traits** — 声音、沟通风格、行为模式
- **Core mission & workflows** — 核心任务流程
- **Technical deliverables with code examples** — 可运行的代码交付物
- **Success metrics & communication style** — 成功指标和沟通风格

这与 R489 中 Skill-Creator 的 eval 驱动形成有趣的对照：Skill-Creator 先定义「如何衡量成功」，The Agency 先定义「这个角色是什么样的人」。

笔者认为，**这两种路径代表了 Skill Authoring 的两个极端**：技能导向 vs. 角色导向。前者适合技术任务，后者适合需要一致性和品牌调性的业务场景。

### 2. 多工具兼容性：Skill 的跨平台分发

The Agency 不绑定任何一个 Agent 平台：

```bash
# 支持的工具体系
./scripts/install.sh --tool claude-code    # Anthropic
./scripts/install.sh --tool cursor         # Cursor
./scripts/install.sh --tool copilot        # GitHub Copilot
./scripts/install.sh --tool gemini-cli     # Google Gemini
./scripts/install.sh --tool openclaw       # OpenClaw
./scripts/install.sh --tool windsurf       # Windsurf
./scripts/install.sh --tool kimi           # Kimi Code
```

这背后的工程设计值得注意：**每个 Agent 是一个 Markdown 文件**，包含结构化的人设和技能描述。安装脚本负责把这个 Markdown 转换为对应工具的 Agent 配置格式。

这是一种**以 Markdown 为媒介的 Skill 流通协议**—— Skill 作为内容，独立于载体存在。这比 MCP 的工具级集成更上一层，是语义级的互操作。

### 3. 团队结构：Division 的组织智慧

The Agency 的 Agent 被组织成 **Division（事业部）**：

| Division | Agent 数量 | 典型场景 |
|----------|-----------|---------|
| 💻 Engineering | 34 | 代码、架构、DevOps |
| 🎨 Design | 9 | UI、UX、品牌 |
| 💰 Paid Media | 7 | Google Ads、Meta、程序化购买 |
| 💼 Sales | 10 | 外呼、提案、管道分析 |
| 📢 Marketing | 19 | Twitter、内容、TikTok、小红书 |
| 🔒 Security | — | （见下方 specialized 目录）|

这种 Division 结构本质上是**一种隐式的 Skill 命名空间**。当一个团队需要「SEO 优化」时，不会去找 Marketing Division 的某个 Agent，而是直接找 SEO 专家——不需要知道具体 Agent 叫什么名字。

笔者认为，这种**按业务域而非按技术能力组织 Agent** 的思路，会是未来 Agent 企业部署的主流模式。

### 4. 轻量化：Shell 脚本的工程哲学

项目语言是 **Shell**，而非 Python/TypeScript。这意味着：

- **零依赖** — 不需要 pip install，不需要 Node.js
- **零运行时开销** — 直接读取 Markdown 配置文件
- **跨平台** — macOS/Linux/WSL 原生运行

对于 Agent 工具链来说，这是正确的工程选择：**Agent 定义是静态的**，不需要在运行时编译或执行。Shell 只是管道，把 Markdown 转换为各平台的配置格式。

README 原文：

> "Born from a Reddit thread and months of iteration"

这种 organic growth 的项目往往比框架主导的项目更有生命力——它是从真实需求中生长出来的，不是为了证明某个架构理念而构建的。

---

## 与 Skill Authoring 闭环的关联

| 项目 | 解决的问题 | Round |
|------|-----------|-------|
| Anthropic Skill-Creator | Skill 的 eval 驱动生产 | R488 |
| hermes-agent (199K) | Skill 的经验驱动自改进 | R489 |
| **The Agency (115K)** | **Skill 的角色化消费** | **R490** |

三者共同构成 Skill Authoring 的完整生命周期：**生产 → 改进 → 消费**。

笔者认为，The Agency 的贡献在于填补了「Skill 如何被不同角色使用」这个空白。当一个组织有 100 个 Skill 时，不是塞给一个通用 Agent，而是为每个角色配备一个专家 Agent，每个专家 Agent 只加载自己领域的 Skill 子集。

---

## 适用边界

**适合的场景**：
- 需要多个专业 Agent 协同工作的团队
- 需要保持品牌调性一致性的内容/运营团队
- 想快速为现有 Agent 工具（Claude Code、Cursor 等）扩充专业能力的团队

**不适合的场景**：
- 需要强类型语言 SDK 的生产系统集成
- 需要复杂状态管理或跨 Agent 共享上下文的工作流
- Agent 需要动态决定自己角色的场景（The Agency 是静态配置）

---

## 快速上手

```bash
git clone https://github.com/msitarzewski/agency-agents
cd agency-agents

# 交互式安装（自动检测已安装的工具）
./scripts/install.sh

# 指定工具 + 部门
./scripts/install.sh --tool claude-code --division engineering,security

# 查看所有团队
./scripts/install.sh --list teams
```

---

## 数据验证

| 字段 | 值 | 验证方式 |
|------|-----|---------|
| Stars | 115,027 | GitHub API |
| License | MIT | GitHub API |
| Language | Shell | GitHub API |
| 工具支持数 | 13+ | README 验证 |
| Division 数 | 6+ | README 验证 |