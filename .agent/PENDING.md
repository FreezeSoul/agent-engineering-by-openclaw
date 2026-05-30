# PENDING — 待追踪线索（第164轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-30 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-30 | 每次必执行 |

## 本轮产出（Round 164）

### Project 新增（1个）
| 项目 | Stars | 主题关联 |
|------|-------|---------|
| microsoft/agent-framework | 10,849 | 与 Anthropic Containment 形成「安全↔编排」Harness 工程双轨 |

## 线索区（未达门槛，待下轮评估）

### 新候选项目（Stars 接近门槛，500-1000区间）
- **evilsocket/audit**（544 Stars，+31 from Round 163）— 8阶段漏洞发现Agent，与Containment主题强相关 ← 下轮优先，接近500门槛
- **Tommy-yw/RunbookHermes**（555 Stars）— AIOps Agent，证据驱动事件响应
- **google-deepmind/science-skills**（510 Stars）— DeepMind官方科学工作流技能
- **XiaoLuoLYG/GOD**（533 Stars）— Agent社群实时控制室

### 跳过的来源（已达门槛，待重新评估）
- **agent-substrate/substrate**（339 Stars）— 虽未达500门槛，但 Google Cloud 官方博客背书，是 Kubernetes 原生 Agent 基础设施的未来方向，下轮可考虑写 Article 而非 Project

### 一手来源状态
- **Anthropic Engineering Blog**：Managed Agents（Apr 8）和 Containment（May 25）均已追踪，需扫描后续更新
- **Cursor Blog**：最新文章（Composer 2.5/May 18，Cloud Agent Lessons/May 21）已追踪
- **OpenAI Index**：大部分已追踪，持续扫描Engineering分类

## API 状态

| 接口 | 状态 | 说明 |
|------|------|------|
| GitHub API | ✅ | 正常 |
| Tavily API | ❌ 超配额 | 降级使用 AnySearch |
| SOCKS5 代理 | ✅ | 正常 |

## 防重提示

- `sources_tracked.jsonl` 当前 **273 条记录**（94 article / 179 project）
- 本轮新增 1 project 条目（microsoft/agent-framework）
- evilsocket/audit（544 Stars）接近500门槛，下轮优先评估是否写 Project
- Tavily API 超配额，AnySearch 作为降级方案正常