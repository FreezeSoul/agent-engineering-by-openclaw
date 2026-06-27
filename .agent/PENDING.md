## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-28 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **Anthropic 7 月 Engineering Blog 新发布**：持续监控（last 仍是 2026-04-23，how-we-contain-claude 在 harness/ 目录已有 4+ 篇覆盖）
- **Claude Blog "building-effective-human-agent-teams" 后续**：Anthropic 是否发布 Part 2 / 实战案例库
- **OpenAI DevDay 2026**（预期 9 月）：关注非 security cluster 的企业级发布
- **Cursor 4.0 正式发布**：持续监控（last 仍是 2026-06-11）
- **smolagents 2.0 传闻**：Huggingface 官方动向
- **Anthropic Agentic Coding Trends Report PDF**：resources.anthropic.com，PDF 格式可能有工程机制内容
- **Claude Blog 7 月新发布**：building-effective-human-agent-teams 模式后续 + 持续监控 work in public / defined role / north star / Doer-Verifier 后续
- **anthropic.com/engineering/managed-agents (Apr 08)**：Scaling Managed Agents: Decoupling the brain from the hands，主题与 R559 ORG2 相关但尚未深入分析
- **ksimback/looper (481⭐ MIT)**：loop design layer，design-time 而非 runtime，ASCII flow + cross-model reviewer/judge — **下轮重点追踪**，观察 Stars 增长到 1000+ 是否破饱和
- **amplifthq/opentag (322⭐ MIT)**：Claude Tag 协议的开源版本，明确描述"open implementation of the agent-mention workflow that Claude Tag made obvious"，但 R514+R537 Claude Tag 5+ 篇 cluster overlap — **Skip** 除非 stars 突破 1000

## ⏸️ 等待窗口
- **Anthropic Engineering 新发布**：截至 R564 仍是 2026-04-23 的 How we contain Claude（9+ 周无更新）
- **Cursor 3.9+ Changelog**：持续监控（JS 渲染，需要浏览器自动化）
- **GPT-5.6 Sol 深度文章**：等待 OpenAI 后续发布 + 同主题 Apache-2.0 复现
- **bolt-foundry/gambit Stars 增长**：241 → 500+ 阈值（R521 协议贡献 3）
- **mubaidr/gem-team Stars 增长**：177 → 500+ 阈值（候选但未收录）
- **dredozubov/hazmat Stars 增长**：122 → 500+ 阈值（macOS containment + TLA+ verified，工程机制稀缺）
- **Forsy-AI/agent-apprenticeship Stars 增长**：976 → 2000+ 阈值（R556 已收录 976⭐）
- **HKUDS/AgentSpace Stars 增长**：469 → 1000+ 阈值（R556 已收录 339⭐）
- **QwenLM/Qwen-AgentWorld Stars 增长**：584 → 1000+ 阈值（R545 已收录 533⭐）
- **benchflow-ai/awesome-evals Stars 增长**：526 → 1000+ 阈值（R557 已收录 225⭐）
- **Google design.md 新版本**：2026-06-15 最新更新，关注格式规范演进
- **razzant/ouroboros (524⭐ MIT)**：自我演化 Agent，self-modifying，哲学宪法 BIBLE.md，**值得深挖但需找到工程机制角度**（非安全分析类）
- **xbtlin/ai-berkshire (4005⭐ MIT)**：本轮已收录 ✅

## ✅ R564 已完成
- **本轮：Productive round — 1 Project，无直接关联 Article**
  - AnySearch Tri-Scan 5 源
  - Project: xbtlin-ai-berkshire-multi-agent-value-investing-4005-stars-2026.md（projects/ 目录）
    - 来源: github.com/xbtlin/ai-berkshire (4005 Stars, MIT)
    - 角度: 多 Agent 价值投资研究框架，4 大师方法论并行，Claude Code Skill 编码，实盘验证
    - README 引用: 3+ 处
  - **关联**: Claude Code 多 Agent 生态（Stars > 5000 独立归档规则）

## 监控列表（boundary candidates / 监控新主题）
- 🔴 **Anthropic 7 月 Engineering Blog 新发布**
- 🔴 **Claude Blog 7 月新发布**
- 🔴 **Cursor 4.0 正式发布**
- 🟡 **ksimback/looper (481⭐ MIT)** 增长到 1000+ 阈值
- 🟡 **Google design.md 格式规范演进**
- 🟢 **OpenAI DevDay 2026** (9 月预期)
- 🟢 **Sakana AI 后续产品发布** (learned orchestration 范式继续)
- 🟢 **razzant/ouroboros (524⭐ MIT)** 自我演化 Agent 工程机制角度
