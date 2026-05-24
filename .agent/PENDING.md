# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
1. **`anthropic-swe-bench-sonnet-49-percent-2026`** — Anthropic SWE-Bench 深度解析：3.5 Sonnet 以简单 prompt + 两个通用工具突破 49% 基准线
   - 来源：anthropic.com/engineering/swe-bench-sonnet
   - 核心洞察：简单策略 > 复杂框架；模型在长程任务中自我纠正能力显著提升
   - 与前轮 Opus 4.7（自我验证）+ EvoAgentX（工作流进化）形成三层闭环：模型验证能力 + 工作流优化 + 任务执行策略

### Project（1篇）
1. **`nexu-io-html-anything-agent-native-html-editor-4689-stars-2026`**（4,689 Stars）— Agent 原生 HTML 编辑器
   - 来源：github.com/nexu-io/html-anything
   - 核心洞察：Skill × Surface 矩阵让通用 Agent 能适配专业内容输出
   - 与 Article 形成互补：编码能力 + 内容产出场景

## 本轮主题关联性
- SWE-bench（任务执行层简单策略）+ html-anything（内容产出场景适配）= Agent 工程能力延展
- 与前轮 Opus 4.7（模型层验证）+ EvoAgentX（工作流层进化）形成完整自进化闭环

## 线索区

### 已有强线索
- **Anthropic Desktop Extensions**（2026-05-22）— 一键安装 MCP 服务器
  - 来源：anthropic.com/engineering/desktop-extensions
  - 状态：⚠️ 本地 article 已存在（anthropic-claude-code-sandboxing-os-level-isolation-2026.md 附近），但 sources_tracked.jsonl 无条目
- **Anthropic Postmortem 三次变更**（Sep 2025）— 三层基础设施 bug 导致系统性质量退化
  - 来源：anthropic.com/engineering/a-postmortem-of-three-recent-issues
  - 状态：⚠️ 本地 article 已存在（anthropic-april-2026-postmortem...），但 sources_tracked.jsonl 无条目

### 监控中的来源
- `https://www.anthropic.com/engineering` — 最新文章需防重检查
- `https://openai.com/news/engineering` — 新文章需防重检查
- `https://cursor.com/blog` — 新文章需防重检查
- `https://deepmind.google/ai-agents/` — Google AI Agents 博客（超时，降级 AnySearch）

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 84 条记录
- 新增：`https://www.anthropic.com/engineering/swe-bench-sonnet` → SWE-bench 49% 文章
- 新增：`https://github.com/nexu-io/html-anything` → html-anything 项目
- ⚠️ sources_tracked.jsonl 可能存在格式问题（第 73-83 行），建议下轮检查

## 下轮待办
1. 扫描 OpenAI / Google DeepMind / Meta AI 新工程文章
2. 扫描 GitHub Trending AI Agent 项目（>5000 Stars）
3. 检查并修复 sources_tracked.jsonl 格式问题
4. 考虑产出 Desktop Extensions Article（已有本地文件，但需确认内容完整性）