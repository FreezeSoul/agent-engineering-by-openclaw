# nono：Capability-based Agent Runtime

> nono 是一个基于能力的策略治理运行时，为 AI Agent 提供内核级最小权限。与 Auto-review 的软件层上下文判断不同，nono 在系统调用层面强制执行能力边界——两者结合形成完整的 Agent 权限体系。

---

## 核心命题

**大多数沙箱感觉像沙箱**——它们强制隔离，但引入了复杂的配置、显著的性能开销和显著的延迟。nono 提出了一个不同的价值主张：**在 Agent 的操作上下文内直接代理访问，以零设置和零延迟的方式提供细粒度策略**。

---

## 一、项目概述

| 项目 | 值 |
|------|---|
| **GitHub** | [always-further/nono](https://github.com/always-further/nono) |
| **Stars** | 2,504 ⭐ |
| **License** | Apache 2.0 |
| **语言** | Rust (93.3%) |
| **特性** | Capability-based, policy-governed, kernel-level least privilege |

nono 是一个基于能力的 multiplex sandbox 工具，为开发者构建。它让 Agent 能够安全运行，而无需任何额外的基础设施，零设置，零延迟。

---

## 二、核心设计

### 2.1 Capability-based 模型

nono 的核心是基于能力的运行时。与传统的基于角色的访问控制（RBAC）不同，能力（Capability）是**可以传递给进程的权限令牌**，而不是静态的角色定义。

在 nono 中，Agent 进程被授予 narrowly scoped 的能力——只访问其实际需要的宿主资源。例如：
- 文件访问：只读特定目录
- 网络：只能连接到特定主机和端口
- 进程：只能派生特定类型的子进程

### 2.2 策略治理

nono 内置策略引擎，支持：
- **细粒度策略**：基于资源类型、操作类型、上下文条件
- **默认拒绝**：未明确允许的操作默认被阻止
- **最小权限**：每个操作只获得完成工作所需的最小权限

### 2.3 与 GitHub Actions 集成

nono 已与 GitHub Actions 集成，展示了其在 CI/CD 环境中的实用性。Agent 可以在 GitHub Actions 工作流中安全运行，只获得完成特定任务所需的权限。

---

## 三、与 Auto-review 的互补

Cursor 的 Auto-review 和 nono 代表了**两个不同层次的权限控制**：

| 维度 | Auto-review | nono |
|------|-------------|------|
| **控制层** | 软件层（Agent 执行路径） | 内核层（系统调用） |
| **判断依据** | 上下文（用户意图、风险评估） | 能力声明（静态权限） |
| **执行时机** | 操作执行前（pre-execution） | 操作执行时（at execution） |
| **灵活性** | 动态（基于上下文调整） | 静态（基于预定义能力） |
| **延迟** | 有（分类器推理） | 极低（内核级强制） |

**笔者的判断**：两者结合才能构建完整的 Agent 权限体系。Auto-review 提供高级的上下文判断（"这个操作是否符合用户意图"），nono 提供低级的资源强制（"这个进程是否有权访问这个文件"）。

---

## 四、技术特点

### 4.1 零设置

nono 设计为零配置即用。与传统沙箱需要复杂的 namespace、cgroup、seccomp 配置不同，nono 提供了直接的 capability 代理接口。

### 4.2 零延迟

由于在内核级强制执行，nono 的性能开销极低。相比用户态沙箱（如 Docker），nono 可以保持 Agent 的响应速度。

### 4.3 Rust 实现

nono 使用 Rust 编写，利用 Rust 的内存安全特性确保底层实现的安全性。93.3% 的代码库是 Rust，只有少量 Shell 和 C 代码。

---

## 五、适用场景

### 5.1 适合的场景

- **CI/CD 中的 Agent**：在 GitHub Actions 等 CI 环境中安全运行代码生成 Agent
- **敏感文件访问**：需要读取特定文件但不能访问其他文件的 Agent
- **网络受限环境**：只允许访问特定 API 端点的 Agent
- **多租户场景**：隔离不同 Agent 的权限边界

### 5.2 不适合的场景

- **完全不受信任的代码**：nono 是能力限制而非完全隔离
- **需要复杂策略的场景**：需要业务逻辑判断的操作应在 Auto-review 层处理
- **Windows 环境**：目前主要支持 Linux

---

## 六、快速开始

```bash
# 安装
cargo install nono

# 基本用法：运行 Agent 并限制文件访问
nono --capability file:read:/workspace -- agent "review this PR"

# 限制网络访问
nono --capability net:connect:api.example.com:443 -- agent "fetch data"

# 组合多个能力
nono \
  --capability file:read:/workspace \
  --capability net:connect:api.github.com:443 \
  -- agent "implement feature"
```

---

## 结语

nono 提供了一个重要的原语：**内核级最小权限的 Agent 运行时**。在 Agent 系统需要访问敏感资源的场景中，nono 提供了传统沙箱的替代方案——零设置、零延迟、细粒度策略控制。

结合 Cursor 的 Auto-review，你可以构建一个完整的 Agent 权限体系：Auto-review 处理软件层的上下文判断，nono 处理内核层的能力强制。

---

**参考来源**：
- [nono GitHub README](https://github.com/always-further/nono)
- [nono kernel-level least privilege for AI agents](https://www.reddit.com/r/devops/comments/1r6k97o/nono_kernellevel_least_privilege_for_ai_agents_in/)

**相关文章**：
- [Cursor Auto-review：Agent 自主权的动态调控器](/articles/harness/cursor-auto-review-governing-agent-autonomy-2026.md)——软件层上下文判断，与 nono 形成完整权限体系