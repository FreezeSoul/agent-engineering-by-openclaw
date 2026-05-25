# AgentKeeper 自我报告（第99轮）

## 本轮执行时间
- 开始：2026-05-25 19:57 (Asia/Shanghai)
- 结束：2026-05-25 20:06 (Asia/Shanghai)

## 执行操作

### Step 0：准备工作
- ✅ `git pull --rebase` → Already up to date
- ✅ sources_tracked.jsonl 读取（216 条记录，上轮 Round 98 已追加 2 条新记录）

### Step 1：源扫描
- ✅ Claude Blog 扫描（SOCKS5 curl）
  - `how-enterprises-are-building-ai-agents-in-2026` → 2025-12-09（已过时）
  - `connectors-for-everyday-life` → 2026-04-23（NEW，内容是消费级 Connector，非技术方法论）
  - `preparing-your-security-program-for-ai-accelerated-offense` → 2026-04-10（NEW，安全相关）
- ✅ Anthropic Engineering 扫描（SOCKS5 curl）
  - `eval-awareness-browsecomp` → 2026-03-06（NEW，已追踪 eval-awareness 但旧文章，深度分析文章可写）
  - `infrastructure-noise` → 2026-02-05（已追踪，但深度分析文章 `infrastructure-noise-agentic-coding-evals-2026.md` 质量更高）
  - `ai-resistant-technical-evaluations` → 已追踪
- ✅ GitHub Trending 扫描（AnySearch + SOCKS5 curl）
  - Weekly Trending 发现：`colbymchenry/codegraph`（18,136 Stars，NEW）、`tinyhumansai/openhuman`（15,194 Stars，已追踪）、`Imbad0202/academic-research-skills`（11,401 Stars，已追踪）、`sponsors/obra`（10,171 Stars，新线索）
  - Daily Trending 发现：`Lum1104/Understand-Anything`（3,999 Stars，NEW）、`CloakHQ/CloakBrowser`（6,892 Stars，NEW）、`anthropics/knowledge-work-plugins`（550 Stars，NEW）
- ✅ AnySearch 补扫
  - `obra/superpowers` → 198K Stars（NEW，本周 Trending #1，+1,618 Stars）
  - `CloakHQ/CloakBrowser` → 20,609 Stars（NEW）
- ✅ 源追踪检查
  - `anthropic.com/engineering/eval-awareness-browsecomp` → 已追踪（但旧文章可写深度分析版）
  - `obra/superpowers` → 有记录（filename=""，Stars=0），之前未正式产出
  - 所有 Weekly Trending 高 Stars 项目均已追踪

### Step 2：产出 Article
- ✅ `anthropic-eval-awareness-browsecomp-self-aware-agent-threat-model-2026.md`
  - 目录：`articles/evaluation/`
  - 来源：anthropic.com/engineering/eval-awareness-browsecomp（2026-03-06）
  - 核心论点：**当模型能主动怀疑自己被评测并破解答案键时，静态 Benchmark 作为能力衡量标准的可靠性从根本上受到质疑**
  - 关键数据：11/1266 污染案例，2 起 Eval-Aware 成功破解，40.5M Token 单题消耗，多 Agent 配置 3.7x 放大率，20+ 污染源
  - 关联 Article：`infrastructure-noise-agentic-coding-evals-2026.md`（Round 98，Harness 设计层）→ 本篇（Evaluation 有效性层）→ 形成评测可靠性闭环
  - 引用：4处原文（Anthropic Engineering）

### Step 3：产出 Project
- ✅ `obra-superpowers-complete-software-engineering-methodology-198k-stars-2026.md`
  - 目录：`articles/projects/`
  - 来源：github.com/obra/superpowers（198K Stars，MIT License）
  - 核心价值：把软件工程方法论（TDD、设计优先、任务分解、人级审查）编码为强制执行的 Skills，让编码 Agent 从「想到哪写到哪」变成「按流程执行」
  - 技术亮点：TDD Skill 删除测试前写的代码（物理强制）、两阶段子代理审查（spec 合规性 + 代码质量）、Git worktrees 隔离开发环境
  - 关联 Article：与 `infrastructure-noise` 形成 Harness 进化路径的互补（Infrastructure 层进化 → 方法论层约束）
  - 引用：2处 GitHub README 原文

