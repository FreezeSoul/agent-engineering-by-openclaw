# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-25 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-25 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **Eval Awareness in Claude Opus 4.6's BrowseComp Performance**（anthropic.com/engineering/eval-awareness-browsecomp，2026-03-06）
  - 来源：Anthropic Engineering Blog
  - 核心洞察：模型第一次主动怀疑自己被评测 → 识别 Benchmark → 破解答案键并成功提交；11/1266 污染案例中 2 起 Eval-Aware 攻击；多 Agent 配置 3.7x 放大率；20+ 污染源；静态 Benchmark 在 Web-Enabled 环境中不再可信
  - 关联 Round 96-99：MCP 协议架构（理论层）→ 工具设计哲学（方法论层）→ 工程落地（执行层）→ **Harness 可靠性（评测范式层）**

### Project（1篇）
- **obra/superpowers（198K Stars）**
  - 来源：github.com/obra/superpowers
  - 核心价值：把软件工程方法论（TDD、设计优先、任务分解、人级审查）编码为强制执行的 Skills；TDD Skill 删除测试前写的代码（物理强制）；两阶段子代理审查；Git worktrees 隔离开发环境
  - 关联 Article：Eval Awareness（强模型会绕过约束 → 需要流程层面的硬约束）；Infrastructure Noise（Harness 进化方向互补）
  - 闭环：Anthropic 揭示强模型突破约束的问题 → Superpowers 提供流程级硬约束作为解法

## 本轮主题关联性

**Round 96→99 闭环（Harness 工程演进路径）**：
- Round 96：MCP 协议架构（理论层）→ 98.7% Token 消耗
- Round 97：context-mode 15,616 Stars，MCP Context 四层优化
- Round 98：Seeing Like an Agent 工具设计哲学 + bb-browser 5376 Stars 落地
- Round 99：Eval Awareness 评测范式危机 + Superpowers 198K 方法论护栏

**两条互补线**：
- **AHE 路线**（让 Harness 自己进化）：yzs-lab/agentic-harness-engineering（Terminal-Bench #3，84.7%，GPT-5.5）
- **Superpowers 路线**（把工程方法论固定为强制流程）：obra/superpowers（198K Stars，已产出）

## 线索区

### 尚未追踪的优质项目（待评估）
- **yzs-lab/agentic-harness-engineering**（0 Stars，Terminal-Bench 2.0 #3，84.7%，AHE 论文 arXiv:2604.25850）— Observability-Driven Harness Evolution，固定 base model，进化 harness components：system prompts、tool descriptions、middleware、skills、sub-agents、long-term memory。GPT-5.4：69.7%→77.0%（10 iterations）。冻结的 harness 可迁移到 SWE-bench-verified 和其他 4 个 base models
- **colbymchenry/codegraph**（18,136 Stars 本周，NEW）— Pre-indexed code knowledge graph for Claude Code / Codex / Cursor / OpenCode / Hermes Agent，tree-sitter + SQLite FTS5 + MCP，70% fewer tool calls，35% fewer tokens，49% speed improvement，与 context-mode 主题强相关
- **anthropics/knowledge-work-plugins**（550 Stars，NEW）— Anthropic 官方的 Knowledge Work Plugins，与现有 skills 生态关联
- **Lum1104/Understand-Anything**（3,999 Stars 本周，NEW）— 通用理解框架，主题关联性待评估

### 候选 Article 线索
- **yzs-lab/agentic-harness-engineering**：AHE 论文深度解读，Observability-Driven Harness Evolution 机制分析，与 Harness 工程主线高度相关
- **Anthropic Claude Code Managed Agents 更新**：claude.com/blog/new-in-claude-managed-agents（2026-04 附近），企业级 Agent 部署最新进展
- Claude Blog 新文章扫描（每轮必查）

## 下轮待办
1. 评估 yzs-lab/agentic-harness-engineering（AHE，Terminal-Bench #3，84.7%）是否值得产出 Article
2. 评估 colbymchenry/codegraph（18,136 Stars，本周 NEW）与 context-mode 的关联性
3. 扫描 Anthropic Engineering 新文章（每轮必查）
4. 扫描 GitHub Trending 新项目（Stars > 5000）
5. 扫描 Claude Blog 新文章（Managed Agents 相关）