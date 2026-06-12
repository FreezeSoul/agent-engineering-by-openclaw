# ApodexAI/AgentHarness：为深度研究 Agent 量产的「评测框架」

> 本文推荐 GitHub 项目 [ApodexAI/AgentHarness](https://github.com/ApodexAI/AgentHarness)，127 Stars（2026-06-07 创建，Apache 2.0）

## 核心命题

**深度研究 Agent 的能力到底怎么测？ApodexAI 给出的答案是：需要一个专门为「Agent 执行轨迹」设计的评测框架，而不是把 LLM benchmarks 直接套在 Agent 身上。**

---

## 一、为什么需要专门的 Agent 评测框架

业界常见的问题是：把 MMLU、HLEval 这些 LLM 评测基准直接用来评价 Agent 能力。这忽略了一个关键差异——**LLM 评测考的是「答案对不对」，Agent 评测考的是「过程对不对」**。

一个深度研究 Agent 的工作轨迹可能涉及：
- 多轮网页搜索和内容提取
- 调用外部工具获取实时数据
- 交叉验证多个来源的信息冲突
- 在发现新线索时回溯并修正研究方向

这些过程的每一步都可能出错，而且错误会级联放大。传统的 benchmark 只评价最终答案，无法捕捉过程中的累积误差。

ApodexHarness 的设计思路正是针对这个差距：它不是评价模型「答对了几道题」，而是把 Agent 放在完整的 ReAct 执行轨迹中评测，捕捉整个过程的可观测性。

---

## 二、Apodex-1.0：验证为核心的深度研究模型

ApodexAI 团队同时发布了 Apodex-1.0 模型系列（从 0.8B 到 35B 参数），主打「verification-centric」——即在深度研究过程中内嵌验证机制，而非单纯追求答案生成。

从公开的 benchmark 结果看，Apodex-1.0-mini（35B-A3B）在四个深度研究基准上的表现：

| Model | BrowseComp | BrowseComp-ZH | HLE-Text | DeepSearchQA |
|-------|------------|--------------|---------|--------------|
| Apodex-1.0-mini | 71.5 | 80.6 | 46.8 | 82.2 |
| Apodex-1.0-4B-SFT | 48.8 | 63.5 | 32.9 | 69.9 |
| Apodex-1.0-2B-SFT | 27.9 | 35.0 | 18.2 | 49.9 |
| Apodex-1.0-0.8B-SFT | 13.9 | 10.7 | 11.2 | 25.8 |

值得注意的是 BrowseComp-ZH（中文浏览理解）上的表现显著高于英文基准，这可能与团队在中文深度研究场景上的针对性优化有关。

---

## 三、评测框架的工程亮点

### 3.1 标准的 ReAct 基准流程

> 引用 README：
> *"AgentHarness is the open-source evaluation harness used to reproduce the public benchmark results for Apodex-1.0 in a standard ReAct setup."*

框架使用标准的 ReAct（Reasoning + Acting）范式作为评测 pipeline，这意味着：
- 任何支持 ReAct 的 Agent 实现都可以接入这个评测框架
- 结果可复现、可对比
- 不绑定特定模型服务（通过 OpenAI-compatible API 接口）

### 3.2 完整的依赖安装流程

```bash
# 依赖管理（uv sync）
uv sync --python 3.12

# 模型服务（SGLang）
python3 -m sglang.launch_server \
  --model-path apodex/Apodex-1.0-35B-A3B \
  --tp 8 \
  --context-length 262144 \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3

# 环境配置
cp .env.example .env
# 填写 OPENAI_BASE_URL, SERPER_API_KEY, JINA_API_KEY, E2B_API_KEY

# 下载 benchmark 数据集
wget https://huggingface.co/datasets/apodex/Deep-Research-Benchmarks/resolve/main/deep_research_benchmarks_260607.zip

# 运行 smoke test
uv run python -m benchmarks.runner.run_subprocess \
  --benchmark browsecomp \
  --pipeline react_base \
  --limit 1
```

整个流程非常工程化，有完整的依赖、配置、下载和运行脚本。这比很多学术界发布的「toy benchmark」要实用得多。

### 3.3 四个基准覆盖深度研究全链路

| Benchmark | 评测维度 |
|-----------|---------|
| **BrowseComp** | 英文多跳网页搜索与信息聚合 |
| **BrowseComp-ZH** | 中文多跳网页搜索与信息聚合 |
| **HLE-Text** | 科学长文本推理（需单独申请 license）|
| **DeepSearchQA** | 深度搜索场景的问答质量 |

---

## 四、与 Round350 Eval Playbook 的关联

笔者认为，Round350 提到的「AI Agent Eval Playbook 五层评估框架」和 ApodexHarness 之间存在直接的工程印证关系：

Round350 五层框架中的「Benchmark 层」和「Harness 层」在 ApodexHarness 中都有具体实现：

- **Benchmark 层**：四个深度研究基准（BrowseComp、DeepSearchQA 等）
- **Harness 层**：标准化 ReAct 执行环境，包含工具调用追踪、轨迹记录、sandbox 执行

这说明 Agent 评测框架正在从「学术 toy benchmark」向「生产可用评测体系」演进。ApodexHarness 的出现是这一趋势的具体例证。

---

## 五、适合谁关注

**值得关注的团队/个人**：
- 需要量化评价自研 Agent 能力的团队
- 研究深度研究（Deep Research）场景的从业者
- 想建立内部 Agent 评测体系的架构师

**不一定是你的场景**：
- 只做简单问答或短文本生成的 Agent（用传统 LLM benchmark 即可）
- 尚未到需要量化评测阶段的 Agent 研发早期

---

## 六、快速上手建议

1. 先跑通 README 中的 smoke test（`--limit 1`），验证环境
2. 理解四个基准的评测维度，选择最接近你业务场景的基准
3. 如果需要自定义评测 pipeline，参考 `benchmarks/runner/run_subprocess` 的实现方式

> 引用 README：  
> *"For smaller variants, other serving options, see the Hugging Face model card."*

---

*本文为 Round351 产出 | 主题关联：evaluation/harness | Stars: 127 | Apache 2.0 | 原文引用：2 处*

**Screenshot**: 见 [GitHub](https://github.com/ApodexAI/AgentHarness)