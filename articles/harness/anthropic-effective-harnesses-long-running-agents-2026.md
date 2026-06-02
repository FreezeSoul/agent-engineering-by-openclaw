# Anthropic 长时运行 Agent 评测框架：跨越 Context Window 的工程机制

> 本文解读 Anthropic Engineering Blog 文章：*Effective harnesses for long-running agents* (2025.11)
> 原文：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

---

## 核心论点

长时运行 Agent 的核心挑战不是「能力不足」，而是**跨 Context Window 的状态传递问题**。Anthropic 的解法不是造一个万能 Agent，而是通过结构化的环境管理——初始化 Agent + Feature List + Progress File + Git History——让每个新 Session 都能在 3 步内定位状态，把「跨session记忆」从模型内部压缩变成**外部可读取的工件（Artifacts）**。

---

## 一、问题：Agent 在长时任务中为什么会失败

Anthropic 观测到，即便给 Opus 4.5 配上 Claude Agent SDK + Compaction，在跨越多个 Context Window 的长时任务中，Agent 仍然会陷入两种典型的失败模式：

### 失败模式 1：One-Shot 冲动

Agent 倾向一次性实现整个应用。遇到 Context 耗尽时，停在「功能实现一半、代码未归档」的状态。下一个 Session 的 Agent 必须先花大量时间「猜测」前面发生了什么，再花等量时间把基础状态恢复出来。**Compaction 传递的信息不够清晰**，无法确保下一个 Agent 拿到的是可继续工作的上下文。

### 失败模式 2：过早宣布胜利

当项目已经有了某些功能之后，新的 Agent 实例会「环顾四周，看到已有进展」，然后宣布任务完成。这与模式 1 正好相反——不是做太多，而是**看不到还有多少没做完**。

这两个问题的根源相同：**Agent 每次都从「空状态」开始，既不知道之前做了什么，也不知道还有什么没做**。

---

## 二、解法：两阶段 Agent 架构

Anthropic 的方案将 Agent 角色分成两类，但使用完全相同的 System Prompt 和工具集：

```
┌─────────────────────────────────────────────────────────────┐
│  Initializer Agent（初始化 Agent）                          │
│  ├─ 触发条件：项目第一个 Session                            │
│  ├─ 任务：基于用户需求扩展为 Feature List JSON              │
│  │         生成 init.sh（启动脚本）                        │
│  │         提交初始 git commit                             │
│  └─ 产出：完整的环境骨架 + 200+ 个细化功能项               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Coding Agent（编码 Agent）                                  │
│  ├─ 触发条件：每个后续 Session                              │
│  ├─ 任务：每次只做一个功能                                  │
│  │         完成后将 passes: false → true                    │
│  │         写 git commit + claude-progress.txt             │
│  └─ 关键约束：离开时必须留下「可合并到主分支」的状态       │
└─────────────────────────────────────────────────────────────┘
```

### Feature List 的设计细节

