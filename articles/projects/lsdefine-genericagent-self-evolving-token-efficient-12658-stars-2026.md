# lsdefine/GenericAgent：极简自展 Agent，从3K 行种子代码长出技能树

> 这个项目解决了一个让所有 Agent 开发者头疼的问题：**为什么 Agent 框架越来越重，而能力却没有本质提升？**

---

## 核心命题

当我第一次看到 GenericAgent 的架构时，第一反应是"这不对劲"——一个12,658 Star 的项目，核心 Agent Loop 只有 **~100 行代码**。这与当前"框架越来越重"的趋势完全相反。

```
LangChain: ~1200K 行依赖
CrewAI: ~200K 行依赖  
GenericAgent: ~3K 行核心代码
```

笔者认为，GenericAgent 的核心价值不在于"功能多"，而在于**重新定义了什么才叫 Agent 框架**——不是把所有能力都塞进去，而是让 Agent 自己长出能力。

**关键数据对比**：
- 上下文窗口需求：**<30K tokens**（其他 Agent 普遍 200K-1M）
-核心代码量：~3K 行
- Agent Loop：~100 行
- 原子工具数：9 个
- Token 消耗：其他 Agent 的 **1/6**

---

## 技术架构：从 3K 行种子代码长出来的系统

### 分层记忆机制

GenericAgent 的记忆系统分为 4 层，这是它"自展"能力的基础：

| 层级 | 名称 | 作用 |
|------|------|------|
| L0 | Meta Rules | 核心行为规则和系统约束 |
| L1 | Insight Index | 快速路由和召回的最小记忆索引 |
| L2 | Global Facts | 长期运行积累的稳定知识 |
| L3 | Task Skills / SOPs | 可复用的工作流，应对特定任务类型 |
| L4 | Session Archive | 归档的任务记录，用于长周期召回 |

```python
# Agent Loop 核心逻辑 (~100行)
Perceive environment state → Task reasoning → Execute tools →
Write experience to memory → Loop
```

每完成一个任务，GenericAgent 会自动将执行路径**结晶成可复用的 Skill**。使用越久，技能树越丰富——这正是"自展"的含义。

### 9 个原子工具

GenericAgent 只提供 9 个原子工具，覆盖系统级控制能力：

| 工具 | 功能 |
|------|------|
| code_run | 执行任意代码（Python/PowerShell）|
| file_ops | 文件系统操作 |
| browser | 浏览器注入控制 |
| terminal | 终端操作 |
| input | 键盘/鼠标输入控制 |
| screen_vision | 屏幕视觉感知 |
| adb | Android 设备控制 |
| memory | 记忆读写 |

这9 个工具足够驱动完整的桌面操作——外卖下单、股票筛选、自动浏览、支付宝记账。

### 自展证明

README 中有一段令人印象深刻的话：

> 🤖 **Self-Bootstrap Proof** — Everything in this repository, from installing Git and running `git init` to every commit message, was completed autonomously by GenericAgent. **The author never opened a terminal once.**

也就是说，这个仓库本身就是这个 Agent 的作品。这比任何 benchmark 都有说服力。

---

## 为什么"极简"反而是优势

当前主流 Agent 框架的设计哲学是**预先塞入大量能力**：
- LangChain 内置 RAG、工具、记忆、评估...
- AutoGen 多 Agent 协作、代码执行...
- CrewAI 角色定义、工作流...

笔者认为这种模式存在根本问题：**当框架承担了太多，Agent 就失去了自主生长的动力和能力**。

GenericAgent 的设计哲学是**"不要预加载技能，让它们自己进化"**：
- 不预装任何具体能力
- 每次完成任务后自动结晶 Skill
- 技能树随使用时长增长

这意味着 GenericAgent 不是一个"开箱即用"的工具，而是一个**会随你的使用变得更懂你的 Agent 系统**。

---

## Token 效率：被忽视的核心指标

在"context window is cheap"的叙事下，Token 效率很少被当作核心指标。但 GenericAgent 做到了 **<30K context window**，是其他 Agent 的 1/6。

笔者认为这个指标比很多人意识到的更重要：

1. **成本**：更少的 token = 更低的 API费用
2. **延迟**：更短的上下文 = 更快的推理
3. **精度**：更少的干扰信息 = 更少的幻觉
4. **可靠性**：简单上下文 = 更稳定的行为

当其他框架在卷"百万级 context window"时，GenericAgent 在卷"谁能在更少 context 下完成任务"——这是截然不同的工程方向。

---

## 多前端支持：不是特色，是必需

GenericAgent 支持多种即时通讯前端：

| 平台 | 启动命令 |
|------|---------|
| Telegram | `python frontends/tgapp.py` |
| WeChat | `python frontends/wechatapp.py` |
| QQ | `python frontends/qqapp.py` |
| Feishu/Lark | `python frontends/fsapp.py` |
| WeCom | `python frontends/wecomapp.py` |
| DingTalk | `python frontends/dingtalkapp.py` |

这种设计让 GenericAgent 成为一个**可以在任何 IM 平台上运行的个人 Agent**。笔者认为这是"Desktop Agent"到"Personal Agent"的关键一步——你不需要打开特定的 App，Agent 就在你日常沟通的工具里。

---

## 适用场景

GenericAgent 适合：

- **个人效率自动化**：外卖下单、记账、股票筛选
- **需要长期运行的 Agent**：技能树随使用增长
- **Token 成本敏感的场景**：6x 的 token 节省
- **多平台桌面操作**：Windows/macOS/Linux + Android

GenericAgent 不适合：

- 需要开箱即用完整能力的场景
- 不希望 Agent 有自主操作权限的场景
- 依赖复杂 RAG 能力的场景

---

## 快速上手

```bash
# Linux/macOS 一键安装
GLOBAL=1 bash -c "$(curl -fsSL http://fudankw.cn:9000/files/ga_install.sh)"

# Windows PowerShell
powershell -ExecutionPolicy Bypass -c "$env:GLOBAL=1; irm http://fudankw.cn:9000/files/ga_install.ps1 | iex"

# 启动桌面应用
frontends/GenericAgent.exe

# 或使用 TUI
python frontends/tuiapp_v2.py
```

---

## 总结

笔者认为 GenericAgent 之所以值得推荐，不是因为它功能多，而是因为它代表了一种**反主流的工程哲学**：

> 不是把 Agent 框架做成瑞士军刀，而是让 Agent 自己长出技能。

当其他框架在追求"预装更多能力"时，GenericAgent 在追求"让 Agent 自己学会更多"。3K 行种子代码、9 个原子工具、<30K 的 context需求——这不是简陋，而是**极简主义的工程美学**。

如果你厌倦了臃肿的 Agent 框架，想要一个会随着你的使用变得更懂你的系统，GenericAgent 值得关注。

---

**项目信息**：

|指标 | 值 |
|------|---|
| GitHub | [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent) |
| Stars | 12,658 |
| 语言 | Python (89.3%), JavaScript (6.5%) |
| 核心代码 | ~3K 行 |
| Agent Loop | ~100 行 |
| 上下文需求 | <30K tokens |
| License | MIT |