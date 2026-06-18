# DeusData/codebase-memory-mcp：让 AI Coding Agent 拥有"持久记忆"的代码知识图谱

> **一句话概括**：用 Tree-Sitter AST 分析 + 内存级 SQLite，将任意代码库压缩为可毫秒级查询的知识图谱——相当于给 Agent 装上了一个永不遗忘的"代码海马体"。

**关联文章**：[Anthropic 财务团队 Claude 叙事完整性 2026](./enterprise/anthropic-finance-team-claude-narrative-integrity-2026.md) — 财务团队用"Context 驱动"让 Claude 保持叙事一致性；本项目用知识图谱让 Agent 保持"代码上下文一致性"。两条路径，共同指向：**长任务中，持久化上下文是可靠性的基石。

---

## 一、解决的问题：Agent 在代码库里为什么"失忆"

当 Claude Code 在一个 5 万行代码库里工作时，它的 Context 窗口是有限的。但代码库本身是巨大的——函数调用链跨越几十个文件，HTTP 路由映射到 controller 再到 service 再到 DB，每一处都依赖对整体结构的理解。

**传统的解法**是让 Agent 自己通过 `grep` + `read` 去探索。但这是灾难性的：

- 每次 grep 都是一次 token 消耗，5 万行代码库可能要消耗数十万 token
- 跨文件的调用链（比如 A.py 调用 B.py 的函数，B.py 又调用 C.py 的方法），Agent 根本无法可靠地追踪
- 一旦 Session 结束，这些探索结果全部丢失；下一次对话，Agent 重新变成"失忆"

Anthropic 财务团队在 R433 的实践中揭示了一个关键洞察：**Claude 的价值不在于"能做"，而在于"持续地、一致地做"**。代码世界里，这个一致性就是"对整个代码库结构的持续感知"——而 codebase-memory-mcp 正是这个感知层的工程实现。

---

## 二、核心技术设计

### 2.1 Tree-Sitter AST → 知识图谱

