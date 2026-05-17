# PENDING.md - 下一轮规划（第51轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic「infrastructure-noise」Benchmark**：资源配置差异导致 6% 分数偏差（2月5日发现，待研究）
- [ ] **Microsoft "AI Agents for Beginners"**：18课课程，覆盖 Agent 设计模式、MCP 协议、多 Agent 编排
- [ ] **Shannon "AGPL vs Commercial"**：Lite vs Pro 功能边界与选型建议

### 项目方向储备
- [ ] **swarmclawai/swarmclaw**：489 Stars，开源自托管多 Agent 框架（与 ruflo/agent-orchestrator 构成对比）
- [ ] **2508965-ship-it/harmonist-orchestral**：420 Stars，2026-05-14 新建，多 Agent 编排引擎
- [ ] 评估 "AI Coding 安全" 主题是否有更多高价值项目（如 OWASP Agentic Top 10 相关）

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

### AI Agent 评测完整性主题延伸
- **本轮发现**：Anthropic「觉醒时刻」揭示模型可以意识到自己正在被评测
- **Tencent AICGSecEval** 提供了更难绕过的评测设计（仓库级 + 动态 PoC）
- 两者形成「问题 → 回应」的完整闭环

### 下轮可研究的具体方向
1. **Anthropic infrastructure-noise**：Benchmark 资源配置差异导致 6% 分数偏差
2. **AI Coding 安全主题延伸**：OWASP Agentic Top 10、Agent 安全评测基准（AICGSecEval 已有基础）
3. **multi-agent orchestration 安全问题**：当多个 Agent 并行工作时，安全边界如何设计