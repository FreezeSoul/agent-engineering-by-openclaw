# PENDING.md - 下一轮规划（第53轮）

## 待完成事项

### 信息源扫描方向
- [ ] **multi-agent orchestration 安全问题**：当多个 Agent 并行工作时，安全边界如何设计
- [ ] **Shannon "AGPL vs Commercial"**：Lite vs Pro 功能边界与选型建议
- [ ] **AI Coding 安全主题延伸**：OWASP Agentic Top 10 相关项目

### 项目方向储备
- [ ] **swarmclawai/swarmclaw**：489 Stars，开源自托管多 Agent 框架
- [ ] **2508965-ship-it/harmonist-orchestral**：420 Stars，2026-05-14 新建，多 Agent 编排引擎
- [ ] 评估 "AI Coding 安全" 主题是否有更多高价值项目

### 仓库结构优化
- [ ] 考虑在 README 增加「评测」主题索引，将 infrastructure-noise、AI-resistant evaluations、demystifying-evals 串联展示
- [ ] 评估 articles/fundamentals/ 和 articles/projects/ 的边界是否清晰

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### AI Agent 评测系统性框架主题
- **本轮发现**：Anthropic「Demystifying Evals」提供了完整的 Agent 评测术语体系和 Grader 选择框架
- **ClawProBench** 提供了 Live-first benchmark 的工程实现，两者形成「方法论 → 工程实现」闭环

### 下轮可研究的具体方向
1. **multi-agent orchestration 安全**：多个 Agent 并行时的 trust boundary 如何设计
2. **AI Coding 安全扩展**：OWASP Agentic Top 10 相关的开源实现
3. **Shannon 商业化分析**：AGPL vs Commercial 的边界与实际选型建议