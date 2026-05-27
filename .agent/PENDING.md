# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **cursor-continually-improving-our-agent-harness-2026.md**：Cursor Stefan Heule & Jediah Katz 的 Harness 量化迭代方法论，来源 cursor.com/blog/continually-improving-our-agent-harness（2026-04-30）。核心：Harness 质量 = 量化评估 × 系统化迭代 × 深度模型适配；Keep Rate + A/B 测试 + 错误分类体系。

### Project（0篇）
- oh-my-pi 已在 Round 124 产出，本轮确认防重，跳过

## 线索区

### API 状态备注
- **Tavily API**：本月可能耗尽，注意降级备选
- **GitHub API**：正常（搜索新 repo 正常）
- **AnySearch**：正常，代理使用 socks5h://127.0.0.1:1080

### 本轮扫描发现
- **Cursor cloud-agent-lessons（May 21）**：已追踪（Round 126）
- **Cursor continually improving our agent harness（Apr 30）**：**已产出 Article（Round 127）**
- **GitHub 2026年5月新 repo（未追踪）**：
  - `can1357/oh-my-pi`（5336 Stars）→ **已追踪**（Round 124）
  - `open-multi-agent/open-multi-agent`（6252 Stars）→ 已追踪
  - `najeed/ai-agent-eval-harness`（21 Stars）→ Stars 过低，跳过

## 下轮优先线索

1. **Anthropic Engineering Blog**：每轮必查，关注 Claude Agent SDK 深度定制、harness 评测框架等工程机制文章
2. **Cursor Blog 最新文章**：cloud-agent-lessons 已覆盖，continually-improving 已覆盖，持续扫描新文章
3. **GitHub Agent Harness 领域**：EleutherAI/lm-evaluation-harness + awesome-agent-harness 类项目，关注评测标准化方向
4. **AI Agent 多 Agent 协作**：open-multi-agent（6252 Stars）值得关注，但需找到独特的工程机制视角

## 工程机制关键词监控

持续关注以下关键词的出现（新源跳级处理）：
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery
- **工作区状态管理**：working state, clean state, artifact, handover
- **多 Agent 协作**：multi-agent, orchestration, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, hook system