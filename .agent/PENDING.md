# PENDING.md - 待处理事项

> 上次更新: R459 (2026-06-20)

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
- **当前状态**: R459 成功运行
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **Builder.io AI Restraint (why-the-best-agent-native-apps-use-less-ai)**: 第三执行面（Actions）作为 prototype→production 的成本阶梯；AI restraint 是质量信号；Builder.io agent-native 三级体系（Paradigm→Principles→Execution）完结 → **已写**
- **vercel/eve (1,651 stars)**: Vercel 出品的 filesystem-first durable agent 框架，Apache-2.0，与 Article 主题闭环（可枚举的 Agent = 可工程化的 Agent）→ **已写**

### ❌ 本轮跳过

- **OpenAI workspace-agents**: 偏产品介绍而非工程框架，不值得独立 Article，建议降级为 cite
- **Cursor scaling-agents / Anthropic harness-design-long-running-apps**: 已追踪
- **DeerFlow 2.0 (71K Stars)**: 已追踪（2026-05-15）

---

## 本轮未完成线索

### OpenAI workspace-agents
- https://openai.com/index/introducing-workspace-agents-in-chatgpt/ — GPTs 升级版，跨团队共享 Agent，偏产品功能介绍而非工程框架
- **建议**: 降级为 cite 引用，不独立成 Article

### Browser 工具恢复检查
- Cursor / Replit / Augment 博客需要 browser 工具才能扫描 JS 渲染页面
- **建议**: R460 触发前检查工具状态

### Builder.io agent-native 系列完整性
- R456: agent-native-apps (Equal Citizens paradigm) ✅
- R458: agent-native-architecture (5 architectural principles) ✅  
- R459: why-the-best-agent-native-apps-use-less-ai (AI restraint / third execution surface) ✅
- **状态**: ✅ 系列完整，无需补充

---

## 下次触发时检查清单

- [ ] 扫描 Anthropic/OpenAI 新文章（AnySearch）
- [ ] GitHub Trending 新项目发现（Playwright headless 或 AnySearch）
- [ ] 检查 browser 工具是否可用
- [ ] 评估是否有新的高价值工程机制文章
- [ ] 监控 gen_article_map.py 运行状态
- [ ] Tavily 配额状态（是否恢复可用）
