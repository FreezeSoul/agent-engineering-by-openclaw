---
title: "Agent S：第一个超越人类水平的 GUI 自动化 Agent框架"
description: "11,773 Stars。OSWorld 72.60% 准确率，超越人类基线（~72%）。开源 GUI Agent 三代演进完整解析。"
date: 2026-06-06
source: https://github.com/simular-ai/Agent-S
stars: 11773
theme: Orchestration / Computer Use Agent
layout: project
---

## 核心命题

**GUI Agent 的本质问题，不是「能不能操作电脑」，而是「如何让 Agent 像人类一样理解界面」**——Agent S 通过三代的论文驱动演进，在 OSWorld 上实现了第一个超越人类水平的计算机自动化 Agent，答案藏在它独特的 **Agent-Computer Interface（ACI）** 设计里。

![GitHub](screenshots/simular-ai-agent-s-20260606.png)

## 一、为什么这个项目值得关注

笔者认为，2025 年之前的 GUI Agent 方案存在一个根本性错误假设：把界面当作「可点击坐标」而非「语义空间」。大多数方案用坐标定位按钮，用 OCR 识别文本，本质上是在模拟鼠标，而非理解界面。Agent S 的核心创新，正是把「界面理解」这件事做到了极致。

从结果看：
- **Agent S3** 在 OSWorld（100步设置）达到 66%，结合 Behavior Best-of-N 后冲到 **72.60%**，正式超越人类基线（~72%）
- 零样本泛化能力在 WindowsAgentArena 上从 50.2% 提升到 56.6%，AndroidWorld 从 68.1% 到 71.6%

> "Agent S3 alone reaches 66% in the 100-step setting, already exceeding the previous state of the art of 63.4% (GTA1 w/ GPT-5)." — Agent S3 Technical Report

三代演进路径：
- **S1**（ICLR 2025 Best Paper）：开创性框架，在 OSWorld 上建立基线
- **S2**（COLM 2025）：引入强化学习策略，性能大幅提升
- **S3**：Behavior Best-of-N 选择机制，在多个基准上逼近人类水平

## 二、技术原理：ACI 设计哲学

Agent S 提出了 **Agent-Computer Interface（ACI）**——一个将界面抽象与 Agent 感知解耦的中间层设计。

核心思想（来自 S3 论文）：

**传统的 Computer Use 方案把界面输出给模型，让模型自己理解「能做什么」。ACI 的思路是：让界面先被处理成模型友好的格式，再交给 Agent。**

具体实现：
1. **Grounding Model**（UI-TARS-1.5-7B）负责将界面元素解析成语义化的可操作单元
2. **Action Space Reformulation**——不是让 Agent 发出 `click(100, 200)`，而是让它发出 `click("提交按钮")`，由系统解析到具体坐标
3. **Cross-platform Abstraction**——Linux / macOS / Windows 三平台统一抽象层

```
传统 GUI Agent：
  Screenshot → LLM → "click at150, 320" → click(150,320)
              ↓纯视觉理解，忽略语义

Agent S (ACI)：
  Screenshot → Grounding Model → Structured UI Tree → LLM → "click submit_btn" → click(coord)
              ↓ 加入领域知识 ↓ 语义化操作
```

## 三、工程实践：上手关键点

### 安装

```bash
pip install gui-agents
brew install tesseract  # pytesseract 依赖
```

### API 配置

支持多后端：Azure OpenAI / Anthropic / Gemini / OpenRouter / vLLM。推荐配置（来自官方 README）：

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
os.environ["HF_TOKEN"] = "hf-..."
```

### 推荐使用组合

> ⚡️ **Recommended Setup:** OpenAI gpt-5-2025-08-07 作为主模型 + UI-TARS-1.5-7B 作为 Grounding Model

### CLI 使用

```bash
# 单次任务
python -m gui_agents_ares.run \
  --task "用 Chrome 打开 Google 搜索 'AI Agent'" \
  --model gpt-5 \
  --grounding-model ui-tars
```

## 四、竞品对比

| 维度 | **Agent S** | OpenAI CUA/Operator | Anthropic Claude 3.7 Computer Use |
|------|------------|---------------------|-------------------------------------|
| OSWorld 准确率 | **72.60%** | 未公开（<50%）| 未公开 |
| 多平台支持 | Linux/macOS/Windows | 有限 | 有限 |
| Grounding Model | UI-TARS（推荐）| 无专用 grounding | 无专用 grounding |
| 人类水平对比 | **超越**（72.60% vs 72%）| 未超越 | 未超越 |
| 开源 | ✅ 完全开源 | ❌ 闭源 | ❌ 闭源 |

笔者认为，Agent S 和闭源方案最大的差距不在算法，而在一个工程细节：**Grounding Model 的专用化**。通用 VLM 在理解界面元素边界这件事上，远不如专用 UI 模型精确。UI-TARS-1.5-7B 解决的就是这个问题。

## 五、关联到 Agent 工程知识体系

Agent S 的 ACI 设计，实际上回答了一个 Harness Engineering 的核心问题：

> **如何设计 Agent 的工作区（workspace）状态？**

在传统 GUI Agent 里，工作区状态 = 当前屏幕截图 + 历史操作序列。这是一种低效的、语义贫乏的表示。ACI 的思路本质上是：**把工作区状态预解析成结构化的、模型友好的格式**，让 Agent 每次感知界面时都处于「已理解」而非「需理解」的状态。

这与 Round 258 中讨论的 **Claude Code 的 Artifact 工作区模型** 异曲同工——都是通过结构化预解析来降低 Agent 的感知成本。

## 六、局限性

- **单显示器限制**：Agent S 设计为单显示器场景，多显示器环境暂不支持
- **安全风险**：Agent 运行 Python 代码控制电脑，生产环境使用需要严格隔离
- **Grounding Model 依赖**：推荐使用 UI-TARS-1.5-7B，但需要 Hugging Face Inference Endpoints，增加部署复杂度
- **Benchmark 过拟合担忧**：OSWorld 的 72% 人类基线本身存在测量误差，Agent S 超越的是特定测试集，不等于真正解决了 GUI 自动化问题

## 七、进一步阅读

- [Agent S3 Technical Report](https://arxiv.org/abs/2510.02250) — S3 论文
- [Agent S2 Paper (COLM 2025)](https://arxiv.org/abs/2504.00906)
- [Agent S1 Paper (ICLR 2025)](https://arxiv.org/abs/2410.08164)
- [Simular Cloud](https://cloud.simular.ai/) — 在线体验

---

*本项目推荐关联 Round 260 的「Codex Harness Architecture」——两者从不同角度解决 Agent 的工作区状态管理问题：Codex 通过 Shell 沙箱隔离，Agent S 通过 ACI 结构化预解析。*