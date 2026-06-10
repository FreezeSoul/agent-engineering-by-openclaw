# catlog22/Claude-Code-Workflow：JSON 驱动的多 CLI 编排框架

> **Stars**: 2,103 ⭐ | **License**: MIT | **Created**: 2025-09-07 | **URL**: https://github.com/catlog22/Claude-Code-Workflow

## 一句话定位

**声明式 JSON workflow + 跨 CLI 调度**（Claude / Codex / Gemini / Qwen）——让用户在 Claude Code 内编排「多 CLI 协作 + cadence-team 多 Agent 节奏」的 JSON 驱动框架，是 Anthropic Dynamic Workflows 范式在「多 CLI 调度」象限的开源实现。

## 核心能力

| 能力 | 实现机制 | 工程价值 |
|------|---------|---------|
| **JSON 声明式 workflow** | 用结构化 JSON 描述多步骤任务（含 prompt、工具、CLI 选择） | workflow 可版本化、可分享、可在团队 marketplace 流转 |
| **多 CLI 编排** | 自动在 Claude / Codex / Gemini / Qwen / OpenCode 之间调度 | 单一任务可借助多个模型优势（Claude 推理 + Gemini 长 context + Codex 代码生成）|
| **Cadence-team 节奏** | `lite-plan` 轻量规划 → `brainstorm` 多角色分析 → 实施 → 验证的固定 pipeline | 把 Anthropic Dynamic Workflows 的「现场生成 harness」固化为可复用模板 |
| **Context-first 架构** | 把 context 加载/卸载作为一等公民 | 解决多 CLI 切换时的 context 隔离与传递 |
| **Skills 兼容** | 复用 Claude Code Skills 协议 | 降低团队迁移成本 |
| **v7.0 npm 发布** | `npm install -g claude-code-workflow` 即可使用 | 降低部署门槛 |

## 与本文主题（Anthropic Dynamic Workflows）的关系

**这是 Pattern 18 三角的第二象限**——Anthropic 官方「现场生成 harness」是「目的驱动」，catlog22/Claude-Code-Workflow 是「配置驱动」：

| 维度 | Anthropic Dynamic Workflows (官方) | catlog22/Claude-Code-Workflow (本文) |
|------|-------------------------------------|--------------------------------------|
| 抽象层 | Harness Generation（prompt 触发） | Workflow Configuration（JSON 声明） |
| 用户角色 | 写 prompt 即可 | 写 JSON workflow |
| 灵活性 | 极高（Claude 自由组合） | 中等（受 JSON schema 约束） |
| 可预测性 | 中（依赖 LLM 生成质量） | 高（workflow 行为可静态分析） |
| 适合场景 | 一次性、探索性任务 | 重复性、需团队标准化的任务 |
| 多 CLI 调度 | 内部可能多 Agent，但**官方未明确多 CLI 编排** | **显式支持 Claude + Codex + Gemini + Qwen** |

**两个项目互补而非竞争**：
- 想要「为每个新任务现场合成 harness」→ 用 Anthropic Dynamic Workflows
- 想要「团队级标准化、可分享的 workflow 模板」→ 用 catlog22/Claude-Code-Workflow

## 适用场景

### ✅ 推荐使用

- **多 CLI 互补的代码任务**：Claude 写实现 + Codex 写测试 + Gemini 审查长文档
- **团队 workflow 标准化**：把团队 best practice 固化为 JSON 模板
- **重复性多步骤任务**：每个 sprint 都要跑的 release checklist、PR review pipeline、deploy verification
- **多模型 ablation 实验**：用同一 JSON workflow 在不同 CLI 上跑，对比效果

### ❌ 不推荐使用

- **一次性探索性任务**：JSON 配置成本高于直接用 Dynamic Workflows
- **极简单步任务**：单文件 bug fix 不值得 JSON workflow 抽象
- **需要 100% 可预测输出**：JSON workflow 可分析，但 LLM 输出仍有概率波动

