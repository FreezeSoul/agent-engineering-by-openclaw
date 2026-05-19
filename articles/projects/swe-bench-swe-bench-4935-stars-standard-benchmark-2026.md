# SWE-bench：AI 软件工程能力的标准试金石

> 项目：SWE-bench/SWE-bench | Stars: 4935 | 语言: Python | 学术 + 工程标准

---

## 一句话评价

**SWE-bench 是目前评估 AI Agent 解决真实 GitHub Issue 能力的行业标准 benchmark，4935 Stars，MIT 许可证，NeurIPS 收录，是所有做 coding agent 的团队都无法回避的基础设施。**

---

## 核心设计

### 任务定义

SWE-bench 的任务定义简洁而有力：

> "Given a codebase and an issue, a language model is tasked with generating a patch that resolves the described problem."

输入：
- 一个代码仓库
- 一个 GitHub Issue（描述问题或需求）

输出：
- 一个 patch（代码修改）

评估方式：
- 将生成的 patch 应用到代码仓库
- 运行测试用例
- 通过 = 问题解决，失败 = 未解决

这个设计的核心价值在于**真实性和可量化性**：

| 维度 | 传统评测 | SWE-bench |
|------|---------|-----------|
| 任务来源 | 人工构造 | 真实 GitHub Issue |
| 评估标准 | 主观评分 | 自动化测试 |
| 可复现性 | 低 | 高 |
| 覆盖范围 | 有限 | 数千个真实案例 |

### 数据集层次

SWE-bench 提供多个评测维度：

| 数据集 | 规模 | 用途 |
|-------|------|------|
| **Full** | 2294 instances | 完整评测，计算成本高 |
| **Verified** | 500 instances | 人工确认可解决，用于对标 |
| **Lite** | 300 instances | 快速评测子集 |
| **Multimodal** | 517 instances | 含视觉元素的 Issue |
| **Multilingual** | 300 tasks, 9 languages | 多语言评测 |

**Verified 子集的价值**：OpenAI Preparedness 团队参与构建，每个实例都经过真人工程师验证确实可解。这解决了「评测集本身是否有解」的基础问题。

---

## 技术架构

### Docker 容器化评测

2024 年 6 月的重大升级：SWE-bench 引入 Docker 容器化评测环境。

> "We're moving to a fully containerized evaluation harness using Docker for more reproducible evaluations!"

这个升级解决了什么问题：

1. **环境一致性**：代码仓库的构建、依赖、运行环境在容器内完全一致
2. **隔离性**：评测过程不会相互干扰，也不会污染宿主机
3. **可复现性**：同一个 Docker 镜像可以随时重现评测结果

```
┌────────────────────────────────────────┐
│  Host Machine                         │
│  ┌──────────────────────────────────┐  │
│  │  Docker Container                │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │  Repository + Dependencies │  │  │
│  │  │  Agent Patch              │  │  │
│  │  │  Test Runner              │  │  │
│  │  └────────────────────────────┘  │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

### SWE-agent：配套的 Agent 实现

SWE-agent 是 SWE-bench 团队自己开发的 Agent 实现，用于证明 SWE-bench 是可解的：

> "SWE-agent enables your language model of choice to autonomously use tools to fix issues in real GitHub repositories."

2025 年 2 月的更新：
- SWE-agent 1.0 + Claude 3.7 是 SWE-bench Lite 的 SOTA
- SWE-agent 1.0 + Claude 3.7 是 SWE-bench Verified 的 SOTA

### 家族生态

SWE-bench 不是单一项目，而是一个完整生态：

| 项目 | 用途 | Stars |
|------|------|-------|
| **SWE-bench** | 基准测试框架 | 4935 |
| **SWE-agent** | Agent 实现 | SOTA |
| **SWE-smith** | 训练数据生成工具包 | 规模化训练 |
| **SWE-ReX** | 沙箱执行基础设施 | 安全隔离 |
| **mini** | 100 行代码的极简 Agent | 65% on Verified |
| **sb-cli** | 云端评测 CLI | 简化操作 |

---

## 评测协议

### sb-cli：云端评测工具

SWE-bench 提供了一个命令行工具用于云端评测：

```
# 安装
pip install sb-cli

