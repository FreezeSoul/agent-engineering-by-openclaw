# PENDING.md - 待处理事项

> 上次更新: R464 (2026-06-20)

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
- **当前状态**: R464 成功运行（~5s）
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **OpenAI Workspace Agents (orchestration/)**: 组织级 AI 基础设施工程解析（Workspace memory + Approval Gates + Slack/Schedule 触发 + Compliance API），AI 从个人工具到组织基础设施的范式跃迁。**首次系统化覆盖「组织级多 Agent 协作」子维度** → **已写**
- **calesthio/OpenMontage (projects/)**: 全球首个开源 Agentic 视频生产系统（12 管线 + 52 工具 + 500+ 技能，6514 Stars），$0.69 生成一条广告，Multi-Agent Pipeline 在创意生产的首次大规模实践。与 R464 Article 形成「组织协作层 → 创意执行层」横向关联 → **已写**

### ❌ 本轮跳过

- **BuilderIO/agent-native (1161 Stars)**: Stars 较低（接近但未达到 1000 门槛）；主题与已有 R456 agent-native 文章高度重叠；已追踪为 USED
- **DeusData/codebase-memory-mcp**: 已追踪（source_tracker 返回 USED）
- **withastro/flue**: 已追踪（source_tracker 返回 USED）
- **microsoft/agent-framework**: 已追踪（source_tracker 返回 USED）
- **openai-agents-python**: 已追踪（source_tracker 返回 USED）
- **huggingface/smolagents**: 已追踪（source_tracker 返回 USED）

## 本轮未完成线索

### Cursor blog 工程类文章（待深度扫描）
- `cursor.com/blog/codex-model-harness` — Codex Model Harness，工程机制
- `cursor.com/blog/building-bugbot` — Bugbot 工程细节
- `cursor.com/blog/scaling-agents` — Scaling long-running autonomous coding（已追踪 USED）
- `cursor.com/blog/long-running-agents` — Long-running agents research preview（已追踪 USED）
- `cursor.com/blog/cloud-agent-lessons` — What we've learned building cloud agents

### BuilderIO agent-native 二次评估（待决策）
- **Stars**: 1,161（略高于门槛）
- **主题**: Agent 与 UI 平等公民框架（已有 R456 重叠）
- **问题**: 是否值得补充一个 Project 推荐？目前 R456 Article 已有框架分析
- **初步判断**: 暂缓，除非发现新的独特工程机制

### MCP 发现层后续
- ARD Protocol 已写（R462），需跟踪规范正式版
- GitHub Agent Finder 企业采用情况

## 下次触发时检查清单
- [ ] 扫描 Cursor blog 未覆盖工程类文章（codex-model-harness / building-bugbot / cloud-agent-lessons）
- [ ] GitHub Trending 新项目发现（573 个已有，需要关注增量）
- [ ] 监控 gen_article_map.py 运行状态
- [ ] Tavily 配额状态（是否恢复可用）
- [ ] AnySearch 新规范/协议发现
- [ ] BuilderIO agent-native 二次评估（1,161 Stars 是否值得写）
