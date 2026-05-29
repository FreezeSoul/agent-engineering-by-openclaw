# KevRojo/Dulus：98% 缓存命中率的长程会话 CLI Agent

**stars**: 708 | **language**: Python | **created**: 2026-05-05 | **homepage**: https://dulus.ai

## 概述

[Dulus](https://github.com/KevRojo/Dulus) 是一个 **CLI Agent**，核心卖点是：在 30 亿 Token 的 3 个月会话中保持 **98% 缓存命中率**。支持文件读写、Bash 命令、Grep 搜索、Git 操作、Web 浏览，从终端直接驱动 AI 完成工作。

## 核心创新：长程上下文缓存

Dulus 的核心工程突破是 **上下文缓存机制**：

- **30 亿 Token 会话**：传统 Agent 在长会话中面临上下文膨胀问题
- **98% 缓存命中率**：通过智能缓存策略，大幅降低 Token 消耗
- **3 个月会话**：跨越超长时间周期的状态保持

这种缓存机制与 `context-mode-mksglu`（98% 上下文压缩）形成不同维度的优化：
- **mksglu**：通过上下文折叠（Context Folding）压缩 Token 总量
- **Dulus**：通过智能缓存复用已计算的上下文

## 功能特性

```bash
# Dulus 核心能力
- 📁 文件读写：读取和编辑本地文件
- 🖥️ Bash 执行：运行终端命令
- 🔍 Grep 搜索：快速搜索代码仓库
- 🌐 Web 浏览：搜索互联网获取最新信息
- 📝 Git 操作：提交代码、管理分支
- 🚀 快速出发：30 秒内启动任务
```

## 技术架构推测

Dulus 的高缓存命中率可能基于以下机制：

1. **语义相似度缓存**：相同/相似查询复用已计算结果
2. **增量上下文更新**：仅传递变更部分，而非全量上下文
3. **分层缓存策略**：L1（内存）/ L2（磁盘）/ L3（语义索引）

## 主题关联

- **长程 Agent 会话**：与 `openai-codex-agent-loop-context-window-compaction/` 文章形成「窗口压缩 vs 缓存复用」的互补视角
- **上下文效率优化**：Dulus（缓存命中率）+ mksglu（Token 压缩）+ smallcode（小型 LLM）→ 三种不同的上下文效率优化路径
- **CLI Agent**：与 `deepseek-tui-long-running-agent-session-management/` 项目形成终端 Agent 的架构对照

## 性能对比

| 指标 | Dulus | 传统 Agent |
|------|-------|------------|
| 30 亿 Token 会话成本 | ~2% Token 消耗 | 100% Token 消耗 |
| 3 个月状态保持 | ✅ | ❌ 上下文溢出 |
| 缓存命中率 | 98% | N/A |

## 延伸阅读

- [context-mode-mksglu-98-percent-context-reduction](/articles/projects/context-mode-mksglu-98-percent-context-reduction-2026.md) — 98% 上下文压缩
- [doorman11991-smallcode-ai-coding-agent](/articles/projects/doorman11991-smallcode-ai-coding-agent-small-llms-728-stars-2026.md) — 小型 LLM 优化路径
- [openai-codex-agent-loop-context-window-compaction](/articles/harness/openai-codex-agent-loop-context-window-compaction-2026.md) — Codex 上下文窗口压缩
