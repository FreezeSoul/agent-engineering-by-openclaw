# OpenAI Responses API 三元组：为什么 Shell + Skills + Compaction 是长时 Agent 的工程转折点

> 本文分析 OpenAI Responses API 的三项核心原语（Skills、Hosted Shell、Compaction）如何解决长时 Agent 的三大工程难题，以及为什么这标志了 AI Agent 从「对话助手」到「知识工作者」的产品化转折。

## 核心命题

**Shell + Skills + Compaction 不是三个独立的新功能，而是 OpenAI 给 Agent 配发的「工牌、工具箱和笔记本」——让 AI 从「回答问题的聊天机器人」变成「持续承担知识工作的数字员工」。**

当 Agent 的任务从「回答一个问题」变成「读取数据集、修改代码、写一个完整应用」，它需要：
- 持久的、可复用的工作流程（Skills）
- 一个能执行复杂命令的环境（Shell）
- 一种在长程任务中管理上下文累积的方法（Compaction）

这三者的组合，才是让 Agent 从「玩具」变成「生产线」的关键。

---

## 一、背景：为什么 Agent 长期卡在「演示」阶段

过去一年，大多数 Agent 项目都在演示阶段——在精心控制的环境里跑得很漂亮，但一上生产就出现三类问题：

1. **技能无法复用**：每个任务的 Prompt 都不一样，团队积累的经验无法结构化传承
2. **环境不完整**：Agent 说「我来帮你安装依赖」然后卡住，因为它没有真正的 Shell 执行能力
3. **上下文无限膨胀**：任务跑了 2 小时后，Agent 开始输出重复内容或丢失关键背景

OpenAI 数据显示，这些问题在 Codex 和内部 Agent 的开发过程中反复出现，于是催生了三项原语的组合设计。

---

## 二、三项原语的系统解析

### 2.1 Skills：把「专家经验」编码成可执行的工件

**核心问题**：当团队积累了一套处理某类任务的最佳实践，如何让 Agent 在正确的时间调用这套经验？

传统的做法是塞进 System Prompt——但这会导致：
- Prompt 越来越长，模型注意力被稀释
- 最佳实践无法版本化，迭代困难
- 不同 Agent 实例无法共享同一套技能库

**Skills 的设计思路**：将最佳实践编码为结构化的技能工件（Skill Artifacts），运行时由平台主动暴露给模型。

```json
{
  "name": "data-analysis",
  "description": "数据分析的标准化流程：验证数据质量 → 清洗 → 可视化 → 结论",
  "path": "/skills/data-analysis/v2/"
}
```

当 Skills 可用时，平台将每个 Skill 的 `name`、`description` 和 `path` 暴露给模型，模型在推理时可以主动查询这些技能——**不是塞进 Prompt，是让模型在需要时查询**。

> 引用原文："Think: a versioned playbook the model can consult when it's time to do real work."

OpenAI 的合作伙伴 Glean（企业搜索和知识管理平台）是最早使用 Skills 的客户之一，其场景正好说明了 Skills 的核心价值：把团队的数据分析流程、报告生成逻辑、权限检查规范结构化为可复用的技能，而不是每次都在 Prompt 里重新描述。

**Skills 的三层价值**：
- **知识保留**：团队积累的最佳实践不再随人离职而消失
- **版本控制**：技能可以迭代更新，不影响已部署的 Agent 实例
- **跨 Agent 共享**：多个 Agent 可以引用同一套技能库，保持行为一致性

### 2.2 Hosted Shell：给 Agent 一张桌子

**核心问题**：Agent 需要执行 `pip install`、`curl` 调用、写文件、运行脚本——但大多数 Agent 实现没有真正的执行环境。

常见的解法是「让 Agent 生成命令，用户手动执行」——这本质上还是人机协作，不是真正的自动化。

**Hosted Shell 的设计**：在云端提供一个托管的 Linux 容器环境，Agent 可以在里面执行任意 Shell 命令，容器自带 `/mnt/data` 持久存储。

```python
# 通过 Responses API 调用 Hosted Shell
shell_call(
    command="pip install pandas && python analyze.py",
    timeout=120
)
```

**/mnt/data 持久存储的价值**：这是最容易忽略的设计细节。传统 stateless 函数调用中，Agent 写文件、下一步就读不到；但 Hosted Shell 的 `/mnt/data` 在整个 Response 生命周期内保持持久——Agent 可以分步执行数据下载 → 处理 → 写入，下一步继续使用这些数据。

> 引用原文："The Hosted Shell and its persistent `/mnt/data` storage provide a managed environment where agents can perform complex data transformations using Python or Java without requiring the team to build and maintain custom ETL middleware for every AI project."

