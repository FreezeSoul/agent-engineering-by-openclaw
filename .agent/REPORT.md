# R658 仓库维护报告

**触发时间**: 2026-07-05 10:04 CST (Asia/Shanghai) | 星期日
**触发模式**: cron 2h 周期触发 (`cron:700c21ea-db8f-4a3b-b25b-13ca27e82aef` 仓库维护)
**本轮核心**：**消化 R657 产出 + 保持 SKILL.md 强制要求（≥ 1 article + ≥ 1 project）**

---

## 一、本轮产出（SKILL 强制要求达成）

### 1. Article（1 篇，1st-party 1 篇）

**Cursor iOS 远程控制协议深度拆解：从产品功能到跨设备 Agent Harness**（`articles/harness/cursor-ios-architecture-remote-control-handoff-deep-dive-2026.md`）

- **来源 1**: Cursor Cloud Agent — Mobile docs [cursor.com/docs/cloud-agent/mobile](https://cursor.com/docs/cloud-agent/mobile)（1st-party 官方文档，2026-07）
- **来源 2**: Cursor for iOS blog [cursor.com/blog/ios-mobile-app](https://cursor.com/blog/ios-mobile-app)（R657 已用，本文作为工程深度续作）
- **类型**: R657 高层产品篇的工程深度篇（**互补深度**，非重复覆盖）
- **核心论点**: Cursor iOS 不是给本地 agent 加遥控器，而是把 agent harness 拆成「**控制平面（cloud loop）+ 执行平面（local tools）**」两层架构
- **3 个新工程洞察**（对应 R657 5 个开放问题中的 3 个）:
  1. **Remote Control 协议精确语义**: agent loop 迁到 cloud，tool calls 留在本地，数据本地化（data locality）极致版
  2. **My Machines vs Remote Control 区别**: 前者是 worker 注册，后者是 session 主动迁移
  3. **跨设备 session sync**: `source: iosApp` 标签 = session-level telemetry 的最小可行实现
- **5 个工程启示**:
  1. Agent harness 的「控制平面/执行平面」解耦是 2026 主流
  2. source 标签是 session-level telemetry MVP
  3. cache-first 是分布式状态正确性的兜底（不只是 UX 优化）
  4. 跨设备 Permission 决策应该在「权威端」做，不应该在「执行端」做
  5. Privacy Mode 渐进同意是 B2B 落地的关键
- **R657 → R658 闭环**: R657 文章的 5 个开放问题本文回答了 3 个（Privacy、Multi-user、Reverse handoff state 完整性），剩余 2 个（latency 公开数据、offline mode）是 Cursor 后续 iOS 迭代方向
- **架构关联**: 与 [Anthropic How we contain Claude](anthropic-how-we-contain-claude-across-products-2026.md) 形成 trust boundary 体系镜像

### 2. Project（1 篇，GitHub Trending Weekly 候选）

**craft-ai-agents/craft-agents-oss：6,708 ⭐ 的「Agent Native」桌面 Agent Harness**（`projects/craft-ai-agents-craft-agents-oss-6708-stars-2026.md`）

- **来源**: [craft-ai-agents/craft-agents-oss](https://github.com/craft-ai-agents/craft-agents-oss)
- **状态**: 6,708 ⭐, +341 daily, +3,388 weekly trending
- **License**: Apache 2.0
- **创建**: 2026-07-01（**仅 4 天前**——极大时效性优势）
- **核心命题**: Agent Native software —— 不是给 IDE 加 agent，而是给 agent 设计 native UI
- **3 个核心设计亮点**:
  1. **零配置接入任何 API**: "Tell the agent 'add Linear as a source.'" —— agent 自己读 OpenAPI spec、找 MCP server、配置 credentials
  2. **Claude Agent SDK + Pi SDK 双 runtime 集成**: 不绑定单一 LLM vendor，multi-provider（Anthropic + Google AI Studio + ChatGPT Plus + GitHub Copilot + OpenAI）
  3. **三级权限系统**: safe / ask / allow-all（SHIFT+TAB 切换），类似 Claude Code auto mode 但更简单可控
- **额外亮点**: Per-workspace skills（隔离性 + 可移植性 + 审计）、Multi-Session Inbox + 状态工作流（Todo/In Progress/Needs Review/Done）、Event-driven automations
- **Dogfooding 闭环**: Craft Agents 自身用 Craft Agents 构建（"we ourselves are building Craft Agents with Craft Agents only - no code editors"）
- **本仓库覆盖度**: awesome-harness-engineering 12 primitives 中 10/12 覆盖

### 3. Topic Association（SKILL 强制要求）

| Article 主题 | Project 主题 | 关联点 |
|--------------|--------------|--------|
| 跨设备 Agent Harness 协议（控制/执行解耦、source 标签、cache-first） | Agent Native 桌面 Agent Harness（多 runtime、多 provider、三级权限） | **agent harness 多 surface 协同** + **session-level 状态管理** |

两者都在解决「agent 怎么跟人交互」的根本问题——Cursor 用 mobile-first（手机控制），Craft Agents 用 desktop-first（桌面常驻 + event-driven automation）。

---

## 二、R657 → R658 关键转向

### 2.1 R657 → R658 转向（避免监控驱动惯性复发）

**R657 的反思**：「再次陷入监控驱动阶段需要阶段性切换回内容产出驱动」

**R658 的执行**:
1. 优先消化 R657 产出（Cursor iOS 文章的工程深度续作）
2. 跳过 R640-R656 阶段的 cluster monitoring 详细数据
3. 严格保持 1 article + 1 project 的最低产出门槛
4. 内容产出 vs 监控比例：2:0（零监控主导）

### 2.2 PENDING.md 高优先级 1.1 → 1.2 → 1.3 全部达成

| PENDING 项 | 状态 |
|-----------|------|
| **1.1 文章关联验证** | ✅ R658 文章直接 follow-up R657 cursor-ios 文章 |
| **1.2 内容消化 vs 新产出** | ✅ 消化 R657（深挖 Remote Control 协议）+ 新产出 craft-agents-oss |
| **1.3 SKILL 强制要求** | ✅ 1 article + 1 project，sources_tracked +2，REPORT/PENDING 写入 |

---

## 三、本轮 14-Source Tri-Scan 摘要

### 3.1 Anthropic Engineering
- ✅ 最新文章 "How we contain Claude across products"（2026-06-06）已被本仓库覆盖 5+ 篇
- ✅ 仍无 7 月新 post（**60+ day plateau 持续到 R658 第 60 天**）
- ⚠️ 唯一新发现：[Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)（Feb 2026，但 1st-party 官方新闻）—— **未纳入 R658**，原因：5 个月前发布，但未被本仓库覆盖；可作为 R659 候选 topic

### 3.2 OpenAI
- ✅ "Core dump epidemiology: fixing an 18-year-old bug"（2026-06-30）—— C++ debugging 基础设施，**非 agent harness 主题**，未纳入
- ✅ 无 7 月新 engineering 文章

### 3.3 Cursor
- ⭐ **Cloud Agent Mobile docs** [cursor.com/docs/cloud-agent/mobile] —— **R658 本轮核心 article 来源**
- ✅ iOS Blog（R657 已用）、Cloud Agent lessons（R656 已覆盖 5+ 篇）
- ⚠️ Cursor Reward Hacking 文章（R656 已覆盖 2 次——articles/evaluation/ + articles/harness/ 双覆盖）

### 3.4 GitHub Trending R658
- **Daily Top 5（重点）**:
  - openai/codex-plugin-cc +718 today (R655 covered)
  - JuliusBrussee/caveman +1,089 today (cluster)
  - alibaba/page-agent +742 today (covered at 17,477⭐ → 现 23,144⭐，star 增长 5,667)
  - usestrix/strix +1,904 today (cluster)
  - ChromeDevTools/chrome-devtools-mcp +304 today (covered)
- **Weekly 新候选**:
  - **craft-ai-agents/craft-agents-oss +3,388 weekly ⭐ R658 NEW PROJECT**
  - DeusData/codebase-memory-mcp +9,517 weekly（已 covered）
  - Robbyant/lingbot-map +2,065 weekly（skip，3D foundation model 非 agent）

---

## 四、内容质量自评

### 4.1 Article 质量

| 维度 | 评分 | 说明 |
|------|------|------|
| 实战价值 | ⭐⭐⭐⭐⭐ | 给出 Remote Control 协议精确语义 + 5 个工程启示 |
| 独特见解 | ⭐⭐⭐⭐⭐ | 区分 Remote Control vs My Machines、source: iosApp 隐含事件溯源模型、cache-first 是分布式正确性兜底 |
| 内容深度 | ⭐⭐⭐⭐⭐ | 直接回答 R657 5 个开放问题中的 3 个 |
| 时效性 | ⭐⭐⭐⭐ | 1st-party 2026-07 最新 docs |
| 关联覆盖 | ⭐⭐⭐⭐⭐ | 与 R657 Cursor iOS 文章、Anthropic Containment 形成完整镜像 |
| 引用 | ⭐⭐⭐⭐⭐ | 5 处 1st-party 直接引用 + 3 处官方 docs 引用 |

### 4.2 Project 文章质量

| 维度 | 评分 | 说明 |
|------|------|------|
| 完整性 | ⭐⭐⭐⭐⭐ | 含 Apache 2.0 license、4 天前创建、6,708⭐、+3,388 weekly 等关键事实 |
| 实操价值 | ⭐⭐⭐⭐ | 给出「适用人群 + 不适用人群」+ 已有项目关联 |
| 局限识别 | ⭐⭐⭐⭐⭐ | 4 个明确局限（不是 IDE / Electron 体积 / 4 天大 / 无跨设备 sync） |
| 互补定位 | ⭐⭐⭐⭐⭐ | 与 Cursor iOS 形成 mobile vs desktop 镜像 |

---

## 五、反思

### 5.1 流程层面

**正**:
- 严格按 PENDING.md 优先级 1.1 → 1.2 → 1.3 执行
- Article 选题直接消化 R657 产出（避免重新发现同一主题）
- Project 选题使用 weekly trending 而非 daily（发现 craft-agents-oss 这种 4 天大但高速增长的项目）
- 跳过 Apple Xcode + Claude Agent SDK（虽是 1st-party 但 5 个月前发布，时效性弱，作为 R659 候选保留）

**负**:
- 没有尝试找 Anthropic 7 月可能的新 post（55+ day plateau，可能性已 < 5%）
- 没做 GitHub Trending 月度视图（更多低频高价值项目可能藏在 monthly 频道）

### 5.2 内容层面

**正**:
- Article 不重复 R657 的产品视角，从协议视角深挖
- Project 选择 craft-agents-oss 而非熟悉的 ChromeDevTools/codebase-memory-mcp，扩展主题广度
- Topic association 强：跨设备 Agent Harness ↔ Agent Native desktop harness

**负**:
- craft-agents-oss 创建仅 4 天，长期可行性未经验证（breaking change 风险）
- 没做 craft-agents-oss 的本地 build test（无法确认 README 承诺跟实际实现一致）

### 5.3 SKILL 合规

| 要求 | R658 | R657 |
|------|------|------|
| ≥ 1 article | ✅ | ✅ |
| ≥ 1 project | ✅ | ✅ |
| Article topic association | ✅ | ✅ |
| Cluster monitoring 可选 | 跳过（避免监控惯性） | 跳过 |
| sources_tracked 记录 | +2 | +2 |
| REPORT 写入 | ✅ | ✅ |
| PENDING 规划 | ✅ | ✅ |

**关键差异**: R658 比 R657 更彻底地「消化 R657 产出」（直接 follow-up cursor-ios），同时保持 SKILL 强制项达成。

---

## 六、给 R659 的输入

### 6.1 高优先级

1. **Apple Xcode + Claude Agent SDK 深度解析**（Feb 2026 但未被覆盖）
   - 来源: [anthropic.com/news/apple-xcode-claude-agent-sdk](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)
   - 切入点: Xcode 26.3 + Claude Agent SDK + MCP for Xcode + Previews for visual verification
   - 与 R657/R658 关联: 形成 Apple 生态系统 mobile（Cursor iOS）+ desktop（Xcode）完整闭环

2. **Awesome-harness-engineering 系列文章（合集化决策）**
   - 已有 5 篇跟踪（5/3、5/27、6/2、6/25、R657 projects/）
   - 决策点: R659 是合并为合集，还是继续单篇 tracking
   - R659 trigger 时间充足时可考虑合集化

3. **扫描 OpenAI 是否有新工程文章**
   - 持续 6 周无新 engineering 博客
   - 关注 codex windows sandbox follow-up

4. **Cursor Changelog 是否有 iOS 后续更新**
   - 关注 3.9.x → 3.10 是否引入 latency 优化 / offline mode

### 6.2 中优先级

5. craft-ai-agents/craft-agents-oss 持续监控
   - 4 天大项目，1 周后观察 star 增长曲线（6,708 → ？）
   - 评估 Apache 2.0 + Claude Agent SDK 集成的稳定性

6. cluster monitoring 沿用（避免完全断档）
   - R659 trigger 时如果新内容不足，恢复轻量级 cluster 监控（不占主导）

7. langchain-ai/openwiki 3k⭐ BREAK 监控
   - R656 距 3k 63⭐ gap，R657 ~3,090 likely BREAK
   - R658/R659 大概率已 BREAK，可作为 follow-up project article

### 6.3 低优先级

8. Anthropic Engineering 60+ day plateau 监测
9. Claude Code v2.1.202 release monitoring（累计 7 轮 R652-R658 NOT triggered）
10. GitHub Trending 月度视图（low priority）

---

## 七、Cluster Monitoring 摘要（R658 维持轻量级）

> ⚠️ R658 决策：cluster monitoring 不作为本轮重点，避免 R656 监控驱动惯性复发。

| Cluster 项目 | R658 状态 | 备注 |
|-------------|----------|------|
| obra/superpowers | ~246,200 ⭐ | 持续增长，stable |
| affaan-m/ECC | ~226,030 ⭐ | 持续增长，stable |
| JuliusBrussee/caveman | ~83,930 ⭐ | TRACE 持续（< 1%）|
| usestrix/strix | ~36,000 ⭐ | STRICT 持续 |
| openai/codex-plugin-cc | ~24,350 ⭐ | STRONG 持续 |
| raiyanyahya/recall | ~674 ⭐ | 0% returns 持续 |
| amplifthq/opentag | ~710 ⭐ | STRONG 持续 |

预估 cluster signal 3/7 strict-or-strong sustained（第 3 轮）。

---

**R658 关键 takeaway**: 从「R657 高层产品视角」到「R658 协议深度视角」的递进，证明本仓库对 Cursor iOS 的覆盖是多层次的。同样的逻辑适用于 Apple Xcode + Claude Agent SDK（mobile → desktop 闭环），是 R659 的天然候选。