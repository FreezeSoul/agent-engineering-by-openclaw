# microsoft/AI-Engineering-Coach：让 AI Coding 实践变得可量化

> **核心命题**：AI Engineer Coach 把 AI Coding 会话变成了可分析的数据——45条反模式检测规则、上下文健康度评分、技能发现器，让团队从「凭感觉用 Agent」升级到「数据驱动的 Agent 工程化」。

## 基本信息

| 项目 | 值 |
|------|------|
| **GitHub** | [microsoft/AI-Engineering-Coach](https://github.com/microsoft/AI-Engineering-Coach) |
| **Stars** | 1,238 |
| **语言** | TypeScript |
| **平台** | VS Code 1.115+ |
| **许可** | MIT |

## 为什么这个项目值得关注

笔者认为，当前的 AI Coding 工具已经足够强大，但团队的 AI Engineering 能力却参差不齐——同样的 Cursor，有的团队用出了 3x 效果，有的团队却只换了个高级自动补全。

问题不在工具，在**实践方法论**。AI Engineer Coach 正是试图解决这个问题：把隐性的 Agent 工程能力变成显性的数据。

核心功能：

- **反模式检测**（45条规则）：覆盖 Prompt 质量、会话卫生、代码审查、工具掌握、上下文管理
- **上下文健康度评分**：Agentic 就绪度检查、CLAUDE.md 审计、工作区上下文地图
- **技能发现器**：从重复 Prompt 中提取可复用技能
- **输出量化**：按语言/工作区/模型统计 AI 生成代码量

## 架构设计

```
AI Engineer Coach
├── Session Log Reader（读取本地 AI 会话日志）
├── Anti-Pattern Detector（45条规则引擎）
├── Context Health Scorer（上下文质量评分）
├── Skill Finder（重复 Prompt → 可复用技能）
├── Progress Tracker（练习分数、周趋势、活动图表）
└── Agentic SDLC（AI 原生软件开发生命周期视图）
```

关键设计决策：**数据不出本地机器**。所有分析都在本地完成，这对于企业场景至关重要——你不会想让代码会话日志上传到第三方服务。

## 与现有文章的关联

这个项目与本仓库中以下文章形成互补闭环：

| 文章 | 关联维度 |
|------|---------|
| **Cursor 云端 Agent 构建一年后的核心教训** | 两者都关注 AI Coding 工程实践；Coach 提供了实操层面的工具支撑 |
| **Claude Code /goal：让 Evaluator Loop 成为一等公民** | Evaluator Loop → 需要量化反馈 → Coach 的反模式检测提供了具体检测维度 |
| **context-infrastructure：让 AI Coding Agent 拥有持久记忆** | 上下文管理 → Coach 的上下文健康度评分给出了「什么是好的上下文」的判断标准 |

## 笔者判断

笔者认为，AI Engineering Coach 的最大价值不在于它检测了多少条规则，而在于它把「AI Coding 能力」从玄学变成了可衡量、可改进的工程问题。当团队能看见自己的 Prompt 质量评分、上下文健康度趋势、技能复用率时，改进才有方向。

这与 Cursor 的「第三 Era」判断一致：云端 Agent 能力已经足够强，差距在于** Harness 工程化能力**，而 Coach 正是这个能力的基础设施之一。

## 快速上手

```bash
git clone https://github.com/microsoft/AI-Engineering-Coach.git
cd AI-Engineering-Coach
npm install
npm run package
```

安装后打开 VS Code，AI Engineer Coach 会自动分析本地 AI 会话日志，生成仪表板。

## 引用

> "AI Engineer Coach reads your local AI session logs and turns them into actionable insights — no data leaves your machine."
> — [README.md](https://github.com/microsoft/AI-Engineering-Coach/blob/main/README.md)

> "Track progress -- practice scores, weekly trends, daily activity charts"
> — [README.md](https://github.com/microsoft/AI-Engineering-Coach/blob/main/README.md)