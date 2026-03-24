# Harness Engineering：深度约束下的 Agent 能力最大化

> **本质**：Harness Engineering = 给 Agent 一个安全、可控、最大化能力的执行框架。"Harness"（挽具/甲胄）的隐喻——约束 Agent 的行为边界，同时不限制其核心能力。

---

## 一、为什么需要 Harness

Deep Agent 带来了前所未有的能力，也带来了前所未有的风险：

**无约束 Agent 的问题**：
- 可以执行任意代码、访问任意文件、调用任意 API
- 错误可能造成物理或数字世界的有害后果
- 长时间运行中，错误累积可能导致完全偏离目标
- 恶意操控下，Agent 可能被利用造成危害

**Harness 的目标**：
```
最大化 Agent 能力 + 最小化有害结果风险
```

这本质上是**工程化约束**——用系统设计和规则来控制 Agent 行为，而非依赖 Prompt 的软约束。

---

## 二、Harness Engineering 的三层架构

基于 Martin Fowler 对 OpenAI Agent 的分析，Harness Engineering 包含三层：

### 2.1 第一层：工具约束（Tool Constraints）

定义 Agent **可以**调用的工具及其使用条件。

```json
{
  "tools": {
    "bash": {
      "allowed": true,
      "max_duration_seconds": 60,
      "max_output_chars": 10000,
      "blocked_commands": ["rm -rf /", "mkfs", ":(){ :|:& };:"],
      "require_approval": ["git push", "curl -X DELETE"]
    },
    "file_read": {
      "allowed": true,
      "allowed_paths": ["/workspace/src", "/workspace/tests"],
      "denied_paths": ["/etc", "/root/.ssh", "/workspace/.env"]
    },
    "file_write": {
      "allowed": true,
      "allowed_paths": ["/workspace/src", "/workspace/output"],
      "require_approval": true,
      "backup_before_write": true
    }
  }
}
```

**关键原则**：
- 最小权限原则：只授予完成任务必需的最小权限
- 路径白名单：文件操作限制在特定目录树内
- 命令黑名单：禁止执行高危命令

### 2.2 第二层：行为规则（Behavioral Rules）

定义 Agent 在执行过程中的**行为准则**。

```python
RULES = [
    # 安全规则
    "never_execute_code_outside_sandbox",
    "never_access_user_credential_files",
    "never_perform_actions_without_user_consent_if_irreversible",

    # 质量规则
    "always_verify_critical_actions_before_execution",
    "never_skip_error_handling",
    "always_provide_reasoning_for_major_decisions",

    # 透明度规则
    "always_disclose_limitations_to_user",
    "never_hallucinate_confidence_in_wrong_answers",
    "always_distinguish_facts_from_inferences",
]
```

**行为规则的执行方式**：
1. **静态检查**：执行前验证是否符合规则
2. **动态监控**：执行中实时检测异常行为
3. **事后审计**：执行后检查行为日志

### 2.3 第三层：定期清理（Periodic Cleanup）

Agent 运行时会产生副作用——临时文件、缓存状态、中间进程。定期清理防止这些累积导致问题。

```python
class HarnessCleanup:
    def __init__(self):
        self.ephemeral_state = []  # 需要清理的临时状态

    def register_ephemeral(self, resource):
        self.ephemeral_state.append(resource)

    def periodic_cleanup(self, interval_minutes=30):
        """定期清理临时资源"""
        for resource in self.ephemeral_state:
            if resource.is_old(interval_minutes):
                resource.cleanup()

    def final_cleanup(self):
        """任务完成后全面清理"""
        for resource in self.ephemeral_state:
            resource.cleanup()
        self.ephemeral_state.clear()
```

**清理的内容**：
- 临时文件和进程
- 不再需要的 API 密钥或凭证
- 中间状态的缓存数据
- 超出保留窗口的对话历史

---

## 三、深度 Agent 的特殊 Harness 挑战

### 3.1 长程任务的 Harness

Deep Agent 任务可能持续数小时，涉及数百个操作步骤。这带来了特殊的 Harness 挑战：

**挑战 1：状态追踪**
```
问题：步骤n的错误可能在步骤n+50才显现
方案：引入检查点（Checkpoint），周期性保存 Agent 状态
      异常时可回退到上一个检查点
```

**挑战 2：资源累积**
```
问题：长时间运行累积大量临时文件、进程、网络连接
方案：资源配额 + 定期清理
```

**挑战 3：能力漂移**
```
问题：Agent 在长程执行中逐渐偏离原始目标
方案：目标锚定（Goal Anchoring）+ 周期性目标复核
```

> 详见：[Claude Code Architecture](articles/research/claude-code-architecture-deep-dive.md) 中的 Memory Checkpoint 机制

### 3.2 沙箱隔离（Sandbox Isolation）

完全自主 Agent 必须运行在隔离环境中，防止其操作影响真实系统：

**沙箱类型**：

| 类型 | 适用场景 | 隔离程度 |
|------|---------|---------|
| **进程沙箱** | 单一代码执行 | 进程级隔离 |
| **容器沙箱** | 多工具协同 | Namespace + Cgroup |
| **VM 沙箱** | 高风险操作 | 完整硬件虚拟化 |
| **网络隔离** | 访问外部 API | 网段隔离 |

