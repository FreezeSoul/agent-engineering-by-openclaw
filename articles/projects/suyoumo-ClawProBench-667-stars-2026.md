# ClawProBench：让 Agent Benchmark 回到真实运行时的评测框架

**仓库**: [suyoumo/ClawProBench](https://github.com/suyoumo/ClawProBench)  
**Stars**: 667 ⭐  
**分类**: evaluation

---

## 这个项目解决了一个长期让人头疼的问题

Agent 评测领域有一个根本性问题：**benchmark 在「受控环境」中运行良好，但在真实运行时（live runtime）中表现如何，没有人知道**。

SWE-bench 的测试在 GitHub Actions 中通过，但实际的 Claude Code 用户遇到的bug，benchmark 覆盖不到。ClawProBench 正是为解决这个差距而生——它在**真实的 OpenClaw runtime 中**运行 benchmark，而非隔离的测试环境。

---

## 核心价值

### 1. Live-First 评测架构

ClawProBench 的核心理念是 **"Bring Agent Benchmarks Back to the Real Runtime"**。

传统的 benchmark（如 SWE-bench）在一个独立的环境中运行测试用例。ClawProBench 则在用户实际使用的 runtime 中执行评测——这意味着：
- 真实的环境隔离和权限控制
- 真实的工具调用链和错误处理
- 真实的 Agent 与模型协作过程

> "benchmark is fully open source, it cannot fully avoid vendors optimizing specifically for the public benchmark; a leaderboard based on a closed ClawProBench dataset will be released soon"
> — README 原文，承认了开源 benchmark 的固有局限性

### 2. 多维评分体系：FinalScore

ClawProBench 引入了一个精心设计的复合评分公式：

```
FinalScore = 100 × S^0.40 × r_all^0.45 × r_any^0.15
```

其中：
- `S` = average_score（平均质量）
- `r_all` = (pass^3)^(1/3)（三次全部通过的稳定性）
- `r_any` = 1 - (1 - pass@3)^(1/3)（至少一次通过的上限）

**设计意图**：稳定重复成功权重最高，同时保留整体质量和三次中的最佳表现。这比单纯的 pass rate 更能反映真实使用体验。

### 3. 102 个活跃场景，覆盖 6 个领域

| Profile | 活跃场景数 | 用途 |
|---------|-----------|------|
| core | 26 | 默认排名套件 |
| intelligence | 95 | 扩展能力 benchmark |
| coverage | 7 | 广度和回归测试 |
| native | 36 | OpenClaw 原生 slice |
| full | 102 | 所有活跃场景 |

### 4. 可中断、可恢复的执行

```bash
# 中断后可继续
python3 run.py run --model '<MODEL>' --execution-mode live --trials 3 --continue

# 执行失败可重新入队
python3 run.py run --model '<MODEL>' --execution-mode live --trials 3 --rerun-execution-failures
```

这对于长时间运行的评测至关重要——没有人想因为网络波动从头跑一遍。

---

## 技术细节

### 目录结构

```
scenarios/          # YAML 格式 benchmark 任务
datasets/           # 种子数据 + setup/teardown 脚本
custom_checks/      # 场景特定评分逻辑
harness/           # loader, runner, scoring, reporting
```

### 核心执行命令

```bash
# 快速 smoke test（1 trial）
python3 run.py run --model '<MODEL>' --execution-mode live --benchmark-profile core --trials 1 --cleanup-agents

# 完整评测（3 trials）
python3 run.py run --model '<MODEL>' --execution-mode live --benchmark-profile core --trials 3 --cleanup-agents

# 对比报告
python3 run.py compare --results-dir results
```

---

## 与 Article 的关联

**Anthropic 的文章**揭示了 Agent 评测的核心挑战：
- 多轮交互导致错误传播和叠加
- Grader 类型的选择（Code-based / Model-based / Human）决定评测准确性
- Capability Eval 和 Regression Eval 的区分

**ClawProBench 给出的回应**：它是一个工程上可靠的 live runtime benchmark 实现——
- 用 `FinalScore = f(S, r_all, r_any)` 体现了多维质量评估
- 用 `pass^3` 和 `pass@3` 的组合体现了稳定性和上限的平衡
- 用 OpenClaw native 集成确保评测环境与实际使用环境一致

**两者共同指向**：评测不是一次性设计，而是需要在真实 runtime 中持续迭代的基础设施。

---

## 笔者的判断

### 为什么 ClawProBench 值得关注

1. **它是少数专注于「live runtime eval」的框架**：大多数 benchmark 项目关注题目质量，但 ClawProBench 关注「评测执行环境与实际使用环境的一致性」——这是一个被低估的问题。

2. **FinalScore 公式是亮点**：用 `S^0.40 × r_all^0.45 × r_any^0.15` 的指数加权来平衡质量、稳定性和上限，比简单平均更有表达力。笔者的建议：如果是企业内 部使用，可以根据场景调整指数权重（例如对稳定性要求更高的代码生成场景，可以调高 r_all 的指数）。

3. **它是 OpenClaw 生态的一部分**：如果你已经在用 OpenClaw，ClawProBench 是最自然的评测选择。

### 局限性

1. **依赖 OpenClaw runtime**：如果不是 OpenClaw 用户，集成的成本较高
2. **开源 benchmark 的固有局限**：README 原文承认「无法完全避免针对 benchmark 的优化」——这是所有开源 benchmark 的通病
3. **场景数量（102）vs SWE-bench（12k+）**：广度有待提升

---

## 快速上手

```bash
# 安装 uv（推荐）
pip install uv
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt

# 验证环境
openclaw --help

# 查看评测目录
python3 run.py inventory

# 运行 smoke test
python3 run.py run --model '<MODEL>' --execution-mode live --benchmark-profile core --trials 1 --cleanup-agents
```

---

## 引用来源

> "ClawProBench focuses on real OpenClaw execution with deterministic grading, structured reports, and benchmark-profile selection."
> — [GitHub README](https://github.com/suyoumo/ClawProBench)

> "FinalScore = 100 × S^0.40 × r_all^0.45 × r_any^0.15 — This is intended to weight stable repeated success most heavily, while still preserving overall quality and upside from best-of-3 performance."
> — [GitHub README - FinalScore metric](https://github.com/suyoumo/ClawProBench)