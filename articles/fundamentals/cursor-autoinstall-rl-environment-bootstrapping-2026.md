# Cursor Autoinstall：RL 训练的环境自举法，一个模型帮另一个模型准备好起跑线

**目标读者**：构建过 Agent 系统、对 RL 训练和 Agent 可靠性有实际经验的工程师。

**核心结论**：Cursor 的 Autoinstall 解决了一个被长期忽视的问题——RL 训练中环境配置失败会导致整个训练周期报废。它的解法本质上是「让旧模型帮新模型准备好起跑线」，这个设计思想在 Agent 工程中也有广泛的应用场景：环境准备不应该由人工完成，而应该由前一个版本的 Agent 自动完成。

**一手来源**：[cursor.com/blog/bootstrapping-composer-with-autoinstall](https://cursor.com/blog/bootstrapping-composer-with-autoinstall)（2026-05-06）

---

## 问题：环境配置失败是 RL 训练的隐形杀手

RL 训练需要可运行的环境。如果起点环境破损，模型会把 tokens 浪费在调试配置上，而不是学习解决问题。在最坏的情况下，坏境会让问题根本无解——这意味着算力被浪费了，却没有产生任何 reward signal。

这个问题在云端 Agent 场景下同样存在。Cursor 云端 Agent 在开始工作前需要完成环境初始化（安装依赖、配置设置、运行基本检查），如果这一步失败，后续所有任务都无法正常执行。

> "RL training requires runnable environments, and if the environment is broken at the start, the model wastes tokens debugging setup instead of learning to solve problems. In the worst cases, a bad environment can make a problem unsolvable entirely, which ends up burning compute for no reward signal."
> — [Cursor Engineering Blog](https://cursor.com/blog/bootstrapping-composer-with-autoinstall)

Autoinstall 就是为了解决这个问题：让模型自动创建可运行的 mock 环境，而不是依赖人工配置或外部脚本。

---

## 设计：两阶段 Agent 协作

Autoinstall 的执行分为两个阶段，由两个独立的 Agent 分别完成：

### 第一阶段：Goal Setting Agent（目标设定）

给第一个 Agent 提供代码库的固定 checkout，要求它：
- 探索 README 或 makefiles，了解项目环境需求
- 尝试典型的语言特定命令（uv、clippy 等）
- 提出 10 条命令，并给出每条命令「如果环境正确配置，应该产生什么输出」的高层描述

这个 Agent 的产出是一份「环境验收标准」——不是安装手册，而是目标状态描述。

### 第二阶段：Attempt Agent（尝试执行）

给第二个 Composer Agent（Composer 1.5，上一代模型）提供：
- 环境初始状态
- 从第一阶段选出的 3 条目标命令

第二个 Agent 负责实际执行环境配置：安装依赖、mock 缺失文件、创建占位符图片、创建假的数据库表、启动所需的后台容器（如 MinIO 配置或 Docker 容器）。

完成后，验证所有 3 条命令是否运行成功且输出与目标描述匹配。如果失败，重试此阶段。如果 5 次重试后仍无法达到满意程度，丢弃该环境。

### 为什么是两阶段？

**分离关注点**。Goal Setting Agent 的职责是「定义成功」，Attempt Agent 的职责是「达到成功」。这种分离避免了一个 Agent 同时处理「目标」和「执行」时的认知负担。在 RL 场景中，这意味着 reward signal 的生成是稳定的——第一阶段保证了验收标准的一致性，第二阶段在统一标准下不断尝试。

---

## 自举：新一代用旧一代的产出作为训练数据

Autoinstall 最有意思的地方在于它的名字——Bootstrapping。

在 Composer 2 的训练中，使用了 Composer 1.5 来管理环境准备过程。这意味着 **Composer 1.5 帮助 Composer 2 准备好了起跑线**。这不是一个一次性脚本，而是一个持续的自举循环：

> "Notably, Composer 2 now scores significantly higher on Terminal-Bench (61.7% versus 47.9% for Composer 1.5), a benchmark that includes tests of a model's ability to set up developer environments. This indicates that Composer 2 will provide an improved base for autoinstall."
> — [Cursor Engineering Blog](https://cursor.com/blog/bootstrapping-composer-with-autoinstall)

Composer 2 在 Terminal-Bench（专门测试模型搭建开发环境能力的基准）上的表现从 47.9% 提升到 61.7%。这说明 Composer 2 不只在解决问题上更强，在环境准备上也更强——这让它成为下一代模型更好的「教练」。

Cursor 预期在未来训练中，Composer 实例将在更多环节发挥作用：run 管理、数据预处理、架构调整。这才是真正的自举——不是一次性的工具，而是一个可以持续改进自己的系统。

---

## 工程细节：真实项目的环境自举

Cursor 记录了一个用 autoinstall 配置真实复杂项目的实验：Celo 区块链 monorepo。

Celo 是一个大型区块链项目，有多个主要依赖项。实验过程展现了 Autoinstall 的实际能力：

**第一阶段**，Goal Setting Agent 探索项目文档和代码，找到关键的安装命令。由于项目自身文档相对稀疏，它还使用了 web 命令搜索项目的外部文档站点来找更多设置命令。

**第二阶段**，Attempt Agent 实际执行配置。任务很清晰，但模型并不知道会遇到什么问题。对于这个具体案例：
1. Agent 发现需要安装额外的依赖，比如 Foundry（一个相关的 repo），并使用 web 搜索阅读了 Foundry 的文档
2. 第一次尝试没能让测试应用运行起来
3. 在第二次尝试中，Agent 发现可以通过创建一个 mock user 来启动应用程序，满足了要求

这个案例说明了两件事：第一，即使文档不完整，模型也能通过主动搜索补全信息；第二，模型愿意创建 mock 环境来达到目标，而不只是报告「环境不可用」。

---

## 与 Agent Harness 工程的关联

Autoinstall 的设计对 Agent 工程有直接的启发价值：

### 1. 环境即基础设施

Cursor 云端 Agent 的环境准备此前是一个需要人工干预的环节。Autoinstall 证明了这个环节可以被自动化，并且自动化后的质量（通过 Terminal-Bench 衡量）超过了人工配置。这对所有构建云端 Agent 系统的团队都是一个信号：**环境准备不是 DevOps 问题，而是 Agent 系统本身的问题**。

### 2. 自举是 Agent 能力累积的路径

当一个 Agent 能够帮助下一个 Agent 更好地工作，系统的整体能力就会随时间累积。在 Multi-Agent 系统中，这实际上是一种知识蒸馏——经验丰富的 Agent（老版本模型）将环境配置的知识传递给新 Agent，而不需要人工介入。

> "We anticipate in future runs, previous Composer instances will play a large role in many other aspects of the training process, including run management, data preprocessing, and architecture tuning."
> — [Cursor Engineering Blog](https://cursor.com/blog/bootstrapping-composer-with-autoinstall)

### 3. 两阶段设计的通用性

Goal Setting Agent + Attempt Agent 的两阶段设计可以泛化到很多场景：
- **代码审查**：一个 Agent 定义代码质量标准，另一个 Agent 按标准执行审查
- **测试生成**：一个 Agent 定义覆盖范围目标，另一个 Agent 生成测试用例
- **文档生成**：一个 Agent 定义文档结构要求，另一个 Agent 按要求撰写

两阶段的核心价值在于：**让定义目标和执行目标的人分离**，这样目标定义就可以被复用、被优化、被版本化。

---

## 数据与结论

| 指标 | 数值 | 说明 |
|------|------|------|
| Terminal-Bench（Composer 1.5）| 47.9% | 环境设置能力的基准分数 |
| Terminal-Bench（Composer 2）| 61.7% | 使用 Autoinstall 自举后的提升 |
| 重试上限 | 5 次 | 达到此阈值后丢弃环境 |
| 环境准备阶段 | 2 阶段 | Goal Setting + Attempt |

**核心判断**：Autoinstall 代表了一种新的 Agent 工程思路——**不是让 Agent 适应糟糕的环境，而是让 Agent 自动准备好环境**。这个思路对于构建可靠的长程 Agent 系统（无论是训练场景还是生产场景）都有重要的借鉴价值。