**Hosted Shell 的企业安全边界**：OpenAI 提供 `domain_secrets` 机制，模型运行时看到占位符（如 `$API_KEY`），由 sidecar 只向批准的目标注入真实凭据。

```bash
# 模型看到的是占位符
curl -H "Authorization: $API_KEY" https://api.example.com

# sidecar 自动替换为真实凭据（仅对批准的目的地）
```

这是企业场景中「安全地让 Agent 调用内部 API」的标准解法——模型永远不接触真实凭据，但执行时可以正常使用。

### 2.3 Compaction：防止 Agent 在长程任务中「失忆」

**核心问题**：Agent 处理一个 2 小时的长任务时，上下文窗口会累积大量中间结果、历史推理、工具输出。当上下文快满时，Agent 开始丢失重要背景，或者被迫压缩导致输出质量下降。

**Compaction 的设计**：提供 server-side 的上下文压缩机制，在模型控制下将历史内容（已完成的工作、重要的中间结果）压缩为高密度的摘要，同时保留关键上下文。

```python
# 模型可以主动触发 compaction
{
  "action": "compact",
  "reason": "已完成数据分析，进入报告生成阶段",
  "preserve": ["清洗后的数据集路径", "核心发现摘要"]
}
```

> 引用原文："Compaction in the Responses API gives you two ways to handle that."

OpenAI 提到的两种 Compaction 模式（model-controlled vs automatic），允许团队根据任务性质选择合适的压缩策略——关键是不让 Agent 在长程任务中因为上下文溢出而丧失执行力。

---

## 三、实用模式：三项原语的组合使用

OpenAI 给出了三个经过验证的组合模式（Three build patterns）：

### Pattern A: Install → Fetch → Write Artifact

```
Skills（数据清洗最佳实践）
  ↓
Hosted Shell（pip install + 数据获取）
  ↓
Compaction（保留中间结果）
  ↓
Hosted Shell（处理 + 输出）
```

适用场景：数据分析报告生成、批量数据转换、文档转换流水线。

### Pattern B: 多工具协调（Tool Orchestration）

Agent 使用 Shell 执行 Python 脚本、调用内部 API、写回数据库——所有操作都在同一个容器上下文内，不需要人机协作。

### Pattern C: 增量构建（Incremental Build）

Agent 可以将大型任务分解为多个阶段，每个阶段之间通过 Compaction 管理上下文，防止长程任务中的上下文累积失控。

---

## 四、为什么这是产品化转折点

从工程师视角，这三项原语解决了一个根本矛盾：**Agent 的执行能力和 Agent 的记忆能力之间的不匹配**。

在传统的 Chat 模式下，模型每次 Response 都是「全新」的——没有持久的工作区、没有结构化的技能复用、没有主动的上下文管理。三项原语的组合，补全了这个缺陷：

| 原语 | 解决的问题 | 类比 |
|------|-----------|------|
| Skills | 机构知识无法复用 | 员工的 SOP手册 |
| Hosted Shell | 执行能力不完整 | 员工的工作台 |
| Compaction | 记忆随任务增长而失效 | 员工的笔记本 |

三者组合后，Agent 才真正具备「承担持续性知识工作」的基础——不是问答，是工作。

**笔者认为**：这三项原语的设计有一个共同的设计哲学：**把 Agent 当作「数字员工」而不是「高级聊天机器人」**。Skills 是员工入职培训，Shell 是工作环境，Compaction 是笔记本管理。当你这样理解时，为什么需要这三者就非常清晰了。

---

## 五、关联价值

本文与仓库中以下内容形成主题关联：

- **CrewAI Token Spend Optimization（token 经济学原则层）**：长时 Agent 的成本控制是 token 消耗的核心问题，而 Shell + Skills + Compaction 的工程实现直接影响单位任务 token 消耗量
- **vLLM Semantic Router（路由系统层）**：在 mixture-of-agents 架构下，Skills 可以作为路由决策的依据之一
- **LangSmith Engine Self-Healing Eval Loop（质量工程层）**：Skills 可以编码 eval 检查逻辑，Compaction 可以保留 eval 结果历史

---

## 下轮研究线索

1. **Skills 生态扩展**：Glean 的 Skills 用法、第三方 Skills 市场
2. **Compaction 实现细节**：model-controlled vs automatic 的边界在哪里
3. **Hosted Shell 的配额和成本模型**：企业如何估算长期成本

---

**关联项目**：Onyx（开源 AI 平台，支持 50+ 索引连接器，Skills + RAG + Deep Research 组合，与 OpenAI Skills 概念形成生态互补）

---

*来源：developers.openai.com/blog/skills-shell-tips (Charlie Guo, 2026)*