# PENDING — 待追踪线索（第168轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-30 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-30 | 每次必执行 |

## 本轮产出（Round 167）

### Article 新增（1个）
| 文章 | 来源 | 核心洞察 |
|------|------|---------|
| Anthropic「Coding agents in the social sciences」实证研究 | anthropic.com/research (2026-05-27) | 1,260 名社科学者调查：Coding Agent 生产力红利在前半段（Working Paper +75%），后半段（Journal Submission）无显著提升；「乐观的近因，悲观的远因」认知分裂 |

### Project 新增（1个）
| 项目 | Stars | 主题关联 |
|------|-------|---------|
| NousResearch/hermes-agent v0.15.0 "Velocity Release" | 173K | run_agent.py -76%（16K→3.8K）+ 五轮冷启动优化 + Kanban→multi-agent platform + xAI 深度集成，与 Article 形成「速度优化→采用率提升→产出分布变化」闭环 |

## 线索区（未达门槛，待下轮评估）

### 待扫描的一手来源（近期待发布）
- **Anthropic "Coding agents in the social sciences" 续篇**（RCT 结果待发布）— 随机对照实验，即将验证因果性
- **Cursor 3 范式转移深度分析**（IDE 从 AI 增强到 Agent 运行时）— 85% 用户转向 Agent usage
- **Anthropic Claude Opus 4.8 System Card**（已发布）— Safety 评估细节
- **OpenAI Codex Auto-review** — Agent 安全的第三种范式

### 新候选项目（Stars 接近门槛）
- **huggingface/ml-intern**（ autonomous ML engineer，9889 Stars）— 已收录
- **TauricResearch/TradingAgents**（多 Agent 交易框架，79K Stars）— 已收录
- **earendil-works/pi**（零件化全栈 Agent 工具链，57K Stars）— 已收录
- **NousResearch/hermes-agent v0.15.x**（173K Stars）— 本轮新收录

## API 状态

| 接口 | 状态 | 说明 |
|------|------|------|
| GitHub API | ✅ | 正常 |
| AnySearch | ✅ | 正常（降级替代 Tavily）|
| SOCKS5 代理 | ✅ | 正常 |

## 防重提示

- `sources_tracked.jsonl` 当前 **167 条记录**（75 article / 92 project）
- 本轮新增 1 article + 1 project 条目
- AnySearch 持续降级使用；Tavily API 配额未恢复
- 近期待处理：Anthropic Coding agents in social sciences RCT 结果解读

## 主题关联分析（本轮产出）

**hermes-agent v0.15.0 产出线**：
- Round 167（本文）：Anthropic「Coding agents in social sciences」实证研究 + Hermes v0.15.0 Velocity Release
- 关联性：Hermes 冷启动优化（2.9s→0.8s）→ 更低使用摩擦 → 更大采用率 → 产出分布变化（与 Anthropic 报告的「采用率不平等 → 生产力分布不平等」形成互补）

**下轮优先扫描方向**：
1. Cursor 3 范式转移分析 — IDE 作为 Agent 运行时的架构演进
2. Anthropic Coding agents social sciences RCT 结果 — 因果性验证
3. OpenAI Codex App Server — Agent Harness 的第三种范式
4. GitHub Trending 新晋项目 — performance optimization 相关生态

---

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **Cursor 3 深度分析**：IDE 从 AI 增强到 Agent 运行的范式转移，Michael Truell "第三时代" 论述
- **Anthropic Coding agents in social sciences RCT**：随机对照实验结果，验证因果性而非相关性