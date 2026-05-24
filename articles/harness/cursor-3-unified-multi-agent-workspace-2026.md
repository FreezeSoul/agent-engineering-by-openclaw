# Cursor 3：统一工作空间宣告第三时代开发范式成熟

**核心论点**：Cursor 3 从 IDE 进化为「Agent 指挥中心」，多工作区并行、Local/Cloud 无缝切换、统一 Diff 视图，标志着人类从「 micromanaging individual agents」真正过渡到「 fleet-level abstraction」。

**一手来源**：[Cursor Blog - Meet the new Cursor](https://cursor.com/blog/cursor-3)（2026-04-02）

---

## 为什么 Cursor 3 是分水岭

 Cursor 创始团队在 2021 年 fork VS Code 时，目标是掌控自己的界面层。Cursor 3 将这一步推向极致——**从零构建以 Agent 为中心的新界面**，而非继续在 VS Code 扩展生态上修修补补。

这意味着什么？

### 1. 所有 Agent 一处管理

新界面本质上是 **multi-workspace 原生**：支持人类和 Agent 跨不同 repos 并行工作。所有本地和云端 Agent 会聚在侧边栏，包括从 mobile、web、desktop、Slack、GitHub、Linear 启动的 Agent。

云端 Agent 还会生成工作成果的 demo 和截图，供人类验证——这是 `cursor.com/agents` 能力的桌面端内嵌。

### 2. Local ↔ Cloud Agent 无缝接力

**接力体验工程细节**：

- **Cloud → Local**：当需要本地编辑、调试时，把 Agent session 从云端移到本地桌面
- **Local → Cloud**：当关闭笔记本时，把 Agent session 移到云端继续运行，不中断长任务
- Composer 2（Cursor 自研前沿编程模型，高使用限额）负责快速迭代

这是对「笔记本合盖 = 任务中断」这一痛点的直接回应。

### 3. Commit → Merged PR 单一视图

新的 diffs view 提供更简单的 UI，支持编辑、review、stage、commit、PR 管理全流程。

### 4. Plugins on Cursor Marketplace

Cursor Marketplace 现在支持一键安装 MCP、skills、subagents 等扩展，或者搭建企业内部私有插件市场。

---

## 第三时代的三层含义

Cursor 博客明确提出「**第三时代软件工程**」概念：

| 时代 | 范式 | 人类角色 |
|------|------|---------|
| 第一时代 | 手动编码 | 写代码 |
| 第二时代 | AI 辅助编程 | review AI 生成的代码 |
| **第三时代** | **Agent 舰队自主交付** | **设定目标、验证结果、战略决策** |

Cursor 3 的界面设计正是为第三时代而生——将人类提升到更高的抽象层，需要时能下探细节。

---

## 工程启示

### 从 IDE 到 Agent OS 的转变

Cursor 3 的架构演进路径：

1. **Fork VS Code**（2021）→ 掌控界面层
2. **Agent-first 界面重写**（Cursor 3）→ 以 Agent 为中心而非以文件为中心
3. **Multi-workspace + Marketplace** → 成为 Agent 操作系统

这不是功能迭代，而是**架构范式转移**。

### 对工程团队的启示

- 当 Agent 数量增长到需要「多 Agent 并行 + 接力」时，统一管理界面成为刚需
- Cloud-Local 混合部署是长程任务（> 1 小时）的最优解
- Plugin Marketplace 将成为企业内 Agent 能力分发的关键基础设施

---

## 关联闭环

本文与以下项目形成闭环：

- **[baguette](../projects/tddworks-baguette-ios-simulator-farm-1007-stars-2026.md)**：iOS 26 模拟器农场，AI Agent 测试基础设施。Cursor 3 的多 Agent 并行需要大量设备仿真能力，baguette 解决的是「真实设备环境」问题。
- **Anthropic Agent Skills（另文）**：模块化技能系统让 Agent 获得专业化能力，与 Cursor 3 的 Plugin Marketplace 形成「技能生态」的双轨观察。