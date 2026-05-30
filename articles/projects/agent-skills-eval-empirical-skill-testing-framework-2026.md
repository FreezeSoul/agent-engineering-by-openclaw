# agent-skills-eval：Agent Skills 的实证评估框架，让技能改进可衡量

**来源**：[GitHub: darkrishabh/agent-skills-eval](https://github.com/darkrishabh/agent-skills-eval)（548 Stars，MIT 许可证，2026-05-06）

**核心论点**：`agent-skills-eval` 通过控制变量实验（`with_skill` vs `without_skill`）和 judge 模型评分，让 Agent Skills 的效果从"感觉有用"变成"可衡量改进"。这是 Anthropic SKILL.md 标准的配套评估基础设施。

---

## 背景：Agent Skills 的评估困境

Anthropic 推出的 [SKILL.md](https://agentskills.io) 标准让开发者可以为 AI Agent 编写领域知识技能——写一个 `SKILL.md` 文件，Agent 就能获得该领域的上下文和能力。

但有一个关键问题没有解决：**如何知道这个 Skill 真的有效？**

传统做法是主观感受——"加了这个 Skill 后，Agent 好像回答得更好了"。但这不可靠，因为：

1. **人类的确认偏误**：我们倾向于记住符合预期的结果
2. **上下文差异**：不同的输入可能触发不同的行为
3. **无法测增量**：不知道 Skill 带来了多少改进

`agent-skills-eval` 是第一个试图解决这个问题的基础设施。

---

## 核心设计：控制变量实验

`agent-skills-eval` 的方法论是科学实验的基本原则：**对比**。

### 工作流程

```
1. 准备测试用例（JSONL 格式）
2. 运行两次：
   a. with_skill：加载 SKILL.md 后运行 Agent
   b. without_skill：不加载 SKILL.md 运行 Agent
3. 收集两次的输出
4. 用 judge 模型对比两次输出的质量差异
5. 生成报告：技能是否产生了可测量的改进
```

### 评估指标

评估不是简单的"对/错"，而是多维度评分：

- **正确性**：输出是否正确解决了问题
- **完整性**：输出是否涵盖了问题的所有方面
- **专业性**：输出是否体现了 Skill 领域的专业知识
- **连贯性**：输出是否逻辑一致

---

## 技术实现

### JSONL 测试格式

```jsonl
{"input": "用户查询", "expected": "期望的输出特征", "category": "技能类别"}
{"input": "另一个查询", "expected": "期望的输出特征", "category": "技能类别"}
```

### Judge 模型评分

```typescript
interface EvalResult {
  withSkillScore: number;      // 0-100
  withoutSkillScore: number;   // 0-100
  delta: number;               // 改进幅度
  passed: boolean;             // 是否通过阈值
  reasoning: string;           // 评分理由
}
```

### 与 agent-skills.io 的集成

`agent-skills-eval` 是 agentskills.io 生态的核心组件：

- 从 agentskills.io 获取 Skill 定义
- 在本地运行评估
- 将结果提交到 agentskills.io 作为技能质量指标

---

## 使用场景

### 1. Skill 开发者：验证技能有效性

开发一个 Skill 后，运行评估确认它真的带来了改进。如果 `delta < 0`，说明 Skill 反而降低了质量，需要修改。

### 2. Skill 消费者：选择高质量技能

在 agentskills.io 上选择 Skill 时，可以查看技能的评估分数，而不仅仅是描述。

### 3. Skill 维护者：回归检测

当更新 Skill 后，运行评估确认新版本没有引入能力退化。

---

## 局限性

### 1. Judge 模型的可靠性

评估依赖 judge 模型的质量。如果 judge 本身有偏见，评估结果就不准确。

### 2. 测试用例的覆盖度

评估质量取决于测试用例的质量。如果测试用例不能代表真实使用场景，评估结果就没有意义。

### 3. 主观性与客观性的平衡

某些"专业性"指标本质上是主观的， judge 模型的评分可能因提示词不同而波动。

---

## 与 Anthropic AI-Resistant Evaluations 的关联

Anthropic 的[抗作弊评估框架](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations)揭示了一个关键问题：**LLM 可能在评估中表现好，但不一定在真实任务中真的好**。

`agent-skills-eval` 面临同样的挑战：
- 测试用例是否可能被 Skill 的上下文泄露？
- Judge 模型是否有自己的偏见？
- 如何确保评估本身不成为"刷分对象"？

Anthropic 的方案是**动态评估变体**（每次评估从参数化模板生成新题）；`agent-skills-eval` 的方案是**控制变量**——通过对比 `with_skill` 和 `without_skill` 来隔离技能的效果，而非单纯测试绝对分数。

---

## 结论

`agent-skills-eval` 是 Agent Skills 生态的重要缺失环节。它将技能质量从"主观感受"变成"可衡量数据"，让 Skill 开发者能够基于数据而非直觉进行迭代。

但评估本身也是产品，需要持续迭代。如何设计有区分度的测试用例、如何确保 judge 模型的可靠性、如何防止评估被"游戏化"——这些是下一阶段需要解决的问题。