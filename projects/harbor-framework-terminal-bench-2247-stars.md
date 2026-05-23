# Terminal-Bench：LLM 在复杂终端任务上的评测基准

> Harbor 团队开源的 Terminal-Bench 通过模拟真实 DevOps 场景，填补了 LLM 编程能力评测中「终端操作」维度的空白。

## 项目概述

**GitHub**：`https://github.com/harbor-framework/terminal-bench`
**Stars**：2,247（持续增长）
**定位**：LLM 在终端环境（Linux Shell、Docker、Git 等）中的复杂任务处理能力评测

## 核心价值

### 填补评测空白

现有 LLM 编程基准存在明显的能力维度缺失：

| 基准 | 覆盖维度 | 终端操作 |
|------|----------|----------|
| SWE-bench | Bug 修复 | ❌ |
| HumanEval | 算法实现 | ❌ |
| Terminal-Bench | **完整终端任务** | ✅ |

Terminal-Bench 模拟真实 DevOps 工作流：
- **环境配置**：Docker、Kubernetes、应用部署
- **故障排查**：日志分析、进程监控、网络诊断
- **脚本编写**：自动化运维、多工具协同
- **版本控制**：复杂 Git 操作、分支管理

### 评测方法

Terminal-Bench 采用**轨迹评测**（Trajectory Evaluation）：

1. **任务定义**：给定自然语言需求
2. **终端轨迹**：LLM 执行一系列 shell 命令
3. **结果验证**：检查文件系统状态、服务状态、输出结果

这比传统基于输出的评测更接近真实使用场景。

## 技术架构

```
terminal-bench/
├── benchmark/          # 评测任务集
│   ├── docker/         # 容器相关任务
│   ├── git/            # 版本控制任务
│   └── linux/          # 系统管理任务
├── evaluator/          # 自动评测引擎
├── human-eval/          # 人工标注数据
└── results/            # 各模型评测结果
```

## 与 Article 的闭环

**Article**（SWE-Lancer）揭示了 AI 在**代码编写**上的能力边界。
**Terminal-Bench** 则聚焦于 AI 在**终端操作**上的能力短板。

两者共同指向一个结论：**当前 LLM Agent 在复杂工程任务上的瓶颈不在于「写代码」，而在于「任务理解、工具协同、结果验证」等工程综合能力。**

## 关键数据

基于 Terminal-Bench 评测结果：

- **GPT-4o**：终端任务准确率 ~41%，复杂多步操作仅 23%
- **Claude 3.5 Sonnet**：终端任务准确率 ~38%，Git 操作相对较强
- **开源模型**（CodeLlama 等）：普遍低于 25%，工具调用能力弱

## 应用场景

1. **Agent 能力评估**：在引入 AI 终端助手前进行能力摸底
2. **模型选型参考**：对比不同模型在运维场景的表现
3. **Agent 系统设计**：识别当前架构的终端操作短板
4. **训练数据指导**：发现模型在终端操作上的具体不足

## 关联项目

- **SWE-bench** (`SWE-agent/mini-swe-agent`)：代码修复评测
- **Harbor** (`harbor-framework/harbor`)：AI 友好的终端开发环境
- **SWE-Lancer** (`openai/SWELancer-Benchmark`)：真实经济价值评测

## 结论

Terminal-Bench 提供了一个被长期忽视的评测维度——**LLM 的终端操作能力**。结合 SWE-Lancer 的经济分析，我们可以更全面地评估 AI Agent 在真实软件工程中的可用性边界。
