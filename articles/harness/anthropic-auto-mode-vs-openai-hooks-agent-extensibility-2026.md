# Anthropic Auto Mode vs OpenAI Hooks：Agent 可编程性的两条路径

> 关键词：Hooks API、Classifier-based Permission、Auto Mode、Agent Extensibility、Programmable Harness
>
> 源头：[Anthropic Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode) + [OpenAI Codex Hooks](https://developers.openai.com/codex/hooks) + [OpenAI "Work with Codex from anywhere"](https://openai.com/index/work-with-codex-from-anywhere/)
>
> 演进阶段：Harness Engineering → Agent Extensibility

---

## 背景：两条路径的殊途同归

Anthropic 和 OpenAI 在 2026 年上半年各自推出了面向 Agent 的可扩展机制：

| 公司 | 方案 | 发布时间 | 核心定位 |
|------|------|---------|----------|
| **Anthropic** | Classifier-based Auto Mode | 2026-03-25 | ML 驱动的细粒度权限决策 |
| **OpenAI** | Hooks API (GA) | 2026-05-14 | 同步事件拦截与自定义行为注入 |

表面看起来是两个独立的功能，但深究下去会发现：**两者解决的是同一个根本矛盾——如何在保障安全的前提下让 Agent 获得足够的自主性**。

这个矛盾的本质是：Agent 的能力越强，它能造成的潜在损害就越大。传统的方案是"要么全授权、要么每次都要审批"，这两种极端都无法满足长程 Agent 的实际需求。

两条路径给出了不同的答案。

---

## Anthropic 的路径：Classifier-based Auto Mode

### 核心思想

Anthropic 的 Auto Mode 不让人类事先定义规则，而是让 Claude 自己训练一个分类器来判断哪些操作可以自动执行、哪些需要人工审批。

根据 [Anthropic 工程博客](https://www.anthropic.com/engineering/claude-code-auto-mode)：

> Auto mode uses a machine learning classifier — trained on a corpus of user decisions — to decide whether to automatically approve a tool call or present it for human review. This classifier is trained to replicate user preferences at the action level, not the session level.

关键设计：

1. **Action-level decision**：不是整会话的同意或拒绝，而是逐个工具调用判断
2. **ML classifier over rule engine**：不用 if-then 规则表，而用模型理解上下文
3. **User preference learning**：分类器从用户历史决策中学习，不是工程师预设

### 实现机制

```
User approves/rejects → Feedback signal → Classifier retraining → Future decisions
```

分类器在每次用户决策后更新权重，形成一个**用户偏好模型**。这个模型比规则引擎更灵活，能处理规则无法表达的边界情况——比如"写入 `/tmp` 的文件可以自动通过，但 `/home` 下的文件必须审批"这种上下文敏感的决策。

### 与传统方案的区别

| 维度 | 传统规则引擎 | Anthropic Auto Mode |
|------|------------|---------------------|
| 决策逻辑 | 预设 if-then | ML 分类器学习用户偏好 |
| 覆盖范围 | 只能覆盖明确定义的场景 | 能泛化到规则未覆盖的边界 |
| 更新方式 | 人工修改规则 | 从反馈信号自动更新 |
| 适用场景 | 规则清晰、场景固定 | 决策边界模糊、上下文敏感 |

---

## OpenAI 的路径：Hooks API

### 核心思想

OpenAI 的 Hooks API 是一个**同步拦截机制**，在 Codex 执行关键操作之前/之后触发用户定义的回调函数。

根据 [OpenAI 官方文档](https://developers.openai.com/codex/hooks)：

> Hooks let you run custom code at specific points during Codex's execution — like before a command runs, or after a session ends. You can use hooks to scan for secrets, run validation, log conversations, create memories, or customize behavior for specific repositories.

关键特性：

1. **Synchronous execution**：Hook 在操作执行前同步运行，可以拒绝或修改操作
2. **Event-driven**：按触发点分类（pre-execution、post-execution、session-end 等）
3. **Language agnostic**：通过 stdin/stdout 的 JSON-RPC 协议通信，任何语言都能实现

### 实现机制

```python
# Hook 实现的简单示例
def pre_execution_hook(command: str, context: dict) -> HookResult:
    if contains_secrets(command):
        return HookResult.reject("Secret detected", scan_result)
    if not approved_category(command):
        return HookResult.wait_for_approval(context)
    return HookResult.approve()
```

Hooks 本身不负责决策，它只是一个**触发框架**——真正的决策逻辑由用户编写的 Hook 实现来定义。这与 Anthropic 的 ML 分类器思路完全不同：**Anthropic 把决策逻辑内嵌到模型权重里，OpenAI 把决策逻辑留给外部实现**。

### 与 Anthropic 的互补性

| 维度 | Anthropic Auto Mode | OpenAI Hooks API |
|------|---------------------|------------------|
| 决策位置 | 模型内部（Classifier） | 模型外部（Hook 函数） |
| 决策方式 | ML 模型预测 | 用户自定义代码 |
| 更新方式 | 从反馈信号学习 | 人工修改 Hook 代码 |
| 可控性 | 黑盒（不可解释的权重） | 白盒（代码逻辑透明） |
| 灵活性 | 高（能处理模糊边界） | 中（需要编程） |

两者实际上可以组合：**用 Hooks 实现 Anthropic 那种分类器的接口**，让外部 ML 模型做决策，Hooks 只负责转发。

---

## 为什么这两条路径同时出现

2026 年这个时间点，Anthropic 和 OpenAI 都选择在同一类问题上发力，根本原因是 **Agent 的时间尺度在变长**。

早期 Agent 的典型场景是"单次请求 → 单次响应"，人类实时监控。但当 Agent 开始处理"数小时的长程任务"时：

- 人类无法实时陪伴整个过程
- 每个决策点都让人审批会阻塞工作流
- 但完全不干预又可能导致不可逆的损害

这就产生了对"**选择性自动化决策**"的强需求——不是全自动化，也不是全人工，而是让 AI 学着判断"这个操作安全吗"。

两条路径的区别在于**实现这个判断的方式不同**：

| 判断方式 | Anthropic | OpenAI |
|---------|-----------|--------|
| 谁做判断 | 模型内 Classifier | 外部 Hook 函数 |
| 怎么更新 | 从反馈自动学习 | 人工修改代码 |
| 优点 | 泛化能力强 | 可控性强、可解释 |
| 缺点 | 黑盒、不透明 | 需要编程、覆盖度取决于开发者 |

---

## Hooks API 的企业级场景

根据 [OpenAI "Work with Codex from anywhere"](https://openai.com/index/work-with-codex-from-anywhere/)，Hooks 的实际应用场景包括：

### 1. Secrets 扫描（Pre-execution）

在命令执行前扫描是否包含 API key、password 或其他敏感信息：

```python
def pre_execution_hook(command: str, context: dict) -> HookResult:
    if scan_for_secrets(command):
        return HookResult.reject("Secrets detected")
    return HookResult.approve()
```

### 2. Repository-specific 自定义

对特定仓库应用特定规则：

```python
def pre_execution_hook(command: str, context: dict) -> HookResult:
    repo = context['repository']
    if repo == 'production-api':
        if command.startswith('rm') or command.startswith('drop'):
            return HookResult.wait_for_approval(context)
    return HookResult.approve()
```

### 3. Conversation Memory

在 session 结束后自动提取关键信息写入外部记忆系统：

```python
def session_end_hook(session: dict) -> HookResult:
    memory = extract_key_decisions(session)
    write_to_memory_system(memory)
    return HookResult.approve()
```

### 4. Audit Logging

记录所有操作用于合规审计：

```python
def post_execution_hook(command: str, result: dict) -> HookResult:
    log_event({
        'command': command,
        'result': result,
        'timestamp': now(),
        'user': current_user()
    })
    return HookResult.approve()
```

---

## 两条路径的收敛方向

虽然 Anthropic 和 OpenAI 选择了不同的技术路线，但从功能上看，两者的**最终目标一致**：**让 Agent 在"完全自主"和"完全受控"之间找到动态平衡点**。

这个平衡点不是固定的，而是：

- **随时间收敛**：Anthropic 的 Classifier 从用户反馈中学习，逐渐从"每次都问"收敛到"只在必要时问"
- **随场景切换**：OpenAI 的 Hooks 可以针对不同仓库设置不同规则，在 dev 仓库宽松、在 prod 仓库严格

两条路径各有适用场景：

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 决策边界清晰、规则固定 | OpenAI Hooks | 代码透明、易维护 |
| 决策边界模糊、上下文复杂 | Anthropic Auto Mode | ML 泛化能力强 |
| 需要跨平台统一接口 | OpenAI Hooks（JSON-RPC） | 语言无关 |
| 需要从隐式反馈中学习 | Anthropic Auto Mode | 端到端梯度更新 |

---

## 笔者的判断

Anthropic 的方案更有野心——它试图让模型自己学会判断"这件事该不该做"。这在方向上是正确的，因为手工规则永远无法覆盖所有场景。

但 **Auto Mode 的问题在于它是一个黑盒**：当分类器拒绝某个操作时，用户不知道**为什么**被拒绝，也无法直接干预决策逻辑。对于需要合规审计的企业场景，这是致命的缺陷。

OpenAI 的 Hooks 更务实——它不试图让模型学会判断，而是把判断框架暴露给开发者，让企业在上面构建自己的决策逻辑。这种方案的缺点是覆盖度取决于开发者的水平，但优点是**完全可控、可审计**。

对于**生产级 Agent 部署**，笔者的判断是：**OpenAI Hooks 是更安全的起点**，但长期看 **Anthropic 的 Auto Mode 方向代表了一个更优雅的终态**——当分类器足够准的时候，它会比任何人工规则都更懂用户真正在意什么。

两条路径最终会在某个中间地带汇合：Hooks 作为底层接口，Classifier 作为默认实现，用户可以选择替换或扩展。

---

## 参考资料

- [Anthropic Engineering: Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [OpenAI Codex Hooks Documentation](https://developers.openai.com/codex/hooks)
- [OpenAI: Work with Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/)
- [OpenAI: Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/)