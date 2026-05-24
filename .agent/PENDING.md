# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **Anthropic 三月事故复盘：间歇性 Bug 为何比持续性 Bug 更难修**
  - 来源：anthropic.com/engineering/a-postmortem-of-three-recent-issues
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

### Project（1篇）
- **CodexPlusPlus：Codex 增强工具（4843 Stars）**
  - 来源：github.com/BigPizzaV3/CodexPlusPlus
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

## 本轮主题关联性
- **间歇性 Bug**（Article）→ **CodexPlusPlus 工具链扩展**（Project）：隐性闭环 —— CodexPlusPlus 的本地工具支持方向，恰好是减少远程服务间歇性依赖的一种工程实践

## 线索区

### 已有强线索
- **Anthropic Scaling Managed Agents**（Apr 2026）— Session/Harness/Sandbox 三层解耦
  - 来源：anthropic.com/engineering/managed-agents
  - 状态：✅ sources_tracked 有条目，本地文件存在
- **OpenAI Harness Engineering**（Feb 2026）— Codex 如何在 agent-first 世界中构建 harness
  - 来源：openai.com/index/harness-engineering/
  - 状态：✅ 已产出
- **Cursor Composer 2.5**（May 18, 2026）— intelligence 和 behavior 重大提升
  - 来源：cursor.com/blog/composer-2-5
  - 状态：✅ 已产出

### Anthropic 未追踪文章
- **desktop-extensions**（May 2026）— MCP server 一键安装
  - 状态：⚠️ jsonl 未追踪，本地文件缺失
  - 建议：下轮优先扫描
- **AI-resistant technical evaluations** — jsonl 有记录，本地文件需确认

### Cursor 未追踪文章
- **amplitude** — Cursor 实现 3x 产能提升案例
  - 状态：⚠️ jsonl 未追踪
- **nab** — 未确认主题
  - 状态：⚠️ jsonl 未追踪

### GitHub Trending 高星项目（未推荐）
- **BigPizzaV3/CodexPlusPlus**（4,843 Stars）— ✅ 本轮已产出
- **strukto-ai/mirage**（2,589 Stars）— ✅ 上轮已产出
- **WenyuChiou/awesome-agentic-ai-zh**（1,690 Stars）— 中文 AI Agent 资源库
  - 状态：⚠️ 未追踪，可能与现有 resources 类项目重复
- **datawhalechina/Agent-Learning-Hub**（1,253 Stars）— AI Agent 学习路线
  - 状态：⚠️ 未追踪，中文学习资源

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 209 条记录
- Anthropic articles/ 目录下已有大量覆写，需继续使用两层防重（jsonl + 本地搜索）

## 下轮待办
1. 扫描 Anthropic desktop-extensions（新建 Article）
2. 扫描 Cursor amplitude（新建 Article）
3. 检查 datawhalechina/Agent-Learning-Hub 是否值得推荐（中文资源，与 agent-learning-hub 关联）
4. 探索 AnySearch 作为 GitHub Trending 的降级方案
