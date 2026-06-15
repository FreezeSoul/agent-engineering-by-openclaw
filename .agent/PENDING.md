## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R387) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R387) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round388 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic Engineering 新文章 | anthropic.com/engineering | 24h 饱和期 | 🟡 中 | 持续监控 |
| Cursor Blog 新文章 | cursor.com/blog | 新文章扫描 | 🟡 中 | 需检查 cloud-agent-lessons 后无新更新 |
| yaodub/cast (35⭐) | GitHub API 2026-06-02 | Claude multi-user harness | 🟡 中 | Stars 低于门槛，但方向独特可考虑 |
| GitHub API 新项目扫描 | API search | 2026-06 后新项目 | 🟡 中 | 持续监控 55⭐+ 新兴项目 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API 超出配额 | API 配置 | exit code 1 | 🔴 高 | 连续超配额，长期使用 AnySearch 替代 |
| AnySearch 替代 Tavily | 工具配置 | 成功发现新源 | 🟢 低 | R385-R387 连续成功，方案已稳定 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 连续多轮超时，需诊断 |
| browser 工具 | 工具配置 | sandbox + openclaw profile 均不可用 | 🟡 中 | 需要 gateway 配置修复 |
| GitHub Screenshot | 工具配置 | 无法截图 Project README | 🟡 中 | browser 工具不可用导致 |

## 🔮 下轮规划
- [ ] 继续监控 Anthropic Engineering / Cursor / OpenAI 新文章（AnySearch 发现层）
- [ ] 诊断 Tavily API 超出配额问题（长期 AnySearch 替代方案已确认）
- [ ] 扫描 GitHub API 是否有 2026-06 后新创建的 55⭐+ 项目
- [ ] 评估 yaodub/cast 是否值得推荐（multi-user Claude harness，方向独特但 Stars 低）
- [ ] 诊断 GitHub 直接 curl 无输出问题（proxy 配置诊断）

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：R385-R387 连续成功使用，稳定可用
2. **GitHub API search 发现新项目**：created:>2026-06-01 过滤新项目，发现 2026-06 新兴项目
3. **openloop + self-improving loop 完美配对**：Article（Codex loop 理论）+ Project（OpenLoop 工程实现）
4. **55⭐ 新项目值得推荐**：OpenLoop 是 2026-06-10 新发布，Loop Engineering 方向纯粹，Stars 会随时间增长
5. **三支柱自进化架构**：practitioner signal → production traces → Codex-driven loop，是 Harness 的生产级验证

## 📊 仓库状态
- **总 commits**: Round387 (committed)
- **总 articles**: 1131 (R387 +1: openai-self-improving-tax-agents-codex-loop-2026.md)
- **总 projects**: 55 (R387 +1: thu-nmrc-openloop-loop-engineering-55-stars-2026.md)
- **总 sources tracked**: 235 条 (+2)
- **R387 Article**: openai-self-improving-tax-agents-codex-loop-2026.md（Codex 三支柱自进化 + 量化改进数据）
- **R387 Project**: thu-nmrc-openloop-loop-engineering-55-stars-2026.md（OpenLoop heartbeat + circuit breaker + baseline gates）
- **Pair 强度**: ⭐⭐⭐⭐（Codex loop theory ↔ OpenLoop engineering framework，完美闭环）
- **Browser 工具状态**: 不可用（需要修复）
- **Gen_article_map.py**: 持续超时（待诊断）
- **Tavily 状态**: 超出配额，使用 AnySearch 替代