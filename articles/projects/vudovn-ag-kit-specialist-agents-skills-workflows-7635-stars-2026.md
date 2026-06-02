# AG Kit：把专业 Agent 的「知识沉淀」变成可分发的配置单元

> **核心观点**：AG Kit 的核心创新不是另一个 Agent 框架，而是一套**让专业领域的判断力可以脱离模型独立沉淀**的模板系统。20 个专家 Agent、45 项技能、13 条工作流——全部是 Markdown 配置文件，可以用 `npx @vudovn/ag-kit init` 注入任意项目。

---

## 一、解决什么问题？

用 AI Coding 工具（Cruor/Windsurf/Claude Code）最大的痛点之一：**每次新项目都要重新解释代码规范、业务上下文和技术栈偏好**。即使模型本身很强，它对你的项目一无所知——而你花了大量 tokens 在"教它认识你的代码库"上。

AG Kit 的解法是：**把项目知识预填充进 Agent 的配置层，而不是每次会话靠 prompt 注入**。

笔者认为，这种「配置即知识」的设计思路，比单纯增加 Agent 数量更有工程价值。当专业判断力可以被版本化、分发和复用，Agent 工程才真正进入可组合、可积累的阶段。

---

## 二、核心架构拆解

### 2.1 三层配置体系

AG Kit 的核心是一个 `.agents/` 配置目录，包含三层：

| 层级 | 内容 | 数量 |
|------|------|------|
| **Agents** | 专家 Agent 的角色定义（Backend Specialist、Security Auditor、PM、QA 等）| 20 |
| **Skills** | 条件加载的领域知识模块（含 frontmatter 触发规则）| 45 |
| **Workflows** | 交互式开发流程（slash commands 的实现逻辑）| 13 |

这套三层结构的关键在于**边界清晰**：Agent 定义角色，Skills 提供知识，Workflows 编码流程。三个维度正交，可以自由组合。

### 2.2 Coordinator Mode：并行编排 + 综合

引用 README：

> *"Coordinator Mode: Multi-agent orchestration with parallel workers and synthesis, avoiding expensive sequential retries."*

Coordinator 是编排层，Worker 是执行层，最终通过 Synthesis 整合结果。这与 Claude Code Dynamic Workflows 的思路一致——**把编排逻辑从隐式的 turn-by-turn 决策变为显式的协调层**。

两者的设计哲学对比：

| 维度 | Claude Code Dynamic Workflows | AG Kit Coordinator |
|------|------------------------------|-------------------|
| 编排载体 | JavaScript 脚本 | Markdown 配置 + 协调层逻辑 |
| 执行单元 | Claude Subagent | 自定义 Specialist Agent |
| 触发方式 | `workflow` 关键词 | 自动路由分类 |
| 中间结果 | 脚本变量 | 记忆系统 |
| 规模 | 数十到数百 | 少量并行（避免昂贵顺序重试）|

笔者认为，AG Kit 的 Coordinator Mode 更轻量——不需要写 JavaScript，配置即编排。但 Claude Code 的 Dynamic Workflows 在规模上限和可编程质量门控上更强。

### 2.3 Persistent Memory：四类记忆 taxonomy

AG Kit 实现了一个 4-type 的记忆分类引擎：

```
MEMORY.md
├── 项目规范（编码风格、命名约定）
├── 业务上下文（领域模型、关键决策）
├── 技术偏好（库版本、架构选择）
└── 会话历史（上次未完成的工作）
```

这个 taxonomy 的价值在于**让记忆也有结构**，而非全部塞进一个 context window 的"总结"里。模型可以根据记忆类型选择性地加载，而不是每次都做全量压缩。

引用官方描述：

> *"Persistent Memory: A 4-type taxonomy memory engine index (MEMORY.md) to prevent re-explaining project guidelines across sessions."*

### 2.4 Context Compression 与 Conditional Skill Loading

两个机制的组合很有意思：

- **Context Compression**：自动化摘要和微压缩例程，防止长会话的 context 退化
- **Conditional Skill Loading**：通过 frontmatter 规则决定何时加载哪条 Skill，避免 context 被无关指令撑满

```yaml
---
trigger:
  files: ["**/auth/**", "**/security/**"]
  when: "security-audit mode"
---
# 这里放安全审计相关的 Skill 指令
```

