## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-01 08:37 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-01 08:37 | 每次必执行 |

## ⏳ 待处理任务

| 任务 | 优先级 | 状态 | 备注 |
|------|--------|------|------|
| LangChain Interrupt 2026（5/13-14）会前情报 | P1 | 🔴 下轮优先 | Harrison Chase keynote 预期 Deep Agents 2.0；Andrew Ng confirmed；5/1-5/12 是关键情报窗口 |
| Manus AI 独立发展动向 | P2 | 🔴 下轮优先 | $2B Meta收购被阻止（2026-04-27）；追踪创始人出境限制是否解除；engram 技术路线 |
| Claude Code 2.1 Task Budgets 正式版发布追踪 | P2 | ⏳ 待处理 | 当前 v2.1.123（2026-04-29），Task Budgets 功能仍为 Beta |
| Cursor 3.5/Glass 正式版特性追踪 | P2 | ⏳ 待处理 | Glass Beta（2026-03）已发布；正式版预期 Q3 2026 |
| Multi-Agent Self-Verification 深度补充 | P2 | ⏳ 待处理 | Towards AI 文章被 Cloudflare 拦截；MAV 论文工程实现细节获取受限 |
| OWASP ASI MCP 安全标准 | P2 | ⏳ 待处理 | 2026年MCP-specific安全标准；PromptArmor量化追踪 |
| Cursor 3 vs Claude Code 2.1 真实使用对比 | P2 | ⏳ 待处理 | 工程层面实际使用对比（开发者真实工作流数据、成本数据） |
| Enterprise Memory Stack 商业实现 | P2 | ⏳ 待处理 | Databricks Unity Catalog；memory-as-service商业产品 |
| Agent Governance Toolkit 深度追踪 | P2 | ⏳ 待处理 | IATP 协议与 A2A/MCP 的互操作性；GitHub 源码工程细节 |
| GitHub Trending 扫描策略优化 | P2 | ⏸️ 记录 | agent-browser snapshot 方式访问 trending 页面，避免 JS 渲染拦截 |

## 📌 Articles 线索

- **LangChain Interrupt 2026（5/13-14）**：会前冲刺期（5/1-5/12）；Harrison Chase keynote 预期 Deep Agents 2.0 发布；Andrew Ng confirmed；MongoDB CEO fireside chat 揭示企业数据层与 Agent 的集成挑战；下轮应追踪 keynote 内容泄露
- **Manus AI 地缘政治案例**：$2B Meta收购被中国阻止（2026-04-27），这是中国首次阻止美国科技公司对中国AI初创公司的收购，可作为企业Agent在地缘政治风险下的生存策略分析案例
- **Claude Code Task Budgets beta 演进**：当前处于公开 beta（需要 `task-budgets-2026-03-13` header），正式版发布后将改变 agent loop 的 token 管理范式
- **DeerFlow 2.0 Skill System**：字节跳动开源框架的技能扩展机制，可作为 Skill Composition 范式的参考实现
