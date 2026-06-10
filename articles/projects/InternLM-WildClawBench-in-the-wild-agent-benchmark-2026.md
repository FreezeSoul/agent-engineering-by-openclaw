# InternLM/WildClawBench：把 AI Agent 丢进真实环境里测

> 项目地址：[github.com/InternLM/WildClawBench](https://github.com/InternLM/WildClawBench)
> 许可证：MIT
> 官方页：[internlm.github.io/WildClawBench](https://internlm.github.io/WildClawBench)

---

## 核心命题

AI Agent 的评测benchmark有一个根本缺陷：**它们在模拟环境里跑，真实环境里的模型表现完全是另一个故事**。

WildClawBench 解决的就是这个问题——它把 Agent 丢进真实的 OpenClaw 实例里：真实的 bash shell、真实的文件系统、真实的浏览器、真实的邮件和日历服务。没有 mock API，没有预设响应，没有精心清洗过的数据。如果 Web 搜索返回了意外结果，或者 Python 包抛出了文档里没写的错误——Agent 得自己处理，就像真实用户一样。

**为什么这重要**：这直接呼应了 OpenAI 评估方法论文献里提到的"Broken Problems"问题——评测任务本身无效，因为环境太干净了，掩盖了真实场景中的失败模式。

---

## 关键数据

| 指标 | 数值 |
|------|------|
| 任务数量 | 60 个手工设计的原创任务 |
| 测试模型数 | 10-19 个前沿模型 |
| 最高得分 | 51.1%（对抗性难度）|
| 环境 | 真实 OpenClaw 实例（非模拟）|
| 许可证 | MIT |

---

## 两大 Leaderboard：模型对比和 Harness 对比

WildClawBench 的设计亮点在于它提供了**两套正交的排名体系**：

### 1. Model Leaderboard（OpenClaw Harness 固定）

所有模型在同一个 OpenClaw Harness 下跑——相当于把模型放进同一个"笼子"里比谁更强。这是真正的 apples-to-apples 对比。

### 2. Harness Comparison（同一模型 + 不同 Scaffold）

同一个模型，同样的 60 个任务，跑在四种不同的 Agent Scaffold 上。这直接回答了"Harness 选什么好"这个问题——而不只是"哪个模型最强"。

**这正是 OpenAI 评估方法论的核心主张**：模型分数和 Harness 配置不可分离。WildClawBench 把这个主张变成了一个可观测的对比实验。

---

## 实测亮点

从官网数据可以看到几个有意思的现象：

- **Gemini 3.1 Pro** 在"低投入模式"下评测，分数可能不代表峰值能力——这是 WildClawBench 对 sandbagging 和 elicitation 不充分的主动披露
- **时间与成本的权衡**：不同模型在速度、成本、正确率之间有显著差异，没有免费的午餐
- **Harness 间的分数差距**：同一模型在不同 Scaffold 下得分可能有 10-20% 的波动——再次验证"Harness 不是中立的"

---

## 为什么值得看

笔者认为，WildClawBench 最有价值的设计决策是**坚持用真实环境而不是模拟环境**。

现有的很多 benchmark 测的是"模型在理想条件下的表现"，而不是"模型在真实环境里的表现"。这两者的差距在复杂任务上可能是巨大的——就像考试优秀的学生，到了工地可能连安全帽怎么戴都不知道。

WildClawBench 的 60 个任务由人工设计，强调对抗性难度（adversarial difficulty），目的是找出那些在模拟环境里隐藏很深的能力缺陷。

---

## 快速上手

```bash
# Clone
git clone https://github.com/InternLM/WildClawBench.git
cd WildClawBench

# 运行评测（需要 Docker）
docker build -t wildclawbench .
docker run wildclawbench

# 查看清理命令（如果中途中断）
docker rm -f $(docker ps -q --filter "name=wildclaw")
```

---

## 参考来源

- GitHub README: [github.com/InternLM/WildClawBench](https://github.com/InternLM/WildClawBench)
- 官方 Landing: [internlm.github.io/WildClawBench](https://internlm.github.io/WildClawBench)
- HuggingFace Dataset: [HuggingFace 上的数据集](https://huggingface.co/datasets)