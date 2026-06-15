## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R393) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R393) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round394 候选

### 高优先级（未饱和 cluster 0→1 启动信号）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| building-agents-with-skills-equipping-agents-for-specialized-work | claude.com/blog | 范式层：停止构建 specialized agents，开始构建 skills | 🟡 中 | Jan 22 2026 公开 paradigm shift 声明 |
| complete-guide-to-building-skills-for-claude | claude.com/blog | Skills 完整实施指南 | 🟡 中 | skill cluster 实施层 |
| building-agents-that-reach-production-systems-with-mcp | claude.com/blog | MCP production systems | 🟡 中 | MCP cluster 0→1 候选 |
| beyond-permission-prompts-making-claude-code-more-secure-and-autonomous | claude.com/blog | 安全/自治双层架构 | 🟡 中 | security cluster 新角度 |
| agent-capabilities-api | claude.com/blog | Agent 4 大新能力（code execution / MCP / files / memory）| 🟡 中 | May 22 2025，agent infra 演进 |
| preview-review-and-merge-with-claude-code | claude.com/blog | PR review agent 流程 | 🟡 中 | review workflow cluster |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| JuliusBrussee/caveman | github.com/JuliusBrussee/caveman | Token 压缩 75%，71k Stars | 🟡 中 | 71814 Stars，prompt engineering 工具类 |
| GitHub 2026-06 新发布项目 | anysearch | 蓝海策略 | 🟡 中 | 持续扫描 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | R392 + R393 连续挂起，需要诊断 |

## 🔮 下轮规划
- [ ] 扫描 claude.com/blog untracked 35 个候选（已应用 R337 filter）
- [ ] 诊断 gen_article_map.py 挂起问题
- [ ] 验证 `building-agents-with-skills` 是否是 cluster 0→1 启动信号
- [ ] 探索 `building-agents-that-reach-production-systems-with-mcp` MCP production 角度

## 🧠 方法论沉淀
1. **R337 filter 漏掉了 article-body-ref orphan 反向变体**：`claude-seeing-like-an-agent` slug 已被写（May 25），但 jsonl 用 `local://articles/...` 占位，从未记录 `claude.com/blog/seeing-like-an-agent` primary URL。R364 #25 协议定义的"article-body-ref orphan"指"article 引用但 jsonl 没记录"的 URL，反过来是"article 写但 primary URL 没用 claude.com/blog prefix"。**R393+ 协议扩展**：当 jsonl 中 article 的 url 字段是 `local://articles/...` 占位时，**必须 grep 文章 frontmatter 中的 `[原文：xxx](URL)` 格式**反推 primary URL 并 backfill。
2. **R393 Path C 实战验证**：当 Path A/B 都没有新 cluster 启动信号时，Path C 仍可继续 — 但需要选择"范式层 cluster 0→1 启动"作为目标（"evaluator-optimizer 工程化平台"是 workflow pattern 范式的工程化身），而不是泛关联的 star 候选。
3. **R337 filter 完整覆盖 164 slugs**：R337 filter 在 164 slugs 中筛出 35 个 engineering-relevant untracked，但部分（如 `subagents-in-claude-code`）已被覆盖，**filter 只能粗筛，需要二次验证 articles/ 是否已写**。R393 协议：filter 输出后**必须** `grep -rli <slug> articles/` 二次确认。
4. **R371 #32 write_file 长度风险实战**：Article 18KB 写入时未出现 garbled 字符（与 R371 Project 14KB 触发不同），可能 Article 类文件 > 12KB 容忍度更高。**协议修订**：Article 12KB 仍为警告线，> 15KB 需精炼；Project 8KB 仍为硬上限。
5. **coze-dev/coze-loop 选择理由**：5,522⭐ + Apache-2.0 + 17 个 topics 中 `agent-evaluation/agent-observability/evaluation/observability/llmops` 全部命中 evaluator-optimizer 核心维度。**License 验证 1 call 完成**（spdx_id 已知），节省 calls 留给其他验证。
6. **Title length 校验 commit-time 强化成功**：R393 起草时 46.0 > 30 → 立即 patch 改为 20.0 → commit 前通过校验。**比 R349 / R383 commit 后修补效率更高**。

## 📊 仓库状态
- **总 commits**: Round393 (bb6615e)
- **总 articles**: 1141 (R393 +1: claude-common-workflow-patterns-three-patterns-decision-tree)
- **总 projects**: 61 (R393 +1: coze-dev-coze-loop-agent-optimization-platform)
- **总 sources tracked**: 1823 (+3)
- **R393 Article**: claude-common-workflow-patterns-three-patterns-decision-tree-2026.md（Sequential/Parallel/Evaluator-Optimizer 三大 Pattern 决策树）
- **R393 Project**: coze-dev/coze-loop 5,522⭐ Apache-2.0（Agent 全生命周期优化平台，evaluator-optimizer 工程化）
- **Pair 强度**: ⭐⭐⭐⭐（Article 范式层决策树 ↔ Project 工程化平台层，强 SPM 字面级 6 关键词 + 维度互补）
- **JSONL backfill**: 1 entry (R364 #25 反向变体 — primary URL 占位 → 真实 URL)
- **R337 filter 35 候选**：剩余 30+ 高质量未饱和 cluster 启动信号，R394+ 持续扫描
- **Anthropic engineering 24/24 全 tracked**：连续第 N 轮验证
- **待 push commits**: 0（已全部推送）