Initializer Agent 基于用户的高层需求，生成一个结构化的 Feature List JSON 文件，每个功能节点包含：

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": [
    "Navigate to main interface",
    "Click the 'New Chat' button",
    "Verify a new conversation is created",
    "Check that chat area shows welcome state",
    "Verify conversation appears in sidebar"
  ],
  "passes": false
}
```

关键设计选择：**使用 JSON 而非 Markdown**。Anthropic 发现模型对 JSON 的改写欲望低于 Markdown，不容易发生「悄悄删除功能项或修改描述」的情况。Prompt 中使用明确措辞：「**It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality**」。

---

## 三、Progress File + Git History：Agent 的外部记忆

传统的 Human-in-the-loop 工程师交接靠什么？**工作笔记 + 代码提交记录**。Anthropic 把这套实践搬进了 Agent harness：

### claude-progress.txt

每次 Coding Agent Session 结束时写入，包含：
- 当前完成的功能
- 遇到的问题和绕过方式
- 下一个 Agent 需要关注的事项

### Git History 作为状态导航

每个 git commit message 描述的是「实现了哪个功能」，不是「改了什么文件」。这样下一个 Agent 通过 `git log --oneline` 就能重建整个开发timeline，而不需要重新读代码。

### 快速定位流程（每个 Session 开始时执行）

```bash
pwd                          # 确认工作目录
cat claude-progress.txt      # 读取进度记录
cat feature_list.json        # 了解功能完成状态
git log --oneline -20        # 重建开发时间线
./init.sh                    # 重启开发服务器
# 运行基础功能验证测试
```

> 这套流程将「新人 onboarding」从可能耗费 30 分钟的空转，变成 5 分钟内的高效定位。

---

## 四、测试：被低估的最后一公里

Anthropic 发现了一个**关键的测试盲区**：模型即使在 Session 内做了测试（unit test / curl），也会在未确认功能真正 end-to-end 工作的情况下将 passes 标记为 true。

解法：**提供 Browser 自动化工具**（Puppeteer MCP Server），让 Agent 像真实用户一样操作界面、截图验证。

```python
# Agent 通过 Puppeteer MCP 执行的验证逻辑（示意）
1. 启动本地开发服务器
2. 用 Puppeteer 打开应用
3. 模拟用户操作（点击、输入、提交）
4. 截图比对预期 UI
5. 验证 API 响应和 UI 反馈是否一致
```

通过这种方式，Agent 能发现**纯代码层面看不到的 bug**（例如浏览器原生 alert modal 无法通过 Puppeteer 捕获，导致相关功能 bug 率偏高）。

---

## 五、失败模式与解法映射表

| 失败模式 | Initializer Agent 解法 | Coding Agent 解法 |
|---------|----------------------|-----------------|
| One-Shot 冲动（一次做太多）| 生成 Feature List，强制逐功能实现 | 每次只选一个最高优先级功能 |
| 过早宣布胜利 | 建立所有功能的完整清单 | 读取 Feature List，自验证后再标记 passes |
| 环境状态脏乱 | 初始 git repo + init.sh | 结束前 commit + progress update |
| 不清楚做什么 | 完整的 Feature List + 优先级 | 读取 progress + git log 定位 |
| 测试不充分 | 提供 Browser 自动化工具 | 必须通过 Puppeteer 端到端验证 |

---

## 六、工程意义：Harness 作为架构层

这篇文章的深层含义是：**Harness 不是「给 Agent 包装一层安全壳」，而是定义了 Agent 如何与工作状态交互的接口协议**。

关键洞察：

1. **外部状态 > 内部记忆**：模型压缩 Context Window 是被动行为，但通过 Feature List + Progress File，Agent 能主动「查询」而非「猜测」状态
2. **结构化 > 自由文本**：JSON Feature List 强制模型在「状态变更」和「状态查询」之间保持一致的语义，不给模型留下模糊空间
3. **测试即验证而非完成标志**：将 end-to-end 测试结果作为 passes 的必要条件，防止模型自我安慰

Anthropic 在文末提出了一个开放问题：**单一通用 Agent 是否是最优解**？还是说专用 Agent（测试 Agent、QA Agent、代码清理 Agent）能做得更好？这与 Cursor 的 Multi-Agent Kernel 研究形成呼应——当任务足够复杂时，分工优于全能。

---

## 七、与现有研究的关联

| 概念 | 本文 | 相关文献/项目 |
|------|------|-------------|
| 跨 Session 状态管理 | Feature List + Progress File + Git History | Anthropic GAN Architecture (harness-design-long-running-apps) |
| 增量式任务分解 | 每次只做一个功能 | Cursor Composer 2.5 Targeted RL |
| 端到端测试验证 | Puppeteer MCP 截图验证 | Harbor Terminal-Bench |
| 多角色 Agent | 文末提出：专用 vs 通用 Agent | Cursor Multi-Agent Kernel (Planner-Worker-Judge) |
| 工作区状态传递 | Git commit as memory | OpenAI Codex Long Horizon (25h self-driving) |

---

## 八、适用场景判断

**适合使用此 Harness 模式的场景**：
- 需要跨越数小时乃至数天的复杂软件工程项目
- 多个 Agent 实例需要协同工作的场景
- 需要明确的进度追踪和责任边界的任务

**不太适合的场景**：
- 短时、一次性完成的任务（开销大于收益）
- 需要强实时性的交互式任务
- 模型本身能力不足以完成基本功能的情况（Harness 不能替代模型能力）

---

> **引用来源**：Justin Young, "Effective harnesses for long-running agents", *Anthropic Engineering Blog*, November 26, 2025. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents