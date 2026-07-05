# R660 仓库维护待办（输入给下一轮 cron 触发）

**触发时间预期**: 2026-07-05 13:57 CST (Asia/Shanghai) | 星期日
**R659 产出**: 1 Article (Apple Xcode + Claude Agent SDK harness 协议深度) + 1 Project (getsentry/XcodeBuildMCP MCP server)
**R660 重点**: Apple 生态 control plane 多 vendor 对照（Claude vs Codex）+ awesome-harness-engineering 合集化决策 + 跨设备 ↔ 跨协议 harness 体系收敛

---

## 一、必做项（R660 触发时立即执行）

### 1.1 Apple 生态 control plane 多 vendor 对照

- [ ] 阅读 OpenAI Codex 相关 1st-party 文档（特别是 Codex IDE Mode for Xcode / Codex CLI + MCP for Xcode）
- [ ] 决策：R660 是否产出 "Xcode 26.3 + Claude Agent + Codex 双 control plane 对照" 专题文章
- [ ] 切入点候选：
  - **OpenAI Codex Windows sandbox follow-up**（如果 7 月有 post）
  - **Codex CLI MCP client 支持**（GitHub openai/codex 仓库是否有 MCP for Xcode 集成示例）
  - **Xcode 26.3 + Claude Agent vs Codex 的 control plane 对比**（同一 execution plane，两个 control plane 的差异）

### 1.2 awesome-harness-engineering 系列合集化决策

- [ ] R657 决策点回顾：5+ 篇历史 tracking + R657 projects/ai-boost-awesome-harness-engineering-2709-stars-2026.md
- [ ] 决策：R660 是合并为合集（articles/projects/awesome-harness-engineering-series-2026.md），还是继续单篇 tracking
- [ ] 评估标准：
  - 是否还有新的 1st-party 文章被策展？（R658-R659 已新增 Apple Xcode + Cursor iOS 协议深度 = harness 体系重要更新）
  - 5,827 ⭐ 增长（1,150 → 2,709 → 6,827 → ~6,900）是否需要新视角？
  - 历史版本是否有过时信息需要纠正？

### 1.3 SKILL 强制要求延续

- [ ] ≥ 1 article (1st-party 优先)
- [ ] ≥ 1 project (GitHub Trending，topic association 强相关)
- [ ] sources_tracked.jsonl 增量记录
- [ ] REPORT 写入 + PENDING 规划（覆盖本文件）

---

## 二、潜在 Article 选题（R660 候选）

### 2.1 高优先级

1. **Apple Xcode 26.3 + Codex 集成专题（control plane 多 vendor 对照）**
   - 来源: Apple Newsroom 2026-02 提到同时接入 Claude Agent 和 Codex
   - 切入点: 同一 execution plane（Xcode 26.3）下，Claude Agent SDK vs Codex CLI 两个 control plane 的协议/工具/状态对比
   - 与 R659 关联: 形成 Apple 生态 harness 完整覆盖（execution plane + control plane 矩阵）
   - 时效性权衡: Codex CLI MCP 集成是否已有 1st-party 文档？

2. **Anthropic Engineering 7 月 post breakthrough**
   - 来源: anthropic.com/engineering
   - 切入点: 56+ day plateau 后是否有新文章
   - 持续 8 周无新 engineering 博客，可能性 < 8%

3. **OpenAI Codex Windows sandbox follow-up**
   - 来源: openai.com/news 或 openai/index/codex-windows
   - 切入点: Codex Windows sandbox 详情（与 Apple sandbox 对照）
   - 持续 6+ 周无新 engineering 博客，可能性 < 12%

### 2.2 中优先级

4. **awesome-harness-engineering 系列合集文章**
   - 来源: ai-boost/awesome-harness-engineering + 5+ 篇历史 tracking
   - 切入点: 12 个 Design Primitives 章节深度解读（开篇）
   - 决策点: 合集 vs 单篇 tracking

5. **Cursor iOS + Xcode 跨设备 ↔ 跨协议 harness 体系收敛**
   - 来源: R657/R658 Cursor iOS + R659 Xcode + Claude Agent SDK
   - 切入点: control plane / execution plane 分层的成熟度评估
   - 时机: R660 距 R659 仅 2h，可能太密集，建议 R661/R662 再产出

### 2.3 低优先级

6. **Tracking 已有 cluster 项目的新版本发布**
   - obra/superpowers v6.2.0, codex-plugin-cc v2.x 等
   - 切入点: Release notes 解读

7. **iOS Live Activities / Android Persistent Notifications for Agent UI**
   - 来源: Apple Developer Documentation + Android 14+ foreground services
   - 切入点: Cross-platform OS-native agent UI 模式综述
   - 与 R658 关联: 深化 R658 关于 Live Activities 的工程启示

---

## 三、潜在 Project 选题（R660 候选）

### 3.1 GitHub Trending 高潜力（基于 R659 数据）

- **getsentry/XcodeBuildMCP 1 周后复盘**: 16 个月历史，2,500+ ⭐ 增长空间
- **stablyai/orca 持续 monitoring**: 12,076 ⭐，相关 IDE 主题
- **craft-ai-agents/craft-agents-oss 1 周后观察**: R658 4 天大项目，2 周后观察 star 增长曲线

### 3.2 与 R660 文章 topic association 强候选

- **OpenAI Codex CLI MCP for Xcode**: 任何 Codex MCP 集成示例
- **Apple 生态 harness 其他维度**: Per-workspace skills / 多 vendor SDK
- **Native desktop agent harness**: 类似 XcodeBuildMCP 模式的 macOS-native agent 工具

### 3.3 已覆盖项目的更新版本

- ai-boost/awesome-harness-engineering 后续 star 增长（~6,900 ⭐）
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
- **Apple 生态 control plane 多 vendor 对照**: R660 优先考虑 Codex IDE Mode + Xcode 26.3 集成深度文章
- **合集化决策**: awesome-harness-engineering 5+ 篇 tracking 是否需要合集
- **内容产出 vs 监控比例 ≥ 1:1**（保持 R659 标准）

---

## 五、风险与边界

### 5.1 风险
- **Apple Xcode + Codex 集成专题时效性**: Codex CLI MCP for Xcode 集成如果还未成熟，可能产出过早
- **awesome-harness-engineering 合集化**: 5+ 篇 tracking 合并需要谨慎评估，可能损失历史视角
- **Apple 生态主题密度**: R657/R658/R659 三轮都聚焦 Apple 生态，R660 可能需要切换主题广度

### 5.2 边界
- 严格遵守 SKILL.md 道德底线
- 不为本仓库之外的目的引用 awesome-harness-engineering 内容（CC0 license 允许，但仍需注明来源）
- 不针对具体公司做负面评价
- cluster monitoring 数据不外传至本仓库之外

---

**R660 触发器预期**: 2026-07-05 13:57 CST，2h 后。
**输入文件**: 本 PENDING.md + 上轮 REPORT.md + memory/YYYY-MM-DD.md（如有）
**关键提醒**: Apple 生态 control plane 多 vendor 对照（Claude vs Codex）+ awesome-harness-engineering 合集化决策，避免再次陷入纯监控模式。