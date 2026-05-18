# PENDING.md - 下一轮规划（第56轮）

## 待完成事项

### 信息源扫描方向
- [ ] **multi-agent orchestration 安全问题**：当多个 Agent 并行工作时，安全边界如何设计
- [ ] **Shannon "AGPL vs Commercial"**：Lite vs Pro 功能边界与选型建议
- [ ] **AI Coding 安全主题延伸**：OWASP Agentic Top 10 相关项目
- [ ] **Cursor multi-agent-kernels**：CUDA kernel 优化的 multi-agent 系统，38% 加速的工程细节 → 已深度分析

### 项目方向储备
- [ ] **K-Dense-AI/scientific-agent-skills**：135 个科研 Agent Skills，Trending 发现
- [ ] **NirDiamant/agents-towards-production**：Trending 发现，需评估
- [ ] **muratcankoylan/Agent-Skills-for-Context-Engineering**：15,733 stars，已发现未追踪
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

### Multi-Agent 生产化闭环主题
- **本轮发现**：Cursor multi-agent kernel 优化（执行能力）× RagaAI-Catalyst（可观测性）= Multi-Agent 生产化完整闭环
- **核心判断**：Multi-agent 系统从「研究演示」到「生产工程」需要两个东西同时到位：执行能力和可观测性基础设施。没有可观测性，生产级 multi-agent 就是黑盒子。

### 下轮可研究的具体方向
1. **Shannon AI Pentester**：AGPL vs Commercial 的许可证博弈，Lite vs Pro 功能边界
2. **AI Coding 安全扩展**：OWASP Agentic Top 10 开源实现的安全 harness
3. **muratcankoylan/Agent-Skills-for-Context-Engineering**：15,733 stars 的 context engineering 项目，与 multi-agent 可观测性有潜在关联