# Claude Code `/cd`：不重建 Prompt Cache 的目录迁移

> 来源：[Week 24 · June 8–12, 2026](https://code.claude.com/docs/en/whats-new/2026-w24) | Claude Code Docs
> 标签：`workspace-state` `context-management` `session-migration` `claude-code`

---

## 核心命题

Claude Code 的 `/cd` 命令解决了一个长期被忽视的问题：**如何在切换工作目录时保留已经构建好的上下文状态？**

传统方案是重建 Prompt Cache——这意味着丢失所有已累积的上下文。Claude Code 的方案是：**把新目录的 CLAUDE.md 作为消息追加，而不是替换系统提示词**。这个看似简单的设计选择，背后是一套完整的上下文迁移工程哲学。

---

## 问题：目录切换为何会丢失上下文？

在 `/cd` 出现之前，Agent 切换目录面临一个工程困境：

**传统路径**：检测目录变化 → 重新读取新目录的配置文件（如 CLAUDE.md）→ 重建系统提示词 → 重新初始化 Agent 状态

**代价**：
1. **Prompt Cache 必须重建**：已经消耗大量 Token 构建的上下文全部丢失
2. **会话状态丢失**：`--resume` 和 `--continue` 指向的位置发生变化
3. **项目存储割裂**：每个目录维护独立的会话历史，跨项目上下文无法延续

这对于需要在多个相关项目间协作的开发者来说是致命的——比如 monorepo 中的多个包、或者前后端分离的项目，每次切换都要"重新开始"。

---

## 解决方案：Append as Message

`/cd` 的核心创新在官方文档里只有一句话，但这一句话揭示了完整的工程思路：

> "The new directory's `CLAUDE.md` is appended as a message instead of replacing the system prompt."

### 三步走的实现逻辑

```
┌─────────────────────────────────────────────────────────────┐
│  /cd 执行前的状态                                            │
│  ├─ Prompt Cache 已构建（包含历史对话、项目上下文）           │
│  ├─ Session 指向旧目录的 .claude/ 存储                      │
│  └─ 当前工作目录：~/project-a                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  /cd ../project-b 执行时                                     │
│  ① 检测目录变化                                             │
│  ② 读取新目录的 CLAUDE.md（如果存在）                       │
│  ③ 将 CLAUDE.md 内容作为 USER MESSAGE 追加到对话           │
│  ④ 更新 Session 存储位置到新目录的 .claude/                │
│  ⑤ Prompt Cache 保持不变                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  /cd 执行后的状态                                            │
│  ├─ Prompt Cache 完全保留                                   │
│  ├─ 对话中新增一条 "Here's what I know about this project" │
│  ├─ Session 指向新目录的 .claude/                           │
│  └─ --resume 和 --continue 在新目录查找                     │
└─────────────────────────────────────────────────────────────┘
```

### 为什么"追加消息"比"替换系统提示词"更好？

这里有一个微妙的工程权衡：

| 方案 | Prompt Cache | 上下文连续性 | 实现复杂度 | 灵活性 |
|------|-------------|-------------|-----------|--------|
| 替换系统提示词 | ❌ 重建 | ❌ 完全断裂 | 低 | 低 |
| 追加为消息 | ✅ 保留 | ✅ 自然延续 | 中 | **高** |

追加为消息的优势在于：

1. **Cache 复用**：Prompt Cache 不需要重建，历史上下文仍然在 Cache 中
2. **语义连续**：CLAUDE.md 的内容作为上下文的一部分参与推理，而不是"覆盖"掉之前的上下文
3. **灵活性**：新目录的配置和旧目录的上下文可以同时存在，Agent 可以"看到"两边的信息
4. **调试友好**：追加的消息在对话历史中可见，开发者可以检查到底传递了什么上下文

---

## 工程机制：Session Storage 的重定向

除了消息追加，`/cd` 还做了一件关键的事：**Session Storage 的重定向**。

官方文档指出：

> "The session relocates to the new directory's project storage, so `--resume` and `--continue` find it there."

这意味着：
- `--resume` 在新目录的 `.claude/` 中查找会话
- `--continue` 在新目录的上下文中继续工作
- 跨目录的会话历史通过追加消息的方式保持连续

这是一个聪明的设计：**存储位置和上下文是分开的**。存储位置跟随目录（便于文件系统组织），上下文通过消息追加保持连续（便于语义连贯）。

---

## 新工作流：Context Bridging

`/cd` 开启了一种新的工作模式——我称之为 **Context Bridging**（上下文桥接）：

```
旧模式：                  新模式：
┌─────────────┐          ┌─────────────┐
│  Project A  │          │  Project A  │
│  (fresh)    │  ──/cd─→ │  (with full │
└─────────────┘          │   context)  │
                          └─────────────┘
                               │
                               ↓
                          ┌─────────────┐
                          │  Project B  │
                          │  (context   │
                          │   bridged)  │
                          └─────────────┘
```

**典型场景**：

1. **Monorepo 协作**：在 `packages/frontend` 工作，切换到 `packages/backend` 时保留前端项目的上下文
2. **全栈调试**：在 API 层发现 bug，切换到前端目录写测试，上下文无缝衔接
3. **代码审查**：在一个包的目录审查代码，切换到另一个包继续，审查历史不丢失

---

## 与 Multi-Agent 的关系

Week 24 的另一个特性是：**Subagents can spawn subagents**（子代理可以派生自己的子代理）。

结合 `/cd`，这开启了一种混合模式：

```
Main Session
  ├─ /cd ~/project-a
  │   └─ Subagent for frontend
  │       ├─ /cd ../shared-lib  (nested /cd!)
  │       └─ Sub-subagent for shared components
  └─ /cd ~/project-b
      └─ Subagent for backend
```

嵌套的 `/cd` 允许子代理在不同目录间迁移，同时保持其自身的上下文链条。这对于需要在多个目录间协调的大型任务特别有用。

官方将子代理链限制在 **5 层深度**，以防止失控的并发树：

> "Subagent chains are capped at five levels deep to prevent runaway concurrent trees."

这是一个务实的工程约束——既保留了嵌套的灵活性，又防止了无限递归的风险。

---

## 调试维度：Safe Mode

Week 24 还引入了 `--safe-mode`，这是一个调试工具：

```bash
claude --safe-mode
```

在安全模式下，以下内容不加载：
- `CLAUDE.md`
- Skills
- Plugins
- Hooks
- MCP servers
- Custom commands and agents

这对于诊断配置问题特别有用——如果问题在安全模式下消失，说明问题出在某个自定义配置上。

结合 `/cd`，这意味着：
- 在某个目录遇到配置问题？用 `--safe-mode` + `/cd` 可以隔离问题
- 新目录的上下文和调试状态可以同时存在

---

## 笔者观点

`/cd` 的设计体现了 Anthropic 对 Agent 工程的一个核心认知：**上下文是资产，不是负担**。

很多 Agent 系统把上下文当作"需要管理的资源"，倾向于在必要时清空和重建。Claude Code 的做法是：**上下文是累积的，应该被保留和桥接**。

追加 CLAUDE.md 作为消息而非替换系统提示词，这个选择背后是对"上下文连续性"的深刻理解。消息追加的方式让新旧上下文共存，而不是非此即彼。

对于需要在复杂项目结构中工作的开发者，这是一个实质性的效率提升。monorepo、库开发、全栈项目——这些场景下的目录切换不再是"重新开始"，而是"带着积累继续"。

---

## 总结

| 特性 | 核心创新 | 工程价值 |
|------|---------|---------|
| `/cd` 不重建 Prompt Cache | 追加 CLAUDE.md 为消息 | 上下文资产保留 |
| Session Storage 重定向 | 跟随目录但不丢失上下文 | 跨目录会话连续性 |
| 子代理可派生子代理 | 嵌套执行链，5层上限 | 多层次任务分解 |
| `--safe-mode` | 隔离自定义配置 | 调试友好 |

**核心启示**：Agent 的上下文管理不只是"能存多少"，还在于"如何在不同工作场景间迁移和桥接"。Claude Code 通过 `/cd` 展示了一种优雅的方案：追加而非替换，桥接而非断裂。
