# walkinglabs/learn-harness-engineering：从业界最佳实践到系统性课程

**subtitle**：12 讲 × 6 项目，把 Anthropic + OpenAI 的 harness 工程理论变成可上手的工程能力

> **TL;DR**：如果你想知道"如何让 AI Coding Agent 在长任务中不摆烂"，这个 8,807 ⭐ 的 MIT 课程是当前最完整的自学资源。核心价值是把 OpenAI 和 Anthropic 的散点实践，凝练成一套可操作的方法论。

---

## 一、这个项目解决了一个长期痛点

Harness Engineering 的概念从 2025 年底开始流行，但从业者面临一个困境：**一手资料分散在 Anthropic Engineering Blog、OpenAI Blog、各公司技术博客里，没有人会给你整理成体系的学习路径**。

你可能读过 Anthropic 的 "Effective harnesses for long-running agents"，也读过 OpenAI 的 "Harness Engineering"，但：

- 这两篇文章的术语体系不同，你不确定它们说的是同一件事还是不同的事
- 读完理论还是不知道"我的 agent 应该用哪个模式"
- 没有可复用的模板和配置参考

learn-harness-engineering 做的事，就是**把散点的一手实践整合成一条学习路径**，让你从"知道有这回事"到"能在自己的 agent 里落地"。

---

## 二、课程结构一览

```
12 讲（Lectures）× 6 项目（Projects）
覆盖 5 大 Harness 子系统 + 3 种部署形态 + 14 种语言
```

### 核心讲次映射到本仓库的 Article Cluster

| 讲次 | 主题 | 对应本仓库 Cluster |
|------|------|-------------------|
| **第 1 讲** | What is Harness Engineering（是什么 + 为什么）| harness/evaluation |
| **第 2 讲** | State Management（状态管理）| context-memory |
| **第 3 讲** | Verification Loop（验证循环）| harness/evaluation |
| **第 4 讲** | Scope Control（范围控制）| harness/orchestration |
| **第 5 讲** | **Evaluator Loop（评估器循环）** | harness/evaluation ⭐ |
| **第 6 讲** | Agent Lifecycle（生命周期）| harness/orchestration |
| **第 7 讲** | Multi-Agent Harness（多 Agent 场景）| orchestration |
| **第 8 讲** | Deployment Patterns（部署形态）| infrastructure |
| **第 9 讲** | MCP Integration（MCP 集成）| tool-use |
| 第 10 讲 | Security & Permissions（安全与权限）| harness/security |
| 第 11 讲 | Evaluation & Measurement（评测）| harness/evaluation |
| 第 12 讲 | Capstone Project（毕业项目）| 全方位 |

**Evaluator Loop（第 5 讲）是本课程的核心机制**——也是本文关联的 MiMo-Code Judge Model 的理论背景。

---

## 三、课程哲学：The Model Is Smart, The Harness Makes It Reliable

课程首页给出了一个令人印象深刻的对比数据：

> **Anthropic 做过对照实验**：同一个模型（Opus 4.5），同一个任务（"build a 2D retro game editor"）。
> - **无 harness**：$9 / 20 分钟 → 产出无法运行
> - **有 harness（planner + generator + evaluator）**：$200 / 6 小时 → 产出可玩
> - **模型没变，harness 变了**

这个结论与本仓库 R437/R410 的核心论点完全一致：**在长时任务中，工程机制的权重高于模型选择**。

---

## 四、harness-creator Skill：5 分钟搭一个生产级 harness

课程配套了一个可执行的 skill：

```bash
# 在 Claude Code / Cursor 中加载
# 然后：
/skill harness-creator

# 输入项目信息，自动生成：
# ├── AGENTS.md（指令系统）
# ├── feature_list.md（范围定义）
# ├── init.sh（初始化脚本）
# └── verify.sh（验证流程）
```

这个 skill 解决的现实问题是：**你知道 harness 的概念，但你不知道怎么开始写第一个 AGENTS.md**。harness-creator 给了你一个起点，让你从"我要做什么"的角度出发，反推 harness 文件需要包含什么。

> **引用**（README）：
> "The [`skills/harness-creator/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/skills/harness-creator) skill can help you scaffold a production-grade harness (AGENTS.md, feature lists, init.sh, verification workflows) for your own project in minutes."
> — walkinglabs/learn-harness-engineering README

---

## 五、与同类资源的差异

| 资源 | 类型 | 特点 |
|------|------|------|
| **learn-harness-engineering** | 系统课程 | 12 讲 + 6 项目，有学习路径 |
| Anthropic Engineering Blog | 博客文章 | 散点，单篇质量高但无体系 |
| OpenAI Harness Engineering | 博客文章 | 单点，概念清晰但缺工程细节 |
| awesome-harness-engineering | 链接列表 | 收集全，但不做解读 |

**结论**：如果你已经读过 Anthropic 和 OpenAI 的 harness 文章，learn-harness-engineering 给你的是**把它们串联起来的框架**；如果你还没读过，这是一个带引路的起点。

---

## 六、适合谁，不适合谁

### ✅ 适合

- 已经在用 AI Coding Agent，但发现"跑久了就乱"的工程师
- 想从"会用"升级到"会设计 harness"的技术决策者
- 正在搭建企业内部 AI Coding Platform 的架构师

### ❌ 不适合

- 只想找一个现成 agent 工具拿来用的用户（这不是工具课）
- 已经在生产环境稳定运行成熟 harness 的团队（内容可能偏基础）

---

## 七、如何开始

```bash
# 直接从 GitHub clone
git clone https://github.com/walkinglabs/learn-harness-engineering.git
cd learn-harness-engineering

# 查看课程结构
cat README.md

# 从第 1 讲开始，或直接用 harness-creator skill
```

**推荐学习顺序**：先读第 1 讲（概念建立）→ 第 5 讲（Evaluator Loop，因为这是最核心的工程机制）→ 然后按需选择其他讲次。

---

> **笔者的判断**：这是目前最接近"Harness Engineering 操作系统"定位的学习资源。它的价值不在于提供了什么新概念（核心思想都在 Anthropic 和 OpenAI 的原始 blog 里），而在于**把概念组织成了一条有反馈、有项目的学习路径**。如果你在找 Agent 工程机制的系统性入门，这个仓库值得花一个周末。
