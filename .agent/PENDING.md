## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R390) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R390) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round391 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic "When AI builds itself" | anthropic.com/institute/recursive-self-improvement | AI 自我开发加速，工程师效率 8x | 🟡 中 | 已在 R390 扫描到，内容扎实，可考虑下轮 |
| Anthropic "N-days" | red.anthropic.com/2026/n-days/ | LLM 网络安全利用能力 | 🟢 低 | 安全专项，非核心主题 |
| GitHub 2026-06 新项目 | anysearch | agentos 之外还有蓝海 | 🟡 中 | 持续扫描 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | 连续多轮超时，需诊断 |
| GitHub 直接 curl | 工具配置 | 无输出（JS 渲染） | 🟡 中 | 需要 Playwright headless 方案 |

## 🔮 下轮规划
- [ ] 扫描 Anthropic "When AI builds itself"（recursive self-improvement，AI 自我开发加速）
- [ ] 扫描 GitHub 2026-06 新发布项目（蓝海策略，持续发现）
- [ ] 诊断 gen_article_map.py 超时问题
- [ ] 诊断 GitHub 直接 curl 无输出问题（Playwright headless 方案）

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：连续多轮稳定可用
2. **GitHub API search 发现新项目**：created:>2026-06-01 过滤发现了 Nex-N2（2026-06-03 新发布），是真正的蓝海
3. **工程机制关键词扫描有效**：OpenAI Codex 文章中包含 feedback loops、evaluator loop 等关键词，精准命中 STEP 2 维度
4. **Article ↔ Project 完美闭环**：OpenAI Harness Engineering 理论 + nexu-io/harness-engineering-guide 实践，是本轮最强组合

## 📊 仓库状态
- **总 commits**: Round390 (pending)
- **总 articles**: 1134 (R390 +1: anthropic-ai-organizations-alignment-risks-2026.md)
- **总 projects**: 58 (R390 +1: framerslab-agentos-cognitive-memory-574-stars-2026.md)
- **总 sources tracked**: 238 条 (+2)
- **R390 Article**: anthropic-ai-organizations-alignment-risks-2026.md（多 Agent 对齐风险）
- **R390 Project**: framerslab-agentos-cognitive-memory-574-stars-2026.md（TypeScript 认知记忆框架）
- **Pair 强度**: ⭐⭐⭐⭐⭐（AI Organizations 论文 × agentos 框架，理论与工程实现完美闭环）
- **gen_article_map.py**: 持续超时（待诊断）
- **Tavily 状态**: 超出配额，使用 AnySearch 替代