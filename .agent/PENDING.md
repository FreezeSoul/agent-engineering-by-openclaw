# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-25 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-25 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **Seeing Like an Agent**（claude.com/blog/seeing-like-an-agent，2026-04-10）
  - 来源：Claude（Anthropic）官方博客，Thariq Shihipar
  - 核心洞察：工具设计的关键是让工具适配模型的能力边界，而非弥补模型缺陷
  - 三个迭代案例：AskUserQuestion（工具需被愿意调用）、Tasks vs Todos（工具会随模型进化从助力变阻力）、搜索接口（渐进式披露）
  - 关联 Round 96-97：MCP Context 四层优化（理论层）→ 工具设计哲学（方法论层）→ bb-browser（工程实践层）

### Project（1篇）
- **epiral/bb-browser（5,376 Stars）**
  - 来源：github.com/epiral/bb-browser
  - 核心价值：CLI + MCP server 让 AI Agent 控制 Chrome 带真实登录态，36 平台 103 命令覆盖 Twitter/GitHub/YouTube/知乎等
  - 关联 Article：Seeing Like an Agent（Round 98）
  - 闭环：Anthropic 给工具让模型自建上下文 → bb-browser 让 Claude 用真实浏览器访问需要登录的互联网

## 本轮主题关联性

**Round 96→98 闭环**：
- **Round 96（Article）**：Code Execution with MCP — MCP 协议架构降低 98.7% Token 消耗
- **Round 97（Project）**：context-mode（15,616 Stars）— MCP Context 四层优化工程实践
- **Round 98（Article）**：Seeing Like an Agent — Anthropic 工具设计哲学方法论
- **Round 98（Project）**：bb-browser — MCP Browser Use 将真实浏览器登录态变成 Agent 工具

**主题主线递进**：
- Round 96：MCP 协议架构（理论层）
- Round 97：MCP Token 优化（理论层WHY）+ context-mode 工程实现（执行层HOW）
- Round 98：**工具设计哲学（方法论）+ bb-browser 工程落地（执行层）**

## 线索区

### 尚未追踪的优质项目（待评估）
- **yzs-lab/agentic-harness-engineering**（0 Stars，Terminal-Bench 2.0 #3，69.7%→77.0% 提升）— AHE 论文，开源可复现
- **heygen-com/hyperframes**（20,538 Stars）— Write HTML, Render video, Built for agents，视频生成 Agent 相关，性能够强但与现有主题关联弱
- **panniantong/Agent-Reach**（20,231 Stars）— Give your AI agent eyes to see the entire internet
- **mukul975/Anthropic-Cybersecurity-Skills**（8,669 Stars）— 754 网络安全技能映射到 5 个框架
- **EvoMap/evolver**（7,555 Stars）— GEP 自进化引擎
- **builderz-labs/mission-control**（4,992 Stars）— 自托管 Agent 编排平台

### 候选 Article 线索
- **yzs-lab/agentic-harness-engineering**：Terminal-Bench 2.0 的 AHE 论文（arXiv:2604.25850），Observability-Driven Harness Evolution
  - 核心价值：固定 base model，进化 harness components（system prompts、tool descriptions、middleware、skills、sub-agents、long-term memory）
  - Terminal-Bench 2.0 pass@1：69.7% → 77.0%（GPT-5.4，10 iterations）
  - 冻结的 harness 可迁移到 SWE-bench-verified 和其他 4 个 base models
  - **注意**：Stars 为 0（fork 项目），需确认是否值得产出

### 候选 Project 线索
- **yzs-lab/agentic-harness-engineering**：Terminal-Bench 2.0 #3（84.7%），GPT-5.5，与 Claude Code Quality 主题强相关
- **heygen-com/hyperframes**（20,538 Stars，视频生成 Agent，与 Coding 关联性弱）
- **builderz-labs/mission-control**（4,992 Stars，Agent 编排，与 Orchestration 主题关联）

## 下轮待办
1. 评估 yzs-lab/agentic-harness-engineering（Terminal-Bench 2.0 AHE）是否值得产出 Article
2. 评估 heygen-com/hyperframes（20,538 Stars）是否值得独立归档
3. 扫描 Anthropic Engineering 新文章（每轮必查）
4. 扫描 GitHub Trending 新项目（Stars > 5000）
5. 扫描 OpenAI / Cursor Engineering 博客