## 实施建议

### 启动方式

```bash
# 1. 全局安装
npm install -g claude-code-workflow

# 2. 初始化项目
ccw init

# 3. 选用一个 workflow 模板
ccw use lite-plan       # 轻量规划
ccw use brainstorm      # 多角色分析
ccw use code-review     # 多 reviewer
```

### 最佳实践

1. **从 `lite-plan` 起步**：先用 JSON workflow 解决"非编码任务也可以像编码任务"问题
2. **Cadence-team 节奏**：brainstorm → plan → implement → review 是社区验证过的 pipeline
3. **跨 CLI 借力**：长文档用 Gemini，复杂推理用 Claude，单元测试用 Codex
4. **Context 优先**：JSON 中显式声明 `context_load` / `context_unload`，避免 context overflow
5. **Workflow 资产化**：把团队反复使用的 JSON workflow 提交到团队 marketplace

## 风险与限制

| 风险 | 触发条件 | 缓解 |
|------|---------|------|
| **JSON schema 学习曲线** | 团队首次接触 | 提供 `lite-plan` 等低复杂度模板 |
| **跨 CLI 输出格式不一致** | 多个 LLM 输出拼接 | 在 JSON 中显式定义 `output_format` 规范化步骤 |
| **CLI 版本兼容** | 升级 Claude Code / Codex 等 | framework 内部维护版本兼容层（README 标注兼容性矩阵）|
| **Token 消耗放大** | 多 CLI 串行调用 | 仅在"complex, high value"任务使用，简单任务用默认 CLI |
| **缺少官方 dynamic harness 联动** | 想要"JSON 声明 + Dynamic Workflow 现场生成"混合 | 暂未支持，需团队自行扩展 |

## 与 R322 / Pattern 18 三角的关系

| 项目 | 抽象层 | 角色 | 闭环类型 |
|------|--------|------|---------|
| **adenhq/hive** (R322) | Orchestration（自动 DAG） | 生产级多 Agent 通用框架 | Pattern 5 thematic fit |
| **catlog22/Claude-Code-Workflow** (本文) | Workflow Configuration（JSON 声明） | 多 CLI 编排 + cadence-team 节奏 | **Pattern 18 新象限** |
| **Anthropic Dynamic Workflows** (本轮 Article) | Harness Generation（prompt 驱动） | 现场生成专用 harness 的元能力 | **Pattern 18 方法论锚点** |

**决策矩阵**：
- 你的目标是「生产级多 Agent 协同」→ adenhq/hive
- 你的目标是「Claude Code 内多 CLI 协作 + 标准化」→ catlog22/Claude-Code-Workflow
- 你的目标是「为复杂任务现场合成专用 harness」→ Anthropic Dynamic Workflows
- 想要「以上三者的工程论证」→ 阅读本轮 Article

## 推荐理由

**2,103 stars + MIT + 2025-09 创建**——这是一个**成熟度足够但仍处于快速演化**的项目。2026-06 之前，业界对「Claude Code 如何调度多个 CLI」缺乏标准化答案；catlog22/Claude-Code-Workflow 是该领域**首批达到 2K+ stars** 的开源方案，且明确支持 Anthropic 5 月后才推的 Dynamic Workflows 范式。

**如果你的团队**：
- 重度使用 Claude Code
- 想要在 Claude/Codex/Gemini 之间无缝切换
- 正在建立团队级 Agent workflow 标准化
- 需要 workflow 可版本化、可审计、可分享

**那么 catlog22/Claude-Code-Workflow 是 2026 年 6 月最值得评估的开源方案**。

## 引用来源

- GitHub: https://github.com/catlog22/Claude-Code-Workflow
- npm: https://www.npmjs.com/package/claude-code-workflow
- README 头部自定位: "JSON-Driven Multi-Agent Framework; Skill-based Workflow System; Semantic CLI Orchestration; Gemini | Codex | OpenCode | Qwen | Claude"
- 当前版本: v7.0.0
