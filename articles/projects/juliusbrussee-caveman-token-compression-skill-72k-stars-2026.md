# JuliusBrussee/caveman：让 Claude Code 少说话、说重点的工程实践

**Stars**: 72,000+ | **License**: MIT | **Language**: JavaScript (63%), Python (27.6%)

> 🪨 *"why use many token when few token do trick"* — 同一个工程真相，两种表达方式

---

## 核心命题

**Token 效率不是可选项，而是生产级 AI Coding 的第一性工程问题。**

caveman 项目揭示了一个被广泛忽视的工程真相：在保持 100% 技术准确率的前提下，通过约束输出风格可以削减 **65-75% 的 output tokens**。这不是压缩 Prompt——这是重塑 Agent 的表达层，让"思考"和"输出"解耦。

笔者认为，Token 效率的工程价值被严重低估。多数团队还在优化模型参数和 Prompt 措辞，而真正的问题出在 Agent 的输出风格上——冗长的解释、重复的确认、过度的礼貌用语，每一项都在消耗真实的 API 成本和响应延迟。

---

## 为什么这个项目值得关注

### 1. 真实的 Benchmark 数据，不是营销话术

caveman 在 GitHub 上公开了完整的 [evals/](https://github.com/JuliusBrussee/caveman/blob/main/evals) 评估代码和 [benchmarks/](https://github.com/JuliusBrussee/caveman/blob/main/benchmarks) 原始数据。三臂对比（baseline / terse / caveman），对比基准是"Answer concisely"，而非无限制的 verbose 模式——这是诚实的对比。

| 任务类型 | Normal Tokens | Caveman Tokens | 节省比例 |
|---------|--------------|----------------|---------|
| Explain React re-render bug | 1,180 | 159 | **87%** |
| Fix auth middleware token expiry | 704 | 121 | **83%** |
| Debug PostgreSQL race condition | 1,200 | 232 | **81%** |
| Implement React error boundary | 3,454 | 456 | **87%** |
| Average (10 prompts) | 1,214 | 294 | **65%** |

平均节省 65% output tokens。按 Claude API 的收费标准，这直接影响真实的 API 账单。引用项目 README：

> "The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle..." → "New object ref each render. Inline object prop = new ref = re-render. Wrap in useMemo."

**同一修复，75% 更少 tokens，100% 相同信息。**

### 2. "Brain Still Big. Mouth Small." — 架构分离原则

caveman 提出的核心理念是 **thinking tokens 和 output tokens 的分离**：

```
Caveman only affects output tokens — thinking/reasoning tokens untouched.
Caveman no make brain smaller. Caveman make mouth smaller.
```

这不是让模型变笨，而是重塑输出的表达层。这与 OpenAI Harness Engineering 倡导的"评估器循环"形成了有趣的呼应——如果 Agent 在每次迭代中都要生成冗长的中间输出，Harness 的评估成本会线性增长。caveman 通过压缩输出层，间接降低了 Harness 的评估开销。

### 3. 学术验证：Brevity Constraints 2026 论文

2026 年 3 月的论文 *"Brevity Constraints Reverse Performance Hierarchies in Language Models"*（arXiv:2604.00025）发现：

> **"Constraining large models to brief responses improved accuracy by 26 points on certain benchmarks."**

这为 caveman 的工程实践提供了学术支撑。引用 README：

> "Verbose not always better. Sometimes less word = more correct."

笔者认为，这个发现对 AI Coding 工具链有深远影响：当前的 Agent 工具大多假设 verbose 输出 = 高可靠性，但实证数据表明这个假设在特定场景下是错误的。

### 4. 完整的产品矩阵，而非单一技能

caveman 不是一个单一脚本，而是一套 Token 效率工具集：

| 组件 | 功能 | Token 节省 |
|------|------|-----------|
| `/caveman` | 输出压缩技能（4 档：lite/full/ultra/wenyan）| 65% output |
| `/caveman-compress` | 内存文件压缩（CLAUDE.md、project notes）| 46% input |
| `caveman-shrink` | MCP 中间件，压缩工具描述 | 工具描述 |
| `cavecrew-*` | Caveman 子 Agent（investigator/builder/reviewer）| 60% multi-agent |
| `caveman-code` | 完整终端 Agent，替代 Codex | ~2× vs Codex |

其中 `caveman-shrink` 的 MCP 中间件设计特别值得关注——它将 Token 压缩能力以标准化的 Middleware 形式嵌入 MCP 协议层，这意味着任何支持 MCP 的工具（Cursor、Windsurf、Cline 等）都可以零成本接入。

---

## 技术架构解析

### 安装与触发机制

```bash
# 一行安装（macOS/Linux/Windows）
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash

# Claude Code 自动激活，无需手动触发
# Cursor/Windsurf/Cline 通过规则文件注入
```

关键机制：对于 Claude Code，caveman 写入一个 flag 文件，Agent 在会话一开始就感知到 flag，自动进入压缩模式。这是"行为契约"模式的工程实现——不依赖 Prompt 注入，而是通过文件系统状态改变 Agent 行为。

### 技能层级设计

```
/caveman lite    → 删除填充词，保留完整句子
/caveman full    → 默认 caveman 模式，句子片段化
/caveman ultra   → 电报模式，极限压缩
/caveman wenyan  → 文言文模式（中文世界适用！）
```

`wenyan` 档位对中文用户特别有趣：文言文天然简洁，同等技术内容用文言文表达 Token 消耗更低。

### 子 Agent 架构：cavecrew

```
Main Agent (caveman mode)
├── cavecrew-investigator  → 调查分析，60% fewer tokens
├── cavecrew-builder        → 代码实现，60% fewer tokens  
└── cavecrew-reviewer      → 代码审查，60% fewer tokens
```

多 Agent 协作场景中，每个 Agent 的输出都会进入下一个 Agent 的输入上下文。caveman 的子 Agent 模式通过压缩每个 Agent 的输出，延长了主上下文的有效窗口——这是 Token 效率在 Multi-Agent 场景的工程延伸。

---

## 工程启示

### Token 效率是基础设施问题

caveman 的成功揭示了一个关键认知：**Token 效率不是 Prompt 优化技巧，而是系统基础设施问题**。当 output tokens 减少 65% 时：

- API 成本直接降低 65%
- 网络传输时间缩短 65%
- 上下文窗口可容纳 3 倍更多的对话历史
- 多 Agent 协作时，每个 Agent 的输出对下游的影响更小

笔者认为，随着 Agent 任务复杂度增加，Token 效率将成为与算法效率并列的核心工程指标。

### 表达层与推理层分离

caveman 的架构设计体现了 **表达层与推理层分离** 的原则：

```
Reasoning Layer (unchanged)  → 模型内部推理，完整保留
Expression Layer (compressed) → 输出格式化，显著压缩
```

这与计算机科学中的"编译时优化"和"运行时优化"分离思想一致。模型应该完整推理，但不需要在输出中重复推理过程。

### 对 MCP 生态的补充

`caveman-shrink` 作为 MCP 中间件，解决了 MCP 协议的一个实际问题：**工具描述的 Token 开销**。MCP 协议中每个工具的描述都需要传入上下文，而一个复杂工具的描述可能占用数百 tokens。caveman-shrink 通过压缩工具描述，同时保留了功能完整性。

---

## 适用场景与局限

### 适用场景

- **高频短任务**：日常代码修改、Bug 修复，每个任务节省 60-80% tokens
- **多 Agent 协作**：每个 Agent 输出进入下游上下文，压缩效果累加
- **成本敏感项目**：Token 成本直接影响项目盈利能力的场景
- **中文项目**：wenyan 模式天然适合中文技术文档

### 不适用场景

- **需要完整解释的代码审查文档**：压缩后丢失了详细的逻辑说明
- **教学/培训材料**：caveman 输出不适合作为学习资源
- **需要保留自然语言推理过程的场景**：与"show your work"要求冲突

---

## 竞品对比

| 项目 | Stars | 核心理念 | Token 节省 | 定位 |
|------|-------|---------|-----------|------|
| **caveman** | 72K | 表达层压缩 | 65% output | 单 Agent 技能 |
| **caveman-code** | — | 完整 Agent | ~2× vs Codex | 终端 Agent |
| LangChain | 122K | RAG/Chain 框架 | — | 全栈框架 |
| MetaGPT | 61K | Multi-Agent SOP | — | Multi-Agent |

caveman 的差异化在于**极致轻量**：不是框架，不是库，是一个技能（skill），可以叠加在任何 Agent 之上来解决 Token 效率问题。这是工程上的"最小化干预"——不需要重写项目架构，只需要安装一个技能。

---

## 快速上手

```bash
# 1. 安装 caveman
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash

# 2. 在 Claude Code 中激活
/caveman

# 3. 查看 Token 节省统计
/caveman-stats

# 4. 体验极限压缩
/caveman ultra
```

---

## 一句话总结

**caveman 用工程实践证明了 Token 效率和输出质量可以共存**——65% 的 output token 节省，100% 的技术准确性，以及一个 MIT 协议的开源项目。它解决的不是模型不够聪明的问题，而是 Agent 输出太啰嗦的问题。

笔者认为，这是 2026 年最被低估的 AI Coding 工程实践之一。随着 Agent 任务复杂度增加，Token 效率将从"nice to have"变成"must have"。caveman 提前走到了这个方向。

---

*数据来源：[JuliusBrussee/caveman README](https://github.com/JuliusBrussee/caveman)，benchmark 数据和评估代码均开源在 GitHub 仓库。*
