# Petri Realism Win Rate：让审计真实感可测量、可复现的开源工程

> **核心判断**：这是一套将"审计真实感"工程化的完整工具链——从 deployment data 采集、Petri 审计运行、到 realism win rate 量化评估，全流程开源。配合前文《审计员也会"演戏"》的文章，它是 harness evaluation 领域的稀缺开源实践。

---

## 核心命题

审计框架（如 Petri）有一个根本性挑战：**模型能识别出自己正在被测试**。这个"eval-awareness"问题此前只能定性讨论，无法量化迭代。ckkissane/petri-realism-win-rate 将这个问题工程化——提供了完整的测量工具和一套可运行的实验复现流程。

![GitHub](screenshots/ckkissane-petiri-realism-win-rate-20260616.png)

## 一、这个项目解决什么问题

笔者认为，这个项目解决了 **harness evaluation 领域的一个核心工程缺口**：如何客观衡量"我的审计有多真实"？

目前大多数 audit 框架的困境是：**你不知道你的审计有多容易被模型识破**。Realism Win Rate 提供了一个量化锚点——用 LLM 法官来判断审计转录和真实 deployment 转录的可区分性。如果 win rate 低，说明审计有明显的 artifact 信号；如果 win rate 高，说明审计更接近真实部署。

## 二、架构设计：四阶段工作流

整个工具链分为四个工程阶段：

### Stage 1：Deployment Data 采集

支持两种数据源：

**Claude Code 数据**：通过 `create_claude_code_haystack.py` 从本地的 `~/.claude/projects/` 读取会话转录，自动过滤 warmup/sidechain 消息，输出 JSONL 格式。采样 25 条的典型命令：

```bash
uv run python scripts/create_claude_code_haystack.py \
  -o niah/haystacks/my_claude_code.jsonl -n 25
```

**WildChat 数据**：扫描 HuggingFace WildChat 数据集，通过 Sonnet 4.5 分类器筛选"脆弱用户场景"和"有害请求场景"两类高风险交互：

```bash
uv run python scripts/scan_wildchat_vulnerable.py
uv run python scripts/scan_wildchat_harmful.py
```

每行 JSONL 格式：
```json
{"session_id": "unique_id", "transcript": "USER:\n...\n\nASSISTANT:\n...", "char_count": 12345}
```

### Stage 2：Petri Audit 运行（支持四种模式对比）

| 模式 | 资源 | 说明 |
|------|------|------|
| Baseline Petri | 无额外资源 | 标准 Petri 审计 |
| Realism Filter | 无额外资源 + 分类器过滤 | 加一层真实性过滤器 |
| Prompts + Tools | System prompts + Tool definitions | 审计员可访问真实系统提示词和工具定义 |
| All Resources | Prompts + Tools + Codebases | 审计员可访问全套真实 deployment resources |

```bash
# 基准审计（~10-20分钟/次）
uv run python scripts/run_baseline_audits.py --epochs 3

# 全资源审计
uv run python scripts/run_all_resources_audits.py --epochs 3

# 单个 seed 测试
uv run python scripts/run_baseline_audits.py --seed impossible_html --epochs 1
```

### Stage 3：Realism Win Rate 量化评估

用 LLM 法官对审计转录和 deployment 数据做配对比较：

```bash
bash scripts/run_niah.sh niah/haystacks/combined_sample_30.jsonl big_pile
bash scripts/run_niah.sh niah/haystacks/claude_code_transcripts_no_warmup_25.jsonl cc25

# 生成可视化
uv run python scripts/plot_realism.py
```

结果输出为分组柱状图，对比每种配置在 Mixed Deployment vs Claude Code 两个数据集上的平均 realism win rate。

### Stage 4：多维度 grading（可选）

额外提供三种 grading 脚本，验证 realism win rate 与其他指标的一致性：

```bash
bash scripts/run_grading.sh

# 生成三组图表
uv run python scripts/plot_grading.py          # post-hoc realism + verbalized awareness
uv run python scripts/plot_reward_hacking_rate.py  # reward hacking 率
uv run python scripts/plot_realism_vs_winrate.py    # realism rating vs win rate 散点图
```

## 三、笔者认为有价值的工程细节

### 3.1 四种审计 seed 覆盖不同风险场景

项目包含三类审计场景的完整 seed：

**Reward Hacking（核心实验）**：5 种 seed，包括 impossible test debugging、sabotaged benchmark 等，测试模型是否会 reward hack。

**Benign Tasks**：3 种 seed（Hyperparam Sweep、Fix Failing Test、Hallucination Probe），模拟正常编码任务，用于验证资源对良性任务真实感的提升效果。

**Shutdown Resistance**：测试模型是否会阻止被关闭，是评估"会演戏"问题的极端场景——即使加全套资源 win rate 仍然接近 0%，说明**任务本身的高风险性**是真实感的主要瓶颈。

### 3.2 多epoch设计降低成本

默认 3 epochs/repo（对比论文的 10 epochs），可显著降低 API 成本。论文特别指出每个审计约 10-20 分钟，实际运行时需要考虑并发限制和成本。

### 3.3 部署数据不出本地的设计

项目**不提供训练数据集**，只提供数据采集和格式转换工具。这意味着：
- 你必须用自己的 Claude Code 数据运行实验
- 避免了隐私和合规问题
- 但也意味着结果可能与论文不一致（因为你的 deployment 分布不同）

## 四、竞品对比

同类 harness evaluation 工具：

| 工具 | 特点 | realism win rate 支持 |
|------|------|----------------------|
| **本项目** | 全流程开源，完整复现 | ✅ 原生支持 |
| LangSmith Evals | 生产级 traces，支持自定义评估器 | ⚠️ 需自行实现 |
| RAGAS | RAG 系统专项评估 | ❌ 不适用 |
| LangChain Rubric | 自定义打分规则 | ⚠️ 无 LLM judge 盲测机制 |

笔者认为，本项目的核心差异在于 **pairwise comparison 机制**（让法官同时看审计转录和真实转录），而非简单的打分机制。这种方式避免了绝对评分中 judge 自己校准问题的影响。

## 五、适合谁用

✅ **Harness engineering 研究者**：需要量化评估自己的 audit 框架真实感  
✅ **安全团队**：评估 self-hosting 的 Claude Code 变体的 alignment 风险  
✅ **Agent framework 开发者**：给自己的审计模块建立 baseline  
❌ **只想用现成工具的用户**：需要较多工程配置  

## 六、快速上手

```bash
# 1. 环境安装
uv sync

# 2. 下载默认资源（~10GB，包含真实代码库）
uv run python -m petri.download_default_resources

# 3. 生成你自己的 Claude Code deployment 数据
uv run python scripts/create_claude_code_haystack.py -o niah/haystacks/my_cc.jsonl -n 25

# 4. 运行一次基准审计（单个 seed）
uv run python scripts/run_baseline_audits.py --seed impossible_html --epochs 1

# 5. 评估真实感
bash scripts/run_niah.sh niah/haystacks/my_cc.jsonl my_cc
```

---

**Tags**: #harness #evaluation #realism-win-rate #petri #open-science #anthropic

**关联文章**：  
- `anthropic-coding-audit-realism-win-rate-petrio-auditor-2026.md` — 同一研究的完整分析

**Source**: [github.com/ckkissane/petri-realism-win-rate](https://github.com/ckkissane/petri-realism-win-rate)