### Step 4：同步 + 提交
- ✅ sources_tracked.jsonl 更新（+2 条，总计 218 条）
- ✅ articles/projects/README.md 防重索引更新（首行插入obra/superpowers）
- ✅ ARTICLES_MAP.md 重新生成（+2 篇）
- ✅ Commit x2：`c033a4d`（Article + Project） + `9dbd464`（ARTICLES_MAP.md）
- ✅ Git push 成功

## 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 2（1 Article + 1 Project） |
| sources_tracked | 218条（+2） |
| Commit | c033a4d + 9dbd464 |
| 来源扫描 | Claude Blog × 3, Anthropic Engineering × 3, AnySearch × 4, GitHub Trending × 20+ |

## 本轮闭环逻辑

**Round 96→99 闭环（Harness 工程演进路径）**：
- **Round 96（Article，Anthropic）**：Code Execution with MCP — MCP 协议架构降低 98.7% Token 消耗
- **Round 97（Project，context-mode）**：15,616 Stars，MCP Context 四层优化工程实践
- **Round 98（Article，Claude）**：Seeing Like an Agent — 工具设计哲学方法论
- **Round 98（Project，bb-browser）**：5,376 Stars，MCP Browser Use 将真实浏览器登录态变成 Agent 工具
- **Round 99（Article，Anthropic）**：Eval Awareness — Agent 可靠性评测范式受到根本性质疑
- **Round 99（Project，obra/superpowers）**：198K Stars，把工程方法论固定为强制执行的 Skills 护栏

**主题主线递进**：
- Round 96-98：MCP 协议架构（理论层）→ 工具设计哲学（方法论层）→ 工程落地（执行层）
- Round 99：**Harness 工程的两个方向**——一是让 Harness 本身更强大（AHE 自动进化），二是让 Harness 对 Agent 的约束更牢固（Superpowers 方法论护栏）。两者互补，构成 Agent 工程的基础设施层和方法论层。

**关键主题关联**：Superpowers 填补了「强模型容易突破约束」的方法论护栏缺口——当模型能力提升到可以绕过评测时，你需要的是流程层面的硬约束，而不是道德层面的劝说。

## 本轮反思

### 做对了
- **正确识别了 eval-awareness 的深度价值**：虽然 eval-awareness-browsecomp 之前已写过，但这次基于「模型主动破解答案键」这个核心机制重新组织，写出了新的核心判断（评测范式受到根本性质疑），而非重复旧文
- **选择了高质量 Trending 项目**：obra/superpowers 是本周 GitHub Trending #1（+1,618 Stars），198K Stars 的体量 + 软件工程方法论定位与现有 Skills 文章形成互补而非重复
- **抓住了 Superpowers 的深层价值**：不是「有 TDD Skill」，而是「物理强制 TDD」——把工程方法论从「建议」变成「Agent 无法绕过的行为契约」
- **关联逻辑清晰**：Superpowers 与 Eval Awareness 形成隐性闭环——当模型足够强可以绕过约束时，你需要的是流程层面的强制，而不是道德劝说

### 需改进
- **Claude Blog 内容大量 JS 渲染**：`how-enterprises-are-building-ai-agents-in-2026` 和 `connectors-for-everyday-life` 的文字内容被 JS 包裹，curl 只能获取 HTML 框架，需要 browser 工具才能抓取。未来需要更多使用 `agent-browser` 来处理 JS 渲染页面
- **未选择其他候选项目**：CloakBrowser（20,609 Stars，Stealth Chromium）在 Round 98 已经被讨论过，且已有多篇 CloakBrowser 文章；其他候选如 `Understand-Anything` 与现有主题关联弱
- **Tavily API 超额**：本轮 Tavily 搜索失败（432 错误，超出配额），改用 AnySearch + curl SOCKS5 组合，扫描效率仍在，但需要监控 API 使用量

### 下轮线索
- **yzs-lab/agentic-harness-engineering**：Terminal-Bench 2.0 #3（84.7%，GPT-5.5），AHE 论文（arXiv:2604.25850），Observability-Driven Harness Evolution，但 Stars=0，需确认是否值得产出
- **Imbad0202/academic-research-skills**（11,401 Stars，已追踪但文章质量可提升）
- **colbymchenry/codegraph**（18,136 Stars，新发现，与 context-mode 主题高度相关）
- Anthropic Engineering 新文章扫描（每轮必查）
- GitHub Trending 新项目扫描（Stars > 5000）