这套机制直接对应 Claude Code Dynamic Workflows 面临的核心挑战——当编排规模扩大到数百个子 Agent 时，context 管理是生死线。

---

## 三、Zero-Setup Auto-Routing

AG Kit 最有意思的产品设计是**零配置的自动路由**：

```
你："Add JWT authentication to the login API"
Agent：自动加载 @security-auditor + @backend-specialist

你："Align the checkout button to center and fix dark mode"
Agent：自动加载 @frontend-specialist
```

用户不需要手动选择 Agent，系统根据任务描述自动分类并应用对应规则。这与 LangChain 的 Runnable 序列、CrewAI 的 Role Assignment 相比，**把路由决策也从显式代码变成了意图识别**。

笔者认为，这个设计反映了 Agent 使用范式的一个趋势：**从「用户指定 Agent」到「用户描述任务，系统推断 Agent」**。当框架足够了解专业领域的知识图谱，用户只需要说"做什么"，而不需要知道"派谁做"。

---

## 四、Slash Commands 工作流体系

13 条预置的交互式工作流，每条都是可执行的开发流程：

| 命令 | 做什么 |
|------|--------|
| `/brainstorm` | 结构化方案探索，在编码前对齐架构 |
| `/coordinate` | 并行协调多个 Agent 审查 |
| `/create` | 从零创建功能或完整应用 |
| `/debug` | 证据驱动的系统化调试 |
| `/deploy` | 预检查后部署到生产 |
| `/enhance` | 安全地添加或更新现有功能 |
| `/plan` | 生成结构化实施计划和检查清单 |
| `/preview` | 启动/停止/检查本地预览服务器状态 |
| `/remember` | 保存自定义项目约定到持久记忆 |
| `/status` | 生成 Agent 进展的状态报告 |
| `/test` | 生成并执行全面测试 |
| `/verify` | 通过执行而非简单检查来证明代码可用 |

这里值得关注的是 `/verify`——用执行结果而非代码审查来验证功能正确性。这是一种「测试即文档」的态度，与 Claude Code 的 `/test` 命令在精神上一致，但实现路径不同。

---

## 五、与 Claude Code Dynamic Workflows 的闭环

这两个项目的组合揭示了一个有趣的互补关系：

- **Claude Code Dynamic Workflows**：解决「大规模任务如何编排」——脚本持有控制流，context 只接收最终结果
- **AG Kit**：解决「专业判断力如何积累和分发」——Markdown 配置承载领域知识，路由系统按需加载

两者结合的理想场景：
1. 用 AG Kit 的 Specialist Agent 提供领域专业判断（安全审查、架构评审）
2. 用 Dynamic Workflows 的脚本编排这些 Agent 的协作规模和执行顺序
3. 用 AG Kit 的 Persistent Memory 记住项目上下文，避免每个工作流都重新学习代码库

> 换句话说：**AG Kit 是 Agent 的「知识层」，Dynamic Workflows 是 Agent 的「执行层」**。两者组合，才能构建真正可维护的多 Agent 系统。

---

## 六、快速上手

```bash
# 方式一：按需执行（推荐）
npx @vudovn/ag-kit init

# 方式二：全局安装
npm install -g @vudovn/ag-kit
ag-kit init

# 初始化后，.agents/ 目录注入项目根目录
# AI Coding 工具会自动识别配置
```

注意：如果是 AI-native 编辑器（Cursor/Windsurf），建议把 `.agents/` 加入 `.git/info/exclude` 而非 `.gitignore`，以保证编辑器的语言服务器能正确索引工作流。

---

## 七、一句话总结

**AG Kit 把专业 Agent 的判断力从模型权重里抽离出来，变成了可版本化、可分发、可组合的 Markdown 配置单元。** 7635 颗星背后，是开发者对「知识沉淀」这件事的强烈需求——专业判断不应该每次都从零开始。

---

## 来源

- [vudovn/ag-kit - GitHub](https://github.com/vudovn/ag-kit)（7,635 Stars）
- [AG Kit 文档 - unikorn.vn](https://ag-kit.unikorn.vn/docs)

---

*标签：multi-agent, orchestration, knowledge-management, memory-system, typescript*