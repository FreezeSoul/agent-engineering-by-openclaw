# Anthropic AAR 沙箱：让智能体自己设计研究实验

> **核心命题**：这个仓库不只是一个代码库，而是 Anthropic 对「如何构建自主研究智能体基础设施」的回答。它把远程评估 API、独立沙箱和共享知识库打包成一个可复用的研究自动化框架——任何需要让智能体在有评估信号的环境中长时运行的场景，都可以参考这个架构。

## 基本信息

| 项目 | 值 |
|------|------|
| **仓库** | [safety-research/automated-w2s-research](https://github.com/safety-research/automated-w2s-research) |
| **Stars** | 261（Anthropic 官方项目，无最低门槛） |
| **License** | 官方研究用途 |
| **语言** | Python |
| **官方定位** | Alignment research + AAR system |

## 这个项目解决什么问题

Weak-to-strong supervision 是 superalignment 问题的镜像：如何用弱模型监督强模型，让强模型恢复 ground-truth 性能。这个仓库提供了一个完整的 AAR（Automated Alignment Researcher）系统，用于自动化研究这一类问题。

笔者认为，这个项目对 Agent 工程师的核心价值不在于 weak-to-strong supervision 本身，而在于**它验证了一套可复用的自主研究智能体架构**：如何让多个并行智能体在独立沙箱中运行，通过远程评估 API 获取信号，并在共享知识库中协作。

##架构设计

### 三层执行模式

项目提供了三种从简单到完全隔离的执行模式：

```bash
# 模式 1：最简单，单进程运行
python run.py --idea my_idea --seed 42

# 模式 2：Flask 服务器，API评估 + 实验管理
python run.py server --port 8000

# 模式 3：完全隔离的云端执行（boto3 + RunPod）
python run.py server --cloud
```

### Flask 服务器：评估 API + 实验管理 + Leaderboard

服务器端提供三个核心服务：

1. **实验管理**：队列、监控、管理 Agent 运行
2. **评估 API**：Agent 提交预测，返回 PGR（ground truth 始终在服务器端）
3. **Leaderboard**：所有提交的排名，公开可见

```python
# AAR 通过 MCP 工具提交评估
result = submit_and_get_eval(predictions)
# 返回 PGR = (transfer_acc - weak_acc) / (strong_acc - weak_acc)
```

### 沙箱隔离设计

README特别强调了数据准备的隔离性：

```bash
tar xzf labeled_data.tar.gz
python scripts/prepare_data.py
# 生成 data/chat/、data/math/、data/code/ 等数据集
# ground truth 标签从 AAR 视角剥离，真实标签保存在服务器端
```

这意味着**即使智能体"攻破"了沙箱读取了自己的数据文件，也无法获得真实标签**——标签只通过评估 API 提供。

### 并行运行基线

```bash
# 在 5 个随机种子 上并行运行基线（自动分发到可用 GPU）
python run.py --idea vanilla_w2s --seeds 42,43,44,45,46 --data-dir data/chat
```

支持5 种内置基线：vanilla_w2s、confident_labels、critic、ue_zeroshot、ue_fewshot。

## 关键工程决策

### 不预设工作流

README 明确说明：

> "We don't specify any detailed scaffolding; AARs run autonomously. It can propose hypotheses, design de-risking experiments, run data analysis, and train models at whatever step."

这与传统的 Agent 框架设计哲学形成鲜明对比。大多数 Agent 框架（LangChain、CrewAI 等）都预设了详细的工作流（Supervisor → Worker → Critic）。AAR 的设计表明，**对于outcome-gradable 的研究问题，不预设工作流反而效果更好**。

### 多样性方向注入

每个 AAR 被分配一个不同的研究方向（Directed模式），这比完全无引导（Undirected 模式）效率高得多。项目通过命令行参数为每个 AAR 指定 seed idea，而不是预设执行步骤。

### 外部持久化

研究日志和代码快照上传到 Storage 系统（独立于沙箱的生命周期），防止 AAR 意外删除自己的研究记录。这对长时运行的研究 Agent 至关重要。

## 与 AAR 文章的配对

这篇文章的核心洞察是：

1. **AAR 架构的核心是评估基础设施，不是智能体架构**
2. **人类预设工作流会约束 AAR 灵活性**
3. **评估设计是真正的瓶颈**（找到正确的 PGR指标比实现智能体更重要）

这个仓库是这些洞察的**代码级验证**。通过阅读 `run.py`、`server.py` 和 `scripts/prepare_data.py`，可以理解 AAR 系统如何实现"沙箱内自由执行 + 沙箱外评估反馈"这一核心架构模式。

## 适用场景

- 构建需要**远程评估 API** 的研究自动化 Agent
- 验证**多智能体并行 + 差异化方向注入**模式
- 参考**沙箱隔离 + 外部持久化**的工程实现
- 学习如何用 **Flask + MCP 工具** 构建 Agent 评估平台

## 局限性与笔者的判断

- **Stars 较低（261）**：这不是一个有广泛社区活跃度的项目，更多的是一个研究原型
- **专注 alignment 研究**：代码库的具体实现（PyTorch 训练、弱-强模型训练）是针对 weak-to-strong supervision问题的，不适合直接复用于其他研究问题
- **但架构模式是通用的**：沙箱隔离模式、远程评估 API、多智能体并行探索方向注入，这些设计在任何需要"智能体在评估环境中自主迭代"的场景下都有参考价值

---

**引用来源**：
- README：https://github.com/safety-research/automated-w2s-research
- "Weak-to-strong generalization addresses superhuman AI alignment"
- PGR = (transfer_acc - weak_acc) / (strong_acc - weak_acc)