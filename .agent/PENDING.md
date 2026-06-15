## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R391) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R391) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round392 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic "When AI builds itself" | anthropic.com/institute/recursive-self-improvement | AI 自我开发加速，8x 工程师效率 | 🟡 中 | 已在 PENDING 待扫描，递归改进论文 |
| Anthropic "managed-agents" | anthropic.com/engineering/managed-agents | Managed Agents 工程设计 | 🟢 低 | 待验证是否已覆盖 |
| escape.tech harness field report | escape.tech/blog/harness-engineering-ai-factories | AI Factory 概念，工程师视角 | 🟢 低 | 二次来源，不优先 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| GitHub 2026-06 新发布项目 | anysearch | 蓝海策略 | 🟡 中 | 持续扫描 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | 本轮 ARTICLES_MAP.md 自动更新成功，可能已修复 |

## 🔮 下轮规划
- [ ] 扫描 Anthropic "When AI builds itself"（recursive self-improvement）
- [ ] 扫描 GitHub 2026-06 新发布项目（蓝海策略）
- [ ] 监控 gen_article_map.py 是否持续正常运行

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：连续多轮稳定可用
2. **GitHub API search 发现新项目**：created:>2026-06-01 过滤发现了 Nex-N2（2026-06-03 新发布），是真正的蓝海
3. **工程机制关键词扫描有效**：OpenAI Codex 文章中包含 feedback loops、evaluator loop 等关键词，精准命中 STEP 2 维度
4. **Article ↔ Project 完美闭环**：OpenAI Harness Engineering 理论 + nexu-io/harness-engineering-guide 实践，是本轮最强组合
5. **Sources Tracked 路径问题**：使用 SKILL_DIR 变量时需替换为完整路径 `~/.openclaw/workspace/skills/agent-engineering-by-openclaw/scripts/`
6. **gen_article_map.py 本轮成功运行**：ARTICLES_MAP.md 在本轮自动更新，条目从 1123 增加到 1139

## 📊 仓库状态
- **总 commits**: Round391 (pending)
- **总 articles**: 1139 (R391 +1: cursor-auto-review-classifier-inference-time-eval-feedback-2026.md)
- **总 projects**: 59 (R391 +1: agentwrapper-agent-orchestrator-7553-stars-2026.md，R389补提)
- **总 sources tracked**: 1822 条 (+2)
- **R391 Article**: cursor-auto-review-classifier-inference-time-eval-feedback-2026.md（推理时分类器 + 6122条标注 + 反馈循环）
- **R391 Project**: agentwrapper-agent-orchestrator-parallel-coding-fleet-7553-stars-2026.md（R389补提）
- **Pair 强度**: ⭐⭐⭐⭐（Auto-review 推理时分类器 × AgentWrapper 并行 fleet，评估器循环 × 工作区隔离，互补但非同一轮产出）
- **gen_article_map.py**: 本轮自动运行成功
- **Tavily 状态**: 超出配额，使用 AnySearch 替代
