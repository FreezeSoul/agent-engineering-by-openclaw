# Claude Code CLAUDE.md 工程实践：从配置到子 Agent 隔离

> **官方来源**：[Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files) | Claude Blog, 2025年11月25日
> **核心定位**：CLAUDE.md 不是 README，而是 Agent 的"上岗培训文档"——本文拆解 Anthropic 官方披露的 7 大最佳实践
> **关联 Article**：`anthropic-agent-skills-progressive-disclosure-2026.md`、`claude-code-2026-four-layer-architecture-boris-cherny-2026.md`、`agent-config-overload-context-files-making-agents-dumber-2026.md`

---

## 核心论点

CLAUDE.md 是 Claude Code 区别于通用 Agent 的关键工程设计——它将"瞬态 prompt 控制"转化为"持久化上下文配置"，让 Agent 在每次新会话开始时自动加载项目级规则。

但 Anthropic 官方这篇博客（2025年11月25日发布）给出的远不止"配置语法说明"——它实际上披露了一套完整的工程方法论：**从 /init 自动生成 → 4 大内容结构（架构/工具/工作流/权限）→ 5 个反模式（过多 token、敏感信息、未验证模板）→ 子 Agent 上下文隔离 → 自定义斜杠命令**。这一整套方法论回答了一个核心问题：当 Agent 部署在真实代码库中，如何在不污染上下文的前提下让 Claude 长期遵守团队规范。

笔者认为，这篇文章是理解 Claude Code "prompt-first, skill-on-top" 架构哲学的关键文档。它把"配置即代码"的工程范式从 LLM 应用层下沉到了 Agent Harness 层。

---

## 一、CLAUDE.md 的三层作用域与加载时机

Anthropic 在博客中明确指出，CLAUDE.md 不只是一个项目级文件，它有**三层作用域**：

| 作用域 | 路径 | 适用场景 | 加载时机 |
|--------|------|---------|---------|
| **仓库级** | 仓库根目录 `CLAUDE.md` | 项目约定、构建命令、测试流程 | 每次会话开始（默认） |
| **父目录级** | monorepo 父目录 `CLAUDE.md` | 共享规范（如 monorepo 工具链） | 跨子项目复用 |
| **用户级** | `~/.claude/CLAUDE.md` | 个人偏好（如输出风格、默认编辑器） | 跨所有项目生效 |

关键工程含义：**加载是不可关闭的**。CLAUDE.md 一旦存在，就成为 Claude Code 的"系统提示前缀"（system prompt prefix），每次新会话自动注入。这意味着：

1. **配置 token 是有成本的**——每一行都会进入每次会话的上下文窗口
2. **配置质量是有人评审的**——因为它进了 system prompt，会影响所有后续输出
3. **配置是版本化的**——团队成员 `git pull` 时会自动获得最新规范

与 Cursor 的 `.cursorrules`、GitHub Copilot 的 `copilot-instructions.md` 相比，CLAUDE.md 的设计更接近"代码"而非"文档"——它有加载作用域、有 token 成本约束、有版本演进机制。

---

## 二、/init 命令：自动生成 CLAUDE.md 的工程路径

Anthropic 官方明确推荐使用 `/init` 命令**从零开始**生成 CLAUDE.md：

```bash
cd your-project
claude
/init
```

`/init` 的工作流程：

1. **读取仓库元数据**：`package.json`、`pyproject.toml`、`Cargo.toml` 等构建文件
2. **扫描目录结构**：识别核心模块、入口文件、配置文件
3. **推断命令约定**：从 `scripts` 字段、CircleCI/GitHub Actions 配置提取构建/测试命令
4. **生成 starter CLAUDE.md**：包含 build commands、test instructions、key directories、architectural patterns

但 Anthropic 在博客中明确警告：**`/init` 是起点，不是终点**。

> "Think of /init as a starting point, not a finished product. The generated CLAUDE.md captures obvious patterns but may miss nuances specific to your workflow. Review what Claude produces and refine it based on your team's actual practices."

这与 Boris Cherny 在 [claude-code-2026-four-layer-architecture-boris-cherny-2026.md](articles/fundamentals/claude-code-2026-four-layer-architecture-boris-cherny-2026.md) 中披露的工作流一致——Boris 自己使用的 CLAUDE.md 只有约 2,500 个 token（100 行左右），但**每一行都经过反复迭代**。

**关键迭代信号**：`#` 键。每次发现"重复输入"的指令，就用 `#` 键记录到 CLAUDE.md——Anthropic 把这个机制叫做"摩擦点驱动演进"（friction-point-driven evolution）。

---

## 三、CLAUDE.md 的 4 大内容结构

