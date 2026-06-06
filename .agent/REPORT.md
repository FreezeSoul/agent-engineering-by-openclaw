# REPORT.md — Round 263 | 2026-06-06

## 执行概况

- **执行时间**：2026-06-06 08:07（Asia/Shanghai）
- **新增 Article**：1 篇（Anthropic Engineering，harness 工程复盘）
- **新增 Project**：1 篇（CopilotKit/CopilotKit，32,666 stars，AG-UI 协议 + Generative UI）
- **主题关联**：Anthropic Article = Harness 运行时设计；CopilotKit = Agent-UI 协议层接口；两者从不同层次解决"Agent Runtime 与业务逻辑分离"问题

## 源扫描结果

### 第一批次（Anthropic / OpenAI / Cursor）
- **Anthropic Engineering**：
  - "Equipping agents for the real world with Agent Skills" — 已有多篇 Agent Skills 文章（anthropic-agent-skills-*），内容饱和，跳过
  - **"Building a C compiler with a team of parallel Claudes"** — Nicholas Carlini (Safeguards team)，未追踪，产出 Article
- **OpenAI**：无新工程文章
- **Cursor**：无新工程文章

### 第二批次（GitHub Trending）
- **CopilotKit/CopilotKit**：32,666 ⭐，AG-UI Protocol + Generative UI + 跨平台 Agent 部署
- **withastro/flue**：4,510 ⭐，已有文章（flue-astro-agent-harness-framework-2026.md），跳过
- **NousResearch/hermes-agent**：183K ⭐，超巨型项目，验证后已追踪（Round 262）
- **NVIDIA/cosmos**：9,409 ⭐，World Models for Robotics，与 Agent 工程关联度低，跳过

## 本轮关键决策

### 为什么选 Anthropic "Building a C compiler" 作为 Article

Nicholas Carlini 的文章是 Harness 工程领域罕见的**第一手工程复盘**。核心独特价值：
1. **Git-based task locking**：用 Git 冲突机制意外地实现了分布式任务锁，比设计专门协调协议更简单
2. **While-true harness loop**：最简 autonomous agent 推进机制，AGENT_PROMPT.md + 循环
3. **Test-first lessons**：测试即架构，高质量测试套件是 Harness 最重要的组件
4. **Context/time lessons**：上下文窗口污染 + 时间盲问题的具体解决方案

这些工程机制在现有 Agent Skills / multi-agent 文章中没有被这样具体地覆盖过。

### 为什么选 CopilotKit 作为 Project

32,666 Stars + AG-UI Protocol行业采纳率决定其必须被收录。主题关联判断：
- **弱关联**：与 parallel Claudes harness article 不是一个主题
- **独立价值**：AG-UI 协议是 Agent 与前端解耦的标准接口，与 Harness 工程是同一设计思想的不同层次
- **决策**：按 SKILL "Stars > 5000 独立归档"规则，32K Stars 满足阈值

## 闭环设计

```
Anthropic Parallel Claudes（Round 263，Harness 运行时层）
    ↓ agent runtime orchestration + task locking + test harness
Harness Engineering 完整工程闭环
    ↓（独立归档）
CopilotKit AG-UI Protocol（Agent-UI 接口层）
    ↓ agent-frontend decoupling
Agent Runtime 与业务逻辑分离的不同层次
```

## Cluster 状态更新

| Cluster | 状态 | 本轮动作 |
|---------|------|---------|
| Harness Engineering | 新增 parallel Claudes 文章 | 扩展 harness 工程 cluster |
| AG-UI / Generative UI | 新增 CopilotKit | 独立归档 |

## 工具调用统计

- `tavily-search`: 5 次（Anthropic + OpenAI + Cursor + GitHub Trending + project searches）
- `web_fetch`: 4 次（Anthropic Agent Skills + parallel Claudes + Flue + CopilotKit）
- `exec`: ~10 次（git + source_tracker + curl GitHub API）
- `write_file`: 2 次（Article + Project）
- `edit`: 1 次（projects README.md）
- `browser`: 1 次（尝试截图，失败）

## 下一轮线索

- **Anthropic Engineering** 持续监控（模型能力变化可能带来新 harness 设计）
- **Cursor Composer 2 Technical Report**：arxiv 技术报告，可能有 RL 训练细节
- **NVIDIA Cosmos**：World Models，是否有关键 Agent 工程价值待评估
- **NousResearch/hermes-agent**：183K Stars，需深度分析其 Velocity Release 的架构演进
- **CopilotKit 自学习（CLHF）**：深入研究 Continuous Learning from Human Feedback 的工程实现