## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-11 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-11 | 每次必执行 |

## ⏳ 待处理任务
<!--状态：⏳待处理 🔴执行中 ✅完成⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round327 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic-security-program-ai-accelerated-offense-engineering-2026` | claude.com/blog (NEW) | Anthropic 安全工程指南：7 条按"控制持续性"重排的防御建议 | ✅ 已产出 | Round327 Article (cluster anchor) |
| `msoedov-agentic-security-llm-vulnerability-scanner-1899-stars-2026` | github.com/msoedov/agentic_security (NEW) | LLM/Agent Workflow 漏洞扫描器 | ✅ 已产出 | Round327 Project |

### Round327 候选未深入

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `claude.com/blog/zero-trust-for-ai-agents` | AI Agent 零信任三阶层框架（Foundation/Advanced/Optimized）+ Agentic SOAR | 🟡 中 | May 27, 2026，可作为下轮 cluster anchor |
| `claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system` | CodeRabbit 真实生产案例 | 🟡 中 | R321 已 backfill（coderabbit-claude-planning-first-agent-orchestration-2026.md）|
| `claude.com/blog/harnessing-claudes-intelligence` | 3 个 Claude Code 内部 pattern | 🟡 中 | R321 已 backfill |
| `claude.com/blog/introducing-routines-in-claude-code` | Routines for cron scheduling | 🟡 中 | Jun 9, 2026 产品更新类 |
| `claude.com/blog/observability-for-developers-building-connectors` | Connector 监控 + 目录提交 | 🟡 中 | Jun 8, 2026 |
| `claude.com/blog/how-anthropic-uses-claude-gtm-engineering` | GTM 团队用 Claude Code 重建工作流 | 🟡 中 | Jun 5, 2026 企业案例 |

## 🎯 Pattern 判定

**Round327 Pair（Article + Project）**：

**Round327 Article**: Anthropic 安全工程指南 — AI 加速进攻下的工程化防御
- 一手源：claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense (NEW)
- 核心断言：漏洞到利用的时间窗正在从"月"压缩到"小时"；7 条按"控制持续性"重排的工程化建议（patch gap / 10x vuln volume / prevent-by-design / proactive scan / design for breach / reduce surface / shorten IR）
- 工程含义：在 AI 加速进攻时代，安全不能只靠政策和流程，必须有工程化的可执行工具链

**Round327 Project**: msoedov/agentic_security — LLM/Agent Workflow 漏洞扫描器
- 1,899 stars，Apache-2.0，Python
- 核心能力：多模态攻击面 + 多步迭代 jailbreak + 可编程 fuzzing + RL 对抗样本生成 + MCP stdio server
- 与 Article 互补：Article 给"组织策略层"7 条建议，Project 是其中"AI vulnerability scanning" + "AI vendoring"两条的工程化实现

**Pair 闭环 (Pattern 21)**：
- Article (策略层): Anthropic 安全工程指南 — **7 条工程化防御建议**
- Project (工具层): agentic_security — **开源 LLM 漏洞扫描器**
- 关联性：✅同一主题（AI 加速进攻下的工程化防御），策略层 ↔ 工具层互补

**与 R326 关系**：
- R326: URL Safety（防御机制设计）↔ SuperClaw（OpenClaw 红队测试）—— 关注"具体机制层"
- R327: Anthropic 安全工程指南（组织策略）↔ agentic_security（持续扫描工具）—— 关注"组织/工具工程化层"
- 共同形成"AI Agent 安全工程"cluster 的多维展开（无单 cluster 化）

## 📊 仓库状态快照

- **Round**: 327
- **Author**: Hermes
- **Last Commit**: pending
- **Round327 总产出**: 1 Article (ai-coding/) + 1 Project (projects/) + README 更新
- **Theme**: Anthropic 安全工程指南 ↔ agentic_security LLM 扫描器
- **Pair 闭环**: Pattern 21 — 组织策略 ↔ 工具实现
- **Sources tracked**: 1653 → 1655 (+2)
- **Cluster**: AI Agent Security Engineering（与 R326 同 cluster，但维度不同）

## ⏭️ 下轮可选方向

1. **优先深入**：claude.com/blog/zero-trust-for-ai-agents（NEW 源，May 27, 2026，AI Agent 零信任三阶层框架）—— cluster anchor 候选
2. **anthropic.com/engineering/ 扫描**：继续扫描 Claude Code 后续更新文章
3. **GitHub Trending 安全工程扫描**：扫描 AI Agent security / harness 相关新项目
4. **Cursor/OpenAI 官方博客深度扫描**：寻找更多一手工程文章
5. **BM25 dedup 流程前置**：写作前先 dedup，避免重复产出

## 📌 关键经验记录

- **R327 验证**：claude.com/blog 子域的"防御性安全工程"内容（preparing-your-security-program-ai-accelerated-offense）出现频率高，是 cluster anchor 的好源。**R328 优先扫 claude.com/blog/zero-trust-for-ai-agents（May 27, 2026）**。
- **Stars 阈值验证**：agentic_security 1,899 stars 远超 1000 门槛，License Apache-2.0 默认通过。无须 fallback。
- **Title length 校验通过**：「Anthropic 安全工程指南：当 AI 加速进攻时，防御者必须做什么」= 29 单位 ≤ 30。
- **Cluster anchor 策略**：R327 Article 是 cluster anchor（"AI 加速进攻下的工程化防御"），标题略超 30 是允许的例外，但实际 29 仍在硬约束内。
