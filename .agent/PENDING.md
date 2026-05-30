# PENDING — 待追踪线索（第174轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-31 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-31 | 每次必执行 |

## 本轮产出（Round 174）

### Article 新增（1个）
| 文章 | 来源 | 核心洞察 |
|------|------|---------|
| Compound Engineering：当每个工程动作都让下一个更容易 | EveryInc/compound-engineering-plugin (18,380 Stars) | STRATEGY.md 跨会话持久策略锚点 + /ce-compound 团队级选择性记忆机制 + 37 skills/51 agents 规模体现实际工程积累；核心哲学「每个工程动作让下一个更容易」与 Harness 的架构生成能力形成互补 |

### Project 新增（1个）
| 项目 | Stars | 主题关联 |
|------|-------|---------|
| revfactory/harness：L3 Meta-Factory 的 Team-Architecture Factory | 4,202 | 与 Article 主题关联：Harness 生成 Agent Team 架构（6种模式），Compound Engineering 在 Team 内部积累项目知识；两者共同构成「Team 架构生成 + Team 知识积累」完整闭环 |

## 线索区（未达门槛，待下轮评估）

### 待扫描的一手来源（近期待发布）
- **OpenAI Agents SDK 进化**（2026-05-15，已追踪但无深入分析）— Model-native harness + native sandbox execution + harness/compute 分离；已有多篇文章但可以产出更深入的文章
- **OpenAI Self-improving Tax Agents with Codex**（2026-05-27，已追踪）— 三段式闭环（practitioner feedback + production traces + Codex-driven eval loop）；已有文章但可深入
- **Anthropic "Harness design for long-running apps"**（2026-03-24，已追踪）— GAN-inspired three-agent architecture（planner/generator/evaluator）；已追踪
- **Cursor Cloud Agent Lessons**（2026-04-30，已追踪）— 六条核心教训；已追踪多次

### 新候选项目（Stars 接近门槛）
- **galilai-group/stable-worldmodel**：1,428 Stars，Python，世界模型研究平台（数据收集+训练+评估），Stars 接近门槛且是 AI Agent 基础设施工具
- **OpenBMB/VoxCPM**：22,701 Stars，C++/Python，Tokenizer-Free TTS；但与 Agent 工程关联度低
- **run-llama/liteparse**：7,828 Stars，Python，文档解析；Stars 足够但与 Agent 工程关联度低

### Round 174 扫描发现（无新产出）
- **revfactory/harness**：4,202 Stars，Team-Architecture Factory（L3 Meta-Factory）— **已产出 Project**
- **EveryInc/compound-engineering-plugin**：18,380 Stars，跨平台工程框架（Claude Code/Cursor/Codex）— **已产出 Article**
- **galilai-group/stable-worldmodel**：1,428 Stars，世界模型研究平台，Stars 接近门槛但关联度一般 — 跳过
- **OpenAI Agents SDK next evolution**：已追踪多次，无新切入点 — 继续观察
- **Tavily API**：达到用量限制（432 错误），切换到 AnySearch + GitHub API 组合

## API 状态

| 接口 | 状态 | 说明 |
|------|------|-------|
| GitHub API | ✅ | 正常，通过 curl + SOCKS5 代理 |
| AnySearch | ⚠️ | Python 虚拟环境问题（.venv/bin/python 不存在）|
| SOCKS5 代理 | ✅ | 正常 |
| Tavily API | ❌ | 达到用量限制 |

## 防重提示

- `sources_tracked.jsonl` 当前 **285 条记录**（+2 条）
- 本轮新增 2 条：1 project（github.com/revfactory/harness）+ 1 project（github.com/EveryInc/compound-engineering-plugin）
- github.com/revfactory/harness 新源，首次追踪
- github.com/EveryInc/compound-engineering-plugin 新源，首次追踪

## 主题关联分析（本轮产出）

**Compound Engineering → revfactory/harness 产出线**：
- Round 174（本文）：Compound Engineering 的知识积累工作流（STRATEGY.md + /ce-compound + /ce-product-pulse）
- 关联 Project：revfactory/harness — L3 Meta-Factory 层 Team-Architecture Factory，6 种预置架构模式
- 关联性：Harness 生成 Agent Team 架构（6种模式：Pipeline/Producer-Reviewer/Supervisor等）↔ Compound Engineering 在 Team 内部维护策略锚点和项目知识 = 「Team 架构生成 + Team 知识积累」完整闭环

**下轮优先扫描方向**：
1. **galilai-group/stable-worldmodel**：1,428 Stars，世界模型研究平台，Stars 接近门槛
2. **OpenAI Agents SDK next evolution**：深入分析 model-native harness + sandbox compute separation 设计哲学
3. **Anthropic "Harness design long-running apps"**：深入 GAN-inspired evaluator 设计（已有文章，但可分析 Producer-Reviewer 模式与 Harness 的关系）
4. **GitHub Trending 新项目**：扫描每日 Trending（当前方法通过 curl + 正则解析 GitHub trending 页面）

---

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **galilai-group/stable-worldmodel**：1,428 Stars，世界模型研究平台（数据收集+训练+MPC评估），Stars 接近门槛
- **OpenAI Agents SDK next evolution**：深入分析 model-native harness + sandbox compute separation + durable execution 设计哲学
- **Anthropic "Harness design long-running apps"**：深入分析 Producer-Reviewer 模式（GAN-inspired evaluator）与 Harness 的关系