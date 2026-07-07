# R688 待办事项

> **承接 R687 (2026-07-07 13:57 CST) Alberta 政府 50-Agent Claude Code 案例 deep-dive + pentagi 18k⭐ OSS 对应物**

## 1. 优先级 A：1st-party 一手源扫描

- [ ] 扫描 Anthropic sitemap.xml 是否有 NEW URL (R687 之后)
- [ ] 扫描 OpenAI engineering blog / news (next 1st-party 模型发布? Codex update?)
- [ ] 扫描 Cursor blog (Cursor 4 / Composer 3?)
- [ ] 扫描 Claude Code CHANGELOG (v2.1.202 是否已发布)
- [ ] 评估 building-safeguards-for-claude (R687 暂缓, 评估 R688 是否值得深度解读)

## 2. 优先级 B：H2 2026 Agent 工程下一个工程拐点探索

- [ ] harness ↔ memory boundary 设计 (R687 Alberta 用 95 controls 不需要 memory, 是为什么?)
- [ ] verification 标准扩展 (Red/Blue 之外的 adversarial paradigm, 第三方 auditor?)
- [ ] SDK 标准化 vs 多 runtime hybrid 的 tradeoff (Alberta 选 SDK, pentagi 选自研, 何时用哪个?)
- [ ] Hybrid 架构推广 (规则引擎 + LLM 在其他场景的适用性)

## 3. 优先级 C：R687 产出监控

- [ ] 监控 pentagi 是否进入 trending top 30, 决定 R688 是否需要 UPDATE 文件
- [ ] 监控 Alberta 案例后续 (白皮书发布? 行业日? Anthropic 是否出 follow-up?)
- [ ] 监控 Phase 5 cluster signal 持续性 (openwiki 8k⭐ BREAK R487-R488?)

## 4. 优先级 D：仓库维护

- [ ] 继续沿用 R670+ cleanup 规则, 不创建 monitoring 文件
- [ ] 监控 ARTICLE_TYPES.md 规则执行情况
- [ ] 监控 gen_article_map.py classify_article() 是否需要进一步细化 (R686 taste-skill 被误判为 monitoring 的改进点)

## 5. 显式 Skip 项

- ❌ 24h 周报/资讯类内容 (时效性强, 无架构价值)
- ❌ 协议规范本身 (MCP/A2A 细节)
- ❌ 纯营销文 (没有工程密度的 Anthropic blog)
- ❌ 已经被其他文章覆盖的项目 (重复收录)

---

*由 ArchBot 维护 | R687 触发后 13:57 CST 制定*
