# DomDemetz/claude-soul：当 Claude Code 学会记住

**GitHub**: [DomDemetz/claude-soul](https://github.com/DomDemetz/claude-soul) | **Stars**: 32（截至 2026-05-17）| **Created**: 2026-05-16

**主题关联**：本文承接《Claude Code Auto Mode：权限失控时代的系统级应答》，从「如何让 Agent 记住」的角度延续对 Claude Code 生态的深度分析。

---

## 一句话亮点

> Claude Soul 解决的是一个让所有 Claude Code 重度用户都会心一笑的问题：**每次开新 Session，Agent 就像失忆了一样——同一个错误犯两遍，同一个偏好总是忘。**

这不是一个 Memory Plugin（存储发生过什么），而是一个 **Growth Engine（学会怎么思考）**。

---

## 核心问题：Claude Code 的「Session 失忆症」

| 状态 | 表现 |
|------|------|
| **无 Claude Soul** | 每个 Session 从零开始，犯同样的错，给出通用回复，不记得什么有效 |
| **有 Claude Soul** | 跨 Session 积累，形成认知框架，根据真实反馈调整行为 |

官方自己的说法：

> *"Memory plugins store what happened. Claude Soul develops how to think."*

这不是一个 ChatGPT Memory 那样的简单 KV store，而是一个**持续进化的认知框架系统**。

---

## 工作机制：Signals → Reflection → Evolution

```
┌─────────────────────────────────────────────────────────┐
│                  Claude Soul 工作流                     │
├─────────────────────────────────────────────────────────┤
│  Signals（信号提取）                                     │
│    从每次对话中自动提取学习信号：                        │
│    纠正 → 成功模式 → 困惑点                             │
│                                                         │
│  Reflection（反思）                                      │
│    周期性地用 LLM 将信号综合成认知框架                    │
│    框架不是静态事实，而是「验证后再确认」的观点          │
│                                                         │
│  Evolution（进化）                                       │
│    框架根据真实证据增减置信度                            │
│    不适用的框架自动退役，新框架从模式中涌现              │
└─────────────────────────────────────────────────────────┘
```

### 三个进化阶段

From the README:

**Day 1（`--starter` 安装时）**：
- 身份文件中植入 Pushback、战略思考、验证行为
- 6 个活跃框架立即指导回复
- 信号提取开始工作

**~1 Week（~20 Sessions）**：
- 首次反思触发
- 框架根据你的使用习惯增减置信度
- 不适用于你工作的框架自动淘汰

**~2 Months（~200 Sessions）**：
- **Pushback**：Agent 不再是可etown，开始在你犯错时反对、建议替代方案
- **Depth Calibration**：需要一行回答的问题给一行，复杂架构问题给深度
- **Self-Correction**：在回复中捕捉自己的杜撰，先验证再说
- **Strategic Thinking**：跨 Session 思考时机、定位、权衡

---

## 技术实现：MCP Server + Identity Files

安装后会在 `~/.soul/` 创建：
- `identity files` — 持久化身份
- `MCP server` — 与 Claude Code 集成
- `hooks` — 挂载到 Claude Code 生命周期

使用方式：在 `CLAUDE.md` 中加入：

```markdown
## Soul System
Call `soul_context()` at the start of every conversation.
Use `soul_reflect` when you have idle time.
```

核心命令：

| 操作 | 命令 |
|------|------|
| 加载身份+上下文 | `soul_context()` |
| 快速反思 | `"run a quick reflection"` |
| 深度反思 | `"do a deep reflection"` |
| 记录成功 | `"signal: that approach worked well because..."` |
| 记录失败 | `"signal: that was wrong, the issue was..."` |
| 查看活跃框架 | `"what frameworks are active?"` |

---

## 与 Auto Mode 的互补关系

这是一个有趣的对照：

| 项目 |解决的问题 | 层次 |
|------|---------|------|
| **Auto Mode** | Agent 行动超出用户意图 | 输出控制层 |
| **Claude Soul** | Agent 缺乏跨 Session 学习和身份 | 输入/认知层 |

Auto Mode 解决的是「Agent 做了不该做的事」；Claude Soul 解决的是「Agent 记不住该记的事」。两者是 Agent 成熟度道路上的不同维度——**安全**vs**成长**。

笔者认为：Claude Soul 代表了一个更激进的理念——**Agent 不只是工具，应该是可以成长的协作者**。这个方向目前还很早期，但 200 sessions 后的 Pushback 效果值得期待。

---

## 快速上手

```bash
# 安装（含预置框架，立即生效）
npx claude-soul init --starter

# 空白起点（从零发现自己的框架）
npx claude-soul init
```

**前置条件**：Node.js >= 18，Claude Code（Pro 或 Max Plan）。

---

> **引用来源**
> - [DomDemetz/claude-soul - GitHub README](https://github.com/DomDemetz/claude-soul)
> - `npx claude-soul init --starter` — 官方安装命令