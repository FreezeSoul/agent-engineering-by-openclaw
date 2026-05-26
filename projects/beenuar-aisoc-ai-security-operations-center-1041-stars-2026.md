# AiSOC：开源 AI 安全运营中心——让 Agent 辅助威胁响应

> **来源**：[github.com/beenuar/AiSOC](https://github.com/beenuar/AiSOC)
> **Stars**：1,041（截至 2026-05-26）
> **语言**：Python / Next.js
> **许可证**：MIT

---

## 核心定位

AiSOC（AI-powered Security Operations Center）是一个**开源的 AI 安全运营中心**，它将 AI Agent 引入安全事件响应流程。传统 SOC 依赖大量人工分析告警，AiSOC 通过 AI Agent 实现**告警融合、紫色团队演练、Agent 辅助分类、MITRE ATT&CK 调查**的自动化。

> 原文引用：「Open-source AI-powered Security Operations Center — alert fusion, purple-team drills, agent-assisted triage, MITRE ATT&CK investigation. MIT-licensed, self-hostable.」
> 来源：[AiSOC README](https://github.com/beenuar/AiSOC)

---

## 解决什么问题

安全运营中心（SOC）是企业安全的第一道防线，但面临三个核心挑战：

1. **告警过载**：SIEM 每天产生数千条告警，人工分类耗时且容易遗漏
2. **技能稀缺**：合格的威胁分析师需要多年培养，人才供不应求
3. **响应滞后**：从发现到响应的平均时间（MTTR）过长，给攻击者留下窗口

AiSOC 通过 AI Agent 辅助分类和 MITRE ATT&CK 框架驱动的调查，实现**人机协同**的安全运营。

---

## 核心技术架构

### 1. 告警融合（Alert Fusion）

AiSOC 的告警融合引擎将来自多个来源（防火墙、IDS、EDR、SIEM）的告警进行**关联分析**，识别真正的攻击链而非孤立事件。这减少了 90% 的误报，让分析师专注于真实威胁。

### 2. 紫色团队演练（Purple Team Drills）

AiSOC 内置**攻击模拟**功能，安全团队可以用它来训练防御能力。AI Agent 生成的攻击场景会触发真实的防御响应，帮助团队发现检测盲区。

### 3. Agent 辅助分类

当告警进入系统，AI Agent 会先做**初步分类**：
- 判断是否为真实攻击
- 关联到 MITRE ATT&CK 框架中的 tactics 和 techniques
- 建议下一步调查动作

分析师只需审核 Agent 的建议，而非从零开始分析。

### 4. MITRE ATT&CK 调查

每个告警都会关联到 MITRE ATT&CK 框架，AIC Agent 的调查过程会追溯到**初始访问（Initial Access）→ 执行（Execution）→ 持久化（Persistence）** 的完整 kill chain。

---

## 与传统 SIEM 的关键差异

| 维度 | 传统 SIEM | AiSOC |
|------|-----------|-------|
| **告警分类** | 规则引擎 + 人工 | AI Agent 辅助分类 |
| **攻击链分析** | 手动关联 | 自动关联 + MITRE ATT&CK |
| **演练功能** | 无 | 内置紫色团队攻击模拟 |
| **响应自动化** | 剧本（Playbook）| Agent + Playbook 混合 |
| **部署方式** | 云服务为主 | 完全自托管（MIT 许可）|

---

## 与 Article 的闭环关系

AiSOC 的 AI Agent 辅助安全运营与以下 Article 形成闭环：

- **anthropic-managed-agents-decoupling-brain-hands-2026**：Anthropic 提出「解耦大脑和手」的 Agent 设计，AiSOC 正是这一原则在安全运营领域的实践——Agent（大脑）负责分类和调查建议，人类分析师（手）负责最终决策和响应执行
- **cursor-cloud-agent-four-engineering-lessons-2026**：Cursor 的云端 Agent 工程经验（上下文管理、多 Agent 协作）与 AiSOC 的安全 Agent 设计高度相关——两者都面临「如何让 Agent 在复杂环境中保持可靠性」的挑战

**闭环逻辑**：Anthropic 的 Agent 架构理论 → Cursor 的云端 Agent 工程实践 → AiSOC 的安全运营垂直场景。三者共同揭示了「Agent 在企业级复杂任务中的落地路径」。

---

## 技术亮点

1. **MIT 许可证，完全自托管**：企业可以在自己的基础设施上部署，无需担心数据出境
2. **MITRE ATT&CK 深度集成**：每条告警都有完整的攻击链映射
3. **紫色团队演练内置**：安全团队可以随时进行红蓝对抗训练
4. **FastAPI + Next.js 全栈**：现代化技术栈，便于二次开发

---

## 适用场景

- 需要**AI 辅助安全运营**的中大型企业
- 希望**自动化告警分类**减少人工负担的 SOC 团队
- 需要**紫色团队演练能力**的安全红蓝对抗训练
- 对**数据主权有要求**，必须自托管的金融机构和政府部门

---

## 总结

AiSOC 代表了 AI Agent 在安全运营领域的垂直应用。它不试图替代人类分析师，而是通过**人机协同**的方式，让 AI 处理大量重复的分类工作，人类专注于真正复杂的调查和决策。这是 AI Agent 在企业级场景落地的又一成功案例。