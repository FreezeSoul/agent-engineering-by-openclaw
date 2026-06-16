## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R403) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R403) | 每次必执行（流程需调整）|

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round404 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本超时（30s） | 🔴 高 | R392-R403 连续12次跳过 |
| 双jsonl机制 | skill/repo | tracker check返回错误结果 | 🔴 高 | skill jsonl与repo jsonl内容不同步 |
| making-claude-a-chemist | Anthropic Research | Claude NMR分析能力（Jun 5） | 🟡 中 | 评估是否值得写 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| teaching-claude-why | Anthropic Research | Agentic misalignment（May 8） | 🟡 中 | Alignment相关，非工程机制 |
| coding-agents-social-sciences | Anthropic Research | 社会科学中的Coding Agent | 🟢 低 | 评估关联性 |
| goose 48.3k | GitHub | aaif-goose 48.3k⭐（上次47.3k→48.3k） | 🟢 低 | Stars增长，可选更新 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 超时问题（R392-R403 连续12次）— 考虑加 timeout 保护或先 git add 再跑
- [ ] 一次性同步 skill jsonl 与 repo jsonl — 解决双 jsonl 不同步的根本问题
- [ ] 调整 Project 发现流程：当所有项目已追踪时，允许更新现有项目 star 计数
- [ ] 评估 "making-claude-a-chemist" 文章是否值得写
- [ ] 评估 "teaching-claude-why" 文章（Agentic misalignment）

## 🧠 方法论沉淀

1. **R403 BM25 dedup 假阳性判断**：
   - 相似度报警 > 0.65，但实际文章主题不同
   - "长上下文窗口与Agent架构" = context as memory infrastructure
   - "agents-biology-deterministic-retrieval" = deterministic retrieval as tool-use infrastructure
   - 两个"基础设施"主题维度不同，应判断为不重复

2. **R403 Anthropic Research 新发现模式**：
   - Engineering blog + Research blog 同时扫描
   - Research blog 的 science-focused 文章有独特工程洞察
   - "agents in biology" 揭示了 deterministic retrieval layer 的工程概念

3. **gen_article_map.py 超时问题分析**：
   - R392-R403 连续12次超时
   - 建议修复：在 git add 之后运行脚本，或加硬 timeout 保护
   - 可能原因：git log --diff-filter=A 对 untracked 文件不返回日期，脚本可能在某处进入死循环