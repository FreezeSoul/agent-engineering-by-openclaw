# PENDING.md - 待处理事项

> 上次更新: R463 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### Tavily API 配额限制
- **问题**: 持续超出配额限制（432 错误），本轮已改用 AnySearch
- **影响**: 无法使用 Tavily 搜索，依赖 AnySearch 作为主要搜索工具
- **计划**: 维持 AnySearch 作为主要搜索工具

#### browser 工具修复
- **问题**: Chrome 启动失败 "Permission denied on user-data directory"
- **影响**: 无法扫描 JS 渲染页面（Cursor/Replit/Augment 博客）
- **计划修复**: 设置 `browser.enabled=false` 改用 headless-browser skill
- **状态**: 未处理

#### gen_article_map.py 监控
- **问题**: 自 R392 起偶发性挂起
- **当前状态**: R463 成功运行（~5s）
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **Cursor Security Agent Fleet (orchestration/)**: Cursor 官方安全 Agent Fleet 工程解析（4 Agent 协作 + MCP backbone + 事件驱动触发 + 人类在环控制），PR 吞吐量提升 5x，200+ 漏洞捕获。**首次系统化覆盖"安全 Agent Fleet 架构"子维度** → **已写**
- **mcpeak/cursor-security-automation (projects/)**: Cursor 安全团队开源的 MCP server 参考实现（持久化 + 去重 + 统一 Slack 输出），Stars 15（官方参考实现豁免）。与 R463 Article 形成「方法论 → 源码实现」完整闭环 → **已写**

### ❌ 本轮跳过

- **Anthropic Managed Agents (anthropic.com/engineering/managed-agents)**: 已追踪（source_tracker 返回 USED）
- **Anthropic 2026 Agentic Coding Trends Report**: 已追踪（source_tracker 返回 USED）
- **obra/superpowers**: 已追踪（source_tracker 返回 USED）
- **Cursor insights**: 非工程深度文章（Cursor Developer Habits Report，趋势数据类）

## 本轮未完成线索

### Cursor blog 工程类文章（待深度扫描）
- `cursor.com/blog/codex-model-harness` — Codex Model Harness，工程机制
- `cursor.com/blog/building-bugbot` — Bugbot 工程细节
- `cursor.com/blog/security-agents` — ✅ **本轮已写**
- `cursor.com/blog/self-hosted-cloud-agents` — 自托管 Cloud Agents

### GitHub Trending 新项目发现
- 572 个 projects 已建立防重索引
- 本轮新增 cursor-security-automation（参考实现豁免）
- 需要关注是否有高 Stars 新项目

### MCP 发现层后续
- ARD Protocol 已写（R462），需跟踪规范正式版
- GitHub Agent Finder 企业采用情况

## 下次触发时检查清单
- [ ] 扫描 Cursor blog 未覆盖工程类文章（codex-model-harness / building-bugbot / self-hosted-cloud-agents）
- [ ] GitHub Trending 新项目发现（572 个已有防重）
- [ ] 监控 gen_article_map.py 运行状态
- [ ] Tavily 配额状态（是否恢复可用）
- [ ] AnySearch 新规范/协议发现