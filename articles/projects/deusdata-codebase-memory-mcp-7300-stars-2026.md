# DeusData/codebase-memory-mcp：AI Coding Agent 的"持久记忆"——代码知识图谱 MCP Server

> **一句话概括**：用 Tree-Sitter AST + 内存级 SQLite，将任意代码库压缩为可毫秒级查询的知识图谱——相当于给 AI Agent 装上了一个永不遗忘的"代码海马体"。一次索引，永久保持对整个代码库的结构化感知，99% 更少的 token 消耗。

**License**: MIT | **Stars**: 7,300+ | **GitHub**: [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)

---

## 一、解决的问题：Agent 在代码库里为什么总是"失忆"

当 Claude Code 在一个 5 万行代码库里工作时，Context 窗口是有限的。但代码库本身是巨大的——函数调用链跨越几十个文件，HTTP 路由映射到 controller 再到 service 再到 DB，每一处都依赖对整体结构的理解。

**传统的解法**是让 Agent 自己通过 `grep` + `read` 去探索。但这是灾难性的：

- 每次 grep 都是一次 token 消耗，5 万行代码库可能要消耗数十万 token
- 跨文件的调用链（比如 A.py 调用 B.py 的函数，B.py 又调用 C.py 的方法），Agent 根本无法可靠地追踪
- 一旦 Session 结束，这些探索结果全部丢失；下一次对话，Agent 重新变成"失忆"

**笔者认为**：这个问题在 startup 场景下尤其致命——创业公司往往代码库增长快、人员少、没有专职的 code review 角色。AI Agent 本应成为"不知疲倦的资深工程师"，但它在代码库里"失忆"，意味着它每次都要从零开始理解代码——这不仅慢，还容易出错。

---

## 二、核心技术设计

### 2.1 Tree-Sitter AST → 知识图谱

