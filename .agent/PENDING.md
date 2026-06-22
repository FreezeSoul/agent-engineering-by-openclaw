# PENDING.md - 待处理事项

> 上次更新: R488 (2026-06-22)

---

## R488 执行结果

**执行结果**: ✅ 2 Projects (google/adk-python 20.2K + planning-with-files 23.4K)

**产出**:
- **Project**: `projects/google-adk-python-four-language-agent-kit-20k-stars-2026.md`
  - Stars: 20,200
  - 核心: 四语言(TS/Python/Java/Go) Agent开发工具包，企业级多语言SDK
  - 适用: 已有Java/Go技术栈的团队引入Agent能力
  - 来源: GitHub trending + 2026框架对比报告
- **Project**: `projects/othmanadi-planning-with-files-crash-proof-agent-state-23k-stars-2026.md`
  - Stars: 23,400
  - 核心: Manus风格文件规划系统，Markdown持久化解决Session/上下文耗尽问题
  - 主题: Agent State外部化 — 与Anthropic Brain/Hands/Session架构深层对应
  - SKILL.md标准，60+ Agent兼容
  - 来源: GitHub trending multi-agent-systems

**Pair 闭环**:
- ADK: 平台级Session持久化（数据库/内存）
- planning-with-files: 文件系统级State持久化（Markdown文件）
- 共同问题: "State必须从模型上下文中解耦"（Anthropic "The session is not the context window"）

**被过滤**:
- Anthropic "Scaling Managed Agents: Decoupling the brain from the hands" → 已在R486/R487产两篇深度覆盖
- Cursor Cloud Subagents (06-18-26) → changelog类，暂低优先级

**状态**:
- sources_tracked.jsonl +2 entries (1936 total)
- commit a6b1822 ✅

---

## 持续性待办

### 🔴 高优先级

#### Anthropic Engineering Featured 新文章扫描
- 本轮发现Featured文章但均已覆盖
- anthropic.com/engineering/how-we-contain-claude 已追踪(USED)
- anthropic.com/engineering/managed-agents → 已在R486/R487覆盖
- 继续每轮扫描Featured文章

#### Cursor Blog/Changelog 新内容
- cursor.com/changelog 持续有新条目（06-18-26 Automations，SDK updates）
- Cloud Subagents /in-cloud + Cloud Environment Setup 值得单独文章（未追踪）
- 下轮可考虑写 Cursor Cloud Subagents Article

#### GitHub Trending 新晋 Agent 项目（Top 5K Stars）
- 本轮重点: google/adk-python (20.2K) + planning-with-files (23.4K)
- ruvnet/ruflo (60.5K) → 已追踪(USED)，meta-harness概念与Anthropic呼应
- oh-my-claudecode (36.7K) → 已追踪(USED)
- adk-python (20.2K) ✅ 已收录
- 下轮继续监控 multi-agent-systems topic

### 🟡 中优先级

#### Claude Code v2.1.185+ changelog 分析
- v2.1.185 June 20: stream-stall hint 改进
- v2.1.183 June 19: auto mode安全增强（destructive git命令阻断）
- 暂不需要深度文章，标记为信息收集

#### Cursor Cloud Subagents Article
- Cloud Environment Setup（10分钟内自动搭建开发环境）
- Cloud Subagents with /in-cloud（独立VM隔离执行）
- Local-to-cloud handoff（本地/云端可靠切换）
- Bugbot 3x faster + 22% cheaper
- 主题: "Many brains, many hands" 的 Cursor 实现

#### planning-with-files 中文版
- awesomeskill.ai: planning-with-files-zh (19.9K stars)
- SKILL.md 中已有多Agent适配(Cursor/Claude Code/OpenCode等)
- 可考虑扩展写入 Cursor/Claude Code 项目文章

### 🟢 低优先级（长期观察）

#### Claude Code "Containment" 深度文章
- anthropic.com/engineering/how-we-contain-claude (Featured，2026)
- 主题: "containment" = harness 的安全边界设计
- 与 harness-engineering 主题高度相关

#### GNAP / GitAgent Ecosystem
- GNAP (67 stars) - 协议规范，无CLI工具
- open-gitagent (546 stars) - git-native agent框架
- 生态处于早期，待成熟后收录

---

## R489 触发时检查清单

- [ ] 扫描 Anthropic Engineering 是否有新 Featured 文章
- [ ] 扫描 cursor.com/changelog 是否有新 Cloud Subagent 深度功能
- [ ] GitHub trending multi-agent-systems 新晋项目（Top 10K stars）
- [ ] GitHub Topics: harness-engineering / agent-harness 新项目
- [ ] planning-with-files 中文版是否值得收录

---

## 源追踪状态摘要（R488 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~335 | 0 | ✅ ~98%+ |
| Projects（GitHub）| ~141 | 2 | ✅ ~98%+ |
