# IronClaw：WASM 原生安全 Agent Harness

> **核心命题**：在 Agent 系统中，「安全」不应该是事后添加的防护层，而应该是从设计之初就嵌入架构的核心约束。IronClaw 通过 WASM 沙箱实现了这一理念——每一个工具、每一个操作都在强制性的安全边界内执行，而不是依赖信任链。

---

## 为什么这个项目值得关注

Agent 系统面临一个根本性矛盾：**模型需要执行操作来完成任务，但执行操作意味着潜在的风险**。

传统方案有两种：
1. **信任但验证**：让 Agent 执行操作，事后检查结果
2. **权限最小化**：限制 Agent 能做什么，但限制本身难以精确

IronClaw 选择了第三条路：**WASM 沙箱 + 强制执行**。每个工具都在隔离的 WASM 运行时中执行，Agent 无法突破沙箱边界——这不是「信任」，而是「物理强制」。

笔者认为，这种架构代表了 Agent 安全设计的正确方向：**不是让 Agent「不要做坏事」，而是让 Agent「做不到坏事」**。

---

## 核心设计

### WASM 原生沙箱

IronClaw 的核心是一个基于 WebAssembly 的沙箱运行时。每个工具、每个插件都在 WASM 容器中执行，具有以下特性：

- **内存隔离**：WASM 强制内存边界，工具无法访问沙箱外的内存
- **能力边界**：工具只能访问被明确授权的 API
- **可验证性**：WASM 模块可以被静态分析，验证其行为边界

```rust
// IronClaw 工具执行示例（概念）
let tool = Tool::from_wasm(wasm_bytes);
let result = tool.execute(
    &args,
    Permissions::new()
        .allow("filesystem:read:/workspace")
        .deny("network:outbound")
);
```

### Routines：可审计的工作流

IronClaw 引入了 "Routines" 概念——一种可组合、可审计的工作流单元。每个 Routine 定义了：

1. 输入/输出契约
2. 所需的最小权限集
3. 执行的步骤序列
4. 错误处理策略

Routines 的设计让 Agent 的行为可以被预测和审计——不是因为模型「表现良好」，而是因为执行路径被明确定义。

### 工具插件系统

IronClaw 支持通过插件扩展工具集。插件同样运行在 WASM 沙箱中，保证了扩展的安全性。

笔者认为，**工具插件的沙箱化是 Agent 系统的必由之路**。正如 Codex 的设计指出的，MCP 服务器需要「自己负责 guardrails」。IronClaw 通过强制沙箱化，将这个责任从工具转移到了框架本身。

---

## 与 Codex 的关联

Codex 文章详细讨论了 Agent Loop 的架构，包括工具安全、上下文管理、性能优化等主题。IronClaw 在这些维度上提供了不同的实现思路：

| 维度 | Codex 的做法 | IronClaw 的做法 |
|------|------------|----------------|
| **工具安全** | Shell 沙箱 + MCP 工具自负责 | WASM 原生沙箱，强制隔离 |
| **权限控制** | Approval mode + sandbox 配置 | Routines + 最小权限原则 |
| **上下文管理** | Compaction + Prompt Caching | 持久内存 + 会话状态 |
| **安全模型** | ZDR（数据不存储）+ 无状态请求 | WASM 可验证性 + 强制边界 |

两者都承认：**Agent 系统必须有硬性的安全边界**，但在实现路径上有所不同。Codex 选择在应用层实现边界（沙箱配置、approval mode），IronClaw 选择在运行时层实现边界（WASM 强制执行）。

---

## 适用场景

IronClaw 特别适合以下场景：

1. **高安全需求环境**：金融、医疗、法律等需要强制合规的领域
2. **多租户 Agent 系统**：需要隔离不同用户/租户的 Agent 操作
3. **第三方工具集成**：需要安全地执行来自不受信任源的插件
4. **合规审计要求**：需要证明 Agent 的每个操作都在授权范围内

---

## 快速上手

```bash
# 安装
pip install ironclaw

# 初始化项目
ironclaw init my-agent
cd my-agent

# 启动安全 Agent
ironclaw run --security-level high

# 定义 Routine
ironclaw routine create --name "code-review" \
  --permissions "filesystem:read" "git:execute" "llm:call"
```

---

## 引用

> "Security-first personal agent harness with WASM sandboxing, routines, tool plugins, and persistent memory."
> — IronClaw README

> "Every tool execution happens in an isolated WASM runtime with explicit permission grants."
> — IronClaw Documentation

---

**标签**：Security、Harness Engineering、WASM、Agent Runtime、Sandboxing

**关联文章**：
- Codex Harness Architecture: Agent Loop Deep Dive（工具安全/沙箱设计对比）

**Stars**：12,394 ⭐（2026-06-06）
**License**：MIT
**官方仓库**：https://github.com/nearai/ironclaw