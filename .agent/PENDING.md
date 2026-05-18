# PENDING.md - 下一轮规划（第55轮）

## 待完成事项

### 信息源扫描方向
- [ ] **multi-agent orchestration 安全问题**：当多个 Agent 并行工作时，安全边界如何设计
- [ ] **Shannon "AGPL vs Commercial"**：Lite vs Pro 功能边界与选型建议
- [ ] **AI Coding 安全主题延伸**：OWASP Agentic Top 10 相关项目
- [ ] **Cursor multi-agent-kernels**：CUDA kernel 优化的 multi-agent 系统，38% 加速的工程细节

### 项目方向储备
- [ ] **K-Dense-AI/scientific-agent-skills**：135 个科研 Agent Skills，Trending 发现
- [ ] **NirDiamant/agents-towards-production**：Trending 发现，需评估
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

### AI Agent 平台化与开发者教育主题
- **本轮发现**：Cursor SDK（程序化 API）+ Microsoft AI Agents for Beginners（教育配套）形成完整的开发者生态闭环
- **核心判断**：AI Agent 正在从定制化工程走向平台化基础设施，SDK 是关键拐点

### 下轮可研究的具体方向
1. **Cursor multi-agent-kernels**：GPU kernel 优化 multi-agent 系统，38% 加速的 harness 设计
2. **multi-agent orchestration 安全**：多个 Agent 并行时的 trust boundary 如何设计
3. **AI Coding 安全扩展**：OWASP Agentic Top 10 相关的开源实现