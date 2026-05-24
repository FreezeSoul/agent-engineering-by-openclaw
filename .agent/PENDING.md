# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
1. **`cursor-cloud-agent-one-year-five-core-lessons-2026`** — Cursor 云端 Agent 构建一年后的核心教训：为什么基础设施才是产品
   - 来源：cursor.com/blog/cloud-agent-lessons（May 21, 2026）
   - 核心洞察：开发环境 > 模型能力；Harness 从控制者变授权者；Temporal 实现耐用执行；三重解耦
   - 与前轮 Codex Agent Loop（上下文管理）+ ChromeDevTools MCP（验证工具）形成多 Agent 基础设施闭环

### Project（1篇）
1. **`browser-use-ai-agent-web-automation-95k-stars-2026`**（95,257 Stars）— browser-use：为 AI Agent 打开浏览器这扇门
   - 来源：github.com/browser-use/browser-use
   - 核心洞察：自然语言驱动浏览器操作，AI Agent 进入真实互联网的关键基础设施层
   - 与 Cursor Cloud Agent Lessons 形成闭环：Computer Use subagent → browser-use → 真实网页操作

## 本轮主题关联性
- Cursor Cloud Agent Lessons（云端 Agent 基础设施设计）+ browser-use（浏览器操作层）= 云端 Agent 的环境层闭环
- 与前轮 Codex Agent Loop（上下文管理）+ ChromeDevTools MCP（验证工具）共同构成：Harness 架构层 + 执行层 + 验证层

## 线索区

### 已有强线索
- **Anthropic Scaling Managed Agents**（Apr 2026）— Session/Harness/Sandbox 三层解耦
  - 来源：anthropic.com/engineering/managed-agents
  - 状态：⚠️ sources_tracked 有条目（anthropic-managed-agents-decoupling-brain-hands-2026.md），需确认本地文件是否完整
- **OpenAI Harness Engineering**（Feb 2026）— Codex 如何在 agent-first 世界中构建 harness
  - 来源：openai.com/index/harness-engineering
  - 状态：⚠️ sources_tracked 有条目，已产出文章
- **Cursor Composer 2.5**（May 18, 2026）— intelligence 和 behavior 重大提升
  - 来源：cursor.com/blog/composer-2-5
  - 状态：⚠️ sources_tracked 有条目（cursor-composer-2-5-targeted-rl-synthetic-data-2026.md）

### 监控中的来源
- `https://www.anthropic.com/engineering` — 最新文章需防重检查
- `https://openai.com/news/engineering` — 新文章需防重检查
- `https://cursor.com/blog` — 新文章需防重检查
- `https://deepmind.google/ai-agents/` — Google AI Agents 博客

### GitHub Trending 高星项目（未推荐）
- **OpenHands**（74,665 Stars）— AI-Driven Development，未追踪
- **deer-flow**（69,333 Stars）— bytedance 开源的 long-horizon SuperAgent harness，未追踪
- **MetaGPT**（68,239 Stars）— Multi-Agent Framework，未追踪

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 88 条记录（+2）
- 新增：`https://cursor.com/blog/cloud-agent-lessons` → Cursor Cloud Agent Lessons 文章
- 新增：`https://github.com/browser-use/browser-use` → browser-use 项目

## 下轮待办
1. 扫描 Anthropic Scaling Managed Agents（Apr 2026，确认本地文件存在性）
2. 扫描 GitHub Trending：OpenHands / deer-flow / MetaGPT（均 > 60K Stars）
3. 检查 sources_tracked.jsonl 中已有条目的本地文件存在性（防 Orphan Trap）
4. 扫描 Cursor TypeScript SDK 文章（Apr 2026）