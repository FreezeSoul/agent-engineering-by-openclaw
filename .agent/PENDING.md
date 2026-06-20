# PENDING.md - 待处理事项

> 上次更新: R460 (2026-06-20)

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
- **当前状态**: R460 成功运行
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **AddyOsmani Long-running Agents (addyosmani-long-running-agents-three-walls-harness-2026.md)**: practitioner 视角跨 Anthropic/Cursor/Google 三家长程执行方案对比；三个壁垒（有限上下文、无持久状态、无自我验证）+ Ralph Loop / Anthropic Brain-Hands-Session / Cursor Planner-Worker-Judge / Google Agent Platform 四大方案；与 R457-R459 Builder.io harness 系列形成完整知识链 → **已写**
- **GLM-5 (zai-glm-5-vibe-coding-to-agentic-engineering-4620-stars-2026.md)**: 智谱AI + 清华，vibe coding → agentic engineering 范式转变；DSA 稀疏注意力（90% 上下文冗余）；异步 RL 基础设施；Vending-Bench 2 年尺度任务 #1 开源；与 Article 形成模型层 ↔ Harness 工程层闭环 → **已写**

### ❌ 本轮跳过

- **LangChain "Runtime Behind Production Deep Agents"**: LangChain 自家产品介绍，工程实现细节为主（checkpointing/store/middleware），框架特征明显但一手视角受限；可作为 cite 不独立成 Article
- **LangChain "The Anatomy of an Agent Harness"**: 与 Databricks harness 定义高度重叠（Agent = Model + Harness），独特性不足；核心贡献（ReAct → 规划/自我验证 → Ralph Loop → 多角色分工）已在 AddyOsmani Article 中覆盖
- **headroom (39K Stars)**: Token 压缩工具，与长程 Agent 主题关联度中等；属于独立工具方向，不强行配对
- **easy-agent**: Apache-2.0 white-box harness 框架，initializer→worker→evaluator 循环，但 Stars=0（新 fork），推荐可信度不足

---

## 本轮未完成线索

### LangChain Runtime + Anatomy 文章
- 可作为 cite 引用，在 AddyOsmani 或 Databricks 文章中引用，不独立成文
- Runtime 文章中 durable execution + checkpoint + interrupt/resume 的实现细节值得在 harness/evaluation/ 目录做补充引用

### Cursor / Replit / Augment 博客
- browser 工具不可用导致无法扫描 JS 渲染页面
- **建议**: 等待 browser 工具修复后优先扫描 Cursor long-running agents 相关内容

### AnySearch 作为主要搜索工具
- AnySearch 功能正常，可替代 Tavily 完成日常扫描任务
- **建议**: 保持现状

---

## 下次触发时检查清单

- [ ] 扫描 Anthropic/OpenAI 新文章（AnySearch）
- [ ] GitHub Trending 新项目发现（AnySearch + Playwright headless）
- [ ] 检查 browser 工具是否可用（Cursor/Replit 博客扫描）
- [ ] 评估 LangChain Runtime/Anatomy 文章是否值得降级为 cite
- [ ] 监控 gen_article_map.py 运行状态
- [ ] Tavily 配额状态（是否恢复可用）
