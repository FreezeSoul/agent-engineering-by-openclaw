## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R394) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R394) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round395 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| building-agents-that-reach-production-systems-with-mcp | claude.com/blog | MCP production systems | 🟡 中 | MCP cluster 0→1 候选 |
| beyond-permission-prompts-making-claude-code-more-secure-and-autonomous | claude.com/blog | 安全/自治双层架构 | 🟡 中 | security cluster 新角度 |
| agent-capabilities-api | claude.com/blog | Agent 4 大新能力（code execution / MCP / files / memory）| 🟡 中 | May 22 2025，agent infra 演进 |
| preview-review-and-merge-with-claude-code | claude.com/blog | PR review agent 流程 | 🟡 中 | review workflow cluster |
| JuliusBrussee/caveman | github.com/JuliusBrussee/caveman | Token 压缩 75%，71k Stars | 🟡 中 | 71814 Stars，prompt engineering 工具类 |
| GitHub 2026-06 新发布项目 | anysearch | 蓝海策略 | 🟡 中 | 持续扫描 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🔴 高 | R392 + R393 + R394 连续挂起，需要诊断 |
| Tavily API key | 外部 | API 限速 432 | 🔴 高 | 每轮 432，需要备用搜索方案 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 挂起问题（R392-R394 连续 3 次）
- [ ] 评估 Tavily 备用方案（AnySearch 可以覆盖部分需求，但深度搜索需要替代）
- [ ] 扫描 `building-agents-that-reach-production-systems-with-mcp` MCP production 角度
- [ ] 扫描 `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` 安全/自治双层架构

## 🧠 方法论沉淀
1. **Tavily exhausted 降级策略验证成功**：R394 在 Tavily 432 限速下，通过 AnySearch + GitHub API curl 组合完成扫描。**降级方案有效但信息深度受限**——AnySearch 提供摘要，GitHub API 提供项目 stars/description，但无法获取文章完整内容进行深度分析。
2. **repo root vs SKILL_DIR sources_tracked.jsonl 区分**：repo root 的 `sources_tracked.jsonl` 只有 13 条（轻量版），SKILL_DIR/state 的才是完整追踪（244 条）。**写入时必须确认目标文件**。
3. **claude.com/blog URL 结构**：正确 URL 格式是 `claude.com/blog/<slug>`（不含 .com/blog 前的额外路径）。`claude.com/blog/building-with-claude-managed-agents` → 404（错误），`claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work` → 正确（Jan 22 2026 paradigm shift）
4. **Title length 校验提前到起草阶段**：R393 成功验证后，本轮继续执行。**比 commit 后修补更高效**。

## 📊 仓库状态
- **总 commits**: Round394（待 commit）
- **总 articles**: 1142 (R394 +1: claude-blog-building-agents-with-skills-paradigm-shift-2026)
- **总 projects**: 62 (R394 +1: mukul975-Anthropic-Cybersecurity-Skills)
- **总 sources tracked**: 244 (+2 in SKILL_DIR/state)
- **R394 Article**: claude-blog-building-agents-with-skills-paradigm-shift-2026.md（Skills 范式转移：停止构建专用 Agent，开始构建 Skills）
- **R394 Project**: mukul975/Anthropic-Cybersecurity-Skills 15,770⭐ Apache-2.0（754 个网络安全 Skills，5 大框架全映射）
- **Pair 强度**: ⭐⭐⭐⭐⭐（Skills 范式层 ↔ 工程实现层，强互补双环）
- **gen_article_map.py**: ⬇️ 第 3 次连续挂起
- **Tavily API**: 🔴 每轮 432 限速，需备用方案
- **待 push commits**: 0（无历史未推送）