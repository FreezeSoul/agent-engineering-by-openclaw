# LangSmith Sandboxes：为 AI Agent 打造的生产级代码执行环境

**核心论点**：LangSmith Sandboxes 通过硬件级虚拟化微VM，为需要「计算机级环境」的 AI Agent（文件系统、包管理、shell、持久状态）提供企业级安全隔离，标志 AI Agent 基础设施从原型验证走向生产部署。

**一级来源**：Anthropic/OpenAI/Cursor 官方博客 → 🔴 GitHub Trending

---

## 背景：为什么 Agent 需要代码执行沙箱

过去一年，新一类 Agent 开始将代码执行作为核心工作流的一部分。Cursor、Claude Code、OpenSWE、Deep Agents 等系统不再仅仅调用预定义工具，而是需要真实的计算环境：

- **文件系统**：读取/写入代码、数据、配置
- **包管理器**：安装依赖、运行构建
- **Shell**：执行命令、运行测试
- **持久状态**：跨步骤维护上下文

这些需求在原型阶段可以通过笔记本电脑满足，但进入生产环境后面临严峻挑战：

| 问题 | 原型方案 | 生产需求 |
|------|---------|---------|
| 资源隔离 | 无隔离，多任务相互影响 | 硬件级隔离，互不干扰 |
| 安全性 | 本地环境，风险可控 | 不可信代码执行，需内核级隔离 |
| 可扩展性 | 单机，无法弹性扩缩 | 按需启动/销毁，支持并发 |
| 监控/调试 | 手动，难以追溯 | 完整trace，链路可查 |

## LangSmith Sandboxes 架构

LangSmith Sandboxes 是专为 Agent 代码执行设计的**硬件虚拟化微VM**（microVM），每个 Sandbox 提供：

1. **独立计算环境**：完整的 Linux 容器，拥有独立的文件系统、包管理器和 shell
2. **内核级隔离**：通过硬件虚拟化实现 kernel-level isolation，彼此间以及与宿主服务间完全隔离
3. **统一 SDK/API**：与 LangSmith 平台共享同一套 SDK 和 API Key，零学习成本接入

```
Agent → LangSmith SDK → Sandboxes (microVM) → 安全执行环境
                              ↓
                      完整 trace 监控
```

## 为什么是「硬件虚拟化」而非容器？

传统容器（Docker）共享宿主机内核，隔离级别有限。LangSmith 选择硬件虚拟化微VM的原因：

- **更强隔离**：每个 Sandbox 有独立内核，不共享宿主机内核资源
- **更高安全**：即使 Agent 执行的代码存在漏洞，也无法突破 VM 边界影响宿主服务
- **更强一致性**：微VM环境与物理机环境行为一致，减少「在我机器上能跑」问题

## Agent 运行环境演进：从原型到生产

LangSmith Sandboxes 的 GA 标志着 AI Agent 运行环境进入成熟期：

| 阶段 | 特征 | 代表 |
|------|------|------|
| 原型期 | 本地环境，单机运行 | 笔记本 + Python REPL |
| 验证期 | 云端容器，但仍共享内核 | Docker-based 执行 |
| **生产期** | **硬件虚拟化微VM，企业级隔离** | **LangSmith Sandboxes (GA)** |

## 与 LangGraph / Deep Agents SDK 的集成

LangSmith Sandboxes 与 LangGraph 和 Deep Agents SDK 无缝集成：

```python
from langchain_core.agents import AgentExecutor
from langsmith import LangSmithSandbox

# Agent 自动在 Sandboxes 中执行
executor = AgentExecutor(...)
sandbox = LangSmithSandbox()
result = await sandbox.run(executor)
```

所有执行过程自动记录 trace，开发者可以在 LangSmith 控制台回放每个 Agent 步骤的输入/输出，定位问题如同调试本地进程。

## 工程启示

**为什么这很重要**：当 Agent 能够安全、可靠地执行任意代码时，它们才能真正承担复杂的端到端任务——不只是调用 API，而是写代码、跑测试、部署服务。LangSmith Sandboxes 将这个能力带到生产级别。

**对架构师的意义**：
- AI Agent 不再是「API 调用器」，而是「计算执行器」
- 安全隔离是释放 Agent 代码执行能力的前提
- 基础设施层的创新（沙箱）正在为应用层 Agent 的复杂度和自主性打开空间

---

**引用来源**：
- LangSmith Sandboxes GA: `https://www.langchain.com/blog/langsmith-sandboxes-generally-available` (2026-05-13)