# Paperclip Changelog Watch

> Paperclip 框架动态追踪。重大版本更新记录于此。

---

## 追踪状态

| 项目 | 状态 |
|------|------|
| 追踪频率 | 中频（每次更新检查）|
| 数据来源 | GitHub Releases + 官方博客 |
| 最近检查 | 2026-03-31 |

---

## Release 历史

### v0.x（2026 年活跃开发期）

#### Latest Release（2026-03-27）

**重点更新**：

- **Company Skills Library**：新增公司级 Skills 系统，配合 Skills UI 界面，支持跨所有本地 Adapter（Claude、Codex、Pi、OpenClaw）的 Agent Skill 同步，支持从 GitHub 固定 Skills 并自动检查更新
- **新 Adapter：Cursor、OpenCode、Pi**：Paperclip 现支持 9 种 Agent Adapter
- **Hermes agent adapter**：新增 `hermes_local` Adapter，支持 Hermes CLI 作为 Agent 后端
- **Agent Runs Tab**：Agent 详情页新增独立 Runs Tab，记录每次执行历史
- **Project & Agent Configuration Tabs**：全新 Tab 式配置界面，支持执行工作区策略设置
- **Instructions Tab State Fix**：修复切换 Agent 时 Tab 状态不更新的 Bug

**贡献者**：@aaaaron、@AiMagic5000、@artokun、@cpfarhood、@cschneid、@dalestubblefield、@dotta、@eltociear、@fahmmin、@gsxdsm、@hougangdev、@JasonOA888、@Konan69、@Logesh-waran2003、@mingfang、@MumuTW、@mvanhorn、@numman-ali、@online5880、@RememberV、@richardanaya、@STRML、@tylerwince、@zvictor 等 24+ 贡献者

---

## 关键里程碑

| 日期 | 事件 | 说明 |
|------|------|------|
| 2026-01 | GitHub Stars 突破 10k | 进入主流视野 |
| 2026-03 | Stars 突破 41.6k | 增长迅速 |
| 2026-03-27 | v0.x Latest Release | 新增 Skills Library + 3 个新 Adapter |
| ~2026-Q1 | Clipmart 预告 | 「一键下载并运行整个公司」的功能即将推出 |

---

## 技术栈

| 项目 | 技术 |
|------|------|
| 语言 | TypeScript（34,783 行代码）|
| 许可证 | MIT |
| 运行时 | Node.js 20+ |
| 包管理 | pnpm |
| 前端 | React UI |
| 数据库 | PostgreSQL（嵌入式或自托管）|
| Stars | 41.6k |
| Forks | 6.2k |
| Contributors | 100+ |

---

## 竞品对比

| 框架 | 类型 | Org Chart | Cost Control | Multi-Company | License |
|------|------|-----------|-------------|--------------|---------|
| Paperclip | Company OS | ✅ | ✅ | ✅ | MIT |
| LangGraph | Workflow Framework | ❌ | ❌ | ❌ | MIT |
| CrewAI | Role-Based Team | 有限 | ❌ | ❌ | Apache 2.0 |
| AutoGen | Multi-Agent | ❌ | ❌ | ❌ | MIT |

---

*最后更新：2026-03-31 | 由 AgentKeeper 维护*
