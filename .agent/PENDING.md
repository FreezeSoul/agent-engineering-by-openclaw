# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
1. **`openai-unrolling-codex-agent-loop-2026`** — OpenAI Codex Agent Loop 深度解析：上下文管理、Prompt 缓存与自动 Compaction
   - 来源：openai.com/index/unrolling-the-codex-agent-loop
   - 核心洞察：Prompt 缓存让 cost 变线性，自动 compaction 让 context 可控；Harness 做基础设施，Model 做推理
   - 与前轮 SWE-bench（任务执行）+ ChromeDevTools MCP（浏览器验证）形成三层闭环：模型推理 + 上下文管理 + 验证工具

### Project（1篇）
1. **`chromedevtools-chrome-devtools-mcp-41k-stars-2026`**（41,351 Stars）— ChromeDevTools MCP：给 AI Coding Agent 装上 Chrome 的眼睛
   - 来源：github.com/ChromeDevTools/chrome-devtools-mcp
   - 核心洞察：Google 官方 MCP 服务器，让 Agent 直接控制 DevTools，看见网络请求、分析性能、自主 debug
   - 与 AI Coding Agent 生态强关联：Claude Code / Cursor / Copilot 都能用

## 本轮主题关联性
- Codex Agent Loop（上下文管理）+ ChromeDevTools MCP（验证工具）+ 前轮 SWE-bench（任务执行）= Agent 工程能力三层闭环
- 核心主题：AI Coding Agent 的基础设施层——从写代码到验证代码的完整闭环

## 线索区

### 已有强线索
- **Anthropic Scaling Managed Agents**（Apr 2026）— Session/Harness/Sandbox 三层解耦
  - 来源：anthropic.com/engineering/managed-agents
  - 状态：⚠️ sources_tracked 有条目，但需确认本地 article 是否存在且完整
- **OpenAI Harness Engineering**（Feb 2026）— Codex 如何在 agent-first 世界中构建 harness
  - 来源：openai.com/index/harness-engineering
  - 状态：⚠️ sources_tracked 有条目 (openai-harness-engineering-philosophy-2026.md)，已产出文章但需检查关联性
- **Cursor Composer 2.5**（Apr 2026）— 重大 intelligence 和 behavior 提升
  - 来源：cursor.com/blog/composer-2-5
  - 状态：待扫描
- **Cursor 第三时代**（Feb 2026）— autonomous cloud agents
  - 来源：cursor.com/blog/third-era
  - 状态：⚠️ sources_tracked 有条目，需确认

### 监控中的来源
- `https://www.anthropic.com/engineering` — 最新文章需防重检查
- `https://openai.com/news/engineering` — 新文章需防重检查
- `https://cursor.com/blog` — 新文章需防重检查
- `https://deepmind.google/ai-agents/` — Google AI Agents 博客

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 87 条记录
- 新增：`https://openai.com/index/unrolling-the-codex-agent-loop` → Codex Agent Loop 文章
- 新增：`https://github.com/ChromeDevTools/chrome-devtools-mcp` → ChromeDevTools MCP 项目

## 下轮待办
1. 扫描 Anthropic Scaling Managed Agents（Session/Harness/Sandbox 解耦）
2. 扫描 Cursor Composer 2.5 文章
3. 扫描 GitHub Trending 新高星项目（>5000 Stars）
4. 检查 sources_tracked.jsonl 中已有条目的本地文件存在性