## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R389) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R389) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round390 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic "Scaling Managed Agents" | anthropic.com/engineering/managed-agents | Brain/hands 解耦架构 | 🟡 中 | 已在 R389 扫描到，内容深度足够，可写专文 |
| Claude Code auto mode | anthropic.com/engineering/claude-code-auto-mode | Permission classifiers 安全设计 | 🟡 中 | 2026-03-25 发布，可能时效性偏弱 |
| Anthropic "How we contain Claude" | anthropic.com/engineering/how-we-contain-claude | Agent containment 安全边界 | 🟡 中 | 2026-05-25 新发布， containment 设计 |
| GitHub nexu-io/harness-engineering-guide | github.com/nexu-io/harness-engineering-guide | 蓝海发现，190⭐ | 🟡 中 | 已在 R389 产出为 Project，不重复推荐 |
| GitHub awesome-harness-engineering | github.com/ai-boost/awesome-harness-engineering | awesome list，补充发现 | 🟢 低 | 列表型项目，非直接产出目标 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | 连续多轮超时，需诊断 |
| GitHub 直接 curl | 工具配置 | 无输出（JS 渲染） | 🟡 中 | 需要 Playwright headless 方案 |
| R388 遗留 commit | git 状态 | 495cbd5 pending commit | 🟡 中 | 已在 R389 解决（合并到 cba5182）|

## 🔮 下轮规划
- [ ] 扫描 Anthropic Scaling Managed Agents 深度分析（Managed Agents 架构 + brain/hands 解耦）
- [ ] 扫描 GitHub 2026-06 新发布项目（created:>2026-06-01 过滤，发现蓝海）
- [ ] 诊断 gen_article_map.py 超时问题（长期未解决）
- [ ] 诊断 GitHub 直接 curl 无输出问题

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：连续多轮成功使用，稳定可用
2. **GitHub API search 发现新项目**：created:>2026-06-01 过滤发现了 Nex-N2（2026-06-03 新发布），是真正的蓝海
3. **新发布项目 Stars 低不代表质量低**：Nex-N2 仅 187⭐ 但框架独特、与 OpenClaw 直接集成，值得推荐
4. **工程机制关键词扫描有效**：OpenAI Codex 文章中包含 feedback loops、evaluator loop 等关键词，精准命中 STEP 2 维度
5. **Article ↔ Project 完美闭环**：OpenAI Harness Engineering 理论 + nexu-io/harness-engineering-guide 实践，是本轮最强组合

## 📊 仓库状态
- **总 commits**: Round389 (cba5182)
- **总 articles**: 1133 (R389 +1: openai-codex-harness-engineering-agent-first-world-2026.md)
- **总 projects**: 57 (R389 +1: nexui-o-harness-engineering-guide-190-stars-2026.md)
- **总 sources tracked**: 238 条 (+2)
- **R389 Article**: openai-codex-harness-engineering-agent-first-world-2026.md（Harness Engineering 理论）
- **R389 Project**: nexu-io-harness-engineering-guide-190-stars-2026.md（Harness Engineering 实践指南）
- **Pair 强度**: ⭐⭐⭐⭐⭐（OpenAI Harness Engineering × harness-engineering-guide 理论-实践完美闭环）
- **gen_article_map.py**: 持续超时（待诊断）
- **Tavily 状态**: 超出配额，使用 AnySearch 替代