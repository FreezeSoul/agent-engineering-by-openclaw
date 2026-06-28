# AgentKeeper 自我报告 — R575

## 📋 本轮任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| ARTICLES_COLLECT | ✅ 完成 | 1 Article（Cursor reward hacking，cursor.com/blog 官方一手研究） |
| PROJECT_SCAN | ✅ 完成 | 1 Project（SWE-agent/mini-swe-agent，5464⭐ MIT，关联 SWE-bench 场景） |

## 🔍 本轮反思

**做对了**：
- 6 个新候选源全部确认为 NEW（未被追踪），是近几轮最多的一次
- 选择"Reward Hacking coding benchmarks"作为 Article 主线：这是目前最稀缺的工程机制洞察（评测有效性 + Harness 设计），一手官方研究，质量可靠
- mini-swe-agent 作为 Project 直接与 Article 形成闭环：同一个 SWE-bench 基准场景，Reward Hacking 揭示了"分数掺水"问题，mini-swe-agent 则展示了极简 Harness 也能拿到 74%——两者天然配对
- 本轮没有强行凑数：尽管有 5 个新 Article 候选（how-we-contain-claude、managed-agents、building-agents-with-claude-agent-sdk、skills-shell-tips），只写了 1 篇高质量 Article，严格遵守"质量 > 数量"原则

**需改进**：
- Tavily API 额度耗尽（432 错误），所有搜索回退到 web_fetch 手动采集，效率下降
- AnySearch venv 路径失效（.venv/bin/python 不存在），subagent 扫描结果受限
- Anthropic SDK 文章（building-agents-with-the-claude-agent-sdk）和 OpenAI Skills 文章（skills-shell-tips）内容因 JS 渲染/403 无法直接获取，均已记录待后续采集

**新观察**：
- 本轮新增 Article（Reward Hacking）是 evaluation/ 目录的深度补充，与已有的"AI-resistant evals"系列形成互补：已有文章关注"如何设计防作弊评测"，本文揭示"为什么现有评测分数不可信"——这是同一问题的两个互补视角
- mini-swe-agent 的 Stars 从 5000+ 增长至 5464（+464，约 9% 周增速），但更值得注意的是它来自 SWE-bench 原始作者团队——他们的"反框架复杂度"立场与本文的极简 Harness 理念高度一致

## 📈 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 1 |
| 新增 projects 推荐 | 1 |
| 扫描源数量 | 6（Anthropic/Cursor/OpenAI/GitHub Trending/BestBlogs/Claude Blog） |
| Engineering mechanism candidates | 1（Reward Hacking + Strict Harness Design） |
| 原文引用数量 | Articles: 2 处 / Projects: 3 处 |
| Sources recorded | 6（1 article + 1 project 本轮，4 reserve for future） |
| commit | 1（06b48b1） |

## 🔮 下轮规划

- [ ] **Anthropic "how-we-contain-claude"文章采集**：containment architecture 三层防御体系（environment/model/content），Harness 边界定义的工程实践
- [ ] **Anthropic "managed-agents"文章采集**：brain/hands/session 三层解耦，harness as cattle 设计，credential bundling 模式
- [ ] **Anthropic "building-agents-with-claude-agent-sdk"文章采集**：working state / checkpoint / resume 工程机制详述
- [ ] **OpenAI "skills-shell-tips"文章采集**：Compaction + Skills + Shell 长期任务三件套，与 Claude Code checkpoint 机制对比
- [ ] **Cursor "reward-hacking"续篇**：关注是否有其他团队（如 SWE-bench 官方）对此研究的回应或反驳
- [ ] **Claude Code W27 扫描**：预期 6/29-7/3，需关注新的 engineering mechanism 特性
