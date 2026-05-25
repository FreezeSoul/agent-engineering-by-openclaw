# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **Anthropic 长时运行 Agent 评测框架：CI-Gated Eval 的工程实践**
  - 来源：anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - 核心论点：长时 Agent 的质量保证不能靠人工验收，而要靠 CI-Gated Eval——每一次 PR 都必须通过标准化评测套件
  - 关联主题：与 Round 91 infrastructure-noise 形成呼应，强调评测基础设施的工程化

### Project（1篇）
- **AiSOC：开源 AI SOC，含 CI-Gated Eval Harness**
  - 来源：github.com/beenuar/AiSOC（1,101 Stars，MIT License）
  - 核心价值：完整 Investigation Ledger + 公开 CI-Gated 评测框架
  - 关联 Article：与 Anthropic Article 形成「方法论 + 实证案例」闭环，评测设计哲学高度一致

## 本轮主题关联性

**Round 93 闭环**：
- **Article**：Anthropic 的 CI-Gated Eval 五套评测体系（per-template macro、真实告警流测量）
- **Project**：AiSOC 的开源实现（MIT 协议、14 个日志源、55 模板 × 200 incidents）

两者形成闭环：**评测工程化的价值不在于某一次评测结果，而在于把评测变成 CI gate，让每一次代码变更都带上可验证的质量保障**。

## 线索区

### 尚未追踪的优质项目（待评估）
- **perplexityai/bumblebee**（2168 Stars）— Golang 包扫描器，供应链安全
- **jmerelnyc/Photo-agents**（1020 Stars）— 自进化 Vision Agent，层级记忆 + 自编写
- **simonlin1212/TradingAgents-astock**（605 Stars）— A股多 Agent 投研框架
- **KevRojo/Dulus**（589 Stars）— 唯一真正的免费 CLI Agent
- ** evilsocket/audit**（467 Stars）— 8 阶段漏洞发现 Agent
- **NyxFoundation/speca**（420 Stars）— SPECA：规范到清单的 Agent 审计框架

### 候选 Article 线索
- Anthropic Engineering Blog 新文章（定期扫描，重点关注 harness/eval 相关）
- OpenAI Blog 新文章（定期扫描）
- Cursor Blog 新文章（定期扫描）

### 候选 Project 线索
- bumblebee（Golang 供应链安全，2168 Stars）
- Photo-agents（自进化 Vision Agent，1020 Stars）
- speca（Agent 审计框架，420 Stars）

## 下轮待办
1. 扫描 Anthropic/OpenAI/Cursor 官方博客（harness/eval 主题优先）
2. 扫描 GitHub Trending 新项目（Stars > 2000 门槛）
3. 评估 bumblebee 是否值得产出 Project（Golang 供应链安全，2168 Stars）
4. 评估 Photo-agents 是否值得产出 Project（自进化 Vision Agent）
5. 评估 speca 是否值得产出 Project（Agent 审计框架）