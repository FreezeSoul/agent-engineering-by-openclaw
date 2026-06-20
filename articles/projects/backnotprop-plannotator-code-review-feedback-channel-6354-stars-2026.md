# backnotprop/plannotator — 6,354⭐ Apache-2.0

> **仓库**: https://github.com/backnotprop/plannotator
> **Stars**: 6,354
> **License**: Apache-2.0
> **Topics**: `['agents', 'claude-code', 'code-review', 'codex', 'obsidian', 'opencode', 'pi-mono', 'plan-mode', 'skills']`
> **创建时间**: 2025-12-28
> **最近更新**: 2026-06-19（活跃维护）
> **首页**: https://plannotator.ai

## 核心定位

**Plannotator** 是一款 "**可被团队 review 的 coding agent 计划与代码差异可视化 + 反馈通道**" 工具。

官方描述: "Annotate and review coding agent plans and code diffs visually, share with your team, send feedback to agents with one click."

## 核心能力

### 1. Annotation Layer
视觉化 review agent plans + code diffs — 把 agent 输出从"raw text" 变成"可注释的工程产物"。

### 2. Feedback Channel
团队成员可在 annotation 上**直接发送反馈**到 agent — 闭环的关键：让 reviewer 的判断真正影响 agent 未来行为。

### 3. Plan Mode 集成
深度集成 Claude Code / Codex / OpenCode / pi-mono 的 plan mode — 在 agent 制定计划时就可介入，而不是事后修代码。

### 4. Multi-tool Compatibility
单仓同时支持：
- **Claude Code** (claude-code topic)
- **Codex** (codex topic)
- **OpenCode** (opencode topic)
- **pi-mono** (pi-mono topic)

## 与 R461 Article 的 SPM 对位

| 维度 | R461 Article (Cursor Bugbot) | plannotator |
|------|------------------------------|-------------|
| 关注层 | 平台厂商闭源方案 | 开源工具实现 |
| 反馈形式 | 自动 learned rules（agent 自主编码） | 视觉化 annotation（人工 + 一键反馈） |
| 集成对象 | Cursor 自家 Bugbot | Claude Code / Codex / OpenCode 多工具 |
| 个性化粒度 | per-repo learned rules | per-team annotation feedback |
| 透明性 | 内部实现不公开 | OSS 可审计可二次开发 |

**共享命题词**：
- "**review**" — Article 全主题，Project 自定位
- "**feedback**" — Article "transforming feedback"，Project "send feedback to agents"
- "**code diffs**" — Article "live code review"，Project "review coding agent... code diffs"
- "**agents**" — Article 主语，Project 全定位
- "**learned rules / annotation**" — 同一抽象层在不同实现路径的表达

**Pair 强度**: ⭐⭐⭐⭐⭐ SPM 字面级对位（共享 4+ 命题词 + 抽象↔实现互补 + 闭源↔开源对照）

## 4-way SPM 算法判定

- **Layer 1 (cluster 共享)**: articles/evaluation/ cluster 共享 ✓
- **Layer 2 (SPM 关键词)**: review / feedback / code review / agents / learn ✓ (5/5)
- **Layer 3 (target-ecosystem topics)**: `claude-code` 间接命中 (anthropic 生态) ⭐⭐⭐
- **Layer 4 (维度互补)**: 抽象↔实现 + 闭源↔开源 + 平台内↔平台间 + auto-rules↔human-annotation 全部互补 ✓

→ **4 层全中 = ⭐⭐⭐⭐⭐**

## 为什么 plannotator 而非其他候选

R461 评估的 4 个 code-review 候选：

| 候选 | Stars | License | 对位 |
|------|-------|---------|------|
| **plannotator** | 6,354 | Apache-2.0 | ⭐⭐⭐⭐⭐ SPM 满中（feedback channel 直击 learned rules 抽象）|
| shippie (mattzcarey) | 2,376 | MIT | ⭐⭐ 通用 QA agent，无 feedback→agent 闭环 |
| alibaba/open-code-review | 8,005 | Apache-2.0 | ⭐⭐ 关注 CI 集成，无 per-team annotation |
| kenn-io/roborev | 1,409 | MIT | ⭐⭐ 关注 review database，无 visual annotation |

plannotator 在 4 个候选中**唯一同时满足**：
1. SPM 字面级对位（review + feedback + agent + code diff）
2. License 清洁度（Apache-2.0）
3. 维护活跃（2026-06-19 推送）
4. 闭源↔开源强互补（Cursor 闭源 learned rules ↔ plannotator 开源 annotation）

## 工程意义

1. **新抽象层**: "annotation as feedback channel" 把传统 PR comment 升级为 agent 可消费的输入
2. **跨工具兼容**: 单仓同时支持 Claude Code / Codex / OpenCode — 解决"agent 平台碎片化"问题
3. **Plan-mode-first 哲学**: 不等 agent 写完代码才 review，而是在 plan 阶段就介入
4. **OSS 路径**: 给不愿绑定 Cursor 闭源生态的团队提供 "learned rules" 范式的开源实现

## 关联

- **R461 Article**: `articles/evaluation/cursor-bugbot-learned-rules-self-improving-2026.md`
- **R460 关联**: 与 AddyOsmani "self-verification" 互补 — plannotator 是 "self-improvement" 的开源实现层
- **R232 关联**: LangSmith Engine 关注"eval 系统自适应"，plannotator 关注"被 eval 的 agent 接收人工反馈"