> 详见：[NVIDIA Sandbox Security Guide](articles/community/nvidia-sandbox-security-guide.md)

### 3.3 人机协作模式

Harness Engineering 的一个核心洞见：**完全自主 vs 人类监督不是二元对立，而是连续谱**。

```
完全自主 ←————————————————————————→ 强人类监督
  |                                               |
  |—— 全自主执行，不干预                         |—— 所有操作需人工批准
  |—— 定期报告，进度可见                         |—— 关键节点审批
  |—— 异常暂停，等待指示                         |—— 建议模式（非执行）
```

ResearStudio 的研究证明：最强自主性与最佳人类控制可以共存。

---

## 四、安全 Harness：OWASP ASI 系列

OWASP 2026 年发布了首个 Agent 安全风险框架 **OWASP Top 10 for Agentic Systems (ASI)**：

| 编号 | 风险 | 说明 |
|------|------|------|
| ASI01 | Prompt Injection | 恶意指令注入操纵 Agent 行为 |
| ASI02 | Agent Escape | Agent 突破 Harness 限制 |
| ASI03 | Tool Poisoning | 恶意工具污染 Agent 工具集 |
| ASI04 | Memory Poisoning | 对 Agent 记忆的攻击 |
| ASI05 | Hallucination Harm | 错误信息导致有害决策 |
| ASI06 | Unbounded Self-Replication | Agent 无限制自我复制 |
| ASI07 | Context Overflow | 故意触发上下文溢出 |
| ASI08 | Agent-to-Agent Manipulation | 恶意 Agent 操纵其他 Agent |
| ASI09 | Data Exfiltration | Agent 意外泄露敏感数据 |
| ASI10 | System Overload | 通过 Agent 耗尽系统资源 |

> 详见：[OWASP Top 10 for Agentic 2026](articles/engineering/owasp-top-10-agentic-applications-2026.md)

---

## 五、Harness 的工程实践

### 5.1 快速开始：分层 Harness 设计

```python
class AgentHarness:
    def __init__(self, config: HarnessConfig):
        self.tool_layer = ToolConstraintLayer(config.tools)
        self.behavior_layer = BehavioralRuleLayer(config.rules)
        self.cleanup_layer = CleanupLayer(config.cleanup)

    async def execute(self, task: Task, agent: Agent):
        # Layer 1: 检查工具权限
        for step in agent.plan(task):
            if not self.tool_layer.is_allowed(step):
                step.block()
                await self.report_blocked(step)

        # Layer 2: 检查行为规则
        for action in agent.execute(task):
            violations = self.behavior_layer.check(action)
            if violations:
                await self.handle_violations(violations)

        # Layer 3: 定期清理
        self.cleanup_layer.periodic_cleanup()
```

### 5.2 干运行（Dry Run）模式

在真实执行前，先在 Harness 中模拟执行，检测潜在问题：

```python
class DryRunHarness:
    def validate_plan(self, plan: Plan) -> ValidationReport:
        report = ValidationReport()
        for step in plan.steps:
            if not self.tools.is_allowed(step):
                report.add_error(f"Tool {step.tool} not permitted")
            if not self.rules.is_safe(step):
                report.add_warning(f"Step may violate {self.rules.violated_rules(step)}")
        return report
```

### 5.3 熔断机制（Circuit Breaker）

当 Agent 行为异常时，自动触发熔断：

```python
class CircuitBreaker:
    def __init__(self, threshold=5, window_seconds=60):
        self.errors = deque(maxlen=threshold)
        self.threshold = threshold
        self.window = window_seconds

    def record_error(self, error):
        self.errors.append(time.time())
        if self.is_open():
            raise CircuitBreakerOpen(f"Too many errors in {self.window}s")

    def is_open(self) -> bool:
        if len(self.errors) < self.threshold:
            return False
        return time.time() - self.errors[0] < self.window
```

---

## 六、Harness vs 对齐（Alignment）

| 维度 | Alignment（对齐） | Harness Engineering |
|------|----------------|-------------------|
| **目标** | 让 AI 行为符合人类价值观 | 让 Agent 在给定能力下安全可控 |
| **层级** | 基础模型层 | 部署/工程层 |
| **方法** | RLHF、Constitutional AI | 工具约束、规则、监控 |
| **生效位置** | 训练时决定 | 部署时决定 |
| **可升级性** | 需要重新训练 | 可热更新 |

两者互补：Alignment 决定了 Agent "想"做什么，Harness 决定了 Agent "能"做什么。

---

## 参考文献

- Martin Fowler - Harness Engineering：见 [Harness Engineering: Martin Fowler](articles/community/harness-engineering-martin-fowler.md)
- OWASP ASI Top 10：见 [OWASP Top 10 for Agentic 2026](articles/engineering/owasp-top-10-agentic-applications-2026.md)
- Claude Code Architecture：见 [Claude Code Architecture](articles/research/claude-code-architecture-deep-dive.md)
- NVIDIA Sandbox Security：见 [NVIDIA Sandbox Security Guide](articles/community/nvidia-sandbox-security-guide.md)
