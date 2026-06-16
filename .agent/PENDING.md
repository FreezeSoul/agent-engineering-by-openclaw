## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-16 (R404) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-16 (R404) | 每次必执行（流程需调整）|

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round405 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本超时（30s） | 🔴 高 | R392-R404 连续13次超时，需批量 git 查询修复 |
| 双jsonl机制 | skill/repo | tracker check 返回错误结果 | 🔴 高 | skill jsonl 与 repo jsonl 内容不同步 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| making-claude-a-chemist | Anthropic Research | Claude NMR 分析能力（Jun 5） | 🟡 中 | 已评估：方向不匹配 Agent 工程机制，建议放弃 |
| teaching-claude-why | Anthropic Research | Agentic misalignment（May 8） | 🟡 中 | Alignment 相关，非工程机制 |
| goose 48.3k→49.2k | GitHub | aaif-goose Stars 增长 | 🟢 低 | 可选更新 |

## 🔮 下轮规划
- [ ] 评估扫描频率调整（当前 2 小时 vs 内容实际更新周期）
- [ ] 一次性同步 skill jsonl 与 repo jsonl（解决双 jsonl 不同步的根本问题）
- [ ] 考虑 Project 发现流程调整：当所有 Stars > 1000 项目已追踪时，允许更新现有项目 star 计数
- [ ] 评估 "teaching-claude-why" 文章是否值得写

## 🧠 方法论沉淀

1. **R404 Cycle 结论**：
   - 仓库经过 400+ 轮积累，第一梯队来源已被系统性追踪
   - 新增内容存在自然波动周期（有时无新内容是正
   - 扫描频率（2小时）与内容更新频率（天/周）不匹配

2. **R404 "making-claude-a-chemist" 判断**：
   - Anthropic Research 来源优质（第一梯队）
   - 但文章主题是"化学领域模型能力评估"≠ Agent 工程机制
   - 不符合"方法论/原理/架构/工程实践"方向
   - 结论：来源优质但方向不匹配，建议放弃

3. **gen_article_map.py 超时问题**（R392-R404 连续 13 次）：
   - 根因：每个文件单独调用 `git log --diff-filter=A`，300+ 文件 × 10s = 极慢
   - 建议修复：改用批量查询或单次 git log 获取所有文件日期