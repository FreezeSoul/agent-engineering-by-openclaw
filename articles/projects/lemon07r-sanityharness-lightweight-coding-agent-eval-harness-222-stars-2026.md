# lemon07r/SanityHarness：让评测回到「测能力」本身

> **来源**：[GitHub README](https://github.com/lemon07r/SanityHarness)（2026-05-17，222 ⭐）
> **主题关联**：Anthropic「AI 抗性评估设计」→ 如何用轻量级工具实现「真正测能力」的 Agent 评测

---

## 这个项目解决了一个长期让人头疼的问题

当你在 GitHub 上看到某家厂商骄傲宣布「我们的模型在 SWE-bench 上提升了 3 个百分点」时，你有多少把握说这是真正的能力提升，而不是一次「恰好那天集群调度比较顺」？

Anthropic 在两篇工程博客里分别揭示了这个问题：

1. **《Quantifying Infrastructure Noise》**：资源配置差异可导致 6% 的分数偏差
2. **《Designing AI-resistant Technical Evaluations》**：面试题正在被 AI 攻克，需要持续迭代

两个问题叠加在一起，构成了一个尴尬的现状：**我们其实不知道自己的 Agent 到底有多强**，因为评测本身既受基础设施噪声影响，又面临被 AI 策略性绕过的风险。

SanityHarness 是一个试图「把评测拉回正轨」的尝试——一个轻量级、不依赖云服务、自托管的 Agent 编程能力评测工具。

---

## 核心设计：轻量 + 可复现 + 隔离执行

### 隔离执行：每个任务在独立 Docker 容器里跑

Agent 评测最怕的就是「任务之间互相污染」——上一个任务的缓存、环境变量、进程残留影响下一个任务。SanityHarness 用 Docker 容器为每个任务创建完全独立的执行环境，任务结束后容器销毁，不留痕迹。

这比直接在 host 上跑要干净得多，也更容易复现——只要你 Docker 镜像相同，执行结果就应该相同。

> **笔者注**：但 Docker 本身也引入了基础设施层，Anthropic 的实验表明容器资源限制策略本身就能造成 6% 的分数差异。SanityHarness 用 bubblewrap 做 agent 沙箱隔离（在容器内部再套一层），这比纯 Docker 隔离更细粒度。

### 多语言支持：Go、Rust、TypeScript、Kotlin、Dart、Zig

6 种语言、26 个任务，覆盖了系统编程（Go/Rust/Zig）和应用编程（TypeScript/Kotlin/Dart）两个方向。这比单一语言评测更有代表性——一个真正强的 coding agent 应该跨语言都有稳定表现。

### Weighted Scoring：难度因子不是均匀的

不是所有任务都同样难。SanityHarness 实现了「经验推导的难度加权」：简单任务分值低，困难任务分值高。这比「答对 N 题得 M 分」的粗暴算法更能反映真实能力分布。

### BLAKE3 验证：防止作弊的完整性检查

提交结果用 BLAKE3 做密码学哈希，eval 运行时对代码完整性做验证。这让评测结果更难被「事后修饰」。

### 支持 19 种内置 Agent

Gemini、Claude、OpenCode、Codex、Goose 等主流 coding agent 都内置支持，配置一个 `--agent` 参数就能切换。这对于做横向对比评测特别有用——同一个任务集，让所有 Agent 跑一遍，高下立判。

---

## 快速体验

```bash
# 克隆 + 构建
git clone https://github.com/lemon07r/sanityharness.git
cd sanityharness
make tools
make build

# 列出所有任务
./sanity list

# 初始化一个工作区（下载 stub 文件）
./sanity init go/bank-account

# 在 stub 上实现，然后运行测试
./sanity run go/bank-account --watch

# 评测某个 Agent
./sanity eval --agent gemini --model gemini-3-pro --tier core

# 并行跑所有任务
./sanity eval --agent claude --tier all --parallel 4
```

---

## 和 SWE-bench 的区别

| 维度 | SWE-bench | SanityHarness |
|------|-----------|---------------|
| 部署方式 | 云服务，需拉取完整数据集 | 自托管，一个 CLI 就跑起来 |
| 任务规模 | 2,000+ 真实 GitHub issues | 26 个精选任务 |
| 语言覆盖 | 主要是 Python | Go/Rust/TS/Kotlin/Dart/Zig |
| 隔离方式 | 容器（资源限制复杂）| Docker + bubblewrap 双层隔离 |
| 评测对象 | 模型 vs 真实 issue | 任意 coding agent（支持 --agent 参数切换）|
| 适用场景 | 刷榜、发 paper | 团队内部能力评估、横向对比 |

> **笔者的判断**：SanityHarness 适合「知道自己要做内部评测、但不想花大精力搭建基础设施」的团队。26 个任务不多，但覆盖了核心能力维度，用起来足够轻量。如果你想做深度研究当然还是 SWE-bench 更合适，但如果只是想「快速知道 Claude Code 和 Cursor 哪个在这个任务集上更强」，SanityHarness 几分钟就能给你答案。

---

## 与 Article 的主题关联

Anthropic 的文章探讨了「AI 抗性评估」的设计思路：问题要足够深、时间压力要真实、架构约束要有效。

SanityHarness 则是这些思路的一个具体实现：它用 Docker + bubblewrap 构造了「每个任务独立、环境干净」的评测底座，用 difficulty weighting 替代均匀计分，用 BLAKE3 防止结果篡改。

两者共同指向：**评测不是一次性设计就完事的——它需要持续迭代，且迭代方向要跟 AI 能力进化保持同步**。SanityHarness 本身的 v1.8.x 发布和 leaderboard 更新，就是这种迭代意识的体现。

---

**引用来源**：

- GitHub README: "A lightweight evaluation harness for coding agents" — https://github.com/lemon07r/SanityHarness
- Bubblewrap (沙箱隔离依赖): https://github.com/containers/bubblewrap
- SanityHarness Leaderboard (v1.8.x): https://github.com/lemon07r/sanityharness/releases