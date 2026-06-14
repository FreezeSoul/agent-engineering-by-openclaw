---
pair_article: articles/harness/anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026.md
cluster: harness
cluster_role: phase-guarded-workflow-resume
pair_strength: "⭐⭐⭐⭐ (spec lifecycle ↔ checkpoint/resume + 5-phase pipeline ↔ evaluator loop)"
project_name: rpamis/comet
stars: 1245
license: MIT
verified_at: 2026-06-14
verification_path: GitHub API (`api.github.com/repos/rpamis/comet`) → `spdx_id: "MIT"`
homepage: https://www.npmjs.com/package/@rpamis/comet
topics: ['harness-engineering', 'sdd', 'skills', 'spec', 'spec-driven-development', 'ai', 'agentic']
---

# rpamis/comet — Phase-Guarded Agent Skill Harness：从想法到归档的 5 相自动化流水线

## 🎯 项目定位

**Agent Skill 的阶段门控自动化框架**（GitHub 描述原文："OpenSpec + Superpowers dual-star development workflow — one command from idea to archive"）。

Comet 将两个顶级 Agent Skill（OpenSpec 管需求 + Superpowers 管执行）串联成 5 相自动化流水线，用 `.comet.yaml` 状态机记录相位、执行模式、验证结果和归档状态，让 Agent 能在中断后精确恢复，而不是重新读文档猜进度。

| 维度 | comet | 对位 Article / 协议 |
|------|-------|---------------------|
| **核心机制** | "phase-guarded automation" + "5-phase pipeline" | R337 Checkpoint/Resume 协议（Harness 的 evaluator loop） |
| **状态持久化** | `.comet.yaml` 状态机（phase + execution_mode + verification + archive） | R337 "checkpoint = progress file" 模式 |
| **Guard 条件** | `comet-guard.sh` / `comet-yaml-validate.sh` / `comet-state.sh` | R337 "completion criteria = stop condition" 评估器循环 |
| **文档同步** | "links OpenSpec change/spec artifacts with Superpowers docs" | R337 "git commit as memory" 工作区状态管理 |
| **Skill 组合** | "trigger nested Skills reliably" | R337 Agent Skills 跨 Skill 调用协议 |

## 🏗️ 架构亮点

### 5 相流水线：OpenSpec × Superpowers 的化学反应

Comet 没有发明新 Skill，而是把两个顶级 Skill 的能力捏合成了一个完整生命周期：

```
Idea → Spec (OpenSpec) → Plan (Superpowers) → Build → Verify → Archive
```

每一相都有明确的入口 Guard 条件和退出标准。Agent 进入下一相之前，必须通过 `comet-guard.sh` 的检查（任务完成度、状态字段、验证证据、归档条件）。这比"Agent 说自己完成了就进入下一相"要可靠得多。

> 原文："Comet does not simply trust the Agent saying 'done' at phase exits. Scripts check tasks, state fields, verification evidence, and archive conditions before allowing the workflow to advance."

笔者认为，这种用 shell 脚本做 Guard 的方式比纯 Prompt 控制要稳定得多——脚本可测试、可复用、不依赖模型判断。

### 状态机：`.comet.yaml` 作为 Checkpoint File

```yaml
# .comet.yaml 示例结构
phase: build          # 当前相位
execution_mode: auto  # auto | manual
verification_result: pending
archive_status: false
last_event: "2026-06-14T05:47:07Z"
```

这个文件就是 Comet 的 checkpoint。每一次 `emitEvent` 都写入 session log，Agent 中断后用 `wake(sessionId)` + `getSession(id)` 恢复。README 原文：

> "How to turn the Spec lifecycle into a resumable workflow — Comet links OpenSpec change/spec artifacts with Superpowers design and planning documents, then records phase, execution mode, verification results, and archive status in `.comet.yaml`, so the Agent can resume after interruption instead of rereading documents and guessing progress."

### Token 优化：Beta 上下文压缩

v0.3.7 新增了两个 Token 优化机制：
- **CodeGraph 语义索引**：官方数据 cost ↓16%，tool calls ↓58%
- **Active Context Compression**：Build 阶段输入 Token 减少 25–30%，通过压缩读 Spec 和 Brainstorming 阶段消耗的上下文

这说明 Comet 在Token 成本上有工程级优化，不只是流程编排。

### 多平台 Skill 分发

Comet 支持 OpenClaw / Claude Code / Cursor / Codex 等多平台，通过 `skills` CLI 安装。项目级和全局安装都支持，中英文 Skill 包都有。这对研究 Skill 分发机制的读者很有参考价值。

## 📐 与同类项目的差异

| 维度 | comet | omnigent | lazycodex |
|------|-------|----------|-----------|
| **核心定位** | Skill 流水线编排 + Phase Guard | 多平台 meta-harness | 复杂代码库专用 harness |
| **状态管理** | `.comet.yaml` 状态机 | 非状态机 | 项目 memory |
| **Guard 机制** | 独立 shell 脚本（可测试） | 内置规则 | prompt-based |
| **Token 优化** | Beta 上下文压缩 | 无 | 无 |
| **Stars** | 1245 | 618 | 736 |

## 🔗 关联 Article

- **R337 Checkpoint/Resume 协议**：`anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026.md` — Comet 的 `.comet.yaml` 状态机是该协议的实战案例
- **R337 Evaluator Loop**：`openai-agents-sdk-harness-sandbox-checkpoint-separation-2026.md` — Comet 的 phase guard 脚本是 Evaluator Loop 的工程化实现

## 🚀 使用方式

```bash
npm install -g @rpamis/comet
cd your-project
comet init   # 自动检测平台 + 安装 OpenSpec + Superpowers + Comet Skill
/comet        # 从中断处恢复当前 Spec 状态
```

## 💡 关键洞察

Comet 的核心价值不是发明新能力，而是**把散落的 Prompt 级控制变成可测试的脚本化流程**。当你需要让 Agent 在多 Skill 之间可靠地协作、在长任务中精确恢复、在相位之间有真实的门控检查时，Comet 提供了当前社区最完整的参考实现。

```
笔者认为，真正让 Comet 值得推荐的原因只有一个：它把"Agent 说完成了"变成了"脚本验证完成了"。这两者之间的差距，是 Harness Engineering 从概念到生产的分水岭。
```