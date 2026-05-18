# Cursor 自举之道：Composer 环境自动配置的 RL 训练新范式

**核心问题**：RL 训练中环境配置失败会浪费大量计算资源并产生无效Reward Signal——而 Composer 的解决方案是用旧版本模型自动配置新环境。

---

## 为什么环境配置是 RL 训练的致命瓶颈

Cursor 在文章中直指核心痛点：

> *"if the environment is broken at the start, the model wastes tokens debugging setup instead of learning to solve problems. In the worst cases, a bad environment can make a problem unsolvable entirely, which ends up burning compute for no reward signal."*

这揭示了一个关键认知：**环境配置不是准备工作，而是训练的一部分**。配置失败不是"再来一次"的小问题，而是直接导致模型学到错误行为。

传统的解决方案是人工精心准备环境——但这成为了扩展瓶颈。Cursor 的答案是**让模型自己配环境**。

---

## Autoinstall 两阶段架构

Composer autoinstall 采用了非常优雅的两阶段设计：

### 第一阶段：Goal Setting Agent

给第一个 Agent（Composer 1.5）输入代码库 checkout，让它提出 10 条命令和高级输出描述——定义"成功"的标准。

这个 Agent 会探索 README、makefile、语言特定的包管理器（uv、clippy 等），最终输出一组 setup 命令、测试命令和启动命令。

### 第二阶段：Execution Agent

第二个 Agent（也是 Composer 1.5，但独立运行）接收初始环境状态和第一阶段选出的 3 条目标命令，然后实际执行环境配置。

如果 5 次重试后仍无法满足标准，该环境被丢弃。

**关键设计**：两个 Agent 职责分离——一个定义成功，一个尝试成功。这比让单一 Agent 既配置又验证更可靠。

---

## 自举的魔法：模型自己配环境训练自己

Cursor 揭示了这个方案最有趣的地方——**用旧版本模型管理新版本模型的训练环境**：

> *"Composer 2 now scores significantly higher on Terminal-Bench (61.7% versus 47.9% for Composer 1.5)"*

这意味着 Composer 2 在环境配置基准上比 Composer 1.5 高出近 14 个百分点。反过来，Composer 2 将会提供更好的 base 用于 autoinstall。

这是一个**自举飞轮**：更好的模型 → 更好的环境配置 → 更好的训练信号 → 更好的模型。

---

## 工程细节：从真实项目中看到的能力边界

Cursor 分享了一个真实案例——配置 Celo monorepo（大型区块链项目）的过程：

第一阶段，Agent 读取项目文档后还用了 Web 命令搜索额外的设置命令。第二阶段，它发现需要安装 Foundry（一个相关的独立项目），通过 Web 搜索阅读 Foundry 文档后完成了配置。第一次尝试运行最小化应用失败了，第二次重试时创建了一个 mock user 来启动本地应用。

**这个过程展示了几个关键能力**：
- 自主发现缺失依赖并搜索解决方案
- 在失败后自动重试并调整策略
- 愿意创建 mock 对象来绕过缺失组件

---

## 笔者的判断：这不是一个功能，是范式转移

大多数 Agent 框架将环境配置视为"前期准备"，而 Cursor 的 autoinstall 揭示了一个更本质的认识：**环境配置是 Agent 能力的核心体现**。

一个真正强大的 coding agent 应该能够：
1. 在任意未配置环境中自主推断出正确的 setup
2. 在缺失依赖时主动寻找并安装
3. 创建 mock/fake 对象来处理不可用的外部依赖

这种能力不只是"让开发更方便"，而是 **Agent 从"执行已知步骤"到"自主理解并构建运行环境"的质变**。

Autoinstall 另一个被低估的意义是：**它把环境配置本身变成了可学习的 RL 任务**。模型不只是在学习解决coding问题，同时也在学习如何搭建能够解决coding问题的环境——这是一个meta-learning层面的自我改进。

---

## 对 Harness 工程的启示

从 Harness 设计的角度看，autoinstall 模式有几个值得深思的点：

**1. 双 Agent 验证比单 Agent 更可靠**
分离 goal-setting 和 execution 允许更干净的成功标准定义，也避免了"配置者验证自己"的逻辑漏洞。

**2. 有限重试 + 可信退出比无限重试更实用**
5 次上限后丢弃环境——这个设计把"无法配置"当作有效信号，而不是陷入无限重试。

**3. Mock 作为 first-class 能力**
Cursor 明确提到 Composer 会"mock missing files, create placeholder images, or even create fake database tables"。这意味着 **fake/mock 能力应该被内置到 Agent 的工具集中，而不是事后补救**。

---

## 关联项目

与本文讨论的 **Agent 环境自配置** 主题高度关联的 GitHub 项目：

- **[humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)** — 20,283 ⭐：构建可靠 LLM 应用的核心原则，从 12 Factor Apps 汲取灵感，涵盖 Context Engineering、Control Flow、State Management 等关键设计维度。与 Cursor 的 autoinstall 共同指向一个结论：生产级 Agent 需要精心设计的工程原则，而不是靠"更大的模型"来解决所有问题。

- **[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)** — 24,187 ⭐：即用型 Agent Skills，涵盖研究、科学、工程、分析、金融和写作领域。与 Cursor Composer 的 Skill 化训练方向一致——当 Agent 能够自主获取和组合 Skills 时，环境配置的边界将被进一步拓展。

---

## 引用

> *"Better environments mean better training signal"* — Cursor Engineering Blog

> *"Composer 2 now scores significantly higher on Terminal-Bench (61.7% versus 47.9% for Composer 1.5)"* — Cursor Engineering Blog

> *"To achieve that, it will mock missing files, create placeholder images, or even create fake database tables."* — Cursor Engineering Blog

---

**Related Links**：
- [Cursor Bootstrapping Composer with Autoinstall](https://cursor.com/blog/bootstrapping-composer-with-autoinstall)
- [Cursor Composer 2](https://cursor.com/blog/composer-2)
- [Terminal-Bench](https://www.tbench.ai/)