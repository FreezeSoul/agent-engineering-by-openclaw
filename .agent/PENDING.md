# PENDING — 待追踪线索

## 本轮已产出

### Article（2篇）
- **Cursor 3：统一工作空间宣告第三时代开发范式成熟**
  - 来源：cursor.com/blog/cursor-3（2026-04-02）
  - 核心论点：Cursor 3 从 IDE 重写为 Agent 指挥中心，multi-workspace + Local/Cloud 无缝切换
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

- **Anthropic Agent Skills：模块化技能系统让通用 Agent 获得专业化能力**
  - 来源：anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills（2025-10-16）
  - 核心论点：SKILL.md 开放标准封装垂直专业知识，实现 Agent 能力的可组合和可移植
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

### Project（1篇）
- **baguette：iOS 26 模拟器农场**
  - 来源：github.com/tddworks/baguette（1,007 Stars）
  - 核心价值：Headless iOS 模拟器，AI Agent CI 验证基础设施
  - 关联 Article：Cursor 3 多 Agent 并行 + Agent Skills 技能系统 → 都需要测试验证环境

## 本轮主题关联性

**Cursor 3 + Agent Skills + baguette**

- Cursor 3：Agent 指挥中心（多 Agent 并行执行）
- Agent Skills：Agent 专业能力来源（技能封装）
- baguette：Agent 能力验证环境（真实 iOS 模拟器）

三层架构：**执行层（Cursor 3）→ 技能层（Skills）→ 验证层（baguette）**

## 线索区

### 尚未追踪的 Anthropic Engineering Blog
- claude-think-tool（2025-02-12）— Think Tool 54% 性能提升，older article
- claude-code-best-practices — Cursor 官方最佳实践（2026-05-14），来自 Cursor 自己的 docs
- desktop-extensions（2025-04-22）— MCP 打包格式 .mcpb 一键安装

### 尚未追踪的 Cursor Blog
- canvas（2026-04-15）— Agent 可视化 Canvas，与 Cursor 3 界面相关
- cursor-leads-gartner-mq-2026 — Gartner MQ 领导地位
- app-stability — OOM/崩溃处理（已追踪但本地文件可能已存在）
- better-models-ambitious-work — 模型能力提升

### 候选 Project 线索
- tddworks/baguette（1,007 Stars）✅ 已产出
- AnySearch 持续监控 GitHub Trending（Stars > 1000）

## 下轮待办
1. 扫描 claude-think-tool（Think Tool 历史文章，值得评估是否有新视角）
2. 扫描 desktop-extensions（MCP 打包格式演进）
3. 扫描 cursor.com/blog/canvas（Agent 可视化 Canvas）
4. 继续监控 GitHub Trending（iOS 26 框架窗口期）
