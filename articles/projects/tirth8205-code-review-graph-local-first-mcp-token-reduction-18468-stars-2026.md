# code-review-graph：MCP 代码智能图谱 38x-528x Token 减负 2026

**核心命题**：传统 AI Code Review 让模型重新读取整个代码库的语义上下文；code-review-graph 用 Tree-sitter 构建持久化的结构图谱，通过 MCP 协议让 AI 助手只读取与变更相关的最小文件集。这不是又一个静态分析工具，而是把「代码结构」作为可缓存、可增量、可查询的图数据库产物。

---

## 一手来源

- **GitHub**：`https://github.com/tirth8205/code-review-graph`
- **License**：MIT
- **Stars**：18,468⭐（2026-06-14 验证）
- **创建日期**：2026-02-26（不到 4 个月）
- **最后更新**：2026-06-10
- **语言**：Python（核心）+ 多平台适配

---

## 为什么这个项目值得关注

### 1. 直击 AI Code Review 的「全量读取」痛点

AI 编程助手（Claude Code、Codex、Cursor、Copilot 等）在执行代码评审、PR 分析、上下文补充时，几乎都会**重新加载整个仓库的语义上下文**——这意味着 1,000 个文件的仓库每次评审都消耗 50K+ tokens，其中 95% 是与变更无关的代码。

code-review-graph 解决这个问题的方式是**把代码库解析为 AST 图谱**：

```
Repository → Tree-sitter Parser → SQLite Graph → Blast Radius → Minimal Review Set
```

关键数据：项目 README 的 benchmark 图表显示 **6 个真实仓库平均 38x 到 528x 的 token 减负**——这是一个数量级的改进。

### 2. 与 Anthropic "Code Execution with MCP 98.7% Token Reduction" 的工程对照

> **Pair 关联**：`articles/tool-use/anthropic-code-execution-with-mcp-98-percent-token-reduction-2026.md`
>
> **对位维度**（⭐⭐⭐⭐ 具体对位）：
> - **Anthropic 一手源**：MCP 让 Agent 把代码执行从「每次调用重新加载上下文」变成「协议级共享资源池」，98.7% token 减负
> - **code-review-graph 实践**：把代码**结构**从「每次评审重新解析」变成「MCP 持久化图谱」，38x-528x token 减负
> - **共享机制**：都是把「高频重建的开销」通过**协议级共享**变成一次性投入
> - **共享关键词**：`MCP`、`token reduction`、`persistent map`、`context`、`code intelligence`、`local-first`

### 3. Multi-Platform 一键安装：13 个 AI 编程工具全兼容

code-review-graph 通过自动检测用户的 AI 编程工具环境，一行命令完成配置：

```bash
code-review-graph install    # 自动检测并配置所有支持的平台
```

支持 13 个平台：Codex、Claude Code、Cursor、Windsurf、Zed、Continue、OpenCode、Antigravity、Gemini CLI、Qwen、Qoder、Kiro、GitHub Copilot。

每个平台的 MCP 配置、hooks/skills、graph-aware 规则都自动注入。这意味着用户**不需要切换工具就能享受到代码图谱带来的加速**——这是 Path C 协议下「通过既有 MCP 协议标准扩展到所有平台」的典型实现。

### 4. Blast Radius 分析：变更影响范围的可计算化

项目最具工程价值的设计是 **Blast Radius（爆炸半径）**——当你修改一个文件时，图谱自动追踪所有调用者、依赖者、相关测试，返回「最小需要被 AI 读取的文件集合」。

这解决了 AI Code Review 的核心低效场景：**用户问的是「这个改动影响哪些文件」，但 AI 不得不读整个仓库才能回答**。Blast Radius 把这个问题的答案从「扫描式」变成「查询式」，复杂度从 O(n) 降到 O(受影响子图)。

工程意义：当 Anthropic 强调「context engineering 的注意力预算」时，code-review-graph 用图数据库把预算的**分配策略**从「全量铺平」变成「按需点射」。

### 5. 增量更新：让图谱跟着代码演进

Tree-sitter 的解析结果是可增量更新的——只有修改过的文件需要重新解析，其余节点保留在 SQLite 中。这意味着：

