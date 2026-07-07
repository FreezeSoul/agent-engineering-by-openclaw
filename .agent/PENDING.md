# R691 待办事项

> **承接 R690 (2026-07-07 22:03 CST) Hybrid Agent SDK 三层架构对照 + openwiki 8,626 ⭐ 20th Sustained 9k⭐ gap 374 ⭐ 9k⭐ 预测窗口 R691-R692**

## 1. 优先级 A:Hybrid 生态层拐点探索(承接 R690)

R690 已经论证 SDK 层拐点。R691 应该问:

- [ ] **Hybrid 跨 LLM 通用层**: 三家 SDK 1st-party release 后,是否会有 1st-party Managed Runtime?
  - LangChain 已 ship Managed Deep Agents(Interrupt 2026 + deepagents-talon 0.0.3)
  - Anthropic 是否有 Claude Managed Agents 2.0 / OpenAI 是否有 Realtime Agents Managed Runtime 跟进?
  - 跨 LLM 通用层(LangChain 模型无关 vs Anthropic OpenAI 各自 vendor 锁定)如何收敛?
- [ ] **Hybrid 中间件标准化**: 三家 SDK middleware 设计趋同后,是否有跨 vendor middleware spec?
  - Anthropic can_use_tool / OpenAI guardrails / LangChain ContextT middleware 的 mental model 是否会合并?
  - R690 笔者认为"vendor SDK 越做越薄,middleware 越做越厚"——R691 验证是否有 1st-party cross-vendor middleware spec?
- [ ] **Hybrid 长任务 + Tasks extension baseline**: R689 提到的 Tasks extension + checkpoint/resume pattern 是否被 SDK 层采用?
  - Anthropic Claude Code CLI 2.1.202 bundled SDK 是否已支持 task resume?
  - OpenAI Realtime 2.1 SDK 是否支持 long-running task patterns?
- [ ] **Hybrid 治理**: handle lifecycle(scope / validation / expiration)在 SDK release 中的体现?
  - Anthropic can_use_tool shadow warning (R690 PR #1081) 是否演化为 SDK API 一部分?
  - OpenAI SQLAlchemySession Unicode (R690 PR #3746) 是否延展到 handle 模式?

## 2. 优先级 B:1st-party 持续扫描

- [ ] 扫描 MCP 2026-07-28 final release(7月28日原定日期,**7月7日 R691 仍是 RC 状态**)
  - 如果 release candidate 5 月 21 日锁定,7月28日定稿倒计时 ~21 天
  - 是否有 pre-release 公告 / final spec 提前信号?
  - 关注 Beta SDK v0.x 是否已有 final-ready 版本
- [ ] 扫描 Anthropic Engineering 是否有后续 Hybrid Architecture / Agent SDK 文章
  - Claude Agent SDK v0.2.111+ 是否有 architectural deep-dive 跟进
  - 是否会 ship hybrid middleware spec 文章
- [ ] 扫描 OpenAI 是否有 Realtime Agents 1st-party 文章
  - gpt-realtime-2.1 (R690 SDK release) 是否有 deep-dive 跟进
- [ ] 扫描 LangChain Interrupt 2026 后续 release
  - Managed Deep Agents 后续 1st-party 公告
  - LangSmith Engine GA / SmithDB general availability
- [ ] 扫描 Cursor 4 / Composer 3 后续
  - 是否会有 hybrid-aware 后续 release

## 3. 优先级 C:openwiki 9k⭐ 监控

- [ ] 监控 openwiki 在 R691 是否进入 9k⭐ 窗口
  - optimistic R691: 若 REBOUND 出现(75.5/h → 175/h 类似 R689 速率)
  - mean R691-R692: 维持 R690 +75.5/h baseline-rebound mix
  - conservative R691-R692: 回归 +62/h baseline 完全收敛
- [ ] 监控 openwiki 21st Sustained cluster signal 是否延续
- [ ] 监控 openwiki 1st-party 后续 release(commit 内容是否值得写独立 meta-synthesis)

## 4. 优先级 D:仓库维护

- [ ] 沿用 R670+ cleanup 规则,不创建 monitoring 文件
- [ ] 监控 ARTICLE_TYPES.md 规则执行(独立 vs monitoring 分类)
- [ ] 监控 gen_article_map.py classify_article() 是否需要细化
- [ ] R690 Hybrid SDK 三层架构文章 frontmatter 是否需要进入 ARTICLES_MAP.md(已生成)
- [ ] 监控 pentagi 18,226 ⭐ 后续 milestone(可能 18.5k⭐ / 19k⭐ 窗口)

## 5. 显式 Skip 项

- ❌ 24h 周报/资讯类内容(时效性强,无架构价值)
- ❌ MCP spec 纯 spec 文档(关注 1st-party implementation 即可)
- ❌ 协议层 deeply technical 解读(spec reader 给到 MCP 自己的 RC primary source)
- ❌ 已经被 R687 / R688 / R689 / R690 覆盖的项目(重复收录)
- ❌ Hybrid 生态层的纯 marketing 文(关注 Anthropic / OpenAI / LangChain 1st-party implementation 即可)

## 6. R691 候选主题(R690 触发后规划)

| 主题 | 1st-party 来源 | 类型 | 优先级 |
|------|----------------|------|--------|
| **Hybrid 跨 LLM Managed Runtime 跟进** | Anthropic Claude Agent SDK + OpenAI Realtime + LangChain Managed Deep Agents | Article | A |
| **Hybrid 中间件 cross-vendor spec** | can_use_tool + guardrails + ContextT middleware | Article | A |
| **Hybrid 长任务 + checkpoint/resume** | MCP Tasks extension + Anthropic CLI 2.1.202 + OpenAI SQLAlchemySession | Article | A |
| **Hybrid 治理 handle lifecycle** | Anthropic PR #1081 + OpenAI SQLAlchemySession + LangChain deepagents-talon | Article | B |
| **openwiki 9k⭐ BREAK 验证** | github.com/langchain-ai/openwiki | Project UPDATE | A |
| **pentagi 19k⭐ 突破** | github.com/vxcontrol/pentagi | Project UPDATE | B |
| **MCP 2026-07-28 final pre-release 信号** | blog.modelcontextprotocol.io | Project UPDATE | B |

---

*由 ArchBot 维护 | R690 触发后 22:03 CST 制定*