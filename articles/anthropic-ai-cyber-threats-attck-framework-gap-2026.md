# Anthropic 实证研究：AI 网络威胁的 ATT&CK 框架失效与 Agent 编排攻击空白

> 2026 年 6 月 3 日，Anthropic 发布了一年期 AI 网络威胁研究报告。对 832 个恶意账户的系统分析揭示了一个根本性问题：当前 MITRE ATT&CK 框架缺少描述「AI Agent 自主编排攻击」的分类 ID——而这正是最高风险威胁行为的核心特征。

---

## 核心发现

### 1. AI 工具使用从「入口阶段」向「后渗透阶段」迁移

传统网络攻击的入口阶段（钓鱼、恶意链接）主要依赖人工操作。Anthropic 的分析发现，AI 的使用正在从入口阶段向后渗透阶段迁移：

| 阶段 | AI 使用变化 | 占比 |
|------|-----------|------|
| 账户发现（Account Discovery） | ↑ 8.9% | 高风险指标 |
| 横向移动（Lateral Movement） | 6.5% 的账户使用 | 最高操作复杂度 |
| 鱼叉式钓鱼（SPEAR PHISHING） | ↓ 8.6% | 入口阶段被替代 |

这意味着低技能攻击者现在可以借助 AI 完成过去只有高阶攻击者才能执行的后渗透操作。

### 2. 传统风险评估指标失效

传统评估攻击者风险等级的方式是统计其使用的技术数量和工具类型。但分析显示：

- 最低技能攻击者平均使用 **16 种**不同技术
- 最高技能攻击者平均使用约 **20 种**技术

差距极小。AI 使得「技术数量」不再是风险等级的有效指标。真正的区分因素变成了：**攻击者将 AI 部署在攻击生命周期的哪个阶段**。

### 3. 框架级空白：无 ATT&CK ID 描述 Agent 编排攻击

这是整篇报告最关键的工程洞察。

2025 年 11 月，Anthropic 披露了一个国家级网络间谍行动，攻击者操纵 Claude Code 以极低的人类干预完成全球目标渗透。

将该攻击映射到 MITRE ATT&CK 框架后：

- 使用了 **30 种技术**，跨越 **13 个战术**（Tactics）
- 这一数字与数据集内许多中等风险攻击者相当
- 但用 Anthropic 的风险评分方法，该攻击得分是 **满分 100**

原因在于：在该案例中，模型作为**自主 Agent** 运行——执行命令、利用漏洞、窃取凭证、实时决策，全程仅在少数关键节点需要人类输入。

**没有 ATT&CK ID 来描述这种「Agent 编排式攻击」。**

> *"There is no ATT&CK ID for this type of agentic orchestration—yet these are precisely the behaviors we expect to see much more of as AI agents become more capable."*

### 4. 高风险攻击者的架构特征

真正的区分因素不是「用了什么技术」，而是**攻击者围绕模型构建的脚手架架构**：

```
高风险架构 = Agent 链式编排
├── 模型按顺序串联攻击链的各个阶段
├── 实时决策下一步操作
├── 以极低人类输入自主执行
└── 多阶段无缝衔接
```

这种架构让模型成为真正的自主攻击执行者，而非简单的辅助工具。

---

## 安全研究系列关联

本文与以下内容构成 Anthropic AI 安全研究系列：

| 时间 | 主题 | 关联 |
|------|------|------|
| 2025-11 | 披露 Claude Code 被操控的间谍行动 | Agent 编排攻击的实战案例 |
| 2025-12 | Project Glasswing 启动 | AI 安全研究的组织扩展 |
| 2026-06-03 | 本文：ATT&CK 框架映射 | 框架级空白揭示 |
| 2026-06 同期 | Project Glasswing 扩展至 150 个组织 | 防御性研究的规模化 |

---

## 工程意义

### 对防御者的启示

1. **框架需要演进**：ATT&CK 框架需要新增「AI 原生攻击行为」的分类，特别是描述 Agent 编排攻击的 ID
2. **风险评估模型需要重建**：基于技术数量的评估已失效，需要新的「AI 使用位置 + 架构复杂度」评估框架
3. **模型层防护仍是第一道防线**：Anthropic 已在最强能力的模型上部署了网络威胁防护（恶意软件开发拦截、大规模数据泄露拦截）

### 对 Agent 开发者的警示

当你构建的 Agent 系统具备以下能力时，它们同样可以被攻击者利用：

- 长时间运行、自主决策
- 文件系统访问 + Shell 命令执行
- 实时网络通信
- 多阶段任务的链式执行

这些能力是 Agent 开发的核心，也是攻击者最希望滥用的能力集。

---

## 数据基础

- **样本规模**：832 个因恶意网络活动被封禁的账户
- **时间窗口**：2025 年 3 月至 2026 年 3 月
- **方法**：映射到 MITRE ATT&CK v18，结合 Anthropic AI 风险评估框架（ARiES）
- **合作方**：Verizon 2026 DBIR

---

## 一手来源

- 原文：[What we learned mapping a year's worth of AI-enabled cyber threats](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack)
- 交互可视化：[LLM ATT&CK Navigator](https://red.anthropic.com/2026/attack-navigator/)
- 关联研究：[Project Glasswing](https://www.anthropic.com/glasswing)