- **首次构建**：500 文件项目约 10 秒
- **增量更新**：单文件改动毫秒级
- **Watch 模式**：后台自动同步文件系统事件

工程上的隐性收益：图谱本身就是一个**轻量级代码考古工具**——你可以查询「这个函数的所有调用者」「这个接口的所有实现」「这个模块的所有测试覆盖」，这些都是图数据库的标准查询，不需要重新跑 LLM。

---

## 与现有 AI Coding 项目的定位差异

| 项目 | 定位 | Token 减负机制 |
|------|------|--------------|
| **tirth8205/code-review-graph** | 持久化结构图谱 + MCP | 38x-528x（仅读相关文件） |
| **affaan-m/everything-claude-code** | Agent 性能优化（27K⭐） | 缓存层 + 提示词优化 |
| **microsoft/skillopt** | Skill 训练与优化（5K⭐） | 训练时优化，不是评审时 |
| **Cursor Composer 2.5** | 上下文压缩（商业闭源） | 自总结（lossy） |
| **Anthropic MCP code execution** | 协议级共享（Anthropic 一手源） | 98.7%（代码执行场景） |

**关键差异**：code-review-graph 是「**结构层的优化**」，而其他项目大多在「prompt 层」「缓存层」「训练层」做文章。结构层优化有不可替代的优势——它是**确定性的、可验证的、可重放的**，不依赖 LLM 的"理解"是否正确。

---

## 工程哲学层面：从「扫描代码」到「查询代码」

这是一个范式转移的早期信号：

- **旧范式（扫描式）**：AI 读取整个文件 → 拼接到 prompt → 让 LLM 推理
- **新范式（查询式）**：AI 查询结构图谱 → 获取精确子集 → 只读必要文件

旧范式的隐性成本：每次评审都重新付钱（token + 延迟）。新范式的成本结构：构建图谱一次性投入 + 查询边际成本接近零。

code-review-graph 不是这个范式的唯一实现，但它是**目前做得最完整、跨平台最广、benchmark 数据最透明的**。18K⭐ 在 4 个月内达成，说明开发者社区对「代码图谱 + AI」这个交叉点的需求是真实的。

---

## 适用场景

1. **大型代码库 Code Review**：仓库 > 500 文件，单次评审节省 38x token
2. **多 AI 工具协作**：13 个平台兼容，团队不同成员用不同工具都能享受加速
3. **增量变更分析**：Blast Radius 直接定位受影响文件集
4. **持续集成**：GitHub Action 集成，每次 PR 自动生成最小评审上下文
5. **代码考古与依赖分析**：图数据库查询取代 grep + LLM 推理

---

## 局限与挑战

1. **首次构建成本**：Tree-sitter 全仓库解析在百万行级代码上仍需分钟级时间
2. **多语言支持边界**：Tree-sitter 对主流语言（Python/JS/Go/Rust/Java）支持完善，但 DSL、配置文件的语义建模仍不完整
3. **图谱与代码同步**：极端重构（重命名、文件移动）需要主动触发增量重建
4. **图查询 API 的设计哲学**：当前主要面向「blast radius」一类查询，对更复杂的图算法（图嵌入、PageRank-style 影响因子）尚未原生支持

---

## 我的判断

code-review-graph 是 **Anthropic 一手源「Code Execution with MCP」精神的开源实践层落地**——MCP 不只是「让 AI 调用工具的协议」，更是「让 AI 高效访问结构化知识的协议」。code-review-graph 用 18K⭐ 验证了这个抽象层在代码评审场景下的真实价值。

如果你的仓库 > 200 文件且日常使用 Claude Code / Codex / Cursor 做 Code Review，这是当前最值得尝试的工具之一。

---

## 参考资料

- **Anthropic Engineering Blog**：Code Execution with MCP（98.7% Token Reduction）
- **GitHub 仓库**：`https://github.com/tirth8205/code-review-graph`
- **PyPI 包**：`https://pypi.org/project/code-review-graph/`
- **官方文档**：`https://code-review-graph.com`
- **Pair Article**：`articles/tool-use/anthropic-code-execution-with-mcp-98-percent-token-reduction-2026.md`
- **验证日期**：2026-06-14