Anthropic 官方在博客中给出 4 个核心内容板块的推荐写法：

### 1. 项目架构（Architecture）

```
## Project Architecture
- FastAPI REST API for user authentication
- SQLAlchemy ORM, PostgreSQL backend
- JWT-based auth with refresh token rotation
- Redis for session cache, RabbitMQ for async tasks
```

要点：**给 Claude 看的是目录结构而非完整代码**。一段简洁的目录树 + 关键依赖描述，比一段 README 摘录更有效——因为 Claude 需要的是"如何导航"，不是"为什么存在"。

### 2. 自定义工具（Custom Tools）

团队通常有内部脚本（如部署、测试、代码生成），Claude 默认不知道这些工具的存在。CLAUDE.md 应该明确标注：

```
## Custom Tools
- `bin/deploy.sh <env>`: Deploy to staging/prod, requires VPN
- `bin/gen-migration.py`: Generate Alembic migration from SQL diff
- `bin/load-test.sh`: Run k6 load test against staging
- Check `--help` flag for each tool before invoking
```

**为什么这很重要**：Claude 继承了你的完整 shell 环境，但如果没有指引，它会调用通用命令（如 `npm test`）而非团队特定的脚本。把"什么时候用什么工具"显式写入 CLAUDE.md，等于把团队的运维约定编码进了 Agent 的决策树。

### 3. MCP 配置（MCP Server Configuration）

这是 2026 年 Claude Code 工程实践的关键新增项。CLAUDE.md 应该包含 MCP 服务器的用法说明，例如：

```
### Slack MCP
- Posts to #dev-notifications channel only
- Use for deployment notifications and build failures
- Do not use for individual PR updates (those go through GitHub webhooks)
- Rate limited to 10 messages per hour
```

要点：**Claude 既是 MCP 客户端，又能配置 MCP 服务器**。`.mcp.json` 文件（项目级）或全局配置文件控制 MCP 连接，但 CLAUDE.md 应该说明"什么时候用哪个 server"——这是把 MCP 工具语义嵌入到 Agent 工作流的关键步骤。

### 4. 工作流（Workflows）

这是 Anthropic 博客中**最容易被忽略但工程价值最高**的部分。Claude 默认会"看到代码就改"，但团队通常有规范工作流：

```
## Standard Workflow
Before modifying code in `src/auth/`:
1. Read existing tests in `tests/auth/`
2. Construct implementation plan with risk assessment
3. Develop test plan validating:
   - Backward compatibility
   - Error handling
   - Performance regression
4. Run full test suite before commit
```

具体工作流类型示例：

- **Explore-Plan-Code-Commit**（功能开发）
- **Test-Driven Development**（算法工作）
- **Visual Iteration**（UI 改动）
- **Plan-First with Approval Gates**（关键路径）

每种工作流都要在 CLAUDE.md 显式声明——Anthropic 把这叫做"explicit workflow encoding"。

---

## 四、上下文工程：/clear、子 Agent、自定义命令

CLAUDE.md 的反义不是"不用"，而是"用得太多"。Anthropic 在博客中给出了 3 个上下文工程机制，与 CLAUDE.md 配合使用：

### /clear：会话级上下文重置

```
[Debugging authentication context window]
↓ /clear
[Implementing new API endpoint context window]
```

`/clear` 移除累积历史，保留 CLAUDE.md 配置。当任务切换时（如从调试转向实现），上下文中的无关细节会干扰后续决策。`/clear` 等于"关闭一个工作会话，开启另一个"。

### 子 Agent 上下文隔离（Subagent for Context Isolation）

这是 2026 年 Claude Code 工程实践的**范式转变**。博客原文：

> "Tell Claude to use a subagent for distinct phases of work. Subagents maintain isolated context, preventing information from earlier tasks from interfering with new analysis."

工程价值：实现支付处理器后，让 Claude "用 sub-agent 做安全审查"——实现阶段的架构细节不会污染安全审查的视角。这是**分析独立性（analytical independence）** 的工程实现。

典型场景：

| 阶段 | 主 Agent 上下文 | 子 Agent 上下文 |
|------|--------------|---------------|
| 实现 | 架构、依赖、需求 | — |
| 安全审查 | — | 仅漏洞视角 |
| 性能优化 | — | 仅瓶颈视角 |
| 文档生成 | — | 仅 API 表面 |

每个子 Agent 看到的是"该任务所需的最小上下文集合"。

### 自定义斜杠命令（Custom Slash Commands）

```
.claude/commands/performance-optimization.md
```

