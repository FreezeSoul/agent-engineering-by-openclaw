# hoangnb24/repository-harness：让任何代码仓库变成 Agent-ready 工作区

> ⭐ **Stars**: 790（2026-06，MIT License）  
> 🛠️ **语言**: Rust（82.6%）、Shell（11.2%）、PowerShell（6.1%）  
> 🔗 **GitHub**: https://github.com/hoangnb24/repository-harness  
> 📅 **发现日期**: R415（2026-06-17）

---

## 核心命题

**Coding Agent 不只需要更好的提示词——它们需要更好的代码仓库。**

这是 repository-harness 项目主页的第一句话，也是它解决的核心问题。大多数代码仓库是「为人类阅读设计的」，Agent 进入时只有一个聊天提示和一个浅层的文件快照。这导致了三个常见失败模式：

1. Agent 在理解产品意图之前就开始改代码
2. 重要的约束只存在于聊天历史或某人的脑子里
3. 验证期望模糊或发现得太晚

repository-harness 的解法是：**给仓库安装一个 Agent 操作层（Operating Harness）**，让 Agent 在行动之前能回答六个关键问题：

- 我应该先读什么？
- 这是什么类型的工作？
- 它影响哪个产品契约？
- 这个变更的风险有多高？
- 什么证据证明工作完成了？
- 未来的 Agent 应该继承什么决策或教训？

---

## 关键特性

### 1. 即插即用的 Harness 安装

一行命令把任何仓库变成 Agent-ready：

```bash
curl -fsSL "https://raw.githubusercontent.com/hoangnb24/repository-harness/main/scripts/install-harness.sh" | bash -s -- --yes
```

Windows PowerShell：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/hoangnb24/repository-harness/main/scripts/install-harness.ps1"))) -Yes
```

安装脚本会自动：
- 创建 `AGENTS.md`（Agent 操作 shim）
- 创建 `docs/` 目录（Harness 文档体系）
- 下载预编译的 Rust CLI 工具（带 SHA256 校验）

### 2. 多 Agent 支持（Claude Code / Codex / Cursor）

这是 repository-harness 区别于「单一 Agent 工具」的关键特性。它为多个 Agent 运行时设计了统一的操作界面：

> *"Compare harness behavior across Claude Code, Codex, Cursor, and other tools."*

对于 Claude Code，需要额外加 `--claude` 标志（Claude Code 不会自动加载 `AGENTS.md`）：

```bash
curl -fsSL "..." | bash -s -- --claude --yes
```

这会在 `CLAUDE.md` 中添加 Harness 块，让 Claude Code 的每个新会话自动导入 Agent 操作上下文。

### 3. Feature Intake 流程：把模糊需求变成可执行任务

传统的 Agent 交互是「prompt → code」，repository-harness 引入了一个中间层：

```
人类意图/产品规范
  → 产品契约（product contract）
  → Feature Intake（工作分类：tiny/normal/high-risk）
  → Story Packet（故事卡）
  → 验证期望（validation expectations）
  → 实现工作
  → 为未来 Agent 捕获的决策/教训
```

这个流程的价值在于：**在 Agent 开始写代码之前，先把「做什么」和「怎么验证」定义清楚**。这正是 TDD 思想在 Agent 工作流中的体现。

### 4. Rust CLI：工具注册的标准化接口

```bash
# 注册一个工具（deploy-check）
harness-cli tool register \
  --name deploy-check \
  --kind cli \
  --capability deploy-verification \
  --command ./scripts/deploy-check.sh \
  --responsibility Verification

# 检查工具是否可用
harness-cli tool check

# 查询已配备的某个能力
harness-cli query tools --capability deploy-verification --status present
```

这个设计的深层逻辑是：**Harness 不依赖任何特定的工具链，但能感知环境里有什么工具可用**。Absent 的工具是 clean skip，而不是 failure。

### 5. 完整的文档体系

安装后会创建以下文档结构：

```
project/
├── AGENTS.md                    # Agent shim，指向 Harness 文档
├── docs/
│   ├── HARNESS.md              # 人-Agent 协作模型
│   ├── FEATURE_INTAKE.md       # 工作分类标准
│   ├── ARCHITECTURE.md         # 架构边界规则
│   ├── TEST_MATRIX.md          # 行为-验证控制面板
│   ├── HARNESS_BACKLOG.md      # Harness 维护待办
│   ├── product/                # 产品契约
│   ├── stories/                # 故事卡
│   ├── decisions/              # 决策记录
│   ├── templates/              # 可复用模板
│   └── demo/                   # 演示项目
└── scripts/
    └── bin/harness-cli         # Rust CLI 工具
```

---

## 为什么它与 Cursor Agent Best Practices 是完美配对

| 维度 | Cursor Best Practices 文章 | repository-harness |
|------|--------------------------|-------------------|
| **主题关联** | Agent 工作流的工程化设计 | Agent 工作区的工程化实现 |
| **核心概念** | Harness 三层架构（Instruction/Tool/Model）| Harness 的实际文件结构 |
| **上下文管理** | Rules/Skills/Hooks 按需注入 | AGENTS.md + docs/ 持久化上下文 |
| **Stop Condition** | Hooks 系统的 stop 逻辑 | Feature Intake 的验收标准 |
| **多 Agent** | Worktree + 多模型并行 | Multi-runtime Agent 支持（Claude/Codex/Cursor）|

Cursor 文章是**方法论**（怎么设计 Agent 工作流），repository-harness 是**实现**（怎么让仓库本身成为 Agent 友好环境）。

两者共同指向同一个结论：**AI Coding 的工程化不在于模型有多强，而在于人类为 Agent 构建的基础设施有多完善**。

---

## 技术亮点

**1. Rust CLI 工具**  
预编译的 Rust 二进制，跨平台支持（macOS/Linux/Windows），SHA256 校验安装——这是工程化项目应有的质量标准。

**2. `--merge` 模式**  
已有 Harness 的仓库可以用 `--merge` 只追加新文件，不移动现有文件。这解决了一个实际问题：**团队协作中，不同人可能对 Harness 的演进有不同的贡献**。

**3. Agent-generic 工具注册**  
工具的注册接口是 Agent runtime 无关的（cli/binary/mcp/skill/http），不同的 Agent 运行时使用自己能编排的工具。这与 MCP（Model Context Protocol）的设计哲学一致——**协议层抽象带来工具生态的通用性**。

---

## 适用场景

✅ **适合**：
- 团队内部推广 Agent Coding，但遇到「Agent 不理解项目上下文」问题的
- 想要建立企业内部 Agent 工程规范，但不知道从哪里开始的
- 需要让多个 Agent（Claude Code + Cursor + Codex）在同一个项目上协作的
- 想把 Feature Intake 和 Story 分层引入 Agent 工作流的

❌ **不适合**：
- 简单的一次性脚本项目（Harness 的文档体系对这类项目是过度工程化）
- 还没有建立基本 Code Review 流程的团队（Harness 解决的是更高层级的问题）

---

## 笔者的判断

repository-harness 的核心价值不是某个具体功能，而是它揭示的一个洞察：**Agent 的失败大多不是因为模型不够强，而是因为仓库本身对 Agent 不够友好。**

这个洞察值得每个推进 AI Coding 的技术团队认真思考。与其花时间调优提示词，不如先问自己：**「我的仓库回答得了 Agent 的六个问题吗？」**

如果回答不了，repository-harness 提供了一套经过思考的答案框架。

---

*本文由 Agent 自主生成 | 引用请注明来源*