代码库索引的核心是 [Tree-Sitter](https://tree-sitter.github.io/tree-sitter/)——一个增量式 AST 解析器，能将源代码解析为抽象语法树。codebase-memory-mcp 在此基础上做了一层**跨语言的统一建模**：

- 函数（`Function` 节点）、类（`Class` 节点）、包（`Module` 节点）
- 调用关系（`CALLS` 边）、导入关系（`IMPORTS` 边）
- HTTP 路由 → Controller → Service → DB 的纵向链路

158 种语言各有其语法树结构，但这套系统在所有语言之上建立了统一的图谱 schema——Python 的 `def`、TypeScript 的 `function`、Rust 的 `fn` 全部映射到同一个 `Function` 节点类型。

```
// 示例图谱结构
(commit_changes:Function)-[:CALLS]->(detect_impact:Function)
(commit_changes:Function)-[:IN_FILE]->(changes.rs:File)
(detect_impact:Function)-[:CALLS]->(classify_risk:Function)
```

### 2.2 混合索引：语义搜索 + 全文搜索 + 符号搜索

**语义搜索**（`semantic_query`）：内置 Nomic `nomic-embed-code` 向量模型（768d int8），编译进二进制文件，无需 Ollama 或任何 API Key。11 信号联合评分：TF-IDF、RRI（相对重要性）、API/类型/装饰器签名、AST profile、数据流、Halstead-lite、MinHash、模块邻近度、图扩散。

**BM25 全文搜索**：SQLite FTS5 引擎，`cbm_camel_split` 分词器原生支持 camelCase 和 snake_case 自动切分。

**符号搜索**（`search_graph`）：正则匹配 + Label 过滤 + 节点度数约束，直接在图谱上查询。

```sql
-- 示例 Cypher-like 查询
MATCH (f:Function)-[:CALLS]->(g) 
WHERE f.name = 'handle_request' 
RETURN g.name, g.file
```

### 2.3 极限性能：Linux Kernel 3 分钟索引用

性能指标（README 原文）：

> "Average repository in milliseconds. Linux kernel (28M LOC, 75K files) in 3 minutes. Sub-millisecond structural queries. 120x fewer tokens — 5 structural queries: ~3,400 tokens vs ~412,000 via file-by-file search."

笔者认为，这个性能不是来自"更快的硬件"，而是来自**正确的架构取舍**：

- **RAM-first 管道**：LZ4 压缩 + 内存级 SQLite + Aho-Corasick 模式匹配。所有索引数据在内存中处理完毕后才写入磁盘，索引完成后内存释放。
- **单二进制、零依赖**：不需要 Docker、不需要 Node.js、不需要 Python 环境。macOS/Linux/Windows 各一个压缩包，下载 → 运行 `install` → 完成。
- **无 API Key**：所有模型推理（向量化）全部在本地完成，代码从不离开用户的机器。

### 2.4 11 个 Agent 自动配置

运行 `install` 后，工具自动检测并配置 MCP entry、instruction files、pre-tool hooks，覆盖：

Claude Code、Codex CLI、 Gemini CLI、Zed、OpenCode、Antigravity、Aider、KiloCode、VS Code、**OpenClaw**、Kiro。

> 笔者注意到，OpenClaw 是唯一被列出名称的 Agent 工程平台（而非单纯的产品），这暗示该工具的作者对 Agent 工程框架有较深的理解。

---

## 三、使用体验：装好后说一句"Index this project"

安装流程（README 原文）：

```bash
# macOS / Linux，一行命令
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# 可选：安装带图谱可视化 UI 的版本
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash -s -- --ui

# Windows
powershell -Command "Invoke-WebRequest -Uri ... -OutFile install.ps1; .\install.ps1"
```

装好后，**重启 Agent，说"Index this project"**——done。`install` 命令自动完成：
- 二进制文件放置、macOS quarantine strip + ad-hoc 签名
- MCP server entry 配置
- 各 Agent 的 instruction 文件写入

可视化 UI 在 `localhost:9749`，可选。提供 3D 交互图谱，可探索整个代码库的知识图谱结构。

---

## 四、与 R433 叙事完整性的深层呼应

R433 披露了 Anthropic 财务团队的核心洞察：**Claude 的价值在于"持续保持一致性"而非"一次性完成任务"**。这在代码场景下就是：

| 财务团队实践 | 代码场景对应 |
|-------------|-------------|
| Narrative Integrity：每次 board deck 变更自动重新验证所有数字 | 代码变更后自动追踪影响链：commit → 哪些函数受影响 → 影响多深 |
| 单一真相来源（Google Doc） | 知识图谱作为代码的单一结构真相来源 |
| Recurring workflows（monthly review） | 每次新 Session 自动连接到已有图谱，无需重新索引 |

codebase-memory-mcp 提供的不只是"更快的 grep"，而是**持久化的代码结构记忆**——Agent 每次启动时，知识图谱已经包含了整个代码库的结构，不需要重新探索。这正是"Context 驱动"范式在代码智能层的完整实现。

---

## 五、安全与信任设计

README 明确承认了这个工具的本质风险：

> "This tool reads your codebase and writes to your agent configuration files. That is what it is designed to do."

在这个前提下，项目做了三层安全承诺：

1. **源码可审计**：所有处理逻辑开源，不依赖任何闭源组件
2. **全链路签名**：每个 release 二进制经过 SLSA 3 级 provenance 签名，checksum + 签名双重验证
3. **VirusTotal 扫描**：每次 release 经过 70+ 杀毒引擎扫描
4. **100% 本地处理**：代码从不离开用户的机器

> 笔者认为，最后一条是 AI Coding 工具链的基准线——如果一个代码索引工具需要你把代码上传到云端，这本质上是一个数据安全违规，无论其他指标多么漂亮。

---

## 六、快速上手路径

```bash
# 1. 安装（一键）
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# 2. 重启你的 Agent，说：
#   "Index this project"

# 3. 之后可以用自然语言问：
#   "Which functions does handle_request call?"
#   "Find dead code in the auth module"
#   "Show me the HTTP route → DB call chain"

# 可选：开启自动索引
codebase-memory-mcp config set auto_index true

# 可选：打开可视化图谱
codebase-memory-mcp --ui=true --port=9749
```

---

## 七、技术规格一览

| 指标 | 值 |
|------|-----|
| **Stars** | 5,829（GitHub） |
| **License** | MIT |
| **语言支持** | 158 种 |
| **索引速度** | Linux Kernel（28M LOC, 75K files）3 分钟 |
| **查询延迟** | < 1ms（结构查询）|
| **Token 节省** | ~120x（3,400 vs 412,000 per query set）|
| **向量化** | 内置 Nomic nomic-embed-code（无需 API Key）|
| **平台** | macOS (arm64/amd64)、Linux (arm64/amd64)、Windows |
| **依赖** | 零（单静态二进制）|
| **支持 Agent** | Claude Code、Codex CLI、Copilot、Zed 等 11 个 |
| **安全认证** | OpenSSF Scorecard、SLSA 3、VirusTotal 70+ 引擎 |

---

## 八、适用边界

**适用场景**：
- 大型代码库（> 10K 行）的长期 Agent 开发项目
- 需要跨文件追踪调用链的架构分析任务
- 需要持续性代码记忆的多 Session 开发流程
- 对代码数据隐私有严格要求的团队（100% 本地）

**不适用场景**：
- 超小型项目（单文件或几百行代码，直接问 Agent 更高效）
- 需要自然语言语义理解的代码解释（图谱提供的是结构记忆，不是语义理解）
- 依赖云端协同的团队（虽然本地处理是优点，但协作场景需要额外设计）

---

## 九、结论

codebase-memory-mcp 解决的不是"能不能索引代码"的问题，而是"索引完了怎么持久化、怎么查询、怎么让 Agent 每次都能用上"的问题。这与 R433 Anthropic 财务团队的实践形成了跨越领域的共鸣：**真正让 AI Agent 可靠完成长任务的，不是模型有多强，而是上下文管理层有多扎实。

笔者认为，这个项目的最大价值不在于"快"（虽然确实快），而在于它证明了**持久化的代码知识图谱可以作为 MCP 协议的标准工具层**——任何基于 MCP 的 Agent 都可以通过这个统一的图谱接口获得跨语言、跨文件的代码结构感知，而不需要自己实现一套索引系统。这是基础设施级别的贡献。
