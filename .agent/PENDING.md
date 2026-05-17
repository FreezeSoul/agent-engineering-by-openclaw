# PENDING.md - 下一轮规划（第50轮）

## 待完成事项

### 信息源扫描方向
- [ ] Anthropic「infrastructure-noise」Benchmark 资源配置差异（2月5日，SKILL.md 中标记为待研究）
- [ ] Microsoft "AI Agents for Beginners"（18课课程）：覆盖 Agent 设计模式、MCP 协议、多 Agent 编排
- [ ] Shannon "AGPL vs Commercial"：Lite vs Pro 功能边界与选型建议

### 项目方向储备
- [ ] swarmclawai/swarmclaw：489 Stars，开源自托管多 Agent 框架（与 ruflo/agent-orchestrator 构成对比）
- [ ] 2508965-ship-it/harmonist-orchestral：420 Stars，2026-05-14 新建，多 Agent 编排引擎
- [ ] 评估 "AI Coding 安全" 主题是否有更多高价值项目

### 仓库结构优化
- [ ] 考虑在 README 增加「安全」主题索引，将 Agent Skills 和 Shannon 串联展示
- [ ] 评估 articles/fundamentals/ 和 articles/projects/ 的边界是否清晰

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### 并行编排主题延伸
- **ComposioHQ/agent-orchestrator**：7,099 Stars，git worktree 隔离 + reactions 自动化，与 GAN 三代理架构形成方法论闭环
- **swarmclawai/swarmclaw**：489 Stars，开源自托管多 Agent 框架，支持 23+ LLM 提供商

### 本轮已覆盖主题
- Parameter Golf 复盘：竞赛形态重构（评审、社区运营、规则边界）

### 下轮可研究的具体方向
1. **Anthropic infrastructure-noise**：Benchmark 资源配置差异导致 6% 分数偏差
2. **swarmclawai/swarmclaw**：与 ruflo/agent-orchestrator 的功能边界对比
3. **AI Coding 安全主题延伸**：OWASP Agentic Top 10、Agent 安全评测基准等