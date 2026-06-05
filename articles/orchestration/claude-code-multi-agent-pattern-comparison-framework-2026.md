# Claude Code 多智能体编排模式对比：何时该用哪一种

> **来源**：MindStudio Blog — [Claude Code Dynamic Workflows vs Agent Teams vs Sub-Agents](https://www.mindstudio.ai/blog/claude-code-dynamic-workflows-vs-agent-teams-vs-sub-agents)  
> **整理日期**：2026-06-05 | **演进阶段**：Stage 7 · Orchestration | **分类**：orchestration/

---

## 核心观点

三个模式的核心区别不在于名字，而在于**底层的消息传递机制、上下文边界和执行控制模型**。选错模式的代价是真实的：任务被不必要地复杂化、token 预算提前耗尽、或者关键的协调需求根本无法实现。本文给出一个基于工程机制的决策框架，让你根据任务结构特征选择，而不是凭直觉或"agent 越多越强"的幻觉。

---

## 一、先理解四个核心变量

在对比之前，需要先明确区分三种模式的四个核心变量。它们不是独立无关的，而是相互制约的：

| 变量 | 含义 | 对三种模式的影响 |
|------|------|----------------|
| **Structure** | 层级结构——是父子树状、同级网络、还是单一自适应体 | 决定了通信路径和信息流向 |
| **Parallelism** | 并行能力——任务是否能同时执行 | 决定了规模上限和速度收益 |
| **Specialization** | 专业分工——所有 agent 能力相同，还是各有专长 | 决定了是否能处理异构任务 |
| **Coordination overhead** | 协调开销——配置和管理需要多少额外工作 | 决定了模式的启动成本和运维复杂度 |

这三个模式的选择，本质上是在这四个变量之间寻找当前任务的最优平衡点。

---

## 二、Dynamic Workflows：Claude 自己写控制程序

### 2.1 技术本质

Dynamic Workflows **不是**一个预设的多智能体模板，而是一个**代码生成系统**。Claude 根据任务目标动态编写 JavaScript 脚本来描述整个工作流程，然后由运行时（runtime）执行该脚本。

引用官方文档的描述：

> *"Claude writes its own orchestration scripts, fans work out across tens to hundreds of parallel subagents in a single session, and verifies its own results before anything reaches you."*

这与传统的"预定义 workflow"完全不同：**不是用固定流程控制 agent，而是让 agent 自己写控制程序**。

### 2.2 官方技术参数

| 约束项 | 限制值 | 说明 |
|--------|--------|------|
| **并发 agents 上限** | 16 个 | 受本地 CPU 核心数限制 |
| **单次运行总 agents 上限** | 1,000 个 | 防止失控循环 |
| **运行时用户输入** | ❌ 不支持 | 唯一暂停机制是 agent permission prompts |
| **中间结果存储** | 脚本变量 | 不进入主 context，避免污染 |
| **断点续跑** | ✅ 支持 | 同一 session 内可恢复中断的运行 |
| **Sub-agent 执行模式** | 始终 acceptEdits | 继承 session 的 tool allowlist |

### 2.3 真实案例数据

据 Anthropic 官方披露的案例：

- **Bun Zig → Rust 迁移**：约 750,000 行代码，6 天完成（首个 commit 到 merge）
- **测试通过率**：99.8% 测试套件通过
- **催化剂**：Dynamic Workflows 协调 tens to hundreds 个并行 sub-agents

> *"Work you'd normally plan in quarters can finish in days."* — Anthropic 官方博客

### 2.4 成本特性

Dynamic Workflows 的 token 消耗**显著高于普通 session**，原因有三：

1. **探索性并行分支成本叠加**：workflow 可能在多个方向并行探索，每个分支独立消耗 tokens，最终只保留一条路径
2. **脚本生成开销**：Claude 为每个任务编写编排脚本，这本身消耗 tokens
3. **多 agent 并行执行**：即使最终结果收敛，过程中的并行探索都已付费

> ⚠️ **官方警告**（来自 code.claude.com）："A workflow spawns many agents, so a single run can use meaningfully more tokens than working through the same task in conversation."

### 2.5 适用边界

**真正适合 Dynamic Workflows 的场景**：

- 任务规模足够大（多文件、跨模块、影响范围不确定）
- 质量标准可自动化验证（如：已有测试套件、明确的输出规范）
- 需要在**单一 session** 内完成，不接受人工拆解任务
- 任务中途可能需要动态调整方向（顺序依赖强）

**不适合的场景**：

- 简单修复（单文件、<20 行）：workflow 生成开销远大于收益
- 已有明确 pipeline 定义的工作：直接用 `/goal` + sub-agents 更高效
- 运行时需要人工审批每一步的：workflow 不支持中途交互
- Token 预算敏感型任务

---

## 三、Sub-Agents：独立上下文的并行计算单元

### 3.1 技术本质

Sub-agents 是 Claude Code 通过 **Task 工具** 生成的独立 Claude 实例。每个实例拥有：

- **独立的 200K token context window**
- **独立的工具访问权限**
- **独立的系统提示**
- **独立的推理轨迹**

Sub-agent 完成后**只返回一条信息**：摘要结果。所有中间工作留在 sub-agent 的 context 中，不污染主会话。

### 3.2 与 Dynamic Workflows 的核心区别

| 维度 | Dynamic Workflows | Sub-Agents |
|------|------------------|------------|
| **控制权归属** | Claude 编写脚本，控制整个流程 | 主 agent 决定何时 spawn 谁 |
| **执行环境** | 隔离 runtime，变量不进入主 context | Sub-agent 有独立 context |
| **适用任务量级** | 大规模（百千个文件，跨季度压缩） | 中等规模（可预先拆解） |
| **灵活性** | 可中途调整方向 | 任务块须预先定义 |
| **用户交互** | 几乎无（仅 permission prompts） | 可通过主 agent 干预 |

### 3.3 真实工程限制

这些限制**来自社区实战验证**，已被广泛确认：

**限制 1：Sub-agents 之间不能直接通信**
- Sub-agents 各自独立运行，不能交换中间状态
- 只能通过主 agent 中转或文件系统间接传递
- **如果你需要两个 sub-agent 协作互相验证，Sub-agents 无法做到**

**限制 2：任务摘要不能保证完整性**
- Sub-agent 完成任务后进行 summarization，将结果返回主 agent
- 这个摘要过程是**有损的**——无法保证所有关键细节被捕获

**限制 3：Sub-agents 不能嵌套 spawn**
- 一个 sub-agent 不能 spawn 其他 sub-agents
- 如果你需要多层级分解，必须在主 agent 层处理

**限制 4：每个 Sub-agent 启动时有 ~20K tokens 开销**
- 加载 CLAUDE.md、项目上下文、理解任务描述
- 对于大量微小任务，这可能比串行执行更慢

**限制 5：Context Amnesia（上下文失忆症）**
- Sub-agent 不能继承主 agent 的对话历史
- 对于需要"在前几轮基础上继续"的迭代任务，每次 spawn sub-agent 都从零开始

### 3.4 最佳实践

**文件级边界原则**：两个 sub-agent 写同一个文件会产生冲突。使用文件级或功能级分离，而非行级任务拆分。

**任务合并原则**：12 个 sub-agent 处理 4 个文件，每个 agent 的初始化开销（20K tokens）会抵消并行收益。一个 sub-agent 处理"types + interfaces + validation schemas"比三个 agent 各处理一个文件更高效。

### 3.5 适用场景判断

**适合 Sub-Agents**：

| 场景 | 原因 |
|------|------|
| 批量处理 50+ 个独立文件 | 真正并行，收益覆盖启动开销 |
| 代码审查（隔离于实现） | 需要无偏视角，context 隔离是优势 |
| 并行研究（不同数据源） | 各 sub-agent 独立探索，结果汇总 |

**不适合 Sub-Agents**：

| 场景 | 原因 |
|------|------|
| 简单一次性修复（单文件） | 启动开销大于实际工作量 |
| 需要多轮迭代的创意任务 | 每次 spawn 从零开始，无法累积 context |
| 相互依赖的任务链 | Sub-agents 无法协调，强制串行 |

---

## 四、Agent Teams：持久化专业协作网络

### 4.1 技术本质

Agent Teams 是在 Claude Code 中由 **Lead Agent** 协调的多个**持久化独立实例**。与 Sub-agents 的关键区别：

1. **通信机制**：Sub-agents 只向主 agent 报告；Agent Teams 成员之间可以**直接点对点通信**
2. **持久性**：Sub-agents 是临时工（用完即销毁）；Team members 是持久角色（跨多次任务）
3. **可观测性**：每个 Team member 在独立 tmux panel 中运行，可实时监控、干预、添加任务

### 4.2 架构组件

```
Lead Agent（你与之对话的主 session）
    │
    ├── Spawns teammates（.claude/agents/ 中定义）
    │     ├── 每个 teammate = 完整独立 Claude Code 实例
    │     ├── 每个有独立 context window
    │     └── 独立 tmux panel / iTerm2 split pane
    │
    ├── 共享任务列表（所有 agents 可见，可 claim）
    │
    └── 通信机制：
          ├── 自动消息传递（send → 自动送达）
          ├── 空闲通知（teammate 完成后自动通知 lead）
          └── 点对点消息（teammate A → teammate B by name）
```

### 4.3 上下文传递机制

**Teammates 加载的上下文**：
- ✅ CLAUDE.md（项目级）
- ✅ MCP servers
- ✅ Skills
- ✅ Spawn prompt（来自 lead 的任务描述）
- ❌ Lead 的 conversation history（**不继承**）

### 4.4 与 Sub-Agents 的架构对比

| 维度 | Sub-Agents | Agent Teams |
|------|-----------|-------------|
| **通信模式** | 单向报告主 agent | 直接 teammate ↔ teammate |
| **任务列表** | 主 agent 持有 | 共享（所有可见并可 claim）|
| **生命周期** | 临时（单任务） | 持久（跨多次任务）|
| **上下文继承** | 不继承主 agent 历史 | 继承 CLAUDE.md + skills + spawn prompt |
| **可观测性** | 黑盒（只能看到最终结果）| 每个 member 有独立 tmux panel |
| **干预能力** | 极低（只能等完成或 kill）| 可实时 stop/redirect 各 member |
| **配置持久化** | 否 | 是（.claude/agents/ 定义）|

### 4.5 真实成本数据

Agent Teams 的 token 消耗约为 **$7-8 per complex task**，远高于单 session（$0.10-0.50）和 Sub-Agents（$1-3）。

成本来源：
- 每个 teammate 独立消耗 tokens（不是共享主 context）
- Team members 之间的消息传递消耗 tokens
- Lead agent 需要持续协调

### 4.6 适用场景判断

**真正适合 Agent Teams 的场景**：

| 场景 | 原因 |
|------|------|
| 需要相互验证的工作（研究→撰写→编辑 pipeline） | Teammates 可直接通信，互相挑战 |
| 长期运行的复杂项目 | 持久化角色不需要每次重新配置 |
| 需要实时监控和干预的工作 | 每个 member 独立 panel 可观测 |
| 需要不同专业能力的任务 | 可配置不同模型和工具集 |

**不适合 Agent Teams 的场景**：

| 场景 | 原因 |
|------|------|
| 顺序依赖的文件编辑 | Agent Teams 的并发特性被浪费 |
| 同一文件的并发写 | 文件冲突风险极高 |
| 简单的一次性任务 | Team 设置成本完全不值得 |

---

## 五、决策框架：基于工程机制的判断树

### 5.1 第一层判断：任务是否可并行？

```
任务有独立、可并行的子任务？
  │
  ├─ 否 → Dynamic Workflows（唯一选择）
  │        （任务边界模糊 or 顺序依赖强）
  │
  └─ 是 → 进入第二层判断
```

### 5.2 第二层判断：是否需要 Teammate 间通信？

```
需要多个 worker 之间直接通信/互相验证？
  │
  ├─ 否 → Sub-Agents（单向报告足够）
  │        （并行独立执行，只向主 agent 汇总）
  │
  └─ 是 → Agent Teams（点对点通信必需）
           （研究→撰写→编辑 pipeline，互相对验）
```

### 5.3 第三层判断：任务持续性和复杂度

```
是长期、重复、跨 session 的复杂工作流？
  │
  ├─ 是 → Agent Teams（持久化角色配置）
  │
  └─ 否 → Sub-Agents（一次性任务，无需配置）
```

### 5.4 成本-复杂度矩阵

```
                    简单任务              复杂任务
              ┌──────────────────┬──────────────────┐
   短周期     │  Single Session   │   Sub-Agents     │
              │   (最低成本)      │  (并行加速)      │
              ├──────────────────┼──────────────────┤
   长周期     │   Sub-Agents      │  Agent Teams    │
              │  (临时并行)       │ (持久+通信)      │
              └──────────────────┴──────────────────┘
```

---

## 六、横向对比表

| 维度 | Dynamic Workflows | Sub-Agents | Agent Teams |
|------|-----------------|-----------|-------------|
| **结构** | 单一自适应体 | 父子层级 | 多专长协作 |
| **并行性** | ❌ 无（sequential）| ✅ 有 | ✅ 部分配置有 |
| **专业分工** | ❌ 无（全才）| ❌ 无（同构）| ✅ 有（异构）|
| **最佳场景** | 顺序依赖、范围不确定 | 并行化、有界任务 | 不同阶段/不同能力 |
| **设置复杂度** | 低 | 中 | 高 |
| **调试难度** | 简单 | 中等 | 较难 |
| **Context 管理** | 单一大上下文 | 隔离的小上下文 | 需要显式交接 |
| **成本** | 最低 | 中等 | 最高 |
| **失败模型** | 单点失败 | 失败隔离（局部）| 级联失败可能 |
| **用户干预点** | 仅 permission prompts | 可 kill/restart | 可实时 stop/redirect |
| **协作能力** | 无 | 单向报告 | 点对点通信 |

---

## 七、实战避坑指南

### 7.1 Sub-Agents 高频陷阱

| 陷阱 | 表现 | 解决方案 |
|------|------|---------|
| **过度碎片化** | Spawn 12 个 agent 处理 4 个文件 | 合并相关任务，每 agent 3-4 文件 |
| **忽略启动开销** | 处理 20 秒任务却花了 2 分钟启动 agent | 任务应至少 5+ 分钟才值得 sub-agent |
| **假设迭代能力** | 每次 spawn 期望 agent 记住前几轮 | 用文件持久化中间状态 |
| **文件冲突** | 两个 agent 同时写同一文件 | 文件级边界分离，提前声明 |

### 7.2 Agent Teams 高频陷阱

| 陷阱 | 表现 | 解决方案 |
|------|------|---------|
| **过早建团队** | 简单任务也建完整团队 | 从 read-only 任务开始积累经验 |
| **忽略文件冲突** | 多 member 同时编辑同一文件 | 团队成员只负责自己声明的文件范围 |
| **Lead 过早退出** | Lead 关闭后 teammates 孤立 | 确认所有 member 完成后再退出 |

### 7.3 Dynamic Workflows 高频陷阱

| 陷阱 | 表现 | 解决方案 |
|------|------|---------|
| **为简单任务触发** | 单文件修改触发完整 workflow | 用 `/goal` 替代，workflow 有最低复杂度门槛 |
| **忽略 token 警告** | 跑完后发现消耗惊人 | 事先评估，任务简单则避免 |

---

## 八、关键结论

| 模式 | 本质 | 核心优势 | 核心代价 |
|------|------|---------|---------|
| **Dynamic Workflows** | Claude 自己写控制程序 | 可处理范围不确定的大任务 | token 消耗高，无人工干预点 |
| **Sub-Agents** | 主 agent 控制的临时并行工 | 真正并行，隔离上下文 | 协调能力弱，摘要有损 |
| **Agent Teams** | 持久化专业角色网络 | 点对点通信，可实时干预 | 设置和维护成本最高 |

**行动原则**：

1. 从 Dynamic Workflows 开始，只有找到**明确理由**才升级到 Sub-Agents 或 Teams
2. 模式选择取决于**任务本身的结构特征**，而非个人偏好
3. "agent 越多越强"是误解——不必要的复杂性只会增加调试成本

---

## 参考来源

1. [Anthropic Dynamic Workflows 官方文档](https://code.claude.com/docs/en/workflows)
2. [Anthropic Agent Teams 官方文档](https://code.claude.com/docs/en/agent-teams)
3. [Anthropic Engineering: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
4. [MindStudio: Dynamic Workflows 深度解析](https://www.mindstudio.ai/blog/anthropic-dynamic-workflows-when-to-use-them)
5. [AI Crossroads: Sub-Agents 实战局限性](https://aicrossroads.substack.com/p/claude-code-subagents)
