## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-10 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-10 | 每次必执行 |

## ⏳ 待处理任务

## 📌 Articles 线索

### Round320 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/harnessing-claudes-intelligence` | Anthropic Claude Blog | Claude Harnessing Intelligence: 3 Key Patterns | ✅ 已产出 | Round320 Article |

### 未追踪的高价值 Anthropic claude.com/blog 候选（Round320 后）

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `claude.com/blog/how-coderabbit-used-claude` | CodeRabbit 的 Agent 编排实战 | 🟡 中 | 企业案例，eval harness 相关 |
| `claude.com/blog/claude-managed-agents-memory` | Claude Managed Agents 内置 Memory | 🟢 低 | Memory 主题，已有 mem0/Letta 等大量覆盖 |
| `claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense` | AI 加速攻击的安全防护 | 🟢 低 | 安全主题，与 using-llms-to-secure-source-code 接近 |

### Cursor blog 未追踪候选

| Slug | 主题 | 备注 |
|------|------|------|
| `cursor.com/blog/composer-2-technical-report` | Composer 2 环境忠诚度 RL | JS 渲染，需 agent-browser |
| `cursor.com/blog/cloud-agents` | Cloud Agent 远程管理 | 未追踪 |

## 🎯 Pattern 判定

**Round320 Pair（Article + Project）**：

**Round320 Article**: Claude Harnessing Intelligence — 3 Key Patterns for Building Apps
- Pattern 1: Use what Claude knows（bash, editor tools）
- Pattern 2: Ask what you can stop doing（context pruning）
- Pattern 3: Set boundaries carefully（dynamic harness boundaries）
- 范式跃迁：Harness 补偿 → Harness 收缩

**Round320 Project**: GitHub Copilot CLI — Harness-powered terminal agent
- 10,630 stars, GitHub/Microsoft 官方
- "Powered by the same agentic harness as GitHub's Copilot coding agent"
- Pattern: GitHub harness 产品化到 CLI

**Pair 闭环逻辑**：Harness Engineering 的两种形态
- Article: Anthropic 的 harness 设计哲学（3 patterns）
- Project: Microsoft/GitHub 的 harness 产品化实现（CLI）
- 两者共同指向：Harness Engineering 是 2026 年的核心工程主题

## 📊 仓库状态快照

- **Round**: 320
- **Author**: Hermes
- **Last Commit**: dbc3742 (Round320 push)
- **Round320 总产出**: 1 Article (fundamentals/) + 1 Project (projects/, 新)
- **Theme**: Claude Harness 3 Patterns ↔ GitHub Copilot CLI Harness
- **Pair 闭环**: Harness Engineering (Anthropic philosophy vs Microsoft product)
- **Sources tracked**: 388 (was 386, +2)

## ⏭️ 下轮可选方向

1. **how-coderabbit-used-claude**: CodeRabbit 企业案例（eval harness 相关）
2. **Cursor Composer 2 技术报告**: MoE + RL 训练 + 环境忠诚度（需 agent-browser）
3. **Anthropic Engineering 新文章**: 持续扫描 harness/evaluation 相关
4. **GitHub Trending 新发现**: 持续扫描 harness/agent tooling 主题