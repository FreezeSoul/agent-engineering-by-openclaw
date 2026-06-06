# Kiln-AI/Kiln — 4867 Stars 的 Agent Eval + Optimization 工作台

> **核心观点**：Kiln 解决的是"Agent 评估与优化割裂"的问题——大多数工具只能做单项（eval 或优化），而 Kiln 让你用同一个数据集贯穿 eval、优化、微调、RAG、合成数据生成全过程，结果在各阶段之间复合累积。
> 
> 本文是 Round 264 的项目推荐，与 Article《OpenAI 如何监控内部编码 Agent 的 misalignment》形成闭环：OpenAI 讲"如何检测 Agent 问题"，Kiln 讲"如何系统性地评估和优化 Agent"——检测与改进，缺一不可。

---

## 核心命题

**Agent 工程中最大的浪费是「评估与优化割裂」**——一个团队用 LangSmith 做 eval，用另一个工具做 prompt 优化，再用一个独立流程做微调，数据在各环节之间无法流通，每次都要重新准备测试集，每次都要手动对齐结果。

Kiln 的答案是：**一个数据集，从头流到尾**。定义一次 task，跑一遍 eval，结果自动驱动 prompt 优化、优化结果再驱动微调、微调结果再生成合成数据——所有阶段的结果在同一个界面里可追溯、可比较、可复用。

---

## 为什么这个项目值得关注

### 1. Multi-Agent 评估的完整工具链

Kiln 的 Subagents 功能让你组合多级 Agent 层级，每个 Agent 运行在独立的 focused context window。这对于评估 multi-agent 编排系统特别有价值——你可以分别追踪每个 sub-agent 的质量，然后看整体协作效果。

> "Subagents — Compose multi-agent hierarchies. Each runs in its own focused context window."

### 2. Auto-Optimize：从「手工调参」到「系统搜索」

传统 prompt 优化是手工的、一次性的。Kiln 的 Auto-Optimize 可以自动搜索最佳配置：prompt、model selection、tools、skills、subagents、parameters——全部自动组合测试，找出最优解。

这与 OpenAI 的 monitoring 形成有趣的对比：OpenAI 发现问题是靠「事后监控」，Kiln 解决问题是靠「事前自动优化」。两者结合才是完整的 Harness 工程闭环。

### 3. 本地优先 + 离线可用

> "Runs locally - bring your own API keys, or go fully offline with Ollama."

对于有数据安全要求的企业，这个特性很关键——不需要把训练数据或评估结果发送到第三方。

### 4. 团队协作 + Git 原生

> "Git-native collaboration — The app syncs to Git automatically — even for teammates who don't know what Git is."

这解决了 Agent 工程中一个实际痛点：PM、领域专家、QA 可以直接参与评估（打分、加数据），不需要懂 Git 或写代码。工程团队和业务团队的评估闭环被打通了。

---

## 技术架构亮点

### Eval Builder：10 分钟生成生产级评估集

传统 evals 需要大量手工标注数据。Kiln 的 Eval Builder 可以：
- Auto-generate evals（judge + synthetic eval dataset）
- Align to your preference in ~10 minutes

这个速度对于需要快速迭代的 Agent 开发团队非常重要。

### 合成数据生成：解决冷启动问题

很多团队不做 eval 是因为「没有足够的高质量测试数据」。Kiln 的 Synthetic Data Generation 可以在几分钟内生成 eval 数据或微调数据：

> "Generate data for evals or fine-tuning in minutes."

### MCP 支持 + 190+ 模型库

Kiln 内置 MCP（Model Context Protocol）支持，可以连接各种工具和数据源。190+ 已测试模型包括 Qwen、Llama、GPT、Gemini 等。

---

## 与 OpenAI Monitoring Article 的闭环设计

```
OpenAI Monitoring Article（Round 264）
    ↓ 讲"如何检测 Agent misalignment"
    ↓ overeager behavior / 异步→同步阻断 / 安全案例框架
    ↓
Kiln-AI/Kiln（Round 264）
    ↓ 讲"如何系统性评估和优化 Agent"
    ↓ eval builder + auto-optimize + subagents + fine-tuning
    ↓
Agent 工程闭环：检测问题（OpenAI）+ 改进系统（Kiln）
```

---

## 适合谁用

| 角色 | 使用场景 |
|------|---------|
| Agent 开发团队 | 快速迭代 prompt、优化模型选择、追踪 regression |
| AI 工程 lead | 建立团队级 eval 标准，让 PM/QA 直接参与评估 |
| 企业 AI 团队 | 本地优先部署、数据不出域、Git 原生协作 |
| 研究团队 | 快速构建 eval pipeline、合成数据生成 |

---

## 快速上手

```bash
# Python library quickstart
pip install kiln-ai

# 或下载 Desktop app（一键安装，Mac/Windows/Linux）
# https://kiln.tech/download
```

然后 follow [5-minute quickstart](https://docs.kiln.tech/getting-started/quickstart) 运行第一个 task。

---

**引用来源**：
- [Kiln-AI/Kiln GitHub](https://github.com/Kiln-AI/Kiln)（4,867 stars，MIT License）
- [Kiln Documentation](https://docs.kiln.tech)
- [Kiln Website](https://kiln.tech)