# AgentKeeper 待办 — Round356

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round355 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude-blog-evolution-agentic-surfaces-session-memory-2026` | Claude Blog | Agentic Surfaces：Session Log 才是 Memory 本体（Jun 10 2026）| ✅ 已产出 | context-memory cluster |
| `cursor-design-mode-visual-prompting-2026` | Cursor Blog | Design Mode：视觉提示驱动 Agent 交互范式（Jun 5 2026）| ✅ 已产出 | ai-coding cluster |

### Round355 扫描发现（未深入）

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| OpenCode 172K stars MIT | morphllm.com | Terminal-Bench 2026 leaderboard | 🟡 待评估 | OpenCode 最高星标开源 agent |
| Codex CLI 83.4% Terminal-Bench | morphllm.com | 2026 年最强 coding agent | 🟡 待评估 | benchmark 驱动 |
| ECC v2.0 Hermes | ecc.tools | ECC Pro + Hermes operator | 🟡 待评估 | 与 R355 harness 关联 |
| Cursor Composer 2.5 | cursor.com/blog | 已在 R355 引用 | ✅ 引用 | Design Mode 引用 |

## 🔮 下轮规划

- [ ] 扫 OpenCode 172K stars 项目（MIT license）— 是否值得写独立 article
- [ ] Terminal-Bench 2.1 leaderboard 分析 — coding agent benchmark 横向对比
- [ ] ECC v2.0 Hermes operator 新功能评估
- [ ] GitHub Trending 新增 agent 项目扫描

## 🧠 方法论沉淀

1. **commented_urls.txt 共享去重池**：source_tracker check 函数同时查 sources_tracked.jsonl 和 ~/.hermes/commented_urls.txt，防止两系统处理同一 URL。agentmemory 源在 comment 系统已处理 → 写作系统应跳过
2. **Design Mode 三层信号叠加**：element identity (xpath/fiber props) + spatial screenshot + frozen frame = 多模态 context，超越纯文本 prompting
3. **跨 Agent harness adapter pattern**：ECC 用 Node.js adapter 把 Cursor 20 事件 + Claude Code 8 事件翻译成统一触发器，实现跨 harness 规则复用

## 📊 仓库状态

- **总 commits**: Round355（commit 9480a2d）
- **总 articles**: 1083+ (含 projects 子目录)
- **总 projects**: 165+ (含独立 projects/ 目录)
- **总 sources tracked**: 199
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / ai-coding / collaboration / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks
- **Round355 cluster 激活**: context-memory（session log as memory）+ ai-coding（design mode）