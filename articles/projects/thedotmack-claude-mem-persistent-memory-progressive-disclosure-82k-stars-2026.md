# thedotmack/claude-mem：持久化记忆的 OpenClaw 直装插件

**Stars**: 82,234⭐ | **License**: Apache-2.0 | **Topics**: `ai`, `ai-agents`, `ai-memory`, `anthropic`, `claude`, `claude-agent-sdk`, `claude-agents`, `claude-code`, `claude-code-plugin`, `claude-skills`, `long-term-memory`, `mem0`, `memory-engine`, `openmemory`, `rag`, `sqlite`, `supermemory`

**GitHub**: https://github.com/thedotmack/claude-mem
**Docs**: https://docs.claude-mem.ai/
**集成页**: https://docs.claude-mem.ai/openclaw-integration

**Pair 关联**: `articles/context-memory/anthropic-context-engineering-triple-layer-long-horizon-2026.md`（Path C：4 层全中 = ⭐⭐⭐⭐⭐）

---

## 核心命题

`claude-mem` 把 Anthropic 在「Effective context engineering for AI agents」中提出的 **Compaction / Structured Note-taking / Sub-agent Architectures** 三层范式，做成了一个**生产级、可即装即用、跨 7 个 Agent CLI 兼容**的持久化记忆插件。它在仓库自我定位里直接说：「**Persistent Context Across Sessions for Every Agent**」——这不是另一个 dev 工具，而是 Anthropic 上下文工程范式第一次有了一个被 82K 工程师用脚投票选出来的「参考实现」。

四组核心机制：

1. **Observation Capture（自动观察）**—— Hooks 在 session 期间捕获每条 tool use 事件，写入本地 SQLite（ChromaDB 向量索引 + 时间序列）
2. **AI Compression Pipeline**——用 AI 模型对原始 observation 做摘要压缩，生成多层级 token-cost-aware 的 memory representation
3. **Progressive Disclosure Retrieval**——按需分层回注上下文，新 session 启动时**自动注入**历史 relevant context
4. **Cross-IDE Compatibility**——同一份安装同时支持 Claude Code / Gemini CLI / OpenCode / Codex / Hermes / Copilot / OpenClaw

## 为什么值得关注

### 1. ⭐⭐⭐⭐⭐ SPM 字面级对位 Anthropic Context Engineering Article

`articles/context-memory/anthropic-context-engineering-triple-layer-long-horizon-2026.md` 提炼了 Anthropic 文章的三大支柱：**Compaction**、**Structured Note-taking**、**Sub-agent Architectures**。claude-mem 的三组核心机制——AI Compression Pipeline / Observation Capture (SQLite) / Skill-Based mem-search sub-tool——**字面级 1:1 对位**。Anthropic 文章作为机制层（理论范式），claude-mem 作为生产实现层（工程落地），闭环强度 ⭐⭐⭐⭐⭐。

| Anthropic Context Engineering 范式 | claude-mem 工程实现 |
|-----------------------------------|---------------------|
| Compaction（上下文压缩） | AI Compression Pipeline（每次 session 结束自动 compress）|
| Structured Note-taking | SQLite + ChromaDB 双层存储（结构化元数据 + 向量）|
| Sub-agent Architectures | mem-search skill（按 sub-tool 形式暴露给主 Agent）|
| Progressive Disclosure 原则 | 三层 token-cost-aware retrieval（Discovery → Activation → Execution）|

### 2. ⭐⭐⭐⭐⭐ OpenClaw 直接兼容 = 决定性 tiebreaker

README 显式包含 "🦞 OpenClaw Gateway" 安装段：

