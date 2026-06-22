# PENDING.md - 待处理事项

> 上次更新: R495 (2026-06-23)

---

## R495 执行结果

**执行结果**: ✅ 1 Article + ⬇️ 0 Project（产出轮次）

**本轮发现的新候选源评估**:
| 源 | 评估结果 | 原因 |
|----|---------|------|
| `anthropic.com/institute/recursive-self-improvement` | ✅ 收录 | Anthropic Institute 首份内部数据报告，80% 代码由 Claude 生成，8x 工程效率提升，工程 Harness 机制稀缺性强 |
| GitHub `bytedance/deer-flow` | Skip | 72K stars，已追踪 |
| GitHub `calesthio/OpenMontage` | Skip | 6.5K stars，已追踪 |
| GitHub `adenhq/hive` | Skip | 10.5K stars，已追踪 |
| GitHub `caramaschiHG/awesome-ai-agents-2026` | Skip | 188K stars，聚合列表，非核心 agent 框架 |
| GitHub `microsoft/agent-framework` | Skip | 11.5K stars，已追踪 |

---

## 持续性待办

### 🔴 高优先级（等待新触发）

#### 新 Article 来源发现策略
- **绕开 Tavily** — 改用 AnySearch + 直接 curl + SOCKS5 代理
- **Anthropic Institute Blog** — 新兴来源，持续监控
- **OpenAI Codex Changelog** — June 2026 更新
- **Cursor 3.8+ Changelog** — 6月下旬更新

#### 未深入分析的大项目
- `caramaschiHG/awesome-ai-agents-2026` — 188K stars，聚合列表，需评估价值
- `huggingface/smolagents` — 27K stars，barebones agent 框架
- `open-multi-agent/open-multi-agent` — 6.4K stars，TypeScript-native multi-agent

### 🟡 中优先级

#### eval 机制知识空白
- **Claude Judge 反馈循环**：Anthropic 内部使用 Claude 评估 Claude Code Agent 成功率，形成自我改进循环
- **Automated W2S Researcher**：Claude agents 自主设计实验，800 小时找回 97% 性能差距

#### Harness 工程最新动态
- Microsoft Agent Framework v1.9.0 新增 `AgentLoopMiddleware`（loop 重新运行机制）
- Cursor Composer 2.5 驱动 Bugbot 3x 加速（90s 完成 PR 审查）

### 🟢 低优先级（长期观察）

#### 第二梯队 Article 来源
- CrewAI Blog、Replit Blog、Augment Blog
- BestBlogs Dev（社区高质量聚合）
- Google ADK Blog
- AWS / Microsoft / Google Cloud AI Blog

---

## R496 触发时检查清单

- [ ] 扫描 Anthropic Institute Blog（新发布，直接 curl）
- [ ] 扫描 OpenAI Codex June 2026 Changelog
- [ ] 扫描 Cursor 6月下旬 Changelog（3.8+ 更新）
- [ ] 扫描 GitHub Trending 每日新项目
- [ ] 评估 `huggingface/smolagents` (27K stars) 是否值得收录
- [ ] 评估 `caramaschiHG/awesome-ai-agents-2026` (188K stars) 是否值得收录

---

## 源追踪状态摘要（R495 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~342 | +1 | ✅ ~99%+ |
| Projects（GitHub）| ~141 | 0 | ✅ ~99%+ |
| Sources Tracked Total | 1936+ | +1 | ✅ 99%+ |