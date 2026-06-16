## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R402) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R402) | 每次必执行（流程需调整）|

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round403 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本超时（30s） | 🔴 高 | R392-R402 连续11次跳过/每次超时 |
| 双jsonl机制 | skill/repo | tracker check返回错误结果 | 🔴 高 | skill jsonl与repo jsonl内容不同步 |
| goose 48.3k | GitHub | aaif-goose 48.3k⭐（上次47.3k） | 🟡 中 | Stars增长3k，可选更新 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Agent-Reach 27k | GitHub | panniantong 27k⭐（上次26.8k） | 🟢 低 | Stars增长~200，可选更新 |
| red.anthropic.com 扫描 | Anthropic | 红队博客可能有更多技术文章 | 🟡 中 | N-days 证明 red.anthropic.com 值得扫描 |
| AnySearch 降级 | 搜索 | 扩展 Article 来源 | 🟡 中 | 第五批次，冷却6h |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 超时问题（R392-R402 连续11次）— 考虑加 timeout 保护或先 git add 再跑
- [ ] 一次性同步 skill jsonl 与 repo jsonl — 解决双 jsonl 不同步的根本问题
- [ ] 调整 Project 发现流程：当所有项目已追踪时，允许更新现有项目 star 计数
- [ ] 扫描 red.anthropic.com 是否有更多技术文章
- [ ] 更新 goose 项目 star 计数（48.3k⭐，上次 47.3k⭐）

## 🧠 方法论沉淀

1. **R402 三层 filter pipeline 复用**：
   - AnySearch 扫描 claude.com/blog + anthropic.com + red.anthropic.com
   - source_tracker.py check 过滤（但受双 jsonl bug 影响）
   - 最终 1 高质量候选 = `2026/n-days/`
   - 下轮可复用此扫描策略

2. **R402 Project 困境的根本原因**：
   - AI Agent 工程领域已高度成熟
   - Stars > 1000 的项目均已在 repo jsonl 中追踪
   - Skill jsonl 与 repo jsonl 长期不同步导致误判
   - 需要调整流程而非继续寻找"不存在的 new 项目"

3. **R402 N-days 文章的独特价值**：
   - 首次系统性评估 LLM 在漏洞利用开发自动化方面的能力
   - 揭示 12 分钟是新的"补丁窗口"时间尺度
   - 为 Agent 能力评估提供了 Evaluator Loop 的工程范本

4. **gen_article_map.py 超时问题分析**：
   - R392-R402 连续11次超时
   - 可能原因：git log --diff-filter=A 对 untracked 文件不返回日期，脚本可能在某处进入死循环
   - 建议修复：在 git add 之后运行脚本，或加硬 timeout 保护