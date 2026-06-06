# Round 266 执行报告

## 一、本轮核心交付

### Article: Cursor SDK Custom Tools + Nested Subagents (Jun 4, 2026)
- **路径**：`articles/ai-coding/cursor-sdk-custom-tools-mcp-server-pattern-2026.md`
- **核心论点**：Cursor SDK June 2026 通过内置 MCP 服务器 `custom-user-tools` 把"函数定义"直接变成"Agent 工具"，实现工具继承（父级定义 → 全链路渗透）和 Nested Subagents（任意深度层级委托，每层独立 prompt/model）
- **工程价值**：把扩展机制统一到 MCP 协议层——Custom tools 通过 MCP 服务器暴露，Auto-review 分类器决定调用是否执行，工具继承通过 MCP 链路自动渗透
- **Cluster**：ai-coding / custom-tools / mcp

### Project: ArcadeAI/arcade-mcp（915 ⭐）
- **路径**：`articles/projects/ArcadeAI-arcade-mcp-mcp-server-framework-custom-tools-2026.md`
- **路线**：Python MCP Server Framework，装饰器写工具 + run() 启动服务，三行代码启动 MCP 服务器
- **重要性**：与 Cursor SDK `custom-user-tools` 形成互补闭环——Cursor SDK 是"SDK 内部如何暴露自定义工具"，arcade-mcp 是"如何把你的服务变成标准 MCP 服务器让任何 Agent 都能用"
- **Stars**：915（≥ 500 阈值，满足"创新实现类"）

### 闭环逻辑
| 维度 | Article (Cursor SDK Custom Tools) | Project (Arcade-mcp) |
|------|----------------------------------|---------------------|
| 抽象层 | SDK 内部实现 | 独立 MCP 服务开发框架 |
| 核心机制 | 内置 MCP 服务器 `custom-user-tools` | 装饰器驱动的 MCP 服务器 |
| 解决问题 | 如何在 Cursor SDK 里零成本暴露自定义工具 | 如何把你的服务变成标准 MCP 服务器 |
| 互补关系 | SDK 内部工具暴露 | 跨 Agent 工具复用 |

**关键洞察**：两者共同指向同一个核心工程模式——**工具即 MCP 服务，MCP 服务即工具**。Cursor SDK 把这个模式做到 SDK 内部无缝集成，arcade-mcp 把这个模式做成通用开发框架。

## 二、扫描与防重

### 来源扫描
| 来源 | 状态 | 备注 |
|------|------|------|
| Anthropic engineering | 26/26 TRACKED | exhausted |
| Anthropic news | 全为非工程内容 | 跳过 |
| Cursor blog | 1 NEW | sdk-updates-jun-2026 产出 Article |
| Cursor changelog | 4 NEW (Round 265) | 均为产品级增量，无 Article 价值 |
| LangChain blog | 稳定 | cluster 饱和 |
| CrewAI blog | stale slug false positives | 跳过 |
| GitHub API | 6 个 NEW 项目 | wshobson/agents 已追踪，其余待评估 |

### 防重检查
- ✅ sources_tracked.jsonl（279→281 条，sdk-updates-jun-2026 + arcade-mcp 均为新）
- ✅ articles/projects 目录 grep（无 orphan 重复）
- ✅ wshobson/agents 已存在于 articles/projects（36k stars 版本已追踪）

## 三、关键发现

### 1. Cursor SDK 的 MCP 协议统一价值
- **内置 MCP 服务器 `custom-user-tools`**：你传函数定义，SDK 自动把它暴露成标准 MCP 工具，天然继承完整权限链路
- **工具继承**：父级定义 → 所有子 Agent 可用，无需每层重复注册
- **Auto-review 分类器**：自然语言指令驱动的权限控制，不写规则代码

### 2. arcade-mcp 的框架价值
- 三行代码启动 MCP 服务器（装饰器 + run()）
- 工具继承与层级化组合（MCP 服务器可组合子服务器）
- 与 Cursor SDK 形成"SDK 内部 ↔ 独立服务"互补

### 3. 高价值项目盘点（待下轮深入）
- `karpathy/autoresearch`（85,311 stars，630 行自训练系统）
- `langflow-ai/langflow`（149,275 stars，视觉 LangChain）
- `infiniflow/ragflow`（82,003 stars，RAG 引擎）
- `openai/swarm`（21,582 stars，OpenAI 多 Agent 编排）

## 四、待持续监控线索

1. **Cursor Enterprise Organizations**（Jun 3, 2026 GA）—— 多团队治理，与 Auto-review 协同
2. **karpathy/autoresearch**（85k stars）—— 自训练系统，可能与 multi-agent harness 相关
3. **openai/swarm**（21k stars）—— OpenAI 多 Agent 编排，但已有 agents-sdk
4. **Anthropic Engineering**—— 26/26 exhausted，等待新文章

## 五、Commit 记录

- `050e5e8` Round 265: update .agent/ state
- `[本轮]` Round 266: Cursor SDK custom tools article + ArcadeAI/arcade-mcp project

## 六、Self-Assessment

- ✅ 完成 Article + Project 双交付
- ✅ jsonl 健康度（279→281 条，新增 2 条均为新源）
- ✅ 闭环逻辑清晰（SDK 内部工具暴露 ↔ 独立 MCP 服务框架）
- ✅ 防重检查通过（wshobson/agents 已追踪不重复）
- ✅ Arcade-mcp 满足 stars 阈值（915 ≥ 500 "创新实现类"）
- ⚠️ 高价值项目（autoresearch/langflow/ragflow）待下轮深入评估

**执行流程**：
1. **理解任务**：执行 Round 266 cron 维护，扫描源、产出 Article + Project
2. **规划**：扫描 Cursor changelog（sdk-updates-jun-2026）→ 评估工程价值 → 搜索匹配 GitHub 项目
3. **执行**：cursor.com/changelog fetch + GitHub API search + write_file（Article + Project）+ jsonl record + README update + .agent/ 更新 + git commit
4. **返回**：发现 1 个高价值 Article（Cursor SDK custom tools）+ 1 个匹配 Project（arcade-mcp），完成 MCP 协议层互补闭环
5. **整理**：写 PENDING.md 持续监控 Enterprise Organizations / autoresearch 等下轮线索

**调用工具**：
- `exec`: 15+ 次（curl / grep / python3 / git）
- `read_file`: 3 次
- `write_file`: 5 次（Article + Project + README + state.json + REPORT）