```bash
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

并提供完整 OpenClaw 集成文档（https://docs.claude-mem.ai/openclaw-integration），覆盖插件注册、AI provider 配置、worker 启动、可选实时 observation feed 到 Telegram/Discord/Slack。**本仓库的 80% 的项目只声称 "compatible with Claude Code"，claude-mem 是少数把 OpenClaw 写进 README + 独立文档站 + 一键安装脚本的三栈项目**——这是目标生态 tiebreaker。

### 3. Cluster 共享 + Topics 命中（Layer 1+3 双信号）

- **Layer 1（cluster 共享）**：`articles/context-memory/` cluster 已有 30+ 篇，与本项目强相关
- **Layer 3（topics 命中）**：`topics: ['claude-skills', 'claude-code', 'anthropic']` 三个目标生态标签全部命中
- 实际 description 直接说：「Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More」——这是描述级别（而非仅 topics）的目标生态嵌入

### 4. 维度互补 ≠ 重叠（Layer 4 验证）

| 维度 | Anthropic Article | claude-mem Project |
|------|-------------------|---------------------|
| 范式层 | 理论框架（如何思考 context）| 工程实现（具体数据流）|
| 来源 | 闭源 + 官方 | 开源 Apache-2.0 + 社区 |
| 范围 | Agent 内部 | Agent 内部 + 跨 Agent 边界 |
| 状态管理 | 范式层概念 | SQLite + ChromaDB + 实时 observation feed |

四维互补，**无重叠**。

## 核心机制拆解

### 1. Observation Capture（自动捕获层）

Claude Code 的 Hooks 系统让 claude-mem 在**不修改用户 prompt**的前提下监听每条 tool 调用。捕获的事件包括：文件读写、Bash 命令执行、搜索查询、MCP tool 调用。每条 observation 写入本地 SQLite，附带 metadata（时间戳、session_id、tool_name、token_estimate）。

```bash
# 一次 install 即可，无需任何配置
npx claude-mem install
# 内部触发：注册 plugin hook → 启动 worker service → 启动 web viewer (port 37777)
```

### 2. AI Compression Pipeline（压缩层）

原始 observation 数量巨大（一次 session 可能产生 1000+ tool calls）。claude-mem 用 AI 对 observation 做**分层压缩**：

- **L1 Raw Observation**：原始 tool 输出（保留全部细节）
- **L2 AI Summary**：每 N 条 observation 触发一次 AI 摘要（用户可配置 N 和 AI provider）
- **L3 Session Summary**：session 结束时生成 session-level summary
- **L4 Project Summary**：跨 session 累积生成 project-level understanding

这套分层是 Anthropic 提出的 **token-cost-aware progressive disclosure** 的具体实现——L1 用于精确回忆，L4 用于项目级 context priming。

### 3. Progressive Disclosure Retrieval（回注层）

新 session 启动时，claude-mem 不**全部**注入历史 context，而是分三步：

1. **Discovery**：扫描项目历史，识别**当前任务相关**的 session（语义相似度）
2. **Activation**：注入相关 session 的 L3/L4 summary（约 500-2000 tokens）
3. **Execution**：仅当 Agent 显式调用 `mem-search` skill 时，才加载 L1/L2 原始数据

这正是 Anthropic 强调的「**不填满上下文，只填该填的**」原则的工程化。

### 4. Cross-IDE Compatibility（跨 Agent 边界）

README 强调「Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More」——同一个安装产物可被多个 Agent CLI 共享。技术实现 = 标准化 storage 格式 + 多个 IDE-specific hook 适配器。**这与 wquguru/harness-books（Pair R379）提出的「控制面哲学」一脉相承——claude-mem 是该哲学在 memory 子领域的参考实现**。

## 与本仓库已有项目的对比

| 项目 | 关注点 | 与 claude-mem 的差异 |
|------|--------|---------------------|
| `vectorize-io/hindsight` (R354) | 长期记忆 + 跨 session 学习 | hindsight 偏 research/agent framework，claude-mem 偏 plugin/可即装即用 |
| `tirth8205/code-review-graph` (R371) | 代码图谱 + MCP | code-review-graph 偏 code intelligence，claude-mem 偏 context memory |
| `nanocoai/nanoclaw` (R375) | 容器化 harness 替代 | nanoclaw 偏 self-contained container，claude-mem 偏 cross-IDE memory layer |
| `anysearch-ai/anysearch-skill` (R367) | L3 状态协议 | anysearch-skill 偏 query，claude-mem 偏 stateful memory |
| `darrenhinde/OpenAgentsControl` (R361) | Plan-first 控制 | OpenAgentsControl 偏 plan-as-quality-gate，claude-mem 偏 memory-as-context-priming |

**互补关系而非竞争关系**——这些项目都在 Agent harness 大主题的不同子象限。

## 适用场景

✅ **长 session 跨日工作**：开发 Agent 跨多次重启保持项目认知  
✅ **多 Agent 协作**：Claude Code + Gemini CLI + OpenCode 共享同一份 memory  
✅ **OpenClaw 部署**：直接在 OpenClaw Gateway 上启用持久化 memory  
✅ **代码考古 / bug 复现**：通过 observation 历史回溯 agent 决策链  
✅ **Context Engineering 实战**：把 Anthropic 范式直接落到生产环境

❌ **短期 POC / 一次性任务**：overhead 超过收益  
❌ **完全离线场景**：压缩层需要 AI provider 调用  
❌ **超敏感隐私数据**：尽管有 `<private>` tags，SQLite 本地存储仍需用户审查

## License / 安全审计

- **License**: Apache-2.0（商业友好，无 copyleft 限制）
- **依赖审查**: 单一 npm package + worker service，攻击面较小
- **数据本地化**: SQLite + ChromaDB 全部本地存储，无云端泄漏
- **隐私控制**: `<private>` 标签可排除敏感 observation 不入库
- **审计日期**: 2026-06-15 via GitHub API（spdx_id = "Apache-2.0", stars = 82,234）

## 结语

`thedotmack/claude-mem` 82K stars 不是营销数字，而是**工程师在 Anthropic 范式发布后用脚投票的结果**。当 Anthropic 还在写「Effective context engineering for AI agents」理论文章时，claude-mem 已经把**Compaction + Structured Note-taking + Sub-agent** 三件套打包成一个 `npx` 命令可安装的插件。

**最值得关注的不是它的功能列表，而是它的定位**：「**Persistent Context Across Sessions for Every Agent**」——它把 memory 从「某个 Agent 内部的状态」升级为「**跨 Agent 边界的基础设施**」。这是 Anthropic 范式在生态层最重要的外延。

对于本仓库的 context-memory cluster 而言，claude-mem 是 2026 年最值得收录的「**Anthropic 范式 → 跨 Agent 插件**」对位项目——它把一个 2025-12 的理论概念变成了 2026-06 的 82K 工程师的日常工具。

---

**参考来源**：

- [thedotmack/claude-mem GitHub](https://github.com/thedotmack/claude-mem)
- [Claude-Mem 官方文档](https://docs.claude-mem.ai/)
- [OpenClaw 集成指南](https://docs.claude-mem.ai/openclaw-integration)
- [Context Engineering 文档](https://docs.claude-mem.ai/context-engineering)
- [Progressive Disclosure 原则](https://docs.claude-mem.ai/progressive-disclosure)
- [Pair Article: Anthropic Context Engineering 三层范式](articles/context-memory/anthropic-context-engineering-triple-layer-long-horizon-2026.md)
- [Pair Article: Effective Context Engineering 5 Patterns](articles/context-memory/agent-context-engineering-five-patterns-2026.md)
- [R354 Hindsight Project - 长期记忆对比](articles/projects/vectorize-io-hindsight-long-term-memory-agents-learn-16216-stars-2026.md)
- [R375 nanoclaw Project - Cross-IDE harness 对比](articles/projects/nanocoai-nanoclaw-30k-stars-openclaw-alternative-containerized-2026.md)
