# ReflexioAI/reflexio：让 Agent 在真实交互中自主进化的自改进 Harness

> **核心命题**：自改进 Agent 的瓶颈从来不是「学不到」，而是「学到的经验无法跨 session 传递」——Reflexio 把这个工程问题变成了一个多智能体协作问题，在 Hermes 基线上实现了 −81% 规划步骤和 −72% Token 消耗。

---

## 这个项目解决了一个什么问题

现有的 Self-Improving Agent 框架（如 Hermes-Agent）能在单个会话内通过反思优化自己的行为，但这些优化不会传递到下一个会话、另一个用户。Reflexio 的核心洞察是：Agent 进化的护城河不是「模型本身」，而是「每次交互中产生的数据价值」。

Reflexio 将这个价值提取过程工程化了：从真实用户交互中提取「用户理想响应」和「成功执行路径」，聚合成 Playbook，供同一个 Agent 在后续任务中复用。

---

## 架构设计：五步闭环

```
AI Agent → |对话| → Reflexio
Human Expert → |理想响应| → Reflexio
                ↓
         [User Profiles]      ← 个体用户的行为特征
         [Playbook Extraction]← 从交互中提取成功模式
         [Playbook Aggregation]← 跨用户聚合，形成通用知识
         [Success Evaluation] ← 判断哪些 Playbook 真正有效
```

这与 Hermes 的「单 Agent 内部反思」不同——Reflexio 是跨用户、跨会话的知识蒸馏。一个用户教给 Agent 的经验，可以通过 Playbook 聚合惠及所有用户。

---

## 关键数据：在 Hermes 基线上进一步削减 81% 规划步骤

Reflexio 的基准测试在 OpenAI 的 GDPVal 真实知识工作任务的 4/5 上，使用 Reflexio 的 Hermes Agent 相比「已经完成自学的 Hermes Agent 重跑同一任务」，实现了：

- **−81% 规划步骤**（中位数）
- **−72% Token 消耗**（中位数）

这个数字的意义在于：Reflexio 的收益是在「已经自改进过的 Agent」基础上叠加的，不是对比「没有任何自改进能力的基线 Agent」。

---

## 工程亮点

**会话级持久化**：不是靠修改 Agent 模型的权重（那需要重训练），而是通过外部 Playbook 知识库在运行时注入改进——这意味着任何 Agent（Claude Code、GPT-Code、Cursor）都可以接入。

**Claude Code 插件化**：最新版本（reflexio v2）将 Claude Code 集成迁移为独立的 `claude-smart` npm 包，通过 plugin marketplace 分发，安装门槛大幅降低。

**无幻觉的 Playbook**：Playbook 来自真实交互数据，而非合成数据——从成功执行的对话中提取，降低了「伪造成功经验」的风险。

---

## 与本轮 Article 的关联

本轮的 Anthropic MSM Article 指出：Agent 能否在 OOD 场景中泛化，取决于「是否理解了行为背后的原则」。Reflexio 提供了另一个视角：如果能从真实交互中持续提取「用户为什么认为这个做法是对的」，这些经验本身就构成了「原则的具体体现」——Playbook 不是规则清单，而是从实际判断中凝结的判断力。

两者共同指向一个方向：**Agent 的可靠性不来自更长的思考链，而来自更丰富的经验积累机制**。

---

## 一句话评价

Reflexio 把「用户反馈」变成了「Agent 的集体知识」——这不是微调，但效果接近微调，而成本接近零。

---

*Round 230 | 2026-06-04 | 主题关联：Self-Improving Agent × Experience Learning × Cross-Session Knowledge Transfer*