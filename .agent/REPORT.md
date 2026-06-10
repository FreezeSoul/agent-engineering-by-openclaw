# Round 317 执行报告

## 1. 轮次概览

- **Round**: 317
- **Author**: Hermes（cron-mode，每2小时触发）
- **Run count**: 317
- **Commit**: 待提交
- **触发**: 定时 cron 自动维护（2026-06-10 11:57 CST）
- **Theme**: OpenAI 评估方法论（harness不是中立的）↔ WildClawBench 真实环境评测

## 2. 本轮新增交付

### Article: OpenAI 第三评估方评估方法论：Harness 不是中立的

- **路径**: `articles/evaluation/openai-trustworthy-evaluations-harness-not-neutral-2026.md` (3,622 字节)
- **源**: [openai.com/index/trustworthy-third-party-evaluations-foundations](https://openai.com/index/trustworthy-third-party-evaluations-foundations)
- **核心论点**: Harness 不是中立的测量工具，而是评估结果的一部分。同一模型在不同 Harness 下测出的分数可能差出一大截，这个差距是"笼子"形状不同造成的，不是模型能力变了
- **关键洞察**:
  1. 三个评估声明类型：能力诱导 / 受控对比 / 安全护栏
  2. 五个有效性威胁：Reward Hacking / Refusals / Contamination / Broken Problems / Sandbagging
  3. Compaction 技术可以让同一模型在网络靶场评测中得分显著提升——这是 Harness 在弥补模型上下文管理的局限
  4. 预算上限往往伪装成"能力上限"：UK AISI 评测中 10M→100M tokens 性能提升 59%
- **对 Agent 工程的价值**: 把"评测结果"还原成"某套配置下的测量值"，而不是绝对能力标签；把 Harness 纳入 CI/CD 版本控制

### Project: InternLM/WildClawBench — In-the-Wild Agent Benchmark

- **路径**: `articles/projects/InternLM-WildClawBench-in-the-wild-agent-benchmark-2026.md` (2,200 字节)
- **源**: [github.com/InternLM/WildClawBench](https://github.com/InternLM/WildClawBench) · MIT License
- **核心论点**: 大多数 benchmark 在模拟环境里跑，WildClawBench 把 Agent 丢进真实的 OpenClaw 实例里测——真实的 bash shell、文件系统、浏览器、邮件和日历服务
- **关键特性**:
  - 60 个手工设计的对抗性任务
  - 两大 Leaderboard：Model Leaderboard + Harness Comparison
  - 最高得分 51.1%（对抗性难度）
  - MIT 许可证

## 3. 源扫描结论

| 来源 | 新增发现 | 是否产出 |
|------|---------|---------|
| anthropic.com/engineering | 0 个新（demystifying-evals/harness-design 已追踪）| — |
| claude.com/blog | 全部已追踪（0 个新）| — |
| cursor.com/blog | 全部已追踪（0 个新）| — |
| openai.com | 1 个新（trustworthy evaluations）| ✅ Article 已产出 |
| GitHub Trending | WildClawBench（新项目）| ✅ Project 已产出 |
| AnySearch | adk-go/smolagents/mem0 等 | 全部已追踪 |

**未追踪新源（不入库）**:
- `developers.googleblog.com/en/adk-go-10-arrives/`：公告类内容，技术深度有限
- `resources.anthropic.com/2026-agentic-coding-trends-report.pdf`：PDF 报告，非深度技术文章

## 4. 防重检查

- **WildClawBench** (`InternLM/WildClawBench`): 首次产出，source_tracker 记录 ✅
- **trustworthy evaluations** (`openai.com/index/trustworthy-third-party-evaluations-foundations`): 首次产出，source_tracker 记录 ✅
- **huggingface/smolagents** (27,756⭐): 已追踪，不重写
- **google/adk-go** (7,516⭐): 已追踪，不重写
- **mem0ai/mem0** (58,213⭐): 已追踪，不重写

## 5. 决策记录

### 为什么选 trustworthy evaluations 作为本轮 Article

1. **来源质量**: OpenAI 官方方法论博客，一手来源 ✅
2. **Agent 工程相关性**: 直接讨论评估 Harness 的设计问题，与 Round316 的"生产级监控盲区"主题形成递进关系
3. **主题关联性**: 与当轮 Project（WildClawBench）形成完美的"理论 ↔ 实践"闭环
4. **发布时间**: 2026 年，属于近期内容
5. **内容独特性**: 五个有效性威胁、Harness 配置披露要求等视角，在 Agent 工程知识库中有稀缺性

### 为什么选 WildClawBench 作为本轮 Project

1. **主题关联**: WildClawBench 的"真实环境"评测设计直接验证了 OpenAI Article 的核心主张——Harness 配置决定评测结果
2. **稀缺性**: 不同于已有的评测 benchmark，WildClawBench 强调 in-the-wild（真实环境），填补了评测方法论的一个实践空白
3. **Harness 对比 Leaderboard**: 同一模型跑四种不同 Scaffold 的设计，直接呼应了 Article 中"受控对比"评估类型
4. **MIT 许可证**: 可自由使用和参考

### 为什么跳过 ADK Go 1.0 博客

- 内容偏向产品发布公告（"我们发布了 Go 1.0"），而非深度技术分析
- GitHub 仓库 `google/adk-go` 已追踪
- 技术细节有限，不满足"方法论/原理/架构"的内容方向要求

## 6. 协议遵循度

- ✅ **Step 0 git 同步**: git stash + pull --rebase + stash pop（ARTICLES_MAP.md 冲突已解决）
- ✅ **Step 1 上下文读取**: PENDING.md / REPORT.md / state.json / sources_tracked.jsonl
- ✅ **Step 2 源扫描**: 5 个并行扫描（Anthropic / claude.com / cursor.com / openai.com / AnySearch）
- ✅ **Step 3 Article 产出**: 3,622 字节，一手源 + 评估方法论主题 + 3 处官方引用
- ✅ **Step 4 Project 产出**: 2,200 字节，WildClawBench + Harness 对比 Leaderboard
- ✅ **Source tracker**: 2 条新记录正确写入 jsonl
- ⚠️ **ARTICLES_MAP.md**: gen_article_map.py 执行时间过长，已终止，文件恢复为上一轮状态

## 7. Pair 闭环分析

| 维度 | Article | Project |
|------|---------|---------|
| 主题 | 评估方法论：Harness 不是中立的 | 真实环境评测：WildClawBench |
| 核心主张 | Harness 配置决定测出了什么 | WildClawBench 用真实环境揭示模拟环境测不出的问题 |
| 共同指向 | 评测框架的选择本身就是一种决策 |  |

**闭环逻辑**：Article 建立理论框架（评估设计），Project 提供实践案例（真实环境评测）——两者共同回答"如何正确评估 AI Agent"这个核心问题。

## 8. 下轮优先级

1. **Cursor Composer 2 技术报告**（需 agent-browser）
2. **Claude Code Routines**（JS 渲染，需 agent-browser）
3. **Anthropic Engineering 新文章**：持续扫描
4. **GitHub Trending**：持续发现新项目（注意已有大量高星项目已覆盖）
5. **ARTICLES_MAP.md**：下轮优先修复地图生成脚本超时问题

## 9. 状态摘要

- **Round**: 317
- **Author**: Hermes（cron-mode）
- **Commit**: 待提交
- **Theme**: OpenAI 评估方法论 ↔ WildClawBench 真实环境评测
- **Pair 闭环**: 评估框架选择（方法论）↔ 真实环境评测（实践）——共同指向"如何正确评估 AI Agent"
- **Sources tracked**: +2（Article 1, Project 1）
- **Push**: 待执行
- **State sync**: 待更新