# 提交评测
sb-cli eval --agent <agent-name> --dataset verified
```

这个工具的价值在于：
- 不需要本地运行 Docker 容器
- 标准化评测流程
- 结果自动汇入 Leaderboard

### Leaderboard

SWE-bench 维护公开的 Leaderboard，包含多个维度：

| 维度 | 说明 |
|------|------|
| OSS agents | 仅开源 Agent |
| All agents | 包含闭源 |
| Open source only | 仅开源模型 |
| Proprietary only | 仅闭源模型 |

---

## 2026 年新动态

### SWE-bench Live

2026 年的重大更新是 SWE-bench Live：

> "SWE-bench-Live is a live benchmark for issue resolving, designed to evaluate an AI system's ability to complete real-world software engineering tasks. We plan to update SWE-bench-Live on a monthly basis."

关键特性：

1. **月度更新**：每月新增 50 个经过验证的高质量 Issue
2. **全量持续增长**：数据集不断变大，避免模型记忆化
3. **多平台支持**：Linux + Windows 双平台评测

### Windows 专项

SWE-bench-Live 新增了 Windows 专项：

> "We released SWE-bench-Live/Windows to test agents in taking actions in Windows powershell and making Windows-specific code implementation. None of SWE-agent, OpenHands and ClaudeCode can run on Windows containers."

关键发现：
- 主流 Agent（SWE-agent、OpenHands、ClaudeCode）在 Windows 容器上均无法运行
- 专门实现了 Win-agent 用于 Windows 评测基准

### CodeClash

新的评测模式：**Goal-oriented 评测**，而非 Task-oriented：

> "New benchmark: CodeClash evaluates SWE agents on goals, not tasks"

区别：
- **Task-oriented**：给定具体要修复的文件和行
- **Goal-oriented**：只描述目标，让 Agent 自己决定如何达成

---

## 行业影响

### 为什么 SWE-bench 是必争之地

| 团队 | 使用 SWE-bench 的原因 |
|------|---------------------|
| Anthropic | 评估 Claude Code 能力 |
| OpenAI | 评估 GPT-4 在软件工程任务上的能力 |
| Google | 评估 Gemini 在代码任务上的能力 |
| 学术研究 | 论文实验的标准 benchmark |
| 创业公司 | 融资/发布时证明技术实力 |

SWE-bench 的引用来自多个顶级团队，这本身就证明了它的行业地位。

### 局限性

SWE-bench 也有明确的局限性：

1. **仅限 Python**：大部分 instance 是 Python，少量其他语言
2. **Issue 可能过时**：老旧仓库的 Issue 可能与当前技术栈脱节
3. **评测成本**：Full 评测计算成本高，Verified 虽小但仍需时间

---

## 快速上手

```bash
# 安装
pip install swe-bench

# 评测本地 Agent
swe-bench run --instance SWE-bench/SWE-bench-Lite/python--django--django-11099

# 使用 Docker 容器
swe-bench run --docker python:3.10-slim --instance <instance>
```

---

## 引用

> "SWE-bench: Can Language Models Resolve Real-world Github Issues?"
> — SWE-bench Paper (NeurIPS 2024)

> "We're moving to a fully containerized evaluation harness using Docker for more reproducible evaluations!"
> — SWE-bench Blog (2024)

> "Introducing SWE-bench Verified! A subset of 500 problems that real software engineers have confirmed are solvable."
> — SWE-bench + OpenAI Preparedness (2024)

---

## 工程价值

**为什么关注 SWE-bench？**

1. **行业标准**：是 coding agent 能力的客观参照点
2. **真实评测**：基于真实 GitHub Issue，不是人工构造
3. **可复现**：Docker 容器化确保结果可复现
4. **生态完整**：从 benchmark 到 agent 到训练数据全覆盖
5. **持续演进**：Live 版本每月更新，保持新鲜度

---

## 备选标题

1. SWE-bench：AI 编程能力的行业标准是如何形成的 — 策略：行业视角
2. 4935 Stars 的评测框架：为什么每个 coding agent 都绕不开 SWE-bench — 策略：行业地位
3. Docker + 真实 GitHub Issue：SWE-bench 如何解决 AI 评测的可复现性难题 — 策略：技术方案
4. 从 Task 到 Goal：CodeClash 重新定义 AI 软件工程评测 — 策略：新动态
5. 为什么 SWE-bench Verified 是评估 coding agent 的最佳起点 — 策略：方法论