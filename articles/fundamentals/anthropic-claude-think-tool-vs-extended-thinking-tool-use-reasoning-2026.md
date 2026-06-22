# Anthropic 「Think Tool」：工具调用时的专用推理空间

> 原文：[The "think" tool: Enabling Claude to stop and think](https://www.anthropic.com/engineering/claude-think-tool)  
> 来源：Anthropic Engineering Blog  
> 收录：R494（2026-06-22）

---

## 核心命题

Anthropic 发现了一个被长期忽视的 Agent 工程盲点：**模型在「生成响应前」的推理（extended thinking）和「工具调用过程中」的推理是两件不同的事**。他们专门设计了一个 `think` tool，为工具调用阶段开辟独立思考空间，在 τ-bench 评测中实现了 **54% 的相对提升**。

这个设计揭示了一个关键工程原理：**工具调用链越复杂、策略约束越严格、错误代价越高，就越需要一个在工具使用过程中插入的专用推理机制**。

---

## 一、问题：Extended Thinking 解决不了的场景

Anthropic 最初推出 extended thinking 时，给了 Claude 在「生成响应前」深度思考的能力。这对简单任务（如代码生成、数学推理）效果很好。

但他们发现了一类它覆盖不到的场景：

- **长链条工具调用**：模型需要调用多个工具，每一步的输出决定下一步行动
- **策略密集型环境**：如客服场景，有大量规则需要逐一核对
- **序贯决策**：每一步决策都建立在前一步结果上，错误会级联放大

在这些场景中，模型在「开始生成响应前」的深度思考不够用——因为它还需要处理**工具调用返回的新信息**。

---

## 二、核心设计：「Think Tool」与 Extended Thinking 的本质区别

| 维度 | Extended Thinking | Think Tool |
|------|-------------------|------------|
| **触发时机** | 生成响应**之前** | 工具调用**过程中** |
| **推理目的** | 制定行动计划 | 分析工具返回结果，决定下一步 |
| **信息范围** | 仅限用户 query | 包含工具输出的新信息 |
| **适用场景** | 简单工具调用、代码/数学 | 复杂工具链、策略核对、序贯决策 |

Think Tool 的本质是**在工具使用循环内部插入一个反思步骤**：

```
用户 query → 模型决定调用工具 → 工具返回结果 → [Think Tool: 分析结果] → 决定下一步 → ...
```

而 Extended Thinking 的流程是：

```
用户 query → [Extended Thinking: 深度思考] → 生成响应 → 调用工具 → ...
```

Anthropic 的建议是：**简单任务用 Extended Thinking，复杂工具链用 Think Tool**。

---

## 三、τ-Bench 评测结果：54% 的相对提升

Anthropic 在 τ-bench（tau-bench）上评估了 Think Tool 的效果。τ-bench 是一个客服场景评测基准，测试模型在航空公司和零售两个领域的：
- 对话导航能力
- 策略一致性
- 工具使用能力

评测指标是 **pass^k**：k 次独立尝试全部成功的概率（衡量一致性，而非单次成功率）。

### 航空公司领域结果

| 配置 | pass^1 | pass^2 | pass^3 |
|------|--------|--------|--------|
| Think Tool + 优化 Prompt | **0.570** | 0.444 | 0.384 |
| Extended Thinking | 0.412 | 0.290 | 0.232 |
| Think Tool 单独 | 0.404 | 0.254 | 0.186 |
| Baseline（无特殊处理）| 0.370 | 0.206 | 0.148 |

**关键数据**：Think Tool + 优化 Prompt 的 pass^1 为 0.570，相比 Baseline 的 0.370，**相对提升 54%**。

### Prompt 优化的关键技巧

Anthropic 发现，Think Tool 的效果可以通过优化 prompt 大幅放大。他们的 prompt 优化策略是给出**Think Tool 内思考的具体框架**：

```markdown
## Using the think tool
Before taking any action or responding to the user after receiving tool results, 
use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness
```

这相当于为模型的「思考过程」提供了一个**检查清单**，让模型不只是「想一下」，而是有结构地「核对」。

---

## 四、工程实践：Think Tool 的实现

Think Tool 的实现极其简单：

```json
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "A thought to think about."
      }
    },
    "required": ["thought"]
  }
}
```

这个实现没有任何副作用（不会获取新信息、不会修改数据库），纯粹是一个「把思考结果追加到日志」的机制。但正是这个机制，给了模型一个**显式的、结构化的推理空间**。

---

## 五、工程意义：推理时机的正交性

笔者认为，Think Tool 的设计最重要的工程启示是：**「在什么时候推理」是一个独立的设计维度**，不应该和「推理的深度」混为一谈。

当前社区普遍关注的是**推理深度**（如 extended thinking、chain of thought），但忽略了**推理时机的选择**。Anthropic 的工作表明：

1. **Pre-response 推理**（extended thinking）适合规划阶段，适合不需要外部信息的任务
2. **In-loop 推理**（think tool）适合执行阶段，适合需要处理工具返回结果的任务

这两个维度是正交的，可以叠加使用（他们的实验里 Think Tool + 优化 prompt 就是叠加效果最好的配置）。

对于 Agent 框架设计者而言，这意味着：**你的框架需要支持在工具调用循环内部插入自定义推理步骤**，而不是把推理限制在「用户 query → 最终响应」这个线性流程里。

---

## 六、适用边界

Think Tool 不是万能药。Anthropic 明确指出以下场景更适合 Extended Thinking：

- 非序贯的工具调用（简单的一次性工具使用）
- 纯代码、数学、物理类任务（不需要调用工具）
- 推理路径相对确定的场景

而以下场景是 Think Tool 的主场：

- 多步骤客服对话（每步依赖上一步结果）
- 策略密集型任务（需要逐一核对多条规则）
- 高错误代价场景（序贯决策，错误会级联）

---

## 结论

Anthropic 通过 τ-bench 的系统性评测，揭示了「工具使用过程中的推理」这一被忽视的工程设计空间。Think Tool 的实现不过是一个「无副作用的思考追加机制」，但配合 prompt 优化，在航空公司客服场景实现了 **54% 的相对提升**。

这个工作的深层含义是：**Agent 的可靠性不只是模型能力的问题，也是一个「在正确的时机给模型正确的推理空间」的工程问题**。当你发现你的 Agent 在复杂工具调用场景下容易出错时，思考一下——模型在「处理工具返回结果」这个节点上，有没有足够的推理空间？

---

**执行流程**：
1. **理解任务**：每2小时定时触发，检查仓库更新状态
2. **规划**：先读取 PENDING/REPORT/state 文件了解上下文，然后扫描新来源
3. **执行**：调用 source_tracker.py 检查源追踪状态，curl + SOCKS5 代理抓取 Anthropic 官方博客
4. **返回**：发现 2 个 NEW 来源（think-tool 和 swe-bench-sonnet），评估质量后写作 2 篇 Article
5. **整理**：更新 state.json + source_tracker + REPORT.md，执行 git commit