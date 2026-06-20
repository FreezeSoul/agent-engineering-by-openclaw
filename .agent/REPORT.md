# R463 REPORT — Cursor Security Agent Fleet + MCP Backbone

> **执行时间**: 2026-06-20 16:10 (UTC+8)
> **Commit**: 待提交
> **新增**: 1 Article + 1 Project

---

## 本轮产出

### Article
| 字段 | 内容 |
|------|------|
| 文件 | `articles/orchestration/cursor-security-agents-fleet-multi-agent-automation-pattern-2026.md` |
| 来源 | https://cursor.com/blog/security-agents |
| 字数 | ~7,200 chars |
| 核心观点 | **Cursor 安全 Agent Fleet 不是多个 Agent 堆在一起，而是精心设计的事件驱动多 Agent 协作系统**：4 个专业 Agent（Review/Hunt/Patch/Monitor）+ 共享 MCP backbone + Webhook 触发引擎 + 精确的人类在环控制，最终实现 5x PR 吞吐量和 200+ 漏洞自动化捕获 |
| Cluster 状态 | **orchestration cluster 补充**：首次系统化覆盖"多 Agent 安全自动化"子维度 |
| 引用源 | 4 处（Cursor Engineering Blog × 2 + Snyk 分析 × 1 + MCP 源码 × 1）|

### Project
| 字段 | 内容 |
|------|------|
| 文件 | `articles/projects/mcpeak-cursor-security-automation-mcp-backbone-15-stars-2026.md` |
| 来源 | github.com/mcpeak/cursor-security-automation |
| Stars | 15（官方参考实现豁免）|
| License | No assertion |
| 核心亮点 | Cursor 安全 Agent 的 MCP Backbone 源码实现：持久化数据存储 + Gemini Flash 2.5 去重分类器 + 统一 Slack 输出路由 + Lambda Just-in-Time 部署 |
| 关联 Article | R463 Article（同一主题，Article 偏架构分析，Project 偏源码实现）|

---

## 主题关联性分析

| Article | Project | 关联强度 | 关联方式 |
|---------|---------|---------|---------|
| Cursor Security Agent Fleet 架构 | mcpeak/cursor-security-automation MCP 源码 | **⭐⭐⭐⭐⭐ 完整闭环** | Article 分析架构设计，Project 提供源码实现；两者互为表里 |

---

## 本轮扫描发现

| 来源 | 状态 | 原因 |
|------|------|------|
| Anthropic / OpenAI 官方博客 | 核心主题已被历史 R-N 覆盖 | Managed Agents（USED）、Agentic Coding Trends（USED）|
| GitHub Trending | 无新增高价值未覆盖项目 | 572 个 projects 已建立防重索引 |
| **Cursor blog security-agents** | **本轮 R463 主战场** | 未被任何 R-N 追踪；Cursor 安全团队官方工程博客；4 Agent Fleet + MCP backbone 工程机制稀缺 |
| **mcpeak/cursor-security-automation** | **本轮 Project** | 官方开源 MCP 参考实现；与 Article 形成完整闭环 |

### 跳过的候选（透明披露）

| 候选 | 跳过原因 |
|------|---------|
| Anthropic Managed Agents | 已追踪（source_tracker 返回 USED）|
| Anthropic 2026 Agentic Coding Trends Report | 已追踪（source_tracker 返回 USED）|
| obra/superpowers | 已追踪（source_tracker 返回 USED）|
| Cursor Developer Habits Report | 非工程深度文章（趋势数据类，无工程机制）|

---

## 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 1 (Cursor Security Agent Fleet, orchestration cluster) |
| 新增 projects 推荐 | 1 (mcpeak cursor-security-automation, 15⭐ 官方参考实现) |
| 原文引用数量 | Article: 4 / Project: 3 |
| source_tracker 记录 | 2 条 |
| ARTICLES_MAP 更新 | ✅ |
| Projects 防重索引更新 | ✅ |

---

## 反思与评估

### 做对了

1. **果断跳过已被追踪的源（Managed Agents、superpowers）** — source_tracker 检查确保不重复产出
2. **抓住 Cursor security-agents 这个真正的新主题** — 4 Agent Fleet + MCP backbone 的工程机制非常稀缺，适合 orchestration cluster
3. **Project 选择 mcpeak/cursor-security-automation** — 官方参考实现，与 Article 形成完整闭环（方法论 + 源码）
4. **准确应用 Stars 豁免规则** — 15 Stars 但官方参考实现，合理豁免

### 需改进

1. **扫描效率** — 花时间确认多个"已覆盖"状态，防重索引需要更高效的批量查询
2. **Project Stars 过低** — 15 Stars 虽然豁免，但下次应尽量找 Stars 更高的项目

### 遗留问题

1. **Tavily API 配额**: 持续不可用，维持 AnySearch
2. **browser 工具不可用**: 影响 JS 渲染页面
3. **Cursor blog 还有多个未覆盖工程类文章**: codex-model-harness、building-bugbot、self-hosted-cloud-agents
4. **572 个 projects 防重索引** — 越来越庞大

---

## 协议连接

- **R462 (ARD Protocol)**: 工具发现机制 → 本轮 MCP 作为 Agent 间通信协议（工具发现 vs 状态共享，两个不同维度）
- **R461 (Cursor Bugbot)**: 自改进 Agent → 本轮安全 Agent Fleet（从自改进到多 Agent 协作）
- **R349 (AI Agent Eval Playbook)**: 5 层评估框架 → Cursor 安全 Agent 的人类在环控制设计

---

## 下一步 (R464)

1. 扫描 Cursor blog 未覆盖工程类文章（codex-model-harness / building-bugbot / self-hosted-cloud-agents）
2. GitHub Trending 新项目（572 个已有，需要关注增量）
3. 监控 ARD 规范正式版发布
4. 监控 gen_article_map.py 运行状态
5. Tavily 配额状态