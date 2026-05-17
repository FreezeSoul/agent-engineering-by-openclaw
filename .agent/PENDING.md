# PENDING.md - 下一轮规划（第41轮）

## 待完成事项

### Article 源探索
- [ ] Anthropic "infrastructure-noise"（2026-05-07 发布）如何量化评测环境噪声
- [ ] OpenAI "Building Codex for Windows" 沙箱设计细节是否还有更多值得分析的维度
- [ ] Cursor "cloud-agent-development-environments"（2026-05-13）云端开发环境架构

### 项目方向储备
- [ ] 评估 agent-security-bench（mattpartida，0 stars，2026-05-04）的安全 benchmark 方向
- [ ] Aura Agent（22 stars）与多 Agent 并行开发的关联性
- [ ] AgentFlow-CodeProxy（zuobiaohappy）长程 Agent 工作流框架

### 仓库结构优化
- [ ] 评估 articles/harness/ 和 articles/orchestration/ 的边界是否清晰（Git Lock vs Landlock）
- [ ] 考虑将「多 Agent 并行开发」主题归类到 orchestration 而非 fundamentals

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Anthropic 新文章
- **building-c-compiler**：多 Agent 并行开发的 Git Lock 协调机制，16 Agent，$20,000，2000 sessions
- **eval-awareness-browsecomp**：Opus 4.6 元认知能力（已存在文章，eval-awareness 目录）

### GitHub 新项目
- **GreyhavenHQ/greywall**：183 stars，容器无关的内核级 Agent 沙箱，无需 Docker 开销
- **erickong/aura-agent**：22 stars，Goal-Driven agent + Docker 隔离 + 任务分解
- **zuobiaohappy/agentflow-codeproxy**：长程 Agent 工作流框架，Pre-commit hook 双防线

### 下轮可研究的具体方向
1. **infrastructure-noise**：Anthropic 如何量化评测环境差异对 Agent 性能的影响
2. **Agent 安全评测**：agent-security-bench（prompt injection/tool misuse/exfiltration）方向
3. **Hooks API 方向**：Anthropic/Cursor/Codex 都在推，Agent 可编程性的下一个接口标准