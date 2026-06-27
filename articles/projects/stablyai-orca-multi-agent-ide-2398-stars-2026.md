# Orca: 把整个开发团队装进一个窗口的 AI Orchestrator

> 本文属于 Projects 推荐系列，为你深度分析当前 GitHub 高质量 AI/Agent 开源项目。

## 核心命题

当你在凌晨三点同时跑着 Claude Code、Codex、OpenCode 三个 coding agent 处理不同模块时，你需要的不只是一个终端——你需要一整个**多 Agent 工作台**。Orca 就是这个东西：它把每个 Agent 装进独立的 git worktree，用一个桌面应用统一调度、监控、合并。

![Orca GitHub](screenshots/stablyai-orca-2398-stars-2026-06-27.png)

## 一、为什么这个方向值得关注

### 从"单 Agent 效率"到"多 Agent 并行"的范式拐点

2026 年中，coding agent 领域正在经历一个微妙但重要的转变：从业界主流的「一个长会话 agent 做完所有事」，开始分化出「多个专业化 Agent 并行工作」的第二条路线。

这条路线有几个驱动力：
- **上下文窗口的性价比**：让一个 Agent 做完 100k token 的任务，成本远高于让 5 个 Agent 各做 20k token
- **模型能力的专业化分工**：Claude Code 适合架构决策，Codex 适合代码补全，OpenCode 适合开源生态对接——没有哪个模型在所有任务上都是最优解
- **结果可对比性**：同一个需求让多个 Agent 分别实现，能直接对比质量和风格差异

笔者认为，**多 Agent 并行工作会是 2026 年下半年最重要的 coding agent 演进方向**，而 Orca 正是这个方向目前最成熟的桌面级产品。

## 二、Orca 的核心设计

### 2.1 Parallel Worktrees：隔离但协同

Orca 的核心抽象是 **worktree**——每个 Agent 运行在自己独立的 git worktree 里，共享父仓库但完全不干扰彼此的分支状态。

```bash
# Orca CLI 创建并行 worktree
orca worktree create --agent claude-code --task "用户认证模块" feature/auth
orca worktree create --agent codex --task "支付集成模块" feature/payment
orca worktree create --agent opencode --task "API 文档" feature/docs
```

每个 worktree 有独立的：
- 文件系统路径（完全不冲突）
- git 分支（可独立 commit/PR）
- 终端会话（WebGL 渲染的终端 splits）

### 2.2 Mobile Companion：脱离电脑也能监控

Orca 提供 iOS/Android 应用，能在手机上：
- 接收 Agent 任务完成通知
- 发送文字/语音指令给指定 Agent
- 查看 worktree 状态和 git diff

这对需要「睡前发起任务、起床看结果」的工作流非常实用。

### 2.3 Design Mode：UI Agent 的杀手级功能

Orca 的 Design Mode 允许你点击真实 Chromium 窗口里的任意 UI 元素，把它的 HTML/CSS + 截图直接注入到 Agent 的 context 中。这意味着你的 Agent 不再只能读代码——它能「看见」你正在看的界面。

```markdown
Design Mode 注入示例：
[截图中选中的按钮]
HTML: <button class="checkout-btn primary">立即购买</button>
CSS: .checkout-btn { background: #0066ff; padding: 12px 24px; }
```

这是笔者见过的最实用的 Agent ↔ UI 设计稿打通道，比任何截图描述 prompt 都精准。

## 三、与竞品的差异

| 维度 | Orca | adenhive/hive | 其他方案 |
|------|------|---------------|---------|
| **形态** | 桌面 App + CLI | CLI 工具 | 脚本拼接 |
| **隔离方式** | git worktree（生产级）| 独立进程 | 手动管理 |
| **UI 协作** | ✅ Design Mode | ❌ | ❌ |
| **移动端** | ✅ iOS/Android | ❌ | ❌ |
| **多模型支持** | Claude/Codex/OpenCode/Pi | 多 Agent 框架 | 依赖外部 |
| **Stars** | 2,398（增长中）| 10,593 | — |
| **License** | MIT | Apache-2.0 | — |

笔者认为，Orca 和 hive 解决的是不同层次的问题：**hive 更适合纯 CLI 环境下的多 Agent 调度**，**Orca 更适合需要 UI 协作、设计协作、移动端监控的完整开发场景**。

## 四、适用场景与不适用场景

**✅ 适合：**
- 同时开发多个功能模块，需要隔离避免相互污染
- 想对比不同 coding agent 对同一任务的质量差异
- 远程服务器上跑 Agent，本地监控进度
- UI Agent 需要读取真实页面截图的场景

**❌ 不适合：**
- 纯 CLI 环境（没有图形界面）
- 单 Agent 长任务（Orca 的价值在多 Agent 场景才体现）
- 团队协作场景（目前是单人工具）

## 五、快速上手

```bash
# 安装 Orca CLI
brew install stablyai/tap/orca

# 启动桌面应用
orca app

# 创建第一个并行 worktree
orca worktree create --agent claude-code --task "实现登录模块"

# 在移动端配对（扫描二维码）
orca mobile pair
```

官网：https://onOrca.dev | GitHub：https://github.com/stablyai/orca

## 六、Stars 变化追踪

| 时间 | Stars | 备注 |
|------|-------|------|
| 2026-06-27（本次收录）| 2,398 | 相比 6 月初增长 7x |
| 2026-06-13（R552）| ~331 | 早期发现 |

> ⭐ 本次收录理由：Stars 从 331 增长到 2,398（7x 增长），MIT License，Design Mode + Mobile Companion 功能组合稀缺，值得推荐。

---

*推荐原则：本文为独立发现，与 Articles 无需强制配对，但 Orca 的多 Agent 并行工作模型与当前 Agent 领域「单 Agent 长会话 → 多 Agent 并行」的演进趋势高度吻合。*