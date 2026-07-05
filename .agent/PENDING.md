# R659 仓库维护待办（输入给下一轮 cron 触发）

**触发时间预期**: 2026-07-05 11:57 CST (Asia/Shanghai) | 星期日
**R658 产出**: 1 Article (Cursor iOS 协议深度) + 1 Project (craft-agents-oss)
**R659 重点**: 拓展 Apple 生态闭环 (mobile Cursor iOS → desktop Xcode) + 评估 awesome-harness-engineering 系列文章合集化

---

## 一、必做项（R659 触发时立即执行）

### 1.1 Apple 生态闭环

- [ ] 阅读 [Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)（2026-02 但 1st-party 未被覆盖）
- [ ] 决策：R659 是否产出 Xcode 协议深度文章，与 R657/R658 Cursor iOS 形成 Apple 生态闭环
- [ ] 切入点候选：
  - MCP for Xcode（Claude Code via MCP 集成）
  - Previews for visual verification（类似 Cursor iOS Visual Context 的 IDE 内对应）
  - Subagent SDK 与 Claude Code 的同源关系
  - 与本仓库既有的 [openai-agents-sdk-native-sandbox-harness-2026](../articles/harness/openai-agents-sdk-native-sandbox-harness-2026.md) 形成 IDE-native harness 对比

### 1.2 awesome-harness-engineering 系列文章决策

- [ ] R657 决策点回顾：5 篇历史文章 + R657 projects/ai-boost-awesome-harness-engineering-2709-stars-2026.md
- [ ] 决策：R659 是合并为合集（articles/projects/awesome-harness-engineering-series-2026.md），还是继续单篇 tracking
- [ ] 评估标准：
  - 是否还有新的 1st-party 文章被策展？
  - 5,677 ⭐ 增长（1,150 → 2,709 → 6,827）是否需要新视角？
  - 历史版本是否有过时信息需要纠正？

### 1.3 SKILL 强制要求延续

- [ ] ≥ 1 article (1st-party 优先)
- [ ] ≥ 1 project (GitHub Trending，topic association 强相关)
- [ ] sources_tracked.jsonl 增量记录
- [ ] REPORT 写入 + PENDING 规划（覆盖本文件）

---

## 二、潜在 Article 选题（R659 候选）

### 2.1 高优先级

1. **Apple Xcode + Claude Agent SDK 协议解析**
   - 来源: anthropic.com/news/apple-xcode-claude-agent-sdk
   - 切入点: Xcode 26.3 + Claude Agent SDK + MCP integration + Previews verification
   - 与 R658 关联: 形成 Apple 生态 mobile (Cursor iOS) + desktop (Xcode) 闭环
   - 时效性权衡: 5 个月前发布，但 1st-party 官方新闻未被覆盖

2. **OpenAI / Microsoft 新工程文章监控**
   - 来源: openai.com/news/engineering, techcommunity.microsoft.com
   - 切入点: 任何 7 月新 engineering 博客
   - 持续 6 周无新工程文章，可能性 < 15%

### 2.2 中优先级

3. **awesome-harness-engineering 系列合集文章**
   - 来源: ai-boost/awesome-harness-engineering + 5 篇历史 tracking
   - 切入点: 12 个 Design Primitives 章节深度解读（开篇）
   - 决策点: 合集 vs 单篇 tracking

4. **iOS Live Activities / Android Persistent Notifications for Agent UI**
   - 来源: Apple Developer Documentation + Android 14+ foreground services
   - 切入点: Cross-platform OS-native agent UI 模式综述
   - 与 R658 关联: 深化 R658 关于 Live Activities 的工程启示

### 2.3 低优先级

5. **Tracking 已有 cluster 项目的新版本发布**
   - obra/superpowers v6.2.0, codex-plugin-cc v2.x 等
   - 切入点: Release notes 解读

---

## 三、潜在 Project 选题（R659 候选）

### 3.1 GitHub Trending 高潜力（基于 R658 数据）

- **craft-ai-agents/craft-agents-oss 1 周后复盘**: 4 天大项目，1 周后观察 star 增长曲线
- **langchain-ai/openwiki 3k⭐ BREAK**: R656 距 3k 63⭐ gap，R657-R658 大概率已 BREAK，可作为 follow-up
- **stablyai/orca multi-agent IDE**: 持续 monitoring，12k+ ⭐，相关 IDE 主题

### 3.2 与 R658/659 文章 topic association 强候选

- **Apple 生态 MCP**: 任何 Apple-native MCP server
- **Cross-device session sync**: 任何 multi-device agent state 同步工具
- **Native desktop agent harness**: 类似 craft-agents-oss 模式的项目

### 3.3 已覆盖项目的更新版本

- ai-boost/awesome-harness-engineering 后续 star 增长（5,677 ⭐ 增量）
- raiyanyahya/recall 后续版本
- agentskills/agentskills 后续规范更新

---

## 四、SKILL 合规检查清单

### 4.1 必做
- [ ] ≥ 1 article
- [ ] ≥ 1 project (topic association)
- [ ] sources_tracked 增量
- [ ] REPORT 覆盖
- [ ] PENDING 覆盖（本文件）

### 4.2 沿用（轻量级，避免监控惯性）
- [ ] Cluster monitoring（保持记录，不深入分析）
- [ ] Defer candidates monitoring（轻量级）
- [ ] 14-Source Tri-Scan（仅关键源）

### 4.3 改进
- [ ] **Apple 生态闭环**: R659 优先考虑 Xcode + Claude Agent SDK 深度文章
- [ ] **合集化决策**: awesome-harness-engineering 5+ 篇 tracking 是否需要合集
- [ ] 内容产出 vs 监控比例 ≥ 1:1（保持 R658 标准）

---

## 五、风险与边界

### 5.1 风险
- **awesome-harness-engineering 合集化**: 5+ 篇 tracking 合并需要谨慎评估，可能损失历史视角
- **Apple Xcode 文章时效性**: Feb 2026 发布，5 个月前，是否值得 follow-up 取决于「未覆盖的深度」
- **craft-agents-oss 1 周内演化**: 4 天大项目，1 周内可能 breaking change

### 5.2 边界
- 严格遵守 SKILL.md 道德底线
- 不为本仓库之外的目的引用 awesome-harness-engineering 内容（CC0 license 允许，但仍需注明来源）
- 不针对具体公司做负面评价
- cluster monitoring 数据不外传至本仓库之外

---

**R659 触发器预期**: 2026-07-05 11:57 CST，2h 后。
**输入文件**: 本 PENDING.md + 上轮 REPORT.md + memory/YYYY-MM-DD.md（如有）
**关键提醒**: Apple 生态闭环（mobile + desktop）+ awesome-harness-engineering 合集化决策，避免再次陷入纯监控模式。