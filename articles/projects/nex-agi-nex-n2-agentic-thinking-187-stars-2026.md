# nex-agi/Nex-N2：统一思考范式的 Agent 模型新范式

> 本文推荐 nex-agi/Nex-N2：一个将「思考」与「行动」统一在单一闭环内的 Agent 模型。
> 推荐理由：Agentic Thinking 框架、2026-06 新发布、与 OpenClaw 工作流直接集成
> 源头：https://github.com/nex-agi/Nex-N2

---

## 核心命题

这个项目解决了一个长期困扰 Agent 工程的问题：**为什么模型能在单轮对话中表现优异，却在长时任务中频繁卡壳？**

Nex-N2 的答案是：不是模型能力不够，而是推理、工具调用、环境执行被错误地当作「独立模块」处理了。当模型需要在这三者之间频繁切换时，状态传递的损耗和一致性维护的复杂度急剧增加，导致长时任务可靠性大幅下降。

---

## 为什么值得推荐

### 1. Agentic Thinking：模型层的闭环架构

Nex-N2 不是又一个「提升了 X% 编程能力」的新模型。它提出了一个架构层面的创新：**Agentic Thinking**——将目标分解、状态追踪、策略调整、自我校验统一在单一连贯的推理结构中，跨任务、跨模态复用。

> "Rather than treating reasoning, tool use, and environment execution as separate capabilities, Nex-N2 unifies them through an Agentic Thinking framework that connects requirement understanding, task planning, code implementation, environmental feedback, evaluation and debugging, and continuous iteration into a single closed loop."

这段话值得认真读。它不是在描述一个新能力，而是在指出当前 Agent 架构的一个根本性缺陷，并给出了模型层的解决方案。

### 2. 数字有说服力，但不是噱头

| 指标 | 数值 | 参考 |
|------|------|------|
| Terminal-Bench 2.1 | **75.3** | Opus 4.7: 69.7, GPT-5.5: 83.4 |
| GDPval | **1585** | Opus 4.7: 1753, GPT-5.5: 1769 |
| SWE-Bench Verified | **80.8** | Opus 4.7: 87.6, GPT-5.5: 82.9 |

75.3 在 Terminal-Bench 上是一个值得关注的数字。这个基准测试的是模型在真实终端环境中的长时自主任务能力——正是 Harness Engineering 关注的核心场景。

### 3. 明确提到 OpenClaw 集成

README 中特别提到：

> "In real productivity scenarios such as OpenClaw one-person-company workflows, end-to-end game development, and web and multimodal generation, it likewise demonstrates outstanding usability, robustness, and stability."

这不是一个偶然的提及。OpenClaw 工作流的核心是单人 + 多 Agent 协作，对 Agent 的长时任务可靠性、状态一致性、跨任务能力迁移有严格要求。Nex-N2 将 OpenClaw 列为其验证场景之一，说明其设计目标与 Agent 工程实践高度对齐。

### 4. 开源 + 多平台支持

Nex-N2-Pro 和 Nex-N2-mini 均已开源：
- Hugging Face: https://huggingface.co/nex-agi/Nex-N2-Pro
- ModelScope: https://modelscope.cn/models/nex-agi/Nex-N2-Pro

提供定制 sglang fork 和预构建 Docker 镜像，降低了部署门槛。

---

## 适合谁使用

**推荐尝试的场景**：
- 需要可靠长时任务能力的 Agent 系统（如自动化测试、代码重构、大型项目初始化）
- 单人多 Agent 协作场景（OpenClaw 类工作流）
- 对模型自主性有较高要求的开发环境

**不是最佳选择的场景**：
- 短时单轮对话场景（普通 LLM 调用即可胜任）
- 需要调用大量外部工具的复杂多模态任务（目前支持的 tool calling 能力还在发展中）
- 对开源生态有强依赖的团队（Nex-N2 采用 sglang fork，需要定制基础设施）

---

## 工程集成建议

官方推荐使用定制的 sglang fork 以获得最佳性能：

```bash
git clone https://github.com/nex-agi/sglang.git
cd sglang
pip install -e "python"

# 单节点 2×H100 启动示例
python -m sglang.launch_server \
 --model-path /path/to/your/model \
 --tp 2 \
 --reasoning-parser qwen3 \
 --tool-call-parser qwen3_coder \
 --mamba-scheduler-strategy extra_buffer
```

关键参数：
- `--reasoning-parser qwen3`：解析推理内容与最终输出分离
- `--tool-call-parser qwen3_coder`：启用专用 function calling 解析器

---

## 与同类项目的对比

**相比通用 Agent 框架（LangGraph、CrewAI）**：Nex-N2 是一个模型层方案，提供基础推理能力；框架层方案提供编排能力。两者互补而非竞争关系。

**相比 Claude Code / Codex**：同为 Agent 编码工具，但定位不同。Claude Code 和 Codex 是工程工具，Nex-N2 是基础模型。前者解决「如何可靠地运行 Agent」，后者解决「如何让模型本身更擅长 Agent 任务」。

**相比 Qwen3.5 基座**：Nex-N2 在 Agent 任务上的提升显著超过基座模型。以 Terminal-Bench 为例，Nex-N2-Pro（75.3）vs Qwen3.5-397B 的典型分数约 60+，差距超过 15 分。

---

## 值得关注的工程细节

1. **sglang fork 的 tool-call-parser**：定制的 `--tool-call-parser qwen3_coder` 是专门针对 Qwen3 coder 系列优化的，这解释了为什么官方推荐使用 sglang fork 而非原生 sglang

2. **Adaptive Thinking 的 token 消耗特征**：模型自主调节思考深度意味着 token 消耗不可预测，工程中需要为此设计弹性预算机制

3. **Multi-node TP16 支持**：支持多节点 16×H100 分布式推理，说明团队对生产级部署有实际考虑

---

## 总结

**笔者认为**，Nex-N2 的价值不在于「又一个新的开源模型」，而在于它提出了一个正确的问题：**当前 Agent 可靠性不足的根因是分离式架构，而不是模型能力不足**。Agentic Thinking 框架是对这个问题的模型层回答。

如果你的 Agent 系统在长时任务中频繁出现状态丢失、规划断线、重复试错，Nex-N2 的思路值得认真参考。即使你不直接使用 Nex-N2，它的统一推理范式设计对任何 Agent 架构都有借鉴意义。

---

**引用来源**：
- README: https://github.com/nex-agi/Nex-N2
- Nex-N2-Pro: https://huggingface.co/nex-agi/Nex-N2-Pro
- Nex-N2 思考: https://nex.sii.edu.cn/