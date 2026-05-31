# Cursor Auto-review Run Mode：三层安全过滤的 Agent 执行模式

## 核心论点

**Auto-review 是 Cursor 对「长时运行 Agent 安全边界」的最新工程答案——通过 Allowlist → Sandbox → Classifier Subagent 三层过滤，将 Agent 自主执行能力与人工审批分离，在安全性和连续性之间取得工程化平衡。**

---

## 背景

Cursor 在 2026 年 5 月引入了 Auto-review Run Mode，这是一个新的执行模式，允许 Cursor Agent 在更长时间内自主工作，同时减少审批提示（approval prompts）并提高执行安全性。

## 三层安全架构

### 第一层：Allowlist（白名单即时执行）

对于明确安全的操作（如标准文件读写、特定 shell 命令），Cursor 维护一个 allowlist。命中的操作立即执行，无需任何人工干预。这是追求「连续性」的第一层保障。

### 第二层：Sandbox（沙箱隔离执行）

对于可以安全隔离的操作（如 MCP 工具调用、Fetch 请求），Cursor 在沙箱环境中执行这些操作。沙箱提供了资源限制和权限隔离，即使操作异常也不会影响主机环境。

### 第三层：Classifier Subagent（分类器子 Agent）

对于无法通过前两层判断的操作，Auto-review 引入了一个 classifier subagent。这个子 Agent 负责判断：「是否允许执行」「是否应该换一种方式完成」或「是否需要人工审批」。

```
用户操作 → Allowlist检查 → 命中? → 直接执行
                    ↓ 未命中
              Sandbox检查 → 可沙箱化? → 沙箱执行
                    ↓ 否
              Classifier Subagent → 决策（放行/重试/审批）
```

## 工程意义

### 安全性与连续性的平衡

传统 Agent 面临「频繁审批中断工作流」和「过度信任导致安全风险」的两个极端。Auto-review 的三层架构提供了渐进的信任梯度：

- **第一层**：消除重复性审批负担（已知安全操作）
- **第二层**：隔离风险操作（工具执行层面）
- **第三层**：智能决策（对未知操作进行语义判断）

### Classifier Subagent 的设计价值

第三层的 classifier subagent 是整个架构的核心创新。它不是一个简单的规则引擎，而是一个小型 Agent，专门负责「操作分类」这一单一任务。这种专一 Agent 设计避免了主 Agent 的决策过载，同时也便于单独优化和审计。

## 与现有架构的关联

Cursor 的 Auto-review 三层架构与仓库中已有的 harness 设计理念形成呼应：

- **Allowlist** 对应 Harness 中的「预定义安全边界」
- **Sandbox** 对应「资源隔离」机制
- **Classifier Subagent** 对应「动态策略决策」

这种分层思想在 anthropic-effective-harnesses-for-long-running-agents（ Harness 设计原则）中有系统性论述，Auto-review 是该原则在 Cursor 自身产品中的落地实践。

## 产品可用性

Auto-review 适用于 Cursor Pro、Teams 和 Enterprise 计划。对于需要长时间运行 Agent 的开发者，这个模式显著提升了工作连续性，同时保持了安全边界。

---

**来源**：https://cursor.com/changelog/auto-review

**关联项目**：
- [Cursor 3.5 Multi-repo Automations](cursor-multi-repo-automations-cross-codebase-agent-engineering-2026.md)：跨代码库 Agent 工程范式
- [anthropic-effective-harnesses-for-long-running-agents](./harness/anthropic-effective-harnesses-for-long-running-agents-2026.md)：长时运行 Agent 的 Harness 设计原则