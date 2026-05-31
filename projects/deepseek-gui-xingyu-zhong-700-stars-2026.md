# DeepSeek GUI：桌面端 DeepSeek 智能体工作台

> 把 DeepSeek TUI 的本地智能体能力带进桌面窗口：**Code** 写代码、**Write** 写文档、**Claw** 接 IM 自动化——聊天、审查改动、管理 Skill/MCP 和更新，都在一个图形化工作台里完成。

## 基本信息

| 指标 | 数值 |
|------|------|
| GitHub | [XingYu-Zhong/DeepSeek-GUI](https://github.com/XingYu-Zhong/DeepSeek-GUI) |
| Stars | ⭐ 700 (2026-05-21) |
| License | MIT |
| 语言 | TypeScript |
| 官网 | [deepseek-gui.com](https://deepseek-gui.com) |

## 核心能力

DeepSeek GUI 并不是一个聊天壳，而是一个面向开发者和高频 AI 工作者的本地桌面工作台，让 DeepSeek 变成可以稳定参与真实项目工作的桌面伙伴。

### 三大模式

| 模式 | 功能 |
|------|------|
| **Code** | 围绕真实项目读取、编辑和创建文件，文件变更审查视图 |
| **Write** | 独立写作空间、Markdown 文件树、live 编辑/预览、文本补全 |
| **Claw** | 飞书/Lark 接入、独立 IM Agent、webhook relay、定时任务 |

### 技术架构亮点

- **桌面聊天工作台**：多会话、流式回复、推理过程实时查看、中断和重新发送
- **Skill/MCP 图形化管理**：不用手写配置就能扩展智能体能力
- **文件变更审查**：每一次修改都能被看见、理解和确认
- **跨平台**：macOS/Windows 预构建安装包，Linux 源码构建

## 与小模型 Coding Agent 的主题关联

[smallcode](articles/projects/doorman11991-smallcode-small-llm-coding-agent-1383-stars-2026.md)（1383 Stars）探讨的是「小模型能否做 Coding Agent」的问题。DeepSeek-GUI 则给出了另一个答案：**用 DeepSeek（671B MoE）这样的非顶级模型，通过桌面工作台的方式让 AI 稳定参与真实项目**。

| 维度 | smallcode | DeepSeek GUI |
|------|-----------|--------------|
| 模型 | 专注小模型（Sonnet 3.5 等） | DeepSeek（671B MoE） |
| 交互方式 | 纯命令行 | 桌面 GUI + 实时可视化 |
| 定位 | 轻量工具 | 完整工作台 |
| 目标用户 | 极客/小团队 | 开发者/高频 AI 工作者 |

## 工程洞察

DeepSeek GUI 的关键工程价值在于：**把 AI Agent 从终端的「单次对话」模式，升级为可持续工作的桌面伙伴**。这与 [cursor-multi-repo-automations](articles/orchestration/cursor-multi-repo-automations-cross-codebase-agent-engineering-2026.md) 强调的「跨代码库可持续 Agent」形成互补——两者都在解决「如何让 AI Agent 真正参与真实项目」的问题，只是角度不同。

---

*数据来源：[GitHub API](https://api.github.com/repos/XingYu-Zhong/DeepSeek-GUI)，抓取于 2026-05-31*