代码库索引的核心是 [Tree-Sitter](https://tree-sitter.github.io/tree-sitter/)——一个增量式 AST 解析器。codebase-memory-mcp 在此基础上做了一层**跨语言的统一建模**：

```
// 示例图谱结构
(commit_changes:Function)-[:CALLS]->(detect_impact:Function)
(commit_changes:Function)-[:IN_FILE]->(changes.rs:File)
(detect_impact:Function)-[:CALLS]->(classify_risk:Function)
```

统一 Schema：
- **节点类型**：Function、Class、Module、Package、Route、Resource 等
- **边类型**：CALLS、IMPORTS、DEFINES、HTTP_CALLS、DATA_FLOWS 等

158 种语言各有其语法树结构，但这套系统在所有语言之上建立了统一的图谱 schema——Python 的 `def`、TypeScript 的 `function`、Rust 的 `fn` 全部映射到同一个 `Function` 节点类型。

### 2.2 Hybrid LSP：超越纯 AST 的语义理解

Tree-sitter 只能告诉你代码的"结构"，不能告诉你代码的"含义"：

```python
# Tree-sitter 能知道这是函数调用
profile.display_name()

# Hybrid LSP 能知道这调用的是哪个类的哪个方法
# → Profile.display_name，定义在 user.py 的第 47 行
```

这是通过**内置的轻量级语言服务端**实现的——支持 Python、TypeScript/JS、C#、Go、Java、Kotlin、Rust 等 10 种语言的语义类型解析。没有额外进程，没有 API Key，编译进同一个二进制文件。

### 2.3 性能数据

| 指标 | 数据 |
|------|------|
| Linux Kernel 全量索引（2800 万行代码，75000 文件）| 3 分钟 |
| Django 索引 | ~6 秒，49000 节点 |
| Cypher 查询 | <1ms |
| Token 节省 | 99.2%（3400 tokens vs 412000 tokens）|

**RAM-first 管道**：所有索引在内存中完成（LZ4 压缩），最后才 dump 到 SQLite。索引完成后内存释放回 OS。

---

## 三、工程亮点：为什么这是一个" harness"项目

### 3.1 多 Agent 支持：开箱即用

`install` 命令自动检测并配置 11 种主流 Coding Agent：

| Agent | MCP 配置 | Instructions | Hooks |
|-------|---------|-------------|-------|
| Claude Code | ✅ | 4 Skills | PreToolUse |
| Codex CLI | ✅ | AGENTS.md | SessionStart |
| Gemini CLI | ✅ | GEMINI.md | BeforeTool |
| OpenCode | ✅ | AGENTS.md | — |
| Aider | ✅ | CONVENTIONS.md | — |
| KiloCode | ✅ | Rules | — |
| OpenClaw | ✅ | — | — |

这意味着**不管你的团队用哪种 Coding Agent，都可以一键接入这个知识图谱**。

### 3.2 Team-Shared Graph Artifact

> "Commit a single compressed file to your repo and your teammates skip the reindex."

```bash
# 导出图谱到压缩文件
# 下次 clone 后自动导入，增量索引
```

- **格式**：SQLite + zstd 压缩（8-13:1 压缩率）
- **防冲突**：`.gitattributes` 设置 `merge=ours`
- **两层导出**：Best（全量 vacuum）+ Fast（增量）

**笔者认为**：这个 feature 的真正价值不是"省时间"，而是**让团队所有成员和 AI Agent 共享同一个代码视图**。没有这个，一个 Agent 在分支 A 里做的上下文理解，到分支 B 里就完全失效了。

### 3.3 安全：企业级信任

每个 release 都经过：
- **VirusTotal**：70+ 杀毒引擎扫描，0 误报
- **SLSA Level 3**：构建来源加密验证
- **Sigstore cosign**：Keyless 签名
- **CodeQL SAST**：发布前必须无警报

> "All processing happens 100% locally; your code never leaves your machine."

---

## 四、使用场景

### 场景一：理解陌生代码库

当你接手一个 legacy 项目时：

```
你：给我讲讲这个项目的整体架构

Agent 调用：
  get_architecture() 
  → 返回语言、入口点、路由、热点模块、层级结构

你：这个 ProcessOrder 函数被哪些地方调用？

Agent 调用：
  trace_path(function_name="ProcessOrder", direction="inbound")
  → 返回完整调用链，包含跨文件的类型推断
```

### 场景二：安全影响分析

```
你：我在改 auth.py，这个改动会影响哪些地方？

Agent 调用：
  detect_changes() 
  → 返回受影响的函数 + 风险分类（高/中/低）
```

### 场景三：跨服务的 HTTP 追踪

```
你：哪些前端代码调用了 user-service 的 /api/users 端点？

Agent 调用：
  search_graph(label="Route", name_pattern=".*users.*")
  → 返回路由 → 调用方 → 数据流
```

---

## 五、和竞品的对比

| 维度 | codebase-memory-mcp | 传统 grep/read | 向量数据库方案 |
|------|---------------------|----------------|----------------|
| **索引速度** | 毫秒~分钟 | 无需索引 | 小时级 |
| **上下文精度** | 结构化（调用链）| 文本匹配 | 语义相似 |
| **跨语言支持** | 158 种 | N/A | 依赖 embedding 模型 |
| **部署复杂度** | 单二进制 | 无 | 需要向量服务 |
| **Token 消耗** | 降低 99% | 全量读取 | 中等 |
| **团队共享** | ✅ Artifact | ❌ | ❌ |

**笔者认为**：向量数据库方案（比如基于 embedding 的代码搜索）的核心问题是**丢失了代码的结构信息**。当你搜索"处理订单的相关代码"时，它返回的是语义相似的片段，但无法告诉你这些片段之间的调用关系。codebase-memory-mcp 的图谱模型解决这个问题——它保留的是**关系**，不只是相似性。

---

## 六、快速上手

### 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

重启 Agent，说"Index this project"——done。

### 手动配置

```json
// ~/.claude/.mcp.json
{
  "mcpServers": {
    "codebase-memory-mcp": {
      "command": "/path/to/codebase-memory-mcp"
    }
  }
}
```

---

## 关联文章

- **[资源约束型创业公司的 AI Agent 战略](./enterprise/claude-ai-agents-startups-resource-constrained-2026.md)** — 创业公司如何在人手不足时用 AI 扛起整家公司；本项目让 AI Agent 拥有持久化的代码上下文理解能力，是"让 AI 持续可靠工作"的工程基础

---

## 引用来源

- [codebase-memory-mcp GitHub README](https://github.com/DeusData/codebase-memory-mcp)
- [Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP](https://arxiv.org/abs/2603.27277)（arXiv:2603.27277）
- Multi-Agent Support 列表（README Section: Multi-Agent Support）
