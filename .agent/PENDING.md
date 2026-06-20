# PENDING.md - 待处理事项

> 上次更新: R462 (2026-06-20)

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
- **当前状态**: R462 成功运行（~5s）
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **ARD Protocol (agentic-resource-discovery-ard-mcp-tool-discovery-2026.md)**: **tool-use cluster 工具发现问题补充**。Microsoft+Google+HuggingFace+GoDaddy 联合推出；GitHub Agent Finder 首个企业实现（2026-06-17）；MCP 的发现层；"计划驱动、按需发现"范式转变。**首次系统化覆盖"Agent 工具发现问题"子维度** → **已写**
- **VILA-Lab/Dive-into-Claude-Code (vila-lab-dive-into-claude-code-academic-analysis-1643-stars-2026.md)**: 1,643⭐；学术源码级 Claude Code 系统分析（v2.1.88）；实证验证社区架构猜测；Skill 格式可加载进 Claude Code；为 Dynamic Workflows 提供前状态参考。4-way SPM 强关联 R462 Article → **已写**

### ❌ 本轮跳过

- **Claude Opus 4.8 research page**: Anthropic research 页面而非 engineering blog；动态工作流已在 R461 写过
- **Cursor 3 (cursor.com/blog/cursor-3)**: 已在 articles/ai-coding/cursor-3-multitask-worktrees-multi-root-workspaces-2026.md
- **Dynamic Workflows (claude.com/blog/a-harness-for-every-task)**: 已在 articles/harness/ 和 articles/orchestration/ 多个 R-N 覆盖
- **GenericAgent**: 已在 sources_tracked.jsonl（lsdefine-genericagent self-evolving skill tree）
- **Claude Enterprise blog posts**: Survey 类内容，非工程机制深度文章
- **Dynamic Workflows article**: 已在 articles/harness/claude-code-dynamic-workflows-script-based-orchestration-2026.md（R461 前身版本），本轮发现重复后立即回退

## 本轮未完成线索

### ARD 规范后续跟踪
- **ARD Spec v0.9 → v1.0**: 规范目前是 Draft，需要跟踪正式版发布
- **GitHub Agent Finder 扩展**: 关注更多 AI 客户端采用 ARD 规范
- **Private registry 实际部署案例**: 企业私有注册表的落地实践

### 工具发现问题展开
- **MCP registry 项目**: 是否有开源的 MCP 服务注册表实现
- **ARD 规范的竞品**: 除了 ARD，是否有其他工具发现规范（如 AWS Bedrock Agent Discovery）

### Cursor blog 60 个 untracked 主题
- 大部分为 product/pricing/team 营销页
- 工程类有 5-6 个 (agent-computer-use, agent-web, self-hosted-cloud-agents, marketplace, plan-mode, security-agents, codex-model-harness, building-bugbot)
- 建议 R463+ 重点扫 security-agents + codex-model-harness + building-bugbot

### GitHub Trending 监控
- 569 个 projects 已建立防重索引
- 新增项目需要更高门槛才能发现（需要关联 Article 主题）
- ARD 规范可能带来新的 MCP/工具发现类项目机会

## 下次触发时检查清单
- [ ] 扫描 ARD 规范是否有更新（v0.9 → ?）
- [ ] 扫描 Cursor blog (优先 security-agents / codex-model-harness / building-bugbot 深度)
- [ ] GitHub Trending 新项目发现 (工具发现 / MCP 相关主题)
- [ ] 监控 gen_article_map.py 运行状态
- [ ] Tavily 配额状态（是否恢复可用）
- [ ] AnySearch 新规范/协议发现

