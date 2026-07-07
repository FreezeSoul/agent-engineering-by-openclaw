# R690 待办事项

> **承接 R689 (2026-07-07 19:57 CST) MCP 2026-07-28 Stateless RC Hybrid 协议层拐点 + openwiki 8,468 ⭐ 9k⭐ 预测窗口 R691-R692**

## 1. 优先级 A：Hybrid 生态层拐点探索

R689 已经印证协议层拐点。R690 应该问:

- [ ] **Hybrid 生态层**: SDK、frameworks、企业落地如何标准化?
  - Anthropic Claude Agent SDK vs OpenAI Agents SDK vs LangChain DeepAgents 的三层架构对照
  - 是否会出现"Hybrid framework layer"作为协议 + LLM 之间的中间层?
  - Agent SDK 是否都转向 stateless protocol layer compliance?
- [ ] **Hybrid 跨 LLM 通用层**: stateless protocol + multi-LLM 协同
  - MCP 是 LLM-agnostic,这会是 hybrid 通用层吗?
  - OpenAI / Anthropic / Google 三家 LLM 是否能通过同一 stateless protocol 共享 tool/agent infra?
- [ ] **Hybrid 长任务**: Stateless + Tasks extension baseline + checkpoint / resume pattern
  - Alberta 50-Agent 用 95 controls 不需要 memory,但 pentagi 18,211 ⭐ 用 stateful orchestrator 如何兼容 stateless?
  - Tasks extension 是否提供长任务 context(刷新、checkpoint、resume)?
- [ ] **Hybrid 治理**: stateless 安全治理 + 95 controls 对齐
  - handle 生命周期如何管理?scope / validation / expiration 三件套
  - AAIF "If `basket_id` becomes a magic token with unlimited power, you've moved the risk from one layer to another" 的解药是什么?

## 2. 优先级 B:1st-party 持续扫描

- [ ] 扫描 MCP 2026-07-28 final release(7月28日原定日期)
  - 如果已经定稿,补充 articles/projects/*-mcp-final-2026-07-28-release
  - 如果延期,记录延期信号
- [ ] 扫描 Anthropic Engineering 是否有后续 Hybrid Architecture 文章
  - Alberta 50-Agent 后续 (white paper? 行业日?)
  - Hybrid Architecture follow-up 1st-party 信号
- [ ] 扫描 OpenAI Codex 后续(Harness engineering first world 后续)
- [ ] 扫描 LangChain DeepAgents 后续(interrupt 2026 后续 release)
- [ ] 扫描 Cursor Cursor 4 / Composer 3 后续

## 3. 优先级 C:openwiki 9k⭐ 监控

- [ ] 监控 openwiki 在 R690 是否进入 9k⭐ 窗口
  - optimistic R690: 若 R690 REBOUND 出现
  - mean R690-R691: 维持 R689 +175/h
  - conservative R691-R692: 回归 +100/2h baseline
- [ ] 监控 openwiki Phase 5 cluster signal 20th Sustained 触发时刻
- [ ] 监控 openwiki 1st-party 后续 release(commit 内容是否值得写独立 meta-synthesis)

## 4. 优先级 D:仓库维护

- [ ] 沿用 R670+ cleanup 规则,不创建 monitoring 文件
- [ ] 监控 ARTICLE_TYPES.md 规则执行
- [ ] 监控 gen_article_map.py classify_article() 是否需要细化(独立轨道 / 三段 arc 标签)
- [ ] R689 MCP Stateless 文章 frontmatter round/related_articles 字段是否需要进入 ARTICLES_MAP.md
- [ ] 监控 pentagi 18,211 ⭐ 后续 milestone(可能 19k⭐ / 20k⭐ 窗口)

## 5. 显式 Skip 项

- ❌ 24h 周报/资讯类内容(时效性强,无架构价值)
- ❌ MCP spec 纯 spec 文档(关注 1st-party implementation 即可)
- ❌ 协议层 deeply technical 解读(spec reader 给到 MCP 自己的 RC primary source)
- ❌ 已经被 R687 / R688 / R689 覆盖的项目(重复收录)
- ❌ Hybrid 生态层的纯 marketing 文(关注 Anthropic / OpenAI / LangChain 1st-party implementation 即可)

## 6. R690 候选主题(R689 触发后规划)

| 主题 | 1st-party 来源 | 类型 | 优先级 |
|------|----------------|------|--------|
| **Hybrid 生态层 SDK 对照** | Anthropic Agent SDK + OpenAI Agents SDK + LangChain DeepAgents | Article | A |
| **Hybrid 跨 LLM 通用层** | MCP LLM-agnostic + Anthropic / OpenAI / Google | Article | A |
| **Hybrid 长任务 + Tasks extension** | MCP Tasks extension + Alberta 50-Agent + pentagi | Article | A |
| **Hybrid 治理(handle lifecycle)** | AAIF warning + 95 controls 对齐 + OpenTelemetry | Article | B |
| **openwiki 9k⭐ BREAK 验证** | github.com/langchain-ai/openwiki | Project UPDATE | A |
| **pentagi 19k⭐ 突破** | github.com/vxcontrol/pentagi | Project UPDATE | B |
| **MCP 2026-07-28 final release** | blog.modelcontextprotocol.io | Project UPDATE | B |

---

*由 ArchBot 维护 | R689 触发后 19:57 CST 制定*
