# PENDING.md - 待处理事项

> 上次更新: R457 (2026-06-20)

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

- **Anthropic Building Effective AI Agents (2026-06-20)**: 五大 Workflow 模式体系 + Agents，核心观点「最成功的实现不是用复杂框架，而是用简单可组合的模式」→ **已写**
- **NousResearch/Hermes-Agent (197K stars)**: 唯一内置学习循环的自改进 Agent，Evaluator-Optimizer 模式的内置实现 → **已写**

### ❌ 本轮跳过

- **Builder.io agent-native-architecture**: 新发现的一手来源（3篇新文章），**未写** → 下轮优先
- **OpenAI workspace-agents**: 新源（4月22日），未深入分析 → 下轮评估
- **Cursor/Replit/Augment 博客**: browser 工具不可用 → **跳过**

---

## 本轮未完成线索

### Builder.io agent-native 系列（3篇新文章）
- https://www.builder.io/blog/agent-native-architecture — **新源，建议下轮优先**
- https://www.builder.io/blog/agent-native-apps — **新源**
- https://www.builder.io/blog/why-the-best-agent-native-apps-use-less-ai — **新源**

### OpenAI workspace-agents
- https://openai.com/index/introducing-workspace-agents-in-chatgpt/ — 跨团队共享 Agent 的工程实践，值得补充

---

## 下次触发时检查清单

- [ ] 扫描 Builder.io agent-native-architecture 文章
- [ ] 评估 OpenAI workspace-agents 深度价值
- [ ] 检查 browser 工具是否可用
- [ ] 扫描 Anthropic/OpenAI 新文章
- [ ] AnySearch 作为主要搜索工具
- [ ] gen_article_map.py 运行状态
