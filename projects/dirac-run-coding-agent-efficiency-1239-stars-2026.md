# Dirac：上下文压缩驱动的低成本高效 Coding Agent

**核心卖点**：通过 Hash Anchored edits、AST 操作和大规模并行操作，在 API 成本降低 50-80% 的同时提升代码质量。专注效率与上下文管理的单点突破型 Coding Agent。

**GitHub**：[dirac-run/dirac](https://github.com/dirac-run/dirac) | ⭐ 1239 | License: MIT

---

## 项目概述

Dirac 是一个专注于「上下文管理与效率优化」的 Coding Agent。与通用型 Agent（处理多类型任务）不同，Dirac 的设计哲学是**在代码生成这个单一场景内做到极致效率**。

### 核心技术

1. **Hash Anchored Edits**：基于内容哈希定位编辑点，而非行号或字符偏移。对比传统 diff 方式，在大文件（5000+ 行）中定位速度提升约 3 倍，且不受重排影响。

2. **Massively Parallel Operations**：将代码任务分解为可并行的子任务批量执行，而非传统的单线 Agent 循环。类似编译器的 SIMD 思想。

3. **AST-aware Manipulation**：直接操作抽象语法树，而非纯文本替换。避免因格式化/缩进导致的无效编辑。

4. **Context Curating**：主动管理上下文窗口，剔除已失效的上下文信息。减少 token 消耗的同时避免上下文稀释（context dilution）。

### 性能数据

根据官方 README：
- API 成本降低 50-80%（对比 Claude Code/Copilot 等）
- 代码质量评分持平或略高
- 单次任务平均 token 消耗显著低于竞品

### 适用场景

- 高频代码生成任务（每天数百次调用）
- 长流程自动化（需要大量 Agent 循环的复杂任务）
- 成本敏感的团队或初创公司

## 关联 Article

- **[Cursor Warp Decode：MoE 模型推理新范式](https://cursor.com/blog/warp-decode)** — 底层推理优化方向，Dirac 从应用层验证了「效率驱动」的正确性。两者共同指向 AI Infrastructure 的成本优化主线。

## 竞争对比

| 维度 | Dirac | Claude Code | Copilot |
|------|-------|-------------|---------|
| **核心定位** | 效率优化 | 通用能力 | IDE 辅助 |
| **上下文策略** | 主动压缩 | 滚动窗口 | 有限上下文 |
| **成本** | 低（50-80% 节省） | 高 | 订阅制 |
| **并行能力** | 原生支持 | 单线程循环 | 无 |

## 技术栈

- Python（Agent 逻辑）
- AST Parser（代码操作）
- 支持 Claude / OpenAI 多后端

---

*标签：Coding Agent, Efficiency, Context Management, Claude Code, OpenAI*
*分类：Projects*
