# harmony agent：首个独立复现 gpt-oss-20b 评分

> **本质**：通过逆向工程 gpt-oss-20b 的内建工具和原生 Harmony 格式，构建绕过 Chat Completions 转换的原生 agent harness，首次独立复现 OpenAI 发布的 SWE Verified 评分

> **来源**：[arXiv:2604.00362](https://arxiv.org/abs/2604.00362) | Borislav Mavrin | 2026-04-01
> **分类**：Stage 5（Tool Use） + Stage 12（Harness Engineering）
> **评分**：17/20（演进重要性高 + 技术深度高 + 知识缺口明确 + 可落地性强）

---

## 一、基本概念

### 问题背景：harness gap

SWE-bench 只指定任务，不指定 agent harness——而 harness 的选择可以导致分数相差数十个百分点。

| 模型 | 官方评测 harness | 公开 leaderboard | 差距 |
|------|-----------------|----------------|------|
| Devstral Small 2 | 68% | 56.4% | -11.6% |
| gpt-oss-120b | 62.4% | 26% | -36.4% |

这意味着：用户拿到同一个模型，换一个 harness 就可能得到完全不同的体验。

### gpt-oss 的特殊困难

1. **工具不透明**：论文只披露了 `container` 工具，其他工具（`repo_browser.*`）完全未知
2. **自定义格式**：OpenAI 训练 gpt-oss 使用的是 Harmony 格式，与标准 Chat Completions 完全不同
3. **无可用后端**：没有任何公开后端提供原生 Harmony API，所有现有方案都在做格式转换

### 核心贡献

1. **逆向工程内建工具**：发现 gpt-oss 训练分布内存在 `repo_browser.*` 工具，提取其名称和 schema
2. **原生 Harmony harness**：直接编码/解码 Harmony token 格式，跳过 Chat Completions 转换
3. **首次独立复现**：SWE Verified HIGH 60.4%（官方 60.7%）、MEDIUM 53.3%（官方 53.2%）

---

## 二、核心技术机制

### 2.1 工具逆向工程

**关键洞察**：在不给任何工具定义的情况下，gpt-oss 仍会以高置信度调用训练分布内的工具——这不是幻觉（hallucination），而是一个强先验（strong prior）。

**逆向流程**（7步）：

```
Step 1: 从原始 agent 日志中提取 5683 个 intent-reasoning-tool 元组
Step 2: 不提供任何工具定义，向模型输入 651 条 reasoning 字符串，记录工具调用
        → top prior: container.exec (4.8%), repo_browser.print_tree (3.4%), repo_browser.apply_patch (1.2%)
Step 3: 用特定 prompt 精确定位每个工具的参数 schema（每组 240 样本）
Step 4: 定义发现的工具，对比无工具 baseline 验证效果
Step 5: 直接让模型列出 repo_browser.* 工具，与实际调用交叉验证（160 样本）
Step 6: 强制模型逐个调用每个工具，收集规范 schema（405 样本，334 成功调用）
Step 7: 让模型描述每个工具的 schema，过滤虚构参数
```

**关键发现**：模型文本中提到 170+ 个 `repo_browser.*` 工具名，但大多数调用率 <2%——这些都是幻觉。真正的内建工具只有三个核心组：

| 工具 | 触发条件 | 必需参数 | 可选参数 |
|------|---------|---------|---------|
| `repo_browser.print_tree` | 默认首选动作 | - | recursive |
| `repo_browser.open_file` | 提示含文件路径+行号时（60% vs 整体21%）| - | encoding, case_sensitive, start_line, end_line |
| `repo_browser.search` | 含 "search"/"grep"/"find definition" 关键词 | - | recursive |
| `repo_browser.apply_patch` | 文件编辑（apply_patch 被模型当作内建工具调用了 860 次）| - | - |
| `container.exec` | Shell 执行 | command | - |

**重要细节**：将工具放在 developer message 中（按 OpenAI cookbook 文档）是无效的；必须放在 system message 中，工具调用率才会显著上升。

### 2.2 Harmony Native Agent Harness

**为什么格式转换是损的？**

Harmony 格式中，system/developer message 中的工具定义只需要一次；而 Chat Completions 格式每轮都会重复工具定义。对于 100+ 步的 SWE 任务，高推理强度下 token 消耗差异巨大。

**Harmony 消息格式**：

```
<|start|>header<|message|>content<|end|>

消息分三类角色：system / developer / user
模型响应分三个 channel：
  - analysis：chain-of-thought 推理
  - commentary：工具调用
  - final：面向用户的最终答案
<final> 消息终止任务
```

**Harness 异常处理系统**（关键工程细节）：

由于 gpt-oss 在 temperature=1、top_p=1 下运行，模型偶尔会偏离 Harmony 格式。Harness 通过两类异常处理恢复：

**NonTerminatingException**（可恢复，重试最多10次）：
- `HarmonyParsingError`：解析 LLM 输出失败
- `ToolCallArgParsingError`：工具参数解析失败
- `NoToolCallNoFinalMessage`：既无工具调用也无最终答案
- `ExecutionTimeoutError`：工具执行超时
- 等等

**TerminatingException**（终止任务）：
- `Submitted`：模型声明任务完成
- `LimitsExceeded`：超过步数/token 限制
- `MaxContextWindowOverflow`：上下文溢出

### 2.3 复现结果

| 基准 | gpt-oss-20b（官方）| harmony agent（本工作）|
|------|-----------------|---------------------|
| SWE Verified HIGH | 60.7% | **60.4%** |
| SWE Verified MEDIUM | 53.2% | **53.3%** |
| AIME25 (工具) | 90.4% | **91.7%** |

---

## 三、与其他概念的关系

### 工具定义位置的重要性（与 Prompt Engineering 的关系）

本文揭示了一个重要细节：**工具放在 developer message vs system message 中，调用率差异显著**。这与常见的 "developer message 优先级更高" 直觉相悖。

对于 gpt-oss，system message 是模型训练时的默认工具定义位置，模型的工具调用先验与 system message 中的定义强绑定。

### 与 Harness Engineering 的关系

本文是 Harness Engineering 的典型案例：
- 同一个模型，换 harness 分数可以差 36%
- 原生格式 vs 转换格式不只是 API 便利性问题，直接影响模型能力发挥
- 异常处理系统的设计（可恢复 vs 终止）是 harness 可靠性的关键

### 与 Tool Use 的关系

本文最重要的 Tool Use 贡献：**逆向工程方法论**——通过在无工具定义的情况下探测模型的行为先验，提取其内建工具。这比直接读模型文本（170+ 个工具名大多数是幻觉）可靠得多。

---

## 四、实践指南

### 4.1 给 Agent 开发者的启示

**1. 模型特定格式 ≠ 标准 API 格式**

如果某个模型发布时使用了自定义格式（如 Harmony），不要假设标准 Chat Completions 能完全等价地调用它。格式转换层可能悄悄吃掉模型能力。

**2. 工具定义的放置位置**

对于使用过工具训练的模型，工具定义应该放在模型训练时习惯的位置（通常是 system message），而不是 API 文档推荐的位置。

**3. 逆向工程工具先验的方法**

```
对于一个黑盒 agent 模型：
1. 构造无工具定义的 baseline prompt
2. 收集模型在多种意图下的工具调用行为
3. 统计高频工具名和参数模式
4. 交叉验证：工具名在文本中出现 ≠ 真正被调用
5. 最终在 system message 中定义经验证的工具
```

**4. 处理格式偏离的异常策略**

SWE 任务可能需要 100+ 步，任何一步的格式偏离都可能终止整个任务。设计 NonTerminatingException 的重试机制（上限10次）比直接放弃更合理。

### 4.2 给模型提供者的建议

- **披露 harness 细节**：SWE-bench 只指定任务，不指定 harness；如果模型使用了自定义格式，应该同时发布用于评测的 harness 源码
- **文档化工具定义位置**：说明工具应该放在 system message 还是 developer message

---

## 五、局限性 & 未来方向

| 局限性 | 说明 |
|--------|------|
| gpt-oss-20b 特定 | Harmony 格式和内建工具是 gpt-oss 特有的，不一定适用于其他模型 |
| 工具集可能不完整 | 170+ 个 repo_browser.* 名字中，可能还有少量未被发现的内建工具 |
| SWE-bench 数据污染 | 作者承认 SWE Verified 存在数据污染问题，但认为不在本文讨论范围内 |
| 仅覆盖 gpt-oss-20b | 对于 120b 版本，leaderboard 分数（26%）与官方（62.4%）差距更大，尚未被本研究覆盖 |

**未来方向**：
- 将 Harmony Agent 扩展到 gpt-oss-120b
- 探索其他自定义格式（Claude Format / Gemini Format）的原生 harness
- 将逆向工程方法推广到其他闭源 agent 模型

---

## 六、参考文献

1. Borislav Mavrin. *In harmony with gpt-oss*. arXiv:2604.00362, 2026.
2. SWE-agent. `https://github.com/SWE-agent/mini-swe-agent`.
3. OpenAI. `https://github.com/openai/gpt-oss`.
4. SWE-bench. `https://www.swebench.com/`.