```
# /performance-optimization

Analyze code for:
- Database query issues (N+1, missing indexes)
- Algorithm efficiency (O(n²) loops, unnecessary iterations)
- Memory management (leaks, unbounded collections)
- Caching opportunities

Output format:
1. List issues by severity
2. Estimate performance impact
3. Suggest concrete fixes
```

Anthropic 推荐**只为真正重复的 prompt 创建命令**。博客警告：

> "Repetitive prompts waste time... Custom slash commands store these as markdown files in your `.claude/commands/` directory."

---

## 五、5 大反模式警告

Anthropic 在博客结尾列出了 5 个明确的反模式：

### 反模式 1：不要写给人类读的 README 心态

CLAUDE.md 是给 AI 队友的"上岗培训文档"，不是给人看的项目介绍。每一条都要回答"Claude 应该如何做"，而不是"这个项目是什么"。

### 反模式 2：不要过度填充

> "CLAUDE.md is added to Claude Code's context every time, so from a context engineering and prompt engineering standpoint, keep it concise."

**Boris Cherny 自己的 CLAUDE.md 只有 100 行（2,500 token）**。超过 200 行 Claude 会开始忽略规则。这与 [agent-config-overload-context-files-making-agents-dumber-2026.md](articles/fundamentals/agent-config-overload-context-files-making-agents-dumber-2026.md) 论文结论一致：堆叠 CLAUDE.md / .cursorrules / AGENTS.md 反而让 Agent 变笨。

### 反模式 3：不要包含敏感信息

> "Don't include sensitive information, API keys, credentials, database connection strings, or detailed security vulnerability information—especially if you commit to version control."

CLAUDE.md 进入 system prompt，等于把 secrets 广播给每一次会话。即便不 commit 到 git，团队成员的本地 CLAUDE.md 也可能无意上传。

### 反模式 4：不要把"通用提示"塞进 CLAUDE.md

"Be helpful", "Always be polite", "Use TypeScript" 这种"通用约定"应该放在更上层（用户级 CLAUDE.md 或 system prompt），而非项目级。每个项目的 CLAUDE.md 应该聚焦"该项目的特异性"。

### 反模式 5：不要把 CLAUDE.md 当成"一次配置"

Anthropic 明确指出："Treat customization as an ongoing practice rather than a one-time setup task." 项目演进、团队学习、新工具引入——CLAUDE.md 应该持续迭代。

---

## 六、配置即代码：与 Skills 的边界划分

一个常见困惑：CLAUDE.md 与 Skills 怎么分工？

| 维度 | CLAUDE.md | Skills |
|------|-----------|--------|
| **作用域** | 项目级持久上下文 | 跨项目可复用单元 |
| **加载时机** | 每次会话必加载 | 按需加载（渐进式披露）|
| **粒度** | 规则 + 工作流 + 工具说明 | 完整工作流（含脚本、模板）|
| **典型内容** | "如何做事" | "能做什么" |
| **演进方式** | `#` 键 + 手动编辑 | `/skill-creator` 自动生成 |

Anthropic 在 [building-agents-with-skills-equipping-agents-for-specialized-work](https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work) 中明确了边界：**CLAUDE.md 是"持久规则"，Skills 是"按需能力"**。把通用规则编码进 CLAUDE.md，把可复用工作流封装成 Skills——这两者协同工作，构成 Claude Code 的完整配置栈。

---

## 七、闭环逻辑

| 层级 | 来源 | 角色 |
|------|------|------|
| **L1 哲学层** | Boris Cherny 5 层加载作用域 + WHAT/WHY/HOW 框架 | 理论框架 |
| **L2 规范层** | Anthropic 官方博客（本文）| 工程规范与最佳实践 |
| **L3 实践层** | shanraisshan/claude-code-best-practice (58,460⭐ MIT) | 开源社区参考实现 |
| **L4 反模式层** | ETH Zurich 论文 + 社区报告 | 配置蔓延的失败模式 |

L1 → L2 → L3 → L4 形成完整的"理论 → 规范 → 实践 → 失败模式"四层 stack。每一层都来自一手来源，确保了闭环强度。

---

## 总结：CLAUDE.md 作为"工程契约"

CLAUDE.md 不是"配置"——它是**团队与 Agent 之间的工程契约**。每一行都承诺"我们会如何工作"，每一行都被自动加载、自动执行、自动审计。这与传统的 README + CONTRIBUTING.md 文档范式根本不同：

- README 是"给人看的故事"，CLAUDE.md 是"给 Agent 的指令"
- README 是可选的，CLAUDE.md 是默认加载的
- README 是项目介绍，CLAUDE.md 是工作流规范

理解了这一点，就理解了 Anthropic 把"prompt-first, skill-on-top"作为 Claude Code 架构哲学的根本原因：**配置即代码，规则即工程**。