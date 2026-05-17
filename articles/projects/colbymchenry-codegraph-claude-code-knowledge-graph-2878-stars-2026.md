# CodeGraph：让 Claude Code 的代码探索从"大海捞针"变成"精准制导"

> 这个项目解决了一个长期困扰 Claude Code 用户的问题：代码探索时大量的 grep/glob/Read 调用消耗巨量 tokens，却没有真正高效地获取到需要的信息。

---

## 一句话概括

CodeGraph 是一个**预索引代码知识图谱**，它为 Claude Code 的 Explore agent 提供结构化的代码关系查询，使工具调用减少 92%，探索速度提升 71%。

---

## 为什么这值得关注

当你问 Claude Code "How does the extension host communicate with the main process?" 时，传统流程下：
1. Explore agent 启动 → `find` 扫描项目结构
2. `grep` 查找关键词
3. `glob` 匹配文件模式
4. `Read` 一个一个文件读
5. 汇总分析

这个过程平均产生 **40-52 次工具调用**，每次都带 tokens 成本。

CodeGraph 的做法：
1. `codegraph_explore` 调用 → 返回完整答案
2. **0 次文件读取**

这不是微优化，是数量级的差异。

---

## 技术原理

CodeGraph 在项目初始化时构建一个代码知识图谱：

- **节点（Nodes）**：函数、类、变量、接口等代码符号
- **边（Edges）**：调用关系、引用关系、继承关系
- **索引（Index）**：支持快速图遍历

```
┌──────────────────────────────────────────────────────────────┐
│ Claude Code 主会话                                            │
│ "Implement user authentication"                               │
│                                                               │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │ Explore Agent 1 │    │ Explore Agent 2 │  ← 并行探索      │
│  └────────┬────────┘    └────────┬────────┘                   │
│           │                      │                            │
│           ▼                      ▼                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         CodeGraph MCP Server                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Search   │  │ Callers  │  │ Context  │            │   │
│  │  │ "auth"   │  │ "login()"│  │ for task │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  │       └─────────────┼─────────────┘                    │   │
│  │                     ▼                                    │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │    SQLite Knowledge Graph (本地)                 │ │   │
│  │  │    - 符号关系  - 调用图谱  - 代码结构             │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

关键点：**100% 本地运行**，不需要 API key，不上传代码。

---

## 核心能力

### 1. Smart Context Building
一个 `codegraph_explore` 调用返回：
- 入口点（entry points）
- 相关符号（related symbols）
- 代码片段（code snippets）

不需要启动 Explore agent，不需要多次工具调用。

### 2. 图遍历替代文件扫描

当问 "Trace how a request flows from Session.request() through to the URLSession layer" 时：
- 代码图谱在**深度3的图遍历**中完整捕获了 9 步调用链
- 一次 explore 调用解决战斗

### 3. 跨语言支持

TypeScript、JavaScript、Python、Go、Rust、Java、C#、PHP、Ruby、C、C++、Swift、Kotlin、Dart、Svelte...

更关键的是：**跨语言查询可行**。Python+Rust 混合代码库的查询可以无缝遍历不同语言边界。

### 4. 框架感知路由

CodeGraph 知道 Django 的 `path()`、Flask 的 `@app.route`、Express 的 `app.get()`、Rails 的 `Route::get()`。

当查询某个 controller 的调用者时，不仅返回代码引用，还返回 URL pattern——这对理解 Web 应用架构至关重要。

---

## 性能数据

来自 6 个真实代码库的测试（Claude Opus 4.6 + Claude Code v2.1.91）：

| 代码库 | 工具调用 | 耗时 | 改进 |
|--------|---------|------|------|
| VS Code (TS) | 3 vs 52 | 17s vs 1m37s | **94% 减少 · 82% 加速** |
| Excalidraw (TS) | 3 vs 47 | 29s vs 1m45s | 94% 减少 · 72% 加速 |
| Claude Code (Py+Ru) | 3 vs 40 | 39s vs 1m8s | 93% 减少 · 43% 加速 |
| Claude Code (Java) | 1 vs 26 | 19s vs 1m22s | 96% 减少 · 77% 加速 |
| Alamofire (Swift) | 3 vs 32 | 22s vs 1m39s | 91% 减少 · 78% 加速 |
| Swift Compiler | 6 vs 37 | 35s vs 2m8s | 84% 减少 · 73% 加速 |

Swift Compiler 是最大的测试集：25,874 文件、272,898 节点。CodeGraph 在 **4 分钟内**完成索引，agent 用 **6 次 explore 调用 + 0 次文件读取**回答了复杂的跨切面问题。

---

## 使用方式

```bash
npx @colbymchenry/codegraph
```

交互式安装器会自动：
1. 全局安装 codegraph（作为 MCP server）
2. 配置 `~/.claude.json` 中的 MCP server
3. 设置 CodeGraph tools 的 auto-allow permissions
4. 添加全局 instructions 到 `~/.claude/CLAUDE.md`

```bash
cd your-project
codegraph init -i
```

然后重启 Claude Code。MCP server 加载后，每当 `.codegraph/` 目录存在，Claude Code 自动使用 CodeGraph tools。

---

## 适用场景

**适合**：
- 大型代码库（10k+ 文件）探索
- 需要理解跨模块调用关系的任务
- 对 tokens 消耗敏感的场景
- 有数据安全要求（代码不上云）的场景

**不适合**：
- 小型项目（初始化开销不划算）
- 非结构化代码（缺乏标准语法的代码库支持有限）
- 实时性要求极高的场景（图索引有延迟）

---

## 与 Articles 的关联

本文档配套 Article（[OpenAI Codex 企业级安全五大支柱](./openai-codex-enterprise-security-five-pillars-2026.md)）共同构成 Agent 工程的双重视角：

- **Article**：企业如何安全地部署 Agent——边界、审批、遥测
- **Project**：Agent 如何高效地理解代码——预索引、图遍历、本地化

两者的交汇点是：**当 Agent 能够安全地操作代码时，如何让它更高效地理解代码？** CodeGraph 回答了这个问题——不是因为它更聪明，而是因为它把"查找"变成了"查询"，把文件扫描变成了图遍历。

---

*来源：[GitHub - colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)*