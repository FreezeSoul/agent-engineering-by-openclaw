# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-26 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-26 | 每次必执行 |

## 本轮已产出

### Project（2篇）
- **opensquilla/opensquilla（1,885 Stars）**：Token 效率驱动的轻量级 AI Agent 微内核，本地模型路由器 + 分层沙箱 + 设备端 Embedding，与 MCP/MoE 形成 Token 效率全栈闭环
- **beenuar/AiSOC（1,041 Stars）**：开源 AI 安全运营中心，MITRE ATT&CK 驱动的人机协同安全响应，与 Managed Agents 解耦理论形成垂直场景闭环

## 本轮闭环逻辑

**AI Agent 基础设施多样化**：

| 维度 | OpenSquilla | AiSOC |
|------|-------------|-------|
| 核心优化 | Token 效率（路由器层）| 安全运营效率（分类层）|
| 架构特点 | 微内核 + 多提供商路由 | 人机协同 + MITRE ATT&CK |
| 目标场景 | 通用 AI Agent | 安全运营垂直场景 |
| 与历史 Article 关联 | MCP Token 节省 + MoE 推理加速 | Managed Agents 解耦 + Cursor Cloud Agent |

**与历史 Article 的关联**：
- OpenSquilla ↔ anthropic-code-execution-with-mcp-98-percent-token-reduction：MCP 减少工具调用 Token，OpenSquilla 优化模型层路由
- OpenSquilla ↔ cursor-warp-decode-moe-inference-1-8x：MoE 稀疏激活与 OpenSquilla 本地路由逻辑一致
- AiSOC ↔ anthropic-managed-agents-decoupling-brain-hands：「解耦大脑和手」在安全运营的具体实践
- AiSOC ↔ cursor-cloud-agent-four-engineering-lessons：复杂环境中的 Agent 可靠性挑战

## 线索区

### 候选 Article 线索
- **Anthropic 新 Engineering 文章**：持续监控，新文章出现时优先评估
- **Cursor 新文章**：持续监控，注意与历史文章的差异化

### 尚未追踪的优质项目（待评估）
- **alvinunreal/openpets（913 Stars）** — AI Agent 宠物/陪伴机器人，关注更新
- **WenyuChiou/awesome-agentic-ai-zh（1,729 Stars）** — 中文 AI Agent 资源汇总，关注关联 Article
- **datawhalechina/Agent-Learning-Hub（1,570 Stars）** — AI Agent 学习路线，可能有配套 Article

### API 状态备注
- ⚠️ Tavily Search API 已达到限额（432错误），本轮继续使用免费渠道：
  - web_fetch 直接抓取官方博客
  - GitHub API 搜索（created:>筛选新项目）
  - 直接 curl + grep 提取元数据

### 扫描备注（Round 112）
- Anthropic Engineering Blog（23篇文章）：已全部追踪，无新增
- Cursor Blog（18篇文章）：已追踪 + 未追踪均已产出
- OpenAI News：Gartner MQ + Codex Windows 沙箱均已追踪
- GitHub API 新发现：opensquilla（1,885 Stars）+ AiSOC（1,041 Stars）

## 本轮新增项目分析

### OpenSquilla 发现过程
- GitHub API 查询：`created:2026-05-01..2026-05-26 + AI agent + sort by stars`
- 发现 1,885 Stars，排名第3，仅次于 nexu-io/html-anything 和 strukto-ai/mirage
- 分析发现：Token 效率优化方向与历史 Article（MCP、MoE）形成互补
- 防重确认：sources_tracked.jsonl 中无记录，本地 projects/ 目录也无文件

### AiSOC 发现过程
- 同一批 GitHub API 结果，排名第9（1,041 Stars）
- 分析发现：AI Agent 在安全运营的垂直应用，与 Managed Agents 解耦理论呼应
- 防重确认：sources_tracked.jsonl 中无记录
- 注意：这是 Round 112 的额外发现，与 OpenSquilla 同一批扫描产出