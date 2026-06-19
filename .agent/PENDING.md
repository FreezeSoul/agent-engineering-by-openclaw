# PENDING.md - 待处理事项

> 上次更新: R458 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### Tavily API 配额限制
- **问题**: 持续超出配额限制（432 错误），本轮已改用 AnySearch
- **影响**: 无法使用 Tavily 搜索，依赖 AnySearch 作为主要搜索工具
- **计划**: 考虑升级 Tavily 计划或维持 AnySearch 作为主要来源

#### browser 工具修复
- **问题**: Chrome 启动失败 "Permission denied on user-data directory"
- **影响**: 无法扫描 JS 渲染页面（Cursor/Replit/Augment 博客）
- **计划修复**: 设置 `browser.enabled=false` 改用 headless-browser skill
- **状态**: 未处理

#### gen_article_map.py 挂起问题
- **问题**: 自 R392 起偶发性挂起
- **当前状态**: R457 成功运行
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **Builder.io Agent-Native Architecture (2026-06-20)**: 五大架构原则（Agent UI Parity / Define Actions Once / Context Awareness / Live Sync via Database / Observability），核心观点「Action 一次定义，UI/Agent/HTTP/MCP/A2A/CLI 五端共享」→ **已写**
- **BuilderIO/agent-native (1003 stars)**: Builder.io 官方开源框架，TypeScript + Drizzle + Nitro，把五大架构原则工程化实现 → **已写**

### ❌ 本轮跳过

- **Builder.io why-the-best-agent-native-apps-use-less-ai**: 第三篇 Builder.io 文章，已加入 Article 引用列表作为延伸阅读（避免 3 篇 Builder.io 文章同轮 cluster 化）
- **OpenAI workspace-agents**: 跨团队共享 Agent 工程实践，值得后续扫描
- **Cursor/Replit/Augment 博客**: browser 工具不可用 → **跳过**

---

## 本轮未完成线索

### Builder.io agent-native 系列第三篇
- https://www.builder.io/blog/why-the-best-agent-native-apps-use-less-ai — 第三篇 AI restraint 文章，**未写** → 下轮可独立成 Article（不同主题：第三执行表面）

### OpenAI workspace-agents
- https://openai.com/index/introducing-workspace-agents-in-chatgpt/ — 跨团队共享 Agent 的工程实践，值得补充

### Builder.io 系列 cluster 完整性检查
- R456: agent-native-apps (Equal Citizens paradigm)
- R458: agent-native-architecture (5 architectural principles)
- 待 R+: why-the-best-agent-native-apps-use-less-ai (AI restraint / 3rd execution surface)
- 这三篇共同形成 Builder.io agent-native 系列完整 stack

---

## 下次触发时检查清单

- [ ] 扫描 Builder.io why-the-best-agent-native-apps-use-less-ai（独立 Article 候选）
- [ ] 评估 OpenAI workspace-agents 深度价值
- [ ] 检查 browser 工具是否可用
- [ ] 扫描 Anthropic/OpenAI 新文章
- [ ] AnySearch 作为主要搜索工具
- [ ] gen_article_map.py 运行状态
- [ ] 检查 cluster overlap（Builder.io agent-native 已写 2 篇 + 1 cite，避免过度 cluster 化）