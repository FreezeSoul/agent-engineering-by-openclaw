# vercel-labs/zerolang：为 Agent 时代重新设计的编程语言

> **核心论点**：zerolang 试图回答一个被所有传统编程语言忽略的问题——如果代码的主要读者不是人类，而是 AI Agent，编程语言应该长什么样？它的答案不是「更简单的语法」，而是「让 AI 能诊断、修复、改进代码的结构化接口」。这是编程语言设计史上一次罕见的范式转移。
>
> **关键判断**：zerolang 的核心创新不是语言本身（它的语法没有颠覆性创新），而是**将编译器的诊断和修复能力作为一等公民**——每个检查、每个错误、每个修复建议都通过结构化 JSON 输出，供 AI Agent 直接消费。这是「Agent-Readable Programming」的首次工程化实践。

---

## T - Target：谁该关注

- **Agent 框架开发者**：正在构建「AI 能理解和修改的代码系统」
- **编程语言设计研究者**：对「AI-First 语言设计」这个新方向感兴趣
- **Harness 工程师**：想理解如何让工具链更好地被 Agent 调用和修复

---

## R - Result：能带来什么

| 维度 | 传统编程语言 | zerolang |
|------|-------------|----------|
| **Token 效率** | 需要大量 Token 生成代码 | 专为低 Token 消耗设计 |
| **Agent 可读性** | 错误信息面向人类，AI 难以解析 | 每个输出都有结构化 JSON |
| **修复接口** | 依赖外部 Linter | `zero fix --plan --json` 原生修复计划 |
| **启动速度** | 数百毫秒 | 毫秒级（C 语言实现）|
| **依赖** | 大量外部依赖 | **零依赖**（适合安全隔离环境）|

---

## P - Positioning（定位破题）

### 它是什么

zerolang 是 **Vercel Labs 出品的实验性编程语言**，定位是「Agent 工作流的专用语言」。不是要替代 Rust/Go/Python，而是为 AI Agent 编写和修改代码这个特定场景专门设计。

**核心定位**（官方 README）：
> "Experimental programming language for agent workflows. Built for reliable autonomous software generation."

**技术特征**：
- **语言实现**：C 语言，无运行时依赖
- **编译输出**：本地可执行文件（Linux musl x64 等多平台）
- **核心特性**：零依赖、低内存占用、快速启动、快速构建、低延迟

### 它的真正创新：Agent-Readable Diagnostics

传统的编译器输出：
```
error: unknown identifier 'message'
```

zerolang 的结构化输出：
```json
{
  "code": "NAM003",
  "message": "unknown identifier 'message'",
  "expected": "visible local, parameter, function, or builtin",
  "actual": "no matching visible symbol",
  "repair": {
    "id": "declare-missing-symbol"
  }
}
```

这不是格式的改变，而是**接口设计的根本转变**——编译器不再只是「告诉人类哪里错了」，而是「提供 AI 能直接消费的结构化修复计划」。

### 它的边界

- **安全状态**：官方明确标注 `Security vulnerabilities should be expected. Not ready for production.`
- **生态成熟度**：v1.0 前随时可能 Breaking Change
- **语言能力**：目前主要面向小型工具和 Agent 工作流任务，不是通用编程语言

---

## S - Sensation（体验式介绍）

zerolang 的安装和第一个程序：

```bash
# 一行安装
curl -fsSL https://zerolang.ai/install.sh | bash

# 编写一个简单函数
echo '
fn answer i32
  ret + 40 2

pub fn main Void world World !
  if == answer() 42
    check world.out.write "math works\n"
' > hello.0

# 检查代码（Agent 可直接消费的 JSON）
zero check --json hello.0

# 尝试修复
zero fix --plan --json hello.0
```

zerolang 提供的 Skills 接口让 Agent 能直接获取语言规范：
```bash
zero skills get language      # 获取语言规则
zero skills get diagnostics   # 获取诊断代码含义
zero skills get stdlib        # 获取标准库文档
```

这些 skill 文本与编译器二进制版本匹配，确保 Agent 拿到的文档与实际编译器行为一致——这是「版本一致性」的 Agent 实践。

---

## C - Competition（竞品对比）

| 项目 | 定位 | Agent 适配性 | 成熟度 |
|------|------|-------------|--------|
| **zerolang** | Agent 工作流专用 | ⭐⭐⭐⭐⭐ 原生设计 | 实验性 |
| **Python** | 通用编程 | ⭐⭐ 有生态但非原生 | 生产级 |
| **Rust** | 系统编程 | ⭐⭐ 复杂但工具链好 | 生产级 |
| **Go** | 云服务编程 | ⭐⭐ 简单但无特殊 Agent 支持 | 生产级 |

**笔者认为**：zerolang 代表了一个重要方向——不是用现有语言为 Agent 写代码，而是**为 Agent 重新设计编程语言**。虽然目前是实验阶段，但它触及了 Agent 编程的核心问题：AI 生成的代码需要被 AI 理解和修改，而这需要新的工具链接口设计。

---

## E - Evidence（引用支撑）

### 引用 1：官方设计理念

> "The compiler exposes the workflow through CLI commands with stable structured output. The important contract is the stable fields and repair identifiers." — [zerolang README](https://github.com/vercel-labs/zerolang)

### 引用 2：安全边界声明

> "Security vulnerabilities should be expected. zerolang is not ready for production systems, sensitive data, or trusted infrastructure. Run and develop it in isolated, disposable environments." — [zerolang README](https://github.com/vercel-labs/zerolang)

---

## L - Learn（上手路径）

1. **体验 `zero check --json`**：用结构化输出检查一个错误程序，看 AI 能否直接理解诊断
2. **运行 `zero fix --plan --json`**：体验「修复计划」的 JSON 接口，评估它对 Agent 的可用性
3. **尝试 `zero skills get language`**：看 skill 文本的格式和内容质量
4. **阅读 examples/agent-repair-demo/**：这是 zerolang 设计的「Agent 修复闭环」的核心演示

---

## 与 Agent Engineering 知识库的关联

zerolang 与本仓库以下主题形成闭环：

| 关联主题 | 关联内容 |
|---------|---------|
| **Harness 工程** | 编译器提供的 `check --json`、`fix --plan --json` 是 Harness 评估器循环的原生实现——错误即反馈，修复即行动 |
| **工具安全/权限分层** | 零依赖设计天然适合沙箱化执行环境 |
| **上下文管理** | `zero skills get` 提供版本匹配的文档，Agent 永远不会拿到与编译器行为不一致的文档 |

---

**stars**: 4,523（2026-05-26）  
**fork**: 288 | **language**: C | **created**: 2026-05-15  
**url**: https://github.com/vercel-labs/zerolang